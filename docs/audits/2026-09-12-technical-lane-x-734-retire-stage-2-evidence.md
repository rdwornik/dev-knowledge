# Lane `lane-x-734-retire-stage-2` — retire-stage evidence log (second attempt)

> Working evidence artifact for `LANE-x-734-retire-stage-2.md`, the SECOND run of the
> AX13-2/AX13-3 retire stage (`[#734]`). The first run's record is
> `docs/audits/2026-09-11-technical-lane-x-734-retire-evidence.md` (on `main` at `f1711e3d`);
> this contract was rewritten from it. Appended to across the lane's steps; the final section
> is the end-of-lane artifact. Tool output is recorded verbatim, never narrated.
>
> Governance consumers: `[#734]` (the owning row), `[#267]` (live reader of
> `deploy/lived_sandbox/arc.py`), `ADR-106` §5, `ADR-109`, `ADR-110`, `ADR-89` (the oracle's
> honest limit), `intake #86` (the census fixture).

## Step 1 — preconditions, and the re-execution of the reverse-dep oracle

### Precondition 1: the pinned langserver was vendored

`npm install` — `added 1 package, and audited 2 packages`;
`node_modules/pyright/langserver.index.js` present afterwards. `package.json`'s sole declared
dependency is `pyright@1.1.410` and `package-lock.json` is committed, so this restores a
**declared, pinned, checked-in** dependency (the same class of act as `uv sync --locked`).
The working tree was clean immediately after the install — `node_modules/` stays gitignored and
out of this lane's commits, verified rather than assumed.

### Precondition 2: the oracle ran at its DEFAULT per-symbol timeout

No `--timeout` was passed. The first run's `--timeout 300` is a per-QUERY timeout, not a total
budget, and cost it ~20 minutes of zero output before it was killed.

### Run 1 — the eight-module set exactly as the contract's Step 1 words it

`uv run --locked python scripts/safe_remove.py <the eight modules>`, verbatim:

```
safe-removal verdict: UNSAFE
removal set: scripts/boundary_headers.py, scripts/boundary_report.py, scripts/cloud_provisioning.py, scripts/desired_state_loader.py, scripts/desired_state_report.py, scripts/probe_child_backlogs.py, scripts/seed_runbook.py, scripts/validate_onboarding_rulings.py
reason: 12 surviving referrer(s) would dangle on removal (completeness: complete)

surviving referrers (would dangle on removal):
- tests/test_desired_state_loader.py:186 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:383 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:67 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:92 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:113 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:126 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:159 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:172 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:181 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:260 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:228 -> resolve_fleet_members (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:389 -> resolve_fleet_members (scripts/desired_state_loader.py)

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**The contract's Step 1 premise — "confirm the SAFE verdict still holds" — does NOT hold as
worded.** That is recorded first, before any reading of it, because the re-execution was the
point of the step.

### Why this is not the tree having changed

A history query for the three implicated files over the range `f1711e3d..HEAD`
(`tests/test_desired_state_loader.py`, `tests/test_desired_state_report.py`,
`scripts/desired_state_loader.py`) returns **empty**: they are byte-unchanged since the tree
the first run measured. The divergence is therefore in the **oracle run**, not in the tree.
**This lane could not determine what made the first run report SAFE on an identical tree, and
marks the evidence as stopping here** rather than reconstructing a cause it cannot witness.

### What the 12 referrers actually are, and the tool's own escape

All 12 are in `tests/test_desired_state_loader.py` and `tests/test_desired_state_report.py` —
the **dedicated tests of two of the removal targets**. `safe_remove.py`'s own module docstring
rules this case explicitly:

> Test-only importers ARE real referrers (removing the module breaks the test) -> blocking on
> them is correct; **co-removing the test is the escape.**

And `evaluate_removal`'s contract (`scripts/safe_remove.py:183`): *"a referrer SURVIVES iff its
file is NOT itself in the removal set."*

The Done-contract's clause 1 defines this lane's unit of removal as **module + dedicated test +
`graph_queries.py` Disposition entry + `test_graph_spine.py` `CENSUS_SCRIPT_ORPHANS` entry** —
the test is part of the removal unit, not a survivor of it. Run 1 asked a narrower question
than the contract's own removal unit: it held the dedicated tests fixed while removing their
modules. Run 2 asks the contract's question, and is recorded below.

**Run 2 was still executing when this section was committed.** It is recorded verbatim below
before Step 3 acts on the `desired_state_*` pair. Step 2 does not wait on it and does not need
to: run 1 already reports **zero** surviving referrers for all six of clause 1's targets, and
adding files to a removal set can only REMOVE survivors from the result, never add them
(`evaluate_removal`: a referrer survives *iff its file is not itself in the removal set*). Run
2's verdict can therefore change the disposition of the `desired_state_*` pair, and cannot
change the six.

**This is resolution IN-contract, not a deviation:** the frozen Done-contract clause defines the
removal unit; the Steps skeleton's "eight-module set" phrasing is the looser statement of it.
No decision-budget class is spent.

### Why six of the eight produced ZERO surviving referrers

Not because they have no tests — all six have dedicated tests. Because of the oracle's declared
static-only limit, and the two test-import styles in this repo differ exactly where it bites:

- `tests/test_desired_state_loader.py:32` does `from scripts import desired_state_loader`, then
  `_loader().load_fleet_model(...)`. Pyright resolves the package import and the attribute, so
  the oracle SEES the referrer.
- `tests/test_cloud_provisioning.py` does `sys.path.insert(0, .../"scripts")` then
  `import cloud_provisioning as cp`. Pyright cannot follow a runtime `sys.path` mutation, so
  those referrers are INVISIBLE to the oracle.

So the six targets' clean result is a **limit-bounded pass, not proof of no test coupling** —
exactly the false-PASS class ADR-89 declares and `safe_remove.py` restates. It is recorded as
such here rather than reported as a clean bill. The coupling is handled the same way either
way: clause 1 co-removes each module's dedicated test.
