# Codex Review — foundation-6-ci-speed

**Date:** 2026-10-03
**Branch:** `worktree-foundation-6-ci-speed`
**HEAD at review time:** `3c2c8b6e`
**Diff range:** `origin/main...3c2c8b6e` (`ce6ecb08` base)
**Codex version:** see "Review 2" below
**Mode:** diff-review, isolated read-only session (the diff, the changed files, the measurements and the contract only — not the lane)
**Tally:** see "Reviews" below
**Consumer:** `LANE-FOUNDATION-foundation-6-ci-speed.md` (Done-contract item 5, "the review record citing this contract inside it");
`docs/decisions/ADR-127-ci-os-verification.md` (ADR-127 D1 — CI on Windows and Linux is the verification verdict, so its wall time is the merge's critical path)

**Review profile:** code

---

## What shipped, in one line

One flag: the `pytest` job's test step runs `-n 4 --dist loadgroup` (was `-n 4`). A RED-first pin in
`tests/test_conductor.py` asserts it; `ecosystem/doc-counts.md` is regenerated (+1 test). Nothing else in the job moved
(job id, matrix, step names, artifact, `--workers 4` are byte-identical). **The lane is PARTIAL against its Value line:**
Linux gains about 45 s (7%), Windows gains nothing measurable, and the leg's floor is a test-body defect that this lane
may not edit (finding 1 below).

## Step 0 — measured before any change

Runners: public repo, standard 4-vCPU hosted runners. `vcpu=4` printed by a probe on both legs
(`Linux-6.17.0-1022-azure`, AMD EPYC 7763; `Windows-2025Server-10.0.26100`, AMD EPYC 9V74 on the run that probed it).
Images `ubuntu-24.04` 20260927.320.1 and `windows-2025-vs2026` 20260925.250.1. **N1 confirmed:** the legs were never
single-process — `uv run --locked pytest -q --tb=short -n 4`, xdist 3.8.0, default `--dist load` as run (`addopts = "-n auto"`
is overridden by the explicit `-n 4`; `conductor.yml:142-148` at `ce6ecb08`). The xdist branch of the amendment does not apply.

The last three push runs of `main`, per leg (job total; test step; pytest's own wall; failures):

| run (sha) | Windows job / step / pytest | Linux job / step / pytest |
|---|---|---|
| [37137696130](https://github.com/rdwornik/dev-knowledge/actions/runs/37137696130) (`ce6ecb08`) | 1148 s / 1120 s / 1117.43 s, 67 failed | 642 s / 625 s / 624.03 s, 73 failed |
| [37133589959](https://github.com/rdwornik/dev-knowledge/actions/runs/37133589959) (`13fc203a`) | 1196 s / 1165 s / 1162.38 s, 70 failed | 564 s / 548 s / 547.78 s, 74 failed |
| [37031390518](https://github.com/rdwornik/dev-knowledge/actions/runs/37031390518) (`2e7fa5f2`) | 1101 s / 1074 s / 1071.69 s, 71 failed | 651 s / 631 s / 630.49 s, 77 failed |

**Where a leg's time goes (the same on all three):** set-up job 1-2 s, checkout 6-16 s, setup-uv 1-4 s, toolchain assert 0 s,
`uv sync --locked --group analytics` 2-3 s (nothing to cache), then the test step. Collection: 8737 tests, 13.4 s serial (`-n 0`)
and 2.9 s at `-n 4` on Linux; 10.9 s and 2.3 s on Windows (run [37139734271](https://github.com/rdwornik/dev-knowledge/actions/runs/37139734271),
the unchanged job plus a probe and `--durations=30`). Set-up + install + collection is under 30 s of a 560-1170 s job: **the
test step is 95-97% of every leg**, so it is the only place a lever can land.

**The 30 slowest tests** are in that run's logs; the head of the list, Linux then Windows (identical in shape on every run):

```
Linux                                                       Windows
301.86s call  test_connection_loop::test_no_handback_line…  308.68s call  test_connection_loop::test_no_handback_line…
265.20s setup test_connection_loop::test_one_toy_task…      320.75s setup test_connection_loop::test_one_toy_task…
104.50s call  test_hub_identity::…stored_path_is_stale       71.99s call  test_hub_identity::…stored_path_is_stale
 74.61s call  test_doc_code_edge::…registered_and_resolves   59.62s call  test_writer_integrity::…inert_check_left
 66.03s call  test_writer_integrity::…inert_check_left       46.90s call  test_doc_code_edge::…registered_and_resolves
```

A full-profile run (`--durations=0 --durations-min=1.0`, Linux) shows 143 entries over 1 s summing to 1672 worker-seconds, of which
`tests/test_connection_loop.py` is 573 s (four entries). Everything else is under ~140 s per module.

## The finding that matters: the leg's floor is a 300 s idle poll held inside a lock

`tests/test_connection_loop.py` serializes its heavy operations behind a machine-wide lock file (`_exclusive`, `:693`), across
workers. `test_no_handback_line_means_lane_end_does_not_run` (`:1003`) holds that lock through `stop_hook`'s
`deadline = time.monotonic() + 300` receipt poll (`:458`). It is a negative test — the receipt must never appear — so it always
runs the full deadline. Its call time is **301.86, 301.93, 301.95, 302.05 s in four separate runs**: a wait, not work. The walk fixture
(`:742`, 212-276 s on Linux, 307-489 s on Windows) needs the same lock. So the lock chain is walk + a 300 s idle + ~30 s, which is
**540-610 s on Linux regardless of how the other workers are scheduled**, and it is the leg's critical path.

Measured on a throwaway branch (not shippable by this lane, deleted): cutting that one deadline from 300 s to 20 s in the test
body took the Linux test step from 544-650 s to **397 s** (run [37143522865](https://github.com/rdwornik/dev-knowledge/actions/runs/37143522865)),
the failing set unchanged. On Windows the same edit gave 1058 s: a slow-mode Windows leg is throughput-bound, not chain-bound.

## Levers tried — each on a throwaway branch off `ce6ecb08`, deleted after (5 + 6 + 2 scratch branches, all removed)

| id | run | change | Win step | Linux step | judgement |
|---|---|---|---|---|---|
| M | [37139734271](https://github.com/rdwornik/dev-knowledge/actions/runs/37139734271) | probe step + `--durations=30` only (no lever) | 751 s | 604 s | W +graph_spine expired-lock (flake), +worktree_seed (branch-only) |
| L1 | [37140784100](https://github.com/rdwornik/dev-knowledge/actions/runs/37140784100) | `--dist loadgroup` | 1104 s | 544 s | W +3 errors in test_test_pairing (once; never again) |
| A | [37142453956](https://github.com/rdwornik/dev-knowledge/actions/runs/37142453956) | loadgroup + Windows Defender real-time off | 1099 s | 583 s | W +graph_spine overrun-builder (flake) |
| B | [37142568044](https://github.com/rdwornik/dev-knowledge/actions/runs/37142568044) | loadgroup + `TEMP`→`D:\tmp`, `TMPDIR`→`/dev/shm` | 733 s | 591 s | **REJECTED:** W +scope_guard 8dot3 short-form (path shape), L +preflight_freeze off-repo path |
| C | [37143522865](https://github.com/rdwornik/dev-knowledge/actions/runs/37143522865) | loadgroup + the 300 s poll cut to 20 s **in the test body** (scratch) | 1058 s | **397 s** | L set unchanged |
| D | [37143975968](https://github.com/rdwornik/dev-knowledge/actions/runs/37143975968) | loadgroup + `--durations=0` | 1084 s | 579 s | L set unchanged |
| E | [37144240354](https://github.com/rdwornik/dev-knowledge/actions/runs/37144240354) | loadgroup + conftest ordering that leads the group with the idle test | 854 s | 585 s | none |

Windows is bimodal on one configuration: 733-855 s (B, E, M) against 1048-1165 s (everything else, including every unchanged
`main` run). The CPU model of the slow run D is AMD EPYC 9V74, 4 logical processors; the fast runs were not probed. No lever of
this lane separates from that.

**The paired round (concurrent, so contemporaneous runners; controls = the net-zero branch and three copies of it):**

| run | change | Win job / step | Linux job / step |
|---|---|---|---|
| R1 [37145582724](https://github.com/rdwornik/dev-knowledge/actions/runs/37145582724) | control (revert, workflow byte-identical to `origin/main`) | 828 / 802 s | 648 / 630 s |
| K1 [37146150044](https://github.com/rdwornik/dev-knowledge/actions/runs/37146150044) | control | 1107 / 1079 s | 624 / 605 s |
| K2 [37146164805](https://github.com/rdwornik/dev-knowledge/actions/runs/37146164805) | control | 1087 / 1048 s | 671 / 650 s |
| K3 [37146182112](https://github.com/rdwornik/dev-knowledge/actions/runs/37146182112) | control | 1172 / 1142 s | 665 / 645 s |
| E1 [37146142722](https://github.com/rdwornik/dev-knowledge/actions/runs/37146142722) | loadgroup + lead ordering | 1039 / 1016 s | 566 / 549 s |
| E2 [37146157181](https://github.com/rdwornik/dev-knowledge/actions/runs/37146157181) | loadgroup + lead ordering | 1163 / 1134 s | 635 / 612 s |
| E3 [37146173003](https://github.com/rdwornik/dev-knowledge/actions/runs/37146173003) | loadgroup + lead ordering | 901 / 877 s | 615 / 598 s |

Control means: Windows 1018 s, Linux 633 s. Loadgroup-arm means: Windows 1009 s (−9 s, noise: the arm spans 877-1134 s), Linux 586 s
(−46 s, the arms barely overlap: 549-612 against 605-650). Across every loadgroup run of the lane (L1, A, B, D, E, E1-E3: 544, 583, 591,
579, 585, 549, 612, 598) the Linux mean is 580 s against 619 s for the seven unchanged runs (the three `main` runs and R1, K1-K3): **−39 s, 6%**.
The lead-ordering adds nothing over plain loadgroup (585 / 549 / 612 / 598 vs the loadgroup-only 544 / 583 / 579), so it is not shipped.

## Same judgement — the failing sets, by node id from the full job logs

**Linux: identical in all seven paired runs** (R1, K1-K3, E1-E3: 74 failed each, set difference 0 between every pair) and equal to the
base push run `ce6ecb08` plus exactly one member, `tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH`,
which reads "this lane's base equals main's HEAD" and is red on every branch run by construction, including the unchanged control.
**Windows: the flaking members are the same in the control and loadgroup arms** — `test_graph_spine::test_an_expired_lock_is_broken…`,
`test_graph_spine::test_an_overrun_builder_does_not_release_its_SUCCESSORS_lock`, `test_transport::test_concurrent_appends_…serialize…`,
and once `test_test_pairing::test_record_base_writes_the_red_set…` (+3 errors) in L1 — and they appear in the controls (K1-K3) as well,
so they are the runner's flake set, not the lever's. The base itself is not stable across its own three runs.

## Dispositions

- **DECIDED-BY-LANE:** ship `--dist loadgroup` alone → it makes the module's own `xdist_group` real (the module's comment at `:79-90` says
  it "becomes real the day some invocation adds `--dist=loadgroup`"), the Linux set is unchanged in 7/7 paired runs, and it saves ~40 s there.
  Not shipped: Defender off (no effect), temp-dir moves (changes judgement), lead ordering (no effect beyond loadgroup).
- **DECIDED-BY-LANE:** the worker count stays `-n 4` / `--workers 4` (N2); no QUESTION about it — nothing measured here argues for a change.
- **ROWS-OWED:** `tests/test_connection_loop.py` holds the module lock through a fixed 300 s receipt-absence poll —
  `provenance: logs of runs 37139734271, 37140784100, 37142453956, 37142568044 (301.86-302.05 s on every one), test_connection_loop.py:458,693,1003` —
  `check: gh run view <run> --log | grep "call .*test_no_handback_line"`. Fix is in the test body (narrow the lock, or bound the poll with a terminal
  signal): measured −150 to −230 s on Linux (397 s step, same set). Out of this lane's files.
- **ROWS-OWED:** the comment at `tests/test_connection_loop.py:79-90` ("the marker is a no-op under `--dist load`") becomes stale once
  loadgroup ships — `check: grep -n "inert" tests/test_connection_loop.py`.
- **QUESTION:** is a paid runner class worth its measured gain? Not measured here (N5: an `OPERATOR-ACTION`, not a change). The Windows slow
  mode (1048-1165 s) is throughput-bound on a 4-vCPU box, so a larger runner is the only lever aimed at it.
- **DECIDED-BY-LANE:** the throwaway experiment C edited a test body on a scratch branch purely to measure the finding above; it was never
  merged and the branch is deleted (the contract's "Do not edit a test module's body" governs what ships).

## Reviews

(filled below)
