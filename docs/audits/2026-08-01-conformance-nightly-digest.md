<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-01

**Date:** 2026-08-01
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-01; confirmed unavailable, consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-07-31-conformance-nightly-digest.md`
**Gap:** 1 day (2026-07-31 → 2026-08-01)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | prior S2 (MED): ARCHITECTURE.md "through ADR-107" stale | Fixed — ARCHITECTURE.md now reads "through ADR-109"; commit 2689740 on 2026-07-31 added ADR-108 + ADR-109 bullets. V2 verified clean. |
| **PERSISTING** | prior S1 (HIGH): uv version mismatch — cloud env 0.8.17 vs required 0.11.19 | Infrastructure condition unchanged. Stop hooks continued to fail with the same version error throughout this session. Not re-verifier-checked today (scope was doc claims), but stop hook output confirms it persists. |
| **PERSISTING** | prior S5 (LOW → HIGH): VISION.md `last_reviewed: 2026-07-25` predates last commit | Severity upgraded. Stamp has not been corrected since it was first flagged 2026-07-31. Today's S2. |
| **PERSISTING** | prior S4 (LOW → HIGH): CONTRIBUTING.md Nightly outcome management describes dead Action as live | Severity upgraded. Still unfixed since 2026-07-31. Today's S3. |
| **PERSISTING** | prior S3 (MED): terminal-setup absent from ecosystem/registry.md | Unchanged. Today's S4. |
| **NEW** | today S1 (MED): JOURNAL entry (t) cites broken SHA ee76c412 | SHA does not exist in git history; actual skeleton commit is 48879e2. |

**Delta counts:** 1 resolved · 4 persisting · 1 new
**Raw → survived → killed:** 11 → 4 → 7
**Skeptic kill-rate:** 64% (7 of 11 raw findings killed)

---

## Summary

Overall doc health is solid — 15 JOURNAL claims and 30+ SHA anchors verified against git, 13 backlog closures verified semantically coherent, and the ARCHITECTURE.md ADR currency gap (prior S2) resolved. The 64% skeptic kill-rate reflects aggressive filtering of forward-dated stamps (not A2 violations), self-correcting journal count errors, and a housekeeping-narration preference.

Four findings survive. Two are elevated from LOW severity versus the prior digest: VISION.md's `last_reviewed: 2026-07-25` stamp predates its last commit (2026-07-26), constituting a genuine A2 canonical_freshness violation that has now been unfixed for two nightly runs; and CONTRIBUTING.md's "Nightly outcome management" section continues to describe a deleted GitHub Action in the present tense — a live misdirection for any developer reading that document. One medium-severity journal integrity issue is new: JOURNAL entry (t) cites commit SHA `ee76c412` as the handoff-skeleton anchor, but this SHA is absent from all of git history (the real skeleton commit is `48879e2`). The terminal-setup registry gap persists as medium severity. The systemic uv infrastructure finding (prior S1) persists unaddressed.

<!-- counts: raw=11 survived=4 killed=7 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 11 · **Survived skeptic:** 4 · **Killed false positives:** 7

### High (2)

**S2** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-07-26 (A2 violation)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git -C /home/user/dev-knowledge log --format='%cd' --date=format:'%Y-%m-%d' -1 -- VISION.md` → `2026-07-26`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to the current date. The canonical_freshness A2 gate compares frontmatter stamp vs last commit date; 2026-07-25 < 2026-07-26 is a definitive FAIL. Persisting unfixed since 2026-07-31 digest S5.
- **Skeptic note:** Stamp predates the last edit by one day — exactly the canonical_freshness A2 violation. No ADR exempts VISION.md. Confirmed by live git check.

