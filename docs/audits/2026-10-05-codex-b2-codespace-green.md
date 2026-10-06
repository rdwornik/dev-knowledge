# Codex review of `worktree-b2-codespace-green` — two P1 findings, both open (2026-10-05)

Consumer and contract: row [#1335] and `LANE-B2-W1-b2-codespace-green` (batch B2-W1, lane W1-12), read by the close-out-only repair `LANE-B2-W1-b2-codespace-green-repair-1` (seat ruling A). This is the review record common rules §2 (e) asks for. The run record it pairs with is `docs/audits/2026-10-05-technical-codespace-green-run.md`.

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

---

## Amendment 2026-10-06 — repair 2 answers the integrator's refusal (`to-browser/REFUSED-b2-codespace-green.md`, repair 1 of 2)

Consumer and contract unchanged: row [#1335] and `LANE-B2-W1-b2-codespace-green`; read by `LANE-B2-W1-b2-codespace-green-repair-2`. The integrator refused the handback `86a8d744` because the two P1s above were neither fixed nor declined (order step 3(g)). This repair built only those two fixes, then had Codex terra read the delta.

**P1 1 (C3 bound to the run) — FIXED** at `3face0cc`. RED first (14 failed at the synced tip), then GREEN. The Codespace record carries `lane` = branch and tip (`stamp-lane`); `integration_legs` FAILs a record for another branch or another tip, and reads NOT-RUN when the record names no lane.

**P1 2 (the fate has its own clock and the line records it) — FIXED** at `8ecfd2af`. RED first (6 failed), then GREEN. `codespace_observe` derives the unreachable duration from a stamp stored on the regime ledger's fate row and appends every fate transition through `write_fate`.

### The delta review

```
reviewer        Codex, model gpt-5.6-terra, the common rules' route
served model    gpt-5.6-terra   -- the tool's own run header ("OpenAI Codex v0.155.0 ... model: gpt-5.6-terra, provider: openai, sandbox: read-only, reasoning effort: high")
call            codex exec -m gpt-5.6-terra -c model_reasoning_effort=high --skip-git-repo-check -s read-only <prompt>   (stdin from null)
folder          an empty folder under the job tmp: delta.diff, the six changed files at the tip, refusal.md, nonce.txt
```

```
read 1   a09c4fff..8ecfd2af   delta sha256 a333a2b6fc99175dff758a9c773e21d75a394e6932c364934978c0421d5a2274   session 01a10e7d-b91c-7c70-a654-e336afe5f0c4   nonce c4837ade7279 (returned)
         the first attempt (session 01a10e7c-...) answered "inputs inaccessible": my prompt forbade it every command, so it could not read the folder; no finding, nonce not returned; re-run with reads allowed
         VERDICT: FAIL   P1 dispatch.py:2319 slug optional, an unrecorded observation is possible   P1 dispatch.py:2358 an unreadable listing clears the stamp   P2 codespace_regime.py:251 last_fate ignores the slug
read 2   a09c4fff..f4c65f4d   delta sha256 29da055bef8d05bdfcffce8125443f50383610f571456bb12bdd899b84066617   session 01a10e84-b65b-7371-b16e-bf04239dbe5a   nonce 07d6dfb67a66 (returned)
         VERDICT: FAIL   P1 dispatch.py:2371 `container is None` keeps the stamp even for a confirmed teardown
```

**Read 1 — all three findings were right and are FIXED** at `f4c65f4d`, RED first (3 failed): the `codespace-observe` CLI now REQUIRES `--slug` (the line never reads a lane unrecorded; the one-shot read stays a function seam, covered by its own test); an unreadable listing keeps the stamp, which ends only on an affirmative recovery or a terminal reading; `last_fate` is looked up by codespace and slug.

**Read 2 — the one P1 is DECLINED (N2).** The reporter's claim is that a confirmed teardown is recorded with a carried `unreachable_since`. Author's position: `container is None` happens only when `gh codespace list` failed or its JSON did not parse; a readable listing without the box gives `"Absent"` (`codespace_state.state_from_listing`), which is not `None`, so a confirmed teardown never takes the carry branch. `test_a_terminal_reading_ends_the_streak_and_a_later_box_starts_a_new_clock` already asserted that and passed at the tip it was filed against.

Sent read-only to `grok-4.7` (told it cannot execute; the code, the claim and the test inline), nonce `97937798389b`:

```
served          grok-4.7   -- the tool's own usage record ("modelUsage": {"grok-4.7": ...}), session 01a10e8a-6cc8-7301-9fd3-53b83573364f, request f1c3968b-99dd-4523-9e6a-f1899b168c80
                           (the reply's own "SERVED:" line said grok-4.5; the tool's record is the evidence, the self-report is not)
nonce           97937798389b (returned)
VERDICT: REJECTED   "A confirmed absence is not recorded with a carried unreachable_since ... the unreadable-vs-empty distinction the finding asks for is already in this control flow."
```

Both positions are recorded; the independent verdict decides, so no fix. One test was added for the edge the finding pointed at (`test_an_unreadable_listing_is_never_read_as_a_confirmed_teardown_even_when_one_is_expected`, `2ea065e9`): an unreadable listing with `expected_gone` reads WAITING with the stamp kept, and only the readable empty listing reads TORN-DOWN with no stamp.

**Not read.** Neither read ran code; reads 1 and 2 saw the delta from `a09c4fff` (the sync merge), not the whole lane again. The decision is the reviewers' answers to the prompt, not a proof that no defect remains.
