# N1 — [#529]/[#530] wiring spec (batch-2 Lane L2 prep)

**Lane:** NIGHT N1 · cloud channel · read-only + drafts
**Branch:** `claude/wiring-spec-telemetry-flight-o7oja9`
**Dispatch stamp:** `docs/audits/2026-08-19-technical-n1-wiring-spec-contract.md` (commit `12cc4c6`)
**Reads the tree at:** `87dd41a` (batch-1 packet-amendment merge), which contains the `[#533]`
leg-2 merge `f4a01f0e` the brief names. The decomposed runner is read as it now exists, not as
the pre-merge shape.

## Environment honesty header — WHICH GATES RAN, MEASURED NOT ASSUMED

The brief anticipated a uv-pin issue on this channel. It reproduces, and it is worse than a pin
mismatch alone. Measured live in this container:

```
$ uv run --frozen pytest --collect-only -q
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.

$ python -m pytest --collect-only -q      -> No module named pytest
$ python -m pre_commit --version          -> No module named pre_commit
$ ls -la .git/hooks/ | grep -v sample     -> empty (no hooks installed)
$ python --version                        -> Python 3.11.15
$ grep requires-python pyproject.toml     -> requires-python = ">=3.12"
$ ruff --version                          -> ruff 0.15.8   (>= the >=0.15.5 floor: usable)
```

So: **no pytest, no pre-commit, no armed git hooks, and the interpreter is below the project's
own floor.** The environment cannot build the venv (`uv` pin) and could not run the suite even
if it could (Python 3.11 vs `>=3.12`).

**No gate was bypassed, because no gate ran.** The dispatch-stamp commit produced zero hook
output — that is the absence of installed hooks, not a suppressed failure. Nothing in this lane
used `--no-verify`. This artifact is markdown only: it changes no Python, so the one gate that
*could* have run here (`ruff`, which is present) has nothing to say about it.

**Consequence for Lane L2, and it is not cosmetic:** every claim in items 1–3 below is derived
from *reading* the tree, plus the small number of behaviours I could measure with the stdlib
alone (marked **MEASURED** where they are). Nothing here is derived from a suite run. L2 runs on
a machine with the real toolchain and must re-verify anything marked **UNVERIFIED** before
acting on it.

---

## Item 1 — Call-site derivation — **CLEAR**

### Standing fact both halves rest on

`grep -rn 'telemetry_emit\|single_flight'` over the tree returns, outside the two modules
themselves: their own two test files, and two lines of JOURNAL prose (`JOURNAL.md:515`,
`:1250-1251`). **Zero non-test import sites, confirmed.** Both rows are accurate about their own
state.

### 1A — `[#529]` telemetry_emit

Done-when (BACKLOG.md:265): *"the three stage-1 events emit from live gate runs into a WAL-mode
SQLite store via structlog with a test per event type, each constraint carries a test, and a
recorded gate run reads back without re-measurement"*. Open legs (1) wire the call sites,
(2) `.gitignore` the store, (3) decide structlog, (4) the last two Done-when legs.

The call surface is `telemetry_emit.py:47-93`: `emit_check_run(name, outcome, duration_ms=…)`,
`emit_hook_run(name, outcome, duration_ms=…)`, `emit_blocker_fired(name, reason=…)`, plus
`safe_emit(emitter, …)` for a gate's critical path.

#### `check_run` — ONE site, because `[#533]` leg 2 made it one

| # | Site | Why |
|---|---|---|
| 1 | `scripts/audit.py:3553` `run_checks()` — the whole function | Since `f4a01f0e` this is the single funnel every one of the 43 registry checks runs through. Instrumenting it gives `name`/`outcome`/`duration_ms` per check for **all three** callers with no per-check edit. |
| 1a | `scripts/audit.py:3583-3586` — the serial branch | The default path, and the one `audit-health` actually uses on every commit. |
| 1b | `scripts/audit.py:3590-3593` — the parallel branch | The opt-in path. Timing must be taken **inside the submitted callable**, around `check(repo_path)` — *not* around `future.result()` at `:3593`, which would bill each check for its queue wait and report a fabricated `duration_ms`. |
| 1c | after `:3594` (the slot flatten) | Emission happens here, walking slots in registry order, so emitted event order == `CHECK_ORDER` == finding order. Emitting inside the worker would interleave by completion order. |

The three *callers* are deliberately **not** sites — they inherit instrumentation from the
funnel: `audit_repo` (`:3608`), `cmd_health` (`:4174`), `cmd_ship_gate` (`:4273`).

Wiring the 43 checks individually is rejected: `tests/test_audit.py` is untouchable, 25 of the 43
are facade-resident behind monkeypatch seams (`audit_checks/registry.py:11-16`), and 43 edit
sites is 43 chances to detach a seam for a signal one funnel already carries.

#### The `outcome` impedance mismatch — a decision, not a mapping to improvise

`Finding.status` is a **five**-value enum (`_common.py:34`): `pass|fail|warn|unavailable|n/a`.
`telemetry_emit.OUTCOMES` (`:135`) is **three**: `pass|block|error`. They do not line up, and a
check may emit several findings with different statuses. `emit_event` **refuses** an unknown
outcome (`:368-369`), so this cannot be left to chance.

Proposed mapping — L2 confirms or overrides, and it is a decision-budget item:
`fail` → `block`; `pass`/`warn`/`n/a`/`unavailable` → `pass`; a check that **raised** → `error`.
The collapsed distinction rides `context` (e.g. `{"statuses": {"warn": 2, "pass": 1}}`) so the
read side loses nothing. Multi-finding checks emit **one** event with the aggregate, not N.

