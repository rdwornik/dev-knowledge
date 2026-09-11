---
lane: w-278-impacted-test-selection
batch: W
row: "[#278]"
recorded: 2026-09-11
purpose: the lane's end-of-lane artifact — acceptance, the theatricality review, and the residual
---

# `[#278]` — lane close: impacted-test selection is live, and both ex-ante criteria hold

## 1. The archived intake's two ex-ante criteria, quoted verbatim

From `docs/intake/archive/2026-07-07-test-suite-hygiene.md` §*Acceptance criteria (ex-ante)*:

> - Ship-gate wall-time delta and collected-count delta after cleanup are both
>   measured against a **recorded baseline** (recorded before cleanup starts, not
>   reconstructed after).
> - The "why did it get faster" question is answered with evidence — not a guess —
>   before any cleanup work lands.

### Criterion 1 — discharged

The baseline was this lane's **first commit**, before anything changed:
`docs/audits/2026-09-11-technical-w278-ship-gate-baseline.md`. It records per-row HEADs and
timestamps, including a concurrent fast-forward that moved the base mid-capture — caught by
reading the branch reflog rather than trusting the session's memory of HEAD.

| | baseline (recorded first) | after this lane |
|---|---|---|
| collected tests | **5723** | **5744** (+21, this lane's own witnesses) |
| full suite, `-n auto --dist worksteal` | **1446.49 s** | unchanged — nothing was deleted |
| ship-gate `audit.py ship-gate` | 401 s, RED | unchanged |

**The wall-time delta this row exists to produce is on the SELECTED tier, not the full suite**,
because nothing was removed from the corpus. Measured on the live tree:

| diff shape | selected | wall | vs 1446.49 s full suite |
|---|---|---|---|
| leaf module (`scripts/offload_admission.py`) | 1 test file | **69.3 s** | **95 % saved** |
| docs-only (`JOURNAL.md`) | `live_repo` tier | **335.4 s** | **77 % saved** |
| hub-adjacent (`scripts/journal_anchor.py`) | 61 test files | **550.6 s** | **62 % saved** |

**The hub-adjacent row is the honest worst case and is reported as such.** `journal_anchor` is
imported by `audit.py`, which most test files import, so depth-3 closure reaches 61 of 174
files. That is 3× better than the full suite and nowhere near the 21.5-file mean measured over
the leg population — a mean over leaf-heavy diffs does not describe a hub module, so both
numbers are given.

**A confound, named rather than banked.** The recorded docs-only baseline was 809.11 s and this
run was 335.4 s for the same `live_repo` tier. That gap is **not** selection — it is
`--dist worksteal`, which the baseline row-4 invocation omitted. The savings column above
compares worksteal against a worksteal full-suite baseline, so it is like-for-like; the 809 s
figure is not evidence for this mechanism. **Separately actionable and NOT done here**
(out of this lane's footprint): adding `--dist worksteal` to the `/ship` docs-only tier looks
worth roughly 470 s on its own.

### Criterion 2 — answered with evidence, and the answer inverts the premise

The premise was: *"the suite recently got **faster** for reasons nobody has verified"*, and the
intake made verifying it a precondition. **Measured: the suite did not get faster.** Three
in-repo records, each a measurement rather than an impression:

1. **The one real speedup has a documented cause.** `-n auto` was adopted 2026-08-06 on a
   measured 5.2× — serial **1785.61 s**, `-n auto` **358.77 s** and **330.15 s** — with
   pass/fail/skip counts *identical across all three runs* (`pyproject.toml`; JOURNAL:21634).
   That is a verified cause, not a mystery.
2. **One "it got faster" impression was a wrong baseline.** `pyproject.toml`'s own comment
   corrects it: *"The previous note here claimed '~9m42s wall, 2026-07-05 profile' for the
   serial suite; the measured cost is ~3x that."*
3. **Another was a dead premise, already recorded as dead.** JOURNAL:19797 on intake #27 row 33:
   *"Both premises were dead — the measured serial baseline is 1785.61s, never 410s, and the
   suite is 2716 passing, never 2362."*

**Conclusion:** there was never an unexplained speedup to explain. The suite got *slower* in
absolute terms — 1446.49 s at 5723 collected, against 330–358 s at 2362 collected a month
earlier — and the "faster" impressions trace to two stale baselines plus one genuine,
attributed parallelism win. **No cleanup was ever justified by that premise**, which is why
this lane deleted nothing.

## 2. The theatricality review

The row's Done-when asks for this as a `docs/audits/` artifact; it ships here rather than being
dropped or escalated. The intake sets the bar: *"a theatricality finding must show the test
asserts nothing real, not merely that it's slow or old"*, and the scenario asks for findings
*"each with the evidence"*.

**Instrument.** The same per-test execution matrix the leg measurement used (`sys.monitoring`
PY_START over the full corpus): a test is a *candidate* when it executed **no repo `.py` file
other than its own module**. Such a test ran none of the code under test.

**Raw signal: 556 of 5723 nodeids (9.7 %) across 116 files.** That number is not a finding —
three false-positive classes had to be removed first, each verified by reading the code rather
than assumed:

| excluded | n | why it is not theatre |
|---|---|---|
| **subprocess** | 415 | the test spawns the script; execution is in a CHILD process, which in-process tracing cannot see. Read: `tests/test_assemble_paste.py` (37 of its 38) runs `scripts/assemble_paste.py` via `subprocess`. |
| **tree-assertion** | 115 | the test asserts on the CONTENT of markdown/YAML. It executes no repo `.py` by design, and in a governance repo that is the subject matter, not padding. |
| **declarative** | 19 | behaviour is enforced by a library. Read: `tests/test_desired_state_schema.py` tests real ADR-109 constraints, but the validating code is pydantic's, so the repo module contributes a class body at import and nothing at call time. |

**Survivors: 7 nodeids across 3 files — and all seven were read.**

```
tests/test_proof_layer.py::test_the_class_declares_its_relationship_to_583
tests/test_proof_layer.py::test_the_two_named_exemplars_are_declared
tests/test_seat_ch8.py::test_no_block_is_declared_and_then_read_by_nobody
tests/test_validate_substrate.py::test_adapter_grandfathers_the_two_later_armed_legs_by_their_own_date
tests/test_validate_substrate.py::test_both_new_legs_are_in_the_closed_rule_surface
tests/test_validate_substrate.py::test_leg7_is_in_the_closed_rule_surface_and_arms_at_freeze
tests/test_validate_substrate.py::test_rule_ids_are_the_closed_checkable_surface
```

**Verdict: NOT theatre — zero findings.** All seven are **closed-enum pins**: they assert that a
module-level constant tuple or set still has an exact expected membership. They execute no
function at call time because reading a constant runs no code, which is precisely why the
in-process signal flags them. They assert something real and load-bearing — that a closed
vocabulary has not changed silently — and they say so in their own words:
`test_rule_ids_are_the_closed_checkable_surface` documents that legs entered the tuple
*"deliberately — which is exactly what this pin exists to force: a new leg cannot arrive
silently."*

**This CONFIRMS the row's census note** (*"the theatricality pre-scan was CLEAN fleet-wide"*)
with an independent instrument, rather than restating it. **No test was deleted, altered or
skipped**, which keeps the intake's non-goals — *"No test deletion without operator review"* and
*"No coverage reduction disguised as cleanup"* — and core-invariant #3 intact.

**Honest limit of this review.** The instrument sees in-process execution only. It cannot rank
*assertion quality* inside a test that does execute source, so it bounds the padding question
from one side: it finds tests that ran no code. A test that runs code and asserts something
trivial is outside its reach, and no claim is made about that class.

## 3. What shipped

- `scripts/impacted_tests.py` — the selector. FPG-1 `imports` at depth 3 + a naming-convention
  rule; four mapping rules; fail-safe to the full suite on anything unrecognised.
- `tests/test_impacted_tests.py` — 21 witnesses, RED-first (recorded RED:
  `ModuleNotFoundError: No module named 'impacted_tests'`).
- `.claude/skills/verify/verify.py` + `SKILL.md` — selection live in the verify cadence, **tier
  A only**.
- `.pre-commit-config.yaml` — `impacted-tests-guard`, leg (b)'s refusal, scoped to `scripts/`
  with a 4-file grandfathered ratchet.
- Two measurement artifacts: the baseline, and the leg measurement carrying **both** legs'
  numbers.

## 4. Residual — what a reader should not have to discover

1. **Selection never replaces the full suite.** AW2-1 keeps *"the integrator keeps one full
   suite per integration as the net"*, and the selector's measured **4.8 % miss-rate** is
   acceptable only because that net exists. If tier B is ever dropped, this mechanism's
   justification goes with it.
2. **Hub-adjacent modules select broadly** — 61 of 174 files for `journal_anchor.py`. Depth is
   the dial (`DEFAULT_DEPTH = 3`), chosen on aggregate miss-rate; a future pass could weight by
   measured per-file cost rather than count.
3. **The coverage blind spot is shared, not solved.** 72.6 % of (test, script) path-string edges
   are invisible to in-process coverage; the AST pass sees them, which is why leg A won. The
   lane's own oracle has the same blindness, so the miss-rate is measured against a
   coverage-shaped truth and is disclosed as such.
4. **Two gates were bypassed, each declared in its own commit body, and both are discharged.**
   `SKIP=audit-index-freshness` on the artifact commits — the integrator is gate-of-record for
   the audits index (Q1). `SKIP=graph-orphan-census` on the selector commit — resolved one
   commit later by the real wiring; `orphan-census` now reports **OK**.
5. **`--dist worksteal` on the `/ship` docs-only tier** looks worth ~470 s and is NOT done here.
6. **The suite's 33 pre-existing failures are unchanged by this lane**, and a subset are
   worktree-context artifacts (`_SKIP_PARTS` contains `worktrees`), not tree defects.
7. **Pre-existing drift found and fixed during the mandated CLAUDE.md re-read.** Adding a
   hook obliged an A2 re-stamp, and `last_reviewed` means *"re-read end-to-end and confirmed
   accurate, or drift filed"* — so the file was read end-to-end rather than touched. §9's hook
   roster carries a machine-read marker (*"validate_doc_claims.extract_claimed_hooks takes the
   leading backtick id of every bullet … Keep it complete and contiguous"*) and was **missing
   four live gates** — `graph-rebuild`, `graph-orphan-census`, `graph-task-coverage`,
   `graph-process-list`, all landed under `[#664]` before this lane. They are added, so the
   roster now agrees with `.pre-commit-config.yaml` in both directions (verified by running
   `extract_claimed_hooks` against the config; both difference sets empty). Byte cap: 23945 of
   24576, 631 B headroom. This was outside the lane's subject but inside the file its own
   change forced it to certify — stamping accuracy over a known omission would have been the
   dishonest option.
