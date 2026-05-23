# .dev-knowledge BACKLOG

Cross-session pending items across active streams. See ADR-41 for
schema and grooming cadence.

Last full grooming: 2026-05-09 (P1 HANDOFF_PROCESS closed)
Next quarterly grooming: 2026-07-01

---

## Stream A: corp-monorepo

(no items currently — populate as Phase 2 universalization begins)

## Stream B: ai-council

### [P2] [closed] ai-council needs AGENTS.md (PLAYBOOK governance gap)
- **What:** PLAYBOOK section "AGENTS.md — canonical per-repo governance contract" requires each repo to have AGENTS.md at root. `ai-council` has `CLAUDE.md` but no `AGENTS.md` (verified 2026-05-11). Drift signal: cross-tool LLM agents (Codex, Cursor, Aider) operating on outdated/incomplete repo context.
- **Why:** AGENTS.md is the cross-tool canonical governance file per Council #28 (community standard). CLAUDE.md alone is Claude-Code-specific. Missing AGENTS.md = drift from ecosystem standard set by PLAYBOOK.
- **Vision ref:** VISION.md "Methodology Author" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Item 0 strażnik audit)
- **Closed:** 2026-05-18 — AGENTS.md exists in ai-council repo (last updated 2026-05-17); item superseded. Currency review carried as Directive #1 of 2026-05-18-ai-council-session-sync handoff.

### [P3] [open] ai-council LESSONS.md scope-tag backfill (ADR-46 advisory)
- **What:** ai-council `LESSONS.md` entries do not contain `[scope: X]` tags per the ADR-46 LESSONS payload sniff test. Add `[scope: X]` to each entry's canonical 6-field schema position. Work belongs in ai-council repo.
- **Why:** ADR-46 §LESSONS.md specifies `[scope: X]` substring as required in 6-field entries; absence produces a WARN on `dated_entries_lessons` check. Advisory — WARN not FAIL — but constitutes methodology drift from the ADR-46 standard.
- **Added:** 2026-05-16 by rob (2026-05-16 re-audit advisory WARN — ai-council `dated_entries_lessons`)
- **Status:** open — work belongs in ai-council repo

## Stream C: .dev-knowledge governance

### [P2] [open] .dev-knowledge ADR-38 self-compliance gap — src/ + pyproject.toml
- **What:** Audit tool P1 self-audit surfaced finding: `.dev-knowledge` missing `src/` and `pyproject.toml` (ADR-38 check `adr38_baseline` FAIL). `.dev-knowledge` is a governance/knowledge repo (NOT a code project per CLAUDE.md), yet ADR-38 mandates src/ and pyproject.toml for all tier M+ repos. Resolution options: (a) create minimal pyproject.toml + scripts/ → src/ migration, (b) amend ADR-38 to add "governance-only" tier exemption, (c) document explicit exception in state.yaml.
- **Why:** Self-audit produces FAIL on the repo that runs it — creates awkward "auditor fails its own checks" state. Resolving clarifies whether ADR-38 universal mandate applies to non-code repos.
- **Vision ref:** VISION.md "Auditor" + ADR-38 universal architecture
- **Added:** 2026-05-15 by rob (surfaced by audit tool P1 self-audit)
- **Status:** open

### [P2] [open] Lessons activation P1 implementation
- **What:** Build lessons-index.json + retrieval (SessionStart hook) + querying (CLI) per ADR-35
- **Why:** Activates LESSONS.md from passive archive to active feedback loop; bidirectional pipeline corrections.jsonl ↔ LESSONS.md ↔ ~/.claude/rules/
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P2] [open] ESSENTIALS.md cheat-sheet additions for ADRs 35-54
- **What:** Review which of ADRs 35-54 warrant high-leverage cheat-sheet rules in ESSENTIALS.md. Candidates: lessons retrieval shortcut (ADR-35), audit tool trigger conditions (ADR-36), two-phase handoff quick reference (ADR-37), tier evaluation signals (ADR-40), BACKLOG grooming cadence rules (ADR-41), ARCHITECTURE.md convention (ADR-51), CLAUDE.md single-instruction model (ADR-53), Codex reviewer global standard (ADR-54). Apply ESSENTIALS.md "Keep under 1 page" constraint — judgment call which warrant inclusion.
- **Why:** ESSENTIALS lifecycle update trigger is "lessons promotion, methodology change." Significant methodology changes accumulated 2026-04-30 through 2026-05-19. Audit observed 226 lines (already over "1 page") so additions require pruning OR explicit relaxation of constraint. Verification 2026-05-20: grep confirms only ADR-53 directly referenced in topical content; ADRs 35-52 and 54 absent.
- **Added:** 2026-04-30 by rob (Phase 1 self-audit); scope expanded 2026-05-20 (posture audit verification, `docs/audits/2026-05-20-posture-audit-verification.md` finding C2).
- **Status:** open

