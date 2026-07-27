<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-27

**Date:** 2026-07-27
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-07-27, confirmed unavailable. Consistent with all prior nightly runs.)

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
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 stale repo-level skills claim — "No repo-level skills directory exists yet")

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 stale skills claim | Current CLAUDE.md §8 correctly documents `.claude/skills/verify/` and `check-against-spec`. 4-night persisting finding is resolved. |
| **NEW** | CONTRIBUTING.md nightly action section describes deleted .github/ workflow as active | high severity |
| **NEW** | ARCHITECTURE.md "12 rules" claim for doc-code-edge coverage_scope | 13 entries actually present; med severity |

**Delta counts:** 1 resolved · 0 persisting · 2 new
**Skeptic kill-rate:** 71% (5 of 7 raw findings killed)

---

## Summary

Healthy documentation state overall, with the long-persisting §8 skills claim now resolved and one high-severity stale CONTRIBUTING.md section remaining from a prior architecture change. The skeptic killed 5 of 7 raw findings (71% kill-rate), with 4 kills attributable to ADR-85 journal anchor semantics being more permissive than the verifier assumed: `--no-ff` merges carrying branch-tip journal commits satisfy ADR-85 without requiring additional post-merge anchor commits, and 'Next' sections are not retroactively editable per ADR-29. The 5th kill (V3's #292 gate narrowness) was correctly killed as true-but-irrelevant since the closing commit fully discloses the gate's limitations and open tickets already carry the gap.

Two survivors remain: **(1)** CONTRIBUTING.md's "Nightly outcome management" section (lines 132-156) presents the deleted `.github/workflows/nightly-conformance-triage.yml` as active machinery — the directory was deleted 2026-07-08 and ARCHITECTURE.md itself warns readers at lines 708-710 not to follow this section; a CONTRIBUTING.md update is overdue. **(2)** ARCHITECTURE.md hardcodes "12 rules" in three places (lines 349, 432, 443) for the doc→code coverage_scope, but the actual `ecosystem/doc-code-edge.yaml` has 13 entries since `governance-backlog-story-id` was added by #286 without a corresponding count bump.

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 2 · **Killed false positives:** 5

<!-- counts: raw=7 survived=2 killed=5 -->

### High (1)

**S1** — CONTRIBUTING.md nightly action section describes deleted .github/ workflow as active

- **Claim:** CONTRIBUTING.md lines 132-156 present `.github/workflows/nightly-conformance-triage.yml` as an active organ ("The repo's first GitHub Action handles the morning so the operator touches only findings")
- **Location:** CONTRIBUTING.md:135
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null && echo EXISTS || echo 'NOT FOUND'`
- **Verdict:** contradicted
- **Proposed fix:** Rewrite CONTRIBUTING.md lines 132-156 "Nightly outcome management" section to reflect the retired state of the Action (deleted at commit 82227f08, 2026-07-08) and current manual operator flow.
- **Skeptic note:** `.github/` NOT FOUND on disk. ARCHITECTURE.md:708-710 warns "Do not follow CONTRIBUTING Nightly outcome management as live guidance" and names the deleted workflow, but the stale text remains in CONTRIBUTING.md itself. No ADR formally accepts this stale state as permanent. Any contributor relying on CONTRIBUTING.md is misdirected to a mechanism that cannot execute.

### Med (1)

**S2** — ARCHITECTURE.md "12 rules" claim vs 13 entries in doc-code-edge.yaml

- **Claim:** ARCHITECTURE.md states "live on 12 rules per the ADR-89 OQ1 naming convention (the #194 cohort-1 five + the #201 governance trio + the #202 Tier-3 quartet)" at lines 349, 432, and 443
- **Location:** ARCHITECTURE.md:349 (also :432, :443)
- **Evidence:** direct read of `ecosystem/doc-code-edge.yaml` coverage_scope block (lines 64-76): 13 named entries
- **Verdict:** contradicted
- **Proposed fix:** Update the three "12 rules" occurrences in ARCHITECTURE.md to "13 rules", adding `governance-backlog-story-id` (#286) to the cohort breakdown.
- **Skeptic note:** Direct read of `ecosystem/doc-code-edge.yaml` coverage_scope confirms 13 entries. The 13th (`governance-backlog-story-id`) was added by #286 without a corresponding ARCHITECTURE.md count update. No ADR documents an accepted discrepancy; no known-inconsistency annotation exists for this count.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — Entry (c) 'Next' section lists '[#429]' as future work
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-29 makes the journal append-only; entries are never edited retroactively. [#429] was filed and merged by a concurrent worktree session at 14:02-14:18, while entry (c) was in-flight — the composing session could not have known [#429] would complete before d5ef97d0 landed at 14:35. No ADR requires 'Next' sections to be retrospectively accurate; the documented remedy is a superseding entry (the pattern entry (b) demonstrates with its "Supersedes the NOT merged status in the entry below" line).

**K2** — Five commits between entries (b) and (c) with no dedicated journal anchor
- **Kill reason:** `evidence-not-definitive`
- **Kill detail:** ADR-85 amendment: "one citation in the session suffices." The [#428] merge (e631e59) is covered by entry (b)'s "Filed [#428]" notation. The [#429] commits (712defc-371daef) were filed by a concurrent session; whether that session operated inside an already-anchored arc cannot be determined from the range evidence alone. Insufficient to prove an ADR-85 session-boundary violation.

**K3** — Two most recent handoff bundle merges (811a6cf, 1bb4889) lack post-merge anchor commits
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-85 amendment: "a --no-ff merge that carries the branch's journal still anchors." Both merges are `--no-ff` and carry journal content (entries g, h, i) on the merged branch. The first-parent ADR-85 logic resolves the anchor through the merge commit itself without requiring a separate post-merge anchor commit citing the merge SHA.

**K4** — Entry (d) merge 4aecf09 (close-exception-record) not anchored by SHA in entry (d)
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-85 amendment: "a --no-ff merge that carries the branch's journal still anchors." Confirmed: 4aecf09's second parent is 54d8d09, the journal commit "docs: record the pytest-red push exception" — it traveled to main via the `--no-ff` merge. No additional post-merge SHA citation is required.

**K5** — #292 validate_residual_completeness gate narrowness (diff-triggered/prospective-only)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The closing commit 9fc1a8b fully discloses the narrowness: "the shipped gate is NARROWER than the ticket asked (whole-body markers only, diff-triggered/prospective-only, PROBES.md never inspected)." Open tickets #365 and #366 already carry the residual gap. Done-when is literally satisfied per ADR-81(d) (explicit documented deferral naming the gap). No hidden conformance failure.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, entries i through b, all 2026-07-26; shallow-clone boundary: ~2026-06-03):**
- Entry (i): anchor SHA f0153b61 — verified, matches entry (h) commit
- Entry (g) dev-knowledge: anchors b3a19bba (supplement FILLED) and 98193954 (fold ANSWERS) — both verified
- Entry (g) ai-council: anchors bf9dad37 (fill SUPPLEMENT) and bdf198d7 (fold SUPPLEMENT) — both verified
- Entry (f) ai-council: anchor 3371b1e2 — verified (cross-repo architect bundle for ai-council 2026-07-26)
- Entry (f) dev-knowledge: anchor 49f4e656 — verified (architect bundle 2026-07-26-dev-knowledge-architect)
- Entry (e): anchor 1c5843c4 (reserve [#373]-[#380] id range) — verified
- Entry (e): anchor caec439d (sol adversarial pass — 6 High findings) — verified
- Entry (e): merge d584ff4a (Merge docs/micro-window-currency) — verified
- Entry (e): serialize-group count correction 17→11 (commit 52a367e) — confirmed; current journal shows "11" with explicit list
- Entry (c): merge d5ef97d0 (Merge docs/hub-defects-handoff-tooling) — verified
- Entry (c): recovery of [#421] and [#422] rows — verified in git diff 903638c5..c74f918 -- BACKLOG.md
- Entry (c): [#430] filed (commit 360bdbb) — verified
- Entry (b): merge 903638c5 (Merge docs/0726-brake-discharge) — verified
- Entry (b): [#428] filed (commit 45af1e1) — verified
- Entry (d): pytest RED test "tests/test_audit.py::test_check_fleet_parity_green_on_live_repo" — documented, consistent with [#430] filing

**V2 (living-doc factual claims):**
- VISION.md fleet count ("nine git repos") — matches ADR-104:15
- VISION.md audit.py command set (6 commands: health/repo/run/registry/ship-gate/checks) — all confirmed via @cli.command decorators
- ARCHITECTURE.md registered check count (32) — matches ALL_CHECKS in scripts/audit.py
- ARCHITECTURE.md pre-commit gate count (15) — matches .pre-commit-config.yaml (15 hook ids)
- ARCHITECTURE.md 14 named checks in validators section — all present in ALL_CHECKS
- ARCHITECTURE.md 5 deploy carrier modules — all Python files confirmed in deploy/
- ARCHITECTURE.md editor-config carrier as "implemented: false" — confirmed in manifest-v1.4.0.yaml
- CLAUDE.md §8 skills (verify + check-against-spec) — both confirmed in .claude/skills/
- CLAUDE.md §8 tier1-lifecycle plugin enabled — confirmed in .claude/settings.json enabledPlugins
- CLAUDE.md §9 pre-commit hook names (all 15) vs .pre-commit-config.yaml — set-match clean
- CLAUDE.md §9 SessionStart hooks (5: fleet_health, surface_triage, billing_leak_sentinel, changelog_sentinel, arm_hooks) — all confirmed in .claude/settings.json
- CLAUDE.md §11 recent ADRs (101-105) — confirmed in docs/decisions/
- CLAUDE.md §7 commands (4: changelog-review, handoff, override, save) — confirmed in .claude/commands/
- All script file paths cited in ARCHITECTURE.md validators section — all present in scripts/
- All ecosystem/ file paths cited in ARCHITECTURE.md — all present
- ARCHITECTURE.md known-inconsistency annotation at :708-710 accurately names the CONTRIBUTING.md stale section

**V3 (backlog-closure semantic coherence, since 2026-07-06):**
- #302 (9fc1a8b) — branch-protection guard deployed to n=2 consumers, FIRING witnessed — coherent
- #309 (9fc1a8b) — backlog-id-on-close at both consumers, hub-only backpressure confirmed — coherent
- #131 (9fc1a8b) — REPO_ONBOARDING.md carries all 6 layers, pilot clause at n=2 — coherent
- #314 (9fc1a8b) — protocols/README.md boundary split documented at both consumers — coherent
- #395 (2c48714) — COHERENCE-NUDGE.log rename; all lockstep targets updated — coherent
- #321 (f865abf) — ARCHITECTURE.md boundary organ rows added, last_reviewed re-stamped 2026-07-22 — coherent
- #398 (6d3dd91) — intake status enum deployed, 6 docs migrated, gen_intake_index --check clean — coherent
- #381 (6943c58) — ADR-104 accepted with (a)(b)(c) each explicitly priced — coherent
- #368 (3cbcf39) — VISION.md 7 content defects fixed, last_reviewed updated 2026-07-25 — coherent
- #339 (19b5d59) — ADR-29 ratified, split threshold defined, LESSONS-legacy registry entry added — coherent
- #262 (19b5d59) — kill-candidate closure for flat layout policy (coherent kill-candidate) — coherent
- #295 (19b5d59) — kill-candidate closure for flat layout policy (coherent kill-candidate) — coherent
- #304 (9fa8bde) — REPO_ONBOARDING.md notation fixed, arg-form table added — coherent

---

## Next Actions (proposals for operator)

1. **S1 (high)** — Update CONTRIBUTING.md lines 132-156: rewrite the "Nightly outcome management" section to reflect that `.github/workflows/nightly-conformance-triage.yml` was deleted 2026-07-08, and describe the current manual operator flow (nightly conformance PR reviewed each morning). ARCHITECTURE.md:708-710 already has the correct framing as a starting point.

2. **S2 (med)** — Update ARCHITECTURE.md: change "12 rules" to "13 rules" at lines 349, 432, and 443, and add `governance-backlog-story-id` (added by #286) to the cohort breakdown. Running `grep -n '12 rules' ARCHITECTURE.md` confirms the three locations.

---

## Safety Tripwire

`git status --porcelain` output (run after writing this file, before commit):

```
?? docs/audits/2026-07-27-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
