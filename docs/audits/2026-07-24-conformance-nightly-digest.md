<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-24

**Date:** 2026-07-24
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher attempted, auto-denied — not enabled in this cloud runtime; consistent with all prior nightly runs since 2026-06-04.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents). Native Workflow launcher remains unavailable in cloud — consistent with all nightly runs since pilot on 2026-06-04.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Gap:** 40 days (2026-06-14 → 2026-07-24); no conformance digest ran in this interval.
**Prior surviving findings:** 1 (S1 high persisting — CLAUDE.md §8 stale skills claim)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | CLAUDE.md §8 was updated (v2.23+ onward) to document `.claude/skills/verify/` and `check-against-spec`; V2 checked clean this run |
| **NEW** | N1 (low): ARCHITECTURE.md "12 rules" but doc-code-edge.yaml has 13 entries | #286 added `governance-backlog-story-id` but ARCHITECTURE.md count not updated at three locations |
| **NEW** | N2 (low): Hook order ruff/coherence-nudge inverted in ARCHITECTURE.md, CLAUDE.md §9, CONTRIBUTING.md vs actual .pre-commit-config.yaml | Docs consistently say ruff before coherence-nudge; actual config runs coherence-nudge first |
| **NEW** | N3 (med): #292 closed with gate narrower than Done-when specified (ADR-81 violation) | validate_residual_completeness.py is diff-triggered/prospective-only; Done-when required whole-bundle scope; closing commit acknowledges the gap |

**Delta counts:** 1 resolved · 0 persisting · 3 new
**Skeptic kill-rate:** 40% (2 of 5 raw findings killed)

---

## Summary

Overall doc health is good — the large majority of verifiable factual claims check out across VISION.md, ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, ESSENTIALS.md, JOURNAL.md (last 10 entries), and BACKLOG closures (last 3 weeks, 13 closures examined). The prior persisting high-severity finding (CLAUDE.md §8 stale skills claim) is resolved; the repo has evidently been actively maintained.

Three new findings survived the skeptic's 40% kill rate. Two are low-severity documentation drift items from the busy July development period: the "12 rules" count in ARCHITECTURE.md predates the #286 addition (13th rule is present in doc-code-edge.yaml), and the hook execution order in three documentation files inverts the actual .pre-commit-config.yaml order (coherence-nudge runs before ruff, not after). One medium-severity finding concerns the closure of #292: the closing commit itself acknowledges the shipped gate is "NARROWER than the ticket asked," which the skeptic identifies as contradicting ADR-81's prohibition on scope-narrowing.

<!-- counts: raw=5 survived=3 killed=2 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 5 · **Survived skeptic:** 3 · **Killed false positives:** 2

### High (0)

*(none)*

### Med (1)

**N3** — #292 closed with gate scope narrower than Done-when *(NEW)*
- **Claim:** #292 Done-when says the gate "refuses a bundle carrying an unfilled `fill:` marker" (whole-bundle scope); the delivered `validate_residual_completeness.py` is diff-triggered/prospective-only and only checks files changed in the current commit diff
- **Location:** commit `9fc1a8b4eac93ae6223a7e0e67a7f2fb9b4d8003`
- **Evidence:** `git show 9fc1a8b | grep -A6 'shipped gate is NARROWER'`
- **Verdict:** contradicted
- **Proposed fix:** Reopen #292 (or file a new child ticket) requiring the gate to cover whole-bundle scope as the original Done-when specified, per ADR-81's prohibition on scope-narrowing by the executor.
- **Skeptic note:** The closing commit itself writes "the shipped gate is NARROWER than the ticket asked (whole-body markers only, diff-triggered/prospective-only, PROBES.md never inspected)." ADR-81 prohibits scope-narrowing. Open tickets #365 and #366 track downstream defects but do not retroactively validate the closure against the original Done-when clause.

### Low (2)

