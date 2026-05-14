# Journal — .dev-knowledge

<!-- scope: meta -->

> Per-session tactical log of `.dev-knowledge` Claude Code work. Did/Failed/Next
> entry shape per PLAYBOOK Stream B Gap #4 spec, newest-first prepend ordering
> per PLAYBOOK Documentation file types v1.1 amendment (2026-04-27).
>
> Distinct from CHANGELOG (per-commit notable changes), LESSONS (per-learning
> generalized rules, oldest-top per ADR-29), and handoffs (per-session boundary
> artifacts for browser-chat resumption): JOURNAL is the within-Claude-Code-
> sessions tactical log enabling context recovery across sessions in same repo.
>
> Update protocol: prepend new session entry at top of entry list (under this
> intro blockquote, before existing entries). One entry per Claude Code session
> OR per workday for heavy days. Each entry cites commit hashes, handoff doc,
> or ADR for deeper detail. JOURNAL summarizes, doesn't duplicate.

---

### 2026-05-14 — Same-day LESSONS canonical rewrite + top relocation
- Same-day LESSONS correction: 9 entries rewritten to canonical 6-field schema, moved from tail to top of dated-entries section
- Surfaced by operator's empirical observation that opening LESSONS.md showed pre-existing 2026-04-21 entry at top — visibility convention need
- ADR-29 ordering amendment deferred to BACKLOG Stream C P2; going-forward formalization is its own scope

### 2026-05-14 — Closed Stream C P1: PLAYBOOK additions for ADRs 36/37/40/41
- Closed Stream C P1 methodology debt: new §10 BACKLOG Grooming (ADR-41), new §18 Ecosystem Audit Tool (ADR-36), §8 amended for ADR-37 two-phase protocol, Project Scale Tiers extended with ADR-40 tier transitions; §10–17 renumbered to §11–17+§19
- Verification: scope tags pass, hybrid ≤25%, BACKLOG Stream C P1 marked [done], 9 cross-ref hits updated in 4 living files

### 2026-05-14 — Interleaved capture: 9th LESSON + BACKLOG v3.3.2 entry
- Interleaved capture: 9th LESSON (`universal-without-cross-case-verification`) + BACKLOG entry for v3.3.2 template fix
- Both bugs witnessed during parallel ai-council Stage 3 generation; template fix deferred per Hard Constraint #3 (Option B over Option A)
- Operator mitigation: no new cross-repo handoffs until v3.3.2 ships

### 2026-05-14 — Append 8 architect-discipline LESSONS entries
- Appended 8 architect-discipline LESSONS entries (5 primary + 3 secondary) from extended-session observations
- Source: docs/handoffs/2026-05-14-dev-knowledge-session-sync/06_STATE_OF_PLAY.md "Work in progress not yet captured"
- Action: captured for review; promotion to ESSENTIALS invariants deferred to operator decision

### 2026-05-14 — Handoff Stage 3 complete for ai-council (session-sync)
- Handoff Stage 3 complete for `2026-05-14-ai-council-session-sync`: 11-file bundle at `docs/handoffs/2026-05-14-ai-council-session-sync/`; Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-ai-council-session-sync/`
- Stage 3 verification: 8 witnessed claims verified, 0 contradictions; 4 architect inferences preserved; 0 unknowns
- No SHA drift (Stage 1 and Stage 3 both captured HEAD `0f069554`)
- Next: open NEW claude.ai chat; upload 11-file bundle; paste 00_first-message.md; confirm `role confirmed` then `synthesis confirmed`

### 2026-05-14 — Handoff Stage 1 generated for ai-council (session-sync)
- Handoff Stage 1 generated for `2026-05-14-ai-council-session-sync`: HEAD `0f069554b894802504aa4e5ce140b1d481ae9ec8` captured; awaiting Stage 2

### 2026-05-14 — Handoff Stage 3 complete (session-sync, v3.3.1)
- Handoff Stage 3 complete for `2026-05-14-dev-knowledge-session-sync`: 11-file bundle at `docs/handoffs/2026-05-14-dev-knowledge-session-sync/`; Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-dev-knowledge-session-sync/`
- Stage 3 verification: 7 witnessed claims verified, 0 contradictions; ESSENTIALS.md line count resolved (323 lines — architect had flagged Unknown)
- SHA drift (8663a7c → ef7f66e) confirmed as expected (Stage 1 commit itself); operator approved proceed
- Next: open NEW claude.ai chat; upload 11-file bundle; paste 00_first-message.md; assess v3.3.1 articulation gate empirically

### 2026-05-14 — Handoff Stage 1 generated (v3.3.1) + v3.3.1 amendment
- Handoff Stage 1 regenerated under v3.3.1 for `2026-05-14-dev-knowledge-session-sync`: HEAD `8663a7c` captured; awaiting Stage 2
- Handoff v3.3.1 amendment landed: audience-awareness rules in
  HANDOFF_QUESTION_TEMPLATE.md. Empirical trigger — 2026-05-14
  self-review of Stage 2 response under v3.3 surfaced 7 patterns
  that confuse new chat (which never sees Stage 1). v3.3 had
  explicitly excluded Stage 1 template from refinement scope; that
  was a scope error. v3.3.1 fixes the upstream template so future
  Stage 2 responses naturally exhibit audience awareness without
  manual downstream patching. AI Council research transcript
  (docs/decisions/transcripts/, separate commit) provides
  concept-level reinforcement with documented caveats about
  hallucinated citations and question-framing bias.

### 2026-05-13 — Handoff v3.3 minimum-viable refinement
- Did: handoff v3.3 minimum-viable refinement landed: audit-validated language
  fixes in 06/07 (plain-English section names, code glosses, Hard Constraints /
  Narrow Scope split, verb-led sentences) + mandatory articulation gate in
  00_first-message. Empirical trigger — 2026-05-13 browser session (5+ hours)
  showed architect had VISION in bundle but did not internalize; operator
  uploaded VISION twice during session. Refinement is template/process-level;
  ADR-42 v3 flow + file count + responsibilities preserved. ADR-45 v1
  superseded (v2 rewrite deferred). Sequential loading + question battery
  deferred pending empirical test of minimum.
- Failed: —
- Next: generate handoff from 2026-05-13 browser session using new v3.3 format;
  empirically test articulation gate; measure against baseline

### 2026-05-13 — Four additional 2026-05-12/13 lessons promoted to ESSENTIALS invariants
- Did: promoted LESSONS #1 (epistemic markers), #2 (completion verification), #6 (validation routing), #8 (artifact-direction) to ESSENTIALS as invariant architect rules; each as own commit for revertability; rule bodies preserved verbatim
- Failed: —
- Next: implementation prompts for ADR-45 — shared validator script first

### 2026-05-13 — ESSENTIALS architect channel-discipline rule documented
- Did: moved channel-discipline rule from LESSONS #10 into ESSENTIALS so it loads as invariant at browser-chat session start per ADR-45 architect-compliance path; PLAYBOOK cross-reference skipped (no matching section exists)
- Failed: —
- Next: implementation prompts for ADR-45 (shared validator first, then hooks, templates, sync-script, dry-run, pilot)

