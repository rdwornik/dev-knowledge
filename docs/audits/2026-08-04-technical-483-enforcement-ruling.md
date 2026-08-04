# [#483] enforcement ruling — `preflight_contract` locator verification

**Date:** 2026-08-04
**Ruled by:** architect
**Row:** `[#483]` — *`preflight_contract` is adopted but ungated — rule whether locator verification becomes a gate*
**Status:** RULED — advisory-first; hard-gating deferred with a named evidence bar
**Record class:** ruling record. The row carries a pointer; this file carries the record.

---

## Why this file exists rather than the row

Every task file in `tasks/` is exactly one row line (222 of 222), and
`gen_task_tree.py --emit-source` reassembles `BACKLOG.md` from that line — so the row is
structurally unable to hold a multi-clause ruling, and at ~1100 characters it would cross the
`doc_rot` length threshold if it tried. The standing rule applies: **the row carries a pointer,
the record carries the record.**

**ADR promotion is deferred deliberately.** An ADR written now would ratify an *advisory interim
state*. The ADR moment is the hard-gate flip: when R3's evidence bar is met, that decision
arrives with data behind it and is worth ratifying. Judgment ceremony must not multiply.

---

## The ruling (verbatim)

> **R1  DISCRIMINATION-FIRST (binding precondition).** The backlog-id leg gains
> assertion-vs-citation discrimination BEFORE any gate wiring. Evidence:
> first production run — 11/11 flagged ids were correct historical citations
> (ids in tables headed "closed", plus provenance mentions), 0 real staleness.
> A gate wired today REDs every handoff bundle by construction.
>
> **R2  ROLE RULE.** An [#id] occurrence is an ASSERTION (claims the row is OPEN) only
> in forward-committing surfaces: emitted prompts/contracts, plan documents,
> and OPEN-claiming BACKLOG references. It is a CITATION (no open-claim) in
> historical narration: closed-tables, provenance clauses ("since [#436]"),
> JOURNAL/LESSONS entries, docs/audits/ and docs/handoffs/ artifacts.
> Sub-question (b) is thereby ruled: docs/audits/ and docs/handoffs/ are
> citation-role surfaces — never gated for id-staleness.
>
> **R3  WIRING POINT — advisory first, hard-gate deferred with the gap named**
> (ADR-81(d) explicit deferral). After FR-3b lands, wire the discriminating
> check as an ADVISORY leg in ALL_CHECKS over assertion-role occurrences only.
> Hard-gating is DEFERRED pending measured evidence: zero false positives over
> two consecutive windows, reported at each seal. Named gap that keeps this
> honest: the tool cannot catch a citation on the WRONG line (limit (i)) —
> it verifies id-liveness of assertions, not correctness of placement; hard
> enforcement must not claim otherwise.

---

## R1's evidence, re-derived — and a figure that has already moved

The "11" was **reproduced live** before being built against, not quoted. Re-running the tool over
`docs/handoffs/2026-08-04-dev-knowledge-architect/` today yields **19** flags, not 11 — because
`[#481]` and `[#482]` were closed earlier the same day (FR-1 and FR-2). Removing their 8
occurrences reproduces **11 exactly**, which confirms R1's figure at its own moment and
establishes that **11 is a point-in-time count, not a constant**.

| bundle file | flags today | of which `[#481]`/`[#482]` | flags at ruling time |
|---|---|---|---|
| `HANDOFF_BOOT.md` | 2 | 2 | 0 |
| `PASTE_THIS.md` | 6 | 2 | 4 |
| `PROBES.md` | 1 | 0 | 1 |
| `RESIDUAL.md` | 6 | 2 | 4 |
| `SUPPLEMENT.md` | 4 | 2 | 2 |
| **total** | **19** | **8** | **11** |

Any later citation of these numbers must name which moment it means.

---

## R2 made mechanical — the two layers, and what each was measured to be worth

**Layer 1 — surface path class.** `docs/audits/`, `docs/handoffs/`, `JOURNAL.md`, `LESSONS*.md`
are citation-role wholesale. Measured over the tracked corpus: **4810 of 7178 `[#id]`
occurrences, 67%**. This layer alone takes the handoff bundle to zero.

Why intake / protocols / ADRs are citation-role too — measured, not assumed:

| surface | `[#id]` occurrences | naming a non-open id |
|---|---|---|
| `docs/intake/` | 167 | 99 (59%) |
| `protocols/` | 79 | 45 (56%) |
| `docs/decisions/` | 214 | 111 (51%) |

Treating these as assertion-role would fire ~255 flags on day one, all narration.

**Layer 2 — in-line context**, for surfaces not wholly citation-role. The field **value** is
assertion-role; reason prose after the em-dash, and backtick-quoted spans, are citation.

**Ordering is load-bearing.** Measured progression on the live `BACKLOG.md`:

| rule | flags | why |
|---|---|---|
| naive whole-fragment scan | **24** | conflates `kill-candidates: none — <reason citing a closed id>` with a real kill-candidate |
| field value only (split on em-dash) | **2** | reason prose correctly excluded |
| **strip backticks FIRST, then match** | **1** | catches the row whose own prose quotes `` `kill-candidates: #370` `` — this repo's known convention-quoting false-positive class |

The survivor is a **true positive**: row `[#310]`'s kill-candidate names `#292`, which is closed.

---

## What this ruling does NOT authorise

- **No hard gate.** R3 defers it pending zero false positives over two consecutive windows,
  reported at each seal. The leg lands WARN-tier and must never FAIL.
- **No fix of the one live finding.** Row `[#310]`'s spent kill-candidate is the advisory leg's
  first production finding; it routes to FR-8a grooming rather than being swept up mid-arc.
- **No claim about placement.** R3's named gap stands: this verifies id-*liveness* of assertions,
  not correctness of *placement*. A citation on the wrong line still passes — `:3381` and `:3429`
  are both real lines in a 3800-line file.
