# Test-seam re-point analysis for the `audit.py` decomposition — what actually blocks extraction, and the smallest diff that frees the two `[#533]`-motivating checks

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16
- **Source-session:** night-batch nb5-A, branch `claude/nb5-seam-repoint-analysis-lmaspu`, cut from `main` @ `43cd1cee` (the D-1v2 amendment merge)
- **Status:** DRAFT — PROPOSAL-ONLY. Zero edits to `scripts/` or `tests/` in this branch; the only file this session adds to the tree is this report.
- **Model:** claude-opus-5, effort high
- **Inherited-vs-measured:** Lane m's headline (*25 of 43 checks unmovable*) is **INHERITED** as the question and **INDEPENDENTLY RE-DERIVED** here — this run reproduced 25/43 from the live tree without reading m's packet, which is not in this branch. Everything else is **MEASURED THIS RUN** against `43cd1cee`: the patch-site enumeration (AST parse of all 99 test modules), the seam classification (AST call-graph over `scripts/audit.py`), and — the load-bearing part — a **working prototype extraction executed and tested in a scratchpad copy**, not a proposal reasoned about on paper. Three named failure modes below were found by running the extraction, not by reading it.

---

## Bottom line

**The 25 checks are not unmovable, and the two that matter are the cheapest of them.** A prototype extraction of `check_hooks_armed` + `check_stale_worktrees` was built and run this session: it reaches **byte-identical `audit.py health` output**, preserves `ALL_CHECKS` order and count (43), and lands on **exactly the baseline test result — 5 failed / 249 passed, the same 5 named failures — with ZERO test-file edits**.

Three things this run establishes that change the shape of `[#533]`:

1. **"Unmovable" is not a property of a check.** It is a property of *where the reader of the patched symbol lives*. `check_hooks_armed` — one of the two `[#533]`-motivating checks — extracts with **no test change and no seam re-point at all**, because the symbol its tests patch (`_REPO_ROOT`) is read by `_is_hub`, a shared helper that stays in the facade. Measured: 5/5 of its tests pass against a naive extraction.
2. **A naive extraction has three failure modes that no static reading of the tests reveals**, and one of them is silent. All three were hit by running it. The worst — the dual-import idiom producing **two live `audit` module objects in one process** — turns 11 tests green-but-vacuous rather than red. That is the risk lane m's "unmovable" framing was protecting against, and it is real; it just is not unfixable.
3. **The fix is one ~12-line accessor per extracted module**, plus mechanical `X` → `_f().X` rewriting of seam references inside the moved body. It generalizes: a third check with a different seam shape (`check_no_sibling_orphans`, which also drags two private helpers) was extracted the same way and also landed on baseline.

`seams 26 · smallest-diff files 6 · l/y unblocked yes` — with one caveat on l/y stated in §7 that the source extraction alone does **not** cover.

---

## 1. Method, so the numbers are checkable rather than asserted

Three passes, all re-runnable:

```
A. patch-site census   AST-parse every tests/test_*.py; find monkeypatch.setattr/delattr whose
                       target is the audit module (by alias) or an attribute reached through it.
                       -> 213 sites over 38 distinct symbols.
B. seam classification AST call-graph over scripts/audit.py: per check, the module-level names
                       read by the check body plus every helper PRIVATE to it (a helper used by
                       exactly one check moves with that check; a shared helper stays behind).
                       -> 25 checks of 43 read a symbol some test patches as a module global.
C. prototype           Copy the repo to a scratchpad, actually perform the extraction, run the
                       suite against BOTH copies, diff the results and the CLI output.
                       -> the three failure modes in §3, and the measured diff in §6.
```

Pass C is what separates this report from a plan. Passes A and B agree with lane m's count; pass C is where the disagreement with m's *conclusion* comes from.

Baseline control (unmodified copy, same interpreter, same session):

```
tests/test_audit.py + test_stale_worktrees.py + test_writer_integrity.py + test_skip_is_not_pass.py
  baseline    5 failed, 249 passed
  prototype   5 failed, 249 passed      <- same five names
```

The five are pre-existing and environment-caused, not extraction damage: `routine_consumers` is the known carried RED the batch-6 manifest names under its honest-RED clause; the `fleet_parity` / `health_*` / `audit_run_*` four fail because this is a cloud clone with no sibling fleet repos registered. They fail identically on both trees, which is the point of running the control.

