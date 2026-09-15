# SUITE BASELINE FREEZE — batch Z

> **This freeze is a FILE, not a number.** A merge is judged against THIS SET, member by
> member. Operator ruling 2026-09-15: freeze, do not triage to green tonight.

## The measurement

| | |
|---|---|
| **Measured at SHA** | `b5270d636774abedff1b00cb0a9c7fb3698c226e` (`main`, batch Y close packet merge) |
| **Source** | Actions `conductor` run **34901604346**, `push`, 2026-09-14T21:57:23Z |
| **Command** | `uv run --locked pytest -q --tb=short` |
| **Result** | **51 failed, 5863 passed, 22 skipped, 2 xfailed** in 229.75 s |
| **Workers** | **4** (`gw0`–`gw3`), from `addopts = "-n auto"` on `ubuntu-latest` |
| **Frozen on** | 2026-09-15, integrator seat, batch Z night |

**The worker count is NOT fixed in config — it is `auto`.** It resolved to 4 on a
GitHub-hosted `ubuntu-latest` runner. A runner with a different core count re-partitions the
suite and can flip cross-worker-sensitive members (C9 is exactly that class). **Any
re-measurement for comparison against this freeze must report its own resolved worker count,
and a comparison across different worker counts is not a like-for-like comparison.**

### AMENDMENT 2026-09-15 — the worker count is now PINNED, because a consumer is about to depend on it

**Added in place rather than by re-measurement.** The paragraph above stands and is correct; what
follows removes the ambiguity it describes, and nothing above it is altered.

**THE PIN: `-n 4`.** Any run compared against this freeze **MUST** resolve to **4 workers**, the
count this freeze was measured at. The comparison command is therefore

```
uv run --locked pytest -q --tb=short -n 4
```

— **not** the `-n auto` of `addopts`, which is what produced the ambiguity. `auto` resolved to 4
on this freeze's GitHub-hosted `ubuntu-latest` runner and will resolve to something else on any
runner with a different core count.

**Why this is pinned NOW and not left as a caveat.** `[#790]` makes the conductor workflow compare
every push against this set. A consumer that compares automatically cannot read a warning; it
needs a number it can assert. An unpinned worker count in a file a gate depends on is the
"declared enforcement without enforcement" shape this repo has measured three times this week.

**What a consumer MUST do with the pin, so the gate cannot silently compare across regimes:**

1. **Resolve and REPORT** its own worker count before comparing — never assume `auto` gave it 4.
2. **REFUSE on mismatch.** A run at any count other than 4 is **NOT-COMPARABLE**, and
   not-comparable is a **failure to report**, never a pass. Falling back to comparing anyway is
   the fail-open behaviour the pin exists to prevent.
3. **Treat a missing or stale freeze file the same way** — fail, do not pass blind. Staleness is
   checkable against this file's own `Measured at SHA` and `Source` run id.

**HONEST LIMIT, stated because the pin does not remove it.** Pinning `-n 4` makes runs
*comparable*; it does **not** make this baseline fully *reproducible*. The batch-Z close packet
records that the same tree measures **51 or 52** — at least one member flaps independently of
worker count (C9 is the cross-worker-sensitive class, and it is not the only source of variance).
A consumer must therefore carry a stated policy for the flapping member rather than treating each
flap as a regression. **Pinning the worker count narrows the variance; it does not eliminate it,
and a gate built as though it did will be red every other run.**

**This pin expires with the freeze.** Re-measured at the next batch close, at `-n 4`, and the new
freeze restates its own pin — `[#763]`.

## The judging rule

- A failure **inside** this set is **PRE-EXISTING**. It does not refuse the merge.
- A failure **outside** this set is a **REGRESSION**. It **refuses the merge**.
- Membership is by **test node id**, listed in full below — not by count, and not by file.
  A file with 3 frozen members that fails 4 has a regression, and the count alone hides it.
- A member that **passes** is not a failure of this rule; it is the expected direction.

## The expiry — this is a freeze, not a new normal

