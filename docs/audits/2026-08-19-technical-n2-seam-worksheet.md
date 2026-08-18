# NIGHT N2 — [#533] seam-leg worksheet: the 25 monkeypatch pins

- **Date:** 2026-08-19 (dispatch date; lane ran 2026-08-18, cloud night channel)
- **Lane:** read-only research — branch `claude/seam-leg-monkeypatch-pins-91fh27`
- **Contract of record:** `docs/audits/2026-08-19-technical-n2-seam-worksheet-contract.md` (first commit)
- **Tree read:** this branch's checkout, `f4a01f0e` (leg 2) verified an ancestor of HEAD
- **Executes nothing.** No re-point, no extraction, no merge, no code/test/BACKLOG edit.

## Verdicts

| Item | Verdict | One-line |
|---|---|---|
| 1 · Pin census | **CLEAR** | 25/27 reproduced independently; per-check table in §1 |
| 2 · Re-point recipes | **CLEAR** | 4 pin classes; 1 needs no work; 4 weakening traps named |
| 3 · Other two classes | **CLEAR** | Both unblock shapes drafted; two rulings named |
| 4 · Extraction order | **CLEAR** | 4-wave dependency-ordered queue in §4 |
| 5 · Seam-lane contract | **CLEAR, with a scope correction** | Dispatch scope covers 21% of the bloc — §5 |

**Three measured disagreements with the dispatch/registry text are recorded in §6.** None
changes the shape of the work; all three change its *size*, so they are stated before the
contract rather than discovered inside it.

---

## §0 · Method, and the gate state

**Static analysis only.** Every claim below is from AST + grep over the checked-out tree. Two
independent methods were used for the load-bearing counts (a Python `ast` closure walk and a
flat `grep`/`awk` pass) and they agree; where they would not, the disagreement is reported
rather than reconciled silently.

**GATES UNAVAILABLE — recorded honestly, as the dispatch requires.** Nothing in this worksheet
is backed by a green test run, because no test run is possible in this container:

```
uv 0.8.17            vs pyproject [tool.uv] required-version = "==0.11.19"
                     -> `uv run` / `uv sync` REFUSE outright (hard version gate)
python 3.11.15       vs requires-python = ">=3.12" and .python-version = 3.12.10
pytest               not importable (no .venv; system interpreter has no pytest)
pre_commit           not importable -> no hook fires on this branch's commits
markdown_it          absent -> `scripts/audit.py` will not even import here
ruff 0.15.8          present, but off the pinned 0.15.5 (pre-commit rev + pyproject floor)
```

Consequences, stated rather than papered over:

1. **No parity proof was produced tonight.** §5's contract names the proof the seam lane must
   produce; this lane could not run it.
2. `audit.py` was never executed — every statement about it is a reading of its source.
3. The commits on this branch bypassed the hook mesh **by absence, not by `--no-verify`**. The
   two generated-index gates that this branch's own edits could have reddened were run by hand
   instead: `gen_audit_index.py --check` passes, and the index was regenerated when the stamp
   was staged. `audit-health` could not be run (no `markdown_it`).

---

## §1 · Pin census — CLEAR

### 1.1 The criterion, restated from the tree

`scripts/audit_checks/registry.py` states the rule: a check moves only if nothing in its
**transitive dependency closure** is monkeypatched onto the `audit` module by a test. The
failure it prevents is not a test error — it is a test that keeps *passing* while exercising
nothing, because the check reads its own module's binding while the test rewrites `audit`'s.

Reproduced independently: `scripts/audit.py` defines **27** `check_*` functions; a closure walk
over each intersected with the patched-name set yields **25 pinned**, and the 2 unpinned are
exactly `check_handoff_probes` and `check_import_edges` — the other two blocked classes. Totals
agree with `registry.py`: `CHECK_ORDER` = 43, `EXTRACTED_CHECKS` = 16, 43 − 16 = 27 facade.

### 1.2 The census

Future home follows the established convention exactly — one module per check, named for it,
under `scripts/audit_checks/`. `#t` = distinct test functions that both patch and exercise the
check directly; `0` means the pin arrives through a shared fixture or through `ALL_CHECKS`, not
that the check is unpinned.

