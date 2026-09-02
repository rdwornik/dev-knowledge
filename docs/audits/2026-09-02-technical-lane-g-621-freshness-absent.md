# LANE-g-621 — item 3 landed, items 1 and 2 escalated with reproduced evidence

**Date:** 2026-09-02 · **Class:** technical · **Arc:** `[#621]` · **Lane:** `lane-g-621-freshness-absent`
· **Branch:** `worktree-lane-g-621-freshness-absent` · **Seat:** CC (Sonnet 5)

## 1 · What this is

`LANE-g-621-freshness-absent.md`'s Done-contract had three items. Item 3 landed clean. Items 1
and 2 hit conflicts this lane's own V-2 decision budget reserves for escalation (classes b and
a) and were parked rather than forced through — each conflict was reproduced by actually running
the affected tests, not inferred.

## 2 · Landed: item 3 — BOTH tokens on `conformance-hub.js:133` repointed

`.claude/workflows/conformance-hub.js:133` named `VISION.md` (root file gone since `[#614]`
lane-e-5) and `protocols/ESSENTIALS.md` (superseded, pending `[#628]`) on one line. Fixed:

- `VISION.md` → `docs/archive/VISION.md`
- `protocols/ESSENTIALS.md` dropped from the scan list

`scripts/canonical_docs.py`'s `CONFORMANCE_V2_SCAN` — the Python-side counterpart the same test
checks against — updated in lockstep: `CANONICAL_RETIRED_LOCATIONS[VISION]` replaces the bare
`VISION` member, `ESSENTIALS_PATH` dropped.

**Verified:** `tests/test_canonical_docs.py` full run — 47 passed, including
`test_the_conformance_hub_scan_list_agrees_with_the_registry`. `git diff --stat`: exactly these
two files, `FRESHNESS_FILES` untouched, `validate_doc_claims.py` untouched (Done-contract item
4's constraint held by construction — nothing in this diff was ever near it).

## 3 · Escalated: item 1 — "absent freshness target FAILs, not skips"

Two implementations were tried, both reverted after empirical proof of breakage, not theory:

**Attempt A — flip `canonical_freshness_gate.evaluate()`'s absence handling from `continue` to
appending a FAIL.** REDs 4 tests on the first run: `test_evaluate_absent_file_skipped`,
`test_freshness_absent_file_skipped`, `test_gate_exits_0_when_fresh`,
`test_freshness_real_git_equal_date_passes`. Two of those are "TEETH" tests asserting a minimal
fixture (a repo with only `CLAUDE.md`) reads fresh — the blanket fix makes every OTHER
`FRESHNESS_FILES` member's legitimate absence (hub-only extras absent in a consumer, any
partial fixture) a hard FAIL. This is a Delta-A2 regression by the contract's own definition
("A REGRESSION exits non-zero and is a hard stop") and was reverted.

**Attempt B — a new registry-level guard test** (`FRESHNESS_FILES` member must exist on disk,
`@pytest.mark.live_repo`, no runtime behaviour change) — safe on its own, but it can only pass
once item 2 removes the currently-absent `VISION` member, so it rode with item 2's revert below
and was pulled too.

**Disposition:** parked. A workable version of item 1 likely needs either (a) a registry-only
guard test landed together with item 2 once item 2 itself is unblocked, or (b) an explicit
architect ruling on whether `evaluate()`'s absence handling should ever hard-FAIL, given how many
existing tests and the consumer-safety design (`docs`: "Missing `last_reviewed` -> WARN
(child-repo-safe)") depend on absence being tolerated.

## 4 · Escalated: item 2 — remove `VISION` from `FRESHNESS_FILES`

Removing `VISION` from `scripts/canonical_docs.FRESHNESS_FILES` cascades in two independently
fatal ways, both reproduced:

**a) `canonical_freshness_gate.py`'s literal fallback desyncs.** The module keeps a hand-written
copy of the freshness list for when it's deployed standalone to a consumer
(`DEFAULT_FRESHNESS_FILES`), and `tests/test_canonical_docs.py::test_freshness_gate_consumer_fallback_equals_the_registry`
asserts the two stay byte-equal. Fixable — sync the 2-line fallback — but that file is outside
this lane's frozen write-scope (`scripts/canonical_docs.py` + `conformance-hub.js:133` +
matching tests only). Escalated once; the operator authorized widening the scope for this one
file.

