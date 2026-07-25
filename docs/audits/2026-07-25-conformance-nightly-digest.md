<!-- scope: meta -->
# Nightly Conformance Digest — 2026-07-25

**Date:** 2026-07-25
**Author:** Claude Code (claude-sonnet-4-6), spec-orchestration fallback
**Backlog:** advances #81 (nightly agentic-conformance arc)
**Nature:** **Reports only.** No fixes applied; no living doc edited; no sibling repo touched. All findings are proposals for operator triage.

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (native Workflow launcher not enabled in this cloud runtime — re-probed as of 2026-07-25, confirmed unavailable. Consistent with all prior nightly runs since 2026-06-04.)

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
**Prior surviving findings:** 1 (high, persisting 4 nights: CLAUDE.md §8 stale skills-directory claim)

| Status | Finding | Notes |
|---|---|---|
| **RESOLVED** | Prior S1 (high, persisting): CLAUDE.md §8 "No repo-level skills directory exists yet" | V2 confirmed §8 now correctly names `.claude/skills/verify/` and `.claude/skills/check-against-spec/`. Language removed, directory documented. |
| **NEW** | F2 (med): ARCHITECTURE.md governing-ADR roster stale — "ratified through ADR-103" | ADR-104 accepted 2026-07-24; ARCHITECTURE.md last_reviewed 2026-07-23 (one day prior); no ADR-104 entry in Governing ADRs chapter |
| **NEW** | F3 (med): ESSENTIALS.md corrections.jsonl mechanism claimed active but unimplemented | Active-tense claims in ESSENTIALS.md:138 and PLAYBOOK.md:3153; no file, no script, no Stop hook implements corrections logging |
| **RESOLVED (in-session)** | F1 (med, found this run): fix-live-backlog-test lane SHAs unanchored in JOURNAL | Real at V1 check-time; resolved in-session by commit c98dddd (JOURNAL anchor entry) |

**Delta counts:** 2 new · 1 prior resolved · 1 in-session resolved · 0 persisting from prior baseline
**Skeptic kill-rate:** 33% (1 of 3 raw findings killed)

---

## Summary

The persistent high finding from the prior baseline (CLAUDE.md §8 claiming "no repo-level skills directory exists yet") is now **fully resolved** — V2 confirms §8 now correctly documents both `.claude/skills/verify/` and `.claude/skills/check-against-spec/`. The four-night streak is closed.

Two new medium findings emerge. **F2** is a freshness gap: ADR-104 (fleet repository shape, Accepted 2026-07-24) arrived one day after ARCHITECTURE.md's last_reviewed stamp (2026-07-23), leaving the "ratified through ADR-103" prose and the Governing ADRs chapter one ADR behind. This is a routine post-ADR-acceptance update. **F3** is a phantom mechanism: both ESSENTIALS.md:138 and PLAYBOOK.md:3153 use present-tense active claims that corrections.jsonl logging is live ("every correction logged", "corrections now auto-promote via the corrections.jsonl Stop hook"), but no file, script, or Stop hook implements this. An agent or operator reading ESSENTIALS.md would be misled about whether automated corrections tracking is active.

One finding (F1, the fix-live-backlog-test JOURNAL omission) was real at check-time but resolved in-session: commit c98dddd added the anchoring JOURNAL entry as part of this conformance run, and the skeptic confirmed the gap is closed.

The skeptic kill-rate of 33% (1/3) reflects targeted, well-evidenced verifier output this run: the two survivors both have definitively confirmed evidence commands (ADR-104 existence + ARCHITECTURE.md line, and the absent corrections.jsonl file + settings.json Stop hook wiring), and the one kill was unambiguously resolved before the skeptic ran.

---

## Findings (PROPOSALS ONLY)

**Raw:** 3 · **Survived skeptic:** 2 · **Killed false positives:** 1

<!-- counts: raw=3 survived=2 killed=1 -->

### High (0)

*(none)*