### [P2] [superseded] ADR-29 amendment — formalize "prepend at top" ordering convention for LESSONS.md
- **What:** Amend ADR-29 (or create new ADR superseding ADR-29's position-rule clause) to formalize the going-forward convention: new LESSONS entries prepend at top of dated-entries section, not append at tail. Update any related references in PLAYBOOK / ESSENTIALS / CLAUDE.md that mention LESSONS append direction.
- **Why:** Operator visibility — newest entries should be immediately visible on file open so operator can confirm captures landed. Same-day correction (2026-05-14 session) moved 9 entries to top as one-time fix; going-forward convention needs formalization so future contributors don't tail-append out of habit, creating mixed ordering.
- **Captured here, not fixed here.** Per scope discipline — same-day file correction is one concern, ADR amendment is methodology change deserving its own thought (full Stage 1→3 cycle if needed).
- **Vision ref:** ADR-29 (lessons grandfathering schema, current authority on LESSONS convention).
- **Added:** 2026-05-14 by rob (interleaved scope, same-day correction session).
- **Status:** superseded 2026-05-15 by ADR-46 (cross-repo dated-entries format standard). Prepend-latest is now universal mandate across LESSONS / JOURNAL / CHANGELOG; downstream cross-file references (PLAYBOOK / ESSENTIALS / CLAUDE.md) folded into Session D cleanup pass scope.

### [P2] [open] Audit tool: check_backlog_organization code-span-aware done-token regex
- **What:** `check_backlog_organization` uses a bare regex to detect done-status tokens in `BACKLOG.md`. This regex matches the done-token pattern inside backtick inline-code spans in body text, producing false-positive FAIL findings on entries that reference the ADR-47 vocabulary. Fix: strip or skip backtick-quoted spans before applying the done-token check, so only unquoted status tokens trigger the fatal finding.
- **Why:** Session D encountered 3 false-positive hits (body text references to the done-status concept in backtick spans), requiring rewordings that lost precision. A code-span-aware regex is the correct fix; body-text rewordings are a workaround that degrades entry fidelity. Surfaced as a pattern likely to recur in future BACKLOG entries that explain the ADR-47 two-file state.
- **Vision ref:** VISION.md "Auditor" function; ADR-47 enforcement; ADR-36 audit tool architecture
- **Added:** 2026-05-16 by rob (Session D false-positive hit pattern)
- **Status:** open

### [P2] [open] Stream taxonomy grooming — Cross-stream section exceeds kill criterion
- **What:** BACKLOG.md `Cross-stream / Ecosystem` section currently holds 40% of all open items (kill criterion per ADR-47: 33%). Review the 15 open Cross-stream items and evaluate: (a) which items genuinely belong to an existing stream (A/B/C/D) and should be reclassified; (b) whether a new stream (e.g., Stream E: ecosystem operations or Stream E: tooling) should be created to absorb a coherent sub-group; (c) which items are truly cross-stream and should remain. Output: reclassified BACKLOG with Cross-stream ≤33%, or an operator decision to extend ADR-47's kill threshold with empirical justification.
- **Why:** ADR-47 codified 33% as the kill criterion because Cross-stream > 33% signals that the stream taxonomy is no longer routing items correctly. The current 40% reading persisted after extraction of all done items, confirming it is structural (not noise). Without deliberate grooming, the ratio will increase as new cross-stream items accumulate and the taxonomy's routing signal degrades for LLM agents at session start.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ADR-47 kill criteria; pairs with quarterly grooming cadence
- **Added:** 2026-05-16 by rob (Session D — accepted WARN from kill-criterion re-evaluation post-extraction)
- **Status:** open — deferred to quarterly grooming (2026-07-01); task-mismatch justifies defer over immediate forced reclassification

### [P3] [superseded] Council CLI dual-write trigger logic
- **What:** Define when Council debates dual-write to .dev-knowledge vs ai-council/output only; flag-based or auto-detect (research+pick=curated, test=no-curated)
- **Why:** Test debates currently pollute curated transcripts; surfaced 2026-04-30 session
- **Added:** 2026-04-30 by rob
- **Status:** superseded 2026-05-11 by Cross-stream P1 "AI Council cross-project transcript routing" (broader scope addressing root cause; mechanism choice deferred to Council debate)

### [P3] [open] ADR-39 amendment — BACKLOG.md lifecycle entry
- **What:** Amend ADR-39 registry to add BACKLOG.md entry per ADR-41
- **Why:** Lifecycle compliance per ADR-39; deferred to grouped amendment to minimize ADR churn
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P3] [open] ADR-41 amendment — reference ADR-47 (BACKLOG schema)
- **What:** Amend ADR-41 (BACKLOG architecture — file mandate) to cross-reference ADR-47 (BACKLOG schema decision). ADR-41 stands as the "file mandate" authority; ADR-47 is the "file schema" authority. Small textual amendment in ADR-41 § Storage + Related metadata block.
- **Why:** ADR-47's Follow-ups identifies this as needed for traceability. Without the cross-reference, future readers may treat ADR-41 as the only BACKLOG authority and miss the operational schema in ADR-47.
- **Vision ref:** ADR-41 + ADR-47.
- **Added:** 2026-05-15 by rob (B+C ADR session — surfaced by ADR-47 Follow-ups)
- **Status:** open — bundle with grouped ADR-39 amendments to minimize ADR churn (Stream C P3 above)

### [P3] [open] ADR-39 registry decision — 5 unregistered template files
- **What:** Decide whether `templates/AGENTS-md-template.md`, `templates/CLAUDE-md-template.md`, `templates/codex-review-config-template.md`, `templates/prompt-template.md`, plus any other template-category files require ADR-39 registry entries. Options: (a) add registry entries with template-specific lifecycle; (b) formally exclude templates as a class via ADR-39 amendment ("template files exempt from registry"); (c) hybrid — register only stable templates, exclude transient. Decision required because ADR-39 says "every file in .dev-knowledge MUST have 6 lifecycle elements."
- **Why:** Audit surfaced unregistered files. Either we extend registry or formally narrow scope. Drift risk if neither.
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
- **Status:** open

