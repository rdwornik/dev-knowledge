<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-17

**Date:** 2026-06-17
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-17, confirmed unavailable. Consistent with all prior nightly runs.)

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
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 skills directory, persisting 4 nights)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | S1 (high): CLAUDE.md §8 "no repo-level skills directory exists yet" | `.claude/skills/verify/` confirmed present; 5th consecutive nightly |
| **NEW** | S2 (high): CLAUDE.md §11 "last 5 ADRs" lists 76–80 but ADR-82–86 now exist | Window has not rotated since 2026-06-07 v2.16; 6 newer ADRs exist |
| **NEW** | S3 (med): VISION.md `last_reviewed: 2026-06-04` predates last edit 2026-06-11 | Per PLAYBOOK §4 cadence rule; audit.py check #10 flags this class |
| **NEW** | S4 (high): #152 BACKLOG closure contradicted — PLAYBOOK §8 NOT pointerized | Closure commit 0b89b1d claimed §8 pointerized; §8 is 83 lines of doctrine, not a pointer |

**Delta counts:** 0 resolved · 1 persisting · 3 new
**Skeptic kill-rate:** 43% (3 of 7 raw findings killed)

---

## Summary

Doc health has declined since the 2026-06-14 baseline. Three new findings join the one persisting finding, all with clear evidence commands. The skeptic kill-rate of 43% (3/7) is notably lower than last run's 75% — the new findings are real conformance gaps, not false positives.

The CLAUDE.md §8 skills-directory contradiction persists for a **fifth consecutive night** — it is a trivial one-line fix that has been correctly proposed in every digest since 2026-06-11. The CLAUDE.md §11 ADR rolling window is now 6 ADRs stale (last rotated 2026-06-07; ADR-81 through ADR-86 have since landed). The VISION.md freshness stamp predates its last edit by 7 days, triggering the PLAYBOOK §4 "edited-but-not-re-reviewed" conformance class. Most consequentially, a BACKLOG closure for #152 (PLAYBOOK §8 pointerization) appears premature: the item's own grooming log from 2026-06-12 states "pointerization unmet," yet the closure commit (0b89b1d) was recorded; §8 currently contains 83 lines of Roles, Handoff paths, and doctrine — not a pointer.

The three killed findings were correctly dismissed: V1's May-2026 JOURNAL entries predate the shallow-clone boundary (out-of-scope per spec); the worktree-runbook work in commit 509d8ef is correctly unlinked because items #143–145 remain intentionally open (research deferrals, not forgotten work); and the #150 commit-message style note is a preference, not a conformance rule.

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 4 · **Killed false positives:** 3

<!-- counts: raw=7 survived=4 killed=3 -->

### High (3)

**S1** — CLAUDE.md §8 stale repo-level skills claim *(PERSISTING from 2026-06-11; 5th consecutive nightly)*
- **Claim:** CLAUDE.md §8 states "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)"
- **Location:** CLAUDE.md:122
- **Evidence:** `ls -la /home/user/dev-knowledge/.claude/skills/verify/`
- **Verdict:** contradicted
- **Proposed fix:** Update CLAUDE.md §8 "Repo-level" bullet to document the existing `.claude/skills/verify/` directory (`SKILL.md` + `verify.py`). Remove the "No repo-level skills directory exists yet" sentence.
- **Skeptic note:** Directory visibly exists with verify skill files. Persisting factual contradiction for 5 nights.

**S2** — CLAUDE.md §11 "last 5 ADRs" window not rotated *(NEW)*
- **Claim:** CLAUDE.md §11 lists ADR-76, ADR-77, ADR-78, ADR-79, ADR-80 as "Recent ADRs binding here (last 5)"
- **Location:** CLAUDE.md:160-164
- **Evidence:** `ls -1 /home/user/dev-knowledge/docs/decisions/ADR-*.md | sort -V | tail -8`
- **Verdict:** contradicted — ADR-81 through ADR-86 all exist; window should be ADR-82–86
- **Proposed fix:** Rotate §11 "last 5" from ADR-76–80 to ADR-82–86 (per rolling-window convention last observed in v2.16 changelog entry of CLAUDE.md). Add one-liners for ADR-82–86; drop ADR-76–80 to the `docs/decisions/README.md` full list.
- **Skeptic note:** Six newer ADRs confirmed present. The rolling window hasn't moved since 2026-06-07 despite ADR-81–86 landing since then.

