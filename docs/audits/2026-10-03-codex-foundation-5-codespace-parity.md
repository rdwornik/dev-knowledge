# Review record — foundation-5-codespace-parity (grok-4.7, isolated read-only run)

Consumer: `LANE-FOUNDATION-foundation-5-codespace-parity` (batch FOUNDATION, Done-contract item 6 and common rules §5); the reviewed change is branch `worktree-foundation-5-codespace-parity` against `origin/main` `ce6ecb08`, run record `docs/audits/2026-10-03-technical-codespace-parity-run.md`, row `[#1335]` (not closed here).

## Substitution note

`SUBSTITUTION: codex terra -> grok-4.7 (Codex is at its usage limit until 2026-10-03 21:07 per the batch order's ruling (e); this review ran 20:29-20:35 local)`. Recorded, not hidden; never the producer's vendor (the producer is Claude) and never the implementing session.

- **Served model:** `~/.grok/sessions/<cwd>/01a10307-3de1-7532-ae69-ca43b6dba292/usage.json` → `primaryModelId: "grok-4.7"`, 8 model calls, 322,943 input / 2,165 output tokens (output contract: a non-empty result in the expected shape — a findings list ending in a `TALLY` line — met on attempt 3).
- **Isolation:** run from an empty folder under the job tmp holding only `diff.patch` (`git diff origin/main...HEAD`), the four changed files and the contract; `--tools read_file,list_dir` only; nothing modified.
- **Failure policy (R59), attempts:** attempt 1 (`--tools read_file,list_dir,grep`) stalled after ~3.5 min with no final message — its last event was a ripgrep search that timed out after 20 s (`exit_code -1`), then nothing for 8 min; stopped by pid. Attempt 2 (`--tools read_file,list_dir`) stalled after ~40 events, last event a read of a `gotchas` skill file picked up because the session's git root resolved to `~/.claude/`; stopped by pid. Attempt 3 added `--no-plan --no-subagents --max-turns 20` and a read budget in the prompt, and completed (exit 0). Two retries, the maximum; diagnosis: the headless Grok agent stalls mid-turn on a long exploratory read pattern, not on authentication, quota or input size.

## Findings and dispositions (P1s fixed; the rest recorded)

| sev | where | finding (reviewer) | disposition |
|---|---|---|---|
| P1 | `scripts/codespace_parity.py` `compare_cleanup` | prints PASS from caller-supplied booleans and timestamps; a hand-written `cleanup.json` passes while the Codespace is still listed | **FIXED.** `verify_cleanup` writes `listing_exit` and `ls_remote_exit`; `compare_cleanup` refuses a record without both at 0 (`test_a_hand_written_cleanup_record_without_read_evidence_is_not_a_pass`). Honest limit: a file can still be forged to carry the two zeros; the check refuses the accidental and the lazy case, not a determined one. |
| P1 | `run_check` | with both `--remote` and `--codespace`, the file wins and the Codespace is never contacted | **FIXED.** Both together is a typed `RemoteUnavailable` and no `gh` call is made (`test_both_a_remote_file_and_a_codespace_is_refused_not_silently_resolved`). |
| P1 | `tests/test_provision_sh.py` `_working_bash` | the probe decodes under a non-UTF-8 locale so Git Bash's output never equals `bash-ok`; the helper raises on the machine it fixes | **REFUTED, no change.** The probe prints ASCII `bash-ok`, which decodes identically under cp1252 and UTF-8; and the evidence is direct: `tests/test_provision_sh.py` 10 passed on this workstation through `memory_admission_gate.py run` after the fix (log `fix2.log`), and the run-2 local record shows both nodes `passed`. |
| P2 | `compare_gates` | PASS when both sides have empty `hooks` and `audit_health None` as long as `tests` is non-empty | **FIXED** (`test_a_record_whose_hooks_and_health_never_ran_is_not_a_pass`, both sides). |
| P2 | `compare_transport` | a read that never ran yields NOT-RUN with a `read: PASS` evidence token | **REFUTED for the verdict, test added.** With `rclone` present and `read_exit None`, `read_exit != 0` is true, so the verdict is FAIL and the evidence reads `read: FAIL`; `test_an_rclone_read_that_never_ran_is_a_fail_not_a_read_pass` pins it (it passed on first run, which is the refutation). |
| P2 | `tests/test_codespace_parity.py` | `assert DECLARED_OS_CASES == {} or all(...)` short-circuits on the empty dict, so a later bare forgiveness stays green; `declared_cases_problems` is never called | **FIXED.** The test calls `declared_cases_problems()`; `compare_gates` forgives only a key whose row id starts `[#`; `test_a_bare_forgiveness_without_a_row_id_forgives_nothing`. |
| P2 | run record | the headline marks cond=5 PASS while the block called "pasted live read" marks it NOT-RUN; the pasted lines omit evidence and `exit=` | **FIXED in the record.** The full verbatim output of run 2 is now pasted, and the text states that condition 5 was computed by a second invocation after teardown; two invocations, not one. |
| P3 | `collect_landing` | `ls-remote` first line taken as the pushed sha, though the pattern also matches heads that merely end with the name | **FIXED.** `_exact_head` reads `refs/heads/<branch>` itself, used by `verify_cleanup` too (`test_the_landing_push_reads_the_exact_ref_not_the_first_line`, `test_verify_cleanup_writes_the_read_evidence_and_reads_the_exact_ref`). |
| P3 | run record | wall time 18.6 min and 0.62 core-hours are not what the formula gives for the recorded timestamps | **REFUTED.** `17:31:48.80Z` → `17:50:27.25Z` is 18 min 38.4 s = 18.64 min; × 2 cores / 60 = 0.621 core-hours; the rounded values are 18.6 and 0.62, and `compare_cleanup` prints exactly those (the reviewer used the whole-second times). |

```
TALLY P1=3 P2=4 P3=2   (reviewer)
after disposition: P1 fixed 2, refuted 1 · P2 fixed 3, refuted 1 · P3 fixed 1, refuted 1
```

Re-run after the fixes: `tests/test_codespace_parity.py` 64 passed (RED first: 7 of the new tests failed before the fixes), `ruff check` clean.