### 2026-05-13 — ADR-45 handoff architecture v4 accepted; session lessons archived
- Did: drafted ADR-45 codifying invariant/session separation + 2-file handoff + defense-in-depth enforcement (grounded in Council research debate `council-out-20260513_102702-...` + pick debate `council-out-20260513_111424-...` + audit `docs/audits/2026-05-12-handoff-process-audit.md`); appended 10 methodology lessons to LESSONS.md; flipped ADR-45 status to Accepted; merged to main with --no-ff
- Failed: architect (browser chat) wrote inline git ops in review approval message; surfaced as 10th lesson (channel-discipline) and folded into this session
- Next: implementation prompts in this order — (1) shared validator script `.dev-knowledge/scripts/validator.py`, (2) MANIFEST + NEXT templates with schemas, (3) session-boundary semantics, (4) three enforcement hooks (git pre-commit + Claude Code PreToolUse + `/save`) calling shared validator, (5) sync-script for @path fallback, (6) bootstrap dry-run on throwaway repo, (7) pilot on `.dev-knowledge` for 2 weeks, (8) gate check, (9) fleet rollout one-at-a-time. Also: ESSENTIALS.md update to document architect channel-discipline rule from lesson #10

### 2026-05-12 — Handoff process audit
- Did: read process spec + templates + slash commands + sample artifacts (current + archive + legacy); wrote audit report describing the process end-to-end in plain prose at `docs/audits/2026-05-12-handoff-process-audit.md`
- Failed: —
- Next: browser chat reads audit, proposes improvements (conversational rethink or Council debate, depending on findings depth)

## 2026-05-12 — Inline reminder questions added to Stage 1 questionnaire
- Did: added brief reminder block at end of Stage 1 questionnaire flow surfacing cross-repo + internal-coherence check categories with explicit pointer to HANDOFF_PROCESS Universal Self-Containment Rule as source of truth
- Result: defense-in-depth for handoff lifecycle achieved without sync drift risk — master rule single source; questionnaire surfaces awareness at moment of writing
- Next: continued testing of fresh handoff generation; observe whether reminder reduces residual failure modes

### 2026-05-12 — Residual logging (LESSON + BACKLOG)
- Did: appended methodology LESSON on name-conflict audit framing; added P2 BACKLOG entry for pre-existing test_ratio_pass_when_stable_above_ceiling failure
- Failed: —
- Next: residual handoff items (skills review, token log analysis) remain as separate-session candidates

### 2026-05-12 — Hooks review proper (/review → /codex-review)
- Did: renamed user-defined slash command `/review` → `/codex-review` (resolves shadow collision with Claude Code built-in PR review skill); updated PLAYBOOK § 15 and ESSENTIALS step 3 Codex-wrapper references; produced resolution audit note with pre-rename shadowing observation (both registered simultaneously, disambiguation scenario); merged `chore/2026-05-12-resolve-review-conflict` to main
- Failed: —
- Next: residual handoff items (BACKLOG grooming, token log, skills review) — separate scope

## 2026-05-12 — Universal handoff self-containment rule added to HANDOFF_PROCESS
- Did: added Universal Self-Containment Rule section to HANDOFF_PROCESS.md covering Stage 1 packaging / Stage 2 generation / Stage 3 reception with per-section scope rules + pre-send coherence checklist + ADR-41 per-repo scope reference; appended LESSON capturing empirical failure observed in session as universal pattern (not repo-specific)
- Result: handoff process rule now universal across all repos handoff lifecycles; structurally prevents repeating cross-repo-in-DIRECTIVES failure in any future handoff (corp-monorepo, ai-council, future child repos)
- Next: BACKLOG cross-repo contamination cleanup (separate concern; operator-confirmed scope only)

## 2026-05-12 — Hooks reconnaissance + ai-council check
- Did: produced docs/audits/2026-05-12-hooks-discovery.md; identified review name-conflict location(s) — user-defined `~/.claude/commands/review.md` (Codex wrapper) vs. Claude Code built-in `/review` skill (PR review); recommended Shape (a) for Prompt 4; confirmed ai-council implemented all 10 scrum-master findings + I7/I8 addendum + council-out-* emitter rename
- Failed: —
- Next: hooks review proper (Prompt 4) — scope locked by recon findings (Shape a, low effort)

## 2026-05-12 — PLAYBOOK § 17 + cover-letter template
- Did: added § 17 Scrum-Master Review Propagation + templates/scrum-master-cover-letter.md; closed BACKLOG P2 propagation-structuring entry
- Failed: —
- Next: hooks reconnaissance (Prompt 3) → hooks review proper (Prompt 4, scope locked by recon findings)

## 2026-05-12 — Cleanup pass
- Did: resolved orphaned 2026-05-12-session-handoff deletion (D2 — already committed as 471ecd3); marked ADR-34 ai-council propagation BACKLOG entry as done (D3); added ADR-42 single-vs-multi-artifact amendment-candidate BACKLOG entry P3 (D7)
- Failed: —
- Next: PLAYBOOK § 17 + scrum-master cover-letter template (Prompt 2)

## 2026-05-12 — Handoff Stage 3 complete for ai-council (session-sync)

**Did:** Stage 3 generated 12-file handoff folder at `docs/handoffs/2026-05-12-ai-council-session-sync/`. Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-12-ai-council-session-sync/`. HEAD `f094d08` pinned (no drift). Stage 2 architect knowledge preserved: Step 5 smoke test as next action, cost-optimization principle captured, 12 witnessed claims verified against repo state, stale BACKLOG items flagged. BACKLOG items updated.

---

## 2026-05-12 — Handoff Stage 1 generated for ai-council (session-sync)

- Handoff Stage 1 generated for `2026-05-12-ai-council-session-sync`: HEAD `f094d0821a279f3aa36de554943c1b44576d0924` captured; awaiting Stage 2

---

## 2026-05-12 — Handoff Stage 3 complete for dev-knowledge (session-sync)

**Did:** Stage 3 generated 11-file handoff folder at `docs/handoffs/2026-05-12-dev-knowledge-session-sync/`. Stage 1+2 inputs archived. HEAD `0125f1b` pinned. Stage 2 architect knowledge (10 boundaries, 8 directives) captured. CHANGELOG updated.

---

## 2026-05-12 — Handoff Stage 1 generated for dev-knowledge (session-sync)

**Did:** Handoff Stage 1 generated for slug `2026-05-12-dev-knowledge-session-sync`; HEAD `ec44148` captured; awaiting Stage 2 (old chat response).

---

## 2026-05-12 — Prompt N: Session handoff generated

**Did:** Composed session handoff at `docs/handoffs/2026-05-12-session-handoff/` covering session scope (14 commits, 7 prompt cycles), state at end, operator pending actions, deferred substantive work, and critical process principles. Verified browser-provided inventory against repo state; flagged one adjusted item (`2026-05-11-cross-repo-pattern-audit.md` not found in `docs/audits/` — browser claim adjusted).

**Result:** Fresh-session context primer ready (49 lines); next chat reads handoff as session-start input.

**Next:** Fresh session picks up handoff; substantive work (skills review + hooks audit + token logging + methodology proposal review + Phase 2 cross-repo migrations) starts with clean context.

---

## 2026-05-12 — Prompt M: Governance freshness audit + targeted updates

**Did:** Read-audited 8 governance files (ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, README.md, VISION.md, PLAYBOOK.md, ESSENTIALS.md, HANDOFF_PROCESS.md) plus subdirectory READMEs for stale convention references post 2026-05-11 amendments (ADR-34 universal hyphen mandate + ADR-38 ARCHITECTURE.md root placement + A2 archive folder rename). Applied 10 targeted fixes across 4 files (ARCHITECTURE.md × 2, CONTRIBUTING.md × 2, README.md × 2, PLAYBOOK.md × 4). Added 1 new BACKLOG entry (Cross-stream P2: scrum-master review propagation process codification).

**Result:** Governance docs aligned with ratified amendments; all `ADR-NN_` underscore prescription references updated to `ADR-NN-` hyphen; PLAYBOOK §File naming conventions TBD block replaced with ADR-34 pointer; archival step filenames updated to council-out-* format. VISION.md, ESSENTIALS.md, HANDOFF_PROCESS.md, CLAUDE.md — no stale references found.

**Next:** Handoff to fresh session for substantial new scope (skills review + hooks review + token logging + methodology proposal review + Phase 2 cross-repo migrations).

---

## 2026-05-12 — Prompt L: Scrum-master review of ai-council + legacy transcripts relocation

**Did:**
- Produced structured scrum-master review report for ai-council at `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (Scale M; first empirical instance of scrum-master review authority pattern): 10 findings (1 critical, 6 important, 3 minor); covers governance files, ADR-34 compliance, documentation staleness, tasks/ folder hygiene, dead code scan, folder structure
- Relocated 3 legacy `DECISION_NN_*` transcripts from `docs/decisions/transcripts/` to `docs/decisions/transcripts/archive/legacy/` (pre-CLI historical class separation per content-scoped archival principle); updated path references in ADR-31, ADR-32, decisions/README.md, CHANGELOG.md
- Updated BACKLOG: marked AI Council transcript routing [done]; added Cross-stream P2 (codify scrum-master review pattern) + P3 (extend to other repos)
- Appended LESSON: scrum-master review authority pattern (first empirical instance)

