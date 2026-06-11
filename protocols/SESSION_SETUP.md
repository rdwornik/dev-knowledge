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
1. **ESSENTIALS.md** — your working standards and rules
2. **Relevant files** — presentation, article, document to analyze (if any)
3. **Handoff from previous chat** — paste the code block (if continuing a topic)

No CLAUDE.md needed — functional chats don't involve a specific repo.

First message:
```
[upload ESSENTIALS.md + any relevant files]

Potrzebuję pomocy z [topic].
[paste handoff here if continuing from a previous chat]
```

### Starting a Programming Chat
<!-- scope: llm -->

Upload with your first message:
1. **ESSENTIALS.md** — your working standards and rules
2. **CLAUDE.md from the repo** you're working on (e.g., `Dev/{project}/CLAUDE.md` or `Dev/.dev-knowledge/CLAUDE.md`) — gives Claude project context: architecture, commands, conventions, what NOT to do
3. **Handoff from previous chat** — paste the code block (if continuing)

First message:
```
[upload ESSENTIALS.md + CLAUDE.md from repo]

Kontynuuję pracę nad [project name].
Cel na dzisiaj: [1-2 objectives, max].
[paste handoff here if continuing from a previous chat]
```

PLAYBOOK.md is NOT needed here — ESSENTIALS covers daily work. Upload PLAYBOOK only when starting a new project from scratch or establishing a new process.

### Starting a New Project (from scratch)
<!-- scope: llm -->

Upload:
1. **ESSENTIALS.md**
2. **PLAYBOOK.md** (full file — Claude needs scaffolding template and prompt format)

First message:
```
[upload ESSENTIALS.md + PLAYBOOK.md]

Chcę zbudować [project name] — [3 sentences max what it does].
Pomóż mi:
1. Napisać CLAUDE.md dla tego projektu
2. Przygotować prompt scaffoldingowy do Claude Code
3. Zdecydować Model/Mode/Effort dla pierwszego prompta
```

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

> **Which handoff is this?** This is the **browser→browser** auto-handoff (`wygeneruj handoff`) for carrying context between web-chat sessions. It is a *different layer* from the "Handoff workflow trigger" section below, which is the HANDOFF_PROCESS v5 **Claude-Code** protocol. Two mechanisms, two layers — not competing instructions for the same act.

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
2. Open new chat → go back to Step 1 (upload ESSENTIALS.md, paste handoff)

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

> **Which handoff is this?** This is the HANDOFF_PROCESS v5 **Claude-Code** protocol — *distinct* from the browser→browser auto-handoff in Step 4 above.

When Rob says one of these phrases, follow HANDOFF_PROCESS **v5** per
`protocols/HANDOFF_PROCESS.md` (the single live source of truth for handoff
mechanics); the phrase triggers are stable across versions:

| Phrase | Effect |
|---|---|
| `please create handoff for {repo}` | Phase 1 — generate the interview |
| `complete handoff for {repo}` | Phase 2 — consolidate the bundle |

`{repo}` defaults to `.dev-knowledge` (self-handoff); naming another repo is a
cross-repo handoff.

**Two-phase flow (v4 mechanics — superseded; retained until the v5 residual/probe generator lands, per `HANDOFF_PROCESS.md` §11):**

1. **Phase 1 — Interview** (Claude Code): capture target repo HEAD SHA + branch +
   working-tree state; write `docs/handoffs/in-progress/{slug}/_handoff-interview.md`
   — one sage→apprentice cluster of 5 questions (Past / Present / Future / Wisdom /
   Warnings) plus a `=== PASTE ANSWERS BELOW THIS LINE ===` marker; append a JOURNAL
   marker; commit on the feature branch.
2. **Operator (between phases):** copy the questions into the SENDER browser chat
   (the chat being wrapped up — it holds the lived context), get narrative answers,
   paste them below the marker, save. Answers must come from the sender chat, not a
   fresh one — a new chat has no context to contribute.
3. **Phase 2 — Consolidate** (Claude Code): read the interview; cross-check the
   answers against actual repo state (drift → FLAG to operator); generate the flat
   bundle at `docs/handoffs/{slug}/` (README + `01_ROLE`…`07_ASK_BACK`) from source
   files; remove the `in-progress/{slug}/` folder; append a JOURNAL marker; commit.
   Then Rob opens a NEW (apprentice) chat with the bundle.

No Stage vocabulary, no placeholder dance, no separate claims/scope/probe files —
claims and scope become inline narrative in the generated bundle.

**State detection** (based on `in-progress/{slug}/` presence):

| State | Action |
|---|---|
| No `in-progress/{slug}/` folder | run Phase 1 |
| `_handoff-interview.md` present, no answers below the marker | awaiting operator paste |
| `_handoff-interview.md` with answers pasted | run Phase 2 |

---

## BACKLOG review at session start
<!-- scope: meta -->

When starting any new Claude Code session in `.dev-knowledge` (per ADR-41):

1. Read `.dev-knowledge/BACKLOG.md`
2. Note relevant items for current work
3. After session, append new items or update status via per-handoff grooming

When starting a browser-2 session that consumes a handoff:
- `05_NOW.md` references BACKLOG entry IDs for in-progress / deferred items
- Do NOT duplicate BACKLOG content into the session — cite the entry, don't copy it