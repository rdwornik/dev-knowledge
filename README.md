# Dev Knowledge

Dev practice methodology — how Rob builds software with AI.
Separate from pre-sales work knowledge (ObsidianVault/) and Claude Code runtime config (~/.claude/).

## Files

| File | When to open | What it is |
|------|-------------|------------|
| **ESSENTIALS.md** | Every morning | 1-page cheat sheet: shortcuts, tokens, rules |
| **SESSION_SETUP.md** | Click "New chat" in browser | What to upload, how to communicate, handoff process |
| **PLAYBOOK.md** | Need full process detail | 14 sections + appendices (shortcuts, routing, optimization) |
| **LESSONS.md** | End of session (append) + Friday (review) | Append-only log, never edit old entries |
| **ENVIRONMENT.md** | Config changed | Tools, paths, VS Code, decisions, versions |
| **TOKEN-LOG.md** | Weekly /stats snapshot | Append-only token usage data |
| **CHANGELOG.md** | After notable changes | Version history of this knowledge base |
| **CLAUDE.md** | Claude Code reads automatically | Project contract — what to do, what not to do |

## Triage Rules

| Content type | Where it goes |
|---|---|
| Client intel, product knowledge, competitive analysis, demo prep | Obsidian vault (`ObsidianVault/`) |
| How I build software: methodology, lessons, decisions, retros | Here (`Dev/.dev-knowledge/`) |
| Rules Claude Code must follow, commands, hooks, agent config | `~/.claude/` |

## When a lesson becomes a rule

1. Write the rationale in LESSONS.md (why, what happened, context)
2. Write the executable rule in `~/.claude/` (gotchas, rules/, or learned-rules.md with verify: line)
3. Cross-reference both with file path

## Data sanitization

If a client engagement generates a dev lesson, remove all client names,
proprietary schemas, and identifying details before writing here.

## Growth triggers

- **20 files** here → evaluate migrating to a dedicated Obsidian DevVault
- **50 entries** in LESSONS.md → split into topic files
- Rob opens Obsidian to look for dev methodology → immediate signal DevVault is needed
