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
- **Does the platform's 30-minute idle timer reap a working headless lane?** The docs say terminal
  *output* resets the timer; a headless agent streaming stream-json to a file may produce none.
  If true this is the mechanism behind both silent zeros and the fix is ours, not a monitoring
  question at all. **Measurement pending in the same cloud run that proves the corrected config.**
- **Is `updateContentCommand` re-run at creation from a prebuild?** Documented as prebuilt;
  whether it re-runs on the create path is UNKNOWN in the docs and is being measured. The answer
  changes how much of the source-freshness problem the platform solves for us.