**Result:** ai-council review report ready for operator routing to architect. Legacy transcript cleanup complete. Branch merged to main.

**Next:** Operator routes ai-council review to architect for implementation. Scrum-master pattern awaits N=2 before ADR-level codification (see BACKLOG Cross-stream P2).

---

## 2026-05-12 — Prompt K: Atomic file-level cleanup

**Did:**
- K1 (a95318d): 16 ADR renames (underscore → hyphen); 14 transcript renames (council_out_ → council-out-); `docs/handoffs/_archive/` → `archive/` folder rename; 6 legacy flat .md + v2 folder relocated to `docs/handoffs/archive/legacy/`; 23 living docs updated (link refs, path refs, naming convention desc); scope tag validator: pass
- K2 (this commit): BACKLOG P1 `.dev-knowledge atomic migration` marked done; LESSONS: 2 new entries (merge/cleanup completion pattern, punted-migration anti-pattern); JOURNAL + CHANGELOG updated
- K1.4 skipped: cycle 2 propagation artifact absent from Downloads (not present at time of execution)
- Branch: `chore/atomic-cleanup-hyphen-migration` (2 commits, ready for K3 merge)

**Result:** .dev-knowledge file-level mess fully resolved. All upstream decisions (ADR-34 amendment + A2 + Council ratification) now have matching file-level state. Clean working tree on branch.

**Next:** K3 merge to main. Then: cross-repo handshake (BACKLOG P1 — operator routes to ai-council); Phase 2 migrations per BACKLOG P2 entries.

---

## 2026-05-12 — Prompt J: ADR-34 + ADR-38 amendments + BACKLOG reclassification + content-scoped archival principle

**Did:**
- J1: Amended ADR-34 — separator convention changed to universal hyphen mandate for filenames AND foldernames across .dev-knowledge and all child repos; ADR and transcript table rows updated from underscore to hyphen; example set added; scope changed from mandate/recommendation split to universal; Amendments trail added (commit ec45b2c)
- J2: Amended ADR-38 — ARCHITECTURE.md root placement now explicit (was unspecified); conversational A3 decision; Amendments trail added (commit f264966)
- J3: BACKLOG updated — Prompt H entries added in reclassified state (2 marked done: ADR naming + ARCHITECTURE.md placement; 2 kept open: handoff format + undiscovered repos; archive convention marked done per Council vote; A5 designated legacy/opportunistic); 7 new migration sequence entries added (P1 Prompt K atomic migration, P1 cross-repo handshake, P2 CI enforcement, P2 corp-monorepo migration expanded, P2 ai-council migration expanded, P2 content-scoped archival codification, P3 A5 Phase 2 retirement); LESSONS entry appended (content-scoped archival principle); JOURNAL + CHANGELOG updated
- Branch: chore/adr-34-amendment-hyphen-convention (3 commits ahead of main)

**Result:** ADR-34 + ADR-38 ratified per Council decision and operator A3 decision; migration work scoped into Prompt K (.dev-knowledge atomic, includes _archive/ → archive/ rename + propagation artifact archival); content-scoped archival principle captured as BACKLOG P2 awaiting second empirical instance

**Next:** Operator routes cross-repo notification artifact to ai-council; Prompt K executes .dev-knowledge atomic migration

---

## 2026-05-11 — Item 0 Prompt C: Codex M1 fix
- Did: reconciled PLAYBOOK dual-write contradiction at "Council Debate Archival Protocol" section (~line 1458); accepted M2 (bundle ESSENTIALS snapshot) + L3 (bundle manifest state) as pre-existing bundle state per point-in-time artifact convention
- Result: PLAYBOOK Council output guidance internally consistent; operators no longer instructed to skip manual archival they actually need to perform; Item 0 closed
- Next: merge `chore/session-sync-stage3-generation` to main after Rob confirms

---

### 2026-05-11 — Item 0 Prompt B: docs alignment + BACKLOG updates

**Did:**
- Rewrote `docs/handoffs/README.md` for v3.2 current format + pre-v3.2 legacy classification
- Rewrote `docs/decisions/README.md` with full ADR index 27-42, transcript naming convention, ADR↔transcript traceability table (spot-checked uncertain mappings)
- Added "Council output convention (current state)" section to PLAYBOOK Section 5
- Corrected `protocols/ESSENTIALS.md` Council output convention from aspirational dual-write to actual single-target + manual archival

**BACKLOG:**
- Added Cross-stream P1 "AI Council cross-project transcript routing"
- Added Stream B P2 "ai-council needs AGENTS.md (PLAYBOOK governance gap)"
- Superseded Stream C P3 "Council CLI dual-write trigger logic" (broader P1 addresses root cause)
- Updated Cross-stream P1 "Council decisions management consolidation" — inventory sub-item closed

**Result:** Canonical docs now match reality; AI Council routing feature properly tracked; ai-council AGENTS.md gap surfaced

**Next:** /review (5 files touched, above 3-file threshold per ESSENTIALS) → Rob gates merge to main

---

### 2026-05-11 — Item 0 Prompt A: handoff lifecycle cleanup

**Did:**
- Confirmed Stage 3 folder + archive already committed (e428a5e); only _in_progress/ orphans remain uncommitted
- Appending JOURNAL baseline entry to mark session start for 0a/0b/0c sequence

**Result:**
- Clean baseline: all Stage 3 artifacts committed; working tree has only untracked _in_progress/ orphans
- Ready for 0b (HANDOFF_PROCESS.md fix) and 0c (orphan cleanup)

**Next:**
- 0b: rewrite Stage 3 step 10 with explicit Move-Item semantics + empty-dir cleanup + post-state validator
- 0c: verify and delete _in_progress/ orphans (ai-council-audit-sync empty dir + dev-knowledge-session-sync post-archive)

---

### 2026-05-09 (night) — Stage 3 complete: .dev-knowledge session-sync handoff generated

**Did:**
- Generated Stage 3 handoff folder: `docs/handoffs/2026-05-09-dev-knowledge-session-sync/`
  (12 files flat per ADR-42 v3.2)
- Applied verification layer to Stage 2 architect claims:
  5 witnessed claims verified against repo; 1 conversation-history claim preserved;
  4 architect unknowns resolved (including DoD fix target clarification)
- Archived stage1-question + stage2-response to `_archive/2026-05-09-dev-knowledge-session-sync/`
- Stage 3 note: DoD bug ("5 required sections") is in the *generated*
  ai-council 07_ACTION_PLAN.md:9, not in HANDOFF_FOLDER_TEMPLATE itself
- Drift between Stage 1 SHA and Stage 3 HEAD confirmed safe (4 intra-session
  methodology commits; Rob explicitly confirmed proceed)

