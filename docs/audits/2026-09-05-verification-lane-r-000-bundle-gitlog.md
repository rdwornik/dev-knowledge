# ONE `git log` for all handoff bundles — lane-r-000, batch R5P

`scripts/audit.py::_select_active_bundle` spawned one `git log --diff-filter=A` **per
candidate bundle directory**. It now spawns **one** for all of them. Selection is unchanged,
and that is measured against a frozen copy of the old method rather than asserted.

no-consumer: a frozen batch-R5P lane contract for a P1 performance hotfix that discharges no BACKLOG row, no ADR and no register entry — its consumer is the batch manifest `docs/audits/2026-09-05-technical-batch-r5p-manifest.md`, and this lane files no row by contract.

**Branch:** `worktree-lane-r-000-bundle-gitlog` · **SHAs:** `815fa5c4` (RED), `1045d98e` (GREEN)

## Measured, not asserted

Both arms instrumented on the observed spawn argv, same tree, same 87-candidate set, in one
process. Selection agreement is checked in the same run, because a speed number for a
function that answers differently is not a speed number.

```
                         git spawns   git log   wall       result
BEFORE (per-directory)       90          87     25.714 s   add-date / 2026-09-01-dev-knowledge-architect-v7
AFTER  (batched)              3           1      0.826 s   add-date / 2026-09-01-dev-knowledge-architect-v7

identical selection : True
git log spawns      : 87 -> 1
wall clock          : 25.71 s -> 0.83 s   (31.1x)
```

The three surviving spawns are the two `rev-parse` guards plus the one batched log.

`audit.py health`, wall-clock, **paired on the same tree** — the pre-change `audit.py`
restored from `815fa5c4` for the BEFORE arm, both runs `health: OK`:

```
BEFORE : 1m07.782 s
AFTER  : 0m37.984 s
delta  : -29.80 s
```

That delta is the selector's own 24.9 s plus run-to-run variance, so the saving lands where
the change is and nowhere else.

**A fourth number, reported because it was the lane's first reading and it is confounded.**
The initial BEFORE was **82.78 s** with `health: DEGRADED`, taken before a sync-merge of
`main` and therefore on a different tree with a different check outcome. It is not comparable
to the 37.98 s AFTER and is not the number this artifact stands on; the 67.78 s paired run
replaced it. Recording it rather than dropping it — the dispatcher's own figure (118 spawns /
46.4 s) was likewise measured on a tree that is not this one.

## What changed

One function, plus one module-level constant and a six-line helper beside it.

- **The batched call.** `git -C <repo> -c core.quotePath=false log --diff-filter=A --reverse
  --format=%x02%at --name-only -- docs/handoffs/<a> docs/handoffs/<b> …`. `%at` gives each
  add-commit's date; `--name-only` says *which* bundle that commit added; the `\x02` sentinel
  separates the two so a filename can never be read as a timestamp. `--reverse` is
  oldest-first, so the first commit naming a bundle carries its add-date — the same value
  `lines[0]` carried when each directory was walked alone.
- **Attribution splits on path segments, never a string prefix.** `2026-07-20-x` is a prefix
  of `2026-07-20-x-arc5`; crediting arc5's add-commit to the plain slug converts an active
  bundle into a stale one, which is `[#372]`'s "green about the wrong file" re-entering
  through the batching door. `core.quotePath=false` stops a non-ASCII slug arriving
  octal-escaped and silently unmatchable, which would misreport a tracked bundle as fresh.
- **Chunked above a stated bound** (frozen default exercised — reported, not asked). Windows
  caps a command line at 32767 characters, so an unbounded pathspec list is a crash waiting
  for a large enough corpus rather than a graceful degradation.
  `_BUNDLE_LOG_PATHSPEC_BUDGET = 24_000` counts pathspec bytes only, leaving the
  `git -C <absolute path> …` prefix its own room. The live corpus is **4394 B → 1 chunk**,
  and the budget holds ~470 bundles before a second call. Invocation count is O(chunks),
  driven by argv length and never by candidate count.

### Deliberately unchanged

- **The env scrub.** The batched call goes through the same `_run`, so `_git_location_env()`
  still applies and is still scrubbed **by name**. An inherited `GIT_DIR` resolving the guard
  to a foreign toplevel is the `[#355]` recursion; a test asserts the scrub over the calls
  that now *exist*, including the batched log, and asserts the identity/transport vars it
  must not strip survive.
- **Every failure mode.** A failing `git log` degrades — never a lexical guess, because that
  fallback *is* the defect this selector replaced. An unparseable date degrades. A bundle
  with no add-commit (untracked **or** staged) is still `fresh` and still outranks every
  tracked one. Two fresh candidates still return `bundle=None` as `ambiguous` rather than
  silently picking one.
