---
intake-id: 102
status: DRAFT
origin: operator directive, 2026-09-15 — Phase 3 of the "stop patching Codespaces and learn it first" arc; the operator explicitly routed this question to the decision engine rather than ruling it in the diff
consumed-by:
---

<!--
  ADR-98 genre note, stated because this doc sits close to the line. The operator asked for
  four named OPTIONS with a comparison matrix, a response measure and a flip condition. Those
  are carried below as DECISION OPTIONS — the material the engine rules ON — and not as a
  chosen design. No option is selected here; the "Open questions" section is where the choice
  stays open. The operator's own recommendation is recorded as exactly that, a recommendation,
  because he said the engine rules and not him.
-->

# How the fleet knows a Codespace lane's state

## Problem / motivation

A dispatched Codespace lane is known to have failed only when a human looks at it. Twice a
detached lane produced zero work and nobody noticed until much later. The substrate itself died
at one commit on 2026-09-14 and went unnoticed for two weeks, because nothing ran there in the
interval — a health signal that fires only when someone happens to use the thing is a usage log,
not a health signal.

The reflex for a month has been to patch the symptom: a retired call, then a provenance marker,
then a heartbeat. Each was a real repair. None of them answers the question a dispatcher actually
has to answer, which is *"is the lane I started five minutes ago alive, working, finished, dead,
or reaped?"*

**Three platform facts now establish that this cannot be solved by reading the platform harder.**
They were measured against GitHub's own documentation on 2026-09-15 and are recorded in
`DIGEST-2026-09-15-codespaces-reference.md` (§g, §h) with sources:

1. **There is no codespace webhook.** The documented webhook event index contains no
   `codespace`/`codespaces` event at all. Every event-driven design is unavailable — not
   expensive, unavailable.
2. **A recovery container is externally indistinguishable from a healthy one.** When a container
   fails to start, the platform substitutes a recovery container. No documented state value, API
   field or flag says "recovery"; it reports a normal live state and is reachable. The only
   documented outside discriminator is the creation log, which is prose read by a human.
3. **"Working" is not a platform-observable property.** `Available` means the machine is up, not
   that anything is running. There is no job-status API, no completion callback, no progress
   stream for work inside a codespace.

So the observability we need does not exist to be switched on. It has to be constructed, and the
shape of that construction is an architectural choice with real cost and real failure modes —
which is why it is filed here rather than decided in a diff.

**What already exists, so the decision is not taken on a blank page.** `[#554]`/`[#746]` lane aa-1
landed two layers: **L1 provenance**, a marker written by the build and verified by a lane's step 0,
which a recovery container cannot produce — this is positive proof *from inside*; and **L2
heartbeat**, a scheduled credential-free probe plus a pre-dispatch refusal, which proves the
substrate *declaration* is coherent on a cron. Neither watches a **running lane**, and the
dispatcher records nothing about what it created. That is the gap this intake is about.

## Scenarios (+1 view)

- **The silent zero.** As the operator I dispatch a detached Codespace lane and go to bed. The
  container is reaped by the 30-minute idle timeout twenty minutes in. In the morning there is no
  branch, no receipt, no row, and no signal — only a codespace in a stopped state that I have to
  think to go and look for. This has happened twice.
- **The recovery substitute.** As the operator I dispatch into a container whose `postCreateCommand`
  failed. The platform substitutes a recovery container and reports it live. The lane runs, finds
  no toolchain, and returns quickly with an empty result. I read the fast return as success.
- **The hang.** As the operator I dispatch an attached lane. It stops emitting events but the
  container stays up. Today the inference fuse catches this after 15 minutes of no event arrival —
  but only because a process is attached and watching. A detached lane has no such watcher.
- **The orphan bill.** As the operator I finish a batch. Every codespace a lane created is still
  running, because teardown is a manual verb nobody typed. I pay compute minutes for machines
  whose work landed hours ago.
- **The dispatcher's question.** As the dispatcher I need to know, without a human, which of the
  four lanes I launched are still alive — so that a dead one becomes a row while the batch is
  still open, rather than an archaeology exercise at integration.

## Functional requirements

- **Must:**
  - Distinguish, without a human looking, between: alive-and-working, finished, died, and
    timed-out.
  - Detect a lane that dies mid-work and turn it into a visible failure and a filed row.
  - Detect the recovery container specifically, and say so by that name rather than by a
    downstream symptom such as "claude is not installed".
  - Survive the container's own death — whatever records progress must land somewhere that
    outlives the machine reporting it.
  - Record the codespace's identity at dispatch, durably. Nothing can poll what was never
    written down.
- **Should:**
  - Release paid compute at handback rather than leaving containers warm.
  - Cost no model credential, so the mechanism cannot go permanently red for want of a secret —
    this repo has no Actions secrets at all (`gh secret list` returns `[]`).
- **Could:**
  - Report in-flight progress granularly (turn count, last event), not merely alive/dead.

## Decision options (the engine rules; none is chosen here)

