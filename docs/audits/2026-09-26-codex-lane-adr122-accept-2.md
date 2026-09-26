# Codex Review — lane-adr122-accept-2

**Date:** 2026-09-26
**Branch:** `worktree-lane-adr122-accept-2`
**HEAD:** `fc80dfa9`
**Diff range:** `main..worktree-lane-adr122-accept-2`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

This lane (WAVE5B-N3 row 6, contract LANE-5B3-6-adr122-accept-2.md) resumed N2's twice-refused
lane-adr122-accept from its kept branch worktree-lane-adr122-accept @ f3cd9af0. This session's
OWN commit (fc80dfa9) is small: docs/decisions/README.md flips ADR-122's index row status marker
from Proposed to Accepted to match the ADR-122 header (the exact defect the second refusal named --
validate_adr_status coherence divergence), and tests/test_validate_adr_status.py re-pins the
R_WRAP baseline 1->2 for ADR-122's own pre-existing multi-line Status field. Focus review on:
(1) is the README marker edit correct and sufficient to restore header/index coherence without
disturbing any other row; (2) is the re-pinned test baseline honestly justified (a real measured
corpus change, not a laundered assertion); (3) any other real defect in the full main..HEAD diff
this lane is responsible for landing.

---

## Findings
The ADR-122 index marker correctly matches the Accepted header, and the R_WRAP 1→2 baseline is justified by the newly wrapped header value.

## Critical

(none)

## High

## [HIGH] scripts/task_record.py:296 — D3 link fields are left as `legacy_body`

**What:** The converter never populates declared `routine`, `supersedes`, or `provenance` fields; `routine:` is explicitly treated as uncaptured legacy text.  
**Why:** ADR-122 D3 requires these links as typed data, so conversion retains text but loses the structured relationship needed by consumers and cannot meet the step-1 zero-legacy-body exit.  
**Fix direction:** Parse these clauses into their declared model fields and add corpus-level conversion assertions; reserve `legacy_body` only for genuinely unresolved/narrative material.

**Disposition (this lane):** Recorded, not fixed — the same class N2's own Codex terra round already
found and documented as a step-1 limit ("1 High documented as the step-1 limit", `to-browser/REFUSED-lane-adr122-accept.md`).
`scripts/task_record.py`'s own docstring states step 1 is contract+reconciliation, not the flip, and
`tasks/1080-*.md` (this lane's own remainder row, in the 1076-1085 range) already tracks "eliminate
legacy_body carriers" as ADR-122 step 1's own named exit gap — `routine`/`supersedes`/`provenance`
land inside that same remainder, not as a new untracked defect. Deepening the converter's field
coverage is real work beyond this resumption lane's Done-contract (items 1, 2, 3, 5; item 4 optional)
and beyond its Do-not ("flip the source of truth is step 2").

## Medium

(none)

## Low

(none)