---

## 2. The mechanism — why "patches a module global" does not mean "cannot move"

This is the correction that reshapes the work, and it is a Python-semantics fact rather than a judgement.

When a check moves to `audit_checks/<name>.py` and imports its seams by name, the *function objects* it imports still carry `__globals__` pointing at **the facade's** `__dict__`. So:

```
PATCHED SYMBOL IS A VARIABLE (_REPO_ROOT, ALL_CHECKS, DISPOSITION_REGISTER, ...)
  read by a helper that STAYS in the facade  ->  patch STILL LANDS. No test change. No re-point.
  read by the check body itself              ->  patch MISSES. Re-point needed.

PATCHED SYMBOL IS A FUNCTION (_git_linked_worktrees, _is_hub, _ref_baseline_state, ...)
  called by facade-resident code             ->  patch STILL LANDS.
  called by the extracted body               ->  patch MISSES (name bound at import time).

PATCHED VIA A DELEGATE OBJECT  (monkeypatch.setattr(aud._vdc, "reconcile", ...))
  ALWAYS LANDS -- it mutates the shared sys.modules object, which the extracted module
  reaches too. Move-invariant. 12 of the 38 symbols are this shape.
```

Demonstrated directly, not inferred — a four-module lab reproducing each shape:

```
                       baseline        after patching the facade globals
  naive   (by-name)    (False,[REAL])  (True, ['REAL'])   <- var patch LANDS, func patch MISSES
  latebound (attr)     (False,[REAL])  (True, ['FAKE'])   <- both land
  seams module         (False,[REAL])  (False,['REAL'])   <- neither lands; needs its own patch
```

**Consequence for `check_hooks_armed`:** its tests patch only `_REPO_ROOT`, which only `_is_hub` reads, and `_is_hub` is shared by 20 checks so it stays in the facade. Extracted naively, **all 5 tests pass untouched.** Verified:

```
$ python -m pytest tests/test_audit.py -k hooks_armed     # against the extracted tree
5 passed, 197 deselected
```

**Consequence for `check_stale_worktrees`:** its tests patch two *functions* the check body calls directly. Extracted naively, 11 of its 23 tests fail — and they fail *loudly* (`n/a` where `warn` was expected), because the unpatched `_git_linked_worktrees` returns `None` and the check short-circuits. One broken seam, eleven cascading failures.

So of the two `[#533]`-motivating checks, **one needs nothing and the other needs one seam re-pointed.**

---

## 3. Three failure modes a naive extraction hits — all found by running it

None of these are visible from reading the tests. Each cost a prototype iteration.

### H1 — `ALL_CHECKS` position constrains where the import can go (loud)

`ALL_CHECKS` is a list literal at `scripts/audit.py:4345` naming every check. An import placed at EOF, after the helpers, is **too late**:

```
NameError: name 'check_stale_worktrees' is not defined     (audit.py:4193, in the ALL_CHECKS literal)
```

The import must sit **above `ALL_CHECKS` and below every seam the check modules import**. That window exists and is wide (the last seam is at `:3095`), but it is a real ordering constraint on the facade, not a free choice. Fails loudly, so it costs a minute.

### H2 — the dual-import idiom creates TWO live `audit` module objects (SILENT — the dangerous one)

`audit.py` is reachable as `audit` (script mode + the pytest `pythonpath`) and as `scripts.audit` (`python -m scripts.audit`). Copying the repo's existing `try: from scripts import X / except ImportError: import X` idiom into the check modules looks correct and is not:

```
$ python -c "import audit as aud; import audit_checks.stale_worktrees as sw; print(aud is sw.audit)"
False
sys.modules: ['scripts.audit', 'audit']        <- audit.py EXECUTED TWICE, two sets of globals
```

The test patches one object; the check reads the other. **Eleven tests silently stop testing anything.**

And this is not hypothetical for the extraction only — **both objects are already live during a normal pytest run today**:

```
*** scripts.audit FIRST APPEARS after: tests/test_audit.py::test_audit_repo_good
```

