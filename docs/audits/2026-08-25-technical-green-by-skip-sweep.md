# Green-by-skip sweep — all 46 `ALL_CHECKS` members against one rule

**Date:** 2026-08-25 · **Lane:** X (`worktree-lane-x-failloud`) · **Class:** technical
**Authority:** `protocols/STANDING_RULINGS.md` section U (immutable), wave 1 · Serves `[E4]`/`[E7]`

**The rule swept for:** *a check that cannot compute its ground truth must FAIL, never skip.*

---

> ## PATH RENAME — read before citing this file
>
> | | path |
> |---|---|
> | **contract-frozen (does NOT exist)** | `docs/audits/2026-08-25-green-by-skip-sweep.md` |
> | **landed (cite this)** | `docs/audits/2026-08-25-technical-green-by-skip-sweep.md` |
>
> The frozen name carries no enum class token after the date, so the
> `validate-hermetization` **Rule B** pre-commit gate (ADR-101 R3/R4) refuses it. Measured,
> not assumed — `validate_hermetization.rule_b_violation()` returns for the frozen name:
>
> ```
> class: '2026-08-25-green-by-skip-sweep.md' has no CLOSED-enum <class> token after the
> date (ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/
> conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence;
> whole-token longest-match)
> ```
>
> and `None` (clean) for the landed name. Escalated rather than absorbed, per the recorded
> 2026-08-08 ruling that *"contracts and prompts are not authority over this gate"* and
> *"the gate outranks the contract text, and you say so out loud"*.
>
> **Operator ruling, 2026-08-25:** rename; record the mapping prominently; **the sibling
> lane's citation is repaired at INTEGRATION** (lane G merges before lane X). Lane X did
> **not** touch the sibling lane. The contract's slug is preserved intact — only the class
> token is inserted.

---

## 0. What "green" means here — the measurement this sweep turns on

The rule is unusable until "reports green" is defined mechanically, so this was measured
first and everything below is classified against it.

`Finding.status` has five values, and they are **not** five degrees of severity:

| status | renders as | `_check_outcome` projects to | blocks a commit (`audit-health`) | blocks a ship (`ship-gate`) |
|---|---|---|---|---|
| `fail` | FAIL | `block` | **yes** | **yes** |
| `warn` | WARN | `pass` | no | **yes, while undispositioned** |
| `unavailable` | **N/A** | `pass` | no | no |
| `n/a` | N/A | `pass` | no | no |
| `pass` | PASS | `pass` | no | no |

