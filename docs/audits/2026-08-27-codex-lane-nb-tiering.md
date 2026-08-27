# Codex/terra review — lane-nb-tiering ([#597] + [#598])

> Adversarial code review of `d8211b03..b7ed7bcc` on `worktree-lane-nb-tiering`, scoped to code
> only (`scripts/audit.py`, `scripts/validate_doc_claims.py`, and the three test files); `.md`
> files excluded from scope. Run via `codex exec`. Sibling artifacts:
> `docs/audits/2026-08-27-technical-lane-nb-tiering.md` ([#597]) and
> `-durations.md` ([#598]).
>
> **This file was written by the lane, not by the reviewer, and that is a deviation worth
> stating.** The reviewer was asked to write it and refused: *"Unable to write
> `docs/audits/2026-08-27-codex-lane-nb-tiering.md`: repository instructions require Codex to
> remain read-only."* The findings below are the reviewer's, transcribed; the verification and
> the dispositions are the lane's, and are labelled as such.

## Tally

| Severity | Found | Fixed | Refuted |
|---|---|---|---|
| Critical | 0 | — | — |
| **High** | **3** | **3** | 0 |
| Medium | 0 | — | — |
| Low | 0 | — | — |

The contract's bar is *fix ≥ medium*. All three HIGHs are fixed in `<commit-3>`. **None was
taken at face value** — each was re-derived against live source before acting, per the standing
rule that a reviewer's finding is a claim until resolved.

The reviewer was explicitly asked to **refute** the claim that ship-gate behaviour is unchanged.
It did not refute it; H2 is the observation that the claim was under-tested, not that it was
false. The byte-identity harness result (149 findings, 46 checks, identical in order) stands.

---

## H1 — `runs_at_tier` accepted any runner-tier string · `scripts/audit.py`

**Finding.** `runs_at_tier()` validated the *declared* tier but accepted any *runner* tier;
anything other than `None`/`"ship"` fell through to the commit branch. So
`run_checks(tier="shp")` would silently defer all ten ship-tier checks and report a green,
incomplete gate.

**Verified — REAL, and it is the sharper version of the bug I wrote `_tier` to prevent.** The
declaration side raises on a typo; the runner side quietly did the most dangerous possible thing
with the identical typo. The asymmetry was mine and it was indefensible.

**Fixed** two ways, because one was not enough:
- `runs_at_tier` now raises `ValueError` on an unrecognised runner tier.
- `run_checks` validates **once at entry**, because the per-check comprehension never reaches
  the raise on an **empty** registry — a legitimate call (`tests/` monkeypatches `ALL_CHECKS`
  down to nothing) that would otherwise have returned a clean, empty, GREEN result. The
  reviewer named the entry-point fix; the empty-registry hole is the lane's own finding on top
  of it.

**Tests:** `test_an_unknown_runner_tier_raises_rather_than_deferring_silently`, parametrized over
`shp`, `SHIP`, `push`, `integration`, `""` — `push` and `integration` deliberately, because
[#597]'s row names both and this module has neither; plus
`test_an_unknown_runner_tier_raises_even_on_an_empty_registry`.

## H2 — ship-gate wiring was not tested end-to-end · `tests/test_audit.py`

**Finding.** The new tests prove `run_checks(tier=None)` runs both tiers, but nothing invoked
`cmd_ship_gate` with tiered sentinels. If it were later changed to pass `TIER_COMMIT`, every
added test would stay green while ship-tier checks were silently omitted.

**Verified — REAL, and it is the most important of the three.** The entire claim of this arc —
*tiering moves work to a later gate, never off the gate set* — rests on one line of wiring in
`cmd_ship_gate`, and that line had no test. Byte-identity proves today's behaviour; it does not
protect tomorrow's.

**Fixed:** `test_cmd_ship_gate_runs_BOTH_tiers_end_to_end` invokes the real command with one
sentinel per tier and asserts both ran, that no deferral line appears in the output, and exit 0.

## H3 — the claim-3 monkeypatch was inert · `tests/test_validate_doc_claims.py`

**Finding.** `monkeypatch.setattr(vdc, "_derive_pytest_collected", ...)` does not reach
`_CLAIMS`, which captured the function object at import. The stub never applied; the test shelled
out to a real `pytest --collect-only` and passed anyway.

**Verified — REAL, and it is a defect this lane introduced in act 1.** Worse, the file's own
`_claims_with_stub_pytest` helper documents this exact trap in its docstring, three dozen lines
below the line I wrote. I replaced a `_GATE_MODE` patch with a *different* inert patch and did
not notice, because the test kept passing — the seam-detaches-silently class
`audit_checks/registry.py` exists to name.

**Fixed:** patched on the registry via the supported `claims=` hook
(`_claims_with_stub_pytest(lambda root, n: None)`).

**Corroborating measurement, not just a green test:** the three suites together went from
~51 s to **13.45 s**. Part is B10; part is this test no longer launching a real pytest. A stub
that was working would not have shown up in a wall-time.

---

## What the reviewer did NOT find, recorded so the negative space is legible

The prompt asked specifically about six hazards. Three produced no finding and are worth naming
rather than leaving as silence:

- **Serial vs parallel slot construction / registry order.** No finding. Order is asserted by
  the pre-existing `test_audit_parallel.py` suite plus the new both-modes deferral test.
- **Mutating function objects imported from other modules (the `_tier` stamp on the 16 checks
  defined in `scripts/audit_checks/`).** No finding. The stamp is idempotent, process-global, and
  read by nothing else.
- **Telemetry emission skip for deferred checks.** No finding. Confirmed live: 36 rows, not 46.

**Honest limit on this review:** the reviewer ran no tests (*"repository instructions permit
read-only inspection only"*), so every finding is from static reading. The lane ran the tests.
And a single reviewer at one severity threshold is not a proof of absence — H3 in particular was
an inert-seam bug that had been passing green, which is precisely the class a review catches and
a test suite does not.

## Disposition

ACTIONED — 3 of 3 HIGH fixed, verified individually, tests added for each.
