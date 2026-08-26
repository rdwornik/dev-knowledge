# PERF-RECON-2026-08-25 — LANE P (read-only, cloud)

> Provenance note (added at landing): this file is the verbatim session result of the cloud
> recon lane (Dispatch-Cloud, 2026-08-26), reconstructed from the operator's chat transcript by
> the browser architect because the cloud session's report never reached Downloads. Content
> below is unmodified from the session result.

SUBSTRATE HONESTY (Q1 clause). Cloud clone is SHALLOW (`git rev-parse --is-shallow-repository`
= true, 331 commits), there is no `.venv`, local `uv` is 0.8.17 against a pinned `==0.11.19`,
so NO gate was run and NO timing was produced. Every number below is either (a) a static count
of the checked-out tree, or (b) a number THE REPO ITSELF RECORDS, cited at file:line. Nothing
here is a lane-produced timing finding. Repo state: `436e737` (origin/main).

Headline: the three fixes with the largest expected payoff are algorithmic and library-free,
and they sit in ONE module. "Parallelize the checks" is already DONE — that lever is spent.

================================================================================
Q1 — STATIC BOTTLENECK MAP (ranked by expected payoff)
================================================================================

B1 · VERY HIGH · O(commits x journal) rescan with per-iteration re-splitting ·
     scripts/journal_anchor.py:319-340 · confidence HIGH
     `mention_not_record_warnings` loops: for each introduced commit -> for each of the
     journal's entries -> `entry.splitlines()` -> substring test per line. `_entries()` is
     memoized (:275) but `.splitlines()` is NOT, so every outer iteration re-splits and
     re-allocates the whole file. Live corpus: JOURNAL.md = 2,943,050 bytes / 24,268 lines /
     998 `### ` entries. The scan is invertible to ONE pass building
     {short_sha -> (mentioned, recorded)}. No library needed.

