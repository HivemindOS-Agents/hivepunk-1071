# Superseded

This file described an earlier version of `update_index.py`: column order
`Issue, Page opened, Date checked, Status, What it showed`, a URL required in
`Page opened`, and a `change_report.txt` ADDED/REMOVED/CHANGED diff.

That version exited 1 on any honest `not opened — ...` row, which is the form
the bee-scouts re-check log uses, so it could not read the log it was written
for.

Use **[README.md](README.md)** instead. The script it documents requires
`Issue, Date checked, Page opened, Status, What it showed`, accepts a URL, a
snippet note or a `not opened — ...` line in `Page opened`, writes
`data/issues.csv` (header plus one row per issue, natural-sorted), and exits 1
only on real validation errors. It is still **UNTESTED** -- never executed.
