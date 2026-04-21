# HANDOFF — Tech Radar + Dev-Knowledge Architecture Redefinition
Date: 2026-04-21
Project Scale: S (.dev-knowledge)
Session Duration: ~4h

## OBJECTIVE
Rozpoczęto jako tech radar session (kontynuacja 2026-04-15). Scope rozszerzył się znacząco: handoff process refinement → audit .dev-knowledge → Council #27 debate → fundamental redefinition of .dev-knowledge vision (three-layer architecture). Zero tech radar backlog items addressed.

## STATUS
Heavy decision work ukończony, ZERO implementation. 6 major decisions podjęte w sesji. Implementation backlog 8+ godzin pracy. Świadoma decyzja: handoff teraz, implementacja w nowej sesji ze świeżą głową.

## COMPLETED — Handoff Process Refinement
- Extracted handoff prompts z HANDOFF_PROCESS.md do dedicated files:
  - handoff/typ-a-step1-browser-prompt.md (generate handoff)
  - handoff/typ-a-step2-claudecode-prompt.md (save handoff)
  - handoff/typ-b-step1-browser-prompt.md (conversational handoff)
  - handoff/README.md (index)
- HANDOFF_PROCESS.md zaktualizowany: references do plików w handoff/, plus twarda instrukcja dla modeli czytających ("cat verbatim, zero skracania")
- Renamed Claude Code skill /handoff → /session-summary (uniknięcie konfliktu nazw)
- Fixed description pierwszej linii session-summary.md (usunięto słowo "handoff" z opisu — false trigger fix)
- Diagnozowany root cause słabych handoff outputów: description keyword matching, nie brak frontmattera
- ESSENTIALS.md line 25: /handoff → /session-summary

## COMPLETED — Cleanup
- Skasowany docs/codex-review-integration.md (4-liniowy stub, info żyje w handoff 2026-04-15 + PLAYBOOK S15/S16)

## COMPLETED — .dev-knowledge Audit (Faza 1 + 2)
- docs/audits/2026-04-21-dev-knowledge-inventory.md: 22 files, 2311 lines, 22 days old, zero scope drift po nazwach, zero stubów po cleanup, zero duplicates, orphan files obsługiwane przez folder-level linking
- docs/audits/2026-04-21-dev-knowledge-scope-tagging.md: 63 sections analyzed across 8 primary files
- Tag distribution: meta 35%, llm 22%, hybrid 21%, dev 14%, runtime 8%
- Kluczowe findings:
  - 22% [llm] czysto ekstrahowalne (13 sections)
  - 21% [hybrid] wymaga decyzji Council
  - 7/13 hybrid = pattern "universal structure + dev-specific examples" (PLAYBOOK S2, S7, S9)
  - LESSONS.md strukturalnie nieseparowalny (append-only constraint)
  - ESSENTIALS/PLAYBOOK/LESSONS = hottest files (23 commits w 30 dni) = hot-path decyzji

## COMPLETED — Council #27 (LLM Practice Ecosystem Architecture)
- docs/audits/2026-04-21-council-27-brief.md utworzony z 4 warianty (0, A, B, C) + Decision Matrix + 3 peer-review fixes (Option 0, matrix caveat, LESSONS honest framing)
- AI Council debate uruchomiony przez council_inbox/, 5 modeli × 2 rundy, 379s, $0.83, 186K tokens
- Panel: Claude Opus 4.7, Gemini 3.1 Pro Preview, GPT-5.4, Grok 4.20, DeepSeek Reasoner. Synthesizer: Claude Sonnet
- Output: output/20260421_145718_2026-04-21-council-27-brief.md
- DECYZJA COUNCIL: Option A (single repo + section-level tagging) + dwa additions
- Vote distribution: Claude R1→Option 0, R2→A; Gemini/OpenAI/DeepSeek R1+R2→A; Grok R1→B, R2→C (rejected)
- Decydujący argument (OpenAI R2): "Option A jest dominant strategy" — correct jeśli demand weak (terminal architecture), correct jeśli demand strong (pre-classifies for split)

## COMPLETED — Vision Redefinition (NEW — beyond Council #27)
- Rozpoznane że `.dev-knowledge` nie jest journalem, ale source of truth w szerszej architekturze
- Three-layer architecture sformułowana i zaakceptowana:
  1. Browser chat (analiza, synteza, krytyczne myślenie, processing feedów)
  2. .dev-knowledge (passive storage, templates, patterns, lessons)
  3. Konkretne projekty (wykonanie, czytają z .dev-knowledge, generują content)
- Information flow: browser → handoff → dev-knowledge → pull → projekty → refleksja → browser → handoff → dev-knowledge (cykl zamknięty)
- Zasada: biblioteka nie wywołuje akcji. Żadnych skryptów. Cała analityka w browser chat z Claude.
- "Read-only" odrzucone jako zbyt mocne słowo — information flow jest bidirectional (write back przez browser), tylko execution jest one-way

## PENDING — Council #27 Implementation (8-9h)
- Tag 8 primary files (63 sections) używając Phase 2 tags as source of truth — 4-6h
- Pre-commit hook validating scope: vocabulary (dev | llm | hybrid | meta | runtime) — 1-2h
- Update CLAUDE.md: tag vocabulary + consumer read sets + hybrid ≤25% rule + evidence-triggered reopening conditions — 1h
- Update ESSENTIALS + SESSION_SETUP z explicit upload/read protocols per consumer type — 30 min
- LESSONS.md disposition ADR: grandfather existing 123 lines, tag going forward only — 10 min
- Dodatkowe: udokumentować three-layer architecture w PLAYBOOK lub ESSENTIALS
- Dodatkowe: hygiene review ritual (missing piece, brakujący rytuał dla staleness detection)
- Dodatkowe: ADR-27 formalny w docs/audits/ lub osobnym decisions/ folderze

