# CLAUDE.md — Dev Knowledge

## What this project is
<!-- scope: meta -->

Living knowledge base for Rob's dev practice methodology. NOT a code project — a collection of markdown files that document how Rob works with AI-assisted development. Managed via Claude Code and VS Code.

## Files and their rules
<!-- scope: meta -->

| File                          | Type        | Rule                                                                                         |
| ----------------------------- | ----------- | -------------------------------------------------------------------------------------------- |
| `protocols/ESSENTIALS.md`     | Living      | Daily cheat sheet. Keep under 1 page. Update when workflows change.                          |
| `protocols/SESSION_SETUP.md`  | Living      | Browser chat workflow. 5 chronological steps. Update when chat process changes.              |
| `protocols/PLAYBOOK.md`       | Living      | Full process reference. Numbered sections (1–16) + unnumbered governance sections + appendices. Update when new processes are established. |
| `protocols/HANDOFF_PROCESS.md` | Living     | Handoff trigger rules + Scale-tiered format + Roles. Authoritative protocol for handoff generation. |
| `protocols/ENVIRONMENT.md`    | Living      | Current setup state. Update when config/tools/decisions change.                              |
| `LESSONS.md`                  | Append-only | NEVER edit old entries. NEVER delete. Only append new entries at the bottom.                 |
| `logs/TOKEN-LOG.md`           | Append-only (newest-first) | Threshold-triggered (7-day) via /session-summary. Never edit previous entries.   |
| `CHANGELOG.md`                | Append-only | Notable changes. New entry per session that modifies files.                                  |
| `JOURNAL.md`                  | Append-only (newest-first) | Per-session tactical Did/Failed/Next log. Prepend at session wrap or workday close. Per PLAYBOOK Stream B Gap #4 spec. |
| `README.md`                   | Living      | Triage rules and file index. Update when files are added/removed.                            |
| `config/requirements-dev.txt` | Living      | Python dev dependencies (pre-commit, etc).                                                   |

## What to do here
<!-- scope: meta -->

- Update files when processes, config, or decisions change
- Append lessons after sessions
- Keep files consistent — if a process is described in PLAYBOOK, ESSENTIALS should have the summary version, not a conflicting one
- Cross-reference ~/.claude/ files (gotchas, learned-rules, core-invariants) — they are the executable counterpart to what's documented here
- This is a git repo. Commit after every change. Use /save or commit manually.
- .claude/rules/git-discipline.md enforces this automatically.

## What NOT to do
<!-- scope: meta -->

- Do not create new markdown files without checking README.md growth triggers (when navigation overhead emerges, evaluate DevVault migration)
- Do not duplicate content between files — ESSENTIALS summarizes PLAYBOOK, not copies it
- Do not put project-specific details here (those go in each project's CLAUDE.md)
- Do not put executable rules here (those go in ~/.claude/ with verify: lines)
- Do not edit LESSONS.md entries — only append
- Do not edit TOKEN-LOG.md entries — only append

## Related locations
<!-- scope: meta -->

- `~/.claude/` — Claude Code runtime config (skills, gotchas, memory, rules, commands, hooks)
- `.claude/` — project-level Claude Code config (git-discipline rule, /save command)
- `ObsidianVault/` — pre-sales work knowledge (separate, do not mix)
- `Dev/` — code projects (each has own CLAUDE.md)

## Scope tags
<!-- scope: meta -->

**Vocabulary:** `dev | llm | hybrid | runtime | meta` (per ADR-27).

Every section in living files has a scope tag as an HTML comment directly under its header:

```
## Section Title
<!-- scope: hybrid -->

Section body...
```

File-level tag (single comment under H1 title) substitutes for per-section tags when all sections share the same scope (see LESSONS.md — ADR-29).

### Tag definitions
<!-- scope: meta -->

- `dev` — dev methodology: code, git, testing, programming workflow
- `llm` — LLM work generally: prompting, model choice, tokens, chat workflow
- `hybrid` — inseparably both dev and llm; cannot be split without rewriting
- `runtime` — Claude Code runtime config: skills, shortcuts, hooks, slash commands
- `meta` — about the repo/knowledge system itself: index, triage, governance, decisions

### Consumer read sets
<!-- scope: meta -->

| Consumer type            | Tags to include                     |
| ------------------------ | ----------------------------------- |
| Functional browser chat  | `llm`, `hybrid`, `meta`             |
| Programming browser chat | `dev`, `llm`, `hybrid`, `meta`      |
| Claude Code session      | all tags                            |

### Governance
<!-- scope: meta -->

- Hybrid ≤25% ceiling (ADR-27). Delta-rule enforcement active (blocks regressions only; Stream A closed 2026-04-24).
- All new sections MUST include a scope tag — pre-commit hook enforces.
- Evidence-triggered reopening conditions are in ADR-27.

## Consistency check
<!-- scope: meta -->

When updating any file here, verify:
- Does ESSENTIALS still match PLAYBOOK where they overlap? Some ESSENTIALS sections (e.g., "How Claude thinks") are intentionally ESSENTIALS-only — see Section history in PLAYBOOK CHANGELOG entries
- Does ENVIRONMENT reflect current ~/.claude/ state?
- Are state references in README current and pointing to live sources?
- If a process changed in PLAYBOOK, did SESSION_SETUP also get updated?
- Does JOURNAL reflect last completed Claude Code session?

## Council decisions governing this project
<!-- scope: meta -->

- #23: vault = pre-sales, .dev-knowledge = dev methodology, ~/.claude/ = runtime config
- #24: browser handoff = one format, "wygeneruj handoff", <100 lines, code block
- #27: scope tag vocabulary = dev | llm | hybrid | runtime | meta; all sections tagged; hybrid ≤25% ceiling (ADR-27)
- #28: AGENTS.md = canonical cross-tool governance (Codex, Claude Code, Cursor, Aider) per Council #28 (Stream B Gap #6 foundation)
- Trigger: when navigation overhead emerges, evaluate Obsidian DevVault migration
- Trigger: when LESSONS.md becomes hard to navigate by topic, split into topic files
