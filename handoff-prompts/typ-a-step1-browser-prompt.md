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
- Scale: S (~30 linii) jeśli sesja była krótka/prosta, M (~60-80 linii)
  standardowo, L (~120-200 linii) jeśli sesja długa + wiele decyzji
