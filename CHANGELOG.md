# Changelog — Dev Knowledge

Notable changes to the dev practice knowledge base.

---

## 2026-05-15

### Added (Audit Tool P2 — ADR-46 + ADR-47 checks)

- `scripts/checks/check_dated_entries_format.py` — ADR-46 check: validates `## YYYY-MM-DD`
  envelope + reverse-chrono ordering in LESSONS.md, JOURNAL.md, and CHANGELOG.md per-repo.
- `scripts/checks/check_backlog_organization.py` — ADR-47 check: validates two-file state
  (BACKLOG.md + BACKLOG_ARCHIVE.md), entry status tokens (`[open]`/`[superseded]` only),
  required fields (What / Why / Added / Status), and kill-criterion thresholds.
- `scripts/backlog_extract.py` — deterministic extraction script: moves `[done]`/`[abandoned]`
  entries from BACKLOG.md to BACKLOG_ARCHIVE.md. <50 LOC, no LLM prompt, per ADR-47 spec.
- `tests/test_check_dated_entries_format.py` + `tests/test_check_backlog_organization.py` +
  `tests/test_backlog_extract.py` — fixture-based tests for all new checks + script.
- `tests/test_audit_integration.py` — integration test covering all 5 checks end-to-end.
- Audit Tool total: **3 checks → 5 checks** (vision_md, adr38_baseline, claude_md,
  dated_entries_format, backlog_organization).

### Changed (Audit Tool P2 — ADR-46 + ADR-47 checks)

- Dogfood audit run against `.dev-knowledge` + `ai-council` with all 5 checks.
  51 total checks: 6 pass, 42 fail, 3 warn. High finding count expected — Session D scope.
- `ecosystem/.dev-knowledge/state.yaml` + `ecosystem/ai-council/state.yaml` updated.
- `ecosystem/.dev-knowledge/history/2026-05-15.md` + `ecosystem/ai-council/history/2026-05-15.md`
  updated with P2 check results.
- `docs/audits/2026-05-15-ecosystem-audit.md` updated to include all 5 checks.
- BACKLOG.md: Stream C P2 audit-extension item added as `[done]`; 4 new Session D scope
  items seeded (Stream C P1 x2 for `.dev-knowledge` cleanup, Stream B P1 x2 for `ai-council`
  cleanup).

### Notes (Audit Tool P2)

- ai-council `git status` confirmed clean after cross-repo audit — ADR-36 read-only
  contract intact.
- Session D scope (cleanup pass against real content per ADR-46 + ADR-47 findings) is
  the next downstream session. See BACKLOG Stream C P1 + Stream B P1 items for anchors.

---

### Added (Governance ADRs B+C)

- `docs/decisions/ADR-46-cross-repo-dated-entries-format.md` — cross-repo standard for
  LESSONS.md / JOURNAL.md / CHANGELOG.md. Universal envelope (ISO `## YYYY-MM-DD`,
  reverse-chronological prepend) + file-specific payloads (LESSONS 6-field preserved
  per ADR-29; JOURNAL free-prose; CHANGELOG Keep-a-Changelog semantic groupings).
  ADR-27 HTML comments remain authoritative for scope; YAML frontmatter optional
  and additive only. Archive trigger 10k tokens, rotation tooling deferred.
  Stdlib-regex validator required; markdown-AST library adoption gated behind
  future ADR amendment with empirical justification.
- `docs/decisions/ADR-47-cross-repo-backlog-organization.md` — cross-repo BACKLOG.md
  schema. Two-file state architecture: `BACKLOG.md` (active: `[open]` + `[superseded]`)
  + new `BACKLOG_ARCHIVE.md` (`[done]` + `[abandoned]`, append-only, mirrors stream
  headings). Stream-grouped structure with P1/P2/P3 priorities preserved. Required
  entry fields: What, Why, Added, Status (Vision ref recommended). Session-start
  validator fail-fast on `[done]` in `BACKLOG.md`. Deterministic <50 LOC extraction
  script for Session D — explicitly no LLM prompt. Kill criteria for ADR review:
  BACKLOG.md > 300 lines, any single stream > 15 open items, or Cross-stream > 33%.
  Scope tags / SCOPE_SCHEMA explicitly not adopted (streams carry routing signal).
- 4 council transcripts in `docs/decisions/transcripts/` (research B + pick B +
  research C + pick C, dated 2026-05-15).

### Changed (Governance ADRs B+C)

- BACKLOG.md: Stream C P1 entries for Entry 1 + Entry 2 flipped to `[done]`. Stream C
  P2 "ADR-29 amendment — prepend at top" marked `[superseded]` by ADR-46 (universal
  prepend mandate covers it). New Stream C P3 entry for ADR-41 amendment (cross-
  reference ADR-47 from ADR-41 § Storage + Related metadata).

### Notes (Governance ADRs B+C)

- Files unchanged in this session. Cleanup pass against actual LESSONS / JOURNAL /
  CHANGELOG / BACKLOG content across all repos is Session D scope. Audit tool
  extension (new `check_dated_entries_format` + `check_backlog_organization` checks)
  is Session E scope.

---

### Added (Audit Tool P1)

- `scripts/audit.py` — Click CLI with 4 commands per ADR-36: `audit run`, `audit repo <name>`,
  `audit registry update`, `audit health`. Bootstrap via `--repo-path <path>` flag.
