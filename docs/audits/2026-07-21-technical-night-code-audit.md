# Night code audit — code quality / Clean Architecture (Lane 2 of 3)

Read-only critical review · ADR-101 class `technical` · no repo file mutated to produce it
(the one exception is the generated `docs/audits/README.md` index, regenerated in the same
commit because the `audit-index-freshness` gate requires it — see §9).

## 0. Triage criteria — apply these, do not re-judge by feel

This report is written so that morning triage is a **test**, not a vibe.

- A finding becomes a **ticket** only if it names `file:line` **and** states a **falsifiable
  defect** — something a reader could prove wrong by reading the code or running one command.
- An opinion **without a location** is a **logged-reject**, recorded in §8 with a one-line
  reason. It does not get a ticket, and it does not get re-litigated.
- Every finding below carries a **verification stamp**:
  - `[verified]` — the auditor reproduced it directly at HEAD (command or code read recorded).
  - `[reported]` — a reviewer asserted it with a cited location; not independently re-run.
  Only `[verified]` findings should be treated as settled fact.
- **De-dup rule:** a finding already covered by an open ticket is annotated, not re-raised.
  Where an existing ticket is *adjacent but does not cover* the finding, that is stated
  explicitly, because "adjacent" is where duplicate tickets get manufactured.

**No ticket ids are filed by this report.** Every finding is a proposal for the operator.

## 1. Scope

### 1a. Scope correction — there is no `src/`

The commissioning prompt specified "`src/` critical review". **This repo has no `src/`
directory.** Per `CLAUDE.md` §3 it is not a code project: markdown governance files plus
read-only validators. The review was therefore retargeted to the actual Python surface. This
is recorded rather than silently adapted, because the difference matters for what the findings
mean: this is *tooling* code, and most of it is enforcement machinery that gates commits.

### 1b. What was reviewed

| Tree | Files | LOC | Character |
|---|---|---|---|
| `scripts/` | 57 | ~17.4k | validators, generators, gates, hook entry points |
| `deploy/` | 17 | ~5.5k | methodology deployment (carriers, manifest, lived sandbox) |
| `plugins/tier1-lifecycle/` | 5 | ~1.1k | distributable plugin (ships to consumer repos) |
| `.claude/skills/verify/` | 1 | 43 | verify skill |
| **Production total** | **80** | **25,636** | |
| `tests/` | 100 | 24,286 | reviewed as evidence + §7 test-debt only |

Size distribution (production): **4** files ≥1000 lines · **4** at 500–999 · **20** at
300–499 · **52** under 300.

### 1c. Method, and its limits

Seven reviewers ran in parallel over disjoint slices (audit.py; fleet_parity +
enforcement_coverage; deploy/; cross-`scripts/` consistency; dependency graph; dead
code/tech-debt; mid-band sizing). All seven returned. **Every headline claim was then
independently re-verified by the auditor at HEAD** before being written down — **53 checks**,
including three live reproductions (§4 H1, §5 F1, §5 F6). Claims that could not be reproduced
are marked `[reported]`.

Two method notes, stated because they affect how much weight the report carries:

1. **One correction to the commissioning premise.** The prompt cited
   `crux_check.max_tokens` as proof the dead-config axis is real. **That symbol does not
   exist anywhere in this repo** `[verified]` — the only `max_tokens` hit is unrelated prose in
   a 2026-06-07 council transcript. That finding came from a different repo or lane. The
   dead-config axis was therefore **re-established independently here**, and it does hold (§6).
2. **One false finding was caught and discarded mid-audit.** An auditor scan initially reported
   "15 `_git` wrappers, 0 scrub the git env" — wrong, because the pattern `^def _git`
   prefix-matched helpers like `_git_location_env`. Corrected to **9 wrappers, 1 scrubs**. The
   corrected number is what appears in §6. Recorded because a plausible-looking scan producing
   a plausible-looking number is exactly the failure mode this report is supposed to resist.

## 2. Module health & size

**Headline: size is not this codebase's defect.** The two largest files are large for a
legitimate reason (they are registries of small, independent, uniform units), and the honest
verdict on the biggest file in the repo is *do not split it*.

