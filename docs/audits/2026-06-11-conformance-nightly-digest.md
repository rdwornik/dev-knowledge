<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-11

**Date:** 2026-06-11
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-11, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

**Note on background V3:** A second V3 agent ran concurrently and surfaced one additional finding (closures #81/#14 DONE-UNDETECTED with no `closes [#N]` git tag). That finding was excluded per the V3 spec rule: "Do NOT flag mere presence/absence of the 'closes [#id]' TAG — the commit-msg hook already gates that syntax." The grooming-log entry at commit 88ab795 documents both closures with explicit Done-when justification; DONE-UNDETECTED is an operator-approved grooming pattern.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-10-conformance-nightly-digest.md`
**Prior surviving findings:** 1 new survivor (N5 med) + 2 carried-forward as persisting-but-missed (N2, N3)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** (now confirmed) | N2 (med): ARCHITECTURE.md `last_reviewed: 2026-06-10` ≠ inline `Last updated: 2026-06-07` | Missed by V2 on 2026-06-10; confirmed surviving skeptic today |
| **PERSISTING** (now confirmed) | N3 (med): CLAUDE.md §8 claims "No repo-level skills directory exists yet" but `.claude/skills/verify/` exists | Missed by V2 on 2026-06-10; confirmed surviving skeptic today |
| **PERSISTING** (count updated) | N5 (med): CONTRIBUTING.md "13 self-conformance checks" vs actual registry | Count confirmed at 17 today (was reported as 16 in 2026-06-10 baseline — one additional check added); "13" claim further out-of-date |

**Delta counts:** 0 resolved · 3 persisting (all confirmed by today's scan) · 0 new

**Note:** All three surviving findings have now persisted for at least 2 nightly runs. V2 coverage is confirmed stable — no regressions or V2 misses today.

---

## Summary

The .dev-knowledge repository shows consistent documentation drift in three areas, all persisting across multiple nightly runs. The `audit.py` check registry has grown from the 13 count hardcoded in CONTRIBUTING.md to 17 registered checks, a gap of 4 checks that will continue widening as new checks are added. ARCHITECTURE.md carries a frontmatter `last_reviewed: 2026-06-10` stamp that is 4 days ahead of the inline `Last updated: 2026-06-07` marker — the file was reviewed without updating the inline text. CLAUDE.md §8 still declares no repo-level skills directory exists, while `.claude/skills/verify/` (with `verify.py` and `SKILL.md`) has been present since #104. The skeptic kill-rate is 25% (1 of 4 raw findings killed): the V3 finding about #77 CLOSURE-VOIDED was correctly killed as a documented-decision — the reversal is explicitly recorded in commit 88ab795 and the item remains open in BACKLOG.md with its new scope. V1 found the journal clean against git for all 10 recent entries (history boundary: 2026-06-03 for this shallow clone); V3 verified 11+ backlog closures as semantically coherent. The three persisting medium-severity findings are all straightforward documentation updates with no architectural implications.

---

## Findings (PROPOSALS ONLY)

**Raw:** 4 · **Survived skeptic:** 3 · **Killed false positives:** 1

<!-- counts: raw=4 survived=3 killed=1 -->

### High (0)

*(none)*

### Med (3)

**N2** — ARCHITECTURE.md inline/frontmatter timestamp mismatch
- **Claim:** ARCHITECTURE.md has frontmatter `last_reviewed: 2026-06-10` but inline text reads `Last updated: 2026-06-07`
- **Location:** ARCHITECTURE.md lines 2 and 16
- **Evidence:** `head -5 /home/user/dev-knowledge/ARCHITECTURE.md && grep 'Last updated' /home/user/dev-knowledge/ARCHITECTURE.md`
- **Verdict:** contradicted
- **Proposed fix:** Update the inline `> Last updated: \`2026-06-07\`` line in ARCHITECTURE.md to `2026-06-10` to match the frontmatter `last_reviewed` stamp.

**N3** — CLAUDE.md §8 stale repo-level skills claim
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md line ~122 (§8 "Repo-level" bullet)
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 to document the existing `.claude/skills/verify/` directory (shipped by #104), removing the "no repo-level skills directory exists yet" claim.

**N5** — CONTRIBUTING.md self-conformance check count stale
- **Claim:** CONTRIBUTING.md lines 105 and 109 state `audit.py health` runs "the 13 self-conformance checks"
- **Location:** CONTRIBUTING.md:105, CONTRIBUTING.md:109
- **Evidence:** `awk '/^ALL_CHECKS = \[/,/^\]/' /home/user/dev-knowledge/scripts/audit.py | grep -c 'check_'`
- **Verdict:** contradicted
- **Proposed fix:** Update CONTRIBUTING.md lines 105 and 109 to state "17 self-conformance checks" — or replace the hardcoded count with a pointer to `python scripts/audit.py checks` so the doc cannot drift again.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — V3: #77 closure-voided finding
- **Claim:** #77 closure voided; 77e5d7d committed "closes [#77]" but the actual #77 Done-when work was not delivered
- **Kill reason:** `documented-decision`
- **Kill detail:** The commit message of 88ab795 explicitly records "[CLOSURE-VOIDED 2026-06-09: never removed from BACKLOG; 77e5d7d closes [#77] was a misattribution — shipped CONTRIBUTING→v4, not this work; doc-rot checker split into #140]". BACKLOG.md confirms #77 remains open and re-scoped. This is an operator-approved, intentional reversal recorded in both git history and BACKLOG.md. No ADR required — operator judgment recorded in the commit message is sufficient for a single-item closure reversal.

---

## Checked-and-Clean (50+ items — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; shallow-clone boundary: 2026-06-03):**
- 2026-06-11 entry: v5 ships beta — commit 74d83bc (ADR-82, fence tests, HANDOFF_BOOT.md, HANDOFF_PROCESS_v5.md, /handoff v5 mode) verified; 423 pytest pass confirmed in merge commit message
- 2026-06-11 file changes (ADR-82, test_audit.py, HANDOFF_BOOT.md, HANDOFF_PROCESS_v5.md, handoff.md, BACKLOG.md) — verified via 74d83bc --stat
- 2026-06-10 fleet handoff-readiness audit — commit 2c2a1b5 verified
- 2026-06-10 handoff Phase 2 bundle (8 files under budget) — commit 6d05d0f verified
- 2026-06-10 #147 pre-ship verification-organ gate shipped — commits fe405b4/72035e0/b265df3 verified
- 2026-06-10 consolidation-audit record archived — commit e979730 verified
- 2026-06-10 #11 amendment-coherence gate shipped — commit 5b01123 verified
- 2026-06-09 (#141, #89, #90, #34, #136, #135, #115, backlog-resync, handoff Phase 1+2) — all 2026-06-09 commits verified
- 2026-06-08 floor corrective shipped — commits 1447ebb/3f2cc97/4f0bd12/5c104e9 verified
- All referenced SHAs within shallow-history window (2026-06-03+) confirmed present and matching commit messages

**V2 (living-doc factual claims):**
- ARCHITECTURE.md §Validators: "17 registered checks" vs ALL_CHECKS registry — correct
- ARCHITECTURE.md pre-commit gates count (8) — matches .pre-commit-config.yaml
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in .pre-commit-config.yaml
- CONTRIBUTING.md pre-commit hooks table — matches .pre-commit-config.yaml structure
- .claude/commands/ directory contains save.md, handoff.md, changelog-review.md as documented
- CLAUDE.md §7 plugin-provided /review-closures documented correctly
- CLAUDE.md §4 ruff gate enforcement — verified in .pre-commit-config.yaml
- VISION.md: Tier system deprecated 2026-05-23 per ADR-38 amendment A5 — correct
- CONTRIBUTING.md: [#id] and closes [#id] commit-msg pattern — correct
- ARCHITECTURE.md: Layer 2 invariant (no orchestration) — correct
- ESSENTIALS.md: Factual claims about repo structure — correct

**V3 (backlog-closure semantic coherence):**
- [#147] Pre-ship verification-organ gate — coherent
- [#141] Codex doc_claims findings resolved — coherent
- [#90] git↔backlog verifier direction (a) — coherent
- [#89] prose-vs-state checker — coherent
- [#11] amendment-coherence gate — coherent
- [#121] child methodology floor Step-5 pilot — coherent
- [#137] floor placement + install note — coherent
- [#107] worktree workflow — coherent
- [#125] local-writer commit policy — coherent
- [#79] codemap end-state — coherent
- [#88] graphify rejected — coherent
- [#92] CONTRIBUTING + CLAUDE.md staleness closers — coherent

---

## Next Actions (proposals for operator)

1. **N2** — Update ARCHITECTURE.md: change inline `> Last updated: \`2026-06-07\`` to `2026-06-10` to match the frontmatter `last_reviewed` stamp. (Persisting since 2026-06-09.)
2. **N3** — Update CLAUDE.md §8 "Repo-level" bullet to reflect that `.claude/skills/verify/` exists (added by #104). Remove "No repo-level skills directory exists yet" claim. (Persisting since 2026-06-09.)
3. **N5** — Update CONTRIBUTING.md lines 105 and 109: `13 self-conformance checks` → `17 self-conformance checks`, or replace with a self-documenting pointer to `python scripts/audit.py checks`. (Persisting since 2026-06-10; count has since grown further 16→17.)
4. **V2 coverage note (resolved)** — V2 correctly surfaced N2 and N3 today; the prior-run miss was a one-off, not a structural gap.

---

## Safety Tripwire

`git status --porcelain` output before writing this digest (clean working tree on branch `claude/conformance-2026-06-11`):

```
(empty — clean working tree)
```

`git status --porcelain` output after writing this digest:

```
?? docs/audits/2026-06-11-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
