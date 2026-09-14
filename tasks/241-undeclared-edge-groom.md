---
id: "[#241]"
title: "Undeclared-edge groom"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: coherence
generates: BACKLOG.md
---

- [#241] [P2][S] Undeclared-edge groom — adjudicate every edge the `undeclared_edges` ship-gate leg (Fable consult #1 ruling #2, ADR-88 FC2) surfaces. **PROSE RE-MEASURED 2026-09-05 (R5/B8): the live set is 22, not the 6 this row described.** The original 6 were BACKLOG / VISION / AI_COUNCIL_PROCESS / ESSENTIALS / PLAYBOOK / SESSION_SETUP → handoff-process, from the leg's first live run on 2026-07-03; VISION and SESSION_SETUP no longer fire at all (VISION relocated to `docs/archive/` by [#614] lane-e-5; SESSION_SETUP declared), so the row was steering by a list two of whose members are gone. Live at `main` @ `ac2c6a15`: **22 edges — 17 tier-1, 5 tier-2; 13 → handoff-process, 9 → prompt-template**, of which 14 are dispositioned in `ecosystem/disposition-register.yaml` and 8 are not. Per "declare reconciled_with only for coupled+current refs": DECLARE the genuinely version-coupled current refs and PERMANENTLY-DEFER the analogy / ticket / pointer refs with a recorded reason; any canonical_freshness-gated declaration must ride a genuine freshness re-stamp. · Done when: every id the `undeclared_edges` ship-gate leg surfaces is either declared (`reconciled_with`) or recorded permanent-defer-with-reason, and each such id's disposition entry retires or is re-annotated — the predicate reads the live surfaced set, never a fixed count · refs scripts/scan_undeclared_edges.py, scripts/audit.py, ecosystem/disposition-register.yaml, #179, #172, ADR-88 · serialize-group: coherence · **Archived annotations:** `tasks/archive/241.md`
