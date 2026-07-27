---
id: "[#362]"
title: "#242 carries a SUBSTANTIVE guard loss, not status hygiene"
status: open
priority: P2
size: M
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#362] [P2][M] **#242 carries a SUBSTANTIVE guard loss, not status hygiene** (bound to [#242]) — the census extracted 73 MUST-rules from the seven handoff-cluster ADRs (32/37/42/55/56/57/58) and found the supersession vector is **v4, NOT v5**: no document supersedes any of the seven, v5 never cites them (grep returns zero), and **ADR-32 positively asserts "Superseded by: none"**. **49 rules were dropped in the v4→v5 transition with no successor.** Named risk set: ADR-56:49-50 dual-maintenance anti-drift · ADR-55:50-52 operator audit trace (v5 has no anti-rubber-stamp record) · ADR-57:36-37 `mixed-uncertain` fail-safe (v5 defaults to `execution`, inverting the safety direction) · ADR-58:47 confident-claim trigger · ADR-57:67-68/:81-82 no-free-form guards. A status-only retirement silently discards these. · Done when: each dropped rule is carried, consciously dropped with a reason, or superseded — before any status-flip closes #242 · refs #242, ADR-94 · kill-candidates: none — #242 is the status half; this is the substantive half · serialize-group: audit-py
