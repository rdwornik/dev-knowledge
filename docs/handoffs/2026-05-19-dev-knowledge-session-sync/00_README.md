# Handoff Bundle — README

<!-- scope: meta -->

## What this folder is

- **Date:** 2026-05-19 (Stage 1) / Stage 3 finalized 2026-05-20
- **Target repo:** `.dev-knowledge` (self-handoff)
- **Type:** session-sync
- **Format:** ADR-42 v3 / HANDOFF_PROCESS v3.3.3
- **Slug:** `2026-05-19-dev-knowledge-session-sync`

This is a self-applied handoff (target = `.dev-knowledge`). 11 files,
flat layout, no subdirectories. `02b_ECOSYSTEM_VISION.md` is omitted —
`02_VISION.md` is already `.dev-knowledge`'s VISION.

The OLD `.dev-knowledge` browser chat that provided Stage 2 can now be
closed; its accumulated knowledge is preserved in `06_STATE_OF_PLAY.md`
and `07_ACTION_PLAN.md`.

Stage 1 + Stage 2 inputs are archived at:
`docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/`

## Operator workflow

1. Open a NEW claude.ai chat (fresh, zero context — NOT the OLD chat).
2. Drag-drop all 11 files from this folder, OR zip and upload zip.
3. Paste the content of `00_first-message.md` as the first message.
4. NEW chat reads bundle, performs the articulation gate (4 items), then
   presents receiver synthesis.
5. Confirm with exact phrase:
   - `role confirmed` (after articulation gate)
   - `synthesis confirmed` (after synthesis) — proceeds to Q&A or
     prompt generation
   - `synthesis correction: [text]` — NEW chat updates, re-presents
6. Q&A loop (if NEW chat asks clarification questions):
   - Max 3 questions per round, max 3 rounds
   - Carry questions to OLD chat (Stage 2 source) and return answers
7. NEW chat asks "single Claude Code prompt or split?" — answer based on
   directive complexity (5+ directives or verification-critical gate →
   split).
8. NEW chat generates Claude Code prompt(s) as downloadable .md files.
   Download them.
9. Open Claude Code in `.dev-knowledge` (target = this same repo). Paste
   prompts sequentially. Claude Code executes.
10. Return the completed `09_EXECUTION_EVIDENCE.md` to
    `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` (commit after
    Stage 3 archive).

## File index

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | First message for the NEW chat (copy-paste) |
| `01_MANIFEST.md` | Entry point, file index, drift verification, HEAD pin |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | `.dev-knowledge` VISION.md — target repo's mission and scope |
| `03_PLAYBOOK.md` | Full `.dev-knowledge` PLAYBOOK.md — methodology |
| `04_ESSENTIALS.md` | Full `.dev-knowledge` ESSENTIALS.md — high-leverage rules |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences for ADRs cited in directives (ADR-51, ADR-54) |
| `06_STATE_OF_PLAY.md` | Current state — what was completed, REALITY + RATIONALE from Stage 2 |
| `07_ACTION_PLAN.md` | Future state — OBJECTIVE + DIRECTIVES + BOUNDARIES from Stage 2 |
| `08_TREE.txt` | `git ls-files` snapshot of `.dev-knowledge` at Stage 3 |
| `09_EXECUTION_EVIDENCE.md` | Return-trip template — fill after work completes |

## Notes

- This bundle follows ADR-42 v3 / HANDOFF_PROCESS v3.3.3.
- Stage 1 + Stage 2 inputs are archived at
  `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/`.
- If a Q&A round produces amendments, they are also archived as
  `archive/<slug>/stage2-amendments.md`.
- HEAD validation uses an ancestor check, not strict equality
  (HANDOFF_PROCESS v3.3.3): current HEAD must be a descendant of the
  Stage 1 SHA pinned in `01_MANIFEST.md`.
