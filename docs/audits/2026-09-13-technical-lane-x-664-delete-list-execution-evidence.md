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

## Step 5 — `nopack_sandbox.py` and `trace_writer.py`

The only unordered pair on the list, and the absence of an order is a measured fact rather than
an omission: **neither has an inbound edge of any kind**, so neither can be the other's reason.

```
scripts/nopack_sandbox.py   consumers (0)   edges (1): imports scripts/canonical_docs.py
scripts/trace_writer.py     consumers (0)   edges (0)
```

Four files: `scripts/nopack_sandbox.py`, `tests/test_nopack_sandbox.py`,
`scripts/trace_writer.py`, `tests/test_trace_writer.py`, plus both register rows and both
fixture rows. Unlike the four above, these two leave **no `task-implements` residue at all** —
their only recorded call sites were spent lane contracts, which are immutable and already run.

Targeted tests:

```
tests/test_graph_spine.py tests/test_canonical_docs.py tests/test_decision_coverage.py
tests/test_edge_class_census.py
  -> 2 failed, 172 passed in 365.85s
```

The same two `test_canonical_docs.py` baseline rows, for the third time. Present in the Step 2
baseline set, so not this lane's.

**All six ratified deletions are now landed, in the ratified order.** The `graph-orphan-census`,
`graph-task-coverage` and `graph-process-list` hooks passed on every one of the three commits —
the contract budgeted for them firing, and the reason they did not is that the register rows and
fixture rows left in the same commit as their subjects rather than a commit later.

### The FOREIGN commit block, and why waiting it out was not available

This commit needed a second declared single-hook bypass, and the reasoning is recorded here
rather than only in the commit body because it is the kind of thing a later reader will want to
audit.

`audit.py health` emitted exactly ONE `[!!]` — proven by count, not assumed:

```
uv run --locked python scripts/audit.py health | grep -cE "^\s*\[!!\]"   -> 1
uv run --locked python scripts/audit.py health | grep -oE "^\s*\[!!\] [a-z_]+" | sort -u
  [!!] journal_spine_anchor
```

Its four subjects — `996428f2`, `eb760770`, `0d6b7251`, `87db8060` — are all first-parent spine
entries on the SHARED `main` ref, made by the integrator while this lane ran. Foreignness was
proved, not asserted:

```
git merge-base --is-ancestor <sha> HEAD   -> FOREIGN, all four
git log --merges --oneline c0e0722f..HEAD | wc -l   -> 0
```

Three further facts settle which remedy applies:

1. The discriminator on `87db8060` read **False in this tree AND False at main**, so this is not
   the tree-lag class a sync repairs — the anchors do not exist anywhere yet. `local main` was
   `87db8060` while `git ls-remote origin refs/heads/main` still read `c0e0722f`: unpushed local
   merges, the integrator mid-queue.
2. `batch_manifest.open_batches` returns `[]` — **batch X4 has no manifest**, so the ADR-110
   lane-merge exemption cannot fire for any seat. That is why two of the four are sibling LANE
   merges (`worktree-lane-x-664-dead-callers`, `worktree-lane-x-675-instrument-fixes`) rather
   than only integration branches.
3. The count CLIMBED `1 -> 3 -> 4` across three retries in the same window. Waiting on zero is
   an unsatisfiable fixpoint while a merge queue is being walked, not a delay to sit out.

The contract forbids this lane both available repairs — no JOURNAL entry (the integrator's
surface, `STANDING_RULINGS` P-1) and no merges — so `SKIP=audit-health`, declared and bounded,
is the only remaining act. **The backstop is untouched:** `block-unanchored-push` fails CLOSED at
push time, so a commit-time skip cannot let an unanchored range reach `origin`. Owed to the
integrator: anchor those four, and land the wave-4 manifest so the exemption can fire.

## Step 6 — the Actions TIP run, and the paired diff

| reading | run id | head SHA | pytest tail |
|---|---|---|---|
| baseline | `34757902205` | `c0e0722f` | `55 failed, 5994 passed, 22 skipped in 218.78s` |
| tip | `34763979956` | `f7f04c41` | `54 failed, 5713 passed, 22 skipped in 213.59s` |

