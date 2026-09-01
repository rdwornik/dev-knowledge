# LANE d-4 (deploy-waiver-honoring) — end-of-lane artifact

- **Class:** technical · **Date:** 2026-09-01 · **Lane:** `lane-d-4-deploy-waiver-honoring`
  (branch `worktree-lane-d-4-deploy-waiver-honoring`, contract
  `LANE-d-4-deploy-waiver-honoring.md`)
- **Closes:** `[#276]` D2 per-consumer waiver-honoring, Done-when verbatim (both legs, with tests)

## What changed

`deploy/carrier_precommit.py` is now the single site that reads a consumer's own
`.methodology.yaml` `sanctioned_divergences` allowlist (via
`scripts/enforcement_coverage.py::read_allowlist` — reused, not duplicated) and folds
it into BOTH legs:

1. **Prune leg** — `_classify_prune(config, prunable, *, waived: bool = False)` now
   returns `PruneState.ALREADY_ABSENT` whenever the component's id is a declared
   divergence, regardless of the on-disk shape. `PrecommitCarrier.detect_prune` /
   `.prune` compute `waived` from the consumer's `.methodology.yaml` (matched by the
   `components:` id — the manifest entry, received verbatim) and pass it through.
   `tool.py`'s `execute()`/`build_prune_plan` needed **zero changes**: `ALREADY_ABSENT`
   is already the one `PruneState` that skips cleanly with no REFUSE-abort and no
   destroy-confirm in the existing dispatch — the fix is entirely upstream of it.
2. **Add/converge leg** — `_classify`, `_reconcile`, and `_verify_satisfied` all gained
   a `waived: frozenset[str] = frozenset()` parameter (hook-id keyed — the only
   identity `carriers:` targets expose; `components:` ids are a separate namespace
   `deploy/tool.py` never reads). A waived hook id is treated as not-required across
   all three: `detect` won't call it DRIFTED, `apply` won't append it (creation or
   in-place), and `verify` won't demand it back — the last one matters independently
   (D9): without it, an `apply()` that correctly skipped a waived hook would still
   fail `verify()`, aborting `execute()` on the very divergence the consumer declared.
   `PrecommitCarrier.detect/apply/verify` each independently call
   `_waived_components(self.repo_root)`.

`deploy/tool.py` — **no functional changes.** Confirmed by design: the waiver read
and every waiver-driven decision lives in `carrier_precommit.py` (the "measured site"
per the frozen contract's Done-contract item 2); `tool.py`'s existing
`ALREADY_ABSENT`/`prune_pending`/`execute()` dispatch already does the right thing
once the carrier reports the right state.

## Proposed diffs (already applied, in write-scope)

- `deploy/carrier_precommit.py` — waiver reader + both legs (138 insertions / 21
  deletions net; see `git diff`).
- `tests/test_carrier_precommit.py` (new) — 18 unit tests at the carrier boundary:
  `_waived_components` shape parsing; prune leg on BOTH live corpus shapes
  (ai-council's bare `id: ruff`, corp-monorepo's `args: []` omission) each with a
  REFUSE-baseline test and a skip-when-declared test, plus per-id discrimination and
  the already-absent-is-unaffected case; add leg with a DRIFTED/re-add baseline, the
  waived-is-PRESENT_CORRECT case, apply-never-re-adds, verify-does-not-demand-it-back,
  and a discrimination check (waiving one hook id does not waive a different missing
  one).
- `tests/test_deploy_tool.py` (new) — 3 integration tests driving the REAL
  `PrecommitCarrier` through `tool.assess()`/`tool.execute()` against a hermetic git
  consumer carrying BOTH live-corpus shapes at once: a contrast baseline (no
  `.methodology.yaml` → `--execute` still REFUSE-aborts, proving the fix
  discriminates rather than disabling the hash-guard), the Done-when end-to-end case
  (both declared → `aborted is False`, record written, file byte-untouched on both
  fronts), and an `assess()`-only read check (`prune_pending == ()`, carrier state
  `PRESENT_CORRECT`).

All new/existing targeted tests green; `ruff check` clean on every touched file.

## Design decisions made without escalation (reported, not asked — V-2 budget)

- **Hook-id keying for the add leg vs. `components:`-id keying for the prune leg.**
  Forced by what data each leg actually receives: `detect_prune`/`prune` get the full
  `components:` entry (has `id`); `detect`/`apply`/`verify` get only the `carriers:`
  target (hook ids only, no `components:` linkage — confirmed by the manifest's own
  comment that `components:` entries like `hub-codemap-hooks` are "INERT to
  deploy/tool.py (reads only carriers:)"). Getting a `components:` id into the add
  leg would need a manifest schema edit, which is out of this lane's write-scope.
  Documented in-code at both sites.
- **No expiry/review_date staleness enforcement.** `_waived_components` honors a
  declared divergence on shape alone (non-empty `reason`); it does not reject an
  expired entry the way `scripts/enforcement_coverage.py::validate_allowlist_entry`
  does for the Informant's reporting surface. Staleness policing is that organ's job;
  `[#276]`'s contract is "read the allowlist and honor it," not build a second policy
  engine. Also avoids threading wall-clock `run_date` through `Carrier.detect(target)`,
  whose signature is frozen (contract.py, out of write-scope) and carries no such
  parameter.
- **`ALREADY_ABSENT` reuse for the prune leg's "waived" outcome.** `contract.py`'s
  `PruneState` is a closed three-value enum, out of this lane's write-scope. No other
  value produces "skip, no REFUSE, no destroy-confirm" through the existing
  `tool.py` dispatch, so this is the only enum-compatible answer; narration
  ("already absent -- skip") is not perfectly accurate for a waived-but-present
  entry, but the behavior is correct and `tool.py` needed no changes. Not fixed
  cosmetically here — flagged as an open item below.

## Open items (not this lane's write-scope / not required by the Done-contract)

- `PrunePlanItem`/`PruneExecOutcome` narration doesn't distinguish "genuinely
  absent" from "present but waived" — both read `already absent -- skip` in
  `tool.py`'s plan/execute output. A future increment could add a `waived: bool`
  field to those (tool.py) dataclasses for accurate operator-facing text; not
  needed for `[#276]`'s Done-when, which is behavioral.
- Neither live consumer (ai-council, corp-monorepo) actually carries a
  `.methodology.yaml` entry for `codemap-freshness` today (unverified from this
  sandbox — no sibling checkout available); the add-leg mechanism is proven against
  a synthetic fixture matching #276's original FOLD 2026-07-11 description, not a
  live consumer file. If/when a real consumer declares that exclusion, this
  mechanism honors it with no further code change.
