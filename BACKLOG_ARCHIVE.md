### [P1] [done] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates
- **What:** Update process docs to reflect ADR-37 (two-phase) + ADR-41 (BACKLOG) integration; deprecate ADR-32 §4 in favor of BACKLOG reference. Includes SESSION_SETUP.md updates: BACKLOG review step at session start (per ADR-41 enforcement), audit tool trigger guidance (per ADR-36), JOURNAL update step at handoff generation (per ADR-39 enforcement requirement).
- **Why:** ADR-37 and ADR-41 ratified but templates still v2.0; need v3.0 reflecting overlay + backlog enforcement
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** done (2026-05-09 — closed by ADR-42 ratification + v3.0 implementation; HANDOFF_PROCESS rewritten, HANDOFF_QUESTION_TEMPLATE + HANDOFF_FOLDER_TEMPLATE created, SESSION_SETUP.md updated, ai-council handoff regenerated)

- **Archived:** 2026-05-16

### [P1] [done] v3.3.2 — HANDOFF_FOLDER_TEMPLATE parameterization for cross-repo handoffs
- **What:** Patch `templates/HANDOFF_FOLDER_TEMPLATE.md` to parameterize `{TARGET_REPO}` substitution in articulation gate item #1; refactor `02_VISION.md` generation to use target repo's `VISION.md` (with conditional `02b_ECOSYSTEM_VISION.md` carrying `.dev-knowledge` VISION when target ≠ `.dev-knowledge`); fix "BOUNDARIES" → "Hard Constraints" terminology drift in articulation gate item #4; update `00_README` + `01_MANIFEST` + `00_first-message` template surfaces accordingly; bump `protocols/HANDOFF_PROCESS.md` v3.3.1 → v3.3.2. **Mandatory manual cross-case trace verification step** (Stage 3 simulated against both `.dev-knowledge` and a non-`.dev-knowledge` target before merge) to prevent recurrence of the `universal-without-cross-case-verification` pattern.
- **Why:** Bug 1 (hardcoded .dev-knowledge in articulation gate item #1) + Bug 2 (unconditional .dev-knowledge VISION copy in 02_VISION.md) witnessed 2026-05-14 ai-council Stage 3. **Captured here, not fixed here** — fix is v3.3.2's scope per operator decision 2026-05-14 (Option B over Option A after architect pushback on four briefing-note errors: missed Hard Constraint #3, stale directive #2 state, fabricated "ADR-29 atomic convention", circular citation). v3.3.2 = next dedicated `.dev-knowledge` session's primary objective, not "P1 in BACKLOG for someday."
- **Stage 1 inputs available for next session:**
  - `docs/handoffs/2026-05-14-dev-knowledge-session-sync/06_STATE_OF_PLAY.md` (this session's state)
  - LESSON #9 (`universal-without-cross-case-verification`, appended this commit)
  - This BACKLOG entry (witnessed bug details, literal template content references, evidence trail)
- **Operator mitigation in interim:** do not generate cross-repo handoffs (ai-council, corp-monorepo, corp-ops, corp-sca-time-automation) until v3.3.2 ships. The 2026-05-14 ai-council bundle stays as historical empirical artifact (never delete without explicit ask).
- **Vision ref:** ADR-33 (vision universalization), ADR-42 (handoff format v3 authority)
- **Added:** 2026-05-14 by rob (interleaved scope, current session)
- **Status:** done (2026-05-15 — template fix merged, ai-council bundle regenerated; see CHANGELOG 2026-05-15 [Fixed])

- **Archived:** 2026-05-16

### [P1] [done] PLAYBOOK content additions for ADRs 36/37/40/41
- **What:** Add PLAYBOOK.md sections for ADR-36 (audit tool usage workflow), ADR-37 (two-phase handoff format guidance), ADR-40 (tier transition procedures S→M and M→L), ADR-41 (BACKLOG grooming workflow per-handoff and quarterly cadence). Update PLAYBOOK header version/date to reflect content amendments.
- **Why:** PLAYBOOK lifecycle (per ADR-39) update trigger is "ADR ratification adding/changing process." 4 ADRs ratified 2026-04-30 add/change process; PLAYBOOK currently mentions only ADR-33/34. Methodology debt.
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
- **Status:** done (2026-05-14 — new §10 BACKLOG Grooming, new §18 Ecosystem Audit Tool, §8 amended ADR-37 two-phase, Project Scale Tiers extended ADR-40 tier transitions; sections 10–17 renumbered 11–17+19)

- **Archived:** 2026-05-16

### [P1] [done] Audit tool P1 implementation
- **What:** Build .dev-knowledge audit tool per ADR-36 — P1 MVP (audit run + ecosystem state + markdown report). Implement compute_tier_score, classify_tier per ADR-40.
- **Why:** Required for Phase 2 universalization per repo; algorithmic tier classification (ADR-40) needs implementation to operationalize
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-04-30 by rob
- **Status:** done (2026-05-15 — `scripts/audit.py` CLI (4 commands per ADR-36), ecosystem state schema (state.yaml + history/), 3 checks (vision_md, adr38_baseline, claude_md), markdown report, 27 tests. Self-audit: .dev-knowledge FAIL (missing src/ + pyproject.toml — governance repo, see new BACKLOG item). Cross-repo audit: ai-council PASS with WARN (ARCHITECTURE.md optional but absent). Pre-flight gate: ADR-38 canonical list verified — inferred list in draft plan was wrong (LESSONS.md/JOURNAL.md not universal; src/tests/pyproject.toml missing from inferred list).)

- **Archived:** 2026-05-16

### [P1] [done] Cross-repo dated-entries format standard (Entry 1)
- **What:** Define a single cross-repo standard for dated-entries files (LESSONS.md, JOURNAL.md, CHANGELOG.md) covering date format, header levels, ordering convention (prepend vs append), entry schema (free-prose / structured / hybrid), per-repo flexibility vs universal mandate. Captures and supersedes the narrower P2 "ADR-29 amendment — prepend at top" item (rolled into this broader decision). Output: ADR (next available number) synthesized from Council research + pick.
- **Why:** Empirical drift signals: LESSONS.md schema correction `14f0467`, prepend-vs-append practical convention shift `99a104e`, ordering varying within same file, JOURNAL `##` vs `###` heading drift, CHANGELOG semver-style only in .dev-knowledge. Audit Tool P1 surfaced first cross-repo dated-entries gap on 2026-05-15: VISION.md frontmatter `status` key present in .dev-knowledge, missing in ai-council. Format drift extends beyond the three dated-entries files but those are the immediate scope.
- **Vision ref:** VISION.md "Knowledge Guardian" + "Methodology Author" functions; pairs with Cross-stream P1 "Sacred-files maintenance enforcement"
- **Added:** 2026-05-15 by rob (governance ADR session B+C)
- **Status:** done (2026-05-15 — ratified as ADR-46. Council research + pick winner B-1 (Lightweight Hybrid + sniff-test). Universal envelope (ISO `## YYYY-MM-DD`, reverse-chrono prepend) + file-specific payloads (LESSONS 6-field preserved, JOURNAL free-prose, CHANGELOG Keep-a-Changelog). ADR-27 HTML comments authoritative for scope; YAML optional additive only. Archive threshold 10k tokens, tooling deferred. Stdlib-regex validator required, AST library adoption gated behind future ADR amendment with empirical justification. Session D cleanup + Session E audit check are downstream.)

- **Archived:** 2026-05-16

### [P1] [done] Cross-repo BACKLOG organization standard (Entry 2)
- **What:** Define a single cross-repo standard for BACKLOG.md covering done-item handling (inline status flip / sectioned move / separate archive file), ordering / sorting strategy (priority / date / stream / hybrid), pruning rhythm (continuous / weekly / monthly / on-demand), priority semantics (P0/P1/P2 definitions or simpler), stream / category vocabulary (fixed cross-repo vs per-repo flexibility), per-repo flexibility vs universal mandate. Output: ADR (next available number) synthesized from Council research + pick.
- **Why:** BACKLOG is the primary cross-session handoff anchor. Without consistent organisation, file grows without pruning, done mixes with open reducing scannability, no consistent ordering — each repo drifted ad-hoc. ADR-41 mandates BACKLOG.md at M+ tier but does not specify organisation; this fills that gap.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-41 follow-on
- **Added:** 2026-05-15 by rob (governance ADR session B+C)
- **Status:** done (2026-05-15 — ratified as ADR-47. Council research + pick winner C-2 (Stream-grouped + Two-file state). BACKLOG.md holds [open]/[superseded]; new BACKLOG_ARCHIVE.md holds [done]/[abandoned]. Streams + P1/P2/P3 + required-fields schema preserved. Session-start validator fail-fast on [done] in BACKLOG.md. Deterministic <50 LOC extraction script — no LLM prompt. Kill criteria: 300 lines / 15 per stream / 33% Cross-stream. Scope tags / SCOPE_SCHEMA explicitly NOT adopted. Session D + Session E downstream.)

- **Archived:** 2026-05-16

### [P2] [done] Audit tool extension — ADR-46 + ADR-47 checks + extraction script (Session E)
- **What:** Implement two new audit checks (`check_dated_entries_format` per ADR-46, `check_backlog_organization` per ADR-47) and `scripts/backlog_extract.py` extraction script. Dogfood both checks against `.dev-knowledge` + `ai-council` real repos to produce Session D cleanup scope inventory.
- **Why:** ADR-46 + ADR-47 were ratified in the governance session; audit tool needed corresponding checks to enforce the new standards algorithmically. Dogfood run validates implementation against real-world content and surfaces concrete findings for Session D.
- **Vision ref:** VISION.md "Auditor" function; ADR-36 (audit tool architecture)
- **Added:** 2026-05-15 by rob (Session E scope, downstream of governance ADRs B+C)
- **Status:** done (2026-05-15 — 2 checks + extraction script shipped; 56 tests passing; dogfood: 51 checks across 2 repos — 6 pass, 42 fail, 3 warn. Session D scope routed to BACKLOG. See CHANGELOG 2026-05-15 [Audit Tool P2].)

- **Archived:** 2026-05-16

### [P1] [done] Phase 1 validation — audit + handoff dry-run on ai-council
- **What:** Manual audit ai-council (per ADR-36 architecture, computing tier per ADR-40 manually since audit tool not yet implemented). Generate handoff folder per ADR-37 two-phase format. Transfer handoff to new claude.ai chat for ai-council. Evaluate: did handoff preserve methodology, model/mode/effort context, ADR awareness, BACKLOG context, two-phase Current/Future state framing? Findings inform audit tool P1 implementation and HANDOFF_PROCESS template updates.
- **Why:** End-to-end validation of Phase 1 governance (8 ADRs ratified) before further implementation work. Without this, audit tool P1 implementation is blind to real-world gaps; HANDOFF_PROCESS template updates are theoretical. Real test of whether ratified architecture translates to working process. Gates other P1 items (audit tool implementation, template updates) — those should be informed by validation findings.
- **Vision ref:** VISION.md "Auditor" + "Disseminator" functions
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** done (2026-05-09 — Stage 3 folder generated at
  docs/handoffs/2026-05-09-ai-council-audit-sync/. Governance cycle complete
  from .dev-knowledge side. Execution test (NEW chat consuming bundle) is the
  next operational step — not tracked here; Rob opens new ai-council chat with
  bundle when ready.)

- **Archived:** 2026-05-16

### [P1] [done] AI Council cross-project transcript routing
- **What:** AI Council CLI currently emits transcripts to `ai-council/output/` only; cross-project routing to `<project>/docs/decisions/transcripts/` is via manual archival. Client requirements spec drafted (R1-R8: deterministic routing via YAML frontmatter `target-project:` key, config-driven path resolution, supports all 4 modes, loud failure on unknown target). Mechanism choice (push frontmatter vs pull command vs config-based) is Council debate territory. Implementation lives in `ai-council` repo, not `.dev-knowledge`.
- **Why:** Aspirational "dual-write" claim in ESSENTIALS was drift signal — feature didn't exist in CLI (verified during Item 0 audit 2026-05-11). 12 manual archives in `.dev-knowledge/docs/decisions/transcripts/` are pre-feature state. Deterministic routing reduces drift across ecosystem; supports VISION Strategic emphasis "Cross-repo methodology consistency."
- **Vision ref:** VISION.md "Disseminator" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Item 0 strażnik audit)
- **Status:** done (2026-05-11 — implemented in ai-council: `routing.py` TargetResolver, `--target-project` CLI flag, frontmatter `target-project:` key, `dev_root` + `target_projects` config schema per ADR-43 amendment cycle 1; 359+ tests; CHANGELOG 2026-05-11)

- **Archived:** 2026-05-16

### [P2] [done] Structure and universalize scrum-master review propagation process
- **What:** Codify the full scrum-master review workflow as a templated, repeatable process. Scope: (a) cover-letter template for operator routing (context + review type + process description + action requested + audit-trail note); (b) distinction from cross-repo amendment handshake (unilateral vs bilateral); (c) single-round-trip framing (no Turn 2/3/4 expected; architect pushback opens new conversation, not inline reply); (d) report archival convention (`docs/audits/` per content-scoped principle); (e) review report structure template (executive summary + findings by area + severity classification + recommended actions + out-of-scope). Destination: new section in PLAYBOOK and/or ADR-44.
- **Why:** First empirical instance (Prompt L ai-council review 2026-05-12) operated ad-hoc — operator had to ask routing framing because cover-letter structure was implicit, not templated. N=1 anti-pattern applies; codify now since operator has explicit framing intent, OR await N=2. Operator's call. Second application (corp-monorepo) is imminent — operationalizing before that run avoids second ad-hoc session.
- **Vision ref:** VISION.md "Methodology Author" + "Auditor" functions
- **Added:** 2026-05-12 by rob (Prompt M)
- **Status:** done (2026-05-12 — resolved by PLAYBOOK § 17 Scrum-Master Review Propagation + `templates/scrum-master-cover-letter.md`. ADR-44 authority codification deferred pending N=2.)

---

- **Archived:** 2026-05-16

### [P1] [done] ADR naming convention reconciliation (underscore vs hyphen)
- **What:** Cross-repo audit (2026-05-11) found two incompatible ADR naming conventions: `.dev-knowledge` uses `ADR-NN_topic.md` (underscore); `corp-monorepo` and `ai-council` use `ADR-NN-topic.md` (hyphen). ADR-34 was ambiguous. Resolution: amend ADR-34 (this cycle's Prompt J, J1); migration to follow in Prompt K (.dev-knowledge) and Phase 2 (child repos).
- **Why:** Cross-repo inconsistency between `.dev-knowledge` (underscore) and corp-monorepo/ai-council (hyphen) created contradictory tooling expectations; a single-convention mandate was required before Phase 2 child-repo migration could be prescribed without ambiguity.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** done — ADR-34 amended (commit ec45b2c, this branch). Migration tracked separately: .dev-knowledge in Cross-stream P1 "atomic migration" below; child repos in P2 migration entries below.

- **Archived:** 2026-05-16

### [P2] [done] ARCHITECTURE.md root placement enforcement
- **What:** ADR-38 mandated ARCHITECTURE.md but didn't specify path. `corp-monorepo` placed it at `docs/ARCHITECTURE.md` (not root). Decision needed: root or `docs/`?
- **Why:** ADR-38 mandated ARCHITECTURE.md but left path unspecified; without a root-vs-docs ruling, Phase 2 migration prescriptions would be inconsistent across repos.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A3)
- **Status:** done — ADR-38 amended (commit f264966, this branch): root placement now explicit. corp-monorepo migration tracked in P2 "corp-monorepo migration" entry below.

- **Archived:** 2026-05-16

### [P2] [done] `_archive/` convention — standardize (drop underscore prefix per Council)
- **What:** `_archive/` (underscore-prefix) existed in `.dev-knowledge/docs/handoffs/` and `ai-council/handoffs/`. `corp-monorepo` used bare `archive/` (no underscore). No ADR governed which. Decision: adopt bare `archive/` universally (consistent with hyphen mandate, no underscore anywhere).
- **Why:** Underscore-prefix was inconsistent with the hyphen mandate and created mixed folder naming (`_archive/` in .dev-knowledge vs `archive/` in corp-monorepo); universal convention was needed before Phase 2 migration could prescribe consistent folder names.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A2)
- **Status:** done — operator decision ratified by Council hyphen-universal vote (Q1-A). `.dev-knowledge/docs/handoffs/archive/` → `archive/` folder rename deferred to Prompt K (atomic migration). Child repo `_archive/` cleanup in Phase 2 visits.

