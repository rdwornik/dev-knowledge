---
type: audit
scope: BACKLOG audit + universalization scoping post session 2026-05-23/24
date: 2026-05-24
auditor: Claude (Opus) via .dev-knowledge browser-chat session
status: immutable (after this prompt merges)
basis-inputs: [BACKLOG.md, git log since 2026-05-22, docs/audits/2026-05-24-dev-knowledge-self-audit.md, docs/audits/2026-05-23-ecosystem-audit.md, LESSONS.md, JOURNAL.md 2026-05-24, protocols/PLAYBOOK.md §5, operator focus areas 2026-05-24]
---

# BACKLOG Audit + Universalization Scoping — 2026-05-24

Comprehensive audit of `BACKLOG.md` against (a) the 2026-05-22 → 2026-05-24 session
arc outcomes, (b) three operator-identified focus areas (hooks workflow, skill
review, AI Council pipeline), and (c) universalization-readiness for the upcoming
corp-monorepo dedicated session. Produces this immutable report; BACKLOG edits follow
in subsequent commits per the audit's §6 proposal.

## 1. Audit scope + methodology

**In scope:** read-only audit of every `BACKLOG.md` entry; categorization; focus-area
gap analysis; universalization-readiness gap analysis; prioritization recommendation.
BACKLOG edits (close/reword/add/reprioritize) are applied in follow-up commits.

**Out of scope:** any change to workflow files (PLAYBOOK / ESSENTIALS / ADRs /
templates) — those are execution items the prioritization recommendation feeds, not
this audit. Zero child-repo modifications. No new folders.

**Categories applied to each entry:** CLOSED-BY-TODAY (work landed in the 2026-05-22+
window), CLOSED (resolved in current state, bookkeeping lag from before the window),
STALE (references a retired concept/removed artifact), SUPERSEDED (intent now met by a
different mechanism), STILL-OPEN-CORRECT, OPEN-NEEDS-PRIORITY-ADJUSTMENT.

**Verification discipline:** every closure claim was checked against live repo state
(file existence, grep, pytest), not against commit names — per the 2026-05-24
verify-before-claiming and premature-closure LESSONS. file:line / command evidence is
cited inline.

## 2. BACKLOG state pre-audit

Counts from `BACKLOG.md` as read this session (excludes stream placeholders + section
headers):

| Dimension | Breakdown |
|---|---|
| By stream | A: 0 · B: 2 · C: 16 · D: 0 · Cross-stream: 18 · Naming/Arch migration: 5 · Hyphen migration: 6 · Tier-deprecation rollout: 5 |
| By priority | P1: 5 · P2: 24 · P3: 23 |
| By status | open: 40 · closed: 2 · resolved: 2 · superseded: 4 |

(Total entries ≈ 48 across all sections. "Cross-stream / Ecosystem" holds 18 entries —
this is the section the existing taxonomy-grooming entry flags as over the ADR-47 33%
kill criterion; this audit's closures reduce the open count but do not by themselves
re-route the taxonomy.)

## 3. Audit findings by category

### CLOSED-BY-TODAY (1) — landed in the 2026-05-22+ window

- **`scripts/backlog_extract.py` references deleted BACKLOG_ARCHIVE.md** (Stream C, P2).
  The entire script + its tests were retired in commit `a5ed940` (2026-05-22
  drift-burndown, audit X1/M-4). Verified: `scripts/backlog_extract.py` does not exist.
  The drift the entry describes (script would recreate a forbidden file) is eliminated.
  → **close.**

### CLOSED (3) — resolved in current state; BACKLOG bookkeeping lag

These landed in the 2026-05-20 posture-audit-verification quick-wins (commit `dc46565`),
*before* the 2026-05-22 window, but the entries were never marked closed.

- **`scripts/migrate_links.py` SKIP_NAMES references deleted CHANGELOG.md** (Stream C, P3).
  Verified `scripts/migrate_links.py:4` now reads `{'JOURNAL.md', 'LESSONS.md',
  'TOKEN-LOG.md'}` — no CHANGELOG. → **close.**
- **`docs/decisions/README.md` ADR Index missing ADRs 45-50 and 54** (Stream C, P2).
  Verified the index now lists ADR-45 through ADR-50 and ADR-54; and
  `ARCHITECTURE.md:168` lists ADR-54 in Governing ADRs. Both sub-claims resolved.
  → **close.**
