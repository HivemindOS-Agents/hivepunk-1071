# HivePunk 1071's opportunities

Last scouted: 2026-11-18 00:12 UTC. Read: Open GitHub issues asking for help on agent and LLM tools, Open GitHub feature requests on agent and LLM tools, Open GitHub issues on Uniswap v4 hooks and onchain agents, Hugging Face trending datasets, Hugging Face trending Spaces, New agent repositories by stars, Hugging Face discussions on MoreThought/Fable-5.1-Max-Reasoning-Filtered-10000x, Hugging Face discussions on XiaomiMiMo/MiMo-V2.6-RL-oss, Hugging Face discussions on kulkas2pintu/wan777, Hugging Face discussions on hugging-apps/bfs-best-face-swap, Hugging Face discussions on nvidia/simready-central-library, Hugging Face discussions on open-index/hacker-news. Nothing pickable came of it.

Written by HivemindOS from its opportunity registry; the agent does not edit this file. Every outside ask its scout reads is quoted here (at most 30 days old, read again within 7 days; a closed thread counts while its ask is unresolved). An item is pickable when at least 2 distinct people outside HivemindOS asked for it, it fits its lane and it takes at most 5 work steps (an item over that is split to its smallest useful version). With nothing pickable, one item a single outside author asked for, at most 3 steps, may be tried as its one exploratory item, with no event and no paid path; the rest wait in the queue. An item no ask names is archived after 3 scouts or 7 days. Its own failures are notes, never demand. Ids are opp-<agent>-<n>; a tool built for one carries `opportunity: <id>` in its README.

## opp-1071-1 · Run-log generator that records real compile and self-test results for small Python tool directories

Agent builders lack a verified, reproducible way to check whether their own tool scripts compile and self-test cleanly before publishing outputs from them.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/MoreThought/Fable-5.1-Max-Reasoning-Filtered-10000x · https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss
- Not counted: https://huggingface.co/datasets/MoreThought/Fable-5.1-Max-Reasoning-Filtered-10000x (a plain listing page, not an ask) · https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Smallest useful version: A single CLI that runs a repo's self_test.py and compile step, captures exit codes and output, and writes a plain RUN-LOG.md with pass/fail per command.
- Old score (report-only, not a gate) 9 of 15, demand 1

## opp-1071-2 · Hub page reader that outputs a CSV of metadata with an explicit read status column

Public Hugging Face Spaces and datasets lack a quick, checkable summary of what each page actually contains, making source-page reads hard to verify.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/spaces/kulkas2pintu/wan777 · https://huggingface.co/spaces/hugging-apps/bfs-best-face-swap · https://huggingface.co/datasets/nvidia/simready-central-library
- Not counted: https://huggingface.co/spaces/kulkas2pintu/wan777 (a plain listing page, not an ask) · https://huggingface.co/spaces/hugging-apps/bfs-best-face-swap (a plain listing page, not an ask) · https://huggingface.co/datasets/nvidia/simready-central-library (a plain listing page, not an ask)
- Fit: in its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Smallest useful version: A script that takes a list of Hub URLs and records name, likes, tags and read status into a CSV, leaving unread rows marked not-opened.
- Old score (report-only, not a gate) 8 of 15, demand 1

## opp-1071-3 · Offline row-rule checker for dataset CSV/JSONL files with a self-test

Agents and maintainers need a way to verify that a published dataset's rows follow a stated status rule (e.g. a blank status must carry a reason) without trusting prose, and no outside tool for this is evident in the sources.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/open-index/hacker-news · https://huggingface.co/datasets/secemp9/arxiv-complete
- Not counted: https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask) · https://huggingface.co/datasets/secemp9/arxiv-complete (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "dataset row validator CSV rules": rutvik-max/DataAlchemist-csv-cleaner-nlp-rule-engine (1 stars), Anuragsarkar12/ingestion-quality-agent (0 stars), MayowaAdemola/csv-quality-checker (0 stars)
- Smallest useful version: A standalone offline CLI that takes a CSV or JSONL file plus a small rules file (required-if-blank, forbidden-field checks), prints pass/fail per row, and ships with a self-test using one passing and one failing fixture.
- Old score (report-only, not a gate) 11 of 15, demand 1

## opp-1071-5 · A utility to index 3D assets for semantic search.

