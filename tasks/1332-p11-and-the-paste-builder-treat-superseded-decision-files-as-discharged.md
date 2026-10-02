---
id: "[#1332]"
title: "P11 and the paste builder treat superseded decision files as discharged"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1332] [P2][M] **P11 and the paste builder treat superseded decision files as discharged** - A `-superseded` version of a transport decision file is not an open decision, but P11 counts its `carried-by: OPEN` as owed carriage and `assemble_paste.shed_residual` inlines it in the paste's OPEN list. At the 2026-10-02 cut, 43 of 127 OPEN carriers were superseded versions and cost 2,728 B; that pushed the paste to 22,610 B against `PASTE_BYTE_CEILING` (20,000). The cut was unblocked by hand (R53 (1), option (c)): the 43 files were moved to `to-cc/archive/` on the transport, which `decision_files` does not scan. Without a code fix the same growth recurs every window. Option (a′) of R53 · Done when: `gen_handoff.carriage_verdicts` classifies a `DECLARE-`/`AMEND-`/`BATCH-` file whose name marks it superseded as discharged by its successor, without a hand move, and `assemble_paste.open_list` omits it; a RED-first test pins both on a fixture with a superseded version beside its successor · touches: `scripts/gen_handoff.py`, `scripts/assemble_paste.py`, tests · kill-candidates: none -- no open row tracked superseded carriage before this entry · refs ADR-129, scripts/gen_handoff.py, scripts/assemble_paste.py · source: R53 (1) at the 2026-10-02 architect handoff cut, `docs/handoffs/2026-10-02-dev-knowledge-architect/RESIDUAL.md`
