# lane-z-746-devcontainer-substrate — end-of-lane packet

> **Lane** `lane-z-746-devcontainer-substrate` · **branch** `worktree-lane-z-746-devcontainer-substrate`
> · **row** `[#746]` · **contract** `LANE-z-746-devcontainer-substrate.md` (frozen)
> · **date** 2026-09-15 · **seat** CC (Opus 5, background lane)
>
> What changed · the proposed diffs · the open items. Written at commit-and-STOP: nothing here
> is merged, and integration is the integrator's act from the primary checkout.

## 1. The number that moved, and the refusal that was witnessed

**Recovery containers: 1 → 0.** Both readings are live `creation.log`s, not inference.

BEFORE — `lane-z-substrate-probe`, created 2026-09-14 23:36Z off `-b main`:

```
23:36:59.301Z [provision] freshness: 'main' is behind origin/main by 1401 commit(s)
              - 1059d04d -> b5270d63
23:36:59.515Z [provision] freshness: OK - now at origin/main (b5270d63)
23:37:03.694Z .venv/bin/python3: can't open file
              '/workspaces/dev-knowledge/scripts/cloud_provisioning.py': [Errno 2]
23:37:03.718Z (again)
23:37:03.722Z [provision] REFUSED: B1 the history guard could not look (exit 2)
23:37:03.728Z postCreateCommand from devcontainer.json failed with exit code 1
23:37:03.758Z Container creation failed.
23:37:04.460Z Creating recovery container.
```

AFTER — `lane-z-746-proof`, created 2026-09-15 02:24Z off this lane's branch. Zero matches for
`Container creation failed` and `Creating recovery container` in the whole log:

```
02:25:42.792Z Outcome: success User: vscode WorkspaceFolder: /workspaces/dev-knowledge
02:25:43.911Z Running the onCreateCommand from devcontainer.json...
02:25:44.079Z [provision] L1 OK - uv 0.11.19 == pin 0.11.19
02:26:00.011Z [provision] L2 OK - full history (7630 commits reachable from HEAD)
02:26:05.606Z [provision] B1 OK - the refs every spine-walking instrument reads resolve,
              and the walk succeeds
02:26:43.523Z [provision] L5 OK - at least one repo is registered; audit.py health's
              operational block can pass here
02:26:58.354Z [provision] L-F1 ok - claude installed (2.1.272 (Claude Code))
02:26:58.893Z Running the postCreateCommand from devcontainer.json...
02:27:02.859Z Running the postStartCommand from devcontainer.json...
02:27:04.017Z [provision] gate OK - uv 0.11.19, full history + spine refs, ecosystem
              registered, three hook types armed, stamp current
02:27:05.434Z Finished configuring codespace.
```

Binaries, asked of the container directly:

```
/home/vscode/.local/bin/claude -> .../versions/2.1.272   ->  2.1.272 (Claude Code)
uv 0.11.19 (x86_64-unknown-linux-musl)
python3 3.12.11   (the IMAGE's interpreter, on PATH)
```

**Mark where that last one stops.** `python3 --version` on `PATH` reports the image's 3.12.11;
the project venv is 3.12.10, which is what `.python-version` pins and what provision.sh asserts
(`environment OK — Python 3.12.10`). The two are different facts and the log carries both.
`claude` is NOT on a non-login shell's `PATH` — it resolves through `~/.local/bin`, which a login
shell adds. Present, not reachable by every invocation shape.

**THE REFUSAL, WITNESSED — the legs were not softened to make the container build.** Run inside
the proof container, `/tmp/probe.py`:

```
C: L5 read-only with NOTHING registered   (state.yaml moved aside)
   [provision-legs] ERROR ecosystem: no repo registered - `audit.py health` reports
                    `repos registered (none)` and exits non-zero here
   exit=1                                  <- looked, and found drift
D: the GATE itself, full stack, same condition
   [provision] REFUSED: L4 no repo is registered under ecosystem/ - audit.py health
               cannot pass here; re-provision
   exit=1                                  <- the restored gate leg refusing a live container
E: registration restored
   [provision] gate OK - uv 0.11.19, full history + spine refs, ecosystem registered, ...
   exit=0
```

And the could-not-look half, which is the one the outage turned on:

```
A: --root /tmp/notarepo history
   could not look: git rev-parse --is-shallow-repository failed: fatal: not a git repository
   exit=2
B: --config /tmp/missing.yaml history
   could not look: provisioning declaration not found at /tmp/missing.yaml
   exit=2
```

provision.sh's `case` maps that `2` to `die "B1 the history guard could not look (exit 2) — an
unknown history state is not a clean one"`. **Unchanged from before the outage.** The fix was
never to make that refusal quieter.

## 2. What changed

