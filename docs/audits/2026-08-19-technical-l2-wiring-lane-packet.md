# LANE L2 packet — [#529]/[#530] wiring

**Lane:** L2 · branch `worktree-lane-l-529-wiring` · contract-of-record `b2abedb8`
**Contract body:** item 5 of `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md`
**Status:** written incrementally as the lane proceeds; frozen at STOP.

---

## Environment honesty header — WHICH GATES RAN HERE (measured, not assumed)

N1's own header recorded that it ran with no gates at all. This lane is the opposite, and that
is the whole point of amendment 3:

```
$ python --version                          -> Python 3.12.10   (>= the >=3.12 floor: OK)
$ uv --version                              -> uv 0.11.19       (== the pinned uv: OK)
$ .venv/Scripts/python -c 'import pytest'   -> pytest 9.1.1     (suite runnable)
$ SessionStart arm_hooks                    -> pre-commit / commit-msg / pre-push installed
```

Every commit in this lane goes through the live pre-commit gate set (`audit-health`, `ruff`,
`validate-hermetization`, `block-commit-on-main`, the freshness/index gates, and the two
commit-msg gates). No `--no-verify` and no `SKIP=` anywhere in this lane.

---

## Amendment 3 — UNVERIFIED to verdict log

Every row below is one the N1 spec derived by reading the tree with no pytest and no gates.
Re-verified here on the real toolchain BEFORE acting on it. `CONFIRMED` = the claim holds as
written; `CORRECTED` = it does not, with what is true instead.

