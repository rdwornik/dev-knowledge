# Claude Code Features Inventory — 2026-04-25

**Snapshot date:** 2026-04-25
**Claude Code version observed:** 2.1.119 (from `claude --version`)
**Status:** point-in-time audit; superseded by next dated audit

## Purpose

One-time inventory of Claude Code features with Rob's adoption status. Grounds Continuous Improvement (PLAYBOOK Section 6) triage by surfacing "available but not adopted" features. NOT a living doc — represents 2026-04-25 state only.

## Adoption status legend

- **Adopted** — actively used in Rob's workflow, confirmed by filesystem or settings
- **Available, deferred** — known feature, not adopted, explicit decision exists
- **Available, not evaluated** — known but never seriously considered; needs triage
- **Unknown / requires investigation** — flagged for follow-up
- **N/A** — feature exists but doesn't apply to Rob's solo dev use case

## Inventory

### Core mechanisms

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| Skills — user-level (`~/.claude/skills/`) | Adopted | Knowledge modules loaded on-demand | 2 active: `gotchas`, `verify` | PLAYBOOK 7a |
| Skills — project-level (`<repo>/.claude/skills/`) | Adopted | Project-specific knowledge | corp-monorepo: `gotchas` skill active | PLAYBOOK 7a |
| Skills — marketplace plugins | Adopted (passive) | Extended capabilities via official marketplace | Official marketplace cached at `~/.claude/plugins/`; provides system skills (update-config, simplify, etc.) | — |
| Slash commands — user-level (`~/.claude/commands/`) | Adopted | Invokable actions | 4 active: `/boot`, `/evolve`, `/review`, `/session-summary` | PLAYBOOK 7b |
| Slash commands — project-level (`.dev-knowledge/.claude/commands/`) | Adopted | Repo-specific actions | 1 active: `/save` in .dev-knowledge | PLAYBOOK 7b |
| Slash commands — project-level (corp-monorepo) | Not configured | Repo-specific commands | No `.claude/commands/` in corp-monorepo | — |
| Hooks — Claude Code lifecycle (`~/.claude/settings.json`) | Adopted | Lifecycle automation | 3 hooks: PreToolUse (OneDrive block), SessionStart (evolution banner), Stop (notify + scorecard reminder) | PLAYBOOK 7c |
| Hooks — project-level Claude Code (`.claude/settings.json`) | Partial | Repo-specific lifecycle | corp-monorepo has `settings.local.json`; content not audited. .dev-knowledge has none | — |
| Hooks — pre-commit (`.pre-commit-config.yaml`) | Adopted | Git lifecycle enforcement | scope-tag-validator active in .dev-knowledge | PLAYBOOK 7c |
| Subagents (`~/.claude/agents/`) | Adopted | Read-heavy delegation | 2 active: `ecosystem-snapshot`, `report-generator` (both Haiku-based) | PLAYBOOK 7d |
| Rules (`~/.claude/rules/`, `.claude/rules/`) | Adopted | Persistent constraints loaded each session | User-level: `core-invariants.md`. Project-level: `git-discipline.md` in .dev-knowledge | CLAUDE.md global |

### Model selection

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| Default model (Sonnet 4.6 1M context) | Adopted | Default workhorse | `model=sonnet[1m]` in `settings.json` | settings.json |
| Haiku for subagents | Adopted | Fast/cheap delegation | `CLAUDE_CODE_SUBAGENT_MODEL=haiku` in `settings.json` | settings.json |
| Claude Opus 4.7 | Adopted | High-effort prompts | 18.3% cost share in 8 days post-adoption; invoked via `opusplan` alias | tech-radar 2026-Q2 |
| Effort level — medium (default) | Adopted | Balanced cost/quality | `effortLevel=medium` in settings | settings.json |
| Effort level — xhigh (Opus 4.7) | Available, not evaluated | Deeper reasoning for hardest prompts | Not configured; high and medium cover current workload | — |
| Extended thinking (Opus 4.7) | Partial | Visible reasoning | `MAX_THINKING_TOKENS=10000`, `showThinkingSummaries=true`; thinking cap set but xhigh/extended mode not invoked explicitly | settings.json |
| Third-party LLM providers (Bedrock, Vertex, Foundry) | N/A | Enterprise routing | Solo dev on Anthropic direct; no routing need | — |

