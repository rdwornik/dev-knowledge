# DIGEST — independent crosscheck of the 2026-09-23 audits

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md`, answering
> `to-cc/BATCH-AUDIT-CROSSCHECK-2026-09-23.md`. This is the independent verification pass over
> `2026-09-23-technical-verify-time.md` — read its corrections table before citing a VERIFY-TIME
> number. Scope note carried from the source: two further digests
> (`DIGEST-SELF-CONTAINERIZE-2026-09-23.md`, `DIGEST-TRANSPORT-CONTRACT-2026-09-23.md`) were never
> produced by operator ruling; nothing here covers them.
> Carrier rows: D1-D5 (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`), filed by `lane-landing-window`.

carried-by: CC session (hub root, read-only crosscheck)
answers: to-cc/BATCH-AUDIT-CROSSCHECK-2026-09-23.md
date: 2026-09-23
scope: digest 1 only. The operator ruled that the session finishes without digests 2 and 3, which were never produced.

## Inputs

```
digest | status
DIGEST-VERIFY-TIME-2026-09-23.md | received (DONE 20:30+02:00), crosschecked below
DIGEST-SELF-CONTAINERIZE-2026-09-23.md | NOT PRODUCED (session not launched, operator ruling); no to-cc prompt existed
DIGEST-TRANSPORT-CONTRACT-2026-09-23.md | NOT PRODUCED (session not launched, operator ruling); no to-cc prompt existed
```

## Routing actually served (per step)

```
step | prescribed | served by
orchestrate, assemble | Sonnet | claude-opus-5-5 (the session model; no Sonnet switch was made). Deviation.
read sources >50 KB | Gemini via agy | not needed: the digest is 15 KB and was read directly; the CI logs were filtered by script
lookups | Haiku | orchestrator (gh run list / gh api job logs, git log). Deviation: no Haiku spawn
independent verification | Codex sol, read-only | codex exec -m gpt-5.6-sol -s read-only, fed claims and source paths only, never the digest's reasoning
recommendation challenge | Codex sol | same run, asked blind ("what would you change first")
```

- **CI evidence for Codex was pre-fetched** into job scratch and passed to it as file paths: the 20 completed conductor.yml runs ending at 3d3b3a0e, their per-job times, and per-run pytest failed/regression counts from the job logs.
- **The orchestrator re-tabulated the per-run counts** after Codex saw only 12 of the 20. The cause was a truncation in my first extraction, not in the data.

## Claims table — VERIFY-TIME

```
# | claim (digest) | source | verdict
C1 | local compare 30-59 min per merge at -n 2 | integrator logs wave4/4b | WRONG as a both-wave range: wave4b -n 2 = 30-59; wave4 ran --workers 4 at 28-39. Holds for wave4b only
C2 | gates.py 14-17 min fixed cost | integrator logs | WRONG: 9-17 min (wave4 L625 9m01s; wave4b 13m59s; wave4 16m36s)
C3 | fleet-health-split pairing fallback ~170 min; gate-verdicts pairing killed at 76, split verify 64 | wave4b log L403-430 | CONFIRMED (2h50m; 1h16m; 1h03m46s)
C4 | ~290-350 dup/discarded pytest min over wave-4b's 5 merges | wave4b log | UNVERIFIABLE: "duplicate" undefined, log shows 6 W4B merge events (handback refused+repair), classification changes the total
C5a | conductor last 20: 20/20 failure; pytest job median ~8 min (4-9) | gh runs + jobs | CONFIRMED: median 8.26 min, range 4.02-8.87
C5b | pytest 88-96 failures, 14-24 REGRESSION | gh job logs | WRONG: 83-96 failed, 9-24 regressions over the same 20 runs (low end at 41021988/1084d79e/71b35fa8)
C5c | commit-gate failed 18/20; ruff/seal/phase-gate 20/20 pass | gh jobs | CONFIRMED
C5d | parity table: CI regressions 3d3b3a0e 16, 10a4c9f5 17, de97dad5 17, e8ec23fc 17, 2fd8f256 17, 3689b5ab 18 | gh job logs | CONFIRMED, all six exact
C6 | full suite = 7,343 tests | newest run: 88 failed + 7223 passed + 29 skipped + 3 xfailed | CONFIRMED
C7 | SUITE-BASELINE-FREEZE.md: 87 reds at c5108329, 2026-09-17 | logs/SUITE-BASELINE-FREEZE.md:14-20 | CONFIRMED
C8 | required-checks ruleset enforcement: disabled | deploy/conductor-required-checks.ruleset.json:4 | CONFIRMED
C9 | select() unions all live_repo files (58) when prose changes and anything else is selected | scripts/impacted_tests.py:302-321, 545-549 (digest said L522) | CONFIRMED (58); line locator drifted
C10 | no RULES entry for logs/MERGE-RECEIPTS.jsonl; gates.py refuses FULL SUITE | impacted_tests.py:222-253; gates.py:125-133 | CONFIRMED
C11 | #960 record on unpushed branch worktree-integrate-lane-verify-in-lane (b32b85df), not on main | git | SUPERSEDED: true at writing; since then main has merge 4667f731 (worktree-lane-verify-in-lane @ ee6215e9, ~21:12+02:00), the audit is on main (4b0171cc), and the old branch is gone
C12 | nothing chooses -n from free memory; -n auto OOM history | resource_lifecycle.py:11-12; pyproject.toml:259-269, 280-288 | CONFIRMED
C13 | on 4/5 wave-4b merges >=90% of selected files come from the prose/live_repo union | impacted_tests.py:545-549; wave4b log L427-429, 456-460 | CONFIRMED (mechanism + gate-verdicts 59/61); per-merge replay not re-run
```

