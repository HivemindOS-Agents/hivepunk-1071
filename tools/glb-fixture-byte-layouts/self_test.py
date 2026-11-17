#!/usr/bin/env python3
"""self_test.py - run from inside this folder: python3 self_test.py
Imports and calls the tool's own modules publish_manifest.py and
announce.py on the folder's sample data (data/data.csv, README.md)
and on temp-dir fixtures, comparing what they return. Stdlib only.
"""
import hashlib, json, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import publish_manifest as pm
import announce
CHECKS = 0
PASSED = 0
CARD = "# card\n\nnot a real dataset card in this fixture.\n"
CSV_A = "case_id,rule\na,b\n"
CSV_A_LONG = "case_id,rule\na,cc\n"
CSV_B = "case_id,rule\nc,d\n"
def check(condition, label):
    global CHECKS, PASSED
    CHECKS += 1
    if not condition:
        print("FAIL: %s" % label)
        return
    PASSED += 1
    print("ok: %s" % label)
def build_fixture(root):
    root = Path(root)
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "data" / "a.csv").write_text(CSV_A, encoding="utf-8")
    (root / "data" / "b.csv").write_text(CSV_B, encoding="utf-8")
    (root / "README.md").write_text(CARD, encoding="utf-8")
    return root
def build_two_entry_fixture(root):
    root = Path(root)
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "data" / "data.csv").write_text(CSV_A, encoding="utf-8")
    (root / "README.md").write_text(CARD, encoding="utf-8")
    return root
