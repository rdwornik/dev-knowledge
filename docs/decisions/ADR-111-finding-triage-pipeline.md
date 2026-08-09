# ADR-111: The finding pipeline — every audit finding is triaged into exactly one of four outcomes

- **Status:** Proposed
- **Date:** 2026-08-09
- **Decision tier:** Architecture (Path A — architect ruling, ARC-2 consolidation contract Phase B, 2026-08-09)
- **Amends:** ADR-98 (§3 genre demarcation — see "What this changes in ADR-98" below; the amendment is NAMED rather than left as a silent second rule)
- **Related:** ADR-100 (§4 audit-vs-intake genre split — the half of this doctrine that is already law), ADR-65 (done-item disposition — the close-side sibling of this add-side rule), ADR-108 (§F backlog equilibrium is explicitly NOT ratified there; this ADR does not ratify it either), ADR-66 (story-map schema), ADR-70 (Tier-1 closure loop)
- **Intake:** none — this ADR is not intake-born. It is the standing rule that governs how findings *reach* an intake, and was ruled directly. Recorded explicitly so the ADR-98 traceability edge is not read as missing.
- **Decommission:** none
- **Source:** Architect ruling, ARC-2 consolidation contract Phase B (2026-08-09). Written after establishing, clause by clause, which parts of the proposed pipeline were **already law** — five of eight were, and this ADR deliberately cites rather than restates them.

## Context

The 2026-08-09 night batch produced **153 indexed findings and 38 requested rulings** across five
lane reports. Nothing in the corpus said what must happen to a finding. The available paths were,
in practice, exactly two: file a BACKLOG row, or let it sit in an immutable audit nobody re-reads.
The first inflates the open set; the second loses the finding.

That is measurable. N1 measured **birth rate, not close capacity, as the binding constraint** on
the backlog target (62 closes needed ≈ 37 batches at the measured net rate versus ~11 with births
held at zero), and the live open set stood at 194 rows. Meanwhile four of five lanes independently
re-derived gaps that **an already-open row already recorded** (`[#453]`) — a consumption failure
that a triage step with an OWNED outcome would have caught before any lane was dispatched.

**Most of the pipeline was already law and is not restated here.** Established before drafting:

- *An audit produces evidence, never decisions* — **ADR-100 §4**, verbatim: "**Audit = evidence
  *about* state. Intake (ADR-98) = a request to *change* state.** They are **separate genres with
  separate lifecycles.**"
- *REJECTED is a terminal intake status and the archive is its home* — **`docs/intake/README.md`
  §5**, verbatim: "**REJECTED (reason, kept)** — the technical architect declined it. The one-line
  `reason` is recorded and the doc **stays** (archived, not deleted) — rejections are knowledge,
  not garbage", and "Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
  `docs/intake/archive/`". **No new register and no new path is created by this ADR.**
- *An intake is operator-gated* — **ADR-98 §4**: "the **operator approves the draft intake doc
  before it lands**"; `ACCEPTED` additionally requires `decided-by` + `disposition` (README §5).
- *Rows carry a Done-when and cite their parents* — **ADR-98 §3**: "**Backlog epic** = the WORK —
  **1..n per accepted intake**; each epic entry **cites its intake-id + ADR-id(s)**", and
  "Acceptance criteria copy **VERBATIM** from the intake doc into the epic UAT".
- *Births are already back-pressured* — **PLAYBOOK "Filing backpressure (2026-07-08 ruling)"**: any
  commit adding a task id carries a `kill-candidates:` line, enforced by the
  `backlog-filing-backpressure` commit-msg hook.

**The gap is narrow and specific: the edge from a FINDING to any of those.** The corpus governs the
genres and the intake lifecycle; it has never governed what a finding may become.

## Decision

### 1. Every finding is triaged into exactly one of four outcomes

An audit finding is not actionable until it carries one of:

- **(a) OWNED** — an open row already covers it. **Attach the evidence to that row; birth nothing.**
- **(b) DISCHARGED** — already done, or already ruled. **Record it with its locator.** The locator is
  mandatory and must resolve; "we already do that" without a locator is not a discharge.
