<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-29

**Date:** 2026-07-29
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled / auto-denied in this cloud runtime — re-probed 2026-07-29; consistent with all prior nightly runs.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | synthesized by orchestrator (claude-sonnet-4-6) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (the orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

**Operational observation (not a conformance finding):** The `session_end_backpressure.py` Stop hook failed on every turn of this session with `uv run --locked` erroring: required `==0.11.19`, running `0.8.17`. The `pyproject.toml` [tool.uv] `required-version` correctly states `==0.11.19` (no documentation claim is contradicted), but the runtime environment has an older uv version. This is an environment gap, not a doc-claims issue; surfaced here as an operational note for the operator.

---

## Delta vs Prior Baseline

**Prior nightly digest on main:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high — CLAUDE.md §8 stale "no repo-level skills directory")
**Context:** Seven nightly digests (2026-07-21 → 2026-07-27) exist on unmerged `claude/conformance-*` branches; the 2026-07-27 extraction aggregate (`docs/audits/2026-07-27-verification-conformance-extraction-aggregate.md`) synthesizes their findings. Today's run independently re-verifies all live claims against current main.

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | Resolved — CLAUDE.md §8 (v2.23) now documents `.claude/skills/` (verify + check-against-spec). `evidence: ls /home/user/dev-knowledge/.claude/skills/` |
| **NEW** | N1 (high): CONTRIBUTING.md:135 stale GitHub Action | Deletion at `82227f08` was 2026-07-08; new since 2026-06-14 baseline. Flagged by unmerged 07-27 branch digest (S1, High); still live on main. |
| **NEW** | N2 (med): ESSENTIALS.md:138 `corrections.jsonl` mechanism | Unimplemented claim; confirmed new since 2026-06-14. First flagged on unmerged 07-23 branch digest. |
| **NEW** | N3 (low): ARCHITECTURE.md "12 rules" for doc-code-edge.yaml (actually 13) | Count drift; confirmed new since 2026-06-14. First flagged on unmerged 07-23/07-24 branch digests. |

**Delta counts:** 1 resolved · 0 persisting · 3 new
**Skeptic kill-rate:** 25% (1 of 4 raw findings killed)

---

## Summary

Documentation health is materially good but carries three unclosed items inherited from the unmerged branch run series (2026-07-21→07-27). The prior persisting finding (CLAUDE.md §8 stale skills claim, 4 consecutive nights) is resolved: §8 now correctly names `.claude/skills/` and its two entries.

The three new findings share a structural root: each is a living-doc claim that was correct at one point but became unsupported after a subsequent repo change, and the change's author noted the stale claim as "out of scope to fix in this window." Two are low-complexity fixes (ESSENTIALS.md one-liner, ARCHITECTURE.md three-site count update). One (CONTRIBUTING.md §Nightly outcome management) describes a deleted GitHub Action in present tense; ARCHITECTURE.md Ch6 already contains a "Do not follow CONTRIBUTING…" advisory that partially mitigates it for readers who cross-reference.

The skeptic killed one V1 finding (entry k JOURNAL attribution) as true-but-irrelevant: the JOURNAL's attribution of the [#440] rename-remnant cause to `ae55ff8b` is slightly wrong (the cause was an earlier slug-truncation; the cleanup was at `104a04f`) but the JOURNAL is append-only, immutable, and the actual repo work was done correctly.

V3 closed 12 BACKLOG items since 2026-07-08; all verified semantically coherent with their stated Done-when criteria.

---

## Findings (PROPOSALS ONLY)

**Raw:** 4 · **Survived skeptic:** 3 · **Killed false positives:** 1

<!-- counts: raw=4 survived=3 killed=1 -->

### High (1)

