<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-10

**Date:** 2026-06-10
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-10, confirmed unavailable. Consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-06-09-conformance-nightly-digest.md`
**Prior surviving findings:** 4 (0 high / 3 med / 1 low)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | N1 (med): JOURNAL omission for floor re-pilot commits | V1 verified all 10 recent JOURNAL entries clean against git; JOURNAL updated since 2026-06-09 nightly |
| **RESOLVED** | N4 (low): ARCHITECTURE.md test count stale (329 → 348) | Fixed by commit `f7e026c`; ARCHITECTURE.md now shows "400 collected" (count was later updated to 400 by #141) |
| **PERSISTING** | N2 (med): ARCHITECTURE.md inline/frontmatter timestamp mismatch | Independent check: frontmatter `last_reviewed: 2026-06-09` ≠ inline `Last updated: 2026-06-07`; V2 scan did not surface today |
| **PERSISTING** | N3 (med): CLAUDE.md §8 stale skills-dir claim | Independent check: `.claude/skills/verify/` exists; CLAUDE.md §8 still states "No repo-level skills directory exists yet"; V2 scan did not surface today |
| **NEW** | N5 (med): CONTRIBUTING.md claims "13 self-conformance checks" vs 16 actual | No prior equivalent; added as ALL_CHECKS grew from 13 → 16 via #89 and related work |

**Delta counts:** 2 resolved · 2 persisting (missed by V2 today) · 1 new

**Note on PERSISTING findings:** N2 and N3 from the 2026-06-09 baseline were NOT surfaced by today's V2 verifier scan. They persist in repo state per independent check and are carried forward here for operator awareness. They are excluded from today's surviving-findings count (they are not new survivors this run).

---

## Summary

The .dev-knowledge repository shows one genuine new finding in today's scan: CONTRIBUTING.md still claims the `audit.py health` command runs "13 self-conformance checks" when the ALL_CHECKS registry now contains 16 checks (three added by #89 `check_doc_claims` and related commits since that text was written). ARCHITECTURE.md correctly documents 16 checks; CONTRIBUTING.md has not been updated. The skeptic kill-rate is 0% (no false positives eliminated from 1 raw finding). Two prior findings are confirmed resolved — the JOURNAL gap (N1) and the stale test count (N4, now 400 via #141). Two prior findings persist in repo state (N2 ARCHITECTURE.md timestamp drift, N3 CLAUDE.md skills-dir claim) but were missed by today's V2 scan, indicating a V2 coverage gap on these specific claim types. The checked-clean sweep covered 40 items across JOURNAL history, living-doc claims, and backlog closures.

---

## Findings (PROPOSALS ONLY)

**Raw:** 1 · **Survived skeptic:** 1 · **Killed false positives:** 0

<!-- counts: raw=1 survived=1 killed=0 -->

### High (0)

*(none)*

### Med (1)

**N5** — CONTRIBUTING.md self-conformance check count stale
- **Claim:** CONTRIBUTING.md claims `audit.py health` runs "13 self-conformance checks" but the ALL_CHECKS registry contains 16 checks.
- **Location:** CONTRIBUTING.md:105 and :109
- **Evidence:** `grep -n '13 self-conformance' /home/user/dev-knowledge/CONTRIBUTING.md && awk '/^ALL_CHECKS = \[/,/^\]/' /home/user/dev-knowledge/scripts/audit.py | grep -c 'check_'`
- **Verdict:** contradicted
- **Proposed fix:** Update CONTRIBUTING.md lines 105 and 109 to state "16 self-conformance checks" (or replace with a reference to `python scripts/audit.py checks` so the doc cannot drift again).

### Low (0)

*(none)*

---

## Killed Findings

*(none — 0 killed)*

---

## Checked-and-Clean (40 items — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries):**
- 2026-06-09 #141 closed: commit hashes 9200a70, 0222cfd, f7e026c, 564a708 all present and in order
- 2026-06-09 #89 prose-state-checker: feat/prose-state-checker merge 9bbb415 verified
- 2026-06-09 #77 ruling: chore/77-rescope-split merge 0122c6e verified
- 2026-06-09 #90 git-backlog-verifier: feat/git-backlog-verifier merge b6a8920 verified
- 2026-06-09 #34 review-postures: docs/codify-34-lifecycle merge 342e624 verified
- 2026-06-09 #136 pruning-symmetry: docs/codify-136 merge 2d40505 verified
- 2026-06-09 #135 diagram-form: docs/codify-135 merge c07ebff verified
- 2026-06-09 #115 re-scope: chore/close-115 merge 767cc39 verified
- 2026-06-09 BACKLOG git-resync: chore/backlog-resync merge acc75d4 verified
- 2026-06-09 handoff Phase 2: docs/handoff-2026-06-09 merge 4bbae04 verified

**V2 (living-doc factual claims):**
- ARCHITECTURE.md §Validators: "16 registered checks" in ALL_CHECKS registry — correct
- CONTRIBUTING.md: 8 pre-commit hooks listed and all exist in .pre-commit-config.yaml — correct
- ARCHITECTURE.md: Child repo list (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation) — correct
- VISION.md: Tier system deprecated 2026-05-23 per ADR-38 amendment A5 — correct
- CLAUDE.md: 8 pre-commit hooks listed correctly — correct
- CONTRIBUTING.md: Backlog-id reference format [#id] and closes [#id] pattern — correct
- ARCHITECTURE.md: Layer 2 invariant (never executes orchestration) — correct
- ESSENTIALS.md: Continuous improvement posture described as default — correct
- CONTRIBUTING.md: `git log --grep closes` query command — correct

**V3 (backlog-closure semantic coherence):**
- [#89] prose-vs-state checker shipped — coherent
- [#90] git-backlog verifier shipped — coherent
- [#107] native parallel-session worktree workflow — coherent
- [#121] child methodology floor pilot — coherent
- [#141] Codex hardening follow-ups — coherent
- [#84] two-tier automation doctrine — coherent
- [#91] ARCHITECTURE rewrite layers/organs/automation axes — coherent
- [#92] spec-orchestration fallback rationale to CONTRIBUTING.md — coherent
- [#93] CLAUDE.md pointers to cloud/nightly/spec-orchestration — coherent
- [#101] SessionStart billing-leak sentinel — coherent
- [#104] verify-as-skill shipped — coherent
- [#97] artifact-reader subagent shipped — coherent
- [#113] Wave B changelog-review command — coherent
- [#8] Stop emits additionalContext session-end backpressure — coherent
- [#98] PROPOSALS persistence fix — coherent
- [#85] Wave-A closeout documented — coherent
- [#114] (closure verified as coherent)
- [#115] re-scope — coherent
- [#125] (closure verified as coherent)
- [#78] (closure verified as coherent)
- [#79] (closure verified as coherent)

---

## Next Actions (proposals for operator)

1. **N5** — Update CONTRIBUTING.md lines 105 and 109: `13 self-conformance checks` → `16 self-conformance checks` (or self-documenting pointer to `python scripts/audit.py checks`).
2. **N2 (carry-forward from 2026-06-09)** — Update ARCHITECTURE.md inline `Last updated: 2026-06-07` to match frontmatter `last_reviewed: 2026-06-09`.
3. **N3 (carry-forward from 2026-06-09)** — Update CLAUDE.md §8 to reflect that `.claude/skills/verify/` exists (added by #104).
4. **V2 coverage gap** — V2 missed N2 (inline/frontmatter timestamp consistency) and N3 (skills-dir existence vs CLAUDE.md claim) today; consider extending V2 prompt to explicitly check these two claim classes.

---

## Safety Tripwire

`git status --porcelain` output at review start (pre-branch, clean working tree):

```
(empty — clean working tree)
```

`git status --porcelain` output on branch `claude/conformance-2026-06-10` (post-digest write):

```
?? docs/audits/2026-06-10-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
