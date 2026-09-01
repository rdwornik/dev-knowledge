---
intake-id: 67
status: SEED
origin: measured by the integrator seat on 2026-09-01 while harvesting ATLAS-R1 — its two artifacts existed only under a job-scoped tmp directory that is deleted with the job, and the harvest that went looking for them found nothing until the operator supplied the paths by hand
consumed-by:
---

# A lane that publishes into a directory the harness deletes has not published

<!-- class: tech (lane-contract schema gap) · status: SEED — a pre-intake candidate, not yet
worked. DRAFT BINDS NOTHING; the repo wins on any conflict. -->
<!-- origin: operator direction, 2026-09-01, after the ATLAS-R1 harvest returned empty -->

> **SEED BINDS NOTHING.** This records a measured gap and the mechanism proposed for it. It
> authorises no gate edit, no schema change and no backlog row. ADR-111 gives a raw finding
> exactly one route, and this is its first step.

## Problem / motivation

**ATLAS-R1 produced two real artifacts and the integrator could not find either.** The harvest
searched the tree by name, the tree by word, the operator's `Downloads`, `Downloads` by content,
and every dispatch receipt on disk — and returned empty, recorded at
`docs/audits/2026-09-01-verification-atlas-r1-harvest-attempt.md`. The artifacts existed the whole
time, at `C:\Users\1028120\.claude\jobs\1732b879\tmp\{atlas,ledger}.html`.

**That path is deleted with the job.** A local lane that "publishes" to it has produced something
real and left no durable locator for it, and the failure is silent in the direction that matters:
the lane reports success, the artifact is genuine, and the next seat measures an absence.

**Publishing to a claude.ai artifact URL does not close it either.** ATLAS-R1's two views were
published (`dd03ecac-…` and `ec0fc7fa-…`), and the operator's own instruction records why that is
insufficient: *"record the URLs as provenance, not as the store."* A URL is evidence that
something was rendered, not a tracked file the corpus can index, cite, hash or survive on.

**The near-miss is the argument.** The paths were recovered because the operator had them. Nothing
in the lane's own output would have produced them, and no gate would have noticed. One session
later, or one job cleanup earlier, and two artifacts measured against a real graph — 1,783 nodes,
11,515 edges — would simply have ceased to exist with nothing recording that they had.

## Proposed mechanism

**Extend the lane packet schema with a required `ARTIFACTS:` block.** Every lane packet declares,
for each artifact it produced, a **durable locator** — a tracked `docs/audits/` path, or an
explicit harvest step naming what the integrator must copy and from where, with a hash. A packet
that names a job-scoped, session-scoped or otherwise ephemeral path does not satisfy it.

Shape questions this SEED deliberately does not answer, because they are the technical
architect's:

1. **Is the block validated, and where?** `gen_lane_contract.py check` is the packet's Layer-1
   shape gate and already enumerates mandatory sections; a required `ARTIFACTS:` block is a
   natural member. But a packet is written at the END of a lane while the contract is frozen at
   the START, so the gate that checks it may not be the gate that checks the contract.
2. **Can ephemerality be detected rather than promised?** A path under a job tmp dir, a session
   dir, or `%TEMP%` is recognisable by shape. Refusing on a matched shape is cheap and the escape
   is the durable path the block is asking for — the same conservative posture `[#629]`'s
   predicate takes.
3. **What about a lane that legitimately produces nothing?** `NONE` must be declarable, exactly as
   a write-scope declares `NONE`, or the block becomes a box every lane fills with noise.
4. **Does this generalise past lanes?** The orchestrator seat, the derivation passes and the terra
   rounds all produce artifacts and none is a lane. The ledger makes the same observation about
   cost attribution: *"a total that counted only manifest lanes would be precise and wrong."*

## Status

SEED — filed 2026-09-01 from operator direction as a **mechanism candidate**, per ADR-111's
CANDIDATE → intake → ratification route. Its carrier row is deliberately unborn. Awaiting
technical-architect triage on questions 1–4.
