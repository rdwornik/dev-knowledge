# Handoff Bundle — ai-council
## Session Sync | 2026-05-18

**Slug:** 2026-05-18-ai-council-session-sync
**Repo:** ai-council (`C:\Users\1028120\Documents\Dev\ai-council`)
**Type:** session-sync
**HEAD at capture:** ce885827aada41f582e784fa210f73ff125a18de
**Branch:** main

---

## How to Start the New Chat

1. Open a **new** claude.ai chat.
2. Upload all 12 files from this folder as attachments.
3. Copy the full contents of `00_first-message.md`.
4. Paste it as your **first message** in the new chat (do not type anything else first).
5. Wait for the model to reply with **"role confirmed"** before proceeding.
6. The model will then produce a receiver synthesis. Review it.
7. Reply **"synthesis confirmed"** when satisfied, or correct any misunderstandings.
8. Once synthesis is confirmed, you may proceed with the session normally.

---

## Bundle Contents (12 files)

| File | Purpose |
|------|---------|
| `00_README.md` | This file — start here. Upload instructions and index. |
| `00_first-message.md` | First message to paste into new chat — articulation gate + startup protocol. |
| `01_manifest.json` | File checksums and bundle metadata. |
| `02_VISION.md` | ai-council's VISION.md — project mission, scope, and mode system. |
| `02b_ECOSYSTEM_VISION.md` | .dev-knowledge ecosystem VISION.md — universal context for all repos. |
| `03_PLAYBOOK.md` | Full methodology reference — process, commit conventions, conversation style. |
| `04_ESSENTIALS.md` | Daily cheat sheet — roles, session procedures, key shortcuts. |
| `05_GOVERNANCE_ESSENCES.md` | Operational essences for ADR-38 (repo architecture) and ADR-46 (dated entries, demoted). |
| `06_STATE_OF_PLAY.md` | Current state snapshot including 2 Stage 3 verification failures (flags for new session). |
| `07_ACTION_PLAN.md` | Revised directives, hard constraints, success criteria. |
| `08_TREE.txt` | Full `git ls-files` output for ai-council at capture HEAD (110 files). |
| `09_EXECUTION_EVIDENCE.md` | Test counts, validator notes, HEAD drift verification. |

---

## Critical Flags for New Session

Two architect claims from the stage2 response were **NOT verified** by Stage 3.
The action plan in `07_ACTION_PLAN.md` has been revised accordingly, but read
`06_STATE_OF_PLAY.md` → "Stage 3 Verification Summary" before starting work:

1. **Directive #1 revised**: AGENTS.md already exists (last updated 2026-05-17).
   The create task is obsolete — the new session should do a *currency review*, not
   a creation task.

2. **Directive #3 verification revised**: The ADR-46 `check_dated_entries_format`
   audit check was withdrawn per Council Simplification 2026-05-16. Verification of
   the scope-tag backfill is by visual inspection only — there is no automated gate.

---

## Quick Reference

- **Unit tests:** `pytest tests/ -m "not integration and not envcheck" -v` (413 tests)
- **Pre-commit:** `pre-commit run --all-files`
- **Hyphen check:** see `scripts/check.ps1` or CLAUDE.md
- **Working tree:** clean at capture
- **Anthropic credits:** Unknown — verify before attempting debate mode
