---
id: "[#1646]"
title: "M1 v2: each vendor measured in its role"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1646] [P1][M] **M1 v2: each vendor measured in its role** - M1 v2 measures each vendor in the role R134 gives it (Grok implements, Copilot writes and runs isolated tests, Codex reviews, Gemini through agy reads files, Haiku does read-only fan-out, Sonnet orchestrates, Opus plans and judges) so the role to model-and-effort table is measured, not assumed; Grok has had no real run since its pin · owner: M1 lane (codespace scratch branch, never merged); the operator rules the table. target batch: E2 · Done when: `scratch/m1-model-probe-v2/RESULT.md` holds n = 5 per cell for each vendor in its role, with Sonnet and Opus as reference, each cell carrying the served model id, USD, tokens, wall time and a blind grade, plus a PROPOSED role table; real-use witness: the pre-launch tier refusal (`[#1630]`) reads the table's values and refuses a contract that names a model outside its role · touches: see the body · kill-candidates: `[#1628]` -- M1 v1 (Haiku and Sonnet cells): decide whether v2 supersedes it · refs `[#1628]`, `[#1630]`, `[#1631]`, `to-browser/RATIFICATION-2026-10-18.md` R134 · decided-by: R134 (E1 lane e1-rows). Defect H28: R153 is not taught (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect C15: the Grok served model is absent from its receipt (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
