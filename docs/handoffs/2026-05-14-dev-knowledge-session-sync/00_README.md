# Handoff Bundle — .dev-knowledge (session-sync)

<!-- scope: meta -->

**Date:** 2026-05-14
**Type:** session-sync
**Format version:** v3.3.1 (ADR-42 v3.0, amended through v3.2; Stage 1 template per v3.3.1)
**Target repo:** `.dev-knowledge`

The OLD browser chat for `.dev-knowledge` has served its purpose. Its accumulated knowledge is
preserved in this bundle. You can now close it.

**Stage 1 + Stage 2 inputs archived at:**
`.dev-knowledge/docs/handoffs/archive/2026-05-14-dev-knowledge-session-sync/`

---

## Operator workflow (10 steps)

1. Open a **NEW claude.ai chat** (fresh, zero prior context — NOT the old chat).
2. Drag-drop all **11 files** from this folder into the new chat, OR zip the folder and upload the zip.
3. Paste the full content of `00_first-message.md` as the **first message** in the new chat.
4. The new chat reads the bundle and writes its **articulation gate** (4 items in its own words). Read it carefully.
5. Type the exact phrase to proceed:
   - `role confirmed` → articulation is accurate; proceed to receiver synthesis
   - Or correct any misstatement before confirming
6. After `role confirmed`, the new chat presents a **receiver synthesis**. Confirm with:
   - `synthesis confirmed` → accurate; proceed to Q&A or prompt generation
   - `synthesis correction: [specifics]` → new chat updates and re-presents
7. **Q&A loop** (if new chat has clarification questions):
   - New chat presents up to 3 numbered questions
   - Route to OLD chat (Stage 2 source) if still available, get answers, return to new chat
   - Maximum 3 rounds; after round 3 the new chat proceeds with best available understanding
8. New chat asks: **"single Claude Code prompt or split?"**
   - Single: directive count is small, no verification gates between steps
   - Split: 5+ directives OR verification-critical gates between steps
9. New chat generates **Claude Code prompt(s) as downloadable `.md` files**. Download them.
10. Open Claude Code in `.dev-knowledge`. Paste and run prompts. Return the completed
    `09_EXECUTION_EVIDENCE.md` to `.dev-knowledge/docs/handoffs/2026-05-14-dev-knowledge-session-sync/`
    after work is done.

---

## File index (11 files)

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | Paste as first message in new chat |
| `01_MANIFEST.md` | Entry point, file index, HEAD pin, drift verification |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | Full `.dev-knowledge` VISION — ecosystem context |
| `03_PLAYBOOK.md` | Full `.dev-knowledge` PLAYBOOK — HOW we work |
| `04_ESSENTIALS.md` | Full `.dev-knowledge` ESSENTIALS — daily cheat sheet |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences relevant to this session's directives |
| `06_STATE_OF_PLAY.md` | Current state — what was completed, decisions locked |
| `07_ACTION_PLAN.md` | Action plan — goals, directives, boundaries |
| `08_TREE.txt` | `.dev-knowledge` file inventory at Stage 3 time |
| `09_EXECUTION_EVIDENCE.md` | Return trip — new chat fills this after executing directives |

---

## Notes

- This bundle implements ADR-42 v3.0 (amended through v3.2) + HANDOFF_PROCESS.md v3.3.1.
- Stage 1 + Stage 2 inputs archived at `.dev-knowledge/docs/handoffs/archive/2026-05-14-dev-knowledge-session-sync/`
- If the Q&A loop produces amendments, they are also archived at `archive/2026-05-14-dev-knowledge-session-sync/stage2-amendments.md` if applicable.
- The articulation gate in `00_first-message.md` is mandatory — do not skip even if it feels obvious. It is the v3.3 mechanism being measured for efficacy under v3.3.1 audience-aware Stage 2.
