---
intake-id: 61
status: READY
origin: operator universalization-v2 direction, stated verbatim at the 2026-08-28 window close (TO-NEXT-ARCHITECT-2026-08-28 theme 10); filed under PHASE0-CONTRACT-2026-08-28 item 0f as the phase's one intake birth
consumers: `deploy/manifest-v*.yaml` (the carrier declaration this intake adds a component to); `protocols/HANDOFF_PROCESS.md` (the engine spec whose version a consumer would pin); W3-4 / W3-5 `instantiate-methodology`; `[#559]` (kernel); `[#611]` (v7 minimal-bundle package); `ecosystem/deployed-versions.yaml` (the existing per-repo deployed-version record this reuses)
---

# The handoff engine becomes a deployable, versioned carrier

## Problem / motivation

Every consumer repo is meant to carry its own `docs/{intake, handoffs, decisions, audits,
archive}` so that **every project can run its own handoff**. That half is understood and partly
built. The half with no home is the **engine**: the assembler, the probe gate, the seal-identity
check, the boot contract. Today the engine is hub-local by construction — it is a set of hub
scripts and a hub spec — so a consumer repo that carries the folders still cannot run a handoff
without the hub reaching in.

The operator's direction is explicit and is quoted rather than paraphrased: the engine **stays
hub-owned, versioned, referenced and DEPLOYED from the hub**, so that **consumers know which
engine version they run**.

That last clause is the whole requirement. A consumer running an unknown engine version is the
version-drift disease the fleet has already measured in three other places — it is why
`ecosystem/deployed-versions.yaml` exists for the methodology corpus, and why
`reconciled_with:` edges exist for specs. The handoff engine has neither.

## What is already true (so this intake does not re-litigate settled ground)

- `deploy/manifest-v*.yaml` already carries a `components:[]` model with a `roster`, and the
  deploy tool already ships components to a consumer. A new component is an extension of a
  working mechanism, not a new mechanism.
- `ecosystem/deployed-versions.yaml` already records a per-repo deployed methodology-corpus
  version, written by the deploy runbook and read by the `deployed_methodology_version` audit
  check. The "which version do I run" question already has a shape that works.
- `HANDOFF_PROCESS.md` is already a versioned spec inside `_SPEC_REGISTRY`, so the
  `reconciled_versions` gate already knows how to fail a drifted dependent.
- W3-4 / W3-5 (`instantiate-methodology`) already scaffold a consumer's folder set.

The new scope is **only** the engine becoming a carrier: what gets shipped, how a consumer
records the version it received, and what fails when the two drift.

## Open questions for ratification

1. **What, exactly, is "the engine"?** The assembler (`gen_handoff.py`), the probe gate, the
   seal-identity check and the boot contract are candidates. A carrier that ships all of the hub's
   handoff scripts would ship hub-only assumptions with them; one that ships too little leaves a
   consumer unable to cut a bundle. The boundary is the decision.
2. **Does the engine ship as code, or as a declared dependency?** Copy-with-hash (the
   `CLAUDE-FLOOR.md` pattern, already proven and already gated by `floor-hash-verify`) versus a
   consumer-side pin to a hub release tag. These have different failure modes: a stale copy is
   detectable, a stale pin is not.
3. **Where does a consumer record its engine version?** Reusing `deployed-versions.yaml` avoids a
   second registry; a separate field or file avoids conflating corpus version with engine version,
   which can legitimately diverge.
4. **What is the refusal?** A consumer whose engine version does not match what the hub deployed
   should fail somewhere. Deciding *where* that check lives — hub-side fleet check, consumer-side
   gate, or both — determines whether it has teeth on a repo the hub is not currently looking at.
5. **Layer-2 boundary check.** ADR-28/36 hold that no hub script drives state in a child repo.
   A DEPLOYED engine is carried, then run BY the consumer — this intake reads that as consistent,
   and the ratification should confirm it rather than let it pass unexamined.

## Explicitly out of scope

Authoring the engine's v7 content — that is `[#611]`. This intake is about the carrier and its
version legibility, not about what the bundle contains.
