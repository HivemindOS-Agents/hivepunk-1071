# issue-index upkeep -- how to run it

Run `python3 update_index.py INPUT.csv -o OUTDIR` on a five-column index (`Issue, Page opened, Date checked, Status, What it showed`); it writes `OUTDIR/issues.csv` (natural sort by Issue) and `OUTDIR/change_report.txt` (ADDED / REMOVED / CHANGED against the previous `issues.csv`). Exit 0 ok, 1 validation failed with nothing written, 2 usage/IO error. `update_index.py` is **UNTESTED**: never executed, stdlib only, local files only, no network. Try it first on `sample_input.csv`.

## First test run (nothing outside your machine is touched)

    python3 update_index.py sample_input.csv -o /tmp/idx    # 4 rows ok, no changes
    python3 update_index.py sample_input.csv -o /tmp/idx    # second run: "no changes"

## Commit message

    Add update_index.py: validate, natural-sort and diff the bee-scouts issue index

    - checks the fixed five-column header (Issue, Page opened, Date checked, Status, What it showed)
    - enforces Status in unverified / verified / cannot-check
    - requires Date checked to be a real YYYY-MM-DD calendar date
    - writes issues.csv (natural sort by Issue) and change_report.txt (ADDED/REMOVED/CHANGED)
    - UNTESTED: never executed; stdlib only; local files only; no network
