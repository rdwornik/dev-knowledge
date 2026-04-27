# Handoff Prompts

Ready-to-use prompts for the handoff process. No compression — cat and paste.

**Authoritative protocol:** `protocols/HANDOFF_PROCESS.md` — trigger rules, Scale-tiered format, Roles. This folder contains the copy-paste templates only.

## Files
<!-- scope: llm -->

- `typ-a-step1-browser-prompt.md` — Programming: browser prompt (generate handoff)
- `typ-a-step2-claudecode-prompt.md` — Programming: Claude Code prompt (save handoff)
- `typ-b-step1-browser-prompt.md` — Conversational: browser prompt (generate handoff)

Type B has no step 2 — handoff lives only in the new chat's context window.

## How to use
<!-- scope: llm -->

When user asks "give me the handoff process," the model reading `protocols/HANDOFF_PROCESS.md`
should return the content of the relevant files verbatim (cat), not summarize.

Templates are in Polish — this is intentional. `wygeneruj handoff` is the Vibe Code 4 trigger phrase.
Scale (S/M/L) is specified by Rob at trigger time, not embedded in the template.
