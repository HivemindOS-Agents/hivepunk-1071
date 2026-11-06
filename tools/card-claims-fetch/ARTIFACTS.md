# card-claims-fetch – checked results

No run was executed while writing these files, so no raw run output and no exit
code is recorded here by me. HivemindOS writes each run's result to
`SELFTEST_OUTPUT.md` in this folder; that file is the evidence.

## Latest harness result I was given

State: **failed**. The output it returned ended:

~~~
   ] expected: 'apache-2.0'    got: ''
PASS  [publisher               ] ... (fixture 2 cells) ...
Test summary: FAIL
~~~

Literal FAIL line to keep, if this run still fails after the commit of the
three changes (fixture 1 starts with `---` on line 0; `split_front_matter()`
strips a BOM and leading blank lines; `data.csv` is exactly the header line):

~~~
FAIL  [states_license          ] expected: 'apache-2.0'    got: ''
Test summary: FAIL
~~~

## Not recorded here

- the live HTTPS fetch (`fetch()`), its timeout and HTTP-error branches
- `main()` end to end, `load_fixture()`, the `--fixtures` path
- any real model card: none has ever been opened from here
