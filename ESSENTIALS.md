# Daily Essentials

---

## Starting a Session

1. Open Claude Code in project dir
2. Type `/boot` — verifies rules, loads memory, checks trends
3. Shift+Tab → **Accept Edits** mode (daily driver)
4. Pick **max 2 objectives** for this session

---

## Key Shortcuts

| What | How |
|------|-----|
| Cycle modes (Default → Accept Edits → Plan) | Shift+Tab |
| Undo / rewind bad approach | Esc Esc |
| Toggle extended thinking | Alt+T |
| Switch model | Alt+P |
| Stop generation | Ctrl+C |
| Clear screen (not session) | Ctrl+L |

**Slash commands:** `/boot` (start) · `/clear` (between tasks) · `/compact` (shrink context) · `/handoff` (to browser) · `/evolve` (Friday) · `/stats` (tokens)

---

## Writing a Prompt

Every formal prompt starts with:

```
| Model | Sonnet / Opus |
| Mode  | auto-accept / plan-then-auto / plan |
| Effort| low / medium / high |
```

**Sonnet** = "do X the way we always do it." **Opus** = "figure out the right approach."

Then: Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with COMMIT markers → What NOT to do.

After EVERY step: `pytest -x --tb=short && ruff check && git status`

---

## Managing Tokens

- **`/clear` between unrelated tasks** — different feature, different repo, or after high-effort prompt (saves 30-40%)
- **After 2 failed attempts → `/clear` and rewrite the prompt from scratch.** Polluted context with wrong approaches makes things worse, not better.
- **`!` prefix** for quick commands — `!git status`, `!pytest` runs directly without Claude processing, output goes to context. Zero AI tokens for simple checks.
- **Plan Mode first** (Shift+Tab x2) — catches bad approach at 200 tokens vs 5000
- **Line ranges** `@file:15-80` not whole files
- **VS Code first** — test explorer, Error Lens, GitLens = 0 tokens
- When Claude.ai gives you multiple prompts → it tells you when to `/clear` between them

---

## Ending a Session

1. Full test suite
2. `git status` — must be clean
3. CHANGELOG.md — entry if files changed
4. **Extract lessons** — "what 2-3 things did I learn?" → append to LESSONS.md
5. Session scorecard logs automatically (Stop hook)

**Browser chat checkpoint:** at ~2 hours or when chat gets slow → `wygeneruj handoff` → Copy → Paste to new chat.

---

## Starting a New Browser Chat

Upload ESSENTIALS.md + handoff/context files. See SESSION_SETUP.md for full checklist.

---

## Feedback Loop

**Every correction you make** → logged to `corrections.jsonl` → same mistake 2x → auto-promoted to permanent rule with verify: check.

**Every Friday** → `/evolve` → review corrections, promote/prune rules, check trends.

**New tool/article/repo** → is it mature (>100 stars, >v1.0)? Does it solve a real problem? If architecture-level → Council debate. Otherwise decide in 30 seconds.

---

## Three Homes for Knowledge

| What | Where |
|------|-------|
| Client/product/domain intel | Obsidian vault |
| How I work (processes, lessons) | `Dev/.dev-knowledge/` |
| Rules Claude Code executes | `~/.claude/` |

When a lesson becomes a rule → write rationale in LESSONS.md, write executable rule in `~/.claude/` with verify: line.

---

## The 5 Rules That Matter Most

1. **Test after each change.** Not at the end.
2. **Verify, don't trust.** If AI says "done" in a long session — check the filesystem.
3. **Scope is sacred.** 1-2 objectives. Everything else is backlog.
4. **Claude.ai challenges, Claude Code executes.** Browser = critical thinking. Terminal = action.
5. **Date everything.** Filename or frontmatter. No undated artifacts.
