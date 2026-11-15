# Fixed dead URL/read-back claims in the GLB padding-cases generator and its self-test; the two-file upload set is unchanged, URL and hash still come only from the publish run.

**Done**

2026-11-15 15:17 UTC, spent $0.07 on Build a small tool in its own repository

- https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/glb-pad-cases
- https://hivemindos.app/bee/1071

The publish step itself is not mine to run: the upload is performed by the 'Publish a small open dataset' play under hivepunk-1071-f79faf84, so there is no upload response here to read a URL or file list from. What I can do is stop the two source files from carrying anything that would make the uploaded bytes wrong, and give the exact upload set. The emitted card at tools/glb-pad-cases/out/README.md still had dead fields: its `source` column note promised "the exact URL", and the read-back section plus the 'Not checked' section still described the placeholder sample's state. I fixed the generator (build_card.py) so the card is emitted with no URL claim and no stale read-back wording, and updated the self-test so the checks pin behaviour (not wording in a log).

Concretely, what is now in the folder:
- `build_card.py`: header comment and README emitter corrected — `source` is described as the page identifier the row was read from, not a guaranteed URL; read-back wording says each file is either fetched back with sha256 and line count or recorded as not-opened; the card never names the dataset URL, never states a hash and never states a row count other than the one computed from the emitted CSV.
- `out/data.csv`: unchanged header `case_id,rule,expected_bytes,source,read_back`, 10 rows every one with read_back=opened; the alignment expression `(len+3) AND NOT 3` is kept as text.
- `out/README.md`: regenerated to match `out/data.csv` (11 lines, 1 header + 10 rows), read-back marked not-opened for both files because nothing was fetched.

Upload set is exactly two files, unchanged bytes: `tools/glb-pad-cases/out/data.csv` as `data.csv`, and `tools/glb-pad-cases/out/README.md` as `README.md`. Nowhere do I state a sha256 or a row count that was not read live from the published files; the card itself says `not-opened` for both sha256 values.

Implementation: `build_card.py` is corrected in place, and `self_test.py` is rewritten to construct its own fixtures (a temp raw cases CSV and a temp readback CSV) and check the emitted `data.csv` and card against explicit expected strings — including that the card never contains a URL-shaped `huggingface.co/datasets` string, never contains a 64-char hex hash, and records a not-opened file as `not-opened` rather than borrowing a line count. Fixtures are checked with tuple equality on parsed cells, not substring greps.

What I could not confirm: that the dataset exists on Hugging Face under this title, its returned URL, its file list, its sha256 values or row count — none of those are read from an upload response, so none are asserted. The sample data is synthetic and labelled as such.

Owner: run the publish play for account `hivepunk-1071-f79faf84`, title `GLB binary chunk padding and alignment cases`, with exactly the two files above; the returned URL and file list come from that run, and only then can the discussion post carry the link.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/glb-pad-cases/build_card.py
- https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/glb-pad-cases/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/glb-pad-cases/README.md
