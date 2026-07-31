<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-30

**Date:** 2026-07-30
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances nightly agentic-conformance arc
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-07-30, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

**Environment gap (recurring):** `session_end_backpressure.py` Stop hook failed to execute on every firing this session. Cloud provides `uv 0.8.17`; project pins `==0.11.19` (ADR-106 `pyproject.toml [tool.uv] required-version`). The session-end JOURNAL SHA-anchor gate could not run. This is a platform/toolchain mismatch, not a doc-conformance finding, but it is recorded here as a nightly platform re-probe observation. All `uv run --locked` pre-commit hooks would similarly fail if triggered in this environment.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high persisting — CLAUDE.md §8 stale repo-level skills claim)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | CLAUDE.md §8 now correctly documents `.claude/skills/verify` + `check-against-spec`. Persisted 4 consecutive nights (2026-06-11 through 2026-06-14); fixed between runs. |
| **NEW** | N1 (high): ARCHITECTURE.md labels `silent_rule_ratchet` RULED-UNBUILT but it is built and registered | #436 closed 2026-07-28; two post-closure ARCHITECTURE.md edits did not clear the stale header note |
| **NEW** | N2 (high): CONTRIBUTING.md "Nightly outcome management" describes retired GitHub Action as live | `.github/` deleted 2026-07-08; ARCHITECTURE.md Ch6 knows but defers the fix |
| **NEW** | N3 (med): ESSENTIALS.md claims `corrections.jsonl` auto-logging but file and implementation don't exist | ESSENTIALS.md last_reviewed today; the claim survived the re-review uncorrected |
| **NEW** | N4 (med): `terminal-setup` declared in VISION.md/ADR-104 but absent from `ecosystem/registry.md` | win-tooling IS registered; terminal-setup is the sole missing child |
| **NEW** | N5 (low): JOURNAL entry 2026-07-30(c) Changes list omits commit 26d4858 | Commit added 24 min after wrap, before branch merge; Changes line has no coverage of `ecosystem/disposition-register.yaml` |

**Delta counts:** 1 resolved · 0 persisting · 5 new
**Skeptic kill-rate:** 17% (1 of 6 raw findings killed)

---

## Summary

Documentation health is mixed: the prior persisting high finding (CLAUDE.md §8 skills claim) is cleanly resolved, but this run surfaces 5 new findings — 2 high, 2 med, 1 low — indicating meaningful drift across the living-doc layer over the 46-day gap since the last nightly run.

