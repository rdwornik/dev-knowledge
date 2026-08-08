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
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs. The V1 Explore subagent ran for ~12 minutes and completed after the skeptic subagent was launched; V1's one finding was forwarded to the skeptic via message and assessed in the skeptic's final pass.

**Shallow-clone context (important for freshness findings):** `.git/shallow` lists `bcfe3cf6` as a boundary commit. `git log -1 -- <file>` returning `bcfe3cf6` (2026-08-03) for VISION.md and ESSENTIALS.md is a shallow-clone artifact — git cannot compare to that commit's parents (not in clone), so the "last touching commit" signal is unreliable. Freshness findings based on this commit date were killed as evidence-not-definitive. Operator should re-verify freshness findings from VISION.md and ESSENTIALS.md on a full-depth clone.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-08-02-conformance-nightly-digest.md`
**Gap:** 6 days (2026-08-02 → 2026-08-08; no conformance digest ran 2026-08-03 through 2026-08-07)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | prior S1 (MED): CONTRIBUTING.md "Nightly outcome management" describes deleted GitHub Action as live | Fixed by commit `59b191c` (2026-08-06, [#503]). Section now correctly describes the retirement in past tense ("RETIRED 2026-07-08"); `.github/` returned 2026-08-06 with unrelated organ, documented accurately. |
| **OUT OF SCOPE (shallow clone)** | prior S2 (MED): VISION.md `last_reviewed: 2026-07-25` predates last commit | `bcfe3cf6` is a shallow boundary — evidence not definitive in this clone. Prior digest's finding (confirmed 2026-07-26 > 2026-07-25 stamp on full history) remains the authoritative record. Operator should re-verify on full-depth clone. |
| **OUT OF SCOPE (shallow clone)** | ESSENTIALS.md `last_reviewed: 2026-07-30` — potential NEW finding | Same shallow-clone issue: `bcfe3cf6` parents not available, making the 2026-08-03 "last commit" date unreliable as evidence. |

**Delta counts:** 1 resolved · 2 out-of-scope (shallow clone) · 0 new
**Raw → survived → killed:** 5 → 0 → 5
**Skeptic kill-rate:** 100% (5 of 5 raw findings killed)

---

## Summary

All findings were killed by the adversarial skeptic. The most significant outcome is **resolution of the longest-standing finding**: CONTRIBUTING.md's "Nightly outcome management" section, which had described the retired GitHub Action in present tense since 2026-07-08, was corrected by commit `59b191c` (2026-08-06, [#503]). The `.github/` directory returned 2026-08-06 carrying the unrelated `report-only-wall.yml` organ, which CONTRIBUTING.md now accurately documents in past-tense historical context.

The 100% kill-rate is primarily driven by a **shallow-clone limitation** affecting freshness-stamp evidence: `.git/shallow` lists `bcfe3cf6` as a boundary commit, making `git log -1 -- VISION.md` and `git log -1 -- protocols/ESSENTIALS.md` return an unreliable "2026-08-03" date (the boundary commit's date rather than the actual last-edit date). Without the ability to compare to that commit's parents, freshness findings based on this date are not definitive from this clone. The prior digest (2026-08-02) confirmed VISION.md's freshness failure on full history (2026-07-26 > 2026-07-25 stamp); that confirmation stands, but this run cannot independently verify it.

Three other findings were killed: the "38 checks" stale figure (no live doc claims 38; doc-counts.md correctly states 41); the [#481] scope gap (documented-decision: commit message provides explicit Pyright reverse-dep justification); and the V1 ratchet-narrative finding (notation "441 → 432" follows the repo's established convention of baseline-ceiling → current-count, making "net drain" accurate).

V3 verified 9 closures since 2026-08-02 as semantically coherent. V1 verified all 12 JOURNAL entry (a)–(l) SHA anchors present and matching. The systemic uv infrastructure gap (cloud runtime 0.8.17 vs required 0.11.19) continues to block session-end governance gates.

<!-- counts: raw=5 survived=0 killed=5 -->

---

## Findings (PROPOSALS ONLY)

**Raw:** 5 · **Survived skeptic:** 0 · **Killed false positives:** 5

### High (0)

*(No high-severity findings survived the skeptic.)*

### Med (0)

*(No medium-severity findings survived the skeptic.)*

### Low (0)

*(No low-severity findings survived the skeptic.)*

---

## Killed Findings

**K1** — "VISION.md `last_reviewed: 2026-07-25` predates last commit 2026-08-03"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** `bcfe3cf6` (2026-08-03) is listed in `.git/shallow` as a shallow boundary commit. `git log -1 -- VISION.md` returns this commit not because VISION.md changed there, but because git cannot traverse further back. The commit's parents are not in the clone (`git diff bcfe3cf6^1 bcfe3cf6 -- VISION.md` fails: `fatal: bad revision 'bcfe3cf6^1'`). The file's last actual edit date is beyond the shallow boundary and is unknowable from this clone's evidence. The canonical_freshness_gate.py would produce the same false positive. Note: the 2026-08-02 digest confirmed this finding on full history (last edit 2026-07-26 > stamp 2026-07-25); operator should re-verify on a full-depth clone.

**K2** — "`protocols/ESSENTIALS.md` `last_reviewed: 2026-07-30` predates last commit 2026-08-03"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** Identical shallow-clone situation to K1. `bcfe3cf6` is the shallow boundary for both files; the 2026-08-03 date is a clone artifact. Cannot confirm the file was edited after its 2026-07-30 stamp from this clone's evidence.

**K3** — "ARCHITECTURE.md or some living doc claims exactly 38 audit checks"
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** No live doc currently claims 38. `ecosystem/doc-counts.md` correctly states "41 registered checks"; `ALL_CHECKS` in `scripts/audit.py:4183` has 41 active (non-commented) entries. The "38" figure appeared in the 2026-08-02 digest's checked_clean as a then-accurate count; three checks were added since. Nothing to fix.

**K4** — "[#481] closure diff leaves carrier_mesh.py constants and `.claude/methodology-roster.md` untouched despite backlog row body listing them as in-scope"
- **Kill reason:** `documented-decision`
- **Kill detail:** The task's done-when provides an explicit second alternative: "every keyed consumer moves in lockstep, with a test, OR the mismatch is recorded permanent-defer-with-reason." Commit `e564733e` invokes the second branch via a Pyright reverse-dep analysis (D1+D2+D3) proving carrier_mesh's constants key on the SCRIPT NAME (`scripts/session_end_backpressure.py`), not the renamed organ id — moving them would make the manifest lie about what the carrier deploys. The reasoning is explicit, structural, and self-consistent in the commit message.

**K5** — "JOURNAL entry (k): 'silent_rule_ratchet 441 → 432 (net drain, not growth)' — live count went 431 → 432 within the arc"
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** The "441 → 432" notation follows the repo's established convention of expressing "baseline_ceiling → current_live_count" (confirmed by multiple JOURNAL entries using the same format, e.g., entry (j): "441 → 431"). Under that convention, "net drain" means current (432) < baseline ceiling (441), which is accurate. The charge that the claim is factually wrong applies only under a non-standard reading of the notation. Additionally, "F6 added no normative keyword" is verifiably true — the +1 token was in a YAML comment in `ecosystem/disposition-register.yaml`, not in the F6 ruling itself.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; all 2026-08-07 entries (a)–(l), all within available history boundary):**
- Entry (l): anchor SHAs e351b685, 8132f369, 8c438220 verified — merge is --no-ff (two parents) ✓
- Entry (j): SHAs 0c70d98b, 3a0b7e84, 77b75dd7, df12d2e8, 2467e929 all present and match descriptions ✓
- Entry (j): HANDOFF_PROCESS 6.0.1 → 6.1.0 confirmed in commit 77b75dd ✓
- Entry (i): all seven cited SHAs (e03df5c4, c4d6db25, 6ae62c64, 69ddcb80, e0a07c30, ede671bb, 35868b3c) present ✓
- Entry (i): templates/prompt-template.md v1.10 confirmed in e03df5c4 ✓
- Entry (h): a96040c3 ([#490][#429][#320] closed) and 63b7b6a9 (self-correction) verified ✓
- Entry (h): all four lane merges (ea4ddf23, e685a306, 47bd4f52, ad9332c3) confirmed ✓
- Entry (g): 0094b09a (STANDING_RULINGS B7) and 7030f851 (point-of-use) verified ✓
- Entry (f): 1f41d7d5 present; docs/audits/2026-08-07-technical-fleet-backup-posture.md exists ✓
- Entry (e): e62c412a and d961bc12 (PRE-2 self-review fixes) verified ✓
- Entry (d): 8bb06e00 (mutmut sandbox fix) verified ✓
- Entry (c): a17d791f (R-1), 876cc463 (batch-2 manifest), all other cited SHAs verified ✓
- No significant merged work found in git log that the 10-entry window omits ✓

**V2 (living-doc factual claims):**
- CLAUDE.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- ARCHITECTURE.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- CONTRIBUTING.md last_reviewed 2026-08-07 passes A2 gate (last commit also 2026-08-07) ✓
- ARCHITECTURE.md "five carriers" — exactly 5 carrier_*.py files in deploy/ ✓
- CLAUDE.md §9 ruff pin v0.15.5 — matches .pre-commit-config.yaml exactly ✓
- VISION.md fleet count "nine git repos" — ecosystem/registry.md has exactly 9 data rows ✓
- Pre-commit hook count 17 — matches .pre-commit-config.yaml (17 `id:` entries) and CLAUDE.md §9 list ✓
- ecosystem/doc-counts.md audit check count 41 — matches ALL_CHECKS active entries in audit.py ✓
- All 8 commands in .claude/generated/commands-repo.md have corresponding .md files in .claude/commands/ ✓
- All 5 recent ADRs in .claude/generated/recent-adrs.md (ADR-106 through ADR-110) exist in docs/decisions/ ✓
- tier1-lifecycle plugin enabled in .claude/settings.json ✓

**V3 (BACKLOG closure semantic coherence, post-2026-08-02):**
- [#472] closed 0cf327e 2026-08-03: machine-locatable anchor in ADR-104; check_membership_agreement gains declaration leg. Done-when met ✓
- [#465] closed 397534c 2026-08-04: handoff_tag_canonicity RETIRED; inert-check self-enumeration working. Done-when met ✓
- [#482] closed 2026-08-04 (anchors a2d31508, a8f7a3ee): glob engine true-glob; tests pin live. Done-when met ✓
- [#503] closed 1447d06 2026-08-06: all 8 currency sites corrected; DoD gating gap closed. Done-when met ✓
- [#504] closed 1447d06 2026-08-06: block_ff_push fail-closed posture documented and tested. Done-when met ✓
- [#501] closed 4ad76bc/93b2fa3 2026-08-07: all four done-when clauses met. Done-when met ✓
- [#490] closed a96040c 2026-08-07: parity-surfaces 9/9; unonboarded with declared reasons. Done-when met ✓
- [#429] closed a96040c 2026-08-07: worktree_import_proof.py functional; exercised live. Done-when met ✓
- [#320] closed a96040c 2026-08-07: 9-repo sweep completed; audit record filed. Done-when met ✓

---

## Next Actions (proposals for operator)

1. **(SHALLOW-CLONE LIMITATION)** Verify VISION.md and ESSENTIALS.md freshness stamps on a full-depth clone. Prior digest (2026-08-02) confirmed VISION.md last edit 2026-07-26 > stamp 2026-07-25; that finding may still be valid but could not be confirmed from this shallow clone. Command to run on full clone: `git log --format='%cd' --date=short -1 -- VISION.md` and `git log --format='%cd' --date=short -1 -- protocols/ESSENTIALS.md`.

2. **(INFRASTRUCTURE, persisting)** Upgrade cloud runtime uv to `==0.11.19`. Every governance gate is currently non-functional (session-end backpressure fails with version mismatch on every turn). Blocks from prior digests.

---

## Safety Tripwire

`git status --porcelain` output at digest write time:

```
 M docs/audits/README.md
?? docs/audits/2026-08-08-conformance-nightly-digest.md
```

Expected: one untracked file (this digest) + `docs/audits/README.md` modified (audit index regenerated via `gen_audit_index.py --write`). No other tracked files changed. ✓ Safety check passes.