**Option A — poll from outside only.** A watcher external to the container polls
`gh codespace view --json state,lastUsedAt` (and fetches the creation log once at start).

**Option B — push from inside only.** The lane's runner emits progress from inside the container
to a durable destination (a git ref, an API call, an artifact).

**Option C — both.** Outside liveness polling paired with inside progress reporting, the pair
used as a discriminator: the cross of "container up?" against "progress recent?" distinguishes a
dead container from a hung lane.

**Option D — do not run lanes on Codespaces at all.** Route execution to GitHub Actions or keep
it local.

### Comparison matrix

Criteria are the operator's, in his order. `partial` is used where a criterion is met only under
a stated condition, and the condition is named rather than glossed.

```
criterion                     A (poll only)   B (push only)   C (both)      D (no codespaces)
detects death mid-work        yes             partial (1)     yes           n/a (2)
detects recovery container    partial (3)     yes (4)         yes           n/a
needs no human                yes             yes             yes           yes
survives container death      yes (5)         partial (6)     yes           n/a
distinguishes dead from hung  no (7)          no (8)          yes (9)       n/a
cost                          low (10)        low             low-moderate  see (2)
```

1. A dead container stops pushing — but silence is ambiguous: it is also what a slow turn looks
   like. Absence of a signal is not a signal.
2. Not applicable rather than "yes": D removes the substrate instead of observing it, so it
   scores on a different axis. Its real cost is the capability lost — Actions is not an
   interactive agent host, and local execution is bounded by the workstation's ~24-lane memory
   ceiling and re-serialises work that Codespaces parallelises.
3. Only via the creation log, fetched once and parsed as prose. The state field cannot answer it.
4. L1's provenance marker already gives this: a recovery container cannot produce the marker.
5. The observer is not in the thing being observed, which is the property that matters.
6. Only if the push destination is durable and external. A push to the container's own filesystem
   dies with it — this is exactly how `receipt.json` is lost today when a lane is reaped.
7. Both read as `Available` while a hung lane burns minutes.
8. Both read as silence.
9. This is the whole argument for C: container-up + progress-stale = hung; container-down +
   progress-stale = dead; container-up + progress-fresh = working. One signal cannot make that
   cut; two can.
10. Polling is cheap in API terms but is not free in complexity — it needs a process that
    outlives the dispatch, which the current architecture does not have.

### Response measure

What the fleet does with the answer, stated so the mechanism is judged on an outcome and not on
its own existence:

- **Detection latency** — time from a lane's death to a filed row. Target to be set by the
  engine; today this figure is unbounded (twice measured as "overnight", once as two weeks).
- **Silent-zero count per batch** — lanes that produced no work and generated no signal.
  Currently non-zero; the mechanism is working when this is zero.
- **Paid idle minutes per batch** — compute billed after a lane's last useful work. Currently
  unmeasured and unbounded.

### Flip condition

Stated ex-ante so the decision is revisitable on evidence rather than on fatigue:

- **Flip away from the chosen option if** the observer itself becomes a source of false reports —
  specifically, if it files rows for lanes that were in fact healthy (a false-positive death) more
  than once per batch. An observer that cries wolf is worse than none, because a row that is
  routinely wrong stops being read.
- **Flip toward D if** the measured Codespace minutes per batch exceed the free-tier allowance
  while the silent-zero count stays non-zero — i.e. we are paying for a substrate we still cannot
  observe.
- **Flip away from D if** it is chosen and the local memory ceiling is reached, since that is the
  constraint Codespaces exists to relieve.

## Acceptance criteria (ex-ante)

1. A lane killed mid-work (container stopped externally while the lane runs) produces a filed row
   without any human action, within the detection latency the engine sets.
2. A codespace created from a deliberately broken `devcontainer.json` is reported as
   `recovery-container` **by that name**, with the creation-log evidence that distinguishes it
   from our container quoted in the report.
3. A healthy lane run end to end produces no false failure report.
4. Killing the observer does not silently disable detection — its own absence is detectable.
5. Every requirement above is an entry in `ecosystem/quality-requirements.yaml` with a trip-test
   that goes RED when the organ is neutered.

## Non-goals

- Choosing the implementation. This doc carries options; the engine rules.
- Re-opening whether Codespaces is the right substrate for execution — that is option D's job to
  raise, and the four-axes routing ruling (`execution = CODESPACE-on-green`) stands until an
  accepted decision moves it.
