# Lane M packet — [#529] telemetry v1 EMIT (library only)

**T_start (dispatch):** `2026-08-15T14:33:27Z`
**Branch:** `worktree-lane-m-529-telemetry-emit` (worktree `.claude/worktrees/lane-m-529-telemetry-emit`)
**Base:** `d62796ad` · **HEAD:** `0189aaa6` · **Working tree:** clean · **Merged:** no (commit-and-STOP)
**Contract of record:** `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-contract.md`

## 1. Manifest as executed

| File | Declared at step 0 | As executed |
|---|---|---|
| `scripts/telemetry_emit.py` | new module | new, 472 lines |
| `tests/test_telemetry_emit.py` | new test file | new, 408 lines |
| `docs/audits/2026-08-15-…-lane-contract.md` | step-0 contract of record | added |
| `docs/audits/README.md` | audit-index regen (contract-excluded surface) | 1 line |

`git diff --stat d62796ad..HEAD` = 4 files, 945 insertions, 1 deletion. Nothing outside the
manifest and its named exclusions was touched — in particular not `scripts/audit.py`, no hook or
dispatcher script, not `pyproject.toml` / `uv.lock`, not `BACKLOG.md` / `tasks/529-*.md`, not
`.gitignore`, not `CLAUDE.md` / `ARCHITECTURE.md`, and no `[#id]` was born.

## 2. Per-step commits

| Step | SHA | Subject |
|---|---|---|
| 0 — contract of record | `73831a9e` | `docs(audits): [#529] telemetry-emit lane — contract of record (I-D3, step 0)` |
| 1 — schema + writer | `b4b0f13e` | `feat(telemetry): [#529] step 1 — Stage-1 schema + WAL writer + emit helper` |
| 2 — correctness constraints | `ac759725` | `feat(telemetry): [#529] step 2 — the three binding correctness constraints` |
| 3 — tests | `0189aaa6` | `test(telemetry): [#529] step 3 — 30 targeted tests, firing not presence` |

The step-0 commit body carries the name derivation the contract asked to be quoted:
`<domain>_<role>` snake_case from the sibling modules (`fleet_analytics.py`,
`enforcement_coverage.py`, `window_metrics.py`, `desired_state_loader.py`, `journal_anchor.py`,
`silent_rule_detector.py`), hyphen-free because `pyproject.toml`
`[tool.pytest.ini_options] pythonpath = [".", "scripts", "deploy"]` exists so that "a test file
imports `audit` / `tool` / `carrier_precommit` **by bare name**" — and a bare-name import needs a
valid Python identifier. That comment block is the quoted pattern source.

## 3. Targeted-test evidence

Tiered suite law honoured: this lane ran its own test file only. No full-suite run.

```
uv run --locked pytest tests/test_telemetry_emit.py -n 0 -q   ->  30 passed in 9.13s
uv run --locked pytest tests/test_telemetry_emit.py -q        ->  30 passed in 9.88s   (repo default -n auto)
uv run --locked ruff check scripts/telemetry_emit.py tests/test_telemetry_emit.py  ->  All checks passed!
uv run --locked python scripts/audit.py health                ->  health: OK
uv run --locked python scripts/worktree_import_proof.py --repo .  ->  NOT-APPLICABLE (hub declares no importable package)
```

Both pytest spellings are recorded because the repo default is `-n auto`: green under the default
alone would not distinguish a real pass from an xdist artifact. Every commit passed the live
pre-commit set — `audit-health`, `ruff`, `validate-hermetization`, `audit-index-freshness`,
`codemap-freshness`, `backlog-id-on-close` and `backlog-filing-backpressure` each fired.

Evidence beyond the counts, since a count is not a behaviour:

- **refuse-on-shallow** is proven against a REAL `git clone --depth 1` of a REAL seeded repo,
  and asserts both the refusal AND that the store file does not exist. Reproduced a second time
  outside pytest, against a `--depth 1` clone of this repository in the job tmp dir: `is-shallow`
  reports `true`, `ShallowRepositoryRefusal` raised, `no db file created`.
- **WAL concurrency** is four REAL concurrent processes × 15 events; all 60 rows land with
  distinct ids. Threads in one interpreter would prove something weaker than the memo's
  cross-process claim.
- **`unknown` not `0`** is asserted on the stored `context_json` in both directions, plus a third
  state (coverage not supplied at all → no key).
- **capability vector** asserts the exact key set and `bool` values only. Which tools this host
  happens to have is deliberately NOT pinned.

## 4. Call surface for the phase-3 wiring step

Import is by bare name (`scripts/` is on `pythonpath`):

