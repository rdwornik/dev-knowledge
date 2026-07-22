<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-22

**Date:** 2026-07-22
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher auto-denied in this cloud runtime — re-probed 2026-07-22; consistent with all prior nightly runs since 2026-06-04.)

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | synthesized by orchestrator | claude-sonnet-4-6 |

All stages ran on `claude-sonnet-4-6` (orchestrating session model, inherited by subagents). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-14-conformance-nightly-digest.md`
**Prior surviving findings:** 1 (S1 high — CLAUDE.md §8 stale skills claim, persisted 4 consecutive nights)
**Gap since last run:** 38 days (2026-06-14 → 2026-07-22)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | S1 (high): CLAUDE.md §8 "No repo-level skills directory exists yet" | V2 checked_clean confirms `.claude/skills/` now correctly documented with `verify` + `check-against-spec`; the stale claim is gone. Fixed in the 38-day gap. |
| **NEW** | N1 (med): CONTRIBUTING.md ruff description still says `language: system` | The conversion to `astral-sh/ruff-pre-commit` managed form happened (CLAUDE.md v2.40, 2026-07-12) but CONTRIBUTING.md was not updated in lockstep |
| **NEW** | N2 (med): CONTRIBUTING.md last_reviewed: 2026-07-12 < git date 2026-07-17 | Same file as N1; compound failure — factual content stale AND stamp stale |
| **NEW** | N3 (med): ARCHITECTURE.md Ch2 pre-commit gates paragraph lists only 13 of 15 hooks | `validate-hermetization` and `intake-index-freshness` absent from ARCHITECTURE.md despite being added months ago and present in CLAUDE.md §9 and CONTRIBUTING.md |
| **NEW** | N4 (low): VISION.md last_reviewed: 2026-06-19 < git date 2026-07-17 | 28-day gap; git date from merge commit e6fa80a that introduced the file to main without content change |
| **NEW** | N5 (low): docs/handoffs/README.md last_reviewed: 2026-07-10 < git date 2026-07-17 | 7-day gap; same merge commit e6fa80a artifact |

**Delta counts:** 1 resolved · 0 persisting · 5 new
**Skeptic kill-rate:** 29% (2 of 7 raw findings killed)

---

## Summary

Doc health is largely sound after a 38-day gap: JOURNAL entries are fully corroborated by git (V1 found zero issues across all 10 entries, verified 36 commits), and 15 of 17 BACKLOG closures since 2026-06-14 are semantically coherent. The one persisting high finding from the June nightly series (CLAUDE.md §8 stale skills claim) is confirmed RESOLVED.

Five new findings emerge. The clearest is N1/N2: CONTRIBUTING.md line 114 still describes the ruff hook as `language: system` — a factual contradiction since CLAUDE.md v2.40 (2026-07-12) converted it to the `astral-sh/ruff-pre-commit` managed-hook form but did not update CONTRIBUTING.md in lockstep. This file also carries a stale `last_reviewed` stamp (2026-07-12 < git date 2026-07-17), so a genuine re-read + two-part fix is needed. N3 is a parallel gap: ARCHITECTURE.md Ch2 enumerates only 13 of 15 pre-commit hooks, silently missing `validate-hermetization` and `intake-index-freshness` — both correctly documented in CLAUDE.md §9 and CONTRIBUTING.md but absent from ARCHITECTURE.md despite its last_reviewed being 2026-07-18.

N4 and N5 are freshness-stamp artifacts: three canonical files (VISION.md, CONTRIBUTING.md, docs/handoffs/README.md) show git dates of 2026-07-17 from merge commit e6fa80a, which introduced them to main as new files without content change. The `canonical_freshness_gate.py` has no merge-commit exemption, so A2 FAIL fires on all three. N4 (VISION.md, 28-day gap) and N5 (docs/handoffs/README.md, 7-day gap) are low-severity because the content itself may be accurate — but the gate fires and should be addressed either by genuine re-reads or a documented exemption for this merge-commit pattern.

The skeptic kill-rate of 29% (2/7 killed) is lower than prior runs (75% in June), reflecting that Stage 1 verifiers produced higher-quality, better-evidenced findings this cycle — the two kills were a documented-decision close (#316, operator-approved via ADR-103) and a true-but-irrelevant omission (#292, retroactive closure via the designed review_closures gate).

---

## Findings (PROPOSALS ONLY)

**Raw:** 7 · **Survived skeptic:** 5 · **Killed false positives:** 2

<!-- counts: raw=7 survived=5 killed=2 -->

### Med (3)

**N1** — CONTRIBUTING.md ruff hook description contradicts live config *(NEW)*
- **Claim:** CONTRIBUTING.md line 114 describes ruff as "Lint gate — ruff check (version-pinned >=0.15.5, language: system). Blocks on violations."
- **Location:** CONTRIBUTING.md:114
- **Evidence:** `grep -n 'language: system' /home/user/dev-knowledge/CONTRIBUTING.md && grep -A3 'astral-sh/ruff-pre-commit' /home/user/dev-knowledge/.pre-commit-config.yaml`
- **Verdict:** contradicted
- **Proposed fix:** Replace `language: system` description in CONTRIBUTING.md line 114 with `astral-sh/ruff-pre-commit` managed-hook form (rev-pinned v0.15.5) to match the actual `.pre-commit-config.yaml` wiring.
- **Skeptic note:** Confirmed: line 114 still says `language: system`; the `.pre-commit-config.yaml` comment explicitly records "converted from the former hub-local `language: system` ruff for fleet parity." Definitive factual contradiction.

**N2** — CONTRIBUTING.md last_reviewed stale + factual content stale *(NEW)*
- **Claim:** CONTRIBUTING.md frontmatter `last_reviewed: 2026-07-12` but git last-commit date is 2026-07-17
- **Location:** CONTRIBUTING.md:1
- **Evidence:** `git -C /home/user/dev-knowledge log -1 --format='%as' -- CONTRIBUTING.md`
- **Verdict:** contradicted
- **Proposed fix:** Fix the ruff `language: system` error (N1) and re-read CONTRIBUTING.md end-to-end, then bump `last_reviewed` to a genuine review date ≥ 2026-07-17.
- **Skeptic note:** Gate fires (A2 FAIL: reviewed < git_date). Compound: N1 independently confirms the file needs a genuine re-read, not just a stamp bump. Med severity because the content staleness is real.

**N3** — ARCHITECTURE.md Ch2 pre-commit gates paragraph missing 2 of 15 hooks *(NEW)*
- **Claim:** ARCHITECTURE.md Ch2 "Pre-commit gates" paragraph names 13 hooks; actual `.pre-commit-config.yaml` has 15
- **Location:** ARCHITECTURE.md:401-411
- **Evidence:** `grep -n 'validate-hermetization\|intake-index-freshness' /home/user/dev-knowledge/ARCHITECTURE.md; grep -c '      - id:' /home/user/dev-knowledge/.pre-commit-config.yaml`
- **Verdict:** omitted
- **Proposed fix:** Add `validate-hermetization` (#306, ADR-101) and `intake-index-freshness` (#307) to the ARCHITECTURE.md Ch2 pre-commit gates list and bump `last_reviewed`. Both hooks are already correctly listed in CLAUDE.md §9 and CONTRIBUTING.md.
- **Skeptic note:** Both grep for missing hook names in ARCHITECTURE.md returned zero matches (confirmed absent). Hook count command returns 15. ARCHITECTURE.md `last_reviewed` was 2026-07-18 but both hooks predate that date — a genuine re-review gap.

### Low (2)

**N4** — VISION.md last_reviewed stamp predates git date by 28 days *(NEW)*
- **Claim:** VISION.md frontmatter `last_reviewed: 2026-06-19` but git last-commit date is 2026-07-17
- **Location:** VISION.md:4
- **Evidence:** `git -C /home/user/dev-knowledge log -1 --format='%as' -- VISION.md`
- **Verdict:** contradicted
- **Proposed fix:** Re-read VISION.md end-to-end and bump `last_reviewed` to a genuine review date ≥ 2026-07-17; or add merge-commit exemption to `canonical_freshness_gate.py`.
- **Skeptic note:** Evidence command returns 2026-07-17 definitively. `canonical_freshness_gate.py` has no merge-commit exemption; A2 FAIL fires. Gate is `always_run: true`. 2026-07-17 date is from merge commit e6fa80a (initial population of file to main without content change) — plausible false positive by content, but no documented exemption exists. Low severity.

**N5** — docs/handoffs/README.md last_reviewed stamp predates git date by 7 days *(NEW)*
- **Claim:** `docs/handoffs/README.md` frontmatter `last_reviewed: 2026-07-10` but git last-commit date is 2026-07-17
- **Location:** docs/handoffs/README.md:2
- **Evidence:** `git -C /home/user/dev-knowledge log -1 --format='%as' -- docs/handoffs/README.md`
- **Verdict:** contradicted
- **Proposed fix:** Re-read `docs/handoffs/README.md` end-to-end and bump `last_reviewed` to a genuine review date ≥ 2026-07-17.
- **Skeptic note:** Same A2 FAIL path as N4; no merge-commit exemption. 7-day gap; no additional content staleness identified. Low severity.

---

## Killed Findings

**K1** — #316 closure scope gap (fleet_parity.py `ls`-diff clause unimplemented)
- **Kill reason:** `documented-decision`
- **Kill detail:** Operator explicitly closed #316 via commit 9e8e189 using the standard `backlog-id-on-close` mechanism (`closes [#316]` tag; gate did not block). ADR-103 Consequences section states the 'answers for everything, tracked' residual "closes with a machine-readable reason per entry." The operator's deliberate use of the standard closure gate is the authoritative decision in this system; verifier note acknowledges "Operator approved the closure." Cite: ADR-103 + commit 9e8e189.

**K2** — #292 retroactive closure (no concurrent `closes` tag in satisfying commit)
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The `review_closures` mechanism is an intentionally designed retroactive closure path. JOURNAL explicitly records the pattern in operation: "Closures (5, WEAK tier, each individually approved) … #292, via `review_closures.py plan`." The 2-day lag is designed recovery behavior, not a process gap. The gate system worked as designed.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, TOP 10 entries; 2026-07-17 through 2026-07-22):**
- Entry 1: North-Star ingestion — commit b73319ef exists; `docs/intake/2026-07-21-func-fleet-north-star.md` on disk; BACKLOG now 9 themes / 27 stories / 136 tasks (consistent with E9 addition)
- Entry 2: integration merges 35421081, 85b1a9cc, 323b8bd9 — all exist with correct parent chains
- Entry 3: ai-council handoff 2026-07-21-ai-council-architect — commits 36cf6b42, e54aa40b, c733dc4b confirmed; 13/13 probes verified in PROBES.md
- Entry 4: dev-knowledge supplement fill — commits e78cebe2 and 26929336 confirmed; 11/11 probes verified
- Entry 5: COLD handoff 2026-07-21-dev-knowledge-architect — commit 70d9f4a5 confirmed; BACKLOG at 128 tasks verified at parent 5b2ccadb
- Entry 6: BACKLOG hygiene 133→128 tasks — commits 0c7f04e9, 3e1e3f0, 9fc1a8b4 all confirmed; count change verified
- Entry 7: cleanup lane — commit 3234b4a0 confirmed; comment-only change to ecosystem/deployed-versions.yaml
- Entry 8: code audit — commit c8f7741d confirmed; audit file 723 lines as claimed; "80 prod files, 25,636 LOC" matches commit body
- Entry 9: night backlog audit — commit 571fd234 confirmed; "133 open items, 6 kill-candidates" matches commit message
- Entry 10: night vision audit — commit 6dd559a2 confirmed; retroactive anchor e271be4 acknowledged and present in git
- No significant merged work absent from last-10 JOURNAL entries