| File | Lines | Verdict | Reason |
|---|---:|---|---|
| `scripts/audit.py` | 3082 | **FINE** (one seam) | L381–2390 is 31 independent checks, each `(repo_path) -> list[Finding]`, no cross-talk, driven by a runtime registry (`ALL_CHECKS`, L2393). That is a legitimate shape. The **one** genuine seam is L2548–2738 — the ADR-84 git *writer* (`fp.unlink()` L2594, `commit-tree` L2715, `update-ref` L2724). Everything else in the file reads. |
| `scripts/fleet_parity.py` | 1974 | **SPLIT** (3 seams) | Clean seams with no back-edges: manifest/schema L181–402 → `parity_manifest.py`; PyPI-specifier comparator L746–864 → `dep_parity.py`; digest+events L1609–1812 → `parity_report.py`. Residual core ~900 lines is genuinely one responsibility. The pure/impure split (`collect_facts` impure → `verdicts` pure) is the file's best property and any split must preserve it. |
| `deploy/tool.py` | 1333 | **SPLIT** (2 seams) | Already well-layered (git transport → preflight → factory → domain model → use cases → render → CLI), so this is extraction, not untangling. Two clean seams: **rendering** `render_plan` L622–701 + `render_execute` L1141–1266 (~205 lines of pure presentation, zero domain logic) → `deploy/render.py`; **registry persistence** L724–767, L787–855, L858–870 (~150 lines of git plumbing with its own `RecordError`) → `deploy/record.py`. Leaves ~950 lines of cohesive orchestration. |
| `scripts/enforcement_coverage.py` | 1082 | **SPLIT** (narrow) | The Tier-1 organ registry L360–738 is **exemplary** — 5 organs × 3 small functions on a uniform contract, one 5-row dispatch table. Do not touch it. Split off only: allowlist L158–248, shared repo-facts readers L142–155/L250–311, and Tier-2/Tier-3 L741–906 (the module's own comments call these a separate axis, and they are the sole reason it depends on `deploy/`). |
| `deploy/carrier_precommit.py` | 976 | **SPLIT** (1 clear seam) | The YAML surgical-splice engine — 4 `_Op` dataclasses L271–301 plus `_unquote`/`_line_body_eol`/`_RepoSpans`/`_scan_repo_spans`/`_render_yaml_lines`/`_apply_one_op`/`_surgical_edit` L416–611 — is ~230 lines of pure, domain-free YAML text manipulation with no knowledge of carriers, manifests, or deploy → `deploy/yaml_splice.py`; carrier drops to ~745. This is also the **most defect-prone code in the subsystem** (regex-driven YAML editing behind a parse-equal safety net) and it is currently buried where it cannot be tested or reused on its own merits. |
| `scripts/reverse_dep_oracle.py` | 547 | **FINE** | One-way layered stack: CLI → render → oracle → {LSP transport, AST resolution, git provenance}. No upward calls. Largest function 59 lines. |
| `scripts/gen_handoff.py` | 526 | **FINE** | `generate()` is a composition root; render layer has no mode knowledge, collectors have no template knowledge. Named growth axis: adding a mode needs 4 uncoordinated edits (L49, L112, L496, + a branch in `generate()`). |
| `scripts/fleet_health.py` | 525 | **SPLIT** (narrow) | `groom_escalation_line` L112–152 + constants L51–58: zero in-file callers, parses `BACKLOG.md` not fleet state, explicitly unthrottled while the file's whole premise is a daily throttle, and is a knowing duplicate of `validate_doc_rot._latest_groom_date`. |

**300–499 band (20 files).** Six were individually verdicted, all **FINE**:
`verify_handoff_probes.py` (459, lexer→parser→resolver→classifier),
`session_end_backpressure.py` (448, check-registry),
`coherence_enumerator.py` (398, pure core + thin adapters), plus three by structure. The
remaining 14 showed no size-driven decomposition problem on inspection. **Under 300 lines (52
files): not a size concern and not individually verdicted.**

**Net:** 2 clear SPLITs (`fleet_parity`, `enforcement_coverage`), 1 narrow SPLIT
(`fleet_health`), 1 seam-extraction (`audit.py`). Everything else that is large, is large for
a defensible reason.

## 3. What is genuinely well-built

Stated first and plainly, because several §4–§7 findings would otherwise read as a worse
codebase than this is — and because a "split it / rewrite it" reflex would damage these.

- **The check-registry pattern is real, not decorative** `[verified]`. `audit.py` derives its
  CLI inventory from `ALL_CHECKS` at runtime, so the documented check list *structurally
  cannot* drift from what executes. All 31 members return `list[Finding]`; none returns a bare
  Finding or `None`; no check writes state another reads; the two module globals are set by the
  command wrapper or are order-invariant caches. Checks are freely reorderable.
- **The carrier abstraction is real** `[verified]`. `deploy/contract.py:159` is a true ABC with
  real invariants; all five carriers inherit it and implement exactly `detect`/`apply`/`verify`,
  all set `carrier_id`, all are keyed by it in `make_carriers` (`tool.py:315-323`). **5/5
  structural conformance.** The suspicion that these were five files sharing a naming prefix is
  **refuted** — it is a designed interface and the design is good. *(But it is uniform in
  **signature** only; six behavioural divergences, two of them defects, are in §5 F12–F13 and
  §7 T10. The problem there is enforcement of the contract, not the contract.)*
- **The prune leg is correctly optional** `[reported]` — absent from 4 of 5 carriers, but
  `contract.py:100-104` declares it opt-in with a loud `PruneUnsupported`, and
  `build_prune_plan` captures it as an error row. Not a gap.
- **`deploy/` beats `scripts/` on CLI consistency** `[reported]` — all three `deploy/` CLIs use
  click; `scripts/` is split 8 click / 12 argparse.
- **Zero debt markers across `deploy/`'s 6,700 lines** `[reported]`, and all 68 `#NNN` comment
  references were checked against live BACKLOG — only one (**#244**) is still open. The rest are
  provenance attribution, not deferrals. That is unusually good hygiene.
- **Error-handling discipline is genuinely good** `[reported]`. **Zero bare `except:`** in the
  corpus; every broad catch is `except Exception`, and 24 of 32 carry an inline comment naming
  the intended posture. `hooks/block_immutable_edits.py` is asymmetric *by design* — allows on a
  pre-zone-identification error, fails **closed** once a zone path is confirmed.
- **The house template is followed** `[reported]`. ~85% of `scripts/` conforms: `def main(...)
  -> int` + `sys.exit(main())` in 41 of 45; the frozen-dataclass result convention in 10 of 10;
  the repo-root idiom in 25 of 30; the 5-generator regen-and-diff template uniform.
- **The codebase passes its own lint gate** `[verified]` — `ruff check .` → *All checks
  passed*. The §6 lint findings are gaps in rule **selection**, not violations.
- **The TODO graveyard is empty** `[reported]` — exactly **one** `TODO` in all production code
  (10 days old, ticketed `[#312]`), and zero `FIXME`/`XXX`/`HACK`/`WORKAROUND`. This axis came
  up clean, which is itself worth recording.
- **The plugin is correctly self-contained** `[verified]` — `plugins/tier1-lifecycle/` has
  **zero** imports into the hub's `scripts/`, resolving its own bundled modules via
  `spec_from_file_location` against its own directory. Since it ships to consumer repos that
  have no `scripts/`, this is the difference between working and shipped-broken. It is right.
- **No hardcoded user, absolute, or OneDrive paths** anywhere in the Python surface
  `[reported]` — 26 root-resolution sites all derive from `Path(__file__)`.

## 4. Consistency & spaghetti

There **is** one dominant template and most files follow it (§3). The findings are its edges.

**H1 — MEDIUM (downgraded from HIGH — see the correction below) · `scripts/toc/cli.py:50`
CRLF-ifies the entire target file on `--write`.** `[verified — reproduced, then bounded]`
The line is `md_file.write_text(new_content, encoding="utf-8")`. Its twin
`scripts/codemap/cli.py:69` is the same line **with `newline="\n"`**, and carries a comment
citing #262 explaining exactly this hazard. `toc/` has the bug `codemap/` already fixed.
Reproduced on a scratchpad copy of `protocols/PLAYBOOK.md`: **3808 bare-LF → 3808 CRLF, whole
file flipped.** It fires on the *documented repair path* — `.pre-commit-config.yaml:37`
instructs `python -m scripts.toc.cli generate protocols/PLAYBOOK.md --write` as the fix for a
`toc-freshness-playbook` failure.

> **Correction applied during this audit — severity downgraded.** The reviewer tested on a
> scratchpad copy, i.e. **outside git**, where no normalization applies. Inside the repo,
> `.gitattributes:6` sets `* text=auto eol=lf`, so git normalizes CRLF→LF on staging.
> **Demonstrated inadvertently on this very commit** `[verified]`: regenerating
> `docs/audits/README.md` (via `gen_audit_index.py`, another `newline`-omitting writer) flipped
> the working copy from 0 CRLF / 294 LF to **295 CRLF / 0 LF** — a complete flip — yet
> `git diff --numstat` reported **`2 1`**. So the claimed "whole-file commit diff" does **not**
> occur. Residual real harm: a phantom dirty working tree until git next touches the file, plus
> a git warning — precisely the "content-identical phantom dirty-tree entry" failure the
> `.gitattributes` comments already describe from the 2026-06-08 floor pilot. The repo solved
> this class at the `.gitattributes` layer (#282 / W3, 2026-07-13); `codemap/cli.py:69`'s
> `newline="\n"` is now defense-in-depth. **Still worth fixing** (one word; byte-level writers
> such as hash guards do not benefit from git normalization), but it is not the emergency the
> raw reproduction suggested. Related: 5 of 9 writers repo-wide omit `newline="\n"`.

**C2 — MEDIUM · two commit-msg gates fail silently on a git error.** `[reported]`
`check_backlog_commit_msg.py:43-53` and `check_backlog_filing.py:93-102` read
`subprocess.run(...).stdout` and catch only `OSError`. A **non-zero git exit** is not an
exception: `stdout` is `""`, no removed ids are found, and the gate returns 0. The comment at
`check_backlog_commit_msg.py:48-50` explicitly promises *"the skip is never silent."* It is.
`validate_hermetization.py:211-212` does the same read correctly (raises on `returncode != 0`).

**C3 — MEDIUM · 7 reporters document "exit 0 always" and can exit 1.** `[reported]`
`validate_doc_rot.py:254`, `validate_doc_structure.py:337`, `validate_git_backlog.py:125`,
`validate_no_ff.py:129`, `validate_reconciliation.py:308`, `validate_doc_claims.py:242`,
`scan_undeclared_edges.py:302` each carry a docstring saying *"exit 0 always (awareness layer,
never a gate)"* with no top-level exception guard. The template exists and works —
`boundary_report.py:364-372` and `fleet_health.py:486-521` both do it correctly.

**C4 — MEDIUM · `validate_onboarding_rulings.py` says "not a gate" and exits 1 and 2.**
`[reported]` Docstring L106 "advisory read-only"; L110 prints "(advisory — not a gate)"; then
L113 `sys.exit(1)` and L107 `sys.exit(2)`. Either the words or the codes are wrong.

**C5 — MEDIUM · the two hook shims cannot be imported.** `[verified]`
`scripts/codemap_hook.py:16` and `scripts/toc_hook.py:16` call `main()` at module top level with
no `__main__` guard. These are the only two importable modules in `scripts/` that die on import.

**C6 — LOW · exit-code collision for "markers missing".** `[reported]` The same condition gets
**3** (`toc/check.py:37`, `codemap/check.py:41`), **2** (`gen_intake_index.py:158-160`), and
**1** (`gen_doc_counts.py:145-149`) — across families whose docstrings claim to mirror each other
(`gen_methodology_roster.py:154-155` says it "mirrors scripts/toc/check.py semantics"; it has no
code 3).

**C7 — LOW · `toc/` is a self-declared copy of `codemap/`.** `[reported]` `toc/__init__.py:1`
*"mirrors the codemap pattern"*; the hook shims are byte-identical modulo the tool name. Domains
genuinely differ (AST graph vs markdown headers) so `generator.py` divergence is justified — the
`check.py`/`cli.py`/`__init__.py`/shim scaffolding is not. Sharper sub-case: marker constants are
declared **twice per package** (`check.py` *and* `cli.py`), so renaming a marker in one is a
silent divergence in the other. H1 is the concrete cost of this structure.

**C8 — COSMETIC · split severity vocabulary.** `[reported]` `WARN` (14 sites) vs `WARNING`
(10), including the sibling pair `check_backlog_commit_msg.py:51` / `check_backlog_filing.py:105`.

**Verified NON-finding, recorded to prevent re-investigation:** output encoding is uniform and
correct. A reviewer hypothesised the pervasive em-dash would crash on a cp1252 console, tested
it, and **refuted it** — 0 non-cp1252-encodable characters across all 54 files' print sites.

## 5. Dependency direction & coupling

**F1 — CRITICAL · the repo's own cycle detector is structurally blind.** `[verified]`
`scripts/codemap/ast_walker.py:23-27` counts a node only if it is a **directory containing
`__init__.py`**. Direct invocation of `analyze_repo(Path('.'), source_root='scripts')` returns:

```
nodes: ['codemap', 'toc']
edges: []
```

**2 nodes, 0 edges.** All **45** flat `scripts/*.py` modules — including `audit.py` (3082
lines), `fleet_parity.py`, `enforcement_coverage.py` — are invisible. The `[cycle]` marker in
`mermaid_emit.py:26` can never fire on this repo, and `deploy/` is never scanned at all. This is
gated in `.pre-commit-config.yaml:30`. **A gate reporting "no cycles" over an essentially empty
graph is vacuous**, and F2 is the proof.

**Root cause** `[verified]`: neither `scripts/` nor `deploy/` is a Python package — no
`__init__.py`. Only `codemap/`, `toc/`, and `lived_sandbox/` are. Consequently every
cross-module import goes through **runtime `sys.path.insert` mutation** — **17 sites across 15
production files**. That single fact explains both the detector's blindness and why the
dependency graph is invisible to any static tool.

**F2 — CRITICAL · four import cycles, all masked by function-local imports.** `[verified]`
None raises today (both directions are deferred), so this is a latent-structure finding, not a
live crash. But `audit` and `enforcement_coverage` are mutually dependent and neither can be
extracted or reasoned about independently.

```
audit.py:2276            -> enforcement_coverage      (fn-local)
enforcement_coverage.py:487,616,667 -> audit          (fn-local)
gen_handoff.py:266       -> assemble_paste            (fn-local)
assemble_paste.py:102    -> gen_handoff               (fn-local)
   ...plus a third edge: gen_handoff.py:489 subprocesses assemble_paste.py
   ...plus 2 transitive cycles through fleet_parity.py:97,101
```

The stated rationales are *decoupling* / *"sibling CLI; deferred import"* — **not**
cycle-breaking. The cycles are therefore undocumented as cycles.

**F3 — HIGH · `scripts/` ↔ `deploy/` is bidirectional; the two trees are one component.**
`[verified]`

```
deploy -> scripts:  carrier_floor.py:69 (MODULE-LEVEL, via sys.path.insert :66-68)
                    release_lint.py:158,159
scripts -> deploy:  enforcement_coverage.py:331, 749, 760, 918, 1055
```

Chain: `audit → enforcement_coverage → deploy/tool → deploy/carrier_floor →
scripts/generate_floor`. Neither tree can be packaged, vendored, or moved without the other.

**F4 — HIGH · policy reads a private name across a module boundary, with a silent fallback.**
`[reported]` `scripts/enforcement_coverage.py:488` —
`getattr(_audit, "_FRESHNESS_FILES", ["CLAUDE.md"])`. Rename `audit.py:219 _FRESHNESS_FILES`
and coverage silently reports against a **1-file** list instead of 8 — no error, wrong answer.
This is the worst edge in the graph. Adjacent: `deploy/release_lint.py:161` reads
`_audit._CANONICAL_SPINE` (fails loud, so lower severity);
`enforcement_coverage.py:668` uses `getattr(_audit, f"check_{name}", None)` (a renamed check
degrades silently). Also `fleet_parity` reaches into **6 private helpers** across two modules at
7 call sites — now load-bearing for a *blocking* gate, with nothing declaring that contract.

**F5 — HIGH · `enforcement_coverage` has zero GIT env scrub.** `[verified]`
`_run_in:355` is `full = {**os.environ, **(env or {})}` — it **explicitly re-injects the full
environment**, `GIT_DIR` included, then passes `cwd=`. Grep for any scrub token in the module
returns **0**. `deploy/floor_conformance.py:71-77` is identical. Six unscrubbed git sites,
including `git add`/`git commit` at L426-427 and L553-554. Falsifiable: with `GIT_DIR` set,
those stage and commit into the repo named by `GIT_DIR`, not the clone at `cwd`. **This is the
exact [#355] bug class, unfixed in this module.** Honestly bounded: reachable on the `--fire`
CLI path only; the gated `evaluate_static` path performs no git subprocess.

**F6 — HIGH · `consumer_paths()` is broken in a worktree, on two independent axes.**
`[verified — reproduced live]` Run from this worktree:

```
enforcement_coverage.consumer_paths()        fleet_parity.resolve_fleet()  [same registry]
  .dev-knowledge   exists=False                .dev-knowledge  hub        exists=True
  ai-council       exists=False                ai-council      consumer   exists=True
  corp-monorepo    exists=False                corp-monorepo   consumer   exists=True
  corp-ops         exists=False                corp-ops        pre-deploy not walked
  corp-sca-...     exists=False                corp-sca-...    pre-deploy not walked
```

(a) The **hub is reported as a consumer** — `L921` compares against
`deploy_tool.HUB_DIR_NAME`, which is `_HUB_ROOT.name` = `"night-code-audit"` in a worktree,
never `.dev-knowledge`, so the skip never fires. (b) **All five paths resolve under
`.claude/worktrees/` and none exist**, so every repo reports `unavailable`. (c) **No role
model** — `pre-deploy` repos are treated as consumers, so absent enforcement is reported for
repos with no methodology deployed, which is precisely the "flat all-absent map manufactures a
fake gap" failure the module's own docstring warns against at L15-17. Bounded: `consumer_paths`
is CLI-only; the ship gate is unaffected.

**F7 — MEDIUM · repo discovery implemented twice, unequally.** `[verified]` The side-by-side
above is the evidence. `fleet_parity._dev_dir:406-408`'s docstring *names the exact bug the
deploy resolver still has* ("a linked worktree's plain parent would be `.claude/worktrees/`").
The fix was written once and never shared. Shared home should be `fleet_parity`'s resolver.

**F8 — MEDIUM · latent `GIT_DIR` exposure in `boundary_report`.** `[reported]`
`boundary_report.py:271-291` — `_is_hub()` calls `git -C <path> rev-parse --git-common-dir`
twice and compares. Under an inherited `GIT_DIR`, `-C` is overridden, **both calls return the
same value regardless of `path`**, so `_is_hub()` returns `True` for every consumer and the
reporter skips the fleet while printing a clean surface line. Currently latent — no live caller.
**`[#369]` proposes wiring `boundary_headers --check` into pre-commit, which would activate it.**

**F9 — MEDIUM · Tier-2 pinned to a stale manifest.** `[verified]`
`enforcement_coverage.py:757` — `manifest_version: str = "1.0.0"`, never overridden by any
caller. `manifest-v1.0.0.yaml` declares 4 carriers `[global-config, tier1-plugin, precommit,
floor]`; `v1.4.0` declares 6, adding `enforcement-mesh` and `editor-config`. **The Tier-2
surface has never reported the `enforcement-mesh` carrier for any consumer.** Aggravating: the
same module already has `_latest_manifest()` (L803-811) and uses it for Tier-3 — one module runs
two contradictory manifest-version policies. Adjacent ticket `[#239]` covers *extending* Tier-2
breadth; it does **not** cover this defect in the existing surface.

**F10 — LOW · output-format scraping across a process boundary.** `[reported]`
`validate_doc_claims.py:137-147` shells `pytest --collect-only -q` and regexes the summary line.
A pytest reformat silently yields `None` (fails soft, so defensive — but it is an undeclared
dependency on an external tool's output format).

**F11 — LOW · `check_import_edges` is a name false-friend.** `[reported]` `audit.py:2342`
sounds like the Python-import gate; it checks markdown `@import` target existence. Combined
with F1, **the repo has zero enforcement over its Python import graph while two check names
suggest otherwise.**

**F12 — HIGH · `--force` is silently inert for the plugin carrier.** `[verified]`
`tool.py:1012` computes `do_apply = force or item.state.needs_apply` and calls `apply`. But
`carrier_plugin.py:325-327` opens `apply` with `state = self.detect(target)` and returns
`changed=False` when `PRESENT_CORRECT`. So `--force` — documented at `tool.py:1291` as
*"Re-apply carriers even when detect says they are already correct"* — does nothing for this
carrier. **It is the only carrier that calls `self.detect()` inside `apply`** (single grep hit
repo-wide `[verified]`), and it is defeated in precisely the carrier whose `detect` is least
trustworthy, since that one shells out to an external `claude` CLI. `contract.py:11-12`
explicitly assigns detect-then-conditionally-apply to the *tool*, "never the contract's".
Untested: `test_force_reapplies_a_correct_carrier`
(`tests/test_deploy_tool_execute.py:331-333`) exercises `precommit`, not the plugin.

**F13 — HIGH · detect/verify range over different requirement sets, producing a
non-converging state.** `[reported, mechanism verified]` `tool.py:1012` gates `apply` on
`detect`, but `tool.py:1019` runs `verify` **unconditionally** `[verified]`. Two carriers
implement a *larger* requirement in verify than in detect — mesh (`_classify_mesh` 5 conditions
vs `_verify_mesh` those plus a per-file gitignore committability check, `carrier_mesh.py:204`)
and plugin (`_classify_plugin` reads only `plugin list`; `_verify_plugin` additionally requires
`enabledPlugins[id] is True`). A consumer can therefore sit at detect=`PRESENT_CORRECT` → apply
skipped → verify FAILs → `tool.py:1037-1039` aborts the run — and **re-running never
converges**, because apply stays gated on detect. `--force` cannot rescue mesh either
(`_ensure_gitignore` returns `None` when its own entries are present). This is what the D9
invariant was meant to prevent: detect and verify should differ in *implementation*, not in
*requirement set*.

**F14 — MEDIUM · `deploy/` is not a package either, and the test suite pays for it.**
`[verified]` **`deploy/__init__.py` is absent**, yet `deploy/lived_sandbox/__init__.py` exists —
a regular package nested inside a non-package. All five carriers do bare `from contract import
...` and none puts `deploy/` on the path itself, so **every carrier is unimportable standalone**,
depending on an unstated precondition. Repo-wide grep for `from deploy.` / `import deploy`
returns nothing. Consequence: **there is no `conftest.py` anywhere in the repo** `[verified]`
and `pyproject.toml` sets no `pythonpath`, so **30 test files each duplicate their own
`sys.path.insert`** `[verified]` — order-dependent global state, repeated, with `pytest-xdist`
declared in the dependency groups. This is the same root cause as F1: **no package structure →
runtime path mutation → a graph no tool can see.**

**F15 — MEDIUM · four fragile import edges inside `deploy/`.** `[reported]`
(a) `carrier_floor.py:66-67` mutates global `sys.path` at *module import time*, so importing any
carrier rewrites interpreter state for the whole process as a side effect of `tool.py:60`.
(b) `lived_sandbox/arc.py:38-40` reaches past the `tool.py` façade directly into three concrete
carriers — a skip-level dependency. (c) `lived_sandbox/consumer.py:87` imports
`floor_conformance` with **no path guard in that file**; it resolves only because L26/L29
transitively imported modules whose shims ran first — reordering the imports breaks it — then
calls `_fc._run(...)`, a private function across a directory boundary. (d)
`lived_sandbox/observe.py:383-385` has a `sys.path.insert` at the **bottom** of the file, after
every definition, in a module importing nothing from `deploy/`; it guards nothing, and its
comment claims to mirror `spawn.py:30`, which is correctly positioned *before* its import.

**Correct edge, worth stating:** **no `carrier_*.py` imports `tool.py`** `[reported]` — the
orchestrator depends on the carriers and nothing depends back. `lived_sandbox/` is likewise
properly isolated outbound: nothing in `tool.py` or the carriers imports it.

## 6. Dead code

Method: AST symbol table over 1590 production symbols → tokenized reference count across
`.py`/`.md`/`.yaml`/`.json`/`.ps1`/`.sh`, definition site subtracted; then each survivor
hand-checked for dynamic dispatch. **Five click-decorated commands showed zero direct callers
and were correctly excluded** — a naive grep would have reported all five as dead.

**D1 — 4 dead symbols, from 1590.** `[verified — each has exactly one code hit, the definition]`

| Symbol | Location | Evidence |
|---|---|---|
| `_STATUS_EMOJI` | `scripts/audit.py:2458` | **Born dead.** Sibling `_STATUS_LABEL` is read at L2495; this is read nowhere, and `git log -S` shows no read site ever existed. Worse, it has been *maintained while dead* — the JOURNAL records wiring the new `n/a` status into it. |
| `PruneState.needs_prune` | `deploy/contract.py:137` | Zero refs incl. tests. Every would-be caller open-codes it (`carrier_precommit.py:785-788`, `tool.py:465`). |
| `OUTER_MARKERS` | `deploy/lived_sandbox/arc.py:54` | Self-labelled "Back-compat name", zero refs. **Reason expired:** `docs/audits/2026-07-05-overnight-autonomy-run.md:68` records the assumption behind it was proven confounded. |
| `_DIAGRAM_LANGS` | `scripts/coherence_enumerator.py:48` | Zero refs. Sibling `_SHELL_LANGS` *is* read at L223 as an if/else — the else-fallback made this 15-entry set redundant and it was never deleted. |

**Test-only, explicitly NOT dead:** `Oracle.by_id`, `signature_breadth_problems`, `has_fail`,
`enumerate_repo`, `extract_check_floor_hash_script`. These are test-covered API.

**D2 — dead config: 29 unread key declarations.** `[verified]` This is the axis the prompt
flagged, re-established independently here after the `crux_check` premise was found not to
apply (§1c).

Two independent reviewers converged on this, and the second produced a fuller census — every
key below was grepped for `.get("k")`, `["k"]`, and the bare name across `deploy/`, `scripts/`,
`tests/`, `plugins/`, `.claude/`, with **zero readers anywhere including tests**. Lines are
`deploy/manifest-v1.4.0.yaml`:

| Dead key | Declarations | Note |
|---|---|---|
| `components[].artifacts` (+ nested `.path`/`.source`/`.wiring`) | **17** | Nothing ever walks it. Schema block L277-279 documents it as if functional. |
| `carriers[].adr`, `l0_scope.*[].adr` | **12** | No declarative-only marker. |
| `carriers[].description` | 6 | L111,151,165,217,234,328. |
| `components[].engages.scope` | 4 | L511,568,586,610. `oracle.py:83-100` reads only `expect`/`trigger`/`observable`. |
| `carriers[].target.organs` | 1 | L244. |
| `carriers[].target.override_command` | 1 | L247. **Zero hits in any form repo-wide.** |
| `carriers[].target.logs_dir` | 1 | L248. |
| `carriers[].target.source_paths` | 1 | L343. **Born dead** — new in v1.4.0, never read. |
| `carriers[].l0_scope.implemented` | 1 | L121. `tool.py:517-539` iterates only `deferred_deployables` and `enforced_elsewhere`. |

**Highest risk of the set: `components[].artifacts` and `engages.scope`.** They *read as
machine-checked specification* — the artifact blocks name exact consumer paths, the scope fields
state exact firing conditions — but nothing verifies either against reality, so they drift
silently and indefinitely. That is worse than a merely unused key: it is a spec that looks
enforced.

**A trap flagged so nobody "cleans" it** `[reported]`: `required_local_hooks[].language/.files/
.pass_filenames/.always_run` (L200-212) and `prune.expected.hooks[].args` (L488) *look*
test-only under a naive quoted-string grep but are **load-bearing** — read via whole-dict copy
at `carrier_precommit.py:135`, written verbatim at `:407`, byte-compared by the prune oracle at
`:774`. Do not delete these.

**Honestly declared-inert, NOT defects** — recorded so nobody "fixes" them: `carriers[].target.
{organs, override_command, logs_dir}` are dead but L228-229 says so outright ("the carrier
ignores it"), confirmed in code at `carrier_mesh.py:269,274,291`, which take `target: Any` and
never read it `[verified]`. `source_paths` is dead under an explicit `implemented: false`.
**The inverse case is a real defect:** `manifest-v1.4.0.yaml:287` still says `roster` is
"DECLARATIVE ONLY this release" — but that shipped, and `gen_methodology_roster.py:103` reads it
today.

**D3 — unreachable branches: clean.** `[reported]` AST scan of all 78 production files for
post-`return`/`raise`/`exit` statements, constant conditions, and duplicated `if`/`elif`
conditions: **0 findings**.

**D4 — orphaned files: clean.** `[reported]` All 78 production modules have ≥2 references
across code, hook config, manifests, or docs.

**D5 — unused imports: covered, and absent.** `[verified]` `pyproject.toml:49` sets
`extend-select = []`, but ruff's *default* select includes `F`, which is F401/F841. `ruff check
.` passes clean. What the config does **not** select, on production code: `PLR` 99, `RUF` 67,
`C90` 39, `ERA` 22, `SIM` 13, `ARG` 14, `TC` 7, `B` 5. Two notes: **`ERA` is correctly
excluded** — all 22 hits are false positives on this repo's `# rule:` doc→code edge markers.
**`ARG` has real hits** `[verified]` — `carrier_mesh.py:269,274,291` (the code-side proof of D2)
and `audit.py:2847` `cmd_registry(action)`, a `click.Choice` argument the body never reads. Also
`fleet_parity.py:1541` `_eval_stale(..., facts, ...)` — the body never references `facts`
`[verified]`.

## 7. Tech-debt accretion

**T1 — HIGH · the `_git` wrapper is copy-pasted 9 times and the known bug fix reached 1.**
`[verified]` Nine near-identical git subprocess wrappers; **exactly one scrubs the inherited
git environment**:

```
scripts/fleet_parity.py:528              SCRUBS  (env=_scrubbed_git_env())
scripts/validate_no_ff.py:70             no scrub
scripts/safe_remove.py:115               no scrub
scripts/reverse_dep_oracle.py:157        no scrub
scripts/session_end_backpressure.py:128  no scrub
scripts/propose_closures.py:212          no scrub
scripts/gen_handoff.py:153               no scrub
deploy/lived_sandbox/observe.py:212      no scrub
plugins/tier1-lifecycle/scripts/propose_closures.py:241   no scrub
```

And the scrub itself is **verbatim duplicated** between `audit.py:1531-1560` and
`fleet_parity.py:493-522` (identical 15-name tuple, identical derivation). So the repo
diagnosed a real bug, wrote the fix twice, and applied it to 1 of 9 wrapper sites.
`safe_remove.py:113` and `reverse_dep_oracle.py:155` both carry comments saying they copy each
other's pattern — the duplication is acknowledged in-source and never factored out.
**Counter-evidence that the fix is easy:** `block_ff_push.py:66` does
`_git = _vnf._git`, deliberately importing `validate_no_ff`'s wrapper so detector and gate
cannot disagree. The sharing pattern works; it is applied once. **Currently latent** —
cross-repo callers are guarded (`audit.py:1476-1478`) — but the structure is the bug.
**No open ticket mentions `GIT_DIR`, a scrub, or a shared git helper** `[verified]`.

**T2 — MEDIUM · `_atomic_write` duplicated 4×.** `[verified]`
`enforcement_coverage.py:952`, `fleet_parity.py:1614`, `fleet_health.py:163`,
`boundary_report.py:350` — identical logic differing only in tempfile prefix.
`boundary_report.py:351` *documents the copy* ("mirrors fleet_health._atomic_write").

**T3 — MEDIUM · 5 independent frontmatter parsers.** `[reported]`
`gen_claude_rosters.py:61`, `gen_intake_index.py:44`, `seed_runbook.py:50`,
`validate_reconciliation.py:104`, `boundary_report.py:234`.

**T4 — MEDIUM · the portable repo-root resolver is byte-identical in the two deployed organs.**
`[reported]` `canonical_freshness_gate.py:133-145` ≡ `session_end_backpressure.py:102-113` — same
3-tier priority, same timeout, same handler; only docstrings differ. These are the two organs
**deployed into consumer repos**, so a fix to one silently diverges from the other.

**T5 — MEDIUM · hub↔plugin twin drift.** `[verified]` The duplication is **justified** — the
plugin ships to consumer repos with no `scripts/` (ADR-78 carrier doctrine). The question is
per-pair drift:

| Pair | Hub / plugin | Diff lines | Verdict |
|---|---|---:|---|
| `review_closures.py` | 262 / 295 | 37 | **Clean twin.** +33 is the required host-root port. Zero hub logic missing. |
| `propose_closures.py` | 400 / 421 | 45 | **Benign lag.** Plugin lacks `first_parent` (hub L229). Not a live bug — the only `first_parent=True` caller imports the hub copy — but loading the plugin copy with the hub's signature raises `TypeError`. |
| `validate_backlog.py` | 356 / 239 | **147** | **Real silent drift.** Two hub rule-families entirely absent: `serialize-group` (#167) and the `#187` dedup-on-entry WARN — `_SERIALIZE_CLAUSE_RE` hub 3 / plugin 0, `_DUP_TITLE_THRESHOLD` hub 4 / plugin 0. The `[S<n>]` story-id gap is *deliberate and documented both sides*; these two are not. |

Inert today (the plugin copy is used only as a `parse()` library), but it bites the moment the
floor copy is wired as a consumer gate — which is the stated purpose of
`plugins/tier1-lifecycle/tests/test_validate_backlog_floor.py:3`. Direction is permissive
(under-enforces), not wrongly-blocking. **The sync mechanism exists but is scoped too narrowly
to catch either gap** — `tests/test_validate_backlog_twin_parity.py` (#206) enforces byte-identity
for a *declared* symbol set only, and its own docstring notes fixtures are kept "dup-title-free
so the hub-only #187 WARN never fires." It passes 7/7 against a 147-line divergence.

**T6 — TODO graveyard: essentially empty** (see §3). One `TODO` (10 days, ticketed), one
"stopgap" note at `validate_backlog.py:126` (26 days, ticketed #206 — and §T5 confirms the
stopgap's scope is narrower than the drift it guards). **One expired workaround:**
`OUTER_MARKERS` (D1).

**T7 — MEDIUM · stale docstrings that contradict adjacent live code.** `[verified]`
The sharpest is **`deploy/tool.py:1-30`**, which declares the module *"Strictly read-only… the
ASSESS half"* and states at L28-29 that the `--execute` path *"is scaffolded as an explicit
guard here, **never implemented**."* `execute()` is fully implemented at **L964**, writes to the
consumer (L1115), and commits to a hub branch (L1116). A reader trusting the docstring would
believe the module cannot mutate anything. Others: `tests/test_doc_code_edge.py:711` says
*"(count 28)"* three lines above `assert len(ALL_CHECKS) == 31`; `audit.py:1829` and
`ecosystem/doc-code-edge.yaml:34` both still describe an xfail-strict gate deleted a month ago;
`tool.py:342`'s `_APPLY_HINT` claims the mesh apply creates `logs/` while
`carrier_mesh.py:31-33` says the opposite explicitly — per-carrier knowledge duplicated into the
orchestrator, already drifted. Related dead scaffolding: `tool.py:1249-1253` is unreachable from
`execute()` and its message ("land in step 4 of this build") is stale.

**T8 — LOW · two BACKLOG line-citations have rotted.** `[verified]` `BACKLOG.md:342` cites
`audit.py:363` for `discover_repos` (actually **L371**); `BACKLOG.md:343` cites `audit.py:1961`
for the fleet-parity promotion (actually `check_fleet_parity` at **L2170**).

**T9 — brittle cross-file pins.** `[verified]` `len(ALL_CHECKS) == 31` is pinned at **five**
sites — `tests/test_audit.py:2149`, `:2165`, `tests/test_doc_code_edge.py:249`, `:714`, and
`ecosystem/doc-counts.md:14`. Live count is 31; all consistent. Line pins into `audit.py`:
`tests/test_reverse_dep_oracle.py:79` (`== 274`, 0-based) and `:215` (`== 275`, 1-based) against
`class Finding:` at **L275** — correct at HEAD, and broken by any line inserted above L275.

**T10 — HIGH · the precommit carrier's add-side oracle matches by `id` alone, so an edited
hook reads as correct.** `[verified]` `carrier_precommit.py:242-244` (`_classify`) and `:688-697`
(`_verify_satisfied`) both match `required_local_hooks` by **`id` only** — a set comprehension
over ids — while `apply` writes the **full hook dict** (`:407`). Falsifiable and concrete: a
consumer edits a deployed hook's `entry:` from `python .claude/check_floor_hash.py` to `true`;
detect reports `PRESENT_CORRECT`, verify passes, and the deploy tool records a verified version
**while the floor hash-gate is silently disarmed**. The prune leg *in the same file*
byte-compares every hook field (`_entry_matches_expected:758-774` `[verified]`). **Strict on
remove, id-only on add.** Distinct from `[#290]`, which covers the floor carrier's 3-stage arm.

**T11 — MEDIUM · copy-paste between carriers.** `[reported]` `_write_lf`
(`carrier_floor.py:287-290` / `carrier_mesh.py:218-220`); `_load_settings`
(`carrier_floor.py:160-168` / `carrier_mesh.py:113-120`); the settings.json hook-group walker in
**three** copies (`carrier_floor.py:171-180`, `carrier_mesh.py:123-131`,
`lived_sandbox/arc.py:59-69`); LF-normalizing `_read_text` (`carrier_floor.py:152-157` /
`carrier_mesh.py:109-110`); the `yaml.safe_dump(sort_keys=False, ...)` triple
(`carrier_precommit.py:516,621` / `arc.py:294-296`). The `str | None` "changed?" idiom is an
unstated private protocol duplicated across two files.

**T12 — MEDIUM · the lived-sandbox oracle is pinned to manifest v1.2.0 with no override.**
`[reported]` `arc.py:141` `_MANIFEST_REL = "deploy/manifest-v1.2.0.yaml"`; `arc.py:467` and
`consumer.py:228` `load_for_version("1.2.0")`. Neither `run_arc` nor `run_consumer_arc` exposes a
version parameter. v1.4.0 adds two gated hook-stdout components absent from v1.2.0
(`hub-block-ff-push` pre-push, `hub-backlog-id-hook` commit-msg), so a v1.4.0 consumer can be
reported `FULL-COVERAGE` against an 8-component v1.2.0 expectation **while two deployed gated
hooks are never measured**. Last commit touching `lived_sandbox/` is 2026-07-06; v1.4.0 landed
2026-07-20. This is the predictable cost of an unwired harness. Same family, same file:
`arc.py:471-472` **ignores `disable_precommit_hook`'s return value** while the identical call is
checked eleven lines earlier at `:265` — so a mistyped `--leg-e` hook id disables nothing, the
arc runs green, and `arc-silent.jsonl` records a green arc at exit 0, inverting the
arc-green/arc-silent discrimination that is the subpackage's stated deliverable.

**T13 — MEDIUM · a cleanup hole that lands on the repo's own "No leftovers" invariant.**
`[reported]` `spawn.py:237-238`'s `finally` calls `teardown` → `floor_conformance.py:303-319`,
whose `_onerror` only clears the read-only bit — no retry, no locked-file handling. On an arc
timeout (`arc.py:460`) `subprocess.run` kills only the direct `claude` process; hook
grandchildren survive holding the clone as cwd; `rmtree` raises `PermissionError` **from inside
the `finally`, replacing the original `SandboxError`**. Both halves fail at once: a
multi-hundred-MB clone survives in `%TEMP%`, and the operator sees an rmtree error instead of
"child timed out." Relevant because `CLAUDE.md` rule 9 requires a scratch-creating process to
remove *and verify removal of* everything it created, even on abort. Adjacent: **missing
subprocess timeouts** at `observe.py:212-214`, `floor_conformance.py:71-77` (used for `git
clone`), and `oracle.py:168-169` — while `spawn.py:189-196` does it correctly.

## 8. Test-suite notes (bounded scope)

100 test files / 24,286 LOC against 25,636 production LOC (~0.95:1).

- **Zero `xfail` markers exist anywhere** `[reported]` — the `coverage_scope` xfail-strict gate
  was removed 2026-06-22 (#194 Phase B). No silent-XPASS risk. All 25 skip sites carry reasons.
- **Three env-gated suites have no automated execution path** `[verified for RUN_E2E]`.
  `RUN_E2E` (`tests/test_e2e_consumer_lifecycle.py:33`) is set **nowhere in the repo**, and
  **there is no `.github/` — no CI at all**. Same for `LIVED_SANDBOX_LIVE`. Stated fairly:
  these are *deliberate* opt-in markers, correctly documented as such. The finding is not
  "dead tests" — it is that with no CI, the 11-stage consumer-lifecycle gauntlet only ever runs
  if a human types the env var, so its coverage is theoretical rather than continuous.
- **Worktree-conditional dead coverage** `[reported]` — `tests/test_reverse_dep_oracle.py:36`
  gates on `node_modules/pyright`, which is gitignored and therefore absent from **every linked
  worktree**. The #193 closure-metric test is dead in exactly the parallel/night sessions most
  likely to touch `audit.py` — including this one.
- **One degenerate test** `[verified]` — `tests/test_generate_floor.py:50-52`:
  `floor = gf.render_floor()` is hoisted out, so `assert gf.floor_sha256(floor) ==
  gf.floor_sha256(floor)` hashes the **same string twice**. It asserts sha256 is a pure
  function, which cannot fail. Every sibling `test_render_is_deterministic` correctly
  re-invokes the renderer inside the comparison. Note for `[#278]`: its embedded census note
  claims the theatricality pre-scan was clean fleet-wide, but the pattern set omitted
  **self-comparison** — precisely this shape. That note should be narrowed, not left standing.

## 9. Prioritised shortlist — the handful that actually matter

Ordered by (blast radius × likelihood × cheapness of fix).

1. **The cycle detector is vacuous** (§5 F1) — CRITICAL and the **biggest single lever**.
   Making `ast_walker.analyze_repo` treat flat modules as nodes converts an already-gated,
   already-wired check into a real one, and would immediately surface F2's four cycles and F3's
   cross-boundary edges *with no new machinery*. Everything else in §5 is downstream of this.
   Today the repo has **zero** enforcement over its own Python import graph.
2. **`enforcement_coverage` GIT scrub + worktree resolution** (§5 F5, F6) — two HIGHs in one
   module, one **reproduced live**, both the already-diagnosed [#355] class. F6's fix is to
   *delete* the duplicate resolver and call `fleet_parity`'s (§5 F7) — a subtraction.
3. **One shared git helper** (§7 T1) — collapses 9 wrappers and 2 copies of the scrub into one
   home, and structurally prevents the next caller from picking an unscrubbed one. This is the
   systemic version of item 2; doing 2 without 3 leaves the trap armed.
4. **`_FRESHNESS_FILES` silent fallback** (§5 F4) — a one-line change
   (`getattr(..., default)` → explicit import or hard failure) that removes a *silently wrong
   answer*. Silent-wrong outranks loud-broken.
5. **The three silently-wrong deploy oracles** (§7 T10, §5 F12, F13) — grouped because they
   share one root: *the `Carrier` contract is designed but not enforced*. T10 (id-only hook
   match → a disarmed floor gate reads as verified) is the most consequential single defect in
   the report, because the failure mode is **a gate that reports healthy while disabled**. F12
   (`--force` inert for the plugin) and F13 (detect/verify requirement mismatch → a state that
   never converges) are the same class. Fix shape is one change: state in `Carrier` that detect
   and verify must range over the *same* requirement set and that `apply` may not call
   `self.detect()`.
6. **`validate_backlog` twin drift** (§7 T5) — 147 lines, two undocumented rule-family gaps,
   and the guarding test passes 7/7 against them. Inert now; becomes a real consumer-gate defect
   the moment the floor copy is wired. Decide *deliberately*: propagate, or document as
   intentional the way the `[S<n>]` gap already is.
7. **Dead config: 44 unread key declarations** (§6 D2) — cheap, and the manifest already has an
   honest convention for inert keys. Prioritise `artifacts` (17×) and `engages.scope` (4×),
   which *read as machine-checked spec* but are verified by nothing.
8. **Stale docstrings that invert the truth** (§7 T7) — `deploy/tool.py:1-30` says the module is
   "strictly read-only" and `--execute` is "never implemented"; it writes to consumers and
   commits to branches. Cheap to fix, and actively misleading to the next reader.
9. **`toc/cli.py:50` + the other 4 `newline`-omitting writers** (§4 H1) — one-word fix each.
   Ranked here rather than first **after the in-audit severity correction**: `.gitattributes`
   already absorbs most of the harm, so this is hygiene plus byte-level-writer safety, not an
   emergency. It was the report's initial #1 and the correction is recorded in §4 rather than
   quietly re-ranked.
10. **The 4 dead symbols + rotted line citations** (§6 D1, §7 T8) — trivial cleanups.
    `_STATUS_EMOJI` in particular has been *maintained while dead* for two months.

**Deliberately NOT in the shortlist:** splitting `audit.py`. It is the largest file in the repo
and the analysis says its size is legitimate. The only extraction worth doing there is the
~190-line ADR-84 writer (§2), and that is a tidiness argument, not a defect.

**Sequencing note.** Items **2 and 3** touch the same code — do **3** (the shared git helper)
first, and 2 collapses into a call-site change; doing 2 without 3 leaves the trap armed for the
next caller. **Item 1 belongs before 2 and 3**: it is the organ that *would have caught them*,
and fixing it first means the repo detects the next instance of this class itself instead of
waiting for another audit. Items **4, 6, 7, 8, 9, 10** are independent and can go in any order.
Item **5** is one contract change plus three call-site corrections and does not depend on
anything else here.

**One structural observation across items 1, 3 and 5.** Each is the same shape: *a mechanism
that was designed correctly, built once, and then not enforced* — the cycle detector that
cannot see the graph, the git scrub applied to 1 of 9 sites, the `Carrier` contract whose
invariants no test asserts. The recurring failure in this codebase is not bad design and not
missing tests; **it is designed invariants with no organ asserting them.** That is worth naming
because it suggests the durable fix is usually "make the existing gate real", not "write a new
gate" — which is also the cheapest kind of fix available here.

## 10. Coverage gaps in this audit — stated, not hidden

- **Gap closed during writing.** The `deploy/` reviewer returned after the first draft; its
  findings are folded in (§2 both verdicts changed from provisional-FINE to **SPLIT**; §5 F12–F15;
  §6 D2 census expanded; §7 T10–T13). All seven lanes are represented. The revision is recorded
  rather than silently absorbed.
- **The 14 unverdicted files in the 300–499 band** and all 52 files under 300 lines were not
  individually reviewed for decomposition. No size-driven problem was visible, but absence of
  evidence is recorded as such.
- **`[reported]`-stamped findings were not independently reproduced.** They carry cited
  locations and should be spot-checked before ticketing.

## 11. Logged-rejects — opinions without a falsifiable location

Per §0 these do **not** become tickets. Recorded so they are not re-raised as new insights.

| Rejected claim | Reason |
|---|---|
| "`audit.py` is too big at 3082 lines and should be split." | Size alone is not a defect. It is a registry of 31 uniform, independent checks; no natural seam except the ~190-line writer. Splitting it would damage the runtime-derived registry (§3). |
| "The carriers are 5 files sharing a naming prefix, not a real abstraction." | **Refuted by evidence** — `contract.py:159` is a true ABC with 5/5 structural conformance (§3). *The follow-on question was productive though:* the interface is uniform in signature but not in behaviour, which is where F12/F13/T10 came from. Refuting the coarse claim surfaced the precise one. |
| "`--force` doesn't work." (as first phrased, with no location) | Would have been a logged-reject. It became a ticket-grade finding only once located at `carrier_plugin.py:325-327` with the `tool.py:1012` chain and the untested `tests/test_deploy_tool_execute.py:331-333` — which is exactly the §0 test working as intended. |
| "Em-dashes in print output will crash on a cp1252 console." | **Refuted by test** — 0 non-cp1252-encodable characters across all print sites (§4). |
| "The codebase has unused imports / lint debt." | **Refuted** — `ruff check .` passes clean (§6 D5). The real finding is narrower: rule *selection* gaps. |
| "The `scripts/`↔`plugins/` twins are stale copy-paste that should be de-duplicated." | Too coarse to action. The duplication is **required** (the plugin ships where `scripts/` does not exist). Only the specific `validate_backlog` drift is a defect (§7 T5). |
| "There is a TODO graveyard." | **Refuted** — one TODO, ticketed, 10 days old (§3). |
| "`deploy/` is dead code / unused." | **Refuted** — all 78 production modules have ≥2 references (§6 D4). |

---

**Contract compliance.** Read-only review. No code file was modified. No BACKLOG ticket was
filed and no ticket id was allocated — every finding above is a proposal for operator triage.
The two live reproductions (§4 H1, §5 F6) were executed against scratchpad copies and
in-process calls; the repo tree was verified clean immediately after each. The single
non-report file in this commit is the **generated** `docs/audits/README.md`, regenerated by
`python scripts/gen_audit_index.py --write` because the `audit-index-freshness` pre-commit gate
fires on any `docs/audits/*.md` addition and would otherwise block this commit. That is a
mechanically-required lockstep regeneration of a generated index, not hand-authored content.