**b) `deploy/manifest-v1.1.0.yaml` and `manifest-v1.2.0.yaml` — released, tagged manifests —
desync from live state.** `deploy/release_lint.py`'s C7 check asserts these manifests' `doc_shapes`
(`VISION.md: {freshness_gated: true}`) stay in permanent agreement with the live
`canonical_freshness_gate.DEFAULT_FRESHNESS_FILES` constant. Removing `VISION` from the live
constant REDs 6 tests in `tests/test_release_lint.py`:
`test_live_hub_state_is_green`, `test_unmutated_copy_is_green`, `test_live_v120_state_is_green`,
`test_missing_tag_is_warn_not_fail`, `test_cli_green_exit_0`,
`test_injected_mismatch_fails_the_named_check[freshness-gated-set-drift]`. This is the exact
"retro-edit of a shipped spec" failure mode `canonical_docs.py`'s own docstring already names
for `CANONICAL_SPINE` changes, applied here to `FRESHNESS_FILES` — a **curated-baseline touch**,
decision-budget class (a).

**Operator decision on this second conflict:** stop the lane rather than retro-edit the released
manifests or leave `VISION` in the registry — land only the independently-clean item 3, escalate
items 1 and 2 for a revised contract. Both attempted implementations were reverted in full; the
final diff carries no trace of either.

## 5 · Amendment received mid-lane (R-G-A2)

A peer session (batch g contract review) relayed an operator amendment superseding this
contract's Delta A2 clause: no full-suite run in a lane, targeted tests only, the integrator
computes Delta A2 once at merge. This lane's own full-suite run (`uv run --locked pytest -q
--no-header`, 4841 passed / 28 failed / 11 skipped / 1 xfailed, 49m47s) had already completed by
the time the amendment arrived, so its data is recorded here rather than discarded:

- Compared against the committed base set (`docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`,
  13 nodeids): 3 fixed, 18 flagged REGRESSION.
- All 18 are environmental artifacts of running the full suite inside a worktree, not caused by
  this lane's diff — confirmed, not assumed:
  - 17× `tests/test_fleet_analytics.py::*` — `ModuleNotFoundError: No module named 'pandas'`.
    `pandas` lives in the opt-in `analytics` uv dependency group, absent from this worktree's
    venv. Installing it (`uv sync --locked --group analytics`) and re-running: all 17 pass.
  - 1× `tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` — fails
    because `_git_linked_worktrees` sees THIS worktree itself, plus every other concurrently-live
    lane worktree (`lane-g-276-deploy-waiver`, `lane-g-628-essentials-debless`, others), as
    "linked" relative to git's actual primary checkout — a property of running the suite from
    inside a worktree with sibling worktrees present, not of this lane's diff.
- No changes from this investigation were kept: the `--group analytics` install touched only the
  local venv (`git status` / `git diff --stat uv.lock pyproject.toml` confirm zero tracked-file
  change).

## 6 · What's in the final diff

```
.claude/workflows/conformance-hub.js   line 133 only -- both tokens repointed
scripts/canonical_docs.py              CONFORMANCE_V2_SCAN only -- FRESHNESS_FILES untouched
```

Targeted verification: `tests/test_canonical_docs.py` — 47 passed, 0 failed.

## 7 · Handback

Items 1 and 2 need an architect/operator ruling, not another lane guess:

- Item 2 (curated-baseline): retro-edit `manifest-v1.1.0.yaml`/`v1.2.0.yaml`'s `VISION.md`
  `freshness_gated` entries, or accept `VISION` stays in the live freshness set permanently, or
  some third option (e.g. C7 stops comparing `VISION.md` specifically once it's retired).
- Item 1 (rule-vs-ruling): whether Z-G4 ("FAIL, never skip") is meant to reshape
  `evaluate()`'s runtime absence handling — which this session's own instrumented test run shows
  is relied upon by consumer-safety design and several fixtures — or apply only at the registry
  level (a live-repo guard test, landable once item 2 is resolved).

G6 (the ESSENTIALS de-bless lane, ordered after this one per the frozen contract) can proceed
against `conformance-hub.js:133` as landed here.
