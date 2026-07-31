<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-31

**Date:** 2026-07-31
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-07-31; confirmed unavailable, consistent with all prior nightly runs.)

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
**Gap:** 47 days (2026-06-14 → 2026-07-31); significant repo changes in interval (ADRs 88–108, v6.0 boot, ADR-107 strangler, uv adoption ADR-106, hermetization ADR-101, and many more).

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (HIGH, persisting 4 nights): CLAUDE.md §8 "No repo-level skills directory exists yet" | Fixed — §8 now correctly documents `.claude/skills/verify` + `check-against-spec`. Verified clean by V2. |
| **NEW** | S1 (HIGH): uv version mismatch — cloud env 0.8.17 vs required 0.11.19 | All `uv run --locked` hooks non-functional in this cloud runtime. |
| **NEW** | S2 (MED): ARCHITECTURE.md "through ADR-107" stale | ADR-108 ratified 2026-07-31; not mentioned in ARCHITECTURE.md anywhere. |
| **NEW** | S3 (MED): VISION.md terminal-setup listed as fleet repo | Absent from ecosystem/registry.md (only 8 rows, no terminal-setup). |
| **NEW** | S4 (LOW): CONTRIBUTING.md nightly GitHub Action described as live | .github/ directory deleted; ARCHITECTURE.md acknowledges but CONTRIBUTING.md uncorrected. |
| **NEW** | S5 (LOW): VISION.md `last_reviewed: 2026-07-25` predates last commit | Git shows c74f918 on 2026-07-26; A2 gate would fire. |

**Delta counts:** 1 resolved · 0 persisting · 5 new
**Raw → survived → killed:** 10 → 5 → 5
**Skeptic kill-rate:** 50% (5 of 10 raw findings killed)

---

## Summary

After a 47-day gap, the repo shows overall strong health — 27 concrete JOURNAL claims verified against git, 19 BACKLOG closures verified semantically coherent, and the formerly-persistent §8 skills claim is resolved. The 50% skeptic kill-rate reflects that several of V1's findings were legitimate but too minor for conformance tracking (count errors in JOURNAL SHA parentheticals, batch-vs-one-commit description inaccuracies).

Five findings survive. The most significant is an infrastructure finding: the cloud runtime's `uv 0.8.17` is ~30 point releases behind the project's `required-version = "==0.11.19"` (ADR-106), meaning **every** `uv run --locked` command fails — pre-commit hooks, the session-end backpressure gate, the verify cadence. This was witnessed directly during this run via repeated stop-hook failures. Two medium-severity doc-currency gaps: ARCHITECTURE.md's "ratified through ADR-107" claim is one day stale (ADR-108 ratified 2026-07-31, not yet reflected), and terminal-setup is listed in VISION.md/ADR-104 as a fleet repo but is missing from ecosystem/registry.md. Two low-severity items complete the set.

<!-- counts: raw=10 survived=5 killed=5 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 10 · **Survived skeptic:** 5 · **Killed false positives:** 5

### High (1)

**S1** — Cloud runtime uv version mismatch: all `uv run --locked` hooks non-functional
- **Claim:** ADR-106 pinned toolchain (`required-version = "==0.11.19"`) is in effect; session-end backpressure gate and pre-commit hooks execute normally.
- **Location:** `pyproject.toml:25` / `.claude/settings.json` Stop hook
- **Evidence:** `uv --version` → `0.8.17`; `grep required-version pyproject.toml` → `required-version = "==0.11.19"`
- **Verdict:** contradicted
- **Proposed fix:** Upgrade the cloud runtime's uv to exactly 0.11.19 per ADR-106's own gated-change procedure (dedicated reviewed commit, regenerate uv.lock). This is an environment-level change, not a doc edit.
- **Skeptic note:** Witnessed directly during this run — every stop hook invocation returned the same version mismatch error. Impact is systemic: all `uv run --locked` commands across all pre-commit hooks and session gates are rejected.

### Med (2)

**S2** — ARCHITECTURE.md "through ADR-107" claim stale after ADR-108 ratification
- **Claim:** "The six chapters below are the system as built and ratified through ADR-107." (Purpose section)
- **Location:** `ARCHITECTURE.md:70`
- **Evidence:** `ls docs/decisions/ADR-108-decision-routing-and-engineering-standards.md && grep -c 'ADR-108' ARCHITECTURE.md` → file exists + 0 occurrences
- **Verdict:** contradicted
- **Proposed fix:** Add ADR-108 to ARCHITECTURE.md's Governing ADRs section and update the Purpose line from "through ADR-107" to "through ADR-108". ADR-108 (decision-routing doctrine + standing engineering standards) is substantive doctrine; the ratification commit `09eb57c` did not update ARCHITECTURE.md.
- **Skeptic note:** Read the Governing ADRs section (lines 790–826) — it ends at ADR-107 with no ADR-108 entry. Confirmed by grep returning 0.

