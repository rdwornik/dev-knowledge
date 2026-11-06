---
id: "[#1912]"
title: "gen_handoff --dry-cut renders a bundle outside a cut window (defect 23)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1912] [P2][S] **gen_handoff --dry-cut renders a bundle outside a cut window (defect 23)** - `--dry-cut DIR` is documented as skipping the cut-boundary gates, but it refuses on the preflight, including the cut-day rows ledger_refreshed and ratification_present that `--trial-cut` excludes as false-red outside a cut window, and git_hygiene; so no stage renders, assembles or byte-checks a bundle between cuts and ADR-132's third sample could not exercise them; `--repo` also defaults to the worktree directory name, so a cut worktree reads `LEDGER-handoff-<date>.md`. Defect 23 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - `--dry-cut` from a worktree with other linked worktrees and no ratification for the day renders and assembles a bundle into DIR, reporting the skipped rows; the default repo name is the primary checkout's directory name; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
