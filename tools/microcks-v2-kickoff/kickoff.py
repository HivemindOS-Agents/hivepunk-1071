#!/usr/bin/env python3
"""Offline labelled summary of the Microcks v2 kick-off discussion.

Reads a local JSON file of claims (each labelled FACT, DERIVED
or UNKNOWN) plus goals and open questions, validates labels and
the issue citation, and renders a Markdown summary. It never
fetches the issue and never invents claims: anything not in the
input is reported as UNKNOWN. No network. See README.md.
"""
import json
import sys
from pathlib import Path

ISSUE_URL = "https://github.com/microcks/microcks/issues/2412"
LABELS = ("FACT", "DERIVED", "UNKNOWN")


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    if data.get("issue_url") != ISSUE_URL:
        raise ValueError("issue_url must be %s" % ISSUE_URL)
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be a non-empty list")
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValueError("claim %d must be an object" % i)
        if claim.get("label") not in LABELS:
            raise ValueError("claim %d: label must be one of %s" % (i, ", ".join(LABELS)))
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            raise ValueError("claim %d: text must be a non-empty string" % i)
    for key in ("goals", "open_questions"):
        value = data.get(key)
        if not isinstance(value, list):
            raise ValueError("%s must be a list" % key)
        for i, item in enumerate(value):
            if not isinstance(item, dict) or item.get("label") not in LABELS or not str(item.get("text", "")).strip():
                raise ValueError("%s %d: needs label in %s and non-empty text" % (key, i, ", ".join(LABELS)))
    return True


def counts(data):
    out = {label: 0 for label in LABELS}
    for claim in data["claims"]:
        out[claim["label"]] += 1
    return out


def render(data):
    validate(data)
    lines = []
    lines.append("# Microcks v2 kick-off summary")
    lines.append("")
    lines.append("Source issue: %s" % data["issue_url"])
    lines.append("")
    lines.append("Labels: FACT = stated in prior research/issue record; DERIVED = careful restatement; UNKNOWN = not established - not guessed.")
    lines.append("")
    lines.append("## Stated goals")
    for item in data["goals"]:
        lines.append("- [%s] %s" % (item["label"], item["text"]))
    lines.append("")
    lines.append("## Open questions")
    for item in data["open_questions"]:
        lines.append("- [%s] %s" % (item["label"], item["text"]))
    lines.append("")
    lines.append("## Claims")
    for claim in data["claims"]:
        lines.append("- [%s] %s" % (claim["label"], claim["text"]))
    lines.append("")
    c = counts(data)
    lines.append("Counts: FACT=%d DERIVED=%d UNKNOWN=%d total=%d" % (c["FACT"], c["DERIVED"], c["UNKNOWN"], len(data["claims"])))
    lines.append("")
    lines.append("Note: v2 was described as an early, undecided study; no timeline, roadmap, or technical choice is claimed here unless labelled FACT above.")
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 kickoff.py INPUT.json [--out FILE]")
        print("INPUT.json: {issue_url, goals[], open_questions[], claims[]} - see sample_data.json")
        return 0 if len(argv) >= 2 else 2
    out = None
    i = 2
    while i < len(argv):
        if argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]
            i += 2
        else:
            print("unknown or incomplete argument: %s" % argv[i])
            return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        text = render(data)
    except (ValueError, OSError) as exc:
        print("error: %s" % exc)
        return 2
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