**S3** — terminal-setup listed as fleet repo in VISION.md but absent from ecosystem/registry.md
- **Claim:** "The fleet is nine git repos (ADR-104): the hub .dev-knowledge plus eight child repositories — ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, demo-prep, life-architect, terminal-setup, win-tooling."
- **Location:** `VISION.md:107-111`
- **Evidence:** `grep -n 'terminal-setup' ecosystem/registry.md; grep -c '^| ' ecosystem/registry.md` → 0 matches; 9 pipe-table rows (8 data + 1 header)
- **Verdict:** contradicted
- **Proposed fix:** Add a terminal-setup row to `ecosystem/registry.md` (the hand-maintained human fleet registry). The preamble says "Add a row when a repo is created"; this repo was declared in ADR-104 but never registered.
- **Skeptic note:** registry.md read in full — eight data rows, no terminal-setup. ARCHITECTURE.md:822 confirms ADR-104 declares 9 repos. Gap is definitive.

### Low (2)

**S4** — CONTRIBUTING.md Nightly outcome management section describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (.github/workflows/nightly-conformance-triage.yml) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls .github/ 2>/dev/null || echo 'No .github directory'` → No .github directory
- **Verdict:** contradicted
- **Proposed fix:** Update CONTRIBUTING.md §Nightly outcome management to replace the live-Action description with a tombstone note pointing to ARCHITECTURE.md Ch6's caveat. ARCHITECTURE.md does flag this section as stale (lines 715–716) but CONTRIBUTING.md is unedited.
- **Skeptic note:** No .github directory. CONTRIBUTING.md presents the Action as live operational guidance without caveat. An operator reading only CONTRIBUTING.md receives a false workflow picture.

**S5** — VISION.md `last_reviewed: 2026-07-25` predates last git-commit date 2026-07-26
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git log --format='%ai %h' -1 -- VISION.md` → `2026-07-26 16:14:02 +0200 c74f918`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to the current date. The audit.py A2 gate compares frontmatter date vs git commit date; 2026-07-25 < 2026-07-26 constitutes a definitive A2 FAIL at next gate run.
- **Skeptic note:** Git log confirms one commit on 2026-07-26. The stamp dates from the branch-pre-commit review; the merge to main advanced the commit date by one day. A2 would fire.

---

## Killed Findings

**K1** — ARCHITECTURE.md inline "Last updated: 2026-07-28" narrative header stale
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The inline "Last updated:" block is a human-maintained narrative, not a machine-checked conformance field. The authoritative freshness indicator is frontmatter `last_reviewed: 2026-07-31`, which is current (2026-07-31 > last commit 2026-07-30). audit.py A2 compares only the frontmatter stamp; the inline header has no gate. Evidence is not definitive that any conformance rule governs it.

**K2** — JOURNAL entry (c): SHA range parenthetical claims "6 commits" (actual: 4)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Count error in a parenthetical descriptive comment within a SHA anchor line. JOURNAL entries are tactical notes; commit counts in parentheticals are not governance-binding. All commits in the range exist and are corroborated; the error has no downstream effect on any gate or process.

**K3** — JOURNAL entry (c): "one commit each" for 8 findings (actual: F5-F8 batched in one commit)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Same class as K2. JOURNAL describes work done; the precise batching of findings into commits is not a conformance claim. All 8 findings were addressed; the batching is visible in git history.

**K4** — JOURNAL entry (h): third merge commit a54994a (v6 bundle) unmentioned in "two operator-authorized acts"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The merge a54994a (docs/handoff-2026-07-31-architect-2) is documented in detail across entries (e), (f), and (g). Entry (h) scopes only the acts performed IN that session (night-branch merge + ratification batch). The bundle merge was a separate earlier session. No governance omission.

