# Shape-spec clause readers — which clause an organ actually OPENS

> Lane artifact for `lane-v-000-shape-spec-clauses` (batch V), against the frozen contract
> `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-000-shape-spec-clauses.md`.
> Executes the reader half of intake #73
> (`docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`), whose spec
> `ecosystem/fleet-shape-spec.yaml` states the fleet tree grammar as data. RED-first per
> ADR-108 §B; landed under ADR-110 lane discipline.

## Step 1 — the measurement (as of `33bcb0bd`)

**Question.** For each clause in `ecosystem/fleet-shape-spec.yaml`, does the organ its
`asserted_by` names actually OPEN the clause, or does it merely stand beside it?

**Method, and why it is not a grep.** A name-grep proves wiring, not reading. The clause
mapping returned by `validate_hermetization.load_shape_spec()` was wrapped in a `dict`
subclass that records every `__getitem__` / `get` key, substituted for the module-level
`SHAPE_SPEC`, and the module was re-executed from source. The recorded key set is therefore
what the organ *consumed at load*, not what its text mentions. The two audit-check organs
were measured by reading their bodies for any spec access at all; neither imports the spec
module nor parses the YAML, so their recorded set is empty by construction.

**Result — 4 of 9 clauses are opened by an organ.**

```
clause           asserted_by                                                 OPENED
root_allowlist   validate_hermetization.py::rule_a_violation                 yes
genre_folders    validate_hermetization.py::rule_a_violation                 yes
home_grammar     validate_hermetization.py::rule_c_violation                 yes
naming_grammar   validate_hermetization.py::rule_b_violation                 yes
required_docs    check_adr38_baseline.py + check_canonical_md_visibility.py  NO
vscode           check_workspace_settings.py                                 NO
sorting          check_workspace_settings.py                                 NO
python_layout    null (unasserted_reason given)                              NO
report_first     null (unasserted_reason given)                              NO
```

Recorded touched set: `{genre_folders, home_grammar, naming_grammar, root_allowlist}`.
Untouched: `{python_layout, report_first, required_docs, sorting, vscode}`.

**Clauses whose `asserted_by` names a NON-READING organ: 3** — `required_docs`, `vscode`,
`sorting`. Two clauses (`python_layout`, `report_first`) name no organ at all and carry an
`unasserted_reason`, which the existing `test_every_clause_is_asserted_or_says_why_not`
already admits as an honest gap rather than a defect.

### Discrepancy against the contract's arithmetic — recorded, not silently absorbed

The frozen contract's done-contract states *"clauses read by an organ **2/5 -> 5/5**"* and
*"clauses whose `asserted_by` names a non-reading organ **2 -> 0**"*. Measured against the
tree, the denominators do not reconcile:

- the spec carries **nine** clauses, not five; the only self-consistent reading of `2/5` is
  the sub-set `{home_grammar, naming_grammar}` already read plus the three the contract
  names — `python_layout`, `vscode`, `sorting` — which is `2 + 3 = 5`;
- the non-reading count is **3**, not 2. The third is `required_docs`, which the contract's
  prose does not name.

**This changes no scope and refutes no premise the lane acts on.** The three clauses to wire
are named explicitly and are unaffected by the counting; `required_docs` is handled below
under the same done-contract line (2), and its fix sits wholly inside this lane's declared
footprint. The counts are restated here in measured form so the closure can be checked
against the tree rather than against the contract's arithmetic.

## Step 2 — the PLAN round: the lane's two budgeted forks

Both forks are decided here and recorded before any build code. No third fork was opened.

### Fork 1 — where the kind declaration lives

**Decision: inside `home_grammar`, as two sibling keys — `kinds:` and `declared_kinds:`.**

The contract forbids a new clause for kinds, and `home_grammar` is already the clause that
answers *"where does a class of file live"*. A kind IS a class of file, so the kind axis is
a parameter of that clause rather than a neighbour of it.

- `kinds:` — the fleet grammar. Exactly six members (`source · test · data · model · eval ·
  tooling`), each mapping to **ONE** home.
