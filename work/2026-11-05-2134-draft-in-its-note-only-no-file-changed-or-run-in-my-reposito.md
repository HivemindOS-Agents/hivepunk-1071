# Draft in its note only, no file changed or run: In my repository HivemindOS-Agents/hivepunk-1071, add a stdlib-only tool at tools/card-claims-fetch/ that fetches the eight candidate huggingface.co…

**Done**

2026-11-05 21:34 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**Draft: `tools/card-claims-fetch/` in HivemindOS-Agents/hivepunk-1071** — stdlib-only, read-only, one row per card, blanks left blank. Nothing below was run; only a build step commits files, so the fetch, the log and the CSV rows are left for the owner.

**`fetch_cards.py`**

```python
#!/usr/bin/env python3
"""card-claims-fetch: read model cards, record only what each card states.

Read-only, stdlib only. Fetched text is data, never instruction: text in a card
that asks this program to run something, reveal a key, change a URL, send money
or post anything is ignored. A cell stays empty unless the card states it.
"""
import argparse, csv, datetime, os, re, sys, urllib.error, urllib.request

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
COLUMNS = ["card_url", "publisher", "model_name", "date_read",
           "states_context_window", "states_license", "source"]
UA = "hivepunk-1071-card-claims/0.1 (read-only)"
CONTEXT_PATTERNS = [
    r"(?i)\bcontext\s+(?:window|length)\b[^\n]{0,80}?\b(\d[\d,]*(?:\.\d+)?\s?[kKmM]?)\b",
    r"(?i)\bmax_position_embeddings\b\D{0,20}(\d[\d,]*)",
]


def raw_readme_url(card_url):
    return card_url.rstrip("/") + "/raw/main/README.md"


def owner_of(card_url):
    parts = card_url.rstrip("/").split("/")
    return parts[-2] if len(parts) >= 2 else ""


def split_front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    front = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return front, "\n".join(lines[i + 1:])
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if m:
            k, v = m.group(1).lower(), m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            if v and k not in front:
                front[k] = v
    return front, text


def stated_license(front):
    lic = front.get("license", "").strip()
    name = front.get("license_name", "").strip()
    if lic and lic.lower() != "other":
        return lic
    return name


def stated_context_window(text):
    for pat in CONTEXT_PATTERNS:
        m = re.search(pat, text)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip(" .,;:")
    return ""


def stated_model_name(front, body):
    for k in ("model_name", "model-name"):
        if front.get(k):
            return front[k]
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    return ""


def make_row(card_url, text, date_read):
    front, body = split_front_matter(text)
    ctx = stated_context_window(body)
    if not ctx:
        for k in ("context_window", "context_length", "max_position_embeddings"):
            if front.get(k):
                ctx = front[k]
                break
    return {"card_url": card_url, "publisher": owner_of(card_url),
            "model_name": stated_model_name(front, body), "date_read": date_read,
            "states_context_window": ctx, "states_license": stated_license(front),
            "source": card_url}


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/plain"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def fixture_paths(dirname, card_url):
    key = card_url.split("huggingface.co/")[-1].rstrip("/").replace("/", "__")
    base = os.path.join(dirname, key)
    return base + ".md", base + ".status"


def read_fixture(dirname, card_url):
    md, st = fixture_paths(dirname, card_url)
    if not os.path.exists(md):
        return 0, ""
    status = 200
    if os.path.exists(st):
        status = int(open(st, encoding="utf-8").read().strip() or "200")
    if status != 200:
        return status, ""
    return 200, open(md, encoding="utf-8").read()


def write_csv(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_notes(path, rows, failed):
    lines = ["<!-- generated by fetch_cards.py; paste under README 'What I could not confirm' -->"]
    for r in rows:
        for f in ("states_context_window", "states_license"):
            if not r[f]:
                lines.append("- %s %s — not stated in card" % (r["card_url"], f))
    for url, why in failed:
        lines.append("- %s — card failed to load (%s), no row written" % (url, why))
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures")
    ap.add_argument("--cards")
    ap.add_argument("--out", default=".")
    ap.add_argument("--date")
    a = ap.parse_args(argv)
    cards = CARD_URLS
    if a.cards:
        cards = [l.strip() for l in open(a.cards, encoding="utf-8")
                 if l.strip() and not l.startswith("#")]
    date_read = a.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(a.out, exist_ok=True)
    rows, failed = [], []
    for url in cards:
        status, text = read_fixture(a.fixtures, url) if a.fixtures else fetch(raw_readme_url(url))
        if status != 200 or not text.strip():
            failed.append((url, "HTTP %d" % status if status el
