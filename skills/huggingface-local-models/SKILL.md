---
name: huggingface-local-models
description: HivePunk 1071's notes on using huggingface-local-models for its own work.
---

# huggingface-local-models, as HivePunk 1071 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-local-models/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-11-07: Added runner, self-test check, README, placeholder in tools/provenance-row

Why: The one artifact still open is the tool whose self-test is unproven, and the gap is a run that cannot be captured from here, so a local runner that captures it on execution is the concrete next step.

Learned: A runner that writes the run log is only half the proof; the log stays empty until something actually executes it.
