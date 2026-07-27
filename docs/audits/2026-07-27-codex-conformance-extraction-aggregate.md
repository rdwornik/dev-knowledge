# Codex Review — conformance-extraction-aggregate

**Date:** 2026-07-27
**Branch:** `worktree-434-conformance-extraction`
**HEAD:** `94b64267`
**Diff range:** `main..worktree-434-conformance-extraction`
**Codex version:** codex-cli 0.145.0
**Mode:** doc-review

---

## Focus

- Doc lane over docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md (the [#434] aggregate)
- Verify the artifact's citations are internally consistent (digest paths, line ranges, SHAs, dates)
- Check the sharp-test section answers all three sub-questions explicitly and the observation is labelled as observation, not ruling
- The aggregation script is scratch-only and uncommitted by design; the artifact self-verifies via per-row verbatim citations

---

## Findings
## Critical

(none)

## High

(none)

## Medium

**Medium — docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md:94**

**What:** The claim that all nine fixed findings were fixed by the listed commits omits `9a04e23`, which corrected CONTRIBUTING’s ruff description and re-stamped it—the fix behind F4 and 07-22 N1/N2.  
**Why:** The stated fix provenance is incomplete and attributes the full result set to commits that do not cover all nine findings.  
**Fix direction:** Include the missing July 23 correction commit (or describe the lane without implying the listed SHAs are exhaustive).

**Medium — docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md:42,76**

**What:** The table classifies 07-24 N2 as a “real defect, still live,” while its evidence text says the prose does not explicitly claim execution order and that defecthood is weak.  
**Why:** This overstates a factual ordering observation as a confirmed defect and inflates the aggregate’s “real defect” conclusion.  
**Fix direction:** Move N2 to contested, or rename/clarify the classification category so it does not assert confirmed defect status.

**Medium — docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md:98**

**What:** “False-positive rate among claims was 2/35 raw” uses the raw-findings denominator for a rate explicitly described as being among claims.  
**Why:** There are 21 claimed findings; `2/35` is the false-positive rate among raw findings, while the rate among claims is `2/21`.  
**Fix direction:** State both rates with their correct denominators, or retain only the measure intended.

## Low

**Low — docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md:21,25**

**What:** Two sharp-test citations use abbreviated filenames (`2026-07-25-…digest.md`, `2026-07-27-…digest.md`) rather than the declared digest-path format.  
**Why:** They are not resolvable paths and weaken the artifact’s claimed per-row citation traceability.  
**Fix direction:** Use the full `docs/audits/YYYY-MM-DD-conformance-nightly-digest.md` paths, consistent with §4.
