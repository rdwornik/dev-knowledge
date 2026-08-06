---
id: "[#317]"
title: "Default-parallel test invocation"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#317] [P2][M] Default-parallel test invocation — close the inner-loop serial tax left by #256/#260 (which parallelised only /ship's code path). **NARROWED to leg (a): leg (b) is shipped** — the orthogonal `slow` marker is live at `pyproject.toml:61` ("the #317 marker tier"), so `pytest -m "not slow"` selects and the full-serial nightly is preserved. Leg (a), remaining: point the per-step verify cadence at parallel — verify skill `pytest -x` -> `pytest -n auto --dist worksteal -x`, reconcile the CLAUDE.md §4 convention text (build steps). **Sub-decision D1 (OPERATOR-GATED, not a build step):** the same change to the GLOBAL core-invariant #2 is global infra (EXCEPTION-with-ruling per core-invariant #6) — needs an explicit operator ruling, never unilateral. · Done when: verify cadence parallel by default (or D1 operator-ruled) AND the `not slow` run completes under 60s (measured time recorded at build) AND serial-nightly preserved · refs pyproject.toml, .claude/skills/verify/verify.py, #256, #278 · kill-candidates: none — extends the #256/#260 tiering arc
