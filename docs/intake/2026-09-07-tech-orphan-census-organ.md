---
intake-id: 86
status: DRAFT
origin: browser architect seat, 2026-09-07 — `to-cc/INBOX-dev-knowledge-2026-09-07-034.md` candidate C-H, ruled as the FIRST consumer of the one-graph landing in `to-cc/DECLARE-GRAPH-2026-09-07.md` §2; worked example `ecosystem/north-star.md`
consumed-by:
---

# Nothing asks "does this file have a consumer?" — so an orphan is invisible until someone trips over it

## Problem / motivation

`ecosystem/north-star.md` sat in the tree with zero consumers and no organ noticed. INBOX 034
measures *why*, and the answer is four separate holes rather than one missing check:

- **`consumer_at_landing` watches ONLY `docs/audits/`.** No organ asks the consumer question for
  `ecosystem/`, `templates/`, `protocols/` or `scripts/`.
- **The seal (`validate_hermetization`) polices the HOME of a new file, not whether anything USES
  it.** A file in the right place with no reader passes every gate we own.
- **`canonical_freshness` accepts TWO stamp shapes** — `[frontmatter]` and `[prose]` — which is
  exactly why `PLAYBOOK.md` and `ENVIRONMENT.md` look different at the top. The check tolerates the
  inconsistency instead of refusing it.
- **Templates have no consumer edge at all.** Nothing records which generator reads which template,
  so an unused template is not merely unnoticed — it is unrepresentable.

The sweep lanes S-08…S-13 are a one-time census over grep. A census finds today's orphans; it does
not stop tomorrow's. This intake is the standing organ the census is the fixture for.

## Scenarios (+1 view)

- As the operator, I add `ecosystem/north-star.md` and cite it nowhere. The next nightly Routine
  reports it as a WARN with its last content commit, and the scorecard's `orphans` line moves from
  0 to 1 — so I learn on day 1, not on the day someone happens to read the folder.
- As a lane, I add a template under `templates/` and wire no generator to it. The registry (U4)
  has no `source → generator` edge for it, so it is an orphan **by definition** and the WARN says
  which edge is missing rather than merely that the file is unloved.
- As the operator, twenty-two days after a WARN I have neither dispositioned nor removed the file.
  The organ turns FAIL and names the disposition path, so the decision is forced once — not
  re-noticed every night forever.
- As a seat, I disposition an orphan with a reason ("kept: browser paste source, no in-tree
  citer"). The register records it in the same shape today's WARNs use; no new surface is born.

## Functional requirements

- **Must:**
  - Every tracked file has ≥ 1 consumer — a citation in a doc / row / ADR / intake, a generator, a
    hook, a command, or a test — **or** is covered by a genre allowlist in the #73 grammar (e.g.
    the `docs/audits/` immutability class).
  - **Consumer edges are computed, never declared by hand.** Per `DECLARE-GRAPH` §1 the computation
    is a **query over FPG-1**, not a new edge set: in-degree 0 over citation / generation /
    execution / test / template edges ∧ not in a genre allowlist ∧ no TRACE trigger within the
    groom cadence → candidate.
  - Runs in the nightly Routine **and** at ship-gate. WARN on first sight, carrying the file's last
    content commit; a WARN older than the groom cadence (ADR-41, 21 d) becomes FAIL unless
    dispositioned with a reason.
  - Dispositions use the register shape today's WARNs already use — **no new surface**.
- **Should:**
  - Templates enter the derived-copies registry (U4) as `source → generator` edges, so a template
    with no generator is an orphan by construction.
  - `canonical_freshness` drops the `[prose]` stamp class; `PLAYBOOK.md` and `ENVIRONMENT.md`
    migrate to the frontmatter table every other canonical doc carries (a docs-only lane; S-09
    proposes the exact header).
  - Scorecard line `orphans (count)` — the number is visible, not felt.
- **Could:** a per-genre orphan breakdown, once the #73 grammar's genre → home map is fleet-wide.

## Acceptance criteria (ex-ante)

1. **The sweep's output is the fixture.** Every orphan S-08…S-13 found by grep, the query finds.
   Seeded as test cases, not eyeballed.
2. **The converse is a finding, not a bug.** Every orphan the query finds that the sweep missed is
   recorded as a finding against the sweep — `DECLARE-GRAPH`'s "consequence for tonight" clause,
   pinned as a test that asserts the disagreement is *reported*, never silently reconciled.
3. `ecosystem/north-star.md` at its pre-disposition state returns consumer count **0** and the
   ruled home under #73/D6.
4. A WARN older than 21 d with no disposition returns FAIL; the same WARN with a disposition
   returns WARN-dispositioned. Both directions fixture-tested — a gate that can only fail is not
   a cadence.
5. **The query reads FPG-1 and computes no edges of its own.** A test asserts the organ imports
   the graph rather than walking the tree; this is the Done-when of intake #40 applied to its first
   consumer, so a private computation here would defeat the landing it is meant to prove.
6. A genre-allowlisted file (an immutable audit) is never reported, and the allowlist is read from
   the #73 grammar rather than copied into this organ.

## Non-goals

- **Not a deletion engine.** The organ reports and escalates; retention is ruled by the operator
  and executed by the retention grammar. A-25's mechanical-only rule stands.
- **Not an LLM judgment.** The candidate formula is mechanical and explainable — see the intake
  filed from INBOX 035 for the bounded reader roles, and `DECLARE-GRAPH` §4 for the rule that no
  gate calls a model on its hot path.
- **Not a second census.** S-08…S-13 stay the one-time grep pass; this replaces the *repetition*
  of that pass, not the pass itself.
- **Not a new edge kind.** If the query needs an edge FPG-1 lacks, that edge is added to FPG-1.

## Impact sketch (4+1 lite)

- **Logical:** one query over the one graph; the orphan predicate lives beside the graph, not in
  `audit.py`.
- **Process:** a WARN → 21 d → FAIL cadence, matching ADR-41 groom; dispositions in the existing
  register.
- **Development:** a new `audit.py` check plus fixtures; U4 gains template `source → generator`
  rows; `canonical_freshness` loses a stamp class (a separate, docs-only migration).
- **Physical:** nightly Routine and ship-gate — no new runtime, no new store.

## Open questions

1. Does the stamp-shape unification ride this intake or split into its own docs-only lane? INBOX
   034 item 4 states the migration; it is a different blast radius from the organ.
2. Is `scripts/` in scope on day 1, or does the code layer wait for the FPG-1 code-layer hole (#40
   amendment 2026-08-31 §2 measured it at 21 nodes)?
3. Does the genre allowlist live in the #73 grammar file or in `config/catalog-schema.yaml` (the
   catalog intake's shape)? **Decide once, for both.**
4. Ship-gate as WARN-only, or FAIL-capable from the start? A FAIL leg at ship-gate is a different
   promise from a FAIL leg in the nightly.

## Status

DRAFT — filed 2026-09-07 by filings-N3 from INBOX 034, ruled as first consumer by
`DECLARE-GRAPH-2026-09-07` §2. Awaiting technical-architect triage and ratification. No carrier
row (ADR-111 §2).