### Context & memory

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| `/clear` context reset | Adopted | Between unrelated workstreams | Per ESSENTIALS guidance | ESSENTIALS |
| Plan mode (`plan-then-auto`) | Adopted | Architectural prompts; review before execute | Standard for Scale L prompts | PLAYBOOK prompt template |
| Autocompact | Adopted | Automatic context compression | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40` (triggers at 40% remaining) | settings.json |
| `/compact` command (manual) | Available, not evaluated | Manual context compression at choice points | Autocompact covers automatic case; manual trigger rarely needed | — |
| Auto mode — smart permission classifier (Mar 2026) | Available, deferred | Automatic safe/risky action classification | Deferred — `skipDangerousModePermissionPrompt=true` covers primary friction point; Auto mode is more granular but adds complexity | — |
| Session recap (idle 75+ min return) | Available, not evaluated | Context restore after long idle | Not intentionally triggered; behavior when idle not observed | — |
| Memory — file-based (`~/.claude/memory/`) | Adopted | Cross-session continuity | Active: `MEMORY.md` index, `learned-rules.md`, `corrections.jsonl`, `sessions.jsonl` | CLAUDE.md global |
| MCP memory servers | Available, deferred | Enhanced external memory | Deferred — file-based handoffs sufficient | tech-radar 2026-Q2 |

### External integrations

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| MCP servers | Available, deferred | Tool/API integrations (GitHub, DBs, etc.) | No servers configured in `settings.json` or `claude_desktop_config.json`; file-based workflow sufficient | tech-radar 2026-Q2 |
| WebSearch tool | Adopted (harness) | Real-time research in sessions | Available via tool harness; used in this audit | — |
| WebFetch tool | Adopted (harness) | Read specific URLs in sessions | Available via tool harness | — |
| PowerShell tool | Adopted | Windows shell operations alongside Bash | `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in settings | settings.json |
| Image input | Available, not evaluated | Visual debugging, doc reading | Solo dev; rare use case | — |
| Computer use (research preview, Mar 2026) | Available, deferred | GUI automation | Deferred — terminal/file workflow covers dev loop; no GUI verification tasks | — |
| GitHub Actions / CI integration | Available, not evaluated | Automated PR review, Slack routing | Codex covers code review; GitHub Actions integration not configured | — |

### Project-level features

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| `CLAUDE.md` auto-read | Adopted | Session contract | Required per Gap #5 template; active in all 3 repos | PLAYBOOK Gap #5 |
| `AGENTS.md` cross-tool governance | Adopted | Canonical per-repo governance | Per Gap #6 template; active in corp-monorepo, ai-council | PLAYBOOK Gap #6 |
| Project-level skills | Adopted | Repo-specific knowledge | corp-monorepo: gotchas skill | PLAYBOOK 7a |
| Project-level commands | Adopted | Repo-specific invokable actions | .dev-knowledge: `/save`; corp-monorepo: none | PLAYBOOK 7b |
| Project-level rules (`.claude/rules/`) | Adopted | Domain-specific constraints enforced per repo | .dev-knowledge: `git-discipline.md`; user-level: `core-invariants.md` | — |
| Project-level subagents | Available, not evaluated | Repo-specific delegation | None configured; user-level subagents sufficient for current needs | PLAYBOOK 7d |
| Project-level Claude Code hooks | Partial | Repo-specific lifecycle automation | corp-monorepo `settings.local.json` exists (content not audited). No hooks in .dev-knowledge | — |
| Managed settings (`managed-settings.d/`) | N/A | Organization-wide policy enforcement | Solo dev; no enterprise management layer | — |

### Observability

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| `ccusage` (npm CLI) | Adopted | Scriptable token usage export | Replaced `/stats` TUI; integrated into `/session-summary` | tech-radar 2026-Q2 |
| `/usage` command (merged `/cost` + `/stats`) | Superseded | Interactive token tracking | ccusage covers this; `/usage` available but not primary | — |
| `claude --version` | Adopted | Tool version tracking | v2.1.119 as of 2026-04-25 | — |
| `showThinkingSummaries` | Adopted | Visibility into reasoning process | `=true` in settings; thinking summaries visible in output | settings.json |
| Monitor tool — live log streaming (Apr 2026) | Available, not evaluated | React to streaming background process output | New Apr 2026; potential value for long-running test runs or deploy monitoring | — |
| Session transcripts (`~/.claude/sessions/`) | Available, not evaluated | Audit trail, replay | Sessions directory exists; not surfaced in regular workflow | — |