**N1** — ARCHITECTURE.md "12 rules" stale count *(NEW)*
- **Claim:** ARCHITECTURE.md states "live on 12 rules" for doc-to-code coverage_scope (at lines ~317, ~400, ~411) but `ecosystem/doc-code-edge.yaml` has 13 entries
- **Location:** `ARCHITECTURE.md:317` (also ~400, ~411)
- **Evidence:** `awk '/^coverage_scope:/{flag=1; next} flag && /^[a-z]/{flag=0} flag && /^  - /{print}' /home/user/dev-knowledge/ecosystem/doc-code-edge.yaml`
- **Verdict:** contradicted
- **Proposed fix:** Update all three occurrences of "12 rules" in ARCHITECTURE.md (lines ~317, ~400, ~411) to "13 rules" — the `governance-backlog-story-id` entry added by #286 is the 13th.
- **Skeptic note:** 13 awk-extracted entries confirmed. No ADR documents a deliberate divergence between YAML entry count and prose claim.

**N2** — Hook execution order inverted in documentation *(NEW)*
- **Claim:** ARCHITECTURE.md (~line 422), CLAUDE.md §9 (~line 172), and CONTRIBUTING.md (~line 114) all list ruff before coherence-nudge in hook order, but `.pre-commit-config.yaml` runs coherence-nudge (line 118) before ruff (line 165)
- **Location:** `ARCHITECTURE.md:422`
- **Evidence:** `grep -n 'id: ruff\|id: coherence-nudge\|id: audit-health' /home/user/dev-knowledge/.pre-commit-config.yaml`
- **Verdict:** contradicted
- **Proposed fix:** Swap ruff and coherence-nudge in the hook roster lines of ARCHITECTURE.md (~423), CLAUDE.md §9 (~172–173), and CONTRIBUTING.md (~114–115) to match actual config order: coherence-nudge then ruff.
- **Skeptic note:** grep output is unambiguous (coherence-nudge at line 118, ruff at line 165). The discrepancy appears identically in three independent documentation files.

---

## Killed Findings

