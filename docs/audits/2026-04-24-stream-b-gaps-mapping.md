# Stream B Gaps — Placement Mapping (2026-04-24)

19 gaps identified during Stream A closure sessions, with target file placement, scope, read trigger, and dependencies. **This is implementation specification, not action plan.** Stream B work will execute these mappings in priority order (separate triage session).

## Architectural foundation

- **`.dev-knowledge/` = universal Rob's working system.** Single source of truth for "how Rob works with LLM-augmented dev". Uploaded first to every browser chat; auto-read by Claude Code via repo CLAUDE.md pointer.
- **`{repo}/CLAUDE.md` = thin pointer (≤200 lines).** Says: "Read .dev-knowledge files first. Then read AGENTS.md. Then continue with repo-specific quirks."
- **`{repo}/AGENTS.md` = canonical per-repo governance.** Architecture, conventions, hooks, tests. LLMs advise; hooks/tests enforce. Cross-tool standard (works for Codex, Claude Code, Cursor, Aider, etc.).
- **Skills, slash commands, hooks** = `.claude/` folders (user-level `~/.claude/` or repo-level `{repo}/.claude/`).
- **PLAYBOOK structural decision (Opcja Y):** PLAYBOOK.md grows to ~30 sections in single file. TOC at top. Numbered sections (5.N pattern). Browser workflow prefers single large upload over multi-file.

## Governance layer (session startup)

### Gap #1 — Role definitions (browser vs Claude Code)
- **Target file:** `.dev-knowledge/ESSENTIALS.md` (new section "Roles")
- **Scope:** universal
- **Read trigger:** browser session start (uploaded), Claude Code via repo CLAUDE.md pointer
- **Dependency:** none
- **Why ESSENTIALS:** daily cheat sheet, pierwsza rzecz uploadowana

### Gap #2 — Prompt format + template
- **Target files:**
  - `.dev-knowledge/PLAYBOOK.md` (new section "Writing prompts for Claude Code")
  - `.dev-knowledge/templates/prompt-template.md` (NEW — skeleton with placeholders)
- **Scope:** universal
- **Read trigger:** PLAYBOOK uploaded to browser session start, template referenced when writing prompt
- **Dependency:** Gap #1 (role definition determines who writes prompts)

