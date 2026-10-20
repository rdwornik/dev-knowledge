---
id: "[#1714]"
title: "`Step.stop` counts a continue_on_failure organ's failure as a loop stop, masking the behaviour the harness declares"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1714] [P2][S] **`Step.stop` counts a continue_on_failure organ's failure as a loop stop, masking the behaviour the harness declares** - `Step.stop` in `tests/test_connection_loop.py:155` ignores `continue_on_failure`, so the `ci_red_age` repin of `EXPECTED_STOPS` (line 111) hides that the toy walk should continue past it (RULING e2-fates-repair-1; Codex HIGH on the repin) · owner: connection-loop test lane · target batch: E2 · Done when: (1) RED first: a walk with a `continue_on_failure` organ that fails is shown not to stop; (2) `Step.stop` honours the flag and `EXPECTED_STOPS` is re-pinned without `ci_red_age`; (3) real-use witness: `uv run --locked pytest tests/test_connection_loop.py` green on the real `ecosystem/harness.yaml` · touches: `tests/test_connection_loop.py` · kill-candidates: none -- no open row covers it · decided-by: R149 (operator, 2026-10-19); OWED-ROWS (1) in `to-browser/SESSION-integrator-e2-0-2026-10-18.md` · source: `to-browser/REFUSED-e2-fates.md`