`check_enforcement_coverage` reaches `scripts/enforcement_coverage.py`, whose `_freshness_files()` does `from scripts import audit as _audit` (`scripts/enforcement_coverage.py:566`) — re-executing `audit.py` under the other name. **This is a pre-existing latent condition in the live tree.** Today it is harmless, because every check and its seams share one namespace, so each facade copy is internally self-consistent. The extraction is what makes it load-bearing. Any seam accessor that picks a facade *by name* will pick the wrong one depending on test ordering, and will do it silently.

### H3 — there is a THIRD module name: `__main__` (loud, but only in the CLI)

`python scripts/audit.py health` runs the facade as `__main__`. A `sys.modules["audit"]` lookup raises there:

```
File "scripts/audit_checks/stale_worktrees.py", line 21, in _f
    return sys.modules[_FACADE]
KeyError: 'audit'
```

The suite is green at this point and the CLI is broken — the exact split the `audit-health` pre-commit gate would catch, but only after the fact.

### The design that survives all three

**Mirrored spelling + facade self-injection.** The facade imports its check modules under *its own* spelling, then hands each one **itself**:

```python
# scripts/audit.py -- placed above ALL_CHECKS, below every seam (H1)
if __name__.startswith("scripts."):
    from scripts.audit_checks import hooks_armed as _m_hooks_armed
    from scripts.audit_checks import stale_worktrees as _m_stale_worktrees
else:
    from audit_checks import hooks_armed as _m_hooks_armed
    from audit_checks import stale_worktrees as _m_stale_worktrees

for _m in (_m_hooks_armed, _m_stale_worktrees):
    _m.FACADE = sys.modules[__name__]          # itself -- whatever it is called (H2, H3)

check_hooks_armed = _m_hooks_armed.check_hooks_armed
check_stale_worktrees = _m_stale_worktrees.check_stale_worktrees
```

```python
# scripts/audit_checks/<check>.py
FACADE = None            # injected by audit.py at import


def _f():
    if FACADE is None:   # imported standalone, outside the facade
        import audit
        return audit
    return FACADE
```

Why each piece is load-bearing: the **mirrored `if`** (not a `try/except`) gives each facade copy its own copy of the check modules, so the two graphs never cross; **injection** (not a name lookup) always yields the object that is actually running, which is the object a caller's monkeypatch landed on; `sys.modules[__name__]` covers `__main__`, `audit` and `scripts.audit` without enumerating them.

This restores, explicitly, the property the monolith had for free by keeping check and seam in one namespace.

---

## 4. Per-symbol enumeration — every audit-module patch site in the suite

213 sites, 38 distinct symbols. `[var]`/`[func]` = patched as a module global of `audit` (a true seam, 26 symbols). `[delegate]` = `monkeypatch.setattr(aud.<mod>, "attr", ...)` on a shared `sys.modules` object (**move-invariant, 12 symbols — these need nothing**).

