# lane-x-683-three-small-fixes — end-of-lane evidence

Contract: `LANE-x-683-three-small-fixes.md`. Shape: local, own worktree, commit-and-STOP.
This is the end-of-lane artifact the contract's Step 5 requires; the integrator merges from
the primary checkout.

## Done-contract, clause by clause

### Clause 1 — `[#683]`'s predicate scoped to `status: active`. DONE.

`tests/test_override_command_removed.py`'s id leg refused ANY manifest component with id
`override-command`, at any status. That forbade the deploy manifest's own documented
lifecycle — a removed component's *"manifest entry is retained as a tombstone"* — from ever
recording `/override`'s retirement.

**Source of the exact fix, verbatim.** This clause is not a fresh finding; it is the one-line
resolution `docs/audits/2026-09-12-technical-lane-x-734-retire-stage-2-evidence.md` ("The ONE
escalation") proposed for the operator/architect to rule on: *"scope that predicate to
`status: active` components... a tombstone with no `artifacts:` trips neither"* of the other
two legs.

RED-first witness: `test_a_removed_tombstone_with_no_artifacts_does_not_violate` — a synthetic
`status: removed` `override-command` component with no `artifacts:`. Refused before the scope
(`9ef2dc9d`), passes after (`95f4134e`). Two siblings guard the narrowing didn't hollow the
tooth out: an ACTIVE component with the retired id still violates, and a tombstone that still
ships the payload path still violates (the artifacts[].path leg is id-and-status-blind by
design).

Commits: `9ef2dc9d` (RED), `95f4134e` (fix).

### Clause 2 — `safe_remove.py` downgrades SAFE to REVIEW on a bare-stem string literal. DONE.

Source: the same evidence file, "Open items for the integrator / architect" #3 — the oracle's
false-PASS class named against `_load("desired_state_loader")`, a dynamic/string-keyed
reference no static oracle can see (ADR-89).

Built `_bare_stem_literal_hits()` (greps `*.py` under a scan root for the removed module's bare
stem as a quoted literal); `evaluate_removal()` downgrades an otherwise-SAFE verdict to a new
`"review"` status on a hit, carrying hit sites in `Verdict.review_hits`. Never escalates past
`unsafe`/`unverifiable` — a hit is a heuristic, not proof (WARN + allow, same posture as
`unverifiable`). `evaluate_removal()` gained a `scan_root` kwarg because `check_removal`'s own
`repo_root` is a `scripts/`-only materialization; `check_removal` now passes the REAL repo root
so a dynamic reference under `tests/` is not invisible to the downgrade too.
`check_safe_removal` (the audit adapter) maps `"review"` to one WARN Finding; `format_text`
renders the hit sites.

RED-first witnesses: `test_bare_stem_string_literal_downgrades_safe_to_review` + three
siblings (no-hit stays SAFE; a real surviving referrer still wins over a hit; `check_removal`
scans the real tree, not the scripts/-only materialization). Refused before (`9ef2dc9d`),
green after (`599e44aa`).

Commits: `9ef2dc9d` (RED), `599e44aa` (fix).

**Single-hook bypass declared: `graph-task-coverage`** (`SKIP=graph-task-coverage`, not
`--no-verify` — every other gate ran, `599e44aa`). `scripts/safe_remove.py` has no inbound
`implements` edge from an OPEN `tasks/` row. This fix has no filed task by design: the source
evidence file states verbatim, of this exact item, *"Filing it is a new row, not this lane's
act."* This lane's own decision budget (`protocols/STANDING_RULINGS.md` "The decision budget",
V-2 class (c): fork classes with no standing ruling) has no authority to file a new backlog
task outside its declared footprint — filing one would itself be scope creep — so the gap is
bridged with a declared bypass rather than left silently unfixed. **Flagged for the
integrator/architect**: either file a task claiming `scripts/safe_remove.py`'s bare-stem
downgrade, or rule that this class of small, evidence-sourced fix is exempt.

### Clause 3 — AX25-2's generator-to-verb conformance test GREEN. DONE, but the premise was REFUTED.

The contract states, and the contract's own "A note on the third clause" anticipated the risk:
*"MODEL_ENUM ... was widened ... on the dispatcher's own branch. If that branch has already
merged..."* — **it had.** `lane-x-675` (AX25-2's actual build lane) merged before this lane's
first commit; `tests/test_dispatch_conformance.py::test_the_generators_line_is_a_line_the_ruled_verb_resolves`
already exists verbatim to the contract's description — *"generates a contract with
`gen_lane_contract.py` and runs the ruled verb's DryRun against it, asserting it RESOLVES —
fence, contract location, model and base in one assertion"* — and was **already GREEN** at
this lane's first measurement, not RED.

