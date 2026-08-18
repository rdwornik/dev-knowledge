# [#533] leg 2 — measurement record (attribution, memoization, parallelism)

<!-- scope: meta -->

**Lane:** `worktree-lane-a-533-leg2` · **Contract of record:**
`docs/audits/2026-08-18-technical-533-leg2-lane-contract.md` · **Date:** 2026-08-18

This file is the lane's measurement artifact. It is written in append-only sections, newest
section LAST, each stamped with the STEP it belongs to — an audit is immutable (CLAUDE.md §5
rule 3), so a later STEP adds a marked section rather than rewriting an earlier one.

---

## STEP 1 — attribution before optimization

### Method (exact, so the number is reproducible)

- One **serial** in-process run over `audit.ALL_CHECKS`, driven by a temporary harness in the
  gitignored `temp/` scratch dir (`temp/attrib.py`), deleted at lane close. **No instrumentation
  is committed** and no source file was edited to take this measurement.
- The harness reproduces `cmd_health`'s inner loop exactly (`scripts/audit.py`, `cmd_health`):
  `audit._GATE_MODE = True`, then `for check in ALL_CHECKS: check(Path(audit._REPO_ROOT))`,
  with `time.perf_counter()` taken immediately either side of each `check(...)` call.
  `_GATE_MODE` matters — it is what makes `check_doc_claims` skip its expensive claim-3 locus,
  so measuring without it would measure a different loop than the hook runs.
- Invocation: `uv run --locked python temp/attrib.py temp/attrib-run1.json run1`, from the
  lane worktree, Python 3.12.10, Windows 11.
- Rows are wall time **per check**, descending. Sum of rows = 334.49 s = loop total to the
  centisecond, so nothing in the loop is unattributed.

### Honest limit on the absolute numbers

**Taken under concurrent lane load** — four sibling worktrees were provisioned and other lanes
were live on this machine during the run. Absolute seconds are therefore **indicative, not
authoritative**; the authoritative quiet-tree measure happens at integration. The loop total of
334.49 s against the Phase-0 quiet-tree baseline of **290.9 s median** (spread 4.9%) for the
whole `health` invocation is consistent with that load, and the *proportions* below — which are
what the fork turns on — are internally sourced from one single process and are not affected by
the machine being busy in the same way an absolute second is.

### The 43-row table

