<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-09

**Date:** 2026-08-09
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-09; confirmed unavailable, consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent + inline verification) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (inline orchestrator pass) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-08-02-conformance-nightly-digest.md`
**Gap:** 7 days (2026-08-02 → 2026-08-09)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | prior S1 (MED): CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live | Fixed — section now says "RETIRED 2026-07-08" and correctly describes the new `report-only-wall.yml` gate; V2 verified this session. |
| **PERSISTING (WORSE)** | prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit | Gap widened: prior baseline had stamp vs 2026-07-26 (1 day); today's last commit is 2026-08-04 (10-day gap). Today's S3. |
| **NEW** | S1 (HIGH): ESSENTIALS.md:123 instructs agents `/override [reason]` is the only session-end escape | ADR-85 amendment 2026-08-03 §A2 retired `/override`; CLAUDE.md corrected in v2.51; ESSENTIALS.md not updated (canonical drift). |
| **NEW** | S2 (MED): ARCHITECTURE.md "five carriers" — six exist on disk | `carrier_docs.py` added by batch-3 lane 280/315 at 22:36 on 2026-08-08, after the ARCHITECTURE.md review stamp (~18:23 same day); 4 stale occurrences. |
| **NEW** | S4 (MED): ESSENTIALS.md `last_reviewed: 2026-07-30` predates last commit 2026-08-04 | New A2 violation; 5-day gap. |
| **NEW** | S5 (LOW): ARCHITECTURE.md gates paragraph omits `block-unanchored-push` | Hook live since 2026-08-03; completely absent from ARCHITECTURE.md despite a review on 2026-08-08. |

**Delta counts:** 1 resolved · 1 persisting (worse) · 4 new
**Raw → survived → killed:** 6 → 5 → 1
**Skeptic kill-rate:** 17% (1 of 6 raw findings killed)

---

## Summary

Overall doc health regressed this cycle after the batch-3 integration on 2026-08-08. The prior persistent finding on CONTRIBUTING.md is resolved (confirmed by V2 this run), but the batch-3 arc introduced new drift: `carrier_docs.py` (the 6th carrier) landed after ARCHITECTURE.md's review stamp was set, leaving "five carriers" stale across four locations; and `block-unanchored-push` (live since 2026-08-03) is completely absent from ARCHITECTURE.md despite the 2026-08-08 re-read. The more significant finding is HIGH-severity: ESSENTIALS.md line 123 still instructs agents that `/override [reason]` is the only session-end gate escape — exactly the claim CLAUDE.md v2.51 corrected on 2026-08-03 when the ADR-85 amendment retired that path. The two backward-dated freshness stamps (VISION.md at 10 days, ESSENTIALS.md at 5 days) both block `audit.py` check #10. The skeptic kill-rate is low (17%) because the batch-3 merges brought genuine, verifiable drift rather than edge-case interpretation noise.

<!-- counts: raw=6 survived=5 killed=1 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 6 · **Survived skeptic:** 5 · **Killed false positives:** 1

### High (1)

**S1** — ESSENTIALS.md:123 instructs agents `/override [reason]` is the only session-end gate escape (ADR-85 §A2 retired this path on 2026-08-03)
- **Claim:** "JOURNAL is hard-gated at session-end (ADR-85, C1): a session with commits must name ≥1 commit SHA from *this session* or the Stop-hook blocks turn-end; `/override [reason]` is the only escape."
- **Location:** `protocols/ESSENTIALS.md:123`
- **Evidence:** `grep -n "override.*only escape" /home/user/dev-knowledge/protocols/ESSENTIALS.md` → line 123 confirmed; `grep -n "A2 RETIRED\|override.*retired\|advisory in full" /home/user/dev-knowledge/CLAUDE.md` → §7 confirms ADR-85 amendment §A2 retired the `/override` path in CLAUDE.md v2.51 (2026-08-03).
- **Verdict:** contradicted
- **Proposed fix:** Update `protocols/ESSENTIALS.md` line 123: replace `/override [reason]` is the only escape` with `the sole escape for the pre-push hard leg is \`git push --no-verify\` (ADR-85 amendment 2026-08-03 §A2 retired \`/override\`; Stop hook is advisory in full).`
- **Skeptic note:** CLAUDE.md v2.51 §12 explicitly says "DRIFT FOUND AND FIXED BY THIS RE-READ: §7 still described ADR-85 §4 /override as 'the gate's only escape', which the amendment §A2 retired — corrected in place." ESSENTIALS.md is the always-on PLAYBOOK summary that every session boots on; wrong escape instructions are HIGH-severity operational risk. No ADR or documented decision covers leaving the stale claim in ESSENTIALS.md.