**K1** — JOURNAL.md post-session housekeeping commits unrecorded
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Two commits (c591048, f3ead30) exist 9 minutes after the session-wrap commit (199c181): they trim [#405] in BACKLOG.md to clear a self-induced doc_rot warning. The PLAYBOOK §7 ties JOURNAL entries to session-end wrap, not to every subsequent named-branch housekeeping commit. No ADR or PLAYBOOK passage unambiguously requires a new JOURNAL entry for every post-wrap micro-housekeeping branch.

**K2** — ESSENTIALS.md corrections.jsonl logging mechanism unimplemented in repo
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** ENVIRONMENT.md explicitly places corrections.jsonl under `~/.claude/memory/` and annotates it "Auto-created on first correction." It is a user-level, runtime-created artifact — not a repo-level file. Its absence from `/home/user/dev-knowledge` is the expected and documented state per ENVIRONMENT.md.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries — all 2026-07-23):**
- Entry 1: merge e151dcbf exists; [#405] filing confirmed in 199c181; branches worktree-ai-council-handoff/docs/handoff-architect/docs/handoff-execution deleted; 4 branches kept on origin confirmed
- Entry 2: commits 9ab14bb7 and 3e7aea07 present; 11/11 probe re-verification claim supported
- Entry 3: commit c8faf53b exists ('architect bundle 2026-07-23'), merged via 2134abe; [#404] filed in 0810fcd5
- Entry 4: commit 0810fcd5 exists; merge de402b1 wraps the execution handoff
- Entry 5: commit 57d978a2 exists ('Ch4 channel/carrier vocabulary split'), merged 44e47b48
- Entry 6: commit 037d9f08 exists; [#403] filed in same commit
- Entry 7: commits e47b97ba, ab18f30e, c26bb6db all present; 14/14 probe claim verified in c26bb6db
- Entry 8: merges eefb9f9c, fb868199, consolidation 2802e401 all present; [#398] closed in 6d3dd91/963999e; [#386]/[#401]/[#402] confirmed open
- Entry 9: 5 commits present for [#398] lane; [#402] filed in 5b8e11c0
- Entry 10: 6 commits present for ADR-43 doctrine lane; [#401] filed in a094655a; merged via eefb9f9c

**V2 (living-doc factual claims):**
- `.claude/skills/` contains exactly `verify` and `check-against-spec` (CLAUDE.md §8 claim verified — prior persisting finding RESOLVED)
- All 15 pre-commit hook IDs named in CLAUDE.md §9 and CONTRIBUTING.md exist in `.pre-commit-config.yaml`
- ADRs 99–103 all exist in `docs/decisions/` (CLAUDE.md §11 via generated fragment)
- `docs/decisions/transcripts/` confirmed deleted (CLAUDE.md §4 retirement record accurate)
- 31 registered checks in `scripts/audit.py` ALL_CHECKS matching `ecosystem/doc-counts.md`
- 15 pre-commit gates matching `ecosystem/doc-counts.md`
- `editor-config` carrier is `implemented: false` in `deploy/manifest-v1.4.0.yaml` (ARCHITECTURE.md accurate)
- 5 deploy carriers in `deploy/` (carrier_floor, carrier_globalconfig, carrier_mesh, carrier_plugin, carrier_precommit)
- `win-tooling` in `ecosystem/index.yaml` (5th non-hub entry)
- `audit.py` has cmd_run, cmd_repo, cmd_health, cmd_registry commands (VISION.md accurate)
- `protocols/SESSION_SETUP.md` and `protocols/HANDOFF_BOOT.md` exist
- `HANDOFF_PROCESS.md` is version 5.7, status: stable (CONTRIBUTING.md accurate)
- 5 SessionStart hooks in `.claude/settings.json` match CLAUDE.md §9 list
- `docs/decisions/archive/` exists with ADR-40 and ADR-52
- `docs/decisions/README.md` exists

**V3 (BACKLOG closures, last 3 weeks — 13 closures examined):**
- #321 (ARCHITECTURE Ch2 organ rows) — semantically coherent, Done-when met
- #395 (logs/ UPPERCASE-KEBAB rename) — coherent, convention codified in CLAUDE.md §9 v2.45
- #302 (block-ff-push to n=2 consumers) — coherent, FIRING witnessed and recorded
- #309 (backlog-id-on-close to consumers) — coherent, OR-clause discharged
- #131 (repo-onboarding install sequence) — coherent, pilot recorded for n=2
- #314 (protocols/README.md genre split) — coherent, both consumers carry protocols/
- #355 (fleet_parity ignores-inherited-git-dir) — coherent, gate confirmed
- #372 (_select_active_bundle add-date ranking) — coherent, 4 test classes present
- #384 (fleet_analytics run + hotspot frames) — coherent, #393/#394 tickets filed
- #398 (intake status enum) — coherent, all 6 off-canon docs migrated
- #306, #307, #328 (validate_hermetization, intake-index-freshness, parity-surfaces.yaml) — disk-met artifacts confirmed

---

## Next Actions (proposals for operator)

1. **N3 (med)** — Reopen #292 or file a child ticket specifying the required whole-bundle scope (validate_residual_completeness.py checking all handoff bundle files, not just the current diff), per ADR-81's prohibition on scope-narrowing. Open #365 and #366 may already cover specific defect facets — confirm whether they collectively discharge the original Done-when.

2. **N1 (low)** — Update ARCHITECTURE.md: change "12 rules" to "13 rules" at three locations (~317, ~400, ~411). The `governance-backlog-story-id` entry added by #286 is the uncounted 13th doc→code edge rule.

3. **N2 (low)** — Fix hook execution order in ARCHITECTURE.md (~422), CLAUDE.md §9 (~172), and CONTRIBUTING.md (~114): swap ruff and coherence-nudge to match actual `.pre-commit-config.yaml` order (coherence-nudge at line 118, ruff at line 165).

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-24-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
