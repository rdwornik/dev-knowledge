# CLOUD-3 — `[#566]`: the accepted `[#488]` axis LEAN, built

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-22 · **Slug:** cloud-3-566-axis-lean
- **Lane:** CLOUD-3 (Anthropic cloud session, branch `claude/cloud-3-566-axis-lean`), MUTATING · base `main` @ `0360d6d`.
- **Row built:** `[#566]` — *Constraint-contention tiebreak — implement the accepted `[#488]` LEAN*.
  The axis was **ruled** by the architect on 2026-08-20; this lane builds it and does **not** relitigate scope.
- **Ruling input:** `docs/audits/2026-08-19-technical-c4-ruling-prework.md` §2.5 (the six-axis measurement).
- **Footprint:** `scripts/gen_task_tree.py`, `tests/test_gen_task_tree.py`, this artifact, `docs/audits/README.md` (regenerated).
  No `tasks/`, no `BACKLOG.md`, no `protocols/`, no `.pre-commit-config.yaml`. One shared-file need ships as a fenced diff in §7.

---

## 1. What was built

One read-only CLI verb on the existing generator, plus the four pure functions behind it.

```
python scripts/gen_task_tree.py --rank [--rank-top N]
```

The ordering key, primary first — exactly the LEAN's three layers:

```
1. [P1..P3]            the hand-set priority. PRIMARY, unchanged, never overridden.
2. constraint-contention  (open rows sharing this row's serialize-group) - 1;  0 when ungrouped.
                          Breaks ties WITHIN a P tier. Higher contention ranks first.
3. id                  monotonic, ledger-backed age proxy. Breaks what remains. Lower id first.
```

New public surface in `scripts/gen_task_tree.py`:

```
open_task_rows(rows)        the ranked population: rows whose line carries no `· DEFER`
contention_scores(rows)     id -> contention, counted over the population passed in
rank_key(task, contention)  (P-enum, -contention, id) — a TOTAL order (ids are unique)
rank_tasks(rows)            -> list[RankedTask]  (rank, id, priority, serialize_group, contention, title)
render_ranking(ranked, top) flat, un-padded report text
_cmd_rank(out_dir, top)     the CLI verb: reads the SOURCE tree, prints, writes nothing
```

**Live output on today's tree** (190 open rows, exit 0, zero bytes changed):

```
gen_task_tree: 190 open task(s) ranked — key: [P1..P3] primary · constraint-contention over serialize-group as the tiebreak within a tier · id (age proxy) as the floor
gen_task_tree: contention measures THROUGHPUT, not value — it orders a tie block, it never overrides a hand-set P.
1. [#519] P1 · contention 16 · group architecture · The close path is two edits, and nothing makes a half-done close visible
2. [#359] P1 · contention 10 · group handoff · PHANTOM ENFORCEMENT — HANDOFF_PROCESS.md §14a FILE-BOUNDARY claims a mechanism that does not exist.
3. [#528] P1 · contention 7 · group environment · Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost
4. [#529] P1 · contention 7 · group environment · Telemetry v1 EMIT — stage-1 events from the gate mesh
5. [#565] P1 · contention 7 · group environment · run_id in telemetry emit — sequenced before the read-path build lane
6. [#514] P1 · contention 0 · group none · Two rival LANE_BRANCH_RE constants ship in one repo
7. [#555] P1 · contention 0 · group none · Closing campaign batch 1 + kill-candidates instrument
8. [#153] P2 · contention 41 · group audit-py · Enforcement-completeness pass
…
gen_task_tree: 24 deferred row(s) excluded (· DEFER)
```

## 2. What `[#488]` consumers gain — measured, not asserted

`[#488]`'s complaint is that *"the backlog has no ranking function beyond a hand-set `[P1..P3]`"*. Measured on the
live tree at `0360d6d` (190 open rows in the manifest, 24 deferred and excluded):

```
before — [P1..P3] alone      3 ordered buckets over 190 rows
                             largest tie block: 103 rows (P2).  P3: 80.  P1: 7.
                             two P2 rows are not ordered against each other AT ALL.
after  — P + contention     21 ordered buckets
                             largest tie block: 37 rows (P3 · contention 0) — a 64% cut
after  — P + contention + id  190 buckets — a TOTAL order. No pair is unordered.
```

Concretely, four things a consumer can do today that it could not on 2026-08-21:

1. **Pick the next row inside a 103-way tie deterministically.** The P2 tier was one undifferentiated block; it now
   opens with the 42-member `audit-py` group at contention 41, then `architecture` at 16, `settings-json` at 13,
   `handoff` at 10, and ends at the 32 ungrouped P2 rows scoring 0.
