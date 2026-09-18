# Codex Review — b2-lane1-docs-delete

**Date:** 2026-09-18
**Branch:** `worktree-agent-acdd13c1ff82259b6`
**HEAD:** `035b58c3`
**Diff range:** `main..worktree-agent-acdd13c1ff82259b6`
**Codex version:** codex-cli 0.153.4
**Mode:** doc-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** doc

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### [HIGH] ARCHITECTURE.md:271 — report-only workflow is mislocated

**What:** It calls `report-only-wall.yml` a job in `conductor.yml`; it is a separate workflow at `.github/workflows/report-only-wall.yml`.
**Why:** Readers will inspect or modify the wrong CI surface and conflate the independent report-only wall with conductor behavior.
**Fix direction:** Name `report-only-wall.yml` as the standalone workflow; describe `conductor.yml` separately.

### [HIGH] protocols/PLAYBOOK.md:4106 — stale blocking-hook guidance remains

**What:** The new worktree text correctly says `audit-health` is `stages: [manual]` (1757/1790), but the playbook still says every hook fires automatically and that `audit-health` and `ruff` block commits (also 1275, 1283, 1997, 4108, 6168, and 6235).
**Why:** This gives operators contradictory assurances about which checks ran before a commit and can cause them to rely on protections that no longer execute locally.
**Fix direction:** Reconcile all local-pre-commit claims with the manual-stage/conductor model, retaining only the four live local hooks as automatic gates.

## Medium

### [MEDIUM] ARCHITECTURE.md:124 — generated index is overstated

**What:** It says `ecosystem/organ-index.md` contains failure posture, but the index explicitly says it does not carry that field and points back to Architecture Ch2.
**Why:** The cut removes the per-organ posture map while directing readers to a source that cannot answer “what happens when it says no.”
**Fix direction:** Describe the index as the source for existence, trigger, distribution, and status only; preserve or point to an authoritative per-organ failure-posture source.

## Low

(none)