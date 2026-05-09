# State of Play — ai-council (audit-sync, 2026-05-09)

## Migration completion (verified at Stage 3)

ADR-38 structural migration completed 2026-04-30. 5-commit sequence
(8d16c3c → c821157, HEAD). Refactored to `src/ai_council/` package namespace.
All imports updated. pyproject.toml updated. Tests updated. 310/310 tests pass
per migration report. ADR-38 compliance: PASS (5/5 checks).

## Audit findings (2026-04-30 Faza A2 — .dev-knowledge external view)

**P1 — Governance-blocking, tier-independent:**
- F-01: VISION.md absent — create per ADR-33 schema
- F-02: Lessons discovery not configured — add DEV_KNOWLEDGE_PATH to CLAUDE.md

**P2 — Deferred pending tier calibration:**
- F-03: BACKLOG.md absent — defer until ADR-40 recalibration
- F-04: ARCHITECTURE.md absent — defer until tier confirmed

**P3 — Minor/grandfathered:**
- F-05: ADR naming kebab-case — 7 existing ADRs grandfathered per ADR-29;
  future ADRs follow ADR-34 underscore convention
- F-06: Test count discrepancy (grep vs CLAUDE.md) — class-based tests;
  `pytest --collect-only -q` is canonical; no action
- F-07: Module count 2 vs estimate 8 — calibration imprecision; no action

**Calibration concern (cross-ecosystem, no ai-council action):**
- F-08: All repos clamp to L under current ADR-40 coefficients; algorithm
  miscalibration deferred to audit tool P1 multi-repo data collection

## Architect-witnessed state (Stage 2, with Stage 3 verification)

### Verified claims

- **ADR-38 migration completed in this chat** — VERIFIED (`git log` shows
  5 migration commits: 8d16c3c, 88681ce, c410eaa, 1608fab, 0eef938 + merge c821157)
- **Gemini is default synthesizer** — VERIFIED (`settings.yaml:
  synthesizer: "gemini"`)
- **Grok added as 5th research provider** — VERIFIED (5 files in
  `src/ai_council/research/providers/`: perplexity.py, grok_research.py,
  openai_deep_research.py, openai_mini_research.py, gemini_research.py)
- **5 debate providers** — VERIFIED (5 provider files in
  `src/ai_council/providers/`: anthropic.py, deepseek.py, gemini.py,
  openai_provider.py, xai.py)
- **council CLI entry point** — VERIFIED (`pyproject.toml [project.scripts]:
  council = "ai_council.cli:main"`)
- **council_inbox/ creation fix committed** — VERIFIED (commit `673721d fix:
  resolve council_inbox to repo root not cwd`; architect said
  "(architect inference)")
- **--models flag implemented** — VERIFIED (found in cli.py, orchestrator.py,
  runner.py; architect listed as unknown)

### Verification failures / corrections

- **Architect claimed:** "config/settings.yaml Grok research timeout increased
  from 120s to 300s" — **VERIFICATION FAILED / CORRECTION NEEDED**
  Actual diff: grok model string changed from `"grok-4.20"` to `"grok-4.3"`
  (in `models.grok.model`) plus whitespace normalization across YAML array
  formatting. No timeout change is visible in the diff. The research.grok
  timeout was already 300s in HEAD (pre-diff state).
  **For next session:** verify actual diff before committing. The commit
  message suggested by architect ("config: increase Grok research timeout
  to 300s") does not describe the actual change. Review `git diff
  config/settings.yaml` and write accurate commit message.

### Unverifiable claims (preserved)

- "Claude Sonnet 4.6 timed out on 5-model transcripts" — conversation
  history, cannot verify from repo
- "OpenAI o4-mini-deep-research intermittently fails on complex queries" —
  external service behavior, cannot verify
- "Grok smoke test succeeded at $0.23, 1m06s" — past runtime behavior
- "Downloads auto-scan: files without frontmatter were silently skipped" —
  bug report from conversation history

### Architect inferences (preserved with flag)

- "Most test volume is provider mocking and config validation" —
  (architect inference: based on writing prompts that touched these files)
- "if diff contains more than timeout change, review before committing" —
  (architect inference: may be accumulated changes from prior sessions)
  **Stage 3 note: this inference was CORRECT — see Verification failure above**
- "If config/settings.yaml diff contains unexpected changes: STOP, show
  diff to Rob" — (architect's contingency, in BOUNDARIES section)

## Architect rationale (preserved)

### Tier judgment: M (not L)

Architect reasoning (summarized):
- Personal productivity tool, 1 developer, no SLA, no uptime requirements
- L implies infrastructure criticality that doesn't apply
- 310 tests + 102K tokens look heavy, but core engine is simple: parallel
  API calls, prompt assembly, blind voting, synthesis
- Limited blast radius: if broken, Rob loses a convenience tool
- HOWEVER: ai-council produces binding ADRs governing all repos →
  argues M (not S); output has governance consequences

Recommendation: tier M, revisit if ai-council gains inbound API
dependencies or automated pipeline integration.

### Lessons discovery criterion

ai-council `tasks/lessons.md` contains operational lessons about
provider API quirks, SDK gotchas, code patterns unique to this repo.
These should remain local. Reference DEV_KNOWLEDGE_PATH so future
cross-cutting lessons CAN flow to .dev-knowledge. Criterion: lesson
applies only to ai-council code → stays local; applies across repos
(package renames, provider integrations) → copy to .dev-knowledge.

## Decisions locked

- **Tier per ADR-40 algorithm:** L (all repos clamp; calibration concern
  F-08 flagged; deferred to audit tool P1)
- **Tier per architect judgment:** M (personal tool, limited blast radius,
  low infrastructure criticality)
- **Path 3 calibration strategy** (continue audit, defer recalibration)
  applied 2026-04-30
- **Synthesizer:** Gemini (deliberate; Claude Sonnet 4.6 timed out on
  5-model transcripts)
- **5-provider panel:** deliberate decision from conversation

## Deferred items (BACKLOG references — do not duplicate queue)

- F-03 BACKLOG.md: deferred pending tier calibration
  (.dev-knowledge BACKLOG Cross-stream P1: Phase 1 validation)
- F-04 ARCHITECTURE.md: deferred pending tier calibration
- ADR-40 recalibration: deferred to audit tool P1
  (.dev-knowledge BACKLOG Stream C P1: Audit tool P1 implementation)
- Council research on relative repo complexity
  (.dev-knowledge BACKLOG Cross-stream P2)

## Stage 3 verification summary

Architect provided ~20 claims:
- **7 verified** against repo state (migration commits, synthesizer,
  research providers, debate providers, CLI entry, council_inbox fix,
  --models flag)
- **4 unverifiable** from repo (conversation history, external service
  behavior, past runtime costs)
- **3 inferences preserved with flag** (test volume characterization,
  config review recommendation, accumulated-changes warning)
- **1 VERIFICATION FAILED:** config/settings.yaml change is grok model
  string, not timeout; architect's commit message recommendation incorrect