**Result:**
- Self-handoff bundle ready for upload to fresh .dev-knowledge browser chat
- Return trip template (09_EXECUTION_EVIDENCE.md) pre-created in bundle
- OLD .dev-knowledge browser chat can now be closed

**Next:**
- Open NEW claude.ai chat, upload 12-file bundle, paste `00_first-message.md`
- NEW chat presents synthesis; confirm; optional Q&A loop
- NEW chat generates Claude Code prompt(s) for refinement-partner session
- Execute in Claude Code (.dev-knowledge context)
- Return `09_EXECUTION_EVIDENCE.md` to `docs/handoffs/2026-05-09-dev-knowledge-session-sync/`

---

### 2026-05-09 (night, refinement) — BACKLOG strategic priorities + stage1 regenerated

**Did:**
- Added 9 Cross-stream BACKLOG items capturing Rob's strategic plan for
  next sessions: Council decisions management consolidation [P1], Sacred-files
  maintenance enforcement [P1], Hooks audit + consolidation [P2], Skills
  universalization [P2], Ecosystem standards audit [P2], Kimi K2 evaluation
  [P3], Scale tier re-evaluation [P3], Large repo migration prep [P3],
  VS Code productivity [P3]
- Regenerated stage1-question.md Section B: fresh BACKLOG snippet
  (all existing + 9 new items), updated HEAD sha to f87a5cc
- Added "press back on vague items" instruction to stage1-question Section B
  — next chat (post-Stage 3) is refinement partner, not just executor

**Result:**
- BACKLOG.md now captures Rob's full intended scope for next sessions
- stage1-question.md ready: architect can answer Stage 2 with full
  strategic context; Stage 3 bundle will carry complete BACKLOG

**Next:**
- Rob copies stage1-question.md PASTE_BOUNDARY content to current
  browser chat (the OLD chat for this session-sync)
- Architect provides Stage 2 response (5 sections: OBJECTIVE/REALITY/
  RATIONALE/DIRECTIVES/BOUNDARIES; no outer code fence)
- Rob saves response to stage2-response.md (replace below marker line)
- Next Claude Code session (after /clear): "complete handoff for
  dev-knowledge" → Stage 3 generates bundle
- ai-council branch docs/audit-sync-2026-05-09 awaits separate
  review/merge (not urgent)

---

### 2026-05-09 (night) — Session wrap-up

**Did:**
- Committed ai-council audit-sync execution evidence (return trip closed,
  branch `chore/session-2026-05-09-wrap-up`, commit 818a1c6)
- Added Strategic emphasis section to VISION.md (4 directions: velocity,
  consistency, evolution, lessons-as-default; conversational clarification,
  no specific repo/file references, scope: meta tagged, commit f578ac4)
- Generated Stage 1 question for .dev-knowledge session-sync handoff
  (session-sync variant; 5 pipeline questions adapted from template;
  eat-dogfood test of v3.1+v3.2 infrastructure for self-handoff)
- Pre-created stage2-response.md template in _in_progress slug directory

**Result:**
- Return trip for ai-council audit-sync closed — ADR-42 end-to-end test
  fully documented
- VISION strategic emphasis made explicit (continuous improvement
  principle operationalized as 4 concrete current directions)
- Session handoff infrastructure deployed: Stage 1 ready, Stage 2
  template awaiting architect response from OLD chat

**Next:**
- Rob copies stage1-question.md PASTE_BOUNDARY content to current
  browser chat (this chat IS the OLD chat for the session-sync)
- Architect responds with 5 sections (OBJECTIVE/REALITY/RATIONALE/
  DIRECTIVES/BOUNDARIES) — no code fence wrapper
- Rob saves response to stage2-response.md (replace below marker line)
- Next Claude Code session (after /clear): "complete handoff for
  dev-knowledge" → Stage 3 generates bundle
- ai-council branch docs/audit-sync-2026-05-09 awaits separate
  review/merge decision (not blocked)

---

### 2026-05-09 — Handoff Format v3.0 implemented + ai-council handoff regenerated

**Did:**

#### Council research → ADR-42 ratified
Council research debate (council_out_20260509_144836_research) surveyed
industry patterns (LangGraph, AutoGen, Cline Memory Bank), mature-domain
protocols (SBAR, I-PASS, SITREP), knowledge management theory (SECI,
Diátaxis). Three providers converged on flat folder, manifest + checksums,
5-7 question pipeline, mandatory receiver verification. Rob's refinements:
full VISION/PLAYBOOK/ESSENTIALS as invariants, ADR essences only (not full
copies), separate first-message.md for UX, tree.txt preserved.

ADR-42 ratified implementing three-stage flow: Claude Code generates
question prompt → Browser-2 architect provides project intelligence →
Claude Code reconciles + generates flat 11-file folder.

#### v3.0 artifacts created
- `docs/decisions/ADR-42_handoff_format_v3.md` (commit 1)
- `protocols/HANDOFF_PROCESS.md` rewritten v3.0 (commit 2)
- `templates/HANDOFF_QUESTION_TEMPLATE.md` (commit 3)
- `templates/HANDOFF_FOLDER_TEMPLATE.md` (commit 4)
- `protocols/SESSION_SETUP.md` updated (commit 5)

#### ai-council handoff regenerated
Broken v2.0 handoff (2026-04-30-ai-council-audit-sync, 3-level nesting,
missing VISION/PLAYBOOK) replaced with v3.0 flat 11-file structure (commit
6). Drift flagged: config/settings.yaml modified in ai-council working tree.

#### BACKLOG P1 closed
`[P1] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates`
closed (commit 8).

**Failed / methodology debt:**
- v2.0 handoff (created 2026-04-30) was structurally wrong on 6 dimensions
  (nested 3 levels, missing VISION/PLAYBOOK/ESSENTIALS, 7 full ADR copies,
  no question pipeline, no return trip). Surfaced by Rob; corrected via
  Council research + v3.0 implementation. Recurring "prescriptive writing
  without verification" pattern (see LESSONS 2026-04-30 entry).

**Next (updated evening — Stage 3 complete):**
- Handoff Stage 3 complete for 2026-05-09-ai-council-audit-sync
  (11-file folder generated; _in_progress archived; verification layer applied;
  config/settings.yaml actual diff: grok model string, not timeout — flagged)
- BACKLOG Cross-stream P1 "Phase 1 validation" marked done (governance cycle
  complete from .dev-knowledge side; execution test in NEW chat is next)
- ADR-39 amendment to register new template files (P3 BACKLOG, still open)
- PLAYBOOK content additions for ADRs 36-41 (P1 BACKLOG, still open)

---

### 2026-04-30 — Stream C session 6

**Did:**

#### ADR-33 ratified — VISION.md universalization
Trigger-based mandate (≥1 dependent), two-tier content (Standard/Lite),
child repo VISION.md required, hybrid enforcement (passive AGENTS.md
note + auditor primary). Migration cohort: ai-council + corp-monorepo
immediate; corp-ops + corp-sca-time-automation trigger-based by
2026-06-30.

#### ADR-34 ratified — File naming convention (cross-repo)
No universal master rule, table per file type. Living docs UPPERCASE,
Protocols UPPERCASE_WITH_UNDERSCORES, ADRs ADR-NN_topic_underscores,
Council transcripts council_out_YYYYMMDD_HHMMSS_*, audits/handoffs
YYYY-MM-DD-topic-dashes, templates kebab-case, configs kebab-case.yaml.
Hybrid enforcement (passive + future auditor).

