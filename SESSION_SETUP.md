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
- When evaluating new tools: is it mature (>100 stars, >v1.0)? Does it solve a real problem? If architecture-level → Council debate.

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

**Same process for both chat types.** Claude auto-adapts the content.

### When to handoff
<!-- scope: llm -->

- At ~2 hours of conversation
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
### YYYY-MM-DD | [source] | [one-line lesson] | [category] | [action taken]
```

Or ask Claude: "What were the key lessons from this chat? Format as LESSONS.md entries."

If nothing was learned — skip this step. Not every chat produces lessons.