### Cloud & scheduling (new Apr 2026)

| Feature | Status | Use case | Decision | Reference |
|---------|--------|----------|----------|-----------|
| Routines / `/schedule` (cloud-scheduled tasks) | Available, not evaluated | Recurring automated tasks without local machine | `/schedule` skill available in harness; cloud execution on Anthropic infra; no routines configured | — |
| Ultraplan (early preview, Apr 2026) | Available, not evaluated | Draft plans in cloud, review in web editor, run remotely or locally | New capability; browser-based plan review could complement browser chat layer | — |
| Ultrareview (research preview, Mar 2026) | Available, not evaluated | Multi-agent parallel code review in cloud sandbox | Available as user-triggered command; currently using single-agent Codex `/review`; $5-20/run; 3 free runs through May 2026 | — |

## Blind spots identified

Features available that Rob hasn't evaluated and could provide genuine workflow value:

1. **Ultrareview** — Multi-agent parallel code review running in cloud sandbox. Currently `/review` uses single-agent Codex (synchronous, limited parallelism). Ultrareview runs fleet of parallel agents with independent finding verification. Potential: catch more bugs pre-merge with less manual review effort. Trigger to evaluate: next complex PR where Codex review feels shallow. Note: 3 free runs expire May 5, 2026 — time-sensitive.

2. **Routines / `/schedule`** — Cloud-scheduled recurring agents (no local machine needed). Currently ecosystem snapshots and token reports are session-triggered. Routines could automate weekly `.dev-knowledge` health checks, `ccusage` snapshots, or session scorecard reviews on a cron schedule. Trigger to evaluate: first time Rob forgets to run a recurring task twice in a row.

3. **Monitor tool** — Streams background process stdout into the session as events. Potential: "start pytest, continue working, get notified when test suite finishes or first failure appears." Currently: wait-and-poll or separate terminal. Trigger to evaluate: next session with a >2-minute test run.

4. **Project-level Claude Code hooks (corp-monorepo)** — `settings.local.json` exists but content not audited in this pass. May already have hooks; or may be empty. Verify: read corp-monorepo `settings.local.json`.

5. **Xhigh effort level** — Between "high" and "max" effort on Opus 4.7. Not tried yet. Current maximum is "high" (used implicitly with Opus prompts). Trigger to evaluate: prompt where Opus 4.7 at current effort still misses key design considerations.

## Recommendations for next quarter

Surface these for tech-radar 2026-Q3 evaluation:

- **Ultrareview** — Pilot: use on next complex corp-monorepo PR before May 5 free-run expiry. Evaluate quality vs Codex `/review`. If better, define cost ceiling for regular use.
- **Routines** — Evaluate: define which recurring `.dev-knowledge` or ecosystem tasks would benefit from cron scheduling. Propose a single low-stakes routine (weekly ccusage snapshot) as pilot.
- **Monitor tool** — Evaluate: next session with long-running background process. One trial sufficient to determine if it fits the loop-and-notify pattern.
- **Auto mode** — Revisit: assess whether `skipDangerousModePermissionPrompt=true` + manual approval covers the same ground, or if Auto mode's classifier offers meaningfully different behavior.
- **corp-monorepo `settings.local.json`** — Immediate: read content and document project-level hook state. Should be in AGENTS.md Section 5 if hooks are active.

## Cross-references

- `docs/tech-radar/2026-Q2.md` — quarterly tech-radar (this audit feeds Q3 triage)
- `PLAYBOOK.md` Section "Claude Code internals" — mechanism definitions (skills, commands, hooks, subagents)
- `PLAYBOOK.md` Section 6 "Continuous Improvement" — adoption pipeline
- `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Gap #9 specification

## Methodology notes

- **Web search performed:** Yes — Explore subagent ran WebSearch + WebFetch against code.claude.com docs, GitHub releases, and secondary sources. Source date: 2026-04-25.
- **Filesystem inventory:** `~/.claude/` (commands, agents, skills, plugins, rules, hooks, settings); `corp-monorepo/.claude/`; `.dev-knowledge/.claude/`
- **Settings confirmed:** All settings.json env vars and flags verified from file content
- **Limitations:** Web search covers through ~Apr 10 2026 (Week 15 release notes). Features released Apr 11–25 may be missing. corp-monorepo `settings.local.json` content not read.
- **Next audit recommended:** 2026-Q4 (after meaningful adoption cycle), or sooner if Anthropic ships a major Claude Code release
