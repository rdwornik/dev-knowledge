---
id: "[#1743]"
title: "check_routine_uv_pin unwired, fate 11-09"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1743] [P2][S] **check_routine_uv_pin unwired, fate 11-09** - `check_routine_uv_pin` is built and not wired into the audit registry; fate 2026-11-09 WIRE or REMOVE (R121) -- UV-1 landed `check_routine_uv_pin` in `scripts/audit_checks/check_routine_consumers.py` with `tests/test_routine_uv_pin.py`, but it is not in `scripts/audit_checks/registry.py`, so no audit runs it (refuted premise Q10, R121 "will something USE it"); ruling D accepted it unwired and asked for this row. R-1724 (RATIFICATION-2026-10-26.md Addendum 3): the claude.ai scheduled task is outside the repo (owner TA-47 with the operator, not a CC action) and under the membership rule (C1) it is unbound -- the routine definition moves into the repo and is bound in process-binding.yaml, or the scheduled task is removed -- fate 2026-11-09; `[#1724]` closes when TA-47 reports the task changed. R-UVTAIL (same addendum): the lane routine-uv-pin-tail is abandoned and tagged `archive/routine-uv-pin-tail-2026-10-26` (f2304a3d1); its n/a-not-FAIL fix for a repo with no routine bootstrap and no uv pin is NOT landed. Its own id, not folded into `[#1742]` · owner: integrator-e2-1 (`scripts/audit_checks/registry.py`) · Done when: by 2026-11-09 either (a) WIRE: `check_routine_uv_pin` is registered in `registry.py`, `audit.py checks` lists it, and `tests/test_routine_uv_pin.py` plus the registry tests pass, or (b) REMOVE: the check and its test are deleted with the ruling cited; the choice is recorded in the 11-09 window digest (R121) · touches: `scripts/audit_checks/registry.py`, `scripts/audit_checks/check_routine_consumers.py`, `tests/test_routine_uv_pin.py` · refs `[#1724]` · decided-by: the operator, 2026-10-26, RATIFICATION-2026-10-26.md rulings D and D-ID, S-FATE; Addendum 3 R-1724 and R-UVTAIL · source: `to-browser/SESSION-integrator-e2-1-2026-10-23.md` ORCH-MSG 02:4x; fate 2026-11-09 · filed by the integrator from the operator grant 1737-1743 (RATIFICATION-2026-10-26.md ruling B + D-ID; S-ID: no id beyond it)
