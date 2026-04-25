# Dev Practice Playbook

> **Living document.** Repeatable processes for everything Rob does regularly with AI-assisted development.
> Last updated: 2026-04-21

---

## System Architecture
<!-- scope: meta -->

**`.dev-knowledge` is not a journal and not an orchestrator.** It is the passive storage layer in a three-layer architecture. This section describes what is — it does not decree new constraints.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 — BROWSER CHAT (Claude.ai)  │  Analytical          │
│  Analysis, synthesis, critical thinking, Council debates    │
│  Produces: handoffs, ADRs, session summaries, Council briefs│
└──────────────────────┬──────────────────────────────────────┘
                       │ handoff → git commit
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2 — .dev-knowledge            │  Passive storage     │
│  Templates, patterns, lessons, ADRs, playbook, handoffs     │
│  Read by humans, Claude Code, future browser chats          │
│  No scripts reside here. Library, not daemon.               │
└──────────────────────┬──────────────────────────────────────┘
                       │ read / pull as context
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3 — PROJECTS (Claude Code)    │  Execution           │
│  corp-monorepo, ai-council, sca-time-automation, etc.       │
│  Read from Layer 2, run tests, generate artifacts           │
│  Reflections → back to Layer 1 as new browser chat          │
└──────────────────────┬──────────────────────────────────────┘
                       │ reflection → new browser chat
                       ▼
                  (cycle closes at Layer 1)
