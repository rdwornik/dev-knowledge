# CLAUDE.md — Dev Knowledge

## What this project is

Living knowledge base for Rob's dev practice methodology. NOT a code project — a collection of markdown files that document how Rob works with AI-assisted development. Managed via Claude Code and VS Code.

## Files and their rules

| File             | Type        | Rule                                                                                         |
| ---------------- | ----------- | -------------------------------------------------------------------------------------------- |
| ESSENTIALS.md    | Living      | Daily cheat sheet. Keep under 1 page. Update when workflows change.                          |
| SESSION_SETUP.md | Living      | Browser chat workflow. 5 chronological steps. Update when chat process changes.              |
| PLAYBOOK.md      | Living      | Full process reference. 14 sections + appendices. Update when new processes are established. |
| LESSONS.md       | Append-only | NEVER edit old entries. NEVER delete. Only append new entries at the bottom.                 |
| ENVIRONMENT.md   | Living      | Current setup state. Update when config/tools/decisions change.                              |
| TOKEN-LOG.md     | Append-only | Weekly /stats snapshots. Never edit previous entries.                                        |
| CHANGELOG.md     | Append-only | Notable changes. New entry per session that modifies files.                                  |
| README.md        | Living      | Triage rules and file index. Update when files are added/removed.                            |

## What to do here

- Update files when processes, config, or decisions change
- Append lessons after sessions
- Keep files consistent — if a process is described in PLAYBOOK, ESSENTIALS should have the summary version, not a conflicting one
- Cross-reference ~/.claude/ files (gotchas, learned-rules, core-invariants) — they are the executable counterpart to what's documented here

## What NOT to do

- Do not create new markdown files without checking README.md growth triggers (20 files → evaluate DevVault migration)
- Do not duplicate content between files — ESSENTIALS summarizes PLAYBOOK, not copies it
- Do not put project-specific details here (those go in each project's CLAUDE.md)
- Do not put executable rules here (those go in ~/.claude/ with verify: lines)
- Do not edit LESSONS.md entries — only append
- Do not edit TOKEN-LOG.md entries — only append

## Related locations

- `~/.claude/` — Claude Code runtime config (skills, gotchas, memory, rules, commands, hooks)
- `ObsidianVault/` — pre-sales work knowledge (separate, do not mix)
- `Dev/` — code projects (each has own CLAUDE.md)

## Consistency check

When updating any file here, verify:
- Does ESSENTIALS still match PLAYBOOK? (ESSENTIALS is the summary)
- Does ENVIRONMENT reflect current ~/.claude/ state?
- Are lesson counts in README accurate?
- If a process changed in PLAYBOOK, did SESSION_SETUP also get updated?

## Council decisions governing this project

- #23: vault = pre-sales, .dev-knowledge = dev methodology, ~/.claude/ = runtime config
- #24: browser handoff = one format, "wygeneruj handoff", <100 lines, code block
- Trigger: 20 files here → evaluate Obsidian DevVault migration
- Trigger: 50 entries in LESSONS.md → split into topic files