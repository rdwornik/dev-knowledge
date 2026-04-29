# Changelog — Dev Knowledge

Notable changes to the dev practice knowledge base.

---

## 2026-04-29 — ADR-34 file naming convention (cross-repo)

**Added:**
- ADR-35 lessons base activation (storage + retrieval + querying; promotion deferred to ADR-36)
- ADR-34 file naming convention (cross-repo) — universalization per ADR-33 pattern

---

## 2026-04-28 — ADR-33 VISION.md universalization across ecosystem repos

**Added:**
- `docs/decisions/ADR-33_vision_universalization.md` — formalizes VISION.md as mandatory for any Dev/ repo with ≥1 dependent. Two content tiers (Standard 6-section / Lite 4-section), frontmatter `tier:` field required, trigger-based enforcement (AGENTS.md read-order as baseline; auditor tool in Phase 3). Immediate cohort: ai-council + corp-monorepo. Trigger-based: corp-ops + corp-sca-time-automation by 2026-06-30. Source: Council debate `council_out_20260428_162415_*`.

---

## 2026-04-28 — Heavy audit, VISION.md + ARCHITECTURE.md, Council convention reflection

**Added:**
- `CONTRIBUTING.md` — branch/commit/validator/ADR/handoff conventions for sole-contributor workflow (df637c3, predecessor commit folded in).

**Changed:**
- Heavy audit: `VISION.md` + `ARCHITECTURE.md` added; lessons appended (6); Council output convention reflected in CLAUDE.md / ESSENTIALS.md / PLAYBOOK.md §5; PLAYBOOK §12 cap language → trigger language; framing updates in README/CLAUDE/ESSENTIALS to reflect "universal brain" mission (knowledge guardian, methodology author, auditor); LESSONS.md format normalization for 4 post-ADR-29 multi-line entries (content preserved, structure standardized); PLAYBOOK §13 stale notice on Handoff + Snapshots/reports rows; `scripts/validate_scope_tags.py` IN_SCOPE_FILES expanded with VISION.md + ARCHITECTURE.md; hybrid ratio steady at 18%.

---

## 2026-04-28 — HANDOFF_PROCESS.md v2.0 rewrite (closes Stream C session 1 pending 2a)

- **`protocols/HANDOFF_PROCESS.md`** rewritten end-to-end (v1.x → v2.0) as the operational counterpart of ADR-32. Replaces single-file Type A/B framing and 3-artefact decomposition with: folder-format convention, 9-section `HANDOFF.md` structure (table form), point-in-time governance copies, `manifest.json` schema v1.0, generation/resume workflows, walk-out acceptance test, legacy migration note. Adds the operational mechanics ADR-32 §6 deferred: extract-to-task protocol with hard "Defer requires explicit justification" rule. Documents ADR-32 §6 diagram errata (HANDOFF.md location: live example wins; ADR not amended — flagged for a future Council session).
- **Trigger expansion:** message-cap (~40), time-cap (~2h), and stop-sign signals (scope creep, topic shift, multiple unresolved follow-ups) all fire checkpoint handoffs. JOURNAL workday-close prepend documented as a *separate* artefact, not a folder handoff.
- **`templates/HANDOFF_TEMPLATE.md`** rewritten as a 9-section fillable skeleton matching the new structure.
- **Cross-references:** `CONTRIBUTING.md` "rewrite pending" notice removed; `PLAYBOOK.md §8` gets a stale notice pointing to HANDOFF_PROCESS.md v2.0 (substantive §8 rewrite deferred to its own session).
- Closes Stream C session 1 final HANDOFF pending item **2a**.

---

## 2026-04-28 — Stream C session 1: ADR-31 authority model + ADR-32 handoff format

