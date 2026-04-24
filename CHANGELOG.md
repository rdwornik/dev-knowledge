# Changelog — Dev Knowledge

Notable changes to the dev practice knowledge base.

---

## 2026-04-21
- PLAYBOOK: added "System Architecture" section documenting three-layer architecture (ADR-28)
- PLAYBOOK: added cross-ref in Section 12 to System Architecture
- Automated Codex review: `~/.claude/bin/codex-review.ps1` wraps `codex exec --output-last-message`
- `/review` slash command updated to invoke `codex-review`; PLAYBOOK S15 + ESSENTIALS step 3 updated
- Replaces manual "copy from TUI → paste to file" workflow
- Flag `-AutoCommit` for opt-in commit; file-based commit message avoids OneDrive hook

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

## 2026-04-21 (continued)
- Added ADR-27: Council #27 scope tagging architecture (Option A, binding)
- Added ADR-29: LESSONS.md grandfathering under scope tagging

## 2026-04-22
- Added CLAUDE.md Scope tags section (vocabulary, consumer read sets, governance) per ADR-27
- Added scripts/validate_scope_tags.py (stdlib-only pre-commit validator)
- Added .pre-commit-config.yaml and requirements-dev.txt (pre-commit >= 3.5.0)
- Tagged CLAUDE.md (11 sections) and README.md (5 sections) as meta

## 2026-04-24 — Research Archive Structure

Added:
- `docs/research/` folder for AI Council research mode outputs (distinct from `docs/decisions/` which is for Rob's own decisions)
- 3 research reports archived from 2026-04-23 and 2026-04-24 sessions
- Council #28 and #29 transcripts cross-archived in `corp-monorepo/docs/decisions/transcripts/`

Convention:
- Research reports in `.dev-knowledge/docs/research/YYYY-MM-DD-slug.md`
- Council debate transcripts in `corp-monorepo/docs/decisions/transcripts/DECISION_NN_slug.md`
- Research ≠ decision: research informs, decision commits

## 2026-04-24 — Council Archival Protocol

Added:
- PLAYBOOK Section 5: "Council Debate Archival Protocol" — mandatory immediate archival after every debate
- Retroactive archive of 7 debates + research reports to `docs/research/` and `docs/decisions/transcripts/`
- `docs/research/README.md` and `docs/decisions/README.md` index files

Why:
- Knowledge was being lost in `ai-council/output/`
- No systemic protocol for post-debate archival existed
- 5-debate backlog discovered during Council #28/#29 review session

Scope note:
- corp-monorepo archival deferred (separate session)
- Debates affecting corp-monorepo architecture (#25 diagrams, #26 Tach) archived in `.dev-knowledge/docs/research/` with `-corp-monorepo` suffix
- Future mirror to `corp-monorepo/docs/decisions/transcripts/` is separate work
