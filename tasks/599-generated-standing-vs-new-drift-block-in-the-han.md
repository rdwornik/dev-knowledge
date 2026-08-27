---
id: "[#599]"
title: "Generated standing-vs-NEW drift block in the handoff residual"
status: open
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#599] [P2][M] **Generated standing-vs-NEW drift block in the handoff residual** — the standing-WARN attribution is hand-authored in every bundle that carries a driftflags region, and the census ranks it the **largest single mechanizable class** in the corpus. It needs no judgment to compute: the discriminator is already written down — *attribute a WARN by asking whether the arc's diff touched the file it fires against, not by counting* — and its three inputs (the live WARN set, `ecosystem/disposition-register.yaml`, the window diff) are all machine-readable. **The constraint is the point:** the generated block carries three lists — dispositioned-by-register / dispositioned-by-absence-from-the-diff / NEW-and-un-dispositioned — and **no verdict, no count, no sha**, because a generated block carrying one would move a VALUE into the bundle, which is the single thing every census delta refuses to do. The hand region then narrows to the one question a list cannot answer: which NEW flag is a decision rather than a defect. Census delta D3; the anti-bluff contract is untouched. · Done when: `gen_handoff.py` renders the three-list block above the driftflags FILL-IN with no verdict, count or sha in it, the FILL-IN prompt is narrowed to decision-vs-defect, and `validate_residual_completeness` plus `verify_handoff_probes` are green on a fresh cut · refs docs/audits/2026-08-26-technical-handoff-census.md (b1 and delta D3), docs/intake/2026-08-26-tech-handoff-mechanization.md (intake #55), scripts/gen_handoff.py, ecosystem/disposition-register.yaml · source: intake #55, census row R2 · kill-candidates: none — no open row owns standing-WARN attribution inside the bundle; `[#404]` scopes the execution-mode supplement leak in the generator and would drop a different defect if killed · serialize-group: handoff