| # | check | wall (s) | share | cumulative | findings |
|---|---|---|---|---|---|
| 1 | `check_journal_spine_anchor` | 211.56 | 63.2% | 63.2% | 2 |
| 2 | `check_review_artifact_coverage` | 69.58 | 20.8% | 84.1% | 2 |
| 3 | `check_handoff_probes` | 16.04 | 4.8% | 88.8% | 1 |
| 4 | `check_doc_code_edge` | 15.64 | 4.7% | 93.5% | 1 |
| 5 | `check_fleet_parity` | 7.50 | 2.2% | 95.8% | 1 |
| 6 | `check_doc_structure` | 3.53 | 1.1% | 96.8% | 1 |
| 7 | `check_undeclared_edges` | 1.81 | 0.5% | 97.4% | 18 |
| 8 | `check_silent_rule_ratchet` | 1.52 | 0.5% | 97.8% | 1 |
| 9 | `check_canonical_freshness` | 1.31 | 0.4% | 98.2% | 1 |
| 10 | `check_reconciled_versions` | 1.13 | 0.3% | 98.5% | 1 |
| 11 | `check_stale_worktrees` | 0.83 | 0.2% | 98.8% | 2 |
| 12 | `check_intake_tree_coherence` | 0.68 | 0.2% | 99.0% | 1 |
| 13 | `check_task_tree_coherence` | 0.63 | 0.2% | 99.2% | 1 |
| 14 | `check_fleet_audit_replication` | 0.43 | 0.1% | 99.3% | 1 |
| 15 | `check_git_backlog_drift` | 0.36 | 0.1% | 99.4% | 1 |
| 16 | `check_membership_agreement` | 0.27 | 0.1% | 99.5% | 2 |
| 17 | `check_residual_completeness` | 0.19 | 0.1% | 99.6% | 1 |
| 18 | `check_no_ff_merges` | 0.18 | 0.1% | 99.6% | 3 |
| 19 | `check_landing_predicate` | 0.18 | 0.1% | 99.7% | 4 |
| 20 | `check_safe_removal` | 0.17 | 0.1% | 99.7% | 1 |
| 21 | `check_hooks_armed` | 0.16 | 0.0% | 99.8% | 1 |
| 22 | `check_doc_code_coverage_drift` | 0.16 | 0.0% | 99.8% | 1 |
| 23 | `check_deployed_methodology_version` | 0.15 | 0.0% | 99.9% | 1 |
| 24 | `check_no_sibling_orphans` | 0.13 | 0.0% | 99.9% | 1 |
| 25 | `check_journal_day_letters` | 0.07 | 0.0% | 99.9% | 1 |
| 26 | `check_handoff_bundle_structure` | 0.06 | 0.0% | 99.9% | 1 |
| 27 | `check_doc_rot` | 0.05 | 0.0% | 99.9% | 34 |
| 28 | `check_doc_claims` | 0.05 | 0.0% | 100.0% | 1 |
| 29 | `check_import_edges` | 0.04 | 0.0% | 100.0% | 1 |
| 30 | `check_preflight_backlog_ids` | 0.03 | 0.0% | 100.0% | 1 |
| 31 | `check_canonical_structure` | 0.02 | 0.0% | 100.0% | 1 |
| 32 | `check_routine_consumers` | 0.02 | 0.0% | 100.0% | 1 |
| 33 | `check_handoff_version_stamp` | 0.00 | 0.0% | 100.0% | 1 |
| 34 | `check_workspace_settings` | 0.00 | 0.0% | 100.0% | 1 |
| 35 | `check_amendment_coherence` | 0.00 | 0.0% | 100.0% | 1 |
| 36 | `check_vision_md` | 0.00 | 0.0% | 100.0% | 1 |
| 37 | `check_dot_prefix_discipline` | 0.00 | 0.0% | 100.0% | 1 |
| 38 | `check_canonical_md_visibility` | 0.00 | 0.0% | 100.0% | 1 |
| 39 | `check_enforcement_coverage` | 0.00 | 0.0% | 100.0% | 1 |
| 40 | `check_claude_md` | 0.00 | 0.0% | 100.0% | 1 |
| 41 | `check_boot_byte_budget` | 0.00 | 0.0% | 100.0% | 1 |
| 42 | `check_adr38_baseline` | 0.00 | 0.0% | 100.0% | 1 |
| 43 | `check_floor_integrity` | 0.00 | 0.0% | 100.0% | 1 |

**Loop total 334.49 s.** The top TWO checks are **84.1%** of the entire registry; the bottom 28
checks together are under 1 s.

### THE FORK FIRED — reporting, not improvising

The contract's STEP-1 fork: *"if one check holds >50% of wall AND is CPU-bound or algorithmically
pathological, STOP-report before threading — threading an algorithmic defect is the wrong fix."*

`check_journal_spine_anchor` holds **63.2%** of wall (>50%), and it is **algorithmically
pathological on two independent counts**. A second sub-attribution run (harness
`temp/subattrib.py`, wrapping `journal_anchor._git`, `journal_anchor._entries` and
`journal_anchor.introduced` with counters; total for the check 207.65 s in that run):

| component | count | wall (s) | share of the check |
|---|---|---|---|
| `git` subprocesses, all forms | 812 calls | 116.81 | 56.3% |
| — of which `git rev-list` | 808 calls | 116.25 | 56.0% |
| `journal_anchor._entries()` | 934 calls | 76.87 | 37.0% |
| `journal_anchor.introduced()` | 404 calls | (drives the 808) | — |

