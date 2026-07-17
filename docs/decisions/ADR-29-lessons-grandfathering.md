# ADR-29: LESSONS.md Grandfathering Under Scope Tagging

**Status:** Accepted
**Date:** 2026-04-21
**Type:** Binding — derivative of ADR-27 Council decision
**Parent decision:** ADR-27 (Council #27 scope tagging)

## Context

ADR-27 mandates `<!-- scope: X -->` tags on all sections. LESSONS.md is append-only (CLAUDE.md rule: "NEVER edit old entries. NEVER delete. Only append new entries at the bottom"). Phase 2 audit lists LESSONS.md as a single section "Entries" with `[hybrid]` tag because existing 123 lines mix `prompt-craft` + `token-optimization` (llm), `gotcha` + `architecture` (dev), `process` + `tooling` (both) categories.

Retroactive per-entry tagging would edit existing content, violating append-only. Council #27 brief flagged this as an open question with three options: grandfather, explicit rule exception, or split.

## Decision

**Grandfather existing entries. Tag going forward only.**

### Specific rules

1. **Existing 123 lines remain untouched.** No per-entry tags added retroactively. No reformatting of the entry format.

2. **New entries include inline scope tag** as part of the entry format. Updated format:

   ```
   ### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]
   ```

   Where `[scope: X]` uses the ADR-27 vocabulary: `dev | llm | hybrid | runtime | meta`.

3. **File-level section tag.** The LESSONS.md "Entries" section gets a single file-level `<!-- scope: hybrid -->` comment (consistent with Phase 2 audit classification). This satisfies the pre-commit hook's section-tag requirement. Entry-level scope lives within entries per rule 2.

   **2026-04-24 amendment:** insertion point is directly under H1 (`# Lessons Learned — Append-Only Log`), not under `## Entries`. Rationale: validator uses 3-line H1 detection window; H1 placement satisfies the "file-level" intent more literally than `## Entries` placement (which fell outside the detection window). No change to decision intent — only insertion point clarified.

4. **Append-only preserved.** No exception to append-only rule is created. Retroactive tagging would require such an exception; grandfathering sidesteps it entirely.

### Consequences

- **Pre-ADR-27 entries are unfilterable by scope.** Acceptable: entries older than the tagging architecture predate the filter concept.
- **New-entry filtering works from first tagged entry forward.** `grep "scope: llm" LESSONS.md` returns all LLM-scoped lessons added after ADR-27 adoption.
- **Format migration is one-time.** The next entry written after ADR-27 acceptance uses the new format. No bulk migration session.

## Rejected alternatives

- **Explicit rule exception (one-time retroactive migration, documented as ADR):** rejected because append-only is a load-bearing invariant; carving an exception weakens the rule for future edge cases.
- **Split going forward (LESSONS_DEV.md / LESSONS_LLM.md):** rejected because it fragments the single-log property without clear read-time benefit; current LESSONS.md is short (123 lines) and single-file grep serves filtering adequately.

## Consequences — operational

- Pre-commit hook treats LESSONS.md specially: satisfied by file-level `<!-- scope: hybrid -->` under the "Entries" section header. Hook does NOT validate per-entry scope tags (those are within the entry format, not a separate hook concern).
- The entry-format change is documented in ESSENTIALS.md (lesson-extraction section) and PLAYBOOK Section 4 during Stream A rollout. Not in this ADR.

## References

- ADR-27: scope tagging architecture (parent decision)
- CLAUDE.md: append-only rule for LESSONS.md
- Phase 2 audit LESSONS.md section: `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`

## Amendment — 2026-07-17 (chronological legacy-archival split sanctioned; [#339])

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94).** The decision body above is preserved verbatim as drafted; this section extends ADR-29's own append-only + single-log invariants to sanction ONE new size-management path and records the resolution of the three open decisions [#339] raised. **Amendment status: Proposed 2026-07-17** — drafted lane B under plan-first architect review; the lane never self-accepts (ADR-94). Ratify per the "Amendment status / ratification" note at the end of this section.

### Context — why ADR-29 is reopened

ADR-29's **Rejected alternatives** rested the split rejection on a size premise that has since flipped: *"current LESSONS.md is short (123 lines) and single-file grep serves filtering adequately."* As of 2026-07-16 the log holds **241 entries / 571 lines** spanning 2026-03-25 → 2026-07-16 (~3.7 months, ~65 entries/month) — roughly 5× the line count the rejection assumed, and growing fast. The standing split-trigger note at the head of `LESSONS.md` ("when navigation *by topic* becomes painful; reopen if filtering by scope proves insufficient") addresses a **different axis** and has never fired, because the `[scope: X]` inline field made by-topic filtering unnecessary — exactly as ADR-29 predicted.

