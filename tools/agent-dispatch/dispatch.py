#!/usr/bin/env python3
"""Tag-to-strength matcher with deterministic ties and explicit no-match.

Offline, stdlib only. Rules are evaluated in input order; the
winner is the highest strength, ties broken by earliest rule
position, then by normalized tag (lexicographic). If no rule
matches any tag, the result is an explicit no-match object.
No rule, tag, or strength is inferred. See README.md.
"""
import json
import sys
from pathlib import Path


def normalize_tag(value):
    if not isinstance(value, str):
        raise ValueError("tag must be a string: %r" % (value,))
    normalized = " ".join(value.strip().lower().split())
    if not normalized:
        raise ValueError("tag must not be empty")
    return normalized


def _validate_strength(value, index):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("rule %d: strength must be a number" % index)
    return value


def match(tags, rules):
    if not isinstance(tags, (list, tuple)):
        raise ValueError("tags must be a list")
    if not isinstance(rules, (list, tuple)):
        raise ValueError("rules must be a list")
    normalized_tags = []
    seen = set()
    for tag in tags:
        norm = normalize_tag(tag)
        if norm not in seen:
            seen.add(norm)
            normalized_tags.append(norm)
    candidates = []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError("rule %d must be an object" % index)
        if "tag" not in rule or "strength" not in rule:
            raise ValueError("rule %d requires tag and strength" % index)
        rule_tag = normalize_tag(rule["tag"])
        strength = _validate_strength(rule["strength"], index)
        if rule_tag in seen:
            candidates.append({
                "tag": rule_tag,
                "strength": strength,
                "label": rule.get("label"),
                "_index": index,
            })
    if not candidates:
        return {
            "matched": False,
            "strength": None,
            "tag": None,
            "label": None,
            "rule_index": None,
            "reason": "no-match",
            "normalized_tags": normalized_tags,
            "candidates": [],
        }
    # Deterministic: strength desc, then earliest rule, then tag.
    candidates.sort(key=lambda c: (-c["strength"], c["_index"], c["tag"]))
    winner = candidates[0]
    return {
        "matched": True,
        "strength": winner["strength"],
        "tag": winner["tag"],
        "label": winner["label"],
        "rule_index": winner["_index"],
        "reason": "matched",
        "normalized_tags": normalized_tags,
        "candidates": [
            {"tag": c["tag"], "strength": c["strength"],
             "label": c["label"], "rule_index": c["_index"]}
            for c in candidates
        ],
    }


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 dispatch.py INPUT.json [--out FILE]")
        print('INPUT.json: {"tags": ["..."], "rules": [{"tag": "...", "strength": 1, "label": "..."}]}')
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
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        result = match(data.get("tags", []), data.get("rules", []))
    except (ValueError, OSError) as exc:
        print("error: %s" % exc)
        return 2
    text = json.dumps(result, indent=2, sort_keys=True)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