- **Archived:** 2026-05-16

### [P1] [done] .dev-knowledge atomic migration to hyphen convention (Prompt K scope)
- **What:** Atomic PR for .dev-knowledge: (1) 16 ADR + 14 transcript filename renames to hyphen; (2) Markdown link reference rewrites across 23 living docs; (3) `docs/handoffs/_archive/` → `docs/handoffs/archive/` folder rename (per A2 underscore drop ratified by Council); (4) retroactive archival of cross-repo decision propagation artifact (K1.4 skipped — files absent from Downloads); (5) 6 flat legacy .md + v2 folder relocated to `docs/handoffs/archive/legacy/`. Single atomic commit K1 (a95318d); pre-commit: pass.
- **Why:** ADR-34 amendment (this cycle) specifies hyphen universal mandate; .dev-knowledge must lead the migration before child repos can follow. Atomic commit ensures link integrity — partial migration creates broken references.
- **Vision ref:** VISION.md "Knowledge Guardian" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** done — commit a95318d (branch chore/atomic-cleanup-hyphen-migration, Prompt K, 2026-05-12).

- **Archived:** 2026-05-16

### [P1] [done] Cross-repo handshake: ADR-34 amendment propagation to ai-council
- **What:** Cross-repo notification artifact generated 2026-05-11 (browser chat session alongside Prompt J). Operator routes to ai-council repo. ai-council architect proposes own implementation of hyphen convention (CLI output format change: `council_out_*` → `council-out-*`). Per ADR-43 cross-repo cycle pattern.
- **Why:** ADR-34 is now universal mandate; ai-council CLI generates filenames that violate it. Cross-repo handshake ensures adoption without unilateral changes to ai-council.
- **Vision ref:** VISION.md "Disseminator" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** done (2026-05-12 — Cycle 2 closed 2026-05-11. Turn 1 routed; Turn 2 received from ai-council architect with implementation plan; Turn 3 closure routed per "handshake = 1 round trip" principle.)

