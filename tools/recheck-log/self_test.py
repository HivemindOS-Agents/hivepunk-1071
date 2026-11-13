#!/usr/bin/env python3
"""self_test.py — offline tests for recheck_log.py.

Run from inside this folder with no arguments, no network:
    python3 self_test.py

It builds fixture CSVs in a temp directory, runs recheck_log.py on each,
checks stdout lines and exit codes. Exits 0 only when every check passes.
Stdlib only.
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable
RECHECK = os.path.join(HERE, "recheck_log.py")

_CHECKS = 0
_FAILS = 0


def check(condition, label):
    global _CHECKS, _FAILS
    _CHECKS += 1
    if not condition:
        _FAILS += 1
        print("FAIL: %s" % label)
    else:
        print("  ok: %s" % label)


def _csv_text(*rows):
    """Return bytes, header then rows, LF only."""
    lines = ["issue,url,state,checked_at"]
    for row in rows:
        # Escape any commas or quotes in fields (simple: wrap in quotes)
        fields = []
        for val in row:
            sv = str(val)
            if ',' in sv or '"' in sv or '\n' in sv:
                sv = '"' + sv.replace('"', '""') + '"'
            fields.append(sv)
        lines.append(",".join(fields))
    return ("\n".join(lines) + "\n").encode("utf-8")


def run_on(text_bytes, label):
    """Write CSV to a temp file, run recheck_log.py, return (stdout, stderr, code)."""
    tmpd = tempfile.mkdtemp(prefix="recheck-log-self-test-")
    csv_path = os.path.join(tmpd, "test.csv")
    with open(csv_path, "wb") as f:
        f.write(text_bytes)
    proc = subprocess.run(
        [PYTHON, RECHECK, csv_path],
        capture_output=True,
        timeout=10,
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace")
    return out, err, proc.returncode


def main():
    # 1. All rows PASS
    data = _csv_text(
        ("issue-1", "https://example.com/1", "ok", "2026-11-12"),
        ("issue-2", "https://example.com/2", "not-opened", "2026-11-12T09:28:00Z"),
        ("issue-3", "https://example.com/3", "NOT_RUN", "2026-11-12T14:30:00+00:00"),
    )
    out, err, code = run_on(data, "all-pass")
    check(
        "PASS" in out and "FAIL" not in out,
        "all-ok rows: no FAIL in output",
    )
    check(out.strip().endswith("rows=3 failed=0"),
          "all-ok rows: summary is rows=3 failed=0")
    check(code == 0, "all-ok rows: exit 0")

    # 2. Blank state -> FAIL
    data = _csv_text(("i1", "https://x.com/i1", "", "2026-11-12"))
    out, err, code = run_on(data, "blank-state")
    check("FAIL row 1" in out and "state is blank" in out,
          "blank state: FAIL with reason")
    check(code == 1, "blank state: exit 1")

    # 3. state outside allowed set -> FAIL
    data = _csv_text(("i2", "https://x.com/i2", "invalid", "2026-11-12"))
    out, err, code = run_on(data, "invalid-state")
    check("not in {ok, not-opened, NOT_RUN}" in out,
          "invalid state: FAIL with reason")
    check(code == 1, "invalid state: exit 1")

    # 4. state with trailing space -> FAIL
    data = _csv_text(("i3", "https://x.com/i3", "ok ", "2026-11-12"))
    out, err, code = run_on(data, "trailing-space-state")
    check("'ok '" in out and "not in {ok, not-opened, NOT_RUN}" in out,
          "trailing space state: FAIL")
    check(code == 1, "trailing space state: exit 1")

    # 5. Blank url -> FAIL
    data = _csv_text(("i4", "", "ok", "2026-11-12"))
    out, err, code = run_on(data, "blank-url")
    check("url is blank" in out, "blank url: FAIL with reason")
    check(code == 1, "blank url: exit 1")

    # 6. Non-ISO checked_at -> FAIL
    data = _csv_text(("i5", "https://x.com/i5", "ok", "2026/11/12"))
    out, err, code = run_on(data, "non-iso-date")
    check("not ISO 8601" in out, "non-ISO checked_at: FAIL with reason")
    check(code == 1, "non-ISO checked_at: exit 1")

    # 7. Non-real date -> FAIL
    data = _csv_text(("i6", "https://x.com/i6", "ok", "2026-02-30"))
    out, err, code = run_on(data, "unreal-date")
    check("not a real calendar date" in out,
          "impossible date: FAIL with reason")
    check(code == 1, "impossible date: exit 1")

    # 8. Impossible time -> FAIL
    data = _csv_text(("i7", "https://x.com/i7", "ok", "2026-11-12T25:61:00Z"))
    out, err, code = run_on(data, "impossible-time")
    check("impossible" in out,
          "impossible time: FAIL with reason")
    check(code == 1, "impossible time: exit 1")

    # 9. Space-separated datetime -> FAIL
    data = _csv_text(("i8", "https://x.com/i8", "ok", "2026-11-12 09:28"))
    out, err, code = run_on(data, "space-separated")
    check("not ISO 8601" in out,
          "space-separated datetime: FAIL (not ISO)")
    check(code == 1, "space-separated datetime: exit 1")

    # 10. Empty CSV -> exit 2
    data = b"issue,url,state,checked_at\n"
    out, err, code = run_on(data, "empty-csv")
    check(code == 0 and "rows=0 failed=0" in out,
          "empty CSV: exit 0, summary rows=0 failed=0")

    # 11. Missing header -> exit 2
    data = _csv_text()  # header only
    # Force header wrong by writing different column
    tmpd = tempfile.mkdtemp(prefix="recheck-log-self-test-")
    csv_path = os.path.join(tmpd, "bad_header.csv")
    with open(csv_path, "wb") as f:
        f.write(b"a,b,c,d\n1,2,3,4\n")
    proc = subprocess.run(
        [PYTHON, RECHECK, csv_path],
        capture_output=True,
        timeout=10,
    )
    err = proc.stderr.decode("utf-8", errors="replace")
    check("missing column" in err and "issue" in err,
          "wrong header: exit 2, missing column error")
    check(proc.returncode == 2, "wrong header: exit 2")

    # 12. Mixed PASS/FAIL -> summary rows= N failed= M, exit 1
    data = _csv_text(
        ("i1", "https://x.com/i1", "ok", "2026-11-12"),
        ("i2", "https://x.com/i2", "invalid", "2026-11-12"),
        ("i3", "https://x.com/i3", "ok", "2026-11-12"),
    )
    out, err, code = run_on(data, "mixed")
    check("rows=3 failed=1" in out,
          "mixed: summary rows=3 failed=1")
    check("PASS row 1" in out and "FAIL row 2" in out and "PASS row 3" in out,
          "mixed: two PASS and one FAIL")
    check(code == 1, "mixed: exit 1")

    # 13. Empty checked_at -> FAIL
    data = _csv_text(("i9", "https://x.com/i9", "ok", ""))
    out, err, code = run_on(data, "empty-checked-at")
    check("checked_at is empty" in out,
          "empty checked_at: FAIL")
    check(code == 1, "empty checked_at: exit 1")

    # Summary
    print("\nResults: %d/%d checks passed" % (_CHECKS - _FAILS, _CHECKS))
    return 1 if _FAILS > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
