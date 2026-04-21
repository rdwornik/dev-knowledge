# HANDOFF — Tech Radar + Dev Practice OS Session
Date: 2026-04-21
Project Scale: S (.dev-knowledge)

## OBJECTIVE
Kontynuacja tech radar: refinement handoff process, scope hygiene między chatami, przygotowanie do kolejnych tool evaluations (A/B test Codex vs /ultrareview, claude-usage dashboard, Markitdown benchmark).

## STATUS
Proces-level improvements. Żadnych tool evaluations nie zakończono w tej sesji. Rozpoznane gaps w Dev Practice OS — fix zaplanowany, prompty dla Claude Code przygotowane.

## COMPLETED — Handoff Convention Refinement
- Ustalono split handoff PENDING w dwie sekcje:
  - PENDING — Tech Radar Scope (items dla tego chatu/scope)
  - REFERRED OUT — Other Chats (items wymagające action w innym chacie/projekcie)
- Decyzja: konwencja mieszka w ESSENTIALS.md (nie PLAYBOOK, nie osobny doc)
- Magistrala verification zidentyfikowana jako REFERRED OUT → corp-monorepo chat (operational debt, nie tool evaluation)

## COMPLETED — Scope Hygiene Diagnosis
- Rozpoznano pomylenie scope: handoff 2026-04-15 miał magistrala verification w PENDING, choć to operational debt corp-monorepo, nie tech radar
- Ustalono zasadę: ten chat = LLM/dev tooling evaluation i adoption (Codex, Tach, Opus 4.7, Markitdown, claude-usage). Wszystko inne → REFERRED OUT
- Presales knowledge base architecture pytanie (Databricks demo prep, training materials) → zidentyfikowane jako off-topic, nowy chat "Presales Knowledge Base Architecture" proponowany

## COMPLETED — Dev Practice OS Gap Identified
- Claude Code w .dev-knowledge generował słabe handoffy (mała głębia, brak Model/Mode/Effort, tworzył dwa pliki zamiast jednego)
- Root cause: ESSENTIALS.md "Browser chat checkpoint" ma tylko 4-liniowy skrót bez specyfikacji formatu
- Gaps do naprawy:
  - Brak specyfikacji required sections
  - Brak rule "JEDEN plik w docs/handoffs/"
  - Brak wymagania Model/Mode/Effort w prompcie
  - Brak template/canonical example reference
- Prompt dla Claude Code przygotowany (w chacie, nie jeszcze wykonany)

## PENDING — Tech Radar Scope
- Fix ESSENTIALS.md handoff section — rozszerzenie sekcji "Browser chat checkpoint" z required sections, jeden-plik rule, Model/Mode/Effort requirement, canonical example link
- Utworzenie templates/HANDOFF_TEMPLATE.md w .dev-knowledge
- Codex vs /ultrareview A/B test — next feature branch, run both, compare findings
- claude-usage dashboard (phuryn/claude-usage) — install for baseline cost numbers
- Markitdown benchmark — vs CKE tier-1 extraction on Lenzing/PepsiCo test set
- Tach for M-scale repos (ai-council, corp-ops) — Council #26 deferred, evaluate after 1 month (~15 maja)

## REFERRED OUT — Other Chats
- Magistrala verification → corp-monorepo chat
  Reason: operational debt from Council #24 MyWork restructure, not tool evaluation
- Presales knowledge base architecture (Databricks training materials, platform services, presentation workspace) → new chat "Presales Knowledge Base Architecture"
  Reason: knowledge management architecture, not LLM tool evaluation. Tylko tool-choice subset (Claude Projects vs NotebookLM vs vault+RAG) może wrócić tu jako tool eval.

## KEY DECISIONS
- Tech radar chat scope: LLM/dev tooling evaluation + adoption only. Wszystko inne → REFERRED OUT z named target chat
- Handoff format: PENDING (same scope) vs REFERRED OUT (other chat) — zawsze split
- Handoff = JEDEN plik, docs/handoffs/YYYY-MM-DD-[topic].md. Żadnego dodatkowego HANDOFF.md w docs/
- Claude Code prompt dla handoffu musi zawierać Model/Mode/Effort header
- Konwencja mieszka w ESSENTIALS.md, nie PLAYBOOK ani osobny doc

## CONTEXT
- Claude Code v2.1.112, Opus 4.7 available
- .dev-knowledge: S-scale, handoff process improvement pending
- Tech radar backlog: 4 items w scope (A/B test, claude-usage, Markitdown, Tach M-scale)
- 2 items referred out: magistrala (corp-monorepo), presales KB architecture (new chat)
- Poprzednia sesja: 2026-04-15 — Codex, Tach, Opus 4.7, Project Scale Tiers wdrożone