### Med (2)

**S1** — ARCHITECTURE.md governing-ADR roster stale *(NEW)*
- **Claim:** ARCHITECTURE.md:46 states "The six chapters below are the system as built and ratified through ADR-103"
- **Location:** ARCHITECTURE.md:46; Governing ADRs chapter (approx. line 671+)
- **Evidence:** `ls /home/user/dev-knowledge/docs/decisions/ADR-104-fleet-repository-shape.md` (file exists, Status: Accepted, Date: 2026-07-24); `grep -n 'last_reviewed' ARCHITECTURE.md` returns `last_reviewed: 2026-07-23`; `sed -n '40,55p' ARCHITECTURE.md` shows "ratified through ADR-103" at line 46; Governing ADRs section contains no ADR-104 entry
- **Verdict:** contradicted
- **Proposed fix:** Update ARCHITECTURE.md last_reviewed to 2026-07-24, change "ratified through ADR-103" to "ratified through ADR-104", and add ADR-104 entry to the Governing ADRs chapter.
- **Skeptic note:** Evidence definitively confirmed: ADR-104 Accepted 2026-07-24, last_reviewed 2026-07-23 (one day prior), exact stale phrase on line 46, Governing ADRs section has no ADR-104 entry. No ADR exempts ARCHITECTURE.md from updating after a new governing ADR is accepted.

**S2** — ESSENTIALS.md corrections.jsonl mechanism claimed active but unimplemented *(NEW)*
- **Claim:** ESSENTIALS.md:138 states "every correction logged to corrections.jsonl → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook)"
- **Location:** protocols/ESSENTIALS.md:138; also PLAYBOOK.md:3153 positively asserts "corrections now auto-promote via the corrections.jsonl Stop hook"
- **Evidence:** `find /home/user/dev-knowledge -name 'corrections.jsonl'` returns empty; `grep -rn 'corrections' /home/user/dev-knowledge/scripts/` returns empty; `.claude/settings.json` Stop hook runs only `session_end_backpressure.py` — no corrections logger present
- **Verdict:** contradicted
- **Proposed fix:** Either implement the corrections-logging Stop hook as described in ESSENTIALS.md:138 + PLAYBOOK.md:3153, or reword both to mark the mechanism as planned/deferred rather than currently active.
- **Skeptic note:** Both docs use active present-tense. settings.json definitively contains only session_end_backpressure.py. No corrections.jsonl anywhere. No ADR documents intentional deferral of this mechanism after PLAYBOOK.md:3153 explicitly retired the prior manual-review path.

### Low (0)

*(none)*

---

## Killed Findings

**K1** — fix-live-backlog-test lane omitted from JOURNAL.md *(found this run, resolved in-session)*
- **Kill reason:** `true-but-irrelevant`
- **Kill detail:** The omission was real at V1 check time: git log --oneline -3 showed merge 8e2ecc8 (docs/fix-live-backlog-test), grep -c '[#415]' JOURNAL.md returned 0. However, commit c98dddd (now HEAD on branch claude/conformance-2026-07-25) explicitly resolves the gap with a JOURNAL anchor entry for all three SHAs. Re-running grep -c '[#415]' JOURNAL.md now returns 1. No open conformance gap remains.

---

## Checked-and-Clean (selected — absence of findings is informative)

