---
intake-id: 26
status: ACCEPTED
origin: "Layer-1 architect, session 2026-08-06-dev-knowledge-architect, 2026-08-06"
decided-by: "operator GO on SESSION PLAN v2 §3 (2026-08-06) — acceptance granted in-session; this document formalizes that ruling as pipeline input, it does not re-open it"
disposition: active
note: "Class: functional. Provenance (ruled, do-not-relitigate): 2026-08-06 consolidation window — supplement ADDENDUM \"Parallel-management architecture RULED\" + predecessor ratification AM-1/AM-2; red-teamed by predecessor riders."
---

# Parallel multi-agent execution system — batch protocol as versioned repo artifacts

## Problem

Parallel multi-agent execution today depends on seat memory: the batch shape (lanes, contracts, budgets, integrator, teardown) is known in chat, not in the repo. Consequences, all witnessed: unclosed parallel work (the operator's #1 pain — stale worktrees, unmerged lane branches), per-lane environment errors (bare `pytest` inheriting the primary tree's `VIRTUAL_ENV` — V-1 lesson iv), and zero portability of the way-of-working to a fresh seat. The system must be stable, methodologized, universal — repo-encoded, memory-free.

## Scope — Track 1 (this intake's build surface)

Encode the batch protocol as versioned artifacts on CC-native primitives (`claude --worktree`, agents view, native `/batch` — adopt-native ruling stands):

1. **PLAYBOOK §** — the batch protocol: ONE plan → N file-disjoint lanes → ONE integrator; frozen per-lane contracts + V-2 decision budgets; `uv run --locked` mandatory per lane; commit-and-STOP, never self-merge; serial integration from the primary; exactly 2 operator touches per batch (GO · end-of-batch packet).
2. **Project-scoped `.claude/commands/`** — lane-boot and integrator commands so no seat re-derives the shape.
3. **Handoff-bundle pointer** — successor bundles point at the protocol, never restate it.
4. **Hygiene organ** — WARN on stale worktrees (mechanized weekly prune stays).
5. **Lane/branch-prefix enum** — validator-checked naming.
6. **Parameterized by lane count (AM-2i):** drilled at 3, designed for 4–10; provisioning, board view, integrator queue assume N, never three.
7. **Refuse-to-finish integrator checklist (AM-2ii), encoded in the artifacts themselves** — structurally unable to close while open: every lane branch merged-or-explicitly-abandoned · full suite once on the merged result · `git worktree list` == primary only · manifest/packet archived.

## Scope — Track 2 (evaluation gate, no build)

30-min Vibe Kanban eval (`bloop.vibe-kanban`), operator-parallel during the batch-1 drill; PASS criteria pre-named (in-IDE tasks/logs/diffs · full lifecycle incl. worktree CLEANUP verified · Codex on one card · headless server as VS Code task); version pinned in win-tooling config-as-code. Verdict wanted BEFORE the wide batch.

## Non-goals

- No provider-agnostic execution layer (that is intake #25 / W-10 — separate pipeline).
- No bespoke board or hand-rolled `/batch-*` (rejected with reasons; herdr watch-listed).
- No gate promotion of [#501] (Free tier, private repo — report-only stands).
- No re-scope of [#429]: its live body owns FLEET worktree portability (portable seed-manifest + per-worktree venv) — a distinct, complementary concern. This intake is HUB-scoped protocol encoding. Cross-reference both ways; do not merge the scopes.

## Births proposed (backlog rows)

- **[#5xx] Batch-protocol encoding (Track 1, items 1–7 above)** — [P1][M] · footprint: `protocols/PLAYBOOK.md`, `.claude/commands/`, handoff templates/generator pointer, hygiene organ site · refs: this intake, [#429] (cross-ref only), ADR-<parallel-execution WoW> · done when: a fresh seat runs a full batch from repo artifacts alone; batch-1 executes under it with exactly 2 operator touches; hygiene WARN and branch-prefix enum are validator-checked; the refuse-to-finish checklist is mechanical.
- **Track 2 births nothing** — the eval's ADOPT verdict (if PASS) files its own follow-up.

## Acceptance criterion for this intake

Both births' pipeline stages exist: ADR cut and accepted, row(s) filed and regenerated into BACKLOG, protocol row executable with a frozen done-contract. The drill (batch 1) is the protocol's test — TDD at doctrine level.