The two high findings share a root cause pattern: a living doc's description of a system state was correct when written but was not updated when the underlying system changed. `ARCHITECTURE.md`'s header note calling `silent_rule_ratchet` RULED-UNBUILT was accurate before [#436] merged on 2026-07-27, but two subsequent ARCHITECTURE.md edits (2026-07-28) did not clear it. `CONTRIBUTING.md`'s "Nightly outcome management" section was accurate when the GitHub Action existed but was never updated after the `.github/` deletion (2026-07-08); ARCHITECTURE.md Ch6 explicitly acknowledges this stale reference at line 758 but defers the fix — meaning the stale guidance has been known and unaddressed for 22 days.

The medium finding on `corrections.jsonl` is particularly notable because ESSENTIALS.md carries `last_reviewed: 2026-07-30` — the claim was reviewed today and still not corrected. The corrections.jsonl automation (correction logging → auto-promotion to permanent rule via Stop hook) appears to be an aspirational concept from a self-evolution article cherry-picked in 2026-03 (LESSONS.md:516) that was documented across multiple files (ESSENTIALS.md, PLAYBOOK.md, ENVIRONMENT.md) but never implemented.

The skeptic kill-rate of 17% (1/6) is lower than the prior run's 75%, reflecting that the findings this cycle are better-evidenced and less ambiguous than previous false positives.

---

## Findings (PROPOSALS ONLY)

**Raw:** 6 · **Survived skeptic:** 5 · **Killed false positives:** 1

<!-- counts: raw=6 survived=5 killed=1 -->

### High (2)

**N1** — ARCHITECTURE.md organ map: `silent_rule_ratchet` labeled RULED-UNBUILT but fully implemented

- **Claim:** ARCHITECTURE.md lines 26-27 read "Deliberately NOT added: `silent_rule_ratchet` ([#436], ruled-unbuilt) — this chapter's own Status legend keeps a RULED-UNBUILT organ *out* of the table until it is built."
- **Location:** `ARCHITECTURE.md:26-27`
- **Evidence:** `grep -n 'silent_rule_ratchet' /home/user/dev-knowledge/scripts/audit.py` → returns lines 2720, 2804 (implementation), 2988 (ALL_CHECKS registration with comment `# [#436] D4 ratchet — gates GROWTH of the silent-rule pool`)
- **Verdict:** contradicted
- **Context:** The ARCHITECTURE.md note was correct at the time of commit `c0ae98b` (2026-07-27 18:01 UTC+2, before #436 implementation merged at 22:56). Two subsequent ARCHITECTURE.md edits (`5c8a9d6` at 2026-07-28 13:57, `251c42f` at 2026-07-28 14:34) touched ARCHITECTURE.md without clearing the stale exclusion note. No ADR documents intentional staleness.
- **Proposed fix:** Remove the "Deliberately NOT added: `silent_rule_ratchet` ([#436], ruled-unbuilt)" sentence from ARCHITECTURE.md lines 26-27 and add `check_silent_rule_ratchet` to the Ch2 organ table with status ACTIVE in the next ARCHITECTURE.md currency-lane pass.

**N2** — CONTRIBUTING.md "Nightly outcome management": retired GitHub Action described as live

- **Claim:** CONTRIBUTING.md lines 132-159 describes `.github/workflows/nightly-conformance-triage.yml` as "the repo's first GitHub Action" that "handles the morning," framing three conditional behaviors (clean night / findings night / anomalous PR) as currently executing.
- **Location:** `CONTRIBUTING.md:134-136`
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null || echo 'DOES NOT EXIST'` → DOES NOT EXIST
- **Verdict:** contradicted
- **Context:** The Action was deleted at commit `82227f08` (2026-07-08, merged to main at `57ae83a6` under [#255]) because a PR-triggered organ under a local-merge workflow was vacuous. ARCHITECTURE.md Ch6 explicitly states "Do not follow CONTRIBUTING 'Nightly outcome management' as live guidance" at line 758 and acknowledges the stale reference, but defers the fix as out of scope. The deferral is a scope decision, not an ADR-backed architectural decision.
- **Proposed fix:** Rewrite CONTRIBUTING.md "Nightly outcome management" section to describe the Action as RETIRED (referencing commit `82227f08`, 2026-07-08) and point readers to ARCHITECTURE.md Ch6 for the current state of the broken triage edge ([#428]).

### Med (2)

**N3** — ESSENTIALS.md: `corrections.jsonl` auto-logging described as active but not implemented

- **Claim:** `protocols/ESSENTIALS.md:139` reads "**Automated:** every correction logged to `corrections.jsonl` → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook)."
- **Location:** `protocols/ESSENTIALS.md:139`
- **Evidence:** `ls /home/user/dev-knowledge/corrections.jsonl 2>/dev/null || echo 'DOES NOT EXIST'` → DOES NOT EXIST; `grep -rn 'corrections.jsonl' /home/user/dev-knowledge/scripts/` → no matches
- **Verdict:** unsupported
- **Context:** The concept originates from a 2026-03-29 self-evolution article (LESSONS.md:516, "Cherry-picked 5 actionable items: verify lines, corrections log, core-invariants, /boot, session scorecard"). It is also referenced in PLAYBOOK.md:3258 and ENVIRONMENT.md:74, but no implementation exists. The Stop hook (`session_end_backpressure.py`) has no corrections.jsonl logic. ESSENTIALS.md carries `last_reviewed: 2026-07-30`; the claim survived today's re-review uncorrected.
- **Proposed fix:** Update ESSENTIALS.md:139 to either (a) strike the automation claim and mark it as aspirational with a backlog reference, or (b) qualify with "PLANNED — not yet implemented." Update PLAYBOOK.md:3258 and ENVIRONMENT.md:74 consistently.

**N4** — `ecosystem/registry.md` missing `terminal-setup` row

- **Claim:** VISION.md:108 declares "eight child git repos (ADR-104): the hub `.dev-knowledge` plus eight child repos: ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, demo-prep, life-architect, terminal-setup, win-tooling." The registry header states "Add a row when a repo is created."
- **Location:** `VISION.md:108-111` / `ecosystem/registry.md`
- **Evidence:** `grep 'terminal.setup' /home/user/dev-knowledge/ecosystem/registry.md 2>/dev/null || echo 'NOT FOUND'` → NOT FOUND (win-tooling IS present — terminal-setup is the single missing child)
- **Verdict:** omitted
- **Context:** ADR-104 explicitly names terminal-setup in the fleet declaration. VISION.md:111 lists it. ecosystem/registry.md has 7 children (hub + 6) but not terminal-setup. The registry is described as "human-maintained" and "Add a row when a repo is created."
- **Proposed fix:** Add a `terminal-setup` row to `ecosystem/registry.md` following the existing format (Repo | Path | Purpose | Status), consistent with ADR-104's fleet declaration and the registry's own maintenance instruction.

### Low (1)

**N5** — JOURNAL 2026-07-30(c) Changes list omits commit 26d4858

- **Claim:** The 2026-07-30(c) JOURNAL entry Changes line lists six areas but does not record commit 26d4858 (`docs(ecosystem): disposition the intake-21 orientation -> handoff-process edge`, +17 lines to `ecosystem/disposition-register.yaml`).
- **Location:** `JOURNAL.md`, entry `2026-07-30 (c)` Changes line
- **Evidence:** `git log --format='%H %ai %s' 6ecfb2b..470b24f` → shows commit 26d4858 at 2026-07-29 21:11:27, between the journal wrap 3b722f0 (20:47:28) and the merge 470b24f (21:12:27)
- **Verdict:** omitted
- **Proposed fix:** No retroactive edit (JOURNAL is append-only). No action required; acknowledged here as a timing artifact.

---

## Killed Findings

**K1** — Commit d993922 false-positive in backlog closure grep
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** V3's own note concedes "Not a real closure; flagged for analytical completeness only." `git show d993922` confirms the commit body files [#437] (the CLOSES_RE quoting defect) and uses the text `closes [#N]` as illustrative prose explaining the defect — not an actual closure instruction. No ticket row was removed from BACKLOG.md. This is meta-evidence of the [#437] quoting-defect issue, now closed by aa16bf6.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; 2026-07-28(k) through 2026-07-30(c)):**
- All explicitly cited SHA anchors for hub commits verified present in git history with matching subjects
- Cross-repo SHAs (65a8a35 corp-monorepo, e4f002e ai-council, be46b30/c954876 Extended-section merges) correctly attributed to external repos — out of scope for hub verification
- Night-batch merge (14bcb1c) correctly used as baseline reference in entry (a) 2026-07-29
- No significant merged work found in hub git log outside the coverage of the 10 entries

**V2 (living-doc factual claims):**
- `scripts/audit.py` ALL_CHECKS: 34 registered checks confirmed (grep count of `check_` entries in ALL_CHECKS list at line 2954)
- Pre-commit gates (15): all 15 hook IDs in `.pre-commit-config.yaml` match CLAUDE.md §9 and CONTRIBUTING.md hook table exactly
- `.claude/commands/`: changelog-review.md, handoff.md, override.md, save.md — all present
- `.claude/skills/`: `verify` + `check-against-spec` confirmed — prior S1 finding **RESOLVED**
- CLAUDE.md §9 SessionStart hooks (5): fleet_health.py, surface_triage.ps1, billing_leak_sentinel.ps1, changelog_sentinel.py, arm_hooks.py — confirmed in `.claude/settings.json`
- ADR-103 through ADR-107 all exist in `docs/decisions/`; `.claude/generated/recent-adrs.md` enumerates them correctly
- All key script files exist: `block_ff_push.py`, `check_backlog_commit_msg.py`, `check_backlog_filing.py`, `session_end_backpressure.py`, `gen_claude_rosters.py`, `gen_methodology_roster.py`, `gen_audit_index.py`, `gen_intake_index.py`
- ARCHITECTURE.md defers count claims to `ecosystem/doc-counts.md` (34 checks, 15 gates, 1963 tests) — indirection working as designed
- `tasks/` directory and `tasks/manifest.json` exist, confirming ADR-107 source-zone flip

**V3 (backlog-closure semantic coherence, since 2026-07-09):**
- 18 distinct closures verified coherent across 11 commits: #435, #437, #439, #444, #386, #434, #436, #398, #321, #395, #384, #302, #309, #131, #314, #292, #355, #372
- In every case, closing diff matches stated Done-when conjuncts; scope gaps explicitly recorded as filed follow-on tickets

---

## Next Actions (proposals for operator)

1. **N1 (high)** — Clear the stale RULED-UNBUILT note from `ARCHITECTURE.md:26-27` and add `check_silent_rule_ratchet` to the Ch2 organ table. Simple currency-lane edit; the implementation is complete and verified.

2. **N2 (high)** — Rewrite `CONTRIBUTING.md` "Nightly outcome management" section to describe the Action as RETIRED. The stale live-guidance has been acknowledged in ARCHITECTURE.md for 22 days without being fixed. Two-paragraph rewrite; no architectural decision needed.

3. **N3 (med)** — Update `ESSENTIALS.md:139` (and PLAYBOOK.md:3258, ENVIRONMENT.md:74) to mark `corrections.jsonl` automation as aspirational/unimplemented. Reviewed-but-uncorrected today (`last_reviewed: 2026-07-30`) — needs an explicit operator call on whether to build it or retire the claim.

4. **N4 (med)** — Add `terminal-setup` row to `ecosystem/registry.md`. One-row table addition; ADR-104 and VISION.md already declare it.

5. **N5 (low)** — No action required. JOURNAL is append-only; the 26d4858 omission is a timing artifact acknowledged here.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-30-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked file changed. If any other tracked file appears above, that is a safety breach requiring operator investigation before merge.
