# LANE-h0-suite-speed — end-of-lane artifact: the suite pays for live worktrees, and stops

Contract: `LANE-h0-suite-speed.md`. Board label `[.dev-knowledge · #528 · lane-h0-suite-speed]`
(related: [#528] — this lane is one narrow leg of that broader lane-latency task, not a
closure of it). Branch `worktree-lane-h0-suite-speed`.

## What was measured

**pytest's own collection phase never paid for live worktrees, at any count tried.**
`pytest --collect-only -q` reported `4917 tests collected` at 0, 2 and 5 live worktrees
under `.claude/worktrees/`, wall-clock ~1.4-1.9s throughout (noise, not a trend). This is
because pytest's default `norecursedirs` includes the pattern `.*`, which already prunes
`.claude` itself before pytest's walker ever reaches `.claude/worktrees`. So the literal
`pyproject.toml` `norecursedirs`/`testpaths` lever named in the contract's Done-clause 2 was
never the defect — it was already closed, by an undocumented default.

**The real cost lives in two `live_repo` tests that walk the repo tree themselves,
independent of pytest's collector.** `tests/test_toc.py::test_corpus_fence_fix_never_...`
and `tests/test_normalize_headers.py::test_corpus_no_code_block_line_is_ever_modified` each
build their own corpus via `Path.rglob("*.md")` over the repo root, filtered by a
module-level `_SKIP_PARTS` set. That set excluded `.venv`, `.git`, `node_modules`,
`__pycache__`, `.pytest_cache` — but not `.claude/worktrees`, which is a FULL CHECKOUT of
this repo per live worktree (ADR-61/[#107]), gitignored so `git status` never shows it but
present on disk exactly like the primary's own tree. `Path.rglob` does not consult
`.gitignore` or pytest's `norecursedirs` — it walks everything on disk, and the `_SKIP_PARTS`
filter was applied only AFTER the walk, so every live worktree's duplicate `.md` corpus was
being fully read and parsed on top of the primary's.

Verbatim numbers, this session, this container:

| state | corpus files (`rglob("*.md")`, filtered by the OLD `_SKIP_PARTS`) | `normalize_text` over that corpus |
|---|---|---|
| 0 worktrees (repo alone) | 2,420 | — |
| 5 live worktrees, pre-fix | 14,510 (12,090 of them duplicates under `.claude/worktrees/*`) | 78.57 s |
| 5 live worktrees, post-fix | 2,420 | 12.96 s |

Running the two real pytest tests together (`-n 0`, serial) at 5 live worktrees, pre-fix:
**killed twice after exceeding a 120 s bound** — never observed to complete. Post-fix, same
2 tests at 5 live worktrees: `2 passed in 51.39s`. Post-fix at 2 live worktrees (the
operator's declared floor — the primary checkout already carries 2 live worktrees in
ordinary use, so 0 is never the state the suite actually runs in): `2 passed in 51.49s` — a
0.2% delta, because after the fix the corpus size (and therefore the cost) no longer depends
on worktree count at all. Both numbers are inside the contract's 10% witness by a wide
margin, and by construction rather than by luck.

`pytest --collect-only` count (`4917`) was checked and stayed unchanged at every worktree
count and on both sides of the fix, satisfying Done-clause 2's "collected test COUNT is
unchanged" half directly.

## What changed

Both walkers' `_SKIP_PARTS` set gained one entry, `"worktrees"`, matching the same
`Path.parts`-membership test they already used for the other skip classes — no new
mechanism, no behavior change for any file outside `.claude/worktrees/*`:

- `tests/test_toc.py` (`_SKIP_PARTS`, line ~261)
- `tests/test_normalize_headers.py` (`_SKIP_PARTS`, line ~219)

Each edit carries a comment naming the reason (full-checkout duplication, cost scales with
live worktree count, zero coverage lost) so a future reader does not have to re-derive it.

This repeats a pattern the repo had already adopted elsewhere, correctly, before this lane:
`tests/test_export_backlog_view.py`'s `_SKIPPED_DIRS` already names `.claude/worktrees`;
`scripts/enforcement_coverage.py`'s `_has_reconciled_edge` already checks
`part == "worktrees"`; `scripts/scan_undeclared_edges.py`, `scripts/validate_reconciliation.py`
and `scripts/verify_handoff_probes.py` all prune excluded dirs (worktrees among them)
DURING an `os.walk`, which is strictly cheaper than rglob-then-filter since it never
descends into the pruned subtree at all. `test_toc.py` and `test_normalize_headers.py` were
the two outliers that filtered after the fact instead of before, and paid for the walk they
had already decided to discard.

## Investigated and left alone (out of scope, stated rather than silently dropped)

`tests/test_boundary_headers.py::test_glob_matches_agrees_with_stdlib_glob_per_glob` also
runs a `glob.glob(".claude/**/*.md", ..., recursive=True)`-shaped oracle over the live repo,
which would in principle re-walk each worktree's own nested `.claude/` tree. Measured: that
subtree is 16 files at 0 worktrees; even at 5 live worktrees the multiplied walk is
sub-second (`.claude/**/*.md`, not the ~2,420-file docs corpus). Not touched — no measurable
cost, and the contract's witness (10% delta on the 2-vs-5 wall-clock) does not require it.

Every other `rglob`/`os.walk` call site with a `tmp_path`/fixture root (the large majority —
`test_ship_gate.py`, `test_scan_undeclared_edges.py`, `test_gen_dashboard.py`,
`test_preflight_contract.py`, `test_desired_state_report.py`, and others) operates on an
isolated tmp directory, not the live repo tree, and is unaffected by live worktree count
regardless.

## Provisioning and teardown (no leftovers)

Per Done-clause 1, this codespace clone starts with `.claude/worktrees/` untracked and
empty, so the operator's declared floor of 2 was PROVISIONED rather than found:
`git worktree add .claude/worktrees/h0-measure-{1,2}` on new branches
`worktree-h0-measure-{1,2}` (closed-enum `worktree-` prefix), then 3 more
(`h0-measure-{3,4,5}`) to reach 5 for the re-measurement. All 5 were removed
(`git worktree remove --force` + `git branch -D`) once measurement was complete; the
now-empty `.claude/worktrees/` directory itself (this lane's own scratch, not tracked) was
also removed. `git worktree list` shows only the primary; `git branch -a` carries no
`worktree-h0-measure-*` remnant; `git status --short` was clean before this artifact's own
add.

## Open items

- The broader [#528] lane-latency task is untouched by this lane — it covers gate-run
  call-site `-n auto`/`--dist worksteal` adoption and telemetry emission, neither of which
  this lane's footprint (two test files) reaches.
- `pytest`'s reliance on the undocumented default `norecursedirs` pattern `.*` to keep
  `.claude` (and therefore `.claude/worktrees`) out of node collection is not itself pinned
  anywhere in this repo's own `pyproject.toml`. It works today; a future explicit
  `norecursedirs`/`testpaths` override that omitted the `.*` default would silently
  reintroduce the class of defect this lane closes for the two named walkers, without
  touching them. Flagged, not fixed — the contract's Done-clause 2 asks only that whatever
  walks `.claude/worktrees` today be named and excluded, and pytest's own collector does not.

`SKIP=audit-index-freshness` on this commit (declared, single-hook bypass): regenerating
`docs/audits/README.md` is the integrator's act at merge (contract "What NOT to do" — no
index regeneration in a lane), not this commit's.
