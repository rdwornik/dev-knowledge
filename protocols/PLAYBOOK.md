# Dev Practice Playbook

> **Living document.** Repeatable processes for everything Rob does regularly with AI-assisted development.
> Last updated: 2026-06-24
>
> *Section history lives in git (commit log + JOURNAL `Changes:` line), not in per-section changelog blocks — per ADR-49.*
>
> **Organization:** Two explicit parts. **Part I — Reference** (chapters Ch1–Ch14: System Architecture, the CLAUDE.md contract, repo conventions, documentation file types, session boundaries, Claude Code internals, …) → **Part II — Workflows** (numbered recipes §1–§19; the §18 gap is intentional — it was deleted; git has it) followed by **Appendices A–C** plus tooling addenda (Codemap, Auto-TOC). Every heading carries an ordinal under an explicit Part; the numbered spine is the workflow-recipe middle, not the whole document.

<!-- structure-allow: numbering-gap 18 — deleted, git has it -->

---

<!-- TOC:START -->
- [Part I — Reference](#part-i--reference)
- [Ch1. System Architecture](#ch1-system-architecture)
  - [Cross-reference](#cross-reference)
- [Ch2. CLAUDE.md as agent-instruction contract](#ch2-claudemd-as-agent-instruction-contract)
  - [Authority hierarchy](#authority-hierarchy)
  - [What CLAUDE.md is](#what-claudemd-is)
  - [What CLAUDE.md is NOT](#what-claudemd-is-not)
  - [Why ≤200 lines](#why-200-lines)
  - [LLMs advise; hooks/tests enforce](#llms-advise-hookstests-enforce)
  - [Drift-proofing precedence: source → gate → agent](#drift-proofing-precedence-source--gate--agent)
  - [Child methodology floor (ADR-78)](#child-methodology-floor-adr-78)
  - [Template](#template)
  - [Update cadence](#update-cadence)
  - [Length notes](#length-notes)
  - [Handoff scope](#handoff-scope)
  - [LLM-LLM context transfer is back-and-forth, not unilateral](#llm-llm-context-transfer-is-back-and-forth-not-unilateral)
  - [Process versioning: beta vs stable promotion](#process-versioning-beta-vs-stable-promotion)
- [Ch3. Repo conventions](#ch3-repo-conventions)
  - [Default branch — `main`](#default-branch--main)
  - [File naming conventions](#file-naming-conventions)
  - [Folder structure](#folder-structure)
  - [Root hygiene convention](#root-hygiene-convention)
  - [Additional root hygiene rules (added 2026-05-24, root hygiene pass 2)](#additional-root-hygiene-rules-added-2026-05-24-root-hygiene-pass-2)
  - [Universal visual pattern (per ADR-59)](#universal-visual-pattern-per-adr-59)
  - [docs/ folder taxonomy (per ADR-60)](#docs-folder-taxonomy-per-adr-60)
  - [Secrets storage path](#secrets-storage-path)
  - [Capitalization conventions](#capitalization-conventions)
  - [Rule-ID naming convention (doc to code edge)](#rule-id-naming-convention-doc-to-code-edge)
- [Ch4. Writing prompts for Claude Code](#ch4-writing-prompts-for-claude-code)
  - [Why standard format](#why-standard-format)
  - [Standard structure (8 sections)](#standard-structure-8-sections)
  - [Per-Scale guidance](#per-scale-guidance)
  - [Delivery format](#delivery-format)
  - [Pre-send checklist](#pre-send-checklist)
  - [Anti-patterns](#anti-patterns)
  - [Checkable rules: concrete over aspirational](#checkable-rules-concrete-over-aspirational)
  - [Update cadence](#update-cadence-1)
- [Ch5. Project complexity bands](#ch5-project-complexity-bands)
  - [Testing rules (scaled by repo complexity)](#testing-rules-scaled-by-repo-complexity)
  - [VS Code workspace](#vs-code-workspace)
- [Ch6. Documentation file types and session continuity](#ch6-documentation-file-types-and-session-continuity)
  - [File type taxonomy](#file-type-taxonomy)
  - [File presence (universal baseline)](#file-presence-universal-baseline)
  - [Canonical-file freshness cadence (audit check #10)](#canonical-file-freshness-cadence-audit-check-10)
  - [Multi-surface amendment coherence (audit check `amendment_coherence`)](#multi-surface-amendment-coherence-audit-check-amendment_coherence)
  - [Declared-edge reconciliation (audit check `reconciled_versions`)](#declared-edge-reconciliation-audit-check-reconciled_versions)
  - [Common confusions resolved](#common-confusions-resolved)
  - [Supersession & decommissioning](#supersession--decommissioning)
  - [Handoff format spec](#handoff-format-spec)
  - [Order conventions](#order-conventions)
- [Ch7. Review postures](#ch7-review-postures)
- [Ch8. Session boundaries](#ch8-session-boundaries)
  - [Scope declaration at start](#scope-declaration-at-start)
  - [Stop-signs (recognize and act)](#stop-signs-recognize-and-act)
  - [Decision fatigue threshold](#decision-fatigue-threshold)
  - [Recursive planning anti-pattern](#recursive-planning-anti-pattern)
  - [Session resumption protocol](#session-resumption-protocol)
  - [Parallel sessions & worktree discipline (per ADR-61)](#parallel-sessions--worktree-discipline-per-adr-61)
  - [No leftovers: automated processes clean up — and verify it (invariant)](#no-leftovers-automated-processes-clean-up--and-verify-it-invariant)
- [Ch9. Tier-1 closure loop — usage](#ch9-tier-1-closure-loop--usage)
  - [Propagating a plugin change across the fleet](#propagating-a-plugin-change-across-the-fleet)
- [Ch10. Two-tier automation doctrine](#ch10-two-tier-automation-doctrine)
  - [Writer policy — automation that writes the tree commits its own output (ADR-80)](#writer-policy--automation-that-writes-the-tree-commits-its-own-output-adr-80)
  - [What each tier checks (a green one and a red other are both correct)](#what-each-tier-checks-a-green-one-and-a-red-other-are-both-correct)
- [Ch11. Routine/night deployment standard](#ch11-routinenight-deployment-standard)
  - [The envelope](#the-envelope)
  - [Naming](#naming)
  - [Safety envelope — allow-only platform guards, no committed deny](#safety-envelope--allow-only-platform-guards-no-committed-deny)
  - [Spec-orchestration doctrine — and why code guarantees must sit on the executing path](#spec-orchestration-doctrine--and-why-code-guarantees-must-sit-on-the-executing-path)
  - [The outcome loop](#the-outcome-loop)
  - [T-shirt model pins](#t-shirt-model-pins)
  - [Cloud-session closeout](#cloud-session-closeout)
  - [The shallow-clone false-positive class](#the-shallow-clone-false-positive-class)
  - [Cloud-session hub-independence (self-containment)](#cloud-session-hub-independence-self-containment)
  - [What every routine must meet (the operational standard)](#what-every-routine-must-meet-the-operational-standard)
- [Ch12. Definition of done (organs)](#ch12-definition-of-done-organs)
  - [Definition of shipped (closure gate)](#definition-of-shipped-closure-gate)
- [Ch13. Continuous Improvement](#ch13-continuous-improvement)
  - [Pipeline overview](#pipeline-overview)
  - [Stage 1: Discovery](#stage-1-discovery)
  - [Stage 2: Triage](#stage-2-triage)
  - [Stage 3: Evaluation](#stage-3-evaluation)
  - [Stage 4: Decision](#stage-4-decision)
  - [Stage 5: Implementation (only for "Adopt")](#stage-5-implementation-only-for-adopt)
  - [Stage 6: Review (on-trigger)](#stage-6-review-on-trigger)
  - [Where evaluations are recorded](#where-evaluations-are-recorded)
- [Ch14. Claude Code internals](#ch14-claude-code-internals)
  - [Quick disambiguation](#quick-disambiguation)
  - [Usage protocol: which command / hook, when](#usage-protocol-which-command--hook-when)
  - [7a. Skills (progressive-disclosure knowledge modules)](#7a-skills-progressive-disclosure-knowledge-modules)
  - [7b. Slash commands (custom invokable commands)](#7b-slash-commands-custom-invokable-commands)
  - [7c. Hooks (lifecycle automation)](#7c-hooks-lifecycle-automation)
  - [7d. Subagents (separate Claude instances)](#7d-subagents-separate-claude-instances)
  - [Adoption protocol — when Claude Code proposes a new skill/command/hook/subagent](#adoption-protocol--when-claude-code-proposes-a-new-skillcommandhooksubagent)
  - [Cross-reference to CLAUDE.md tools sections](#cross-reference-to-claudemd-tools-sections)
- [Part II — Workflows](#part-ii--workflows)
- [1. Starting a New Project](#1-starting-a-new-project)
  - [Scaffold](#scaffold)
  - [CLAUDE.md template (minimum viable)](#claudemd-template-minimum-viable)
  - [First commit, then dev loop](#first-commit-then-dev-loop)
- [2. Creating a Claude Code Prompt](#2-creating-a-claude-code-prompt)
  - [Architect output vs CC consumption-spec](#architect-output-vs-cc-consumption-spec)
  - [Summary table (required at top of every formal prompt)](#summary-table-required-at-top-of-every-formal-prompt)
  - [How to choose Model](#how-to-choose-model)
  - [When to escalate to a Dynamic Workflow](#when-to-escalate-to-a-dynamic-workflow)
  - [How to choose Mode](#how-to-choose-mode)
  - [How to choose Effort](#how-to-choose-effort)
  - [Model / effort platform doctrine (Claude Code 2.1.x)](#model--effort-platform-doctrine-claude-code-21x)
  - [Structure](#structure)
  - [Quick-reference examples](#quick-reference-examples)
  - [Decision scope for when to write a formal prompt](#decision-scope-for-when-to-write-a-formal-prompt)
  - [Key rules](#key-rules)
  - [Prompt Generation Card maintenance rule (per ADR-56, Council Q3)](#prompt-generation-card-maintenance-rule-per-adr-56-council-q3)
- [3. Absorbing New Information](#3-absorbing-new-information)
  - [Evaluation flow](#evaluation-flow)
  - [Council debate threshold](#council-debate-threshold)
- [4. Extracting Lessons from Any Session](#4-extracting-lessons-from-any-session)
  - [When to extract](#when-to-extract)
  - [How to extract (2 minutes, no more)](#how-to-extract-2-minutes-no-more)
  - [What qualifies as a lesson](#what-qualifies-as-a-lesson)
  - [What does NOT qualify](#what-does-not-qualify)
  - [When a lesson becomes a rule](#when-a-lesson-becomes-a-rule)
- [5. Running an AI Council Debate](#5-running-an-ai-council-debate)
  - [When to use Council vs. decide yourself](#when-to-use-council-vs-decide-yourself)
  - [Debate question format (summary)](#debate-question-format-summary)
  - [Running the debate](#running-the-debate)
  - [Post-debate protocol](#post-debate-protocol)
  - [Council Debate Archival Protocol](#council-debate-archival-protocol)
  - [Council output convention (current state)](#council-output-convention-current-state)
  - [When to run Council vs single-model + critic](#when-to-run-council-vs-single-model--critic)
  - [ADR authorship paths (how an ADR gets written)](#adr-authorship-paths-how-an-adr-gets-written)
  - [Amendment vs Reopen Decision Protocol](#amendment-vs-reopen-decision-protocol)
  - [Codex review archival protocol](#codex-review-archival-protocol)
- [6. Code Review with Claude Code](#6-code-review-with-claude-code)
  - [Process](#process)
- [7. Managing a Long Claude Code Session](#7-managing-a-long-claude-code-session)
  - [Session start protocol](#session-start-protocol)
  - [During session](#during-session)
  - [When context gets heavy](#when-context-gets-heavy)
  - [Context budget — read-scoping rule](#context-budget--read-scoping-rule)
  - [Session end protocol](#session-end-protocol)
- [8. Handing Off Between Sessions](#8-handing-off-between-sessions)
  - [What the v5 handoff carries](#what-the-v5-handoff-carries)
  - [Roles](#roles)
  - [Handoff paths](#handoff-paths)
  - [Token log cadence](#token-log-cadence)
  - [Output the operator copies into browser chat (render-layer note)](#output-the-operator-copies-into-browser-chat-render-layer-note)
- [9. Weekly Review (Friday)](#9-weekly-review-friday)
- [10. BACKLOG Grooming Workflow](#10-backlog-grooming-workflow)
  - [Schema (ADR-66; machine-checked by `scripts/validate_backlog.py`)](#schema-adr-66-machine-checked-by-scriptsvalidate_backlogpy)
  - [Per-handoff grooming (~2 min, mandatory for M+)](#per-handoff-grooming-2-min-mandatory-for-m)
  - [Quarterly deep grooming (~30 min, scheduled)](#quarterly-deep-grooming-30-min-scheduled)
  - [Split-brain prevention](#split-brain-prevention)
- [11. Evaluating a New Tool/Framework/Model](#11-evaluating-a-new-toolframeworkmodel)
  - [Quick eval checklist](#quick-eval-checklist)
  - [Decision framework](#decision-framework)
- [12. Multi-Project Rules](#12-multi-project-rules)
  - [Principles](#principles)
  - [Config hierarchy (most specific wins)](#config-hierarchy-most-specific-wins)
- [13. Where Knowledge Lives](#13-where-knowledge-lives)
  - ["Where does this go?" decision rule](#where-does-this-go-decision-rule)
  - [When a lesson becomes a rule](#when-a-lesson-becomes-a-rule-1)
  - [Data sanitization](#data-sanitization)
  - [Migration triggers](#migration-triggers)
- [14. Markdown Governance](#14-markdown-governance)
  - [Project governance folder](#project-governance-folder)
  - [Diagram-form selection algorithm](#diagram-form-selection-algorithm)
- [15. Anti-Patterns — What NOT to Do](#15-anti-patterns--what-not-to-do)
- [The 10 Commandments](#the-10-commandments)
- [16. Cross-Tool Review](#16-cross-tool-review)
  - [Review Tools](#review-tools)
- [17. Code Quality Audit Process](#17-code-quality-audit-process)
  - [Severity tiers](#severity-tiers)
  - [Process](#process-1)
  - [Rules](#rules)
  - [Post-Structural-Change Documentation](#post-structural-change-documentation)
- [19. Scrum-Master Review Propagation](#19-scrum-master-review-propagation)
  - [Three-stage flow](#three-stage-flow)
  - [Addendum mechanism](#addendum-mechanism)
  - [Distinction from cross-repo amendment handshake](#distinction-from-cross-repo-amendment-handshake)
  - [Single-round-trip framing](#single-round-trip-framing)
  - [Cover-letter template](#cover-letter-template)
  - [Rules](#rules-1)
- [Appendix A: Claude Code Shortcuts](#appendix-a-claude-code-shortcuts)
  - [Permission Modes (Shift+Tab cycles)](#permission-modes-shifttab-cycles)
  - [Keyboard](#keyboard)
  - [Slash Commands](#slash-commands)
  - [CLI Flags](#cli-flags)
  - [The ! Prefix](#the--prefix)
- [Appendix B: Model Routing Table](#appendix-b-model-routing-table)
  - [Time-Shifting Schedule](#time-shifting-schedule)
- [Appendix C: Token Optimization Techniques](#appendix-c-token-optimization-techniques)
  - [Golden Rule](#golden-rule)
  - [CLAUDE.md size limit](#claudemd-size-limit)
- [Codemap workflow](#codemap-workflow)
  - [When the generator runs](#when-the-generator-runs)
  - [Manual invocation](#manual-invocation)
  - [Edge case handling](#edge-case-handling)
  - [Per-repo opt-in checklist](#per-repo-opt-in-checklist)
  - [Troubleshooting](#troubleshooting)
- [Auto-TOC for large canonical docs](#auto-toc-for-large-canonical-docs)
<!-- generated by toc tool; do not edit by hand -->
<!-- TOC:END -->

## Part I — Reference
*Foundational doctrine — the durable reference chapters (Ch1–Ch14). Read the chapter you need; this part is reference, not a start-to-finish read.*

## Ch1. System Architecture
<!-- scope: meta -->

**`.dev-knowledge` is not a journal and not an orchestrator** — it is **Layer 2**, the passive storage & governance layer of the ADR-28 three-layer ecosystem. The canonical model — the browser-architect → operator → Claude-Code-executor loop, its diagram, the authority chain, and the binding Layer-2 invariants — lives in **`ARCHITECTURE.md` Ch1 "Layer Boundaries & Invariants"** and is **not restated here**: a resident copy is exactly the drift this repo exists to kill (`ARCHITECTURE.md:14`). The copy that used to sit here had gone stale — its diagram showed the browser producing and committing the handoff, the opposite of the canon (`ARCHITECTURE.md:106`: Claude Code, Layer 3, commits the handoff).

The one rule below is **PLAYBOOK-local** — a domain boundary, not layer doctrine (deliberately absent from ARCHITECTURE.md):

- **Separate from Obsidian vault.** Vault = pre-sales domain knowledge (see Section 13). `.dev-knowledge` = dev methodology. Different domains, different audiences, different write paths.

### Cross-reference
<!-- scope: meta -->

Section 13 "Where Knowledge Lives" describes knowledge **domains** (what lives where); the workflow **layers** (how information flows) are canonical in `ARCHITECTURE.md` Ch1 "Layer Boundaries & Invariants". Complementary views of the same ecosystem.

---

## Ch2. CLAUDE.md as agent-instruction contract
<!-- scope: meta -->

**Purpose:** Each repo (corp-monorepo, ai-council, .dev-knowledge, future projects) has a `CLAUDE.md` at root. Auto-read by Claude Code on session start. Auto-read by Codex via `project_doc_fallback_filenames = ["CLAUDE.md"]` in `~/.codex/config.toml`. **Substantive single canonical per-repo agent-instruction file (≤200 lines).** Per ADR-53.

### Authority hierarchy
<!-- scope: meta -->

1. `.dev-knowledge/protocols/ESSENTIALS.md` + `protocols/PLAYBOOK.md` (this file) — universal rules across all Rob's work
2. `{repo}/CLAUDE.md` — per-repo agent-instruction contract (architecture, conventions, tools, ADRs, anti-patterns)
3. `{repo}/.claude/skills/`, `commands/`, `hooks/` — runtime config

### What CLAUDE.md is
<!-- scope: meta -->

- **Single canonical agent-instruction contract** for both Claude Code and Codex operating in this repo
- Repo identity, architecture pointer, conventions, tools active here
- Lists slash commands, skills, hooks ACTIVE in this repo
- Critical rules and anti-patterns specific to this repo
- Recent ADRs binding here

#### Content-distribution map

Where each class of per-repo content lives (v2.1 template, 12 sections):

| Content class | Home |
|---|---|
| Session read order / identity | §1 First read + §2 Repo identity |
| Architecture overview | `ARCHITECTURE.md` — §3 carries a one-line pointer (required, every repo, per ADR-51 as amended 2026-05-23) |
| Conventions (naming, commits, testing, linting) | §4 Conventions |
| Toolchain commands (test/lint invocations) | §4 Conventions |
| Out-of-scope for this repo | §4 Conventions ("Out of scope" sub-section) |
| Critical governance rules | §5 Critical rules |
| Session start checklist | §6 Session start protocol |
| Slash commands | §7 Slash commands available |
| Skills (including gotchas) | §8 Skills active |
| Toolchain enforcement (hooks, pre-commit) | §9 Hooks active |
| Anti-patterns / Do NOT | §10 Anti-patterns |
| Council decisions / ADRs | §11 Recent ADRs |

**Not in CLAUDE.md:** universal rules (`.dev-knowledge/`), architecture docs (`ARCHITECTURE.md`), decision rationale (`docs/decisions/ADR-NN-*.md`).

### What CLAUDE.md is NOT
<!-- scope: meta -->

- Universal rules — those live in `.dev-knowledge/`
- Architecture documentation — that's `docs/ARCHITECTURE.md`
- Decision rationale — that's `docs/decisions/ADR-NN-*.md`

### Why ≤200 lines
<!-- scope: meta -->

CLAUDE.md grows by accretion in most repos, ending as a 1000+ line dump that nobody reads. Cap at 200 lines — overflow goes to dedicated docs (ADRs, PLAYBOOK sections), not back into this file.

corp-monorepo CLAUDE.md (4KB, stale numbers like "24 Council Decisions" when there are 29) is exactly the failure mode this template prevents. <!-- intentional stale example illustrating anti-pattern; do not "fix" -->

### LLMs advise; hooks/tests enforce
<!-- scope: meta -->

CLAUDE.md tells the LLM what to do/avoid. Tach, pre-commit hooks, pytest, Codex /review enforce mechanically. Don't put rules in CLAUDE.md that aren't backed by enforcement somewhere — they'll drift.

### Drift-proofing precedence: source → gate → agent
<!-- scope: meta -->

Generalizes "LLMs advise; hooks/tests enforce" into a precedence rule for *where* a rule should live so it can't rot. Prefer the earliest tier that can hold the rule — each beats the next on durability and cost:

1. **Source** — make the fact self-documenting so it has nothing to drift from: derive it from code (e.g. `audit.py checks` reads `ALL_CHECKS`), single-source the canon, auto-generate the artifact (codemap, TOC). No separate copy, no drift.
2. **Gate** — for what can't be made self-documenting, add an active enforcement gate (pre-commit hook, test, `verify:` line). A lesson that isn't always-loaded doesn't fire; a gate fires every commit.
3. **Agent** — for what neither covers (semantic conformance, judgment, prose drift), an agentic review is the safety net (the ADR-70 Tier-3 / BACKLOG #81 conformance workflow).

Reach for a gate only when the fact can't be self-documented, and an agent only when it can't be gated. (Codified 2026-06-03; precedent for promoting a session-decided principle into PLAYBOOK: the v4.2 "handoff is back-and-forth" promotion.)

### Child methodology floor (ADR-78)
<!-- scope: meta -->

Each registered child repo carries a generated `.claude/CLAUDE-FLOOR.md` (≤1,500 tokens, conformance-enforced) plus a `.claude/CLAUDE-FLOOR.md.sha256` sidecar — under the child's own CC config dir, not the repo root (keeps the operator's workspace uncluttered); the child's `CLAUDE.md` references it via an `@.claude/CLAUDE-FLOOR.md` import (verified empirically: CC 2.1.168 resolves `@`-includes at session start, transitively, and degrades fail-soft on a missing target). The floor is the always-loaded methodology baseline (prompt-header, valve discipline, verify cadence, ship rule, context budget, safety pointers) so a child session carries the working style without depending on a bundle upload. It is **self-contained** — no hub-internal references (ADR-72 class); the `.dev-knowledge` hub appears only as a labeled, optional depth escape-hatch (ADR-78 Decision 1).

- **Generator (`scripts/generate_floor.py`) is operator-invoked ONLY** at rollout moments (ADR-73). Never a hook, never scheduled, no autonomous cross-repo writes — the operator runs it and commits the floor *in the child repo*. `generate --out-dir <child>` writes the floor + sidecar into the child's `.claude/` (creating it if absent), prints the complete install note (the `@`-include line, the child-side hash-verify hook + its `pre-commit install` arming step, and `git checkout HEAD --` tamper-revert — all baked from the 2026-06-08 pilot), and refreshes the hub canonical hash; `check` validates without writing. Output is deterministic so the hash is meaningful.
- **Token ceiling is hard at 1,500** (ADR-78 §4). The binding measure is the conservative `ceil(chars / 3.5)` heuristic (deterministic, dependency-free); a real tokenizer is informational only. Exceeding it is a generation refusal — trim content, never the rule.
- **Conformance (source → gate → agent):** the template is the source; `audit.py floor_integrity` (hash vs sidecar + F5 self-containment grep + same-repo pointer existence) and the child pre-commit sidecar-hash hook are the gates; `/ship` warns (advisory, never blocks) when a child's floor hash is stale vs the hub canonical hash.
- **Re-anchor rule:** the floor instructs a session to re-read the floor before any *structural* change (architecture, governance, multi-file refactor, new abstraction) and to trust session-persisted context for ordinary work — a cheap per-structural-action re-anchor without a per-action cost.

### Template
<!-- scope: meta -->

See `templates/CLAUDE-md-template.md` for the canonical 12-section skeleton (≤200 lines).

### Update cadence
<!-- scope: meta -->

CLAUDE.md updates when:
- New ADR is binding (Recent ADRs section §11)
- New slash command adopted (Slash commands section §7)
- New skill adopted or gotcha promoted (Skills section §8)
- New hook added (Hooks section §9)
- New slash command, skill, or hook added (§7, §8, or §9 as applicable)
- PLAYBOOK.md restructure (update First read section §1 paths)

**Architecture changes go in `ARCHITECTURE.md`** — CLAUDE.md §3 is a static pointer that needs no edit when architecture changes.

**Stale CLAUDE.md = agents operating on outdated context every session.** Treat updates as part of the change that triggered them.

### Length notes
<!-- scope: meta -->

CLAUDE.md length scales with repo complexity (advisory, not gated): a small repo may need only 50-100 lines (less infrastructure); a larger repo with rich tooling and more binding ADRs approaches but does not exceed the 200-line cap.

If CLAUDE.md grows past 200 lines, split content to dedicated docs; only per-repo governance stays here.

### Handoff scope
<!-- scope: meta -->

CLAUDE.md is an agent-instruction contract, not a repo-descriptive document. The Claude-oriented handoff process must not narrate, summarize, or manage CLAUDE.md as Claude-side repo-descriptive handoff content. See ADR-53.

### LLM-LLM context transfer is back-and-forth, not unilateral
<!-- scope: meta -->

When transferring context across LLM boundaries — handoff bundles, chat-to-chat
references, browser-to-CC interactions, CC-to-Codex review handovers — the sender
verifies load-bearing claims inline (via tool calls or a colleague-LLM) rather
than carrying forward "unknown" or "I think this was true earlier." The receiver
asks back before unilateral interpretation. This emerged from the v4.1 handoff
first run (2026-05-29), where the sender carried "aborted folder preserved" as
witnessed when it was actually recalled-from-earlier-session — Phase 2 verification
caught the drift, but the upstream discipline avoids the drift in the first place.

Applies broadly: not just to handoff process.

### Process versioning: beta vs stable promotion
<!-- scope: meta -->

Processes (like HANDOFF_PROCESS, AI_COUNCIL_PROCESS) ship at status `beta` after
design + first end-to-end implementation. Promotion to `stable` requires one
independent fresh-eyes review (LLM chat with zero project context, given the
artifact + a meta-reviewer prompt) with **both** of:

1. **Mechanical condition:** Stage 1 returns **fewer than 2 critical findings**
   (severity 4-5/5)
2. **Judgment condition:** reviewer's Stage 3 verdict is **PROMOTE** or **PROMOTE
   WITH CAVEATS** (caveats logged to BACKLOG)

**Override:** if reviewer judgment recommends DO NOT PROMOTE despite <2 critical
count, reviewer judgment wins (next refinement cycle). This honors **hard-metric >
easy-metric**: count is a proxy for convergence judgment, not a replacement.

Triangulation guards process versioning. Routine artifacts produced by the process
rely on operator review + structural self-verification — adversarial per-artifact
review is a separate concern.

No Council convene required for promotion (operator's call). Council remains the
right venue for ratifying the architectural decision behind a process, separately
from quality promotion.

---

## Ch3. Repo conventions
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-26 -->

Universal repo-level conventions binding across all Rob's repos. Each convention's **canonical home is its ADR** (ADR-30/34/59/60); the subsections below are **pointers** to those ADRs — except where the rule is PLAYBOOK-canonical (the `main` migration *procedure*; the root-hygiene *caveats* ADR-59 references back into PLAYBOOK) or a `[TBD]` forward-reference. Concrete enforcement happens via Claude Code, Codex, hooks, `scripts/audit.py`, and reviewer judgment. (#158, 2026-06-15: pointerized the subsections whose doctrine is fully in an ADR; retained the genuinely PLAYBOOK-canonical ones with reason.)

### Default branch — `main`
<!-- scope: dev -->
<!-- version: 1.0 — 2026-04-26 -->

**Rule:** Every Rob's repo uses `main` as the default branch. No exceptions. Per ADR-30.

> Decision + rationale are canonical in **ADR-30**; the operational migration procedure below is **PLAYBOOK-local** — ADR-30 carries only a one-line summary of it (#158: retained, not pointered).

**New repos:**
- `git init -b main`, or set `init.defaultBranch = main` in `~/.gitconfig` so `git init` always lands on `main`
- When creating on GitHub UI, default already correct

**Existing repos still on `master`:**

Procedure (Phase 1 = file changes on feature branch; Phase 2 = destructive remote ops):

Phase 1:
1. Grep entire repo for hardcoded `master` in CI workflows, hooks, scripts, docs. Update any found alongside the rename
2. Update any docs naming the default branch by name (e.g. JOURNAL entries; CHANGELOG retired — §14)

Phase 2 (destructive — explicit confirm before each):
3. Local rename: `git branch -m master main`
4. Push `main`: `git push -u origin main`
5. Set remote HEAD: `git remote set-head origin main`
6. Delete origin/master: `git push origin --delete master`
7. GitHub repo Settings → Branches → default branch = `main` (manual UI step if step 5 didn't cover it)

**Anti-patterns:**
- Phase 2 without grep step from Phase 1 → CI breaks post-rename
- Renaming on remote without local rename first → divergent state
- Skipping the GitHub default branch UI update → next PRs target the deleted ref

### File naming conventions
<!-- scope: meta -->

Per ADR-34 (ratified 2026-04-29, amended 2026-05-11). Canonical source: `docs/decisions/ADR-34-file-naming-convention.md`. Key rules: hyphen separator universal across filenames and foldernames; `ADR-NN-topic.md` for decisions; `council-out-YYYYMMDD-HHMMSS-topic.md` for Council CLI output; `DECISION_NN_*` legacy transcripts grandfathered; kebab-case + ISO date for audits/handoffs; UPPERCASE for living docs.

### Folder structure
<!-- scope: meta -->

Canonical: **ADR-60** (the two-variant `docs/` taxonomy — `.dev-knowledge` vs child-repo) + its 2026-05-28 addendum (child-repo baseline always-present) + **ADR-38 A5** (mandatory root files). Not restated here — see the docs/ folder taxonomy pointer below for the same canon at finer grain.

### Root hygiene convention
<!-- scope: dev -->
<!-- version: 1.0 — 2026-05-23 -->

**Goal:** keep the repo root visually clean (low cognitive overhead) without breaking tooling defaults.

**Consolidate tool configs into `pyproject.toml`** where supported, instead of standalone files at root:

- `[tool.ruff]` (instead of `ruff.toml`)
- `[tool.pytest.ini_options]` (instead of `pytest.ini`)
- `[tool.mypy]` (instead of `mypy.ini`)
- `[tool.tach]` if Tach supports pyproject embedding (verify per Tach version); else keep `tach.toml` at root

> Caveat: only consolidate when a `pyproject.toml` already exists or the repo is a code project. A governance-only repo with no `pyproject.toml` should NOT create one solely to absorb a single `ruff.toml` — that adds a root file rather than removing one, defeating the goal. In that case keep the standalone config.

**Dot-prefix workspace files:** rename `<repo>.code-workspace` to `.<repo>.code-workspace` — hides it from default `ls` while preserving VS Code "Open Workspace" functionality.

**Files that MUST remain at root** (tooling defaults; moving creates friction):

- `pyproject.toml`, `.gitignore`, `.gitattributes`, `.pre-commit-config.yaml`, `.editorconfig`, `.git/`

**Files that CAN move to subfolders:**

- SVGs and rendered diagrams → `docs/diagrams/` or `_assets/`
- Standalone scripts → `scripts/`
- Test fixtures → `tests/fixtures/`

### Additional root hygiene rules (added 2026-05-24, root hygiene pass 2)
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-24 -->

**`.env.example` policy: do not create.** Standard practice in many projects is generating `.env.example` as a template for required environment variables. In this repo's workflow, this is unnecessary clutter — environment variable docs live in CLAUDE.md / ENVIRONMENT.md / VISION.md as appropriate. Do not auto-generate `.env.example` files.

**Dot-prefix where tool supports.** If a config file MUST live at root (tool defaults to root discovery), prefer dot-prefixed variant if the tool accepts both:
- Ruff: `.ruff.toml` (instead of `ruff.toml`) — supported per Ruff docs ✓ applied 2026-05-24
- pre-commit: `.pre-commit-config.yaml` — standard name, already dot-prefixed
- ESLint: `.eslintrc.json` (instead of `eslintrc.json`) — already dot-prefixed convention
- pytest: must be `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` — no dot-prefix variant
- Tach: `tach.toml` — verify movability per tool version before assuming dot-prefix works

**`.env` placement.** If `.env` is required by tooling: stays at repo root (dot-prefixed convention preserved). If only used by scripts that accept configurable env-file path: prefer `.config/.env` or similar subfolder placement.

**No `files.exclude` to hide root config files.** Operator preference: VISIBILITY of what tools are configured matters. Do not use VS Code `files.exclude` settings to hide config files from Explorer — defeats the purpose of seeing what's configured. Apply dot-prefix instead where supported.

### Universal visual pattern (per ADR-59)
<!-- scope: dev -->

Canonical: **ADR-59** Decisions 1–4 + its amendments. The three audit-enforced pillars — **dot-prefix discipline** (+ the un-dotted exception list, incl. the 2026-06-02 `pytest.ini` addition), **ALL-CAPS canonical `.md` visibility** (incl. the 2026-06-01 `logs/TOKEN-LOG.md`-under-`logs/` clarification), **workspace sort** (`lexicographic: upper` + `sortOrderReverse: true`, per the 2026-05-27 amendment) — the adopt-a-new-tool maintenance rule, and the date-sorted-folder note all live in the ADR. Enforced by `scripts/audit.py` (`dot_prefix_discipline` / `canonical_md_visibility` / `workspace_settings`; `audit.py health` surfaces drift). Not restated here (#158: the pillars are fully codified in ADR-59).

### docs/ folder taxonomy (per ADR-60)
<!-- scope: meta -->

Canonical: **ADR-60** + its 2026-05-27 amendment (repo-type variants) + 2026-05-28 addendum (child-repo baseline always-present). Covers, all in the ADR — the two-variant folder tables (`.dev-knowledge` carries `decisions/`+`audits/`+`handoffs/`+`archive/`; child code repos carry `decisions/`+`audits/`+`archive/`+`diagrams/`, no `handoffs/`), the `archive/` triage-zone semantics, the file-placement rules (entry-scripts → `scripts/`; root-exception configs `pyproject.toml`/`tach.toml`/`requirements.txt`), and **Rule 5 — append-only/immutable records are not rewritten on move** (ADRs, transcripts, handoffs, `JOURNAL`/`LESSONS` are point-in-time history; update only living docs + the moved file's own cross-refs; repo critical rules #2/#3). Not restated here (#158: the taxonomy + Rule 5 are fully in ADR-60).

### Secrets storage path
<!-- scope: meta -->

**[TBD — Stream C session 3, ADR-33]**

Standardize location of `.secrets/` (currently `C:\Users\1028120\Documents\.secrets\.env` per Rob's environment, not yet PLAYBOOK-documented as standard). Rule covers: path convention, what kinds of repos use this, whether per-repo `.env` is allowed, how the global PowerShell profile auto-loads relate.

### Capitalization conventions
<!-- scope: meta -->

**[TBD — Stream C session 3, ADR-34]**

File and folder casing rules. Currently mixed: `LESSONS.md` ALLCAPS, `docs/` lowercase, `ESSENTIALS.md` ALLCAPS, kebab-case for dated files. Decision on what casing applies where, and whether existing files migrate.

### Rule-ID naming convention (doc to code edge)
<!-- scope: meta -->

How an enforced rule is named so the `doc_code_edge` advisory check (ADR-89 OQ1) can resolve its doc declaration to its code teeth. All example tokens below use the angle-bracket **placeholder** form on purpose (see the last bullet).

- **Form:** `<domain>-<slug>` — lowercase kebab, charset `[A-Za-z0-9_.-]+`, **semantic not numeric** (the ID reads as *what the rule governs*, not an opaque counter). Doc side: `<!-- rule: <domain>-<slug> -->`; code side: `# rule: <domain>-<slug>` (a real comment token, never inside a string). The ID is the identity on both sides, so the edge is **move-safe** — the resolver re-finds the code token by content; moving the file does not fire `broken_edge`.
- **`<domain>` = a cited theme/source, NEVER a location.** The allowed tokens each cite an existing source (a BACKLOG serialize-group / theme / ADR domain): `seal`, `coherence`, `canonical`, `governance`, `handoff`, `dep`, `tooling`. **Extend by cited append** — add a token that cites a source; "do not invent domains" means "cite a source," not "never add one" (no ADR rewrite to extend).
- **Only a rule with live code enforcement gets an ID** (the edge presupposes a code site). **IDs are unique and never reused** after retirement — a retired ID stays burned, like a departed BACKLOG id.
- **Declare at the authoritative source, never in a summary.** The doc-side token lives where the rule is *authoritatively declared*, never on a doc that merely *summarizes* it (e.g. `seal-journal-anchor` is declared in `DEFINITION_OF_DONE.md` — ADR-85's single-source — not in the ESSENTIALS summary of it). The scanned declaration docs are an include-list registry, `ecosystem/doc-code-edge.yaml` (`declaration_docs:`); a doc joins it when it first authoritatively declares an enforced rule (the same cited-append extensibility as the domain namespace).
- **Illustrative vs live (the self-trip guard):** every example token in teaching prose uses the angle-bracket placeholder form `<!-- rule: <domain>-<slug> -->`. `<` / `>` are outside the ID charset, so a placeholder is never matched as a live edge — this section cannot self-trip the scan. Live tokens sit only at a rule's authoritative doc site + its code site.

Full doctrine + reversibility: **ADR-89 OQ1 "NAMING CONVENTION — ADOPTED"**. Advisory-first; a hard-gate promotion is a later data-gated arc.

---

## Ch4. Writing prompts for Claude Code
<!-- scope: meta -->

**Purpose:** Standardize prompts that browser chat produces for Claude Code execution. Per ADR-28 (three-layer architecture): browser is architect, Claude Code is executor — prompts are the contract between them.

> **Cross-ref (ADR-87):** the architect↔CC equilibrium contract refines this — the architect emits intent + plan/auto mode + a thin governance-pointer, and CC self-loads code-impact context + generic gotchas. See §2 "Creating a Claude Code Prompt" / ADR-87. **Overlap flag:** this section and §2 both cover prompt authoring and both predate ADR-87 — candidate for a later focused consolidation (flagged only; not done here).

### Why standard format
<!-- scope: meta -->

Without standard structure, prompts diverge:
- Different naming for same fields (Model vs LLM, Effort vs Difficulty)
- Inconsistent COMMIT markers — Claude Code can't tell when to commit
- Missing UNDERSTAND section → Claude Code makes wrong assumptions
- Polish prompts → Claude Code outputs Polish (per ESSENTIALS line 25, prompts are English-only)
- Inline code blocks → can't be saved as artifact, breaks asynchronous workflow

Vibe Code 4 (2026-04-22) established the standard structure during Stream A. This section codifies it as PLAYBOOK protocol.

### Standard structure (8 sections)
<!-- scope: meta -->

1. **Model/Mode/Effort table** — `| Model | Sonnet | / | Mode | plan-then-auto | / | Effort | medium |`
2. **Title** (imperative, what gets accomplished)
3. **Repo + Purpose** (absolute path + one-sentence outcome)
4. **Read first** (CLAUDE.md, gotchas, relevant docs)
5. **Git workflow** (branch + commit cadence + merge command)
6. **UNDERSTAND** (problem, what could break, most likely failure mode)
7. **Steps with COMMIT markers** (numbered, each ends with conventional commit message)
8. **Final + What NOT to do** (verification + merge + anti-patterns)

Template: `templates/prompt-template.md`

### Per-Scale guidance
<!-- scope: meta -->

- **Scale S** (single file, <50 lines change): use minimal version — Title + Steps + What NOT to do. Skip UNDERSTAND if change is mechanical.
- **Scale M** (multi-file): full template, but UNDERSTAND can be 1-2 sentences.
- **Scale L** (3+ files, architectural): full template required, prefer `plan-then-auto` mode for review checkpoint after Step 1.

### Delivery format
<!-- scope: meta -->

Prompts are **downloadable `.md` artifacts**, not inline code blocks. Browser chat outputs them as fenced markdown blocks; Rob saves as file, then pastes file content into Claude Code's prompt field.

Why: pasted-as-text is fine, but file form preserves structure for re-use, audit, and handoff.

### Pre-send checklist
<!-- scope: meta -->

Before delivering a prompt to Claude Code, verify:

- [ ] **English only** — no Polish in prompt body (Rob speaks Polish; prompts are English per ESSENTIALS)
- [ ] **Model/Mode/Effort table** present at top — embedded **verbatim** from the non-negotiable spec, never paraphrased (#25)
- [ ] **Absolute paths** for all repo/file references (not relative — Claude Code's CWD varies)
- [ ] **Read first** lists CLAUDE.md and gotchas (always) plus task-relevant docs
- [ ] **Git workflow** specifies branch name, commit cadence, merge command
- [ ] **UNDERSTAND section** answers: what's the problem? what could break? most likely failure mode?
- [ ] **Steps numbered** with imperative titles ("Create X" not "Creating X")
- [ ] **COMMIT markers** end each step (or explicit "no commit" if grouping)
- [ ] **What NOT to do** lists at least 3 anti-patterns specific to this task
- [ ] **Final** has concrete verification commands and merge command
- [ ] **Out-of-scope items explicit** (e.g., "Do NOT touch corp-monorepo")
- [ ] **No `!` shortcuts** for state-changing git operations (per Vibe Code 4 protocol)
- [ ] **Versioning if applicable** — sections in repo files include `<!-- version: X.Y -->` for amendment tracking

**Judgment checks (knowledge-application, not just form — #34 / 2026-06-06 application-skipped misses):**

- [ ] **Review applicability (two-stage)** — does the diff touch 3+ code files or anything safety-critical? If so, plan the two-stage code review: `/code-review high` for an in-flight/interim pass, then `/codex-review` as the final pre-merge pass (code only — doc-only diffs skip both)
- [ ] **Context-budget pass** — every read instruction is scoped (no "read the whole repo"); per §7 read-scoping rule
- [ ] **JOURNAL-read needed?** — does the task need recent session continuity (last few JOURNAL entries) to avoid re-deciding settled things?
- [ ] **Inherited-framing counter-check** — *"Have I assumed any operator decision as resolved that the operator has not actually ruled on?"* (origin: a floor/rollout assumption treated as settled while still pending)

Skip checklist items only when not applicable to specific task type. If unsure, include them.

### Anti-patterns
<!-- scope: meta -->

- **Polish prompts** — even if Rob asks in Polish, prompt body is English
- **Inline `!` git commits** — Claude Code commits via explicit Bash steps, not shortcuts
- **Missing UNDERSTAND** — Claude Code without context makes wrong assumptions, especially on Scale L
- **Unclear out-of-scope** — Claude Code expands work; explicit "Do NOT touch X" prevents
- **Relative paths** — break when CWD shifts between repos

### Checkable rules: concrete over aspirational
<!-- scope: meta -->

A rule a model can *check its own output against* gets followed; a rule it can
only *aspire to* gets broken — even when the model can recite it. Traces show
models that correctly explain "keep functions small" still ship 80-line
functions: the vague form gives the output nothing to be tested against, so
nothing stops the drift. Phrase every rule — in prompts AND in CLAUDE.md — so
compliance is a yes/no check against a number, an enumerable set, or a named
artifact, not a feeling.

**The test for your own rule:** could a second reader (or the model itself) mark
it pass/fail *without re-using your judgment*? If grading the rule needs the same
taste the rule was meant to encode, it's aspirational — rewrite it.

**Vague → checkable rewrites:**

| Aspirational (drifts) | Checkable (holds) |
| --- | --- |
| "clean code" | "functions ≤ 50 lines; every public symbol has a docstring; no module > 500 lines" |
| "be concise" | "summary ≤ 5 bullets; no bullet > 2 lines" |
| "good test coverage" | "every public function has ≥ 1 test; `pytest --cov` ≥ 60% on `src/`" |
| "handle errors properly" | "no bare `except:`; every `except` names a concrete type and logs before re-raising" |
| "keep docs current" | "TOC matches headers (toc-freshness hook green); `last_reviewed` ≥ the file's last-edit date" |

Keep the *why* in prose where it helps the model reason, but make the **bar** a
thing it can measure. A rule that can't go red is decoration. (Companion: the
circular-testing guard under "Testing rules" — a *test* that can't go red has the
same defect.)

### Update cadence
<!-- scope: meta -->

Prompt format updates when:
- New common failure mode discovered → add to "What could break" guidance
- New repo with different conventions → may require template variant
- ADR amendment changes prompt protocol (e.g., new git workflow standard)

This section's history is in git log (search commits for "prompt template" or "Gap #2").

---

## Ch5. Project complexity bands
<!-- scope: dev -->

> **Repo-tier system DEPRECATED 2026-05-23.** The formal S/M/L tier system — a declared `tier:`/`scale:` per repo that gated governance baselines — is deprecated ecosystem-wide (operator decision 2026-05-23; see ADR-33 amendment, ADR-38 amendment A5, ADR-40 deprecation). Repos no longer **declare** a tier, and no governance obligation is gated on one. The universal governance baseline (ADR-38 A5) applies to every repo regardless of size. The tier-*transition* procedures (S→M, M→L triggers/steps, formerly a subsection here under ADR-40) are likewise retired and **not re-introduced** — there is no tier to transition between and no score is computed.

The S/M/L labels below survive only as **informal complexity descriptors** — shorthand for "how big is this repo" used to calibrate judgment (how much test infrastructure, how rich a workspace), not as a declared, audited tier:

- **large** — multi-package repo, hundreds+ of tests, cross-package dependencies.
- **medium** — standalone package, dozens-to-hundreds of tests, multiple modules.
- **small** — single script or tool, few tests, simple flow.

These are bands on a continuum, applied by judgment. Guidance below that references them is advisory calibration, not a tier mandate. (Distinct from the *task-complexity* S/M/L sizing used to size Claude Code prompts in `templates/prompt-template.md` — that taxonomy is unaffected by this deprecation.)

### Testing rules (scaled by repo complexity)
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-23 -->

Test infrastructure scales with project size. Over-investing in test infra on a tiny single-script repo wastes effort; under-investing on a large repo creates fragility. The bands below are advisory calibration (per the complexity descriptors above), not tier mandates.

| Repo size | Minimum | Coverage target | Test types | Run command |
|-------|---------|-----------------|------------|-------------|
| **small** (<50 tests) | optional | n/a — coverage measurement overhead exceeds value | smoke tests at most | `pytest` (single run) |
| **medium** (50-500 tests) | required | ≥60% on source, no untested public API | pytest unit + selective integration | `pytest -x --tb=short` |
| **large** (500+ tests) | required | ≥80% on source, comprehensive public API coverage, integration suite for critical paths | pytest unit + integration + e2e where applicable | `pytest -x --tb=short` per step + `pytest --collect-only` for sanity |

> Coverage targets (60%/80%) are guidelines from observed practice, not enforced thresholds.

#### Reading the table
<!-- scope: dev -->

- **required** — tests must exist and pass before merge; CI/CD enforces
- **optional** — tests welcomed but not blocking; useful when complexity warrants
- **n/a** — measurement overhead exceeds practical value at this scale

#### Per-step test cadence (any repo with a test suite)
<!-- scope: dev -->

Per `templates/prompt-template.md` and PLAYBOOK "Writing prompts for Claude Code" section:

After every numbered step in a Claude Code prompt:
1. `pytest -x --tb=short` — fail fast, short tracebacks
2. `ruff check src/ tests/ --fix` — autofix lint issues
3. `git status` — verify expected file scope

This cadence catches regressions early and keeps each commit's diff sane to review.

#### Tests derive from acceptance criteria, not the implementation (circular-testing guard)
<!-- scope: hybrid -->

A test written *from the implementation* only proves "the code does what the code
does" — it re-states the behavior it was meant to challenge, so it passes by
construction and can never go red on a real defect. The architect breaks the
loop: **acceptance criteria are authored in the prompt (in UNDERSTAND or a step's
success line), and Claude Code derives the test FROM those criteria — never from
the code it just wrote.**

**Teeth check (companion to checkable rules):** before trusting a green test, ask
*"what one-line change to the implementation would make this go red?"* If the
honest answer is "none" — the assertion pins the implementation's current shape,
not the criterion — the test has no teeth. Add an assertion that fails when the
criterion is violated, even if today's code happens to satisfy it.

**Worked example — this session's #141 vacuous claim-3 test (the live case this
guard would have flagged):** the `pytest_collected` claim-check test was meant to
prove claim-3 actually *evaluated* on the expensive path, but its assertion was
`status != "skipped" or actual`. The intent was "require a non-skip" — yet the
`or actual` clause let a *skipped* result pass whenever `actual` was non-empty,
and a skipped result always carries a non-empty `actual` string. So the test
could not distinguish "claim-3 evaluated and matched" from "claim-3 silently
skipped"; it went green either way. (A preceding
`assert status in {"mismatch", "match", "skipped"}` accepted all three states,
asserting nothing.) It pinned the implementation's reachable states instead of
the criterion (claim-3 *must* evaluate). The fix grew teeth: a deterministic mock
of the pytest subprocess so the deriver actually runs, then
`assert status == "match"` **and** `assert status != "skipped"` (the second, now
un-weakened, rejects the vacuous skip-pass), with the genuine infra-skip path
moved to a *separate* test so neither masks the other
(`tests/test_validate_doc_claims.py::test_reconcile_evaluates_test_count_when_expensive`).

The rule: a test must be able to distinguish "criterion met" from "criterion
silently not evaluated." If it can't, it is testing the implementation, not the
acceptance criterion.

#### Test types and when
<!-- scope: dev -->

- **Unit tests:** any repo with non-trivial logic. Mock external dependencies. Fast feedback (<10s per file).
- **Integration tests:** for critical paths on larger repos (e.g. data pipeline, auth flow). Real dependencies, isolated DB, slower (1-30s per test).
- **E2E tests:** for top user journeys on larger repos. Real environment, optional in standard CI (run nightly or pre-release).
- **Smoke tests:** minimum bar for a small repo — "did basic flow break?" Single-file pytest, optional CI.

#### Anti-patterns
<!-- scope: dev -->

- **Coverage chasing on a tiny repo** — measuring coverage on a <50-test repo wastes 30+ min per session for diminishing return
- **Skipping tests on a large repo** — "this commit is small" + large repo = recipe for hidden regression
- **Integration-only on a large repo** — slow feedback discourages running tests; unit tests are the foundation
- **Implementation-derived tests** — writing the assertion from the code instead of the prompt's acceptance criteria proves only "the code does what the code does"; it can't go red on a real defect (see "Tests derive from acceptance criteria" above; #141's vacuous skip-pass is the live case)

### VS Code workspace
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-23 -->

Each repo has a `.code-workspace` file at root that VS Code uses for project-specific settings and recommended extensions. Three templates of increasing richness ensure baseline consistency without preventing repo-specific customization — pick the one matching the repo's complexity (the S/M/L suffixes are richness levels, not declared tiers).

**Templates location:** `.dev-knowledge/templates/workspace-{S,M,L}.code-workspace`

**Bootstrap workflow:**
1. Copy the template matching repo complexity: `cp .dev-knowledge/templates/workspace-S.code-workspace <repo>/<repo-name>.code-workspace`
2. Rename to match repo name (e.g. `corp-monorepo.code-workspace`)
3. Edit `folders` array if multi-folder workspace needed (rare)
4. Add repo-specific settings/extensions on top of template baseline
5. Commit `.code-workspace` to repo root (yes, commit it — workspace config is part of dev environment)

#### Minimal (small repos)
<!-- scope: dev -->

For small repos (<50 tests, single script/tool, simple flow):

**Settings:**
- Python interpreter via `.venv/`
- Ruff format-on-save with import organization
- Trailing whitespace cleanup, final newline
- Editor rulers at 88 (Ruff default) and 120

**Extensions:**
- ms-python.python — Python language support
- charliermarsh.ruff — linter + formatter

That's it. No testing infra, no git tooling, no diagram support — a small repo doesn't need them.

#### + testing & git tooling (medium repos)
<!-- scope: dev -->

For medium repos (50-500 tests, standalone package, multiple modules):

**Adds to the minimal set:**
- pytest test discovery (`python.testing.pytestEnabled`)
- GitLens (eamodio.gitlens) — git history, blame
- Error Lens (usernamehw.errorlens) — inline diagnostics
- TODO Tree (gruntfuggly.todo-tree) — surfaces TODO/FIXME comments

**Why these:** on a medium repo, test infrastructure is worthwhile (per Testing rules subsection above), and git/error tooling becomes worth setup cost.

#### Full stack (large repos)
<!-- scope: dev -->

For large repos (500+ tests, multi-package monorepo):

**Adds to the medium set:**
- mypy type checking (`python.analysis.typeCheckingMode: "basic"`)
- mypy type checker extension (ms-python.mypy-type-checker)
- TOML support (tamasfe.even-better-toml) — for tach.toml, pyproject.toml, etc.
- Spell checker (streetsidesoftware.code-spell-checker)
- Mermaid diagram preview (bierner.markdown-mermaid)
- TODO Tree extended tag list

**Real example:** `corp-monorepo.code-workspace` (a large repo, currently active) reflects this template with corp-monorepo-specific additions.

**Why these:** on a large repo, architecture diagrams (Mermaid) and type discipline (mypy) become high-leverage. TOML editing matters for Tach, pyproject.toml monorepo-wide configs.

#### Customization
<!-- scope: dev -->

Template is starting point, not contract. Repos may:
- Add project-specific extensions (e.g. corp-monorepo adds Tach extension if available)
- Tighten settings (e.g. require strict type checking instead of basic)
- Override interpreter path for non-standard venv locations
- Add custom tasks, debug configurations, multi-folder workspaces

**Don't:** remove template baseline without rationale — that's diverging from baseline, not customizing on top of it.

---

## Ch6. Documentation file types and session continuity
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

Two related questions: **what does each documentation file do** (Gap #4) and **which files a repo carries** (Gap #18; file presence is now universal, not tier-gated — see below). Combined here because they answer "when I need to write something down, where does it go?"

### File type taxonomy
<!-- scope: meta -->

| File | Purpose | Format | Cadence | Audience | Order | Scope |
|------|---------|--------|---------|----------|-------|-------|
| `README.md` | User-first navigation, what is this repo | Prose + folder layout | When repo state shifts notably | Rob, future contributors | Living (rewrite) | Per-repo |
| `CLAUDE.md` | Single canonical agent-instruction contract for Claude Code + Codex; per-repo specifics (architecture, conventions, active tools, binding ADRs, anti-patterns) ≤200 lines | 10-section template | When ADRs, tools, architecture, or gotchas change | Claude Code (auto-read), Codex (via project_doc_fallback_filenames) | Living (sections updated) | Per-repo |
| `ESSENTIALS.md` | Rob's daily cheat sheet, universal | Sectioned, scope-tagged | When Rob's working style evolves | Rob + every browser/Claude Code session | Living (sections updated) | Universal (`.dev-knowledge` only) |
| `PLAYBOOK.md` | Universal protocols, this file | Sectioned, scope-tagged, versioned | Per Stream B implementation gaps | Rob + Claude (browser + Code) | Living + section history | Universal (`.dev-knowledge` only) |
| `JOURNAL.md` | Tactical per-session log | Append-only, dated entries: Did/Failed/Next | Every Claude Code session | Future Claude Code (last 5 entries on startup) | Newest-first prepend | Per-repo (optional; kept when a repo benefits from a per-session log) |
| `CHANGELOG.md` | RETIRED ecosystem-wide (ADR-49) — git history + JOURNAL `Changes:` line replace it; row kept for legacy context | Newest-first dated entries | n/a | — | n/a | Removed |
| `LESSONS.md` | Process lessons learned | Append-only with `[scope: X]` inline (per ADR-29) | When new lesson emerges (auto-promote at 2× repeat) | Rob, future Claude | Append-only | Universal (`.dev-knowledge` only) |
| `logs/TOKEN-LOG.md` | Claude usage snapshots | Threshold-triggered (7-day) via /session-summary | Auto when stale | Rob | Newest-first (prepend) | Universal (`.dev-knowledge` only) |
| `ENVIRONMENT.md` | Tooling state, what's installed | Sectioned, scope-tagged | When tool adopted/deprecated | Rob, Claude Code | Living (sections updated) | Per-repo |
| `docs/decisions/ADR-NN-*.md` | Architectural decisions | Michael Nygard format | When decision binds | Rob, future contributors | Numbered, immutable (amend in-place per ADR-29) | Per-repo |
| `docs/decisions/transcripts/council-out-*.md` | Raw Council debate outputs (canonical; legacy `DECISION_NN_*` grandfathered in `transcripts/archive/legacy/`) | Multi-model debate transcript | When Council debate concludes (routed per ADR-43; manual fallback per §5) | Reference for ADR rationale | Numbered, immutable | Per-repo |
| `docs/handoffs/YYYY-MM-DD-*/` (v5.2 bundle) | Chat-to-chat session summary | Flat bundle entered via `HANDOFF_BOOT.md` (operator session entry) + CC-owned residual/probe-manifest, per HANDOFF_PROCESS v5.2 (ADR-82); legacy v4 `README.md` + `01_ROLE`…`07_ASK_BACK`, single-file, and v3.x `contents/` bundles preserved as history | When session boundary requires continuity | Next browser chat | Dated, immutable | `.dev-knowledge` only |
| `docs/audits/YYYY-MM-DD-*.md` | Point-in-time analyses | Free-form audit | When deep analysis needed | Reference for follow-up work | Dated, immutable (mark SUPERSEDED if redone) | Per-repo |

### File presence (universal baseline)
<!-- scope: meta -->

File presence is no longer gated per tier (repo-tier system deprecated 2026-05-23). The universal governance baseline (ADR-38 amendment A5) applies to every repo regardless of size:

| File | Status |
|------|--------|
| `VISION.md` | mandatory (ADR-33, amended frontmatter) |
| `CLAUDE.md` | mandatory (ADR-31 / ADR-53) |
| `ARCHITECTURE.md` | mandatory (ADR-51 amended 2026-05-23; root placement per ADR-38 A3) |
| `BACKLOG.md` | mandatory (ADR-41) |
| `README.md` | optional — external-audience repos only (deprecated from baseline) |
| `CHANGELOG.md` | removed — superseded by ADR-49 |
| `JOURNAL.md` | optional — kept when a per-session log helps |
| `ENVIRONMENT.md` | optional — kept when tooling state is worth tracking |
| `docs/decisions/`, `docs/audits/`, `docs/archive/` | universal under the 2026-05-27 ADR-60 amendment (see taxonomy above) |
| `docs/handoffs/` | `.dev-knowledge` only (canonical home for handoff bundles) |
| `docs/diagrams/` | child code repos, where architecture diagrams exist |
| `ESSENTIALS.md`, `PLAYBOOK.md`, `LESSONS.md`, `logs/TOKEN-LOG.md` | n/a per-repo — live in `.dev-knowledge` only |

Optional files are added by judgment of repo complexity; no tier makes them mandatory.

### Canonical-file freshness cadence (audit check #10)
<!-- scope: meta -->
<!-- rule: canonical-freshness -->

The living docs `VISION / ARCHITECTURE / CLAUDE / CONTRIBUTING / ESSENTIALS` carry a `last_reviewed` frontmatter date. **`last_reviewed` means "re-read end-to-end and confirmed accurate (or the drift filed)" on that date — NOT merely "touched".** Bump it only after a genuine review, never reflexively.

`scripts/audit.py` check #10 (`canonical_freshness`, in `ALL_CHECKS` → runs in `audit health` and `audit run`) enforces two signals:

- **A2 — edited-since-review (FAIL):** `last_reviewed` predates the file's last git-commit date. The load-bearing signal — you changed the file but never re-confirmed it.
- **A1 — calendar backstop (WARN, 30 days):** a loose nudge to re-read even when nothing changed. WARN, not FAIL — a quiet doc is not a broken one.

Append-only (`JOURNAL`, `LESSONS`) and per-session (`BACKLOG`) files are excluded — their freshness is intrinsic. A file with no `last_reviewed` → WARN (lets a repo adopt the convention without a hard failure). **Portable:** the check is parameterised by a file list, so a child repo inherits it unchanged (its own project `CLAUDE.md` is `"CLAUDE.md"`). Operationalizes the ADR-39 "grooming" lifecycle element.

**Scope + caveats (honest limits).** This enforces *edit-hygiene* + a calendar backstop. It does **not** detect content-vs-decision drift — a doc whose prose lagged a new ADR while its file was never edited trips neither signal (that is the doc-truth sweep, BACKLOG [#10]). A2 is **commit-based** (keyed off the file's last *author* date, stable across rebase): an uncommitted working-tree edit is flagged at the next audit *after* it lands in a commit, not while the tree is dirty — the signal is eventually-consistent, not real-time (failing a dirty tree would fire mid-edit, before the reviewer has bumped the stamp). It is **gated at pre-commit**: the `audit-health` hook runs `audit.py health` on every commit, so an A2 FAIL blocks the commit — while A1 (the 30-day backstop) and a missing stamp are WARN and never block (`git commit --no-verify` bypasses). There is no CI/remote in this flow, so pre-commit is the gate; a session-close hook remains a possible future addition.

### Multi-surface amendment coherence (audit check `amendment_coherence`)
<!-- scope: meta -->
<!-- rule: coherence-amendment -->

**A version/authority amendment that spans several hand-maintained surfaces must leave no straggler.** This converts LESSON-#9's advisory "cross-case trace before a multi-surface amendment" guard into an enforced gate — the failure it prevents is the v3.4 self-handoff abort (the skill announced v3.3.3 while the spec was v3.4: a stale version string that mis-signalled authority). The cross-case trace is no longer a remembered intention; it is a gate.

`scripts/audit.py` `amendment_coherence` (in `ALL_CHECKS` → runs in `audit health` and `audit run`) reads a declarative manifest — `_COUPLED_VERSION_SETS`, the cross-case **"checklist as data"**. Each `CoupledSet` names an *anchor* (the authority version) and the *surfaces* that must agree with it at a `granularity` (`major`, or `full` with `3.4 == 3.4.0` normalization). A surface left at a stale version is a **straggler → FAIL**. Add a set when a new family of surfaces must track one authority version; the membership criterion is **semantic intent-to-mirror, not mere co-occurrence** of a version string (an incidental mention that versions independently would false-FAIL — anchor the regex on the *intent-bearing construct*). Child-repo-safe: an absent anchor skips the set (the hub-only sets skip entirely on a child → PASS). FAIL-blocking via the `audit-health` pre-commit hook.

**Scope + caveats (honest limits).** This guards only surfaces that **still hand-maintain a version**. The superior fix for a coupled surface is to **de-hardcode** it — make it interpolate the spec version (the handoff skill/templates read `{{VERSION}}`), so there is no static token to go stale; de-hardcoded surfaces carry nothing to compare and are **out of scope by design** (de-hardcoding, not this gate, closes their straggler class). So the gate does **not** by itself prevent a literal v3.4 recurrence — it guards the residual hand-maintained surfaces and is the extensible home for future coupled families. The narrow `handoff_version_stamp` check owns the full `stamp vX.Y` mirrors in `ARCHITECTURE`/`CONTRIBUTING`; `amendment_coherence` is the generalized manifest beside it. Per the prose↔state seam, it does not detect drift on de-hardcoded or unmanifested surfaces.

### Declared-edge reconciliation (audit check `reconciled_versions`)
<!-- scope: meta -->
<!-- rule: coherence-spec-reconciled -->

**A doc that declares a dependency on a versioned spec must not drift from it.** A dependent carrying a `reconciled_with: <spec-id>@<version>` edge MUST match that spec's live version; a drifted edge **FAILs** (`scripts/audit.py` `reconciled_versions`, in `ALL_CHECKS` → runs in `audit health` and `audit run`; teeth in `scripts/validate_reconciliation.py`). This is the **declared half** of dependency coherence — the ADR-88 coherence spine (#172) — the complement to the undeclared-edge discovery scan (`scan_undeclared_edges.py`, #179, awareness-only). The spec registry is `_SPEC_REGISTRY` in `validate_reconciliation.py` (v1: `handoff-process`); add a spec there when a new versioned dependency must be tracked. Child-repo-safe (an absent edge skips); read-only. Distinct from `amendment_coherence` above: that guards hand-maintained version *mirrors*; this guards *declared* `reconciled_with` *edges*.

### Common confusions resolved
<!-- scope: meta -->

**JOURNAL vs handoff:**
- JOURNAL = within-repo, per-session tactical log. Continuity across Claude Code sessions in same repo.
- handoff = across-context, browser-chat-to-browser-chat session summary. Continuity when switching chats.
- Both can coexist. Larger repos typically use both; smaller repos usually one or the other (often handoffs).

**LESSONS vs ADR:**
- LESSONS = process lessons (how Rob works, anti-patterns, what tooling drift looked like). Append-only.
- ADR = architectural decisions (technical commitments). Amendable per ADR-29 pattern.
- Process generalization → LESSONS. Technical commitment → ADR.

**CHANGELOG vs JOURNAL:** (CHANGELOG.md retired 2026-05-16 per ADR-49 — the JOURNAL `Changes:` line + git history now carry what CHANGELOG used to; the distinction below is preserved for legacy context.)
- CHANGELOG (retired) = strategic, what user/contributor needs to know about repo evolution. Newest-first.
- JOURNAL = tactical, what Claude Code did session-by-session. Append-only, newest-first prepend (amended 2026-04-27 from oldest-top per Rob's preference; matches TOKEN-LOG convention).
- Same commit might warrant entries in both — different abstraction levels.

**audits vs research:**
- audits = backward-looking analysis of current state (per-repo, dated)
- Council debates (research-mode and pick-mode) → `docs/decisions/transcripts/` (routed per ADR-43). The retired `research/` folder is no longer used (2026-05-27 ADR-60 amendment).

### Supersession & decommissioning
<!-- scope: meta -->

Decisions are additive by default — they describe the new state, not the
teardown of the old. This is how orphans accumulate: a structure is relocated
or replaced, the new location is recorded, the old one is left behind and
forgotten. A presence-checking audit will never catch it.

Rule: any decision — ADR or decision-note — that relocates, replaces, or
centralizes an artifact MUST name what becomes obsolete in a `Decommission:`
field. A non-empty `Decommission:` field becomes a BACKLOG item and stays open
until the obsolete artifact is removed.

The decommission action is part of the decision, not an optional follow-up. A
decision that supersedes something is not complete until its `Decommission:`
items are removed or tracked in BACKLOG.

### Handoff format spec

<!-- scope: meta -->

**Authoritative spec: `protocols/HANDOFF_PROCESS.md` v5** — the single live source of truth for handoff mechanics. This is a pointer, not a duplicate; do not re-document the structure here (the duplication is what drifted).

Formats in `docs/handoffs/`, all but the current one historical:

- **Legacy single-file (before 2026-04-27)** — one dated `YYYY-MM-DD-slug.md` free-form summary. Preserved as-is; do not migrate.
- **v3.x folder bundle (2026-04-27 → v4 rollout)** — `upload-instructions.md` + `first-message.md` + a `contents/` subfolder of point-in-time copies. **Superseded**; preserved as point-in-time history, never regenerated.
- **v4 bundle (2026-05-29 → v5 flip 2026-06-11; historical)** — flat `docs/handoffs/<slug>/` = `README.md` + `01_ROLE`…`07_ASK_BACK`, generated from source via a two-phase flow. **Superseded by v5**; existing bundles preserved as history, never regenerated.
- **v5 handoff (current)** — CC-owned: a lean **residual** + **probe manifest** under `docs/handoffs/<slug>/`, plus a thin browser boot (`protocols/HANDOFF_BOOT.md`) that replaces the multi-file bundle. Generated from live state at handoff time; teeth-y forced primary-source read. Full structure in `HANDOFF_PROCESS.md` §2–§5.

### Order conventions
<!-- scope: meta -->

Per Token-LOG flip 2026-04-24:

- **Newest-first (prepend):** TOKEN-LOG, JOURNAL (CHANGELOG retired — §14). Rationale: logs optimize for current-state scanning. (JOURNAL flipped 2026-04-27 — original Stream B Gap #4 spec had oldest-top; amended for consistency with TOKEN-LOG/CHANGELOG.)
- **Append-only (oldest top):** LESSONS. Rationale: chronological narrative for grandfathered learning patterns; order preserves "what we learned when" per ADR-29.
- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT. Rationale: not logs; current state matters more than history.
- **Immutable (dated):** ADRs, transcripts, handoffs, audits, research. Rationale: point-in-time records; supersession via new file or in-file marker.

---

## Ch7. Review postures
<!-- scope: meta -->

Four review postures distilled from the 2026-05-19 posture-audit (`docs/audits/2026-05-19-dev-knowledge-posture-audit.md`, findings H3/H4/T1/T2). Governance-doc and ADR craft — apply when editing, relocating, or deleting canonical content, or when deciding whether a one-off decision earns an ADR. Wording sourced **verbatim** from the audit; codified per #34.

- **Stable-end-state** (audit H3) — *"Governance docs phrased as stable end-state; transient status lives in JOURNAL."* Governance docs describe end-states; transient status (what's done / pending) lives in JOURNAL or a rollout-tracker, never as time-bound clauses that read stale later.
- **Verify-destination** (audit H4) — *"When relocating or dropping content, Plan Mode confirms destination genuinely covers it."* Before deleting a pointer or relocating a section, confirm the destination already carries each sub-part — verify, don't assume.
- **No-delete-canonical-dup** (audit T1) — single-source-of-truth (P1) overrides never-delete (P7) **only** when the deletion targets a *"duplicate of canonical content"* preserved elsewhere. The no-delete invariant has an explicit exception for duplicates of canonical content; deleting a unique copy is still forbidden.
- **ADR-with-N=1** (audit T2) — *"A single architectural CHOICE with no prior precedent can be an ADR-with-N=1 because the choice itself is the record, not a pattern claim."* The N≥2 bar blocks PATTERN extraction without evidence; it does not block recording a singular decision whose record IS the choice.

---

## Ch8. Session boundaries
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Browser chats and Claude Code sessions have natural quality limits. Pushing past them produces decisions that look fine in the moment but read poorly the next day. This section codifies recognition signals and stop-protocols.

### Scope declaration at start
<!-- scope: meta -->

Every session opens with explicit scope. If Rob doesn't state it, browser chat asks before proceeding.

**Format (one sentence each):**
- **In scope:** what this session aims to accomplish
- **Out of scope:** what this session deliberately defers
- **Success criterion:** what makes the session "done" (commit merged? decision documented? specific artifact produced?)

**Why explicit:** without scope declaration, every passing thought becomes a candidate detour. Scope is the contract for "is this proposal in scope or scope creep?"

**Example (good):**
> In scope: implement Gap #13 in PLAYBOOK. Out of scope: per-repo PLAYBOOK rollout, other gaps. Success: new section merged with v1.0 marker.

**Example (bad):**
> Let's work on .dev-knowledge today. (No scope = unbounded session = guaranteed creep)

### Stop-signs (recognize and act)
<!-- scope: meta -->

These signals indicate a session should stop or refocus, NOT push through:

- **Decision fatigue:** >3 hours active session AND >3 architectural decisions made. Each subsequent decision is statistically lower quality.
- **Recursive planning** (anti-pattern, see below) — three consecutive turns producing plans/audits/specs without execution
- **Scope creep accumulation:** more than 2 "while we're at it" expansions in one session — even if individually small
- **Re-explanation loops:** Rob explaining the same protocol/context to Claude more than once in a session — signal that earlier context is gone or wasn't applied
- **"Just one more thing"** at end of natural stopping point — usually the wrong call; the next thing deserves fresh start
- **Quality regression:** finding errors in prompts/decisions that wouldn't have happened earlier in session

When stop-sign appears, ACTION:
1. Generate handoff (per HANDOFF_PROCESS.md)
2. Identify the specific stop-sign that triggered (helpful for next session retrospective)
3. Stop. Resume with fresh head.

### Decision fatigue threshold
<!-- scope: meta -->

**Numeric guideline:** >3h elapsed + >3 architectural decisions made = wrap-up zone.

This isn't a hard limit. Session may legitimately need to push past it (e.g., critical fix, time-bound deliverable). But entering wrap-up zone shifts default from "continue" to "wrap up unless reason to continue."

**Why these numbers:** a working threshold drawn from session experience — quality of decisions visibly degraded past these points, including by the "decider's" own self-assessment in retrospect. Treat as a calibrated rule of thumb, not a measured constant.

**Counter-indicator:** if session is execution-heavy (running prompts, watching Claude Code commit) rather than decision-heavy, threshold is generous. The fatigue is decision-specific, not pure clock time.

### Recursive planning anti-pattern
<!-- scope: meta -->

**Detection:** session produces plans/audits/specs about plans/audits/specs without producing any actual artifact change.

**In-vivo example (2026-04-24):** during Stream A→B transition, browser chat repeatedly proposed:
- "Let's audit what we have"
- "Let's audit again with mapping"
- "Let's create reference doc for the gaps"
- "Let's plan the implementation order"

While useful for some context, this stacked 4 layers of meta-work before any gap was implemented. Pattern only broke when Rob explicitly said "implementacja, nie planowanie" — and even then, it took conscious resistance.

**Symptoms:**
- Proposing "audit" when implementation is the next logical step
- Proposing "plan" when a plan already exists
- Proposing "framework" or "specification" before MVP attempt exists
- Each output describes what to do, not what was done

**Counter-protocol:**
- After 2 consecutive planning/audit outputs, FORCE next output to be implementation prompt
- If implementation feels too risky → spike (4h throwaway branch) instead of more planning
- Watch for rationalizing: "we need to audit because..." Almost always: we don't.

### Session resumption protocol
<!-- scope: meta -->

When opening a new session that continues prior work:

**Browser chat resumption:**
1. Upload `ESSENTIALS.md` (always)
2. Upload most recent `docs/handoffs/*.md` (if any)
3. Upload PLAYBOOK.md (if doing dev work — large file, but contains all protocols)
4. Upload task-specific docs (specific ADRs, Stream B mapping if continuing Stream B, etc.)
5. First message states: scope (in/out), success criterion, what was last session's stopping point

**Claude Code resumption:**
1. Read CLAUDE.md (auto on session start)
2. `git status` and `git log --oneline -5`
3. Read most recent handoff if exists
4. Read JOURNAL.md last 5 entries (if the repo keeps one)
5. Wait for prompt — never improvise

**Anti-pattern:** opening new session with bare prompt "continue what we were doing" — without uploading context, both sides reconstruct from memory (browser) or scratch (Claude Code). Quality drops fast.

### Parallel sessions & worktree discipline (per ADR-61)
<!-- scope: meta -->

**Decide first:** *different* repos in parallel need **no** worktree — separate `.git/`
directories already isolate them, so just open two Claude Code sessions (this is the common
case, e.g. a corp-monorepo handoff and an ai-council handoff at the same time). Only
*same-repo* parallel work requires a `git worktree` (ADR-61).

**The real trigger is *committing*, not *editing* (sharpened 2026-06-07 — 2nd incident).** Same-repo parallel sessions are allowed in exactly two shapes:
- **(a) Zero-write** — read/analysis only: no commits, no `git add`/staging, no branch ops. Any number of zero-write sessions may share one checkout safely.
- **(b) Each committing session in its OWN worktree.** **One checkout = one committing session.** A "single commit at the end" still counts as a committing session — there is no "I'll only commit once" exception. (Witnessed 2026-06-07: a no-worktree session whose lone witness commit `49c7db7` landed on a *concurrent* session's branch, swept its staged file, mis-rooted the branch, and stranded its closeout into a multi-commit tangle. First incident class: 2026-06-01.)

**#107 SHIPPED (2026-06-07, verify-first + witnessed).** Shape (b) now runs on **CC-native
managed worktrees** — the low-friction path. The earlier *"sequential exclusivity until #107"*
interim rule is **retired**, and the old *sibling* worktree naming (`<repo>-parallel` /
`<repo>-wt-*`) is **superseded** by the in-repo native location below — sibling worktree dirs
are exactly what spawned the `.dev-knowledge-cadence` / `.dev-knowledge-night-adr` rule-9
orphans, so do not create them anymore.

**Lifecycle (same-repo only):** a worktree is **per-goal scratch, not a persistent
checkout** — *provision → use → ephemeral teardown*. Create one for a single goal, work it on
its own branch, and remove it the moment that branch merges. It must not linger between goals.

**0 — Decide: should I parallelize? (checkable — apply BEFORE provisioning)**

Parallelizing costs a worktree + a serial integration pass. Reach for it only when **every
check is YES** — otherwise do the items serially:

- **Disjoint substantive files?** Do the two items touch *different* substantive files? Shared
  canonical files (BACKLOG / JOURNAL / PLAYBOOK / CLAUDE) do **not** disqualify a pair — they are
  *handled*, not parallelized (see below) — but two items editing the *same substantive* file must
  go serial.
- **Two distinct goals, not one?** "Finish the rest of X" is **one** goal — complete it serially,
  do not split it. Only split genuinely independent items.
- **Each stream more than a single-file edit?** Tiny disjoint edits (a file or two, minutes each)
  are faster done serially than provisioned + integrated. This is the one check with an irreducible
  judgment margin; the working threshold is *more than a single-file edit per stream* — below that,
  don't parallelize.

**Canonical safe pair: one code item ∥ one doc item.** Disjoint files by construction. Review
contention is at most one-sided: the **doc** stream never needs Codex; only the **code** stream
*might* — and only if it trips the Codex bar (3+ files or safety-critical, per ADR-54). Reach for
this shape first.

**Shared canonical files are handled, not parallelized** (refines §3's serialize rule):
- **BACKLOG: removal travels the closure loop, not the branch.** Don't have each branch delete its
  own task line; leave the removal to the Tier-1 closure loop (`/review-closures`) after merge, so
  two branches never contend on the same deletion. The edits §3 serializes are BACKLOG **adds /
  grooming** (and id allocation at write-time) — not removals.
- **JOURNAL: the conflict is trivial.** Each branch prepends its own newest-first entry; a merge
  conflict is just two top-of-file prepends — resolve by keeping both in timestamp order. JOURNAL
  is therefore not a real serialization blocker.
- **Operator is the serial gate.** Parallel branches return to the operator, who `/ship`s them **one
  at a time from the primary** — branches never self-merge in arbitrary order.

**1 — When a worktree is needed**

- **Different repos in parallel: already safe.** Separate `.git/` directories isolate each
  session completely — no worktree setup needed. Cross-repo sequential orchestration (one
  session `cd`-ing into multiple repos) is also safe for the same reason.
- **Same repo in parallel: REQUIRES a worktree.** One working tree has one HEAD + one index;
  two+ committing sessions on a shared checkout collide — a commit in one sweeps the other's
  staged file and lands on the wrong branch (witnessed 49c7db7 2026-06-07; the witness replay
  proving separate worktrees = zero sweep is in the #107 JOURNAL entry / LESSONS).

**2 — Provision (native-primary)**

**Recommended START — Primary = stream A, worktree = stream B** (the from-scratch recipe for
splitting one session into two same-repo streams):
1. **Pre-flight:** `git worktree list` shows only the primary; working tree clean.
2. **Stream A** stays in the **primary** checkout, on its own `feat/<A>` branch — the primary is
   also the integration + serial gate (step 4).
3. **Stream B:** `claude --worktree <B>` → a session inside `.claude/worktrees/<B>` on branch
   `worktree-<B>` (`.worktreeinclude` seeds `ecosystem/*/state.yaml` so the audit-health gate
   passes — see below).
4. **Integrate from the primary on `main`, one at a time:** `/ship` stream A; then
   `git merge --no-ff worktree-<B>` + `git push`; then tear down B (the §4 three-command
   round-trip) and verify no leftovers.

**The command the architect hands the operator is `claude --worktree <B>` (new terminal) or
`EnterWorktree` (mid-session) — NEVER a raw sibling `git worktree add ../dev-knowledge-<B>`.** The
sibling-dir recipe is superseded (above): it skips the `.worktreeinclude` auto-seed (forcing the
manual seed in §2a) and is the documented source of the `.dev-knowledge-*` rule-9 orphans. Native
keeps the worktree gitignored under `.claude/worktrees/` and seeds it for you.

The bullets below are the mechanism this recipe rests on.

- **New parallel session:** `claude --worktree <name>` (alias `-w`) starts a session already
  inside a fresh worktree. **Mid-session:** the `EnterWorktree` tool switches the *current*
  session into one (`ExitWorktree` returns). Both create **`.claude/worktrees/<name>/` on
  branch `worktree-<name>`** (verified). Base ref = `worktree.baseRef` setting: `fresh`
  (default → `origin/<default-branch>`) or `head` (current local HEAD).
- **`.worktreeinclude` is load-bearing — do NOT delete it.** A fresh worktree is a clean
  checkout and so OMITS gitignored runtime state — including `ecosystem/*/state.yaml` (ADR-80
  high-churn pointers). Without them the `audit-health` pre-commit gate runs the worktree's own
  `audit.py`, sees `repos registered (none)`, reports `health: DEGRADED`, and **blocks every
  commit** — a fresh committing worktree is dead on arrival. The repo's committed
  `.worktreeinclude` (lists `ecosystem/*/state.yaml`) makes the **native** worktree-create copy
  that state in, so the gate passes (witnessed: seeded worktree commit lands; unseeded blocks).
  **Verified 2026-06-18 (native in-session via `EnterWorktree`):** all 5 `ecosystem/*/state.yaml`
  — *including the dot-prefixed `.dev-knowledge` hub dir* — auto-seeded with no manual step, and
  `python scripts/audit.py health` returned `health: OK` / `repos registered (all 5)` from *inside*
  the worktree. The **raw** `git worktree add` path does NOT honor `.worktreeinclude`, so there the
  §2a manual seed is still required — that is the seed-friction the sibling-dir flow hits, not the
  native one.
- **Walker safety (why in-repo `.claude/worktrees/` is safe):** it's gitignored, so `git status`
  stays clean and **ruff** (respects gitignore) won't double-lint the full second checkout;
  **pytest** is safe via its default `.*` dot-dir skip (collection stays 329, not 658). These
  hold *only* while worktrees live under `.claude/worktrees/` — keep them there.
- **Pre-flight:** always `git worktree list` before starting parallel work.

**Manual residual (cross-repo / non-CC / interactive — Fork B, KILL-2):** native manages only
*Claude-spawned* worktrees. For a worktree you must drive outside CC, use raw
`git worktree add .claude/worktrees/<name> -b worktree-<name>` (same in-repo location) and seed
the state by hand (`.worktreeinclude` does **not** apply to raw `git worktree add`); teardown is
manual (below). Each session works a distinct branch (git forbids one branch in two worktrees).

**2a — Cold-start specifics** (the four details a fresh operator needs that the recipe above
assumed — terminal anchor, slug, manual seed, pwd-confirm; verified by the 2026-06-15 smoke test)

- **Where you launch it (terminal anchor).** `claude --worktree <name>` (alias `-w`) is run from
  a **fresh PowerShell terminal at the `<repo>` root** — a cold-start session that begins life
  *inside* the new worktree. To split an **already-running** session instead, use the
  `EnterWorktree` tool mid-session (`ExitWorktree` returns to the primary). Either path lands you
  in `.claude/worktrees/<name>/` on branch `worktree-<name>` (observed, not just documented —
  the smoke test confirmed this exact in-repo location + branch name on this machine/CC version).
- **`<name>` slug convention.** Name the worktree **`<issue#>-<kebab-slug>`** — e.g.
  `156-taskgraph` → dir `.claude/worktrees/156-taskgraph/`, branch `worktree-156-taskgraph`. With
  no backing issue, use a bare `<kebab-purpose>` slug (e.g. `changelog-sync`). This formalizes the
  de-facto `156-taskgraph` example as the convention — it is not a new scheme.
- **Manual-seed commands (raw `git worktree add` path ONLY).** `.worktreeinclude` is honored by
  the **native** create but **NOT** by raw `git worktree add`, so a hand-driven worktree starts
  WITHOUT the gitignored `ecosystem/*/state.yaml` it declares — and its first commit is blocked by
  the `audit-health` gate (`repos registered (none)` → `health: DEGRADED`). Seed it by hand,
  copying exactly what `.worktreeinclude` lists. From the `<repo>` root in PowerShell:

  ```powershell
  # 1. create the worktree (raw path — same in-repo location the native create uses)
  git worktree add .claude/worktrees/<name> -b worktree-<name>
  # 2. seed the runtime state .worktreeinclude declares (ecosystem/*/state.yaml), mirroring paths
  Get-ChildItem ecosystem -Directory | ForEach-Object {
    $src = Join-Path $_.FullName 'state.yaml'
    if (Test-Path $src) {
      $dst = Join-Path ".claude/worktrees/<name>/ecosystem" $_.Name
      New-Item -ItemType Directory -Force -Path $dst | Out-Null
      Copy-Item $src (Join-Path $dst 'state.yaml')
    }
  }
  ```

  (The native `claude --worktree` / `EnterWorktree` path performs this copy for you — these
  commands are ONLY for the raw fork. As of 2026-06-15 `.worktreeinclude` lists `ecosystem/*/state.yaml`
  and `ecosystem/` holds 4 child dirs, each with a gitignored `state.yaml`.)
- **pwd-confirm before working (ADR-61 rule 5, re-carried into the manual path).** Before any work
  in a hand-driven worktree, verify you are actually in it — `Get-Location` (`pwd`) must resolve to
  `…/.claude/worktrees/<name>`, NOT the primary root. A commit fired from the wrong cwd lands on the
  wrong branch (the shared-index sweep this whole discipline exists to prevent).

**Worked example end-to-end** (copy, don't reconstruct — values observed in the 2026-06-15 smoke test):

```
# 1. fresh PowerShell terminal at the repo root, cold start:
claude --worktree 156-taskgraph
#    -> session opens inside .claude/worktrees/156-taskgraph/ on branch worktree-156-taskgraph
#    -> .worktreeinclude auto-seeds ecosystem/*/state.yaml (native path) so audit-health passes
# 2. work the task there -- fully isolated; the primary checkout's `git status` never sees it
# 3. integrate from the PRIMARY checkout on main (never from inside the worktree):
git merge --no-ff worktree-156-taskgraph
git push
# 4. teardown -- the 3-command round-trip (see section 4 below), then verify no leftovers:
git worktree remove .claude/worktrees/156-taskgraph
git worktree prune
git branch -d worktree-156-taskgraph
#    -> git worktree list shows only the primary; the dir is gone; git status clean
```

The raw `git worktree add` layer this wraps was run end-to-end on 2026-06-15 (create → isolation
check → 3-command teardown) and left zero leftovers, confirming the observed dir/branch values
above. Windows caveat: if VS Code (or any IDE with a recursive file watcher) has the repo open,
the teardown's first command can deregister the worktree yet fail to delete the now-empty
directory — re-check `.claude/worktrees/` and clear any empty husk once the IDE releases the handle.

**3 — Discipline while running in parallel** (earned 2026-06-01 — see LESSONS)

- **One worktree per goal.** Never drive a single checkout from two committing sessions.
- **Serialize edits to shared canonical files** (BACKLOG, JOURNAL, PLAYBOOK, CLAUDE). Only
  one active branch touches a given canonical file at a time — parallel branches each read
  their *own* `main` and won't see each other's edits, producing silent divergence + conflicts.
- **Allocate backlog ids at write-time, in order — for *parallel* arcs, reserve a
  non-overlapping range per arc by writing it into BACKLOG *before* the split.** Never reserve an id
  "verbally" (held only in conversation); a phantom reservation outside the file causes id
  collisions (#68/#69 near-misses). Parallel branches each read their *own* stale `main`, so even
  write-time allocation collides unless the ranges were committed before branching — reserve in the
  *file*, never in conversation (#186 was hand-coordinated this way this session).

**4 — Integration & ephemeral teardown** (the moment the parallel branch's work is done)

- **`/ship` runs from the PRIMARY checkout, not from inside a worktree.** A worktree cannot
  `git checkout main` (`fatal: 'main' is already used by worktree …`), which `/ship`'s merge
  step needs; ship.md now **refuses cleanly** from a worktree (pre-flight #1) with this guidance.
- **`/review-closures` also runs from a primary on-`main` session, not a worktree.** The plugin's
  `review_closures.py` resolves its `BACKLOG.md` via `$CLAUDE_PROJECT_DIR` (the session's checkout;
  it falls back to `cwd`, which in a worktree session is *also* the worktree) — so run from a
  worktree it would read/close against the *feature branch's* BACKLOG, not `main`. Closing is the
  *primary's* job, after the merge — the operator-facing form of the "removal travels the closure
  loop" rule above. Witnessed this session; mechanism confirmed in `review_closures.py`.
- **Integrate from the primary:** from the primary on `main`, `git merge --no-ff worktree-<name>`
  then `git push` (repo `--no-ff` norm). Don't try to rebase/linearize a branch that is checked
  out in another worktree — git blocks it.
- **Merge serialization — why two concurrent merges to `main` can't tangle (#200).** The
  decided guard is *not* a lock/mutex; the verify-first finding (#200) is that the
  concurrent-merge race is already serialized — by **git itself**, plus the existing FF-block:
  - **`index.lock`** — two simultaneous `git merge` commands can't both proceed; the second
    fails `Unable to create '.git/index.lock': File exists. Another git process seems to be running`.
  - **`MERGE_HEAD` refusal** — a second `git merge` while one is in-progress is refused by git
    (`Merging is not possible because you have unmerged files` / `You have not concluded your merge`).
  - **Push-rejection = `main` moved = re-integrate.** A push to a `main` that another clone
    already advanced is rejected `! [rejected] … (fetch first)`; you `git pull` and re-merge.
    This is git serializing the integration point across clones — lean on it, don't rebuild it.
  - **The FF-block** (`scripts/block_ff_push.py`, pre-push, hub-only) refuses any push adding a
    non-merge commit to main's first-parent spine (core-invariant #5).
  - **A worktree→`main` merge is git-structurally prevented** — a linked worktree cannot
    `git checkout main` (it's already checked out in the primary), so integration *always*
    funnels through the single primary checkout, where the natives above apply.
  - **Honest limit (not gate-catchable):** a *primary*-checkout self-merge is byte-identical to a
    legitimate operator merge (same command, same branch shape — no git signal separates them), so
    **no hook can distinguish them.** That case is held by the commit-and-STOP / integrate-from-the-
    primary discipline (operator is the serial gate, above) + the A1 empirical close (#184), and by
    #107 worktree isolation for the shared-HEAD hazard — *not* by machinery. The git-native behavior
    is witnessed in `tests/test_merge_serialization.py`; #200 closed accepted-prose-only on this basis.
- **Teardown — native first:** a *changeless* worktree auto-removes on `ExitWorktree`/session
  exit (and `isolation:"worktree"` subagents auto-clean); a worktree that has commits is KEPT.
  After merging, remove it:

```
git -C <repo> worktree remove .claude/worktrees/<name>
git -C <repo> worktree prune
git -C <repo> branch -d worktree-<name>
```

- **`cd` out of the worktree before removing it; use `--force` when seeds block the remove.** If
  your shell's cwd is *inside* `.claude/worktrees/<name>`, your own shell locks the dir and `git
  worktree remove` cannot delete it (a lock source distinct from an IDE file-watcher). Use `git
  worktree remove --force …` when the gitignored seeds (`ecosystem/*/state.yaml`) make git treat
  the worktree as dirty and refuse a plain remove. The native `ExitWorktree` path does both for you
  (restores cwd first, and removed a seeded changeless worktree cleanly — verified 2026-06-18);
  these manual steps are the raw-path case. **`remove` is NOT idempotent — if a first remove is
  interrupted, recover with `git worktree prune` (step 2 above), never a second `remove`; see the
  dedicated gotcha.**
- **Verify the teardown left nothing behind (no-leftovers round-trip).** `git worktree list`
  shows only the primary; the `.claude/worktrees/<name>` dir is gone from disk; `git status`
  is clean. `git worktree remove` silently no-ops when the dir is busy/locked, so re-check —
  never assume. The provision→teardown cycle must leave the tree *identical* to its pre-provision
  state.

Full rationale: ADR-61 (as superseded by the #107 native-worktree convention). This teardown is
the worktree-specific case of the broader rule that any automated or scratch-creating process
cleans up — and verifies it cleaned up — everything it created (the no-leftovers invariant, next).

### No leftovers: automated processes clean up — and verify it (invariant)
<!-- scope: meta -->

**Invariant.** Any automated or scratch-creating process — a parallel-session worktree (above),
the night-agent's per-run review worktree (ADR-68), a temp/scratch file, a generated bundle's
intermediate artifacts — **removes everything it created, and verifies the removal**, before it
counts as done. Cleanup is part of the process, not a follow-up, and it must fire even on abort
or failure (ADR-68's worktrees are "created per run and removed at run end, cleanup fires even
on abort/failure" — that is the model to copy).

**The verification is a concrete round-trip:** a provision→cleanup cycle leaves the tree
*identical* to its pre-provision state. Diff before against after — if anything the process
created survives, teardown is incomplete. For worktree/scratch work the round-trip is three
commands:
- `git worktree list` → only the main worktree remains (no leftover registration).
- no stray sibling directories on disk (`<repo>-*` worktree dirs gone — the check G4 step 4 names).
- `git status` → clean (no untracked scratch/temp files left behind).

**The failure this prevents:** the `.dev-knowledge-cadence` and `.dev-knowledge-night-adr` sibling
worktree directories — created for a goal, deregistered from git, but never removed from disk, so
they linger as orphans. (One was locked by another process — which is *exactly* when a `remove`
silently no-ops and the result must be re-checked, never assumed.) An orphan is invisible to a
presence-checking audit, which verifies that required files *exist* and structurally cannot detect
a file that exists but should not (the 2026-05-17 decommissioning-gap LESSON). So the round-trip
diff is an explicit process step at run end, not something a later scan will catch.

**Lightweight check, not heavy tooling.** The three commands above *are* the check — a process
step, not a script (Layer 2 never executes — critical rule #4). Run them at the end of any
worktree/scratch-creating run. The read-only `audit.py` assertion that no stray `<repo>-*` sibling
exists is now **built** — `check_no_sibling_orphans` (#11), keyed on `git worktree list`
registration so a *live* registered worktree passes and only an unregistered orphan fails; it runs
in the `audit-health` pre-commit gate, so an orphan blocks the next commit until removed. The
process step above remains the first line of defence (catch it at teardown); the check is the
backstop that catches what the manual teardown missed. (Recurrence cleaned 2026-06-02 — see LESSONS.)

---

## Ch9. Tier-1 closure loop — usage
<!-- scope: meta -->

Per session: commit work normally, using `closes [#id]` on the commit that **finishes** a backlog item (not `advances` — see CONTRIBUTING; `advances` leaves the item open and invisible to the detector). At session end the `tier1-lifecycle` plugin's `Stop` hook proposes likely closures (`logs/PROPOSALS-*.md`); at the next session start the global `[closures] N proposed` reminder (L0 `surface-closures.ps1`) surfaces the count; run `/review-closures` to confirm and update `BACKLOG.md`. Architecture of the three layers: `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle".

### Propagating a plugin change across the fleet

When the `tier1-lifecycle` plugin source changes in `.dev-knowledge`:
1. bump `version` in `plugins/tier1-lifecycle/.claude-plugin/plugin.json`;
2. `claude plugin marketplace update dev-knowledge-methodology`;
3. per installed repo, `claude plugin update tier1-lifecycle@dev-knowledge-methodology --scope project`;
4. restart the session.

The cache is **version-keyed** — `marketplace update` alone won't refresh at an unchanged version, and `plugin install` no-ops on an already-installed repo (use `update`, not `install`). `--scope project` is mandatory for project-scoped installs. Full reference: `plugins/tier1-lifecycle/INSTALL.md`.

---

## Ch10. Two-tier automation doctrine
<!-- scope: meta -->

The canonical layer→job matrix is **ADR-74**; this is its operating-doctrine prose, adopted fleet-wide by **ADR-80**. The organising question is a single axis — **does the organ exercise LLM judgment?** — which splits all automation into two tiers.

**Deterministic automation (no model).** Pre-commit + commit-msg hooks, `audit.py` self-conformance, and the scheduled `fleet_health.py` cross-repo baseline (Windows Task Scheduler → Python directly — **no `claude -p` on the scheduled path**, ADR-76). Posture: **fail-closed on any executing path** (a gate that *can* block a commit does) and **fail-soft on awareness paths** (a surfacing hook that can't run prints nothing and exits 0, never blocking a session). Spans ADR-74 Tiers 1–2 (lifecycle + scheduled baseline).

**LLM-judgment automation.** Any organ that runs a model. Invariant: **always read-only + adversarial-skeptic-filtered + operator-ratified** — it proposes, a skeptic kills false positives, and a human funnel ratifies before anything binds. Nothing it emits is binding unattended. Two delivery forms, both ADR-74 Tier 3:

- **Cloud Routine** — self-contained (clones only its own repo, reads no sibling — ADR-72/73); read-only schema-bound agents + skeptic; output via its **declared channel**: a `claude/<task>-YYYY-MM-DD` branch → PR → the GitHub Action diff-guards and **squash-merges** (compliant-by-design — witnessed 2026-06-07, PR #17 squash-merged to `main` as `221c63e`; the single non-merge commit is the *designed* cloud channel, deliberately distinct from the local branch+merge `--no-ff` discipline for human-authored arcs). See "Routine/night deployment standard › The outcome loop".
- **Dynamic Workflow** — escalation-only heavy/episodic fan-out (the `Workflow` tool). **Operator-invoked, never scheduled**; trigger keyword **`ultracode`** (the word "workflow" stopped triggering — Claude Code 2.1.160). Escalation criteria: §2 "When to escalate to a Dynamic Workflow".

> **Numbering note.** "Two-tier" is the *LLM-judgment axis* (deterministic vs judgment) — **orthogonal** to ADR-70/74's friction-cadence Tiers 1/2/3 (always-on / scheduled / episodic). Both lenses are live and this section never renumbers ADR-74: a cloud Routine is ADR-74 **Tier 3** *and* a judgment organ; the scheduled baseline is ADR-74 **Tier 2** *and* a deterministic organ.

### Writer policy — automation that writes the tree commits its own output (ADR-80)
<!-- scope: meta -->

A job that writes tracked files **owns the commit of those files**; the tree is never left dirty for the operator to stash around. This **supersedes the interim stash→ship→pop pattern** (and the now-OBSOLETE `ship-around-fleet-health-dirty-tree` memory note). Option (b) + three binding riders (operator ruling 2026-06-07):

1. **Mutable vs durable split.** The high-churn mutable pointer (`ecosystem/<repo>/state.yaml`) is **gitignored**; the durable record (`history/*.md`, digests, the audit rollup `docs/audits/*-ecosystem-audit.md`) is **committed by the writer**.
2. **Pathspec-bounded.** The job stages **exactly its own declared output paths** — never `git add -A`, never anything outside its outputs. An operator's unrelated dirty files are untouchable by automation.
3. **Fail-soft.** On any commit failure (locked index, mid-merge, diverged `main`) the job leaves its files uncommitted, logs one WARN line, and **exits 0** — it never forces, never pulls/rebases, never resolves.

Local writer commits carry the `Routine: <name>` observability trailer (#123); the cloud channel keeps its PR (above). *Wiring is captured as a follow-up item — not built in the ratifying session.*

### What each tier checks (a green one and a red other are both correct)
<!-- scope: meta -->

| Organ | Scope | Dimension checked | Example signal |
| --- | --- | --- | --- |
| `audit.py` / `fleet_health.py` (deterministic) | the repo **+ its siblings** | structural + **freshness-stamp** health (file present, dot-prefix, `last_reviewed` vs last-edit) | `corp-monorepo canonical_freshness FAIL` (CLAUDE.md edited 06-06, reviewed 06-02) |
| cloud conformance Routine (judgment) | the repo's **own docs only** (self-referential) | **claims-vs-docs** coherence (JOURNAL↔git, living-doc claims↔repo state, BACKLOG closure coherence) | nightly digest `0 high / 0 med / 0 low` |
| dynamic Workflow (judgment) | scoped per invocation | whatever the harness defines (deep audit, migration, checked-twice review) | per-run |

The 2026-06-07 cloud digest reading `0/0/0` while the local baseline shows one `canonical_freshness` FAIL is **not** a contradiction: different **dimension** (claims-vs-docs vs freshness-stamp) **and** different **scope** (hub-self vs corp-sibling, tracked as #100). Per-tier value — findings-acted-on vs noise — is reviewed in the morning funnel (#123).

---

## Ch11. Routine/night deployment standard
<!-- scope: meta -->

How a recurring unattended review runs **in the cloud** (Claude Code Routines), as distinct from the rejected local-scheduler design. ADR-68 chose a *local* Windows Task Scheduler → headless `claude -p` night-agent; that mechanism was **never registered** as a scheduled task and is superseded in reality by the cloud Routine described here (see the `ARCHITECTURE.md` ADR-68 supersession note; the unbuilt local track survives as BACKLOG #85). The standard below is distilled from the nightly-conformance arc (CONTRIBUTING "Nightly outcome management"; JOURNAL 2026-06-05 entries; LESSONS 2026-06-05; `docs/audits/2026-06-05-conformance-nightly-digest.md`).

### The envelope

A nightly Routine deployment is four parts:

1. **Routine** — the cloud-scheduled trigger (a Claude Code Routine, ~03:00 local) that launches the run on a fresh `claude/<task>-YYYY-MM-DD` branch.
2. **Workflow spec** — the orchestration logic committed as `.claude/workflows/<name>.js` (e.g. `conformance-hub.js`): verifier fan-out → adversarial skeptic → digest synthesis.
3. **Action** — the outcome handler (`.github/workflows/nightly-conformance-triage.yml`): diff-guard + auto-merge / triage on the PR the run opens.
4. **SessionStart surfacing** — `scripts/surface_triage.ps1` prints a `[triage] N …` line at the next session start, so the operator touches only findings (CONTRIBUTING "Nightly outcome management").

### Naming

Routine **display names** follow `<repo>: <cadence>-<domain>` — lowercase, kebab-case after the colon, **repo first** so the Routines panel self-sorts by repo. The display name is a **label only**: no contract depends on it (the diff-guard keys off the digest path, the Action off the `claude/*` branch pattern, surfacing off the Issue label — see "The outcome loop"), so a rename is purely cosmetic and safe. Applies to all current and future Routines. Current set: `dev-knowledge: nightly-conformance`, `corp-monorepo: nightly-conformance`.

### Safety envelope — allow-only platform guards, no committed deny

The cloud run is read-only by **platform allow-list**, not by a committed `permissions.deny`. (Contrast the *local* track #85, which uses a session Write/Edit deny + a post-run fleet `git status --porcelain` tripwire — a committed deny is the local pattern.) In the cloud the load-bearing guarantee is the **diff guard**: the Action merges only when `git diff --name-status base...head` is exactly one `A` line matching `docs/audits/*-conformance-nightly-digest.md` — so a mislabeled or lying digest is at worst a document on `main`, never code (CONTRIBUTING "Nightly outcome management"; JOURNAL 2026-06-05).

### Spec-orchestration doctrine — and why code guarantees must sit on the executing path

The native Workflow launcher is **not enabled** in the cloud runtime (re-probed 2026-06-05, still unavailable — `docs/audits/2026-06-05-conformance-nightly-digest.md`). When it is absent the cloud agent **falls back** to reading the `.js` as a *spec* and orchestrating it by hand (spec-orchestration), rather than executing it as code. Doctrine: **native-attempt-first, with a nightly re-probe** of launcher availability.

The contract consequence is load-bearing: **any guarantee written as in-script code is INERT on the fallback path** — the `.js` is read, not run, so a throw-on-mismatch validator inside `conformance-hub.js` never fires in production (LESSONS 2026-06-05, "locate contract guarantees on the path that actually executes"). The real backstop must therefore sit on the **executing path**: the **parser-side fail-closed** in the Action — a missing or unparseable counts marker opens an Issue and blocks the merge rather than guessing. Rule: **put the code guarantee where the bytes actually flow** — for a cloud Routine that means the consumer-side (Action/parser) guard that runs unconditionally, not the generator-side validator that fires only on the native path. An LLM-produced machine contract is pinned in code at **both** ends (a code-built marker the model echoes verbatim + code that validates the echo) and prose is never a parse target (LESSONS 2026-06-05, counts-contract).

### The outcome loop

The Action handles the morning so the operator triages only findings (CONTRIBUTING "Nightly outcome management"):

- **diff-guard** → anything other than exactly one ADDED digest file = guard FAIL → nothing merged, an `Anomalous nightly PR` Issue is opened listing the changed files, the PR is left open for review;
- **clean night** (`survived=0` in the machine-readable marker `<!-- counts: raw=N survived=N killed=N -->`) → the PR is squash-merged automatically and its branch deleted;
- **findings night** (`survived>0`) → the digest is merged too (it is the record) **and** a `nightly-triage` Issue is opened with the digest's Findings + Next-Actions sections;
- **SessionStart surfacing** → `surface_triage.ps1` prints `[triage] N …`; the SessionStart nightly run-health check also reports the last Action conclusion plus a **digest-presence side-effect check** — a green run that wrote no digest is itself an anomaly (JOURNAL 2026-06-05).

### T-shirt model pins

**Unpinned fan-out is a bug.** An unpinned subagent now inherits the **main session model** (measured Opus 4.8 on both the Agent-tool and workflow-engine paths after the `CLAUDE_CODE_SUBAGENT_MODEL=haiku` override was removed — see the gotchas "Per-agent model routing" entry), so an unpinned bulk fan-out silently runs the most expensive tier. On the spec-orchestration fallback path every stage likewise inherits the orchestrating session model (all five conformance stages ran `claude-sonnet-4-6` because that was the session model — `docs/audits/2026-06-05-conformance-nightly-digest.md`). **Native workflow scripts CAN route models per stage** (a per-stage `opts.model`, a separate and now-honored code path); pin deliberately by t-shirt size (S=Haiku / M=Sonnet / L,judgment=Opus — Appendix B; ADR-70) rather than leaning on an inherited default.

### Cloud-session closeout

A cloud run leaves a `claude/<task>-YYYY-MM-DD` branch behind. Closeout convention: **check for stranded `claude/*` branches** (the clean-night path deletes its own branch; a guard-failed or interrupted run does not) and prune the orphans — the cloud analogue of the local no-leftovers invariant (CLAUDE.md §5 #9; staleness-audit "cloud-readiness", `docs/audits/2026-06-05-living-doc-staleness.md`).

### The shallow-clone false-positive class

A cloud runner may produce a **shallow clone**, so a verifier that checks "does commit X exist in history" will falsely report any SHA older than the shallow boundary as **absent** — a false "commit absent" finding, not a real conformance defect. Two guards: (1) the Action sets `fetch-depth: 0` so three-dot `base...head` diffs have both endpoints reachable (`.github/workflows/nightly-conformance-triage.yml`); (2) the `conformance-hub` V1 stage treats SHAs older than the history boundary as **out-of-scope**, not absent (JOURNAL 2026-06-04 "V1 shallow-history guard"). Read a first production raw count with this class in mind (JOURNAL 2026-06-05).

### Cloud-session hub-independence (self-containment)

A cloud Routine **clones only its target repo** (single-repo Linux clone at `/home/user/<repo>/`) and must be **self-contained** — it consults only that repo's own git, living docs, and BACKLOG. **No hub reference is load-bearing on the cloud executing path** (ADR-72, #86 sub-decision 2). The hub `.dev-knowledge` is **private**, which permanently closes ADR-71's "URL-swappable later" hatch *for the cloud case*: a git-source/URL hub would need auth inside the sandbox, which the secrets-boundary stance forbids (treat the sandbox as compromised). So plugin/skill distribution does **not** resolve a private hub in cloud — the `tier1-lifecycle` plugin is **verified inert** there (local-directory marketplace absent on Linux; JOURNAL 2026-06-04, "harmless"), and the `repo: ../.dev-knowledge` pre-commit hooks never fire (pre-commit uninstalled in a fresh clone; a read-only run commits no source). These are inert-**by-design**, not bugs.

The honest catch: that degradation is **silent** (the machinery that would log a no-op is exactly what doesn't run), so the "loud" guard moves to **design/review time** — authoring a cloud spec that reads any `../.dev-knowledge/...` path is a defect a reviewer must catch, and any spec that genuinely needs a hub ref must fail-closed at the consumer/Action layer ("put the code guarantee where the bytes actually flow", above). A future cloud Routine that truly needs hub methodology/tooling at runtime is a **STOP-and-escalate**: it cannot be served for a private hub without publishing a hub subset (an operator data-classification call) or new auth'd infra — do not improvise it in-session (ADR-72 Decision 5).

### What every routine must meet (the operational standard)
<!-- scope: meta -->

A recurring unattended review — local or cloud — graduates to "standard" only when it satisfies **all** of these (ratified by ADR-80):

1. **Self-containment** — consults only its own repo at runtime; no hub reference on the executing path (ADR-72/73; "Cloud-session hub-independence" above). Cross-repo reach is the *local* deterministic baseline's job, not a cloud Routine's.
2. **Declared output channel.** *Cloud:* `claude/<task>-YYYY-MM-DD` branch → PR → Action diff-guard → **squash-merge** (compliant-by-design — witnessed 2026-06-07, PR #17 squash-merged to `main` as `221c63e`; the single non-merge commit is the *designed* cloud channel, distinct from the local branch+merge `--no-ff` discipline for human-authored arcs). *Local:* the writer commits its own pathspec-bounded output, fail-soft ("Two-tier automation doctrine › Writer policy").
3. **`Routine: <name>` commit trailer** on every automation commit, so routine output is git-indexable and value-reviewable (#123).
4. **Per-stage model pins** — every stage pinned by t-shirt size ("T-shirt model pins"); **no `fallbackModel`** on a pinned stage (it breaks evidence comparability — §2 "Model / effort platform doctrine"). Unpinned fan-out is a bug.
5. **Fail-soft + catch-up posture** — a missed run is tolerated by design: catch-up on next opportunity (local: Task Scheduler "run as soon as possible after a missed start", ADR-76; cloud: the next scheduled night), surfaced at the next SessionStart. No alerting, no wake-from-sleep.
6. **Funnel-review as the consuming contract** — findings are *proposals*; the operator's morning funnel ratifies before anything binds, and records per-routine findings-acted-on vs noise (#123). A routine with no funnel consumer is not deployed.
7. **Evidence gate: n=2 before graduation** — a new routine pattern is codified into this standard only after **two real runs** demonstrate it end-to-end (ADR-74 Footnote B meta-rule). The nightly conformance routine cleared this gate (n=1 red 2026-06-06 → triaged → n=2 clean 2026-06-07, both PR'd into `main`); #84 is the codification that consumed it.

---

## Ch12. Definition of done (organs)
<!-- scope: meta -->

Recorded as **ADR-81** (2026-06-09). An organ — a plugin, hook, command, skill, workflow, generator, or convention — is **not DONE** until it has all four:

- **(a) a methodology home** — its rule/doctrine written in PLAYBOOK **sufficiently for a fresh
  session to act on it from that section alone** (existence ≠ sufficiency). Verified at the handoff
  articulation gate — *could a new session do this from the section alone?* — not merely "a section
  exists." (Evidence: #107 shipped a worktree section, yet a fresh chat still could not parallelize
  from it — the transmission gap this clause closes.)
- **(b) a deployment path** — a runbook or documented install sequence;
- **(c) a maintenance/refresh cadence** — how it stays current, and how staleness is detected;
- **(d) actual deployment, OR an explicit documented deferral** that names the gap and what remains.

Stopping at build+test is the **half-feature rot trap**: build-and-test ≠ done. (The routine-specific analog is "What every routine must meet" above — this is its generalization to every organ class.)

### Definition of shipped (closure gate)
<!-- scope: meta -->

ADR-81 (a)–(d) above answers *"is this organ a complete organ?"* This answers the adjacent question *"is this work actually shipped, or only prematurely announced?"* — the **"deployment is half the success"** gate (LESSONS 2026-06-10). "Unit tests pass → announce shipped" is the EASY metric; declaring on it under momentum is the recurring premature-closure failure (the floor saga is the worked example). A feature/arc is **shipped** only when ALL six hold:

1. **Git clean + merged** — branch merged `--no-ff` to `main` and pushed; `upstream..HEAD` empty (LESSONS 2026-06-09 /ship-completion).
2. **Version surfaces coherent** — every coupled version surface agrees with its anchor (`audit.py amendment_coherence` green).
3. **An E2E / user-flow test passes** — the whole sequence exercised as a user would, not only unit tests (**#144**).
4. **Checked against the original expectation in a back-and-forth** — reconciled with what the operator actually asked, not a one-shot self-grade (LLM-LLM transfer is bidirectional — see "LLM-LLM context transfer is back-and-forth, not unilateral").
5. **Records updated** — JOURNAL / LESSONS / ADR / archive reflect the change.
6. **The verification organs RUN green** — `audit-health`, `validate_doc_claims` (#89), `validate_git_backlog` (#90a), `canonical_freshness` actually **executed against THIS arc**, not merely existing. Building an organ ≠ running it on the feature it should guard. **"Organs run green" is class-specific:** hard-fail organs (`audit-health`, `amendment_coherence`) exit 0; awareness organs (`validate_doc_claims`, `validate_git_backlog`) surface no new or undispositioned WARN — a documented pre-existing WARN (e.g. a voided closure pending #139) does not block.

Announcing before (2)–(6) is **premature closure**, not shipped. Point (6) is **operator-enforced discipline until #147** wires it as a pre-ship gate (a hook/command that RUNS the organs and BLOCKS `/ship` on red). De-dup: point (3) E2E = **#144**; codification-completeness of the methodology home = **#145**; #147 = the run-organs-as-gate mechanism — three distinct items.

**Distinct from the per-session close gate:** this "organ done" (ADR-81) and "arc shipped" gate answer *"is this feature/arc complete?"* The adjacent, narrower question *"did THIS session leave the record current?"* has its own single-source — `protocols/DEFINITION_OF_DONE.md` (ADR-85), enforced mechanically by the session-end Stop-hook (JOURNAL SHA-anchor hard block + BACKLOG nudge). Don't conflate the three scopes: organ-completeness, arc-shipped, session-close.

---

## Ch13. Continuous Improvement
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

New tools, models, agents, and patterns emerge constantly in 2025-2026 LLM dev (Claude Code releases, OpenAI Codex updates, Chinese models like GLM/Qwen, MCP servers, multi-agent frameworks, Spec Kit/Kiro). Without explicit process, adoption thrashes (re-evaluating same tool quarterly), forgets context (why did we reject MCP memory?), or misses signals (a relevant tool sits unread for weeks).

This section defines the lifecycle: from "I saw something on Twitter" to "we adopted/rejected/deferred."

### Pipeline overview
<!-- scope: meta -->

Six stages, executed in order. Stages can be implicit (skipped/quick) for low-stakes evaluations; explicit (full ceremony) for high-stakes ones.

```
Discovery → Triage → Evaluation → Decision → Implementation → Review
```

- **Discovery:** something new shows up
- **Triage:** is it worth evaluating?
- **Evaluation:** does it actually solve our problem?
- **Decision:** adopt / reject / defer
- **Implementation:** if adopt — execute via standard pipeline (ADR + work)
- **Review:** periodic re-check that adopted things still earn their keep

### Stage 1: Discovery
<!-- scope: meta -->

**Sources to monitor:**
- Anthropic engineering blog
- OpenAI engineering blog (for Codex / GPT-5.x)
- Karpathy (Twitter)
- Simon Willison (blog)
- Latent Space podcast / blog
- Cursor / Aider / Claude Code release notes
- agents.md / Spec Kit / Kiro initiatives
- Chinese model releases (GLM, Qwen, DeepSeek)

**Cadence:** weekly informal scan. No formal time box.

**Capture:** when something looks interesting, note it informally (a JOURNAL line, or operator scratch) under "discovered, not yet triaged" — don't wait for full evaluation. There is no formal radar inbox (tech-radar retired — see "Where evaluations are recorded").

### Stage 2: Triage
<!-- scope: meta -->

**Criteria for "worth evaluating":**
- **Maturity:** v1.0+, ≥100 GitHub stars, or backed by recognized org
- **Addresses real problem:** maps to existing Rob pain point or unblocks identified gap
- **Scale fit:** works for solo developer (not team-only)
- **Platform fit:** runs on Windows/PowerShell (or has portable equivalent)
- **Cost-bounded:** trial cost <$50 OR API trial available

If 4+ criteria met → proceed to Evaluation (majority-of-6 threshold; ≤3 = not worth evaluation cost). If 3 or fewer → record "deferred" with the reason (a JOURNAL note, or a BACKLOG "Tooling & evaluation" item if it carries a reopen trigger).

**Anti-pattern:** evaluating every novelty. The job of triage is saying no.

### Stage 3: Evaluation
<!-- scope: meta -->

Three evaluation modes — pick by stakes:

**Quick check (Scale S decision):**
- Browser chat reads docs / community feedback
- ~30 min reading + thinking
- Output: yes/no/defer with one-paragraph rationale

**Spike (Scale M decision):**
- Throwaway branch, install tool, attempt real task
- ≤4 hours
- Output: works/fails/uncertain with concrete observation

**Research debate (Scale L decision):**
- AI Council research-mode debate (4 models, 1-2 rounds, ~$0.30-$0.50)
- 30-60 min from brief to synthesis
- Output: routed to `docs/decisions/transcripts/` (ADR-43; `docs/research/` retired per ADR-60 amendment 2026-05-27)

Decision threshold for which mode: per PLAYBOOK Section 5 "When to run Council vs single-model + critic."

### Stage 4: Decision
<!-- scope: meta -->

Three outcomes:

- **Adopt:** triggers Implementation (Stage 5)
- **Reject:** record the reason (an ADR if architectural, else a JOURNAL note); closed unless evidence changes
- **Defer:** record an explicit reopen trigger (e.g., "if cost drops below X" or "after solo→team transition") as a BACKLOG "Tooling & evaluation" item — where deferred tool evals already live (e.g. Kimi K2, the `ecosystem/` model)

**Document the decision:** even rejection deserves a paragraph. Future self asks "why didn't we adopt MCP memory?" — answer must exist.

### Stage 5: Implementation (only for "Adopt")
<!-- scope: meta -->

Standard pipeline:
1. **ADR if architectural impact** (per Section 5 gating) — module boundaries, dependencies, data model
2. **Brief Stream B-style gap entry** if it requires multiple changes across files
3. **Updates to:** CLAUDE.md (Slash commands §7, Skills §8, or Hooks §9 as applicable), ENVIRONMENT.md (if env-level), JOURNAL entries
4. **Hooks/tests/CI** if enforcement needed (LLMs advise; mechanism enforces, per Council #28)

Cross-link the ADR to its implementation commits; the JOURNAL entry records the adoption (the `Changes:` line replaces the retired CHANGELOG — §14).

### Stage 6: Review (on-trigger)
<!-- scope: meta -->

**Cadence:** the quarterly tech-radar snapshot is **retired** — `docs/tech-radar/` is gone, its dated research notes archived directly under `docs/archive/` (no dedicated `tech-radar/` subfolder; ADR-60 — it held one dormant entry and never ran on a real cadence; reversible if a quarterly cadence ever resumes). Review is now **on-trigger**, not scheduled: re-examine an item when its reopen trigger fires, when it visibly stops earning its keep, or when a replacement appears — not on a calendar.

**When an Adopted item is reviewed:**
- Still earning its keep? (concrete value vs cost/maintenance)
- Configuration drift? (deprecated flags, version skew)
- Replacement candidate emerged?

**When a Deferred item's reopen trigger fires:**
- Re-triage it (Stage 2).
- Still relevant, or made obsolete by an alternative already adopted?

**Rejected items:**
- Re-open only if the rejection reason no longer holds ("wrong reason at the time" — rare but happens).

**Where it lands:** the outcome is recorded where the decision lives — an ADR (architectural), a BACKLOG "Tooling & evaluation" update (deferred items), or a JOURNAL note. No separate radar inventory to maintain.

### Where evaluations are recorded
<!-- scope: meta -->

`docs/tech-radar/` is retired (its dated research notes live directly under `docs/archive/` — there is no `docs/archive/tech-radar/` subfolder — per ADR-60; reversible if a quarterly cadence ever resumes), and `docs/research/` is retired (ADR-60 2026-05-27 amendment). With no separate radar inventory, an evaluation's record lives where its decision lives:
- **ADRs** in `docs/decisions/` — the adopt/reject decision itself (research-mode debate transcripts route to `docs/decisions/transcripts/` per ADR-43).
- **BACKLOG** "Tooling & evaluation" theme — deferred tool evals carrying their reopen triggers (e.g. Kimi K2).
- **JOURNAL** — the per-session record of what was evaluated and decided.

---

## Ch14. Claude Code internals
<!-- scope: runtime -->
<!-- version: 1.0 — 2026-04-24 -->

Claude Code (Anthropic's terminal-based agentic coding tool) has four extension mechanisms with confusingly similar names. Rob and Claude have repeatedly conflated them in 2026 sessions. This section establishes canonical definitions, locations, use cases, and the existing examples in Rob's ecosystem.

### Quick disambiguation
<!-- scope: runtime -->

| Mechanism | What it is | Where it lives | Trigger |
|-----------|-----------|----------------|---------|
| **Skill** | Progressive-disclosure knowledge module | `.claude/skills/<name>/SKILL.md` | Read on-demand by Claude Code when topic matches |
| **Slash command** | Custom invokable command | `.claude/commands/<name>.md` | Rob types `/<name>` |
| **Hook** | Lifecycle automation | `.claude/settings.json` OR `.pre-commit-config.yaml` | Auto-fires on event (PreToolUse, pre-commit, PostToolUse) |
| **Subagent** | Separate Claude instance with narrow focus | `.claude/agents/` | Invoked via Agent tool (formerly Task tool; Task(...) remains an alias) from main agent |

**User-level vs project-level:**
- User-level: `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/settings.json` — applies across all repos
- Project-level: `<repo>/.claude/skills/`, `<repo>/.claude/commands/`, etc. — applies only in that repo
- Both can coexist; project-level takes precedence when names collide

### Usage protocol: which command / hook, when
<!-- scope: runtime -->
<!-- version: 1.0 — 2026-06-01 -->

7a–7d say what each mechanism *is*; the Adoption protocol says how to *add* one. This is the mid-session "which do I reach for, and does it fire on its own?" map, grounded in the live `~/.claude/` + repo `.claude/` contents (2026-06-01). When it drifts from `ls ~/.claude/commands ~/.claude/skills`, **the filesystem wins** — re-ground before trusting the table.

**Commands** — you type `/<name>`; nothing fires them for you:

| Command | Level | When to invoke |
|---------|-------|----------------|
| `/session-summary` | user | Session end / handing to browser chat (Path A). Also appends a TOKEN-LOG snapshot if >7 days stale. |
| `/code-review high` | user (built-in) | **In-flight / interim** leg of the two-stage code review — a correctness + reuse pass on the working diff mid-session, before you commit/ship. Pairs with `/codex-review` (the final leg). |
| `/codex-review` | user | **Final / pre-ship** leg of the two-stage review: before merging a **code** change (3+ files / safety-critical). Code only — never a markdown-only diff (LESSON 2026-05-19). |
| `/save` | repo | Stage + commit with a Conventional Commits message + full body (git-discipline rule). After a discrete change. |
| `/ship` | plugin (`tier1-lifecycle`) | Git-finish from the PRIMARY checkout: merge the current feature branch `--no-ff` → push → **auto-delete the merged branch** (no question). Branch cleanup is automatic; an anomalous `git branch -d` refusal is **reported loudly** and the branch left in place (session still ends). Refuses from inside a worktree (pre-flight #1). |
| `/handoff` | repo | CC-owned handoff per HANDOFF_PROCESS v5 (ADR-82): "create handoff" → "complete handoff" — emits the residual + probe manifest + points at the thin boot. At ~2h, context still fresh. |
| `/changelog-review` | repo | Operator-invoked review of tool changelogs (claude-code + codex) since last review — classify per the audit rubric, write a digest, bump the state file. PUSH-triggered (a SessionStart sentinel surfaces "run /changelog-review"); never implements adoptions. |

**Skills** — read on-demand by Claude when the topic matches; you do **not** invoke them:

| Skill | Level | Fires |
|-------|-------|-------|
| `gotchas` | user | Auto-consulted before edits when an encoding / shell / test-pitfall pattern is in play. |
| `verify` | repo | Domain verification scripts for the ecosystem (`.claude/skills/verify/`); consult/run after `pytest` passes. |

**Subagents** — Task-tool, read-heavy / write-light (`ecosystem-snapshot`, `report-generator`, both Haiku, user-level): invoke for read-only fan-out (snapshots, report condensation), never as code-gen peers (7d).

**Hooks** — auto vs manual: **every hook fires automatically; none are operator-invoked.** The canonical, drift-tracked roster lives in **CLAUDE.md §9** — the live pre-commit gate set, the project-level SessionStart/Stop/PreToolUse session layer, the pre-push prevent organ, and the `.claude/rules/` — read it there rather than maintaining a duplicate copy here (this table re-drifted twice: a self-stamped enumeration of "6 hooks" while the live config carried 10, and rows describing the retired `/boot`+`/evolve` machinery — the failure this pointer exists to kill). The operational "when":

- **Pre-commit gates** fire on `git commit`. Two **BLOCK** (`audit-health` on FAIL, `ruff` on violation); the rest normalize, validate, or surface (run `ruff check --fix` / `/save` to auto-fix lint before committing).
- **commit-msg** gate (`backlog-id-on-close`) requires `[#id]` when a commit removes a backlog task.
- **pre-push** prevent organ (`block-ff-push`) refuses a non-merge commit onto main's first-parent spine (one-time local activation: `pre-commit install --hook-type pre-push`).
- **Session hooks** (`~/.claude/` + the project `.claude/settings.json` layer) fire at SessionStart (surfacing — fleet/triage/billing/changelog), Stop (back-pressure + notify), and PreToolUse (the OneDrive guard + transcript-immutability guard).

CLAUDE.md is the inventory authority — §7 (commands), §8 (skills), §9 (hooks); this is the operational "when". Adding/removing any of them follows the Adoption protocol below and updates both surfaces.

### 7a. Skills (progressive-disclosure knowledge modules)
<!-- scope: runtime -->

**What:** Knowledge modules Claude Code reads on demand when context matches a trigger pattern. Designed for content too large for CLAUDE.md but reusable across sessions.

**Structure:**
```
<repo>/.claude/skills/<skill-name>/
  SKILL.md          # main file, <500 lines, trigger description + instructions
  references/       # additional content loaded only when needed (progressive disclosure)
  scripts/          # auxiliary executables if applicable
  examples/         # concrete examples Claude can study
```

**SKILL.md format (top of file):**
```
---
name: <skill-name>
trigger: <when does Claude Code load this — e.g. "before making changes to module X" or "when user asks about Y">
---

# <Skill Title>

[content]
```

**When to use:**
- Empirical patterns ("things this repo gets wrong" — see Rob's `gotchas` skill)
- Domain-specific knowledge that recurs across sessions
- Workflows too long for CLAUDE.md (which has ≤200 lines target per Council #28)

**When NOT to use:**
- Knowledge that fits in CLAUDE.md (≤200 lines budget) — keep there for auto-read
- Universal Rob rules — those go in `.dev-knowledge/protocols/PLAYBOOK.md`
- One-off task — slash command may fit better

**Real example in Rob's ecosystem:**
- `corp-monorepo/.claude/skills/gotchas/SKILL.md` — empirical patterns this repo has stumbled on (Trigger/Symptom/Fix/verify pattern)

**Anti-patterns:**
- **Skill files >500 lines** — defeats progressive disclosure; split to references/
- **Skills with no trigger description** — Claude Code can't know when to read it
- **Universal content as project skill** — should live in `.dev-knowledge/protocols/PLAYBOOK.md` instead

### 7b. Slash commands (custom invokable commands)
<!-- scope: runtime -->

**What:** Markdown files defining commands Rob can invoke by typing `/<name>` in Claude Code. Each command is a templated prompt Claude Code executes.

**Structure:**
```
~/.claude/commands/<name>.md   # user-level (cross-repo)
<repo>/.claude/commands/<name>.md   # project-level
```

**File format:** Just markdown. Body is the prompt Claude Code follows when command invoked. May contain `$ARGUMENTS` placeholder for command-line args.

**When to use:**
- Repeated workflow Rob runs >3× across sessions
- Multi-step procedures that benefit from consistent prompt
- Operations crossing multiple files/tools (e.g. `/session-summary` context loading)

**When NOT to use:**
- One-off task — write inline prompt instead
- Knowledge lookup — use skill instead
- Content best fits CLAUDE.md auto-read

**Real examples in Rob's ecosystem (level noted per entry — user = `~/.claude/commands/`, repo = `./.claude/commands/`, plugin = `tier1-lifecycle`):**
- `/session-summary` (user) — generate handoff for current session, include `logs/TOKEN-LOG.md` snapshot if stale (renamed from `/handoff` 2026-04-24 to avoid trigger-word collision)
- `/codex-review` (user) — invoke Codex review on staged code changes
- `/save` (repo) — stage + commit with a Conventional Commits message + full body (git-discipline)
- `/handoff` (repo) — CC-owned handoff per HANDOFF_PROCESS v5 (ADR-82): create → complete
- `/override` (repo) — logged, HEAD-bound bypass of the ADR-85 session-end gate (the gate's only escape)
- `/ship` (plugin) — git-finish: merge the feature branch `--no-ff` → push → auto-delete it (refuses inside a worktree)
- `/review-closures` (plugin) — review + execute operator-approved session-end closures (ADR-70 Tier-1)
- `/verify` (skill) — run the standard pytest + ruff + git-status check cadence

> **Retired machinery (history; do not re-add to command tables/cheat-sheets):** `/boot` and `/evolve` were archived 2026-06-05 (Phase-C3) — the self-evolution loop they drove (memory / learned-rules promotion + per-session boot) is retired. Archive: `~/.claude/archive/2026-06-05-machinery-c3/`.

**Anti-patterns:**
- **Commands without clear naming** — `/x` or `/do` are unmemorable
- **Trigger-word collisions** — `/handoff` matched user typing "handoff" in conversation; renamed to `/session-summary` (lesson 2026-04-24)
- **Treating commands as skills** — commands are invoked actions; skills are read-on-demand knowledge

### 7c. Hooks (lifecycle automation)
<!-- scope: runtime -->

**What:** Automated actions firing on Claude Code lifecycle events or git lifecycle events. LLMs advise; hooks enforce (per Council #28 community finding).

**Two flavors:**

**Claude Code hooks** — fire on tool/agent lifecycle:
- Location: `.claude/settings.json` (user or repo)
- Events: PreToolUse, PostToolUse, others per Claude Code docs
- Use case: enforce rules before/after Claude takes specific actions

**Pre-commit hooks** — fire on git commit:
- Location: `.pre-commit-config.yaml` (repo root)
- Framework: pre-commit.com (Python tool, cross-platform)
- Use case: enforce rules before code/docs land in repo

**When to use:**
- Mechanical enforcement of governance rules (scope tags, lint, test pass)
- Safety nets — block accidental violations LLM advice alone might miss
- Cost: hooks run on every commit; keep fast (<5 seconds typical)

**When NOT to use:**
- Rules best left as LLM advice (subjective conventions where context matters)
- Heavy validation (>30s) — moves to CI/CD instead
- Ambiguous rules — hooks fail loudly; vague rule = constant friction

**Real examples in Rob's ecosystem:**
- `.dev-knowledge/.pre-commit-config.yaml` — `normalize-dated-headers`, `codemap-freshness`, `validate-backlog`, `audit-health` (the [#69] self-conformance gate), `ruff` (lint gate — blocks on violations; [#13] closed), `backlog-id-on-close` (commit-msg). (scope-tag enforcement withdrawn per ADR-48; CLAUDE.md §9 is the full live hook roster.)
- corp-monorepo pre-commit (likely): ruff format, pytest collection check (verify per repo)

**Anti-patterns:**
- **Hooks bypassed with `--no-verify`** — defeats the safety net; should never be habit
- **Hooks slower than 5s** — incentivizes bypass; move to CI
- **Validator/hook divergence** — both tools must enforce identically (see ADR-27 amendment 2026-04-25, lesson re: invocation semantics)

### 7d. Subagents (separate Claude instances)
<!-- scope: runtime -->

**Amendment 2026-04-25 (subagents factually active):** Original v1.0 section called subagents "DEFERRED — no active subagents in Rob's ecosystem." This was incorrect. Verification 2026-04-25 confirmed two active user-level subagents exist at `~/.claude/agents/`. Section now describes actual subagents (Anthropic docs framing preserved as conceptual context). Per Gap #19 amendment-vs-reopen protocol: prescription drift, intent (disambiguation of 4 mechanisms) preserved.

**What (per Anthropic docs + Council #28 research):** Subagents are spawned Claude instances with narrow focus and fresh context window, invoked via main agent's Agent tool. Designed for "read-heavy, write-light" delegation (per Cognition's June 2025 warning against subagents-as-code-generation-peers).

**Where they live:** `~/.claude/agents/<name>.md` (user-level, cross-repo) OR `<repo>/.claude/agents/<name>.md` (project-level).

**Distribution doctrine (extends ADR-71):** agents are **authored and versioned in the hub**; they distribute **user-level (`~/.claude/agents/`) for cross-repo** organs and **via the `tier1-lifecycle` plugin for repo-class** organs. **Children consume, never author.** Library admission is gated by the Discovery→Review funnel + *used-in-anger* evidence — the small **ACTIVE**-roster guard is unchanged (headcount is an anti-goal; leverage is the admission test).

**File format:** Markdown files describing the subagent's role, trigger conditions, and instructions. Main agent invokes them via Agent tool.

**When to use:**
- Read-heavy operations (code search across large codebase, log analysis, doc lookups)
- Tasks benefiting from fresh context window (avoid main agent's context bloat)
- Operations that should not write/modify (per Cognition warning — subagents as readers, not collaborators)

**When NOT to use:**
- Code generation peers (anti-pattern per Cognition June 2025)
- Tasks that need main agent's full context (e.g. complex refactoring with cross-file knowledge)
- One-off operations — slash command may fit better

**Real examples in Rob's ecosystem (user-level, `~/.claude/agents/`):**
- `ecosystem-snapshot.md` — read-only point-in-time snapshot generator across all Corporate OS repos (git status, recent commits, test counts, dirty files); Haiku model; outputs facts only, refuses analysis
- `report-generator.md` — read-only structured report builder for weekly ecosystem reports and data condensation; Haiku model; markdown tables with source paths, escalates architectural reasoning back to main session

**Anti-patterns:**
- **Subagents as code-generation peers** — they diverge, conflict, waste tokens (Cognition's "Don't Build Multi-Agents" warning, June 2025)
- **Heavy write operations in subagents** — main agent loses sight of state changes; coordination breaks
- **Overusing subagents** — main agent + skills + slash commands sufficient for most workflows; subagents are specialist tool, not default

**For deeper guidance:**
- Anthropic Claude Code subagents documentation
- Cognition "Don't Build Multi-Agents" (cognition.ai blog, June 2025)
- Stream B Gap #10 (Adoption protocol) — applies to subagent additions/changes

### Adoption protocol — when Claude Code proposes a new skill/command/hook/subagent
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

When Claude Code observes a recurring pattern and suggests adding a skill, slash command, hook, or subagent, this protocol decides scope (user-level vs project-level), validates the addition, and ensures it's documented in the right places. Companion to subsections 7a-7d above (what they are) — this is "how to add one safely."

**Distinct from the unnumbered "Continuous Improvement" section above** — that covers external tool/model adoption (Codex, Tach, ccusage). This subsection covers Claude Code's own extension mechanisms. (Not §6, which is "Code Review".)

#### Triage: is the proposal worth adopting?
<!-- scope: meta -->

Adopt when ALL apply:
- **Pattern recurs** — Rob has done the same thing ≥3 times across sessions, OR Claude Code recognizes it'll save ≥5 prompts in next month
- **Stable interface** — what the skill/command/hook does won't change drastically next month
- **Clear scope** — fits one of the four mechanisms (Gap #7a-d) without forcing
- **Documentable** — Rob can explain in one sentence what it does and when

Reject if any:
- One-off pattern unlikely to recur
- Interface still evolving (premature to codify)
- Hybrid of multiple mechanisms (might be 2 separate additions instead)
- Better solved by updating CLAUDE.md or PLAYBOOK directly (not all knowledge needs an extension mechanism)

Defer if:
- Pattern looks valuable but Rob hasn't tried it manually enough times to validate friction is real
- Reopen trigger: after N more occurrences (set explicit count)

#### Decision: user-level vs project-level
<!-- scope: meta -->

**User-level** (`~/.claude/<mechanism>/`) when:
- Pattern applies across all repos Rob works in (.dev-knowledge, corp-monorepo, ai-council, future)
- Universal Rob workflow (e.g. `/session-summary`)

**Project-level** (`<repo>/.claude/<mechanism>/`) when:
- Pattern is repo-specific (corp-monorepo Tach layers, ai-council debate framework)
- Sensitive content shouldn't leak to other repos
- Repo's CLAUDE.md needs to reference it explicitly

When unclear: start project-level (lower blast radius), promote to user-level if pattern proves universal across 2+ repos.

#### Validation: does it actually work?
<!-- scope: meta -->

Before "adopted":
1. **Smoke test** — invoke the mechanism in its intended scenario; verify behavior matches description
2. **Side-effect check** — does it interfere with existing workflows? (e.g. trigger-word collision: `/handoff` → `/session-summary` rename 2026-04-24 happened because trigger phrase matched user typing)
3. **Speed check** — hooks <5s; skills/commands <50KB SKILL.md; subagents fresh-context appropriate
4. **Failure mode** — what happens when mechanism fails? Graceful or noisy?

If any fails: reject or iterate before adopting.

#### Install: where the file lands
<!-- scope: meta -->

Per mechanism (cross-reference subsection 7a-7d for full structure):

| Mechanism | User-level path | Project-level path |
|-----------|-----------------|---------------------|
| Skill | `~/.claude/skills/<name>/SKILL.md` | `<repo>/.claude/skills/<name>/SKILL.md` |
| Slash command | `~/.claude/commands/<name>.md` | `<repo>/.claude/commands/<name>.md` |
| Hook (Claude Code) | `~/.claude/settings.json` | `<repo>/.claude/settings.json` |
| Hook (pre-commit) | n/a (always project-level) | `<repo>/.pre-commit-config.yaml` |
| Subagent | `~/.claude/agents/<name>.md` | `<repo>/.claude/agents/<name>.md` |

#### Document: where to link
<!-- scope: meta -->

After install, link from:
- **CLAUDE.md** (Slash commands §7, Skills §8, or Hooks §9 as applicable) — for project-level adoptions; keeps Codex aware of active governance
- **CLAUDE.md** — for project-level Claude Code-specific behavior (per Gap #5 template Slash commands, Skills, and Hooks sections)
- **JOURNAL.md entry** for the session that adopted it
- **JOURNAL.md `Changes:` line** for repo-visible adoptions (CHANGELOG retired — §14)
- **JOURNAL.md** for user-level adoptions too (they need no per-repo CLAUDE.md); file a BACKLOG "Tooling & evaluation" item if it warrants periodic value review (tech-radar retired — see §Continuous Improvement)

User-level adoptions don't need per-repo CLAUDE.md updates (they apply everywhere automatically); record them in JOURNAL, and file a BACKLOG "Tooling & evaluation" item if they warrant periodic value review.

#### Anti-patterns
<!-- scope: meta -->

- **Adoption without triage** — every Claude proposal becomes a new file; ecosystem bloats
- **Project-level when should be user-level** — duplicates same skill across 3 repos; one source of truth lost
- **User-level when should be project-level** — leaks repo-specific knowledge into universal scope
- **Skip validation** — broken hook/command/skill propagates and fails silently for weeks
- **Forget documentation step** — Codex/Cursor never learn about the new tool; cross-tool awareness breaks

### Cross-reference to CLAUDE.md tools sections
<!-- scope: meta -->

When a repo has any of the above active (skills, slash commands, hooks, subagents), they get listed in the relevant CLAUDE.md sections: Slash commands (§7), Skills (§8), or Hooks (§9). Specifically:

- **Code review:** Codex configuration → see `templates/codex-review-config-template.md`
- **Architecture enforcement:** Tach configuration if used
- **Pre-commit hooks:** list active hooks with purpose
- **Skills:** list active skills with paths
- **Subagents:** list if any are active (per Rob's ecosystem currently: ecosystem-snapshot, report-generator at user-level)

This keeps Codex aware of the same governance Claude Code operates under.

---

## Part II — Workflows
*Numbered, repeatable recipes (§1–§19) plus Appendices A–C and tooling addenda. These are step-by-step procedures, not reference doctrine.*

## 1. Starting a New Project
<!-- scope: dev -->

**Every project begins with CLAUDE.md, not code.** If you can't describe what the project does in 3 sentences, you don't understand it yet. For architectural decisions (new database? new package? new integration?), run an AI Council debate before writing a single line.

### Scaffold
<!-- scope: dev -->

```bash
mkdir -p my-project/src/my_package my-project/tests my-project/config my-project/scripts
# Universal governance baseline (ADR-38 A5): VISION/CLAUDE/ARCHITECTURE/BACKLOG mandatory.
# README optional (external-audience repos only); no CHANGELOG (retired — §14).
touch my-project/{CLAUDE.md,VISION.md,ARCHITECTURE.md,BACKLOG.md,pyproject.toml,.gitignore}
touch my-project/src/my_package/{__init__.py,cli.py}
touch my-project/tests/conftest.py
```

### CLAUDE.md template (minimum viable)
<!-- scope: dev -->

```markdown
# CLAUDE.md — project-name

## What this project does
[3 sentences max]

## Architecture
[Folder layout table]

## Dev standards
- Python 3.11+, type hints
- pyproject.toml for deps
- ruff for linting, pytest for testing
- Click for CLI, Rich for output
- Logging not print, dataclasses not dicts
- Config in YAML not hardcoded

## Key commands
[How to run, test, lint]

## What NOT to do
- Do not create files outside src/, tests/, config/, scripts/
- Do not hardcode paths
- Do not commit output/generated data
- Do not skip tests between changes

## Folder governance
- docs/: project-level governance, handoffs, decision records, architecture
- output/: gitignored, disposable
- Every generated .md file needs a date (filename or frontmatter)

## Global skills
Before modifying code, read ~/.claude/skills/gotchas/gotchas.md
```

### First commit, then dev loop
<!-- scope: dev -->

```bash
git init && git add -A && git commit -m "feat: scaffold project-name"
```

Then for each feature:
1. Branch: `git checkout -b feat/feature-name`
2. Write test stub FIRST (even `def test_thing_exists(): assert hasattr(module, 'thing')`)
3. Implement
4. Test: `pytest -x --tb=short`
5. Lint: `ruff check src/ tests/ --fix`
6. Commit: `git commit -m "feat: description"`
7. Merge: `git checkout main && git merge feat/feature-name`
8. Delete branch; prepend a JOURNAL entry if files changed (CHANGELOG retired — §14)

---

## 2. Creating a Claude Code Prompt
<!-- scope: hybrid -->

**The prompt skeleton below is CC's consumption-spec** — the contract for what a *complete* prompt contains and the shape CC works from, **not** a checklist the architect hand-authors top to bottom. Front-loading the spec still eliminates 2-3 discovery turns and the skeleton's shape stays non-negotiable; but per **ADR-87** the architect's actual output is thinner — CC self-loads the code-impact context and generic gotchas and fills the skeleton itself. What the architect emits (and the one gap CC can't self-infer) is the next subsection. Every formal prompt still resolves to a summary table that determines execution parameters.

### Architect output vs CC consumption-spec
<!-- scope: hybrid -->

Per **ADR-87** (the architect↔CC equilibrium contract). STEP 1 verified CC self-loads context **reliably only for code-impact tasks**; read-only, governance-context, and execution-time gotcha self-load are unreliable. So the labor splits:

- **The architect emits:** *intent* · *closure* (what done looks like) · *anti-patterns* · the **plan/auto mode** (with its basis — "How to choose Mode" below) · a **thin per-task governance-pointer** (the specific ADR / LESSONS entry / sibling-spec this task touches — CC won't self-infer it).
- **CC owns:** *code-impact context* (the files/tests it self-loads) · *generic gotchas* · the **skeleton** (this section's structure) · *model/effort*.

**Intent-only is conditional.** For a code-impact task, intent + mode (+ pointer if governance applies) is enough — CC self-loads the rest. For a **read-only, governance-touching, or gotcha-sensitive** task the thin governance-pointer is **required** — omitting it regresses the gap CC cannot close from inside the repo. The mode is the architect's judgment: state it **and** its basis (plan when uncertain / multi-file / unfamiliar; auto when a trivial one-sentence diff — the criterion is "How to choose Mode" below, not restated here). Full rationale + the self-load finding: **ADR-87**.

### Summary table (required at top of every formal prompt)
<!-- scope: hybrid -->

```
| Parameter | Value                               |
| --------- | ----------------------------------- |
| Model     | Sonnet / Opus                       |
| Mode      | auto-accept / plan-then-auto / plan |
| Effort    | low / medium / high / xhigh / max   |
```

### How to choose Model
<!-- scope: llm -->

- **Sonnet** for: mechanical work ("apply this fix"), single-file edits, well-specified implementation, pattern-matched code, boilerplate, file renames, config updates, code-and-test loops where the spec is detailed.
- **Opus** for: audit / review / synthesis tasks; architecture decisions and clause-level reasoning; judgment-heavy work (severity calibration, ambiguity resolution); long-context comparison across multiple inputs; subtle pattern recognition (security review, gotcha identification); multi-package changes; complex debugging; novel logic design.

Rule of thumb: if the task is "do X the way we always do it" → Sonnet. If the task is "figure out the right approach, then do it" → Opus.

**Actively choose per task; do NOT default to Sonnet.** There is no budget ceiling per the LLM-spend rule. When uncertain, lean Opus — Sonnet's failure modes (missed nuance, factual misses) cost more than Opus's overhead.

### When to escalate to a Dynamic Workflow
<!-- scope: llm -->

The Sonnet/Opus model ladder has a third rung — *the orchestration tier*. Escalate execution to a **scoped Dynamic Workflow** (the Claude Code `Workflow` tool: Claude writes a JS harness — `agent()` / `parallel()` / `pipeline()` — that a runtime drives in the background, coordinating many subagents while the session stays responsive) when **any** of these hold:

- **(a) Scale** — the task needs more agents than one conversation can coordinate (fan-out across many files / rules / sources).
- **(b) Reusable artifact** — the orchestration is worth keeping as a rerunnable, diffable artifact (saved to `.claude/workflows/` project-shared, or `~/.claude/workflows/` personal, as a slash command) rather than an ephemeral conversation.
- **(c) Adversarial quality** — result quality justifies independent cross-checking (skeptic / refuter agents try to break each finding before it lands).

**Stay with a subagent or skill** when the task is bounded, the split is already known, and token economy matters — a workflow spends substantially more tokens, so pilot on a small slice first (one directory / one narrow question).

The ladder, one line per rung:

| The ask | Route |
| --- | --- |
| "do X the way we always do it" | Sonnet |
| "figure out the approach, then do it" | Opus |
| "too big for one pass / needs independent verification" | scoped Workflow |

**Boundary — heavy-execution, not heavy-decision.** The AI Council remains the heavy-**decision** organ (judgment, ADRs); the workflow is the heavy-**execution** organ — workflows do not creep into Council's role. A tournament / multi-angle workflow may *select among artifacts* (competing drafts judged pairwise), but the binding decision still routes to Council. Inside a workflow the same model split applies *per stage* (t-shirt pins — see "Routine/night deployment standard › T-shirt model pins").

Source: research note `docs/archive/2026-06-03-dynamic-workflows-research-note.md` §5 — the escalation criterion falls straight out of S1's comparison table; the six-pattern taxonomy (incl. *tournament*) is official Anthropic vocabulary per S5. See also ADR-70 (Tier-3), ADR-67 (Council).

> **Forward-pointer — decision-routing family.** This is the heavy-execution rung of the repo's decision-routing ladder. Its two siblings — the convene-vs-Path-A criterion (#18) and the cost/value relax-vs-gate criterion (#27) — are not yet written; when they land they belong **alongside this rule** as the same routing family. (#74's Done-when names that co-location; #18/#27 did not exist when this rung was written.)

### How to choose Mode
<!-- scope: runtime -->

- **auto-accept** — read-only tasks, mechanical changes with clear spec, file moves/renames, formatting. You know exactly what should happen, Claude just executes
- **plan-then-auto** — design decisions embedded in a prompt. Start in plan mode for the UNDERSTAND + PLAN phases, review the plan, then switch to auto-accept for execution. This is the default for most multi-step prompts
- **plan** (manual approval each step) — risky operations touching production data, OneDrive paths, database migrations, anything with blast radius. Also for learning/exploration where you want to see each step

### How to choose Effort
<!-- scope: hybrid -->

- **low** — single file, <30 min, no architectural decisions. Example: "add a CLI flag", "fix this test", "rename this variable across the file"
- **medium** — 2-5 files, 30-90 min, may involve design choices within known patterns. Example: "add a new CLI command", "refactor this module to use dataclasses"
- **high** — 5+ files or 2+ packages, 90+ min, requires UNDERSTAND phase, potential blast radius. Example: "implement search federation", "migrate classifier to new taxonomy"
- **xhigh** — hardest debugging, end-to-end pipeline verification, Council-level analysis. Opus only. Example: "find why magistrala silently drops events", "verify boundary enforcement across all packages"
- **max** — the top effort rung above `xhigh` (live effort ladder: `low / medium / high / xhigh / max`). Reserve for the hardest single-session synthesis where even `xhigh` under-resolves; burns the most tokens, use deliberately.

### Model / effort platform doctrine (Claude Code 2.1.x)
<!-- scope: hybrid -->
<!-- last-verified: 2026-06-23 -->

Platform-current facts that pin the tables above (Claude Code 2.1.186; refreshed for #84 from `docs/audits/2026-06-07-platform-max-audit.md`). The pins below are dated by the `last-verified` stamp — re-ground them against `claude --version` and the live tool schemas before trusting:

- **Opus 4.8 is the default model and defaults to `high` effort.** Don't treat "use Opus" as exceptional for judgment work — it's the floor. Reserve the explicit Effort knob mainly for moving *off* `high`.
- **Implementation waves run on Opus, not Sonnet.** A wave that wires multiple items across hooks / platform config (commit-msg hooks, pre-commit `language` modes, git pathspec behavior on Windows) carries real debugging risk: the failure modes are platform-specific and *silent*. Witnessed 2026-06-07 (wave-A closeout) — the `backlog-id-on-close` `pass_filenames` gate-bypass, the `language:python` flat-layout `pip install .` trap, and the Windows glob-pathspec miss each surfaced only under careful multi-step debugging. Tier these as Opus from the start; Sonnet under-resolves the multi-layer interactions. (Gotchas captured under "Pre-commit hook authoring" + "Git".)
- **`xhigh`** is for the hardest *single-session* synthesis — clause-level architecture, end-to-end verification, this-codification class. It burns more tokens than `high`; use it deliberately, not by default. **`max`** is the rung above it (top of the live `low / medium / high / xhigh / max` ladder) — reserve for cases even `xhigh` under-resolves.
- **Fast mode** (`/fast`) trades token cost for output speed on Opus 4.8/4.7/4.6 — same model, faster output (it does *not* downgrade to a smaller model). Use it for latency-sensitive interactive work; skip it for routine/unattended work where speed buys nothing. *(The historical ≈2× cost / ≈2.5× speed multipliers are unverified — pending re-check for Opus 4.8; do not treat as a current pin.)*
- **`ultracode` is the Dynamic-Workflow trigger keyword, NOT an effort tier** (renamed from "workflow", Claude Code 2.1.160). It escalates a prompt into multi-agent orchestration ("When to escalate to a Dynamic Workflow", above) — never write it in a Model/Mode/Effort table as a fourth effort level.
- **`fallbackModel` policy (ADR-80; VF-2 confirmed schema-accepted on 2.1.168 — the native `--fallback-model` flag is its CLI twin):**
  - **Interactive sessions MAY set it** (e.g. one Sonnet fallback) for resilience when the primary is overloaded/unavailable — a degraded answer beats a dead session.
  - **Pinned routine / workflow stages MUST NOT set it.** A per-stage model pin (t-shirt routing — "Routine/night deployment standard › T-shirt model pins") is a deliberate evidence choice; a silent fallback to a different model breaks **evidence comparability** across runs (the n=2 gate compares like-for-like). A pinned stage that can't reach its model must fail loudly, not silently substitute.

### Structure
<!-- scope: hybrid -->

```
LEGEND  [A] = architect emits  ·  [CC] = CC self-loads  (per the ADR-87 split above)

| Parameter | Value  |   <- Mode is [A]; Model + Effort are [CC]
| --------- | ------ |
| Model     | [pick] |
| Mode      | [pick] |
| Effort    | [pick] |

[A]  TITLE: What we're doing
[A]  REPO: Which repo/package
[A]  PURPOSE: Why (1 sentence)

[CC] → Read CLAUDE.md + relevant gotchas
[A]  → Governance pointer: the ADR / LESSONS / sibling-spec this task touches (architect fills; required for read-only/governance tasks — ADR-87)
[CC] → Git workflow (branch, commit per step, pytest between)
[CC] → Hooks/commands in play: which auto-fire (pre-commit gate: audit-health/validate-backlog; block-onedrive on Bash) + which to invoke (/save to commit; /codex-review before merging code) — see §"Usage protocol: which command / hook, when"

[A]  UNDERSTAND:
- What's the problem?
- What's the scope? (which files, which packages)
- What are the risks?
- What does failure look like?

[A]  STEPS:
1. [action] — COMMIT: "feat: description"
2. [action] — COMMIT: "feat: description"
...

[CC] FINAL: Run full test suite, merge to main

[A]  WHAT NOT TO DO:
- [explicit anti-patterns for this task]
```

### Quick-reference examples
<!-- scope: hybrid -->

| Task                              | Model  | Mode           | Effort |
| --------------------------------- | ------ | -------------- | ------ |
| Fix typo in config                | Sonnet | auto-accept    | low    |
| Add CLI flag to existing command  | Sonnet | auto-accept    | low    |
| Write tests for untested module   | Sonnet | auto-accept    | medium |
| Refactor module to dataclasses    | Sonnet | plan-then-auto | medium |
| New extraction pipeline step      | Opus   | plan-then-auto | high   |
| Cross-package schema migration    | Opus   | plan           | high   |
| Debug flaky test (unknown cause)  | Opus   | plan           | medium |
| Full data rebuild from scratch    | Opus   | plan           | high   |
| Batch file renames across project | Sonnet | plan-then-auto | medium |
| New package scaffolding           | Sonnet | auto-accept    | low    |

### Decision scope for when to write a formal prompt
<!-- scope: hybrid -->

- **1 file change** → conversational ("hey, fix X in Y") — no summary table needed
- **2-3 files** → conversational + paste context — summary table optional
- **3+ files or 2+ packages** → formal prompt with summary table (required)
- **Architecture decision** → AI Council debate first, then formal prompt

### Key rules
<!-- scope: hybrid -->

- Git workflow section is non-negotiable in EVERY prompt, even for non-repo changes (explain why not needed)
- "What NOT to do" section prevents Claude from over-engineering
- Include `pytest -x --tb=short && ruff check && git status` after each step, not just at the end
- Include `git status must show clean between each numbered step`
- JOURNAL `Changes:` line in the session entry if files changed (CHANGELOG retired — §14)
- Bypass permissions (no approval) → almost never, only for trivial read-only operations
- **Pruning symmetry** — every adding flow gets a review-gated pruning counterpart: CC PROPOSES removals with evidence (superseded-by ADR/commit, dead reference, obsoleted scope), operator ratifies, git history preserves; auto-delete stays forbidden. Point-of-use: the prompt template's Final "obsolescence pass" line (`templates/prompt-template.md`) — every session proposes deletion of content its change supersedes, instead of writing around it. Refs #136, #91 capture, #134 (family pattern), no-delete invariant

### Prompt Generation Card maintenance rule (per ADR-56, Council Q3)
<!-- scope: hybrid -->

The historical v4 handoff bundle folded the **Prompt Generation Card** (ADR-56) into
`02_METHODOLOGY.md` (the operational extract a fresh browser chat used to
generate Claude Code prompts, since it cannot read the filesystem). Under v5 the
browser boots from `HANDOFF_BOOT.md` and pulls methodology by **pointer** via CC —
no copied card travels in the handoff. This PLAYBOOK section remains the rationale
and edge-case authority for prompt conventions.

**Any change to prompt conventions (model/mode/effort criteria, the summary
table, the mandatory skeleton, hook guidance) updates:**

1. this PLAYBOOK rationale (the live authority), and
2. the point-of-use card wherever it travels — under v5, `templates/prompt-template.md`.
   (The handoff bundle's methodology template lives at `templates/handoff/02_METHODOLOGY.md.tmpl`;
   the pre-v5 frozen copies are no longer co-maintained.)

Drift between the two is a process bug — the card is the point-of-use authority,
PLAYBOOK is the maintenance source. The card has a ≤200-line size budget; if it
overflows, restructure into card + appendix rather than relocating authority.

---

## 3. Absorbing New Information
<!-- scope: hybrid -->

**Papers, repos, articles, tools → evaluate → extract actionable items → implement or reject.** Don't let "interesting" become "installed."

### Evaluation flow
<!-- scope: hybrid -->

1. **Quick triage (30 seconds):** Is this relevant to my work? Is it at my level or below?
   - Tutorial-level content (below Rob's level) → bookmark for reference only, skip
   - New tool with <100 GitHub stars and v0.1 → too early, revisit in 3 months
2. **Extract (5 minutes):** What are 2-3 actionable items from this?
3. **Decide:** Implement now, add to backlog, or reject with reason
4. **Log:** Add entry to LESSONS.md with category and action taken

### Council debate threshold
<!-- scope: hybrid -->

- Tactical choices (which library, which formatter) → decide yourself
- Architectural decisions (new database, new integration pattern, new package) → AI Council
- When in doubt: if reverting would take >1 hour, it's architectural

---

## 4. Extracting Lessons from Any Session
<!-- scope: llm -->

**Lessons die in chat history if not extracted.** Every session — browser chat, Claude Code terminal, Council debate, article analysis — potentially contains lessons. Without an explicit extraction step, they vanish.

### When to extract
<!-- scope: llm -->

- **End of every browser chat** that involved decisions, debugging, or new insights
- **End of every Claude Code session** (via LESSONS.md entry if applicable)
- **After every Council debate** (decisions are binding, but the reasoning often contains lessons)
- **After reading an article/repo/tool** that changed how you think about something

### How to extract (2 minutes, no more)
<!-- scope: llm -->

Ask yourself: **"What 2-3 things did I learn that I didn't know before this session?"**

For each, write one entry in LESSONS.md:
```
### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]
```

Categories: `prompt-craft` / `token-optimization` / `architecture` / `tooling` / `process` / `gotcha`  
Scope: `dev | llm | hybrid | runtime | meta` (ADR-29 — applies to new entries only; existing 123 entries are grandfathered)

### What qualifies as a lesson
<!-- scope: llm -->

- Something that surprised you (expectation ≠ reality)
- A mistake that cost >10 minutes
- A technique that saved significant time
- A decision rationale you want to remember
- A tool/article insight that changed your approach

### What does NOT qualify
<!-- scope: llm -->

- Things you already knew (no "learned that tests are important")
- Pure factual information (that goes to vault or ~/.claude/)
- Decisions without reasoning (those are ADRs, not lessons)

### When a lesson becomes a rule
<!-- scope: meta -->

If you find yourself writing a lesson that sounds like "always do X" or "never do Y," it might be a **rule**, not a lesson. The test: a lesson in `LESSONS.md` is human context (why, what happened); a rule in `~/.claude/` is machine-executable (a `verify:` line, a gotcha check). When a lesson matures into a rule:
1. Keep the lesson entry in `LESSONS.md` (provenance — the why).
2. Add the rule to `~/.claude/rules/`, `gotchas.md`, or `learned-rules.md` with a `verify:` line.
3. Cross-reference both with the file path.

---

## 5. Running an AI Council Debate
<!-- scope: llm -->

**Council debates are valuable but can become procrastination.** Hard rule: max 2 debates before implementation starts. Full format guide lives in the council project's docs/ folder.

> **End-to-end operational lifecycle:** see `protocols/AI_COUNCIL_PROCESS.md` (six stages: frame → author → route → debate → verdict → ADR → close), the prose companion to the ARCHITECTURE.md C3 "AI Council debate pipeline" Mermaid diagram. This section gives the *when* and the format summary; the runbook gives the full *how* with gate checks, troubleshooting, and code-grounded references.

### When to use Council vs. decide yourself
<!-- scope: llm -->

- **Council:** New package creation, database choice, integration pattern, tool adoption, major refactor, knowledge organization
- **Self:** Library version, config format, variable naming, test strategy for single feature
- **Rule of thumb:** If reverting would take >1 hour, it's architectural → Council

### Debate question format (summary)
<!-- scope: llm -->

A Council debate is NOT a Claude Code prompt. No Model/Mode/Effort, no UNDERSTAND, no Steps, no "What NOT to do." It's a question with options.

```markdown
---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
---

## Question: [one clear sentence]

### Current State
[concrete facts — numbers, problems, what exists today]

### Questions
1. **[sub-question]?**
   - A: [option with trade-off in one sentence]
   - B: [option with trade-off]
   - C: [option with trade-off]

### Constraints
- [hard boundary that eliminates options]
```

**Key rules:**
- Question = one sentence. If you can't, split into two debates.
- Current State = facts and numbers, not narrative or opinions
- Options = 2-4 per question, genuinely different approaches, trade-off baked into each
- Constraints = only hard boundaries that eliminate options. "ADHD" eliminates manual daily discipline. "Zero plugins" eliminates plugin solutions.
- Total file: 40-80 lines. Over 100 = too much narrative, trim.

### Running the debate
<!-- scope: llm -->

The current entry point is **`/council-question`** (per ADR-67 — Claude Code generates a templated Council question, symmetric with `wygeneruj handoff`; the slash command is implemented in the `ai-council` repo). The bare `council-cli` calls below predate ADR-67 and are illustrative of the underlying tool:

```bash
# Process debates from inbox
council-cli --inbox

# Direct question
council-cli "REST vs GraphQL?" --full --rounds 2
```

> Exact CLI syntax depends on the council tool — see its CLAUDE.md for current commands.

### Post-debate protocol
<!-- scope: llm -->

1. Decision is BINDING once synthesized
2. **Distill the verdict into a committed ADR** — this is a mandatory, automated step, never a manual hand-off. Run a Claude Code prompt that: (a) verifies the next ADR number against the `docs/decisions/ADR-*.md` sequence, (b) aligns the draft to `templates/ADR-template.md`, (c) writes `docs/decisions/ADR-{NN}-{topic}.md` (hyphens per ADR-34), and (d) commits it. The browser layer drafts ADR content; it never hands over a file with a placeholder number (`NN`) or manual TODOs. A debate is not done until its ADR is committed.
3. Archive transcript → `docs/decisions/transcripts/` (commit separately or together with ADR)
4. Add the ADR row and traceability entry to `docs/decisions/README.md` in the same commit
5. Never reopen a decided topic unless new evidence appears

### Council Debate Archival Protocol
<!-- scope: llm -->

Every Council debate output MUST be archived immediately after the debate completes. Skip this and the debate is effectively lost. Retroactive archive 2026-04-24 recovered 5 debates that sat in `ai-council/output/` for weeks.

> **Current state (updated 2026-05-26 — ADR-43 routing implemented):** Cross-project transcript routing now ships in `ai-council` (`routing.py` `TargetResolver`, ADR-43 amendment cycle 1). When a debate names a `target-project:` (frontmatter) or `--target-project` (CLI), the CLI writes the transcript to `<dev_root>/<target>/docs/decisions/transcripts/` automatically on completion — for `.dev-knowledge`-targeted debates that is `docs/decisions/transcripts/`, with **no manual archival step**. The canonical copy still lands in `ai-council/output/`; mirror writes are best-effort (a failure logs a warning, the canonical write still succeeds). Routing is **opt-in per invocation**: the manual pipeline below remains the fallback for debates that do **not** set a target-project.

**Pipeline (3 steps, ~5 min):**

1. **Identify target location** (`docs/research/` retired per ADR-60 amendment 2026-05-27 — all Council outputs land in `transcripts/`):
   - Debate about .dev-knowledge itself (any mode) → `.dev-knowledge/docs/decisions/transcripts/council-out-YYYYMMDD-HHMMSS-topic.md`
   - Debate targeting another repo → that repo's `docs/decisions/transcripts/` (routing handles this automatically when `target-project:` is set — ADR-43; this manual copy is the fallback only)

2. **Copy** `ai-council/output/council-out-YYYYMMDD-HHMMSS-topic.md` to target:
   - Decisions: keep filename as-is (`council-out-YYYYMMDD-HHMMSS-topic.md`)
   - Research: `YYYY-MM-DD-kebab-case-slug.md`
   - Byte-exact copy, preserve original in ai-council/output/

3. **Commit** with message: `docs: archive Council #NN — [topic]`

**Optional follow-up (separate commit):**
- Pick-mode with clear decision → write ADR in `docs/decisions/` referencing transcript
- Research-mode → no ADR, transcript/report suffices
- Judge-mode → depends on verdict

**Anti-pattern:** Accumulating 2+ un-archived debates in `ai-council/output/`. If detected, run retroactive archive before the next Council session.

**Future enforcement:** possible pre-commit hook checking ai-council/output/ for files >7 days old not present in any repo's archive locations.

### Council output convention (current state)
<!-- scope: meta -->

AI Council CLI writes the canonical transcript to `ai-council/output/` and, when a debate sets a
`target-project:` (frontmatter) or `--target-project` (CLI), **also routes a copy automatically**
to `<target>/docs/decisions/transcripts/` per ADR-43 (`routing.py` `TargetResolver`; `settings.yaml`
`target_projects` lists `.dev-knowledge`). Routed debates need **no manual archival** — the routed
copy is the transcript file only (no `_metrics.json`), preserving the canonical
`council-out-YYYYMMDD-HHMMSS-*.md` filename. Source of truth remains `ai-council/output/`.

Routing is **opt-in per invocation** — a debate that does not name a target-project still emits only
to `ai-council/output/` and is archived via the manual pipeline above ("Council Debate Archival
Protocol"). Mirror writes are best-effort (failure logs a warning; the canonical write always
succeeds), and routing depends on `settings.yaml` naming the target with a resolvable `dev_root`
(see ADR-43; routing-fragility noted in the 2026-05-25 pipeline audit, finding D2).

### When to run Council vs single-model + critic
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Per Council #28 community research finding: AI Council debate (4-model panel, 2 rounds, ~$0.50, ~5min) is overkill for normal implementation decisions. Reserve Council for truly ADR-worthy questions; use single-model + critic loop for the rest.

#### Gate Council to ADR-worthy decisions
<!-- scope: meta -->

Council debate is justified when ALL apply:
- **Architectural impact** — affects module boundaries, layer taxonomy, dependencies, data model
- **Multi-ADR ripple** — decision touches 2+ existing ADRs or creates new binding constraint
- **Reversal cost > 1 hour** — backing out the decision means meaningful rework
- **Multiple plausible options** — at least 2 genuinely different approaches exist (not "do or skip")

If any criterion fails, prefer single-model + critic loop.

#### Single-model + critic alternative
<!-- scope: meta -->

For decisions outside the Council gate:
1. **Browser chat (architect)** drafts the decision (option choice + rationale)
2. **Codex review** (or analogous critic) checks the drafted decision for risks, edge cases, missed alternatives
3. **Rob** approves, rejects, or iterates
4. **Outcome** lands as: ADR (if binding), JOURNAL entry (if tactical), or just commit message (if local)

Cost: ~$0.05 + 2min vs Council's $0.50 + 5min. Significantly cheaper for the >70% of decisions that don't need 4-model debate.

#### Examples (2026-04 sessions)
<!-- scope: meta -->

| Decision | Path used | Reason |
|----------|-----------|--------|
| Scope tagging architecture (Option A) | Council #27 | Affected entire `.dev-knowledge` repo, 3 plausible options, multi-week reversal cost |
| ADR-29 LESSONS grandfathering format | Council #27 (companion) | Bound to scope tagging decision, multi-format alternatives |
| TOKEN-LOG cadence (per-session vs threshold) | Browser + Rob | Two clear options, low reversal cost, browser-architect sufficient |
| TOKEN-LOG order convention (newest-first) | Browser + Rob | Two options, consistent with CHANGELOG, no architectural ripple |
| Validator/hook H3 divergence fix | Browser + Rob | Implementation bug, single correct fix, no debate needed |
| CLAUDE.md template structure (10 sections) | Browser + Rob | Well-known community pattern (Council #28 research), no need to re-debate |

#### Anti-patterns
<!-- scope: meta -->

- **Council habit-formation** — running Council because "it's how we decide" without checking the gate. Costs add up fast ($0.50 × N decisions).
- **Single-model laziness** — choosing single-model path when criteria genuinely apply (architectural ripple), then later reopening as Council = wasted first decision.

### ADR authorship paths (how an ADR gets written)
<!-- scope: meta -->

An ADR reaches the repo by one of **two authorship paths** — choose by the decision's gate (§5 "When to use Council vs. decide yourself"), not by habit:

- **Chat-drafted** — the browser architect drafts the decision in conversation (operator-ruled calls, synthesis, single-correct-fix decisions below the Council gate); **Claude Code** then creates the ADR in-repo with the next number, frontmatter, and template. Default path for operator rulings (e.g. ADR-80 itself).
- **Council-convened** — an AI Council debate produces a transcript; the **post-debate protocol** (§5) distills it into an ADR, number verified and template-aligned. Used when the decision clears the Council gate (architectural ripple, multi-ADR impact, genuine cross-model uncertainty — e.g. ADR-76 from the local-scheduler debate).

Both paths **converge on the same invariant**: the ADR is generated and committed *in Claude Code* — never hand-pasted from browser chat into the repo (ESSENTIALS "Artifact generation direction"; LESSONS #8) — numbered, frontmatter-stamped, and **immutable thereafter** (changes go through "Amendment vs Reopen", below).

### Amendment vs Reopen Decision Protocol
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

When validator/tooling reality contradicts an ADR's prescription, two paths exist: amend in place (preserve intent, update prescription) or reopen the decision (intent itself was wrong). This protocol decides which.

**Pattern emerged organically 2026-04-24** — used 3 times in sequence:
1. ADR-27 amendment: delta rule replaced flat-threshold enforcement (validator built differently than ADR prescribed)
2. ADR-29 amendment: H1 placement for LESSONS file-level tag (collided with validator's 3-line H1 detection window)
3. ADR-27 amendment: heading levels H2+H3 explicit, invocation semantics clarified (silent vacuous-pass discovered)

#### Decision tree
<!-- scope: meta -->

**Amend in place** if:
- Validator/tooling implementation diverged from ADR prescription, but original intent still correct
- Real-world use revealed prescription was unclear/incomplete; clarification preserves intent
- New edge case discovered; addressing it doesn't change the decision's core
- Implementation detail correction (e.g., regex pattern, file path, threshold value tweak)

**Reopen the decision** (full Council or browser+critic per gating above) if:
- Original intent itself was wrong (not just prescription)
- Context changed materially: new constraints, new tools available, new evidence contradicting decision premise
- Multiple ADRs affected by the change (cascading impact)
- Stakeholder expectations shifted (e.g., adding non-dev contributors changes decision economics)

#### Amendment mechanics
<!-- scope: meta -->

When amending in place:
1. Add **Amendment YYYY-MM-DD** block at end of ADR file (do not rewrite original decision text)
2. Block structure — both forms are acceptable (the live 2026-06-21 examples, ADR-88/89, use the **H2 heading** form with an inline status-flip; the blockquote is the original template):

   > **Amendment YYYY-MM-DD ([brief topic]):** [What was wrong/unclear in original prescription]. Resolution: [what the prescription now says]. Intent preserved: [why this is amendment not reopen].

   …or, equivalently, as a heading: `## Amendment — YYYY-MM-DD: [topic]` followed by the same What/Resolution/Intent-preserved content (used when the amendment also flips the ADR's status, e.g. Proposed → Accepted).

3. Update validator/tool/process to match amendment
4. Add LESSONS.md entry (per ADR-29 format) describing what was discovered
5. JOURNAL `Changes:` line: "ADR-NN amended YYYY-MM-DD — [topic]" (CHANGELOG retired — §14)

#### Reopen mechanics
<!-- scope: meta -->

When reopening:
1. Mark original ADR with **Status: Reopened YYYY-MM-DD** at top
2. Run Council per gating criteria above (full Council if architectural; browser+critic if not)
3. Outcome lands as new ADR (e.g., ADR-NN with "Supersedes ADR-MM" reference)
4. Original ADR retains content (history preserved), but new ADR governs

#### Anti-patterns
<!-- scope: meta -->

- **Amending intent, not prescription** — if you find yourself rewriting the original decision text to "what we should have said," that's a reopen, not amendment. Don't conflate.
- **Reopen for prescription drift** — if validator just needs a regex tweak, that's amendment. Reopen ceremony wastes effort.
- **No amendment record** — silently changing tool to match new behavior without an amendment block in the ADR. Future Claude sees ADR vs reality mismatch with no trail.

#### Examples (2026-04-24)
<!-- scope: meta -->

| ADR | Trigger | Decision | Reason |
|-----|---------|----------|--------|
| ADR-27 (scope tagging) | Validator built with delta-rule enforcement, not flat threshold | Amend | Original intent (≤25% hybrid ceiling, blocking) preserved; mechanism (when to block) clarified |
| ADR-29 (LESSONS grandfathering) | H1 file-level tag collided with validator's H1 detection window | Amend | Original intent (file-level tag for LESSONS, not per-section) preserved; placement (H1 not `## Entries`) clarified |
| ADR-27 (scope tagging) | Validator silently passed when called without args; H2 vs H3 ambiguous | Amend | Original intent (every section header tagged) preserved; level scope (H2+H3) and invocation semantics (auto-scan IN_SCOPE_FILES) explicit |

### Codex review archival protocol
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Codex code review (OpenAI's read-only reviewer) produces findings in terminal output during a session. Without explicit archival, findings disappear when the session ends. This protocol captures Codex output as a durable artifact — analogous to Council Archival Protocol above.

**Pattern parallel to Council Archival:** Council debates → `docs/decisions/transcripts/`. Codex reviews → `docs/audits/YYYY-MM-DD-codex-{slug}.md`.

#### Trigger
<!-- scope: meta -->

Archive Codex review when ANY apply:
- Review found ≥1 Critical or High severity finding
- Review precedes a non-trivial merge (3+ files OR safety-critical paths)
- Findings reference future work (e.g. "this should be refactored later" with concrete pointer)
- Rob explicitly requests "archive this Codex output"

Skip archival when:
- Review found only Low severity polish issues addressed in same session
- Trivial commits (typo fix, dependency bump, single-file refactor)
- Review explicitly inconclusive ("could not parse changeset")

#### Target path
<!-- scope: meta -->

`{repo}/docs/audits/YYYY-MM-DD-codex-{slug}.md`

Where:
- `YYYY-MM-DD` — date of review
- `{slug}` — kebab-case identifier (feature, branch, or commit topic)

Example: `docs/audits/2026-04-22-codex-handoff-process-rewrite.md`

#### Format
<!-- scope: meta -->

```markdown
# Codex Review — {topic}

**Date:** YYYY-MM-DD
**Branch:** {branch-name}
**Commit (HEAD at review):** {short SHA}
**Reviewer:** Codex (OpenAI)
**Mode:** {full review | diff review | targeted}

## Severity breakdown

| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |

## Findings

### [SEVERITY] file:line — short description

**What:** One sentence.
**Why:** One sentence.
**Fix direction:** One sentence.
**Action:** [resolved in this session / queued / deferred / dismissed with reason]

(Repeat per finding. Group by severity. Omit empty sections.)

## Resolution summary

What was fixed in this session vs queued for later. Cross-link to JOURNAL entry and commits.

## Notes

Reviewer's narrative observations beyond per-finding (e.g. "consistent error handling pattern across module"), if any.
```

#### Linking from other docs
<!-- scope: meta -->

After archival, cross-link FROM:
- **JOURNAL.md entry** for that session: "Codex review archived: docs/audits/YYYY-MM-DD-codex-{slug}.md (N findings, M resolved)"
- **Commit message** of the resolution merge: "fix(scope): address Codex Critical/High findings — see docs/audits/YYYY-MM-DD-codex-{slug}.md"
- **JOURNAL `Changes:` line** if findings affected user-visible behavior (CHANGELOG retired — §14)

#### Anti-patterns
<!-- scope: meta -->

- **Archive everything** — low-severity polish findings don't warrant an audit document; archive only when trigger criteria match
- **Archive without resolution tracking** — review without clear "what was fixed / what's deferred" loses accountability
- **Codex output rot** — letting findings linger across sessions without resolution status creates ambiguity over what's still open

---

## 6. Code Review with Claude Code
<!-- scope: dev -->

**Code review stays on Sonnet — security boundary, never Haiku.** This is a Council-binding decision.

### Process
<!-- scope: dev -->

1. Specify scope: which files, which changes, what to focus on
2. Ask Claude Code to read the diff first, report what it sees
3. Focus areas: security, edge cases, error handling, test coverage
4. Never auto-apply suggested changes — review each one

---

## 7. Managing a Long Claude Code Session
<!-- scope: hybrid -->

**Sessions longer than ~4 hours should be split.** Context degradation is not linear — it accelerates.

### Session start protocol
<!-- scope: hybrid -->

1. Review recent JOURNAL.md entries (CHANGELOG retired — §14)
2. Read CLAUDE.md
3. Check gotchas
4. `git status` (must be clean)
5. Define 1-2 objectives for this session — everything else is backlog

### During session
<!-- scope: hybrid -->

- `/clear` between unrelated tasks (saves 30-40% input tokens)
- Commit after each logical change
- Test after each change (not at the end)
- If scope creeps: "Adding to BACKLOG.md, not doing today" (no `OPEN_DECISIONS.md` — BACKLOG is the single pending-items queue, ADR-41)
- Use Plan Mode before implementation (catches bad approach at 200 tokens vs 5000)
- Use line ranges (`@file:15-80`) instead of whole files

### When context gets heavy
<!-- scope: hybrid -->

- `/compact` at 40% (aggressive, Council-approved)
- `/session-summary` before switching to Claude.ai for architecture consulting
- If Claude says "it's done" on a complex operation — VERIFY with filesystem commands

### Context budget — read-scoping rule
<!-- scope: hybrid -->

**A formal prompt's main thread never full-reads a large artifact** (transcript, audit, long doc; threshold ≈ >500 lines or >20k tokens). Consumption order: (1) a machine-readable marker, if the artifact carries one — producers compute markers, consumers read only markers (the counts-contract pattern, ADR-74 doctrine: the contract lives on the executing path); (2) `grep -n` anchors or a line-range view scoped to the needed lines; (3) a read-only subagent that reads in its own context window and returns a summary plus pinpoint quotes. Evidence/valve steps in prompts are authored as "grep -n the specific lines", never "read the file and quote". Session hygiene pointers: inspect window composition with `/context`; prefer manual `/compact <preserve-instructions>` at natural breakpoints over auto-compact; side questions via `/btw` stay out of history. Edit-flow synergy: a single-file `grep` now satisfies Claude Code's read-before-edit check (v2.1.160), so grep-first reading carries no edit-flow penalty.

### Session end protocol
<!-- scope: hybrid -->

1. Run full test suite
2. Prepend a JOURNAL.md entry (Did/Result/Changes/Next) if files changed (CHANGELOG retired — §14)
3. Update project handoff doc (if exists)
4. `git status` (must be clean — if "27 modified files", STOP and commit)
5. Write 3-line handoff note

---

## 8. Handing Off Between Sessions
<!-- scope: meta -->

Operational authority: `protocols/HANDOFF_PROCESS.md` v5 (ADR-82; CC-owned residual + thin browser boot). This section summarizes handoff governance; for handoff generation, follow HANDOFF_PROCESS.md — it is the single live source of truth and this summary must not duplicate its mechanics.

Mode-awareness — the `architect | execution` payload switch (one process, two residual profiles + browser postures) — is defined in `protocols/HANDOFF_PROCESS.md` §13; it is **not** described here (resident-copy drift is this section's named failure).

Cross-refs: ADR-82 (v5 ratification), ADR-62 (v4 ratification — superseded), ADR-37 (session-boundary two-phase overlay — design history), ADR-32/42 (handoff format v2/v3 — superseded).

### What the v5 handoff carries
<!-- scope: meta -->

Canonical: `protocols/HANDOFF_PROCESS.md` §2 (the **residual** CC emits) + §5 (the teeth-y **probe manifest**) + §13 (the `architect | execution` modes). Not restated here — a resident copy is the drift this section names as its own failure. (The historical v4 8-file bundle is superseded; preserved bundles in `docs/handoffs/` are point-in-time history.)

### Roles
<!-- scope: meta -->

Canonical: **ESSENTIALS § Roles** (Does/Does NOT lists, Three-layer flow per ADR-28) + `protocols/HANDOFF_PROCESS.md` §1 (the v5 actor table) / §7 (the browser operating role). Not restated here.

### Handoff paths
<!-- scope: meta -->

**Path A — Claude Code → Browser:** `/session-summary` in Claude Code → paste into Claude.ai. Discuss architecture/strategy; decisions return as prompts (Section 2 format).

**Path B — Browser → New Browser:** the operator triggers `please create handoff for <repo>` then `complete handoff for <repo>`; Claude Code generates the v5 handoff (residual + probe manifest + thin boot) per HANDOFF_PROCESS.md — Rob makes zero formatting decisions. Trigger at ~2 hours while context is still fresh.

**Path C — Browser → Claude Code:** Claude.ai writes prompts in Section 2 format (Model/Mode/Effort table). Prefer questions over commands. Let Claude Code discover actual state, then propose actions.

### Token log cadence
<!-- scope: meta -->

Relocated to `protocols/HANDOFF_PROCESS.md` §14 (#152, 2026-06-15) — session-boundary maintenance fired by `/session-summary` (7-day staleness check + short-format `ccusage --json` snapshot, newest-first prepend to `logs/TOKEN-LOG.md`). Canonical there; not restated here.

### Output the operator copies into browser chat (render-layer note)
<!-- scope: runtime -->

The trap is the **render layer**, not what Claude writes. A plain markdown pipe-table (`| col | col |`) is the token-cheapest table to write *in a file*, but the Claude Code TUI renders it by **painting Unicode box-drawing borders** (`┌─┬─┐ │ ├─┼─┤ └─┴─┘`) client-side. Those glyphs are added at *display* time — Claude never emits them. So a rule that only bans Claude from writing box-drawing is a no-op: it forbids something Claude already doesn't do, while the operator still copies the painted borders out of the terminal (Path A) into browser chat and pays ~3× the tokens for them.

**The fix targets render, not emit.** For any report the operator copies back — `/session-summary` output and ad-hoc step reports — make it:
1. **Flat** — plain markdown or `key: value` lines / bullets; no column-padding spaces.
2. **Code-fenced** — wrap it in a triple-backtick block. A fenced block renders raw (monospace, un-painted), so the pasted text is exactly the characters Claude wrote — no borders.

A bare (un-fenced) pipe-table is the failure case: clean-looking in the TUI, box-drawing on paste. This is the same fenced-block discipline already used for Scale-S PowerShell snippets (ESSENTIALS § "Architect → operator channel-discipline for execution actions") and downloadable prompts (§2 "Delivery format") — extended to every copy-back report. Reconciles with Path A above (`/session-summary` → paste into Claude.ai).

**Operator-side option (not a repo change):** Claude Code also exposes an output-style setting; a plainer style reduces TUI table-painting globally. That is runtime config under `~/.claude/` — outside this repo's scope, noted for the operator, not changed here.

Canonical rule: **CLAUDE.md §4 "Output formatting (render-layer)"**. This subsection is the rationale authority; the CLAUDE.md bullet is the point-of-use rule.

---

## 9. Weekly Review (Friday)
<!-- scope: hybrid -->

**Friday consolidation — 30 minutes max, not a project.**

1. Review gotchas added this week — any patterns?
2. Review token usage — `ccusage --json` → append snapshot to logs/TOKEN-LOG.md. Is Opus verbosity still the main drain?
3. Review LESSONS.md entries from this week — anything to change in PLAYBOOK?
4. Review BACKLOG.md — anything stale? Anything urgent? (single pending-items queue; no `OPEN_DECISIONS.md`)
5. Quick project health check (test suite, lint, stale branches)
6. Update ENVIRONMENT.md if any config changed

(The retired self-evolution step was dropped 2026-06-19; corrections now auto-promote via the `corrections.jsonl` Stop hook — see ESSENTIALS "Feedback Loop".)

---

## 10. BACKLOG Grooming Workflow
<!-- scope: meta -->

`BACKLOG.md` is the single canonical source for ALL pending items across sessions. Handoffs reference BACKLOG items by pointer (stream + title), never duplicate the queue. Per-handoff and quarterly grooming prevent the write-only graveyard anti-pattern.

**Mandate:** `BACKLOG.md` is part of the universal governance baseline (ADR-38 amendment A5, 2026-05-23; ADR-41) — mandatory for every repo regardless of size. (Previously gated to M+ repos; the repo-tier system is deprecated.)

**Done-item disposition (ADR-47/65).** Done items **leave** the file on close — git history (the closing commit, located by the entry id per CONTRIBUTING) + the existing per-session JOURNAL entry are the record. **No archive file** (`BACKLOG_ARCHIVE.md` deleted 2026-05-16; CLAUDE.md §5). No collapsed stubs. Closing a backlog item adds **no** new per-item write — the per-session JOURNAL ritual already carries it.

**Layout (ADR-66 — supersedes ADR-64's flat layout).** `BACKLOG.md` is a **story map**: **Big Picture → Theme → User Story → Task**. The operator scans goals (Big Picture + themes + stories); the LLM reads execution detail (tasks). **No `repo:` field** (implicitly `.dev-knowledge`); cross-repo governance lives under the *Cross-repo universalization* theme, naming repos in task text; child-repo *execution* items live in the relocation queue, not here. **Authority chain:** ADR-41 (mandate) → ADR-47 (organization) → ADR-64 (done-items-leave / routing / validator) → ADR-65 (disposition) → ADR-66 (story-map layout). A read-only validator (`scripts/validate_backlog.py`) machine-checks the hierarchy.

### Schema (ADR-66; machine-checked by `scripts/validate_backlog.py`)
<!-- scope: meta -->
<!-- rule: governance-backlog-schema -->

**Four layers:**

```
# .dev-knowledge BACKLOG
## Big picture              <- 2-3 sentences + the theme backbone list (no stories/tasks)
## <Theme>                  <- backbone header; a durable area of work
> As a <persona>, I want <goal>.       <- theme intent (persona = operator or an AI agent)
### <User story>            <- human goal — the layer the operator scans
So that <why>.              <- the why (required, immediately under the story)
- [#id] [P1][M] <action> · Done when: <criterion> · refs <ADR/file>   <- task (for the machine)
```

- **Big Picture** — what `.dev-knowledge` is working toward (from VISION) + the theme list. The map, not a priority queue.
- **Theme** — a `## ` backbone header; a durable area of work.
- **User Story** — a `### ` header in human language + one `So that …` line. Personas = the operator and the AI agents (Claude Code / Codex) who inherit the repo. This is the scan layer.
- **Task** — a bullet `- [#id] [P{1-3}][{S|M|L}] <terse technical action> · Done when: <criterion> · refs <…>`. Technical density is expected here. No `repo:`/`status:` field — in-file = open; done tasks **leave** (ADR-65).

**Rules** (validator hard-fail unless marked warn):
- every **task** has a unique `[#id]`, a `[P{1-3}][{S|M|L}]` band, and a `Done when:` clause;
- every task sits **under a Story under a Theme** (no orphans; nothing directly under `## Big picture`);
- every **User Story** has a `So that` line;
- **no done task** in the file — a `status:done` / `[x]` / `~~strikethrough~~` marker hard-fails (done tasks leave);
- *(warn-only: a story with zero tasks.)*

Anti-pattern: do NOT collapse the layers back to a flat list, or re-expand a task to multi-paragraph form — goals-on-top / task-detail-below is the readability fix ADR-66 ratified; the validator guards it.

### Per-handoff grooming (~2 min, mandatory for M+)
<!-- scope: meta -->

Browser 1 (departing) runs at handoff generation:

1. Read current BACKLOG.md state
2. Mark stale items (no progress in 3+ sessions) for review
3. Prune obvious dead items (completed, no longer relevant)
4. Add new items surfaced this session
5. **Remove** completed items — they leave the file (the closing commit + the per-session JOURNAL entry are the record, ADR-65); do not leave `done` entries in place
6. Future State in handoff references BACKLOG items by id + title (pointers, not copy-paste)

Light P1 items MAY be copy-pasted inline into Future State (acceptable at P1 only — Council Risk #2 mitigation).

### Quarterly deep grooming (~30 min, scheduled)
<!-- scope: meta -->

Rob reviews full BACKLOG once per quarter (recurring quarterly cadence — schedule the next review at the start of each quarter; no fixed anchor date, to avoid silent rot into a past date):

1. Confirm **no `done` items remain** — done items leave on close (ADR-47/65); the validator hard-fails on any `done` entry. **No archive file** (CLAUDE.md §5). Retrospect via `git log` + JOURNAL, not a parallel archive
2. Re-prioritize P1/P2/P3 based on current ecosystem state
3. Remove items that no longer align with VISION
4. Groom each stream: still active? Items still actionable?

**Write-only graveyard prevention:** speculative or distant ideas route to VISION.md, not BACKLOG.md. Strict curation — actionable items only.

### Split-brain prevention
<!-- scope: meta -->

BACKLOG.md is the single source of truth. Handoffs must NOT duplicate the pending queue:
- Handoff Future State (per ADR-37, Section 8) = which BACKLOG items THIS session targets — not a parallel queue
- ADR-32 v2.0 §4 "Pending — next session candidates": deprecated in favor of "Pending items: see BACKLOG.md" pointer

Browser 2 (incoming) at session start: read handoff Current + Future State → read BACKLOG.md for full context → validate Future State items against BACKLOG.md (drift check per ADR-37) → act on prioritized items.

Cross-refs: ADR-41, ADR-37 (Section 8), ADR-38 amendment A5 (universal baseline — BACKLOG mandatory every repo)

---

## 11. Evaluating a New Tool/Framework/Model
<!-- scope: hybrid -->

**Check maturity before investing time.** Fresh repos with <100 stars and v0.1 = too early.

### Quick eval checklist
<!-- scope: hybrid -->

1. GitHub stars, last commit date, release cadence
2. Does it solve a problem I actually have? (not "might have someday")
3. Does it integrate with my existing stack? (Python, Click, YAML config)
4. What does adoption cost? (learning curve, migration, dependencies)
5. Is there a simpler alternative I'm already using?

### Decision framework
<!-- scope: hybrid -->

- **Obvious yes:** Solves real pain, mature, good docs, easy to adopt → just do it
- **Maybe:** Interesting but not urgent → bookmark, revisit in 2 weeks
- **Council debate:** Would change architecture or replace an existing tool
- **Hard no:** Pre-v1, no community, solves a problem I don't have

---

## 12. Multi-Project Rules
<!-- scope: dev -->

**Package boundaries are sacred.** Projects/packages should never import directly from each other — they communicate via CLI subprocess, shared schema packages, or well-defined interfaces.

### Principles
<!-- scope: dev -->

- Designate one package as the **source of truth** for shared data models, taxonomy, naming, and validation. Other packages depend on it — never duplicate a schema.
- Orchestrator pattern: one central project calls others via subprocess or API. Tools stay stateless; the orchestrator owns state.
- Document the architecture in the project's CLAUDE.md, not here. This playbook covers methodology, not project-specific design.

### Config hierarchy (most specific wins)
<!-- scope: dev -->

```
~/.claude/CLAUDE.md              ← Global rules (all projects)
~/.claude/skills/gotchas/        ← Global traps
Dev/CLAUDE.md                    ← Workspace rules
Dev/{project}/CLAUDE.md          ← Project rules
Dev/{project}/packages/X/CLAUDE.md  ← Package rules
```

---

## 13. Where Knowledge Lives
<!-- scope: meta -->

**Three domains, three homes, zero overlap.** Council Decision #23 (2026-03-29, unanimous 4-0).

> See also "System Architecture" section — domains (this section) and layers (that section) are complementary frames.

| Domain                     | Location              | Tool                       | Purpose                                                  |
| -------------------------- | --------------------- | -------------------------- | -------------------------------------------------------- |
| Pre-sales work knowledge   | `ObsidianVault/`      | Obsidian                   | Clients, products, domains, competitive intel, demo prep |
| Dev practice methodology   | `Dev/.dev-knowledge/` | VS Code workspace          | How I build software: processes, lessons, setup state    |
| Claude Code runtime config | `~/.claude/`          | Claude Code auto-discovery | Rules, commands, hooks, agents, memory, gotchas          |

### "Where does this go?" decision rule
<!-- scope: meta -->

- Is it about a **client, product, or domain**? → Obsidian vault
- Is it about **how I work** (process, methodology, lesson learned)? → `.dev-knowledge/`
- Is it a **rule Claude Code must execute** (gotcha, verify check, command, hook)? → `~/.claude/`

### When a lesson becomes a rule
<!-- scope: meta -->

See §4 *Extracting Lessons from Any Session → When a lesson becomes a rule* for the canonical trigger + 3-step process.

### Data sanitization
<!-- scope: meta -->

If a client engagement generates a dev lesson, strip all client names, proprietary schemas, and identifying details before writing to `.dev-knowledge/`.

### Migration triggers
<!-- scope: meta -->

- **`.dev-knowledge/` navigation overhead emerges** (cross-file search starts feeling slow; new files don't slot into an obvious folder) → evaluate creating a dedicated Obsidian DevVault
- **LESSONS.md becomes hard to navigate by topic** → split into topic files
- Rob opens Obsidian to search for dev methodology → immediate signal DevVault is needed

> Triggers, not caps. See LESSONS.md 2026-04-28 entry "Distinguish triggers from limits."

---

## 14. Markdown Governance
<!-- scope: dev -->

> **Reconciled 2026-06-23 (Handoff + Snapshots/reports rows).** The Handoff and Snapshots/reports rows below now match practice: handoffs are dated, immutable `docs/handoffs/YYYY-MM-DD-*/` bundles (folder convention per ADR-32 / HANDOFF_PROCESS v5.2), not a living `docs/HANDOFF.md`; dated snapshots/audits under `docs/archive/` are kept **indefinitely** (the prior "delete after 90 days" lifecycle never matched practice — audits are immutable records).

**Every markdown file in the project falls into exactly one category.** If you're about to create a .md file and it doesn't fit any category below — it probably shouldn't exist.

| Category          | Location        | Naming                                         | Lifecycle                      |
| ----------------- | --------------- | ---------------------------------------------- | ------------------------------ |
| Project docs      | Root            | CLAUDE.md, README.md                           | Living, never delete           |
| Decision records  | docs/decisions/ | ADR-{NN}_{topic}.md                            | Frozen, never edit             |
| Handoff           | docs/handoffs/  | YYYY-MM-DD-{slug}/ bundle (HANDOFF_BOOT.md + …)| Dated, immutable               |
| Snapshots/reports | docs/archive/   | {YYYY-MM-DD}-{topic}.md                        | Frozen, kept indefinitely      |
| Eval data         | eval/           | eval_history.jsonl                             | Append-only, keep indefinitely |
| Ephemeral prompts | Not in repo     | PROMPT_{topic}.md                              | Delete after execution         |

**Two date rules, no exceptions:**
- Frozen/snapshot files → date in filename: `2026-03-28_CLEANUP_PLAN.md`
- Living files → date in YAML frontmatter: `last_updated: 2026-03-28`

**Retired file types — canonical statement.** `CHANGELOG.md` is **retired ecosystem-wide** (ADR-49, 2026-05-16): git history + the JOURNAL `Changes:` line now carry what it used to, and it must not be recreated. This is the single canonical statement of that rule; everywhere else in this file an inline mention points here (`§14`) rather than restating it.

**Heading scheme — canonical statement.** This PLAYBOOK is a two-part spine: **Part I — Reference** chapters are `## ChN. <Title>` (sequential from Ch1); **Part II — Workflows** recipes are `## N. <Title>` (sequential; the §18 gap is intentional, held by its co-located `<!-- structure-allow: numbering-gap 18 -->` marker). A new conceptual reference → Part I + the next `Ch`; a new task recipe → Part II + the next `§` (a deletion leaves a `structure-allow` marker, never a renumber). This is the single canonical statement of the scheme — and it is machine-enforced: `scan_heading_scheme` in `scripts/validate_doc_structure.py` fires when a Part-I heading loses its `ChN.` prefix or falls out of sequence, so the standardization cannot silently re-drift.

### Project governance folder
<!-- scope: dev -->

Use `docs/` for project-level governance. Define its allowed contents in CLAUDE.md. Standard layout:

```
docs/
  HANDOFF.md                   ← living, update in place
  decisions/                   ← ADRs + Council transcripts, frozen
  archive/                     ← frozen snapshots, 90-day TTL
  staging/                     ← gitignored, disposable
```

Keep it tight. If something doesn't fit one of these categories, it goes somewhere specific — don't let `docs/` become a dumping ground.

### Diagram-form selection algorithm
<!-- scope: dev -->

Before authoring any diagram in a living doc, pick the lightest form that carries the structure. The five-rule algorithm (applied in the #91 ARCHITECTURE rewrite, which demoted 7 of 8 Mermaid diagrams):

1. linear ≤1-branch → text arrow-chain
2. inventory/mapping → table
3. ≥2-branches / cycle / ≥3-actors → Mermaid (ADR-51 theme)
4. auto-generable fact → generated only
5. any Mermaid >12 nodes → split or demote

Mermaid is the heaviest form (token cost + AI-edit-reliability drop above ~100 lines of markup) — reserve it for genuine branching/cyclic/multi-actor structure, and demote on the first rule that a lighter form satisfies. Refs #91 (amendment A), ADR-51.

---

## 15. Anti-Patterns — What NOT to Do
<!-- scope: hybrid -->

**"I'll organize later"** — If you create a file without knowing where it belongs, you'll never organize it. Know the category BEFORE creating.

**"Let's put it in docs/ for now"** — `docs/` is not a staging area. It has defined categories: handoff, archive, decisions. If it doesn't fit one, it doesn't belong there.

**"Let's name it descriptively"** — `ARCHITECTURE_REVIEW.md` is useless without a date. `2026-03-21_ARCHITECTURE_REVIEW.md` is findable.

**"We can consolidate these output folders later"** — Output dirs grow exponentially. Set a single canonical output path at project creation.

**"The AI will remember"** — It won't. Not after 4 hours. Not across sessions. Not after compaction. Write it down in JOURNAL.md or CLAUDE.md (CHANGELOG retired — §14).

**"We'll add tests later"** — Later never comes. Write the test stub before the implementation.

**"Let's rename/restructure everything"** — Every rename has blast radius (env vars, configs, DBs, venvs, caches). Never rename without full impact analysis FIRST, and never in the same session as feature work.

---

## The 10 Commandments
<!-- scope: hybrid -->

1. **CLAUDE.md first, code second.** Define the project before building it.
2. **Date everything.** Filename or frontmatter. No undated artifacts.
3. **Test after each change.** Not at the end. After EACH step.
4. **One home per file type.** Decisions → docs/decisions/. Reports → docs/archive/. No exceptions.
5. **Commit after each logical change.** Git status must be clean between tasks.
6. **Log changes continuously.** JOURNAL `Changes:` line when files change (CHANGELOG retired — §14), LESSONS entry when something was learned.
7. **Scope is sacred.** 1-2 objectives per session. Everything else is backlog.
8. **Verify with Claude Code, plan with Claude.ai.** Don't let Claude.ai generate filesystem commands from memory.
9. **Output dirs are disposable.** Canonical location, gitignored, size-monitored, regularly cleaned.
10. **If the AI says "it's done" — verify.** The longer the session, the less you should trust it.

---

## 16. Cross-Tool Review
<!-- scope: dev -->

**When:** Feature branch touches 3+ files OR 2+ packages OR safety-critical paths (vault writes, OneDrive ops, cleanup/delete)
**Skip when:** Single-file fix, test-only changes, documentation updates

(Gated by change size and risk, above — not by any repo tier; the repo-tier system was deprecated 2026-05-23.)

### Review Tools
<!-- scope: dev -->

Two options for code review (A/B test both, then standardize):

**Option A — /code-review ultra (Claude Code built-in; `/ultrareview` is the deprecated alias):**
Cloud-based multi-agent review. Run without arguments (current branch) or with a PR number. No second terminal needed.

**Option B — Codex CLI (automated, single command):**
`/codex-review <topic>` wraps `codex exec --output-last-message`. Produces dated, frontmatter-wrapped audit at `docs/audits/YYYY-MM-DD-codex-{topic}.md`. Read-only sandbox. Opt-in `-AutoCommit`. Requires ChatGPT Plus subscription. See `~/.claude/bin/codex-review.README.md`.

**Code-only rule (per-change codex-review):** codex-review is for code review, not markdown/prose. The wrapper enforces a path-guard against an extension allowlist (`.py .ps1 .sh .ts .tsx .js .jsx .go .rs .rb .java .cs .cpp .c .h .sql .toml .yaml .yml .json .ini`). Mixed diffs are filtered to the code subset before invoking codex. Markdown-only or empty diffs exit cleanly without invoking codex. Mechanically enforced in `~/.claude/bin/codex-review.ps1`.

Both satisfy S15 review requirement. Choose based on quality of findings after 2-week A/B test.

Codex/ultrareview reviews. Claude Code builds. Never reverse the roles.

**Codex reviewer config:** The global reviewer config (role, checklist, output format) lives at `~/.codex/AGENTS.md`; canonical source tracked in `.dev-knowledge/codex/AGENTS.md` (ADR-54). Per-repo `AGENTS.md` adds only repo-specific rules — it does not repeat the global config.

---

## 17. Code Quality Audit Process
<!-- scope: dev -->

**When:** Periodic full audit (cadence by repo complexity — larger/more-active repos more often) · On-demand before major refactors · a tiny single-script repo may skip entirely. Judgment call, not tier-gated.
**Tool:** Codex CLI or Codex Desktop (independent reviewer — no authorship bias)
**Cycle:** Read-only audit → triage by severity → fix by severity → re-audit

**Scope distinct from per-change codex-review:** the monthly full-repo audit is deliberately whole-repo (within `src/`) and is **unchanged** by the per-change diff-scoping rules in §16. The code-only path-guard applies here too (no review of markdown files inside `src/`), but the audit's whole-`src/` scope is preserved.

### Severity tiers
<!-- scope: dev -->
- **CRITICAL** — data loss, security, broken imports that fail at runtime
- **HIGH** — wrong dependency direction, missing tests on public API, type errors
- **MEDIUM** — style violations, redundant code, unclear naming
- **LOW** — suggestions, nitpicks, debatable patterns

### Process
<!-- scope: dev -->
1. Run audit (read-only): `codex "Audit this repo against CLAUDE.md rules. Output findings by severity. Do not fix anything."`
2. Triage output manually — expect ~30% false positives. Demote miscalibrated patterns in CLAUDE.md.
3. Fix CRITICAL and HIGH first. One commit per logical group.
4. Re-run audit. Confirm flags resolved.
5. Update ARCHITECTURE.md if module boundaries or dependency direction changed.

### Rules
<!-- scope: dev -->
- Audit-first, fix-second. Never fix while auditing.
- Claude Code fixes. Codex audits. Never reverse the roles.
- Structural changes with N>5 call sites: shim first, migrate incrementally, remove shim last.
- Any session touching module boundaries must produce or update ARCHITECTURE.md (mandatory every repo per ADR-51 as amended 2026-05-23).

### Post-Structural-Change Documentation
<!-- scope: dev -->

After any change that moves, renames, or reorganizes files or modules, update documentation that describes the changed structure:

- Always update `ARCHITECTURE.md` (mandatory every repo per ADR-51 as amended 2026-05-23).
- On a larger repo, also update affected module READMEs under `src/*/`.

This is not optional. Stale structural documentation is worse than no documentation — it actively misleads.

---

## 19. Scrum-Master Review Propagation
<!-- scope: meta -->

> Authorized by **ADR-63** (Accepted 2026-05-30, N=3) — superseding the Reserved ADR-44 (N=2 hold).

**When:** `.dev-knowledge` (or any ecosystem-meta repo) audits a target repo against universal conventions (ADR-34 naming, ADR-38 architecture, ADR-41 backlog, etc.) and finds non-conformities to route. Distinct from § 16 Cross-Tool Review (within-repo Codex audit) and § 17 Code Quality Audit Process (within-repo audit cycle).

**Skip when:** target repo audits itself internally (no cross-repo routing needed).

### Three-stage flow
<!-- scope: meta -->

**Stage 1 — Audit (strażnik produces report)**

- Strażnik (`.dev-knowledge` or other ecosystem-meta repo) runs read-only audit against target repo's working tree against universal conventions.
- Produces dated artifact: `docs/audits/YYYY-MM-DD-<target-repo>-scrum-master-review.md`
- Findings grouped by severity (CRITICAL / HIGH / MEDIUM / LOW per § 17 convention).
- Audit is internal to strażnik repo; not yet routed.

**Stage 2 — Route (operator routes with cover letter)**

- Operator copies `templates/scrum-master-cover-letter.md`, fills placeholders, pastes cover letter + audit report contents to target repo architect (separate chat or browser session).
- Cover letter sets expectation: single round trip, architect implements in own repo, no delivery turn back.

**Stage 3 — Implement (target architect produces changes in own repo)**

- Target repo architect reviews findings and implements changes in target repo.
- Implementation evidence: commits + JOURNAL entry in target repo (CHANGELOG retired — §14). No browser-to-browser turn back to strażnik expected.
- Strażnik may verify (read-only) target repo JOURNAL / commits at next session start — informational, not gated.

### Addendum mechanism
<!-- scope: meta -->

If strażnik catches additional gaps after Stage 2 routing (audit gaps surfaced post hoc), produce a supplementary artifact rather than regenerating the full report:

- Naming: `docs/audits/YYYY-MM-DD-<target-repo>-scrum-master-review-addendum.md`
- Content: supplemental findings only; references the original audit by name.
- Routing: operator routes addendum alongside (or shortly after) the main cover letter.
- Addendum supplements; it does not supersede.

**Empirical reference:** ai-council scrum-master review 2026-05-11 produced 10 findings + addendum covering I7 (tasks/lessons.md location accepted-as-by-design) and I8 (underscore-prefix archive folder not flagged for rename). Addendum mechanism prevented full report regeneration.

### Distinction from cross-repo amendment handshake
<!-- scope: meta -->

| Aspect | Cross-repo amendment handshake (ADR-43 pattern) | Scrum-master review propagation (this section) |
|--------|--------------------------------------------------|------------------------------------------------|
| Nature | **Bilateral** — shared concern across two repos | **Unilateral** — strażnik recommends, target implements |
| Initiator | Either repo (concern emerges) | Strażnik repo (audit surfaces non-conformity) |
| Round trips | 1 (per "handshake = 1 round trip" principle) | 1 (per same principle) |
| Pushback handling | Continues in same handshake | Opens new conversation as separate handshake |
| Empirical example | ADR-34 propagation to ai-council 2026-05-11 | ai-council scrum-master review 2026-05-11 |

### Single-round-trip framing
<!-- scope: meta -->

Both patterns share the operator principle "handshake = 1 round trip". Cover letter explicitly states no Turn 2/3/4 expected. If target architect pushes back on a finding (disagreement, scope mismatch, by-design justification):

- Pushback does NOT continue the original routing thread.
- Pushback opens a **new conversation** framed as a separate handshake.
- Multi-turn ceremony for S-scale findings = over-engineering (per BOUNDARY in 2026-05-12 handoff: "do NOT generate multi-turn handshake ceremony for S-scale cross-repo changes").

### Cover-letter template
<!-- scope: meta -->

Use `templates/scrum-master-cover-letter.md`. Operator fills placeholders for target repo, review type, severity counts, top-3 findings, expected-response framing. Template cites first empirical instance (ai-council 2026-05-11) as reference.

### Rules
<!-- scope: meta -->

- Audit before route; never route before audit completes.
- Strażnik produces; operator routes; target architect implements. Never reverse roles.
- Strażnik does NOT directly edit target repo files. Cross-repo changes route via target architect.
- Pushback opens new handshake. Pushback does not extend the original routing.
- Addendum is for post-routing gap discovery; not for finding revisions (revisions = re-audit).

---

## Appendix A: Claude Code Shortcuts
<!-- scope: runtime -->

> Kept PLAYBOOK-local with reason (#158, Decision B): a Claude Code UI quick-reference with no in-repo canonical home — CLAUDE.md is 200-line-capped (see Appendix C "CLAUDE.md size limit") and `~/.claude/` is outside this repo. Retained here for discoverability; the deeper procedures→skills extraction is Move 2's scope.

### Permission Modes (Shift+Tab cycles)
<!-- scope: runtime -->

- **Default** — asks permission for everything. For sensitive/unfamiliar work.
- **Accept Edits** (Shift+Tab x1) — auto-saves files, asks before shell. **Daily driver.**
- **Plan Mode** (Shift+Tab x2) — read-only. Use when you don't know the approach.

### Keyboard
<!-- scope: runtime -->

| Shortcut  | What it does                        |
| --------- | ----------------------------------- |
| Shift+Tab | Cycle permission modes              |
| Esc Esc   | Rewind/undo to previous checkpoint  |
| Alt+T     | Toggle extended thinking            |
| Alt+P     | Switch model                        |
| Ctrl+C    | Stop generation                     |
| Ctrl+L    | Clear terminal screen (not session) |
| Ctrl+G    | Open prompt in external editor      |
| Ctrl+V    | Paste image                         |

### Slash Commands
<!-- scope: runtime -->

| Command            | When to use                                       |
| ------------------ | ------------------------------------------------- |
| `/clear`           | Between repos/tasks — #1 token saver              |
| `/compact`         | Mid-session when context heavy                    |
| `/compact [focus]` | Compress with focus ("focus on API changes")      |
| `/session-summary` | Before switching to Claude.ai browser             |
| `/usage`           | Check token usage (interactive TUI; use `ccusage --json` for scriptable export) |
| `/plan [prompt]`   | One-shot plan mode without cycling Shift+Tab      |
| `/model`           | Change model mid-session                          |
| `/effort`          | Change effort level                               |
| `/context`         | See what's using context window                   |
| `/resume`          | Resume previous session                           |

### CLI Flags
<!-- scope: runtime -->

```
claude --permission-mode plan      # start in plan mode
claude --permission-mode acceptEdits  # start in accept edits
claude -p "prompt"                 # headless non-interactive
claude -r "session-name"           # resume named session
```

### The ! Prefix
<!-- scope: runtime -->

Type `!` before any command to run it directly in shell without Claude processing:
```
!git status          # output goes to context, zero AI tokens
!pytest -x --tb=short  # see test results without asking Claude to run them
!cat src/config.py   # show file to Claude without a read request
```
Use for quick checks where you don't need Claude to interpret — just inject output into context.

---

## Appendix B: Model Routing Table
<!-- scope: llm -->

The model-routing table is canonical in **`~/.claude/ROUTING.md`** — deterministic, no judgment calls; the source of truth for which model (or no-AI) per task class. Not duplicated here (#158, Decision B: killed the resident copy — a cached table silently drifts from ROUTING.md). The **time-shifting schedule** below is PLAYBOOK-local (not in ROUTING.md) and is retained.

### Time-Shifting Schedule
<!-- scope: llm -->

| CET Time    | Activity                           | Rationale                                                         |
| ----------- | ---------------------------------- | ----------------------------------------------------------------- |
| 08:00-09:00 | Planning in Plan Mode (Opus)       | Fresh mind + off-peak ET                                          |
| 09:00-13:00 | Heavy implementation (Opus/Sonnet) | Off-peak ET (3-7AM). Golden window.                               |
| 13:00-14:00 | Break                              | Before peak begins                                                |
| 14:00-20:00 | Light work only                    | Peak ET. Code review (Sonnet), Haiku reports, manual coding, docs |
| 20:00-22:00 | Optional overflow                  | Off-peak resumes. Only if energy allows                           |

---

## Appendix C: Token Optimization Techniques
<!-- scope: llm -->

> Kept PLAYBOOK-local with reason (#158, Decision B): tactical token doctrine with no in-repo canonical home (CLAUDE.md is 200-line-capped; `~/.claude/` is outside this repo). Retained for discoverability; revisit in Move 2.

Ranked by impact/effort (Council-approved):

1. **`/clear` between tasks/repos** — 30-40% input tokens saved. Highest leverage. Build the habit.
2. **Front-load full spec** in first message — eliminates 2-3 discovery turns (15-25% fewer round-trips). Use prompt template from Section 2.
3. **Plan Mode before implementation** — catches bad approach at 200 tokens vs 5000.
4. **Line-range reads** `@file:15-80` — 10-15% savings on read-heavy sessions. Know your codebase.
5. **ROUTING.md enforcement** — Haiku for reports, no AI for trivial edits (15-20% total).
6. **`/compact` at task boundaries** — 12-18% context savings. Config: compaction at 40%.
7. **Batch related changes** in single prompt — fewer turns = less context repetition.
8. **VS Code first** — test explorer, Error Lens, GitLens = 0 tokens for informational queries.
9. **`!` prefix for quick commands** — `!git status`, `!pytest` run directly in shell, output goes to context without Claude processing. Zero AI tokens for simple checks.

### Golden Rule
<!-- scope: llm -->

**After 2 failed attempts at something → `/clear` and rewrite the prompt from scratch.** A fresh context with a clear prompt almost always works better than a polluted context full of failed approaches. Don't keep hammering — reset.

### CLAUDE.md size limit
<!-- scope: runtime -->

Keep CLAUDE.md under 200 lines per file. Instruction adherence drops above that. Use `.claude/rules/` for domain-specific rules and `.claude/skills/gotchas/` for institutional memory — these load separately and don't bloat the main prompt.

---

## Codemap workflow
<!-- scope: meta -->

The codemap section of every M/L `ARCHITECTURE.md` is an auto-generated embedded Mermaid block showing the repo's top-level Python packages, their import relationships, and their layer assignments (if `tach.toml` is present). VS Code 1.121 and GitHub render Mermaid natively — the diagram is clickable and navigable without a separate SVG pipeline. Governing authority: ADR-51 Decision 6 + amendment 2026-05-22.

**Mermaid theme directive (required on every block in `ARCHITECTURE.md`).** Every Mermaid fence in `ARCHITECTURE.md` (the codemap block AND every hand-authored diagram) opens with the custom-base theme directive `%%{init: {'theme':'base', 'themeVariables': {…}}}%%` so diagrams render readably on dark backgrounds; every `classDef` with a light `fill:` must also carry an explicit `color:` to prevent inherited-light-text on light-fill. Standard: ADR-51 amendment 2026-05-28 (v2). Enforcement: `scripts/audit.py` check #7 `mermaid_theme_directive` (scope: `ARCHITECTURE.md` + `templates/ARCHITECTURE-template.md`). The generator emits the directive automatically for the codemap block; hand-authored diagrams must include it manually — copy from the canonical example in `templates/ARCHITECTURE-template.md`.

### When the generator runs
<!-- scope: meta -->

A pre-commit hook (`codemap-freshness`) fires whenever Python source files, `pyproject.toml`, `tach.toml`, or `ARCHITECTURE.md` itself change. If the committed codemap block differs from a fresh generation, the hook exits non-zero and blocks the commit. The operator runs `generate --write` and re-stages `ARCHITECTURE.md` before retrying. The generator can also be invoked manually at any time for inspection.

### Manual invocation
<!-- scope: meta -->

```bash
# Dry-run — print generated Mermaid block to stdout (does not modify ARCHITECTURE.md)
python -m scripts.codemap.cli generate . --source-root <path>

# Write — replace CODEMAP-bounded region in ARCHITECTURE.md in place
python -m scripts.codemap.cli generate . --source-root <path> --write

# Check freshness — exit non-zero + unified diff if committed block is stale
python -m scripts.codemap.cli check . --source-root <path>
```

Default `--source-root` is `src/`. Repos with non-standard layout supply an explicit override:
- `.dev-knowledge` uses `scripts/` → `--source-root scripts`
- corp-monorepo uses `src/` → default applies

### Edge case handling
<!-- scope: meta -->

**Orphan modules** (zero in/out edges): the generator assigns the `:::orphan` class (dashed border) and emits a stderr warning. Investigate whether the package is legitimately unused (deletion candidate) or has runtime-only invocation (re-classification candidate). Orphans do not block commit.

**Circular dependencies**: nodes in the cycle get `:::cycle` class (red border); edges in the cycle are styled red. A circular dependency is an architectural smell — investigate import structure; common resolution is to extract a shared interface to a foundation layer.

**Missing `tach.toml`**: generator degrades gracefully — codemap is generated without layer color assignments. No warning emitted. Adding `tach.toml` post-hoc and re-generating restores layer colors.

**Missing `ARCHITECTURE.md` or CODEMAP markers**: generator fails with an operator-actionable error. Resolution: create `ARCHITECTURE.md` from `templates/ARCHITECTURE-template.md`, ensure both `<!-- CODEMAP:START -->` and `<!-- CODEMAP:END -->` markers are present, then re-run.

### Per-repo opt-in checklist
<!-- scope: meta -->

For an M/L repo to adopt generator-based codemap maintenance:

1. **Template instantiation.** Ensure `ARCHITECTURE.md` exists at repo root and contains `<!-- CODEMAP:START -->` and `<!-- CODEMAP:END -->` marker comments in the `## Codemap` section.
2. **Hook entry.** Add a local hook entry to `.pre-commit-config.yaml`:
   ```yaml
     - repo: local
       hooks:
         - id: codemap-freshness
           name: Codemap freshness check
           entry: python -m scripts.codemap.cli check . --source-root <path>
           language: system
           files: '(\.py$|^pyproject\.toml$|^tach\.toml$|^ARCHITECTURE\.md$)'
           pass_filenames: false
   ```
   Replace `<path>` with the repo's source root (`src` by default; override as needed).
3. **First generation.** Run `python -m scripts.codemap.cli generate . --source-root <path> --write` and inspect the diff.
4. **Commit.** Stage `ARCHITECTURE.md` and commit — the hook should now pass on all future relevant changes.

Authority reference: ADR-51 amendment 2026-05-22 § Per-repo adoption — opt-in, not mandatory.

### Troubleshooting
<!-- scope: meta -->

**Freshness check blocks an unrelated commit:** the hook fires on Python source changes even when the developer didn't intend to change the codemap. Run `generate --write` first, then retry the commit.

**Non-deterministic output across runs:** sort order, locale, or file encoding drift. Check that file discovery uses a sorted glob and that the generator's output is locale-independent. The codemap generator uses sorted package discovery to ensure determinism.

## Auto-TOC for large canonical docs
<!-- scope: meta -->

Large canonical docs carry an **auto-maintained table of contents** between `<!-- TOC:START -->` / `<!-- TOC:END -->` markers — **never hand-maintained** (a static TOC rots and contradicts the repo's "drift detected proactively" ethos). It mirrors the codemap mechanism exactly: generator-driven + freshness-gated.

- **Generator:** `python -m scripts.toc.cli generate <file> --write` (dry-run without `--write`). Parses the doc's own `##`/`###` headers into a nested anchor-link list with GitHub-compatible anchors. The full header text is slugged for the anchor (so `## Purpose [CORE]` → `#purpose-core`) while a trailing `[TAG]` is stripped from the visible link text; fenced code blocks are skipped.
- **Freshness gate:** the `toc-freshness` pre-commit hook (`python -m scripts.toc.cli check <file>`) fails-on-stale with a unified diff, exactly like `codemap-freshness`. It is a standalone hook (not an `audit.py` check), matching where `codemap-freshness` lives. The hook fires only on the target doc's own edits (the TOC depends solely on that doc's headers — no source-root dependency).
- **Adoption:** insert the two markers in the natural spot (after the title/intro, before the first `##` section), add a `toc-freshness` hook entry scoped to the file, run `generate --write`, and commit. Unlike the codemap (hardwired to `ARCHITECTURE.md`), the TOC CLI takes the target file as an argument, so the same mechanism applies to any doc.

Applied to `ARCHITECTURE.md`. **Not** auto-applied to every doc — add only where navigation overhead is real (see threshold note in ESSENTIALS). Authority: ADR-51 § Auto-TOC (same freshness regime as the codemap).

