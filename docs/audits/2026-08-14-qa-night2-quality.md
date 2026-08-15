# Night-2 lane C — code-quality scan (DRAFT), 2026-08-14

- **Class:** qa (ADR-101 enum) · **Date:** 2026-08-14 · **Slug:** `night2-quality`
- **Status:** **DRAFT — proposals only.** Nothing here is a decision, a ruling, or a closure. No BACKLOG row is opened, closed or amended by this document.
- **Base:** `origin/main` = **`7bbb0674`**; local `HEAD` = the same SHA, working tree clean at branch time. Branch `claude/night2-quality-audit-8a3ixh` (the session's designated lane branch; the brief's shorthand was `claude/night2-quality`).
- **Lane posture:** READ-ONLY. The only writes are this file and the mechanically-regenerated `docs/audits/README.md` index that the `audit-index-freshness` gate requires of any `docs/audits/` ADD — the same carve-out the 2026-08-12 night-1 cloud lane took and recorded.
- **Environment:** Python 3.11.15, ruff 0.15.8 (system) **and** ruff 0.15.5 (the pinned rev, fetched ephemerally — see §1). `uv` present at 0.8.17, which does **not** satisfy `[tool.uv] required-version = "==0.11.19"`, so `uv sync --locked` was unavailable and the audit's own tooling deps were installed with plain `pip` into the container. That is a container fact, not a repo defect.
- **PARTIAL protocol:** absent inputs are named at the point of use and the item is marked UNVERIFIABLE; work continues past them.

## Measurement provenance (M / I)

Every figure below is **M** — measured this session against `7bbb0674` — except where a line says otherwise. Two items are explicitly **UNVERIFIABLE** and say so with the reason (radon in §2, mutation results in §4). No figure in this document is inherited from another artifact.

---

## Findings summary

```
severity   count   ids
HIGH           0   —
MEDIUM         3   M-1, M-2, M-3
LOW            7   L-1 .. L-7
total         10
```

Three of the ten (M-2, M-3, L-5) are **derivation** findings rather than code defects: they say a metric the telemetry v1 EMIT lane will want to compute cannot be computed the obvious way without being wrong. They are the ones worth reading first if this scan feeds that lane.

---

# §1 · ruff — full output, classified

**Verdict: CLEAN. Zero findings against the landed spec.**

The landed spec is `[tool.ruff.lint] extend-select = []` (pyproject.toml), i.e. ruff's default rule set (`E4`, `E7`, `E9`, `F`) at `line-length = 120`, `target-version = "py311"`, `required-version = ">=0.15.5"`.

```
ruff check .                        -> All checks passed!   (exit 0)   ruff 0.15.8
uvx --from ruff==0.15.5 ruff check . -> All checks passed!   (exit 0)   ruff 0.15.5 (pinned rev)
```

**Non-vacuity established** (CLAUDE.md §10 names "running validators with no args" as a repo anti-pattern). `ruff check --show-files .` enumerates **242 files**. Every one of the **233** tracked `*.py` paths is in that set — verified by set-difference against `git ls-files '*.py'`, which is empty. The extra 9 are untracked/generated files in the container. So the pass covers the whole Python surface, not a filtered subset.

**The version question is closed, not caveated.** The container ships ruff 0.15.8 while the repo pins `ruff==0.15.5` (dev group) and the pre-commit rev is `v0.15.5`. Rather than reason about whether a later ruff's defaults are a superset, the pinned version was fetched and run: it is also clean. Both verdicts agree, so no version caveat attaches to this section.

### L-1 (LOW) · 117 dead `# noqa: E402` directives

Not a spec violation — `RUF100` is not in the landed selection, so nothing today reports these and no gate is failing. It is recorded because it is measurable residue, and because it is the kind of thing that quietly inverts: a dead suppression is indistinguishable from a live one at a glance, so a *real* E402 arriving later at one of these lines would be pre-suppressed and invisible.

Measured by adding one rule to the landed config (`ruff check --extend-select RUF100 .`): **170 hits**, which ruff itself splits into two categories that mean different things.

```
53   (non-enabled: ...)   directive names a rule outside the landed selection
                          (S603, S607, BLE001, PLC0415, ANN001 ...)
                          -> DEFENSIVE, not dead. No action proposed.
117  (unused: E402)       directive names an ENABLED rule that did not fire
                          -> DEAD. This is L-1.
```

The 117 dead ones split again, by *why* they cannot fire:

```
102  module-level import under a sys.path preamble
      e.g. scripts/block_unanchored_push.py:55-56
           scripts/boundary_headers.py:58
           scripts/codemap_hook.py:14
 15  function-local (lazy) import
      e.g. scripts/enforcement_coverage.py:331, 566, 569, 695, 1016
           deploy/release_lint.py:158-159
```