**Re-measured at the next batch close.** For every cause whose lane has merged, that cause
**must have left the set**. If the number has not fallen, **that is a row, not a new normal**.
Causes with a lane in batch Z are marked below.

## The 51, grouped by cause

| Cause | Count | Lane in batch Z? |
|---|---|---|
| **C1** — Intake frontmatter unreadable (Z-G4) - ONE file: docs/intake/2026-09-11-tech-batch-x-roster.md parses to {} | 6 | no |
| **C2** — audit.py health emits an 'operational:' line / telemetry flag defaults | 6 | YES — lane 1 (cost telemetry wired) |
| **C3** — Committed baseline vs live corpus DRIFTED (a count or roster moved; the corpus grew past a frozen figure) | 11 | partial — lane 9 (ARCHITECTURE) touches one member |
| **C4** — Runner-vs-Windows environment assumption (POSIX runner path vs Windows-authored expectation) | 4 | no |
| **C5** — FAIL-OPEN: a guard that must refuse does not refuse (or refuses constantly, discriminating nothing) | 3 | YES — lanes 2 & 3 (decision engine / spine witnessed) |
| **C6** — Date-driven freshness (a stamp vs a derived date; flips with the calendar, not with a commit) | 2 | no |
| **C7** — prompts-dir normalisation refuses a benign form (trailing separator, case difference) | 2 | no |
| **C8** — BACKLOG over its byte bar (94,255 B vs 72,000 B) | 1 | YES — lane 7 (BACKLOG to bar) |
| **C9** — xdist frozenset identity (a spec-derived constant is not the same object across workers) | 1 | no |
| **C10** — Regex / parser precision defect (over- or under-matching) | 6 | no |
| **C11** — Declared-but-unbuilt, or two surfaces disagree about live state | 9 | no |
| **TOTAL** | **51** | |

### C5 is not cosmetic — read it before dismissing this set as noise

Three members assert that a guard **refuses** and it does not: `a mid-evaluation crash must
refuse, not permit` and `an unrecognised verdict must refuse, not permit` (deny-and-point),
plus an anchor-gate probe that **refuses a correctly-anchored push too**, so it discriminates
nothing — `a constant refusal enforces nothing`. **A fail-open guard inside a frozen baseline
is a guard nobody is watching.** These are frozen as PRE-EXISTING for merge-judging only;
they are not thereby accepted as correct.

## The roster — membership is by node id

### C1 — Intake frontmatter unreadable (Z-G4) - ONE file: docs/intake/2026-09-11-tech-batch-x-roster.md parses to {}  (6)

```
tests/test_funnel_lifecycle.py::test_live_tree_leg_a1_is_location_sensitive
tests/test_funnel_lifecycle.py::test_live_tree_leg_b_measures_zero_and_the_reason_is_recorded
tests/test_funnel_lifecycle.py::test_live_tree_leg_c_measures_zero_so_arming_cannot_red_a_clean_tree
tests/test_funnel_lifecycle.py::test_live_tree_reproduces_the_census_finding
tests/test_gen_handoff.py::test_funnel_health_renders_no_unavailable_against_the_live_repo
tests/test_governance_health.py::test_shared_fields_equal_fm4_block_byte_for_byte
```

### C2 — audit.py health emits an 'operational:' line / telemetry flag defaults  (6)

```
tests/test_audit.py::test_health_ok_with_registered_repo
tests/test_audit.py::test_health_stays_ok_with_na_status
tests/test_audit_parallel.py::test_health_accepts_the_parallel_flags_and_defaults_to_serial
tests/test_telemetry_wiring.py::test_a_wired_health_run_puts_no_telemetry_line_on_stderr
tests/test_telemetry_wiring.py::test_health_exposes_the_telemetry_flag_and_defaults_to_off
tests/test_telemetry_wiring.py::test_the_env_switch_turns_health_on_and_the_explicit_flag_still_wins
```

### C3 — Committed baseline vs live corpus DRIFTED (a count or roster moved; the corpus grew past a frozen figure)  (11)

