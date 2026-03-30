# Dev Environment — Current State

> **Living document.** Update when any config changes.
> Last updated: 2026-03-29

---

## Claude Code CLI

- **Version:** 2.1.87 (native installer, auto-updates)
- **Plan:** Claude Max $100/month
- **Model routing:** opusplan (Opus plans, Sonnet executes)

### settings.json (key values)

- MAX_THINKING_TOKENS: 10000
- CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: 40
- CLAUDE_CODE_SUBAGENT_MODEL: haiku
- CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: 1
- CLAUDE_CODE_USE_POWERSHELL_TOOL: 1
- defaultShell: powershell

### ~/.claude/ directory

```
~/.claude/
  CLAUDE.md                  ← Global P0/P1/P2 rules + Self-Evolution Protocol
  ROUTING.md                 ← Deterministic task routing table
  settings.json              ← Permissions, hooks, safety
  agents/
    report-generator.md       ← Haiku subagent
    ecosystem-snapshot.md     ← Haiku subagent
  skills/
    gotchas/gotchas.md       ← 3 universal entries (cp1252, az shell, pytest-asyncio)
  commands/
    handoff.md               ← Token-efficient output for browser chat
    boot.md                  ← Session start: load memory, verify rules, check trends
    evolve.md                ← Weekly evolution audit: promote/prune/graduate rules
  hooks/
    PreToolUse:Bash → block-onedrive.ps1   ← CRITICAL: blocks OneDrive paths
    Stop → claude-notify.ps1               ← Session end notification
    SessionStart                           ← Evolution boot reminder
    Stop                                   ← Evolution scorecard reminder
  rules/
    core-invariants.md       ← 4 compression-proof rules (paths: **/* = every file touch)
  memory/
    README.md                ← Protocol doc (formats, promotion ladder)
    learned-rules.md         ← Empty body, header only (graduated rules moved to project scope)
    evolution-log.md         ← Audit trail of /evolve decisions
    corrections.jsonl        ← Auto-created on first correction
    observations.jsonl       ← Auto-created on first observation
    sessions.jsonl           ← Auto-created on first session scorecard
    violations.jsonl         ← Auto-created on first verification failure
```

Project-specific skills, gotchas, and rules live in each repo's `.claude/` directory. See corp-monorepo/.claude/ for example.

---

## VS Code

### Workspaces

Two VS Code workspaces:
- **Coding:** project-level `.code-workspace` file in the main project repo — all code projects + packages
- **Knowledge:** `Dev/.dev-knowledge/dev-knowledge.code-workspace` — dev practice files only

Project-specific workspace details (folder count, roots) live in each workspace file.

### Extensions (10 installed)

| Extension                | Replaces in Claude Code (0 tokens)                          |
| ------------------------ | ----------------------------------------------------------- |
| Python + Pylance         | "Why does this import fail?" → red squiggles + hover        |
| Ruff                     | `ruff check` in terminal → inline errors + auto-fix on save |
| Error Lens               | Problems panel → errors NEXT TO the line (ADHD-friendly)    |
| GitLens                  | "When was this changed?" → hover any line for blame         |
| Todo Tree                | `grep -r TODO` → sidebar panel across all repos             |
| Test Explorer (built-in) | `pytest` in terminal → click ▶, green/red dots              |
| Rainbow CSV              | "What's in column 4?" → colored columns                     |
| YAML (Red Hat)           | "Is my YAML valid?" → schema validation                     |
| Even Better TOML         | pyproject.toml validation + autocomplete                    |
| Markdown All in One      | Preview, TOC, shortcuts                                     |

### Key settings (in workspace file)

**Testing (pytest in Test Explorer):**
- pytest enabled, unittest disabled
- Args: `--tb=short -q` (short traceback, quiet)
- Auto-discover on save: ON — save a test file → test explorer updates
- How to use: click flask icon in sidebar → tree of all tests across all workspace roots → click ▶ to run → green/red dots. Click failed test → jumps to exact line.

**Ruff (format + lint):**
- formatOnSave: ON, default formatter: Ruff
- fixAll + organizeImports on save (explicit)
- lint.run: onSave — errors appear inline as you type

**Todo Tree:**
- Scans all workspace roots for TODO/FIXME/HACK
- Sidebar panel (tree icon) → grouped by repo → click to jump
- Use for tracking technical debt across entire ecosystem

**File visibility:**
- files.exclude: __pycache__, .pytest_cache, _outputs, .sandbox, .venv, egg-info (hidden)
- search.exclude: _outputs, output, .sandbox, rebuild_staging (skipped in Ctrl+Shift+F)
- stickyScroll, rulers at 120, highlightModifiedTabs

