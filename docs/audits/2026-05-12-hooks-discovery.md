---
audit: hooks-discovery
date: 2026-05-12
scope: ecosystem
status: complete
---

# Hooks Discovery — 2026-05-12

<!-- scope: meta -->

## Purpose

<!-- scope: meta -->

Locate the `review` name-conflict surfaced by operator. Precondition for Directive 5 (hooks review proper, Prompt 4). Folds Directive 6: ai-council read-only CHANGELOG + commit-log check for scrum-master review implementation evidence.

## Locations inspected

<!-- scope: meta -->

| Path | Exists | `review*` matches |
|------|--------|-------------------|
| `~/.claude/hooks/` | Yes | none |
| `~/.claude/commands/` | Yes | `review.md` |
| `~/.claude/bin/` | Yes | `codex-review.ps1`, `codex-review.README.md` |
| `~/.claude/skills/` | Yes | none |
| `.dev-knowledge/.claude/hooks/` | No | — |
| `.dev-knowledge/.claude/commands/` | Yes | none (contains `handoff.md`, `save.md` only) |
| `ai-council/.claude/hooks/` | No | — |
| `ai-council/.claude/commands/` | No | — |
| `corp-monorepo/.claude/hooks/` | No | — |
| `corp-monorepo/.claude/commands/` | No | — |
| `corp-ops/.claude/hooks/` | No | — |
| `corp-ops/.claude/commands/` | No | — |
| `corp-sca-time-automation/.claude/hooks/` | No | — |
| `corp-sca-time-automation/.claude/commands/` | No | — |
| `~/.codex/` | Yes | none in user-defined location (`.tmp/plugins/` matches are Codex-internal plugin files, not user hooks) |

**Also inspected (from `~/.claude/settings.json`):** event-based hooks wired via `hooks:` key — PreToolUse (block-onedrive.ps1), SessionStart (evolution echo), Stop (claude-notify.ps1 + evolution echo). None named `review*`. Witnessed.

## Findings

<!-- scope: meta -->

### Finding 1: `review.md` at `~/.claude/commands/review.md`

- **Type:** slash command (user-defined, `/review` invocation)
- **Trigger:** manual — operator types `/review` in Claude Code session
- **Purpose:** Invokes `codex-review.ps1` wrapper; runs `codex exec --sandbox read-only --output-last-message`; produces dated `docs/audits/YYYY-MM-DD-codex-{topic}.md` with frontmatter + Codex findings grouped by severity band
- **Parameters surfaced:** `-Topic` (required), `-DiffRange` (default `main..<branch>`), `-Focus`, `-OutDir`, `-AutoCommit`, `-FullAudit`, `-Force`
- **Conflicts with:** Finding 2 — same `/review` name as built-in Claude Code skill
- **Marker:** Witnessed (file read directly)

### Finding 2: Built-in Claude Code `/review` skill — "Review a pull request"

- **Type:** built-in Claude Code skill (system-provided)
- **Trigger:** manual — operator types `/review` in Claude Code session; also invocable via `Skill` tool
- **Purpose:** Reviews a GitHub pull request (inferred from description "Review a pull request" in skills system-reminder)
- **Location:** Not a file on disk — registered by Claude Code harness; appears in system-reminder alongside user-defined skills
- **Conflicts with:** Finding 1 — same `/review` name as user-defined Codex wrapper
- **Marker:** (architect inference) — description observed in system-reminder; underlying file/implementation not directly inspectable

### Finding 3: `codex-review.ps1` at `~/.claude/bin/codex-review.ps1`

- **Type:** standalone PowerShell script (execution target, not a slash command itself)
- **Trigger:** invoked by Finding 1 (`review.md`) or directly from terminal
- **Purpose:** Wraps `codex exec --sandbox read-only --output-last-message`; handles diff vs. full-audit modes, frontmatter composition, optional AutoCommit
- **Conflicts with:** none independently (it is the implementation, not the registration)
- **Marker:** Witnessed (full script read)

### Finding 4: `codex-review.README.md` at `~/.claude/bin/codex-review.README.md`