| # | Check (facade) | #t | Test files carrying the pins | Monkeypatched name(s) in closure | Future home `scripts/audit_checks/…` |
|---|---|---|---|---|---|
| 1 | `check_canonical_freshness` | 7 | `test_audit.py` | `_git_last_commit_date` | `check_canonical_freshness.py` |
| 2 | `check_no_sibling_orphans` | 9 | `test_audit.py` | `_git_registered_worktrees` | `check_no_sibling_orphans.py` |
| 3 | `check_stale_worktrees` | 13 | `test_stale_worktrees.py` | `_git_linked_worktrees`, `_git_stash_entries`, `_git` | `check_stale_worktrees.py` |
| 4 | `check_hooks_armed` | 5 | `test_audit.py` | `_is_hub`, `_REPO_ROOT` | `check_hooks_armed.py` |
| 5 | `check_git_backlog_drift` | 6 | `test_validate_git_backlog.py`, `test_ship_gate.py` | `_is_hub`, `_REPO_ROOT` | `check_git_backlog_drift.py` |
| 6 | `check_doc_claims` | 6 | `test_validate_doc_claims.py` | `ALL_CHECKS`, `_GATE_MODE`, `_is_hub`, `_REPO_ROOT` | `check_doc_claims.py` |
| 7 | `check_no_ff_merges` | 5 | `test_validate_no_ff.py` | `_is_hub`, `_REPO_ROOT` | `check_no_ff_merges.py` |
| 8 | `check_doc_rot` | 4 | `test_validate_doc_rot.py` | `_is_hub`, `_REPO_ROOT` | `check_doc_rot.py` |
| 9 | `check_doc_structure` | 4 | `test_validate_doc_structure.py` | `_is_hub`, `_REPO_ROOT` | `check_doc_structure.py` |
| 10 | `check_doc_code_edge` | 1 | `test_legibility_graph_conformance.py` | `_is_hub`, `_REPO_ROOT` | `check_doc_code_edge.py` |
| 11 | `check_deployed_methodology_version` | 3 | `test_audit.py` | `DEPLOYED_VERSIONS_REGISTRY`, `_git_repo_root_name` | `check_deployed_methodology_version.py` |
| 12 | `check_enforcement_coverage` | 0 | — (via `ALL_CHECKS` / health) | `_is_hub`, `_REPO_ROOT` | `check_enforcement_coverage.py` |
| 13 | `check_undeclared_edges` | 2 | `test_undeclared_edges_leg.py` | `_is_hub`, `_REPO_ROOT` | `check_undeclared_edges.py` |
| 14 | `check_doc_code_coverage_drift` | 1 | `test_doc_code_edge.py` | `ALL_CHECKS`, `_is_hub`, `_REPO_ROOT` | `check_doc_code_coverage_drift.py` |
| 15 | `check_fleet_parity` | 0 | — (via `ALL_CHECKS` / health) | `_is_hub`, `_REPO_ROOT` | `check_fleet_parity.py` |
| 16 | `check_silent_rule_ratchet` | 3 | `test_silent_rule_ratchet.py` | `_ref_baseline_state`, `_index_worktree_divergence`, `_git`, `_is_hub`, `_REPO_ROOT` | `check_silent_rule_ratchet.py` |
| 17 | `check_task_tree_coherence` | 6 | `test_task_tree_gate.py` | `_index_worktree_divergence`, `_git`, `_is_hub`, `_REPO_ROOT` | `check_task_tree_coherence.py` |
| 18 | `check_intake_tree_coherence` | 2 | `test_gen_intake_tree.py` | `_index_worktree_divergence`, `_git`, `_is_hub`, `_REPO_ROOT` | `check_intake_tree_coherence.py` |
| 19 | `check_fleet_audit_replication` | 6 | `test_fleet_audit_replication.py` | `_is_hub`, `_REPO_ROOT` **+ `_gitenv`** | `check_fleet_audit_replication.py` |
| 20 | `check_membership_agreement` | 1 | `test_membership_agreement.py` | `_is_hub`, `_REPO_ROOT` (+ `ECOSYSTEM_DIR` patched as a **poison the check must not read** — §2.5 W1; not a closure seam) | `check_membership_agreement.py` |
| 21 | `check_journal_spine_anchor` | 12 | `test_batch_manifest.py`, `test_adr85_integration_enforcement.py` | `_is_hub`, `_REPO_ROOT` | `check_journal_spine_anchor.py` |
| 22 | `check_journal_day_letters` | 3 | `test_audit.py` | `_is_hub`, `_REPO_ROOT` | `check_journal_day_letters.py` |
| 23 | `check_preflight_backlog_ids` | 1 | `test_audit.py` | `_is_hub`, `_REPO_ROOT` | `check_preflight_backlog_ids.py` |
| 24 | `check_review_artifact_coverage` | 0 | — (fixture `_repo`) | `_is_hub`, `_REPO_ROOT` | `check_review_artifact_coverage.py` |
| 25 | `check_landing_predicate` | 2 | `test_audit.py` | `DISPOSITION_REGISTER`, `_is_hub`, `_REPO_ROOT` | `check_landing_predicate.py` |

Row order is `CHECK_ORDER` order, because that order is load-bearing (it is the emission order
and therefore part of the byte-identical output contract the hooks read).

### 1.3 What each pinned name fakes

