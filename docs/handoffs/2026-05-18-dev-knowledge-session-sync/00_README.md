# Handoff Bundle: .dev-knowledge (session-sync)

**Date:** 2026-05-18
**Type:** session-sync
**Target repo:** `.dev-knowledge`
**Format version:** v3.0
**Files in this bundle:** 11

The OLD browser chat for `.dev-knowledge` has been wrapped up. Its accumulated
knowledge has been distilled into this bundle. You may close the OLD chat —
everything it knew is captured in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

Stage 1 + Stage 2 inputs are archived at:
`.dev-knowledge/docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/`

---

## Operator workflow

1. Open a NEW claude.ai chat (fresh, zero context — NOT the OLD chat).
2. Drag-drop all 11 files from this folder into the new chat, OR zip the folder
   and upload the zip.
3. Paste the full content of `00_first-message.md` as the first message.
4. The NEW chat reads the bundle and writes its articulation (4 items in its
   own words). Wait.
5. After the articulation appears, type **`role confirmed`** to proceed.
6. The NEW chat presents receiver synthesis. Respond with:
   - **`synthesis confirmed`** → NEW chat proceeds to Q&A or prompt generation.
   - **`synthesis correction: [specifics]`** → NEW chat updates and re-presents.
7. Q&A loop (if NEW chat has clarification questions):
   - NEW chat presents up to 3 questions per round.
   - Take questions to OLD chat (it is still accessible even if "closed").
   - Return answers to NEW chat.
   - Maximum 3 rounds; after round 3 NEW chat proceeds with best understanding
     or asks operator to restart Stage 2.
8. NEW chat asks: **"single Claude Code prompt or split?"**
   - Single: small directive count, no verification gates between steps.
   - Split: 3+ directives OR a verification gate separates them.
9. NEW chat generates Claude Code prompt(s) as downloadable `.md` file(s).
   Download them.
10. Open Claude Code in `.dev-knowledge` (for governance work) or the target
    child repo (if directives write to one). Paste prompts sequentially.
    After execution, return the filled-in `09_EXECUTION_EVIDENCE.md` to
    `.dev-knowledge/docs/handoffs/2026-05-18-dev-knowledge-session-sync/`.

---

## File index

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions and workflow |
| `00_first-message.md` | First message to paste into NEW chat |
| `01_MANIFEST.md` | Metadata, file index, drift verification |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | `.dev-knowledge` VISION.md — target repo's mission and scope |
| `03_PLAYBOOK.md` | `.dev-knowledge` PLAYBOOK.md — full methodology reference |
| `04_ESSENTIALS.md` | `.dev-knowledge` ESSENTIALS.md — high-leverage cheat sheet |
| `05_GOVERNANCE_ESSENCES.md` | Operational ADR essences for this session's actions |
| `06_STATE_OF_PLAY.md` | Current project state (completed work, deferred items) |
| `07_ACTION_PLAN.md` | Next session goal, action plan, constraints |
| `08_TREE.txt` | `git ls-files` snapshot for structural orientation |
| `09_EXECUTION_EVIDENCE.md` | Return-trip evidence form (fill after execution) |

---

## Notes

- This bundle is the Stage 3 handoff per ADR-42 v3.2.
- Stage 1 + Stage 2 inputs archived at
  `.dev-knowledge/docs/handoffs/archive/2026-05-18-dev-knowledge-session-sync/`.
- If the Q&A loop produces amendments, they are also recorded in
  `archive/2026-05-18-dev-knowledge-session-sync/stage2-amendments.md`.