## PENDING — Tech Radar Scope (nienaruszone z 2026-04-15)
- Codex vs /ultrareview A/B test — next feature branch, compare findings
- claude-usage dashboard (phuryn/claude-usage) — install dla baseline cost numbers
- Markitdown benchmark — vs CKE tier-1 extraction on Lenzing/PepsiCo test set
- Tach for M-scale repos (ai-council, corp-ops) — deferred ~15 maja

## REFERRED OUT — Other Chats
- Magistrala verification → corp-monorepo chat
  Reason: operational debt z Council #24 MyWork restructure, nie tool evaluation
- Presales knowledge base architecture → new chat "Presales Knowledge Base Architecture"
  Reason: knowledge management architecture, nie LLM tool evaluation (off-topic, zidentyfikowany i odłożony wcześniej w sesji)
- Council #28 Candidate: three-layer architecture formal ratification
  Reason: odkryte w tej sesji post-Council #27, zasługuje na własny debate
- Council #29 Candidate: hygiene review ritual design
  Reason: missing piece zidentyfikowany, ale design deserves own thought

## KEY DECISIONS

### Council #27 — Option A (binding, consensus 4/5 models)
- Adopt single repo z full section-level scope tagging
- Additions: pre-commit hook enforcement + evidence-triggered reopening (NIE calendar-based)
- Reopening triggers: (a) staffed non-dev project starts, OR (b) 5+ new [llm]-only sections in 60 days, OR (c) second contributor
- Grandfathered LESSONS.md: existing 123 lines untouched, new entries require inline scope tag
- Hybrid ≤25% governance rule: hybrid jest temporary, decompose at quarterly hygiene pass

### Three-Layer Architecture (moja decyzja, pending formal ratification)
- Browser chat (ten i podobne) = analytical layer
- .dev-knowledge = passive storage layer
- Projekty = execution layer
- Brak skryptów, brak active orchestrator, brak corp-by-os-style wykonania
- Feedback loop explicite: write back do .dev-knowledge wyłącznie przez browser chat handoff

### Session Discipline
- Decision fatigue po 4h = realna. Świadome zamknięcie sesji z handoff lepsze niż zmęczona implementacja
- Handoff jest critical infrastructure dla three-layer architecture — bez niego ciągłość myślenia ginie

### Rejected Options
- Option B (two repos + shared core) — odrzucony przez Council, non-dev demand hypothetical
- Option C (base + extension overlay) — odrzucony przez Council, fails 2am test, custom markdown loader liability
- Option 0 (defer decision) — odrzucony przez Council, Phase 2 audit IS the evidence, dodanie 6-8 tygodni marginal value
- "Read-only" jako słowo — odrzucone, information flow jest bidirectional

## CONTEXT

### Repo State
- .dev-knowledge: master, clean
- 22 tracked markdown files, 2311 lines
- Last commits: handoff prompt extraction, /session-summary rename, audits (Fazy 1-2), Council brief, codex stub deletion
- AI Council output: output/20260421_145718_2026-04-21-council-27-brief.md

### Tooling
- Claude Code v2.1.112, Opus 4.7
- AI Council CLI: 5 debate + 4 research providers, 4 modes, synthesizer Sonnet (standard)
- VS Code workspace, pytest, ruff, git

### Drag & Drop Issue (diagnosed)
- VS Code explorer drag → browser daje tylko path, nie file data
- Workaround: File Explorer (not VS Code) drag działa
- Rekomendacja: pin docs/audits/ + docs/handoffs/ do Quick Access + keybind Ctrl+Alt+R dla Reveal in File Explorer

### Session Discipline Insight
- Tech radar sesja rozszerzyła się o fundamental architecture work — NIE był to scope creep w sensie negatywnym, tylko discovery
- Ale zero original tech radar items addressed — backlog nietknięty
- Lesson: architecture discovery może wyjść z tool evaluation context naturally, trzeba to rozpoznać i albo refocus albo domknąć

### Files Generated Today
- docs/audits/2026-04-21-dev-knowledge-inventory.md
- docs/audits/2026-04-21-dev-knowledge-scope-tagging.md
- docs/audits/2026-04-21-council-27-brief.md
- handoff/ folder (4 files) + HANDOFF_PROCESS.md updates
- ESSENTIALS.md updated (session-summary rename)
- ~/.claude/commands/session-summary.md description fix
- Deleted: docs/codex-review-integration.md
- AI Council archive: output/20260421_145718_2026-04-21-council-27-brief.md

### Next Session Priorities (sugerowane dla new chat)
1. Udokumentować three-layer architecture w PLAYBOOK przed implementation (30 min)
2. Council #27 implementation — tagi + hook + CLAUDE.md updates (6-8h, może być rozłożone na 2 sesje)
3. ADR-27 formalny
4. Considering hygiene review ritual (osobna decyzja, może Council #29)
5. Powrót do tech radar backlog (A/B test, claude-usage, Markitdown) dopiero po Council #27 implementation