Same workflow, same `workflow_dispatch` event, same branch ref, same runner class, both inside
this lane's own run, and both reporting `pyright shape: unprovisioned (modelled: 7/8 proven, 1
skip)`. **The pairing is clean in the one way that matters: the tip is a descendant of the
baseline SHA and nothing from `main` was merged in between.** The integrator moved `main` four
times while this lane ran (Step 5) and none of it was pulled in, so every delta below is this
lane's diff and nothing else's.

### The diff, in full

```
diff baseline-nodeids.txt tip-nodeids.txt
34d33
< FAILED tests/test_gen_north_star.py::test_the_committed_view_is_current
```

**One line. It is a REMOVAL. There are ZERO tip-only failures.**

Item 3's blocking condition — *"a failure present only at tip is [this lane's], and it blocks"* —
is not met, and it is not met by measurement rather than by assertion. The single departing row
is the one Step 2 predicted would leave: `test_gen_north_star.py` was deleted with its module,
and the failure it carried (`ecosystem/north-star.md` already stale against its generator) left
with it. Every one of the other 54 baseline failures is present in both readings and is
therefore not this lane's.

The passing count falls `5994 -> 5713`, which is the 281 test bodies the nine deleted test files
carried. A falling pass count with an unchanged failure set is what a clean removal looks like;
it is recorded here so nobody later reads the drop as a regression.

**This is the leg that carries the weight the oracle cannot** (done-contract item 2). Three of
the six modules verdicted SAFE, one of those SAFE verdicts was demonstrably a false PASS on an
`importlib` edge (Step 1), and the paired run is what turns "the oracle found nothing" into
"nothing broke". `scripts/desired_state_loader.py` is the repo's worked example of the case
where these two answers differ; this run is the one where they agree.

## Step 7 — TRIGGER 1: `archive_row_body.py` onto the pre-commit stage

RED-first, and the RED was OBSERVED before a line of wiring existed. Two witnesses, both run
against the unwired tree:

```
tests/test_archive_row_body.py::test_a_pre_commit_hook_FIRES_archive_row_body_and_not_merely_names_it
  AssertionError: scripts/archive_row_body.py is fired by no pre-commit hook -- it is
  referenced only by this test file, and a test schedules nothing.
  assert []

tests/test_archive_row_body.py::test_the_trigger_row_and_its_disposition_cannot_both_be_live
  AssertionError: archive_row_body.py now has a trigger and still carries an
  ORPHAN_DISPOSITIONS entry