### [P3] [open] LESSONS.md parenthetical-qualifier entries escape dated-entry audit regex
- **What:** 8 entries use `### YYYY-MM-DD (qualifier) |` format (all 2026-05-09 with time qualifiers). The audit's `_LESSONS_H3_RE` regex requires date immediately before `|`; the parenthetical causes these entries to be invisible to the ordering check. They are correctly positioned (reorder script treated them as opaque), but the validator cannot enforce their ordering going forward. Decision: (a) broaden regex to permit optional parenthetical, or (b) reformat the 8 entries to move qualifier into body text (requires operator sign-off under ADR-29 "never edit old entries" — qualifier is metadata, not lesson content).
- **Why:** Latent coverage gap: future misordering around these 8 entries would not be caught. Surfaced by Session D content-preservation count (127 H3 total, 120 regex-matched; delta of 8 = parenthetical entries).
- **Added:** 2026-05-16 by rob (Session D content-preservation verification)
- **Status:** open — operator decision required (regex broadening vs entry reformat) before fix

### [P2] [open] scripts/backlog_extract.py references deleted BACKLOG_ARCHIVE.md
- **What:** `scripts/backlog_extract.py` writes done/abandoned BACKLOG entries to `BACKLOG_ARCHIVE.md` (docstring line 2; code lines 22, 64). `BACKLOG_ARCHIVE.md` was deleted on 2026-05-16 per CLAUDE.md §5 ("Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md` — deleted 2026-05-16"). Running the script today would either no-op (no archive to write to) or recreate a file governance forbids. Decide: (a) retire the script entirely (the archive was a deliberate removal), (b) repurpose it (e.g., archive to JOURNAL `Changes:` line or just delete the done entries in place), (c) leave dormant if there's a future scenario that resurrects the archive concept.
- **Why:** Live script drift against current governance. Either the script is broken (silently) or it would actively re-introduce a deleted file. Confirm + act.
- **Refs:** `scripts/backlog_extract.py`; CLAUDE.md §5; `docs/audits/2026-05-20-posture-audit-verification.md` finding X1.
- **Added:** 2026-05-20 by rob (posture audit verification — bonus drift surfaced beyond witness-based audit).
- **Status:** open

### [P3] [open] scripts/migrate_links.py SKIP_NAMES references deleted CHANGELOG.md
- **What:** `scripts/migrate_links.py` line 4: `SKIP_NAMES = {'CHANGELOG.md', 'JOURNAL.md', 'LESSONS.md', 'TOKEN-LOG.md'}`. `CHANGELOG.md` was deleted 2026-05-16 per CLAUDE.md §5. The skip-set protects a phantom file. Remove `CHANGELOG.md` from SKIP_NAMES.
- **Why:** Cosmetic drift; no functional harm but a hard-coded reference to a deleted canonical file. Low-cost touch.
- **Refs:** `scripts/migrate_links.py:4`; CLAUDE.md §5; `docs/audits/2026-05-20-posture-audit-verification.md` finding X2.
- **Added:** 2026-05-20 by rob (posture audit verification — bonus drift).
- **Status:** open

### [P2] [open] docs/decisions/README.md ADR Index missing ADRs 45-50 and 54
- **What:** `docs/decisions/README.md` carries the canonical ADR index table. Verification 2026-05-20 confirmed the table lists ADR-27 through ADR-44 (44 marked "Reserved"), then jumps to ADR-51 through ADR-53. **Missing from index:** ADR-45 (handoff architecture v4), ADR-46 (cross-repo dated-entries format), ADR-47 (cross-repo BACKLOG.md organization), ADR-48 (trim documentation governance), ADR-49 (consolidate past-recording files), ADR-50 (machine-document encoding), ADR-54 (Codex reviewer global standard). Additionally `ARCHITECTURE.md` "Governing ADRs" section lists ADRs 27-53 but is missing ADR-54.
- **Why:** Index is the primary discoverability surface for ADRs. 7 missing entries materially degrades navigability for new contributors and for re-orientation after time away. Low-cost to fix (one table extension + one ARCHITECTURE.md list extension). Related to broader I1 (ADR relationship map / supersession graph).
- **Refs:** `docs/decisions/README.md`; `ARCHITECTURE.md` § Governing ADRs; `docs/audits/2026-05-20-posture-audit-verification.md` finding X3.
- **Added:** 2026-05-20 by rob (posture audit verification — bonus drift).
- **Status:** open

### [P3] [open] ADR relationship index / supersession graph
- **What:** With 27+ ADRs accumulated (gaps at 44 reserved; supersessions like ADR-52 → ADR-53 in flight), the relationship structure — supersedes / supersededBy / related / amends — is not navigable for a fresh reader. Build either (a) a machine-generated graph from ADR frontmatter (`supersedes:`, `related:`, `amends:` fields already exist in newer ADRs), or (b) an index doc with explicit edges. Could be DOT, Mermaid, or markdown table. Same shape as codemap generator work — read frontmatter, render, CI-check freshness.
- **Why:** New contributors reading ADRs in sequence miss relationship structure. As corpus grows past 30 ADRs, the cost of unfamiliarity compounds. Pairs with F1 (contradiction detection — both need ADR/decision graph as substrate).
- **Refs:** `docs/decisions/`; `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` finding I1.
- **Added:** 2026-05-20 by rob (posture audit verification).
- **Status:** open

