---
id: "[#1346]"
title: "The surface_triage SessionStart hook has no stated posture in bounded_hook"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1346] [P2][S] **The surface_triage SessionStart hook has no stated posture in bounded_hook** - `tests/test_bounded_hook.py` (three tests) refuses the live settings: "[hook-bound] REFUSED SessionStart: uv run --locked python \"$CLAUDE_PROJECT_DIR/scripts/surface_triage.py\" -- no stated posture in bounded_hook.POSTURES". A hook is wired in `.claude/settings.json` with no posture, so the bounding check cannot say whether it fails open or closed. Both legs, every recent run; registered pre-freeze under lane-end-hook without an owner · Done when: `bounded_hook.POSTURES` carries a stated posture with a reason for the `surface_triage.py` SessionStart hook, every registered hook resolves, and the three tests are green on both CI legs · touches: `scripts/hooks/bounded_hook.py`, `tests/test_bounded_hook.py`, `.claude/settings.json` · kill-candidates: none -- [#863] is the suspended-process wedge, not the posture table · refs `scripts/hooks/bounded_hook.py`, `tests/test_bounded_hook.py`, `.claude/settings.json`, `scripts/surface_triage.py`, [#863] · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
