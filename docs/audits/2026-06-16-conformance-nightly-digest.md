<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-16

**Date:** 2026-06-16
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-16, confirmed unavailable. Consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md` *(no 2026-06-15 digest — 2-day gap)*
**Prior surviving findings:** 1 (S1 high persisting)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/verify/` confirmed present; claim directly contradicted; persisting from 2026-06-11 (**5th consecutive nightly with finding; no 06-15 digest**) |

**Delta counts:** 0 resolved · 1 persisting · 0 new
**Skeptic kill-rate:** 80% (4 of 5 raw findings killed)

---

## Summary

Continuing strong health. One finding persists for the **5th consecutive nightly** (no 2026-06-15 digest; 6-day-old baseline): CLAUDE.md §8 "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" is directly contradicted by the actual presence of `.claude/skills/verify/` (added 2026-06-10 via closes [#104]). This is a simple one-line documentation update that has been actionable since first detected on 2026-06-11.

The skeptic kill-rate of 80% (4/5) is healthy. The four kills reflect accurate filtering: (1) V1's bundle-count finding used the wrong artifact type in its evidence command (counted HANDOFF_BOOT.md files from June 11-15 only, while the JOURNAL's "12 v4 bundles" claim refers to all bundles across both v4 and v5 formats in docs/handoffs/ — evidence-not-definitive); (2) the pytest test-count finding (502 def test_ functions vs documented 511 "collected") was killed for the same reason as prior nights — counting def test_ functions is not equivalent to pytest --collect-only (parametrize expansion makes collected count > function count); (3) the [closes #164-slice] non-standard syntax was killed as true-but-irrelevant (#164 remains intentionally OPEN in BACKLOG and the commit is a partial slice delivery, not a fraudulent closure); (4) the 509d8ef worktree runbook without #107 closure was killed as true-but-irrelevant (d92d3c2, 2026-06-13, already references #107 in its commit message as the root-cause fix, and #107 is no longer an active BACKLOG item).

---

## Findings (PROPOSALS ONLY)

**Raw:** 5 · **Survived skeptic:** 1 · **Killed false positives:** 4

<!-- counts: raw=5 survived=1 killed=4 -->

### High (1)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory (`SKILL.md` + `verify.py`). Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Directory visibly exists with verify skill files. Added 2026-06-10 via closes [#104]. CLAUDE.md was last reviewed 2026-06-12, after the directory was added — the re-review missed this update.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — JOURNAL.md:26 "the hub has 12 valid stamped v4 bundles" for handoff_bundle_structure check
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The evidence_command (`git ls-tree -r --name-only 2f560a2 | grep 'docs/handoffs/2026-06-1[1-5].*HANDOFF_BOOT.md'`) counts only v5-format bundles (those with HANDOFF_BOOT.md) from June 11-15. The JOURNAL explicitly says "v4 bundles" — a different format. There are 40 total directories in docs/handoffs/ including older v4-format bundles (without HANDOFF_BOOT.md). The evidence command cannot disprove a claim about v4 bundles by counting v5 bundles over a restricted date range.

**K2** — ARCHITECTURE.md:274 "pytest unit tests for the validators (**511 collected**)"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Same root cause as prior nights (K2 in 2026-06-14 digest). The evidence_command counts `def test_` function definitions (502), but "collected" in pytest means the count AFTER parametrize expansion — a single def test_ with @pytest.mark.parametrize(N cases) yields N collected tests. Without pytest available in this cloud environment, the function-count evidence cannot definitively disprove the 511 "collected" claim. The count was freshly bumped to 511 in commit d34487f (2026-06-15) by an author running actual pytest.

**K3** — commit 354df89 uses `[closes #164-slice]` non-standard closure syntax
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** While `[closes #164-slice]` is non-standard (the repo pattern is `closes [#<id>]`), #164 remains intentionally OPEN in BACKLOG.md because this commit is a partial slice delivery (PASTE_THIS.md assembler), not a full closure. The '-slice' suffix is a naming variant signaling partial delivery. The backlog-id-on-close hook fires on `[#\d+]` which the syntax contains, so the gate was not bypassed. The semantic question (did the commit match its stated scope?) is yes — the commit delivers exactly what the JOURNAL/PR describe for the slice.

**K4** — commit 509d8ef delivers worktree operator-runbook work without closing a backlog item
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Commit d92d3c2 (2026-06-13, "Merge chore/worktree-watcher-exclude -- root-cause fix for locked worktree-dir leftovers (#107 gotcha)") already references #107 as delivered scope. #107 is no longer an active item in BACKLOG.md. The 509d8ef commit (2026-06-16) delivers additional worktree documentation (PLAYBOOK runbook + ESSENTIALS/ADR-61 SUPERSEDED annotations) and is additive follow-on work, not the primary #107 delivery vehicle. No formal `closes [#107]` commit exists, but the item's scope was handled across multiple commits and grooming, and it is not present in the live BACKLOG.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-15: Faza A A2 (G6) — vacuous hub no-op checks report `n/a` — commits c39634c/d34487f/2f560a2 verified in git
- 2026-06-15: Faza A A1 — pytest_collected bumped 500→511 in ARCHITECTURE.md — verified in d34487f
- 2026-06-15: changelog-review session — digest at `2026-06-15-changelog-review.md` — commits 3ddaf6d/fdf2b87 verified
- 2026-06-15: architect-mode v5 handoff — bundle with HANDOFF_BOOT.md/RESIDUAL.md/PROBES.md generated — files verified in repo
- 2026-06-15: hybrid session handoff — bundle created at `docs/handoffs/2026-06-15-dev-knowledge-session` — verified in repo
- 2026-06-14: ADR-84 Q9 automation isolation ratified — commits 0ca36f1/374e602 verified as ancestors of HEAD
- 2026-06-14: ADR-66 ratified — commits 0e9cf6f/086aae2 verified
- 2026-06-15: Move-1 pointerization (#152/#158) — commits 76bf001/3b58611/3981c5a/0b89b1d verified
- 2026-06-14: collision graph encoded (#150) — commit 89f0ed0 verified
- ARCHITECTURE.md last_reviewed re-stamped to 2026-06-15 — verified live (commit 3a78133)

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-06-15` frontmatter — verified current
- ARCHITECTURE.md "19 registered checks" in ALL_CHECKS — verified correct
- CLAUDE.md §11: ADR-76 through ADR-80 all exist in `docs/decisions/` — verified
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in `.pre-commit-config.yaml`
- CONTRIBUTING.md pre-commit hooks table — matches `.pre-commit-config.yaml` (8 hooks)
- `.claude/commands/` contains `save.md`, `handoff.md`, `changelog-review.md` — verified
- ESSENTIALS.md worktree section — SUPERSEDED annotation present; PLAYBOOK canonical content at line 1056 — verified (509d8ef)
- VISION.md tier system deprecated 2026-05-23 per ADR-38 — confirmed

**V3 (backlog-closure semantic coherence, since 2026-05-24):**
- 0b89b1d (closes [#152] [#158]) — PLAYBOOK pointerization, removed items match promised scope — coherent
- d849bf9 (closes [#150]) — collision graph encoding + task-graph redesign, diffs match Done-when — coherent
- Recent Faza A closures (A1/A2 doc fixes) — diff content matches JOURNAL description
- BACKLOG.md validate_backlog gate — passing (65 tasks, no schema errors)

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 5 nights)** — Update CLAUDE.md §8: change "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" to document `.claude/skills/verify/` (added by #104 on 2026-06-10). This is a simple one-line doc fix; the directory has been present and contradicting the claim for 6 days.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-16-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
