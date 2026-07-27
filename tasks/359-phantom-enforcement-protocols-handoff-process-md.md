---
id: "[#359]"
title: "PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a mechanism that does not exist."
status: open
priority: P1
size: M
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: handoff
source: BACKLOG.md
derived: true
---

- [#359] [P1][M] **PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a mechanism that does not exist.** The FILE-BOUNDARY rule asserts the parallelism ruling was "made mechanical"; nothing implements it. `scripts/boundary_report.py` is a keyword false-friend — the #312 fleet CLAUDE.md region reporter, self-declared "a reporter, NOT a gate ... deliberately NOT registered in `audit.ALL_CHECKS`". **Record the category explicitly:** phantom enforcement is worse than a silent rule, because it actively misleads a reader into believing a guard exists, and the four-state ledger has **no cell for it** — a rule claiming a mechanism it lacks is neither `silent` nor `declared`. Routes to W6. · Done when: the false claim is corrected or the mechanism built, AND the ledger model carries an explicit disposition for the phantom-enforcement class · refs protocols/HANDOFF_PROCESS.md, scripts/boundary_report.py, [E8] baseline · kill-candidates: none — a failure class the four-state model cannot express · serialize-group: handoff
