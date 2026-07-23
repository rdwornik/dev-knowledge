<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-23

**Date:** 2026-07-23
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-07-23, confirmed unavailable. Consistent with all prior nightly runs since 2026-06-04.)

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
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 stale skills claim, persisting 4 nights)
**Gap since prior run:** 39 days (2026-06-14 → 2026-07-23)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high, 4-night): CLAUDE.md §8 "No repo-level skills directory exists yet" | §8 was updated in CLAUDE.md v2.38 (2026-07-12) to document `.claude/skills/verify` + `check-against-spec`. No longer contradicted. |
| **NEW** | ARCHITECTURE.md hard-codes '12 rules' in 3 locations | coverage_scope in ecosystem/doc-code-edge.yaml now has 13 entries; 13th added via #286 post-documentation |
| **NEW** | ESSENTIALS.md:138 describes corrections.jsonl auto-promotion as operational | Mechanism never built; ADR-35 explicitly defers it ("manual review now; automation per ADR-36 future") |

**Delta counts:** 1 resolved · 0 persisting · 2 new
**Skeptic kill-rate:** 0% (0 of 2 raw findings killed — both confirmed by direct evidence re-run)

---

## Summary

After a 39-day gap since the last run (2026-06-14), this digest covers a period of substantial repo activity: ADRs 99–103 ratified, the transcripts/ directory deleted (operator ruling), multiple fleet-parity and Tier-1 closure-loop advances, and the CLAUDE.md v2.38–v2.46 arc. The prior persisting finding (CLAUDE.md §8 skills-directory claim) is **resolved** — the section was corrected in v2.38 (2026-07-12) and accurately documents `.claude/skills/` today.

Two new findings survive the skeptic with a 0% kill rate. S1 (med) is a hardcoded count drift: ARCHITECTURE.md refers to "12 rules" in three prose locations but ecosystem/doc-code-edge.yaml's coverage_scope now has 13 entries (governance-backlog-story-id added via #286 post-documentation, no automated gate catches this count). S2 (low) is an aspirational-presented-as-operational claim in ESSENTIALS.md: the corrections.jsonl → auto-promotion Stop hook is described as current fact but ADR-35 explicitly defers its automation, no script implements it, and corrections.jsonl does not exist on disk.

V1 (JOURNAL vs git) verified 10 entries covering the 2026-07-21–23 night-batch arc — every SHA corroborated, all clean. V3 (BACKLOG closures) verified 12 closures since 2026-07-02 — all semantically coherent, Done-when clauses met. The 0% skeptic kill rate reflects that both surviving findings are directly confirmed by command output with no ADR-documented exception covering them.

---

## Findings (PROPOSALS ONLY)

<!-- counts: raw=2 survived=2 killed=0 -->

### High (0)

*(none)*

### Med (1)