```python
from telemetry_emit import emit_check_run, emit_hook_run, emit_blocker_fired, safe_emit

emit_check_run("journal_spine_anchor", "pass", duration_ms=812)
emit_hook_run("block-unanchored-push", "block", duration_ms=44)
emit_blocker_fired("block-unanchored-push", reason="range carries 3 unanchored entries")

safe_emit(emit_check_run, "no_ff_merges", "pass")     # never fails the host gate
```

| Symbol | Signature | For the wiring step |
|---|---|---|
| `emit_check_run` | `(name, outcome, duration_ms=None, **kw) -> int` | one call in the audit-check dispatcher |
| `emit_hook_run` | `(name, outcome, duration_ms=None, **kw) -> int` | one line per pre-commit / pre-push script |
| `emit_blocker_fired` | `(name, reason, **kw) -> int` | at each non-zero (refusing) exit; `outcome` is fixed to `block` |
| `emit_event` | `(event_type, name, outcome=None, duration_ms=None, context=None, db_path=None, ts=None, git_derived=False, coverage=_UNSET, skipped=None, repo_path=None) -> int` | the general form the three wrap |
| `safe_emit` | `(emitter, *a, **kw) -> int \| None` | wrap any call on a gate's critical path |
| `connect` | `(db_path=None)` context manager | read-back / maintenance; applies the pragmas |
| `default_db_path` | `() -> Path` | `$DEV_KNOWLEDGE_TELEMETRY_DB`, else `<repo>/logs/TELEMETRY.db` |
| `capability_vector` | `() -> dict[str, bool]` | git / grep / pre-commit / powershell / pandas |
| `coverage_value` | `(int \| None) -> int \| "unknown"` | constraint-2 normalizer |
| `is_shallow_repository` | `(repo_path=None) -> bool \| None` | tri-state; `None` = could not determine |
| `assert_not_shallow` | `(repo_path=None) -> None` | raises `ShallowRepositoryRefusal` |
| `logger_backend` | `() -> "structlog" \| "stdlib-logging"` | which side-channel is live (see D1) |
| `EVENT_TYPES` / `OUTCOMES` / `WAL_PRAGMAS` / `CAPABILITY_PROBES` / `UNKNOWN` | constants | assert against these, don't re-spell them |

Refusal contract the wiring step inherits: `TelemetryError` (unknown event type / outcome, empty
name, unserializable context, a raw `coverage` or skip key in `context`) and
`ShallowRepositoryRefusal` both propagate through `safe_emit`; only `sqlite3.Error` / `OSError`
are swallowed. A wiring defect and a fired constraint are meant to be visible; a locked database
is not worth failing a commit over.

The three constraints are reached from the wiring site as keyword arguments — `git_derived=True`,
`coverage=None`, `skipped=<n>` — and each is ALSO refused at the raw-context door, so a site that
spells the field by hand cannot bypass the normalizer or the vector.

## 5. Which memo lines each event maps to

Memo: `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`.

| Element | Memo line | What the line says (condensed) |
|---|---|---|
| `check_run` | **82** | each audit check fires: `name`, `outcome` (pass/block/error), `duration_ms` → retire checks with fires>0/blocks=0 |
| `hook_run` | **83** | each git hook (pre-commit/pre-push) fires: `name`, `outcome` → is a hook pure ceremony? |
| `blocker_fired` | **84** | any gate that refuses an action, with reason in `context` → guardrail efficacy |
| `outcome` enum | **36**, **82** | "you want `outcome ∈ {pass, block}` per fire"; `error` is the third (a crashed check is neither) |
| `context` freeform | **38** | "a freeform `context` field helps disambiguate later" |
| table `events(...)` | **79** | `events(id, ts, event_type, name, outcome, duration_ms, context_json)` |
| WAL + the 3 pragmas | **52** | "Set `journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=5000`" |
| WAL concurrency claim | **15** | "readers do not block writers and a writer does not block readers" |
| structlog emit helper | **54**, **96** | structlog preferred; stdlib `logging` named as the least-deps fallback; "~40 lines: `emit_event()` helper + WAL pragmas" |
| scope = Stage 1 only | **132** | "Add `emit_event()` … and wire `check_run`, `hook_run`, and `blocker_fired`. **Ship nothing else yet.**" |

Deliberately NOT built, each with the memo line that defers it: the `(event_type, ts)` index
(**141** — gated behind "millions of rows or query latency degrades", a condition that does not
hold); the 90-day retention prune (**93** — a maintenance check, Stage 2); the read surfaces
`dispatch report` + Datasette (**91**, Stage 3); the five Stage-2/3 event types
`dispatch_invoked` / `agent_session` / `test_run` / `mutation_run` / `dep_scan` (**85–89**).
Memo line **152** ("WAL does not work over a network filesystem") is why the store default is a
local `logs/` path and not a synced drive.

