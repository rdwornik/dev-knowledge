---
id: "[#1737]"
title: "Dispatcher template 2 h vs yaml 3 h"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1737] [P2][S] **Dispatcher template 2 h vs yaml 3 h** - The dispatcher cycle instruction says about every 2 h while the dispatcher stop leg uses the 3 h threshold; align the template to `ecosystem/seat-cycle.yaml` -- `templates/dispatcher-order-template.md` tells a dispatcher to hand over "about every 2 h" while `scripts/seat_cycle.py:436` (`_STOP_ROLES`: dispatcher maps to the orchestrator row) judges it against the `ecosystem/seat-cycle.yaml` 3 h `max_age_hours`; a dispatcher that hands over at 2 h never sees `CROSSED` (sol HIGH :436 on SH1-X, ruled a row, `RATIFICATION-2026-10-25.md` SH1-X) · owner: integrator-e2-1 (template + yaml) · Done when: (1) RED first: a test fails while the dispatcher template's cycle cadence disagrees with `threshold.orchestrator.max_age_hours` in `ecosystem/seat-cycle.yaml`; (2) the template states the cadence from that yaml (3 h) and does not retype a different number; (3) `uv run --locked pytest -n0` on the new test and `tests/test_seat_cycle.py` passes · touches: `templates/dispatcher-order-template.md`, `ecosystem/seat-cycle.yaml`, `tests/test_seat_cycle.py` · refs `[#1636]`, `[#1700]`, `[#1727]` · decided-by: the operator, 2026-10-25, RATIFICATION-2026-10-25 SH1-X ("Finding :436 -> H1-X row: align the template to ecosystem/seat-cycle.yaml (3 h)") · source: `to-browser/SESSION-stop-hook-cycle-check-repair-2.md:63` · filed by the integrator from the operator grant 1737-1743 (RATIFICATION-2026-10-26.md ruling B + D-ID; S-ID: no id beyond it)