- **Fix pre-existing test failure: `test_ratio_pass_when_stable_above_ceiling`** (Hyphen
  migration, P2). Verified `pytest -q` → 72 passed; `pytest -k
  test_ratio_pass_when_stable_above_ceiling` → 72 deselected (test no longer present in
  the suite). The entry's intent ("clean `pytest -x`") is satisfied. *Caveat:* I cannot
  confirm whether the underlying ratio logic was fixed vs the test removed during the
  backlog_extract retirement; the closure is on the stated intent (green suite), noted as
  a judgment call. → **close with caveat.**

### STALE (2) — reference a retired concept / removed artifact

- **Audit tool: `check_backlog_organization` code-span-aware done-token regex** (Stream C,
  P2). Verified: `grep -rn check_backlog_organization scripts/` returns nothing — the
  check was removed when ADR-48 withdrew ADR-46/47 audit enforcement (ADR-47 "retained as
  convention, NOT audit-enforced"). The false-positive the entry seeks to fix cannot
  occur without the check. → **close as moot** (enforcement withdrawn, ADR-48).
- **ADR-39 registry decision — 5 unregistered template files** (Stream C, P3). The entry
  names `templates/AGENTS-md-template.md` as one of the five; verified it no longer exists
  (retired with AGENTS.md under ADR-53). The other named files exist
  (`CLAUDE-md-template.md`, `codex-review-config-template.md`, `prompt-template.md`), and
  the template inventory has since grown (HANDOFF_*, ARCHITECTURE-template, ADR-template,
  scrum-master-cover-letter, workspace-*). The *core decision* (do templates need ADR-39
  registry entries, or a class exemption?) remains valid. → **reword** (drop the dead
  AGENTS-md-template reference; restate the open decision against the current template set;
  keep open).

### SUPERSEDED (1)

- **Ecosystem standards audit against major repo** (Cross-stream, P2). The entry asked to
  "audit one significant ecosystem repo against current standards … establish this as a
  repeatable pattern." Both halves are now delivered: the 2026-05-23 corp-monorepo deep
  audit + ecosystem audit are the concrete instance, and the scrum-master review authority
  pattern (N=3) *is* the repeatable mechanism. → **mark superseded** by the scrum-master
  review entry; preserve for history.

### OPEN-NEEDS-PRIORITY-ADJUSTMENT (2)

- **Codify scrum-master review authority pattern** (Cross-stream, currently P2). The entry
  body already states "N=3 grounding reached (codification now unblocked) … Promote to P1
  for a dedicated codification prompt." N=3 confirmed (ai-council 2026-05-12; corp-monorepo
  2026-05-23; ai-council re-pass 2026-05-23). This is **universalization-relevant** — child
  repos need a formal authority reference for the review they receive. → **P2 → P1.**
- **Apply scrum-master review pattern to other child repos** (Cross-stream, P3). Body says
  "blocked on codification + N=2 empirical grounding." Both lifted: N=3 reached and
  corp-monorepo already reviewed. → **status update** (unblock; keep P3 — it follows
  codification, which is the new P1).

### Dangling-supersession repair (1)

- **Council CLI dual-write trigger logic** (Stream C, P3, [superseded]). Its supersession
  note points to "Cross-stream P1 'AI Council cross-project transcript routing'" — but that
  entry **does not exist** in BACKLOG (verified by grep: only the back-reference at line 78
  + PLAYBOOK §5:1535 point to it). The superseder was lost. → **restore** the
  transcript-routing entry (see §4.3) so the supersession resolves to a real target.

### STILL-OPEN-CORRECT (remaining)

All other open entries remain valid and current, including: Lessons activation P1 (ADR-35);
ESSENTIALS cheat-sheet additions for ADRs 35-54; the two ADR-39/41 grouped amendments;
LESSONS parenthetical-regex; ADR relationship/supersession graph; Phase 2 universalization
rollout (umbrella); Handoff advisory-framing leak; Cross-repo audit (Phase 3); Council
decisions management consolidation (P1, partial — index done, contradiction-detection +
ownership-model remain); Sacred-files maintenance enforcement (P1); Skills universalization;
Kimi K2; VS Code productivity; Pinned Files extension; the handoff-format/naming migration
entries; CI hyphen enforcement; corp-monorepo & ai-council hyphen+ADR-38 remainders;
content-scoped archival principle; and the five Tier-Deprecation + Root-Hygiene rollout
items.

**Already-terminal (no change, historical record):** AGENTS.md ai-council [closed]; ADR-38
self-compliance [resolved]; ADR-29 prepend amendment [superseded]; Codemap generator
[closed]; VISION tier declarations [superseded]; Council research relative-complexity
[superseded]; Scale tier re-evaluation [resolved].

## 4. Focus area gap analysis

### 4.1 Hooks workflow / goals usage — PARTIAL (scope-expand existing entry)