```
_REPO_ROOT                   [var  audit.py:70 ]  46  test_audit.py:1340,1702,1751,1780,2009,2019,2029,2039,2049,2062,2074,2087,2564,2614
                                                      test_fleet_audit_replication.py:85,92,106,115,141,155,172,188,204
                                                      test_task_tree_gate.py:177,227,244,266,292,311,330,344,355
                                                      test_ship_gate.py:122,202 · test_silent_rule_ratchet.py:495,512
                                                      test_undeclared_edges_leg.py:37,110 · test_doc_code_edge.py:151
                                                      test_legibility_graph_conformance.py:141 · test_review_artifact_coverage.py:95
                                                      test_validate_doc_claims.py:383 · test_validate_doc_rot.py:323
                                                      test_validate_doc_structure.py:306 · test_validate_git_backlog.py:244
                                                      test_validate_no_ff.py:216
_is_hub                      [func audit.py:82  ]  22  test_batch_manifest.py:139,153,172,193,211,276,696,721,742
                                                      test_membership_agreement.py:262,271,286,297,306,315,324,357,377,388
                                                      test_adr85_integration_enforcement.py:380,433,445
ECOSYSTEM_DIR                [var  audit.py:222 ]  15  test_audit.py:117,133,548,561,1341,1697,1745,1775
                                                      test_writer_integrity.py:225,247,264,307,327,403 · test_membership_agreement.py:171
_git_linked_worktrees        [func audit.py:1065]  12  test_stale_worktrees.py:71,82,95,111,124,150,162,262,278,289,309,345
_git_stash_entries           [func audit.py:1142]  12  test_stale_worktrees.py:72,87,99,114,127,151,263,279,290,310,324,347
_git_registered_worktrees    [func audit.py:899 ]   9  test_audit.py:1049,1065,1083,1099,1116,1128,1147,1161,1176
ALL_CHECKS                   [var  audit.py:4345]   8  test_audit.py:629,645,1698,1746,1776 · test_doc_code_edge.py:701
                                                      test_ship_gate.py:72 · test_writer_integrity.py:97
_git_last_commit_date        [var  audit.py:851 ]   7  test_audit.py:883,896,911,921,932,943,957
AUDITS_DIR                   [var  audit.py:223 ]   4  test_audit.py:502,510,518,1342
DISPOSITION_REGISTER         [var  audit.py:227 ]   4  test_audit.py:1747,1792 · test_ship_gate.py:74,78
_GATE_MODE                   [var  audit.py:217 ]   4  test_audit.py:628,644 · test_validate_doc_claims.py:372,384
_ref_baseline_state          [func audit.py:3095]   4  test_silent_rule_ratchet.py:456,465,566,583
_git                         [func audit.py:3039]   3  test_silent_rule_ratchet.py:485,513 · test_task_tree_gate.py:295
DEPLOYED_VERSIONS_REGISTRY   [var  audit.py:232 ]   2  test_audit.py:1865,1904
_git_repo_root_name          [func audit.py:928 ]   2  test_audit.py:1939,1949
_index_worktree_divergence   [func audit.py:2991]   2  test_gen_intake_tree.py:268,310
_commit_routine_outputs      [func audit.py:4731]   2  test_writer_integrity.py:370,440
append_history               [func audit.py:512 ]   2  test_writer_integrity.py:367,437
audit_repo                   [func audit.py:4502]   2  test_writer_integrity.py:365,435
discover_repos               [func audit.py:564 ]   2  test_writer_integrity.py:362,432
generate_report              [func audit.py:4535]   2  test_writer_integrity.py:368,438
load_state                   [func audit.py:456 ]   2  test_writer_integrity.py:363,433
resolve_repo_path            [func audit.py:548 ]   2  test_writer_integrity.py:364,434
save_state                   [func audit.py:465 ]   2  test_writer_integrity.py:366,436
write_report                 [func audit.py:4590]   2  test_writer_integrity.py:369,439
_today                       [func            ]     1  test_writer_integrity.py:371

--- MOVE-INVARIANT (delegate-object patches; no re-point, no test change) ---------------
subprocess  [delegate]  7  test_audit.py:1456,1486,1509,1913,1922,1929 · test_verify_handoff_probes.py:988
_vdc        [delegate]  5  test_validate_doc_claims.py:259,269,278,289,371
_vgb        [delegate]  5  test_validate_git_backlog.py:188,199,209,227 · test_ship_gate.py:198
_vnf        [delegate]  4  test_validate_no_ff.py:164,175,185,203
_vdr        [delegate]  3  test_validate_doc_rot.py:281,293,301
_vds        [delegate]  3  test_validate_doc_structure.py:267,279,287
_vrc        [delegate]  3  test_residual_completeness.py:237,247,258
_gtt        [delegate]  2  test_task_tree_gate.py:233,250
_sr         [delegate]  2  test_safe_remove.py:128,193
_srd        [delegate]  2  test_silent_rule_ratchet.py:245,514
_sue        [delegate]  1  test_undeclared_edges_leg.py:123
_vhp        [delegate]  1  test_verify_handoff_probes.py:667
```

Note `subprocess` appears in both shapes in the suite; its 7 sites are all `setattr(aud, "subprocess", fake)` on the facade's binding, which the accessor design handles like any other facade attribute.

---

## 5. Per-check classification

**Class 1 — 25 of 43.** The check's moved code reads a symbol some test patches as an audit module global. This reproduces lane m's count exactly, from an independent derivation:

