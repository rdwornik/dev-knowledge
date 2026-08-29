---
reconciled_with: handoff-process@6.3.0
---

# Dev Practice Playbook

> **Living document.** Repeatable processes for everything Rob does regularly with AI-assisted development.
> Last updated: 2026-08-01
>
> *Section history lives in git (commit log + JOURNAL `Changes:` line), not in per-section changelog blocks — per ADR-49.*
>
> **Organization:** Two explicit parts. **Part I — Reference** (chapters Ch1–Ch14: System Architecture, the CLAUDE.md contract, repo conventions, documentation file types, session boundaries, Claude Code internals, …) → **Part II — Workflows** (numbered recipes §1–§21; the §18 gap is intentional — it was deleted; git has it) followed by **Appendices A–C** plus tooling addenda (Codemap, Auto-TOC). Every heading carries an ordinal under an explicit Part; the numbered spine is the workflow-recipe middle, not the whole document.

<!-- structure-allow: numbering-gap 18 — deleted, git has it -->

---

<!-- TOC:START -->
- [The two lifelines](#the-two-lifelines)
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
  - [Commit message standard](#commit-message-standard)
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
  - [Plan-review output contract](#plan-review-output-contract)
  - [Delivery format](#delivery-format)
  - [Architect → operator channel-discipline (execution actions)](#architect--operator-channel-discipline-execution-actions)
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
  - [Measuring the surface, rather than enumerating it](#measuring-the-surface-rather-than-enumerating-it)
  - [Declared-edge reconciliation (audit check `reconciled_versions`)](#declared-edge-reconciliation-audit-check-reconciled_versions)
  - [Prose-vs-state claim coherence (audit check `doc_claims`)](#prose-vs-state-claim-coherence-audit-check-doc_claims)
  - [Doc-rot / history-accretion (audit check `doc_rot`)](#doc-rot--history-accretion-audit-check-doc_rot)
  - [Prose structural coherence (audit check `doc_structure`)](#prose-structural-coherence-audit-check-doc_structure)
  - [Deployed-version record (audit check `deployed_methodology_version`)](#deployed-version-record-audit-check-deployed_methodology_version)
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
  - [Tree orchestration — architect-root + epic-chat lanes (ADR-97)](#tree-orchestration--architect-root--epic-chat-lanes-adr-97)
  - [The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110)](#the-batch-protocol--one-plan--n-lanes--one-integrator-adr-110)
  - [The lane lifecycle — five legs, and where each one is ruled](#the-lane-lifecycle--five-legs-and-where-each-one-is-ruled)
  - [The wave close — every dispatched wave ends D0–D5, and the funnel table is mandatory](#the-wave-close--every-dispatched-wave-ends-d0d5-and-the-funnel-table-is-mandatory)
  - [The night batch — the batch protocol run unattended, in five phases](#the-night-batch--the-batch-protocol-run-unattended-in-five-phases)
  - [Dispatch visibility — Agent View shows DISPATCHED sessions only (STANDING_RULINGS B7)](#dispatch-visibility--agent-view-shows-dispatched-sessions-only-standing_rulings-b7)
  - [Dispatching a session — the boundary, the dispatch table, and the standing rules](#dispatching-a-session--the-boundary-the-dispatch-table-and-the-standing-rules)
  - [Dispatch prompts and the contract of record — two locations, one of them in the tree](#dispatch-prompts-and-the-contract-of-record--two-locations-one-of-them-in-the-tree)
  - [The dispatch surface is `dispatch <file>` — the contract file is the source ([#509] v2)](#the-dispatch-surface-is-dispatch-file--the-contract-file-is-the-source-509-v2)
  - [Cloud lanes — the receipt gate and the fresh-branch rule](#cloud-lanes--the-receipt-gate-and-the-fresh-branch-rule)
  - [Model + effort are stated at dispatch — the routing matrix](#model--effort-are-stated-at-dispatch--the-routing-matrix)
  - [Handoff prep for the next architect — an index, not a restatement](#handoff-prep-for-the-next-architect--an-index-not-a-restatement)
- [Ch9. Tier-1 closure loop — usage](#ch9-tier-1-closure-loop--usage)
  - [Propagating a plugin change across the fleet](#propagating-a-plugin-change-across-the-fleet)
  - [The methodology↔project boundary (what IS methodology)](#the-methodologyproject-boundary-what-is-methodology)
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
  - [Night-batch work — the morning-loop wave from the night side](#night-batch-work--the-morning-loop-wave-from-the-night-side)
- [Ch12. Definition of done (organs)](#ch12-definition-of-done-organs)
  - [Definition of shipped (closure gate)](#definition-of-shipped-closure-gate)
- [Ch13. Continuous Improvement](#ch13-continuous-improvement)
  - [Project-evolution posture (always be improving)](#project-evolution-posture-always-be-improving)
  - [Pipeline overview](#pipeline-overview)
  - [Stage 1: Discovery](#stage-1-discovery)
  - [Stage 2: Triage](#stage-2-triage)
  - [Stage 3: Evaluation](#stage-3-evaluation)
  - [Stage 4: Decision](#stage-4-decision)
  - [Stage 5: Implementation (only for "Adopt")](#stage-5-implementation-only-for-adopt)
  - [Stage 6: Review (on-trigger)](#stage-6-review-on-trigger)
  - [Where evaluations are recorded](#where-evaluations-are-recorded)
  - [The window mandate — what a window owes, and what it is allowed to carry](#the-window-mandate--what-a-window-owes-and-what-it-is-allowed-to-carry)
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
  - [The intake pipeline — intent → intake doc → decomposition → epic lanes (ADR-98)](#the-intake-pipeline--intent--intake-doc--decomposition--epic-lanes-adr-98)
  - [Architect output vs CC consumption-spec](#architect-output-vs-cc-consumption-spec)
  - [Summary table (required at top of every formal prompt)](#summary-table-required-at-top-of-every-formal-prompt)
  - [How to choose Model](#how-to-choose-model)
  - [When to escalate to a Dynamic Workflow](#when-to-escalate-to-a-dynamic-workflow)
  - [How to choose Mode](#how-to-choose-mode)
  - [How to choose Effort](#how-to-choose-effort)
  - [Model / effort platform doctrine (Claude Code 2.1.x)](#model--effort-platform-doctrine-claude-code-21x)
  - [Structure](#structure)
  - [Multi-agent / fan-out prompt checklist (the browser-emitted mandate contract)](#multi-agent--fan-out-prompt-checklist-the-browser-emitted-mandate-contract)
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
  - [Council Debate Archival Protocol (RETIRED 2026-07-22)](#council-debate-archival-protocol-retired-2026-07-22)
  - [Council output convention (canonical-only since 2026-07-22)](#council-output-convention-canonical-only-since-2026-07-22)
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
  - [How to hand off — which mode, what to type (operator runbook)](#how-to-hand-off--which-mode-what-to-type-operator-runbook)
  - [Roles](#roles)
  - [Architect epistemic discipline: explicit verification markers](#architect-epistemic-discipline-explicit-verification-markers)
  - [Architect epistemic discipline: completion claims require state verification](#architect-epistemic-discipline-completion-claims-require-state-verification)
  - [Architect routing for technical proposals](#architect-routing-for-technical-proposals)
  - [Artifact generation direction](#artifact-generation-direction)
  - [Handoff paths](#handoff-paths)
  - [Token log cadence](#token-log-cadence)
  - [Output the operator copies into browser chat (render-layer note)](#output-the-operator-copies-into-browser-chat-render-layer-note)
- [9. Weekly Review (Friday)](#9-weekly-review-friday)
- [10. BACKLOG Grooming Workflow](#10-backlog-grooming-workflow)
  - [Schema (ADR-66; machine-checked by `scripts/validate_backlog.py`)](#schema-adr-66-machine-checked-by-scriptsvalidate_backlogpy)
  - [Per-handoff grooming (~2 min, mandatory for M+)](#per-handoff-grooming-2-min-mandatory-for-m)
  - [Quarterly deep grooming (~30 min, scheduled)](#quarterly-deep-grooming-30-min-scheduled)
  - [The grooming routine — the standing declaration ([#348] anchor)](#the-grooming-routine--the-standing-declaration-348-anchor)
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
  - [Codex-utilization doctrine (lanes + exact model strings)](#codex-utilization-doctrine-lanes--exact-model-strings)
  - [Codex dual-role — reviewer today, producer gated](#codex-dual-role--reviewer-today-producer-gated)
  - [DEGRADED-REVIEW — the fallback chain when the doctrinal reviewer lane is unavailable](#degraded-review--the-fallback-chain-when-the-doctrinal-reviewer-lane-is-unavailable)
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
- [20. Deploying the methodology corpus to a consumer (deploy runbook)](#20-deploying-the-methodology-corpus-to-a-consumer-deploy-runbook)
  - [The three phases — assess → execute → ratify](#the-three-phases--assess--execute--ratify)
  - [Operational nuances (learned on run #1)](#operational-nuances-learned-on-run-1)
  - [Floor semantics — tracked + hash-guarded (model A)](#floor-semantics--tracked--hash-guarded-model-a)
  - [What to expect on runs #2–4 (per-consumer divergences the run-#1 probe surfaced)](#what-to-expect-on-runs-24-per-consumer-divergences-the-run-1-probe-surfaced)
- [21. The delivery loop (end-to-end)](#21-the-delivery-loop-end-to-end)
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

## The two lifelines
<!-- scope: meta -->

The methodology maintains exactly two things; every chapter below serves one of them. Naming them is the frame.

**Lifeline 1 — Workflow.** The architect↔CC delegation loop: **decide → plan → delegate → verify → archive → educate.** Judgment-phases (plan / verify / archive / educate) are the architect's and are never delegated; build-phases (implement / test / deploy) are delegated to CC but *owned* by the architect — "merged" ≠ "done", and the architect declares closure on the hard end-state, not on "tests pass." The loop runs across the three layers (`ARCHITECTURE.md` Ch1 "Layer Boundaries & Invariants" / ADR-28 — canonical there, not restated here): L1 browser-architect → L2 `.dev-knowledge` → L3 Claude Code. Transition gates that keep the loop honest: `HANDOFF_BOOT` (orientation), the ship-gate, the Stop-gate, `block_immutable_edits`, `block_ff_push`.

*The architect↔CC division (ADR-87 equilibrium — canonical here; §2 and §8 point to this table, do not restate it):*

| Resident in the browser (architect) | Outsourced to CC |
|---|---|
| decompose, prioritize | pick the model |
| choose MODE (plan vs auto) | fill the prompt skeleton |
| decide parallel / worktree | load code-impact context |
| review + verify CC's output | load generic gotchas |
| declare closure (hard metric) | execute + commit |
| off-repo inputs + governance-pointer | self-load the rest |

The architect emits **intent + closure + anti-patterns + MODE + a thin governance-pointer**; CC self-loads everything else. **Model is CC's pick** — default Opus 4.8 (the floor); CC may route smaller for mechanical sub-steps. The architect does **not** choose the model; effort is set by token budget. Full rationale: ADR-87.

**Lifeline 2 — Coherence.** The corpus stays internally consistent across four dependency edge-types. Each has a *discovery / compute* half and a *gate / enforce* half:

| Edge | Mechanism | State |
|---|---|---|
| **code↔code** | reverse-dependency oracle computes referrers before a module is removed | oracle built; consuming gate = #195 safe-removal **(M1) shipped** (audit check #24, `scripts/safe_remove.py`; #195 closed 2026-06-26) — M2+M3 deferred as **#218**. The import-cycle gate was **refuted by data** (one defect in 28 nodes) → fixed by dependency inversion; no standing gate. |
| **code↔doc** | rule-ID `<domain>-<slug>`: doc-side `<!-- rule: -->` ↔ code-side `# rule:`, resolved by the `doc_code_edge` check | gated for the curated rule set; completeness via #201 (`resolver-allows-N`, **ADR-90**) → #202 → #203. |
| **doc↔doc** | `reconciled_with: <spec>@<version>`: the gate checks the version stamp; `check-against-spec` (triggered on a bump, #205) checks the content was re-reasoned | declared-half gated; undeclared-discovery is advisory-only. |
| **undeclared** | `scan_undeclared_edges` surfaces prose references lacking a declared edge | surfaces as a ship-gate **WARN** leg (`check_undeclared_edges` in `ALL_CHECKS`, #179 / Fable consult #1 ruling #2, 2026-07-03); awareness-only — one WARN per candidate, never FAIL, does **not block** the commit. |

**The sealing test (applies to both lifelines):** *"does this mechanism have its consumer / gate?"* — and its refinement, *"is there real signal for a consumer to act on?"* The answer can be **no**: the import-cycle gate was the right shape but guarded nothing, so it was declined. *Built-without-consumer* is the recurring failure class both 2026-06-25 audits found; this test is the standing guard against it.

**Chapter map — every chapter below serves one lifeline (the frame is the backbone; this map organizes, it does not renumber):**

- **Lifeline 1 — Workflow** (the delegation loop): Ch2 (CLAUDE.md contract) · Ch4 + §2 (the prompt contract) · Ch5 (build / test) · Ch7 + §6 + §16 + §17 (review / verify) · Ch8 (session boundaries) · Ch9 (closure loop) · Ch12 (definition of done) · Ch14 (Claude Code internals) · §1 §4 §5 §7 §8 (new-project / lessons / Council / long-session / handoff recipes).
- **Lifeline 2 — Coherence** (corpus consistency): Ch3 (repo conventions) · Ch6 (doc-file types + freshness / amendment / reconciled-edge checks) · Ch11 (nightly conformance mesh) · §10 (BACKLOG grooming) · §14 (markdown governance) · §19 (scrum-master propagation).
- **Cross-cutting** (frame both): Ch1 (system architecture) · Ch10 (two-tier automation) · Ch13 (continuous improvement) · §3 §9 §11 §12 §13 §15 (absorb / weekly / tool-eval / multi-project / where-knowledge-lives / anti-patterns) · Appendices A–C.

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

**Purpose:** Each repo (corp-monorepo, ai-council, .dev-knowledge, future projects) has a `CLAUDE.md` at root. Auto-read by Claude Code on session start. Auto-read by Codex via `project_doc_fallback_filenames = ["CLAUDE.md"]` in `~/.codex/config.toml`. **The per-repo agent-instruction layer is TWO files with one contract (ADR-115, 2026-08-25, superseding ADR-53 Decision 2):** `AGENTS.md` carries the portable half (≤120 lines, non-inferable facts) and `CLAUDE.md` the Claude-runtime half plus the `@AGENTS.md` importer, at ≤200 lines. No fact is duplicated — the importer is what preserves ADR-53's substance, one place where each fact lives. ADR-53's three authority levels stand unchanged.

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
- Pointers to archived/retired/deleted content — root and `CLAUDE.md` reference only CURRENT surfaces; archived detail lives in `templates/archive/`, `LESSONS.md`, or `docs/` (git history + the CLAUDE.md §12 changelog preserve provenance). An archived command must not head a live protocol list. Per [#330] / parity-register g2. (A marked "do not recreate X" guardrail that names a deleted file is the rule working, not a violation — the ban is on *live* pointers to archived surfaces.)

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
<!-- rule: governance-child-floor -->

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
asks back before unilateral interpretation. Applies broadly, not just to the
handoff process. (Origin: the v4.1 handoff first run carried a recalled claim as
witnessed; Phase-2 verification caught the drift — the upstream discipline avoids
it in the first place. Incident: LESSONS 2026-05-30.)

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

**Two-tier new-path rule — convention-compliance IS authorization (ADR-101 amendment 2026-07-18).**
Block convention-**VIOLATING** creations and **never** convention-**COMPLIANT** ones. Two tiers, and
which one applies decides whether you STOP:

- **Tier 1 — pattern-sanctioned new paths:** a new **file** matching a **codified, citable**
  convention. Currently-effective set: ADRs at `docs/decisions/ADR-NN-{slug}.md` (ADR-34); intake
  docs at `docs/intake/YYYY-MM-DD-{func|tech}-slug.md` (ADR-98 + `docs/intake/README.md` §4);
  `docs/audits/*.md` per the ADR-101 §2 / R3 / R4 grammar; JOURNAL entries. For a covered class the
  executor **derives the path, CITES the governing source in the log/commit message, and PROCEEDS**
  — **no per-instance operator STOP** (the citation is the audit trail).
- **Tier 2 — unsanctioned paths:** any **new FOLDER**, any file matching **no** codified pattern, or
  any **ambiguity** about which pattern applies → **operator authorization required; absent → STOP.**

Two standing riders: **any ambiguity about which pattern applies = tier 2 = STOP**, and the
**citation is MANDATORY for every proceed — no citation, no proceed.** **Folder creation stays
hard-gated in ALL cases** — every new folder is surfaced *before* creation. **Path authorization is
not content authorization** — creating an ADR/intake file at its sanctioned path does not approve the
decision or content inside it. The rule is **in force now** by operator ruling; until the #345
registry-driven gate lands it is upheld by executor/reviewer discipline (cite-and-proceed / STOP),
not by machinery. (Distinct from Ch10's "two-tier automation doctrine" — same adjective, unrelated
axis.)

### Commit message standard
<!-- scope: dev -->

Git history IS the changelog (no CHANGELOG.md since 2026-05-16) — commit messages carry the load CHANGELOG used to. (Moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the pointer.)

- **Conventional Commits.** `type(scope): summary` — types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Scope is optional but use the file/folder slug when it clarifies.
- **Summary line.** Imperative mood, specific, describes WHAT changed. Under ~72 chars. **Never** "wip", "fix", "updates", "stuff", "various changes".
- **Body required for any non-trivial change.** WHAT changed and WHY — enough detail that `git log` answers "what happened here" without a separate changelog. One-line typo fixes can skip the body.
- **One logical change per commit.** If you'd write "and" in the summary, split the commit.

`/save` follows this standard. See CONTRIBUTING.md for live examples and the pre-commit hook list.

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

**[UNRULED — no ADR claims this; carried as an open question by intake #57]**

Standardize location of `.secrets/` (today: a single absolute path under the operator's home, outside any repo, loaded by the global PowerShell profile -- the path itself is deliberately NOT restated in a deploy-carried governance doc). Rule covers: path convention, what kinds of repos use this, whether per-repo `.env` is allowed, how the global PowerShell profile auto-loads relate.

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

> **Cross-ref (ADR-87):** the architect↔CC equilibrium contract refines this — the architect emits intent + plan/auto mode + a thin governance-pointer, and CC self-loads code-impact context + generic gotchas. The division is canonical in **"The two lifelines" § Lifeline 1** (the equilibrium table); this section and §2 "Creating a Claude Code Prompt" both cover prompt authoring and **point to** that table rather than restate it. Full rationale: ADR-87.

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
- **Scale L** (3+ files, architectural): full template required, prefer `plan-then-auto` mode for review checkpoint after Step 1. **L-sized epic stories default plan-first** (full plan mode, reviewed before execution), and **every architect prompt re-declares MODE** — a lane/session inherits no mode from a prior prompt (HANDOFF_PROCESS §14a item 7; the 2026-07-06 plan-gate corrective).

### Plan-review output contract
<!-- scope: meta -->

In plan mode, what the operator is asked to decide is surfaced as a **structured, addressable choice — an option-select (pick one/several) or a typed answer — NEVER a free-form dialog exchange.** A ruling given as a dialog turn dies with the session (a hung/closed chat takes its conversation with it), so a plan-review answer must be a durable, citable artifact: an `AskUserQuestion`-style option-select, or an explicit "type X" instruction whose answer lands in the plan/prompt. Corollary: `ExitPlanMode` presents the plan for approval; any fork it raises is an option-select, not "let's discuss." This is why operator rulings live in prompts/plans, not conversation (LESSONS 2026-07-12 ruling-addressability; the FR-4 ruling-addressability requirement, intake #14 ruled pack) — a later session must be able to cite "already ruled @ &lt;ref&gt;", which a dialog turn cannot provide.

### Delivery format
<!-- scope: meta -->

Prompts are **downloadable `.md` artifacts**, not inline code blocks. Browser chat outputs them as fenced markdown blocks; Rob saves as file, then pastes file content into Claude Code's prompt field.

Why: pasted-as-text is fine, but file form preserves structure for re-use, audit, and handoff.

### Architect → operator channel-discipline (execution actions)
<!-- scope: meta -->

The browser-chat architect never writes git commands, shell sequences, or executable code inline in chat prose as informational text the operator manually copies. Two channels only, scale-determined (moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the frame + pointer):

- **Scale S** (one command, one mechanical edit, no judgment): PowerShell snippet in a fenced code block; operator copy-pastes and runs as-is.
- **Scale M+** (multi-step, multi-file, judgment needed, merge ops): Claude Code prompt as a downloadable `.md` file with full structure per this chapter.

**Test:** if the operator has to edit, paraphrase, or interpret anything when copying, the format is wrong.

**Report-direction sibling (intake #18 A1):** any load-bearing CC→browser report longer than one
screen ends with `=== END — {k} sections ===` — the truncation-visibility mechanism of the paste
END sentinel (HANDOFF_PROCESS §13), applied in the report direction; a report without its END
line is truncated, and the reader says so and stops.

Sourced from LESSONS #10 (2026-05-13). Architect-side enforcement is operator-review; mechanical enforcement on executor side via the Claude Code harness.

**Authorized integration act (transcribed 2026-07-31, [#446] window).** Merging to `main` is an
operator-authorized act, granted per-act, not agent judgment.

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
- [ ] **TARGET-REPO guard is line one** (cross-repo prompts) — every prompt whose work lands in a repo other than the session's own opens with `TARGET-REPO: <absolute path>` as its **first line, above the parameter table and before any instruction** (skeleton: §2 "Structure"). Not buried in a REPO field mid-prompt: a session that reads the task before it reads the target has already begun reasoning against the wrong tree, and the hub↔consumer confusion is the expensive one (Ch8 "Hub→consumer writes"). Pairs with — does not replace — *Absolute paths* and *Out-of-scope items explicit* above.

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

**Paste-vs-file transport — a partial artifact reads as a whole one.** A paste channel can deliver a truncated artifact that looks complete, and the cost lands on the *reader's assumption that it arrived whole* rather than on the transport. Two instances in the 2026-08-10/11 window: a lane stood blocked for an hour on an unverified assumption that a half-landed paste had landed whole, and the browser paste channel later degraded to empty frames mid-window. The cheap discriminator is a check the reader can run before acting — the artifact's own tail, a line count, the closing fence. The mechanical half already exists as `STANDING_RULINGS` **I-D3** (a batch lane's contract is COMMITTED to the repo before dispatch), which takes the paste channel out of the path entirely for the artifact class where it cost the most.

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

#### Tiered suite — targeted in-lane, one full suite at integration
<!-- scope: dev -->

The cadence above states *when* the suite runs; this states *which* suite. A batch lane pays a
suite run once per step plus once at its merge, so an undifferentiated full suite multiplies
across a batch instead of being paid once. **Tier A — the targeted gate** runs in-lane, per step:
the test files covering the lane's own diff. **Tier B — the full suite** runs once, at
integration, on the merged result (the refuse-to-finish item in Ch8's batch protocol). Per-lane
greens are evidence about each lane in isolation; the merged tree is a state no lane exercised.

**Measured basis.** Host full suite **918.9 s** (`JOURNAL.md` 2026-08-15 (a)). On a 4-core cloud
container — INDICATIVE, so ratios travel and absolute minutes do not — the same tree ran
**701.6 s** serial against **473.0 s** at `-n auto`: a 1.48× ratio, with the outcome sets
identical in both arms (14 failed / 2874 passed / 8 skipped / 1 xfailed, set-differenced both
ways). The suite is not uniformly slow — one test carries 38.4 % of it, and 2489 of 2897 tests
share 11 % between them. Excluding five files leaves 96.5 % of the tests at 22.1 % of the cost,
which is where tier A comes from. Source: the night-2 lane-latency audit, landed on `main` at
`docs/audits/2026-08-14-technical-night2-latency.md` §1–§3, whose §3 tier-A
figure is derived arithmetic that the audit itself flags as not measured.

**The exclusion set — five files, and why each is integration-only.**

| Tier | Files | Why |
|---|---|---|
| Oracle | `test_safe_remove.py`, `test_reverse_dep_oracle.py`, `test_legibility_graph_conformance.py` | each drives a real `pyright-langserver` subprocess; the cost is I/O-wait on an external language server, and these are the only tests needing one |
| Corpus | `test_normalize_headers.py`, `test_toc.py` | whole-repo corpus scans — cost scales with the doc tree and is invariant to a lane's diff |

**A cost split is not a correctness split — the oracle-tier rule.** A lane that touches
`scripts/safe_remove.py` or `scripts/reverse_dep_oracle.py` runs the oracle tier in-lane, because
those modules are exactly what that tier covers. The general form is *tier A plus anything
covering the touched module*, which is [#278] (impacted-test selection); until that lands, the
named-module rule above is its checkable subset. Two limits stated rather than left to be
discovered: the existing `slow` marker does **not** express this split — it marks
`test_e2e_consumer_lifecycle.py` and `test_fleet_analytics.py`, neither of which is in the top-10
cost list, so `pytest -m "not slow"` removes almost none of the 89 % — and deferring the oracle
tier to integration defers real signal on a host where the oracle works.

**Settings ladder — what makes xdist safe in a gate context**, ordered by what each buys. Source
for the whole ladder: the night-2 research audit, landed on `main` at
`docs/audits/2026-08-14-technical-night2-research.md` §2.2–§2.6 (blob `c01efd44`).

1. **`--max-worker-restart=0`.** xdist's default restart budget is `numprocesses × 4`, so a
   crashed worker is replaced silently up to 4N times — the witnessed 19 strays sit inside what
   that default permits. Zero converts quiet proliferation into a loud, bounded failure, which is
   the honest posture for a gate: one that restarts workers quietly reports a verdict it did not
   earn.
2. **The tier split above.** A full suite inside a commit hook is the multiplication risk itself,
   and parallelism is not its cure.
3. **`--maxprocesses=N`** caps `-n auto` so a high-core host does not pay N full-suite imports
   inside a gate. `-n auto` counts *physical* cores; `-n logical` wants `psutil`, which is absent
   from the lock.
4. **`-n 0` for anything running inside a forking parent** (mutmut forks one process per mutant).
   `-p no:xdist` is **not** a way to force serial — it unloads the plugin that supplies the `-n`
   which `addopts` already passes, so pytest exits 4 before collecting a single test and the run
   looks green while measuring nothing (`pyproject.toml` L83–91, measured twice in-repo).
5. **`--dist loadfile` / `loadgroup`** for tests sharing the real tree (the `live_repo` marker),
   which keeps them on one worker; `--dist worksteal` is the default for the balanced remainder.
6. **`-p no:cacheprovider` in hook context** keeps `.pytest_cache` writes out of a mid-staging
   tree.
7. **A detection leg, because no setting covers a killed controller.** execnet spawns workers
   with a plain `Popen` — no process group, no Job Object — so on Windows a controller that dies
   before teardown orphans its workers, which survive holding pipes open. They carry a constant
   bootstrap command line, so detection is exact and a blunt image-name sweep is unwarranted (it
   would take out the operator's own live interpreter):

   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
     Where-Object { $_.CommandLine -like '*exec(eval(sys.stdin.readline()))*' } |
     Select-Object ProcessId, CreationDate, CommandLine
   ```

Live call site carrying items 1 and 5: `.claude/skills/verify/verify.py` ([#528] leg 1).

#### The cadence — a per-unit budget (ratified 2026-08-28)
<!-- scope: dev -->

The split above names two tiers; this names how often each is paid, in three units:

- **Per merge** — the targeted checks covering that lane's own diff (Tier A). Every merge pays it.
- **Per batch** — the full suite is paid exactly **ONCE**, not once per lane.
- **Where that one payment lands** — integration, on the merged result (Tier B).

Stated as a budget because the failure it prevents is arithmetic. A six-lane batch running an
undifferentiated full suite per step pays the 918.9 s figure above a dozen times over, on lanes
whose diffs a targeted selection already covers. Per-lane greens stay evidence about each lane in
isolation, which is exactly why the one batch-level payment lands on the merged tree rather than
being spread across lanes that greened before that tree existed.

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

**Worked example (#141 vacuous claim-3 test):** a claim-check assertion
`status != "skipped" or actual` let a *skipped* result pass whenever `actual` was
non-empty (a skip always carries a non-empty `actual`), so the test could not tell
"evaluated and matched" from "silently skipped" — it pinned the implementation's
reachable states, not the criterion (claim-3 *must* evaluate). Fixed by mocking the
pytest subprocess so the deriver actually runs, then asserting `status == "match"`
**and** `status != "skipped"`, with the infra-skip path split to its own test
(`tests/test_validate_doc_claims.py::test_reconcile_evaluates_test_count_when_expensive`).

The rule: a test must be able to distinguish "criterion met" from "criterion
silently not evaluated." If it can't, it is testing the implementation, not the
acceptance criterion.

**Structural over enumerated.** Where a mechanism declares which keys, paths or globs it
covers, derive that set from the mechanism's **own config** at test time — not as a hand-built
literal list. A literal list agrees with the code the day it is written and
diverges silently forever after, and the test still passes because it compares the author's
intention with itself. Live instance: `scripts/gen_intake_index.py:44` compiles
`_FM_KV_RE = r"^([a-z0-9-]+):\s*(.*?)\s*$"` — a frontmatter key class with **no underscore** —
so `last_reviewed:` and `review_date:` match nothing while `status:` and `id:` match. The probe
is green because it is looking at zero keys.

**A mechanism needs its own verification.** A gate, probe or generator is not verified by
running and reporting green — green then means only "it executed", which is not the claim it
makes. It is verified by a test that constructs the input it claims to catch and proves it
catches it. ADR-81 leg (e) already requires demonstrated *firing* for an enforcement organ
(Ch12); this generalizes the same bar past enforcement to any mechanism that reports a verdict.

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
| `LESSONS.md` | Process lessons learned | Append-only with `[scope: X]` inline (per ADR-29) | When new lesson emerges (auto-promote at 2× repeat) | Rob, future Claude | Append-only (chronological legacy-archival split option per ADR-29 amend. 2026-07-17) | Universal (`.dev-knowledge` only) |
| `logs/TOKEN-LOG.md` | Claude usage snapshots | Threshold-triggered (7-day) via /session-summary | Auto when stale | Rob | Newest-first (prepend) | Universal (`.dev-knowledge` only) |
| `ENVIRONMENT.md` | Tooling state, what's installed | Sectioned, scope-tagged | When tool adopted/deprecated | Rob, Claude Code | Living (sections updated) | Per-repo |
| `docs/decisions/ADR-NN-*.md` | Architectural decisions | Michael Nygard format | When decision binds | Rob, future contributors | Numbered, immutable (amend in-place per ADR-29) | Per-repo |
| `docs/decisions/transcripts/council-out-*.md` | RETIRED 2026-07-22 (ADR-43 amendment 2026-07-23) — routed-mirror retired, hub archive deleted (`b4435fad`); transcripts are canonical-only in `ai-council/output/`; row kept for legacy context | Multi-model debate transcript | n/a | Historical reference (git history) | n/a | Removed |
| `docs/handoffs/YYYY-MM-DD-*/` (v5.4 bundle) | Chat-to-chat session summary | Flat bundle entered via `HANDOFF_BOOT.md` (operator session entry) + CC-owned residual/probe-manifest, per HANDOFF_PROCESS v5.4 (ADR-82); legacy v4 `README.md` + `01_ROLE`…`07_ASK_BACK`, single-file, and v3.x `contents/` bundles preserved as history | When session boundary requires continuity | Next browser chat | Dated, immutable | `.dev-knowledge` only |
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

### Measuring the surface, rather than enumerating it
<!-- scope: meta -->

**Before a cross-cutting change, grep the repo and classify every hit.** An enumerated list of
affected sites — the kind a seat writes from memory, or inherits from a previous packet — is a
fact *carried* rather than *derived*, and it fails in the direction hardest to see: it omits. The
list reads as complete because every entry on it is real.

**Measured basis (2026-08-28).** The `handoff-process` version sweep resolved to **874 hits**
across the corpus. Classifying all of them surfaced **six live false statements in a file no list
named** — a file that no enumeration produced, and that only the measurement reached. The
operator-ratified wording of this term is recorded verbatim as a lesson in `LESSONS.md`
(2026-08-28); the chapter states it here in its own declarative voice.

**The three version classes — what "classify every hit" actually produces.** Each hit sorts into
exactly one class, and the sorting *is* the work:

| Class | What it is | What happens to it |
|---|---|---|
| **LIVE-NORMATIVE** | a version claim governing current behaviour | updated to the new version |
| **STRUCTURAL-LEGAL** | a name that merely *contains* a version — a folder, an archived filename, an id | left alone: a folder name is not a version claim |
| **HISTORICAL-IMMUTABLE** | a citation of what was true at a past moment | left untouched: rewriting a `v4.4` citation fabricates history |

The third class is where a well-meant sweep does its damage. An unclassified find-and-replace over
874 hits reaches into immutable records and edits the past silently — the edit looks like
maintenance and reads, later, like evidence. `amendment_coherence` above gates the LIVE-NORMATIVE
class on the surfaces it manifests; the other two classes have no gate at all and rest entirely on
this classification being performed.

### Declared-edge reconciliation (audit check `reconciled_versions`)
<!-- scope: meta -->
<!-- rule: coherence-spec-reconciled -->

**A doc that declares a dependency on a versioned spec must not drift from it.** A dependent carrying a `reconciled_with: <spec-id>@<version>` edge MUST match that spec's live version; a drifted edge **FAILs** (`scripts/audit.py` `reconciled_versions`, in `ALL_CHECKS` → runs in `audit health` and `audit run`; teeth in `scripts/validate_reconciliation.py`). This is the **declared half** of dependency coherence — the ADR-88 coherence spine (#172) — the complement to the undeclared-edge discovery scan (`scan_undeclared_edges.py`, #179, awareness-only). The spec registry is `_SPEC_REGISTRY` in `validate_reconciliation.py` (v1: `handoff-process`); add a spec there when a new versioned dependency must be tracked. Child-repo-safe (an absent edge skips); read-only. Distinct from `amendment_coherence` above: that guards hand-maintained version *mirrors*; this guards *declared* `reconciled_with` *edges*.

**Re-stamp flow — the semantic half (#205).** A `reconciled_versions` mismatch (a spec version bump) is a signal to **reconcile**, not to blindly re-stamp the version number. The reconcile step is the `check-against-spec` skill: enumerate every candidate reference site in the dependent and verdict each (`stale | fine | not-relevant`) so a missed walkthrough step or un-updated diagram cannot pass silently. The trigger is wired into the reconciled_with discipline itself — `validate_reconciliation.py` (CLI + `restamp_invocations(repo_root)`) **emits the exact `check-against-spec` invocation on each mismatch**, and the `reconciled_versions` FAIL remediation points at it. Procedure on a bump: (1) `py scripts/validate_reconciliation.py` (or read the FAIL) → copy the emitted invocation; (2) `py scripts/coherence_enumerator.py --dependent <dep> --spec <spec> --old-version <old> --new-version <new>` for the by-category site skeleton; (3) invoke `check-against-spec`, verdict EACH site, put the filled checklist **in the re-stamp commit message**; (4) bump `reconciled_with` in the same commit. **The ship-gate is deliberately NOT the trigger** (recorded note): the gate gates the version mismatch only; running or passing `check-against-spec` is never a gate condition (the semantic skill's v1 scope forbids gating it — gating every reconciliation on an LLM verdict is the false-positive death-spiral the nudge/gate split exists to avoid). The skill fires from the re-stamp flow, not from `audit ship-gate`.

### Prose-vs-state claim coherence (audit check `doc_claims`)
<!-- scope: meta -->
<!-- rule: coherence-doc-claims -->

**A living doc's self-contained, deterministically-checkable CLAIMS must match repo ground truth.** A count/list a doc asserts about itself — the `ALL_CHECKS` check-count + the pytest-collected count in `ARCHITECTURE.md`, the pre-commit hook count/roster in `ARCHITECTURE`/`CLAUDE.md` — is reconciled against live state by `scripts/audit.py` `doc_claims` (in `ALL_CHECKS`; teeth in `scripts/validate_doc_claims.py`, a data-driven claim registry). A drifted claim → **WARN** (advisory; the expensive pytest-collected claim runs off the per-commit gate). Single-doc accuracy only: history-accretion bloat is `doc_rot` below, cross-file fidelity the coherence spine (#179–#182). Child-repo-safe; read-only (#89).

### Doc-rot / history-accretion (audit check `doc_rot`)
<!-- scope: meta -->
<!-- rule: coherence-doc-rot -->

**A living doc must not accrete unbounded history past its grooming thresholds.** Five read-only sub-detectors in `scripts/validate_doc_rot.py` (surfaced via `scripts/audit.py` `doc_rot`, in `ALL_CHECKS`) flag BACKLOG inline-history accretion (ARM 1 — citation-blind dates, with a span term), BACKLOG row length against a declared ceiling (ARM 2, split out by `[#532]` because length is a different property from accretion), per-section Section-history accretion, file-bloat vs a self-declared line budget, and grooming-cadence lapse — one **WARN** per locus, DETECT-ONLY (never condenses). Load-bearing doctrine: ADR-65 condense-to-git / ADR-49 retired changelogs / ADR-41 cadence (ADR-88 FC4). Pre-existing loci are grandfathered in the disposition register; read-only (#140).

**The row carries a pointer, the record carries the record.** When a tracked row and a durable record both want the same content, the record takes the load and the row keeps a one-line pointer. This is a container rule, not a style preference: `_BACKLOG_ROW_CEILING` caps a BACKLOG task line at 1320 chars — ARM 2's declared ceiling, which superseded `_BACKLOG_GROSS_CHARS` at 1200 when `[#532]` split the check — so a row absorbing narrative becomes physically unwritable and the failure surfaces as a doc-rot WARN at commit time rather than as a design signal. It blocked a write twice in two days in 2026-08, both measured against the then-current 1200 — `[#457]` sat at 1182 of 1200, and `[#383]` measured 1206 as its irreducible minimum before a wave record took the load. At the 1320 ceiling neither of those two crosses, which is worth stating plainly: the container argument rests on the mechanism, not on those two figures. Read the ceiling as the mechanism saying the content is in the wrong container. The escape is **not** a disposition: every past `warn-doc-rot-backlog-*` entry in the register is `(cleared …)`, resolved by condensing.

### Prose structural coherence (audit check `doc_structure`)
<!-- scope: meta -->
<!-- rule: coherence-doc-structure -->

**A living doc's structure — section numbering, header scheme, ToC accuracy — must stay internally consistent.** `scripts/validate_doc_structure.py` (surfaced via `scripts/audit.py` `doc_structure`, in `ALL_CHECKS`) lints numbering integrity, header-scheme consistency (the canonical heading-scheme convention it enforces is stated once at §"Heading scheme — canonical statement", not restated here), ToC accuracy, and dangling-allow self-policing — one **WARN** per locus, DETECT-ONLY (never renumbers); documented-intentional gaps pass via co-located `structure-allow` markers. Distinct failure class from `doc_rot` (structural shape, not history-accretion); read-only (#192).

### Deployed-version record (audit check `deployed_methodology_version`)
<!-- scope: meta -->

**Each repo's deployed methodology-corpus version (ADR-91) is recorded in one committed registry and reported per repo.** Record-home: `ecosystem/deployed-versions.yaml` — a dedicated committed registry on the `tool-versions.yaml` durable-version pattern (committed · written-by-command · read-by-a-check). Deliberately **NOT** `ecosystem/index.yaml` (a *derived* rollup `audit.py::regenerate_index` overwrites wholesale each run → a field written there is clobbered) and **NOT** the gitignored `state.yaml` (non-durable). **Write-contract:** the field is set by the **deploy-runbook** at deploy time (now built — the ADR-92 deploy tool; operational how-to at §20) to the corpus release it deployed (the ADR-91 `vMAJOR.MINOR.PATCH` git tag) — never hand-fabricate a value (a value cannot precede its release; every repo stays `null` until a release is tagged). **Reader:** `scripts/audit.py` `deployed_methodology_version` (in `ALL_CHECKS`; `exempt` in `doc-code-edge.yaml` — a status reporter, not a doc→code rule) reads the registry by repo directory name → `n/a` while unset (the expected pre-deploy state), `pass` with the version once set — surfaced per repo through `fleet_health`. This version-aware signal supersedes a raw-commit-count drift indicator. Full doctrine: ADR-91; record-home rationale also in ADR-91 "Record-home decision".

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
- Council debates (research-mode and pick-mode) → canonical `ai-council/output/` only; the ADR records the decision (routed-mirror into `docs/decisions/transcripts/` retired 2026-07-22 per the ADR-43 amendment 2026-07-23). The retired `research/` folder is no longer used (2026-05-27 ADR-60 amendment).

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

**Authoritative spec: `protocols/HANDOFF_PROCESS.md` v6.3.0** — the single live source of truth for handoff mechanics. This is a pointer, not a duplicate; do not re-document the structure here (the duplication is what drifted).

Formats in `docs/handoffs/`, all but the current one historical:

- **Legacy single-file (before 2026-04-27)** — one dated `YYYY-MM-DD-slug.md` free-form summary. Preserved as-is; do not migrate.
- **v3.x folder bundle (2026-04-27 → v4 rollout)** — `upload-instructions.md` + `first-message.md` + a `contents/` subfolder of point-in-time copies. **Superseded**; preserved as point-in-time history, never regenerated.
- **v4 bundle (2026-05-29 → v5 flip 2026-06-11; historical)** — flat `docs/handoffs/<slug>/` = `README.md` + `01_ROLE`…`07_ASK_BACK`, generated from source via a two-phase flow. **Superseded by v5**; existing bundles preserved as history, never regenerated.
- **v5 handoff (current)** — CC-owned: a lean **residual** + **probe manifest** under `docs/handoffs/<slug>/`, plus a thin browser boot (`protocols/HANDOFF_BOOT.md`) that replaces the multi-file bundle. Generated from live state at handoff time; teeth-y forced primary-source read. Full structure in `HANDOFF_PROCESS.md` §2–§5.

**Supplement authorship (transcribed 2026-07-31, [#446] window).** `SUPPLEMENT.md` answers are
**architect-authored**; the executor supplies verified facts only. The executor may gather, quote
and check — it does not compose the strategic answer, because the supplement is where judgment
travels between seats, and judgment sourced from the seat that did the work is not a second opinion.

### Order conventions
<!-- scope: meta -->

Per Token-LOG flip 2026-04-24:

- **Newest-first (prepend):** TOKEN-LOG, JOURNAL (CHANGELOG retired — §14). Rationale: logs optimize for current-state scanning. (JOURNAL flipped 2026-04-27 — original Stream B Gap #4 spec had oldest-top; amended for consistency with TOKEN-LOG/CHANGELOG.) **JOURNAL write cadence — the unit is the shipped merge** (operator ruling 2026-08-03): one entry per merged-and-pushed unit, not per session and not per commit. Mid-arc churn *within* one unit is the anti-pattern; a wrap-only entry across a multi-merge session is the opposite error and leaves shipped commits unanchored. Full statement and both failure modes: LESSONS 2026-08-03 "journal at wrap, not mid-arc".
- **Append-only, newest-first (prepend):** LESSONS — new entries at the top of the Entries section, per the file's own header and ADR-29. Rationale: append-only preserves "what we learned when"; newest-first optimizes the scan, same as the logs above. (Corrected 2026-07-30 — this line read "oldest top" until the intake #18 A10 / RM-1 sweep, which fixed `HANDOFF_PROCESS.md` §15 and missed this sibling; the file itself has been newest-first throughout.)
- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT. Rationale: not logs; current state matters more than history.
- **Immutable (dated):** ADRs, transcripts, handoffs, audits, research. Rationale: point-in-time records; supersession via new file or in-file marker.

**Generator determinism is a property of the input set, not of the code.** A generator that walks the filesystem rather than the *tracked* set emits different bytes per checkout, so its regen-and-diff gate is armed everywhere and satisfiable only on the machine that last regenerated — it stops describing committed state, which is the thing it claims to check. Three instances, one of them live and unfixed when this was written: an untracked `.claude/commands/*.md` rendered as a row in the organ index; `--probe-user-level` reporting four present session hooks as *"declared but absent"* because it inventoried files; and `scripts/gen_audit_index.py:57` reading `audits_dir.glob("*.md")` unfiltered, where a sibling session's untracked audit rendered as an index row and moved the count 487 → 489. The repair that generalizes: route every collector through `git ls-files`, pinned by a test that builds a real git repo containing an untracked file of the collected type.

**Loud degradation is per-SOURCE, not per-class.** An absent source is invisible whenever another source still populates the same rendered class — the section renders, the class is non-empty, and nothing reports that one contributor vanished. Witnessed when a disappeared `.claude/agents/` returned `[]` and the L0 registry kept the class populated. The instructive part is the test history: a class-level *"(no organ in this class)"* assertion was **replaced** rather than kept, and replacing it is what made the defect look covered. An assertion per source, retained alongside the class-level one, is what makes the absence audible.

---

## Ch7. Review postures
<!-- scope: meta -->

Four review postures distilled from the 2026-05-19 posture-audit (`docs/audits/2026-05-19-dev-knowledge-posture-audit.md`, findings H3/H4/T1/T2). Governance-doc and ADR craft — apply when editing, relocating, or deleting canonical content, or when deciding whether a one-off decision earns an ADR. Wording sourced **verbatim** from the audit; codified per #34.

- **Stable-end-state** (audit H3) — *"Governance docs phrased as stable end-state; transient status lives in JOURNAL."* Governance docs describe end-states; transient status (what's done / pending) lives in JOURNAL or a rollout-tracker, never as time-bound clauses that read stale later.
- **Verify-destination** (audit H4) — *"When relocating or dropping content, Plan Mode confirms destination genuinely covers it."* Before deleting a pointer or relocating a section, confirm the destination already carries each sub-part — verify, don't assume.
- **No-delete-canonical-dup** (audit T1) — single-source-of-truth (P1) overrides never-delete (P7) **only** when the deletion targets a *"duplicate of canonical content"* preserved elsewhere. The no-delete invariant has an explicit exception for duplicates of canonical content; deleting a unique copy is still forbidden.
- **ADR-with-N=1** (audit T2) — *"A single architectural CHOICE with no prior precedent can be an ADR-with-N=1 because the choice itself is the record, not a pattern claim."* The N≥2 bar blocks PATTERN extraction without evidence; it does not block recording a singular decision whose record IS the choice.

- **Single-witness verification insufficiency (the PATH-regression class)** — *"it works here"* establishes that it works **there**. The failure surfaces on the first machine that was not the witness, which is usually the machine that runs the work rather than the one that authored it. Four failures across one saga made the point: the dispatch helper's root causes were measured layer by layer on a machine that had not been the witness. The recorded sibling is the relic `core.hooksPath` disarm (n=2), where a repo looked gated and was not. A second witness — another machine, a clean clone, a container — is the cheap discriminator, and its absence is worth stating rather than assuming away. (The fleet-attestation question this raises is owned by intake #32 and is not re-derived here.)
- **A refuted finding is kept, not deleted** — a review tally that COUNTS a refuted finding reports a defect that does not exist; a tally that ERASES the finding hides that the loop produced a false positive. Both errors live in the same place, so the tally **excludes** the refuted finding and the body **retains** it, with the refutation and its commands recorded alongside. Worked examples: a `Tally: 0/0/0/0` artifact carrying its pass-1 HIGH in full together with the two commands that refuted it, and a `Tally: 0/16/0/0` artifact whose two DECLINED findings carry reasons and are pinned by tests. A checker cannot tell a refuted finding from an unfixed one, which is why this is a drafting posture rather than a gate.
- **Citation convention — cite by anchor; carry the locator or mark the paraphrase** (adopted 2026-08-10 as ruling 3b-4, advisory) — a claim about repo state cites something a reader can resolve: a heading or other stable anchor, a SHA, or a command with its output. Line numbers are recorded as *the measurement taken on a date*, not as the anchor, because a line range rots inside its own file while the claim still reads as current — which is how a row came to cite `:517-518` for a clause that had moved to `:775-776` and was restated at `:938-939`. The rule earns a check on n=2 evidence; it had already produced two citation defects in the window before it landed anywhere. Pairs with *Architect epistemic discipline: explicit verification markers* (Part II), whose locator-or-paraphrase half covers claims arriving from outside the repo.

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

**Worktree side-effect rule — refuse an undeclared mid-session order (operator-ruled 2026-07-18,
[#353]).** A session must **REFUSE to act on an externally-authored order** — a prompt injecting new
work mid-session — unless **either** (a) the order **names a worktree for its side effects**, **or**
(b) **the tree is clean**. Dirty tree + no worktree declaration = **STOP and ask**, do not start.

*Why:* the ARC-4 session inherited a pre-existing untracked bundle mid-session; the
isolate-to-worktree / no-dirty-tree-action discipline lived in prose, not in a gate — five recovery
episodes since 2026-06-05, each fixed **after** the fact, **none prevented**.

*Honest limit:* this is **prose discipline today, not a mechanism.** `session_end_backpressure.py` is
Stop-only (wrong lifecycle phase) and no boot-time organ exists — the boot-snapshot + PreToolUse
refusal is [#353]'s open build. Until it lands, the rule is upheld by the executor, so apply it
deliberately at every mid-session order.

**A claim of green names WHERE it is green (transcribed 2026-07-31, [#446] window).** Branch-green
is not done — **done is post-merge green on `main`.** A gate set that passes on a feature branch
proves the arc is internally consistent; it does not prove the arc composes with everything that
landed on `main` while the branch was open. The two states are routinely different (a merge can
surface a WARN neither parent carried), so "ship-gate GREEN" is an incomplete sentence: say
**GREEN-on-branch** or **GREEN-on-main** and mean it. Report the weaker one when both are known;
a branch-green reading does not stand in for the post-merge verification a done-when asks for.

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
- **(b) Each committing session in its OWN worktree.** **One checkout = one committing session.** A "single commit at the end" still counts as a committing session — there is no "I'll only commit once" exception. (Why: a no-worktree session's lone commit can land on a *concurrent* session's branch, sweep its staged file, and mis-root the branch — witnessed twice, LESSONS 2026-06-07 / 2026-06-05.)

**A long gate/suite run and a commit are mutually exclusive IN THE SAME TREE (witnessed 2026-07-31, the [#382] W3 boundary — JOURNAL entry (p)).** Distinct from the session-concurrency rule above, and the reason it needs its own line: this fires inside a **single** session, where the two shapes above both look satisfied. A background full-suite run raced a JOURNAL commit in the same checkout and produced a **phantom failure** — `test_check_selects_correctly_under_inherited_git_dir`, a test that spawns git, observing the tree mid-swap while pre-commit's stash/restore held it; the clean rerun PASSED with no code change. Same family as the pre-commit-stash and `GIT_DIR` gotchas, but a separate rule: **sequence the suite and the commit, or run the suite in a worktree.** Why it earns a rule rather than a footnote: a phantom RED is more expensive than a slow lane, because it invites a disposition — or a "fix" — against a defect that never existed.

**Integration authority — operator authorizes, CC-primary executes (2026-07-16 ruling).** Merge execution is delegated to the CC-primary session: on the operator's explicit **GO** (one authorization per integration), CC performs the `--no-ff` merge to `main` **from the primary checkout**, verifies (that repo's suite + — for the hub — `ship-gate` green; any failure STOPS the chain and surfaces), then completes teardown — a plain merged branch is deleted directly; a worktree branch requires the worktree to be **removed first** (a checked-out branch cannot be `-d` deleted), per the worked example below. The operator is the **authorization gate, not the executor**. Invariants unchanged: one merge to `main` at a time; integration only from the primary checkout; parallel/worktree sessions still **commit-and-STOP and never self-merge** — they hand their branch to the primary for the authorized merge.

**Recorded precedent — an operator-DIRECTED shortened sequence is not a violation (2026-07-29).** At
`14bcb1c4` the operator ordered the night-prep branch merged **ahead of** local verification, wanting to
review the night audit from `origin` rather than off a branch. The sequence therefore ran shortened —
merge first, verify after — and the verification leg completed post-hoc at `3205db7b` with `main` GREEN.
Recorded as a sanctioned **operator-directed serial-gate act**, not a breach of the verify-then-teardown
ordering above: the operator holds the authorization gate, so ordering its steps is his to do, and the
verification leg stays **owed rather than optional**. What makes the precedent sanctioned is that the
post-hoc leg actually ran and its verdict is on the record; the unshortened default stands for every
integration the operator has not explicitly re-ordered.

**MERGE IS ATOMIC (standing operator rule, established after three repeats — 2026-07-27).** Stated verbatim, and binding wherever a merge happens:

> merge `--no-ff` + push + delete the source branch are ONE operation. A branch merged into main and pushed is deleted in the same step, without separate operator authorization. Exceptions exist only by EXPLICIT PROTECTION (currently `claude/conformance-*`); silence is not protection. A merged branch left alive is a defect, not a pending decision.

This sharpens the teardown clause above from *a thing CC does* into *a thing CC may not defer*: do not ask whether to delete a branch you just merged and pushed — the delete is part of the merge already authorized. `--merged` is still verified first and nothing is force-deleted; the rule removes the **authorization round-trip**, not the safety check. The operative copy CC self-loads is `.claude/rules/git-discipline.md`; this is the doctrinal home. (Established after three repeats of the same operator correction; the mechanical backstop is a proposal, not built — see the note in that rule file's arc.)

**Hub→consumer writes — the only sanctioned shape (RULING-W; ADR-36/41 amendments 2026-07-18).** The
hub **MAY and SHOULD** write into a consumer repo for methodology/cleanup work — the read-only
"don't-touch-consumers" guardrail is **narrowed, not revoked**. The **only sanctioned write shape** is
**consumer worktree/branch → report**: the hub creates a **separate git worktree/branch inside the
consumer**, makes its edits there, then **reports**. Hard bounds:

- **Never a direct push into a live consumer checkout** — no unmediated edit of the consumer's
  working tree and no fast-forward onto its `main`.
- **Re-witness the consumer live before any edit** — never act from a stale ledger of the consumer's
  HEAD. The re-witness is the **unfiltered live-session check** below, and it runs *first*, before
  the branch — not after the edits are staged.
- **Mechanism before act:** the FIRST step of any consumer leg is codifying the mechanism (that
  amendment is landed — ADR-36 qualifies §Q5, ADR-41 narrows the guardrail).
- The write is **agent-mediated, not tooled**: `audit.py` stays read-only w.r.t. child repos and **no
  orchestration script is added to Layer 2** (ADR-28 preserved). §Q5 now reads: *the tool never
  touches child repos; a hub session may, only via this shape.*

**The unfiltered live-session check — run BEFORE any consumer write (proven 2026-07-21).** A live
session in the target repo can swap `HEAD` mid-command, so writing under one corrupts both lanes;
this is the class that put a stray commit on hub `main` on 2026-07-20 and the class the `assets/`
lane's check **blocked** the next day. The check is *checkable*, not a feeling:

- **Transcript-cwd is authoritative.** Answer *"is a session live in repo X?"* from
  `~/.claude/projects/<mangled-cwd>/*.jsonl` plus a `"cwd"` grep — worktrees mangle to their own
  distinct dirs, so each is answered separately. **Process inspection cannot answer it**:
  `Win32_Process` carries no cwd and the parent chain resolves only to `cmd`/`pwsh`.
- **Stopped-growing ≠ closed.** A stalled transcript mtime means *idle-at-prompt*, not gone;
  corroborate against the live `claude.exe` count before concluding a repo is free.
- **Unfiltered means unfiltered.** The check covers every session, not the subset you expect to
  matter. A filtered check is the *"green that means nothing"* class — it reports safe by
  construction, which is worse than not checking.
- **Never branch, commit, or merge under a live session.** If one is live: STOP and report. Do not
  wait it out silently, and do not kill it — a worktree dir held by a live session is a session-
  lifecycle matter, not a git one ("Lifecycle" below).

**Consumer-leg merge delegation (the composite).** The hub session **never merges its own consumer
branch**. The **consumer's own merge discipline governs integration** — operator **GO** + `--no-ff`,
same as any change arc — so the consumer leg runs **worktree off the consumer's live `main` → that
repo's gates green + a `gpt-5.6-terra` codex doc/code-lane review pre-merge → commit-and-STOP →
report**. Integration then follows the **consumer's own** authority split (the rule above, applied in
that repo): operator **GO**, and the merge executed from **that repo's primary checkout** — never by
the hub session, which is the *author* and never the integrator. A **pre-existing,
orthogonal** gate failure in the consumer (owned by that repo's own session) is **reported, not
silently fixed and not quietly bypassed**; a failure **caused by your diff** is fixed, never bypassed.

Shape (b) runs on **CC-native managed worktrees** (#107) — the low-friction path. The old *sibling*
worktree naming (`<repo>-parallel` / `<repo>-wt-*`) is **superseded** by the in-repo native location
below; sibling dirs spawned the `.dev-knowledge-*` rule-9 orphans (LESSONS 2026-06-02), so do not
create them anymore.

**Lifecycle (same-repo only):** a worktree is **per-goal scratch, not a persistent
checkout** — *provision → use → ephemeral teardown*. Create one for a single goal, work it on
its own branch, and remove it the moment that branch merges. It must not linger between goals.

**0 — Launch decision: one strong prompt on primary is the DEFAULT; worktrees are the exception ([#441])**

*Ruling record — ADOPTED (operator, 2026-07-29).* Drafted on the 2026-07-28→29 night-prep branch and
carried unratified through that merge; ruled ADOPTED at the following morning's review, so this block
is live doctrine. It **replaces** the prior three-check "0 — Decide: should I parallelize?" launch test
so the corpus carries one launch test (the mapping is recorded below). Ruling evidence: the shipped
2026-07-28 window cited under *Evidence*, plus the operator's live endorsement of the fat-prompt
default across the 2026-07-28→29 window itself. One item was resolved at the intake #18 ratification (2026-07-30) — condition 2 now cites the §8 allocation convention.

**The default (operator + outgoing-seat ruling 2026-07-28):** one strong, self-contained
prompt on the **primary** checkout. Parallelism lives **inside** the session — the
orchestrator (Opus) fans out in-session subagents (Sonnet probes, Haiku read-only
fan-out) and the Codex lane runs in the background — with **every git mutation serial in
the main thread**. A second *committing session* is not the default shape; it is the
exception below, and it costs a worktree + a serial integration pass.

**The four-condition worktree test — launch a parallel committing session only when ALL
FOUR are YES:**

1. **Two substantial BUILD arcs?** Two genuinely independent build efforts — not one goal
   split in two ("finish the rest of X" is one goal), not a build plus a doc ride-along,
   and not tiny disjoint edits (a file or two each) that integrate slower than they run.
2. **Zero shared gate-forced surfaces — or a contract pre-resolves them?** Surfaces a
   gate forces both lanes through (JOURNAL entries, BACKLOG/`tasks/` rows + regen,
   generated indexes) either aren't shared, or a written contract pre-resolves the
   contention (a dispatch-pre-assigned JOURNAL-letter contract (per the §8 allocation
   convention), disjoint rows, a named `tasks/` regen
   owner). Two lanes editing the *same substantive file* is always a NO.
3. **Wall-clock matters?** Real calendar pressure that serial execution would miss —
   parallelism for its own sake is not a reason.
4. **Operator takes the serial gate?** The operator affirmatively wants two terminals AND
   accepts serial-gate duty (authorizing integrations one at a time from the primary).

**One NO = fat prompt.** No judgment margin, no partial credit: a single failed condition
routes the work into one self-contained prompt on primary.

*Evidence (the prove-then-codify basis):* the 2026-07-28 window is the shipped run of the
default — serial fat prompts (JOURNAL (k)–(n)) with in-session fan-out + Codex background,
zero collisions — against the 07-27/28 JOURNAL letter collisions (n=3) + leftovers from
parallel lanes, the 07-21 operator preference, the 07-23 complaint, and exactly one clean
parallel success (adr∥ratchet — a pair that passes the four conditions).

*Mapping from the superseded three-check test:* "disjoint substantive files" → condition 2;
"two distinct goals" + "more than a single-file edit per stream" → condition 1. Conditions
3–4 are new — the ruled additions. Everything below this block (canonical-safe-pair,
shared-surface handling, provisioning, seeding, integration authority, teardown) governs
**HOW** a sanctioned parallel session runs; this block alone governs **WHETHER** one
launches. The **content** of a sanctioned multi-agent mandate is §2's "Multi-agent / fan-out
prompt checklist" + the HANDOFF_PROCESS §13 destination contract (intake #18 A4) — WHETHER is
ruled here, WHAT the mandate declares is ruled there.

**Canonical safe pair: one code item ∥ one doc item.** Disjoint files by construction. Review
contention is at most one-sided: the **doc** stream never needs Codex; only the **code** stream
*might* — and only if it trips the Codex bar (3+ files or safety-critical, per ADR-54). Reach for
this shape first.

**Shared canonical files are handled, not parallelized** (refines §3's serialize rule):
- **BACKLOG: removal travels the closure loop, not the branch.** Don't have each branch retire its
  own row; leave the removal to the Tier-1 closure loop (`/review-closures`) after merge, so two
  branches never contend on the same deletion — on the hub that removal is a `tasks/` retirement
  (manifest node out + regen), on an unflipped consumer the direct line removal. The edits §3
  serializes are queue **adds / grooming** (and id allocation at write-time) — in `tasks/` on the
  hub — not removals.
- **JOURNAL: the conflict is trivial.** Each branch prepends its own newest-first entry; a merge
  conflict is just two top-of-file prepends — resolve by keeping both in timestamp order. JOURNAL
  is therefore not a real serialization blocker.
  **The letter-allocation convention (intake #18 A5/U3, ratified 2026-07-30):** JOURNAL letters
  are assigned **at integration**, by the primary's single writer — **lanes never allocate.** One
  scoped exception: inside a sanctioned worktree pair (the Ch8 four-condition test passed), the
  dispatch MAY pre-assign letters as its condition-2 contention contract; absent that written
  dispatch contract, assign-at-integration governs.
- **Operator is the serial gate.** Parallel branches return to the operator, who `/ship`s them **one
  at a time from the primary** — branches never self-merge in arbitrary order.

**1 — When a worktree is needed**

- **Different repos in parallel: already safe.** Separate `.git/` directories isolate each
  session completely — no worktree setup needed. Cross-repo sequential orchestration (one
  session `cd`-ing into multiple repos) is also safe for the same reason.
- **Same repo in parallel: REQUIRES a worktree.** One working tree has one HEAD + one index;
  two+ committing sessions on a shared checkout collide — a commit in one sweeps the other's
  staged file and lands on the wrong branch (LESSONS 2026-06-07; separate worktrees = zero sweep).

**2 — Provision (native-primary)**

**Recommended START — Primary = stream A, worktree = stream B** (the from-scratch recipe for
splitting one session into two same-repo streams):
1. **Pre-flight:** `git worktree list` shows only the primary; working tree clean.
2. **Stream A** stays in the **primary** checkout, on its own `feat/<A>` branch — the primary is
   also the integration + serial gate (step 4).
3. **Stream B:** `claude --worktree <B>` → a session inside `.claude/worktrees/<B>` on branch
   `worktree-<B>` (then seed `ecosystem/*/state.yaml` from the primary so the audit-health gate
   passes — §2a; do not rely on auto-seed, n=3 — see below).
4. **Integrate from the primary on `main`, one at a time:** `/ship` stream A; then
   `git merge --no-ff worktree-<B>` + `git push`; then tear down B (the §4 three-command
   round-trip) and verify no leftovers.

**The command the architect hands the operator is `claude --worktree <B>` (new terminal) or
`EnterWorktree` (mid-session) — NEVER a raw sibling `git worktree add ../dev-knowledge-<B>`.** The
sibling-dir recipe is superseded (above): it is the documented source of the `.dev-knowledge-*`
rule-9 orphans. Native keeps the worktree gitignored under `.claude/worktrees/` (but seed
`ecosystem/*/state.yaml` from the primary regardless — neither path reliably auto-seeds, n=3).

The bullets below are the mechanism this recipe rests on.

- **New parallel session:** `claude --worktree <name>` (alias `-w`) starts a session already
  inside a fresh worktree. **Mid-session:** the `EnterWorktree` tool switches the *current*
  session into one (`ExitWorktree` returns). Both create **`.claude/worktrees/<name>/` on
  branch `worktree-<name>`** (verified). Base ref = `worktree.baseRef` setting: `fresh`
  (default → `origin/<default-branch>`) or `head` (current local HEAD).
- **Seed `ecosystem/*/state.yaml` from the primary — treat a fresh worktree as unseeded by
  default; do NOT delete `.worktreeinclude`.** A fresh worktree is a clean checkout and OMITS
  gitignored runtime state — including `ecosystem/*/state.yaml` (ADR-80 high-churn pointers).
  Without them the `audit-health` pre-commit gate sees `repos registered (none)` → `health:
  DEGRADED` and **blocks every commit** — a fresh committing worktree is dead on arrival. The
  committed `.worktreeinclude` lists the 5 `state.yaml` (incl. the dot-prefixed `.dev-knowledge`
  hub dir) for the native create to copy in, **but neither native nor raw `git worktree add`
  reliably auto-seeds** (n=3 witnessed misses — LESSONS 2026-06-19; the "native seeds for you"
  claim is refuted), so seed by hand from the primary (§2a) before the first commit and do not
  rely on the auto-copy.
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

**2a — Cold-start specifics** (the four details a fresh operator needs — terminal anchor, slug,
manual seed, pwd-confirm)

- **Where you launch it (terminal anchor).** `claude --worktree <name>` (alias `-w`) is run from
  a **fresh PowerShell terminal at the `<repo>` root** — a cold-start session that begins life
  *inside* the new worktree. To split an **already-running** session instead, use the
  `EnterWorktree` tool mid-session (`ExitWorktree` returns to the primary). Either path lands you
  in `.claude/worktrees/<name>/` on branch `worktree-<name>` (verified on this machine/CC version).
- **`<name>` slug convention.** Name the worktree **`<issue#>-<kebab-slug>`** — e.g.
  `156-taskgraph` → dir `.claude/worktrees/156-taskgraph/`, branch `worktree-156-taskgraph`. With
  no backing issue, use a bare `<kebab-purpose>` slug (e.g. `changelog-sync`). This formalizes the
  de-facto `156-taskgraph` example as the convention — it is not a new scheme.
- **Manual-seed commands (any fresh worktree — n=3).** A fresh worktree starts WITHOUT the
  gitignored `ecosystem/*/state.yaml` that `.worktreeinclude` declares, so its first commit is
  blocked by the `audit-health` gate (`repos registered (none)` → `health: DEGRADED`). Native
  *may* copy them but n=3 says don't rely on it (LESSONS 2026-06-19), so seed by hand, copying
  exactly what `.worktreeinclude` lists. From the `<repo>` root in PowerShell:

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

  (`.worktreeinclude` lists the 5 `ecosystem/*/state.yaml` — one per `ecosystem/` child plus the
  dot-prefixed hub dir.)
- **pwd-confirm before working (ADR-61 rule 5, re-carried into the manual path).** Before any work
  in a hand-driven worktree, verify you are actually in it — `Get-Location` (`pwd`) must resolve to
  `…/.claude/worktrees/<name>`, NOT the primary root. A commit fired from the wrong cwd lands on the
  wrong branch (the shared-index sweep this whole discipline exists to prevent).

**Worked example end-to-end** (copy, don't reconstruct):

```
# 1. fresh PowerShell terminal at the repo root, cold start:
claude --worktree 156-taskgraph
#    -> session opens inside .claude/worktrees/156-taskgraph/ on branch worktree-156-taskgraph
# 1b. seed ecosystem/*/state.yaml from the primary (see 2a) so audit-health passes -- n=3: don't rely on auto-seed
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

Windows caveat: if VS Code (or any IDE with a recursive file watcher) has the repo open,
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
  *Q2 (`protocols/STANDING_RULINGS.md`): the primary checkout is **seat-arc-only** — a helper
  task runs zero git operations in it, on the evidence of two witnessed HEAD-swap incidents.*
- **Merge serialization — why two concurrent merges to `main` can't tangle (#200).** Not a
  lock/mutex: the concurrent-merge race is already serialized by **git itself**, plus the FF-block:
  - **`index.lock`** — two simultaneous `git merge` commands can't both proceed; the second
    fails `Unable to create '.git/index.lock': File exists. Another git process seems to be running`.
  - **`MERGE_HEAD` refusal** — a second `git merge` while one is in-progress is refused by git
    (`Merging is not possible because you have unmerged files` / `You have not concluded your merge`).
  - **Push-rejection = `main` moved = re-integrate.** A push to a `main` that another clone
    already advanced is rejected `! [rejected] … (fetch first)`; you `git pull` and re-merge.
    This is git serializing the integration point across clones — lean on it, don't rebuild it.
  - **The FF-block** (`scripts/block_ff_push.py`, pre-push, hub-only) refuses any push adding a
    non-merge commit to main's first-parent spine (core-invariant #5). <!-- rule: governance-no-ff -->
    The `--no-ff`-merge norm (every change is a branch → `--no-ff` merge; never a direct or FF
    commit on `main`'s spine) is the rule this enforces, detected post-hoc by `validate_no_ff.py`
    (the `no_ff_merges` WARN) and prevented at push by `block_ff_push.py`.
  - **A worktree→`main` merge is git-structurally prevented** — a linked worktree cannot
    `git checkout main` (it's already checked out in the primary), so integration *always*
    funnels through the single primary checkout, where the natives above apply.
  - **Honest limit (not gate-catchable):** a *primary*-checkout self-merge is byte-identical to a
    legitimate operator merge — no git signal separates them, so **no hook can distinguish them.**
    Held by the commit-and-STOP / integrate-from-primary discipline (operator is the serial gate)
    + #107 worktree isolation, not by machinery (witnessed in `tests/test_merge_serialization.py`).
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
  (restores cwd first; removes a changeless worktree cleanly); these manual steps are the raw-path case. **`remove` is NOT idempotent — if a first remove is
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

### Tree orchestration — architect-root + epic-chat lanes (ADR-97)
<!-- scope: meta -->

**Extends the worktree discipline above from CC sessions to whole browser lanes** (additive —
every rule above still holds; formalizes the 2026-07-04 lived precedent). Handoff contracts:
HANDOFF_PROCESS §14 (§14a EPIC handoff / §14b EPIC RETURN). Decision record: ADR-97.

**The tree.** **Root** = the one architect chat: owns ADRs, backlog structure, epic
decomposition, the parallelism ruling, plan review at epic level, ALL merges to main (serial,
`--no-ff`), closure declaration, and worktree lifecycle. **Branch** = epic chats — one browser
chat + one root-provisioned worktree per epic (branch `epic/<slug>`), each owning one epic
end-to-end (story decomposition, CC delegations, review, own-epic BACKLOG checkboxes); they
commit-and-STOP. **Leaf** = user stories, executed by CC sessions serialized on the epic branch
(commit-per-story). Worktree per EPIC, not per story — a genuinely disjoint large story gets a
sub-worktree only by architect escalation, never self-provisioned.

**The file-boundary mechanism.** Each epic lane's §14a handoff declares the explicit file/dir
set it may touch — the parallelism ruling made mechanical. Two concurrent epics MUST have
disjoint boundaries (adjudicated by the root **at spawn, not discovered at merge**); a needed
file outside the boundary = escalate, don't touch. This generalizes "disjoint substantive
files?" (step 0 above) from a self-check into a root-issued contract.

**Root-only merges.** Only the root merges to main, one merge at a time — the never-self-merge
rule (step 4 above) generalized from CC sessions to whole lanes. An epic lane never merges,
never writes ADRs, never restructures the backlog, never provisions or tears down worktrees.
Structural BACKLOG changes travel in the §14b EPIC RETURN and are applied by the root at
integration (lanes tick checkboxes only inside their own epic block); JOURNAL entries merge
chronologically, both kept (the trivial-conflict rule above).

**The cap: 2–3 concurrent epic lanes.** The root's review + serial-merge bandwidth is the
deliberate bottleneck — more lanes queue at the gate, they don't add throughput. Authority does
not descend; every lane boots from a generated §14a handoff and closes with a §14b return.

**Scope, declared 2026-08-06 — this cap counts EPIC lanes, not work lanes.** An ADR-97 epic lane
runs its own chat with a §14a boot and a §14b return. A *work lane* is a different object: one
footprint-disjoint slice of a batch, pasted into a session as a frozen contract.
`templates/prompt-template.md` (v1.14) carries a separate **~10** ceiling for work lanes (intake
#25 `AMENDMENT 2026-08-05-c` c1), bounded by file-disjointness and integration capacity rather
than by integrator bandwidth. Different objects, different bottlenecks, both live — ~10 work
lanes can sit inside far fewer epic lanes, and the two figures are deliberately **not** reconciled
to one number. **This PLAYBOOK text wins on epic-lane criteria**; the card is the point-of-use
authority for work-lane prompts only. Declared here and in the card together, repairing the
undeclared scope collision the FR-7 v1.6 diff left behind.

**Execution MODE is part of the contract (v5.6).** Every §14a handoff — and every subsequent
architect prompt into a lane — declares the execution mode (plan / plan-then-auto /
auto-accept) with its basis; **L-sized epic stories default plan-first** (HANDOFF_PROCESS §14a
item 7; the 2026-07-06 plan-gate corrective — a lane inherits no mode from a prior prompt).

**Naming (ADR-98):** *developer* is the **mode** an epic lane's chat runs under (the additive
alias of epic mode); the *epic lane* is the **unit of work**. Defined once in Part II §2 "The
intake pipeline" — cross-referenced, never synonyms.
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

**The failure this prevents:** sibling worktree dirs deregistered from git but never removed from
disk linger as orphans (the `.dev-knowledge-*` recurrence — LESSONS 2026-06-02; one was
process-locked, *exactly* when a `remove` silently no-ops and must be re-checked). An orphan is
invisible to a presence-checking audit — it verifies that required files *exist* and structurally
cannot detect a file that exists but should not (the 2026-05-17 decommissioning-gap LESSON). So the
round-trip diff is an explicit process step at run end, not something a later scan catches.

**Lightweight check, not heavy tooling.** The three commands above *are* the check — a process
step, not a script (Layer 2 never executes — critical rule #4). Run them at the end of any
worktree/scratch-creating run. The read-only `audit.py` assertion that no stray `<repo>-*` sibling
exists is now **built** — `check_no_sibling_orphans` (#11), keyed on `git worktree list`
registration so a *live* registered worktree passes and only an unregistered orphan fails; it runs
in the `audit-health` pre-commit gate, so an orphan blocks the next commit until removed. The
process step above remains the first line of defence (catch it at teardown); the check is the
backstop that catches what the manual teardown missed. (Recurrence cleaned 2026-06-02 — see LESSONS.)

### The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110)
<!-- scope: meta -->

**What this section is.** The *how* of a sanctioned parallel run, encoded so that a seat which
has seen no prior conversation can run one from the repo alone. **The four-condition test above
([#441]) governs WHETHER parallel work launches; this section governs HOW a batch runs once it
has.** One launch test, one execution protocol — the two do not overlap, and neither restates
the other. Decision record: ADR-110 (§1 the artifact set, §2 lane-count parameterization, §3 the
refuse-to-finish close-out); intake #26 is its pipeline input.

**The shape.** ONE plan → **N file-disjoint lanes** → ONE serial integrator. The plan is authored
once, before any lane boots; each lane receives one frozen contract naming its own footprint; the
integrator merges the lanes back one at a time from the primary checkout. Dependency-chained work
stays **inside a single lane** — a lane is the unit that can carry order, so splitting a chain
across two lanes trades a cheap serial step for a merge-order constraint the integrator has no
way to express. Serialize-groups bind on witnessed file footprints within a batch: label
co-membership alone does not serialize lanes whose witnessed footprints are disjoint
(`protocols/STANDING_RULINGS.md` G2, ratified 2026-08-08).

**Parameterized by N — drilled at 3, designed for 4–10.** Batch 1 runs three lanes because three
is enough to exercise the machinery; every artifact is written for N. Provisioning, the board
view, and the integrator queue read the lane list rather than assuming a width of three, so batch
2 widens by changing the list. ADR-110 §2 records why staging won: width ahead of a proven
integrator buys risk rather than speed. The ~10 work-lane ceiling in `templates/prompt-template.md`
and the 2–3 concurrent *epic* lane cap above are **different axes**, deliberately unreconciled —
see the scope declaration under "Tree orchestration" above.

**Per-lane requirements — the five a lane contract carries.**

1. **A frozen contract.** The lane's authoritative surface is the contract it booted with.
   Load-bearing content arriving in a later message is indistinguishable from an injected
   instruction — the two arrive on the same channel wearing the same shape
   (`protocols/STANDING_RULINGS.md` D2) — so a correction re-enters as a *new contract* rather
   than as a mid-flight addition.
2. **A V-2 decision budget.** A lane escalates on three classes only: **(a)** curated-baseline
   touches, **(b)** genuine rule-vs-ruling conflicts, **(c)** fork classes with no standing
   ruling. Everything else is decided per contract defaults and **reported in the end packet**
   (STANDING_RULINGS "The decision budget").
3. **`uv run --locked` on every test invocation.** A bare `pytest` inside a worktree lane
   inherits `VIRTUAL_ENV` from the primary tree, imports the PRIMARY checkout's source, and
   reports green about code the lane did not touch — silently (STANDING_RULINGS D4; ADR-106 for
   the pin). The wrapper is the mechanism that makes the environment follow the checkout.
4. **Commit-and-STOP, with `git stash list` empty at STOP.** A lane commits its work and hands
   the branch back; integration is the integrator's act, from the primary checkout — the
   no-self-merge rule above, applied at batch scale. A mid-work stash is popped or dropped by
   the lane that made it, before it stops. The reason is structural rather than tidiness
   (batch-1 F4): `refs/stash` lives in the **common** git directory, not in the worktree's
   private ref space, so a stash pushed inside a lane belongs to the whole repository. It
   survives `git worktree remove`, `git worktree prune`, the branch delete, and every one of
   the refuse-to-finish items below, all of which are worktree- or branch-shaped. Work left
   there is absent from the tree, absent from the handed-back branch, and findable only by
   someone who thinks to look — and the lane is the only seat that still knows what it was.
5. **A worktree name paired 1:1 with its prompt file.** One lane = one contract file = one
   worktree = one branch, so an open worktree resolves to the contract that created it and an
   orphan is attributable at a glance. Naming grammar + prefix enum:
   `scripts/validate_branch_naming.py`.

**Artifact paths in a contract are DERIVED from the ADR-101 enum, not composed freehand
(batch-1 F3).** A contract that tells a lane to write `docs/audits/<date>-<slug>.md` has named a
path the `validate-hermetization` Rule B gate REFUSES: the grammar wants an enum class token
(`-technical-` / `-codex-` / `-verification-` / …) that a freehand slug omits. Batch 1 produced
two such filenames in one batch, from the same authoring surface, and both lanes spent decision
budget renaming to conform — one escalating it, which is the correct lane behaviour and also the
proof that the cost lands in the wrong place. The authoring fix is to read the class enum out of
ADR-101 §R3/R4 (or run `python scripts/validate_hermetization.py` over the intended name) while
writing the plan, so the gate confirms a name the contract already got right. The general shape:
**a contract that cites a path a gate governs is checkable at authoring time, and checking it
there is cheaper than any lane discovering it.** `/preflight` is the built organ for this; a
batch plan is exactly the class of document it exists to verify.

**The integrator's refuse-to-finish checklist.** A batch closes when all **five** hold; an open
item leaves the batch open (ADR-110 §3). The load-bearing property is that the checklist is
*mechanical* — a close-out a reader can skim past and still declare done is the state it replaces.
(Item 5 joined 2026-08-07 on batch-1 F4; ADR-110 §3 enumerates four, so the fifth rides as a
recorded addition here until the ADR is amended.)

- **Every lane branch merged-or-explicitly-abandoned.** "Explicitly abandoned" is a recorded
  disposition; a lane branch with no verdict leaves the checklist open.
- **Full suite run once on the merged result.** Per-lane greens are evidence about each lane in
  isolation; the merged tree is a state no lane tested. Which suite a lane runs in-lane and which
  one lands here is Ch5 "Tiered suite — targeted in-lane, one full suite at integration".
- **`git worktree list` == primary only.** The batch-scale form of the no-leftovers round-trip
  stated immediately above.
- **Manifest/packet archived — TWO halves, one at each end (batch-1 packet §8).** The **batch
  manifest is committed at DISPATCH**, before any lane boots: the lane contracts *are* the plan,
  and a plan that lives only in chat prompts leaves the batch reconstructable from its outcome
  but not from its intent. **Since the ADR-110 amendment 2026-08-07 the manifest is also
  load-bearing at the GATE**: it declares the open batch that grants the
  declared-integration-arc exemption, retiring `SKIP=audit-health` on intermediate merges. Two
  frontmatter fields carry that — `status: open` and `closed_by: <the packet path>` — and the
  exemption ends by itself when that packet lands, because `docs/audits/` is immutable and a
  mutable `status:` flag would be no expiry at all.
  The **end-of-batch packet** lands at close. Batch 1 archived the
  second half only — contracts were delivered as prompts — so this item passed on a technicality
  while half its evidence had already evaporated. A committed manifest is also what makes the F3
  path check above possible at authoring time, and what lets a successor answer "was this lane's
  footprint respected?" against a frozen contract rather than against memory.
- **`git stash list` is empty (batch-1 F4).** The item the other four structurally cannot cover.
  They read branches and worktrees; `refs/stash` is neither — it lives in the common git dir — so
  a lane's abandoned stash passes all four and the batch closes looking clean while the work sits
  where nothing points at it. One command, one line of output. An entry that stays gets a
  recorded disposition like any other leftover, because `git stash list` reports no worktree of
  origin: an integrator cannot tell a lane's forgotten stash from the operator's deliberate one
  by reading it, and guessing is how real work gets dropped.

`/lane-integrate` walks this list mechanically; `/lane-boot` boots one lane against it. (The two
are deliberately *not* named `/batch-*`: ADR-110 §4 records hand-rolled `/batch-*` commands as
rejected, native `/batch` being the substrate, and these two encode lane protocol rather than
orchestration.)

**JOURNAL-rides-the-branch is the anchoring law.** An arc's JOURNAL entry is written **on that
arc's own branch, ahead of the merge** (STANDING_RULINGS B2). The reason is structural rather
than stylistic: the pre-push anchor gate discharges **range-level**, against SHAs the pushed range
*introduces*, and a merge commit cannot name its own hash. A journal-only wrap merge therefore has
nothing to anchor against and is unanchorable by construction — the recovery is a reset, which is
why the ordering is not a preference. **An anchor discharges by APPEND ONLY** (architect ruling
2026-08-07; register `protocols/STANDING_RULINGS.md` B6): a new entry naming the SHA, rather than
an in-place amendment of an entry already committed — the predicate matches a SHA anywhere in the
file, so editing a landed entry discharges the anchor *retroactively* and leaves no trace it once
did not. JOURNAL letters are allocated **at integration** by the
primary's single writer, unless the dispatch pre-assigned them as its contention contract (the
allocation convention above).

**The integrator's branch carries ≥2 commits — substantive work first, JOURNAL last (batch-1
F1b).** `introduced()` for a `--no-ff` merge is the merge plus every commit its branch brought
in, so a branch carrying exactly ONE commit offers the JOURNAL only its own hash to name — which
it cannot, being written before that hash exists. A one-commit integration branch is therefore
unanchorable by the same law one level up, and it is invisible until *after* the integration
merge lands. Every ordinary arc already has the ≥2 shape by accident of how it grows; the
integrator is the one seat whose work is naturally a single commit (carried edits + packet +
JOURNAL, all in one), so it is the one seat that falls in. The split is cheap and mechanical:
**commit 1** carried edits / reconciliations / packet, **commit 2** the JOURNAL entry naming
commit 1. Batch 1 hit this live — the integration merge landed unanchored and surfaced as two
extra suite REDs downstream of one `journal_spine_anchor` FAIL, repaired by a normal two-commit
arc rather than by rewriting unpushed history.

**The integrator's branch is `docs/…`-class, and having no lane prefix is why (batch-1 F2).**
Merging on `main` leaves the session on `main`, so the integrator's own carried-edit / JOURNAL /
packet commits would land direct-to-`main` and breach core-invariant #5. ADR-110 gives the
integrator no prefix of its own deliberately (minting `integrate/` would invent an enum member
the ruling clause reserves), and the consequence is not "no branch" but "an ordinary author-chosen
branch": the convention is **`docs/<batch>-integration`** for the carried-edit arc and
**`docs/<batch>-<repair>`** for any follow-up, merged `--no-ff` from the primary like any other
serial arc. Batch 1 ran `docs/batch-1-integration` and `docs/batch-1-anchor-repair`. The naming
enum classifies these as plain serial-arc branches, which is the intended reading — the
integrator is an author here, not a lane.

**WINDOW = BATCH.** One batch is one window: the seal — handoff bundle, packet, JOURNAL wrap —
fires at true batch boundaries. A mid-batch seal sits outside the rhythm, because it produces a
bundle describing a tree nobody has integrated yet, and the successor then boots against a
manifest the rest of the batch is about to invalidate. Operator directive 2026-08-06; carried
in-repo by intake #27.

**2-touch transport, on both seams.** The interaction budget applies to each seam independently:

- **operator ↔ integration** — **GO** at dispatch, the **end-of-batch packet** at close.
- **operator ↔ lane** — **batched packets**: one round-trip carries every item.

Single-question round-trips are reserved for genuine ask-class **(a)–(c)** items above; anything
outside those three classes travels in the next packet. Target metric: ≤2 operator interactions
per lane-batch (intake #25 V-2). Operator directive 2026-08-06.

**The two numbers, counted separately (ratified 2026-08-08 — [#505] clause 2).** The 2-touch
budget is measured per seam, per batch, and the two seams are counted separately. operator ↔
integration: the GO at dispatch and the end-of-batch packet at close — target exactly 2. operator
↔ lane: contract acceptance plus any ask-class (a)–(c) escalation — target ≤1 escalation per
batch, reported in the packet rather than budgeted away. A batch reports both numbers; neither
substitutes for the other. Under sequential contract authoring, per-lane contract acceptances
count within the dispatch GO seam, not as additional touches.

**V-3 tiered ceremony — ceremony scales with arc size.** **S:** headless / auto-accept, no
plan-mode — contract → execute → terra → queue. **M:** one plan round. **L:** full ceremony.
`templates/prompt-template.md` (the work-lane card) is the point-of-use authority for the
per-Scale detail; the tiering is intake #25 AMENDMENT-b V-3, refined by AMENDMENT-c c2
(plan-mode-by-exception — the contract IS the plan).

**The S-contract, at its floor, is three parts:**

1. **One paragraph of contract** — the change, its footprint, and the one thing to avoid.
2. **One line of register entry** — the row or ruling the arc discharges.
3. **A JOURNAL entry as a fixed final step** — not removable by the tiering. Ceremony scales
   down; the anchor holds. An S-arc that drops its JOURNAL entry leaves an unanchored spine entry
   behind, which is the ARC-2 lesson this clause carries forward.

**Process-lane cap — from batch 2 onward, at most 1/4 of a batch's lanes target methodology or
hub-process surfaces.** The remainder carry product/consumer work. A batch that cannot fill its
non-process lanes **reports the shortfall** in its end-of-batch packet and runs narrower;
backfilling the gap with additional process lanes defeats the cap, which exists because
methodology work is the class that expands to fill whatever width is available. The cap is
evaluated against **dispatched width**; the end-of-batch packet reports the **close-width
delta**. Operator directive 2026-08-06; carried in-repo by intake #27. Denominator ratified
2026-08-08.

**Honest limits.** This protocol is doctrine plus two commands. The only mechanized parts are the
stale-worktree WARN (`audit.py::check_stale_worktrees`) and the naming enum
(`scripts/validate_branch_naming.py`), and both are advisory — the enum is wired into no gate at
all. Nothing here blocks a batch that skips a step: a lane that self-merges, a batch that closes
with an open lane branch, and a mid-batch seal all remain mechanically possible. The refusal in
"refuse-to-finish" is carried by the integrator command's checklist, not by a gate.

### The lane lifecycle — five legs, and where each one is ruled
<!-- scope: meta -->

The batch protocol above states the *shape* — one plan, N file-disjoint lanes, one integrator.
This subsection states the *sequence* a single lane travels end to end, because that sequence is
currently something a reader assembles out of five subsections that do not name each other in
order. It is an index in the sense this chapter's closing subsection uses the word: four of the
five legs are pointers to text that already exists, and only the fourth carries doctrine of its
own, having had no home until now.

1. **Dispatch.** The operator runs `dispatch <contract.md>` from a terminal; the contract's own
   `## Dispatch` block carries the literal line, and model + effort ride on it. Where the contract
   file lives and why the authoritative copy is a committed repo artifact — "Dispatch prompts and
   the contract of record" below. The surface itself — "The dispatch surface is `dispatch <file>`"
   below. The routing — "Model + effort are stated at dispatch" below. Visibility — "Dispatch
   visibility" below, whose consequence is that a lane is dispatched by the operator rather than
   spawned from a session, a spawned session having no Agent View row of its own.
2. **Execute under the frozen contract.** Under the batch protocol's five per-lane
   requirements, enumerated directly above and not re-listed here.
3. **Commit-and-STOP.** The lane hands back a branch and stops — requirement 4 above, and the
   integrator's own two surfaces: "Integrate from the primary" and "JOURNAL-rides-the-branch",
   the second of which is why a lane's arc leaves the JOURNAL to the integrator
   (`protocols/STANDING_RULINGS.md` P-1).
4. **Harvest.** The leg below — the only one of the five with no prior home in this chapter.
5. **Teardown.** The three-command round-trip plus the no-leftovers verification, at "4 —
   Integration & ephemeral teardown" above; its batch-scale form is `git worktree list` == primary
   only, in the refuse-to-finish checklist directly above.

**Harvest — the return leg, and its two rules.**

**Push before delete, on every harvest** (`protocols/STANDING_RULINGS.md` Q3; recorded as a
standing order in `JOURNAL.md` 2026-08-20 (i)). A merged branch is deleted on `origin` only after
the merge itself is pushed, so no window opens in which integrated work lives solely in one local
clone. The ordering is the whole content of the rule: delete-then-push inverts it, and between
those two commands the only copy of that lane's work is a local ref on one machine. Read together
with MERGE IS ATOMIC above, which makes merge + push + delete **one** operation — this line fixes
the *order* of that operation's three parts and leaves its atomicity untouched.

**Index freshness on lane material: the integrator is gate-of-record**
(`protocols/STANDING_RULINGS.md` Q1). A generated index — the audits index, the intake index, the
organ index — is regenerated **once, by the integrator, at the merge**. A lane that adds
index-governed material carries a **declared single-hook bypass on its own branch**, with the
declaration written into the commit body: which hook, and why. Two properties make that the
sanctioned shape rather than a concession. A generator reads the *tracked* working tree, so a lane
regenerating an index inside a tree another lane is also writing emits bytes that depend on
in-flight files — the determinism defect `scripts/gen_audit_index.py`'s own header records, and
the reason the 2026-08-12 night-1 lane declared the bypass instead of committing a wrong index.
And N lanes each regenerating one shared index produce N conflicting versions of a single
generated file, which is exactly the collision file-disjointness exists to prevent.

*Live practice, and it predates this text.* The 2026-08-20 playbook-status lane ran under exactly
this rule — `SKIP=audit-index-freshness` declared on both of its commits — and its integrator
regenerated the index once at the merge (`JOURNAL.md` 2026-08-20 (e)).

*Scope, stated so the sanction does not read wider than it is.* One hook, named in the commit body,
on a lane branch, for index-freshness material. It is not a general license against the gate mesh:
a bypass outside that scope is an operator decision, and `git push --no-verify` remains the sole
escape for the ADR-85 pre-push hard leg (amendment 2026-08-03 §A5), backstopped by the
`journal_spine_anchor` audit check.

**Honest limits, for both.** Prose, held by the integrator's checklist rather than by machinery.
No organ reads the ordering of a push against a remote-branch delete after the fact — MERGE IS
ATOMIC carries the same posture, its mechanical backstop being a proposal rather than a build. And
no organ reads a commit body for the bypass declaration: `SKIP=` leaves no artifact beyond the
message an author chose to write, so an undeclared bypass and a declared one are
indistinguishable to the tree.

### The wave close — every dispatched wave ends D0–D5, and the funnel table is mandatory
<!-- scope: meta -->

The batch protocol above governs how a wave is *dispatched* and how its lanes *merge*. It says
nothing about what happens to the **findings** those lanes produce, and that gap is where waves
have historically leaked: a lane records a finding correctly, the merge queue runs, the branches
are torn down, and the finding goes unclassified. **ADR-111 §4 and the decision tree already
exist** — the register's **P-2** anti-orphan rule and **Q6** contract-as-file sit beside it — but
nothing made *running* the tree a condition of closing a wave. This subsection does: it is the
mechanization of a tree that was already ruled, not a new tree.

**Every dispatched wave ends with the same six steps, in this order.**

| Step | What | Why the order is load-bearing |
|---|---|---|
| **D0** | **Enumerate, don't trust.** `git fetch --prune`, then find each dispatched lane's branch *by title*, across `claude/*`, `docs/*` and `feat/*`. | A missing lane is **reported, not assumed failed**. Both prefixes occur; a lane that produced nothing is a fact about the dispatch, and inferring failure from absence throws away the only evidence there is. |
| **D1** | **Read before merging.** Per lane: the artifact and its terra tally. **Unfixed Critical/High ⇒ that lane is HELD.** Confirm the environment caveat was declared wherever gates were hand-run. | Reading after merging means discovering a Critical on `main`. An undeclared hand-run is a *finding*, not a blocker — it is recorded, and the wave continues. |
| **D2** | **Merge queue, serial, operator GO each.** `--no-ff`. **Generated-file conflicts resolve by regeneration rather than by hand.** Then: relocations, ONE index regen, JOURNAL anchors per arc, the suite, WARN ownership, teardown push-before-delete. | Hand-resolving a generated file produces a result no generator would emit, and the next regen silently reverts it. Teardown follows the merge of the content; it does not precede it. |
| **D3** | **Closure sweep on the wave's own results**, before any filing. Record **`banked_D`**. | Closures before filing is the R2 arithmetic: births are capped by demonstrated close capacity, so the cap has to be *known* before it is spent. |
| **D4** | **THE FUNNEL TABLE.** Every finding, recommendation and residual from every artifact, classified into **exactly one** lawful next step, **each line citing its clause**. Then **PAUSE** — the architect returns one batched ruling over the whole table. | One batched ruling instead of N interruptions is the point. A table that classifies nothing is not a wave close. |
| **D5** | **Execute the ruling** — mechanical fixes, ADR drafts as PROPOSED, intakes filed, rejections recorded. **Births ≤ `banked_D`**; the remainder is a **named queue**, not a silent drop. | An unnamed remainder is indistinguishable from work that was forgotten. |

**The five classifications, and the clause each answers to** (ADR-111 §1's four outcomes, plus the
executed case):

- **MECHANICAL** — §1(b) DISCHARGED. The fix is judgment-free, so the integrator may execute it in
  the session. **List these first**, and a discharge is only a discharge **with a locator that
  resolves** — "we already do that" without one is not a discharge.
- **ADR** — §1(c) CANDIDATE where ADR-98 §3's fork test is met (a reasonable person could choose
  otherwise **and** reversal is costly). Draft it **PROPOSED with the Decision blank**, or attach
  it to an existing draft. A lane prices a decision; it does not make one.
- **INTAKE** — §1(c) CANDIDATE otherwise. **A finding may not become a backlog row directly**
  (§2): the only path runs finding → intake → ratification. Its carrier row waits for `ACCEPTED`
  plus the ledger, per **P-2**.
- **REJECT** — §1(d), **with the reason recorded where the finding lives**. A rejection is a
  recorded decision rather than a silent drop, and it is **not relitigated**.
- **COVERED** — §1(a) OWNED. Cite the id and **add nothing**.

**Four checks that make the table honest rather than decorative:**

1. **A COVERED cite resolves to a LIVE row, or it is not COVERED.** Check it. A sibling arc closing a row *while the
   lanes are in flight* is not hypothetical — it happened in the 2026-08-22 cloud wave, where four
   correctly-carried findings all named owner rows closed that same day, and classifying them
   COVERED would have pointed every one at a closed row. **That is how a correctly-filed finding
   dies quietly.**
2. **A lane's own recommendation is not automatically lawful.** Lanes ask for backlog rows because
   a row is the shape they think in; §2 forbids it. Re-route it through intake and carry the
   lane's specified shape verbatim, so ratification loses nothing by the detour.
3. **A finding may be refuted, and the refutation is recorded too** — including which half. A
   reviewer's *reason* can be wrong while the underlying defect is real; charging it to the wrong
   owner blames a lane that only mirrored existing state **and** leaves the real defect owned by
   nobody.
4. **A residual the lane names as OWED is discharged if this host can discharge it.** A second-
   reader pass a cloud container could not run is not a residual on a host that carries the
   wrapper — it is a step. Running it pre-merge is what keeps a Critical off `main`.

**The funnel table is a mandatory artifact section for every future integrator.** A wave whose
artifacts carry findings and whose close carries no table is **unfinished**, in exactly the sense
ADR-111 means when it says an audit whose findings are untriaged is an incomplete deliverable.

**One integrator at a time is enforced by mechanism (a lock or a branch guard), not by
convention** — its build rides the queued Q2-enforcement item. This line is born of the incident
that produced this subsection: the discipline held because one operator was watching, and a
discipline that holds only while someone is watching is not a mechanism. Until that item lands,
the serial-integrator rule in D2 is prose, and it should be read as prose.

### The night batch — the batch protocol run unattended, in five phases
<!-- scope: meta -->

**What this is, and what it is not.** Ch11's "Night-batch work" subsection states the night's
*doctrine* — propose-only, branch-only, honest-limits, the three organs a night needs. This
subsection states the *sequence*, in the same index sense the lane lifecycle above uses: a night
batch is the batch protocol, the lane lifecycle and the wave close above, run while the operator
sleeps, plus the handful of things that are only true at night. Where a phase is already ruled
elsewhere it points; where it is not, it carries the doctrine itself.

**Provenance — measured, not designed.** Architect ruling **X8**
(`protocols/STANDING_RULINGS.md` §X, 2026-08-27), intake **#60**, row `[#610]`. Every mechanic
below was read off the **2026-08-26 night**, whose four dispatched cloud sessions all delivered
read-only and lost nothing; the reference artifacts are
`docs/audits/2026-08-27-technical-night-harvest-manifest.md` and its sibling
`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md`. The cost of leaving the
protocol as habit was visible inside that same night: the harvest verb had no name and its API
mechanics were rediscovered rather than looked up, and the manifest shape that made the night
auditable was invented that evening and would have been reinvented the next.

| Phase | Owner | The one thing that makes it a phase |
|---|---|---|
| **1 · Dispatch** | operator | N frozen contracts go out; the night's compute is committed before the operator stops watching |
| **2 · Manifest** | orchestrating seat | the batch's own record, written in **two halves** — one before any lane boots, one at wake |
| **3 · Night run** | the lanes | unattended production, read-only or branch-only, ending in a harvest |
| **4 · Morning adjudication** | operator + architect | one packet is read, then D0–D5 runs over it |
| **5 · Ledger** | architect | every finding, its verdict and its destination, written down so the night outlives the seat |

**X8's own ordering, reconciled rather than left contradicting this one.** X8 names the phases
*dispatch → sentinel → harvest → manifest → morning adjudication*. Its "manifest" is the
**return** half only, and it stops before the ledger. The five-phase naming here spans **both**
manifest halves — the batch protocol's refuse-to-finish item above already rules the manifest as
"TWO halves, one at each end" — and promotes the ledger to a phase of its own, per intake #60's
acceptance criterion 6. Sentinel and harvest sit inside phase 3 as its two beats.

#### Phase 1 — Dispatch

*Inputs.* One frozen contract per lane, each a committed repo artifact ("Dispatch prompts and the
contract of record" below); the routing cut per lane (Q1–Q4 of the dispatch table below); the
substrate answer ("Two standing boundary rules the night inherits", at the end of this
subsection).

*Outputs.* N dispatched sessions, each with its receipt captured, and the **dispatch half** of the
manifest, committed **before any lane boots**.

*Refusal conditions.* A launch line composed by hand rather than copied from the dispatch table —
that table is the sole literal-command site, and four rival copies of that one command cost
roughly thirty consecutive seats a lane (`protocols/STANDING_RULINGS.md` §V). A contract whose
cited locators were not opened: `/preflight` is the built organ for exactly this, and a premise a
contract asserts without a witness is a defect **at freeze**, not at failure. A gate-dependent
lane routed onto a substrate where no gate runs — the boundary test is "The boundary — LOCAL or
CLOUD" below, and its night-standing form is rule (b) at the end of this subsection.

#### Phase 2 — Manifest

*Inputs.* The lane list and the frozen contracts (dispatch half); at wake, one report per
dispatched session (return half).

*Outputs.* The **dispatch half** is the batch manifest — the plan, committed before any lane
boots, so the batch stays reconstructable from something other than its own outcome (the
refuse-to-finish item above). The **return half** is the harvest manifest, whose shape is
specified here because it was invented once and has no other home.

**The harvest-manifest shape — specified so two seats produce the same sections.** Reference
instance: `docs/audits/2026-08-27-technical-night-harvest-manifest.md`, which validates against
every clause below.

1. **A header** naming the harvested night, the read-only transport actually used
   (`GET /v1/code/sessions/{id}/events`, paginated by `next_cursor`), and one sentence on what
   was written where. An explicit statement that nothing was written to any repo is **part of the
   record**, not an omission.
2. **`## Reports`** — one numbered block per dispatched session, each **opening with the
   session's label** and carrying **four fields in this order**: `file:` the landed artifact,
   `bytes:` its size, `first heading:` the artifact's opening heading (with its line number
   whenever that is not line 1), and `top recommendation:` one sentence of the report's own
   conclusion. A block missing a field is incomplete rather than short.
3. **`## PENDING`** — the sessions that had not delivered at wake. **An empty PENDING section is
   written out** (`None.`, with the reason). Its absence and its emptiness are different facts,
   and only one of them is a statement.
4. **`## Verification`** — what was checked, and every deviation recorded rather than repaired.
   This is the section the byte-identity rule in phase 3 lands in.

A manifest carrying those four, in that order, is the artifact the morning opens **first**, ahead
of any report. That ordering is the point of the phase: one file answers what came back, what did
not, and what deviated.

*Refusal conditions.* A `## PENDING` section **absent** rather than empty — absence and
emptiness are different facts, and only the written-out form is a statement. A `## Reports`
block short a field, which reads as a session that reported less rather than as a manifest that
recorded less. A `## Verification` section that **repairs** a deviation instead of recording it,
which is the byte-identity rule in phase 3 read backwards. And a dispatch half that lands
**after** the lanes boot: from that point it records the batch that ran rather than the batch
that was planned, which is the one property it exists to hold.

#### Phase 3 — Night run

*Inputs.* The dispatched contracts. *Outputs.* One artifact per lane, landed; the return half of
the manifest.

**Sentinel — the beat, without a mandated organ.** At wake the seat establishes which sessions are
complete, so a second sleep is taken only when one is actually owed. On the witnessed night all
four were complete at first wake and no second sleep happened. The phase is named and the organ is
not required: one clean night is n=1, and this chapter's own evidence gate asks for two
(Ch11's operational standard for a routine, item 7 — the n=2 graduation gate).

**Harvest — read-only, and byte-identical.** A cloud session's report is **evidence**. It lands
verbatim — same bytes, UTF-8, no trimming, no reflow, no heading surgery.

**Byte-identical, or state the deviation.** Where a landed artifact does not satisfy a convention
the landing seat expected, **the artifact wins and the Verification section records the
deviation**. Trimming an artifact so a check passes destroys the evidence and hides the finding in
one act. Worked example, from the reference night: C2 and C4 open at byte 0 with their own
heading; **C1 and C3 do not** — each wrapped its report in a code fence preceded by one line of
prose, putting the heading on line 4. Both were landed verbatim and both deviations were written
into Verification. That was a judgement on the night; here it is the rule.

**Report selection — and the Stop-hook-noise trap.** The report is **not** reliably the last
assistant text in a session. On the reference night the last text in each of the four sessions was
trailing Stop-hook backpressure noise ("Unchanged. Done.", "Nothing further.") from a container
where `uv run --locked` could not start — uv 0.8.17 against the repo pin `==0.11.19`, so the
hook's own gate refused before its script began. Taking the last text would have harvested that
noise as the night's product, four times over. The rule that held: **select the longest assistant
text**, which in all four sessions was assistant text #2, immediately after the RECEIPT. Name the
selector used in the manifest, so a wrong selection is visible rather than silent.

*Refusal conditions.* A night lane that merges, pushes, edits canon, closes a row or issues a
ruling has left the propose-only envelope (Ch11 "Night-batch work"). A gate-dependent claim
produced on a substrate that ran no gate is marked MEASUREMENT-OWED-LOCAL rather than estimated.
Every night output stays UNVERIFIED-UNTIL-LOCAL until a local gate run says otherwise.

#### Phase 4 — Morning adjudication

*Inputs.* The manifest, read first; then the landed artifacts and their terra tallies.
*Outputs.* One operator-facing packet, and the wave close.

The adjudication itself is **already ruled and is not restated here**: it is D0–D5 in "The wave
close" directly above, whose D4 funnel table classifies every finding into exactly one lawful next
step (ADR-111 §1). Two night-specific additions:

- **The manifest is read before any report.** It is the only surface carrying what did *not* come
  back, and a wave that reads only what arrived closes over the reports it has rather than the
  reports it dispatched — D0's "enumerate, don't trust", applied to artifacts instead of branches.
- **Adjudication stays a human act in the morning.** The night produces proposals and evidence;
  **nothing merges unattended.** That is Ch11's hard rule, stated where it gets tested.

*Refusal conditions.* A close carrying findings and no funnel table is unfinished. A verdict taken
against a report whose gate-dependent claims are still MEASUREMENT-OWED-LOCAL is a verdict on an
unmeasured claim.

#### Phase 5 — Ledger

*Inputs.* The adjudicated funnel table. *Outputs.* one consumption ledger under `docs/audits/`,
carrying an ADR-101 enum class token like any other audit artifact.

**The ledger is a REQUIRED output of the protocol, not an optional one.** Reference instance:
`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md`. It carries every finding
from every night report with **the architect's verdict and its destination** — including the
rejected items, listed with their reason, because a rejection is a recorded verdict rather than a
deletion. Its own statement of purpose is the whole case for the phase: *if this chat or seat is
lost, the next seat executes THIS file and nothing from the night is dropped.*

Why `docs/audits/` rather than a handoff bundle: a ledger is adjudicated once and cited
thereafter, which is the audit lifecycle rather than the bundle lifecycle. Intake #60 left this
open; it is answered here on the reference instance's precedent.

*Refusal conditions.* A night that closes with no ledger has produced findings whose only carrier
is the seat that read them. A ledger listing the accepted items and dropping the rejected ones has
lost the reasons — the half that stops an item being relitigated next window.

#### The night's four standing constraints

Carried here from intake brief #1 §6 by way of `[#271]`'s 2026-08-28 re-cut, which struck that
row's rival charter and routed its constraint list to this protocol as its correct home
(`tasks/271-nightly-proposal-loop.md`; row `[#610]`). They bind an unattended night whichever
phase is running:

1. **A cap of roughly five proposals per night.** Past it the morning stops being adjudication and
   becomes new toil — the fleet-audit failure mode the cap exists to refuse.
2. **Untriaged items auto-expire after seven days.** An item nobody ruled in a week is a queue,
   and an unread queue is indistinguishable from a decision nobody took.
3. **No autonomous semantic refactoring at night.** Mechanical and pre-authorized deterministic
   work is in scope; a change turning on judgement about *meaning* waits for a seat that is awake.
4. **Proposals land in `docs/intake/` as `status: SEED`** — the ADR-98 requirements spine, and
   deliberately not a parallel `proposals/` folder.

*Honest limit, and it is why the list reads as prose rather than as enforcement.* Each of the four
is prose. `[#271]`'s surviving Done-when asks for the **survival review** — a dated `docs/audits/`
artifact recording a measured accept-rate against the `<20 %` kill threshold, over whatever
unattended cadence is actually running — and that review has not been run. Until it is, these four
bind the seat and not the tree.

#### Two standing boundary rules the night inherits

Both were answered by a prior architect seat and would otherwise die in that seat's head. They
land here, and `protocols/HANDOFF_PROCESS.md` §4 asks the bundle's operator-facing forms card to
carry them, so a future bundle boots them instead of rediscovering them.

**(a) The session boundary — a merge is not an ending.** The architect does **not** propose
session closure and does **not** initiate the bundle; **the operator declares closure**. The
window's rhythm is *boot → plan → freeze → GO → integrate → audit → next batch*, and it continues
until the operator ends it. Recorded as seat lesson **L-S2**,
`docs/audits/2026-08-28-technical-night-mission-authorization.md`. *Locator note:* the frozen
contract that landed this rule also names a **"five-pillar close"** as part of it; that term
resolves to no surface in this tree at the time of writing, so the two clauses above — the ones
the contract itself enumerates — are what land, and the term is reported as **unlocatable** rather
than reconstructed from guesswork.

**(b) Substrate routing — LOCAL is the default, conditionally.** Ruling **Z-G3**
(`protocols/STANDING_RULINGS.md` §Z) amends U(b): *"GitHub compute is the DEFAULT substrate"* is
**conditional**, taking effect only once all three defects ruling W4 measured are closed —
`gh codespace cp` receiving literal single quotes, `uv` unusable in the container, and the
silently stale clone. **Until then the default substrate is LOCAL.** A gate-dependent lane routed
onto a substrate where no gate can run does not produce a slow verdict; it produces a green one
that nothing earned. The entry condition for the wave-2 router ADR is the smoke-6 receipt —
`Ok=True` **and** `RemoteExitCode=0` **and** `receipt HEAD == pushed HEAD` — which has not been
produced. Untouched by that ruling: the settled 2026-08-20 position, Codespaces free 4-core, no
overage.

*The `uv` nuance, at the resolution the night actually measured.* The container's `uv` is not
simply missing: on 2026-08-26 it measured **0.8.17 against the repo pin `==0.11.19`**, so every
`uv run --locked` gate refused before its script started — **unrunnable by default, and runnable
after a one-step `pip install --target` provisioning of the pinned build**, after which the gates
ran clean (`docs/audits/2026-08-26-technical-handoff-census.md`, Appendix B). **The routing is
unchanged by that measurement.** Ch8's Q1 row below carries it as an *amendment candidate, routing
unchanged pending a ruling*, and this subsection **cites that status rather than resolving it** —
a night seat reading only this text routes exactly as Q1 routes today.

#### What the night corrected in itself

Both rules below come from the 2026-08-28->29 night's own run. Each records a live failure of the
window that produced this protocol, which is why they land as rules rather than as notes.

**A time-conditioned stop reads a fresh clock at decision time.** Any stop conditioned on wall
time — the night mission's **S5 hard stop** is the instance — takes the time from a **fresh source
at the moment the decision is taken**, rather than from a value the session read earlier and
carried forward. *Why it is a rule:* on the night that produced it, the S5 07:30 hard stop was
reasoned against a **stale clock** — the session was working from 01:5x while the wall clock had
already moved to 11:0x — so the remaining schedule was derived from a premise that was hours
wrong, and every downstream go/stop judgement inherited that error. A cached timestamp is an
observation about the past; a stop condition is a question about the present, and the two coincide
only at the instant of the read.

**Orchestrator handover happens at a phase boundary.** A change of orchestrating seat lands
**post-integration and pre-wave** — on the seam between phases — rather than mid-queue. A handover
taken with a merge queue part-walked hands the incoming seat a state no artifact describes: the
contracts record what was dispatched and the ledger records what was adjudicated, and between them
sits a half-walked queue that neither surface carries. At a phase boundary both surfaces are
current, so the incoming seat boots from the record instead of from the outgoing seat's memory.

#### Honest limits

This whole subsection is prose. No gate reads it: no organ counts a night's proposals against the
cap, expires an untriaged item at seven days, checks a manifest for its four sections, or refuses
a night that closes with no ledger. The two verbs the protocol wants — **`Dispatch-After`** (the
*deferred form of* the ruled `Dispatch` verb, `protocols/STANDING_RULINGS.md` §V, and not a rival
to it) and **`Harvest-Cloud`** — are win-tooling and operator-owned, and are the other half of row
`[#610]`. The shape has been witnessed **once** (2026-08-26), so by this chapter's own evidence
gate it is a **recorded practice at n=1**, not a graduated standard.

### Dispatch visibility — Agent View shows DISPATCHED sessions only (STANDING_RULINGS B7)
<!-- scope: meta -->

Claude Code Agent View (`claude agents`) lists `--bg` (dispatched) sessions. A foreground session
running in another terminal, even a long one, is outside that view — a property of how the view
is built, confirmed live 2026-08-06, not a bug to route around.

**The convention this sets.** A handed-off, non-interactive task starts life as `claude --bg`, or
crosses over via `/bg` at the point a foreground session becomes hand-off work. Foreground stays
reserved for interactive sessions the operator is watching in real time. A batch lane (the
protocol above) dispatches `--bg` in every case — one exception would put that lane outside the
one place an operator scans for "what's running."

**The dispatch shape — POINTER, not a command.** The literal launch line for every substrate
lives in ONE place, "The dispatch table — the SOLE literal-command site" above. This subsection
used to carry a raw `claude --worktree --bg …` line of its own; that line was one of the four
rival forms the 2026-08-25 measurement identified as the root cause, and it is removed rather
than restated here. What this subsection owns is the VISIBILITY property and the board label
below — not the command.

**The board label opens every dispatch prompt**, so a row in Agent View scans at a glance even at
ten concurrent agents — the operator's attention goes to Needs-input rows, not to re-deriving what
each row is from its tail text. Shape: `[repo · #id-or-slug · verb-object]` — e.g.
`[dev-knowledge · #505 · fold-dispatch-visibility]`. `.claude/commands/lane-boot.md` and
`templates/prompt-template.md` carry this by construction rather than by reminder — a dispatch
prompt built from either starts with the label already in place.

**Flag composition, checked against the installed CLI (2.1.224).** `claude --help` lists `--bg`
(`--bg, --background`) and `-w, --worktree` as independent flags with no documented mutual
exclusion — the only noted dependency runs the other way (`--tmux` needs `--worktree`). Where a
live nested dispatch cannot be exercised (a worktree-isolated session declining to spawn another
worktree session from inside itself, for instance), the fallback is dispatching `--bg` from inside
a worktree the lane-boot protocol already provisioned — the two steps run in sequence rather than
composed on one command line, with the same visibility result.

**A nested session carries no row of its own — so the OPERATOR dispatches, from a terminal (AM-5,
operator-ratified 2026-08-11).** A session spawned from *inside* another session (nested / child)
does not surface as its own Agent View row. The consequence for the batch protocol above is
direct: **batch lanes are dispatched by the operator via `dispatch <contract>` from a terminal,
never spawned from the primary session or any other session.** A lane spawned session-side runs
invisibly, which is the one property "VISIBLE = DISPATCHED" exists to guarantee — defeated at the
point of dispatch rather than by a dropped flag, and therefore invisible to the flag discipline
the paragraph above encodes. This also settles the sequencing fallback recorded there: the second
step is an operator act at a terminal, not a spawn from the session that provisioned the tree.

**The agent-view dispatch input is scoped to ad-hoc, read-only, default-model tasks.** The input
inherits the *view session's* default model and effort — fixed when the view is opened
(`claude agents --model … --effort …`) or changed in-view via `/model` — and offers **no per-task
override**. A task typed there runs at whatever routing the view happens to carry, which is
exactly what disqualifies it for a batch lane: a lane's model and effort are stated at dispatch
and travel on the lane's own dispatch line ("Model + effort are stated at dispatch — the routing
matrix" below). Ad-hoc read-only work is what the input is for; a lane goes through
`dispatch <contract>` instead.

### Dispatching a session — the boundary, the dispatch table, and the standing rules
<!-- scope: hybrid -->

**A session handed to the operator without its command does not get started.** That is the
failure this subsection closes, and the chapter's other dispatch sections assumed it away: they
rule on the conditions a dispatch satisfies — a receipt, a committed contract, a stated tier —
and stop short of *what the operator types*. Everything below is directly actionable. A seat writing a
handover **copies** a line from here rather than composing one, and
`scripts/gen_lane_contract.py` emits the same line mechanically with every contract it generates,
selecting the shape from the contract's own declared type — so the prose and the generator cannot
drift, and a contract emitted with no command line is a generator bug with a test asserting it.

**Where the commands live — OPERATOR-OWNED, at L0, and deliberately not reimplemented here.**
`Dispatch-Local`, `Dispatch-Cloud` and `Dispatch-Codespace` (with their working version-named
aliases `Dispatch-Lane`, `Dispatch-CloudV2`) are PowerShell aliases exported by `win-tooling`
`config/dispatch-helpers/DispatchHelpers.psm1`, deployed SHA-256-compared and auto-loading by that
repo's `scripts/dispatch-helpers/Apply-DispatchHelpers.ps1`; `dispatch` is a PATH command from that
same repo's `scripts/dispatch/Invoke-Dispatch.ps1`. **That module is the source of truth for their
BEHAVIOUR and this repo does not carry a copy of it** — what this chapter records is each verb's
CONTRACT (argument shape, receipt, guards) so a seat can use it without reading PowerShell, and
which one to reach for, and why. They are a versioned, tested, SHA-deployed module rather than
profile cruft: they resolve identically in `pwsh -NoProfile`, profiled `pwsh`, and PS 5.1, and the
profile is deliberately unused because it sits inside the corp OneDrive exclusion zone. A raw diff
of the deployed copy against source shows all 1211 lines differing; that is CRLF vs LF and nothing
else — the applier normalizes to LF before hashing, by design. Do not report it as drift.
`Dispatch-CloudBrief` is **superseded** — it prints its own supersession notice — and is named
here only so a seat meeting it in an old artifact knows not to use it.

#### The boundary — LOCAL or CLOUD, and the rule that gets forgotten

- **LOCAL** if the work needs the operator's **disk**: provider keys and vendor CLIs (any
  model-admission run), unpushed local branches, files in the prompts dir, anything that reads his
  machine.
- **CLOUD** if all inputs are **in the repo on `origin/main`**. *"Cloud" here means a **dispatched
  cloud lane** — a session someone launched against a brief. It is a different population from
  Ch11's **scheduled cloud Routine**, which fires on a cron and answers to that chapter; the two
  share a word and nothing else.* A cloud session clones from origin
  and **cannot see unpushed branches or local files**. That is a physical limit of the transport,
  not a caution — a cloud lane pointed at unpushed work does not run slowly, it runs against
  content that is not there.
- **Integration is always LOCAL *and* INTERACTIVE.** Merges need operator GO per merge, and a
  background lane can neither merge to `main` nor ask a question. An integrator dispatched `--bg`
  is a contradiction in terms, not an aggressive schedule.

This is the routing test the "Cloud lanes" subsection below records as **owed** — it is answered
here, and that subsection's gate-mesh heuristic (local when a local-only gate governs the
footprint) refines it rather than competing with it. Where the two would disagree, the disk test
above decides: a footprint no local gate governs still routes LOCAL if it needs the operator's
disk to read its inputs.

#### The dispatch table — the SOLE literal-command site
<!-- scope: hybrid -->

**This table is the only place in the repository that carries a literal launch command.** Every
other site — `templates/prompt-template.md`, `.claude/commands/lane-boot.md`, and the two other
dispatch subsections in this chapter — points here. That is a correction, not a style preference:
the hub documented FOUR rival commands for one act, `/lane-boot` emitted the form this chapter
itself calls "the FALLBACK form, not the default" while silently dropping `--model` and
`--effort`, and roughly thirty consecutive browser seats failed to launch a lane. They were not
uninformed; they were informed by sources that disagreed. Full measurement, probed in three
shells: `docs/audits/2026-08-25-technical-dispatch-surface-measured.md` (2083 lines).

**THE RULING (operator, 2026-08-25).** `dispatch <contract.md>` is THE sole operator verb for a
LOCAL lane — and it is **local-only**: it does not read a contract's `Substrate` field and cannot
route, so today the substrate is chosen by **which verb the operator types**
(`Dispatch-Local` / `Dispatch-Cloud` / `Dispatch-Codespace`) and a contract's `Substrate:` line is
**documentation only** until the Layer-3 router lands. `Dispatch-Local` (née `Dispatch-Lane`) is
the documented manual fallback. Substrate-named verbs are canonical; version-named ones
(`Dispatch-CloudV2`) are working aliases. The raw `claude --bg` / `--worktree` form is
**FALLBACK-ONLY** and does not appear in a command file or a template. Interactive and
primary-checkout seats keep the shape in row 3 below.

##### Layer 1 — which substrate, cut in this order, first match wins

| | Question | Route |
|---|---|---|
| **Q1** | Does the result depend on a gate (suite / hooks / ship-gate)? | **NOT cloud** — measured: no hook armed there, unpinned `uv`, no `click`. Codespace or local. **Measured again 2026-08-26: container `uv` is pinned-but-WRONG (0.8.17 against the repo's `==0.11.19`) and provisionable in one step, after which `uv run --locked` gates ran clean — an amendment candidate, routing unchanged pending a ruling (`docs/audits/2026-08-26-technical-handoff-census.md`, Appendix B).** |
| **Q2** | Does it need operator-disk state (contracts in the prompts dir, authenticated vendor CLIs, unpushed branches), or is it an operator-gated act (merge, push, integration)? | **LOCAL**, stop. |
| **Q3** | Is it read-only / reconnaissance (censuses, verification, fan-out)? | **CLOUD** — own clones, cheap, unlimited parallelism. |
| **Q4** | Everything else — repo-mutating, disk-independent | **CODESPACE** (the default once the devcontainer carries Claude Code and its credential). |

**Concurrency ceilings and cost, per route.** LOCAL: one WRITER per checkout; parallelism only
across worktrees. CODESPACE: 2–4 concurrent (2-core, ~60 s to Available, 120 free core-hours per
month ≈ 60 h). CLOUD: effectively unlimited (own clones); not for gate-dependent work. **The batch
ceiling stays 4–6 lanes on every substrate** — it is bounded by integration capacity, which is
serial, not by how many independent work items exist (`STANDING_RULINGS.md` section U rule (b);
evidence `LESSONS.md` 2026-08-25 coordination tax).

##### Layer 2 — the commands, per substrate

Every line below is **probed and current 2026-08-25**. A seat copies one; it does not compose one.
All three verbs run Claude with **bypass permissions** as a standing rule — no permission prompt
blocks a lane on any substrate.

**1 — LOCAL background lane** (own worktree, commit-and-STOP). Run **from the target repo root**
— the verb is cwd-bound, and dispatching from the wrong repo puts the worktree in the wrong repo.

```
dispatch <FILE.md>                  prompts [y/N], then fires
dispatch <FILE.md> -DryRun          prints the resolved line, sends nothing
```

- **Argument shape:** a bare filename resolving against the prompts dir; a bare stem also resolves
  (`FOO` finds `FOO.md`). An absolute path, or one that exists relative to the cwd, is used as given.
- **Where the contract lives:** the prompts dir (below), copied in-tree into
  `docs/audits/<date>-technical-<batch>-launch-contracts/`.
- **Receipt:** the resolved `claude --bg …` line is printed before firing; the lane's own receipt
  is its branch — `worktree-<slug>` — appearing in `git branch`.
- **Guards:** model/effort/worktree/label are derived from the contract, so the contract and the
  command cannot disagree. Effort is a closed enum `{low | medium | high | xhigh | max}` and a
  miss is a refusal naming the enum. A live `claude` does not fire bare: with neither `-DryRun`
  nor `-Run` the operator is asked to confirm, and anything but `y`/`yes` — including empty or
  non-interactive input — refuses.
- **Manual fallback, when the contract does not carry a parseable routing block:**
  `Dispatch-Local <slug> <FILE.md> -Effort high` (alias `Dispatch-Lane`; a third positional
  argument is an amendment appended without reissuing the contract). It creates
  `worktree-<slug>`, **refuses if that branch exists** so a re-run is a no-op, and treats a
  120 s branch-wait timeout as a WARNING rather than a failure. Feed it the slug
  `lane-<letter>-<id>-<slug>` and it produces exactly the canonical batch-lane branch.

**2 — CLOUD lane** (repo-bound, off-machine, receipt-gated):

```
Dispatch-Cloud <FILE.md> -Title '<slug>'
```

- **Argument shape:** the WHOLE file is the brief — it travels in a JSON body, so one file = one
  lane, and a multi-lane bundle is not a thing this transport carries. Binds Revision `main`.
- **Receipt:** three gates. G1 *created* (HTTP 200, id prefixed `session_`), G2 *bound*
  (`config.sources[0].type == git_repository`; an **empty `sources` array is the bundle-mode
  defect** by name), G3 *receipt* (first assistant text, soft on timeout). G1 and G2 are hard —
  fail either and nothing ran. Watchable at `claude.ai/code`.
- **ID TRAP:** create mints `session_<suffix>`; every read/manage endpoint wants `cse_<suffix>`.
  Feeding the minted id to a read returns 404, which reads as "no such session".
  Manage: `Get-CloudSession cse_01ABC` · `Archive-CloudSession cse_01ABC`.
- **Guards:** a cloud session clones from origin and cannot see unpushed branches or local files —
  a physical limit of the transport. Its image may carry the wrong `uv`, so a brief instructs the
  lane to hand-run gates as `python3` and to declare that it did. `Dispatch-CloudV2` is the
  working version-named alias; `Dispatch-CloudBrief` is superseded and prints its own notice.

**3 — INTERACTIVE** (integration, seat acts, anything needing operator GO). Start `claude`, then
send as the FIRST message — expand the path by eye, because a chat is not a shell and nothing
expands the variable for the operator:

```
claude
```
```
Read <PROMPTS_DIR>\<FILE>.md and execute it exactly.
```

- **Receipt:** the session answers. **Guards:** integration is always LOCAL *and* INTERACTIVE — a
  background lane can neither merge to `main` nor ask a question, so an integrator dispatched
  `--bg` is a contradiction rather than an aggressive schedule. Rows 1 and 2 take a bare filename;
  this row is the one shape where the operator resolves the path himself.

**4 — CODESPACE** (the repo's own devcontainer, off-machine, receipt-gated):

```
Dispatch-Codespace -Contract <FILE.md> [-Slug <name>] [-Repo <owner/repo>] [-Branch <b>]
                   [-Machine basicLinux32gb] [-IdleTimeout 30m] [-Retention 24h] [-DryRun]
```

- **Argument shape:** the contract is shipped in **as a file**, and so is the runner — the only
  thing on the ssh command line is `bash <path>`, one token, no quotes. A PowerShell string
  reaching a bash login shell through gh's ssh transport is parsed twice, which is the failure
  class this design exists to avoid.
- **Receipt:** `receipt.json` is pulled back out, and success is reported only with it in hand.
  **Read `Ok` and `RemoteExitCode` separately**: `Ok` means the transport succeeded,
  `RemoteExitCode` is the work's own code parsed from gh's `shell closed: exit status N` text
  (gh's own code is 1 regardless). A caller branching on `Ok` alone reads a failed lane as a success.
- **Cost guards:** `--machine basicLinux32gb` is 2 cores / 8 GB — the smallest machine meeting the
  floor `devcontainer.json` declares, so it is both correct and cheapest. `-IdleTimeout` and
  `-Retention` bound the spend, and cost inputs print on **every** dispatch including `-DryRun`.
  `Stop-DispatchCodespace` wraps `gh codespace stop`; **stopping is not deleting** — compute
  billing ends, storage keeps counting until retention expires. `gh codespace delete` is
  deliberately not wrapped: deletion stays an operator act.
- **Measured wall-times (five runs, stable):** create returns 5.4–6.1 s · Available ~60 s · cp-in
  ~74 s (blocks until the container is up) · in-container run 5.9 s · receipt out 6.2 s ·
  **total ~95 s**.
- **Credential — the SUBSCRIPTION OAuth token, not a Console API key.** Codespaces secret
  `CLAUDE_CODE_OAUTH_TOKEN`, from `claude setup-token`; model-requests only, and usage counts
  against the operator's plan rather than raising a separate API invoice. `ANTHROPIC_API_KEY` is
  kept out of the image and its config: when both are present the API key takes precedence and
  would silently flip billing off-subscription. Exposure and rotation:
  `protocols/STANDING_RULINGS.md` section V.
- **That token arrives via the LOGIN-SHELL profile, so a non-login probe reads it as ABSENT — and
  the false negative is the point of this bullet.** Measured 2026-08-29, codespace
  `nb2-smoke6c-j47pvjw957ghq76v` (`rdwornik/dev-knowledge`), one container at one moment:
  `gh codespace ssh -c <name> -- 'printenv | grep CLAUDE_CODE_OAUTH_TOKEN'` returned **0 matches**
  and `/proc/1/environ` carried it **not at all**, while `bash -lc 'echo ${#CLAUDE_CODE_OAUTH_TOKEN}'`
  returned it **present, length 108**. The Codespaces user secret IS delivered; it lands through
  the login-shell profile rather than in the container's base environment.
  *The operational consequence, which is the half worth writing down:* any automated step running
  a **non-login** shell — `gh codespace ssh -- <cmd>`, a CI step, a hook, a dispatched lane's
  command string — reads the token as absent and presents as a missing-secret or mis-wired-secret
  failure **while the secret is in fact configured correctly**. The caller-side fix is to wrap the
  command as **`bash -lc '<cmd>'`**; re-issuing or re-adding the secret fixes nothing and costs a
  rotation. This is recorded because the first probe against it read ABSENT and a wiring gap that
  did not exist was nearly reported — a debugging round already spent once. Reconciling this with
  the "Argument shape" bullet above: the **interactive** `gh codespace ssh` session gets a login
  shell, and the `-- <cmd>` form does not, which is why the same transport reads two ways.
  *Probing it:* run the check with `python3` (or `bash -lc`) invoked directly and **say so** —
  `uv` measured **absent** in that image on 2026-08-29, so a bare `uv run --locked` there fails
  before its script starts. That reading is stronger than the pinned-but-wrong `0.8.17` recorded
  at Q1 above; both measurements are cited and neither is resolved here. The sibling hazard is
  unchanged and still open: a codespace clone sits silently behind `origin/main` (measured 50
  commits, with `git status` looking unremarkable until read closely).

##### Where the contract file lives — two homes, one of them in the tree

**The prompts dir** is the operator-side home: `$env:CLAUDE_PROMPTS_DIR`, defaulting to
`~\Downloads`. A dispatch line cites `<PROMPTS_DIR>\<file>` rather than a hard-coded absolute
path, which keeps the line portable across machines. All four verbs above resolve a bare filename
against it.

**`docs/audits/<date>-technical-<batch>-launch-contracts/` is the in-tree home** (operator ruling
2026-08-26; ADR-101 amendment 2026-08-26 (b)). The contracts a batch was ACTUALLY launched from
are copied there byte-identical and committed with the batch, one directory per batch. Contracts
are hand-authored off-repo, which is why every commit-time gate was structurally blind to them;
this convention is what makes a batch's launch inputs committed evidence a later reader can open.
It changes nothing about how the operator receives or edits a contract.

**The root `prompts/` folder this convention briefly used (2026-08-25 → 2026-08-26) is REVOKED** —
*"root is sacred, the docs disease is cured by the consumer gate, not by a sibling folder."* An
accumulating artifact class earns a **consumer**, not a top-level home: these contracts are read
by the **batch close packet**, which is the consumer `[#595]`'s consumer-at-landing rule asks a
landed `docs/audits/` artifact to declare. Cite the new path in anything you write; `prompts/`
resolves to nothing on the live tree, and Rule A refuses it if recreated.

**Two honest limits, so this section is not read as more than it is.** (1) The name shape above is
**checked by nobody** — ADR-101's `_HOME_PATTERNS` grammar is three tokens wide and can only say
`docs/audits/*`, so any immediate child directory of `docs/audits/` is admitted and the convention
rests on this text. (2) The generated `docs/audits/README.md` index globs `*.md` at **one** level,
so a launch-contracts directory **does not appear in it** — the batch's close packet is what makes
it findable.

##### Honest limits of this table, stated so it is not read as more than it is

- **`dispatch` is local-only and does not route.** Repeated here because it is the single fact a
  seat most often gets wrong: the substrate is the verb you type, and a `Substrate:` line in a
  contract is documentation until the Layer-3 router lands (`STANDING_RULINGS.md` section V,
  PLANNED).
- **The lane-contract `Model` cell carries a machine token from `{opus | sonnet | haiku}` — prose
  belongs in its own column or outside the table.** A cell reading `Opus (opusplan default)` is
  refused by `dispatch`, which is why the 2026-08-25 batch launched through the manual fallback
  rather than the ruled verb. `templates/prompt-template.md` carries the corrected shape.
- **This table checks nothing.** It is prose that agrees with the machine today. The drift organ
  that would assert every literal command here resolves via `Get-Command`, and that
  `/lane-boot` names the ruled verb, is owed rather than landed.


#### Standing operator-interface rules

- **Every prompt file reaches the operator via the prompts dir (`~\Downloads`), never the
  Desktop.**
- **Inline paste arrives empty in his client — always a `.md` upload.** A brief pasted into the
  message body is not a brief that was delivered.
- **No session ships without its command.** A handover that names a contract and not the line
  that launches it is incomplete, whoever wrote it.
- **Lane artifacts land in `docs/audits/`, never the repo root** — `validate-hermetization`
  Rule A refuses a new top-level file class, so a root artifact is a refusal discovered after the
  work is done.
- **Teardown is sequenced *after* a session STOPs**, never alongside a ruling that keeps it alive.

### Dispatch prompts and the contract of record — two locations, one of them in the tree
<!-- scope: meta -->

**The prompts dir.** A dispatch prompt is an operator-side file: the operator opens it, references
it in the launching line, and pastes. It lives in the **prompts dir** — `~/Downloads` by default,
overridden by the `CLAUDE_PROMPTS_DIR` environment variable — and a dispatch line cites it as
`<PROMPTS_DIR>\<file>` rather than as a hard-coded absolute path. The variable form keeps a
dispatch line portable across machines and keeps one operator's directory layout out of an
artifact other people read. Token expansion is no longer the operator's job: `win-tooling`'s
`scripts/dispatch/Invoke-Dispatch.ps1` resolves the literal `$env:CLAUDE_PROMPTS_DIR` token
itself, and also resolves a bare contract filename against that same directory ([#509] v2,
merged `d743937`) — the dispatch-surface section directly below.

**The contract of record is a different object, and it lives in the tree.** [#505] clause 1 asks
for a fresh seat that runs a full batch from repo artifacts alone, and batch 2 falsified it for
one precise reason: its four lane contracts were files in the operator's Downloads. The *plan* was
in the tree — the manifest committed at dispatch, which was the batch-2 advance — while the
*contracts* were not, so the integrator reconstructed the merge queue from the ref store and from
**session transcripts**, which are repo artifacts in no sense at all.

**Contract-as-file, without exception (`protocols/STANDING_RULINGS.md` Q6, ruled 2026-08-19/20)
— at dispatch, the batch manifest links or embeds each frozen lane contract as a committed repo
artifact.** Dispatch convenience stays in the prompts dir; the
authoritative copy lands with the manifest — embedded in it, or committed beside it under a name
derived from the ADR-101 class enum — and the manifest's lane rows point at it. That leaves the
prompts dir as a *delivery channel* rather than a storage location, which is what a
`<PROMPTS_DIR>` reference already implies.

**The cutover, dated (architect ruling 2026-08-21).** Batch-1 contracts predate
`gen_lane_contract` and are **records, not templates**; every later contract is
generator-emitted and hook-checked. The eleven committed at
`docs/audits/2026-08-21-*-lane-contract.md` carry a title-plus-prose shape that fails
`gen_lane_contract check` 11-for-11, and they are grandfathered rather than retro-fitted:
editing a contract after its batch executed would falsify the record of what was actually
dispatched. The `lane-contract-check` pre-commit gate is therefore scoped to the
generator's own emitted name shape (`LANE-<slug>.md`), so it governs batch 2 onward and
ignores the record.

*Q10 (`protocols/STANDING_RULINGS.md`): a lane that discovers a refuted premise **PAUSEs with
the fact** — deviation-with-disclosure is not a license; the disclosure discharges the
reporting duty, it does not authorise the deviation.*

**Inline-with-a-dummy-filename is a forbidden dispatch form.** A dispatch line naming a file that
was pasted rather than committed records a locator that resolves to nothing, which is the whole of
what this rule closes. Q6 is the **unconditional** reading of `protocols/STANDING_RULINGS.md`
I-D3, and it **retires the "repair path, for batch 3" scoping this paragraph carried until
2026-08-21**: the rule is not staged to a batch and carries no conditional form. The two
consequences below are unchanged — they are read as the standing shape rather than as one
batch's repair.

Two consequences, both drawn from batch-2 evidence rather than from design taste:

- A lane's frozen contract becomes citable by a successor seat, which is the property
  "reconstructable from repo artifacts" actually names. Reconstruction from transcripts is
  available only to a seat that can read those transcripts, and it expires with them.
- A committed contract's own path is checkable at authoring time against the ADR-101 enum —
  exactly what the F3 paragraph above already asks of the paths a contract *names*, now applied to
  the contract itself. `validate-hermetization` sees it, rather than a lane discovering the
  refusal after boot.

**Honest limit, stated so this is not read as done.** This is a documented path, not a
mechanism: nothing checks that a manifest's lane rows resolve to committed contracts, so the
property [#505] clause 1 names — a fresh seat running a full batch from repo artifacts alone — is
carried by the authoring seat rather than by a gate, and is re-established or lost batch by batch.
The sentence that used to stand here pointed at the batch-3 manifest as "the first artifact that
can satisfy it"; it is removed with the batch-3 scoping the amendment above retires, since a rule
with no conditional form has no first batch either.

### The dispatch surface is `dispatch <file>` — the contract file is the source ([#509] v2)
<!-- scope: hybrid -->

**SCOPE, amended 2026-08-23 (M10).** This section's claim below — *"the operator's whole dispatch
surface is one typed line"* — was written when a local contract was the only dispatch this chapter
described, and read alone it is now false: it is true of **shape 1 of three**. `dispatch` /
`Invoke-Dispatch.ps1` carries a **local** contract to a background lane; it is not the cloud
transport and not the interactive form. A seat holding a cloud brief takes `Dispatch-CloudV2` from
"Dispatching a session — the boundary, the dispatch table" above. Everything else in this section —
contract mode, the doubled-prefix incident, the effort enum, the execution gate — stands
unchanged, scoped to that one shape.

**The operator's dispatch surface for a local lane is one typed line: `dispatch <contract.md>`.**
It is not a convenience wrapper over a line the operator still has to know — it is the line's
*only* author.
The class this retires is dispatch-line composition by hand: an operator (or a browser seat writing
one for an operator) assembling `--bg`, `--model`, `--effort`, `--worktree`, `--permission-mode`
and a board label from memory, where a dropped constant is invisible until the session boots wrong.

**Witnessed 2026-08-16 (batch 6), on this exact flag.** `--worktree` takes the **bare** lane name,
and the provisioner prefixes `worktree-` **exactly once** — the branch is `worktree-<name>`, as the
parallel-session section above records. A hand-assembled dispatch line passed the intended *branch*
name as the `--worktree` value, so `worktree-lane-a-409-conversions` produced the branch
`worktree-worktree-lane-a-409-conversions`, uniformly across all twelve lanes. Nothing surfaced it
at dispatch: the pre-dispatch grammar check had validated the *intended* names rather than the ones
git created, and the cost appeared only at the integrator's merge queue, where
`batch_manifest.is_lane_merge` matched 0 of 12 and the ADR-110 exemption silently did not apply.
The repair was a uniform rename; `[#531]` is the gate that refuses such a name at creation.

Home: `win-tooling` `scripts/dispatch/Invoke-Dispatch.ps1`, merged `d743937`. **`dispatch` is a
PATH command, not a dot-sourced shell function** — `win-tooling@fb52bf6` (2026-08-11; a
cross-repo SHA, named as one per the citation convention): `scripts/dev-terminals/bin/dispatch.ps1`
plus a `dispatch.cmd` shim for `cmd.exe`, both deployed by
`scripts/dev-terminals/Apply-DevTerminals.ps1` to `$HOME\.dev-terminals\bin`, with that directory
added to the user PATH (HKCU, unexpanded, no elevation). The superseded route —
`config/dev-terminals/dispatch-alias.ps1` dot-sourced by the branded VS Code terminal profiles —
is why the earlier claim here, that `dispatch` was thereby *live in every branded terminal*, did not
hold: that commit body records three dot-source routes and how each covers only part of the machine
(profile args reach 1 of 8 terminal types, and only when picked or default; `CurrentUser $PROFILE`
sits inside the OneDrive - Blue Yonder exclusion zone and cannot be written at all;
`$PROFILE.AllUsersAllHosts` has the right scope but wants an elevated run no agent can perform).
PATH lookup is the shell's own mechanism rather than something each shell has to be configured to
do, so every shell resolves it. The alias, the profile args and `-Global` all still work, demoted to
an optional fallback; the deployed copies are regenerated from source rather than hand-edited.

**Contract mode is the default, and it executes the contract's own line verbatim.** Given a
contract file, the helper looks for a `## Dispatch` heading followed by a fenced code block. If it
finds one, that line **is** the dispatch — run as written, with exactly one substitution: the
literal token `$env:CLAUDE_PROMPTS_DIR` becomes the resolved prompts directory
(`$env:CLAUDE_PROMPTS_DIR`, falling back to `$env:USERPROFILE\Downloads`). The helper does not
re-compose, re-order or top up that line. **That is the point of the whole design** — one source
for the dispatch, authored where the arc is authored, so the line the operator runs and the line
the contract records cannot disagree. A bare filename argument resolves against the same prompts
directory; an absolute path, or a path that exists relative to the current directory, is used as
given.

**Table fallback, for a contract with no `## Dispatch` block.** The helper derives a line from the
contract's `| Model | ... |` and `| Effort | ... |` table rows plus the filename: worktree name =
the filename stem lower-cased; board label = `[<repo> . #<ids> . <verb-object>]`, where repo is the
stem's first hyphen-token, ids the first digit-run, and verb-object the remaining tokens. The
dispatch constants `--bg --permission-mode bypassPermissions` are appended. This path exists so an
older contract still dispatches; a contract written today carries the block and takes the first
path.

**Effort is a CLOSED enum — `{low | medium | high | xhigh | max}` — and a miss is a refusal, not
a guess.** *(Converged 2026-08-22 by architect ruling: the **CLI-validated** enum is canonical and
this surface follows it. `[#539]` reported the divergence — its contract named five values while
this text and the routing matrix named four — and a generator is not where that gets decided.
`max` is a valid effort for a **contract**; whether the routing matrix accepts it is the separate
question the paragraph below answers.)* An effort value outside the enum stops the dispatch with a message naming the enum, so a
typo surfaces at the operator's terminal rather than booting a session at an effort nobody chose.
This is the same posture the routing matrix below takes on `max`: an unroutable value is refused at
the surface instead of being silently rounded to a neighbour.

**The execution gate — a live `claude` never fires bare.** `-DryRun` prints the resolved line and
stops. `-Run` executes it immediately. With neither flag the resolved line is printed and the
operator is asked to confirm (`Execute this live claude --bg dispatch? [y/N]`); anything but
`y`/`yes` refuses — **including empty or non-interactive input**, so a script or an accidental
invocation with no attached terminal defaults to refused rather than to running. Both parameter
sets share this gate, which is the operator rider that closed the gap a real accidental firing
exposed (`win-tooling` JOURNAL 2026-08-08). *Honest limit, worth knowing before relying on it:* the
`dispatch` alias exposes only `-DryRun`, so a live run **through the alias** always goes through
the interactive confirm; `-Run` is reachable by invoking `Invoke-Dispatch.ps1` directly.

**POINTER — the literal commands live in "The dispatch table — the SOLE literal-command site"
above.** This section owns the MECHANICS of the contract-driven surface (contract mode, the
table fallback, the effort enum, the execution gate, the doubled-prefix incident); it no longer
competes with that table on what the operator types. Reach for the table first; read on here when
you need to know why the surface behaves as it does.

**Raw-line composition is the FALLBACK form, and it is not the default.** The helper keeps a legacy
explicit-parts mode (`-Repo -IdOrSlug -VerbObject -Prompt [-Worktree] [-WorktreeName]
[-PermissionMode]`) that composes the same board-label convention from arguments, and a
hand-typed `claude --bg ...` line still works because nothing removed it. Both are recorded here
once, as the form to fall back to when a contract file is not the unit being dispatched — not as an
equal-standing alternative. The composed-by-hand line is the class this section exists to retire,
so reaching for it is a deliberate exception rather than a matter of taste.

**What this means for a contract author.** Every lane or arc contract opens with a `## Dispatch`
block carrying its own literal dispatch line, in the variable form — `templates/prompt-template.md`
is the point-of-use card and shows one literal example line, so the line is *copied*, never
composed. The routing decisions that line carries (model, effort, and the dispatch constants) are
the subject of the section directly below; this section covers only how the line gets from the
contract to a running session.

### Cloud lanes — the receipt gate and the fresh-branch rule
<!-- scope: meta -->

A cloud lane is a dispatch that runs off this machine, on a branch under the `claude/<slug>` lane
prefix. Everything above about contracts, decision budgets, commit-and-STOP and serial integration
applies to it unchanged. Two *rules* apply additionally — the two below — and both exist for one
reason: a remote lane's state is knowable only through what it reports back. A third question,
which lanes are cloud lanes at all, is recorded at the end of this section as owed rather than
answered.

**The receipt gate — two parts, checked as a conjunction**
(`protocols/STANDING_RULINGS.md` Q5). Every cloud dispatch carries one:

- **the git source resolves non-empty** — the lane is attached to a real branch carrying real
  content, rather than to a repo reference that quietly resolved to nothing; and
- **the first assistant text is echoed back** — the session produced output, rather than accepting
  a dispatch and dying before its first turn.

**A dispatch without both is not a dispatch that ran** — Q5's own consequence, in its own
words. What follows from that is the dispatching seat's, and the register leaves it there rather
than prescribing it.

*Why the conjunction, and this is reading rather than ruling.* Each half alone has a failure mode
only the other catches: a non-empty source with no first text is a session that booted against
real code and then died; a first text with an empty source is a session talking about nothing.
Either half read alone reports a success the other refutes.

**Cloud lane hygiene — fresh off `origin/main`, foreign dirty files left as found**
(`protocols/STANDING_RULINGS.md` Q4). A cloud lane branches from `origin/main` rather than from
whatever state a container happened to inherit, so its base is a ref a successor can name and
re-resolve. Foreign dirty files are left untouched: a remote container can arrive carrying
another actor's uncommitted work, and a lane that sweeps those into its own commit hands the
integrator a diff whose authorship the tree no longer records. Q4 admits no carve-out for a file
the lane's own contract happens to name — a file the contract names and the lane then edits is the
lane's own work, not a foreign dirty file, so the two cases do not overlap and the rule needs no
exception to state. This is the batch protocol's file-disjointness rule, applied to a tree the
lane did not provision.

**Which substrate — ANSWERED 2026-08-23 (M10), above.** This paragraph recorded the gap as owed
because the chapter carried no test for which lanes are cloud lanes. "Dispatching a session — the
boundary, the dispatch table" now states one: **the operator's disk vs `origin/main`**. What
follows stays as the *refinement* it always was — a second, footprint-shaped read that agrees with
the disk test in the ordinary case and yields to it where they diverge. The working
distinction in live practice: a lane routes **local** when it wants the local gate mesh — a
`last_reviewed`-stamped canonical file behind the freshness and TOC gates, a hook stack that has
to fire, an interactive credential, or timing the operator is watching — and **cloud** when its
footprint is read-only analysis or a docs-only artifact no local-only gate governs.
`.devcontainer/` ([#554]) is the provisioning half of the off-machine substrate; the routing half
is the boundary above. This paragraph stays a **description of practice**, deliberately outside
the two rules of this section, and `docs/audits/2026-08-20-technical-playbook-status.md` G1 —
which read the routing half as an open gap — is **discharged by the boundary subsection**, not by
this text.

**Honest limits, all three.** The receipt gate and the hygiene rule are prose, checked by the seat
that dispatches and by nothing else. The ADR-110 exemption that grants an open batch its
declared-integration-arc relief keys on a committed manifest and does **not** extend to a
`claude/*` lane — a cloud lane's branch tips are anchored before the merge queue opens, rather
than bypassed. And the transport a cloud dispatch travels on is recorded outside this repo, in
`win-tooling`; this chapter states the gate a dispatch passes, not the client that carries it.

### Model + effort are stated at dispatch — the routing matrix
<!-- scope: hybrid -->

**Ruled 2026-08-07 (architect, batch-2 consolidation arc).** The browser-architect states model
**and** effort on every dispatch it emits; the operator overrides either at the point of dispatch.
The rule is scoped to that one act — the line the operator pastes carries the routing, so a lane's
tier is a decision on the record rather than an inherited default nobody picked.

**The matrix, as ruled** (Model row amended 2026-08-07 — see the amendment directly below):

| Tier | Routes |
|---|---|
| **opus** | **the default for any arc touching `.dev-knowledge`** · M/L arcs anywhere · gate and organ code · architecture · adversarial verification · any arc whose failure poisons downstream work |
| **sonnet** | small **and** self-contained sub-tasks only — read-only quick reviews · sub-agent chores · single-file mechanics carrying no system context |
| **haiku** | retrieval only |

**AMENDMENT 2026-08-07 (operator-ruled, on measured evidence) — the tier keys on CONTEXT LOAD,
not task shape.** As first written, the `sonnet` row read as a *shape* table: S-class bounded
edits and documentation arcs route to sonnet wherever they land. Measurement retired that
reading. **A shape-S arc on sonnet ran ~3h against this repo's gate mesh** (operator
measurement, 2026-08-07) — small by diff, large by the context it had to hold at every step:
`CLAUDE.md`'s twelve sections re-read at each boot, the pre-commit / commit-msg / pre-push stack
of its §9, and `audit.py`'s 41-member `ALL_CHECKS` registry, any leg of which can bounce a commit
and send the session back through the same derivation. A tier picked from diff size prices none
of that in. The routing variable is therefore the **context load the arc carries**, and in
`.dev-knowledge` that load is high by construction — so **opus is the default here**, and sonnet
keeps only the work that is small *and* self-contained. Elsewhere in the fleet the shape reading
still holds; this amendment is scoped to the hub, where the gate mesh lives.

*In-repo corroboration, stated as the bound it is.* The PRE-2 gate-hygiene arc — five inherited
WARNs, no feature work, shape-S by diff — shows 1h40m between its base commit `b669bd8f` and its
first landed commit `e351b685`, and 1h50m base-to-merge (`81d572d7`). Git dates a commit, not a
session, so this is a **lower bound** on derivation time rather than a reproduction of the ~3h
figure; it is consistent with it, and it is the only part of the measurement the tree can carry.

Effort — `high` for multi-file reasoning, design and review; `medium` as the S-class default;
`low` for mechanical single-file work. **`max` stays out of dispatch routing.** Its recorded uses
in this repo are session-level rather than flag-level (`JOURNAL.md` 2026-07-04, the Fable
architecture review; the 2026-06 HANDOFF_PROCESS audit), and the architect's stated reason also
cites a history of the flag being disregarded — a history no in-repo artifact carries, so it is
recorded here as the ruling's rationale rather than as a verified platform fact. The full ladder
and what each rung buys stay at "How to choose Effort" in §2; this matrix routes dispatches, not
the ladder.

**Dispatch constants.** Three items ride every dispatch without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label (shape and rationale directly
above). Checked against the installed CLI (2.1.224): `claude --help` carries `--bg`,
`--permission-mode <mode>`, `--effort <level>` and `--model <model>` as independent flags, so the
matrix above is expressible on the command line exactly as written.

**Ceremony cut, ruled in the same act — the dispatch line is authoritative for model and effort.**
An **S-class contract therefore drops the `Model | Mode | Effort` table**: the line that launched
the session already carries two of its three rows, and a table restating them is a second source
free to disagree with the first. **M- and L-class contracts keep the table**, where the `Mode` row
carries something the dispatch line does not. `templates/prompt-template.md` (v1.10) is the
point-of-use form.

**Declared collision with "Model is CC's pick", and the boundary that scopes it.** The ADR-87
equilibrium — "The two lifelines" § Lifeline 1, restated at §2 "How to choose Model" — puts model
selection on CC's side of the table and keeps the architect out of it. The ruling above points the
other way for one population: the dispatch of a `--bg` lane. The boundary declared here is
population-shaped rather than a reversal — the architect states the tier a *session boots at*; CC
keeps its routing of sub-steps **inside** that session, which is the act ADR-87's row was written
about. ADR-87 is left untouched, and the residual is recorded rather than closed by an edit no
ruling covers: the equilibrium table and its §2 restatement still read as architect-excluded on
the dispatch act itself. Operator item, filed in
`docs/audits/2026-08-07-technical-batch-2-lessons.md`.

### Handoff prep for the next architect — an index, not a restatement
<!-- scope: meta -->

A seat inheriting the architect role needs four things it does not arrive holding and cannot
infer from the tree. Each is written once, elsewhere. **This subsection is the index and carries
no doctrine of its own** — every line below is a pointer, deliberately, because a second copy of
a rule is a second thing to keep true.

**1 · How a dispatch prompt is made.** `templates/prompt-template.md` is the work-lane card and
the point-of-use authority: Scale tiering, the `Mode` row, the board label, the dispatch
constants. Where the prompt file lives, how a dispatch line cites it, and where a lane's
*contract of record* lives instead — "Dispatch prompts and the contract of record" above.

**2 · How model and effort are estimated.** "Model + effort are stated at dispatch — the routing
matrix" above: the matrix itself, the live-CLI flag check behind it, and the declared boundary
against ADR-87's "Model is CC's pick". Rung-by-rung detail stays at §2 "How to choose Effort";
the ceremony consequence (an S-class contract drops the `Model | Mode | Effort` table) is stated
with the matrix.

**3 · How a batch is run.** "The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110)"
above: the five per-lane requirements, the integrator's refuse-to-finish checklist,
JOURNAL-rides-the-branch as the anchoring law, the ≥2-commit integrator-branch shape, and the
process-lane cap. `/lane-boot` boots one lane against it; `/lane-integrate` walks the close-out. The sequence one
lane travels — dispatch, execute, commit-and-STOP, harvest, teardown — is indexed at "The lane
lifecycle — five legs, and where each one is ruled" above, which is also where the harvest leg's
two rules live (push-before-delete; the integrator as gate-of-record for index freshness on lane
material). A lane running off this machine adds two more — "Cloud lanes — the receipt gate and
the fresh-branch rule" above.

**4 · How completion is managed.** Four items, each at its own home:

- **Agent View lists dispatched sessions only** — `protocols/STANDING_RULINGS.md` B7, encoded at
  "Dispatch visibility" above. Operator attention goes to **Needs-input** rows rather than to
  re-reading every row.
- **Packets are batched** — one round-trip carries every item, and single-question trips are
  reserved for ask-class (a)–(c): "2-touch transport, on both seams" above, plus
  `STANDING_RULINGS.md` "The decision budget".
- **The integrator runs once per batch**, serially, from the primary checkout — the batch
  protocol above.
- **WINDOW = BATCH** — the seal (bundle, packet, JOURNAL wrap) fires at true batch boundaries,
  and the batch protocol above records why a mid-batch seal misleads its successor.

**Rulings an incoming seat applies without asking:** `protocols/STANDING_RULINGS.md` — section F
carries the batch-execution set landed 2026-08-07.

**Green-without-predicate, shape (b): cleared-incidentally — order the repair before the merge that would mask it.** A gate cleared as a side effect of another actor's honest bookkeeping has not discharged the obligation it was tracking: the signal is gone and the work is still owed. Witnessed at the batch-4 integration, where a lane's own truthful JOURNAL entry would have cleared an anchor gap the lane did not create — so the integrator landed the repair `ce81d5bd` **before** the W2 merge `c7f4fd92`, deliberately, rather than letting the merge absorb it. The ordering generalizes: when a pending repair and an incoming merge would both satisfy the same predicate, the repair lands first, so the gate reports the repair rather than the coincidence. (Shape (a), *gate-greened-by-diagnosis*, is the mechanical sibling and is routed to an "anchored by mention, not by record" WARN inside `scripts/journal_anchor.py`.)

---

## Ch9. Tier-1 closure loop — usage
<!-- scope: meta -->

Per session: commit work normally, using `closes [#id]` on the commit that **finishes** a backlog item (not `advances` — see CONTRIBUTING; `advances` leaves the item open and invisible to the detector). At session end the `tier1-lifecycle` plugin's `Stop` hook proposes likely closures (`logs/PROPOSALS-*.md`); at the next session start the global `[closures] N proposed` reminder (L0 `surface-closures.ps1`) surfaces the count; run `/review-closures` to confirm and update the backlog. Architecture of the three layers: `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle". **Post-flip shape (hub, ADR-107 step 3 / [#439]):** `tasks/` is the source of truth and `BACKLOG.md` is generated, so closing a row is **not** an edit to `BACKLOG.md` — that edit REDs the coherence gate and the next regen undoes it. Retire instead: drop the task's node from `tasks/manifest.json`, **leave its file in place** as the allocation record with its `status:` set to a terminal value — `closed`/`retired`/`superseded`, enforced by the check (retire-not-delete + terminal status, ADR-107 §6.3), and run `gen_task_tree.py --emit-source`; the row leaves `BACKLOG.md` as a result. The `/review-closures` command branches on whether `tasks/manifest.json` exists, so an unflipped consumer keeps the direct-edit path.

### Propagating a plugin change across the fleet

When the `tier1-lifecycle` plugin source changes in `.dev-knowledge`:
1. bump `version` in `plugins/tier1-lifecycle/.claude-plugin/plugin.json`;
2. `claude plugin marketplace update dev-knowledge-methodology`;
3. per installed repo, `claude plugin update tier1-lifecycle@dev-knowledge-methodology --scope project`;
4. restart the session.

The cache is **version-keyed** — `marketplace update` alone won't refresh at an unchanged version, and `plugin install` no-ops on an already-installed repo (use `update`, not `install`). `--scope project` is mandatory for project-scoped installs. Full reference: `plugins/tier1-lifecycle/INSTALL.md`.

### The methodology↔project boundary (what IS methodology)

Before propagating anything across the fleet you must answer, per surface, **methodology or project?** — WITHOUT searching. The hub is the **root of a decision tree** that classifies every fleet surface, and the boundary is made **machine-readable** so the answer is a lookup, not a judgment call (operator charter; fleet-boundary-matrix Surface 2 / candidate C1).

- **Marker form (Form A).** A methodology span inside a shared doc is wrapped in a fenced region: `<!-- methodology:start id=<id> owner=hub|repo -->` … `<!-- methodology:end id=<id> -->`. `owner=hub` = a universal span that must stay byte-aligned to the hub baseline fleet-wide; `owner=repo` = project-local. Full spec + owner-set + form-vs-floor rationale live in `docs/audits/2026-07-11-technical-fleet-boundary-marker-design.md` (the 11-surface divergence it answers: `…-technical-fleet-boundary-matrix.md`) — not restated here. CLAUDE.md is the first application (grandfathered, #312); the root-file-**set** boundary is #316.
- **The drift organ.** `scripts/boundary_report.py` (read-only, Layer-2) aligns every consumer's `owner=hub` regions against the hub CLAUDE.md baseline by `id` and REPORTS drift — it DETECTS, never prevents (a reporter, not a gate; ruling severity=warn). Unmarked consumers read as `unmarked`, distinct from clean.
- **The sequence.** A boundary question resolves **audit → operator ruling → mechanism**, never ad-hoc: the matrix audit surfaced the divergence, the operator ruled per surface, and each ruling lands as a marker / reporter / carrier — the capture-precedes-construction discipline of ADR-70. New boundary surfaces (`protocols/` as a mandated genre #314, `INSTALL.md` uniform #315) follow it.

---

## Ch10. Two-tier automation doctrine
<!-- scope: meta -->

The canonical layer→job matrix is **ADR-74**; this is its operating-doctrine prose, adopted fleet-wide by **ADR-80**. The organising question is a single axis — **does the organ exercise LLM judgment?** — which splits all automation into two tiers.

**Deterministic automation (no model).** Pre-commit + commit-msg hooks, `audit.py` self-conformance, and the scheduled `fleet_health.py` cross-repo baseline (Windows Task Scheduler → Python directly — **no `claude -p` on the scheduled path**, ADR-76). Posture: **fail-closed on any executing path** (a gate that *can* block a commit does) and **fail-soft on awareness paths** (a surfacing hook that can't run prints nothing and exits 0, never blocking a session). Spans ADR-74 Tiers 1–2 (lifecycle + scheduled baseline).

**LLM-judgment automation.** Any organ that runs a model. Invariant: **always read-only + adversarial-skeptic-filtered + operator-ratified** — it proposes, a skeptic kills false positives, and a human funnel ratifies before anything binds. Nothing it emits is binding unattended. Two delivery forms, both ADR-74 Tier 3:

- **Cloud Routine** — self-contained (clones only its own repo, reads no sibling — ADR-72/73); read-only schema-bound agents + skeptic; output via its **declared channel**: a `claude/<task>-YYYY-MM-DD` branch → PR → the GitHub Action diff-guards and **squash-merges** (compliant-by-design: the single non-merge commit is the *designed* cloud channel, deliberately distinct from the local branch+merge `--no-ff` discipline for human-authored arcs — witnessed 2026-06-07 PR#17). See "Routine/night deployment standard › The outcome loop".
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
3. **Action** — the outcome handler (`.github/workflows/nightly-conformance-triage.yml`): diff-guard + auto-merge / triage on the PR the run opens. **RETIRED by `82227f08`** (`.github/` deleted, 2026-07-08, `closes [#255]`) — the file named here no longer exists; `.github/workflows/` now holds only `report-only-wall.yml`. Described in the past tense from here on, and kept rather than deleted because the mechanism it documents is what the rest of this section reasons about.
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

A cloud runner may produce a **shallow clone**, so a verifier that checks "does commit X exist in history" will falsely report any SHA older than the shallow boundary as **absent** — a false "commit absent" finding, not a real conformance defect. Two guards: (1) the Action set `fetch-depth: 0` so three-dot `base...head` diffs have both endpoints reachable (`.github/workflows/nightly-conformance-triage.yml` — **RETIRED by `82227f08`**; the live carrier of the same guard is `.github/workflows/report-only-wall.yml`, which sets `fetch-depth: 0` for this reason); (2) the `conformance-hub` V1 stage treats SHAs older than the history boundary as **out-of-scope**, not absent (JOURNAL 2026-06-04 "V1 shallow-history guard"). Read a first production raw count with this class in mind (JOURNAL 2026-06-05).

### Cloud-session hub-independence (self-containment)

A cloud Routine **clones only its target repo** (single-repo Linux clone at `/home/user/<repo>/`) and must be **self-contained** — it consults only that repo's own git, living docs, and BACKLOG. **No hub reference is load-bearing on the cloud executing path** (ADR-72, #86 sub-decision 2). The hub `.dev-knowledge` is **private**, which permanently closes ADR-71's "URL-swappable later" hatch *for the cloud case*: a git-source/URL hub would need auth inside the sandbox, which the secrets-boundary stance forbids (treat the sandbox as compromised). So plugin/skill distribution does **not** resolve a private hub in cloud — the `tier1-lifecycle` plugin is **verified inert** there (local-directory marketplace absent on Linux; JOURNAL 2026-06-04, "harmless"), and the `repo: ../.dev-knowledge` pre-commit hooks never fire (pre-commit uninstalled in a fresh clone; a read-only run commits no source). These are inert-**by-design**, not bugs.

The honest catch: that degradation is **silent** (the machinery that would log a no-op is exactly what doesn't run), so the "loud" guard moves to **design/review time** — authoring a cloud spec that reads any `../.dev-knowledge/...` path is a defect a reviewer must catch, and any spec that genuinely needs a hub ref must fail-closed at the consumer/Action layer ("put the code guarantee where the bytes actually flow", above). A future cloud Routine that truly needs hub methodology/tooling at runtime is a **STOP-and-escalate**: it cannot be served for a private hub without publishing a hub subset (an operator data-classification call) or new auth'd infra — do not improvise it in-session (ADR-72 Decision 5).

### What every routine must meet (the operational standard)
<!-- scope: meta -->

A recurring unattended review — local or cloud — graduates to "standard" only when it satisfies **all** of these (ratified by ADR-80):

1. **Self-containment** — consults only its own repo at runtime; no hub reference on the executing path (ADR-72/73; "Cloud-session hub-independence" above). Cross-repo reach is the *local* deterministic baseline's job, not a cloud Routine's.
2. **Declared output channel.** *Cloud:* `claude/<task>-YYYY-MM-DD` branch → PR → Action diff-guard → **squash-merge** (compliant-by-design: the single non-merge commit is the *designed* cloud channel, distinct from the local branch+merge `--no-ff` discipline for human-authored arcs — witnessed 2026-06-07 PR#17). *Local:* the writer commits its own pathspec-bounded output, fail-soft ("Two-tier automation doctrine › Writer policy").
3. **`Routine: <name>` commit trailer** on every automation commit, so routine output is git-indexable and value-reviewable (#123).
4. **Per-stage model pins** — every stage pinned by t-shirt size ("T-shirt model pins"); **no `fallbackModel`** on a pinned stage (it breaks evidence comparability — §2 "Model / effort platform doctrine"). Unpinned fan-out is a bug.
5. **Fail-soft + catch-up posture** — a missed run is tolerated by design: catch-up on next opportunity (local: Task Scheduler "run as soon as possible after a missed start", ADR-76; cloud: the next scheduled night), surfaced at the next SessionStart. No alerting, no wake-from-sleep.
6. **Funnel-review as the consuming contract** — findings are *proposals*; the operator's morning funnel ratifies before anything binds, and records per-routine findings-acted-on vs noise (#123). A routine with no funnel consumer is not deployed.
7. **Evidence gate: n=2 before graduation** — a new routine pattern is codified into this standard only after **two real runs** demonstrate it end-to-end (ADR-74 Footnote B meta-rule). The nightly conformance routine cleared this gate (n=1 red 2026-06-06 → triaged → n=2 clean 2026-06-07, both PR'd into `main`); #84 is the codification that consumed it.

### Night-batch work — the morning-loop wave from the night side
<!-- scope: meta -->

> **Provenance:** source intake #19 **§A** (night shift), U6(a) rider — trigger fired 2026-07-30 (the 2026-07-30→31 night batch ran); landed by arc `0731-g0-groom`. Note the rider is cited as "§B" on four upstream surfaces; the content is **§A** — see that arc's JOURNAL entry.

Distinct from everything above in this chapter: the subsections above govern a **scheduled cloud Routine** (cron-triggered, self-contained, Action-mediated). This governs an **operator-requested night batch** — an interactive orchestrating session that fans out, then stops. Both are unattended writing; only the batch has a human who asked for it that evening.

> **The sequence lives in Ch8.** This subsection carries the night's *doctrine*. The five-phase
> *protocol* — dispatch · manifest · night run · morning adjudication · ledger, each with its
> inputs, outputs and refusal conditions — is Ch8 "The night batch — the batch protocol run
> unattended, in five phases" (ruling X8, intake #60, `[#610]`). Doctrine here, sequence there;
> the two point at each other rather than restating one another.

A night batch is not a new project. It is the morning-loop wave seen from the night side, and existing doctrine already governs most of it: model routing by t-shirt size ("T-shirt model pins"; Appendix B), unattended-writer branch isolation (ADR-84), the Tier-3 propose-only rule, and ADR-105's rule that a routine may not activate without a named consumer. What night work adds is executable, not doctrinal.

**The hard rule: nothing merges unattended.** The night produces proposals and evidence; the morning is the operator plus ONE report. A night lane is branch-only — it does not merge, does not push, does not edit canon, does not close a row, and does not issue a ruling. Every output is UNVERIFIED-UNTIL-LOCAL until a local gate run confirms it. This is the existing propose-only doctrine, stated where it gets tested.

**Three organs a night batch needs** (intake #19 §A items (a)–(c)):

1. a **HOST** — no CI exists, so nightly work runs on the operator's machine or a cloud Routine;
2. a **NIGHT-JOB REGISTRY** — each job declares trigger, scope, consumer, consumption path (the ADR-105 six-field shape, which also converts `[#426]` from a 30-item retrofit into one field per job);
3. a **MORNING RATIFICATION SURFACE** — the consumer whose absence is the root of `[#419]`.

**Shape of a batch.** Opus orchestrates; Sonnet runs bounded probes; Haiku runs read-only fan-out. **Every git mutation stays serial in the orchestrating thread** — parallel writers on one tree corrupt each other. Producer ≠ reviewer holds: an agent that did not write the artifact is less biased toward it. Each workstream lands **one dated report** carrying a named `consumer` and `consumption_path` (ADR-105 discipline), and reports are reports — a night batch does not create standing planning artifacts (`[#443]` rent rule).

**Isolation.** Parallel runs sharing one home directory corrupt each other's session state; each needs its own. A night lane names its branch in a sanctioned machine-produced lane shape (`claude/<slug>`, CLAUDE.md §4) and is not self-merged.

**Honest-limits requirement.** A night report states what it did **not** check. A batch reporting only findings, with no statement of coverage limits, is not a completed batch.

**Two beats learned from the first witnessed batch** (2026-07-30→31, n=1 — this shape has **not** cleared the n=2 evidence gate above, so it is a recorded practice, not yet a graduated standard):

- **Report what you did not check.** The batch's ruled-out lists (e.g. a QA leg that disproved CRLF corruption, byte-vs-char miscounting and sentinel spoofing) were as decision-useful as its findings, and cheaper to act on than a padded finding list.
- **A read-only mandate needs a leftover sweep.** One workstream wrote a working file into the repo root despite an explicit read-only brief. The mandate alone did not prevent it; the cleanup beat is what caught it (CLAUDE.md §5 #9 no-leftovers, applied per-workstream rather than per-session).

---

## Ch12. Definition of done (organs)
<!-- scope: meta -->

Recorded as **ADR-81** (2026-06-09; leg (e) added 2026-07-03). An organ — a plugin, hook, command, skill, workflow, generator, or convention — is **not DONE** until it has all five:

- **(a) a methodology home** — its rule/doctrine written in PLAYBOOK **sufficiently for a fresh
  session to act on it from that section alone** (existence ≠ sufficiency). Verified at the handoff
  articulation gate — *could a new session do this from the section alone?* — not merely "a section
  exists." (Evidence: #107 shipped a worktree section, yet a fresh chat still could not parallelize
  from it — the transmission gap this clause closes.)
- **(b) a deployment path** — a runbook or documented install sequence;
- **(c) a maintenance/refresh cadence** — how it stays current, and how staleness is detected;
- **(d) actual deployment, OR an explicit documented deferral** that names the gap and what remains.
- **(e) functional proof** (enforcement mechanisms) — a mechanism (organ / gate / hook / enforcement rule) is not done on presence or configuration alone. Closure requires demonstrated enforcement-in-effect — a functional proof that the mechanism **fires**: a test observing the gate block/trigger, or an observed in-situ firing, not evidence that the artifact is present or conforms. Presence-conformance is necessary but not sufficient; demonstrated firing is the sufficient condition. (ADR-81 Amendment 2026-07-03, Fable consult #1; generalizes the 2026-06-24 hard-metric amendment from deterministic builds to every enforcement mechanism.)

Stopping at build+test is the **half-feature rot trap**: build-and-test ≠ done — and for an enforcement mechanism, present-and-conformant ≠ done either (leg (e): it must be shown to fire). (The routine-specific analog is "What every routine must meet" above — this is its generalization to every organ class.)

**Worked example — removal-in-effect (P2 / ADR-96 / [#244]).** Leg (e) generalizes from *firing* to *removal*: the deploy **remove leg** is not done on "prune code merged + tests green." It closed on a functional proof that the mechanism **removes** — `ruff-gate` pruned from ai-council (n=1) and verified **ABSENT** by an independent `verify_pruned` (D9, which gates the record so it can never report success with the component still present); a locally-modified target **REFUSED** (hash-guard, no clobber); the non-pruned surface byte-identical. Merged ≠ done; **removed-and-verified-absent = done** — the removal analog of the mesh's enforcing-local ×2 firing proof. Same discipline: presence/merge is necessary, demonstrated effect (here, verified absence + a demonstrated refusal) is sufficient.

**Worked example — enforcement-in-effect across the mesh (Stage-4 / [#238] / ADR-93).** For a **deployed** organ, leg (e) has a second edge beyond firing-in-the-hub: **deployed presence ≠ deployed enforcement.** A hub gate *carried into* a consumer is done only on **enforcement-in-effect in that consumer** — the **configured → armed → proven** progression generalized to the mesh: *configured* (the carrier wrote the hook/script), *armed* (`pre-commit install` ran; the hook is live in `.git/hooks`), *proven* (the Informant's lived-sandbox arc **observed it FIRE** — or ARMED-BUT-SKIPPED on a matching file scope — on a real branch→edit→commit→wrap arc, never merely present-and-conformant). ai-council (n=1, Wave-3) is the worked proof: the mesh organs (`session_end_backpressure`, `canonical_freshness`) measured **enforcing-local**, while two file-scoped hooks measured ARMED-BUT-SKIPPED — the firing witness a single-file arc structurally cannot produce ([#267]). The repeatable **measure → complete → re-measure** loop that makes a future `.dev-knowledge` change re-provable across the fleet is `templates/consumer-onboarding-runbook.md` (pointer — the steps live there, never restated here). Same discipline as removal-in-effect: presence/merge is necessary; **demonstrated enforcement in the consumer is sufficient.**

### Definition of shipped (closure gate)
<!-- scope: meta -->

ADR-81 (a)–(e) above answers *"is this organ a complete organ?"* This answers the adjacent question *"is this work actually shipped, or only prematurely announced?"* — the **"deployment is half the success"** gate (LESSONS 2026-06-10). "Unit tests pass → announce shipped" is the EASY metric; declaring on it under momentum is the recurring premature-closure failure (the floor saga is the worked example). A feature/arc is **shipped** only when ALL six hold:

1. **Git clean + merged** — branch merged `--no-ff` to `main` and pushed; `upstream..HEAD` empty (LESSONS 2026-06-09 /ship-completion).
2. **Version surfaces coherent** — every coupled version surface agrees with its anchor (`audit.py amendment_coherence` green).
3. **An E2E / user-flow test passes** — the whole sequence exercised as a user would, not only unit tests (**#144**).
4. **Checked against the original expectation in a back-and-forth** — reconciled with what the operator actually asked, not a one-shot self-grade (LLM-LLM transfer is bidirectional — see "LLM-LLM context transfer is back-and-forth, not unilateral").
5. **Records updated** — JOURNAL / LESSONS / ADR / archive reflect the change.
6. **The verification organs RUN green** — `audit-health`, `validate_doc_claims` (#89), `validate_git_backlog` (#90a), `canonical_freshness` actually **executed against THIS arc**, not merely existing. Building an organ ≠ running it on the feature it should guard. **"Organs run green" is class-specific:** hard-fail organs (`audit-health`, `amendment_coherence`) exit 0; awareness organs (`validate_doc_claims`, `validate_git_backlog`) surface no new or undispositioned WARN — a documented pre-existing WARN (e.g. a voided closure pending #139) does not block.

Announcing before (2)–(6) is **premature closure**, not shipped. Point (6) is **operator-enforced discipline until #147** wires it as a pre-ship gate (a hook/command that RUNS the organs and BLOCKS `/ship` on red). De-dup: point (3) E2E = **#144**; codification-completeness of the methodology home = **#145**; #147 = the run-organs-as-gate mechanism — three distinct items.

**Review-before-STOP (closure-contract standard step).** The code / second-reader review is a step INSIDE the closure contract, run **BEFORE** the session STOPs — never deferred to the operator as a post-STOP task. Deferred past the session boundary a review becomes the operator's chore and routinely doesn't happen, so defects ship unreviewed; and the second-reader catch is only worth anything while the author can still act on it. The executing session owns the review — `/codex-review` (code, per the §16 lane doctrine) or `/code-review` — as a named step every plan carries and every session runs before handing back. A plan that ends "…STOP; operator reviews" has misplaced the review. (LESSONS 2026-07-12 review-before-STOP; pairs with the two-stage review applicability, Ch4, and the Codex-utilization doctrine, §16.)

**Authored before the build — the ex-ante half (deterministic build tasks).** The six points above are the *ex-post* checklist (at ship time, confirm these held). For a **deterministic build task** there is also an *ex-ante* property: the executable **pass/fail criterion is authored by the architect _before_ the build and frozen** — immutable to the executor (CC may *strengthen* it — add cases, tighten assertions — but **never weaken** the gate: no assertion removal, input-specific branching, or scope-narrowing), so closure is declared on a contract that **predates** the work rather than one reverse-engineered to fit a green run. Review verifies the contract was **not gamed** (assertions intact, scope not narrowed) — green status alone does not close. Proven exemplar: **#194 Phase-A** — the xfail-strict coverage test whose failing output *is* the rollout inventory, committed before any annotation (the xfail-strict decorator made a premature green *fail* — immutability in action). This is the test-first generalization the **ADR-81 amendment (2026-06-24)** records; it is **deterministic-scoped** — the fuzzy band (decks/prose, where "done" cannot reduce to an exact assertion) is deferred to its own arc. **#144** folds the requirement into ADR-81(d).

**Distinct from the per-session close gate:** this "organ done" (ADR-81) and "arc shipped" gate answer *"is this feature/arc complete?"* The adjacent, narrower question *"did THIS session leave the record current?"* has its own single-source — `protocols/DEFINITION_OF_DONE.md` (ADR-85), enforced mechanically by the session-end Stop-hook (JOURNAL SHA-anchor hard block + BACKLOG nudge). Don't conflate the three scopes: organ-completeness, arc-shipped, session-close.

**Vacuous-zero negative control — a measurement already reading 0 is 0 evidence.** Leg (e) above requires that a mechanism be shown to FIRE; the measurement analogue is that a number already reading 0 before the change says nothing about the change, and becomes evidence only once the red is produced deliberately. Worked example from `[#521]`: pre-rollout **0/101**, config-only **0/101**, post-rollout **0/101** — three greens carrying no information, because 77 `sys.path.insert` lines were carrying the imports the whole time. The clause became load-bearing when the roots were narrowed back to `["."]` on the finished tree and **68 of 101** files broke, reproducing `[#502]`'s 67-of-99 on a tree three days newer. So a clause phrased as *"zero X"* is paired with the deliberate production of a non-zero X — the same pairing leg (e) makes between presence and demonstrated firing.

---

## Ch13. Continuous Improvement
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

New tools, models, agents, and patterns emerge constantly in 2025-2026 LLM dev (Claude Code releases, OpenAI Codex updates, Chinese models like GLM/Qwen, MCP servers, multi-agent frameworks, Spec Kit/Kiro). Without explicit process, adoption thrashes (re-evaluating same tool quarterly), forgets context (why did we reject MCP memory?), or misses signals (a relevant tool sits unread for weeks).

This section defines the lifecycle: from "I saw something on Twitter" to "we adopted/rejected/deferred."

### Project-evolution posture (always be improving)
<!-- scope: meta -->

Distinct from the tool-adoption lifecycle below: the default posture for every project. (Moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the one-liner + pointer.)

- Project goal at meta level is continuous development and refinement; specific session goals are immediate scope, the long-term posture is always advancing.
- Static maintenance is the exception and requires explicit declaration in VISION Lifecycle (e.g., archived project, frozen for compliance).
- "Feature-complete" never means "done" — it means "no near-term feature additions planned, but improvement continues."
- Improvements emerge from real usage and lessons, not feature speculation.
- VISION is reviewed at session boundaries; if a Vision section appears realized, propose the next horizon (per ADR-33 lifecycle pattern).

**Applied to per-repo VISION.md:** the Lifecycle section MUST reflect the continuous-improvement posture unless an explicit static-maintenance declaration with justification exists.

Wrong (frozen state implied):
> "Feature-complete v1. Active maintenance. No planned major features."

Correct (continuous improvement implied):
> "Active development with continuous improvement focus. Roadmap reviewed at session boundaries — improvements emerge from real usage and lessons. Static-maintenance posture is exception requiring explicit declaration."

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

#### Step 0 — the ownership check, run BEFORE any research is commissioned
<!-- scope: meta -->

**Filed 2026-08-25 (lane RL) from a measured failure, and deliberately a checklist rather than a
principle.** Three separate instances in one window commissioned research into a question the repo
already answered. The prose form of this rule ("check whether we already own it") was present and
did not fire, because a principle is something a seat agrees with and a checklist is something a
seat executes. So this is the executable form: run these four, paste the output into the intake or
the brief, and only then pick an evaluation mode below. A commissioning that cannot show this
output is not yet a commissioning.

```
# 1. Does a decision already exist? (ADRs, including rejected and parked)
uv run --locked python -c "import pathlib,re;[print(p.name) for p in sorted(pathlib.Path('docs/decisions').glob('ADR-*.md')) if re.search(r'<TERM>', p.read_text(encoding='utf-8'), re.I)]"

# 2. Does a ruling already exist? (the register is the ruled-but-not-ADR surface)
grep -n -i "<TERM>" protocols/STANDING_RULINGS.md

# 3. Does an open row already own it? (tasks/ is the source of truth, not BACKLOG.md)
grep -rn -i "<TERM>" tasks/

# 4. Has it already been evaluated and rejected? (the Rejected list is a real surface)
grep -n -i -A3 "<TERM>" protocols/ENVIRONMENT.md
```

**Reading the output.** A hit in (1), (2) or (4) means the question is answered — the honest next
act is to cite it, not to re-open it, and re-opening requires new evidence stated as such. A hit
in (3) means an owner exists and the work is attaching evidence to that row rather than birthing
a second one (ADR-111's OWNED outcome). Four clean misses is the only state in which
commissioning research is the cheapest way to learn the answer.

**Why this is Step 0 and not advice.** The cost asymmetry is measured, not assumed: the four
commands above run in seconds, and the research they can pre-empt is a Scale-L Council debate or a
half-window of a lane. Research-as-procrastination is the failure this closes — see `LESSONS.md`
2026-08-25.

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
- Output: canonical transcript in `ai-council/output/` (routed-mirror retired 2026-07-22, ADR-43 amendment 2026-07-23; `docs/research/` retired per ADR-60 amendment 2026-05-27)

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
- **ADRs** in `docs/decisions/` — the adopt/reject decision itself (research-mode debate transcripts stay canonical in `ai-council/output/`; routed-mirror retired 2026-07-22 per ADR-43 amendment).
- **BACKLOG** "Tooling & evaluation" theme — deferred tool evals carrying their reopen triggers (e.g. Kimi K2).
- **JOURNAL** — the per-session record of what was evaluated and decided.

**Mechanism-class-before-more-fixes.** Four consecutive repairs of the dispatch helper each addressed a symptom inside a mechanism class — a profile-sourced shell alias — that was wrong for the machine it ran on. The recurrence ended when the **class** changed, to a PATH command with `-Check` guarding, rather than when a better fix landed inside the old class. The recognition signal is the third repair in the same family: at that point the cheaper question is which class the mechanism belongs to, not which detail is broken. Not mechanizable as stated — a checkable proxy would need a register of repair-attempts-per-mechanism that does not exist — so it is a diagnosis posture rather than a gate.

**A literal is not a site.** A pattern occurrence inside *generated source for a subprocess* is data, not an instance of the thing being swept, and a mechanical sweep that treats the two alike breaks what it was tidying. Witnessed on the `sys.path.insert` sweep: `tests/test_batch_manifest.py` carries three occurrences and only two are sites — the third lives inside the `_SHADOW_PROBE` string literal that generates source for a subprocess carrying no pytest `pythonpath`, so sweeping it would have broken the probe. Same class as the residual exempted at `tests/test_enforcement_coverage.py:389`. A sweep step therefore reports occurrences inside string literals separately from occurrences at statement level — a contract-time check, not an organ.

### The window mandate — what a window owes, and what it is allowed to carry
<!-- scope: meta -->

**Filed 2026-08-25 (lane RL).** Two rules about the shape of a window, landed together because
they are the same measurement read twice: a window that spends itself entirely on its own
machinery produces no consumer-visible change, and an intake surface with no cap absorbs that
pressure silently instead of surfacing it. Each carries its own status, and the statuses differ —
stating them as one ratified block would be the overclaim this file exists to avoid.

**(1) Governance/product parity — STATUS: PROPOSED (not ruled).** The proposal is that every
window carries **at least one consumer-facing arc** alongside its governance work — an arc whose
output a fleet consumer can observe, as distinct from an arc that improves how the hub governs
itself. The evidence it rests on is the 2026-08 window record: governance arcs outnumber
consumer-facing arcs there by a wide margin, and no organ notices. It is recorded here as
PROPOSED rather than adopted because the ratio a window *should* hold is an operator question
about what the fleet is for, and this file does not get to answer that by writing it down. A seat
citing this as binding is citing it wrong; until it is ruled it informs planning and gates
nothing.

**(2) C12 icebox cap + one-in-one-out — STATUS: RULED-ADOPTED (operator, 2026-08-25).** The icebox
carries a **cap**, and past the cap admission is **one-in-one-out**: landing a new icebox item
requires naming the item it displaces. This is the same filing-backpressure doctrine the
`backlog-filing-backpressure` commit-msg hook already enforces for BACKLOG task ids
(`kill-candidates:` on every add), applied to the surface that had no such pressure. Its purpose
is not tidiness — it is that an uncapped icebox lets a window defer decisions at zero cost, which
is indistinguishable from making them and produces a queue nobody ever reads.

**Honest limit, stated because the pair reads stronger than it is.** Neither half has an organ
today. (1) is unruled and so has nothing to enforce; (2) is ruled but its cap is not yet a number
this file names, and no check counts icebox members or refuses an uncapped add. Mechanizing (2)
is the natural sibling of `scripts/check_backlog_filing.py` and is owed; until it lands, the rule
binds the seat and not the tree, and saying otherwise would be the paper-enforcement class
recorded elsewhere in this chapter.

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

### The intake pipeline — intent → intake doc → decomposition → epic lanes (ADR-98)
<!-- scope: hybrid -->

Where a formal prompt comes **from**. Before anything below is authored, a new initiative runs the ratified intake pipeline (ADR-98) — three roles, each a boot **mode/profile** of `scripts/gen_handoff.py`, one chain:

1. **Functional architect** (`--mode functional`, HANDOFF_PROCESS.md §16) — a fluid conversation that captures the operator's intent as an **intake doc** (WHAT/WHY: problem, scenarios, requirements, **ex-ante acceptance criteria**). Confirm-gated: the operator approves the draft before it lands in `docs/intake/` (format + lifecycle: `docs/intake/README.md`; feeds like `/changelog-review` drop `status: SEED` candidates into the same folder).
2. **Technical architect** (`--mode architect`, HANDOFF_PROCESS.md §13) — triages the confirmed intake doc (accept / defer / reject), then decomposes: BACKLOG epics (ADR-66 story-map, each citing its intake-id + ADR ids), any ADRs the initiative forces, and one §14a epic handoff per parallelizable epic. The prompt-authoring spec below is this role's output surface.
3. **Developer** (`--mode developer`, HANDOFF_PROCESS.md §14 — the additive alias of epic mode, ADR-98) — executes one epic lane end-to-end; UAT at EPIC RETURN = the intake doc's acceptance criteria **verbatim**; go-live = root merge.

**Terminology (defined here, once — cross-referenced, never synonyms):** **developer = the mode/profile** (the boot contract a chat runs under); **epic lane = the unit of work** (one epic · one root-provisioned worktree · one browser chat; ADR-97). A developer *works on* an epic lane. Other sections and specs point back here rather than re-defining.

**Genre demarcation (ADR-98 §3):** intake doc = **WHAT/WHY** (0..1 per initiative) · ADR = **the DECISION at a genuine fork** (0..n per intake) · backlog epic = **the WORK** (1..n per accepted intake). Acceptance criteria copy **verbatim** from intake doc → epic UAT; the intake↔epic edge stays advisory until n=2 docs are consumed end-to-end (ADR-98 §5). Corporate mapping: blueprint = intake doc · implementation = epic lanes · UAT = the EPIC-RETURN acceptance check · go-live = root merge.

### Architect output vs CC consumption-spec
<!-- scope: hybrid -->

Per **ADR-87** (the architect↔CC equilibrium contract). STEP 1 verified CC self-loads context **reliably only for code-impact tasks**; read-only, governance-context, and execution-time gotcha self-load are unreliable. So the labor splits **per the canonical equilibrium table — "The two lifelines" § Lifeline 1** (architect emits *intent · closure · anti-patterns · mode · a thin governance-pointer*; CC owns *code-impact context · generic gotchas · the skeleton · model/effort*). Not restated here; the prompt-authoring nuances that table does not carry follow:

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

**Model is CC's pick** (see "How to choose Model" below); **Mode and Effort are the architect's** (Effort set by token budget). The architect does not choose Model.

### How to choose Model
<!-- scope: llm -->

**Model is CC's pick, not the architect's** (canonical: "The two lifelines" § Lifeline 1) — default **Opus 4.8**, the floor (see "Model / effort platform doctrine" below); CC may route a mechanical sub-step smaller. The architect does not set the model; **effort is the architect's**, keyed to token budget. CC's routing heuristic:

- **Sonnet** for: mechanical work ("apply this fix"), single-file edits, well-specified implementation, pattern-matched code, boilerplate, file renames, config updates, code-and-test loops where the spec is detailed.
- **Opus** for: audit / review / synthesis tasks; architecture decisions and clause-level reasoning; judgment-heavy work (severity calibration, ambiguity resolution); long-context comparison across multiple inputs; subtle pattern recognition (security review, gotcha identification); multi-package changes; complex debugging; novel logic design.

Rule of thumb: "do X the way we always do it" → Sonnet; "figure out the right approach, then do it" → Opus. No budget ceiling (LLM-spend rule); when uncertain, lean Opus — Sonnet's failure modes (missed nuance, factual misses) cost more than Opus's overhead.

**Scope note (2026-08-07), reciprocal.** This heuristic covers CC routing its own sub-steps
*inside* a running session. **Dispatching** a `--bg` batch lane is a separate act under a separate
ruling — the architect states model and effort on the dispatch line, and the operator overrides:
Ch8 "Model + effort are stated at dispatch — the routing matrix", which declares the boundary
between the two populations and records the residual this section carries.

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

**Scope, declared 2026-08-06.** These three values are the governed vocabulary, and `plan-then-auto` is the default stated above for most multi-step prompts. `templates/prompt-template.md` (v1.7) carries a separate **execution** default for *work-lane* prompts — the pasted-frozen-contract case where the contract itself is the plan (intake #25 `AMENDMENT 2026-08-05-c` c2). `execution` there is a work-lane label for that case, **not** a fourth value in this vocabulary; the term is already taken twice in this corpus (the handoff boot-mode at `:3148` / `gen_handoff.py --mode execution`, and the field name "Execution MODE" at `HANDOFF_PROCESS.md:704`). Where the populations meet, **this section governs**; the card is the point-of-use authority for work-lane prompts only.

### How to choose Effort
<!-- scope: hybrid -->

- **low** — single file, <30 min, no architectural decisions. Example: "add a CLI flag", "fix this test", "rename this variable across the file"
- **medium** — 2-5 files, 30-90 min, may involve design choices within known patterns. Example: "add a new CLI command", "refactor this module to use dataclasses"
- **high** — 5+ files or 2+ packages, 90+ min, requires UNDERSTAND phase, potential blast radius. Example: "implement search federation", "migrate classifier to new taxonomy"
- **xhigh** — hardest debugging, end-to-end pipeline verification, Council-level analysis. Opus only. Example: "find why magistrala silently drops events", "verify boundary enforcement across all packages"
- **max** — the top effort rung above `xhigh` (live effort ladder: `low / medium / high / xhigh / max`). Reserve for the hardest single-session synthesis where even `xhigh` under-resolves; burns the most tokens, use deliberately.

### Model / effort platform doctrine (Claude Code 2.1.x)
<!-- scope: hybrid -->
<!-- last-verified: 2026-07-06 -->

Platform-current facts that pin the tables above (Claude Code 2.1.202; refreshed for #84 from `docs/audits/2026-06-07-platform-max-audit.md`; Sonnet-5/XL refresh 2026-07-06, Arc 5 — `docs/audits/2026-07-06-changelog-review.md` A1 + ADR-70 amendment 2026-07-07). The pins below are dated by the `last-verified` stamp — re-ground them against `claude --version` and the live tool schemas before trusting:

- **Opus 4.8 is the default model and defaults to `high` effort.** Don't treat "use Opus" as exceptional for judgment work — it's the floor. Reserve the explicit Effort knob mainly for moving *off* `high`.
- **The Sonnet/M tier is Sonnet 5 (`claude-sonnet-5`).** The CC platform default since 2.1.197 (native 1M-token context); verified live on our install 2026-07-06 (accepted, no deprecation warn — the prior `claude-sonnet-4-6` is still active, so the A1 pin refresh was discretionary, ratified GO). Every "Sonnet" row in the tables above means Sonnet 5; the t-shirt size pins themselves are unchanged (S=Haiku / M=Sonnet / L,judgment=Opus).
- **XL = Claude Fable 5, browser-architect layer ONLY (ADR-70 amendment 2026-07-07).** Adjudication, multi-document synthesis, and ratification sessions at the browser layer route XL. It is **not a fourth CC-side fan-out size** — the S/M/L fan-out pins stay untouched (amendment Decision 2). Conditional on current pricing/availability; coarse availability fallback = Opus. Anti-conflation (mandatory, amendment Decision 4): that Opus fallback is an interactive browser-layer availability fallback, **not** a `fallbackModel` on a pinned stage — the ADR-80 §5 pinned-stage `fallbackModel` ban is untouched.
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
LEGEND  [A] = architect emits  ·  [CC] = CC self-loads  (per "The two lifelines" § Lifeline 1)

[A]  TARGET-REPO: <absolute path>   <- cross-repo prompts ONLY: first line, above the table
                                       (Ch4 pre-send checklist)

| Parameter | Value  |   <- Mode + Effort are [A]; Model is [CC]
| --------- | ------ |
| Model     | [pick] |
| Mode      | [pick] |
| Effort    | [pick] |

[A]  TITLE: What we're doing
[A]  REPO: Which repo/package   <- same-repo prompts; TARGET-REPO supersedes it cross-repo
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

### Multi-agent / fan-out prompt checklist (the browser-emitted mandate contract)
<!-- scope: hybrid -->

The Structure skeleton above is single-session-shaped. A prompt that fans out to more
than one agent, worktree, or repo (a night-audit run, an ARC-scale multi-leg mandate, a
parallel-epic dispatch) additionally states these seven items — generalizing HANDOFF_PROCESS
§14a's EPIC-handoff checklist to any multi-agent mandate, chat-native or generated:

1. FAN-OUT SHAPE — how many agents, at which model tier each (Opus orchestrator / Sonnet
   / Haiku, or the t-shirt pins), and whether they run parallel or serial.
2. WORKTREE + BRANCH — the absolute path and branch name for every side-effecting agent
   (or an explicit "no worktree — tree must be clean" fallback declaration; the #353
   boot-contract precedent). No agent acts on an undeclared worktree.
3. READ-ONLY vs WRITE SCOPE — per agent: read-only, or write-scoped to a named
   file/dir set (the §14a FILE-BOUNDARY shape). Any write that crosses a repo boundary
   MUST cite the RULING-W path (consumer worktree/branch → report; ADR-36 Amendments) —
   never an unmediated write into a live consumer checkout.
4. CODEX LANE — which lane (sol/terra/luna), if any, reviews each leg, named per task,
   not as a shared risk caveat; note known quota/availability volatility if applicable.
5. PLAN-MODE BASIS — the MODE (plan / plan-then-auto / auto-accept, per "How to choose
   Mode") AND its basis, declared per agent/lane — no agent inherits a mode from a prior
   prompt (§14a item 7, generalized).
6. DELIVERABLE NAMING + LOCATION — the exact output path(s) each agent must write to and
   the naming grammar it follows (e.g. the ADR-101 `<date>-<class>-<slug>.md` audit
   grammar), stated ex-ante, not left to the agent to infer.
7. CLOSE DISCIPLINE — what "done" looks like for the mandate as a whole: how per-agent
   outputs get consolidated/integrated (serial merge from primary / operator digest /
   `/ship`), and the escalation rule (§14a items 5-6: a genuine fork or boundary breach
   STOPS and returns to the architect — it is never silently absorbed by an agent).

Applies whenever §2 "Decision scope for when to write a formal prompt" already requires a
formal prompt AND the mandate spans more than one agent/worktree/repo. A single-session,
single-worktree prompt stays on the existing Structure skeleton unchanged.

**Boundary with Ch8:** WHETHER a parallel *committing session* launches at all is not this
checklist's question — that is Ch8's four-condition launch test ([#441]). This checklist governs
the CONTENT of a multi-agent mandate once its shape is chosen; the per-lane ex-ante destination
declaration it presumes is HANDOFF_PROCESS §13's destination contract (intake #18 A4).
*(Adopted verbatim from the s7 draft, `docs/audits/2026-07-19-technical-night-s7-prompt-authoring-quality.md` §4,
at the intake #18 ratification 2026-07-30 — A4 item 1.)*

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
- **Multi-prompt sessions:** if the browser generates 3+ prompts for one feature, check for overlap before running — duplicate context wastes tokens and creates conflicting diffs. (Moved from ESSENTIALS 2026-07-05, [#258].)

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

**Prove, then codify (intake #16 §5 rule 3).** Working discipline enters PLAYBOOK **after it has shipped once — never as a substitute for shipping.** A practice written up before it has survived a real end-to-end run is a plan wearing doctrine's clothes: it codifies what we *intended* to do, and the codification itself then reads as progress. That is the plan-without-ship failure the 2026-07-21 `assets/` delivery broke after 3–5 sessions of it — and why the delivery loop (§21) was owed only *after* that run, not during the sessions that designed it. The threshold here is **one shipped run**, which is deliberately *lower* than Ch11's routine "evidence gate" (**n=2 before graduation**) — a routine must prove it repeats; a working practice need only prove it happened at all. Corollary: when a lane wants to write up a **working practice** it has not yet run, the honest move is to run it and file the write-up, not to write it up and file the run.

**Not in tension with "mechanism before act" (Ch8, RULING-W).** The two rules govern **different objects**, and the corollary above is deliberately scoped to *working practice*, not to Ch8's sense of *mechanism*. *Mechanism-before-act* governs **authorization** — a hub→consumer write needs its sanctioning amendment landed *first*, because the amendment is what makes the act legitimate at all; that amendment is a permission, and permissions cannot be earned retroactively. *Prove-then-codify* governs **working discipline** — how a practice becomes doctrine, which is a claim about evidence, not about permission. Where both bear on the same consumer leg the order is: **land the authorizing amendment → run the leg → codify what the run taught.** The amendment is not the doctrine, and the doctrine is not the permission.

---

## 5. Running an AI Council Debate
<!-- scope: llm -->

**Council debates are valuable but can become procrastination.** Hard rule: max 2 debates before implementation starts. Full format guide lives in the council project's docs/ folder.

> **End-to-end operational lifecycle:** see `protocols/AI_COUNCIL_PROCESS.md` (six stages: frame → author → route → debate → verdict → ADR → close), the prose companion to the AI Council debate pipeline in `ARCHITECTURE.md` (Ch6 decision-flow, compact text — Mermaid left canonical docs per the ADR-51 amendment 2026-07-05). This section gives the *when* and the format summary; the runbook gives the full *how* with gate checks, troubleshooting, and code-grounded references.

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
3. Transcript stays canonical in `ai-council/output/` — no archival/copy step (routed-mirror retired 2026-07-22, ADR-43 amendment 2026-07-23)
4. Add the ADR row and traceability entry to `docs/decisions/README.md` in the same commit
5. Never reopen a decided topic unless new evidence appears

### Council Debate Archival Protocol (RETIRED 2026-07-22)
<!-- scope: llm -->

**This protocol is RETIRED** (operator ruling 2026-07-22; ADR-43 amendment 2026-07-23). The hub archive `docs/decisions/transcripts/` was deleted (`b4435fad`) and the routed-mirror mechanism retired as fleet doctrine — there is **no transcript archival step, manual or routed**. The transcript stays canonical in `ai-council/output/`; the binding record of a Council decision is its ADR ("Post-debate protocol", above). Git history retains the pre-retirement archive and the full manual pipeline this section used to carry; the ADR-77 immutability guard on the deleted zone stays armed (re-creation refusal). Config-side disarm of ai-council's routing is tracked [#401].

### Council output convention (canonical-only since 2026-07-22)
<!-- scope: meta -->

AI Council CLI writes the canonical transcript to `ai-council/output/` — the **only** landing
zone. The former ADR-43 routed-mirror (`target-project:` / `--target-project` → a copy in
`<target>/docs/decisions/transcripts/`) is **retired** (ADR-43 amendment 2026-07-23; operator
ruling 2026-07-22): do **not** set `target-project`. The mechanism still exists in ai-council
code and `settings.yaml` until [#401] lands the config-side disarm — a stray `target-project:`
run would re-create the deleted hub folder as untracked files ([#401]'s hazard half); if that
appears, do not commit it. The decision record is the ADR; the transcript is evidence, cited
by filename from `ai-council/output/`.

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

Both paths **converge on the same invariant**: the ADR is generated and committed *in Claude Code* — never hand-pasted from browser chat into the repo (§8 "Artifact generation direction"; LESSONS #8) — numbered, frontmatter-stamped, and **immutable thereafter** (changes go through "Amendment vs Reopen", below).

### Amendment vs Reopen Decision Protocol
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

When validator/tooling reality contradicts an ADR's prescription, two paths exist: amend in place (preserve intent, update prescription) or reopen the decision (intent itself was wrong). This protocol decides which.

The pattern emerged organically 2026-04-24 (three ADR-27/29 amendments in sequence — see the Examples table below).

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

Codex code review (OpenAI's read-only reviewer) produces findings in terminal output during a session. Without explicit archival, findings disappear when the session ends. This protocol captures Codex output as a durable artifact — the durable-record discipline the (now-retired) Council Archival Protocol above used to carry for debates; a Council decision's durable record is its ADR.

**Pattern parallel to Council record-keeping:** Council debates → their ADR (canonical transcript in `ai-council/output/`; the transcript-archival protocol is retired 2026-07-22). Codex reviews → `docs/audits/YYYY-MM-DD-codex-{slug}.md`.

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

Example (illustrative, not a real file): `docs/audits/2026-04-22-codex-handoff-process-rewrite.md`

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
2. Prepend a JOURNAL.md entry if files changed (CHANGELOG retired — §14). Structure: `### YYYY-MM-DD — <session topic>` header, then bullets — `- Did:` what was actually done · `- Result:` outcome / state on disk · `- Changes:` what files / areas moved (this is the change record — there is no CHANGELOG) · `- Abandoned:` items deliberately dropped (each non-trivial drop also gets a short note in `docs/decisions/`; do not record reasoning inline in JOURNAL) · `- Next:` follow-ups
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

Canonical: `protocols/HANDOFF_PROCESS.md` §2 (the **residual** CC emits) + §5 (the teeth-y **probe manifest**) + §13 (the `architect | execution` modes). Not restated here — a resident copy is the drift this section names as its own failure. (The historical v4 8-file bundle is superseded; preserved bundles in `docs/handoffs/` are point-in-time history.) Upstream of every handoff: where initiatives *enter* is the intake pipeline — Part II §2 "The intake pipeline" (ADR-98; HANDOFF_PROCESS.md §16 functional mode).

### How to hand off — which mode, what to type (operator runbook)
<!-- scope: meta -->

**Single home for "which handoff mode, and what exactly do I type."** Every mode is one
generator — `scripts/gen_handoff.py --mode <mode>` — run from the repo root. The command
help (`.claude/commands/handoff.md`) carries the same invocations at the point of use;
`protocols/HANDOFF_PROCESS.md` §13 and `docs/handoffs/README.md` point here, not copy.
`HANDOFF_PROCESS.md` is the *mechanics*; this table is the *copy-paste*. (Consuming a
generated bundle — booting the browser from it — is the separate `docs/handoffs/README.md`
runbook.)

| Mode | Use it when | Type exactly (from repo root) | Generates in `docs/handoffs/<slug>/` | Paste |
|---|---|---|---|---|
| **architect** | Planning / reshaping the way-of-working — weigh design tensions, drive the decomposition (§13) | `python scripts/gen_handoff.py --mode architect` | `SUPPLEMENT.md` · `HANDOFF_BOOT.md` · `RESIDUAL.md` · `PROBES.md` · `PASTE_THIS.md` | `PASTE_THIS.md` (one paste) into a fresh Claude.ai chat |
| **execution** *(the default)* | Advancing a named backlog item — reactive execute-and-verify (§13) | `python scripts/gen_handoff.py --mode execution` | `HANDOFF_BOOT.md` · `RESIDUAL.md` · `PROBES.md` · `PASTE_THIS.md` (no supplement) | `PASTE_THIS.md` (one paste) |
| **epic** | Spawning one epic lane in a root-provisioned worktree (§14a) | `python scripts/gen_handoff.py --mode epic --epic-slug <epic-slug>` | `EPIC_BOOT.md` · `PROBES.md` · `EPIC_RETURN.md` (no `PASTE_THIS`) | `EPIC_BOOT.md` + `PROBES.md` into the fresh epic chat |
| **developer** | Additive alias of **epic** (ADR-98 — the go-forward executor name; §14) | `python scripts/gen_handoff.py --mode developer --epic-slug <epic-slug>` | Byte-identical to **epic** (`{{MODE}}` renders `epic` until the deferred naming flip) | Same as epic |
| **functional** | Requirements intake — capture WHAT/WHY into an intake doc, **no probes** (§16) | `python scripts/gen_handoff.py --mode functional` | `FUNCTIONAL_BOOT.md` (one file only) | `FUNCTIONAL_BOOT.md` alone into a fresh functional-architect chat |

*(architect | execution are the two §13 residual profiles; epic + developer share one bundle; functional is the §16 intake boot — the four bundle shapes.)*

**`--epic-slug <epic-slug>`** (epic / developer only) names the epic: it sets the lane
branch `epic/<epic-slug>` and worktree `epic-<epic-slug>`. Kebab-case, no spaces; tie the
backlog id in for traceability; defaults to the bundle slug if omitted. In PowerShell,
single-quote it so nothing in the value is parsed — `--epic-slug '278-test-suite-hygiene'`.

**Optional (all modes):** `--slug <name>` overrides the bundle folder (default
`<date>-<repo>-<mode>`); `--repo <name>` / `--date YYYY-MM-DD` override the display name /
date; `--no-assemble` skips `PASTE_THIS.md` (architect / execution only). For
architect | execution the richer interview + strategic-supplement lifecycle also runs via
the `/handoff` command ("please create handoff for dev-knowledge" → fill answers →
"complete handoff for dev-knowledge").

**Worked example — an epic handoff for story #278 (the test-suite-hygiene epic):**

```
python scripts/gen_handoff.py --mode epic --epic-slug 278-test-suite-hygiene
```

writes `docs/handoffs/<today>-dev-knowledge-epic/` holding `EPIC_BOOT.md` (the scope
contract, branch `epic/278-test-suite-hygiene`), `PROBES.md`, and `EPIC_RETURN.md`; paste
`EPIC_BOOT.md` + `PROBES.md` into the fresh epic chat.

### Roles
<!-- scope: meta -->

Canonical: the architect↔CC **division** is the equilibrium table in **"The two lifelines" § Lifeline 1** (ADR-87); the v5 actor table / browser operating role are `protocols/HANDOFF_PROCESS.md` §1 / §7. The fuller **Does/Does-NOT** lists + three-layer flow (ADR-28) live below — moved from ESSENTIALS 2026-07-05 ([#258]); ESSENTIALS keeps the day-to-day frame + pointer.

Two distinct LLM contexts collaborate on every workstream. Mixing them = chaos.

**Browser chat (architect)** — strategic thinking, decisions, prompt generation, conversation that won't survive across sessions.

Does:
- Discusses design, architecture, trade-offs with Rob
- Writes downloadable `.md` prompts for Claude Code
- Reviews Claude Code session summaries, decides next step
- Holds context across one session (not across sessions)
- References `.dev-knowledge` documents when uploaded

Does NOT:
- Touch any repo file directly (no filesystem access)
- Run commands, tests, or git operations
- Persist memory between conversations
- Make state-changing decisions without Rob's confirmation

**Claude Code (executor)** — execution, file changes, commits, validations, testing.

Does:
- Reads CLAUDE.md on session start (auto). Codex reads CLAUDE.md via project_doc_fallback_filenames. the per-repo agent-instruction contract is `AGENTS.md` + `CLAUDE.md` with one importer (ADR-115 superseding ADR-53 D2); the handoff process does not narrate or manage either
- Executes downloadable prompts from browser chat
- Modifies files, runs tests, commits, branches
- Reports session summary back to Rob
- Has filesystem and shell access

Does NOT:
- Make architectural decisions without explicit prompt instruction
- Skip pre-commit hooks or validators
- Push to remote without Rob's confirmation
- Operate without a clear prompt — "improvise" is forbidden

**Three-layer flow (per ADR-28):**

```
Browser chat (analysis)  →  .dev-knowledge (reference)  →  projects (execution)
                                  ↑
              both sides read .dev-knowledge for universal rules
```

- **Information flow:** bidirectional (browser ↔ .dev-knowledge ↔ projects)
- **Execution flow:** one-way (browser produces prompts → Claude Code executes in projects)
- **No shortcuts:** browser does not edit project files; Claude Code does not redesign architecture

**When in doubt about which role applies:** "Should we...?" → browser (decision) · "Implement X per spec" → Claude Code (execution) · "What did we decide about Y?" → either, but check `.dev-knowledge` first.

### Architect epistemic discipline: explicit verification markers
<!-- scope: meta -->

The browser-chat architect distinguishes three claim categories explicitly in handoffs, summaries, and any factual statement about repo state or prior work (moved from ESSENTIALS 2026-07-05, [#258]):

- **Witnessed** — directly observed by the architect (read a file, ran a command, saw a transcript)
- **Inference** — derived from witnessed evidence but one step removed (e.g. "test must pass because the commit message says so")
- **Unknown** — not verifiable from current context

Bundle-asserted facts (SHAs, file counts, version pins, prior session claims) are never propagated as Witnessed unless the architect actually verified them. Default for any claim arriving through a handoff bundle is Inference at most, Unknown if not corroborated.

Sourced from LESSONS #1 (2026-05-12). Architect-side enforcement is operator review; ADR-45 Stage 3 verification provides mechanical cross-check on executor side. Companion executor-side discipline: Ch2 "LLM-LLM context transfer is back-and-forth, not unilateral" (verify inline, ask back; don't carry forward unknown).

**An off-repo claim carries a locator or is marked as paraphrase.** The ladder above says what a claim *is*; this says how it is *written*. Any claim about repo state originating outside the repo — browser chat, a brief, memory of a prior session — is quoted with a locator (`path:line`, a SHA, a command's output) or explicitly labelled a paraphrase. Unlabelled, it enters the next contract as fact and is thereafter defended rather than checked. Two instances propagated into briefs across two days in 2026-08: `67863180` asserted as an ADR-109 §4 discharge (its own merge body records the "9 governs" Related-line gloss; §4 discharged once, at `1afd9579`), and "Act-1 lossless union" asserted as a repo phrase (the referent `55733ea4` unified three runs of one day inside the lane, not two lineages).

**Prompt-premise pre-flight.** Every locator, path, section name and SHA in an emitted contract is verified read-only **before** the contract freezes. A frozen contract resting on an unverified premise forces the executor to choose between an unsatisfiable criterion and a silent reinterpretation — and the reinterpretation is invisible in the result. Pre-flight is a grep per locator, run once, against the tree the contract will execute in. The executor-side counterpart is STOP-and-report, not reinterpretation.

### Architect epistemic discipline: completion claims require state verification
<!-- scope: meta -->

Before declaring a session, directive list, or task "done" / "closed" / "complete", the architect verifies against actual state — BACKLOG residuals, untouched scope items, files modified but not committed, things mentioned earlier in chat that were never resolved. Pattern-matched "all done" framing from prompt structure alone is not evidence; it's a failure mode. (Moved from ESSENTIALS 2026-07-05, [#258].)

If the architect cannot verify completion (no filesystem access from browser chat), the claim becomes a question: "based on what I see here, X and Y look complete; please confirm Z is also done before I declare closure."

Sourced from LESSONS #2 (2026-05-12). Architect-side enforcement is operator review; the ADR-45 shared validator was never implemented — enforcement is operator review only.

**Discharge with evidence — closure names its artifact.** The Witnessed / Inference / Unknown ladder above governs *claims*; this governs *closure*. Every item declared done discharges against a **named evidence artifact** — a SHA, a command's actual output, or the operator's own eye — cited at the point of closure, not gestured at. "Tests pass", "it's merged", "that's handled" name no artifact and discharge nothing.

**Witnessed is the operator's eye or a mechanical report — never a proxy** (intake #16 §5 rule 4). The proxy this rejects is **unsupported self-attestation** — "I verified it", "it's working" — which is Inference wearing Witnessed's label. It does **not** disqualify CC's state-verification reports: captured command output, a gate's actual verdict, or a cited SHA are exactly the *mechanical report* half of the rule, and the architect assessing them is the sanctioned evidence path (Ch2 "LLM-LLM context transfer"). The line is between a claim that carries its artifact and a claim that asks to be believed. Consequently **merged ≠ done** — merge is one of Ch12.1's six shipped conditions, not a synonym for them, and for an enforcement mechanism ADR-81 leg (e) requires demonstrated *firing* on top (Ch12 — pointers, not restated here). Worked precedent already in the record: **`[#352]` sat merged-but-open** pending the operator's render witness, and closing it on the merge would have been the exact error.

### Architect routing for technical proposals
<!-- scope: meta -->

The browser-chat architect does not seek operator validation on technical proposals where the operator lacks expertise to validate ("is this approach better?", "does this design make sense?", "should I use X or Y?"). The operator's role in technical questions is constraints, priorities, and scope — not technical adjudication. (Moved from ESSENTIALS 2026-07-05, [#258].)

For technical questions the architect cannot resolve alone:
- Research mode: web search, documentation, prior session memory
- AI Council: research or pick debate via `ai-council` CLI
- Analysis: build the comparison/proposal with explicit trade-offs the operator can choose from

Operator is asked: "which of these matters most to you?", "what's the constraint here?", "is this priority correct?" — not "is my technical choice right?".

Sourced from LESSONS #6 (2026-05-12). Architect-side enforcement is operator review.

### Artifact generation direction
<!-- scope: meta -->

Repo artifacts (ADRs, AI Council transcripts, audit reports, handoff bundles, any file destined for a source-of-truth repo) are generated IN Claude Code with proper repo path, ADR-NN numbering, frontmatter, archival convention, and commit hygiene — never generated as markdown artifacts in browser chat for the operator to copy-paste into the repo. (Moved from ESSENTIALS 2026-07-05, [#258].)

Browser chat role: architect-review of artifacts that Claude Code produces. Not artifact-source for repo files. The operator may upload a final repo artifact (e.g. an ADR draft) back to chat for review; the architect reviews and approves, Claude Code merges.

Sourced from LESSONS #8 (2026-05-13). Architect-side enforcement is the workflow rule itself; this is a permanent invariant per LESSONS.md 2026-05-13 (ADR-45 was explored but not adopted).

**Council ADR distillation** is a mandatory automated step of the post-debate protocol: number verified, template-aligned, committed by Claude Code — never a browser-chat hand-off with a placeholder. See §5 "Post-debate protocol". End-to-end Council lifecycle runbook: `protocols/AI_COUNCIL_PROCESS.md`.

### Handoff paths
<!-- scope: meta -->

**Path A — Claude Code → Browser:** `/session-summary` in Claude Code → paste into Claude.ai. Discuss architecture/strategy; decisions return as prompts (Section 2 format).

**Path B — Browser → New Browser:** the operator triggers `please create handoff for <repo>` then `complete handoff for <repo>`; Claude Code generates the v5 handoff (residual + probe manifest + thin boot) per HANDOFF_PROCESS.md — Rob makes zero formatting decisions. Trigger at ~2 hours while context is still fresh.

**Path C — Browser → Claude Code:** Claude.ai writes prompts in Section 2 format (Model/Mode/Effort table). Prefer questions over commands. Let Claude Code discover actual state, then propose actions.

### Token log cadence
<!-- scope: meta -->

Relocated to `protocols/HANDOFF_PROCESS.md` §15 (#152, 2026-06-15; §14→§15 renumber in handoff-process v5.5) — session-boundary maintenance fired by `/session-summary` (7-day staleness check + short-format `ccusage --json` snapshot, newest-first prepend to `logs/TOKEN-LOG.md`). Canonical there; not restated here.

### Output the operator copies into browser chat (render-layer note)
<!-- scope: runtime -->

The trap is the **render layer**, not what Claude writes. A plain markdown pipe-table (`| col | col |`) is the token-cheapest table to write *in a file*, but the Claude Code TUI renders it by **painting Unicode box-drawing borders** (`┌─┬─┐ │ ├─┼─┤ └─┴─┘`) client-side. Those glyphs are added at *display* time — Claude never emits them. So a rule that only bans Claude from writing box-drawing is a no-op: it forbids something Claude already doesn't do, while the operator still copies the painted borders out of the terminal (Path A) into browser chat and pays ~3× the tokens for them.

**The fix targets render, not emit.** For any report the operator copies back — `/session-summary` output and ad-hoc step reports — make it:
1. **Flat** — plain markdown or `key: value` lines / bullets; no column-padding spaces.
2. **Code-fenced** — wrap it in a triple-backtick block. A fenced block renders raw (monospace, un-painted), so the pasted text is exactly the characters Claude wrote — no borders.

A bare (un-fenced) pipe-table is the failure case: clean-looking in the TUI, box-drawing on paste. This is the same fenced-block discipline already used for Scale-S PowerShell snippets (Ch4 "Architect → operator channel-discipline (execution actions)") and downloadable prompts (§2 "Delivery format") — extended to every copy-back report. Reconciles with Path A above (`/session-summary` → paste into Claude.ai).

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

The task queue is the single canonical home for ALL pending items across sessions — on the hub `tasks/` is the source and `BACKLOG.md` its generated rendering (Layout, below); on an unflipped consumer `BACKLOG.md` is itself the source. Handoffs reference queue items by pointer (stream + title), never duplicate the queue. Per-handoff and quarterly grooming prevent the write-only graveyard anti-pattern.

**Mandate:** `BACKLOG.md` is part of the universal governance baseline (ADR-38 amendment A5, 2026-05-23; ADR-41) — mandatory for every repo regardless of size. (Previously gated to M+ repos; the repo-tier system is deprecated.)

<!-- rule: governance-backlog-leave -->
**Done-item disposition (ADR-47/65).** Done items **leave** the file on close — git history (the closing commit, located by the entry id per CONTRIBUTING) + the existing per-session JOURNAL entry are the record. **No archive file** (`BACKLOG_ARCHIVE.md` deleted 2026-05-16; CLAUDE.md §5). No collapsed stubs. Closing a backlog item adds **no new record-keeping surface** — the per-session JOURNAL ritual already carries it; the write a closure does make lands inside the queue's own source of truth (`tasks/` on the hub: manifest node out, terminal `status:` on the retained record; the line simply leaves on an unflipped consumer).

**Filing backpressure (2026-07-08 ruling).** The add-side mirror of Done-item disposition: any commit whose `BACKLOG.md` diff **adds** a new task id must carry a `kill-candidates:` line in the commit message — either naming ≥1 existing `#id` proposed for removal, or `kill-candidates: none — <reason>`. Candidates are **proposals** routed to the operator's ruling; the gate never auto-removes or auto-closes anything. Enforced by the `backlog-filing-backpressure` commit-msg hook (`scripts/check_backlog_filing.py`, the add-side sibling of `backlog-id-on-close`), which also emits the advisory ADR-98 intake-id WARN on a new L-sized new-feature epic (#279).

**Closures fund births — close BEFORE filing (the D3/D5 order, ratified 2026-08-28).** Filing
backpressure above makes a birth *state its cost*; this states where the budget comes from. The
**banked closure ledger IS the birth budget** — rows closed in a window fund the rows born in it —
and the order is load-bearing: closing happens first, because a cap that is not yet known cannot
be spent against. A filing pass that opens before it closes is spending an unmeasured budget, and
the number it settles on is whatever appetite the session happened to have. Recorded with its own
arithmetic: the 2026-08-28 window banked **5** and spent **3** (2 rows + 1 intake), routing three
further items as CANDIDATEs — which are not births and draw nothing from the ledger (ADR-111).

**Grooming by regex — the carrier-vs-subject false-positive class (recorded 2026-07-28).** A grep-driven sweep over `BACKLOG.md` / `tasks/` conflates two different kinds of row: those **carrying** a field and those whose **text discusses** it. Witnessed: an activation-gate sweep surfaced [#426] because ADR-105's activation gate is its *subject*, not because it declares one; a `depends-on` sweep surfaced [#424] / [#425] / [#23], all three of which *write about* the field ([#424] is the parser defect, [#425] the fixture-coverage gap, [#23] a prose mention of another row's dependency) while none of them carries a `depends-on` clause. Acting on the match set without that distinction manufactures phantom edges and phantom blockers, which then propagate into the very sequencing the grooming pass was meant to verify. **Rule:** a regex sweep produces **candidates, not findings** — confirm carrier-vs-subject by reading the row's own field position (on the hub, the derived frontmatter key in `tasks/<id>-*.md`, post-ADR-107) before recording any effect.

**Layout (ADR-66 — supersedes ADR-64's flat layout).** `BACKLOG.md` is a **story map**: **Big Picture → Theme → User Story → Task**. The operator scans goals (Big Picture + themes + stories); the LLM reads execution detail (tasks). **No `repo:` field** (implicitly `.dev-knowledge`); cross-repo governance lives under the *Cross-repo universalization* theme, naming repos in task text; child-repo *execution* items live in the relocation queue, not here. **Authority chain:** ADR-41 (mandate) → ADR-47 (organization) → ADR-64 (done-items-leave / routing / validator) → ADR-65 (disposition) → ADR-66 (story-map layout) → **ADR-107 (engine/schema; step 3 flipped the source of truth)**. A read-only validator (`scripts/validate_backlog.py`) machine-checks the hierarchy. **On the hub, `BACKLOG.md` is GENERATED** from `tasks/` (per-task `.md` bodies + `manifest.json`) since 2026-07-28 — edit the tree and run `gen_task_tree.py --emit-source`; the story-map layout above is unchanged, it is simply assembled rather than hand-maintained. `tasks/README.md` is the runbook.

### Schema (ADR-66; machine-checked by `scripts/validate_backlog.py`)
<!-- scope: meta -->
<!-- rule: governance-backlog-schema -->

**Four layers:**

```
# .dev-knowledge BACKLOG
## Big picture              <- 2-3 sentences + the theme backbone list (no stories/tasks)
## <Theme>                  <- backbone header; a durable area of work
> As a <persona>, I want <goal>.       <- theme intent (persona = operator or an AI agent)
### [S<n>] <User story>     <- human goal (stable numeric story id); the layer the operator scans
So that <why>.              <- the why (required, immediately under the story)
- [#id] [P1][M] <action> · Done when: <criterion> · refs <ADR/file>   <- task (for the machine)
```

- **Big Picture** — what `.dev-knowledge` is working toward (from VISION) + the theme list. The map, not a priority queue.
- **Theme** — a `## ` backbone header; a durable area of work.
- **User Story** — a `### [S<n>] ` header (a stable numeric story id + human language) + one `So that …` line. Personas = the operator and the AI agents (Claude Code / Codex) who inherit the repo. This is the scan layer.
- **Task** — a bullet `- [#id] [P{1-3}][{S|M|L}] <terse technical action> · Done when: <criterion> · refs <…>`. Technical density is expected here. No `repo:`/`status:` field — in-file = open; done tasks **leave** (ADR-65).

<!-- rule: governance-backlog-story-id -->
**Rules** (validator hard-fail unless marked warn):
- every **task** has a unique `[#id]`, a `[P{1-3}][{S|M|L}]` band, and a `Done when:` clause;
- every task sits **under a Story under a Theme** (no orphans; nothing directly under `## Big picture`);
- every **User Story** has a `So that` line **and a stable numeric `[S<n>]` id prefix** (unique across the file; a missing or duplicate `[S<n>]` hard-fails, #286);
- **no done task** in the file — a `status:done` / `[x]` / `~~strikethrough~~` marker hard-fails (done tasks leave);
- *(warn-only: a story with zero tasks.)*

**retire-not-delete at story level.** "Done tasks leave" does **not** generalize upward. A completed **story** keeps its `### [S<n>]` heading and gains a COMPLETED marker naming the closing SHAs; it is not deleted. A task is a work item whose removal *is* the signal; a story is a map coordinate, so deleting it renumbers the operator's mental model and frees an id for reuse — the sequence stops being readable and the allocation record is lost, exactly as with a retired task that keeps its allocation record (ADR-107 §6.3). This is also why the zero-task rule above stays **warn-only**: a completed story legitimately has no tasks. Precedent: `[S24]`, the first empty story on main (`3c050b15`, merged `a02dd111`).

Anti-pattern: do NOT collapse the layers back to a flat list, or re-expand a task to multi-paragraph form — goals-on-top / task-detail-below is the readability fix ADR-66 ratified; the validator guards it.

### Per-handoff grooming (~2 min, mandatory for M+)
<!-- scope: meta -->

Browser 1 (departing) runs at handoff generation:

1. Read current BACKLOG.md state
2. Mark stale items (no progress in 3+ sessions) for review
3. Flag obvious dead items (completed, no longer relevant) for the closure loop / a `tasks/` retirement — not a direct `BACKLOG.md` edit
4. Add new items surfaced this session
5. **Remove** completed items — they leave the file (the closing commit + the per-session JOURNAL entry are the record, ADR-65); do not leave `done` entries in place (on the hub: retire in `tasks/` — manifest node out, terminal `status:`, `--emit-source`; the row leaves as a result)
6. Future State in handoff references BACKLOG items by id + title (pointers, not copy-paste)

Light P1 items MAY be copy-pasted inline into Future State (acceptable at P1 only — Council Risk #2 mitigation).

### Quarterly deep grooming (~30 min, scheduled)
<!-- scope: meta -->

Rob reviews full BACKLOG once per quarter (recurring quarterly cadence — schedule the next review at the start of each quarter; no fixed anchor date, to avoid silent rot into a past date):

1. Confirm **no `done` items remain** — done items leave on close (ADR-47/65); the validator hard-fails on any `done` entry. **No archive file** (CLAUDE.md §5). Retrospect via `git log` + JOURNAL, not a parallel archive
2. Re-prioritize P1/P2/P3 based on current ecosystem state
3. Remove items that no longer align with VISION
4. Groom each stream: still active? Items still actionable?

Steps 1 and 3 state the **outcome**, not the edit: on the hub the removal mechanism is a `tasks/` retirement per `tasks/README.md` (manifest node out, terminal `status:`, `--emit-source`), not a direct `BACKLOG.md` edit; on an unflipped consumer it is the direct line removal.

**Write-only graveyard prevention:** speculative or distant ideas route to VISION.md, not BACKLOG.md. Strict curation — actionable items only.

### The grooming routine — the standing declaration ([#348] anchor)

<!-- scope: meta -->

**Grooming is CONFIGURATION, not "whoever notices."** `[#348]` turned the improvised-per-session
pass into a declared routine and carried the ADR-105 declaration in its own row body. A backlog row
is a **mortal** carrier — it leaves the file when it closes, taking the declaration with it — so on
`[#348]`'s closure the declaration is re-anchored **here**, in the living doc that already owns the
grooming workflow. This paragraph is now the routine's home; the row is its history.

```
routine: backlog-grooming
  trigger:           on-demand (operator ask, or session boot via the §6 start protocol)
  scope:             the task queue — `tasks/` on the hub, `BACKLOG.md` on an unflipped consumer
  consumer:          any session reading the queue; the operator at quarterly deep grooming
  consumption_path:  the queue in place — `tasks/` retirement then `--emit-source`, never a
                     hand edit of the generated `BACKLOG.md`
  verified_by:       `scripts/validate_backlog.py` (schema) + `task_tree_coherence` (source↔view)
  cadence:           per-handoff (~2 min, mandatory for M+) and quarterly deep (~30 min)
```

**Honest limit, stated because the gate cannot state it:** `check_routine_consumers` reads
`· routine:` markers out of **backlog rows only**. This declaration lives in a protocol file and is
therefore **not** gated by that organ — the fenced block above is deliberately fenced, since the
check treats a fenced example as an example and not a declaration. What holds it accurate is the
freshness cadence on this file, not a machine. Extending the organ to doc-resident routines is
`[#426]`'s scope, which is where the ~30 live hook/schedule routines are also owed.

### Split-brain prevention
<!-- scope: meta -->

The task queue is single-source (per §10's opening: `tasks/` on the hub, `BACKLOG.md` on unflipped consumers). Handoffs must NOT duplicate the pending queue:
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

**Library-first adoption order (ruled 2026-08-04).** **stdlib > an existing dependency > a new
distribution — and an adoption claim carries a measured divergence, not a preference.** The
sharp half is the second clause: "the library is better" is not an adoption argument until you
have run both and can say by how much they differ. Precedent, the L-E adoption audit: `graphlib`
was **rejected** because it matched the hand-rolled DFS across **24,000 random graphs** — a
measured non-divergence, so adopting it would have bought nothing; `ruamel` and `tenacity` were
**rejected as new distributions** where an existing dependency or stdlib already reached. The
adoptions that landed did so on measured divergence: `markdown_it` replaced a fence toggle that
was wrong four distinct ways over a 1578-file corpus, and `fnmatchcase` replaced `fnmatch` whose
verdict changed with the host OS. Note the order's own consequence — an *existing* dependency
outranks a new one even when the new one is nicer, and a transitively-present library is
declared explicitly before a gate leans on it (the `packaging>=24.0` / `markdown-it-py>=4.0`
precedent) so no gate rides an edge nobody declared.

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

If a client engagement generates a dev lesson, strip all client names, proprietary schemas, internal tool names, and client-specific API endpoints before writing to `.dev-knowledge/` — replace with `[client]` or generic placeholders. Methodology generalizes; project specifics don't — those belong in the Obsidian vault.

### Migration triggers
<!-- scope: meta -->

- **`.dev-knowledge/` navigation overhead emerges** (cross-file search starts feeling slow; new files don't slot into an obvious folder) → evaluate creating a dedicated Obsidian DevVault
- **LESSONS.md outgrows single-file navigation (size/age)** → **chronological legacy-archival split** (ADR-29 amend. 2026-07-17): relocate the oldest contiguous by-date block **byte-identical** into a dated `LESSONS-legacy-<span>.md`, pointer left behind, when the active file exceeds the entry-count threshold (recommended dial ~300 entries → archive to ≤~180). NOT a by-topic / by-scope split — that stays **rejected** (ADR-29); the `[scope: X]` inline field handles topic filtering.
- Rob opens Obsidian to search for dev methodology → immediate signal DevVault is needed

> Triggers, not caps. See LESSONS.md 2026-04-28 entry "Distinguish triggers from limits."

---

## 14. Markdown Governance
<!-- scope: dev -->

> **Reconciled 2026-06-23 (Handoff + Snapshots/reports rows).** The Handoff and Snapshots/reports rows below now match practice: handoffs are dated, immutable `docs/handoffs/YYYY-MM-DD-*/` bundles (folder convention per ADR-32 / HANDOFF_PROCESS v5.4), not a living `docs/HANDOFF.md`; dated snapshots/audits under `docs/archive/` are kept **indefinitely** (the prior "delete after 90 days" lifecycle never matched practice — audits are immutable records).

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
3. ≥2-branches / cycle / ≥3-actors → Mermaid (on the human-facing visualization surface only)
4. auto-generable fact → generated only
5. any Mermaid >12 nodes → split or demote

Mermaid is the heaviest form (token cost + AI-edit-reliability drop above ~100 lines of markup) — reserve it for genuine branching/cyclic/multi-actor structure, and demote on the first rule that a lighter form satisfies. **Canonical root docs carry no Mermaid** — since the ADR-51 amendment 2026-07-05 (LLM-first canonical docs) diagrams live on the separate visualization surface (ADR-59), so rule 3 applies there, not in `ARCHITECTURE.md`/`CLAUDE.md`/`VISION.md`/`protocols/*`. Refs #91 (amendment A), ADR-51 + amendment 2026-07-05.

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
**Skip when:** Single-file fix, test-only changes. (Documentation/prose diffs are *not* skipped wholesale — they route to the `/codex-review` doc-lane; see "Code-vs-doc routing" below and [#333].)

(Gated by change size and risk, above — not by any repo tier; the repo-tier system was deprecated 2026-05-23.)

### Review Tools
<!-- scope: dev -->

Two options for code review (A/B test both, then standardize):

**Option A — /code-review ultra (Claude Code built-in; `/ultrareview` is the deprecated alias):**
Cloud-based multi-agent review. Run without arguments (current branch) or with a PR number. No second terminal needed.

**Option B — Codex CLI (automated, single command):**
`/codex-review <topic>` wraps `codex exec --output-last-message`. Produces dated, frontmatter-wrapped audit at `docs/audits/YYYY-MM-DD-codex-{topic}.md`. Read-only sandbox. Opt-in `-AutoCommit`. Requires ChatGPT Plus subscription. See `~/.claude/bin/codex-review.README.md`.

**Code-vs-doc routing (per-change codex-review):** the wrapper routes by an extension path-guard against a code allowlist (`.py .ps1 .psm1 .sh .bash .ts .tsx .js .jsx .go .rs .rb .java .cs .cpp .cc .c .h .hpp .sql .toml .yaml .yml .json .ini` — the wrapper is authoritative; this list is illustrative) and a prose set (`.md .rst .txt`). A diff containing **any** code file uses the **code profile**; a diff with **no code files but ≥1 prose file** routes to the **doc-lane** prose/structural profile ([#333]) rather than exiting unreviewed (non-prose paths like images are ignored in the review, not a blocker). Mixed code+prose diffs filter to the code subset (code profile). Empty diffs — or diffs with neither code nor prose — exit cleanly without invoking codex. Mechanically enforced in `~/.claude/bin/codex-review.ps1`.

Both satisfy S15 review requirement. Choose based on quality of findings after 2-week A/B test.

Codex/ultrareview reviews. Claude Code builds. Never reverse the roles.

**Codex reviewer config:** The global reviewer config (role, checklist, output format) lives at `~/.codex/AGENTS.md`; canonical source tracked in `.dev-knowledge/codex/AGENTS.md` (ADR-54). Per-repo `AGENTS.md` adds only repo-specific rules — it does not repeat the global config.

### Codex-utilization doctrine (lanes + exact model strings)
<!-- scope: dev -->

- **Exact model strings only.** The Codex 5.6 lanes are `gpt-5.6-terra` / `gpt-5.6-sol` / `gpt-5.6-luna` — always the full string, **never a bare `gpt-5.6`** (an invalid identifier: a bare-string call fails as bad input — a 400 on ChatGPT auth — which is NOT evidence the capability is absent — LESSONS 2026-07-12 invalid-input-vs-absent-capability). Nicknames map exactly: **terra / sol / luna = `gpt-5.6-terra` / `-sol` / `-luna`**. Verified against the live codex-cli `/model` selector (registry snapshot in [#333]).
- **terra is the doctrinal default review lane, and BOTH lanes now pin it explicitly.** *(Corrected 2026-08-04 — this bullet described a drift that `[#469]` closed on 2026-08-01. It read: "the code lane currently inherits the codex config default (`gpt-5.6-sol` as of 2026-07-16) because the wrapper passes no `-m` flag on that path." Verified against the live wrapper `~/.claude/bin/codex-review.ps1`, which sets `$reviewModel = 'gpt-5.6-terra'` and passes it on both paths; the same stale claim was corrected in `~/.claude/commands/codex-review.md` on 2026-08-03.)* The pin exists because an unpinned run the operator asked for as terra silently EXECUTED as sol, with nothing in the artifact recording which model had run — and an unpinned reviewer also makes cross-provider comparison unreproducible. Choose sol or luna deliberately only when a lane's stated strength fits the task better, and say why.
- **Doc-lane review is first-class in `/codex-review`** ([#333]): a prose diff (no code files, ≥1 `.md`/`.rst`/`.txt`) routes to the wrapper's **doc-lane** — a prose/structural profile (disposition-faithfulness, cross-doc consistency, structural integrity, template usability) pinned to `gpt-5.6-terra`. The code-only path-guard still filters markdown out of the *code* profile; mixed diffs review as code. (Ad-hoc `codex exec` remains available for one-off reads outside a diff.)
- **Every plan names its Codex lane.** A plan / architect prompt states which lane (terra/sol/luna) + surface (code or doc, both via `/codex-review`) its review leg uses — an addressable planned decision, not an ad-hoc runtime pick (pairs with review-before-STOP, Ch12).
- **Read the body, not the severity summary.** A reviewer's severity header is a routing hint, not a finding — and it is the part most likely to be wrong, being generated last and compressing most. Read the finding body, reproduce the claim against live state, and disposition on what you reproduced: a HIGH that does not reproduce closes as not-reproduced, and a LOW whose body names a real defect is fixed regardless of band. Acting on the summary line alone propagates the reviewer's triage error into the repo. Family: `[#431]` / `[#445]`; cross-reference the wrapper change-record audit from the terra-pin arc, where band and body disagreed.

### Codex dual-role — reviewer today, producer gated

Codex has two potential roles in the fleet — **reviewer** (the live, doctrinal one — everything above) and **producer** (author of code/design, the EPIC-H charter axis). Their governance (ratified from the ai-council 2026-07-17 role-governance feedback, R1/R4/R5):

- **The global Codex config is HUB-OWNED (R1 — fleet doctrine).** The global reviewer config — `~/.codex/AGENTS.md` (role / checklist / output format; canonical source `.dev-knowledge/codex/AGENTS.md`, ADR-54) **and** `~/.codex/config.toml` (model pin, effort) — is owned at the hub, exactly as **core-invariant #6** governs `~/.claude/` hooks/rules and hub protocols. **Consumers never edit it**, and a session never edits it unilaterally; a change is an explicit hub ruling, never a per-repo or per-session drive-by. This is the global-infra "exception-with-ruling" invariant, now stated for the Codex surface (same class as `#289` OneDrive-guard and `#338`(c)).
- **The producer lane is NOT activatable as written today (R4 — reconciliation).** The EPIC-H charter extension describes a Codex **producer** role (Codex authors, CC adversarially verifies — the inverse of the live Codex-verifies-CC review flow). But the hub-owned global config currently **fixes Codex as a read-only reviewer** (`~/.codex/AGENTS.md` pins the reviewer role; the exec sandbox is read-only). So the producer lane is **charter-only** — a documented intent, not a switch a session may flip — until the activation mechanism (`#341`) lands and is ruled. Do not treat "Codex producer" as available; a plan that names a producer leg is describing future work, not a runnable lane.
- **Sanctioned interim producer-lane fallback (R5 — codified).** Until per-invocation producer activation is designed (`#341`), the sanctioned way to get producer-grade leverage from Codex **without editing global infra** is: **Codex fully specifies the design under a bounded prompt → CC implements → terra (`gpt-5.6-terra`) read-only review pre-merge.** The design-specification step is a **bounded, read-only `codex exec` design prompt** — Codex emits a spec/plan *as text* inside the read-only sandbox, **writes nothing to the tree, and never authors the merged artifact (CC does).** This is a **distinct invocation** from the `/codex-review` **reviewer** role (findings-only, governed by `~/.codex/AGENTS.md`) — so it is not bound by that config's "review findings, don't author fixes" contract — **and** it stops short of the gated **producer** role (authoring merged code). Nothing about the hub-owned config changes. This is exactly the flow executed on **ai-council #30**. *Whether an ad-hoc design-spec `codex exec` prompt should carry its own bounded reviewer-config reconciliation* is inside `#341`'s scope — which also carries the producer *mechanism itself* (repo-local `AGENTS.md` precedence, per-invocation activation, the producer guardrails).

### DEGRADED-REVIEW — the fallback chain when the doctrinal reviewer lane is unavailable
<!-- scope: dev -->

*Architect ruling 2026-08-29, amended the same day to the chain below.* **A missing reviewer does
not block the work.** The doctrinal pre-merge reviewer is terra (`gpt-5.6-terra` via
`/codex-review`, pinned on both lanes — "Codex-utilization doctrine" above); when it is unavailable
on quota or outage, the arc **descends the chain** rather than stalling. An arc blocked on an
absent reviewer produces no review at all, which is worse than a tagged review that terra re-reads
afterwards.

**The chain — ordered COST-ASCENDING, and the ordering has a stated reason.** Because terra
re-review restores quality afterwards (the standing obligation below), the cheap-but-weaker rungs
are tried ahead of the expensive-but-equivalent one:

| Rung | Lane | Why it sits here |
|---|---|---|
| 1 | **terra** (`gpt-5.6-terra`) | the default |
| 2 | **grok CLI** | pay-per-call, measured cheap |
| 3 | **Kimi / GLM / DeepSeek CLI** | the FIRST transport that passes a **liveness probe** |
| 4 | **Codex via pay-as-you-go API** | **last resort only** |

Rung 3 is **conditional by design**: the last preflight found these transports dead or corrupt, so
probing one before use is part of the rule rather than an optimisation. Rung 4 sits at the bottom
precisely because it pairs terra's own model class with the highest price of any fallback — same
quality, worst cost, which is what makes it the last resort rather than the obvious substitute.

**Obligations carried by every fallback artifact:**

- **The `DEGRADED-REVIEW` tag plus the reason** — which lane was unavailable, and why (quota /
  outage). A degraded review that reads like a doctrinal one launders its own provenance.
- **The served model id, recorded PER ROUND — the `[#492]` scar, not ceremony.** Grok has served a
  **substituted model id silently**: the request named one model, the response came back from
  another, and nothing in the artifact recorded it. The tag alone is therefore not enough.
- **A transport that cannot report the served id is tagged `REVIEW-UNVERIFIED-TRANSPORT` instead**,
  and terra re-review becomes **mandatory rather than best-effort**. An unverifiable reviewer
  identity is a weaker claim than a verified substitution, so the two carry different labels.

**The standing obligation, stated so the chain is not read as a quality equivalence.** **Terra
re-reviews EVERY degraded artifact once quota returns.** The chain buys **availability**; it is
**not** a quality substitute. A rung that unblocked an arc leaves the terra re-read owed, and that
obligation outlives the outage that caused it.

**The funding rule.** Where a pay-as-you-go balance is insufficient, **that review stops — the work
and the arc keep going.** Report the **exact top-up needed**; the operator funds it and says go. A
review that cannot be paid for is a stopped review rather than a stopped lane.

**Admission — and this is what reconciles the chain with the refusal on record.** Every fallback
model still owes the **SDA-1 reviewer-role gate as its measured admission row**. `[#562]` closed
2026-08-23 with an architect verdict of **`grok-4.6` REFUSED** (G1 FAIL, G2 FAIL;
`docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §5.1), and `[#492]` — *"Grok
review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs"* — stays
open and undischarged by this subsection. **The two facts are consistent rather than
contradictory:** the chain licenses grok and its siblings as an **availability stopgap under a tag,
with mandatory terra re-review**, and it admits none of them as a **quality-equivalent review
lane**. Refusal-as-admission and admission-as-stopgap are different questions; a seat reading this
subsection as "grok is an approved reviewer" has read past the tag, the re-review and the refusal
alike.

*Why this lives here and not in the routing table.* `~/.claude/ROUTING.md` is an **L0 surface
outside this repo** (`ARCHITECTURE.md` Ch3, ruled 2026-08-22) and it routes **task-classes to model
tiers**, not reviewer lanes to arcs. A reviewer-lane fallback is review doctrine, so this chapter
is its home.

*Honest limit.* Prose, gated by nothing. No organ checks an artifact for the tag, for a served-id
line, for the rung-3 liveness probe, or for the terra re-review a degraded artifact owes; this
binds the seat, not the tree.

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

**Empirical reference:** the ai-council scrum-master review 2026-05-11 (10 findings + an addendum) — the addendum mechanism prevented full report regeneration. (`docs/audits/2026-05-11-ai-council-scrum-master-review.md`.)

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

## 20. Deploying the methodology corpus to a consumer (deploy runbook)
<!-- scope: hybrid -->

> Operational how-to for the ADR-92 deploy tool (`deploy/tool.py` + the four carriers). **Doctrine is ADR-92 — not restated here.** Proven end-to-end on run #1 (ai-council → v1.0.0; retrospective in `LESSONS.md`). Run from the hub; the tool reconciles ONE consumer per invocation.

### The three phases — assess → execute → ratify

1. **Assess (read-only).** `python deploy/tool.py <repo> --target <vX.Y.Z>` — prints the per-carrier deployment plan (detected state + planned action) and mutates nothing. Review it. If any carrier shows an unexpected state or an error row, STOP and investigate before executing.
2. **Execute.** `python deploy/tool.py <repo> --target <vX.Y.Z> --execute` — per carrier: apply-if-needed (or `--force`) then verify; the **verify-gate** proceeds to the record write ONLY if EVERY carrier verifies. On full success it (a) **stages** the consumer's carrier changes (write-yes / commit-no) and (b) commits the version record on a **hub branch** `deploy/record-<repo>-<bare-version>`. On any verify failure it ABORTS — no record, no staging (earlier carriers stay applied on disk; rerunnable).
3. **Ratify (operator — two writes, two contexts).**
   - **Consumer:** `git -C <consumer> diff --cached` → review → **branch + `--no-ff` commit in the consumer** (the universal no-direct-to-main rule applies to consumers too; core-invariants #5), push per the consumer's norm. The tool NEVER commits in the consumer.
   - **Hub record:** review + **merge** `deploy/record-<repo>-<bare-version>` → hub main (`--no-ff`). The tool NEVER merges it. This sets `ecosystem/deployed-versions.yaml` for `<repo>` (read by `audit.py deployed_methodology_version`; see Ch6 "Deployed-version record").

### Operational nuances (learned on run #1)

- **Verify the record on BOTH axes before merging.** The record blob must be **0 CR (LF)** AND **non-ASCII byte-faithful**: `git show <branch>:ecosystem/deployed-versions.yaml | tr -cd '\r' | wc -c` → `0`, and em-dashes (`E2 80 94`) present with no `â€` mojibake. Two earlier runs produced a blocked record (CRLF, then mojibake) before the writer was hardened; it is now binary+UTF-8+LF and fails loudly on malformed input, but verifying the bytes is cheap insurance.
- **Re-run safety.** An existing record branch → `RecordError` (never clobbered). To regenerate: `git -C <hub> branch -D deploy/record-<repo>-<bare-version>` then re-run `--execute`.
- **Clean-tree preflight.** The tool requires a clean CONSUMER tree — commit the consumer gate (phase 3) BEFORE re-running `--execute`, or preflight aborts.
- **Run gates + ship from Git Bash, not PowerShell** (the ship-gate false-RED gotcha — `gotchas.md`).

### Floor semantics — tracked + hash-guarded (model A)

The methodology floor (`.claude/CLAUDE-FLOOR.md` + `.sha256`, ADR-78) is generated from **hub-canonical** (ADR-73) and, under **model A (ADR-93)**, is **committed + tracked** in the consumer behind a **two-leg hash-guard**: a session-start `.claude/settings.json` hook + a commit-time `floor-hash-verify` pre-commit hook, both running the one canonical `.claude/check_floor_hash.py`. The hub template stays the **single authoritative source**; the committed consumer floor is a hash-guarded **replica**, so the #95 copy-drift invariant is preserved — drift is **caught by the guard, not avoided by non-tracking** (never a second *unguarded* source). To make the floor/sidecar/guard trackable, the floor carrier rewrites the consumer `.gitignore`'s bare `.claude/` to the contents-form `.claude/*` + `!`-negations (a bare directory exclusion defeats negations, #138), so the floor stages with a plain `git add` — **no `git add -f`**. The carrier writes/stages; the operator commits (ADR-92 commit-no). *(Supersedes the prior "local-only / not committed / on-disk-but-unstaged" framing — it produced the configured-not-armed floor ADR-93 fixes.)*

### What to expect on runs #2–4 (per-consumer divergences the run-#1 probe surfaced)

The mechanics transfer; the consumer *shapes* differ:
- **`.gitignore` shape varies** — model A rewrites a bare `.claude/` to `.claude/*` + `!`-negations so the floor/sidecar/guard track (the floor carrier does this in `apply`); a consumer that already tracks `.claude/settings.json` (e.g. ai-council, force-added) carries the SessionStart guard hook on a fresh clone (a *greenfield* consumer that gitignores `.claude/` needs `settings.json` tracked too — #221/ADR-93 known limit). Check `git -C <consumer> status --porcelain --ignored` and `git -C <consumer> check-ignore .claude/CLAUDE-FLOOR.md` (should print nothing once armed).
- **Noisy `.pre-commit-config.yaml` diff** — the precommit carrier round-trips the YAML, reformatting the whole file (comment-strip / reindent). Cosmetic + functionally equivalent (deferred surgical-edit fix). Review the LOGICAL change (added ruff gate + rev-pin), not the reformat noise.
- **Record generation is now reliable** — writer hardened on the Windows-I/O class; still verify both axes before merging.

---

## 21. The delivery loop (end-to-end)
<!-- scope: meta -->

The eight gates a change passes from intent to closure. Every gate below is **canonical somewhere else** — this section exists because the pieces were scattered across Ch8, Ch12.1, §8 and §16, so no cold reader could find *the loop* as a whole. Read it as an index with an order, not as doctrine: each row points, none restates.

Proven end-to-end on **2026-07-21** (ai-council `assets/` dissolution, merge `88b0876`) — the first complete pass after 3–5 sessions of plan-without-ship, with every safety gate firing for real. Per *"prove, then codify"* (§4), that run is what made this write-up owed.

| # | Gate | Canonical home (read it there — the constraints live there, not here) |
|---|---|---|
| 1 | **Frozen ex-ante contract** | Ch12.1 "Authored before the build"; ADR-81 amend. 2026-06-24 |
| 2 | **Branch + commit-and-STOP** | Ch8 "Integration authority" (2026-07-16 ruling) |
| 3 | **Gates green in the target repo** | Ch8 "Consumer-leg merge delegation" (incl. the pre-existing-failure posture); Ch12.1 point 6 |
| 4 | **terra review pre-merge** — name the lane *and* the surface | §16 "Codex-utilization doctrine" — lane routing, the mixed-diff rule, and the exact model strings are all specified there |
| 5 | **Operator GO** | Ch8 "Integration authority" |
| 6 | **`--no-ff` serial merge from the primary checkout** | Ch8; core-invariant #5; `block-ff-push` |
| 7 | **OPERATOR WITNESS** | §8 "Discharge with evidence" |
| 8 | **Educate** — change · why · what-next | "The two lifelines" § Lifeline 1 (`… → archive → educate`) |

**Merged ≠ done.** Gate 6 is one of Ch12.1's six shipped conditions, not a synonym for them; gates 7–8 sit *after* it. A lane that stops at the merge has completed six of eight — which is the whole reason this section is an ordered list and not a prose paragraph.

**The four supporting substances, and where each lives** (this section points; it does not own them):

- **Unfiltered live-session check** — before any consumer write; transcript-cwd is authoritative → **Ch8 "Hub→consumer writes"**
- **TARGET-REPO guard** — line one of every cross-repo prompt → **Ch4 "Pre-send checklist"** (skeleton: §2 "Structure")
- **Prove, then codify** — discipline enters PLAYBOOK only after it ships once → **§4 "When a lesson becomes a rule"**
- **Discharge with evidence** — closure names its artifact → **§8 "Completion claims require state verification"**

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

The codemap section of every M/L `ARCHITECTURE.md` is an auto-generated **compact-text** block — a module/layer list plus a `from -> to` dependency list, with orphan and cycle classification and per-module source paths — showing the repo's top-level Python packages, their import relationships, and their layer assignments (if `tach.toml` is present). It is optimized for the LLM readers that consume canonical docs: the same dependency facts the earlier Mermaid form carried, at a fraction of the token cost. Governing authority: ADR-51 Decision 6 + amendment 2026-05-22, **as amended 2026-07-05** (Mermaid → compact text; the codemap stays generated, `mermaid_emit.py` retained unwired for the future visualization surface).

**Visualization surface (was: the Mermaid theme directive).** The ADR-51 amendment 2026-07-05 moved Mermaid out of canonical `ARCHITECTURE.md`, and `scripts/audit.py` check #7 `mermaid_theme_directive` is **retired** (with its pinning tests + fixtures). The high-contrast custom-base theme standard (ADR-51 amendment 2026-05-28 v2) is **not revoked** — it is re-scoped as *guidance* for the separate, human-facing visualization surface (ADR-59), no longer an audited gate. Diagrams are a rendering *of* canonical facts, produced on demand or stored outside canonical docs; `mermaid_emit.py` is the natural emitter for that surface.

### When the generator runs
<!-- scope: meta -->

A pre-commit hook (`codemap-freshness`) fires whenever Python source files, `pyproject.toml`, `tach.toml`, or `ARCHITECTURE.md` itself change. If the committed codemap block differs from a fresh generation, the hook exits non-zero and blocks the commit. The operator runs `generate --write` and re-stages `ARCHITECTURE.md` before retrying. The generator can also be invoked manually at any time for inspection.

### Manual invocation
<!-- scope: meta -->

```bash
# Dry-run — print the generated compact-text codemap block to stdout (does not modify ARCHITECTURE.md)
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

Applied to `ARCHITECTURE.md` and `protocols/PLAYBOOK.md`. **Not** auto-applied to every doc — add only where navigation overhead is real (threshold: roughly **≥~400 lines / ~8+ sections**). Authority: ADR-51 § Auto-TOC (same freshness regime as the codemap).

