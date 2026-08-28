# NB2 · LANE E hand-back packet — [#605] de-hardcode consumer-root resolution

**Batch:** night-batch-2 · **Architect's lane id:** N6 · **Substrate:** local
**Branch:** `worktree-lane-e-605-consumer-root` · **Base:** `fcc94855` (main at freeze)
**Write-scope as frozen:** `deploy/tool.py` · `scripts/audit.py` · one new test file. Held: the
lane's whole diff is exactly those three paths (`git diff --name-only fcc94855..HEAD`).

---

## 1. Per-done-item verdict

### Done-item 1 — consumer-root resolution EXPLICIT in both modules, sibling default as fallback — **MET**

The contract required this be verified, not assumed ("the row's premise that it is *hardcoded*
in **both** modules is itself a claim to verify"). Verified at the base commit, and the two
modules were **not** the same defect — which is what the `tasks/` row already said and what the
grep confirms:

| Module | At `fcc94855` | Verdict |
|---|---|---|
| `deploy/tool.py:216-223` | `return (hub_root.parent / repo).resolve()` — **unconditional**, no escape of any kind | hardcoded sibling |
| `scripts/audit.py:603-616` | hub → `_REPO_ROOT`; else `stored_path` if truthy; else `_REPO_ROOT.parent / repo_name` | **already layered** — sibling only as fallback |

Witness (base-commit text, not a re-read of HEAD):

```
$ git show fcc94855:deploy/tool.py | grep -n "def resolve_repo_root" -A 8
216:def resolve_repo_root(repo: str, hub_root: Path = _HUB_ROOT) -> Path:
217-    """Resolve a registry repo-name to its working-tree path (a sibling under Dev/).
...
223-    return (hub_root.parent / repo).resolve()

$ git show fcc94855:scripts/audit.py | grep -n "def resolve_repo_path" -A 13
603:def resolve_repo_path(repo_name: str, stored_path: Optional[str]) -> Path:
612:    if repo_name == HUB_REPO_NAME:
613:        return Path(_REPO_ROOT)
614:    if stored_path:
615:        return Path(stored_path)
616:    return Path(_REPO_ROOT).parent / repo_name
```

**So the premise is PARTIALLY TRUE and the distinction matters**: `audit.py`'s `stored_path` is
`path:` from `ecosystem/<repo>/state.yaml`, which is **gitignored**. On a fresh checkout it says
nothing, so the sibling fallback is all there is and the observable outcome is identical to
`deploy`'s. Only one of the two was unconditional; both needed the fix.

**Landed precedence** (identical in both modules, sibling **last**):

1. explicit argument — `deploy --repo-root <path>` / `preflight(..., repo_root=)` /
   `resolve_repo_root(..., explicit=)`; `audit repo --repo-path` / `resolve_repo_path(..., explicit=)`
2. `DEV_KNOWLEDGE_REPO_ROOT_<SLUG>` — derived from the registry key, so a newly registered
   consumer needs no code change
3. registry entry — `path:` in `ecosystem/<repo>/state.yaml`
4. sibling default `<dev>/<repo>`, where `<dev>` is `DEV_KNOWLEDGE_FLEET_ROOT` when set and
   `hub_root.parent` / `_REPO_ROOT.parent` otherwise

Shape chosen per the contract's instruction to match what already exists rather than invent a
configuration surface: `ecosystem/*.yaml` is the registry home, `state.yaml` is the file that
**already** carries a per-repo `path:`, and `DEV_KNOWLEDGE_*` is the live env-var convention
(`audit.py:4207 TELEMETRY_ENV = "DEV_KNOWLEDGE_TELEMETRY"`,
`telemetry_emit.py:163 DB_PATH_ENV = "DEV_KNOWLEDGE_TELEMETRY_DB"`).

Witnesses: `deploy/tool.py::resolve_repo_root` + `registry_repo_root` + `repo_root_env_var`;
`scripts/audit.py::resolve_repo_path` + `repo_root_env_var`.

**Backward compatibility held, and it is tested, not asserted** —
`test_deploy_sibling_default_is_unchanged_when_nothing_is_set` and
`test_audit_sibling_default_is_unchanged_when_nothing_is_set`. A caller passing nothing gets the
pre-[#605] answer, which is what the contract required for lane A's behavioural adjacency.

### Done-item 2 — a non-sibling layout resolves in both, PROVEN BY A TEST — **MET**

`tests/test_consumer_root_resolution.py`, **27 tests collected, 27 passed**:

```
$ uv run --locked pytest tests/test_consumer_root_resolution.py -q
27 passed
```

Directly on the done-item:

- `test_deploy_resolves_a_non_sibling_layout_from_the_environment`
- `test_deploy_resolves_a_non_sibling_layout_from_the_registry`
- `test_audit_resolves_a_non_sibling_layout_from_the_environment`
- `test_deploy_fleet_root_relocates_the_sibling_parent` / `test_audit_fleet_root_relocates_…`
- `test_deploy_precedence_is_…` / `test_audit_precedence_is_…` — all four steps armed at once,
  so each higher step is proven to beat every lower one rather than proven in isolation

Each of the non-sibling tests asserts `not (hub.parent / "ai-council").exists()` **before**
resolving, so a test that accidentally resolved through the sibling rule would fail rather than
pass for the wrong reason.

Two hazards the contract named, both handled: **nothing is moved on disk** (every layout is
built under `tmp_path`, and the resolvers are driven with an injected `env=` mapping or a
monkeypatched `_REPO_ROOT`, never by mutating the ambient process environment); **nothing shells
out to git** (`GIT_DIR` overrides both `cwd=` and `-C`, so a git-touching test would silently
read the developer's own repo — the one test that drives the `audit repo` command injects the
git-touching writers out, the `tests/test_writer_integrity.py` pattern).

### Done-item 3 — `audit repo <name>` runs from a checkout with no sibling tree — **MET**

`test_audit_repo_command_runs_from_a_checkout_with_no_sibling_tree` drives `cmd_repo`'s callback
with `_REPO_ROOT` monkeypatched to a `tmp_path` hub whose parent holds nothing, asserts the
sibling path does not exist, and asserts the path `audit_repo` actually receives is the
non-sibling consumer tree — reached with **no `--repo-path`** and **no `state.yaml`**, i.e.
through the env-var step alone. That step is the one that makes the command reachable off the
laptop, because the state file is gitignored and a fresh hub clone has no stored path to fall
back to.

The CLI seam was also collapsed onto the resolver rather than left as a parallel branch:
`cmd_repo` previously did `if repo_path: Path(repo_path).resolve() else resolve_repo_path(...)`,
so the precedence lived in two places. It now calls
`resolve_repo_path(name, stored, explicit=repo_path)` once.

### Done-item 4 — `deploy/tool.py`'s docstring tells the truth — **MET**

The module docstring gains a **"Where the consumer tree comes from"** section naming all four
steps, stating plainly what was false before ("Until 2026-08-28 `resolve_repo_root` returned
`hub_root.parent / repo` unconditionally, with no escape — true only on the operator's laptop"),
adding the `--repo-root` line to the CLI block, and correcting preflight gate 3 from "the
consumer `<repo>` working tree is clean" to "**resolves, exists, and is clean**". It also points
at `scripts/audit.py::resolve_repo_path` as the sibling implementation and says the two are
deliberately not folded.

This is the same class of correction the docstring already carries for C2b (the "scaffolded,
never implemented" claim that was false at HEAD for months) — the file has a recorded history of
its own prose being the first thing a lane reads and the first thing that misleads it.

---

## 2. Commits on this branch, in order

| SHA | Subject |
|---|---|
| `79d5707b` | `fix(deploy,audit): de-hardcode consumer-root resolution [#605]` |
| *(this packet)* | `docs(audit): NB2 lane E hand-back packet [#605]` |

No generated surface was regenerated, so there is **no** "regeneration to keep my own commit
legal" commit to name (contract item 4). Every pre-commit gate passed on `79d5707b` without a
`SKIP=` and without `--no-verify`.

---

## 3. Terra tally

Reviewer run as `codex exec` over the staged diff (not `/codex-review` — a mixed doc/code diff
kills that lane). Two rounds, because round 1 found a real defect:

```
r1  TALLY: critical=0 high=1 medium=0 low=0
r2  TALLY: critical=0 high=0 medium=0 low=0
```

**Round-1 HIGH, accepted and fixed** — `scripts/audit.py:4927`, and it was a regression *this
lane introduced*: `audit.py run --repo-path <path>` bootstraps `state.yaml` and then falls
through to the normal loop, where the path reached the resolver as `stored_path`. Inserting the
env var **above** the stored path silently demoted the operator's own command-line answer, so a
set `DEV_KNOWLEDGE_REPO_ROOT_<SLUG>` would register one tree and audit another.

Fix: `cmd_run` carries the bootstrapped `(name, path)` forward and passes it as `explicit` for
that repo only. Regression test `test_audit_run_bootstrap_path_outranks_the_environment`.

Note on the shape of that fix, because it looks odd on purpose: the **non-bootstrap** call site
stays two-positional. `resolve_repo_path` is a documented monkeypatch seam —
`tests/test_writer_integrity.py:364,434` substitute a two-argument `lambda n, _p:` — and that
file is outside this lane's write-scope, so the `explicit=` keyword is passed only on the branch
that has an explicit answer to pass. The reason is in a comment at the call site.

---

## 4. Gate state

| Gate | Result |
|---|---|
| `uv run --locked python scripts/audit.py health` | **health: OK** (no FAIL; WARNs pre-existing — see §6) |
| `uv run --locked ruff check` (3 changed files) | **All checks passed** |
| `uv run --locked python scripts/silent_rule_detector.py` | **443 / 61 / silent-rule-v5** — dispatch-time value, **delta 0** |
| pre-commit on `79d5707b` | all hooks Passed / Skipped; no bypass |

Ratchet measured **before the first commit and again before the last**, per the shared clause;
both readings are `count: 443, files: 61, detector: silent-rule-v5`. This lane touched no
`protocols/` or `templates/` file, which is why the delta is structurally zero rather than
merely observed zero.

### Targeted tests (the files covering this lane's diff; full suite is the integrator's)

| Selection | Result |
|---|---|
| `test_consumer_root_resolution.py` | 27 passed |
| `test_consumer_root_resolution` + `test_hub_identity` + `test_writer_integrity` | 58 passed |
| `test_hub_identity` + `test_writer_integrity` + `test_deploy_tool_assess` + `test_deploy_tool_execute` + `test_consumer_root_resolution` | 91 passed (348 s) |
| `test_enforcement_coverage.py` (downstream consumer of `resolve_repo_root`) | 44 passed, **1 inherited RED** — §6 |

---

## 5. Candidate filings for the integrator — REPORTED, NOT FILED

No `tasks/` write was made (lane D is the batch's exclusive `tasks/` writer) and no row was
closed.

**CF-1 — `ecosystem/doc-counts.md` / the `doc_claims` check will need regeneration.**
This lane adds one test file. `doc_claims` is declared **ship-tier** and so reads `n/a` at the
commit gate (`[--] doc_claims: declared ship-tier -- not run at the commit gate ([#597] per-check
tiering)`), but it runs at the ship-gate and on `audit run`. Resolution is
`gen_doc_counts.py --write` on the merged result — i.e. exactly the shared clause A5 regeneration
the integrator already owns. Named here so it is expected rather than discovered.

**CF-2 — `deploy/tool.py:98 HUB_DIR_NAME = _HUB_ROOT.name` is the same defect class, one site
over, and is NOT fixed here.** In a worktree that constant evaluates to the *worktree directory
name*, not `.dev-knowledge`. Measured live from this lane:

```
hub_root      : ...\.claude\worktrees\lane-e-605-consumer-root
HUB_DIR_NAME  : lane-e-605-consumer-root
```

`scripts/enforcement_coverage.py:1016-1021` uses `HUB_DIR_NAME` as the key to *skip the hub* when
listing consumers, so from any worktree the hub is not skipped and `.dev-knowledge` is walked as
though it were a consumer. Left alone deliberately: `enforcement_coverage.py` is outside this
lane's frozen write-scope, and the row's anti-patterns forbid widening. It is a candidate, not a
finding this lane may act on.

**CF-3 — a behaviour change in a worktree, reported because it is a change even though it is an
improvement.** With the registry step live, `resolve_repo_root("ai-council")` **from a worktree**
now returns `C:\...\Dev\ai-council` (via `ecosystem/ai-council/state.yaml`) where it previously
returned `...\.claude\worktrees\ai-council`, a path that does not exist. Same for the
`.dev-knowledge` key, which now resolves to the real primary hub. Nothing in the suite depended
on the old answer (`test_enforcement_coverage` is green apart from the inherited RED below), and
the primary-checkout answer is byte-identical to before. Flagged so the integrator sees it named
rather than inferring it from a diff.

**CF-4 — the fold question, preserved.** The row was ruled KEPT SEPARATE from `[#294]`, and this
lane honours that: the two resolvers duplicate the precedence and share only the constant *names*
(`FLEET_ROOT_ENV`, `REPO_ROOT_ENV_PREFIX`, `repo_root_env_var`). A test —
`test_both_modules_agree_on_the_env_var_constants` — asserts the two modules agree, so the
duplication cannot drift silently. A fold, if ever wanted, remains a deliberate act with its own
reason; nothing here decides it by silence.

---

## 6. Deviations and inherited state, each with an owner

**D-1 — inherited RED, PROVEN inherited, not this lane's.**
`tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent`
fails on this branch. The contract pre-declares it ("the anchor-gate probe test has been RED on
main since 2026-08-22"), but a pre-declaration is not evidence, so it was measured: a detached
worktree at the batch base `fcc94855` — *before any file this lane touched* — produces the
**identical** failure:

```
$ git worktree add --detach <tmp>/base-check HEAD~1     # HEAD is now at fcc94855
$ python -m pytest tests/test_enforcement_coverage.py::test_anchor_gate_probe_… -n 0
E   AssertionError: … pre-push organ REFUSED an anchored push too (exit 1) — it does not
    discriminate; a constant refusal enforces nothing
    assert 'absent' == 'enforcing-local'
1 failed in 13.40s
```

The failing assertion probes the `block-unanchored-push` pre-push organ and reaches no
consumer-root code. Not fixed here — the contract forbids fixing an inherited RED inside a lane.
**Owner:** whoever owns the anchor-gate probe row. The scratch worktree was removed and the
removal verified (`git worktree list` shows no `base-check`; `git status --porcelain` empty).

**D-2 — `test_stale_worktrees` was not exercised.** The known structural lane-worktree RED sits
in the full suite, which this lane does not run ([#528]; the full suite runs once, at
integration). Reported as expected, not as observed. **Owner:** integrator.

**D-3 — the commit body of `79d5707b` says "28 cases"; the file collects 27.** An off-by-one in
prose written before the final collection count. The code, the tests and this packet are correct
at 27; the commit message is immutable and is wrong by one. Recorded rather than left for a
reader to trip over. **Owner:** this lane.

**D-4 — no JOURNAL entry, deliberately.** A batch lane never journals; the integrator writes one
anchor for the whole queue after every lane has STOPped. The session-end Stop hook's demand for a
JOURNAL entry naming these SHAs is **declined explicitly on that ground** — it is advisory in
full since the ADR-85 amendment 2026-08-03 §A5, the hard leg is `block-unanchored-push` at
pre-push, and this lane does not push.

**D-5 — no self-merge, no merge command named.** Hand-back ends at branch + SHAs + gate state +
findings. Merge order (after N1/lane A, per D4) is the integrator's constraint; this lane did not
read lane A's branch, coordinate with it, or wait on it.

---

## 7. Decisions taken under the V-2 budget

The shared clause allows standing rulings silently and reserves the operator for four forks
(curated-baseline / rule-vs-ruling / no-ruling fork / out-of-scope path). **None of the four was
hit, so nothing was escalated.** Decisions taken per defaults:

**B-1 — the registry surface is `ecosystem/<repo>/state.yaml`, not a new file and not
`deployed-versions.yaml`.** The contract says pick what already exists ("library-first on our own
organs"). `state.yaml` already carries `path:` and is already what `audit.py` reads;
`deployed-versions.yaml` is a *committed* ADR-91 record with a "one concern per file" header and
a write-contract owned by the deploy runbook, so a machine-specific absolute path does not belong
in it. Adding one would also have been the manifest-adjacent widening the dispatcher's honest
note warns about.

**B-2 — `--repo-root` was added to the `deploy` CLI.** Done-item 1 says resolution must be
*explicit in both modules*; `audit repo` already had `--repo-path`, and without the mirror the
explicit step would have been reachable from a library caller but not from the command line.
Default `None` ⇒ behaviour identical to before. Judged inside the contract rather than a
widening, and recorded here so the integrator can disagree cheaply — reverting it is deleting one
option and one parameter.

**B-3 — preflight refusal semantics untouched.** `preflight` gained a `repo_root=` keyword that
selects *which* tree the gates read; every gate, every `PreflightError` and every message is
byte-identical. The anti-pattern is not tripped.

**B-4 — the [#465] hub binding was kept ABOVE env and registry.** Only `explicit` outranks it,
because `--repo-path` already outranked it at the CLI. If an environment variable could capture
the hub, every hub-only check would skip as `n/a` from a mis-set shell — the exact 14-WARN
collapse [#465] closed, re-opened through a new door. Pinned by
`test_audit_env_cannot_undo_the_hub_binding`.

**B-5 — no count pin was touched.** The contract's trap warning holds: this row is a resolution
seam, not a new check. `ALL_CHECKS` is unchanged, no oracle test moved, and the six count-pin
sites were not edited — which is itself the evidence that the change did not grow past its
contract.

**B-6 — the registry step is fail-soft.** An absent, empty or malformed `state.yaml` contributes
nothing rather than raising. "Missing" is the *normal* case (the file is gitignored), so a raise
would make the sibling fallback unreachable — the opposite of the row's intent. Five malformed
shapes are parametrized in `test_deploy_registry_step_is_fail_soft`.

---

## 8. STOP

Lane E is complete and stopped. Branch `worktree-lane-e-605-consumer-root` is committed, clean,
unpushed and unmerged, awaiting the integrator's frozen queue order.