```
canonical_freshness            doc_code_edge          journal_day_letters      preflight_backlog_ids
deployed_methodology_version   doc_rot                journal_spine_anchor     review_artifact_coverage
doc_claims                     doc_structure          landing_predicate        silent_rule_ratchet
doc_code_coverage_drift        enforcement_coverage   membership_agreement     stale_worktrees
fleet_audit_replication        fleet_parity           no_ff_merges             task_tree_coherence
git_backlog_drift              hooks_armed            no_sibling_orphans       undeclared_edges
intake_tree_coherence
```

**Class 2 — 3 of 43** (`handoff_probes`, `residual_completeness`, `safe_removal`): exposure is **only** through delegate-object patches. Move-invariant; extract with no seam work at all.

**Class 3 — 15 of 43**: no patched symbol anywhere. `vision_md`, `adr38_baseline`, `claude_md`, `dot_prefix_discipline`, `canonical_md_visibility`, `workspace_settings`, `handoff_bundle_structure`, `canonical_structure`, `handoff_version_stamp`, `amendment_coherence`, `floor_integrity`, `reconciled_versions`, `import_edges`, `routine_consumers`, `boot_byte_budget`. **These 18 (Class 2 + 3) are the free ones and should go first** — they are pure moves that exercise the facade wiring before any seam work.

### The tighter cut that says where the work actually is

Class 1 is the *could-break* set. The set whose **own** tests patch a global its moved code reads — the ones that would actually go red — is **11**, and the sites are concentrated:

```
stale_worktrees              24 sites  _git_linked_worktrees(12) _git_stash_entries(12)
journal_spine_anchor         12 sites  _is_hub(12)
membership_agreement         10 sites  _is_hub(10)
no_sibling_orphans            9 sites  _git_registered_worktrees(9)
canonical_freshness           7 sites  _git_last_commit_date(7)
silent_rule_ratchet           6 sites  _ref_baseline_state(4) _git(2)
deployed_methodology_version  4 sites  DEPLOYED_VERSIONS_REGISTRY(2) _git_repo_root_name(2)
doc_claims                    2 sites  _GATE_MODE(2)
intake_tree_coherence         2 sites  _index_worktree_divergence(2)
landing_predicate             2 sites  DISPOSITION_REGISTER(2)
doc_code_coverage_drift       1 site   ALL_CHECKS(1)
```

`check_hooks_armed` is **not** in this list. That is the §2 result, and it is why the two `[#533]`-motivating checks are the cheapest pair on the board rather than the hardest.

**Under the §3 accessor design all 11 need ZERO test edits too** — the re-point happens inside the newly-created module, which is new code, so it is not a diff against anything. The 11 matter only as the list of checks where the mechanical `X` → `_f().X` rewrite is *required* rather than optional.

---

## 6. The smallest diff freeing `hooks_armed` + `stale_worktrees` — MEASURED, not estimated

Built and run this session. Two variants, because they answer two different questions.

### 6a. Source-only (clears the `scripts/audit.py` collision)

```
scripts/audit.py                          -132 / +15 lines
scripts/audit_checks/__init__.py           NEW    0 lines
scripts/audit_checks/hooks_armed.py        NEW   84 lines   (53 moved verbatim + accessor + imports)
scripts/audit_checks/stale_worktrees.py    NEW  119 lines   (87 moved verbatim + accessor + imports)
tests/**                                   UNCHANGED -- zero test files edited
```

Result:

```
python -m pytest tests/test_audit.py tests/test_stale_worktrees.py
    5 failed, 220 passed          <- identical to baseline, same five names
python scripts/audit.py checks    -> BYTE-IDENTICAL to baseline
python scripts/audit.py health    -> BYTE-IDENTICAL to baseline (modulo the scratch checkout's
                                     own directory name, which appears in 2 findings by design)
python -m scripts.audit health    -> runs clean (package mode)
len(ALL_CHECKS) == 43, order preserved (stale_worktrees idx 9, hooks_armed idx 14)
```

Only **one existing file** is touched. `[#533]`'s Done-when byte-comparison proof is met on the first two checks.

### 6b. Source + the test split (what l/y actually needs — see §7)

```
scripts/audit.py                          -132 / +15
scripts/audit_checks/{__init__,hooks_armed,stale_worktrees}.py   NEW (203 lines total)
tests/test_audit.py                       -~85 lines (block removed, nothing rewritten)
tests/test_hooks_armed.py                 NEW -- the removed block, VERBATIM
```

