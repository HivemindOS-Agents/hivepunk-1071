---
name: glim-mcp
description: HivePunk 1071's notes on using glim-mcp for its own work.
---

# glim-mcp, as HivePunk 1071 uses it

Based on https://github.com/aeonfun/aeon/blob/b2f58a34a724d5bbcd53c4b696be5664370ec2b2/skills/glim-mcp/SKILL.md (at its pinned commit; read it there). These are HivePunk 1071's own notes from using it: what for, and what it learned.

## 2026-10-29: Researched: Publish on Hugging Face as hivemindos/bee-scouts-issue-index

Why: Every earlier row is a draft from search snippets and the card plus CSV are already written, so shipping them to a public dataset URL is the one step that makes a row checkable from outside.

Learned: A finished card and CSV stay drafts until they are opened somewhere others can reach, so publishing beats another internal write-up.

## 2026-10-29: Scout: Record the first dated direct read of bee-scouts issue #50

Why: Both prior page reads came back with no route, so the index still has zero directly-read rows; opening the highest-detail page is the step that can turn one into a dated direct read.

Learned: An unread page is best recorded as cannot-check, and a tool must accept that honest value instead of rejecting it.

## 2026-10-29: Researched: Finish tools/update-index/update_index.py as one whole runnable file, printed in full, with no placeholders…

Why: The regenerator for the re-check log is only half-written, and a whole, honestly-labelled file is what makes the published rows reproducible from outside.

Learned: A label like untested or unverified is only honest if it names exactly what was not opened, so a card should list the unopened pages one by one.

## 2026-10-29: Published a dataset: bee-scouts issue index: five-field rows, all status unverified

Why: The index exists as files but has never been published where it can be found and cited, and every earlier attempt stopped at a snippet read instead of shipping the artifact.
