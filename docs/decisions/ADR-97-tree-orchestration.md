# ADR-97: Tree orchestration — architect-root + epic-chat lanes

- **Status:** Accepted
- **Date:** 2026-07-05
- **Decision tier:** Architecture (Path A — direct architect ruling; designed in browser 2026-07-05, root pre-accepted via `tree-orchestration-design-spec.md`; no Council transcript, like ADR-87/90/92/95)
- **Related:** ADR-87 (Architect↔CC equilibrium contract — epic lanes consume it identically when delegating to CC), PLAYBOOK §8 (worktree discipline + parallel-session rules this extends), HANDOFF_PROCESS §14 (the EPIC handoff / EPIC RETURN types this decision introduces), ADR-82 (handoff process v5 — the assembler `gen_handoff.py --mode epic` reuses)
- **Source:** operator design spec `tree-orchestration-design-spec.md` (browser, 2026-07-05); formalizes the 2026-07-04 lived precedent (Slice-B primary lane ∥ Phase-0 worktree lane, architect as serial gate)
- **Decommission:** none

## Context

Multi-chat work to date ran on ad-hoc convention: one architect chat plus occasional parallel worktree lanes, with the architect as the serial integration gate. On 2026-07-04 this pattern was lived successfully (Slice-B primary lane in parallel with a Phase-0 worktree lane), but nothing recorded who may merge, who owns worktree lifecycle, how parallelism is adjudicated, or what contract a parallel lane boots from. Left unrecorded, the pattern drifts: lanes self-merge, boundaries are discovered at merge-collision time instead of ruled at spawn, and authority (ADRs, backlog structure, closure) leaks downward.

Existing invariants already point the way — PLAYBOOK §8's worktree discipline, "parallel sessions never self-merge", and ADR-87's equilibrium contract. This ADR extends them into an explicit orchestration model; it is not a new regime.

## Decision

Adopt a **tree-shaped multi-chat orchestration model** with three tiers:

- **Root — Architect chat (exactly one).** Owns: vision/backlog integrity, ADRs, epic decomposition, the **parallelism ruling** (which epics may run concurrently, adjudicated by file-boundary disjointness), plan review at epic level, **serial integration** (all merges to main, one at a time, `--no-ff`), backlog structure, closure declaration, and worktree provision/teardown.
- **Branch — Epic chats (one browser chat per epic, one worktree per epic).** Own one epic end-to-end inside their worktree: decompose into user stories, author CC delegations, review CC's produced work, keep their epic's BACKLOG checkboxes current. They commit-and-STOP on the epic branch. They NEVER: merge to main, write ADRs, restructure the backlog, create/destroy worktrees, or touch files outside their declared file-boundary.
- **Leaf — user stories.** Executed by CC sessions inside the epic's worktree, serialized on the epic branch (commit-per-story).

### Explicit rulings (deviations from the operator's raw sketch)

- **Worktree per EPIC, not per user story.** Intra-epic stories usually share files; per-story worktrees explode orphan management and break the 2–3-stream cap. Stories serialize within the epic worktree. Exception path: a genuinely disjoint, large story → the epic chat escalates to the architect for a sub-worktree (architect provisions; never self-provisioned).
- **Concurrency cap: 2–3 epic lanes.** The architect's review + serial-merge bandwidth is the deliberate bottleneck; more lanes queue at the gate, they don't add throughput.
- **BACKLOG single-writer for structure.** Epic chats may tick checkboxes ONLY inside their own epic block (keeps the Stop-gate's BACKLOG leg working, minimizes merge conflicts). Structural changes (new stories, re-scoping, closures) travel in the EPIC RETURN and are applied by the architect at integration.
- **JOURNAL merges chronologically at integration** (both entries kept) — the already-accepted seam.

### Handoff contracts

Two new handoff types carry the model (specified normatively in HANDOFF_PROCESS §14, additive to §13):

- **§14a EPIC handoff (architect → epic chat):** a scope-contract generated per epic at lane spawn — epic scope (BACKLOG slice), the ex-ante immutable epic done-contract, root-provisioned worktree + branch (`epic/<slug>`, relative paths only), the explicit **FILE-BOUNDARY** (the parallelism ruling made mechanical — concurrent epics MUST have disjoint boundaries; a needed file outside the boundary = escalate, don't touch), escalation rules, and the refusal list.
- **§14b EPIC RETURN handoff (epic chat → architect):** the lane's closing report, required before any merge — branch commits + state, contract-vs-outcome per story (closure claimed on the hard metric, never "committed"), self-adjudications + ARCHITECT-REVIEW-PENDING items, proposed BACKLOG delta, and the merge-readiness checklist. The architect then reviews vs contract → serial `--no-ff` merge → applies the backlog delta → declares closure → teardown (worktree remove + prune + branch -d + orphan check). The loop closes at the root, always.

### Invariants (the load-bearing five)

1. **Only the root merges to main.** One merge at a time. (Generalizes the existing never-self-merge rule from CC sessions to whole browser lanes.)
2. **Disjointness is adjudicated at spawn, not discovered at merge.** Overlapping epics are serialized by ruling, before any lane starts.
3. **Worktree lifecycle is root-owned.** Lanes work inside; they never provision or tear down.
4. **Authority does not descend.** ADRs, backlog structure, parallelism rulings, closure declarations live at the root only. The epic lane's anti-drift guard is its own handoff's refusal list.
5. **Every lane boots from a generated handoff and closes with a return.** No lane runs on chat-prose instructions; the contract is the artifact.

## Consequences

- **Easier:** parallel epic work becomes contract-driven — a lane's scope, boundary, and refusals are a generated artifact, not chat prose; merge collisions are ruled out at spawn instead of untangled at integration; the architect's serial gate stays the single point of backlog/ADR/closure authority.
- **Cost / mechanism:** templates `templates/handoff/epic/{EPIC_BOOT,EPIC_RETURN}.md.tmpl` + `gen_handoff.py --mode epic` (reuses the v5 assembler; probes stay, scoped to the epic boundary). The deliberate 2–3-lane cap trades raw parallelism for review integrity.
- **What this does NOT change:** CC's three-layer position (browser → hub → CC) — epic chats are still L1 browsers with the same stance, scoped down. The v5 architect handoff (§13) is unchanged for root-to-root succession. The equilibrium contract (ADR-87) — epic lanes consume it identically when delegating to CC.

## Alternatives considered

- **Worktree per user story** (the raw sketch). Rejected: intra-epic stories share files; per-story worktrees multiply orphan-cleanup surface and break the concurrency cap that keeps the architect's review bandwidth honest.
- **Uncapped lane concurrency.** Rejected: merges are serial at the root by invariant #1, so lanes beyond 2–3 queue at the gate without adding throughput while multiplying boundary-ruling and review load.
- **Epic lanes as backlog co-writers.** Rejected: concurrent structural writers to BACKLOG.md guarantee merge conflicts and break the Stop-gate's BACKLOG leg; checkbox-only writes inside the lane's own epic block keep the seam narrow, with structure traveling via the EPIC RETURN.
- **Leave the pattern as lived convention.** Rejected: the 2026-07-04 precedent worked because one operator held the whole model in his head; unrecorded, the next parallel run re-derives (or violates) the merge/authority/boundary rules.
