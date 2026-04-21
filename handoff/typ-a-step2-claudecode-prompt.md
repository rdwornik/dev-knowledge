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
   COMPLETED, PENDING, REFERRED OUT, KEY DECISIONS, CONTEXT.
   Jeśli brakuje — dopisz "(none)" albo wyciągnij z git log
5. Zapisz JEDEN plik: docs/handoffs/YYYY-MM-DD-[topic].md
6. git add + commit: "docs(handoff): [topic] YYYY-MM-DD"

Nie twórz HANDOFF.md w docs/. Tylko jeden plik w docs/handoffs/.
