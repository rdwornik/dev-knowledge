# STATE OF THE HARNESS — 2026-09-23

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/STATE-OF-THE-HARNESS-2026-09-23.md`. Full was/is companion to
> `2026-09-23-technical-handoff-readiness.md`; supersedes-as-baseline
> `STATE-OF-THE-HARNESS-2026-09-20.md` (not committed here — cite by that same transport name if
> it is ever landed).
> Carrier rows: D1-D29 (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`) and D30-D34
> (`to-cc/AMEND-WINDOW-DEFECTS-2026-09-23.md`), filed by `lane-landing-window`; §6 Track C item 3
> (validate_backlog's 10 hard-fails) is the same P9 finding this lane fixed directly.

carried-by: OPEN
lands-via: read by the architect with DIGEST-HANDOFF-READINESS-2026-09-23; no repo change
date: 2026-09-23
from: postwave-state (POSTWAVE CHAIN S3, job 60a4eb17, Opus 5.5), read-only on main @ 4667f731 (== origin/main, tree clean before and after)
supersedes-as-baseline: STATE-OF-THE-HARNESS-2026-09-20.md (same sections; every number carries "was / is")

The system tested itself on `main` with its own tools, one after another, on a loaded box: `audit.py health`,
`audit.py ship-gate`, `gates.py run` (the JSON verdict), `organ_usage_metric.py census`, `graph_queries.py
moments / orphan-census / process-list`, `no_leftovers.py verify` (slug-less), the connection walk
(`tests/test_connection_loop.py`, `-n 2`), and the active handoff bundle's probe set in report-only mode.
Raw outputs are in the S3 job's tmp directory. Nothing was repaired.

Tags: **MEASURED** means run in this session. **INHERITED** means taken from a named receipt without
re-running it. **WAS** is the value in `STATE-OF-THE-HARNESS-2026-09-20.md` unless stated otherwise.

**Run note (MEASURED):**
- The self-test battery ran its steps one after another.
- The harness reaped its shell for low memory at the connection-walk step, 22:29.
- The walk's orphaned `pytest`/`gates` children kept running. S3 stopped them (11 processes, its own), and free memory rose from 1.31 GB to 2.79 GB.
- Per the harness notice, the walk was not restarted.
- The repo tree was clean before and after. No worktree or branch was created.
- The walk figures above are WAVE4B's measurement of the same SHA.

---

## 1. Where the loop stops, why, and what each remaining stage needs

The spine is no longer "12 stages that halt at 7". ADR-120 (Accepted 2026-09-22) makes it the whole loop: 12
spine stages plus 6 moments (pre-launch, lane-start, merge, teardown, lane-end, batch-close) in
`ecosystem/harness.yaml`. The connection walk drives one toy task through all of them in a toy copy of the repo,
using the real organs.

```
metric                                   | was (09-20)                          | is (09-23)                                   | tag
spine stage 7 (substrate)                | BROKEN, exit 2, no `paths` argv      | argv now `{contract}`; the walk passes spine  | MEASURED harness.yaml:19; walk INHERITED
spine stage 11 (token-cap)               | command: null, halts every run       | wired: `dispatch.py plan ... --token-cap`     | MEASURED (harness.yaml:23)
spine stage 12 (contract)                | never reached                         | reached in the walk (spine moment fires)      | INHERITED (walk) + test asserts read
where a real run stops                   | stage 7                               | moment merge / organ gates                   | EXPECTED_STOPS, tests/test_connection_loop.py:95
second stop                              | n/a                                   | batch-close / digest-names-the-task          | same
moments before the first stop, all fire  | n/a                                   | spine, pre-launch, lane-start, lane-end      | test asserts (:763)
merge organs that fire before `gates`    | n/a                                   | merge_receipt.open, .models, go_reader, review_packet | test asserts (:768)
whole-loop test                          | n/a                                   | strict xfail (still)                          | MEASURED (:745)
connection module at -n 2                | n/a (W3-F built 09-21)                | 21 passed, 1 xfailed (strict), 0 failed, 18 min 59 s | INHERITED (DIGEST-WAVE4B B5, same SHA 4667f731; this session's run was reaped, see note)
[#922] (stage-7 row)                     | OPEN                                  | still OPEN, although the argv is fixed        | MEASURED (tasks/922 status: open)
```

**Why it stops at `merge/gates`:** `gates.py` runs `audit.py health`, `audit.py ship-gate`, `ruff` and the
impacted-test selector against the tree. `ship-gate` is RED by construction on this repo: it has 319
undispositioned WARNs today (§6 Track C). The walk records that as a stop, not a pass. WAVE4B also recorded that
`impacted-tests` runs with `-x` and stops at two registry reds on every merge
(`test_boot_retrieval::test_repo_tracked_boot_base_is_under_its_ceiling` at 40,669 B against 40,000 B, and
`test_audit::test_check_fleet_parity_green_on_live_repo`). **So every gates run is RED before a lane changes
anything** (INHERITED from DIGEST-WAVE4B F7; this session's `gates.py run` on main, JSON verdict MEASURED: **RED, red = [ship-gate] only**. audit-health exit 0 (258 warn / 0 fail findings), ship-gate exit 1 (407 warn findings, 476 s), ruff ok, impacted-tests ok (base = HEAD, so nothing was selected). The per-organ `findings` lists are present in the JSON: W4B-3's FR4 works on main.).

**Why batch-close stops:** the digest names the batch, not the task. WAVE4B measured the production form of the
same defect: the batch-close digest showed merge sha 0/6 and verdict 0/6, because `merge_receipt` records no
merge sha and no timed step under the procedure the integrator actually runs (F4).

**Two merge paths still exist (RC1 of DECLARE-WAVE4B-DIRECTION).** The walk exercises `moment:merge`.
Production merges ran through an integration worktree by hand. The lane that was meant to unify them,
W4B-1 lane-merge-path, was DEFERRED at 13:16Z and never launched. B1 "one path" was scored MET on a ledger count
(6 rows for 6 merges), but every row is incomplete by the ledger's own predicate.

**What each remaining stop needs:**
- `merge/gates`: a green ship-gate is unreachable while 319 WARNs sit undispositioned. Either the WARN tiers get a
  bulk disposition mechanism, or `gates` judges only what the merge *introduced*. The integrator already does the
  second by hand, as a base-vs-merge diff.
- `batch-close/digest`: `merge_receipt` must record the merge sha and the timed steps under the operated path.
  That is lane-merge-path's scope.

---

## 2. What is armed and what only looks armed

```
surface                                   | was (09-20)                     | is (09-23)                                    | tag
pre-commit hooks, default stage (fire)    | 12                              | 12 (with counter + expiry 2026-09-25)         | MEASURED (.pre-commit-config.yaml)
commit-msg hooks                          | 3                               | 3                                             | MEASURED
pre-push hooks                            | 2                               | 2                                             | MEASURED
pre-commit hooks `stages: [manual]`       | 19                              | 19                                            | MEASURED
block-commit-on-main                      | manual (inert)                  | manual (inert)                                | MEASURED
graph-* refusals ([#664])                 | manual                          | manual (5 ids); REPORT-ONLY in CI             | MEASURED
SessionStart hooks in repo settings       | 1 firing (arm_hooks)            | 8 (re-armed by W4B-0, 2026-09-22)             | MEASURED (.claude/settings.json)
Stop hooks in repo settings               | 1 (backpressure) + plugin       | 2 (backpressure, lane_end_guard) + plugin     | MEASURED
PreToolUse hooks (repo or L0)             | 0                               | 0                                             | MEASURED
block-onedrive.ps1 (P0 write/delete guard)| DISARMED since 09-17            | DISARMED; no expiry                           | MEASURED (~/.claude/settings.json: only Notification hooks, disableAllHooks true)
OneDrive Read-deny permission             | binds                           | binds (Read only)                             | MEASURED
organ-index hook arming                   | all 36 "ARMED" (wrong)          | 19 MANUAL correct; block-onedrive still "ARMED" (wrong) | MEASURED (ecosystem/organ-index.md:100)
methodology-roster "hard block" wording   | wrong                           | still wrong (roster line 33)                  | MEASURED
audit checks registered                   | 55                              | 56 (last: organ_truth)                        | MEASURED (audit.py checks)
required-checks ruleset                   | enforcement: disabled           | unchanged; last 3 conductor pushes: failure   | MEASURED (boot banner)
```

**What changed:** the eight emergency-disabled SessionStart hooks came back on isolated-run evidence (W4B-0).
Lane end is now an event: `lane_end_guard.py` on Stop claims, detaches, writes a receipt and reaps.

**What only looks armed** (S2, MEASURED from transcript `hookEvent` attachments, 72 h):
- `surface_triage.ps1` timed out on 23 of about 31 boots.
- `fleet_health.py` takes 15.6 s at p50 and 26.6 s at p90 in-session.
- `propose_closures` timed out on 33 of 208 runs, and nothing reads what it writes.

The boot banner still prints seven re-armed hooks as "DECLARED BROKEN", because `logs/HOOK-BYPASSES-BROKEN.json` was
never reconciled with the re-arm. The commit-hook counter that the 2026-09-25 "0 catches → REMOVE" verdict will
read is per-checkout, so every lane's rows die at teardown. Four armed hooks have zero runs in the primary store.
**On that data, the 09-25 verdict cannot tell "never ran" from "never caught".**

**The P0 exclusion zone is protected only against Read.** Write, Edit and Bash into it are guarded by nothing but
the model. That is unchanged since 09-17, and no dated expiry exists ([#863]/[#865]).

---

## 3. What we built, what calls it, and what a complete run still lacks

```
metric                                         | was (09-20)                     | is (09-23)                               | tag
scripts/**/*.py tracked                        | 156 (118 top-level)             | 169 (130 top-level; 25 audit_checks)     | MEASURED
graph processes (process-list)                 | n/a                             | 189; 141 triggered, 48 not               | MEASURED
census over 30 d (observable 175 of 189)       | n/a                             | CALLED 78 / REACHABLE-BUT-UNOBSERVED 80 / UNREACHABLE 17 | MEASURED
census: not observable (commands/skills)       | n/a                             | 14                                       | MEASURED
moments query: declared at a moment            | n/a                             | 23 of 189                                | MEASURED
moments query: declared nowhere                | n/a                             | 166 (130 wired by another surface, 36 by none) | MEASURED (REFUSED)
orphan-census undispositioned                  | 5                               | 14                                       | MEASURED (REFUSED)
```

**The graph still has no edge from a harness stage or moment to the script it runs.** The 09-20 Track B #1 gap
is unfiled and unclosed, and it is now worse. Nine of the 14 orphans are scripts that `harness.yaml` names at a
moment or stage:
- `gates.py`, `go_reader.py`, `no_leftovers.py`, `test_pairing.py`, `worktree_occupancy.py`, `lane_digest.py`;
- `dispatch.py`, `stage_prior_art.py`, `stage_library_first.py`.

`moments` lists `gates.py` as "declared-at-moment merge/gates", while `orphan-census` lists the same file as
"reached by no wiring surface". **Two queries over one store disagree about one file**, because only one of them
reads `harness.yaml`. The other five orphans:
- `handback.py` and `plan_lint.py`: new this wave, lane-called;
- `dodo.py`: the spine runner;
- `/spine` and `/why`.

**UNREACHABLE 17 (the ratchet's binding number, per the three-state ruling)** includes `handback.py`,
`go_reader.py`, `lane_digest.py`, `lane_boot.py`, `provider_router.py`, `cost_usage_telemetry.py`, `dodo.py`,
`propose_closures.py`, `offload_admission.py` and `provider_bench.py`. Several of these are run by the harness or
by a lane every batch. The census cannot see a `harness.yaml`- or command-driven call, so **UNREACHABLE
over-counts** until the stage/moment edge exists.

**What a complete run still lacks** (the 09-20 list of 4, re-checked):
1. The stage-7 argv: **CLOSED** (argv `{contract}`, the walk passes spine).
2. Stage 11 wired: **CLOSED** (`dispatch.py plan`).
3. A record of stages 1-10 completing together: **CLOSED in the toy** (the walk). Still NONE on a real row.
   O-2 condition 2 ("a real backlog task travels the whole loop") is unmet and has no row (§5).
4. A stage-to-script edge in FPG-1: **OPEN**. It is now the cause of 9 of 14 orphan findings, of the 166
   "declared nowhere" and of the UNREACHABLE over-count.

New lacks:
5. One merge path. W4B-1 was deferred, so the walk and production run different merge paths.
6. A merge receipt that records the sha and the steps (F4).
7. A gate that judges what a merge introduced, not the repo's WARN backlog (§1).

---

## 4. Graph coverage

```
metric                                   | was (09-20)   | is (09-23)   | drift  | tag
graph nodes / edges (stats)              | 3,010 / 22,232| 3,103 / 22,669 | +93 / +437 | MEASURED
tracked files (worktrees excluded)       | 3,671         | 3,777        | +106   | MEASURED
tracked files with a node                | 2,591         | 2,683        | +92    | MEASURED
unknown (no node)                        | 1,080         | 1,094        | +14    | MEASURED
  docs/handoffs/** (Cause A)             | 665           | 665          | 0      | MEASURED
  tests/** (Cause B)                     | 159           | 174          | +15    | MEASURED
  ecosystem/** (Cause C)                 | 81            | 81           | 0      | MEASURED
  docs/decisions + docs/intake (Cause D) | 64 (44+20)    | 63 (43+20)   | -1     | MEASURED
  docs/audits non-.md (Cause E)          | 11            | 11           | 0      | MEASURED
no-purpose (unknown + known-silent)      | 1,147         | 1,154 (1,094 + 60) | +7 | MEASURED
no-edges (unknown + known, edges=0)      | 1,816         | 1,830 (1,094 + 736) | +14 | MEASURED
purpose stated but zero edges            | 669           | 695          | +26    | MEASURED
coverage (with-node / tracked)           | 70.6 %        | 71.0 %       | +0.4 pt| MEASURED
```

**Nothing in the graph's coverage moved in four days except drift.** The two BUG causes, D (63 pathless ADR and
intake nodes; one loader) and E (11 non-.md audit files; one glob), are still open. Both were rated cheap on
09-20. Cause B grew by 15, which is the new test files of waves 3 to 4B. The unknown set still grows by commit
traffic, not by design.

---

## 5. Which rulings are in force, which are homeless, and whether the ADR mechanism is working

```
metric                                           | was (09-20)          | is (09-23)                    | tag
ADR files / highest number                       | 119 highest          | 93 files / ADR-120            | MEASURED
ADR-120 (spine is the whole loop)                | did not exist        | Accepted 2026-09-22           | MEASURED
STANDING_RULINGS.md lines                        | 4,373                | 4,602 (+ section AJ, 7 entries)| MEASURED
09-20's 4 flagged homeless rulings, now homed    | 0 of 4               | 0 of 4 (BUILD-LIST only, or nowhere) | MEASURED (grep SR / ADR)
09-20's 6 self-flagged rulings, now homed        | 0 of 6               | 0 of 6                        | MEASURED (grep protocols, LESSONS, ADRs, templates)
BUILD-MODE vs BUILD-LIST B2->B3 wording          | disagree             | still disagree (BUILD-MODE.md:69 vs BUILD-LIST.md:21) | MEASURED
09-19..23 DECLARE/AMEND/BATCH files (P11 set)   | n/a                  | 45 (44 carry a flush-left carried-by; BATCH-map-verification none) | MEASURED (P11)
... resolved to a repo path on main              | n/a                  | 7                             | MEASURED (P11)
... OPEN and named in the bundle's RESIDUAL      | n/a                  | 5 (all 09-19)                 | MEASURED (P11)
... OPEN and NOT named in the bundle's RESIDUAL  | n/a                  | 32 (P11 FAIL), plus 1 with no carried-by | MEASURED (P11)
09-23 DECLAREs with any repo citation            | n/a                  | 0 of 8                        | MEASURED (git grep -F, handoffs excluded)
standing operator requests (09-19..23)           | n/a                  | 17; 4 with an OPEN row; 10 with no home | MEASURED (S3 probe)
```

**The landing step works, and it runs one window behind.**
- LANE-W4-5 (2026-09-22) landed seven decision files of 09-20..22 into STANDING_RULINGS §AJ and ADR-87/ADR-120.
  That is the first real drain of the transport.
- Everything decided on 09-23 has no repo citation at all: MODEL-AGNOSTIC, NIGHT-AUTONOMY, OFFBOX-PORTABILITY,
  TRANSPORT-SCHEMA, WAVE5A-VERIFICATION, WINDOW-DEFECTS, COPILOT-TRIAL, STATE-STORE-LEARNING,
  RATIFICATION-copilot, AMEND-ADR-STATE-STORE.
- DECLARE-WAVE4B-DIRECTION is carried by rows (tasks 955, 957, 958, 961) but still says `carried-by: OPEN`.
- The 09-20 homeless-ruling set is unchanged: ARCHITECTURE.md KEPT, the repo-map deferral, the layer-invariant
  split, the three-state census, the six self-flagged doctrines, and the BUILD-MODE/BUILD-LIST disagreement.

**ADR verdict, updated:** the mechanism now produces again (ADR-120 was accepted inside the window). The routing
around it continues: this window's biggest decisions exist only as transport DECLAREs:
- model-agnostic routing;
- off-box portability;
- the transport schema;
- night autonomy;
- the state store, which the operator explicitly sent to an ADR.

---

## 6. The ordered work queue per track

### Track A — the loop completes a run

```
1. One merge path: land lane-merge-path (deferred W4B-1) so production merges run `moment:merge`. Closes RC1 and F4/F5.
2. merge_receipt records the merge sha and timed steps under that path; batch-close names the task (walk stop 2, WAVE4B B4).
3. gates judges what a merge INTRODUCED (base-vs-merge diff), not the repo's WARN stock (walk stop 1).
4. Remove the strict xfail when 1-3 hold. This is O-2 condition 1, and it has no row.
5. One real backlog row through the whole loop, operator touching only the task and GO. O-2 condition 2, no row.
6. Close [#922]; its argv defect is fixed and the row is stale.
```

### Track B — the repo answers questions about itself

```
1. Add the stage/moment -> script edge class to FPG-1 (harness.yaml argv). It explains 9 of 14 orphans, the 166
   "declared nowhere" and the UNREACHABLE over-count. Still UNFILED as a row (09-20 said the same).
2. Cause D loader (63 files) and Cause E glob (11 files). Cheap, unchanged since 09-20.
3. Make `orphan-census` and `moments` read one wiring truth, so two queries over one store cannot disagree about gates.py.
4. Policy calls on Cause A (665 handoffs) and Cause B (174 tests). Still unmade.
```

### Track C — blockers

```
1. Ship-gate RED: 407 WARN, 88 dispositioned, 319 undispositioned, 0 [stale].
   09-20 was 357 / 88 / 269 / 3 [stale]. Undispositioned grew by 50 in four days.
   Top checks (all WARNs, including dispositioned):
     consumer_at_landing 170 (09-20: 121)
     funnel_coverage     120 (09-20: 83)
     proof_layer          69 (09-20: 44)
     undeclared_edges     16
     doc_rot              10
     fleet_parity          5
   Hard-fails ([!!]): 0.
2. The two registry reds that make every gates run RED (F7).
3. validate_backlog: 10 hard-fails on a bare run. `implements:` tokens are outside the grammar ([#906], [#908]-[#914])
   and [#664] is struck through in place. Its pre-commit hook is manual, so nothing refuses them.
4. The connection module takes 17.5-19 min at -n 2 (B5 bar: 10 min).
```

### Track D — enforcement mechanism

```
1. P0 path protection without a process (S2 row 5): permissions.deny for Edit/Write/NotebookEdit on the zone.
   block-onedrive has been off since 09-17 with no expiry.
2. The commit-hook counter moves to the git common dir before the 2026-09-25 verdict (S2 row 4). Zero runs is UNMEASURED, not REMOVE.
3. SessionStart becomes one stdlib reader (S2 row 1). 23 of about 31 boots time out a hook.
4. The boot banner is reconciled with the re-arm: 7 hooks are falsely printed "DECLARED BROKEN" (S2 row 6).
5. Correct organ-index (block-onedrive ARMED) and the roster's "hard block" wording.
6. Home the 09-23 decisions: every ruled DECLARE and both RATIFICATIONs cited by a row or STANDING_RULINGS.
   This is O-4's "every operator request becomes a row the same day".
```

---

## 7. The three open questions of 09-20, and where they stand

- **Q1: does a user-level-only PreToolUse hook fire here?** Still UNTESTED. User settings carry `disableAllHooks:
  true` with only a Notification hook. The repo carries `disableAllHooks: false`. S2 proposes making the
  question moot with deny rules, which need no process.
- **Q2: the fair `why` test (unnamed target)?** Still NOT RUN. It is deferred to wave 5 (DECLARE-EQUILIBRIUM E6,
  STANDING_RULINGS AJ-7).
- **Q3: how many rulings sit in the transport?** Partly answered. P11 counts 45 DECLARE/AMEND/BATCH files of
  09-19..23, of which 32 are OPEN and not named in the active bundle's RESIDUAL. At ruling granularity, S3 counts 17 standing
  operator requests, and 10 of them have no home. No full per-ruling count exists.

---

## 8. THE QUEUE QUESTION

```
FACT (09-20): waves 1-3 took their work from the spine's STOP and from measurement, not from the backlog.
FACT (09-23): waves 4a and 4b did the same. Their rows (937-961) were filed FOR the waves, as carriers of
              DECLARE decisions, not picked FROM the backlog.
              OPEN rows: 390 -> 441 (+51 in four days; boot banner 134 P1 / 212 P2 / 95 P3; conductor "441 rows").
              O-2 now makes "a real backlog task travels the whole loop" a BUILD MODE exit condition, so the
              operator has partly answered the question: the backlog becomes the queue again when the loop can carry one row.
STILL UNRULED: whether rows 390-441, filed as findings, are ever worked in backlog order, or retired.
```

---

## CURRENT STANDING DECISIONS

Verbatim from 09-20, plus this window's ruled items (the ledger's "Ruled" row), so the next seat does not
relitigate them:

```
- aider DEFERRED, with its consumer named
- library-first is a wired spine stage
- the graph is at ~71% file coverage (was ~70%)
- the peer harness was REJECTED on a measured head-to-head
- byte targets REJECTED as acceptance criteria
- ARCHITECTURE.md KEPT, with a stated exit condition
- ADR-120: the spine is the whole loop (stages + moments), Accepted 2026-09-22
- O-1: secrets live outside every repo; a per-lane env allow-list is wave-5 hardening
- O-2: BUILD MODE ends when (1) the walk is clean on main, (2) one real row travels the loop, (3) a second repo's
  walk passes; 2026-11-18 is the backstop
- O-3/O-4: Copilot budget is licensed and must be a routine producer where the routing table assigns it
- equilibrium (ADR-87 amend.): the browser rules forks, writes Done-when and budget; CC holds state as data
```