```

### Rules
<!-- scope: dev -->

- **Layer 2 never executes.** No scripts, no orchestrator, no active daemon residing in `.dev-knowledge/`. Read-only execution semantics.
- **Write-back via Layer 1 only.** Claude Code (Layer 3) does not directly edit `.dev-knowledge/` files. Reflections flow back through browser chat → handoff → commit.
- **Bidirectional, not read-only.** Layer 2 is updateable via handoffs/ADRs/lessons from Layer 1. The *execution* direction is one-way (Layer 2 → Layer 3).
- **Separate from Obsidian vault.** Vault = pre-sales domain knowledge (see Section 12). `.dev-knowledge` = dev methodology. Different domains, different audiences, different write paths.

### Cross-reference
<!-- scope: meta -->

Section 12 "Where Knowledge Lives" describes knowledge **domains** (what lives where). This section describes workflow **layers** (how information flows). Complementary views of the same ecosystem.

---

## AGENTS.md — canonical per-repo governance contract
<!-- scope: meta -->

**Purpose:** Each repo (corp-monorepo, ai-council, .dev-knowledge, future projects) has an `AGENTS.md` at root. This is the canonical governance file — what any LLM-based agent (Claude Code, Codex, Cursor, Aider) reads to understand "how this repo works" before making changes.

**Authority hierarchy:**
1. `.dev-knowledge/ESSENTIALS.md` + `PLAYBOOK.md` (this file) — universal rules across all Rob's work
2. `{repo}/AGENTS.md` — per-repo specifics (architecture, conventions, tools active here)
3. `{repo}/CLAUDE.md` — thin pointer (≤200 lines) referencing both above + Claude Code-specific quirks
4. `{repo}/.claude/skills/`, `commands/`, `hooks/` — runtime config

**Why hybrid (not duplicate):**
- AGENTS.md does NOT repeat universal PLAYBOOK content — it points to it (Section 1: "Read first")
- AGENTS.md covers only repo-specific: architecture, dependencies, conventions, tools, ADRs binding here, gotchas, do-NOTs
- Avoids drift: when PLAYBOOK rule changes, no per-repo file needs updating

**Cross-tool standard (Council #28 community finding):**
AGENTS.md is read by Claude Code, Codex, Cursor, Aider, Jules, Factory, and other LLM agents per the agents.md initiative (Sept 2025). Single canonical file vs tool-specific config files.

**Template:**
See `templates/AGENTS-md-template.md` for the canonical 10-section skeleton. Copy to a new repo's root and fill in placeholders.

**Sections (template):**
1. Read first (pointer to .dev-knowledge)
2. Repo identity (name, scale, purpose, status)
3. Architecture (layer structure, dependencies, enforcement)
4. Conventions (filenames, branches, commits, testing, linting)
5. Tools active (review tools, hooks, etc.)
6. Things this repo gets wrong (pointer to gotchas skill)
7. Council decisions binding here (ADR list)
8. Out of scope (what does NOT belong here)
9. Session start checklist (concrete checks)
10. Do NOT (rejected patterns + anti-patterns)

**LLMs advise; hooks/tests enforce:**
AGENTS.md tells the LLM what to do/avoid. Tach, pre-commit hooks, pytest, Codex /review enforce mechanically. Don't put rules in AGENTS.md that aren't backed by enforcement somewhere — they'll drift.

**Update cadence:**
AGENTS.md updates when:
- New ADR is binding (Section 7)
- New tool adopted (Section 5)
- New gotcha promoted to skill (Section 6)
- Architecture change (Section 3)
- Anti-pattern discovered (Section 10)

Stale AGENTS.md = LLMs operating on outdated context. Treat updates as part of the change that triggered them, not separate maintenance.

---

## CLAUDE.md as session contract
<!-- scope: meta -->

**Purpose:** Each repo (corp-monorepo, ai-council, .dev-knowledge, future projects) has a `CLAUDE.md` at root. Auto-read by Claude Code on session start. **Thin pointer (≤200 lines)** to:
- `AGENTS.md` (cross-tool canonical governance — per Council #28)
- `.dev-knowledge/ESSENTIALS.md` + `PLAYBOOK.md` (universal Rob rules)
- Recent ADRs, handoffs, journal entries

### What CLAUDE.md is
<!-- scope: meta -->

- **Session contract for THIS tool** (Claude Code) operating in THIS repo
- Lists slash commands, skills, hooks ACTIVE in this repo
- Critical rules specific to Claude Code's behavior here
- Anti-patterns Claude Code has gotten wrong in this repo

### What CLAUDE.md is NOT
<!-- scope: meta -->

- Comprehensive governance — that's AGENTS.md
- Universal rules — those live in `.dev-knowledge/`
- Architecture documentation — that's `docs/ARCHITECTURE.md`
- Decision rationale — that's `docs/decisions/ADR-NN_*.md`

### Why ≤200 lines
<!-- scope: meta -->

Council #28 community finding: CLAUDE.md grows by accretion in most repos, ending as 1000+ line dump that nobody reads. Solution: thin pointer pattern. CLAUDE.md says "read AGENTS.md, then continue" + Claude-Code-specific quirks. Comprehensive content lives in dedicated files.

corp-monorepo CLAUDE.md (4KB, stale numbers like "24 Council Decisions" when there are 29) is exactly the failure mode this template prevents.

### Authority hierarchy (recap from AGENTS.md section)
<!-- scope: meta -->

1. `.dev-knowledge/ESSENTIALS.md` + `PLAYBOOK.md` — universal
2. `{repo}/AGENTS.md` — cross-tool, per-repo
3. `{repo}/CLAUDE.md` — Claude-Code-specific quirks, thin pointer
4. `{repo}/.claude/skills/, commands/, hooks/` — runtime config

### Template
<!-- scope: meta -->

See `templates/CLAUDE-md-template.md` for the canonical 10-section skeleton (≤200 lines).

### Update cadence
<!-- scope: meta -->

CLAUDE.md updates when:
- New slash command, skill, or hook added (Sections 5, 6, 7)
- ADR list rotation needed (Section 9 — keep last 5-10)
- New anti-pattern discovered for Claude Code specifically (Section 8)
- AGENTS.md or PLAYBOOK.md restructure (update Section 1 paths)

**Stale CLAUDE.md = Claude Code operating on outdated context every session.** Treat updates as part of the change that triggered them.

### Per-Scale notes
<!-- scope: meta -->

- **Scale S:** CLAUDE.md may be 50-100 lines (less infrastructure)
- **Scale M:** CLAUDE.md may be 100-150 lines (some skills, hooks)
- **Scale L:** CLAUDE.md should approach but not exceed 200 lines (rich tooling, more ADRs to reference)

If CLAUDE.md grows past 200 lines, split content: most goes to AGENTS.md, only Claude-Code-specific stays.

---

## Writing prompts for Claude Code
<!-- scope: meta -->

**Purpose:** Standardize prompts that browser chat produces for Claude Code execution. Per ADR-28 (three-layer architecture): browser is architect, Claude Code is executor — prompts are the contract between them.

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
4. **Read first** (CLAUDE.md, AGENTS.md, gotchas, relevant docs)
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
- [ ] **Model/Mode/Effort table** present at top
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

Skip checklist items only when not applicable to specific task type. If unsure, include them.

### Anti-patterns
<!-- scope: meta -->

- **Polish prompts** — even if Rob asks in Polish, prompt body is English
- **Inline `!` git commits** — Claude Code commits via explicit Bash steps, not shortcuts
- **Missing UNDERSTAND** — Claude Code without context makes wrong assumptions, especially on Scale L
- **Unclear out-of-scope** — Claude Code expands work; explicit "Do NOT touch X" prevents
- **Relative paths** — break when CWD shifts between repos

### Update cadence
<!-- scope: meta -->

Prompt format updates when:
- New common failure mode discovered → add to "What could break" guidance
- New repo with different conventions → may require template variant
- ADR amendment changes prompt protocol (e.g., new git workflow standard)

This section's history is in PLAYBOOK CHANGELOG entries (search for "prompt template" or "Gap #2").

---

## Project Scale Tiers
<!-- scope: dev -->

Every project declares its scale in its CLAUDE.md:

```
## Project Scale: L
```

Three tiers:
- **L (Large):** Multi-package repo, 500+ tests, cross-package dependencies. Has ARCHITECTURE.md, per-module READMEs, AGENTS.md for external reviewers.
- **M (Medium):** Standalone package, 50-500 tests, multiple modules, one namespace. May have ARCHITECTURE.md.
- **S (Small):** Single script or tool, <50 tests, simple flow. Minimal docs beyond CLAUDE.md and CHANGELOG.md.

Sections in this Playbook marked with a tier tag (e.g. **[L only]** or **[L+M]**) apply only to those tiers. Unmarked sections apply to all projects.

### Testing rules per tier
<!-- scope: dev -->
<!-- version: 1.0 — 2026-04-25 -->

Test infrastructure scales with project size. Over-investing in test infra at Scale S wastes effort; under-investing at Scale L creates fragility.

| Scale | Minimum | Coverage target | Test types | Run command |
|-------|---------|-----------------|------------|-------------|
| **S** (<50 tests) | optional | n/a — coverage measurement overhead exceeds value | smoke tests at most | `pytest` (single run) |
| **M** (50-500 tests) | required | ≥60% on `src/`, no untested public API | pytest unit + selective integration | `pytest -x --tb=short` |
| **L** (500+ tests) | required | ≥80% on `src/`, comprehensive public API coverage, integration suite for critical paths | pytest unit + integration + e2e where applicable | `pytest -x --tb=short` per step + `pytest --co --collect-only` for sanity |

#### Reading the table
<!-- scope: dev -->

- **required** — tests must exist and pass before merge; CI/CD enforces
- **optional** — tests welcomed but not blocking; useful when complexity warrants
- **n/a** — measurement overhead exceeds practical value at this scale

#### Per-step test cadence (Scale M and L)
<!-- scope: dev -->

Per `templates/prompt-template.md` and PLAYBOOK "Writing prompts for Claude Code" section:

After every numbered step in a Claude Code prompt:
1. `pytest -x --tb=short` — fail fast, short tracebacks
2. `ruff check src/ tests/ --fix` — autofix lint issues
3. `git status` — verify expected file scope

This cadence catches regressions early and keeps each commit's diff sane to review.

#### Test types and when
<!-- scope: dev -->

- **Unit tests:** all Scale M+. Mock external dependencies. Fast feedback (<10s per file).
- **Integration tests:** Scale L for critical paths (e.g. data pipeline, auth flow). Real dependencies, isolated DB, slower (1-30s per test).
- **E2E tests:** Scale L for top user journeys. Real environment, optional in standard CI (run nightly or pre-release).
- **Smoke tests:** Scale S for "did basic flow break?" Single-file pytest, optional CI.

#### Anti-patterns
<!-- scope: dev -->

- **Coverage chasing at Scale S** — measuring coverage on <50-test repo wastes 30+ min per session for diminishing return
- **Skipping tests at Scale L** — "this commit is small" + L-scale repo = recipe for hidden regression
- **Integration-only at Scale L** — slow feedback discourages running tests; unit tests are the foundation

#### Section history
<!-- scope: dev -->

- v1.0 (2026-04-25) — initial. Baseline numbers from observed practice (corp-monorepo 2515 tests at L; ai-council ~200 at M). Coverage targets are guidelines, not enforced thresholds.

---

## Documentation file types and session continuity
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

Two related questions: **what does each documentation file do** (Gap #4) and **which files exist per Scale tier** (Gap #18). Combined here because they answer "when I need to write something down, where does it go?"

### File type taxonomy
<!-- scope: meta -->

| File | Purpose | Format | Cadence | Audience | Order | Scope |
|------|---------|--------|---------|----------|-------|-------|
| `README.md` | User-first navigation, what is this repo | Prose + folder layout | When repo state shifts notably | Rob, future contributors | Living (rewrite) | Per-repo |
| `CLAUDE.md` | Session contract for Claude Code, thin pointer (≤200 lines) | Sectioned, scope-tagged | When skills/commands/hooks/ADRs change | Claude Code (auto-read) | Living (sections updated) | Per-repo |
| `AGENTS.md` | Cross-tool canonical governance | 10-section template | Same triggers as CLAUDE.md | Claude Code, Codex, Cursor, Aider | Living (sections updated) | Per-repo |
| `ESSENTIALS.md` | Rob's daily cheat sheet, universal | Sectioned, scope-tagged | When Rob's working style evolves | Rob + every browser/Claude Code session | Living (sections updated) | Universal (`.dev-knowledge` only) |
| `PLAYBOOK.md` | Universal protocols, this file | Sectioned, scope-tagged, versioned | Per Stream B implementation gaps | Rob + Claude (browser + Code) | Living + section history | Universal (`.dev-knowledge` only) |
| `JOURNAL.md` | Tactical per-session log | Append-only, dated entries: Did/Failed/Next | Every Claude Code session | Future Claude Code (last 5 entries on startup) | Append-only (oldest top, newest bottom) | Per-repo (Scale L mandatory; Scale M optional; Scale S no) |
| `CHANGELOG.md` | Notable changes, release-note style | Newest-first dated entries | Per noteworthy commit | Rob, future contributors | Newest-first (prepend) | Per-repo |
| `LESSONS.md` | Process lessons learned | Append-only with `[scope: X]` inline (per ADR-29) | When new lesson emerges (auto-promote at 2× repeat) | Rob, future Claude | Append-only | Universal (`.dev-knowledge` only) |
| `TOKEN-LOG.md` | Claude usage snapshots | Threshold-triggered (7-day) via /session-summary | Auto when stale | Rob | Newest-first (prepend) | Universal (`.dev-knowledge` only) |
| `ENVIRONMENT.md` | Tooling state, what's installed | Sectioned, scope-tagged | When tool adopted/deprecated | Rob, Claude Code | Living (sections updated) | Per-repo |
| `docs/decisions/ADR-NN_*.md` | Architectural decisions | Michael Nygard format | When decision binds | Rob, future contributors | Numbered, immutable (amend in-place per ADR-29) | Per-repo |
| `docs/decisions/transcripts/DECISION_NN_*.md` | Raw Council debate outputs | Multi-model debate transcript | When Council debate concludes (per PLAYBOOK 5.N archival) | Reference for ADR rationale | Numbered, immutable | Per-repo |
| `docs/handoffs/YYYY-MM-DD-*.md` | Chat-to-chat session summary | Tiered (Scale-dependent) | When session boundary requires continuity | Next browser chat | Dated, immutable | Per-repo |
| `docs/audits/YYYY-MM-DD-*.md` | Point-in-time analyses | Free-form audit | When deep analysis needed | Reference for follow-up work | Dated, immutable (mark SUPERSEDED if redone) | Per-repo |
| `docs/research/YYYY-MM-DD-*.md` | Research outputs (Council research mode, standalone reports) | Free-form research | When research generates value | Reference for design decisions | Dated, immutable | Universal (`.dev-knowledge` only — research is methodology) |

### Scale tier presence matrix
<!-- scope: meta -->

Which files exist per Scale tier (per `Project Scale Tiers` section above):

| File | Scale S | Scale M | Scale L |
|------|---------|---------|---------|
| `README.md` | required | required | required |
| `CLAUDE.md` | required | required | required |
| `AGENTS.md` | optional | required | required |
| `ESSENTIALS.md` | n/a (universal `.dev-knowledge`) | n/a | n/a |
| `PLAYBOOK.md` | n/a (universal `.dev-knowledge`) | n/a | n/a |
| `JOURNAL.md` | not used | optional | required |
| `CHANGELOG.md` | optional | required | required |
| `LESSONS.md` | n/a (universal `.dev-knowledge`) | n/a | n/a |
| `TOKEN-LOG.md` | n/a (universal `.dev-knowledge`) | n/a | n/a |
| `ENVIRONMENT.md` | optional | recommended | required |
| `docs/decisions/` | optional | recommended | required |
| `docs/handoffs/` | optional | recommended | recommended |
| `docs/audits/` | optional | optional | recommended |

**Reading the matrix:**
- **required** — file presence is non-negotiable for the Scale tier
- **recommended** — strong default; absence requires explicit rationale
- **optional** — use when value clear, skip otherwise
- **not used** — actively avoid (overkill at this Scale)
- **n/a (universal)** — file lives in `.dev-knowledge`, not per-repo

### Common confusions resolved
<!-- scope: meta -->

**JOURNAL vs handoff:**
- JOURNAL = within-repo, per-session tactical log. Continuity across Claude Code sessions in same repo.
- handoff = across-context, browser-chat-to-browser-chat session summary. Continuity when switching chats.
- Both can coexist. Scale L typically uses both. Scale S/M usually one or the other (often handoffs).

**LESSONS vs ADR:**
- LESSONS = process lessons (how Rob works, anti-patterns, what tooling drift looked like). Append-only.
- ADR = architectural decisions (technical commitments). Amendable per ADR-29 pattern.
- Process generalization → LESSONS. Technical commitment → ADR.

**CHANGELOG vs JOURNAL:**
- CHANGELOG = strategic, what user/contributor needs to know about repo evolution. Newest-first.
- JOURNAL = tactical, what Claude Code did session-by-session. Append-only chronological.
- Same commit might warrant entries in both — different abstraction levels.

**audits vs research:**
- audits = backward-looking analysis of current state (per-repo, dated)
- research = forward-looking exploration (universal in `.dev-knowledge`, dated)
- Council research-mode debates → research/. Council pick-mode debates → transcripts/.

### Order conventions
<!-- scope: meta -->

Per Token-LOG flip 2026-04-24:

- **Newest-first (prepend):** TOKEN-LOG, CHANGELOG. Rationale: logs optimize for current-state scanning.
- **Append-only (oldest top):** LESSONS, JOURNAL. Rationale: chronological narrative; order preserves "what we learned when."
- **Living (in-place updates):** README, CLAUDE.md, AGENTS.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT. Rationale: not logs; current state matters more than history.
- **Immutable (dated):** ADRs, transcripts, handoffs, audits, research. Rationale: point-in-time records; supersession via new file or in-file marker.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 12-file taxonomy + Scale matrix + 4 common confusions + order conventions. Will refine after live use.

---

## Session boundaries
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

**Why these numbers:** observed empirically from 2026-04-24 session. Quality of decisions visibly degraded after these thresholds — including by the "decider's" own self-assessment in retrospect.

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
2. Read AGENTS.md (auto)
3. `git status` and `git log --oneline -5`
4. Read most recent handoff if exists
5. Read JOURNAL.md last 5 entries (if file exists per Scale)
6. Wait for prompt — never improvise

**Anti-pattern:** opening new session with bare prompt "continue what we were doing" — without uploading context, both sides reconstruct from memory (browser) or scratch (Claude Code). Quality drops fast.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. 5 subsections: scope declaration, stop-signs, decision fatigue threshold, recursive planning anti-pattern, session resumption protocol. Codifies patterns observed in 2026-04-24 sessions. Will refine after live use.

---

## Continuous Improvement
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

New tools, models, agents, and patterns emerge constantly in 2025-2026 LLM dev (Claude Code releases, OpenAI Codex updates, Chinese models like GLM/Qwen, MCP servers, multi-agent frameworks, Spec Kit/Kiro). Without explicit process, adoption thrashes (re-evaluating same tool quarterly), forgets context (why did we reject MCP memory?), or misses signals (relevant tool sat in tech-radar chat unread for weeks).

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

**Capture:** when something looks interesting, drop a one-liner into the next quarterly tech-radar entry under "discovered, not yet triaged" — don't wait for full evaluation.

### Stage 2: Triage
<!-- scope: meta -->

**Criteria for "worth evaluating":**
- **Maturity:** v1.0+, ≥100 GitHub stars, or backed by recognized org
- **Addresses real problem:** maps to existing Rob pain point or unblocks identified gap
- **Scale fit:** works for solo developer (not team-only)
- **Platform fit:** runs on Windows/PowerShell (or has portable equivalent)
- **Cost-bounded:** trial cost <$50 OR API trial available

If 4+ criteria met → proceed to Evaluation. If 3 or fewer → mark "deferred" with reason in tech-radar.

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
- Output: archived to `docs/research/YYYY-MM-DD-{topic}.md` per PLAYBOOK 5.N

Decision threshold for which mode: per PLAYBOOK Section 5 "When to run Council vs single-model + critic."

### Stage 4: Decision
<!-- scope: meta -->

Three outcomes:

- **Adopt:** triggers Implementation (Stage 5)
- **Reject:** record in tech-radar with reason; closed unless evidence changes
- **Defer:** record in tech-radar with explicit reopen trigger (e.g., "if cost drops below X" or "after solo→team transition")

**Document the decision:** even rejection deserves a paragraph. Future self asks "why didn't we adopt MCP memory?" — answer must exist.

### Stage 5: Implementation (only for "Adopt")
<!-- scope: meta -->

Standard pipeline:
1. **ADR if architectural impact** (per Section 5 gating) — module boundaries, dependencies, data model
2. **Brief Stream B-style gap entry** if it requires multiple changes across files
3. **Updates to:** AGENTS.md (Section 5: tools active), CLAUDE.md (if Claude Code-specific), ENVIRONMENT.md (if env-level), JOURNAL/CHANGELOG entries
4. **Hooks/tests/CI** if enforcement needed (LLMs advise; mechanism enforces, per Council #28)

Cross-link from tech-radar entry to the ADR + implementation commits.

### Stage 6: Review (periodic)
<!-- scope: meta -->

**Cadence:** quarterly tech-radar snapshot (`docs/tech-radar/YYYY-Q.md`).

**Per quarter, for each Adopted item:**
- Still earning its keep? (concrete value vs cost/maintenance)
- Configuration drift? (deprecated flags, version skew)
- Replacement candidate emerged?

**Per quarter, for each Deferred item:**
- Reopen trigger met?
- Still relevant or made obsolete by adoption of alternative?

**Per quarter, for each Rejected item:**
- Re-check if rejected for "wrong reason at the time" (rare but happens)

**Output:** updated tech-radar quarterly entry. NOT each time something changes — quarterly batch keeps cost down.

### Tech radar folder
<!-- scope: meta -->

Location: `docs/tech-radar/`

**File pattern:** `YYYY-Q.md` for quarterly snapshots; `YYYY-MM-DD-{tool}.md` for per-tool deep-dives when warranted (e.g. Spec Kit eval).

**Distinct from `docs/research/`:**
- `docs/research/` — research-mode debate outputs (point-in-time, rich content)
- `docs/tech-radar/` — quarterly inventory of what's adopted/rejected/deferred (snapshot)

A tool might appear in BOTH (research debate evaluating it; tech-radar entry recording the decision and tracking subsequent review).

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 6-stage pipeline, source list, evaluation modes by stake, tech-radar folder convention. Codifies organic 2026-Q1/Q2 adoption practice (Codex, Tach, Opus 4.7, ccusage, Perplexity, MCP-memory-deferred, GLM/Qwen-deferred, Spec Kit-evaluated).

---

## Claude Code internals
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
| **Subagent** | Separate Claude instance with narrow focus | `.claude/agents/` | Invoked via Task tool from main agent |

**User-level vs project-level:**
- User-level: `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/settings.json` — applies across all repos
- Project-level: `<repo>/.claude/skills/`, `<repo>/.claude/commands/`, etc. — applies only in that repo
- Both can coexist; project-level takes precedence when names collide

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
- Universal Rob rules — those go in `.dev-knowledge/PLAYBOOK.md`
- One-off task — slash command may fit better

**Real example in Rob's ecosystem:**
- `corp-monorepo/.claude/skills/gotchas/SKILL.md` — empirical patterns this repo has stumbled on (~30 entries, Trigger/Symptom/Fix/verify pattern)

**Anti-patterns:**
- **Skill files >500 lines** — defeats progressive disclosure; split to references/
- **Skills with no trigger description** — Claude Code can't know when to read it
- **Universal content as project skill** — should live in `.dev-knowledge/PLAYBOOK.md` instead

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
- Operations crossing multiple files/tools (e.g. session summary, /boot context loading)

**When NOT to use:**
- One-off task — write inline prompt instead
- Knowledge lookup — use skill instead
- Content best fits CLAUDE.md auto-read

**Real examples in Rob's ecosystem (user-level, `~/.claude/commands/`):**
- `/session-summary` — generate handoff for current session, include TOKEN-LOG snapshot if stale (renamed from `/handoff` 2026-04-24 to avoid trigger-word collision)
- `/boot` — load context: skills, recent commits, JOURNAL entries
- `/evolve` — promote learned patterns to skills/rules
- `/review` — invoke Codex review on staged changes

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
- `.dev-knowledge/.pre-commit-config.yaml` — runs `scripts/validate_scope_tags.py` (Stream A enforcement)
- corp-monorepo pre-commit (likely): ruff format, pytest collection check (verify per repo)

**Anti-patterns:**
- **Hooks bypassed with `--no-verify`** — defeats the safety net; should never be habit
- **Hooks slower than 5s** — incentivizes bypass; move to CI
- **Validator/hook divergence** — both tools must enforce identically (see ADR-27 amendment 2026-04-25, lesson re: invocation semantics)

### 7d. Subagents (separate Claude instances)
<!-- scope: runtime -->

**Amendment 2026-04-25 (subagents factually active):** Original v1.0 section called subagents "DEFERRED — no active subagents in Rob's ecosystem." This was incorrect. Verification 2026-04-25 confirmed two active user-level subagents exist at `~/.claude/agents/`. Section now describes actual subagents (Anthropic docs framing preserved as conceptual context). Per Gap #19 amendment-vs-reopen protocol: prescription drift, intent (disambiguation of 4 mechanisms) preserved.

**What (per Anthropic docs + Council #28 research):** Subagents are spawned Claude instances with narrow focus and fresh context window, invoked via main agent's Task tool. Designed for "read-heavy, write-light" delegation (per Cognition's June 2025 warning against subagents-as-code-generation-peers).

**Where they live:** `~/.claude/agents/<name>.md` (user-level, cross-repo) OR `<repo>/.claude/agents/<name>.md` (project-level).

**File format:** Markdown files describing the subagent's role, trigger conditions, and instructions. Main agent invokes them via Task tool.

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

**Distinct from PLAYBOOK Section 6 Continuous Improvement** — that covers external tool/model adoption (Codex, Tach, ccusage). This subsection covers Claude Code's own extension mechanisms.

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
- Universal Rob workflow (e.g. `/session-summary`, `/boot`)

**Project-level** (`<repo>/.claude/<mechanism>/`) when:
- Pattern is repo-specific (corp-monorepo Tach layers, ai-council debate framework)
- Sensitive content shouldn't leak to other repos
- Repo's AGENTS.md/CLAUDE.md needs to reference it explicitly

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
- **AGENTS.md Section 5 ("Tools active in this repo")** — for project-level adoptions; cross-tool agents (Codex, Cursor, Aider) become aware
- **CLAUDE.md** — for project-level Claude Code-specific behavior (per Gap #5 template Sections 5/6/7)
- **JOURNAL.md entry** for the session that adopted it
- **CHANGELOG.md entry** for repo-visible adoptions
- **tech-radar 2026-Q?.md** Adopted (active inventory) section if user-level (per Gap #17 Continuous Improvement Section 6)

User-level adoptions don't need per-repo AGENTS.md updates (they apply everywhere automatically) but do warrant tech-radar entry for periodic value review.

#### Anti-patterns
<!-- scope: meta -->

- **Adoption without triage** — every Claude proposal becomes a new file; ecosystem bloats
- **Project-level when should be user-level** — duplicates same skill across 3 repos; one source of truth lost
- **User-level when should be project-level** — leaks repo-specific knowledge into universal scope
- **Skip validation** — broken hook/command/skill propagates and fails silently for weeks
- **Forget documentation step** — Codex/Cursor never learn about the new tool; cross-tool awareness breaks

#### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. 5-stage pipeline (Triage → Decision → Validation → Install → Document) with cross-reference to Gap #17 (broader tool adoption). Anti-patterns from observed practice. Will refine after live use.

### Cross-reference to AGENTS.md template Section 5
<!-- scope: meta -->

When a repo has any of the above active (skills, slash commands, hooks, subagents), they get listed in `AGENTS.md` Section 5 "Tools active in this repo" per Gap #6 template. Specifically:

- **Code review:** Codex configuration → see `templates/codex-review-config-template.md`
- **Architecture enforcement:** Tach configuration if used
- **Pre-commit hooks:** list active hooks with purpose
- **Skills:** list active skills with paths
- **Subagents:** list if any are active (per Rob's ecosystem currently: ecosystem-snapshot, report-generator at user-level)

This keeps cross-tool agents (Codex, Cursor, Aider) aware of the same governance Claude Code operates under.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 4 subsections: skills, slash commands, hooks, subagents (deferred). Disambiguation table at top. Real examples from corp-monorepo (gotchas skill), user-level (/session-summary, /boot, /evolve, /review), .dev-knowledge (scope tag pre-commit hook). Subagents documented from Anthropic docs + Council #28 research, no Rob ecosystem instance.

---

## 1. Starting a New Project
<!-- scope: dev -->

**Every project begins with CLAUDE.md, not code.** If you can't describe what the project does in 3 sentences, you don't understand it yet. For architectural decisions (new database? new package? new integration?), run an AI Council debate before writing a single line.

### Scaffold
<!-- scope: dev -->

```bash
mkdir -p my-project/src/my_package my-project/tests my-project/config my-project/scripts
touch my-project/{CLAUDE.md,README.md,CHANGELOG.md,pyproject.toml,.gitignore}
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
8. Delete branch, update CHANGELOG.md if files changed

