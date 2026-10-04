# Codex Review — b2-row-close-on-merge

**Date:** 2026-10-04
**Branch:** `worktree-b2-row-close-on-merge`
**Diff range:** `origin/main...HEAD` (`ecosystem/doc-counts.md` excluded as generated). Base `e67f27ac`, the sha this lane merged at step 0. Reviews 1-4 were taken at `6cf78acd` (the `da5078e8` code plus the counts regeneration), `1d89fc16`, `f754e6f3` and `1841dcd6`.
**Mode:** diff-review, isolated read-only session — a fresh folder under the job tmp holding the diff, the changed files, the contract, the earlier answers and a `nonce.txt` (not the lane)
**Consumer:** `LANE-B2-W1-b2-row-close-on-merge.md` (Done-contract item 6, "the review record per common rules §2 (e) … citing this contract inside it, its P1s fixed"); the integrator's merge verdict for batch B2-W1 reads it.
no-consumer: a lane's frozen contract is the only consumer this record has, and it is a transport file, not a governance surface (`[#id]` row, ADR, `STANDING_RULINGS`, intake) that `consumer_at_landing` recognises

**Model used:** `gpt-5.6-terra`, served — read from each run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`. Reasoning effort `low` for review 1 (the default) and `high` for reviews 2-4. Sessions: review 1 `01a106d2-41ee-78a3-a567-c0b87e0b3405`; review 2 `01a106dd-74bd-76c1-80c2-bfcdd76fd698`; review 3 `01a106f7-9897-7ec3-b909-5c322a42d1be`; review 4 `01a106fc-3984-75a3-a113-4bab44faacaa`. Codex route, so no substitution.
**Nonce returned:** review 1 `NONCE-a59b2fee80174d83`; review 2 `NONCE-f506d27b76e54a33`; review 3 `NONCE-21fe12ad632547fa`; review 4 `NONCE-883a980a006f4aa8` — each the first line of the reviewer's answer, equal to the `nonce.txt` it was given.
**Review profile:** code
**Tally:** review 1 P1=3 P2=1 P3=0, `FAIL`; review 2 P1=3 P2=0 P3=0, `FAIL`; review 3 P1=2 P2=0 P3=0, `FAIL`; review 4 P1=2 P2=0 P3=0, `FAIL`. Verdict lines reported as given. Every P1 is fixed or disposed (below). The tip after the review-4 fixes was **not** reviewed a fifth time; each pass found narrower defects than the last, and the loop stopped there by decision, not by a clean read.

## Review 1 (tip `6cf78acd`)

| P | Finding | Disposition |
|---|---|---|
| P1 | `scripts/gen_task_tree.py` `--close-row`: the direct CLI still closes with a typed SHA and no CI or test evidence | **Disposed, out of scope.** That is the existing `[#730]` writer; the contract's N1 says reuse it and its Do-not bars a second writer or a wrapper that removes it. The new step is the only path that closes with verified evidence; barring a lane from the direct CLI is ruling (h)'s procedure. Carried as a `ROWS-OWED` line in the SESSION file |
| P1 | `--lane-session` is caller-controlled and overrides the claim-marker session | **Fixed, `1d89fc16` then `f754e6f3`.** The first fix made the marker win and refused a disagreeing flag; review 2 showed a no-marker fallback to the flag was still a forgery route, so the flag is removed and the marker is the only source. RED shown first: `test_a_lane_session_flag_cannot_override_the_claim_marker` failed with `assert 0 != 0` |
| P1 | test-node check finds class and function names anywhere in the source; a wrong-class or non-parametrised `[param]` id passes | **Fixed, `1d89fc16`.** Exact class nesting through `ast`. RED shown first: four tests `DID NOT RAISE RowCloseRefusal` |
| P2 | `Rows:` parser takes ids from any text before `; related` | **Fixed, `1d89fc16`.** The clause must open `closes —`. RED shown first |

## Review 2 (tip `1d89fc16`; the reviewer also read review 1)

| P | Finding | Disposition |
|---|---|---|
| P1 | any `[param]` selector is accepted on a parametrised function | **Fixed, `f754e6f3`.** A selector is refused outright; the function id is what is recorded |
| P1 | lane identity falls back to caller-provided values when no marker is found | **Fixed, `f754e6f3`.** No flag; no marker means the implementing session is unknown and the step refuses. Stated limit: the caller session is `$CLAUDE_CODE_SESSION_ID` |
| P1 | `closes - [#1]; notes [#2]` parses both ids | **Fixed, `f754e6f3`.** A suffix after the first `;` must be a `related` clause. RED shown first: 3 of 5 new tests failed before the fix |

## Review 3 (tip `f754e6f3`; the reviewer also read reviews 1-2)

| P | Finding | Disposition |
|---|---|---|
| P1 | `closes — none filed … ([#519] is the source)` closes `#519` | **Fixed, `1841dcd6`.** `none` is parsed as the no-row form before ids are read |
| P1 | an AST definition such as a module helper is accepted as a pytest node id | **Fixed, `1841dcd6`.** `test_*.py` / `*_test.py` file, `Test*` classes, `test*` function |

## Review 4 (tip `1841dcd6`; the reviewer also read reviews 1-3)

| P | Finding | Disposition |
|---|---|---|
| P1 | AST-valid tests can still be uncollectable (`__test__ = False`, a class with `__init__`) | **Fixed in part, `700aed43`.** Those static refusals are added. The remaining gap (conftest hooks, plugins, `python_*` overrides, skip markers) is a stated limit of a static check, in the module docstring: real collection at the merge sha is not run |
| P1 | the lane-worktree guard checks only the cwd, not `--repo-root` | **Fixed, `700aed43`.** Both are checked. RED not shown against the unfixed guard; the test fails by construction there (the old guard never looked at `repo_root`) |

## What shipped, in one line

`scripts/row_close.py`: the integrator's step after `merge_receipt.py close` that reads the contract's `**Rows:** closes —` ids, verifies the merge sha (from the closed receipt, reachable from `origin/main`), the CI push run and the named test node ids, and closes each row through `gen_task_tree`'s one writer with all three in the evidence clause — refusing, with every file byte-identical, on any missing evidence and when called from the lane itself.