The 102 exist because **ruff's E402 deliberately allows a `sys.path` modification before imports**. That was not assumed — it was tested in isolation:

```
probe/a.py   docstring, imports, sys.path.insert(...), then `import os`   -> E402 does NOT fire
probe/b.py   docstring, import sys, `x = 1`, then `import os`            -> E402 fires
             (ruff check --isolated --select E402)
```

So the preamble is still present (`scripts/block_unanchored_push.py:53`) and correct; the noqa beside it is simply inert under ruff. flake8's E402 has no such allowance, which is the most likely origin — that origin is **inferred, not verified**, and nothing below depends on it.

The 15 are a different thing: E402 is defined over *module-level* imports, so it can never apply to an import inside a function. Those directives were never valid. Where the repo wants to suppress a lazy import it already uses the correct code — `# noqa: PLC0415` appears 9 times.

**Proposal (P3, mechanical):** `ruff check --extend-select RUF100 --fix .` removes exactly the 117 and leaves the 53 defensive ones untouched. Worth pairing with a decision on whether `RUF100` joins the landed selection permanently — without that, the residue simply regrows. Adopting a rule is a Tier-S/Tier-L question under ADR-112 and is **not** proposed here.

### Recorded so it is not mistaken for drift

`ruff format --check .` reports **200 of 233 files would be reformatted**. This is **not** a finding. The landed spec gates `ruff check` only — the formatter appears in no pre-commit hook and no manifest roster. The number is recorded solely so a future reader who runs `ruff format` does not read it as regression.

### Informational — rule-set headroom

`ruff check --select ALL .` reports **19,320** across the tree (top contributors: `S101` assert 5300, `ANN001` 2468, `ANN201` 2364, `D103` 1701). This is context for what "clean" currently means, **not** a proposal: `--select ALL` includes rules that are actively wrong for this repo (`S101` fires on every `assert` in a 2,897-test suite). No rule adoption is proposed by this document.

---

# §2 · Complexity hotspots in `scripts/`

### UNVERIFIABLE — radon

`radon` is **not installed** (`ModuleNotFoundError: No module named 'radon'`) and the brief forbids installing it. **No radon cyclomatic-complexity grade (A–F) is reported, and none should be inferred from this section.** Per the brief, the ranking below uses the line-count + function-count proxy.

A second column — an `ast`-derived branch count — is reported alongside it because the brief permits a stdlib-derivable metric and the branch count discriminates far better than line count alone. **It is my own walk, not McCabe and not radon-calibrated**, so it must not be compared against radon's A–F bands. The rule is stated so the number is reproducible: start at 1, then `+1` for each `If / For / AsyncFor / While / ExceptHandler / With / AsyncWith / Assert / IfExp / Match / match_case`, `+1` per comprehension and per comprehension `if`, and `+(n-1)` for a boolean operator with `n` operands.

Docstring lines are excluded from the `code` column. This repo documents extremely densely — some functions are majority prose — and a raw span would rank documentation, not logic.

**Population:** 959 functions across 71 modules (75 `scripts/**/*.py` files parsed; 4 contain no function definitions — `codemap/__init__.py`, `codemap_hook.py`, `toc/__init__.py`, `toc_hook.py`). Total 29,454 LOC.

```
distribution      median    mean    p90    p99    max
code LOC              10    16.1     36     96    210
branches               4     5.6     11     23     88
nested defs            0     0.0      0      1      2
```

### Top 10 functions — ranked by the mandated proxy (code LOC), with locators

```
 #  locator                              function                        code  span  nest  branches
 1  scripts/fleet_parity.py:1131         _eval_row                        210   210     0        35
 2  scripts/fleet_analytics.py:748       build_digest                     205   206     1        23
 3  scripts/fleet_parity.py:595          collect_facts                    199   201     0        88
 4  scripts/gen_task_tree.py:750         _scan_source                     164   172     0        38
 5  scripts/fleet_parity.py:267          load_manifest                    156   159     0        56
 6  scripts/audit.py:4731                _commit_routine_outputs          120   138     0        19
 7  scripts/preflight_contract.py:297    verify                           101   102     2        23
 8  scripts/gen_task_tree.py:546         _cmd_emit_source                  99   112     0        23
 9  scripts/audit.py:4131                check_review_artifact_coverage    98   153     0        35
10  scripts/gen_handoff.py:705           generate                          96   129     0        15
```

### The same population ranked by branches — a different top of the list

