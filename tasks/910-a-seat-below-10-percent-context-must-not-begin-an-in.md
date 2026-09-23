---
id: "[#910]"
title: "A seat below ~10% context must not begin an integration walk -- retire and boot fresh"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "AMEND-BUILD-MODE-B2-INTEGRATION-2026-09-18"
generates: BACKLOG.md
---

- [#910] [P1][S] **A seat below ~10% context must not begin an integration walk -- retire and boot fresh** - a compaction in the middle of a multi-step merge loses the walk's state: which branches are merged, which JOURNAL letter comes next, which teardown is pending. In B2 the previous integrator seat was retired at 3% remaining context and a fresh seat did the integration. That was the right move, but only the operator's judgment made it; there is no floor. The rule: a seat with less than ~10% context remaining does not begin an integration walk or any other multi-step merge. It writes its state to `to-browser/SESSION-<seat>.md` and retires, and a fresh seat boots from that file · Done when: the integrator seat boot (`gen_seat_boot.py` output) and `/lane-integrate` refuse to open the merge queue below the floor, reading the remaining-context figure mechanically rather than from the seat's self-report; a seat that crosses the floor mid-walk stops at the next merge boundary and writes its state file; and the floor value and where it is read are stated once, in PLAYBOOK Ch8 · implements: AMEND-BUILD-MODE-B2-INTEGRATION-2026-09-18 · refs `protocols/PLAYBOOK.md` Ch8 (integrator refuse-to-finish), `scripts/gen_seat_boot.py`, `.claude/commands/lane-integrate.md` · kill-candidates: none -- no open row sets a context floor on a seat
