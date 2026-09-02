---
last_reviewed: 2026-09-01
status: active
owner: Rob
reconciled_with: handoff-process@7.0.0
---

# Session Setup

> Browser chat workflow. 5 chronological steps.

---

## Step 1: Know Which Chat You're Starting
<!-- scope: llm -->

Every browser chat falls into one of two types:

**Functional chat** — you're solving a problem that doesn't involve code. Creating a presentation, analyzing an article, evaluating a tool, planning strategy, preparing for a meeting, writing a document.

**Programming chat** — you're building or changing software. Creating prompts for Claude Code, reviewing session logs, debugging architecture, preparing Council debates, designing systems.

If you're not sure: if Claude Code or a code repo is involved, it's programming. Everything else is functional.

---

## Step 2: Start the Chat
<!-- scope: llm -->

### Starting a Functional Chat
<!-- scope: llm -->

Upload with your first message:
1. **Relevant files** — presentation, article, document to analyze (if any)
2. **Handoff from previous chat** — paste the code block (if continuing a topic)

No CLAUDE.md needed — functional chats don't involve a specific repo.

First message:
```
[upload any relevant files]

Potrzebuję pomocy z [topic].
[paste handoff here if continuing from a previous chat]
```

### Starting a Programming Chat
<!-- scope: llm -->

Upload with your first message:
1. **CLAUDE.md from the repo** you're working on (e.g., `Dev/{project}/CLAUDE.md` or `Dev/.dev-knowledge/CLAUDE.md`) — gives Claude project context: architecture, commands, conventions, what NOT to do
2. **Handoff from previous chat** — paste the code block (if continuing)

First message:
```
[upload CLAUDE.md from repo]

Kontynuuję pracę nad [project name].
Cel na dzisiaj: [1-2 objectives, max].
[paste handoff here if continuing from a previous chat]
```

PLAYBOOK.md is NOT needed here — CLAUDE.md covers daily work for this repo. Upload PLAYBOOK only when starting a new project from scratch or establishing a new process.

### Starting a New Project (from scratch)
<!-- scope: llm -->

Upload:
1. **PLAYBOOK.md** (full file — Claude needs scaffolding template and prompt format)

First message:
```
[upload PLAYBOOK.md]

Chcę zbudować [project name] — [3 sentences max what it does].
Pomóż mi:
1. Napisać CLAUDE.md dla tego projektu
2. Przygotować prompt scaffoldingowy do Claude Code
3. Zdecydować Model/Mode/Effort dla pierwszego prompta
```

---

### The browser role file lives in the project, installed once (pointer)
<!-- scope: llm -->

The architect seat's operating role is `protocols/HANDOFF_BOOT.md`, installed **once** as the
browser project's own instructions rather than pasted into every session. This file is the third
home of that arrangement and carries the **pointer only** — the mechanics stay where they already
live, so three sites cannot drift into three versions:

- **Mechanics** (the one-time install, the ROLE PIN's three lines, what a version refusal means and
  what the operator does about it) → `protocols/OPERATOR-INTERFACE.md` §5.
- **Mechanism** (the requirement that the role reaches the browser, and what satisfies it) →
  `protocols/HANDOFF_PROCESS.md`, §"Browser-role delivery".
- **Which project** → the single fleet-wide claude.ai Project *"Dev — Architect Seat"*, recorded as
  landed state in `OPERATOR-INTERFACE.md` §6.

Recorded here because a browser chat is started from this file, so the role install is a
precondition of Step 2 rather than a detail of the handoff that follows it. Operator ruling
2026-08-28 (B2): the third home is this file, in place of a new `PLAYBOOK.md` heading.

---

## Step 3: Work in the Chat
<!-- scope: hybrid -->

### In functional chats, Claude.ai:
<!-- scope: hybrid -->
- Thinks critically — challenges assumptions, identifies risks
- Provides structured analysis, not generic advice
- Extracts actionable items, not theory
- Says "nie" when an idea doesn't make sense

### In programming chats, Claude.ai:
<!-- scope: hybrid -->
- Writes prompts for Claude Code (always with Model/Mode/Effort table)
- Tells you when to `/clear` between prompts
- Challenges your approach — pushes back when something conflicts with decisions or gotchas
- Does NOT generate filesystem commands from memory — always "ask Claude Code to check first"

### In both types:
<!-- scope: hybrid -->
- Max 2 objectives per session. Everything else is backlog.
- When evaluating new tools: is it mature (>100 stars, >v1.0 — heuristics for community validation + production stability)? Does it solve a real problem? If architecture-level → Council debate.

### Decision routing (programming chats):
<!-- scope: hybrid -->

