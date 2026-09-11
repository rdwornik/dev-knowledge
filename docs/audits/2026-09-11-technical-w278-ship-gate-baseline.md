---
lane: w-278-impacted-test-selection
batch: W
recorded: 2026-09-11
head: 1c27ad4f (rows 1, 3) and 2040653c (rows 2, 4, 5) — see "A concurrent fast-forward moved the base mid-capture"
tree-state: CLEAN — no lane work had started when every number below was taken
purpose: the RECORDED BASELINE the archived intake's first ex-ante acceptance criterion demands
---

# `[#278]` — the ship-gate baseline, recorded BEFORE any change

This file exists to satisfy one clause, quoted verbatim from
`docs/intake/archive/2026-07-07-test-suite-hygiene.md` §*Acceptance criteria (ex-ante)*:

> Ship-gate wall-time delta and collected-count delta after cleanup are both
> measured against a **recorded baseline** (recorded before cleanup starts, not
> reconstructed after).

**It is first because it is the one clause that becomes unsatisfiable the moment work starts.**
Every number below was taken on a clean tree at `1c27ad4f`, before the lane's first
content commit. Nothing here is reconstructed.

## Measurement conditions — stated, because a wall-time without them is a rumour

| Fact | Value |
|---|---|
| Checkout | `.claude/worktrees/lane-w-278-impacted-test-selection` (NOT the primary) |
| HEAD | `1c27ad4f` for rows 1 and 3; `2040653c` for rows 2, 4 and 5 — see below |
| Platform | Windows 11 Enterprise 10.0.26200 |
| Logical CPUs | 16 |
| Box load at capture start | 3 % CPU, 3.8 GiB free of 27.67 GiB |
| Toolchain | `uv` 0.11.19 (the ADR-106 exact pin), CPython 3.12 |
| Capture window opened | 2026-09-10T22:32:29Z |

Runs were taken **serially and adjacent in time**, never concurrently: a wall-time
measured while a sibling run saturates sixteen workers measures the sibling.

## The baseline

| # | What | Invocation | Wall | Outcome |
|---|---|---|---|---|
| 1 | Collected count | `pytest --collect-only -q` | 29.06 s | **5723 tests collected** |
| 2 | Full suite | `pytest -n auto --dist worksteal --max-worker-restart=0 --timeout=900 --tb=no -q` (`--group analytics`) | **1446.49 s (24m06s)** | 33 failed · 5682 passed · 8 skipped |
| 3 | Ship-gate code-diff path | `pytest -n auto --dist worksteal -x --tb=short` (no analytics group) | **1149.74 s (19m09s)** | ABORTED at 14 failures · 2810 passed · 6 skipped |
| 4 | Ship-gate docs-only path | `pytest -m live_repo -q` | **809.11 s (13m29s)** | 12 failed · 106 passed · 1 skipped |
| 5 | Gate organ | `python scripts/audit.py ship-gate` | **401 s** | **RED** — 1 hard-fail organ, 52 new/undispositioned WARN |

**Row 3 is a time-to-abort, not a suite time.** `-x` stops the run at the first failures, so
its wall moves whenever the failure set moves. Row 2 is the stable number a later delta should
be measured against; row 3 is recorded because it is what the gate literally runs.

## A concurrent fast-forward moved the base mid-capture — caught, not papered over

This lane's branch was fast-forwarded **by another actor, during the capture window**. It is
recorded here because a baseline that names the wrong base is worse than no baseline, and the
error was found by reading the branch reflog rather than by trusting the session's own memory
of what HEAD was.

```
00:28:10 +0200  branch created at 1c27ad4f
00:32:29 +0200  capture window opens (load probe)
~00:33          row 1 collect-only runs — the run's own output echoes HEAD 1c27ad4f
~00:33-00:52    row 3 runs (1149.74 s)
00:52:55 +0200  EXTERNAL fast-forward 1c27ad4f -> 2040653c (not this session's act)
~00:53 onward   rows 4, 5 and 2 run
01:45:43 +0200  this session's own sync-merge 2040653c -> 3acca581
```

**Attribution per row:** rows 1 and 3 measured `1c27ad4f` (row 1's HEAD is echoed in its own
output; row 3 began ~20 minutes before the fast-forward, and pytest resolves the tree at
collection). Rows 2, 4 and 5 measured `2040653c`.

**Why the numbers still stand.** `git diff --stat 1c27ad4f 2040653c` is **markdown only** — 9
files, `JOURNAL.md` plus the batch-W manifest, six lane contracts and the audits index, with
**no `.py` file and no config touched**. The collected count cannot move on a docs-only delta,
so 5723 holds across both bases, and the code paths those wall-times exercise are byte-identical.
The one real effect is that the doc corpus grew by 1209 lines, which slightly raises the cost of
the corpus-scanning tests inside rows 2 and 4 — in the direction of making those numbers
*conservative*, not flattering.

**What this costs a later delta:** nothing for rows 1 and 3, and a sub-percent doc-corpus
difference for rows 2, 4 and 5. It is stated so a future reader compares against the base that
was actually measured rather than the one this file would have claimed.

## Two recorded claims in this repo are now stale, by a wide margin

Both are corrected here rather than left to be trusted — the same discipline
`pyproject.toml` already applied when it corrected its own "~9m42s serial" note.

- `plugins/tier1-lifecycle/commands/ship.md:32-36` claims the docs-only tier costs
  *"~21s tests + ~13s ship-gate ≈ 34s (budget ≤60s)"*, measured 2026-07-05. **Measured now:
  809.11 s + 401 s.** The docs-only tier is ~38× its recorded cost and the stated ≤60 s budget
  is breached by a factor of ~20.
- `ship.md:37-39` claims the code path is *"~2m05s wall vs 9m42s serial"*. **Measured now:
  1446.49 s (24m06s)** for the full parallel suite.

The corpus grew from 2362 collected tests (2026-08-06, recorded in `pyproject.toml`) to **5723**
— a 2.42× growth — which accounts for direction but not for the full magnitude on the docs-only
tier, where 119 selected tests cost 809 s (~6.8 s/test).

## Honest limit — this baseline is taken IN A WORKTREE, and that changes some outcomes

Several failures in rows 2–4 are **worktree-context artifacts, not tree defects**, and this is
verified rather than assumed. `tests/test_normalize_headers.py:223` defines

    _SKIP_PARTS = {".venv", ".git", "node_modules", "__pycache__", ".pytest_cache", "worktrees"}

Every path in this checkout contains the segment `worktrees`, so the live-corpus glob resolves
to zero files and the corpus tests fail their own plausibility floor
(`assert len(files) > 100, "corpus implausibly small (0) — glob is wrong"`).
`tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` fails for the
same structural reason.

**Consequence for any later delta:** compare like with like. A number taken in the primary
checkout is not comparable to a number in this table, and the failure COUNTS above are
worktree-inflated. The wall-times are the transferable half; the pass/fail counts are not.

## What this file does NOT claim

It does not answer the archived intake's second ex-ante criterion — *"the 'why did it get
faster' question is answered with evidence — not a guess — before any cleanup work lands"*.
That criterion is addressed separately in this lane's closing artifact, where the measured
direction of travel turns out to matter: against the repo's own recorded numbers the suite did
not get faster, it got **substantially slower**, which changes what that question is even asking.

No test was deleted, altered, or skipped to produce any number above.