- `ecosystem/` — state schema: per-repo `state.yaml` + append-only `history/YYYY-MM-DD.md`
  per ADR-36 architecture.
- 3 deterministic audit checks: `vision_md` (ADR-33 frontmatter), `adr38_baseline` (ADR-38
  canonical mandatory files + dirs), `claude_md` (ADR-31 CLAUDE.md presence).
- Markdown report to `docs/audits/YYYY-MM-DD-ecosystem-audit.md`; overwrites on same-day re-run.
- `tests/test_audit.py` — 27 tests: schema roundtrip, each check on good/bad fixtures, report
  generation, health command.
- `config/requirements-dev.txt` — added `click>=8.0` and `pyyaml>=6.0`.

### Notes (Audit Tool P1)

- Self-audit finding: `.dev-knowledge` FAIL on `adr38_baseline` (missing `src/` + `pyproject.toml`).
  Governance repo doesn't follow full code-repo ADR-38 structure — new BACKLOG item Stream C P2.
- Cross-repo audit: `ai-council` PASS with WARN (`ARCHITECTURE.md` optional at tier M).
- Pre-flight gate caught: architect-inferred mandatory-files list in handoff was wrong — `LESSONS.md`
  and `JOURNAL.md` are `.dev-knowledge`-specific (not universal); `src/`, `tests/`, `pyproject.toml`
  were missing from the inferred list. Implementation uses ADR-38 canonical spec.

---

### Fixed (v3.3.3)

- Handoff state validation: strict-equality check replaced with ancestor check
  (`git merge-base --is-ancestor`). The "expected HEAD" field in `01_MANIFEST.md` pins Stage 1
  input HEAD; current HEAD at validation time is by-design a descendant after Stage 3 commits.
  Strict equality produced false-negative validation on the 2026-05-15 case (bundle pinned
  `b640bcf9`, current HEAD `777af78`). Operator override is no longer required for benign
  Stage 3 drift.

### Changed (v3.3.3)

- `protocols/HANDOFF_PROCESS.md` v3.3.2 → v3.3.3: validation logic amendment documented.
- Template surfaces updated: `HANDOFF_FOLDER_TEMPLATE.md` state validation wording and receiver
  synthesis line; `01_MANIFEST.md` description in folder structure and file responsibilities table.

### Verified (v3.3.3)

- Empirical smoke test: `git merge-base --is-ancestor b640bcf9 HEAD` → exit 0 on 2026-05-15 case.

---

### Fixed (v3.3.2)

- `templates/HANDOFF_FOLDER_TEMPLATE.md` cross-repo parameterization (v3.3.2):
  articulation gate item #1 now uses `{repo}` placeholder (was hardcoded `.dev-knowledge`);
  `02_VISION.md` now sources target repo's VISION via `{TARGET_REPO_PATH}` (was unconditional
  `.dev-knowledge` VISION); new conditional `02b_ECOSYSTEM_VISION.md` for ecosystem context
  when target ≠ `.dev-knowledge`. Articulation gate item #4 terminology fixed: "per BOUNDARIES"
  → "Hard Constraints section" (matches 07_ACTION_PLAN.md section header since v3.3).
- `docs/handoffs/2026-05-14-ai-council-session-sync/` regenerated from v3.3.2 template:
  `02_VISION.md` now ai-council's mission; new `02b_ECOSYSTEM_VISION.md` carries .dev-knowledge
  ecosystem context; articulation gate and reading order corrected; format v3.3.2; 12 checksummed
  files. Broken state preserved in git history at `c09ee71`.

### Changed

- `protocols/HANDOFF_PROCESS.md` v3.3.1 → v3.3.2: amendment scope documented (Bugs A/B/C),
  new `02b_ECOSYSTEM_VISION.md` conditional file, Hard Constraint #3 formal amendment by
  operator authorization 2026-05-14, mandatory cross-case trace requirement for future amendments.

---

## 2026-05-14

### Added

- `protocols/PLAYBOOK.md`: added Section 10 (BACKLOG Grooming Workflow) covering ADR-41 schema, per-handoff ~2 min grooming, quarterly deep grooming, split-brain prevention; added Section 18 (Ecosystem Audit Tool Workflow) covering ADR-36 read/write boundary, CLI commands, 4-phase roadmap; amended Section 8 (Handing Off Between Sessions) in-place for ADR-37 two-phase Current/Future State protocol (dropped stale marker, retagged meta); extended "Project Scale Tiers" structural section with ADR-40 tier transition procedures (S→M, M→L, demotion rules). Sections 10–17 renumbered to 11–17 (+19 for old §17) to maintain sequential ordering. Closes Stream C P1 methodology debt outstanding since 2026-04-30.
- Cross-reference updates: ESSENTIALS.md §16→17, ADR-28 §12→13 (×2), 2026-04-27 deep-cleansing-diagnostic.md §16→17 (×2), PLAYBOOK.md internal §10→11 + §12→13 (×3).

