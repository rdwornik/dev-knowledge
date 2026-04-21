# Handoff Process

Handoff = transfer kontekstu z jednego Claude chatu do drugiego.
Cel: nie tracić wątku między sesjami.

## Który typ?

- **Typ A — Programming / workspace** (masz repo z plikami):
  3 kroki, git + Claude Code, handoff zapisany jako plik, verified
- **Typ B — Conversational** (browser only, brak plików, brak repo):
  2 kroki, handoff tylko w context window nowego chatu

---

## Typ A — Programming Handoff

### Krok 1 — W starym chacie (Claude.ai browser)

Wklej zawartość pliku: `handoff/typ-a-step1-browser-prompt.md`

Skopiuj output.

### Krok 2 — W Claude Code (projekt docelowy)

Wklej handoff z Kroku 1, potem zawartość pliku:
`handoff/typ-a-step2-claudecode-prompt.md`

(Zmień [topic] na slug tematu.)

### Krok 3 — Nowy chat (Claude.ai browser)

Upload:
- ESSENTIALS.md
- docs/handoffs/YYYY-MM-DD-[topic].md
- CLAUDE.md projektu

Pierwsza wiadomość:
```
Kontynuuję [projekt]. Cel na dzisiaj: [1-2 cele].
```

---

## Typ B — Conversational Handoff

### Krok 1 — W starym chacie

Wklej zawartość pliku: `handoff/typ-b-step1-browser-prompt.md`

Skopiuj output.

### Krok 2 — W nowym chacie

Wklej handoff + pierwsza wiadomość:
```
Kontynuuję [projekt/temat]. Cel: [1-2 cele].
```

---

## Required Sections — Tabela

| Sekcja        | Co tu idzie                          | Typ A | Typ B |
|---------------|--------------------------------------|-------|-------|
| OBJECTIVE     | Cel sesji                            | ✔     | ✔     |
| STATUS        | One-liner: co skończone / co nie     | ✔     | ✔     |
| COMPLETED     | Per topic, osobna sekcja             | ✔     | ✔     |
| PENDING       | Do zrobienia w tym samym chacie      | ✔     | ✔     |
| REFERRED OUT  | Inne chaty, zawsze z named target    | ✔     | opt   |
| KEY DECISIONS | Decyzje + rationale                  | ✔     | ✔     |
| CONTEXT       | Wersje, stan repo, co działa         | ✔     | ✔     |

---

## Canonical Example

Typ A: `docs/handoffs/2026-04-15-tech-radar-session.md`

(Typ B canonical example — dodamy gdy będzie pierwszy dobry przykład)

---

## Dla Claude Code / modeli czytających ten plik

Gdy user pyta "daj mi proces handoff programming project":

1. Zwróć strukturę 3 kroków (Krok 1 / Krok 2 / Krok 3)
2. Dla Kroku 1: wykonaj `cat handoff/typ-a-step1-browser-prompt.md`
   i zwróć zawartość verbatim w code blocku
3. Dla Kroku 2: wykonaj `cat handoff/typ-a-step2-claudecode-prompt.md`
   i zwróć zawartość verbatim w code blocku
4. Dla Kroku 3: zwróć listę uploadów + pierwszą wiadomość

NIE skracaj. NIE odsyłaj do "linia X-Y". NIE pisz "pełny prompt jest w pliku".
User chce copy-paste-able output. Jeśli plik ma 40 linii — zwróć 40 linii.

Analogicznie dla Typ B — cat handoff/typ-b-step1-browser-prompt.md verbatim.
