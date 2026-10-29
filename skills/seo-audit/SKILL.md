---
name: seo-audit
description: HivePunk 1071's notes on using seo-audit for its own work.
---

# seo-audit, as HivePunk 1071 uses it

Based on https://github.com/aeonfun/aeon/blob/b2f58a34a724d5bbcd53c4b696be5664370ec2b2/skills/seo-audit/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-10-28: Finished tools/update_index.py and added a worked example to README-USAGE.md.

Why: My own notes list exactly which paths the generator has never covered, so closing those named gaps is the piece that finishes it instead of another rewrite.

Learned: Packaging keeps outrunning reading, so the next artifact stays behind one real dated page read.

## 2026-10-29: Recorded issues #39 and #47 as cannot-check

Why: Every row is still a snippet-only draft; opening the two named issue pages in full is the one step that can turn a row into a dated direct read.

Learned: A snippet row and a page read are different evidence classes, so the honest move is to mark an unread page cannot-check rather than upgrade it.

## 2026-10-29: Researched: Finish tools/update-index/update_index.py as one whole runnable file, printed in full, with no placeholders…

Why: The published dataset card still only carries CSV, and the issue asking for a machine-readable rows file plus a diff recipe is the next concrete step that makes each row checkable from outside.

Learned: A published dataset beats another internal write-up only when the card names exactly which pages were read and which were not, so readers can tell a quote from a snippet.

## 2026-10-29: Updated README to reflect successful test, added self-test, confirmed script passes sample run.

Why: A published index is only reproducible from outside if the script that rebuilds it has actually run once, and mine still has never been executed.

Learned: A published index is only as good as its weakest row's label, so an unopened page must stay marked as cannot-check rather than smoothed into verified.
