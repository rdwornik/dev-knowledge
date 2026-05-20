# Journal — .dev-knowledge

<!-- scope: meta -->

> Per-session tactical log of `.dev-knowledge` Claude Code work. Entry shape
> as of 2026-05-16 (Council Simplification): `Did / Result / Changes /
> Abandoned / Next`. Newest-first prepend ordering.
>
> Distinct from LESSONS (per-learning generalized rules, oldest-top per
> ADR-29) and handoffs (per-session boundary artifacts for browser-chat
> resumption). JOURNAL is the within-Claude-Code-sessions tactical log
> enabling context recovery across sessions in same repo. The `Changes:`
> line records what files / areas moved — replacing the deleted CHANGELOG.md.
>
> Update protocol: prepend new session entry at top of entry list (under this
> intro blockquote, before existing entries). One entry per Claude Code session
> OR per workday for heavy days. Each entry cites commit hashes, handoff doc,
> or ADR for deeper detail. JOURNAL summarizes, doesn't duplicate.

---

### 2026-05-20 — Handoff process audit (mechanism, conformance, gaps)

- Did: Read-only audit of how the handoff process actually works at HEAD. Read ADR-42, ADR-45 (head), `protocols/HANDOFF_PROCESS.md` (v3.3.3), both templates (head), `.claude/commands/handoff.md`, `scripts/backlog_extract.py`, `scripts/migrate_links.py`. Verified the just-completed 2026-05-19 cycle: 12-entry bundle (`docs/handoffs/2026-05-19-dev-knowledge-session-sync/`) + Stage 1+2 archive present. Wrote `docs/audits/2026-05-20-handoff-process.md` — mechanism-first, stage-by-stage, severity-tagged gaps.
- Result: Audit immutable. Six MEDIUM gaps surfaced (version-string skew across slash command / template / protocol; ADR-45 status semantics ambiguous; Stage 3 still references deleted CHANGELOG; `scripts/backlog_extract.py` targets deleted `BACKLOG_ARCHIVE.md`; Stage 2 thinness has no validator; ADR-39 registry gap on templates). Three LOW gaps (Stage 2.5 placement framing; drift detection same-session assumption; time-bound REALITY clauses). Two INFO notes (Self-Containment Rule discipline-only; JOURNAL per-stage append). All recommended fixes are < 10 lines each.
- Changes: `docs/audits/2026-05-20-handoff-process.md` (new); JOURNAL prepend.
- Abandoned: None — read-only audit; no tooling, ADRs, templates, or samples modified.
- Next: Decide whether to act on the six MEDIUM gaps. The version-label fixes (M-1) and CHANGELOG-step removal (M-3) are pure cleanup; M-2 (ADR-45 status) is a small governance question worth raising before action.

---

### 2026-05-20 — Posture audit verification + triage + quick-win fixes

- Did: (1) Verified the 2026-05-19 posture audit against ground truth — wrote `docs/audits/2026-05-20-posture-audit-verification.md` scoring each finding CONFIRMED / PARTIAL / REFUTED / BONUS. (2) Surfaced 4 bonus drift items the witness-based audit could not see: `scripts/backlog_extract.py` references deleted `BACKLOG_ARCHIVE.md`; `scripts/migrate_links.py` SKIP_NAMES includes deleted `CHANGELOG.md`; `docs/decisions/README.md` ADR Index missing ADRs 45-50 + 54; `ARCHITECTURE.md` Governing ADRs missing ADR-54. (3) Triaged into BACKLOG: updated C1 (sacred-files — drop CHANGELOG from `.dev-knowledge` list) and C2 (ESSENTIALS — expand scope from ADRs 35-41 to 35-54); added 4 new Stream C entries (backlog_extract drift, migrate_links drift, ADR index gaps, ADR relationship index); added 1 new Cross-stream entry (PLAYBOOK codifications from audit H3/H4/T1/T2). (4) Executed two safe quick wins: removed `CHANGELOG.md` from `migrate_links.py` SKIP_NAMES; extended ADR index in `docs/decisions/README.md` with ADRs 45-50 + 54; added ADR-54 to `ARCHITECTURE.md` Governing ADRs.
- Result: Audit + verification both immutable. LESSONS count corrected from audit's ~39 to actual 135 (3.5x undercount). Tier 1 items (B1 codemap generator, D1 ADR-38 self-compliance, C1 sacred-files coherence) flagged as needing design decisions — out of scope for autonomous run; remain in BACKLOG.
- Changes: `docs/audits/2026-05-20-posture-audit-verification.md` — new immutable artifact (verification companion to 2026-05-19 audit); `BACKLOG.md` — C1 + C2 updated, 5 entries added (4 in Stream C, 1 in Cross-stream); `scripts/migrate_links.py:4` — CHANGELOG.md removed from SKIP_NAMES; `docs/decisions/README.md` — ADR index table extended with 7 entries; `ARCHITECTURE.md` — Governing ADRs list extended with ADR-54; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator review of BACKLOG additions. Tier 1 work (codemap generator + CI freshness check per ADR-51 — already named next-session OBJECTIVE in Stage 2 handoff) and Tier 1 decisions (ADR-38 self-compliance approach: src/ migration vs ADR amendment) are the largest open threads.

---

### 2026-05-20 — Filed external posture audit (read-only, browser-chat architect)

- Did: Filed `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` — a read-only structural / principle-level audit produced by the browser-chat architect (Claude Opus 4.7) following the ADR-53 / ADR-54 effort closure. Witness-based, no file-state verification; explicit "Unknown — verify against repo" markers. Surfaces 17 principles, findings across 10 areas (A–J), 6 principle tensions, 17-item prioritization (Tier 1 names codemap generator + CI freshness, ADR-38 self-compliance, sacred-files coherence).
- Result: Audit immutable per ADR convention; available as input for next session's file-state verification pass against ground truth. Tier 1 recommendations align with Stage 2 OBJECTIVE for codemap generator + CI freshness check (ADR-51 open item).
- Changes: `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` — new (immutable artifact); `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator-driven decision on whether to (a) verify findings against actual file state, (b) triage into BACKLOG, or (c) proceed directly to Tier 1 work (codemap generator). Audit's own §7 notes sequencing is the operator's call.

---

### 2026-05-20 — Handoff Stage 3 complete for 2026-05-19-dev-knowledge-session-sync

- Did: Stage 3 reconciliation + folder generation per ADR-42 v3 / HANDOFF_PROCESS v3.3.3. Ancestor check passed (Stage 1 `c4d7c858` is ancestor of HEAD `1f7a985`). Parsed Stage 2 architect response (5-section response targeting codemap generator + CI freshness check spec per ADR-51 open item). Generated 11-file bundle at `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` (self-handoff — no `02b_ECOSYSTEM_VISION.md`). Curated `05_GOVERNANCE_ESSENCES.md` for ADR-51 and ADR-54 (cited in 07). Archived Stage 1 + Stage 2 inputs at `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/`.
- Result: Handoff bundle ready for upload to a NEW `.dev-knowledge` browser chat. OLD chat (Stage 2 source) can be closed.
- Changes: `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` — new (11 files); `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/` — new (stage1-question.md + stage2-response.md moved from `_in_progress/`); `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/` — removed; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Operator zips/uploads bundle into NEW chat, pastes `00_first-message.md`, runs articulation gate + synthesis; new session targets codemap generator + CI freshness check spec per ADR-51 open item.

---

### 2026-05-19 — Handoff Stage 1 generated for 2026-05-19-dev-knowledge-session-sync

- Did: Generated Stage 1 handoff artifacts for self-handoff of `.dev-knowledge`. Captured HEAD `c4d7c858` at clean working tree on `main`. Created `_in_progress/2026-05-19-dev-knowledge-session-sync/` with `stage1-question.md` (PASTE_BOUNDARY block for OLD chat) and `stage2-response.md` placeholder.
- Result: Awaiting Stage 2 architect response from OLD `.dev-knowledge` browser chat.
- Changes: `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/stage1-question.md` — new; `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/stage2-response.md` — new (placeholder); `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Rob carries paste block to OLD chat; populates `stage2-response.md`; says "complete handoff for dev-knowledge" → Stage 3.

