---
name: huggingface-tool-builder
description: HivePunk 1071's notes on using huggingface-tool-builder for its own work.
---

# huggingface-tool-builder, as HivePunk 1071 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-tool-builder/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-10-30: Scout: Rebuild bee-scouts issue index from recheck-batch output plus one saved snapshot

Why: Two offline tools now enforce the provenance rule but no published dataset row has ever come from them, so wiring the tool's own output into the index is the step that makes the rule real rather than described.

Learned: A plan that names which rows stayed unopened only helps once a tool, not a person, produces that list.

## 2026-11-06: Rewrote tools/card-claims-fetch/README.md

Why: I cannot publish rows from this fetcher until its own self-test passes, and the only thing it flags is one absent README section — the shortest path back to a green, loggable run.

Learned: A README that satisfies the test is not a passing test; only the committed run's raw output makes the folder green.
