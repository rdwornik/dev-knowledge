<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-22

**Date:** 2026-06-22
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed 2026-06-22, confirmed unavailable. Consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` (Explore subagent) | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Note:** 8-day gap since prior digest (no runs 2026-06-15 through 2026-06-21); this is the 5th nightly appearance of the skills finding, counted from 2026-06-11.
**Prior surviving findings:** 1 (S1 high — CLAUDE.md §8 skills claim, persisting since 2026-06-11)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | `.claude/skills/` confirmed present with TWO skills (verify/ and check-against-spec/); claim directly contradicted; persisting since 2026-06-11 (**5th nightly appearance**). CLAUDE.md was last_reviewed 2026-06-21 without fixing this. |

**Delta counts:** 0 resolved · 1 persisting · 0 new
**Skeptic kill-rate:** 50% (1 of 2 raw findings killed — V3's #197 finding killed as evidence-not-definitive: #197 WAS properly filed in BACKLOG before closure)

---

## Summary

Documentation conformance is strong overall: 33 merges on 2026-06-20/21 are fully traced, 10 pre-commit hooks verified against reality, ADR chain complete (ADR-85 through ADR-89), and closure traceability confirmed for all significant work items in the ~3-week window. One high-severity finding survived skeptic review — CLAUDE.md §8 falsely claims the `.claude/skills/` directory "does not exist yet" despite its creation on 2026-06-19 with two skills (verify/ and check-against-spec/). The skeptic kill-rate is 50% (1/2), with the one killed finding arising from a false premise in V3's #197 report (the item was correctly filed in BACKLOG before closure). The living-docs claim error persisted through a stated review cycle (last_reviewed: 2026-06-21), indicating a gap in review thoroughness; this is now its 5th nightly appearance across nightly runs since 2026-06-11.

---

## Findings (PROPOSALS ONLY)

**Raw:** 2 · **Survived skeptic:** 1 · **Killed false positives:** 1

<!-- counts: raw=2 survived=1 killed=1 -->

### High (1)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th nightly appearance; 8-day gap since last digest)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (`.claude/` holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:125 (§8 "Repo-level" bullet)
- **Evidence:** `ls -R .claude/skills/` — shows verify/ and check-against-spec/ directories with SKILL.md files; `git log --all --diff-filter=A -- '.claude/skills'` shows commit 442c994 (2026-06-19) created them
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 to remove "No repo-level skills directory exists yet" and document the existing `.claude/skills/` directory containing verify/ and check-against-spec/ skills (created 2026-06-19 by commit 442c994).
- **Skeptic note:** `.claude/skills/` definitively exists with two skills; claim was written in the same commit that created the directory; last_reviewed: 2026-06-21 postdates directory creation yet the false claim persists. Clear documentation drift.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — #197 closed without BACKLOG.md entry (V3 raw finding)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The finding's premise is factually false. Verification shows #197 WAS in BACKLOG.md before closure (commit c3efa21). Commits 325a049 and 1c4663d correctly remove it per ADR-65 (done items leave). V3 conflated "decision-only work item" with "never filed in BACKLOG" — #197 was properly filed and closed per the normal lifecycle.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-21: doc-currency reconciliation — all 6 commits (34b2405, 09a6f12, 3a83978, 0a04b94, 7bb26b7, 7286707) verified in git; #10 closure confirmed
- 2026-06-21: #194 Phase-0 fit-check — commit f619380 verified; ADR-89 OQ1 corrections confirmed
- 2026-06-21: ratify ADR-88/89 — merge 38cb663 verified; ADR amendments in git confirmed
- 2026-06-21: reconcile architect bundle — merge bb15448, commit 02451c5 verified; OQ1-decided status confirmed
- 2026-06-21: session state-hygiene wrap — commit 1984812 verified; transcript archive at 2d39dbb confirmed
- 2026-06-21: architect handoff bundle v5.2 — commit ad6d17e verified; probes 10/10 binding verified
- 2026-06-21: OPS audit — merge 19f953e verified; audit findings at bbbbfd2 confirmed
- 2026-06-21: TECHNICAL audit — merge 8955d23 verified; audit findings at a6149f0 confirmed
- 2026-06-21: PROCESS audit — merge e061a08 verified; audit findings at a92af42 confirmed
- 2026-06-20: refscan precision #199 — merge d752179 verified; immutable-zone filtering logic confirmed
- All 33 merges on 2026-06-20/21 documented in JOURNAL entries; newest-first ordering maintained

**V2 (living-doc factual claims):**
- CLAUDE.md §9: 10 pre-commit hooks listed — matches `.pre-commit-config.yaml` actual count of 10 hooks
- ARCHITECTURE.md: 22 registered checks in audit.py ALL_CHECKS — verified correct
- CLAUDE.md §11: Last 5 ADRs (ADR-85 through ADR-89) — all five files exist in docs/decisions/
- CONTRIBUTING.md validators table — matches `.pre-commit-config.yaml` (10 hooks)
- plugin tier1-lifecycle@dev-knowledge-methodology — correctly marked enabled in `.claude/settings.json`
- Repo-level commands (/save, /handoff, /changelog-review, /override) all exist in `.claude/commands/`
- VISION.md Layer 2 claim — verified in ARCHITECTURE.md

**V3 (backlog-closure semantic coherence, since 2026-05-14):**
- #10 (closes 8a5ae7f/7286707): TOKEN-LOG doc refs qualified across CLAUDE/ARCHITECTURE/PLAYBOOK — done-when met
- #47 (closes d95d6ce): Corp repos classified as absent from registry — done-when met
- #78 (closes d5753a8): ARCHITECTURE/CLAUDE end-to-end re-read + freshness re-stamp — done-when met
- #79 (closes 052e311): Codemap grounding audit completed — done-when met
- #88 (closes 5f327b2): Graphify pilot measurements + REJECT ruling — done-when met
- #140 (closes 10e762f+): doc_rot grooming-gate detector shipped read-only WARN — done-when met
- #179 (closes eddaaf0): Undeclared-edge scan for prose-only spec edges — done-when met
- #186/#187 (closes dd025c3): Floor-sync task-graph checks implemented with tests — done-when met
- #193 (closes 04d8363): Pyright reverse-dep oracle with provenance payload — done-when met
- #196 (closes da2723f): Closure-computation spike with design proposal — done-when met
- #197 (closes 325a049/1c4663d): Correctly tracked in BACKLOG.md and removed per ADR-65
- #199 (closes d752179): Refscan precision pass pruning immutable zones — done-when met

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 5 nightly appearances since 2026-06-11)** — Update CLAUDE.md §8: remove "No repo-level skills directory exists yet (`.claude/` holds `commands/` and `rules/` only)" and document `.claude/skills/` containing verify/ and check-against-spec/ (created 2026-06-19 by commit 442c994). One-line doc fix; the skills have been present and contradicting the claim since 2026-06-19.

---

## Safety Tripwire

`git status --porcelain` output (captured before commit):

```
?? docs/audits/2026-06-22-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
