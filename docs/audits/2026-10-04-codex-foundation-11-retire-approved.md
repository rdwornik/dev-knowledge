# Codex Review — foundation-11-retire-approved

**Date:** 2026-10-04
**Branch:** `worktree-foundation-11-retire-approved`
**HEAD at review time:** `d6d1f7f5` (base `origin/main` `31c791ae`)
**Diff range:** `origin/main...d6d1f7f5` (56,392 B patch, `diff.patch` in the review folder)
**Mode:** diff-review, isolated read-only folder under the job tmp holding only `diff.patch`, `changed/` (post-change copies of the changed files that still exist), `CONTRACT.md` and `nonce.txt`
**Tally:** P1=0 P2=1 P3=0
**Consumer:** `LANE-FOUNDATION-foundation-11-retire-approved.md` (Done-contract item 5, "the review record route above: Codex terra first")

**Route:** Codex terra, first choice (no limit message; Codex answered). No `SUBSTITUTION`.

## Proof of read (R59 §0a item 1)

- **Served model id, from the tool's own run header** (`codex.err` of the run): `model: gpt-5.6-terra`, `provider: openai`, `sandbox: read-only`, `reasoning effort: low`, `OpenAI Codex v0.155.0`, `session id: 01a10413-6371-7e00-b57e-49b9fefa4cdb`.
- **Nonce:** `nonce.txt` held `3cd1cf8679594c6ba31436746b9a3b17`; the reviewer's first line was `NONCE: 3cd1cf8679594c6ba31436746b9a3b17` — matches.
- **Verdict:** as returned, verbatim below.

## What the reviewer was asked

Check (a) only the contract's seven files are deleted; (b) no forbidden path edited; (c) the ADR-116 edit is the status line only and the README edit the ADR-116 index entry only, wording per N3; (d) no surviving template or `/handoff` line names a deleted file and no new must/shall/never; (e) the new tests are real outcome tests; (f) the ledger agrees with the diff.

## Reviewer output (verbatim)

```
NONCE: 3cd1cf8679594c6ba31436746b9a3b17

## P2 tests/test_validate_adr_status.py:1612 — cited-ADR guard silently skips

**What:** The test passes when no open citing rows are found.
**Why:** It would not detect removal/mis-discovery of the required ADR-117/118 citations.
**Fix direction:** Assert the expected citing rows exist before asserting their status.

VERDICT: FAIL
TALLY: P1=0 P2=1 P3=0
```

The reviewer reported no P1 and no finding against (a)–(d), (f).

## Disposition

The tool's verdict line reads `FAIL` on a tally of P1=0, P2=1; it is recorded as returned, not rewritten. The contract's rule is "its P1s fixed", and there is no P1.

- **P2 — the cited-ADR guard skips when no row cites the ADR.** Half accepted, half declined, recorded as `DECIDED-BY-LANE`:
  - **Fixed (commit `555f98cd`):** the part about a blind scan. `test_r66_open_row_discovery_is_not_vacuous` now asserts the open-row scan sees open rows and finds at least one row citing ADR-120, so an empty scan cannot read as "no row cites ADR-116" or "no rows to check".
  - **Declined:** asserting that ADR-117 and ADR-118 *have* citing rows. Today they do (642, 650; 640, 664, 674, 755, 839, 963), but when those rows close the assertion would fail with no defect behind it — a date-driven red the repository already records as a trap. The test's job is the other direction: an ADR an open row cites is never withdrawn. The current citing rows are in the ledger of `2026-10-04-technical-foundation-11-retire-approved.md` instead.

## Re-run after the fix

The fix is a test-only addition; `tests/test_validate_adr_status.py -k r66`: 7 passed. The reviewed content is otherwise unchanged (commits after the reviewed `d6d1f7f5` are `555f98cd` and this record).
