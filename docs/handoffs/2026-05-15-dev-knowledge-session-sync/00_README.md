# Handoff Bundle — .dev-knowledge (session-sync)

<!-- scope: meta -->

**Date:** 2026-05-15
**Type:** session-sync
**Target repo:** .dev-knowledge
**Format version:** v3.3.2 (ADR-42 three-stage flow)

The OLD browser chat for .dev-knowledge has been wrapped up. Its accumulated
knowledge is preserved in `06_STATE_OF_PLAY.md` (current state) and
`07_ACTION_PLAN.md` (next session directives). The OLD chat can be closed.

Stage 1+2 inputs archived at:
`.dev-knowledge/docs/handoffs/archive/2026-05-15-dev-knowledge-session-sync/`

---

## Operator workflow (10 steps)

1. Open a **NEW** claude.ai chat (fresh, zero context — NOT the OLD chat)
2. Drag-drop all 11 files from this folder, OR zip and upload zip
3. Paste content of `00_first-message.md` as first message
4. NEW chat reads bundle, writes the four-item articulation gate
5. Operator confirms articulation: type exact phrase `role confirmed`
6. NEW chat presents receiver synthesis
7. Confirm synthesis. Type exact phrase:
   - `synthesis confirmed` — proceeds to Q&A or prompt generation
   - `synthesis correction: [specifics]` — NEW chat updates, re-presents
8. Q&A loop (if NEW chat asks clarification questions):
   - NEW chat presents up to 3 questions
   - Take questions to OLD chat (Stage 2 source — the chat being wrapped up)
   - Get answers from OLD chat; paste back to NEW chat
   - Repeat up to 3 rounds total
   - After round 3 OR when NEW chat says "no more questions": proceed
9. NEW chat asks: "single Claude Code prompt or split?"
   - Single prompt: directive count is small, no verification gates
   - Split: 5+ directives OR verification-critical gate
   NEW chat generates Claude Code prompt(s) as downloadable .md files.
   Download them.
10. Open Claude Code in **.dev-knowledge** repo.
    Paste prompts sequentially. Claude Code executes.
    Return the filled `09_EXECUTION_EVIDENCE.md` to `.dev-knowledge` when done.

---

## File index (11 files)

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | Copy-paste first message for NEW chat |
| `01_MANIFEST.md` | Entry point, file index, HEAD SHA pin |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | Full .dev-knowledge VISION.md — target repo's mission |
| `03_PLAYBOOK.md` | Full .dev-knowledge PLAYBOOK.md (methodology) |
| `04_ESSENTIALS.md` | Full .dev-knowledge ESSENTIALS.md (high-leverage rules) |
| `05_GOVERNANCE_ESSENCES.md` | ADR operational essences for directives |
| `06_STATE_OF_PLAY.md` | What was done; current state; architect rationale |
| `07_ACTION_PLAN.md` | Next session goal, directives, boundaries |
| `08_TREE.txt` | .dev-knowledge file inventory (`git ls-files`) |
| `09_EXECUTION_EVIDENCE.md` | Return trip template — NEW chat fills post-work |

---

## Notes

- This bundle implements ADR-42 v3.3.2 (three-stage flow)
- Self-applied handoff (target = .dev-knowledge): no `02b_ECOSYSTEM_VISION.md`
- Stage 1 + Stage 2 inputs archived at
  `.dev-knowledge/docs/handoffs/archive/2026-05-15-dev-knowledge-session-sync/`
