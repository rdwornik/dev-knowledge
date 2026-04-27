# CLAUDE.md
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Thin pointer (≤200 lines) — not a comprehensive spec.
>
> **For full governance:** read `AGENTS.md` (cross-tool canonical).
> **For universal rules:** read `<absolute path>/.dev-knowledge/protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md`.

## 1. First read (session start)
<!-- scope: meta -->

In order, read:
1. This file (you're here)
2. `./AGENTS.md` — repo governance (architecture, conventions, tools, ADRs)
3. `<path>/.dev-knowledge/protocols/ESSENTIALS.md` — Rob's universal working style
4. `<path>/.dev-knowledge/protocols/PLAYBOOK.md` — universal protocols (only sections relevant to current task)
5. Most recent `docs/handoffs/*.md` if continuing prior session
6. Last 5 entries of `JOURNAL.md` (if exists per Scale tier)

**Skip if not applicable** — but always read 1-3.

## 2. Repo identity
<!-- scope: meta -->

- **Name:** `<repo-name>`
- **Scale:** `<S | M | L>` (per `.dev-knowledge/protocols/PLAYBOOK.md` Project Scale Tiers)
- **Status:** `<active | maintenance | archived>`

## 3. Critical rules (non-negotiable for Claude Code)
<!-- scope: meta -->

These rules apply to THIS tool (Claude Code) operating in THIS repo. Universal rules in PLAYBOOK; cross-tool rules in AGENTS.md.

1. `<rule, e.g. "Run pytest -x --tb=short and ruff check src/ tests/ --fix after every numbered step in any prompt">`
2. `<rule, e.g. "Never push to remote without Rob's explicit confirmation">`
3. `<rule, e.g. "If pre-commit hook fails, stop and ask Rob — never bypass with --no-verify">`
4. `<add 5-7 more, repo-specific>`

Total ≤10 bullets. If you have more, they belong in AGENTS.md or PLAYBOOK.

## 4. Session start protocol
<!-- scope: runtime -->

1. `/boot` (if available — loads skills, memory, recent commits)
2. `git status` — clean working tree?
3. `git log --oneline -5` — recent context
4. Read most recent handoff if continuing
5. Wait for Rob's prompt — never improvise

## 5. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`):
- `/session-summary` — generate handoff at session end
- `/boot` — load context
- `<add as discovered>`

Repo-level (`./.claude/commands/`):
- `<command + one-line purpose>`
- `<add as created>`

## 6. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `<skill name + path + trigger>`

Repo-level (`./.claude/skills/`):
- `gotchas` (if exists) — empirical patterns this repo has stumbled on. Read before changes.
- `<add as created>`

## 7. Hooks active
<!-- scope: runtime -->

Pre-commit (from `.pre-commit-config.yaml`):
- `<hook + purpose>`
- `<add as configured>`

Other (`.claude/settings.json`):
- `<hook + purpose>`

## 8. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->

Things this tool has gotten wrong here:
- `<pattern, e.g. "Don't run validators with no args — vacuous pass; always pass --all or specific paths">`
- `<add as discovered, link to LESSONS.md entry if applicable>`

## 9. Recent ADRs binding here (last 5-10)
<!-- scope: meta -->

Brief one-liners. Full list in `docs/decisions/README.md`.

- ADR-NN: `<topic — one sentence>`
- ADR-NN: `<topic — one sentence>`
- `<auto-rotate as new ADRs land>`

## 10. Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial template per Gap #5. Hybrid pattern, thin pointer, ≤200 lines target.

---

**Last updated:** `<YYYY-MM-DD>`
**Maintained by:** `<Rob | other>`
