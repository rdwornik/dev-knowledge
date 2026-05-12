# README — 2026-05-12-ai-council-session-sync

<!-- scope: meta -->

## What this folder is

Stage 3 handoff bundle for **ai-council**, generated 2026-05-12.
Type: session-sync. Format: ADR-42 v3.2 (12-file flat structure).

The OLD browser chat for ai-council (Stage 2 source) can now be **closed** — its
accumulated knowledge is preserved in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

Stage 1 + Stage 2 inputs archived at:
`.dev-knowledge/docs/handoffs/archive/2026-05-12-ai-council-session-sync/`

---

## Operator workflow (10 steps)

1. Open a **NEW** claude.ai chat (fresh, zero context — NOT the old ai-council chat)
2. Drag-drop all 12 files from this folder into the upload area, OR zip and upload
3. Paste the content of `00_first-message.md` as the first message
4. NEW chat reads the bundle and presents a **receiver synthesis** (its understanding
   of state, goals, and plan)
5. Confirm the synthesis with one of these exact phrases:
   - `synthesis confirmed` → NEW chat proceeds to Q&A or prompt generation
   - `synthesis correction: [specifics]` → NEW chat updates and re-presents
6. **Q&A loop** (if NEW chat has clarification questions before generating prompts):
   - NEW chat presents up to 3 questions
   - Take questions to the OLD chat (the one being closed)
   - Get answers from OLD chat, paste back to NEW chat
   - Maximum 3 rounds; after round 3 or "no more questions" → proceed
7. NEW chat asks: "single Claude Code prompt or split?"
   - Single: few directives, no verification gates between them
   - Split: 5+ directives OR gates where Claude Code output informs next step
8. NEW chat generates Claude Code prompt(s) as downloadable `.md` files — download them
9. Open Claude Code in **ai-council repo** (NOT in .dev-knowledge). Paste prompts
   sequentially and execute
10. After execution, return the filled `09_EXECUTION_EVIDENCE.md` to
    `.dev-knowledge/docs/handoffs/2026-05-12-ai-council-session-sync/` for next
    session reference

---

## File index (12 files)

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | Copy-paste first message for NEW chat |
| `01_MANIFEST.md` | Entry point, file index, HEAD pin |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | Ecosystem context (full VISION.md copy) |
| `03_PLAYBOOK.md` | Methodology reference (full PLAYBOOK.md copy) |
| `04_ESSENTIALS.md` | Daily cheat sheet (full ESSENTIALS.md copy) |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences for ADR-01, ADR-28, ADR-34 |
| `06_STATE_OF_PLAY.md` | What was done, rationale, deferred items |
| `07_ACTION_PLAN.md` | Goals, directives, boundaries — operational center |
| `08_TREE.txt` | ai-council file inventory snapshot |
| `09_EXECUTION_EVIDENCE.md` | Return trip template — fill after work |

---

## Notes

- This bundle is Stage 3 per ADR-42 v3.2
- Stage 1 + Stage 2 inputs: `.dev-knowledge/docs/handoffs/archive/2026-05-12-ai-council-session-sync/`
- Q&A loop amendments (if any): same archive location as `stage2-amendments.md`
- HEAD at Stage 3: `f094d0821a279f3aa36de554943c1b44576d0924` — verify before acting
