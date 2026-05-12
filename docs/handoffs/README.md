# Handoffs — `.dev-knowledge`

<!-- scope: meta -->

Session boundary artifacts. Canonical format defined by ADR-42 (v3.2, ratified 2026-05-09).

## Current format (v3.2, per ADR-42, ratified 2026-05-09)

Each session produces a flat folder with no subdirectories:

```
docs/handoffs/{YYYY-MM-DD}-{slug}/
├── 00_README.md
├── 00_first-message.md
├── 01_MANIFEST.md
├── 01_manifest.json
├── 02_VISION.md
├── 03_PLAYBOOK.md
├── 04_ESSENTIALS.md
├── 05_GOVERNANCE_ESSENCES.md
├── 06_STATE_OF_PLAY.md
├── 07_ACTION_PLAN.md
├── 08_TREE.txt
└── 09_EXECUTION_EVIDENCE.md
```

**First v3.2 instance:** `docs/handoffs/2026-05-09-ai-council-audit-sync/`

## Stage 1+2 archive

`archive/{slug}/` holds `stage1-question.md` + `stage2-response.md` inputs after Stage 3 generation.

## In-progress

`_in_progress/{slug}/` exists during a handoff session; cleaned at Stage 3 close per HANDOFF_PROCESS.md step 10.

## How to find current session

```powershell
Get-ChildItem docs/handoffs/ | Sort-Object Name | Select-Object -Last 5
```

## Pre-v3.2 legacy (historical, do not edit)

Relocated to `docs/handoffs/archive/legacy/` per Prompt K atomic migration (2026-05-12).

### Flat `.md` files (legacy single-file format, pre-2026-04-27)

- `archive/legacy/2026-04-15-codex-tach-opus47-session.md`
- `archive/legacy/2026-04-15-tech-radar-session.md`
- `archive/legacy/2026-04-21-dev-knowledge-architecture-redefinition.md`
- `archive/legacy/2026-04-21-tech-radar-session.md`
- `archive/legacy/2026-04-26-stream-b-complete-stream-c-scope.md`
- `archive/legacy/2026-04-26-stream-c-session-1-branch-convention.md`

### Folder v2 format (pre-2026-05-09, pre-ADR-42)

- `archive/legacy/2026-04-27-stream-c-session-1-final/` — uses `contents/` subfolder + `upload-instructions.md`

## References

- `docs/decisions/ADR-42-handoff-format-v3.md` — canonical format spec
- `protocols/HANDOFF_PROCESS.md` — operational procedure
- `templates/HANDOFF_FOLDER_TEMPLATE.md`
- `templates/HANDOFF_QUESTION_TEMPLATE.md`