| Size                   | Where                              |
| ---------------------- | ---------------------------------- |
| 1 file, obvious fix    | Conversational in Claude Code      |
| 2-3 files              | Claude.ai → prompt for Claude Code |
| 3+ files / 2+ packages | Formal prompt with summary table   |
| Architecture           | AI Council debate first            |

---

## Step 4: Handoff — When the Chat Gets Heavy
<!-- scope: llm -->

> **Which handoff is this?** This is the **browser→browser** auto-handoff (`wygeneruj handoff`) for carrying context between web-chat sessions. It is a *different layer* from the "Handoff workflow trigger" section below, which is the HANDOFF_PROCESS v6 **Claude-Code** protocol. Two mechanisms, two layers — not competing instructions for the same act.

**Same process for both chat types.** Claude auto-adapts the content.

### When to handoff
<!-- scope: llm -->

- At ~2 hours of conversation (buffer before 3h decision-fatigue threshold per PLAYBOOK Section 4)
- When the chat starts getting slow
- When you're switching to a different topic
- Don't wait until context is dead — checkpoint while Claude still remembers

### How to handoff
<!-- scope: llm -->

Type: `wygeneruj handoff`

Claude generates a summary in a code block (<100 lines). You don't choose format, sections, or detail level — Claude decides based on the chat content.

### Transfer to new chat
<!-- scope: llm -->

1. Click "Copy" on the code block
2. Open new chat → go back to Step 1 (paste handoff)

### What the handoff contains
<!-- scope: llm -->

Claude includes what's relevant (you don't pick):
- Objective (one sentence)
- Current status
- Decisions made (with reversals: "X → Y because Z")
- Open tasks
- Files / artifacts created
- Key context (max 5 bullets)
- Programming chats add: prompts prepared, repo state
- Functional chats add: conclusions, references discussed

### Handoff rules
<!-- scope: llm -->

- Always in English, always in a single code block
- If Claude can't see early context: writes `[CONTEXT LOST]` instead of guessing
- No archiving step — Generate → Copy → Paste. That's it.

---

## Step 5: Extract Lessons (optional but valuable)
<!-- scope: llm -->

Before closing, ask yourself: "What 2-3 things did I learn?"

Append to `Dev/.dev-knowledge/LESSONS.md`:
```
### YYYY-MM-DD | [source] | [one-line lesson] | [category] | [scope: X] | [action taken]
```

Or ask Claude: "What were the key lessons from this chat? Format as LESSONS.md entries."

If nothing was learned — skip this step. Not every chat produces lessons.

---

## Handoff workflow trigger
<!-- scope: hybrid -->

> **Which handoff is this?** This is the HANDOFF_PROCESS v6 **Claude-Code** protocol — *distinct* from the browser→browser auto-handoff in Step 4 above.

When Rob says one of these phrases, follow HANDOFF_PROCESS **v6.3.0** per
`protocols/HANDOFF_PROCESS.md` (the single live source of truth for handoff
mechanics); the phrase triggers are stable across versions:

| Phrase | Effect |
|---|---|
| `please create handoff for {repo}` | Phase 1 — generate the interview |
| `complete handoff for {repo}` | Phase 2 — consolidate the bundle |

`{repo}` defaults to `.dev-knowledge` (self-handoff); naming another repo is a
cross-repo handoff.

**Mechanics live in `protocols/HANDOFF_PROCESS.md` (v6.3.0 — the single source of truth).** It owns the two-phase flow (interview → consolidate), the `in-progress/{slug}/` state detection, and the generated bundle shape. Not restated here so this file can't drift from it; the trigger phrases above are the only handoff detail that lives in SESSION_SETUP.

---

## BACKLOG review at session start
<!-- scope: meta -->

When starting any new Claude Code session in `.dev-knowledge` (per ADR-41):

1. Read `.dev-knowledge/BACKLOG.md`
2. Note relevant items for current work
3. After session, file new items (a `tasks/` add on the hub, since `BACKLOG.md` is generated there) or close via the Tier-1 closure loop — per-handoff grooming (PLAYBOOK §10). Done items **leave** the queue: there is no `done` marker to set in it (ADR-65); a hub retirement instead sets a terminal `status:` on the retained `tasks/` record

When starting a browser-2 session that consumes a handoff:
- The v6/v7 bundle's `HANDOFF_BOOT.md` / `RESIDUAL.md` reference BACKLOG entry IDs for in-progress / deferred items (the v4-era `05_NOW.md` is gone; `HANDOFF_PROCESS.md` §"Task-state re-narrated in `05_NOW`" keeps it only as a named anti-pattern — the fix is a pointer to BACKLOG plus drift-flags)
- Do NOT duplicate BACKLOG content into the session — cite the entry, don't copy it