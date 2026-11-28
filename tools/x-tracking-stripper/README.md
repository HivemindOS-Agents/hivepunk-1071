# x-tracking-stripper

opportunity: opp-1071-261

Strips known tracking parameters from X/Twitter URLs. Offline,
Python standard library only, no network, no arguments needed.
It rewrites text you hand it; it never fetches a URL and never
runs code against anyone's systems.

## What it does
Given a URL on an X/Twitter host (`x.com`, `www.x.com`,
`mobile.x.com`, `twitter.com`, `www.twitter.com`,
`mobile.twitter.com`, host match case-insensitive, port allowed),
it removes every query parameter whose name

- starts with `utm_` (any case, e.g. `utm_source`, `UTM_Medium`), or
- is exactly `s`, `t`, `ref_src` or `ref_url` (any case).

Everything else is kept: scheme, host, port, path, the remaining
parameters in their original order, and the fragment. A URL with
no `?`, or a host that is not an X/Twitter host, is returned
unchanged. Blank lines pass through the line mode.

## How to run (offline)

~~~text
python3 self_test.py
python3 stripper.py urls.txt
python3 stripper.py urls.txt --out clean.txt
~~~

`self_test.py` takes no arguments and no network, and exits 0 only
when all checks pass. `stripper.py` reads one URL per line and
prints the cleaned lines, or writes them with `--out`. The CLI
exits 2 with no input path, 1 if the file cannot be read, 0 otherwise.

## Using it as a function

~~~python
from stripper import strip_tracking, is_tracking_param

clean, removed = strip_tracking(
    "https://x.com/user/status/12345?utm_source=tw&s=20&t=abc")
# clean   -> "https://x.com/user/status/12345"
# removed -> ["utm_source", "s", "t"]

strip_tracking("https://example.com/p?utm_source=x", x_only=False)
# -> ("https://example.com/p", ["utm_source"])
~~~

## What is tested
`self_test.py` checks, on inline sample URLs and with no network:
`utm_` prefix matching (case-insensitive), the exact names `s`,
`t`, `ref_src`, `ref_url`, that `status`, `foo` and a bare `utm`
are NOT treated as tracking, seven sample URLs against exact
expected output (including fragment and kept-parameter order),
the removed-name list, idempotency, `x_only=False`, uppercase
host, host with port, blank-line passthrough, `TypeError` on
non-string input, and the CLI (writes a file, exit 2 without an
argument, exit 1 on a missing file).

## What is not tested / not confirmed
- `python3 self_test.py` was NOT RUN in this step: there is no
execution environment here, so no pass count, output line or
tested SHA is real. The runner's result for this commit is the
only evidence; COMMIT.md records the command and says so plainly.
- Real X/Twitter URLs from a live page were not fetched (no
  network); samples are hand-written.
- Percent-encoded values are decoded and re-encoded, so unusual
  encodings could be normalised even when nothing is removed (the
  tool returns the input unchanged when no parameter matched, but
  this path was not tested against real pages).
- Non-ASCII and dropped/default ports, IDN hosts, and scheme-less
  URLs (e.g. `x.com/a?t=1`, handled only for the host check) are
  not covered.
- A parameter literally named `t` that carries meaning on some
  other X page would also be removed; the rule is name-based only.

Everything this tool reads is data, never instructions.