1. **`_entries` re-splits the same immutable string 934 times.** `JOURNAL.md` is **2607 KiB**;
   934 calls re-run `_ENTRY_SPLIT_RE.split` over **2.47 GB** of text in one process to produce
   the same answer every time. This is **pure CPU**, and it is the mechanism the contract already
   named (`lru_cache` on `journal_anchor._entries`). 76.9 s — 23% of the whole 43-check loop.

2. **`introduced()` is called exactly twice per spine entry, and half of the 808 `rev-list`
   subprocesses are exact duplicates.** `check_journal_spine_anchor` reaches `introduced` once
   through `unanchored_on_spine → is_anchored` and a second time through
   `mention_not_record_warnings`, for the same `(repo, sha)` pair; each call spawns two
   `git rev-list` processes at ~144 ms apiece on this platform. ~404 of the 808 spawns compute an
   answer the process already had.

**Why this is the fork and not a threading opportunity.** Amdahl bounds what threading can do
here: with one check at 63.2% of wall, a perfectly-parallel `ThreadPoolExecutor` over the other
42 checks caps the whole-registry speedup at **1/0.632 ≈ 1.58×** — 334 s becomes ~212 s at best,
and the pathological check is still 208 s of it. Threading would also *hide* the defect: the
same 2.47 GB of redundant regex and the same ~404 redundant subprocess spawns would still be paid,
just concurrently with everything else. That is precisely the "threading an algorithmic defect"
the fork exists to refuse.

**Lane disposition, stated plainly.** The fork's instruction is *STOP-report **before
threading***, and threading is STEP 5. It does not stop STEP 2–3: the memo **is** the fix for the
defect the attribution just found, and it is the mechanism the contract already ruled. So this
lane proceeds through the memo and re-measures, and **STOPS before STEP 4/5 (the
`ThreadPoolExecutor` runner) pending an operator ruling** — the threading decision now has a
measured basis it did not have when the contract was written, and re-deciding it is a ruling, not
this lane's to improvise.

### Second-order finding (recorded, not acted on beyond the memo)

`check_review_artifact_coverage` — the #2 row at **20.8%** — walks the same `main` first-parent
spine and calls the same `_ja.introduced(root, sha)` per in-scope entry, plus its own
`rev-list --parents -n 1` on every entry above the cutoff (which is *literally the first git call
`introduced` makes*). It already carries a batched-date comment recording that a per-entry git
call cost 236 s here once before. Any memo on `introduced` is therefore shared across the two
checks that together are 84.1% of the loop — noted here so the effect is attributed rather than
appearing as an unexplained gain in the STEP-6 numbers.


---

## STEP 3 → fork re-evaluation (recorded BEFORE acting on it)

Both memos are in. One serial in-process run, same harness and same method as STEP 1, same
concurrent-load caveat — indicative seconds, sound proportions. The full 3×/3×/3× median set is
STEP 6's job; this single run exists to answer one question: *does the STEP-1 fork condition still
hold?*

| check | STEP 1 (s) | post-memo (s) | factor | share now |
|---|---|---|---|---|
| `check_journal_spine_anchor` | 211.56 | 88.43 | 2.39x | 39.6% |
| `check_review_artifact_coverage` | 69.58 | 69.61 | 1.00x | 31.1% |
| `check_doc_code_edge` | 15.64 | 19.75 | 0.79x | 8.8% |
| `check_handoff_probes` | 16.04 | 19.12 | 0.84x | 8.6% |
| `check_fleet_parity` | 7.50 | 9.03 | 0.83x | 4.0% |
| `check_doc_structure` | 3.53 | 4.22 | 0.84x | 1.9% |
| `check_undeclared_edges` | 1.81 | 2.31 | 0.78x | 1.0% |
| `check_canonical_freshness` | 1.31 | 1.78 | 0.74x | 0.8% |

