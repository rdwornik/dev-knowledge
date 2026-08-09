# Codex Review — arc1-doc-defects-retro

**Date:** 2026-08-09
**Branch:** `docs/arc1-doc-defects`
**HEAD:** `fc0b1f04`
**Diff range:** `df1b05b0^1..df1b05b0`, filtered to `*.py` (the wrapper's code-path guard)
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/0/0/0 <!-- Critical/High/Medium/Low, counted from the Findings section. The reviewer returned zero findings against the reviewed diff. The out-of-diff observation below is AUTHOR-sourced, was never put to the reviewer, and is deliberately NOT counted here. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Passes:** 1 (a 24-line diff, comment + one registry row; nothing for a loop to converge on)

---

## Why this artifact exists

`review_artifact_coverage` flagged `df1b05b0` as a code-impact merge carrying no linked review
artifact. **The WARN was cleared by running the review, not by dispositioning it** — the ARC-2
Phase-0 ruling, and the same discharge the batch-2 morning arc and the batch-3 integrator arc took.
Retroactive review has precedent here.

### Header authored from the parser, not from the wrapper

`codex-review.ps1` stamps `**Branch:**` with the *current* branch and `**HEAD:**` with the *current*
HEAD. Run from the primary checkout after the merge, that yields `main` / `df1b05b0` — and `main`
matches no merge subject, so the BRANCH leg would not have linked. The fields above are corrected to
the reviewed branch (`docs/arc1-doc-defects`, the name in the merge subject) and to a commit the
merge introduced (`fc0b1f04`, the code-bearing one), so the artifact links on **both** legs.

This is the same defect class the batch-3 artifact was rewritten for: *correct to a human reader,
invisible to the machine*. Noting it because the wrapper reproduces it on every retroactive review —
a review run after the merge can never self-stamp a linking header.

---

## Focus put to the reviewer

1. This registers a SECOND spec in `_SPEC_REGISTRY`. Does the new row's presence change behaviour of
   `parse_spec_version` / `should_nudge` / `scan_undeclared_edges` in any way the comment does not describe?
2. Is the comment's claim accurate that an HTML `<!-- version: -->` sentinel is invisible to
   `parse_spec_version`, and that `should_nudge` requires a parsed version on **both** sides?
3. Any correctness risk from a spec whose file path does not exist, or whose version fails to parse,
   now that the registry has n>1 rows?

## Findings

## Critical

(none)

## High

(none)

## Medium

(none)

## Low

(none)

---

## Author verification of the zero (question 2)

A zero-finding tally on a diff whose whole content is a *claim about other code* is worth one
independent check, because a rubber stamp and a real pass look identical in this file. The diff's
load-bearing claim is that `coherence_nudge` "silently never fires, since `should_nudge` requires a
parsed version on both sides."

Read directly: `should_nudge` (`scripts/coherence_nudge.py`) returns
`hv is not None and sv is not None and hv == sv`. Had `_extract_version` returned the spine parser's
`""` for an unversioned spec, `hv is not None` would be **True** and `hv == sv == ""` would make the
nudge fire on *every* content edit of a version-less spec — the exact inverse of the claim. It does
not: `_extract_version` is `spec_version_numeric(text) or None`, which coalesces `""` to `None`.
**The comment's claim holds.** The zero is confirmed on the axis that could most plausibly have
falsified it.

## Out-of-diff observation — NOT a finding against this diff, not in the tally

Registering `prompt-template` made 8 advisory `undeclared_edges` WARNs visible. Eight are mentions.
**One is not:** `protocols/PLAYBOOK.md` "Tree orchestration" cites
`` `templates/prompt-template.md` (v1.7) `` while the spec now reads `Version: 1.13`.

- The **claim** that citation labels is still true — the template's lane-count note still reads
  "up to ~10 parallel **work** lanes". Only the version token is stale.
- Severity is low and the diff did not cause it; the registration is what *revealed* it.
- It is recorded here rather than fixed, because Phase 0's ruling was to disposition the eight, not
  to edit PLAYBOOK. It carries forward as a triage finding, and it is the concrete evidence for the
  gap the ruling names: **nothing in the corpus distinguishes a doc that *mentions* a spec from one
  that *depends on* it.** All eight WARNs look identical to the scanner; exactly one had rotted.

## Honest limits

This artifact proves a review ran, is linked, and carries a parseable tally. It does not prove the
review was competent. The diff is 24 lines, 20 of them comment; the reviewed surface is small enough
that a zero is credible, which is not the same as verified. One claim was independently checked
above; the other two focus questions rest on the reviewer's word.
