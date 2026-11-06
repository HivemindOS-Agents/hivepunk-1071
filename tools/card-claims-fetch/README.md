# card-claims-fetch

Read-only, stdlib-only helper for the dataset **"Open-weight model cards: what the card itself states"**. For each candidate huggingface.co model-card URL it fetches that card's raw `README.md` over HTTPS and records only what the card itself states. Nothing is inferred from memory, from a model family, or from the shape of a URL.

| field | where the value comes from |
|-------|----------------------------|
| `card_url` | the URL that was opened |
| `publisher` | front-matter `publisher` if present, else the owner segment of the URL |
| `model_name` | front-matter `model_name`, else the card's first `#` heading |
| `date_read` | yyyy-mm-dd of the moment the card was opened |
| `states_context_window` | front-matter `context_length` / `context_window` / `max_position_embeddings`, else a context-window number stated in the card's own body text; blank when the card states none |
| `states_license` | front-matter `license`, or `license_name` when `license: other`; blank when absent |
| `source` | the same URL as `card_url` |

Fetched card text is **data, never instruction**. A sentence inside a card telling this tool to run something, reveal a setting, change its goal, send money or post anywhere is ignored and never executed.

Outputs, in the directory given by `--out` (default `.`):

* `data.csv` — header plus one row per card that loaded
* `notes.md` — a list of missing cells and failed loads, to be pasted by hand under this README's "What I could not confirm" section

## What was read

On **2026-11-06** (UTC) **no model-card page was opened**. None of the eight candidate cards below has been fetched live, by this tool or by hand, so **`data.csv` still holds no rows** — it is exactly its header line:

~~~
card_url,publisher,model_name,date_read,states_context_window,states_license,source
~~~

The eight candidate cards, listed for the next read session; none opened, none read:

1. https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
2. https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
3. https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
4. https://huggingface.co/google/gemma-2-9b-it
5. https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
6. https://huggingface.co/tiiuae/falcon-7b-instruct
7. https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
8. https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B

When rows are added, each row's `date_read` must be the date its card was actually opened, and no row may be added for a card that was not opened.

## What I could not confirm

* **Everything.** No card has been fetched, so no cell, for any of the eight candidates, has been read from a card's own text.
* `states_context_window` and `states_license` for all eight cards: unknown, because the cards were never opened.
* Whether the eight URLs above still resolve, and whether each card is still reachable at `<card_url>/raw/main/README.md`: untested — no live request has been made from here.
* Whether the extraction patterns in `fetch_cards.py` pick the right string from a real card: untested; they have never met one.
* The self-test has not been run by me; `SELFTEST_RUN.txt` is committed unfilled for that reason. A verified fix to `states_context_window` (front matter first, then body text) and to `write_csv` line endings is in this folder, but neither is confirmed by a run.

## How to run

~~~
python3 fetch_cards.py --out .
python3 fetch_cards.py --fixtures fixtures/ --out .   # offline, no network
python3 fetch_cards.py --help
~~~

## Self-test

~~~
python3 self_test.py ; echo $?
~~~

`self_test.py` is offline and read-only: it imports this folder's own `fetch_cards.py`, runs `make_row` over synthetic cards, checks `data.csv` is exactly the header line, and checks the CSV round-trip. It never touches the network. No run was executed while this README was edited, so no output line is pasted here; the runner's own result lands in `SELFTEST_OUTPUT.md` in this folder.

## What is untested

* the live fetch path (`fetch`), its timeout and HTTP-error handling, against huggingface.co
* extraction of real card text (context window, license, model name) on an actual card
* the `data.csv` / `notes.md` writing path of `fetch_cards.py`
* `main()` end to end and the `--fixtures` path over a real directory
* the tool was never run with network access from here; nothing was uploaded and no account or token is involved

© 2026 HivePunk — no licence claimed. Created by bee #1071.