- **(c) CANDIDATE** — it needs a decision. It becomes, or joins, an **intake** — which is an idea
  that may be rejected, not a commitment.
- **(d) REJECTED** — recorded with its reason, and **not relitigated**.

**An audit whose findings are untriaged is incomplete.** This is a property of the audit, not of the
reader: producing 153 findings and no outcomes is an unfinished deliverable.

### 2. A finding may not become a backlog row without triage

The only path from a finding to a row runs through (c) → intake → ratification. A finding may not be
filed directly as a row. Outcomes (a), (b) and (d) exist precisely so that most findings never
approach the backlog: **a triage pass that routes most items to (c) has not triaged.**

### 3. Ratification is the birth authority, and it is recorded

An intake is **ratified or rejected**, and the ratification is the decision to implement. Ratifying
may still prove wrong — that is what testing is for; revertability, not certainty, is the standard
(ADR-108 §A item 2). Only a **ratified intake** births backlog rows, each with a Done-when.

### 4. What this changes in ADR-98, stated rather than left implicit

The ARC-2 contract's clause reads *"an intake may not become rows without an ADR"* — i.e. every
birth traces to an **accepted ADR**. **That conflicts with ratified ADR-98 §3**, which says an ADR
is "authored **only** when a reasonable person could choose otherwise **and** reversal is costly —
**0..n per intake** (an intake may force no ADR, or several)", while epics are "**1..n per accepted
intake**". Under ADR-98, an accepted intake with **zero** ADRs still births epics; live practice
matches it — intakes #16 and #26 were accepted by operator ruling recorded in `decided-by`, not by
ADR, and intake #25 was ratified the same way on 2026-08-09.

Requiring an ADR per birth would force ADRs at non-forks, which ADR-98 forbids in the same sentence.
**This ADR therefore does NOT adopt the ADR-mandatory form.** It ratifies the weaker, coherent rule:
**birth requires a ratified intake**; an ADR is required only where ADR-98's fork test is met. The
ratifying act — ADR or recorded operator ruling — is named in `decided-by` either way, which is what
makes the birth auditable.

**This is a deliberate departure from the contract's literal text, made because the literal text
contradicts a ratified ADR.** It is flagged as **OPERATOR-owed**: if the intent really is to make
an ADR mandatory for every birth, that is an amendment to ADR-98 §3 and should be ruled as one.

### 5. Birth rate is bounded — but the equilibrium form stays unratified

Outcomes (a), (b) and (d) are what make a bound achievable, and the add-side backpressure hook is
already live. The stronger claim — *"birth rate is bounded by demonstrated close capacity"* — is
**intake #22 §F ("backlog equilibrium")**, which **ADR-108 explicitly declares unratified and
"non-citable as ruled doctrine"**. This ADR does not ratify it either. It is named here so the next
reader can see the boundary rather than infer that a quantitative bound is in force.

## Consequences

**Easier.** A finding has somewhere to go that is not the backlog. The `[#453]` class — four lanes
re-measuring an open row — becomes a triage miss with a name, so it can be reported instead of
repeating. Discharges accumulate a citable locator set, which is the anti-rebuy mechanism.

**Harder, and deliberately so.** Every audit now owes a triage pass; the pass is real work and its
cost lands on the producer. A finding cannot be filed as a row in one step, which will feel slower
in exactly the moment the finding seems obvious.

**Unenforced, and this ADR does not pretend otherwise.** No organ checks that an audit's findings
are triaged, and none is built here. The nearest live mechanisms are adjacent, not equivalent:
`backlog-filing-backpressure` gates the *commit that adds a row*, not the *route the row took*; the
Tier-1 closure loop (ADR-70) works the close side. Whether this rule earns a gate is an n=2
question, per the repo's standing evidence discipline — **it should be measured on the next two
audits before any gate is proposed.** Until then this is doctrine a reviewer can cite, not a
refusal, and stating that is the honest limit.