| File | Change |
|---|---|
| `scripts/provision_legs.py` | **new**, 870 lines. The `history` (B1) and `ecosystem` (L5) commands of the retired `scripts/cloud_provisioning.py`, carried across from `3c9418cc^`. Its third command, `prebuild`, is deliberately absent. |
| `tests/test_provision_legs.py` | **new**, 75 cases. 72 carried verbatim from `tests/test_cloud_provisioning.py` at `3c9418cc^`; 3 new, covering this lane's own doc edits. |
| `.devcontainer/provision.sh` | `leg2b_history` / `leg5_ecosystem` restored; the two `gate()` asserts restored; **`refresh_source_tree` now hands over to a refreshed copy of itself**; `self_digest()` added; `PROVISION_ARGV` captured at file scope; docstring, usage and gate message corrected. |
| `tests/test_provision_sh.py` | 2 tests → 9. The `[#664]` invocation regex widened from one spelling to four; six new tests for the legs, the ordering and the hand-over; one that RUNS the real `self_digest` body. |
| `.devcontainer/provisioning.yaml` | Names its live reader. The `prebuild:` block is marked at its own head as a declaration of record with **no reader**. Its "makes the image's own age irrelevant" claim is amended in place with what was measured. |
| `.devcontainer/devcontainer.json` | The prebuild comment stops naming a checker that no longer runs, and records that editing THAT file is what refreshes the image under `trigger: on_configuration_change`. |
| `scripts/graph_queries.py` | One `ORPHAN_DISPOSITIONS` row for `scripts/provision_legs.py` — see §4, it is the most load-bearing edit in the lane. |
| `tasks/746-...md` | P2 → P1, the witnessed evidence, and a third Done-when clause for the hand-over. |

Commits, in contract order: `a7edeecf` (step 1) · `3abd8098` (step 2, seven RED) ·
`0dcdb153` (step 3) · this packet (steps 4–5). Plus two sync merges, `f1c27f33` and `7c65ceaf`
— §5.

## 3. The contract's step-2 premise was refuted in its MECHANISM

The frozen contract says *"the live creation.log proves TWO call sites survive and still invoke
the deleted file"*. **They do not survive.** `ec56b417` removed all six, it is an ancestor of
`b5270d63`, and the probe container's own on-disk `provision.sh` carried the post-`[#664]` file
(five prose mentions of the retired path, no `leg2b_history` function at all — checked live).

What survived is the **image snapshot**. The container booted a tree at `1059d04d`
(2026-09-01, 1401 commits behind, twelve days older than `3c9418cc`), `refresh_source_tree`
fast-forwarded the TREE to `b5270d63` mid-run, and the already-running `bash` went on executing
the stale body it had already read — straight into the call sites that no longer exist in the
tree it had just written to disk.

**The conclusion the contract drew is untouched; the cause is one layer down.** So the lane did
what the Done-contract required and added the cause: `provision.sh` mutates the very file it is
executing, so a fix landed in `main` could not take effect during the creation that needs it.
That is `[#746]`'s new Done-when clause 3 rather than a second row, because without it clauses 1
and 2 are not provable on a fresh container at all.

## 4. Open items — for the operator and the integrator

**O-1 · `WIRING_SURFACES` cannot see a devcontainer lifecycle command. This is the defect that
caused the outage, and this lane only disposed of it.**
`graph-orphan-census` refused `scripts/provision_legs.py` with *"script reached by no wiring
surface over triggers/imports"* — the same false-orphan verdict that got its predecessor deleted
at `3c9418cc` and cost a codespace a recovery container twelve days later. The real trigger chain
fires on every container creation with no human deciding in the moment, which is the census's own
predicate:

```
.devcontainer/devcontainer.json  onCreateCommand / postCreateCommand / postStartCommand
  -> bash .devcontainer/provision.sh
  -> uv run --no-sync python scripts/provision_legs.py     (six call sites)
```

`WIRING_SURFACES` lists five files and a workflow glob; `devcontainer.json` is not among them,
and `_SCRIPT_PATH_RE` reads config VALUES rather than shell scripts, **so adding it would not be
enough** — the chain needs one hop through a `.sh`. This lane wrote an `ORPHAN_DISPOSITIONS` row
instead, because widening the enum changes the census POPULATION repo-wide (every `scripts/*.py`
any shell script names stops being an orphan at once), which is a change to what the corpus
measures and not a `.devcontainer/` lane's edit. **Proposed row, not filed** (filing needs a
triage the lane's decision budget does not cover): *"Teach the process census to follow a shell
referrer, or declare shell-invoked scripts out of its population — the blind spot that retired
`cloud_provisioning.py`."* Kill-candidates for that row: none known.

