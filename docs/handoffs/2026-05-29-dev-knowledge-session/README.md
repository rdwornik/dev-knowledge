# Handoff — 2026-05-29-dev-knowledge-session

**Repo:** .dev-knowledge (self-handoff)  ·  **Type:** session  ·  **Generated:** 2026-05-29
**Repo state at generation:** branch `docs/handoff-2026-05-29`, HEAD `367c81e` (main tip)

This bundle onboards a **new chat** to continue work on `.dev-knowledge`. It is a
teaching sequence, not a file dump: the new chat learns its role, our methodology,
the project, what just happened, and what to do now — then proves it understood
before touching anything.

Files `01`–`07` are the teaching sequence (paste them to the new chat). This
`README.md` is for you only — do not paste it.

## Paste sequence + escalation ladder

```
Step A: Paste 01_ROLE + 02_METHODOLOGY + 03_PROJECT + 04_RECENT + 05_NOW
        as ONE message into the new chat. Wait for acknowledgment.
Step B: Paste 06_QUESTIONS. Read the chat's answers.

IF comprehension FAILS:
  Tier 1 — Re-paste the specific file(s) the chat got wrong + "read again carefully".
  IF still fails:
  Tier 2 — Ask Claude Code to verify the specific facts against repo state;
           paste CC's findings to the new chat.
  IF still fails:
  Tier 3 — ABORT onboarding. Reactivate the sender chat, or do a manual context dump.

IF comprehension PASSES:
  Step C: Paste 07_ASK_BACK. Answer the chat's questions from memory or the sender chat.
  Step D: The chat begins work.
```

## Bundle contents

| File | Purpose | Budget |
|---|---|---|
| `01_ROLE.md` | Who the new chat is; who Rob is | ≤100 |
| `02_METHODOLOGY.md` | How we work (PLAYBOOK pointers + key extracts) | ≤200 |
| `03_PROJECT.md` | Vision + sacred files | ≤150 |
| `04_RECENT.md` | Narrative of recent work | ≤250 |
| `05_NOW.md` | Top P1s + in-progress branches | ≤100 |
| `06_QUESTIONS.md` | Comprehension check (5–7 Q) | ≤80 |
| `07_ASK_BACK.md` | New chat's question slot (max 3) | ≤50 |

## Generation notes

**No degradation** — all source files present (VISION, CLAUDE, PLAYBOOK, ESSENTIALS,
BACKLOG, JOURNAL); every `{{PULL}}`/`{{SYNTHESIZE}}`/`{{CONTEXT}}` marker resolved.

**Drift surfaced at Phase 2** (cross-check of sender answers vs repo state — full
detail in `04_RECENT.md` "Load-bearing facts"):

1. **Aborted handoff folder.** Sender said `docs/handoffs/aborted/…ABORTED/` is
   preserved, "do not delete." Repo fact: it was **deliberately deleted** (commit
   `987edac`) and is absent. The surviving record is the post-mortem audit
   `docs/audits/2026-05-29-handoff-v3.4-process-audit.md`. The bundle tells the new
   chat not to go looking for it.
2. **corp-monorepo P1-2 branch.** Sender relayed Rob's belief it may be merged
   (*"chyba ogarnięty"*). Repo fact (read-only per ADR-41): corp-monorepo is still
   **on** `chore/extract-p1-2-to-backlog-2026-05-28` (HEAD `a1007b1`), **unmerged** —
   confirms BACKLOG CM-1. Flagged as corp-monorepo's own session work.

Both are decision-relevant; neither blocks the handoff. Worth confirming with Rob.