2. **See what the queue is actually serialized on before dispatch.** Contention is the same quantity the batch
   protocol's pre-dispatch matrix reasons about — 119 of 190 open rows carry a `serialize-group`, across 11 groups
   (`audit-py` 42 · `architecture` 17 · `settings-json` 14 · `handoff` 11 · `playbook` 8 · `environment` 8 ·
   `claude-md` 5 · `pre-commit-config` 4 · `gates` 4 · `codex-review` 4 · `coherence` 2). The prework records that
   this axis is *the only one of the six that would have predicted the batch-6 dispatch refusal before it happened*.
3. **Get an age ordering for free inside a contention tie.** No `created:` field, no backfill: the id ledger already
   refuses re-issue, so the age proxy is tamper-evident by an existing gate rather than by a new one.
4. **Pay nothing recurring for any of it.** Every input is derived from a task's own body line, which
   `gen_task_tree` already parses. Zero new authored fields, zero estimates, zero backfill.

**What it does NOT buy, stated as plainly as the gain:** contention ranks *throughput*, not *value*. A row can
unblock forty others and still matter less than one that unblocks none — which is precisely why the LEAN layers it
*under* the hand-set P rather than in place of it. The axis also cannot tell the operator that a P3 is actually
urgent; that remains a judgement, and the P field remains where it is recorded.

## 3. What was deliberately NOT built

- **No new authored field** — the `[#566]` done-clause requires it, and it is the property the LEAN was selected for.
  WSJF would have needed 732 recurring estimates across 183 open rows; RICE 3 fields with a `Reach` term that is
  meaningless at n=1 operator; both are foreclosed by the ruling and are **not re-costed here**.
- **No graph-centrality build** — inert on a 3-edge population (`blocks:` does not exist as a field). The prework
  reframes it as a prose-mention attention measure or a drop; neither is this row's scope.
- **No reordering of `BACKLOG.md`.** Document order is carried by `tasks/manifest.json` and is the operator's
  narrative structure (themes, stories, prose) that the byte-exact reassembly contract depends on. Ranking is a
  report *over* the queue, not a rewrite *of* it.
- **No `rank:` in task frontmatter.** A rank is not a property of a row: it changes when a *different* row is filed
  or closed, so materialising it would churn every file in a group on every unrelated edit and hand the freshness
  gates a permanent diff. `--rank` computes it on demand instead.
- **No wiring into `audit.py`, no hook, no gate.** A ranking is advice; it has no pass/fail semantics, and this repo
  does not arm organs that cannot refuse anything.

## 4. Design decisions a reader would otherwise have to reverse-engineer

- **Deferred rows are excluded, and are not counted as contending.** A `· DEFER` row is out of the queue by operator
  decision; ranking it would put a row nobody may pick up ahead of one they may, and counting it would inflate a
  mostly-deferred group's members. 24 rows are excluded today.
- **Contention is `(group size − 1)`, over the OPEN population only.** This reproduces the prework's measured
  41-for-`audit-py`. Honest limit, stated at the function that computes it: `(size − 1)` is what the group *contends
  over*, which equals what a completion *frees* only for the row that dissolves or shrinks the group; a row that
  merely shares the file scores the same.
- **`--rank` reads `tasks/`, not `BACKLOG.md`.** Post-flip the tree is the source of truth; ranking the derived file
  would rank a copy `--check` might already be calling stale.
- **A structural problem is reported, never raised.** A report must not traceback on a tree `--check` would simply
  RED, so `_cmd_rank` returns 1 with a `rank FAIL … nothing written` line.
- **A row with no `[P#]` sorts after every P3** rather than defaulting into P1. `validate_backlog.py` already pins the
  enum to P1–P3, so this is a defensive floor, not an expected state.
- **Report text is flat and cp1252-encodable.** No column padding (the output-formatting rule), and every non-ASCII
  glyph used (`—`, `·`, `…`) encodes on a cp1252 console — the `[#470]`/`[#486]` crash class is not repeated.

## 5. Tests — 10 added, all green

`tests/test_gen_task_tree.py` (83 tests in the module, 83 pass):

