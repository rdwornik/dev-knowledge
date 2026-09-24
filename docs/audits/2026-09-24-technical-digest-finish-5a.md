> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-browser/DIGEST-FINISH-5A-2026-09-24.md` (a Drive transport path, not retained in
> this repo — verifiable against the bytes landed below by their hash,
> `sha256:fc52cb97592ce2a1c559ff419817f0bfd1f6820adf13a7a26c9dfbc35a4fcd55`, 6,891 B, computed by
> this lane at landing time).

---

# DIGEST -- FINISH-5A, 2026-09-24

from: the INTEGRATOR (CC, Opus 5.5, job c3c952db, seat bound for WAVE5A) · order to-cc/FINISH-5A-2026-09-24.md
base main 536786b8 · final main 665e2a3b · receipt (full evidence): to-browser/SESSION-finish-5a-2026-09-24.md

## 1. Merges (sha on main, pickup -> push minutes, verdict local | CI)

```
lane                          sha on main  push (Z)  min  local                                         CI (paired by node id)
lane-one-registry-ci   5A-1   a40468c4     12:40     76   ship-gate 0/0 hard-fail, WARN 363->363;       clean (new: 1 flake, red on
                                                          lane tests green (1 xdist flake, 39/39 -n 0)  main's own run too)
lane-graph-stage-edge  5A-10  715c7f32     12:40     65   ship-gate 0/0, WARN 363->364 (finding)        clean (0 new vs step 2)
lane-landing-night-f.  5A-11  665e2a3b     13:04     28   ship-gate 0/0, WARN 364->366 (findings)       clean (0 new vs step 3)
```
- Step 2 is the repair-1 handback 0d750e2d, rebuilt on 536786b8; the three refusal reds are gone (CI and local).
- Step 3: SUBSTITUTION Copilot -> Sonnet 5 (Copilot reaped 07:23, 0 commits). **The lane did NOT edit ecosystem/harness.yaml**
  (0 lines), so the architect's (a)-(c) ruling did not arise: the edge already lives in scripts/file_purpose_graph.py +
  graph_queries.py. It retired one test whose premise its own edge falsified (single_flight.py is an orphan) -- accepted,
  not a weakened check; finding: intake #86 AC 2 has no live witness left.
- Step 4 landed PARTIAL by necessity (below). Its JOURNAL "(k)" collided with mine and was re-lettered (m) at merge.
- Stacked: step 3 was verified on step 2's merge; each merge commit carries its own ledger line; tree == verified tree + ledger.
- The merge receipts recorded 0 timed steps and no model reading again (WALL 72.7 / 46.6 / 17.1 min).

## 2. Baseline id

`2026-09-24-6b1c6bf4df83` -- logs/KNOWN-REDS-REGISTRY.json, now on main (a40468c4), measured at aca2385b, 88 members
(72 pre-freeze, 4 [#664] witnesses, 12 attributed, none anonymous).

## 3. Orphan census

```
before  18 findings  (536786b8 / 4eba148d)
after    8 findings  (on main 715c7f32): .claude/commands/spine.md, .claude/commands/why.md, scripts/ci_verdict.py, dodo.py,
                     handback.py, hook_expiry_verdict.py, plan_lint.py, ship_gate_diff.py
resolved 10          dispatch, gates, go_reader, lane_digest, memory_admission_gate, no_leftovers, stage_library_first,
                     stage_prior_art, test_pairing, worktree_occupancy
```

## 4. Documentation tier (pytest -m live_repo, final main 665e2a3b, no cap, memory gate -n 2)

- 53 min 22 s: **30 failed, 167 passed.** (Last night's 900 s cap run did not finish; this one did.)
- Paired by node id with the known-reds registry: **30 of 30 in it** -- 29 pre-freeze, 1 attributed
  (test_boot_retrieval::test_repo_tracked_boot_base_is_under_its_ceiling -> buildlist-l6-hazard @ d7ce1d43).
- **Reds not in the registry: none.**

## 5. Session janitor

```
before  12 claude.exe, 2,431 MB (11:40Z)
stopped e52f9fb2 (this order's lane) + 937de568, 380fd9bd, 8db6dce2 (at teardown; each printed stopped/removed).
        No other WAVE5A job of the dispatcher receipt was still resident.
after    6 claude.exe, 1,185 MB (13:07Z); free 3.85 GB
remains 0eca324c -- finished background session from 09-21 ("architect jutra comparison batch"), NOT WAVE5A: outside this
        order's scope, left for the operator (326 MB) · 23160 the background daemon · 16696 an interactive `claude agents`
        view (never stopped) · this seat
```

## 6. Origin branches (13:08Z, after fetch --prune)

```
main · automation/fleet-audit (protected) · claude/conformance-2026-09-18 .. 09-24 (7, protected)  -> no leftover
```
- Every lane branch and every CI integration branch of this order was deleted. No Copilot branch ever existed.
- Teardown: no_leftovers CLEAN (11/11) for all three lanes. The %TEMP% fleet-health-producer worktree no longer exists
  (no directory, not registered) -- nothing to remove.

## 7. The two checks

- **(a) none.** No hook, check or script reads `~/.claude/settings.hooks-DISABLED-2026-09-17.json` or its expiry. The only
  mentions are prose: JOURNAL.md:1056, a comment at ecosystem/organ-registry.yaml:100, tasks/927-*, and
  docs/audits/2026-09-23-technical-hook-architecture-appendix.md. **The 09-24 date was prose only.**
- **(b) P9:** `validate_backlog.py` -> OK, 0 hard-fails (488 tasks at 536786b8; 491 at 665e2a3b; 2 WARN: story S24 has no
  tasks, [#426] is past its review_date).
  **P11:** carriage_verdicts over the transport -> 178 decision files: 155 resolve on main, 23 state literal OPEN (leg 2:
  discharged only when a bundle's RESIDUAL names them, at assemble time), 0 without a carrier -> leg 1 passes.

## 8. Findings from this order (for rows)

- The landing lane could file only 3 of 15 findings as rows: **BACKLOG.md sits at the [#589] 100,000 B view ceiling**
  (gen_task_tree refuses above it; 23 B headroom now). 12 findings live in LESSONS.md (2026-09-24 entry). Rows filed:
  [#1010] [#1012] [#1014]; cited: [#966] [#971] [#976].
- The 3 reaps this session (my step-2 tests, step-3 ship-gate, CI wait) confirm [#1012]: heavy runs must be detached
  processes. From then on I ran them detached, with foreground waits: 0 further losses.
- A merge commit still runs no pre-commit registry ("Checking merge-conflict files only") -- [#1014].
- MY DEFECT, caught before push: a rebuild that took the verified tree's ledger file dropped the previous merge's ledger
  line. Fixed by an amend before the push. Lesson: rebuild the ledger file as base + new line, never copy it whole.
- The docs-tier output wraps FAILED in ANSI colour codes: a pairing parser must strip them (mine first read 0 ids).
- review_artifact_coverage 201 -> 202: step 2's Codex review lives only in its session file, not in-repo.
- The ship-gate base output from last night was cp1252-mangled; the line diff needs encoding normalization.
- The step-3 HANDBACK line sat inside backticks again (accepted).

## 9. What is left

- **OPERATOR-ACTION: the [#589] BACKLOG view ceiling** -- raise it (architect precedent: the 2026-09-01 re-baseline) or
  groom rows, then file the 12 LESSONS-held findings as rows.
- Carried from the WAVE5A digest and still open: the block-onedrive sidecar redate in ~/.claude (check (a) confirms
  nothing reads it); re-upload protocols/HANDOFF_BOOT.md; ADR-121 D1; handoff-repair's HANDOFF_PROCESS 7.2.0 bump at the
  next cut.
- step 2's ROW 5: 8 CI-only reds unadjudicated; logs/SUITE-BASELINE-FREEZE.md stays until they are.
- 0eca324c (a finished session from 09-21) is still resident -- stop it at your discretion.
- The 8 remaining orphans carry fates owed by wave 5b.
- WAVE5A: every lane MERGED (13 of 13 merges across the two sessions); nothing WAITING.
