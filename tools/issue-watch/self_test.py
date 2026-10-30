#!/usr/bin/env python3
"""self_test.py -- offline checks for issue_watch.py.

Run with no arguments, no network. Exits 0 only when every check passes.
Everything runs on the synthetic fixture pages in fixtures/.
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "issue_watch.py")
PAGES = os.path.join(HERE, "fixtures")
FIELDS = ["issue", "title", "state", "opened_date", "labels", "ask",
          "source_url", "read_status"]
FACT_FIELDS = ["title", "state", "opened_date", "labels", "ask"]


def run(args):
    return subprocess.run([sys.executable, SCRIPT] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, cwd=HERE)


def check(cond, label):
    if not cond:
        print("FAIL: " + label)
        sys.exit(1)
    print("ok: " + label)


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames, [dict((k, (v or "").strip()) for k, v in r.items())
                                   for r in reader]


def main():
    check(os.path.isdir(PAGES), "fixtures/ exists")
    check(os.path.isfile(os.path.join(PAGES, "64.md")), "fixture page 64.md exists")
    check(not os.path.isfile(os.path.join(PAGES, "65.md")),
          "fixture has no page for 65 (the missing case)")

    work = tempfile.mkdtemp(prefix="issue-watch-selftest-")
    try:
        data = os.path.join(work, "data.csv")
        card = os.path.join(work, "README.md")

        res = run(["64", "66", "--pages", PAGES, "--data", data, "--card", card])
        check(res.returncode == 0, "run over #64-#66 exits 0")

        header, rows = load(data)
        check(header == FIELDS, "data.csv header is the exact eight fields")
        check(len(rows) == 3, "data.csv holds one row per number in the range")
        check([r["issue"] for r in rows] == ["64", "65", "66"],
              "rows are numeric-ordered 64, 65, 66")

        by = dict((r["issue"], r) for r in rows)
        check(by["64"]["read_status"] == "opened", "#64 has a saved page so is opened")
        check(by["66"]["read_status"] == "opened", "#66 has a saved page so is opened")
        check(by["65"]["read_status"] == "not-opened",
              "#65 has no saved page so is not-opened")
        check(all(not by["65"][f] for f in FACT_FIELDS),
              "the not-opened row has every fact field blank")
        check(all(by["65"][f] == "" for f in FACT_FIELDS),
              "no snippet value leaked into the not-opened row")
        check(by["64"]["title"] != "" and by["64"]["ask"] != "",
              "the opened row carries the facts from its saved page")
        check(by["64"]["source_url"].endswith("/issues/64"),
              "the opened row keeps a per-number source_url")
        check(by["65"]["source_url"].endswith("/issues/65"),
              "the not-opened row still records its source_url")

        with open(card, encoding="utf-8") as fh:
            text = fh.read()
        check("Rows not opened" in text, "card ends with a Rows not opened section")
        tail = text.split("Rows not opened", 1)[1]
        check("#65" in tail, "the not-opened number #65 is named in that section")
        check("#64" not in tail and "#66" not in tail,
              "opened numbers are not listed as not opened")
        check("No row had a second read" in text,
              "card states plainly that no row had a second read")
        check("which numbers exist" in text.lower() or "which do not" in text.lower(),
              "card says which numbers exist and which do not")

        res = run(["64", "66", "--pages", PAGES, "--data", data, "--card", card,
                   "--dry-run"])
        check(res.returncode == 0, "dry run exits 0")
        check("wrote" not in res.stdout, "dry run writes nothing")

        res = run(["64", "66", "--allow-facts", "--pages", PAGES,
                   "--data", os.path.join(work, "a.csv")])
        check(res.returncode == 2, "--allow-facts with --pages exits 2")

        allpath = os.path.join(work, "all.csv")
        res = run(["64", "66", "--allow-facts", "--data", allpath,
                   "--card", os.path.join(work, "all.md")])
        check(res.returncode == 0, "run with no pages at all exits 0")
        _, rows2 = load(allpath)
        check(all(r["read_status"] == "not-opened" for r in rows2),
              "with no pages every row is not-opened")
        check(all(all(r[f] == "" for f in FACT_FIELDS) for r in rows2),
              "with no pages every fact field is blank")

        res = run(["--verify", data])
        check(res.returncode == 0, "verify accepts the tool's own data.csv")

        broken = os.path.join(work, "broken.csv")
        with open(broken, "w", newline="", encoding="utf-8") as fh:
            fh.write(",".join(FIELDS) + "\n")
            fh.write("99,Guessed title,Open,2026-10-30,bee-1071,Invented ask,"
                     "https://github.com/LiamVisionary/bee-scouts/issues/99,"
                     "not-opened\n")
        res = run(["--verify", broken])
        check(res.returncode == 1, "verify rejects a not-opened row carrying facts")

        res = run(["80", "64"])
        check(res.returncode == 2, "a reversed range exits 2")

        res = run(["64", "66", "--checked", "2026-02-30"])
        check(res.returncode == 2, "an impossible --checked date exits 2")

        res = run(["64", "66", "--pages", PAGES, "--data",
                   os.path.join(work, "sub", "d.csv"), "--card",
                   os.path.join(work, "sub", "c.md")])
        check(res.returncode == 0, "writing into a new subdirectory exits 0")
        check(os.path.isfile(os.path.join(work, "sub", "d.csv")),
              "the nested data.csv was created")

        print("all checks passed")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
