---
intake-id: 58
status: READY
origin: cloud night batch C2 (Dispatch-Cloud, 2026-08-26, `.dev-knowledge` @ d8211b0, read-only), harvested and ruled 2026-08-27 in the night-harvest consumption ledger section B (I-KODEKS); architect rulings X3 and X4
consumers: "`docs/audits/2026-08-27-technical-python-kodeks-census.md` (the landed C2 report, this intake's evidence); `pyproject.toml` `[tool.ruff.lint]`; `ecosystem/parity-surfaces.yaml` (a fifth MUST-uniform surface); `templates/ruff-config-block.toml`; `protocols/PLAYBOOK.md`'s Python-standard section; STANDING_RULINGS sections X3 and X4"
---

# The Python standard is a doc that enforces nothing — split it on enforceability

## Problem / motivation

The hub declares a Python standard in `protocols/PLAYBOOK.md` and enforces almost none of it.
`pyproject.toml` carries `extend-select = []` — an empty selection — so the standard has sat in a
protocol file for months while the hub's own **135 modules** diverged from every clause a machine
was never asked to check.

C2 measured the divergence rather than asserting it, and the numbers decide the shape:

- **Rich-for-output**: **1 of 135** files uses Rich. The clause as written is fiction.
- **Click-for-CLIs**: **13 of 78**. Retrofitting 65 modules is not a standard, it is a rewrite.
- **dataclasses-over-dicts**: **141** dict-returning functions.
- **`ANN`**: 302 non-test violations against **6910** tree-wide — 96% of it is test code.
- Twelve rule families measure **zero tree-wide**; a further seven cost **58 fixes total**.

Three of the standard's substantive items are **unrepresentable in ruff** — there is no rule for
Click-vs-argparse, Rich-vs-print, or dataclass-vs-dict. The tempting fix is a hub checker for
those three, and `scripts/enforcement_coverage.py` already records why that fails: a hub-hardcoded
standalone checker lands as **`absent`** on a consumer by measurement, entering the
genuinely-unclosable-without-porting class. Presence is not enforcement.

So the standard has two halves with different physics, and the current single doc-shaped carrier
serves neither. **Ruling X3 (Option C): split on enforceability.** Ruff-decidable clauses become an
executable rule set pinned as a **fifth MUST-uniform parity surface**; the three unrepresentable
clauses stay doc-level intent, and **no new hub checker is built for them**. **Ruling X4:** those
three are **amended, not enforced** — Rich narrowed to operator-facing CLI output only, Click as
intent for NEW CLIs with no retrofit, dataclasses-over-dicts as intent.

One recorded ruling must be reversed on the record, not quietly edited around:
`templates/ruff-config-block.toml` currently declares `select` **REPO-PERSONAL by name** (an ARC-4
ruling). X3 supersedes that declaration, and the supersession is part of the work.

## Scenarios (+1 view)

- As a consumer repo I inherit the fleet's pinned `astral-sh/ruff-pre-commit` hook and a
  `pyproject.toml`. Today that buys me nothing of the Python standard, because the selection is
  empty. After X3 it buys me the whole enforceable half with **no hub script present** — ruff is
  the runtime.
- As an executor I read the standard, see "use Rich for output", and look at the tree: one file in
  135 does. I cannot tell whether I am reading a rule, an aspiration, or a dead letter — so I
  ignore all three clauses, including the two that are good advice.
- As the fleet-parity organ I already read `pyproject.toml` and already hold four MUST-uniform
  surfaces. A fifth costs nothing new to distribute; the channel is proven.

## Functional requirements

- **Must:** the free ratchet lands first — the twelve rule families measuring **zero** tree-wide
  (`T203, LOG, G, ICN, INT, SLOT, TID, NPY, W, YTT, ASYNC, FA`) plus the near-zero tier
  (`ISC, A, PIE, RET, B, FLY, C4`, 58 fixes total) are selected, with `ruff check .` exiting 0.
  Zero-cost enforcement is not a phase-in; it is free and should not wait on the rest.
- **Must:** the three unrepresentable clauses are **ruled per X4** and PLAYBOOK's Python-standard
  section is edited to match the ruling. A clause measured at 1-of-135 stays in the doc only if the
  doc says what it now means.