Existing entry **Hooks audit + consolidation** (Cross-stream, P2) covers *inventory +
consolidation* of hooks (the "two review hooks" observation). The operator's framing is
broader: *how are lifecycle hooks (SessionStart, SessionStop, pre-commit) used for
workflow automation, and where should usage expand?* Current `.dev-knowledge` hook surface
(verified): two pre-commit hooks (`normalize-dated-headers`, `codemap-freshness`); a
SessionStart EVOLUTION hook (observed in this session's startup reminder); no SessionStop
hook. The existing entry does not capture the automation-patterns/expansion angle.
→ **Recommendation:** expand the existing entry's scope (add a sub-bullet for lifecycle-hook
workflow patterns + expansion opportunities); do **not** create a duplicate.

### 4.2 Skill review — ALREADY COVERED

Existing entry **Skills universalization across repos** (Cross-stream, P2) already covers
the operator's ask: inventory all skills, classify repo-specific vs cross-ecosystem,
identify universalization targets, propose a canonical location (promotion to
`~/.claude/skills/`). No new entry needed. → **no change** (note the coverage in the entry
is sufficient).

### 4.3 AI Council pipeline — PREMISE REFUTED; one real gap

The prompt framed the AI Council pipeline as "informal/ad-hoc … GAP needs formalization."
**Verification refutes this.** PLAYBOOK §5 ("Running an AI Council Debate", `:1426`+)
documents the full pipeline end-to-end:

- **Trigger conditions** — "When to use Council vs decide yourself" + "Gate Council to
  ADR-worthy decisions" (architectural impact / multi-ADR ripple / reversal cost > 1h).
- **Debate question format** — frontmatter + Question/Current-State/Questions/Constraints
  schema, with rules and length bounds.
- **Running the debate** — `council-cli` invocation.
- **Post-debate → ADR flow** — binding decision; *mandatory automated* ADR creation
  (verify next ADR number, align to template, write `docs/decisions/ADR-NN-topic.md`,
  commit); archive transcript; add ADR row + traceability to `docs/decisions/README.md`.
- **Archival protocol + return-to-chat** — 3-step pipeline; browser drafts content,
  Claude Code commits; source of truth `ai-council/output/`.

