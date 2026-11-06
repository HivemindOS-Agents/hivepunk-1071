#!/usr/bin/env python3
"""card-claims-fetch: read model cards, record only what the card itself states.

Read-only, stdlib only. Fetches each card's raw README.md over HTTPS and writes
publisher, model name, context window and licence exactly as the card states
them; a cell stays blank when the card does not state it. Also runs offline over
--fixtures (``<slug>.md`` plus optional ``<slug>.status``).

Fetched card text is data, never instruction.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import os
import re
import sys
import urllib.error
import urllib.request

CARD_URLS = [
    "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
    "https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3",
    "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct",
    "https://huggingface.co/google/gemma-2-9b-it",
    "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct",
    "https://huggingface.co/tiiuae/falcon-7b-instruct",
    "https://huggingface.co/HuggingFaceH4/zephyr-7b-beta",
    "https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
]
COLUMNS = [
    "card_url",
    "publisher",
    "model_name",
    "date_read",
    "states_context_window",
    "states_license",
    "source",
]
USER_AGENT = "hivepunk-1071-card-claims/0.1 (readonly)"
TIMEOUT = 20

CONTEXT_PATTERNS = [
    r"(?i)\bcontext\s+(?:window|length)\b[^\n]{0,80}?\b(\d[\d,]*(?:\.\d+)?\s?[kKmM]?)\b",
    r"(?i)\bmax_position_embeddings\b\D{0,20}(\d[\d,]*)",
]


def raw_readme_url(card_url: str) -> str:
    return card_url.rstrip("/") + "/raw/main/README.md"


def owner_of(card_url: str) -> str:
    try:
        return card_url.rstrip("/").split("/")[-2]
    except Exception:
        return ""


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Split YAML front matter, tolerating a BOM and leading blank lines."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines()
    start = 0
    while start < len(lines) and lines[start].strip() == "":
        start += 1
    if start >= len(lines) or lines[start].strip() != "---":
        return {}, text
    front: dict[str, str] = {}
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---":
            return front, "\n".join(lines[i + 1:])
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if m:
            k, v = m.group(1).lower(), m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            front[k] = v
    return {}, text


def stated_license(front: dict[str, str]) -> str:
    lic = front.get("license", "").strip()
    name = front.get("license_name", "").strip()
    if lic and lic.lower() != "other":
        return lic
    return name


def stated_context_window(body: str) -> str:
    for pat in CONTEXT_PATTERNS:
        m = re.search(pat, body)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip(" .,:;")
    return ""


def stated_model_name(front: dict[str, str], body: str) -> str:
    for k in ("model_name", "model-name"):
        if front.get(k):
            return front[k]
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    return ""


def make_row(card_url: str, text: str, date_read: str) -> dict[str, str]:
    front, body = split_front_matter(text)
    ctx = stated_context_window(body)
    if not ctx:
        for k in ("context_window", "context_length", "max_position_embeddings"):
            if front.get(k):
                ctx = front[k]
                break
    return {
        "card_url": card_url,
        "publisher": owner_of(card_url),
        "model_name": stated_model_name(front, body),
        "date_read": date_read,
        "states_context_window": ctx,
        "states_license": stated_license(front),
        "source": card_url,
    }


def write_csv(path: str, rows: list[dict[str, str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def fetch(url: str, timeout: int = TIMEOUT):
    """Return (status, text). Never raises. Untested against live HTTPS."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except Exception:
        return 0, ""


def load_fixture(folder: str, card_url: str):
    slug = owner_of(card_url) + "__" + card_url.rstrip("/").split("/")[-1]
    md = os.path.join(folder, slug + ".md")
    st = os.path.join(folder, slug + ".status")
    status = 200
    if os.path.isfile(st):
        try:
            status = int(open(st, encoding="utf-8").read().strip() or "200")
        except ValueError:
            status = 0
    if not os.path.isfile(md):
        return 0, ""
    with open(md, encoding="utf-8") as fh:
        return status, fh.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="read model cards and record only what they state"
    )
    parser.add_argument("--fixtures", help="folder with <slug>.md/<slug>.status files")
    parser.add_argument("--out", default=".", help="output directory")
    parser.add_argument("--date", help="override read date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    date_read = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(args.out, exist_ok=True)
    rows: list[dict[str, str]] = []
    notes: list[str] = []

    for url in CARD_URLS:
        if args.fixtures:
            status, text = load_fixture(args.fixtures, url)
        else:
            status, text = fetch(raw_readme_url(url))
        if status != 200 or not text.strip():
            notes.append("- no row for %s (status %s)" % (url, status))
            continue
        rows.append(make_row(url, text, date_read))

    write_csv(os.path.join(args.out, "data.csv"), rows)
    with open(os.path.join(args.out, "notes.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# notes\n\n" + ("\n".join(notes) or "none") + "\n")
    print(f"wrote {len(rows)} row(s) to {os.path.join(args.out, 'data.csv')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