B2 · VERY HIGH · 2 git subprocess spawns per spine SHA, in a loop ·
     scripts/journal_anchor.py:142-150 (+ the repo's own note at :184-187) · HIGH
     REPO-RECORDED, verbatim at :185-187: "a single `audit.py health` run called this 404
     times and spawned 808 `git rev-list` processes at ~144 ms each, 116.8 s in all". The
     [#533] `lru_cache` (:153) removed the duplicate half; the per-unique-SHA spawns remain.
     `git rev-list --parents <ref>` returns the entire parent map in ONE process; `fp..sha`
     is then a graph walk in Python. 404 spawns -> 1. The ~144 ms/spawn is a Windows
     process-creation tax, which is why this dominates on the operator's host and not here.

B3 · HIGH · substring scan of a 2.9 MB string per introduced commit ·
     scripts/journal_anchor.py:203-205 · HIGH
     `is_anchored` = `any(c[:7] in journal for c in introduced(...))`. Same inversion as B1
     kills it. B1+B2+B3 are one refactor of one module.

B4 · HIGH · 44 of 46 checks spend full ship-time cost on every commit ·
     scripts/audit.py:644 and :1192 are the ONLY two `_GATE_MODE` consumers · HIGH
     `cmd_health` sets `_GATE_MODE = True` (:4464) and the mechanism exists — but only
     `generated_artifact_freshness` and `doc_claims` consult it. The repo names the
     consequence itself at :630-632 ("a WARN-class check still SPENDS its cost on every
     commit") and at :1902 for `check_fleet_parity`: "the walk is ~8s and ALL_CHECKS also runs
     on the per-commit audit-health gate; ship-gate-only scoping is a filed follow-up".
     There is no per-check commit/ship tier declaration anywhere.

B5 · HIGH · >=8 independent whole-tree enumerations per health, no shared corpus ·
     enforcement_coverage.py:302, :714 · validate_doc_code_edge.py:107, :161, :189 ·
     validate_reconciliation.py:228 · scan_undeclared_edges.py:215 · funnel_coverage.py:449 ·
     validate_adr_status.py:400 · sites HIGH, per-run count MEDIUM (some branches conditional)
     Corpus walked: 2,469 tracked files, 2,061 `.md`, 287 `.py`; docs/audits alone is 722
     files / 13 MB, docs/handoffs another 13 MB. Nothing shares an enumeration or a read.

B6 · MEDIUM-HIGH · whole-file read to use the first 2 KB, across the full .md corpus ·
     scripts/enforcement_coverage.py:302-306 (`read_text(...)[:2000]`), reached from
     `_reconciled_applicability` :666 · HIGH

B7 · HIGH (structural) · zero content-addressed caching anywhere in the gate set · HIGH
     `lru_cache` appears at exactly 3 sites, all in journal_anchor.py (:153, :275). No
     on-disk cache exists. Yet the corpus is IMMUTABLE BY RULE (CLAUDE.md §5.3: ADRs,
     transcripts, handoffs, audits) — 722 audit files that provably cannot change are
     re-read and re-parsed on every commit. This is the largest untaken structural lever.

B8 · SPENT LEVER · check parallelism is already shipped and already armed ·
     scripts/audit.py:3795 `run_checks(..., parallel=...)`, ThreadPoolExecutor at :3870,
     width capped at 8 (`_PARALLEL_MAX_WORKERS`, :3683); `.pre-commit-config.yaml:238` runs
     `audit.py health --parallel` (armed 2026-08-20, b7833f). CONFIDENCE HIGH.
     Consequence: all 46 checks ARE embarrassingly parallel and ARE being run that way, so
     remaining wall time is Amdahl-bound by the single slowest check — which B1/B2/B3 say is
     `check_journal_spine_anchor`. Do not re-propose "parallelize the audit".
     Open sub-question (MEASURE): is 8 the right width for I/O-bound git spawns?

B9 · HIGH · test-suite structure: no session state, heavy process spawning, unarmed tier ·
     tests/ = 123 files, 3,416 `def test_` (parametrize expands to the ~3.9k cited) ·
     37 fixtures, 0 session-scoped, 2 module-scoped (grep over tests/*.py) ·
     70 of 123 files spawn subprocesses; 41 `sys.executable` spawns across 28 files ·
     `slow` marker: 4 files, ~8 tests — while 59 subprocess-spawning files carry NO marker ·
     `live_repo`: 69 uses / 36 files. CONFIDENCE HIGH.
     Reading: the #317 marker tier exists but does not cover the actual slow population, so
     the tiered-gating protocol has no selector to key on today. Zero session fixtures means
     xdist `--dist load` is safe (nothing to share), which is consistent with the repo's own
     recorded result at pyproject.toml:154-162 (identical counts across serial and two
     parallel runs).

B10 · MEDIUM · nested `pytest --collect-only` inherits `-n auto` and boots a worker pool ·
     scripts/validate_doc_claims.py:137 · HIGH
     It passes `-p no:cacheprovider` but NOT `-o addopts=`. Compare
     scripts/worktree_import_proof.py:419, which DOES pass `-o addopts=` with the comment
     "drop the repo's own addopts (e.g. `-n auto`)". Same defect class the repo already
     documents for mutmut at pyproject.toml:100-115. Ship-gate path only (gated off commit
     by `run_expensive`), so payoff is bounded — but it is a one-token fix.

B11 · MEDIUM · per-commit process fan-out at the hook layer · .pre-commit-config.yaml · HIGH
     4 `always_run: true` pre-commit hooks (:50, :136, :211, :240) plus ruff plus staged-file
     hooks, each a separate `uv run --locked python ...`. Every one pays interpreter startup
     AND a uv lock validation. Most hooks are correctly `files:`-scoped already — this is the
     residual, not a systemic miss.

================================================================================
Q2 — LIBRARY-FIRST REPLACEMENTS (verdict per item)
================================================================================

pytest-xdist — ALREADY ADOPTED, not a candidate. `addopts = "-n auto"` since 2026-08-06
  (pyproject.toml:153). Repo-recorded: serial 1785.61s vs -n auto 358.77s/330.15s, identical
  pass/fail counts. Incompatibilities to re-check are NOT the usual ones (0 session fixtures,
  no DB): they are (a) nested pytest invocations inheriting `-n auto` (B10), (b) `-n auto`
  oversubscribing when tests themselves spawn 41 interpreters, (c) mutmut, already handled.
  Open: trial `--dist loadfile` vs `load` — MEASURE-first.

pytest --durations=25 — ADOPT-candidate, zero cost, do this first. It is the only instrument
  that tells you whether the suite is long-tail (fixable by tiering) or long-pole (not).

pytest-benchmark — REJECT for this problem. It measures micro-benchmarks of chosen functions;
  the bottleneck here is process spawning and whole-corpus I/O, which it does not see.

pytest-testmon — MEASURE-first, and it is the strongest candidate for the per-merge tier.
  Coverage.py-based dependency tracking, selects only tests affected by changed files,
  DB-backed and VCS-independent; actively maintained, with a documented history of
  sqlite3.OperationalError under xdist. That last point is the measure-first condition:
  testmon + `-n auto` together is exactly the combination with a known failure mode.
  Alternative if it fails: arm the `slow` marker properly (B9) and key the tier on markers,
  which needs no dependency at all. PREFER THE MARKER PATH for universalization (Q4).

py-spy — ADOPT-candidate for ONE diagnostic run, with a caveat. Runs on Windows; `--subprocesses`
  follows subprocess.Popen and multiprocessing children into one process tree, which is what a
  spawn-dominated workload needs. CAVEAT that changes the recommendation: on a workload that is
  ~144 ms/spawn of external git, py-spy attributes time to `subprocess.run` frames — true but
  low-information.
  BETTER INSTRUMENT, AND IT IS ALREADY BUILT: the [#529] telemetry emits one `check_run` event
  per check with `duration_ms` timed INSIDE the worker (scripts/audit.py:3795-3860 docstring,
  explicitly "never around `future.result()`"). Default OFF; switch is `DEV_KNOWLEDGE_TELEMETRY=1`
  (audit.py:1706 `TELEMETRY_ENV`) or `--telemetry`. Turning it on is the profile step. Use py-spy
  only to open up whichever single check the telemetry names.

Content-hash caching (diskcache / joblib.Memory / hand-rolled) — ADOPT-candidate, but hand-rolled
  keyed on GIT BLOB SHA, not mtime and not a new dependency. Rationale: `git ls-files -s` /
  `git cat-file --batch` already give a content hash for free and are immune to mtime churn from
  clone/worktree provisioning — which this repo does constantly (worktree lanes). joblib.Memory
  and diskcache both solve a problem (pickling arbitrary returns, eviction) this repo does not
  have, and each adds a fleet-wide dependency row under ADR-106/ecosystem/dependency-baseline.yaml.
  The in-repo precedent is already correct: journal_anchor.py:275 keys its memo ON THE TEXT and
  says so — "There is nothing to invalidate, so there is no invalidation to get wrong."

concurrent.futures, process vs thread — SETTLED, do not relitigate. Threads, already chosen,
  with the reasoning recorded at audit.py:3812-3818: checks are I/O-bound on git subprocesses and
  share process-global state (`_GATE_MODE`, the journal_anchor memos) that a ProcessPoolExecutor
  could not, and several are closures that would not pickle. The only open question is width.

Ruff's model — HALF APPLIES, and it is not the half people reach for. Ruff is fast from (a) a Rust
  core and (b) a single-pass architecture: parse once, run every rule over one AST, cache per file
  on content hash. (a) is IRRELEVANT here (REJECT — this is not language-level work, and the
  brief's own ordering puts it last). (b) IS THE FINDING: today >=8 validators each independently
  enumerate and re-read the same 2,061-file markdown corpus (B5). The transferable idea is
  parse-once-share-the-corpus, which is a pure-Python refactor.

pre-commit-uv — REJECT for this bottleneck. Its published gains are install-time (~1.3x) and
  memory; per-commit `audit-health` is the cost, not hook installation. Note `uv run --no-sync`
  as a micro-lever for B11 only, and note it WEAKENS the ADR-106 `--locked` guarantee — not worth
  it without a measurement showing lock validation is material.

================================================================================
Q3 — MEASUREMENT PLAN (execute locally / Codespace; ~one session)
================================================================================

Preconditions: `uv sync --locked`; a quiet workstation (close the other lanes — the 569 s figure
was taken on a contended host, so contention is a confound, not a datum).

1. Baseline the audit, with the instrument that already exists.
   `DEV_KNOWLEDGE_TELEMETRY=1 uv run --locked python scripts/audit.py health --parallel`
   then the same with `--no-parallel`, then `--parallel --workers 16`.
   Artifact: three sets of `check_run` rows in the SQLite store (path per audit.py:1718).
   Deliverable: the 46 checks ranked by `duration_ms`. THIS IS THE PROFILE STEP.
   Expect `check_journal_spine_anchor` at or near the top (B1/B2/B3) and `check_fleet_parity`
   second (audit.py:1902). If that is NOT what comes back, stop and re-rank before building.

2. Open the top check only.
   `py-spy record --subprocesses -o audit-health.svg -- uv run --locked python scripts/audit.py health --parallel`
   Artifact: one flamegraph. Read it for the split between `subprocess.run` wait (B2 class) and
   in-Python scanning (B1/B3 class) — that split decides which of R1/R2 lands first.

3. Suite long-pole vs long-tail.
   `uv run --locked pytest --durations=25 -q` (parallel, the default path)
   `uv run --locked pytest -n 0 --durations=25 -q` (serial reference; repo-recorded ~30 min)
   Artifacts: two duration tables. Question answered: does the top 25 hold >20% of wall time
   (long-pole -> fix those tests) or <5% (long-tail -> tiering is the only lever)?

4. Width and utilization.
   During step 3's parallel run, capture core + disk utilization
   (`Get-Counter '\Processor(_Total)\% Processor Time','\PhysicalDisk(_Total)\% Disk Time'`
   sampled every 2 s, or Resource Monitor). Artifact: one CSV.
   Question answered: is `-n auto` CPU-saturating or I/O-stalled? If cores idle, raise `-n`
   and `_PARALLEL_MAX_WORKERS` past 8; if disk pegs, caching (R4) beats more workers.

5. xdist trial variations (only if step 3 shows the long-tail shape).
   `uv run --locked pytest -n auto --dist loadfile -q` vs the default `--dist load`.
   Failure modes to watch, specifically: worker crashes on the 41 `sys.executable`-spawning
   tests under oversubscription; any test that passes serially and fails under load (ordering
   coupling); and count divergence between runs — the repo's 2026-08-06 evidence is that counts
   were IDENTICAL, so any divergence is new and must be chased, not averaged away.

DO NOT run mutmut locally (Windows, no fork() — pyproject.toml:57-62).

================================================================================
Q4 — UNIVERSALIZATION SHAPE (hub-owned, per the operator's mandate)
================================================================================

PLAYBOOK protocol rules. The tiered gating already approved this window — targeted-per-merge
plus one full suite per batch — needs a SELECTOR to be real, and today it does not have one
(B9: `slow` covers ~8 tests while 59 subprocess-spawning files carry no marker). So the protocol
rule that belongs in PLAYBOOK Ch5 is not "run fewer tests", it is the authoring obligation that
makes the tier checkable: a test that spawns a subprocess or an interpreter carries `slow`; the
per-merge cadence is `-m "not slow"` plus the targeted files covering the lane's diff; the full
suite runs once at integration. That is a rule a consumer repo can adopt with no hub code at all,
and it is enforceable by a lint (`slow`-marker coverage over files matching a spawn pattern) the
way the existing marker tiers are. The second protocol rule is the commit/ship tier declaration:
every gate check declares which tier it runs in, and the commit gate runs only the commit tier.

Shared hub tooling that consumers inherit. Three things are genuinely universal and belong in the
hub, carried by the deploy manifest like the rest of the corpus. First, the corpus loader — one
enumeration and one read of a repo's markdown, memoized on git blob sha, consumed by every
validator (B5/B6/B7); it is the ruff single-pass idea in Python, it is the only fix that scales
with corpus size rather than with check count, and every consumer repo with a docs corpus gets
it for free. Second, the per-check tier declaration mechanism itself — `_GATE_MODE` generalized
from a module global consulted by 2 of 46 checks into a declared attribute the runner reads (B4);
the checks are already the deployed methodology corpus, so the tier travels with them. Third, the
git-batching idiom: one `git rev-list --parents` producing a parent map, replacing per-SHA spawns
(B2). All three are hub-owned code that a consumer inherits by taking the corpus, not by tuning
anything.

Per-repo tuning, and it must stay per-repo. Thread-pool width (`_PARALLEL_MAX_WORKERS`), xdist
`-n`, and the `--dist` mode are host-shaped, not fleet-shaped: the operator's contended Windows
workstation pays ~144 ms per process spawn where a Linux CI runner pays a fraction of that, so a
fleet-fixed width would be wrong somewhere by construction. These should become named, overridable
constants with an env override (the pattern audit.py:1690-1706 already establishes for the
telemetry switch, and explicitly NOT a new runtime-knobs YAML — that would be an ADR-101 Rule A/C
question). Also per-repo: which checks land in the commit tier, since a consumer's corpus and risk
profile differ from the hub's.

================================================================================
PROPOSED ROWS (<=6, for architect adjudication into wave-2)
================================================================================

P-1 · Invert the journal-anchor scan to a single pass
  done-when: `mention_not_record_warnings` and `is_anchored` consume one precomputed
    {short_sha -> (mentioned, recorded)} map built in ONE pass over JOURNAL.md; findings
    byte-identical to today on the live tree.
  payoff class: LARGE (CPU, per-commit) · measure-first: NONE — algorithmic, existing tests pin
    the contract. Ship independent of the profile.

P-2 · Batch the spine parent map into one git process
  done-when: `journal_anchor.introduced` derives every answer from a single
    `git rev-list --parents <ref>`; process count per health run is O(1), not O(spine).
  payoff class: LARGE on Windows, moderate on Linux · measure-first: NONE (the repo already
    recorded 808 spawns / 116.8 s at journal_anchor.py:185).

P-3 · Turn on the [#529] telemetry for a window and publish the per-check ranking
  done-when: a documented `DEV_KNOWLEDGE_TELEMETRY=1` window produces a ranked
    duration table for all 46 checks, committed as an audit artifact.
  payoff class: ENABLING (this IS the profile step; it gates P-4 and P-5) · measure-first: n/a.

P-4 · Declare a commit/ship tier per check and make the commit gate honour it
  done-when: every ALL_CHECKS member declares its tier; `audit-health` runs only the commit
    tier; `ship-gate` runs all; `check_fleet_parity` is ship-only (discharging the follow-up
    named in-line at audit.py:1902).
  payoff class: LARGE (per-commit wall time) · measure-first: P-3 — the ranking decides which
    checks are worth the commit tier.

P-5 · Shared corpus loader with git-blob-sha caching (hub-owned, consumer-inherited)
  done-when: one enumeration + one read of the `.md` corpus per process, memoized on blob sha;
    the >=8 walk sites in B5 and the whole-file-for-2KB read at B6 consume it.
  payoff class: MEDIUM-LARGE, and the only one that scales with corpus size · measure-first:
    P-3 + step 4 utilization capture (if the run is CPU-saturated, not I/O-stalled, this drops
    in priority below P-4).

P-6 · Arm the test tier so the approved per-merge cadence has a selector
  done-when: every test spawning a subprocess or interpreter carries `slow` (59 files today
    do not); `-m "not slow"` is the documented per-merge cadence; full suite once at
    integration; PLAYBOOK Ch5 carries the authoring rule. Fix B10 (`-o addopts=` at
    validate_doc_claims.py:137) in the same arc.
  payoff class: LARGE on the per-merge loop · measure-first: step 3 `--durations=25` — if the
    suite is long-pole rather than long-tail, fix the poles instead and narrow this row.

NOT PROPOSED, deliberately: "parallelize audit.py" (already shipped and armed — B8);
"rewrite in a faster language" (the brief's own ordering puts it last, and B1/B2/B5 say the
Python is doing avoidable work, not slow work); adding diskcache/joblib/testmon as fleet
dependencies before P-3 says they are needed.
