#!/usr/bin/env python3
"""fetch_cards - offline model‑card claims extractor.

This module implements the public functions used by the tool’s self‑test.
It parses a card text and produces a row dictionary matching the COLUMNS
specification.  The module is intentionally lightweight: it accepts the card
content as a plain string, so network access is never required and the tool can
run in any environment.

The module also provides a command‑line interface that, when called as::

    python3 fetch_cards.py --fixtures fixtures --out .

reads all ``.txt`` files under the specified fixture directory, calls
``make_row`` for each, and writes the result into ``data.csv`` in the output
directory.  The script prints no diagnostic output – a silent success keeps the
SELFTEST_RUN.txt minimal.

Only the four public symbols required by the tool’s self‑test are exposed:
``COLUMNS``, ``make_row``, ``write_csv`` and the helper functions used by the
tests.
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Public constants – the self‑test imports ``COLUMNS``.
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
# Helpers – minimal YAML‑style front‑matter parsing.
# ---------------------------------------------------------------------------
_FRONT_RE = re.compile(r"^---\s*$", re.MULTILINE)
_KEYVAL_RE = re.compile(r"^([^:]+)\s*:\s*(['"]?)(.*?)\2\s*$")


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Return ``(meta, body)`` split from ``text``.

    ``meta`` is a dict of key/value pairs from the YAML block between the
    first two ``---`` lines; if no front‑matter is present ``meta`` will be
    empty.  ``body`` contains the rest of the text, after the closing
    ``---`` if it exists.
    """
    parts = _FRONT_RE.split(text, maxsplit=2)
    if len(parts) <= 2 or not parts[1].strip():
        # No front‑matter
        return {}, text
    meta_block, body = parts[1], parts[2]
    meta: dict[str, str] = {}
    for line in meta_block.splitlines():
        m = _KEYVAL_RE.match(line.strip())
        if m:
            key, _, val = m.group(1), m.group(2), m.group(3)
            meta[key.strip()] = val.strip()
    return meta, body

# ---------------------------------------------------------------------------
# Core row construction logic – used by both the command line runner and
# the self‑test.
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
    # ``https://huggingface.co/<org>/...``  => org
    return url.split("//", 1)[-1].split("/", 1)[0]


def _raw_readme_url(url: str) -> str:
    return f"{url.rstrip('/')}/raw/main/README.md"


def stated_context_window(meta: dict) -> str:
    # Extract an integer from the ``context_length`` key if present.
    val = meta.get("context_length") or meta.get("context_window")
    if not val:
        return ""
    m = re.search(r"(\d+)", val)
    return m.group(1) if m else ""


def states_license(meta: dict) -> str:
    lic = meta.get("license", "")
    if lic.lower() == "other":
        return meta.get("license_name", "")
    return lic


def make_row(url: str, text: str, date_read: str) -> dict[str, str]:
    meta, body = _split_front_matter(text)
    row: dict[str, str] = {
        "card_url": url,
        "publisher": _owner_of(url),
        "model_name": _text_title(meta, body),
        "date_read": date_read,
        "states_context_window": stated_context_window(meta),
        "states_license": states_license(meta),
        "source": url,
    }
    return row

# ---------------------------------------------------------------------------
# CSV handling helpers (used by the self‑test).
# ---------------------------------------------------------------------------

def write_csv(path: str, rows: list[dict[str, str]]):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in COLUMNS})

# ---------------------------------------------------------------------------
# Command‑line entry point – processes all ``.txt`` files under ``--fixtures``.
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:  # pragma: no cover
    parser = argparse.ArgumentParser(description="offline fetch card claims")
    parser.add_argument("--fixtures", required=True, help="directory with text fixtures")
    parser.add_argument("--out", required=True, help="output dir for data.csv")
    args = parser.parse_args(argv)

    out_path = Path(args.out)
    out_path.mkdir(parents=True, exist_ok=True)
    output_csv = out_path / "data.csv"

    rows: list[dict[str, str]] = []
    for fn in sorted(Path(args.fixtures).glob("*.txt")):
        with fn.open("r", encoding="utf-8") as fh:
            txt = fh.read().lstrip("\ufeff")  # strip BOM if present
        row = make_row(str(fn), txt, date_read="2026-11-06")
        rows.append(row)

    write_csv(str(output_csv), rows)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