- `LESSONS.md`: appended 9th architect-discipline observation (`universal-without-cross-case-verification`) — interleaved capture from parallel ai-council handoff observation; evidence: v3.3.1 universality claim validated only against .dev-knowledge self-handoff, two cross-repo template bugs surfaced on first ai-council Stage 3 run
- `BACKLOG.md`: added Stream C P1 item for v3.3.2 (HANDOFF_FOLDER_TEMPLATE parameterization for cross-repo handoffs); captured here, fix deferred to v3.3.2 dedicated session per Hard Constraint #3 of active action plan
- `LESSONS.md`: appended 8 architect-discipline observations (5 primary + 3 secondary) from 2026-05-14 extended session — `captured for review` (ref `docs/handoffs/2026-05-14-dev-knowledge-session-sync/06_STATE_OF_PLAY.md`)
- Handoff Stage 3 complete: `docs/handoffs/2026-05-14-ai-council-session-sync/` (11-file bundle, session-sync, v3.3.1). Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-ai-council-session-sync/`. Directives: synthesizer scoring → ADR-01 amendment; AGENTS.md; ADR-38 Scale M compliance; hyphen spot-check; origin push.
- Handoff Stage 3 complete: `docs/handoffs/2026-05-14-dev-knowledge-session-sync/` (11-file bundle, session-sync, v3.3.1). First handoff cycle generated under v3.3.1 audience-awareness rules. Stage 1+2 inputs archived at `docs/handoffs/archive/2026-05-14-dev-knowledge-session-sync/`.

### Changed

- `LESSONS.md`: rewrote 9 same-day entries to canonical 6-field schema
  (dropped non-schema `— source: X; evidence: Y` trailer) and relocated
  from tail to top of dated-entries section per operator visibility
  convention. Same-day correction; ADR-29 same-day override per operator
  decision 2026-05-14
- `BACKLOG.md`: added Stream C P2 item for deferred ADR-29 ordering
  convention amendment (formalize "prepend at top" going-forward)

- Handoff process amended to v3.3.1 (HANDOFF_QUESTION_TEMPLATE.md +
  HANDOFF_PROCESS.md):
  - Stage 1 template gains an `Audience Awareness` section (7 rules
    + 1 self-check) so the OLD chat writes Stage 2 for the new chat
    audience that never sees Stage 1.
  - Rules address 7 empirically observed gap patterns in v3.3 Stage 2
    responses: self-referential meta-framing, Stage 1 references,
    forward references, invisible session-history references, in-flight
    work references, cross-reference burdens, external research
    citations.
  - Verification list in Stage 1 template gains an `Audience awareness
    check` requiring the OLD chat to mentally simulate fresh-LLM
    reading before submitting.
  - Corrects v3.3 scope error (Stage 1 template was excluded; producing
    the 7-gap pattern in resulting Stage 2 responses).

---

## 2026-05-13

### Changed

- Handoff process refined to v3.3 (HANDOFF_PROCESS.md + HANDOFF_FOLDER_TEMPLATE.md):
  - 06_STATE_OF_PLAY and 07_ACTION_PLAN section names changed from SBAR
    codes (OBJECTIVE/REALITY/RATIONALE/DIRECTIVES/BOUNDARIES) to plain
    English (`What was completed this session` / `Current state` /
    `Action plan` / `Hard Constraints` etc.) per 2026-05-12 audit
    "decoder-required language" findings.
  - First reference to any status code (P-NN/F-NN/ADR-NN) in any
    section now requires in-line gloss; subsequent references in same
    section may use bare code.
  - DO-NOT lists split into `Hard Constraints` (max 5, critical for
    next step, bold) and `Narrow scope rules` (collapsed / sub-bulleted).
  - Verb-led sentences required in 06/07 state descriptions; process-
    language noun phrases ("amendment cycle closed", "compliance
    verification") not permitted.
- 00_first-message.md spec now requires mandatory articulation gate as
  the new chat's first action: 4-item articulation (role per VISION /
  phase per BACKLOG / immediate next action per ACTION_PLAN directive
  #1 / top 3 Hard Constraints per BOUNDARIES) in own words; operator
  confirms via `role confirmed` before any other work. Empirical basis:
  2026-05-13 browser session showed delivery ≠ internalization.
- ADR-45 status demoted from `Accepted` to `Superseded` (v1 over-
  concluded toward bundle replacement; conflicts with ADR-42 v3.2 +
  audit's "preserve" findings). v2 rewrite deferred pending empirical
  test of minimum-viable refinement.

---

- feat(decisions): add ADR-45 Handoff Architecture v4 (supersedes ADR-42 v3.2) — invariant/session separation, 2-file handoff (MANIFEST + NEXT), defense-in-depth harness enforcement; pending implementation prompts
- docs(lessons): archive 10 methodology lessons from 2026-05-13 handoff-architecture design session (9 from main append + 1 channel-discipline addendum)

---

## 2026-05-12

### Added
- Stage 1 questionnaire template (`templates/HANDOFF_QUESTION_TEMPLATE.md`): inline reminder questions block (pointer to HANDOFF_PROCESS master rule; no content duplication)

---

## 2026-05-12

### Added
- `HANDOFF_PROCESS.md`: Universal Self-Containment Rule section (Stage 1 / Stage 2 / Stage 3 explicit guidance + pre-send coherence checklist + ADR-41 cross-repo scope)
- `LESSONS.md` entry: handoff self-containment universal pattern + empirical failure capture

---

## 2026-05-12

- feat(playbook): add § 17 Scrum-Master Review Propagation — codifies three-stage flow (audit → route → implement), addendum mechanism, distinction from cross-repo amendment handshake, single-round-trip framing
- feat(templates): add `scrum-master-cover-letter.md` — operator-paste-ready routing template, ADR-34 hyphen naming

## 2026-05-12 — Handoff Stage 3: ai-council session-sync

### Added
- `docs/handoffs/2026-05-12-ai-council-session-sync/` — 12-file ADR-42 v3.2 handoff folder; Stage 2 architect knowledge (OBJECTIVE/REALITY/RATIONALE/DIRECTIVES/BOUNDARIES) preserved; HEAD `f094d08` pinned
- `docs/handoffs/archive/2026-05-12-ai-council-session-sync/` — Stage 1 + Stage 2 inputs archived

### Changed
- `BACKLOG.md` — Phase 2 universalization + VISION.md tier declarations updated with ai-council progress notes

---

## 2026-05-12 — Handoff Stage 3: dev-knowledge session-sync

### Added
- `docs/handoffs/2026-05-12-dev-knowledge-session-sync/` — 11-file ADR-42 v3.2 handoff folder; Stage 2 architect knowledge preserved; HEAD `0125f1b` pinned
- `docs/handoffs/archive/2026-05-12-dev-knowledge-session-sync/` — Stage 1 + Stage 2 inputs archived

---

## 2026-05-12 — Prompt N: Session handoff

### Added
- `docs/handoffs/2026-05-12-session-handoff/` — session handoff for next-session context primer

---

## 2026-05-12 — Prompt M: Governance freshness audit + targeted updates

### Changed
- `ARCHITECTURE.md`: layout example `ADR-NN_*.md` → `ADR-NN-*.md`; key conventions filename block updated (ADR-NN-topic.md, council-out-* CLI format, "consolidation pending" removed)
- `CONTRIBUTING.md`: ADR process section filename prescription updated from underscore to hyphen (`ADR-NN_` → `ADR-NN-` in 2 places)
- `README.md`: Conventions section + Navigation section ADR filename examples updated to hyphen
- `protocols/PLAYBOOK.md`: ADR-NN-*.md in CLAUDE.md scope section; §File naming conventions TBD block replaced with ADR-34 pointer; file taxonomy table ADR row updated; Council Debate Archival Protocol archival target filenames updated to council-out-* format

### Added
- `BACKLOG.md`: Cross-stream P2 entry — Structure and universalize scrum-master review propagation process (cover-letter template, single-round-trip framing, report archival convention, review report template structure)

---

## 2026-05-12 — Prompt L: Scrum-master review of ai-council + legacy transcripts relocation

### Added
- `docs/audits/2026-05-11-ai-council-scrum-master-review.md` — first scrum-master review under new authority pattern; 10 findings (1 critical, 6 important, 3 minor)
- `docs/decisions/transcripts/archive/legacy/` subfolder for pre-CLI `DECISION_NN_*` historical transcripts (3 files relocated)
- `LESSONS.md`: scrum-master review authority pattern (first empirical instance)
- `BACKLOG.md`: Cross-stream P2 (codify scrum-master review pattern) + P3 (extend to other repos)

### Changed
- 3 legacy `DECISION_NN_*` transcripts relocated from `docs/decisions/transcripts/` to `docs/decisions/transcripts/archive/legacy/` (pre-CLI historical class separation); path references updated in ADR-31, ADR-32, decisions/README.md, CHANGELOG.md
- `BACKLOG.md`: AI Council cross-project transcript routing marked done (2026-05-11 implementation)

---

## 2026-05-12 — Prompt K: Atomic file-level cleanup (hyphen convention migration)

### Changed
- File-level cleanup atomic migration per Council 2026-05-11 hyphen mandate: 16 ADR renames + 14 transcript renames + folder rename (`_archive/` → `archive/`) + 6 flat legacy .md + v2 folder relocation + 23 living doc link rewrites in single revertable commit (a95318d)
- `BACKLOG.md`: Cross-stream P1 ".dev-knowledge atomic migration to hyphen convention" marked done

### Added
- `docs/handoffs/archive/legacy/` subfolder for pre-ADR-42 handoff format archival (6 flat .md + v2 folder `2026-04-27-stream-c-session-1-final/`)
- `LESSONS.md`: merge/cleanup completion pattern (sub-instance of operator-is-not-the-terminal)
- `LESSONS.md`: punted-migration anti-pattern (empirical instance: session 2026-05-11)
- `scripts/migrate_links.py`: reusable link migration utility for Phase 2 cross-repo migrations

### Skipped
- K1.4 (cycle 2 cross-repo propagation artifact archival): files absent from Downloads at time of execution

---

## 2026-05-12 — Prompt J: ADR-34 + ADR-38 amendments + BACKLOG reclassification

### Changed
- `docs/decisions/ADR-34_file_naming_convention.md`: separator convention amended to universal hyphen mandate per AI Council 2026-05-11 (all 4 panel models Q1-A, Q2-A, Q3-A, Q4-A). Scope changed from mandate (.dev-knowledge) / recommendation (child repos) to universal mandate across all Dev/ repos. ADR and transcript table rows updated from underscore to hyphen. Versioning archive path updated. Universalization section updated. Amendments trail entry added.
- `docs/decisions/ADR-38_universal_repo_architecture.md`: ARCHITECTURE.md placement specified as root (was unspecified). Conversational A3 decision from 2026-05-11 cross-repo audit. Amendments trail entry added.
- `BACKLOG.md`: two new sections added — "Cross-repo Naming + Architecture Migration (Prompt H audit + Prompt J ratification)" with 7 reclassified Prompt H items; "Hyphen Convention Migration Sequence (Prompt J ratification)" with 7 new migration sequence entries covering Prompt K atomic migration, cross-repo handshake, CI enforcement, corp-monorepo + ai-council Phase 2 migration (expanded scope), content-scoped archival principle codification, and A5 Phase 2 retirement.

### Added
- `LESSONS.md`: content-scoped archival principle (2026-05-11 entry) — archive subfolder location follows artifact type; generic docs/archive/ mixed-content grab-bag is anti-pattern; codification deferred to second empirical instance.

---

## 2026-05-11 — Item 0 Prompt C: Codex M1 fix

### Fixed
- `protocols/PLAYBOOK.md` "Council Debate Archival Protocol" section
  (~line 1458): reconciled with reality. Removed stale dual-write claim
  that contradicted "Council output convention (current state)" added in
  commit `f05e267`. Operators no longer instructed to skip manual archival
  they actually need to perform. Addresses Codex `/review` finding M1
  from `43715b3`.

---

## 2026-05-11 — Docs alignment + BACKLOG updates (Item 0 strażnik audit)

### Changed
- Aligned canonical docs with reality after Item 0 strażnik audit (2026-05-11):
  - `protocols/ESSENTIALS.md` — corrected Council output convention text (was aspirational dual-write description; CLI is single-target with manual archival)
  - `protocols/PLAYBOOK.md` — added "Council output convention (current state)" section
  - `docs/handoffs/README.md` — rewrote for v3.2 current format + pre-v3.2 legacy classification
  - `docs/decisions/README.md` — rewrote with full ADR index 27-42 + transcript naming convention + ADR↔transcript traceability table
  - `BACKLOG.md` — added Cross-stream P1 "AI Council cross-project transcript routing"; added Stream B P2 "ai-council needs AGENTS.md"; superseded Stream C P3 "Council CLI dual-write trigger logic"; updated Cross-stream P1 "Council decisions management consolidation" progress

---

## 2026-05-11 — Handoff lifecycle fix + stale cleanup

### Fixed
- Stage 3 handoff lifecycle in `HANDOFF_PROCESS.md`: explicit `Move-Item`
  semantics, empty-dir cleanup, post-state validator added to Stage 3 step 10
  and validation checkpoints table. Prior implementation used copy semantics,
  leaving stale `_in_progress/{slug}/` directories after Stage 3 completion.

---

## 2026-05-09 (night) — Stage 3: .dev-knowledge session-sync handoff generated

### Added
- `docs/handoffs/2026-05-09-dev-knowledge-session-sync/` — 12-file flat handoff
  bundle per ADR-42 v3.2 (Stage 3 output):
  - `00_README.md` — 10-step operator workflow
  - `00_first-message.md` — NEW chat first message with press-back partner instruction
  - `01_MANIFEST.md` — entry point, state validation, file index
  - `01_manifest.json` — SHA-256 checksums for all 11 content files
  - `02_VISION.md` — full VISION.md copy (includes Strategic emphasis section)
  - `03_PLAYBOOK.md` — full PLAYBOOK.md copy
  - `04_ESSENTIALS.md` — full ESSENTIALS.md copy
  - `05_GOVERNANCE_ESSENCES.md` — ADR-33/36/37/40/41/42 essences
  - `06_STATE_OF_PLAY.md` — Stage 2 REALITY+RATIONALE + Stage 3 verification layer
  - `07_ACTION_PLAN.md` — Stage 2 OBJECTIVE+DIRECTIVES+BOUNDARIES + DoD fix clarification
  - `08_TREE.txt` — .dev-knowledge file inventory at Stage 3
  - `09_EXECUTION_EVIDENCE.md` — return-trip template
- `docs/handoffs/_archive/2026-05-09-dev-knowledge-session-sync/` — Stage 1+2 inputs

### Verification layer findings
- Drift confirmed safe: Stage 1 SHA f87a5cc → Stage 3 HEAD 5f09fe1 (4 intra-session commits)
- DoD bug target clarified: "5 required sections" in ai-council 07_ACTION_PLAN.md:9,
  NOT in HANDOFF_FOLDER_TEMPLATE (template has no pre-populated DoD text)
- 5/6 witnessed claims verified; 4 architect unknowns resolved

---

## 2026-05-09 (night, refinement) — BACKLOG strategic priorities + stage1 v2

### Added
- `BACKLOG.md` Cross-stream items — 9 new entries capturing Rob's strategic
  plan for next sessions (all [P1]/[P2]/[P3], no specific repo names where
  Rob requested omission):
  - [P1] Council decisions management consolidation
  - [P1] Sacred-files maintenance enforcement
  - [P2] Hooks audit + consolidation
  - [P2] Skills universalization across repos
  - [P2] Ecosystem standards audit against major repo
  - [P3] Kimi K2 model integration evaluation
  - [P3] Scale tier evaluation re-evaluation (references existing P2 research item)
  - [P3] Large repo migration preparation
  - [P3] VS Code productivity maximization

### Changed
- `docs/handoffs/_in_progress/2026-05-09-dev-knowledge-session-sync/stage1-question.md`
  Section B: HEAD sha updated to f87a5cc; BACKLOG items section expanded with
  all 9 new strategic priorities; "press back on vague items" instruction
  added before closing divider — next chat is refinement partner, not just
  executor (6 concrete behaviors: sharpen vague items, first steps, surface
  deps, debate vs. conversational gating, flag compound items, scope bounds).

### Notes
- This refinement follows the earlier 2026-05-09 (night) wrap-up session
  (5 commits on `chore/session-2026-05-09-wrap-up`, merged). That session
  established the handoff structure. This refinement makes BACKLOG reflect
  Rob's true strategic priorities so Stage 2 architect response carries
  full context into Stage 3 bundle.

---

## 2026-05-09 (night, session wrap-up) — Evidence commit + VISION emphasis + Stage 1 handoff

### Committed
- `docs/handoffs/2026-05-09-ai-council-audit-sync/09_EXECUTION_EVIDENCE.md`
  closing return trip for ai-council audit-sync handoff. End-to-end ADR-42
  v3.1+v3.2 test fully documented: drift detection, directive execution,
  pytest baseline held (310/310), Codex review complete (no blockers).

### Added
- `VISION.md` Strategic emphasis section: 4 current directions — velocity
  in LLM adoption, cross-repo methodology consistency, methodology evolution
  as obsession, lessons capture as default. Conversational clarification per
  Rob's VISION rule (Scope changes require Council; emphasis clarifications
  are conversational). No specific repo/file references.
- `docs/handoffs/_in_progress/2026-05-09-dev-knowledge-session-sync/`
  with `stage1-question.md` (session-sync Stage 1; 5 pipeline questions
  adapted for self-handoff) and pre-created `stage2-response.md` template.

### Session summary
Historic 2026-05-09 session delivered: Phase 1 governance closure (9 ADRs
ratified), ADR-42 handoff infrastructure v3.0→v3.1→v3.2 evolution,
end-to-end ai-council audit-sync test, ~16 methodology debt lessons captured,
VISION continuous improvement + strategic emphasis updated, 36+ branches
cleaned. Wrap-up: 4 additional commits closing return trip and launching
.dev-knowledge self-handoff Stage 1.

---

## 2026-05-09 (night) — ADR-42 v3.2: Q&A loop + continuous improvement + operator clarity

### Added
- ADR-42 v3.2 amendment: Stage 2.5 Q&A iteration loop (max 3 rounds between
  NEW chat and OLD chat for clarification questions before Stage 3 prompt
  generation)
- `protocols/HANDOFF_PROCESS.md` v3.2: Stage 2.5 procedure documented; "What
  changed v3.1 → v3.2" table; Section history entry
- `templates/HANDOFF_FOLDER_TEMPLATE.md` 00_README spec: explicit 10-step
  operator workflow (open NEW chat → upload → paste first-message → synthesis
  confirmation → Q&A loop → prompt generation → Claude Code execution → return
  evidence)
- `templates/HANDOFF_FOLDER_TEMPLATE.md` 00_first-message spec: explicit
  synthesis confirmation phrases ("synthesis confirmed" / "synthesis
  correction: [text]"), Q&A loop instructions, single-vs-split prompt
  question, prompt generation protocol, continuous improvement reminder
- `protocols/ESSENTIALS.md` Continuous Improvement section: default project
  posture, applied-to-VISION guidance, frozen-state vs continuous-improvement
  Lifecycle wording examples

### Changed
- `VISION.md`: continuous improvement principle added to Vision section;
  Values section references ESSENTIALS Continuous Improvement section
- `docs/handoffs/2026-05-09-ai-council-audit-sync/02_VISION.md`: synced with
  continuous improvement update
- `docs/handoffs/2026-05-09-ai-council-audit-sync/00_README.md`: regenerated
  with v3.2 10-step operator workflow
- `docs/handoffs/2026-05-09-ai-council-audit-sync/00_first-message.md`:
  regenerated with v3.2 Q&A loop + operator response handling + prompt
  generation protocol + continuous improvement reminder
- `docs/handoffs/2026-05-09-ai-council-audit-sync/07_ACTION_PLAN.md`
  Directive 2 VISION Lifecycle: "Feature-complete v1. No planned major
  features" → "Active development with continuous improvement focus..."
- `docs/handoffs/2026-05-09-ai-council-audit-sync/01_manifest.json`:
  SHA-256 checksums recomputed for 4 modified files; format_version bumped
  to v3.2

### Lesson captured
- LESSONS.md: qa-loop-continuous-improvement-operator-clarity — 16th
  instance of design-without-empirical-contact pattern; continuous
  improvement elevated to ecosystem-wide value

---

## 2026-05-09 (late evening, part 3) — Handoff bundle review fixes

### Changed
- `VISION.md` frontmatter: added `tier: M` + `scale: M` per ADR-33 mandate;
  updated `last_reviewed: 2026-05-09`; lowercased `owner`. Lifecycle section
  documents architect-judgment basis (M chosen under F-08 calibration
  uncertainty; algorithm output L pending recalibration).
- `docs/handoffs/2026-05-09-ai-council-audit-sync/02_VISION.md`: synced to
  updated canonical VISION (now ADR-33 compliant frontmatter).
- `docs/handoffs/2026-05-09-ai-council-audit-sync/00_README.md`: file count
  corrected 11 → 12.
- `docs/handoffs/2026-05-09-ai-council-audit-sync/00_first-message.md`:
  reading order adds explicit note about `01_manifest.json` (machine-readable,
  skip during reading).
- `docs/handoffs/2026-05-09-ai-council-audit-sync/01_manifest.json`: SHA-256
  checksums recomputed for 8 modified files.

---

## 2026-05-09 (evening, part 2) — ai-council audit handoff Stage 3 complete

### Added
- `docs/handoffs/2026-05-09-ai-council-audit-sync/` — final 11-file flat
  handoff bundle for ai-council audit-sync. Generated via proper 3-stage
  v3.1 flow with semantic corrections (OLD/NEW chat distinction), audience
  split (Section A/PASTE_BOUNDARY/Section B), pre-created stage2-response,
  tolerant parser, and verification layer. Replaces deleted single-stage
  2026-04-30 version.
- `docs/handoffs/_archive/2026-05-09-ai-council-audit-sync/` — stage1-question.md
  + stage2-response.md archived for traceability.

### Changed
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/` → moved to
  `_archive/` (Stage 1 + Stage 2 inputs preserved).
