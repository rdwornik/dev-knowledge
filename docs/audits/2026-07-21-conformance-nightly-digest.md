<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-21

**Date:** 2026-07-21
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed 2026-07-21, confirmed unavailable. Consistent with all prior nightly runs.)

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
**Prior surviving findings:** 1 (S1 high: CLAUDE.md §8 "No repo-level skills directory exists yet")

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | V2 checked_clean confirms `.claude/skills/` now contains `verify` and `check-against-spec` and CLAUDE.md §8 correctly documents them. Fixed since 2026-06-14 (persisted 4 nights). |
| **NEW** | F1 (high): ARCHITECTURE.md "four carriers" at 5 locations | deploy/tool.py makes_carriers() instantiates five; no ADR update |
| **NEW** | F2 (med): ARCHITECTURE.md "12 rules" for doc->code check | ecosystem/doc-code-edge.yaml has 13 coverage_scope entries |
| **NEW** | F3 (med): ARCHITECTURE.md pre-commit hook list names 13 of 15 hooks | validate-hermetization + intake-index-freshness absent |
| **NEW** | F4 (low): CONTRIBUTING.md ruff hook "language: system" stale | CLAUDE.md §9 corrected in v2.40; CONTRIBUTING.md not updated |

**Delta counts:** 1 resolved · 0 persisting · 4 new
**Skeptic kill-rate:** 43% (3 of 7 raw findings killed)

---

## Summary

Doc health is solid across the journal-commit fidelity layer (V1), the audit/check-count layer (V2), and the backlog-closure layer (V3): 40 of 40 recent commits are accounted for, ALL_CHECKS and pre-commit gate counts match in doc-counts.md, and six closed backlog items have verified Done-when evidence. The four survivors are all straightforward living-doc staleness in ARCHITECTURE.md and CONTRIBUTING.md — no architectural ambiguity, no missing ADRs, just counts and descriptions that drifted when code changed. The most material gap is the "four carriers" claim propagated across five locations in ARCHITECTURE.md and ADR-92, contradicted by unambiguous code evidence and the handoff docs' own "fifth carrier" language. The skeptic filter killed 3 of 7 raw findings (43% kill-rate): one on documentation-style grounds (journal retroactive editing is ungoverned), and two on documented-decision grounds (ADR-103 closes #316; an explicit in-commit declaration exempts the residual-completeness gate from a new ticket). No false positives survived that had documentary cover.

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 4 · **Killed false positives:** 3

<!-- counts: raw=7 survived=4 killed=3 -->

### High (1)

