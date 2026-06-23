<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-23

**Date:** 2026-06-23
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-23, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high — CLAUDE.md §8 stale skills claim, persisting since 2026-06-11)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/` confirmed present with TWO directories (check-against-spec + verify); claim directly contradicted; persisting from 2026-06-11 (**5th+ consecutive nightly**) |

**Delta counts:** 0 resolved · 1 persisting · 0 new
**Skeptic kill-rate:** 67% (2 of 3 raw findings killed)

---

## Summary

Repo health remains strong. The 2026-06-22 sessions added substantial new work under #194 (doc→code edge: naming convention decided, 3 starters annotated, Arc-1 Phase-A/B coverage gate, and two regression test hardening arcs), with all JOURNAL claims verified against git — every commit SHA corroborates its entry, counts are consistent, and the branch merge topology is correct.

V3 found zero backlog-closure coherence issues: recent closures (#47, #10) both met their stated Done-when criteria, and the newly added #201/#202/#203 deferred-tail items appear correctly in BACKLOG.md.

The skeptic killed 2 of 3 raw findings. V1 filed a suppression-level item (pre-shallow-boundary JOURNAL entries) incorrectly as an "omitted" finding despite the verifier's own note flagging it as out-of-scope — killed as evidence-not-definitive. V2 raised a pytest count discrepancy (793 claimed vs 343 cloud-collected), but the cloud environment is missing Python dependencies, making `pytest --collect-only` output unreliable; the 793 count was verified by the session author via real pytest on 2026-06-22 with no test file changes since — killed as evidence-not-definitive.

One finding persists for the **5th+ consecutive night**: CLAUDE.md §8 "No repo-level skills directory exists yet" is directly contradicted by `.claude/skills/` containing both `check-against-spec/` and `verify/` subdirectories. The directory has grown since initial detection: last baseline found only `verify/`; today it also contains `check-against-spec/`. This is a straightforward documentation update.

---

## Findings (PROPOSALS ONLY)

**Raw:** 3 · **Survived skeptic:** 1 · **Killed false positives:** 2

<!-- counts: raw=3 survived=1 killed=2 -->

### High (1)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th+ consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:125
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document `.claude/skills/check-against-spec/` and `.claude/skills/verify/`. Remove the "No repo-level skills directory exists yet" sentence and list both skills.
- **Skeptic note:** Directory visibly exists with two inhabited subdirectories (verify + check-against-spec). Direct filesystem proof. Persisting factual contradiction for 5+ consecutive nights. Skills have grown since initial detection.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — JOURNAL entries from 2026-05-09 back are "omitted" from verifiable history
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The finding is internally contradictory: verdict=\"omitted\" conflicts with the verifier's own note stating \"OUT-OF-SCOPE: not contradicted, not unsupported, simply not verifiable against available history.\" The shallow-history guard in V1's prompt explicitly requires suppressing (not filing) such entries. This was filed incorrectly by V1 and should have been a checked_clean suppression, not a finding.

**K2** — ARCHITECTURE.md claims \"793 collected\" but cloud pytest returned 343 with 16 errors
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The evidence_command runs pytest in a cloud environment missing Python dependencies (click, etc.), causing 16 import errors that prevent full collection. The 793 count was set by commit 25394c9 (2026-06-22) verified by the session author running real pytest; the JOURNAL Phase-B entry explicitly confirms \"Collection stays **793** (only the decorator removed, not the test); pytest moved from '791 passed / 1 xfailed' → **792 passed / 1 skipped**\" (793 collected). No test files were added or removed in any subsequent commit. Cloud env's 343 is an artifact of missing deps, not a real regression.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, within shallow-clone boundary ~2026-06-22):**
- 2026-06-22 doc-legibility (#194): commit a4c568c exists; yaml + test docstring changes, pytest 21 passed — JOURNAL entry matches git
- 2026-06-22 Arc-1 Phase-B (#194): commits 25394c9 + f1d2e77 exist; xfail decorator removed; 5/5 edges resolved; 793 collected — matches JOURNAL
- 2026-06-22 Arc-1 Phase-A (#194): commit 19f0176 exists; xfail-strict coverage test added; 2/5 broken inventory — matches JOURNAL
- 2026-06-22 edge test-hardening (#194): commit 2e40c76 exists; cp1252-safe + real-starter regression tests added (+4 to 792) — matches JOURNAL
- 2026-06-22 Phase-2 sub-arc 2 (#194): commits 6a4d2a6/36fa2ad/633e44a/88efb5a exist; ADR-89 OQ1 amended; 3 starters annotated; ESSENTIALS/PLAYBOOK teaching — matches JOURNAL
- 2026-06-21 Phase-2 sub-arc 1 (#194): commits 8052c51/2eed4bf exist; doc_code_edge advisory check #23 live — matches JOURNAL
- All JOURNAL entry ordering (newest-first) confirmed correct vs git log chronology
- All commit SHAs referenced in JOURNAL verified to exist in git history

**V2 (living-doc factual claims):**
- ARCHITECTURE.md pre-commit gates count (10) — matches `.pre-commit-config.yaml` (10 hooks including block-ff-push)
- ARCHITECTURE.md \"23 registered checks\" in ALL_CHECKS — verified in audit.py
- CLAUDE.md §9 pre-commit hook list — matches `.pre-commit-config.yaml`
- CONTRIBUTING.md pre-commit hooks table — matches `.pre-commit-config.yaml`
- ESSENTIALS.md `last_reviewed: 2026-06-22` frontmatter — consistent with sub-arc 2 genuine re-read claimed in JOURNAL
- `.claude/commands/` contains `save.md`, `handoff.md`, `changelog-review.md`, `override.md` — verified
- ARCHITECTURE.md doc→code edge count (5 resolved) — consistent with Phase-B result

**V3 (backlog-closure semantic coherence, ~3 weeks):**
- #47 repos-absent-from-registry classification — Done-when met (d95d6ce)
- #10 TOKEN-LOG path qualification — both Done-when legs met (7286707 + 8a5ae7f)
- BACKLOG #201/#202/#203 (new deferred tail items) — correctly present per JOURNAL description
- validate_backlog: 86 tasks OK, 0 warnings
- No semantically incoherent closures found
- No omitted closures (done-work without backlog entry) detected

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 5+ nights)** — Update CLAUDE.md §8: the "No repo-level skills directory exists yet" sentence is false. `.claude/skills/` now holds two skills: `verify/` (SKILL.md + verify.py) and `check-against-spec/`. Update the bullet to list both. This is a simple 1–2 line documentation fix. The directory has been contradicting the claim since at least 2026-06-11 (9+ days).

---

## Safety Tripwire

`git status --porcelain` output at run time (working tree must show only the new digest file):

```
(empty — clean working tree; digest written via GitHub API to branch claude/conformance-2026-06-23)
```

No tracked files modified in the main working tree during this run. Digest delivered exclusively via `mcp__github__push_files` to the conformance branch. If this PR shows any modification to tracked files other than `docs/audits/2026-06-23-conformance-nightly-digest.md`, that is a safety breach requiring operator investigation before merge.
