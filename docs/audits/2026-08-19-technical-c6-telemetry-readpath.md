# C6 — the telemetry READ path: the data contract, the D3-first page, the stack ruling, and the build lane

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, and births no BACKLOG row.
> No config file, dependency, hook, workflow or protocol was edited by the lane that produced it.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-19
- **Lane:** CLOUD C6 · read-only + drafts · branch `claude/c6-telemetry-readpath-memo`
- **Dispatch stamp:** `docs/audits/2026-08-19-technical-c6-telemetry-readpath-contract.md` (commit `5d7c486`)
- **Reads the tree at:** `4541155` (`main` = `origin/main` at lane start), which contains the
  `[#533]` leg-2 decomposed runner and the `tasks/` strangler tree. The emit side is read as it
  now exists — **library only, zero call sites** — not as lane L2 will leave it.
- **Spec of record consumed:** `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md` (night N1)
- **Predecessor NOT re-litigated:** `docs/audits/2026-08-16-technical-nb4-telemetry-read.md` (night-batch-4
  lane B). NB4 already evaluated the stack, designed three dashboards and ruled the home. **This memo
  advances it and does not repeat it.** Where a finding of NB4's is re-measured here it says so, and
  where this lane contradicts or extends NB4 it is called out explicitly (§1.4, §3.5, §5).

---

## Environment honesty header — WHICH GATES RAN, MEASURED NOT ASSUMED

Same cloud channel N1 ran on, and it reproduces identically. Measured live in this container:

```
$ python3 --version                       -> Python 3.11.15
$ grep requires-python pyproject.toml     -> requires-python = ">=3.12"
$ python3 -m pytest --version             -> No module named pytest
$ python3 -m pre_commit --version         -> No module named pre_commit
$ ls .git/hooks | grep -v sample | wc -l  -> 0
$ ruff --version                          -> ruff 0.15.8   (>= the >=0.15.5 floor: usable)
$ python3 -c 'import sqlite3; print(sqlite3.sqlite_version)' -> 3.45.1
$ git rev-parse --is-shallow-repository   -> true
$ git rev-list --count HEAD               -> 299
$ git log --reverse --format='%ad' --date=short | head -1 -> 2026-08-13
```

**No gate was bypassed, because no gate ran.** The dispatch-stamp commit produced zero hook output —
that is the absence of installed hooks, not a suppressed failure. Nothing in this lane used
`--no-verify`. This artifact is markdown only.

**One environment fact is not incidental to this lane — it is load-bearing evidence, and it goes in
the memo rather than the footnotes.** This container is a **shallow clone with a 2026-08-13 floor**.
Two of the four charts the brief asks for are git-derived, and a git-derived number computed here
would be silently truncated. That is the exact failure `telemetry_emit.assert_not_shallow()`
(`:219`) exists to refuse on the WRITE side, and **§2.6 makes it a requirement on the READ side**,
because this lane is its own worked example. Every git-derived figure below is labelled with the
window it was computed over, or reported as `unavailable`.

**What IS measured here, and is therefore trustworthy:** everything derived from the committed tree
by reading files (the audit corpus parse in §2.4, the task-tree census in §2.5, the grep sweeps in
§1) and everything produced by **executing** a repo module (the ADR-101 gate probe in §3.4). Those
do not depend on history depth.

---

## Item 1 — the exact data contract the read path consumes — **CLEAR**

### 1.1 The store, as the library actually defines it

`scripts/telemetry_emit.py:149-159`. One table, seven columns, append-only by discipline (the module
carries no UPDATE and no DELETE path):

```
events(id           INTEGER PRIMARY KEY AUTOINCREMENT,
       ts           TEXT    NOT NULL,          -- UTC ISO-8601 with microseconds (:301)
       event_type   TEXT    NOT NULL,          -- check_run | hook_run | blocker_fired  (:131)
       name         TEXT    NOT NULL,          -- organ name; refused if empty (:370)
       outcome      TEXT,                      -- pass | block | error, or NULL         (:135)
       duration_ms  INTEGER,                   -- int or NULL; refused if not an int    (:373)
       context_json TEXT    NOT NULL DEFAULT '{}')
```

- **Path:** `$DEV_KNOWLEDGE_TELEMETRY_DB` else `<root>/logs/TELEMETRY.db` (`:124`, `:266-275`).
  **The read path must NEVER call `default_db_path()`** — for the same reason N1 forbids it on the
  write side: `_REPO_ROOT` is `Path(__file__).resolve().parent.parent` (`:110`), which resolves to
  the *worktree* in a linked worktree. A reader that resolves its own root differently from the
  writer silently reads an empty or stale store and renders a confident zero. The reader resolves
  via `git rev-parse --git-common-dir` — the `fleet_analytics.py:1075 _git_common_dir()` pattern.
- **Connection:** WAL / `synchronous=NORMAL` / `busy_timeout=5000` (`:140-146`, `:289-291`). WAL is
  the property that makes the read path safe at all: a reader never blocks a hook mid-commit.
- **`context_json`** is `json.dumps(..., sort_keys=True)` and carries the three bound constraints:
  `git_derived: true` · `coverage: <int|"unknown">` · `skipped: <int>` **plus** `capabilities: {...}`
  (the live host vector over `git`/`grep`/`pre-commit`/`powershell`/`pandas`, `:170`).

### 1.2 What N1's wiring adds to the contract — the read path's real input

The seven columns are the *storage* contract. The *semantic* contract is set by N1's wiring
decisions, and the reader is coupled to all six of them. Stated as the reader sees them:

| # | N1 decision | What the reader must therefore do |
|---|---|---|
| 1 | **One `check_run` event per check**, emitted after the slot flatten in `CHECK_ORDER` (N1 §1 sites 1/1c) | `COUNT(*) WHERE event_type='check_run'` per run == the registry size at that moment (**43** today, `audit.py:3374-3424`, counted). Emission order == registry order, so ordinal position is meaningful and need not be re-derived. |
| 2 | **`Finding.status` 5→3 collapse**: `fail`→`block`; `pass`/`warn`/`n/a`/`unavailable`→`pass`; a raising check→`error` (N1 §1) | **`outcome='pass'` DOES NOT MEAN PASS.** It means "not a fail". A WARN is invisible in the `outcome` column by construction. The reader gets the WARN count **only** from `context.statuses`, and any chart that reads WARN off `outcome` is wrong by design. This is §2.4's whole dependency. |
| 3 | **Multi-finding checks emit ONE aggregate event**, the detail riding `context` (N1 §1) | Per-check finding counts come from `json_extract(context_json,'$.statuses.warn')` etc., never from row counts. |
| 4 | **A refusal emits BOTH** a `hook_run(outcome='block')` and a `blocker_fired` (N1 §1, `emit_blocker_fired` hard-fixes `outcome='block'` at `:447-456`) | **Never `SUM()` across `event_type`.** Every blocker is double-counted in a naive total. Every aggregate in this memo is scoped by `event_type`. |
| 5 | **Every site passes an explicit `db_path=`** (N1 §1, the sandbox-seam blocker) | The store is wherever the *caller's* root was. The reader must resolve the same root, not its own. See 1.1. |
| 6 | **Emission defaults OFF** — `--telemetry/--no-telemetry` on the click layer, `DEV_KNOWLEDGE_TELEMETRY=1` for the hooks (N1 §2) | **The series is discontinuous by default.** A gap in the data means "not enabled", not "no commits". The page must distinguish those two and must never interpolate across a gap. See §2.7. |

### 1.3 **BLOCKER — there is no run correlation key, and this is the read path's one blocking defect**

Measured, not inferred:

```
$ grep -n 'run_id\|session_id\|correlation' scripts/telemetry_emit.py \
      docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md
(no output)
```

**Zero hits in the emit library and zero in the wiring spec.** The schema has `id`, `ts`, and five
payload columns and **no column that groups the 43 `check_run` rows of one `audit.py health`
invocation into one run.**