The 2026-07-16 LESSONS ruling (`tail micro-arc`) recorded the reopen: when the log outgrows single-file navigation, the sanctioned reorganization is a **chronological legacy-archival split** — a contiguous *older* block relocated **byte-unchanged** into a dated `LESSONS-legacy-<period>.md` with a pointer left behind — which **redefines two of ADR-29's invariants** and therefore needs ADR-29 reconciliation before execution. This amendment is that reconciliation.

### What is sanctioned (and what stays rejected)

- **SANCTIONED — chronological legacy-archival split.** A contiguous **older** block of entries MAY be moved wholesale, **byte-identical**, out of the active `LESSONS.md` into a dated, read-only `LESSONS-legacy-<date-span>.md`, leaving a dated pointer line in `LESSONS.md` at the boundary. Chronological order is preserved *within each file*; no entry body is rewritten, reformatted, or deleted. The active file keeps the "hot" (recent) working set; the legacy file holds the cold tail.
- **STILL REJECTED — by-scope / by-topic split.** ADR-29's rejection of `LESSONS_DEV.md` / `LESSONS_LLM.md` (fragmenting the single-log property along the scope axis) **STANDS unchanged.** This amendment sanctions splitting along the **chronological** axis ONLY. The `[scope: X]` inline field remains the mechanism for topic filtering; nothing here reintroduces per-scope files.

The distinction is load-bearing: a by-scope split shatters the single chronological narrative into parallel logs read in isolation; a chronological split keeps one narrative and merely archives its oldest reach into an adjacent dated file that any grep can still sweep (`grep … LESSONS*.md`).

### Invariant redefinition (append-only + single-log)

