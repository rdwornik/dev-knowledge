---
id: "[#1033]"
title: "export_backlog_view.py / offload_admission.py retirement claims collide with [#563] -- needs an explicit operator GO"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1033] [P2][S] **export_backlog_view.py / offload_admission.py retirement claims collide with [#563] -- needs an explicit operator GO** - SESSION-lane-precut-landing rows-owed item 8: a prior lane's retirement claim for these two modules conflicts with the ruling recorded at `[#563]`; neither side has been reconciled, and this is a functional call (ADR-108 §A), not a technical one this lane can make. · Done when: the operator's GO (retire, keep, or reconcile the `[#563]` conflict) is recorded, and the row that acts on it is filed or the modules are confirmed kept · refs `[#563]`, `scripts/export_backlog_view.py`, `scripts/offload_admission.py` · kill-candidates: none -- no open row records this collision
