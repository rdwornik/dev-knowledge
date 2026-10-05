---
id: "[#1410]"
title: "The dispatcher enforces a lane's same-defect attempt bound in code, not by the lane's reading of its contract"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1410] [P1][M] **The dispatcher enforces a lane's same-defect attempt bound in code, not by the lane's reading of its contract** - Lane W1-12 `b2-codespace-green`'s contract N6 says "The same defect failing 3 runs stops item 6 `WAITING` ... do not run a fourth time on it", and the lane ran 13 attempts (the architect's DECIDED-BY-SEAT A, 2026-10-05 21:34Z: about 10 runs failed on C3 against main's own red/cancelled CI, about 7 past the bound). Nothing outside the lane counted: the bound lived only in prose the lane itself was trusted to obey, and the dispatcher's FATE lines read "working/busy" throughout · Done when: (1) a lane contract can declare a same-defect attempt bound in a machine-read form (default 3), and `plan_lint` refuses a contract whose prose names a bound the form does not carry; (2) the dispatcher (or the lane-end guard it reads) counts attempts per defect signature from the lane's run records and, at the bound, records `WAITING <slug>: attempt bound <n> reached on <defect>` and stops the lane through the line's own stop verb, never by `claude rm`; (3) RED-first tests: a fixture of 4 same-defect failures is stopped at 3 (fails on `9c72c990`), a fixture of 3 failures on 3 different defects is not stopped, and a passing run resets the count · kill-candidates: none -- `dispatch.py` has no attempt count (`git grep -n attempt scripts/dispatch.py` shows only the CI poll loop), and no open row carries one · refs `scripts/dispatch.py`, `scripts/lane_end_guard.py`, `scripts/plan_lint.py`, `templates/lane-contract-template.md` · source: B2-W1 integrator and dispatcher receipts (`to-browser/SESSION-integrator-b2-w1-2026-10-04.md`, `to-browser/SESSION-dispatcher-b2-w1-2026-10-04.md`, DECIDED-BY-SEAT A 21:34Z); `LANE-B2-W1-b2-codespace-green.md` N6; render record `to-browser/SESSION-gen-b2-w1-record-2026-10-04.md` §"AMEND-5"
