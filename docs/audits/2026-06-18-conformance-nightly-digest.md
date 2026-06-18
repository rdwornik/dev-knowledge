<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-18

**Date:** 2026-06-18
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-18, confirmed unavailable. Consistent with all prior nightly runs.)

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
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 stale skills directory claim, persisting 4 nights)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | `.claude/skills/` confirmed present with `check-against-spec/` + `verify/`; persisting from 2026-06-11 (**5th consecutive nightly**) |
| **NEW** | S2 (med): CLAUDE.md §8 ".claude/ holds `commands/` and `rules/` only" | Same §8 sentence, now flagged as distinct sub-claim: `.claude/` has 5 subdirs (agents/, commands/, rules/, skills/, workflows/) — not 2 |
| **NEW** | S3 (med): VISION.md `last_reviewed: 2026-06-04` but last edited 2026-06-12 | 14-day freshness drift; audit.py check #10 would flag this |

**Delta counts:** 0 resolved · 1 persisting · 2 new
**Skeptic kill-rate:** 40% (2 of 5 raw findings killed)

---

## Summary

Mixed health. V1 (JOURNAL vs git) and V3 (backlog-closure coherence) are fully clean: all 10 most recent JOURNAL entries corroborate against git, and all 9 closures since 2026-05-28 were semantically coherent. V2 (living-doc claims) surfaces 3 survivors.

The S1 CLAUDE.md §8 skills-directory claim persists for a **5th consecutive nightly** — it is a simple one-line documentation update that has not yet been merged from prior PR proposals. S2 is a related but distinct sub-claim in the same sentence: `.claude/` is described as holding only `commands/` and `rules/`, when it actually has five subdirectories (agents/, commands/, rules/, skills/, workflows/). S3 is a new finding: VISION.md carries `last_reviewed: 2026-06-04` in its frontmatter, but git shows the file was last edited on 2026-06-12 — a 14-day drift that audit.py check #10 gates on. This is a freshness-cadence violation.

The skeptic kill-rate of 40% (2/5) is lower than recent baseline runs (75% on 2026-06-14), reflecting that V2 surfaced two genuine new findings (S2, S3) alongside the persisting S1 rather than mostly false positives.

---

## Findings (PROPOSALS ONLY)

**Raw:** 5 · **Survived skeptic:** 3 · **Killed false positives:** 2

<!-- counts: raw=5 survived=3 killed=2 -->

### High (1)

