# Open‑weight model cards: what the card itself states

A dataset of the factual claims lodged in open‑weight model card pages visible on the web.  Each row corresponds to one model card that was actually opened during a single session.  All values are taken verbatim from the page itself; no inference, memory or URL pattern guessing is performed.

## Columns

| Column | Description |
|--------|-------------|
| `card_url` | HTTPS URL of the model card page that was opened |
| `publisher` | Organization or person that published the card, as stated on the page |
| `model_name` | The model’s name or title, as shown on the card |
| `date_read` | yyyy‑mm‑dd of the moment the card was opened |
| `states_context_window` | `yes` if the card explicitly mentions a context‑window size, otherwise blank |
| `states_license` | The license stated on the card, e.g. `apache-2.0`, `mit`, or blank |
| `source` | The same URL as `card_url` (kept for redundancy)

Blank fields appear **only when the page did not state the information**.  Nothing is filled in from other sources.

## What was read

No model cards were opened in this session.  The dataset contains only the header line.

## What I could not confirm

- All fields are blank because no page was read.
- No page failed to load (zero attempts).  If that changes, the dataset will be updated accordingly.

## How to use

Load `data.csv` into a spreadsheet or a data‑science environment.  The CSV uses UTF‑8 and the column order is as listed above.

---

Created by bee #1071.
