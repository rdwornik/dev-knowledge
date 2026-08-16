# Lane k — [#293] cross-repo consumer seeding — execution packet

T_start: this dispatch's first tool call (2026-08-16), operator confirmation via two
AskUserQuestion rounds in-session: (1) materialize the missing contract and proceed with
/lane-boot, (2) proceed with all 8 ADR-104 consumer repos including corp-monorepo.

## OWNED-FILES manifest, as executed

Hub side (per contract): `tasks/293-consumer-runbook-fan-out.md` (this update),
`docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-contract.md` (step 0),
`docs/audits/README.md` (regen), this packet, `BACKLOG.md` (regen via
`gen_task_tree.py --emit-source`). Consumer side: exactly `docs/handoffs/README.md` in each
of the 8 ADR-104 non-hub members, written only inside a per-repo worktree/branch created for
this act (RULING-W shape), never the live checkout.

## Step 0 — COMMIT

Contract of record committed per I-D3 (docs(audits) commit, byte-identical diff verified
against `~/Downloads/CONTRACT-K-293-SEEDING.md`, materialized this session from
`PHASE2-MAX-PACK.md` §C's "LANE k (OPTIONAL — operator word)" block since Position 0 had
excluded lane k from the 12-lane split pending that word).

## Row read (row-is-the-spec)

`tasks/293-consumer-runbook-fan-out.md`: denominator is 8 (ADR-104 non-hub members, R6);
"Seeding stays OPERATOR-GATED, not executed" as of lane Q's prior STOP (`82d128f8`). This
lane's contract explicitly authorizes the cross-repo write lane Q's contract did not.

## Mechanism used (RULING-W, quoted)

`protocols/ESSENTIALS.md` / `docs/decisions/ADR-41-cross-session-backlog-architecture.md`
2026-07-18 entry: *"The hub MAY and SHOULD write into a consumer repo for
methodology/cleanup work. The only sanctioned write shape is: consumer worktree/branch →
report — the hub creates a separate git worktree/branch inside the consumer, makes its
edits there, then reports. Hard bounds: never a direct push into a live consumer checkout;
re-witness the consumer live before any edit."* Executed per repo as: `git fetch origin` →
`git worktree add <repo>/.worktrees/seed-handoffs-runbook -b docs/seed-handoffs-runbook
origin/main` → `scripts/seed_runbook.py --target-root <that worktree>` → commit → push →
`gh pr create` (never merged) → `git worktree remove` (no leftovers).

## Results — 7 of 8 seeded, 1 STOP-and-report

| Repo | Status | PR |
|---|---|---|
| demo-prep | seeded | https://github.com/rdwornik/demo-prep/pull/1 |
| corp-monorepo | seeded | https://github.com/rdwornik/corp-monorepo/pull/54 |
| corp-ops | seeded | https://github.com/rdwornik/corp-ops/pull/1 |
| corp-sca-time-automation | seeded | https://github.com/rdwornik/corp-sca-time-automation/pull/1 |
| life-architect | seeded | https://github.com/rdwornik/life-architect/pull/1 |
| terminal-setup | seeded | https://github.com/rdwornik/terminal-setup/pull/1 |
| win-tooling | seeded | https://github.com/rdwornik/win-tooling/pull/1 |
| ai-council | STOP-and-report | none opened |

None of the 7 PRs above were merged — each consumer's own merge discipline (operator GO,
`--no-ff`) governs integration, per RULING-W's hard bound.

## Why ai-council STOPs (quoted, not assumed)

Its own pre-commit hook `validate-docs-registry` refused the commit:

> `validate_docs_registry: refused -- unregistered new docs/ directory (#68): 'docs/handoffs/'
> is a new directory under docs/ that is neither a sanctioned taxonomy folder nor a registered
> live corpus (registries live in docs/audits/README.md). To register a live corpus: add an
> essence markdown at the parent root AND a row to the 'Live corpora' table in
> docs/audits/README.md naming the path, what it is, the ruling that keeps it there, its
> essence markdown, and its exit condition.`

This is exactly the contract's own named STOP condition ("STOP-and-report on any consumer
repo whose governance forbids the write"). Registering `docs/handoffs/` in ai-council's own
corpus registry is a decision for that repo's own maintainer/session — inventing a
registration on its behalf from the hub would be exactly the "invented path with no quoted
home" the OWNED-FILES discipline forbids, and would exceed this lane's OWNED-FILES manifest.
The worktree and empty branch were removed; nothing was left behind. Whoever owns ai-council's
`docs/audits/README.md` Live-corpora table registers `docs/handoffs/` there and re-runs the
seed; the mechanism (`scripts/seed_runbook.py`) needs no change.

## Decision budget (V-2), reported

- Escalation used: two AskUserQuestion rounds before any write, both operator-confirmed in
  session — (a) the contract file itself was missing (Position 0 had excluded lane k pending
  operator word) and needed to be materialized from `PHASE2-MAX-PACK.md` before it could be
  "read and executed"; (b) full 8-repo scope including corp-monorepo (ADR-104-flagged
  employer/pre-sales content) confirmed explicitly rather than assumed from the contract text
  alone.
- ai-council's STOP was decided per contract default (the contract's own line names this
  exact outcome for governance-refused writes) — not batched as a question, no operator
  judgment call needed to reach it.
- Environmental finding, recorded not disposed: this worktree's branch (`worktree-lane-k-293-
  seeding` provisioned as `worktree-worktree-lane-k-293-seeding`) and all 11 sibling batch-6
  lanes carry the same double `worktree-worktree-` prefix, failing the grammar gate Position 0
  validated against the intended names. Also: `journal_spine_anchor` initially FAILed on this
  worktree's stale JOURNAL.md (branched before main's D-1v2 merge `43cd1cee` landed); resolved
  by a plain fast-forward sync to main (verified main's own JOURNAL.md already anchors it
  correctly first — lane tree-lag, not a real gap; no `SKIP=` used).

## Targeted checks

Hub side: `audit-index-freshness` and `audit-health` fired at the step-0 commit (heavy
concurrent load from all 12 batch-6 lanes running simultaneously made both gates slow, not
wrong — no `SKIP=`, no `--no-verify`, retried to completion). Consumer side: each repo's own
commit hooks fired natively; 7 passed, 1 (ai-council) correctly refused per its own gate.

## Done-when, clause by clause vs delivered

Row's Done-when: "each onboarded consumer carries the seeded runbook (per-repo tracked,
n≥1 recorded)."

- Delivered: 0/8 → **7/8** seeded and tracked (open PR per repo, not yet merged into any
  consumer's own main — the count reflects PRs opened, matching the row's own
  onboarding-in-progress framing; merge-in is each consumer's own decision). ai-council stays
  at 0/1 pending its own docs-registry registration.

## Deviations self-reported

- None from the contract's own instructions. Two decision points were escalated rather than
  decided-and-reported, both because they were prerequisite/scope questions this lane could
  not answer from its own contract text alone (see decision budget above) — not routine
  in-contract choices.

STOPPED.
