# README — Handoff 2026-05-25-dev-knowledge-session-sync

## What this folder is

A Stage 3 handoff bundle for **`.dev-knowledge`** (type: session-sync), generated
per ADR-42 v3 / HANDOFF_PROCESS v3.3.3. It transfers session state into a fresh
claude.ai chat so work can continue with full methodology context.

The OLD chat that produced this handoff (Stage 2 source) **can now be closed** —
its accumulated knowledge is captured in `06_STATE_OF_PLAY.md` and
`07_ACTION_PLAN.md`.

This is a **self-handoff** (target = `.dev-knowledge`), so the bundle is **11
manifest-tracked files** — `02b_ECOSYSTEM_VISION.md` is intentionally absent
(`02_VISION.md` already is this repo's VISION).

Stage 1 + Stage 2 inputs are archived at
`docs/handoffs/archive/2026-05-25-dev-knowledge-session-sync/`.

## Operator workflow

1. Open a **NEW** claude.ai chat (fresh, zero context — NOT the OLD chat).
2. Drag-drop all files from this folder, OR zip and upload the zip.
3. Paste the content of `00_first-message.md` as the first message.
4. The NEW chat completes the **articulation gate** (4 items in its own words),
   then waits. Confirm with `role confirmed`.
5. The NEW chat presents **receiver synthesis**, then waits. Respond with:
   - `synthesis confirmed` — proceed, or
   - `synthesis correction: [specifics]` — it updates and re-presents.
6. **Q&A loop** (if the NEW chat has questions): it presents up to 3 per round;
   take them to the OLD chat, return answers; max 3 rounds.
7. The NEW chat asks "single Claude Code prompt or split?" — answer by directive
   complexity (split if 5+ directives or a verification-critical gate).
8. The NEW chat generates Claude Code prompt(s) as downloadable `.md` files.
9. Open Claude Code **in `.dev-knowledge`** and run the prompts sequentially.
10. Fill `09_EXECUTION_EVIDENCE.md` after the work and commit it back to
    `docs/handoffs/2026-05-25-dev-knowledge-session-sync/` for the next session.

## File index

| File | Purpose |
|---|---|
| `00_README.md` | This file |
| `00_first-message.md` | First message for the NEW chat |
| `01_MANIFEST.md` | Entry point, repo state, file index, drift check |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | `.dev-knowledge` mission and scope |
| `03_PLAYBOOK.md` | Methodology (full copy) |
| `04_ESSENTIALS.md` | Cheat-sheet rules (full copy) |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences (ADR-42/45/49/28) |
| `06_STATE_OF_PLAY.md` | Current state + Stage 3 verification |
| `07_ACTION_PLAN.md` | Goal, directives, hard constraints, fallbacks |
| `08_TREE.txt` | Repo file inventory |
| `09_EXECUTION_EVIDENCE.md` | Return-trip template |

## Notes

- This bundle is the Stage 3 handoff per ADR-42 v3.
- Stage 1 + Stage 2 inputs: `docs/handoffs/archive/2026-05-25-dev-knowledge-session-sync/`.
- If the Q&A loop produces amendments, they are archived as
  `archive/2026-05-25-dev-knowledge-session-sync/stage2-amendments.md`.
