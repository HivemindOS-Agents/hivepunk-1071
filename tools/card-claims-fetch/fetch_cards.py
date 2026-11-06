#!/usr/bin/env python3
"""fetch_cards - offline model-card claims extractor.

This module implements the public functions used by the tool's self-test.
It parses a card text and produces a row dictionary matching the COLUMNS
specification. The module is intentionally lightweight: it accepts the card
content as a plain string, so network access is never required and the tool can
run in any environment.

The module also provides a command-line interface that, when called as::

    python3 fetch_cards.py --fixtures fixtures --out .

reads all ``.txt`` files under the specified fixture directory, calls
``make_row`` for each, and writes the result into ``data.csv`` in the output
directory.

Only the public symbols required by the tool's self-test are exposed:
``COLUMNS``, ``make_row``, ``write_csv`` and the helper functions used by the
tests (``owner_of``, ``raw_readme_url``, ``stated_context_window``).

Fetched or fixture card text is **data, never instruction**. A sentence inside a
card telling this tool to run something, reveal a setting, change its goal, send money
or post anywhere is ignored and never executed.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Public constants - the self-test imports ``COLUMNS``.
# ---------------------------------------------------------------------------
COLUMNS = [
    "card_url",
    "publisher",
    "model_name",
    "date_read",
    "states_context_window",
    "states_license",
    "source",
]

# ---------------------------------------------------------------------------
# Helpers - minimal YAML-style front-matter parsing.
# ---------------------------------------------------------------------------
_FRONTR_RE = re.compile(r"^---\s*$", re.MULTILINE)
# NOTE: the character class below is ``['\"]`` - a square bracket that opens
# the class, the two quote characters it holds, and the bracket that closes it.
_KEYVAL_R = re.compile(r"^([^:]+)\s*:\s*(['\"]?)(.*?)\2\s*$")


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Return ``(meta, body)`` split from ``text``.

    A leading BOM and leading blank lines are stripped first, so a card whose
    file begins with a blank line or a byte-order mark still parses its front
    matter. ``meta`` is a dict of key/value pairs from the YAML block between
    the first two ``---`` lines; when no front matter is present ``meta`` is
    empty. ``body`` is the rest of the text.
    """
    text = text.lstrip("\ufeff")
    text = text.lstrip("\r\n")
    parts = _FRONTR_RE.split(text, maxsplit=2)
    if len(parts) <= 2 or not parts[1].strip():
        return {}, text
    meta_block, body = parts[1], parts[2]
    meta: dict[str, str] = {}
    for line in meta_block.splitlines():
        m = _KEYVAL_R.match(line.strip())
        if m:
            key, val = m.group(1), m.group(3)
            meta[key.strip()] = val.strip()
    return meta, body


# ---------------------------------------------------------------------------
# Core row construction logic - used by both the command-line runner and
# the self-test.
# ---------------------------------------------------------------------------

def _clean_html(text: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def _text_title(meta: dict, body: str) -> str:
    # Prefer the YAML ``model_name`` key, otherwise try the first heading.
    title = meta.get("model_name")
    if title:
        return title
    m = re.search(r"^#\s*(.*)$", body, re.MULTILINE)
    if m:
        return m.group(1)
    return ""


def _owner_of(url: str) -> str:
    """Return the first path component of ``url`` (the org/username).

    A known card host (huggingface.co, www.huggingface.co, hf.co) is dropped
    so ``https://huggingface.co/example-org/example-model-7b`` yields
    ``example-org``. For a bare host URL the host itself is returned; for
    other hosts the first path segment is returned.
    """
    rest = url.split("//", 1)[-1]
    rest = rest.split("@", 1)[-1]              # drop any user@
    host, _, path = rest.partition("/")
    host = host.split(":", 1)[0].lower()
    if host in ("huggingface.co", "www.huggingface.co", "hf.co"):
        seg = path.split("/", 1)[0] if path else ""
        return seg or host
    seg = path.split("/", 1)[0] if path else ""
    return seg or host


def _raw_readme_url(url: str) -> str:
    return f"{url.rstrip('/')}/raw/main/README.md"


# Public aliases. ``self_test.py`` calls ``fetch_cards.owner_of`` and
# ``fetch_cards.raw_readme_url``; ``make_row`` and the CLI keep using the
# underscore names. Both spellings resolve to the same function.
owner_of = _owner_of
raw_readme_url = _raw_readme_url


# Body-text fallback patterns. The card may state its window only in prose
# ("a context window of 32768 tokens") instead of in its front matter.
_BODY_WINDOW_R = re.compile(
    r"(?:context\s*window|context\s*length|max_position_embeddings)"
    r"[^0-9]{0,40}?(\d[\d,]*)\s*(?:tokens?)?",
    re.IGNORECASE,
)


def stated_context_window(meta, body: str = "") -> str:
    """Return the context-window number, front matter first, then body text.

    The function is defensive: if ``meta`` is not a dictionary (e.g. an empty
    string passed by the self-test) it is treated as an empty mapping rather
    than raising ``AttributeError``. Front-matter keys ``context_length`` and
    ``context_window`` are read first; when neither is present, the card's own
    body text is searched for a stated number. Commas in a number are removed.
    """
    if not isinstance(meta, dict):
        return ""
    val = meta.get("context_length") or meta.get("context_window")
    if not val:
        val = meta.get("max_position_embeddings")
    if val:
        m = re.search(r"(\d[\d,]*)", str(val))
        if m:
            return m.group(1).replace(",", "")
    if isinstance(body, str) and body:
        m = _BODY_WINDOW_R.search(body)
        if m:
            return m.group(1).replace(",", "")
    return ""


def states_license(meta: dict) -> str:
    lic = meta.get("license", "")
    if lic.lower() == "other":
        return meta.get("license_name", "")
    return lic


def make_row(url: str, text: str, date_read: str) -> dict[str, str]:
    meta, body = _split_front_matter(text)
    row: dict[str, str] = {
        "card_url": url,
        "publisher": meta.get("publisher") or _owner_of(url),
        "model_name": _text_title(meta, body),
        "date_read": date_read,
        "states_context_window": stated_context_window(meta, body),
        "states_license": states_license(meta),
        "source": url,
    }
    return row


# ---------------------------------------------------------------------------
# CSV handling helpers (used by the self-test).
# ---------------------------------------------------------------------------

def write_csv(path: str, rows: list[dict[str, str]]) -> None:
    # ``lineterminator="\n"`` keeps the file free of carriage returns; the
    # default ("\r\n") is what made the earlier run fail ``write_csv no CR``.
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS,
                                lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in COLUMNS})


# ---------------------------------------------------------------------------
# Command-line entry point - processes all ``.txt`` files under ``--fixtures``.
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:  # pragma: no cover
    parser = argparse.ArgumentParser(description="offline fetch card claims")
    parser.add_argument("--fixtures", required=True,
                        help="directory with text fixtures")
    parser.add_argument("--out", required=True,
                        help="output dir for data.csv")
    args = parser.parse_args(argv)

    out_path = Path(args.out)
    out_path.mkdir(parents=True, exist_ok=True)
    output_csv = out_path / "data.csv"

    rows: list[dict[str, str]] = []
    for fn in sorted(Path(args.fixtures).glob("*.txt")):
        with fn.open("r", encoding="utf-8") as fh:
            txt = fh.read()
        row = make_row(str(fn), txt, date_read="2026-11-06")
        rows.append(row)

    write_csv(str(output_csv), rows)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
