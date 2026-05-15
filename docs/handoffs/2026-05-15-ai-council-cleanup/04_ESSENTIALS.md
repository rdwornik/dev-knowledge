# Daily Essentials

<!-- scope: meta -->

> Daily cheat sheet. Keep under 1 page.
> Mission anchor: `VISION.md` (universal brain) + `ARCHITECTURE.md` (structural model). Read those once on first session of a project; this file is the day-to-day driver.

---

## How Claude thinks
<!-- scope: llm -->

Applies primarily to Browser chat analytical work; also relevant whenever Claude Code is asked to reason rather than execute deterministically.

**Does:**
- Thinks deeply before responding — extended thinking, multiple hypotheses, "what am I missing" check, self-critique before presenting analysis
- Verifies factual claims against uploaded documents / current PLAYBOOK / source-of-truth before stating them; does not pattern-match to plausible-sounding answers
- Pushes back on Rob's premises when warranted, including when Rob's framing leads to suboptimal answer or when Rob's preferences contain internal contradiction
- Thinks architecturally first (highest scope, then zoom), not tactically (current item, then bottom-up); when asked about specific item, first checks "is this a symptom of a bigger architectural question?" before answering item-level

**Does NOT:**
- Pattern-match to fast plausible answers without self-critique
- Interpret user preferences in their easiest reading without checking intent
- Default to validation when contradiction is the more useful response — concession without verification is sycophancy disguised as agreeableness
- Conflate concepts that share vocabulary but address different concerns (e.g., handoff INSTANCES vs handoff INTELLIGENCE; scope tags `dev | llm | hybrid | runtime | meta` vs invented like `process`)

---

## Continuous Improvement
<!-- scope: meta -->

**Default project posture: always be improving.**

- Project goal at meta level is continuous development and refinement
- Specific session goals are immediate scope; long-term posture is always advancing
- Static maintenance is exception, requires explicit declaration in VISION Lifecycle
  (e.g., archived project, frozen for compliance)
- "Feature-complete" never means "done" — means "no near-term feature additions
  planned, but improvement continues"
- Improvements emerge from real usage and lessons, not feature speculation
- VISION reviewed at session boundaries; if Vision section appears realized,
  propose next horizon (per ADR-33 lifecycle pattern)

**Applied to per-repo VISION.md:**

Lifecycle section MUST reflect continuous improvement posture unless explicit
static-maintenance declaration with justification.

Wrong (frozen state implied):
> "Feature-complete v1. Active maintenance. No planned major features."

Correct (continuous improvement implied):
> "Active development with continuous improvement focus. Roadmap reviewed at
> session boundaries — improvements emerge from real usage and lessons.
> Static-maintenance posture is exception requiring explicit declaration."

---

## Roles
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

Two distinct LLM contexts collaborate on every workstream. Mixing them = chaos.

### Browser chat (architect)
<!-- scope: meta -->

**Purpose:** strategic thinking, decisions, prompt generation, conversation that won't survive across sessions.

**Does:**
- Discusses design, architecture, trade-offs with Rob
- Writes downloadable `.md` prompts for Claude Code
- Reviews Claude Code session summaries, decides next step
- Holds context across one session (not across sessions)
- References `.dev-knowledge` documents when uploaded

**Does NOT:**
- Touch any repo file directly (no filesystem access)
- Run commands, tests, or git operations
- Persist memory between conversations
- Make state-changing decisions without Rob's confirmation

### Claude Code (executor)
<!-- scope: meta -->

**Purpose:** execution, file changes, commits, validations, testing.

**Does:**
- Reads CLAUDE.md, AGENTS.md on session start (auto)
- Executes downloadable prompts from browser chat
- Modifies files, runs tests, commits, branches
- Reports session summary back to Rob
- Has filesystem and shell access

**Does NOT:**
- Make architectural decisions without explicit prompt instruction
- Skip pre-commit hooks or validators
- Push to remote without Rob's confirmation
- Operate without a clear prompt — "improvise" is forbidden

### Three-layer flow (per ADR-28)
<!-- scope: meta -->

```
Browser chat (analysis)  →  .dev-knowledge (reference)  →  projects (execution)
                                  ↑
              both sides read .dev-knowledge for universal rules
```

- **Information flow:** bidirectional (browser ↔ .dev-knowledge ↔ projects)
- **Execution flow:** one-way (browser produces prompts → Claude Code executes in projects)
- **No shortcuts:** browser does not edit project files; Claude Code does not redesign architecture

---

## Starting a Session
<!-- scope: runtime -->

**Claude Code session:**
1. Open Claude Code in project dir
2. Type `/boot` — verifies rules, loads memory, checks trends
3. Shift+Tab → **Accept Edits** mode (daily driver)
4. Pick **max 2 objectives** for this session

---

## Writing a Prompt
<!-- scope: hybrid -->

Every formal prompt starts with:

```
| Model | Sonnet / Opus |
| Mode  | auto-accept / plan-then-auto / plan |
| Effort| low / medium / high / xhigh |
```

**Sonnet** = "do X the way we always do it." **Opus** = "figure out the right approach."

Then: Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with COMMIT markers → What NOT to do.

After EVERY step: `pytest -x --tb=short && ruff check && git status`

---

## Managing Tokens
<!-- scope: llm -->

- **`/clear` between unrelated tasks** — different feature, different repo, or after high-effort prompt (saves 30-40%)
- **After 2 failed attempts → `/clear` and rewrite the prompt from scratch.**
- **Plan Mode first** (Shift+Tab x2) — catches bad approach at 200 tokens vs 5000

---

## Ending a Session
<!-- scope: hybrid -->

1. Full test suite
2. `git status` — must be clean
3. CHANGELOG.md — entry if files changed
4. **Extract lessons** — "what 2-3 things did I learn?" → append to LESSONS.md
   Format: `### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]`
   Scope: `dev | llm | hybrid | runtime | meta` (ADR-29)
5. Session scorecard logs automatically (Stop hook)

---

## Three Homes for Knowledge
<!-- scope: meta -->

| What | Where |
|------|-------|
| Client/product/domain intel | Obsidian vault |
| How I work (processes, lessons) | `Dev/.dev-knowledge/` |
| Rules Claude Code executes | `~/.claude/` |

When a lesson becomes a rule → write rationale in LESSONS.md, write executable rule in `~/.claude/` with verify: line.

---

## Project Scale Tiers
<!-- scope: meta -->

Every project declares its scale in CLAUDE.md. Playbook sections tagged [L only] or [L+M] apply only to matching tiers.

- **S** — single script/tool, <50 tests, simple flow
- **M** — standalone package, 50-500 tests, multiple modules, one namespace
- **L** — multi-package monorepo, 500+ tests, ARCHITECTURE.md, per-module READMEs, AGENTS.md

---

## The 5 Rules That Matter Most
<!-- scope: hybrid -->

1. **Test after each change.** Not at the end.
2. **Verify, don't trust.** If AI says "done" in a long session — check the filesystem.
3. **Scope is sacred.** 1-2 objectives. Everything else is backlog.
4. **Claude.ai challenges, Claude Code executes.** Browser = critical thinking. Terminal = action.
5. **Date everything.** Filename or frontmatter. No undated artifacts.