**S4** — #152 BACKLOG closure contradicted — PLAYBOOK §8 NOT pointerized *(NEW)*
- **Claim:** Commit 0b89b1d (2026-06-15) closes #152 as "PLAYBOOK pointerization Move 1"; Done-when required "no restated layer/handoff doctrine remains in §8"
- **Location:** commit 0b89b1d; grooming note 2026-06-12 states "KEPT OPEN reframed: #152 (§8 v4→v5 repointed but pointerization unmet)"
- **Evidence:** `sed -n '/^## 8\./,/^## 9\./p' /home/user/dev-knowledge/protocols/PLAYBOOK.md | wc -l`
- **Verdict:** contradicted — §8 is 83 lines of content (Roles, Handoff paths A/B/C, Output rendering doctrine), not a pointer
- **Proposed fix:** Either reopen #152 with a note that the commit delivered only the v4→v5 repoint (partial), and file a new item for full §8 pointerization; OR document that "Move 1" was intentionally scoped to just the v4→v5 repoint and the Done-when was misaligned.
- **Skeptic note:** The 2026-06-12 grooming log explicitly says "pointerization unmet" and flagged the item "KEPT OPEN reframed," yet a closure was recorded in 0b89b1d. The §8 current state confirms the Done-when clause was not met.

### Med (1)

**S3** — VISION.md `last_reviewed` stamp predates last edit *(NEW)*
- **Claim:** VISION.md frontmatter has `last_reviewed: 2026-06-04`
- **Location:** VISION.md:4
- **Evidence:** `git log --follow -1 --format="%ai" /home/user/dev-knowledge/VISION.md` → 2026-06-11 16:40:46
- **Verdict:** unsupported — stamp 2026-06-04, last edit 2026-06-11 (7 days gap)
- **Proposed fix:** Re-read VISION.md end-to-end and update `last_reviewed` to the re-read date (per PLAYBOOK §4 "Canonical-file freshness cadence" — stamp means genuinely re-read and confirmed accurate).
- **Skeptic note:** Per PLAYBOOK §4 and audit.py check #10, a stamp predating the last edit is a real conformance violation in this cadence model. The file was edited 7 days after the stamp.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — V1: May 2026 JOURNAL entries outside shallow-clone boundary
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The verifier self-identified these as OUT-OF-SCOPE per the shallow-history guard. Git history starts 2026-06-03; May entries predate that. Per the V1 spec, SHAs older than the history boundary are out-of-scope, not findings.

**K2** — V3: Worktree-runbook work (commit 509d8ef) shipped without backlog closure tag
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The work shipped as PLAYBOOK runbook addition + SUPERSEDED annotations on ADR-61. Items #143 (parallel-work-as-first-class-mode), #144 (feature-DoD E2E test), and #145 (codification-completeness) are research/methodology deferrals intentionally left open on the BACKLOG. They are not forgotten; they remain awaiting operator decision. No closure tag is expected because the items remain open by design.

**K3** — V3: #150 closure commit lacks explicit operator-authority stamp
- **Kill reason:** `style`
- **Kill detail:** Commit message style is a preference, not a conformance rule. The operator authority for #150's closure is documented in the BACKLOG item text and the prior decision annotation. Absence of a specific phrase in the commit message is not a conformance violation.

---

