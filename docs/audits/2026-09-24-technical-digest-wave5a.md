> **Status:** landed verbatim by `lane-landing-night-findings` (LANE-5A-11) from the transport.
> Source: `to-browser/DIGEST-WAVE5A-2026-09-24.md` (a Drive transport path, not retained in this
> repo -- verifiable against the bytes landed below by their hash,
> `sha256:ea0078ff9d114f8b9866c53bc2284134f676c607df481b01794e1e2ea04c7aa9`, 12,791 B, computed
> by this lane at landing time). Carrier rows: three of the Done-contract
> item 1 findings landed as full backlog rows -- `[#1010]` (Stop hook / HANDBACK grammar),
> `[#1012]` (dispatcher-held producer must run detached from the reaper), `[#1014]` (post-merge
> check before push, `--no-ff` bypasses pre-commit) -- and three more were already covered by an
> open row, cited rather than duplicated: `[#966]` (D3/CI-as-gate), `[#971]` (autonomy liveness
> watchdog), `[#976]` (merge_receipt timed steps).
>
> **The remaining 12 findings could not be filed as rows tonight.** `gen_task_tree.py
> --emit-source` REFUSED at 15 new rows (102,182 B against the 100,000 B `_VIEW_BYTE_CEILING`
> from `[#589]`); with only `[#1010]`/`[#1012]`/`[#1014]` landed, the regenerated view sits at
> 99,977 B -- 23 B of headroom, none left for a fourth row of any length. Per the pre-authorized
> WAVE5A ruling to decide by this lane's own Value line rather than wait for the operator, and
> because this lane's own Do-not bars changing code (so `_VIEW_BYTE_CEILING` is not this lane's
> to move -- the one prior re-baseline, 2026-09-01, was the architect's own ruling, not a lane's),
> the remaining 12 findings are recorded verbatim in `LESSONS.md` (2026-09-24 entry, this lane)
> instead, with the ceiling collision itself named as an `OPERATOR-ACTION` item below so a
> deliberate re-baseline (or a grooming pass) can unblock filing them as rows next session.
> DECIDED-BY-LANE: land what fits as real rows, defer the rest losslessly to LESSONS.md, name the
> blocker -> no finding is silently dropped, and no code is changed to force them all in.

carried-by: OPEN
lands-via: lane-landing-night-findings files backlog rows for what fits under `[#589]`'s view
  ceiling and LESSONS.md entries for the rest (in-repo provenance: ADR-120 + this record), so
  tonight's findings become data in the repo either way
date: 2026-09-24
from: lane-landing-night-findings (LANE-5A-11, CC sonnet)

---

# DIGEST -- WAVE5A integrator, 2026-09-24

from: the INTEGRATOR (CC, Opus 5.5) · base main 4667f731 · final main 536786b8 · closed 2026-09-24T05:34Z (the 05:30Z deadline; two lanes still WAITING)
receipt (full evidence per merge): to-browser/SESSION-integrator-wave5a-2026-09-23.md

## 1. Merges (priority order of landing; pickup-to-push minutes; verdict local | CI)

``
lane                     sha on main  push (Z)  min  local ship-gate / compare                          CI (paired by node id)
postwave-changelog       9fdccf0f     00:31     155  0 hard-fail; CI-paired (registry not ready)        clean
lane-memory-gate    5A-3 aca2385b     00:38      68  0 hard-fail; CI-paired                             clean
lane-adr-state-store     c9132e7f     01:43      62  0 hard-fail; docs-only (ADR-121 stays Proposed)    clean
lane-hooks-urgent   5A-7 50a257d2     02:32      30  0 hard-fail after repair 1; 3 reds pre-existing    clean
lane-ci-verdict     5A-6 30930b1e     03:19      49  0 hard-fail after repair 1; compare rc=4           clean
lane-handback-fixes 5A-4 7104f588     03:38      31  0 hard-fail; +3 proof_layer (finding)              clean
lane-landing-window 5A-5 297c44ec     03:53      43  0 hard-fail after repair 1; +12 WARN (findings)    clean
lane-handoff-repair 5A-9 10b1570e     04:14      64  0 hard-fail after repair 1; compare rc=0 CLEAN     clean
lane-test-selection 5A-2 fab80bd7     05:08      85  0 hard-fail after repair 1; compare KILLED (mine) clean (1 flake, DECIDED)
lane-provider-reg.  5A-8 536786b8     05:17      26  0 hard-fail after repair 1; compare rc=4           clean
``
- "min" = handback pickup (or repair-handback pickup) -> push. compare rc=4 (UNATTRIBUTABLE: selected test files the
  registry never ran) was the norm tonight; every such merge was covered by the CI full-suite pairing, and local stayed
  authoritative. CI branches were deleted from origin as soon as each verdict was recorded.
