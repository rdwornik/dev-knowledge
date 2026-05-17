# README — 2026-05-17 .dev-knowledge session-sync handoff

## What this folder is

- **Date generated:** 2026-05-17
- **Type:** session-sync
- **Target repo:** `.dev-knowledge`
- **Format:** ADR-42 v3.3.3 (11-file self-applied bundle)

The OLD `.dev-knowledge` browser chat (Stage 2 source) can be closed —
its knowledge is preserved in this bundle (primarily in
`06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`).

Stage 1 and Stage 2 inputs are archived at
`.dev-knowledge/docs/handoffs/archive/2026-05-17-dev-knowledge-session-sync/`.

## Operator workflow (10 steps)

1. Open NEW claude.ai chat (fresh, zero context — **NOT** the OLD chat).
2. Drag-drop all 11 files from this folder, OR zip and upload zip. *(Skip
   `00_README.md` if you want — it is operator-facing only.)*
3. Paste content of `00_first-message.md` as the first message.
4. NEW chat reads bundle, performs the four-item articulation gate, then
   presents receiver synthesis.
5. Confirm synthesis. Type exact phrase:
   - `synthesis confirmed` — proceeds to Q&A or prompt generation
   - `synthesis correction: [specifics]` — NEW chat updates, re-presents
6. Q&A loop (if NEW chat asks clarification questions):
   - NEW chat presents up to 3 questions per round
   - Take to OLD chat (Stage 2 source), get answers, paste back
   - Max 3 rounds
7. NEW chat asks: "single Claude Code prompt or split?" Pick:
   - Single: small directive count, no verification gates
   - Split: 5+ directives OR verification-critical gate
8. NEW chat generates Claude Code prompt(s) as downloadable `.md` files.
9. Open Claude Code in `.dev-knowledge` (target repo). Paste prompts.
   Claude Code executes.
10. Return the populated `09_EXECUTION_EVIDENCE.md` to `.dev-knowledge`
    for the next session.

## File index

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | First message to paste into NEW chat |
| `01_MANIFEST.md` | Entry point, file index, HEAD pin (ancestor-validated), synthesis prompt |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | `.dev-knowledge` VISION.md — target repo's mission and scope |
| `03_PLAYBOOK.md` | Full `.dev-knowledge` PLAYBOOK.md — methodology |
| `04_ESSENTIALS.md` | Full `.dev-knowledge` ESSENTIALS.md — high-leverage cheat-sheet |
| `05_GOVERNANCE_ESSENCES.md` | 2-4 sentence essences for ADRs cited in directives |
| `06_STATE_OF_PLAY.md` | Current State per ADR-37 (REALITY + RATIONALE + verification) |
| `07_ACTION_PLAN.md` | Future State per ADR-37 (OBJECTIVE + DIRECTIVES + BOUNDARIES) |
| `08_TREE.txt` | `git ls-files` snapshot at Stage 3 |
| `09_EXECUTION_EVIDENCE.md` | Return-trip template — fill after execution |

Note: target = `.dev-knowledge` so `02b_ECOSYSTEM_VISION.md` is omitted
(would be a duplicate of `02_VISION.md`). Bundle = 11 files.

## Notes

- Stage 1 + Stage 2 inputs archived at
  `.dev-knowledge/docs/handoffs/archive/2026-05-17-dev-knowledge-session-sync/`
- If Q&A produces amendments they will appear in
  `archive/.../stage2-amendments.md`
- Per ADR-42 v3.3.3 HEAD validation uses an ancestor check, not strict
  equality
