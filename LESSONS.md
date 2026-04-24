# Lessons Learned — Append-Only Log
<!-- scope: hybrid -->

> **Format:** Date | Source | Lesson | Category | Action taken
> New entries go at the bottom. Never edit old entries. Never delete.
> Last updated: 2026-03-30

---

> Split trigger at 50 entries (currently 61) deferred 2026-04-24. Rationale: ADR-29 [scope: X] inline field provides equivalent filtering without losing chronology. Reopen if filtering by scope proves insufficient.

## Entries

### 2026-04-21 | browser-chat | Browser-as-tutor defaulting violates three-layer architecture | process | caught + corrected mid-session

### 2026-03-25 | corp-monorepo session | "Stop debating, start deploying" — council debates are valuable but can become procrastination | process | Hard rule: max 2 debates before implementation

### 2026-03-26 | corp-monorepo session | HyperAgents: "Last triggered" date on persistent lessons enables data-driven pruning — agents that track frequency improve faster | architecture | Added to gotchas skill format

### 2026-03-26 | corp-monorepo session | Claude synthesizer costs $0.23/debate (46% of total) — switch to Gemini ($0.04) for synthesis | token-optimization | Updated council default synthesizer to gemini

### 2026-03-28 | dev-practice session | Opus output verbosity (7.5:1 output-to-input ratio) is the main token drain, not model choice | token-optimization | Added conciseness instruction to CLAUDE.md

### 2026-03-28 | dev-practice session | /clear between tasks saves 30-40% input tokens — council unanimous #1 optimization | process | Added to session management workflow

### 2026-03-28 | dev-practice session | Claude Code PowerShell tool requires explicit CLAUDE.md instruction "prefer PowerShell" — settings.json alone insufficient | gotcha | Added Shell section to CLAUDE.md

### 2026-03-28 | dev-practice session | Native installer auto-updates, npm is deprecated — migrate before deploying skills | tooling | Migrated to native Claude Code installer

### 2026-03-28 | dev-practice session | Nested _outputs/_outputs/ caused by script writing to wrong relative dir — always verify output paths | architecture | Added to gotchas

### 2026-03-28 | dev-practice session | "Sacrifice formatting to save tokens, never sacrifice content" — for handoffs between tools | prompt-craft | Created /handoff command

### 2026-03-28 | dev-practice session | Don't constrain output by volume ("max 50 lines") — constrain by format ("flat not tables") | prompt-craft | Corrected /handoff prompt

### 2026-03-28 | corp-monorepo retrospective | Never trust "it's done" from AI in a long session — context degradation accelerates after ~4 hours, AI confabulates based on stale mental model | process | Added verification after every major operation as hard rule

### 2026-03-28 | corp-monorepo retrospective | "Commit and move on" is a trap — optimizing for closure over correctness. When the human says "something feels off" — STOP and investigate, don't reassure | process | Handoff written continuously, not at session end

### 2026-03-28 | corp-monorepo retrospective | Any path change is a database migration — editable installs bake absolute paths, ops.db rows have old paths, venvs have baked paths, PowerShell profile on OneDrive | gotcha | Created path_consumers.md checklist concept; added editable-install reinstall to gotchas

### 2026-03-28 | corp-monorepo retrospective | .ecosystem/ needs enforcement, not just convention — conventions in markdown are suggestions, without validation script drift is inevitable | architecture | Added validation rules to corp doctor

### 2026-03-28 | corp-monorepo retrospective | Claude.ai guesses file paths from memory, Claude Code sees actual files — never let Claude.ai generate filesystem commands from stale mental model | process | Prompts for Claude Code are QUESTIONS not COMMANDS; Claude Code discovers state first

### 2026-03-28 | corp-monorepo retrospective | Naming decisions drain disproportionate energy (ADHD perfectionism loop) — set timer: 2 min to propose, 1 min to pick, never reopen | process | 3 options → 30 seconds → pick shortest → move on

### 2026-03-28 | corp-monorepo retrospective | Test after each structural change IMMEDIATELY, not at the end — broken editable installs after Scripts/ → Dev/ migration found 2 hours late because tests ran at the end | gotcha | Added "pytest after each step" to every Claude Code prompt format

### 2026-03-28 | corp-monorepo retrospective | Council decisions need instant ADR capture — 22 debates but ADRs #13-21 were missing for days because the pipeline was manual | process | Designed corp council-archive automation; until scripted, added to session protocol checklist

### 2026-03-28 | corp-monorepo retrospective | Handoff quality determines next session quality — writing handoffs at end of session = lowest energy, most degraded context, highest time pressure | process | Write handoff notes continuously (JOURNAL entries after each task), final handoff is just formatting

