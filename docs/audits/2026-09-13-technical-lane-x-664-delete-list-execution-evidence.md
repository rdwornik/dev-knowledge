# Lane `lane-x-664-delete-list-execution` — delete-list execution evidence log

> Working evidence artifact for `LANE-x-664-delete-list-execution.md`, the execution of the
> ratified `[#664]` DELETE / TRIGGER / KEEP list
> (`docs/audits/2026-09-13-census-x-664-delete-list.md`). Appended to across the lane's steps;
> the final section is the end-of-lane artifact. Tool output is recorded verbatim, never
> narrated.
>
> Governance consumers: `[#664]` (the owning row and the census), `[#694]` (owner of the
> telemetry disposition), `[#655]` (owner of `run_retention()` has no production caller),
> `ADR-89` (the oracle's declared static-only limit), `ADR-110` (the lane protocol),
> `intake #86` (the census fixture).

## Step 0 — the lane's base moved, and one done-contract item was already discharged

The worktree was provisioned at `dbac84b8`. `main` had moved to `c0e0722f` (the
`docs/batch-x3-close-packet` merge) while this lane booted, and `journal_spine_anchor` refused
the first commit on the classic tree-lag shape — the check reads the JOURNAL from the committing
tree and the spine from the shared `main` ref. The discriminator was run before any remedy, as
the check's own diagnostic prescribes:

```
introduced: ['c0e0722f664907bf3abc9408ecf01cd2b261ccb6', '54c759854173e722dd16ca2288aa3487c5b1d220', 'e07615759c5693577fec9f1a50194ac06e790a51']
anchored in this tree: False
anchored at main: True
```

False here with True at main is tree lag, not a gap on main, so `git merge origin/main` is the
recorded fix rather than a guess. It fast-forwarded (the lane had no commits of its own yet), so
**this lane's base is `c0e0722f`, not `dbac84b8`** — and the paired-run baseline is re-taken
there rather than at the provisioned SHA. A baseline at a pre-sync commit would charge this lane
for `main`'s own deltas, which is the one thing the pairing exists to prevent. Both readings are
recorded in Step 2.

### DONE-CONTRACT ITEM 7 IS ALREADY DISCHARGED, BY MAIN, NOT BY THIS LANE

The sync brought in a four-line deletion in `scripts/graph_queries.py`:

```
-    "scripts/worktree_seed.py": Disposition(
-        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
-               "(.claude/commands/lane-boot.md:124)",
-        owner="operator -- one of the census's seven acts"),
```

That is done-contract item 7 verbatim — *"`scripts/worktree_seed.py`'s `ORPHAN_DISPOSITIONS`
entry DELETED — the MODULE STAYS"* — and its stated acceptance,
`tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`,
is green on the synced base:

```
uv run --locked python -m pytest tests/test_graph_spine.py -x -q -p no:randomly -n 0
37 passed in 34.11s
```

The same test is in the `dbac84b8` baseline's FAILED list (Step 2), with the exact subject the
contract names: `['scripts/worktree_seed.py']`. So the premise *"two prior lanes declined this
one-line edit … the operator has now ruled it … make the edit"* is **refuted by having been
satisfied**, between the freeze and this run.

**This is a PAUSE-class fact under Q10, and it is DISCLOSED rather than paused on**, because
AX27-1 forbids a wave-4 lane waiting on the operator mid-run and the refutation is
work-eliminating rather than work-blocking: re-making an edit that is already on `main` would
either be a no-op or a conflict, and neither is an act. Step 9 therefore carries only the
`cost_usage_telemetry.py` half of its two-part item. Nothing was reverted, re-applied or
re-litigated.

## Step 1 — the oracle is PROVISIONED, and it is RUN before any deletion

### Precondition: the pinned langserver was vendored

`npm install`, verbatim:

```
added 1 package, and audited 2 packages in 57s

found 0 vulnerabilities
```

`node_modules/pyright/langserver.index.js` present afterwards. `package.json`'s sole declared
dependency is `pyright@1.1.410` and `package-lock.json` is committed, so this restores a
**declared, pinned, checked-in** dependency. `node_modules/` is gitignored (`.gitignore:124`)
and stays out of this lane's commits.

**This was the lane's own precondition, not an inherited state.** The census records
(`2026-09-13-census-x-664-delete-list.md:26-28`) that *"No DELETE row below carries a
`safe_remove` verdict"* because the oracle *"returned `oracle-unavailable` for all nine
candidates tried"*. **That no longer reproduces.** Every run below returned a resolved
verdict; `oracle-unavailable` did not recur once. The census's gap was a provisioning gap on
the box, exactly as it said it was.

### A note on the transcription of the verdicts below

The verdicts are recorded as the tool emitted them. One correction of the CAPTURE, not of the
output: the Windows console renders this repo's em dash (U+2014) as a replacement character
under cp1252, so the `reason:` lines below carry the em dash the source actually emits
(`scripts/safe_remove.py:307`), not the console's mangling of it. Nothing else is altered.

### Run 1 — `scripts/gen_trend_dashboard.py`

```
safe-removal verdict: REVIEW
removal set: scripts/gen_trend_dashboard.py
reason: 2 bare-stem string-literal hit(s) for gen_trend_dashboard — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_gen_trend_dashboard.py:49
- tests/test_trend_dashboard.py:48

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 2 — `scripts/gen_north_star.py`

```
safe-removal verdict: SAFE
removal set: scripts/gen_north_star.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 3 — `scripts/window_metrics.py`

```
safe-removal verdict: REVIEW
removal set: scripts/window_metrics.py
reason: 1 bare-stem string-literal hit(s) for window_metrics — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_window_metrics.py:31

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 4 — `scripts/failed_set.py`

```
safe-removal verdict: SAFE
removal set: scripts/failed_set.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 5 — `scripts/nopack_sandbox.py`

```
safe-removal verdict: SAFE
removal set: scripts/nopack_sandbox.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 6 — `scripts/trace_writer.py`

```
safe-removal verdict: REVIEW
removal set: scripts/trace_writer.py
reason: 1 bare-stem string-literal hit(s) for trace_writer — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_trace_writer.py:14

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

### Run 7 — all six as ONE removal set, which is the shape the lane actually performs

Recorded because six single-module runs answer a question the lane does not ask. The deletions
land as a set, and two of the six are reachable only from another member of it — so a per-module
verdict is systematically more pessimistic than the act.

```
safe-removal verdict: REVIEW
removal set: scripts/failed_set.py, scripts/gen_north_star.py, scripts/gen_trend_dashboard.py, scripts/nopack_sandbox.py, scripts/trace_writer.py, scripts/window_metrics.py
reason: 4 bare-stem string-literal hit(s) for failed_set, gen_north_star, gen_trend_dashboard, nopack_sandbox, trace_writer, window_metrics — a possible dynamic/string-keyed reference the oracle cannot see (static-Python-only limit); downgraded from SAFE, human review needed before removing

bare-stem string-literal hits (downgraded from SAFE; WARN + allow):
- tests/test_gen_trend_dashboard.py:49
- tests/test_trend_dashboard.py:48
- tests/test_trace_writer.py:14
- tests/test_window_metrics.py:31

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**Zero surviving referrers across the whole set.** No `unsafe` verdict, no `unverifiable` entry,
and no `oracle-unavailable` — the set run reaches the same answer the six single runs did, by the
same route. The four REVIEW hits are the same four already accounted for above, each in a test
file that is co-removed with its module.

### What the oracle did NOT see, and this is the item that matters

**`gen_north_star.py` verdicts SAFE, and it has a live in-repo importer.**
`scripts/gen_trend_dashboard.py:113-117` loads it through
`importlib.util.spec_from_file_location(..., Path(__file__).resolve().with_name("gen_north_star.py"))`
and reads `_north_star.ARCS` at `:900`. That is not an `import` statement, so Pyright's
`references()` never sees it — **the exact false-PASS class ADR-89 declares and
`scripts/desired_state_loader.py` is this repo's worked example of.**

The bare-stem literal scan did not downgrade it to REVIEW either, and the reason is worth
writing down rather than leaving to be rediscovered: the scan looks for the module's **bare
stem** inside a quoted literal, and the only literal here is `"gen_north_star.py"` — the stem
**plus the extension**. A dynamic loader that names a sibling by filename is the most natural
spelling of this edge, and it is the spelling the REVIEW downgrade misses. Recorded as a
finding against `safe_remove._bare_stem_literal_hits`, owned by `[#195]`/`ADR-89`, not repaired
here: widening that scan changes what a removal gate says across the whole repo, which is not
this lane's footprint.

**It does not change what this lane does.** The census already ordered
`gen_north_star.py` deleted **after** `gen_trend_dashboard.py` for exactly this edge, so the
importer dies with the import. The ordering was ruled from the FPG-1 graph, which sees the edge
the oracle cannot — and this run is the measurement that says the graph, not the oracle, is what
made that ordering safe.

Same shape, one level weaker, for `failed_set.py`: SAFE individually, and its recorded referrer
`window_metrics.py:359` is prose in an f-string rather than an import. There is no code edge to
break in either direction; the ordering is still honoured, because the ratified order is
immutable and a lane does not relitigate it on a measurement that agrees with it.

### The verdict-vs-act ledger

| module | verdict | what the verdict is downgraded by | deleted at step |
|---|---|---|---|
| `scripts/gen_trend_dashboard.py` | REVIEW | its own two dedicated test files | 3 (first) |
| `scripts/gen_north_star.py` | SAFE (a FALSE PASS on the importlib edge, see above) | — | 3 (second) |
| `scripts/window_metrics.py` | REVIEW | its own dedicated test file | 4 (first) |
| `scripts/failed_set.py` | SAFE | — | 4 (second) |
| `scripts/nopack_sandbox.py` | SAFE | — | 5 |
| `scripts/trace_writer.py` | REVIEW | its own dedicated test file | 5 |

Every REVIEW downgrade is a hit in the module's **own dedicated test file**, which is co-removed
with the module. That is the `[#734]` precedent's rule, not a new one: *"DELETED with their
dedicated tests and their `ORPHAN_DISPOSITIONS` entries"*. A REVIEW whose only hit is a test that
leaves in the same commit is not a surviving reference.

**No verdict is treated as a licence.** Done-contract item 2 binds: a SAFE verdict is necessary
and not sufficient, and the paired baseline/tip Actions run in Step 2 / Step 6 is what carries
the weight the oracle cannot.
