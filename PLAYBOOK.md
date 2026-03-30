# Dev Practice Playbook

> **Living document.** Repeatable processes for everything Rob does regularly with AI-assisted development.
> Last updated: 2026-03-29

---

## Project Scale Tiers

Every project declares its scale in its CLAUDE.md:

```
## Project Scale: L
```

Three tiers:
- **L (Large):** Multi-package repo, 500+ tests, cross-package dependencies. Has ARCHITECTURE.md, per-module READMEs, AGENTS.md for external reviewers.
- **M (Medium):** Standalone package, 50-500 tests, multiple modules, one namespace. May have ARCHITECTURE.md.
- **S (Small):** Single script or tool, <50 tests, simple flow. Minimal docs beyond CLAUDE.md and CHANGELOG.md.

Sections in this Playbook marked with a tier tag (e.g. **[L only]** or **[L+M]**) apply only to those tiers. Unmarked sections apply to all projects.

---

## 1. Starting a New Project

**Every project begins with CLAUDE.md, not code.** If you can't describe what the project does in 3 sentences, you don't understand it yet. For architectural decisions (new database? new package? new integration?), run an AI Council debate before writing a single line.

### Scaffold

```bash
mkdir -p my-project/src/my_package my-project/tests my-project/config my-project/scripts
touch my-project/{CLAUDE.md,README.md,CHANGELOG.md,pyproject.toml,.gitignore}
touch my-project/src/my_package/{__init__.py,cli.py}
touch my-project/tests/conftest.py
```

### CLAUDE.md template (minimum viable)

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

**Rob's prompt format is non-negotiable.** Front-loading the full spec in the first message eliminates 2-3 discovery turns. Every prompt starts with a summary table that determines execution parameters.

### Summary table (required at top of every formal prompt)

```
| Parameter | Value                               |
| --------- | ----------------------------------- |
| Model     | Sonnet / Opus                       |
| Mode      | auto-accept / plan-then-auto / plan |
| Effort    | low / medium / high                 |
```

### How to choose Model

- **Sonnet** — single-file changes, mechanical refactors, test writing, boilerplate generation, file renames, config updates, code review
- **Opus** — multi-package changes, complex debugging, architecture decisions, anything requiring reasoning across 3+ files, novel logic design

Rule of thumb: if the task is "do X the way we always do it" → Sonnet. If the task is "figure out the right approach, then do it" → Opus.

### How to choose Mode

- **auto-accept** — read-only tasks, mechanical changes with clear spec, file moves/renames, formatting. You know exactly what should happen, Claude just executes
- **plan-then-auto** — design decisions embedded in a prompt. Start in plan mode for the UNDERSTAND + PLAN phases, review the plan, then switch to auto-accept for execution. This is the default for most multi-step prompts
- **plan** (manual approval each step) — risky operations touching production data, OneDrive paths, database migrations, anything with blast radius. Also for learning/exploration where you want to see each step

### How to choose Effort

- **low** — single file, <30 min, no architectural decisions. Example: "add a CLI flag", "fix this test", "rename this variable across the file"
- **medium** — 2-5 files, 30-90 min, may involve design choices within known patterns. Example: "add a new CLI command", "refactor this module to use dataclasses"
- **high** — 5+ files or 2+ packages, 90+ min, requires UNDERSTAND phase, potential blast radius. Example: "implement search federation", "migrate classifier to new taxonomy"

### Structure

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

- **1 file change** → conversational ("hey, fix X in Y") — no summary table needed
- **2-3 files** → conversational + paste context — summary table optional
- **3+ files or 2+ packages** → formal prompt with summary table (required)
- **Architecture decision** → AI Council debate first, then formal prompt

### Key rules

- Git workflow section is non-negotiable in EVERY prompt, even for non-repo changes (explain why not needed)
- "What NOT to do" section prevents Claude from over-engineering
- Include `pytest -x --tb=short && ruff check && git status` after each step, not just at the end
- Include `git status must show clean between each numbered step`
- CHANGELOG.md entry required in FINAL section if files changed
- Bypass permissions (no approval) → almost never, only for trivial read-only operations