This is not a cosmetic gap. It is the difference between the read path being possible and being
guesswork, and it lands on the brief's **first** chart:

- **Chart A ("commit-tax over time") is per-RUN, not per-CHECK.** The number the operator wants is
  *"what did this commit cost me"* — the sum of 43 `duration_ms` values belonging to one
  invocation. With no correlation key that sum can only be reconstructed by **bucketing rows on `ts`
  proximity**, and the bucketing threshold is a guess. At a 290.9 s median commit-tax (§2.3) with
  concurrent lane writers into one WAL store — which is precisely why WAL was chosen — runs
  *interleave*, and a proximity heuristic will merge two lanes' runs into one fabricated
  600-second commit. That is a plausible-but-false metric, the exact failure class the emit
  library's own docstring says the slice exists to avoid (`:346-348`).
- **It is nearly free at wiring time and expensive afterwards.** `context` is free-form and already
  `sort_keys=True` JSON. One `uuid4()` (or the ISO timestamp of run start) generated once in
  `run_checks()` and stamped into every event's `context` costs L2 roughly two lines. Adding it
  *after* L2 merges means either a schema migration on an append-only store, or a permanent
  discontinuity between pre-key and post-key rows.
- **It needs no schema change.** `context.run_id` is queryable as
  `json_extract(context_json,'$.run_id')` and needs no new column, so it does not reopen the
  "no new EVENT_TYPES/OUTCOMES" fence N1's contract draws.

**Requirement, routed to L2 TODAY rather than filed for later:** every event emitted within one
`run_checks()` invocation carries the same `context.run_id`, and each hook invocation carries its
own. Suggested minimum: `{"run_id": "<uuid4 hex>", "invocation": "health|ship-gate|audit-repo"}`.
**If L2 has already merged when this is read, it is a follow-up row, not a silent loss** — but the
window in which it is two lines wide is open only until that merge.

**Second, smaller correlation gap, filed at the same time:** nothing links a `check_run` to the
**commit** it gated. `context.head_sha` would let Chart A be plotted against the spine rather than
against wall-clock, which is what makes "tax per commit" literally true rather than
approximately true. Cheap at the same moment, and optional in a way `run_id` is not.

### 1.4 One correction to NB4, and it is in the read path's favour

NB4 §1.2 F1 recorded that `audit.py` carries no timing instrumentation. **Re-measured at this tree
and still true, and now true of the decomposed modules as well:**

```
$ grep -c 'perf_counter\|monotonic\|elapsed\|duration_ms' scripts/audit.py   -> 0
$ grep -rn 'perf_counter\|monotonic' scripts/audit_checks/                   -> (no output)
```

NB4 flagged the risk that `[#529]` leg 1 says *"wire the call sites"* and not *"and time them"*, so
a conforming wiring pass could emit `duration_ms=NULL` 43 times and leave the timing chart empty.
**N1 closed that hole**: its site table requires the timer *inside* the submitted callable, around
`check(repo_path)`, and explicitly refuses timing around `future.result()` because that would bill
each check for its queue wait. So **Chart B's data arrives with L2's merge** rather than needing a
further leg — provided L2 executes N1 §1 site 1b as written. That is a genuine improvement on NB4's
forecast and it is the reason Chart B is scheduled in the first page rather than deferred.

### 1.5 What the reader must NOT assume — the five traps, collected