```
 #  locator                              function            branches  code
 1  scripts/fleet_parity.py:595          collect_facts             88   199
 2  scripts/fleet_parity.py:267          load_manifest             56   156
 3  scripts/gen_task_tree.py:750         _scan_source              38   164
 4  scripts/fleet_parity.py:1131         _eval_row                 35   210
 5  scripts/audit.py:4131                check_review_artifact_cov 35    98
 6  scripts/fleet_parity.py:811          _probe_dep                28    58
 7  scripts/verify_handoff_probes.py:618 main                      27    63
 8  scripts/audit.py:4535                generate_report           27    53
 9  scripts/audit.py:2901                check_routine_consumers   24    64
10  scripts/fleet_analytics.py:748       build_digest              23   205
```

Both rankings are given because they disagree, and the disagreement is the useful part: `build_digest` is the 2nd-longest function but sits at the p99 boundary for branching (23), i.e. it is long and *straight*. `_probe_dep` is 58 lines with 28 branches, i.e. short and dense. Length alone would have missed it.

### M-1 (MEDIUM) · `fleet_parity.collect_facts` is the single branch outlier in `scripts/`

`scripts/fleet_parity.py:595` — **88 branches**, against a population p99 of 23 and a median of 4. That is 3.8× the 99th percentile and 22× the median; the next-densest function in the repo is 56.

**Verified as real logic, not a metric artifact.** The node census inside the function: 30 `If`, 10 `IfExp` (ternaries), 17 boolean operands, 15 comprehensions, 5 `For`, 2 `ExceptHandler`, 1 `Assert`. The shape is a long procedural fact-collector doing inline conditional coercion at nearly every step (`sorted(...) if rc_ls == 0 else []`, `x.get(...) if isinstance(...) else ...`).

Its own docstring names the property that makes it awkward to split: *"One deterministic facts snapshot per walked repo (FR-3): every probe runs here; `verdicts()` is pure over the result."* Concentrating impurity in one function so the verdict layer stays pure is a deliberate, defensible design — so this is **not** proposed as a defect to fix.

**Proposal (P3):** extract the per-surface probes (git, pre-commit, settings/plugins, deploy) into named private helpers returning their own sub-dicts, leaving `collect_facts` as the assembler. This preserves the one-snapshot contract exactly — the function still runs every probe and still returns one dict — while making each probe testable in isolation. Cost is real and the row is not obviously worth opening; recorded as a candidate, not a recommendation.

### L-2 (LOW) · `fleet_parity._eval_row` — the longest function in `scripts/`, with no docstring

`scripts/fleet_parity.py:1131` — 210 lines, **0 docstring lines**. It is the longest function in the tree and the only member of the top 5 with no docstring at all; it takes 8 parameters and returns `None`, mutating `ev` in place. In a repo whose median function is 10 code lines and which documents as heavily as this one does, a 210-line undocumented in-place mutator is the outlier worth naming. **Proposal (P3):** a docstring stating what it mutates on `ev` and under what conditions it returns early. No behaviour change.

### L-3 (LOW) · `fleet_parity.py` concentration

`scripts/fleet_parity.py` holds the **top two** branch-densest functions in `scripts/` and 4 of the top 10 by either ranking. Module totals:

```
file                              LOC   fns   sum(branches)   max(branches)
scripts/audit.py                 5243   120             927              35
scripts/fleet_parity.py          2049    50             504              88
scripts/fleet_analytics.py       1263    40             237              23
scripts/gen_task_tree.py         1215    38             229              38
scripts/enforcement_coverage.py  1180    54             257              14
```

`audit.py` is much larger in absolute terms but flatter: 120 functions, max branch count 35, mean ~7.7. `fleet_parity.py` carries 55% of `audit.py`'s branch mass in 39% of the lines, in half the functions. Recorded as an observation about where complexity is concentrated; no action proposed.

---

# §3 · The audit checks — organ-usage prep for the telemetry v1 EMIT lane

**Count re-derived as instructed:** `python scripts/audit.py checks` → **43 registered checks** (ALL_CHECKS — run by `health` and `run`). The table below is built from `scripts/audit.py`'s AST (the `ALL_CHECKS` list at `scripts/audit.py:4345`), so it cannot drift from what actually runs.

**Column predicates, stated so each is checkable:**

- `lines` — the function's full source span, and `code` = span minus docstring lines.
- `has-tests` — **yes** iff at least one test function under `tests/` exercises the check. Derivation and its two blind spots are M-2 below; the column is reported after manual reconciliation, not raw.
- `tests` — count of test functions whose body calls `check_<name>` (directly, or via a module-local helper followed one level). This is the *raw* predicate; the two zeros it produces are false and are corrected in M-2.
- `last-touched` — `git log -L <start>,<end>:scripts/audit.py -1`, i.e. the last commit touching **any** line in the function's span. It measures *any* edit — a cross-cutting signature refactor counts — not a semantic change. See M-3 before reusing it.