- BACKLOG Cross-stream P1 "Phase 1 validation — audit + handoff dry-run on
  ai-council": marked done.
- JOURNAL 2026-05-09 Next section updated with Stage 3 completion notes.

### Verification finding
- config/settings.yaml actual uncommitted change: grok model string
  `"grok-4.20"` → `"grok-4.3"` + whitespace normalization. Architect
  believed change was Grok research timeout 120s → 300s — this is incorrect.
  Flagged in 06_STATE_OF_PLAY.md verification section.

---

## 2026-05-09 (evening) — Stage 1 question template context completeness

### Changed
- `templates/HANDOFF_QUESTION_TEMPLATE.md` Section B restructured: role
  definition + handoff bundle awareness + epistemic honesty requirement +
  format requirements now appear at TOP of Section B (before current state,
  audit context, and questions). Inline epistemic notes added per question.
  Generation rules updated to enforce Section B order.
- `protocols/HANDOFF_PROCESS.md` Stage 1 procedure: Section B structure
  documented (10-item order); rationale for top-placement explained
  (version with format at end produced plain-text headings, fabricated
  specifics, duplicated ecosystem info).
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`
  regenerated with corrected Section B structure.

### Added
- LESSONS.md: `stage2-context-completeness` — LLM-to-LLM prompts need
  role/bundle/epistemic/format at top before any content to be responded to.

---

## 2026-05-09 (late afternoon, part 2) — Stage 2 pre-create + markdown format

### Changed
- `protocols/HANDOFF_PROCESS.md` Stage 1 procedure: new step 9 pre-creates
  `stage2-response.md` placeholder template alongside `stage1-question.md` in
  the single Stage 1 commit. Stage 3 detection refined: checks for substantive
  content below `═══ REPLACE BELOW ═══` marker, not just file existence.
  Stage 2 section updated to reference pre-created file.
- `templates/HANDOFF_QUESTION_TEMPLATE.md` Section A step 5 updated to reference
  pre-created stage2-response.md. Section B end: added "Format requirements
  (CRITICAL)" block mandating pure markdown response from architect (no preamble,
  no code fence, exact heading format).
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`
  regenerated with updated Section A step 5 + format requirements in Section B.

