#!/usr/bin/env python3
"""self_test.py - offline checks for check_publish.py. No network."""
import csv, hashlib, json, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_publish as cp

CHECKS = 0; PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: " + label)
    else:
        print("FAIL: " + label)

HEADER = "case_id,rule,expected_bytes,source,read_back\n"
ROWS = [
    "a1,header 12 bytes,12,spec 3.2,not-opened",
    "a2,chunk header 8,8,spec 3.3,not-opened",
    'a3,chunk data padded to 4,"(len+3) AND NOT 3",spec 3.3,not-opened',
    "a4,json type,4,spec 3.3,not-opened",
    "a5,bin type,4,spec 3.3,not-opened",
    "a6,magic,4,spec 3.2,not-opened",
    "a7,version,4,spec 3.2,not-opened",
    "a8,total length,4,spec 3.2,not-opened",
    "a9,chunk length field,4,spec 3.3,not-opened",
    "a10,chunk type field,4,spec 3.3,not-opened",
]
README = "# GLB\n\n10 rows in data/data.csv and README.md. No URL stated.\n"

def build(root, csv_text=None, readme_text=None):
    root = Path(root); (root / "data").mkdir(parents=True)
    (root / "data" / "data.csv").write_text(HEADER + "\n".join(ROWS) + "\n" if csv_text is None else csv_text, encoding="utf-8")
    (root / "README.md").write_text(README if readme_text is None else readme_text, encoding="utf-8")
    return root

def main():
    good = build(tempfile.mkdtemp(prefix="glb-check-good-"))
    r = cp.check_folder(good)
    check(r["passed"] is True, "good fixture passes")
    check(len(r["checks"]) >= 8, "good fixture has at least 8 checks")
    check(r["files_local_only"]["data/data.csv"]["lines"] == 11, "good csv has 11 lines")
    raw = (good / "data" / "data.csv").read_bytes()
    check(r["files_local_only"]["data/data.csv"]["sha256_local_only"] == hashlib.sha256(raw).hexdigest(), "local sha256 matches bytes on disk")
    parsed = json.loads(json.dumps(r))
    check(parsed["passed"] is True, "result is json-serialisable")
    # wrong row count
    few = build(tempfile.mkdtemp(prefix="glb-check-few-"), csv_text=HEADER + ROWS[0] + "\n")
    check(cp.check_folder(few)["passed"] is False, "9-row-missing fixture fails row count")
    # evaluated / missing alignment expression
    no_align = build(tempfile.mkdtemp(prefix="glb-check-noalign-"), csv_text=HEADER + "\n".join(ROWS).replace("(len+3) AND NOT 3", "4") + "\n")
    res = cp.check_folder(no_align)
    check(res["passed"] is False, "missing alignment expression fails")
    check(any((not c["ok"]) and c["name"] == "alignment expression preserved as text" for c in res["checks"]), "alignment check named in failure")
    # README with guessed URL
    with_url = build(tempfile.mkdtemp(prefix="glb-check-url-"), readme_text=README + "https://example.invalid/dataset\n")
    check(cp.check_folder(with_url)["passed"] is False, "README with a URL fails")
    # missing file
    empty = Path(tempfile.mkdtemp(prefix="glb-check-empty-"))
    check(cp.check_folder(empty)["passed"] is False, "empty folder fails")
    # real shipped sample in this tool folder is not the publish folder; checker must not crash on it
    r2 = cp.check_folder(HERE)
    check(isinstance(r2["passed"], bool), "checker runs on own folder without crashing")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1

if __name__ == "__main__":
    sys.exit(main())
