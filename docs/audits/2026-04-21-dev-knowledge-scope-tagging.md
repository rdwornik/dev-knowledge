# Dev-Knowledge Scope Tagging — 2026-04-21

> Phase 2 of scope audit. Section-level dev/llm/hybrid/runtime/meta classification.
> Prepared for Council #27 — LLM Practice Ecosystem Architecture.
> No architecture recommendations — tagging and summary only.

**Tag definitions:**
- `[dev]` — dev methodology: code, git, testing, repo, programming workflow
- `[llm]` — LLM work generally: prompting, model choice, tokens, chat workflow (not programming-specific)
- `[hybrid]` — inseparably both dev and llm; cannot be split without rewriting
- `[runtime]` — Claude Code runtime config: skills, shortcuts, hooks, settings, slash commands
- `[meta]` — about the repo/knowledge system itself: index, triage, governance, decisions

---

## PLAYBOOK.md

### S0: Project Scale Tiers
Tag: `[dev]`
Rationale: defines tiers by test count (500+/50-500/<50), package structure, ARCHITECTURE.md requirement — all code-repo metrics.

### S1: Starting a New Project
Tag: `[dev]`
Rationale: bash scaffold, pyproject.toml, Python standards (ruff, pytest, Click), git init, branch/test/lint/commit dev loop.

### S2: Creating a Claude Code Prompt
Tag: `[hybrid]`
Note: Model/Mode/Effort routing is universal LLM tooling; the prompt structure embeds non-negotiable git workflow (branch per feature, pytest after each step, ruff check, git status clean) making the two inseparable as written.

### S3: Absorbing New Information
Tag: `[hybrid]`
Note: the triage/extract/log framework is universal knowledge management; Council debate thresholds (library choice, database, integration pattern, new package) are dev-domain specific. Neither part can stand alone.

### S4: Extracting Lessons from Any Session
Tag: `[llm]`
Rationale: lesson extraction applies to all session types (browser chat, Council debate, article analysis, code session). Categories (prompt-craft, token-optimization) are LLM-native. The process is not code-specific.

### S5: Running an AI Council Debate
Tag: `[llm]`
Rationale: multi-model orchestration for decisions. Format (YAML frontmatter, models list, question/options/constraints) and CLI (council-cli) apply to any domain. Post-debate protocol (ADR → docs/decisions/) is methodology-neutral.

### S6: Code Review with Claude Code
Tag: `[dev]`
Rationale: reviewing code changes. Security, edge cases, error handling, test coverage — all dev-specific.

### S7: Managing a Long Claude Code Session
Tag: `[hybrid]`
Note: session lifecycle mixes LLM runtime (/compact, /clear, context, /session-summary, Plan Mode) with dev workflow (git commit after each change, pytest after each change, CHANGELOG, git status) in a single undivided protocol. Neither survives extraction intact.

### S8: Handing Off Between Sessions
Tag: `[hybrid]`
Note: handoff B format (wygeneruj handoff) is universal LLM context transfer; handoffs A and C explicitly integrate Claude Code execution ↔ Claude.ai architecture with code repos, filesystem state, and programming prompts. The "Roles" section (Code executes / Browser architects) is dev-workflow framing applied to an LLM concept.

### S9: Weekly Review (Friday)
Tag: `[hybrid]`
Note: single routine mixes LLM hygiene (/evolve, token usage review, gotchas, LESSONS.md) with dev health (test suite run, lint check, stale branches). The steps alternate between the two domains with no dividing line.

### S10: Evaluating a New Tool/Framework/Model
Tag: `[hybrid]`
Note: evaluation framework is universal (GitHub stars, adoption cost, integration fit); stack references ("Python, Click, YAML config") and Council debate triggers pull toward dev; "model" in the title and model evaluation criteria pull toward LLM. Both domains are live simultaneously.

### S11: Multi-Project Rules
Tag: `[dev]`
Rationale: package boundaries, orchestrator pattern, subprocess communication, shared schema packages, config hierarchy across CLAUDE.md files — all code architecture concerns.

### S12: Where Knowledge Lives
Tag: `[meta]`
Rationale: three-domain taxonomy (ObsidianVault/pre-sales, .dev-knowledge/methodology, ~/.claude/runtime), "where does this go?" decision rule, and migration triggers govern the knowledge system structure, not any methodology.