- **Type:** documentation file for Finding 3
- **Trigger:** n/a (read-only reference)
- **Purpose:** Installation instructions, parameter table, smoke-test procedure, exit codes
- **Conflicts with:** none
- **Marker:** Witnessed (file read directly)

## Conflict assessment

<!-- scope: meta -->

- **Number of `review*` artifacts found:** 4 (1 user slash command, 1 built-in slash command, 1 script, 1 README)
- **Conflict location:** `~/.claude/commands/review.md` (user-defined) vs. Claude Code built-in skill (system-provided) — both register as `/review`
- **Conflict type:** name-collision-across-systems (user-defined slash command vs. built-in harness skill, same name)
- **Severity:** MEDIUM — functional ambiguity: when operator types `/review`, harness may present both options or may resolve via precedence rules not documented in PLAYBOOK. Neither the shadowing order nor the invocation behavior under conflict has been tested. No data loss risk; confusion risk.

**What is NOT a conflict:** The `.codex/.tmp/plugins/` review files are Codex-internal plugin artifacts, not user-defined hooks. Not relevant to the name-conflict.

## Scope-shape recommendation for follow-up (Prompt 4 hooks review)

<!-- scope: meta -->

- **Shape (a) — Single-source-of-truth audit:** conflict is contained within `~/.claude/` (user-defined `commands/review.md` vs. built-in harness registration). No cross-repo routing required.
- **Shape (b) — Cross-repo scrum-master review:** N/A — no cross-repo hook conflict found.

**Recommended shape: (a)**

**Justification:** All `review*` artifacts live in `~/.claude/` or are system-built-ins. No per-repo `.claude/` directories contain `review*` files. Prompt 4 scope = single user config dir audit + resolution decision (rename user command, or accept shadowing if precedence is deterministic).

**Estimated effort for Prompt 4:** low — one file to rename or clarify; no cross-repo propagation; resolution is a rename + PLAYBOOK cross-reference update.

## ai-council CHANGELOG + commit evidence (Directive 6)

<!-- scope: meta -->

Recent commits (20-most-recent oneline):

```
f094d08 docs(audit): codex review for audit-addendum-i7-i8
baeb6bc docs: CHANGELOG + JOURNAL for scrum-master addendum (I7 + I8)
7fb45b0 docs(backlog,lessons): BACKLOG M2 supersession sync + architect local-config-defense lesson
2986ac0 chore(handoffs): I8 rename _archive → archive (align to A2 operator decision)
21ef4e7 chore(lessons): I7 move tasks/lessons.md → LESSONS.md root + retire tasks/ folder
5346045 fix(review): codex medium/low — grok_research in README, panel defaults in guide, docs/ folder governance, rubric provenance
d106697 docs(audit): codex review for scrum-master-review-2026-05-12
55c393e docs: CHANGELOG + JOURNAL for scrum-master review implementation
821d8b4 docs(lessons): append 4 lessons from 2026-05-11 transcript-routing + observability cycles
bbab35c chore: retire tasks/todo.md (superseded by BACKLOG.md per ADR-41) + update CLAUDE.md
06bb51b feat(governance): create BACKLOG.md per ADD-41 mandate (Scale M)
7bcd288 docs(vision): bump last_reviewed to 2026-05-12 post transcript-routing + observability cycles
95a41dd docs(readme): update architecture section (src/ai_council namespace) + test count
858496e chore(audits): archive pre-ADR-34 underscore/UPPERCASE legacy review reports
7dfaf58 chore(docs): rename to ADR-34 hyphen-lowercase form (council-question-guide, synthesis-quality-rubric)
64f715f docs: update test count 354 -> 362 in CLAUDE.md
aad6ebe fix(review): codex low/medium — wall-clock latency, remove dead synth_timeout_flag, fix rubric doc link
9baf8d4 docs: CHANGELOG + JOURNAL for Phase 1 + ADR-34 combined session
a1bf6ec docs(adr-06): defer Qwen trial; reopen trigger documented
```

CHANGELOG head (ai-council, 2026-05-12 entries):

