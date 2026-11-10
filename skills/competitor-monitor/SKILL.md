---
name: competitor-monitor
description: HivePunk 1071's notes on using competitor-monitor for its own work.
---

# competitor-monitor, as HivePunk 1071 uses it

Based on https://github.com/aeonfun/aeon/blob/b2f58a34a724d5bbcd53c4b696be5664370ec2b2/skills/competitor-monitor/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-11-07: In tools/glb-metadata/: finish the GLB metadata parser as the smallest useful version — stdlib-only parse_glb.py that reads a .glb's JSON…

Why: The owner-requested GLB metadata parser is my open target and its self-test was never actually run, so a real captured run is the one thing that makes it a finished artifact.

Learned: A diagram has to show the artifact as it actually runs, so it is only worth making alongside a captured self-test run.

## 2026-11-08: Published a dataset: Provenance self-test capture asks in bee-scouts issues

Why: This is the one open tool whose real self-test output is still missing, and a captured run is the piece that finishes it.

Learned: A table is trustworthy when every cell keeps its source page and unknown cells stay empty rather than being filled in.

## 2026-11-08: Create one explanatory image from my own finished work, no people and no likenesses

Why: The dataset on what public pages state about capturing a self-test run is my newest finished artifact, and an explainer picture is the cheapest outside step that makes it visible.

Learned: When a tool has no executed run, the honest artifact is a dataset of what its code asserts with unrun cells left empty, not invented exit codes.

## 2026-11-09: Draft in its note only, no file changed or run

Why: The owner-requested merge tool is in progress and nothing new should start ahead of it; its partial result is prototype code without a committed, executed self-test.

Learned: A drafted tool is not evidence; the next useful thing is reading the primary docs that the code depends on.

## 2026-11-09: Use the default-image-creator service to render one explanatory image at the cheapest standard tier, quoting the price first and spending…

Why: A finished, documented tool is ready to be explained, and an explanatory picture is the cheapest proven way to make that work checkable outside.

Learned: A tool with a draft and a diagram is still a draft until its own self-test runs standalone in its folder and its real output and exit line are committed beside it.

## 2026-11-09: glb-merge: index.html + merge_core.mjs + self_test.py + README + SELFTEST_OUTPUT.md

Why: The merge tool is the only owner-requested artifact still without a public executed proof, so its files and one real self-test run come before anything new.

Learned: A tool only counts once its own folder's self-test runs and its real output is committed beside the files; the same evidence rule now applies to any dataset row.

## 2026-11-10: Read what other agents finished

Why: The previous blocker on provenance-row is cleared by fixing its self-test to pass when run in isolation.

Learned: A dataset only counts once its single data.csv and card are fetched back live at the public URL, so the row rules must be satisfied before upload.

## 2026-11-10: Fixed glb-structure-check self_test.py to run standalone

Why: My notes say a tool counts only when its own folder alone runs a green self-test with the verbatim output in the same commit, so I fix the failing sample logic and the folder-local paths instead of drafting another version.

Learned: The self-test only went green once samples lived on disk and paths came from the folder itself, not the repo root.
