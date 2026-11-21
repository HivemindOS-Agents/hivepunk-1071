#!/usr/bin/env python3
"""Standalone offline self-test. No args, no network.
Covers thresholds, duplicates and week boundaries on synthetic
fixtures. Exits 0 only when every check passes."""
import csv
import json
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import tally as t
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def row(rid, d, amt, auth="yes", ev="present"):
    return {"receipt_id": rid, "date": d, "amount_cents": str(amt),
            "authorized": auth, "evidence": ev}
def main():
    # Thresholds: at threshold counts, one below does not.
    r = t.tally([row("a", "2026-11-16", 100), row("b", "2026-11-16", 99)], 100)
    check(r["eligible_count"] == 1 and r["eligible_cents"] == 100, "threshold: 100 eligible, 99 not at threshold 100")
    r0 = t.tally([row("a", "2026-11-16", 0)], 0)
    check(r0["eligible_count"] == 1, "threshold 0: zero amount eligible")
    # Duplicates: first wins, second ignored even if larger.
    r = t.tally([row("dup", "2026-11-16", 100), row("dup", "2026-11-16", 9999)], 100)
    check(r["eligible_count"] == 1 and r["eligible_cents"] == 100 and r["duplicates"] == ["dup"], "duplicates counted once, first wins")
    # Missing evidence -> UNKNOWN, excluded from eligible.
    r = t.tally([row("m", "2026-11-16", 500, ev="missing"), row("ok", "2026-11-16", 500)], 100)
    check(r["eligible_count"] == 1 and r["unknown_evidence"][0]["receipt_id"] == "m" and r["unknown_evidence"][0]["evidence"] == "UNKNOWN", "missing evidence marked UNKNOWN and excluded")
    # Unauthorized excluded.
    r = t.tally([row("u", "2026-11-16", 500, auth="no")], 100)
    check(r["eligible_count"] == 0 and r["ineligible"][0]["reason"] == "not authorized", "unauthorized receipt ineligible")
    # Week boundaries: Sunday 2026-11-22 vs Monday 2026-11-23 differ.
    sun = t.tally([row("s", "2026-11-22", 100)], 100)
    mon = t.tally([row("m2", "2026-11-23", 100)], 100)
    check(sun["weeks"][0]["week"] != mon["weeks"][0]["week"], "week boundary: Sunday and Monday in different ISO weeks")
    check(sun["weeks"][0]["week_start"] == "2026-11-16" and mon["weeks"][0]["week_start"] == "2026-11-23", "week_start is Monday of each week")
    # Year boundary: 2025-12-29 (Mon) .. 2026-01-04 (Sun) share week 2026-W01 label handling via ISO.
    w = t.tally([row("y1", "2025-12-29", 100), row("y2", "2026-01-04", 100)], 100)
    check(len(w["weeks"]) == 1 and w["weeks"][0]["eligible_count"] == 2, "year boundary: Dec 29 and Jan 4 same ISO week")
    w2 = t.tally([row("y3", "2026-01-05", 100)], 100)
    check(w2["weeks"][0]["week_start"] == "2026-01-05", "week after year boundary starts 2026-01-05")
    # CLI round-trip via temp CSV, offline.
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "r.csv"; o = Path(td) / "out.json"
        p.write_text("receipt_id,date,amount_cents,authorized,evidence\nx,2026-11-16,250,yes,present\n", encoding="utf-8")
        check(t.main(["tally.py", str(p), "--threshold-cents", "100", "--out", str(o)]) == 0, "CLI writes output file")
        data = json.loads(o.read_text(encoding="utf-8"))
        check(data["eligible_cents"] == 250 and data["synthetic_fixtures_only"] is True, "CLI output JSON correct and marked synthetic")
    check(t.tally([], 100)["weeks"] == [], "empty input gives empty weeks")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
