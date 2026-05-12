# 00_README.md — Operator Instructions

Handoff: 2026-05-09-dev-knowledge-session-sync
Type: session-sync (self-handoff — .dev-knowledge to .dev-knowledge)
Format version: v3.2 (ADR-42, amended three times 2026-05-09)
Generated: 2026-05-09 (night)

The OLD .dev-knowledge browser chat that produced the Stage 2 response
can now be closed — its accumulated knowledge is preserved in this bundle.

Stage 1+2 inputs archived at:
`.dev-knowledge/docs/handoffs/archive/2026-05-09-dev-knowledge-session-sync/`

---

## Operator workflow (10 steps)

1. **Open a NEW claude.ai chat** (fresh, zero context — NOT the OLD chat that
   answered the Stage 2 questions).

2. **Upload all 12 files** from this folder (drag-drop, or zip the folder and
   upload the zip).

3. **Paste `00_first-message.md`** as the first message in the NEW chat.

4. **NEW chat reads the bundle** and presents its receiver synthesis — a
   paraphrase of the goal, current state, reasoning, directive sequence, and
   boundaries it understood from the bundle.

5. **Confirm or correct the synthesis.** Type one of these exact phrases:
   - `synthesis confirmed` — synthesis is accurate; NEW chat proceeds
   - `synthesis correction: [specifics]` — NEW chat updates and re-presents

6. **Q&A loop (if NEW chat has clarification questions):**
   - NEW chat presents up to 3 questions per round
   - Take questions to the OLD chat (Stage 2 source) and get answers
   - Return answers to NEW chat
   - Repeat up to 3 rounds total
   - After round 3 OR when NEW chat says "no more questions": proceed

7. **NEW chat asks: "single Claude Code prompt or split?"** Answer based on
   directive complexity:
   - Single prompt: small directive count, no verification gates between steps
   - Split: 5+ directives OR verification-critical gates

8. **NEW chat generates Claude Code prompt(s)** as downloadable `.md` file(s).
   Download them.

9. **Open Claude Code in `.dev-knowledge`** (NOT in another repo). Paste the
   prompt(s) sequentially. Claude Code executes the directives.

10. **Return `09_EXECUTION_EVIDENCE.md`** to `.dev-knowledge` for next session
    review. Commit it to `.dev-knowledge/docs/handoffs/2026-05-09-dev-knowledge-session-sync/`
    after Stage 3 archive.

---

## File index

| # | File | Purpose |
|---|---|---|
| 1 | `00_README.md` | This file — operator instructions |
| 2 | `00_first-message.md` | Paste as first message in NEW chat |
| 3 | `01_MANIFEST.md` | Entry point, metadata, state validation |
| 4 | `01_manifest.json` | Machine-readable checksums |
| 5 | `02_VISION.md` | Full .dev-knowledge VISION (ecosystem context) |
| 6 | `03_PLAYBOOK.md` | Full .dev-knowledge PLAYBOOK (methodology) |
| 7 | `04_ESSENTIALS.md` | Full .dev-knowledge ESSENTIALS (cheat-sheet) |
| 8 | `05_GOVERNANCE_ESSENCES.md` | ADR essences for active directives |
| 9 | `06_STATE_OF_PLAY.md` | Current state, decisions, verification |
| 10 | `07_ACTION_PLAN.md` | Goal, directives, boundaries |
| 11 | `08_TREE.txt` | .dev-knowledge file inventory |
| 12 | `09_EXECUTION_EVIDENCE.md` | Return-trip template (fill after work) |

---

## Notes

- This bundle is the Stage 3 handoff per ADR-42 v3.2
- Stage 1+2 inputs: `.dev-knowledge/docs/handoffs/archive/2026-05-09-dev-knowledge-session-sync/`
- Q&A loop amendments (if any): `archive/2026-05-09-dev-knowledge-session-sync/stage2-amendments.md`
- Drift between Stage 1 SHA and Stage 3 HEAD is documented in `01_MANIFEST.md`
  (intentional — 4 commits of intra-session methodology updates)
