<!-- scope: meta -->

# BACKLOG.md — Architecture Diagnosis (Council-ready, analysis-only)

> **DRAFT diagnosis — NO structural edits to `BACKLOG.md` were made.** Companion to
> `2026-05-31-methodology-canonical-audit.md`. Produced on branch
> `docs/methodology-canonical-audit-2026-05-31` (off `main` @ `22cf2de`).
> The architecture choice is **Council scope** (per the analysis in §G). This
> document verifies the problem, benchmarks organization against the reference's
> scannability principles, enumerates the full options space, recommends one, and
> drafts a leak-free Council brief. It does **not** author ADR-64, revive any
> deleted file, or re-route any cross-repo item.

**Subject:** `.dev-knowledge/BACKLOG.md` — 871 lines, 107 entries (66 open / 41 closed-in-place), 9 H2 sections.
**Operator framing:** priority-one, actionable surface; the operator (ADHD/autism; low-friction, deterministic, scannable systems) cannot see "what to do next" at a glance.

---

## §A — Problem verification (problem-doc observations: confirm / refute / add)

The problem doc's structural problems are treated as **observations, not constraints** — confirmed, refuted, or refined against live state.

| # | Problem-doc observation | Verdict | Live evidence |
|---|---|---|---|
| 1 | ~840 lines | **CONFIRMED (worse)** | **871** lines. |
| 2 | ~76 entries mixing open/closed | **CONFIRMED + REFINED** | **107** entries — **66 open, 41 (38%) closed/superseded/resolved retained in-place**. Doc undercounted (pre-arc). |
| 3 | No actionability ranking | **CONFIRMED** | P1/P2/P3 exist but there is **no "next-N" / "now" surface**; 66 open items spread across 9 sections. Nothing tells the operator where to start. |
| 4 | Taxonomy drift: Cross-stream >40% vs ADR-47 33% kill | **REFRAMED — partly refuted** | The **33% kill criterion was withdrawn from enforcement 2026-05-16 (ADR-48)** — it is *not a live constraint*; measuring against it is measuring a retired rule. The **real** taxonomy failure is sharper: the named stream taxonomy (A/B/C/D) routes **only 10/66 open (15%)**; **56% (37/66)** live in **4 session-arc-named sections**. The stream design has collapsed. |
| 5 | Cross-repo items violate ADR-41 ownership | **REFUTED as "violation" — REFRAMED as clutter** | ADR-41 explicitly *permits* child-repo items to "contribute to .dev-knowledge BACKLOG via Stream sections" OR live in the child repo's own BACKLOG. So this is **not** an ADR-41 violation. But ~20 open items are child-repo **execution** work (tier-deprecation, hyphen migration, retrofits) interleaved with `.dev-knowledge` methodology items — a routing/clutter problem. Re-homing them is ADR-41-permitted but is **execution (out of scope this run)**. |
| 6 | Multi-level dated notes dilute scannability | **CONFIRMED** | Many entries stack 2–4 dated `Status update` / `Scope update` / `Amendment` bullets (e.g. lines 169, 264, 303, 389, 408, 588, 685, 700, 730, 830). Current status is buried under supersession history — the direct cost of in-place closure. |
| 7 | (inferred) HTML-comment subsection delimiters / schema mutation | **CONFIRMED + ADDED** | Invisible HTML-comment section markers (lines 444, 504, 665). Entries have **drifted from ADR-41's "rigid, mutation-resistant" schema** — non-schema fields proliferate (`Order`, `Sub-items`, `Escalated`, `Effort`, `Acceptance criteria`, `Trigger`, multiple `Status update`s). Exactly the "mutation drift" ADR-41 warned against. |

**Added observations (beyond the problem doc):**

- **A1 — the methodology is self-contradictory about done-item disposition (root cause).** Three live, conflicting prescriptions: **ADR-41** (quarterly → archive done items to `BACKLOG-archive/YYYY-Q{N}.md`); **ADR-47-retained** (2026-05-16: "done items simply leave BACKLOG; their trace is git history; no ceremonial archive"); **PLAYBOOK §10** (still says "Archive all `done` items to `BACKLOG-archive/`" — i.e. teaches the *superseded* ADR-41 flow, naming a file CLAUDE.md §5 forbids recreating). The actual practice — **keep in-place with dated notes** — follows **none of the three**. (= audit finding C1.)
- **A2 — status vocabulary drift.** File uses `open/closed/superseded/resolved`; ADR-41 + ADR-47 + PLAYBOOK §10 all specify `open/in-progress/blocked/done`. (= C2.)
- **A3 — the premise that justified dropping the kill criteria has been falsified.** ADR-48/ADR-47 dropped the 300-line/15-per-stream/33% kill criteria *because* "the active file is small enough that the dilution risk doesn't materialise." The in-place-closure practice has falsified that premise (871 lines, 38% closed). The current state honors **neither** the kill-criteria world **nor** the lean-active-file world.