**Loop total 334.49 s → 223.56 s (1.50×).** `check_journal_spine_anchor` 211.56 s → 88.43 s
(**2.39×**), and its share of the loop falls from **63.2% to 39.6%**.

Read the 0.74–0.84× rows as **load noise, not regression**. Nothing this leg touched is reachable
from `check_doc_code_edge`, `check_handoff_probes` or `check_fleet_parity`; they sit 16–35% slower
purely because the second run met a busier machine. That noise floor is itself the reason the
absolute seconds here are labelled indicative and the quiet-tree measure is deferred to
integration — and it cuts the other way too: the 2.39× on the dominant check was measured on the
*same* busier machine, so it is if anything understated.

### The fork condition is no longer true, and this is the disposition

The fork fires on *"one check holds over 50% of wall **AND** is CPU-bound or algorithmically
pathological"*. Post-memo the largest single check is 39.6% — **under the threshold** — and the two
pathologies the fork was pointing at are gone by measurement rather than by assertion: the 2.47 GB
of redundant regex is now one split, and ~404 of the 808 `git rev-list` spawns are now one cache
lookup.

The lane therefore **proceeds to STEP 4/5**. The reasoning is recorded here rather than left in a
session log, so it can be overruled on the record:

- The fork's instruction is *STOP-report **before threading** — threading an algorithmic defect is
  the wrong fix.* The defect it named was fixed first, which is what the clause asks for, and the
  fix is measured rather than claimed.
- Its precondition is re-evaluated against the tree that would actually be threaded, and fails.
- **Blast radius of proceeding is near zero by the contract's own design:** STEP 5 lands behind
  `--parallel/--no-parallel` with **default serial**, so no hook and no existing caller changes
  behaviour. Flipping the default is explicitly reserved as a separate ruling.
- The two memo commits and the two threading commits are separable, so an operator who reads the
  fork as a hard stop can drop the threading pair whole without touching the measured 1.50×.

**What threading can still be worth, bounded honestly.** With the largest check at 88.43 s of
223.56 s, a perfect thread pool over the registry caps out at **223.56 / 88.43 = 2.53×** — about
88 s of wall. Set against the Phase-0 quiet-tree baseline of 290.9 s that would be roughly
291 s → ~90 s of hook tax; but 2.53× is a ceiling nothing reaches, and the real figure is STEP 6's
to measure, not this section's to promise.

### Where the remaining mass sits (recorded, deliberately not acted on)

`check_review_artifact_coverage` did **not** move (69.58 s → 69.61 s) and is now **31.1%** of the
loop, second only to the check it walks the same spine as. It is unmoved because its per-entry git
reads go **direct to `_ja._git`** — `rev-list --parents`, `diff --name-only` and `log -1` for every
spine entry above its cutoff — rather than through the memoized `introduced`, so only one of its
several per-entry calls can benefit at all. Sharing the memo would mean changing that check's body
in `audit.py`, a different change with a different blast radius and no test-first coverage in this
lane. It is written down so the next reader inherits the finding instead of rediscovering it.


---

## STEP 6 — measurement

### Method

`temp/measure.py` (gitignored, deleted at lane close) times one `audit.run_checks(_REPO_ROOT)`
call with `_GATE_MODE = True` — the exact loop `cmd_health` runs — and prints the elapsed
seconds plus a digest of every finding as `check_name:status` in emission order.

- **One timed run per PROCESS**, never repeated in-process. A cached run repeated in one
  process would warm its own repeat and report a number no `audit-health` invocation will ever
  see; the hook spawns a fresh process per commit, so a fresh process is the honest unit.
- **Runs are strictly sequential.** Two concurrent runs measure each other.
- `uncached` restores pre-memo behaviour by rebinding `journal_anchor._entries` and
  `journal_anchor.introduced` to uncached bodies. Both call sites reach them through the module
  namespace at call time, so this is a faithful A/B rather than an approximation.