- CI's branch-run artifacts (4 ids red only on non-main dispatch runs, green locally) were excluded from every pairing:
  test_provision_legs::test_history_check_exits_0_on_this_repo, test_validate_branch_naming::test_local_branches_reads_the_live_repo,
  test_worktree_seed::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH, test_worktree_seed::test_the_verdict_names_WHY_rather_than_only_failing.

## 2. Refusals (all written by the INTEGRATOR, `repair N of 2`; none reached a third)

``
lane-hooks-urgent    00:00Z  organ_truth: a new organ with no fate; review record unconsumed -> cured, merged
lane-ci-verdict      01:15Z  a red in its own new test; no fate; record unconsumed               -> cured, merged
lane-handoff-repair  02:12Z  assemble_paste.py named the ledger file (test_decision_coverage red)  -> cured, merged
lane-landing-window  02:55Z  row [#1000]'s YAML-escaped title red test_preflight_freeze_predicates -> cured, merged
lane-test-selection  03:05Z  its row re-issued [#963], spent by ADR-121 (gen_task_tree refused)    -> cured ([#1009]), merged
lane-provider-reg.   04:30Z  its two new records declared no consumer at all                     -> cured, merged
lane-one-registry-ci 04:40Z  3 reds: silent-rule ratchet 453>452 x2, connection_loop unreached list -> repair 1 handed back
                             0d750e2d at ~05:28Z, NOT verified (close)
``

## 3. Median before / after test-selection

- Pickup-to-push, the merges that landed BEFORE test-selection (8): 155, 68, 62, 30, 49, 31, 43, 64 -> median 55.5 min
  (30 / 31 / 43 / 49 / 62 / 64 / 68 / 155). AFTER test-selection (1): provider-registry 26 min -- one point, not a median.
- merge_receipt.py median prints 17.9 min, but only over older receipts: it EXCLUDES every WAVE5A receipt (0 timed steps
  each), so it measures nothing from tonight. The before/after comparison the order asks for cannot be read off the
  receipts yet.
- Documentation tier (`pytest -m live_repo`, once, on final main 536786b8, -n 2): DID NOT FINISH -- my 900 s cap expired
  (rc=124) with at least 178 of 191+ results in, 31 of them F. No node ids were written, so none is attributed against the
  registry. LEFT OPEN: rerun without the cap and pair its reds with the registry's 71.

## 4. Reaps

- reap 1 (mine, ~00:05Z): the harness reaped my background CI wait (bg-shell pressure). Nothing lost, since CI runs off-box;
  after that, waits ran in the foreground or were bounded by a deadline.
- Lanes reported memory/reaper kills of their own ship-gate/pytest runs: memory-gate (2 stalls + 1 kill), ci-verdict (2),
  handback-fixes (2, then adopted the merged memory gate). Each lane left that step to the integrator instead of retrying.
- Dispatcher 05:08 local: ~7 finished lane/repair `claude` processes stayed resident (~360-400 MB each), which held a repair
  below the 3 GB threshold. At each teardown the integrator stopped and removed the lane's jobs; several lane jobs' stop/rm printed nothing, which is recorded rather than claimed.

## 5. Operator inputs this session

- Mid-session order (teardown): postwave-changelog and adr-state-store are in my queue and are torn down like a lane
  (done, recorded in the receipt); every CI integration branch is deleted from origin once its verdict is recorded (done);
  at close, list origin's branches and name leftovers (section 7).
- No other operator input; no operator wait was taken.

## 6. Registry and baseline id

- Batch registry: logs/receipts/TEST-PAIRING-REGISTRY-WAVE5A.json (schema test-pairing-registry/1, gitignored), 120
  test files at 4667f731, 71 red, 31 skipped, 0 base flakes; recorded 22:00Z -> 01:40Z (3 h 40 min, too slow to gate the
  first merges -> CI pairing substituted, DECIDED). sha256 0D125C6A2536...
- Known-reds registry carried by lane-one-registry-ci: logs/KNOWN-REDS-REGISTRY.json, baseline_id
  2026-09-24-6b1c6bf4df83 -- NOT on main yet (lane-one-registry-ci WAITING); the batch registry has no baseline_id field.

## 7. Origin branches at close

```
main
worktree-lane-one-registry-ci      a lane still waiting in my queue (repair 1 handed back 0d750e2d) -- not a leftover
automation/fleet-audit             LEFTOVER by the rule's letter; explicitly protected (organ replication branch) -- keep
claude/conformance-2026-09-18 .. claude/conformance-2026-09-24 (7)
                                   LEFTOVERS by the rule's letter; protected until absorbed (conformance digests,
                                   not this batch's) -- 7 unabsorbed digests is itself a finding for the morning
```
- Every integration branch pushed for a CI verdict was deleted once recorded (none remain on origin).
- Every merged lane's origin branch was deleted at teardown (postwave-changelog and adr-state-store per the operator's teardown order, landing-window, handoff-repair,
  provider-registry; the
  others were never on origin). Local: main, automation/fleet-audit, worktree-lane-one-registry-ci and
  worktree-lane-graph-stage-edge (both WAITING). Not mine: a fleet-health-producer temp worktree under %TEMP%.

## 8. What is left

- **lane-one-registry-ci (5A-1)**: repair 1 handed back @ 0d750e2d at ~05:28Z -- verify and merge (priority 11). Its merge
  must be rebuilt on 536786b8; its baseline id lands with it.
- **lane-graph-stage-edge (5A-10)**: launched after provider-registry merged (worktree at 536786b8, no session file
  yet) -- WAITING, not handed back.
- The documentation tier: rerun to completion on main and attribute its reds.
- One-time rows owed from tonight's findings (below); handoff-repair's HANDOFF_PROCESS 7.2.0 bump at the next cut.

## MORNING

### OPERATOR-ACTION
- **block-onedrive expiry (hooks-urgent):** the 2026-09-17 emergency disable lives at
  `~/.claude/settings.hooks-DISABLED-2026-09-17.json` (user home; the lane could not touch it). Give it the same redate
  the lane gave the repo's three entries: `expiry: "2026-10-08"`, `reenable_when: "awaiting the hook target design (wave 5b)"`.
- **Re-upload `protocols/HANDOFF_BOOT.md` to the browser project** (handoff-repair merged 10b1570e; its ROLE PIN sha changed,
  so a seat holding the old copy refuses, as designed).
- **ADR-121 question (adr-state-store, D1):** may the harness act on a change saved on the machine that made it but not yet
  pushed? The draft says "no" for anything another seat or machine reads, and "yes" only inside the integrator's own step.

### QUESTION
- none filed tonight (no QUESTION-*wave5a* file; the lane-level QUESTION files on the transport are from earlier batches).

### DECIDED-BY-LANE (one line each; full text in each SESSION-lane-*.md)
- memory-gate: test_pairing wired to the gate through a subprocess/CLI boundary (keeps test_pairing stdlib-only); no row for
  D7 (landing-window files it); its ship-gate self-check left to the integrator after stalls + a reaper kill.
- test-selection: replayed the five wave-4B merges that have a measured compare time as its "measured proof"; filed and
  registered its own row (later renumbered [#963] -> [#1009] on refusal); dated new artifacts 2026-09-24.
- hooks-urgent: redated the three 09-17 emergency disables to 2026-10-08; did not touch block-onedrive (user home).
- landing-window: folded three window items into open rows [#961]/[#962]; replaced [#908]-[#914]'s fabricated AMEND-*
  provenance; ship-gate self-check left to the integrator after a stall.
- ci-verdict: a three-value verdict (green/red/not-run), with every GitHub-access absence folded into not-run plus a reason;
  a new organ beside actions_verdict.py rather than on it; the verdict goes to logs/receipts/CI-VERDICT-<lane>.json,
  not a new harness moment; full pytest and hard-fail identification left to the integrator after two memory kills.
- handback-fixes: merged origin/main to adopt the memory gate after two reaper kills; no rows for D10/D11/D14/D23
  (landing-window files them); conformance.md staleness + proof_layer WARNs left open.
- handoff-repair: review record kept in its session file (no new path); HANDOFF_PROCESS stays 7.1.0 (bump owed at the next
  cut); edited the v5 HANDOFF_BOOT template + 2 gen_handoff tests outside Owns (the "bundle forms" live only there);
  lane-contract template spells `**Files you own:**` (plan_lint reads only that label); gen_handoff dispatch helpers left dead.
- dispatcher: repairs launched with plain `claude --bg` in the lane worktree; finished sessions were not stopped
  (outside its role).

### DECIDED (integrator)
- CI full-suite pairing substituted for the unfinished registry on the first merges (postwave, memory-gate).
- A consumer_at_landing / funnel_coverage WARN on a lane's own record that declares 
o-consumer:` (or names a consumer)
  is a finding, not a refusal; a record with no declaration at all would be a refusal.
- handback-fixes' +1 entries in the consumer and funnel baselines accepted (the record declares no-consumer:; the batch-F
  provenance records the same escape).
- provider-registry's backticked HANDBACK line accepted as a handback.
- The test_wal_concurrency_smoke_real_processes red in test-selection's CI run = a flake ("database is locked"; 3/3 green
  locally; untouched by the lane).

### Findings (for rows; not filed tonight)
- **Two handbacks reached me late**: test-selection (2 h 06 min; most likely swallowed by orphaned poll loops) and
  provider-registry (4 h 23 min; its HANDBACK line sat inside backticks). Nothing enforces the handback grammar at write
  time. My poll now tolerates backticks.
- **Monitor expiry leaves the poll's bash children alive on Windows** (34 orphans killed at ~01:50Z); poll.sh now exits itself.
- **merge_receipt records 0 timed steps** for every merge tonight; `median` excludes all of them, so its 17.9 min is from
  older receipts only.
- **A --no-ff merge commit runs almost no pre-commit hooks**: my first test-selection build (d908b6eb) committed a
  conflict marker in JOURNAL.md and a manifest missing 45 nodes, and no hook refused it. I caught it from the
  generator's refusal and discarded it before push.
- **Preflight test fragility**: test_iii_a picks the first open row by string sort, so any id sorting first with an
  escaped-quote title reds it.
- The test-pairing registry lives in the primary's gitignored logs/receipts; compare resolves its own worktree's (rc=2 until copied).
- Owns-list drift: hooks-urgent (deploy manifest, organ registry) and handoff-repair (template + tests) edited outside
  their literal Owns lists; each said why.
- handback-fixes' handback called 3 new proof_layer guards "pre-existing"; they are new.
- landing-window lands 11 audits with no ledger disposition (+11 funnel_coverage WARNs).
- ci-pair.ps1 must run from the repo: from elsewhere, gh resolves the wrong repository.
- dispatcher plan_lint grammar defect (reported earlier in the receipt).
