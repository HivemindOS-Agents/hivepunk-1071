#!/usr/bin/env python3
"""announce.py - build the discussion announcement from an upload response.
No network, no upload. Reads a JSON file holding the upload response
supplied by the platform publish play, validates it, and prints the
announcement to post in the dataset discussion.
Expected JSON shape (field names may be url/dataset_url and files/file_list):
    {"url": "https://huggingface.co/datasets/hivepunk-1071-f79faf84/<slug>",
     "files": ["data/data.csv", "README.md"]}
Validation (each failure raises ValueError starting with "announce:"):
- url is present, https, and under the hivepunk-1071-f79faf84 datasets path;
- files is exactly the two entries data/data.csv and README.md (any order).
Usage:
    python3 announce.py response.json
    python3 announce.py < response.json
Exit 0 prints the announcement; 1 on a refused response; 2 on bad usage.
Stdlib only.
"""
import json
import sys
ACCOUNT_PREFIX = "https://huggingface.co/datasets/hivepunk-1071-f79faf84/"
EXPECTED_FILES = {"README.md", "data/data.csv"}
TITLE = "GLB byte-layout fixtures: 4-byte alignment cases"
def _get(response, *names):
    for name in names:
        if isinstance(response, dict) and response.get(name):
            return response[name]
    return None
def load_response(path=None):
    raw = sys.stdin.read() if path is None else open(path, encoding="utf-8").read()
    try:
        return json.loads(raw)
    except Exception as exc:
        raise ValueError("announce: response is not valid JSON: %s" % exc)
def check_response(response):
    url = _get(response, "url", "dataset_url", "datasetUrl")
    files = _get(response, "files", "file_list", "fileList")
    if not url or not isinstance(url, str):
        raise ValueError("announce: missing url in upload response")
    if not url.startswith("https://"):
        raise ValueError("announce: url is not https: %r" % url)
    if not url.startswith(ACCOUNT_PREFIX):
        raise ValueError("announce: url is not under hivepunk-1071-f79faf84 datasets: %r" % url)
    if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
        raise ValueError("announce: files must be a list of file paths")
    if set(files) != EXPECTED_FILES or len(files) != 2:
        raise ValueError("announce: file list is not exactly data/data.csv and README.md: %r" % (files,))
    return True
def announcement_text(response):
    check_response(response)
    url = _get(response, "url", "dataset_url", "datasetUrl")
    files = _get(response, "files", "file_list", "fileList")
    ordered = [f for f in ["data/data.csv", "README.md"] if f in files]
    lines = ["%s is up on the Hugging Face Hub under hivepunk-1071-f79faf84." % TITLE, "The upload returned exactly two files, carried unchanged: %s." % " and ".join(ordered), "Live dataset URL: %s" % url]
    return "\n".join(lines) + "\n"
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print("usage: python3 announce.py [response.json]", file=sys.stderr)
        return 2
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    try:
        response = load_response(argv[0] if argv else None)
        sys.stdout.write(announcement_text(response))
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    except OSError as exc:
        print("error: announce: cannot read response file: %s" % exc, file=sys.stderr)
        return 2
    return 0
if __name__ == "__main__":
    sys.exit(main())
