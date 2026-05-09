# Handoff: ai-council audit-sync

**Type:** audit-sync
**Date:** 2026-04-30 (audit date) / regenerated 2026-05-09 (v3.0 format)
**Target repo:** ai-council
**Format:** v3.0 (ADR-42)

> Note: Stage 2 was implicit for this audit-sync handoff. Audit findings
> (Faza A2) substituted for browser-2 architect response. No
> `01_question_for_browser.md` was generated for this handoff.

---

## How to use this handoff

1. Open a **new browser chat** (Claude.ai)
2. Upload **all files in this folder** (drag the whole folder, or upload individually)
3. Paste the contents of `00_first-message.md` as your **first message**
4. Browser-2 will verify HEAD SHA, provide receiver synthesis, then execute directives

---

## What's in this folder

| File | Purpose |
|---|---|
| `00_README.md` | These instructions (you are here) |
| `00_first-message.md` | Paste verbatim as browser-2 first message |
| `01_MANIFEST.md` | Entry point: metadata, file index, HEAD pin, receiver synthesis |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | Full .dev-knowledge VISION — ecosystem context |
| `03_PLAYBOOK.md` | Full .dev-knowledge PLAYBOOK — HOW we work |
| `04_ESSENTIALS.md` | Full .dev-knowledge ESSENTIALS — daily cheat sheet |
| `05_GOVERNANCE_ESSENCES.md` | ADR-33 and ADR-35 essences (drive F-01, F-02) |
| `06_STATE_OF_PLAY.md` | Current state: audit findings, decisions locked, deferred |
| `07_ACTION_PLAN.md` | Goals, directives (F-01, F-02), boundaries |
| `08_TREE.txt` | ai-council file inventory at audit HEAD |
| `09_EXECUTION_EVIDENCE.md` | Return trip: fill after completing work |

---

## What this handoff is for

Apply Phase 1 governance to ai-council:
- **F-01:** Create `ai-council/VISION.md` per ADR-33 mandate
- **F-02:** Update `ai-council/CLAUDE.md` to reference DEV_KNOWLEDGE_PATH per ADR-35

Two P1 audit findings, tier-independent, actionable now.

---

## After completing work

Fill `09_EXECUTION_EVIDENCE.md` with:
- Commands run (with stdout)
- Test results
- git diffs
- Final HEAD SHA

This closes the return trip for the next `.dev-knowledge` session.