```
test_rank_pins_the_ordering_of_a_seeded_tie_block          THE done-clause acceptance test
test_rank_priority_stays_the_primary_key                   a 40-member group never lifts a P3 over a P1
test_contention_is_group_size_minus_one_and_zero_when_ungrouped   the 41-vs-0 prework shape
test_rank_excludes_deferred_rows_and_scores_contention_over_the_open_ones
test_rank_sorts_an_unprioritized_row_after_every_p3
test_rank_cli_reads_the_source_tree_and_writes_nothing     exit 0, zero bytes changed
test_rank_top_truncates_and_says_how_many_it_hid           a truncated report never reads as the whole queue
test_rank_top_is_guarded_by_the_cli                        --rank-top alone, and --rank-top 0, both exit 2
test_rank_reports_rather_than_crashes_on_a_broken_tree     rc 1, not a traceback
test_rank_reports_the_live_queue                           the committed tree ranks, P key never violated
```

The seeded tie block is built so each of the three keys decides a step of it and none is redundant: a P1 with zero
contention outranks a 3-contention P2 (key 1); `#21/#22/#23` tie at P2 and separate only on contention (key 2);
`#30/#31` tie at P2 *and* at contention 1 and separate only on id (key 3). The expected order is pinned literally.

## 6. Gates run — and the two environment caveats, declared

**uv-pin caveat (the R4 precedent).** This container carries `uv 0.8.17`; `pyproject.toml` pins
`required-version = "==0.11.19"`, so every `uv run --locked …` hook entry refuses before doing anything:

```
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

Every applicable gate was therefore run **by hand as `python3` / the PATH binaries**, and that is declared here
rather than implied.

**Second caveat, and it is why the suite total is not a clean number.** The container's interpreter is missing
third-party runtime deps (`click`, `markdown_it`, `pandas`), so 87 test-module collections error and 105 tests fail
**before any of this lane's code is reached**. That is a pre-existing environment condition, not a regression, and
it was *proved* rather than asserted:

```
pytest -q --tb=no -o addopts="" -p no:cacheprovider --continue-on-collection-errors
  with this change:     191 FAILED/ERROR lines · 1029 passed · 10 skipped
  stashed (clean main): 191 FAILED/ERROR lines · identical set (diff → empty)
