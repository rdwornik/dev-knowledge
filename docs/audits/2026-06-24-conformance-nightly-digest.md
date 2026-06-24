<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-24

**Date:** 2026-06-24
**Author:** Claude Code (claude-sonnet-4-6), native Workflow launcher
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** NATIVE WORKFLOW LAUNCHER — **first successful native run** (all prior nightly runs used the spec-orchestration fallback; the native Workflow launcher was confirmed unavailable as of 2026-06-14). Platform re-probe as of 2026-06-24: native launcher is NOW ENABLED in this cloud runtime.

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (session model, inherited by workflow agents). 5 agents, 435 tool calls, ~405k tokens.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high, persisting 4 consecutive nights — CLAUDE.md §8 stale skills claim)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high, 4 nights): CLAUDE.md §8 "no repo-level skills directory exists yet" | Fixed in commit 930631d (2026-06-23 corpus-drift cleanup). V2 now confirms `.claude/skills/verify` and `.claude/skills/check-against-spec` both exist and CLAUDE.md §8 accurately describes them. |
| **NEW** | S1 (high): CONTRIBUTING.md:130-132 "squash-merged automatically" language | CONTRIBUTING.md still uses pre-ADR-84 squash-merge language; live workflow and ARCHITECTURE.md:412 already implement/describe the DIVERT+CLOSE model. |

**Delta counts:** 1 resolved · 0 persisting · 1 new
**Skeptic kill-rate:** 67% (2 of 3 raw findings killed)

---

## Summary

Documentation conformance is in strong health across the 40+ checked-clean items spanning JOURNAL fidelity, ARCHITECTURE claims, CLAUDE.md hook/command/skill rosters, CONTRIBUTING.md structural references, and BACKLOG closure coherence. The skeptic kill-rate was 67% (2 of 3 raw findings eliminated): one JOURNAL narrative-compression was correctly ruled a non-violation of append-only policy (the JOURNAL is a human narrative, not a machine-conformance surface), and one backlog-hygiene opinion was ruled against a non-existent enforced rule. One real finding survives at high severity: CONTRIBUTING.md lines 130-135 retain stale "squash-merged automatically" language that contradicts the ADR-84 Q9 DIVERT-and-CLOSE model already correctly described in ARCHITECTURE.md line 412 and explicitly inverted in the nightly workflow's own comments. The gap is machine-observable and survived a genuine re-read in June 2026, indicating it requires a targeted in-place correction to CONTRIBUTING.md.

The CLAUDE.md §8 skills claim that persisted for 4 consecutive nights (2026-06-11 through 2026-06-14) is now **RESOLVED** via commit 930631d.

**Platform note:** The native Workflow launcher is now enabled in this cloud runtime — all prior nightly runs (2026-06-10 through 2026-06-14) used the spec-orchestration fallback.

---

## Findings (PROPOSALS ONLY)

**Raw:** 3 · **Survived skeptic:** 1 · **Killed false positives:** 2

<!-- counts: raw=3 survived=1 killed=2 -->

### High (1)

**S1** — CONTRIBUTING.md stale nightly-outcome model *(NEW)*
- **Claim:** CONTRIBUTING.md lines 130-132 describe the nightly outcome as "squash-merged automatically" (clean night) and "digest is squash-merged too (it is the record)" (findings night), but the actual workflow implements ADR-84 Q9: DIVERT to `automation/conformance-digest` + CLOSE the PR without merging to main.
- **Location:** CONTRIBUTING.md:130-132
- **Evidence:** `grep -n 'squash.merge\|divert\|CLOSE\|conformance-digest' /home/user/dev-knowledge/.github/workflows/nightly-conformance-triage.yml | head -20`
- **Verdict:** contradicted
- **Proposed fix:** Replace CONTRIBUTING.md lines 130-135 "squash-merged" language with the ADR-84 Q9 model: on clean nights the branch is deleted without merging; on findings nights the digest is diverted to `automation/conformance-digest` and the PR is closed without merging to main. Cross-reference ARCHITECTURE.md:412 for the already-correct description.
- **Skeptic note:** The workflow comments at lines 7-9 and 187-188 explicitly call out the inversion of the "former squash-merge"; ARCHITECTURE.md line 412 already carries the correct description and notes this superseded squash-merge-to-main. ADR-84 adopted the branch-isolation policy. CONTRIBUTING.md is a living doc (not immutable) last re-read 2026-06-21 — the stale language survived that re-read.

### Med (0)

*(none)*

### Low (0)

*(none)*

---

## Killed Findings