### Med (3)

**S2** — ARCHITECTURE.md claims "five carriers" across four locations; six carrier files exist on disk
- **Claim:** "the five carrier modules" / "five carriers (carrier_globalconfig, carrier_plugin, carrier_precommit, carrier_floor, carrier_mesh)" — appears at lines 282, 456, 615, 888.
- **Location:** `ARCHITECTURE.md:282,456,615,888`
- **Evidence:** `ls /home/user/dev-knowledge/deploy/carrier_*.py` → 6 files: `carrier_docs.py carrier_floor.py carrier_globalconfig.py carrier_mesh.py carrier_plugin.py carrier_precommit.py`; `grep -n "five carrier" /home/user/dev-knowledge/ARCHITECTURE.md` → 4 hits.
- **Verdict:** contradicted
- **Proposed fix:** Update all four "five carriers" occurrences in ARCHITECTURE.md to "six carriers"; add `carrier_docs` to the enumerated list at line 456; update line 888 summary which says "five in reality today".
- **Skeptic note:** `carrier_docs.py` was merged by batch-3 lane 280/315 at 22:36 on 2026-08-08, after the ARCHITECTURE.md `last_reviewed: 2026-08-08` stamp was set (~18:23). Evidence is unambiguous: six files, four stale "five" claims. Line 888 explicitly says "five in reality today" — written accurately at review time but now wrong. No ADR ratifies leaving a stale count.

**S3** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-08-04 (A2 violation, persisting 10 days)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git -C /home/user/dev-knowledge log --date=short --format='%cd' -- VISION.md | head -1` → `2026-08-04`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to on or after 2026-08-04.
- **Skeptic note:** Stamp (2026-07-25) predates the last commit (2026-08-04) by 10 days — an exact backward-dated A2 gate failure. Was 1 day wide in the 2026-08-02 digest; gap widened by the 2026-08-04 commit (batch-3 handoff bundle merge touching VISION.md). Persisting unfixed since 2026-07-31; no ADR covers leaving it backward-dated.

**S4** — ESSENTIALS.md `last_reviewed: 2026-07-30` predates last git commit 2026-08-04 (A2 violation, new)
- **Claim:** `protocols/ESSENTIALS.md` was reviewed end-to-end on 2026-07-30 (frontmatter stamp).
- **Location:** `protocols/ESSENTIALS.md:2`
- **Evidence:** `git -C /home/user/dev-knowledge log --date=short --format='%cd' -- protocols/ESSENTIALS.md | head -1` → `2026-08-04`
- **Verdict:** contradicted
- **Proposed fix:** Re-read ESSENTIALS.md end-to-end (especially line 123 — the /override claim is a known defect requiring correction), then bump `last_reviewed` to on or after 2026-08-04.
- **Skeptic note:** NEW finding this cycle. Stamp (2026-07-30) predates last commit (2026-08-04) by 5 days. The 2026-08-04 commit edited ESSENTIALS.md without re-reviewing it. Note that the S1 HIGH finding (stale /override instruction at line 123) is a direct consequence of this gap — a genuine re-read would have caught it and prompted correction.

### Low (1)

**S5** — ARCHITECTURE.md pre-commit gates paragraph omits `block-unanchored-push` (17th hook, live since 2026-08-03)
- **Claim:** The enumeration paragraph (lines 512–527) lists `block-ff-push` as the last pre-push hook; `block-unanchored-push` is completely absent from ARCHITECTURE.md.
- **Location:** `ARCHITECTURE.md:512`
- **Evidence:** `grep -n "block-unanchored" /home/user/dev-knowledge/ARCHITECTURE.md` → no output (completely absent); `grep -c "^- id:" /home/user/dev-knowledge/.pre-commit-config.yaml` → 17; `grep -n "block-unanchored" /home/user/dev-knowledge/.pre-commit-config.yaml` → present.
- **Verdict:** omitted
- **Proposed fix:** Add `block-unanchored-push` to ARCHITECTURE.md gates paragraph (after `block-ff-push`), including its ADR-85 HARD-leg role, fail-closed posture, and one-time activation note.
- **Skeptic note:** Hook has been live since 2026-08-03 (CLAUDE.md v2.51 documents it fully at §9); ARCHITECTURE.md was reviewed 2026-08-08 and missed it. Ch2 Organ map is silent too. LOW severity because CLAUDE.md §9 is the authoritative agent instruction source and documents it correctly; ARCHITECTURE.md is the structural reference whose gap does not mislead session agents. Still a real omission in the structural doc.

---

## Killed Findings

**K1** — "Commit 5631660c closes [#394] but SHA does not exist in this repo"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** `git cat-file -t 5631660c` returns NOT FOUND in this clone, but the done-when criteria for [#394] are confirmed met in current `fleet_analytics.py` code — V3 verified the implementation is present. The absent SHA could reflect a rebased/amended commit history or a shallow-clone boundary artifact. A missing SHA reference is poor hygiene but not a conformance failure when the semantic done-when is demonstrably fulfilled.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; within shallow-clone boundary):**
- Entry (a) 2026-08-09: batch-3 integration reporting SHAs, night manifest ref — all verified in git log ✓
- Entry (b) 2026-08-08: batch-3 integration merge SHAs (10 lane merges) — confirmed in `git log --oneline -40` ✓
- Entry (c) 2026-08-08: batch-3 lane reviews, ARCHITECTURE.md review reference ✓
- Entry (d) 2026-08-07/08: pre-batch housekeeping SHAs — all verified ✓
- 20+ SHA anchors checked across 10 entries; no significant unattributed merged work found ✓

**V2 (living-doc factual claims):**
- ARCHITECTURE.md `last_reviewed: 2026-08-08` — passes A2 gate (last commit also 2026-08-08) ✓
- CLAUDE.md `last_reviewed: 2026-08-08` — passes A2 gate ✓
- CONTRIBUTING.md `last_reviewed: 2026-08-08` — passes A2 gate ✓
- Pre-commit hook count 17 — matches `.pre-commit-config.yaml` and `ecosystem/doc-counts.md` ✓
- Audit check count 41 — matches `ALL_CHECKS` in `scripts/audit.py` and `ecosystem/doc-counts.md` ✓
- CONTRIBUTING.md §"Nightly outcome management" — correctly shows RETIRED state and `report-only-wall.yml` ✓
- VISION.md fleet count "nine git repos" — `ecosystem/registry.md` has exactly 9 rows ✓
- CLAUDE.md §9 ruff pin v0.15.5 — matches `.pre-commit-config.yaml` rev ✓
- `.claude/commands/` (5 files) — matches `.claude/generated/commands-repo.md` enumeration ✓
- ARCHITECTURE.md "six chapters" — six `##`-level chapter sections confirmed ✓
- `ecosystem/doc-counts.md` check counts (41 checks, 17 gates, 2721 tests) — all verified ✓