---

## Projects

All projects live under `Dev/`. Each project has its own CLAUDE.md with architecture, test counts, dependency graphs, and safety rules. This file does not track project-specific details — only the development environment itself.

---

## Key Paths

| What                 | Path                                       |
| -------------------- | ------------------------------------------ |
| Dev root             | `C:\Users\1028120\Documents\Dev\`          |
| Obsidian Vault       | `C:\Users\1028120\Documents\ObsidianVault` |
| MyWork               | `C:\Users\1028120\Documents\MyWork`        |
| API keys             | `C:\Users\1028120\Documents\.secrets\.env` |
| SCRIPTS_ROOT env var | → Dev\                                     |

Project-specific paths (database locations, output dirs, exclusion zones) live in each project's CLAUDE.md.

---

## Dev Practice Knowledge

Location: `Dev/.dev-knowledge/` — visible in VS Code workspace as `📓 .dev-knowledge`

```
CLAUDE.md           ← Project contract for Claude Code
README.md           ← Triage rules ("co gdzie idzie")
ESSENTIALS.md       ← Daily cheat sheet (1 page)
SESSION_SETUP.md    ← How to start new browser chat / project
PLAYBOOK.md         ← Full process reference (14 sections + appendices)
LESSONS.md          ← Append-only lessons log
ENVIRONMENT.md      ← This file
TOKEN-LOG.md        ← Append-only token usage snapshots
CHANGELOG.md        ← Notable changes history
```

Separation rationale (Council Decision #23): vault = pre-sales work knowledge, .dev-knowledge = dev methodology, ~/.claude/ = runtime config. Trigger: 20 files → evaluate DevVault migration.

---

## Obsidian Vault

Purpose: Pre-sales work knowledge ONLY. No dev practice, no Claude Code config.

```
00_Home/          ← Dataview dashboard
01_Knowledge/     ← Flat (488+ notes)
02_Navigate/      ← 9 MOC folders (auto-generated)
99_System/        ← taxonomy.yaml, 11 tag dimensions
```

Tags: product/, client/, domain/, topic/, type/, source/, comp/, compliance/, training/, function/, audience/

---

## Hardware

- ThinkPad, AMD Ryzen Pro CPU, 32GB RAM, no NVIDIA GPU
- Not suitable for local LLM inference (rejected by Council)
- Local LLM via Ollama: planned, not deployed

---

## API Keys and Providers

Location: `C:\Users\1028120\Documents\.secrets\.env` — standard key: `GEMINI_API_KEY`

| Provider               | Used for                                                |
| ---------------------- | ------------------------------------------------------- |
| Anthropic (Claude Max) | Claude Code — primary dev tool                          |
| Google (Gemini)        | Extraction pipelines + Council synthesis ($0.04/debate) |
| OpenAI (GPT-5.4)       | Council panel member                                    |
| xAI (Grok 4.20-beta)   | Council panel member                                    |
| DeepSeek (R1)          | Council panel member                                    |

CRITICAL: Audit Gemini API tier (AI Studio vs Vertex) before batch extraction on corporate documents.

---

## Binding Council Decisions

### Active

- Stay on Claude Code as sole interactive tool
- Code review stays on Sonnet (never Haiku — security boundary)
- Haiku only for reports/snapshots
- Stay on Max $100 (no downgrade to Pro + GLM)
- Default council synthesizer: Gemini
- Time-shift heavy work to 08:00-14:00 CET
- Zero Obsidian plugins
- Vault = pre-sales only, .dev-knowledge = dev methodology (#23)
- No GMKtec local inference
- No Codex CLI, no Gemini CLI

### Pending

- Council mode system (brainstorm/evaluate/strategy) — prompt ready in inbox
- GLM-5.1 re-evaluate April 12 only if rate limits >2x/week

### Rejected (do NOT revisit before Q3)

- GMKtec local inference ($2,500 ADHD trap, 38-month ROI)
- Codex CLI (no advantage over Haiku subagents)
- Mandatory TDD (council rejected)
- Git worktrees for daily work (council rejected)
- Confidence scoring in council debates (LLMs poorly self-calibrate)

---

## Version Tracking

| Component   | Version                       | Last checked |
| ----------- | ----------------------------- | ------------ |
| Claude Code | 2.1.87 (native, auto-updates) | 2026-03-29   |
| Python      | 3.11+                         | 2026-03-28   |
| VS Code     | Current + 10 extensions       | 2026-03-29   |

Project versions tracked in each project's CLAUDE.md / CHANGELOG.md.