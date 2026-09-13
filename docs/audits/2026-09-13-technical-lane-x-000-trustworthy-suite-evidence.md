# lane-x-000-trustworthy-suite — evidence

**Date:** 2026-09-13 · **Lane:** `lane-x-000-trustworthy-suite` ·
**Branch:** `worktree-lane-x-000-trustworthy-suite` ·
**Contract:** `LANE-x-000-trustworthy-suite.md` (frozen) · **Mode:** execute · **Budget:** V-2

Three defects that made this suite report things about itself that were not true. Each was
reproduced RED before any fix existed, and each fix is measured rather than argued. The
dependency behind the seventeen failures is **pandas**, named rather than described, as the
contract's step 1 asks.

## The commits

```
84ce7976  test(suite): RED-first witnesses for the three defects that make the suite lie
5973acba  fix(graph-store): publish a rebuild through the live file, not over readers
9c4e5a91  fix(gen-handoff): load a target repo's audit in isolation, not into sys.modules
ab6e4f00  test(fleet-analytics): declare the pandas requirement instead of erroring 17 times
```

Plus two SYNC merges (`5b363a2e`, `c6158662`) — see "What blocked the lane" below.

## Defect 1 — the store a sibling worker could break

**Cause.** `graph_store.rebuild` published by `os.replace(tmp, path)`. On Windows that FAILS
while any process holds the destination or its `-wal`, so `_swap_into_place` retried 20 times
(~5 s) and raised `StoreUnreadable`. Under `-n auto` every worker shares ONE store — it is
keyed to the TREE and the workers are all in the same tree — so a handle held open in worker A
made worker B's `ensure()` raise, **inside B's own tests, naming a file B never touched**. Six
witnesses in `tests/test_graph_spine.py` bound `gs.ensure(REPO_ROOT)` and never closed it,
which turned any worker that ran one into a permanent reader for the rest of the session.

**Fix.** Stop fighting WAL. The module's own pragma comment already quotes the guarantee that
makes the swap unnecessary — *"readers do not block writers and a writer does not block
readers"*. A rebuild now writes THROUGH the live file inside ONE transaction (`_write_graph`).
Atomicity comes from the transaction, which is strictly better than what it replaces: an
interrupted transaction rolls back on next open, where an interrupted temp-file build left a
temp file behind. `_swap_into_place` is kept and NARROWED to the one case an in-place
transaction cannot serve — a destination that is not a database at all. The six leaked readers
now take a function-scoped `live_store` fixture that closes in a `finally`.

**Two facts measured before being relied on:**

| Question | Answer | Consequence |
|---|---|---|
| Does a WAL `COMMIT` move the main file's mtime? | **No** — byte-identical across a commit that changed the contents | `is_stale` reads exactly that mtime, so `os.utime` after commit is REQUIRED. Without it the store reads stale forever and every `ensure()` pays a full ~13 s build — a silent performance cliff, not a failure, so nothing would have caught it |
| Does an in-place transactional rewrite succeed with a `mode=ro` reader held open? | **Yes** | the property the whole change rests on |

**Evidence.**

```
paired, same tree, same witness:
  old publication path  ->  StoreUnreadable ... after 20 attempts ([WinError 32] ... FPG.db-wal)
  new publication path  ->  passes

four workers racing a DELIBERATELY backdated live store:
  pytest tests/test_graph_spine.py -n 4   ->  36 passed, 0 StoreUnreadable
```

## Defect 2 — the stub that shadowed everything collected after it

**Cause.** `gen_handoff.collect_hints` did `sys.path.insert(0, repo_root/"scripts")` then
`import audit`, undoing neither half. With the test stub repo as `repo_root`, its one-line
`scripts/audit.py` (`ALL_CHECKS = []`) became `sys.modules["audit"]` and that directory stayed
FIRST on `sys.path` for the rest of the process.

**Why it survived.** The damage lands in whatever is collected NEXT, never in the file that
causes it — so re-running the victim alone "proves" the victim is fine.

**The path half is the wider one.** That stub directory also carries one-line placeholders for
`validate_backlog`, `validate_doc_claims`, `validate_git_backlog` and `gen_task_tree`. A later
import of any of those resolved to a module with nothing in it — which does not fail, it
**passes vacuously**.

**Fix.** `_load_target_audit` loads the target's `audit.py` through an explicit spec under a
private name — never `"audit"` — restoring `sys.path` and dropping every module name the exec
introduced. A third witness pins the other direction: isolation must not be bought by
reporting the HUB's check count for a repo that declared its own.

**Evidence.**

```
pytest tests/test_gen_handoff.py tests/test_residual_completeness.py -n 0
  BEFORE:  8 failed, 110 passed   <- 3 in the SECOND file:
                                     module 'audit' has no attribute '_vrc'
  AFTER:   5 failed, 116 passed   <- those 3 are gone
pytest tests/test_residual_completeness.py -n 0  ->  29 passed, both ways
```

## Defect 3 — the dependency decision

**The dependency is `pandas`.** `scripts/fleet_analytics.py` imports it INSIDE the three frame
builders and the digest renderer, so the module collects cleanly without it and fails
seventeen witnesses at CALL time.

