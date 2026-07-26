<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-26

**Date:** 2026-07-26
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed 2026-07-26, confirmed unavailable. Consistent with all prior nightly runs since 2026-06-04.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path).

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Gap:** 42 days (no nightly digests filed between 2026-06-14 and 2026-07-26)
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 stale skills claim, persisting 4 nights as of 2026-06-14)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high, persisting): CLAUDE.md §8 "no repo-level skills directory exists yet" | V2 confirms `.claude/skills/` now contains `verify/` and `check-against-spec/` — claim corrected at some point in the 42-day gap |
| **NEW** | N1 (med): JOURNAL.md missing merge-SHA anchor for 2a3d57b | ai-council handoff bundle merge has no JOURNAL anchor entry; the JOURNAL entry itself planned this step |
| **NEW** | N2 (med): ARCHITECTURE.md:41 win-tooling in machine-registered list incorrectly | No `ecosystem/win-tooling/` directory; registry.md confirms unonboarded |
| **NEW** | N3 (low): ARCHITECTURE.md:122 win-tooling duplicate in Layer 3 table | Same root cause as N2; second occurrence in the layer-boundary table |

**Delta counts:** 1 resolved · 0 persisting · 3 new
**Skeptic kill-rate:** 25% (1 of 4 raw findings killed)

---

## Summary