**V2 (living-doc factual claims):**
- `.pre-commit-config.yaml` has 15 hooks (15 confirmed) — matches doc-counts.md "15"
- `audit.py` has 31 registered checks in ALL_CHECKS — matches doc-counts.md "31"
- CLAUDE.md §9 pre-commit hooks roster: all 15 hooks present and correctly described
- CLAUDE.md ruff §9: correctly states `astral-sh/ruff-pre-commit` @ v0.15.5 fleet-canonical form
- `.claude/skills/` contains exactly `verify` and `check-against-spec` — matches CLAUDE.md §8
- `.claude/commands/` has changelog-review.md, handoff.md, override.md, save.md — matches generated roster
- `.claude/rules/git-discipline.md` exists — matches CLAUDE.md §9 Rules section
- `docs/decisions/ADR-099` through `ADR-103` all exist on disk — matches recent-adrs.md roster
- ARCHITECTURE.md `last_reviewed: 2026-07-18` — git date is 2026-07-18 (no stale flag)
- CLAUDE.md `last_reviewed: 2026-07-20` — git date is 2026-07-20 (no stale flag)
- ESSENTIALS.md `last_reviewed: 2026-07-19` — git date is 2026-07-19 (no stale flag)
- All 13 ARCHITECTURE.md Ch2 named audit checks exist in ALL_CHECKS registry
- All validator scripts named in ARCHITECTURE.md/CLAUDE.md exist in `scripts/`
- ARCHITECTURE.md audit.py subcommands (run, repo, registry, health, ship-gate, checks): all 6 confirmed
- CONTRIBUTING.md hooks table correctly lists all 15 hooks (the missing-from-ARCHITECTURE.md two ARE in CONTRIBUTING.md)

