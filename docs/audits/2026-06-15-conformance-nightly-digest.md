<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-15

**Date:** 2026-06-15
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-15, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent, parallel + background) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent, two passes) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high — CLAUDE.md §8 skills-dir claim, 4th consecutive night)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/verify/` confirmed present; claim directly contradicted; persisting from 2026-06-11 (**5th consecutive nightly**) |
| **NEW** | S2 (high): VISION.md `last_reviewed: 2026-06-04` predates last edit 2026-06-09 | File edited by commit b6a8920 on 2026-06-09 but stamp never updated; audit.py check #10 (`check_canonical_freshness`) will FAIL on this; not previously flagged |

**Delta counts:** 0 resolved · 1 persisting · 1 new
**Skeptic kill-rate:** 0% (0 of 2 raw findings killed)

---

## Summary

Two high-severity findings this run — one persisting, one new.

**Persisting (5th night):** CLAUDE.md §8 "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" is directly contradicted by `.claude/skills/verify/` (containing `SKILL.md` and `verify.py`, created 2026-06-09 in commit b6a8920). This is a simple one-line doc fix. Now on its 5th consecutive nightly flag.

**New:** VISION.md carries `last_reviewed: 2026-06-04` (line 4) but was last edited on 2026-06-09 (commit b6a8920, which merged feat/git-backlog-verifier — the same commit that created `.claude/skills/verify/`). VISION.md is explicitly listed in `_FRESHNESS_FILES` in `scripts/audit.py` (line 149), and `check_canonical_freshness` (check #10) implements the A2 check: `if git_date is not None and reviewed < git_date` → FAIL. The audit-health pre-commit gate would block commits made while this drift exists, but this edit landed before the freshness-gate covered it or was missed in the review. Both findings originate from the same root commit (b6a8920, 2026-06-09) — the skills-dir creation also coincided with the VISION.md edit that was not re-reviewed.

The skeptic kill-rate of 0% this run is unusual but reflects that both findings carry direct, re-confirmed evidence: directory existence (`ls .claude/skills/`) and git-date vs. stamp comparison — no ambiguity, no documented decision that would excuse them.

---

## Findings (PROPOSALS ONLY)

**Raw:** 2 · **Survived skeptic:** 2 · **Killed false positives:** 0

<!-- counts: raw=2 survived=2 killed=0 -->

### High (2)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la .claude/skills/` — directory exists with `verify/` subdirectory; `git log --reverse --oneline -- '.claude/skills/'` — first commit b6a8920 on 2026-06-09
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory (`SKILL.md` + `verify.py`). Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Directory visibly exists with verify skill files. Persisting factual contradiction for 5 nights. No ADR documents an intentional decision to keep this stale claim.

