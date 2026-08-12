---
id: "[#359]"
title: "PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist."
status: open
priority: P1
size: M
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: handoff
generates: BACKLOG.md
---

- [#359] [P1][M] **PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist.** The FILE-BOUNDARY rule asserts the parallelism ruling was "made mechanical"; nothing implements it. `scripts/boundary_report.py` is a keyword false-friend — the #312 fleet CLAUDE.md region reporter, self-declared "a reporter, NOT a gate ... deliberately NOT registered in `audit.ALL_CHECKS`". **Record the category explicitly:** phantom enforcement is worse than a silent rule, because it actively misleads a reader into believing a guard exists, and the four-state ledger has **no cell for it** — a rule claiming a mechanism it lacks is neither `silent` nor `declared`. Routes to W6. · **RE-PEGGED 2026-08-12** (operator adjudication; register `protocols/STANDING_RULINGS.md` M-7 / `N2-R1-03`): this row cited `:517-518`, correct when the spec was shorter — that range now holds unrelated FILL-IN-region text. The live claim (*"the parallelism ruling made mechanical"*) sits at **`:775-776`**, under `### §14a — EPIC handoff (architect → epic chat)` item 4 **FILE-BOUNDARY**, and is **restated at `:938-939`** under `## Section history` — a second site this row did not name. Anchored to the heading text per the 3b-4 citation convention, with the line numbers recorded as the 2026-08-12 measurement rather than as the anchor, so a further shift in a spec that advanced 6.1.0 → 6.2.0 underneath this row cannot re-orphan it again. · Done when: the false claim is corrected or the mechanism built, AND the ledger model carries an explicit disposition for the phantom-enforcement class · refs protocols/HANDOFF_PROCESS.md, scripts/boundary_report.py, [E8] baseline · kill-candidates: none — a failure class the four-state model cannot express · serialize-group: handoff
