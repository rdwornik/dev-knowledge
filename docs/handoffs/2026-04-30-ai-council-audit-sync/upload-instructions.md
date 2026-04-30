# Upload instructions (for Rob)

This handoff folder is the audit cycle output for ai-council. To use:

1. Open a new claude.ai chat dedicated to ai-council (browser-2 session).
2. Upload the entire `contents/` folder OR the zipped folder. Order
   doesn't matter — browser-2 will read all files.
3. Copy-paste the contents of `first-message.md` as the FIRST message
   in that chat.
4. Browser-2 will validate Current State, then execute Future State
   actions (F-01 VISION.md creation, F-02 lessons configuration).
5. Browser-2 will report completion. Return to .dev-knowledge session
   for evaluation:
   - Did browser-2 verify HEAD SHA + working tree?
   - Did browser-2 act only on tier-independent F-01/F-02?
   - Did browser-2 honor DEFER list (no BACKLOG.md, no ARCHITECTURE.md)?
   - Did browser-2 use formal Claude Code prompts where appropriate?
   - Did browser-2 use ADR references (ADR-33, ADR-35) substantively?

This evaluation is the test of Phase 1 governance end-to-end.

## What's in this folder

- `upload-instructions.md` (this file) — for you, Rob
- `first-message.md` — copy-paste content for browser-2's first message
- `contents/` — the actual handoff payload (browser-2 reads all of this)
  - `HANDOFF.md` — main handoff document with Current/Future State + Detailed Context
  - `manifest.json` — machine-readable summary (HEAD SHA, findings list, etc.)
  - `audit-report.md` — full Faza A2 findings report
  - `tree.txt` — ai-council file inventory at handoff generation
  - `relevant-decisions/` — full text of 7 relevant ADRs
