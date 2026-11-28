#!/usr/bin/env python3
"""Strip known tracking parameters from X/Twitter URLs.

Offline, stdlib only, no network. It never fetches a URL and never
runs code against anyone's systems: it only rewrites text you give it.

Removed: any parameter whose name starts with "utm_", plus the exact
names s, t, ref_src and ref_url (case-insensitive).
Kept: every other parameter, in its original order, plus scheme,
host, path and fragment.
"""
import sys
from pathlib import Path
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

TRACKING_EXACT = {"s", "t", "ref_src", "ref_url"}
TRACKING_PREFIXES = ("utm_",)
X_HOSTS = {
    "twitter.com", "www.twitter.com", "mobile.twitter.com",
    "x.com", "www.x.com", "mobile.x.com",
}

USAGE = ("usage: python3 stripper.py URLS.txt [--out FILE]\n"
         "URLS.txt: one URL per line; cleaned lines are written out.\n"
         "removed: utm_*, s, t, ref_src, ref_url (X/Twitter hosts only)")


def is_tracking_param(name):
    """True if a query-parameter name is a known tracking parameter."""
    low = (name or "").lower()
    if low in TRACKING_EXACT:
        return True
    return any(low.startswith(p) for p in TRACKING_PREFIXES)


def host_of(url):
    """Lowercase host, handling userinfo, port and scheme-less URLs."""
    parts = urlsplit(url)
    netloc = parts.netloc
    if not netloc and parts.path and not parts.path.startswith("/"):
        netloc = parts.path.split("/", 1)[0]
    return netloc.rsplit("@", 1)[-1].split(":")[0].lower()


def is_x_host(url):
    return host_of(url) in X_HOSTS


def strip_tracking(url, x_only=True):
    """Return (clean_url, removed_names).

    With x_only=True (default) a URL whose host is not an X/Twitter
    host is returned unchanged and nothing is reported as removed.
    A URL without a '?' is returned unchanged.
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    if "?" not in url:
        return url, []
    if x_only and not is_x_host(url):
        return url, []
    parts = urlsplit(url)
    kept, removed = [], []
    for name, value in parse_qsl(parts.query, keep_blank_values=True):
        if is_tracking_param(name):
            removed.append(name)
        else:
            kept.append((name, value))
    if not removed:
        return url, []
    query = urlencode(kept, quote_via=quote)
    clean = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, query, parts.fragment))
    return clean, removed


def strip_lines(text, x_only=True):
    """Clean one URL per line; blank lines pass through."""
    out = []
    for line in text.splitlines():
        if not line.strip():
            out.append(line)
            continue
        clean, _ = strip_tracking(line.strip(), x_only=x_only)
        out.append(clean)
    return out


def main(argv):
    if len(argv) < 2:
        print(USAGE)
        return 2
    path = argv[1]
    out = None
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            print(USAGE)
            return 2
        out = argv[i + 1]
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        print("error: %s" % exc)
        return 1
    result = "\n".join(strip_lines(text)) + "\n"
    if out:
        Path(out).write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
