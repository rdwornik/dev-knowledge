# Arc 5 P1 — Routines pilot: second cloud-night routine, DESIGN ONLY (#270-gated)

> **PLAN-ONLY. Nothing here runs.** This is the P1 pilot deliverable (intake doc #2 §3 SHOULD-Routines, EXTEND-not-create per the 07-06 correction): the design of a SECOND routine under the #86 cloud-night envelope. **Hard gate (architect ruling, non-negotiable): this routine does not START before BACKLOG #270 (operator-load gauge) is IN EFFECT.** Zero night executions were performed by Arc 5. Feeds #271 (its "full serial test suite + timing-trend report" executing element) and buy-vs-build verdict 1.

## The routine: nightly full-serial test suite + timing trend

- **What it does:** one nightly cloud run on the hub clone executes `pytest --tb=short -q --durations=25` (full serial suite — 1384 tests, ~10 min local-Windows witnessed 2026-07-06) and emits ONE dated digest: pass/fail counts, total wall-clock, top-25 durations, and the delta vs the prior run's digest.
- **Why it pays rent:** Epic-5 (test-tiering) needs slow-test candidates from real serial runs, and the operator's morning funnel needs suite-health without spending an attended 10-minute run. The digest's per-night wall-clock series IS the timing trend.
- **Pre-authorized deterministic contract (frozen; the #271 §6 class — night EXECUTES, judgment sleeps):** run the suite → write the digest → open the PR. No refactoring, no test edits, no triage, no proposals. Anything unexpected (collection error, guard trip) = report-and-stop.
- **Honest environment note:** cloud runs measure the Linux runner, not the operator's Windows box. The trend is self-consistent night-over-night (same runner class) and that is the series Epic-5 consumes; it is NOT a Windows-latency oracle — never compare cloud digests against local wall-clocks.

## EXTEND-not-create: what is reused from the #86 envelope, unchanged

Platform-guards model (no Write/Edit deny, by design) · `claude/test-timing-YYYY-MM-DD` branch → PR, never main · Action diff-guard: anything other than exactly one ADDED digest file fails the run · post-run `git status --porcelain` tripwire reported in the PR · fail-soft catch-up posture (a missed night is caught up next night, surfaced at SessionStart) · A2 native auto-mode nets — already LIVE on the envelope as of Arc 5 WI-1b (`b79e675`), inherited here, nothing new to add.

## The 7-point routine standard (PLAYBOOK "What every routine must meet"), walked ex-ante

1. **Self-containment:** single-repo Linux clone; consults only its own tree; pytest + git only; no hub-external reference on the executing path (trivially met — it IS the hub).
2. **Declared output channel:** `claude/test-timing-YYYY-MM-DD` → PR → diff-guard → squash-merge of the one digest (the compliant-by-design cloud channel).
3. **`Routine: test-timing` commit trailer** on the digest commit (#123 git-indexability).
4. **Per-stage model pins:** mechanical single-stage session — pinned M-tier `claude-sonnet-5` (post-A1); no fan-out, no `fallbackModel` (ADR-80 §5).
5. **Fail-soft + catch-up:** missed run tolerated; next night catches up; SessionStart surfacing reports last conclusion + digest-presence side-effect check (the existing pattern).
6. **Funnel-review as consuming contract:** consumer = the operator morning funnel + Epic-5 test-tiering; findings are data, nothing binds without ratification.
7. **n=2 evidence gate:** two real runs demonstrate end-to-end before any codification into the routine standard; runs 1–2 are the probation window.

## Rent + survival (ex-ante, pre-registered)

- **Consumer:** morning funnel (digest read) + Epic-5 (slow-test candidates).
- **Survival metric:** within 2 weeks of start, ≥1 funnel item or Epic-5 decision cites the timing digest; otherwise the routine is reviewed for removal (fleet-audit lesson).
- **Kill criterion:** two consecutive weeks unread/unactioned → demote to weekly, then remove — the meter must not become more noise (inherits the #270 draft's own kill-shape).
- **Load discipline:** the digest adds at most ONE funnel item per night and is CAP-exempt only as a pure data artifact; any proposal-shaped content is out of contract (see the frozen contract above).

## Start condition (the gate, restated as the doc's own contract)

START = (#270 `[load]` line rendering live in the SessionStart digest AND the OPERATOR-LOAD.csv appending) THEN architect approves this contract as a pre-authorized nightly contract. Neither condition is waivable by a lane; night execution before #270 requires the explicit pre-authorized-contract proposal route to the architect — which this document is, submitted for that later approval, not exercised now.

## Pilot ex-ante metric (Arc 5's own, frozen at plan approval)

Met iff: this design doc passes architect review with all 7 standard points + rent + the intact #270 gate named, and Arc 5 performed zero night executions. (Outcome recorded at the frozen-contract read-back.)
