# Codex Review — seat-release-b1-followup

**Date:** 2026-09-29
**Branch:** `worktree-lane-handoff-moments`
**HEAD:** `a453c7a0`
**Diff range:** `main..worktree-lane-handoff-moments`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/0/0/0 <!-- Critical/High/Medium/Low. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Follow-up review of the LANE-5B5-2 diff after two fix-forward commits (64f233fb: era comes from the bundle's directory-name date instead of HANDOFF_RECEIPT.json, closing a receipt-deletion evasion; a453c7a0: exclude docs/handoffs/archive/ from era-gating, fixing a false positive the first fix introduced -- caught live in a fix re-proof CI run, run 36623905708). Focus specifically on .github/workflows/conductor.yml's handoff-manifest job's new era-gating logic: any remaining evasion path (e.g. a differently-named non-bundle container, a bundle dated exactly on the cutoff, a directory whose name starts with a valid date but is not a real bundle), and any other soundness issue in the inline python.

---

## Findings
## CRITICAL

### .github/workflows/conductor.yml:719

**What:** An invalid calendar date before the cutoff (for example, `2026-02-31-evasion`) matches `date_re` and is exempted by the lexical `< CUTOFF` comparison.  
**Why:** A current bundle can evade BD-manifest verification simply by using an impossible pre-cutoff-looking date; the canonical verifier already treats such dates as in-era/fail-closed.  
**Fix direction:** Use the verifier’s date-validating era predicate rather than a local regex/string comparison, and add a CI-step regression test for invalid calendar dates.

### .github/workflows/conductor.yml:716

**What:** Excluded direct children, especially `archive*`, are skipped wholesale and their descendants are never inspected.  
**Why:** A post-cutoff bundle placed in `docs/handoffs/archive/` (or an `archive-*` container) is touched by the push but never checked, allowing an absent or tampered manifest to pass.  
**Fix direction:** Restrict container exclusions to the exact intended container and inspect/reject any manifest-era descendants, or enforce that excluded containers cannot contain post-cutoff bundles.

**Resolution.** Both fixed, same-lane, in `.github/workflows/conductor.yml`'s `handoff-manifest`
job. A directory is now a candidate bundle iff it is date-prefixed OR carries
`HANDOFF_RECEIPT.json` directly; anything else (`archive/`, and a container is recursed into at
any depth, not just one level — a second real false positive, `docs/handoffs/archive/legacy/`,
a nested undated container, was caught by hand while re-verifying the first fix against the live
tree and is now also covered). This closes both the fake-old-date-with-receipt evasion and the
smuggled-bundle-inside-a-container evasion at any nesting depth, including a rename-only evasion
(strip the date prefix, keep the receipt) at any depth. RED-first witnesses added for all three
scenarios (fake-old-date, smuggled-in-archive, nested-undated-container), confirmed red
pre-fix, green post-fix; also reverified clean against the real live `docs/handoffs/` tree
(`checked 1 manifest-era bundle(s)`, matching the pre-review baseline exactly) and against a
real tamper via CI (see the base review's Resolution note for the run URLs).

**Accepted residual (documented, not silently left unaddressed):** a bundle that is BOTH renamed
to strip its date prefix AND has its receipt deleted/relocated is still undetectable by this
job, since nothing inside `docs/handoffs/` would then identify it as a bundle at all. Closing
that fully needs a ledger of known bundle identities kept OUTSIDE the bundle itself, which is new
infrastructure outside this lane's Owns/Do-not (no new path may be created). Recorded here so
the gap is explicit rather than assumed closed.

## HIGH

(none)

## MEDIUM

(none)

## LOW

(none)