---

## 3. Absorbing New Information

**Papers, repos, articles, tools → evaluate → extract actionable items → implement or reject.** Don't let "interesting" become "installed."

### Evaluation flow

1. **Quick triage (30 seconds):** Is this relevant to my work? Is it at my level or below?
   - Tutorial-level content (below Rob's level) → bookmark for reference only, skip
   - New tool with <100 GitHub stars and v0.1 → too early, revisit in 3 months
2. **Extract (5 minutes):** What are 2-3 actionable items from this?
3. **Decide:** Implement now, add to backlog, or reject with reason
4. **Log:** Add entry to LESSONS.md with category and action taken

### Council debate threshold

- Tactical choices (which library, which formatter) → decide yourself
- Architectural decisions (new database, new integration pattern, new package) → AI Council
- When in doubt: if reverting would take >1 hour, it's architectural

---

## 4. Extracting Lessons from Any Session

**Lessons die in chat history if not extracted.** Every session — browser chat, Claude Code terminal, Council debate, article analysis — potentially contains lessons. Without an explicit extraction step, they vanish.

### When to extract

- **End of every browser chat** that involved decisions, debugging, or new insights
- **End of every Claude Code session** (via LESSONS.md entry if applicable)
- **After every Council debate** (decisions are binding, but the reasoning often contains lessons)
- **After reading an article/repo/tool** that changed how you think about something

### How to extract (2 minutes, no more)

Ask yourself: **"What 2-3 things did I learn that I didn't know before this session?"**

For each, write one entry in LESSONS.md:
```
### YYYY-MM-DD | [source] | [one-line lesson] | [category] | [action taken]
```

Categories: `prompt-craft` / `token-optimization` / `architecture` / `tooling` / `process` / `gotcha`

### What qualifies as a lesson

- Something that surprised you (expectation ≠ reality)
- A mistake that cost >10 minutes
- A technique that saved significant time
- A decision rationale you want to remember
- A tool/article insight that changed your approach

### What does NOT qualify

- Things you already knew (no "learned that tests are important")
- Pure factual information (that goes to vault or ~/.claude/)
- Decisions without reasoning (those are ADRs, not lessons)

### When a lesson becomes a rule

If you find yourself writing a lesson that sounds like "always do X" or "never do Y" — it might be a rule, not a lesson. Write the lesson in LESSONS.md for context, then also add it to `~/.claude/` (gotchas, rules/, or learned-rules.md) with a verify: line. Cross-reference both.

---

## 5. Running an AI Council Debate

**Council debates are valuable but can become procrastination.** Hard rule: max 2 debates before implementation starts. Full format guide lives in the council project's docs/ folder.

### When to use Council vs. decide yourself

- **Council:** New package creation, database choice, integration pattern, tool adoption, major refactor, knowledge organization
- **Self:** Library version, config format, variable naming, test strategy for single feature
- **Rule of thumb:** If reverting would take >1 hour, it's architectural → Council

### Debate question format (summary)

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

```bash
# Process debates from inbox
council-cli --inbox

# Direct question
council-cli "REST vs GraphQL?" --full --rounds 2
```

> Exact CLI syntax depends on the council tool — see its CLAUDE.md for current commands.

### Post-debate protocol

1. Decision is BINDING once synthesized
2. Create ADR summary → `docs/decisions/ADR-{NN}_{topic}.md`
3. Archive transcript → `docs/decisions/transcripts/`
4. `git add + commit` both immediately
5. Never reopen a decided topic unless new evidence appears

---

## 6. Code Review with Claude Code

**Code review stays on Sonnet — security boundary, never Haiku.** This is a Council-binding decision.

### Process

1. Specify scope: which files, which changes, what to focus on
2. Ask Claude Code to read the diff first, report what it sees
3. Focus areas: security, edge cases, error handling, test coverage
4. Never auto-apply suggested changes — review each one

---

## 7. Managing a Long Claude Code Session

**Sessions longer than ~4 hours should be split.** Context degradation is not linear — it accelerates.

### Session start protocol

1. Review recent CHANGELOG.md entries
2. Read CLAUDE.md
3. Check gotchas
4. `git status` (must be clean)
5. Define 1-2 objectives for this session — everything else is backlog

### During session

- `/clear` between unrelated tasks (saves 30-40% input tokens)
- Commit after each logical change
- Test after each change (not at the end)
- If scope creeps: "Adding to OPEN_DECISIONS.md, not doing today"
- Use Plan Mode before implementation (catches bad approach at 200 tokens vs 5000)
- Use line ranges (`@file:15-80`) instead of whole files

### When context gets heavy

- `/compact` at 40% (aggressive, Council-approved)
- `/handoff` before switching to Claude.ai for architecture consulting
- If Claude says "it's done" on a complex operation — VERIFY with filesystem commands

### Session end protocol

1. Run full test suite
2. Update CHANGELOG.md if files changed
3. Update project handoff doc (if exists)
4. `git status` (must be clean — if "27 modified files", STOP and commit)
5. Write 3-line handoff note

---

## 8. Handing Off Between Sessions

**Claude Code executes. Claude.ai architects and challenges.** Three handoff scenarios exist.

### Roles

- **Claude Code (terminal):** reads files, runs commands, edits code, verifies state, runs tests. Trusts filesystem, not memory.
- **Claude.ai (browser):** architecture consulting, strategic decisions, critical thinking. **ALWAYS maintains critical thinking** — questions the approach, identifies risks, says "no" when something doesn't make sense. Never rubber-stamps.

### Handoff A: Claude Code → Browser

1. In Claude Code: `/handoff` → generates token-efficient state summary
2. Paste into Claude.ai browser chat
3. Discuss architecture, strategy, decisions
4. Decisions go back to Claude Code as prompts (Section 2 format)

### Handoff B: Browser → New Browser (Council Decision #24)

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

- Claude.ai writes prompts using Section 2 format (Model/Mode/Effort table)
- Prompts should be QUESTIONS, not COMMANDS
- Good: "What's in the docs folder? Report structure."
- Bad: "Move benchmark.md to eval/"
- Let Claude Code discover actual state, then propose actions

---

## 9. Weekly Review (Friday)

**Friday consolidation — 30 minutes max, not a project.**

1. Run `/evolve` in Claude Code — review corrections, observations, propose rule promotions/pruning
2. Review gotchas added this week — any patterns?
3. Review token usage — is Opus verbosity still the main drain?
4. Review LESSONS.md entries from this week — anything to change in PLAYBOOK?
5. Review OPEN_DECISIONS.md — anything stale? Anything urgent?
6. Quick project health check (test suite, lint, stale branches)
7. Update ENVIRONMENT.md if any config changed

---

## 10. Evaluating a New Tool/Framework/Model

**Check maturity before investing time.** Fresh repos with <100 stars and v0.1 = too early.

### Quick eval checklist

1. GitHub stars, last commit date, release cadence
2. Does it solve a problem I actually have? (not "might have someday")
3. Does it integrate with my existing stack? (Python, Click, YAML config)
4. What does adoption cost? (learning curve, migration, dependencies)
5. Is there a simpler alternative I'm already using?

### Decision framework

- **Obvious yes:** Solves real pain, mature, good docs, easy to adopt → just do it
- **Maybe:** Interesting but not urgent → bookmark, revisit in 2 weeks
- **Council debate:** Would change architecture or replace an existing tool
- **Hard no:** Pre-v1, no community, solves a problem I don't have

---

## 11. Multi-Project Rules

**Package boundaries are sacred.** Projects/packages should never import directly from each other — they communicate via CLI subprocess, shared schema packages, or well-defined interfaces.

### Principles

- Designate one package as the **source of truth** for shared data models, taxonomy, naming, and validation. Other packages depend on it — never duplicate a schema.
- Orchestrator pattern: one central project calls others via subprocess or API. Tools stay stateless; the orchestrator owns state.
- Document the architecture in the project's CLAUDE.md, not here. This playbook covers methodology, not project-specific design.

### Config hierarchy (most specific wins)

```
~/.claude/CLAUDE.md              ← Global rules (all projects)
~/.claude/skills/gotchas/        ← Global traps
Dev/CLAUDE.md                    ← Workspace rules
Dev/{project}/CLAUDE.md          ← Project rules
Dev/{project}/packages/X/CLAUDE.md  ← Package rules
```

---

## 12. Where Knowledge Lives

**Three domains, three homes, zero overlap.** Council Decision #23 (2026-03-29, unanimous 4-0).

| Domain                     | Location              | Tool                       | Purpose                                                  |
| -------------------------- | --------------------- | -------------------------- | -------------------------------------------------------- |
| Pre-sales work knowledge   | `ObsidianVault/`      | Obsidian                   | Clients, products, domains, competitive intel, demo prep |
| Dev practice methodology   | `Dev/.dev-knowledge/` | VS Code workspace          | How I build software: processes, lessons, setup state    |
| Claude Code runtime config | `~/.claude/`          | Claude Code auto-discovery | Rules, commands, hooks, agents, memory, gotchas          |

### "Where does this go?" decision rule

- Is it about a **client, product, or domain**? → Obsidian vault
- Is it about **how I work** (process, methodology, lesson learned)? → `.dev-knowledge/`
- Is it a **rule Claude Code must execute** (gotcha, verify check, command, hook)? → `~/.claude/`

### When a lesson becomes a rule

A lesson in LESSONS.md is human context (why, what happened). A rule in `~/.claude/` is machine-executable (verify: line, gotcha check). When a lesson matures into a rule:
1. Keep the lesson entry in LESSONS.md (provenance)
2. Add the rule to `~/.claude/rules/`, `gotchas.md`, or `learned-rules.md` with verify: line
3. Cross-reference both with file path

### Data sanitization

If a client engagement generates a dev lesson, strip all client names, proprietary schemas, and identifying details before writing to `.dev-knowledge/`.

### Migration triggers

- **20 files** in `.dev-knowledge/` → evaluate creating a dedicated Obsidian DevVault
- **50 entries** in LESSONS.md → split into topic files
- Rob opens Obsidian to search for dev methodology → immediate signal DevVault is needed

---

## 13. Markdown Governance

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

**"I'll organize later"** — If you create a file without knowing where it belongs, you'll never organize it. Know the category BEFORE creating.

**"Let's put it in docs/ for now"** — `docs/` is not a staging area. It has defined categories: handoff, archive, decisions. If it doesn't fit one, it doesn't belong there.

**"Let's name it descriptively"** — `ARCHITECTURE_REVIEW.md` is useless without a date. `2026-03-21_ARCHITECTURE_REVIEW.md` is findable.

**"We can consolidate these output folders later"** — Output dirs grow exponentially. Set a single canonical output path at project creation.

**"The AI will remember"** — It won't. Not after 4 hours. Not across sessions. Not after compaction. Write it down in CHANGELOG.md or CLAUDE.md.

**"We'll add tests later"** — Later never comes. Write the test stub before the implementation.

**"Let's rename/restructure everything"** — Every rename has blast radius (env vars, configs, DBs, venvs, caches). Never rename without full impact analysis FIRST, and never in the same session as feature work.

---

## The 10 Commandments

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

**When:** Feature branch touches 3+ files OR 2+ packages OR safety-critical paths (vault writes, OneDrive ops, cleanup/delete)
**Tool:** Codex CLI or Codex Desktop
**Process:** `/review` in Claude Code → copy command → run in second terminal → address flags → merge
**Skip when:** Single-file fix, test-only changes, documentation updates

Codex reviews. Claude Code builds. Never reverse the roles.

---

## 16. Code Quality Audit Process

**When:** Monthly full audit **[L only]** · On-demand before major refactors **[L+M]** · S projects skip.
**Tool:** Codex CLI or Codex Desktop (independent reviewer — no authorship bias)
**Cycle:** Read-only audit → triage by severity → fix by tier → re-audit

### Severity tiers
- **CRITICAL** — data loss, security, broken imports that fail at runtime
- **HIGH** — wrong dependency direction, missing tests on public API, type errors
- **MEDIUM** — style violations, redundant code, unclear naming
- **LOW** — suggestions, nitpicks, debatable patterns

### Process
1. Run audit (read-only): `codex "Audit this repo against AGENTS.md rules. Output findings by severity. Do not fix anything."`
2. Triage output manually — expect ~30% false positives. Demote miscalibrated patterns in AGENTS.md.
3. Fix CRITICAL and HIGH first. One commit per logical group.
4. Re-run audit. Confirm flags resolved.
5. Update ARCHITECTURE.md if module boundaries or dependency direction changed. **[L+M]**

### Rules
- Audit-first, fix-second. Never fix while auditing.
- Claude Code fixes. Codex audits. Never reverse the roles.
- Structural changes with N>5 call sites: shim first, migrate incrementally, remove shim last.
- Any session touching module boundaries must produce or update ARCHITECTURE.md. **[L+M]**

---

## Appendix A: Claude Code Shortcuts

### Permission Modes (Shift+Tab cycles)

- **Default** — asks permission for everything. For sensitive/unfamiliar work.
- **Accept Edits** (Shift+Tab x1) — auto-saves files, asks before shell. **Daily driver.**
- **Plan Mode** (Shift+Tab x2) — read-only. Use when you don't know the approach.

### Keyboard

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

| Command            | When to use                                       |
| ------------------ | ------------------------------------------------- |
| `/boot`            | Session start — load memory, verify rules         |
| `/clear`           | Between repos/tasks — #1 token saver              |
| `/compact`         | Mid-session when context heavy                    |
| `/compact [focus]` | Compress with focus ("focus on API changes")      |
| `/evolve`          | Weekly Friday — review corrections, promote rules |
| `/handoff`         | Before switching to Claude.ai browser             |
| `/stats`           | Check token usage                                 |
| `/plan [prompt]`   | One-shot plan mode without cycling Shift+Tab      |
| `/model`           | Change model mid-session                          |
| `/effort`          | Change effort level                               |
| `/context`         | See what's using context window                   |
| `/resume`          | Resume previous session                           |

### CLI Flags

```
claude --permission-mode plan      # start in plan mode
claude --permission-mode acceptEdits  # start in accept edits
claude -p "prompt"                 # headless non-interactive
claude -r "session-name"           # resume named session
```

### The ! Prefix

Type `!` before any command to run it directly in shell without Claude processing:
```
!git status          # output goes to context, zero AI tokens
!pytest -x --tb=short  # see test results without asking Claude to run them
!cat src/config.py   # show file to Claude without a read request
```
Use for quick checks where you don't need Claude to interpret — just inject output into context.

---

## Appendix B: Model Routing Table

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

| CET Time    | Activity                           | Rationale                                                         |
| ----------- | ---------------------------------- | ----------------------------------------------------------------- |
| 08:00-09:00 | Planning in Plan Mode (Opus)       | Fresh mind + off-peak ET                                          |
| 09:00-13:00 | Heavy implementation (Opus/Sonnet) | Off-peak ET (3-7AM). Golden window.                               |
| 13:00-14:00 | Break                              | Before peak begins                                                |
| 14:00-20:00 | Light work only                    | Peak ET. Code review (Sonnet), Haiku reports, manual coding, docs |
| 20:00-22:00 | Optional overflow                  | Off-peak resumes. Only if energy allows                           |

---

## Appendix C: Token Optimization Techniques

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

**After 2 failed attempts at something → `/clear` and rewrite the prompt from scratch.** A fresh context with a clear prompt almost always works better than a polluted context full of failed approaches. Don't keep hammering — reset.

### CLAUDE.md size limit

Keep CLAUDE.md under 200 lines per file. Instruction adherence drops above that. Use `.claude/rules/` for domain-specific rules and `.claude/skills/gotchas/` for institutional memory — these load separately and don't bloat the main prompt.