Strong overall health on returning after a 42-day gap. The one persisting finding from the 2026-06-14 baseline — the CLAUDE.md §8 stale skills claim — is definitively resolved: V2 confirms `.claude/skills/` now contains both `verify/` and `check-against-spec/` directories, consistent with the §8 prose that was updated during the gap. The V3 check is the standout result: 17 backlog closures since 2026-07-05 were all verified as semantically coherent against their Done-when criteria, including several complex multi-consumer Tier-1 gate closures and one legitimately borderline narrowing (#292, acknowledged transparently with open follow-on tickets).

Three new findings surfaced. Two are in ARCHITECTURE.md: `win-tooling` appears in the machine-registered repo list at two locations (line 41 and line 122) but fails the stated criterion — no `ecosystem/win-tooling/` directory exists and `registry.md` explicitly marks it as `unonboarded`. The third is a JOURNAL anchor gap: the ai-council handoff bundle merge (`2a3d57b`) has no dedicated merge-SHA anchor entry in JOURNAL.md, despite the JOURNAL entry itself recording this as a planned Next step.

The skeptic kill-rate of 25% (1/4) is within healthy range. The killed finding (the dev-knowledge handoff merge `1aa1fc41` lacking its own dedicated anchor) was correctly killed — the evidence command was structurally ambiguous, the SHA is traceable as a parent reference in the a2cebf47 anchor, and the session's ADR-85 gate obligation was satisfied by Entry 5.

---

## Findings (PROPOSALS ONLY)

**Raw:** 4 · **Survived skeptic:** 3 · **Killed false positives:** 1

<!-- counts: raw=4 survived=3 killed=1 -->

### High (0)

*(none)*

### Med (2)

**N1** — JOURNAL.md missing merge-SHA anchor for ai-council handoff merge 2a3d57b *(NEW)*
- **Claim:** The ai-council handoff bundle merge 2a3d57b is recorded with a JOURNAL merge-SHA anchor per ADR-85
- **Location:** JOURNAL.md:62-88 (Entry 4 addendum planned anchor; anchor never created)
- **Evidence:** `grep '2a3d57b' /home/user/dev-knowledge/JOURNAL.md` (returns no matches)
- **Verdict:** omitted
- **Proposed fix:** Create a dedicated merge-SHA anchor JOURNAL entry for 2a3d57b on a `docs/*-anchor` branch, following the Entry 1/Entry 2 pattern (Merge docs/handoff-2026-07-25-ai-council).
- **Skeptic note:** grep is definitive (zero output). Entry 4 addendum explicitly planned this step; every other comparable main merge in the window has an anchor. No ADR documents an exception.

**N2** — ARCHITECTURE.md:41 win-tooling incorrectly listed in machine-registered set *(NEW)*
- **Claim:** child repos include win-tooling as part of the machine-registered set (defined by `ecosystem/<repo>/state.yaml` presence)
- **Location:** ARCHITECTURE.md:41
- **Evidence:** `ls /home/user/dev-knowledge/ecosystem/` (no win-tooling/ subdirectory)
- **Verdict:** contradicted
- **Proposed fix:** Remove win-tooling from the machine-registered parenthetical at ARCHITECTURE.md line 41; retain only in the human registry reference.
- **Skeptic note:** ls is definitive. ARCHITECTURE.md's own criterion ("by `ecosystem/<repo>/state.yaml` presence") excludes win-tooling. `registry.md` confirms `registered · unonboarded`. No ADR documents win-tooling as machine-registered.

### Low (1)

**N3** — ARCHITECTURE.md:122 win-tooling duplicate in Layer 3 table *(NEW)*
- **Claim:** Layer 3 projects (machine registry) includes win-tooling
- **Location:** ARCHITECTURE.md:122
- **Evidence:** `ls /home/user/dev-knowledge/ecosystem/` (no win-tooling/ subdirectory)
- **Verdict:** contradicted
- **Proposed fix:** Remove win-tooling from the Layer 3 table cell at ARCHITECTURE.md:122 — same root cause as N2.
- **Skeptic note:** Same definitive evidence as N2; second occurrence must be corrected independently.

---

## Killed Findings

**K1** — JOURNAL.md missing dedicated anchor for dev-knowledge handoff merge 1aa1fc41
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The evidence command (`git log --format='%H %s' -- JOURNAL.md | grep '1aa1fc4'`) structurally returns the commit's own hash, not a subsequent anchor entry — cannot distinguish the two. The SHA is traceable as a parent reference in the a2cebf47 anchor (JOURNAL line 38). ADR-85's gate obligation for the session was satisfied by Entry 5's anchor of ada52980. The gap is a form-convention issue, not a substance or gate-compliance failure.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; all 2026-07-25):**
- Entry 1: cleanup merge ac798945 present; ecosystem/disposition-register.yaml modified correctly
- Entry 1: task count arithmetic (159 = 158 + 1 for #423) consistent
- Entry 2: merge a2cebf47 parents 1aa1fc41 + 357a15ef verified
- Entry 3: commits 71615bdd and 138f9bb5 present in git
- Entry 4: commit bc3eee77 (1071 insertions) and supplement commits 784d297 + f03b0c7 all present
- Entry 5: commit ada52980 (architect bundle) present in git
- Entry 6: merge c5f65165 and leaf d46d1f07 present
- Entry 7: merge 27f033df (Lane D) with closes-set {262, 295, 304, 339} confirmed; TOKEN-LOG merge d589844c and leaf bd543bdb present
- Entry 7: task-count arithmetic (158 - 1 + 5 - 4 = 158 before branch-only) consistent
- Entry 8: Lane D commits b4ac7d54, 89ae1d1d, 9fa8bdef, 19b5d598 and terra codex-review 2945f894 all present
- Entry 9: merge 7f248f95 (vision-reread, closes #368) present
- Entry 10: commit 30a8c42b (fix terra HIGH) present
- All doc/*-anchor branch merges in git correspond to JOURNAL anchor entries

**V2 (living-doc factual claims):**
- CLAUDE.md §8 skills: `.claude/skills/` confirmed contains `verify/` and `check-against-spec/` — prior persisting finding RESOLVED
- CLAUDE.md §9 pre-commit hooks: all 15 listed hooks match `.pre-commit-config.yaml` exactly
- CLAUDE.md §11 ADRs (generated): ADR-100 through ADR-104 confirmed; ADR-104 is highest-numbered
- CLAUDE.md §7 commands: `/changelog-review`, `/handoff`, `/override`, `/save` match `.claude/commands/`
- CLAUDE.md §8 plugin: `tier1-lifecycle@dev-knowledge-methodology` confirmed in settings.json `enabledPlugins`
- CLAUDE.md §9 session hooks: all 5 SessionStart hooks and Stop/PreToolUse hooks match settings.json
- Pre-commit gate count (15) in `ecosystem/doc-counts.md` matches `.pre-commit-config.yaml`
- CONTRIBUTING.md hook table: all 15 hooks and ruff rev v0.15.5 match config
- CONTRIBUTING.md script references: `check_backlog_commit_msg.py`, `check_backlog_filing.py`, `block_ff_push.py` all exist
- CONTRIBUTING.md: HANDOFF_PROCESS.md confirmed v5.7 stable
- VISION.md "nine git repos (ADR-104)": ADR-104 confirms fleet is 9 git repos
- ESSENTIALS.md path references: `protocols/HANDOFF_BOOT.md` and `protocols/SESSION_SETUP.md` both exist

**V3 (backlog-closure semantic coherence, 2026-07-05 to 2026-07-26 — 17 closures, all clean):**
- #355 — fleet_parity commit-context inversion fix; named regression test confirmed present
- #372 — check_handoff_probes add-date order fix; all 4 test classes confirmed
- #131 — docs/runbooks/repo-onboarding.md; 6-layer install sequence and pilot clause confirmed
- #302 — block-ff-push guard at v1.3.1 on both consumers; FIRING confirmed in both JOURNALs
- #309 — backlog-id-on-close portable (both consumers); backlog-filing-backpressure hub-only-by-construction confirmed
- #314 — protocols/README.md mandated-genre wording; both consumers carry git-tracked protocols/
- #292 — validate_residual_completeness.py present; Done-when met; narrowness acknowledged with open #366/#365
- #321 — ARCHITECTURE.md Ch2 gains all 4 owed organ rows; last_reviewed bumped correctly
- #395 — coherence_nudge.py→COHERENCE-NUDGE.log and fleet_parity.py→PARITY-EVENTS.jsonl renames; all 4 sites updated
- #384 — fleet_analytics frames reviewed; rot tickets #393 and #394 filed
- #398 — intake enum SEED→DRAFT→READY→{ACCEPTED|CONSUMED|SUPERSEDED|REJECTED} deployed; gen_intake_index --check clean
- #368 — 7 content defects found and fixed; last_reviewed bumped 2026-06-19→2026-07-25
- #381 — ADR-104 Proposed→Accepted; all 3 required pricing items discharged
- #262 — kill-candidate (hand-authored-by-policy for flat/single-package layouts) used; concrete defect carved to #416
- #295 — same kill-candidate ruling as #262; flat-layout settled by policy
- #304 — deploy commands fixed + per-command arg-form table added and verified
- #339 — Done-when second branch satisfied: ADR-29 ratification marker records threshold + current state (241 < 300)

---

## Next Actions (proposals for operator)

1. **N1 (med)** — Create merge-SHA anchor JOURNAL entry for merge `2a3d57b` (Merge docs/handoff-2026-07-25-ai-council). The JOURNAL addendum at Entry 4 already records this as planned. Follows the standard `docs/*-anchor` branch + merge-SHA anchor commit pattern.

2. **N2 + N3 (med + low, same root cause)** — Remove `win-tooling` from the machine-registered repo list at ARCHITECTURE.md lines 41 and 122. It is `registered · unonboarded` (human registry only) with no `ecosystem/win-tooling/` directory. Single edit, two locations.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-26-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
