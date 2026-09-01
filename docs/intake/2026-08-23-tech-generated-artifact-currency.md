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

## AMENDMENT — 2026-09-01: `conformance.html` is MIGRATED, not deleted — and the consumer count in the direction is UNDERSTATED

> **Source:** operator direction, 2026-09-01 (the OBSERVABLE HARNESS), filed under
> *reconcile-before-birth*. Appended, not edited. **No file is moved, no row is born, and no
> artifact is retired by this amendment** — it records a direction and corrects one of its factual
> premises before that premise is acted on. This intake stays `DRAFT`.

### The direction

`ecosystem/conformance.html` is to be **MIGRATED, not deleted**. Its **one honest question** — the
one this intake already quotes in its own first scenario, *"did the intakes pass their gate?"* —
becomes a panel on the new dashboard; the live consumers are re-pointed; the file is then retired.
`ecosystem/trends.html` moves alongside it. The destination is a root `dashboard/` whose sanction is
**not granted** and is recorded as an open question on intake #38.

**Migrate-not-delete is the right call and this intake is the reason.** The artifact is a
**committed trust surface** — a reader opens it and believes it — and it is the single artifact
whose ungated status is this intake's entire subject. Deleting it would dissolve the question
rather than answer it.

### The correction: the direction names two consumers; there are at least four

The direction re-points *"the two live consumers (freshness tuple, #42)"*. Both are real:

1. **The freshness tuple** — `scripts/generated_artifact_freshness.py:147-148`, the
   `conformance-dashboard` entry, whose `outputs` tuple is
   `("ecosystem/conformance.md", "ecosystem/conformance.html")`.
2. **This intake**, whose first scenario is the honest question itself.

**Two more resolve, and they change the shape of the work:**

3. **`ARCHITECTURE.md` Ch2** carries the pointer in prose — *"Conformance dashboard →
   `ecosystem/conformance.md` (+ its HTML sibling `ecosystem/conformance.html`, operator addendum
   2026-08-19), generated by `scripts/gen_dashboard.py`"* — and `ARCHITECTURE.md` is a
   freshness-stamped canonical living doc, so a stale pointer there is a gated defect, not a typo.
4. **`[#171]`**, still **open**, whose done-when names `ecosystem/conformance.md` *and* the
   ARCHITECTURE Ch2 pointer. A migration that leaves the row untouched leaves an open row
   describing a surface that has moved. (`[#586]`, also open, records that regenerating
   `conformance.{md,html}` REDs a suite test — a fourth site that a migration touches.)

### The asymmetry that is the actual trap

**The direction retires the `.html`. The freshness tuple, ARCHITECTURE Ch2 and `[#171]` all key on
the `.md`.** They are one generator's two outputs (`scripts/gen_dashboard.py`), and nothing said
what becomes of the Markdown twin. Retiring only the HTML leaves the tuple **half-pointed** — an
`outputs` pair with one live member and one dead one — which is precisely the silent-narrowing
failure this intake exists to prevent. **The `.md`'s disposition must be ruled in the same act as
the `.html`'s, not after it.**

### What a migration does to THIS intake's own question

Recorded because it changes what "done" means here. This intake exists because
`ecosystem/conformance.{md,html}` is the **one** committed-generated artifact with no `--check`
gate. Its successor surface, `ecosystem/trends.html`, is **gitignored** (`.gitignore:84`) and
regenerated on demand. So if the atlas panel lands in a **gitignored** dashboard, the artifact
**leaves the committed-generated class altogether** — and this intake's question is **dissolved for
this artifact while remaining wide open for the class**. That is an acceptable outcome, but it is a
different outcome from the one the Acceptance criteria above describe, and it should be chosen
knowingly rather than arrived at. If instead the dashboard is **committed**, the artifact stays in
the class and this intake's rule is still owed — now for a surface at the root.

**Either way the class rule is still owed**, and no reading of the migration discharges it.
