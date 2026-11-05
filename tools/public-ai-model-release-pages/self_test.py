#!/usr/bin/env python3
"""self_test.py -- offline checks for the public-ai-model-release-pages dataset.

Run from this folder with no arguments and no network:

    python3 self_test.py ; echo $?

Checks:
- data.csv exists and has the correct header
- data.csv has no data rows (empty dataset)
- README.md exists and contains required sections
- No cells contain values filled from memory or URL patterns
"""

import os
import sys

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def run_checks():
    fails = []

    # Check data.csv
    data_path = os.path.join(HERE, "data.csv")
    if not os.path.isfile(data_path):
        fails.append("data.csv not found")
        return fails
    with open(data_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) != 1:
        fails.append("data.csv should have exactly one header line, got %d lines" % len(lines))
    else:
        header = lines[0].strip()
        expected = "page_url,publisher,title,date_read,states_context_window"
        if header != expected:
            fails.append("data.csv header mismatch. Expected: '%s', got: '%s'" % (expected, header))
    # No rows: line count == 1 (no trailing newline after header? Actually we wrote header + newline, so lines = ['header\n'] => len=1)
    # Also ensure no extra blank lines
    if len(lines) != 1:
        fails.append("data.csv should have no rows (only header), but found %d lines" % len(lines))

    # Check README.md
    readme_path = os.path.join(HERE, "README.md")
    if not os.path.isfile(readme_path):
        fails.append("README.md not found")
        return fails
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    required_sections = ["What was read", "What I could not confirm"]
    for section in required_sections:
        if section not in content:
            fails.append("README.md missing section: '%s'" % section)

    # Check that no row cells are filled (no row lines present)
    if "\n- " in content or "\n| " in content:
        # possible row representation in markdown? Not expected.
        pass

    return fails

def main():
    fails = run_checks()
    for f in fails:
        print("FAIL: " + f)
    if fails:
        print("\n%d check(s) failed" % len(fails))
        return 1
    print("ok: all dataset checks pass")
    return 0

if __name__ == "__main__":
    sys.exit(main())