- Monitoring the *local* substrate. A local lane runs on the machine the operator is sitting at;
  its liveness is not in question and gating it on a cloud probe would refuse the one substrate
  that is definitely alive (L2's existing reasoning, unchanged).
- Anything about model spend, token cost, or provider routing.

## Open questions

- **Which option?** The operator's recommendation is **C**, recorded as a recommendation. The
  engine rules.
- **Where does an inside push land so that it survives the container?** A git ref on the lane's
  own branch is durable and needs no credential beyond the one the codespace already has, but it
  writes to the repo on a cadence. An Actions artifact, a gist, or a comment are alternatives with
  different durability and different noise. Unresolved.
- **What polls, and what keeps the poller alive?** A dispatcher that exits has stopped watching.
  A cron on Actions outlives the dispatch but adds minutes against a live spend ruling. A local
  scheduled task is free but dies with the workstation.
- **Does the platform's 30-minute idle timer reap a working headless lane?** **ANSWERED
  2026-09-15 by derivation, not by a cloud run** -- see the amendment below. Yes, by construction.
  What remains unmeasured is narrower and is named there.
- **Is `updateContentCommand` re-run at creation from a prebuild?** Documented as prebuilt;
  whether it re-runs on the create path is UNKNOWN in the docs and is being measured. The answer
  changes how much of the source-freshness problem the platform solves for us.

## Amendment 2026-09-15 — the reap is ours, and it is upstream of every option here

> Added the day this intake was filed, before any ruling. It does not change the question; it
> changes what the options can be expected to achieve, so leaving it out would let the engine
> rule on a matrix that overstates all four.

**The finding.** A detached Codespace lane produces **zero terminal output for its entire run**,
and the codespace is created with `--idle-timeout 30m`. The platform documents that a process
producing no terminal output does not keep a codespace alive. So the machine is stopped at thirty
minutes of wall clock, mid-work, however much real inference is happening inside it.

**Derived from our own source plus the platform's own rule, at no cloud cost:**

1. `DispatchHelpers.psm1` passes `--idle-timeout 30m` at create (`$script:CodespaceDefaultIdle`).
2. The generated runner starts the agent as
   `claude -p ... --output-format stream-json --verbose > "$RUN_LOG" 2>&1 &` —
   **both** streams into a file. Nothing reaches a terminal.
3. In detach mode the runner re-execs itself as
   `setsid nohup bash -l "$0" </dev/null >>.../dispatch-detach.log 2>&1 &` and the parent exits,
   so the ssh session ends immediately. After that there is **no terminal at all**.
4. The fuse loop's only `printf` is redirected to `$RUN_DIAG/verdict.txt` — also a file.
5. GitHub documents activity as "Personal interaction with a codespace, such as typing or using
   the mouse" and "Terminal activity, either input or output", and its own worked example is a
   process still running while the codespace times out for want of terminal output.

**Why this matters to the ruling.** The fuse inside the container measures *event arrival* and
resets on every new line in the log — the right quantity, measured well. But the platform's timer
measures a quantity our design holds at **exactly zero for the whole run**. Two clocks, and the
one that can kill the machine is the one nothing in our design feeds.

**It explains the silent zeros.** A lane reaped at T+30min leaves no receipt — `receipt.json` is
written after the run and dies with the container (matrix footnote 6) — so the lane produces
nothing, and the codespace reports a stopped state that looks exactly like an orderly finish.

**The consequence for the options, stated plainly: none of A, B or C prevents the reap.** They
change only whether anyone finds out.

- **A (poll outside)** sees the stopped state and can report a death. It does not prevent one.
- **B (push inside)** is *worse than neutral here*: a git push or an API call from inside the
  container is **not terminal output**, so it does not reset the platform's timer either. A
  design that reports progress faithfully every thirty seconds would still be reaped at thirty
  minutes.
- **C (both)** inherits both properties: excellent detection, no prevention.

So **keep-alive is a separate decision from observability**, and it is upstream: ruling A/B/C
without it buys a fleet that reliably reports its own lanes dying on schedule. The candidate
remedies, none chosen here:

- **Raise `--idle-timeout`** to the documented 240-minute maximum. Bounded, one flag, and it does
  not eliminate the class — a lane over four hours still dies. It also raises the cost of a lane
  that finishes early, which is exactly what the auto-STOP-at-handback requirement (QR-RES-002)
  is for; the two should be ruled together.
- **Keep a terminal attached** — do not detach; hold the ssh session and tee the stream to it.
  Restores real terminal output, at the price of making the workstation's connection load-bearing
  for the lane's whole life.
- **Emit terminal output from inside** on a cadence. Cheap to write, but see UNKNOWN below: with
  no session attached it is not established that any terminal exists to write to.

**What is still UNKNOWN, and is cheap to settle in the one billable run already planned.** The
docs answer what counts as activity; they do not answer these, and they are not inferred here:

- Does an **open ssh session with no bytes flowing** count as activity?
- Does output written inside a **detached `tmux`/`screen`** session count?
- Does an **outside API poll** (`gh codespace view`) touch `last_used_at` or reset the timer?
- Is the timer's zero point last activity, or codespace start?

**This is now an instruction to the proof run**, which should carry the measurement rather than
merely prove the config: dispatch one trivial detached lane whose work is a sleep longer than the
idle timeout, set `--idle-timeout` to its five-minute documented minimum so the answer arrives in
minutes rather than hours, and record the state transition and its timestamp. The same run answers
the `updateContentCommand` prebuild question. One machine, both UNKNOWNs.