#### `hook_run` and `blocker_fired` — three organs, clean single `main()` each

| # | Site | Exit points | Why |
|---|---|---|---|
| 2 | `scripts/block_ff_push.py:222` `main()` | `:241` allow-n/a · `:255` error · `:257` allow-clean · `:271` **refuse** | PREVENT half of core-invariant #5. Its fire-count-vs-block-count is literally the memo's "is a hook pure ceremony?" question. |
| 3 | `scripts/block_unanchored_push.py:79` `main()` | `:95` allow-n/a · `:103` allow-no-obligation · `:110` error · `:112` allow-anchored · `:123` **refuse** | The ADR-85 hard leg. Its block rate is the evidence base the ADR-85 amendment was argued from. |
| 4 | `scripts/block_commit_on_main.py:133` `main()` | `:138` allow · `:143` error · `:154` **refuse** | The commit-time sibling. Its documented fail-**open** hole (`current_branch()` returns `None` on any git error) becomes *visible* as `outcome="error"` rather than staying a silent allow. |

`blocker_fired` fires **only** at the bolded refuse returns (`:271`, `:123`, `:154`) — each
already computes the reason string the emitter wants. Note `emit_blocker_fired` hard-fixes
`outcome="block"` (`:447-456`), so a refusal emits **both** a `hook_run(outcome="block")` and a
`blocker_fired`. That is the memo's own shape (they are separate event types for separate
questions), but it is double-counting if a reader sums naively — L2 records the choice rather
than letting a reader discover it.

Every hook call uses `safe_emit` (`:459-472`): a locked store must never turn into a failed
push. Exit codes must not move — see item 3.

#### **BLOCKER — MEASURED.** Wiring `audit.py` prints telemetry to stderr on every commit

`scripts/audit.py:283` calls, at **module scope**:

```python
logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
```

`telemetry_emit._log_event` (`:305-319`) logs each event at **INFO** to logger `"telemetry"`.
`basicConfig`'s default stream is `stderr`. Measured in this container:

```
$ python -c 'import logging,json; logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO); \
    logging.getLogger("telemetry").info(json.dumps({"event_type":"check_run","name":"doc_claims","outcome":"pass"}, sort_keys=True))'
telemetry: {"event_type": "check_run", "name": "doc_claims", "outcome": "pass"}      # -> stderr

$ python -c 'import logging; logging.basicConfig(level=logging.INFO); print(logging.getLogger().handlers[0].stream.name)'
<stderr>
```

So a wired `audit.py health` gains **one `telemetry: {…}` stderr line per check — 43 per run**,
on a pre-commit gate that fires on every commit. This is not hypothetical and L2 must handle it.
Options, in the order I'd take them:

1. `logging.getLogger("telemetry").setLevel(logging.WARNING)` at the audit wiring site — one
   line, local to the caller, changes no library.
2. `logger.propagate = False` + a `NullHandler` — same effect, also caller-local.
3. Rule the 43 lines acceptable. (I would not; it makes every commit noisier for a signal
   already durably recorded in SQLite.)

**The hooks are NOT affected, and I measured that too:** none of `scripts/*.py` except `audit.py`
touches `logging`, and with no handler configured Python's `logging.lastResort` is WARNING-level,
so an `.info()` emits nothing. A hook subprocess's stderr stays byte-clean:

```
$ python -c 'import logging,json; logging.getLogger("telemetry").info(json.dumps({"x":1}))' 2>&1
(no output)
```

#### **BLOCKER — the sandbox seam does not reach the telemetry store**

`telemetry_emit.py:110` sets `_REPO_ROOT = Path(__file__).resolve().parent.parent` and
`default_db_path()` (`:266-275`) returns `_REPO_ROOT / logs/TELEMETRY.db`. `audit._REPO_ROOT`
(`audit.py:70`) is a **different, independent** module-level value — and it is one of the 25
names `tests/test_audit.py` monkeypatches.

Therefore: monkeypatching `audit._REPO_ROOT` to a tmp dir does **not** redirect the telemetry
store. `tests/test_ship_gate.py:118 test_ship_gate_is_readonly` builds a tmp repo, patches
`aud._REPO_ROOT` at it, and asserts `before == after` over `repo.rglob("*")`. A wired ship-gate
would write to the **real** `logs/TELEMETRY.db` — outside the tmp tree the test watches. The test
still passes, **for the wrong reason**, while the suite writes into the real repo on every run.

That is exactly the "seam detaches SILENTLY … the check would still pass while testing nothing"
failure class `audit_checks/registry.py:18-22` documents.

**Requirement, therefore, and it is not optional:** every wiring site passes an **explicit**
`db_path=` derived from the caller's own repo root (`audit._REPO_ROOT` for the audit sites, the
hook's `_repo_root()` for the hook sites). Never rely on `default_db_path()`. This single rule
also discharges the `[#529]` row's own terra P1 (`default_db_path()` resolves to the WORKTREE in
a linked worktree) — same defect, same fix, and `fleet_analytics.py:1075` `_git_common_dir()` is
the named pattern for resolving the shared root when that matters.

#### Leg 2 — `.gitignore`, and it needs a glob not a line

The row says *".gitignore `logs/TELEMETRY.db`"*. **MEASURED:** WAL mode creates two sidecars
while a connection is open —

```
files while connection OPEN: ['TELEMETRY.db', 'TELEMETRY.db-shm', 'TELEMETRY.db-wal']
files after clean close:     ['TELEMETRY.db']
```

