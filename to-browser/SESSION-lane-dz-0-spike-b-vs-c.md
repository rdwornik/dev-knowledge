# SESSION lane-dz-0-spike-b-vs-c

Served model: claude-sonnet-5-5 (every step; no routed tool, so no SUBSTITUTION). Substrate: codespace box, scratch branch `worktree-lane-dz-0-spike-b-vs-c`, never merged.

## What is now true that was not

- `scratch/b-vs-c-spike/RESULT.md` grades form B (python-statemachine) against form C (BPMN on SpiffWorkflow) on P1 dispatch, with a recommendation: **B**, plus the evidence rows and what would change it. Read it first.
- Both prototypes run in dry-run against the real verbs and end in the same terminal node in all 10 scenarios; in the 5 scenarios the real `launch_lane` can answer (spawn seam faked) they agree with it, exit codes 0/5/5/5/8.
  - `/tmp/spike/venv-python_statemachine/bin/python -W ignore scratch/b-vs-c-spike/b_statemachine/run_scenarios.py`
  - `/tmp/spike/venv-spiffworkflow/bin/python scratch/b-vs-c-spike/c_bpmn/run_scenarios.py`
  - (the venvs are in the box's /tmp; rebuild: `uv venv`, `uv pip install python-statemachine pydot pytest` / `spiffworkflow pytest`)
- Diagrams: `b_statemachine/out/p1_dispatch_b.{png,svg,dot,mmd}`, `c_bpmn/out/p1_dispatch_c.{png,svg,dot}`; traces `*/out/traces.md`.
- 19 tests per form pass (0.09 s B, 0.23 s C): `pytest -c /dev/null --rootdir=/tmp -p no:cacheprovider scratch/b-vs-c-spike/<form>/test_*.py`.

## Value, in one sentence

The operator now has a graded B-vs-C comparison on one real process, resting on measurements, and the finding that C bought no behaviour B lacked at +14 nodes, a compiled dependency, an LGPL licence and a custom renderer.

## Self-check

- Targeted tests: 19 passed (B), 19 passed (C). Hub suite NOT run: the diff outside `scratch/` is none of mine (see purity).
- `ruff` ran in pre-commit on every commit and passed.
- `audit.py health`: DEGRADED, warnings only (canonical_freshness, journal_day_letters, consumer_at_landing, model_currency), none touches `scratch/`; no FAIL line. `audit.py ship-gate` and `tests/test_silent_rule_ratchet.py` NOT run: this branch is never merged. Codex review NOT run: scratch code, no row closed.
- Purity: `git log origin/main..HEAD` lists the D0 base commit `d8aa4dd7` (the parity pin the dispatch put under this branch; not mine) and my 7 commits before this file; every file I touched is under `scratch/b-vs-c-spike/` except this session file.
- Vacuity: a refused contract (S2) and a spawn failure (S7) each end in `end_refused`, and a clean one in `end_launched`, so the matrices are not vacuous; the oracle disagrees if a model is wrong (it did not).

## DECIDED-BY-LANE

- DECIDED-BY-LANE: claim step 0 -> proceeded without a claim marker (`claim.py` exited 2, "CLAUDE_PROMPTS_DIR is not set": the codespace has no transport; exit 3 is the refusal, this was not it). Nothing else could hold the contract in this box.
- DECIDED-BY-LANE: ADR-101 hermetization hook refused the contract's own path `scratch/` (unsanctioned top-level directory) -> committed with `SKIP=validate-hermetization`, one named hook, declared in every commit body (the branch is never merged, so main's Tier-1 set is untouched; no ADR-101 amendment sought).
- DECIDED-BY-LANE: the 3 required scenarios plus 5 more (dependency hold, codespace route, spawn fails, job unresolved) and 2 model-only ones (reaped, END-EARLY) -> the extra ones exercise the error-boundary path the contract asks for and the two holes.
- DECIDED-BY-LANE: pure functions with no CLI dry-run (`decide_lane`, `_held_by`, `launch_lane`...) were called in-process through `common/probe.py` with the spawn seam faked and a throwaway receipts dir -> no process was started; this goes one step past "plan / --dry-run / --help" only in that a library function runs, never `claude`, `codex` or `gh`.
- DECIDED-BY-LANE: substrate gateway placed before cap/RAM, as `decide_lane` does, against the contract's order (the contract's order would apply the local cap to a codespace lane); every other divergence is kept in contract order and listed in RESULT section 6.
- DECIDED-BY-LANE: actor/zone/TODAY-GLUE values are my assignment (RESULT section 7) -> they test the colouring mechanism, not the operator's intent.
- DECIDED-BY-LANE: `apt-get install graphviz` in the box (sudo was available) because neither form can render without `dot` -> recorded as a system dependency in RESULT.

## OPERATOR-ACTION

- OPERATOR-ACTION: ratify or reject B in an ADR (this lane only proposes); and, if bpmn.io editing matters, have someone open `c_bpmn/p1_dispatch.bpmn` in bpmn.io, which this lane could not test.

## Unresolved

- bpmn.io rendering of the BPMN file (UNVERIFIED); `transitions` beyond a toy (UNVERIFIED); `[#1572]` behaviour by execution (UNVERIFIED).

HANDBACK worktree-lane-dz-0-spike-b-vs-c @ 85bf002e docs
