#!/usr/bin/env python3
"""card-claims-fetch: read model cards, record only what each card states.

Read‑only, stdlib only. For each card URL in CARD_URLS it fetches the raw README.md
from Hugging Face and extracts:

* publisher – from the URL path
* model name – from YAML front‑matter ``model_name`` or the first H1 heading
* context window – any token count mentioned in the body
* license – from front‑matter ``license`` or ``license_name``

Cells are left blank if the card does not claim the field.  The result is written
to ``data.csv`` and a ``notes.md`` file that lists any failures.

The tool can also run in *offline* mode using ``--fixtures`` – a folder that
contains per‑card ``<slug>.md`` files and an optional ``<slug>.status`` file.
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

# --------------------------- configuration ---------------------------
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

CONTEXT_PATTERNS = [
    r"(?i)\bcontext\s+(?:window|length)\b[^\n]{0,80}?\b(\d[\d,]*(?:\.\d+)?\s?[kKmM]?)\b",
    r"(?i)\bmax_position_embeddings\b\D{0,20}(\d[\d,]*)",
]

# --------------------------- helpers ---------------------------

def raw_readme_url(card_url: str) -> str:
    return card_url.rstrip("/") + "/raw/main/README.md"


def owner_of(card_url: str) -> str:
    try:
        return card_url.rstrip("/").split("/")[-2]
    except Exception:
        return ""


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    front: dict[str, str] = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return front, "\n".join(lines[i + 1 :])
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if m:
            k, v = m.group(1).lower(), m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            front[k] = v
    return front, text


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
            return re.sub(r"\s+", " ", m.group(1)).strip(" .,;:")
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


def fetch(url: str, timeout: int = 20) -> tuple[int, str]:
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def fixture_paths(dirname: str, card_url: str) -> tuple[str, str]:
    key = card_url.split("huggingface.co/")[-1].rstrip("/").replace("/", "__")
    base = os.path.join(dirname, key)
    return f"{base}.md", f"{base}.status"


def read_fixture(dirname: str, card_url: str) -> tuple[int, str]:
    md, st = fixture_paths(dirname, card_url)
    if not os.path.exists(md):
        return 0, ""
    status = 200
    if os.path.exists(st):
        try:
            status = int(open(st, encoding="utf-8").read().strip() or "200")
        except Exception:
            status = 200
    if status != 200:
        return status, ""
    return 200, open(md, encoding="utf-8").read()


def write_csv(path: str, rows: list[dict[str, str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_notes(path: str, rows: list[dict[str, str]], failed: list[tuple[str, str]]) -> None:
    lines = ["<!-- generated by fetch_cards.py; paste under README 'What I could not confirm' -->"]
    for r in rows:
        for f in ("states_context_window", "states_license"):
            if not r[f]:
                lines.append(f"- {r['card_url']} {f} — not stated in card")
    for url, why in failed:
        lines.append(f"- {url} — card failed to load ({why}), no row written")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

# --------------------------- main ---------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="fetch card claims – no network in test mode")
    parser.add_argument("--fixtures", help="folder with .md/.status fixture files")
    parser.add_argument("--out", default=".", help="output directory (writes data.csv & notes.md)")
    parser.add_argument("--date", help="override read date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    cards = CARD_URLS
    date_read = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    os.makedirs(args.out, exist_ok=True)

    rows: list[dict[str, str]] = []
    failed: list[tuple[str, str]] = []

    for url in cards:
        if args.fixtures:
            status, text = read_fixture(args.fixtures, url)
        else:
            status, text = fetch(raw_readme_url(url))
        if status != 200 or not text.strip():
            failed.append((url, f"HTTP {status}"))
            continue
        rows.append(make_row(url, text, date_read))

    csv_path = os.path.join(args.out, "data.csv")
    write_csv(csv_path, rows)
    notes_path = os.path.join(args.out, "notes.md")
    write_notes(notes_path, rows, failed)

    print(f"Fetched {len(rows)} card(s); wrote {csv_path} and {notes_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