```

**The first witness is the one that matters, and it is written the way it is on purpose.** The
other 47 tests in that file prove the module WORKS. All 47 were green while the census counted
the module an orphan, which is the whole distinction `[#664]` draws: *"a test proves a module
works and schedules nothing, so it is not a trigger."* A test that could not tell the wired tree
from the unwired one would not have discharged this row however thorough it was.

### The wiring

`row-archive-proof`, placed immediately after `validate-backlog` — the census named *"the
pre-commit stage, beside the row-lifecycle gates"* and that is the neighbour.

```yaml
      - id: row-archive-proof
        name: Row-body archival byte-identity proof (legs A-E; [#612]/[#664] TRIGGER)
        entry: uv run --locked python scripts/archive_row_body.py verify
        language: system
        files: '(^BACKLOG\.md$|^tasks/.*\.(md|json)$|^scripts/archive_row_body\.py$)'
        pass_filenames: false
```

Two choices in it are load-bearing and both are pinned by the test rather than left to a
comment:

- **`verify`, never `relocate` or `rerender`.** Those two WRITE — one moves clauses out of a
  live row, the other rewrites a record's prose. A gate reads and refuses; one that edits the
  rows it judges would have Layer 2 mutating the corpus at commit time (Critical Rule #4), and
  relocation is an operator act with a `propose` step in front of it. The test asserts the last
  entry token is `verify`, so a later widening cannot quietly turn this gate into a writer.
- **The selector reaches `tasks/`, not only `BACKLOG.md`.** LEG E enumerates from the ROWS
  precisely so that deleting a record is detectable — *"a verifier that enumerates only what
  exists cannot detect absence"* — and a selector blind to `tasks/archive/` would sit out the
  one change that removes the thing that could complain.

### GREEN, and the trigger is real in the graph rather than only in the config

```
uv run --locked python -m pytest tests/test_archive_row_body.py tests/test_graph_spine.py
  -> 86 passed in 36.68s

uv run --locked python scripts/file_purpose_graph.py why scripts/archive_row_body.py
  consumers (9) ... - is triggered by  file:.pre-commit-config.yaml   [wiring]
```

The `triggers` edge did not exist before this commit and does now. That is the assertion the
row actually wanted, and it is why the module's `ORPHAN_DISPOSITIONS` row and its
`CENSUS_SCRIPT_ORPHANS` entry leave in the same commit: **a wired module is not an orphan**, and
`test_a_disposition_register_entry_cannot_manufacture_its_own_trigger` would RED on a register
row for a reachable process. The row leaves this register in both directions — retired (Steps
3-5) or wired (here) — for one reason: the register holds live rulings about orphans.

`ecosystem/organ-index.md` was regenerated with the generator the hook names
(`generate_organ_index.py --write`), never hand-edited.

### CLAUDE.md §9, and a PRE-EXISTING roster gap found while satisfying it

§9 is not prose: `validate_doc_claims.extract_claimed_hooks` parses that bullet list and
compares it to the live config, so adding a hook without adding its roster line grows a real
drift. The line was added, and `CLAUDE.md`'s `last_reviewed` bumped to `2026-09-13` **in the
same commit** — a separate follow-up commit is the one shape that provably fails the A2 setter
test. The file is 24,258 B against the 24,576 B cap.

Satisfying that surfaced a drift this lane did not create and does not repair:

```
DRIFT  precommit_hook_roster@CLAUDE.md
  doc    = {... row-archive-proof ...}                      (31 ids)
  actual = {... dispatch-conformance, graph-edge-class-census, row-archive-proof ...}  (33 ids)
```

**`dispatch-conformance` and `graph-edge-class-census` are live pre-commit hooks that §9 has
never named.** The drift predates this lane, my line neither caused nor cures it, and adding
two rosters lines for other lanes' hooks is outside this footprint — filed here for the
operator rather than silently absorbed, which is what the check's WARN class is for.

## Step 8 — TRIGGER 2: `logs_retention.py` onto the `SessionStart` path

RED-first again, observed before the wiring:

```
tests/test_logs_retention.py::test_a_session_hook_CALLS_run_retention_and_not_only_the_test_suite
  AssertionError: scripts/logs_retention.py is called by no SessionStart hook -- run_retention()
  still has no production caller ([#655]), and the tests above call it themselves, which
  schedules nothing.

tests/test_logs_retention.py::test_the_retention_trigger_row_and_its_disposition_cannot_both_be_live
  AssertionError: logs_retention.py now has a trigger and still carries an ORPHAN_DISPOSITIONS entry
```

31 of the file's tests were passing at that moment. They prove the retention RULE correct; none
of them makes anything CALL it, which is the entire content of `[#655]`, whose title is *"`run_retention()` has no production caller"*.

### The wiring, and WHY `SessionStart` rather than `Stop`

```json
{ "type": "command",
  "command": "uv run --locked python \"$CLAUDE_PROJECT_DIR/scripts/logs_retention.py\"",
  "timeout": 20 }
```

appended to `SessionStart` in `.claude/settings.json`. The census offered *"the
`SessionStart`/`Stop` path that writes the logs it would retain"* and left the choice open, so
the choice is recorded as an assertion
(`test_the_retention_trigger_is_on_SESSION_START_not_STOP_and_the_reason_is_pinned`) rather than
as a comment a later reader can miss:

- The producer of the files this rule retains is `propose_closures.py`, fired by the
  tier1-lifecycle plugin's **Stop** hook. Wiring the renamer into that same event puts a
  relocator and that producer's own `**/PROPOSALS-*.md` read inside one event, for no gain:
  relocation at the next session's start reaches exactly the same files, one session later,
  with nothing racing it.
- The plugin's `hooks.json` is a deploy-carried surface with a derived-copy registry behind it;
  editing it is an AX4-1 floor-declaration act. `.claude/settings.json` is this repo's own
  project surface and is one of FPG-1's five in-tree `WIRING_SURFACES`.
- Relocation is safe for the consumer by construction, not by luck: lane-c-3 (2026-09-01)
  re-pointed all three `PROPOSALS-*` globbers at `**/PROPOSALS-*.md` — bucketed AND flat — and
  only then retired this module's prefix exemption. That sequencing is what makes a
  session-start relocation harmless to the closure detector's pending-window baseline.
- The command is asserted NOT to carry `--dry-run`. A retention rule wired in report-only mode
  would satisfy a grep for the module name and leave `[#655]` exactly as open as it is.

### GREEN, and the second trigger edge is real

```
uv run --locked python -m pytest tests/test_logs_retention.py tests/test_graph_spine.py
  -> 70 passed in 17.09s

uv run --locked python scripts/file_purpose_graph.py why scripts/logs_retention.py
  consumers (4) ... - is triggered by  file:.claude/settings.json   [wiring]
```

Register row and fixture row leave with it, same rule as Step 7. `ecosystem/organ-index.md`
regenerated with its own generator.

**CLAUDE.md was deliberately NOT touched in this commit.** Its `last_reviewed` was bumped to
`2026-09-13` in Step 7, and `audit.py health` confirms `CLAUDE.md … declared 2026-09-13 …
derived 2026-09-13 (de2f3e6e9) … gated-and-fresh`. A second content commit to it on the SAME
DAY would flip it gated-and-stale with no expressible repair — rewriting the stamp to the value
it already holds produces no diff, so the setter SHA does not move. §9's machine-read surface
(the pre-commit bullet list `validate_doc_claims` parses) is already correct; §9's session-hooks
paragraph is summary prose that already abstracts over three of the six `SessionStart` commands,
so it is left as it is rather than paid for with an unrecoverable freshness flip.

### One owed declaration, named rather than absorbed

`fleet_parity` will report the new hook as
`settings-local-blocks WARN-undeclared: settings.json hook command not hub-carried and not
manifest-owned` — the same class the live `conductor.py session-start` hook already carries, and
already visible in the Step 2 baseline through
`tests/test_audit.py::test_check_fleet_parity_green_on_live_repo`. Curing it means registering
the component in `deploy/manifest-v1.5.0.yaml` / `ecosystem/parity-surfaces.yaml`, which is an
AX4-1 floor-declaration act — the register itself states that a new hook needs one and that the
surface *"is not this lane's to write"*. **Owed: the floor declaration for
`scripts/logs_retention.py`'s SessionStart hook.**

## Step 9 — the register corrections

This step's contract item had two halves. **One was already discharged by `main` before this
lane ran** (Step 0), so only the telemetry half is executed here.

### `cost_usage_telemetry.py` — the text read as a DELETE; the ruling is KEEP

The stale text was `_LANE_BUILT` plus *"only call site is LANE-f-6-observability-otel.md:27"* —
lane-built-and-never-adopted, with a spent lane contract for a call site. That reads as a
retirement candidate, and it is how `[#664]`'s census found the module. FPG-1 says otherwise,
and it was consulted rather than assumed:

```
uv run --locked python scripts/file_purpose_graph.py why scripts/cost_usage_telemetry.py
  consumers (3) ... - is imported by  file:scripts/provider_router.py   [wiring]
```

So the module is an **ADOPTED library whose ADOPTER is untriggered** — a materially different
condition from an unadopted organ, with a different remedy. The replacement text says that, cites
`[#694]`'s PARTIALLY DISCHARGED ruling and the real call site, and re-owns the row to `[#691]`
Half B jointly with the `provider_router.py` row it now inherits: the two are adopted by ONE act
(Half B routing through the router), and wiring the telemetry module on its own would place
exactly the non-Claude call AX23-2 forbids.

`102 passed`, `ruff` clean.

### `worktree_seed.py` — NOT executed, because it was already done

Done-contract item 7 arrived on `main` at `c0e0722f` before this lane's first commit (Step 0),
with the four-line register row already deleted and
`test_a_disposition_register_entry_cannot_manufacture_its_own_trigger` already green. The
contract's framing — *"Two prior lanes declined this one-line edit as a V-2 class (a)
curated-baseline touch. The operator has now ruled it … make the edit"* — is satisfied, by
someone else. Re-making it would be a no-op or a conflict, so nothing was done and the fact is
reported. This is the lane's one refuted premise.

## Step 10 — the end-of-lane packet

This section is the lane's handback. Everything above it is the working record; this is what an
integrator, a reviewer or the operator reads if they read nothing else.

### The lane, as landed

Base `c0e0722f`. Ten commits, one per contract step, no squash, no amend.

```
step 1  c2eb3501  docs(x-664): provision the oracle, record all six DELETE verdicts, disclose one refuted premise
step 2  cb0cf65c  docs(x-664): record the Actions BASELINE -- 55 nodeids at c0e0722f, in full
step 3  c9ea3b07  feat(x-664): retire gen_trend_dashboard, then gen_north_star -- module, tests, disposition, fixture row
step 4  3a380fd8  feat(x-664): retire window_metrics, then failed_set -- module, test, disposition, fixture row
step 5  f7f04c41  feat(x-664): retire nopack_sandbox and trace_writer -- the last two of the ratified six
step 6  c971e45e  docs(x-664): the Actions TIP run -- zero tip-only failures, the pairing measured
step 7  de2f3e6e  feat(x-664): TRIGGER 1 -- archive_row_body verify onto the pre-commit stage, RED-first
step 8  d418d337  feat(x-664): TRIGGER 2 -- logs_retention onto the SessionStart path, RED-first
step 9  b7f68efb  fix(x-664): correct cost_usage_telemetry's stale disposition -- it is a KEEP, not a DELETE
step 10 (this commit)
```

`git diff --shortstat c0e0722f..HEAD` at step 9: **22 files changed, 1004 insertions(+),
8635 deletions(-)**. Twelve files deleted — the six ratified modules and the six dedicated test
files that only existed to test them.

The base was taken ONCE, at `c0e0722f`, and `main` was deliberately **never merged again** after
that sync (Step 0). Every commit above is therefore a pure descendant of the baseline commit, and
the paired Actions diff below is attributable to this lane alone rather than to whatever the
integrator landed on `main` while the lane ran.

### The oracle verdicts — all seven runs, recorded verbatim above

Done-contract item 1 required the `safe_remove` oracle **provisioned** and **run over all six
candidates before any deletion**, with every verdict recorded verbatim. That is Step 1: the
vendoring of the pinned langserver (§*Precondition*), seven runs — six single-module and one
whole-set — at §*Run 1* … §*Run 7*, and the summary at §*The verdict-vs-act ledger*:

```
gen_trend_dashboard.py  REVIEW  (downgraded by its own two dedicated test files)
gen_north_star.py       SAFE    (a FALSE PASS on the importlib edge -- see Step 1)
window_metrics.py       REVIEW  (downgraded by its own dedicated test file)
failed_set.py           SAFE
nopack_sandbox.py       SAFE
trace_writer.py         REVIEW  (downgraded by its own dedicated test file)
all six as one set      -- run 7, the shape the lane actually performs
```

Done-contract item 2 was honoured rather than recited: no SAFE verdict was treated as a licence.
Step 1 §*What the oracle did NOT see* records the concrete false-PASS class this oracle has —
and records that `gen_north_star.py`'s own SAFE verdict sits on it.

### The Actions readings — four runs, of which two are the contract's pair

Same workflow (`report-only-wall.yml`), same runner class, adjacent in time, `workflow_dispatch`
at a pinned SHA each time.

```
reading                    run id       head SHA   pytest tail
superseded baseline        34756963263  dbac84b8   54 failed, 5996 passed, 21 skipped, 177.89s
BASELINE OF RECORD         34757902205  c0e0722f   55 failed, 5994 passed, 22 skipped, 218.78s
TIP (contract item 3)      34763979956  f7f04c41   54 failed, 5713 passed, 22 skipped, 213.59s
supplementary, post-wiring 34766329800  b7f68efb   54 failed, 5718 passed, 22 skipped, 211.75s
```

The first reading is **superseded, not hidden**: it was taken at `dbac84b8` before the forced
sync moved the lane's base (Step 0). Reusing it would have measured a base this lane never built
on. It is kept because deleting a measurement you took is how a pairing stops being falsifiable.

**The pair of record is `34757902205` → `34763979956`.** Both failure sets are recorded in full
rather than counted (Step 2 §*The baseline failure set of record*, Step 6 §*The diff, in full*),
because item 3's rule is a set operation and a count cannot perform it. The diff is one line, and
it is a REMOVAL:

```
=== DIFF baseline(c0e0722f) -> tip(f7f04c41) ===
34d33
< FAILED tests/test_gen_north_star.py::test_the_committed_view_is_current
```

**Zero tip-only failures.** The single change is a baseline failure that left with the file that
produced it.

### The supplementary run, and why it exists

The contract's tip run is step 6, which by construction predates the two TRIGGER wirings of steps
7 and 8. A pairing that stops before the last two commits does not measure the last two commits.
So a fourth run was fired at the true final tip `b7f68efb`, beyond the contract's ask:

```
=== DIFF baseline(c0e0722f) -> final tip(b7f68efb) ===
34d33
< FAILED tests/test_gen_north_star.py::test_the_committed_view_is_current
```

Still exactly one line, still a removal, still zero tip-only failures **after** the wirings. The
two new trigger surfaces cost the suite nothing.

This also discharges the breadth question the local selector declined to answer:
`impacted_tests.py select --ref HEAD~7` returns `# FULL SUITE -- the selector declined to
narrow`. Running a full suite locally in a lane is exactly what `[#528]` forbids; running it on
Actions at the tip is what the contract already asked for. The lane kept to targeted tests
locally and paid for breadth on the runner.

### Local targeted tests — the final run

Ten files covering the whole lane footprint, `uv run --locked`:

```
tests/test_graph_spine.py tests/test_archive_row_body.py tests/test_logs_retention.py
tests/test_enforcement_coverage.py tests/test_prompts_guard_hook_wiring.py
tests/test_carrier_hooks_source.py tests/test_floor_mechanisms.py tests/test_hook_telemetry.py
tests/test_decision_coverage.py tests/test_edge_class_census.py

2 failed, 346 passed in 748.97s (0:12:28)
  FAILED tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
  FAILED tests/test_floor_mechanisms.py::test_pre_existing_components_are_untouched_by_the_mechanism_reader
```

**Both failures are in the baseline failure set of record**, recorded above at Step 2 before this
lane deleted anything — they are lines 15 and 19 of that 55-nodeid block. By item 3's own rule
(*a failure present in BOTH readings is not this lane's*), neither is the lane's, and neither is
repaired here: `test_pre_existing_components_are_untouched_by_the_mechanism_reader` asserts a
manifest component count (`assert 22 == 21`) over `deploy/manifest-v1.5.0.yaml`, a curated
baseline this lane is barred from touching, and the anchor-gate probe test is the same
`journal_spine_anchor` condition documented at Step 5. The lane's own targeted suites were green
at every step (`102 passed` at step 9; `70 passed` at step 8).

### Every V-2 decision TAKEN rather than asked

The budget admits escalation on three classes only — (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling — and AX27-1 forbids waiting
on the operator mid-run. Each decision below was checked against those three and resolved in
lane. The column that matters is the last one.

**1. Co-removing each module's dedicated test file with the module.** Three of six verdicts are
REVIEW, and in every case the downgrade is a hit inside the module's own dedicated test file.
*Not a fork class:* the `[#734]` precedent already rules it — *"DELETED with their dedicated
tests and their `ORPHAN_DISPOSITIONS` entries"*. A REVIEW whose only surviving reference leaves
in the same commit is not a surviving reference.

**2. Keeping `ecosystem/north-star.md` and `README.md:74`.** Both now name a generator that no
longer exists. *Nearest to class (a), and that is the reason to leave them:* `[#624]` holds a
live `implements` edge to the artifact, and the contract says in terms *"Do not close or rewrite
another lane's row to make a gate green."* Deleting the artifact would orphan `[#624]`'s edge on
top of the module edges the contract already anticipated. Left, and named below as owed.

**3. `SessionStart` rather than `Stop` for `logs_retention.py`.** *Would have been class (c) had
there been nothing to reason from;* there was. The producer of the files being retained runs on
the plugin's `Stop` hook and re-reads `**/PROPOSALS-*.md` in that same event; the plugin's
`hooks.json` is a deploy-carried surface and editing it is an AX4-1 act, whereas
`.claude/settings.json` is this repo's own project surface and one of FPG-1's five in-tree
`WIRING_SURFACES`; and lane-c-3 already re-pointed all three globbers at recursive paths, making
relocation safe by construction. The choice is pinned by a **test**, not a comment —
`test_the_retention_trigger_is_on_SESSION_START_not_STOP_and_the_reason_is_pinned`.

**4. Editing `CLAUDE.md` §9 and bumping its `last_reviewed` in the SAME commit.** *Class (a) on
its face — `CLAUDE.md` is curated.* Taken anyway because item 5 requires a live pre-commit hook
and `validate_doc_claims.extract_claimed_hooks` parses §9's bullet list, so wiring the hook
without rostering it lands a self-contradicting tree. Both halves went into `de2f3e6e` because
`canonical_freshness` A2 identifies a stamp by the commit that ADDED the line and a same-day
re-stamp is not expressible. `audit.py health` reads the file `gated-and-fresh` afterwards. The
file was then **deliberately not touched again** for the rest of the lane, including here.

**5. The two declared single-hook bypasses.** *Class (b) territory, resolved by reading the
contract's own reservation rather than by asking.* `doc-counts-pytest-freshness` and
`gen_audit_index` are index regeneration, which the contract reserves to the integrator as
gate-of-record — so the hooks were SKIPped with the exact delta declared in each commit body,
never `--no-verify`, and never more than one named hook per reason. `audit-health` was SKIPped
from step 5 onward for `journal_spine_anchor` firing on **FOREIGN** unanchored merges on the
shared `main` ref: proved foreign for all four SHAs (`git merge-base --is-ancestor <sha> HEAD` →
FOREIGN ×4; `git log --merges --oneline c0e0722f..HEAD` → 0), proved `batch_manifest.open_batches`
returns `[]` so no ADR-110 exemption was available to anyone, and proved the backstop
`block-unanchored-push` still fails CLOSED at push time. Full reasoning in `f7f04c41`.

**6. Building this artifact incrementally across the lane's commits.** *Would be a rule-vs-ruling
conflict if `docs/audits/` immutability bound before landing.* It does not: `git log --follow` on
the `[#734]` precedent shows it created at `6214cbd5` and edited across four later commits of the
same lane. Immutability binds after landing.

**7. Re-taking the baseline at `c0e0722f` after the forced sync.** A baseline measured at a base
the lane never built on is not a baseline. Both readings are kept.

**8. Firing the supplementary Actions run.** Beyond the contract's ask, for the reason given
above. Extra evidence, never a substitute for the pair of record.

### Residue left deliberately, and owed to the operator

Named here because the contract says to name it rather than sweep it.

- **`ecosystem/north-star.md`** — the deleted generator's committed output; header names a
  script that no longer exists. `[#624]` holds a live `implements` edge to it.
- **`README.md:74`** — points a reader at both the artifact and the generator.
- **`scripts/assemble_paste.py:30-41`** — narrative comment naming `scripts/window_metrics.py`
  twice as the importer of `PASTE_BUDGET_BYTES`. Comment only; no code path.
- **`scripts/canonical_docs.py:50` and `:130-131`** — prose naming `nopack_sandbox.NEVER_REMOVE`
  as one of two literal-path matchers. Comment only; no code path.
- **The `task-implements` rows still naming a deleted file** — `[#589] [#615] [#694] [#470]
  [#611] [#689] [#383] [#624]`. Left untouched on the contract's explicit instruction: *"Do not
  close or rewrite another lane's row to make a gate green."* Each is another lane's surface.

`ecosystem/trends.html` needed no decision — `gen_trend_dashboard.py`'s docstring records it as
`regenerated on demand; NOT committed`, and `git ls-files` confirms it untracked.

### Owed at integration

**Integrator:**
1. `gen_doc_counts.py --write` — `pytest_collected` and `precommit_hook_count` both moved. The
   exact deltas are declared in the body of every commit that SKIPped the hook.
2. `gen_audit_index.py --write` — this artifact is new and the index is generated.
3. Anchor the foreign spine entries, or land the wave-4 batch manifest so ADR-110's lane-merge
   exemption can fire. `batch_manifest.open_batches` currently returns `[]`.
4. Run the full suite once, at integration, per `[#528]`.

**Operator:**
5. The **AX4-1 floor declaration** for the new `logs_retention.py` `SessionStart` hook —
   `deploy/manifest-v*.yaml` + `ecosystem/parity-surfaces.yaml`. Until it lands, `fleet_parity`
   WARNs the hook as *not hub-carried and not manifest-owned*, the same class the live
   `conductor.py` hook already carries. The register itself says this surface is not a lane's to
   write.
6. The **§9 roster gap**: `dispatch-conformance` and `graph-edge-class-census` are live
   pre-commit hooks that `CLAUDE.md` §9 has never rostered. Pre-existing, found while satisfying
   item 5, not repaired — §9 is a curated surface and `CLAUDE.md` is byte-capped and already
   re-stamped today.

### Findings filed, not repaired

1. **`safe_remove._bare_stem_literal_hits` misses `"<stem>.py"` literals.** The downgrade scan
   looks for the bare stem, so a reference written with its extension inside a string does not
   trigger REVIEW. Owner `[#195]` / ADR-89. This widens the false-PASS class ADR-89 already
   declares; it does not change any verdict in this lane, because every act here was gated on
   the paired Actions pair rather than on the oracle.
2. The §9 roster gap (above).
3. The `fleet_parity` WARN (above).

### One unresolvable locator

The contract cites **`to-browser/RATIFICATION-2026-09-13.md`** as the GO authorising this lane.
That path does not exist anywhere in the tree — not at the lane base, not on `main`, not on any
branch. The lane proceeded on the frozen contract itself, which is the artifact actually in hand.
Reported rather than assumed resolved: a locator you have not opened is a claim, not evidence.

### The done-contract, item by item

```
1  oracle provisioned + run over all six BEFORE deletion, verdicts verbatim  DONE   Step 1
2  SAFE is necessary, not sufficient -- the false-PASS class honoured        DONE   Step 1
3  paired baseline/tip on Actions, both run ids + both failure sets          DONE   Steps 2, 6
4  six deletions IN THE RATIFIED ORDER                                       DONE   Steps 3-5
5  two TRIGGER rows, RED-first, ONE ROW PER COMMIT                           DONE   Steps 7, 8
6  cost_usage_telemetry's stale DELETE text corrected to the KEEP ruling     DONE   Step 9
7  worktree_seed's ORPHAN_DISPOSITIONS entry deleted, module stays           ALREADY DONE
                                                                             BY MAIN at c0e0722f
                                                                             -- Step 0, the
                                                                             lane's one refuted
                                                                             premise
8  English, hyphen-only names, logging not print, Click, targeted tests      DONE   throughout
```

### Where the lane stops

`git status` clean. `git stash list` **empty**. Ten commits on
`worktree-lane-x-664-delete-list-execution`, pushed to the lane's own remote ref only.

**No merge. No push to `main`. No other lane's branch touched. No JOURNAL entry** — the JOURNAL
is the integrator's surface under `STANDING_RULINGS` P-1. **No index regeneration** — the
integrator is gate-of-record. Integration is the integrator's act, not this lane's.