| Seam name | Kind | Fakes |
|---|---|---|
| `_REPO_ROOT` | `str` global, derived from `__file__` at import | *Which checkout is the hub.* Redirects hub identity at a synthetic `tmp_path` tree, so hub-only checks run hermetically — and, pointed at a non-hub path, proves the hub-only skip actually fires |
| `_is_hub` | function | The hub-identity **predicate** itself — forces the hub-only branch on/off without building a matching tree |
| `ECOSYSTEM_DIR` | `Path` global | The fleet-state root, so state I/O and repo discovery read a tmp fleet |
| `AUDITS_DIR` | `Path` global | The report destination, so `write_report` writes into tmp |
| `ALL_CHECKS` | `list` global | The **live registry** — shrunk to a sentinel (hermetic/fast) or grown by an escapee (drift-guard teeth) |
| `_GATE_MODE` | `bool` global | "running as the pre-commit gate", which switches expensive legs off |
| `DISPOSITION_REGISTER` | `Path`, computed from `_REPO_ROOT` **at import** | The dated-exemption register consulted by the landing-predicate gate |
| `DEPLOYED_VERSIONS_REGISTRY` | `Path` global | The deployed-methodology-version registry file |
| `_git_last_commit_date` | alias → `_cfg.git_last_commit_date` | Per-file git commit dates, making the freshness cadence deterministic |
| `_git_registered_worktrees` | function | The `git worktree list` registration set |
| `_git_linked_worktrees` | function | Linked-worktree records **with ages**, so the staleness horizon is testable without waiting |
| `_git_stash_entries` | function | `git stash list` — including the unreadable-vs-absent distinction |
| `_git_repo_root_name` | function | The repo-root basename as seen from inside a worktree |
| `_git` | function | Raw git invocation — used to fake **probe failure**, not probe content |
| `_index_worktree_divergence` | function | Staged-vs-worktree disagreement (the "refuse to answer" input) |
| `_ref_baseline_state` | function | A git-ref baseline read for the ratchet |
| `_today` | function | The current date (writer layer only; no check reads it) |

---

## §2 · Re-point recipes per pin class — CLEAR

### 2.0 The taxonomy is by *mechanism*, and one class is already safe

Measured over the whole `tests/` tree, resolving the module alias per file:

| Class | Mechanism | Sites | Survives a pure move? |
|---|---|---|---|
| **A** | rebind a module-global **value** on `audit` — `setattr(aud, "ECOSYSTEM_DIR", …)` | 89 | **No** |
| **B** | rebind a **function defined in `audit`** — `setattr(aud, "_is_hub", …)` | 85 | **No** |
| **C** | rebind an **alias to another module's symbol** — `setattr(aud, "_git_last_commit_date", …)`, where `audit` holds `_git_last_commit_date = _cfg.git_last_commit_date` | 7 | **No** |
| **D** | set an attribute **on a shared module object reached through `audit`** — `setattr(aud._vgb, "reconcile", …)`, `setattr(aud.subprocess, "run", …)` | 38 | **Yes** — see 2.1 |

A + B + C = **181 name-rebind sites across 21 test files.** Classes A/B/C are one problem
wearing three coats: all three rebind a name *on the `audit` module object*, and the reader
resolves that name through *its own* module namespace.

Class D is different in kind and this distinction is the single most useful result in this
worksheet: it mutates an attribute **on a third module's object**, and the reader looks that
attribute up at call time on the same shared object. Relocating the reader changes nothing.

### 2.1 Recipe D — Class D needs no re-point, but does need one guard

**Cost: 0 test edits.** Two preconditions, both mechanical:

1. The extracted module must reach the **same module object** `audit` reached. `audit.py`
   resolves each validator through a dual `try: from scripts import X as _x / except
   ImportError: import X as _x`. The two spellings produce **distinct module objects** when
   both `scripts/` and the repo root are importable — which `pytest` from the repo root really
   does. If the check module lands on the other spelling, `aud._vgb` and the check's `_vgb` are
   different objects and the patch silently misses. **Fix: one owner.** `_common.py` (already
   imported by both sides) performs the dual import once; facade and check modules both take
   the alias from there, so identity holds by construction.
2. The check must keep the **module-attribute call form** — `_vgb.reconcile(…)`. A
   `from validate_git_backlog import reconcile` detaches the seam; this is the one way to break
   a Class-D pin, and it is an easy accident during a move.

**Guard owed:** a test asserting `aud._vgb is <check_module>._vgb` for each alias. Without it,
precondition 1 fails silently — the exact failure mode the whole leg exists to prevent.

### 2.2 Recipe R2 — "facade stays the seam owner" (Classes A + B + C)

The extracted module takes a **lazy, in-function** `import audit as _facade` and reads
`_facade._is_hub(…)`, `_facade._REPO_ROOT` **at call time**. Attribute lookup happens on the
`audit` module object, which is exactly what `monkeypatch.setattr(aud, …)` mutates.

- **Test edits: zero.** Intent is byte-equivalent *by construction* — not by review.
- **Import cycle:** legal, because the import is inside the function body, after both modules
  are loaded.
- **Honest verdict, and it is the reason this is not the recommendation:** R2 relocates text
  without decoupling anything. Every extracted module would import the facade it was extracted
  from, and the dependency graph gets *worse* than before while the line count improves. It
  buys the `audit.py` size reduction and nothing else.
- **Use it for:** nothing, unless the operator's goal is purely the file-size metric. Recorded
  because it is the zero-risk option and the lane should know it exists.

### 2.3 Recipe R3 — "move the seam to a shared owner" (Classes A + B + C) — **recommended**

A single `scripts/audit_checks/_seam.py` owns the patched names. Facade and check modules both
read them **as attributes of that module** at call time — i.e. deliberately converting Classes
A/B/C into the Class-D shape that is already proven to survive relocation. Tests re-point from
`setattr(aud, "_is_hub", …)` to `setattr(_seam, "is_hub", …)`.

**The safety property that makes this executable mechanically:** `monkeypatch.setattr(obj,
"name", value)` **raises `AttributeError` when `name` does not exist**. So if the seam lane
*removes* the old `audit._is_hub` re-export rather than keeping it for back-compat, every
re-point site it missed becomes a **loud error**, not a silent pass. A back-compat re-export
would do the opposite — leave `aud._is_hub` patchable but no longer read — which is precisely
the silent detachment being engineered away. **Therefore: no back-compat re-exports for
re-pointed names. That is not a style preference; it is the whole safety argument.**