### [P2] [closed] Codemap generator output specification (ADR-51 open item)
- **What:** ADR-51 §5 mandates an auto-generated, CI-freshness-checked codemap for every M/L `ARCHITECTURE.md`, but the generator's output specification is undecided: directory tree vs package dependency graph vs CLI/module inventory vs hybrid. Under-generation fails re-orientation; over-generation produces noise. Two artifacts pending: (a) the generator tool itself (resides in `.dev-knowledge`, consumed by child repos per ADR-36 shared-tooling pattern), (b) the CI freshness-check hook that consumes its output and fails on diff. Until both exist, `templates/ARCHITECTURE-template.md` instructs authors to hand-maintain the codemap in the interim package-tree-with-layer-annotation format documented inline; the template's `<!-- CODEMAP:START/END -->` machine region is reserved for the future generator's insertion point.
- **Why:** ADR-51 mandatory minimum (Decision 4) requires a codemap; the convention is **load-bearing** on the generator existing — no M/L repo can satisfy the convention as written until the generator and CI check ship. Resolving the output spec is the first blocker; the tool and CI follow.
- **Vision ref:** VISION.md "Methodology Author" + "Auditor" functions; ADR-51 open questions; ADR-36 shared tooling
- **Refs:** `docs/decisions/ADR-51-architecture-doc-convention.md` (open questions section); `templates/ARCHITECTURE-template.md` §2 (interim format + CODEMAP machine region); `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` (corp-monorepo's all-hand-written precedent)
- **Added:** 2026-05-19 by rob (Directive 1b — template authoring; output spec deliberately deferred per Directive instructions)
- **Closed:** 2026-05-23 — Generator built in Prompt 1 (branch feat/codemap-generator-tool, 6 commits, merged b2296ff). Convention landed in Prompt 2 (branch feat/codemap-amendment-and-dogfood): ADR-51 amendment 2026-05-22 (commit 9cb5aef), template update (09ba1ad), PLAYBOOK § Codemap workflow (392d0c9), pre-commit hook (ed28304), dogfood on .dev-knowledge ARCHITECTURE.md (b439cbd). End-to-end pipeline validated. Cross-repo rollout (corp-monorepo, ai-council) is future-session work.

## Stream D: corp-sca-time-automation

(no items currently — trigger-based migration per ADR-33)

## Cross-stream / Ecosystem

### [P2] [open] Phase 2 universalization rollout
- **What:** Apply ADR-33/34/35/37/38/39/40/41 to ai-council and corp-monorepo (immediate cohort per ADR-33)
- **Why:** Validates universalization pattern; unblocks trigger-based cohort migration; first per-repo audit + handoff cycle
- **Vision ref:** VISION.md "Disseminator" function
- **Added:** 2026-04-30 by rob
- **Status:** open — ai-council substantially complete as of 2026-05-12 session: ADR-34 hyphen compliance achieved (CLI emitter + docs), ADR-38 Scale M gaps closed (BACKLOG.md, LESSONS.md at root, tasks/ retired), VISION.md tier M declared, scrum-master review cycle N=1 completed. .dev-knowledge AGENTS.md retired 2026-05-19 (Chunk 4 — content migrated to CLAUDE.md v2.1 per ADR-53). Remaining ai-council: ARCHITECTURE.md (optional at M). ai-council AGENTS.md retired 2026-05-19 per ADR-53 chunk 4. corp-monorepo: not yet started.

### [P2] [open] VISION.md tier declarations across ecosystem
- **What:** Update VISION.md frontmatter `tier:` field across all repos per ADR-40 calibration baseline (corp-ops=S, ai-council=M, corp-monorepo=L, etc.)
- **Why:** Operationalizes ADR-40 algorithm; declared tier vs computed tier comparison enables audit findings
- **Added:** 2026-04-30 by rob
- **Status:** open — ai-council tier M declared in VISION.md frontmatter (2026-05-12 session). Other repos: pending.
- **Status update 2026-05-23:** Tier declarations CONFIRMED for the 3 registered repos — `.dev-knowledge` (M), `ai-council` (M), `corp-monorepo` (L) — verified via 2026-05-23 ecosystem audit (all three VISION.md frontmatters include `'tier'` key; report `docs/audits/2026-05-23-ecosystem-audit.md`). Other ecosystem repos (corp-ops, corp-sca-time-automation, corp-knowledge-extractor, corp-by-os, corp-rfp-agent) NOT verified — pending discovery + verification (cross-ref P3 entry "Undiscovered repos confirmation"). Entry status: OPEN (partial completion).

### [P2] [open] Council research — relative repo complexity evaluation in solo dev / LLM workflows
- **What:** Council research debate. Question: how do professionals evaluate repo complexity at relative scale (small/medium/large) in solo dev and LLM-driven workflows? Current ADR-40 algorithm (logarithmic Maintainability Index pattern) may embed enterprise-scale assumptions inappropriate for 1-person ecosystem. Surface industry practice — surveys, blog posts, indie hacker conventions, monorepo tools' tier definitions for personal vs team scale. Plus philosophical framing: at what point does a small project become medium, medium become large, when complexity grows logarithmically? Output informs ADR-40 amendment alongside audit tool P1 multi-repo data collection.
- **Why:** All ecosystem repos currently classify L per ADR-40 (calibration concern surfaced 2026-04-30 ai-council audit, finding F-08). Research before amendment ensures evidence-based decision rather than gut-feel coefficient adjustment. Dependency: pair with audit tool P1 multi-repo data; both inform ADR-40 amendment.
- **Vision ref:** VISION.md "Methodology Author" + "Auditor" functions
- **Added:** 2026-04-30 by rob (ai-council audit Faza A2 closure)
- **Status:** open

### [P2] [open] Handoff advisory framing leaks into receiver behavior
- **What:** Session-start handoff containing architect's "REST recommended" advisory (2026-05-09-dev-knowledge-session-sync bundle) propagated to receiver chat as 3 unprompted session-end suggestions during 2026-05-11 session, despite explicit operator preference rule against unprompted scheduling. Handoff content framing shapes receiver behavior more strongly than receiver-side preference rules counteract.
- **Why:** ADR-37 session boundary protocol assumes handoff content is informational; in practice, advisory framing (rest, defer, urgency, complexity recommendations) becomes behavioral pressure on receiver. Pattern likely repeats with other advisory framings. Worth classifying root cause (handoff design vs receiver discipline vs both) before next high-stakes handoff.
- **Vision ref:** VISION.md "Methodology Author" function — handoff design is methodology
- **Added:** 2026-05-11 by rob (empirical finding from session)
- **Status:** open — classify root cause, propose mitigation
- **Related:** ADR-37, ADR-42, LESSONS 2026-05-11 entries

### [P3] [open] Cross-repo audit (Phase 3)
- **What:** Audit tool runs across all repos with VISION.md, generates ecosystem compliance report; verifies adoption of ratified ADRs
- **Why:** Validates universalization actually adopted (not just ratified); drift detection over time
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P1] [open] Council decisions management consolidation
- **What:** Council debates produce architectural decisions (ADRs), but decision artifacts are dispersed across `docs/decisions/`, `docs/decisions/transcripts/`, and ADR references in individual files. Need: (a) consolidated index of all decisions with traceability from decision to implementation, (b) explicit mechanism to detect contradictions between decisions over time, (c) clear ownership model for decision evolution (amendment vs. new ADR vs. conversational clarification). Scope: audit current dispersion, design consolidation pattern, implement index.
- **Why:** Dispersion observed during 2026-05-09 session work. As ADR count grows (42+), navigating, cross-referencing, and detecting drift becomes harder. Governance debt compounds silently.
- **Vision ref:** VISION.md "Knowledge Guardian" + "Methodology Author" functions
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open — Item 0 (2026-05-11) closed first-step inventory: `docs/decisions/README.md` rewritten with full ADR index 27-42 + transcript convention + ADR↔transcript traceability. Remaining sub-items: (1) contradiction detection mechanism (Council debate territory), (2) ownership model for decision evolution — amendment vs new ADR vs conversational clarification (Council debate territory). "Consolidated index" sub-item closed.

