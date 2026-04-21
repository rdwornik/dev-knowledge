# Changelog — Dev Knowledge

Notable changes to the dev practice knowledge base.

---

## 2026-04-21
- PLAYBOOK: added "System Architecture" section documenting three-layer architecture (ADR-28)
- PLAYBOOK: added cross-ref in Section 12 to System Architecture

---

## 2026-03-29 — Initial Release

### Added
- ESSENTIALS.md — daily cheat sheet (shortcuts, tokens, 5 rules)
- SESSION_SETUP.md — 5-step browser chat workflow (functional vs programming)
- PLAYBOOK.md — 14 sections + 3 appendices (shortcuts, routing, optimization)
- LESSONS.md — 45 entries from corp-monorepo retrospective, dev-practice sessions, Council debates
- ENVIRONMENT.md — tools, config, paths, VS Code setup, binding decisions
- TOKEN-LOG.md — baseline snapshot from 2026-03-28
- README.md — triage rules, file index, growth triggers
- CLAUDE.md — project contract for Claude Code
- JOURNAL.md — session log
- This CHANGELOG

### Removed (consolidated)
- SHORTCUTS.md → absorbed into PLAYBOOK Appendix A
- WORKFLOW.md → absorbed into PLAYBOOK + ESSENTIALS
- OPTIMIZATION.md → absorbed into PLAYBOOK Appendix C
- TOOLS.md → absorbed into ENVIRONMENT
- VSCODE_SETUP_REFERENCE.md → absorbed into ENVIRONMENT
- DECISIONS.md → absorbed into ENVIRONMENT

### Infrastructure (deployed to ~/.claude/)
- memory/ directory (README, learned-rules, evolution-log)
- rules/core-invariants.md (5 compression-proof rules)
- commands/boot.md and evolve.md
- SessionStart + Stop hooks in settings.json
- 41 gotchas upgraded with verify: lines

### Council Decisions
- #23: vault = pre-sales, .dev-knowledge = dev methodology, ~/.claude/ = runtime config
- #24: browser handoff = one format, "wygeneruj handoff", <100 lines, checkpoint at ~2h
