#!/usr/bin/env python3
"""Offline check: reported airline phone number vs official evidence.

Verdict is UNKNOWN unless all are supplied:
  - discussion text actually retrieved (not assumed),
  - a claimed phone number,
  - official numbers for the claimed airline.
Only then is MATCH / MISMATCH returned. Entity classification
separates SAS Scandinavian Airlines (airline) from SAS software
(SAS Institute); software evidence never proves an airline number.
No network. See README.md.
"""
import json
import re
import sys

def normalize_phone(value):
    if value is None:
        return ""
    s = str(value).strip()
    if s.startswith("+"):
        digits = re.sub(r"\D", "", s[1:])
        return "+" + digits if digits else ""
    digits = re.sub(r"\D", "", s)
    return digits

def classify_entity(name):
    s = str(name or "").strip().lower()
    if not s:
        return "unknown"
    if "wizz" in s:
        return "wizz_air"
    if "sas" in s:
        software_terms = ("software", "institute", "analytics", "data",
                          "programming", "statistical", "ai software")
        if any(t in s for t in software_terms):
            return "sas_software"
        return "sas_airline"
    if "scandinavian" in s:
        return "sas_airline"
    return "unknown"

def evaluate(claimed_airline, claimed_number, official_numbers,
             discussion_text_retrieved=False, discussion_text=""):
    entity = classify_entity(claimed_airline)
    reasons = []
    if not discussion_text_retrieved or not str(discussion_text or "").strip():
        reasons.append("discussion text not retrieved")
    if not claimed_number:
        reasons.append("no claimed number supplied")
    if entity in ("unknown", "sas_software"):
        reasons.append("claimed entity is not an airline: %s" % entity)
    officials = [normalize_phone(n) for n in (official_numbers or [])]
    officials = [n for n in officials if n]
    if not officials:
        reasons.append("no official airline numbers supplied")
    claimed = normalize_phone(claimed_number)
    if reasons:
        return {"verdict": "UNKNOWN", "entity": entity,
                "claimed_normalized": claimed, "official_normalized": officials,
                "reasons": reasons}
    verdict = "MATCH" if claimed in officials else "MISMATCH"
    return {"verdict": verdict, "entity": entity,
            "claimed_normalized": claimed, "official_normalized": officials,
            "reasons": ["compared supplied claimed number to supplied official numbers"]}

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 check.py INPUT.json [--out FILE]")
        print("INPUT.json keys: claimed_airline, claimed_number,")
        print("  official_numbers [], discussion_text_retrieved bool,")
        print("  discussion_text string. Output verdict is UNKNOWN")
        print("unless every input is supplied.")
        return 0 if len(argv) >= 2 else 2
    with open(argv[1], encoding="utf-8") as f:
        data = json.load(f)
    out = None
    i = 2
    while i < len(argv):
        if argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]; i += 2
        else:
            print("unknown argument: %s" % argv[i]); return 2
    result = evaluate(data.get("claimed_airline"), data.get("claimed_number"),
                      data.get("official_numbers"),
                      data.get("discussion_text_retrieved", False),
                      data.get("discussion_text", ""))
    text = json.dumps(result, indent=2, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