---

## 2. Creating a Claude Code Prompt
<!-- scope: hybrid -->

**Rob's prompt format is non-negotiable.** Front-loading the full spec in the first message eliminates 2-3 discovery turns. Every prompt starts with a summary table that determines execution parameters.

### Summary table (required at top of every formal prompt)
<!-- scope: hybrid -->

```
| Parameter | Value                               |
| --------- | ----------------------------------- |
| Model     | Sonnet / Opus                       |
| Mode      | auto-accept / plan-then-auto / plan |
| Effort    | low / medium / high / xhigh         |
```

### How to choose Model
<!-- scope: llm -->

- **Sonnet** — single-file changes, mechanical refactors, test writing, boilerplate generation, file renames, config updates, code review
- **Opus** — multi-package changes, complex debugging, architecture decisions, anything requiring reasoning across 3+ files, novel logic design

Rule of thumb: if the task is "do X the way we always do it" → Sonnet. If the task is "figure out the right approach, then do it" → Opus.

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

### Structure
<!-- scope: hybrid -->

```
| Parameter | Value  |
| --------- | ------ |
| Model     | [pick] |
| Mode      | [pick] |
| Effort    | [pick] |

TITLE: What we're doing
REPO: Which repo/package
PURPOSE: Why (1 sentence)

→ Read CLAUDE.md + relevant gotchas
→ Git workflow (branch, commit per step, pytest between)

UNDERSTAND:
- What's the problem?
- What's the scope? (which files, which packages)
- What are the risks?
- What does failure look like?

STEPS:
1. [action] — COMMIT: "feat: description"
2. [action] — COMMIT: "feat: description"
...

FINAL: Run full test suite, merge to main

WHAT NOT TO DO:
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
- CHANGELOG.md entry required in FINAL section if files changed
- Bypass permissions (no approval) → almost never, only for trivial read-only operations

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

If you find yourself writing a lesson that sounds like "always do X" or "never do Y" — it might be a rule, not a lesson. Write the lesson in LESSONS.md for context, then also add it to `~/.claude/` (gotchas, rules/, or learned-rules.md) with a verify: line. Cross-reference both.

---

## 5. Running an AI Council Debate
<!-- scope: llm -->

**Council debates are valuable but can become procrastination.** Hard rule: max 2 debates before implementation starts. Full format guide lives in the council project's docs/ folder.

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
2. Create ADR summary → `docs/decisions/ADR-{NN}_{topic}.md`
3. Archive transcript → `docs/decisions/transcripts/`
4. `git add + commit` both immediately
5. Never reopen a decided topic unless new evidence appears

### Council Debate Archival Protocol
<!-- scope: llm -->

Every Council debate output MUST be archived immediately after the debate completes. Skip this and the debate is effectively lost. Retroactive archive 2026-04-24 recovered 5 debates that sat in `ai-council/output/` for weeks.

**Pipeline (3 steps, ~5 min):**

1. **Identify target location** within .dev-knowledge:
   - Debate about .dev-knowledge itself (pick/judge mode) → `docs/decisions/transcripts/DECISION_NN_slug.md`
   - Research-mode debate → `docs/research/YYYY-MM-DD-slug.md`
   - Debate about another repo (e.g., corp-monorepo architecture) → `docs/research/YYYY-MM-DD-council-NN-slug-REPO.md`
     - Suffix with `-REPO` indicates decision applies elsewhere
     - Future work: mirror to that repo's transcripts/ folder

2. **Copy** `ai-council/output/YYYYMMDD_HHMMSS_source.md` to target:
   - Decisions: `DECISION_NN_snake_case.md` (NN optional if no sequential numbering)
   - Research: `YYYY-MM-DD-kebab-case-slug.md`
   - Byte-exact copy, preserve original in ai-council/output/

3. **Commit** with message: `docs: archive Council #NN — [topic]`

