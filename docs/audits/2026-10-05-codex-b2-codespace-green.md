# Codex review of `worktree-b2-codespace-green` — two P1 findings, both open (2026-10-05)

Consumer and contract: `LANE-B2-W1-b2-codespace-green` (batch B2-W1, lane W1-12), read by the close-out-only repair `LANE-B2-W1-b2-codespace-green-repair-1` (seat ruling A). This is the review record common rules §2 (e) asks for. The run record it pairs with is `docs/audits/2026-10-05-technical-codespace-green-run.md`.

## What was read, and by what

```
reviewer        Codex, model gpt-5.6-terra  (the common rules' route; deploy/codex-review.ps1 not used -- see below)
served model    gpt-5.6-terra   -- the tool's own run header: "OpenAI Codex v0.155.0 ... model: gpt-5.6-terra, provider: openai,
                                   sandbox: read-only, reasoning effort: high", session id 01a10e37-e939-7933-b591-3184fb03fb9a
nonce           2aa9e032c217    -- written to nonce.txt in the review folder; the reviewer returned it as its own line "NONCE: 2aa9e032c217"
content hash    sha256 13ed52c03c92a15b453a8abb6405c429d282c2d151b5bbdd2aa8eff558b92eb2  (the 3,880-line `git diff origin/main...HEAD` it read)
read at         branch tip f663d7b44796508efd2904224628a6dc2bc9cb88; origin/main 9c72c990e565d7212f3b27f36b481a587bda356e at the time
folder          an empty folder under the job tmp holding only branch.diff, the 20 changed files at the tip, the contract and nonce.txt
call            codex exec -m gpt-5.6-terra -c model_reasoning_effort=high --skip-git-repo-check -s read-only <prompt>   (stdin from null)
```

The wrapper `deploy/codex-review.ps1` was not used: it writes its own audit file, which the lane's own record replaces. A probe call before the review (the same flags, a trivial prompt) served and returned a nonce, so Codex was not limited. The pin in this repo's `deploy/codex-review.ps1` now names `gpt-6-astra` (R82), while the common rules fix this lane's review route at terra; the review ran on terra, as the rules say, whatever the re-point decides.

## Verdict

```
VERDICT: FAIL two P1 correctness defects          (the reviewer's own last line)
P1  scripts/codespace_parity.py:1523   C3 does not bind the integration record to the Codespace's own lane branch
P1  scripts/dispatch.py:2312           disconnect detection is caller-supplied; nothing accumulates the bound or writes the FAILED fate
P2  none
P3  none
```

## The two findings, and this session's check of each against the code

**P1 1 — C3 can pass on an integration record that is not about this run.** The reviewer: nothing binds the integration record's `run_branch`/`run_sha` to the branch the Codespace run produced, so a green record for another or stale `worktree-*` branch cut from the same base passes beside the Codespace record. Checked: `integration_legs` (`codespace_parity.py:1403`) compares the integration's own `base_sha` with the compared base, requires `run_cut_from_base`, and requires the merge's second parent to equal the integration's own `run_sha`; `compare_landing` (`:1525`) compares the Codespace's `pushed_sha` with its own HEAD. No line compares `integration.run_branch` or `integration.run_sha` with anything the Codespace record says it produced. The finding stands. The record does name the Codespace-side pushed branch (`worktree-<slug>-parity`) and the integration names the test lane's branch (`worktree-<slug>`): they are different branches by design, so the binding needs the Codespace record to carry the lane branch it worked and its tip, which it does not today.

**P1 2 — the heartbeat's disconnect bound has no clock and nothing records the fate.** The reviewer: `codespace_observe(unreachable_for_s=0.0)` takes how long the box has been unreachable from its caller; a repeated call defaults it to zero, so a box unreachable for hours stays `WAITING`; no dispatch path calls `write_fate`. Checked: the docstring at `dispatch.py:2322` says "the observer owns that clock, not this one-shot read"; `codespace_state.assess_lane` reads the bound at `:471`; `write_fate` has one caller, the `codespace_regime.py fate` CLI (`:425-442`), run by hand. The tests pass by injecting `unreachable_for_s`. The finding stands: the heartbeat classifies correctly when told the time, and the stall (`hung`) path reads the box's own progress file so it needs no caller clock, but no runner turns repeated unreachable readings into the `disconnected` fate or writes a fate row on its own. The night's polling loop that did it (`observe-loop.ps1`) lived in the stopped job's tmp, not in the repository.

## Disposition

Neither P1 is declined, so nothing goes to N2's independent reviewer. Neither is fixed in this repair: seat ruling A makes this a close-out-only repair with no new build work, and each fix is a design change with its own tests (a lane-branch field in the Codespace record plus a comparison; an observer loop or a stored first-unreachable stamp plus a `write_fate` call). Both are carried into the follow-on W2 lane in `to-browser/SESSION-b2-codespace-green.md`. The effect on the Done-contract is stated there: items 2 and 5 are built and tested, with one reviewer P1 open on each; item 7 is PARTIAL on that account.

## Not read

The review read the diff and the changed files. It did not run any code. The reviewer reported no P2 or P3; that is its answer to the prompt above (correctness defects, N1 parity-leg vacuity, classifier and heartbeat fates, secret leakage, the login-shell change, the four-seam re-point, vacuous tests), not a proof that none exist.