**The second limb of clause 3 was taken — skip BY DECLARATION — and that is a ruling this lane
declines to overturn rather than a preference.** pandas is ALREADY declared, in the opt-in
`analytics` group, and `pyproject.toml` states the reason in its own words: the L5a lane is
HUB-ONLY, *"so a consumer never needs it"*. A plain `uv sync --locked` is therefore CORRECT not
to install it. Moving pandas into the default `dev` group would overturn that recorded stance
and pull pandas + numpy into every consumer's default sync to serve a lane none of them run.
What was missing was the declaration on the TEST side: the seventeen **erred** where they
should have **skipped**.

**Evidence.**

```
uv run --locked pytest tests/test_fleet_analytics.py -n 0
  BEFORE:  17 failed, 47 passed   (every failure ModuleNotFoundError: pandas)
  AFTER:   49 passed, 17 skipped
```

The skip reason names the package, the group, why the group is opt-in, and the exact command
(`uv sync --locked --group analytics`). Verified rendered with `pytest -rs`, not assumed.

**Honest limit.** This makes the seventeen SKIP, not pass. Their subject stays unexercised in a
default environment, and a skip is a declared absence of evidence, not evidence.

## Final targeted run

TARGETED only — this lane ran no full local suite (`[#528]`; the full suite runs once, at
integration).

```
pytest tests/test_graph_spine.py tests/test_gen_handoff.py tests/test_fleet_analytics.py \
       tests/test_residual_completeness.py tests/test_decision_coverage.py \
       tests/test_deny_and_point.py -n 4          (live store deliberately backdated first)

  389 passed, 17 skipped, 6 failed   in 188.65s
```

## The 6 failures are PRE-EXISTING and are not absorbed

Neither set is in this lane's contract, and both are proved rather than asserted.

**1 — `test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`.**
`scripts/worktree_seed.py` is a dispositioned orphan that is now genuinely triggered:
`file_purpose_graph.py why` names two wiring consumers — `gen_lane_contract.py` imports it and
`.claude/settings.json` triggers it. The trigger landed in **f903a24f (2026-09-12)** and the
`ORPHAN_DISPOSITIONS` entry was already present at this lane's branch point **b154fd1a**, so
the test was RED ON ARRIVAL — before the sync merges and before any edit here. The fix is to
drop that row from the register, which is a **curated-baseline touch and outside this lane's
declared footprint**, so it is reported rather than taken (V-2 class (a)).

**5 — in `tests/test_gen_handoff.py`:** `test_dogfood_no_probe_row_carries_an_answer_value`
and `test_dogfood_generated_bundle_has_no_failing_probe` (`assert 15 == 13`),
`test_epic_bundle_has_no_failing_probe` (`assert 6 == 5`),
`test_suffixed_bundle_probes_resolve_against_their_own_directory`, and
`test_funnel_health_renders_no_unavailable_against_the_live_repo`. All five were measured on a
CLEAN tree at this lane's start, before any edit, in the same run that first exposed defect 2.

## What blocked the lane, and how it was discriminated

Two gates refused commits for reasons that were not this lane's work. Both were diagnosed with
the repo's own instruments before acting, rather than assumed.

**`journal_spine_anchor` — twice.** Other seats merged to `main` while this lane worked. The
check reads the JOURNAL from the COMMITTING tree and the spine from the shared ref, so a
lagging tree reports gaps that do not exist. Every named SHA answered `this_tree=False /
at_main=True` under the check's own diagnostic — the tree-lag reading, not a real gap. Resolved
by two sync merges.

> **One correction to the gate's own advice, recorded because it cost a step.** The refusal
> prescribes `git merge origin/main`. Here `origin/main` was already an **ancestor of this
> branch's HEAD** and LOCAL `main` was the ref that was ahead, so that command is a no-op and
> the sync target is local `main`. The prescribed command needs that one substitution whenever
> the integrator has committed locally without pushing.

**`decision-coverage`.** Refused on `to-cc/AMEND-BATCH-W-005.md`, a TRANSPORT decision in the
operator's prompts directory that no open row implemented. Not this lane's file and not in this
repo. The second sync merge cleared it — another lane had filed the implementing row on `main`.

**Declared single-hook bypass, on all four commits: `SKIP=doc-counts-pytest-freshness`.**
Step 1's seven new tests moved the collected-test claim in the GENERATED
`ecosystem/doc-counts.md` (file 6012 / actual 6019), and it stays moved until the index is
regenerated — which this lane's contract puts with the integrator, gate-of-record, once, at the
merge (Q1). Every other pre-commit, commit-msg and pre-push hook ran and passed on every
commit. **`--no-verify` was not used at any point.**

## For the integrator

1. Regenerate `ecosystem/doc-counts.md` at the merge — `gen_doc_counts.py --write`. The claim
   is 7 collected tests behind; that is the whole of the declared bypass.
2. `scripts/worktree_seed.py` needs removing from `graph_queries.ORPHAN_DISPOSITIONS` — a
   one-line curated-register edit this lane was not scoped to make. It REDs
   `tests/test_graph_spine.py` for anyone who runs it.
3. `lane-x-664-spine-armed` is serialised behind this lane (AX27-3) and may now enter. It
   touches the same persisted store: note that the publication path changed from file-swap to
   in-place transaction, and that `_swap_into_place` is now the corrupt-file fallback only.