**V3 (BACKLOG closure semantic coherence, 2026-07-12 → 2026-08-09):**
- 16 of 17 recent closures verified semantically coherent ✓
- All batch-3 closures (lane 280/315, 316, 317, 318, etc.) verified: done-when criteria met ✓

---

## Next Actions (proposals for operator)

1. **S1 (HIGH)** — Update `protocols/ESSENTIALS.md` line 123: replace the `/override [reason]` escape instruction with the correct ADR-85 amendment §A2 language (`git push --no-verify` is the sole escape; Stop hook advisory in full). This is the same correction CLAUDE.md v2.51 made on 2026-08-03 but did not propagate to ESSENTIALS.md. Then re-read ESSENTIALS.md end-to-end and bump `last_reviewed` (fixes S4 simultaneously).

2. **S2 (MED)** — Update all four "five carriers" occurrences in ARCHITECTURE.md (lines 282, 456, 615, 888) to "six carriers" and add `carrier_docs` to the enumerated list. Also add `block-unanchored-push` to the gates paragraph and organ map (fixes S5 simultaneously).

3. **S3 (MED, persisting 10 days)** — Re-read VISION.md end-to-end and bump `last_reviewed` to on or after 2026-08-04. The A2 canonical_freshness gate has been failing at every audit run since 2026-07-31.

4. **S4 (MED)** — After fixing S1 (which requires re-reading ESSENTIALS.md), bump ESSENTIALS.md `last_reviewed` to on or after 2026-08-04. Covered by S1's fix action.

5. **S5 (LOW)** — Add `block-unanchored-push` to ARCHITECTURE.md gates paragraph and Ch2 organ map. Covered by S2's fix action.

6. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (session-end backpressure fires as advisory noise; pre-commit hooks may be affected). Blocks from prior digests.

7. **(OUT OF SCOPE — needs manual verify)** Prior digest noted JOURNAL.md entry (t) broken SHA anchor `ee76c412` had scrolled beyond the 10-entry review window. V1 did not re-verify this cycle either. Operator should check JOURNAL.md entry (t) (~line 257) manually.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-09-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