```
tests/test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it
tests/test_doc_code_edge.py::test_edge_check_registered_and_resolves_starter_set
tests/test_floor_mechanisms.py::test_pre_existing_components_are_untouched_by_the_mechanism_reader
tests/test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement
tests/test_gen_handoff.py::test_dogfood_generated_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_dogfood_no_probe_row_carries_an_answer_value
tests/test_gen_handoff.py::test_epic_bundle_has_no_failing_probe
tests/test_gen_handoff.py::test_suffixed_bundle_probes_resolve_against_their_own_directory
tests/test_proof_layer.py::test_the_live_guard_population_is_at_or_below_its_baseline
tests/test_validate_adr_status.py::test_shipped_corpus_grammar_distribution_matches_the_measured_baseline
tests/test_validate_adr_status.py::test_shipped_corpus_parses_one_status_field_per_live_adr
```

### C4 — Runner-vs-Windows environment assumption (POSIX runner path vs Windows-authored expectation)  (4)

```
tests/test_gen_handoff_preflight.py::test_session_slug_matches_a_REAL_session_store_directory_name
tests/test_offload_admission.py::test_a_destination_REPLACED_during_publication_is_REPORTED_not_silently_used
tests/test_offload_admission.py::test_the_probe_cli_REPORTS_a_replaced_destination_rather_than_reporting_success
tests/test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused
```

### C5 — FAIL-OPEN: a guard that must refuse does not refuse (or refuses constantly, discriminating nothing)  (3)

```
tests/test_deny_and_point.py::test_a_CRASH_MID_EVALUATION_fails_CLOSED
tests/test_deny_and_point.py::test_an_UNRECOGNISED_VERDICT_fails_CLOSED
tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
```

### C6 — Date-driven freshness (a stamp vs a derived date; flips with the calendar, not with a commit)  (2)

```
tests/test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival
tests/test_canonical_docs.py::test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date
```

### C7 — prompts-dir normalisation refuses a benign form (trailing separator, case difference)  (2)

```
tests/test_fleet_health.py::test_prompts_dir_case_difference_is_not_staleness
tests/test_fleet_health.py::test_prompts_dir_trailing_separator_is_not_staleness
```

### C8 — BACKLOG over its byte bar (94,255 B vs 72,000 B)  (1)

```
tests/test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar
```

### C9 — xdist frozenset identity (a spec-derived constant is not the same object across workers)  (1)

```
tests/test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object
```

### C10 — Regex / parser precision defect (over- or under-matching)  (6)

```
tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_normalises[
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_off_repo_input_defect
tests/test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_wrong_id_citation
tests/test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration
tests/test_reverse_dep_oracle.py::test_position_points_at_name_not_keyword
tests/test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers
```

### C11 — Declared-but-unbuilt, or two surfaces disagree about live state  (9)

```
plugins/tier1-lifecycle/tests/test_plugin_paths.py::test_propose_operates_on_host_repo_not_plugin
tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
tests/test_desired_state_loader.py::test_live_repo_loads_clean_and_writes_nothing
tests/test_desired_state_schema.py::test_enums_match_parity_surfaces_on_disk
tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
tests/test_gen_ledger.py::test_the_worktree_line_counts_lanes_rather_than_trees
tests/test_handoff_modes.py::test_boot_carries_both_postures
tests/test_routing_agreement.py::test_the_live_table_is_well_formed
tests/test_v6_frozen_contract.py::test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped
```

## Discrepancy against the causes named at freeze time — RECORDED, NOT SILENTLY DROPPED

The freeze was ordered with two causes described as already known: **a missing optional
dependency (~17)** and **module-shadowing (~5)**. **Neither appears in this measurement.**
Searched run 34901604346 for `ModuleNotFoundError`, `ImportError` and `No module named`:
**0 matches.** No member of this set is an import or dependency failure; the 51 are
assertion failures against live repo state, plus one pydantic `ValidationError`.

The largest real classes are **C3 baseline drift (11)**, then **C1 (6)**, **C2 (6)** and
**C10 (6)** — no cause reaches 17.