**S3** — CONTRIBUTING.md "Nightly outcome management" section describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (.github/workflows/nightly-conformance-triage.yml) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null && echo EXISTS || echo MISSING` → `MISSING`
- **Verdict:** contradicted
- **Proposed fix:** Replace CONTRIBUTING.md §Nightly outcome management present-tense live-organ description with a tombstone pointing to ARCHITECTURE.md Ch6 (which already carries the caveat). The Action was retired at commit `82227f08` (2026-07-08); no ADR permanently exempts this section from correction. Persisting unfixed since 2026-07-31 digest S4.
- **Skeptic note:** `.github/` directory confirmed MISSING. ARCHITECTURE.md's own note defers correction without dismissing it. A developer reading CONTRIBUTING.md in present tense is actively misled.

### Med (2)

**S1** — JOURNAL entry (t) cites broken SHA anchor `ee76c412`
- **Claim:** "skeleton committed ee76c412 on docs/2026-08-01-handoff-skeleton" (JOURNAL.md entry t Result block)
- **Location:** `JOURNAL.md:257`
- **Evidence:** `git rev-parse ee76c412` → `fatal: ambiguous argument 'ee76c412': unknown revision`
- **Verdict:** contradicted
- **Proposed fix:** Update JOURNAL.md entry (t) to cite the actual skeleton commit SHA `48879e2` in place of the non-existent `ee76c412`. The skeleton work itself is real (commit `48879e2` adds HANDOFF_BOOT.md, PROBES.md, RESIDUAL.md, SUPPLEMENT.md); only the SHA anchor is wrong — likely changed by an amend or rebase after the journal entry was written.
- **Skeptic note:** `git rev-parse ee76c412` definitively returns fatal. A journal anchor that cannot resolve is a broken reference regardless of whether the underlying work is real. No ADR documents that journal SHA anchors may be approximate.

**S4** — terminal-setup listed as fleet repo in VISION.md but absent from ecosystem/registry.md
- **Claim:** "The fleet is nine git repos (ADR-104): the hub .dev-knowledge plus eight child repositories — ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, demo-prep, life-architect, terminal-setup, win-tooling."
- **Location:** `VISION.md:108-113`
- **Evidence:** `grep -n 'terminal-setup' /home/user/dev-knowledge/ecosystem/registry.md` → 0 matches; registry has 8 rows (hub + 7 children)
- **Verdict:** omitted
- **Proposed fix:** Add a terminal-setup row to `ecosystem/registry.md` per the file's own "add a row when a repo is created" instruction. The repo was declared in ADR-104 but never registered. Persisting unfixed since 2026-07-31 digest S3.
- **Skeptic note:** grep returns nothing. VISION.md:111 and ADR-104 both place terminal-setup in the 9-repo fleet; registry's own header instruction is unambiguous. No ADR documents an exemption or deferral.

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — Entry (s): "net backlog delta is +3 (4 filed, 1 closed, 181→185 incl. this pack's two)"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The count in entry (s) was a transient intermediate state; entry (t) — the immediately following entry — explicitly self-corrects to "5 ids filed, net +4." A parenthetical count discrepancy self-corrected in the next entry leaves no persisting conformance defect.

**K2** — Entry (u) Changes section omits accretion-threshold trim commits (5442074, 09fa62f)
- **Kill reason:** `opinion`
- **Kill detail:** No protocol requires journal Changes blocks to enumerate every commit in the covered range. Non-destructive housekeeping commits not appearing in journal narrative is a completeness preference, not a rule violation. The finding's own note calls the trim "non-destructive housekeeping."

**K3** — ARCHITECTURE.md inline narrative header "Last updated: 2026-07-28"
- **Kill reason:** `documented-decision`
- **Kill detail:** Killed in the prior digest (K1, kill_reason: evidence-not-definitive) on the same grounds and grounds remain valid: the authoritative freshness indicator is the frontmatter stamp (`last_reviewed: 2026-07-31`), which passes A2. The inline narrative box header is non-canonical per ADR-51's hybrid approach. Re-killing on the same K1 basis.

**K4** — ESSENTIALS.md frontmatter `last_reviewed: 2026-07-30` (one day ahead of last commit 2026-07-29)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** canonical_freshness A2 only fails when the stamp predates the last edit. A forward-dated stamp is not a conformance violation — the check passes. The finding's own note confirms "A2 check would NOT flag it."

**K5** — CLAUDE.md frontmatter `last_reviewed: 2026-07-31` (one day ahead of last commit 2026-07-30)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Same pattern as K4: forward-dated stamp, canonical_freshness A2 does not flag it. Not a conformance violation.

**K6** — CONTRIBUTING.md frontmatter `last_reviewed: 2026-07-31` (one day ahead of last commit 2026-07-30)
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Same pattern as K4 and K5. Note: this frontmatter finding is independent of surviving finding S3 about the dead Action prose in CONTRIBUTING.md lines 132-136.

**K7** — Commit a42e5fc closes [#370] with "self-referential Done-when" rationale, but Done-when text mentioned marker/template/test work
- **Kill reason:** `documented-decision`
- **Kill detail:** Architect-ratified under ADR-108 §A technical lane authority. The Done-when text is genuinely conditional and self-referential — it delegates to "whatever the ruling calls for" without specifying any concrete deliverable. The commit explicitly addresses prior refusals (d66aef63, 4911f009), establishes independent grounds, and documents the non-blocking follow-up in JOURNAL. ADR-65 governs backlog done-item disposition; ADR-108 §A covers architect authority over this lane.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; all within shallow-clone boundary):**
- Entry (y): SHA anchors 9a75777e, 0807fbda, 597c81ab all match described purposes (intake split, §4 DISCHARGED, four HIGH findings closed) ✓
- Entry (y): scripts/gen_intake_tree.py and tests/test_gen_intake_tree.py (26 test cases) confirmed present ✓
- Entry (x): SHA anchors 5fc6b8ab and a489402f both exist; merge to main confirmed at f2ccda9 ✓
- Entry (v): SHA anchors 626c51bb, f4c3503f, ede6fc5a all exist; PASTE_THIS 51454 B claim confirmed ✓
- Entry (u): SHA anchors bb217819, 61757e82, bd08f343, b2329590, 13b98f2 all exist; ARCHITECTURE.md ADR-107→ADR-109 update confirmed ✓
- Entry (s): SHA anchors 0acc3328, f7abe22, d47c94a1, 9fa4105f all exist; 185-row BACKLOG count confirmed ✓
- Entry (r): SHA anchors 8ed32d0d, 7f5e8cec, d62acf3d, 517fc524 all exist ✓
- 30+ SHA anchors verified; no significant merged work missing from last 10 entries ✓

**V2 (living-doc factual claims):**
- ARCHITECTURE.md "through ADR-109": correct — ADR-109 is the latest ADR, ARCHITECTURE.md updated 2026-07-31 ✓
- Pre-commit hook count 15: matches `.pre-commit-config.yaml` and `doc-counts.md` exactly ✓
- CLAUDE.md §7 commands (5 files): changelog-review, handoff-verify, handoff, override, save ✓
- CLAUDE.md §8 skills: `.claude/skills/` holds exactly `verify` + `check-against-spec` ✓
- Recent ADRs fragment accurate through ADR-109 — all five files exist ✓
- ARCHITECTURE.md `last_reviewed: 2026-07-31` — current (last commit 2026-07-31) ✓
- CLAUDE.md `last_reviewed: 2026-07-31` — A2 gate passes (stamp ≥ last commit 2026-07-30) ✓
- CONTRIBUTING.md `last_reviewed: 2026-07-31` — A2 gate passes (stamp ≥ last commit 2026-07-30) ✓
- ESSENTIALS.md `last_reviewed: 2026-07-30` — A2 gate passes (stamp ≥ last commit 2026-07-29) ✓
- CLAUDE.md §9 ruff pin v0.15.5 matches rev in `.pre-commit-config.yaml` ✓
- tier1-lifecycle plugin enabled in `.claude/settings.json` ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-11 → 2026-08-01):**
- 13 closures verified semantically coherent: #382, #386, #434, #435, #436, #437, #439, #444, #35, #41, #367, #446, #421 — all Done-when clauses verified against live state ✓
- #382: ADR-109 accepted + schema v1 committed — both clauses confirmed ✓
- #446: v6.0 one-round-trip boot shipped; 9/9 frozen tests GREEN ✓
- #437: shared helper exists in propose_closures.py:79; twin parity pinned; 110 tests green ✓

---

## Next Actions (proposals for operator)

1. **(PERSISTING-HIGH, infrastructure)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (pre-commit hooks, session-end gate fail with version mismatch). ADR-106 gated-change procedure: dedicated reviewed commit + uv.lock regen. Still blocking from prior digest S1.

2. **S2 (HIGH)** — Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to current date. The A2 canonical_freshness gate fires at every audit run. Two-day backlog.

3. **S3 (HIGH)** — Update CONTRIBUTING.md §Nightly outcome management: replace present-tense GitHub Action description with a tombstone pointing to ARCHITECTURE.md Ch6. Two-day backlog; low-effort fix.

4. **S1 (MED)** — Update JOURNAL.md entry (t) line 257: replace broken SHA `ee76c412` with actual skeleton commit SHA `48879e2`. Simple one-line correction to restore journal integrity.

5. **S4 (MED)** — Add terminal-setup row to `ecosystem/registry.md`. The repo was declared in ADR-104 but never registered. Three-day backlog.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-01-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
