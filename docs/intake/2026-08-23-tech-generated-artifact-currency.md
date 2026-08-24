---
intake-id: 42
status: DRAFT
origin: lane L4 (`dashboard-commit-path`), 2026-08-23 — surfaced while executing ruling R1 on `[#171]` leg 1
consumed-by:
---

# Generated-artifact currency — one artifact is committed-generated and ungated, and the class has no uniform rule

## Problem / motivation

This repo commits generated artifacts on purpose: ADR-86 rejected generate-on-demand because "the
value is a committed artifact whose history shows conformance drift over time." A committed
generated file is a **trust surface** — a reader opens it and believes it.

Every committed-generated artifact in this repo is guarded by a `--check` regen-and-diff
pre-commit hook that refuses a stale copy — `codemap-freshness`, `toc-freshness-playbook`,
`roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`,
`intake-index-freshness`, `check_task_tree_coherence` for `BACKLOG.md`. **Exactly one is not:
`ecosystem/conformance.{md,html}`.** `gen_dashboard.py --check` exists and is armed nowhere.
`ARCHITECTURE.md` Ch2 already names it "the lone ungated committed-generated surface in this
repo"; it is R3 finding **F5**.

The consequence was measured at `aeec0fd1`: the dashboard was **4 days** stale, sitting behind 42
first-parent landings, while asserting in its own header that it was current-by-construction.
Lane L4 corrected the header (ADR-86 amendment, 2026-08-23) and armed a ship-gate staleness WARN
against that measured baseline. **Neither act gives the class a rule.** The next
committed-generated artifact will be a per-artifact judgment call again, and the one artifact that
is ungated stays ungated by omission rather than by decision.

What happens if this stays unaddressed: the repo keeps two different, undeclared answers to "how
does a committed generated artifact stay current?" — a pre-commit `--check` for seven of them, and
a post-hoc ship-gate WARN for the eighth — with no doctrine saying which is right when, and no
`# rule:` marker either can bind to (the freshness leg ships under a temporary
`doc-code-edge.yaml` exemption for exactly this reason).

## Scenarios (+1 view)

- As the operator I open `ecosystem/conformance.html` to answer "did the intakes pass their gate?"
  It renders cleanly, says nothing about being out of date beyond a commit date I have to reason
  about myself, and describes a repo state from several landings ago. I act on it.
- As an executor I add a ninth committed-generated artifact. Nothing tells me whether it owes a
  pre-commit `--check`, a ship-gate freshness WARN, both, or neither — so I copy whichever
  neighbour I happened to read.
- As a reviewer I try to bind the new staleness leg to a `coverage_scope` rule-ID and find the
  rule exists only inside an immutable ADR amendment, so the check ships exempt.

## Functional requirements

- **Must:** a single written answer to *how a committed generated artifact is kept current*, in a
  living doc a `# rule:` marker can bind to — so the leg's temporary exemption can convert.
- **Must:** a decision on whether `gen_dashboard.py --check` is armed (F5), and if not, why this
  artifact is the exception.
- **Should:** cover the whole class rather than the dashboard alone — the rule should say what a
  *new* committed-generated artifact owes on the day it is created.
- **Should:** say how the two mechanisms relate. They answer different questions (`--check`:
  do the committed bytes match a regeneration? freshness: is the committed copy current with its
  inputs?) and a HEAD-pinned artifact cannot use the first as a gate at all.
- **Could:** generalize the freshness registry beyond n=1 — the module already takes a registry.

## Acceptance criteria (ex-ante)

1. A named section in a living doc states the rule for committed-generated artifact currency, and
   `ecosystem/doc-code-edge.yaml`'s `generated_artifact_freshness` entry has moved from `exempt:`
   to `coverage_scope:` with a `# rule:` marker pointing at it.
2. Every committed-generated artifact in the repo is either covered by an armed mechanism or
   carries a recorded, reasoned exception naming who decided.
3. F5 is closed — `gen_dashboard.py --check` is armed, or its non-arming is a recorded decision
   rather than an omission.
4. Running the rule against a deliberately-stale tree produces a signal (ADR-81 leg (e): observed
   firing, not observed presence).

## Non-goals

- Re-opening ADR-86's committed-vs-on-demand decision, or its 2026-08-23 amendment. Both are
  settled; this is about keeping the committed copy current, not about whether to commit it.
- Making the freshness leg RED. That is a separate act with its own ruling.
- Implementing ADR-80 §3's self-committing writer policy. Ruled out for this artifact by R1.

## Impact sketch (4+1 lite)

- **Logical:** one rule replacing an undeclared per-artifact convention; the `doc→code` edge
  becomes bindable.
- **Process:** possibly one more pre-commit gate (a commit-time tax on artifacts whose inputs
  churn — the reason L4 chose the ship-gate for its own leg, and the trade-off the rule must make
  explicitly rather than by accident).
- **Development:** `scripts/generated_artifact_freshness.py` already takes a registry; adding
  artifacts is data, not code.
- **Physical:** none.

## Open questions

- Is HEAD-pinning (rendering HEAD's sha/date into the artifact) itself the defect? It is what makes
  `--check` unusable as a gate here. Dropping it would let the dashboard use the same mechanism as
  its seven siblings — but it would also cost the artifact its own provenance stamp. Technical
  architect's call; not answered here.
- Does the rule belong in PLAYBOOK, ARCHITECTURE Ch2, or an ADR? (The exemption converts only for a
  *living* doc.)
- Should the freshness registry cover artifacts that already have a `--check` gate — belt and
  braces — or only ungated ones?

## Status

DRAFT — filed by lane L4 (batch 2026-08-23) under R2 `banked = 0` (no task rows born this batch).
The BACKLOG row this work would need is specified in
`docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md` §7.
