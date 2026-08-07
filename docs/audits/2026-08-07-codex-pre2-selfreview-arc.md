# Codex Review — pre2-selfreview-arc

**Date:** 2026-08-07
**Branch:** `docs/pre2-self-review`
**HEAD:** `e62c412a`
**Diff range:** `945598f9..HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Review of the CURRENT branch's own code diff (docs/pre2-self-review), before it merges.
- scripts/batch_manifest.py: the new _is_tracked git probe, _valid_closer path validation, and inline-comment stripping in _frontmatter. Can any of the three be bypassed, and do they all fail toward NO exemption?
- scripts/audit.py: the mixed-case FAIL evidence now discloses applied exemptions.
- .github/workflows/report-only-wall.yml: the two new before-sha guards (ancestry in the changes job, existence in the anchor leg).
- tests/test_fleet_analytics.py: the mutmut-sandbox skip.
- Ignore prose/markdown paths entirely.

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/batch_manifest.py:171 — “tracked” manifests can still be uncommitted or modified

**What:** `git ls-files` accepts staged additions and previously tracked paths, while the manifest content and closer presence are then read from the working tree.  
**Why:** A staged new manifest—or an unstaged edit to an existing manifest—can declare an open batch and exempt a lane merge without that exact manifest state being committed; this violates the stated committed-manifest boundary.  
**Fix direction:** Resolve the manifest and closer against a committed Git tree (for example `HEAD:<path>`), and add staged/unstaged mutation cases that must yield no exemption.

## Medium

(none)

## Low

(none)
---

## Disposition — 2026-08-07

**Tally 0/1/0/0 — ACCEPTED and FIXED, and it is the SECOND terra HIGH in a row on the same
line of defence.**

### H1 · "tracked" manifests can still be uncommitted or modified — FIXED

The finding is exactly right, and it lands on the fix for the PREVIOUS finding. Earlier today
`open_batches()` was hardened from "a file exists" to "`git ls-files` says tracked". But
`ls-files` is satisfied by a merely **STAGED** addition, and the manifest CONTENT and the
closer's existence were still read from the **working tree**. So three states still granted an
exemption the rule forbids:

- a staged-but-uncommitted manifest,
- an unstaged EDIT to a committed manifest (flipping `status:` or `closed_by:` off the record),
- an uncommitted closing packet, which would appear to expire a batch that is still open.

**Fixed by making every input HEAD-based**, which is the only implementation that means what
"committed" says: `_committed_manifests` lists via `git ls-tree HEAD`, `_committed_text` reads
the blob at `HEAD:<path>`, and `_closer_committed` probes `git cat-file -e HEAD:<closer>`. All
three route through one `_git` helper that returns `None` on any failure, so every error still
reduces to *no exemption*.

Pinned by `test_an_UNCOMMITTED_manifest_grants_nothing` (untracked → staged → committed →
unstaged-edit, four states in one test) and
`test_an_UNCOMMITTED_closing_packet_does_not_expire_the_exemption`.

**Two existing tests were de-vacuumed in the same pass**, and this is worth recording because
the HEAD-based change made them silently meaningless:
`test_a_manifest_that_declares_no_closer_does_not_open_a_batch` and
`test_a_manifest_marked_closed_opens_nothing` both wrote their manifest WITHOUT committing it.
Under the new rule they would have passed for the wrong reason — the manifest is invisible at
HEAD, so `status:`/`closed_by:` were never consulted at all. Both now commit, so they test the
clause they name.

`test_the_exemption_leg_cannot_turn_a_fail_into_silence_when_it_errors` was also rewritten:
its source-level assertion (`"except" in getsource(open_batches)`) broke when error handling
moved into `_git`. It now asserts the property BEHAVIOURALLY against a non-repo directory, and
checks the single git chokepoint separately — a source-shape assertion outliving the shape it
described, while still claiming to check the property, is its own small lesson.

### The pattern this arc keeps demonstrating

Two consecutive reviews, two HIGHs, both on the exemption's committed-ness boundary — and the
second landed on the fix for the first. A hardening that looks obviously correct is exactly the
kind that needs a second reader, because the author has already convinced themselves. This is
the fourth time today a review found my code contradicting its own stated rule.