Result: `5 failed, 220 passed` — baseline again. **Zero assertions changed anywhere**; the test move is a relocation.

**k = 6 files** (2 edited: `scripts/audit.py`, `tests/test_audit.py`; 4 new). Source-only it is **k = 4** (1 edited, 3 new).

**One judgement call inside the test split, flagged because it is the only non-mechanical step:** `_arm_repo` / `_PRECOMMIT_HOOK_TMPL` are shared by the 5 `hooks_armed` tests *and* the 2 `test_arm_hooks_*` tests. Moving only the former leaves a cross-test-module import. The prototype moves **both groups** — splitting on the subject (hook arming) rather than on the check name — which keeps the fixture with all its users and needs no shared `conftest.py` (the repo has none). The alternative, introducing `tests/conftest.py`, is a larger and more opinionated change and is **not** proposed here.

### Generalization evidence

To check the design was not overfitted to two checks, a **third** — `check_no_sibling_orphans`, which has a different seam shape (9 sites on `_git_registered_worktrees`) and drags **two private helpers** out with it — was extracted the same way. Result: `5 failed, 249 passed`, baseline again, zero test edits. Its one wrinkle was mundane and loud: the moved body needed `import os`, which the mechanical move must carry.

### Full-suite control

Both trees, whole suite, same interpreter and flags (prototype = all three extracted checks):

```
baseline    114 failed, 2734 passed, 37 skipped, 1 xfailed, 13 errors   (508.64s)
prototype   114 failed, 2734 passed, 37 skipped, 1 xfailed, 13 errors   (511.60s)
```

Identical counts across 2886 tests — and the **names** were captured and diffed separately, because matching totals could in principle mask a swap (one test fixed, one broken):

```
$ diff fail_base.txt fail_proto.txt     # 127 FAILED/ERROR node ids each, sorted
(no output)   -> the same 127 tests fail on both trees; no test changed side
```

The 114 are environment-caused on this cloud clone (absent optional deps, no sibling fleet repos, no language server) and are **not** a claim that the live hub suite is 114-red.

---

## 7. Does this unblock batch-7 lanes l and y? — **Yes, with one condition**

The batch-6 collision, as the D-1v2 amendment records it:

```
COLLISION  l <-> y : scripts/audit.py , tests/test_audit.py
   lane y  check_hooks_armed      -> scripts/audit.py:1625  (logic INLINE, no module)
   lane l  check_stale_worktrees  -> scripts/audit.py:1221  (logic INLINE, no module)
   lane l  tests/test_audit.py    -> named EXPLICITLY in its OWNED-FILES
```

After 6a, the source half is gone: lane y owns `scripts/audit_checks/hooks_armed.py`, lane l owns `scripts/audit_checks/stale_worktrees.py`. Disjoint.

**The test half is not gone, and 6a alone does not clear it.** `check_hooks_armed`'s five tests live at `tests/test_audit.py:1976–2052` — inside the file lane l names explicitly, and lane l genuinely needs it for its `[#426]` `routine_consumers` legs. Lane l's `check_stale_worktrees` tests are already in their own file (`tests/test_stale_worktrees.py`), so the residual collision is **precisely and only** the `hooks_armed` block sitting in `tests/test_audit.py`.

**6b clears it.** With `tests/test_hooks_armed.py` split out:

```
lane y owns  scripts/audit_checks/hooks_armed.py  +  tests/test_hooks_armed.py
lane l owns  scripts/audit_checks/stale_worktrees.py  +  tests/test_stale_worktrees.py
             +  tests/test_audit.py  (routine_consumers legs, uncontested)
             ->  DISJOINT
```

So: **yes, l/y are unblocked — provided lane m's extraction includes the 6b test split.** If lane m ships 6a only, the batch-7 matrix will re-refuse the same pair on `tests/test_audit.py` alone, which would be the same lesson at a second cost. That is the single most consequential recommendation in this report.

---

## 8. Proposed sequencing for the full 25 (proposal only — no lane is dispatched by this file)

