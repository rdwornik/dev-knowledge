<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-14

**Date:** 2026-06-14
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-14, confirmed unavailable. Consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-06-13-conformance-nightly-digest.md`
**Prior surviving findings:** 3 (S3 high persisting, S1 high new/borderline, S2 high new/borderline)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S3 → S1 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/verify/` confirmed present; claim directly contradicted; persisting from 2026-06-11 (**4th consecutive nightly**) |
| **RESOLVED (scope)** | S1 (high, borderline): JOURNAL SHA f578ac4 non-resolvable | V1 correctly read the TOP 10 entries (most recent, 2026-06-12/13) per updated prompt. May 2026 entries are pre-shallow-boundary and out-of-scope per the shallow-history guard; not re-examined this run |
| **RESOLVED (scope)** | S2 (high, borderline): JOURNAL SHA 818a1c6 non-resolvable | Same as S1 — pre-boundary, out-of-scope, not re-examined this run |

**Delta counts:** 2 scope-resolved · 1 persisting · 0 new
**Skeptic kill-rate:** 75% (3 of 4 raw findings killed)

---

## Summary

Continuing strong health since the 2026-06-12 baseline. The two skeptic-borderline SHA findings from 2026-06-13 (S1, S2 — JOURNAL entries citing May 2026 SHAs that predate the shallow-clone boundary) do not reappear this run: V1 was correctly directed to read the TOP 10 entries of the newest-first JOURNAL, which are all 2026-06-12/13 entries well within the shallow-clone boundary, and all corroborate correctly against git. The shallow-history guard marks those pre-boundary entries as out-of-scope — they are scope-resolved rather than fixed.

One finding persists for the **4th consecutive night**: CLAUDE.md §8 "No repo-level skills directory exists yet" is directly contradicted by the actual presence of `.claude/skills/verify/` (containing `SKILL.md` and `verify.py`). This is a simple one-line documentation update.

The skeptic kill-rate of 75% (3/4) reflects healthy filter performance: the test-count discrepancy finding (V2's function-count vs. pytest-collected comparison) was killed as evidence-not-definitive (counting `def test_` functions is not equivalent to `pytest --collect-only`; the claimed 496 was set by commit 6db46ca via actual pytest run). The double-closure finding (V3) was killed as documented-decision (standard work+merge pattern). The JOURNAL count reference (V1) was killed for the same evidence-not-definitive reason.

---

## Findings (PROPOSALS ONLY)

**Raw:** 4 · **Survived skeptic:** 1 · **Killed false positives:** 3

<!-- counts: raw=4 survived=1 killed=3 -->

### High (1)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 4th consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory (`SKILL.md` + `verify.py`). Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Directory visibly exists with verify skill files. Persisting factual contradiction for 4 nights.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — JOURNAL.md:26 "collected **496**" for the #156+#163 integration session
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The evidence_command counts `def test_` function definitions (487), but the JOURNAL records the result of actual `pytest --collect-only` run by the author. Commit 6db46ca explicitly states "collected 494->496" after running real pytest. Parametrize decorators and other pytest collection mechanics mean function count ≠ collected count. Without pytest installed in this environment, the function-count evidence command does not definitively disprove the pytest-collected 496 metric.

**K2** — ARCHITECTURE.md line 273 "pytest unit tests for the validators (**496 collected**)"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Same root cause as K1. The evidence_command (counting `def test_` = 487) is not equivalent to `pytest --collect-only`. Commit 6db46ca (authored by robdwornik running actual pytest) states "collected 494->496". The 1 `@pytest.mark.parametrize` decorator with 5 cases means pytest collects more instances than function definitions. Without pytest installed, the evidence_command cannot definitively disprove the 496 claim.

**K3** — #154 double closure (fcc3363 + 5cc5a24, both 2026-06-11)
- **Kill reason:** `documented-decision`
- **Kill detail:** Standard work+merge closure pattern per ADR-65: 5cc5a24 (work commit, 14:12) removes #154 from BACKLOG.md; fcc3363 (merge commit, 14:18) references the same closure. This is intentional and correct; V3 itself assessed it as "coherent, not an error."

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-13: parallel integration #156+#163 merged as dba11d0 — JOURNAL entry matches git merge
- 2026-06-13: architect-mode v5 handoff refresh — JOURNAL entry matches commit a0aad10
- 2026-06-13: #163 handoff-probe teeth validator — JOURNAL entry matches d6cbac6 and associated commit chain
- 2026-06-12: handoff READMEs collapsed into canonical operator runbook — JOURNAL entry matches merge commits 7770806/66d0293
- 2026-06-12: architect-mode v5 handoff (`-architect`) — JOURNAL entry matches commit 1d52af0
- 2026-06-12: architect-mode v5 handoff (`-session-3`) — matches commit c4c9e61
- 2026-06-12: remote-state truth pass + `docs/handoffs/_references/` reorg — matches merge 31635bb
- 2026-06-12: operator-first v5 handoff README redesign — matches merge 96706b2
- 2026-06-12: v5 architect-mode handoff emitted (`-session-2`) — matches merge fc8608c
- 2026-06-12: #149 flip HANDOFF_PROCESS v5 promoted to canonical — matches merge 22cbd06
- V1 methodology note: correctly read TOP 10 entries (newest-first file; most recent are at top) — no methodology confusion this run

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-06-13` frontmatter — verified (set in 9c257c5)
- ARCHITECTURE.md pre-commit gates count (8) — matches `.pre-commit-config.yaml` (8 hooks)
- ARCHITECTURE.md "19 registered checks" in ALL_CHECKS — verified correct
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in `.pre-commit-config.yaml`
- CLAUDE.md §11: ADR-76 through ADR-80 exist in `docs/decisions/` — verified
- `.claude/commands/` contains `save.md`, `handoff.md`, `changelog-review.md` — verified
- VISION.md tier system deprecated 2026-05-23 per ADR-38 — correct
- CONTRIBUTING.md pre-commit hooks table — matches `.pre-commit-config.yaml`
- ESSENTIALS.md structural claims — correct

**V3 (backlog-closure semantic coherence, since 2026-05-24):**
- #156 durable task-graph closure (dba11d0) — semantically coherent, Done-when met
- #163 handoff-probe teeth validator closure (dba11d0) — semantically coherent, Done-when met
- #90 git-backlog drift verifier — deployed to audit.py health path, verified
- #147 pre-ship verification gate — audit.py ship-gate delivered, verified
- #154 DRIFT-1 test-count restamp — doc_claims MATCH verified
- #149 v5 flip arc closures — 6 atomic coupled-surface removals coherent
- BACKLOG.md validate_backlog gate — passing

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 4 nights)** — Update CLAUDE.md §8: change "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" to document `.claude/skills/verify/` (added by #104). This is a simple one-line doc fix; the directory has been present and contradicting the claim since at least 2026-06-11.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-14-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
