# AX9-5 re-run — organ calls vs raw searches, measured with the guard's declared escape

**Date:** 2026-09-18 · **Order:** `DECLARE-BATCH-AC-CLOSE-2026-09-18` §5 P1 · **Seat:** primary, worktree
`ac-close-followups` · **Supersedes the number in:** `2026-09-18-census-lane-ac-694-organ-call-census.md`
(branch `worktree-lane-ac-694-insurance-census`, commit `9bbb4d89`), which reported the count BLOCKED.

## 1 · Verdict

**The measurement is no longer blocked, and organs are used.** Over the last 14 days, across 215
sessions with a classified call, the harness made **2,230 raw-search calls** and **2,759 organ
invocations** (strict count; 5,818 by the organ's own lenient count). The median session makes
**0.67 raw searches per organ invocation**. **36 of 215 sessions (17 %) invoked no organ at all.**
ac-694's "4,482 raw scans vs 0 organ calls" was an artifact of how it searched, as that audit itself
suspected. It is not a measurement.

## 2 · The escape: works on a single segment, defeated by a pipe

The order said to stop if the escape was defeated again. **It was not defeated in the form the census
needed**, so the measurement ran. Both halves were witnessed live in this session:

| Command shape | Guard verdict |
|---|---|
| `rg --files-with-matches --stats "file_purpose_graph.py" <store> --glob "*.jsonl" # raw-needed: <reason>` | **ALLOWED** — 73 files, 1,377 matches |
| the same `rg -l …` then `\| wc -l # raw-needed: <reason>` | **DENIED** — and the refusal tells the caller to append the escape it already carries |

The rule in `deny_and_point.search_candidates` is that a declaration attaches to the **last command on
its line**. A pipe therefore leaves the search segment undeclared. That rule is documented and
deliberate, but the refusal text does not know it. On a piped search it tells the caller to "append
`# raw-needed:`", which the caller has already done. **Finding F1 (teaching defect):** the refusal
should say *"the declaration covers only the last segment; move the search to its own line or drop
the pipe."* This is a text fix, not a posture change.

## 3 · The organ already existed — and the census did not use it

`scripts/organ_usage_metric.py` is **AX9-5's own organ** (`[#694]`, AMEND-BATCH-X-ROSTER-009 Part 9).
It classifies every `tool_use` block in the session transcripts per call, which is what AX9-5 asks
for. ac-694's census grepped the transcript store instead, and the organ-use guard then refused it.
That is the loop this re-run breaks. **Finding F2:** a census lane was contracted to measure organ use
and never looked the organ up in `ecosystem/organ-index.md` or by name. The "organs first" order
exists for this case.

Running the organ surfaced three defects. None blocks the number above, because §4 controls for all
three:

- **F3 — worktree scoping silently empties the corpus.** Run from a worktree, the default repo root
  resolves to the worktree. `_session_dirs` then matches only that worktree's own transcript
  directory: **1 session, and 164 of 171 organs reported UNCALLED**. With
  `--repo-root <primary>`: **865 sessions**. An "uncalled" list produced this way is false and gives
  no warning (memory: `worktrees-in-a-skip-set-empties-the-live-corpus` class).
- **F4 — totals are all-time.** `--days` windows only the uncalled list. `totals` and the per-session
  tallies cover every transcript on disk, so "the last two weeks", AX9-5's own window, is not
  expressible through the CLI.
- **F5 — a mention counts as a call.** `classify_tool_call` returns `organ_call` for any shell command
  whose text contains an organ path, so `git add scripts/x.py`, `sed -n … scripts/x.py` and
  `cat scripts/x.py` all count. The lenient count (5,818) is 2.1× the strict count (2,759).

## 4 · Method (re-runnable)

A thin wrapper **reuses the organ's own reader, classifier, organ set and session-directory matcher**
(`_iter_tool_calls`, `classify_tool_call`, `known_organs`, `_session_dirs`) and adds only three
controls:

1. `--repo-root` pinned to the primary checkout (controls F3): **362 transcript directories** (primary
   plus every worktree), **226 transcripts with a call in the window**.
2. A per-call timestamp window of 14 days, from each record's own `timestamp` (controls F4).
3. A **strict** leg: an organ counts as invoked only when it appears in the same command segment as an
   interpreter token (`python`, `uv run … python`, `py -m`, `pwsh`, `powershell`, `bash`) (controls F5).

Raw search = the organ's own rule: the `Grep` tool always, or a shell line headed by a search tool
(the same head vocabulary `deny_and_point.SEARCH_HEADS` uses).

## 5 · Numbers

| Measure (14 d, 2026-09-04 → 2026-09-18) | Value |
|---|---|
| Raw-search calls | 2,230 |
| Organ calls, lenient (the organ's own classifier) | 5,818 |
| Organ invocations, strict | 2,759 |
| Sessions with ≥1 classified call | 215 |
| Median raw-per-strict-organ ratio, per session | 0.67 |
| Sessions with zero strict organ invocations | 36 |

**The five organs AX9-5 names (strict invocations, 14 d):** `gen_task_tree` 343 · `graph_queries` 121 ·
FPG-1 (`file_purpose_graph.py`) 71 · `decision_coverage` 42. The **orphan census** has no file of its
own: it is a `graph_queries` verb plus the `graph-orphan-census` pre-commit id, so its invocations are
inside the `graph_queries` figure and cannot be separated.

## 6 · Organs not invoked in 30 days (strict), 54 of 171 known

Read this list by kind. Most of it is structural, not neglect:

- **Not invocable through an interpreter, so this method cannot see them (29):** the 10 command and
  skill files (`.claude/commands/*.md`, `.claude/skills/*/SKILL.md`, the two plugin commands),
  because slash commands leave no `python …` line. Also 19 `scripts/audit_checks/*.py` modules,
  imported by `audit.py` and never run directly.
- **Package internals (8):** `scripts/codemap/*` (6) and `scripts/toc/{__init__,check}.py` (2), reached
  through `codemap_hook.py` / `toc_hook.py`.
- **Git-hook entry points (7), uncalled because their gate is `stages:[manual]`:**
  `block_commit_on_main.py`, `check_backlog_commit_msg.py`, `check_backlog_filing.py`,
  `coherence_nudge.py`, `normalize_headers.py`, `validate_prepend_order.py`,
  `plugins/tier1-lifecycle/scripts/validate_backlog.py`. This is the same shape as W5: **the organ
  exists, and nothing reaches it.**
- **Directly invocable and genuinely uncalled (10):** `backlog_source.py`, `changelog_sentinel.py`
  (its SessionStart hook is disabled), `coherence_enumerator.py`, `enforcement_coverage.py`,
  `fleet_analytics.py`, `gitenv.py`, `governance_health.py`, `reverse_dep_oracle.py`,
  `validate_doc_code_edge.py`, `validate_no_ff.py`.

## 7 · Anti-claims

- Transcripts record local Claude Code sessions only. Browser seats, cloud Routines and git-hook
  firings are invisible here, as ac-694 stated.
- The strict leg can miss an organ invoked through an alias or a wrapper script. That biases the
  organ count **down**, so the raw/organ ratio is if anything an upper bound.
- Raw searches are not screened for "an organ would have answered this". The 2,230 includes
  legitimate raw needs, for example the one this audit declared.
- A `--bg` lane's transcript files under its launcher's directory
  (`session-store-tally-is-per-directory-not-per-lane`), so the per-session ratio mixes lanes into
  their launchers.

## 8 · Proposed rows (filed with this window's rows)

F1 (refusal teaching text on piped searches) and F3–F5 (the organ's scoping, window and mention-as-call
defects) are filed as one row against `scripts/organ_usage_metric.py` / `scripts/hooks/deny_and_point.py`.
F2 is a dispatch-contract lesson, recorded here and not rowed.