- **Test edits:** ~156 sites (89 A + 67 B, excluding the writer-layer names), across 21 files.
- **Intent preservation:** the fake is unchanged — same value, same lambda, same behaviour
  faked. Only the *owner named in the patch target* changes. A reviewer checks this by
  diffing: **the diff must touch patch targets and imports only, never an `assert`.**

### 2.4 Recipe R4 — the import-time-derived path constants

`DISPOSITION_REGISTER = Path(_REPO_ROOT) / "ecosystem" / "disposition-register.yaml"` is
computed **at import**. Patching `_REPO_ROOT` therefore does **not** move it — which is why the
two landing-predicate tests patch both. This is a live trap that predates the decomposition.

**Recommendation: carry it across unchanged, as a value on `_seam`.** Converting these to lazy
accessors would be an improvement, but it changes what the tests patch (a value becomes a
callable) and so is no longer a pure re-point. **Do it in a separate act or not at all** —
mixing a semantic improvement into a mechanical re-point is how a parity proof stops proving
anything.

### 2.5 Pins whose re-point would WEAKEN what they guard — four, named

This is the part of the dispatch that mattered most, and the four are not interchangeable.

**W1 · `test_membership_agreement.py::test_state_dirs_are_read_from_repo_path_not_the_module_global`.**
The test patches `aud.ECOSYSTEM_DIR` to a **poisoned** value and asserts the check *ignores*
it — a regression guard for a first draft that reused `discover_repos()` and so reported a
different repo than the other five surfaces. **`ECOSYSTEM_DIR` is deliberately NOT in this
check's dependency closure — that absence is exactly what the test asserts**, which is why the
check reads as bloc-only in §1.2 and lands in Wave 2 rather than Wave 3. The pin is a *poison*,
not a dependency. Under a **dependency-injection** recipe (pass `ecosystem_dir` into the check)
the test goes **vacuous**: with no module global left to ignore, it can no longer prove the
check ignores one. → **DI is forbidden for `ECOSYSTEM_DIR`.** R3 preserves the teeth, because a
reachable-but-ignored global still exists — and note the guard only keeps working while
`audit.ECOSYSTEM_DIR` still *exists*, since `monkeypatch.setattr` raises on a missing
attribute. `ECOSYSTEM_DIR` is therefore a name the seam lane must **keep on `audit`**, not
re-point: it is the one case where the §2.3 "no re-exports" rule must not be applied blindly.

**W2 · `test_doc_code_edge.py::test_coverage_drift_guard_full_check_fails_on_injected_escape`.**
Patches `aud.ALL_CHECKS` with an extra member and asserts the drift-guard **names** it. The
check's subject *is* the registry. Under DI the test would exercise the list it was handed and
stop proving the guard reads **the registry that actually runs**. → **`ALL_CHECKS` must stay a
live global read.**

**W3 · a structural veto on every wrapper-shaped recipe.** `audit._markers_for_check` reads a
check's `# rule:` marker via `inspect.getsourcelines(fn)` plus a walk-back through
`sys.modules[fn.__module__]`'s source. Any recipe that registers a **`functools.partial`, a
closure, or an adapter** in `ALL_CHECKS` breaks `fn.__name__` (→ `_coverage_drift_findings`
raises), and/or the source walk-back (→ marker lost → the drift-guard FAILs naming a phantom
escapee). → **Checks must remain plain module-level functions in `ALL_CHECKS`.** This rules out
the whole "inject dependencies at registration" family, not merely one variant of it.

**W4 · the tempting collapse: do not fold `_REPO_ROOT` pins into `_is_hub` pins.** `_is_hub`
reads `_REPO_ROOT`, so re-pointing 46 `_REPO_ROOT` sites to 46 `_is_hub` lambdas looks like a
free simplification. It is not. Tests such as `test_hooks_armed_off_hub_is_pass`,
`test_preflight_backlog_ids_is_na_off_hub`, `test_undeclared_edges_hub_only_skip` and
`test_alarm_is_hub_only` patch `_REPO_ROOT` **to a non-hub path** specifically to prove that
`_is_hub`'s own comparison fires. Stubbing `_is_hub` would *assume* the very thing they test.
→ **`_REPO_ROOT` and `_is_hub` are two seams and stay two seams.**

---

## §3 · The other two classes — CLEAR

### 3.1 `_gitenv` position-dependent load — and it blocks **two** checks, not one