### Added
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage2-response.md`
  — pre-created placeholder template with 5 headings, replacement marker, and
  Rob's instructions as HTML comment.
- LESSONS.md: `handoff-friction-precreate` — upstream stages pre-create
  downstream input files; operator fills content, never creates files.

---

## 2026-05-09 (late afternoon) — Handoff template audience split

### Changed
- `templates/HANDOFF_QUESTION_TEMPLATE.md` refactored with explicit two-section
  structure: Section A (Rob operational steps) / PASTE_BOUNDARY (thick `═` line) /
  Section B (architect-facing question block). Receiver synthesis prompt removed
  (wrong audience — old chat answers, it does not synthesize before responding).
- `templates/HANDOFF_FOLDER_TEMPLATE.md` 00_first-message.md content guidance
  expanded to include receiver synthesis prompt (correct audience: NEW chat
  receiving handoff bundle validates understanding before acting).
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`
  regenerated with corrected audience split and PASTE_BOUNDARY delimiter.
- `protocols/HANDOFF_PROCESS.md` Stage 1 generation spec updated: removed
  "Receiver synthesis prompt at end" bullet; added note that synthesis belongs
  in Stage 3 output (00_first-message.md).

### Added
- LESSONS.md: `handoff-audience-confusion` entry — visual delimiters required
  for multi-audience artifacts; list readers and responsibilities before structuring.

