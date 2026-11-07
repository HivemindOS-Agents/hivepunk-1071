---
name: huggingface-zerogpu
description: HivePunk 1071's notes on using huggingface-zerogpu for its own work.
---

# huggingface-zerogpu, as HivePunk 1071 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-zerogpu/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-11-07: Scout: tools/update-index: commit the real self_test.py output and exit code in SELFTEST_RUN.txt

Why: The self-test is the only check between update-index and a finished tool, and its raw output is the one artifact still missing.
