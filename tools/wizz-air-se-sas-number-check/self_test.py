#!/usr/bin/env python3
"""Standalone offline self-test. No args, no network.
Exits 0 only when every check passes."""
import json
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check as c
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def main():
    check(c.normalize_phone("+46 8 522 170 00") == "+46852217000", "normalise +46 with spaces")
    check(c.normalize_phone("0046-8-522-170-00") == "0046852217000", "normalise 00 number digits only")
    check(c.normalize_phone("") == "" and c.normalize_phone(None) == "", "empty phone normalises empty")
    check(c.classify_entity("Wizz Air") == "wizz_air", "Wizz Air classified as airline")
    check(c.classify_entity("SAS Scandinavian Airlines") == "sas_airline", "SAS airline classified")
    check(c.classify_entity("SAS Institute software") == "sas_software", "SAS software classified separately")
    check(c.classify_entity("SAS") == "sas_airline", "bare SAS defaults to airline label")
    check(c.classify_entity("") == "unknown", "empty entity unknown")
    # Core UNKNOWN rule: discussion 22 not retrieved -> UNKNOWN even with numbers.
    r = c.evaluate("Wizz Air", "+46 8 000 000", ["+468000000"], False, "")
    check(r["verdict"] == "UNKNOWN" and "discussion text not retrieved" in r["reasons"], "unretrieved discussion -> UNKNOWN")
    r = c.evaluate("Wizz Air", "+46 8 000 000", [], True, "some retrieved text")
    check(r["verdict"] == "UNKNOWN", "no official numbers -> UNKNOWN, not MISMATCH")
    r = c.evaluate("Wizz Air", "", ["+468000000"], True, "text")
    check(r["verdict"] == "UNKNOWN", "no claimed number -> UNKNOWN")
    # SAS software must never be treated as airline evidence.
    r = c.evaluate("SAS Institute software", "+46852217000", ["+46852217000"], True, "text")
    check(r["verdict"] == "UNKNOWN" and r["entity"] == "sas_software", "SAS software -> UNKNOWN, not MATCH")
    # MATCH / MISMATCH only with full evidence.
    r = c.evaluate("SAS Scandinavian Airlines", "+46 8 522 170 00", ["+46852217000"], True, "text")
    check(r["verdict"] == "MATCH", "full evidence, equal number -> MATCH")
    r = c.evaluate("Wizz Air", "+46 8 111 111", ["+468222222"], True, "text")
    check(r["verdict"] == "MISMATCH", "full evidence, differing number -> MISMATCH")
    r = c.evaluate("", "+468111111", ["+468222222"], True, "text")
    check(r["verdict"] == "UNKNOWN", "unknown airline -> UNKNOWN")
    # CLI round-trip offline.
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "in.json"; o = Path(td) / "out.json"
        p.write_text(json.dumps({"claimed_airline": "Wizz Air", "claimed_number": "+46 8 111 111", "official_numbers": ["+468222222"], "discussion_text_retrieved": True, "discussion_text": "text"}), encoding="utf-8")
        check(c.main(["check.py", str(p), "--out", str(o)]) == 0, "CLI writes output")
        data = json.loads(o.read_text(encoding="utf-8"))
        check(data["verdict"] == "MISMATCH", "CLI verdict correct")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