#### ADR-35 ratified — Lessons base activation
Storage + retrieval + querying. LESSONS.md remains canonical narrative
+ derived lessons-index.json. Push retrieval (SessionStart hook,
scope+recency filter, 60 days). Pull querying (`lessons query`).
Bidirectional pipeline: corrections.jsonl → LESSONS.md → lessons-index
+ ~/.claude/rules/. Cross-repo discovery via DEV_KNOWLEDGE_PATH env
var + walk-up fallback. Promotion automation deferred.

#### ADR-37 ratified — Session Boundary Protocol (two-phase handoff)
Augments ADR-32. Top-level `## Current State` + `## Future State` over
existing 9-section structure (renamed to `## Detailed Context`).
Type-dependent mandate: audit handoffs STRONG, session handoffs MEDIUM
with explicit "undetermined" justification (cognitive exhaustion /
scope mismatch / dependency unresolved). Two-layer drift mitigation:
Browser 2 validation + Browser 1 instrumentation (timestamp + commit
SHA). Confidence level dropped (no enforcement mechanism = decoration).
Forward-only, no migration of historical handoffs.

**Failed:**
- Methodology debt surfaced: JOURNAL.md not updated, LESSONS.md not
  appended, BACKLOG.md proposed without verifying existing files already
  cover function. Strażnik łamiący metodologię. Cleanup before resuming
  Phase 1 closure (ADR-36 audit tool, ADR-38 backlog re-evaluation).

**Next pending:**
- ADR-38 (Cross-Session Backlog Architecture) — paused for re-evaluation
  after JOURNAL + LESSONS cleanup
- ADR-36 (Audit Tool Architecture) — Council debates done, draft pending
- HANDOFF_PROCESS / HANDOFF_TEMPLATE / first-message.md updates reflecting
  ADR-37 overlay (separate session)
- Phase 2 universalization rollout (ai-council + corp-monorepo immediate
  cohort)

**Afternoon addendum (post-ratification work):**
- Phase 1 validation initiated: ai-council audit Faza A1 discovery completed
  (output `docs/audits/2026-04-30-ai-council-discovery.md`); revealed
  ADR-38 architecture violation (flat src/, no src/ai_council/).
  ai-council migration brief generated for browser-2 architect session.
- ADR-40 amendment proposed (coefficient recalibration) then withdrawn —
  observed L-classification of ai-council was symptom of non-compliance,
  not algorithm error. Coefficients (b=12, c=8, d=15) retained pending
  validation against compliant repo measurements.
- `.dev-knowledge` self-audit performed (`docs/audits/2026-04-30-dev-knowledge-self-audit.md`):
  14 registered files audited; surfaced 8 small alignment gaps + ADR-39
  registry self-error (Tach taxonomy conflation).
- This commit applies Tier 1+2+3 batch fixes from self-audit (stale text,
  missing ADR refs, ADR-39 registry correction).

---

### 2026-04-28 | Heavy audit + VISION.md + ARCHITECTURE.md + Council convention reflection

**Did:**
- Heavy audit pass on `.dev-knowledge` after Stream C session 1 deliverables landed (ADR-31, ADR-32, HANDOFF_PROCESS.md v2.0). Phase A read-only audit surfaced: missing VISION.md/ARCHITECTURE.md, stale "personal operating system" framing in README/CLAUDE, JOURNAL/CHANGELOG gaps, PLAYBOOK §12 cap-language vs trigger-language inconsistency, missing Council CLI dual-write convention documentation, LESSONS.md format inconsistency in 4 post-ADR-29 entries, and `docs/decisions/transcripts/` naming dual-track (`DECISION_NN_*.md` vs `YYYYMMDD_HHMMSS_*.md`).
- Phase B created: `VISION.md` (universal-brain mission, charter format per AI Council debate Topic VISION); `ARCHITECTURE.md` (structural model per ADR-28 + ADR-31 Scale-M-with-one-L-tier-artifact); appended 6 lessons (dates-as-deadlines anti-pattern, don't-create-files-unnecessarily, session-close ≠ stream-done, message-count ≠ measurement, prompts always English, distinguish triggers from limits); standardized 4 multi-line LESSONS entries to single-line format per ESSENTIALS spec (content preserved verbatim, missing fields marked `[unknown]`).
- Phase C updated: README mission framing + index + Current state date 2026-04-27 → 2026-04-28; CLAUDE.md files-table adds VISION/ARCHITECTURE + Council output convention subsection + Topic 1/2 entries; ESSENTIALS adds mission anchor + Council convention note; PLAYBOOK §12 trigger language fix + §13 stale notice block + §5 Council Debate Archival Protocol dual-write blockquote (light update; manual path retained).
- Validator change: `scripts/validate_scope_tags.py` IN_SCOPE_FILES expanded to include VISION.md and ARCHITECTURE.md so they participate in section-tag validation and hybrid-ratio counting. Hybrid ratio steady at 18% post-changes (HEAD 18%, delta -0%).
- Predecessor commits folded into this session's narrative (no separate JOURNAL entries warranted): `df637c3` (CONTRIBUTING.md add — gets standalone CHANGELOG line per Rob's rule), `638a916` (VISION debate transcript moved to docs/decisions/transcripts/), `53e7da9` (ADR filename slug fixes from previous session pickup).

