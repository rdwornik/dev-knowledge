---
audit: skills-hooks-usage-review
date: 2026-05-17
scope: ecosystem
status: complete
---

# Skills and Hooks Usage Review — 2026-05-17

<!-- scope: meta -->

**Author:** Claude Code (Sonnet 4.6) in `.dev-knowledge`
**Purpose:** Assess how `.claude/skills/` and `.claude/hooks/` are used
across the ecosystem repos; surface usage gaps and document clearer
guidance. Output is a review note — any PLAYBOOK-worthy guidance is
*recommended* here for a future session, not applied now.

---

## 1. Inventory

### 1.1 Global skills (`~/.claude/skills/`)

| Skill | File | Trigger | Used in practice? |
|---|---|---|---|
| `gotchas` | `~/.claude/skills/gotchas/SKILL.md` + `gotchas.md` | Manual (`/gotchas`) or pre-task CLAUDE.md mandate | Yes — CLAUDE.md says "check gotchas.md before modifying any file" |
| `verify` | `~/.claude/skills/verify/SKILL.md` | Manual (`/verify`) | Sparse — SKILL.md body is empty; trigger guidance lives only in CLAUDE.md P1 step 5 |

### 1.2 Global commands (`~/.claude/commands/`)

| Command | Purpose | Trigger |
|---|---|---|
| `/boot` | Session start sweep (memory + rules) | Manual |
| `/codex-review` | Run Codex review via `codex-review.ps1` | Manual |
| `/evolve` | Evolution audit — promotions and prunings | Manual |
| `/session-summary` | Generate token-efficient session summary | Manual |

### 1.3 Project-level skills

| Repo | Path | Content |
|---|---|---|
| `corp-monorepo` | `.claude/skills/gotchas/` | Project-specific gotchas (SKILL.md + gotchas.md) |
| `ai-council` | — | None |
| `.dev-knowledge` | — | None |
| `corp-sca-time-automation` | — | None |
| `corp-ops` | — | None |

### 1.4 Project-level commands

| Repo | Path | Content |
|---|---|---|
| `.dev-knowledge` | `.claude/commands/` | `handoff.md`, `save.md` |
| All others | — | None |

### 1.5 Hooks (`~/.claude/settings.json`)

| Event | Matcher | Command | Purpose |
|---|---|---|---|
| `PreToolUse` | `Bash` | `block-onedrive.ps1` | Block all Bash commands touching OneDrive paths |
| `SessionStart` | `""` (all) | echo evolution reminder | Prompt Claude to load memory/corrections at start |
| `Stop` | `""` (all) | `claude-notify.ps1` | Desktop notification on session end |
| `Stop` | `""` (all) | echo evolution reminder | Prompt Claude to write session scorecard |

**No project-level hooks exist in any repo** (`.claude/settings.json`
does not have a `hooks` key in any repo checked). Project-level
permissions are set in `.claude/settings.local.json` only.

---

## 2. Observations

### 2.1 The gotchas skill is the most adopted pattern

The global `gotchas` skill is the clearest success: it is referenced in
CLAUDE.md, has structured content in `gotchas.md`, and the corp-monorepo
correctly extends it with a project-specific layer. No other repo has
adopted the project-level gotchas pattern, which means ai-council,
corp-ops, and corp-sca-time-automation have no repo-specific gotcha
surface.

### 2.2 The `verify` skill is a stub

`~/.claude/skills/verify/SKILL.md` contains only frontmatter — no body,
no instructions, no reference to what scripts to run. The actual
verification guidance lives in CLAUDE.md P1 step 5 ("Run tests. Run
verification if available"). The skill exists as a namespace but is not
a usable skill in the Claude Code sense. Anyone typing `/verify` gets a
near-empty invocation.

### 2.3 All hooks are global, reactive, and non-project-specific

The three hook events (PreToolUse, SessionStart, Stop) serve
cross-cutting concerns — safety (OneDrive block), memory hygiene
(evolution), and UX (notification). No project has wired hooks for
project-specific automation (e.g., run tests after a file write, check
for forbidden patterns before a commit).

This is probably fine for a solo-operator ecosystem where Claude Code
sessions are short and focused, but it means the hook system is
underused for project-level guardrails.

### 2.4 Session hygiene hooks echo, but don't act

The SessionStart and Stop hooks emit reminder text to Claude's context
but do not execute any file writes. The self-evolution protocol
(corrections.jsonl, sessions.jsonl) depends on Claude remembering to
write these during the session. The hook reminder helps, but a missed
write isn't caught by any automated check.

### 2.5 Project commands are sparse

Only `.dev-knowledge` has project-level commands (`/handoff`, `/save`).
These are high-value — `/save` is used regularly. Other repos have no
project commands at all, meaning the global command set must cover all
repos. This creates a discoverability gap: an operator in corp-monorepo
has no repo-local reminder of project-specific slash commands.

---

## 3. Guidance for using skills well

Drawn from observed patterns:

**Skills are instructional context, not executables.** A skill's body
tells Claude *how to do something*. The trigger is manual (`/skill-name`
in the prompt). Skills should not be empty stubs — if the content lives
elsewhere (e.g., in CLAUDE.md), either consolidate it into the skill or
remove the stub.

**Project-level gotchas skills should exist for every active repo.**
The `corp-monorepo` pattern is the right one: a `SKILL.md` + `gotchas.md`
under `.claude/skills/gotchas/` that extends the global gotchas. Any
repo that has recurring failure patterns (shell quoting, test isolation,
import order) should have this.

**Don't add a skill for a one-liner.** A skill is worth adding when the
instructional content is ≥5 lines and would be tedious to re-dictate
every session. Single-command reminders belong in CLAUDE.md, not a skill.

---

## 4. Guidance for using hooks well

**Hooks are automated reactive behaviors, not instructional content.**
A hook fires unconditionally on an event. Use hooks for things that must
*always* happen — safety gates, notifications, context echoes. Use skills
for things that happen *on demand*.

**The three-hook model (PreToolUse safety / SessionStart context / Stop
notification) covers the most common needs.** Before adding a new hook,
check whether the need is truly automated (hook) or just a reminder to
Claude (skill/CLAUDE.md).

**Project-level hooks are appropriate for hard guardrails.** Examples:
- `PreToolUse` on `Write` to block writes to specific paths
- `PostToolUse` on `Edit` to automatically run `ruff check` on changed files
- `PreToolUse` on `Bash` to block destructive commands in non-interactive mode

These are not currently used anywhere in the ecosystem. The OneDrive
block pattern is the template: a PowerShell script that inspects the
tool input and exits non-zero to block.

**Hook failures should be auditable.** The current hooks produce output
(echo, PS1 notifications) but not structured logs. If a hook fires and
blocks something, the operator only knows via the session transcript. A
future pattern worth considering: append hook-block events to a
`~/.claude/hook-audit.log`.

---

## 5. Recommendations (for future session, not this one)

| Priority | Recommendation | Effort |
|---|---|---|
| M | Fill the `verify` skill body with actual instructions and a reference to what scripts exist | Low |
| M | Add `.claude/skills/gotchas/` to ai-council and corp-sca-time-automation | Low |
| L | Consider a `PostToolUse` hook on `Edit`/`Write` to echo "run tests now" reminder | Low |
| L | Document the hook-and-skill separation principle in PLAYBOOK § Claude Code Workflow | Low |
| L | Add `/save`-equivalent command to corp-monorepo and ai-council (if they don't get it via global commands) | Low |

No governance ADR is needed for any of the above — these are operational
improvements within the existing architecture.
