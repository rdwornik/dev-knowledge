---
id: "[#518]"
title: "`scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row because they are one fix."
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#518] [P2][S] **`scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row because they are one fix.** (a) it runs with `cwd=` but no `env=` while the module imports `gitenv` at module level, so `GIT_DIR` makes it read repo A while labelling the answer repo B; the worst of six call sites feeds `check_silent_rule_ratchet`'s BASELINE read, so a confidently wrong baseline reads as valid — and lane worktrees export `GIT_DIR` absolutely, so it fires in every lane commit. (b) `text=True` with no `encoding=`/`errors=`: UnicodeDecodeError is a ValueError and escapes the function's own handler, so under `core.quotePath=false` the blocking `audit-health` gate dies with a traceback instead of returning a verdict — every other git call in the file already decodes explicitly, making this the outlier. UNOWNED: [#396] and [#512] both closed and neither covered this helper. Fix with the fifth scrub copy in `gen_handoff.py` and `gitenv.py`'s missing `timeout=`. · Done when: the call site scrubs the environment and decodes explicitly, with a test reproducing each defect first · refs N4-F1/F6/F5/F12 · kill-candidates: none — [#396]/[#512] closed, neither covered this helper
