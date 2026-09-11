---
lane: w-278-impacted-test-selection
batch: W
recorded: 2026-09-11
purpose: the MEASUREMENT that chooses the impacted-test-selection implementation
legs-measured: BOTH — FPG-1 `imports` (leg A) and pytest-testmon (leg B)
verdict: leg A, FPG-1 `imports` at depth 3 plus a naming-convention rule
---

# `[#278]` — which selector, decided by a number

AW2-1 binds this choice to a measurement rather than a preference:

> Implementation is chosen by a number, not a preference: FPG-1 `imports` edges
> (existing organ — a CONNECT) versus an established pytest plugin
> (library-first), decided by measured miss-rate on this batch's own diffs,
> recorded in the lane's receipt.

and the contract adds the condition that makes the number mean something: *"The lane records
the miss-rate for BOTH legs, not only the winner's"*, and *"Measure precision alongside
miss-rate"*, because **a corpus-wide selector has a miss-rate of zero and a value of zero**.

## 1. The library-first survey came first

CLAUDE.md ranks an established dependency above hand-rolling, so the library leg was surveyed
before anything was built. Three candidates, resolved from PyPI metadata rather than memory:

| candidate | latest | released | mechanism | verdict |
|---|---|---|---|---|
| `pytest-testmon` | 2.2.0 | 2025-12-01 | coverage DB per test; selects tests whose covered files changed | **the real contender** — `pytest<10,>=5` admits our `>=9.0` floor |
| `pytest-picked` | 0.5.1 | 2024-11-06 | selects test files that are themselves changed, from git status | **answers a different question** — a changed `scripts/x.py` selects nothing |
| `pytest-incremental` | 0.6.0 | 2021-04-24 | AST import graph (the direct leg-A analogue) | unmaintained 4+ years, declares no `requires_python` |

Leg B is therefore `pytest-testmon`, and it was **measured, not argued about** — installed into
an ephemeral environment via `uv run --with`, which left `pyproject.toml` and `uv.lock`
byte-identical (verified).

## 2. The oracle, and its disclosed bias

Ground truth is a **per-test file-execution matrix**: for every test nodeid, the set of
repo-relative `.py` files whose code actually ran. Collected in ONE instrumented full-suite run
with a `sys.monitoring` (PEP 669) `PY_START` probe, the same strategy coverage.py's `sysmon`
core uses.

- 5723 nodeids traced, 5715 with a non-empty set, 172 test files, mean 2.49 files per test.
- Run wall 924.23 s, outcome **33 failed / 5682 passed / 8 skipped** — **identical** to the
  uninstrumented baseline, which is the evidence that the instrument did not perturb the suite.

**THE BIAS IS DISCLOSED RATHER THAN BURIED.** This oracle defines "impacted" as *executed
in-process*. `pytest-testmon` selects by that same definition, so **leg B scores at the ceiling
here by construction, not by merit.** Leg A (AST imports) is an independent definition and is
the one genuinely under test. A number whose bias is hidden decides nothing, so it is stated
before the table rather than after it.

## 3. The population

34 diffs, two populations kept separate on purpose:

- **W-*** — this batch's own lane diffs, which is what the Done-when names. Three of the four
  (W-1, W-5, W-7) are **docs-only**: batch W is 6/6 a process batch.
- **H-*** — the 30 most recent real code commits on `main` touching `scripts/`. Included
  because a miss-rate computed only over docs-only diffs measures nothing about a mechanism
  whose whole job is *source → covering tests*.

**31 of the 34 have a non-empty truth set and are the scored population.** The three that do
not are docs-only and are handled by a separate rule (§6).

## 4. The numbers

Micro figures pool over the 31 scored diffs; `sel_mean` is the mean number of test files
selected, against a corpus of **173**.

| leg | miss-rate | recall | precision (micro) | precision (macro) | sel_mean |
|---|---|---|---|---|---|
| leg A — depth 1 | 0.357 | 0.643 | 0.931 | 0.951 | 2.8 |
| leg A — depth 1 + convention | 0.341 | 0.659 | 0.933 | 0.967 | 2.9 |
| leg A — depth 2 | 0.111 | 0.889 | 0.228 | 0.742 | 15.9 |
| leg A — depth 2 + convention | 0.095 | 0.905 | 0.231 | 0.744 | 15.9 |
| leg A — depth 3 | 0.064 | 0.936 | 0.177 | 0.679 | 21.5 |
| **leg A — depth 3 + convention** | **0.048** | **0.952** | **0.180** | **0.680** | **21.5** |
| leg A — unbounded | 0.064 | 0.936 | 0.126 | 0.654 | 30.1 |
| leg A — unbounded + convention | 0.048 | 0.952 | 0.128 | 0.655 | 30.2 |
| **control** — corpus-wide | **0.000** | 1.000 | **0.024** | 0.024 | 173.0 |
| **leg B** — pytest-testmon | **0.000** | 1.000 | 1.000 | 1.000 | 4.1 |

