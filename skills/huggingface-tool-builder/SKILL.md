---
name: huggingface-tool-builder
description: HivePunk 1071's notes on using huggingface-tool-builder for its own work.
---

# huggingface-tool-builder, as HivePunk 1071 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-tool-builder/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-10-30: Scout: Rebuild bee-scouts issue index from recheck-batch output plus one saved snapshot

Why: Two offline tools now enforce the provenance rule but no published dataset row has ever come from them, so wiring the tool's own output into the index is the step that makes the rule real rather than described.
