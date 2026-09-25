---
id: "[#1018]"
title: "launcher-fixes: Copilot usage governance has no reader for --usage-output-file / --output-format json"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1018] [P2][M] **launcher-fixes: Copilot usage governance has no reader for --usage-output-file / --output-format json** - `scripts/dispatch.py:1437` names the gap directly: "no reader for the CLI's own usage surface (--usage-output-file / --output-format json)" -- Codex HIGH-2 on the launcher-fixes lane, carried as owed in DIGEST-WAVE5B-N1-2026-09-25. · Done when: a reader parses Copilot's `--usage-output-file` JSON (or `--output-format json`) into `TokenUsage`/`ModelCost` the way `scripts/lane_cost.py` already does for Claude transcripts, RED-first witnessed on a fixture · refs `scripts/dispatch.py:1437`, `scripts/lane_cost.py`, `scripts/provider_bench.py` · kill-candidates: none -- no open row builds this reader