**The corpus-wide control is in the table for a reason.** It posts a perfect miss-rate and is
worthless — precision 0.024. It is the contract's named trap, kept visible so every other row's
precision is read against it.

### Depth is the dial, and it was chosen by measurement

FPG-1's `imports` closure is transitive, and this repo has hub modules that most test files
import. Unbounded, *"tests that reach `scripts/fleet_health.py`"* returns **76 of 173 test
files** while the oracle says **7** — the closure travels test → `audit.py` → everything
`audit.py` reaches. Depth 3 is where miss-rate stops improving (0.064 → 0.064 from d3 to
unbounded) while precision keeps decaying, so paying more depth buys nothing.

### The residual misses have a NAMED cause, not just a value

Leg A's remaining misses are not diffuse. They concentrate on one idiom:

```
tests/test_fleet_health.py:15   _P = Path(__file__).resolve().parent.parent / "scripts" / "fleet_health.py"
tests/test_fleet_health.py:19   spec = importlib.util.spec_from_file_location("fleet_health", _P)
```

The filename is a string constant, but it sits in a `BinOp`, not in **call position** —
and `_import_targets` reads strings only in call position, deliberately, to avoid the
false-positive class the process-trigger census recorded (*"a regex pass counted any docstring
mention as a call site … 133 of 139 scripts came back 'triggered'"*). Widening the string rule
would reintroduce that blowup. A `tests/test_<x>.py` ↔ `<root>/<x>.py` **convention rule**
recovers exactly this class instead: **100 sources matched**, miss-rate 0.064 → **0.048**, and
precision *improves* (macro 0.679 → 0.680; 0.951 → 0.967 at depth 1) because the edges it adds
are true ones. It ships because of that number, not because it sounds sensible.

## 5. What the oracle cannot see — and why it decides the leg

Leg B posts 0.000 miss-rate **against a coverage oracle**. Its miss-rate against this repo's
actual dependency shape is a different number, and it was measured:

**72.6 % of (test, script) path-string edges are invisible to in-process coverage — 53 of 73
pairs.**

A test that runs `subprocess.run([sys.executable, "scripts/audit.py", …])` exercises that
script for real, in a **child process**, where coverage.py records nothing by default. **82 of
171 test files in this corpus use `subprocess`; 70 spawn python or a script directly.** Worse
for the coverage definition, a governance repo is full of tests that assert *on a source file's
text* — a dependency coverage cannot model even in principle, while an AST string reference
sees it exactly.

FPG-1 sees these edges because `_import_targets` resolves non-docstring string constants in
call position through `_resolved_targets`. **This is the asymmetry that decides the leg**, and
it is a property of this repo, not a general claim about the two techniques.

## 6. Leg B's operational cost, measured rather than asserted

| property | measured result |
|---|---|
| Installs against our pinned pytest | yes — `pytest 9.1.1` + testmon 2.2.0 coexist |
| xdist-compatible | **yes** — DB written under `-n 4`, second run deselects (an initial "no tests ran" was a warm DB, not an incompatibility; re-tested cold) |
| Warm-DB selection | **excellent** — 390/391 deselected in **1.29 s** |
| **Cold-DB bootstrap** | **212 s for 4 test files / 391 tests.** Linear extrapolation to 5723 tests ≈ **50 min** |
| New dependencies | **two** — `pytest-testmon` + `coverage<8,>=6`; an ADR-106 gated change |
| State | a machine-local `.testmondata` DB, untracked |

**The cold-DB cost is the disqualifier, and it is structural to this repo's working model.**
ADR-110 lanes each run in a *fresh worktree*. A fresh worktree has no `.testmondata`, so the
first run in every lane selects everything and pays a full instrumented suite before it returns
any benefit — a per-lane cost larger than the full suite the selection was meant to avoid.
Leg B is strongest exactly where this repo is weakest: a long-lived single checkout.

## 7. Verdict

**Leg A — FPG-1 `imports`, depth 3, plus the naming-convention rule.** Recorded miss-rate
**0.048**, precision (macro) **0.680**, mean selection **21.5 of 173** test files.

Chosen on four measured grounds, with leg B's numbers recorded alongside rather than omitted:

1. Leg B's 0.000 is **tautological** against a coverage oracle, and its real blind spot on this
   corpus is **72.6 %** of path-string edges.
2. Leg B costs ≈ **50 min of cold bootstrap per lane worktree**; leg A computes from AST in
   seconds and needs no persisted state.
3. Leg A adds **no dependency**; leg B adds two, gated under ADR-106.
4. Leg A is a **CONNECT to an existing organ** (FPG-1), which ADR-118 §1 prefers to a new one.

**A 4.8 % in-lane miss-rate is acceptable *because tier B exists*.** AW2-1 keeps *"the
integrator keeps one full suite per integration as the net"*, so an in-lane miss costs a later
catch, not an escape. Selection never replaces the full suite, and this verdict depends on that
remaining true.
