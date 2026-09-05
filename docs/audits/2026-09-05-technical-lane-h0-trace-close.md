# Lane h0 — dispatch trace stream, close packet

<!-- lane: lane-h0-trace · branch: worktree-lane-h0-trace · contract: LANE-h0-trace.md
     board: [.dev-knowledge · #66 · lane-h0-trace] · model/effort: opus / high -->

Every dispatch leaves a readable trace under `logs/prompts/`, reusing `receipt.json`'s
own fields rather than inventing a new format (`LANE-h0-trace.md`). This packet is the
lane's end-of-lane artifact per its own Done-contract / Steps §3.

## What changed

- **`scripts/trace_writer.py`** (new) — `render_trace()` / `write_trace()` plus a Click
  CLI. Writes one file at `logs/prompts/<date>-<lane>.md` carrying the five parts the
  contract names: the contract AS SENT, the skeleton run (`dispatch-run.sh`),
  `receipt.json`, the outcome (branch / commits / targeted tests), and model/effort.
  Concatenation only — no computed metric, no distillation, no second format.
- **`.gitignore`** — `logs/prompts/` added to the existing DISPATCH ARTIFACTS block:
  never committed, same ephemeral-organ-output pattern as `logs/FLEET-HEALTH.md`.
- **`scripts/fleet_health.py`** — `count_traces_today(logs_dir, today)` scans
  `logs/prompts/` for today's `<date>-*.md` files, mirroring the `_scan_md`
  absent-is-0 / unreadable-is-None split the other five funnel producers already use.
  `main()` prints `[traces] N today`, unthrottled and fail-soft, right after `[funnel]`.
- **Tests** — `tests/test_trace_writer.py` (9 tests: all-five-parts rendering, filename
  shape, exactly-one-file-per-dispatch, same-day overwrite-not-accumulate, out-dir
  creation, CLI round-trip) and three new cases in `tests/test_fleet_health.py`
  (today-count, absent-dir, unreadable-dir) plus one `main()` line-presence test.

## Seeding / witnessing — the honest limit

Done-contract item 1 asks for one seeded dispatch witnessed with all five parts present.
That witnessing is via `tests/test_trace_writer.py`'s hermetic `tmp_path` fixtures
(`test_render_trace_carries_all_five_parts`, `test_write_trace_names_file_by_date_and_lane`,
`test_write_trace_seeds_exactly_one_file`), not a live capture of **this lane's own**
dispatch. That is a structural limitation, not a shortcut taken for convenience:
`dispatch-run.sh` writes `receipt.json` only after the `claude -p` process it launched
exits (`wait "$CLAUDE_PID"` precedes the python receipt-assembly block), so no action
taken from inside this very session can produce a genuine `receipt.json` for its own run
— the file does not exist until after this session is over. A live end-to-end trace for
a real dispatch needs either a later dispatch that re-invokes the writer once its own
receipt has landed, or a change to `dispatch-run.sh` itself to call the writer after the
receipt is assembled — both outside this lane's declared footprint (no edits outside it).

## Commits on `worktree-lane-h0-trace`

- `413b9592` — step 1: trace writer + ignore rule
- `f2802939` — step 2: fleet_health.py traces-per-day count
- *(this commit)* — step 3: a real defect the fleet's own newline-pinning gate caught
  (`out_path.write_text(body, encoding="utf-8")` was missing `newline="\n"`, so the
  trace file would have inherited platform newline translation on a Windows dispatch
  substrate) fixed in `scripts/trace_writer.py`, plus this close packet.

## Verification

- **Targeted:** `tests/test_trace_writer.py` (9 passed), `tests/test_fleet_health.py`
  (152 passed), `tests/test_generator_newlines.py` (all passed, after the fix above).
- **Full suite** (`uv run --locked pytest --tb=line -q`, run twice — once before this
  lane's diff via `git stash`, once after): **16 pre-existing failures, identical with
  and without this lane's diff** — none reference `logs/prompts`, `trace_writer`, or
  `fleet_health`. Confirmed baseline drift, not something this lane introduced or is
  scoped to fix:
  - `test_cloud_provisioning.py::test_the_gate_never_syncs_the_environment_it_is_asserting`
  - `test_cloud_provisioning.py::test_provision_sh_runs_the_history_repair_before_arming_hooks`
  - `test_audit.py::test_check_fleet_parity_green_on_live_repo`
  - `test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it`
  - `test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement`
  - `test_gen_north_star.py::test_the_committed_view_is_current`
  - `test_boundary_report.py::test_live_hub_baseline_and_consumers_legal`
  - `test_desired_state_report.py::test_live_report_renders_the_real_fleet`
  - `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent`
  - `test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export`
  - `test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused`
  - `test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_off_repo_input_defect`
  - `test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_wrong_id_citation`
  - `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge`
  - `test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration`
  - `test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`

## Proposed diffs (none pending)

Nothing further is proposed against this lane's declared footprint. The three commits
above are the whole of it.

## Open items

- The pre-existing 16-failure baseline above is unowned by this lane and reported
  rather than fixed, per "No edits outside this lane's declared footprint."
- The seeding gap named above (no live self-referential trace is possible from inside
  a dispatch) is a fact about `dispatch-run.sh`'s own sequencing, not a defect in
  `trace_writer.py`. Closing it — if wanted — is a `dispatch-run.sh` change and belongs
  to whichever row owns that script (`[#634]` is the most recent one touching it).
- `logs/prompts/` and the trace format are intake `#66`'s TRACE-layer gap, filed as
  DRAFT/READY and not ratified; this lane implements the shape `LANE-h0-trace.md`
  specified directly rather than waiting on that ratification, per the contract's own
  authority (a dispatched contract, not the intake).
