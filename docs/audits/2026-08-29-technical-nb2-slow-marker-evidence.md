# NB2 · CLOUD C2 — [#598] slow-marker selector evidence

**Lane:** night-batch-2 C2 · **Repo:** `dev-knowledge` · **Revision:** `fcc9485` (`origin/main`, committed 2026-08-29T00:02:07+02:00) · **Substrate:** cloud container, READ-ONLY · **Writes:** zero.

---

## 0. Verdict first, because it changes what the three deliverables mean

**[#598]'s marker sweep was already measured and STOPPED — one day before this brief was frozen — and the row is still `status: open`.**

`docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md` ran a `--durations=25` arm, applied the row's own gating clause (*"if the suite is long-pole (top25 >20% wall), STOP the marker sweep, report, and fix nothing"*), returned **LONG-POLE at 21.42 % of worker-seconds**, and recorded (§8): *"the marker sweep, the PLAYBOOK Ch5 cadence line and the coverage lint are all correctly NOT executed."* Its §4 states the reason in one line: *"The lever is therefore [#597]/W2A, not markers."*

Meanwhile `tasks/598-p-6-a-slow-marker-selector-so-tiered-gating-has.md:4` still reads `status: open`, and its done-when still asks for a regenerable marker set. So the row is **narrowed-by-measurement but not discharged**, and the brief's three deliverables are asking for a design the evidence has already ruled out *in the shape P-6 originally proposed*.

I did not resolve that by declining. **The brief's three deliverables are delivered in full below, as a design of record** — because the 2026-08-27 audit killed *one specific rule* (mark every subprocess-spawning file, select on `-m "not slow"`), not the question the row's done-when actually asks, which is whether a marker set can be **derived and re-derivable**. My answer to deliverable 3 is that a *purely* durations-derived set cannot be, and I show that with a number I computed here rather than asserting it. That is the substantive finding of this lane.

**Premise defect, flagged per the standing clause:** the brief's "WHAT TO GROUND IT IN" names `conftest.py`. **There is no `conftest.py` anywhere in this repo** — `find . -name conftest.py -not -path "./.git/*"` returns empty, and `pyproject.toml:144-145` records this deliberately: *"Root `conftest.py` (Shape A) stays permitted-not-mandated ([#430](a), STANDING_RULINGS F5) — none exists in this repo."* The row's own `refs` list carries the same dead locator. Any design that assumes a conftest hook point is assuming a file that would have to be *created*, which is an ADR-101 Rule C question, not a free move.

---

## 1. What I measured here, and what I did not

Per the standing clause, **I ran no gate, no hook, no pytest, and no `audit.py`.** The container's `uv` is 0.8.17 against the pinned `==0.11.19` (`pyproject.toml:25`), so `uv run --locked` cannot start. Everything below is either (a) read from a file in the clone, (b) computed by `grep`/`git`/`python3 -c` over the clone with the command shown, or (c) marked **MEASUREMENT-OWED-LOCAL**.

### 1a. Composition of the suite — computed in this clone

```
command: see each row; run at fcc9485 from /home/user/dev-knowledge

test_files_toplevel      135     ls tests/*.py | wc -l
fixtures_entries          13     ls tests/fixtures | wc -l
spawn_pattern_files       66     grep -rl 'subprocess\.\|sys\.executable' tests/*.py | wc -l
slow_marked_files (grep)   5     grep -rl 'pytest\.mark\.slow' tests/*.py | wc -l
slow_marked_files (AST)    4     <- the grep count is WRONG; see 1b
spawn_AND_slow             4     comm -12 of the two sorted lists
spawn_NOT_slow            62     comm -23 of the two sorted lists
live_repo_files           29     grep -rl 'pytest\.mark\.live_repo' tests/*.py | wc -l
audit_driving_files       33     grep -rl 'ALL_CHECKS\|cmd_health' tests/*.py | wc -l
tmp_path_files           120     grep -rl 'tmp_path' tests/*.py | wc -l
langserver_files           3     tests/test_{safe_remove,reverse_dep_oracle,legibility_graph_conformance}.py
```

My `spawn_NOT_slow = 62` differs from the 2026-08-27 audit's *"64 files match a `subprocess.`/`sys.executable` pattern, 4 carry a marker"* (§4) and from PERF-RECON B9's *"59 subprocess-spawning files carry no marker"* (`docs/audits/2026-08-26-technical-perf-recon.md`, Q4 §). Three different numbers for one predicate across three days is itself the finding: **the spawn-pattern predicate is not stable enough to be an admission rule**, which is a second, independent reason to reject P-6's original shape. All three counts are reported; none is reconciled here.

**Collected test counts are MEASUREMENT-OWED-LOCAL.** `--collect-only` needs the pytest suite. I report AST `def test_*` counts as a floor; parametrization makes collected > defs.

### 1b. A locator correction — the `slow` marker covers 4 files, not 5

`grep -rl pytest.mark.slow tests/*.py` returns **5** files. An AST pass shows **`tests/test_proof_layer.py` carries no real marker** — its two hits (`tests/test_proof_layer.py:176`, `:215`) are inside `textwrap.dedent(...)` *fixture source strings* that the proof-layer scanner parses as synthetic test files. The real surface:

```
file                            module-level pytestmark   function-level @slow
test_e2e_consumer_lifecycle.py  YES (+ 2 skipif)          0     (1 test def)
test_hook_telemetry.py          YES                       0     (11 test defs, 9 parametrized)
test_fleet_analytics.py         no                        3     (of 64 test defs)
test_telemetry_emit.py          no                        3     (of 33 test defs)
test_proof_layer.py             no                        0     <- fixture strings only
                                                          --
                          function-level @slow decorations: 6
```

Command: an `ast.parse` walk over `tests/test_*.py` resolving `pytestmark` assignments and `@pytest.mark.slow` decorators, ignoring string literals.

This matters beyond pedantry: **a durations-derived regeneration script that finds its "current" marker set by grep will disagree with pytest by one file**, and a regen-and-diff gate built on that grep would report a permanent false diff. The rule is the repo's own (`CLAUDE.md` §4, *"Resolve a locator before you act on it"*).

**Second stale locator, in the row that owns the marker:** `tasks/317-default-parallel-test-invocation-slow-tier-marke.md:12` says *"the orthogonal `slow` marker is live at `pyproject.toml:61`"*. At `fcc9485` the `markers = [` block is at **`pyproject.toml:122`**, `live_repo` at `:123`, `slow` at `:124`. `pyproject.toml:61` is inside the `[tool.mutmut]` prose. Reported, not fixed.

---

## 2. The evidence base — three durations runs, none of them mine

| # | Artifact | Host | Command | Collected | Result |
|---|---|---|---|---|---|
| R1 | `docs/audits/2026-08-14-technical-night2-latency.md` §1 | 4-core Linux cloud, **pyright present** (§1c fails #1/#2) | `pytest -n 0 --durations=50 -q` | 2897 | 701.60 s serial / 473.02 s `-n auto` |
| R2 | `pyproject.toml:153-168` (comment) | operator host | serial vs `-n auto` ×2 | 2362 | 1785.61 s / 358.77 s / 330.15 s |
| R3 | `docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md` §1-2 | operator host, 16 logical CPUs, **contended** | `pytest --durations=25 -q` (`-n auto`) | 3988 | 1440.9 s wall, exit 1 (35 F) |

R1 is the only run in the repo that emitted a **full-ish** table (`--durations=50`) and a **junit** sum (699.24 s). R3 emitted a top-25 only. Neither emitted `--durations=0`. That gap is the whole of §5 below.

---

## 3. The finding that constrains everything: the cost ranking is NOT stable across hosts

I cross-referenced R1's top-25 against R3's top-25 mechanically (parsing both tables out of the two markdown files with `re`, normalising `tests/` prefixes and stripping parametrize ids):

```
R1 top-25 ∩ R3 top-25                                14 of 25   (56%)
R1 top-25 sum                                        624.00 s   of a 699.24 s junit total
R1 ranks 1-7, all three langserver files             482.10 s = 68.9% of R1's total cost
those same 3 files' appearances in R3's top-25       0
```

Every test in the three files that grep for `langserver|pyright` — `test_safe_remove.py`, `test_reverse_dep_oracle.py`, `test_legibility_graph_conformance.py` — occupies **ranks 1 through 7 of R1** and holds **68.9 % of that run's measured cost**, and **not one of them appears anywhere in R3's top-25**.

The mechanism is readable, not mysterious. `scripts/reverse_dep_oracle.py:297-311` resolves the language server in three steps: an explicit override, a vendored `node_modules/pyright/langserver.index.js`, then `shutil.which("pyright-langserver")` — and returns `None` otherwise, which `:441/:474/:477` map to a fail-soft `oracle-unavailable` envelope. **There is no `node_modules/pyright` in this clone** (`ls node_modules/pyright` → absent). So the class's cost is a step function on host tool presence: present ⇒ ~69 % of the suite; absent ⇒ near zero, and the tests still *pass* (fail-soft) rather than skipping visibly.

Two consequences, both load-bearing for deliverable 3:

1. **A rank-keyed rule ("mark the top N by `--durations`") is not regenerable.** Regenerated on an R1-shaped host it marks the oracle files; regenerated on an R3-shaped host it un-marks them and marks eight live-audit tests instead. The set would flip on re-derivation with no code change — which is *worse* than the hand-curated list [#598] exists to replace, because it rots silently and looks measured.
2. **It un-marks the class exactly when un-marking is most wrong.** A class whose tests fail-soft-fast when their tool is absent does not become cheap; it becomes *unproven*. Removing its marker on the host where it did not run, and re-adding it on the host where it did, inverts the intent.

**Honest limit on this finding:** I am comparing a `-n 0` table (R1) with an `-n auto` table (R3), and R3's own §7 records host contention. The *ordinal* comparison is still valid — R3's own numerator is its top-25 regardless of denominator, and zero oracle tests appear in it — but I have not established *why* R3's host produced no oracle cost. The most economical explanation is that `pyright-langserver` is absent there (R1's §1c records it *present* on that container, as two assertion failures). **Whether `pyright-langserver` resolves on the operator's host is MEASUREMENT-OWED-LOCAL** — one line, `python -c "import shutil;print(shutil.which('pyright-langserver'))"`, settles it and converts this inference into a fact.

---

## 4. DELIVERABLE 1 — Marker taxonomy

The existing `slow` (`pyproject.toml:124`) declares its admission rule as *"subprocess / pre-commit / real-git spawns"*. That rule is now measured not to select cost: **62 files match the spawn pattern and carry no marker**, and R3 §4 shows marking them *"would not have moved the top five, because those five are slow from the audit they run, not from a spawn count."* PLAYBOOK Ch5 (`protocols/PLAYBOOK.md:870-873`) already records the same defect: *"`pytest -m "not slow"` removes almost none of the 89 %."*

So the taxonomy must key on the **dominant cost driver**, and the evidence contains exactly two that clear any plausible threshold, plus one that must stay separate.

```
oracle    — the test drives an EXTERNAL LANGUAGE SERVER (pyright-langserver / a
            vendored node langserver.index.js), directly or through
            scripts/{safe_remove,reverse_dep_oracle,legibility_graph}.py's real-oracle path.
            Admission (no judgement call): if removing pyright-langserver from PATH changes
            this test's outcome or its runtime, it is `oracle`.
            Today: 3 files, 35 test defs (safe_remove 10, reverse_dep_oracle 19,
            legibility_graph_conformance 6).

livegate  — the test's cost is a walk of the LIVE repo tree that the test did not build:
            an audit.py check-registry run (`ALL_CHECKS` / `cmd_health` / `cmd_ship_gate`)
            or a whole-corpus markdown scan.
            Admission (no judgement call): if the test's cost scales with the size of
            docs/ + tasks/ rather than with a tmp_path fixture you constructed, it is
            `livegate`.
            Candidate population: 33 files match `ALL_CHECKS|cmd_health`; the corpus-scan
            arm adds test_normalize_headers.py and test_toc.py. Which of the 33 actually
            clear the threshold is MEASUREMENT-OWED-LOCAL (see §6).
```

**`slow` is retired, not redefined.** Redefining a live marker in place leaves 6 function-level decorations and 2 module-level `pytestmark` blocks asserting an admission rule that no longer holds, with nothing to detect the mismatch. Retire the name, re-mark those 4 files under the new rules, and let the registration in `pyproject.toml:124` go — a marker whose rule is measured not to select what it claims is a rule that has already failed.

**`live_repo` (`pyproject.toml:123`, 29 files) stays untouched and is NOT merged into `livegate`.** It is a *scope* marker, not a cost marker: `pyproject.toml:119-121` and `plugins/tier1-lifecycle/commands/ship.md:32` use it for the **docs-only ship pre-flight** (`pytest -m live_repo -q`), which selects *what a docs diff can break*, not *what is expensive*. The two populations overlap heavily and mean opposite things — merging them would silently change what a docs-only `/ship` runs. Stated because the overlap makes the merge look free.

**Rejected alternative, named as the brief requires:** *P-6 as originally written* — "every test spawning a subprocess or interpreter carries `slow`" (`docs/audits/2026-08-26-technical-perf-recon.md`, row P-6). Rejected on two independent grounds, both measured: (a) it imposes an authoring obligation on ~62 files and R3 §4 measures that it *"would not have moved the top five"*; (b) my §1a shows the predicate itself yields 59 / 62 / 64 across three consecutive days, so it cannot be the stable half of a regen-and-diff gate. **Also rejected:** a single `integration` marker covering both classes — rejected because PLAYBOOK Ch5's *"oracle-tier rule"* (`protocols/PLAYBOOK.md:865-869`) already requires the oracle class to be **separately selectable in-lane** for a lane touching `scripts/safe_remove.py` or `scripts/reverse_dep_oracle.py`. One name cannot express a split the doctrine already relies on.

---

## 5. DELIVERABLE 2 — Selector shape, and where it is declared

### 5a. The literal invocations

```
# TIER A — fast, per-step in a lane. Adds the lane's own touched-module tests.
uv run --locked pytest -m "not oracle and not livegate" -n auto --dist worksteal -x --tb=short

# TIER A' — the PLAYBOOK Ch5 oracle-tier rule: a lane touching an oracle module runs
#           the oracle tier in-lane, because that tier is exactly what covers it.
uv run --locked pytest -m "oracle" -n auto --dist worksteal --tb=short

# TIER B — full suite, ONCE, at integration on the merged result ([#528] leg 2).
uv run --locked pytest -n auto --dist worksteal --tb=short

# TIER B-serial — the on-demand sweep that catches what parallelism masks
#                 (pyproject.toml:163-168 already documents this arm).
uv run --locked pytest -n 0 -q

# DOCS-ONLY ship pre-flight — UNCHANGED, orthogonal axis (ship.md:32).
uv run --locked pytest -m live_repo -q && uv run --locked ruff check
```

### 5b. Where it is declared — the single-source problem is real and it has four heads

The invocation is currently written out longhand in at least four places, and they already disagree:

| # | Site | Locator | What it says today |
|---|---|---|---|
| 1 | pytest default | `pyproject.toml:162` | `addopts = "-n auto"` — no `--dist worksteal` |
| 2 | `verify` skill | `.claude/skills/verify/verify.py:137` | `pytest -n auto --dist worksteal --max-worker-restart=0 -x --tb=short` |
| 3 | `/ship` pre-flight | `plugins/tier1-lifecycle/commands/ship.md:32,37-38` | `-m live_repo` (docs) / bare full suite (code) |
| 4 | Doctrine prose | `AGENTS.md` "Build / test / lint", `CLAUDE.md` §4, `protocols/PLAYBOOK.md:838-873` | `pytest -x --tb=short`; "targeted in-lane, full at integration" |

Site 1 lacks the `--dist worksteal` that site 2 has and that [#528] leg 1 asks for. Site 3 is the subject of an open row, `tasks/340-*` (*"the skill text still prescribes the bare run"*). Site 4 is prose. **A fifth selector added to this without a single source is a fifth thing to drift.**

**Recommendation: declare the tiers once, machine-readably, in `pyproject.toml`, and gate the prose sites for agreement.**

```toml
# pyproject.toml — new table, alongside [tool.pytest.ini_options]
[tool.dev-knowledge.test-tiers]
fast        = "not oracle and not livegate"
oracle      = "oracle"
full        = ""
docs-only   = "live_repo"
```

`verify.py:137` reads `fast` from that table instead of hardcoding; `/ship`'s code-diff branch reads `full` (which also discharges the mechanism `tasks/340-*` asks for); the PLAYBOOK/CLAUDE/AGENTS prose keeps its human sentence and is held to the table by a **`test-tier-agreement` pre-commit hook**.

That hook is not an invention — it is a copy of a shape this repo already ships. `CLAUDE.md` §9 lists **seven regen-and-diff / agreement gates** (`codemap-freshness`, `toc-freshness-playbook`, `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`, `intake-index-freshness`), and `provider-registry-agreement` (`scripts/check_provider_registry.py`) is the exact precedent for *"a `.md` prose binding and a source-of-truth file must agree, and the gate asserts agreement, not correctness."* Its documented honest limit applies here verbatim: **agreement is not correctness — nothing in this gate says the tier is the right tier.**

**Rejected alternative:** a `Makefile` (or `justfile`) as the tier home. Rejected on a repo fact, not taste: the primary development host is Windows — `pyproject.toml:56-59` records *"This repo is Windows-developed"* as the reason the mutation pilot is CI-only — and `make` is not a declared dependency in `[dependency-groups]`. A tier home the operator's own host cannot invoke is a second source of truth with extra steps. **Also rejected:** a root `conftest.py` implementing auto-marking by import inspection — it does not exist (§0), creating it is an ADR-101 question, and `pyproject.toml:144-145` records the permitted-not-mandated status deliberately.

---

## 6. DELIVERABLE 3 — REGENERABILITY (the half [#598] turns on)

### 6a. What a `--durations` run MUST emit — and why neither R1 nor R3 qualifies

Both prior runs used `--durations=N` with a small N. **A top-N table cannot be turned into a threshold rule**, because the rule needs the denominator's tail, and the tail is exactly what a top-N discards. Concretely: R3's §3 had to invent *three* denominators and argue about which was fair, precisely because it had a numerator without a population.

The regeneration run must emit all six of these, in one artifact:

```
1. --durations=0 --durations-min=0
      The COMPLETE per-test table, not a top-N. Without the tail there is no
      denominator and no threshold, only a ranking.

2. -n 0
      Serial. Under -n auto, --durations accumulates per worker and the honest
      denominator becomes worker-seconds; R3 §3 spent a whole section on that
      problem. Serial gives one denominator and needs no argument.

3. --junit-xml=<path>
      Machine-readable per-testcase times, so the rule is applied by a script and
      not by re-reading a markdown table. PRECEDENT, not invention: R1 §1 already
      reports "Sum of testcase times (junit) 699.24 s".

4. A HOST-CONDITIONAL TOOL MANIFEST, in the same artifact:
      pyright-langserver | node | pre-commit | git | RUN_E2E | uv | pytest | xdist
      resolved presence/absence, plus nproc, OS, .python-version.
      THIS IS THE LEG BOTH PRIOR RUNS LACK, and §3 shows it is the leg that
      decides whether the numbers are comparable at all.

5. The collected count and the base SHA.

6. The exit code and the failure set, unfiltered.
      R3 exited 1 with 35 failures; a durations table from a partially-failed run
      under-costs every test that did not reach its assertion.
```

**Every duration produced by such a run is MEASUREMENT-OWED-LOCAL.** No number in this section is one I computed; I am specifying the emission, not supplying it.

### 6b. The mechanical rule — and the split that makes it re-derivable

The naive rule — *"mark the top N by duration"* — is refuted by §3: 14/25 stability, and the class holding 68.9 % of R1 is 0 % of R3's top-25. A set derived that way flips on re-derivation with no code change.

**The rule that survives splits membership from threshold:**

```
MEMBERSHIP is derived from SOURCE, not from durations.
    A test is `oracle`   iff its module (or the module it drives) resolves a
                             langserver argv — i.e. reaches
                             reverse_dep_oracle.find_langserver / the safe_remove
                             real-oracle path / the legibility-graph oracle.
    A test is `livegate` iff it reaches audit.py's ALL_CHECKS / cmd_health /
                             cmd_ship_gate against a path that is not a tmp_path
                             it constructed, OR enumerates the live .md corpus.
    Both are computed by an AST + call-graph pass over tests/ and scripts/.
    Host-INDEPENDENT. Deterministic. Re-derivable on any machine, offline.

THRESHOLD is derived from DURATIONS, and governs the CLASS, never the test.
    From the §6a junit table, for each class D:
        share(D) = sum(t for tests in D) / sum(t for all tests)
    D is integration-only iff share(D) >= 0.10 ON A RUN WHERE D's ENABLING TOOL
    IS PRESENT (manifest leg 4 proves presence; a run with the tool absent
    CANNOT lower a class below threshold — it can only fail to raise it).
    Host-DEPENDENT, re-measurable, and stamped with the host that measured it.

THE GATE is regen-and-diff, over MEMBERSHIP only.
    scripts/gen_test_tiers.py --check  recomputes membership from source and
    diffs it against the markers on disk; non-empty diff BLOCKS. Exactly the
    shape of the seven regen-and-diff hooks CLAUDE.md §9 already lists.
    --write applies the markers. A contributor who adds an oracle-driving test
    and forgets the marker is refused at commit time, with the fix being one
    regeneration.
```

Why this and not the alternatives: a purely durations-derived set is host-unstable (§3, computed). A purely hand-curated set is what [#598] exists to eliminate — R3 §4 names it precisely: *"a hand-maintained selector, rotting from the day it landed."* The split makes the **volatile** input (durations) govern a decision taken **once per class** — a number the architect rules on and that appears in an audit artifact with its host stamped — while the **daily-churning** input (which tests exist) is derived deterministically from source and gated mechanically. That is the only arrangement in which "regenerate the marker set" is a safe command rather than a coin flip.

**The AST/call-graph pass is the load-bearing unbuilt piece and I am not going to understate it.** `scripts/proof_layer.py:203-332` already does AST resolution of markers, `skipif` conditions and probed tool names over `tests/`, so the technique is in-repo and proven; but membership for `livegate` requires following a call *through* `scripts/audit.py`, which `proof_layer.py` does not do. **Whether that resolves cleanly for all 33 `ALL_CHECKS|cmd_health` files is MEASUREMENT-OWED-LOCAL.** The honest fallback if it does not: `livegate` membership degrades to a per-file declaration with an *authoring* gate (the file matches `ALL_CHECKS|cmd_health` ⇒ it must carry the marker or an inline `# not-livegate: <reason>`), which is checkable and re-derivable but is a weaker guarantee than a call graph. Say partial when it is partial.

---

## 7. THE COVERAGE GAP — stated, not softened

The repo's own doctrine is that a gate that never fired is not proven. A fast tier that skips a slow tier does not run some tests. Here, by name, is what it does not run.

### 7a. Today's `-m "not slow"` — what it already deselects

Enumerated by AST (§1b), not estimated:

| Deselected | Scope | What stops being proven |
|---|---|---|
| `tests/test_hook_telemetry.py` | whole module (`pytestmark`), 11 test defs / 9 parametrized | **The two fail-closed pre-push gates' exit-code contract.** Its own docstring: *"`block_ff_push` and `block_unanchored_push` are the two pre-push organs that fail CLOSED … exit codes must not move — 0 allow, 1 refuse, 2 internal error."* Plus `block_commit_on_main`. All three are live blocking hooks in `CLAUDE.md` §9. |
| `tests/test_e2e_consumer_lifecycle.py` | whole module, 1 test def | The consumer install/arm gauntlet. **Already unrun in every default invocation** — `pytestmark` additionally carries `skipif(not RUN_E2E)` and `skipif(shutil.which("pre-commit") is None)` (`:32-36`), so `-m "not slow"` removes nothing here that was running. |
| `tests/test_telemetry_emit.py` | 3 of 33 defs | The WAL multi-process concurrency smoke, and both halves of the **git-derived shallow-clone refusal** (`test_git_derived_refuses_on_a_real_shallow_clone`, `test_git_derived_emits_on_a_full_clone_and_stamps_provenance`). |
| `tests/test_fleet_analytics.py` | 3 of 64 defs | Real-repo mining end-to-end and `analyze_repo`'s fail-soft on a non-repo. |

**So today's fast tier already leaves the three gate organs' exit-code contract unproven**, and that is true *right now*, before any change this report proposes.

### 7b. What the PROPOSED fast tier would additionally not cover

`oracle` — **certain**, 3 files / 35 test defs:

```
tests/test_safe_remove.py                    10 defs   the removal-refusal oracle:
                                                       test_real_oracle_blocks_real_cross_module_removal
                                                       test_real_oracle_allows_orphan_removal
tests/test_reverse_dep_oracle.py             19 defs   reverse-dependency resolution + the
                                                       oracle-unavailable fail-soft envelope
tests/test_legibility_graph_conformance.py    6 defs   test_graph_oracles_registered_and_operational
                                                       test_cell_code_code_fires
```

Unproven in a fast run: **`scripts/safe_remove.py`'s refusal to remove a cross-module-referenced symbol** — a correctness gate, not a lint — and the legibility-graph oracle registration. R1 §1c is the direct warning here: on a host where the langserver is absent these tests *fail soft and pass*, so excluding them from the fast tier means the class is unproven on **two** independent axes at once (deselected where the tool exists, vacuous where it does not).

`livegate` — **population MEASUREMENT-OWED-LOCAL** (which of the 33 clear the 10 % threshold needs the §6a run). The named candidates, taken from R3's top-25 and R1's top-25 rather than guessed:

```
tests/test_audit.py                      (test_health_degraded_no_ecosystem, _ok_with_registered_repo,
                                          _stays_ok_with_na_status)   — 202 tests per R1 §1b
tests/test_hub_identity.py               (test_no_hub_only_check_skips_when_the_stored_path_is_stale)
tests/test_writer_integrity.py           (test_live_registry_has_no_unconditionally_inert_check_left)
tests/test_membership_agreement.py       (test_declaration_leg_works_under_package_mode_invocation)
tests/test_review_artifact_coverage.py   (test_leg_is_advisory_on_the_live_repo)
tests/test_verify_handoff_probes.py      (test_registered_check_never_fails_on_live_repo)
tests/test_generated_artifact_freshness.py
tests/test_floor_conformance.py
tests/test_normalize_headers.py          (4 corpus scans)   — corpus arm
tests/test_toc.py                        (1 corpus scan)    — corpus arm
tests/test_doc_code_edge.py, test_validate_doc_structure.py, test_validate_doc_claims.py
```

**And here is the gap that must not be softened:** those tests are the ones that prove `audit.py`'s check registry runs clean against the live tree — and `audit-health` (`audit.py health`) is itself a **blocking pre-commit hook** (`CLAUDE.md` §9: *"FAIL blocks the commit"*). R3 §4 states the identity plainly: *"the suite's pole and the commit gate's pole are the same object."*

> **A fast tier that excludes `livegate` is a tier in which the repo's own blocking self-conformance gate is unproven.** Not "less covered" — unproven, in the repo's own sense of the word. That cost is real, it is the largest single cost of tiering here, and it is the direct consequence of the fact that the expensive tests and the load-bearing tests are the same tests.

That is not an argument against tiering. It is the reason the tier boundary must be an architect's ruling with the number attached ([#597]'s MEASURE-FIRST clause, and its *"NO check is made faster by being made weaker"*), and not a marker sweep a lane performs.

### 7c. The gap no tier closes

Neither tier exercises the **merged** tree. That is [#528] leg 2 and it is already doctrine (`protocols/PLAYBOOK.md:838-846`, `AGENTS.md` "Suite cadence"): *"Per-lane greens are evidence about each lane in isolation; the merged tree is a state no lane exercised."* Tiering does not create this gap and does not close it; the one full suite at integration is what covers it. Named so the fast/full split is not mistaken for the whole of the cadence.

---

## 8. Self-audit — applying the brief's own failure mode to this report

The brief's stated failure mode: *"If your report contains a number you did not compute from a file in the clone, you have guessed."* Applying it:

**Numbers I computed in this clone** (commands shown at §1a, §1b, §3): 135 test files; 66 spawn-pattern files; 62 spawn-not-slow; 29 `live_repo` files; 33 `ALL_CHECKS|cmd_health` files; 120 `tmp_path` files; 4 real slow-marked files (AST) vs 5 by grep; 6 function-level `@slow`; the per-file test-def counts; the 14/25 top-25 overlap; the 624.00 s R1 top-25 sum; the 482.10 s / 68.9 % oracle share; the zero oracle appearances in R3's top-25; `fcc9485` and its commit date; the absence of `conftest.py`; the absence of `node_modules/pyright`; the presence of `pyright-langserver` at `/root/.local/bin/` **on this container**.

**Numbers I cited from artifacts and did NOT re-measure** — every one carries a locator, and none was produced by me or on the operator's host: R1's 701.60 / 473.02 / 268.74 s and its per-test table (`docs/audits/2026-08-14-technical-night2-latency.md` §1-2); R2's 1785.61 / 358.77 / 330.15 s (`pyproject.toml:153-168`); R3's 1440.9 s, 4932.45 s top-25 sum, 21.42 %, 3988 collected (`docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md` §1-3); the close packet's wall-times (`docs/audits/2026-08-26-verification-batch-1-close-packet.md` §8).

**MEASUREMENT-OWED-LOCAL, explicitly:** every collected-test count in this report (I report AST def-counts as a floor and never as collected); which of the 33 `livegate` candidates clear the 10 % threshold; whether the AST/call-graph membership pass resolves cleanly through `audit.py`; whether `pyright-langserver` resolves on the operator's host (§3's inference depends on it); every wall-time of every proposed tier; and the [#317] done-when bar *"the `not slow` run completes under 60 s"*, which `docs/audits/2026-08-10-technical-satisfied-row-census.md:108-113` already records as **NOT** established and needing *"one timed `not slow` run on a machine with the toolchain."* I did not supply it.

**Ways this report can still fail while looking complete, stated because the brief demands it:**

1. **§3 is an ordinal comparison across two different pytest modes** (`-n 0` vs `-n auto`) on two different, differently-loaded hosts. The conclusion — *rank-keyed derivation is host-unstable* — is robust to that, since a class holding 68.9 % in one run and appearing zero times in the other's top-25 cannot be reconciled by a denominator. But the *magnitude* of the instability is not a measured quantity, and I have not claimed it is.
2. **The `livegate` class is defined but not enumerated.** I give a population of 33 by a grep predicate and a candidate list from two audits' top-25. The actual membership is the output of a pass that does not exist yet. A reader could mistake the candidate list for the tier.
3. **This is a design of record for a row a landed measurement already narrowed.** §0 says so plainly, but the length of §4-§6 could read as a recommendation to *proceed*. It is not. On the evidence in this repo, the correct next act for [#598] is a **disposition** — the row is either discharged against R3 §8 or re-scoped by the architect to the membership/threshold split in §6b — and the durations run in §6a is what a re-scope would need first. Nothing here should be built before that ruling.
4. **I did not verify that `--durations=0 --durations-min=0` and `--junit-xml` behave as specified under this repo's pinned pytest 9.x + xdist 3.8.** They are documented flags, but the repo's own history (`pyproject.toml:93-113`, the `-n 0` vs `-p no:xdist` correction, measured twice and still insufficient) is a standing warning that flag interactions here are not safely assumed. **MEASUREMENT-OWED-LOCAL.**

---

## 9. Locator index

```
tasks/598-p-6-a-slow-marker-selector-so-tiered-gating-has.md:4,13   the row + its done-when
tasks/317-default-parallel-test-invocation-slow-tier-marke.md:12    stale locator pyproject.toml:61
tasks/528-lane-latency-full-suite-multiplied-across-a-batch.md:12   tiered-suite law, legs 1-3
tasks/597-p-4-a-declared-tier-per-check-and-p-3-s-telemetr.md       the actual lever (R3 §4)
tasks/340-ship-pre-flight-validator-honors-the-consumer-re.md:12    /ship selector site
pyproject.toml:25                    required-version = "==0.11.19"  (why no gate ran here)
pyproject.toml:122-125               markers = [ live_repo:123, slow:124 ]
pyproject.toml:144-145               "Root conftest.py ... none exists in this repo"
pyproject.toml:153-168               R2 durations comment; the -n 0 serial arm
pyproject.toml:56-59                 "This repo is Windows-developed" (Makefile rejection)
.claude/skills/verify/verify.py:137  the fast-tier invocation site
plugins/tier1-lifecycle/commands/ship.md:32,37-38   docs-only / code-diff branches
protocols/PLAYBOOK.md:838-873        Ch5 Tiered suite; :865-869 the oracle-tier rule;
                                     :870-873 "removes almost none of the 89%"
scripts/reverse_dep_oracle.py:297-311, :441/:474/:477   langserver resolution + fail-soft
scripts/proof_layer.py:203-332       in-repo AST marker/skipif/tool-probe resolution
scripts/check_provider_registry.py   the agreement-gate precedent (CLAUDE.md §9)
docs/audits/2026-08-14-technical-night2-latency.md         §0 env, §1a top-50, §1b/§1c, §2, §3
docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md  §1-3 measurement, §4 finding,
                                                               §7 limits, §8 disposition
docs/audits/2026-08-26-technical-perf-recon.md             Q4 + row P-6 as originally proposed
docs/audits/2026-08-26-verification-batch-1-close-packet.md §8 integrator wall-times
docs/audits/2026-08-10-technical-satisfied-row-census.md:108-113  the <60s bar, NOT established
tests/test_proof_layer.py:176,215    the two fixture-string false positives
tests/test_e2e_consumer_lifecycle.py:31-36   module pytestmark + double skipif
tests/test_hook_telemetry.py:1-20,47         the three fail-closed organs; module pytestmark
```

**Repo-fact reconciliation** (the brief's operator-disk figures vs this clone at `fcc9485`, `ls … | wc -l`): `docs/intake/*.md` **56** = 56 · `docs/decisions/*.md` **89** = 89 · `docs/audits/*.md` **769** = 769 · `tasks/**/*.md` **344** = 344. No disagreement; the clone is not behind.