1. `outcome='pass'` is not "passed" — it is "did not fail" (1.2 #2).
2. Rows do not sum across `event_type` (1.2 #4).
3. Absence of rows is ambiguous between "gate did not run" and "telemetry was off" (1.2 #6).
4. `duration_ms` may be `NULL` per row; a distribution over partial coverage must print its
   denominator, not average a hole. `coverage_value()` (`:252-263`) already encodes this discipline
   on the write side and the read side inherits it: **`unknown` is not zero.**
5. The store's location is the writer's root, not the reader's (1.1).

---

## Item 2 — the D3-first read page — **CLEAR** (four charts, three data verdicts)

### 2.1 What "D3-first" means here, stated so the two documents do not drift

The ruling carried in the 2026-08-17 architect residual is *"D3-first … datasette versus static HTML
is decided only after `[#529]` wiring emits real data"*. NB4's **D3** is the WARN ledger burn-down,
and NB4 recommended it first for one reason: **it is the only dashboard whose data exists today.**

The brief asks for a **four**-chart page, which is broader than NB4's D3 alone. Those are not in
conflict, and the resolution is the design principle of this whole section:

> **D3-first is a DATA-AVAILABILITY ordering, not a scope limit.** The page ships with all four
> panels present from day one; the panels whose data has not arrived render an explicit
> `awaiting data` state that names the blocking leg. A panel that renders its own emptiness
> honestly is worth more than a panel that is absent, because absence is indistinguishable from
> oversight — and it is the same `unknown ≠ 0` discipline the emit library already enforces.

### 2.2 The four panels and their data verdicts, up front

| Panel | Source | Data **today** | Unblocks at |
|---|---|---|---|
| **A. Commit-tax over time** | `check_run` + `hook_run` `duration_ms`, grouped per run | **NONE as a series** — 3 hand-measured points exist (§2.3) | L2 merge **+ the `run_id` fix of §1.3**. Without `run_id` this panel is *not buildable honestly*. |
| **B. Per-check timing distribution** | `check_run.duration_ms` by `name` | **NONE** (0 timers, re-measured §1.4) | L2 merge, per N1 §1 site 1b. No further leg. |
| **C. WARN-class trend** | 17 committed `docs/audits/*-ecosystem-audit.md` **+** live `context.statuses` | **YES — 17 points, extracted and printed in §2.4** | already live; gains live rows at L2 merge |
| **D. Closures-vs-births ledger** | `tasks/*.md` frontmatter `status:` + git history of those files | **PARTIAL** — full snapshot yes, series shallow-limited (§2.5) | nothing; it is a *quality* problem, not a blocked leg |

**So the page is 1 live panel, 1 partial, and 2 waiting on one merge plus one two-line fix.** That
is the honest state, and it is exactly why the build lane in Item 4 is dispatched *after* L2.

### 2.3 Panel A — commit-tax over time

**Question.** *What is a commit costing me, and is that number moving?*

**Why it is panel one.** This is the operator's most expensive measured fact. Three points exist,
all hand-measured, all in committed audits:

```
2026-08-15   42.2 s   median of 5   docs/audits/2026-08-15-technical-night3-research.md:458,466
                                    ("42.2 s of a 42.75 s commit — 98.5% of per-commit cost")
2026-08-18  373   s   1 run, CONTENDED (CPU contention, ~22% inflation)
2026-08-18  290.9 s   median of 3, quiet tree, spread 4.9%
                                    docs/audits/2026-08-18-technical-phase0-baselines.md T0.1
```

A **6.9x regression against the recorded baseline**, and `.pre-commit-config.yaml:171` still claims
`~1.4s`. This panel exists so that number is never again discovered by a special-purpose
measurement arc.

**Three points hand-measured across four days are not a series**, and the panel must not draw a line
through them as though they were. They render as **annotated reference marks** on the axis —
labelled with their source audit and their run count — against which the live series, once it
starts, is read. The 373 s point renders visually distinct and labelled `contended`; dropping it
would be tidier and would hide that contention is a real operating mode.

**Layout.**

```
COMMIT TAX                                    telemetry ON since <first run_id ts> · runs: N
--------------------------------------------------------------------------------------------
  wall seconds per audit-health run  [ line, one point per run_id ]
  reference marks:  42.2s (2026-08-15, n=5)  ·  290.9s (2026-08-18, n=3, quiet)
                    373s (2026-08-18, n=1, CONTENDED — shown, not averaged in)
  overlay:          registry size at each run (43 today) — a bigger suite is not a regression
  p50 / p95 / max over window                      -- / -- / --
  hook tax (block_ff_push + block_unanchored_push + block_commit_on_main), summed separately
```

**What keeps it honest.**
- **Per-run sum requires `run_id`.** Until §1.3 lands, the panel renders `awaiting run correlation
  — see C6 §1.3`, and **does not** fall back to `ts`-bucketing. A wrong tax number is worse than no
  tax number, because the operator will act on it.
- **Registry growth is overlaid**, per NB4's D1 note. 43 checks costing 290 s and 60 checks costing
  300 s are not the same trend.
- **Hook tax and check tax are separate series.** They fire at different moments (commit vs push)
  and summing them answers no question anyone has.
- **The default-OFF switch means the series has holes by construction** (§1.2 #6). Holes are shaded
  and labelled `telemetry off`, never bridged.

### 2.4 Panel C — WARN-class trend (the D3 panel: live today, extracted here)

**Question.** *Is the WARN count going to zero, and which check is not moving?*

**The corpus is more machine-readable than NB4 recorded**, and this lane parsed all 17 files rather
than sampling. Every file carries, at a **fixed header position**, a uniform roll-up line plus a
repo count:

```
**Repos audited:** N
**Checks:** T total — a pass, b fail, c warn, d unavailable[, e n/a]
```

**Extracted live this session — the full series, printed so nobody re-derives it:**

```
date         repos  total  pass  fail  warn  unavail  n/a
2026-05-15     2      40     8    29     3      0       -
2026-05-16     2       6     4     1     1      0       -     <- PARTIAL RUN, not a collapse
2026-05-23     3       9     8     1     0      0       -     <- PARTIAL RUN, not a collapse
2026-06-02     5      60    60     0     0      0       -
2026-06-03     5      60    60     0     0      0       -
2026-06-04     5      60    59     1     0      0       -
2026-06-05     5      60    60     0     0      0       -
2026-06-06     5      65    65     0     0      0       -
2026-06-07     5      65    64     1     0      0       -
2026-06-08     5      70    69     1     0      0       -
2026-06-09     5      70    68     2     0      0       -
2026-06-10     5      80    77     2     1      0       -
2026-06-11     5      85    81     2     2      0       -
2026-06-12     5      90    87     2     1      0       -
2026-06-13     5      90    86     2     2      0       -
2026-06-14     5      97    90     2     5      0       -
2026-07-31     6     221   159     3    21      0      38     <- schema change: gains n/a
```

**Four honesty requirements, and two of them are findings NB4 did not carry.**

- **NEW — two entries are PARTIAL RUNS, not data points.** The denominator goes 40 → **6** → **9** →
  60. A trend line that plots those as-is renders a catastrophic collapse and recovery that never
  happened; a *normalised* line (warn ÷ total) renders `2026-05-16` as a **16.7% WARN rate**, the
  worst point in the entire series, off 6 checks. Both files must be flagged as partial and excluded
  from the trend line while staying visible as marks. The mechanical discriminator is available and
  needs no heuristic: **`Repos audited:` is 2 and 3 while the fleet was 5.**
- **NEW — the denominator has two independent dimensions, and the header carries both.** `total` is
  *checks × repos*, and repos moves 2 → 3 → 5 → 6 across the series. So the only comparable quantity
  is **WARNs per check-slot**, computed with the `Repos audited:` field the header already provides.
  This is the mechanical form of NB4's warning that *"221 is the fleet roll-up across 5 repos, 36 is
  the hub's own ledger — these must never share an axis"*: the fix is not vigilance, it is
  normalising by a field that is already in the file.
- **The series has a 47-day hole** (2026-06-14 → 2026-07-31, no committed digest). Shaded and
  labelled, never interpolated. Confirmed: no file exists between those dates.
- **The last file's schema differs** — it adds `n/a` (38 of them) that the earlier 16 lack. Version
  the parse; report `unknown` for a field a given file does not carry. A parser that treats a
  missing `n/a` as 0 mis-attributes 38 checks into the pass bucket.

**And the live half depends on §1.2 #2:** because `fail`→`block` and everything else→`pass`, the
WARN count **cannot** be read from `outcome`. The live series comes from
`json_extract(context_json,'$.statuses.warn')`, which exists only because N1 chose to ride the
collapsed detail in `context`. If L2 takes the STEP-1 fork differently, this panel's live half
changes shape — so the panel names its dependency on the page.

### 2.5 Panel D — closures-vs-births ledger line

**Question.** *Is the backlog net-negative — are we closing faster than we file?*

This is `[#555]`'s Done-when in chart form: *"the first batch closes net-negative — closures
strictly greater than births — measured against the live denominator at that batch's close, with the
before/after figures both re-derived rather than carried."*

**The source is better than the brief's framing assumes, and worse in one specific way.**

Better: the `tasks/` strangler tree (ADR-107 step 3, `[#439]`, manifest first added `05df81f`
2026-08-15) makes this **machine state, not prose**. Measured live:

```
$ ls tasks/*.md | wc -l                          -> 292   (291 tasks + tasks/README.md)
$ grep -h '^status:' tasks/*.md | sort | uniq -c
    183 status: open
     80 status: closed
     24 status: deferred
      3 status: retired
      1 status: superseded
$ python3 -c "...json.load(tasks/manifest.json)"  -> schema 2, role source-of-truth,
                                                     generates BACKLOG.md, 481 nodes
```

Worse, in three specific ways the panel must state on its face:

- **`status` is a FIVE-value enum and the chart line is binary.** `deferred`(24) / `retired`(3) /
  `superseded`(1) are none of open, and none of them are closures either. **28 rows — 9.6% of the
  tree — have no home in a two-line chart.** The panel renders them as a third band, not folded
  into either. Folding `retired` into "closed" would let the ledger go net-negative by relabelling,
  which is exactly the gaming `[#555]` was filed against.
- **Closure is an in-file annotation, not a delete.** `git log --diff-filter=D -- 'tasks/*.md'`
  returns **0** — no task file has ever been deleted. So the births series comes from
  `--diff-filter=A` and the closures series from *frontmatter transitions* in the file's history.
  Two different git predicates, and the second is the expensive one.
- **Three live denominators already disagree** — `[#555]` says so itself (194 open · 218 bullets
  incl. deferred · a SessionStart gauge agreeing with neither), and this lane measures a **fourth**
  (183 `status: open`, 207 `- [#` bullets in the generated `BACKLOG.md`). **The panel must name
  which predicate it uses, in the panel header, as a literal string.** A ledger chart whose
  denominator is ambiguous is the thing `[#555]`'s first act exists to kill, and a chart is a
  faster way to entrench the wrong one than prose is.

**The prose alternative is not a substitute.** The `**Ledger:**` convention in `JOURNAL.md` has a
clean grammar (`banked closures A→B, births C→D, window net X→Y; live task nodes …`) and is
**2 lines old** (`JOURNAL.md:47`, `:98`, both 2026-08-19). It is the operator's intent expressed by
hand; it is not a series.

**Shallow-clone limit, stated rather than worked around:** the births/closures *time axis* is
git-derived, and in this container git reaches back only to 2026-08-13 (299 commits). The snapshot
above is exact; **any series this lane computed would be a truncation, so this lane computed none.**
On the operator's full clone the series is available. The panel prints `unavailable — shallow
clone` rather than a short line, per §2.6.

### 2.6 The refusal rule, promoted from a caveat to a page-wide requirement

`telemetry_emit.assert_not_shallow()` (`:219`) refuses to emit a git-derived number from a shallow
repo. **The read page adopts the same refusal**, and this lane is the worked example: three of the
four panels above would have rendered a plausible short line in this container.

> **Rule.** Any panel whose series is git-derived calls the shallowness probe first and renders
> `unavailable — shallow clone (history floor <date>)`. It never renders a truncated series, and it
> never renders an empty one as zero.

This is one function (`is_shallow_repository()` already exists at `:192` and returns
`bool | None` — the third state being "could not tell", which also renders `unavailable`), reused,
not reimplemented.

### 2.7 The page shape, and how it coexists with lane K's dashboard

**Honest statement of what I could and could not verify.** `grep -rn 'lane K'` over
`docs/audits/`, `docs/handoffs/`, `JOURNAL.md` and `BACKLOG.md` returns **no lane-K artifact for
2026-08-19**, and `git branch -r` shows only `origin/main`. The only "lane k" in the tree is
batch 6's `[#293]` cross-repo seeding lane, which is not a dashboard. **So lane K's dashboard is
named by the brief and not yet visible in the tree**, and the boundary below is drawn against the
two rows that could be it, both of which give the same answer:

- **`[#171]`** (`status: open`) — *"Build the conformance dashboard at `ecosystem/conformance.md` …
  a read-only validator generates it and commits its own output (ADR-80 committed-generated-zone
  writer policy)"*.
- **`[#322]`** (`status: deferred`, dated review 2026-09-09) — the fleet dashboard, three legs, data
  sources `logs/BOUNDARY-DRIFT.md` + `fleet_health.py`.

**The boundary, and it is a clean one because it falls out of ADR-80 rather than being negotiated:**

| | **Read page (this memo)** | **Lane K's dashboard** |
|---|---|---|
| Owns | **cost and outcome over TIME** — what the gate mesh charged and how its verdicts moved | **conformance STATE now** — which repo satisfies which rule at HEAD |
| Question | *"is this getting better?"* | *"is this correct right now?"* |
| Source | `logs/TELEMETRY.db` + the audit corpus + `tasks/` | validator output over the live fleet |
| Format | self-contained `.html` | generated `.md` (`[#171]` names it) |
| Home | `logs/TELEMETRY-DASHBOARD.html` | `ecosystem/conformance.md` |
| Writer policy | **gitignored** — regenerates on every run, ADR-80 §(b) high-churn | **committed** — ADR-80 §(b) durable record, and `[#171]` says so |
| Cadence | on demand / post-run | per validator run, gate-adjacent |

**The no-duplication rule, in one line each:**

- The read page renders **no per-repo conformance table**. If the operator wants "is `corp-ops`
  conformant", that is one link out, not a second copy.
- The conformance dashboard renders **no trend**. If it wants "is this improving", that is one link
  back.
- **One link each way, and the link is the entire integration.** No shared generator, no shared
  data file, no shared module. Two writers, two homes, two writer policies. The file-disjointness
  in Item 4's contract is what makes them dispatchable in parallel.

**Why the trend/state split rather than a topic split** (e.g. "K owns fleet, C6 owns hub"): a topic
split has to be re-negotiated the moment either surface grows. The trend/state split is already
enforced by ADR-80's own writer policy — a high-churn view is gitignored and a durable record is
committed — so the two surfaces cannot converge without one of them violating the rule that put it
where it is.

### 2.8 The skeleton — draft, fenced, zero external services

Not built; this is the shape the build lane starts from. Zero dependencies, zero network, one file,
theme-aware, and **every panel carries its own honesty state**.

```html
<!DOCTYPE html>
<meta charset="utf-8">
<title>dev-knowledge · gate telemetry</title>
<style>
  /* Intake #9 AC-4: theme-aware. Tokens on :root, redefined under prefers-color-scheme.
     No color is defined ONLY inside the media block. */
  :root { --bg:#fff; --fg:#1a1a1a; --mut:#666; --grid:#e5e5e5;
          --ok:#2f7d32; --warn:#b26a00; --bad:#c1272d; --acc:#3b5bdb; --card:#fafafa; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#16181c; --fg:#e6e6e6; --mut:#9aa0a6; --grid:#2c2f36;
            --ok:#6abf69; --warn:#e0a458; --bad:#e26d6d; --acc:#7f9cf5; --card:#1d2026; }
  }
  body { background:var(--bg); color:var(--fg); margin:0; padding:1.5rem;
         font:14px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace; }
  .panel { background:var(--card); border:1px solid var(--grid); border-radius:6px;
           padding:1rem; margin:0 0 1rem; }
  .panel h2 { font-size:1rem; margin:0 0 .25rem; }
  .den { color:var(--mut); font-size:.85rem; }        /* denominator, always printed */
  .await { color:var(--warn); font-style:italic; }     /* awaiting-data state           */
  .na    { color:var(--mut); font-style:italic; }      /* unavailable state             */
  svg { width:100%; height:180px; overflow:visible; }
  .gap { fill:var(--grid); opacity:.5; }               /* shaded, never bridged         */
</style>

<h1>gate telemetry <span class="den" id="stamp"></span></h1>

<section class="panel" id="p-tax">
  <h2>A · commit tax</h2>
  <div class="den" id="p-tax-den"></div>
  <div id="p-tax-body"></div>
</section>

<section class="panel" id="p-dur">
  <h2>B · per-check timing distribution</h2>
  <div class="den" id="p-dur-den"></div>
  <div id="p-dur-body"></div>
</section>

<section class="panel" id="p-warn">
  <h2>C · WARN trend <span class="den">(per check-slot — repos audited varies 2→6)</span></h2>
  <div class="den" id="p-warn-den"></div>
  <div id="p-warn-body"></div>
</section>

<section class="panel" id="p-ledger">
  <h2>D · closures vs births</h2>
  <div class="den" id="p-ledger-den"></div>
  <div id="p-ledger-body"></div>
</section>

<p class="den">
  state now: <a href="../ecosystem/conformance.md">conformance dashboard</a> — this page is trend,
  that page is state. Neither duplicates the other.
</p>

<script>
// DATA is inlined by the generator. No fetch(), no CDN, no external host: intake #9 AC-1/AC-2.
// Every series carries its own provenance so a panel can refuse rather than guess.
const DATA = {
  generated: "<ISO ts>",
  source_db: "<abs path the generator actually opened>",
  shallow:   false,                       // is_shallow_repository(); null => "could not tell"
  tax:    { state:"awaiting", reason:"no run_id correlation — C6 §1.3", runs:[],
            marks:[ {d:"2026-08-15", s:42.2,  n:5, note:"night3"},
                    {d:"2026-08-18", s:290.9, n:3, note:"quiet"},
                    {d:"2026-08-18", s:373.0, n:1, note:"CONTENDED"} ] },
  dur:    { state:"awaiting", reason:"0 timers in audit.py — unblocks at L2 merge",
            covered:0, registry:43, checks:[] },
  warn:   { state:"ok", points:[ /* {d,repos,total,pass,fail,warn,na,partial} x17 */ ],
            gaps:[ {from:"2026-06-14", to:"2026-07-31", reason:"no digest committed"} ] },
  ledger: { state:"partial", predicate:"tasks/*.md frontmatter status:",
            snapshot:{open:183, closed:80, deferred:24, retired:3, superseded:1},
            series_state:"unavailable", series_reason:"shallow clone (floor 2026-08-13)" }
};

const $ = id => document.getElementById(id);

// One renderer per state. A panel NEVER silently renders empty:
// "awaiting" (leg not landed) and "unavailable" (cannot be computed here) are distinct,
// and neither is zero. This is coverage_value()'s unknown-is-not-zero rule at the read end.
function guard(key, bodyEl, denEl, s) {
  if (s.state === "awaiting")
    { bodyEl.innerHTML = `<span class="await">awaiting data — ${s.reason}</span>`; return false; }
  if (s.state === "unavailable")
    { bodyEl.innerHTML = `<span class="na">unavailable — ${s.reason}</span>`; return false; }
  return true;
}

// --- C: the only panel with a full series today -------------------------------------------
function renderWarn(s, body, den) {
  if (!guard("warn", body, den, s)) return;
  const live = s.points.filter(p => !p.partial);          // partial runs are marks, not line
  den.textContent = `${live.length} of ${s.points.length} points on the trend `
                  + `(${s.points.length - live.length} partial runs shown as marks, not plotted) · `
                  + `${s.gaps.length} gap(s), shaded and never interpolated`;
  // rate is warn / total, and total is checks x repos — normalising by the header's own
  // "Repos audited:" field is what stops the fleet roll-up sharing an axis with the hub ledger.
  const pts = live.map(p => ({ x:p.d, y: p.warn / p.total }));
  body.appendChild(sparkline(pts, s.gaps));               // inline <svg><polyline>, no library
}

// --- A/B: present from day one, rendering their own emptiness honestly ---------------------
function renderTax(s, body, den) {
  den.textContent = s.state === "ok"
      ? `${s.runs.length} runs · grouped by context.run_id`
      : "reference marks only — three hand-measured points are not a series";
  if (!guard("tax", body, den, s)) { body.appendChild(marksOnly(s.marks)); return; }
  body.appendChild(sparkline(s.runs.map(r => ({x:r.ts, y:r.total_ms/1000})), []));
}
function renderDur(s, body, den) {
  den.textContent = `coverage ${s.covered}/${s.registry} checks reporting a duration`;
  if (!guard("dur", body, den, s)) return;
  if (s.covered < s.registry)                             // partial denominator => no percentages
    den.textContent += " — shares suppressed while coverage is partial";
  body.appendChild(boxplots(s.checks));                   // inline SVG, p50/p95/max per check
}
function renderLedger(s, body, den) {
  den.textContent = `predicate: ${s.predicate} · `
    + `${s.snapshot.deferred + s.snapshot.retired + s.snapshot.superseded} rows are neither `
    + `open nor closed and are shown as a third band, never folded`;
  body.appendChild(stackedBands(s.snapshot));
  if (s.series_state !== "ok")
    body.insertAdjacentHTML("beforeend",
      `<div class="na">trend unavailable — ${s.series_reason}</div>`);
}

$("stamp").textContent = `generated ${DATA.generated} · ${DATA.source_db}`;
renderTax   (DATA.tax,    $("p-tax-body"),    $("p-tax-den"));
renderDur   (DATA.dur,    $("p-dur-body"),    $("p-dur-den"));
renderWarn  (DATA.warn,   $("p-warn-body"),   $("p-warn-den"));
renderLedger(DATA.ledger, $("p-ledger-body"), $("p-ledger-den"));
// sparkline() / boxplots() / marksOnly() / stackedBands() build inline <svg> from the arrays.
// ~120 lines of plain SVG path construction; no charting library, no <img>, no external href.
</script>
```

**Four properties of that skeleton are requirements, not style:**

1. **`DATA` is inlined by the generator** — no `fetch`, no CDN, no `<img src>`. That is intake #9
   AC-1 ("renders with no network fetch") in mechanical form, and the build lane's test asserts the
   emitted file contains no `http://` or `https://` resource reference.
2. **`guard()` is the whole design.** Three states — `ok` / `awaiting` / `unavailable` — and empty is
   never one of them. This is `coverage_value()`'s `unknown ≠ 0` rule (`:252-263`) moved to the read
   end, and it is what makes shipping the page before its data arrives defensible rather than
   premature.
3. **Every panel prints its denominator** in `.den`, unconditionally, above the chart.
4. **Theme tokens are defined on bare `:root` first**, then redefined under
   `prefers-color-scheme: dark`. No colour has its only definition inside the media block — a page
   that inverts to unreadable in VS Code's other theme fails intake #9 AC-4.

---

## Item 3 — Datasette vs static HTML, priced on our constraints — **CLEAR** · recommendation **LEAN**

NB4 §2 already scored both on four axes and recommended static. **This section does not re-score
them.** It prices the two routes against the three constraints the brief names — Windows operator
console, no server appetite, the AppLocker precedent — and adds the one cost NB4 could not have
priced, because it was measured by executing the gate this session (§3.4).

### 3.1 Constraint 1 — the Windows operator console

Measured from the tree: `protocols/ENVIRONMENT.md:41-42` sets `CLAUDE_CODE_USE_POWERSHELL_TOOL: 1`
and `defaultShell: powershell`; `:155` puts the repo at
`C:\Users\1028120\Documents\Dev\.dev-knowledge`; `ecosystem/registry.md:26` records the fleet on the
same corporate host.

- **Static HTML:** passes with nothing to install. `start .\logs\TELEMETRY-DASHBOARD.html`, or open
  it in the VS Code tab that is already there. Intake #9's literal ask.
- **Datasette:** runs on Windows — upstream's position is that it works while its *test suite* needs
  WSL. That is fine for a consumer. But the operator's interaction becomes: open a terminal, start a
  process, switch to a browser, navigate a table UI, remember to stop the process. **That is four
  more steps than "open the file", every time, forever.**

### 3.2 Constraint 2 — no server appetite

This is the constraint that decides it, and it is worth being precise about *why*, because
"no server" sounds like a preference and is actually a property.

`datasette serve` is a uvicorn ASGI process. **The dashboard exists only while it runs.** Every
consequence follows from that one fact: it cannot be opened from a handoff link; it cannot be read
in a session that did not start it; it has no state to inspect after the fact; and it adds a
process the operator must remember to stop. A surface with a lifetime shorter than the question it
answers is not an observability surface — it is a query tool with a UI.

Datasette's `--get` escape hatch (bake a page to stdout, no server) is real, and NB4 recorded it.
Priced here: **what it bakes is Datasette's own table HTML, not a chart.** Full static export is
still an open upstream request. So the mode that satisfies "no server" is the mode that does not
produce the four panels the brief asks for.

Static HTML has no process, no port, no lifetime. It is a file. It survives being emailed, attached
to a handoff, or opened three weeks later.

### 3.3 Constraint 3 — the AppLocker precedent

**Stated plainly: I searched for this and did not find it.**
`grep -rn -i applocker` over the tree returns **zero hits** in `*.md` and `*.yaml`. There is no
recorded AppLocker ruling, incident or exemption in this repo.

**The premise still prices correctly, and here is the honest form of it.** The operator's host is a
corporate Blue Yonder Windows machine (`ecosystem/registry.md:26`, and the `1028120` user path).
On such a host, software-restriction policy is a *live risk class* rather than a documented event:
an unsigned executable, a locally-bound listening socket, or a browser reaching `127.0.0.1` are each
things corporate policy commonly restricts, and none of them can be assumed available.

Priced under that risk, without overclaiming:

- **Static HTML touches none of the restricted classes.** It is a `file://` document opened by an
  already-approved browser or an already-approved editor. **There is no policy surface to be
  refused by.**
- **Datasette touches two of them** — it runs a Python process that **binds a local port**, and the
  operator's browser then connects to `localhost`. Either can be restricted, and the failure mode is
  the worst kind: it works today and stops working after a policy push, at which point the
  observability surface is gone precisely when someone wanted to look at it.

**If the operator wants this constraint to be doctrine rather than a risk assessment, it needs a
recorded ruling.** Today it is neither cited nor citable, and this memo does not manufacture one.
It does not change the recommendation: the route that touches no policy surface wins under both
readings.

### 3.4 The cost NB4 could not price — the ADR-101 gate, **executed** against this design

Run live this session, `python3 -c "import validate_hermetization as v; ..."`, against every path
either route would need. Not reasoned about — executed:

```
logs/TELEMETRY-DASHBOARD.html                              A=ok    B=ok    C=ok
logs/GATE-DASHBOARD.html                                   A=ok    B=ok    C=ok
ecosystem/telemetry-dashboard.html                         A=ok    B=ok    C=ok
ecosystem/conformance.md                                   A=ok    B=ok    C=ok
scripts/gen_telemetry_dashboard.py                         A=ok    B=ok    C=ok
tests/test_telemetry_dashboard.py                          A=ok    B=ok    C=ok
docs/audits/2026-08-19-technical-c6-telemetry-readpath.md  A=ok    B=ok    C=ok
docs/DASHBOARD.html                                        A=ok    B=ok    C=BLOCK
docs/dashboards/telemetry.html                             A=BLOCK B=ok    C=BLOCK
queries/warn-ledger.sql                                    A=BLOCK B=ok    C=ok
scripts/queries/warn-ledger.sql                            A=ok    B=ok    C=BLOCK
```

Three results, and **the third is new and contradicts a recommendation of NB4's**:

1. **`logs/*.html` is still admissible**, re-confirmed against a tree that has changed since NB4
   measured it (the `tasks/` strangler tree landed in between, and Rule C's allowlist is derived
   from the **live** taxonomy). NB4's home proposal survives the tree change.
2. **`docs/dashboards/` and a loose `docs/*.html` are refused**, as NB4 found. No amendment is being
   walked into.
3. **NEW — NB4's recommended data layer has no admissible home.** NB4 §2.4 recommended shipping SQL
   as `.sql` files (*"a `.sql` file the operator runs with `sqlite3 -box`"*) and called views
   *"the correct place to put the definition of organ cost"*. **Both plausible homes are refused:**
   top-level `queries/` by Rule A, `scripts/queries/` by Rule C —
   *"new path outside allowlisted homes — operator approval required"*.

   **The fix is cheap and it is better than the thing it replaces.** The query definitions live as
   **named module constants in `scripts/gen_telemetry_dashboard.py`** — an admissible path, no new
   home, no ruling. It also keeps them testable in the same pytest run as the generator, and it
   follows the precedent `[#533]` leg 2 set for exactly this class of decision
   (`_PARALLEL_MAX_WORKERS`: *"configuration a reader can find and an operator can argue with rather
   than a literal buried in a call"*, `audit.py:3535-3540`). NB4's *substance* — one versioned
   definition of "organ cost", reused by every consumer — is preserved. Only its container changes.

### 3.5 One more correction to NB4, because it changes the build estimate

NB4 §2.3 leaned on the Arc-5 P6 pilot as proof the repo had *"already done this once … zero deps,
CSP-self-contained, theme-aware, one session"*. **Re-measured:**

```
$ grep -rln '<!DOCTYPE\|prefers-color-scheme\|<svg' scripts/   -> (no output)
```

**There is no HTML-generating code anywhere in `scripts/`.** The P6 pilot published a **claude.ai
Artifact** (`docs/audits/2026-07-06-arc5-buy-vs-build-verdicts.md:14`), which proved the *shape* and
left no generator in the tree. So the build lane is **greenfield**, not a copy-and-adapt. That
raises the estimate — it is why Item 4 is sized **M** rather than S — and it does not change the
recommendation, because the thing being written is ~120 lines of SVG path construction, not a
framework.

### 3.6 The comparison, on our three constraints plus the two costs

| | Windows console | No server appetite | Policy surface | ADR-101 cost | ADR-112 tier |
|---|---|---|---|---|---|
| **Datasette (`serve`)** | works; +4 steps per look | **FAILS** — surface dies with the process | binds a local port; browser → localhost | none (never in-tree) | Tier S if `uvx` and never imported |
| **Datasette (`--get`)** | works | passes | none | none | Tier S |
| **Static HTML + stdlib `sqlite3`** | **open the file** | **passes** | **none** | `logs/*.html` + `scripts/gen_*.py` both admissible | **none — not an adoption** |

`--get` passes two axes and still loses, for the reason in §3.2: what it bakes is a table, and all
four panels are shapes.

### 3.7 Recommendation — **LEAN** (the ruling stays with the architect)

> **LEAN: build the read page as a self-contained static HTML file generated by
> `scripts/gen_telemetry_dashboard.py`, reading `logs/TELEMETRY.db` through stdlib `sqlite3` with
> the query definitions as named module constants in that generator. Write it to
> `logs/TELEMETRY-DASHBOARD.html`, gitignored per ADR-80 §(b). Keep `uvx datasette` as the
> zero-install ad-hoc explorer for the "slice it six ways once a month" question — never imported,
> never the dashboard. Adopt no charting library.**

Four reasons, in the order they carry weight:

1. **It is the only route that satisfies "a place he OPENS and SEES."** Every other route puts a
   process, a port, or a step between the operator and the number.
2. **It is not an ADR-112 adoption at all** — no dependency, no tier, no gap-week evaluation slot,
   no ledger line. It draws its first pixel in the same session it is dispatched.
3. **It needs no ADR-101 ruling** — every path it touches was executed against the live gate in
   §3.4 and passed.
4. **It has the lowest policy surface** on a corporate host (§3.3), under the honest form of that
   constraint rather than the cited-but-absent one.

**This confirms NB4's recommendation rather than re-deciding it.** The deferral's own trigger
("until `[#529]` emits data") fires at L2's merge; what this memo adds is that **the decision does
not actually depend on that trigger** — none of the four reasons above turns on how many rows are in
the store. What the trigger genuinely gates is the *build*, because panels A and B have no data
until then, which is what Item 4's dispatch condition encodes.

**Revisit condition, stated so this is not re-opened casually:** adopt a charting library only if a
panel appears that inline SVG cannot carry. If that day comes, the pick is Altair (~322 KB,
`vl-convert-python` ships Windows wheels) over Plotly (~3 MB per file) — NB4's finding, carried
unchanged.

---

## Item 4 — draft build-lane contract — **CLEAR** · sized **M**

House pattern taken from `docs/audits/2026-08-18-technical-533-leg2-lane-contract.md` via N1 §5.
**This is a draft for the operator to freeze, amend or discard — it is not itself a dispatch.**

**Sizing: M, not S.** Three reasons, each measured above: the generator is greenfield (§3.5, zero
HTML code in `scripts/` today); four panels each need a distinct honesty state (§2.8 `guard()`); and
the WARN parser has to handle two partial runs, a schema change and a 47-day hole (§2.4). It is
still one lane — one new script, one new test file, one `.gitignore` line, no dependency.

**Dispatch condition: AFTER L2 merges.** Not before, and the reason is not sequencing hygiene: two
of the four panels have no data until then, and the `run_id` requirement of §1.3 is L2's to land.

```
# LANE R1 — TELEMETRY READ PAGE: the D3-first four-panel dashboard

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — contract-is-the-plan, NO plan-mode | high |

> Fresh CC session (`/clear`). Worktree lane — you never touch the primary checkout and you
> NEVER merge. Commit-and-STOP.

**Worktree (STEP 0):** `claude --worktree lane-r1-readpath --bg "[.dev-knowledge · read path ·
telemetry dashboard] docs/audits/<this-contract>.md"` — branch name verified against
`scripts/validate_branch_naming.py` LANE_BRANCH_RE before provisioning.

**DISPATCH CONDITION — verify before STEP 1, do not assume:** lane L2 has MERGED. Check
`git log --oneline main | grep -i 'telemetry.*wir\|529'` and confirm `scripts/audit.py`
imports `telemetry_emit`. If L2 has NOT merged, STOP-report — panels A and B have no data
source and this lane would build two empty panels and call them done.

**Governing rows:** `[#529]`'s read-side consumer. This lane closes NO row on its own; it is the
first consumer the `[#529]` Done-when names. `[#171]`/`[#322]` are NOT this lane's (see below).
**ADR-110:** save this prompt as `docs/audits/<YYYY-MM-DD>-technical-r1-readpath-lane-contract.md`
and COMMIT it as your first commit.
**Spec of record:** `docs/audits/2026-08-19-technical-c6-telemetry-readpath.md` (this memo).
Its §1.3 names a BLOCKER you verify rather than rediscover; its §2.4 carries the extracted
17-point series so you do not re-derive it; its §3.4 carries the executed gate probe.

## FILE-DISJOINTNESS (parallel-safe with lane K)
- **YOURS:** NEW `scripts/gen_telemetry_dashboard.py` · NEW `tests/test_telemetry_dashboard.py` ·
  `.gitignore` (ONE line appended at the end of the logs/ block).
- **NOT YOURS, DO NOT OPEN:** `ecosystem/conformance.md` · `scripts/fleet_health.py` ·
  `scripts/boundary_report.py` · anything lane K touches · any file lane L2 wired
  (`scripts/audit.py`, the three `block_*.py`, `.claude/commands/lane-{boot,integrate}.md`).
- `.gitignore` is the ONLY shared file. Append at the end of the existing `logs/` block; if it
  already carries a `*-DASHBOARD.html` line, take it and say so in the packet.

## PINNED-BY-TESTS (do not detach)
- `tests/test_telemetry_emit.py` — you are a READER. Do not touch the emit library or its tests.
  If you need a library change, STOP-report; it is not this lane's.
- `tests/test_validate_hermetization.py` — the live-tree test asserts Rule C admits every tracked
  path. Your two new files are admissible (verified live, memo §3.4) — but they are ADDS, so
  re-run this file and confirm rather than trusting the memo.
- `tests/test_writer_integrity.py` — a new writer under `scripts/` is exactly its subject.
- `ecosystem/doc-counts.md` — the collected-test count moves when you add a test file.

## UNDERSTAND
- Problem: `[#529]` will be wired and emitting, and there is still no surface the operator can
  OPEN. The store is a binary file in `logs/`. This lane is the whole answer to "gdzie w końcu
  będą wyniki tej telemetrii".
- Four panels, THREE data states. Panel C is live today; A and B arrive with L2; D is a snapshot
  whose time axis is git-derived. **A panel with no data renders `awaiting data — <reason>`, NOT
  an empty chart and NOT a zero.** That rule is the design (memo §2.8 `guard()`), not a polish item.
- **VERIFY §1.3 FIRST.** If L2 landed `context.run_id`, panel A is buildable. If it did NOT, panel A
  renders `awaiting run correlation` and you file the follow-up — **you do NOT bucket rows by `ts`
  proximity**. Concurrent lane writers into one WAL store make proximity-bucketing fabricate runs,
  and a wrong commit-tax number is worse than no number because the operator will act on it.
- Scope: ONE new generator, ONE new test file, ONE `.gitignore` line. **No dependency additions.**
  No charting library. No `.sql` files — the queries are named module constants in the generator
  (memo §3.4 result 3: both `.sql` homes are gate-refused).

## STEPS
**STEP 0 — worktree + contract commit** (above). `COMMIT`

**STEP 1 — VERIFY THE DISPATCH CONDITION AND THE run_id STATE, before any code.** Confirm L2 is
merged; then run one `audit.py health --telemetry` and read the store back with stdlib `sqlite3`.
Record in the lane artifact: row count, distinct `event_type`, distinct `name`, whether
`json_extract(context_json,'$.run_id')` is non-NULL, and whether `duration_ms` is populated for
all 43. **That readback decides which panels you build live and which render `awaiting`.** Write
the decision down before writing code. `COMMIT`

**STEP 2 — TEST-FIRST: `tests/test_telemetry_dashboard.py` (NEW), RED before any generator.**
The load-bearing cases, in this order:
  1. **self-contained** — emitted HTML contains no `http://` and no `https://` resource
     reference (intake #9 AC-1, mechanical form). This is the one that must never regress.
  2. **awaiting ≠ empty ≠ zero** — a store with no `check_run` rows renders the literal
     `awaiting data`, and the emitted HTML contains NO `0` presented as a measurement.
  3. **shallow refusal** — with `is_shallow_repository()` forced True, every git-derived panel
     renders `unavailable`, never a truncated series (memo §2.6).
  4. **partial-run exclusion** — the 2026-05-16 (6 checks / 2 repos) and 2026-05-23 (9 / 3)
     entries are NOT on the trend line, and ARE present as marks (memo §2.4).
  5. **gap not bridged** — the 2026-06-14 → 2026-07-31 hole renders as a gap, and no polyline
     segment spans it.
  6. **denominator printed** — every panel emits its `.den` line unconditionally.
  7. **no root guess** — the generator refuses to call `telemetry_emit.default_db_path()`;
     assert the resolved path comes from `git rev-parse --git-common-dir` (memo §1.1).
  8. **schema-version tolerance** — a corpus file lacking the `n/a` field yields `unknown`
     for that field, not 0 (memo §2.4).
  9. **theme tokens** — every custom property defined on bare `:root` is also defined inside the
     `prefers-color-scheme: dark` block, and none is defined ONLY there (intake #9 AC-4).
  `COMMIT`

**STEP 3 — the corpus parser (panel C, the only live panel).** Parse the 17
`docs/audits/*-ecosystem-audit.md` roll-ups. Use `Repos audited:` as the partial-run discriminator
and as the normaliser — the trend is WARNs per check-slot, never a raw count (memo §2.4). Green
STEP 2 cases 4, 5, 8. `COMMIT`

**STEP 4 — the store reader (panels A and B).** stdlib `sqlite3`, opened READ-ONLY
(`file:...?mode=ro` URI) so the reader cannot create `-wal`/`-shm` sidecars in a clean tree.
Queries as named module constants. Scope every aggregate by `event_type` — a refusal emits BOTH a
`hook_run(block)` and a `blocker_fired`, so nothing sums across types (memo §1.2 #4). WARN counts
come from `context.statuses`, NEVER from `outcome` (memo §1.2 #2). Green STEP 2 cases 2, 7.
`COMMIT`

**STEP 5 — the task-tree reader (panel D).** `tasks/*.md` frontmatter `status:`. Print the
predicate string in the panel header. `deferred`/`retired`/`superseded` are a THIRD band, never
folded into either line (memo §2.5). Series is git-derived → shallow-guarded. Green case 3.
`COMMIT`

**STEP 6 — the HTML emitter.** Memo §2.8 skeleton. Inline `<svg>` only; ~120 lines of path
construction. Green STEP 2 cases 1, 6, 9. `COMMIT`

**STEP 7 — `.gitignore logs/*-DASHBOARD.html`.** ONE line, appended in the `logs/` block, with the
one-line reason the six existing reporter entries all carry (high-churn view; ADR-80 §(b)).
Note whether `logs/TELEMETRY.db*` is present — L2 owed it as `[#529]` leg 2; if it is MISSING,
say so in the packet and DO NOT add it (it is L2's leg, not yours). `COMMIT`

**STEP 8 — regenerate what the new files moved.** `gen_doc_counts.py --write` (collected-test
count) and the codemap if the new module adds an import edge. Both are pre-commit-gated; neither
is optional. `COMMIT`

**STEP 9 — GENERATE IT AND LOOK AT IT.** Run the generator, open the emitted file, and paste into
the lane artifact: the byte size, the panel states (which rendered live / awaiting / unavailable),
and the printed denominators. **Also state which panels you could not verify visually** — a cloud
lane cannot open a browser, and claiming a visual check you did not perform is worse than not
performing it. `COMMIT`

## FINAL
Targeted, `-n 0`: the NEW test file + `tests/test_validate_hermetization.py` +
`tests/test_writer_integrity.py` + `tests/test_telemetry_emit.py`. All green ->
**commit-and-STOP.** STOP packet: the STEP-1 readback · which panels are live vs awaiting ·
the run_id verdict · the `.gitignore` state of `logs/TELEMETRY.db*` · files touched · every fork
taken · what you could NOT verify.
**NO merge, no push to main, no touching the primary checkout.**

## WHAT NOT TO DO
No dependency additions (no plotly, no altair, no vl-convert, no datasette — memo §3.7) · no
`.sql` files (both homes gate-refused, memo §3.4) · no new top-level dir and no `docs/<genre>/`
(ADR-101 Rule A/C) · no edits to `scripts/telemetry_emit.py` or its tests (you are a reader) ·
no edits to any file lane L2 wired · no `ecosystem/conformance.md` (lane K's) · no `ts`-proximity
bucketing to fake a run_id · no rendering an empty panel as zero · no committing the emitted
`.html` (it is gitignored by construction) · no `--no-verify` · no `git add -A` · no merge.
```

---

## Item 5 — findings filed, not fixed

Four, none in this lane's scope, all recorded so they are not re-discovered.

1. **`run_id` absent from the emit contract** (§1.3) — the one BLOCKER. Routed to L2 today because
   the window in which it is two lines wide closes at L2's merge. **This is the single highest-value
   line in this memo.**
2. **NB4's `.sql` data-layer home is gate-refused** (§3.4 result 3) — `queries/` blocked by Rule A,
   `scripts/queries/` by Rule C. Resolved here by relocating the queries into the generator as
   module constants; recorded because NB4's §2.4 recommendation reads as though a `.sql` file were
   admissible, and the next reader of NB4 will assume it is.
3. **`.pre-commit-config.yaml:171` still claims `~1.4s`** for a hook measured at 290.9 s (§2.3) —
   a 200x-stale comment on the most expensive organ in the repo, sitting one line above the entry
   it describes. Not this lane's file to edit.
4. **Four live denominators for "open backlog rows"** (§2.5): `[#555]` names three (194 / 218 / a
   SessionStart gauge) and this lane measures a fourth (183 `status: open` vs 207 `- [#` bullets in
   the generated `BACKLOG.md`). `[#555]`'s first act is to name ONE predicate; panel D cannot be
   trusted until that lands, and the panel prints its own predicate so the disagreement stays
   visible rather than being resolved by whichever number a chart happened to pick.

---

## Commands verbatim — everything this lane ran

```
# environment (the honesty header)
python3 --version ; ruff --version ; python3 -m pytest --version
python3 -c 'import sqlite3; print(sqlite3.sqlite_version)'
ls .git/hooks | grep -v sample | wc -l
git rev-parse --is-shallow-repository ; git rev-list --count HEAD
git log --reverse --format='%h %ad %s' --date=short | head -3

# the emit contract
sed -n '108,180p;335,400p' scripts/telemetry_emit.py
grep -n 'run_id\|session_id\|correlation' scripts/telemetry_emit.py \
     docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md     # -> ZERO hits (the blocker)

# F1 re-measured at this tree
grep -c 'perf_counter\|monotonic\|elapsed\|duration_ms' scripts/audit.py   # -> 0
grep -rn 'perf_counter\|monotonic' scripts/audit_checks/                   # -> (none)
grep -n 'def run_checks' scripts/audit.py                                  # -> 3553
# ALL_CHECKS members counted from source between 'ALL_CHECKS = [' and its ']' -> 43

# the WARN corpus (panel C's live series)
ls docs/audits/*ecosystem-audit*.md | wc -l                                # -> 17
for f in docs/audits/*ecosystem-audit*.md; do grep -m1 '^\*\*Repos audited:\*\*' "$f"; done
for f in docs/audits/*ecosystem-audit*.md; do grep -m1 '^\*\*Checks:\*\*'        "$f"; done

# the task tree (panel D)
ls tasks/*.md | wc -l                                    # -> 292 (291 tasks + README)
grep -h '^status:' tasks/*.md | sort | uniq -c           # -> 183/80/24/3/1
grep -L '^status:' tasks/*.md                            # -> tasks/README.md only
git log --diff-filter=D --name-only -- 'tasks/*.md' | grep -c '^tasks/'   # -> 0 (never deleted)
python3 -c "import json,pathlib; d=json.loads(pathlib.Path('tasks/manifest.json').read_text()); \
            print(d['schema'], d['role'], d['generates'], len(d['nodes']))"

# the ADR-101 gate, EXECUTED (not reasoned about)
python3 -c "import sys; sys.path.insert(0,'scripts'); import validate_hermetization as v; \
  [print(p, v.rule_a_violation(p), v.rule_b_violation(p), v.rule_c_violation(p)) for p in [...]]"

# the P6 correction
grep -rln '<!DOCTYPE\|prefers-color-scheme\|<svg' scripts/     # -> (none: greenfield)

# the AppLocker search
grep -rn -i applocker --include=*.md --include=*.yaml . --exclude-dir=.git   # -> ZERO hits

# lane K
grep -rln 'lane K\|Lane K\|LANE K' docs/audits/ docs/handoffs/  # -> (none for 2026-08-19)
git branch -r                                                   # -> origin/main only
grep -h '^status:' tasks/171-*.md tasks/322-*.md                # -> open / deferred

# .gitignore state
grep -n 'TELEMETRY\|DASHBOARD' .gitignore                       # -> ZERO hits ([#529] leg 2 open)
```

---

## STOP packet

**Items:** 1 **CLEAR** · 2 **CLEAR** · 3 **CLEAR** · 4 **CLEAR**. None blocked.

**The one thing to act on today:** §1.3 — **there is no `run_id` in the emit contract**, measured by
grep over both the library and N1's spec. Panel A (commit-tax, the operator's most expensive number)
is **not honestly buildable without it**, the fix is ~2 lines in `run_checks()` and needs no schema
change, and the window in which it is that cheap closes when **lane L2 merges**.

**Item 1 — the contract:** 7 columns + 4 context keys (§1.1), plus six semantic constraints the
wiring imposes (§1.2) and five traps the reader must not fall into (§1.5). One correction to NB4 in
the read path's favour: N1 *did* close the "wire but don't time" hole, so panel B arrives with L2
and needs no extra leg (§1.4).

**Item 2 — the page:** four panels, three data states. **C is live today** (17-point series
extracted and printed in §2.4, so nobody re-derives it). **A and B unblock at L2's merge**
(A additionally on `run_id`). **D is a snapshot now, series shallow-limited.** D3-first is read as a
*data-availability ordering, not a scope limit*: all four panels ship, and a panel with no data
renders `awaiting data — <reason>` rather than an empty chart or a zero (§2.1, §2.8 `guard()`).
Two new honesty findings on the corpus: **two of the 17 entries are partial runs** (6 and 9 checks)
that render as a false collapse, and **`Repos audited:` moves 2→6**, so the only comparable quantity
is WARNs per check-slot — both discriminated by a field already in each file's header (§2.4).
**Coexistence with lane K: trend vs state**, a split that ADR-80's own writer policy already
enforces (gitignored high-churn view vs committed durable record), one link each way, no shared
generator and no shared data file (§2.7). Honest limit: **no lane-K artifact exists in the tree**,
so the boundary is drawn against `[#171]` and `[#322]`, which give the same answer.

**Item 3 — the ruling: LEAN static HTML + stdlib `sqlite3`**, queries as module constants,
`logs/TELEMETRY-DASHBOARD.html`, gitignored; `uvx datasette` retained as the ad-hoc explorer, never
the dashboard; no charting library (§3.7). This **confirms NB4 rather than re-deciding it**, and
adds that the decision never actually depended on the deferral's trigger — none of its four reasons
turns on row count. What the trigger gates is the *build*. Two things NB4 could not price:
**NB4's own `.sql` data layer has no admissible home** (both candidates gate-refused, executed in
§3.4) and **the P6 "we've done this before" precedent left no code in the tree** (§3.5), which is
why Item 4 is sized M.

**Honest negative:** the brief's **AppLocker precedent does not exist in this repo** — zero hits.
It is priced as a live risk class on a corporate Windows host rather than a citable ruling, stated
as such in §3.3, and it does not change the recommendation.

**Item 4 —** lane R1 drafted, house pattern, sized **M**, **dispatch-gated on L2's merge** (verified
in STEP 1, not assumed), file-disjoint from lane K by an explicit NOT-YOURS list, `.gitignore` the
only shared file.

**Filed not fixed (§5):** the `run_id` gap · NB4's refused `.sql` home · the `~1.4s` comment on a
290.9 s hook · four live denominators for one backlog count.

**Constraints honoured:** no build · no dependency additions · no touching L2's files · no index
regeneration · no JOURNAL writes · drafts only. Two commits: the dispatch stamp and this artifact.