### Gap #3 — Prompt quality checklist
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (subsection "Pre-send checklist" under Gap #2's section)
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** Gap #2

## Documentation architecture

### Gap #4 — JOURNAL/CHANGELOG/LESSONS/ADR/transcripts boundaries
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (new section "Documentation file types — what goes where")
- **Scope:** universal rules
- **Read trigger:** browser session start
- **Dependency:** Gap #18 (session continuity per Scale)

### Gap #5 — CLAUDE.md purpose (≤200 lines, thin pointer)
- **Target files:**
  - `.dev-knowledge/PLAYBOOK.md` (section "CLAUDE.md as session contract — rules")
  - `.dev-knowledge/templates/CLAUDE-md-template.md` (NEW — skeleton)
  - **Action items per repo:** corp-monorepo CLAUDE.md trim, ai-council CLAUDE.md verify, .dev-knowledge CLAUDE.md verify
- **Scope:** universal rules + per-repo implementation
- **Read trigger:** template referenced when bootstrapping or trimming
- **Dependency:** Gap #6 (AGENTS.md exists first, CLAUDE.md points to it)

### Gap #6 — AGENTS.md purpose (canonical governance)
- **Target files:**
  - `.dev-knowledge/PLAYBOOK.md` (section "AGENTS.md — canonical governance contract")
  - `.dev-knowledge/templates/AGENTS-md-template.md` (NEW — skeleton)
  - **Action items per repo:** .dev-knowledge create, corp-monorepo expand (Codex-only currently), ai-council create
- **Scope:** universal rules + per-repo implementation
- **Read trigger:** Claude Code auto-reads AGENTS.md on session start
- **Dependency:** none (foundational)
- **Note:** Highest priority per Council #28

## Tooling & environment (Claude Code internals)

### Gap #7a — Skills architecture
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (section "Claude Code internals — Skills (progressive-disclosure knowledge)")
- **Scope:** universal rules; live in `~/.claude/skills/` or `{repo}/.claude/skills/`
- **Read trigger:** browser session start
- **Dependency:** none

### Gap #7b — Slash commands architecture
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (section "Claude Code internals — Slash commands")
- **Scope:** universal rules; live in `~/.claude/commands/` or `{repo}/.claude/commands/`
- **Read trigger:** browser session start
- **Dependency:** Gap #7a (related concept, naming collision risks)

### Gap #7c — Hooks architecture
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (section "Claude Code internals — Hooks (lifecycle automation)")
- **Scope:** universal rules; per-repo implementation in `.claude/settings.json` or `.pre-commit-config.yaml`
- **Read trigger:** browser session start
- **Dependency:** none

### Gap #7d — Subagents architecture (future, not yet adopted)
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (section "Claude Code internals — Subagents (future, deferred)")
- **Scope:** universal documentation of "we know about it, decided not to adopt yet"
- **Read trigger:** browser session start
- **Dependency:** none

### Gap #8 — VS Code workspace management + templates
- **Target files:**
  - `.dev-knowledge/PLAYBOOK.md` (section "VS Code workspace per Scale tier")
  - `.dev-knowledge/templates/workspace-S.code-workspace` (NEW)
  - `.dev-knowledge/templates/workspace-M.code-workspace` (NEW)
  - `.dev-knowledge/templates/workspace-L.code-workspace` (NEW)
- **Scope:** universal templates per Scale
- **Read trigger:** template referenced when bootstrapping new repo
- **Dependency:** Gap #15 (Scale tiers definitions inform workspace differences)

### Gap #9 — Claude Code potential maximization audit
- **Target file:** `.dev-knowledge/docs/audits/2026-XX-claude-code-features-inventory.md` (NEW one-time audit)
- **Scope:** universal knowledge; findings flow into PLAYBOOK Gap #7a-d sections
- **Read trigger:** referenced when adopting new feature
- **Dependency:** Gap #17 (continuous improvement triggers this)

### Gap #10 — Skills/commands/hooks-by-Claude protocol
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (section "Adopting new skills/commands/hooks proposed by Claude")
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** Gap #7a-d

## Process & rhythm

### Gap #11 — Handoff process
- **Target files:**
  - `.dev-knowledge/HANDOFF_PROCESS.md` (UPDATE — exists, needs Vibe Code 4 protocol additions)
  - `.dev-knowledge/handoff-prompts/` (UPDATE existing — verify templates current)
- **Scope:** universal
- **Read trigger:** browser session start, /session-summary command triggers
- **Dependency:** Gap #2 (prompt format), Gap #18 (session continuity per Scale)

### Gap #12 — Council debate lifecycle
- **Target file:** `.dev-knowledge/PLAYBOOK.md` Section 5 (already has 5.N archival; ADD subsection "When to run Council vs single-model + critic")
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** none
- **Status:** 80% done (5.N exists from 2026-04-24)

### Gap #13 — Session boundaries
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (new section "Session boundaries — scope, stop-signs, decision fatigue")
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** none

## Observability

### Gap #14 — Token management + TOKEN-LOG cadence — DONE 2026-04-24
- **Target files (already done):** PLAYBOOK Section "Token log cadence", ENVIRONMENT.md ccusage section, TOKEN-LOG.md (newest-first)
- **Status:** ✅ CLOSED
- **Reference:** model for completion of Gap #16 (Codex archival)

### Gap #15 — Pytest per Scale tier
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (extend existing "Project Scale Tiers" section with testing rules per tier)
- **Scope:** universal rules
- **Read trigger:** browser session start
- **Dependency:** existing Scale Tiers section

### Gap #16 — Codex review archival protocol
- **Target file:** `.dev-knowledge/PLAYBOOK.md` Section 5 (extend with "Codex review archival" — analogous to Council 5.N)
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** Gap #12 (Council archival as template pattern)

## Meta

### Gap #17 — Continuous Improvement Process
- **Target files:**
  - `.dev-knowledge/PLAYBOOK.md` (new section "Continuous Improvement — adopting new tools/models/agents")
  - `.dev-knowledge/docs/tech-radar/` (NEW folder for periodic tech radar updates)
- **Scope:** universal
- **Read trigger:** browser session start (PLAYBOOK), tech-radar referenced quarterly
- **Dependency:** Gap #9 (Claude Code audit pattern), Gap #10 (adoption protocol)

### Gap #18 — Session continuity per Scale tier
- **Target file:** `.dev-knowledge/PLAYBOOK.md` (extend existing "Project Scale Tiers" section with session continuity rules per tier)
- **Scope:** universal rules
- **Read trigger:** browser session start
- **Dependency:** Gap #4 (file types boundaries)

### Gap #19 — Amendment vs reopen protocol
- **Target file:** `.dev-knowledge/PLAYBOOK.md` Section 5 (subsection "Amending ADRs vs reopening decisions")
- **Scope:** universal
- **Read trigger:** browser session start
- **Dependency:** Gap #12 (Council lifecycle context)

## Pattern observed

**15 of 19 gaps target `.dev-knowledge/PLAYBOOK.md`.** Decision (Opcja Y, 2026-04-24): PLAYBOOK grows to ~30 sections in single file. Browser workflow prefers single large upload over multi-file. Discipline:
- TOC at top of PLAYBOOK
- Numbered sections (5, 5.N, 6 pattern continues)
- Per-section scope tags (already enforced)
- Future enhancement: `/playbook` slash command for section navigation (Stream B item, not now)

**4 gaps need NEW templates files:**
- `templates/prompt-template.md` (Gap #2)
- `templates/CLAUDE-md-template.md` (Gap #5)
- `templates/AGENTS-md-template.md` (Gap #6)
- `templates/workspace-S/M/L.code-workspace` (Gap #8 — 3 files)

**3 gaps need per-repo action** (not just `.dev-knowledge` work):
- Gap #5 (CLAUDE.md trim per repo)
- Gap #6 (AGENTS.md create/expand per repo)
- Gap #8 (workspace files per repo)

**1 gap is one-time audit:**
- Gap #9 (Claude Code features inventory)

**1 gap already done:**
- Gap #14 (Token management — closed 2026-04-24)

## Next session entry point

When opening Stream B implementation chat, upload:
- `ESSENTIALS.md`
- This mapping file
- `PLAYBOOK.md` (current state — implementation will extend it)
- One specific gap per session (focus discipline)

Stream B implementation order (suggested by dependency graph):
1. Gap #6 (AGENTS.md template) — foundational, no dependencies
2. Gap #1 (Role definitions) — quick, into ESSENTIALS
3. Gap #5 (CLAUDE.md template) — depends on #6
4. Gap #2, #3 (Prompt format + checklist) — quick, related
5. Gap #4, #18 (file types + session continuity) — related, in PLAYBOOK
6. Gap #7a-d (Claude Code internals) — single PLAYBOOK section, batch
7. Gap #11 (Handoff process update) — depends on #2, #18
8. Gap #12, #19 (Council lifecycle + amendment protocol) — extend Section 5
9. Gap #13 (Session boundaries) — standalone
10. Gap #15 (Pytest per Scale) — extend existing section
11. Gap #16 (Codex archival) — extend Section 5
12. Gap #17 (Continuous Improvement) — new section + tech-radar folder
13. Gap #8 (Workspace templates) — separate, depends on #15
14. Gap #10 (Adoption protocol) — depends on #7a-d
15. Gap #9 (Claude Code audit) — separate one-time work

**Estimated total Stream B work:** 15-25 hours, 8-12 sessions, 1-3 weeks.