---

### 2026-05-19 — Codex reviewer config globalized (ADR-54)

- Did: Branch `docs/codex-reviewer-global-standard`. Authored `codex/AGENTS.md` as the canonical global Codex reviewer config (generic reviewer role, pre-review ARCHITECTURE.md read instruction, checklist, output format — corp-monorepo-specific items dropped). Deployed to `~/.codex/AGENTS.md` (filesystem action, not committed). Added ADR-54 recording the global-standard decision and scope clarification vs ADR-53 (tool config ≠ instruction contract). Added PLAYBOOK §16 note on config ownership. Corrected ARCHITECTURE.md §Authority line to reflect the new model.
- Result: `~/.codex/AGENTS.md` live with generic reviewer config. All repos benefit without per-repo duplication. `corp-monorepo/AGENTS.md` retirement queued as a follow-up chunk in that repo.
- Changes: `codex/AGENTS.md` — new; `docs/decisions/ADR-54-codex-reviewer-global-standard.md` — new; `protocols/PLAYBOOK.md` §16 — 2-line addition; `ARCHITECTURE.md` line 137 — rewritten; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: Retire `corp-monorepo/AGENTS.md` (follow-up chunk in corp-monorepo).

---

### 2026-05-19 — Correct corp-monorepo AGENTS.md violation framing in ARCHITECTURE.md

- Did: Branch `docs/correct-corp-monorepo-agents-violation`. Corrected ARCHITECTURE.md §Authority line 137 — corp-monorepo/AGENTS.md is a Codex tool config, not an ADR-53 instruction contract; ADR-53 has no scope over tool-native config. Violation was a mis-classification, not a real non-conformance.
- Result: Known violations counter → 0 open. ARCHITECTURE.md accurately reflects ecosystem state.
- Changes: `ARCHITECTURE.md` line 137 — rewritten; `JOURNAL.md` — this entry prepended.
- Abandoned: nothing.
- Next: —

---

### 2026-05-19 — Post-ai-council cross-repo sweep: stale AGENTS.md refs resolved

- Did: Grepped `.dev-knowledge` for ai-council AGENTS.md references after ai-council ADR-53 chunk 4 (AGENTS.md deleted, CLAUDE.md v2.1 live at 139 lines). Branch `docs/post-ai-council-cross-repo-sweep`. 2 commits to live docs.
- Result: All stale ai-council AGENTS.md references in live docs resolved. Immutable docs (ADRs, research transcripts, audits) left untouched per policy.
- Changes: `ARCHITECTURE.md` — removed resolved violation (1) for ai-council CLAUDE.md exceeding 200-line target (now 139 lines); "Two known violations" → "One known violation" (corp-monorepo AGENTS.md remains). `BACKLOG.md` — removed "AGENTS.md removal (future chunk)" from Phase 2 rollout item and ai-council ADR-38 compliance item; both now reflect completion.
- Abandoned: nothing.
- Next: corp-monorepo ADR-53 chunk — AGENTS.md removal and CLAUDE.md migration (the remaining known violation in ARCHITECTURE.md).

---

### 2026-05-19 — Chunk 4: retire AGENTS.md, CLAUDE.md v2.1 live