```
 #  check                          line  lines  code  has-tests  tests  last-touched
 1  vision_md                       578     23    22  yes            5  2026-06-03
 2  adr38_baseline                  603     27    13  yes            7  2026-06-03
 3  claude_md                       632      9     8  yes            3  2026-06-03
 4  dot_prefix_discipline           643     22    17  yes            4  2026-06-03
 5  canonical_md_visibility         667     27    20  yes            4  2026-06-03
 6  workspace_settings              696     35    30  yes            5  2026-06-03
 7  handoff_bundle_structure        769     75    54  yes           11  2026-08-04
 8  canonical_freshness             855     42    15  yes           13  2026-07-03
 9  no_sibling_orphans              988     48    24  yes           11  2026-08-01
10  stale_worktrees                1221     88    41  yes           17  2026-08-07
11  canonical_structure            1351     25    15  yes            5  2026-06-03
12  handoff_version_stamp          1382     47    39  yes            7  2026-08-04
13  amendment_coherence            1485     74    55  yes            7  2026-06-10
14  floor_integrity                1565     58    40  yes            6  2026-08-04
15  hooks_armed                    1625     54    36  yes            5  2026-08-04
16  git_backlog_drift              1682     36    23  yes            6  2026-08-04
17  doc_claims                     1721     36    23  yes            8  2026-08-04
18  doc_rot                        1760     35    18  yes            6  2026-08-04
19  undeclared_edges               1797     44    21  yes            6  2026-08-04
20  doc_structure                  1844     35    17  yes            6  2026-08-04
21  no_ff_merges                   1882     36    19  yes            6  2026-08-04
22  handoff_probes                 2065     90    68  yes           21  2026-08-04
23  reconciled_versions            2158     48    26  yes            8  2026-08-04
24  doc_code_edge                  2305     72    52  yes            9  2026-08-04
25  residual_completeness          2379     41    15  yes            3  2026-07-19
26  safe_removal                   2422     50    27  yes            2  2026-06-26
27  doc_code_coverage_drift        2516     35    24  yes            3  2026-08-04
28  fleet_parity                   2576     33    18  yes            2  2026-08-04
29  deployed_methodology_version   2611     43    26  yes            7  2026-08-04
30  enforcement_coverage           2656     37    20  yes            2  2026-08-04
31  import_edges                   2781     49    41  yes            9  2026-08-04
32  routine_consumers              2901     88    64  yes           26  2026-08-04
33  silent_rule_ratchet            3228     53    29  yes            4  2026-08-04
34  task_tree_coherence            3305     71    45  yes            8  2026-08-04
35  intake_tree_coherence          3378     57    29  yes            3  2026-08-04
36  boot_byte_budget               3438     36    18  yes            4  2026-08-04
37  fleet_audit_replication        3503     56    40  yes            6  2026-08-04
38  membership_agreement           3793     63    48  yes           16  2026-08-04
39  journal_spine_anchor           3859     94    60  yes           12  2026-08-14
40  journal_day_letters            3970     37    28  yes            3  2026-08-14
41  preflight_backlog_ids          4009     70    42  yes            4  2026-08-04
42  review_artifact_coverage       4131    153    98  yes          19*  2026-08-05
43  landing_predicate              4286     57    37  yes           2*  2026-08-13

* corrected by hand — the automated predicate returned 0 for both. See M-2.
```

**Aggregates:** 43 checks · 2,209 total span lines · median span 47 · `has-tests` **43 / 43 yes, 0 no**.

### M-2 (MEDIUM) · `has-tests` cannot be derived by a static call-graph predicate — 2 of 43 are false negatives

This is the finding most directly load-bearing for the telemetry v1 EMIT lane, because "is this organ tested?" is exactly the sort of column such a lane would compute automatically.

A reasonable static predicate — *a test function that calls `check_<name>`, following module-local helpers one level* — reports **2 of 43 as having zero tests**: `check_review_artifact_coverage` and `check_landing_predicate`. **Both are wrong.** Each is defeated by a different real pattern already in this suite:

**1. Dynamic lookup.** `tests/test_review_artifact_coverage.py` is a 19-test module dedicated to that check. It never names the function in a call position — it goes through a helper:

```
tests/test_review_artifact_coverage.py:45
    fn = getattr(aud, "check_review_artifact_coverage", None)
    assert fn is not None, ("... the [#480] advisory review-artifact coverage leg
                            is unbuilt (this is the RED)")
```

The indirection is deliberate — it makes the suite fail with a readable assertion rather than an `AttributeError` while the leg was unbuilt. Good practice that happens to be invisible to a call-graph walk.

**2. Registry injection.** `check_landing_predicate` is exercised end-to-end, but through the registry rather than by name:

```
tests/test_audit.py:1746, 1776
    monkeypatch.setattr(aud, "ALL_CHECKS", [aud.check_landing_predicate])
    ...
    blocked = CliRunner().invoke(aud.cmd_health)
    assert blocked.exit_code == 1 and "DEGRADED" in blocked.output
```

