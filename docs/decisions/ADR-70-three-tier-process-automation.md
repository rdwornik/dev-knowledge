<!-- scope: meta -->

# ADR-70 — Three-tier self-enforcing process layer: native primitives, scheduled baseline, episodic Workflows

**Status:** Accepted — 2026-06-02. AI Council verdict (2026-06-02) + the operator's three-tier synthesis. This ADR is the **capture** of that decision; nothing is built by it — the build sequence lives in the BACKLOG (see Consequences).
**Records:** the decision to make `.dev-knowledge`'s own *process* layer enforced-not-remembered, structured across three tiers by tool fit.
**Supersedes:** the earlier "evidence-ledger" custom-file design — a hand-rolled ledger file tracking done-vs-open work. Dropped: git (the `closes [#N]` commit convention) is the capture backbone; no custom ledger file is built.
**Related:** ADR-28 (three-layer model — Layer 2 never executes in child repos), ADR-36 (audit-tool architecture), ADR-65 (git is the technical record, JOURNAL the business record — the capture model this ADR generalizes), ADR-67 (AI-Council loop — the heavy-*decision* analog Tier 3 is paired with), ADR-68 (night agent — the natural host for the scheduled Tier 2 run), ADR-69 (cross-repo audit reach — the `audit.py run` Tier 2 leans on). BACKLOG #13/#8/#12/#72/#4 (the Tier-1/2 build units), #73/#74/#75 (the net-new build units).

## Context

**The cobbler's-children diagnosis.** `.dev-knowledge` machine-enforces the *structure* of every repo it governs — the seven-file canonical set, the BACKLOG story-map schema, the dot-prefix/visibility rules, the freshness cadence — each behind an `audit.py` check or a pre-commit gate. But its own *process* layer (close what you finished, promote lessons to enforced rules, review at session boundaries, lint before commit) ran on **memory and discipline**, not on tools. The methodology held the artifacts it governs to an enforced-not-remembered bar it did not apply to itself. The recurring symptom: large arcs satisfy pre-existing backlog items without ever closing them (the arc commits name their own scope, never `closes [#N]`), so the backlog accrues done-but-open items until a manual git-verified groom retires them (the 2026-06-02 groom retired six such items).

**Two corrected over-swings.** Designing the fix surfaced two symmetric failures, both pattern-matching rather than judgment:
1. **Over-building custom machinery** — the first design was a bespoke "evidence-ledger" file plus the scripts to maintain it, re-implementing what git's commit history (`closes [#N]`, ADR-65) already records.
2. **Over-correcting by dismissing Workflows** — having been burned by over-building, the reflex swung to "Dynamic Workflows are too heavy, skip them," which would have left the genuinely heavy episodic work (deep cross-repo audits, large migrations, checked-twice work) with no home.

Both are the same error — placing a tool by reflex instead of by fit. The correction is to place each capability at the tier whose tool actually fits it.

**The Council verdict (2026-06-02)** ratified the three-tier shape: native primitives for the always-on lifecycle, the existing scheduled audit for the baseline, and Dynamic Workflows reserved for heavy/episodic work — explicitly *not* a new custom subsystem.

## Decision

A **three-tier self-enforcing process layer**, each tier placed by tool fit. Scope of this ADR: `.dev-knowledge`, additive only — capture, not construction.

