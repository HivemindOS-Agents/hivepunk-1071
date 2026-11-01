# issue-watch fixtures

These files are **synthetic samples written by hand** for this tool's self-test.
They are not copied from any website, repository, issue tracker or dataset, and
they describe no real issue, user or observation.

* `issue-64.html` -- a small page that mimics the shape of a public issue page:
a title, an opened date, a status and a one-line finding. The values are
invented.
* Any non-HTML file placed here would be listed by the tool as a row with
`Page opened=no` and blank facts, so an unopened page stays visibly unopened.

Nothing here is a command and nothing here is fetched: the tool reads these
files from disk and never opens a network connection.