| # | Spec claim | Verdict | Evidence |
|---|---|---|---|
| U1 | `audit.py:3553 run_checks` is the single funnel; three callers `audit_repo`/`cmd_health`/`cmd_ship_gate` | **CONFIRMED** | `grep -n 'def run_checks'` -> 3553; callers at 3597 / 4127 / 4234 |
| U2 | serial branch `:3583-3586`, parallel `:3590-3593`, flatten at `:3594` | **CONFIRMED (1-line drift)** | live: `if not parallel` 3582, `out.extend` 3585; parallel 3590-3593 exact; flatten `return [f for slot ...]` 3594 exact. The drift is the branch's opening line, not a different site |
| U3 | `Finding.status` is a 5-value enum; `telemetry_emit.OUTCOMES` is 3; `emit_event` REFUSES an unknown outcome | **CONFIRMED** | `_common.py:44` field comment + docstring; `OUTCOMES` at `telemetry_emit.py:135`; the refusal is `emit_event`'s 2nd guard |
| U4 | hook `main()` at `block_ff_push:222`, `block_unanchored_push:79`, `block_commit_on_main:133`, with the enumerated exit lines | **CONFIRMED, exactly** | `grep -n 'def main\|return [0-9]'`: 222 / 241,255,257,271 · 79 / 95,103,110,112,123 · 133 / 138,143,154 — every number as written |
| U5 | `emit_blocker_fired` hard-fixes `outcome="block"`, so a refusal emits BOTH a `hook_run(block)` and a `blocker_fired` | **CONFIRMED** | `telemetry_emit.py:447-457`; the double-count is recorded as a deliberate shape below |
| U6 | `telemetry_emit._REPO_ROOT` is independent of `audit._REPO_ROOT`; `default_db_path()` reads the former | **CONFIRMED** | `telemetry_emit.py:110` vs `audit.py:70`; `default_db_path()` returns `_REPO_ROOT / DEFAULT_DB_RELPATH` |
| U7 | `test_ship_gate_is_readonly` watches only the tmp tree `aud._REPO_ROOT` points at, so it cannot see a telemetry write | **CONFIRMED** | `tests/test_ship_gate.py:118-128`: `monkeypatch.setattr(aud,"_REPO_ROOT",str(repo))` then `repo.rglob("*")` before/after |
| U8 | `audit.py:283` `logging.basicConfig(level=INFO)` at module scope + `_log_event` at INFO gives telemetry lines on stderr | **CONFIRMED, re-measured here** | see "Blocker (a)" below — reproduced against the real modules on 3.12.10, not a synthetic snippet |
| U9 | the three hook scripts touch no `logging`, so `lastResort` (WARNING) keeps their stderr clean | **CONFIRMED** | `grep -n logging scripts/block_*.py` -> no match in any of the three |
| U10 | `safe_emit` swallows store/IO failure but NOT `TelemetryError` | **CONFIRMED** | `except (sqlite3.Error, OSError): return None` — nothing else caught |
| U11 | WAL leaves `-wal`/`-shm` sidecars, so the ignore must be the glob `logs/TELEMETRY.db*` | **CONFIRMED, re-measured here** | see STEP 6 evidence |
| U12 | `check_silent_rule_ratchet` scopes to `protocols/*.md`, `templates/**`, `ecosystem/*.yaml` — `scripts/` and `.claude/` are out | **CONFIRMED** | `silent_rule_detector.py` scope globs; baseline measured unchanged across this lane (STEP 7) |
| U13 | `check_import_edges` walks Claude-Code `@import` targets, not Python imports; no `tach.toml` | **CONFIRMED** | the check reads `CLAUDE.md` `@`-imports; `ls tach.toml` -> absent |
| U14 | **`codemap-freshness` fires on the new import edge, so a codemap regen is part of the wiring commit** | **CORRECTED — no regen is owed** | The live `ARCHITECTURE.md` CODEMAP block (`:162-173`) lists **packages only** (`codemap`, `toc`) and its Dependencies section is literally `- (none)`. `scripts/audit.py` and `scripts/telemetry_emit.py` are top-level modules, not packages, so neither is a node and an edge between them cannot appear. Verified by running the gate itself after the wiring landed (STEP 8). **This correction matters beyond tidiness:** `ARCHITECTURE.md` is in `_FRESHNESS_FILES`, so an unnecessary regen would have bumped its commit date past `last_reviewed: 2026-08-14` and RED-ed `canonical_freshness` A2 on the next commit — STEP 8 would have wedged the lane on a re-stamp nobody had earned. |
| U15 | `ecosystem/doc-counts.md` `3033 collected` moves when the new test files land | **CONFIRMED** | regenerated at STEP 8; before/after quoted there |
| U16 | `[#530]`: no Python dispatch entry point — `/lane-boot` §1 pre-flight `:22-26`, `/lane-integrate` §3 five-row table `:57-63` | **CONFIRMED** | `lane-boot.md` §1 ends with the `validate_branch_naming.py --lane` fence at 23-25; `lane-integrate.md` §3 table has exactly rows 1-5 under a "Run all five" lead-in |
| U17 | `single_flight` open leg (a) ABA in `release`, leg (b) `rev-parse` conflation at `:206-208` | **CONFIRMED** | `release()` reads `_local_holder` then deletes the remote ref unconditionally; `_local_holder` maps any non-zero return to `""` |