### 2026-03-28 | corp-monorepo retrospective | "One more thing" anti-pattern — cleanup work is fractal, every dirty corner reveals 3 more. Session planned for 2 tasks expanded to 13 | process | Hard rule: 1-2 objectives per session, everything else → backlog. Set context budget: "50% context left = write handoff"

### 2026-03-28 | corp-monorepo retrospective | Don't declare victory before user sees results — sandbox renames, vault rebuilds, extraction outputs need human review step before "done" | process | Added REVIEW CHECKPOINT markers in prompts; "show me 3 examples" before "clean up the rest"

### 2026-03-28 | corp-monorepo retrospective | Git discipline was non-negotiable but got negotiated — session ended with 27 modified, 20 untracked files. Commits batched instead of per-step | gotcha | "git status must show clean between each numbered step" added to prompt format

### 2026-03-28 | corp-monorepo retrospective | Best Claude Code prompts are investigative (UNDERSTAND → PLAN → EXECUTE → VERIFY → COMMIT), not imperative commands | prompt-craft | Updated prompt format: always start with UNDERSTAND, never skip to EXECUTE

### 2026-03-28 | corp-monorepo retrospective | Handoff generator only as good as its sources — update_handoff.py produced 113-line doc missing 80% of state because it read narrow inputs | architecture | Handoff generator must read ALL sources (JOURNAL, decisions/, eval/, git log, test results) + include "Generated from" footer

### 2026-03-29 | dev-practice-os session | verify: lines transform gotchas from "text Claude hopefully reads" into "rules Claude automatically verifies" — machine-checkable enforcement beats documentation | architecture | Added verify: lines to all 41 gotchas (27 auto-verifiable, 14 manual debt)

### 2026-03-29 | dev-practice-os session | core-invariants.md with paths: **/* loads on every file touch, surviving context compaction — compression-proof rules for the 5 most critical safety rules | architecture | Created ~/.claude/rules/core-invariants.md

### 2026-03-29 | dev-practice-os session | Every prompt should include Model/Mode/Effort table — deterministic routing replaces "use judgment" for ADHD-friendly zero-decision workflow | prompt-craft | Added summary table to PLAYBOOK Section 2 with quick-reference examples

### 2026-03-29 | dev-practice-os session | Claude.ai browser role is NOT just "architecture" — it's critical thinking layer that challenges, pushes back, says "no." Rubber-stamping is a failure mode | process | Updated PLAYBOOK Section 7 with explicit critical thinking mandate

### 2026-03-29 | dev-practice-os session | Knowledge domains should stay separate — pre-sales work knowledge (vault) and dev practice methodology (.dev-knowledge/) serve different contexts, mixing them pollutes search and creates cognitive noise | architecture | Kept vault for work knowledge only, dev practice stays in Dev/.dev-knowledge/, Claude Code config stays in ~/.claude/

### 2026-03-29 | self-evolving-article analysis | Self-evolution article's biggest insight: corrections.jsonl + auto-promotion on 2nd occurrence. Most of the article's infrastructure (agents, path-scoped rules) we already had under different names | tooling | Cherry-picked 5 actionable items (verify lines, corrections log, core-invariants, /boot, session scorecard), skipped the rest

### 2026-03-29 | dev-practice-os session | repos with <100 stars and v0.1.0 = too early to adopt, even when they solve real pain — agentfiles (25 stars, 1 day old) and skill-kit (31 stars, 0 releases) failed own criteria | process | Documented in PLAYBOOK Section 9, enforced as evaluation checkpoint

### 2026-03-28 | council-token-optimization | Every routing decision between providers is a "cache miss that flushes the developer's working set" — for ADHD, fewer providers = higher throughput, even if multi-provider is theoretically cheaper | architecture | Stay on single Claude Max, rejected GLM-5.1 dual-backend

### 2026-03-28 | council-token-optimization | Time-shifting heavy work to 08:00-14:00 CET leverages Anthropic off-peak (3-8AM ET) AND ADHD morning hyperfocus window. Afternoon = light work only (review, docs, testing) | process | Calendar blocked, added to ROUTING.md time-shift section

### 2026-03-28 | council-token-optimization | Manual token logging in spreadsheets has "terrible survival rate with ADHD" — automate or use gut-check: "did I hit rate limit today? what was I doing?" | process | No spreadsheet, intuitive daily check only, re-evaluate GLM on April 12 if limits hit >2x/week

### 2026-03-28 | council-token-optimization | The cheapest tokens are the ones you don't send — /clear between tasks (30-40%), front-load specs (15-25% fewer roundtrips), line ranges (10-20%), batch changes (10-15%) | token-optimization | Ranked by impact/effort, implemented as habits not tools

