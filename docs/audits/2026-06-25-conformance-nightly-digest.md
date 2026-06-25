<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-25

**Date:** 2026-06-25
**Author:** Claude Code (claude-sonnet-4-6), native Dynamic Workflow
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** NATIVE DYNAMIC WORKFLOW (`.claude/workflows/conformance-hub.js` via the Workflow tool — **re-probe result: ENABLED as of 2026-06-25**. This is the first successful native run; all prior nights used the spec-orchestration fallback.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-4-6 |

All 5 stages ran via the native Workflow harness (Run ID: wf_31411cc6-cca). 5 agents · 303,973 tokens · 307 tool calls · 18m 17s wall-clock. **Platform note: the native Workflow launcher is NOW enabled in cloud — this resolves the long-standing spec-orchestration fallback condition reported on every prior nightly run since 2026-06-04.**

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 high (S1: CLAUDE.md §8 stale repo-level skills claim)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | V2 checked-clean confirms `.claude/skills/` now holds `verify` + `check-against-spec`. The claim that was persisting for 4+ consecutive nights (since 2026-06-11) is no longer present. Operator fixed the doc between 2026-06-14 and now. |
| **NEW** | HIGH: CONTRIBUTING.md:130-135 'squash-merged automatically' contradicts live workflow | V2 found this; adversarial skeptic confirmed it is real (unambiguous code evidence at workflow lines 184-234 + governing ADR-84/Q9). |

**Delta counts:** 1 resolved · 0 persisting · 1 new
**Skeptic kill-rate:** 50% (1 of 2 raw findings killed)

---

## Summary

Documentation health is strong overall. The verifier suite swept 10 JOURNAL merge-commit SHAs, 26+ leaf-commit SHAs, all 23 audit checks, 818 pytest-collected tests, 10 pre-commit gates, and 7 closed BACKLOG items — every claim checked out clean. The prior 4-night persisting finding (CLAUDE.md §8 stale skills claim) is **resolved** this run: V2 confirmed `.claude/skills/` holds `verify` + `check-against-spec` and CLAUDE.md §8 now documents this correctly.

The adversarial skeptic killed 1 of 2 raw findings (50% kill rate): the JOURNAL omission for #200 (commit 69f9f5c landed two minutes after the journal wrap was authored) is a temporal artifact of commit ordering within the branch, not a documentation integrity failure — correctly killed as `true-but-irrelevant`.

One new high-severity finding survives: **CONTRIBUTING.md lines 130-135 describe the nightly-conformance Action as 'squash-merged automatically'**, but the live `.github/workflows/nightly-conformance-triage.yml` does the opposite — it diverts the digest onto `automation/conformance-digest` via commit-tree plumbing and **closes** the PR without merging to main (ADR-84/Q9 change). ARCHITECTURE.md already uses the correct language; CONTRIBUTING.md was not updated when ADR-84 changed the behavior.

**Platform note:** This is the first nightly run to use the native Dynamic Workflow launcher. All prior digests (2026-06-04 through 2026-06-14) used the spec-orchestration fallback. The native path is now confirmed available in cloud.

---

## Findings (PROPOSALS ONLY)

**Raw:** 2 · **Survived skeptic:** 1 · **Killed false positives:** 1

<!-- counts: raw=2 survived=1 killed=1 -->

### High (1)

**S1** — CONTRIBUTING.md:130-135 stale 'squash-merged automatically' description *(NEW this run)*

- **Claim:** CONTRIBUTING.md lines 130-135 describe the nightly-conformance Action as performing a squash-merge automatically for both clean nights (survived=0) and findings nights (survived>0), and deleting its branch.
- **Location:** `CONTRIBUTING.md:130-135` (also line 140: "the Action merges only when")
- **Evidence:** `grep -n 'squash' /home/user/dev-knowledge/CONTRIBUTING.md && head -30 /home/user/dev-knowledge/.github/workflows/nightly-conformance-triage.yml`
- **Verdict:** contradicted
- **Proposed fix:** Replace the 'squash-merged automatically' description in CONTRIBUTING.md lines 130-135 with language matching ADR-84/Q9: the digest is diverted onto `automation/conformance-digest` via commit-tree plumbing and the PR is closed without merging to main. Also update line 140 ('the Action merges only when') to reflect the divert-and-close pattern.
- **Skeptic note:** The workflow code at lines 184-234 is unambiguous: comment on line 188 reads 'the inverse of the former squash-merge'; `gh pr close --delete-branch` executes at line 227 without a merge step. ADR-84 explicitly mandates isolation from main. ARCHITECTURE.md Ch3 and Ch6 already use the correct language ('diverts', 'closes the PR (does not merge)'). CONTRIBUTING.md is contradicted by both the live workflow and the governing ADR.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — JOURNAL.md:98 — #200 Changes line omits commit 69f9f5c
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** Confirmed via git timestamps: the journal wrap commit (05c8584) was authored at 12:17:10 and commit 69f9f5c was authored at 12:19:11 — two minutes after the journal was written, and 11 minutes before the merge (4a0e6d1 at 12:30:06). The Changes line was accurate when written; the omission is a temporal artifact of the commit ordering within the branch, not a documentation integrity failure. The work is correctly captured in git history. `git log --ancestry-path e288435..4a0e6d1 --oneline` confirms the commit is present in the arc.

---

## Checked-and-Clean (informative — absence of findings means these were verified correct)

**V1 (JOURNAL → git, last 10 entries):**
- All 10 JOURNAL entry merge-commit SHAs (afb7421, 8f5694b, 57dd61a, de5b0f3, 30408f6, 4a0e6d1, 4108be3, ab8a5a8, cf2d858, fe3fa03) confirmed present in git log
- All 26+ leaf-commit SHAs named in Changes lines verified (3061535, c48e46b, b017256, d95a580, 8fcf716, a7d77d2, 2080f52, b39b552, 002f90e, 90e3134, 9ad3dd5, 5e1db96, de06d64, 51cda73, e4af3a0, 56b26a8, 437b961, e288435, e57be90, 4e40517, fa10a13, 629d755, 8a695b9, b9790d5, 5c83555, 9ceaa3b)
- C5 commit fa10a13 touches exactly the two files claimed (HANDOFF_PROCESS.md, scripts/audit.py)
- #194 fixture directory tests/fixtures/doc-code-structural/ created by b9790d5 and exists on disk
- ecosystem/doc-code-edge.yaml updated in the #194 close commit 8acf23e
- #194 and #200 both removed from BACKLOG.md as claimed
- .gitignore contains logs/coherence-nudge.log as claimed by C5 follow-on entry
- A3/C3 commit de06d64 modifies HANDOFF_BOOT.md, HANDOFF_PROCESS.md, and tests/test_handoff_modes.py
- A4 commits (b017256/d95a580/8fcf716/a7d77d2/2080f52) all touch protocols/HANDOFF_BOOT.md only
- A2 commit 002f90e amends ADR-81 as claimed
- pytest count chain 809 (heading-convention) → 815 (#194) → 818 (#200) internally consistent
- Local main 176 commits ahead of origin/main — not-pushed claims accurate
- a1-prose branches and handoff-c4-condense-finding branch absent from git branch (deleted after merge)
- BACKLOG advances for #145, #144, #164 in dedicated commits b39b552, 5e1db96, c48e46b
- Integration session (2026-06-24) merge hashes fe5b790 and c407038 both confirmed in git log
- ARCHITECTURE.md restamp commit 7dca06d (last_reviewed 2026-06-24) + merge e5a3cbb confirmed
- Heading-convention arc: e11a971, a21108a, 440548d, 6e92adb all confirmed in git log
- No significant merged work in recent git history unmentioned in the last 10 JOURNAL entries

**V2 (living-doc factual claims):**
- ARCHITECTURE.md: 23 registered audit checks verified (`python scripts/audit.py checks`)
- ARCHITECTURE.md: 818 tests collected verified (`python -m pytest --collect-only -q`)
- ARCHITECTURE.md and CLAUDE.md: 10 pre-commit gates verified against .pre-commit-config.yaml
- ARCHITECTURE.md: pre-commit hook roster (normalize-dated-headers, codemap-freshness, toc-freshness, toc-freshness-playbook, validate-backlog, audit-health, ruff, coherence-nudge, backlog-id-on-close, block-ff-push) verified
- ARCHITECTURE.md: Two codemap nodes (scripts/codemap/, scripts/toc/) verified
- ARCHITECTURE.md: audit.py commands (checks, health, registry, repo, run, ship-gate) verified
- ARCHITECTURE.md: doc-code-edge.yaml lives on 5 DONE rules (#194 Arc-1 cohort-1) verified
- ARCHITECTURE.md: ecosystem/doc-code-edge.yaml, ecosystem/disposition-register.yaml, docs/audits/2026-06-07-methodology-transfer-audit.md all exist
- ARCHITECTURE.md: coherence-nudge fires only on protocols/HANDOFF_PROCESS.md verified
- ARCHITECTURE.md: ruff gate version-pinned >=0.15.5 verified in .pre-commit-config.yaml and pyproject.toml
- ARCHITECTURE.md: all session/runtime scripts exist (block_ff_push.py, session_end_backpressure.py, fleet_health.py, surface_triage.ps1, billing_leak_sentinel.ps1, changelog_sentinel.py, scripts/hooks/block_immutable_edits.py)
- ARCHITECTURE.md: .claude/workflows/conformance-hub.js exists
- ARCHITECTURE.md: _commit_routine_outputs function in audit.py uses 'automation/fleet-audit' branch
- ARCHITECTURE.md: Pyright vendored via npm, pinned in package.json (pyright: 1.1.410), node_modules/ gitignored
- ARCHITECTURE.md: state.yaml gitignored as ecosystem/*/state.yaml; logs/PROPOSALS-*.md gitignored
- ARCHITECTURE.md: all referenced test files exist (test_legibility_graph_conformance.py, test_coherence_integration.py, test_validate_reconciliation.py, test_doc_code_edge.py, test_scan_undeclared_edges.py, test_reverse_dep_oracle.py)
- ARCHITECTURE.md: scan_undeclared_edges.py and reverse_dep_oracle.py not in ALL_CHECKS (verified)
- ARCHITECTURE.md: reverse_dep_oracle.py CLI has --json and --text flags
- ARCHITECTURE.md: nightly-outcome-loop table correctly describes divert+close / divert+issue
- ARCHITECTURE.md: ecosystem/conformance.md description consistent with ADR-86 (deferred to #171)
- CLAUDE.md §8: .claude/skills/ holds verify + check-against-spec (verified)
- CLAUDE.md §7: save.md, handoff.md, changelog-review.md, override.md in .claude/commands/
- CLAUDE.md §9: tier1-lifecycle plugin enabled in .claude/settings.json
- CONTRIBUTING.md: HANDOFF_PROCESS.md version is v5.2
- CONTRIBUTING.md: pre-commit hook table lists all 10 hooks matching .pre-commit-config.yaml
- CONTRIBUTING.md: .claude/workflows/conformance-hub.js is the nightly run definition file
- VISION.md: audit.py has health/repo/run/registry commands
- ARCHITECTURE.md: plugins/tier1-lifecycle/commands/ contains review-closures.md and ship.md

**V3 (backlog-closure semantic coherence):**
- #200 merge-serialization gate — tests/test_merge_serialization.py + PLAYBOOK §8 + commits 4e40517/4a0e6d1; done-when met
- #194 doc-code L1 structural-integrity — scan_structural_integrity + build_edge_index in 5c83555/9ceaa3b, closed 8acf23e; done-when met
- #10 TOKEN-LOG alignment — both legs met in PLAYBOOK §Token-log-cadence (line 2740) and commit 7286707
- #47 corp repo status — all three repos absent from ecosystem/index.yaml (grep confirmed)
- #88 graphify evaluation — reject ruling in JOURNAL line 2608 + commit 5f327b2
- #78 docs-refresh pass — ARCHITECTURE.md + CLAUDE.md last_reviewed bumped to 2026-06-04 in d5753a8
- #79 codemap grounding — grounding audit + ADR-71 end-state note in 052e311/fb24810

---

## Next Actions (proposals for operator)

1. **S1 (high, new)** — Update CONTRIBUTING.md lines 130-135 (and line 140): replace 'squash-merged automatically' / 'its branch deleted' / 'the Action merges only when' with the ADR-84/Q9 divert-and-close language. ARCHITECTURE.md already has the correct description; CONTRIBUTING.md was not updated when the behavior changed. Evidence: `grep -n 'squash' CONTRIBUTING.md && head -30 .github/workflows/nightly-conformance-triage.yml`

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-06-25-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. **CLEAN — no safety breach.**

---

*Generated by native Dynamic Workflow (conformance-hub.js). Run ID: wf_31411cc6-cca. Proposals only — operator approval required before any fix is applied.*
