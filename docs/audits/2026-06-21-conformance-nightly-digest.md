<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-21

**Date:** 2026-06-21
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-21, confirmed unavailable. Consistent with all prior nightly runs.)

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
**Prior surviving findings:** 1 (CLAUDE.md §8 skills claim, high, persisting 4 consecutive nights)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | CLAUDE.md §8 "No repo-level skills directory exists yet" | `.claude/skills/` (with `verify/` + `check-against-spec/`) confirmed present since commit c5a98ba (2026-06-18); this is the **5th consecutive nightly**. Severity assessed as `med` this run (prior nights: `high`). |

**Delta counts:** 0 resolved · 1 persisting · 0 new
**Skeptic kill-rate:** 67% (2 of 3 raw findings killed)

---

## Summary

Continuing strong repo health. The prior baseline's single survivor persists for the **5th consecutive night**: CLAUDE.md §8 claims no repo-level skills directory exists, yet `.claude/skills/verify/` and `.claude/skills/check-against-spec/` have been present since commit c5a98ba (2026-06-18). CLAUDE.md was re-reviewed and stamped on 2026-06-19 (v2.19) and again on 2026-06-20 (v2.20), but §8 was not updated in either review pass. This is a simple one-line doc fix.

V1 (JOURNAL vs git) came back entirely clean: all 10 most recent JOURNAL entries (covering the substantial 2026-06-20 activity — block-ff-push gate #153, refscan precision #199, removal-closure spike #196, session-wrap audit, reverse-dep oracle #193, undeclared-edge scan #179) corroborate fully against git history. No omissions or contradictions.

The skeptic kill-rate of 67% (2/3) reflects healthy filter performance. The version-history-count finding (CLAUDE.md §12 v2.20 entry referencing "739→760") was killed as true-but-irrelevant: §12 is a historical changelog, not a current-state claim; ARCHITECTURE.md is the authoritative current-count source and was correct at 772 when checked. The V3 finding about #153 staying open without a closing commit was also killed as true-but-irrelevant: the item correctly remains open per its Done-when clause (scope-boundary + methodology-reach undone), and the commits themselves document this intent ("advances #153 — prevent half ... scope-boundary + reach remain open").

---

## Findings (PROPOSALS ONLY)

**Raw:** 3 · **Survived skeptic:** 1 · **Killed false positives:** 2

<!-- counts: raw=3 survived=1 killed=2 -->

### High (0)

*(none)*

### Med (1)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th consecutive nightly; severity downgraded high→med this run)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/` directory with its two skills: `verify/` (`SKILL.md` + `verify.py`) and `check-against-spec/`. Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Genuine drift in a living doc. `.claude/skills/` was added by commit c5a98ba (2026-06-18) and CLAUDE.md's own §4 promises living docs are kept current via re-review. CLAUDE.md was reviewed and re-stamped on 2026-06-19 (v2.19) and 2026-06-20 (v2.20) without updating §8. This is a broken promise on a reviewable factual claim.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — CLAUDE.md §12 v2.20 version-history entry states "collected 739→760" but ARCHITECTURE.md now shows 772
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** §12 is "Section history" — a historical version log, not a current-state claim. The v2.20 entry documents what was true at v2.20 release time. Verified: commit 212bb2a (2026-06-20 22:14:23) synced CLAUDE.md v2.20 with ARCHITECTURE.md which showed exactly 760 collected at that moment. Commit d752179 (2026-06-20 23:11:42) then advanced the count to 772. Version-history entries are not required to track all subsequent changes; ARCHITECTURE.md (not §12) is the authoritative current-count source. This is a finding-design error, not a documentation defect.

**K2** — #153 shipped block-ff-push pre-push hook + tests without closing BACKLOG item or recording intermediate milestone
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The item CORRECTLY remains open per BACKLOG.md #153's explicit Done-when scope (scope-boundary + methodology-reach remain undone). The commits document this intent: fbab423 says "advances #153 — prevent half of core-invariant #5; scope-boundary + reach remain open." This is intentional partial delivery of a multi-part work item. No closure is warranted; the current open state is correct per ADR-65 (done-items-leave only when done-when is fully met).

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; all 2026-06-20; within shallow-clone boundary):**
- 2026-06-20: refscan precision #199 — feat(scan) commit f484a9a prunes immutable zones + gitignored paths; scan result 245/104→12/4; 748 passed/3 skipped; JOURNAL matches
- 2026-06-20: removal-closure spike #196 — design proposal + feasibility verdict (e31de4a); docs/audits/2026-06-20-removal-closure-spike-findings.md created; JOURNAL matches
- 2026-06-20: block-ff-push pre-push gate #153 — 5 commits (94652fd, 6d1c776, 44eca4a, 13d795d, 212bb2a); merge fbab423; 739→760 tests; JOURNAL matches
- 2026-06-20: session-wrap mega-audit — close #197, #193/#179 inventory, handoff bundle dd98524; ship-gate GREEN; JOURNAL matches
- 2026-06-20: reverse-dep oracle #193 — pyright code→code oracle (80afcba); 21 tests; ADR-89 OQ2 resolution; JOURNAL matches
- 2026-06-20: undeclared-edge scan #179 — prose-only dependency scan (eb603d4); 18 tests; FC2 implementation; JOURNAL matches
- 2026-06-20: dependency-arc backlog reconcile — 6 items filed (#193–#198); validate_backlog passing; JOURNAL matches
- All 10 entries fully corroborated against git history; no omissions of significant merged work

**V2 (living-doc factual claims):**
- CLAUDE.md §7 user-level commands: /session-summary, /boot (archived), /evolve (archived), /codex-review — verified
- CLAUDE.md §7 repo-level commands: /save, /handoff — `.claude/commands/` confirmed
- CLAUDE.md §9 pre-commit hooks (10): all 10 hooks verified in `.pre-commit-config.yaml`
- CLAUDE.md §11 ADR list (76–80): ADR-76 through ADR-80 exist in `docs/decisions/`
- ARCHITECTURE.md §Organ map pre-commit gates count (10) — matches `.pre-commit-config.yaml`
- ARCHITECTURE.md `last_reviewed: 2026-06-20` — confirmed in file
- CLAUDE.md `last_reviewed: 2026-06-20` — confirmed in file
- VISION.md `last_reviewed: 2026-06-19` — confirmed in file
- CONTRIBUTING.md `last_reviewed: 2026-06-17` — confirmed in file
- ESSENTIALS.md `last_reviewed: 2026-06-19` — confirmed in file

**V3 (backlog-closure semantic coherence, since 2026-05-31):**
- #199: prune immutable zones from undeclared-edge scan — diff delivers exclusion logic + 30 tests; Done-when met (scan excludes immutable zones, candidate list actionable)
- #196: removal-closure spike — design doc (docs/audits/2026-06-20-removal-closure-spike-findings.md) + feasibility verdict; Done-when met
- #197: §4.4 ship-gate disposition — two commits dispositioned + ship-gate GREEN; Done-when met
- #179: undeclared-edge scan — scripts/scan_undeclared_edges.py with 18 tests; FC2 implementation delivered; Done-when met
- #193: Pyright reverse-dep oracle — scripts/reverse_dep_oracle.py with 21 tests + provenance; ADR-89 OQ2 resolved; Done-when met

---

## Next Actions (proposals for operator)

1. **S1 (med, persisting 5 nights)** — Update CLAUDE.md §8: replace "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" with documentation of the actual `.claude/skills/` directory and its two skills: `verify/` (verify.py + SKILL.md) and `check-against-spec/`. This is a simple one-line doc fix; the directory has been present since 2026-06-18 and through two subsequent re-reviews.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-21-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
