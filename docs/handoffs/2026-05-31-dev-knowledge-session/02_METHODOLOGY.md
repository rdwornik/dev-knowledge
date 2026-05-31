# 02 · Methodology

<!-- scope: meta -->

> How work is done in `.dev-knowledge`. This is the standing
> methodology — read it before acting. Condensed from PLAYBOOK +
> ESSENTIALS at handoff time.

## The loop

1. **Understand** — read the relevant ADRs, protocols, and prior arc before changing anything.
2. **Plan** — state what you'll change and why; get operator sign-off on non-trivial work.
3. **Implement** — minimal diffs, matching conventions.
4. **Verify** — `pytest -x --tb=short`, `ruff check`, audit health gate (9/9).
5. **Capture** — JOURNAL entry (newest-first), LESSONS if a generalizable pattern emerged.

## Non-negotiables

- **Layer-2 never executes** — `.dev-knowledge` holds methodology + lightweight read-only validators (audit.py checks, codemap, hooks); no orchestration scripts (ADR-28/36).
- **Conventional Commits** — `feat/fix/docs/chore/refactor`; one logical change per commit; commit after every file edit (git-discipline rule).
- **Verify before claiming** — structured-claims discipline (ADR-58); never assert a number you didn't measure.
- **ADRs are immutable** — supersede with a new file; never edit a ratified decision in place (ADR-39).
- **Append-only** — LESSONS, TOKEN-LOG, JOURNAL; prepend newest-first where applicable (ADR-29).

## Triangulation (the v4 lesson)

Process versioning is gated on **fresh-eyes review** — an independent Opus 4.8 with zero project context reviews the artifact. Insider review alone caught ~25% of criticals; fresh-eyes caught 100%. Promotion criterion is **judgment-augmented**: <2 critical findings AND reviewer Stage-3 verdict PROMOTE/PROMOTE-WITH-CAVEATS (reviewer judgment overrides the count). Routine artifacts still ride on Phase-2 self-verification — a known gap (BACKLOG P1 "Adversarial fresh-eyes pass in routine handoff generation").

## Council + Codex

- **AI Council** — convened for architecture decisions (multi-model debate via the ai-council CLI). Transcript auto-routing is opt-in per-invocation (ADR-43 partial — untargeted debates still archive manually).
- **Codex** — reviews safety-critical changes per ADR-54 (foundational ADRs, executable code).
- **Path A exception** — for post-hoc records of an already-made + validated decision, the ADR may be written directly via CC rather than convening Council (precedent: ADR-62/63, 2026-05-30).

---

**Source:** condensed from `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md` at handoff time.