## 6. Deviations — self-reported

**D1 — structlog is OPTIONAL, not a declared dependency. This is the one that needs an operator
decision.** The memo (line 54) and the `[#529]` row both name structlog for the emit helper. It is
absent from `pyproject.toml` `[dependency-groups]` and from `uv.lock`, and `pyproject.toml` is not
in this lane's owned-files manifest; declaring a dependency is separately confirmation-gated. Three
rules pointed the same way, so this was decided rather than escalated. The structured-log
side-channel therefore binds structlog **when importable** and otherwise falls back to the option
the memo names on that same line — stdlib `logging` emitting one JSON object per event.
`logger_backend()` reports which is live; **measured on this host: `stdlib-logging`**. No event is
lost either way: the SQLite row is the durable record and the log line is a mirror. Adding
structlog for real is an open, separate decision the integrator or a later row owns.

**D2 — no JOURNAL entry on this branch.** `/lane-boot` §6 says to write one; the contract's
owned-files manifest does not include `JOURNAL.md` and says "you modify NOTHING outside it". The
manifest is the narrower, later instruction and matches the batch convention that a lane does not
journal — the integrator anchors the batch. Flagged rather than silently skipped.

**D3 — `docs/audits/README.md` modified.** The audit-index regen, explicitly excluded from the
manifest by the contract's own file-discipline line. Regenerated with
`gen_audit_index.py --write` after `git add` of the new audit (the index reads tracked files only).

**D4 — an instrument defect was found and fixed inside step 3, recorded because it fails loudly
but misleadingly.** The broken-side-channel test first monkeypatched stdlib `logging.getLogger`
via the module alias `te.logging`. That is the real stdlib module, so the patch took down pytest's
own logging plugin and killed an xdist worker: `INTERNALERROR`, `KeyError: <WorkerController
gw12>`, reported as `1 failed / 21 passed / 1 error` with the named failure pointing nowhere near
the cause. Fixed by patching the `logging` NAME inside `telemetry_emit`, which is the seam the test
meant. Worth a gotcha: **patching a stdlib module attribute through a module alias is a global
patch, and under xdist it kills the worker rather than failing the test.**

**D5 — `@pytest.mark.slow` used on the three real-git / real-subprocess tests**, per the repo's
#317 marker tier. There is no conftest deselecting `slow`, so they run in a default invocation;
the marker labels cost honestly rather than hiding it.

**No stop-and-report conditions were hit.** No curated baseline was touched, no rule-vs-ruling
conflict arose that the manifest did not settle, and no fork class lacked a standing precedent —
including the Layer-2 write question, where four live in-repo instances (`logs/FLEET-HEALTH.md`,
`logs/ENFORCEMENT-COVERAGE.md`, `logs/COHERENCE-NUDGE.log`, `logs/PARITY-EVENTS.jsonl`) already
establish the local-ephemeral-artifact pattern this store joins.

## 7. Owed after this lane — [#529] does NOT close here

The contract narrowed this lane to the emit library. Three of the row's Done-when legs are
therefore untouched by design, and the row stays open:

1. **Wire the call sites (the owed phase-3 step).** The audit-check dispatcher, the pre-commit /
   pre-push scripts, and each refusing exit. Until then a grep for `telemetry_emit` outside the
   module and its test returns nothing — that is the state of the slice, not a defect in it.
2. **`.gitignore` needs `logs/TELEMETRY.db`.** Concrete and load-bearing: the first live emit
   after wiring leaves an untracked file in the tree, which dirties `git status` and trips
   session-end backpressure. The line belongs with the wiring commit, alongside the existing
   ephemeral-artifact entries. This lane did not add it because `.gitignore` is outside the
   manifest and nothing in the tree writes the store yet.
3. **Decide structlog** (D1) — declare it in `[dependency-groups]` and regenerate `uv.lock`, or
   record that `stdlib-logging` is the accepted backend.
4. **The row's last two legs** — "the three stage-1 events emit from **live gate runs**" and "a
   recorded gate run **reads back** without re-measurement" — are phase-3 and Stage-3 work
   respectively, not this lane's.

**Integrator precondition, noted not acted on:** no `docs/audits/*-batch-*-manifest.md` for
2026-08-15 is committed on `main` as of `d62796ad`. A batch without a committed manifest is
unintegrable under the ADR-110 exemption key, so that is worth resolving before the merge queue
opens. Filing one is outside this lane's manifest, so this lane reports it rather than creating it.

---

**STOPPED.**