## Checked-and-Clean (absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; shallow-clone boundary: ~2026-06-03):**
- 2026-06-16: HANDOFF_PROCESS v5.1 — pytest 523 passed / 1 skipped — corroborated by git show 929c91d
- 2026-06-16: ADR-85 hard gate — pytest 516 passed / 5 skipped — corroborated by git show 11b44ca
- 2026-06-15: Faza A doc-flow pass — pytest 510 passed / 1 skipped — corroborated by git show c39634c
- 2026-06-16: ADR-82 amendment commit 5191ce8 exists and matches JOURNAL
- 2026-06-16: Session consolidation entry commits (2ed615e, c152254, 99f2bd4, 30ea942, 5d8bfa7, ef8ca43, 859e322) all exist
- 2026-06-16: assemble_paste architect-mode supplement 929c91d exists with +3 tests
- 2026-06-16: ADR-85 hard gate commits all exist (1212025, 9cd72ab, bbb9aa6, 47001ea, 4e60b01)
- All V1-checked SHAs fall within the available shallow-clone boundary (no pre-boundary out-of-scope SHA verified this run)

**V2 (living-doc factual claims):**
- CLAUDE.md §7 repo-level commands (/save, /handoff) — both .md files present in `.claude/commands/`
- CLAUDE.md §9 pre-commit hook list (8 hooks) — all 8 verified in `.pre-commit-config.yaml` (normalize-dated-headers, codemap-freshness, toc-freshness, toc-freshness-playbook, validate-backlog, audit-health, ruff, backlog-id-on-close)
- CLAUDE.md §1 handoff pointer — HANDOFF_BOOT.md (v5 bundles) and canonical `docs/handoffs/README.md` both exist
- CONTRIBUTING.md pre-commit hooks table — all 8 hooks match `.pre-commit-config.yaml`
- ARCHITECTURE.md Layer Boundaries invariant (validators read-only, no orchestration scripts) — correct
- ADR files referenced in CLAUDE.md §11 (ADR-76–80) all exist; ALSO ADR-81–86 all confirmed present
- ESSENTIALS.md structural claims — correct

**V3 (backlog-closure semantic coherence, since 2026-05-28):**
- #154 no_ff_merges FF-guard — semantically coherent
- #151 v5→canonical flip doc-sweep — semantically coherent
- #149 v5→canonical flip atomic — semantically coherent
- #148 v5 shipped with teeth, lean task-state, /handoff generator — coherent
- #111 prompt-format pack shipped; PLAYBOOK readiness valve added — coherent
- #84 two-tier automation doctrine codified; ADR-80 adoption — coherent
- #158 §Repo conventions + Appendices pointerized to ADRs — coherent
- #78, #79, #88 Phase C3 closeouts — coherent via JOURNAL records

---

## Next Actions (proposals for operator)

1. **S1 (high, persisting 5 nights)** — Update CLAUDE.md §8: change "No repo-level skills directory exists yet (.claude/ holds `commands/` and `rules/` only)" to document `.claude/skills/verify/` (added by #104). Simple one-line doc fix; directory has contradicted the claim since 2026-06-11.

2. **S2 (high, new)** — Rotate CLAUDE.md §11 "last 5 ADRs" window from ADR-76–80 to ADR-82–86. ADR-81 (feature lifecycle DoD), ADR-82 (HANDOFF_PROCESS v5 model C), ADR-83 (protocols archive convention), ADR-84 (automation writer isolation), ADR-85 (session lifecycle enforcement), ADR-86 (conformance dashboard location) all exist. Drop the 5 oldest from the inline list; full list remains in `docs/decisions/README.md`. This is the §11 rolling-window rotation last performed in v2.16 (2026-06-07).

3. **S4 (high, new)** — Resolve the #152 closure ambiguity: either reopen #152 with a note that commit 0b89b1d delivered "Move 1" (v4→v5 repoint only, not full pointerization) and file a new item for the remaining §8 pointerization work; OR amend the closure record to document that "Move 1" was intentionally scoped as partial and the Done-when was misaligned. §8 is currently 83 lines and must be reduced to a pointer for the Done-when to be met.

4. **S3 (med, new)** — Re-read VISION.md and update `last_reviewed` stamp. The file was edited 2026-06-11 but the stamp shows 2026-06-04 — a 7-day edited-but-not-re-reviewed gap that triggers audit.py check #10.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-17-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