---

## §B — Taxonomy distribution (the hard numbers)

| Section group | Open | Share | Read |
|---|---|---|---|
| Named streams A/B/C/D (ADR-41 design) | 10 | **15%** | A=0, B=1, C=9, D=0 |
| Cross-stream / Ecosystem | 19 | 29% | the catch-all |
| 4 session-arc sections | 37 | **56%** | Cross-repo Naming (11), Hyphen (4), Tier-Deprecation (5), Council-Pipeline (17) |
| **Total open** | **66** | 100% | |

**Reading:** the file accreted one new H2 section per major session-arc instead of routing items into the stream model. Those 4 arc sections are **duplicate cross-stream buckets** distinguished only by *when* they were created. The ADR-41 stream taxonomy is effectively dead (15% coverage).

---

## §C — Root cause

The bloat is **not** primarily a grooming-discipline failure — it is a **methodology contradiction (A1)**. Because the canonical methodology (PLAYBOOK §10) still teaches the archive-to-file flow while ADR-47-retained says "done items leave," sessions had no unambiguous rule and defaulted to the safest-feeling option (keep everything in-place, annotate richly). 41 closed entries × multi-paragraph supersession notes = the bulk of the 871 lines. **Fixing the file without fixing the contradiction will re-bloat it.** The done-item-disposition decision is therefore the architectural keystone.

---

## §D — Benchmark vs reference scannability principles

The reference (`copilot-collections`) has **no backlog methodology** (confirmed) — only organizational principles transfer. What it *informs* vs what is **internal architecture (ADR + Council)**:

| Reference-informed (the *form*) | Internal architecture (ours alone — ADR/Council) |
|---|---|
| **Severity/priority-tiered, scannable surface** → a "Now/Next" actionable view | Done-item disposition (leave vs archive vs collapse) — touches ADR-41/47/48 |
| **Progressive disclosure** → current status visible; history collapsed/linked, not stacked inline | Section taxonomy (streams vs status×priority vs arc) — amends ADR-41 design |
| **Prioritized action-plan format** → top-of-file curated next-actions | Cross-repo item routing — ADR-41 ownership (execution) |
| **Separation of concerns** → open (actionable) separated from closed (record) | Whether to re-institute a size/health signal — re-touches ADR-48 |

The reference confirms the *goal* (a lean, scannable, priority-ranked actionable surface with history progressively disclosed) but supplies **no structure to copy**. Every structural decision below is ours.

---

## §E — Options matrix (full solution space)

