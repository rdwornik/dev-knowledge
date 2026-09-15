---
intake-id: 101
status: DRAFT
origin: operator direction, dispatcher seat session, 2026-09-15 — filed rather than ruled in chat, at the operator's explicit instruction
consumed-by:
---

<!--
  Genre (ADR-98 §3): WHAT/WHY only. No HOW, no solutioning, no ADR-drafting.
  Where a fix suggested itself while writing, it is recorded as an open question instead.
  Evidence base: $CLAUDE_PROMPTS_DIR/to-browser/DIGEST-2026-09-15-unrecorded-findings.md §1, §2, §6.
  That digest is EVIDENCE, deliberately not a decision — a decision file on the transport arms
  decision-coverage against every concurrent session.
-->

# Runtime resources have no owning organ

## Problem / motivation

The harness has organs for **decisions** (ADRs, the intake spine, `decision-coverage`), for
**files** (hermetization, the canonical-doc registry, freshness gates), for **tests** (RED-first,
the impacted-tests guard, the proof-layer ratchet), for **gates** (the pre-commit chain, the ship
gate, `audit.py health`) and for **process-as-workflow** (the conductor, lane contracts, the merge
queue).

**Nothing owns runtime resources.** No surface declares who may allocate them, for how long, what
reclaims them, or what refuses when the budget is gone.

Every operational incident of the week of 2026-09-08 is that single absence expressed differently:

- orphaned process trees — a measured **46.8-hour orphan**, and a **grandchild that outlived its
  parent's kill**
- commits killed by the OOM reaper — currently a **non-zero** count per batch
- idle sessions reaching **~15 GB each**; four combined to ~60 GB and triggered the OS OOM killer
- lanes slowed by memory pressure, with a loaded box degrading monitoring first and silently
- a session transcript large enough to freeze the client (**102 MB `.jsonl`**, ~90% of available
  RAM)

Each has been handled as its own incident, by whoever noticed. That is the shape of a missing
organ: the individual repairs are all reasonable, none accumulates into a mechanism, and the next
instance arrives unattenuated and is diagnosed from scratch.

**Why now.** Eight concurrent lanes on one workstation is now an ordinary batch, and the
arithmetic is fixed: ~28 GB total, ~15.6 GB held by non-Claude processes, ~3 GB reserve —
**~9.6 GB for Claude at ~392–400 MB per lane, a 24-lane hard ceiling.** That ceiling is real, is
written nowhere, and is re-derived by hand each time anyone asks. Meanwhile a second regime with
entirely different economics — Codespace, metered per minute of uptime — is being planned for
with none of its costs measured.

**If this stays unaddressed:** the ceiling keeps being rediscovered; batches keep being sized by
intuition; OOM keeps killing commits mid-gate, which is the worst available failure mode because a
half-applied gate looks like a defect in the gate; and Codespace budget is spent without anyone
able to say on what.

## Scenarios (+1 view)

**S1 — the dispatcher sizes a batch.** As the operator I ask for eleven lanes. The lane-ceiling
refuses at six, on *coordination* grounds. Nothing refuses on *memory* grounds, and the memory
ceiling (24) and the coordination ceiling (6) are unrelated numbers never stated together. Today
the operator learns which one binds by watching the box fall over.

**S2 — a seat runs long.** As the integrator I keep one session alive for 22–24 hours because
context is expensive to rebuild. Unknown to me the leak is **time-based, not context-based**:
idle sessions grew to ~15 GB with context *constant* at 6,664 chars. My long-lived session is the
worst available shape and I hold it deliberately, for a reason that does not apply.

**S3 — a lane finishes and something of it does not.** As a lane I spawn a background process via
the Bash tool. My session ends. The process is reparented and runs indefinitely. Nobody owns it,
nothing reaps it, and it is found 46.8 hours later by someone looking for something else.

**S4 — the cost instrument meets the transcript.** As `lane_cost` I read session transcripts to
price a batch. One is 102 MB. I load it whole — no streaming read, no size guard — and take ~90%
of the machine's RAM with me, while being the instrument every routing decision now depends on.

**S5 — a Codespace is left attached.** As a lane I finish and hand back. My container stays warm
"in case", metered per minute. No receipt records uptime minutes, so the spend appears in no
report and is attributed to nothing.

**+1 (deployment view):** the two regimes are not one resource. Local is a **fixed ceiling you
allocate against**; Codespace is a **meter you run down**. A single policy tuned for one is wrong
for the other.

## Functional requirements

- **Must:** a named owner for runtime resources — an organ that can be pointed at, in the sense
  the other five can.