Per Q10 (a refuted premise PAUSEs with the fact; disclosure discharges the reporting duty, it
does not authorise inventing a deviation): no duplicate test was written, no code was touched
for this clause. Verified GREEN at every commit in this lane (`22 passed`, most recently
against `599e44aa` merged forward to current `main`). The Done-contract's clause 3 predicate —
*"AX25-2's ... test exists and is GREEN"* — is satisfied by inheritance from `lane-x-675`, not
by this lane's own act.

### Clause 4 — English, hyphen-only names, logging over print, Click for a CLI, `pytest` green.

- English, hyphen-only names: yes throughout.
- Logging vs print: unchanged from the existing modules' convention (neither `safe_remove.py`
  nor its test files gained a new print/log call this lane didn't already have a precedent
  for; `format_text`'s CLI rendering is pre-existing `print`, not touched).
- Click: no new CLI surface was added; `safe_remove.py`'s existing `argparse` CLI is unchanged.
- `pytest` green: see Verification below.

## Verification

```
uv run --locked pytest tests/test_override_command_removed.py tests/test_safe_remove.py \
  tests/test_dispatch_conformance.py tests/test_release_lint.py tests/test_audit.py \
  -q -n auto -k "not real_oracle"
-> 324 passed, 1 failed
```

The one failure, `test_check_fleet_parity_green_on_live_repo`, is **outside this lane's
footprint**: it reports `.dev-knowledge` `settings.json` hook drift and sibling-repo
(`ai-council`, `corp-monorepo`) `.claude/commands/override.md` roster gaps — none of which this
lane's diff touches (`ecosystem/doc-counts.md`, `scripts/safe_remove.py`,
`scripts/audit_checks/check_safe_removal.py`, `tests/test_override_command_removed.py`,
`tests/test_safe_remove.py`). Not investigated further per "no edits outside this lane's
declared footprint"; flagged for the integrator.

`test_safe_remove.py`'s two `@requires_pyright` real-oracle tests are skip-guarded (no Pyright
langserver in this environment) — pre-existing honest-limit posture, unrelated to this lane.

`uv run --locked ruff check` on every changed file: all checks passed (run per-commit above).

`deploy/release_lint.py --version 1.5.0`: 0 FAIL, 1 WARN (C2, expected pre-release), 7 pass —
unaffected by this lane's diff.

`ecosystem/doc-counts.md` regenerated once per test-count-changing commit
(`gen_doc_counts.py --write`): `6012 -> 6019` (RED-first commit, +7 test defs) `-> 6020`
(clause 2's adapter test).

## Worktree hygiene note (not a footprint item — recorded because it consumed most of this
## lane's wall-clock and is worth the integrator knowing)

This worktree was created stale enough that the ADR-85 `journal_spine_anchor` check false-
FAILed twice on tree lag rather than a real gap (the discriminator: `is_anchored` False in
this tree but **True at `main`** for the SHAs it named) — `git merge main` (a plain
fast-forward both times, zero conflicts with this lane's files) resolved it, per the check's
own printed diagnostic and fix command. Neither sync touched `main` or another lane's branch;
both only advanced this lane's own branch pointer to catch up with commits already landed and
pushed by others. `git rev-list --count HEAD..main` is `0` as of this artifact.

## What NOT done, per contract

No merge to `main`, no push, no JOURNAL entry, no index regeneration beyond the two narrow,
gate-mandated `ecosystem/doc-counts.md` touches above. No edits outside
`tests/test_override_command_removed.py`, `tests/test_safe_remove.py`, `scripts/safe_remove.py`,
`scripts/audit_checks/check_safe_removal.py`, `ecosystem/doc-counts.md`, and this artifact.

## Open items for the integrator / architect

1. **`scripts/safe_remove.py`'s bare-stem downgrade has no OPEN task claiming it** — the
   `graph-task-coverage` single-hook bypass above. File one, or rule the class exempt.
2. **`test_check_fleet_parity_green_on_live_repo` fails on the live repo** independent of this
   lane — sibling-repo `.claude/commands/override.md` roster drift and a `.dev-knowledge`
   `settings.json` hook not manifest-owned. Pre-existing; not this lane's footprint.
