# Archive copy of transport file DIGEST-TEST-STRATEGY-DECISION-2026-10-15-ANNEX.md

> Provenance: verbatim copy of `to-browser/DIGEST-TEST-STRATEGY-DECISION-2026-10-15-ANNEX.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] e72982e325879587. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
supersedes: none
summary: ANNEX to DIGEST-TEST-STRATEGY-DECISION-2026-10-15 -- the full decide_checks artifacts verbatim (evidence + subagent claims + pre-mortem, 8 matrix files with every cell and footnote, Codex and Grok evaluator records, the 35-row response table, the full ADR draft). Each part passed its decide_checks subcommand with 0 defects.
by: S1 test-strategy council (CC seat b85d73fc, Claude Opus 5.5, high)

# ANNEX -- test strategy decision, 2026-10-15


---

<!-- part: EVIDENCE-TEST-STRATEGY.md -->

# EVIDENCE — test strategy decision (R119, R120), 2026-10-15

producer-model: claude-opus-5-5 · base b6161972 · order `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md`
No-double-analysis (LEDGER v204): nothing below re-runs a digest. New reads are named with their reason.

## Evidence register (cited, not re-run)

- DIGEST-TEST-EXECUTION-MAP-2026-10-15: CI command `pytest -q -n 4 --dist loadgroup -m "not operator_host"` (conductor.yml:163); Windows tests 1555 s / 1551 s / 1163 s (runs 38656374259, 38725590391, 38713361053); ubuntu 751 / 544 / 770 s; setup 13-29 s; ship-gate step 66 s / 70 s / job 98 s, failing every run; `ship_gate_diff` last 10 events 655-1146 s, mean 899 s, all `fail`, catches unrecorded; land runs no tests and polls 900 s; mutmut run 38706597567 job 116327524000: 2077 of 2291 executed, 863 killed, 1210 survived, 4 timeout, 214 no tests; baseline `logs/MUTATION-BASELINE.json` = run 38073707389, identical totals.
- DIGEST-VERIFIED-HARNESS-MAP-2026-10-15: V3 ci BROKEN rows (known-reds baseline mismatch, 133 new reds over both OS, ship-gate canonical_freshness, handoff-manifest); DEAD list (substrate cloud, substrate interactive, job terra, ruleset json `enforcement: disabled`, scripts/read_gate.py, provider_bench aider/llm/amp); DUPLICATE (ruff manual id, plugin validate_backlog.py).
- RATIFICATION-2026-10-14 v9: R119, R120 (text quoted in the digest); R112 (wired or removed), R117 (T2 council), R118 (admission through the graph) from v6/v8.
- ADR-127 D1 (docs/decisions/ADR-127-ci-os-verification.md:36-41): the merge evidence is the both-OS run on the sha the integrator pushes; a lane's own push run is advisory. D6 (:59-63) local verification shrinks.
- S2 (parallel, BATCH-TEST-GRAPH-DATA-2026-10-15) measures coverage contexts and a preliminary census today; this decision designs the night pipeline and cites S2's output, it does not re-measure.

## New reads (reason: the digests do not hold these)

- `pyproject.toml:236-238`: the mutmut pilot mutates `*fleet_analytics.py` only and runs `tests/test_fleet_analytics.py` only. **The ≈41 % kill rate is ONE module (1263 lines) against ONE test file, not a repo score** — the repo-wide mutation score is unmeasured.
- `uv.lock`: pytest-cov and coverage are NOT locked (only pytest-xdist 3.8.0, grimp 3.17). Night tools need a dependency decision (precedent: `--with mutmut==3.7.0`, report-only-wall.yml:282).
- Brief D (repo reader) answers 1-9, claims below.

## Research (web, read 2026-10-15)

- Selectors: testmon 2.2.0 (coverage DB, cold = full, blind to non-Python inputs; testmon.org); pytest-impacted 0.35.0 beta (git diff + AST imports; config/lockfile -> full; conftest-fixture gap; github.com/promptromp/pytest-impacted); pytest-impact 0.1.0 (fixture graph only, misses app code; github.com/az-pz/pytest-impact). Microsoft TIA doctrine: unknown file type -> all tests, plus a periodic full run (learn.microsoft.com/azure/devops/pipelines/test/test-impact-analysis).
- Required checks: a workflow skipped by a path filter leaves its check Pending; a job skipped by `if:` reports Success; a job whose `needs` failed is skipped and may not block -> use one aggregate job with `if: always()` (docs.github.com troubleshooting-required-status-checks; github.com/re-actors/alls-green: skipped fails unless in allowed-skips).
- Sharding: pytest-split 0.11.0 (2026-02-03), `least_duration`, missing durations -> split by count; pytest-balance 0.1.0 beta (2 stars); Free plan 20 concurrent jobs (docs.github.com/actions/reference/limits).
- Merge queue: org-owned public repo or Enterprise Cloud only; this repo is personal (`isInOrganization: false`); bors-ng archived 2024-04-04.
- coverage contexts: pytest-cov `--cov-context=test` works under xdist, `dynamic_context=test_function` breaks (pytest-cov #604); `CoverageData.contexts_by_lineno`; DB schema not stable (dbschema.html); subprocess lines via `[run] patch = subprocess` + parallel + combine (subprocess.html) — whether test contexts propagate into the child is NOT documented.
- mutmut 3.x: `mutants/mutmut-stats.json` maps tests -> functions (`tests_by_mangled_function_name`); the killing test is NOT recorded; no git-diff selection for .py; name filters `mutmut run "scripts.mod*"`; 3.8.0 is latest.
- No-outcome: no ruff PT rule for assertion-free / mock-only tests; extreme-mutation ("pseudo-tested") is the studied method (arXiv 1807.05030), no Python port; LLM smell detection best 74.35 % on Python (arXiv 2506.07594).

## Subagent claims

- impacted_tests rejected coverage selection: 72.6 % of test->script edges are subprocess-only {probe: grep -c '72\.6' scripts/impacted_tests.py}
- conftest.py, pyproject.toml and uv.lock select the full suite {probe: scripts/impacted_tests.py:85}
- an unclaimed path falls back to the full suite {probe: scripts/impacted_tests.py:579}
- the guard skips deletions (staged set ACMRT) {probe: grep -c 'ACMRT' scripts/impacted_tests.py}
- the measured miss rate is 0.048 {probe: grep -c '0\.048' scripts/impacted_tests.py}
- land refuses a sha that is not a two-parent merge on base {probe: scripts/merge_path.py:300}
- the CI poll timeout is 900 s {probe: grep -c 'POLL_TIMEOUT_S = 900' scripts/ci_verdict.py}
- ci_verdict counts a failing job, including ship-gate {probe: scripts/ci_verdict.py:542}
- the CI ship-gate job is advisory at job level {probe: grep -c 'ship-gate \(advisory\)' .github/workflows/conductor.yml}
- gen_handoff's ship-gate verdict regex is anchored at line start {probe: scripts/gen_handoff.py:813}
- R37.2 (ship_gate_diff to batch close) is withdrawn {probe: protocols/STANDING_RULINGS.md:5263}
- one known-reds entry expires 2026-10-19 {probe: grep -c '2026-10-19' logs/KNOWN-REDS-REGISTRY.json}
- the mutation pilot is scoped to fleet_analytics {probe: grep -c 'only_mutate = \["\*fleet_analytics\.py"\]' pyproject.toml}
- the mutation job fails on 0 mutants executed {probe: grep -c '0 mutants executed' .github/workflows/report-only-wall.yml}
- FPG has no test node; tests/ is excluded deliberately {probe: grep -c 'tests/' scripts/file_purpose_graph.py}
- 288 top-level test files and one conftest.py {unverified}
- testmon deletes its DB on a DATA_VERSION mismatch {unverified}
- mutmut does not record which test killed a mutant {unverified}
- the repo is not in an organisation, so merge queue is unavailable {unverified}

## Pre-mortem (what could make this wrong)

1. **Registry expiry, 2026-10-19:** one windows entry expires; any expired entry makes `load_registry` refuse the whole registry and the compare exit 2 (known_reds.py:266-269). The first BUILD-2 night after 10-19 has no verdict unless renewed (V3 OPERATOR-ACTION, already open).
2. **Day is Linux-only:** Windows-only regressions surface only at night. 5 Windows-only reds existed at ADR-127 time. Accepted by R119; the cost is one repair round.
3. **Under-selection by day:** impacted_tests' measured miss rate is 0.048; the night full suite is the net, which is exactly R119's design. The three named holes (workflow/ecosystem data, deletions, empty selection) are fixed RED-first.
4. **Sharding vs the known-reds contract:** the compare is per OS leg and checks workers (known_reds.py:589-591). Shards must be unioned into the existing leg before the compare, or the verdict changes meaning.
5. **pytest-split + `--dist loadgroup`:** a group split across shards runs in two machines; safe for serialisation groups, unsafe for an order-dependent group (inference, not measured).
6. **Coverage contexts overhead and subprocess attribution:** no published overhead; S2 measures it today. Subprocess test attribution is undocumented, so 72.6 % of edges rely on the static leg.
7. **The ≈41 % premise:** R120 cites it as repo evidence; it is one module. The decision does not depend on it, but the census and the 70 % goal must not be read against it.
8. **mutmut module-name mismatch** (pyproject.toml:218-235) recurs for any module whose tests load it under another name: 0 executed -> FAIL (loud, by design).

---

<!-- part: MATRIX-Q1.md -->

# MATRIX Q1 -- Tier 1 impact selector (day, lane branch)

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A impacted_tests.py + 3 hole fixes | 4[^s1] | 4[^s4] | 4[^s2] | 4[^s4] | 4[^s3] | 4[^s4] | 3 | 4[^s1] | 3.80 |
| B pytest-testmon | 2 | 3 | 4[^s5] | 3 | 3 | 3 | 2 | 2 | 2.65 |
| C pytest-impacted | 4[^s6] | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 2.85 |
| D pytest-impact | 3 | 3 | 2 | 3 | 2 | 3 | 1 | 3 | 2.35 |

[^s1]: measured -- scripts/impacted_tests.py:22-24 (no state; table rebuilt from the tree each call), live callers .pre-commit-config.yaml:715, gates.py:150, verify.py:53
[^s2]: measured -- scripts/impacted_tests.py:15-24: coverage-based selection rejected, 53 of 73 test->script edges (72.6 %) invisible in-process, 82 of 171 test files use subprocess (recorded divergence, library-first rank 3)
[^s3]: measured -- pure Python rule table, runs today in pre-commit on Windows and in CI on ubuntu (DIGEST-TEST-EXECUTION-MAP (b), gates.py:176-181)
[^s4]: measured -- no model call and no DB; impacted_tests.py:242-279 rule table
[^s5]: measured -- pypi.org/pypi/pytest-testmon/json 2.2.0 2025-12-01, read 2026-10-15
[^s6]: measured -- github.com/promptromp/pytest-impacted README: no DB, git diff + AST graph, read 2026-10-15

---

<!-- part: MATRIX-Q2A.md -->

# MATRIX Q2A -- Tier 2 sharding (night, both OS)

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A pytest-split least_duration x4 per OS, -n 4 inside | 4[^t1] | 3 | 4[^t1] | 3 | 3 | 3 | 3 | 3 | 3.30 |
| B pytest-balance | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 2 | 2.70 |
| C xdist alone (today) | 2 | 3 | 4[^t2] | 3 | 3 | 3 | 3 | 4[^t2] | 3.15 |

[^t1]: measured -- pypi.org/project/pytest-split 0.11.0 (2026-02-03): missing durations -> even split by count, unknown tests get the mean; read 2026-10-15
[^t2]: measured -- uv.lock:994-995 pytest-xdist 3.8.0; conductor.yml:163 -n 4 --dist loadgroup live
[^t3]: measured -- run 38656374259 windows tests 1555 s, run 38725590391 1551 s (DIGEST-TEST-EXECUTION-MAP table)

---

<!-- part: MATRIX-Q2B.md -->

# MATRIX Q2B -- Tier 2 batching of the night lands

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A serial land, sharded CI per merge | 3 | 4[^b1] | 3 | 3 | 3 | 3 | 4[^b2] | 4[^b1] | 3.45 |
| B grouped land + bisection | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 2 | 2.70 |
| C grouped + attribute-by-impact, then confirm | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 2.85 |
| D GitHub merge queue | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 2.40 |

[^b1]: measured -- scripts/merge_path.py:292-355 one sha per land, refuses a stacked tip at :295-300
[^b2]: measured -- actions_verdict.py:502-557 per-test compare against the base run, per OS
[^b3]: measured -- gh repo view: public, isInOrganization false; docs.github.com merge queue requires an org-owned public repo or Enterprise Cloud, read 2026-10-15

---

<!-- part: MATRIX-Q3.md -->

# MATRIX Q3 -- The always-red CI ship-gate job

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A remove the job and gen_handoff's reader leg | 4[^g1] | 3 | 3 | 3 | 3 | 4[^g2] | 3 | 4[^g3] | 3.40 |
| B fix (CI profile) and make blocking | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 2.75 |
| C keep advisory as is | 1 | 2 | 3 | 3 | 3 | 2 | 1 | 3 | 2.10 |

[^g1]: measured -- scripts/ci_verdict.py:542 counts the job's failure; actions_verdict.py:651-654 turns it into PRE-EXISTING/REGRESSED
[^g2]: measured -- 66 s and 70 s per run, runs 38656374259 and 38725590391 (DIGEST-TEST-EXECUTION-MAP)
[^g3]: measured -- conductor.yml:577-624 is one job; ci_verdict.py:535-550 needs no edit (any non-success job fails); its reporting reader gen_handoff.py:813 never matches (3 receipts 'emitted no verdict line')

---

<!-- part: MATRIX-Q4.md -->

# MATRIX Q4 -- ship_gate_diff

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A once per night on the tip, kept until ship-gate is green on main; seeded new-FAIL-on-red-base witness | 3 | 3 | 3 | 3 | 3 | 3 | 4[^d2] | 3 | 3.20 |
| B remove now | 3 | 3 | 3 | 3 | 3 | 4[^d1] | 1 | 4[^d1] | 2.85 |
| C keep per merge | 2 | 3 | 3 | 3 | 3 | 2 | 2 | 3 | 2.55 |

[^d1]: measured -- MERGE-PATH-RUN-EVENTS.jsonl last 10 events mean 899 s, all fail (DIGEST-TEST-EXECUTION-MAP Answers)
[^d2]: measured -- a seeded defect is a controlled run whose expected catch is known before it runs

---

<!-- part: MATRIX-Q5.md -->

# MATRIX Q5 -- R120 test->code edge source

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A static edges UNION in-process coverage contexts, per-sha artifact | 3 | 4[^e2] | 4[^e1] | 3 | 3 | 3 | 4[^e2] | 2 | 3.30 |
| B coverage contexts alone | 3 | 3 | 4[^e1] | 3 | 3 | 3 | 2 | 3 | 2.95 |
| C testmon database | 3 | 3 | 2 | 3 | 3 | 3 | 2 | 2 | 2.50 |
| D grimp import edges | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2.80 |

[^e1]: measured -- coverage.readthedocs.io api_coveragedata: contexts_by_lineno, contexts survive combine; pytest-cov contexts.html --cov-context=test works under xdist (pytest-cov #604); read 2026-10-15
[^e2]: measured -- scripts/impacted_tests.py:15-24 (72.6 % of test->script edges are subprocess-only) and :462-529 (static edges: FPG imports depth 3, naming, literal text search)
[^e3]: measured -- testmon/db.py DATA_VERSION 14 deletes and recreates the file on a version mismatch, read 2026-10-15

---

<!-- part: MATRIX-Q6.md -->

# MATRIX Q6 -- R120 NO-OUTCOME detection

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A AST check (stdlib ast, custom) | 4[^n3] | 4[^n3] | 3 | 4[^n3] | 3 | 4[^n3] | 3 | 3 | 3.40 |
| B LLM reviewer | 3 | 1 | 3 | 2 | 3 | 1 | 2 | 2 | 2.20 |
| C AST, then an LLM second opinion on the flagged list (advisory) | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 2.75 |

[^n1]: measured -- docs.astral.sh/ruff/rules: no PT rule for an assertion-free or mock-only test, read 2026-10-15
[^n2]: measured -- arXiv 2506.07594: LLM test-smell detection 74.35 % (Python) best case
[^n3]: measured -- an AST walk is deterministic Python with no model call (stdlib ast)

---

<!-- part: MATRIX-Q7.md -->

# MATRIX Q7 -- Mutation policy (night)

Weights: unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15

| Option | unattended | code | library | model | os | tokens | testable | simplicity | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A changed functions, strict score, 70 %, 0-mutant FAIL | 3 | 3 | 4[^m2] | 3 | 2 | 3 | 4[^m1] | 3 | 3.25 |
| B changed modules | 3 | 3 | 4[^m2] | 3 | 2 | 3 | 2 | 4[^m2] | 3.00 |
| C whole scripts/ nightly | 1 | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 2.50 |

[^m1]: measured -- report-only-wall.yml:330-356 already fails the job on 0 mutants executed
[^m2]: measured -- pyproject.toml:237 only_mutate exists; mutmut 3.x name filter 'mutmut run "scripts.mod*"' (mutmut __main__.py, read 2026-10-15)
[^m3]: measured -- pyproject.toml:206-209: an unscoped run over scripts/ is impractical; 2291 mutants for one 1263-line module

---

<!-- part: EVAL-CODEX.md -->

served-model: gpt-5.6-sol
attestation-source: codex exec header (model: gpt-5.6-sol, provider: openai, sandbox: read-only, session id 01a13f92-5caa-7782-9c76-4154f48b0fbc) in codex-full.log
producer-model: claude-opus-5-5
nonce: NONCE-212397440 (echoed on line 1)
invocation: codex exec -m gpt-5.6-sol --sandbox read-only -C <repo> --output-last-message codex-last.md - < prompt-codex.md (stdin = the prompt file, closed at EOF)

NONCE-212397440

Q1: AMEND — Keep the selector, but make an empty selection machine-failing or explicitly typed; a printed line alone can silently pass.

Q2: DISAGREE — `pytest-split` is not locked, cannot directly consume the promised JUnit durations, and its interaction with `xdist_group` is unproved.

Q3: AGREE — Removing the permanently red advisory job eliminates cost and a false failure consumed by `ci_verdict`.

Q4: DISAGREE — One seeded defect and five quiet nights cannot justify removing a gate whose last ten recorded runs all failed.

Q5: AMEND — The static union is necessary, but coverage-context generation needs locked tooling and a proven subprocess-attribution contract.

Q6: DISAGREE — The proposed AST predicates do not establish whether a test has an outcome or is semantically duplicate.

Q7: DISAGREE — Current mutmut configuration hardcodes one module/test, while diff-hunk function selection and per-merge attribution are unspecified and unreliable.

- id: C1 -- D1's `selected: 0` is only output, not a refusal: the current command returns normally after emitting an empty pytest argument string, so its Done-when can pass without executing a test (`scripts/impacted_tests.py:827-838`).
- id: C2 -- Q1 understates selector risk: its own measured miss rate is 0.048 over only 31 diffs, yet the flip condition waits for more than 5% of night reds over ten nights, a denominator that may never become large enough to trigger (`scripts/impacted_tests.py:32-40`).
- id: C3 -- D3 names `pytest-split` as production machinery although neither `pytest-split`, `pytest-cov`, nor `coverage` is locked; the declared environment currently contains only the existing pytest tooling (`pyproject.toml:198-238`, `uv.lock`).
- id: C4 -- D3 says durations come “from junit,” but the current pytest command emits only console output and no JUnit file, duration database, or conversion step (`.github/workflows/conductor.yml:148-163`).
- id: C5 -- D3 does not prove that splitting test groups across four machines preserves `xdist_group` assumptions; the current design only guarantees each group stays on one worker within one pytest invocation (`.github/workflows/conductor.yml:154-159`).
- id: C6 -- The claim that six required contexts remain unchanged is not an effective gate contract: the checked-in ruleset is disabled, and only the two pytest contexts are shown as required (`deploy/conductor-required-checks.ruleset.json:4-20`).
- id: C7 -- D3's “union shard results and run the compare unchanged” omits a fail-closed specification for missing/cancelled shard artifacts, while the comparator requires an exact worker pin and rejects non-comparable pytest exits (`scripts/known_reds.py:583-592`).
- id: C8 -- D4's “about 8 minutes” is not established by the cited measurements; dividing test time by four ignores setup, artifact transfer, aggregation, imbalance, and the unmeasured nested `pytest-split` plus xdist topology (`.github/workflows/conductor.yml:145-227`).
- id: C9 -- D5 inaccurately describes a `ci_verdict` “job set” to edit: `ci_verdict` dynamically treats every non-success job as failing, so deleting the workflow job is the actual behavior change (`scripts/ci_verdict.py:535-550`).
- id: C10 -- D5's second reader is reporting-only and explicitly does not control pass/fail, weakening the stated rationale for removing it (`scripts/gen_handoff.py:807-818`).
- id: C11 -- D6's five-night removal rule is statistically empty: a single known seeded failure proves only that one path, while the proposal provides no coverage model for the unique defects `ship_gate_diff` is meant to detect (`scripts/ship_gate_diff.py:89-153`).
- id: C12 -- D7 assumes useful subprocess test contexts despite the selector's measured evidence that 53 of 73 relevant edges are invisible to in-process coverage; `[run] patch = subprocess` supplies line data but the draft provides no fail-closed test-attribution proof (`scripts/impacted_tests.py:15-24`).
- id: C13 -- D7 does not define whether regenerated `ecosystem/test-edges.json` is committed before the tested SHA; existing doctrine says integrator-generated material is regenerated at merge, so generating it “within the batch” can leave the verdict and committed graph describing different trees (`scripts/impacted_tests.py:600-609`).
- id: C14 -- D8 reverses the present staged-input contract, which deliberately excludes true deletions; it needs explicit rename/delete/test-delete cases before it can safely refuse removals (`scripts/impacted_tests.py:710-727`).
- id: C15 -- D9's DUPLICATE predicate is unsound: identical covered lines and assert targets do not imply identical fixtures, parameters, inputs, environment, subprocess behavior, or expected values.
- id: C16 -- D9's NO-OUTCOME predicate falsely flags legitimate `unittest` assertions, helper assertions, snapshot checks, exit-code checks, and tests whose called code raises on failure; merely finding `assert` or `pytest.raises` is not an outcome oracle.
- id: C17 -- D10 cannot work by merely adding a mutmut name filter because the live configuration still restricts mutation to `fleet_analytics.py` and test execution to one test file (`pyproject.toml:236-238`).
- id: C18 -- D10 inherits a documented mutmut attribution failure whenever the loader's module name differs from the path-derived mutant name, with no general repair beyond the one pilot module (`pyproject.toml:223-235`).
- id: C19 -- D10's per-lane 70% score is undefined when one changed function spans or is touched by multiple nightly merges; the draft specifies a night-range function filter but no deterministic function-to-lane ownership rule.
- id: C20 -- The first post-expiry night can have no comparable verdict because one expired registry entry invalidates the registry, and expiry is fail-closed (`scripts/known_reds.py:259-269`).
---

<!-- part: EVAL-GROK.md -->

served-model: grok-4.20-0309-non-reasoning
attestation-source: grok --output-format json modelUsage key, and debug log line "resolved credentials model=grok-4.20-0309-non-reasoning auth_type=ApiKey"
producer-model: claude-opus-5-5
nonce: NONCE-212397440 (echoed on line 1)
invocation: grok --prompt-file prompt.md --output-format json --max-turns 2 (cost USD 0.0339)

NONCE-212397440

**Q1: DISAGREE** -- matrix underweights testable (miss rate 0.048 unproven at scale) and simplicity (custom script vs library).

**Q2A: DISAGREE** -- least_duration with missing data falls back to even split; pytest-split's beta status and cross-shard group risk ignored.

**Q2B: DISAGREE** -- serial land with 900s poll + 8min CI cannot scale; flip-condition admits grouped land is needed but defers it.

**Q3: DISAGREE** -- removing always-red job without fixing root cause (known-reds mismatch) just hides the symptom; advisory status was already a silent failure.

**Q4: DISAGREE** -- seeded-defect measurement on throwaway branch does not prove production catch rate; 899s mean runtime makes nightly untenable.

**Q5: DISAGREE** -- static + coverage union still blind to 72.6% subprocess edges per evidence; mutmut non-attribution makes ZERO-KILL column unreliable.

**Q6: AGREE** -- AST is only viable no-model option; LLM numbers confirm it.

**Q7: DISAGREE** -- 70% threshold on changed-functions with unmeasured repo-wide kill rate (pilot was 41% on 1 module) sets unachievable bar; 0-mutant FAIL already breaks pilot.

- id: G1 -- ADR D1 claims impacted_tests.py is "measured" but pilot was only fleet_analytics (pyproject.toml:236-238)
- id: G2 -- D1 "RED-first" holes fix assumes deletions guarded (scripts/impacted_tests.py: guard skips ACMRT per subagent claim)
- id: G3 -- D2 `re-actors/alls-green` pinned by SHA is not in evidence; 20-line in-repo alternative unproven (GitHub required-checks docs)
- id: G4 -- D3 shard aggregator unions results but known-reds compare expects exact worker context (known_reds.py:589-591)
- id: G5 -- D3 pytest-split least_duration unsafe for order-dependent groups (pre-mortem #5, unmeasured)
- id: G6 -- D5 removal of ship-gate ignores that ci_verdict counts it explicitly (scripts/ci_verdict.py:542)
- id: G7 -- D6 ship_gate_diff nightly on tip with 899s mean (DIGEST-TEST-EXECUTION-MAP) violates night close-by-0700 goal
- id: G8 -- D7 test-edges.json generation inside night batch creates race with parallel lands (no lock mentioned)
- id: G9 -- D9 census ZERO-KILL column cannot work: mutmut 3.x does not record killing test (mutmut-stats.json evidence)
- id: G10 -- D9 NO-OUTCOME AST check has no "Done-when cannot fail" criterion; false-positive rate flip at 20% admits design flaw
- id: G11 -- D10 mutation name filter from diff hunks fails on modules loaded under different name (pre-mortem #8, pyproject.toml:218-235)
- id: G12 -- Quality attribute "0 regressions reach main" cannot be measured if Tier-1 selector under-selects (flip-condition threshold of 5% too lax)
- id: G13 -- Pre-mortem #1 registry expiry on 2026-10-19 makes first post-expiry night fail hard (known_reds.py:266-269)
- id: G14 -- Coverage contexts with xdist + subprocess patch undocumented and unproven at scale (pytest-cov #604)
- id: G15 -- No dependency decision for pytest-split, pytest-cov, or mutmut pinning (uv.lock omits them; precedent in report-only-wall.yml)
---

<!-- part: RESPONSES.md -->

# Responses to the adversaries — test strategy decision, 2026-10-15

| id | objection (short) | response |
|---|---|---|
| C1 | `selected: 0` is only printed, can pass with no test run | **Accepted** -- D1(c) adopts the already-ruled `[#703]`: an empty selection on a diff with any non-`.md` path FAILS CLOSED and runs the full suite; a docs-only diff runs the `-m live_repo` tier. `[#703]`'s RED witness carries it |
| C2 | 0.048 miss rate over 31 diffs; 5 % flip may never trigger | **Accepted** -- flip is an absolute count: 3 Tier-1 misses (a night red in a test the lane's diff should have selected) in 10 nights; night 1 also re-measures the miss rate against the coverage edges |
| C3 | pytest-split, pytest-cov, coverage not locked | **Accepted** -- OQ1 asks to lock them (ADR-106); the rows' Done-when includes the `uv.lock` entries |
| C4 | no JUnit file or conversion exists | **Accepted** -- shards run with `--junitxml`; the aggregator converts JUnit times to `.test_durations` (stdlib xml) and uploads them as the next night's artifact |
| C5 | `xdist_group` across 4 machines unproved | **Accepted** -- RED witness: a test fails when any `xdist_group` spans two shards; if it fires, a conftest hook pins group members to the first member's shard |
| C6 | ruleset disabled, only pytest contexts shown | **Accepted** -- wording fixed: the effective contract is `actions_verdict.py:97-98` (what `land` reads); the ruleset stays disabled (VERIFIED-MAP DEAD, R112) |
| C7 | no fail-closed spec for missing or cancelled shards; worker pin | **Accepted** -- aggregator FAILs the leg on any missing, cancelled or artifact-less shard; every shard keeps `-n 4` and records it for the pin |
| C8 | "about 8 minutes" not established | **Accepted** -- stated as an estimate (1551/4 + setup + collection + aggregation); night 1 measures it and the morning digest reports it |
| C9 | ci_verdict has no job set to edit | **Accepted** -- D5 changed: deleting the job is the whole verdict change; no `ci_verdict` edit |
| C10 | gen_handoff reader is reporting-only | **Accepted** -- rationale corrected: removal is R112 (red every run, a reader that never matches); the reader leg is deleted with the job |
| C11 | one seeded defect and 5 quiet nights prove nothing | **Accepted** -- D6 rewritten: ship-gate is red on every base, so `ship_gate_diff` is the only gate that sees a NEW failure; it stays nightly until ship-gate is green on main; the seeded defect is a new FAIL on an already-red base |
| C12 | subprocess test attribution unproved | **Accepted** -- `patch = subprocess` dropped; the coverage leg is in-process only and subprocess edges come from the static leg |
| C13 | committed edge file can describe a different tree | **Accepted** -- edges are a per-sha CI artifact `test-edges-<sha>.json` of the night run, never committed; readers name the sha |
| C14 | guard deliberately excludes deletions | **Accepted** -- D8 Done-when covers delete, rename (old path treated as deleted) and test-deleted-in-the-same-change |
| C15 | DUPLICATE predicate unsound | **Accepted** -- DUPLICATE is a CANDIDATE class only, never auto-REMOVE; a parametrized test or a different fixture set is excluded |
| C16 | NO-OUTCOME predicate misfires | **Accepted** -- predicate widened to unittest `assert*`, same-file helpers that assert, returncode and raises checks; flagged only if no assertion-bearing call exists or every one targets a Mock |
| C17 | live config hardcodes one module and one test | **Accepted** -- D10 row generates the scope per night (`only_mutate` + test selection) and retires the pilot's hardcoded scope, RED-first |
| C18 | loader module-name mismatch | **Accepted** -- 0 executed for a module FAILs loudly and names it; the loader fix per module is a STRENGTHEN item |
| C19 | no function-to-lane ownership rule | **Accepted** -- a function belongs to the LAST merge in the night's first-parent order whose diff touched it |
| C20 | expired registry entry voids the verdict | **Accepted** -- the night starts with a registry load at base; an expired entry STOPS the night with OPERATOR-ACTION before any land |
| G1 | impacted_tests "measured" but pilot was one module | **Rejected** -- the Q1 footnotes cite `impacted_tests.py:15-24` (selector data); the mutmut pilot is a different organ |
| G2 | deletions not guarded | **Accepted** -- same as C14 |
| G3 | alls-green not in evidence | **Accepted** -- alls-green's skip semantics are cited (its `job_outcome.py`); adoption is OQ1; the in-repo fallback carries a RED test per need state |
| G4 | worker pin under sharding | **Accepted** -- same as C7 |
| G5 | order-dependent groups across shards | **Accepted** -- same as C5 |
| G6 | removal ignores that ci_verdict counts it | **Rejected** -- the draft cites `ci_verdict.py:542` as the reason for removal; removing the job is the answer to it |
| G7 | 899 s ship_gate_diff breaks the 07:00 window | **Rejected** -- it runs once on the final tip, not per merge: about 15 min in a night window of about 8 h; the morning digest measures it |
| G8 | edge file regeneration races the lands | **Accepted** -- same as C13: a per-sha artifact, no commit |
| G9 | ZERO-KILL cannot work without kill attribution | **Rejected** -- D9 already defines it under non-attribution: certain only when every covered mutated function has 0 kills, else UNKNOWN |
| G10 | NO-OUTCOME Done-when cannot fail | **Accepted** -- RED fixture set of 6 shapes with expected labels (assert-free, mock-only, unittest assert, helper assert, raises, returncode) |
| G11 | name filter fails on renamed loaders | **Accepted** -- same as C18 |
| G12 | 5 % flip too lax | **Accepted** -- same as C2 |
| G13 | expiry 2026-10-19 | **Accepted** -- same as C20 |
| G14 | xdist + contexts unproven at scale | **Accepted** -- `--cov-context=test` under xdist is the documented working path (pytest-cov #604); the scale is measured by S2 today; subprocess patch dropped (C12) |
| G15 | no dependency decision | **Rejected** -- OQ1 is that decision; mutmut is added to its list |

---

<!-- part: ADR-DRAFT-TEST-SYSTEM.md -->

# ADR-NNN: Test system — day/night cadence, impact selection, sharding, tests in the graph

- **Status:** Proposed (draft; number assigned at landing)
- **Date:** 2026-10-15
- **Decision tier:** T2 mini-council (R117) on R119 and R120; ratification is the operator's
- **Builds on:** ADR-127 unchanged (the merge verdict = both-OS run on the pushed sha); ADR-110 (serial `--no-ff`); ADR-118 §1 (one graph); R112 (wired or removed); R118 (admission)
- **Source:** `to-browser/DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md` + its ANNEX

## Context

R119 moves the full both-OS suite to one night batch so integration never blocks the day; today every push runs it (Windows 1551-1555 s, runs 38725590391, 38656374259). R120 makes tests graph nodes and finds tests that prove nothing by measurement. Two facts shape the design: 72.6 % of test->script edges are subprocess-only and invisible to in-process coverage (`scripts/impacted_tests.py:15-24`); mutmut does not record which test killed a mutant. The ≈41 % kill rate R120 cites is one module (`pyproject.toml:236-238`), not the repo.

## Decision

- **D1 Tier 1 (day).** A push to `worktree-**` (not `worktree-integrate-*`) runs job `tier1` on ubuntu: ruff, then `impacted_tests.py select` against the merge-base with `origin/main`, then `pytest -n 4 --dist loadgroup` over the selection; a `# FULL SUITE` answer runs D3's Linux shards. `impacted_tests.py` is extended RED-first: (a) `.github/workflows/*` and `ecosystem/**` select the tests naming them, else FULL; (b) a deleted or renamed-away `scripts/` module selects the tests importing or naming it; (c) an empty selection on a diff with any non-`.md` path FAILS CLOSED and runs the full Linux shards (`[#703]`, already ruled), a docs-only diff runs the `-m live_repo` tier. The both-OS `pytest` legs skip on a lane push unless the head commit carries `[full-ci]` (the blocker exception).
- **D2 One aggregate gate.** Job `gate`, `if: always()`, needs every job: red on a failed, cancelled or skipped need, except the `pytest` legs on a lane branch. No workflow-level path filter. `re-actors/alls-green` pinned by SHA (OQ1), else an in-repo step with one RED test per need state.
- **D3 Tier 2 sharding.** Each OS leg = 4 pytest-split shards (`--splits 4 --group k --splitting-algorithm least_duration`), `-n 4 --dist loadgroup` and `--junitxml` in each. A per-OS aggregator keeps the context names `pytest (ubuntu-latest)` / `pytest (windows-latest)`, FAILs the leg on a missing, cancelled or artifact-less shard, unions the shard results and runs the existing known-reds compare (`conductor.yml:165-227`) unchanged, with every shard's `-n 4` recorded for the worker pin. It converts JUnit times to `.test_durations` for the next night (artifact); missing durations split by count. A RED witness fails when any `xdist_group` spans two shards. The effective verdict contract is `actions_verdict.py:97-98`; the ruleset stays disabled.
- **D4 Night lands are serial.** `merge_path land` unchanged (one two-parent merge on base per land). The night opens with a registry load at base; an expired entry stops the night with OPERATOR-ACTION before any land. Each land's wall time is measured (estimate 7-9 min sharded vs about 26 today) and reported in the morning digest.
- **D5 The CI ship-gate job is removed (R112).** Red every run and counted by `ci_verdict.py:542`, whose rule (any non-success job fails, `:535-550`) needs no edit; `gen_handoff`'s reporting leg that never matches (`:813`) goes with it. The integrator's ship-gate on the merged tree (`gates.py:176-181`) stays.
- **D6 `ship_gate_diff` stays at night while ship-gate is red on main.** On an always-red base it is the only gate that sees a NEW failure. It runs once on the final tip; each run appends its introduced `(check, status, evidence)` triples to its event as `catches`. Night 1 seeds a new FAIL on an already-red base on a throwaway branch and records which gates catch it. Removal is due when ship-gate is green on main (then ship-gate alone discriminates).
- **D7 Tests are graph nodes.** Edges `test -exercises-> module` = the UNION of `source: static` (the impacted_tests table: FPG imports depth 3, naming, literal text) and `source: coverage` (nightly `--cov-context=test`, Linux, in-process only). The coverage edges are a per-sha CI artifact `test-edges-<sha>.json`, never committed; readers name the sha. FPG gains node kind `test` and edge kind `exercises` (static), excluded from `orphan_census`'s process walk; `system_map`'s `tests` field reads them; R118 admission keeps `impacted_tests.select`. The same night coverage run feeds R86's no-drop gate on changed modules (`[#1451]` item 2).
- **D8 A removal carries its tests.** `impacted_tests guard` reads staged deletions and renames: a removed module that leaves a test whose only `exercises` edges point to it, or that imports or names it, is REFUSED naming that test, unless that test is deleted or rewritten in the same change. Cold, from the static edges.
- **D9 The census** (night 1, then weekly) flags ORPHAN (all edges to DEAD or missing modules), DUPLICATE (CANDIDATE only: line-set subset and equal assert expressions, no parametrize or fixture difference), ZERO-KILL (certain only when every covered mutated function has 0 kills, else UNKNOWN), NO-OUTCOME (stdlib `ast`: no assertion-bearing call — `assert`, unittest `assert*`, `pytest.raises`, returncode checks, same-file asserting helpers — or every one targets a Mock). Output KEEP / STRENGTHEN / REMOVE for the operator's GO; no model decides a class.
- **D10 Mutation on changed functions, nightly, Linux** (mutmut needs `fork`). The night job generates the scope (changed functions -> mutmut name filter; tests from `impacted_tests.select`) and retires the pilot's hardcoded `fleet_analytics` scope. Score `killed / (killed + survived + timeout + no_tests)`, threshold 70 % per lane; a function belongs to the LAST merge in first-parent order that touched it. 0 executed for a module with a changed function FAILs naming the module; no changed function prints `SKIPPED`. Advisory 5 nights, then blocking (OQ2).

## Quality attributes

- **Quality attribute(s):** availability of the operator's day; fidelity of the merge verdict; measurability of test value.
- **Scenario:** Source: a lane seat. Stimulus: pushes a commit to its branch. Artifact: `conductor.yml`, `impacted_tests.py`. Environment: by day, BUILD lanes running. Response: Tier 1 runs impacted tests on Linux; the night lands it with both OS sharded. **Response measure:** Tier-1 verdict ≤ 5 min; night batch closed by 07:00; 0 regressions the full suite would catch reach main (R119); 0 orphan tests after the census; mutation score on changed code ≥ 70 % per lane (R120).
- **Decision evidence:** matrices Q1-Q7 (`decide_checks matrix`, 0 defects); DIGEST-TEST-EXECUTION-MAP-2026-10-15; DIGEST-VERIFIED-HARNESS-MAP-2026-10-15; EVAL Codex gpt-5.6-sol and Grok grok-4.20 (35 objections, 29 accepted).

## Flip-condition

3 Tier-1 misses (a night red in a test the lane's diff should have selected) in 10 nights -> FULL on every non-`.md` change until repaired. Serial lands over the window twice -> grouped land with bisection (needs `land` to accept a first-parent chain). The `xdist_group` witness unfixable -> xdist alone at night. NO-OUTCOME false positives above 20 % in the operator's REMOVE review -> an advisory LLM second opinion.

## Alternatives considered

Selectors: pytest-testmon (persisted DB; blind to subprocess and non-Python inputs), pytest-impacted (beta; import graph only), pytest-impact (fixture graph only). Sharding: pytest-balance (0.1.0 beta), xdist alone (cannot cut a 26-min leg on 4 vCPU). Batching: GitHub merge queue (unavailable: personal-account repo), grouped land + bisection (`land` refuses a stacked tip, `merge_path.py:295-300`; kept as flip). Edges: coverage alone (misses 72.6 %), testmon DB (unstable schema), grimp (a second import graph, ADR-118 §1). NO-OUTCOME: LLM reviewer (74 % best case). Mutation: whole `scripts/` (impractical), changed modules (scores a lane on legacy code it did not touch). ship_gate_diff: remove now or after quiet nights (it is the only new-failure detector on a red base).