Four coherent architectures (bundles of the disposition/taxonomy/surface axes). Per option: what changes · pains addressed (§A #) · ADR fit · amends a prior decision? · migration shape · reversal cost.

### Option 1 — Minimal truth-up (in-place, collapsed)
- **What changes:** keep all entries in-file; **collapse each closed entry to a one-line "[closed YYYY-MM-DD, <SHA>] — <title>"**; reconcile PLAYBOOK §10 + status vocabulary to docs. No archive, no taxonomy change, no actionability surface.
- **Pains:** 6, 7, partial 1/2. Does **not** fix 3 (actionability) or 4 (taxonomy).
- **ADR fit:** respects ADR-41 (single file, streams), ADR-48 (no new check), CLAUDE §5 (no revived file). **Still deviates from ADR-47-retained** ("done items *leave*") — keeps them, just shorter.
- **Amends prior decision?** No (but perpetuates the ADR-47 deviation explicitly).
- **Migration:** trivial, fully in-place. **Reversal cost: minutes** (git revert).

### Option 2 — Honor ADR-47 (lean active file) — *recommended candidate*
- **What changes:** (a) reconcile PLAYBOOK §10 + ADR-41 cross-ref + status vocabulary to ADR-47-retained (done items **leave**; git history is the record); (b) **remove the 41 closed/superseded/resolved entries** (their closing-commit SHAs are already embedded and preserved in git history); (c) add a **top-of-file "Now / Next" actionable surface** (curated pointer list of the ~5–8 items the operator will actually do next); (d) collapse the 4 session-arc sections into Cross-stream/Ecosystem (or a new **Stream E: ecosystem/tooling**) and re-route the 10 stream items.
- **Pains:** 1, 2, 3, 4, 6, 7 — all addressed. Resolves A1/A2/A3 (file finally matches a single coherent rule).
- **ADR fit:** **strongest** — *is* the ADR-47-retained convention; respects ADR-41 (single file, stream sections retained), ADR-48 (no new enforcement check), CLAUDE §5 (no revived archive). ADR-39 immutability **not implicated** — BACKLOG is Living/mutable (CLAUDE.md §4), and removed-entry evidence is preserved in git history (SHAs intact).
- **Amends prior decision?** **No.** Reconciling PLAYBOOK §10 is *truthing-up a doc to an existing decision*, not a new decision.
- **Migration:** incremental, one commit per batch; the removal step is git-revertable. **Reversal cost: low–moderate** (git revert restores entries verbatim).

### Option 3 — Two-file with revived archive
- **What changes:** re-institute a closed-item archive (`BACKLOG_ARCHIVE.md` **or** `docs/archive/backlog/YYYY-Q{N}.md`); move closed entries there; active file holds open items only. Re-aligns with the **original ADR-41** quarterly-archive flow and with PLAYBOOK §10's current text.
- **Pains:** 1, 2, 3, 6 — addressed (open file becomes lean); 4/7 still need taxonomy work.
- **ADR fit:** **CONTRADICTS ADR-47-retained** ("no ceremonial archive — git history is the record") and **⚠ AMENDS the 2026-05-16 `BACKLOG_ARCHIVE.md` deletion decision** + **CLAUDE.md §5** ("Do not recreate … BACKLOG_ARCHIVE.md"). This is effectively **rolling back the 2026-05-16 Council Simplification** for backlog archival.
- **Amends prior decision?** **YES — explicitly: the 2026-05-16 deletion + ADR-47 demotion + CLAUDE §5.** Requires Council ratification of the rollback; cannot be done as a truth-up.
- **Migration:** moderate (create file/folder + relocate 41 entries preserving SHAs/dates). **Reversal cost: moderate** (re-delete + git history).

### Option 4 — Status×Priority restructure (retire streams)
- **What changes:** replace the stream taxonomy with a **status-first layout** — `## Now` (curated next-actions) / `## Open — by priority` (P1→P3) / closed-items-elsewhere — since streams route only 15%. Pairs naturally with cross-repo re-homing (Option-D routing) to shrink the open set.
- **Pains:** 3, 4, 6, 7 — strongest on actionability + taxonomy.
- **ADR fit:** **amends ADR-41's stream-organization clause** (the `## Stream {name}` design); neutral on ADR-47/48 (pairs with disposition choice from Opt 2 or 3).
- **Amends prior decision?** **YES — ADR-41 stream-section design.**
- **Migration:** largest (re-bucket all 66 open + rewrite section headers). **Reversal cost: high.**

### Cross-cutting sub-decisions (compose with any option)
- **Cross-repo routing (D):** propose moving ~20 child-repo execution items to child repos' own BACKLOGs (ADR-41-permitted). **Execution → separate sessions, not this run.**
- **Schema re-rigidification (E):** restore the ADR-41 entry schema + `open/in-progress/blocked/done` vocabulary going forward. An **audit check** for it is gated by ADR-48's governance-admission rule (recurring real failure + fully automatable + low cost) — likely a doc-convention, not a check, for now.

---

## §F — Recommendation + proposed migration sequence (commits, NOT executed)

**Recommend Option 2 (honor ADR-47), composed with the "Now/Next" surface (B) and arc-section collapse (C); propose cross-repo routing (D) for separate sessions.**

Rationale: it is the **only option that resolves the root cause (A1) without amending a prior decision** — it makes the file *match the convention that already exists* (ADR-47-retained), fixes the strongest pains (1/2/3/4/6/7), and stays Layer-2/ADR-coherent. Option 1 leaves the actionability + taxonomy problems unfixed and perpetuates the ADR-47 deviation. Option 3 buys a lean file by **rolling back** the 2026-05-16 simplification (re-amends three artifacts) — viable but higher-ceremony and against the demotion's own reasoning. Option 4's actionability gains are real but it amends the ADR-41 stream design and carries the highest reversal cost; it is the **strong runner-up** and its `## Now` surface should be grafted into Option 2 regardless.

**Proposed incremental, revertable sequence (each a commit; none executed here):**
1. **Doc reconciliation (no BACKLOG change):** fix PLAYBOOK §10 (done items leave; strike the `BACKLOG-archive/` line), align ADR-41↔ADR-47 cross-ref, correct status vocabulary. *(Path-A-eligible — truth-up to existing decisions; arguably outside Council. But sequence it after the Council verdict so the disposition rule is settled first.)*
2. **Add `## Now / Next`** actionable surface at top of BACKLOG (additive, non-destructive).
3. **Groom-and-remove** the 41 closed/superseded/resolved entries — one commit per logical batch; closing SHAs already embedded; git history is the archive. Fully revertable.
4. **Collapse the 4 arc sections** into Cross-stream/Ecosystem (or new Stream E); re-route the 10 stream items.
5. **Propose** (separate sessions) child-repo execution items → child-repo BACKLOGs (ADR-41-permitted; execution).
6. **Restore the rigid entry schema + vocabulary** as a documented convention going forward; revisit an audit check only against ADR-48's admission rule.

Evidence preservation: every removed entry's closing-commit SHA + date is already in its text and in git history; **no SHAs or dates are lost** by removal (the prompt's evidence-preservation constraint is met by git, not by retention-in-file).

