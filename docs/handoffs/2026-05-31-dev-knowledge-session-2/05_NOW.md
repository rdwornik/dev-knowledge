# 05 · What to do now

## Immediate objective

No work is mid-flight — the handoff skill saga is fully closed and merged. The
natural next move is the operator's call among three; **proposed sequence below, not
a forced rank.** Scope of likely next work: docs/process/governance (not code).

**Sage's recommendation (carry forward):**
- **(a) Close the matrix-validation loop — 10 min.** After this bundle merges, invoke
  `please create handoff for dev-knowledge` again. *Note:* merging this bundle adds
  commits, so the next invocation will land in **Case 4 again** (new commits + slug
  exists) → another counter-suffix, **not** the Case 5 clean-exit. To actually
  exercise **Case 5** you need a state with *zero* commits since the last bundle.
  Either outcome is a question-free pass — just know which you're triggering.
- **(b) Universalization roadmap — the strategic direction (multi-week).** Start with
  **memory-management hardening** (foundational — if memory drifts, everything
  downstream degrades, WC6). Then: ecosystem-folder continuous-audit design (Council
  scope — genuine open question), AI Council operational write-up, playbook hooks,
  skills-review cycle, harness formalization.
- **(c) Lightweight housekeeping (Sonnet/medium).** Doc-truth sweep, the v4.3.1 P3
  refinement batch, branch cleanup. Clears debt before (b).

## Top priorities (from BACKLOG)

- **[P1] Adversarial fresh-eyes pass in routine handoff generation** — extend
  triangulation from the promotion gate to *every* handoff (routine bundles still ride
  on Phase-2 self-verification — the ~25% insider blind spot the v4 arc disproved).
  Council scope; pairs with `protocols/AGENT_FRAMEWORK.md` v0.1 stub.
- **[P1] Council decisions management consolidation** — contradiction-detection +
  ownership model (amendment vs new ADR) as ADR count grows. The **ADR-62-relaxes /
  ADR-63-gates ML-2 tension** is a live example needing a reconciling principle (P3).
- **[P1] Sacred-files maintenance enforcement** — canonical files drift stale at
  session boundaries; need a mechanism (staleness hook / session-end check). Pairs
  with the [P2] hooks-audit track.
- Full queue in `BACKLOG.md` — do not duplicate it here.

## In-progress branches & repo state

- `main` → `f7de267` (comprehensive matrix merged).
- `docs/handoff-session-2-2026-05-31` → this bundle's branch (Phase 1 `a21e355` +
  the Phase-2 bundle commit). **Merge to main after review.**
- `feat/handoff-skill-comprehensive-fix-2026-05-31` → `93c3ce9`, already merged to
  main; safe to delete.
- **Branch:** `docs/handoff-session-2-2026-05-31` · **HEAD:** `a21e355`
- **Working tree at generation:** clean (Phase-1 interview committed; bundle commit follows).

## Boundaries

- **Do NOT create new folders / naming / conventions without checking the existing
  one first** (W6 — operator standing rule, violated 3× this arc).
- **Do NOT ship partial fixes** — enumerate all cases upfront; a third "small fix" on
  one surface means STOP and design comprehensively (W1).
- **Do NOT edit another repo** from here (ADR-41) — `ai-council`/`corp-monorepo` work
  routes through their own sessions.
- **Do NOT touch `OneDrive - Blue Yonder` paths** (hard exclusion).
- **Do NOT propose "rest / later / next session"** unprompted (W10).
- Looks-wrong-but-intentional: JOURNAL gaps from reverted auto-scope entries (revert
  `0c98611` documents them); slug `-2` is differentiation, not retry.

## How to choose

If you face multiple candidate first-moves, **propose your choice with rationale** —
don't ask Rob to forced-rank. Operator energy is finite; reasoned pre-selection is
your job. Rob confirms or redirects.
