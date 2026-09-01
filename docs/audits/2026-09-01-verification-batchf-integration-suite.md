# BATCH F — THE INTEGRATION SUITE RUN, and what it does to the L5 verdict

- **Class:** verification · **Date:** 2026-09-01 · **Arc:** `[#614]` / `[#632]` / `[#528]`
- **Author:** CC (Opus 5, batch-F integrator seat) · **Consumed by:** the batch-F close packet §9

> The close packet's honest-limits section stated: *"No full-suite run at integration ... the
> suite's state is MEASURED but its attribution is OPEN."* **This file closes that gap.** The
> packet is immutable; this supersedes its §9 second bullet rather than editing it.

## 1 · THE RUN

```
command   uv run --locked pytest --tb=no -q       (ADR-106: never a bare pytest)
tree      5c2495c6, main, clean, ALL batch-F merges + the v7 bundle in
result    13 failed · 4843 passed · 4 skipped · 1 xfailed
wall      1137.97 s (18:57), serial-equivalent on a workstation with no lanes running
```

## 2 · WHAT IT DOES TO `[#632]`'s L5 VERDICT — the load-bearing consequence

The proof lane reported **L5 LONG-RUN RED** in the codespace (17 failed / 4759 passed at tree
`e96ad50c`) and attributed the failures to *"pre-existing app-level failures unrelated to the
container."* **Terra refused that attribution** — correctly: a post-stash rerun proves the
failures survive without the session's untracked files, not that they are independent of
Codespaces.

**This run supplies the missing evidence: the workstation ALSO fails.** A RED suite is not a
property of the container. That was the open question, and it is now answered in the direction
the lane guessed but could not prove.

**IT IS NOT A CONTROLLED COMPARISON, AND MUST NOT BE READ AS ONE.** The two runs are at
DIFFERENT TREES — `e96ad50c` in the codespace against `5c2495c6` here, with eight merges
between them — so the 17-vs-13 difference is not a container effect and no arithmetic should be
done on it. What survives is the qualitative claim, which is the one that matters for the
substrate decision: **a RED suite reproduces off the container.**

## 3 · THE 13, CLASSIFIED

```
DOCUMENTED PRE-EXISTING REDs ON MAIN (known false positives, not this window's)
  test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
  test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
  test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings
      -- calendar-driven: spans cross the 30d accretion arm with no edit

COMMITTED-BASELINE vs LIVE-CORPUS (go RED whenever the corpus grows; this window added ~8
audit artifacts, so these are EXPECTED and self-inflicted-but-benign)
  test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it
  test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement
  test_gen_north_star.py::test_the_committed_view_is_current
  test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance
  test_reverse_dep_oracle.py::test_main_finding_json_exit_zero
  test_preflight_freeze_predicates.py::test_vi_batch1_reproduces_the_wrong_id_citation

PREDICTED BY TERRA, AND IT WAS RIGHT
  test_audit.py::test_check_fleet_parity_green_on_live_repo
      -- terra's lane-e finding (b): "ecosystem/parity-surfaces.yaml:197 keeps the root-path
         probe at VISION.md, so the hub emits a declared SHOULD-absent WARN until the
         sanctioned-divergence entry lands." The VISION relocation moved the file; the parity
         root-sweep still probes the root. This is the recorded tension MATERIALISING, not a
         surprise -- and it is one more reason [#621] is correctly OPEN.

SUBSTRATE / PROVISIONING
  test_cloud_provisioning.py::test_provision_sh_runs_the_history_repair_before_arming_hooks
  test_cloud_provisioning.py::test_the_gate_never_syncs_the_environment_it_is_asserting
  test_desired_state_report.py::test_live_report_renders_the_real_fleet
```

## 4 · HONEST LIMITS

- **No before/after was run.** Establishing which of the 13 this window CAUSED would need the
  suite at `0424741f` (the window's start) — another ~19 minutes. The classification above is
  by known-behaviour and by terra's own prediction, **not** by a controlled bisect. Where a row
  says "expected", that is an inference, and it is labelled as one.
- **`[#528]` is satisfied in letter** — the full suite ran once, at integration — **and its own
  thesis is confirmed:** 18:57 of wall-clock for one run is exactly the per-batch cost that row
  exists to measure.
- **This does not make L5 GREEN.** It removes one objection to the lane's attribution. The
  substrate verdict remains the operator's, and the packet's "substrate stays NON-DEFAULT" line
  stands until they rule otherwise.
