<!-- scope: meta -->

# ADR-69 — Cross-repo audit reach model: a Layer-2 read-only runner, not per-repo ports

**Status:** Accepted — 2026-06-02, **Path A** (operator-confirmed; post-hoc record of the reach model already implemented across the registration + structural-enforcement sessions — not a new architecture choice).
**Records:** the BACKLOG #44 reach decision; pairs with the #29 closure (the runner is implemented).
**Related:** ADR-28 (three-layer model — Layer 2 never executes in child repos), ADR-36 (audit-tool architecture — `.dev-knowledge` as read-only ecosystem auditor), ADR-38 A6 (the seven-file standard the runner audits), ADR-61 (ephemeral read-only worktrees), BACKLOG #72 (the residual sliver).

## Context

`audit.py`'s governance checks (`ALL_CHECKS`) must reach the four child repos so drift against the ADR-38 standard is caught without a manual per-repo sweep. BACKLOG #44 framed the open question as **how** the checks reach child repos, with three candidate models:

1. **Per-repo port** — copy the check code into each child repo, run locally at each repo's own commit time.
2. **Cross-repo runner** — one runner in `.dev-knowledge` iterates the registered repos, reads each read-only, reports centrally.
3. **Governance-only** — the auditor only ever checks `.dev-knowledge`; child repos are out of reach.

The choice was made implicitly across the implementing sessions (the cross-repo `run` command, the `ecosystem/` registry, the per-repo registration of corp-ops/corp-sca). This ADR records that decision explicitly so BACKLOG #44 closes against a written reach model rather than against implementation alone.

## Decision

**The reach model is the cross-repo runner (option 2), Layer-2 read-only.**

- `audit.py run` discovers the registered repos from `ecosystem/` (`discover_repos()`), runs the full `ALL_CHECKS` suite against each, and produces a per-repo PASS/FAIL compliance matrix (`docs/audits/<date>-ecosystem-audit.md`).
- The runner is **read-only on every child repo** (ADR-36 contract; ADR-28 Layer-2 invariant — Layer 2 never executes or mutates a child). It **writes only into `.dev-knowledge`**: the report, the regenerated `ecosystem/index.yaml`, and per-repo `state.yaml`/`history`. No child repo carries any `.dev-knowledge` tooling (option 1 rejected — it would duplicate the check code into every repo and drift).
- **Commit-time enforcement stays self-only.** The `audit-health` pre-commit gate runs `ALL_CHECKS` against `.dev-knowledge` itself and blocks only `.dev-knowledge` commits. A child repo's conformance is surfaced by `audit run` (on-demand or scheduled), **not** at the child's own commit time — by design, since Layer 2 does not install gates into child repos.

## Consequences

- **Positive:** one command produces the ecosystem compliance report; the check code lives in exactly one place; the read-only contract is structurally true (the runner never writes outside `.dev-knowledge`); a newly registered repo is covered automatically by the next `run`.
- **The residual sliver (BACKLOG #72):** because commit-time enforcement is self-only, an orphan or drift *beside a child repo* is caught by a full `audit run`, never at that child's commit time. Closing the gap needs a scheduled/automated cross-repo run (ADR-68 night agent is the natural host). Tracked as #72; not closed here.
- **Coverage depends on registration:** the runner only reaches *registered* repos. Registration is the single coverage lever (the corp-ops/corp-sca registration session existed precisely to close a silent coverage gap).

## Alternatives considered

- **Per-repo port** — rejected: duplicates check code into every child, re-introduces the cross-repo drift the auditor exists to catch, and would require Layer 2 to install tooling into child repos (ADR-28 violation).
- **Governance-only** — rejected: leaves child-repo drift entirely uncaught, defeating the auditor's cross-repo purpose (VISION "Auditor").
- **Council convene** — not taken: a reach-model record for an already-implemented, operator-confirmed mechanism; Path A per the ADR-65/66 precedent.

## References

- `scripts/audit.py` (`cmd_run`, `discover_repos`, `audit_repo`, `ALL_CHECKS`)
- `docs/decisions/ADR-28-three-layer-architecture.md`, `ADR-36-audit-tool-architecture.md`, `ADR-38-universal-repo-architecture.md`
- `ecosystem/index.yaml` (the registry the runner iterates)
- BACKLOG #72 (commit-time cross-repo orphan detection — the residual)
