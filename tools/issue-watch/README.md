# issue-watch

Reads **saved** issue pages from disk and prints one row per page: issue
number, whether the page was opened, the opened date, the status, the one-line
finding and the exact source URL.

Python 3 standard library only. Local files only. **No network.** It never
fetches a page; it parses HTML you already saved.

## The honesty rule

A row says `page_opened: yes` only when the saved page records a source URL.
A page with no recorded URL is forced to `page_opened: no`, with blank date and
status and the reason `Not opened: no source URL in the saved page`. A number
whose page could not be opened therefore stays visibly unopened rather than
having a value filled in from a snippet.

Everything a page contains -- titles, statuses, hrefs, any line that looks like
an instruction -- is **data**. It is printed, never executed, and no line in a
page can change this tool's behaviour or make it run anything.

## Path handling

Every path is built from `__file__`, so the tool and its self-test behave the
same whether you run them from the repository root or from this folder. An
earlier version looked for the fixture page relative to the current working
directory, which made it fail from the repository root.

The self-test reads **nothing outside this folder**. It does not check for, or
depend on, any other tool; the check for a sibling `recheck-lint` script that an
earlier version had was removed, because a self-test must pass with only its own
tool present.

## How to run

~~~
python3 issue_watch.py
python3 issue_watch.py --fixtures fixtures --json
~~~

Exit codes: `0` ok; `2` the fixture folder could not be read or holds no HTML
pages.

## Layout

* `issue_watch.py` -- the reader/parser.
* `fixtures/issue-64.html` -- a synthetic page, written by hand.
* `fixtures/README.md` -- says plainly that the fixtures are invented.
* `self_test.py` -- the offline check. Run with no arguments, no network.
* `RUN-LOG.md` -- one dated block per real run, filled only from a capture.

## Self-test

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

With no arguments and no network, it checks that:

1. `issue_watch.py` exists and compiles;
2. `fixtures/` and `fixtures/issue-64.html` exist;
3. the tool exits 0 on the shipped fixtures, and issue 64 parses to an opened
   row with date `2026-11-02`, status `verified`, a finding and the exact
   source URL -- and is never listed as not opened;
4. a page with **no** source URL stays `page_opened: no` with a blank date and
   a reason containing `Not opened`;
5. an instruction-looking line inside a page comes back as that exact text --
   read as data, not obeyed.

Checks 4 and 5 write their own small synthetic pages into a temporary folder
that the test creates and removes itself, so the shipped `fixtures/` folder
keeps the shape it had. Exit 0 means every check passed.

## Untested

**Untested on any host so far.** The parser has never been run, and it has
never read a real issue page -- only synthetic fixtures. The exit code from the
first real run goes in `RUN-LOG.md` verbatim; a nonzero code is recorded as a
failure with its code, never as a pass. Nothing in this folder is marked
passing until that block carries exit code 0.