**K5** — [#352] Done-when met but ADR-70 closure gate not executed; row open in BACKLOG.md
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-70 Tier-1 lifecycle explicitly allows work-complete items to remain open until an operator-approved /review-closures cycle removes them. The [#352] shelf-life extends to 2026-08-13 (13 days out); this is within the normal ADR-70 window. The Done-when amendment is transparent. The item will be proposed at the next /review-closures run.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; all within shallow-clone boundary):**
- 27 concrete claims verified against git history — all clean
- Entry (h): SHA anchors 09eb57c4, 64893913, 6bfa544f, f2ae0a80, f2ed2648, 645822ba all match git log ✓
- Entry (d): merge SHA 7f8a0473 matches `Merge branch 'feat/446-boot'` ✓
- Entry (a): SHA anchor 65483b39 matches Step 8 feat(446) commit ✓
- Entry (c): SHA anchor 55b07712 matches F5-F8 rulings commit ✓
- Entry (f 2026-07-31): SHA anchor 68d767db matches first-live-v6-bundle handoff commit ✓
- All handoff files (docs/handoffs/2026-07-31-dev-knowledge-architect-2/) exist on disk ✓
- All tasks/448–452 exist on disk ✓
- The [#446] 9-commit frozen contract claim confirmed by git log ✓
- The six reconciled_with edges claim confirmed by commit message ✓

**V2 (living-doc factual claims):**
- CLAUDE.md §8: `.claude/skills/` holds exactly `verify` + `check-against-spec` ✓
- Pre-commit hook count 15: matches .pre-commit-config.yaml and doc-counts.md exactly ✓
- CLAUDE.md §7 commands (5 files): changelog-review, handoff-verify, handoff, override, save ✓
- Generated fragments: .claude/generated/commands-repo.md + recent-adrs.md match disk ✓
- Recent ADRs ADR-104 through ADR-108 all exist in docs/decisions/ ✓
- CLAUDE.md `last_reviewed: 2026-07-31` — current; last edit 2026-07-30 ✓
- ARCHITECTURE.md `last_reviewed: 2026-07-31` — current; last edit 2026-07-30 ✓
- CONTRIBUTING.md `last_reviewed: 2026-07-31` — current; last edit 2026-07-30 ✓
- ESSENTIALS.md `last_reviewed: 2026-07-30` — current; last edit 2026-07-29 ✓
- CLAUDE.md §9 ruff pin v0.15.5 matches rev: v0.15.5 in .pre-commit-config.yaml ✓
- tier1-lifecycle plugin enabled in .claude/settings.json ✓
- CLAUDE.md §12 v2.48 "six reconciled_with edges @5.7→@6.0" confirmed by commit 65483b3 ✓

**V3 (BACKLOG closure semantic coherence, since 2026-07-10):**
- 19 closures verified semantically coherent: #131, #292, #302, #309, #314, #321, #355, #372, #386, #395, #398, #421, #434, #435, #436, #437, #439, #444, #446 — all Done-when clauses verified against live state
- [#437] strip_quoted_contexts: shared helper exists in propose_closures.py:79; imported by validate_git_backlog; seeded-tag tests present in tests/test_closure_token_quoting.py ✓
- [#444] tier1-lifecycle 0.1.11: plugin.json + manifest both show 0.1.11; 0.1.10 tombstoned ✓
- [#386] delivery loop: PLAYBOOK §21 "The delivery loop (end-to-end)" exists at line 3773 ✓
- [#446] v6.0 boot: one-round-trip boot shipped; 9/9 frozen tests GREEN; HANDOFF_PROCESS v6.0 stamped ✓

---

## Next Actions (proposals for operator)

1. **S1 (HIGH)** — Upgrade cloud runtime uv to `==0.11.19`. Every governance gate in this runtime is currently non-functional (pre-commit hooks, session-end gate). ADR-106 gated-change procedure: dedicated reviewed commit + uv.lock regen.

2. **S2 (MED)** — Update ARCHITECTURE.md: add ADR-108 bullet to the Governing ADRs section; change "ratified through ADR-107" to "through ADR-108" in the Purpose section. Simple doc update; same-day fix.

3. **S3 (MED)** — Add terminal-setup row to `ecosystem/registry.md`. The repo was declared in ADR-104 but never registered in the human-maintained fleet registry.

4. **S4 (LOW)** — Update CONTRIBUTING.md §Nightly outcome management: replace live-Action prose with a tombstone pointing to ARCHITECTURE.md Ch6. Low urgency; the stale section is already flagged in ARCHITECTURE.md.

5. **S5 (LOW)** — Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to today's date. The A2 gate will fire at next audit run.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-07-31-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
