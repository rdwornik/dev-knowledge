---
id: "[#317]"
title: "Default-parallel test invocation + slow-tier markers"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
source: BACKLOG.md
derived: true
---

- [#317] [P2][M] Default-parallel test invocation + slow-tier markers — close the inner-loop serial tax left by #256/#260 (which parallelised only /ship's code path). Leg (a): point the per-step verify cadence at parallel — verify skill `pytest -x` -> `pytest -n auto --dist worksteal -x`, reconcile the CLAUDE.md §4 convention text (build steps). **Sub-decision D1 (OPERATOR-GATED, not a build step):** the same change to the GLOBAL core-invariant #2 is global infra (EXCEPTION-with-ruling per core-invariant #6) — needs an explicit operator ruling, never unilateral. Leg (b): add an orthogonal `slow`/`e2e` marker (distinct from `live_repo`) on the ~20-25 subprocess/git-spawning E2E tests carrying the runtime, enabling a `pytest -m "not slow"` default; keep the full-serial nightly (pyproject) as the xdist-masking catcher. · Done when: verify cadence parallel by default (or D1 operator-ruled) AND `slow` selects the E2E set AND the `not slow` run completes under 60s (measured time recorded at build) AND serial-nightly preserved · refs pyproject.toml, .claude/skills/verify/verify.py, #256, #278 · kill-candidates: none — extends the #256/#260 tiering arc
