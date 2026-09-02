# Verification parity — local vs. codespace, both at `b5753f52`

> `[.dev-knowledge · #632 · lane-g-632-parity]`. This is the parity leg for G0's substrate
> decision: a nodeid-set diff between the local leg (frozen input, already measured) and this
> container leg (measured below), both run against the byte-identical tree at `b5753f52`.
>
> consumer: batch G's G0 substrate decision — `[#632]`, `protocols/STANDING_RULINGS.md` R-G0-2/R2,
> and the AMENDMENT 3 marker this lane appends to `docs/audits/2026-09-02-technical-batch-f-close-packet.md`.

## Arrival gate

- `git rev-parse HEAD`: `b5753f52dd7942db924fcac764bfa6c0b6c9a4fd`
- `uv --version`: `uv 0.11.19 (x86_64-unknown-linux-musl)`
- `CODESPACE_NAME`: `lane-g-632-parity-7r5j6v4w9pvhrrqj`
- Container provenance: created for this dispatch (`Dispatch-Codespace -Contract LANE-g-632-parity.md -Slug lane-g-632-parity`), not rebuilt — per ruling 2026-08-31, a rebuilt container has not applied its own `devcontainer.json`. No commit existed on this branch ahead of `b5753f52` before the suite ran.

## Run facts

### Local leg (frozen input, source `run-report`, measured on the primary checkout at `b5753f52`)

```
13 failed, 4863 passed, 4 skipped, 1 xfailed in 897.22s (0:14:57)
```

### Container leg (measured this run, source `run-report`)

```
16 failed, 4852 passed, 12 skipped, 1 xfailed in 311.24s (0:05:11)
```

- `uv --version` (container): `uv 0.11.19 (x86_64-unknown-linux-musl)`
- `HEAD` (container): `b5753f52dd7942db924fcac764bfa6c0b6c9a4fd`

## Nodeid-set diff

### both (11)

```
tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
tests/test_cloud_provisioning.py::test_provision_sh_runs_the_history_repair_before_arming_hooks
tests/test_cloud_provisioning.py::test_the_gate_never_syncs_the_environment_it_is_asserting
tests/test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it
tests/test_desired_state_report.py::test_live_report_renders_the_real_fleet
tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
tests/test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement
tests/test_gen_north_star.py::test_the_committed_view_is_current
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_wrong_id_citation
tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings
```

### local-only (2)

```
tests/test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance
tests/test_reverse_dep_oracle.py::test_main_finding_json_exit_zero
```

### container-only (5)

```
tests/test_boundary_report.py::test_live_hub_baseline_and_consumers_legal
tests/test_merge_serialization.py::test_index_lock_blocks_concurrent_merge
tests/test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_off_repo_input_defect
tests/test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration
```

Counts check: both (11) + local-only (2) = 13 = the local leg's total. both (11) + container-only
(5) = 16 = the container leg's total.

## The two named exceptions (ruling R-G0-2)

Neither `tests/test_audit.py::test_health_ok_with_registered_repo` nor
`tests/test_audit.py::test_health_stays_ok_with_na_status` appears in this run's failed set at
all — both passed (or were otherwise not failing) on this container leg, so the previously
root-caused `receipt.json`-artifact failure mode did not manifest this run. There is nothing to
subtract from the container-only set on that account: all 5 container-only nodeids above are
already "other" by construction.

## R2

The container-only set, after subtracting the two named exceptions (which were not present to
subtract), is **not empty** — 5 nodeids remain. Per the contract, R2 fires.

VERDICT: FLIP — G1-G8 re-dispatch LOCAL (verb change only). Container-only nodeids beyond the two named exceptions: tests/test_boundary_report.py::test_live_hub_baseline_and_consumers_legal, tests/test_merge_serialization.py::test_index_lock_blocks_concurrent_merge, tests/test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused, tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_off_repo_input_defect, tests/test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration.