**Shape of the block.** `audit.py` loads the git-env scrub by path:
`spec_from_file_location("dev_knowledge_gitenv", Path(__file__).resolve().with_name("gitenv.py"))`.
`.with_name()` is anchored to the *loading file's own directory*, so evaluated from
`scripts/audit_checks/` it resolves to `scripts/audit_checks/gitenv.py`, which does not exist.
The by-path load is not incidental: three name-based spellings were each reproduced live to
have a shadow hole that ends with the scrub silently becoming the **empty set** and re-opening
[#355] (terra HIGH ×3, 2026-08-08, recorded in `gitenv.py`'s docstring). **Correction to the
dispatch's framing:** the closure walk shows `check_fleet_audit_replication` reaches
`_git_location_env` as well, so this class holds `check_handoff_probes` **and**
`check_fleet_audit_replication` — and the latter also carries the `_is_hub`/`_REPO_ROOT` bloc
pin, making it the only doubly-blocked check in the facade.

**Unblock shape (lower risk).** The position-dependence lives in the **anchor expression**, not
in the by-path policy. A check module can load the same file with an anchor that climbs one
level — `Path(__file__).resolve().parent.parent / "gitenv.py"` — preserving the property that
matters (no `sys.path` entry can intercept a path load) exactly. Crucially, `gitenv.py`'s own
contract **already sanctions a second module object**: *"Each consumer gets its own module
object and therefore its own cache — behaviourally identical … the invariant that matters is
the defining FILE, never object identity."* So a fourth consumer is within the existing
decision rather than an amendment to it. The alternative — moving the load into `_common.py` as
a single owner — is architecturally cleaner but **reddens `tests/test_gitenv.py::
test_no_consumer_loads_the_scrub_by_NAME`**, which asserts the literal string
`spec_from_file_location` is present in `audit.py`.

**Coverage gap the lane must close, and it is outside the dispatch's stated scope.** All three
gitenv guards enumerate consumers by **hardcoded tuple** — `("audit.py", "fleet_parity.py",
"fleet_analytics.py")`, `(aud._gitenv, fp._gitenv, bm._gitenv, fa.gitenv)`, and `("audit.py",
"fleet_parity.py", "batch_manifest.py")`. A new consumer under `audit_checks/` is invisible to
every one of them: it could regress to a name-based load and **no test would fire**. Adding it
to those tuples is a `tests/test_gitenv.py` edit.

**Who must rule.** The **architect**, on one question: *does a fourth consumer with a climbing
anchor fall inside the [#396] by-path decision, or amend it?* The reading above says inside —
the file-identity invariant is preserved and the docstring pre-authorises multiple objects — but
the decision is defended by a terra HIGH ×3 finding, so the lane must not self-certify it. The
operator's GO can carry it if the architect's reading is recorded first.

### 3.2 The landing-predicate N-1 site naming `scripts/audit.py`

**Shape of the block.** `protocols/STANDING_RULINGS.md` §N-1 declares a `landed:` predicate
with four sites, one of which is `site: scripts/audit.py | pattern: from markdown_it import
MarkdownIt`. The chain `check_import_edges → _import_targets → _strip_code_regions → _FENCE_MD
= MarkdownIt("commonmark")` is the **only** consumer of `markdown_it` in `audit.py` (its sole
occurrences are the import and that one construction). Moving the check therefore moves the
import, `scripts/audit.py` stops matching the pattern, and the ruling's sites become **mixed**
— 3 landed, 1 not — which `check_landing_predicate` emits as **FAIL** (one Finding per ruling,
undispositioned). A pure relocation would redden a gate by doing exactly what it was asked to.

**Unblock shape.** Update the site to name the new home
(`site: scripts/audit_checks/check_import_edges.py | pattern: from markdown_it import
MarkdownIt`) — a one-line change inside the fenced block. The obstacle is not the edit but the
register's amend discipline: `STANDING_RULINGS.md` is append-not-amend (B6), demonstrated
in-file by the "PRESENT TENSE SUPERSEDED" bullet deliberately **left unrewritten** when its
claim expired. So the question is whether a `landed:` site list is *decision content*
(immutable) or *machine-readable state about where a mechanism currently lives* (editable in
place, as ADR-94 carved out for an ADR status line). §N-1's own expiry clause — "retires only
if the mechanism itself is retired" — says a **move is not a retirement**, which is an argument
for editing the site list rather than superseding the entry.

**The alternative, named and rejected.** Leave a bare `from markdown_it import MarkdownIt` in
`audit.py` to keep the pattern matching. It is an unused import (`ruff` F401), and it
manufactures a landing site that reflects nothing — a predicate that passes while measuring
nothing, which is the identical failure mode the entire [#533] seam work exists to prevent.
Rejected on those grounds, not on style.

**Who must rule.** The **operator/architect**, on the register-semantics question: *may a
`landed:` site list be edited in place when the mechanism relocates?* It is a general ruling —
it will recur for every future extraction that moves a declared site — so it belongs in the
register as its own entry, not as a one-off note in the seam lane's packet.

---

## §4 · Risk-ranked extraction order — CLEAR

Ranked by **blast radius of the unblocking act**, then by independence. The principle: a wave
must not begin until the wave it depends on is green, and the early waves are chosen so that a
mistake is cheap and local.

### Wave 1 — exclusive seams, one test file each (4 checks) · LOW risk

Each of these reads seam names **no other facade check reads**, and all its pins live in a
single test file. Verified exclusive: `_git_last_commit_date`, `_git_registered_worktrees`,
`_git_linked_worktrees`, `_git_stash_entries`, `DEPLOYED_VERSIONS_REGISTRY`,
`_git_repo_root_name`. A mistake here cannot reach another check.

| Order | Check | Unblocking act | Sites | File |
|---|---|---|---|---|
| 1 | `check_deployed_methodology_version` | R3 on 2 exclusive names | 4 | `test_audit.py` |
| 2 | `check_no_sibling_orphans` | R3 on 1 exclusive name | 9 | `test_audit.py` |
| 3 | `check_canonical_freshness` | R3 on 1 exclusive alias (Class C) | 7 | `test_audit.py` |
| 4 | `check_stale_worktrees` | R3 on 2 exclusive names + shared `_git` | 24 | `test_stale_worktrees.py` |

Run order 1–3 first: they are the cheapest possible rehearsal of the R3 mechanics on names
nothing else touches. **`check_stale_worktrees` is last in the wave** because it also reads the
shared `_git`, so it is the first act that must respect a seam another check uses.

### Wave 2 — the `_is_hub` / `_REPO_ROOT` bloc (21 checks) · HIGH risk, ONE act

68 patch sites across **17 test files** unblock **21 of the 25** checks. This is one act, not
21: the re-point either lands whole or is reverted whole, because a half-re-pointed bloc is the
silent-detachment state itself.

- **Do the re-point as its own commit, extracting nothing.** Full suite green on the re-point
  alone is the proof that intent survived; only then do the moves.
- Then extract in `CHECK_ORDER` order, one commit per check, so a bisect lands on one check.
- **Four checks in this bloc carry additional seams and belong to Wave 3**, not here:
  `check_doc_claims`, `check_doc_code_coverage_drift`, `check_landing_predicate`,
  `check_silent_rule_ratchet`, `check_task_tree_coherence`, `check_intake_tree_coherence` — and
  `check_fleet_audit_replication` is bloc-only but held to Wave 4 by `_gitenv` (§3.1). Bloc-only
  members extractable at the end of Wave 2: **14** (`check_hooks_armed`,
  `check_git_backlog_drift`, `check_no_ff_merges`, `check_doc_rot`, `check_doc_structure`,
  `check_doc_code_edge`, `check_enforcement_coverage`, `check_undeclared_edges`,
  `check_fleet_parity`, `check_journal_spine_anchor`, `check_journal_day_letters`,
  `check_preflight_backlog_ids`, `check_review_artifact_coverage`,
  `check_membership_agreement`).

### Wave 3 — multi-seam residue (6 checks) · MEDIUM risk, needs Waves 1–2 green

| Check | Additional seam(s) beyond the bloc | Note |
|---|---|---|
| `check_doc_claims` | `ALL_CHECKS`, `_GATE_MODE` | `ALL_CHECKS` stays a live global (**W2**) |
| `check_doc_code_coverage_drift` | `ALL_CHECKS` | **W2** and **W3** both bind here — extract last of the three |
| `check_landing_predicate` | `DISPOSITION_REGISTER` | R4 — carry the import-time derivation across unchanged |
| `check_silent_rule_ratchet` | `_ref_baseline_state`, `_index_worktree_divergence`, `_git` | densest seam set in the facade |
| `check_task_tree_coherence` | `_index_worktree_divergence`, `_git` | shares both with the two neighbours |
| `check_intake_tree_coherence` | `_index_worktree_divergence`, `_git` | extract alongside `task_tree` — same seams |

### Wave 4 — the ruling-gated checks (3) · BLOCKED on a human decision, not on code

| Check | Blocked on | Ruler |
|---|---|---|
| `check_handoff_probes` | §3.1 gitenv anchor reading | architect |
| `check_fleet_audit_replication` | §3.1 **and** Wave 2 (doubly blocked) | architect |
| `check_import_edges` | §3.2 register-amendability of a `landed:` site list | operator/architect |

**These three should be put to the ruler at lane GO, not when the lane reaches them** — they
are the only items on the critical path that cannot be resolved by working harder, and both
questions are answerable in a sentence.

### End state

Wave 1–3 land 24 checks (4 + 14 + 6); Wave 4 lands the final 3, taking `scripts/audit_checks/` from 16/43 to
43/43 and reducing the facade to registry, CLI, writer and shared primitives.

---

## §5 · Draft seam-lane contract — CLEAR, with a scope correction

### 5.1 The scope correction, stated before the contract

The dispatch specifies the lane be scoped *"strictly `tests/test_audit.py` + the re-point
targets."* **Measured, that scope is too narrow, and by a wide margin:**

- `tests/test_audit.py` carries **55 of 181** name-rebind sites — **30%**.
- For the Wave-2 bloc specifically it carries **14 of 68** — **21%**. The other 54 sit in 16
  files, the largest being `test_membership_agreement.py` (10), `test_batch_manifest.py` (9),
  `test_fleet_audit_replication.py` (9) and `test_task_tree_gate.py` (9).
- Two further files are needed that are neither `test_audit.py` nor a re-point target:
  `tests/test_gitenv.py` (§3.1 consumer tuples) and a new identity guard for §2.1.

A lane held to the literal scope would re-point 21% of the bloc and leave the rest patching a
name nothing reads — **the silent-detachment state, at scale**. The contract below therefore
scopes by *seam*, not by file, and names the file list as measured output.

### 5.2 The contract

```markdown
# LANE — [#533] SEAM RE-POINT (WAVE 1 + WAVE 2)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — contract-is-the-plan, NO plan-mode | high |

> Fresh CC session (`/clear`). Worktree lane — commit-and-STOP, never merge.

**Worktree (STEP 0):** `git worktree add ../worktree-lane-533-seam -b worktree-lane-533-seam main`
**Governing row:** `[#533]`. **ADR-110:** save this prompt as
`docs/audits/<date>-technical-533-seam-lane-contract.md`, COMMIT FIRST.
**Input of record:** `docs/audits/2026-08-19-technical-n2-seam-worksheet.md` (census §1,
recipes §2, order §4). Its counts are measured — re-measure before trusting, do not inherit.

## SCOPE — by SEAM, not by file
IN:
  - `scripts/audit.py` — remove re-pointed seam names (NO back-compat re-exports; §2.3)
  - `scripts/audit_checks/_seam.py` — NEW; the single owner of the re-pointed names
  - `scripts/audit_checks/_common.py` — single-owner dual-import for the validator aliases (§2.1)
  - EVERY `tests/*.py` file carrying a pin on a re-pointed name — measured, currently 21 files.
    `tests/test_audit.py` is 30% of the sites; scoping to it alone re-creates the defect.
  - `tests/test_gitenv.py` — ONLY if Wave 4 is authorised at GO (§3.1); otherwise untouched.
OUT:
  - No check is MOVED in this lane. Re-point only. Extraction is the next lane.
  - The writer/CLI-layer pins in `tests/test_writer_integrity.py` (`discover_repos`,
    `load_state`, `save_state`, `append_history`, `generate_report`, `write_report`,
    `audit_repo`, `resolve_repo_path`, `_commit_routine_outputs`, `_today`) — same mechanism,
    different subject. Out of scope; do not "while I'm here" them.
  - `BACKLOG.md`, `tasks/`, ADRs, `protocols/STANDING_RULINGS.md`.

## THE FOUR RULES
1. NO BACK-COMPAT RE-EXPORTS for a re-pointed name (one carve-out — see rule 4). `monkeypatch.setattr` raises on a missing
   attribute, so removal turns every missed site into a LOUD error. A re-export turns the same
   miss into a silently detached seam. This is the lane's whole safety argument.
2. NEVER EDIT AN `assert`. The diff touches patch targets and imports ONLY. A changed assertion
   is a changed test, and a changed test cannot prove parity.
3. CHECKS STAY PLAIN MODULE-LEVEL FUNCTIONS in `ALL_CHECKS` — no partial, closure, adapter or
   decorator. `audit._markers_for_check` reads `# rule:` markers via `inspect.getsourcelines`
   + a `fn.__module__` source walk-back; a wrapper breaks the drift-guard (§2.5 W3).
4. NO DEPENDENCY INJECTION for `ECOSYSTEM_DIR` or `ALL_CHECKS`. Two tests deliberately poison
   a global and assert the check ignores it / reads the live registry; DI makes them vacuous
   (§2.5 W1, W2). `ECOSYSTEM_DIR` is the ONE carve-out to rule 1: KEEP it on `audit` — the
   poison test needs the attribute to exist in order to patch it. And do NOT collapse
   `_REPO_ROOT` pins into `_is_hub` pins (§2.5 W4).

## ORDER (do not reorder)
  A. `_seam.py` + `_common.py` single-owner import; add the `aud._vgb is <module>._vgb`
     identity guard (§2.1). Suite green. COMMIT.
  B. Wave 1 — the 4 exclusive seams, one commit each, in worksheet §4 order. Suite green
     after EACH. COMMIT each.
  C. Wave 2 — the `_is_hub`/`_REPO_ROOT` bloc, 68 sites / 17 files, as ONE commit. A
     half-re-pointed bloc IS the defect. Suite green. COMMIT.
  D. STOP. Extraction is the next lane.

## PARITY-WITH-BEFORE PROOF (all five, in the packet, or the lane is not done)
  P1. `pytest -x --tb=short` green, and the collected test count is IDENTICAL to the
      pre-lane baseline captured at STEP 0. Same tests, not merely a green run.
  P2. `python scripts/audit.py health` output BYTE-IDENTICAL to the STEP 0 capture
      (`diff` the two, paste the empty diff). Emission order is part of the output contract.
  P3. `git diff` contains ZERO changed `assert` lines:
      `git diff -U0 -- tests/ | grep -E '^[+-]\s*assert' | sort | uniq -c` -> every `+`
      line has a matching `-` line with identical text, or the count is 0. Paste it.
  P4. NO re-export left behind: `grep -nE '^(_is_hub|_REPO_ROOT|...) *=' scripts/audit.py`
      returns nothing for each re-pointed name. Paste the empty result.
  P5. Registry agreement — close the HONEST LIMIT `registry.py` states about itself:
      add the test asserting `CHECK_ORDER == tuple(f.__name__ for f in audit.ALL_CHECKS)`.
      The lane is about to churn this surface; leaving it hand-maintained is the risk.

## REFUSE-TO-FINISH
  - Any of P1-P5 unproduced -> the lane is OPEN. No packet, no merge.
  - The bloc commit red at any point -> revert the WHOLE bloc, do not repair forward.
  - A seam whose re-point would need an `assert` change -> STOP and report it. It is a
    weakening trap the worksheet missed; it needs a ruling, not a judgement call.
```

### 5.3 Why these five proofs

P1 and P3 together are the intent-equivalence argument: same tests, same assertions, only the
owner named in the patch target changed. P2 is the behavioural argument, and it is byte-level
because emission order is part of the contract the hooks consume. P4 is the mechanical proof
that R3's safety property actually holds — without it, the "loud not silent" claim is untested.
P5 is the one addition beyond parity, and it is justified narrowly: `registry.py` documents that
**nothing asserts `CHECK_ORDER` agrees with `ALL_CHECKS`**, and this lane is the first to churn
both. Closing it costs one test.

---

## §6 · Three measured disagreements with the received text

Recorded because the dispatch asked for the tree as merged today, and in three places the tree
disagrees with the text describing it. None changes the shape of the work; all three change its
size, so they belong before the contract rather than inside it.

**D1 · `_is_hub` blocks 21 checks, not 19.** `scripts/audit_checks/registry.py` states
*"`_is_hub` … alone accounts for 19 of the 25 held-back checks."* Two independent methods put it
at **21**: an AST closure walk, and an `awk` pass attributing every `_is_hub(` call site to its
enclosing function. All 21 are **direct depth-1 calls** — no transitive inference is involved,
so this is not a difference of method. The 25-check total and the `_REPO_ROOT` co-occurrence are
confirmed; only the "19" is off. Consequence: Wave 2 is ~10% larger than the registry implies.

**D2 · the `_gitenv` class holds two checks, not one.** The dispatch and `registry.py` both
present `check_handoff_probes` as the sole `_gitenv` casualty.
`check_fleet_audit_replication` also reaches `_git_location_env`, and it carries the bloc pin
too — the only doubly-blocked check in the facade. Consequence: Wave 4 is 3 checks, not 2, and
one of them cannot be attempted until Wave 2 is green.

**D3 · the pins are not confined to `tests/test_audit.py`.** Both `registry.py` ("`tests/`
patches these names") and the dispatch's §5 scope ("strictly `tests/test_audit.py`") can be read
as locating the work in one file. Measured: **181 sites across 21 files**, of which
`test_audit.py` holds 55. `registry.py`'s own 16-name list is accurate as far as it goes but
omits `_today` and the whole Class-D set. This is the finding with the largest practical
consequence and it is why §5.1 exists.

---

## Provenance

Every count reproducible from this checkout with the commands used to derive it:

```
grep -cE '^def check_' scripts/audit.py                 # 27 facade checks
python - <<'…'  ast closure walk over scripts/audit.py  # 25 pinned, 2 clean
awk '/^def /{fn=$2} /_is_hub\(/ {print fn}' scripts/audit.py | sort -u | wc -l   # 21
python - <<'…'  strict-alias AST census over tests/*.py # 181 name-rebind + 38 attr sites
git merge-base --is-ancestor f4a01f0e HEAD              # leg 2 present
```

Analysis scripts were written to the session scratchpad, not to the repo — this lane is
read-only to `scripts/` and `tests/` and left both untouched.

---

## AMENDMENT 1 — 2026-08-18, at session wrap: the Stop hook is a fifth gates-unavailable instance

Added as an in-file amendment marker, not an edit to §0 (audits are immutable — CLAUDE.md §5
rule 3). §0 was written before session wrap; this instance was hit after it.

**What happened.** The `Stop` hook `session_end_backpressure.py` failed to run, with the same
root cause §0 already records — its wrapper is `uv run --locked`, and `uv` 0.8.17 refuses
against the `pyproject` `required-version = "==0.11.19"` pin. The failure is in the **runner**,
not in any check: no leg reported anything, because no leg executed.

**Useful for the next lane in this container:** the hook itself runs fine under the plain
interpreter — `python scripts/session_end_backpressure.py` exits 0 (silent pass). The uv pin
blocks the wrapper, not the script. Anything in `scripts/` that is stdlib-or-`yaml`-only can be
run directly; only `markdown_it` consumers (i.e. `audit.py`) are genuinely unrunnable here.

**All four advisory legs verified independently, since a silent pass under a hand-run hook is
not by itself evidence:**

| Leg | State | Evidence |
|---|---|---|
| dirty tree | clean | `git status --porcelain` → 0 lines |
| BACKLOG marker (ADR-85 R1) | none owed | the session's whole diff is 3 files, none is `BACKLOG.md` |
| canonical cadence | none owed | no `VISION`/`ARCHITECTURE`/`CLAUDE`/`CONTRIBUTING`/`ESSENTIALS` edit |
| JOURNAL anchor | **not owed here** | HEAD is `claude/seam-leg-monkeypatch-pins-91fh27`; the hard leg `block_unanchored_push.py` states its own scope — *"A push that does not target `main` is not this organ's business"* — and the `journal_spine_anchor` backstop walks `git log --first-parent main` |

**The JOURNAL anchor is owed at INTEGRATION, not here,** and that is a real obligation, not a
dismissal: these two commits carry no anchor, so whoever merges this branch to `main` owes a
JOURNAL entry naming ≥1 SHA the merge range introduces, or `block-unanchored-push` will refuse
the push (fails CLOSED, exit 2) and the `journal_spine_anchor` audit check will FAIL. That
matches the house pattern already visible in the log (`docs(journal): anchor the … arc`, done
by the integration arc, not by the lane).
