#!/usr/bin/env python3
"""self_test.py - offline checks for publish_manifest.py.

Run from inside this folder with no arguments, no network:

    python3 self_test.py

Builds its own throwaway artifact folder in a temp dir, drives
publish_manifest.py's real code on it, and compares what comes out with
what should. The real folder is read too: its upload set is the data/
tree plus README.md, which in this checkout is data/data.csv plus
README.md - two entries, never three. Nothing is written outside the temp
dir. Exits 0 only when every check passes. Stdlib only.
"""

import hashlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import publish_manifest as pm  # noqa: E402

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


def main():
    # --- the real folder in this checkout ---
    # The upload set is exactly the data/ tree plus README.md. This folder
    # ships data/data.csv and README.md, so collect() returns 2 entries.
    # An earlier version of this test demanded ">= 3" entries and failed on
    # a folder that was in fact correct; the assertions below say what must
    # hold instead of naming a third file the set cannot contain.
    mine = pm.collect(HERE)
    check(all(e[2] is not None for e in mine),
          "every upload-set source in this folder exists on disk")
    check(any(s == "README.md" for s, _, _, _ in mine),
          "this folder's upload set carries README.md")
    check(any(s.startswith("data/") for s, _, _, _ in mine),
          "this folder's upload set carries at least one data/ file")
    check(len(mine) >= 2, "this folder has the data/ file plus README.md")
    check(pm.check_two_entries(mine) is True, "this folder's upload set is valid")
    check(all(s.startswith("data/") or s == "README.md" for s, _, _, _ in mine),
          "nothing outside data/... plus README.md is in this folder's set")

    tmpd = tempfile.mkdtemp(prefix="glb-fixture-self-test-")
    root = build_fixture(tmpd)

    entries = pm.collect(root)
    check(len(entries) == 3, "fixture upload set is exactly 3 files")
    check(pm.check_two_entries(entries) is True, "fixture upload set is valid")

    dests = sorted(d for _, d, _, _ in entries)
    check(dests == ["README.md", "data/a.csv", "data/b.csv"],
          "destinations keep the data/ tree and README.md name")

    want = {
        "data/a.csv": (len(CSV_A.encode()), hashlib.sha256(CSV_A.encode()).hexdigest()),
        "data/b.csv": (len(CSV_B.encode()), hashlib.sha256(CSV_B.encode()).hexdigest()),
        "README.md": (len(CARD.encode()), hashlib.sha256(CARD.encode()).hexdigest()),
    }
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
    check(after[2] == len(CSV_A_LONG.encode()),
          "byte count equals the length of the bytes on disk")

    changed.write_text(CSV_A.replace("a,b", "a,c"), encoding="utf-8")
    same_len = [e for e in pm.collect(root) if e[0] == "data/a.csv"][0]
    check(same_len[3] != before[3], "same-length change still changes the sha256")
    check(same_len[2] == before[2],
          "same-length change keeps the byte count (correct, not a bug)")

    manifest = pm.manifest_text(pm.collect(root))
    check("README.md" in manifest and "data/a.csv" in manifest,
          "manifest names both upload entries")
    check("self_test.py" not in manifest,
          "manifest does not list the test file")
    check("https://" not in manifest and "huggingface" not in manifest,
          "manifest states no URL and no host")

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
    check(pm.check_two_entries(extra) is True,
          "an extra data/ file is still an upload-set path")

    (root / "stray.txt").write_text("x\n", encoding="utf-8")
    stray_manifest = pm.manifest_text(pm.collect(root))
    check("stray.txt" not in stray_manifest,
          "a file outside the two sources is not uploaded")

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

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