- **Nothing else in `audit.py`.** Not a neighbouring check, not an import tidy, and
  explicitly not the fleet-automation commit path, which sets `GIT_INDEX_FILE` on purpose via
  its own `env=` dict.

## How selection-identity is proved

`_perdir_select` in `tests/test_verify_handoff_probes.py` is a **frozen copy** of the
pre-batching method — a copy, not an import, because an oracle that imports the
implementation it checks agrees with it by construction. It passed *before* the production
change landed, which is the pre-condition that makes it usable as a judge afterwards.

Ten seeded shapes cover every kind the selector can return — `sole`, `fresh` (untracked and
staged), `add-date`, `ambiguous` (two untracked; untracked + staged), unborn-HEAD, `no-git`,
nested-repo `degraded`, and the prefix-sibling shape — each asserting both methods return the
same bundle **and** the same kind, plus a separately pinned expected kind so a shape that
quietly stops exercising its case fails rather than agreeing vacuously.

**The live-tree arm is the one that mattered.** git computes history simplification over the
**union** of the pathspecs, not over each one alone, so a batched walk is not equivalent to N
single-pathspec walks by construction — the seeded histories are linear and cannot show it.
`test_batched_and_per_directory_selection_agree_on_the_live_tree` runs both methods over all
87 live bundles, merges and renames included. They agree.

## Gate state

- Targeted tests: **158 passed** — `test_verify_handoff_probes.py`, `test_proof_layer.py`,
  `test_gitenv.py`, `test_v6_frozen_contract.py`. The five RED assertions from `815fa5c4`
  are green.
- `ruff check`: clean on both changed files.
- `audit.py health`: **OK** (exit 0).
- Full suite **not** run: a lane runs the targeted tests for its diff; the full suite runs
  once, at integration (`[#528]`).

## Open items for the integrator

1. **`tests/test_audit.py::test_check_fleet_parity_green_on_live_repo` is RED, and it is not
   this lane's.** Two WARN-undeclared findings: `VISION.md` absent as a SHOULD surface (it
   was relocated to `docs/archive/VISION.md` by `[#614]` lane-e-5) and
   `.claude/commands/boot-session.md` covered by no manifest row or roster expectation.
   **Proven foreign, not argued:** the pre-change `audit.py` was restored from `815fa5c4`
   and the test re-run alone — byte-identical failure. Reported, not fixed; both causes are
   governance declarations outside a hotfix lane's scope.
2. **The new tests carry no `@_needs_git` skipif, deliberately.** `proof_layer` ratchets the
   environment-conditional guard population against a committed baseline with zero headroom,
   so 11 new guards would have required regenerating `ecosystem/proof-layer-baseline.json`
   — a **curated-baseline touch**, a V-2 escalation class, and one a background lane cannot
   escalate without wedging. Dropping the decorator is also what that gate's own doctrine
   asks for: a proof that can be skipped on the machine where git is the thing under test is
   not a mechanism. Without git these tests error loudly instead of reporting a green they
   did not earn. A comment in the file says so, so nobody restores it for symmetry.
3. **The lane sync-merged `main` once, `--ff-only`, creating no merge commit.**
   `journal_spine_anchor` blocked the first commit on four foreign spine entries. The
   two-line split diagnostic showed the gap in this tree and **empty** against `main`'s
   `JOURNAL.md` — pure lane tree-lag, not a real gap on main. `git merge --ff-only main`
   from zero lane commits cleared it (re-diagnosed after: `[]` in both). No `SKIP=`, no
   `--no-verify`, no JOURNAL entry.
4. **The declared consumer does not exist yet.** The contract names
   `docs/audits/2026-09-05-technical-batch-r5p-manifest.md`; no such file is in the tree at
   this lane's STOP. The `no-consumer:` line above satisfies the landing leg either way; the
   consumption leg reports this artifact as unconsumed until the manifest lands and links it.
5. **The audits index was not regenerated** — a batch lane leaves `docs/audits/README.md`
   stale by design, and `audit-index-freshness` is scoped to the index and its generator for
   exactly that reason (`[#590]`).

## Honest limit

Equivalence under union history simplification is **measured on this corpus, not proved in
general**. A history where a bundle's oldest add is reachable only through a merge that the
union pathspec prunes differently from a single pathspec would diverge, and no test can rule
that out for a corpus that does not exist yet. The live-tree agreement test is the standing
guard: it re-measures on every run, against the tree as it actually is.
