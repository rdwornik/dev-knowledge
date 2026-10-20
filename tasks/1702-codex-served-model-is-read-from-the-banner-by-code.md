---
id: "[#1702]"
title: "The Codex served model is read from the CLI banner by code, not from the model's own MODEL= line"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1702] [P2][S] **The Codex served model is read from the CLI banner by code, not from the model's own MODEL= line** - R172 asks for the banner `model:` line, but a lane reads the model's self-description: the e2-graph-hotspot lane recorded 'served gpt-5' while the banner said `model: gpt-5.6-terra`; `[#1652]` records the symptom as defect N10 and `[#1687]` fixes the claude path only, so no code reads a `codex exec` banner · owner: a review-tooling lane · Done when: (1) RED first: a test feeds a `codex exec` output with a banner `model: gpt-5.6-terra` and an answer footer 'GPT-5 (Codex)' and expects `gpt-5.6-terra`, and one without a banner and expects a refusal, not a guess; (2) a helper returns the banner model and the review step and the handback check use it; (3) real-use witness: a real `codex exec -m gpt-5.6-terra -s read-only` review record carries the helper's value · touches: a helper beside `scripts/run_phase.py`, `tests/` · kill-candidates: `[#1687]` -- served model for the claude path; same field, other CLI · refs `[#1652]`, `[#1687]`, `[#1663]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-e2-graph-hotspot.md` (served gpt-5 vs banner), R162, R172