---

## 2026-05-09 (later afternoon) — Handoff v3.1 semantic correction

### Changed
- ADR-42 second amendment: Stage 2 source clarified as OLD browser chat (existing,
  being wrapped up), Stage 3 target clarified as NEW browser chat (fresh). Three-actor
  flow table added to amendment block.
- `protocols/HANDOFF_PROCESS.md`: 3-actor ASCII diagram added near top; Stage 2
  section rewritten to specify OLD chat source; Stage 1 + Stage 3 report steps
  updated with correct chat direction.
- `templates/HANDOFF_QUESTION_TEMPLATE.md`: Rob's instructions corrected (paste into
  OLD chat, not new); architect intro rewritten to address existing dying chat;
  closing instructions added (OLD chat closes after Stage 3, NEW chat opens).
- `templates/HANDOFF_FOLDER_TEMPLATE.md`: 00_README and 00_first-message content
  guidance acknowledges fresh chat receiver context.
- `protocols/SESSION_SETUP.md`: 3-actor table added; Stage 2 direction explicit (OLD
  chat); Stage 3 direction explicit (NEW chat).
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`:
  regenerated with corrected OLD chat instructions throughout.

### Added
- LESSONS.md: `handoff-semantic-misunderstanding` entry — protocol semantics matter
  as much as protocol mechanism; specify actor state (fresh/dying/persistent) before
  writing process steps.

---

## 2026-05-09 (afternoon) — Handoff v3.1: end-to-end implementation

### Changed
- ADR-42 amended: audit-sync Stage 2 shortcut removed; ALL handoffs follow
  full 3-stage flow regardless of type. Amendment block added to ADR header.
- `protocols/HANDOFF_PROCESS.md` rewritten to v3.1: operational state tracking
  via `_in_progress/{slug}/` directory, explicit trigger phrase table, per-stage
  validation checkpoints, JOURNAL hook (Stages 1+3), CHANGELOG hook (Stage 3),
  BACKLOG integration, drift detection reports both SHAs on mismatch.
- `protocols/SESSION_SETUP.md` handoff workflow trigger section updated to v3.1
  flow with state detection table.
- `templates/HANDOFF_QUESTION_TEMPLATE.md` adds filename conventions, Stage 2
  response format requirements, and operational instructions for Rob.
- `templates/HANDOFF_FOLDER_TEMPLATE.md` documents Stage 3 input source
  (`_in_progress/{slug}/`) and archive sibling pattern.

### Added
- `.claude/commands/handoff.md` — `/handoff` slash command implementing v3.1
  three-stage flow with critical constraints listed.
- `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`
  — first proper Stage 1 artifact for ai-council audit-sync, awaiting browser-2
  response (Stage 2).

### Removed
- `docs/handoffs/2026-04-30-ai-council-audit-sync/` — deleted because generated
  under now-removed audit-sync shortcut (Stage 2 skipped). To be regenerated via
  proper 3-stage flow after browser-2 response received.

---

## 2026-05-09 — Handoff Format v3.0 implementation

### Added
- ADR-42 Handoff Format v3.0 — three-stage flow (Stage 1 question generation,
  Stage 2 architect response, Stage 3 reconciliation + folder generation),
  flat 11-file structure with full VISION/PLAYBOOK/ESSENTIALS as invariants,
  standardized 5-question SBAR/I-PASS pipeline, SHA-256 drift mitigation,
  09_EXECUTION_EVIDENCE.md return trip
- `templates/HANDOFF_QUESTION_TEMPLATE.md` — Stage 1 output skeleton
- `templates/HANDOFF_FOLDER_TEMPLATE.md` — Stage 3 folder structure spec

### Changed
- `protocols/HANDOFF_PROCESS.md` rewritten to v3.0 (supersedes v2.0; ADR-32 §4 deprecated)
- `protocols/SESSION_SETUP.md` — added handoff workflow trigger + BACKLOG review sections
- `docs/handoffs/2026-04-30-ai-council-audit-sync/` regenerated using v3.0
  (replaces broken v2.0 nested structure; 13 files → 12 flat files)

### Deprecated
- ADR-32 §4 "Pending — next session candidates" — superseded by BACKLOG.md
  (per ADR-41) referenced from handoff Future State (07_ACTION_PLAN.md)

---

## 2026-04-30 — Phase 1 alignment fixes (self-audit Tier 1+2+3 batch)

**Changed:**
- Phase 1 alignment fixes (Tier 1+2+3): stale text in VISION/PLAYBOOK/CONTRIBUTING; missing ADR references in README/CLAUDE/VISION/ENVIRONMENT; ADR-39 ARCHITECTURE.md registry entry correction (Tach taxonomy conflation)
- JOURNAL.md 2026-04-30 entry: addendum for afternoon post-ratification work (ai-council audit, self-audit, alignment fixes)
- LESSONS.md: appended "prescriptive writing without verification" pattern (recurring methodology debt, 3 instances in single session)

---

## 2026-04-30 — ADR-41 cross-session backlog architecture + initial BACKLOG.md seed

**Added:**
- ADR-41 Cross-Session Backlog Architecture (BACKLOG.md mandate at M+ tier, no Scrum vocabulary, split-brain prevention)
- BACKLOG.md initial seed with Stream C items

---

## 2026-04-30 — ADR-40 scale tier evaluation + ADR-39 file lifecycle governance + ADR-38 universal repo architecture baseline + ADR-37 session boundary protocol + ADR-36 audit tool architecture

**Added:**
- ADR-40 Scale Tier Evaluation Algorithm (logarithmic Maintainability Index pattern, 3 signals, transition procedures)
- ADR-39 File Lifecycle Governance (universal 6-element pattern + registry of existing files)
- ADR-36 Audit Tool Architecture (.dev-knowledge as ecosystem auditor, 4-phase implementation)
- ADR-38 Universal Repo Architecture Baseline (foundation for ADR-39/40/41)
- ADR-37 Session Boundary Protocol (two-phase handoff: current state + future state overlay)

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

Source: Council debates Topics 1 and 2 (`docs/decisions/transcripts/archive/legacy/DECISION_28_authority_model.md`, `docs/decisions/transcripts/archive/legacy/DECISION_29_handoff_synergy.md`).

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