**Optional follow-up (separate commit):**
- Pick-mode with clear decision → write ADR in `docs/decisions/` referencing transcript
- Research-mode → no ADR, transcript/report suffices
- Judge-mode → depends on verdict

**Anti-pattern:** Accumulating 2+ un-archived debates in `ai-council/output/`. If detected, run retroactive archive before the next Council session.

**Future enforcement:** possible pre-commit hook checking ai-council/output/ for files >7 days old not present in any repo's archive locations.

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
| AGENTS.md template structure (10 sections) | Browser + Rob | Well-known community pattern (Council #28 research), no need to re-debate |

#### Anti-patterns
<!-- scope: meta -->

- **Council habit-formation** — running Council because "it's how we decide" without checking the gate. Costs add up fast ($0.50 × N decisions).
- **Single-model laziness** — choosing single-model path when criteria genuinely apply (architectural ripple), then later reopening as Council = wasted first decision.

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
2. Block structure:

   > **Amendment YYYY-MM-DD ([brief topic]):** [What was wrong/unclear in original prescription]. Resolution: [what the prescription now says]. Intent preserved: [why this is amendment not reopen].

3. Update validator/tool/process to match amendment
4. Add LESSONS.md entry (per ADR-29 format) describing what was discovered
5. CHANGELOG entry: "ADR-NN amended YYYY-MM-DD — [topic]"

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
- **CHANGELOG.md** if findings affected user-visible behavior

#### Anti-patterns
<!-- scope: meta -->

- **Archive everything** — low-severity polish findings don't warrant an audit document; archive only when trigger criteria match
- **Archive without resolution tracking** — review without clear "what was fixed / what's deferred" loses accountability
- **Codex output rot** — letting findings linger across sessions without resolution status creates ambiguity over what's still open

#### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. Manual archival protocol mirroring Council Archival pattern. Future enhancement: pre-commit hook checking for un-archived Codex sessions older than N days.

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

1. Review recent CHANGELOG.md entries
2. Read CLAUDE.md
3. Check gotchas
4. `git status` (must be clean)
5. Define 1-2 objectives for this session — everything else is backlog

### During session
<!-- scope: hybrid -->

- `/clear` between unrelated tasks (saves 30-40% input tokens)
- Commit after each logical change
- Test after each change (not at the end)
- If scope creeps: "Adding to OPEN_DECISIONS.md, not doing today"
- Use Plan Mode before implementation (catches bad approach at 200 tokens vs 5000)
- Use line ranges (`@file:15-80`) instead of whole files

### When context gets heavy
<!-- scope: hybrid -->

- `/compact` at 40% (aggressive, Council-approved)
- `/session-summary` before switching to Claude.ai for architecture consulting
- If Claude says "it's done" on a complex operation — VERIFY with filesystem commands

### Session end protocol
<!-- scope: hybrid -->

1. Run full test suite
2. Update CHANGELOG.md if files changed
3. Update project handoff doc (if exists)
4. `git status` (must be clean — if "27 modified files", STOP and commit)
5. Write 3-line handoff note

---

## 8. Handing Off Between Sessions
<!-- scope: hybrid -->

**Claude Code executes. Claude.ai architects and challenges.** Three handoff scenarios exist.

### Roles
<!-- scope: hybrid -->

- **Claude Code (terminal):** reads files, runs commands, edits code, verifies state, runs tests. Trusts filesystem, not memory.
- **Claude.ai (browser):** architecture consulting, strategic decisions, critical thinking. **ALWAYS maintains critical thinking** — questions the approach, identifies risks, says "no" when something doesn't make sense. Never rubber-stamps.

### Handoff A: Claude Code → Browser
<!-- scope: hybrid -->

1. In Claude Code: `/session-summary` → generates token-efficient state summary
2. Paste into Claude.ai browser chat
3. Discuss architecture, strategy, decisions
4. Decisions go back to Claude Code as prompts (Section 2 format)

### Handoff B: Browser → New Browser (Council Decision #24)
<!-- scope: hybrid -->

**Chats die. Handoffs preserve momentum.** Don't wait until the chat is slow — checkpoint at ~2 hours while context is still fresh.

**Trigger:** Say `wygeneruj handoff`. Claude generates everything — Rob makes zero formatting decisions.

**What Claude generates:** A single markdown code block, <100 lines, strictly English. Sections auto-adapted to chat content:

```
HANDOFF — [topic]
Date: YYYY-MM-DD

OBJECTIVE: [one sentence — what this chat was trying to accomplish]
[If context is degraded: "CONTEXT LOST — objective reconstructed from partial context"]

STATUS: [where we are right now]

DECISIONS:
- [decision]. *(Changed from X because Y.)* ← only if reversed
- [decision]

OPEN TASKS:
- [what remains to be done]
- [what was deferred]

FILES / ARTIFACTS:
- [filepath] — [what it is]
- [filepath] — [what it is]

KEY CONTEXT: [max 5 bullets of non-obvious context the new chat needs]
```

**Transfer:** Click "Copy" button on the code block → open new chat → paste. Two steps.

**Rules:**
- No archiving step. Generate → Copy → Paste. That's it.
- Claude auto-sizes: simple chat (~30 lines), complex chat (~80-100 lines)
- If Claude can't see early objectives due to context limits, it writes `[CONTEXT LOST]` instead of hallucinating
- Output is always in English, even if conversation was in Polish
- Never inline full prompts or session logs — list file paths only

### Handoff C: Browser → Claude Code
<!-- scope: hybrid -->

- Claude.ai writes prompts using Section 2 format (Model/Mode/Effort table)
- Prompts should be QUESTIONS, not COMMANDS
- Good: "What's in the docs folder? Report structure."
- Bad: "Move benchmark.md to eval/"
- Let Claude Code discover actual state, then propose actions

### Token log cadence
<!-- scope: meta -->

Every /session-summary run checks TOKEN-LOG.md staleness. If latest entry >7 days old, a new short-format snapshot is appended via `ccusage --json`. Otherwise skipped.

**Trigger:** /session-summary staleness check; conditional execution (not every session).

**Source:** `ccusage --json` (reads local Claude Code usage data — see ENVIRONMENT.md)

**Threshold:** 7 days. Most recent entry's date extracted from first `## YYYY-MM-DD` header line in TOKEN-LOG.md.

**Format (short, sustainable):**

```
## YYYY-MM-DD (since YYYY-MM-DD delta)

Cost: $X.XX | Sessions: N | Active days: N
Tokens (in+out): X.XM
Top models: Model-A X%, Model-B Y%, Model-C Z%
Peak day: $X.XX on YYYY-MM-DD
Notable: [1-2 line signal e.g. "Opus 4.7 adoption curve", "Haiku routing shift"]
```

**Order convention:**
- TOKEN-LOG.md and CHANGELOG.md: newest-first (prepend). Rationale: logs optimize for current-state scanning.
- LESSONS.md: append-only (oldest-first). Rationale: chronological narrative; order preserves "what we learned when".

New TOKEN-LOG entries go at the top (after file header, before previous newest entry). /session-summary reads the first matching `## YYYY-MM-DD` header for the staleness check.

**Cache tokens** excluded from in+out for cross-period comparability. Note cache only when notable.

**Rationale:**
- Per-session cadence rejected: ~$0.02/run overhead wasteful for weekly-sufficient data
- Manual weekly ritual rejected: forgetting risk (4 weeks stale before ccusage adoption)
- Threshold-based: amortized ~$0.006/run, auto-triggers on staleness, zero forgetting risk
- Short format keeps entries scannable over months; full format reserved for migrations

---

## 9. Weekly Review (Friday)
<!-- scope: hybrid -->

**Friday consolidation — 30 minutes max, not a project.**

1. Run `/evolve` in Claude Code — review corrections, observations, propose rule promotions/pruning
2. Review gotchas added this week — any patterns?
3. Review token usage — `ccusage --json` → append snapshot to TOKEN-LOG.md. Is Opus verbosity still the main drain?
4. Review LESSONS.md entries from this week — anything to change in PLAYBOOK?
5. Review OPEN_DECISIONS.md — anything stale? Anything urgent?
6. Quick project health check (test suite, lint, stale branches)
7. Update ENVIRONMENT.md if any config changed

---

## 10. Evaluating a New Tool/Framework/Model
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

## 11. Multi-Project Rules
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

## 12. Where Knowledge Lives
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

A lesson in LESSONS.md is human context (why, what happened). A rule in `~/.claude/` is machine-executable (verify: line, gotcha check). When a lesson matures into a rule:
1. Keep the lesson entry in LESSONS.md (provenance)
2. Add the rule to `~/.claude/rules/`, `gotchas.md`, or `learned-rules.md` with verify: line
3. Cross-reference both with file path

### Data sanitization
<!-- scope: meta -->

If a client engagement generates a dev lesson, strip all client names, proprietary schemas, and identifying details before writing to `.dev-knowledge/`.

### Migration triggers
<!-- scope: meta -->

- **20 files** in `.dev-knowledge/` → evaluate creating a dedicated Obsidian DevVault
- **50 entries** in LESSONS.md → split into topic files
- Rob opens Obsidian to search for dev methodology → immediate signal DevVault is needed

---

## 13. Markdown Governance
<!-- scope: dev -->

**Every markdown file in the project falls into exactly one category.** If you're about to create a .md file and it doesn't fit any category below — it probably shouldn't exist.

| Category          | Location        | Naming                                         | Lifecycle                      |
| ----------------- | --------------- | ---------------------------------------------- | ------------------------------ |
| Project docs      | Root            | CLAUDE.md, README.md, CHANGELOG.md             | Living, never delete           |
| Decision records  | docs/decisions/ | ADR-{NN}_{topic}.md                            | Frozen, never edit             |
| Handoff           | docs/           | HANDOFF.md                                     | Living, update in place        |
| Snapshots/reports | docs/archive/   | {YYYY-MM-DD}_{TYPE}_{topic}.md                 | Frozen, delete after 90 days   |
| Eval data         | eval/           | eval_history.jsonl                             | Append-only, keep indefinitely |
| Ephemeral prompts | Not in repo     | PROMPT_{topic}.md                              | Delete after execution         |

**Two date rules, no exceptions:**
- Frozen/snapshot files → date in filename: `2026-03-28_CLEANUP_PLAN.md`
- Living files → date in YAML frontmatter: `last_updated: 2026-03-28`

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

---

## 14. Anti-Patterns — What NOT to Do
<!-- scope: hybrid -->

**"I'll organize later"** — If you create a file without knowing where it belongs, you'll never organize it. Know the category BEFORE creating.

**"Let's put it in docs/ for now"** — `docs/` is not a staging area. It has defined categories: handoff, archive, decisions. If it doesn't fit one, it doesn't belong there.

**"Let's name it descriptively"** — `ARCHITECTURE_REVIEW.md` is useless without a date. `2026-03-21_ARCHITECTURE_REVIEW.md` is findable.

**"We can consolidate these output folders later"** — Output dirs grow exponentially. Set a single canonical output path at project creation.

**"The AI will remember"** — It won't. Not after 4 hours. Not across sessions. Not after compaction. Write it down in CHANGELOG.md or CLAUDE.md.

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
6. **Log changes continuously.** CHANGELOG entry when files change, LESSONS entry when something was learned.
7. **Scope is sacred.** 1-2 objectives per session. Everything else is backlog.
8. **Verify with Claude Code, plan with Claude.ai.** Don't let Claude.ai generate filesystem commands from memory.
9. **Output dirs are disposable.** Canonical location, gitignored, size-monitored, regularly cleaned.
10. **If the AI says "it's done" — verify.** The longer the session, the less you should trust it.

---

## 15. Cross-Tool Review **[L+M]**
<!-- scope: dev -->

**When:** Feature branch touches 3+ files OR 2+ packages OR safety-critical paths (vault writes, OneDrive ops, cleanup/delete)
**Skip when:** Single-file fix, test-only changes, documentation updates

### Review Tools
<!-- scope: dev -->

Two options for code review (A/B test both, then standardize):

**Option A — /ultrareview (Claude Code built-in):**
Cloud-based multi-agent review. Run without arguments (current branch) or with PR number. No second terminal needed.

**Option B — Codex CLI (automated, single command):**
`codex-review -Topic <topic>` (slash command: `/review`) wraps `codex exec --output-last-message`. Produces dated, frontmatter-wrapped audit at `docs/audits/YYYY-MM-DD-codex-{topic}.md`. Read-only sandbox. Opt-in `-AutoCommit`. Requires ChatGPT Plus subscription. See `~/.claude/bin/codex-review.README.md`.

Both satisfy S15 review requirement. Choose based on quality of findings after 2-week A/B test.

Codex/ultrareview reviews. Claude Code builds. Never reverse the roles.

---

## 16. Code Quality Audit Process
<!-- scope: dev -->

**When:** Monthly full audit **[L only]** · On-demand before major refactors **[L+M]** · S projects skip.
**Tool:** Codex CLI or Codex Desktop (independent reviewer — no authorship bias)
**Cycle:** Read-only audit → triage by severity → fix by tier → re-audit

### Severity tiers
<!-- scope: dev -->
- **CRITICAL** — data loss, security, broken imports that fail at runtime
- **HIGH** — wrong dependency direction, missing tests on public API, type errors
- **MEDIUM** — style violations, redundant code, unclear naming
- **LOW** — suggestions, nitpicks, debatable patterns

### Process
<!-- scope: dev -->
1. Run audit (read-only): `codex "Audit this repo against AGENTS.md rules. Output findings by severity. Do not fix anything."`
2. Triage output manually — expect ~30% false positives. Demote miscalibrated patterns in AGENTS.md.
3. Fix CRITICAL and HIGH first. One commit per logical group.
4. Re-run audit. Confirm flags resolved.
5. Update ARCHITECTURE.md if module boundaries or dependency direction changed. **[L+M]**

### Rules
<!-- scope: dev -->
- Audit-first, fix-second. Never fix while auditing.
- Claude Code fixes. Codex audits. Never reverse the roles.
- Structural changes with N>5 call sites: shim first, migrate incrementally, remove shim last.
- Any session touching module boundaries must produce or update ARCHITECTURE.md. **[L+M]**

### Post-Structural-Change Documentation
<!-- scope: dev -->

After any change that moves, renames, or reorganizes files or modules, update documentation that describes the changed structure:

- **L:** Update ARCHITECTURE.md + affected module READMEs in src/*/
- **M:** Update ARCHITECTURE.md if it exists
- **S:** No structural docs to update beyond CHANGELOG.md

This is not optional for the applicable tier. Stale structural documentation is worse than no documentation — it actively misleads.

---

## Appendix A: Claude Code Shortcuts
<!-- scope: runtime -->

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
| `/boot`            | Session start — load memory, verify rules         |
| `/clear`           | Between repos/tasks — #1 token saver              |
| `/compact`         | Mid-session when context heavy                    |
| `/compact [focus]` | Compress with focus ("focus on API changes")      |
| `/evolve`          | Weekly Friday — review corrections, promote rules |
| `/session-summary` | Before switching to Claude.ai browser             |
| `/stats`           | Check token usage (interactive TUI; use `ccusage --json` for scriptable export) |
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

From ~/.claude/ROUTING.md — deterministic, no judgment calls.

| Task                              | Model          | Examples                                                           |
| --------------------------------- | -------------- | ------------------------------------------------------------------ |
| No AI needed                      | —              | .gitignore edits, git ops, file moves, config tweaks (<60s manual) |
| Reports, snapshots                | Haiku subagent | Test summaries, doc condensation, ecosystem snapshots              |
| Implementation, debugging, review | Sonnet         | All code review (security boundary), test creation, refactoring    |
| Architecture, cross-repo design   | Opus           | Ecosystem reasoning, complex debugging, novel logic                |
| Large doc extraction              | Gemini Flash   | Domain-specific extraction pipelines (PPTX/MP4/PDF)                |
| Council synthesis                 | Gemini         | Cost: $0.04 vs Claude $0.23/debate                                 |

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