- **Archived:** 2026-05-16

### [P1] [done] Session D — `.dev-knowledge` dated-entries cleanup (ADR-46 compliance)
- **What:** Fix audit findings surfaced by `check_dated_entries_format`: (1) `LESSONS.md` non-ISO H2 heading `## Entries` — retitle/restructure to ADR-46 envelope; (2) `CHANGELOG.md` reverse-chrono ordering violation (`2026-04-24` appears before `2026-04-25`).
- **Why:** ADR-46 mandates ISO `## YYYY-MM-DD` headings and reverse-chrono ordering; both violations block a PASS on `dated_entries_lessons` and `dated_entries_changelog` checks.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-46
- **Added:** 2026-05-15 by rob (Session E dogfood findings — Step 3 inventory)
- **Status:** done (2026-05-16 — removed ## Entries H2; reordered pre-convention tail entries in both LESSONS.md and CHANGELOG.md; all dated_entries checks PASS)

- **Archived:** 2026-05-16

### [P1] [done] Session D — `.dev-knowledge` BACKLOG.md → BACKLOG_ARCHIVE.md extraction (ADR-47 compliance)
- **What:** (1) Run `scripts/backlog_extract.py` to move all archived items to new `BACKLOG_ARCHIVE.md`; (2) Fix 8 entries missing `Why:` field (migration-era entries in Cross-repo Naming and Hyphen Convention sections); (3) Address 2 kill-criterion WARNs.
- **Why:** ADR-47 mandates two-file state architecture; completed items pollute the active backlog, reducing scannability and triggering the session-start validator fail-fast.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-47
- **Added:** 2026-05-15 by rob (Session E dogfood findings — Step 3 inventory)
- **Status:** done (2026-05-16 — 15 entries extracted to BACKLOG_ARCHIVE.md; 8 Why: fields added; >300-line WARN resolves after this extraction; Cross-stream WARN accepted + new Stream taxonomy grooming P2 item added)

- **Archived:** 2026-05-16

### [P1] [done] Session D — `ai-council` dated-entries cleanup (ADR-46 compliance)
- **What:** Fix audit findings surfaced by `check_dated_entries_format`: (1) `LESSONS.md` non-ISO H2 heading `## Session: Phase 1 Foundation (2026-02-21)` — retitle to ISO `## YYYY-MM-DD` envelope per ADR-46; (2) `JOURNAL.md` reverse-chrono ordering violation (`2026-03-15` before `2026-05-12`) — reorder entries.
- **Why:** ADR-46 mandates ISO envelope headers and reverse-chrono ordering; both violations produce FAIL on `dated_entries_lessons` and `dated_entries_journal` checks.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-46; pairs with Phase 2 universalization rollout (Cross-stream P2)
- **Added:** 2026-05-15 by rob (Session E dogfood findings — Step 3 inventory)
- **Status:** done (2026-05-16 — 2026-05-16 re-audit shows ai-council `dated_entries_lessons` WARN, `dated_entries_journal` PASS, overall PASS; ordering violations resolved; residual scope-tag WARN tracked as new P3 item)

- **Archived:** 2026-05-16

### [P1] [done] Session D — `ai-council` BACKLOG.md ADR-47 compliance
- **What:** (1) Create `BACKLOG_ARCHIVE.md` in ai-council (no archived items in current BACKLOG but file required by ADR-47); (2) Fix 1 entry with `[blocked]` status (not a valid ADR-47 status — must be `[open]` or `[superseded]`); (3) Add missing `Status:` field to 11 entries.
- **Why:** ADR-47 mandates two-file state + specific valid status values + required entry fields; missing these produces FAIL on `backlog_organization` check.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-47; pairs with Phase 2 universalization rollout (Cross-stream P2)
- **Added:** 2026-05-15 by rob (Session E dogfood findings — Step 3 inventory)
- **Status:** done (2026-05-16 — 2026-05-16 re-audit shows ai-council `backlog_organization` PASS; two-file state and required fields confirmed compliant)

- **Archived:** 2026-05-16

