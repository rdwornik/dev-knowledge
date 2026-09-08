# LANE lane-v-643-enforcement-debt — Build the checks that were claimed but never written: the two-stage P11 carriage predicate, the empty-PROBES bypass, a falsifiable retention test, and an unattended suite path that reproduces the baseline.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-643-enforcement-debt LANE-v-643-enforcement-debt.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #643 · lane-v-643-enforcement-debt]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-643-enforcement-debt` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-643-enforcement-debt` -> branch `worktree-lane-v-643-enforcement-debt` -> contract `LANE-v-643-enforcement-debt.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- `scripts/gen_handoff.py` — the PREFLIGHT REFUSAL functions only (see pins)
- `scripts/assemble_paste.py` (the leg-2 assemble gate)
- `scripts/verify_handoff_probes.py` (empty-PROBES = FAIL)
- `tests/test_logs_retention.py`, `scripts/logs_retention.py`, `logs/PROPOSALS-*`
- `pyproject.toml` — the `pytest-timeout` dependency + the unattended invocation path

**Pinned OUT — another lane owns these, or nobody does:**

- `scripts/gen_handoff.py` — V-6 owns the SEAT-BOOT **render** hook in the same file. Disjoint functions, same wave: stay out of V-6's render function, and `git merge origin/main` BEFORE your HANDBACK (step-0 coupling scan C2, batch-U C4 precedent).
- the `carried-by:` WRITE-TIME refusal is **V-6's**, not this lane's (coupling scan C3)
- `addopts` for the INTERACTIVE path — do not change it
- the four `proof_layer` WARNs — `[#638]` owns them; do not suppress

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **The predicate does not exist yet — this lane BUILDS it, it does not move it.** AMEND-643-001 measured it and the dispatcher re-measured at step 0: `grep -rl 'carried-by' scripts/` returns `file_purpose_graph.py` ONLY. Nothing in `verify_handoff_probes.py` opens a transport file.
- **Locators resolved at step 0:** `tests/test_logs_retention.py:264` -> `test_the_repos_own_logs_dir_is_allowed`, whose body is `assert mod.run_retention(...) is not None` — the unfalsifiable assertion named in the intent. `run_retention()` -> `scripts/logs_retention.py:213`. Flat `logs/PROPOSALS-*` counted: **154**, matching the intent exactly.

## Done-contract (immutable)

1. **`[#643]` Done-when, verbatim:** leg 1 is a `preflight_rows` row that REFUSES the cut, with a RED-first test per ADR-108 §B proving a missing/unresolvable flush-left key blocks `generate()` before it writes; AND leg 2 is a distinct assemble-time gate proving an `OPEN` carrier absent from the filled residual blocks assembly; AND both cite `DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08` / `DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08` as the family precedent for where a handoff refuses debt; AND `.claude/commands/handoff.md` states the two-stage split so a seat is not told a single row covers both.
2. P11 fixture **7 FAIL -> 0** on the seven-file short.
3. tests-that-cannot-fail **>=1 -> 0** (`tests/test_logs_retention.py` line ~264 is the first).
4. flat `logs/PROPOSALS-*` **154 -> 0** (the dispatcher measured 154 at step 0).
5. an unattended run reproduces the baseline **28 RED, not 44**.
6. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. PLAN round: the two-stage P11 gating design, and where the unattended path lives. Those are the TWO budgeted forks. Propose the `pytest-timeout` per-test value here.
2. RED first (ADR-108 §B): the seven-file short is the fixture — prove 7 FAIL before writing the predicate. **COMMIT**
3. Leg (a): flush-left `carried-by:` in HEAD + value resolves on `main` -> a `preflight_rows` row that REFUSES the cut. **Mind the leg ORDER** — several live files carry prose paths that resolve while their stated value is literal `OPEN`; a path-first read under-counts the OPEN set (this is how the `-1` run read 7 as 2). **COMMIT**
4. Leg (b): zero PROBES rows = FAIL, not pass. **COMMIT**
5. Leg (d): make `test_logs_retention.py` falsifiable, give `run_retention()` a production caller, sweep the 154 flat `logs/PROPOSALS-*`. **COMMIT**
6. Leg (e): an unattended path that cannot inherit the committed `-n auto` AND passes `--group analytics`. Add `pytest-timeout` (operator-approved 2026-09-08). **COMMIT**
7. Witness the unattended run reproducing 28 RED; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Do not change `addopts` for the interactive path.
- Do not build the declared-enforcement meta-check (AMEND-002 D1 — spike now, fix in V+1).
- Do not suppress the four `proof_layer` WARNs.
- Do not add `pytest-timeout` AND touch `addopts` — the dependency only, plus a proposed value.
- Do not build the `carried-by:` write-time refusal — V-6 owns it.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- `to-cc/AMEND-643-001.md`
- HANDOVER-NOTE §A
- `[#643]` · `tasks/643-preflight-reports-p11-carriage-instead-of-refusing.md`
- `to-cc/SUITE-ANALYTICS-CODESPACES-2026-09-08.log`
- `pyproject.toml:9`

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*
