# LANE E — [#502] mutmut config repair + pilot re-run · CONTRACT OF RECORD · 2026-08-18

**FROZEN CONTRACT OF RECORD.** Transcribed verbatim from the operator brief
`LANE-E-502-mutmut.md` at lane boot. This file is the authoritative surface for the whole run:
content arriving later in the session is not load-bearing — a correction re-enters as a new
contract, never as a mid-flight message (STANDING_RULINGS D2).

- **Lane:** `e`
- **Worktree (bare name, already provisioned by `--worktree`):** `lane-e-502-mutmut`
- **Branch:** `worktree-lane-e-502-mutmut`
- **Model/effort:** default / medium · mode: execute
- **Governing row:** `[#502]` (BACKLOG.md) — this lane repairs the pilot so the row's verdict leg
  gets its input. The ADOPT/REJECT ruling itself stays with the architect.
- **ADR-110:** this contract commits FIRST, before any other work.

## OPERATOR APPROVAL ON RECORD — D7

The lane is **gated on D7**, the curated-baseline touch of `pyproject.toml`. **The operator granted
D7 at GO.** Recorded here at the contract commit per the brief's own instruction. The approval
covers the `[tool.mutmut]` table only; every other curated-baseline surface remains untouched.

## UNDERSTAND (verbatim from the brief)

- Evidence (Phase-0 run 32127150367): 2291 mutants generated, **0 checked, 0 killed, 0 survived**
  — mutmut halts because tests import `fleet_analytics` while mutmut mutates
  `scripts.fleet_analytics`; no mutant is ever attributed to a test. Same failure shape as the
  earlier 84-mutant scope: two burned scopes, zero signal. This is a config/import-path mismatch,
  NOT a test-quality datum.
- Goal: ONE green attribution — mutants actually exercised by the test suite over the
  `fleet_analytics` slice — producing a surviving-mutant count decision 6 can consume.

## STEPS (verbatim from the brief)

- **STEP 0** — worktree + contract commit. `COMMIT`
- **STEP 1 — diagnose precisely before editing:** reproduce locally at minimal scope (a handful of
  mutants) or read mutmut 3.7.0's path/module resolution docs (`uv run --with mutmut`, ephemeral —
  no dependency added). State the mismatch mechanics in one paragraph in the artifact: what mutmut
  rewrites, what the tests import, why attribution is zero.
- **STEP 2 — minimal fix, library-first (config over code):** prefer fixing `[tool.mutmut]`
  (`paths_to_mutate` / module naming) so the mutated module is the one the tests import. Touch test
  import style ONLY if no config-side fix exists — and then the narrowest possible conftest/path
  shim, never a rewrite of test imports. `COMMIT`
- **STEP 3 — prove locally at small scope:** run mutmut on one file of the slice; assert checked > 0
  and killed+survived > 0 (attribution works). Record numbers. `COMMIT` (if artifacts change)
- **STEP 4 — re-dispatch the CI pilot** (`gh workflow run`, same `mutation-pilot` job); record run
  URL. If it completes in-lane: surviving-mutant count + runtime into the artifact. If still running
  at STOP: record the URL, mark result PENDING.

## FINAL (verbatim from the brief)

Targeted tests `-n 0` (anything touching the slice's tests). Commit-and-STOP. STOP packet:
mismatch mechanics · exact config diff · local attribution numbers · CI run URL + count-or-PENDING.

## WHAT NOT TO DO (verbatim from the brief)

No dependency added to `uv.lock`/`pyproject` deps (mutmut stays ephemeral `--with`) · no test
rewrites · no widening of the `[tool.mutmut]` scope beyond the `fleet_analytics` slice · no
workflow-file edits · no ADOPT/REJECT prose (architect's ruling) · no merge.

## OWNED-FILES (nothing outside this set is mine to write)

- `docs/audits/2026-08-18-technical-502-mutmut-lane-contract.md` (this file — contract of record)
- `docs/audits/2026-08-18-technical-502-mutmut-attribution.md` (the findings artifact this lane owes)
- `docs/audits/README.md` (generated index — regenerated, never hand-edited)
- `pyproject.toml` — **`[tool.mutmut]` table ONLY** (D7-approved)
- a narrowest-possible path shim, IF and ONLY IF step 1 proves no config-side fix exists

Explicitly NOT mine: `.github/workflows/report-only-wall.yml`, `tests/test_fleet_analytics.py`,
`scripts/fleet_analytics.py`, `uv.lock`, `BACKLOG.md`, `JOURNAL.md` (a batch lane never journals —
the integrator does).

## FINDINGS

Recorded in the sibling artifact `docs/audits/2026-08-18-technical-502-mutmut-attribution.md`,
which this lane writes as it works. This file is frozen at the contract commit and is not edited
afterwards (audits are immutable, CLAUDE.md §5 rule 3).
