# 03 · The project — ai-council

## Vision

`ai-council` is a multi-model AI debate and research tool for architectural
decision-making across the dev ecosystem. It runs structured deliberation across a
configurable AI panel and **produces the verdicts that become binding ADRs** governing all
repos under `Dev/`. It is a standalone CLI (`council` entry point) consumed by other repos
— invoked by them, never embedded as a library.

## Scope

- **5 debate providers:** Claude Opus, Gemini, GPT, Grok, DeepSeek.
- **5 research providers:** Perplexity, Gemini Deep Research, OpenAI o4-mini deep research,
  Grok x_search, OpenAI o3 deep research.
- **4 modes:** pick / ideas / judge / research. **Synthesizer:** Gemini (ADR-01).
- **Dual output:** operational metrics + transcripts in `ai-council/output/`; curated
  transcripts in `.dev-knowledge/docs/decisions/transcripts/` (ADR-43 routing).

**Core values (do not erode):**
- **Blind deliberation over authority** — Round-2 responses are anonymized + shuffled
  (ADR-03) so verdicts rest on argument, not provider reputation.
- **Config as single source of truth** — model strings, prompts, personas, cost rates live
  only in `config/settings.yaml`.
- **Fail loud at the boundary** — unknown routing → RoutingError; degraded research run →
  exit code 3 + alarm banner (ADR-08).
- **Cost-aware deliberation** — panel size + rounds tunable; `--lite` + per-provider cost
  tracking keep debate proportional to the question.

## Purpose & critical paths

- **Name:** `ai-council`  ·  **Status:** active  ·  **Owner:** Rob.
- **Purpose:** Multi-model debate/research CLI; produces binding ADRs governing the `Dev/`
  ecosystem.
- **Critical paths:** `src/ai_council/`, `tests/`, `docs/decisions/`, `config/settings.yaml`.
- **Out of scope:** client/pre-sales → Obsidian vault; cross-ecosystem lessons →
  `.dev-knowledge/LESSONS.md`; curated transcripts → `.dev-knowledge/docs/decisions/transcripts/`.

## Sacred files (do not break these)

- **`config/settings.yaml`** — the single source of truth for every model string, prompt,
  persona, timeout, and cost rate. Hard-coding any of these is a critical-rule violation.
- **`LESSONS.md`** — append-only (ADR-29); never edit old entries, only append.
- **`JOURNAL.md`** — append-only, newest-first prepend at session wrap.
- **ADRs (`docs/decisions/ADR-*`)** — immutable; supersede with a new ADR, never edit in place.
- **`_anonymize_responses()` shuffle** — part of the blind-voting contract (ADR-03); do not
  change without an ADR.
- **`xai.py` / `deepseek.py`** — keep as separate providers; do NOT merge them (CLAUDE §5
  critical rule 7).
- **Living docs** — `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md` carry a `last_reviewed`
  stamp; bump only after a genuine end-to-end re-read (audit.py check #10).

## Cross-repo ownership (ADR-41)

This bundle covers **ai-council only**. Never direct work on another repo from here, never
edit another repo's BACKLOG or files. `.dev-knowledge` is the methodology meta-layer
(it hosts this bundle and the ecosystem ADRs); ai-council consumes those ADRs and feeds
lessons back — no authority hierarchy, only functional roles. The ADR-67 implementation
obligation (below) is ai-council's own to build; the *process* spec lives in `.dev-knowledge`.
