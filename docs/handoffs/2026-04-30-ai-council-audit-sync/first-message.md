# First message for browser-2 (ai-council session)

Copy-paste the following as the first message in your new claude.ai
chat for ai-council:

---

I am the browser session for ai-council. I am receiving an audit
handoff from .dev-knowledge generated 2026-04-30.

This is an AUDIT HANDOFF with STRONG enforcement (per ADR-37). I MUST:

1. Read all files in this handoff folder before taking any action:
   - `contents/HANDOFF.md` (main handoff document)
   - `contents/manifest.json` (machine-readable summary)
   - `contents/audit-report.md` (full findings)
   - `contents/tree.txt` (ai-council file inventory at handoff time)
   - All files in `contents/relevant-decisions/` (ADR full texts)

2. VALIDATE Current State before acting:
   - In ai-council repo, run `git rev-parse HEAD` and verify it matches
     manifest.json `target_repo.verified_head_sha`
     (`c821157fcfa957bc6612c74667d70c8c9a88ef5c`)
   - Run `git status --porcelain` and verify working tree is clean
   - If either check fails, STOP and report drift — do NOT proceed
     with actions

3. Execute Future State actions in priority order:
   - Action 1 (F-01): Create ai-council VISION.md per ADR-33
   - Action 2 (F-02): Update CLAUDE.md to reference DEV_KNOWLEDGE_PATH
     per ADR-35
   - Honor DEFER list: do NOT create BACKLOG.md or ARCHITECTURE.md
     yet (tier-dependent, calibration pending)

4. Use formal Claude Code prompts where appropriate:
   - Per .dev-knowledge prompt format (Model/Mode/Effort table →
     Title/Repo/Purpose → Read first → Git workflow → UNDERSTAND →
     Steps with COMMIT markers → Final → What NOT to do)
   - Single feature branch per action; incremental commits

5. After completing F-01 and F-02:
   - Verify pytest passes (310/310 baseline)
   - Update ai-council CHANGELOG.md, JOURNAL.md
   - Report completion to Rob

I will start by reading the handoff folder and validating Current State.

---
