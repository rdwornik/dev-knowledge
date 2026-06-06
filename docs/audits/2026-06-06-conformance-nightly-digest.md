<!-- scope: meta -->
# Nightly Conformance Digest — 2026-06-06

**Date:** 2026-06-06
**Author:** Claude Code (claude-sonnet-4-6), operator Rob
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-06-06, confirmed unavailable).

| Stage | Label | Model actually used |
|---|---|---|
| Stage 1 — V1 JOURNAL-vs-git | `V1-journal-vs-git` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V2 living-doc claims | `V2-livingdoc-claims` (Explore subagent) | claude-sonnet-4-6 |
| Stage 1 — V3 backlog closures | `V3-backlog-closures` (Explore subagent) | claude-sonnet-4-6 |
| Stage 2 — skeptic | `skeptic-adversarial` (Explore subagent) | claude-sonnet-4-6 |
| Stage 3 — digest | `digest-synthesis` (Explore subagent) | claude-sonnet-4-6 |

All five stages ran on `claude-sonnet-4-6` (the orchestrating session model, inherited by all subagents in the spec-orchestration fallback path). Native Workflow launcher remains unavailable in cloud — consistent with all prior nightly runs.

---

## Delta vs Prior Baseline

**Prior digest:** `docs/audits/2026-06-05-conformance-nightly-digest.md`
**Prior surviving finding:** S1 (med) — ARCHITECTURE.md and CONTRIBUTING.md reference HANDOFF_PROCESS v4.3.2, but canonical file is v4.4

| Status | Finding | Evidence |
|---|---|---|
| **RESOLVED** | S1 (med): ARCHITECTURE.md/CONTRIBUTING.md stale HANDOFF_PROCESS v4.3.2 stamp | ARCHITECTURE.md:336,402 now say "stamp 4.4, status live"; CONTRIBUTING.md:171 says "stamp v4.4, live" — confirmed correct by V2 scan |
| **NEW** | N1 (high): #74 closure reinterprets Done-when 'alongside' as 'honored via forward-pointer' without ADR amendment | commit 11ef2d8 explicitly acknowledges #18/#27 not yet written; closure accepted proxy satisfaction |
| **NEW** | N2 (med): ARCHITECTURE.md 'Last updated: 2026-06-04' contradicts last_reviewed: 2026-06-05 frontmatter | Commit a1b2856 (2026-06-05) bumped last_reviewed but not the "Last updated:" changelog line |

**Delta counts:** 1 resolved · 0 persisting · 2 new

---

## Summary

Overall documentation conformance is healthy with 33 verified clean items spanning commits, architecture, living docs, and backlog closures across 2026-06-05 to 2026-06-06. Two substantive findings survived skeptic review: a high-severity interpretation drift in backlog closure #74 (Done-when reinterpreted from literal co-location to forward-pointer satisfaction) and a medium-severity metadata inconsistency in ARCHITECTURE.md (Last updated timestamp not incremented to match last_reviewed frontmatter after 2026-06-05 review). Skeptic kill-rate is 0% (no false positives eliminated this run), indicating both survivors represent genuine doc-state gaps rather than verification artifacts.

---

## Findings (PROPOSALS ONLY)

**Raw:** 2 · **Survived skeptic:** 2 · **Killed false positives:** 0

<!-- counts: raw=2 survived=2 killed=0 -->

### High (1)

**N1** — `backlog-closures` — #74 closure reinterprets Done-when 'alongside' criterion from literal co-location to forward-pointer satisfaction without explicit ADR amendment

- **Location:** commit `4c62f63` (closure message); commit `11ef2d8` (diff)
- **Evidence command:** `git show 4c62f63 | head -10 && git show 11ef2d8 | grep -A 3 'Forward-pointer'`
- **Verdict:** contradicted
- **Proposed fix (proposal only):** Document the 'alongside vs forward-pointer' interpretation drift in an ADR clarification or update the #74 Done-when to reflect that co-location via forward-pointer satisfies the criterion
- **Skeptic note:** Original #74 Done-when: "the criterion is written alongside the convene-vs-Path-A (#18) and relax-vs-gate (#27) rules". Closure message explicitly states '#18/#27' co-location aspect is 'honored via the PLAYBOOK forward-pointer (those rules are not yet written)'. The literal Done-when was not satisfied, but the closure accepted a reinterpreted version. This represents unwritten consent to a different completion standard.

### Med (1)

**N2** — `living-docs` — ARCHITECTURE.md 'Last updated: 2026-06-04' contradicts last_reviewed: 2026-06-05 frontmatter after 2026-06-05 substantive review (incomplete post-edit metadata cleanup)