- **Must:** **no new hub checker** is built for Click / Rich / dataclasses (X3). If a future arc
  disagrees, it reverses X3 explicitly rather than shipping the checker.
- **Should:** the ruff rule set becomes a fifth MUST-uniform surface in
  `ecosystem/parity-surfaces.yaml`, and `templates/ruff-config-block.toml`'s REPO-PERSONAL `select`
  declaration is **superseded on the record**, not silently overwritten.
- **Should:** `templates/ruff-config-block.toml` carries the `tests/fixtures/**`
  `per-file-ignores` idiom beside the values it already ships — without it any consumer switching
  on `ANN` or `T201` takes thousands of violations in test code.
- **Could:** the costed phase-in of the four expensive enforceable clauses — `T201` (344),
  `ANN001/ANN201` (211 non-test), `C901+PLR0912/0915` (131), `PLR2004` (61) — each either
  selected-and-clean or carrying a dated, reasoned `per-file-ignores` entry naming the module.

## Acceptance criteria (ex-ante)

1. `pyproject.toml`'s `[tool.ruff.lint]` selection is non-empty and names the twelve zero-cost
   families explicitly; `uv run --locked ruff check .` exits 0 with no new `per-file-ignores`
   introduced for the zero-cost tier.
2. A recorded ruling exists for **each** of Click-for-CLI, Rich-for-output and
   dataclasses-over-dicts, stating one of {enforce via new organ · amend the standard · accept as
   aspiration}, with the measured denominator quoted (13/78 · 1/135 · 141).
3. PLAYBOOK's Python-standard section text agrees with those three rulings — a reader cannot find a
   clause the tree refutes.
4. `ecosystem/parity-surfaces.yaml` carries a fifth MUST-uniform surface covering
   `[tool.ruff.lint]`, and `fleet_parity` reports it across all three fleet repos.
5. `templates/ruff-config-block.toml`'s `select` REPO-PERSONAL declaration is superseded with a
   dated pointer to X3 — the reversal is legible in the file, not only in the register.
6. `uv run --locked pytest -x --tb=short` green; pre-commit green including the pinned ruff hook.

## Non-goals

- **Not a new hub organ.** X3 forecloses a standalone checker for the three unrepresentable
  clauses; this intake does not reopen it.
- Not a retrofit of the 65 non-Click CLIs or the 141 dict-returning functions. X4 makes both
  **intent for new code**, and a retrofit would need its own ratification and its own budget.
- Not a change to the pinned ruff **rev**. The hook rev is fleet-canonical and a uv/ruff bump is
  its own gated change (ADR-106); this intake changes the *selection*, not the *version*.
- Not `pytest` configuration beyond the `minversion` already declared.

## Impact sketch (4+1 lite)

- **Logical:** the standard gains an executable half and keeps a documented half; the two are
  bound by a named agreement rather than by hope.
- **Process:** lint failures become a commit-time refusal for the ratcheted families rather than a
  review-time opinion.
- **Development:** the zero-cost tier is a config edit; the costed tier is real remediation work
  across `scripts/audit.py`, `scripts/nopack_sandbox.py` and `deploy/carrier_precommit.py`, which
  the phase-in must disposition by name.
- **Physical:** none new — the distribution channel (`pyproject.toml` + the pinned pre-commit hook)
  already exists and already reaches every consumer.

## Open questions

- Should the fifth parity surface pin the **whole** `[tool.ruff.lint]` table, or only the `select`
  list? Pinning the whole table makes `per-file-ignores` fleet-uniform, which may be wrong for a
  consumer with a different test layout.
- Two surfaces must stay in agreement (the ruff table and the doc). Is the
  `provider-registry-agreement` hook the right precedent to copy for that, or is the doc's
  agreement cheap enough to leave to review?
- Does amending Rich to "operator-facing CLI output only" leave the clause with any teeth at all,
  or is the honest act to retire it? X4 amends; this records the doubt.

## Status

READY — filed 2026-08-27 from the night-harvest consumption ledger section B. Rulings X3 (Option C,
split on enforceability, no new hub checker) and X4 (the three clauses amended, not enforced)
already taken. First act is the free ratchet.