Tally over 16 rows: 11 CONFIRMED (C3, C5a, C5c, C5d, C6-C10, C12, C13), 3 WRONG (C1, C2, C5b), 1 UNVERIFIABLE (C4), 1 SUPERSEDED (C11).

## Corrections to carry forward

- **CI red counts:** 83-96 failed and 9-24 regressions over the last 20 runs. The upward creep is real (9 → 16-17), but it started lower than the digest states.
- **`compare` cost:** 28-59 min across both waves. The "30-59 at `-n 2`" figure is a wave-4b-only figure.
- **`gates.py` cost:** 9-17 min, not 14-17. The floor of the "fixed cost" is lower.
- **Duplicate-minute totals** (wave-4 85/195, wave-4b 293-348) are **judgment, not measurement**. Do not freeze a savings target on them.
- **#960 has landed** (4667f731). Recommendation #4 is no longer a proposal; wave 5 should measure its effect rather than schedule it.
- **Locator drift:** the union sits at `impacted_tests.py:545-549`, not L522.

## Challenge of the top recommendation

- **Digest's #1:** retire the local `compare`/pairing leg in favour of CI's 8-min full suite, after refreshing `SUITE-BASELINE-FREEZE.md`.
- **Codex sol's first change, derived blind:** stop expanding mixed prose+code diffs into all 58 `live_repo` files. Map prose and generated edits narrowly, or verify them once per batch, and keep the lane's direct code/test selection. This targets the repeated 30-64 min merged-tree runs on at least 4 of 5 wave-4b merges, without touching CI's verdict.

**Agreement:**
- Both locate the cost in the merged-tree `compare` run, not in `gates.py`.
- Both keep CI's full suite as the authority.
- Codex's pick is the digest's own #3.

**Disagreement (ordering):**
- The digest ranks retiring `compare` first. Codex ranks the selection fix first, because it has no prerequisite.
- The digest's #1 is blocked on two facts verified above: C7 (freeze 6 days stale, CI 20/20 red) and C8 (enforcement disabled). The `lane-verify-in-lane` record, now on main, also advises against arming required checks before the freeze is refreshed and commit-gate is diff-scoped.
- Codex's order is buildable now; the digest's #1 needs the freeze refresh as its own step first.

## Safe to build on

- **SAFE:** the mechanism findings.
  - The prose-triggered 58-file `live_repo` union (C9, C13).
  - The MERGE-RECEIPTS.jsonl FULL-SUITE hazard (C10).
  - The stale freeze and disabled ruleset (C7, C8).
  - No memory-derived `-n` (C12).
  - CI runs the full suite in ~8 min and is 20/20 red, with exact local-vs-CI disagreement on all six parity SHAs (C5a/c/d, C6).
  - The pairing-fallback cost (C3).
- **NOT SAFE as stated:**
  - The duplicate-minute totals (C4).
  - The low ends of the failure and regression ranges (C5b).
  - The `compare` and `gates.py` ranges (C1, C2).
  - The #960 status (C11, now landed).
- **Wave 5 can freeze on the selection fix (digest #3 = Codex's first) and the freeze refresh.** Retiring local `compare` (digest #1) should wait until the refreshed freeze gives a readable CI verdict.

DONE 2026-09-23T20:57Z (22:57+02:00)