### Tier 1 — always-on lifecycle (native primitives only)
The per-session/per-commit loop, built from primitives that already exist — no custom subsystem:
- **Git as the capture backbone** — the `closes [#N]` commit convention *is* the ledger (ADR-65). **No custom ledger file** (this is the evidence-ledger supersession).
- **A propose-closures skill, invoked by the Stop hook** — reuses `audit.py` + git to detect done-but-open backlog items at session boundaries and *propose* closures; friction-calibrated (proposes, does not auto-close).
- **The existing `/boot`** as the session-start review primitive.
- **A pre-commit lint gate** (the version-pinned ruff hook — BACKLOG #13).
- **A lesson-promotion skill** — moves captured lessons toward enforced rules (the #4 lessons-feedback-loop machinery).

All of Tier 1 bundles as **one methodology plugin**, installed across all repos — a single install propagates the lifecycle to every repo rather than re-deriving it per repo.

### Tier 2 — scheduled baseline
The existing `audit.py run` (ADR-69 cross-repo reach) run **headless on a schedule** → a `fleet-health.md` digest. The natural host is the ADR-68 night agent. No new auditing machinery — Tier 2 is a cadence wrapper around the runner that already exists.

### Tier 3 — heavy / episodic
**Dynamic Workflows** for work that genuinely warrants fan-out: deep cross-repo or large-repo audits, big migrations/rollouts, and checked-twice (adversarially-verified) work. **Invoked explicitly, scoped first** — never the default, never always-on.

### Escalation rule (added to the decision ladder)
A **Dynamic Workflow is the heavy-*execution* analog of the AI Council** (ADR-67, the heavy-*decision* analog). The decision ladder gains a symmetric execution rung: most execution runs inline; escalate to a scoped Dynamic Workflow when the work is heavy, cross-repo/large, or must be checked twice — the same way a heavy *decision* escalates to the Council.

## Consequences

- **What becomes enforced (was remembered):** session-boundary closure proposal (Stop-hook skill), lint-before-commit (pre-commit gate), lesson→rule promotion (skill), and the scheduled fleet baseline. The process layer is held to the same enforced-not-remembered bar the methodology imposes on the artifacts it governs.
- **One install point:** bundling Tier 1 as a plugin means the lifecycle propagates to every repo in one step, not by per-repo re-derivation — and updates ship the same way.
- **Token-cost caveat on Tier 3:** Dynamic Workflows fan out across many agents and can consume a large token budget. They are opt-in and scoped-first **by design** — the cost is the reason Tier 3 is episodic, not always-on. Escalating to a Workflow is a deliberate decision, like convening the Council.
- **Capture precedes construction:** this ADR records the decision; **the build sequence lives in the BACKLOG** (Tier-1/2 units annotated `refs ADR-70` on #13/#8/#12/#72/#4; net-new units #73 plugin-bundle / #74 escalation-rule-codification / #75 first scoped corp-monorepo Workflow). Nothing is built here — recording-before-building is itself the discipline the architecture exists to enforce.
- **Layer-2 invariant preserved:** Tier 1's plugin installs *into* each repo's own runtime, but the scheduled Tier 2 audit and any Tier 3 cross-repo Workflow remain read-only on child repos per ADR-28/36/69 — capture and audit, never mutate-from-Layer-2.

## Alternatives considered

- **Custom evidence-ledger file** (the prior design) — **superseded.** Re-implements git's commit history; adds a hand-maintained surface that itself drifts (the very failure mode the layer exists to prevent). Git + `closes [#N]` already is the ledger.
- **Skip Dynamic Workflows as "too heavy"** — rejected. Leaves heavy episodic work (deep audits, migrations, checked-twice) homeless; the token cost is managed by making Tier 3 explicit and scoped, not by refusing the tool.
- **One monolithic always-on automation** — rejected. Conflates friction profiles: the lifecycle must be cheap and constant (Tier 1), the baseline periodic (Tier 2), the heavy work rare and deliberate (Tier 3). Collapsing them either makes the cheap path expensive or the heavy path reflexive.

## References

- AI Council verdict 2026-06-02 (three-tier process automation) + the operator's three-tier synthesis
- ADR-65 (git technical record / JOURNAL business record), ADR-67 (Council loop — decision analog), ADR-68 (night agent — Tier 2 host), ADR-69 (`audit.py run` cross-repo reach — Tier 2 runner)
- BACKLOG: #13 (ruff pre-commit gate), #8 (lifecycle hooks), #12 (evolution/lesson machinery), #72 (cross-repo orphan detection in scheduled run), #4 (lessons feedback loop); #73/#74/#75 (net-new build units)
