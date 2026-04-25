# Handoff Process
<!-- version: 1.0 — 2026-04-25 (Vibe Code 4 protocol patch) -->

A handoff transfers context from one Claude chat to the next.
Goal: preserve momentum across session boundaries without losing thread.

---

## Handoff trigger
<!-- scope: meta -->

Handoffs are **explicitly triggered by Rob**, never proactive from Claude.

**Triggers:**
- Rob says `wygeneruj handoff` (Polish trigger phrase) or "generate handoff" (English)
- Rob runs `/session-summary` slash command in Claude Code
- Session boundary clearly reached: scope completed, decision fatigue (>3h + >3 decisions), or Rob signals end

**Anti-pattern (Vibe Code 4 protocol):**
Browser chat must NOT proactively suggest "let's wrap up" or "this is a good stopping point."
Claude generates a handoff only when Rob explicitly asks.

---

## Handoff types
<!-- scope: llm -->

- **Type A — Programming / workspace** (repo with files):
  3 steps, git + Claude Code, handoff saved as file, verified against git log
- **Type B — Conversational** (browser only, no files, no repo):
  2 steps, handoff lives only in new chat's context window

---

## Type A — Programming Handoff
<!-- scope: dev -->

### Step 1 — In old chat (Claude.ai browser)
<!-- scope: dev -->

Paste the content of: `handoff-prompts/typ-a-step1-browser-prompt.md`

Copy the output.

### Step 2 — In Claude Code (target project)
<!-- scope: dev -->

Paste the handoff from Step 1, then the content of:
`handoff-prompts/typ-a-step2-claudecode-prompt.md`

(Replace `[topic]` with the session slug.)

### Step 3 — New chat (Claude.ai browser)
<!-- scope: dev -->

Upload:
- `ESSENTIALS.md`
- `docs/handoffs/YYYY-MM-DD-[topic].md`
- Project `CLAUDE.md`

First message:
```
Continuing [project]. Goal today: [1-2 objectives].
```

---

## Type B — Conversational Handoff
<!-- scope: llm -->

### Step 1 — In old chat
<!-- scope: llm -->

Paste the content of: `handoff-prompts/typ-b-step1-browser-prompt.md`

Copy the output.

### Step 2 — In new chat
<!-- scope: llm -->

Paste handoff + first message:
```
Continuing [project/topic]. Goal: [1-2 objectives].
```

---

## Handoff format
<!-- scope: meta -->

Handoffs are **downloadable `.md` artifacts** — browser chat outputs them as fenced markdown code blocks; Rob saves the file to `docs/handoffs/YYYY-MM-DD-slug.md`.

Per `PLAYBOOK.md` "Documentation file types and session continuity," handoff format tiers per Scale:

| Scale | Format | Approximate length |
|-------|--------|--------------------|
| **S** (minimal) | What was done + immediate next step | ~30 lines |
| **M** (reduced) | + decisions made + open questions | ~60–80 lines |
| **L** (full) | + context for next chat + files-to-upload checklist + protocol reminders | ~120–200 lines |

**Required structure (Scale M and L):**

1. **Date + repo + branch state**
2. **Objective** — what was the session about
3. **Status** — what got done, what merged, what's pending
4. **Decisions** — with rationale (link to ADRs if applicable)
5. **Pending** — what's not done, urgency, effort estimate
6. **Context for next session** — what files to upload, where to start
7. **Self-critical note** — what didn't work, lessons (becomes LESSONS.md candidate per ADR-29)

---

## Required sections — table
<!-- scope: llm -->

| Section | Content | Type A | Type B |
|---------|---------|--------|--------|
| OBJECTIVE | Session goal | ✔ | ✔ |
| STATUS | One-liner: done / not done | ✔ | ✔ |
| COMPLETED | Per topic, separate section, bullet points with specifics | ✔ | ✔ |
| PENDING | To do within this same chat | ✔ | ✔ |
| REFERRED OUT | Other chats — always with named target | ✔ | opt |
| KEY DECISIONS | Decisions + rationale | ✔ | ✔ |
| CONTEXT | Versions, repo state, what works | ✔ | ✔ |

**Depth rule:** every bullet in COMPLETED/PENDING has a concrete detail (filename, test count, decision, number) — no general statements.

---

## Roles in handoff generation
<!-- scope: meta -->

Per `ESSENTIALS.md` Roles section (v1.0):

- **Browser chat (architect)** generates handoff content. Reads session context, structures output.
- **Claude Code (executor)** does NOT generate browser-chat handoffs. Claude Code's analog is `/session-summary`, which produces session log entries (different artifact, different audience).
- **Rob** decides when handoff happens (trigger), reviews content, saves to `docs/handoffs/`.

Handoffs are the **artifact** that flows architect → next architect (next browser chat session).
They are NOT prompts for Claude Code — those use `templates/prompt-template.md`.

---

## Canonical example
<!-- scope: meta -->

Type A: `docs/handoffs/2026-04-15-tech-radar-session.md`

(Type B canonical example — will add when a good first example exists.)

---

## For Claude Code / models reading this file
<!-- scope: runtime -->

When user asks "give me the handoff process for a programming project":

1. Return the 3-step structure (Step 1 / Step 2 / Step 3)
2. For Step 1: run `cat handoff-prompts/typ-a-step1-browser-prompt.md`
   and return the content verbatim in a code block
3. For Step 2: run `cat handoff-prompts/typ-a-step2-claudecode-prompt.md`
   and return the content verbatim in a code block
4. For Step 3: return the upload list + first message

Do NOT summarize. Do NOT refer to "line X-Y." Do NOT write "the full prompt is in the file."
User wants copy-paste-able output. If the file is 40 lines — return 40 lines.

Same for Type B — cat `handoff-prompts/typ-b-step1-browser-prompt.md` verbatim.

---

## Related references
<!-- scope: meta -->

- `PLAYBOOK.md` "Documentation file types and session continuity" — handoff is one of 12 file types
- `PLAYBOOK.md` "Handoff B: Browser → New Browser" — canonical trigger phrase and format rules
- `PLAYBOOK.md` "Writing prompts for Claude Code" — different artifact (prompts ≠ handoffs)
- `ESSENTIALS.md` "Roles" — browser = architect, Claude Code = executor
- `templates/prompt-template.md` — for Claude Code prompts (companion artifact, not handoffs)
- `handoff-prompts/` — copy-paste templates for handoff generation (per Scale)
- ADR-28 — three-layer architecture (where handoffs fit in the flow)

---

## Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — Vibe Code 4 protocol patch. Translated to English. Added: explicit trigger rule, Scale-tiered format, downloadable artifact requirement, Roles cross-reference, related references section, section history. Prior content (Typ A/Typ B structure, Required Sections table, runtime instructions) preserved and translated.