**K1** — JOURNAL.md:110 "claim-3 reconciled 793→800" — actual git diff at d7c2aee shows 794→800, not 793→800
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The evidence command confirms d7c2aee shows 794→800. However, the JOURNAL entry narrates the overall reconciliation arc (spanning both 8c90eba at 793→794 and d7c2aee at 794→800) as a single session outcome description, not making a commit-level attribution claim. The JOURNAL is append-only (ADR-29/ADR-39) and is a human narrative document, not a machine-read conformance surface. No conformance protocol requires the JOURNAL to attribute each count increment to its exact commit. The inaccuracy is a narrative compression, not a protocol violation, and cannot be corrected in an append-only document regardless.

**K2** — PLAYBOOK heading-scheme restructure (fe5b790) and scan_heading_scheme enforcement (fe3fa03) shipped with no dedicated backlog closure, referenced only to #77
- **Kill reason:** `opinion`
- **Kill detail:** No documented rule requires every work arc to have its own dedicated backlog item. PLAYBOOK §1353 only requires "closes [#id]" on the commit that finishes a backlog item; "refs #id" to associate in-progress work is explicitly permitted and commonly used (the JOURNAL entry itself says "refs #77, advances not closes"). The developer made a conscious, recorded choice to advance #77 rather than open a new item. The validate-backlog pre-commit hook (ADR-66) validates schema, not work-to-item coverage. The finding is an opinion about ideal backlog hygiene, not a violation of any enforced conformance rule.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; shallow-clone boundary ~2026-06-03):**
- Entry 1 (heading-convention enablement): SHAs e11a971 (RED), a21108a (GREEN detector), 440548d (PLAYBOOK §14), 6e92adb (800→809 reconcile) all verified; +9 test functions confirmed; 809 collected in ARCHITECTURE.md confirmed
- Entry 2 (integration session): Merge SHAs fe5b790, c407038, e5a3cbb, 7dca06d all present with correct parents; JOURNAL conflict narrative consistent with git graph
- Entry 3 (PLAYBOOK batch-3): Commits c4a4060, 2397b56, merge c961e5a all verified; protocols/PLAYBOOK.md changed in both commits
- Entry 4 (ARCHITECTURE reconciled_with): Commit 6330c9c verified adding `reconciled_with: handoff-process@5.2` frontmatter; merge 2f461c2 verified
- Entry 5 (PLAYBOOK two-part heading scheme): Commit f8af23c verified with "37 insertions(+), 29 deletions(-)" — matches JOURNAL "37 +/29 −" exactly; 796 passed/4 skipped = 800 total consistent
- Entry 6 (corpus-drift cleanup): All commits verified — abec69e, 930631d, 8b6d6e5, 757ca86, a897e05; CLAUDE §11 ADR-88/89 ratification diff confirmed in 930631d
- Entry 7 (PLAYBOOK batch-2 tier-transition removal): Commits 41d1e19, merge 1e3ddf3 both verified
- Entry 8 (ARCHITECTURE fidelity audit): Report commit 778e9c2 creates correct audit file; merge b00f5a4 verified; "No ARCHITECTURE content edited" confirmed
- Entry 9 (PLAYBOOK currency batch-1): Three commits ba8bdfb, f5067e2, 1fc98f5 verified; merge a39e416 verified
- Entry 10 (PLAYBOOK fidelity audit): Report commit 855f748 creates correct audit file; merge c29ba3a verified; "No PLAYBOOK content edited" confirmed
- No significant git commits in window (5d10cfc..fe3fa03, 42 commits) absent from JOURNAL coverage
- All test count claims internally consistent: 796+4=800, 799+1=800, 800→809 (+9 heading-scheme tests) all verified