- `declared_kinds:` — the repo's own declaration of which of the six it HAS. A kind a repo
  does not declare is not expected to have a home in its tree, which is what stops a
  governance hub taking a permanent WAIVE for having no `models/`.

**The `source` home is CITED, never copied.** It varies by layout, not by kind, and
`python_layout.source_home_by_layout` is already the single statement of it. `kinds.source`
therefore carries the cite token `python_layout.source_home_by_layout`, resolved at load
against a new `python_layout.declared_layout`. Copying `scripts` into a second key would
have created exactly the drift pair this spec exists to end.

### Fork 2 — where the three new readers sit

**Decision: `python_layout` -> `scripts/validate_hermetization.py`; `vscode` and `sorting`
-> `scripts/audit_checks/check_workspace_settings.py`.**

The lane's footprint admits exactly two organs, and the assignment is forced rather than
chosen: `vscode` and `sorting` already name `check_workspace_settings.py` in their
`asserted_by`, so wiring them anywhere else would move the claim instead of honouring it;
`validate_hermetization.py` is then the only remaining in-footprint organ, and it is already
the module that opens the spec at load.

Both readers are **fail-closed at load or at call**, matching the module's declared posture:
a spec that will not load means the gate has no rules, and a gate that silently admits
everything is worse than one that refuses to start.

### Not a fork — `required_docs`

Done-contract line 2 requires the non-reading count to reach **0**, and the measurement puts
`required_docs` in that set. It is wired in the same act, in `validate_hermetization.py`,
because that is the only in-footprint organ that can read it — there was no decision to
make, so no third fork was opened. The reader asserts the one property the clause can carry
without restating a roster: that `required_docs.source` and `root_allowlist.files_from` name
the **same** registry. Two clauses citing one registry by two strings is a drift pair; one
string checked at load is not.

The two audit-check organs `required_docs` names are **outside this lane's footprint** and
are not touched. Their `asserted_by` entry is kept and the new reader is appended to it, so
the clause names all three surfaces that now bear on it.

## Step 6 — closure

### The done-contract, measured

| # | Done-contract line | Measured at close |
|---|---|---|
| 1 | clauses read by an organ | **4/9 -> 8/9.** `python_layout`, `vscode` and `sorting` are each OPENED by a named reader. The ninth is `report_first`, which names no organ and states why. |
| 2 | `asserted_by` names a non-reading organ | **3 -> 0.** `required_docs` was the third, unnamed by the contract's prose; it is wired in the same act. |
| 3 | `home_grammar` carries the kind parameter | **present.** Six kinds, ONE home each, `declared_kinds` says which four this repo has. |
| 4 | reader-proof spec test | **absent -> `tests/test_fleet_shape_spec_readers.py`, 16 tests.** |
| 5 | English, hyphen-only names, logging over print, `pytest` green | held; no CLI was added, so the Click leg does not arise. |

The clause-by-clause close, against the step-1 table:

```
clause           reader                                                       OPENED
root_allowlist   validate_hermetization (unchanged)                           yes
genre_folders    validate_hermetization (unchanged)                           yes
home_grammar     validate_hermetization -- patterns, and now kinds            yes
naming_grammar   validate_hermetization (unchanged)                           yes
required_docs    validate_hermetization::_require_one_registry                yes  (was NO)
vscode           check_workspace_settings -- glob, dir_allowed, dir_forbidden  yes  (was NO)
sorting          check_workspace_settings -- asserted_by_setting               yes  (was NO)
python_layout    validate_hermetization::_python_layout                        yes  (was NO)
report_first     none -- a declared posture, `asserted_by: null` with a reason  n/a
```

### Line 4 is a witness, not a claim

The test file landed RED at `044cf902`, **before** any build code: 15 failed, 1 passed. It
went green only as the readers landed — the load-time half at `73ee4418`, the call-time half
at `982f83a8`. That sequence IS the proof the contract asks for. Every proof is behavioural:
each doctors the clause's payload and asserts the organ's verdict follows, so an organ that
stops reading its clause makes these tests fail rather than pass more quietly. A name-grep
over an organ would have proven the clause is mentioned there, not that its value is used.

`test_the_census_is_complete` is the forward guard: it derives the claimed set from the FILE,
so a clause that gains an `asserted_by` without gaining a proof surfaces on the next run
instead of joining the decorative set unnoticed.

