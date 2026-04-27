# Handoffs — `.dev-knowledge`

<!-- scope: meta -->

> Session boundary artifacts. Most recent handoff = newest folder
> or file by date prefix.

## Two formats coexist

**New format (since 2026-04-27)** — folder per session:

```
{date}-{session-slug}/
├── upload-instructions.md
├── first-message.md
└── contents/
    ├── HANDOFF.md
    ├── manifest.json
    ├── tree.txt
    └── point-in-time copies of relevant governance docs
```

**Legacy format (before 2026-04-27)** — single `.md` file. Preserved
as-is.

## How to find current session

```bash
ls docs/handoffs/ | sort | tail -5
```

## Format decision rationale

See:
- `docs/decisions/transcripts/DECISION_29_handoff_synergy.md` (Topic 2 — handoff synergy debate)
- `docs/research/2026-04-27-handoff-patterns-council-research.md` (Council research-mode debate)
- `docs/research/2026-04-27-handoff-patterns-external-research.md` (single-shot research report)
- `protocols/PLAYBOOK.md` § "Handoff format spec (since 2026-04-27)"

## First folder-format instance

`docs/handoffs/2026-04-27-stream-c-session-1-final/` — Stream C
session 1 close.
