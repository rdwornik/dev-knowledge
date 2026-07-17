# Codex Review — adr29-legacy-split-amendment

**Date:** 2026-07-17
**Branch:** `worktree-lane-b-adr29-amendment`
**HEAD:** `32372c20`
**Diff range:** `main..worktree-lane-b-adr29-amendment`
**Codex version:** codex-cli 0.144.5
**Mode:** doc-review

---

## Focus

- Draft ADR-29 in-file amendment sanctioning a CHRONOLOGICAL legacy-archival split of LESSONS.md (distinct from the by-scope split ADR-29 rejected, which must STAND).
- Check disposition-faithfulness: does the amendment faithfully reflect the 2026-07-16 LESSONS ruling and #339 body? Does it preserve the by-scope rejection explicitly?
- Check cross-doc consistency: append-only/single-log invariant redefinitions vs ADR-29 rule 1, ADR-39 registry, CLAUDE.md §5; any stale claims or dangling refs.
- Check structural integrity: in-file amendment marker convention (ADR-101/ADR-94), Proposed status, ratification note.
- Check the three resolved decisions (A1 threshold, A2 helper, A3 form) for internal consistency and sound justification.

---

## Findings
## Critical

(none)

## High

### docs/decisions/ADR-29-lessons-grandfathering.md:97 — The proposed byte-identity verifier has no preserved pre-move baseline

**What:** Hashing the moved block after relocation cannot prove it matches its former `LESSONS.md` content.  
**Why:** The amendment calls this the load-bearing proof for the redefined invariant, but the original bytes are gone from the active file.  
**Fix direction:** Require an immutable pre-move source reference/hash manifest (for example, the pre-split Git blob and block digest) recorded with the pointer/legacy file.

### docs/decisions/ADR-29-lessons-grandfathering.md:113 — Deferring the ADR-39 registry update contradicts ADR-39’s lifecycle requirements

**What:** The amendment says an ADR-39 registry note is only follow-up work, while the split creates a new legacy-file lifecycle and changes the existing LESSONS lifecycle.  
**Why:** ADR-39 requires lifecycle updates to be amended and new files to have all six lifecycle elements documented before creation; the JOURNAL also overstates this as already “reconciled.”  
**Fix direction:** Make ADR-39 registry reconciliation a required ratification/build prerequisite, including the legacy file’s complete lifecycle definition.

### docs/decisions/ADR-29-lessons-grandfathering.md:117 — The proposed ratification edit is not the ADR-94 status-line exception

**What:** ADR-29’s actual `**Status:**` line is already `Accepted`; the text instead proposes editing an embedded “Amendment status” statement.  
**Why:** ADR-94 permits editing an ADR’s status line, not arbitrary amendment prose, so this ratification path would violate the cited immutability rule.  
**Fix direction:** Define a compliant ratification mechanism for a proposed amendment to an accepted ADR, such as appending a ratification marker rather than editing the draft amendment text.

### docs/decisions/ADR-29-lessons-grandfathering.md:79 — Ratification leaves binding append-only instructions contradictory

**What:** The amendment creates a LESSONS-only relocation exception but does not require updates to CLAUDE.md and ARCHITECTURE.md, which still say LESSONS “only append” and is “never edited.”  
**Why:** After ratification, an operator following those current instructions would be told not to perform the newly sanctioned archival move.  
**Fix direction:** Include the precise LESSONS chronological-archival exception in the atomic ratification/reconciliation set, while preserving the stricter rules for JOURNAL and TOKEN-LOG.

## Medium

### docs/decisions/ADR-29-lessons-grandfathering.md:86 — Entry-size justification conflicts with the amendment’s own figures

**What:** It says each entry is “~one line,” but 241 entries over 571 lines is about 2.4 lines per entry.  
**Why:** This weakens the stated rationale for preferring entry count and makes future threshold interpretation less reliable.  
**Fix direction:** State that entry count is the navigation unit while line count remains a separate reported size signal.

## Low

(none)
