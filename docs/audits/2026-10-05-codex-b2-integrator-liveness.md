# Codex Review — b2-integrator-liveness

**Date:** 2026-10-05
**Branch:** `worktree-b2-integrator-liveness`
**Diff range:** `origin/main...HEAD` (merge-base `cd3ab8a6`); four read rounds, each on the HEAD of its time
**Codex version:** `codex-cli 0.155.0`
**Mode:** diff-review, isolated read-only session (`codex exec --sandbox read-only`, stdin closed from the prompt file), run from an empty folder under the job's tmp that held only `diff.patch`, the six changed files, the contract, the previous round's findings and `nonce.txt`. The implementing session ran nothing in it.
**Tally:** round 1 P1=3 · round 2 P1=3 · round 3 P1=2 · round 4 P1=1 — every P1 fixed or dispositioned below (no fifth read; the round-4 fix is covered by a test, not by a re-read)
**Consumer:** `LANE-B2-W1-b2-integrator-liveness.md` (Done-contract item 5, "the review record per common rules §2 (e) … citing this contract inside it"); related rows `[#971]` (liveness watchdog), `[#972]` (janitor stops every wake-up), `[#648]` (dispatcher liveness gate)

**Model used (served):** `gpt-5.6-terra`, read from each run's own header (`model: gpt-5.6-terra`, `provider: openai`) — no substitution; the pinned route answered every round.
**Review profile:** code

## Proof of read (R59 item 1)

Each answer had to open with the nonce from `nonce.txt` and the first line of `diff.patch`, verbatim. All four did.

| Round | Codex session id | Nonce returned | First line returned |
|---|---|---|---|
| 1 | `01a10b55-cdf5-7380-ab26-7020c5e94632` | `89b3a45d66524345` | `diff --git a/ecosystem/doc-counts.md b/ecosystem/doc-counts.md` |
| 2 | `01a10b5d-8e03-7a73-b359-9fbf4d32b5aa` | `4f603df4b96e4427` | same |
| 3 | `01a10b62-754f-7dc2-8b81-3b9d8ec5c821` | `c1ec697be77542b5` | same |
| 4 | `01a10b69-3fe1-70a1-b77a-2e176c96e283` | `a83662d13f6245ec` | same |

## Findings and dispositions

**Round 1 (3 × P1) — all fixed**

| Finding | Disposition |
|---|---|
| `watch` defaults to "since my own start", so a wake written just before the Monitor starts is dropped | FIXED — the default watch resumes from a ledger of the wake files it already reported; `--since` keeps the time-based mode. Tests: `test_a_restarted_watch_reports_a_wake_that_landed_while_no_monitor_ran`, `test_the_watch_cli_without_since_resumes_from_its_ledger` |
| A wake-write failure is only a stderr line | FIXED in part, then in full (rounds 2-3): 3 attempts, the failure named in the hook receipt's `reason`, and a private sibling fallback home (below) |
| `HARNESS_WAKE_DIR` can aim the wake at the repository or the transport | FIXED — `checked_home` refuses an override inside this worktree, its primary checkout, or `$CLAUDE_PROMPTS_DIR`. Tests: `test_a_wake_home_inside_this_repository_is_refused`, `test_a_wake_home_inside_the_primary_checkout_or_the_transport_is_refused`. Round 2 attacked it (relative path, `..`, symlink, Windows case) and accepted: `resolve()` plus containment covers them |

**Round 2 (3 × P1)**

| Finding | Disposition |
|---|---|
| The first Monitor records existing wakes as seen without reporting them (the template has no separate initial scan) | FIXED — a missing ledger now reports every wake from the last 3 h (`FIRST_START_LOOKBACK_S`, the cycle ceiling) and only records older ones. Tests: `test_the_first_start_reports_recent_wakes_and_only_records_the_old_ones` and the amended restart test |
| No durable fallback for a persistent wake-write failure | DECLINED in round 2, ACCEPTED in round 3 once the reviewer named a concrete failure (the home replaced by a file, or a deny ACL on it, while a sibling stays writable) — see round 3 |
| Overlapping Monitors emit the same wake twice | DECLINED as a defect — claiming a wake before reporting it would let the OUTGOING seat's Monitor take a wake the SUCCESSOR needs at a handover; each Monitor reports to its own seat. Changed instead: the template's cycle says the successor reads every `IN-FLIGHT` lane's session file for a closing `HANDBACK` and the outgoing seat starts no new merge once the successor has claimed; the `watch_wakes` docstring states the choice. **Round 3 attacked the disposition and accepted it** ("at a no-merge point, any earlier merge finishes before handover; after successor claim the outgoing seat starts none, while the successor scans every IN-FLIGHT session file"). Tests: `test_two_monitors_each_report_every_wake_to_their_own_seat`, `test_the_successor_scans_the_in_flight_lanes_and_the_outgoing_seat_starts_no_new_merge` |

