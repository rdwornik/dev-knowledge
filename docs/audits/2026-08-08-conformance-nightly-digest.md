<!-- scope: meta -->
# Nightly Conformance Digest — 2026-08-08

**Date:** 2026-08-08
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-08-08; confirmed unavailable, consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent + in-context reconciliation) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs. The V1 Explore subagent ran for 12 minutes and completed after the skeptic subagent was already launched; V1's one finding was assessed via in-context adversarial review and merged into the skeptic result.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-08-02-conformance-nightly-digest.md`
**Gap:** 6 days (2026-08-02 → 2026-08-08; no conformance digest ran 2026-08-03 through 2026-08-07)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | prior S1 (MED): CONTRIBUTING.md "Nightly outcome management" describes deleted GitHub Action as live | Fixed by commit 59b191c (2026-08-06, [#503]). Section now correctly describes the retirement in past tense ("RETIRED 2026-07-08"). `.github/` directory returned 2026-08-06 with unrelated `report-only-wall.yml` organ; CONTRIBUTING.md accurately documents this. |
| **PERSISTING (severity held)** | prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit | Now 9-day gap (last commit 2026-08-03 via merge bcfe3cf6). Still MED. Today's S1. |
| **NEW** | ESSENTIALS.md `last_reviewed: 2026-07-30` predates last commit 2026-08-03 | Same merge (bcfe3cf6) touched ESSENTIALS.md without re-stamping. Was previously forward-dated (killed K3 in 2026-08-02 digest). Now backward-dated. Today's S2. |

**Delta counts:** 1 resolved · 1 persisting · 1 new
**Raw → survived → killed:** 5 → 2 → 3
**Skeptic kill-rate:** 60% (3 of 5 raw findings killed)

---

## Summary

Overall doc health continues to improve: the longest-standing finding (CONTRIBUTING.md stale GitHub Action description, flagged every digest since 2026-07-31) was resolved by commit 59b191c as part of the [#503] currency-correction arc. The `.github/` directory returned 2026-08-06 carrying the report-only wall, which CONTRIBUTING.md now accurately documents. No high-severity findings survived the skeptic.

Two medium-severity freshness-stamp violations persist. VISION.md's `last_reviewed: 2026-07-25` stamp predates its last commit (2026-08-03, merge bcfe3cf6) by 9 days — a backward-dated A2 canonical_freshness gate failure persisting since 2026-07-31. A new companion finding: `protocols/ESSENTIALS.md`'s `last_reviewed: 2026-07-30` stamp also predates its last commit (same merge, 2026-08-03) by 4 days. Both files were touched by the same `docs/480-terra-tally-evidence` merge without triggering a freshness re-stamp.

The 60% kill-rate reflects appropriate filtering: the "38 checks" claim from the prior digest's checked-clean was not re-raised against any live doc (doc-counts.md correctly shows 41); a V3 scope-gap in the [#481] closure was killed as a documented decision (commit message provides explicit Pyright-based justification); and a V1 ratchet-narrative discrepancy was killed as evidence-not-definitive (the "441 → 432" notation may follow a baseline-ceiling convention rather than prior-count notation).

The systemic uv infrastructure issue (cloud runtime 0.8.17 vs required 0.11.19) continues to block all session-end governance gates; noted as infrastructure context, not a doc-conformance finding.

<!-- counts: raw=5 survived=2 killed=3 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 5 · **Survived skeptic:** 2 · **Killed false positives:** 3

### High (0)

*(No high-severity findings survived the skeptic.)*

### Med (2)

**S1** — VISION.md `last_reviewed: 2026-07-25` predates last git commit 2026-08-03 (A2 violation, persisting)
- **Claim:** VISION.md was reviewed end-to-end on 2026-07-25 (frontmatter stamp).
- **Location:** `VISION.md:4`
- **Evidence:** `git -C /home/user/dev-knowledge log --format='%H %ai %s' -1 -- VISION.md` → `bcfe3cf6 2026-08-03 Merge branch 'docs/480-terra-tally-evidence'`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to on or after 2026-08-03. The A2 canonical_freshness gate fires at every audit run.
- **Skeptic note:** Stamp (2026-07-25) is 9 days before last commit (2026-08-03). VISION.md is in `DEFAULT_FRESHNESS_FILES` (canonical_freshness_gate.py:32). No ADR or documented decision covers leaving this backward-dated. Persisting unfixed since 2026-07-31 (7+ days).

**S2** — `protocols/ESSENTIALS.md` `last_reviewed: 2026-07-30` predates last git commit 2026-08-03 (A2 violation, NEW)
- **Claim:** ESSENTIALS.md was reviewed end-to-end on 2026-07-30 (frontmatter stamp).
- **Location:** `protocols/ESSENTIALS.md:2`
- **Evidence:** `git -C /home/user/dev-knowledge log --format='%H %ai %s' -1 -- protocols/ESSENTIALS.md` → `bcfe3cf6 2026-08-03 Merge branch 'docs/480-terra-tally-evidence'`
- **Verdict:** contradicted
- **Proposed fix:** Re-read ESSENTIALS.md end-to-end and bump `last_reviewed` to on or after 2026-08-03.
- **Skeptic note:** Stamp (2026-07-30) is 4 days before last commit (2026-08-03). `protocols/ESSENTIALS.md` is explicitly named in `DEFAULT_FRESHNESS_FILES` (canonical_freshness_gate.py:33). Same merge touched both VISION.md and ESSENTIALS.md without re-stamping either. Prior digest (2026-08-02) killed the ESSENTIALS.md finding as "forward-dated" (K3: stamp 2026-07-30 was later than then-last-commit 2026-07-29). The bcfe3cf6 merge on 2026-08-03 converted it to a backward-dated violation.

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — "ARCHITECTURE.md or some living doc claims exactly 38 audit checks"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** No live doc currently claims 38. ARCHITECTURE.md defers to `ecosystem/doc-counts.md` (line 319: "count in ecosystem/doc-counts.md"), which correctly states "41 registered checks". `ALL_CHECKS` in `scripts/audit.py:4183` has 41 active (non-commented) entries. The "38" figure appeared in the 2026-08-02 digest's checked_clean as a then-accurate count; three new checks were added since (check_journal_spine_anchor, check_preflight_backlog_ids, check_review_artifact_coverage). No live doc makes a false claim; nothing to fix.

**K2** — "[#481] closure diff leaves carrier_mesh.py constants and .claude/methodology-roster.md untouched despite backlog row body listing them as in-scope"
- **Kill reason:** `documented-decision`
- **Kill detail:** The closing commit (e564733e) explicitly addresses the non-movement: Pyright reverse-dependency analysis showed all 7+11 referencers of OrganProbe/Cell are inside `scripts/enforcement_coverage.py` only, and `carrier_mesh.py` references the SCRIPT NAME rather than the renamed organ id. This reasoning is disclosed in the commit message, not silently omitted. The commit does not invoke the done-when's second alternative explicitly, but the justification is the same in substance. No ADR needed — the commit message is the documented reasoning. The `_ORGAN_TO_COMPONENT` honest-limit is recorded as well.

**K3** — "JOURNAL.md entry (k) claims 'silent_rule_ratchet 441 → 432 (net drain, not growth)' but live count went from 431 to 432"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The "441 → 432" notation is ambiguous: it may follow a repo convention of expressing "baseline_ceiling → current_live_count" (the same notation appears in entry (j): "441 → 431"), not "prior_session_count → current_count". Under that reading, the notation is accurate (ceiling: 441, current use: 432). The "net drain, not growth" claim is less ambiguous — within this arc the count did increase by 1 (+1 from 431 to 432, driven by a YAML comment token). However, the ship-gate remained GREEN (432 ≤ 441 baseline), the JOURNAL is a tactical log not a gated conformance surface, and F6 itself added zero normative keywords (the +1 was in a YAML comment in `ecosystem/disposition-register.yaml`). The evidence_command does not definitively prove narrative intent error given the notation ambiguity.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; all 2026-08-07 entries (a)–(l), all within available history boundary 2026-08-03+):**
- Entry (l): anchor SHAs e351b685, 8132f369, 8c438220 verified — merge is --no-ff (two parents) ✓
- Entry (j): SHAs 0c70d98b, 3a0b7e84, 77b75dd7, df12d2e8, 2467e929 all present and match descriptions ✓
- Entry (j): HANDOFF_PROCESS 6.0.1 → 6.1.0 confirmed in commit 77b75dd ✓
- Entry (i): all seven cited SHAs (e03df5c4, c4d6db25, 6ae62c64, 69ddcb80, e0a07c30, ede671bb, 35868b3c) present ✓
- Entry (i): templates/prompt-template.md v1.10 confirmed in e03df5c4 ✓
- Entry (h): a96040c3 ([#490][#429][#320] closed on evidence) and 63b7b6a9 verified ✓
- Entry (h): all four lane merges (ea4ddf23, e685a306, 47bd4f52, ad9332c3) confirmed ✓
- Entry (g): 0094b09a (STANDING_RULINGS B7 VISIBLE=DISPATCHED) and 7030f851 (point-of-use) verified ✓
- Entry (f): 1f41d7d5 present; docs/audits/2026-08-07-technical-fleet-backup-posture.md exists ✓
- Entry (e): e62c412a and d961bc12 (PRE-2 self-review fixes) verified ✓
- Entry (d): 8bb06e00 (mutmut sandbox fix) verified ✓
- Entry (c): a17d791f (R-1), 876cc463 (batch-2 manifest), and all other cited SHAs verified ✓
- No significant merged work found in git log that the 10-entry window omits ✓

**V2 (living-doc factual claims):**
- CLAUDE.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- ARCHITECTURE.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- CONTRIBUTING.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- ARCHITECTURE.md "five carriers" — exactly 5 carrier_*.py files in deploy/ ✓
- CLAUDE.md §9 ruff pin v0.15.5 — matches .pre-commit-config.yaml exactly ✓
- VISION.md fleet count "nine git repos" — ecosystem/registry.md has exactly 9 data rows ✓
- Pre-commit hook count 17 — matches .pre-commit-config.yaml (17 `id:` entries) and CLAUDE.md §9 list (17 named hooks) ✓
- ecosystem/doc-counts.md audit check count 41 — matches ALL_CHECKS active entries in audit.py ✓
- All 8 commands in .claude/generated/commands-repo.md have corresponding .md files in .claude/commands/ ✓
- All 5 recent ADRs in .claude/generated/recent-adrs.md (ADR-106 through ADR-110) exist in docs/decisions/ ✓
- tier1-lifecycle plugin enabled in .claude/settings.json ✓

**V3 (BACKLOG closure semantic coherence, post-2026-08-02):**
- [#472] closed 0cf327e 2026-08-03: machine-locatable anchor appended to ADR-104; check_membership_agreement gains declaration-agreement leg. Done-when fully met ✓
- [#465] closed 397534c 2026-08-04: handoff_tag_canonicity RETIRED; detect_unconditionally_inert_checks self-enumerates. Done-when met ✓
- [#482] closed 2026-08-04 (anchors a2d31508, a8f7a3ee): glob engine switched to true-glob semantics; tests pin governed set live. Done-when fully met ✓
- [#503] closed 1447d06 2026-08-06: all 8 currency sites corrected (CONTRIBUTING.md ×6, DEFINITION_OF_DONE.md, .claude/commands/override.md); DoD gating gap closed. Done-when fully met ✓
- [#504] closed 1447d06 2026-08-06: block_ff_push.py:39 states fail-closed posture; ARCHITECTURE.md:341 states fail-CLOSED; terra artifact exists. Done-when fully met ✓
- [#501] closed 4ad76bc/93b2fa3 2026-08-07: all four done-when clauses met (runs-on-push, records retrievably, judges nothing, ARCHITECTURE rows). Done-when met ✓
- [#490] closed a96040c 2026-08-07: parity-surfaces 9/9 achieved; 4 unonboarded with declared reasons (second limb of OR). Done-when met ✓
- [#429] closed a96040c 2026-08-07: worktree_import_proof.py runs as CLI; exercised live on ai-council. Done-when met ✓
- [#320] closed a96040c 2026-08-07: 3 named repos confirmed clean; 9-repo sweep documented. Done-when met ✓

---

## Next Actions (proposals for operator)

1. **S1 (MED, 7+ days)** — Re-read VISION.md end-to-end and bump `last_reviewed` from 2026-07-25 to on or after 2026-08-03. The A2 canonical_freshness gate fires at every audit run.

2. **S2 (MED, NEW)** — Re-read `protocols/ESSENTIALS.md` end-to-end and bump `last_reviewed` from 2026-07-30 to on or after 2026-08-03. The same merge (bcfe3cf6) that touched VISION.md also touched ESSENTIALS.md without re-stamping.

3. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (session-end backpressure fails with version mismatch on every turn). Blocks from prior digests.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
 M docs/audits/README.md
?? docs/audits/2026-08-08-conformance-nightly-digest.md
```

Expected: one untracked file (this digest) + `docs/audits/README.md` modified (audit index regenerated via `gen_audit_index.py --write` to include this digest). No other tracked files changed. ✓ Safety check passes.
