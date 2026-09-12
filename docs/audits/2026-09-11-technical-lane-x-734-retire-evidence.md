# Lane `lane-x-734-retire-stage` — retire-stage evidence log

> Working evidence artifact for `LANE-x-734-retire-stage.md`, the first run of the AX13-2/AX13-3
> retire stage ([#734]). Appended to across the lane's steps; the final section is the
> end-of-lane artifact required by Steps 4/5 of the contract. Nothing here is prose narration
> of the census — it is the tool output the Done-contract requires be recorded verbatim.

## Step 1 — `safe_remove.py` + reverse-dep oracle verdicts, and the FPG-1 reader check

### The eight `scripts/` modules (covered by `safe_remove.py`, which drives the reverse-dep oracle)

First run, BEFORE `npm install` (the pyright langserver was not yet vendored in this worktree —
`node_modules/` is gitignored per-checkout, so a fresh worktree starts without it):

```
safe-removal verdict: UNVERIFIABLE
removal set: scripts/boundary_headers.py, scripts/boundary_report.py, scripts/cloud_provisioning.py, scripts/desired_state_loader.py, scripts/desired_state_report.py, scripts/probe_child_backlogs.py, scripts/seed_runbook.py, scripts/validate_onboarding_rulings.py
reason: 112 symbol(s)/module(s) the oracle could not verify (WARN + allow; honest-limit)

unverifiable (WARN + allow): 112 symbols, all `oracle-unavailable` -- the pyright langserver
was not resolvable (`find_langserver` returned None: no `--langserver` override, no vendored
`node_modules/pyright/langserver.index.js`, no `pyright-langserver` on PATH).

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a
non-blocking false PASS is possible; never a false FAIL).
```

Per the GO footprint clause ("a silent tool is INCONCLUSIVE... an inconclusive target is KEPT
with that reason recorded"), an all-`oracle-unavailable` UNVERIFIABLE run is not a pass. Rather
than KEEP all eight on that basis, this lane bootstrapped the already-declared, already-pinned
langserver dependency: `package.json`'s sole purpose is to pin `pyright@1.1.410` for this exact
oracle (`package.json` description: "Vendored Pyright langserver for the #193 code->code
reverse-dependency oracle (ADR-89)... Bootstrap a fresh checkout with `npm install`"), and
`package-lock.json` is committed. Running `npm install` here restores a declared, pinned,
checked-in dependency — not an addition of a new one — the same class of act as `uv sync
--locked`. `node_modules/` stays gitignored and untouched by this lane's commits.

Second run, AFTER `npm install` vendored `node_modules/pyright/langserver.index.js`, with the
oracle's own default per-symbol timeout (20s; the first re-run used `--timeout 300` per-symbol
by mistake, which is a per-QUERY timeout not a total budget, and was killed after ~20 minutes
with zero output rather than let it run out its ~9h worst case):

```
safe-removal verdict: SAFE
removal set: scripts/boundary_headers.py, scripts/boundary_report.py, scripts/cloud_provisioning.py, scripts/desired_state_loader.py, scripts/desired_state_report.py, scripts/probe_child_backlogs.py, scripts/seed_runbook.py, scripts/validate_onboarding_rulings.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a
non-blocking false PASS is possible; never a false FAIL).
```

**Verdict: SAFE, explicit "no surviving referrers" for the full eight-module set together** — the
in-set coupling (`boundary_headers` imports `boundary_report`; `desired_state_report` imports
`desired_state_loader`) resolves clean because the oracle evaluated the whole removal set at
once, so an in-set import is not a "surviving" external referrer. This is the explicit
"no importer, no reader" verdict the Done-contract requires. **All eight are DELETE.**

### `deploy/lived_sandbox/` (8 tracked `.py` files) — NOT covered by `safe_remove.py`

`safe_remove.py` only drives symbol-level oracle queries for `scripts/` modules; per AX13-5's own
warning this census corpus needs its readers checked via FPG-1's `imports`/`reads` edges instead.
`scripts/file_purpose_graph.py why <path>`, verbatim:

```
=== deploy/lived_sandbox/__init__.py ===
REFUSED: deploy/lived_sandbox/__init__.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/arc.py ===
path     : deploy/lived_sandbox/arc.py
node     : file:deploy/lived_sandbox/arc.py
purpose  : Lived-workflow sandbox — the GATED-MESH ARC driver + GATE-0 (Slice B; [#252]).

consumers (1) -- what reads this
  - is implemented by    task:267                                             [task-implements]

edges (0) -- what this reads / is coupled to
  (none)

=== deploy/lived_sandbox/cli.py ===
REFUSED: deploy/lived_sandbox/cli.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/consumer.py ===
REFUSED: deploy/lived_sandbox/consumer.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/isolation.py ===
REFUSED: deploy/lived_sandbox/isolation.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/observe.py ===
REFUSED: deploy/lived_sandbox/observe.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/oracle.py ===
REFUSED: deploy/lived_sandbox/oracle.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.

=== deploy/lived_sandbox/spawn.py ===
REFUSED: deploy/lived_sandbox/spawn.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.
```

`task:267` resolves to `tasks/267-scope-exercising-arc-extension.md`, **status: open**, whose
`refs` line names `deploy/lived_sandbox/arc.py (ARC_PROMPT)` directly. **This is a live reader**
— an open backlog row citing the file by name and role — which the domain census's
"UNTRIGGERED + UNREAD ≥ 60 days" disposition missed. This is exactly the blind spot AX13-5
records: the census read `.pre-commit-config.yaml` and missed the runtime/task-citation edge.

The other seven files return `REFUSED` — FPG-1 has no governed input naming them at all. A
`REFUSED` is **not** a clean "no reader" verdict; it is the same class of inconclusive result the
GO footprint clause treats a silent tool as. Since the census's own table row bundles all eight
tracked `.py` files as ONE target line, and one member of that bundle (`arc.py`) has a confirmed
live reader, **the whole `deploy/lived_sandbox/` target is KEPT**, not split: `arc.py` because it
is live, and the other seven because their verdict is inconclusive rather than a pass, and
because this lane's GO footprint does not extend to re-dispositioning the directory into
"delete seven, keep one" — that would be a scope decision this lane was not asked to make.

**Verdict: KEEP (whole directory).** Reason recorded per-target below.

### `config/requirements-dev.txt` — NOT covered by `safe_remove.py`

FPG-1 `why`, verbatim:

```
=== config/requirements-dev.txt ===
REFUSED: config/requirements-dev.txt: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.
```

Same inconclusive class as above. But a direct repo-text search surfaces a standing ruling that
resolves this one outright: **ADR-106 §5** ("Deliberate exceptions") states, verbatim:

> `config/requirements-dev.txt` is superseded but **retained** (deletion needs an explicit
> operator ask — no-delete invariant); retire-candidate for the rollout.

This is a genuine rule-vs-ruling conflict (decision-budget class (b)): the batch GO's target
table lists this file among the ten, but ADR-106 names a **standing no-delete invariant**
requiring its own explicit operator ask, distinct from a bundled batch GO alongside nine
unrelated targets. The 2026-09-11 domain census itself flagged it only as a `GARBAGE-CANDIDATE`
**proposal** ("awaiting the operator's GO, not an action"), not as pre-cleared.

**Verdict: KEEP, flagged for the operator.** This lane does not delete a file an ADR names
under a no-delete invariant on the strength of a bundled batch GO; the conflict is reported here
and in the end-of-lane packet rather than resolved unilaterally.

## Disposition summary (after Step 1)

| target | verdict | disposition |
|---|---|---|
| `scripts/boundary_headers.py` | SAFE — no surviving referrers | DELETE |
| `scripts/boundary_report.py` | SAFE — no surviving referrers | DELETE |
| `scripts/cloud_provisioning.py` | SAFE — no surviving referrers | DELETE |
| `scripts/seed_runbook.py` | SAFE — no surviving referrers | DELETE |
| `scripts/validate_onboarding_rulings.py` | SAFE — no surviving referrers | DELETE |
| `scripts/probe_child_backlogs.py` | SAFE — no surviving referrers | DELETE |
| `scripts/desired_state_loader.py` | SAFE — no surviving referrers | DELETE |
| `scripts/desired_state_report.py` | SAFE — no surviving referrers | DELETE |
| `deploy/lived_sandbox/` (8 tracked `.py`) | `arc.py` has a live reader (open task `[#267]`); the other 7 are FPG-1 `REFUSED` (inconclusive) | KEEP — reason: live reader on one bundled member, inconclusive on the rest |
| `config/requirements-dev.txt` | FPG-1 `REFUSED` (inconclusive); ADR-106 §5 no-delete invariant | KEEP — reason: ADR-106 standing no-delete invariant requires its own explicit operator ask |

## Step 2 — deletions, and one target reversed after the targeted tests REDded

Deleted, with their coupled surfaces (module + dedicated test + `graph_queries.py`
`Disposition` entry + `tests/test_graph_spine.py` `CENSUS_SCRIPT_ORPHANS` entry), per the SAFE
verdict above:

- `scripts/boundary_headers.py` + `scripts/boundary_report.py` (the coupled pair, moved together)
- `scripts/cloud_provisioning.py`
- `scripts/seed_runbook.py`
- `scripts/validate_onboarding_rulings.py`
- `scripts/probe_child_backlogs.py`

**`scripts/desired_state_loader.py` / `scripts/desired_state_report.py` were REVERSED after
deletion and are KEPT, not removed.** Deleting the pair REDded
`test_the_live_tree_carries_no_dangling_process_reference`: `ARCHITECTURE.md:503-504` still
names both files in prose ("`scripts/desired_state_loader.py` is the **loader**... ;
`scripts/desired_state_report.py` is the **divergence report** over it"), and once the files
and their `Disposition` entries were gone, `dangling_references()` correctly flagged the stale
prose. Fixing `ARCHITECTURE.md` is **outside this lane's declared GO footprint** (target file +
dedicated test + `Disposition` entry + `test_graph_spine.py` entry only — the GO footprint
clause is explicit that "anything else a deletion appears to require is out of footprint: stop,
keep the target, and report it"). Both files, their tests, their `Disposition` entries and their
`CENSUS_SCRIPT_ORPHANS` fixture rows were restored. **KEPT — reason: deletion requires an
ARCHITECTURE.md prose edit outside this lane's GO footprint; flagged for the operator/integrator
to decide whether ARCHITECTURE.md's prose or the deletion should move first.**

**One pre-existing, unrelated defect was also fixed in the same coupled surface this lane
already had open:** `scripts/graph_queries.py`'s `ORPHAN_DISPOSITIONS` still carried an entry
for `.claude/commands/override.md`, which does not exist on disk — it was removed by a prior
batch-W commit (`5e17ecd7`, "remove /override -- node, payload and the carrier leg, in one
act"). The stale entry's own text still claimed "kept rather than deleted", which was simply
wrong by the time this lane read it, and it REDded
`test_the_disposition_register_names_no_file_that_is_gone` once the tests were run end to end.
This is not out-of-footprint tidy-up: **AX13-3, already carried verbatim into row `[#734]` by
this lane's first commit, explicitly assigns this exact gap to this lane** ("the W-4 `/override`
removal gets its tombstone retroactively"). The stale `Disposition` entry is removed here; its
tombstone is recorded in Step 3 below alongside the eight targets this lane actually deletes.

Targeted tests after all of the above: `pytest tests/test_graph_spine.py` — **35 passed**.
Full-repo `pytest --collect-only` — **5544 tests collected, no collection errors** (no stray
import of a deleted module anywhere in the suite).

The `doc-counts-pytest-freshness` pre-commit gate then refused the commit on the resulting
`pytest_collected` drift (file claimed 5752, actual 5544 after six modules' tests left the
suite) until `ecosystem/doc-counts.md` was regenerated with `gen_doc_counts.py --write` — a
narrow, gate-mandated, one-line count update, not the fleet-wide index regeneration the
contract reserves for the integrator.

## Step 3 — tombstones and lifecycle records: no eligible edit found; two findings flagged instead

The Done-contract's clause 2 and AX13-3 call for `deprecated -> removed` records in
`ecosystem/organ-index.md` and `status: removed` tombstones in
`deploy/manifest-v1.5.0.yaml`. Checked both registries against the six actually-deleted
scripts, and against AX13-3's named retroactive case (`/override`); **neither registry
gets an edit from this lane**, for two distinct, checked reasons:

**1. None of the six deleted scripts were ever entries in either registry.**
`ecosystem/organ-index.md` is machine-generated purely from organ SOURCES — `.claude/{agents,
commands,skills,workflows,rules}`, `.claude/settings.json`, `.pre-commit-config.yaml`, the
`tier1-lifecycle` plugin manifest, plus the L0 rows in `ecosystem/organ-registry.yaml` (its own
header, verbatim). `deploy/manifest-v1.5.0.yaml`'s `components:` section tracks items the
CARRIER ships to consumer repos. A `grep` for each of the six names across both files returns
zero component/organ entries — they were plain untriggered `scripts/*.py` utility modules,
never organs and never shipped. There is nothing to transition from `deprecated` to `removed`
in either registry for them, because they were never IN either registry to begin with.

**2. `/override`'s retroactive tombstone (AX13-3's named case) is BLOCKED by a documented,
gated release constraint — a genuine rule-vs-ruling conflict (decision-budget class (b)),
flagged rather than forced.** `deploy/release_lint.py`'s own module docstring states the P1
lifecycle boundary explicitly: *"only `status: active` is legal this release —
`deprecated`/`removed` (tombstones) unlock in P2, gated on operator decision D3, so a tombstone
landing early fails loud here instead of silently meaning nothing"* (C6). The manifest's own
`override-command` comment block (written by the very commit `5e17ecd7` that removed
`/override`) already records this: *"A `status: removed` tombstone was NOT available — this
release admits only `status: active` (release_lint C6; tombstones unlock in P2 on operator
decision D3) — so consumers already carrying the command keep it until a prune leg exists."*
The one existing `status: removed` entry in the manifest (`ruff-gate`) is an explicit, one-time
"n=1 prune truth-maker" demonstration, not a general opening of the tombstone mechanism.
Writing a second `status: removed` entry for `/override` here would contradict the release's
own documented lifecycle boundary and the deliberate architectural decision already recorded
at its removal commit. **This lane does not force it.** Flagged for the operator/architect:
AX13-3 assumes tombstoning is generally available; it is not, until D3. `/override`'s stale
`ecosystem/organ-index.md` row (still showing `.claude/commands/override.md` as if it exists)
is a pre-existing generation-drift artifact from the same gap — regenerating that index is
reserved for the integrator under this lane's "No index regeneration" bound, and is flagged
here for the integrator's next regen pass rather than run by this lane.

`deploy/release_lint.py --version 1.5.0` (unaffected by this lane, since neither registry was
touched): `0 FAIL, 1 WARN (C2 — git tag not yet resolved, expected pre-release), 7 pass`.
**Green**, per the Done-contract's precondition.

## Step 4/5 — end-of-lane artifact: what changed, what was kept, what is open

### Deleted (module + dedicated test + `graph_queries.py` Disposition + `test_graph_spine.py` entry, all four coupled surfaces removed together)

- `scripts/boundary_headers.py` + `scripts/boundary_report.py` (coupled pair)
- `scripts/cloud_provisioning.py`
- `scripts/seed_runbook.py`
- `scripts/validate_onboarding_rulings.py`
- `scripts/probe_child_backlogs.py`

Six of the ten GO'd targets. All SAFE per the reverse-dep oracle: no surviving referrers.

### KEPT, with reason

- **`scripts/desired_state_loader.py` / `scripts/desired_state_report.py`** — SAFE per the
  oracle, but deletion REDs `test_the_live_tree_carries_no_dangling_process_reference`:
  `ARCHITECTURE.md:503-504` still names both in prose, and fixing `ARCHITECTURE.md` is outside
  this lane's declared GO footprint (target file + dedicated test + `Disposition` entry +
  `test_graph_spine.py` entry only). **Open item for the operator/integrator:** either amend
  `ARCHITECTURE.md:503-504` (removing or updating the prose naming these two files) in a lane
  whose footprint covers it, or re-scope the GO footprint for this pair specifically, then
  re-run this same deletion.
- **`deploy/lived_sandbox/` (8 tracked `.py` files)** — NOT covered by `safe_remove.py`.
  `arc.py` has a confirmed live reader: open task `[#267]` names it directly as `ARC_PROMPT`
  — exactly the blind spot AX13-5 warns the census missed. The other 7 files return FPG-1
  `REFUSED` (inconclusive, not a clean pass). The census bundles all eight as one target line;
  since one member is confirmed live, the whole directory is KEPT rather than split into a
  per-file re-disposition this lane was not asked to make. **Open item:** a future pass should
  re-examine `deploy/lived_sandbox/` file-by-file now that `arc.py`'s live status is known,
  rather than treating the directory as one unit.
- **`config/requirements-dev.txt`** — NOT covered by `safe_remove.py`; FPG-1 `REFUSED`
  (inconclusive). More importantly, **ADR-106 §5 names a standing no-delete invariant**
  ("deletion needs an explicit operator ask") distinct from this batch's bundled GO. **Open
  item, flagged as a genuine rule-vs-ruling conflict (decision-budget class (b)):** the
  operator's batch GO listed this file among the ten targets; ADR-106 requires its own,
  separate explicit ask. This lane does not treat a bundled batch GO as satisfying a
  standing-invariant's requirement for a dedicated ask, and defers to the operator/architect
  to either issue that explicit ask or amend/retire the ADR-106 invariant.

### Proposed diffs this lane did NOT make, and why (all flagged above, collected here for one read)

1. `ARCHITECTURE.md:503-504` — would need editing to un-block `desired_state_loader.py` /
   `desired_state_report.py`'s deletion. Out of this lane's GO footprint.
2. `deploy/manifest-v1.5.0.yaml` — AX13-3 asks for a retroactive `status: removed` tombstone
   for `/override`. Blocked by `release_lint.py`'s documented P1 lifecycle boundary (tombstones
   illegal until operator decision D3 unlocks P2), and by the manifest's own recorded rationale
   for why `/override` was removed without one. Not attempted.
3. `ecosystem/organ-index.md` — carries a stale `/override` row (names a file that no longer
   exists). Regenerating it is reserved for the integrator under this lane's "No index
   regeneration" bound. Not attempted; flagged for the integrator's next regen pass.
4. `config/requirements-dev.txt` deletion — blocked by ADR-106's no-delete invariant, per above.

### AX4-1 disposition (carried per AX12-1, not this row's clause)

AX4-1 (floor declaration mandatory) was carried verbatim into row `[#734]` per AX12-1's mandate,
for the record. **It names the `decision_coverage` lane (X1-1) as owner and was left
untouched by this lane** — no edit was made to X1-1's row or to `ecosystem/parity-surfaces.yaml`
on its behalf.

### Verification summary

- `safe_remove.py` (reverse-dep oracle): SAFE for the eight-module set — verbatim in Step 1.
- Targeted tests: `pytest tests/test_graph_spine.py` — **35 passed** (re-confirmed after every
  content-affecting commit in this lane).
- Full-repo collection sanity: `pytest --collect-only` — **5544 tests collected, no errors**.
- `deploy/release_lint.py --version 1.5.0` — **0 FAIL, 1 WARN (expected pre-release), 7 pass**.
- `ecosystem/doc-counts.md` regenerated (pytest_collected 5752 → 5544) to satisfy the
  `doc-counts-pytest-freshness` gate — a narrow, mandatory, one-line count fix, not a
  discretionary index regeneration.

### Row `[#734]` status

**Not closed by this lane.** `[#734]`'s Done-when covers the full census disposition (35
non-live items each DELETE/TRIGGER/KEEP, 16 UNKNOWN resolved by a second pass, delivered as ONE
file for ONE GO). This lane executed only the already-GO'd deletion leg for ten specific
targets. `kill-candidates: none` on every commit in this lane, consistently.
