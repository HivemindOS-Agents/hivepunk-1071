# Drafted standalone path-safe self_test.py, SELFTEST_RUN.txt and SELFTEST_OUTPUT.md (NOT_RUN, no shell here) for tools/provenance-row, plus commit message with command; owner must run and paste real…

**Done**

2026-11-10 11:22 UTC, spent $0.03 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**What I drafted (not run, not committed — no shell here)**

Three file contents for `tools/provenance-row/`, plus the commit message, all written so the folder works when opened alone. The honest status of the recorded run is **NOT_RUN**, which is also what my earlier note on issue #126 says a run without a shell must record.

### 1. `tools/provenance-row/self_test.py` (full contents)

```python
#!/usr/bin/env python3
"""Standalone self-test for tools/provenance-row.

Run from this folder only:
    cd tools/provenance-row && python3 self_test.py

Every path is built from Path(__file__).parent. Nothing is resolved from the
repository root or from the current working directory.

Exit codes
    0  every check passed
    1  at least one check failed
    2  NOT_RUN - a prerequisite was missing, so nothing was proven
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
RUNNER = BASE / "runner.py"
CHILD_ENV = "PROVENANCE_ROW_SELFTEST_CHILD"
EXPECTED_SIBLINGS = ("runner.py", "README.md", "SELFTEST_RUN.txt", "SELFTEST_OUTPUT.md")

results = []  # (status, name, detail)


def record(status, name, detail=""):
    results.append((status, name, detail))


def check_siblings():
    missing = [n for n in EXPECTED_SIBLINGS if not (BASE / n).is_file()]
    if missing:
        record("FAIL", "folder-local siblings", "missing: " + ", ".join(missing))
    else:
        record("PASS", "folder-local siblings",
               f"{len(EXPECTED_SIBLINGS)} files resolved from {BASE}")


def check_no_cwd():
    hits = []
    for name in ("self_test.py", "runner.py"):
        path = BASE / name
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = line.strip()
            if s.startswith("#"):
                continue
            if "os.getcwd(" in s or "Path.cwd(" in s or "os.chdir(" in s:
                hits.append(f"{name}:{i}")
    if hits:
        record("FAIL", "no cwd dependency", ", ".join(hits))
    else:
        record("PASS", "no cwd dependency", "no getcwd/chdir in self_test.py or runner.py")


def check_foreign_cwd():
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ)
        env[CHILD_ENV] = "1"
        env.pop("PYTHONPATH", None)
        proc = subprocess.run([sys.executable, str(BASE / "self_test.py")],
                              cwd=td, env=env, capture_output=True, text=True)
    lines = (proc.stdout + proc.stderr).strip().splitlines() or [""]
    if proc.returncode == 0:
        record("PASS", "runs from a foreign cwd", f"exit=0 outside the folder; {lines[-1]}")
    else:
        record("FAIL", "runs from a foreign cwd", f"exit={proc.returncode}; {lines[-1]}")


def load_runner():
    if not RUNNER.is_file():
        return None
    spec = importlib.util.spec_from_file_location("provenance_row_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check_runner_alignment():
    runner = load_runner()
    if runner is None:
        record("NOT_RUN", "runner.py checks", "runner.py not found next to self_test.py")
        return
    good = getattr(runner, "GOOD_ROW", None) or getattr(runner, "SAMPLE_ROW", None)
    bad = getattr(runner, "BAD_ROW", None)
    entry = None
    for name in ("validate_row", "check_row", "row_checks", "validate"):
        fn = getattr(runner, name, None)
        if callable(fn):
            entry = (name, fn)
            break
    if entry is None or good is None:
        record("NOT_RUN", "runner.py checks",
               f"no agreed entry point or fixture in runner.py "
               f"(entry={entry[0] if entry else None}, fixture={'yes' if good else 'no'})")
        return
    ok = bool(entry[1](good))
    record("PASS" if ok else "FAIL", f"runner.{entry[0]} accepts a good row", repr(good)[:80])
    if bad is not None:
        rejected = not bool(entry[1](bad))
        record("PASS" if rejected else "FAIL", f"runner.{entry[0]} rejects a bad row", repr(bad)[:80])


def main():
    child = os.environ.get(CHILD_ENV) == "1"
    check_siblings()
    check_no_cwd()
    check_runner_alignment()
    if not child:
        check_foreign_cwd()
    for status, name, detail in results:
        print(f"{status}: {name}" + (f" - {detail}" if detail else ""))
    failed = sum(1 for r in results if r[0] == "FAIL")
    notrun = sum(1 for r in results if r[0] == "NOT_RUN")
    passed = sum(1 for r in results if r[0] == "PASS")
    print(f"Total: {passed} passed, {failed} failed, {notrun} not-run")
    code = 1 if failed else (2 if notrun else 0)
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
```

### 2. `tools/provenance-row/SELFTEST_RUN.txt`

```
The recorded self-test run for this folder lives in SELFTEST_OUTPUT.md, next to this file.

Run it yourself with:
    cd tools/provenance-row && python3 self_test.py

Exit codes: 0 = all checks passed, 1 = a check failed, 2 = NOT_RUN (nothing proven).
```

### 3. `tools/provenance-row/SELFTEST_OUTPUT.md`

```markdown
# provenance-row self-test output

Status: NOT_RUN

Command: `cd tools/provenance-row && python3 self_test.py`

Exit code: not captured

Raw output: not captured

Why: this revision was written without a shell. It is a draft; no interpreter ran it.
Run the command above and replace this whole file with the verbatim stdout and the
real exit code, in one commit that also carries the self_test.py change.
```

### 4. Draft commit message

```
provenance-row: run self_test.py standalone from its own folder

self_test.py now builds every path from Path(__file__).parent: it
resolves its sibling files from BASE, imports runner.py by file path,
and re-runs itself in a temporary directory to prove it does not
depend on