### [P1] [open] Sacred-files maintenance enforcement
- **What:** Canonical files in every ecosystem repo drift out of date because browser chats forget to update them at session boundaries. Original list (2026-05-09) was 9 files: ARCHITECTURE, BACKLOG, CHANGELOG, CLAUDE, CONTRIBUTING, JOURNAL, LESSONS, README, VISION. **2026-05-20 verification:** CHANGELOG was deleted from `.dev-knowledge` on 2026-05-16 per CLAUDE.md §5 and must not be recreated; updated list for `.dev-knowledge` is 8 files (drop CHANGELOG). Child repos may retain CHANGELOG. Need enforcement mechanism — candidates: pre-commit hook checking `last_reviewed` staleness, session-end checklist skill, CI check for file age, or automated diff-based staleness detection. Scope: enumerate per-repo lists (the 8/9 split is repo-dependent), design enforcement pattern, implement at least one mechanism, validate against known drift scenarios.
- **Why:** Methodology debt pattern surfaced repeatedly across 2026-05-09 session (LESSONS captures multiple instances of "prescriptive writing without empirical contact"). Sacred files are the ground truth — stale ground truth silently misleads future sessions and chats. Self-referential drift confirmed 2026-05-20: the sacred-files list itself was stale (listed deleted CHANGELOG).
- **Vision ref:** VISION.md "Knowledge Guardian" function; ESSENTIALS "Continuous Improvement" section
- **Added:** 2026-05-09 by rob (session wrap-up observation); cross-referenced 2026-05-20 (posture audit verification, finding C1).
- **Status:** open

