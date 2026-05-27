---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
---

## Question: Should the handoff keep delivering invariants and discipline inside a self-contained document bundle, or move them to a stateful or harness-mediated layer that the bundle only references?

### Current State

- The current bundle is ~12 entries; full copies of VISION, PLAYBOOK, and ESSENTIALS account for roughly 60% of its size by the 2026-05-12 audit's estimate, and PLAYBOOK alone is ~94% of the 2026-05-25 bundle's markdown bytes (`ADR-45:54-58`; `wc -l` on `docs/handoffs/2026-05-25-dev-knowledge-session-sync/`).
- ADR-45 (2026-05-13) proposed collapsing the bundle to two files (MANIFEST + NEXT), delivering invariants via `@path` imports plus a sync-script verifier for the executor and operator-upload for the browser chat, and moving discipline enforcement into three mechanical gates (git pre-commit + PreToolUse hook + `/save`) calling one validator. It projected ~87% payload reduction and 96–99% convention adherence (`ADR-45:163-201,271-287`).
- ADR-45 was explored and not adopted; its supersession claim was formally withdrawn on 2026-05-25. ADR-42 v3.2 plus HANDOFF_PROCESS v3.3.3 remain canonical (`ADR-45:5-7,387-409`).
- The recorded rollback reason: the 2026-05-12 audit's "what works, preserve" finding — full invariants prevent norm drift, and the full bundle empirically caught a real architect fabrication (`ADR-45:21-31`).
- On 2026-05-25 the delivery model failed in a different way: full delivery occurred, yet internalization did not — the failure was not payload size (evidence `:91-99`).
- Governance currently classifies any bundle collapse as a methodology change requiring a formal ADR, and fences it behind an explicit operator-approved ADR-45 reopen (`07_ACTION_PLAN.md:104-108,134-135`).

### Questions

1. **Where should the invariants (VISION/PLAYBOOK/ESSENTIALS) live relative to the bundle?**
   - A: Full copies in every bundle (current).
   - B: Canonical in `.dev-knowledge`, reaching the executor by reference and the browser chat by operator-upload (the ADR-45 direction).
   - C: A single condensed anchor in the bundle, with full copies available on request.

2. **Where should discipline enforcement live?**
   - A: Prompt discipline plus reader judgment (current).
   - B: Mechanical gates where the actor can run them (executor-side hooks + validator), prose elsewhere.
   - C: A hybrid split — mechanical on the executor side, prose on the browser side.

3. **Does the 2026-05-25 evidence change the ADR-45 rollback calculus?**
   - A: No — internalization failed despite full delivery, so payload size is orthogonal; keep ADR-42.
   - B: Yes — bundle size and redundancy are part of why engagement fails; reopen ADR-45.
   - C: Partially — adopt the enforcement half (mechanical gates) without the payload-shrink half.

### Constraints

- The browser chat must end the session holding everything it needs to act (session self-containment); how that is achieved — full copy vs operator-upload vs condensed anchor — is what this debate decides (`ADR-45:80-86`).
- Full-invariant value was validated by the 2026-05-12 audit and explicitly not rolled back; any move away from full copies must answer that finding (evidence `:138`; `ADR-45:21-31`).
- Layer-2 invariant: orchestration/workflow scripts do not live in `.dev-knowledge`; only mechanical, non-sequencing work may (`ADR-28:15`; evidence `:159`).
- Bundle collapse requires an explicit operator-approved ADR-45 reopen and a formal ADR deliverable (`07_ACTION_PLAN.md:104-108,134-135`).
- Which specific documents are relevant is decided in Q2; how the receiver internalizes what is delivered is decided in Q1. This debate is the delivery and custody layer only.

### Adjacent concerns — handled in separate debates (not this one)

- Which content types are relevant → Q2.
- How the receiver internalizes whatever is delivered → Q1.
- Sender-side verification discipline → Q4.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/council-questions/2026-05-25-handoff-failures-evidence.md:91-99,138,159`
- ADR-45 design + rollback + withdrawal: `docs/decisions/ADR-45-handoff-architecture-v4.md:5-7,21-31,54-58,80-86,163-201,271-287,387-409`
- Governance fence on collapse: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/07_ACTION_PLAN.md:104-108,134-135`
- Layer-2 invariant: `docs/decisions/ADR-28-three-layer-architecture.md:15`

### What a usable answer looks like

A decision on the delivery/custody layer, recorded either as a formal ADR-45 reopen (new ADR or ADR-45 amendment) if the bundle abstraction changes, or as a BACKLOG entry with revisit-criteria if the status quo holds. This is the concern the operator framed as "methodology-level, requiring architectural deliberation, not incremental tuning"; "keep the document bundle, with rationale" is a legitimate outcome.