**O-2 · The stale-image window is still open until this lands AND the prebuild refreshes.**
`prebuild.trigger` is `on_configuration_change`, so the image refreshes only when
`.devcontainer/devcontainer.json` or its `Dockerfile` changes. This lane edits `devcontainer.json`,
so merging it should refresh the image — **but that is a prediction, not a measurement.** Until
the refreshed image carries a `provision.sh` that has the hand-over in it, a codespace created
from the OLD image still runs the old script and still dies: the hand-over cannot be executed by a
script that does not contain it. **The first `-b main` create after this merges is the datapoint
that closes it**, and it is the integrator's to take, not this lane's.

**O-3 · `ecosystem/doc-counts.md` is stale by this lane's 84 tests.** `pytest_collected` reads
5938; actual is 6021+. Regeneration is the integrator's act per this lane's contract; every
commit here declared `SKIP=doc-counts-pytest-freshness` for it.

**O-4 · Test surfaces lost with `tests/test_cloud_provisioning.py` and NOT restored here.** That
file also carried the devcontainer-surface cases — `devcontainer.json` parses and wires every
lifecycle stage, the unexpanded-stamp refusal, three `--gate` stamp refusals, the
`uv run --no-sync` audit, the C1 accounting checks. They died with the module at `[#664]` and are
outside `[#746]`'s two legs, so they are named rather than quietly restored. `provision.sh`'s own
comment at the `refresh_source_tree` block still cites
`tests/test_cloud_provisioning.py::test_provision_sh_runs_the_history_repair_before_arming_hooks`
as a file that no longer exists; the TEST is back (in `tests/test_provision_sh.py`) but that
locator is stale and this lane did not rewrite the surrounding honest-limits paragraph.

**O-5 · `provisioning.yaml`'s `prebuild:` block now has no reader at all.** Marked as such at its
own head. Either a successor checker is written or the block is retired; neither is `[#746]`'s
call.

**O-6 · Codespaces quota.** This lane's probe (`lane-z-746-proof`) was deleted. The operator's
`lane-z-substrate-probe` — the recovery container this lane read its BEFORE evidence from — was
gone from `gh codespace list` by 04:30Z; **this lane did not delete it** and does not know who
did. One codespace remains: `suite-baseline-2026-09-08` (Shutdown).

## 5. Gate bypasses declared, and why each was not this lane's to fix

Every bypass is named in the commit that used it. Consolidated:

- `decision-coverage` — refuses on four operator decisions on the Drive transport
  (`to-cc/AMEND-NIGHT-PLAN-001.md`, `-002.md`, `DECLARE-NIGHT-PLAN-2026-09-15.md`, `-FINAL.md`).
  MEASURED with **nothing staged**: it refuses with the same four and only those four. They do
  not exist in this worktree.
- `doc-counts-pytest-freshness` — O-3 above.
- `graph-orphan-census` — on the two commits where `scripts/provision_legs.py` was still
  untracked. Its disposition landed in the same commit as the file, and `orphan-census` exits
  **OK** on the final tree.
- `audit-health` — its single `[!!]` is `journal_spine_anchor` on `0ee3d161`, **main's own tip
  merge**, whose JOURNAL entry belongs to the integrator seat that landed it minutes earlier.

**Main moved six times during this lane**: `b5270d63 -> 4328496e -> b81c5548 -> 8d029783 ->
7eb26e81 -> 0ee3d161`. Two sync merges were needed (`f1c27f33`, `7c65ceaf`) and a third attempt
was aborted rather than completed against a tip that had already moved. Note the direction at the
end: local `main` ran AHEAD of `origin/main`, so the second sync had to target the shared LOCAL
ref — which is the ref `journal_spine_anchor` reads the spine from. Each sync's anchor claim was
verified with `journal_anchor.is_anchored` **before** committing rather than by re-running the
gate.

## 6. Tests

```
tests/test_provision_legs.py   75 passed   (72 carried from 3c9418cc^, 3 new)
tests/test_provision_sh.py      9 passed   (was 7 failed, 2 passed at 3abd8098)
tests/test_graph_spine.py      37 passed
ruff check <every touched file>            clean
bash -n .devcontainer/provision.sh         clean
scripts/graph_queries.py orphan-census     OK
```

The 20 files `impacted_tests select --changed scripts/graph_queries.py` picks were also run:
**1206 passed, 1 skipped, 8 FAILED**. The eight are **pre-existing**, attributed by a paired
baseline/tip run adjacent in time and differing only in `scripts/graph_queries.py` — the failing
SET is identical in both: `test_canonical_docs` (2, both of which `audit.py health` already
reports as ungated-and-stale on main), `test_gen_handoff` (5, live-state probe binding and two
probe counts), `test_v6_frozen_contract::test_fr6` (*"R6 unbuilt"*). None names a file this lane
touches.

**The full suite is not run here** — `[#528]`: targeted per lane, full once at integration.