### [P2] [open] Hooks audit + consolidation
- **What:** Two `review` hooks observed in ecosystem (one for Codex, one for internal review). Full hook inventory not documented. Need: (a) list all hooks across `.claude/` (global) and `.claude/` (project-level), (b) document each hook's purpose and trigger condition, (c) evaluate whether review hooks are intentionally separate or candidates for consolidation, (d) identify gaps (hooks that should exist but don't). Output: documented hook inventory + consolidation recommendation.
- **Why:** Undocumented hooks create confusion about what fires when. Two review hooks with overlapping purposes may produce redundant or conflicting signals.
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Skills universalization across repos
- **What:** Each repo has `.claude/skills/` (or equivalent) with skill definitions. Need cross-repo review: (a) inventory all skills across ecosystem repos, (b) classify each as repo-specific vs. cross-ecosystem candidate, (c) identify universalization targets — skills that should live in `.dev-knowledge` and be referenced/shared, (d) propose canonical location for universal skills. Output: skills inventory + universalization proposal.
- **Why:** Skills defined redundantly across repos create drift — same skill evolves differently in each context. Universalization reduces maintenance burden and ensures cross-repo consistency (per VISION Strategic emphasis: "Cross-repo methodology consistency").
- **Vision ref:** VISION.md Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Ecosystem standards audit against major repo
- **What:** Audit one significant ecosystem repo against current standards: folder naming (ADR-34), file naming (ADR-34), workspace structure (ADR-38), sacred-files presence (per set above), scope tag compliance (ADR-27). Surface drift items, classify by severity, plan remediation. Establish this as a repeatable pattern for auditing future repos.
- **Why:** Phase 2 universalization rollout (Cross-stream P2, above) needs a concrete audit run to validate the pattern works. Without an actual audit against a real repo, the process is theoretical.
- **Vision ref:** VISION.md "Auditor" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Note:** Do not name specific repo in BACKLOG until audit scoping session decides target. See "Phase 2 universalization rollout" for cohort selection.
- **Status:** open

### [P3] [open] Kimi K2 model integration evaluation
- **What:** Evaluate Kimi K2 as addition to ecosystem LLM stack. Scope: (a) capability evaluation for Council debate quality, code generation, and reasoning depth, (b) cost comparison vs. Claude on equivalent task types, (c) integration patterns with existing infrastructure. Decision artifact: Council debate output recommending adoption level — research-only / production peer / experimental supplement.
- **Why:** Significantly lower cost than Claude on equivalent tasks (per Rob). Speed of LLM technology adoption is a competitive advantage (VISION Strategic emphasis: "Velocity in LLM technology adoption"). Evaluation before adoption; Council debate before production use.
- **Vision ref:** VISION.md Strategic emphasis "Velocity in LLM technology adoption"
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P3] [open] Scale tier evaluation re-evaluation
- **What:** Current scale tier system (S/M/L per ADR-40) has documented calibration concern (F-08: all repos classify L under current coefficients). Decision point: (a) formalize via tighter metrics with empirical calibration data, or (b) deprioritize — remove scale tiers as a primary governance signal. Decision artifact: Council debate. Dependency: pairs with "Council research — relative repo complexity" (Cross-stream P2, above) and audit tool P1 multi-repo data collection (Stream C P1).
- **Why:** Subjective tier assignment reduces auditability and creates inconsistent governance. Either make it rigorous or explicitly drop it — the middle ground of "declared but uncalibrated" is methodology debt.
- **Vision ref:** VISION.md "Auditor" function; ADR-40 Lifecycle section
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P3] [open] Large repo migration preparation
- **What:** One significant ecosystem repo requires structural migration aligned with current standards (folder structure naming conventions, sacred-files compliance, scope tagging, ADR adoption). Significant scope — requires dedicated planning session with Council-debate-level design before execution. Scope: design migration plan, estimate effort, sequence against other BACKLOG items.
- **Why:** Migration will be disruptive if unplanned. Early planning (before audit tool P1 is complete) enables correct sequencing. Capture intent now to avoid ad-hoc migration later.
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Note:** Specific repo not named until planning session scopes it. Do not begin migration without Council-debate-level planning.
- **Status:** open

### [P3] [open] VS Code productivity maximization
- **What:** Longer-term initiative to maximize Claude Code + git workflow productivity via VS Code tooling. Scope: extensions audit (what's installed vs. what's optimal), workflow templates, integration with ecosystem tools (validators, pre-commit hooks, git workflows). Output: extensions + settings recommendation + any automation improvements.
- **Why:** Low-friction tooling reduces cognitive overhead during sessions. Deferred until higher-priority methodology items closed.
- **Vision ref:** VISION.md "Methodology Author" function (tooling as methodology support)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Codify scrum-master review authority pattern
- **What:** First empirical instance of scrum-master review pattern completed 2026-05-12 (Prompt L, ai-council review). Pattern: `.dev-knowledge` strażnik produces structured review report (read-only, no writes) identifying governance / documentation / dead code / filename compliance issues in child repo → operator routes report → child-repo architect implements. Candidate codification: new ADR-44 or amendment to ADR-26 (ecosystem strażnik role definition). Awaits N=2 empirical grounding before ADR-level codification per session pattern.
- **Why:** Pattern emerged organically as first cross-repo scrum-master review; needs codification to be repeatable and delegatable. Without ADR, subsequent reviews have no formal authority reference.
- **Vision ref:** VISION.md "Auditor" function + "Methodology Author" function
- **Added:** 2026-05-12 by rob (Prompt L)
- **Status:** open — N=1 (ai-council 2026-05-12); codification awaits N=2

