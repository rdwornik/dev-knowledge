# Handoff Bundle — ai-council (session-sync)

**Slug:** `2026-05-17-ai-council-session-sync`  
**Generated:** 2026-05-17  
**Target repo:** `ai-council` — `C:\Users\1028120\Documents\Dev\ai-council`  
**Type:** session-sync

---

## Rob's Upload Instructions

### Step 1 — Open a NEW claude.ai chat for ai-council

Open a fresh browser chat. Do NOT use the old chat that provided the Stage 2 response — that chat's context is exhausted.

### Step 2 — Upload the bundle files

Upload all files from this folder to the new chat. The most reliable method is to drag-drop all files at once. Alternatively, select all and attach.

Files to upload (upload all of them):

| File | Purpose |
|---|---|
| `00_first-message.md` | Do NOT upload — paste as first message (Step 3) |
| `01_MANIFEST.md` | Entry point and file index |
| `01_manifest.json` | Machine-readable checksums |
| `02_VISION.md` | ai-council VISION |
| `02b_ECOSYSTEM_VISION.md` | .dev-knowledge ecosystem VISION |
| `03_PLAYBOOK.md` | Full methodology |
| `04_ESSENTIALS.md` | High-leverage rules |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences for this handoff |
| `06_STATE_OF_PLAY.md` | Current state + verified findings |
| `07_ACTION_PLAN.md` | Objective, directives, boundaries |
| `08_TREE.txt` | ai-council tracked file tree |
| `09_EXECUTION_EVIDENCE.md` | Return-trip template (new chat fills this) |

Upload **all 12 files above** (not `00_README.md`, not `00_first-message.md`).

### Step 3 — Paste `00_first-message.md` as the first message

Open `00_first-message.md` in a text editor. Copy the entire contents. Paste as the first message in the new chat (do not send a different opening message first).

### Step 4 — Confirm the synthesis

After the new chat presents its synthesis, read it carefully. Then type one of:
- `synthesis confirmed` — if the summary is accurate
- `synthesis correction: [specifics]` — if something is wrong or missing

### Step 5 — Q&A loop (if the new chat has questions)

If the new chat asks clarification questions before generating prompts, route them to the OLD ai-council chat (or to Rob directly if the old chat is closed). Return the answers. Up to 3 rounds.

### Step 6 — Choose prompt format

The new chat will ask: "single Claude Code prompt or split into separate prompts?" Answer based on how you want to run the work.

### Step 7 — Run the generated prompts in Claude Code

Open Claude Code in the ai-council repo directory and run the prompt(s) the new chat generates.

### Step 8 — Return `09_EXECUTION_EVIDENCE.md`

After execution, bring `09_EXECUTION_EVIDENCE.md` (filled out by the new chat or Claude Code) back to `.dev-knowledge` and commit it.

---

## File count verification

This folder should contain **13 files** (including this README):

```
00_README.md
00_first-message.md
01_MANIFEST.md
01_manifest.json
02_VISION.md
02b_ECOSYSTEM_VISION.md
03_PLAYBOOK.md
04_ESSENTIALS.md
05_GOVERNANCE_ESSENCES.md
06_STATE_OF_PLAY.md
07_ACTION_PLAN.md
08_TREE.txt
09_EXECUTION_EVIDENCE.md
```

If any file is missing, do not proceed — return to `.dev-knowledge` and run `"complete handoff for ai-council"` again.