**V2 (living-doc factual claims):**
- ARCHITECTURE.md "pre-commit gates (10)": exactly 10 hook ids in .pre-commit-config.yaml confirmed
- ARCHITECTURE.md "23 registered checks": ALL_CHECKS list in scripts/audit.py lines 1642-1666 contains exactly 23 check functions confirmed
- ARCHITECTURE.md "Two nodes (scripts/codemap/ and scripts/toc/ both Python packages)": both __init__.py present confirmed
- ARCHITECTURE.md "live on 5 rules per ADR-89 OQ1 naming convention": ecosystem/doc-code-edge.yaml has exactly 5 coverage_scope entries confirmed
- CLAUDE.md §9 hook roster (all 10 hook IDs): all verified present in .pre-commit-config.yaml
- CLAUDE.md §9 SessionStart scripts (fleet_health.py, surface_triage.ps1, billing_leak_sentinel.ps1, changelog_sentinel.py): all 4 exist in scripts/ and wired in .claude/settings.json
- CLAUDE.md §9 Stop hook session_end_backpressure.py: file exists and wired
- CLAUDE.md §9 PreToolUse block_immutable_edits.py: file exists at scripts/hooks/ and wired
- CLAUDE.md §8 ".claude/skills/ holds verify + check-against-spec": both directories confirmed (the 4-night persisting finding is RESOLVED)
- CLAUDE.md §7 repo-level commands (save.md, handoff.md, changelog-review.md, override.md): all 4 exist in .claude/commands/
- CLAUDE.md §7 plugin commands (/review-closures, /ship): both exist in plugins/tier1-lifecycle/commands/
- CLAUDE.md §8 tier1-lifecycle plugin enabled: confirmed in .claude/settings.json enabledPlugins
- ARCHITECTURE.md "ruff check >=0.15.5": pyproject.toml [tool.ruff] required-version confirmed
- ARCHITECTURE.md child repos (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation): all 4 in ecosystem/
- CONTRIBUTING.md HANDOFF_PROCESS "v5 (stamp v5.2, stable)": protocols/HANDOFF_PROCESS.md header confirmed
- CONTRIBUTING.md "v4.4 archived at protocols/archive/HANDOFF_PROCESS_v4.4.md": file exists
- CONTRIBUTING.md "protocols/HANDOFF_BOOT.md": file exists
- CLAUDE.md §5 "Root README.md deleted 2026-05-23": confirmed absent
- ARCHITECTURE.md all named scripts/ and ecosystem/ files: all verified to exist
- CLAUDE.md §4 freshness-gated docs (VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS) and docs/handoffs/README.md: all 6 in scripts/audit.py _FRESHNESS_FILES
- VISION.md audit.py subcommands reference: verified
- ARCHITECTURE.md ".claude/workflows/conformance-hub.js": file exists
- ARCHITECTURE.md "check_doc_code_edge hub-only": confirmed no-op on non-hub repos
- ARCHITECTURE.md "pytest unit tests for validators (809 collected)": count set in commit 6e92adb (800→809); lower env count due to missing modules, not doc staleness
- ARCHITECTURE.md "docs/handoffs/README.md" canonical operator runbook: file exists
- protocols/DEFINITION_OF_DONE.md: file exists
- codex/AGENTS.md: file exists
- CONTRIBUTING.md ".github/workflows/nightly-conformance-triage.yml" diff guard: confirmed present
- ESSENTIALS.md "SESSION_SETUP.md" reference: file exists at protocols/SESSION_SETUP.md

**V3 (backlog-closure semantic coherence, recent closures):**
- #10 TOKEN-LOG path alignment: all done-when items met; BACKLOG entry removed
- #47 corp-knowledge-extractor/corp-by-os/corp-rfp-agent classification: all three classified via operator-approved absence-equals-classification ruling; BACKLOG entry removed
- #78 consolidated docs-refresh pass: ARCHITECTURE de-hardcoded, CLAUDE §11 rotated; genuine re-read with last_reviewed re-stamped; BACKLOG entry removed
- #79 codemap generator decision: no-build ruling recorded; ADR-71 end-state appended; BACKLOG entry closed and stub removed
- #88 graphify evaluation and rejection: pilot ran; REJECT ruling issued; BACKLOG entry removed
- #179 undeclared-edge scan: read-only scan with 18 tests green; BACKLOG entry removed
- #193 Pyright reverse-dep oracle: resolves Finding with full provenance; 21 tests green; BACKLOG entry removed
- #196 removal closure spike: GO verdict design doc landed; BACKLOG entry removed
- #197 ship-gate disposition: sha-scoped disposition landed; ship-gate GREEN; BACKLOG entry removed
- #199 refscan precision: live scan dropped from 245/104 to 12/4 actionable; 12 tests added; BACKLOG entry removed

---

## Next Actions (proposals for operator)

1. **S1 (high, new)** — Update CONTRIBUTING.md lines 130-135: replace "squash-merged automatically" (clean night) and "digest is squash-merged too (it is the record)" (findings night) with the ADR-84 Q9 model: on clean nights the branch is deleted without merging; on findings nights the digest is diverted to `automation/conformance-digest` and the PR is closed without merging to main. Cross-reference ARCHITECTURE.md:412 for the already-correct description. This is an in-place edit to a living doc and does not require a new ADR.

---

## Safety Tripwire

`git status --porcelain` output (run after review, before commit):

```
?? docs/audits/2026-06-24-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