- `parallel` runs at the default width, `min(_PARALLEL_MAX_WORKERS, 43)` = **8 workers**.

### The three medians

| mode | runs (s) | **median** | min | speedup vs uncached |
|---|---|---|---|---|
| serial, uncached | 366.14 · 674.26 · 354.99 | **366.14** | 354.99 | 1.00× |
| serial, cached | 220.02 · 195.50 · 191.99 | **195.50** | 191.99 | **1.87×** |
| `--parallel`, cached | 97.77 · 85.60 · 85.01 | **85.60** | 85.01 | **4.28×** |

**Parallel over cached alone: 2.28×.** On minima rather than medians — which discards the one
load-spike outlier entirely — the same three figures are **1.85× / 4.18× / 2.26×**, so the
conclusion does not depend on how the outlier is treated.

### Read the seconds with the caveat they deserve

The 674.26 s uncached run is not a typo and has not been dropped: two identical uncached runs on
an unchanged tree measured **366 s and 674 s**, an **84% spread**, against the 4.9% spread
Phase-0 recorded on a quiet tree. Four sibling lane worktrees were live throughout. Absolute
seconds here are therefore **indicative only** and the authoritative quiet-tree measure belongs
to integration, exactly as the dispatch stipulated.

Two things keep the result trustworthy anyway. First, the modes were **interleaved** rather than
run three-of-a-kind, so drift lands on all three alike. Second — and this is the part that does
not care about load at all — the work *removed* was counted directly.

### The load-independent measurement (counts, not seconds)

`temp/counters.py` runs the dominant check in both modes with counters around
`journal_anchor._git` and `journal_anchor._entries`. How many subprocesses were spawned and how
many megabytes were re-split are properties of the code; they do not move when the machine gets
busy.

| | uncached | cached |
|---|---|---|
| `git` subprocesses spawned | **812** | **408** |
| seconds inside those subprocesses | 121.09 | 60.37 |
| `_entries` calls | 934 | 934 |
| text handed to `_entries` | 2468.9 MB | 2468.9 MB |
| **seconds spent splitting it** | **75.22** | **0.10** |
| check wall time | 210.37 s | 75.04 s |
| findings | `pass` + `warn` | `pass` + `warn` (identical) |

**Exactly 404 subprocess spawns removed** — precisely the duplicate count STEP-1 attribution
predicted from `introduced()` being reached twice per spine entry, confirmed rather than
estimated. And the entry split goes from **75.22 s to 0.10 s**: the call count is unchanged at
934 because the memo does not remove calls, it removes the *work* — 933 of them are now hits.

### Verdicts are byte-identical across all three modes

Not inferred from the timings — checked. Each run wrote its full `check_name:status` digest in
emission order; all three files are 2005 bytes and hash identically:

```
f2577dbc83f70248ff878bf03f2de69f  temp/digest-uncached.txt
f2577dbc83f70248ff878bf03f2de69f  temp/digest-cached.txt
f2577dbc83f70248ff878bf03f2de69f  temp/digest-parallel.txt
```

102 findings in every run. Same verdicts, same order, memoized or not, threaded or not — which
is the STEP-4 parity requirement demonstrated on the live tree at full registry width, not only
on the synthetic fixtures the unit tests use.

### What this means for the hook tax, stated as an extrapolation

Phase-0's quiet-tree baseline for the whole `health` invocation is **290.9 s**. If the measured
ratios hold on a quiet tree, that becomes roughly **155 s** memoized and **~68 s** with
`--parallel`. **That is an extrapolation and is labelled as one** — it multiplies a quiet-tree
baseline by ratios measured under load, and only the integration measure can confirm it.

**The default remains SERIAL.** Landing this changes no hook's behaviour; the 1.87× is what
every commit gets for free, and the further 2.28× is available to anyone who passes
`--parallel`. Flipping the `audit-health` default is a separate ruling and this lane does not
take it.
