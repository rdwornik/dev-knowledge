# ADR-131: Landing is a script; a model is called only on conflict, red CI or BASE-MOVED

- **Status:** Proposed
- **Date:** 2026-10-22
- **Decision tier:** Path A — operator ratification (the operator's O1, LEDGER v300 T-B: GO on direction (e)+(b) of the integration-throughput digest).
- **Related:** ADR-85 (journal anchor, first-parent spine), ADR-120 (the spine is the whole loop), ADR-127 (CI on Windows and Linux is the verdict), ADR-130 (the outer loop runs in code); the standing-rules process-model ruling (2026-10-18: processes are models in code, one responsible module per step, the diagram is generated, library-first; 2026-10-20: code defines prose, never the reverse); R158, R158b, R159.
- **Decommission:** none. `.claude/commands/lane-integrate.md` stays the by-hand path until the teaching change below is applied.
- **Source:** `to-browser/DIGEST-INTEGRATION-THROUGHPUT-2026-10-22.md` §0 (reuse check), §1 (AS-IS), §4 (grades), §5 (option matrix and recommendation), §8 (decision box); `to-browser/DIGEST-HARNESS-MAP-2026-10-20.md` transition "landed" and ANNEX A row S12 (`land / merge`, `merge_path.py`, `merge_receipt.py`, trigger: integrator seat). Built by lane `e2-landing-script`, batch E2.0.

## Context

Landing is seat-run. The digest measured 22 landings, 2026-10-17..21 (§1): median open-to-close 43.9 min, of which about 11.6 min before the first integration push, 17.9 min waiting for CI, 0.8 min after. The E2.0 integrator session of 2026-10-21 spent about 62.5 Opus calls and 13.6 M cache-read tokens per receipt row (a session total divided by 8 rows, not a per-landing record). The deterministic part of that loop already exists as code: `merge_path.land()` (merge-on-base check, BASE-MOVED twice, integration push, CI verdict, the SAME sha to main), `merge_receipt.py` (steps and ledger) and `no_leftovers.py`. What is not code is the sequence before the first push (fetch, merge, regeneration, receipt carry) and the wait: `land()` polls 900 s by default against a 17.9 min median CI run, so a seat re-enters the wait by hand or by wake cron (digest §0, §1).

## Decision

- **D1 — option (e): the `land` transition is one script.** `scripts/land_lane.py` runs the lane-integrate sequence for ONE lane end to end: `fetch`, `merge --no-ff`, `regenerate`, `carry`, then ONE call to `merge_path.land()` (push-integration, poll, land), then `receipt` and `teardown`. It adds no second landing push and no receipt format: `land()` pushes, `merge_receipt` records, and a post-landing re-read of `origin/main` refuses to report LANDED if main does not hold exactly the sha CI judged.
- **D2 — a model is called only on conflict, red CI or BASE-MOVED.** The script makes no model call (a test puts `claude`, `codex` and `copilot` stubs on PATH and asserts none runs). On those three stops it exits non-zero (`EXIT_CONFLICT` 2, `EXIT_RED` 3, `EXIT_BASE_MOVED` 4; any other refusal 5) with a one-screen message naming the conflicting files, the failing checks, or whether main moved before or after the integration push. A conflict leaves the integration worktree clean at BASE.
- **D3 — the poll window is a parameter above 25 minutes.** `DEFAULT_TIMEOUT_S` is 1800 s (`--timeout`), against the 900 s of `land()`'s own default and a 17.9 min median run; the Windows-sensitive extension (+7 to +19 min on 7 of 22 landings) fits inside it.
- **D4 — landing for real is explicit.** Against a non-local `origin` the script refuses unless `--i-am-the-integrator` is passed; `--dry-run` prints the plan and touches nothing remote. The only tested mode is a throwaway clone with a local bare origin.
- **D5 — option (b), local batching, comes second and on top of (e).** One merge chain judged by one CI run, with a bisect on red, is a later lane that extends the same module; it is recorded here as the direction, not built.
- **D6 — what stays with a model.** Conflict resolution, a red or REGRESSED verdict, BASE-MOVED re-merge decisions, the handback verdict (`audit.py handback`) and reviews. The script reads none of these as judgement; it stops and reports.
- **D7 — the org move and merge queue (option (a)) is not decided here.** It stays blocked on the digest's UNVERIFIED items (§7.7) and is a precondition-free follow-on: a merge queue also needs a PR-open and wait script.

## Quality attributes

- **Quality attribute(s):** latency per lane, integrity (tested merge = landed merge), cost (model calls per landing).
- **Scenario:** a clean lane is ready to land; CI takes 17.9 minutes; or the lane conflicts; or main advances while CI runs.
- **Response measure:** a clean landing makes 0 model calls and prints per-step seconds; a conflict, red or BASE-MOVED stops with a named cause and exit code, pushing nothing it should not. Measurement plan (no number is claimed here): after ratification and the template change, record 5 consecutive clean landings through `land_lane.py` and report the median open-to-close wall from `logs/MERGE-RECEIPTS.jsonl` (baseline 43.9 min, digest §1; the digest's expectation of about 21 min is an expectation, not a result) and the Opus calls per landing from the integrator session's usage (baseline 62.5 per receipt row, session-amortized; target 0 on clean landings). Both baselines are the digest's and carry its caveats.
- **Decision evidence:** `tests/test_land_lane.py` (the six frozen witnesses a-f plus the dry-run, flag, carry and regeneration tests) and the real-use witness below.

## Evidence (R158b), throwaway clone with a LOCAL bare origin, CI verdict stubbed (no GitHub)

Run 2026-10-22 on the lane branch, no landing on the real main:
- clean lane: `state=LANDED exit=0`, steps fetch 2.16 s, merge 0.88 s, regenerate 0.00 s, carry 0.00 s, push-integration 1.78 s, poll 2.77 s, land 1.66 s, receipt 0.23 s, teardown 1.39 s; `origin main` equals `worktree-integrate-e1.0` (`caa1877dc4c1`); the `claude`/`codex`/`copilot` stubs on PATH were never run (marker file absent). The poll figure measures the stubbed verdict, not CI.
- conflicting lane: `state=CONFLICT exit=2`, `conflicts: ['shared.txt']`, worktree status empty, HEAD equals `origin/main`.
- BASE-MOVED: `state=BASE-MOVED exit=4`, "BASE-MOVED before any push", nothing pushed.

Honest limits: CI is the only judge the script reads and it is stubbed in the witness; `land()` is as sound as `ci_verdict`. The post-landing re-read DETECTS an unjudged sha on main after the fact; prevention is `land()`'s construction (one sha variable for both pushes), pinned by a mutation test. The ruleset (`deploy/conductor-required-checks.ruleset.json`) remains disabled, so until the operator applies it GitHub itself does not refuse a bad push to main.

## Consequences

- **No process changes until this ADR is ratified.** `.claude/commands/lane-integrate.md` and the integrator order template are untouched by the lane that built the script (R159); READY-TO-APPLY teaching text is carried in that lane's handback and applies only after ratification.
- The integrator seat stops being a waiting loop on the clean path; the Opus seat is needed on conflict, red and BASE-MOVED.
- A new script enters `ecosystem/harness.yaml` fates (`manual_until` 2026-11-23) and `ORPHAN_DISPOSITIONS` until the template names it.
- One carried receipt line per landing travels in a carry file and is folded into the next merge commit, as the integrator already did by hand.
- Reversible: the integrator can still run the by-hand chain.

## Flip-condition

Revisit if five consecutive clean landings through the script do not beat the baseline median wall, if a landing through it ever leaves main at a sha CI did not judge, or if option (a) clears its UNVERIFIED items (digest §7.7) and the org move is ratified, which would replace the CI wait and the BASE-MOVED check with the queue's own.

## Alternatives considered

- **(a) free org + GitHub merge queue** — blocked: the queue is available only to organisation-owned repositories and four items are UNVERIFIED (digest §7.7); it also changes the spine, the anchor and the receipts. Deferred, not rejected.
- **(b) local batching** — chosen as the second step on top of (e) (D5); alone it still pays 11.6 min of seat work per landing.
- **(c) Mergify** — a GitHub App on the PR flow; free-plan eligibility for a user-owned repo UNVERIFIED. Not chosen.
- **(d) TAP-style post-merge last green** — would let main be red and needs a revert script and a ruling on "tested merge = landed merge". Not chosen.
- **Do nothing** — the 44-minute median and about 62 Opus calls per receipt row stay.