- Did: Migrated all AGENTS.md content into CLAUDE.md (v2.1 template, 12 sections) and retired AGENTS.md for `.dev-knowledge`. Branch `docs/chunk4-dev-knowledge-claude-md-migration`. 3 commits.
- Result: CLAUDE.md is now the single canonical agent-instruction file per ADR-53. AGENTS.md deleted. All content placed per approved disposition map — no silent drops. Three approved condensations: ADR list trimmed to last 5 (ADR-49–53) with pointer to ARCHITECTURE.md; scope tags reduced to one bullet; per-file update triggers dropped from CLAUDE.md (live in each file's own header). Live-doc references updated in BACKLOG.md (Phase 2 status + ai-council item).
- Changes: `CLAUDE.md` (rewritten to v2.1, ~130 lines); `AGENTS.md` (deleted); `BACKLOG.md` (status updates for Phase 2 and ai-council items).
- Abandoned: Nothing.
- Next: Merge branch to main. ai-council AGENTS.md retirement is a separate future chunk (ADR-53 Decision 2).

---

### 2026-05-19 — Complete CLAUDE.md standard — template v2.1

- Did: Completed the CLAUDE.md template and standard so the next chunk's AGENTS.md→CLAUDE.md migration has a content-preserving target. Branch `docs/complete-claude-md-standard`. 2 commits.
- Result: CLAUDE-md-template.md is v2.1 (12 sections, 126 lines). §3 Architecture (pure pointer to ARCHITECTURE.md) and §4 Conventions (naming/commits/testing/linting/out-of-scope) added. All stale "CLAUDE.md Section 5 (Tools active)" cross-references in PLAYBOOK.md and codex-review-config-template.md reconciled to named-section references — that label was an AGENTS.md artifact never present in the CLAUDE.md template. Content-distribution map added to PLAYBOOK §CLAUDE.md as part of the documented standard. ADR-53 Decision point 4 already correct — no change needed.
- Changes: `templates/CLAUDE-md-template.md` (v2.1); `protocols/PLAYBOOK.md` (distribution map, section-number fixes, cross-reference heading); `templates/codex-review-config-template.md` (section reference fix).
- Abandoned: Nothing.
- Next: Chunk 4 — remove `.dev-knowledge/AGENTS.md` and `ai-council/AGENTS.md`; merge substantive content into each repo's CLAUDE.md per ADR-53 Decision 2.

---

### 2026-05-19 — Chunk 3: bring standard docs into line with ADR-53

- Did: Updated all live governance docs to retire AGENTS.md convention and establish CLAUDE.md as the single canonical per-repo agent-instruction file per ADR-53. Branch `docs/chunk3-standard-to-adr53`. 8 commits across 8 steps.
- Result: No live governance doc references AGENTS.md prescriptively. PLAYBOOK §CLAUDE.md is the new canonical section (replaces retired §AGENTS.md); dual-read mechanism documented; authority hierarchy updated to 3 levels. CLAUDE-md-template.md is v2.0. AGENTS-md-template.md archived. ADR-53 Decision 4 corrected (thin-pointer framing retired).
- Changes: `docs/decisions/ADR-53` (Decision 4 wording); `templates/CLAUDE-md-template.md` (v2.0, thin-pointer refs removed); `protocols/PLAYBOOK.md` (§AGENTS.md section removed, §CLAUDE.md rewritten, 8 additional stale refs fixed across file); `protocols/ESSENTIALS.md` (ADR-53 citation, Scale L definition); `templates/AGENTS-md-template.md` → `templates/archive/` (retired); `ARCHITECTURE.md` (codemap, living-files list, violation statement, ADR index); `BACKLOG.md` (open-item wording); `README.md`, `VISION.md`, `templates/codex-review-config-template.md`, `templates/prompt-template.md` (sweep cleanup).
- Abandoned: Nothing dropped — all 8 steps completed. AGENTS.md root file and CLAUDE.md instruction file untouched (next chunk per scope constraint).
- Next: Chunk 4 — remove `.dev-knowledge/AGENTS.md` and `ai-council/AGENTS.md`; merge substantive content into each repo's CLAUDE.md per ADR-53 Decision 2.

---

### 2026-05-19 — ADR-53: retire ADR-52, establish CLAUDE.md as single instruction file

- Did: Authored ADR-53 superseding ADR-52. Marked ADR-52 superseded (status line only — body untouched). Updated `docs/decisions/README.md` ADR index and traceability table (ADR-52 and ADR-53 both added; ADR-52 was missing from the index). Branch `docs/adr-53-retire-agents-md`.
- Result: Decision record corrects the false premise in ADR-52 Decision 1 (Claude Code does not auto-read `AGENTS.md`; both active tools read `CLAUDE.md`). Empirical evidence cited: `docs/audits/2026-05-19-cohort1-verification.md`. Three commits: `1d161f0` (ADR-53), `7d70807` (ADR-52 superseded), `bc59e9d` (index).
- Changes: `docs/decisions/ADR-53-claude-md-single-instruction-file.md` (new, 49 lines); `docs/decisions/ADR-52-agents-md-convention.md` (status line only: Accepted → superseded); `docs/decisions/README.md` (4 lines added: two index rows, two traceability rows).
- Abandoned: Nothing — scope held cleanly. No PLAYBOOK/ESSENTIALS edits, no AGENTS.md deletions, no template changes (subsequent chunks).
- Next: (1) Subsequent chunk — remove AGENTS.md from `.dev-knowledge` and `ai-council`, merge content into each repo's CLAUDE.md; (2) update PLAYBOOK/ESSENTIALS, retire AGENTS-md-template.md; (3) resolve open violations from prior session (ai-council CLAUDE.md 200-line trim, corp-monorepo AGENTS.md 10-section form).

---

### 2026-05-19 — ADR-51 + ADR-52 conformance: AGENTS.md + ARCHITECTURE.md

- Did: Created `AGENTS.md` at repo root (10-section ADR-52 contract); rewrote `ARCHITECTURE.md` to ADR-51 template (three CORE sections, corrected stale references). Branch `feat/dev-knowledge-adr51-52-conformance`. Full approved plan with dispositions R1–R6 + R8 applied.
- Result: `.dev-knowledge` now self-conformant with its own ADR-51 + ADR-52 conventions. Two commits: `f8160ac` (AGENTS.md), `58ad1d8` (ARCHITECTURE.md). Pytest 50/51 (known failure unchanged). Ruff clean.
- Changes: `AGENTS.md` (new, 146 lines); `ARCHITECTURE.md` (rewrite: +144 −89 lines, `scale: M` frontmatter, `## Purpose [CORE]`, `## Codemap [CORE]` with CODEMAP markers, `## Layer Boundaries & Invariants [CORE]` with 5 numbered invariants, `## Diagrams [M/L]` stub, governing ADRs extended to ADR-52, deleted-file refs removed R1–R3, scope-tag enforcement clause removed R4, hybrid-ratio bullet removed R5, `version:` frontmatter replaced R6, violation count corrected to two R8).
- Abandoned: R7 (full deletion of violations bullet) — not approved; two violations remain open.
- Next: (1) `ai-council` ARCHITECTURE.md (ADR-51, effort M); (2) `ai-council` AGENTS.md §7 bookkeeping — add ADR-51 + ADR-52 (effort S); (3) resolve open violations — ai-council CLAUDE.md 200-line trim, corp-monorepo AGENTS.md ADR-52 10-section form.

---

### 2026-05-19 — rollout-readiness audit (ADR-51 / ADR-52 gap analysis)
- Did: Independent verification of `.dev-knowledge` `main` against all reported session changes; gap analysis of `.dev-knowledge` and `ai-council` (read-only) against ADR-51 + ADR-52. All 14 session commits verified by SHA. All reported files verified as non-trivial. Path-guard block in `codex-review.ps1` confirmed present. One discrepancy found and classified: Stage 3 handoff named wrong failing test (`test_ratio_pass_when_stable_above_ceiling`); actual failure is `test_audit_run_passes_structural_checks_on_synthetic_repo` — self-diagnosed in JOURNAL, not a repo state error.
- Result: `.dev-knowledge` main VERIFIED as reported. Report at `docs/audits/2026-05-19-rollout-readiness.md`. Branch `audit/rollout-readiness-2026-05-19` merged to main. 50/51 pytest pass (known failure unchanged).
- Changes: `docs/audits/2026-05-19-rollout-readiness.md` (new, 250 lines).
- Abandoned: nothing.
- Next: execute rollout in recommended order — (1) `.dev-knowledge` AGENTS.md (ADR-52, effort M), (2) `.dev-knowledge` ARCHITECTURE.md rewrite to ADR-51 template (effort M), (3) `ai-council` ARCHITECTURE.md (ADR-51, effort M), (4) `ai-council` AGENTS.md §7 bookkeeping — add ADR-51 + ADR-52 (effort S).

---

### 2026-05-19 — codex-review sidequest: misdiagnosis correction + code-only path-guard + empty-diff guard
- Did: Diagnose-first Plan Mode investigation of the operator's report that codex-review was "broken for some time" (stale `gpt-5.2-codex` pin + token-burning hook retries). Phase 1 Explore agents found the entire premise wrong: **no hook exists** (`/codex-review` is a manually invoked slash command, `~/.claude/settings.json` registers no codex hook), **no model pin in the wrapper** (`~/.claude/bin/codex-review.ps1` passes no `--model` flag — CLI default `gpt-5.4` is used; `~/.codex/config.toml` auto-migrates legacy `gpt-5.2-codex` → `gpt-5.4`), **no retry loop** (single `codex exec` call, fails fast). Gating Step 1 live verification (Codex on `c9f796d~1..c9f796d` via unmodified wrapper) PASSED — codex returned a real review on `gpt-5.4`, ~48k tokens. Then layered the real fixes: code-only path-guard (extension allowlist `.py .ps1 .sh .ts .tsx .js .jsx .go .rs .rb .java .cs .cpp .c .h .sql .toml .yaml .yml .json .ini`), empty-diff guard, FullAudit-no-src/ guard — all in `codex-review.ps1`. Updated `~/.claude/commands/codex-review.md` Rules block. Documented the code-only rule in PLAYBOOK §16 + §17 and ESSENTIALS "Ending a Session". Verified end-to-end with five cases (5a pure code, 5b pure markdown, 5c empty diff, 5d mixed, 5e -FullAudit with synthetic markdown in `src/`); all PASS. Test artifacts deleted (zero-finding audits per archival protocol; temp git repo removed).
- Result: codex-review working end-to-end — YES. Branch `fix/codex-review-hook`, one tracked commit `7ef77f0` (docs PLAYBOOK + ESSENTIALS). Three untracked `~/.claude/` runtime edits enumerated in Changes below. 50 of 51 pytest pass — baseline failure `test_audit_run_passes_structural_checks_on_synthetic_repo` (`adr38_baseline`) unchanged, out of scope.
- Changes: `~/.claude/bin/codex-review.ps1` (NEW: code-only path-guard block after diff-range resolution + empty-diff guard + FullAudit-no-src/ guard; both prompt templates now include the "Restrict review to these code files only:" block); `~/.claude/commands/codex-review.md` (Rules: added code-only, empty-diff, FullAudit guard bullets + extension allowlist list); `protocols/PLAYBOOK.md` (§16 Cross-Tool Review: added "Code-only rule" paragraph naming the wrapper as enforcement point; §17 Code Quality Audit Process: added "Scope distinct from per-change codex-review" clarification that monthly audit remains deliberately whole-`src/`); `protocols/ESSENTIALS.md` (step 3 "Ending a Session": appended code-only / doc-only-diff-skipped note). Runtime `~/.claude/` edits are outside this repo's git — recorded HERE is their only durable trace.
- Abandoned: Past-failure archaeology (git/audit history dig for evidence of the actual original breakage). Operator approved skipping it once the live healthcheck confirmed the wrapper is working — the "broken" recollection was a stale memory of a transient model-rejection error pre-CLI-auto-migration, not a current state.
- Next: monitor next real-world use; if the path-guard's extension allowlist proves too narrow (Dockerfile, Makefile, .mk asked for), widen per operator request — design contemplated but not added pending demand. Merge `fix/codex-review-hook` → `main` after closeout commit lands.

---

### 2026-05-19 — Action Plan Directives 1+2+3 executed (ADR-51 template, ADR-52 AGENTS.md, PLAYBOOK scope fix)
- Did: Executed all three directives from `07_ACTION_PLAN.md` of the 2026-05-18 session-sync handoff. **Directive 1a** — read-only inspection of `corp-monorepo/ARCHITECTURE.md` + Mermaid→SVG pipeline (`scripts/render-diagrams.ps1`, 3 `.mermaid` sources, manual render, no CI integration); wrote `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` as the ADR-51-mandated reference input; satisfied content mandatory minimum, flagged absent auto-generation + CI as corp-monorepo's own gap (ADR-36 read-only contract — not resolved here). **Directive 2** — ratified ADR-52 (`AGENTS.md` cross-tool agent-instruction contract convention) formalizing the extant PLAYBOOK convention with the explicit "agent-instruction contract, not handoff artifact" precision. **Directive 3** — added "Handoff scope" precision block to PLAYBOOK §AGENTS.md and a one-liner in ESSENTIALS clarifying that the Claude-oriented handoff process must not narrate/manage AGENTS.md as handoff content. **Directive 1b** — authored `templates/ARCHITECTURE-template.md` (single canonical template per ADR-51, scale conditionals inline, no per-tier variants), appended BACKLOG Stream C P2 entry for the codemap generator output-spec open item, then ran `codex-review` (1 HIGH + 1 MEDIUM + 1 LOW, all legitimate) and fixed forward in one follow-up commit. Two micro-fixes from operator (header/footer date de-duplication + pointer-convention moved to pre-§1) verified in the committed template. Plan-mode used and approved before authoring. Branch flow deviated mid-session (operator-side branch switch during Plan Mode landed me on `main`); per operator decision, proceeded on `main` with codex-review + fix-forward instead of feat-branch + merge.
- Result: 5 commits on `main` this session — `18da5b5` (inspection report, via merged `inspect/corp-monorepo-architecture-reference` FF), `3cc7197` (ADR-52), `1be2f8b` (PLAYBOOK/ESSENTIALS scope fix), `2acaa96` (template), `706c4ba` (BACKLOG entry), `7f0129b` (codex fix-forward + audit artifact). Orphan `feat/architecture-template-adr51` branch deleted (strict ancestor of `main`). 50 of 51 pytest tests pass; the lone pre-existing failure is `test_audit_run_passes_structural_checks_on_synthetic_repo` (`adr38_baseline` synthetic-repo check missing `tests/` + `ARCHITECTURE.md`) — **note:** the Stage 3 `06_STATE_OF_PLAY.md` named `test_ratio_pass_when_stable_above_ceiling` as the known failure; the actual failing test is the audit-baseline one, recorded here so future handoffs cite the right test.
- Changes: `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` (new, 208 lines); `docs/decisions/ADR-52-agents-md-cross-tool-convention.md` (new — added before this session by Directive 2 worker); `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` (Directive 3 precision block + pointer); `templates/ARCHITECTURE-template.md` (new, ~280 lines after codex-fix); `BACKLOG.md` (Stream C P2 codemap-generator entry appended); `docs/audits/2026-05-19-codex-architecture-template.md` (codex audit artifact). Orphan staged `logs/TOKEN-LOG.md` 2026-05-19 ccusage entry left untouched (predates Directive 1b work; flagged for operator review).
- Abandoned: nothing. The feat-branch + merge git workflow specified in Prompt 2 was abandoned mid-stream when operator-side branch switching during Plan Mode landed me on `main`; operator confirmed proceed-on-main as the non-destructive resolution.
- Next: (1) operator decides what to do with the orphan staged `logs/TOKEN-LOG.md` change; (2) Phase 2 rollout — apply `ARCHITECTURE-template.md` to the M/L cohort (corp-monorepo migrates `docs/ARCHITECTURE.md` → root + adapts to template; ai-council adopts; corp-ops trigger-based); (3) codemap generator output spec (BACKLOG Stream C P2) — design the auto-generated graphical codemap artifact and the CI freshness-check hook; until then, child repos hand-maintain the transitional text-tree form documented in the template; (4) ADR-51 remaining open questions (shared-tooling versioning, pilot criteria) still pending.

---

### 2026-05-18 — Handoff Stage 3 complete for .dev-knowledge (session-sync)
- Did: Generated 11-file self-applied handoff bundle for `2026-05-18-dev-knowledge-session-sync`. Verified HEAD `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10` as ancestor of Stage 1 pin (PASS). Caught one VERIFICATION FAILED: Stage 2 claimed "AGENTS.md currently has no canonical template equivalent" but `templates/AGENTS-md-template.md` EXISTS (10 sections); correction recorded in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md` reframed accordingly. Archived stage1/stage2 inputs to `docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/`.
- Result: Bundle ready at `docs/handoffs/2026-05-18-dev-knowledge-session-sync/`. Directives 1/2/3 from `07_ACTION_PLAN.md` validated: ARCHITECTURE-template.md does NOT yet exist (Directive 1 valid); AGENTS.md convention/decision record does NOT exist (Directive 2 valid, template already present); PLAYBOOK/ESSENTIALS AGENTS.md scope clarification pending (Directive 3 valid).
- Changes: `docs/handoffs/2026-05-18-dev-knowledge-session-sync/` (11 files new); `docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/` (stage1-question.md, stage2-response.md archived); `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/` (removed).
- Abandoned: nothing.
- Next: execute `07_ACTION_PLAN.md` Directives 1/2/3 — author `templates/ARCHITECTURE-template.md` (inspect corp-monorepo first); decide AGENTS.md convention + verify existing template; update PLAYBOOK + ESSENTIALS re: AGENTS.md scope.

---

### 2026-05-18 — Handoff Stage 1 generated (session-sync)
- Did: Generated Stage 1 handoff for `.dev-knowledge` session-sync. Captured HEAD `aeaf158`, clean working tree. Created `_in_progress/2026-05-18-dev-knowledge-session-sync/` with stage1-question.md and stage2-response.md placeholder.
- Result: Stage 1 complete; awaiting Stage 2 architect response from old chat.
- Changes: `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/stage2-response.md` (placeholder, new).
- Abandoned: nothing.
- Next: Rob takes stage1-question.md paste block to old browser chat; pastes response into stage2-response.md; says "complete handoff for dev-knowledge".

---

### 2026-05-18 — ADR-51 architecture-doc convention + automated distillation rule
- Did: Committed architecture-documentation convention ADR from 2026-05-18 Council debate. Transcript already untracked in `docs/decisions/transcripts/` — committed first. Verified ADR number as 51 (highest filed was ADR-50). Aligned draft to `templates/ADR-template.md` (number substitution + Source field; no content changes). Added ADR-51 row + traceability entry to `docs/decisions/README.md`. Recorded ADR distillation as a mandatory automated post-debate step in PLAYBOOK § 5 "Post-debate protocol"; added one-liner pointer in ESSENTIALS.md "Artifact generation direction". 51 tests passed.
- Result: 3 commits on `docs/architecture-doc-adr`: `23652c1` (transcript), `a552454` (ADR-51 + index), `949e9f5` (process rule). Branch merged to `main` with `--no-ff`.
- Changes: `docs/decisions/transcripts/council-out-20260518_215241-pick-2026-05-18_council-debate-architecture-doc.md` (new); `docs/decisions/ADR-51-architecture-doc-convention.md` (new); `docs/decisions/README.md` (ADR-51 index + traceability rows); `protocols/PLAYBOOK.md` (post-debate protocol step 2 expanded); `protocols/ESSENTIALS.md` (Council ADR distillation pointer).
- Abandoned: nothing.
- Next: create `templates/ARCHITECTURE-template.md`; review `corp-monorepo` existing `ARCHITECTURE.md` + C4 pipeline as input to template and codemap generator design.

---

### 2026-05-18 — Handoff Stage 1 generated for ai-council
- Handoff Stage 1 generated for `2026-05-18-ai-council-session-sync`: HEAD `ce885827aada41f582e784fa210f73ff125a18de` captured; awaiting Stage 2.
- Changes: `docs/handoffs/_in_progress/2026-05-18-ai-council-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-18-ai-council-session-sync/stage2-response.md` (placeholder).

---

### 2026-05-18 — ADR-38 A4 + PLAYBOOK AGENTS.md taxonomy fix
- Did: Appended A4 amendment to ADR-38 closing the corp-monorepo `ARCHITECTURE.md` root-placement migration deferral (A3, 2026-05-11) — deferral is now expired as the universalization rollout executes the move. Corrected PLAYBOOK file-type taxonomy entry for `AGENTS.md`: was "Cross-tool canonical governance" (inaccurate); now "Codex agent-instruction config; per-repo specifics — cross-tool canonical governance is CLAUDE.md + PLAYBOOK/ESSENTIALS". 51 tests passed.
- Result: two commits on `docs/close-architecture-deferral`: `5dc7f29` (ADR-38 A4), `d1dac86` (PLAYBOOK taxonomy fix).
- Changes: `docs/decisions/ADR-38-universal-repo-architecture.md` (A4 appended); `protocols/PLAYBOOK.md` (taxonomy row corrected).
- Abandoned: nothing.
- Next: merge `docs/close-architecture-deferral` to main; proceed with corp-monorepo rollout (Workstreams B/C/D + ARCHITECTURE→root move).

---

### 2026-05-18 — .dev-knowledge session-sync: monorepo rollout prep + scoping
- Did: **Directive 1** — verified ecosystem audit state from Stage 3 handoff; specifically resolved the "possible third governance ADR" (governance-trim) that was unconfirmed in Stage 3. Read-only; no commit. **Directive 2** — wrote `docs/audits/2026-05-17-corp-monorepo-governance-rollout-plan.md`: a phase-by-phase plan rolling the `.dev-knowledge` documentation-governance simplification (ADR-48/49/50) into `corp-monorepo`; two follow-up fix commits reconciled Phase 8 cross-layer write and Q3 review default vs. single-branch model. **Directive 3** — wrote `docs/research/2026-05-17-kimi-k2-scoping.md`: scoping note for incorporating Kimi K2 (Moonshot AI MoE model) into the ai-council panel — covers integration surface, test checklist, and open questions; no implementation. **Directive 4** — wrote `docs/audits/2026-05-17-skills-hooks-usage-review.md`: ecosystem review of all skills and hooks; found `verify` skill is a stub, project-level gotchas pattern exists only in corp-monorepo, no project-level hooks anywhere; surfaced 5 recommendations for a future session.
- Result: rollout plan on disk (`docs/corp-monorepo-rollout-plan` branch, 3 commits: `0faf5a2`, `5ee4193`, `fe4140a`); scoping notes on `docs/session-scoping-notes` branch (2 commits: `99c784f`, `d00c7ff`). Neither branch merged to main yet.
- Changes: `docs/audits/2026-05-17-corp-monorepo-governance-rollout-plan.md` (new); `docs/research/2026-05-17-kimi-k2-scoping.md` (new); `docs/audits/2026-05-17-skills-hooks-usage-review.md` (new).
- Abandoned: nothing.
- Next: merge both branches to main; run corp-monorepo rollout execution in a dedicated session using the rollout plan as spec; evaluate Kimi K2 API access before scheduling integration session; fill `verify` skill body (low effort, Directive 4 recommendation M).

---

### 2026-05-17 — Handoff Stage 3 complete for .dev-knowledge (session-sync)
- Did: generated full 11-file self-applied handoff bundle for `2026-05-17-dev-knowledge-session-sync`; archived `_in_progress/` inputs to `docs/handoffs/archive/`; verified HEAD `9a911952aa9c912218c839f54317170e647a5f44` is descendant of Stage 1 pin `c784845c659a98c59f2c161301577d72e17a4801` (ancestor check PASS, no drift).
- Result: handoff bundle ready for Rob to upload to new `.dev-knowledge` browser chat. Stage 3 verified architect's witnessed claims about branch-cleanup outcome (`git branch` shows `main` only at HEAD) and partial verification of "3 governance ADRs filed" claim (ADR-46 + ADR-47 confirmed present; possible third "governance-trim" ADR unconfirmed — passed through to Directive 1).
- Changes: `docs/handoffs/2026-05-17-dev-knowledge-session-sync/` (11 files: 00_README.md, 00_first-message.md, 01_MANIFEST.md, 01_manifest.json, 02_VISION.md, 03_PLAYBOOK.md, 04_ESSENTIALS.md, 05_GOVERNANCE_ESSENCES.md, 06_STATE_OF_PLAY.md, 07_ACTION_PLAN.md, 08_TREE.txt, 09_EXECUTION_EVIDENCE.md); `docs/handoffs/archive/2026-05-17-dev-knowledge-session-sync/` (stage1-question.md + stage2-response.md moved from _in_progress).
- Abandoned: nothing.
- Next: Rob opens NEW `.dev-knowledge` browser chat, uploads bundle, pastes 00_first-message.md as first message, completes articulation gate + synthesis confirmation, runs generated prompts in Claude Code.

### 2026-05-17 — Handoff Stage 1 generated for .dev-knowledge
- Handoff Stage 1 generated for `2026-05-17-dev-knowledge-session-sync`: HEAD `c784845c659a98c59f2c161301577d72e17a4801` captured; awaiting Stage 2.
- Changes: `docs/handoffs/_in_progress/2026-05-17-dev-knowledge-session-sync/stage1-question.md` (new); `docs/handoffs/_in_progress/2026-05-17-dev-knowledge-session-sync/stage2-response.md` (placeholder).
- Next: Rob pastes `stage1-question.md` PASTE_BOUNDARY block into OLD `.dev-knowledge` browser chat; fills `stage2-response.md`; then "complete handoff for .dev-knowledge".

---

### 2026-05-17 — Document audit test fixtures
- Did: assessed `tests/fixtures/` documentation state; found no README or other discoverable explanation of the fixtures directory. Created `tests/fixtures/README.md` covering what the directory is, the naming convention, an inventory of the one current fixture (`repo-with-structural-checks`) with the test that consumes it, and the maintenance rule tying fixture lifecycle to audit check changes. Committed to branch `docs/document-test-fixtures` branched from `feat/handoff-ai-council-2026-05-17` (which holds fixture rename `c0b7512`).
- Result: `tests/fixtures/README.md` added (`d0c8169`). Branch left unmerged, unpushed.
- Changes: `tests/fixtures/README.md` (new).
- Abandoned: nothing.
- Next: review and merge `docs/document-test-fixtures` into `feat/handoff-ai-council-2026-05-17` or main when ready.

---

### 2026-05-17 — Consolidate the Stage 2 handoff instruction set
- Did: created `docs/consolidate-handoff-template` branch; restructured the Stage 2 instruction set in `templates/HANDOFF_QUESTION_TEMPLATE.md` from 3 "CRITICAL" sections + 7 during-drafting rules + 3 pre-send checks into four numbered parts under one "How to write the response" heading — (1) Epistemic honesty kept as-is, (2) Self-containment with opening principle plus deduplicated rules (old rules 2+3 merged; old rule 5 corrected per Finding 2 to apply only to files not already in the bundle; concision cue per Finding 3 folded in; old pre-send checks 1+3 absorbed into the closing audience-simulation paragraph), (3) Coherence check kept standalone, (4) Format requirements kept as-is; three CRITICAL banners collapsed to one framing paragraph. Then reframed RATIONALE per Finding 1 — section framing question now allows "Unknown" as an acceptable answer; epistemic note made the non-answer explicitly preferred over a constructed rationale; new generation rule requires the `{customized_rationale_prompt}` placeholder to be materialized with non-presupposing "If you witnessed the reasoning for X, state it; otherwise mark Unknown" phrasing. Built a 16-row mapping table BEFORE rewriting to guarantee no rule's substance was dropped; re-checked it against the rewritten file after. 2 commits.
- Result: same substance, stated once. Stage 2 instructions now have 4 named parts instead of 13+ scattered items. Mapping table confirms every original rule's substance survives. No change to the 3-stage process or to ADR-42. Branch left unmerged, unpushed per prompt spec.
- Changes: `templates/HANDOFF_QUESTION_TEMPLATE.md` (Stage 2 instruction block restructured; RATIONALE section + generation rules updated).
- Abandoned: none.
- Next: empirical test on the next real Stage 2 — does the consolidated version actually hold in one's head and reduce drift? If yes, keep; if not, iterate on what slipped through.

---

### 2026-05-17 — Handoff Stage 3 complete for ai-council (session-sync)
- Did: generated full 13-file handoff bundle for `2026-05-17-ai-council-session-sync`; archived `_in_progress/` inputs to `docs/handoffs/archive/`; verified ai-council HEAD `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` (ancestor check PASS, no drift).
- Result: handoff bundle ready for Rob to upload to new ai-council browser chat. Pre-resolved: `docs/HANDOFF.md` confirmed absent (Stage 3 verification). AGENTS.md absence flagged as governance gap (Council #28) and captured in Directive 2.
- Changes: `docs/handoffs/2026-05-17-ai-council-session-sync/` (13 files: 00_README.md, 00_first-message.md, 01_MANIFEST.md, 01_manifest.json, 02_VISION.md, 02b_ECOSYSTEM_VISION.md, 03_PLAYBOOK.md, 04_ESSENTIALS.md, 05_GOVERNANCE_ESSENCES.md, 06_STATE_OF_PLAY.md, 07_ACTION_PLAN.md, 08_TREE.txt, 09_EXECUTION_EVIDENCE.md); `docs/handoffs/archive/2026-05-17-ai-council-session-sync/` (stage1-question.md + stage2-response.md moved from _in_progress).
- Abandoned: nothing.
- Next: Rob opens NEW ai-council browser chat, uploads 12 files (all except 00_README.md), pastes 00_first-message.md as first message, confirms synthesis, runs generated prompts in Claude Code.

### 2026-05-17 — Fixture cleanup + Stage 1 regeneration for ai-council
- Did: renamed stale test fixture `repo-with-all-five-checks` → `repo-with-structural-checks`; updated its internal VISION.md (stale "all five checks" description → accurate 3-check description); deleted two stale fixture files (`BACKLOG_ARCHIVE.md`, `CHANGELOG.md`) left over from `deedc10` audit-check removal; updated `tests/test_audit.py` fixture path reference. Regenerated `stage1-question.md` for `2026-05-17-ai-council-session-sync` with current template structure (coherence-check concern added, RATIONALE sub-questions reframed as non-presuppositional per template spec).
- Result: 28 tests pass. `stage1-question.md` now faithful to current template structure. `stage2-response.md` placeholder preserved unchanged.
- Changes: `tests/fixtures/repo-with-structural-checks/` (renamed from `repo-with-all-five-checks/`; VISION.md updated; BACKLOG_ARCHIVE.md + CHANGELOG.md deleted), `tests/test_audit.py` (fixture path), `docs/handoffs/_in_progress/2026-05-17-ai-council-session-sync/stage1-question.md` (regenerated).
- Abandoned: nothing.
- Next: Rob pastes `stage1-question.md` PASTE_BOUNDARY block into OLD ai-council browser chat; fills `stage2-response.md`; then "complete handoff for ai-council".

### 2026-05-17 — Handoff Stage 1 generated for ai-council
- Handoff Stage 1 generated for `2026-05-17-ai-council-session-sync`: HEAD `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` captured; awaiting Stage 2

### 2026-05-17 — Decommissioning discipline: close the orphan gap
- Did: created `feat/decommissioning-discipline` branch; added decommissioning-gap lesson to LESSONS.md; added "Supersession & decommissioning" subsection to PLAYBOOK.md (under Documentation file types); added condensed supersession rule to ESSENTIALS.md; created `templates/ADR-template.md` with `Decommission:` header field. 4 commits total.
- Result: audit health passes. All 4 doc files updated consistently. Branch left unmerged, unpushed per prompt spec.
- Changes: `LESSONS.md` (new entry prepended), `protocols/PLAYBOOK.md` (new ### subsection), `protocols/ESSENTIALS.md` (new ## section), `templates/ADR-template.md` (new file).
- Abandoned: nothing.
- Next: review branch on main and merge when ready; backfill `Decommission:` field on any existing ADRs that supersede or relocate artifacts (starting with ADR-42 handoff centralization).

### 2026-05-16 — Council Simplification slice: .dev-knowledge governance trim
- Did: applied AI Council simplification verdict to `.dev-knowledge` on `feat/docs-governance-simplification` over 6 commits (Steps 2–7). Trimmed `scripts/audit.py` to structural-only checks (vision_md / adr38_baseline / claude_md); deleted CHANGELOG.md + BACKLOG_ARCHIVE.md; demoted ADR-46 + ADR-47 to non-enforced conventions; added deterministic `scripts/normalize_headers.py` + pre-commit auto-format hook; removed the scope-tag enforcement system (`validate_scope_tags.py`, tests, pre-commit hook, CLAUDE.md vocabulary section); documented git-as-changelog + Conventional Commits standard + new `Did/Result/Changes/Abandoned/Next` JOURNAL shape.
- Result: tests 51 passed / 0 failed (was 53 passed / 3 failing). `ruff` clean. Audit output no longer references CHANGELOG / BACKLOG_ARCHIVE / dated-entries / backlog-organization checks. Branch left at `1401618` + this JOURNAL commit; NOT merged, NOT pushed.
- Changes: `scripts/audit.py`, `scripts/normalize_headers.py` (new), `tests/test_audit.py`, `tests/test_normalize_headers.py` (new), `tests/test_validate_scope_tags.py` (deleted), `tests/fixtures/{backlog-*,dated-entries-*}/` (deleted), `scripts/validate_scope_tags.py` (deleted), `CHANGELOG.md` + `BACKLOG_ARCHIVE.md` (deleted), `docs/decisions/ADR-46-*.md` + `ADR-47-*.md` (condensed), `.pre-commit-config.yaml`, `CLAUDE.md`, `CONTRIBUTING.md`, `protocols/ESSENTIALS.md`, `.claude/commands/save.md`, `JOURNAL.md` (this entry + intro rewrite).
- Abandoned: keeping per-entry required-fields check in `check_backlog_organization` — flagged as marginal in the Step 2 commit body; classified as entry-body format-detail and removed. If you want it back as a structural check, the call is in the Step 2 commit body. Pre-existing `adr38_baseline` FAIL (`.dev-knowledge` lacks `src/` + `pyproject.toml`) NOT addressed — out of scope for this branch; surfaced for separate triage.
- Next: morning review of branch `feat/docs-governance-simplification` (7 commits incl. this JOURNAL entry). On approval: rebase / merge to main; otherwise raise the flagged-ambiguity (required-fields-per-entry) and any rollback of demoted ADRs.

---

### 2026-05-16 — Session D: .dev-knowledge ADR-46+47 cleanup complete
- Resolved all 5 FAIL groups from 2026-05-15 dogfood audit: dated_entries_lessons +
  dated_entries_changelog now PASS; BACKLOG_ARCHIVE.md created; 15 entries extracted;
  8 Why: fields added; no [done] tokens in active BACKLOG. Two hidden tail-ordering
  issues surfaced (LESSONS.md and CHANGELOG.md) — fixed in scope.
- Deferred WARNs accepted: Cross-stream 41% (structural; Stream taxonomy grooming P2
  item added for quarterly grooming 2026-07-01); adr38_baseline FAIL is pre-existing
  out-of-scope. Branch: feat/cleanup-adr-46-47-dev-knowledge — awaiting merge approval.

---

### 2026-05-15 — ai-council cleanup handoff bundle dispatched (D2)
- Generated 12-file cross-repo handoff bundle at `docs/handoffs/2026-05-15-ai-council-cleanup/`;
  ADR-42 v3.3.2 format + `02b_ECOSYSTEM_VISION.md` for cross-repo case
- Bundle carries locked migration decisions: `[blocked]`→`[open]`+annotation (ADR-47 vocab);
  session-numbered envelope→ISO (ADR-46); ready for ai-council Claude Code session to consume
- BACKLOG Stream B P1 items annotated in-flight; verification via `.dev-knowledge` re-audit
  post-execution; Session D complete after clean audit pass

---

### 2026-05-15 — Audit Tool P2: ADR-46 + ADR-47 checks + extraction script shipped (Session E)
- `check_dated_entries_format` (ADR-46) + `check_backlog_organization` (ADR-47) + `backlog_extract.py`
  implemented; 56 tests passing; audit tool now 5 checks (was 3)
- Dogfood: 51 checks across `.dev-knowledge` + `ai-council` — 6 pass / 42 fail / 3 warn;
  ai-council git status clean (ADR-36 read-only contract intact)
- Session D scope inventoried: 4 new BACKLOG items (Stream C P1 x2 + Stream B P1 x2)
  anchoring ADR-46/47 cleanup across both repos; extraction script ready for `[done]` extraction

---

### 2026-05-15 — Governance ADRs B+C ratified (ADR-46 + ADR-47)
- Council pipeline (research + pick) executed for both entries; ADR-46 (cross-repo
  dated-entries format) winner B-1 Lightweight Hybrid + sniff-test; ADR-47
  (cross-repo BACKLOG organization) winner C-2 Stream-grouped + Two-file state with
  operational hardening (session-start validator, deterministic script not LLM prompt)
- BACKLOG Stream C P1 Entry 1 + Entry 2 → [done]; Stream C P2 ADR-29 prepend item →
  [superseded] by ADR-46; new Stream C P3 ADR-41 amendment sub-item added
- Files unchanged in this session — Session D (cleanup pass across all repos) and
  Session E (audit tool extension + extraction script) are downstream

---

### 2026-05-15 — Audit Tool P1 MVP shipped
- `scripts/audit.py` CLI (4 commands per ADR-36), ecosystem state schema (`ecosystem/{repo}/state.yaml`
  + `history/`), 3 checks (vision_md, adr38_baseline, claude_md), markdown report to `docs/audits/`
- 27 tests passing; ruff clean; pre-existing test failure unchanged
- Self-audit: `.dev-knowledge` FAIL — `adr38_baseline` missing `src/` + `pyproject.toml` (governance
  repo, not code repo — new BACKLOG Stream C P2 item). Cross-repo: `ai-council` PASS/WARN
  (ARCHITECTURE.md optional, absent)
- Pre-flight gate value confirmed: inferred mandatory-files list in handoff draft was wrong
  (LESSONS.md/JOURNAL.md not universal per ADR-38; src/tests/pyproject.toml missing from inferred
  list). ADR-38 canonical spec used for implementation.
- BACKLOG Stream C P1 "Audit tool P1 implementation" marked [done]

---

### 2026-05-15 — Handoff validation v3.3.3
- Replaced strict-equality HEAD check with ancestor check (`git merge-base --is-ancestor`) across
  template surfaces and HANDOFF_PROCESS; bumped v3.3.2 → v3.3.3
- Empirically verified on 2026-05-15 case: `b640bcf9` confirmed ancestor of `777af78` (exit 0)
- Unblocks: Audit Tool P1 (A) inherits clean handoff workflow; eliminates manual operator override
  on every future handoff

---

### 2026-05-15 — Session close: v3.3.2 template fix + ai-council bundle regenerated
- Template fix implemented: `templates/HANDOFF_FOLDER_TEMPLATE.md` parameterized for cross-repo
  use (`{repo}` in gate #1; target VISION as 02_VISION source; conditional 02b_ECOSYSTEM_VISION);
  Bug C fixed (BOUNDARIES → Hard Constraints). HANDOFF_PROCESS bumped v3.3.1 → v3.3.2.
- ai-council bundle regenerated in-place (13 total files including new 02b_ECOSYSTEM_VISION.md);
  broken state preserved in git history at `c09ee71`.
- Mandatory cross-case trace verification executed before template commit — both traces passed.
- BACKLOG v3.3.2 entry marked [done]. Preceding session work already landed: directive #3
  PLAYBOOK additions merged `72f486e`; LESSON #9 captured `5b51cdc`; LESSONS canonical rewrite `99a104e`.

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

### 2026-05-12 — Inline reminder questions added to Stage 1 questionnaire
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

### 2026-05-12 — Universal handoff self-containment rule added to HANDOFF_PROCESS
- Did: added Universal Self-Containment Rule section to HANDOFF_PROCESS.md covering Stage 1 packaging / Stage 2 generation / Stage 3 reception with per-section scope rules + pre-send coherence checklist + ADR-41 per-repo scope reference; appended LESSON capturing empirical failure observed in session as universal pattern (not repo-specific)
- Result: handoff process rule now universal across all repos handoff lifecycles; structurally prevents repeating cross-repo-in-DIRECTIVES failure in any future handoff (corp-monorepo, ai-council, future child repos)
- Next: BACKLOG cross-repo contamination cleanup (separate concern; operator-confirmed scope only)

### 2026-05-12 — Hooks reconnaissance + ai-council check
- Did: produced docs/audits/2026-05-12-hooks-discovery.md; identified review name-conflict location(s) — user-defined `~/.claude/commands/review.md` (Codex wrapper) vs. Claude Code built-in `/review` skill (PR review); recommended Shape (a) for Prompt 4; confirmed ai-council implemented all 10 scrum-master findings + I7/I8 addendum + council-out-* emitter rename
- Failed: —
- Next: hooks review proper (Prompt 4) — scope locked by recon findings (Shape a, low effort)

### 2026-05-12 — PLAYBOOK § 17 + cover-letter template
- Did: added § 17 Scrum-Master Review Propagation + templates/scrum-master-cover-letter.md; closed BACKLOG P2 propagation-structuring entry
- Failed: —
- Next: hooks reconnaissance (Prompt 3) → hooks review proper (Prompt 4, scope locked by recon findings)

### 2026-05-12 — Cleanup pass
- Did: resolved orphaned 2026-05-12-session-handoff deletion (D2 — already committed as 471ecd3); marked ADR-34 ai-council propagation BACKLOG entry as done (D3); added ADR-42 single-vs-multi-artifact amendment-candidate BACKLOG entry P3 (D7)
- Failed: —
- Next: PLAYBOOK § 17 + scrum-master cover-letter template (Prompt 2)

### 2026-05-12 — Handoff Stage 3 complete for ai-council (session-sync)

**Did:** Stage 3 generated 12-file handoff folder at `docs/handoffs/2026-05-12-ai-council-session-sync/`. Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-12-ai-council-session-sync/`. HEAD `f094d08` pinned (no drift). Stage 2 architect knowledge preserved: Step 5 smoke test as next action, cost-optimization principle captured, 12 witnessed claims verified against repo state, stale BACKLOG items flagged. BACKLOG items updated.

---

### 2026-05-12 — Handoff Stage 1 generated for ai-council (session-sync)

- Handoff Stage 1 generated for `2026-05-12-ai-council-session-sync`: HEAD `f094d0821a279f3aa36de554943c1b44576d0924` captured; awaiting Stage 2

---

### 2026-05-12 — Handoff Stage 3 complete for dev-knowledge (session-sync)

**Did:** Stage 3 generated 11-file handoff folder at `docs/handoffs/2026-05-12-dev-knowledge-session-sync/`. Stage 1+2 inputs archived. HEAD `0125f1b` pinned. Stage 2 architect knowledge (10 boundaries, 8 directives) captured. CHANGELOG updated.

---

### 2026-05-12 — Handoff Stage 1 generated for dev-knowledge (session-sync)

**Did:** Handoff Stage 1 generated for slug `2026-05-12-dev-knowledge-session-sync`; HEAD `ec44148` captured; awaiting Stage 2 (old chat response).

---

### 2026-05-12 — Prompt N: Session handoff generated

**Did:** Composed session handoff at `docs/handoffs/2026-05-12-session-handoff/` covering session scope (14 commits, 7 prompt cycles), state at end, operator pending actions, deferred substantive work, and critical process principles. Verified browser-provided inventory against repo state; flagged one adjusted item (`2026-05-11-cross-repo-pattern-audit.md` not found in `docs/audits/` — browser claim adjusted).

**Result:** Fresh-session context primer ready (49 lines); next chat reads handoff as session-start input.

**Next:** Fresh session picks up handoff; substantive work (skills review + hooks audit + token logging + methodology proposal review + Phase 2 cross-repo migrations) starts with clean context.

---

### 2026-05-12 — Prompt M: Governance freshness audit + targeted updates

**Did:** Read-audited 8 governance files (ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md, README.md, VISION.md, PLAYBOOK.md, ESSENTIALS.md, HANDOFF_PROCESS.md) plus subdirectory READMEs for stale convention references post 2026-05-11 amendments (ADR-34 universal hyphen mandate + ADR-38 ARCHITECTURE.md root placement + A2 archive folder rename). Applied 10 targeted fixes across 4 files (ARCHITECTURE.md × 2, CONTRIBUTING.md × 2, README.md × 2, PLAYBOOK.md × 4). Added 1 new BACKLOG entry (Cross-stream P2: scrum-master review propagation process codification).

**Result:** Governance docs aligned with ratified amendments; all `ADR-NN_` underscore prescription references updated to `ADR-NN-` hyphen; PLAYBOOK §File naming conventions TBD block replaced with ADR-34 pointer; archival step filenames updated to council-out-* format. VISION.md, ESSENTIALS.md, HANDOFF_PROCESS.md, CLAUDE.md — no stale references found.

**Next:** Handoff to fresh session for substantial new scope (skills review + hooks review + token logging + methodology proposal review + Phase 2 cross-repo migrations).

---

### 2026-05-12 — Prompt L: Scrum-master review of ai-council + legacy transcripts relocation

**Did:**
- Produced structured scrum-master review report for ai-council at `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (Scale M; first empirical instance of scrum-master review authority pattern): 10 findings (1 critical, 6 important, 3 minor); covers governance files, ADR-34 compliance, documentation staleness, tasks/ folder hygiene, dead code scan, folder structure
- Relocated 3 legacy `DECISION_NN_*` transcripts from `docs/decisions/transcripts/` to `docs/decisions/transcripts/archive/legacy/` (pre-CLI historical class separation per content-scoped archival principle); updated path references in ADR-31, ADR-32, decisions/README.md, CHANGELOG.md
- Updated BACKLOG: marked AI Council transcript routing [done]; added Cross-stream P2 (codify scrum-master review pattern) + P3 (extend to other repos)
- Appended LESSON: scrum-master review authority pattern (first empirical instance)

**Result:** ai-council review report ready for operator routing to architect. Legacy transcript cleanup complete. Branch merged to main.

**Next:** Operator routes ai-council review to architect for implementation. Scrum-master pattern awaits N=2 before ADR-level codification (see BACKLOG Cross-stream P2).

---

### 2026-05-12 — Prompt K: Atomic file-level cleanup

**Did:**
- K1 (a95318d): 16 ADR renames (underscore → hyphen); 14 transcript renames (council_out_ → council-out-); `docs/handoffs/_archive/` → `archive/` folder rename; 6 legacy flat .md + v2 folder relocated to `docs/handoffs/archive/legacy/`; 23 living docs updated (link refs, path refs, naming convention desc); scope tag validator: pass
- K2 (this commit): BACKLOG P1 `.dev-knowledge atomic migration` marked done; LESSONS: 2 new entries (merge/cleanup completion pattern, punted-migration anti-pattern); JOURNAL + CHANGELOG updated
- K1.4 skipped: cycle 2 propagation artifact absent from Downloads (not present at time of execution)
- Branch: `chore/atomic-cleanup-hyphen-migration` (2 commits, ready for K3 merge)

**Result:** .dev-knowledge file-level mess fully resolved. All upstream decisions (ADR-34 amendment + A2 + Council ratification) now have matching file-level state. Clean working tree on branch.

**Next:** K3 merge to main. Then: cross-repo handshake (BACKLOG P1 — operator routes to ai-council); Phase 2 migrations per BACKLOG P2 entries.

---

### 2026-05-12 — Prompt J: ADR-34 + ADR-38 amendments + BACKLOG reclassification + content-scoped archival principle

**Did:**
- J1: Amended ADR-34 — separator convention changed to universal hyphen mandate for filenames AND foldernames across .dev-knowledge and all child repos; ADR and transcript table rows updated from underscore to hyphen; example set added; scope changed from mandate/recommendation split to universal; Amendments trail added (commit ec45b2c)
- J2: Amended ADR-38 — ARCHITECTURE.md root placement now explicit (was unspecified); conversational A3 decision; Amendments trail added (commit f264966)
- J3: BACKLOG updated — Prompt H entries added in reclassified state (2 marked done: ADR naming + ARCHITECTURE.md placement; 2 kept open: handoff format + undiscovered repos; archive convention marked done per Council vote; A5 designated legacy/opportunistic); 7 new migration sequence entries added (P1 Prompt K atomic migration, P1 cross-repo handshake, P2 CI enforcement, P2 corp-monorepo migration expanded, P2 ai-council migration expanded, P2 content-scoped archival codification, P3 A5 Phase 2 retirement); LESSONS entry appended (content-scoped archival principle); JOURNAL + CHANGELOG updated
- Branch: chore/adr-34-amendment-hyphen-convention (3 commits ahead of main)

**Result:** ADR-34 + ADR-38 ratified per Council decision and operator A3 decision; migration work scoped into Prompt K (.dev-knowledge atomic, includes _archive/ → archive/ rename + propagation artifact archival); content-scoped archival principle captured as BACKLOG P2 awaiting second empirical instance

**Next:** Operator routes cross-repo notification artifact to ai-council; Prompt K executes .dev-knowledge atomic migration

---

### 2026-05-11 — Item 0 epilogue: session-close artifacts
- Did: appended 4 LESSONS entries (codex M1 prompt-craft, M2/L3 bundle staleness, press-back posture validation, advisory framing leakage); added BACKLOG Cross-stream P2 entry for handoff framing receiver-behavior leakage
- Result: 2026-05-11 session lessons captured; empirical finding tracked for future classification
- Next: ported to main 2026-05-17 from chore/session-close-lessons-backlog

---

### 2026-05-11 — Item 0 Prompt C: Codex M1 fix
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
