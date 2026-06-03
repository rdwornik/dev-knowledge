# 05 · What to do now

## Immediate objective

**The one move: BACKLOG #80 — research and internalize the shipped Dynamic Workflows
feature** (Claude Code, shipped 2026-05-28, *after the sender's knowledge cutoff*).
This is [P1] because it is the **foundation the rest of the agentic arc stands on**.
Scope: research + synthesis (docs work, not code). Internalize the six patterns
(classify-and-act, fan-out-synthesize, adversarial-verification, generate-and-filter,
tournament, loop-until-done) and the three failure modes they fix (agentic-laziness,
self-preferential-bias, goal-drift), then map them to our conformance/review needs.
**#80 mandates verifying against Anthropic's own docs first** — the two articles Rob
uploaded are the seed, not the authority. Land a research note + a pattern→use-case
mapping.

## Top priorities (from BACKLOG)

- **[#80] [P1][L]** — research the Dynamic Workflows feature (above). Prerequisite for
  #74, #75, #81. *Do this first.*
- **[#81] [P2][L]** — build the methodology-conformance Dynamic Workflow for
  `.dev-knowledge`: verifier-per-rule fan-out + a skeptic persona (suppresses false
  positives), run continuously via `/loop`, **read-only proposals only** (no
  auto-write — Layer-2 forbids the hub writing to siblings). The #77 doc-rot check
  becomes one verifier inside it. *This is the engine that keeps universalization from
  rotting once hand-tending stops — not a side-quest.*
- **[#82] [P3][M]** — per-repo agentic-review profiles (what agentic review each repo
  runs, on what cadence). Queued behind #81.
- **[#70] [P3][M]** — operationalize the AI-Council gated loop (ADR-67). The
  heavy-*decision* companion to the heavy-*execution* workflows above; gate lifted
  2026-06-02 (Phase-2 universalization complete), now actionable.
- **[#78] [P3][S]** — deferred docs-refresh: ARCHITECTURE "12 checks" hardcode →
  point at `audit.py checks`, and CLAUDE §11 ADR rotation to include ADR-71. **Do both
  in one genuine end-to-end re-read** (the freshness gate re-stamps `last_reviewed` on
  any edit — don't drive-by).

**The frame Rob named, hold it:** finish the agentic layer; run the handoff process
successively for *every* repo so the whole fleet reaches the top tier; keep the
dynamic files live so there are **no dead docs**; build the process/workflow for all
of it. "No dead docs" is exactly what #81 mechanizes.

## In-progress branches & repo state

- `main` — `d439969` (session-end tip; the work this bundle hands off).
- `docs/handoff-2026-06-03` — `81399a6` — **this handoff's branch** (Phase 1 + Phase 2
  commits). Merge it after the bundle is accepted; no other unmerged work.
- **Branch (handed-off state):** `main`  ·  **HEAD:** `d439969`
- **Working tree at generation:** clean

## Boundaries

- **Nothing is pushed**, and hook consumption uses **local relative paths**
  (`../.dev-knowledge`). This works *only* because the whole fleet is co-located on one
  Windows box. Push or relocate any repo and the `repo:` entries must swap to URLs or
  the hooks silently stop resolving.
- **Never run `codemap-generate --write` against a child repo** — it overwrites a
  curated hand-authored diagram with orphan dust. The `not generator-managed` marker is
  load-bearing.
- **#81 is read-only proposals only** — Layer-2 forbids the hub writing into siblings.
- Don't operationalize #70/#81 as code-execution in *this* repo's `scripts/` — Layer 2
  never executes; agentic workflows are authored/run, not committed as orchestration.

## How to choose

The order above is the sender's reasoned recommendation (#80 → #81 → #82, with #70 as
the decision-side companion). If you see a reason to reorder, **propose your choice
with rationale to Rob** — don't ask him to forced-rank. Operator energy is finite; your
job is reasoned pre-selection. Rob confirms or redirects.