- **Must:** an allocation rule that can REFUSE. The local ceiling exists arithmetically and
  refuses nothing today.
- **Must:** a reclamation rule — what returns a resource, and on whose initiative.
- **Must:** separate parameters for the local and Codespace regimes, with no shared thresholds.
- **Must:** resource consumption visible in the receipts that already carry tokens and cost, so a
  batch can be priced in the resource it actually spent.
- **Should:** distinguish **context reclamation** from **session replacement** as different
  mechanisms — clearing context does not free process memory.
- **Should:** thresholds DERIVED from our own transcripts rather than chosen, with the derivation
  recorded so it can be re-run rather than re-argued.
- **Could:** a budget that can be exhausted, and a defined refusal when it is.

## Acceptance criteria (ex-ante)

1. A named surface answers, for any runtime resource: **who may allocate it, for how long, what
   reclaims it, and what refuses when the budget is gone.** Pointing at four separate mechanisms
   does not satisfy this; the question must have one home.
2. Asking for a batch that would exceed the local memory ceiling is **REFUSED**, with the ceiling
   read from a declared register rather than re-derived.
3. A spawned grandchild does **not** survive teardown — witnessed by a test that reproduces the
   survival first.
4. A seat past its declared lifetime is retired and re-booted **from its render**, and resumes
   from files alone with no loss.
5. A transcript over the declared bound is archived out of the scan path **before** any whole-file
   read; `lane_cost` is demonstrably safe against the 102 MB case.
6. A Codespace lane's receipt records **uptime minutes** alongside tokens.
7. The four operational measures have **before and after** figures under the same stated
   definition: lanes completed per hour; cost per lane; commits killed by the OOM reaper per
   batch; Codespace minutes paid per batch.

## Non-goals

- **Not** a rewrite of the lane-ceiling. The coordination ceiling (bounded by serial integration
  capacity) and a memory ceiling are different constraints that happen both to bound batch size.
  They should agree on nothing except that each can refuse.
- **Not** a fix for the upstream Claude Code defects. Five of the six behaviours above are
  **documented upstream and are not ours**. This is about owning our exposure to them.
- **Not** a cost-attribution or model-routing scheme — that is the enforced-routing work, in
  flight separately.
- **Not** a decision on whether to use Codespace at all. This asks what it costs, not whether.

## Impact sketch (4+1 lite)

- **Logical:** a sixth organ alongside decisions / files / tests / gates / process.
- **Process:** batch sizing, seat rotation and lane teardown gain a resource dimension; seat
  rotation stops being hygiene and becomes a performance requirement.
- **Development:** a register for declared ceilings; a reaper with process-tree semantics; a size
  guard in front of every whole-file transcript read; receipts extended with a resource field.
- **Physical:** the regimes are physically different — one workstation with a hard ceiling, one
  metered remote host with an idle timeout and a build cost.

## Open questions

1. **Is this one organ or two?** The regimes share a question (who allocates, what reclaims) and
   share no parameters. One organ with two policy sets, or two organs with a common vocabulary?
2. **Who initiates reclamation** — the seat on self-evaluation, an external reaper, or both? A
   seat that evaluates itself cannot act when it is the thing that has degraded.
3. **What is the refusal's blast radius** when the budget is gone? Refusing the 25th lane is
   clearly right; refusing an integrator mid-merge-queue may be worse than the overage.
4. **Where does the declared ceiling live** so it is read rather than re-derived — the
   desired-state register, `quality-requirements.yaml`, or a new surface?
5. **Do prebuilds pay for themselves** at our batch frequency? Unanswerable until container build
   time and batch frequency are both measured.
6. **What is the derivation** for the RSS and cost-per-turn thresholds, and is it re-runnable as
   the fleet changes? A threshold that cannot be re-derived becomes a restated constant.
7. **Does the response measure belong to this organ or to the conductor?** The four operational
   figures are the natural response measure, and the conductor already runs per push.
8. **What is the flip condition** — what evidence would say this organ is not needed, or that its
   ceiling is set wrong? Stating it now prevents the ceiling becoming unfalsifiable.

## Response measure

The four operational figures, per batch, before and after: **lanes completed per hour · cost per
lane · commits killed by the OOM reaper per batch (currently non-zero) · Codespace minutes paid
per batch.** The one that most directly falsifies success is the OOM-kill count: if it does not
reach zero, the allocation rule is not binding.

## Flip condition

If, across three consecutive batches with the organ in place, the OOM-kill count stays at zero
**without** the allocation rule ever refusing anything, the ceiling is set too loosely to be doing
work and should be re-derived — or the organ is carrying its weight through reclamation alone and
the allocation half should be retired rather than kept as decoration.