**S2** — VISION.md `last_reviewed` stamp predates last edit *(NEW)*
- **Claim:** VISION.md `last_reviewed: 2026-06-04` (line 4) is current
- **Location:** VISION.md:4
- **Evidence:** `git log --format='%ai' -1 -- VISION.md` → `2026-06-09 19:34:06 +0200` (commit b6a8920); `last_reviewed: 2026-06-04` predates by 5 days
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end, confirm it is accurate (or update any stale claims), then bump `last_reviewed` to 2026-06-15 (or the date of genuine review).
- **Skeptic note:** VISION.md is in `_FRESHNESS_FILES` (audit.py line 149); check_canonical_freshness (check #10) will FAIL this file. The edit and the CLAUDE.md skills-dir creation both occurred in commit b6a8920 — the review stamp was not updated when VISION.md was touched. Confirmed via audit.py A2 logic (lines 776-780).

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

*(none — 0 killed this run)*

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-14: collision graph encoded with serialize-group (commits 89f0ed0 → d849bf9) — JOURNAL entry matches git merge
- 2026-06-14: ADR-66 task-graph amendment ratified (commits 0e9cf6f → 086aae2) — JOURNAL entry matches git
- 2026-06-14: Q9 automation-writer isolation shipped (commits 0ca36f1 → 374e602 merged 621aafc) — JOURNAL entry matches git
- 2026-06-13: parallel integration #156/#163 merged as dba11d0 — JOURNAL entry matches git merge
- 2026-06-13: architect-mode v5 handoff refresh generated — JOURNAL entry matches commit a0aad10 and associated handoff dir
- 2026-06-13: durable task-graph with depends-on/serialize-group (commit 89f0ed0) — JOURNAL matches
- 2026-06-13: #163 handoff-probe teeth validator shipped (9aae4e1 + 7a4795e) — JOURNAL matches
- 2026-06-12: remote-state truth pass + _references reorg (01a8a96, ac796bf) — JOURNAL matches
- 2026-06-12: architect-mode v5 handoff bundles generated (2026-06-12-dev-knowledge-architect, session, session-2, session-3) — JOURNAL matches
- All commits 2026-06-03 to 2026-06-15 accounted for in JOURNAL entries — no significant omitted work found

**V2 (living-doc factual claims):**
- ARCHITECTURE.md §Validators: "19 registered checks" — verified against ALL_CHECKS list in scripts/audit.py
- ARCHITECTURE.md: "8 pre-commit gates" — matches .pre-commit-config.yaml (8 hooks)
- CLAUDE.md §7: `/save` and `/handoff` are Repo-level commands in `.claude/commands/` — verified
- CLAUDE.md §7: `/review-closures` is Plugin-provided (not in `.claude/commands/`; plugin enabled in settings.json) — verified
- CLAUDE.md §8: `tier1-lifecycle@dev-knowledge-methodology` plugin enabled — verified in .claude/settings.json
- CLAUDE.md §9: 8 pre-commit hooks listed — all 8 verified in .pre-commit-config.yaml
- CLAUDE.md §11: ADR-76 through ADR-80 exist in `docs/decisions/` — verified
- CONTRIBUTING.md: `config/requirements-dev.txt` exists — verified
- ARCHITECTURE.md: 57 ADRs in `docs/decisions/` — verified (`find docs/decisions -name 'ADR-*.md' | wc -l = 57`)
- VISION.md: tier system deprecated 2026-05-23 per ADR-38 — verified
- VISION.md and ARCHITECTURE.md: root README.md deleted — verified (file does not exist)
- CLAUDE.md §1: `docs/handoffs/README.md` exists as canonical operator runbook — verified
- ARCHITECTURE.md: Layer 2 never executes invariant — scripts/audit.py confirmed read-only (header comment verified)
- ESSENTIALS.md: does NOT carry last_reviewed (confirmed excluded from _FRESHNESS_FILES)

**V3 (backlog-closure semantic coherence, since 2026-05-24):**
- #150 closure (d849bf9): encode collision graph — BACKLOG item scope matches diff
- #154 closure (5cc5a24): DRIFT-1 test-count restamp — doc_claims MATCH verified, architecture counts re-stamped
- #147 closure: ship-gate verification gate — audit.py +130 lines delivered, semantically coherent
- #11 closure (5193de5): amendment-coherence gate — check_amendment_coherence delivered, ADR-81 DoD met
- #111 closure: PLAYBOOK prompt-format pack (a)+(b) — both parts confirmed in grooming log as shipped
- All checked closures remove items from BACKLOG.md per ADR-65 (done-items-leave)

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 5 nights)** — Update CLAUDE.md §8: change "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" to document `.claude/skills/verify/` (added by #90/#104). Simple one-line doc fix; directory has been present and contradicting the claim since 2026-06-09.

2. **S2 (high, new)** — Re-read VISION.md end-to-end and bump `last_reviewed` if accurate (or update any stale claims found). Root cause: commit b6a8920 (2026-06-09) edited VISION.md as a side-effect of the feat/git-backlog-verifier merge but the review stamp was not updated. The audit-health pre-commit gate will FAIL until this is resolved.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
(empty — clean working tree before digest file was created)
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
