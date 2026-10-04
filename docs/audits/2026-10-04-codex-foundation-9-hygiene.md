# Codex Review — foundation-9-hygiene

**Date:** 2026-10-04
**Branch:** `worktree-foundation-9-hygiene`
**Diff range:** `origin/main...HEAD` (doc-counts excluded as generated). Review 1 at `6a45b1ff`, review 2 at `6d5e36b5`; base `3157d69b`, the sha this lane merged at step 0.
**Mode:** diff-review, isolated read-only session — an empty folder under the job tmp holding the diff, the nine changed files, the contract and a `nonce.txt` (not the lane)
**Consumer:** `LANE-FOUNDATION-foundation-9-hygiene.md` (Done-contract item 5, "the review record (route above) citing this contract inside it, its P1s fixed"); the integrator's merge verdict for batch FOUNDATION reads it.
no-consumer: a lane's frozen contract is the only consumer this record has, and it is a transport file, not a governance surface (`[#id]` row, ADR, `STANDING_RULINGS`, intake) that `consumer_at_landing` recognises

**Model used:** `gpt-5.6-terra`, served — read from each run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`, reasoning effort high (review 1 session `01a103f4-4169-7321-a1fd-dd15489bc15c`; review 2 session `01a10416-6a73-7f53-9ad2-58597502559b`). Codex route, so no substitution.
**Nonce returned:** review 1 `NONCE-57992783703346a7`; review 2 `NONCE-d3e016419d9b4980` — each the first line of the reviewer's answer, equal to the `nonce.txt` it was given.
**Review profile:** code
**Tally:** review 1 P1=2 P2=0 P3=0, verdict `FAIL (P1=2 P2=0 P3=0)`; review 2 P1=2 P2=0 P3=0, verdict `FAIL (P1=2 P2=0 P3=0)`. Verdict lines reported as given. All four P1s are fixed (below). The tip after the fixes, `dfe3e4fb`, was **not** reviewed a third time.

## Review 1 (tip `6a45b1ff`)

| P | Finding | Disposition |
|---|---|---|
| P1 | `scripts/no_leftovers.py` check 08: a `state.json` that parses but is not an object (`[]`) is ignored, so check 08 passes on a record it cannot read | **Fixed, `6d5e36b5`.** A non-object record joins the unreadable set and FAILs. RED shown first: 4 of 4 parametrised cases (`[]`, `null`, `"stopped"`, `42`) failed with the fix removed |
| P1 | the simulated-cycle test does not run `audit.py health` (Done item 1 names it) | **Fixed, `6d5e36b5`.** `test_audit_health_reads_ok_after_a_simulated_cycle` runs the command as a child with HOME on a folder whose registry holds a bound-then-unbound dispatcher silent past `WEDGED_AFTER_MIN`; it asserts exit 0 and `health: OK` (106 s). `audit.py` has no seat reader of its own (grep), so the test pins that the integrated command stays OK beside a cycled registry; the readers (`fleet_health.seat_health_line`, `handoff_state.row_seats`) are pinned by `test_a_simulated_cycle_leaves_the_health_readers_clean` |

## Review 2 (tip `6d5e36b5`; the reviewer also read review 1)

| P | Finding | Disposition |
|---|---|---|
| P1 | check 08: an object whose locator field is malformed (`{"worktreePath": []}`) reads as unrelated and passes | **Fixed, `dfe3e4fb`.** A `cwd`, `worktreePath` or `worktreeBranch` that is present and not a string is unreadable and FAILs; `null` and absent stay fine (no record on this box carries a non-string one — grep of `~/.claude/jobs/*/state.json`). Pinned by `test_8_fails_closed_on_a_record_whose_locator_field_is_not_a_string` and `test_8_passes_a_record_with_null_or_absent_locators_that_names_no_lane`. The new locator test was not run RED against the unfixed script (it fails by construction: the old reader skipped non-string locators) |
| P1 | `test_a_hand_appended_unbind_row_carrying_a_state_is_discarded` passes on the pre-change reader, so it is not RED-first evidence for item 1 | **Fixed, `dfe3e4fb`.** It is a regression guard, not the item's RED evidence (that is the other eight failing tests, shown in the SESSION file). It now also appends the same row without `state` and asserts the seat reads `absent`; the pre-change reader discarded every unbind row and would read `live` |

## What shipped, in one line

Four small fixes, each its own commit: a `seat_registry.py unbind` verb called by the dispatcher order's Cycle section (a cycled seat reads `absent`, not `wedged`); check 08 passes a record in the terminal `stopped` state and still FAILs a live, unknown-state or unreadable one; `decide_lane`'s HOLD reason names only the unmet `starts_after` lanes; the lane template's close-out item asks for the R59 proof of read.
