---
id: "[#458]"
title: "PLAYBOOK candidate note — gates and commits never run concurrently in one tree"
status: closed
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
serialize-group: playbook
generates: BACKLOG.md
---

- [#458] [P3][S] **PLAYBOOK candidate note — gates and commits never run concurrently in one tree** — witnessed 2026-07-31 ([#382] W3 boundary): a background full-suite run raced a JOURNAL commit in the same checkout and produced a phantom failure (`test_check_selects_correctly_under_inherited_git_dir` — a test spawning git while pre-commit's stash/restore ran); clean rerun PASSED. Same family as the pre-commit-stash and GIT_DIR gotchas but a distinct rule: a long gate/suite run and a commit are mutually exclusive IN THE SAME TREE — sequence them, or run the suite in a worktree. Grep-verified: PLAYBOOK Ch8 covers session/merge concurrency, not this. PLAYBOOK edit deferred out of the [#382] arc (freshness-restamp discipline; genuine re-read owed). · Done when: the note lands in PLAYBOOK Ch8 (or the gotchas skill, whichever the review picks) with the witness cited, and the PLAYBOOK freshness stamp rides a genuine re-read · refs protocols/PLAYBOOK.md Ch8, JOURNAL entry (p), ~/.claude/skills/gotchas · kill-candidates: none — no open row owns this lesson; [#457] owns the test-side defects, not the process rule · serialize-group: playbook
