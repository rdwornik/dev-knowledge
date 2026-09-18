---
id: "[#900]"
title: "AX9-5's own organ miscounts -- from a worktree it reads one session, its totals ignore the window, and a path mention counts as a call"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#900] [P2][S] **AX9-5's own organ miscounts -- from a worktree it reads one session, its totals ignore the window, and a path mention counts as a call** - Found while re-running AX9-5 under ruling P1 (`docs/audits/2026-09-18-census-ax9-5-organ-use-rerun.md`). The re-run used `scripts/organ_usage_metric.py`, the organ built for AX9-5, which batch AC's census never looked up. It has three defects, plus one teaching defect in the guard. (F3) Run from a worktree, its default root resolves to the worktree, and `_session_dirs` then reads only that worktree's transcripts: **1 session, and 164 of 171 organs reported UNCALLED**, against **865 sessions** from the primary. The false list comes with no warning. (F4) `--days` windows only the uncalled list, while `totals` and the per-session tallies are all-time, so AX9-5's own two-week window cannot be expressed. (F5) `classify_tool_call` counts any shell command whose text contains an organ path as an `organ_call`, including `git add`, `sed -n` and `cat`, which is 5,818 lenient against 2,759 strict over 14 d. (F1) `deny_and_point.py`'s refusal of a PIPED search tells the caller to append `# raw-needed:`, but the declaration covers only the last segment, so a caller who already appended it is told to do what they did · Done when: (1) the organ resolves the primary checkout's root from a worktree, or refuses rather than reporting a partial corpus. (2) `--days` windows the counts as well as the uncalled list. (3) The organ leg counts invocations: an organ in an interpreter's segment, not a mention. (4) The piped-search refusal names the last-segment rule. Each lands with a RED-first test · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `scripts/organ_usage_metric.py` (`organ_usage_report`, `classify_tool_call`, `_session_dirs`), `scripts/hooks/deny_and_point.py` (`search_candidates`), `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §5 P1, `[#694]` (owns AX9-5's metric clause), `[#685]` · kill-candidates: `[#694]` -- its Done-when already owns "raw-search calls vs organ calls per session, and organs never called in 30 days"; fold (1)-(3) into it at intake and keep (4) here