```

The two failure sets are **byte-identical**, so this change introduces zero new failures.

```
pytest tests/test_gen_task_tree.py -x -q -o addopts=""   ->  83 passed          (the module, incl. the 10 new)
ruff check scripts/gen_task_tree.py tests/test_gen_task_tree.py  ->  All checks passed!  (ruff 0.15.8)
python3 scripts/gen_task_tree.py --check                  ->  check ok           (tree ⇄ BACKLOG.md coherent)
python3 scripts/gen_task_tree.py --rank                   ->  exit 0, 190 ranked, tree byte-unchanged
python3 scripts/gen_audit_index.py --check                ->  green after the regen committed here
```

```
python3 -m scripts.codemap.cli check . --source-root scripts  ->  clean (orphan-module warning only)
python3 scripts/validate_hermetization.py                     ->  rc 0 on the staged add (ADR-101 R3 name grammar)
```

`-o addopts=""` is required because `addopts = "-n auto"` needs `pytest-xdist`, absent here. Spine-walking
instruments (`validate_git_backlog` and kin) were **skipped by the brief's shallow guard** — this clone is shallow.
`audit.py health`, `validate_doc_claims` and `gen_doc_counts.py` could not run at all: all three import `click`.

**One known WARN this lane LEAVES for the integrator, deliberately rather than by omission.**
`ecosystem/doc-counts.md:16` claims `- tests: **3372 collected**`; these 10 new tests make the live number 3382, so
`doc_claims` will carry a `pytest_collected` drift WARN (WARN, not FAIL — it does not block a commit). It is **not**
regenerated here because it *cannot honestly be*: this container collects only 1160 of the suite (70 modules error on
the missing deps above), so running `gen_doc_counts.py --write` would replace a correct number with a badly wrong
one — and the file is generated, so hand-typing 3382 would be asserting a figure nothing here can verify. The
one-line clearance on a full environment is `python scripts/gen_doc_counts.py --write`.

## 7. Terra review — severity tally

A full adversarial review pass was run at high effort over this lane's diff, plus the behaviour-changing code in the
branch range.

```
THIS LANE'S DIFF (scripts/gen_task_tree.py + tests):   0 findings.  Critical 0 · High 0 · Medium 0 · Low 0
```

Verified by the reviewer, item by item: the `(P-enum, −contention, id)` key matches the seeded tie block by hand
calculation; contention is counted over the filtered open population as documented; `_UNPRIORITIZED_RANK` cannot
silently demote a valid priority (the enum is pinned to P1–P3 by `validate_backlog.py`); `_cmd_rank`'s except clause
covers everything `reassemble_from_tree`/`parse_backlog` can raise (`json.JSONDecodeError` and `FileNotFoundError`
included); the report's glyphs are cp1252-safe.

**Nothing to fix at Critical or High in this lane's code.** The pass did surface four findings in code this lane did
not touch (already on `main`, owned by other rows). They are recorded here rather than swept in — widening a lane
into another row's footprint is the failure mode the batch protocol exists to prevent:

```
OUT-OF-LANE (carried, not fixed here):  High 1 · Medium 3
High    scripts/single_flight.py:731  the lease-rejected branch of `release` calls `_not_ours(owner=None)`,
                                      printing "it carries no run_id" about a lock it never read — which steers
                                      the operator to the unguarded `ESCAPE: git push <remote> :<ref>` printed
                                      below, deleting a LIVE sibling's lock. `_remote_lock_token` is reachable
                                      there.  Owner: [#530].
Medium  scripts/single_flight.py:325  `_not_ours` prints its per-claim ownership TOKEN as "belongs to run
                                      {owner[:8]}" — an id matching nothing in the telemetry store, plus 8 bytes
                                      of another run's capability. `_lock_run_id` is never called on that path.
                                      Owner: [#530]/[#565].
Medium  .pre-commit-config.yaml:167   `lane-contract-check` omits `pass_filenames: false`; pre-commit's default
                                      passes ALL matched files, while `gen_lane_contract.py check` declares
                                      exactly one `click.argument("path")` — staging two `LANE-*.md` files fails
                                      the hook with "Got unexpected extra argument". Latent today only because
                                      zero tracked files match the glob (the arms-clean state CLAUDE.md v2.63
                                      records).  VERIFIED against both files.  Fix below.  Owner: [#539].
Medium  scripts/gen_lane_contract.py:467  `is_cloud = CLOUD_SECTION in sections` is an EXACT match while every
                                      other mandatory section is prefix-matched to allow a trailing qualifier,
                                      so `## Receipt gate (Q5)` reads as a local lane and the Q5 conjunction is
                                      silently skipped (or falsely fails under `--cloud`).  Owner: [#539].
```

`.pre-commit-config.yaml` is a **reserved shared file** for this lane, so its fix ships as a fenced proposed diff —
the same discipline `[#539]` itself used when it shipped the hook:

```diff
--- a/.pre-commit-config.yaml
+++ b/.pre-commit-config.yaml
@@
         entry: uv run --locked python scripts/gen_lane_contract.py check
         language: system
         files: '(^|/)LANE-[^/]*\.md$'
+        # pre-commit's default hands the entry EVERY matched staged file at once, but
+        # `gen_lane_contract.py check` declares exactly one `click.argument("path")`:
+        # staging two LANE-*.md files fails with "Got unexpected extra argument".
+        # Latent only because zero tracked files match the glob today.
+        require_serial: true
+        pass_filenames: true
```

`pass_filenames: true` is already the default, so the one-line behavioural change is **not** enough on its own — the
durable fix is to make `check` accept `nargs=-1` paths in `gen_lane_contract.py` (owner `[#539]`); the diff above is
the config-side half and is offered as an interim narrowing, not as a claimed cure. Recorded so `[#539]`'s owner
inherits the whole picture rather than a partial patch.

## 8. Done-contract, item by item

`[#566]`'s own done-clause, each leg against what shipped:

```
"the ranking is computed by the existing generator"           gen_task_tree.py --rank  ✔
"from serialize-group"                                        contention_scores()      ✔
"with no new authored field"                                  every input derived from the task body line ✔
"[P1..P3] remains the primary key"                            rank_key element 0; test_rank_priority_stays_the_primary_key ✔
"the contention count breaks ties within a tier"              rank_key element 1; 103-row tie block -> 37 ✔
"P-enum + age breaks what remains"                            rank_key element 2 (id); total order over 190 rows ✔
"a test pins the ordering of a seeded tie block"              test_rank_pins_the_ordering_of_a_seeded_tie_block ✔
```

Brief legs: artifact in `docs/audits/` on the ADR-101 grammar ✔ · `docs/audits/README.md` regenerated in the same
commit ✔ · no reserved-file edits (one fenced diff instead) ✔ · shallow guard honoured ✔ · uv-pin caveat declared ✔ ·
terra tally in the artifact ✔ · tests green ✔.

**STATUS: CLEAR.** Committed on `claude/cloud-3-566-axis-lean`; not merged, not pushed to `main`.