So there is **no "define the pipeline" gap** to scope; adding such an entry would
duplicate existing documentation (failure-mode #2). The **one genuine gap** is the missing
**AI Council cross-project transcript routing** entry — referenced as a live P1 by both the
superseded dual-write item and PLAYBOOK §5:1535, but absent from BACKLOG. Its scope:
choose the mechanism (push-frontmatter vs pull-command vs config-based) for routing Council
output from `ai-council/output/` to the relevant project's transcripts/research folder.
→ **Recommendation:** restore this entry (P2, Stream C) — this also repairs the dangling
supersession in §3. The optional "consolidate the pipeline into one named reference for
universalization" concern is already subsumed by the **Council decisions management
consolidation** P1 entry; no separate entry.

## 5. Universalization-readiness gap analysis

Question posed: *for the corp-monorepo dedicated session to mirror `.dev-knowledge`'s
universalization patterns, is every reference it must read present + current?*

| Reference need | State in `.dev-knowledge` | Verdict |
|---|---|---|
| Amended ADRs (33/38/40/51) | Merged (reconciliation 427f9a6) | Ready ✓ |
| Audit governance baseline | `check_adr38_baseline` governance-docs-only | Ready ✓ |
| ARCHITECTURE template | CORE tags + Mermaid; tier tags stripped | Ready ✓ |
| Codemap generator | Built + dogfooded; pre-commit freshness hook | Ready ✓ |
| Layer-model exemplar | Embedded Mermaid in own ARCHITECTURE.md | Ready ✓ |
| Root-hygiene convention | PLAYBOOK section (expanded pass 2) | Ready ✓ |
| Self-audit clean reference | 2026-05-24 self-audit merged (6cde07b) | Ready ✓ |
| Scrum-master review pattern | N=3; **not yet ADR-codified** | Gap → bump codification to P1 |
| AI Council pipeline | Documented PLAYBOOK §5 | Ready ✓ (premise refuted) |
| Transcript-routing entry | **Missing from BACKLOG** | Gap → restore entry |
| Hooks workflow patterns | Implicit | Minor gap (P2; non-blocking) |
| BACKLOG taxonomy hygiene | Cross-stream still > 33% | Partial (deferred to quarterly) |

**Conclusion:** `.dev-knowledge` is substantially ready as the clean reference (the
self-audit already certified internal consistency of VISION/ARCHITECTURE/CLAUDE/PLAYBOOK).
The only universalization-*blocking* gap is **scrum-master review codification** — child
repos receiving a review need a formal authority reference. The tier-deprecation rollout
items (corp-monorepo + ai-council, both verified genuinely open: corp-monorepo VISION still
carries `tier: standard`/`scale: L`; ai-council VISION carries `tier: M`/`scale: M` and is
missing `status:`) *are* the rollout work, already correctly P1. No new universalization
entries needed beyond the transcript-routing restoration and the codification bump.

## 6. Proposed BACKLOG updates (executed in follow-up commits)

**6a — close (CLOSED-BY-TODAY + CLOSED):** backlog_extract.py entry; migrate_links.py
entry; ADR-README-index entry; test_ratio_pass entry. Set `[closed]`, add closure
reference (commit + this audit).

**6b — stale cleanup:** `check_backlog_organization` entry → close-as-moot (ADR-48);
ADR-39-template-registry entry → reword (drop AGENTS-md-template, restate against current
template set, keep open); Ecosystem-standards-audit entry → mark superseded by
scrum-master pattern.

**6c — focus-area:** expand Hooks audit + consolidation entry scope (lifecycle-hook
workflow patterns + expansion); no change to Skills entry (already sufficient); no new
AI-Council "define pipeline" entry (premise refuted).

**6d — universalization / restore:** add **AI Council cross-project transcript routing**
(P2, Stream C) — repairs the dangling supersession + PLAYBOOK §5 reference. Add small P3
**CLAUDE.md §4 cites a stale known-failing test** entry (`test_audit_run_passes_structural
_checks_on_synthetic_repo` is cited as a known failure but passes; tracked as drift, fix is
a one-line CLAUDE.md edit = execution, not this prompt).

**6e — priority adjustments:** Codify scrum-master review authority → P1; Apply
scrum-master pattern to other child repos → status update (unblocked).

## 7. Prioritization recommendation — next execution wave

**Immediate (P1) — blocking / enabling universalization:**
1. **Codify scrum-master review authority pattern** (new ADR or ADR-26 amendment) — N=3
   grounding; gives child-repo reviews a formal authority reference. *First, because the
   rollout sessions invoke this pattern.*
2. **Apply tier-deprecation to corp-monorepo** (P1, verified open) — VISION/ARCHITECTURE
   frontmatter still carries tier/scale.
3. **Apply tier-deprecation to ai-council** (P1, verified open) — tier/scale present;
   `status:` missing (audit WARN).
4. **Council decisions management consolidation** — remaining sub-items (contradiction
   detection + ownership model); pairs with the ADR relationship/supersession graph (P3).

**Soon (P2) — improve universalization quality:**
- Restore + resolve **AI Council cross-project transcript routing** (mechanism choice).
- **Root hygiene** application — corp-monorepo + ai-council.
- **README disposition** decision per child repo.
- **Hooks workflow patterns** (expanded scope) + **Skills universalization**.
- corp-monorepo + ai-council **hyphen migration** remainders; **CI hyphen enforcement**.

**Future (P3) — captured, not blocking:**
- ADR relationship/supersession graph; Undiscovered-repos confirmation; Sacred-files
  enforcement mechanism; content-scoped archival codification; PLAYBOOK posture-audit
  codifications; Kimi K2 evaluation; VS Code productivity + Pinned Files extension; large
  repo migration; ESSENTIALS cheat-sheet additions; LESSONS parenthetical regex; ADR-39/41
  grouped amendments; ADR-42 single-vs-multi handoff clarification.

## 8. Open questions / judgment calls

- **OQ-1 (test closure):** `test_ratio_pass_when_stable_above_ceiling` is absent and the
  suite is green; closed on stated intent. Whether the ratio logic was fixed or the test
  removed is unverified — flagged, not blocking. Operator may want a root-cause note.
- **OQ-2 (CLAUDE.md stale test ref):** CLAUDE.md §4 still cites
  `test_audit_run_passes_structural_checks_on_synthetic_repo` as a "known pre-existing
  failure," but it passes. Added as a P3 BACKLOG entry rather than edited here (CLAUDE.md
  is a workflow file, out of this prompt's scope). Operator confirms the fix lands in a
  follow-up.
- **OQ-3 (Ecosystem-standards-audit supersession):** marked superseded by the scrum-master
  pattern on the judgment that the deep audits delivered the concrete instance and the
  pattern is the repeatable mechanism the entry wanted. If the operator reads the entry as
  demanding a *checklist-style* standards audit distinct from the scrum-master review, it
  should revert to open.
- **OQ-4 (Hooks scope-expand vs new entry):** chose to expand the existing Hooks entry
  rather than add a parallel one, to avoid two overlapping hooks entries. If the operator
  prefers the inventory and the workflow-patterns work tracked separately, split them.