**F1** — ARCHITECTURE.md "four carriers" claim contradicted by code *(NEW)*
- **Claim:** ARCHITECTURE.md states deploy tool has "four carriers" (globalconfig/plugin/precommit/floor) in five locations (lines 193, 204, 345, 500, 663) and ADR-92 Decision 8
- **Location:** ARCHITECTURE.md:193
- **Evidence:** `grep -n 'MeshCarrier\|FloorCarrier\|PluginCarrier\|GlobalConfigCarrier\|PrecommitCarrier' /home/user/dev-knowledge/deploy/tool.py | head -10`
- **Verdict:** contradicted
- **Proposed fix:** Update all five "four carriers" occurrences in ARCHITECTURE.md (lines 193, 204, 345, 500, 663) and ADR-92 Decision 8 to say "five carriers" and explicitly name carrier_mesh alongside the other four.
- **Skeptic note:** deploy/tool.py lines 60–64 import all five carriers and lines 316–322 instantiate all five. Handoff docs explicitly call carrier_mesh.py the "5th carrier" (#236). No ADR updates the "four carriers" claim.

### Med (2)

**F2** — ARCHITECTURE.md "12 rules" for doc->code check is stale *(NEW)*
- **Claim:** ARCHITECTURE.md states doc->code check is "live on 12 rules" (lines 310, 385, 396)
- **Location:** ARCHITECTURE.md:310
- **Evidence:** `grep -A 20 '^coverage_scope:' /home/user/dev-knowledge/ecosystem/doc-code-edge.yaml | grep -c '^  -'`
- **Verdict:** contradicted (returns 13, not 12; governance-backlog-story-id added in #286)
- **Proposed fix:** Update all three "12 rules" occurrences in ARCHITECTURE.md (lines 310, 385, 396) to "13 rules."
- **Skeptic note:** Evidence is unambiguous. No ADR documents or sanctions the discrepancy.

**F3** — ARCHITECTURE.md pre-commit hook enumeration missing two hub-only hooks *(NEW)*
- **Claim:** ARCHITECTURE.md pre-commit gates list (lines 401–411) names 13 hooks as the full set
- **Location:** ARCHITECTURE.md:401
- **Evidence:** `grep '^      - id:' /home/user/dev-knowledge/.pre-commit-config.yaml | wc -l`
- **Verdict:** contradicted (returns 15; validate-hermetization and intake-index-freshness absent from ARCHITECTURE.md)
- **Proposed fix:** Add "validate-hermetization" (#306, Hub-only) and "intake-index-freshness" (#307, Hub-only) to the pre-commit gates enumeration at ARCHITECTURE.md lines 401–411.
- **Skeptic note:** Both hooks are documented in CLAUDE.md §9 and CONTRIBUTING.md. No ADR sanctions omitting them from ARCHITECTURE.md.

### Low (1)

**F4** — CONTRIBUTING.md ruff hook description stale *(NEW)*
- **Claim:** CONTRIBUTING.md line 114 describes ruff hook as "language: system"
- **Location:** CONTRIBUTING.md:114
- **Evidence:** `grep -A3 'astral-sh/ruff-pre-commit' /home/user/dev-knowledge/.pre-commit-config.yaml`
- **Verdict:** contradicted (external pinned managed hook via astral-sh/ruff-pre-commit rev v0.15.5, not language: system)
- **Proposed fix:** Update CONTRIBUTING.md line 114 to describe the external pinned managed hook; mirror the fix already applied to CLAUDE.md §9 in v2.40 (chore/ruff-hub-pin).
- **Skeptic note:** .pre-commit-config.yaml comment explicitly states it was "converted from the former hub-local language: system ruff." CLAUDE.md §9 already correct; CONTRIBUTING.md not updated in lockstep.

---

## Killed Findings

**K1** — JOURNAL.md entry 1 (2026-07-21) says repair "Not repaired — awaiting operator ruling" but git shows repair was executed
- **Kill reason:** `opinion`
- **Kill detail:** The journal entry was authored before the repair was carried out. No ADR or session protocol (ADR-37, ADR-82, ADR-85) requires retroactive updates to journal entries once a subsequent intra-session action resolves the described incident. Whether a session log must be post-edited to reflect intra-session outcomes is a documentation style preference with no documented governance requirement.

**K2** — [#316] closure Done-when not satisfied by ownership-axis delivery
- **Kill reason:** `documented-decision`
- **Kill detail:** ADR-103 (Accepted, 2026-07-17) is the explicit architectural decision that closes #316. ADR-103 states "every parity surface now carries a hub-authoritative, provenance-cited ownership classification — the answers for everything, tracked residual for the root/file-set boundary closes with a machine-readable reason per entry." The operator explicitly chose to satisfy #316 via the ownership axis on parity-surfaces.yaml rather than via a root_files manifest with a diff reporter. Cite: ADR-103.

**K3** — Residual-completeness gate (622baed) shipped with no backlog ticket
- **Kill reason:** `documented-decision`
- **Kill detail:** Merge commit ecc8b5a explicitly states "this lane MINTS no new backlog task id" with detailed rationale. [#292] deliberately remains open and DEFERRED. The absence of a new ticket is not an omission but an operator-conscious, explicitly documented, in-commit decision satisfying the "kill-candidates: none — \<reason\>" clause the backlog-filing-backpressure hook requires.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; 2026-07-20–2026-07-21):**
- All 10 journal entries reconcile to named commits; no significant git work omitted across 40 commits
- First-parent spine: only merge commits on main; the one direct-to-main exception (94426dc0) is documented in journal entry 1 as an in-session incident that was subsequently repaired (e3e79ada)
- Entry 1 (2026-07-21): commits 980584e2 (housekeeping merge) and 94426dc0 (id-range [#373]-[#380] reservation) — confirmed
- Entry 2 (2026-07-20): commit 520bfd56 closing [#355] and [#372]; pytest_collected 1660→1669; BACKLOG.md 135→133 tasks — all confirmed
- Entry 3 (2026-07-20): enforcement-organs commits 7a9ddc6d, 36ca03f0, b0443523, 95ef6d26, 40c7bce3; [#372] filed — confirmed
- Entry 4 (2026-07-20): commit a8136b4 ([#352] render gap); [#370] and [#371] filed (merge 3fc9458) — confirmed
- Entries 5–10 (2026-07-20): commits 5b3b7c70, 42f63015, 34c59b6d, fc6268b5/c993fadc/1d4ea278, 0727e3a0, 21ec4653/10f71693/d84e86c7; doc-counts 1627→1660 — all confirmed

**V2 (living-doc factual claims):**
- ALL_CHECKS count: doc-counts.md claims 31; audit.py ALL_CHECKS list confirms 31
- Pre-commit gate count: doc-counts.md claims 15; .pre-commit-config.yaml confirms 15
- CLAUDE.md §9 hook roster: all 15 hooks match .pre-commit-config.yaml (incl. validate-hermetization + intake-index-freshness)
- All ARCHITECTURE.md Validators section named checks present in audit.py ALL_CHECKS; all script file paths exist on disk
- deploy/tool.py, deploy/contract.py existence — both present
- VISION.md CLI command names (health/repo/run/registry) — all four exist as @cli.command
- .claude/commands/ roster (changelog-review.md, handoff.md, override.md, save.md) matches CLAUDE.md §8
- .claude/skills/ (verify + check-against-spec) matches CLAUDE.md §8 — **the 2026-06-14 persisting high finding is RESOLVED**
- ARCHITECTURE.md defers audit check-count and pre-commit gate count to doc-counts.md (no stale hardcoded numbers at those delegation points)

**V3 (backlog-closure semantic coherence, since 2026-07-01):**
- [#337] fleet_parity ALL_CHECKS blocking promotion + tests on witnessed zero-WARN fleet — Done-when met
- [#336] ADR-102 gate_rev_ahead corp WARN cleared without over-claiming — Done-when met
- [#355] GIT_DIR scrub + regression test test_collect_facts_ignores_inherited_git_dir — Done-when met
- [#372] bundle selection by git add-date + all 4 test classes (add-date order, uncommitted-wins, ambiguous-refusal, exported-GIT_DIR) — Done-when met
- [#313] ADR-101-conformant rename + audit index regenerated — Done-when met
- [#312] design-only deliverable; build landed LANE-D 2026-07-11 — Done-when met

---

## Next Actions (proposals for operator)

1. **F1 (high, NEW)** — Update ARCHITECTURE.md: replace "four carriers" with "five carriers" at all five locations (lines 193, 204, 345, 500, 663) and update ADR-92 Decision 8 in lockstep; explicitly name carrier_mesh alongside the four original carriers.

2. **F2 (med, NEW)** — Update ARCHITECTURE.md: replace all three "12 rules" occurrences (lines 310, 385, 396) with "13 rules" to reflect the 13 coverage_scope entries in ecosystem/doc-code-edge.yaml (governance-backlog-story-id added in #286).

3. **F3 (med, NEW)** — Update ARCHITECTURE.md: add "validate-hermetization" (#306, Hub-only) and "intake-index-freshness" (#307, Hub-only) to the pre-commit gates enumeration at lines 401–411; both already documented in CLAUDE.md §9 and CONTRIBUTING.md.

4. **F4 (low, NEW)** — Update CONTRIBUTING.md line 114: replace "language: system" with description of the external pinned managed hook (astral-sh/ruff-pre-commit rev v0.15.5); mirrors the fix already applied to CLAUDE.md §9 in v2.40 (chore/ruff-hub-pin).

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-21-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