- **Append-only** is redefined from *"an entry, once written, never leaves the file"* to *"an entry, once written, is never edited or deleted; it may be **relocated byte-identical** into a dated `LESSONS-legacy-<span>.md` as part of a sanctioned chronological archival, never otherwise."* In-place edits and deletions remain forbidden (ADR-29 rule 1 / ADR-39 append-only). The archival move is the **only** sanctioned way an entry leaves the active file, and it is size-management, not content change.
- **Single-log** is redefined from *"one physical file"* to *"one logical chronological log, physically the active `LESSONS.md` plus zero-or-more dated legacy files that together tile the timeline with no gap and no overlap."* Reading the full history = the active file + its legacy files in date order.
- **Scope of the exception.** This is ADR-29-and-LESSONS-specific (mirroring how ADR-94's status-line exception is ADR-status-line-specific). It does **not** loosen append-only for JOURNAL/TOKEN-LOG, nor the immutability of ADRs/transcripts/handoffs/audits. Contrast the ADR-49/65 CLAUDE §12 condense, which is sanctioned only for THAT file's own history — this sanctions a *relocation-byte-identical* move, not a condense/rewrite.

### Decision A1 — Split trigger: **hard threshold + hysteresis, with the soft criterion retained as an earlier override**

**Recommendation: a machine-checkable hard threshold is the primary trigger; the navigation-pain criterion is retained only as a *permitted earlier* operator override, not as the sole trigger.**

- *Justification.* ADR-29's original soft trigger ("when navigation becomes painful") has sat un-fired for ~3 months while the log grew ~5×, because a subjective trigger with no owner and no gate defers forever — the same failure mode ADR-39 was written to prevent (implicit lifecycle → silent drift). This repo consistently prefers machine-checkable numeric thresholds for exactly this reason (ADR-53 doc-rot line budgets, `scan_file_budget`, ADR-100's count-tiered audit index). A hard count removes the judgment call, makes "not-yet-needed" a *defined* state, and is trivially surfaced by the A2 helper.
- *Metric.* **Entry count** is primary (each entry is ~one line; entries are what a reader navigates by and what the boundary is drawn on). Line count is a secondary read-out the helper also reports.
- *Recommended dial (architect-tunable).* Trigger when the **active** `LESSONS.md` exceeds **300 entries**; on trip, archive the **oldest contiguous by-date block** until the active file holds **≤ ~180 entries** (≈ the trailing working set at current velocity), naming the legacy file by the actual span moved, e.g. `LESSONS-legacy-2026-03-to-2026-05.md`. The two numbers give hysteresis so a split isn't re-triggered every session.
- *Soft override.* The operator MAY archive **earlier** on felt navigation pain; the hard count is the **backstop** guaranteeing the trigger eventually fires unattended.
- *State today.* 241 entries < 300 → **not-yet-needed**. This amendment records the threshold; **no block is moved this arc** (execution is [#339]'s build leg).

### Decision A2 — Boundary helper: **yes — spec a read-only enumerator + byte-identity verifier (build deferred)**

**Recommendation: sanction a read-only helper; its byte-identity check is the load-bearing safety proof for the redefined append-only invariant.** The redefinition is only safe if "relocated byte-identical" is *mechanically provable* rather than honor-system.

Spec (build is a follow-up, not this arc — capture-precedes-construction, ADR-70; consistent with the Layer-2 read-only / WARN-only posture of ADR-28/36):
- **Threshold read-out** — report active-file entry count (and line count) vs the A1 threshold: is a split due / how close.
- **Byte-identity check** — for each `LESSONS-legacy-*.md`, prove every archived entry body is byte-identical to its pre-move form (hash the moved block; a split-execution test asserts zero entry-body change). This is the invariant's teeth.
- **Boundary enumeration** — report the newest entry of each legacy file and the oldest entry of the active file, so chronological **tiling** (no gap, no overlap, strict date order across files) is provable, and confirm the pointer line in `LESSONS.md` resolves.
- **Posture** — read-only, exit-0/WARN-only (never mutates, never moves a file), HUB-first (LESSONS is per-repo, so it is fleet-portable later). Build filed under [#339]'s follow-up (or a dedicated ticket at ratification).

### Decision A3 — Amendment form: **in-file amendment to ADR-29 (this section), NOT a successor ADR**

**Recommendation: amend ADR-29 in place (the section you are reading), derived from the repo's own taxonomy precedent.**

- *ADR-101 pattern (in-file):* ADR-101 records its later rulings as appended `## Ratification amendment` / `## Amendment — 2026-07-13` sections that **extend the same ADR's own doctrine** (its sanctioned-set / naming grammar). When the change refines the ADR's *own* subject, ADR-101 amends in-file.
- *ADR-102 pattern (successor):* ADR-102 chose a **successor** ADR over amending ADR-101, with an explicit "Why not amend ADR-101": the parity-schema-semantics concept is *"taxonomically unrelated to hermetization"* — a **different domain**.
- *Applying the test.* Sanctioning the chronological split **redefines ADR-29's own core invariants** (append-only, single-log) and directly qualifies the **size premise of ADR-29's own by-scope rejection**. This is the *same* subject in the *same* taxonomic domain (LESSONS.md lifecycle) — the ADR-101 case, not the ADR-102 case. ADR-39's registry already floats a *"Quarterly archive option per ADR-29"* for the LESSONS.md row, attributing the archive concept to ADR-29's domain — this amendment realizes that long-standing pointer.
- *Readability clincher.* An in-file amendment sits adjacent to the still-standing **Rejected alternatives**, so a reader sees the by-scope rejection and the by-chronology sanction **together in one document** — exactly the "the rejection STANDS and the amendment must say so" legibility the reconciliation demands. A successor ADR would have to quote-and-supersede that sentence across documents.
- *Immutability.* Appending an in-file amendment marker (not editing decision content) is expressly sanctioned by CLAUDE.md §5 item 3 / ADR-94 — the same mechanic ADR-101 and ADR-39 use.

### Reconciliation with ADR-39

- ADR-39's LESSONS.md registry row **Grooming** cell already reads *"Never (append-only, history preserved). Quarterly archive option per ADR-29."* — this amendment **defines** that previously-unspecified archive option (mechanism + trigger). The **Update trigger** cell (append-only) is unchanged in spirit: entries are still never edited/deleted; the archival relocation is a size-management move, not a lifecycle-category change. A one-line ADR-39 registry note pointing here is a follow-up, not required for this sanction.

### Amendment status / ratification

**Proposed 2026-07-17** (Path A, plan-first architect-reviewed; lane B, commit-and-STOP — integration is operator-serialized from the primary checkout). Ratify by editing this section's **Amendment status** line in place `Proposed → Accepted` (ADR-94) and annotating the `docs/decisions/README.md` ADR-29 index row *"amended 2026-07-17 — chronological legacy-archival split sanctioned"*. The split stays **UNsanctioned until ratification**; [#339]'s build leg (execute-once or record not-yet-needed, + the A2 helper) does not proceed before then.
