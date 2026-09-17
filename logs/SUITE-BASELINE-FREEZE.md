# SUITE BASELINE FREEZE — re-measured at the batch AB close

> **This freeze is a FILE, not a number.** A merge is judged against THIS SET, member by
> member, by `scripts/conductor.py suite-gate` (`[#802]`). Re-measured 2026-09-17 by operator
> order (`[#763]`'s ruled condition was firing: 36 of 41 "regressions" at `8c258bfb` were
> already failing at `a92ff5c4`, because the previous freeze was measured at `b5270d63` and the
> repo had moved past it). The previous freeze is not deleted from history:
> `git show 8c258bfb:logs/SUITE-BASELINE-FREEZE.md`.

## The measurement

| | |
|---|---|
| **Measured at SHA** | `c51083290de6a58056e815aa787b65031fabc623` (`main`, the merge that fixed the one new regression of the batch AB close) |
| **Source** | Actions `conductor` run **35239925999**, `push`, 2026-09-17T15:23:34Z |
| **Command** | `uv run --locked pytest -q --tb=short -n 4` |
| **Result** | **91 failed, 6382 passed, 22 skipped, 2 xfailed in 307.18s (0:05:07)** |
| **Workers** | **4**, passed explicitly as `-n 4` (NOT resolved from `-n auto`) |
| **Frozen members** | **87** = 91 failed in that run, minus the 4 deliberate `[#664]` witnesses |
| **Frozen on** | 2026-09-17, integrator seat (batch AB close) |

**THE PIN: `-n 4`.** Any run compared against this freeze MUST run at exactly 4 workers, and
the conductor passes `--workers 4` to the gate, which refuses any other count as NOT-COMPARABLE
(never a pass). This freeze was measured at the pinned count itself, not at an `auto` that
happened to resolve to 4, so the measurement and every comparison against it share one regime.
**Pinning narrows variance; it does not remove it:** see "Known flapping members" below.

## The judging rule

- A failure **inside** this set is **PRE-EXISTING**. It does not refuse the merge.
- A failure **outside** this set is a **REGRESSION**. It **refuses the merge**.
- Membership is by **test node id**, listed in full below — not by count, and not by file.
- A member that **passes** is the expected direction; at the next re-measure it leaves the set.

## Deliberately NOT frozen — the four `[#664]` commit-tier witnesses

These fail at `c51083290de6a58056e815aa787b65031fabc623` and are **kept OUT of the set by operator ruling**, so that every conductor
run reports them as REGRESSIONS. **That is their purpose:** they witness that the three graph
refusals do not block a real commit while those hooks run at `stages: [manual]` (since
`6e9f0bb8`). Freezing them would hide exactly the absence they exist to show. **Consequence,
stated so nobody "fixes" the gate:** the pytest job's verdict is FAIL with 4 regressions on every
push until enforcement is ON (conductor tier) or the refusals return to the local stage under
`[#883]` — and a run showing MORE than these 4 is a real regression.

```
tests/test_graph_spine_commit_tier.py::test_the_live_spine_is_ordered_rebuild_first_and_always_runs
tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-orphan-census]
tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-process-list]
tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-task-coverage]
```

## What moved since the `b5270d63` freeze

- **departed (in the old set, not failing at `c51083290de6a58056e815aa787b65031fabc623`): 0**

```
```

- **carried (in both): 51** — the old freeze's cause classes C1–C11 still describe these.
- **new entrants (failing now, not in the old set): 36** — unclassified; they entered
  between `b5270d63` and `c51083290de6a58056e815aa787b65031fabc623` without a freeze to catch them, which is the drift `[#763]` names.

## Known flapping members — the set is not fully reproducible

- `tests/test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable` fails
  only when main's short SHA is all digits (~1 commit in 44); it is frozen only if it failed here.
- C9 (`test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`)
  is cross-worker sensitive; `-n 4` narrows but does not remove it.

## The roster — membership is by node id

### Carried from the `b5270d63` freeze (51)

