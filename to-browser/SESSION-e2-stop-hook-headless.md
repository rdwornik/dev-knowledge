carried-by: OPEN
kind: SESSION
date: 2026-10-21
by: lane head claude-sonnet-5-5 medium (this session), implement + RED by Copilot CLI

# SESSION e2-stop-hook-headless

Value: a dirty-ended headless turn now costs 1 model call. Witness on a dirty clone: 88,770 tokens before, 44,187 / 44,220 after (calls inferred, see item 6).

## Summary (item by item)

- **0 REUSE CHECK.** Quoted: the marker/state mechanism in the hook is `_record_seat_stop` -> `seat_registry.record_hook_event` (`scripts/session_end_backpressure.py:553-570`, `scripts/seat_registry.py:101` `REGISTRY_PATH = ~/.claude/seat-registry.jsonl`, `:268`). It is an append-only EVENT log that writes one `Stop` row per Stop; it records no "nudged" fact, and carrying one needs a registry schema change in a file this lane does not own (`scripts/seat_registry.py` is outside "Files you own"). So the once-per-session marker is genuinely new: one empty file per session under `<tmp>/dk-session-end-backpressure` (override env `SESSION_END_BACKPRESSURE_MARKER_DIR`), outside the repo. The existing fire-once branch (`main()` `if data.get("stop_hook_active") is False`) is reused and kept. Existing tests extended: `tests/test_session_end_backpressure.py` (one autouse fixture). Missing: a headless discriminator and a per-session guard.
- **1 Read.** Row [#1700], source bisect Item 5, the hook, the tests, docs (code.claude.com hooks page, first 100k chars: it does not document `CLAUDE_CODE_SESSION_ATTENDED`, `CLAUDE_CODE_ENTRYPOINT`, or a headless marker). The file contradicted itself (docstring says `stop_hook_active` is sent, `_read_hook_input` says it is not): MEASURED, it IS sent (false on a fresh Stop) on CC 2.1.306. Docstring corrected.
- **3 Capture (CC 2.1.306, throwaway `--settings` file with `disableAllHooks:false`, because user-level `~/.claude/settings.json:30` has `disableAllHooks: true`; no global edit made).**
  - (a) `claude -p ... --output-format json --model claude-sonnet-5-5`: stdin keys `background_tasks,cwd,effort,hook_event_name,last_assistant_message,permission_mode,prompt_id,session_crons,session_id,stop_hook_active,transcript_path`; `stop_hook_active=false`; env `CLAUDE_CODE_ENTRYPOINT=sdk-cli`, `CLAUDE_CODE_SESSION_ATTENDED=0`, `CLAUDE_CODE_CHILD_SESSION=1`.
  - (b) `claude --bg`: same keys plus `scratchpad_dir`; env `CLAUDE_CODE_ENTRYPOINT=cli`, `CLAUDE_CODE_SESSION_ATTENDED=0`, `CLAUDE_JOB_DIR` set. (Run from this worktree: the scratch folder was an untrusted workspace and `--bg` refused it.)
  - (c) interactive terminal: **UNMEASURED** (a bg lane cannot drive one).
  - Discriminator picked: env `CLAUDE_CODE_SESSION_ATTENDED`. Stdin has NO headless marker. Contract rule for an unmeasured interactive state applied: silent unless the var is exactly `"1"` (assumed interactive value); any other state is silent.
- **4 RED first (Copilot wrote, I ran `-n0`).** Round 1 on base `3906829bb`: `5 failed, 9 passed` (test_headless_p_is_silent, test_bg_is_silent, test_interactive_once_per_session_id, test_attended_var_absent_behaves_like_interactive, test_retry_suppressed_and_records_no_marker), committed `258a95975`. After the verifier flagged that round-1 spec inverted the contract's fallback rule, round 2 changed the spec (fixture sets ATTENDED=1, absent/odd values silent) and RED was re-recorded: 6 failed (`test_attended_var_absent_is_silent`, `test_non_exact_attended_values_are_silent[ , true, " 1", 01, 2]`), commit `6d1d14d62`. Covers (a) headless silent, (b) same `session_id` silent / new id once, (c) existing tests unchanged (only an autouse env fixture added), (d) bad stdin and unwritable marker dir fail soft.
- **5 Fix** (`scripts/session_end_backpressure.py`, stdlib `tempfile` only): `_is_provably_interactive()` gate in `main()` after `_record_seat_stop`, before any git call; `_claim_nudge()` atomic `O_EXCL` marker claim before printing; marker filename `s-<sanitised id>`. Advisory text and hard-leg semantics untouched. Commits `f16387533`, `2ed67e159` (atomic claim, both reviewers), `44c567833` (contract rule), `3356e9b4c` (dot-id, final code tip). Final: `77 passed` (headless + existing files, `-n0`), `ruff` clean.
- **6 Real-use witness.** See EVIDENCE. Probe `claude -p "Reply with OK." --output-format json --model claude-sonnet-5-5` from a dirty throwaway clone (untracked file; branch hook copied over the clone's): BEFORE (base hook) usage legs sum 88,770 (in 6, out 225, cache_read 64,832, cache_write 23,707), reply was the hook-induced note about the dirty tree; AFTER (branch hook) 44,187 (in 2, out 4), reply `OK`; AFTER on the final tip 44,220. NOTE: `usage.iterations` listed ONE entry and `num_turns` 1 in both BEFORE and AFTER, so "calls" is inferred from the usage legs (about 2x), not read from iterations. Clone removed, removal verified; no marker dir created in `%TEMP%`.
- **7 Boundaries.** Rows: none filed or closed. [#739] untouched.
- **R.** Exercised for real: the `claude -p` probe above (hook fired for real, `CLAUDE_CODE_SESSION_ATTENDED=0` set by the CLI itself). The interactive path is covered by unit/e2e tests only, never by a real interactive Stop (UNMEASURED).
- **T Teaching.** No process changed, teaching unchanged: the only docs naming the hook (`.claude/BOOT-REFERENCE.md:38`, `templates/CONTRIBUTING-md-template.md:152`) say it is wired and advisory, not when it nudges.

## MODELS

```
MODELS:
plan: requested=in-contract served=n/a
implement: requested=copilot-cli(default) served=claude-sonnet-5.5 (usage-output-file currentModel, 4 runs: impl, impl2, impl3, impl4)
red: requested=copilot-cli(default) served=claude-sonnet-5.5 (2 runs: red, red2)
lane head: requested=claude-sonnet-5-5/medium served=claude-sonnet-5-5
review-codex: requested=gpt-5.6-terra served=gpt-5.6-terra (banner line `model:` in both runs; round 2 self-described "MODEL: gpt-5", a note per R162)
review-copilot: requested=copilot-cli(default) served=claude-sonnet-5.5 (2 runs)
isolated verify: requested=claude-sonnet-5-5/medium served=claude-sonnet-5-5 (modelUsage key, 2 runs)
```

## SPEND

- SPEND: claude -p / --bg probes + witness + 2 verifier runs: about USD 0.93 list (witness 0.1666+0.1036 BEFORE, 0.1056+0.1058 AFTER; verifier 0.1420 + 0.1872; captures about 0.09); lane-head tokens not itemised. Under the USD 6 stop.
- SPEND: Copilot CLI premium requests: 8 (red, red2, impl x4, review x2). Codex: 2 read-only runs.

## Reviews (served model + nonce, round 1 on tip `f16387533`, round 2 on `44c567833`)

Round 1 (diff sha12 `25f5b6b67292`): Codex gpt-5.6-terra nonce RVW-CODEX-7f3a91; Copilot claude-sonnet-5.5 nonce RVW-COPILOT-c20be4.
Round 2 (diff sha12 `0bd12e99d9a9`): Codex gpt-5.6-terra nonce RVW-CODEX-b81d02 (returned `0BD12E99D9A91`); Copilot claude-sonnet-5.5 nonce RVW-COPILOT-5ae7f6.

| # | reviewer | sev | class | location | disposition |
|---|---|---|---|---|---|
| 1 | Codex r1, Copilot r1 | major | functional: logic | `main()` check-then-touch non-atomic | fixed in `2ed67e159` (`_claim_nudge`, O_EXCL before print) |
| 2 | Copilot r1 | major | functional: check | headless return might skip seat recording / hard leg | false positive: `_record_seat_stop` (`:~619`) runs before the gate; `_HARD_CHECKS = ()` since ADR-85 A5; comment added in `3356e9b4c` |
| 3 | Codex r2 | major | functional: check | `:581` "."/".." id -> FileExistsError -> silenced; dot test red on Linux | fixed in `3356e9b4c` (`s-` prefix) |
| 4 | Codex r2 | major | functional: resource | `SESSION_END_BACKPRESSURE_MARKER_DIR` could point into the repo | deferred: operator-controlled env seam, default is `%TEMP%`; tests assert the tree stays clean |
| 5 | Codex r2 | major | functional: logic | marker mkdir/open failure returns True (prints every Stop) | deferred, deliberate: contract (4d) requires fail soft; worst case is today's behaviour in an interactive session |
| 6 | Copilot r1/r2 | minor | functional | markers never cleaned up; shared predictable tmp dir; sanitiser collisions (`a/b` vs `a_b`) | deferred: session ids are UUIDs, OS clears tmp, impact is a lost nudge |
| 7 | Copilot | minor | evolvability | stale in-function comment, mid-file `import pytest`, fail-soft test does not assert empty stdout | stale comment fixed `3356e9b4c`; rest deferred |

## Isolated verifier (R147), saw ONLY the contract and the diff

Served `claude-sonnet-5-5`. Round 1 (nonce VER-9d41) FAIL: major, fix inverted the contract's fallback rule (silent unless provably interactive) -> fixed by respec in `6d1d14d62` / `44c567833`; major, second marker store without REUSE CHECK -> justified in item 0; minor test gaps. Round 2 (nonce VER-3c88, diff sha12 `0bd12e99d9a9`) FAIL on: F1 "."/".." ids (real; fixed `3356e9b4c`), F2 reuse justification (item 0 above, the verifier could not see this file), F3 hard leg under ATTENDED=0 unverifiable from the diff (`main()` has no hard leg, `_HARD_CHECKS = ()`; no test added, deferred), F4 interactive `"1"` unmeasured (flagged here). No third verifier round was run on `3356e9b4c`; its only delta from round 2 is the `s-` prefix and two comment lines.

## CI (branch tip `3356e9b4c`, run 39603638017, conclusion failure)

`gh run view 39603638017`: plan, ruff, tier1, spine, seal, handoff-manifest, anchor, terra, phase-gate, windows-gate pass; commit-gate, ship-gate, pytest (ubuntu-latest), gate fail. `known-reds-compare.out` verdict `FAIL -- REGRESSION -- 5 failure(s)` (baseline 2026-10-04-fdf4f4952211; 39 failed / 3 errors in the pytest run). None of the 5 is a test of the files I changed (all 22 + existing hook tests pass in CI):
- `tests/test_check_derived_copies.py::test_self_gated_rows_pass_on_the_current_tree` and `::..._verdict_is_the_same_on_a_lane_that_adds_a_test@branch_context`: **lane-caused, expected**: `ecosystem/doc-counts.md` collected-test-count is stale because this lane adds tests; the integrator regenerates it at the merge (no-regeneration order). 
- `tests/test_onboarding_items.py` x3 (`test_a_fresh_seat_finds_all_13_onboarding_items`, `test_a_warm_bundle_is_filled...`, `test_an_architect_paste_carries_no_probe_table...`): **branch-state**: `gen_handoff.PreflightError` on `journal_anchored: 1 unanchored spine entr(ies): 6106a05c`, which is main's own merge of `worktree-e2-test-flow-metrics` (`origin/main` tip when the run started), not a commit of this branch. Main's latest conductor run (push, 39602107786) concluded success.
- commit-gate / ship-gate failures not itemised further; both ran the same gates over a range containing the docs-count drift above. Not investigated beyond the verdict.

## READY-TO-FILE (not filed, rows barred)

- Interactive path UNMEASURED: if a real interactive CC session does not set `CLAUDE_CODE_SESSION_ATTENDED=1`, the hook now never nudges there. Owner action: run one interactive Stop with the capture hook (`dump.py` recipe below) and confirm the value; if different, change `_is_provably_interactive()` only.
- `usage.iterations` / `num_turns` of `claude -p --output-format json` do not count Stop-hook continuation calls (1 entry both before and after); the row's "calls = iterations[0]" witness is unreliable, use the usage legs.

## EVIDENCE

```
capture -p : stdin keys background_tasks,cwd,effort,hook_event_name,last_assistant_message,permission_mode,prompt_id,session_crons,session_id,stop_hook_active,transcript_path ; ENTRYPOINT=sdk-cli SESSION_ATTENDED=0
capture bg : same + scratchpad_dir ; ENTRYPOINT=cli SESSION_ATTENDED=0 CLAUDE_JOB_DIR set
RED r1 (base 3906829bb): 5 failed, 9 passed in 66.33s
RED r2: 6 failed (attended-absent, 5 non-exact values) ; copilot served claude-sonnet-5.5
GREEN: uv run --locked pytest -n0 -q tests/test_session_end_backpressure_headless.py tests/test_session_end_backpressure.py -> 77 passed (223s) ; ruff: All checks passed!
WITNESS BEFORE (base hook, dirty clone): usage_sum=88770 in=6 out=225 cread=64832 cwrite=23707 iterations=1 num_turns=1 cost=0.1036
WITNESS AFTER  (branch hook)           : usage_sum=44187 in=2 out=4 cread=18239 cwrite=25942 result=OK cost=0.1056
WITNESS AFTER  (final code tip 44c5678): usage_sum=44220 out=4 result=OK
clone removed: "clone exists: False" ; %TEMP%\dk-session-end-backpressure exists: False
CI 39603638017 (tip 3356e9b4c): failure ; known-reds-compare: 5 REGRESSION (2 doc-counts lane-caused, 3 onboarding branch-state 6106a05c)
```

HANDBACK worktree-e2-stop-hook-headless @ 3356e9b4c code
