# Codex Review — mutmut-sandbox-skip

**Date:** 2026-08-07
**Branch:** `fix/502-mutmut-sandbox-markers`
**HEAD:** `8bb06e00`
**Diff range:** `945598f9..3234abb3`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/0/1/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- RETROACTIVE review of a 14-line test change: tests/test_fleet_analytics.py gains a skip when the repo root is named mutants (mutmut copies only the mutated source tree there, so protocols/ and docs/ do not exist).
- Is the skip correctly scoped? Could it swallow a genuinely broken or incomplete checkout?
- Does anything meaningful still get asserted inside the sandbox, or is the test hollowed out there?

---

## Findings
## CRITICAL

(none)

## HIGH

(none)

## MEDIUM

tests/test_fleet_analytics.py:635 — Sandbox detection is based solely on the checkout directory name.

**What:** Any normal or incomplete checkout rooted in a directory named `mutants` skips the marker and common-dir assertions.  
**Why:** This contradicts the stated intent to fail on genuinely incomplete checkouts, silently weakening this live-repo test outside mutmut.  
**Fix direction:** Identify mutmut using a sandbox-specific signal in addition to (or instead of) the directory basename.

## LOW

(none)
---

## Disposition — 2026-08-07

**Tally 0/0/1/0. The MEDIUM is ACCEPTED AS ACCURATE and deliberately NOT fixed here.**

### M1 · Sandbox detection is the checkout directory name alone

**Correct as stated.** `if root.name == "mutants": skip(...)` means any checkout rooted in a
directory literally called `mutants` would skip the marker and common-dir assertions, weakening
this test outside mutmut — which does contradict the stated intent that a genuinely incomplete
checkout still fails.

**Why it stands for now, as a judgement rather than a dismissal:**

- The blast radius is one test's identity legs, in a repo whose checkout is `.dev-knowledge`
  and whose CI checkout is `dev-knowledge`. Neither is `mutants`, and a hub clone named
  `mutants` is not a state anything here produces.
- The available stronger signals are each worse in a specific way: `MUTANT_UNDER_TEST` is set
  per-mutant and is absent during the BASELINE run that this test breaks; probing for
  `mutants/` as a child inverts the check without strengthening it; and an env var mutmut does
  not document is a dependency on unversioned behaviour.
- The narrower question — how mutmut's sandbox should be recognised — belongs with [#502]'s
  ADOPT/REJECT verdict, which is still open. If the answer is REJECT, the skip and its
  detection disappear together.

**Recorded rather than absorbed:** if [#502] moves to ADOPT, tightening this detection is part
of that work, and this artifact is the reference. Until then the honest description is *the
skip is keyed on a directory name and would fire for any tree so named* — which the test's own
comment now says.
