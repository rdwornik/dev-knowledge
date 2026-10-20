---
id: "[#1670]"
title: "No silent substitution: the launcher and contract lint refuse a model not in the phase or role table (R139, P1)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1670] [P1][M] **No silent substitution: the launcher and contract lint refuse a model not in the phase or role table (R139, P1)** - R139: a model or account that is not in the table is never substituted silently; the work belongs to lane e2-subst-gate of batch E2.0 · owner: E2 lane. target batch: E2.0 · Done when: (1) the launcher and the contract lint refuse a model absent from the phase table or the role table; (2) RED first: a test launches with an unlisted model and fails today; real-use witness: a real launch naming an unlisted model is refused with the table row it lacks · touches: launcher and contract lint in `scripts/`, `ecosystem/provider-registry.yaml` · kill-candidates: `[#898]` -- the dispatcher-shape defect where a local substitute committed what the contract forbade · refs `protocols/STANDING_RULINGS.md`, `to-browser/RATIFICATION-2026-10-18.md` R139 · decided-by: R139. Defect N8: three tests broke on the empty-batch refusal (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect H23: a model substitution is silent in the launcher while the rulings say 'record it' (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