---

## §G — Route decision: **Council** (not Path A)

Per `AI_COUNCIL_PROCESS.md` § "When to convene" — Council is justified when **all** hold:

| Criterion | This decision |
|---|---|
| Architectural impact | **Yes** — the structure/lifecycle of a canonical governance file. |
| Multi-ADR ripple (≥2) | **Yes** — touches ADR-41 (mandate/schema/streams), ADR-47 (organization), ADR-48 (enforcement withdrawal), PLAYBOOK §10; Option 3 would amend the 2026-05-16 deletion + CLAUDE §5. |
| Reversal cost > 1 hr | **Yes** for Options 2–4. |

And it is **forward-looking with genuine optionality** (four viable architectures, real trade-offs, an amends-prior-decision tension) — which is precisely Council's domain and **not** the Path-A case. Path A (direct ADR by CC) was legitimate for ADR-62/63 because those were *post-hoc records of decisions already made + independently fresh-eyes-validated*; here **no decision has been made** and the choice is not forced. → **Council.** (This diagnosis is also a **live instance** of the open BACKLOG item *"AI Council convene-vs-Path-A decision criterion"* (line 863) — it exercises exactly that criterion.)

**Do NOT author ADR-64** (the resulting decision's ADR) here — it is the Council/operator's to write post-verdict.

### Leak-free Council brief (Stage-0 one-sentence problem statement)

> **What organization should `.dev-knowledge`'s single `BACKLOG.md` adopt for entry lifecycle (open- vs done-item disposition), section taxonomy, and an actionable-items surface, given 107 entries (66 open / 41 closed-in-place), a stream taxonomy currently routing 15% of open items, and the standing ADR-47/48 convention that done items leave the file?**

*Self-check (council-question-guide §Neutralizing bias): states the problem not an answer; no leading headline; no asker-leakage; the four options in §E become the ballot with "a different approach (name it)" as the explicit escape; the eliminating constraints are ADR-47/48 + CLAUDE §5 (no silent revival), solo-operator + single co-reader LLM scale, and Layer-2 read-only. A fast unanimous agreement would be surprising → not leading.*

When convened, the full brief uses the `AI_COUNCIL_PROCESS.md` Stage-1 decision-mode format: this sentence as `## Question`; §A/§B numbers as `### Current State`; §E options 1–4 (+ escape) as `### Questions`; the constraints above as `### Constraints`.

---

## Constraints honored (what this diagnosis did NOT do)

- **No edit to `BACKLOG.md`** — diagnosis + options + recommendation only.
- **No ADR-64**, no ADR authored.
- **No revived deleted file** — Option 3 explicitly flags that it would amend the 2026-05-16 `BACKLOG_ARCHIVE.md` deletion + CLAUDE §5.
- **No closed-entry evidence destroyed** — removal proposals rely on git history; embedded closing SHAs/dates preserved.
- **No cross-repo item moved** — re-homing is ADR-41-permitted but is execution; proposed for separate sessions only.
- **No other repo touched.**