The check appears as an attribute *reference*, never a call — the call happens inside `cmd_health`. There is also a dedicated `tests/test_validate_landing_predicate.py` for the underlying validator.

**Proposal (P3):** if the EMIT lane derives a per-organ test-coverage signal, it must either (a) handle both patterns explicitly — `getattr(mod, "<name>")` with a literal string, and attribute references inside `monkeypatch.setattr(..., ALL_CHECKS, [...])` — or (b) emit `unknown` rather than `0` when the only evidence is a non-call reference. Emitting `0` here would report two well-tested organs as untested, which is worse than emitting nothing: it manufactures a gap that would then get "fixed".

### M-3 (MEDIUM) · `last-touched` is unreliable from a cloud checkout — this session hit it

**This clone arrived shallow.** `git rev-parse --is-shallow-repository` → `true`; `.git/shallow` present; **318 commits**, **21 grafted root commits**, earliest date 2026-08-02.

Under that horizon the `last-touched` column was measured first and was **near-useless**: 40 of 43 checks reported the *same* date, 2026-08-09, because `git log -L` cannot see past a graft and attributes the whole function to the boundary commit that appears to have created the file. (`4bef950` presents as a root commit adding all 5,072 lines of `audit.py` and every other file in the repo.)

`git fetch --unshallow origin` was run — **5,043 commits**, not shallow — and the column was re-derived. The real distribution:

```
2026-06-03   7      2026-08-01   1      2026-08-07   1
2026-06-10   1      2026-08-04  26      2026-08-13   1
2026-06-26   1      2026-08-05   1      2026-08-14   2
2026-07-03   1
2026-07-19   1
```

Range 2026-06-03 → 2026-08-14. **The 26-check cluster at 2026-08-04 was checked and is genuine**, not a second artifact: `f020e0b9` ("[#465] leg 4 — an inert check is now detectable, and the first one is retired", +182/−73) and `4edbd7fe` (+95/−56) were real cross-cutting edits across many check functions that day.

**This is a new instance of a class the repo already knows.** `.github/workflows/report-only-wall.yml:80` carries `fetch-depth: 0` with the note that *"a shallow clone makes the graft root look like it created whole files, so `canonical_freshness` returns 5 false FAILs, `no_ff_merges` false-WARNs on a truncated-parent merge, and `journal_spine_anchor` raises a FAIL-class `AnchorError`."* The CI wall is guarded. What is unguarded is the derivation path: any history-derived metric computed inside a cloud session — including anything the telemetry EMIT lane computes — has no such guard, and the failure is silent and plausible-looking rather than loud.

Worth noting the contrast: the 2026-08-12 night-1 cloud lane explicitly recorded *"This clone is NOT shallow"*. So cloud sessions differ from each other, and the shallowness cannot be assumed either way from a prior lane's finding.

**Proposal (P2, the highest-priority proposal in this document):** any organ deriving a git-history metric should assert `git rev-parse --is-shallow-repository == false` and **refuse to emit** rather than emit a truncated figure. A shallow clone does not produce an obviously-broken number — it produces a wrong number that looks fine, which is the failure mode the repo's own `silent_rule` vocabulary exists for.

### L-4 (LOW) · `check_review_artifact_coverage` is the largest check by a wide margin

`scripts/audit.py:4131` — 153-line span / 98 code lines, against a median check span of 47. It is also 35 branches (5th-densest function in `scripts/`). Its 19 dedicated tests are the suite's largest per-check block, so this is **not** a coverage concern — recorded only as the size outlier in the registry. No action proposed.

### L-5 (LOW) · the `43` count is pinned at five sites across three files

```
tests/test_audit.py:2207              assert len(aud.ALL_CHECKS) == 43
tests/test_audit.py:2223              assert len(aud.ALL_CHECKS) == 43
tests/test_doc_code_edge.py:248       assert len(aud.ALL_CHECKS) == 43
tests/test_doc_code_edge.py:713       assert len(aud.ALL_CHECKS) == 43
tests/test_writer_integrity.py:185    assert len(aud.ALL_CHECKS) == 43
```

Three of these carry the *same* ~1,900-character inline history comment, duplicated verbatim (`tests/test_audit.py:2207`, `tests/test_doc_code_edge.py:248`, `tests/test_doc_code_edge.py:713`). `tests/test_audit.py:2223` already points at `test_all_checks_count_is_pinned` in `tests/test_writer_integrity.py` as the canonical home for the full history — so the intended single-source already exists and three sites have not adopted it.

Adding a check today means editing five assertions, three of which also want a prose-history append. That is a mechanical cost on every registry change, and duplicated prose is the drift mode this repo names explicitly (CLAUDE.md §5 rule 6). **Proposal (P3):** keep the pinned count in `test_writer_integrity.py` and have the other four reference it, replacing the three duplicated histories with the existing pointer. Note the count is deliberately pinned — the pin is the point, and no change to *that* is proposed.