- **ADR-31** (`docs/decisions/ADR-31_authority_model.md`): formalizes `.dev-knowledge` as binding source of cross-repo prescriptions. Authority model = Prescriptive with conformance audit (1B). Enforcement: centralized out-of-band `tools/audit.py`, read-only, `repos.toml` manifest, green-baseline prerequisite (3 known violations fixed before launch). Scale M + ARCHITECTURE.md only. Content stays in PLAYBOOK + ADRs (`cross-repo/` subfolder deferred past ~10 prescriptions).
- **ADR-32** (`docs/decisions/ADR-32_handoff_format.md`): formalizes browser/agent role split, session charter, step-verification handshake, 9-section handoff standard, folder-format convention (`contents/` + `manifest.json` + `tree.txt`), AGENTS.md as canonical cross-tool governance (Council #28). Consequences note: `protocols/HANDOFF_PROCESS.md` rewrite is a follow-up task (separate session, not yet scheduled).

Source: Council debates Topics 1 and 2 (`docs/decisions/transcripts/DECISION_28_authority_model.md`, `DECISION_29_handoff_synergy.md`).

---

## 2026-04-27 — Stream C session 1 bonus scope: Path B numbers cleanup

Living governance docs eliminated maintenance-burden numbers per Path B principle (cached state, arbitrary thresholds drift over time when nobody updates them):

- **Tier A removals (13 fixes):** counts removed from README ("31 ADRs", "69 lessons", "Council #1-#29 archived", "19 gaps"), ENVIRONMENT (gotchas count, core-invariants count, extensions count, vault notes count, MOC folders, tag dimensions, PLAYBOOK section count), PLAYBOOK (test count examples, gotchas skill entry count). Replaced with source pointers.
- **Tier B replacements (3 fixes):** "20 files → DevVault" trigger → "when navigation overhead emerges"; "50 entries → split LESSONS" → "when LESSONS.md becomes hard to navigate by topic"; "~44 H2 headers" count dropped, kept structural description.
- **Tier D rationale additions (4 fixes):** legitimate empirical numbers preserved with explicit basis to prevent future strip-as-cleanup (>100 stars/v1.0 maturity heuristic, 60%/80% coverage targets, 3+ files cross-module risk threshold, 4+ criteria majority-of-6 evaluation gate).
- **Tier E decisions (3 fixes):** ~2h handoff trigger kept as Cat. 4 with cross-ref to PLAYBOOK 3h decision-fatigue threshold; "1 page" UX constraint kept; "24 Council Decisions" example annotated as intentionally stale anti-pattern illustration.

Driven by `docs/audits/2026-04-27-numbers-audit.md` 5-tier classification. 7 commits, 5 living docs modified (README, PLAYBOOK, ESSENTIALS, ENVIRONMENT, SESSION_SETUP).

---

## 2026-04-26 — Stream C session 1 bonus scope: ESSENTIALS refactor + UI preferences

- ESSENTIALS.md 4-commit refactor: structural cleanup (C1, -6 lines),
  skills reference added to Writing a Prompt (C2, +2), Feedback Loop
  restructured with Auto/Manual labels and stale "Playbook S16" →
  "PLAYBOOK Section 16" (C3, +1 net), new section "How Claude thinks"
  inserted before Roles encoding 4 Does + 4 Does NOT thinking-quality
  directives (C4, +19). Net +16 lines, 12 H2 sections (restructured).
- UI user preferences rewrite: added Continuous context self-evaluation
  directive (trigger-based proactive monitoring), Defer requires explicit
  justification, refined Engineering mandate (delete vs condense
  distinction, multi-commit one-file clause), refined Claude Code prompts
  (CHANGELOG conditional on change type), removed Project Scale Tiers
  (now lives in ESSENTIALS post-C1). UI changes apply to NEW chats only.

---

## 2026-04-26 — Stream C session 1: ADR-30 default branch = `main`

- Added ADR-30 prescribing `main` as default branch for all Rob's repos (universal rule)
- Added PLAYBOOK section "Repo conventions" with 5-subsection skeleton: Default branch FILLED (this session, ADR-30); File naming, Folder structure, Secrets path, Capitalization marked TBD with forward-references to ADR-31 through ADR-34
- Renamed `.dev-knowledge` default branch from `master` to `main` (per-repo execution for corp-monorepo, ai-council pending — Stream C execution sprint 1)
- Updated `HANDOFF_PROCESS.md` and `templates/prompt-template.md` to reference `main` instead of `master`

---

## 2026-04-26 — HANDOFF_PROCESS.md v1.1 amendment

**Changed:**
- `HANDOFF_PROCESS.md` amended from v1.0 to v1.1
- Documents handoff as 3 distinct artifacts (persistent doc + Claude Code commit prompt + first-message template), not 1
- Adds workflow for both handoff generation and next-chat opening
- Adds walk-out test (next browser Claude's first response = substantive, no clarification needed)

**Why:**
- v1.0 conflated 3 artifacts into single .md file
- Discovered failure 2026-04-26: first attempted Stream B → Stream C handoff produced single file with upload checklist + first message + retrospective conflated
- Self-referential paradox: upload list inside the file being uploaded
- Reverted single-file commit, redesigning per amendment

**Per Gap #19 protocol:** amendment, not reopen — intent (cross-session context transfer) preserved; prescription (artifact count and structure) corrected.

**Lesson candidate:**
- Process discovered organically during execution often reveals gaps invisible during specification. v1.0 was specified without going through full handoff cycle; v1.1 codifies what actually works.

**Reference:**
- Gap #11 (Handoff process) — original implementation
- Gap #19 (Amendment vs Reopen Decision Protocol) — protocol applied
- Reverted commit history: docs(handoff) Stream B→C v1 attempt, reset to 1c9ff9a

---

## 2026-04-25 (continued) — Gap #9 Claude Code features inventory audit (Stream B FINAL)

**Added:**
- `docs/audits/2026-04-25-claude-code-features-inventory.md` — one-time audit, point-in-time snapshot (Claude Code v2.1.119)
- Tabular inventory: Core mechanisms, Model selection, Context & memory, External integrations, Project-level features, Observability, Cloud & scheduling
- Adoption status confirmed from filesystem (`~/.claude/` settings, commands, agents, skills) + web search (code.claude.com, Apr 2026)
- Blind spots section: 5 features with value rationale and evaluation triggers (Ultrareview, Routines, Monitor tool, project hooks audit, xhigh effort)
- Recommendations for 2026-Q3 triage with specific pilots
- Cross-link added to `docs/tech-radar/2026-Q2.md` Notes for Q3 section

**Why:**
- Without audit, "blind spots" persist — features that would help, never discovered
- Twitter/blog discovery scattered; audit grounds future Continuous Improvement triage
- Final remaining Stream B gap (19/19)

**Stream B status: COMPLETE.**

19 of 19 gaps from `docs/audits/2026-04-24-stream-b-gaps-mapping.md` implemented:
- Gaps #1–#6: Foundational (roles, prompt template, CLAUDE.md/AGENTS.md templates, doc taxonomy)
- Gaps #7a-d, #10: Claude Code internals + adoption protocol
- Gap #7d amendment 2026-04-25: subagents corrected to active status
- Gaps #11, #18: Handoff process + session continuity
- Gaps #12, #19: Council gating + amendment-vs-reopen protocol
- Gap #13: Session boundaries
- Gap #14: Token management (ccusage adoption + threshold cadence)
- Gaps #15, #16: Pytest per Scale + Codex archival
- Gap #17: Continuous Improvement Process + tech-radar bootstrap
- Gap #8: VS Code workspace templates per Scale
- Gap #9: This audit

**Per-repo action items** (separate Stream B work, NOT Stream B-internal):
- corp-monorepo CLAUDE.md trim per Gap #5 template
- corp-monorepo AGENTS.md expand per Gap #6 template
- .dev-knowledge create AGENTS.md
- ai-council create AGENTS.md
- ADR-27 collision fix corp-monorepo
- Read corp-monorepo `settings.local.json` — document project-level hook state (surfaced by Gap #9 audit)

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #9 specification + full Stream B mapping

---

## 2026-04-25 (continued) — Gap #8 VS Code workspace templates per Scale

**Added:**
- `templates/workspace-S.code-workspace` — Scale S minimal (Python + Ruff)
- `templates/workspace-M.code-workspace` — Scale M (+ pytest + GitLens + Error Lens + TODO Tree)
- `templates/workspace-L.code-workspace` — Scale L (+ mypy + Mermaid + spell check + TOML)
- PLAYBOOK Project Scale Tiers section: new "VS Code workspace per Scale tier" subsection (v1.0)

**Why:**
- Each repo improvised `.code-workspace` config; no baseline per Scale
- Bootstrap workflow now copy-paste from template, rename, customize
- Grounded in `corp-monorepo.code-workspace` (Scale L active example)

**Companion to prior Stream B gaps:**
- Gap #15 (Testing rules per tier): workspace test discovery aligns with pytest cadence
- Gap #5 (CLAUDE.md template): workspace settings reference align with Section 7 (Hooks active)
- Gap #6 (AGENTS.md template): repo Scale tier (Section 2) determines workspace template choice

**Per-repo action items (separate work):**
- Verify ai-council `.code-workspace` aligns with Scale M template
- Bootstrap any new project from appropriate template

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #8 specification
- `corp-monorepo.code-workspace` — Scale L exemplar source

---

## 2026-04-25 (continued) — Gap #10 Adoption protocol for Claude Code extensions

**Added:**
- PLAYBOOK "Claude Code internals" section: new subsection "Adoption protocol — when Claude Code proposes a new skill/command/hook/subagent" (v1.0)
- 5-stage pipeline (Triage → Decision → Validation → Install → Document)
- Decision rules: user-level vs project-level scope
- Install paths matrix per mechanism
- Documentation linkage (AGENTS.md Section 5, CLAUDE.md, JOURNAL, CHANGELOG, tech-radar)
- Anti-patterns

**Why:**
- Gap #7a-d (just merged) documents WHAT skills/commands/hooks/subagents are
- Without adoption protocol, Claude proposals adopted ad-hoc — ecosystem bloats, AGENTS.md Section 5 stale, validation skipped
- Companion to Gap #17 Continuous Improvement: that covers external tools (Codex, Tach, ccusage); this covers Claude Code's own extension mechanisms

**Companion to prior Stream B gaps:**
- Gap #7a-d (Claude Code internals): defines mechanisms; this defines adoption protocol for them
- Gap #6 (AGENTS.md template): Section 5 "Tools active" gets populated from adoptions
- Gap #5 (CLAUDE.md template): Sections 5/6/7 reference adoptions per Gap #10 documentation step
- Gap #17 (Continuous Improvement): broader pipeline pattern (Stages 4-5 are this protocol's "Decision/Install")

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #10 specification
- 2026-04-24 `/handoff` → `/session-summary` rename — trigger-word collision example in Validation stage

---

## 2026-04-25 — Gap #7d amendment (subagents)

**Changed:**
- PLAYBOOK Section "Claude Code internals" subsection 7d (Subagents) — amended from DEFERRED to active status; documents two real subagents (`ecosystem-snapshot`, `report-generator`)
- Amendment block added at top of 7d per Gap #19 amendment-vs-reopen pattern
- tech-radar 2026-Q2.md — subagents moved from any deferred entry to Adopted (active inventory)

**Why:**
- Verification 2026-04-25 found two active user-level subagents at `~/.claude/agents/` that v1.0 section incorrectly called deferred
- Amendment, not reopen — intent (disambiguation of 4 mechanisms) preserved; prescription (active vs deferred status) corrected
- Documentation drift caught quickly; one-day-old v1.0 entry already had factual error

**Lesson candidate:**
- Section 1 verification steps must include filesystem checks for "absence" claims (e.g. confirm `.claude/agents/` is empty before saying "no subagents"). Spec for Gap #7a-d directed "no subagents in Rob's ecosystem" without verification step — drift propagated.

**Reference:**
- Gap #19 (Amendment vs Reopen Decision Protocol) — pattern applied
- ADR-27 amendments precedent — same protocol used 3× during Stream A

---

## 2026-04-24 (continued) — Gap #7a-d Claude Code internals

**Added:**
- PLAYBOOK new section "Claude Code internals" (v1.0) — disambiguation table + 4 subsections covering skills (7a), slash commands (7b), hooks (7c), subagents deferred (7d)
- Real examples from Rob's ecosystem cited per subsection
- Cross-reference to AGENTS.md template Section 5 ("Tools active in this repo")

**Why:**
- Skills, slash commands, hooks, subagents have confusingly similar names — Rob and Claude conflated them multiple times in 2026-04-24 sessions
- Each new repo and session re-discovered distinctions via failure
- Subagents documented despite deferred adoption — future reference saves rediscovery cost when reopen trigger hits

**Subagents status:** deferred per tech-radar 2026-Q2 (solo developer scale, AI Council covers multi-perspective need, no identified pain point)

**Companion to prior Stream B gaps:**
- Gap #6 (AGENTS.md template): Section 5 "Tools active" gets populated from Claude Code internals adoptions
- Gap #5 (CLAUDE.md template): Section 5 (slash commands), Section 6 (skills), Section 7 (hooks) reference these definitions
- Gap #16 (Codex archival): hooks subsection establishes "LLMs advise; hooks enforce" pattern Codex review embodies
- Gap #17 (Continuous Improvement): adoption pipeline (Stages 4-5) applies to new skills/commands/hooks adoption

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #7a-d specification
- `docs/research/2026-04-24-multi-agent-debate-patterns.md` — subagents Council research
- Cognition "Don't Build Multi-Agents" (June 2025) — subagents anti-pattern source
- ADR-27 amendments — validator/hook divergence lesson informs hooks subsection anti-patterns

---

## 2026-04-25 (continued) — Gap #17 Continuous Improvement Process

**Added:**
- PLAYBOOK Section 6 "Continuous Improvement" (v1.0) — 6-stage pipeline (Discovery → Triage → Evaluation → Decision → Implementation → Review), source list, evaluation modes by stake
- `docs/tech-radar/` folder — quarterly snapshots of adopted/rejected/deferred/discovered tools
- `docs/tech-radar/README.md` — folder index, distinct-from-research clarification
- `docs/tech-radar/2026-Q2.md` — bootstrap entry retrospectively capturing 2026-Q1/Q2 adoption activity (ccusage, Perplexity, Codex, Tach, Opus 4.7, scope tagging adopted; MCP memory, GLM/Qwen, multi-agent frameworks, Spec Kit deferred; Kiro rejected)
- `scripts/validate_scope_tags.py`: `docs/tech-radar/` added to SKIP_PATTERNS (snapshot content, like docs/research)

**Why:**
- Adoption was organic — Twitter signal → ask browser → decide → execute. No record of why MCP memory was rejected vs deferred. Risk of re-evaluation thrash.
- 14 Stream B gaps closed today demonstrated the pipeline implicitly: each gap adoption went through stages 1-5. Codifying makes the pattern reusable for future tools.
- Quarterly review cadence prevents stale "adopted" tools from accumulating without value check.

**Companion to prior Stream B gaps:**
- Gap #5 (CLAUDE.md template), Gap #6 (AGENTS.md template): "Tools active in this repo" sections feed from tech-radar adoptions
- Gap #16 (Codex archival): Codex review findings can trigger Continuous Improvement Stage 1 (Discovery) when reviewer suggests new pattern/tool
- Gap #4 + #18 (Doc files taxonomy): tech-radar/ folder is universal (.dev-knowledge only), not per-repo

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #17 specification
- 2026-Q1/Q2 adoption activity captured in `docs/tech-radar/2026-Q2.md`

---

## 2026-04-25 (continued) — Gap #15 + #16 testing rules + Codex archival

**Added:**
- PLAYBOOK Project Scale Tiers section: new "Testing rules per tier" subsection (v1.0)
- PLAYBOOK Section 5: new "Codex review archival protocol" subsection (v1.0)

**Gap #15 (Testing rules):**
- S/M/L matrix: minimum requirement, coverage target, test types, run command
- Per-step test cadence (Scale M+) — `pytest -x --tb=short` + ruff + git status after each numbered step
- Anti-patterns: coverage chasing at S, skipping tests at L, integration-only at L

**Gap #16 (Codex archival):**
- Trigger criteria (Critical/High findings, non-trivial merges, future work pointers)
- Target path: `{repo}/docs/audits/YYYY-MM-DD-codex-{slug}.md`
- Standard format with severity breakdown table and per-finding structure
- Cross-linking protocol (JOURNAL, commits, CHANGELOG)
- Anti-patterns including "archive everything" and "Codex output rot"

**Why:**
- Gap #15: Project Scale Tiers defined sizes but not testing requirements per tier
- Gap #16: Codex review findings were session-ephemeral; analogous to Council debates which got archival protocol earlier today (5.N)

**Companion to prior Stream B gaps:**
- Gap #12 + #19 (Council gating + Amendment): Section 5 now covers Council debates, archival, gating, amendment, AND Codex archival — complete decision-making/review lifecycle
- Gap #2 (Prompt template): per-step test cadence references prompt-template.md
- Gap #4 + #18 (Doc files + Scale matrix): testing rules align with Scale-tiered file requirements

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gaps #15 and #16 specifications
- corp-monorepo AGENTS.md — Codex review pattern (severity tiers, modes) source

---

## 2026-04-25 (continued) — Gap #13 Session boundaries

**Added:**
- PLAYBOOK.md "Session boundaries" section (v1.0)
- 5 subsections: scope declaration, stop-signs, decision fatigue threshold, recursive planning anti-pattern, session resumption protocol
- Numeric guidelines (>3h + >3 decisions = wrap zone) + qualitative signals
- In-vivo example from 2026-04-24 session as concrete reference

**Why:**
- Session-management was tribal knowledge — each new browser chat re-discovered patterns via failure
- 2026-04-24 sessions ran 8+ hours with multiple recursive-planning episodes; pattern broke only when Rob pushed back explicitly
- Stop-signs without explicit codification get rationalized away in the moment
- Session resumption protocol prevents bare "continue what we were doing" anti-pattern

**Companion to prior Stream B gaps:**
- Gap #1 (Roles): browser=architect — applies to session-mgmt decisions
- Gap #11 (Handoff process): handoff is the action when stop-sign triggers
- Gap #18 (Doc files + Scale matrix): handoff and JOURNAL referenced in resumption protocol
- Gap #12 (Council gating): decision fatigue applies to architectural decisions specifically

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #13 specification
- 2026-04-24 sessions — in-vivo example source

---

## 2026-04-25 (continued) — Gap #12 + #19 Council gating and amendment protocol

**Added:**
- PLAYBOOK Section 5 subsection "When to run Council vs single-model + critic" (v1.0) — gates Council to ADR-worthy decisions per Council #28 finding; provides single-model + critic alternative for ~70% of decisions
- PLAYBOOK Section 5 subsection "Amendment vs Reopen Decision Protocol" (v1.0) — codifies pattern used 3× organically on 2026-04-24
- Decision trees, mechanics, anti-patterns, examples in both subsections

**Why:**
- Gap #12: Council #28 community research flagged AI Council overhead risk — running 4-model debate on every decision wastes ~$0.50 + 5min when ~70% don't need it
- Gap #19: Amendment pattern emerged 3 times in a single day during Stream A closure (ADR-27 delta rule, ADR-29 H1 placement, ADR-27 heading levels). Without codification, future Claude/Rob would re-discover from scratch or default to expensive reopens.

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gaps #12 and #19 specifications
- `docs/research/2026-04-23-council-28-community-patterns.md` — community finding on Council overhead
- ADR-27 amendments (2× on 2026-04-24 and 2026-04-25) — amendment pattern instances
- ADR-29 amendment (2026-04-24) — amendment pattern instance

---

## 2026-04-25 (continued) — Gap #11 Handoff process Vibe Code 4 protocol patch

**Changed:**
- `HANDOFF_PROCESS.md` updated to v1.0:
  - Translated to English (was entirely Polish)
  - Explicit trigger rule (Rob explicit, never proactive)
  - Scale-tiered format (S minimal / M reduced / L full)
  - Downloadable `.md` artifact requirement
  - Roles section cross-reference (ESSENTIALS Gap #1)
  - Related references list
  - Section history
- `handoff-prompts/` templates updated minimally:
  - `README.md`: added cross-reference to HANDOFF_PROCESS.md as authoritative protocol source; translated to English; noted Polish in templates is intentional (Vibe Code 4 trigger phrase)
  - `typ-a-step1-browser-prompt.md`: added Scale (S/M/L) line
  - `typ-b-step1-browser-prompt.md`: added Scale (S/M/L) line

**Why:**
- Vibe Code 4 (2026-04-22) established binding handoff protocol but only in handoff itself
- Each new browser chat re-discovered "Rob triggers, not Claude" by trial and error
- Handoffs are the artifact connecting consecutive browser chats — protocol consistency is high-leverage

**Companion to prior Stream B gaps:**
- Gap #1 (Roles in ESSENTIALS): browser=architect, Claude Code=executor
- Gap #2/#3 (Prompt format + checklist): downloadable `.md` artifact pattern
- Gap #4/#18 (Doc files + Scale matrix): handoff is one of 12 file types, Scale-tiered

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #11 specification
- `docs/handoffs/2026-04-22-vibe-code-4-stream-a.md` — original protocol establishment

---

## 2026-04-25 (continued) — Gap #4 + #18 doc files taxonomy + Scale matrix

**Added:**
- PLAYBOOK.md "Documentation file types and session continuity" section (v1.0)
- Table 1: 12-file taxonomy (purpose, format, cadence, audience, order, scope)
- Table 2: Scale tier presence matrix (S/M/L × file requirements)
- Subsections: common confusions resolved, order conventions, section history

**Why:**
- 12 documentation file types existed without canonical "what goes where" reference
- JOURNAL vs handoff confusion documented (within-repo tactical vs across-context summary)
- LESSONS vs ADR boundary clarified (process lesson vs technical commitment)
- TOKEN-LOG/LESSONS/ESSENTIALS/PLAYBOOK as universal `.dev-knowledge` files vs per-repo files now explicit
- Scale matrix prevents over-documenting Scale S projects with full Scale L apparatus

**Companion to prior Stream B gaps:**
- Gap #6 (AGENTS.md template), Gap #5 (CLAUDE.md template) — file types now have authoritative cross-reference
- Gap #14 (Token log cadence), order conventions — both linked from this section
- Future Stream B work referencing file types points to this section

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gaps #4 and #18 specifications
- `docs/research/2026-04-23-council-28-community-patterns.md` — JOURNAL/handoff faction analysis

---

## 2026-04-25 (continued) — Gap #2 + #3 prompt format template + checklist

**Added:**
- `templates/prompt-template.md` v1.0 — 8-section skeleton with per-Scale guidance
- PLAYBOOK.md "Writing prompts for Claude Code" section with Gap #2 rules + Gap #3 checklist subsection
- Per-Scale variants documented (S minimal, M reduced UNDERSTAND, L full + plan mode)

**Why:**
- Vibe Code 4 (2026-04-22) established standard structure during Stream A but only in historical prompts
- Each new browser chat reinvented prompt structure, often with errors (Polish, inline blocks, missing UNDERSTAND)
- Pre-send checklist makes anti-patterns visible before delivery to Claude Code

**Companion to Gaps #1, #5, #6:**
- Gap #1 (Roles in ESSENTIALS): browser=architect, Claude Code=executor
- Gap #6 (AGENTS.md template): cross-tool governance per repo
- Gap #5 (CLAUDE.md template): Claude Code session contract per repo
- Gap #2/#3 (this): the artifact format that flows from architect to executor

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gaps #2 and #3 specifications
- `handoff-prompts/` examples — pattern source from Vibe Code 4
- ADR-28 — three-layer architecture (browser/.dev-knowledge/projects)

---

## 2026-04-25 — Gap #5 CLAUDE.md template + PLAYBOOK section

**Added:**
- `templates/CLAUDE-md-template.md` v1.0 — thin pointer skeleton, 10 sections, ≤200 lines target
- PLAYBOOK.md "CLAUDE.md as session contract" section (with H3 subsections per ADR-27)
- Versioned per ADR-29 amendment pattern

**Why:**
- Per Council #28 community standard: CLAUDE.md ≤200 lines, thin pointer to AGENTS.md and universal rules
- corp-monorepo CLAUDE.md (4KB, stale numbers) is exactly the failure mode template prevents
- Companion to AGENTS.md template (Gap #6) — together they form per-repo governance pattern

**Per-repo action items (separate Stream B work):**
- Trim corp-monorepo CLAUDE.md from 4KB to ≤200 lines using template (P0-1 from consolidated-actions)
- Verify .dev-knowledge CLAUDE.md alignment with template
- Verify ai-council CLAUDE.md alignment with template

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #5 specification
- `docs/research/2026-04-24-claude-md-best-practices.md` — research informing structure
- `templates/AGENTS-md-template.md` — companion template (Gap #6)

---

## 2026-04-25 — Validator/hook H3 divergence resolved

**Fixed:**
- `scripts/validate_scope_tags.py`: no-args invocation now scans all in-scope files on disk instead of vacuously passing on an empty list
- `docs/decisions/ADR-27_scope-tagging.md`: Amendment 2026-04-25 added — heading levels (H2 + H3) and validator standalone invocation semantics now explicitly specified
- Validator and pre-commit hook now produce identical results on identical content regardless of invocation mode

**Root cause:**
- `main(sys.argv[1:])` with no arguments → empty `paths` → zero files validated → `"all files pass"` (vacuous)
- Pre-commit hook passes staged filenames via `pass_filenames: true` → files actually validated → caught missing H3 scope tags
- Both tools agreed on the rule (H2_RE covers `##` and `###`); invocation semantics were the gap

**Why:**
- Discovered during Gap #1 (Roles section in ESSENTIALS): manual validator run passed, hook failed on H3 tags
- Governance tools sharing enforcement rules cannot diverge by invocation mode — creates silent false-negatives
- Resolved via Direction C: clarify invocation semantics; no rule change needed

**Lesson recorded:** see LESSONS.md 2026-04-25 entry

---

## 2026-04-24 (continued) — Gap #1 Roles section in ESSENTIALS

**Added:**
- ESSENTIALS.md: new "Roles" section (v1.0)
- Documents browser chat (architect) vs Claude Code (executor) division
- References ADR-28 three-layer flow
- Versioned for amendment tracking

**Why:**
- Vibe Code 4 (2026-04-22) established binding protocol but lived only in handoff
- Each new chat re-discovered rule via Rob's reminders
- ESSENTIALS is uploaded to every browser session — protocol now universal context

**Versioning approach:**
- v1.0 documents observed practice (not aspiration)
- Future amendments tracked in section's "Section history" subsection
- Per ADR-29 amendment pattern: minor drift → amend in place; intent change → new ADR
- Will refine after live use of v1.0 in next sessions

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #1 specification
- Vibe Code 4 handoff (2026-04-22) — original protocol establishment
- ADR-28 — three-layer architecture

---

## 2026-04-24 (continued) — AGENTS templates reconciled

**Changed:**
- `templates/AGENTS.md.template.md` → `templates/codex-review-config-template.md` (rename — file was misnamed; true purpose is Codex review configuration, embeddable in AGENTS.md Section 5)
- Internal title updated to reflect Codex-specific role
- New AGENTS template Section 5 cross-links to Codex config template

**Why:**
- Two files named like AGENTS template caused confusion
- Old file is NOT full governance — it's Codex review subset
- Cross-link makes relationship explicit: governance template (parent) embeds Codex config (subset) per Scale

**Per-repo follow-up (NOT this commit):**
- corp-monorepo AGENTS.md likely originated from old template (Codex-only) — needs expansion to full governance using new template, with Codex content per Codex template embedded in Section 5. Separate Stream B work.

---

## 2026-04-24 (continued) — Gap #6 AGENTS.md template + PLAYBOOK section

**Added:**
- `templates/AGENTS-md-template.md` — hybrid governance contract skeleton, 10 sections
- PLAYBOOK.md "AGENTS.md — canonical per-repo governance contract" section
- Template documents: pointer to .dev-knowledge for universal rules, per-repo specifics only, cross-tool standard per Council #28

**Why:**
- Each repo needs canonical governance file (AGENTS.md) — community standard 2025-2026
- Hybrid pattern (point to PLAYBOOK, don't duplicate) avoids drift when universal rules change
- Template enables consistent AGENTS.md across corp-monorepo, ai-council, .dev-knowledge, future projects

**Per-repo action items (separate Stream B work, NOT this commit):**
- Create AGENTS.md in .dev-knowledge using template
- Expand corp-monorepo AGENTS.md (currently Codex-specific) using template
- Create AGENTS.md in ai-council using template

**Reference:**
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #6 specification
- Council #28 community findings (`docs/research/2026-04-23-council-28-community-patterns.md`)
- `docs/research/2026-04-24-claude-md-best-practices.md` — informs per-repo CLAUDE.md design (next gap, #5)

---

## 2026-04-24 (continued) — TOKEN-LOG order flipped to newest-first

**Changed:**
- TOKEN-LOG.md: reordered entries newest-first (matches CHANGELOG convention)
- `~/.claude/commands/session-summary.md`: staleness check step clarified — "first match = most recent entry" (logic already correct, note added)
- PLAYBOOK.md "Token log cadence": order convention documented (logs = newest-first, LESSONS = append-only)

**Why:**
- TOKEN-LOG was oldest-first; PLAYBOOK spec said "append to top" — contradiction would break /session-summary on next edit
- Two distinct categories codified: logs (scan for current state → newest-first) vs append-only narrative (LESSONS → chronological, preserve order)
- LESSONS.md not modified — append-only is ADR-29 core design, 61 entries, narrative-oriented

**Scope:**
- User-level /session-summary command clarified (no logic change)
- LESSONS.md intentionally preserved as-is

---

## 2026-04-24 (continued) — TOKEN-LOG cadence formalized

**Added:**
- PLAYBOOK.md: "Token log cadence" section with threshold-based (7-day) trigger spec
- `~/.claude/commands/session-summary.md`: conditional ccusage --json snapshot step (absolute paths)
- ENVIRONMENT.md: cross-reference to PLAYBOOK cadence section

**Why:**
- TOKEN-LOG had 2 entries and no ritual (would go stale again)
- Per-session cadence rejected — ~$0.02/run overhead for data that changes weekly
- Manual weekly ritual rejected — forgetting risk (4 weeks stale before ccusage adoption)
- Threshold-based: amortized ~$0.006/run, auto-triggers on staleness, zero forgetting risk

**Scope:**
- /session-summary is user-level (`~/.claude/commands/`) — applies to any session with .dev-knowledge accessible
- TOKEN-LOG global tracker in .dev-knowledge (not per-repo)
- New entries staged but NOT auto-committed — Rob reviews before committing

---

## 2026-04-24 — Repo hygiene pass

**Changed:**
- LESSONS.md: 50-entry split trigger deferred — ADR-29 scope tags provide equivalent filtering
- `docs/audits/2026-04-21-dev-knowledge-inventory.md`: marked SUPERSEDED (newer inventory 2026-04-24)
- `ADR-27_council-27-scope-tagging.md` → `ADR-27_scope-tagging.md` (naming consistency with ADR-28/29)
- `handoff/` → `handoff-prompts/` (disambiguate from `docs/handoffs/`)
- `README.md` full rewrite — user-first, 87 lines, current state after Stream A

**Fixed:**
- `scripts/validate_scope_tags.py`: bug in `_enforce_ratio` where staged file with same basename as in-scope file (in skipped directory) corrupted hybrid ratio delta calculation
- `handoff-prompts/` added to SKIP_PATTERNS (prompt templates, not governance)

**Dropped:**
- 3 README sections: "lesson→rule" (already in PLAYBOOK), "data sanitization" (moved to ESSENTIALS.md), growth trigger #3 (resolved by ADR-28)

**Not done (deferred):**
- TOKEN-LOG.md snapshot — Anthropic /stats UX is multi-page interactive TUI, no native export. Adopting `claude-usage` npm tool as permanent solution (separate session).

**Metrics:**
- Hybrid ratio: 26% → 25% (exactly at ceiling)
- Commits: 6 (+ merge)
- Branch: `chore/repo-hygiene-2026-04-24` → master ff-only

---

## 2026-04-24 — ccusage tool adopted
- Global npm install: `ccusage` v18.0.11 for Claude Code usage tracking
- ENVIRONMENT.md entry documenting tool + cadence (under Claude Code CLI section)
- TOKEN-LOG.md: first post-adoption snapshot (delta 2026-03-29 to 2026-04-24, $190.53, 31 sessions)
- PLAYBOOK.md: /stats table row + weekly cadence step updated to reference ccusage
- Rationale: /stats is interactive TUI, no scriptable export; ccusage reads local Claude Code data, outputs JSON

## 2026-04-24 — repo hygiene
- docs(lessons): defer 50-entry split, rationale inline
- docs(audits): mark 2026-04-21 dev-knowledge inventory as superseded
- refactor(decisions): ADR-27 filename simplified (drop _council-27 segment)
- refactor: rename handoff/ → handoff-prompts/ (disambiguate from docs/handoffs/)
- docs(readme): user-first rewrite, 87 lines, current state after Stream A
- fix(validator): basename collision bug in ratio enforcer (out-of-scope staged files could corrupt HEAD delta); add handoff-prompts/ to SKIP_PATTERNS

## 2026-04-24
- feat(validator): ratio-aware hybrid enforcement (block regressions only, not stuck-above state); ruff E741 fixed
- docs: ADR-27 amendment for commit-time enforcement prescription; Stream A CLOSED; 3 lessons extracted in new ADR-29 format
- Stream A prompt 6 complete; hybrid ratio 26% at closure; carried-forward: none
- chore(lessons): add file-level scope tag per ADR-29, preserve append-only (58 entries untouched); placed under H1 per validator reality
- docs: document [scope: X] inline field in ESSENTIALS Ending-a-Session and PLAYBOOK Section 4
- docs(adr-29): amend insertion point to H1; Stream A prompt 5 complete, hybrid ratio 0%
- chore(dev-knowledge): tag ESSENTIALS/SESSION_SETUP/HANDOFF_PROCESS/ENVIRONMENT (55 sections)
- chore(validator): allowlist already covered all 4 files — no edits needed; hook now enforces repo-wide
- Stream A prompt 4 complete, hybrid ratio 16% (4 new files), 25% repo-wide; REVIEW-flagged subsections: none
- structural fix: added description lines after H1 in ESSENTIALS.md + SESSION_SETUP.md to prevent validator H1-window false-positive on first section tag
- fix(playbook): correct 5 top-level tag mismatches vs Phase 2 audit (S4 S6 S7 S14 S15)
- chore: cascade subsection inherit-parent fixes, hybrid ratio X% → 0%
- Stream A prompt 3.6, sanity check verdict now PASS
- docs: add PLAYBOOK tagging sanity check report
- verifies top-level tags match Phase 2 audit and subsections inherit parent
- Stream A prompt 3.5, report at docs/audits/2026-04-24-playbook-tagging-sanity-check.md

---

## 2026-04-21
- PLAYBOOK: added "System Architecture" section documenting three-layer architecture (ADR-28)
- PLAYBOOK: added cross-ref in Section 12 to System Architecture
- Automated Codex review: `~/.claude/bin/codex-review.ps1` wraps `codex exec --output-last-message`
- `/review` slash command updated to invoke `codex-review`; PLAYBOOK S15 + ESSENTIALS step 3 updated
- Replaces manual "copy from TUI → paste to file" workflow
- Flag `-AutoCommit` for opt-in commit; file-based commit message avoids OneDrive hook

---

## 2026-03-29 — Initial Release

### Added
- ESSENTIALS.md — daily cheat sheet (shortcuts, tokens, 5 rules)
- SESSION_SETUP.md — 5-step browser chat workflow (functional vs programming)
- PLAYBOOK.md — 14 sections + 3 appendices (shortcuts, routing, optimization)
- LESSONS.md — 45 entries from corp-monorepo retrospective, dev-practice sessions, Council debates
- ENVIRONMENT.md — tools, config, paths, VS Code setup, binding decisions
- TOKEN-LOG.md — baseline snapshot from 2026-03-28
- README.md — triage rules, file index, growth triggers
- CLAUDE.md — project contract for Claude Code
- JOURNAL.md — session log
- This CHANGELOG

### Removed (consolidated)
- SHORTCUTS.md → absorbed into PLAYBOOK Appendix A
- WORKFLOW.md → absorbed into PLAYBOOK + ESSENTIALS
- OPTIMIZATION.md → absorbed into PLAYBOOK Appendix C
- TOOLS.md → absorbed into ENVIRONMENT
- VSCODE_SETUP_REFERENCE.md → absorbed into ENVIRONMENT
- DECISIONS.md → absorbed into ENVIRONMENT

### Infrastructure (deployed to ~/.claude/)
- memory/ directory (README, learned-rules, evolution-log)
- rules/core-invariants.md (5 compression-proof rules)
- commands/boot.md and evolve.md
- SessionStart + Stop hooks in settings.json
- 41 gotchas upgraded with verify: lines

### Council Decisions
- #23: vault = pre-sales, .dev-knowledge = dev methodology, ~/.claude/ = runtime config
- #24: browser handoff = one format, "wygeneruj handoff", <100 lines, checkpoint at ~2h

## 2026-04-21 (continued)
- Added ADR-27: Council #27 scope tagging architecture (Option A, binding)
- Added ADR-29: LESSONS.md grandfathering under scope tagging

## 2026-04-22
- Added CLAUDE.md Scope tags section (vocabulary, consumer read sets, governance) per ADR-27
- Added scripts/validate_scope_tags.py (stdlib-only pre-commit validator)
- Added .pre-commit-config.yaml and requirements-dev.txt (pre-commit >= 3.5.0)
- Tagged CLAUDE.md (11 sections) and README.md (5 sections) as meta

## 2026-04-23 — Tech Radar Session + Architecture Analysis

Added:
- Operating model analysis for corp-monorepo (Scale L): `docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md` (572 lines, extended 2026-04-23 with AI Council integration, ADR-27 collision, naming conventions, VS Code workspace sections)
- Council #28 research debate executed: community LLM dev patterns ($0.56)
- Council #29 research debate executed: Spec Kit / Kiro evaluation ($0.21)
- 3 standalone research reports from Perplexity-backed debates archived to `docs/research/`

## 2026-04-24 — Research Archive Structure

Added:
- `docs/research/` folder for AI Council research mode outputs (distinct from `docs/decisions/` which is for Rob's own decisions)
- 3 research reports archived from 2026-04-23 and 2026-04-24 sessions
- Council #28 and #29 transcripts cross-archived in `corp-monorepo/docs/decisions/transcripts/`

Convention:
- Research reports in `.dev-knowledge/docs/research/YYYY-MM-DD-slug.md`
- Council debate transcripts in `corp-monorepo/docs/decisions/transcripts/DECISION_NN_slug.md`
- Research ≠ decision: research informs, decision commits

## 2026-04-24 — Council Archival Protocol

Added:
- PLAYBOOK Section 5: "Council Debate Archival Protocol" — mandatory immediate archival after every debate
- Retroactive archive of 7 debates + research reports to `docs/research/` and `docs/decisions/transcripts/`
- `docs/research/README.md` and `docs/decisions/README.md` index files

Why:
- Knowledge was being lost in `ai-council/output/`
- No systemic protocol for post-debate archival existed
- 5-debate backlog discovered during Council #28/#29 review session

Scope note:
- corp-monorepo archival deferred (separate session)
- Debates affecting corp-monorepo architecture (#25 diagrams, #26 Tach) archived in `.dev-knowledge/docs/research/` with `-corp-monorepo` suffix
- Future mirror to `corp-monorepo/docs/decisions/transcripts/` is separate work

## 2026-04-24 — Supplements (repo sync session)

Added:
- `docs/audits/2026-04-24-council-28-29-consolidated-actions.md` — triage of P0/P1/P2/P3 action items from Council #28, #29 + 2 research reports
- `docs/audits/2026-04-24-stream-a-gap-report.md` — Stream A remaining work (Prompts 3.5, 4, 5, 6); supersedes P0-2 in consolidated actions
- PLAYBOOK: all 78 section headers tagged with scope vocabulary (ad-hoc, under pre-commit hook pressure on 2026-04-24 — not via planned Vibe Code 4 batch workflow)
- CLAUDE.md: updated PLAYBOOK section count (14 → 16 + System Architecture); added Council #27 to governing decisions list
- CHANGELOG: retroactive 2026-04-23 entry added (was missing)

Note:
- Scope tag validator ran clean; no actual `<!-- scope: X -->` placeholder tags found (ADR files reference the syntax in explanatory text only)
