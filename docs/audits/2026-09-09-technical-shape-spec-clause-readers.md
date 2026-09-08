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

Filled at the end of the lane.
