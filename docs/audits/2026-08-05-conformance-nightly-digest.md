<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-05

**Date:** 2026-08-05
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-05; confirmed unavailable, consistent with all prior nightly runs.)

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

**Prior digest:** `docs/audits/2026-08-02-conformance-nightly-digest.md`
**Gap:** 3 days (2026-08-02 → 2026-08-05; no digests exist for 2026-08-03 or 2026-08-04)

| Status | Finding | Notes |
|---|---|---|
| **PERSISTING** | prior S1 (MED): CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live | Skeptic held at MED; ARCHITECTURE.md:788–790 correction still mitigates reader risk but CONTRIBUTING.md itself remains misleading. Now persisting 5+ days. Today's S1. |
| **PERSISTING (downgraded MED→LOW)** | prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit | Gap widened (2026-07-25 vs 2026-07-31, now 6-day gap vs 1-day gap in baseline) due to restore-as-is merge bd08f34. Skeptic downgraded to LOW: underlying content unchanged by restore. Today's S4. |
| **NEW** | — (MED): CONTRIBUTING.md pre-commit hook table omits two hooks | check-seal-identity ([#475]) and block-unanchored-push (ADR-85 amendment 2026-08-03) absent from CONTRIBUTING.md table; .pre-commit-config.yaml has 17 hooks, table lists 15. Today's S2. |
| **NEW** | — (MED): ARCHITECTURE.md Pre-commit gates paragraph missing block-unanchored-push | Added 2026-08-03, one day after ARCHITECTURE.md last_reviewed 2026-08-02; grep returns zero hits. Today's S3. |

**Delta counts:** 0 resolved · 2 persisting (1 downgraded) · 2 new
**Raw → survived → killed:** 6 → 4 → 2
**Skeptic kill-rate:** 33% (2 of 6 raw findings killed)

---

## Summary

Overall doc health has two new findings this cycle alongside two persisters. V1 found the last 10 JOURNAL entries (arcs b–k, 2026-08-04) completely coherent: all 22 SHA anchors verified, test-count progression (2259→2329 collected) matches doc-counts.md at each merge boundary, and ALL_CHECKS transitions (39→38 in arc b, 38→39 in arc k) are confirmed. V3 verified 12 new closures (#465, #472, #479, #455, #433, #474, #475, #476, #473, #481, #482, #483) as semantically coherent. The skeptic kill-rate dropped to 33% (vs 78% last run) because two genuine new conformance gaps survived: the ADR-85 amendment (2026-08-03) added block-unanchored-push to .pre-commit-config.yaml, but neither ARCHITECTURE.md nor CONTRIBUTING.md was updated to reflect it, and CONTRIBUTING.md also omits check-seal-identity ([#475]) which was wired before its last_reviewed date. Two findings were killed: the ESSENTIALS.md stamp gap (a no-edit restore-as-is merge, not a real review gap) and #458 (structurally unmeetable Done-when conjunct, consistent with K6 from the 2026-08-02 digest).

<!-- counts: raw=6 survived=4 killed=2 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 6 · **Survived skeptic:** 4 · **Killed false positives:** 2

### High (0)

*(No high-severity findings survived the skeptic.)*

### Med (3)

**S1** — CONTRIBUTING.md §"Nightly outcome management" describes deleted GitHub Action as live
- **Claim:** "The repo's first GitHub Action (.github/workflows/nightly-conformance-triage.yml) handles the morning so the operator touches only findings."
- **Location:** `CONTRIBUTING.md:135`
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null || echo 'DOES NOT EXIST'` → `DOES NOT EXIST`
- **Verdict:** contradicted
- **Proposed fix:** Replace CONTRIBUTING.md §"Nightly outcome management" (lines 132–136) with a tombstone note pointing readers to ARCHITECTURE.md Ch7 as the authoritative current description of nightly conformance flow.
- **Skeptic note:** .github/ directory is definitively absent (deleted at commit 82227f08, 2026-07-08). ARCHITECTURE.md:788–790 provides an explicit in-repo correction flagging CONTRIBUTING.md as stale, mitigating reader risk — holds at MED (not HIGH). Persisting unfixed since 2026-07-31.

**S2** — CONTRIBUTING.md pre-commit hook table omits check-seal-identity and block-unanchored-push
- **Claim:** CONTRIBUTING.md's "Pre-commit hooks" table (lines 104–118) is the complete roster, listing 15 hooks.
- **Location:** `CONTRIBUTING.md:100`
- **Evidence:** `grep '  - id:' /home/user/dev-knowledge/.pre-commit-config.yaml && grep 'check-seal-identity\|block-unanchored' /home/user/dev-knowledge/CONTRIBUTING.md` → 17 ids found in yaml; zero matches in CONTRIBUTING.md for either hook name
- **Verdict:** contradicted
- **Proposed fix:** Add rows for check-seal-identity ([#475]) and block-unanchored-push (ADR-85 amendment 2026-08-03) to the CONTRIBUTING.md hook table, with stage, description, and ADR citations matching the other rows.
- **Skeptic note:** Two enforcement-relevant hooks are simply absent from the documented roster; the table presents itself as complete and is the first reference any new contributor sees. Not style — both hooks are in .pre-commit-config.yaml. NEW this cycle.

**S3** — ARCHITECTURE.md Pre-commit gates paragraph missing block-unanchored-push
- **Claim:** ARCHITECTURE.md Ch2 Validators section enumerates the complete set of pre-commit hooks; block-unanchored-push is absent.
- **Location:** `ARCHITECTURE.md:488`
- **Evidence:** `grep -n 'unanchored' /home/user/dev-knowledge/ARCHITECTURE.md` → zero matches
- **Verdict:** contradicted
- **Proposed fix:** Add block-unanchored-push to the Pre-commit gates summary at ARCHITECTURE.md:488, citing the ADR-85 amendment dated 2026-08-03 as authority.
- **Skeptic note:** block-unanchored-push is entirely absent from ARCHITECTURE.md. Added 2026-08-03, one day after ARCHITECTURE.md last_reviewed (2026-08-02). CLAUDE.md §9 already documents it correctly — gap is ARCHITECTURE.md-specific. Ch2 Organ map also has no row for it. NEW this cycle.

### Low (1)

**S4** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-07-31 (A2 violation)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git log --format='%ad' --date=short -1 -- VISION.md` → `2026-07-31`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to a date on or after 2026-07-31.
- **Skeptic note:** git log confirms most recent commit is 2026-07-31 (restore-as-is merge bd08f34; file appears as new file mode 100644 with same blob SHA — no content change). canonical_freshness A2 check fires mechanically: stamp 2026-07-25 < commit 2026-07-31 (6-day gap). Downgraded MED→LOW from prior baseline: underlying content was unchanged by the restore, but a genuine review is still owed. Persisting unfixed since 2026-07-31.

---

## Killed Findings

**K1** — "protocols/ESSENTIALS.md frontmatter last_reviewed: 2026-07-30 predates last git commit 2026-07-31"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The 1-day gap is caused entirely by restore-as-is merge bd08f34 (ESSENTIALS.md appears as new file mode 100644 with same blob SHA — zero content change). The stamp 2026-07-30 accurately reflects the last genuine re-read documented at commit e0528cc ("genuine re-read + re-stamp", 2026-07-30). The canonical_freshness A2 check fires mechanically because it compares stamp to git commit date without regard to whether the commit introduced any content change. A gate that fires due to a no-edit restore is a mechanical false positive, not a review gap.

**K2** — "#458 Done-when requires 'the PLAYBOOK freshness stamp rides a genuine re-read', but closing commit explicitly states no re-read was performed"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** PLAYBOOK.md is definitively not in `_FRESHNESS_FILES` (audit.py enumerates 8 gated files — PLAYBOOK absent by design) and carries no last_reviewed frontmatter stamp. The freshness-stamp limb of the Done-when was structurally unmeetable as written: there is no stamp to ride and no gate that would enforce one. Commit 9039d2d's explicit acknowledgment is transparent non-performance of an unmeetable condition, not a closure defect. Consistent with K6 kill in 2026-08-02 digest.

---

## Checked-and-Clean (absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; arcs b–k, 2026-08-04, all within shallow-clone boundary):**
- All 22 SHA anchors across 10 entries verified against git log (entries b–k) ✓
- Entry (k) SHA anchors f15065cf, 7e8f1d98 — both verified ✓
- Entry (k) ALL_CHECKS 38→39 — doc-counts.md at HEAD shows 39 checks ✓
- Entry (k) Full suite 2324 passed — arithmetic verified (2329 collected - 2 baseline failures - 3 skipped) ✓
- Entry (j) SHA anchors a2d31508, a8f7a3ee — both verified ✓
- Entry (j) Full suite 2309 passed — arithmetic verified (2314 collected - 5) ✓
- Entry (i) SHA anchors 0c38bae9, e564733e — both verified ✓
- Entry (h) SHA anchor 558bd902 (handoff bundle) — verified ✓
- Entry (g) SHA anchor 43eced57 — verified; --stat confirms ADR-82/-88/-89 amendments ✓
- Entry (f) SHA anchors aad1a235, 4306a46a — both verified ✓
- Entry (e) SHA anchors 4f11a792, abf7c12a, 02d1351f — all verified ✓
- Entry (d) SHA anchor 4e70a0aa — verified ✓
- Entry (c) SHA anchor 6057bbba — verified; token-log delta confirmed ✓
- Entry (b) SHA anchors f020e0b9, 7ead2cd3, 4edbd7fe — all verified ✓
- Test count progression (2259→2280→2306→2308→2314→2329 collected) matches doc-counts.md at each merge boundary ✓
- ALL_CHECKS transitions (39→38 in arc b; 38→39 in arc k) confirmed by doc-counts.md snapshots ✓
- No significant unattributed merged work found in last 40 git commits ✓

**V2 (living-doc factual claims):**
- doc-counts.md "audit: 39 registered checks" — ALL_CHECKS in audit.py has exactly 39 active entries ✓
- doc-counts.md "pre-commit gates (17)" — .pre-commit-config.yaml has exactly 17 hook ids ✓
- ARCHITECTURE.md `last_reviewed: 2026-08-02` — passes A2 gate ✓
- ARCHITECTURE.md check-seal-identity named in Ch2 ✓
- CLAUDE.md §8 skills (verify + check-against-spec) — matches .claude/skills/ on disk ✓
- CLAUDE.md @-imported fragments both exist on disk ✓
- CONTRIBUTING.md `last_reviewed: 2026-07-31` — passes A2 gate (matches last commit) ✓
- scripts/block_unanchored_push.py — exists on disk ✓

**V3 (BACKLOG closure semantic coherence, since 2026-08-02):**
- 12 closures verified semantically coherent: #465, #472, #479, #455, #433, #474, #475, #476, #473, #481, #482, #483 ✓
- #483: enforcement ruling recorded, advisory-first check wired with discrimination tests ✓
- #482: true-glob engine swap with governed-set pin and mutation tests ✓
- #481: block_unanchored_push organ id renamed with invariant tests ✓
- #475: pre-commit seal-identity hook wired with 7 RED-first tests ✓

---

## Next Actions (proposals for operator)

1. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (session-end backpressure, pre-commit hooks fail with version mismatch). Blocks from prior digests.

2. **S2+S3 (MED, NEW)** — Update ARCHITECTURE.md Ch2 Pre-commit gates paragraph and CONTRIBUTING.md hook table to include block-unanchored-push (ADR-85 amendment 2026-08-03). Both documents lag by one day since the amendment landed. Low-effort, high-consistency fix.

3. **S2 (MED, NEW)** — Also add check-seal-identity ([#475]) to CONTRIBUTING.md hook table. It was wired before CONTRIBUTING.md's last_reviewed date (2026-07-31) — an inadvertent omission.

4. **S1 (MED, persisting)** — Update CONTRIBUTING.md §"Nightly outcome management": replace present-tense GitHub Action description with a tombstone pointer to ARCHITECTURE.md Ch7. Now persisting 5+ days; low-effort fix.

5. **S4 (LOW, persisting)** — Re-read VISION.md end-to-end and bump `last_reviewed` to on or after 2026-07-31. The A2 canonical_freshness gate fires at every audit run. Six-day backlog.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
?? docs/audits/2026-08-05-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. ✓ Safety check passes.