```
plugins/tier1-lifecycle/tests/test_plugin_paths.py::test_propose_operates_on_host_repo_not_plugin
tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
tests/test_audit.py::test_health_ok_with_registered_repo
tests/test_audit.py::test_health_stays_ok_with_na_status
tests/test_audit_parallel.py::test_health_accepts_the_parallel_flags_and_defaults_to_serial
tests/test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival
tests/test_canonical_docs.py::test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date
tests/test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it
tests/test_deny_and_point.py::test_a_CRASH_MID_EVALUATION_fails_CLOSED
tests/test_deny_and_point.py::test_an_UNRECOGNISED_VERDICT_fails_CLOSED
tests/test_desired_state_loader.py::test_live_repo_loads_clean_and_writes_nothing
tests/test_desired_state_schema.py::test_enums_match_parity_surfaces_on_disk
tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_normalises["C:\\Program Files\\claude.exe" --bg-claude]
tests/test_doc_code_edge.py::test_edge_check_registered_and_resolves_starter_set
tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
tests/test_fleet_health.py::test_prompts_dir_case_difference_is_not_staleness
tests/test_fleet_health.py::test_prompts_dir_trailing_separator_is_not_staleness
tests/test_floor_mechanisms.py::test_pre_existing_components_are_untouched_by_the_mechanism_reader
tests/test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement
tests/test_funnel_lifecycle.py::test_live_tree_leg_a1_is_location_sensitive
tests/test_funnel_lifecycle.py::test_live_tree_leg_b_measures_zero_and_the_reason_is_recorded
tests/test_funnel_lifecycle.py::test_live_tree_leg_c_measures_zero_so_arming_cannot_red_a_clean_tree
tests/test_funnel_lifecycle.py::test_live_tree_reproduces_the_census_finding
tests/test_gen_handoff.py::test_dogfood_generated_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_dogfood_no_probe_row_carries_an_answer_value
tests/test_gen_handoff.py::test_epic_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_funnel_health_renders_no_unavailable_against_the_live_repo
tests/test_gen_handoff.py::test_suffixed_bundle_probes_resolve_against_their_own_directory
tests/test_gen_handoff_preflight.py::test_session_slug_matches_a_REAL_session_store_directory_name
tests/test_gen_ledger.py::test_the_worktree_line_counts_lanes_rather_than_trees
tests/test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar
tests/test_governance_health.py::test_shared_fields_equal_fm4_block_byte_for_byte
tests/test_handoff_modes.py::test_boot_carries_both_postures
tests/test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object
tests/test_offload_admission.py::test_a_destination_REPLACED_during_publication_is_REPORTED_not_silently_used
tests/test_offload_admission.py::test_the_probe_cli_REPORTS_a_replaced_destination_rather_than_reporting_success
tests/test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_off_repo_input_defect
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_wrong_id_citation
tests/test_proof_layer.py::test_the_live_guard_population_is_at_or_below_its_baseline
tests/test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration
tests/test_reverse_dep_oracle.py::test_position_points_at_name_not_keyword
tests/test_routing_agreement.py::test_the_live_table_is_well_formed
tests/test_telemetry_wiring.py::test_a_wired_health_run_puts_no_telemetry_line_on_stderr
tests/test_telemetry_wiring.py::test_health_exposes_the_telemetry_flag_and_defaults_to_off
tests/test_telemetry_wiring.py::test_the_env_switch_turns_health_on_and_the_explicit_flag_still_wins
tests/test_v6_frozen_contract.py::test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped
tests/test_validate_adr_status.py::test_shipped_corpus_grammar_distribution_matches_the_measured_baseline
tests/test_validate_adr_status.py::test_shipped_corpus_parses_one_status_field_per_live_adr
tests/test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers
```

### New since `b5270d63` (36)

```
tests/test_archive_row_body.py::test_a_pre_commit_hook_FIRES_archive_row_body_and_not_merely_names_it
tests/test_archive_row_body.py::test_every_committed_record_still_proves_out
tests/test_check_derived_copies.py::test_every_delegated_gate_exists_in_precommit_config
tests/test_conductor.py::test_the_session_start_hook_is_wired_in_settings_json
tests/test_deny_and_point.py::test_the_guard_is_WIRED_on_the_tools_it_judges
tests/test_deny_and_point.py::test_the_wired_command_FAILS_OPEN_when_the_project_dir_is_unset
tests/test_generator_newlines.py::test_every_text_write_in_scripts_pins_newline
tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger
tests/test_lived_sandbox_observer.py::test_outer_only_markers_real_hub_wiring_derived_253d
tests/test_logs_retention.py::test_a_session_hook_CALLS_run_retention_and_not_only_the_test_suite
tests/test_logs_retention.py::test_the_retention_trigger_row_and_its_disposition_cannot_both_be_live
tests/test_prompts_guard_hook_wiring.py::test_hook_command_falls_back_to_cwd_when_claude_project_dir_is_set_but_wrong
tests/test_prompts_guard_hook_wiring.py::test_hook_command_falls_back_to_cwd_when_claude_project_dir_is_set_empty
tests/test_prompts_guard_hook_wiring.py::test_hook_command_names_the_guard_flag_and_the_guard_module
tests/test_prompts_guard_hook_wiring.py::test_hook_command_propagates_the_guards_refusal
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_a_bare_exit_2_with_a_message_that_teaches
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_a_shadow_interpreter_that_never_runs_the_guard
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_an_exit_0_that_carries_no_evaluated_marker
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_output_that_merely_contains_the_marker
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_when_no_root_resolves
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_when_the_guard_crashes
tests/test_prompts_guard_hook_wiring.py::test_hook_command_refuses_when_the_interpreter_is_unavailable
tests/test_prompts_guard_hook_wiring.py::test_hook_command_resolves_a_root_whose_path_contains_spaces
tests/test_prompts_guard_hook_wiring.py::test_hook_command_resolves_the_script_without_claude_project_dir
tests/test_prompts_guard_hook_wiring.py::test_hook_command_still_passes_when_the_guard_passes
tests/test_prompts_guard_hook_wiring.py::test_hook_command_still_prefers_claude_project_dir_when_it_is_set
tests/test_prompts_guard_hook_wiring.py::test_hook_command_still_runs_the_real_guard_from_the_repo_root
tests/test_prompts_guard_hook_wiring.py::test_hook_command_tests_for_the_marker_the_guard_module_actually_emits
tests/test_prompts_guard_hook_wiring.py::test_matcher_is_not_match_all
tests/test_prompts_guard_hook_wiring.py::test_matcher_leaves_the_break_glass_reachable
tests/test_prompts_guard_hook_wiring.py::test_matcher_still_covers_every_class_a_stale_prompts_dir_makes_lie
tests/test_release_lint.py::test_cli_green_exit_0
tests/test_release_lint.py::test_live_hub_state_is_green
tests/test_release_lint.py::test_live_v120_state_is_green
tests/test_release_lint.py::test_missing_tag_is_warn_not_fail
tests/test_release_lint.py::test_unmutated_copy_is_green
```

## Expiry

Re-measured at the next batch close, at `-n 4`, by node-id diff (never the total). A member whose
cause has merged must have left the set; if it has not, that is a row, not a new normal (`[#763]`).
