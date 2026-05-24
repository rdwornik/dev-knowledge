# Workspace Combo Setup — Multi-root + Modified Sort + Open-Latest Tasks
<!-- dated: 2026-05-24 -->

## What was set up

A native VS Code combo (no extensions) for fast access to dated artifacts:

1. **Multi-root workspace** (`.dev-knowledge.code-workspace`) — 5 folders:
   - `📓 .dev-knowledge` — full repo root
   - `⚙️ ~/.claude (config)` — Claude Code user config
   - `📅 Audits` → `docs/audits/`
   - `📅 Handoffs` → `docs/handoffs/`
   - `📋 ADRs` → `docs/decisions/`
   Each dated-folder alias appears as a separate Explorer root, so its contents are immediately visible without drilling through `docs/`.

2. **`explorer.sortOrder: "modified"`** — within each root, most-recently-touched files appear at the top. Combined with the dated-folder aliases, this surfaces the latest artifact in each category without any filename hacks.

3. **Workspace tasks** — three tasks for single-keystroke access to the latest file in each dated folder:
   - `open-latest-audit` — opens newest `*.md` in `docs/audits/` by name-desc
   - `open-latest-handoff` — opens newest `HANDOFF.md` in `docs/handoffs/` by directory-desc
   - `open-latest-adr` — opens newest `ADR-*.md` in `docs/decisions/` by name-desc

## Recommended user-scope keybindings

Add to your personal `keybindings.json` (Ctrl+Shift+P → "Preferences: Open Keyboard Shortcuts (JSON)"):

```json
{ "key": "ctrl+alt+a", "command": "workbench.action.tasks.runTask", "args": "open-latest-audit" },
{ "key": "ctrl+alt+h", "command": "workbench.action.tasks.runTask", "args": "open-latest-handoff" },
{ "key": "ctrl+alt+d", "command": "workbench.action.tasks.runTask", "args": "open-latest-adr" }
```

## Post-merge operator actions

1. **Reopen workspace** — File → Open Workspace from File → `.dev-knowledge.code-workspace` (multi-root changes take effect on reopen, not file save)
2. **Add keybindings** as above (user-scope, cannot be committed to repo)
3. **Trial 2–3 days** — evaluate cognitive load:
   - Does the 5-root Explorer panel feel cluttered or useful?
   - Does modified-sort surfacing latest-touched actually help navigation?
   - Are the task keybindings used, or does Ctrl+Shift+P feel fast enough?

## Revert path (if combo doesn't work)

- Partial revert (keep root hygiene, revert workspace): `git revert d87bd31` (Step 4 commit)
- Full revert of workspace+tasks: `git revert d87bd31 <step5-sha>`
- Root hygiene file moves (Steps 1+2) are low-risk and worth keeping regardless

## Why this approach

VS Code has no native per-folder sort order override — `explorer.sortOrder` is workspace-global. The workaround options were:

| Option | Approach | Cost |
|--------|----------|------|
| A (this) | Multi-root aliases + modified sort + tasks | Native, no ext, ~5 Explorer roots |
| B | Filename prefix hack (00-, 01- prefixes) | Pollutes filenames, affects git log |
| C | `explorer.sortOrderReverse: true` (v1.93+) | Reverses ALL folders, not just dated ones |
| D | Custom extension | Build cost ~4–8h; overkill for 3 folders |

Option A chosen for empirical trial per operator decision 2026-05-23.
