# D-queue for the 2026-08-26 session — the ruling-signalled open rows

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** d-queue-0826
- **What this is:** the queue of open rows whose NEXT actionable step is an operator/Council ruling — for the
  2026-08-26 review cluster. **LIST ONLY:** one line per id naming the ruling it waits for. No dispositions,
  no recommendations, no closures here.
- **Arc:** PROMPT P6 prep arc, branch `docs/p6-dated-pressure-prep`.

> **PREP, NOT EXECUTION.** Nothing in this list is ruled, closed, re-prioritized, or annotated in
> BACKLOG/`tasks/` by this arc.

**Derivation, stated honestly.** The commissioning prompt cites "the 26 ruling-signalled rows from the P10
groom". The P10 groom's own list is on **no committed surface** (searched: JOURNAL 2026-07-28 (a)–(m),
`docs/audits/`, the 2026-07-28 handoff bundle, `git log --all --grep P10` — the P10 probe is answer-free by
design, and per JOURNAL 2026-07-26 (h) its grooming output is deliberately derived state, never committed
prose). This list is therefore **re-derived live at 2026-07-28 HEAD**: a mechanical Done-when scan of the 147
open `tasks/` rows for ruling-shaped clauses (41 hits) followed by per-row adjudication down to
"next step is a ruling". After excluding the six rows this prep arc handles on their own surfaces — the drain
slice [#356]+[#358]–[#361] (drain-slice-prep artifact) and [#364] (cap option matrix) — the derivation yields
**exactly 26**. The equality with the operator's count is reconstructed, not verified against a committed
groom output; the 08-26 session should reconcile **id-by-id against this list**, not count-to-count.

---

## The 26, each with the ruling it waits for

1. **[#122]** Retire the PATH shim — waits for the operator's remove vs keep-for-defence-in-depth call.
2. **[#126]** Backpressure-loop pattern evaluation — waits for a go/no-go (or explicit drop) on the doctrine
   bounds, after a corp pilot result.
3. **[#153]** Enforcement-completeness pass — waits for two decisions: the invariant-#5 `--no-ff` scope
   boundary, and the `~/.claude`-reach question.
4. **[#162]** Vocab decision — waits for an ADR/ruling landing the term disambiguation across the enumerated
   surfaces.
5. **[#170]** Traceability-spine ADR — waits for the ADR defining the issue-ID↔commit linkage (and #168's
   ratified anchor).
6. **[#210]** Journal-wrap no-ff WARNs — waits for the shape decision: standing exemption vs moving the wrap
   behind a `--no-ff` arc.
7. **[#323]** Design question (`hub_hooks`) — waits for the carry-vs-freshness-only decision on
   `codemap-generate`/`toc-generate`.
8. **[#331]** Consumer BACKLOG schema adoption — waits for a per-consumer ruling: adopt-at-P6 vs
   accept-durable-divergence.
9. **[#346]** Two-tier new-path executor rule into `~/.claude` — waits for an explicit global-infra ruling
   (core-invariant #6 class) or a recorded permanent-defer.
10. **[#362]** The 49 dropped #242 guards — waits for per-guard carry / consciously-drop / supersede rulings,
    before any status-flip closes #242.
11. **[#370]** Ownership-model third state — waits for the scope ruling: is the marker/template/test work the
    `owner=user` ruling calls for in-row or a follow-on (operator's `/review-closures` call).
12. **[#371]** Consumer editor-config write-through — waits for the buy-vs-build fleet-template vehicle ADR
    (its recorded do-NOT-implement-bespoke constraint; see the sibling `.vscode` sizing artifact for the
    2026-08-13 half).
13. **[#393]** corp-sca rot review — waits for confirm-live-or-retire on the 3 candidates.
14. **[#397]** `scripts/` target structure — waits for adopt/reject on the mapped grouping (or
    flat-is-fine-with-reason).
15. **[#400]** The rosters ownership cell — waits for the ownership-model ruling to explicitly cover the
    hub-mandated-STRUCTURE / repo-owned-CONTENT cell (the half the `owner=user` ruling did not absorb).
16. **[#406]** Commit-time doc_rot surfacing — waits for the enforcement-point pick: nudge / pre-commit leg /
    accept-ship-gate-only.
17. **[#407]** Fleet Python style — waits for the functional-vs-OOP stance + naming-convention doctrine ruling
    (or deferred-with-reason).
18. **[#409]** Night batch: CODE review — waits for ruled-in-or-out as an ADR-105 routine (trigger, scope,
    consumption path).
19. **[#410]** Night batch: ARCHITECTURE review — waits for the same ruled-in-or-out.
20. **[#411]** Night batch: creative session + recurring Q&A cadence — waits for the same ruled-in-or-out.
21. **[#413]** Colors semantics interim — waits on the [#400]-family ownership ruling to re-ground the
    semantics (its own dated review is 2026-10-22, later than this cluster).
22. **[#414]** Self-acting-on-main incident family — waits for the organ pick (which guard(s) refuse an
    unanchored `main` change) or recorded permanent-defer.
23. **[#420]** Top-level `docs/archive/` — waits for kept-with-restated-charter vs dissolved-into-per-area-homes
    (with a destination per file).
24. **[#430]** Root `conftest.py` fleet-parity — waits for the admissibility ruling: is the consumer's root
    entry admissible or declared (limb (a) of its Done-when).
25. **[#435]** Intake #18 stewardship — waits for the ratification session: per-amendment A1–A11
    ADOPT/DEFER/REJECT with reasons (intake #19 §B rides it).
26. **[#443]** Planning-artifact rent rule — waits for, per uncovered class, a stated rent/binding rule or a
    recorded deliberately-not-a-rule with its reason.

## Excluded with reasons (so the reconciliation is checkable)

- **Handled by this prep arc's sibling artifacts:** [#356], [#358]–[#361] (the 2026-08-26 drain slice —
  drain-slice-prep), [#364] (cap option matrix).
- **Ruling already landed; residue is build/codification, not a ruling** (their Done-when text still names the
  ruling — the [E8] reconciliation-debt pattern, `BACKLOG.md:353`): [#347] (R3 ruled by delegation
  2026-07-26), [#389] (R6 ruled by delegation 2026-07-26; row text "R6 … UNRULED" is stale), [#401] (its
  ruling is recorded in-row), [#402] (RULED DEPLOY 2026-07-25, execution HELD at the 5-file bar), [#438]
  (posture in force; codification is the build), [#441] (launch-shape ruled 2026-07-28; PLAYBOOK text is the
  build), [#405]/[#403] (ruled 2026-07-25, build residue).
- **Build- or date-gated, not ruling-gated:** [#383]/[#385] (depends-on chain), [#387] (rewrite task),
  [#357] (census sweep), [#348] (gated on #270), [#270]/[#271], [#130], [#317] (buildable default without
  D1), [#327] (documentation build), [#419]/[#426] (declaration work; gated at ACTIVATION per ADR-105),
  [#433] (waits on the §6.2/§6.3 demonstrations, owner [#383]), [#388] (ruled HOLD at P3, 2026-07-28).
