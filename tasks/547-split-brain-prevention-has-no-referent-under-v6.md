---
id: "[#547]"
title: "Split-brain prevention is instructed against a handoff section shape v6 does not produce"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: playbook
generates: BACKLOG.md
---

- [#547] [P3][S] **Split-brain prevention is instructed against a handoff section shape v6 does not produce** — `protocols/PLAYBOOK.md` §"Split-brain prevention" tells the incoming browser seat to *"read handoff Current + Future State"* and to *"validate Future State items against BACKLOG.md (drift check per ADR-37)"*, citing ADR-37 §8 as the authority. **The live spec has no such sections:** `protocols/HANDOFF_PROCESS.md` is v6.2.0 and a case-insensitive count of `current state|future state` over it returns **0** (`protocols/ESSENTIALS.md` likewise 0, measured 2026-08-17); the v6 boot artifacts are `HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md`, and `scripts/gen_handoff.py` renders only from `templates/handoff/v5/`. So the one mechanism that stops a handoff duplicating the task queue is an instruction with **no referent** — a seat following it looks for a section that cannot exist, and the drift check silently never runs. **This is NOT [#362]'s defect**, which enumerates 49 MUST-rules DROPPED at the v4→v5 transition with no successor: this rule was *retained* on a live surface while the artifact it points at was removed, so [#362]'s Done-when ("carried into a live surface") reads as already satisfied for it — the inverse case, and invisible to that row. Nor is it [#242]'s ADR status hygiene. · Done when: the split-brain drift check either names v6 artifacts and sections that actually exist, or is recorded as retired with its successor mechanism named (the v6 P-probes are the candidate) — and no live surface instructs reading a handoff section absent from `HANDOFF_PROCESS.md` · refs protocols/PLAYBOOK.md ("Split-brain prevention"), protocols/HANDOFF_PROCESS.md, docs/decisions/ADR-37-session-boundary-protocol.md, docs/decisions/ADR-82-handoff-process-v5-model-c.md, #362, #242 · kill-candidates: none — [#362] owns the rules dropped at v4→v5 and [#242] owns ADR status hygiene; neither covers a retained instruction whose referent was deleted · serialize-group: playbook · source: docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md step 1 (ADR currency sweep)