- **Location:** `ARCHITECTURE.md:2` (last_reviewed frontmatter), `ARCHITECTURE.md:11` ("Last updated:" changelog line)
- **Evidence command:** `git show a1b2856:ARCHITECTURE.md | head -15 && git log -1 --oneline -- ARCHITECTURE.md`
- **Verdict:** contradicted
- **Proposed fix (proposal only):** Update 'Last updated:' timestamp to 2026-06-05 in the changelog line to match last_reviewed frontmatter
- **Skeptic note:** Commit a1b2856 (2026-06-05) bumped last_reviewed to 2026-06-05 and added substantive ADR-68 [REFUTED — historical] annotation. The 'Last updated:' changelog line was not incremented from 2026-06-04. This is an incomplete metadata update on an otherwise substantive review — the discrepancy is real and demonstrates incomplete post-edit cleanup.

### Low (0)

*(none)*

---

## Killed Findings

*(none — skeptic kill-rate 0% this run; both raw findings survived adversarial review)*

---

## Checked-and-Clean (33 items — absence of findings is informative)

**V1 (JOURNAL → git, last 10 entries):**
- 2026-06-06 ADR-72 created and merged (commit 931034c verified)
- 2026-06-06 #75 bookkeeping session commits verified (f50dda6, bd3482e, a164cda, 8d91c2f, 848f6a7)
- 2026-06-06 External research note landed (commit 1b54c8e verified)
- 2026-06-05 Pilot #81 findings applied (6266fd8, 74c5e41, 0e3d021, a381f72 all verified)
- 2026-06-05 Escalation rule written and committed (11ef2d8 verified)
- 2026-06-05 #80 research note landed (ca843bb, fdea539, 397e42d verified)
- 2026-06-05 Night-doctrine section added (7a3e48b, a1b2856, 137048e verified)
- 2026-06-05 Doc-debt items codified in BACKLOG (27ae852, eee32d7 verified)
- 2026-06-05 Plugin 0.1.3 deployed and validated (b55053f verified)
- 2026-06-05 Backlog hardening completed (7ecef15, b6334c4, 5415ad1 verified)
- 2026-06-05 Test A re-run passed (c904618, b640207 verified)
- All commits cited in entries 2026-06-05+ exist in git history (81/81 commits verified)

**V2 (living-doc factual claims):**
- VISION.md tier-system deprecated 2026-05-23 per ADR-38 amendment A5 — confirmed
- ARCHITECTURE.md codemap two-node (codemap/ and toc/ packages) — both directories exist in scripts/
- ARCHITECTURE.md audit.py check count de-hardcoded to point at `python scripts/audit.py checks`
- ARCHITECTURE.md audit.py is read-only validator — zero orchestration confirmed in scripts/audit.py
- CLAUDE.md last_reviewed freshness check with 30-day backstop — verified in CONTRIBUTING.md
- CONTRIBUTING.md 13 self-conformance checks — verified ALL_CHECKS list in scripts/audit.py:967–981
- CONTRIBUTING.md pre-commit hooks complete (8 hooks) — all present in .pre-commit-config.yaml
- HANDOFF_PROCESS.md v4.4 status live — verified in file header
- HANDOFF_PROCESS.md 8-file bundle (README + 01–07) — verified
- ARCHITECTURE.md:336 and :402 reference HANDOFF_PROCESS stamp 4.4 — correct (**prior S1 resolved**)
- CONTRIBUTING.md:171 references HANDOFF_PROCESS stamp v4.4 live — correct (**prior S1 resolved**)
- ARCHITECTURE.md ADR-68 marked [REFUTED — historical] with evidence citations — correct
- ADR-71 doc-tooling hook source-repo pattern documented and referenced
- All living docs exist: VISION.md, CLAUDE.md, ARCHITECTURE.md, CONTRIBUTING.md, protocols/
- docs/decisions/README.md exists with full ADR index
- Root README.md absent (deleted per ADR-38 amendment A5) — confirmed

**V3 (backlog-closure semantic coherence):**
- `5f327b2` closes [#88]: graphify REJECT verdict recorded with measurements — coherent
- `b6334c4` closes [#83]: validate_backlog hardening — coherent
- `a53c7ae` closes [#12]: evolution machinery — coherent
- `bd3482e` closes [#75]: corp audit — coherent
- `0ee6877` closes [#80]: Dynamic Workflows research — coherent

---

## Next Actions (proposals for operator)

1. **[HIGH]** Clarify #74 Done-when interpretation via ADR amendment or explicit rule: current closure accepts forward-pointer proxy satisfaction without recorded consent to the reinterpreted completion standard — either amend the Done-when retroactively or file a new BACKLOG item for the literal co-location work (#18/#27 still open).
2. **[MED]** Increment ARCHITECTURE.md "Last updated:" timestamp to `2026-06-05` to match `last_reviewed` frontmatter, completing post-review metadata hygiene from commit a1b2856.

---

## Safety Tripwire

`git status --porcelain` output at review completion (before this digest file was written):

```
(empty — clean working tree)
```

Only this digest file was written during the review. If any other tracked file appears in the porcelain output on the PR branch, that is a safety breach.

`git status --porcelain` output on this branch (post-digest write, pre-commit):

```
?? docs/audits/2026-06-06-conformance-nightly-digest.md
```

Expected: one untracked file (this digest). No other changes.