**N1** — CONTRIBUTING.md §Nightly outcome management stale GitHub Action *(NEW since 2026-06-14; flagged on unmerged 07-27 branch digest as S1 High)*
- **Claim:** CONTRIBUTING.md:135 says "The repo's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`) handles the morning so the operator touches only findings" — describing it as a live organ in present tense.
- **Location:** CONTRIBUTING.md:135
- **Evidence:** `ls /home/user/dev-knowledge/.github/ 2>/dev/null || echo 'NO .github/ dir'`
- **Verdict:** contradicted
- **Proposed fix:** Update CONTRIBUTING.md §"Nightly outcome management" (lines 132-156) to match ARCHITECTURE.md Ch6's framing: the Action was retired at `82227f08` (2026-07-08), Stage 2 of the triage loop is dead, and the section should describe the current fallback-only loop. ARCHITECTURE.md Ch6 already has the "Do not follow CONTRIBUTING…" advisory but CONTRIBUTING.md itself remains unreconciled.
- **Skeptic note:** Evidence definitive. `.github/` directory deleted `82227f08`. ARCHITECTURE.md Ch6 explicitly warns readers not to follow this CONTRIBUTING.md section but does not constitute ADR-documented approval to leave it stale. Reader impact is high (the section would direct someone to find a file that doesn't exist).

### Med (1)

**N2** — ESSENTIALS.md:138 `corrections.jsonl` auto-promotion mechanism *(NEW since 2026-06-14; first flagged on unmerged 07-23 branch digest)*
- **Claim:** ESSENTIALS.md:138 states "**Automated:** every correction logged to `corrections.jsonl` → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook)."
- **Location:** protocols/ESSENTIALS.md:138
- **Evidence:** `find /home/user/dev-knowledge -name "corrections.jsonl" 2>/dev/null | head -5` (returns nothing); `grep -n "corrections" /home/user/dev-knowledge/scripts/session_end_backpressure.py` (returns nothing)
- **Verdict:** unsupported
- **Proposed fix:** Either implement the described mechanism (corrections.jsonl logging → auto-promotion to LESSONS.md rule + verify: check) or remove this sentence from ESSENTIALS.md and replace with what actually happens (corrections are manually codified via LESSONS.md append).
- **Skeptic note:** Evidence is definitive: `corrections.jsonl` does not exist anywhere in the repo and `session_end_backpressure.py` (the Stop hook) has zero references to "corrections." The feature described is either aspirational or was removed without updating ESSENTIALS.md.

### Low (1)

**N3** — ARCHITECTURE.md "12 rules" for `ecosystem/doc-code-edge.yaml` (actually 13 behavioral rules) *(NEW since 2026-06-14; first flagged on unmerged 07-23/07-24 branch digests; persisted across all subsequent nights)*
- **Claim:** ARCHITECTURE.md:360, :443, :454 all state "12 rules" for the doc→code declared-edge check, referencing "the #194 cohort-1 five + the #201 governance trio + the #202 Tier-3 quartet."
- **Location:** ARCHITECTURE.md:360 (also :443, :454)
- **Evidence:** `grep -n "12 rules" /home/user/dev-knowledge/ARCHITECTURE.md` (shows 3 sites) vs behavioral rule count: `grep -E "^\s+- [a-z_]+" /home/user/dev-knowledge/ecosystem/doc-code-edge.yaml | grep -v "not a doc->code behavioral rule\|self-referential\|code->code\|sits outside" | wc -l` (returns 13)
- **Verdict:** contradicted
- **Proposed fix:** Update ARCHITECTURE.md:360, :443, :454 to say "13 rules" (the 12 original + `residual_completeness` added by a later arc). Three-site replacement, same session — `ARCHITECTURE.md` will need its `last_reviewed` re-stamped if edited end-to-end.
- **Skeptic note:** Count discrepancy is real and has persisted across seven consecutive nightly digests on unmerged branches. `residual_completeness` is a genuine behavioral rule added after the "12 rules" text was set. The three ARCHITECTURE.md sites are consistent with each other but all off by one.

---

## Killed Findings

**K1** — JOURNAL.md:77 (entry k) attribution of [#440] rename remnant to `ae55ff8b`
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** V1 found that entry (k)'s "Ride-alongs" line attributes the [#440] rename remnant to "ae55ff8b retitled without regen," but `git show ae55ff8b --name-only` shows that commit did not touch any `tasks/440-*` file. The actual cause was a slug-truncation divergence from the strangler flip (entry f); the cleanup was performed correctly at `104a04f`. However: (a) the JOURNAL is append-only and immutable — it cannot be corrected; (b) the described repair action (`104a04f`) is correct in git; (c) the wrong attribution of root cause within one arc's cleanup note has no downstream impact on repo navigation, verification, or correctness. Killed as true-but-irrelevant.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries; git history NOT shallow — 249 commits):**
- Entry (n) five prep artifacts: `b35c909` — git stat confirms exactly 5 new files in `docs/audits/` ✓
- Entry (n) terra review `577cfab`: 3 P2 + 1 P3 records, all adopted ✓
- Entry (m) P9 sweep `aa16bf6`: closes [#437][#439][#444], leaves [#433] open; BACKLOG.md 179→176 verified ✓
- Entry (l) plugin release `f725323`: 0.1.10→0.1.11, 6 files (plugin.json + 5 manifests) ✓
- Entry (k) closure-token core `08aff16`, design `3b2142b`, impl `605d45c`, H-A/H-B `583ec52`: all verified ✓
- Entry (j) intake ratification `ae55ff8`: #20 ACCEPTED, #16 ACCEPTED/deferred, [#443] filed ✓
- Entry (i) doc_rot fit `9ce96be`: corrects entry h; 6 task rows compressed to fit ✓
- Entry (h) recording batch `93f92ab`: owner=user ruled, [#441][#442] filed, 0 closures ✓
- Entry (g) [#386] closure `7668fa1a` (PLAYBOOK §21 authoring, 2026-07-22): SHA exists, subject matches ✓
- Entry (f) ADR-107 ratification `096364ac`, flip `5c8a9d6d`: both verified ✓
- Entry (e) supplement fold `6818b7d9`: verified ✓
- No unaccounted merge commits in the window (all 10 merge commits in range have JOURNAL entries) ✓

**V2 (living-doc factual claims):**
- CLAUDE.md §9 pre-commit hook roster (15 hooks) matches `.pre-commit-config.yaml` exactly ✓
- CONTRIBUTING.md validator table (15 rows) matches `.pre-commit-config.yaml` ✓
- CLAUDE.md §7 commands (@-imported fragment) reflects `.claude/commands/` (4 files: changelog-review, handoff, override, save) ✓
- CLAUDE.md §8 skills: `.claude/skills/verify/` and `.claude/skills/check-against-spec/` both present ✓ (prior S1 RESOLVED)
- CLAUDE.md §9 SessionStart: 5 commands (fleet_health.py, surface_triage.ps1, billing_leak_sentinel.ps1, changelog_sentinel.py, arm_hooks.py) match `.claude/settings.json` ✓
- CLAUDE.md §11 @-imported recent-ADRs fragment: ADR-103 → ADR-107 match the 5 highest-numbered on disk ✓
- VISION.md "nine git repos (ADR-104)" confirmed by ADR-104 Context ✓
- ARCHITECTURE.md five deploy carriers: 5 `carrier_*.py` files in `deploy/` ✓
- ruff pre-commit hook at `v0.15.5`; pyproject.toml `[tool.ruff] required-version = ">=0.15.5"` — floor matches pin ✓
- HANDOFF_PROCESS.md v5.7; CONTRIBUTING.md frontmatter `reconciled_with: handoff-process@5.7` ✓
- `ecosystem/doc-counts.md` records 15 pre-commit gates — consistent with CLAUDE.md §9 and CONTRIBUTING.md ✓
- `.claude/settings.json` enables `tier1-lifecycle@dev-knowledge-methodology` plugin — matches CLAUDE.md §8 ✓
- Living-doc `last_reviewed` stamps: CLAUDE.md 2026-07-23, ARCHITECTURE.md 2026-07-28, VISION.md 2026-07-25, CONTRIBUTING.md 2026-07-27, ESSENTIALS.md 2026-07-23 — all consistent with git modification dates ✓

**V3 (backlog-closure semantic coherence, since 2026-07-08):**
- closes [#437] @ `aa16bf6`: shared `closure_ids` core; seeded quoted tag yields nothing; 110 tests green ✓
- closes [#439] @ `aa16bf6`: `--emit-source` zero writes, `--check` REDs divergence, ship-gate GREEN ✓
- closes [#444] @ `aa16bf6`: 0.1.11 version-keyed cache for hub + corp + ai-council; release-lint 0 FAIL ✓
- closes [#386] @ `3ed2934`: PLAYBOOK §21 contains all three required rules (live-session check, frozen contract, operator witness) ✓
- closes [#434] @ `d66aef6`: aggregate at `16c5386f` (07-27) AND fork ruled same window `495b8a22`; both Done-when clauses verified in commit body ✓
- closes [#436] @ `a3d383d`: all 5 Done-when clauses verified; ratchet registered in ALL_CHECKS, FAILs above / passes at-or-below baseline, baseline committed, tests pin both directions, terra review recorded ✓
- closes [#339] @ `19b5d59`: ADR-29 in-file ratification marker (2026-07-17), threshold 300 recorded, state 241 < 300 — disjunctive Done-when second branch ("recorded not-yet-needed") satisfied ✓
- closes [#262] @ `19b5d59`: kill-candidate path pre-authorized; ai-council drift carved to [#416] (confirmed open BACKLOG.md:187) ✓
- closes [#295] @ `19b5d59`: kill-candidate path pre-authorized in item text (flat no-tach layout policy) ✓
- closes [#304] @ `9fa8bde`: runbook deploy command fixed, enforcement_coverage.py fixed (2 sites), per-command arg-form table added ✓
- closes [#368] @ `3cbcf39`: genuine end-to-end re-read, 7 content defects fixed + re-stamped `last_reviewed` in same commit ✓
- closes [#381] @ `6943c58`: ADR-104 Accepted; (a) unfold cost, (b) employer-data boundary, (c) pre-sales blast radius — all three explicitly priced in ADR-104 §3 ✓

---

## Next Actions (proposals for operator)

1. **N1 (high)** — Update CONTRIBUTING.md §"Nightly outcome management" (lines 132–156): replace present-tense description of the deleted `.github/workflows/nightly-conformance-triage.yml` Action with the current reality (dead Stage 2 / spec-orchestration fallback running nightly, no auto-triage). ARCHITECTURE.md Ch6 already has accurate prose — cross-referencing it would inform the rewrite.

2. **N2 (med)** — Reconcile ESSENTIALS.md:138 "Automated: every correction logged to `corrections.jsonl`…": either implement the mechanism or rewrite the sentence to describe what actually happens (manual LESSONS.md append for recurring-error patterns). This sentence has likely been aspirational since the Stop hook was last redesigned.

3. **N3 (low)** — Update ARCHITECTURE.md:360, :443, :454 from "12 rules" to "13 rules" to match the current `ecosystem/doc-code-edge.yaml` behavioral rule count (the 12 original + `residual_completeness`). Three-site replacement; update `last_reviewed` if the file is re-read end-to-end.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-29-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
