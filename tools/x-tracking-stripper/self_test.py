#!/usr/bin/env python3
"""Offline self-test for stripper.py: no arguments, no network.

Runs the tool's own code on inline sample URLs and compares each
result with what should come out. Exits 0 only when every check
passes. Prints one ok:/FAIL: line per check and a final count.
"""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import stripper as s

CHECKS = 0
PASSED = 0

# Inline sample data: (input URL, expected cleaned URL)
SAMPLES = [
    ("https://x.com/user/status/12345?utm_source=tw&utm_medium=social&s=20&t=abc",
     "https://x.com/user/status/12345"),
    ("https://twitter.com/i/web/status/1?ref_src=twsrc%5Etfw&ref_url=https%3A%2F%2Fexample.com",
     "https://twitter.com/i/web/status/1"),
    ("https://x.com/a?keep=1&utm_campaign=x&t=1#frag",
     "https://x.com/a?keep=1#frag"),
    ("https://mobile.twitter.com/u/status/2?utm_content=z&lang=en",
     "https://mobile.twitter.com/u/status/2?lang=en"),
    ("https://example.com/page?utm_source=x&s=1",
     "https://example.com/page?utm_source=x&s=1"),
    ("https://x.com/u/status/3?status=1&foo=t&utm_source=z",
     "https://x.com/u/status/3?status=1&foo=t"),
    ("https://x.com/nothing",
     "https://x.com/nothing"),
]


def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1
        print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)


def main():
    check(s.is_tracking_param("utm_source"), "utm_source is tracking")
    check(s.is_tracking_param("UTM_Source"), "utm_ match is case-insensitive")
    check(s.is_tracking_param("s") and s.is_tracking_param("t"),
          "exact s and t are tracking")
    check(s.is_tracking_param("ref_src") and s.is_tracking_param("ref_url"),
          "ref_src and ref_url are tracking")
    check(not s.is_tracking_param("status"), "status is not tracking")
    check(not s.is_tracking_param("utm") and not s.is_tracking_param("foo"),
          "utm alone and foo are not tracking")

    for url, expected in SAMPLES:
        got, removed = s.strip_tracking(url)
        check(got == expected, "sample -> %s" % expected)
        if got == url:
            check(removed == [], "no change reported nothing removed")

    got, removed = s.strip_tracking(SAMPLES[0][0])
    check(sorted(removed) == ["s", "t", "utm_medium", "utm_source"],
          "removed names are listed")
    check(s.strip_tracking(got)[0] == got and s.strip_tracking(got)[1] == [],
          "stripping is idempotent")
    check(s.strip_tracking("https://x.com/a?utm_source=1", x_only=False)[0]
          == "https://x.com/a", "x_only=False still strips on X hosts")
    check(s.strip_tracking("https://X.COM/a?t=1")[0] == "https://X.COM/a",
          "host match is case-insensitive")
    check(s.strip_tracking("https://x.com:443/a?t=1")[0] == "https://x.com:443/a",
          "host with port is handled")
    check(s.strip_lines("https://x.com/a?t=1\n\n") == ["https://x.com/a", ""],
          "strip_lines keeps blank lines")

    try:
        s.strip_tracking(None)
        check(False, "non-string input raises TypeError")
    except TypeError:
        check(True, "non-string input raises TypeError")

    with tempfile.TemporaryDirectory() as td:
        inp = Path(td) / "urls.txt"
        out = Path(td) / "clean.txt"
        inp.write_text("https://x.com/u/status/9?utm_source=a&t=1\n"
                       "https://example.com/p?s=1\n", encoding="utf-8")
        check(s.main(["stripper.py", str(inp), "--out", str(out)]) == 0,
              "CLI exits 0 and writes a file")
        check(out.read_text(encoding="utf-8")
              == "https://x.com/u/status/9\nhttps://example.com/p?s=1\n",
              "CLI output matches strip_lines")
        check(s.main(["stripper.py"]) == 2, "CLI requires an input path")
        check(s.main(["stripper.py", str(Path(td) / "missing.txt")]) == 1,
              "CLI exits 1 on a missing file")

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
