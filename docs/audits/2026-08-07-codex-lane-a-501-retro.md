# Codex Review — lane-a-501-retro

**Date:** 2026-08-07
**Branch:** `worktree-lane-a-501-ci-recorder`
**HEAD:** `6714f7cd`
**Diff range:** `df815c7c0d5dc62828cacd22cc8442e474ddac51..6714f7cd`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (RETROACTIVE)
**Tally:** 0/1/0/0
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- RETROACTIVE review of an already-merged lane (batch-1 lane A, [#501]) that shipped WITHOUT a review. This is the compensating pass.
- .github/workflows/report-only-wall.yml: the report-only recorder. Check trigger correctness, the continue-on-error posture on the three measured legs, fetch-depth 0, the exact uv pin, shell-injection risk in the summary-table interpolation, and any input passed to an action that the action does not accept.
- scripts/validate_hermetization.py + tests: .github admitted to SANCTIONED_TIER1_DIRS. Is the sanction correctly scoped and tested?
- Known-open findings you do NOT need to re-report: the setup-uv python-version-file input (already ticketed), and the mutation-pilot paths gating (already ticketed).

---

## Findings
## Critical

(none)

## High

## HIGH scripts/validate_hermetization.py:62 — `.github` sanction is not limited to the report-only recorder

**What:** Adding `.github` to the general Tier-1 allowlist permits any new file below `.github/`, including arbitrary workflows, rather than only the intended recorder.  
**Why:** A later change can silently introduce a blocking, privileged, or differently triggered GitHub Actions workflow, violating the stated report-only-only boundary; the positive-only test at `tests/test_validate_hermetization.py:72` does not detect that expansion.  
**Fix direction:** Add a path-level restriction for `.github` that permits only the approved recorder path (and explicitly test disallowed `.github` descendants).

## Medium

(none)

## Low

(none)
---

## Disposition — 2026-08-07 (PRE-2 arc)

**Tally 0/1/0/0.** This is the compensating pass the batch-1 dossier §5 said lane A was owed:
it shipped code-impact (a workflow plus four gate conformances) with no review at all.

### H1 · `.github` sanction is not limited to the report-only recorder — ACCEPTED, NOT FIXED HERE

**The finding is correct on its facts.** `SANCTIONED_TIER1_DIRS` gaining `.github` is a
DIRECTORY-level sanction, so ADR-101 Rule A now permits any new file beneath it — including a
workflow that blocks, that runs privileged, or that triggers differently. The
`report-only`-only boundary is stated in ARCHITECTURE Ch2 and in the workflow's own summary
text, and **nothing mechanizes it**. `tests/test_validate_hermetization.py` is positive-only
on this path, so the expansion would not be detected.

**Why it is not fixed in this arc, stated as a scope judgement rather than a dismissal:**

- The hermetization gate's ruled subject (ADR-101 §3, R3/R4) is the **tree seal** — which
  top-level trees and which `docs/<genre>/` folders may exist, plus audit-name grammar. It has
  never been a per-file content policy for any sanctioned directory, and `scripts/`, `tests/`,
  `deploy/` and `tasks/` all carry the same directory-level sanction. Adding a path allowlist
  for `.github` alone would make it the one exception, which is a design decision for ADR-101,
  not a bug fix.
- PRE-2's scope is fixed at two births (LA-3-remainder and MC-1-FOLLOWUP), and the brief is
  explicit that nothing else is birthed here.

**So it is recorded, not absorbed.** It goes to the architect in the PRE-2 packet as a
candidate row with this artifact as its evidence. The honest current state: *the report-only
boundary is doctrine plus one reviewer's attention, not a mechanism* — which is exactly the
class of claim this repo's [#480] leg exists to stop people asserting.

**Severity read, for the record:** HIGH is defensible as written, though the exploit path
requires an author to add a privileged workflow AND every human/gate reviewing that commit to
miss it. It is a missing-guardrail finding, not a live defect: no such workflow exists today
(`.github/workflows/` holds exactly `report-only-wall.yml`).

### Verified clean in the same pass

The four gate conformances lane A took — the ADR-101 amendment landing in the same commit as
the sanction and its pinning test, the `github-ci` parity row EXTENDED rather than duplicated,
the `2417 → 2418` doc-count bump, and the codemap regen — drew no findings. Neither did the
workflow's trigger syntax, its `continue-on-error` posture on the three measured legs, its
`fetch-depth: 0`, or the exact uv pin.

**Two known-open items were excluded from this review by the focus hints** and are therefore
NOT evidence of absence: the `setup-uv` `python-version-file:` input (LA-2) and the
`mutation-pilot` paths gating (LA-4). Both are fixed in the PRE-2 arc's step 3.
