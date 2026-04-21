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

Wklej dokładnie ten prompt:

```
wygeneruj handoff w formacie markdown, wypisz treść w code blocku.

Required sections:
- OBJECTIVE (cel sesji)
- STATUS (one-liner: co skończone / co nie)
- COMPLETED — [topic] (per topic, osobna sekcja, bullet points z detalami)
- PENDING — [scope] (do zrobienia w tym samym chacie)
- REFERRED OUT — Other Chats (items wymagające action w innym chacie,
  z named target chat + reason)
- KEY DECISIONS (decyzje + rationale)
- CONTEXT (wersje, stan repo, co działa)

Reguły:
- Głębia: każdy bullet w COMPLETED/PENDING ma konkret (plik, test count,
  decyzja, liczba) — nie general statement
- Nie omijaj żadnej sekcji — jeśli pusta, napisz "none"
- PENDING i REFERRED OUT to różne sekcje — PENDING zostaje w tym chacie,
  REFERRED OUT idzie gdzie indziej
```

Skopiuj cały output.

### Krok 2 — W Claude Code (projekt do którego robisz handoff)

Wklej handoff z Kroku 1, potem poniższy prompt (zmień [topic] na slug):

```
| Model  | Sonnet          |
| Mode   | plan-then-auto  |
| Effort | low             |

Zadanie: zapisz handoff z browser chat.

Kroki:
1. Przeczytaj canonical example: docs/handoffs/2026-04-15-tech-radar-session.md
   (jeśli istnieje — jeśli brak, pomiń ten krok)
2. Zweryfikuj handoff powyżej przeciw git log ostatnich 7 dni i aktualnym plikom
3. Popraw rozbieżności (daty, nazwy, statusy)
4. Sprawdź że handoff ma wszystkie required sections: OBJECTIVE, STATUS,
   COMPLETED, PENDING, REFERRED OUT, KEY DECISIONS, CONTEXT. Jeśli brakuje —
   dopisz placeholder "(none)" albo wyciągnij z git log
5. Zapisz JEDEN plik: docs/handoffs/YYYY-MM-DD-[topic].md
6. git add + commit: "docs(handoff): [topic] YYYY-MM-DD"

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

Wklej dokładnie ten prompt:

```
wygeneruj handoff w formacie markdown, wypisz treść w code blocku.

Required sections:
- OBJECTIVE (cel sesji)
- STATUS (one-liner: co skończone / co nie)
- COMPLETED — [topic] (per topic, osobna sekcja, bullet points z detalami)
- PENDING (do zrobienia w tym samym chacie)
- KEY DECISIONS (decyzje + rationale)
- CONTEXT (clients, environments, credentials jako placeholdery, output files)

Reguły:
- Głębia: każdy bullet ma konkret — nie general statement
- Security: sekrety (tokens, client_secret, PAT) zastąp placeholderami
  <TOKEN>, <CLIENT_SECRET>
```

Skopiuj output.

### Krok 2 — W nowym chacie (Claude.ai browser)

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

## Canonical Example (Typ A)

`docs/handoffs/2026-04-15-tech-radar-session.md`

(Typ B canonical example — dodamy gdy będzie pierwszy dobry przykład)

## Template

`templates/HANDOFF_TEMPLATE.md`