def main():
    mine = pm.collect(HERE)
    check(all(e[2] is not None for e in mine), "every upload-set source in this folder exists on disk")
    check(any(s == "README.md" for s, _, _, _ in mine), "this folder's upload set carries README.md")
    check(any(s.startswith("data/") for s, _, _, _ in mine), "this folder's upload set carries at least one data/ file")
    check(len(mine) >= 2, "this folder has the data/ file plus README.md")
    check(pm.check_two_entries(mine) is True, "this folder's upload set is valid")
    check(all(s.startswith("data/") or s == "README.md" for s, _, _, _ in mine), "nothing outside data/... plus README.md is in this folder's set")
    check(any(s == "data/data.csv" for s, _, _, _ in mine), "sample data data/data.csv is in the upload set")
    csv_entry = [e for e in mine if e[0] == "data/data.csv"][0]
    csv_bytes = (HERE / "data" / "data.csv").read_bytes()
    check(csv_entry[2] == len(csv_bytes), "sample data.csv size matches bytes on disk")
    check(csv_entry[3] == hashlib.sha256(csv_bytes).hexdigest(), "sample data.csv sha256 matches bytes on disk")
    check(csv_entry[1] == "data/data.csv", "sample data.csv destination keeps its name")
    readme_entry = [e for e in mine if e[0] == "README.md"][0]
    check(readme_entry[1] == "README.md", "sample README.md destination keeps its name")
    manifest = pm.manifest_text(mine)
    check("data/data.csv" in manifest and "README.md" in manifest, "manifest names the sample entries")
    check("self_test.py" not in manifest, "manifest does not list the test file")
    check("https://" not in manifest and "huggingface" not in manifest, "manifest states no URL and no host")
    check(csv_entry[3] in manifest, "manifest carries the sample data.csv sha256")
    two_root = build_two_entry_fixture(tempfile.mkdtemp(prefix="glb-fixture-two-"))
    two = pm.collect(two_root)
    check(len(two) == 2, "exact 2-entry fixture has exactly 2 entries")
    check(pm.check_two_entries(two) is True, "exact 2-entry fixture is valid")
    check(sorted(d for _, d, _, _ in two) == ["README.md", "data/data.csv"], "exact 2-entry fixture keeps data/data.csv and README.md names")
    tmpd = tempfile.mkdtemp(prefix="glb-fixture-self-test-")
    root = build_fixture(tmpd)
    entries = pm.collect(root)
    check(len(entries) == 3, "fixture upload set is exactly 3 files")
    check(pm.check_two_entries(entries) is True, "fixture upload set is valid")
    dests = sorted(d for _, d, _, _ in entries)
    check(dests == ["README.md", "data/a.csv", "data/b.csv"], "destinations keep the data/ tree and README.md name")
    want = {"data/a.csv": (len(CSV_A.encode()), hashlib.sha256(CSV_A.encode()).hexdigest()), "data/b.csv": (len(CSV_B.encode()), hashlib.sha256(CSV_B.encode()).hexdigest()), "README.md": (len(CARD.encode()), hashlib.sha256(CARD.encode()).hexdigest())}
    for source, dest, size, digest in entries:
        exp = want[source]
        check(size == exp[0], "size read for %s" % source)
        check(digest == exp[1], "sha256 read for %s" % source)
    before = [e for e in entries if e[0] == "data/a.csv"][0]
    changed = root / "data" / "a.csv"
    changed.write_text(CSV_A_LONG, encoding="utf-8")
    after = [e for e in pm.collect(root) if e[0] == "data/a.csv"][0]
    check(after[3] != before[3], "a changed byte changes the sha256")
    check(after[2] != before[2], "a longer change changes the byte count")
    check(after[2] == len(CSV_A_LONG.encode()), "byte count equals the length of the bytes on disk")
    changed.write_text(CSV_A.replace("a,b", "a,c"), encoding="utf-8")
    same_len = [e for e in pm.collect(root) if e[0] == "data/a.csv"][0]
    check(same_len[3] != before[3], "same-length change still changes the sha256")
    check(same_len[2] == before[2], "same-length change keeps the byte count (correct, not a bug)")
    manifest2 = pm.manifest_text(pm.collect(root))
    check("README.md" in manifest2 and "data/a.csv" in manifest2, "manifest names both upload entries")
    raised = False
    try:
        pm._safe_child(root, "../secret.txt")
    except ValueError:
        raised = True
    check(raised, "traversal path is refused")
    raised = False
    try:
        pm._safe_child(root, "/etc/passwd")
    except ValueError:
        raised = True
    check(raised, "absolute path is refused")
    (root / "data" / "extra.csv").write_text("x,y\n", encoding="utf-8")
    extra = pm.collect(root)
    check(len(extra) == 4, "an added data/ file appears as an extra entry")
    check(pm.check_two_entries(extra) is True, "an extra data/ file is still an upload-set path")
    (root / "stray.txt").write_text("x\n", encoding="utf-8")
    stray_manifest = pm.manifest_text(pm.collect(root))
    check("stray.txt" not in stray_manifest, "a file outside the two sources is not uploaded")
    empty = Path(tempfile.mkdtemp(prefix="glb-fixture-empty-"))
    raised = False
    try:
        pm.check_two_entries(pm.collect(empty))
    except ValueError:
        raised = True
    check(raised, "an empty folder fails the upload-set check")
    missing_card = Path(tempfile.mkdtemp(prefix="glb-fixture-missing-"))
    (missing_card / "data").mkdir()
    (missing_card / "data" / "a.csv").write_text(CSV_A, encoding="utf-8")
    raised = False
    try:
        pm.check_two_entries(pm.collect(missing_card))
    except ValueError:
        raised = True
    check(raised, "a folder with no README.md fails the upload-set check")
    missing_data = Path(tempfile.mkdtemp(prefix="glb-fixture-nodata-"))
    (missing_data / "README.md").write_text(CARD, encoding="utf-8")
    raised = False
    try:
        pm.check_two_entries(pm.collect(missing_data))
    except ValueError:
        raised = True
    check(raised, "a folder with no data/ file fails the upload-set check")
    good_response = {"url": "https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-byte-layout-fixtures", "files": ["data/data.csv", "README.md"]}
    text = announce.announcement_text(good_response)
    check(good_response["url"] in text, "announce: carries the live URL from the response")
    check("data/data.csv" in text and "README.md" in text, "announce: carries both file names")
    check(announce.check_response(good_response) is True, "announce: exact 2-file response is valid")
    check(announce.check_response({"url": good_response["url"], "files": ["README.md", "data/data.csv"]}) is True, "announce: file order does not matter, set must be exact")
    resp_file = Path(tempfile.mkdtemp(prefix="glb-announce-")) / "response.json"
    resp_file.write_text(json.dumps(good_response), encoding="utf-8")
    check(announce.load_response(str(resp_file))["url"] == good_response["url"], "announce: loads response JSON from a file")
    for bad, label in [({"url": good_response["url"], "files": ["README.md"]}, "announce: one-file response is refused"), ({"url": good_response["url"], "files": ["data/data.csv", "README.md", "extra.txt"]}, "announce: three-file response is refused"), ({"url": good_response["url"], "files": ["data/data.csv", "data/other.csv"]}, "announce: renamed file response is refused"), ({"url": "https://huggingface.co/datasets/other-account/x", "files": ["data/data.csv", "README.md"]}, "announce: wrong-account URL is refused"), ({"files": ["data/data.csv", "README.md"]}, "announce: missing URL is refused"), ({"url": "http://huggingface.co/datasets/hivepunk-1071-f79faf84/x", "files": ["data/data.csv", "README.md"]}, "announce: non-https URL is refused")]:
        try:
            announce.check_response(bad)
            check(False, label)
        except ValueError as exc:
            check("announce:" in str(exc), label)
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
