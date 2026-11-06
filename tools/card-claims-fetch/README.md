# card-claims-fetch

## Purpose

`fetch_cards.py` is a lightweight, **stdlib‑only** command that fetches the eight candidate model‑card URLs listed in the Open‑weight model‑cards dataset README. For each card it extracts only the information that the card **owns**:

* publisher – the organization appearing on the page
* model name – the title shown on the card or the `model_name` front‑matter field
* stated context window – any explicit token‑count mentioned on the card
* stated license – the license string from the card’s front‑matter

No inference, no external API calls, and no mutation of the card are performed. Cells are left blank if the card does not state the field.

The tool writes:

* `data.csv` – a CSV with one row per successfully fetched card
* `notes.md` – a Markdown list of missing or failed cards, inserted for
  manual review

Both outputs are produced in the directory passed via `--out` (default `.`).  In
offline mode the tool can read local fixture files (plain `.md` with an optional
`.status` file) with `--fixtures`.

### Caveats

* The tool only works with publicly readable Hugging Face card pages.
* Large front‑matter tables or non‑standard key names are not handled.
* The output is *not* test‑validated except for the empty‑dataset self‑test.
* Network failure or unexpected HTML changes will result in a failure row.

© 2026 HivePunk – no licence claimed.

---

Run the tool:

```
python3 fetch_cards.py --out .
```

Or with fixtures:

```
python3 fetch_cards.py --fixtures fixtures/ --out .
```

For further testing the provided `self_test.py` can be executed.
