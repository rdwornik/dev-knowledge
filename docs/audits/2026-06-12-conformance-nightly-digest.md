<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-12

**Date:** 2026-06-12
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-12, confirmed unavailable. Consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-06-11-conformance-nightly-digest.md`
**Prior surviving findings:** 3 med (N2, N3, N5)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | N5 (med): CONTRIBUTING.md "13 self-conformance checks" hardcoded count | De-hardcoded in the 2026-06-12 v5-canonical-flip session — lines 105+109 now say "the self-conformance checks" with no number |
| **PERSISTING** | N2→F2 (med): ARCHITECTURE.md inline `Last updated: 2026-06-07` ≠ frontmatter | Frontmatter `last_reviewed` advanced from `2026-06-10` to `2026-06-12` today (restamped in the flip session) but inline prose date was not updated; still contradicted |
| **PERSISTING** (severity upgraded) | N3→F3 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | Severity raised med→high: `.claude/skills/verify/` predated the 2026-06-11 re-review of CLAUDE.md; the claim was not corrected then and again not during today's flip session despite CLAUDE.md being touched |
| **NEW** | F4 (med): merge 0ee6c3d claims `closes [#147]` but BACKLOG not updated in that commit | ADR-65 tag-placement: item removed in separate chore commit e56375f |
| **NEW** | F5 (med): merge 5193de5 claims `closes [#11]` but BACKLOG not updated in that commit | ADR-65 tag-placement: item removed in separate chore commit 88ab795 |
| **NEW** (historical + self-corrected) | F7 (high): c4c6831 closed #79 via inline RESOLVED notation, not removal | ADR-65 violation; item subsequently removed by 024282c (today) — current BACKLOG state is correct but the historical commit violated done-items-leave |

**Delta counts:** 1 resolved · 2 persisting · 3 new  
**Skeptic kill-rate:** 29% (2 of 7 raw findings killed)

---

## Summary

The .dev-knowledge repository closed one long-standing drift today (N5: CONTRIBUTING.md hardcoded check count de-hardcoded as part of the v5-canonical-flip session), but two persistent medium-severity documentation mismatches remain and three new findings surfaced. The ARCHITECTURE.md timestamp inconsistency (N2/F2) is uniquely stubborn: today's flip session restamped the frontmatter to `2026-06-12` without updating the inline prose `Last updated:` marker, meaning the mismatch now spans 5 days (2026-06-07 vs 2026-06-12) rather than 5 days (2026-06-07 vs 2026-06-10). CLAUDE.md §8 (N3/F3) was touched twice in the last two sessions without correcting the stale "no repo-level skills directory" claim; severity is upgraded to high. Three new V3 findings address ADR-65 done-items-leave compliance: two are tag-placement violations where merge commits claim `closes [#N]` while BACKLOG removal happens in a subsequent chore commit (F4 #147, F5 #11), and one (F7 #79) is a historical inline-RESOLVED violation in c4c6831 that was self-corrected by today's 024282c cleanup commit — F7 is actionable only as a process note. The skeptic killed 2 of 7 raw findings: F1 (JOURNAL omission of 024282c) killed as true-but-irrelevant (024282c DID update JOURNAL.md, adding 14 lines); F6 (fcc3363 closes #154) killed as evidence-not-definitive (BACKLOG.md WAS modified in fcc3363, removing #154). V1 found the JOURNAL clean for all 10 verifiable entries; V2 verified 8+ living-doc factual claims as correct.

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 5 · **Killed false positives:** 2

<!-- counts: raw=7 survived=5 killed=2 -->

### High (2)

**F3** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from N3; severity upgraded med→high)*
- **Claim:** CLAUDE.md §8 line 122 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory (shipped by #104). Remove the "No repo-level skills directory exists yet" claim. Severity upgraded because the directory predated the 2026-06-11 re-review of CLAUDE.md and was not corrected.

**F7** — BACKLOG #79 closed via inline RESOLVED notation instead of removal *(NEW; historical + self-corrected)*
- **Claim:** Commits c4c6831 and 052e311 claim to close [#79] but the item was modified in BACKLOG.md with strikethrough and "RESOLVED 2026-06-03" inline notation rather than being removed, violating ADR-65 done-items-leave
- **Location:** c4c6831, 052e311
- **Evidence:** `git diff c4c6831^1 c4c6831 -- BACKLOG.md | grep '\[#79\]'`
- **Verdict:** contradicted
- **Note:** Item was subsequently properly removed by 024282c (today). Current BACKLOG state is correct; the historical commit violated ADR-65. Prior 2026-06-11 V3 listed #79 as "coherent" — that was a V3 miss (it checked semantic content, not removal pattern). Process note only; no current remediation needed.
- **Proposed fix:** No action required on BACKLOG (already correct). Process note: use removal, not inline RESOLVED notation, when closing items (ADR-65 §Decision 1).

### Med (3)

**F2** — ARCHITECTURE.md inline/frontmatter timestamp mismatch *(PERSISTING from N2)*
- **Claim:** ARCHITECTURE.md has frontmatter `last_reviewed: 2026-06-12` but inline text reads `Last updated: 2026-06-07`
- **Location:** ARCHITECTURE.md:2 and ARCHITECTURE.md:16
- **Evidence:** `head -20 /home/user/dev-knowledge/ARCHITECTURE.md`
- **Verdict:** contradicted
- **Proposed fix:** Update the inline `> Last updated: \`2026-06-07\`` line in ARCHITECTURE.md to `2026-06-12` to match the frontmatter `last_reviewed` stamp. (Frontmatter was bumped during today's v5-canonical-flip session but the inline marker was not co-updated.)

**F4** — merge commit 0ee6c3d claims `closes [#147]` but BACKLOG not updated in that commit *(NEW)*
- **Claim:** Merge commit 0ee6c3d message says "closes [#147]" but BACKLOG.md still contained the [#147] item at that commit's tree; actual removal occurred in separate chore commit e56375f
- **Location:** 0ee6c3d
- **Evidence:** `git log -1 --format=%B 0ee6c3d | head -1 && git show 0ee6c3d:BACKLOG.md | grep -c '^- \[#147\]'`
- **Verdict:** omitted
- **Proposed fix:** In future closures, place the `closes [#N]` tag in the commit that actually removes the item from BACKLOG.md (the chore commit), not the feature-shipping merge. The merge can reference the item without a `closes` tag.

**F5** — merge commit 5193de5 claims `closes [#11]` but BACKLOG not updated in that commit *(NEW)*
- **Claim:** Merge commit 5193de5 message says "closes [#11]" but BACKLOG.md still contained the [#11] item at that commit's tree; actual removal occurred in separate chore commit 88ab795
- **Location:** 5193de5
- **Evidence:** `git log -1 --format=%B 5193de5 | head -1 && git show 5193de5:BACKLOG.md | grep -c '^- \[#11\]'`
- **Verdict:** omitted
- **Proposed fix:** Same pattern as F4 — place `closes [#N]` in the commit that removes the item from BACKLOG.md.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — F1: JOURNAL omits commit 024282c
- **Claim:** 2026-06-12 JOURNAL entry omits commit 024282c which closes 6 major BACKLOG items
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Commit 024282c message includes "JOURNAL" because it DID modify JOURNAL.md (14 lines added). The 2026-06-12 entry at lines 22-32 is present and comprehensive, covering the #149 flip closures. The missing SHA is a style matter, not a conformance gap.

**K2** — F6: fcc3363 closes #154 without removing from BACKLOG
- **Claim:** merge commit fcc3363 says "closes [#154]" but BACKLOG not modified in that commit
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** V3's claim was contradicted by the actual diff: `git show fcc3363 --stat` shows `BACKLOG.md | 7 +-`, confirming the file WAS modified. Verification shows #154 was removed in that commit (present in fcc3363^1, absent in fcc3363). Finding was factually wrong.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-12 entry: #149 flip (22cbd06 merge, c3ba6d4, fb9fece) — all verified in git log
- 2026-06-11 handoff-arc cleanup (36f210f merge) — verified
- 2026-06-11 foundation stabilization (fcc3363 merge, 4307539, c0fae5e, 884699a, 5cc5a24) — verified
- 2026-06-11 architecture-coherence audit (c3c2513 merge) — verified
- 2026-06-11 v5 beta parallel-ship (c32bcad merge) — verified
- 2026-06-11 two-mode handoff, surface-responsibility audit, v5 dogfood — all verified
- All cited SHAs within shallow-history window confirmed present

**V2 (living-doc factual claims):**
- ARCHITECTURE.md "18 registered checks" in ALL_CHECKS — correct (18 checks in audit.py)
- ARCHITECTURE.md pre-commit gates count (8) — matches .pre-commit-config.yaml
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in .pre-commit-config.yaml
- CLAUDE.md §11: ADR-76 through ADR-80 exist in docs/decisions/ — verified
- .claude/commands/ contains save.md, handoff.md, changelog-review.md — verified
- CLAUDE.md §7 plugin-provided /review-closures — verified
- CONTRIBUTING.md pre-commit hooks table — matches .pre-commit-config.yaml
- CONTRIBUTING.md "13 self-conformance checks" — RESOLVED (de-hardcoded; no hardcoded count remains)
- VISION.md tier system deprecated 2026-05-23 per ADR-38 — correct
- ESSENTIALS.md structural claims — correct

**V3 (backlog-closure semantic coherence):**
- fcc3363 closes #154 — coherent (item removed in that commit; K2)
- 024282c closes #149, #151, #160, #148, #124, #25 — semantically coherent (v5 flip delivered Done-when)
- 5cc5a24 closes #154 clause — coherent
- e56375f removes #147 — coherent (item properly removed post-merge)
- 88ab795 removes #11 — coherent (item properly removed post-merge)

---

## Next Actions (proposals for operator)

1. **F3 (high, persisting 3+ days)** — Update CLAUDE.md §8: remove "No repo-level skills directory exists yet" and document `.claude/skills/verify/` (shipped by #104). This was missed in the 2026-06-11 re-review and again in today's flip session. Simple one-line fix.
2. **F2 (med, persisting 3+ days)** — Update ARCHITECTURE.md inline marker: change `> Last updated: \`2026-06-07\`` to `2026-06-12`. The frontmatter was restamped today without co-updating the inline prose.
3. **F4 + F5 (med, process note)** — Future closures: place `closes [#N]` in the commit that removes the item from BACKLOG.md, not the feature-shipping merge. Historical commits 0ee6c3d/#147 and 5193de5/#11 are closed and cannot be amended; process note only for future work.
4. **F7 (high, process note, self-corrected)** — No BACKLOG action needed (#79 already removed by 024282c). Process note: use removal, not inline RESOLVED notation, for future closures (ADR-65 §Decision 1).

---

## Safety Tripwire

`git status --porcelain` output before writing this digest:

```
(empty — clean working tree on branch claude/conformance-2026-06-12)
```

`git status --porcelain` output after writing this digest:

```
?? docs/audits/2026-06-12-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