**V3 (backlog-closure semantic coherence, 2026-06-14 → 2026-07-22):**
- #330 root-archive prohibition: rule codified in PLAYBOOK Ch2 + CLAUDE.md g2 sweep — coherent
- #326 ARCHITECTURE ToC+Mermaid stripped fleet-wide: Done-when verified via A0 traceability table
- #333 codex-review doc-lane: Done-when verified via PLAYBOOK §16
- #254 fleet-audit data-branch organ: Done-when verified against ARCHITECTURE Ch2:L181
- #336 fleet_parity split-state reconciliation: Done-when verified via ADR-102 GATE_AHEAD_DECLARED
- #337 fleet_parity ALL_CHECKS membership: Done-when verified with tests
- #313 ADR-101 audit rename: Done-when verified via closing merge bf6f559d7
- #312 fleet methodology-boundary marker DESIGN: Done-when verified via design doc + marker spec
- #355 fleet_parity commit-context resolution: Done-when verified at 520bfd5 with regression test
- #372 check_handoff_probes active-bundle selection: all 4 test classes verified at 520bfd5
- #302 block-ff-push consumers: Done-when (n=2 + witnessed firing) verified at 9fc1a8b
- #309 backlog-id-on-close consumers: Done-when (both OR branches discharged) verified at 9fc1a8b
- #131 repo-onboarding runbook: Done-when (runbook + 6 layers + piloted n=2) verified at 9fc1a8b
- #314 protocols/ mandated genre: Done-when (documented + n=2) verified at 9fc1a8b
- #292 handoff-completeness gate: retroactively closed via review_closures gate (designed path) — coherent
- No large merges in the 5-week window arrived without traceable backlog attribution

---

## Next Actions (proposals for operator)

1. **N1 + N2 (med, compound)** — Fix CONTRIBUTING.md in one edit: (a) replace `language: system` at line 114 with the `astral-sh/ruff-pre-commit` managed-hook description (matching `.pre-commit-config.yaml` and CLAUDE.md §9); (b) re-read end-to-end; (c) bump `last_reviewed` to the genuine review date. Two problems, one re-read pass.

2. **N3 (med)** — Update ARCHITECTURE.md Ch2 pre-commit gates paragraph: add `validate-hermetization` and `intake-index-freshness` to the named-hook list (already in CLAUDE.md §9 and CONTRIBUTING.md), then bump `last_reviewed`. Simple additive edit.

3. **N4 + N5 (low)** — Address the merge-commit freshness-stamp artifact: either (a) re-read VISION.md and `docs/handoffs/README.md` end-to-end and bump their `last_reviewed` stamps to a genuine review date ≥ 2026-07-17; or (b) add merge-commit exemption logic to `canonical_freshness_gate.py` so the gate correctly ignores merge commits that introduce a file without content change. Option (a) is simpler; option (b) prevents recurrence.

---

## Safety Tripwire

`git status --porcelain` output:

```
?? docs/audits/2026-07-22-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
