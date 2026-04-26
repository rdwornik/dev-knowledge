# Handoff Process
<!-- version: 1.1 — 2026-04-26 (3-artifact amendment) -->

**Amendment 2026-04-26 (handoff = 3 artifacts):** Original v1.0 documented handoff as single downloadable .md artifact. Real process produces 3 distinct artifacts with different audiences and lifecycles. Section restructured to make this explicit. Per Gap #19 amendment-vs-reopen protocol: prescription drift (artifact count), intent (cross-session context transfer) preserved.

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

A complete handoff produces **3 distinct artifacts**, each with a different audience and lifecycle. Conflating them creates self-referential failures (e.g. upload list inside the file being uploaded).

### Artifact 1: Handoff document (persistent)
<!-- scope: meta -->

**Audience:** future Rob + future browser Claude (in next chat)
**Lifecycle:** permanent record committed to repo
**Location:** `<repo>/docs/handoffs/YYYY-MM-DD-<slug>.md`
**Tier:** Scale-dependent format per Project Scale Tiers section:
- **Scale S** (minimal): What was done + immediate next step. ~30 lines.
- **Scale M** (reduced): + decisions made + open questions. ~60–80 lines.
- **Scale L** (full): + context for next chat + files-to-upload checklist + protocol reminders. ~120–200 lines.

**Required structure (Scale M and L):**
1. Date + repo + branch state
2. Objective — what was the session about
3. Status — what got done, what merged, what's pending
4. Decisions — with rationale (link to ADRs if applicable)
5. Pending — what's not done, urgency, effort estimate
6. Files to upload to next chat — explicit numbered list with paths from repo root
7. Self-critical note — what didn't work, lessons (becomes LESSONS.md candidate per ADR-29)

**Does NOT contain:**
- First message template (that's Artifact 3)
- Claude Code commit instructions (that's Artifact 2)

### Artifact 2: Claude Code commit prompt (disposable)
<!-- scope: runtime -->

**Audience:** Claude Code (executor — saves Artifact 1 to repo)
**Lifecycle:** disposable — used once at handoff generation, can be deleted after
**Location:** local file on Rob's machine, NOT in repo
**Format:** standard Claude Code prompt per `templates/prompt-template.md`

**Required content:**
- Repo path, branch workflow (new branch, single commit, ff-merge to master)
- Instruction to receive Artifact 1 content from Rob's paste
- Save to `docs/handoffs/YYYY-MM-DD-<slug>.md`
- Validator + git status verification
- Report commit hash and state back to Rob

### Artifact 3: First message template for new chat (disposable)
<!-- scope: llm -->

**Audience:** new browser Claude (in next chat)
**Lifecycle:** disposable — pasted once at chat start, can be deleted after
**Location:** local file on Rob's machine OR clipboard, NOT in repo
**Format:** plain text suitable for paste into chat input

**Required content:**
- Greeting + which Stream/session this is
- Scope: IN/OUT/Success criterion
- Reference to handoff document (Artifact 1) by upload position number
- Last session stopping point
- Protocol reminders (browser=architect, English in prompts, session boundaries, etc.)
- First task pointer — what specific gap/work to start with

**Why disposable separately:** if first message lived inside Artifact 1, new browser Claude would receive its own instructions as upload context, creating confusion. Separating makes audience clear: Artifact 1 is read material, Artifact 3 is the prompt.

### Workflow at handoff generation
<!-- scope: meta -->

1. Browser chat (architect) produces Artifact 1 content + Artifact 2 prompt + Artifact 3 template — all in chat output
2. Rob copies Artifact 1 content to clipboard
3. Rob pastes Artifact 2 prompt to Claude Code, including Artifact 1 content as part of prompt input
4. Claude Code saves + commits + reports
5. Rob saves Artifact 3 template to clipboard or temp file for later use

### Workflow at next chat start
<!-- scope: llm -->

1. Rob opens new browser chat
2. Rob uploads files from Artifact 1's "Files to upload" section (in order)
3. Rob pastes Artifact 3 template as first message
4. New browser Claude receives full context + scoped first task → responds substantively without "what did you mean by X" follow-ups

### Walk-out test
<!-- scope: meta -->

Handoff succeeded if new browser Claude's first response is substantive analysis of the scoped first task, with no clarification questions about prior session context. If it asks "what did we decide about X" or "what files should I look at" → handoff failed; previous session must produce better artifacts.

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

- v1.1 (2026-04-26) — amended to document handoff = 3 artifacts (persistent doc + commit prompt + first-message template). v1.0 conflated all three into single file, creating self-referential paradox. Discovered in practice during Stream B → Stream C handoff attempt.
- v1.0 (2026-04-25) — Vibe Code 4 protocol patch. Translated to English. Added: explicit trigger rule, Scale-tiered format, downloadable artifact requirement, Roles cross-reference, related references section, section history. Prior content (Typ A/Typ B structure, Required Sections table, runtime instructions) preserved and translated. (Superseded by v1.1 — single-artifact framing.)
