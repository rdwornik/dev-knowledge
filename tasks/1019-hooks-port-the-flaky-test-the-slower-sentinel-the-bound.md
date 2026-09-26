---
id: "[#1019]"
title: "hooks-port: the flaky test, the slower sentinel, the bounded_hook gap and the 18 [#802] regressions have no landed digest or row"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1019] [P2][M] **hooks-port: the flaky test, the slower sentinel, the bounded_hook gap and the 18 [#802] regressions have no landed digest or row** - DIGEST-WAVE5B-N1-2026-09-25 lists four unresolved hooks-port findings with no `docs/audits/2026-09-25-codex-lane-hooks-port.md` landed to carry them (confirmed absent): CANDIDATE flaky `tests/test_lane_end_guard.py` detached-worker timing; `billing_leak_sentinel.ps1` running slower post-port; a `bounded_hook.py` POSTURES gap; and the 18 `[#802]` regressions the lane's own review listed. · Done when: each of the four sub-items has either a landed audit under `docs/audits/` naming it or a dedicated row; this row's own check is that at least one of the two exists · refs `tests/test_lane_end_guard.py`, `scripts/bounded_hook.py`, `[#802]`, DIGEST-WAVE5B-N1-2026-09-25 ROWS-OWED (hooks-port) · kill-candidates: none -- no open row or landed audit carries these four findings