**Failed:**
- Pre-existing test break in `tests/test_validate_scope_tags.py::test_ratio_pass_when_stable_above_ceiling`: test references unqualified `"ESSENTIALS.md"` while IN_SCOPE_FILES uses `"protocols/ESSENTIALS.md"`. Verified pre-existing (failure reproduces on `main` HEAD before this audit's changes). Out of scope to fix in this audit; flagged for follow-up.
- LESSONS.md normalization for the 4 multi-line entries had to leave Category and Action fields as `[unknown]` for 3 of them (post-ADR-29 entries that omitted those fields); content preserved per "never delete content," missing structure marked rather than inferred.

**Next pending (Stream C / future sessions):**
- **Pattern dissemination ADR.** Formal ADR universalizing VISION.md template across child repos (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation). Currently flagged in VISION.md Relationships as "pending formal ADR." Templates `CLAUDE-md-template.md` and `AGENTS-md-template.md` would also gain VISION.md / ARCHITECTURE.md cross-refs in that session.
- **Audit tool implementation.** ADR-31 prescribes `tools/audit.py` (read-only cross-repo conformance audit + `repos.toml` manifest + `AUDIT.md` report). Per ADR-31 baseline rule, three known violations (ai-council AGENTS.md missing, ai-council CLAUDE.md trim ≤200 lines, corp-monorepo AGENTS.md correct template) must be remediated before audit ships green. Also implements VISION.md Lifecycle "verification mechanism."
- **`docs/decisions/transcripts/` naming consolidation.** Recommended: standardize on `DECISION_NN_topic.md` for the curated location; rename today's `20260428_125133_format-and-structure-of-visionmd-for-dev.md` → `DECISION_30_vision_format.md`. Defer to dedicated session with ADR for naming convention.
- **Lessons base activation strategy.** Lessons accumulate in LESSONS.md but lack mechanisms for retrieval, promotion, or querying. Future Stream C item; possibly Council-debate territory.
- **PLAYBOOK §8 substantive rewrite.** Already flagged stale (HANDOFF_PROCESS.md v2.0 supersedes); rewrite is its own session per scope discipline.
- **PLAYBOOK §13 substantive rewrite.** Stale notice added this session; rewrite is its own session.
- **ADR-32 §6 diagram errata.** Carried forward from prior JOURNAL entry — Council session decides whether to reissue ADR-32 or accept diagram as known slip.
- **Pre-existing test fix** for `tests/test_validate_scope_tags.py::test_ratio_pass_when_stable_above_ceiling` (path qualification: `"ESSENTIALS.md"` → `"protocols/ESSENTIALS.md"`).

(refs: this branch = `feat/heavy-audit-vision-mission`; commits = VISION add, ARCHITECTURE add, lessons append, lessons normalize, README, CLAUDE, ESSENTIALS, PLAYBOOK, plus this JOURNAL + CHANGELOG entries; VISION debate transcript at `docs/decisions/transcripts/20260428_125133_format-and-structure-of-visionmd-for-dev.md`)

---

### 2026-04-28 | HANDOFF_PROCESS.md v2.0 rewrite

**Did:**
- Full rewrite of `protocols/HANDOFF_PROCESS.md` (v1.x → v2.0) per ADR-32. 9-section table form, folder anatomy, point-in-time copies, charter + step-verification controls, extract-to-task mechanics with defer-requires-justification rule. ~290 lines, hybrid ratio 18%. 4 commits on `feat/handoff-process-rewrite`: protocol rewrite (`b9a7486`), template update (`f21a4d9`), cross-references (`dbca501`), CHANGELOG (`b04605c`).
- `templates/HANDOFF_TEMPLATE.md` rewritten to 9-section skeleton matching new structure.
- `CONTRIBUTING.md` "rewrite pending" notice removed; `PLAYBOOK.md §8` got a one-line stale notice pointing to v2.0 (substantive §8 rewrite deferred to its own session).

**Failed:** —

**Next pending (cross-stream):**
- **ADR-32 §6 diagram amendment.** ADR-32 §6 ASCII diagram puts `HANDOFF.md` at folder root; live first instance + PLAYBOOK + new HANDOFF_PROCESS.md v2.0 put it inside `contents/`. Live layout wins (drag-drop target). HANDOFF_PROCESS.md §4 documents this as known errata. Future Council session decides: reissue ADR-32 or accept diagram as known slip. Do NOT amend ADR-32 silently.
- Substantive PLAYBOOK §8 rewrite (currently stub with stale notice).

---

### 2026-04-28 | ADR-31 + ADR-32 formalized

**Did:**
- Drafted ADR-31 (authority model) + ADR-32 (handoff format) from DECISION_28 + DECISION_29 transcripts. 4 commits on feature branch, merged clean. 2 amendments after Rob review (manifest name softened, extract-to-task follow-up pointer added).

**Failed:** —

**Next:** (a2) `protocols/HANDOFF_PROCESS.md` rewrite referencing ADR-32 — own session.

---

### 2026-04-27 | Stream C session 1 bonus scope — audit infrastructure + Path B + Tier 3 Prompt 2 + X1 + JOURNAL backfill

**Did:**
- ESSENTIALS.md 4-commit refactor (C1-C4): structural cleanup (`2bbe340`, `7421d9e`, `957baee`, `66382ca`, `e1c30cf`), skills reference sub-bullet (`2132a77`), Feedback Loop restructured with Auto vs Manual cadence labels (`e6baca9`), new "How Claude thinks" thinking-quality directives section (`ac96b2c`)
- CLAUDE.md stale references update — PLAYBOOK section count, TOKEN-LOG cadence, ESSENTIALS rule, Council #28 added (`fc8d8b5`)
- README.md Current state section updated to reflect post-Stream-B reality (`2de7826`); handoffs clarified as persistent stream-level decision archive (`3997f11`)
- Deep cleansing diagnostic audit created — 18 findings across 7 files (`8c4a10a`, see `docs/audits/2026-04-27-deep-cleansing-diagnostic.md`)
- ENVIRONMENT.md stale "Last updated: 2026-03-29" fixed → 2026-04-27 (`9e166d9`)
- Path B numbers audit + classification (`d52c243`, see `docs/audits/2026-04-27-numbers-audit.md`); 5-tier execution: Tier A removals (`44f795f`), Tier B replacements (`cff571b`), Tier D rationale (`81edce3`), Tier E decisions (`9a700d9`), merged (`9058238`)
- Tier 3 Prompt 2 audit findings fixes — T1 + C2 + anomaly in CLAUDE.md (`0993669`), E2 + E3 in ESSENTIALS (`3cb9f98`), R2 in README (`3adb6b2`), merged (`0d199e3`)
- X1 verification (Outcome C: PLAYBOOK has its own ### Roles at line 1716 in Section 8, partial overlap with ESSENTIALS canonical version) → blockquote cross-ref added to PLAYBOOK (`b17092d`); audit X1 marked PARTIALLY-INVALID/RESOLVED (`586e360`)
- PLAYBOOK Documentation file types v1.1 — JOURNAL ordering flipped oldest-top → newest-first prepend per Rob's preference (`167c11b`); aligns with TOKEN-LOG/CHANGELOG, LESSONS retains oldest-top per ADR-29
- This JOURNAL.md created with full historical backfill (10 entries, repo creation through today)

**Failed:**
- Audit hallucination N1: deep cleansing audit fabricated specific file metadata (1019 lines, exact filename) for a file that does not exist on disk and has no git history. Discovered via filesystem check + git log verification. Finding marked INVALID (`1d4f3af`); audit reliability flagged. Lesson appended to LESSONS.md.
- Tier 3 Prompt 2 session summary listed 4 items as PENDING that were actually already done in same session (R1/R3/N1/E1). Acknowledged after Rob's pushback. Cause: had git log visible, didn't cross-check before listing pending. Pattern: model produces plausible-looking state claims that read as confirmed evidence.
- Initial JOURNAL backfill prompt halted at Step 1 pre-write after archaeology revealed PLAYBOOK already formally documents JOURNAL.md at three locations with deliberate contradictory spec (oldest-top, Did/Failed/Next, per-session, Scale-conditional). Surfaced conflict, prompt re-issued with PLAYBOOK ordering amendment included.

**Next:**
- CHANGELOG Path B entry (MEDIUM gap — substantive content changes uncovered)
- Handoff doc `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md` append items 21-26 covering today's 6 unlogged Krok 3 bonus-scope work areas
- README "Current state (2026-04-26)" date refresh to 2026-04-27 (LOW cosmetic)
- H1 audit finding (HANDOFF_PROCESS path template) — Krok 5 deferred
- 34 stale feature branches from Streams A/B — future hygiene pass
- Stream C session 2: file naming convention (per Stream C plan)

(refs: 39 commits today; 16 files modified; `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`; audit docs `2026-04-27-deep-cleansing-diagnostic.md` + `2026-04-27-numbers-audit.md`)

---

### 2026-04-26 | Stream B close + Stream C session 1 — ADR-30 default branch + PLAYBOOK Repo conventions skeleton

**Did:**
- HANDOFF_PROCESS.md v1.1 amendment — 3 artifacts not 1 per Vibe Code 4 protocol patch (`ee7e644`, `4055006`)
- Stream B → Stream C handoff document created (`16bb05c`, see `docs/handoffs/2026-04-26-stream-b-complete-stream-c-scope.md`)
- 8 lessons promoted from CHANGELOG to LESSONS.md as standalone pre-work before session 1 ADR-30 work (`aa6b34f`, branch `chore/lessons-promotion-stream-b-leftovers`)
- ADR-30 created — universal `main` default branch rule for all Rob's repos (`2b337bf`, see `docs/decisions/ADR-30_default_branch_main.md`)
- PLAYBOOK "Repo conventions" section added with 5-subsection skeleton: 1 filled (Default branch), 4 TBD with forward-references to ADR-31/32/33/34 (`274221b`)
- README ADR count updated (`341548c`); CHANGELOG Stream C session 1 entry (`415f275`); HANDOFF_PROCESS + prompt-template master→main updates (`7289cdd`); ADR-30 prompt-template "Merge to master" prose fix (`3a2bf18`); PLAYBOOK ADR-32 placeholder wording standardized (`fabb6eb`)
- `.dev-knowledge` repo renamed master→main (Phase 2; remote rename N/A — local-only repo)
- Codex audit of ADR-30 work (`bc85704`, see `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)
- 8 commits on `feat/adr-30-default-branch-main`, merged via `9df901e`
- Stream C session 1 handoff document created with full 11-session plan (`3c97dd2`, see `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`)

**Failed:**
- Codex audit found 1 Medium ("Merge to master" prose in prompt-template) — fixed in `3a2bf18`. 2 Low findings: Finding 1 accepted as deliberate extended ADR schema, Finding 2 fixed in `fabb6eb`.
- Phase 2 master→main rename reduced scope: Steps 11-14 (push/delete/GitHub UI) N/A — `.dev-knowledge` is local-only repo, no remote configured. First full-flow validation deferred to Stream C sprint 1 (corp-monorepo + ai-council).

**Next:**
- Stream C session 2: file naming convention (per 11-session plan)
- Sprint 1 (session 4): per-repo branch renames + corp-monorepo `.claude/settings.local.json` audit
- Council #27 filter-by-tag rule — UNRESOLVED follow-up (logged in handoff item 17)

(refs: `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`; ADR-30; Codex audit `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)

---

### 2026-04-25 | Stream B implementation marathon — 19 of 19 gaps closed + 1 amendment

**Did:**
- Stream B gaps mapping audit — 19 gaps with placement + dependencies (`5aa3b35`, see `docs/audits/2026-04-24-stream-b-gaps-mapping.md`)
- Gap #6 AGENTS.md template + canonical governance section (`ed82b46`, `f3d981a`); template renamed to codex-review-config-template.md after purpose clarification (`c9d6c07`, `e838b1a`)
- Gap #1 Roles section v1.0 in ESSENTIALS — browser/Claude Code division (`54d7289`)
- Validator/hook H3 divergence discovered + fixed: validator no-args fallback (`446abbe`); validator/hook alignment on heading level scope (`7eaa2c2`)
- Gap #5 CLAUDE.md template v1.0 (thin pointer, hybrid pattern) + PLAYBOOK section (`001fbb2`, `e87525d`)
- Gap #2 + #3 prompt template v1.0 + writing prompts PLAYBOOK section (`1bd4442`, `76af001`)
- Gap #4 + #18 PLAYBOOK Documentation file types and session continuity section — 12-file taxonomy + Scale matrix + 4 common confusions + order conventions (`9a0ed10`)
- Gap #11 HANDOFF_PROCESS.md v1.0 — Vibe Code 4 protocol; handoff-prompts aligned (`5c3ddb5`, `b45a9b5`)
- Gap #12 + #19 PLAYBOOK — Council vs single-model + critic gating; amendment vs reopen decision protocol (`bc4946b`, `6145b8c`)
- Gap #13 PLAYBOOK session boundaries section v1.0 (`80fac2f`)
- Gap #15 + #16 PLAYBOOK — testing rules per Scale tier; Codex review archival protocol (`5aecf57`, `370cf16`)
- Gap #17 PLAYBOOK Continuous Improvement section v1.0 (`0e9105a`); validator skip pattern for docs/tech-radar/ added (`3088a2d`)
- Gap #7a-d PLAYBOOK Claude Code internals section v1.0 (`9a31446`); Gap #7d amendment — subagents factually active (`3860d4d`, `f008489`)
- Gap #10 PLAYBOOK adoption protocol for Claude Code extensions (`8dfe69c`)
- Gap #8 VS Code workspace templates S/M/L (`0b00f70`, `2d890a9`, `05d08a2`) + PLAYBOOK section (`4be065c`)
- Gap #9 Claude Code features inventory audit (`271d6d6`, see `docs/audits/2026-04-25-claude-code-features-inventory.md`); tech-radar cross-link (`a684fc1`)
- Stream B COMPLETE: 19/19 gaps + 1 amendment (`1c9ff9a`)

**Failed:**
- Validator/hook H3 divergence discovered during Gap #1 work — manual validator passed but pre-commit hook failed on H3 tags. Root cause: hook called validator with no args; validator's no-args fallback was vacuous-pass instead of scanning all in-scope files. Fixed in same session.
- Gap #7d initial pass missed that subagents are factually active per `~/.claude/agents/` — amendment commit added explicitly noting this.
- AGENTS.md mental model reverted twice in 48h despite docs documenting reconciliation — logged as lesson candidate (mental model drift after recent reconciliation).

**Next:**
- Stream B → Stream C handoff (Gap #18 amendment candidate: Scale matrix recalibration based on actual project sizes)
- Stream C scope definition + session 1 planning

(refs: `docs/audits/2026-04-24-stream-b-gaps-mapping.md`; `docs/audits/2026-04-25-claude-code-features-inventory.md`; CHANGELOG entries 2026-04-25)

---

### 2026-04-24 | Stream A close + plumbing — ratio-aware enforcement, ADR-27 amendment, TOKEN-LOG cadence, scope-tag rollout

**Did:**
- Research archival (`ccc91d6`, `71ca513`); Council #28/#29 transcripts + research archived (`731cf9d`, `292a4a7`); 7 historical Council debates retroactively archived (`802a533`); README.md created for `docs/research/` and `docs/decisions/` (`60ee717`)
- Council archival protocol added to PLAYBOOK Section 5 (`bd5e6c5`)
- Stream A gap report created with supersession note on consolidated actions (`6945921`); repo sync + CHANGELOG + CLAUDE.md (`4bc8859`)
- PLAYBOOK Phase 2 tagging sanity check (Stream A prompt 3.5) — 5 top-level scope tags corrected on S4/S6/S7/S14/S15 + cascade inherit-parent fixes (`85190db`, `c3f8e0d`, `f3e1956`, `2bb5528`)
- Phase 2 audit applied — sections tagged in ESSENTIALS, SESSION_SETUP, HANDOFF_PROCESS, ENVIRONMENT (`fd96b5a`, `8a25a19`, `bcd0c36`, `b533d12`)
- ADR-29 amendment — file-level scope tag for LESSONS, [scope: X] inline format for new entries (`b0df750`, `296767a`, `8013d9c`, `496c9f0`)
- ADR-27 amendment — commit-time enforcement prescription (ratio-aware, `aec1a4b`); validator implementation (`b54cddd`); unit tests (`3987348`); ruff + decimal precision fixes (`c02e57e`, `9ea94d3`, `8c5ea66`)
- Stream A CLOSED — gap report marked complete, lessons extracted (`19d6516`, `f0702f2`)
- LESSONS 50-entry split deferred with rationale (`eaf3f53`); 2026-04-21 inventory marked SUPERSEDED (`b940661`); ADR-27 filename simplified (`722960b`); handoff/ → handoff-prompts/ rename (`a65b495`)
- README user-first rewrite reflecting post-Stream-A state (`093d545`)
- ccusage tool adopted — TOKEN-LOG snapshot (`2fe0b99`); ENVIRONMENT documentation (`c6f3351`); PLAYBOOK reference (`6db896f`)
- TOKEN-LOG cadence formalized (`eb7cc03`, `7d6e51a`); TOKEN-LOG order flipped to newest-first matching CHANGELOG convention (`43eb577`, `7d8219a`)
- ESSENTIALS data sanitization rule for lessons (`8605202`); validator rename-collision lesson + file-level tag pattern lesson (`717d649`)

**Failed:**
- Validator rename collision: handoff/ → handoff-prompts/ rename initially broke validator's path resolution. Fix: file-level tag pattern documented as workaround, lesson appended.
- Original ADR-27 prescription was flat 25% blocking; turned out to cause "stuck above ceiling" failure mode. Amended to delta-rule (blocks regressions only).

**Next:**
- Stream B scope mapping (became 2026-04-25 marathon)
- Per-Scale Stream B gap implementation

(refs: `docs/audits/2026-04-24-stream-a-gap-report.md`; ADR-27 amendment; ADR-29 amendment; CHANGELOG entries 2026-04-24)

---

### 2026-04-23 | corp-monorepo Scale L operating model audit

**Did:**
- corp-monorepo Scale L operating model analysis audit (`54c9644`, see `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`)
- Audit extended with AI Council integration analysis, ADR-27 collision flag, naming conventions deviation, VS Code workspace findings (`a29b0d9`)

**Failed:**
- (none recorded)

**Next:**
- Apply Stream A scope tagging per audit findings; Council #28 + #29 follow-up

(refs: `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md`)

---

### 2026-04-22 | ADR-27 + ADR-29 created + validator scaffolding

**Did:**
- ADR-27 Council #27 scope tagging architecture (binding, Council 4/5 consensus, Option A) — five tag values dev/llm/hybrid/runtime/meta, pre-commit enforcement, evidence-triggered reopening (`b878cce`, see `docs/decisions/ADR-27_scope-tagging.md`)
- ADR-29 LESSONS.md grandfathering (binding, derivative of ADR-27) — existing entries untouched, [scope: X] inline field on new entries (`00e4467`, see `docs/decisions/ADR-29_lessons-grandfathering.md`)
- CHANGELOG sync 2026-04-21 ADR-27 + ADR-29 (`f0bc0e3`)
- `validate_scope_tags.py` validator created (`42588b3`); pre-commit config + `requirements-dev.txt` (`1acdf84`)
- CLAUDE.md scope tags section + all sections tagged as meta (`2a048b4`); README sections tagged as meta (`d106c78`)
- CHANGELOG vocab + hook + self-tag entry (`29c867e`)

**Failed:**
- (none recorded)

**Next:**
- Phase 2 audit — section-level tagging across all `.dev-knowledge` files
- corp-monorepo audit (became 2026-04-23 work)

(refs: ADR-27; ADR-29; CHANGELOG entries 2026-04-22)

---

### 2026-04-21 | Tech radar + Council #27 + dev-knowledge architecture redefinition

**Did:**
- Tech radar handoff (`b297677`); ESSENTIALS handoff process expanded with template (`8f99f9b`); HANDOFF_PROCESS.md extracted as dedicated file (`a704aaf`, `1bc115a`); redundant codex-review stub removed (`4a22305`); handoff prompts extracted to dedicated files (`588e4d4`); /handoff renamed to /session-summary (`a5330fe`) avoiding naming conflict
- `.dev-knowledge` inventory audit (`2fd99c5`, see `docs/audits/2026-04-21-dev-knowledge-inventory.md`)
- Phase 2 scope tagging audit — 63 sections classified across 8 primary files; distribution: 14% dev, 22% llm, 21% hybrid, 8% runtime, 35% meta (`0395a04`, see `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`)
- Council #27 brief — 3 architecture options with decision matrix (`bd0c9bb`); Option 0 added with honest LESSONS framing + matrix caveat (`2f287a6`)
- 2026-04-21 session handoff with dev-knowledge redefinition (`25808c3`)
- ADR-28 three-layer architecture (descriptive — browser → `.dev-knowledge` → projects) added to PLAYBOOK System Architecture section (`695e54c`, `0704f06`); Section 12 cross-ref (`4ace660`); CHANGELOG entry (`40a857d`)
- 2 process lessons appended — browser-as-tutor defaulting violates three-layer (`fbf0863`); session-level lessons (`906b61c`)
- S15 + ESSENTIALS + CHANGELOG codex-review automation update (`9b5785a`)
- Codex review for smoke-test added then deleted (`88aa66a`, `49d6647`)

**Failed:**
- Codex review smoke-test audit added then deleted same-day — premature artifact, pattern not yet stable. Deleted before any consumers.

**Next:**
- ADR-27 from Council #27 (became 2026-04-22 work)
- ADR-29 LESSONS grandfathering (Council #27 raised this open question)
- Validator implementation (Phase 2 enforcement)

(refs: `docs/handoffs/2026-04-21-dev-knowledge-architecture-redefinition.md`; `docs/handoffs/2026-04-21-tech-radar-session.md`; `docs/audits/2026-04-21-council-27-brief.md`; ADR-28)

---

### 2026-04-15 to 2026-04-17 | Codex/Tach/Opus 4.7 tooling adoption + handoff workflow formalization

**Did:**
- Codex CLI installed (ChatGPT Plus, GPT-5.4 default); AGENTS.md created in corp-monorepo (severity calibrated, two review modes); `/review` slash command in `~/.claude/commands/review.md`
- PLAYBOOK Section 15 Cross-Tool Review [L+M] added; Section 16 Code Quality Audit Process [L only] added
- ESSENTIALS updated with monthly Codex audit + Codex review step in "Ending a Session"
- Opus 4.7 + xhigh effort level added to ESSENTIALS (`a6f7a10`) and PLAYBOOK prompt template (`5168c64`)
- 3 Tach adoption lessons appended to LESSONS.md (`beaecfb`)
- ENVIRONMENT.md updated with Opus 4.7 and new settings (`ef0ae1e`); .claude/settings.local.json gitignored (`567ed61`)
- 2026-04-15 session handoff added (`0e999e7`); handoff workflow formalized in ESSENTIALS (`9a17db3`); verified handoff step (`615e116`); verified tech radar session handoff added (`1ba8a05`)

**Failed:**
- Magistrala verification deferred (pipeline still unverified end-to-end since Council #24 MyWork restructure)
- One A/B test deferred (per session handoff status)

**Next:**
- Tech radar continuation (became 2026-04-21 session)
- Handoff process refinement (became 2026-04-21 work)
- Magistrala verification (carried as standing follow-up)

(refs: `docs/handoffs/2026-04-15-codex-tach-opus47-session.md`; `docs/handoffs/2026-04-15-tech-radar-session.md`)

---

### 2026-04-14 | Dev practice OS state audit

**Did:**
- Audit of dev practice OS state after 2026-03-30 session (`4ba0513`) — point-in-time snapshot before tooling evaluation work begins

**Failed:**
- (none recorded)

**Next:**
- Tooling evaluation (Codex CLI, Tach, Opus 4.7) — became 2026-04-15 session

(refs: commit `4ba0513`)

---

### 2026-03-30 | Repo creation — initial scaffolding + same-day expansion

**Did:**
- Initial commit — dev practice knowledge base scaffolding, 9 files (`b635615`)
- `.claude/` project config with git-discipline rule and `/save` command (`583f335`)
- Codex review step added to ESSENTIALS.md "Ending a Session" (`2f70713`); Section 15 Cross-Tool Review added to PLAYBOOK (`d6bfddb`); Codex review integration spec (`73e8a9a`); 5 Codex audit lessons appended + Section 16 added to PLAYBOOK + ESSENTIALS updated (`343abdf`)
- Project Scale Tier system added to PLAYBOOK (`0741aeb`); tier tags applied to scale-dependent sections (`665ff14`); post-structural-change documentation rule with tier scaling (`3f186be`); ESSENTIALS Project Scale Tier reference (`fe0d6ca`); LESSONS Project Scale Tier lesson (`9a3f25f`)
- AGENTS.md template with L and M scale variants (`f34dc7a`); TODO management lesson (`dd58836`)

**Failed:**
- (none recorded — initial creation session)

**Next:**
- Dev practice OS state audit (became 2026-04-14 standalone)
- Tooling evaluations (Codex CLI, Tach, Opus 4.7)

(refs: 13 commits 2026-03-30; initial commit `b635615`)