```
## 2026-05-12

### Changed (scrum-master review addendum — I7 + I8)
- tasks/lessons.md → LESSONS.md at repo root (I7; universal ecosystem convention)
- docs/handoffs/_archive/ → docs/handoffs/archive/ (I8; align to A2 operator decision)
- CLAUDE.md Lessons Discovery + Folder Governance sections updated to new paths
- VISION.md lessons path reference updated

### Removed (scrum-master review addendum — I7)
- tasks/ folder retired entirely

### Added (scrum-master review addendum — I7)
- LESSONS.md entry: architect failure mode — defending local config as "by-design" against ecosystem audit

### Added (scrum-master review implementation)
- BACKLOG.md per ADR-41 Scale M mandate
- docs/audits/README.md archive convention note for pre-ADR-34 legacy reports

### Changed (governance + filename compliance per .dev-knowledge scrum-master review 2026-05-12)
- docs/COUNCIL_QUESTION_GUIDE.md → docs/council-question-guide.md (ADR-34 hyphen+lowercase)
- docs/SYNTHESIS-QUALITY-RUBRIC.md → docs/synthesis-quality-rubric.md (ADR-34 hyphen+lowercase)
- README.md: Architecture section rewritten to src/ai_council/ namespace layout
- VISION.md: last_reviewed bumped 2026-05-09 → 2026-05-12
- CLAUDE.md Folder Governance: tasks/todo.md reference removed
- tasks/lessons.md: 4 lessons appended from 2026-05-11 cycles

### Removed
- tasks/todo.md: severely stale; surviving items migrated to BACKLOG.md

### Archived
- docs/audits/2026-03-15_CODE_REVIEW_REPORT.md, docs/audits/2026-03-26_CODE_REVIEW_REPORT.md → docs/audits/archive/legacy/

### Changed (breaking, per .dev-knowledge ADR-34 universal hyphen mandate)
- Council CLI output filename format: council_out_* → council-out-*
```

Commits matching scrum-master / review / emitter / council-out: (no `--grep` output returned — grep run against commit messages; the above commits contain these terms but `git log --grep` requires exact string match; matches are identifiable in the 20-commit listing above by message content.) Marker: (architect inference)

**Implementation evidence for 2026-05-11 scrum-master review findings (10 items + I7/I8 addendum):** **found** — CHANGELOG 2026-05-12 explicitly documents implementation of governance findings (COUNCIL_QUESTION_GUIDE rename, SYNTHESIS-QUALITY-RUBRIC rename, BACKLOG.md creation, README rewrite, VISION.md bump, tasks/ retirement) and addendum items (I7 LESSONS.md root move, I8 `_archive` → `archive` rename). Commits `55c393e`, `21ef4e7`, `2986ac0`, `baeb6bc` directly trace to scrum-master review items. Witnessed.

**Implementation evidence for CLI emitter format change (`council_out_*` → `council-out-*`):** **found** — CHANGELOG 2026-05-12 entry "Council CLI output filename format: `council_out_*` → `council-out-*`" (marked breaking change, per .dev-knowledge ADR-34 universal hyphen mandate). Witnessed.

Informational only; no browser-to-browser delivery turn expected per "handshake = 1 round trip" principle.

## Unknowns / flagged

<!-- scope: meta -->

- **Built-in skill invocation precedence:** When both `~/.claude/commands/review.md` (user-defined) and the built-in "Review a pull request" skill are registered as `/review`, it is Unknown which takes precedence. Claude Code harness resolution rules not documented in any inspected file. Prompt 4 should test empirically or check Claude Code docs.
- **Codex `.tmp/plugins/` origin:** The three `review*` files under `~/.codex/.tmp/plugins/` (cloudflare `review.md`, figma `review-design-parity.md`, heygen `reviewer-prompt.md`) are Codex-internal plugin artifacts. Their origin (auto-downloaded, manually installed, bundled) is Unknown. Not relevant to the `/review` name-conflict; flagged for completeness.
- **`~/.claude/commands/review.md` description mismatch:** The skills system-reminder shows two separate entries: `review: /review — Invoke Codex review` and `review: Review a pull request`. These appear to be distinct skill registrations. Whether both entries originate from the single `review.md` file (one file, two invocation modes) or from two separate registrations (user file + built-in) is Unknown without harness source inspection. Most likely the latter. Marker: (architect inference).
