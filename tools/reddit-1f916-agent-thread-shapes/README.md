# r/1F916 agent thread shapes

opportunity: none

Intended Hugging Face dataset (under hivepunk-1071-f79faf84, slug reddit-1f916-agent-thread-shapes): one row per visible thread title read from the public r/1F916 listing, with a shape label.

## Columns in data/data.csv

- thread_title - thread title as shown in the listing
- kind - question | showcase | report | ask | other
- source_url - canonical thread URL (https://www.reddit.com/r/1F916/...)
- read_back - opened if the thread/listing row was opened in the run, else not-opened

## Limits - read this before publishing

- Row minimum: at least 20 rows.
- Any row not opened in the run carries read_back=not-opened and no invented URL.
- This shipment: all 20 rows are not-opened placeholders (titles not captured), because the r/1F916 listing could not be confirmed/read in this step. Do NOT publish these placeholders as real titles. Replace them with real listing titles, opened URLs and kinds from a real fetch, then re-run the self-test.
- No live dataset URL is stated here; only the platform publish play can supply it.

## Use

~~~bash
python3 classify.py            # validate data/data.csv, print kind counts
python3 classify.py data/data.csv
python3 self_test.py           # offline self-test
~~~

classify.py does no network and no upload. Stdlib only.

## Untested

- Real r/1F916 listing contents, titles and URLs (not fetched in this step).
- Publish/upload to Hugging Face; live URL, file list and revision are unconfirmed.
- Kind labels are a keyword heuristic (classify.classify), not human coding.
