# Upload Instructions — Stream C Session 1 Final Handoff

<!-- scope: meta -->

## To resume this work in a new browser chat

1. Drag the entire `contents/` folder into the chat input area.
   All files inside upload at once.

2. Wait for upload completion.

3. Open `first-message.md` (sibling of this file). Copy its
   contents verbatim. Paste into the chat as your first message.

4. Browser will read manifest, then files in order specified,
   then propose plan for next steps.

## What's in `contents/`

- `HANDOFF.md` — current session state, decisions, pending work
- `manifest.json` — context orchestration index
- `tree.txt` — repo structure snapshot
- `ESSENTIALS.md` — point-in-time copy of universal Claude rules
- `PLAYBOOK.md` — point-in-time copy of full process reference
- `JOURNAL.md` — point-in-time copy of session timeline
- `CLAUDE.md` — point-in-time copy of repo-specific governance

## Why this format

Per Topic 2 + Research synthesis (2026-04-27): single drag-drop
target avoids file-fishing across repo paths. Point-in-time copies
prevent drift between session intent and current live state at
resume time. `manifest.json` provides browser with deterministic
upload index + reading order + rationale. `tree.txt` orients
browser to repo structure post-cleanup.
