---
id: "[#1574]"
title: "A Copilot child run is not recorded as a wedged seat, and its Stop hook resolves a real path"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1574] [P2][S] **A Copilot child run is not recorded as a wedged seat, and its Stop hook resolves a real path** - a Copilot CLI child fires the repo SessionStart hook, the row takes the parent's `CLAUDE_PID` with empty `transcript_path` and reads `wedged`, which reds `handoff_probes BD-seats`; under Copilot the empty `$CLAUDE_PROJECT_DIR` makes the Stop hook path `C:\scripts\...` (`to-browser/SESSION-lane-bu-863-prompts-guard.md:~74-98`; to-browser/SESSION-integrator-bu-2026-10-15.md:135). The memory note `which-non-claude-clis-honour-claude-settings-json` is also wrong for Copilot 1.0.98 · Done when: RED first: (1) `record_event` declines a payload with no `transcript_path`, asserted by a test; (2) a test runs the Stop hook with empty CLAUDE_PROJECT_DIR and asserts it resolves the repo-relative script; fails on 97bcd374 · touches: `scripts/seat_registry.py`, `.claude/settings.json`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#833]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