### S13: Markdown Governance
Tag: `[dev]`
Rationale: file category taxonomy (project docs, decision records, handoff, snapshots, eval data), naming conventions with dates, and docs/ governance folder layout apply to code project repos specifically.

### S14: Anti-Patterns — What NOT to Do
Tag: `[hybrid]`
Note: The 10 Commandments mix dev rules (#3 Test after each change, #5 Commit after each change, #9 Output dirs are disposable) with universal LLM/process rules (#2 Date everything, #7 Scope is sacred, #8 Verify with Claude Code / plan with Claude.ai). Anti-patterns follow the same mixed pattern.

### S15: Cross-Tool Review [L+M]
Tag: `[dev]`
Rationale: feature branch review triggered by file/package count, /ultrareview and Codex as review tools, "Codex audits, Claude Code builds" role separation — all code-review process.

### S16: Code Quality Audit Process
Tag: `[dev]`
Rationale: severity tiers (CRITICAL/HIGH/MEDIUM/LOW for broken imports, dependency direction, type errors), audit-first/fix-second cycle, ARCHITECTURE.md update requirement — dev code quality process.

### Appendix A: Claude Code Shortcuts
Tag: `[runtime]`
Rationale: permission modes (Default/Accept Edits/Plan Mode), keyboard shortcuts table (Shift+Tab, Esc Esc, Alt+T), slash commands table (/boot, /clear, /compact), CLI flags — pure Claude Code runtime configuration.

### Appendix B: Model Routing Table
Tag: `[llm]`
Rationale: deterministic task → model assignment (No AI / Haiku / Sonnet / Opus / Gemini Flash) and time-shifting schedule (CET hours vs Anthropic peak) are LLM cost and capability management, not code-specific.

### Appendix C: Token Optimization Techniques
Tag: `[llm]`
Rationale: all 9 ranked techniques (/clear, front-load spec, Plan Mode, line ranges, ROUTING enforcement, /compact, batch changes, VS Code first, ! prefix) address LLM token economy. Golden rule (2 failed attempts → /clear + rewrite) is LLM context management.

---

## HANDOFF_PROCESS.md

### Który typ?
Tag: `[llm]`
Rationale: type decision (A vs B) based on whether a repo is involved. Meta-taxonomy for the handoff system, not a process step itself.

### Typ A — Programming Handoff
Tag: `[dev]`
Rationale: 3-step process requires Claude Code, git, file creation in repo (`docs/handoffs/`), and CLAUDE.md upload. Inseparable from programming workflow.

### Typ B — Conversational Handoff
Tag: `[llm]`
Rationale: browser-only, no repo, no git, no files. Pure context transfer between chat sessions for any topic type.

### Required Sections — Tabela
Tag: `[llm]`
Rationale: handoff section schema (OBJECTIVE, STATUS, COMPLETED, PENDING, REFERRED OUT, KEY DECISIONS, CONTEXT) applies to both handoff types. Universal handoff content contract.

### Canonical Example
Tag: `[meta]`
Rationale: pointer to a file. No process content.

### Dla Claude Code / modeli czytających ten plik
Tag: `[runtime]`
Rationale: behavioral instructions for Claude Code (when to cat specific files verbatim, what NOT to abbreviate). These are runtime directives, not user-facing process.

---

## ESSENTIALS.md

### Starting a Session
Tag: `[runtime]`
Rationale: /boot, Shift+Tab → Accept Edits mode, max 2 objectives — Claude Code session initialization steps.

### Key Shortcuts
Tag: `[runtime]`
Rationale: keyboard shortcuts table + slash commands list. Pure Claude Code runtime reference.

### Writing a Prompt
Tag: `[hybrid]`
Note: Model/Mode/Effort table and model selection rules are [llm]; the prompt structure prescribes git workflow, pytest after every step, ruff check, CLAUDE.md — making the dev workflow part of the LLM prompt spec inseparably.

### Managing Tokens
Tag: `[llm]`
Rationale: /clear, failed-attempts reset, ! prefix, Plan Mode, line ranges, VS Code first — all LLM token management techniques. None are dev-specific.

### Ending a Session
Tag: `[hybrid]`
Note: test suite and git status and /review (Codex) are [dev]; lessons extraction ("what 2-3 things did I learn?") and session scorecard logging are [llm] process maintenance. Combined in one section as a single end-of-session protocol.

### Starting a New Browser Chat
Tag: `[llm]`
Rationale: upload protocol for new browser chat session (ESSENTIALS.md + handoff/context files). LLM session initialization, not code work.

### Feedback Loop
Tag: `[hybrid]`
Note: corrections.jsonl + /evolve self-evolution loop is [runtime]/[llm]; monthly Codex full-repo audit is [dev]. Presented as one unified feedback cycle.

### Three Homes for Knowledge
Tag: `[meta]`
Rationale: knowledge domain taxonomy (Obsidian/dev-knowledge/.claude) and lesson-to-rule escalation. About the system, not a process.

### The 5 Rules That Matter Most
Tag: `[hybrid]`
Note: #1 (test after each change) and #2 (verify with filesystem) are [dev]; #3 (scope is sacred), #4 (Claude.ai challenges / Claude Code executes), #5 (date everything) are universal LLM/process principles. The 5 are presented as a single ranked list with no internal division.

---

## LESSONS.md

### Entries
Tag: `[hybrid]`
Note: single append-only log holds lessons across all categories: `prompt-craft` and `token-optimization` are [llm]; `gotcha` and `architecture` are [dev]; `process` and `tooling` span both. The append-only constraint means the content cannot be split by tag retroactively without violating the no-edit rule.

---

## SESSION_SETUP.md

### Step 1: Know Which Chat You're Starting
Tag: `[llm]`
Rationale: functional vs programming chat taxonomy for browser session initialization. LLM session meta-decision, not a code activity.

### Step 2: Start the Chat
Tag: `[llm]`
Rationale: what to upload for functional / programming / new-project chats. Even the programming chat variant describes what to upload to the browser chat, not what to do in code.

### Step 3: Work in the Chat
Tag: `[hybrid]`
Note: in-chat behavior is split between functional (analysis, critical thinking) and programming (write prompts for Claude Code, when to /clear, decision routing table). The routing table (1 file → conversational, 3+ files → formal prompt with table) integrates dev scale with LLM session decisions.

### Step 4: Handoff — When the Chat Gets Heavy
Tag: `[llm]`
Rationale: when/how to trigger "wygeneruj handoff," transfer process (Copy → new chat), handoff content description. Universal for both functional and programming chats as explicitly stated.

### Step 5: Extract Lessons
Tag: `[llm]`
Rationale: end-of-chat lesson extraction prompt. Applies to any chat type, links to LESSONS.md but the extraction process itself is LLM session hygiene.

---

## ENVIRONMENT.md

### Claude Code CLI
Tag: `[runtime]`
Rationale: version, plan, model routing, settings.json values (MAX_THINKING_TOKENS, CLAUDE_AUTOCOMPACT_PCT_OVERRIDE, defaultShell), ~/.claude/ directory tree.

### VS Code
Tag: `[dev]`
Rationale: extensions (Python, Pylance, Ruff, Error Lens, GitLens, Test Explorer), pytest in Test Explorer config, ruff format-on-save, workspace file settings. All dev-tooling configuration.

### Projects
Tag: `[meta]`
Rationale: one-line pointer — projects live under Dev/, each has CLAUDE.md. No content.

### Key Paths
Tag: `[meta]`
Rationale: filesystem path table. Organizational reference.

### Dev Practice Knowledge
Tag: `[meta]`
Rationale: directory listing of this repo's own files. Self-description.

### Obsidian Vault
Tag: `[meta]`
Rationale: boundary definition — vault purpose, folder structure, tag dimensions. Describes a system outside this repo.

### Hardware
Tag: `[meta]`
Rationale: infrastructure state (ThinkPad, RAM, GPU absence, Ollama planned). Not methodology.

### API Keys and Providers
Tag: `[llm]`
Rationale: provider table (Anthropic, Google Gemini, OpenAI, xAI, DeepSeek) with LLM use cases per provider. LLM ecosystem state.

### Binding Council Decisions
Tag: `[meta]`
Rationale: governance decisions for the whole ecosystem (Claude Code as sole tool, code review on Sonnet, Max plan, GLM re-evaluation). Decision log, not process.

### Version Tracking
Tag: `[meta]`
Rationale: component version table. State snapshot.

---

## CLAUDE.md

### What this project is
Tag: `[meta]`

### Files and their rules
Tag: `[meta]`

### What to do here
Tag: `[meta]`

### What NOT to do
Tag: `[meta]`

### Related locations
Tag: `[meta]`

### Consistency check
Tag: `[meta]`

### Council decisions governing this project
Tag: `[meta]`

---

## README.md

### Files
Tag: `[meta]`

### Triage Rules
Tag: `[meta]`

### When a lesson becomes a rule
Tag: `[meta]`

### Data sanitization
Tag: `[meta]`

### Growth triggers
Tag: `[meta]`

---

## Summary

| Tag | Count | % |
|-----|-------|---|
| `[dev]` | 9 | 14% |
| `[llm]` | 14 | 22% |
| `[hybrid]` | 13 | 21% |
| `[runtime]` | 5 | 8% |
| `[meta]` | 22 | 35% |
| **Total** | **63** | 100% |

**Sections per file:**

| File | Total sections | [dev] | [llm] | [hybrid] | [runtime] | [meta] |
|------|---------------|-------|-------|----------|-----------|--------|
| PLAYBOOK.md | 20 | 7 | 4 | 7 | 1 | 1 |
| HANDOFF_PROCESS.md | 6 | 1 | 3 | 0 | 1 | 1 |
| ESSENTIALS.md | 9 | 0 | 2 | 4 | 2 | 1 |
| LESSONS.md | 1 | 0 | 0 | 1 | 0 | 0 |
| SESSION_SETUP.md | 5 | 0 | 4 | 1 | 0 | 0 |
| ENVIRONMENT.md | 10 | 1 | 1 | 0 | 1 | 7 |
| CLAUDE.md | 7 | 0 | 0 | 0 | 0 | 7 |
| README.md | 5 | 0 | 0 | 0 | 0 | 5 |

---

## Candidates for extraction to new repo

Cleanly `[llm]` sections with no dev dependencies — most directly portable to a non-code LLM practice repo:

- PLAYBOOK S4: Extracting Lessons from Any Session
- PLAYBOOK S5: Running an AI Council Debate
- PLAYBOOK AppB: Model Routing Table
- PLAYBOOK AppC: Token Optimization Techniques
- HANDOFF_PROCESS: Typ B — Conversational Handoff
- HANDOFF_PROCESS: Required Sections — Tabela
- SESSION_SETUP: Step 1 — Know Which Chat You're Starting
- SESSION_SETUP: Step 2 — Start the Chat (Functional Chat sub-section only)
- SESSION_SETUP: Step 4 — Handoff
- SESSION_SETUP: Step 5 — Extract Lessons
- ESSENTIALS: Managing Tokens
- ESSENTIALS: Starting a New Browser Chat
- ENVIRONMENT: API Keys and Providers

---

## Hybrid sections — deferred decision

Sections where dev and llm content cannot be split without rewriting. Require Council #27 decision on split vs. keep-together:

- PLAYBOOK S2 (Creating a Claude Code Prompt) — Model/Mode/Effort routing is universal; git/pytest structure is dev. Splitting requires two separate prompt-writing guides.
- PLAYBOOK S3 (Absorbing New Information) — triage framework is universal; Council thresholds name dev artifacts (library, database, package).
- PLAYBOOK S7 (Managing a Long Claude Code Session) — /compact and context management is LLM; git commit and pytest after each step is dev. A single session protocol drives both.
- PLAYBOOK S8 (Handing Off Between Sessions) — Handoff B is universal LLM; Handoffs A and C require Claude Code / repo state / programming prompts.
- PLAYBOOK S9 (Weekly Review) — /evolve and token review is LLM hygiene; test suite and lint check is dev health. One Friday ritual, two domains.
- PLAYBOOK S10 (Evaluating a New Tool) — framework is universal; stack references and Council triggers are dev-biased. "Model" in title adds LLM domain.
- PLAYBOOK S14 (Anti-Patterns + 10 Commandments) — dev commandments (#3, #5, #9) interspersed with universal ones (#2, #7, #8). Single numbered list.
- ESSENTIALS: Writing a Prompt — same issue as PLAYBOOK S2, cheat-sheet version.
- ESSENTIALS: Ending a Session — test/git/review (dev) + lessons/scorecard (LLM) as one exit protocol.
- ESSENTIALS: Feedback Loop — /evolve self-evolution (LLM runtime) + Codex audit (dev) as one cycle.
- ESSENTIALS: The 5 Rules That Matter Most — 5 rules span both domains, presented as a unified priority list.
- LESSONS.md: Entries — structurally cannot split without violating append-only constraint.
- SESSION_SETUP S3 (Work in the Chat) — routing table couples dev file-count scale with LLM session decisions.

---

*End of scope tagging. No architecture recommendations — classification only.*
