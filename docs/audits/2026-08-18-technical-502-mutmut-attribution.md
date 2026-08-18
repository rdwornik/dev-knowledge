# [#502] — why the mutation pilot measured nothing, and the one-string repair · 2026-08-18

**Lane E findings artifact.** Contract of record:
`docs/audits/2026-08-18-technical-502-mutmut-lane-contract.md` (commit `2bc1ea6c`, which also
records the operator's D7 grant for the `pyproject.toml` touch). Scope: repair the pilot so
`[#502]`'s verdict leg gets an input. **No ADOPT/REJECT is recorded here — that ruling is the
architect's, and this lane deliberately writes none.**

**Headline:** the pilot now attributes. CI run
[32140001292](https://github.com/rdwornik/dev-knowledge/actions/runs/32140001292) on `a2e9a0eb`
checked **2291 of 2291** mutants (was 0 of 2291), `mutmut run` exit **0**, in **9m28s** against a
30-minute budget. **1210 mutants survived.**

---

## 1. The mismatch mechanics

mutmut attributes a mutant to a test only where two independently derived names agree. In this
repo they did not, and neither half was wrong on its own terms:

| half | derived from | value here |
|---|---|---|
| **mutant key** | the SOURCE PATH | `scripts.fleet_analytics.x_main__mutmut_39` |
| **stats key** | the LOADED MODULE | `fleet_analytics.x_main` |

**The mutant key comes from the file path.** `mutmut/utils/format_utils.py::get_mutant_name` is
the whole of it:

```python
module_name = str(relative_source_path)[: -len(relative_source_path.suffix)].replace(os.sep, ".")
module_name = strip_prefix(module_name, prefix="src.")
mutant_name = f"{module_name}.{mutant_method_name}"
```

With `source_paths = ["scripts"]` the walker yields `scripts/fleet_analytics.py`, so every one of
the 2291 mutants is keyed `scripts.fleet_analytics.<fn>__mutmut_N`. The single rename mutmut ever
performs is that hardcoded `src.` strip.

**The stats key comes from the module object.** During the stats pass mutmut sets
`MUTANT_UNDER_TEST=stats` and the trampoline injected into each mutated function records
(`mutmut/mutation/trampoline.py`):

```python
orig_qual_name = f"{orig_func.__module__}.{mangled_name_from_mutant_name(orig_func.__name__)}"
record_trampoline_hit(orig_qual_name, caller=caller_name)
```

`orig_func.__module__` is whatever name **Python** knows the module by — chosen by whoever loads
it. `tests/test_fleet_analytics.py` does not import `fleet_analytics` at all; it loads the file
directly, and hardcoded the name:

```python
_P = Path(__file__).resolve().parent.parent / "scripts" / "fleet_analytics.py"
spec = importlib.util.spec_from_file_location("fleet_analytics", _P)   # <- the defect
```

**So attribution was zero.** `run_mutation_tests` looks a mutant's tests up as
`tests_by_mangled_function_name.get(mangled_name_from_mutant_name(mutant_name))` — a lookup of
`scripts.fleet_analytics.x_main` in a dict whose only keys are `fleet_analytics.*`. Empty for
every mutant. `mutmut results` then printed all 2291 as `not checked`, which is indistinguishable
from "the pilot ran and found nothing".

Two details make this a *naming* defect rather than a *coverage* defect:

- **The tests were already loading the MUTATED file.** `_P` is `__file__`-relative and mutmut runs
  pytest with cwd = `mutants/`, so `_P` resolved to `mutants/scripts/fleet_analytics.py`. The
  phase-0 run recorded real trampoline hits. Only the name was wrong. The defect was one string.
- **mutmut 3.7.0 diagnosed itself.** `_check_test_to_mutant_associations` exists for exactly this
  case and fired in run 32127150367 (`__main__.py:1411`, immediately after mutant collection and
  *before* the clean-test run and the mutant loop — so the run halted there and the per-mutant
  "no tests" exit code 33 was never reached; the mutants stayed at `None`, which is what prints as
  `not checked`):

  ```
  Stopping early, because tests recorded trampoline hits but none match any mutant key.
  It looks like tests import the source under a different module path than mutmut sees
  from the file path.
  Recorded keys (e.g.): ['fleet_analytics.x__git', 'fleet_analytics.x__git_common_dir', ...]
  Expected keys (e.g.): ['scripts.fleet_analytics.x__atomic_write', 'scripts.fleet_analytics.x__git', ...]
  Fix: use fully-qualified package imports (e.g. from pkg.foo import ...) and rely on
  mutmut's default sys.path setup.
  ```

  This artifact's diagnosis is therefore not a reconstruction — the tool named the defect and the
  remedy in the pilot's own log. **That line was present in the phase-0 evidence and was not
  read.** The lesson is cheaper than the mechanism: two burned scopes were spent inferring a cause
  the tool had already printed. (The correction is recorded because it is the useful part; the
  STEP-2 commit body `a2e9a0eb` says the mutants were "assigned exit code 33", which overstates —
  the run halted before the loop that assigns it. The diagnosis and the fix are unaffected.)

### The correction to the `-n 0` story

The `[tool.mutmut]` comment block attributed the earlier 84-mutant / all-`not checked` outcome to
`addopts = "-n auto"` making every mutant's pytest exit 4 on `unrecognized arguments: -n`, fixed
by `pytest_add_cli_args = ["-n", "0"]`. **That diagnosis was correct and the fix was real.** It was
simply not the only cause: a second, independent defect produced the *same* visible output and
survived it. That is why the 84-mutant and 2291-mutant scopes both read as green-while-measuring-
nothing — `not checked` was never diagnostic of its cause. Both notes now sit in `pyproject.toml`,
the older one corrected in place rather than deleted.

---

## 2. Why the fix is not in `[tool.mutmut]`

The contract prefers config over code, so this was checked rather than assumed. mutmut 3.7.0's
`Config` dataclass was enumerated field by field:

`also_copy` · `only_mutate` · `do_not_mutate` · `do_not_mutate_patterns` · `max_stack_depth` ·
`debug` · `source_paths` · `resolved_mutated_source_paths` · `pytest_add_cli_args` ·
`pytest_add_cli_args_test_selection` · `mutate_only_covered_lines` · `timeout_multiplier` ·
`timeout_constant` · `type_check_command` · `use_setproctitle` · `track_dependencies` ·
`dependency_tracking_depth` · `cache_invalidation_files` · `cache_invalidation_exclude` ·
`on_dependency_change` · `use_git_change_detection`

**There is no module-naming key.** Three config-side routes were considered and rejected:

1. `source_paths = ["scripts/fleet_analytics.py"]` — `walk_all_files` yields the file path
   unchanged, so the derived name is still `scripts.fleet_analytics`. No effect.
2. `source_paths = ["."]` — derives `..scripts.fleet_analytics`, strictly worse, and widens the
   mutation scope past the slice the contract fixes.
3. Relocating the slice under `src/` to reach the hardcoded `src.` strip — the only rename mutmut
   offers. It is a tree move far outside this lane's footprint and would break
   `fleet_analytics.py`'s own `sys.path.insert(0, _SCRIPTS_DIR)` bootstrap for `audit` / `gitenv`.

The existing `[tool.mutmut]` scoping was **already correct** and is functionally unchanged. The
alignment can only happen where the name is chosen: the loader.

---

## 3. The exact diff

**`tests/test_fleet_analytics.py`** — the narrowest possible shim. Not one import statement moves,
not one assertion or call site changes, `fa` stays the handle for all 76 tests:

```python
+_MODNAME = "scripts.fleet_analytics"
+
+
 def _load():
-    spec = importlib.util.spec_from_file_location("fleet_analytics", _P)
+    spec = importlib.util.spec_from_file_location(_MODNAME, _P)
     module = importlib.util.module_from_spec(spec)
     # Register before exec so module-level @dataclass can resolve cls.__module__.
-    sys.modules["fleet_analytics"] = module
+    sys.modules[_MODNAME] = module
+    sys.modules["fleet_analytics"] = module   # keep the bare name on the same object
     spec.loader.exec_module(module)
     return module
```

The bare-name alias is deliberately kept: `tests/test_gitenv.py` does a plain
`import fleet_analytics`, and when the two modules share a session that registration is what it has
always resolved to. Dropping it would silently change that test's subject. mutmut reads
`__module__`, not `sys.modules` keys, so the alias costs nothing.

**`pyproject.toml`** — the D7-approved touch, **comment-only**; no key's value changes. It records
where the module name comes from, that this table cannot set it, and the `-n 0` correction above.

Both landed in commit `a2e9a0eb`, which is the SHA the successful pilot ran against.

---

## 4. Local attribution numbers

`mutmut run` **cannot execute on this host**, and the row's CI-ONLY ruling is structural rather
than a printed warning — `mutmut/__main__.py` is unimportable on Windows behind *three* independent
walls: a `platform.system() == "Windows"` → `sys.exit(1)` gate (line 17), a top-level
`import resource` (POSIX-only, line 29), and a module-level `set_start_method("fork")` (line 1349,
raising `ValueError: cannot find context for 'fork'`). **That settles the row's open "`mutmut`
under `uv run --locked` is NOT VERIFIED" question in the direction the host ruling assumed, and
the CI run below settles the composition itself: `uv run --locked --with mutmut==3.7.0 mutmut run`
exited 0.**

The local proof is therefore a **fork-free harness** driving mutmut 3.7.0's own two halves
in-process: `create_mutants_for_file` (the real generator, writing the real trampolined file and
`.meta`) and then the generated trampoline itself under `MUTANT_UNDER_TEST=stats`, loading the
mutated file exactly as `_load()` does with the module name supplied as an argument.

**Stated limitation:** the three walls above are neutralised for the import (`platform.system`
faked, `resource` stubbed, `set_start_method` no-oped). All three are inert for what is measured —
no fork, no Pool, and `resource` is referenced exactly once, inside the forked mutant child at
`__main__.py:1487`, which this harness never reaches. **The harness proves the NAMING mechanics;
it does not and cannot show that a full `mutmut run` works on Windows.**

| loader module name | mutants generated | distinct fn keys expected | trampoline hits | keys matching | attribution |
|---|---|---|---|---|---|
| `fleet_analytics` (before) | 2291 | 37 | 4 | **0** | **ZERO** |

The generated count, 2291, is identical to the CI pilot's — which is what ties the harness to the
real thing. Recorded keys were `fleet_analytics.x__int_or_none`, `fleet_analytics.x__posix`,
`fleet_analytics.x_canonical_path`; expected keys were `scripts.fleet_analytics.x__atomic_write`,
`scripts.fleet_analytics.x__git`, … — intersection empty, reproducing CI exactly.

The after-case harness run is **not reported here**: it was still generating when this lane
stopped, and it has been superseded as evidence by §5, which measures the same property on the
real tool over all 2291 mutants rather than on three hand-picked calls. The harness removes its
`mutants/` tree and asserts the removal on exit (CLAUDE.md §5 rule 9); the completed run reported
`cleanup: mutants/ removed -> True`.

**Targeted suite:** `pytest -n 0 tests/test_fleet_analytics.py tests/test_gitenv.py` → **76 passed
in 86.98s**.

---

## 5. CI pilot re-run — the attribution actually works

**Run:** https://github.com/rdwornik/dev-knowledge/actions/runs/32140001292 (job `mutation-pilot`,
id 95720222054) · **ref** `worktree-lane-e-502-mutmut` · **SHA** `a2e9a0eb` ·
**`mutmut run` exit code 0**

**Wall clock 9m28s** (13:01:47Z → 13:11:15Z) against the declared `timeout-minutes: 30`, at
**4.24 mutations/second**. The budget question the pilot's brief made a precondition is answered:
the slice fits in under a third of it. Phase-0's 1m50s measured nothing, having halted before the
mutant loop.

| verdict | count |
|---|---|
| **checked** | **2291 / 2291** (phase-0: 0 / 2291) |
| killed 🎉 | 865 |
| **survived** 🙁 | **1210** |
| no tests 🫥 | 214 |
| timeout ⏰ | 2 |
| suspicious 🤔 | 0 |
| skipped 🔇 | 0 |
| caught by type check 🧙 | 0 |

`865 + 1210 + 214 + 2 = 2291`. **1210 is the surviving-mutant count over the pilot slice** that
`[#502]`'s "Done when" clause asks for.

**The calibration case fired.** `[tool.mutmut]`'s own note predicted that a mutant flipping *which*
node `canonical_path` returns should SURVIVE, because `test_canonical_path_survives_a_cycle`
asserts `in {"a","b"}` where the correctness assertion is `== "b"`. Two survivors are recorded:

```
scripts.fleet_analytics.x_canonical_path__mutmut_1:  survived
scripts.fleet_analytics.x_canonical_path__mutmut_10: survived
```

This is reported as an **observation, not a verdict** — the prediction the pilot was built to test
came true, and what that implies for ADOPT/REJECT is the architect's call.

---

## 6. What this lane did NOT settle

- **No ADOPT/REJECT.** The architect's ruling, out of scope by contract.
- **The survivor list is not triaged.** 1210 survivors is a raw count. How many are equivalent
  mutants, how many are real assertion gaps, and which ones matter is a reading of the artifact
  (`mutation-pilot-<sha>`, 90-day retention), not a repair.
- **The 214 "no tests" mutants are unexplained.** They are functions the selected test file never
  reaches — expected for a single-file test selection over a 56KB module, but not investigated.
- **The pilot ran on a lane branch, not `main`.** The fix must merge before `main` produces this
  result; the run above is evidence about the fixed code, not about `main`'s current state.