### 2026-03-28 | council-token-optimization | Compaction at 40% (not 50%) is aggressive but correct — long sessions carry too much dead context. Set-and-forget config wins over willpower-dependent habits | token-optimization | Config: CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40

### 2026-03-29 | dev-practice-os session | Lessons from chats die in browser history if not extracted — need explicit end-of-chat extraction step: "what 2-3 things did I learn?" → append to LESSONS.md | process | Added extraction process to PLAYBOOK and SESSION_SETUP

### 2026-03-29 | axel-bitblaze article | After 2 failed attempts → /clear and rewrite prompt from scratch. Polluted context with wrong approaches actively hurts — fresh context almost always nails it | process | Added as golden rule to PLAYBOOK Appendix C and ESSENTIALS

### 2026-03-29 | axel-bitblaze article | ! prefix runs shell commands directly without Claude processing — !git status, !pytest inject output to context at zero AI token cost | token-optimization | Added to ESSENTIALS and PLAYBOOK Appendix A+C

### 2026-03-29 | axel-bitblaze article | CLAUDE.md instruction adherence drops above 200 lines — confirmed our architecture decision to split rules into ~/.claude/rules/ and skills/gotchas/ instead of one mega CLAUDE.md | architecture | Noted as validation, no action needed (already doing this)

### 2026-03-29 | council-browser-handoff #24 | Browser handoff is a checkpoint, not an autopsy — trigger at ~2 hours while context is fresh, not at 4+ hours when context is degraded. Generate → Copy → Paste, zero archiving step | process | Added to PLAYBOOK Section 8, SESSION_SETUP, ESSENTIALS

### 2026-03-29 | council-browser-handoff #24 | One universal handoff format, zero choices for Rob — Claude auto-adapts sections based on chat content (programming vs business). Two templates = branching decision = ADHD death | architecture | Single template with optional sections, Claude decides

### 2026-03-29 | dev-practice-os session | Council debate format is NOT Claude Code prompt format — debate = YAML frontmatter + question + numbered options + constraints. Prompt = Model/Mode/Effort + UNDERSTAND + Steps. Mixing produces bloated narrative debates | prompt-craft | Corrected browser handoff debate format

### 2026-03-30 | universalization session | Content written during project work gets absorbed wholesale — always abstract into universal methodology before writing to .dev-knowledge/ | architecture | universalization pass completed

### 2026-03-30 | universalization session | Name folders by function not origin — .ecosystem/ was a relic of "ecosystem of packages" mental model, docs/ is universally understood | process | .ecosystem/ eliminated, docs/ standardized in PLAYBOOK

### 2026-03-30 | universalization session | One governance home, zero exceptions — decisions/ at root alongside docs/ breaks "one home per file type" immediately after establishing the rule | architecture | decisions/ moved to docs/decisions/

### 2026-03-30 | universalization session | Skills scoping: ~/.claude/skills/ = universal (loads everywhere), repo/.claude/skills/ = project-specific (auto-discovered). When in doubt, project scope — better to load explicitly than pollute globally | tooling | gotchas split 3 universal + 37 project-specific

### 2026-03-30 | Codex audit session | Audit-first, fix-second is the only safe order — jumping straight to fixes without a read-only audit produces thrash: fixes invalidate each other, new issues appear mid-session, scope creeps | process | Established Audit-Fix-Verify cycle: read-only pass → triage by severity → fix by tier → re-audit

### 2026-03-30 | Codex audit session | Two AI reviewers catch different blind spots — Claude Code misses structural violations it introduced; Codex flags them because it has no authorship bias. Reviewer ≠ builder | architecture | Hard rule: Codex reviews, Claude Code builds. Never reverse the roles.

### 2026-03-30 | Codex audit session | Structural refactors need shims, not big-bang rewrites — renaming a module used in 40 places requires a compatibility shim first, then migrate callers incrementally, then remove shim | process | Added to PLAYBOOK S16; applies to any change with N>5 call sites

### 2026-03-30 | Codex audit session | ARCHITECTURE.md is the highest-value deliverable of any major session — code can be re-derived from git, but the "why" behind structural decisions evaporates in 48 hours | architecture | Any session that touches module boundaries or dependency direction must produce or update an ARCHITECTURE.md

### 2026-03-30 | Codex audit session | Automated audit false-positive rate ~30% — calibrate AGENTS.md severity levels against real violations before treating every flag as critical. Over-flagging → flag fatigue → real issues ignored | process | After first audit run: triage flags manually, demote false-positive patterns to MEDIUM/LOW in AGENTS.md

