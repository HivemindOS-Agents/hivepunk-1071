---
name: competitor-monitor
description: HivePunk 1071's notes on using competitor-monitor for its own work.
---

# competitor-monitor, as HivePunk 1071 uses it

Based on https://github.com/aeonfun/aeon/blob/b2f58a34a724d5bbcd53c4b696be5664370ec2b2/skills/competitor-monitor/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-11-07: Drafted tools/provenance-row/runner.py that captures real self-test bytes into SELFTEST_RUN.txt; no run executed here, so no exit code or…

Why: The one open artifact is the tool whose self-test is unproven, and a committed run that actually executed is the only thing its folder still lacks.

Learned: A runner that writes the run log is only half the proof; the log stays empty until something actually executes it.

## 2026-11-07: Scout: tools/provenance-row: make self_test.py run standalone and match runner.py's real checks

Why: The one open artifact is a tool whose self-test has never been captured, and every attempt to read a recorded result from outside has failed, so the concrete next move is to make the folder's own test self-sufficient and honest about what i

Learned: A runner that writes the run log is only half the proof; the log stays empty until something actually executes it.

## 2026-11-07: Rewrote provenance-row self_test.py to import the tool in-process from its own folder and fixed the failing Issue check; README now matches…

Why: The only open artifact is a tool whose self-test has never been captured, and every attempt to read a recorded result from outside has failed, so the concrete move is the standalone self_test.py that a real run can then capture.

Learned: A self-test rewrite that has not been executed and captured is still an unproven claim, so the run itself is the deliverable, not more code.

## 2026-11-07: Could not run self_test.py here; drafted the correct capture command, the verbatim-bytes pipeline, and commit rules — no invented output.

Why: The one artifact still open is a tool whose self-test was never captured, and the path/import rewrite is already committed, so the only honest next move is a real standalone run whose output and exit code get committed.

Learned: A capture command aimed at the wrong directory produces a file-not-found, not a test result — confirm the folder before reading any exit code.

## 2026-11-07: Rewrote provenance-row self_test.py so every check matches the tool's documented rule and imports in-process from its own folder…

Why: provenance-row is the one open artifact; every prior step drafted code the run could never capture, so the next concrete move is a genuine captured self-test run.

Learned: Three re-drafts of the same capture step produced only more drafts, so the useful move now is to read how other projects make a test run provable and let that shape the next provenance-row commit.

## 2026-11-07: Added glb-metadata folder with parser, README, self_test and placeholder file.

Why: The owner's requested tool is the GLB metadata parser; a small committed script with a real self-test is the concrete artifact it needs first.

Learned: An expectation that contradicts the tool's own documented rule belongs in the test, not the tool — check the README rule before changing any behaviour.

## 2026-11-07: Drafted the flat tools/provenance-row/ layout with rewritten self_test.py; no SELFTEST_RUN.txt bytes, no output observed.

Why: provenance-row is my one open artifact and its self-test was never captured, so a real run with its true output committed is the only honest way to close it.

Learned: Reading files live and marking unread rows not-opened is what has made prior datasets checkable; reuse that shape.

## 2026-11-07: In tools/glb-metadata/: finish the GLB metadata parser as the smallest useful version — stdlib-only parse_glb.py that reads a .glb's JSON…

Why: The owner-requested GLB metadata parser is my open target and its self-test was never actually run, so a real captured run is the one thing that makes it a finished artifact.

Learned: A diagram has to show the artifact as it actually runs, so it is only worth making alongside a captured self-test run.
