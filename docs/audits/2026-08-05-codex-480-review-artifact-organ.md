# Codex Review — 480-review-artifact-organ

**Date:** 2026-08-05
**Branch:** `feat/480-review-artifact-organ`
**HEAD:** `c31306a1`
**Diff range:** `main..feat/480-review-artifact-organ`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Tally:** 0/5/0/0 (C/H/M/L)

---

> **Tally is hand-corrected, and that is itself a finding.** The wrapper's heuristic counter
> printed `Critical 0 / High 0 / Medium 0 / Low 0` for this run while the body carries **five
> HIGH** findings under `## High`. The tally above is the true count, read from the body. This
> is exactly the failure mode the [#480] canonical-header ruling exists to remove — a machine
> counter that disagrees with the artifact it counts — and it argues that the `**Tally:**` line
> should be authored from the findings, never trusted from the wrapper's regex.
>
> **Disposition of the five (all fixed pre-merge; details in the commit that follows):**
> 1. `:3690` docs-under-code-dirs treated as code-impact — **FIXED** (43 tracked files affected;
>    the bare directory-prefix rule is gone). The reviewer's proposed "suffix AND prefix" fix was
>    **not** taken: 3 tracked code files live outside those dirs, so it trades false positives
>    for false negatives. Suffix-anywhere + exact paths has neither; pinned by 11 cases.
> 2. `:3751` any doc with Branch/HEAD accepted as an artifact — **FIXED** (13 tracked non-review
>    docs carry a `**Branch:**` field; the canonical title is now required, 0/13 of them match).
> 3. `:3797` branch-only linkage can launder — **PARTLY ACCEPTED, NOW NAMED.** Two-leg linkage
>    is the operator-approved design (2026-08-05); full-SHA-only would break the pre-rebase case
>    the leg exists to tolerate. Branch-name reuse and abbreviation collision are now documented
>    as explicit limits rather than left implicit.
> 4. `:3792` squash/amend fallback not implemented — **FIXED AS A DOC DEFECT.** The claim was
>    wrong, not the code: the branch leg reads `Merge branch '<x>'`, the only shape
>    core-invariant #5 permits (`block_ff_push` refuses the rest). The docstring now says so.
> 5. `:3771` cutoff depended on each commit's local timezone — **FIXED** (`%cs` → `%ct`, cutoff
>    is a UTC instant, pinned to epoch 1785888000).

---

## Focus

- check_review_artifact_coverage: is it genuinely incapable of a hard FAIL verdict on ANY input path, including the outer exception handler? Any route to status='fail'?
- The code-impact predicate (suffix .py/.ps1 + prefix scripts/ deploy/ tests/ plugins/ + exact .pre-commit-hooks.yaml/.pre-commit-config.yaml). Any way a code change evades it, or a docs-only merge falsely trips it? Is str.startswith/endswith with a tuple correct here?
- Linkage: branch OR in-range HEAD. Can an UNRELATED artifact launder an unreviewed merge (false negative)? Is the ny(c.startswith(art['head'])) prefix match safe against a short/ambiguous HEAD value, e.g. a 7-char prefix colliding?
- The batched spine_dates map: is spine_dates.get(sha, '') < _REVIEW_RULING_DATE correct for an ABSENT sha (should skip, not scan)? Any correctness change vs the per-entry form it replaced?
- Date comparison is string-vs-string on %cs (YYYY-MM-DD). Any timezone/format edge where this misclassifies a merge?
- _REVIEW_BRANCH_RE / _REVIEW_HEAD_RE / _REVIEW_TALLY_RE: can a non-review doc (audit index, memo) be misparsed as a review artifact, or a real artifact be missed?
- Is the WARN evidence honest about what it does NOT verify?

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:3690 — Docs-only changes under code directories are treated as code-impact

**What:** The predicate ORs the suffix and directory checks, so `scripts/README.md`, `tests/fixtures.md`, or `plugins/notes.yaml` triggers review coverage.  
**Why:** This creates false WARNs and corrupts the zero-false-positive evidence bar.  
**Fix direction:** Require the intended suffix-and-prefix combination, with the two YAML files retained as exact-path exceptions.

### scripts/audit.py:3751 — Any audit document with matching metadata can be accepted as a review artifact

**What:** A file is classified as an artifact when it contains either `Branch` or `HEAD`; it need not have the canonical review title/mode/header shape.  
**Why:** A non-review memo with a matching branch/HEAD and tally can silently satisfy coverage; the WARN/pass evidence then overstates that a “linked review artifact” exists.  
**Fix direction:** Parse and require one complete, anchored canonical review-artifact header before considering linkage or tally.

### scripts/audit.py:3797 — Branch-only linkage can launder an unrelated artifact

**What:** Any artifact with the same branch name passes, regardless of its recorded HEAD; the next line also accepts ambiguous seven-character SHA prefixes.  
**Why:** A reused branch, or an artifact whose abbreviated HEAD collides with an in-range commit, can silently mark an unreviewed merge as covered.  
**Fix direction:** Bind artifacts to an unambiguous commit identity (resolve and compare full SHA); do not let branch equality alone establish coverage without durable merge-specific evidence.

### scripts/audit.py:3792 — The documented squash/amend fallback is not implemented

**What:** The branch is extracted only from `Merge branch '…'` subjects. Squash merges have no such subject, and their pre-squash reviewed HEAD is not in `introduced()`.  
**Why:** A valid review for a squash merge produces a false WARN, despite the stated branch fallback intended to cover that case.  
**Fix direction:** Persist a merge-specific linkage that survives squash/amend, or explicitly narrow the supported merge forms and test that contract.

### scripts/audit.py:3771 — Date cutoff depends on each commit’s local timezone

**What:** `%cs` is compared to a timezone-free ruling date.  
**Why:** A merge near midnight in a non-local commit timezone can be skipped although it occurred after the ruling cutoff, or scanned although it occurred before it.  
**Fix direction:** Define the cutoff as an offset-aware instant and compare normalized commit timestamps; add boundary tests with opposing timezone offsets.

## Medium

(not assessed — default diff-review scope is Critical/High only.)

## Low

(not assessed — default diff-review scope is Critical/High only.)