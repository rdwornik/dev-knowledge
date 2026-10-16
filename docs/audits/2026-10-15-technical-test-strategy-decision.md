# Archive copy of transport file DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] b76def8b1a86d5e6. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
supersedes: none
summary: The T2 council on R119 and R120. It produced an ADR draft, 9 rows ([#1560]-[#1568], intake 115, on branch `worktree-test-strategy-rows-2026-10-15`, not on main) and 3 open questions. Codex sol and Grok raised 35 objections; 29 were accepted and changed 7 decisions. The ≈41 % mutmut figure covers one module, not the repo.
by: S1 test-strategy council (CC seat b85d73fc, Claude Opus 5.5, high)

# TEST STRATEGY DECISION — R119 day/night, R120 tests in the graph (2026-10-15)

**What this rests on, and what was new.** The evidence is the TEST-EXECUTION-MAP and VERIFIED-HARNESS-MAP digests and R119/R120 (v9), cited and not re-run (LEDGER v204). The council also read the repo for the facts those digests lack (brief D) and did web research with sources (briefs A-C).

**The gates passed.** `decide_checks` gave 0 defects on every check: 9 matrices, subagent-exclusions, subagent-claims (15 probes run, 4 claims marked `{unverified}`), paths, evaluators, response-coverage (35 of 35) and adr-sections.

**The ANNEX holds everything else verbatim:** `DIGEST-TEST-STRATEGY-DECISION-2026-10-15-ANNEX.md` (full matrix cells and footnotes, both evaluator records, all 35 responses, the full ADR, the evidence file).

## Premise correction

R120 says mutmut "executed 2077 mutants … ≈41 % killed". That is **one module, `scripts/fleet_analytics.py`, against one test file**:
- `pyproject.toml:236-238`;
- `logs/MUTATION-BASELINE.json:10`;
- run 38706597567, job 116327524000.

The repo-wide mutation score has never been measured. R120 still stands: the census and D10 measure it. The 70 % goal must not be read against 41 %.

## Verdicts

Weights (the operator's criteria): `unattended=15 code=10 library=15 model=5 os=10 tokens=10 testable=20 simplicity=15`. A score of 4 or more needs a measured citation.

| Q | decision | Σ, options in order | Codex | Grok | final |
|---|---|---|---|---|---|
| 1 Tier 1 | `impacted_tests.py`, with 2 holes fixed + `[#703]` empty → full; job `tier1` + one `if: always()` gate | ours 3.80 · impacted 2.85 · testmon 2.65 · impact 2.35 | AMEND | DISAGREE | **AMEND** |
| 2a shards | pytest-split, 4 per OS, `-n 4` inside, fail-closed aggregator under today's leg names | split 3.30 · xdist-only 3.15 · balance 2.70 | DISAGREE | DISAGREE | **AMEND** |
| 2b batching | serial `land`, unchanged; the night stops at open on an expired known-reds entry | serial 3.45 · attribute+confirm 2.85 · bisect 2.70 · merge queue 2.40 | (none) | DISAGREE | **AGREE** |
| 3 CI ship-gate | remove the job (R112) | remove 3.40 · fix+block 2.75 · keep 2.10 | AGREE | DISAGREE | **AGREE** |
| 4 ship_gate_diff | once a night on the tip, kept while ship-gate is red on main; record `catches` | keep-measured 3.20 · remove 2.85 · per-merge 2.55 | DISAGREE | DISAGREE | **AMEND** |
| 5 edges | static UNION in-process coverage contexts; a per-sha artifact, never committed | union 3.30 · coverage 2.95 · grimp 2.80 · testmon 2.50 | AMEND | DISAGREE | **AMEND** |
| 6 NO-OUTCOME | stdlib `ast`, widened predicate; DUPLICATE is a candidate only | ast 3.40 · ast+llm 2.75 · llm 2.20 | DISAGREE | AGREE | **AMEND** |
| 7 mutation | changed functions, strict score, 70 % per lane, 0 executed = FAIL | functions 3.25 · modules 3.00 · whole 2.50 | DISAGREE | DISAGREE | **AMEND** |

Facts that decided it:
- **Merge queue is impossible here.** The repo is personal (`isInOrganization: false`); merge queue needs an org or Enterprise Cloud. bors-ng is archived.
- **`land` takes one merge on base per sha** (`merge_path.py:295-300`).
- **72.6 % of test→script edges are subprocess-only** (`impacted_tests.py:15-24`).
- **mutmut does not record the killing test.**
- **The ship-gate job is red on every run, and `ci_verdict.py:542` counts it.**

## Objections that changed a decision (verbatim; all 35 are in the ANNEX)

- **C1** — "D1's `selected: 0` is only output, not a refusal … its Done-when can pass without executing a test (`scripts/impacted_tests.py:827-838`)." → **Accepted.** The already-ruled `[#703]` applies: an empty selection on a code diff runs the full suite.
- **C11** — "D6's five-night removal rule is statistically empty: a single known seeded failure proves only that one path …" → **Accepted.** On an always-red base, ship_gate_diff is the only detector of new failures. It stays until ship-gate is green on main, and its witness seeds a new FAIL on a red base.
- **C13** — "D7 does not define whether regenerated `ecosystem/test-edges.json` is committed before the tested SHA …" → **Accepted** (also G8, a race). The edges are the artifact `test-edges-<sha>.json`, never committed.
- **C17** — "D10 cannot work by merely adding a mutmut name filter because the live configuration still restricts mutation to `fleet_analytics.py` …" → **Accepted.** The night job generates the scope and retires the hardcoded pilot scope.
- **C20** — "The first post-expiry night can have no comparable verdict because one expired registry entry invalidates the registry …" → **Accepted** (also G13). The night stops at open with OPERATOR-ACTION; one entry expires **2026-10-19**.
- **Other accepted objections:** C2 (the flip uses an absolute count: 3 misses in 10 nights), C4/C5/C7/C8 (junit durations, an `xdist_group` witness, fail-closed shards, the wall time stated as an estimate), C9/C10 (no `ci_verdict` edit is needed), C12 (subprocess context propagation dropped), C14-C16, C18-C19.
- **Rejected: G1, G6, G7, G9, G15.**
  - G7 "899 s breaks 07:00": it runs once per night, not per merge.
  - G9 "ZERO-KILL cannot work": the draft already defines it under non-attribution (certain only at 0 kills, else UNKNOWN).
  - G15: OQ1 is that dependency decision.

## ADR draft (condensed; full text in the ANNEX) — "Test system: day/night cadence, impact selection, sharding, tests in the graph"

ADR-127 is unchanged: the merge verdict is the both-OS run on the pushed sha.

- **D1 Tier 1 by day.**
  - A push to `worktree-**` (not `worktree-integrate-*`) runs `tier1` on ubuntu: ruff, then `impacted_tests.py select` against the merge-base, then `pytest -n 4 --dist loadgroup`. FULL runs the Linux shards.
  - The selector gains two fixes: workflow/ecosystem data selects the tests that name it, and a removed module selects its tests. An empty selection is handled by `[#703]`.
  - The both-OS legs skip on a lane push unless the commit carries `[full-ci]` (the blocker exception).
- **D2 One aggregate gate.** Job `gate`, `if: always()`, needs every job. A failed, cancelled or skipped need makes it red, except the pytest legs on a lane branch. Never a workflow `paths:` filter.
- **D3 Night sharding.**
  - Each OS runs 4 pytest-split shards (`least_duration`, `--junitxml`).
  - A per-OS aggregator keeps `pytest (ubuntu-latest)` and `pytest (windows-latest)`, FAILs on any missing shard, unions the results and runs the known-reds compare unchanged.
  - Durations come from last night's junit. A witness fails when an `xdist_group` is split across shards.
- **D4 Serial night lands** with `land` unchanged. The night opens with a known-reds registry load; an expired entry stops it.
- **D5** Remove the CI ship-gate job and gen_handoff's reader leg. The integrator's ship-gate on the merged tree stays.
- **D6 ship_gate_diff:** once a night on the final tip, recording `catches`, kept while ship-gate is red on main.
- **D7 Test→module `exercises` edges.**
  - Static edges live in FPG (node kind `test`, kept out of the orphan census).
  - Coverage edges come from nightly `--cov-context=test`, as a per-sha artifact. The same run feeds R86's no-drop gate (`[#1451]`).
- **D8** Pre-commit refuses a delete or rename that leaves tests pointing only at the removed module.
- **D9 The census** marks ORPHAN, DUPLICATE (candidate only), ZERO-KILL (certain or UNKNOWN) and NO-OUTCOME (`ast`). It emits KEEP / STRENGTHEN / REMOVE for the operator's GO; no model decides a class.
- **D10 Mutation**, nightly on Linux, on changed functions.
  - Score = killed / (killed + survived + timeout + no_tests); threshold 70 % per lane.
  - A function belongs to the last merge that touched it.
  - 0 executed = FAIL; no changed function = SKIPPED.
  - Advisory for 5 nights, then blocking.
- **Flip conditions.**
  - 3 Tier-1 misses in 10 nights: FULL on every non-`.md` change.
  - Serial lands over the window twice: grouped land with bisection.
  - An `xdist_group` that cannot be pinned: xdist only.
  - More than 20 % AST false positives: an advisory LLM second opinion.

## Rows (branch `worktree-test-strategy-rows-2026-10-15`, lands with the next freeze; Done-when RED-first in each file)

- **BUILD-2a slot 1:**
  - `[#1560]` `tier1` + gate + `[full-ci]`;
  - `[#1561]` the two selector holes;
  - `[#1562]` shards + aggregator (kill-candidate `[#1383]`; carries `[#1451]` item 1);
  - `[#1563]` remove the CI ship-gate job (after OQ3);
  - `[#1564]` registry check at night open + ship_gate_diff `catches` + the seeded witness.
- **First night:**
  - `[#1565]` test nodes + the coverage-context artifact;
  - `[#1566]` `scripts/test_census.py` (4 classes, 6-shape fixture set);
  - `[#1567]` mutation on changed functions.
- **BUILD-2b:** `[#1568]` the removal guard.
- **The first night's census commands:**
  - `uv run --locked pytest -n 4 --dist loadgroup -m "not operator_host" --cov=scripts --cov-context=test --cov-report= -p no:cacheprovider`
  - `coverage json --show-contexts`
  - `scripts/test_census.py classify --edges test-edges-<sha>.json --dead <DEAD list> --mutmut mutants/mutmut-stats.json`
  - `scripts/test_census.py report`

  S2's preliminary census (`BATCH-TEST-GRAPH-DATA`) supplies night 1's overhead figure.
- **Ids** were taken above the parallel sessions' reach. On every ref the highest task id was 1540 and the highest intake id 110.

## Open questions for the operator

1. **How are pytest-split, pytest-cov/coverage and mutmut declared, and is `re-actors/alls-green` admitted?**
   - The tools are already approved (R86 split + coverage gate; R81 mutmut).
   - **Recommendation:** lock all three in `uv.lock` (ADR-106; `--with` resolves transitive dependencies unlocked), and admit alls-green pinned by commit SHA.
2. **Is mutation blocking from night 1?**
   - **Recommendation:** advisory for 5 nights, then blocking. The real per-lane score is unknown until it is measured.
3. **GO to remove the CI ship-gate job (`[#1563]`, R112)?**
   - **Recommendation: GO.** It is red on every run, `ci_verdict` counts it, and its only reader never matches.
