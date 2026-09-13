# Lane `lane-x-664-delete-list-execution` — delete-list execution evidence log

> Working evidence artifact for `LANE-x-664-delete-list-execution.md`, the execution of the
> ratified `[#664]` DELETE / TRIGGER / KEEP list
> (`docs/audits/2026-09-13-census-x-664-delete-list.md`). Appended to across the lane's steps;
> the final section is the end-of-lane artifact. Tool output is recorded verbatim, never
> narrated.
>
> Governance consumers: `[#664]` (the owning row and the census), `[#694]` (owner of the
> telemetry disposition), `[#655]` (owner of `run_retention()` has no production caller),
> `ADR-89` (the oracle's declared static-only limit), `ADR-110` (the lane protocol),
> `intake #86` (the census fixture).

## Step 0 — the lane's base moved, and one done-contract item was already discharged

The worktree was provisioned at `dbac84b8`. `main` had moved to `c0e0722f` (the
`docs/batch-x3-close-packet` merge) while this lane booted, and `journal_spine_anchor` refused
the first commit on the classic tree-lag shape — the check reads the JOURNAL from the committing
tree and the spine from the shared `main` ref. The discriminator was run before any remedy, as
the check's own diagnostic prescribes:

```
introduced: ['c0e0722f664907bf3abc9408ecf01cd2b261ccb6', '54c759854173e722dd16ca2288aa3487c5b1d220', 'e07615759c5693577fec9f1a50194ac06e790a51']
anchored in this tree: False
anchored at main: True
```

False here with True at main is tree lag, not a gap on main, so `git merge origin/main` is the
recorded fix rather than a guess. It fast-forwarded (the lane had no commits of its own yet), so
**this lane's base is `c0e0722f`, not `dbac84b8`** — and the paired-run baseline is re-taken
there rather than at the provisioned SHA. A baseline at a pre-sync commit would charge this lane
for `main`'s own deltas, which is the one thing the pairing exists to prevent. Both readings are
recorded in Step 2.

### DONE-CONTRACT ITEM 7 IS ALREADY DISCHARGED, BY MAIN, NOT BY THIS LANE

The sync brought in a four-line deletion in `scripts/graph_queries.py`:

```
-    "scripts/worktree_seed.py": Disposition(
-        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
-               "(.claude/commands/lane-boot.md:124)",
-        owner="operator -- one of the census's seven acts"),
```

That is done-contract item 7 verbatim — *"`scripts/worktree_seed.py`'s `ORPHAN_DISPOSITIONS`
entry DELETED — the MODULE STAYS"* — and its stated acceptance,
`tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`,
is green on the synced base:

```
uv run --locked python -m pytest tests/test_graph_spine.py -x -q -p no:randomly -n 0
37 passed in 34.11s
```

The same test is in the `dbac84b8` baseline's FAILED list (Step 2), with the exact subject the
contract names: `['scripts/worktree_seed.py']`. So the premise *"two prior lanes declined this
one-line edit … the operator has now ruled it … make the edit"* is **refuted by having been
satisfied**, between the freeze and this run.

**This is a PAUSE-class fact under Q10, and it is DISCLOSED rather than paused on**, because
AX27-1 forbids a wave-4 lane waiting on the operator mid-run and the refutation is
work-eliminating rather than work-blocking: re-making an edit that is already on `main` would
either be a no-op or a conflict, and neither is an act. Step 9 therefore carries only the
`cost_usage_telemetry.py` half of its two-part item. Nothing was reverted, re-applied or
re-litigated.

## Step 1 — the oracle is PROVISIONED, and it is RUN before any deletion

### Precondition: the pinned langserver was vendored

`npm install`, verbatim:

```
added 1 package, and audited 2 packages in 57s

found 0 vulnerabilities
```

`node_modules/pyright/langserver.index.js` present afterwards. `package.json`'s sole declared
dependency is `pyright@1.1.410` and `package-lock.json` is committed, so this restores a
**declared, pinned, checked-in** dependency. `node_modules/` is gitignored (`.gitignore:124`)
and stays out of this lane's commits.

**This was the lane's own precondition, not an inherited state.** The census records
(`2026-09-13-census-x-664-delete-list.md:26-28`) that *"No DELETE row below carries a
`safe_remove` verdict"* because the oracle *"returned `oracle-unavailable` for all nine
candidates tried"*. **That no longer reproduces.** Every run below returned a resolved
verdict; `oracle-unavailable` did not recur once. The census's gap was a provisioning gap on
the box, exactly as it said it was.

### A note on the transcription of the verdicts below

The verdicts are recorded as the tool emitted them. One correction of the CAPTURE, not of the
output: the Windows console renders this repo's em dash (U+2014) as a replacement character
under cp1252, so the `reason:` lines below carry the em dash the source actually emits
(`scripts/safe_remove.py:307`), not the console's mangling of it. Nothing else is altered.

### Run 1 — `scripts/gen_trend_dashboard.py`

```
safe-removal verdict: REVIEW
removal set: scripts/gen_trend_dashboard.py
reason: 2 bare-stem string-literal hit(s) for gen_trend_dashboard — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_gen_trend_dashboard.py:49
- tests/test_trend_dashboard.py:48

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 2 — `scripts/gen_north_star.py`

```
safe-removal verdict: SAFE
removal set: scripts/gen_north_star.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 3 — `scripts/window_metrics.py`

```
safe-removal verdict: REVIEW
removal set: scripts/window_metrics.py
reason: 1 bare-stem string-literal hit(s) for window_metrics — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_window_metrics.py:31

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 4 — `scripts/failed_set.py`

```
safe-removal verdict: SAFE
removal set: scripts/failed_set.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 5 — `scripts/nopack_sandbox.py`

```
safe-removal verdict: SAFE
removal set: scripts/nopack_sandbox.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 6 — `scripts/trace_writer.py`

```
safe-removal verdict: REVIEW
removal set: scripts/trace_writer.py
reason: 1 bare-stem string-literal hit(s) for trace_writer — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_trace_writer.py:14

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 7 — all six as ONE removal set, which is the shape the lane actually performs

Recorded because six single-module runs answer a question the lane does not ask. The deletions
land as a set, and two of the six are reachable only from another member of it — so a per-module
verdict is systematically more pessimistic than the act.

```
safe-removal verdict: REVIEW
removal set: scripts/failed_set.py, scripts/gen_north_star.py, scripts/gen_trend_dashboard.py, scripts/nopack_sandbox.py, scripts/trace_writer.py, scripts/window_metrics.py
reason: 4 bare-stem string-literal hit(s) for failed_set, gen_north_star, gen_trend_dashboard, nopack_sandbox, trace_writer, window_metrics — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_gen_trend_dashboard.py:49
- tests/test_trend_dashboard.py:48
- tests/test_trace_writer.py:14
- tests/test_window_metrics.py:31

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**Zero surviving referrers across the whole set.** No `unsafe` verdict, no `unverifiable` entry,
and no `oracle-unavailable` — the set run reaches the same answer the six single runs did, by the
same route. The four REVIEW hits are the same four already accounted for above, each in a test
file that is co-removed with its module.

### What the oracle did NOT see, and this is the item that matters

**`gen_north_star.py` verdicts SAFE, and it has a live in-repo importer.**
`scripts/gen_trend_dashboard.py:113-117` loads it through
`importlib.util.spec_from_file_location(..., Path(__file__).resolve().with_name("gen_north_star.py"))`
and reads `_north_star.ARCS` at `:900`. That is not an `import` statement, so Pyright's
`references()` never sees it — **the exact false-PASS class ADR-89 declares and
`scripts/desired_state_loader.py` is this repo's worked example of.**

The bare-stem literal scan did not downgrade it to REVIEW either, and the reason is worth
writing down rather than leaving to be rediscovered: the scan looks for the module's **bare
stem** inside a quoted literal, and the only literal here is `"gen_north_star.py"` — the stem
**plus the extension**. A dynamic loader that names a sibling by filename is the most natural
spelling of this edge, and it is the spelling the REVIEW downgrade misses. Recorded as a
finding against `safe_remove._bare_stem_literal_hits`, owned by `[#195]`/`ADR-89`, not repaired
here: widening that scan changes what a removal gate says across the whole repo, which is not
this lane's footprint.

**It does not change what this lane does.** The census already ordered
`gen_north_star.py` deleted **after** `gen_trend_dashboard.py` for exactly this edge, so the
importer dies with the import. The ordering was ruled from the FPG-1 graph, which sees the edge
the oracle cannot — and this run is the measurement that says the graph, not the oracle, is what
made that ordering safe.

Same shape, one level weaker, for `failed_set.py`: SAFE individually, and its recorded referrer
`window_metrics.py:359` is prose in an f-string rather than an import. There is no code edge to
break in either direction; the ordering is still honoured, because the ratified order is
immutable and a lane does not relitigate it on a measurement that agrees with it.

### The verdict-vs-act ledger

| module | verdict | what the verdict is downgraded by | deleted at step |
|---|---|---|---|
| `scripts/gen_trend_dashboard.py` | REVIEW | its own two dedicated test files | 3 (first) |
| `scripts/gen_north_star.py` | SAFE (a FALSE PASS on the importlib edge, see above) | — | 3 (second) |
| `scripts/window_metrics.py` | REVIEW | its own dedicated test file | 4 (first) |
| `scripts/failed_set.py` | SAFE | — | 4 (second) |
| `scripts/nopack_sandbox.py` | SAFE | — | 5 |
| `scripts/trace_writer.py` | REVIEW | its own dedicated test file | 5 |

Every REVIEW downgrade is a hit in the module's **own dedicated test file**, which is co-removed
with the module. That is the `[#734]` precedent's rule, not a new one: *"DELETED with their
dedicated tests and their `ORPHAN_DISPOSITIONS` entries"*. A REVIEW whose only hit is a test that
leaves in the same commit is not a surviving reference.

**No verdict is treated as a licence.** Done-contract item 2 binds: a SAFE verdict is necessary
and not sufficient, and the paired baseline/tip Actions run in Step 2 / Step 6 is what carries
the weight the oracle cannot.

## Step 2 — the Actions BASELINE

Workflow `report-only wall` (`.github/workflows/report-only-wall.yml`), fired by
`workflow_dispatch` on this lane's own branch so that the baseline and the tip run the SAME
workflow on the SAME runner class, adjacent in time and both inside this lane's own run. The
workflow records and never blocks, so a non-zero pytest leg is the reading, not a breakage.

### Two baseline readings, because the base moved (Step 0)

| reading | run id | head SHA | pytest tail |
|---|---|---|---|
| provisioned base (superseded) | `34756963263` | `dbac84b8` | `54 failed, 5996 passed, 21 skipped in 177.89s` |
| **THE BASELINE OF RECORD** | **`34757902205`** | **`c0e0722f`** | **`55 failed, 5994 passed, 22 skipped in 218.78s`** |

Both are kept. The first is what the contract's words asked for; the second is the base this
lane actually builds on, and it is the one Step 6 diffs against. Both ran `pyright shape:
unprovisioned (modelled: 7/8 proven, 1 skip)` — the runner does not vendor the langserver, which
is a property of the workflow (REQUIREMENT 6, resolved as RECORD) and is constant across the
pair, so it cancels in the diff.

The delta between the two readings is exactly three nodeids and every one of them belongs to
`main`, not to this lane — recorded because a moved base is the easiest place to lose a
failure:

- **`+ tests/test_gen_audit_index.py::test_live_index_is_fresh`**
- **`+ tests/test_gen_audit_index.py::test_live_index_excludes_nothing_because_every_audit_is_tracked`**
  — `main` landed `docs/audits/2026-09-13-technical-batch-x3-close-packet.md` without the index
  pass, which is the integrator's owed regeneration under the `[#590]` narrowing, not a lane's.
- **`- tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`**
  — main's own fix; done-contract item 7, discharged before this lane ran (Step 0).

### The baseline failure set of record — 55 nodeids at `c0e0722f`

Recorded in full rather than counted, because item 3's rule (*"a failure present in BOTH
readings is not this lane's; a failure present only at tip is, and it blocks"*) is a set
operation and a count cannot perform it.

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
tests/test_gen_audit_index.py::test_live_index_excludes_nothing_because_every_audit_is_tracked
tests/test_gen_audit_index.py::test_live_index_is_fresh
tests/test_gen_handoff.py::test_dogfood_generated_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_dogfood_no_probe_row_carries_an_answer_value
tests/test_gen_handoff.py::test_epic_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_funnel_health_renders_no_unavailable_against_the_live_repo
tests/test_gen_handoff.py::test_suffixed_bundle_probes_resolve_against_their_own_directory
tests/test_gen_handoff_preflight.py::test_session_slug_matches_a_REAL_session_store_directory_name
tests/test_gen_ledger.py::test_the_worktree_line_counts_lanes_rather_than_trees
tests/test_gen_north_star.py::test_the_committed_view_is_current
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
tests/test_validate_branch_naming.py::test_local_branches_reads_the_live_repo
tests/test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers
tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH
tests/test_worktree_seed.py::test_the_verdict_names_WHY_rather_than_only_failing
```

Two of these are RUNNER-SHAPED rather than repo-shaped, and are named so a reader does not chase
them: `test_validate_branch_naming.py::test_local_branches_reads_the_live_repo` fails because the
Actions checkout carries only the dispatched branch and no local `main`, and the two
`test_worktree_seed.py` rows fail for the same reason (*"main does not resolve in
/home/runner/work/dev-knowledge/dev-knowledge"*). They are constant across the pair and cancel in
the diff; they are not evidence about this repo's health either way.

**One baseline failure is expected to DISAPPEAR at tip, and that is not a regression.**
`tests/test_gen_north_star.py::test_the_committed_view_is_current` fails here because
`ecosystem/north-star.md` is already stale against its generator. Step 3 deletes that test with
its module. Item 3's rule is one-directional by construction — it blocks on a failure present
ONLY AT TIP — so a baseline failure that leaves is reported, never treated as a pass to be
explained away.

## Step 3 — `gen_trend_dashboard.py`, then `gen_north_star.py`

Removed in that order, which is the ratified one and is load-bearing: the dashboard loads the
north-star view through `importlib`, so deleting the loaded module first would have left a
broken load in the tree between the two `git rm`s.

Each module leaves with **its dedicated tests and its `ORPHAN_DISPOSITIONS` row**, which is not
this lane's invention — it is the `[#734]` retire stage's recorded rule, and the same rule the
census fixture's own comment states. Five files:

- `scripts/gen_trend_dashboard.py`, `tests/test_gen_trend_dashboard.py`, `tests/test_trend_dashboard.py`
- `scripts/gen_north_star.py`, `tests/test_gen_north_star.py`

plus both rows out of `graph_queries.ORPHAN_DISPOSITIONS` and both out of
`test_graph_spine.CENSUS_SCRIPT_ORPHANS`. The register rows leave rather than being re-worded
for the reason the register's own `.claude/commands/override.md` note already states: *"a
disposition says 'this orphan was LOOKED AT and ruled', and a file that is gone is not an
orphan"*. The fixture rows leave for the reason its own comment states: *"A census row leaves
this fixture WITH the commit that retires its subject"* — and they are removed under a NEW
attribution block rather than folded into the `[#734]` one, so the two retirements stay
separable by a later reader.

Targeted tests, selected by the organ rather than guessed
(`impacted_tests.py select --changed scripts/gen_trend_dashboard.py --changed
scripts/gen_north_star.py --changed scripts/graph_queries.py`):

```
tests/test_graph_spine.py tests/test_canonical_docs.py tests/test_gen_ledger.py
  -> 2 failed, 109 passed in 158.95s
tests/test_assemble_paste.py tests/test_batch_manifest.py tests/test_decision_coverage.py
tests/test_edge_class_census.py tests/test_fleet_parity.py tests/test_gen_lane_contract.py
tests/test_gen_seat_boot.py tests/test_impacted_tests.py tests/test_prompts_guard_hook_wiring.py
tests/test_verify_handoff_probes.py
  -> 634 passed, 1 skipped in 1377.22s
```

Both failures are `tests/test_canonical_docs.py` rows that are **already in the Step 2 baseline
set** (`test_the_derived_leg_is_warn_class_on_arrival` and
`test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date`). Present in
both readings, so not this lane's, and named here rather than left as a bare count.

### RESIDUE LEFT DELIBERATELY, and what it costs

`ecosystem/north-star.md` is `gen_north_star.py`'s committed output, and it **stays**. Its own
header now names a generator that no longer exists, and `README.md:74` points a reader at both.
That is a real stale locator and it is left rather than swept, on the contract's own rule for
this class: `[#624]` holds a live `implements` edge to the artifact (`file_purpose_graph.py why
ecosystem/north-star.md` → `is implemented by task:624`), `[#383]`/`[#624]` name the generator,
and the contract's words are *"Do not close or rewrite another lane's row to make a gate green
… say so in the end-of-lane artifact and leave it for the operator."* Deleting the artifact
would orphan `[#624]`'s edge on top of the module edges the contract already anticipated, and
the README bullet is in this repo's canonical front door — closer to a V-2 class (a)
curated-baseline touch than any of the six deletions are. **Owed to the operator, named in the
end-of-lane packet: `ecosystem/north-star.md` and `README.md:74`.**

`ecosystem/trends.html` needs no decision — `gen_trend_dashboard.py`'s docstring records it as
`regenerated on demand; NOT committed`, and `git ls-files` confirms it is untracked.

## Step 4 — `window_metrics.py`, then `failed_set.py`

The same shape as Step 3 and the same ordering discipline. `failed_set` is an orphan **by
inheritance** — its own register row says it is *"dispositioned WITH its caller and not before
it"* — so it is retired with its caller and not before it either. Four files:
`scripts/window_metrics.py`, `tests/test_window_metrics.py`, `scripts/failed_set.py`,
`tests/test_failed_set.py`, plus both register rows and both fixture rows.

The graph was read before the act rather than after it:

```
scripts/window_metrics.py   consumers (4): task:470 task:611 task:689 task:694 (all task-implements)
                            edges (2): imports scripts/assemble_paste.py, scripts/fleet_health.py
scripts/failed_set.py       consumers (1): task:694 (task-implements)
                            edges (0)
```

Every consumer is a `task-implements` edge — a row naming the module, not code calling it — which
is the contract's anticipated residue class and is left for the operator. The two OUTBOUND edges
are this module reading others; deleting the reader breaks nothing it read.

Targeted tests:

```
tests/test_graph_spine.py tests/test_assemble_paste.py tests/test_fleet_parity.py
tests/test_edge_class_census.py tests/test_decision_coverage.py tests/test_gen_ledger.py
tests/test_gen_lane_contract.py
  -> 434 passed in 755.94s
```

`test_assemble_paste.py` is in that set deliberately: `assemble_paste.PASTE_BUDGET` is PUBLIC
*because* `window_metrics` imported it (`assemble_paste.py:33-41`). The constant and its tests
are untouched and green; the comment explaining its visibility now names a module that is gone,
and that one-line staleness is recorded in the residue list rather than repaired from a lane
whose footprint is the delete list.