### What this lane did NOT do

- **`report_first` stays unasserted.** It is a posture, not a mechanism, and the report
  generator is a sibling lane's deliverable. Line 2 is about clauses naming a *non-reading
  organ*; `asserted_by: null` names none.
- **The two `required_docs` audit-check organs are untouched** — outside the footprint. The
  new reader is appended to the clause's `asserted_by`, so it names all three surfaces that
  bear on it rather than displacing the two that assert its presence half.
- **`config/` is not read as the `data` home.** Its fate is intake #73 open question 8;
  answering it here would encode a guess as data. The hub's declared state is `ecosystem/`.
- **No seal re-run, no `BACKLOG.md` edit, no index regeneration, no JOURNAL entry** — V-3,
  V-4 and the integrator respectively.

### Coupled edit, disclosed

`tests/test_fleet_shape_spec.py`'s doctored payload gains `scripts` and `tests` in its home
patterns. `_python_layout` refuses at load a source or tests home the home grammar does not
admit, and that test's doctored spec left `python_layout` at the live `flat` layout while
removing `scripts` from the grammar — an internally incoherent spec that the new reader is
right to refuse. The addition changes nothing that test asserts: its refusals turn on
`protocols/` and `docs/audits/` still being absent from the doctored grammar.

### Targeted tests, against the 28-RED baseline

The batch gate is *compare against 28 RED @ `08c35b9c`, never against zero*, and a lane runs
the targeted tests covering its diff — the full suite runs once, at integration.

```
uv run --locked pytest tests/test_fleet_shape_spec_readers.py tests/test_fleet_shape_spec.py \
  tests/test_validate_hermetization.py tests/test_audit.py tests/test_audit_parallel.py \
  tests/test_batch_manifest.py tests/test_canonical_docs.py tests/test_manifest_link_route.py

469 passed, 1 failed
```

`uv run --locked ruff check scripts/ tests/` — clean.
`uv run --locked python scripts/audit.py health` — `health: OK` (WARN rows only, every one of
them pre-existing: batch U/V lane contracts under `consumer_at_landing`, and the four
`proof_layer` rows `[#638]` owns).

**The one RED is pre-existing and outside this lane's footprint**, established rather than
assumed:

- `tests/test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival`
- Cause: `audit.py::_derived_freshness_findings` narrows the UNSTAMPED class to the gated
  set's own directories (R5 window bundle B10, ruled 2026-09-05). The fixture's unstamped
  doc is `protocols/README.md` while the test pins the gated set to two ROOT files, so the
  unstamped member is out of scope and no UNSTAMPED warn is emitted. The test still expects
  the pre-narrowing behaviour.
- Attribution: the narrowing landed at `63e94ff2` (2026-09-05), which `git merge-base
  --is-ancestor 63e94ff2 33bcb0bd` confirms predates this lane's base. This lane's diff
  touches neither `scripts/audit.py` nor `tests/test_canonical_docs.py` (`git diff --stat
  33bcb0bd..HEAD` is six files, listed in the commits above), and nothing on that code path
  imports anything this lane changed.
- Disposition: **left alone.** It is out of footprint, and the fix is a ruling-driven test
  update owned by whoever ruled B10 — not a drive-by from a spec-reader lane.

One measurement note recorded so it is not repeated: an early background run of a subset of
these files reported exit 0 with an EMPTY output file. That exit code was not evidence — the
same selection run in the foreground reproduces the failure. A background run whose output
never landed is an un-run, not a pass.

### Gate bypasses declared

Three commits declared a single-hook bypass in the commit body, per the contract's
"the integrator is gate-of-record and regenerates once at the merge" (Q1):

- `f8eb6c5e` — `audit-index-freshness` (this artifact is a new `docs/audits/` member)
- `044cf902`, `73ee4418` — `doc-counts-pytest-freshness` (`pytest_collected` 5390 -> 5406)

No other hook was skipped, and `--no-verify` was not used. **The integrator owes two
regenerations at the merge:** `docs/audits/README.md` and `ecosystem/doc-counts.md`.

