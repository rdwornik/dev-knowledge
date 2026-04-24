# Handoff Prompts

Gotowe do użycia prompty dla handoff process. Zero kompresji — cat i paste.

## Pliki
<!-- scope: llm -->

- `typ-a-step1-browser-prompt.md` — Programming: browser prompt (generate handoff)
- `typ-a-step2-claudecode-prompt.md` — Programming: Claude Code prompt (save handoff)
- `typ-b-step1-browser-prompt.md` — Conversational: browser prompt (generate handoff)

Typ B nie ma step 2 — handoff żyje tylko w context window nowego chatu.

## Jak użyć
<!-- scope: llm -->

Gdy user pyta "daj proces handoff", model czytający HANDOFF_PROCESS.md
powinien zwrócić zawartość odpowiednich plików verbatim (cat), nie skracać.
