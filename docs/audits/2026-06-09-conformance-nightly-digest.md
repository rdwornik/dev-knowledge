<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-09

**Date:** 2026-06-09
**Author:** Claude Code (claude-sonnet-4-6), operator Rob
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-09, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` (Explore subagent) | claude-sonnet-4-6 |

All five stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-07-conformance-nightly-digest.md`
**Prior surviving findings:** 0 (clean — 1 raw, 1 killed false positive)

| Status | Finding | Notes |
|---|---|---|
| **NEW** | N1 (med): Floor re-pilot commits undocumented in JOURNAL | No prior equivalent |
| **NEW** | N2 (med): ARCHITECTURE.md inline/frontmatter timestamp mismatch | Prior N2 was same class — fully resolved 2026-06-06; this is a fresh recurrence on 2026-06-08 |
| **NEW** | N3 (med): CLAUDE.md §8 stale skills-dir claim | No prior equivalent |
| **NEW** | N4 (low): ARCHITECTURE.md test count stale (329 vs 348) | No prior equivalent |

**Delta counts:** 0 resolved · 0 persisting · 4 new

---

## Summary

The .dev-knowledge repository maintains strong documentation-conformance overall, with 3 medium-severity and 1 low-severity finding surviving skeptic review. The skeptic kill-rate is 0% (no false positives eliminated from 4 raw findings), indicating all 4 are genuine discrepancies between living documentation and repository state. The issues are: a JOURNAL gap for a floor re-pilot session committed after the prior session-close entry; a familiar timestamp-drift pattern in ARCHITECTURE.md (frontmatter updated, inline text missed); a stale claim in CLAUDE.md §8 that the repo-level `.claude/skills/` directory does not exist (it was created by #104 on 2026-06-06 but CLAUDE.md's subsequent 2026-06-07 obsolescence pass did not catch it); and a drifted test count (329 vs 348). The checked-clean sweep is thorough: 41 items verified across JOURNAL history, living-doc claims, and backlog closures. No high-severity findings.

---

## Findings (PROPOSALS ONLY)

**Raw:** 4 · **Survived skeptic:** 4 · **Killed false positives:** 0

<!-- counts: raw=4 survived=4 killed=0 -->

### High (0)

*(none)*

### Med (3)

**N1** — JOURNAL omission: floor re-pilot commits undocumented
- **Claim:** Commits 23d89e8 and 9c90797 (2026-06-08 21:39-40) documenting floor re-pilot validation work have no corresponding JOURNAL entry; JOURNAL protocol requires one entry per Claude Code session with newest-first prepend.
- **Location:** JOURNAL.md (gap after final entry at 21:35:55 on 2026-06-08)
- **Evidence:** `git log --oneline HEAD~2..HEAD && grep -c 'floor-repilot' /home/user/dev-knowledge/JOURNAL.md`
- **Verdict:** omitted
- **Proposed fix:** Prepend a new JOURNAL entry documenting the floor re-pilot session (commits 23d89e8, 9c90797, audit file creation, BACKLOG #138/#131 updates).

**N2** — ARCHITECTURE.md inline/frontmatter timestamp mismatch
- **Claim:** ARCHITECTURE.md inline text reads `Last updated: 2026-06-07` while frontmatter `last_reviewed` reads `2026-06-08`; commit 011d304 (2026-06-08) updated the frontmatter but left the inline text unchanged.
- **Location:** ARCHITECTURE.md:16 (inline) vs ARCHITECTURE.md:2 (frontmatter)
- **Evidence:** `grep 'Last updated' /home/user/dev-knowledge/ARCHITECTURE.md && grep 'last_reviewed' /home/user/dev-knowledge/ARCHITECTURE.md`
- **Verdict:** contradicted
- **Proposed fix:** Update ARCHITECTURE.md line 16 from `Last updated: 2026-06-07` to `Last updated: 2026-06-08` to match frontmatter.

**N3** — CLAUDE.md §8 stale skills-dir claim
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds commands/ and rules/ only)" but `.claude/skills/verify/` (verify.py + SKILL.md) was created 2026-06-06 by #104; CLAUDE.md's 2026-06-07 obsolescence pass did not update this claim.
- **Location:** CLAUDE.md ~line 122
- **Evidence:** `find /home/user/dev-knowledge/.claude/skills/ -type f`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 to acknowledge that `.claude/skills/` exists and contains the `verify/` repo-level skill (added by #104).

### Low (1)

**N4** — ARCHITECTURE.md test count stale
- **Claim:** ARCHITECTURE.md §Validators states `329 collected` for the pytest suite; actual current count is 348.
- **Location:** ARCHITECTURE.md ~line 239
- **Evidence:** `grep -r 'def test_' /home/user/dev-knowledge/tests/ | wc -l`
- **Verdict:** contradicted
- **Proposed fix:** Update ARCHITECTURE.md `329 collected` → `348 collected` to reflect current test suite size.

---

## Killed Findings

*(none — 0 killed)*

---

## Checked-and-Clean (41 items — absence of findings is informative)

**V1 (JOURNAL → git, last 10+ entries):**
- 2026-06-08 floor corrective .claude/ placement work documented (commit 5c104e9)
- 2026-06-08 two floor install-note fix-forwards documented (commits 85c89dc, ddc2c89)
- 2026-06-08 #121 floor pilot closeout documented (commit fc82b32)
- 2026-06-07 #121 child methodology floor work documented (commit 0fb6ea9)
- 2026-06-07 #107 worktree workflow documented (commit 0441357)
- 2026-06-07 #134 backlog grooming documented (commit 1ee48e6)
- 2026-06-07 ARCHITECTURE rewrite documented (commit 40b8001)
- 2026-06-07 /ship message handling fix documented (commit 5bfd667)
- 2026-06-07 peer-audit v2 documented (commit cf21651)
- 2026-06-07 Wave B changelog-review documented (commit ceb53a2)
- 2026-06-07 Wave A post-ship closeout documented (commit 5d2abaa)
- 2026-06-07 Wave A writer-policy documented (commit 1e5ae0b)
- 2026-06-07 #84 two-tier automation documented (commit 13e09ac)
- 2026-06-07 Council F1/F2 distillation documented (commit 3505ad7)
- All JOURNAL entries 2026-05-09 through 2026-06-08 21:35 verified against git commits

**V2 (living-doc factual claims):**
- CLAUDE.md §9 8 pre-commit hooks claim matches `.pre-commit-config.yaml` (all 8 hook ids confirmed)
- CLAUDE.md §11 ADRs 76–80 all exist in `docs/decisions/`
- CLAUDE.md §4 ruff enforced pre-commit gate verified in `.pre-commit-config.yaml`
- CLAUDE.md slash commands (`/save`, `/handoff`, `/review-closures`) all exist in `.claude/commands/` or plugin
- ARCHITECTURE.md §Validators 8 pre-commit gates list is correct
- CONTRIBUTING.md 13 self-conformance checks matches `audit.py` ALL_CHECKS registry
- CONTRIBUTING.md HANDOFF_PROCESS v4.4 live confirmed
- VISION.md §Lifecycle correctly cites `scripts/audit.py` per ADR-36
- ESSENTIALS.md `/boot` and `/evolve` correctly marked archived 2026-06-05 Phase-C3

**V3 (backlog-closure semantic coherence):**
- `[#137]` LF-pin hub templates/*.sha256 via .gitattributes (011d304) — coherent
- `[#121]` Child methodology floor Step-5 pilot witnessed (03bb7a2) — coherent
- `[#107]` Native parallel-session worktree workflow (37586d4) — coherent
- `[#101]` SessionStart billing-leak sentinel (20d67ab) — coherent
- `[#104]` verify-as-skill shipped (36b5294) — coherent
- `[#97]` artifact-reader subagent shipped (f8bbf1c) — coherent
- `[#98]` PROPOSALS persistence fix (408f9b6) — coherent
- `[#8]` Stop emits additionalContext session-end backpressure (dfbb585) — coherent
- `[#92]` Add spec-orchestration fallback rationale to CONTRIBUTING.md (6f465b0) — coherent
- `[#93]` Add CLAUDE.md pointers to cloud/nightly/spec-orchestration sections (fa7d3ee) — coherent
- `[#113]` wave B changelog-review command (107f60e) — coherent
- `[#91]` ARCHITECTURE rewrite layers, organs, automation axes (40b8001) — coherent
- `[#84]` Two-tier automation doctrine codified (13e09ac) — coherent
- `[#85]` Wave-A closeout documented (5d2abaa) — coherent
- `[#75]` Corp scoped audit Workflow end-to-end witness (0d69a51) — coherent
- `[#81]` Methodology-conformance Dynamic Workflow shipped (DONE-UNDETECTED, grooming log evidence) — coherent
- `[#14]` ecosystem/ as committed continuous-audit substrate (DONE-UNDETECTED, grooming log evidence) — coherent

---

## Next Actions (proposals for operator)

1. **N1** — Prepend a JOURNAL entry for the 2026-06-08 floor re-pilot session (commits 23d89e8, 9c90797).
2. **N2** — Update ARCHITECTURE.md inline `Last updated: 2026-06-07` → `2026-06-08`.
3. **N3** — Update CLAUDE.md §8 to reflect that `.claude/skills/verify/` exists (added by #104).
4. **N4** (low) — Update ARCHITECTURE.md test count `329 collected` → `348 collected`.

---

## Safety Tripwire

`git status --porcelain` output at review start (pre-branch, clean working tree):

```
(empty — clean working tree)
```

`git status --porcelain` output on branch `claude/conformance-2026-06-09` (post-digest write):

```
?? docs/audits/2026-06-09-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed.
