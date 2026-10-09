# Codex Review — b2w2-rulings-landing

**Date:** 2026-10-10
**Branch:** `worktree-b2w2-rulings-landing`
**HEAD:** `e035d77f`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0

**Model used:** `gpt-6-astra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#1446] (lane b2w2-rulings-landing, contract LANE-1446-b2w2-rulings-landing.md; STANDING_RULINGS section AS)

---

## Focus

Contract: LANE-1446-b2w2-rulings-landing.md (frozen Done-contract items 1-4; batch B2-W2 lane 6, row [#1446]). BEGIN YOUR ANSWER WITH THE LINE 'NONCE: b529c85ed5ed'. This diff lands STANDING_RULINGS section AS (R80-R92) plus rows tasks/1450-1456 and tests; the code-profile file list omits the prose, so ALSO review protocols/STANDING_RULINGS.md section AS, tasks/1450-*.md to tasks/1456-*.md and tasks/1420-*.md. Attack my dispositions: (1) does each Carried-by row really carry its ruling by scripts/decision_coverage.py rules (names the ruling, Done-when, owner:) and is each row's Done-when measurable and its cited evidence true; (2) is R92's 'no implementation required' honest; (3) do the new tests in tests/test_standing_rulings_sources.py bite (RED before, GREEN after) or pass vacuously; (4) anything in the diff outside the lane's declared scope.

---

## Findings
NONCE: b529c85ed5ed

## Critical

(none)

## High

### protocols/STANDING_RULINGS.md:6056 — New carriers break a required existing test

**What:** Section AS introduces carrier IDs outside the allowance in `tests/test_decision_coverage.py:1418`, whose selector includes every ruling ≥ R55.
**Why:** `test_the_live_rows_this_lane_filed_sit_in_its_id_block` necessarily fails, leaving Done-contract item 4 unsatisfied.
**Fix direction:** Coordinate with that test’s owner to scope its historical allocation check to R55–R79 and retain separate coverage for AS.

### tasks/1451-ci-runs-pytest-split-a-coverage-gate-and-the-mutation-pilot-nightly-r81-r86.md:12 — Nightly acceptance test permits a skipped pilot

**What:** Done-when (3) checks only trigger presence; the existing pilot condition accepts manual dispatch or changed pilot files.
**Why:** Scheduled events have no push `before`, so the filter returns false and skips mutation testing—even while the proposed acceptance test passes.
**Fix direction:** Require evidence that a scheduled event actually selects and executes the mutation pilot, including its job condition and dependencies.

## Medium

(none)

## Low

(none)

All 14 verbatim blocks match their sources; R92’s disposition is supported. No out-of-scope diff found. Tests were not executed: `uv` required a temporary-file write blocked by the read-only sandbox.

---

## Record (b2w2-rulings-landing, 2026-10-10)

- **Served model:** `gpt-6-astra`, provider `openai`, codex-cli 0.155.0, session `01a122d3-cb11-7cd3-a421-0d2a4969991f` -- read from the tool's own run header (`model: gpt-6-astra`), not from this file's pin line.
- **Nonce:** the focus asked for `b529c85ed5ed`; the answer opens with `NONCE: b529c85ed5ed`.
- **First attempt** (session `01a122cd-53b4-7d91-bfd1-2522d7428105`, same model) ended at the usage limit ("try again at 12:38 AM"); the retry ran after 12:38, the first of the two retries R59 allows. No substitution: `grok` was not used.
- **Contract cited:** `LANE-1446-b2w2-rulings-landing.md`, Done-contract items 1-4; consumer row [#1446].
- **Tally 0/2/0/0**, counted against the Findings above.

### Dispositions

- **High 1 (the id-block test).** Confirmed, and found before the review by the lane's close-out run: `tests/test_decision_coverage.py::test_the_live_rows_this_lane_filed_sit_in_its_id_block` selects every register entry from R55 on, so section AS's carriers (1435-1437, 1439, 1450-1456) fall outside its 1360-1399 allowance. The one-line fix (`55 <= e.number <= 79`, matching its docstring) was made on the branch, GREEN, and then reverted at the integrator's instruction because the contract bars the lane from that file (commits 3e341c8d, e035d77f). Open as `OPERATOR-ACTION: seat ownership extension for tests/test_decision_coverage.py (one line, the id bound)`; the lane's Done-contract item 4 reads WAITING seat-ruling on it, not met.
- **High 2 ([#1451] Done-when 3).** Accepted and fixed: the item now requires a scheduled event to select and run the pilot (the `changes` job answers false when there is no push range, `.github/workflows/report-only-wall.yml:54-63`), with the trigger, the pilot's `if` and its `needs:` checked together by one test.
- The reviewer ran no tests (its sandbox could not write the `uv` temp files); the lane's own runs are in its session file.