### [P3] [open] PLAYBOOK codifications from 2026-05-19 posture audit
- **What:** The posture audit (H3, H4, T1, T2) and verification surfaced four candidate PLAYBOOK additions, each with N≥2 grounding:
  1. **Governance docs phrased as stable end-state.** Transient status ("to be retired in a follow-up chunk", "not yet started") lives in JOURNAL or a rollout-tracker, not in ADRs / PLAYBOOK / ESSENTIALS. Evidence: three instances this session arc (audit H3).
  2. **Verify destination before drop.** When relocating or dropping content, Plan Mode confirms destination genuinely covers it. Evidence: chunk B + chunk B-prime this session arc (audit H4).
  3. **No-delete exception for canonical-source duplicates.** "Never delete content without asking" (Core Invariant #3) does not apply when the deletion targets a duplicate of canonical content preserved elsewhere; the deletion *eliminates* a drift pair. Evidence: vault-writer pointer deletion + corp-monorepo AGENTS.md deletion (audit T1).
  4. **ADR-with-N=1 valid for singular choices.** N≥2 grounding prevents PATTERN extraction without evidence; a singular architectural CHOICE with no prior precedent can be an ADR-with-N=1 because the choice itself is the record. Evidence: ADR-54 (Codex config placement) (audit T2).
- **Why:** Each codification prevents an already-observed failure mode from recurring. Bundling into one focused PLAYBOOK update minimizes ADR churn.
- **Refs:** `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` (findings H3, H4, T1, T2); `docs/audits/2026-05-20-posture-audit-verification.md`.
- **Vision ref:** VISION.md "Methodology Author" function.
- **Added:** 2026-05-20 by rob (posture audit triage).
- **Status:** open

### [P3] [open] Apply scrum-master review pattern to other child repos
- **What:** Extend scrum-master review cycle (post-codification) to remaining ecosystem repos. Priority order: (1) corp-monorepo (Scale L; deeper audit warranted — most complex, most governance drift risk); (2) corp-knowledge-extractor / corp-by-os / corp-rfp-agent (verify existence on disk first); (3) corp-ops + corp-sca (Scale S; lighter touch).
- **Why:** Phase 3 of ecosystem universalization. Each repo reviewed = one point of drift caught before it compounds. Pattern validated on ai-council; broader rollout follows codification.
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-05-12 by rob (Prompt L)
- **Status:** open — blocked on codification (Cross-stream P2 above) + N=2 empirical grounding

## Cross-repo Naming + Architecture Migration (Prompt H audit + Prompt J ratification)

> Items below were surfaced by 2026-05-11 cross-repo pattern audit (Prompt H)
> and ratified/reclassified by Council + operator decisions (Prompt J).
> Framing corrected: was "fix-violator" tasks; now correctly sequenced as
> "ADR amended → then migrate" per Prompt I Implication finding.

### [P2] [open] Handoff folder format adoption (corp-monorepo)
- **What:** ADR-42 folder format is current standard. `corp-monorepo` still has flat `docs/HANDOFF.md` (pre-ADR-42 pattern). Migration options: convert existing flat file to folder format at next handoff event, or explicitly deprecate. Tied to A4 decision (separate ADR or conversational) about whether flat file is still acceptable as legacy.
- **Why:** ADR-42 folder format is the current standard; flat `docs/HANDOFF.md` files represent pre-ADR-42 state. Without migration or explicit deprecation, the repo appears non-compliant and future sessions have ambiguous precedent about which format is active.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A4)
- **Status:** open — ai-council resolved: `docs/HANDOFF.md` confirmed absent at HEAD `1bcc6ab` (Stage 3 verification 2026-05-17). corp-monorepo: open; A4 separate decision needed before prescribing migration.

### [P3] [open] UPPERCASE TYPE tag in legacy archive filenames (A5 — retire opportunistically)
- **What:** `corp-monorepo` and `corp-sca` use `YYYY-MM-DD_TYPE_topic.md` pattern in `docs/archive/` files (e.g. `CODE_REVIEW_REPORT`). Not in ADR-34 spec. Pre-ADR-34 legacy pattern.
- **Why:** Pre-ADR-34 pattern is outside the current naming spec and creates ecosystem naming inconsistency; retiring opportunistically during Phase 2 visits is lowest-cost remediation and avoids a dedicated migration prompt for a cosmetic change.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A5)
- **Status:** open — designated as legacy pattern; retire opportunistically during Phase 2 repo visits. No dedicated migration prompt needed; handle when touching those files anyway.

### [P3] [open] ADR-42 amendment — clarify single vs multi-artifact handoff format
- **What:** ADR-42 v3.2 specifies folder-format handoffs. Empirically established 2026-05-11 that single-artifact handoffs work better as flat `.md` in `docs/handoffs/`. Folder format reserved for multi-artifact bundles with `contents/` subfolder. ADR-42 text does not state this distinction explicitly.
- **Why:** Methodology debt — practitioners must infer the rule from convention rather than reading it in the ADR. Without explicit statement, future sessions may default to folder format for single-artifact handoffs, causing unnecessary complexity.
- **Vision ref:** VISION.md — methodology evolution
- **Added:** 2026-05-12
- **Status:** open

### [P3] [open] docs/HANDOFF.md flat file deprecation (corp-monorepo, ai-council)
- **What:** Both `corp-monorepo` and `ai-council` have `docs/HANDOFF.md` at `docs/` level (pre-ADR-42 flat pattern). Not breaking. Retire at next handoff event or explicitly designate as legacy.
- **Why:** Pre-ADR-42 flat pattern persists alongside folder-format handoffs; parallel patterns mislead future sessions about which format is the active standard. Explicit deprecation or migration is required to maintain clarity.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** open — tied to A4 decision (Handoff folder format adoption, above).

### [P3] [open] Undiscovered repos confirmation
- **What:** Repos `corp-knowledge-extractor`, `corp-by-os`, `corp-rfp-agent` not found under `Dev/` during 2026-05-11 audit. Confirm status: renamed, archived, not yet cloned, or dropped.
- **Why:** Unknown repo status creates a gap in ecosystem audit coverage; universalization rollout cannot be fully scoped if repos may exist that are not tracked. Confirmation before Phase 3 prevents missed repos.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** open