**S1** — CLAUDE.md §8 stale "no repo-level skills directory" claim *(PERSISTING from 2026-06-11; 5th consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/` directory with its two skills: `check-against-spec/` and `verify/`. Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Git history confirms skills directory was added in commits 05c9eb1 and 89f7140. Factually outdated for at least 5 nights. Simple doc update.

### Med (2)

**S2** — CLAUDE.md §8 stale .claude/ directory inventory *(NEW)*
- **Claim:** CLAUDE.md §8 states ".claude/ holds `commands/` and `rules/` only" (implying 2 subdirectories)
- **Location:** CLAUDE.md:122
- **Evidence:** `find /home/user/dev-knowledge/.claude -maxdepth 1 -type d | sort`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 to list all 5 actual subdirectories: `agents/`, `commands/`, `rules/`, `skills/`, `workflows/`. The S1 fix (removing the stale sentence) would partially resolve this; the remainder needs inventory correction.
- **Skeptic note:** `.claude/` demonstrably contains 5 subdirectories; the claim of "only commands/ and rules/" is directly contradicted. Note: S1 and S2 are in the same sentence (CLAUDE.md:122); a single targeted edit would resolve both.

**S3** — VISION.md `last_reviewed` freshness drift *(NEW)*
- **Claim:** VISION.md `last_reviewed: 2026-06-04` is current
- **Location:** VISION.md:4
- **Evidence:** `git log --format='%ai' -1 /home/user/dev-knowledge/VISION.md`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end, confirm or correct its content, and bump `last_reviewed` to the actual review date (at minimum to 2026-06-12, the last edit date).
- **Skeptic note:** Git confirms file last edited 2026-06-12 13:09:24 +0200; frontmatter stamp says 2026-06-04 — 8 days of unreviewed drift (14 days from today). Per CLAUDE.md §4 freshness cadence, `last_reviewed` must be re-stamped after edits are confirmed. audit.py check #10 gates on this.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — ARCHITECTURE.md `last_reviewed: 2026-06-17` potentially stale
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Git log confirms the last commit touching ARCHITECTURE.md was 2026-06-17 22:01:25, which matches the `last_reviewed: 2026-06-17` frontmatter stamp. The working-tree modification time (2026-06-18 01:04:33 UTC) is later, but this is attributable to session-startup hooks touching the file without committing. Git state is the authoritative source for conformance; it agrees with the stamp. Not a real finding.

**K2** — CLAUDE.md §12 v2.15 history note says "now 8 hooks" when .pre-commit-config.yaml has 9
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The v2.15 section-history line (dated 2026-06-06) is a historical annotation describing what was true when that version was written. The coherence-nudge hook was added after v2.15. Historical annotations in §12 are not current factual claims; they are an immutable record of past state. Not a conformance violation.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; full history available to 2026-03-30):**
- 2026-06-18: #167 serialize-group multi-surface close via /review-closures — JOURNAL matches bf0471a + cf265f6 + 5322449
- 2026-06-18: #172 coherence-spine v1 closure, #179-#183 roadmap extraction — JOURNAL matches BACKLOG changes
- 2026-06-17: architect-mode v5.2 handoff (-architect-2) + supplement FILLED — matches d209837 + downstream
- 2026-06-17: coherence spine v1 integration (adf0cbe..4719dbc, 4 commits) — JOURNAL matches
- 2026-06-17: check-against-spec skill implementation (5da375f) — JOURNAL matches
- 2026-06-17: architect-mode v5.2 handoff (-architect) — matches eee0717 bundle commit
- 2026-06-16: ADR-85 Stop-hook loop fix — matches 6cd4a55 and 0752efa
- 2026-06-15: PLAYBOOK pointerization Move 1 (0b89b1d merge, closes [#152] [#158]) — JOURNAL matches
- 2026-06-15: Move-1 merged to main, session handoff hybrid bundle (fa2ad82) — JOURNAL matches
- 2026-06-15: Faza A conformance gap closure (A2 n/a, A1 pytest_collected bump) — JOURNAL matches
- No undocumented significant merges found in git since 2026-06-15

**V2 (living-doc factual claims):**
- CLAUDE.md §11 "last 5" ADRs (ADR-76 through ADR-80) — all 5 exist in docs/decisions/
- ARCHITECTURE.md "20 registered checks" in ALL_CHECKS — verified against scripts/audit.py
- ARCHITECTURE.md pre-commit gates count (9) — matches .pre-commit-config.yaml (9 hooks)
- CLAUDE.md §9 pre-commit hook list (9 hooks listed) — all 9 verified in .pre-commit-config.yaml
- CLAUDE.md §7 commands — `save.md`, `handoff.md`, `changelog-review.md` exist in .claude/commands/
- ARCHITECTURE.md `last_reviewed: 2026-06-17` — matches last git commit on that file (2026-06-17)
- CLAUDE.md `last_reviewed: 2026-06-17` — current per git log
- CONTRIBUTING.md `last_reviewed: 2026-06-17` — current per git log
- ADR-76 through ADR-80 exist in docs/decisions/ directory

**V3 (backlog-closure semantic coherence, since 2026-05-28):**
- #167 multi-surface serialize-group (bf0471a, merged 5322449) — Done-when met: _parse_serialize_groups + tests delivered
- #172 coherence-spine v1 (commits 4719dbc/05c9eb1/5da375f) — Done-when met: integration arc C complete
- #152 PLAYBOOK §8 pointerization (76bf001) — token-log cadence moved to HANDOFF_PROCESS §14
- #158 PLAYBOOK Repo conventions + Appendices (3981c5a) — sections pointerized per operator-approved split
- #150 two-mode handoff (d67993d) — mode-switch + architect orientation layer landed
- #142 Stop-hook same-day blind-spot (b7fb74f) — advisory-only floor fix implemented
- #88 graphify pilot (5f327b2) — evaluation completed, REJECTED ruling documented
- #78 docs-refresh (d5753a80) — HANDOFF_PROCESS stamp updated, audit check count de-hardcoded
- #79 codemap grounding (052e311) — resolved end-state, no build needed

---

## Next Actions (proposals for operator)

1. **S1 + S2 (combined fix — high+med, S1 persisting 5 nights)** — Update CLAUDE.md §8 "Repo-level" bullet (line 122): remove the sentence "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" and replace with accurate inventory documenting `.claude/skills/check-against-spec/` and `.claude/skills/verify/`, and noting that `.claude/` also contains `agents/` and `workflows/`. A single sentence edit resolves both S1 and S2.

2. **S3 (med, new)** — Perform a genuine end-to-end re-read of VISION.md, confirm its content is current, and bump `last_reviewed` to today's date in the frontmatter. The file was last edited 2026-06-12; the stamp is 2026-06-04. Per §4 freshness cadence, the stamp must reflect an actual end-to-end review, not merely touching the file.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-18-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