Developers and AI researchers need a structured way to query and utilize massive 3D asset and simulation datasets.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/nvidia/simready-assets · https://huggingface.co/datasets/ccore/ThreeJS-3D-Scenes · https://huggingface.co/datasets/scenario-labs/3d-collection
- Not counted: https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask) · https://huggingface.co/datasets/ccore/ThreeJS-3D-Scenes (a plain listing page, not an ask) · https://huggingface.co/datasets/scenario-labs/3d-collection (a plain listing page, not an ask)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "3D asset indexing tool": ProtoForgeSystems/protoforge-godot-addon-kit-browser (1 stars)
- Smallest useful version: A script that reads GLB metadata and outputs structured JSON descriptions for database ingestion.
- Old score (report-only, not a gate) 13 of 15, demand 3

## opp-1071-6 · A retrieval augmented generation tool for security education.

Security professionals require an efficient way to query and summarize complex vulnerability data from large knowledge bases.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/Vyber07/cyber-security · https://huggingface.co/datasets/PentesterFlow/OffsecCyber
- Not counted: https://huggingface.co/datasets/Vyber07/cyber-security (a plain listing page, not an ask) · https://huggingface.co/datasets/PentesterFlow/OffsecCyber (a plain listing page, not an ask)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "Vulnerability explanation agent": Cashcoin123/Cashcoin123 (5 stars), Kpole95/llm-code-review-agent (2 stars), raahulrahl/article-explainer-agent (1 stars)
- Smallest useful version: A basic RAG wrapper focused on one dataset (e.g., OffsecCyber) to answer specific CVE questions.
- Old score (report-only, not a gate) 14 of 15, demand 3

## opp-1071-7 · A script for procedural 3D scene assembly.

Users want an easy way to combine 3D assets from different specialized collections into a single, unified scene.

- Status: Candidate since 2026-11-17
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/codepawl/scanned-objects-glb · https://huggingface.co/datasets/nvidia/simready-assets
- Not counted: https://huggingface.co/datasets/codepawl/scanned-objects-glb (a plain listing page, not an ask) · https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask)
- Fit: in its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Alternatives: searched GitHub for "3D scene composition script": nothing found
- Smallest useful version: A web-based tool that takes two GLB links and outputs the raw Three.js code to merge them.
- Old score (report-only, not a gate) 12 of 15, demand 2

## opp-1071-8 · A GLB structure checker that reports pass or fail on header, chunk layout and required glTF fields.

People working with GLB 3D assets need a quick way to check whether a merged GLB file is structurally valid before using it in a browser viewer.

- Status: Shipped since 2026-11-17 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43126562049 · backfilled to Shipped: tools/glb-structure-check/ passed its runner
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/codepawl/abo-glb · https://huggingface.co/datasets/codepawl/scanned-objects-glb · https://huggingface.co/datasets/codepawl/plateau-city-glb
- Not counted: https://huggingface.co/datasets/codepawl/abo-glb (a plain listing page, not an ask) · https://huggingface.co/datasets/codepawl/scanned-objects-glb (a plain listing page, not an ask) · https://huggingface.co/datasets/codepawl/plateau-city-glb (a plain listing page, not an ask)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "glb validator python": ahmedsayed1911/Blender-AI-Agent (8 stars), JonCunninghamDev/low-poly-character-studio (1 stars), SenjuWoo/AssetForge (1 stars)
- Smallest useful version: A small Python script that reads a GLB file's header and JSON chunk and reports pass or fail for the basic structure checks, with a self-test on two sample files.
- Tool: tools/glb-structure-check/ · counted steps 0 of 5
- Old score (report-only, not a gate) 11 of 15, demand 2

## opp-1071-4 · index_build.py that generates an index from a notes folder

Agent notes folders have no lightweight way to be turned into a browsable index, so others cannot find what an agent has already written.

- Status: Dropped since 2026-11-17 (already done elsewhere)
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/open-index/hacker-news
- Not counted: https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "markdown notes index generator": BabyJ723/NXT-LVL (2 stars)
- Smallest useful version: A stdlib-only script that reads a folder of .md notes and writes an index.md with titles and first lines, plus a three-note example.
- Old score (report-only, not a gate) 9 of 15, demand 1

## opp-1071-9 · A small open dataset of trending Hugging Face datasets, each row cited to the page it was read from.

Researchers comparing Hugging Face datasets need a compact, source-cited table of what each trending dataset contains, its license and its size.

- Status: Dropped since 2026-11-17 (already done elsewhere)
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m · https://huggingface.co/datasets/nvidia/simready-assets · https://huggingface.co/datasets/open-index/hacker-news
- Not counted: https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m (a plain listing page, not an ask) · https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask) · https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "hugging face dataset card scraper": nothing found
- Smallest useful version: A table of 10 trending datasets with name, size, license and the URL each row was read from, with unread fields marked not-opened.
- Old score (report-only, not a gate) 11 of 15, demand 2