---

## Hyphen Convention Migration Sequence (Prompt J ratification)

### [P2] [open] CI enforcement of hyphen-only separator rule
- **What:** Pre-commit hook + GitHub Action enforcing hyphen-only separator in new filenames and foldernames. Scope TBD: which paths (`.md` only vs all?), generated artifact handling (exclude CLI auto-generated?), exceptions list. Per Council synthesizer blind spot 4: enforcement mechanism deferred from this PR.
- **Why:** Convention without enforcement drifts. Manual discipline insufficient per 2026-05-11 audit finding (recommendation-tier scope failed immediately).
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** open — scope decision needed before implementation; small Council question or conversational decision.

### [P2] [open] corp-monorepo hyphen migration + ADR-38 compliance (Phase 2 expanded scope)
- **What:** (1) Universal hyphen filename migration for corp-monorepo ADR files; (2) ADR-38 Scale L gaps closure: ARCHITECTURE.md move to root (from `docs/`), add VISION.md, LESSONS.md, BACKLOG.md; (3) `docs/archive/` content reclassification per content-scoped archival principle (CODE_REVIEW_REPORT files currently at top level of `docs/archive/` — should move to `docs/audits/archive/` or appropriate scoped location).
- **Why:** ADR-34 amendment (universal mandate) + ADR-38 amendment (root placement) both now apply to corp-monorepo. Phase 2 scope expanded from original "verify compliance" to "migrate non-compliant items."
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-11 by rob (Prompt J ratification, expanded from Prompt H P2)
- **Status:** open — execute in Phase 2, separate prompt; after Prompt K closes.
- **Status update 2026-05-23:** Subitem (2) ADR-38 Scale L gaps closure — CONFIRMED COMPLETE per 2026-05-23 ecosystem audit (`check_adr38_baseline` PASS on corp-monorepo; report `docs/audits/2026-05-23-ecosystem-audit.md`). Subitems (1) hyphen migration + (3) archive reclassification — NOT verified by audit; remain open. Entry status: OPEN (partial completion).

### [P2] [open] ai-council hyphen migration + ADR-38 compliance (Phase 2 expanded scope)
- **What:** (1) Universal hyphen filename migration for ai-council (likely low impact — audit suggests mostly hyphen-compliant already; verify before migrating); (2) ADR-38 Scale M gaps closure: ARCHITECTURE.md to root, add LESSONS.md, BACKLOG.md. ai-council AGENTS.md removed 2026-05-19 per ADR-53 chunk 4.
- **Why:** ADR-34 amendment (universal mandate) + ADR-38 amendment (root placement) now apply. Confirm compliance before claiming clean.
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-11 by rob (Prompt J ratification, expanded from Prompt H P2)
- **Status:** open — execute in Phase 2, separate prompt; after cross-repo handshake (P1 above) completes.

### [P2] [open] Content-scoped archival principle codification
- **What:** New principle emerged 2026-05-11: archive subfolder location follows artifact type (handoffs/archive/ only for handoff content; decisions/archive/ for decisions if archival needed; each content type has own scoped archive subfolder). Generic `docs/archive/` as top-level mixed-content grab-bag (current corp-monorepo pattern) is anti-pattern. Codification options: amendment to ADR-38 (universal repo architecture) OR new ADR-44 (archival principle). Defer codification to second empirical instance (per N=1 anti-pattern lesson).
- **Why:** Principle emerged from operator framing during archival destination decision for cross-repo propagation artifact. First empirical instance captured. Premature ADR at N=1 is itself an anti-pattern (see LESSONS.md).
- **Vision ref:** VISION.md "Knowledge Guardian" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** open — captured in LESSONS.md (2026-05-11 entry). Codification awaits second empirical instance. Monitor for second instance during Phase 2 repo visits.

### [P2] [open] Fix pre-existing test failure: test_ratio_pass_when_stable_above_ceiling
- **What:** Fails on main as of 2026-05-12 prior to hooks review work. Not introduced by Directive 5 of 2026-05-12 handoff (witnessed during Prompt 4 verification). Blocks clean `pytest -x` runs; pre-commit may flag in subsequent sessions if test is in pre-commit scope. Root cause unknown — needs investigation.
- **Why:** Clean test state is a baseline hygiene requirement. Pre-existing failures mask future regressions.
- **Vision ref:** VISION.md — methodology consistency (clean test state)
- **Added:** 2026-05-12
- **Status:** open

### [P3] [open] A5 Phase 2: retire UPPERCASE TYPE tag in legacy archive filenames
- **What:** During Phase 2 repo visits (corp-monorepo, ai-council), when touching `docs/archive/` files with `YYYY-MM-DD_TYPE_topic.md` pattern — rename to plain `YYYY-MM-DD-topic.md` (hyphen separator, no UPPERCASE tag). Opportunistic, not a dedicated migration.
- **Why:** Pre-ADR-34 legacy pattern creates naming inconsistency during Phase 2 repo visits; opportunistic retirement is lowest-cost path and avoids a dedicated migration prompt for a cosmetic change.
- **Added:** 2026-05-11 by rob (Prompt J ratification, A5 designation)
- **Status:** open — opportunistic during Phase 2 visits; no dedicated prompt.

---