**Round 3 (2 × P1) — both fixed**

| Finding | Disposition |
|---|---|
| The first-start initialisation records a wake it could not `stat()` as seen | FIXED — an unreadable wake is left for the polling loop. Test: `test_the_first_start_does_not_record_a_wake_it_could_not_stat` |
| The declined fallback stays valid: the home can be replaced by a file or denied by an ACL while a sibling directory is writable | FIXED — `write_wake` tries the home, then `<home>-fallback` in the same per-user state directory (still the R17 private home; a temp directory is not), and `watch` reads both. The ledger moved BESIDE the homes (`<home>.watch-seen`) so a broken home cannot take the watch down. The hook receipt's `reason` names a fallback or a total loss. Tests: `test_an_unusable_wake_home_falls_back_to_its_private_sibling_and_the_watch_reads_both`, `test_the_watch_runs_when_the_wake_home_is_replaced_by_a_file`, `test_the_fallback_home_is_a_sibling_so_it_is_as_private_as_the_home` |

**Round 4 (1 × P1) — fixed**

| Finding | Disposition |
|---|---|
| A failed moment's reason overwrites the wake-loss note in the receipt | FIXED — the receipt's `reason` carries both. Test: `test_a_failed_moment_does_not_hide_a_lost_wake_in_the_receipt` (both a non-zero exit and a crash) |

## Reviewer's clean reads

Round 2 held no P2/P3. Round 3 held no P2/P3. Round 4 held one P1 and no P2/P3. No finding concerned Done-contract item 4 (`no_leftovers` check 08), the template's cycle ordering (claim and bind before the outgoing release, three read-backs 30 s apart, the 3 h ceiling), or a change to `lane_end_guard.py`'s existing flags and exit codes.

## Not covered by a re-read

The round-2 fixes (first-start lookback, the cycle's in-flight scan) were re-read in round 3; the round-3 fixes in round 4. The single round-4 fix has its test (`…does_not_hide_a_lost_wake…`) and no fifth read: **the integrator should read it as tested, not as re-reviewed.** The RED run of the round-2 and round-4 tests was shown for the round-4 test only; the round-2 tests were written before their code in the same working step and their failing run was not captured separately.

## Consumer

This record is the review the contract names (`LANE-B2-W1-b2-integrator-liveness.md`, Done-contract item 5), written to the name the audit grammar admits (`docs/audits/<date>-codex-<slug>.md`). `docs/audits/README.md` is left stale for the integrator (`[#590]`).

## Amendment 2026-10-05 — repair 1 of 2 (dated, append-only)

The integrator refused the merge of `4a9a03cd` (`to-browser/REFUSED-b2-integrator-liveness.md`, repair 1 of 2): `tests/test_order_cycle_rule.py::test_integrator_cycle_section_names_the_handover_interval_and_rebind` still asserted the old `"2 h"` interval that Done-contract item 2 replaced in `templates/integrator-order-template.md`; it was red on both CI legs and one of eight test files that read the template, which the lane's targeted runs had not included.

**The one test change:** in that test, `assert "2 h" in cycle` became `assert "at least every 3 h" in cycle` — the contract's own 3-hour ceiling as the template now states it. The other three assertions are unchanged; `test_dispatcher_cycle_section_names_the_handover_interval_and_rebind` is untouched (the dispatcher template still says 2 h and is not this lane's). A one-assertion re-point to the contract's own number needs no new Codex read (the refusal's fix list, item 5); no code changed in this repair, so none was requested.

**Not changed (refusal item 6, optional):** the P3 on `c0b19118` (the conftest fixture is inert for `tests/test_connection_loop.py`, whose `World.env()` strips every `HARNESS_*` variable; the witness only reads the in-process variable) is left as it stands — making the witness bite is a further test change that would need its own Codex read. It remains the integrator's `ROWS-OWED` line.