Sources: `scripts/audit.py::_STATUS_LABEL` / `_STATUS_EMOJI`; `_check_outcome`
(*"`fail` is the only status that stops a commit at `audit-health` or a ship at
`ship-gate`"*); `cmd_ship_gate`, whose verdict block is literally
`if fails or undispositioned:` → `sys.exit(1)`.

Two consequences drive every verdict below:

1. **`warn` has teeth.** An undispositioned WARN REDs the ship-gate. So the large
   `except Exception -> Finding(..., "warn", "check degraded …")` family is **loud**, not
   green. It does not satisfy the rule's letter (which says FAIL) but it does satisfy its
   purpose: the arc cannot ship while pretending the check ran.
2. **`unavailable` is green.** It renders as *N/A* and projects onto `pass`. Nothing blocks.
   A check reporting `unavailable` because it could not compute ships clean.

**This is not a new reading.** The house already made this exact call once and never swept
it — `scripts/audit.py::check_silent_rule_ratchet`:

> ```
> # FAIL, not "unavailable" (terra HIGH, 2026-07-27): ship-gate blocks only on `fail`
> # and undispositioned `warn`, so an "unavailable" detector would ship GREEN having
> # measured nothing at all.
> ```

The sweep is therefore the application of a **landed 2026-07-27 precedent** to the other 45
members, not the invention of doctrine.

**The counter-rule, stated because over-applying is the other failure.** A check whose
**subject is absent** is *inapplicable*, not *failed*. `no docs/handoffs/`, `no BACKLOG.md`,
`hub-only — not the hub repo` are correct `n/a`s: nothing was measured because there was
nothing to measure. Turning those into FAILs would red every consumer repo for checks never
meant to run there. **Failed-to-compute and nothing-to-compute are different events and must
keep different statuses.** Both directions are pinned by tests.

---

## 1. Classification — all 46

Method: each member's AST was walked for every `Finding(...)` / `_na(...)` verdict and every
`ExceptHandler`, and each non-`pass` exit read against §0. Not a grep for the word "skip" —
neither fixed instance contains it.

**Totals: 32 CONFORMS · 10 N-A · 4 VIOLATES** (2 fixed here, 2 deferred).

### CONFORMS (32)

Either no uncomputable path exists, or every such path exits `fail` or a loud `warn`.

| # | check | how it degrades |
|---|---|---|
| 1 | `vision_md` | `except yaml.YAMLError -> fail` |
| 6 | `workspace_settings` | `except (JSONDecodeError, ValueError) -> fail` |
| 8 | `canonical_freshness` | no swallowing handler — an IO error propagates as `error` |
| 14 | `amendment_coherence` | no swallowing handler |
| 16 | `hooks_armed` | `except Exception -> warn` — see caveat C-1 |
| 17 | `git_backlog_drift` | `except Exception -> warn` |
| 18 | `doc_claims` | `except Exception -> warn`; `not-computed -> warn` (added this lane) |
| 19 | `no_ff_merges` | `except Exception -> warn` |
| 20 | `handoff_probes` | `except Exception -> warn` |
| 21 | `reconciled_versions` | `except Exception -> warn` |
| 22 | `doc_rot` | `except Exception -> warn` |
| 23 | `doc_structure` | `except Exception -> warn` |
| 24 | `doc_code_edge` | `except Exception -> warn` |
| 25 | `safe_removal` | `except Exception -> warn` |
| 26 | `residual_completeness` | `except Exception -> warn` |
| 27 | `deployed_methodology_version` | `except (OSError, yaml.YAMLError) -> warn` |
| 28 | `enforcement_coverage` | `except Exception -> warn` (its `except ImportError` is an import shim, not a swallow) |
| 29 | `undeclared_edges` | `except Exception -> warn` |
| 30 | `doc_code_coverage_drift` | `except Exception -> warn` |
| 32 | `fleet_parity` | `except Exception -> warn` (+ import shim) |
| 34 | `silent_rule_ratchet` | `except (…) -> fail` — **the precedent this sweep applies** |
| 35 | `task_tree_coherence` | `except (OSError, ValueError, KeyError, UnicodeDecodeError) -> fail` |
| 36 | `intake_tree_coherence` | `except Exception -> fail` |
| 37 | `boot_byte_budget` | `except OSError -> warn` |
| 39 | `membership_agreement` | three handlers, all `-> fail` |
| 40 | `journal_spine_anchor` | `except Exception -> fail` (*"an unknown anchoring state is not a clean one"*) |
| 41 | `journal_day_letters` | `except OSError -> fail` |
| 42 | `preflight_backlog_ids` | `except Exception -> warn` (+ import shim) |
| 43 | `review_artifact_coverage` | `except Exception -> warn` (+ import shim) |
| 44 | `landing_predicate` | `except Exception -> warn` |
| 45 | `adr_status_grammar` | **exemplar — see below** |
| 46 | `funnel_coverage` | `except Exception -> warn` |

**#45 `adr_status_grammar` is the model implementation** and is worth copying. On an
unreadable ADR index it neither skips nor fails the whole check: it records
`index_error = "ADR index unreadable (…) — coherence leg DID NOT RUN"`, **skips only that
leg**, then forces a non-green verdict for it (`if warns or index_error:` returns WARN
carrying the text). A partial run is reported as partial, **by name**, and cannot reach
`pass`. That is the shape the rule actually wants: per-leg honesty, not all-or-nothing.

### N-A (10) — no external ground truth to fail on

Presence/structure checks whose only non-verdict exit is subject-absent.

| # | check | the `n/a` |
|---|---|---|
| 2 | `adr38_baseline` | — |
| 3 | `claude_md` | — |
| 4 | `dot_prefix_discipline` | — |
| 5 | `canonical_md_visibility` | — |
| 7 | `handoff_bundle_structure` | `no docs/handoffs/ — nothing to validate` |
| 9 | `generated_artifact_freshness` | `ship-gate-only leg -- skipped at the audit-health commit gate` |
| 11 | `stale_worktrees` | `git unavailable or not a repo` |
| 12 | `canonical_structure` | — |
| 13 | `handoff_version_stamp` | `no protocols/HANDOFF_PROCESS.md` |
| 15 | `floor_integrity` | `no .claude/CLAUDE-FLOOR.md` |

**#9 is a deliberate scope ruling, not a skip** (ADR-86 amendment 2026-08-23): the leg is
ship-gate-only and says so. Same shape as `validate_doc_claims`' `pytest_collected` running
off-gate — a check that declares *where* it runs is not a check that failed to run. Recorded
so a later reader does not "fix" it.

### VIOLATES (4)

| # | check | site | what it does | disposition |
|---|---|---|---|---|
| 33 | `routine_consumers` | `scripts/audit_checks/check_routine_consumers.py:117` | `unavailable` when BACKLOG.md exists but is unreadable | **FIXED** |
| 38 | `fleet_audit_replication` | `scripts/audit.py:2693` | `unavailable` when `git rev-list` fails | **FIXED** |
| 31 | `import_edges` | `scripts/audit.py:2139-2141` | silent `continue`, then **`pass`** | **DEFERRED — F-1** |
| 10 | `no_sibling_orphans` | `scripts/audit.py:786-787` | `unavailable` on an unreadable parent dir | **DEFERRED — F-2** |

**Locators.** The two FIXED rows cite their **pre-fix** positions (that is where the defect
was). The two DEFERRED rows cite **current** positions on this branch, re-resolved after
this lane's own edits shifted `audit.py` — a deferred finding is acted on by someone else,
so its locator has to resolve. Stated because the governance-drift audit's own replacement
locator was off by one, and the rule binds the auditor too.

---

## 2. Fixes applied

**#33 `routine_consumers`** — `"unavailable"` → `"fail"`. The absent-file case is already
`NOT-APPLICABLE` on the line above, so reaching the handler means the file **exists and
could not be read**: a failed computation of an available ground truth. One-liner. The
counter-rule leg (absent BACKLOG stays `n/a`) is pinned by a test so the fix cannot be
over-applied into a false gate on consumer repos.

**#38 `fleet_audit_replication`** — `"unavailable"` → `"fail"`. Both refs are verified before
that line, so git works and the repo is intact; `rev-list` failing there is a real defect.
Notably the branch **immediately above it in the same function** had already refused this
exact reasoning for the never-replicated case (codex HIGH 2026-08-01: *"Returning `n/a` here
would disable the backstop in exactly the never-replicated case it exists for"*). The
function argued the sweep's position against itself and then did not apply it one branch
later.

Both are the ruled one-liner class. Both verified not to red the live tree.

## 3. Violations deferred — findings, not fixes

Deferred because the contract admits fixes **only** where they are fail-closed one-liners.
Neither of these is; both need a shape change, not a status word.

### F-1 · `import_edges` — the most severe instance in the registry

`scripts/audit.py:2139-2141`:

```python
try:
    text = current.read_text(encoding="utf-8", errors="replace")
except OSError:
    continue
```

An unreadable file in the `@import` walk is **dropped from the walk entirely**. `file_count`
never increments, so the file leaves no trace, and the check then returns:

```python
return [Finding(name, "pass", f"{edge_count} @import edge(s) resolve across {file_count} file(s)")]
```

This is worse than every other instance in this sweep: not a greenish `unavailable` but an
actual **`pass`**, whose evidence states a file count that silently excludes the files it
could not read. A reader has no way to tell a clean walk from a half-walk.

**Why not fixed here:** the fix accumulates unreadable paths and folds them into the verdict
(~5 lines across two sites), past the contract's one-liner bar.
**Fix shape when taken:** mirror `adr_status_grammar` (#45) — keep walking, collect the
names, and refuse `pass` while the list is non-empty.

### F-2 · `no_sibling_orphans` — one of its two `unavailable` exits

`scripts/audit.py:786-787` returns `unavailable` when the parent directory is unreadable. That
is a failed computation (the siblings exist; they could not be listed) and it ships green.

Its *other* exit, `:778-779` (`git unavailable or not a repo`), is a genuine precondition and is
correctly inapplicable — but it spells that **`unavailable`** where the adjacent
`stale_worktrees` spells the **identical** condition **`n/a`**. Both render as "N/A", so
nothing is mis-gated today, but the two words mean different things in this codebase
(`audit.py:3920`: *"`unavailable` = path-absent / couldn't run; `n/a` = ran but not
applicable here"*). Splitting `:786` → `fail` and `:778` → `n/a` is the coherent fix; two
decisions, not a one-liner.

### C-1 · caveat, not a violation · `hooks_armed`

`audit.py:1109` maps *any* non-zero `git rev-parse --git-path hooks` to
`n/a "not a standard git checkout"`, conflating "this is not a git repo" (inapplicable) with
"git failed" (uncomputable). Low severity — in the hub the command does not fail — but it is
the same conflation F-2 names.

---

## 4. Wall-times — and why the substrate leg of this lane is NOT discharged

**The contract mandated a Codespaces devcontainer** (*"MANDATORY … this lane doubles as the
substrate measurement"*). **This lane ran on the local Windows 11 workstation instead**
(`$CODESPACES` empty, `OS=Windows_NT`). Every number below is therefore a *local* number and
**the D1 substrate question is not answered by this lane.** Recording them as devcontainer
measurements would have falsified the record — the one outcome worse than not measuring.

They are also **contended, not clean**. Mid-lane process inspection found **two sibling lane
sessions and the primary checkout** running `audit.py health` concurrently
(`lane-cs-codespace-transport`, `lane-g-governance`, `.dev-knowledge` primary). These numbers
measure *this machine under a 3-way parallel-lane load* — a real operating condition, but not
a substrate baseline.

| measurement | value | notes |
|---|---|---|
| lane session start | `2026-08-25T18:19:45Z` | worktree already provisioned |
| codespace provision-to-ready | **not measured** | no codespace — leg not discharged |
| first full `pytest` | **abandoned** | started `18:24:22Z`, killed ~25 min in, unfinished: self-contended (a second suite was launched against the same tree) and then invalidated by mid-flight edits. Recorded as abandoned rather than reported as a number. |
| **final full `pytest`, lane branch** | **1722.9 s** (28 m 43 s) | 3976 tests; clean single run |
| **full `pytest`, pristine `main` baseline** | **1923.6 s** (32 m 04 s) | same interpreter, detached worktree at `436e7375` |
| `audit.py health` (standalone, whole tree) | **625.6 s** (~10 m 26 s) | this IS the pre-commit commit tax |
| commit 1 (hook-inclusive) | ~6 min | landed `21:50:59+02:00`; start not stopwatch-precise |
| **commit 2 (hook-inclusive)** | **296.0 s** (~4 m 56 s) | stopwatch-measured |
| **commit 3 (hook-inclusive)** | **241.6 s** (~4 m 02 s) | stopwatch-measured |
| `pytest test_audit.py test_doc_code_edge.py` | **1648.9 s** (~27 m 29 s), 260 tests | serial (`-n 0`) |
| 2 tests, pristine detached worktree | **618.0 s** | one of them runs the full audit |
| targeted lane tests (4 files, 88 tests) | **28.8 s** | serial |
| `test_fleet_audit_replication.py` (14 tests) | **76.6 s** | serial; real git fixtures |

**The one substrate observation this lane can honestly make:** running on Windows was an
*advantage* for step 1. The contract anticipated that the cp1252 crash "reproduces only on a
bare Windows console" and instructed reproducing it in the devcontainer via an ASCII-forced
encoding test. On this substrate it reproduced **natively** —

```
$ PYTHONIOENCODING=cp1252 uv run --locked python scripts/audit.py checks
UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 30
```

— so the fix was verified against the real failure mode rather than a simulation of it. A
devcontainer run would have tested a proxy.

---

## 5. Judgment calls made under the decision budget

Recorded rather than escalated, per the contract (decide, record, batch).

**J-1 · Fail-closed is a per-claim property, not a blanket rule.** In `validate_doc_claims`
the single `actual is None` branch served two different events. Blanket-failing it would have
flipped `pytest_collected`'s *documented* fail-soft (*"an infra hiccup must not flap a
WARN"*) — a widening the contract forbids. Added `Claim.fail_closed` instead; a test pins the
boundary in both directions.

**J-2 · The new status is `not-computed`, not `unavailable`.** Discovered mid-lane that
`Finding.status` already has an `"unavailable"` value and that it is **green** (§0). Reusing
that word for a status which must not read as green would have imported exactly the wrong
connotation into a fix about connotations. *(Caught after an over-broad rename briefly
renamed the whole house vocabulary; reverted — `Finding`'s five values are untouched.)*

**J-3 · The CLI exits 1 on not-computed, but still 0 on a real mismatch.** Fail-loud applies
*only* to the did-not-run case. A `mismatch` exiting 0 is a recorded awareness-layer ruling
(2026-06-10 consolidation audit F1) and is outside the swept class. Verified this moves no
gate: the module is wired into no hook, and `verify_handoff_probes` is **resolve-only** — it
never executes probe commands — so the active bundle's P6 probe
(`python scripts/validate_doc_claims.py`) cannot red on the new exit code.

**J-4 · The adapter surfaces `not-computed` as WARN, not FAIL.** `check_doc_claims` has an
explicit never-FAIL posture (a separate ruling). Since the adapter always injects
`len(ALL_CHECKS)`, the branch is unreachable today; it exists so the status can never go
*silent* if a future claim is marked `fail_closed`.

**J-5 · Section U's stated mechanism for the cp1252 crash is off by one hop, recorded rather
than quietly worked around.** Section U attributes it to a `→` separator at `audit.py:4639`.
Measured: 4639's separator is an **em dash** (U+2014), which cp1252 encodes as 0x97 and which
never crashed. The crashing `→` (U+2192) is inside `check_doc_code_edge`'s **first docstring
line**, which 4639 interpolates. 4639 is the emit site, not the glyph's home. Section U is
immutable and was not edited; `[#470]` already had the mechanism right, and its Done-when
(ASCII swap + a cp1252-encodability regression over every `ALL_CHECKS` first docstring line)
is what was implemented. **`[#470]` is NOT closed by this lane** — row births and closures
belong to a sibling lane.

**J-6 · The `propose_closures` repair keeps exit 0.** `hooks.json` declares the Stop hook
non-blocking, and a detector that wedges session-end is a worse failure than one that reports
loudly. The repair is loud + diagnosable + non-destructive, not a new gate.

**J-7 · `import_edges` deferred despite being the worst instance.** The contract's one-liner
bar is a decision boundary, not a formality; a 5-line shape change is the operator's call.
Filed as F-1 with the fix shape pre-specified so taking it is cheap.

**J-8 · No `len(ALL_CHECKS) == 46` tripwire was added for the sweep.** Five such pins already
exist (`test_audit.py:2326`, `:2342`; `test_doc_code_edge.py:248`, `:715`;
`test_writer_integrity.py:185`) plus an order pin in `test_audit_parallel.py`. A sixth would
cost every future check another edit site while buying nothing the existing five do not
already force. The substantive guard added instead is **behavioural**: an AST test that fails
for any check reporting `pass` from an error handler, which covers checks added after this
lane with no roster to keep current.

---

## 6. Verification

| leg | result |
|---|---|
| `audit.py checks` under `PYTHONIOENCODING=cp1252` | **all 46 listed, exit 0** (was exit 1, `UnicodeEncodeError` at position 30) |
| `audit.py health` (working tree) | **OK** — the fail-closed changes do not red the commit gate (contract risk (b)) |
| targeted: detector-error + doc-claims + closures + twin-parity | **88 passed** |
| `test_fleet_audit_replication.py` | **14 passed** |
| `test_green_by_skip_sweep.py` + siblings | **passed** |
| full suite | **33 failed / 3922 passed** — every failure also fails on pristine `main` (39 there); zero introduced by this lane. Measured, §8 |

**One pre-existing RED, proven not this lane's.** `test_audit.py::test_health_stays_ok_with_na_status`
fails on `funnel_coverage` WARNs over undispositioned `2026-08-24` / `2026-08-25` audit
artifacts. Proven pre-existing by running it in a **detached worktree at pristine
`436e7375`** (main's tip, no lane changes) — it fails identically there. The worktree was
removed and pruned; `git worktree list` shows no stale entry.

A second failure (`test_doc_code_edge.py::test_coverage_drift_guard_registered_and_clean_on_live_repo`)
*was* this lane's, transiently: a background test run read `audit.py` mid-way through the
over-broad rename described in J-2. It passes on the corrected tree.

**Owed, not done here (deliberate).** `ecosystem/doc-counts.md:16` claims
`**3949 collected**`; this lane adds tests, so that claim now drifts. Not regenerated because
the contract restricts this lane's doc writes to *"the ONE frozen artifact path (+ its index
regen)"*, and sibling lanes are adding tests concurrently — one regeneration at integration
is correct, not three racing ones. Nothing is gated by it: `pytest_collected` is evaluated
only off-gate (`run_expensive`), so `audit-health` is unaffected; `audit.py run` will WARN
until regenerated.

## 7. terra review

`codex exec` (gpt-5.6-sol, read-only sandbox) over the lane's full diff `436e7375..HEAD`,
with the status semantics of §0 supplied as context so the reviewer could judge "ships
green" correctly.

**Severity tally: 0 CRITICAL · 1 HIGH · 0 MEDIUM · 0 LOW.** Counted from the artifact body,
not a console tally line.

### HIGH — ACCEPTED and FIXED · `_write_error_marker` still created a `PROPOSALS-*` husk

> *"When no same-day proposal exists, `_write_error_marker()` writes the error marker to
> `PROPOSALS-<date>.md` … `review_closures.latest_proposals()` selects the newest
> `PROPOSALS-*`, so a failed first run today can shadow yesterday's genuine pending
> proposals with an empty error marker."*

**Verified before accepting** — `scripts/review_closures.py:198-200` is exactly
`sorted(logs_dir.glob("PROPOSALS-*.md"))` → `files[-1]`. The finding stands.

The step-2 fix protected only a **same-day** proposals file, so it closed the
overwrite hole and left the shadowing one open. Three defects were actually live, and the
third is worse than the one terra named — it is this module's **own documented contract**,
`scripts/propose_closures.py:19-21`:

> *"ALWAYS writes `logs/PROPOSALS-YYYY-MM-DD.md` … The file's presence proves the detector
> ran; its **ABSENCE is the loud failure signal**."*

A husk written at that path makes the file **present while the detector did not run** —
the precise inversion of the signal the module promises. Terra found the shadowing; the
signal inversion surfaced when its fix direction was checked against the module docstring,
and it is the stronger reason.

**Fix:** the marker no longer occupies the `PROPOSALS-*` namespace at all — every failure
writes `DETECTOR-ERROR-<date>.md`. This closes all three at once and *restores* the
absence-signal: on failure, today's `PROPOSALS` file is absent (so the signal fires) and a
named diagnosis sits beside it. Applied to both copies. Tests rewritten to assert each hole
separately, including a dedicated regression for the yesterday-shadowing case terra named.

### Also corrected in the same pass (not terra findings)

* **Two deferred-finding locators were off**, because this lane's own `audit.py` edits
  shifted the file after the sweep measured it: F-1 `2139-2140` → **`2139-2141`**, F-2
  `:785` / `:777` → **`:786-787`** / **`:778-779`**, C-1 `:1106` → **`:1109`**. Re-resolved
  against the branch. A deferred finding is acted on by someone else, so its locator has to
  resolve — and the governance-drift audit's own replacement locator was itself off by one,
  which is precisely why this was re-checked rather than trusted.
* **The `len(ALL_CHECKS) == 46` tripwire was removed** — see J-8.

**Not executed by terra:** the checkout was read-only, so terra ran no tests. Every claim it
made was re-verified against the source here before being accepted.

## 8. Lane close — the full suite, measured against a controlled baseline

The suite is **not green**, and it is not green on `main` either. What matters is the
delta, so it was measured rather than asserted: the same interpreter (this lane's `.venv`)
was run against a **detached worktree at pristine `436e7375`** and against the lane branch,
and the two failure sets compared name-by-name.

| run | result | wall-time |
|---|---|---|
| lane branch `0263feed` | **33 failed · 3922 passed · 21 skipped · 1 xfailed** | 1722.9 s (28 m 43 s) |
| pristine `main` 436e7375 | **39 failed · 3888 passed · 21 skipped · 1 xfailed** | 1923.6 s (32 m 04 s) |

**Every one of the lane's 33 failures also fails on pristine `main`. The lane introduces
zero new failures**, and `main` carries six *more* that the lane branch does not.

The 33, by file, with why each is not this lane's:

| n | file | cause |
|---|---|---|
| 17 | `test_fleet_analytics.py` | `ModuleNotFoundError: No module named 'pandas'` — the lane venv lacks the `analytics` dependency group. Environmental; identical count on both sides. |
| 9 | `test_nopack_sandbox.py` | `rc=127`, absent sandbox tooling on this host. Environmental. |
| 2 | `test_verify_handoff_probes.py` | `tool absent: sed` — not on PATH in this shell. Environmental. |
| 1 | `test_stale_worktrees.py` | the known worktree-hostile reader test: running the suite *from* a linked worktree REDs it. |
| 1 | `test_enforcement_coverage.py` | the anchor-gate probe test, RED on `main` since 2026-08-22. |
| 1 | `test_validate_doc_rot.py` | live-corpus accretion findings — pre-existing corpus state. |
| 1 | `test_funnel_coverage.py` | `test_committed_baseline_agrees_with_a_live_measurement` — see below. |
| 1 | `test_audit.py` | `test_health_stays_ok_with_na_status` — separately proven pre-existing on a detached run at `436e7375`. |

**The six `main`-only failures** — `test_telemetry_wiring.py` (3), `test_export_backlog_view.py`,
`test_boundary_report.py`, `test_audit_parallel.py` — are in files this lane never touched.
The two runs used different test orderings (the lane run random, the baseline
`-p no:randomly`), which is the honest explanation for an order-sensitive difference; it is
recorded rather than claimed as an improvement this lane made.

**`test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement` deserves
its own note, because this lane adds a `docs/audits/` file and that is exactly what the
check watches.** It fails on pristine `main` too: `audit.py health` already reports ~15
artifacts dated 2026-08-24/25 as *"carries no disposition and is not in the arm-time
baseline"*, so the committed `ecosystem/audit-funnel-baseline.json` was already out of step
with the corpus before this lane existed. This artifact adds one more name to a set that was
already non-empty — it does not create the failure. **Re-arming that baseline, or writing
disposition rows for the 2026-08-24/25 batch, is a governance act this lane is contracted
not to perform** (`ecosystem/` registries and the disposition ledger are both on the
do-not-touch list). **OWED at integration**, alongside the `doc-counts.md` regeneration
noted in §6.

`audit.py health` — **OK** on the final branch state, so the pre-commit gate the fleet
actually runs on is green; the five lane commits each passed it at commit time.
