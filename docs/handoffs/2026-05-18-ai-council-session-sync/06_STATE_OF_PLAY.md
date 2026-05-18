# State of Play

**Repo:** ai-council
**Date:** 2026-05-18
**HEAD:** ce885827aada41f582e784fa210f73ff125a18de
**Branch:** main
**Working tree:** clean

---

## What Was Completed

All of the following landed in commits and are merged to `main`:

**Provider reliability hardening arc (now complete):**
- OpenAI research providers migrated off deprecated deep-research model identifiers
  onto current-generation models.
- Research-panel degradation alarm added: when fewer than the configured minimum of
  research providers succeed, the run completes but emits an aggregate banner and
  exits with code 3. Recorded in ADR-08.
- Health classifier gained a distinct billing error category — an exhausted-API-credit
  failure now surfaces clearly rather than as a generic error.
- Provider health gate scoped to the active mode: a mode that does not use a given
  provider family no longer blocks startup on that family's health check. Research mode
  is unaffected by Anthropic provider health failures.
- Perplexity research timeout raised from 60s to 240s; single SDK-level transient retry
  added. Accompanying test asserts `>= 120` invariant (not literal `240`).
- Brief-file naming convention section added to `docs/council-question-guide.md`.

**Governance (present at Stage 3 verification):**
- `AGENTS.md` exists at repo root, last updated 2026-05-17. Fully populated with
  conventions, build/test commands, and constraints for Codex.

---

## Current State

- Test suite: **413 unit tests passing** (no API keys needed;
  `pytest tests/ -m "not integration and not envcheck" -v`)
- 110 tracked files (see 08_TREE.txt)
- Working tree clean; no commits since Stage 1 capture
- Anthropic API credit state: **Unknown** — verify before attempting debate mode
  (research mode is unaffected; uses no Anthropic providers)

---

## Decisions Locked

Do not revisit without the rationale below:

1. **Perplexity timeout at 240s** — based on a live reproduction that measured a real
   research query completing at ~68 seconds; 240s is a deliberate variance buffer.
   The accompanying test asserts `>= 120` (not literal `240`) to guard against
   regression to the old 60s ceiling without blocking legitimate retuning.

2. **Provider health gate is mode-scoped** — research mode must not be blocked by
   Anthropic provider failures (exhausted credits) because research mode uses no
   Anthropic providers. Changing to a global gate would break this guarantee.

3. **Billing exhaustion is a distinct classifier** — surfacing it clearly prevents
   future debugging from chasing phantom code bugs when the actual cause is an operator
   top-up need.

4. **Research-panel degradation alarm (ADR-08)** — non-zero exit code 3 + aggregate
   banner on insufficient provider success is intentional design, not a bug. Retune
   only after consulting ADR-08.

---

## Deferred Items (not yet committed)

- `datetime.utcnow()` deprecation sweep — identified during code review of Perplexity
  work; not executed. No commit exists. Carried as Directive #2.
- `[scope: X]` tag backfill in LESSONS.md — some entries lack tags. Carried as
  Directive #3.
- Hyphen filename compliance check — likely low-impact per prior audit; not run.
  Carried as Directive #4.

---

## Rationale

Three pieces of reasoning from recent work shape the current state:

**Why billing exhaustion is a distinct error category.** A debate-mode provider
failure was traced to an exhausted Anthropic API credit balance, not a code defect.
A generic classification would have buried this, sending future debugging toward
phantom code bugs. Distinct classification makes the real cause legible at a glance.

**Why the provider health gate is scoped to the active mode.** The original global
gate would block research-mode runs whenever Anthropic providers failed (e.g. on
exhausted credits), even though research mode uses no Anthropic providers. Scoping
the gate to the active mode means each mode only health-checks the providers it
actually uses. For research mode, the summarizer outage is non-fatal (run degrades
gracefully).

**Why the Perplexity timeout is 240s.** A live reproduction measured a real research
query completing at roughly 68 seconds — over the prior 60s ceiling that caused
intermittent timeouts. 240s chosen with variance buffer because: (a) single data
point with unknown variance; (b) a higher ceiling is nearly free since providers
run in parallel; (c) Perplexity is a priority provider; (d) bias is against false
timeouts. SDK-level single transient retry added alongside, mirroring the OpenAI
research provider pattern. Test asserts `>= 120` not literal `240` — guards
regression without blocking deliberate retuning.

---

## Stage 3 Verification Summary

### VERIFICATION FAILED — Directive #1: AGENTS.md existence

**Architect claim (stage2-response.md):** "Verify: the repo file tree confirms
`AGENTS.md` does not currently exist."

**Stage 3 finding:** `AGENTS.md` IS present in `git ls-files` and was last updated
2026-05-17. It is fully populated with conventions, build/test commands, and Codex
constraints. The architect's DIRECTIVE #1 framing (create AGENTS.md) is **obsolete**.

**Impact on action plan:** Directive #1 revised from "Create AGENTS.md" to "Review
AGENTS.md for currency" — verify it reflects the provider-reliability changes from
recent commits (billing classifier, mode-scoped health gate, Perplexity timeout).

---

### VERIFICATION FAILED — Directive #3: ADR-46 audit check

**Architect claim (stage2-response.md):** "Verify: the ADR-46 dated-entry audit
check resolves from WARN to clean."

**Stage 3 finding:** The `check_dated_entries_format` audit check was **WITHDRAWN**
per Council Simplification 2026-05-16 and removed from `scripts/audit.py`. No such
check exists. The verification step cited by the architect is not actionable.

**Impact on action plan:** Directive #3 verification step revised — the [scope: X]
backfill is still cosmetically valid, but verification is by visual inspection only.
There is no automated gate to "pass."