**V1 (JOURNAL → git, top 10 entries; shallow-clone boundary: ~2026-07-04):**
- 2026-07-25: ADR-104 merged at SHA 92fabb51 with parents 023520f0 + 6943c584 — confirmed
- 2026-07-25: [#381] task removed in acceptance commit 6943c584 — confirmed
- 2026-07-25: Anchor branch docs/lane-a-anchor touches only JOURNAL.md (60d68b2) — confirmed
- 2026-07-24: ADR-104 amendment at 224096b (precondition (c) discharged NEGATIVE) — confirmed
- 2026-07-24: ADR-104 draft at aa64def — confirmed
- 2026-07-24: Lane C merge 023520f0 parents f3ead30b + 438887e2 — confirmed
- 2026-07-24: ADR-104 draft-to-acceptance chain aa64def → 224096b → 6943c584 — confirmed
- 2026-07-23 CONSOLIDATION: worktree-ai-council-handoff merged at e151dcbf — confirmed
- 2026-07-23: docs/architecture-currency verified on main as merge 44e47b48 — confirmed
- 2026-07-23: [#405] filed in 199c181 / merge 21a21e8 — confirmed

**V2 (living-doc factual claims):**
- CLAUDE.md §8: `.claude/skills/` holds `verify` and `check-against-spec` — both confirmed present (prior persisting finding RESOLVED)
- CLAUDE.md §9: all 15 pre-commit hooks match `.pre-commit-config.yaml` exactly — verified
- ecosystem/doc-counts.md "31 registered checks" matches ALL_CHECKS in scripts/audit.py (31 active) — verified
- ecosystem/doc-counts.md "15 pre-commit gates" matches 15 hook IDs in .pre-commit-config.yaml — verified
- ARCHITECTURE.md: five carriers (globalconfig/plugin/precommit/floor/mesh) — 5 carrier_*.py files confirmed in deploy/
- ARCHITECTURE.md: 12 doc-code rule IDs — all 12 confirmed in scripts
- ARCHITECTURE.md: docs/decisions/transcripts/ deleted 2026-07-22 — confirmed NOT FOUND
- VISION.md: scripts/audit.py four @cli.command definitions (health/repo/run/registry) — all confirmed
- CONTRIBUTING.md: pre-commit hook table matches .pre-commit-config.yaml (all 15 hooks) — verified
- CLAUDE.md §11: machine-generated recent-adrs.md correctly shows ADR-100 through ADR-104 — verified
- ESSENTIALS.md: protocols/SESSION_SETUP.md exists — confirmed

**V3 (BACKLOG-closure semantic coherence, since 2026-07-04):**
- #381 (ADR-104 fleet shape) — all three intake-required items explicitly priced in ADR-104 §2–§3 — coherent
- #398 (intake status-enum) — audit artifact §3 confirms all 6 off-canon docs migrated; gen_intake_index --check clean — coherent
- #321 (ARCHITECTURE Ch2 organ map) — both boundary rows added, last_reviewed re-stamped — coherent
- #395 (logs/ artifact naming) — UPPERCASE-KEBAB ruled and conformed in one commit — coherent
- #302, #309, #131, #314, #292 (five tickets, commit 9fc1a8b) — all five Done-whens discharged with specific file-level evidence — coherent
- #355, #372 (commit 520bfd5) — regression tests lock the fixed behaviour — coherent

---

## Next Actions (proposals for operator)

1. **S1 (med, new)** — Update ARCHITECTURE.md: change "ratified through ADR-103" → "ratified through ADR-104", add ADR-104 entry to Governing ADRs chapter, re-stamp last_reviewed to 2026-07-24 (or date of next genuine end-to-end re-read). Routine post-ADR-acceptance maintenance.

2. **S2 (med, new)** — Triage the corrections.jsonl mechanism: either (a) implement the Stop hook that logs corrections and promotes at 2× repeat (as ESSENTIALS.md:138 and PLAYBOOK.md:3153 claim), or (b) reword both references to mark the mechanism as planned/deferred and remove the active-tense present claims. Current state misleads agents and operators about automated corrections tracking being live.

---

## Safety Tripwire

`git status --porcelain` output (run after digest written, before commit):

```
 M JOURNAL.md
?? docs/audits/2026-07-25-conformance-nightly-digest.md
```

Expected: JOURNAL.md modified (JOURNAL anchor entry committed to this branch as c98dddd), plus one untracked new digest file. Both expected. No other tracked files changed. If any other tracked file appears here, that is a safety breach requiring operator investigation before merge.