### 2026-03-30 | dev-practice session | Universal rules that don't apply universally erode compliance — if a Playbook rule says "update per-module READMEs" but the project has no modules, Claude Code learns that Playbook rules are suggestions. Fix: declare project scale (L/M/S) in CLAUDE.md, tag scale-dependent rules in Playbook, leave universal rules untagged. Rules that apply — apply always. Rules that don't apply — are explicitly scoped out, not silently ignored | process | Added Project Scale Tier system to PLAYBOOK.md and ESSENTIALS.md

### 2026-03-30 | dev-practice session | TODO markers belong in code and tasks/todo.md, never in documentation — TODO in code = technical debt marker (valuable, TODO Tree tracks it). TODO in docs = noise — docs are instructions, not task lists. If a doc needs work, add entry to tasks/todo.md with file reference, don't leave TODO in the doc itself. Applies to all project scales | process | Rule established; applies to all repos

### 2026-04-15 | corp-monorepo tach-adoption session | Intent-based module classification fails; use actual import graph — when classifying modules into architectural layers, don't rely on design intent documents. Use tach sync output (AST-parsed imports) as ground truth. corp.project_resolver was classified as orchestration by intent but imported by core modules. corp.query_engine was classified as interface but imported by orchestration. Tach sync revealed the truth in seconds. Applies to Scale L projects. | architecture | Use tach sync as classification ground truth before writing boundary rules

### 2026-04-15 | corp-monorepo tach-adoption session | Baseline violations are documentation, not blockers — when adopting boundary enforcement (Tach, lint rules), document baseline violations and fix in a separate phase. Phase 1 = instrumentation + documentation. Phase 2 = reclassification fixes. This prevents scope creep and keeps each PR focused. CI may fail between phases — this is known and acceptable if Phase 2 follows immediately. | process | Phased adoption: instrument first, fix in dedicated follow-up PR

### 2026-04-15 | corp-monorepo council-session | Council debate quality scales with real data — Council #26 brief improved significantly after feeding it real numbers (0 import violations from grep, pytest timing 166s, .pre-commit-config.yaml contents). Briefs without repo-specific data produce generic recommendations. Always run data-gathering audit before Council debate. | process | Gather concrete repo metrics before writing Council brief

### 2026-04-24 | stream-a-finale | Prerequisite guards prevent cascade failures across multi-prompt streams | gotcha | [scope: meta] | added prereq check pattern to prompt template

### 2026-04-24 | stream-a-finale | ADR prescription can drift from validator reality — H1 insertion point for LESSONS.md file-level tag discovered wrong only during implementation | process | [scope: meta] | amend ADR when reality proves prescription wrong, do not reopen the decision

### 2026-04-24 | stream-a-finale | Sanity-check step after any bulk change catches systematic errors — Prompt 3.5 caught 5 of 20 top-level PLAYBOOK tag mismatches | process | [scope: dev] | added sanity-check pattern to prompt template for bulk tagging operations

---
Date: 2026-04-21
Source: .dev-knowledge audit + Council #27 session
Lesson: Session wyprodukowała 4 process-level lessons about (a) handoff content granularity — WHAT vs HOW-level detail, (b) browser-chat-as-tutor anti-pattern (proactive session transitions violate PLAYBOOK S8), (c) scope creep flagging — real-time detection zamiast post-hoc, (d) decision fatigue predictability at >3h / >3 decisions. See handoff 2026-04-21-dev-knowledge-architecture-redefinition.md for detail and generative rule candidates.
Category: process | meta
Action: Lessons 1, 2, 4 mają generative rule candidates — promote to PLAYBOOK/HANDOFF_PROCESS.md przy drugim powtórzeniu pattern (per feedback loop rule). Lesson 3 = specific-case observation.
---

---
Date: 2026-04-24
Source: repo hygiene session (handoff/ → handoff-prompts/ rename)
Lesson: Renames that create basename collisions with in-scope files expose validator path-handling assumptions. When validator uses basename lookups (rather than full-path), a file with the same name in a skipped directory can spoof in-scope file's HEAD content, corrupting ratio calculations. Fix: validators should match on full path + ensure is_in_scope() guard before substituting staged content.
[scope: dev]

---
Date: 2026-04-24
Source: repo hygiene session (README.md rewrite)
Lesson: File-level scope tag (placed under H1) causes validator to count all sections as 1 for ratio purposes, shrinking denominator and triggering false regressions when the file's headers are counted separately. Prefer per-section tags (each H2 tagged individually) over file-level tag for repos with ratio-based enforcement. File-level tag remains appropriate for append-only logs (LESSONS.md) where section count is not meaningful.
[scope: dev]
