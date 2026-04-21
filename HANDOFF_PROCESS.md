# Handoff Process

Handoff = transfer kontekstu z jednego Claude chatu do drugiego.
Cel: nie tracić wątku między sesjami.

## Który typ?

- **Typ A — Programming / workspace** (masz repo lub workspace z plikami):
  git + Claude Code, handoff zapisany jako plik, verified
- **Typ B — Conversational** (czysto browser, brak plików, brak repo):
  tylko browser, handoff w context window, copy-paste między chatami

---

## Typ A — Programming Handoff

### Krok 1 — W starym chacie (Claude.ai browser)

Wpisz:

```
wygeneruj handoff w formacie markdown, format jak canonical example
docs/handoffs/2026-04-15-tech-radar-session.md, ze splitem PENDING /
REFERRED OUT
```

Skopiuj cały output.

### Krok 2 — W Claude Code (projekt do którego robisz handoff)

Wklej handoff, potem poniższy prompt (zmień [topic] na slug):

```
| Model  | Sonnet          |
| Mode   | plan-then-auto  |
| Effort | low             |

Zadanie: zapisz handoff z browser chat.

Kroki:
1. Przeczytaj canonical example: docs/handoffs/2026-04-15-tech-radar-session.md
2. Zweryfikuj handoff powyżej przeciw git log ostatnich 7 dni i aktualnym plikom
3. Popraw rozbieżności (daty, nazwy, statusy)
4. Zapisz JEDEN plik: docs/handoffs/YYYY-MM-DD-[topic].md
5. git add + commit: "docs(handoff): [topic] YYYY-MM-DD"

Required sections: OBJECTIVE, STATUS, COMPLETED (per topic),
PENDING — [scope], REFERRED OUT — Other Chats, KEY DECISIONS, CONTEXT.

Nie twórz HANDOFF.md w docs/. Tylko jeden plik w docs/handoffs/.
```

### Krok 3 — Nowy chat (browser)

Upload:
- ESSENTIALS.md
- docs/handoffs/YYYY-MM-DD-[topic].md
- CLAUDE.md projektu (jeśli programming chat)

Pierwsza wiadomość:
```
Kontynuuję [projekt]. Cel na dzisiaj: [1-2 cele].
```

---

## Typ B — Conversational Handoff

### Krok 1 — W starym chacie (Claude.ai browser)

Wpisz:

```
wygeneruj handoff w formacie markdown, required sections: OBJECTIVE,
STATUS, COMPLETED, PENDING, KEY DECISIONS, CONTEXT
```

Skopiuj cały output.

### Krok 2 — W nowym chacie (Claude.ai browser)

Wklej handoff + pierwsza wiadomość:
```
Kontynuuję [projekt/temat]. Cel: [1-2 cele].
```

**Security:** Jeśli handoff zawiera sekrety (tokens, client_secret,
PAT) — zastąp placeholderami `<TOKEN>`, `<CLIENT_SECRET>` przed wklejeniem.

---

## Required Sections — Tabela

| Sekcja       | Co tu idzie                       | Typ A | Typ B |
|--------------|-----------------------------------|-------|-------|
| OBJECTIVE    | Cel sesji                         | ✔     | ✔     |
| STATUS       | One-liner: co skończone / co nie  | ✔     | ✔     |
| COMPLETED    | Per topic, osobna sekcja          | ✔     | ✔     |
| PENDING      | Do zrobienia w tym samym chacie   | ✔     | ✔     |
| REFERRED OUT | Inne chaty, zawsze z named target | ✔     | opt   |
| KEY DECISIONS| Decyzje + rationale               | ✔     | ✔     |
| CONTEXT      | Wersje, stan repo, co działa      | ✔     | ✔     |

---

## Canonical Example (Typ A)

`docs/handoffs/2026-04-15-tech-radar-session.md`

(Typ B canonical example — dodamy gdy będzie pierwszy dobry przykład)

## Template

`templates/HANDOFF_TEMPLATE.md`
