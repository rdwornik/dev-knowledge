# CLAUDE.md — Dev Knowledge

## What this project is
<!-- scope: meta -->

Universal LLM-driven development guide and methodology framework — the
ecosystem's knowledge guardian, methodology author, and auditor. Works
in any folder on any machine; governs all projects under `Dev/`
(corp-monorepo, ai-council, corp-ops, corp-sca-time-automation, future
repos). NOT a code project — a collection of markdown governance files
+ read-only validators. Managed via Claude Code and VS Code. Full
mission in `VISION.md`; structural model in `ARCHITECTURE.md`.

## Files and their rules
<!-- scope: meta -->

| File                          | Type        | Rule                                                                                         |
| ----------------------------- | ----------- | -------------------------------------------------------------------------------------------- |
| `VISION.md`                   | Living      | Universal-brain mission statement. Vision/Scope changes via AI Council debate; clarifications + References conversational. |
| `ARCHITECTURE.md`             | Living      | Structural model per ADR-28 + ADR-31. Update when layout, conventions, governance, or binding ADRs shift. |
| `protocols/ESSENTIALS.md`     | Living      | Daily cheat sheet. Keep under 1 page. Update when workflows change.                          |
| `protocols/SESSION_SETUP.md`  | Living      | Browser chat workflow. 5 chronological steps. Update when chat process changes.              |
| `protocols/PLAYBOOK.md`       | Living      | Full process reference. Numbered sections (1–16) + unnumbered governance sections + appendices. Update when new processes are established. |
| `protocols/HANDOFF_PROCESS.md` | Living     | Handoff trigger rules + Scale-tiered format + Roles. Authoritative protocol for handoff generation. |
| `protocols/ENVIRONMENT.md`    | Living      | Current setup state. Update when config/tools/decisions change.                              |
| `LESSONS.md`                  | Append-only | NEVER edit old entries. NEVER delete. Only append new entries at the bottom.                 |
| `logs/TOKEN-LOG.md`           | Append-only (newest-first) | Threshold-triggered (7-day) via /session-summary. Never edit previous entries.   |
| `JOURNAL.md`                  | Append-only (newest-first) | Per-session tactical log. Entry shape: `Did / Result / Changes / Abandoned / Next` (per Council Simplification 2026-05-16). Prepend at session wrap or workday close. The `Changes:` line carries what CHANGELOG.md used to record — git history is the rest. |
| `BACKLOG.md`                  | Living      | Cross-session pending items (per ADR-41). M+ tier mandate. Done items leave the file; their trace is git history. Abandoned items get a short note in `docs/decisions/`, not a tombstone here. |
| `README.md`                   | Living      | Triage rules and file index. Update when files are added/removed.                            |
| `config/requirements-dev.txt` | Living      | Python dev dependencies (pre-commit, etc).                                                   |

## What to do here
<!-- scope: meta -->

- Update files when processes, config, or decisions change
- Append lessons after sessions
- Keep files consistent — if a process is described in PLAYBOOK, ESSENTIALS should have the summary version, not a conflicting one
- Verify against VISION.md Lifecycle: BACKLOG reflects in-scope items; JOURNAL traces work to VISION goals; git history records movement toward VISION; ADRs implement VISION decisions. Drift in any direction → trigger VISION review.
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
- Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md` (deleted 2026-05-16 per Council Simplification). Git history + JOURNAL `Changes:` line replace CHANGELOG. Done items simply leave BACKLOG; trace lives in git.

## Related locations
<!-- scope: meta -->

- `~/.claude/` — Claude Code runtime config (skills, gotchas, memory, rules, commands, hooks)
- `.claude/` — project-level Claude Code config (git-discipline rule, /save command)
- `ObsidianVault/` — pre-sales work knowledge (separate, do not mix)
- `Dev/` — code projects (each has own CLAUDE.md)

## Scope tags (informal, no longer enforced)
<!-- scope: meta -->

ADR-27 defined a scope-tag vocabulary (`dev | llm | hybrid | runtime | meta`)
with pre-commit enforcement and a hybrid-ratio ceiling. Per Council
Simplification 2026-05-16 the enforcement system has been removed:
`scripts/validate_scope_tags.py` deleted, pre-commit hook removed,
hybrid-ratio governance withdrawn.

Existing `<!-- scope: X -->` HTML comments and LESSONS-entry `[scope: X]`
tags are LEFT IN PLACE as informal lightweight metadata. Authors can use
them when useful; nothing automated enforces them or audits drift. New
sections do NOT need to add scope tags.

ADR-27 is retained as historical record. See also ADR-46/47 demotion notes
for the broader simplification context.

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
- Topic 1 (ADR-31): authority model = Prescriptive with conformance audit (1B); .dev-knowledge stays Scale M with one L-tier artifact (ARCHITECTURE.md)
- Topic 2 (ADR-32): handoff format = folder-based with 9-section HANDOFF.md, point-in-time governance copies, manifest.json (HANDOFF_PROCESS.md v2.0 is the operational counterpart)
- ADR-33: VISION.md universalization — mandatory at ≥1 dependent; Standard/Lite tiers; migration cohort ai-council + corp-monorepo immediate
- ADR-34: file naming convention — per-file-type table; UPPERCASE living docs, ADR-NN_topic ADRs, YYYY-MM-DD-slug audits/handoffs
- ADR-35: lessons base activation — push retrieval via SessionStart hook, pull via `lessons query`, DEV_KNOWLEDGE_PATH cross-repo discovery
- ADR-36: audit tool architecture — .dev-knowledge as ecosystem auditor; 4-phase implementation plan
- ADR-37: session boundary protocol — two-phase handoff overlay (Current State + Future State) over ADR-32 9-section structure
- ADR-38: universal repo architecture baseline — mandatory files per tier (S/M/L); foundation for ADR-39/40/41
- ADR-39: file lifecycle governance — 6-element pattern (purpose/trigger/owner/grooming/boundaries/enforcement); registry of all files
- ADR-40: scale tier evaluation algorithm — logarithmic Maintainability Index pattern; 3 signals; transition procedures
- ADR-41: cross-session backlog architecture — BACKLOG.md mandate at M+ tier; no Scrum vocabulary; split-brain prevention
- Trigger: when navigation overhead emerges, evaluate Obsidian DevVault migration
- Trigger: when LESSONS.md becomes hard to navigate by topic, split into topic files

### Council output convention
<!-- scope: meta -->

Council CLI dual-writes its outputs:
- `ai-council/output/` — operational archive (transcript `.md` + `_metrics.json`)
- `.dev-knowledge/docs/decisions/transcripts/` — curated source of truth (transcript `.md` only, no metrics)

Naming: legacy `DECISION_NN_topic.md` (manual narrative numbering) coexists with new `YYYYMMDD_HHMMSS_topic.md` (CLI auto-generated). Consolidation pending — see `docs/decisions/transcripts/`.
