# Residual — 2026-08-08-dev-knowledge-architect — the part the repo does not already encode

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
Read P7 and P4 for what the gate says right now; this section says only which classes are
STANDING and which would be NEW, so the block can be triaged rather than re-litigated.

STANDING, each with a home that explains it:
  * the undeclared prose-edge family against the handoff spec (ADR-88 FC2) — a dispositioned
    class, not a defect; every member is a doc that references HANDOFF_PROCESS without a
    declared `reconciled_with`.
  * the closed-but-present backlog drift on the row the batch-2 consolidation arc left open —
    dispositioned, and the disposition names the matcher false-positive as its reason, not the
    row's state (`docs/audits/2026-08-07-technical-batch-2-lessons.md`; JOURNAL 2026-08-07 (k)).
  * the malformed `reconciled_with` on the CONTRIBUTING template — carried under its own row.
  * the backlog-accretion locus on the Grok row — dispositioned against that row's peg.
  * the review-artifact tally gap on one batch-1 lane artifact — advisory by the [#480] P3
    ruling; the hard pre-push leg is deliberately deferred.
  * the legacy first-parent spine entries that predate the prevent organ.

NEW would be anything outside that list.

The `[stale]` disposition class is P7's to report; if it reports any, they are decorations to
review under the ADR-75 rule, and reviewing them is a decision, not a cleanup.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Closed this window: [#501] (report-only recorder, closed on push-run evidence), [#503]
(doc-currency sweep), [#504] (block_ff_push fail-closed claims), [#429] (portable worktree
provisioning), [#490] (parity manifest), [#320] (fleet backup posture). Born: [#507] [#508]
[#509] [#510] [#511] [#512].

Landed as doctrine rather than rows: ADR-110's batch protocol ran twice — batch 1 and batch 2,
both with archived packets under `docs/audits/`; STANDING_RULINGS gained sections D, E and F
(F1–F6) plus B5/B6/B7; HANDOFF_PROCESS went 6.0.1 → 6.1.0 with two boundary invariants at the
cut; the ADR-85 amendment's hard leg moved to pre-push; the Ch8 routing matrix landed and was
then amended to key on context load. `templates/prompt-template.md` reached v1.11.

Landed on the morning of the cut, after the night window sealed: the night branch was
integrated to `main`, and intake #27's ledger was re-pegged and extended — six spent
`DEFERRED(batch 2 …)` pegs replaced, the library-research memo's §9 applied as two new ledger
rows plus two amendments, and items 34/36 annotated. Zero rows born by that arc.

Still open and load-bearing: [#505] (the batch protocol's own row — clause 2 is measured but
unresolved), [#502] (mutmut unblocked, three blockers cleared, still zero mutant numbers),
[#506] (the whole-set grooming arc). Detail: JOURNAL 2026-08-07 entries (a)–(l) and
2026-08-08 (a), and `docs/audits/2026-08-08-technical-successor-prep.md`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
1. Batch 3's composition, under a cap whose denominator is itself unruled. The ≤1/4
   process-lane cap is width-dependent: batch 2 planned width 6 as 5+1 and RAN at width 3, where
   floor(3/4)=0 process lanes are permitted — so it exceeded, retroactively, a cap it was planned
   to satisfy. The proposal on the table (evaluate against DISPATCHED width, report the
   close-width delta in the packet) was RATIFIED by the operator at this bundle's supplement —
   and is still **unlanded**. What remains is not a decision but the landing: the ratified
   wording has no repo home yet (the architect's own A7(a) names intake #27 + Ch8 as the
   destinations). Land it before sizing batch 3, or the same thing happens again.
   Context: `docs/audits/2026-08-07-technical-batch-2-lessons.md` §3.2; ratification in
   `SUPPLEMENT.md` (`OPERATOR RATIFIED: 3.2 YES`).

2. [#505] clause 2 — per batch or per integration? Measured for the first time and the answer
   depends entirely on the unit: 7 by the per-batch reading (falsified), exactly 2 by the
   per-integration reading (met). A precise replacement sentence exists, and the operator
   RATIFIED it at this bundle's supplement — so this too is now a landing, not a fork: the
   two-number wording (per-seam and per-batch) owes a home at the [#505] row + Ch8 per A7(b).
   §3.3 of the same file; ratified, unlanded.

3. The ADR-87 residual the routing matrix opened. The matrix puts model AND effort on the
   architect's dispatch line; ADR-87 puts model on CC's side. A population boundary was declared
   rather than either text edited, and the equilibrium table plus its §2 restatement still read
   as architect-excluded on the dispatch act itself. **The fork closed at this bundle's
   supplement:** A7(c) records the population boundary as RATIFIED — the architect states the
   session's boot tier, CC routes sub-steps inside it — and the descriptive ADR-87 amendment as
   **authorized and unlanded**. So what travels is not the question but the write: the amendment
   section owes an ADR-87 home, and amending the routing matrix again still does not discharge it.

4. The six W-rows have been re-pegged — what they were re-pegged TO is now the question. Items
   13/14/15/16/21/24 of intake #27 read `DEFERRED(batch 2 …)` against an event that had already
   finished with zero W-items in it; the morning of this cut replaced that with a peg naming the
   W-wave batch and its precondition. That is bookkeeping, not a decision: nobody has ruled when
   the W-wave batch runs, or whether it runs at all as a batch. Two of the six additionally
   moved underneath: W-5 was scoped against a 410s suite that xdist adoption has already cut,
   and W-4's `.github/workflows/` single-owner is now a real file that a live row already
   targets.

5. The consumer lanes' shared blocker, which nobody has retired. All three of batch 2's wave-2
   lanes were carried for one stated reason — the satellite repo lacks the enforcement organs the
   lane would need — and nothing in this window deployed organs to a satellite. Batch 3 plans
   into the same condition unless the premise is re-witnessed or a lane is accepted without them.

6. win-tooling has no `origin` remote and 14 branches of real work live on one disk. Named as
   the highest-value item on the operator list because it is the only one whose failure mode is
   losing work. **The fork is closed** — the operator ruled **private-remote** at this bundle's
   supplement. It is now execution owed to the win-tooling S-list (A7(e)'s destination), and it
   is the one carried item whose delay is measured in lost work rather than lost tempo.

7. How an immutable bundle with a bad seal gets retired. A 2026-08-01 bundle's internal slug
   names a different (also existing) directory, so `check-seal-identity` fails every
   `pre-commit run --all-files` sweep, and `docs/handoffs/` is immutable. This is a rule gap, not
   a cleanup.

8. One ordering proposal is recorded but unratified: land [#396] before [#512], because the
   reverse order produces five copies of one `GIT_DIR` scrub. It sits in intake #27's Sequencing
   note rather than in `protocols/STANDING_RULINGS.md`, deliberately — that register carries
   rulings ratified in chat, and this one has not been. Ratifying it is one line.

Sheets, not decisions: the batch-3 candidate pool and the full carried-decision list are in
`docs/audits/2026-08-08-technical-successor-prep.md` §3 and §5. They are retrieval — this seat
cuts them.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