```
Wave 0  the 18 free checks (Class 2 + Class 3). Pure moves. Proves the facade wiring, the H1
        import window and the ALL_CHECKS byte-comparison before any seam is touched.
Wave 1  hooks_armed + stale_worktrees. The [#533] motivating pair; unblocks batch-7 l/y.
        MUST include the tests/test_hooks_armed.py split (§7).
Wave 2  the 9 remaining low-site checks: doc_code_coverage_drift(1), doc_claims(2),
        intake_tree_coherence(2), landing_predicate(2), deployed_methodology_version(4),
        silent_rule_ratchet(6), canonical_freshness(7), no_sibling_orphans(9),
        membership_agreement(10).
Wave 3  journal_spine_anchor. LAST of the checks -- its 12 sites live in
        test_adr85_integration_enforcement.py and test_batch_manifest.py, i.e. the files that
        gate the batch protocol running the extraction. Moving it mid-batch changes the
        machinery measuring the batch. Same edge-not-middle reasoning that put lane m last.
Wave 4  the 14 facade-level symbols nothing needs to move: ECOSYSTEM_DIR, AUDITS_DIR,
        ALL_CHECKS, _GATE_MODE, DISPOSITION_REGISTER and the 9 test_writer_integrity.py
        orchestration seams (discover_repos, load_state, audit_repo, ...). These belong to
        cmd_run / cmd_health / ship-gate, which STAY in the facade. Nothing to do -- listed so
        a later reader does not go looking for work that is not there.
```

Wave 0 first is the substantive recommendation: it front-loads the wiring risk (H1–H3 all surface on the very first extracted check) onto checks where nothing can silently miss, because none of their tests patch anything.

---

## 9. Honest limits

- **The prototype extracted 3 checks, not 43.** Waves 2–4 are proposed on a mechanism validated three times across three seam shapes, not executed. A check with a seam shape none of the three exhibits could still surprise; `check_doc_claims` (which reads `ALL_CHECKS` *and* `_GATE_MODE` *and* delegates to `_vdc`) is the most likely candidate and was not prototyped.
- **This ran on a cloud clone, where 114 of 2886 tests fail at baseline for environment reasons.** Every claim here is a *delta* against that baseline, measured on the same machine in the same session. It is not a claim about the live hub's suite, and lane m should re-establish its own baseline before trusting these numbers.
- **`audit.py health` byte-identity was verified modulo the checkout's directory name**, which legitimately appears in two findings (`no_sibling_orphans` prints the sibling prefix; `deployed_methodology_version` names the repo). On a same-named checkout the comparison is exact; here it required normalizing two lines, and I am stating that rather than claiming a cleaner result than I measured.
- **H2 is a pre-existing defect this report does not fix.** `audit.py` is executed twice per pytest session today via `scripts/enforcement_coverage.py:566`. The proposed design is immune to it, but the double execution remains — wasted work, doubled import side effects, and a trap for the next thing that reaches across the two spellings. It deserves its own row; **this report does not file one** (filing is not in this lane's scope) and does not propose fixing it inside `[#533]`, which is explicitly a mechanical extraction.
- **Lane m's packet was not read** — it is not present in this branch, and no lane-m branch exists on the remote. The 25/43 agreement is therefore genuine independent corroboration, but the per-symbol list here is *my* enumeration; if m's packet names a symbol absent from §4, §4 is the one to re-check.
- **`_today` could not be resolved to a module-level definition** by the AST pass (patched once at `test_writer_integrity.py:371`). It is a facade-level orchestration seam either way (Wave 4), so nothing here depends on it, but the classification for that one symbol is unverified.
- **No claim is made about mutation coverage or about whether the moved tests still test what they did.** The evidence is "same tests, same results, same CLI bytes" — necessary, not sufficient, for a refactor of this size. The `[#533]` Done-when asks for a byte-comparison, and that is what was produced.

---

## 10. What this report deliberately does NOT do

- It edits no source, no test and no BACKLOG row. It births nothing, closes nothing, and dispatches no lane.
- It does not reopen or amend the batch-6 manifest, or its D-1v2 amendment.
- It does not rewrite lane m's contract or claim authority over lane m's OWNED-FILES; the §7 recommendation (include the test split) is a proposal to whoever rules on lane m's scope, not a change to it.
- It leaves the prototype in the session scratchpad, uncommitted and outside the repo tree, per the no-leftovers rule (CLAUDE.md §5 rule 9).
