# Pre-Debate Audit — Cross-Repo Prescriptions + Handoff Pain — 2026-04-27

<!-- scope: meta -->

> READ-ONLY audit feeding two AI Council debates:
> 1. `.dev-knowledge` identity shift — authority model for universal pattern guardian role
> 2. Handoff architecture — pool vs medium model + browser ↔ Claude Code synergy
>
> Evidence-based enumeration only. No solutions, no recommendations.
> Council debates produce those.

## Summary

Output A: 5 active cross-repo prescriptions (2 fully deployed, 3 partially deployed or pending).
Output B: 5-repo inventory — 3 compliance gaps (ai-council CLAUDE.md overlength, corp-monorepo AGENTS.md wrong template, 3 repos missing AGENTS.md entirely).
Output C: 11 within-`.dev-knowledge` handoff pain points with citations; 0 evidenced cross-repo handoff pain points.

---

## Output A — Cross-Repo Prescriptions Inventory

Grep sources: `PLAYBOOK.md`, `docs/decisions/ADR-*.md`, `CLAUDE.md`, `CHANGELOG.md`.

| Prescription | Source (file:line) | Scope | Downstream repos affected | Deployment state |
|--------------|--------------------|-------|---------------------------|-----------------|
| Default branch = `main` | ADR-30 (`docs/decisions/ADR-30_default_branch_main.md:13`); PLAYBOOK:180 "Every Rob's repo uses `main`. No exceptions." | Universal — all Rob's repos | corp-monorepo, ai-council, corp-ops, corp-sca-time-automation | All 4 already show `main` in current inventory; CHANGELOG:41 and handoff:169 label corp-monorepo + ai-council "pending sprint 1" — gap between label and observed state |
| AGENTS.md per-repo (M+L) | PLAYBOOK:58 "each repo … has an `AGENTS.md` at root"; Council #28; `templates/AGENTS-md-template.md` (10-section skeleton) | Scale M + L repos | corp-monorepo (has old Codex-only file, wrong template), ai-council (absent) | Active prescription, partial deployment: corp-monorepo has `AGENTS.md` but titled "Codex Code Review Configuration" (1 line grep); ai-council NO; corp-ops (S) NO; corp-sca (S) NO |
| CLAUDE.md ≤200 lines thin pointer | PLAYBOOK:107; LESSONS.md:94 ("CLAUDE.md instruction adherence drops above 200 lines"); `templates/CLAUDE-md-template.md` | Universal — all repos with Claude Code | corp-monorepo 94 lines ✓; ai-council 233 lines **VIOLATION**; corp-ops 140 lines ✓; corp-sca 171 lines ✓ | Active prescription; ai-council violates as of this audit |
| JOURNAL.md per-repo (Scale L mandatory, M optional) | PLAYBOOK:493 "Scale L mandatory; Scale M optional; Scale S no"; `PLAYBOOK:516` Scale matrix | Scale L + M repos | corp-monorepo (L) YES ✓; ai-council (M) YES ✓; corp-ops (S) NO (correct); corp-sca (S) NO (correct) | Deployed for L+M; Scale S correctly excluded |
| Scope tag vocabulary + hybrid ≤25% ceiling | ADR-27 (`docs/decisions/ADR-27_scope-tagging.md`); CLAUDE.md:88 "Delta-rule enforcement active" | `.dev-knowledge` only — no evidence of cross-repo scope tag prescription | Pre-commit hook enforces in `.dev-knowledge`; other repos: no `validate_scope_tags.py` evidence | `.dev-knowledge`-scoped; cross-repo extension not yet prescribed |

**Prescriptions documented but not yet active (TBD placeholders):**

| Placeholder | Source | Status |
|-------------|--------|--------|
| File naming conventions | PLAYBOOK:206-211; ADR-31 reserved | Stream C session 2 — no content yet |
| Folder structure per Scale | PLAYBOOK:213-219; ADR-32 reserved | Stream C Cluster 2 — depends on Scale assessment |
| `.secrets/` path standard | PLAYBOOK:224-226; ADR-33 reserved | Stream C session 3 — no content yet |
| Capitalization conventions | PLAYBOOK:227; ADR-34 reserved | Stream C session 3 — no content yet |

---

## Output B — Repo Ecosystem Structural Overview

Filesystem inventory run 2026-04-27 via `ls` + `wc -l` across 5 repos.