---

# §4 · mutmut — recorded state only

**No mutation run was performed.** Per the brief this section reports existing cached results and configuration state only.

### Cached results: none exist locally

Searched the tree for `.mutmut-cache`, `mutants/`, `.mutmut*`, `mutmut-results*` (excluding `.git/`): **no artifacts found**. `mutmut` is also **not importable** in this container.

### The fork/Windows caveat, as recorded in-repo

`pyproject.toml` `[tool.mutmut]` states it verbatim: mutmut requires `fork()`; upstream requires WSL on Windows; this repo is Windows-developed, so the pilot **cannot run on the operator's host** and is hosted by the `[#501]` report-only wall's `mutation-pilot` job. That is a tool constraint, not a defect. It equally explains why nothing runs it in this Linux container: nothing is wired to.

### Configuration state — present, deliberate, and more carefully reasoned than usual

```
[tool.mutmut]
source_paths                       = ["scripts"]
only_mutate                        = ["*fleet_analytics.py"]     # fnmatch, not glob
pytest_add_cli_args_test_selection = ["tests/test_fleet_analytics.py"]
pytest_add_cli_args                = ["-n", "0"]                 # NOT -p no:xdist
```

Three points worth carrying forward, all already recorded in the config's own comments and **not** re-litigated here:

- **mutmut is deliberately absent from `uv.lock` and from every dependency group.** CI installs it ephemerally: `uv run --locked --with mutmut==3.7.0 mutmut run`. This is a designed choice (no lock churn; no Windows-unrunnable tool landing in the operator's environment via a plain `uv sync`), not an omission. It was checked before being reported.
- **`-n 0`, not `-p no:xdist`.** `addopts = "-n auto"` is prepended, so unloading xdist also unloads the `-n` option that `addopts` still supplies, and every mutant's pytest exits 4 on `unrecognized arguments: -n` before collecting a test — a pilot that measures nothing while looking green. Corrected 2026-08-06; CI repro cited in-config as run 31127625224.
- **The suite is already mutmut-aware.** `tests/test_fleet_analytics.py:636` skips a marker assertion when `root.name == "mutants"`, because mutmut copies only the mutated source tree and `protocols/`/`docs/` do not exist there. Scoped to mutmut's own sandbox directory rather than softened to a tolerant check, so a genuinely incomplete checkout still fails.

### What a run would need

```
1. A fork()-capable host.        Linux/macOS, or WSL. Not the operator's Windows host.
                                 (This container qualifies but is not wired for it.)
2. uv == 0.11.19 exactly.        pyproject [tool.uv] required-version is an == pin;
                                 this container has 0.8.17, so `uv sync --locked` refuses.
3. The locked env + analytics.   uv sync --locked --group analytics   (fleet_analytics needs pandas;
                                 pandas is absent here).
4. mutmut, ephemerally.          uv run --locked --with mutmut==3.7.0 mutmut run
                                 then  ... mutmut results
5. Full history.                 fetch-depth 0 — mutmut's default use_git_change_detection
                                 reads history. (Same M-3 hazard: this clone arrived shallow.)
6. A wall-clock budget.          The CI job declares timeout-minutes: 30.
```

### State of the pilot itself — reported, not filed

`[#502]`'s Done-when requires "a recorded ADOPT/REJECT with measured divergence". **No such verdict exists in the tree** — the in-repo record contains the config, the CI job, and the job's own disclaimer that no verdict can be inferred from its existence. The row is open and tracked; this document does not re-file it.

Two observations about how the job now fires, offered as input to whoever settles the row:

- Since LA-4 (2026-08-07) the job runs only on `workflow_dispatch`, or on a push whose diff touches `scripts/fleet_analytics.py`, `tests/test_fleet_analytics.py`, or `pyproject.toml`.
- The pilot's *subject* last changed **2026-08-08** (`0f162aa5`). The trigger set also includes `pyproject.toml`, which changed once since gating (**2026-08-11**, `58427730`, the `[#521]` import substrate) — so the job has fired since, but on a push that did not touch the code being mutated.

**Not established here:** whether any specific CI run produced usable survivor output. Artifacts live on GitHub Actions under 90-day retention; this session did not enumerate a specific run's results, and the API path for doing so proved token-expensive. A `workflow_dispatch` is the direct way to settle `[#502]` and does not depend on any of the above.

---

# §5 · Test hygiene

**Population:** 132 test files · **2,593** `def test*` functions (AST) · **2,897** collected items (`pytest --collect-only -q -n 0`; the difference is parametrization expanding). Collection succeeds cleanly in this container.

## 5a · Tests with no assert

**Verdict: 0 genuinely assertion-free tests.**

A scan for test functions containing no `ast.Assert`, no `assert*`/`self.assert*` call, and no `pytest.raises/warns/fail/approx/deprecated_call` returned **9 candidates**. All 9 were read. **All 9 are the deliberate raises-if-wrong idiom, and every one carries a comment saying so** — the call *is* the assertion:

```
tests/test_fleet_analytics.py:502          test_digest_is_ascii_only
tests/test_fleet_audit_replication.py:74   test_classifier_evidence_is_cp1252_safe
tests/test_fleet_health.py:732             test_load_line_is_ascii_only
tests/test_fleet_health.py:794             test_append_load_row_never_raises_on_unwritable_path
tests/test_generate_floor.py:192           test_install_note_is_pure_ascii
tests/test_probe_child_backlogs.py:268     test_report_is_cp1252_encodable
tests/test_validate_reconciliation.py:228  test_restamp_invocation_is_ascii
tests/test_window_metrics.py:97            test_report_is_ascii_only
tests/test_gen_handoff.py:701              test_seal_identity_accepts_a_correctly_labelled_bundle
```

Eight are `.encode("ascii")` / `.encode("cp1252")` guards enforcing the `[#470]` Windows-console discipline — a `UnicodeEncodeError` is the failure. The ninth calls `gh.verify_seal_identity(...)` under a `# must not raise` comment. This is a consistent, documented, intentional house idiom and **is not reported as a defect**.

### L-6 (LOW) · the 9 implicit assertions are invisible to assertion-density tooling

Relevant specifically because §4's mutation pilot is in flight: a test with no explicit assertion still kills mutants (an exception is a failure), but any tool that *counts* assertions — coverage-quality reporting, a lint rule like `PT015`, or a human skimming for untested paths — will read these 9 as empty. The `# raises if ...` comments carry the intent for humans and nothing carries it for machines.

**Proposal (P3):** wrap the expression in an explicit assertion (`assert text.encode("ascii")`) or a one-line shared helper (`assert_encodable(text, "ascii")`). No behaviour change, no coverage change; it makes an existing intent machine-visible.

### L-7 (LOW) · one of the nine is weaker than the other eight

`tests/test_fleet_health.py:794` — `test_append_load_row_never_raises_on_unwritable_path` asserts a fail-soft contract by calling and expecting no exception. It would pass unchanged if `append_load_row` became a no-op entirely. This is inherent to "never raises" contracts rather than a mistake, and the fail-soft intent (*"the gauge never breaks SessionStart"*) is documented in the test. **Proposal (P3):** add a positive assertion alongside it — that a *writable* path does produce a row — so the test distinguishes "swallowed the error" from "does nothing at all". Related to §4: this is precisely the shape a surviving mutant would expose.

## 5b · Skipped-test inventory, with reasons

**68 static skip sites.** All 68 carry a reason. (My scanner initially reported one without — `tests/test_closure_token_quoting.py:95` — but that was a scanner limitation: the reason is an f-string, `pytest.skip(f"commit {sha} not reachable (shallow clone / detached fixture)")`, and the extractor only read plain string constants. Corrected by reading the site.)

```
by kind          skipif 54 · skip 10 · importorskip 4
by concentration test_gen_handoff.py 8 · test_audit.py 6 · test_verify_handoff_probes.py 6
                 test_enforcement_coverage.py 3 · test_propose_closures.py 3 · (33 files with 1-2)
```

**`skipif` reasons — 54 sites, all environment-conditional:**

```
24  git not available                     9  git not in PATH
 5  grep not in PATH                      3  pre-commit not installed — commit-time leg unavailable
 2  pre-commit or git not available       1  pre-commit not on PATH — cannot arm consumer git hooks
 1  pre-commit not installed — the commit-time leg cannot be exercised
 1  opt-in E2E gauntlet (slow: subprocess+pre-commit+git); set RUN_E2E=1
 1  reverse_dep_oracle needs a Pyright langserver; absent in this env
 1  safe-removal real-oracle catch needs a Pyright langserver; absent in this env
 1  pyright langserver not vendored — run `npm install`
 1  isolation fixtures not captured (run cli prove-isolation --freeze)
 1  arc fixtures not captured — run cli observe-arc --freeze [+ --leg-e]
 1  live spawn: set LIVED_SANDBOX_LIVE=1, have `claude` on PATH + a key
 1  live arc: set LIVED_SANDBOX_LIVE=1, have `claude` on PATH + a key
 1  workflow absent
```

**Unconditional `pytest.skip(...)` call sites — 10, each guarded by a runtime condition immediately above it:**

```
tests/test_batch_manifest.py:401          no batch open in the live repo
tests/test_block_immutable_edits.py:149   symlink creation not permitted on this host
tests/test_closure_token_quoting.py:95    commit {sha} not reachable (shallow clone / detached fixture)
tests/test_deploy_docs.py:232             symlink creation not permitted in this environment
tests/test_fleet_analytics.py:636         mutmut sandbox: only the mutated source tree is copied
tests/test_gen_audit_index.py:208         symlink creation not permitted in this environment
tests/test_gen_task_tree.py:42            tasks/ not yet generated (module 3 commits it)
tests/test_gen_task_tree.py:965           tasks/ not yet generated
tests/test_gitenv.py:225                  git could not report --local-env-vars
tests/test_surface_triage.py:71           Windows PowerShell (powershell.exe) not on PATH
```

**`importorskip` — 4:** `pandas` ×2 (`test_desired_state_report.py:220,229`), `yaml` ×2 (`test_generate_floor.py:269`, `test_report_only_wall.py:24`).

### Two guards are inert, and their prose is stale

`tests/test_gen_task_tree.py:42` and `:965` both skip when `tasks/manifest.json` is missing. **That file exists and is tracked** (`tasks/` holds 263 tracked files), so both guards are false and both tests run. Only the *comment* is stale — `"tasks/ not yet generated (module 3 commits it)"` describes a pre-`[#439]`-flip world. Recorded as a sub-item of this section rather than a numbered finding — the guards are inert, not wrong. **Proposal (P4):** delete the two guards, or restate the comment. Deleting is the stronger option — a guard that can no longer fire will silently absorb a real regression if `tasks/` generation ever breaks.

### Host-dependence of the skip set — an EMIT-lane input

The skip *count* is not a property of the repo; it is a property of the host. Measured in this container:

```
git         present      ->  33 skipif sites do NOT fire
grep        present      ->   5 skipif sites do NOT fire
pre-commit  ABSENT       ->   7 skipif sites DO fire
powershell  ABSENT       ->   1 skip site DO fire
pandas      ABSENT       ->   2 importorskip sites DO fire
claude      present      ->   (still skipped — also needs LIVED_SANDBOX_LIVE=1 + a key)
```

So a cloud lane silently runs a *different* suite than the operator's Windows host: `pre-commit` legs skip here and run there, `powershell` legs run there and skip here. Nothing currently records which set ran. **Proposal (P3):** if the telemetry v1 EMIT lane reports suite health, emit the skip count **with the host capability vector**, not as a bare number — a bare "3 skipped" is not comparable between two runs on different hosts, and comparing them would manufacture a trend that is really a host difference.

---

## Method notes and honest limits

- **Everything is proposals.** No BACKLOG row is opened, closed, or amended. No ADR is written. No code, test, config or governance file was edited. The tree changes by exactly two files: this report and the regenerated audit index.
- **The complexity metric is mine, not radon's.** Its rule is stated in §2 so it is reproducible, and it must not be read against radon's A–F bands. radon is marked UNVERIFIABLE per the brief and was not installed.
- **The suite was collected, not run.** `--collect-only` succeeded (2,897 items). A full run was not performed — it is not among the five deliverables, `pandas`/`pre-commit` are absent here so the result would not match the operator's host, and the measured cost is ~6 min parallel / ~30 min serial. So this document makes **no claim about pass/fail state**, including no claim about the two known `[#457]` legs.
- **§3's `last-touched` column required un-shallowing the clone** (`git fetch --unshallow origin`, 318 → 5,043 commits). Both the pre- and post-fix figures are reported in M-3 rather than only the good one, because the discarded measurement *is* the finding.
- **This lane does not move `audit.py health`.** `health` reports **DEGRADED** (exit 1) in this container, from two `[!!]` operational items — `repos registered (none)` (no `ecosystem/*/state.yaml` in this clone) and `hooks_armed` (pre-commit is absent here, so `.git/hooks/` is empty). Neither is caused by this lane and no `[XX]` FAIL-class finding exists. Established by measurement rather than assertion: the working tree was stashed and `health` re-run clean — **same DEGRADED, same two `[!!]`, 72 WARNs baseline vs 71 with this lane's two files applied.** On a correctly-armed operator host the two `[!!]` should not appear.
- **The scan is static.** §5a's assertion predicate cannot see assertions made through indirection deeper than one module-local helper — the same blind-spot class as M-2, and it is the reason all 9 candidates were read individually rather than reported from the scanner's output.
- **Not covered, and not claimed:** `deploy/`, `tests/` and `plugins/` were included in the ruff and test-hygiene passes but **not** in §2's complexity ranking, which the brief scoped to `scripts/`. Module-level dead-code, duplication and dependency-cycle analysis were out of scope entirely.

---

**Findings: 0 HIGH · 3 MEDIUM (M-1, M-2, M-3) · 7 LOW (L-1 … L-7) · 10 total.**
