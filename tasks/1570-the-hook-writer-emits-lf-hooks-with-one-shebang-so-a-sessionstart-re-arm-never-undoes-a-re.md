---
id: "[#1570]"
title: "The hook writer emits LF hooks with one shebang, so a SessionStart re-arm never undoes a repair"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1570] [P1][S] **The hook writer emits LF hooks with one shebang, so a SessionStart re-arm never undoes a repair** - `.git/hooks/{pre-commit,commit-msg,pre-push}` are rewritten CRLF with a doubled shebang by the arm/`pre_commit install` writer (to-browser/SESSION-integrator-bu-2026-10-15.md:114; `to-browser/SESSION-lane-bu-1537-codespace-finish.md:171`); `[#282]` `[#471]` `[#485]` `[#1341]` cover generators, not hooks · Done when: RED first: a test runs `arm_hooks.py` twice into a temp hooks dir on a CRLF-autocrlf config and asserts each hook has no `\r` and exactly one `#!` line; fails on 97bcd374 · touches: `scripts/hooks/arm_hooks.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1341]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