| Repo | Scale (per Rob) | CLAUDE.md lines | AGENTS.md | JOURNAL.md | ADR count | Handoffs count | Branch | Compliance gaps |
|------|-----------------|-----------------|-----------|------------|-----------|----------------|--------|-----------------|
| `.dev-knowledge` | M (L boundary) | ~120 (est) | NO (pending session 6 scope decision) | YES | 4 (ADR-27–30) | 6 | main ✓ | None vs current prescriptions |
| corp-monorepo | L | 94 ✓ | YES — but Codex-only template ("AGENTS.md — Codex Code Review Configuration", 130 lines) | YES | 29 | 1 | main | AGENTS.md wrong template: Codex-only vs 10-section governance contract |
| ai-council | M | **233 ❌** (violates ≤200) | NO | YES | 6 | 1 | main | AGENTS.md absent (Scale M — required per current Gap #6 scope); CLAUDE.md overlength |
| corp-ops | S | 140 ✓ | NO | NO | 0 | 0 | main | None vs current prescriptions (Scale S correctly excluded from AGENTS.md + JOURNAL) |
| corp-sca-time-automation | S | 171 ✓ | NO | NO | 0 | 1 | main | None vs current prescriptions (Scale S) |

**Divergence patterns visible from inventory:**

- corp-monorepo has `docs/` subfolders: `ARCHITECTURE.md, archive, audits, decisions, diagrams, HANDOFF.md, handoffs` — richest structure, organic growth
- ai-council has `docs/`: `archive, COUNCIL_QUESTION_GUIDE.md, decisions, HANDOFF.md, handoffs` — partial structure
- corp-ops and corp-sca: no `docs/` ADR or handoff subfolders — minimal governance
- Branch label gap: CHANGELOG:41 and handoff pending items 8-9 mark corp-monorepo + ai-council branch renames as "Stream C sprint 1 pending" yet both show `main` today — status ambiguous (prior rename, or label not updated)
- `.dev-knowledge` has 2 `HANDOFF.md` root files in other repos (corp-monorepo, ai-council) in addition to the `docs/handoffs/` convention — naming divergence

---

## Output C — Handoff Pain Points Catalog

### Within-`.dev-knowledge` handoff pain (Stream C session 1 + last 2 transitions)

Sources: `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md` (primary); `docs/handoffs/2026-04-26-stream-b-complete-stream-c-scope.md`; `LESSONS.md`.

| # | Pain | Evidence (file:line) | Frequency | Severity |
|---|------|----------------------|-----------|----------|
| 1 | Audit hallucination — fabricated specific file metrics ("1019 lines" for non-existent file in N1 finding) | LESSONS.md:178 | Single session 2026-04-27: 1 confirmed incident | HIGH |
| 2 | False PENDING claim — governance verification failure (artifact claimed present without filesystem check) | LESSONS.md:182 "third governance failure in single session" | 3 failures in one session 2026-04-27 | HIGH |
| 3 | JOURNAL spec miss — proposing artifact creation without searching existing governance spec for same artifact name | LESSONS.md:182 | Same session; root cause shared with #1, #2: cached assumption without verification | HIGH |
| 4 | Scope creep post-merge — items 13-20 added as "bonus scope" after ADR-30 wrapped (ESSENTIALS refactor, ADR template, vocabulary check, LESSONS format reconciliation) | handoff:183-218 (items 13-20 labeled "From Stream C session 1 execution feedback — added post-merge") | Recurring pattern across sessions (see also LESSONS.md:139 "scope creep flagging — real-time detection vs post-hoc") | MEDIUM |
| 5 | Handoff artifact skipped during execution — Artifact 1 (commit handoff doc) was Krok 2, skipped en route to Krok 3; discovered only at session wrap when Claude Code couldn't find file | handoff:265 | At least 1 confirmed incident per session 1 | MEDIUM |
| 6 | Mechanical tasks bundled into browser session — lesson promotion bundled into session 1; Rob caught and forced standalone Claude Code task | handoff:242 "Pre-work extraction was Rob's intervention, not browser-side proactivity" | Recurring (LESSONS.md:139 references session boundary violations) | MEDIUM |
| 7 | Bottom-up planning default — jumped to "plan item 1" instead of "plan full stream, then zoom"; Rob redirected | handoff:244 "jumped to 'rozpisz plan dla item 1' instead of full stream plan" | Session 1; pattern expected to recur | MEDIUM |
| 8 | Session boundary violation — ~13h active in Stream B across 2026-04-24/25/26 | handoff-B:164 | Stream B final session; noted as risk that didn't become defect | LOW |
| 9 | Recursive planning anti-pattern — Stream B; caught only by Rob's pushback, not browser self-detection | handoff-B:165 | Stream B; detection mechanism = human judgment, no automated guard | LOW |
| 10 | Documentation drift undetected during session — Gap #7d v1.0 caught next day | handoff-B:167 | Stream B; pattern addressed by LESSONS.md:178 counter-pattern | LOW |
| 11 | HANDOFF_PROCESS v1.0 specification without full-cycle dogfooding — 3-artifact need discovered mid-handoff generation | handoff-B:173 | Stream B → C transition; corrected in v1.1 | LOW (resolved) |

### Cross-repo handoff pain (evidence-required)

No evidence found in `.dev-knowledge` handoffs, audits, or LESSONS.md for cross-repo handoff pain (browser → corp-monorepo Claude Code transitions or similar).

**Confirmed structural gap** (not invented pain): `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md:385` states "pointer to ai-council: currently nowhere" — cross-repo context linkage absent but not yet attempted as workflow. Stream C Cluster 3 item 11 ("Browser ↔ Claude Code in different repo handoff") acknowledges this as future work (`handoff-B:128`), confirming the protocol doesn't exist rather than that pain has been experienced and undocumented.

---

## What was NOT audited (out of scope)

- Solutions or recommendations — Council debate territory
- Code or implementation files of other repos — governance docs only
- LESSONS.md content edits — append-only
- Pain points without concrete evidence
- Handoff history beyond last 2 transitions (`2026-04-26-stream-b-*` and `2026-04-26-stream-c-session-1-*`)
- ADR files in other repos (their internal decisions, not `.dev-knowledge` prescriptions)
- `illustrated-book-gen` and `terminal-setup` repos — not referenced as part of Rob's active ecosystem in any `.dev-knowledge` source