They vanish on a *clean* close; a crashed writer or a concurrent reader leaves them. Since the
whole point of WAL here is concurrent hook/lane writers, the ignore must be `logs/TELEMETRY.db*`,
not `logs/TELEMETRY.db`. A stray `-wal` dirties `git status` and trips session-end backpressure —
the exact failure the leg was filed to prevent.

#### Leg 3 — structlog stays a non-decision for L2

`logger_backend()` (`:322-332`) reports `stdlib-logging` today; structlog is absent from
`[dependency-groups]` and `uv.lock`. The brief forbids dependency changes, and the module is
explicit that no event is lost either way (`:32-40`). **L2 wires against the fallback and changes
nothing.** Leg 3 stays open on the row.

### 1B — `[#530]` single_flight

Done-when (BACKLOG.md:66) is **already met** (row: *"merged `50daad05`, Done-when met, NOT
closed"*). What is open is two defects plus the absence of call sites.

#### The honest structural finding: there is no Python dispatch entry point to wire into

`single_flight` is a library + CLI whose grain is one contract id. Dispatch in this repo is
**operator-run** — `[#540]` states it outright (*"Dispatch stays operator-run"*), and the
dispatch surface is `/lane-boot`, a markdown command. So "wiring [#530]" does not mean adding
imports; it means adding invocation steps to two command files.

| # | Site | Verb | Why |
|---|---|---|---|
| 5 | `.claude/commands/lane-boot.md` §1 "Pre-flight", after the branch-name check at `:22-26` | `claim` | The last point before a worktree exists. The witnessed failure was three executions of ONE contract; a claim here is the first moment that is refusable, and §1 already runs from the primary checkout where the remote is reachable. |
| 6 | `.claude/commands/lane-integrate.md` §3, as a **6th** refuse-to-finish row (table at `:57-63`) | `release` | The checklist is already the mechanical close-out, and item 5's own reasoning — a thing that lives in the *common* git dir and outlives `worktree remove`, `prune` and the branch delete — applies verbatim to a held `refs/locks/<id>`. A lock ref is precisely a stash-shaped residue. |
| 7 | `scripts/preflight_contract.py:401` `main()` | `inspect` **only** | Optional, weaker, and read-only. `/preflight` is adoption-first and wired into no gate (`.methodology.yaml:73-81`), so reporting "this contract is already in flight" as a preflight finding costs nothing and gates nothing. Never `claim` here — `/preflight` must stay side-effect-free. |

The contract id needs no new config: `/lane-boot <letter> <id> <slug> <contract-path>` already
carries it.

#### **BLOCKER — wiring `release` activates a latent data-loss race**

The row records two open legs, both *"latent (wired to no hook)"*. Wiring is exactly what ends
that latency:

* **(a) ABA in `release` (`single_flight.py:271-283`).** `release` reads the local holder, then
  deletes the remote ref. After a manual lock clear and a re-claim by a *different* lane, lane
  A's cleanup deletes lane B's **live** lock. Racers share HEAD, so the sha guard on the local
  delete does not disambiguate them — the row says a generation-unique token is needed.
* **(b) `rev-parse` conflation (`:206-208`).** `_local_holder` maps *any* non-zero return to
  "ref absent", so on a corrupt repo `--local-only` prints `FREE` and `release` reports success
  without having read state.

**Requirement:** L2 either lands the (a) fix before wiring site 6, or wires `claim` + `inspect`
only and defers `release` to a follow-up with the residual stated on the row. Wiring `release`
on top of an unfixed (a) converts a documented latent bug into a live one that silently unlocks
another lane's contract. Fixing (a) is a `scripts/` behaviour change and therefore its own
decision — I flag it, I do not rule it.

---

## Item 2 — Config surface — **CLEAR** (with one honest negative)

### What must be configurable

| Knob | Library | Today | Verdict |
|---|---|---|---|
| Emit destination | `[#529]` | `DEV_KNOWLEDGE_TELEMETRY_DB` env var (`:124`) + per-call `db_path=` (`:341`) | **Sufficient** — but item 1 requires the caller pass `db_path=` explicitly anyway, so the env var becomes the operator override, not the mechanism. |
| Emission on/off | `[#529]` | **Nothing** | **Must be added.** A gate that gained an unconditional side-effect with no off switch is not something to ship into a pre-commit hook. |
| Flight scope — arbiter | `[#530]` | `--remote` (default `origin`), `:323` | Sufficient. |
| Flight scope — network | `[#530]` | `--local-only`, `:324-325` | Sufficient. |
| Flight grain | `[#530]` | positional `contract_id`, `:321` | Sufficient — derived from the contract path, not configured. |

### The existing surface it joins — and the negative result

I looked for a runtime-knobs YAML to join and **there is not one.** The candidates and why each
is wrong:

* `.methodology.yaml` — the hub's *sanctioned-divergence register* (`:1-8`), read by
  `enforcement_coverage.py` and `fleet_parity`. Wrong shape entirely.
* `ecosystem/*.yaml` — ecosystem *state* (`deployed-versions`, `parity-surfaces`,
  `silent-rule-baseline`, `organ-registry`). Not runtime knobs.
* `pyproject.toml` — packaging + `[tool.ruff]`. The ruff table is fleet-equalized and
  parity-gated; adding an unrelated tool table there invites a parity question the lane
  shouldn't open.

**A new YAML file would need ADR-101 sanction.** `validate_hermetization.py` Rule C blocks an
added file whose home is outside the allowlist, and a new top-level config file is a Rule A
question on top. That is an operator ruling, not a lane's call.

**So: follow the precedent `audit.py` itself set one commit ago.** `[#533]` leg 2 needed exactly
this — a knob that is "configuration a reader can find and an operator can argue with rather than
a literal buried in a call" (`audit.py:3535-3538`) — and answered it with a **named module
constant + a click option**:

```python
_PARALLEL_MAX_WORKERS = 8                                    # audit.py:3540
@click.option("--parallel/--no-parallel", default=False, …)  # audit.py:4118
@click.option("--workers", type=click.IntRange(min=1), …)    # audit.py:4123
```

Recommended shape for L2, deliberately isomorphic to that:

```python
_TELEMETRY_DEFAULT = False                       # named constant, not an inline literal
@click.option("--telemetry/--no-telemetry", default=_TELEMETRY_DEFAULT, show_default=True,
              help="Emit check_run telemetry to the [#529] store. DEFAULT OFF: this flag "
                   "exists so emission can be measured and opted into; flipping the "
                   "audit-health hook's default is a separate ruling.")
```

Default **OFF**, and the help text says why — the same "the default did not move, and moving it
is someone else's ruling" posture `[#533]` leg 2 took, which `tests/test_audit_parallel.py:116`
pins with a test rather than a comment. For the hooks, which have no click layer, the switch is
an env var read at `main()` entry (`DEV_KNOWLEDGE_TELEMETRY=1`), defaulting off.

**The `logs/` destination itself is already ruled** — the 2026-07-22 artifact-naming ruling
(CLAUDE.md §9) wants an UPPERCASE-KEBAB stem with an extension honest to the format.
`logs/TELEMETRY.db` conforms; nothing to decide.

---

## Item 3 — PINNED-BY-TESTS — **CLEAR**

Method: `grep -rn` for each surface across `tests/`, plus the monkeypatch sweep. **UNVERIFIED by
execution** — no pytest in this environment (see the header). Every row is a read of the test
source.

### Directly touched surfaces

| Surface | Pinning tests | Touched or avoided |
|---|---|---|
| `audit.run_checks` (`:3553`) | `tests/test_audit_parallel.py` — 18 direct calls at `:71,77,78,91,98,105,110,111,124,132,158,173,175,200,232,233`. The load-bearing ones: `test_parallel_is_byte_identical_to_serial_on_synthetic_checks` (`:75`), `test_serial_and_parallel_are_byte_identical_on_real_checks_against_the_live_tree` (`:219`), `test_every_check_runs_exactly_once` (`:96`), `test_an_exception_in_a_worker_propagates_and_is_never_swallowed` (`:165`), `test_the_default_is_serial_and_runs_on_the_calling_thread` (`:116`), `test_run_checks_defaults_to_the_live_registry` (`:191`) | **TOUCHED** — the body changes. All six must stay green **unedited**. They constrain the wiring precisely: emission may not alter returned findings, may not swallow a worker exception, may not put work on a thread in serial mode, and may not read `ALL_CHECKS` at import. |
| `audit.cmd_health` (`:4127`) | `tests/test_audit.py:550,564,573,616,630,636,646,1703,1708,1752,1757,1793` | **AVOIDED** — `tests/test_audit.py` is the seam leg's and untouchable. The `_GATE_MODE` set/restore tests (`:616`, `:636`) constrain the wiring: emission must sit inside the existing `try/finally`, never around it. |
| `audit.cmd_ship_gate` (`:4234`) | `tests/test_ship_gate.py` — all 12 tests via `_run` (`:67-79`) | **AVOIDED**, but see item 1: `test_ship_gate_is_readonly` (`:118`) **cannot see** a telemetry write, because it watches only the tmp tree `aud._REPO_ROOT` points at. Passing the explicit `db_path=` is what makes this test meaningful again. |
| `block_ff_push.main` (`:222`) | `tests/test_block_ff_push.py` — subprocess-driven; asserts `returncode` (`:191,218,232,244,269,296,345,361`) and `stderr` substrings (`:191,205,258,269,346,362`) | **TOUCHED.** Substring assertions survive extra output, so a stray line would not redden them — which is why "stderr stays clean" needs its **own** new test rather than trusting these. Exit codes must not move. |
| `block_unanchored_push.main` (`:79`) | `tests/test_adr85_integration_enforcement.py`; `tests/test_validate_no_ff.py` (shared-signature) | **TOUCHED** — same constraints. |
| `block_commit_on_main.main` (`:133`) | `tests/test_block_commit_on_main.py` | **TOUCHED** — same constraints. |

### Surfaces deliberately left alone

| Surface | Pinning tests | Touched or avoided |
|---|---|---|
| `telemetry_emit` module | `tests/test_telemetry_emit.py` — 28 tests | **AVOIDED** if the library is unchanged. If the logging fix lands *in the library* rather than at the caller, `test_emit_survives_an_unusable_log_side_channel` (`:387`, monkeypatches `te.logging`) and `test_logger_backend_reports_which_side_channel_is_live` (`:381`) become **TOUCHED** — which is the argument for fixing it caller-side. |
| `single_flight` module | `tests/test_single_flight.py` — 20 tests, real git against a local bare remote | **AVOIDED** if only commands change. If open leg (a) is fixed, `test_t5_release_then_reclaim` (`:258`) and `test_t5_release_is_idempotent` (`:269`) become **TOUCHED**. |
| `audit.ALL_CHECKS` monkeypatch seam | 28 test files (`test_audit.py`, `test_ship_gate.py`, `test_writer_integrity.py`, `test_validate_doc_claims.py`, `test_silent_rule_ratchet.py`, `test_skip_is_not_pass.py`, `test_hub_identity.py`, `test_stale_worktrees.py`, `test_membership_agreement.py`, `test_fleet_audit_replication.py`, `test_legibility_graph_conformance.py`, `test_task_tree_gate.py`, `test_residual_completeness.py`, `test_review_artifact_coverage.py`, `test_preflight_contract.py`, `test_undeclared_edges_leg.py`, `test_verify_handoff_probes.py`, `test_doc_code_edge.py`, `test_gen_intake_tree.py`, `test_gen_handoff.py`, `test_v6_frozen_contract.py`, `test_validate_git_backlog.py`, `test_validate_doc_rot.py`, `test_validate_doc_structure.py`, `test_validate_reconciliation.py`, `test_validate_no_ff.py`, `test_fleet_analytics.py`, `test_audit_parallel.py`) | **AVOIDED** — the registry is not modified. Listed because any of them can route through `run_checks`, so they are all downstream of site 1. |
| Check count | `tests/test_writer_integrity.py:170 test_all_checks_count_is_pinned`; `tests/test_audit.py:2207,2223` (`== 43`) | **AVOIDED** — wiring adds no check. |
| `Finding` shape | `tests/test_coherence_integration.py::test_finding_format_is_locked` | **AVOIDED** — three fields, LOCKED (`_common.py:31-42`). Duration is timed by the runner and carried on the *event*, never added to `Finding`. |

### Generated-count collateral

`ecosystem/doc-counts.md` pins `43 registered checks` / `19 pre-commit gates` / **`3033 collected`
tests**. Adding new test files moves the third. Regenerate with
`python scripts/gen_doc_counts.py --write` or the `doc_claims` check WARNs. Neither of the first
two numbers moves — no check, no hook is added.

### Two gates that are NOT in the blast radius (checked, not assumed)

* **`check_silent_rule_ratchet`** — `silent_rule_detector.py:117` scopes to `protocols/*.md`,
  `templates/**/*.{md,tmpl}`, `ecosystem/*.yaml`. `scripts/` docstrings are out of scope, so
  wiring prose cannot move the 441 baseline. Editing the two `.claude/commands/*.md` files for
  `[#530]` is also out of scope (`.claude/` is not a scope root).
* **`check_import_edges`** — despite the name it walks Claude-Code `@import` targets from
  `CLAUDE.md` (`audit.py:2002-2009`), **not** Python imports. A new `audit.py → telemetry_emit`
  edge is invisible to it. There is no `tach.toml` in the tree (`ls` → absent), so no layer
  contract to satisfy either.

**In the radius:** `codemap-freshness` fires on `^scripts/.*\.py$`, and the codemap records
intra-source import edges (`scripts/codemap/ast_walker.py:10`). Adding
`audit.py → telemetry_emit` changes the generated block, so `python -m scripts.codemap.cli
generate . --source-root scripts --write` (or the repo's regen path) is part of the wiring
commit, not an afterthought.

---

## Item 4 — Test plan — **CLEAR**

**NEW files only.** `tests/test_audit.py` is the seam leg's and is not touched. Test-first: each
case written and RED before the corresponding wiring lands.

### `tests/test_telemetry_wiring.py` (NEW) — the `check_run` funnel

Every case uses an explicit `db_path` under `tmp_path`, which is also what proves the item-1
requirement is honoured.

1. **Emission happens.** `run_checks(tmp, checks=[c1,c2], parallel=False)` with telemetry on →
   the store holds exactly 2 `check_run` rows, named `c1`/`c2`.
2. **Parity — the load-bearing one.** Findings returned with telemetry **on** are field-by-field
   identical to findings returned with it **off**, serial and parallel. This is the
   unwired-behaviour parity the brief asks for, and it mirrors
   `test_audit_parallel.py:75/:219`.
3. **Emission order is `CHECK_ORDER`.** With descending sleeps (completion order reversed —
   the `test_audit_parallel.py:62` trick), `SELECT name FROM events ORDER BY id` still matches
   registry order.
4. **One row per check per run**, including a check that returns zero findings (which occupies
   no finding slot but is still a check that ran — `test_audit_parallel.py:102` is the analogue).
5. **A multi-finding check emits ONE event** carrying the aggregate status, not N.
6. **`duration_ms` is the check's own time, not its queue wait.** Under `parallel=True,
   workers=1` with a slow first check, the second check's `duration_ms` stays near its own
   sleep. This is the test that catches timing around `future.result()`.
7. **A dead store never breaks the run.** `db_path` pointed at an unwritable location → findings
   return normally, no exception (`safe_emit` at work).
8. **A worker exception still propagates** with telemetry on (`test_audit_parallel.py:165` must
   not be weakened by the wiring).
9. **Telemetry OFF is the default**, and off means zero rows.
10. **stderr stays clean** — run `cmd_health` via `CliRunner` with telemetry on and assert no
    `telemetry: ` line in the output. This is the regression test for the measured
    `audit.py:283` `basicConfig` finding, and it is the one item 3 explains cannot be delegated
    to the existing substring assertions.
11. **The store lands where the caller said**, not at `default_db_path()` — patch
    `audit._REPO_ROOT` at a tmp tree and assert nothing is written under the real `logs/`. This
    is the regression test for the seam finding.

### `tests/test_hook_telemetry.py` (NEW) — `hook_run` + `blocker_fired`

Driven as subprocesses with `DEV_KNOWLEDGE_TELEMETRY_DB` pointed at `tmp_path`, mirroring
`tests/test_block_ff_push.py`'s existing harness shape.

12. **`hook_run` on every exit path** — parametrized over the three organs × {allow, refuse}:
    a row lands with the right `name` and `outcome`.
13. **`blocker_fired` on refusal only**, carrying `context["reason"]`; zero on an allow.
14. **Exit codes are unchanged** — the refusal still exits 1, the allow 0, the internal error 2.
    Same assertions the existing hook tests make, re-made with telemetry on.
15. **stderr is byte-identical** with telemetry on vs off. (Expected to pass on the measured
    `lastResort` behaviour — this test is what keeps it true if a host ever configures logging.)
16. **A dead store never changes a verdict** — unwritable `db_path`, refusal still exits 1.
17. **Telemetry off by default** for the hooks too: no env var → zero rows, byte-identical stderr.

### `tests/test_single_flight_wiring.py` (NEW) — **only if** [#530] wiring is Python

If sites 5/6 stay markdown, this file is not written and the row records that "wiring" for
`[#530]` was documentation, not code — an honest outcome, not a shortfall.

18. If site 7 lands: `preflight_contract` reports a HELD lock as a finding and **never claims**
    (assert the ref is untouched after a preflight run).
19. If open leg (a) is fixed first: a generation-token `release` refuses to delete a lock it does
    not own — the ABA case, driven with the two-clone fixture at `test_single_flight.py:87-110`.

### Regeneration, as test-adjacent work

`python scripts/gen_doc_counts.py --write` after the new files land (collected-test count moves),
and the codemap regen noted in item 3. Both are gate-visible; neither is optional.

---

## Item 5 — Draft lane contract for L2 — **CLEAR**

House pattern taken from `docs/audits/2026-08-18-technical-533-leg2-lane-contract.md`. **This is
a draft for the operator to freeze, amend or discard — it is not itself a dispatch.**

```
# LANE L2 — [#529]/[#530] WIRING: telemetry emission + single-flight call sites

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — contract-is-the-plan, NO plan-mode | high |

> Fresh CC session (`/clear`). Worktree lane — you never touch the primary checkout and you
> NEVER merge. Commit-and-STOP.

**Worktree (STEP 0):** `claude --worktree lane-<L>-529-wiring --bg "[.dev-knowledge · #529/#530 ·
wire telemetry + single-flight] docs/audits/<this-contract>.md"` — branch name verified against
`scripts/validate_branch_naming.py` LANE_BRANCH_RE before provisioning.
**Governing rows:** `[#529]` open leg 1 (+ leg 2) and `[#530]` call sites ONLY. Closing these
legs does NOT close either row: `[#529]` leg 3 (structlog) and `[#530]`'s two defect legs stay
open unless explicitly taken below.
**ADR-110:** save this prompt as `docs/audits/<YYYY-MM-DD>-technical-529-530-wiring-lane-
contract.md` and COMMIT it as your first commit.
**Serialize-group `audit-py`:** you land AFTER `[#533]` leg 2 (`f4a01f0e`). Read
`scripts/audit.py:3553 run_checks` as it now exists — the single funnel is the whole reason this
lane is small.
**Spec of record:** `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md` (night N1).
Its item 1 carries two MEASURED blockers you must handle, not rediscover.

## PINNED-BY-TESTS (do not detach)
- `tests/test_audit.py` — **DO NOT TOUCH THIS FILE AT ALL.** Seam leg's. New tests go in NEW
  files only.
- `tests/test_audit_parallel.py` — 18 `run_checks` call sites. Must stay green **unedited**.
  Byte-identical serial-vs-parallel (`:75`, `:219`), exception propagation (`:165`), serial
  default on the calling thread (`:116`), live-registry read at call time (`:191`).
- `tests/test_ship_gate.py:118 test_ship_gate_is_readonly` — currently CANNOT see a telemetry
  write (it watches only `aud._REPO_ROOT`'s tmp tree). Passing an explicit `db_path=` is what
  makes it meaningful. Do not "fix" it by editing the test.
- `tests/test_block_ff_push.py` / `test_block_commit_on_main.py` /
  `test_adr85_integration_enforcement.py` — exit codes and stderr substrings. Codes must not move.
- `audit_checks/registry.py` CHECK_ORDER — emission order == registry order == finding order.
- `tests/test_telemetry_emit.py`, `tests/test_single_flight.py` — leave both libraries' tests
  untouched unless you take a library fix, in which case say so in the packet.

## UNDERSTAND
- Problem: `[#529]` and `[#530]` are BUILT-UNWIRED — zero non-test import sites. The gate mesh
  measures nothing about itself, and the dispatch guard guards nothing.
- Two MEASURED blockers from the spec, both real, neither optional:
  (1) `audit.py:283` calls `logging.basicConfig(level=INFO)` at module scope, and
      `telemetry_emit._log_event` logs at INFO -> 43 `telemetry: {…}` stderr lines per
      `audit.py health`, on a per-commit gate. Fix caller-side (set the `telemetry` logger to
      WARNING), NOT in the library — the library fix would touch pinned tests.
  (2) `telemetry_emit._REPO_ROOT` is independent of `audit._REPO_ROOT`, so the test sandbox seam
      does not reach the store. EVERY call site passes an explicit `db_path=` derived from its
      own caller's repo root. This also discharges the row's terra P1 worktree note.
- `[#530]` risk: wiring `release` activates open leg (a) — the ABA race that deletes another
  lane's LIVE lock. Wire `claim` + `inspect` only, OR fix (a) first. Do not wire `release` onto
  an unfixed (a).
- Scope: `scripts/audit.py`, `scripts/block_ff_push.py`, `scripts/block_unanchored_push.py`,
  `scripts/block_commit_on_main.py`, `.gitignore`, `.claude/commands/{lane-boot,lane-integrate}.md`,
  NEW `tests/test_telemetry_wiring.py`, NEW `tests/test_hook_telemetry.py`. Nothing else.
- Collateral both gate-visible: `codemap-freshness` fires on the new import edge (regen), and
  `ecosystem/doc-counts.md`'s collected-test count moves (`gen_doc_counts.py --write`).

## STEPS
**STEP 0 — worktree + contract commit** (above). `COMMIT`

**STEP 1 — DECIDE AND RECORD THE OUTCOME MAPPING, before any code.** `Finding.status` is a
5-value enum; `telemetry_emit.OUTCOMES` is 3, and `emit_event` REFUSES an unknown outcome.
Proposed: fail->block; pass/warn/n/a/unavailable->pass; a raising check->error; the collapsed
detail rides `context`. Multi-finding check => ONE event with the aggregate. Write the decision
into the lane artifact. **Fork (report, don't improvise):** if you judge the collapse loses a
signal the memo needs, STOP-report — extending EVENT_TYPES/OUTCOMES is Stage 2, not this lane.
`COMMIT`

**STEP 2 — TEST-FIRST: `tests/test_telemetry_wiring.py` (NEW).** Spec item 4 cases 1-11, RED
before any wiring. Cases 2 (parity), 10 (stderr clean) and 11 (store lands where the caller
said) are the load-bearing three — write them first. `COMMIT`

**STEP 3 — wire `check_run` at `audit.py:3553 run_checks`.** Serial branch `:3583-3586` and
parallel branch `:3590-3593`; time INSIDE the worker, emit AFTER the slot flatten in registry
order. Explicit `db_path=`. `--telemetry/--no-telemetry` click option, default **OFF**, named
constant not an inline literal (follow `_PARALLEL_MAX_WORKERS` at `:3540`). Set the `telemetry`
logger to WARNING at the wiring site. Green STEP 2. `COMMIT`

**STEP 4 — TEST-FIRST: `tests/test_hook_telemetry.py` (NEW).** Spec item 4 cases 12-17, RED
first. `COMMIT`

**STEP 5 — wire `hook_run` + `blocker_fired`** at `block_ff_push.py:222`,
`block_unanchored_push.py:79`, `block_commit_on_main.py:133` — every exit path gets `hook_run`,
the refusal returns additionally get `blocker_fired`. `safe_emit` everywhere; env-var switch,
default off. Exit codes unchanged. Green STEP 4. `COMMIT`

**STEP 6 — `.gitignore logs/TELEMETRY.db*`** — the GLOB, not the bare name: WAL leaves `-wal`
and `-shm` sidecars behind a crashed writer (measured), and a stray one trips session-end
backpressure. `[#529]` leg 2. `COMMIT`

**STEP 7 — `[#530]` call sites.** `.claude/commands/lane-boot.md` §1 (after the branch-name
check at `:22-26`): a `claim` step. `.claude/commands/lane-integrate.md` §3: `release` as a 6th
refuse-to-finish row — **only if** open leg (a) is fixed; otherwise wire `inspect` there and
state the deferral in the packet. Report which arm you took. `COMMIT`

**STEP 8 — regenerate what the wiring moved.** Codemap (new import edge) and
`gen_doc_counts.py --write` (collected-test count). Both are pre-commit-gated; neither is
optional. `COMMIT`

**STEP 9 — RECORDED GATE RUN (the Done-when leg).** One `audit.py health --telemetry` on the
lane, then read the store back with `sqlite3` WITHOUT re-measuring anything. Paste the row count,
the distinct check names, and 3 sample rows into the lane artifact. That readback IS `[#529]`'s
"a recorded gate run reads back without re-measurement". `COMMIT`

## FINAL
Targeted, `-n 0` (in-lane tests are always `-n 0`): the two NEW files +
`tests/test_audit_parallel.py` + `tests/test_ship_gate.py` + `tests/test_block_ff_push.py` +
`tests/test_block_commit_on_main.py` + `tests/test_adr85_integration_enforcement.py` +
`tests/test_telemetry_emit.py` + `tests/test_writer_integrity.py`. All green ->
**commit-and-STOP.** STOP packet: outcome-mapping decision · which `[#530]` arm was taken · the
STEP-9 readback · files touched · every fork taken.
**NO merge, no push to main, no touching the primary checkout.**

## WHAT NOT TO DO
No edits to `tests/test_audit.py` · no edits to `tests/test_audit_parallel.py` (green unedited) ·
no new dependencies (structlog stays undeclared; `[#529]` leg 3 stays open) · no new
EVENT_TYPES/OUTCOMES values (Stage 2, not this lane) · no new YAML config file (ADR-101 Rule A/C
— operator ruling) · no `Finding` field additions (LOCKED shape) · no hook-default flip (default
OFF; flipping is a separate ruling) · no wiring `release` onto an unfixed open leg (a) · no
`--no-verify` · no `git add -A` · no merge.
```

---

## Commands verbatim — everything this lane ran that L2 may want to re-run

```bash
# environment state (the honesty header)
uv run --frozen pytest --collect-only -q
python -m pytest --collect-only -q
python -m pre_commit --version
ls -la .git/hooks/ | grep -v sample
python --version; ruff --version
grep -n 'requires-python' pyproject.toml

# built-unwired proof
grep -rn 'telemetry_emit\|single_flight' --include=*.py --include=*.md --include=*.yaml \
  --include=*.yml --include=*.toml --include=*.json . | grep -v '\.git/'

# the runner as it now exists (post-f4a01f0e)
git diff 7a31697 f4a01f0e -- scripts/audit.py
grep -n 'def run_checks\|run_checks(\|_PARALLEL_MAX_WORKERS\|ALL_CHECKS =\|def cmd_health\|def cmd_ship_gate' scripts/audit.py
sed -n '3576,3596p' scripts/audit.py

# hook exit points
for f in block_ff_push block_unanchored_push block_commit_on_main; do
  grep -n 'def main\|return [0-9]' scripts/$f.py; done

# the two MEASURED blockers
sed -n '283p' scripts/audit.py
python -c 'import logging,json; logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO); logging.getLogger("telemetry").info(json.dumps({"event_type":"check_run","name":"doc_claims","outcome":"pass"}, sort_keys=True))'
python -c 'import logging; logging.basicConfig(level=logging.INFO); print(logging.getLogger().handlers[0].stream.name)'
python -c 'import logging,json; logging.getLogger("telemetry").info(json.dumps({"x":1}))'   # hook case: silent
grep -n '_REPO_ROOT' scripts/audit.py | head -3
sed -n '110p;266,275p' scripts/telemetry_emit.py
sed -n '112,130p' tests/test_ship_gate.py

# the WAL sidecar measurement (.gitignore leg)
python -c "
import sqlite3, os, tempfile
d = tempfile.mkdtemp(); p = os.path.join(d,'TELEMETRY.db')
c = sqlite3.connect(p)
for k,v in (('journal_mode','WAL'),('synchronous','NORMAL'),('busy_timeout','5000')): c.execute(f'PRAGMA {k}={v}')
c.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, ts TEXT)')
c.execute(\"INSERT INTO events (ts) VALUES ('now')\"); c.commit()
print('OPEN: ', sorted(os.listdir(d))); c.close(); print('CLOSED:', sorted(os.listdir(d)))"

# pinned-by-tests sweep
grep -rn 'run_checks' tests/
grep -rln 'ALL_CHECKS' tests/
grep -n 'def test_' tests/test_audit_parallel.py tests/test_telemetry_emit.py tests/test_single_flight.py
grep -n 'cmd_health' tests/test_audit.py
grep -n 'def test_\|returncode\|stderr' tests/test_block_ff_push.py

# gates checked and found OUT of the blast radius
grep -n 'SCOPE_GLOBS' scripts/silent_rule_detector.py
grep -n -A8 'def check_import_edges' scripts/audit.py
ls tach.toml
grep -n 'codemap-freshness' -A4 .pre-commit-config.yaml
cat ecosystem/doc-counts.md
```

---

## STOP packet

```
ITEM 1  Call-site derivation ......... CLEAR — 7 sites named with file:line + why. check_run: ONE
        funnel (audit.py:3553 run_checks, serial :3583-3586 + parallel :3590-3593, emit after the
        :3594 flatten). hook_run/blocker_fired: 3 organs (block_ff_push.py:222,
        block_unanchored_push.py:79, block_commit_on_main.py:133) at their enumerated exits.
        single_flight: lane-boot.md §1 claim, lane-integrate.md §3 release, preflight_contract.py:401
        inspect (optional). TWO MEASURED BLOCKERS surfaced: audit.py:283 basicConfig sends 43
        telemetry lines/run to stderr on a per-commit gate; telemetry_emit._REPO_ROOT is independent
        of audit._REPO_ROOT so the test sandbox seam does not reach the store (and
        test_ship_gate_is_readonly passes for the wrong reason). Both have stated fixes.
ITEM 2  Config surface .............. CLEAR, with an honest negative — no runtime-knobs YAML exists
        in this repo, and creating one needs ADR-101 Rule A/C sanction (operator ruling, not a
        lane's). Recommendation: reuse the precedent audit.py set one commit ago — named module
        constant + click option (--telemetry/--no-telemetry, default OFF), env-var switch for the
        hooks. Destination already configurable (DEV_KNOWLEDGE_TELEMETRY_DB + db_path=); flight
        scope already configurable (--remote/--local-only). Nothing hardcoded.
ITEM 3  PINNED-BY-TESTS ............. CLEAR — 6 touched surfaces + 5 avoided, per-pin verdicts,
        with the 28-file ALL_CHECKS monkeypatch sweep enumerated. Two gates checked and ruled OUT
        of the blast radius (silent_rule_ratchet scopes to protocols/templates/ecosystem, not
        scripts/; check_import_edges reads @import not Python imports; no tach.toml). IN the
        radius: codemap-freshness (new import edge) + doc-counts collected-test count.
        UNVERIFIED BY EXECUTION — no pytest in this environment; all rows are source reads.
ITEM 4  Test plan ................... CLEAR — 19 test-first cases across 2 NEW files
        (tests/test_telemetry_wiring.py, tests/test_hook_telemetry.py) + 1 conditional
        (tests/test_single_flight_wiring.py). Covers emission, single-flight dedupe, and
        unwired-behaviour parity. tests/test_audit.py untouched, tests/test_audit_parallel.py
        green-unedited.
ITEM 5  Draft lane contract ......... CLEAR — full house-pattern contract as a fenced block:
        frozen contract header, PINNED-BY-TESTS, UNDERSTAND, STEPS 0-9 each with a COMMIT marker,
        a STEP-1 decision-budget fork, FINAL, and WHAT NOT TO DO (11 refusals).

SHAS    dispatch stamp  12cc4c6   docs/audits/2026-08-19-technical-n1-wiring-spec-contract.md
        deliverable     <this commit>
        tree read at    87dd41a   (contains f4a01f0e, the [#533] leg-2 merge)
        branch          claude/wiring-spec-telemetry-flight-o7oja9

SCOPE   No wiring performed. No dependency changes. No adoption verdicts. No merge. No scripts/
        edits. No BACKLOG/tasks writes. Two files added, both under docs/audits/.
```