**If the ~17/~5 figures came from a LOCAL run, they describe a different baseline on a
different substrate and must not be conflated with this one.** A local Windows run has
failure modes this runner cannot have (and vice versa — C4 is four members that exist only
because the runner is POSIX). **This freeze is the CONDUCTOR's set, at the SHA named above.**
A local baseline, if one is wanted, is a separate measurement and a separate file.

---

## AMENDMENT 2026-09-15 — the set has a member whose outcome depends on the SHA you measure at

**Recorded by APPEND. The roster above is not edited; this section qualifies it.**

### What happened

The judging rule was exercised twice tonight, both times by **node-id diff** rather than by
count, and the second time it refused.

| measured at | conductor run | failed | passed | outside the frozen 51 | departed |
|---|---|---|---|---|---|
| `4f4186a6` (lane z-746 merge) | `34923007619` | 51 | 5946 | **0** | 0 |
| `70356500` (docs arc merge)   | `34925873604` | **52** | 5945 | **1** | 0 |

The one outside the set:

```
tests/test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable
AssertionError: assert {'backlog-id','file-line','heading'} == {'backlog-id','file-line','heading','sha'}
Extra items in the right set: 'sha'
```

### Why it is NOT breakage the merge introduced

The test reads the **live repository's own HEAD**:

```python
head = subprocess.run(["git","-C",str(_REPO_ROOT),"rev-parse","--short","HEAD"], ...)
body = (f"# C\n\n- `scripts/audit.py:1`\n- `{head}`\n- [#383]\n" ...)
assert {c.kind for c in report.checked} == set(pf.CLAIM_KINDS)
```

and asserts the `sha` claim class is extractable from it. **`preflight_contract` silently
skips a short SHA that is all digits** — it reads as a number, not a locator. Reproduced
directly, four inputs, one variable:

```
70356500  all-digits=True   extracted=['backlog-id','file-line','heading']
12345678  all-digits=True   extracted=['backlog-id','file-line','heading']
4f4186a6  all-digits=False  extracted=['backlog-id','file-line','heading','sha']
aad0acdd  all-digits=False  extracted=['backlog-id','file-line','heading','sha']
```

`70356500` is all digits. The merge changed no code this test touches; it changed **what
main's HEAD hashes to**, which every merge does. The defect is latent and pre-existing —
it was latent at `b5270d63` too, which is exactly why the frozen roster does not contain it.

### What this means for the freeze, stated so it is not discovered again

1. **THE BASELINE IS NOT FULLY REPRODUCIBLE.** At least one member's outcome is a function
   of the SHA it is measured at, not of the tree. Re-measuring this freeze at a different
   commit can return 51 or 52 with **no change to the code**. Roughly 2.3% of commits
   ((10/16)^8) have an all-digit short SHA, so this fires about one commit in forty-four.
2. **THE EXPIRY ROW `[#763]` MUST NOT READ A BARE COUNT.** Its condition — "if the number
   has not fallen, that is a row" — is unsafe against a set that can move by ±1 for free.
   `[#763]` is to be discharged on the **node-id diff**, never the total.
3. **THE RULE ITSELF BEHAVED CORRECTLY AND SHOULD NOT BE WEAKENED.** It refused, it named
   the member, and the member was a real defect nobody had recorded. A rule that had
   compared counts would have reported "51 → 52, one regression" with no idea which, and a
   rule that tolerated ±1 would have said nothing at all. **The instrument found something
   true on its first refusal**; the correct response is to fix the defect, not to widen the
   band.

### Disposition

The underlying defect — `preflight_contract` skipping an all-digit short SHA — is a
**CANDIDATE** under the ADR-111 funnel. It is **not** filed as a ratified row here: the only
path from finding to row is CANDIDATE → intake (ADR-98) → ratification, and ratification is
the operator's act, not the integrator's. It is recorded here and in JOURNAL 2026-09-15 (g)
so that it cannot be lost between batches.

**This failure is NOT absorbed into the frozen set.** Adding it would convert a live defect
into an accepted one by the act of noticing it, which is the precise failure mode a freeze
with an expiry exists to prevent.