**No CORRECTED row changed the CONTRACT's shape**, so no STOP-report is owed. U14 removes work
(STEP 8's codemap half) rather than adding it; U2's one-line drift changes no site. Both are
applied as corrections and recorded here, per amendment 3.

---

## The two MEASURED blockers — re-measured HERE, against the real modules

N1 measured blocker (a) with a synthetic `logging.basicConfig` snippet, because it had no venv
to import the real modules into. This lane has one, so both were re-measured through the actual
code paths a wired gate would take. Both reproduce.

**Blocker (a) — `audit.py:283` puts telemetry on stderr.** Import `audit` (which runs
`basicConfig(level=INFO)` at module scope), then emit one event through the real library:

```
$ python -c "import sys; sys.path.insert(0,'scripts'); import audit, telemetry_emit as te; \
             te.emit_check_run('doc_claims','pass',12, db_path=<tmp>)"
RC: 0
STDOUT: ''
STDERR: 'telemetry: {"context_json": "{}", "duration_ms": 12, "event_type": "check_run",
          "name": "doc_claims", "outcome": "pass", "ts": "2026-08-19T10:42:57.693276+00:00"}\n'
```

One line per event, on stderr, on a per-commit gate that runs 43 checks. CONFIRMED.

**And the hook counterpart is clean, which is why the fix is caller-side.** The same emit without
importing `audit` produces nothing at all — `logging.lastResort` is WARNING-level, so an `.info()`
with no configured handler is silent:

```
$ python -c "import sys; sys.path.insert(0,'scripts'); import telemetry_emit as te; \
             te.emit_hook_run('block-ff-push','pass',3, db_path=<tmp>)"
RC: 0  STDOUT: ''  STDERR: ''
```

So the defect belongs to `audit.py`'s module-scope `basicConfig`, not to `telemetry_emit`. Fixing
it in the library would touch `test_emit_survives_an_unusable_log_side_channel` and
`test_logger_backend_reports_which_side_channel_is_live` — pinned tests, for a defect the library
does not have.

**Blocker (b) — the sandbox seam.** `telemetry_emit._REPO_ROOT` and `audit._REPO_ROOT` are
independent module-level values (U6), so monkeypatching the latter does not move the store. The
fix and its before/after are at STEP 3.

**U11 — the WAL sidecars**, re-measured through the real `telemetry_emit.connect()` rather than a
hand-rolled sqlite connection:

```
OPEN:   ['TELEMETRY.db', 'TELEMETRY.db-shm', 'TELEMETRY.db-wal']
CLOSED: ['TELEMETRY.db']
```

They vanish on a clean close and survive a crashed writer or a concurrent reader — which is the
state WAL exists to support here. The `.gitignore` leg therefore needs the glob (STEP 6).

---

## STEP 1 — the outcome mapping (DECIDED, not improvised)

`Finding.status` in {pass, fail, warn, unavailable, n/a} (5) must be projected onto
`telemetry_emit.OUTCOMES` in {pass, block, error} (3). `emit_event` raises `TelemetryError` on an
unknown outcome, and `safe_emit` deliberately does **not** swallow that class — so an improvised
mapping would not degrade quietly, it would crash the audit. The decision is therefore made once,
here, and pinned by a test rather than a comment.

**The mapping, as proposed by the contract and adopted unchanged:**

| `Finding.status` | event `outcome` | why |
|---|---|---|
| `fail` | `block` | the only status that stops a commit at `audit-health` and a ship at `ship-gate` |
| `pass`, `warn`, `n/a`, `unavailable` | `pass` | none of them refuses an action; a WARN informs, an `n/a`/`unavailable` did not evaluate |
| *(the check raised)* | `error` | a check that crashed is neither a pass nor a block — `OUTCOMES`' own reason for a third value |

**Aggregation: ONE event per check per run**, never one per finding. The check is the organ being
measured; its findings are its output. The collapsed detail rides `context`, so the read side
loses nothing:

```json
{"statuses": {"pass": 1, "warn": 2}, "findings": 3, "finding_names": ["doc_claims"]}
```

`finding_names` is this lane's one addition to the contract's proposed context shape, and it is
there for a concrete reason. The event's `name` is the check function's `__name__`
(`check_doc_claims`), because that is the only name a check with **zero findings** has — and the
contract's case 4 requires such a check to still emit a row. But the disposition register and the
ship-gate key on `Finding.check_name` (`doc_claims`), a different string. Carrying both means a
reader can join a `check_run` row to the register without re-deriving the relationship.

**Fork not taken.** The contract offers a STOP-report if the collapse loses a signal the memo
needs. It does not: the memo's two questions are *"retire checks with fires>0/blocks=0"* and
*"promote high-catch checks"*, and both are answered by fires-vs-blocks per check name, which is
exactly what this mapping preserves. Extending `EVENT_TYPES`/`OUTCOMES` is Stage 2 and is
explicitly refused by the contract's WHAT-NOT-TO-DO list.

**The `hook_run` + `blocker_fired` double-count is deliberate, and is recorded here so a reader
does not have to discover it.** A hook that refuses emits BOTH a `hook_run(outcome="block")` and
a `blocker_fired` — `emit_blocker_fired` hard-fixes `outcome="block"` (U5). They are separate
event types answering separate questions ("did this organ fire, and how did it end" vs "what did
this refusal say"), which is the memo's own shape. **A reader summing `outcome="block"` across
event types double-counts every refusal.** Count blocks from `check_run`/`hook_run`; count
refusal reasons from `blocker_fired`.
