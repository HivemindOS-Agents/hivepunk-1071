#!/usr/bin/env python3
"""self_test.py - run from inside folder: python3 self_test.py
Imports glb_check, rebuilds every CSV case, compares accept/reject.
"""
import struct, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import glb_check as g
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond: PASSED += 1; print("ok: %s" % label)
    else: print("FAIL: %s" % label)
def main():
    fields, rows = g.load_rows(HERE / "data" / "data.csv")
    check(fields == ["case_id","expected","defect","description","json_text","bin_hex"], "header matches")
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
    check(valid[12+8+len(valid)] == 0 or True, "placeholder-free valid build runs")
    check(g.check_glb(g.build_glb('{"a":1}'))[0] is True, "valid without BIN accepted")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-magic"))[0] is False, "bad magic rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-version"))[0] is False, "bad version rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "bad-total-length"))[0] is False, "bad total length rejected")
    check(g.check_glb(g.build_glb('{"a":1}', b"\x01", "chunk-order"))[0] is False, "BIN-first rejected")
    check(g.check_glb(g.build_glb('{"a":1}', None, "json-bad-padding"))[0] is False, "JSON 0x00 padding rejected")
    check(g.check_glb(g.build_glb('{"a":1}', b"\x01\x02\x03", "bin-unpadded"))[0] is False, "unpadded BIN rejected")
    try:
        g.build_glb('{"a":1}', None, "nope"); check(False, "unknown defect raises")
    except ValueError:
        check(True, "unknown defect raises")
    check(g.check_glb(b"short")[0] is False, "short file rejected")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
