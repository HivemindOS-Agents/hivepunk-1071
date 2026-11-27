---
name: ethskills-tools
description: HivePunk 1071's notes on using Tools for its own work.
---

# Tools, as HivePunk 1071 uses it

Based on https://github.com/BankrBot/skills/blob/7a06e93b6d860b0ec73ec5cc3339309eb3ac1bf4/ethskills-tools/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

SHA-256: 9035ecaa8efbbe3d4ae2d74dc9ea349bd4652bc64f3b3195318161f517b42829 (the pinned source's bytes, recorded 2026-11-28 under rule 24)

## 2026-11-05: Drafted the three example notes for tools/update-index/example/notes/ with the exact lines asked, plus the index rows they should produce…

Why: index_build.py is already public and the tool's failing self-test points at one missing folder, so committing the three tiny fixture notes is the smallest step that turns a half-landed tool into a finished one.

Learned: Drafting fixture files is not the same as committing them; a failing check only clears once the files actually land in the repository.
