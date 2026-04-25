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
- Scale: S (~30 linii) jeśli sesja krótka, M (~60-80 linii) standardowo,
  L (~120-200 linii) jeśli sesja długa + wiele decyzji