**S1** — ARCHITECTURE.md hardcoded '12 rules' count stale *(NEW)*
- **Claim:** ARCHITECTURE.md states "12 rules" for the doc→code coverage_scope at lines 314, 397, and 408
- **Location:** ARCHITECTURE.md:314 (also :397, :408)
- **Evidence:** `python3 -c "import yaml; data=yaml.safe_load(open('/home/user/dev-knowledge/ecosystem/doc-code-edge.yaml')); print(len(data['coverage_scope']))"`
- **Verdict:** contradicted — returns 13, not 12
- **Proposed fix:** Replace '12 rules' with '13 rules' at ARCHITECTURE.md lines 314, 397, and 408; the 13th entry (governance-backlog-story-id) was added via #286 after these prose lines were written.
- **Skeptic note:** Evidence re-run directly confirmed 13 entries. No ADR documents this count as acknowledged-stale. The drift is invisible to automated gates (validate_doc_claims doesn't track this count).

### Low (1)

**S2** — ESSENTIALS.md corrections.jsonl auto-promotion described as operational *(NEW)*
- **Claim:** "every correction logged to corrections.jsonl → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook)"
- **Location:** protocols/ESSENTIALS.md:138
- **Evidence:** `grep -rn 'corrections' /home/user/dev-knowledge/scripts/session_end_backpressure.py; find /home/user/dev-knowledge -name 'corrections.jsonl' 2>/dev/null`
- **Verdict:** unsupported — session_end_backpressure.py (the actual wired Stop hook) has zero references to 'corrections'; corrections.jsonl does not exist anywhere in the repo
- **Proposed fix:** Update ESSENTIALS.md:138 to qualify as planned/aspirational, e.g. add "(designed; auto-promotion deferred, not yet built — ADR-35/36 backstop)".
- **Skeptic note:** ADR-35 explicitly states "(manual review now; automation per ADR-36 future)"; ADR-70 lists the feedback-loop machinery as open backlog items. ESSENTIALS.md describes an aspirational design as current operational fact.

---

## Killed Findings

*(none — skeptic kill rate 0%)*

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; 2026-07-21 – 2026-07-23):**
- Entry 1 (NIGHT BATCH 2026-07-23): branch docs/night-batch-audit-0722 merged as 624b048 — CONFIRMED
- Entry 1: transcripts/ deletion commit b4435fa (51 files / 47,748 deletions); JOURNAL caught the commit-message overstatement and corrected it — CONFIRMED
- Entry 1: living-docs currency commit 9a04e23c (ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, decisions README) — CONFIRMED
- Entry 1: [#400] filed in commit 0d461e5b — CONFIRMED
- Entry 2 (RUNBOOKS LANE 2026-07-22): docs/runbooks/repo-onboarding.md → protocols/REPO_ONBOARDING.md in 12f506ee; doc-counts regen (1733→1734) — CONFIRMED
- Entry 3 (HYGIENE LANE 2026-07-22): 7 commits on chore/hygiene-pre-handoff (af63a0f3..9b175035), merged f1c9911; [#395] closed 2c48714, [#321] closed f865abf — all CONFIRMED
- Entry 4 ([#384] CLOSED 2026-07-22): closed in 37844c2, merged ffba8dd — CONFIRMED
- Entry 5 (NIGHT-BATCH INTEGRATION 2026-07-22): core SHAs c8de721, a6b326f, 09c50cc, 938b01c, 423a372e, 09e4d70 — all CONFIRMED
- Entry 6 ([#386] PLAYBOOK 2026-07-22): 4 commits + merge db878f4; §21 'The delivery loop' heading — CONFIRMED
- Entry 7 (L5a analytics 2026-07-22): commit 5631660, scripts/fleet_analytics.py exists — CONFIRMED
- Entry 8 (North-Star ingestion 2026-07-21): b73319ef, docs/intake/2026-07-21-func-fleet-north-star.md exists — CONFIRMED
- Entry 9 (integration 2026-07-21): three merges 35421081, 85b1a9cc, 323b8bd9 — all confirmed in git
- Entry 10 (ai-council cross-repo handoff 2026-07-21): 36cf6b42 — CONFIRMED
- No significant merges in the window omitted from JOURNAL

**V2 (living-doc factual claims):**
- doc-counts.md '31 registered checks' — ALL_CHECKS has exactly 31 members (lines 2393–2426)
- doc-counts.md '15 pre-commit gates' — .pre-commit-config.yaml has exactly 15 hook ids
- VISION.md: audit.py has health/repo/run/registry commands — all four @cli.command decorators confirmed
- ARCHITECTURE.md Codemap: both scripts/codemap/__init__.py and scripts/toc/__init__.py exist
- CLAUDE.md §9 SessionStart roster (5 hooks) matches .claude/settings.json exactly
- CONTRIBUTING.md: config/requirements-dev.txt exists at the cited path
- CONTRIBUTING.md: ADR-27 and ADR-41 both exist under docs/decisions/
- CONTRIBUTING.md Handoff Process: 'v5 (stamp v5.7)' matches protocols/HANDOFF_PROCESS.md header
- CLAUDE.md §9 pre-commit hook roster matches .pre-commit-config.yaml — all 15 ids present in both
- ARCHITECTURE.md: check_mermaid_theme_directive correctly stated as retired (commented out of ALL_CHECKS)
- ARCHITECTURE.md: 14 named ALL_CHECKS members verified present in ALL_CHECKS registry

**V3 (BACKLOG-closure semantic coherence, since 2026-07-02):**
- #321 (ARCHITECTURE re-read: +4 organ rows, last_reviewed re-stamped) — Done-when MET
- #395 (logs/ naming convention: COHERENCE-NUDGE.log + PARITY-EVENTS.jsonl) — Done-when MET
- #302 (block-ff-push parity at n=2 consumers) — Done-when MET
- #309 (commit-msg-gate parity, hub-only-by-construction documented) — Done-when OR MET
- #131 (repo-onboarding runbook, 6 layers, piloted n=2) — Done-when MET
- #314 (protocols/ genre mandated, both consumers carry it) — Done-when MET
- #292 (validate_residual_completeness.py shipped, FAIL-class; narrower scope tracked in #365/#366) — Done-when MET
- #355 (fleet_parity commit-context regression test) — Done-when MET
- #372 (_select_active_bundle: 4 test classes + scrubbed-env assertion) — Done-when MET
- #337 (fleet_parity promoted to blocking ALL_CHECKS, tests, live-zero fleet run) — Done-when MET
- #316 (ADR-103 ownership axis on all 73 parity-surfaces.yaml rows) — Done-when MET
- #384 (L5a frames reviewed, rot findings filed as #393/#394) — Done-when MET

---

## Next Actions (proposals for operator)

1. **S1 (med, new)** — Update ARCHITECTURE.md at lines 314, 397, and 408: change "12 rules" to "13 rules" to reflect governance-backlog-story-id (added by #286). Simple text substitution; no structural change.

2. **S2 (low, new)** — Update ESSENTIALS.md:138 to mark the corrections.jsonl auto-promotion as aspirational/deferred rather than current operational fact. ADR-35 already documents the deferral; the ESSENTIALS text needs to align.

---

## Safety Tripwire

`git status --porcelain` output (captured before writing this digest):

```

```

*(Empty — clean working tree before digest was written. Expected output after writing this file: one untracked file only.)*

Post-write `git status --porcelain`:

```
?? docs/audits/2026-07-23-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. **Tripwire status: CLEAN.**
