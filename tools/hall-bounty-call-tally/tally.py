#!/usr/bin/env python3
"""Offline tally of available authorized receipts.
Reads a CSV of receipts, deduplicates by receipt_id, applies a
configurable amount threshold, buckets by ISO week (Monday start),
marks missing evidence UNKNOWN, and writes a JSON tally.
No network. Fixture data used in tests is synthetic.
"""
import csv
import json
import sys
from collections import OrderedDict
from datetime import date

REQUIRED = ["receipt_id", "date", "amount_cents", "authorized", "evidence"]

def parse_date(s):
    y, m, d = (int(x) for x in s.strip().split("-"))
    return date(y, m, d)

def week_start(d):
    # ISO week: Monday of the week containing d.
    return d.toordinal() - d.weekday()

def week_label(d):
    ws = date.fromordinal(week_start(d))
    iso = d.isocalendar()
    return "%04d-W%02d" % (iso[0], iso[1])

def tally(rows, threshold_cents=100):
    seen = {}
    duplicates = []
    weeks = OrderedDict()
    unknown = []
    ineligible = []
    for r in rows:
        rid = (r.get("receipt_id") or "").strip()
        if not rid:
            ineligible.append({"receipt_id": rid, "reason": "missing receipt_id"})
            continue
        if rid in seen:
            duplicates.append(rid)
            continue
        seen[rid] = r
        try:
            d = parse_date(r.get("date", ""))
            amount = int(str(r.get("amount_cents", "")).strip())
        except Exception:
            ineligible.append({"receipt_id": rid, "reason": "bad date or amount"})
            continue
        authorized = (r.get("authorized") or "").strip().lower() == "yes"
        evidence = (r.get("evidence") or "").strip().lower()
        ev = evidence if evidence in ("present", "missing") else "missing"
        label = week_label(d)
        ws = date.fromordinal(week_start(d)).isoformat()
        bucket = weeks.setdefault(label, {"week": label, "week_start": ws,
            "eligible_count": 0, "eligible_cents": 0, "unknown_count": 0,
            "ineligible_count": 0, "receipt_ids": []})
        bucket["receipt_ids"].append(rid)
        if not authorized:
            bucket["ineligible_count"] += 1
            ineligible.append({"receipt_id": rid, "reason": "not authorized"})
            continue
        if ev != "present":
            bucket["unknown_count"] += 1
            unknown.append({"receipt_id": rid, "week": label, "evidence": "UNKNOWN"})
            continue
        if amount < threshold_cents:
            bucket["ineligible_count"] += 1
            ineligible.append({"receipt_id": rid, "reason": "below threshold"})
            continue
        bucket["eligible_count"] += 1
        bucket["eligible_cents"] += amount
    week_list = [weeks[k] for k in sorted(weeks)]
    for b in week_list:
        b["receipt_ids"] = sorted(b["receipt_ids"])
    return {
        "synthetic_fixtures_only": True,
        "threshold_cents": threshold_cents,
        "total_rows_seen": len(rows),
        "unique_receipts": len(seen),
        "duplicates": sorted(duplicates),
        "unknown_evidence": unknown,
        "ineligible": ineligible,
        "weeks": week_list,
        "eligible_count": sum(b["eligible_count"] for b in week_list),
        "eligible_cents": sum(b["eligible_cents"] for b in week_list),
    }

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or any(c not in reader.fieldnames for c in REQUIRED):
            raise ValueError("CSV must have columns: %s" % ",".join(REQUIRED))
        return list(reader)

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 tally.py RECEIPTS.csv [--threshold-cents N] [--out FILE]")
        return 0 if len(argv) >= 2 else 2
    path = argv[1]
    threshold = 100
    out = None
    i = 2
    while i < len(argv):
        if argv[i] == "--threshold-cents" and i + 1 < len(argv):
            threshold = int(argv[i+1]); i += 2
        elif argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i+1]; i += 2
        else:
            print("unknown argument: %s" % argv[i]); return 2
    result = tally(load_csv(path), threshold)
    text = json.dumps(result, indent=2, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
