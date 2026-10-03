# Codex Review — foundation-6-ci-speed

**Date:** 2026-10-03
**Branch:** `worktree-foundation-6-ci-speed`
**HEAD at review time:** `3c2c8b6e` (review 2 — the shipped diff); the candidate patch `origin/main..a958e2d4` (review 1)
**Diff range:** `origin/main...3c2c8b6e` (`ce6ecb08` base); the merged tip is `origin/main` `9683a655` plus this lane's commits
**Codex version:** OpenAI Codex v0.155.0 (review 2); review 1 ran on Grok before 21:07 (see "Reviews")
**Mode:** diff-review, isolated read-only session (the diff, the changed files, the measurements and the contract only — not the lane)
**Tally:** review 1 (grok-4.7) P1=3 P2=5 P3=3; review 2 (gpt-5.6-terra) P1=2 P2=2 P3=0 — every P1 fixed or answered below
**Consumer:** `LANE-FOUNDATION-foundation-6-ci-speed.md` (Done-contract item 5, "the review record citing this contract inside it");
`docs/decisions/ADR-127-ci-os-verification.md` (ADR-127 D1 — CI on Windows and Linux is the verification verdict, so its wall time is the merge's critical path)

**Model used:** `gpt-5.6-terra` (review 2, served — read from the run's own header, `model: gpt-5.6-terra`, `provider: openai`); `grok-4.7` (review 1, served — `usage.json` `primaryModelId`)
**Review profile:** code

---

## What shipped, in one line

One flag: the `pytest` job's test step runs `-n 4 --dist loadgroup` (was `-n 4`). A RED-first pin in
`tests/test_conductor.py` asserts it; `ecosystem/doc-counts.md` is regenerated (+1 test). Nothing else in the job moved
(job id, matrix, step names, artifact, `--workers 4` are byte-identical). **The lane is PARTIAL against its Value line:**
Linux gains about 40 s (6%, pooled over 13 loadgroup runs against 11 controls; noisy — a Linux leg on identical code ran 473 s and
605 s), Windows gains nothing measurable, and the leg's floor is a test-body defect that this lane may not edit (the finding below).

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

The chain, run by run (every run with `--durations`; `walk` = the module-scoped fixture's setup, `poll` = the no-handback test's call,
`pytest` = pytest's own wall; `chain` = walk + poll):

| run | Linux walk / poll / chain / pytest | Windows walk / poll / chain / pytest |
|---|---|---|
| M 37139734271 | 265 / 302 / 567 / 603 s | 321 / 309 / 629 / 751 s |
| L1 37140784100 | 231 / 302 / 533 / 544 s | 489 / 320 / 809 / 1104 s |
| A 37142453956 | 268 / 302 / 570 / 583 s | 368 / 321 / 689 / 1099 s |
| B 37142568044 | 276 / 302 / 578 / 591 s | 307 / 304 / 611 / 733 s |
| D 37143975968 | 264 / 302 / 566 / 579 s | 476 / 310 / 786 / 1084 s |
| E 37144240354 | 270 / 302 / 572 / 585 s | 365 / 314 / 679 / 854 s |
| C 37143522865 (poll cut to 20 s) | 212 / 22 / 234 / 397 s | 452 / 30 / 482 / 1058 s |

On Linux the chain is 94-98% of the pytest wall on all six unchanged-poll runs, and cutting the poll moves the wall by the poll's length
less what the other workers' own work then binds (397 s). On Windows the chain is 80-84% of the wall on the three fast runs (M, B, E) and 63-73% on the slow ones
(L1, A, D; 46% with the poll cut, C): a fast Windows runner is mostly chain-bound, a slow one is throughput-bound beyond it. "Scheduler-independent" follows from the lock being machine-wide
(`_exclusive` is a lock file in the run's shared folder, so two workers cannot overlap on it) — it is a property of the test, not of `-n`.

Measured on a throwaway branch (not shippable by this lane, deleted): cutting that one deadline from 300 s to 20 s in the test
body took the Linux test step from 544-650 s to **397 s** (run [37143522865](https://github.com/rdwornik/dev-knowledge/actions/runs/37143522865)),
the failing set unchanged. On Windows the same edit gave 1058 s: a slow-mode Windows leg is throughput-bound, not chain-bound.

## Levers tried — each on a throwaway branch off `ce6ecb08`, deleted after (19 scratch branches in four batches — 5, 6, 2+3 and 3 — all removed)

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

## The second paired round — on the merged main state (`9683a655`), code only, no record

`origin/main` moved to `9683a655` (the foundation-3 merge) while this lane ran. The base for any comparison is the main push run on that tip,
[37148025981](https://github.com/rdwornik/dev-knowledge/actions/runs/37148025981) (Windows 887 s job / 863 s step, Linux 493 s / 479 s — a fast runner on both),
and contemporaneous controls: three copies of `9683a655` pushed at the same moment as three code-only copies of this lane's change (`3eb74552` =
`9683a655` + the workflow flag, the pin and the regenerated count; no record in it).

| run | change | Win job / step | Linux job / step |
|---|---|---|---|
| C1 [37149765921](https://github.com/rdwornik/dev-knowledge/actions/runs/37149765921) | control (`9683a655`) | 1155 / 1117 s | 648 / 628 s |
| C2 [37149773942](https://github.com/rdwornik/dev-knowledge/actions/runs/37149773942) | control | 1142 / 1113 s | 629 / 608 s |
| C3 [37149781557](https://github.com/rdwornik/dev-knowledge/actions/runs/37149781557) | control | 1142 / 1114 s | 646 / 625 s |
| S1 [37149674248](https://github.com/rdwornik/dev-knowledge/actions/runs/37149674248) | `--dist loadgroup` | 1249 / 1219 s | 614 / 598 s |
| S2 [37149682387](https://github.com/rdwornik/dev-knowledge/actions/runs/37149682387) | `--dist loadgroup` | 826 / 805 s | 488 / 473 s |
| S3 [37149789168](https://github.com/rdwornik/dev-knowledge/actions/runs/37149789168) | `--dist loadgroup` | 1203 / 1170 s | 627 / 610 s |

Linux: control mean 620 s (tight, 608-628), loadgroup mean 560 s (473-610); median −27 s, mean −60 s, the mean pulled by one fast-runner run (S2). Windows:
control mean 1115 s (1113-1117), loadgroup mean 1065 s (805-1219); median **+56 s** (two of three loadgroup runs are slower than every control, one is a
fast-runner run). Neither leg's result is outside this lane's own noise on its own. **Pooled over every run of the lane:** Linux loadgroup 569 s (13 runs)
against 607 s (11 controls), −38 s, 6%; Windows slow-mode loadgroup 1118 s against 1108 s controls, +10 s, 1%. **The honest reading: a small Linux gain
of about 40 s that is real in direction in every comparison (−39, −46, −60 s) and weak in size; nothing on Windows.** The decision rule written
before these runs came back (ship iff the Linux mean gain is at least 30 s with identical failing sets and no Windows regression) is met on the mean, not
on the median; it is recorded as such rather than rounded up.

## Same judgement — the failing sets, by node id from the full job logs

**Linux — identical.** Within each round every run has the same 74 failing node ids (first round: R1, K1-K3, E1-E3, set difference 0 pairwise; second round: C1-C3 equal
to the main push run on their own tip 9683a655, S1-S3 equal to them). The one standing difference is
`tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH`, which asserts "this lane's base equals main's HEAD": it is red on every run whose tip is not
main's HEAD (round-one R1/K/E against ce6ecb08, round-two S1-S3 against 9683a655) and absent where the tip IS main's HEAD (C1-C3, the main push
runs) — a property of the branch, identical in the control and loadgroup arms of round one. 7 of 7 first-round and 3 of 3 second-round Linux runs agree.

**Windows — equal up to a flake set that also flaps in the unchanged controls.** Against the base push run `ce6ecb08` (67 failed), by node id:

| run | arm | difference from the base set |
|---|---|---|
| M | probe only | +graph_spine expired-lock, +worktree_seed |
| R1 | control | +graph_spine expired-lock, +transport concurrent-appends, +worktree_seed |
| K1, K2 | control | +worktree_seed |
| K3 | control | +graph_spine overrun-builder, +worktree_seed |
| E1, E2, E3 | loadgroup + ordering | {+expired-lock, +overrun-builder, +worktree_seed}, {+overrun-builder, +worktree_seed}, {+expired-lock, +worktree_seed} |
| L1 | loadgroup | +expired-lock, +test_test_pairing record-base (+3 errors), +worktree_seed — the only time that member appeared in 12 loadgroup runs |
| C1, C2, C3 | control (second round, vs main `9683a655`) | {+expired-lock}, {none}, {none} |
| S1, S2, S3 | loadgroup | {+worktree_seed}, {+expired-lock, +worktree_seed}, {+worktree_seed} |

The three flapping members — `test_graph_spine` expired-lock and overrun-builder, `test_transport` concurrent-appends — appear in the controls as often as in
the loadgroup arms (controls: 4 of 8 runs carry at least one; loadgroup: 8 of 12). The base is not stable across its own three runs (67, 70 and 71 failed).
**The contract's "no flake" cannot be demonstrated for Windows by any lever of this lane; what can be shown is that the flake set is the runner's and the
change adds no member to it.** `DONE-ITEM 3` is therefore reported Linux-MET and Windows-PARTIAL.

**What the record itself costs on CI (not the lever).** The lane branch's own runs after the record landed ([37149847091](https://github.com/rdwornik/dev-knowledge/actions/runs/37149847091),
Linux 81 failed + 11 errors) add six members that the code-only copies do not have: `test_gen_audit_index` `live_index_is_fresh` and
`live_index_excludes_nothing…` (the index says 1201 documents and the tree has 1202 — BATCH-COMMON §0 lesson (d): a lane writing `docs/audits/` leaves
`docs/audits/README.md` stale and the integrator regenerates it on the merged tree, `[#590]`), and the four `test_handoff_cut_acceptance` tests plus 11
errors in `test_seat_release_moment`, whose cause is a `journal_spine_anchor` hard-fail naming `9683a655` unanchored (`origin/main`'s own tip, not yet anchored in
`JOURNAL.md`). Both clear when the integrator regenerates the index and anchors the merge; neither is touched by this lane (`docs/audits/README.md` and
`JOURNAL.md` are not Files-you-own).

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
- **EXPECTED-RED (the integrator's, rule (d)):** this record makes docs/audits/README.md stale (1201 vs 1202 documents) — gen_audit_index.py --write on the merged tree clears 	est_gen_audit_index x2; the journal_spine_anchor hard-fail on 9683a655 (main's tip, unanchored) is main's state and clears when the integrator anchors it; and 	est_consumer_at_landing::test_the_live_corpus_measures_and_the_baseline_matches_it lists this record as unconsumed (the as-consumption leg: no governance surface cites its identifier yet — the leg-1 declaration above passes) until the integrator's merge receipt names the slug (the [#1329] receipt route), as it does for every lane record.
- **QUESTION:** is a paid runner class worth its measured gain? Not measured here (N5: an `OPERATOR-ACTION`, not a change). The Windows slow
  mode (1048-1165 s) is throughput-bound on a 4-vCPU box, so a larger runner is the only lever aimed at it.
- **DECIDED-BY-LANE:** the throwaway experiment C edited a test body on a scratch branch purely to measure the finding above; it was never
  merged and the branch is deleted (the contract's "Do not edit a test module's body" governs what ships).

## Reviews

### Substitution note

`SUBSTITUTION: codex terra -> grok-4.7 (Codex usage limit until 2026-10-03 21:07; review 1 ran 20:50-20:56 local time)` — the batch order's own route
(BATCH-COMMON §0 ruling (e)), not a silent one; Grok is not the producer's vendor and not the implementing session. **Review 2 ran after 21:07, so it ran on the
registry's first route, Codex terra, with no substitution.**

### Review 1 — `grok-4.7`, of the candidate patch and the lane's disposition "no lever is justified"

**Command:** from an isolated folder holding only `contract.md`, `measurements.md`, `candidate-levers.patch`, `conductor.yml` and `test_connection_loop.py` —
`grok -m grok-4.7 --tools read_file,list_dir,grep -p "<prompt: attack the disposition>"`; exit 0. **Served model:** `grok-4.7`, `usage.json`
`primaryModelId`, 7 model calls. **Output contract (R59 item 1):** the answer had to open with the nonce `STONE-4417` and a word count; it did (`STONE-4417`, 704).
**Tally:** P1=3 P2=5 P3=3. What I did with it — the reviewer was asked to attack the disposition, and parts of it were right:

| finding | disposition |
|---|---|
| P1 — "−150 to −200 s" for cutting the poll is not control-matched (C 397 s vs the loadgroup control L1 544 s is −147 s) and C's Windows set differs | **Accepted.** The record states −147 s against its loadgroup control and about −200 s against the unchanged runs; the Windows set difference is the `graph_spine` flake, now shown per run |
| P1 — "no owned lever moves wall time" is overclaimed: E (conftest ordering) fell 1104→854 s on Windows, never repeated | **Accepted in part.** E was repeated (3 × E against 3 × concurrent controls) and shows nothing beyond loadgroup on either leg; the Windows spread (733-1165 s on unchanged code) is larger than any single-run effect. M is a probe plus `--durations`, cannot cause a 400 s drop, and is the evidence for the runner lottery, not a lever |
| P1 — the patch under review installs the very change the disposition says to revert | **Rejected as a misreading.** The folder held the *candidate* patch on purpose; the shipped state is what review 2 read. The disposition has since changed (loadgroup ships), for the reason in the second paired round |
| P2 — "95%+" is not tabled; 1672 s is worker-time not wall; the chain sum needs both on one worker; "~30 s" has no row; the fourth Linux "base" was M | **Accepted.** Job totals are now in every table; the chain table is added with its arithmetic; the lock is machine-wide so the sum does not need one worker (stated); M is labelled, and the control set is now the unchanged runs only |
| P2 — CPU probed on one slow run only | **Accepted.** Probed on D (slow, EPYC 9V74); the fast runs were not probed — stated, not inferred |
| P3 — Windows ranges untied to run ids; B/E/M are not "the same config"; the contract forbids this lane's fix but not a later owner's | **Accepted.** Tied to runs in the chain table; the ROWS-OWED names the test module's owner as the fixer |

### Review 2 — `gpt-5.6-terra`, of the shipped diff (`origin/main...3c2c8b6e`)

**Command:** from an isolated folder holding `diff.patch`, `contract.md`, `conductor.yml`, `test_conductor.py`, `test_connection_loop.py` and this record without its
reviews — `codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check --output-last-message codex-out.txt -` with the prompt on stdin; exit 0.
**Served model:** `gpt-5.6-terra` (the run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`). **Output contract (R59 item 1):**
the answer had to open by quoting the first line of `diff.patch`; it did (`diff --git a/.github/workflows/conductor.yml b/.github/workflows/conductor.yml`).
**Tally:** P1=2 P2=2 P3=0. It also reports no scope violation: the patch touches only owned files plus the regenerated count; the job id, matrix, step names,
artifact, `-n 4` and `--workers 4` are unchanged.

| finding | disposition |
|---|---|
| **P1** `tests/test_conductor.py:483` — the pin also matches the explanatory comment, so removing the flag from the command leaves it green | **Fixed** in `e342a73c`, RED-first: with the flag removed from the command and the comment kept, the old whole-text pin passes and the new executable-lines pin fails (`mutant (flag removed from the command, comment kept): old whole-text pin passes=True, new executable-lines pin passes=False`); `test_the_group_pin_reads_the_command_and_not_the_comment_that_names_the_flag` pins the helper; 64 tests in the file pass |
| **P1** record — per-run Windows node-id sets are not shown; the contract's "equal to the base, no flake" is not established | **Answered, not fixed away:** the per-run Windows sets are now tabulated above; equality is NOT established for Windows, because the base's own three runs differ (67/70/71 failed) and the unchanged controls flap the same members. Stated as `DONE-ITEM 3 Linux-MET, Windows-PARTIAL`, not claimed |
| P2 — the "540-610 s floor" has no table | **Fixed:** the chain table (walk / poll / chain / pytest, both legs, seven runs) |
| P2 — "~45 s" holds only for the paired arm (46 s), the all-runs estimate is 39 s | **Fixed:** the workflow comment says "(paired round)"; the record gives the three estimates (−39, −46, −60 s) and the pooled −38 s |

### Consumer

This record is the review record that `LANE-FOUNDATION-foundation-6-ci-speed.md` Done-contract item 5 requires ("the review record citing this contract inside it"),
and it is cited by the comment above the pytest step of `.github/workflows/conductor.yml`.
