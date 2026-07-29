---
id: "[#445]"
title: "`codex-review` wrapper path-guard reports SUCCESS having reviewed nothing"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#445] [P2][S] **`codex-review` wrapper path-guard reports SUCCESS having reviewed nothing** — third instance of the [#431] wrapper family, and the one that makes the failure *silent*. A **docstring-only `.py`** is prose wearing a code extension: the path-guard filters a mixed diff to the code subset, routes it to the CODE profile, and reports **success** — the prose subset is not doc-reviewed and nothing at run time says so. Witnessed 2026-07-29 (morning batch): the fix diff carried a docstring-only `review_closures.py`, so the doc lane had to run ad-hoc via `codex exec` — see the invocation note in `docs/audits/2026-07-29-codex-postflip-fix-batch-review.md`. Scope is the MECHANISM: the guard either **fails loud** on a mixed diff or routes the prose subset to the doc profile; a silent success is the defect. · Done when: a mixed diff can no longer report as reviewed while its prose went unreviewed — fail-loud or dual-route — with a test seeding a docstring-only `.py` beside prose · refs [#431], `~/.claude/bin/codex-review.ps1` · kill-candidates: none — [#431] is a sibling defect in the same wrapper, not a duplicate · serialize-group: codex-review
