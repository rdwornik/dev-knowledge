# W2A — perf-core: killing the per-commit anchor tax ([#587] + [#588])

> Lane report. Batch W2, lane `w2a-perf-core`, branch `worktree-w2a-perf-core`, LOCAL worktree,
> gates armed. Contract: `W2A-perf-core.md` (frozen). Evidence input:
> `docs/audits/2026-08-26-technical-perf-recon.md` (PERF-RECON, rows B1/B2/B3).
> Commits: `e806376e` ([#587]), `0839de97` ([#588]), this report.

## Headline

`check_journal_spine_anchor` went from **197.8 s and rank 1 of 46** to **7.1 s and rank 8**, a
**27.9x** cut on the quietest measured run — and it did so with **byte-identical findings**,
proved rather than asserted. The check is no longer the bound on `audit.py health`.

The lane's stated target — health **< 60 s** — was **NOT met**: the run is now bound by a
different check, `check_review_artifact_coverage` (128.4 s, 42.4% of check time), which this
lane's contract explicitly forbids chasing. That residual is named in §5 and belongs to
[#597]'s tiering work.

## 1. Substrate honesty

Every number below was produced on the operator's Windows workstation by the command the
contract names, with the [#529] telemetry switch on:

```
DEV_KNOWLEDGE_TELEMETRY=1 PYTHONUTF8=1 uv run --locked python scripts/audit.py health --parallel
```

Three sibling lane worktrees (`prompts-revocation`, `w2b-surfaces`, `w2c-codespace-repair`)
existed on disk throughout, and `main` MOVED under this worktree mid-lane — a concurrent lane
merged `ac677b6e` onto it. Two consequences, both stated rather than smoothed over:

- **Host contention is a confound in the wall-times, not a controlled variable.** The three
  health runs were taken under different ambient load (run 2 overlapped this session's own test
  and parity jobs; run 3 was the quietest). Cross-run comparisons of the OTHER checks therefore
  carry scheduling noise, and §5 reports all three runs rather than the flattering one.
- **The byte-identity proof does NOT use a before-run and an after-run.** A moving `main` would
  let an unrelated merge masquerade as a behaviour change. Instead the harness loads the
  pre-change module and the post-change module side by side in ONE process against ONE working
  tree — see §4.

## 2. Step 0 — the baseline, and the precondition it had to clear

The contract's P-3 precondition was: if `check_journal_spine_anchor` is not at or near the top
of the per-check ranking, STOP and report. It was **rank 1**. Telemetry run
`f0caf15a50ec4e0b8108b992d88535f1`, wall **210,135 ms**, 46 checks, sum of `duration_ms`
**564,383 ms** (the sum exceeds wall because the runner is an 8-wide thread pool).

```
rank   duration_ms   share   check
   1        197808   35.0%   check_journal_spine_anchor      <-- the lane's target
   2        178298   31.6%   check_review_artifact_coverage
   3         41460    7.3%   check_doc_code_edge
   4         30782    5.5%   check_handoff_probes
   5         25686    4.6%   check_reconciled_versions
   6         24429    4.3%   check_undeclared_edges
   7         16147    2.9%   check_fleet_parity
   8          7597    1.3%   check_task_tree_coherence
   9          7236    1.3%   check_funnel_coverage
  10          5422    1.0%   check_doc_structure
 ...          <=4459   <1%   the remaining 36 checks
```

Two of the top two walk the same first-parent spine and both reach `journal_anchor.introduced`.
That is why one module's repair moves two rows.

## 3. What changed

**[#587] — the single-pass anchor index (`e806376e`).** Both consumers asked their question ONCE
PER INTRODUCED COMMIT and each asking re-walked a 2.9 MB journal: `mention_not_record_warnings`
looped introduced-commit -> entry -> `entry.splitlines()` (the split was memoized by [#533],
the *line* split was not, so every outer iteration re-allocated the whole file), and
`is_anchored` substring-scanned the same text per commit. `_anchor_index(journal)` now builds
`{7-char lowercase-hex short -> (present, recorded)}` in ONE memoized pass over the same
`_entries(journal)` -> `entry.splitlines()` sequence the old inner loop walked; both consumers
read it with set lookups. O(commits x journal) becomes O(journal) + O(commits).

The keys are every 7-char lowercase-hex SUBSTRING, not every hex token, and that distinction is
the whole correctness argument: `0badf00dcafe` contains six distinct 7-char windows, and a
tokenizer would miss a short prefix sitting mid-run — reporting a spine entry UNANCHORED that is
anchored, on a gate that refuses pushes. A needle outside the hex domain falls back to the
pre-inversion scan, so the equivalence is total rather than conditional on what today's callers
happen to pass.

**[#588] — one git process for the whole spine (`0839de97`).** `introduced` spawned TWO
`git rev-list` processes per unique spine entry; the module's own docstring already recorded 808
spawns and 116.8 s in a single health run, and after [#587] that was ALL that remained of the
check. One `git rev-list --parents --timestamp --all` now builds the entire parent map plus each
commit's date, and `firstparent..sha` is a graph walk in Python. Process count per health run is
**O(1)** in the length of the spine.

Trust in the map rests on the immutability argument `introduced` already used: what a commit
introduced is fixed forever by its own hash. A SHA present in the map has an answer that cannot
go stale; a SHA absent is a MISS (the snapshot predates the commit), so the map rebuilds once
and then believes itself; a SHA still absent is unreachable from every ref and falls back to
git. Every case the map cannot answer with certainty defers to git rather than guessing —
including a map that is not ancestry-closed where the walk needs it, because a truncated
exclusion walk yields a TOO LARGE introduced set, and a too-large set reports a spine entry
ANCHORED that is not.

**The version of [#588] that was wrong, recorded because it looked right.** The first
implementation ordered the introduced set by each commit's index in the global `--all` output.
That reproduces git exactly whenever commit dates are DISTINCT and diverges the moment they tie
— and they tie constantly, because git stamps at one-second granularity and a scripted burst of
commits lands inside one second. Measured on a synthetic repo whose commits share a timestamp:
**3 of 5** spine entries came back in a different order, git putting the merge first where the
global index did not. It passed a hand-made fixture and failed a machine-made one. The walk is
now git's own rule — a commit-date priority queue seeded with `sha`, newest-first, ties broken
by insertion order (`commit_list_insert_by_date` inserts AFTER equals), with a `queued` set
standing in for git's ADDED flag. Same synthetic repo after the fix: **0 divergences**.

Order is not cosmetic here: `mention_not_record_warnings` emits one string per introduced commit
in `introduced`'s order, and `check_journal_spine_anchor` joins the FIRST FIVE into its WARN
evidence. Reproducing git's order is part of the answer.

## 4. Byte-identity — the row's own done-when, proved

A harness loads the pre-[#587] module and the post-[#588] module into ONE process and runs the
exact scan the check runs (`floor..main`, minus the floor itself), comparing every observable
the check consumes. 312 spine entries above the ADR-85 floor `24882f8cc`, 1,499 introduced
commits, `JOURNAL.md` = 2,952,618 bytes.

```
observable                                     before   after   verdict
spine entries                                     312     312   IDENTICAL
unanchored list (the FAIL evidence)                 1       1   IDENTICAL
mention-not-record warnings (the WARN evidence)   646     646   IDENTICAL  (order included)
introduced() per spine entry                   1499 c  1499 c   IDENTICAL  (order included)
                                                               VERDICT: BYTE-IDENTICAL
```

Compared as LISTS and never as sets, deliberately — order is output. The oracle for
`introduced` is `_introduced_uncached`, i.e. git's own answer, which is kept in the module as
the fallback precisely so it stays the definition the optimisation is measured against.

In-process leg timings from that same harness, single-threaded:

```
leg                    pre-#587      #587 alone      #587+#588
is_anchored            125.945 s       82.577 s        1.158 s
mention_not_record      18.445 s        0.003 s        0.003 s
```

(The pre-#587 `is_anchored` figure differs between the two harness runs — 97.4 s in the first,
125.9 s in the second — because both were taken under different ambient load. It is a
subprocess-spawn cost, so it moves with host contention; the AFTER figure, which spawns nothing,
does not.)

**A second, wider identity check, at the level a reader of the gate actually sees.** The harness
above compares the four values the check consumes. The whole `audit.py health` finding stream
was also compared, baseline run vs post-change run — all **144** `[OK]`/`[!!]`/`[~~]`/`[--]`
lines across all 46 checks, sorted and diffed:

```
diff baseline-checks.txt after2-checks.txt   ->   no differences (144 lines each)
```

Same single `[!!]`, same 100-plus `[~~]` advisories, same `[--]` skips, same evidence strings —
including the `journal_spine_anchor` WARN line, whose text is the join of the FIRST FIVE
mention-warnings and would therefore have moved on any ordering change. Nothing in the gate's
output moved; only its cost did.

## 5. Step 3 — the re-measure, and the target that was missed

```
run                              wall_ms   sum(duration_ms)   spine_anchor   review_artifact
f0caf15a  baseline (pre-lane)     210135             564383    197808 (#1)     178298 (#2)
00859409  after both commits      173133             429348     11973 (#9)     161508 (#1)
db4aeea2  after, quietest host    140149             302693      7086 (#8)     128428 (#1)
```

- **The check this lane owns: 197,808 ms -> 7,086 ms, rank 1 -> rank 8. A 27.9x cut.**
- Wall-time: 210.1 s -> 140.1 s. **Target `< 60 s`: MISSED.**
- The two after-runs bracket the answer rather than agreeing on it, and the difference between
  them is host load, not code. Reported both ways rather than picking the better one.

**The residual top check, named and NOT chased** (contract: "do not chase it — that is [#597]'s
tiering work"): `check_review_artifact_coverage`, **128,428 ms, 42.4% of check time, rank 1**.
It is now the Amdahl bound on the whole run — wall 140.1 s against its own 128.4 s leaves almost
nothing else to remove. It did get faster as a side effect (178.3 -> 128.4 s), because it calls
the same `journal_anchor.introduced` and shares its memo; what remains is its OWN per-spine-entry
git spawns (`rev-list --parents -n 1`, `diff --name-only`, `log -1 --format=%s`), which are the
same B2 shape one module over and which this lane's contract puts out of scope.

## 6. Tests

No existing assertion was weakened or deleted. Four spawn-count assertions were RE-POINTED to
the smaller number the batch makes true (2 -> 1 read for one SHA, 4 -> 1 for two SHAs, 4 -> 2 for
two repos), which is a strengthening; the moving-ref refusal (2 reads EVERY time, never
memoized) and the never-cache-an-exception assertions are untouched.

Added, 21 test functions across the two arcs:

- **[#587]** — window enumeration inside a long hex run (the tokenizer trap); the
  present/recorded split; byte-identity against an INDEPENDENTLY RESTATED pre-inversion body
  across 10 journal shapes; a behavioural "the journal is walked ONCE regardless of commit
  count" guard; memo bounding and content-keying; the non-object-name fallback; and a
  both-directions agreement test against the live 2.9 MB `JOURNAL.md`.
- **[#588]** — ONE git process for a 200-entry spine (counted, not inferred); the unreachable-SHA
  fallback with its exact four-read sequence; the not-ancestry-closed deferral; whole-spine list
  equality against `_introduced_uncached` on a real multi-merge repo; and a commit made AFTER the
  map was built (the staleness hazard).
- **Terra follow-up (§11)** — a static shallow clone produces zero map-vs-git divergence, and a
  view that moves under the snapshot fails CLOSED (strict subset, and the predicate refuses).

The per-file counts below are the pre-terra run; the two §11 tests were added after it and are
counted in the post-review re-run recorded in that section.

```
tests/test_journal_anchor.py                       71 passed
+ test_adr85_integration_enforcement.py
+ test_batch_manifest.py
+ test_review_artifact_coverage.py                161 passed, 1 skipped, 1 xfailed  (-n 0, 488 s)
ruff check scripts/journal_anchor.py tests/test_journal_anchor.py    clean
```

Per the batch cadence the FULL suite is the integrator's, run once at integration; this lane ran
the targeted files covering its diff.

## 7. Honest limits

- **The <60 s target is not met and this lane cannot meet it.** One module was in scope; the
  bound is now in another check. Nothing here should be read as "the per-commit tax is fixed".
- **`--all` is the map's scope, so a SHA reachable from no ref falls back to the two-spawn git
  path.** Correct, but not batched — a detached-HEAD caller pays the old cost. No caller in this
  repo is in that shape today.
- **`_MAP_GENERATION` is unbounded** (one small int per repo-path string seen in a process). It
  is the cheapest thing in the module to leave unbounded and is named in the source rather than
  left for a reader to find.
- **The map is trusted for what it contains, and a rebuild only fires on a MISS.** If git's
  `--parents --timestamp --all` ever emitted an ancestry-open graph for a reachable SHA, the walk
  defers to git rather than answering — but it would do so silently, one SHA at a time.
- **The snapshot is of git's reported VIEW, not of the object graph**, and a view moves under a
  shallow deepen or a `replace`/graft ref. Measured (§11): a static shallow clone produces zero
  divergence, and a mid-process deepen makes the stale snapshot UNDER-report, which fails CLOSED.
  The residual is a graph-view mutation inside one gate process, which `_introduced_tuple`'s memo
  has been exposed to since [#533] and which this row cannot close without undoing itself.
- **The order reconstruction is validated, not proved.** It matches git on 1,499 live commits
  across 312 spine entries, on a synthetic all-ties repo, and on a multi-merge fixture. It is a
  reimplementation of a heuristic traversal, and the parity tests are what keeps it honest.
- **The telemetry `duration_ms` values are measured inside an 8-wide thread pool on a contended
  host.** The target check's 197.8 -> 7.1 s is far outside that noise; the other checks' run-to-run
  movement is not, and is not claimed as a result.

## 8. Declared bypasses

Both code commits carry `SKIP=audit-health`, with ownership proved rather than claimed.
`check_journal_spine_anchor` FAILs on `ac677b6edbf6ebf4df86660d121782c316459fb4` — "Merge branch
'worktree-prompts-revocation'", a CONCURRENT lane's merge onto `main`.

- **(a) Not mine:** `git merge-base --is-ancestor ac677b6e HEAD` -> false.
- **(b) Not lane tree-lag:** the gap is present with BOTH this worktree's `JOURNAL.md` and
  `main`'s own (`git show main:JOURNAL.md`), so the sync-merge remedy would buy nothing.
- **(c) Not exemptible:** no `docs/audits/*-batch-*-manifest.md` declares an open batch, so the
  ADR-110 declared-integration-arc exemption is unavailable.

`SKIP` drops ONE hook; ruff, the ADR-101 hermetization gate, the provider-registry gate and both
commit-msg gates ran on every commit. `--no-verify` was not used anywhere in this lane.

## 9. Environment note for the integrator

`uv` resolved to **0.12.6** on one invocation mid-lane and to the pinned **0.11.19** on the next,
from the same shell and directory. Two `uv` binaries are on PATH — `~/.local/bin/uv.exe`
(0.12.6, dated 2026-08-25) and the WinGet package (0.11.19) — and `pyproject.toml` pins
`required-version = "==0.11.19"`, so whichever wins decides whether `uv run --locked` runs at all
(the 0.12.6 resolution fails outright: "Required uv version `==0.11.19` does not match"). It was
transient here and a retry cleared it. Flagged, not fixed: a uv bump is its own gated change
(CLAUDE.md §4), and this is outside the lane's frozen scope.

## 11. Step 4 — terra review

`gpt-5.6-terra` (pinned), code profile, diff `852e145c..HEAD`, high reasoning effort, focus
hints on the false-clean direction, the two equivalence questions, cache staleness and the
fail-closed posture. Artifact: `docs/audits/2026-08-26-codex-w2a-perf-core.md`.

```
tally (counted from the artifact's findings section, not the console tail)
  Critical 1   High 0   Medium 0   Low 0
```

**The one finding: `journal_anchor.py:265`, "parent-map cache can return a stale Git graph".**
MECHANISM CONFIRMED, CONSEQUENCE REFUTED — and the refutation is a measurement, not an opinion.

The mechanism is right and was accepted: a rebuild fires on a MISS, so a SHA already in the
snapshot is answered from it for the life of the process, and git reports a *view* that a
shallow deepen or a `replace`/graft ref can move. The stated consequence — a too-large set
returning ANCHORED and letting an unanchored push through — was tested and runs the other way:

- **A static shallow clone produces ZERO divergence.** `git rev-list firstparent..sha` is
  truncated at the same boundary the map is; truncation is git's answer, not the batch's.
- **A deepen mid-process makes the stale snapshot UNDER-report** — 2 missing, 0 extra on the
  fixture, a strict SUBSET. `is_anchored` is `any(...)` over that set, so a subset can only turn
  TRUE into FALSE: the gate reports UNANCHORED and REFUSES. Fail-CLOSED, which is the direction
  this module's whole posture demands.

**Fix taken:** not in code, and the reason is that the code fix would undo the row — detecting a
view mutation costs a git read PER CALL, which is the per-SHA spawn [#588] exists to remove.
Instead: the limit is named at `_spine_map_for` with its measurement attached, and both halves
of the measurement are now tests (`test_a_shallow_clone_does_not_make_the_map_disagree_with_git`,
`test_a_view_that_moves_under_the_snapshot_fails_CLOSED`) so the direction claim is checkable
rather than asserted. The residual — a `replace`/graft ref created inside the seconds-long
lifetime of a gate process — is **not new**: `_introduced_tuple`'s memo has fixed answers for a
whole process since [#533].

Nothing at High/Medium/Low, so no other ≥medium fix was owed. Two comment-level improvements
landed in the same commit because the review's focus surfaced them: the two cache ceilings now
carry MEASURED sizes (index 5,278 + 457 keys, order 0.4 MB; parent map 5,995 commits / 7,329
edges, order 1 MB) instead of adjectives, and `_MAP_GENERATION` now records that
`audit.run_checks` reaches `introduced` from concurrent THREADS — where a lost update can cost
an extra git process and never a wrong answer, because the map is only used after
`sha in smap.parents` is re-checked on whichever map came back.

Post-review re-run, same four files, `-n 0`: **163 passed, 1 skipped, 1 xfailed** (592.41 s),
`ruff check` clean.

## 12. Scope discipline

Touched: `scripts/journal_anchor.py`, `tests/test_journal_anchor.py`, this report. Not touched:
any other check, `scripts/validate_no_ff.py` (named in [#588]'s refs but outside the contract's
frozen scope), `BACKLOG.md`, `tasks/`, tier work ([#597]). Nothing was merged.
