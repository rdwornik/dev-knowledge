# Residual — 2026-07-25-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**The one that is not mechanically caught — read this first.** `[#381]` is **ruled, accepted and merged**
(ADR-104, fleet repository shape). ADR-104's own gate reads *"the E9 brake holds until this ADR is accepted
and merged"* — so the condition is **discharged**. `BACKLOG.md` still asserts the opposite in prose: the
`[E9]` preamble states the brake is live, and `[#409]`/`[#410]`/`[#411]` each still say building would
*"breach the [E9] brake."* No check covers this class — `validate_doc_claims` checks counts and rosters,
`validate_git_backlog` checks closed-but-present — so the stale-brake prose survives every gate. **Decide it
before planning anything in `[E9]` or `[S20]`; do not treat the BACKLOG prose as authority over the merged
ADR.** Note the ADR does *not* open everything: caveats (a)/(b) stand, and the first fold action still needs
its own precondition scan and ruling (ADR-104 §2/§5).

**Orphaned disposition (structural, this window).** `ecosystem/disposition-register.yaml` still carries a
`doc_rot` row keyed to `#262`, which Lane D closed this window. A register row outliving its ticket is the
ADR-75 decoration rule's target; it is **named here, not fixed** — removal is its own `chore(register)` arc,
and the operator has not been asked. `P7` gives the live answer.

**Standing and carried, with reasons — not new.** The register's long-lived rows are the `doc_rot`
backlog-accretion entries (`#344`, `#332`, `#278` — each with a `review_date` shelf-life so it cannot rot into
a paper suppression), the six `undeclared_edges` prose-edge rows to `handoff-process` (all ref `#241`), the
`no_ff_merges` journal-wrap/transcript-archive rows, and the `reconciled_versions` CONTRIBUTING-template row
(`#335`). None originated this window.

**Everything mechanical is the probes' answer.** Both read-only drift-checks were re-run at generation; their
verdicts are deliberately absent here. Re-derive live via `P4`/`P6`/`P7`/`P9` — a value quoted in this bundle
would be exactly the summary-bluffable artifact §5 bars.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail is in `JOURNAL.md` (newest-first) and `git log --first-parent`; this is the map only.

- **ADR-104 accepted + merged** — fleet repository shape: PARTIAL fold on engineering grounds, polyrepo
  mostly retained, corp-monorepo permanently outside; closes `[#381]`. The gate above turns on this.
- **`[#368]` closed** — VISION re-read lane.
- **Lane D — rulings, closures, filings** (one branch, four commits): closes `{#262, #295, #304, #339}`;
  files `#416`–`#420`; retires `[S23]`; appends an ADR-92 amendment marker (stale carrier count, body
  untouched per ADR-94); records an ADR-77 guard declaration; decomposes `[#348]` into `[#411]`/`[#412]`
  keeping only grooming; rules `[#403]`, `[#405]`, `[#402]` (DEPLOY, execution held).
- **`[#401]` clause (b) ruled** — `routing.py` PATH-REFUSAL is the ruled organ; the ticket **does not close**
  (a ruling, not a build; clause (a) is ai-council-side).
- **Weekly `logs/TOKEN-LOG.md` snapshot** — landed from a concurrent session, anchored retroactively.

**Shape of the window, for the architect:** it produced **rulings, not builds**. `[#402]`, `[#403]`,
`[#405]` and `[#401]`(b) are each ruled with no build window assigned — see §4.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**1. What the discharged brake actually unblocks — and in what order.** With `[#381]` ruled, `[#382]`
(desired-state data model, the highest-priority item in `[E9]`) has its `depends-on` satisfied and becomes the
head of the chain `#382 → #383 → #385`. Two things are *not* settled by ADR-104 and are the architect's:
(i) the **matrix width** — the ADR fixes the ruled tree count but explicitly leaves *which repos pair first
and how stages are sized* to `[#383]`; (ii) whether `#382` starts **now** or waits behind the operator's named
topic below. ADR-104 also leaves a candidate follow-up unfiled: a **governed-coverage metric** reporting any
ignored surface, which becomes load-bearing only if a future stage proposes `.gitignore` for real material.

**2. `[#419]` — the operator's named topic — is one shape wearing five ticket numbers.** Its `Done when`
("every standing routine has a named consumer and a consumption path") is *the same sentence* as the
`Done when` on `[#409]`, `[#410]`, `[#411]` (the three dictated night batches) and on `[#348]` (grooming as a
routine): each asks for **trigger · scope · consumption path**. The design call is whether that is **one
contract declared once** — a routine schema, which on the `[E9]` reading is a *row in the desired-state
contract* rather than a sixth registry — or five separate rulings. Two constraints bear on it: `[#270]`
(load-gauge) is the declared **first** element of any Tier-2 nightly layer under a standing operator ruling,
and `[#419]` shares `serialize-group: settings-json` with `[#348]`, so they cannot be executed in parallel.
Also note `[#419]`'s framing is deliberately narrow — *how routine output reaches a decision*, explicitly
**not** branch cleanup; the five unread conformance branches are its evidence, not its scope.

**3. The ruled-but-unbuilt queue has no home.** Four items now carry a ruling and no build window:
`[#402]` (DEPLOY ruled, execution held for its own window), `[#403]` (ruled to the carrier-set derivation
only), `[#405]` (ruled to organ (a)), `[#401]`(b) (ruled organ, no build; the ticket stays open until the
ai-council-side clause (a) ships too). Open question: does the way-of-working need an explicit *ruled,
awaiting build* state — or is a ruling recorded in a task line sufficient, and this is just normal queue?

**4. Two hazards observed and deliberately left unfiled — architect's call whether they are tickets.**
(a) **Concurrency in the primary checkout**: a live session branched, committed, merged `--no-ff` and pushed
in the primary tree *between* another session's state read and its next command. Nothing was lost, but only
because the lanes touched disjoint files. No organ guards HEAD mutation by a concurrent session; `[#417]`
(dirty-tree pathspec) is adjacent but does not cover it. (b) **Review-lane routing**: a governing-document arc
that touches a single `.yaml` reads as a MIXED diff, which routes to the CODE review profile and silently
skips every governing document — it was caught by hand this window, not by an organ.

**5. Sequencing tension to resolve explicitly.** `[#270]` is `P1` and gates the routine layer; `[#382]` is
`P1` and heads the newly-unblocked `[E9]` chain; `[#419]` is the operator-named topic and depends on neither
being finished. These are three credible "next" items with no encoded precedence between them —
`depends-on` records `#270 → #348` and `#382 → #383 → #385`, but nothing orders the three heads against each
other. That ordering is this session's first decomposition output, not a discovery to be re-made later.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
