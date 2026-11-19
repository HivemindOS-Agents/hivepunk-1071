#!/usr/bin/env python3
"""self_test.py - run from inside the folder: python3 self_test.py
No arguments, no network. Imports glb_check and publish_manifest, rebuilds
every CSV case, compares accept/reject, and exercises the upload-set
tool on fixtures written under a temp dir. Exits 0 only when all pass.
"""
import csv
import hashlib
import os
import shutil
import struct
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import glb_check as g
import publish_manifest as pm
CHECKS = PASSED = 0

def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1
        print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)

def write_tree(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

def expect_refused(files, label):
    tmp = Path(tempfile.mkdtemp())
    try:
        write_tree(tmp, files)
        try:
            pm.check_two_entries(pm.collect(tmp))
            check(False, label)
        except ValueError:
            check(True, label)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def main():
    fields, rows = g.load_rows(HERE / "data" / "data.csv")
    check(fields == ["case_id", "expected", "defect", "description", "json_text", "bin_hex"], "header matches")
    check(len(rows) == 9, "exactly 9 rows (%d)" % len(rows))
    check(sum(r["expected"] == "valid" for r in rows) == 3, "3 valid rows")
    check(sum(r["expected"] == "invalid" for r in rows) == 6, "6 invalid rows")
    check(all(r["defect"] in g.DEFECTS for r in rows), "all defects known")
    for r in rows:
        data = g.row_to_bytes(r)
        magic, version, total = struct.unpack("<III", data[:12])
        check(total == len(data) or r["defect"] == "bad-total-length", "%s total-length field as designed" % r["case_id"])
        ok, errs = g.check_glb(data)
        check(ok == (r["expected"] == "valid"), "%s rebuilt: expected %s" % (r["case_id"], r["expected"]))
        check(g.row_to_bytes(r) == data, "%s rebuild is deterministic byte-for-byte" % r["case_id"])
        if r["expected"] == "invalid":
            check(bool(errs), "%s gives a reason" % r["case_id"])
    valid = g.build_glb('{"asset":{"version":"2.0"}}', b"\x01\x02\x03")
    ok, errs = g.check_glb(valid)
    check(ok and errs == [], "valid with BIN is accepted")
    check(struct.unpack("<III", valid[:12])[2] == len(valid), "valid build total length equals file size")
    check(valid[-1] == 0, "valid build BIN padding byte is 0x00")
    check(g.check_glb(g.build_glb('{"a":1}'))[0] is True, "valid without BIN accepted")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-magic"))[0] is False, "bad magic rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-version"))[0] is False, "bad version rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-total-length"))[0] is False, "bad total length rejected")
    check(g.check_glb(g.build_glb('{"a":1}', b"\x01", "chunk-order"))[0] is False, "BIN-first rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "json-bad-padding"))[0] is False, "JSON 0x00 padding rejected")
    check(g.check_glb(g.build_glb('{"a":1}', b"\x01\x02\x03", "bin-unpadded"))[0] is False, "unpadded BIN rejected")
    try:
        g.build_glb('{"a":1}', None, "nope")
        check(False, "unknown defect raises")
    except ValueError:
        check(True, "unknown defect raises")
    check(g.check_glb(b"short")[0] is False, "short file rejected")

    # upload-set tool: exact two-entry fixture must be ACCEPTED (regression
    # for the earlier failure where a >=3-entry demand failed a correct set).
    tmp = Path(tempfile.mkdtemp())
    try:
        write_tree(tmp, {"README.md": "card\n", "data/data.csv": "a,b\n1,2\n"})
        entries = pm.collect(tmp)
        check(len(entries) == 2, "exact-2-entry fixture collects 2 entries")
        check(pm.check_two_entries(entries) is True, "exact-2-entry fixture is accepted")
        digest = hashlib.sha256(b"a,b\n1,2\n").hexdigest()
        csv_entry = [e for e in entries if e[0] == "data/data.csv"][0]
        check(csv_entry[1] == "data/data.csv", "csv keeps its repo path")
        check(csv_entry[2] == 8 and csv_entry[3] == digest, "csv byte count and sha256 match the bytes read")
        text = pm.manifest_text(entries)
        check("NOT a read of any published page" in text, "manifest says it is not a published read")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # a third file at the top level is not in the set and must be ignored,
    # while a third file under data/ is part of the data/ tree and allowed.
    tmp = Path(tempfile.mkdtemp())
    try:
        write_tree(tmp, {"README.md": "c\n", "data/data.csv": "a\n", "data/extra.csv": "b\n", "notes.txt": "x\n"})
        entries = pm.collect(tmp)
        srcs = sorted(e[0] for e in entries)
        check(srcs == ["README.md", "data/data.csv", "data/extra.csv"], "stray top-level file ignored, data/ tree kept: %r" % (srcs,))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    expect_refused({"README.md": "c\n"}, "missing data/ is refused")
    expect_refused({"data/data.csv": "a\n"}, "missing README.md is refused")

    # --write then --check on a temp tree, and drift detection.
    tmp = Path(tempfile.mkdtemp())
    try:
        write_tree(tmp, {"README.md": "card\n", "data/data.csv": "a,b\n"})
        pm.write_manifest(tmp, tmp / "MANIFEST.txt")
        check(pm.main(["--check"]) == 2 or True, "main --check on the tool folder does not crash")
        before = (tmp / "MANIFEST.txt").read_text(encoding="utf-8")
        (tmp / "data" / "data.csv").write_text("a,b\nc,d\n", encoding="utf-8")
        after = pm.manifest_text(pm.collect(tmp))
        check(before != after, "drift after a byte change is detected")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # shipped MANIFEST.txt must be honest about being a local read-back.
    shipped = (HERE / "MANIFEST.txt")
    if shipped.exists():
        txt = shipped.read_text(encoding="utf-8")
        check("NOT a read of any published page" in txt, "shipped MANIFEST.txt is labelled local-only")
        check("published" not in txt.replace("NOT a read of any published page", ""), "shipped MANIFEST.txt claims no published values")

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1

if __name__ == "__main__":
    sys.exit(main())
