# Night-batch-4 lane B — the telemetry READ path: stack evaluation, three dashboards, and where they live

- **Class:** technical (ADR-101 R3 enum) · **Date:** 2026-08-16 · **Slug:** nb4-telemetry-read
- **Status:** **DRAFT** — proposals only. Nothing here was applied: no row born, no dependency added,
  no `.gitignore` line written, no dashboard built, no intake status advanced. Every act below needs
  an architect ruling.
- **Lane:** nb4-B, branch `claude/nb4-telemetry-read-path-ivoka2`, **read-only + web research**.
- **Input:** `[#529]` (Telemetry v1 EMIT, OPEN on 4 legs) · `scripts/telemetry_emit.py` (the Stage-1
  library, merged `4ad2025d`, library-only) · the usage-telemetry memo
  `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md` · intake **#9**
  `docs/intake/2026-07-08-func-dashboards-local-html.md` (SEED) · ADR-80 §(b), ADR-101, ADR-112.
- **Deliverables:** (1) three-way stack evaluation on the four named axes · (2) three dashboard
  designs, mocked as layouts, not built · (3) the governance answer for where they live, with the
  gate measured rather than asserted · (4) a single recommendation.

---

## 0. Measurement environment — read this before reading a number

This lane ran in an **Anthropic cloud container on a shallow clone**, not on the operator's Windows
machine. Same posture the night-3 warn-ledger lane declared, and it bounds what is measurable here.

```
git rev-parse --is-shallow-repository  -> true
git rev-list --count HEAD              -> 281
git worktree list                      -> primary only (no lane worktrees in this container)
python3 -V                             -> 3.11.15   (repo requires-python is >=3.12)
import pandas                          -> ModuleNotFoundError  (the `analytics` group is not synced)
import structlog                       -> ModuleNotFoundError  (so logger_backend() == "stdlib-logging")
ls logs/TELEMETRY.db                   -> No such file or directory
```

**What that last line means, and it is the single most important fact in this report:** the store
has never been written. `[#529]` merged the library with **zero call sites**, so **Stage 2 is being
designed against an empty database**. Every claim below about what a dashboard would *show* is a
claim about a schema, not about observed data. Where I could substitute a real, already-committed
data source for the empty one, I did, and I say so each time.

Everything in §1 (source reading), §2 (library evaluation), §4 (the gate, executed live) and the
`docs/audits/*-ecosystem-audit.md` series in §3.3 reproduces exactly here — none of it needs deep
history or a Windows host. Nothing in this report depends on the shallow clone.

---

## 1. The input contract — what the read path actually has to read

### 1.1 The schema

`scripts/telemetry_emit.py:149-159`, one table, seven columns, append-only by discipline (the module
has no UPDATE or DELETE path):

```
events(id INTEGER PK, ts TEXT, event_type TEXT, name TEXT,
       outcome TEXT, duration_ms INTEGER, context_json TEXT DEFAULT '{}')
```

- `event_type` ∈ {`check_run`, `hook_run`, `blocker_fired`} (`:131`)
- `outcome` ∈ {`pass`, `block`, `error`} (`:135`)
- `ts` is UTC ISO-8601 with microseconds (`:301`)
- `context_json` is `json.dumps(..., sort_keys=True)`, and carries the three bound constraints:
  `git_derived: true`, `coverage: <int|"unknown">`, `skipped: <int>` + `capabilities: {...}`
- store: `$DEV_KNOWLEDGE_TELEMETRY_DB` else `<repo>/logs/TELEMETRY.db`, WAL / `synchronous=NORMAL` /
  `busy_timeout=5000` (`:124-144`, `:266-298`)

This is a good schema to read from. It is flat, it is SQL, `sort_keys=True` makes `context_json`
diffable, and WAL means a reader never blocks a hook mid-commit — which is the property that makes a
"just open the DB while the gate mesh is running" read path safe at all.

### 1.2 Three findings that bound every dashboard in §3

These are not caveats. They decide the build order, so they come before the designs.

**F1 — `audit.py` has no timing instrumentation at all, so per-check duration does not exist.**
Measured: `ALL_CHECKS` has **43** registered members (`scripts/audit.py:4345`), and a grep for
`perf_counter|monotonic|time()|elapsed|_ms` across the whole file returns **zero hits**. The
`duration_ms` column is real; the number that would fill it is not produced anywhere yet. Dashboard
**D1** therefore has no data until the phase-3 wiring both calls `emit_check_run` *and* adds a timer
around each check. That is inside `[#529]` leg 1 as written ("wire the call sites"), but leg 1 does
not currently say "and time them" — worth making explicit, because a wiring pass that emits
`duration_ms=None` for 43 checks satisfies the leg and still leaves D1 empty.

**F2 — lane telemetry is written into the worktree and destroyed at teardown, so per-lane data
cannot reach the store.** Three facts compose into this:

1. `default_db_path()` resolves `_REPO_ROOT = Path(__file__).resolve().parent.parent`
   (`telemetry_emit.py:110, :275`). In a linked worktree the module *is* in the worktree, so the
   path resolves to `<worktree>/logs/TELEMETRY.db`, not the primary checkout's. This is the terra P1
   condition already recorded on the `[#529]` row.
2. `.worktreeinclude` copies `.env`, `.claude/settings.local.json`, `ecosystem/*/state.yaml` — **and
   nothing else**. `logs/TELEMETRY.db` is not on it, so a lane starts with an empty store even if
   the primary has one.
3. CLAUDE.md §5 rule 9 ("No leftovers") requires teardown to remove everything the worktree created,
   and `git worktree remove` takes the lane's `logs/` with it.

So today a batch lane would emit into a private database and then delete it. **Dashboard D2 — the
one about lanes — is precisely the dashboard whose telemetry source does not survive.** The fix is
the one the row already names: resolve the root via `git rev-parse --git-common-dir`, the pattern
`fleet_analytics.py:1075` (`_git_common_dir`) already uses, which is shared across all worktrees of
one repo. Until that lands, D2 must be built from git history, not from `events`.

**F3 — two open `[#529]` legs are load-bearing for the reader, and one is a landmine.**
`logs/TELEMETRY.db` is **still absent from `.gitignore`** (verified: `grep TELEMETRY .gitignore` →
no match). A WAL-mode SQLite store also produces `-wal` and `-shm` sidecars. The first live emit
therefore dirties `git status` with up to three files and trips session-end backpressure. A reader
that opens the DB *also* creates those sidecars on a fresh file — so **the read path can dirty the
tree even though it writes no data**. Any `.gitignore` line for this must cover
`logs/TELEMETRY.db*`, not the bare name.

### 1.3 The consequence for staging

The read path has **two** sources, not one, and only the second has data today:

- **the live store** — `logs/TELEMETRY.db`, empty, blocked behind `[#529]` legs 1–4 and F1/F2;
- **the committed audit corpus** — `docs/audits/*-ecosystem-audit.md`, **17 files**, already carrying
  a machine-parseable per-check verdict table and a one-line roll-up (§3.3).

A reader designed to treat these as one logical event stream can ship something useful *this week*
and gain live rows later without a rewrite. A reader designed only against `events` ships nothing
until phase 3 lands. That distinction drives the recommendation in §5.

---

## 2. The stack evaluation

### 2.1 The axes, defined before they are scored

The four axes were named in the brief; I am fixing their meaning so the scores are checkable.

- **Zero-server operation** — can the operator see the dashboard without a process staying alive?
  A tool that must be running to be looked at fails this axis regardless of how easy it is to start.
- **Windows fit** — works on the operator's Windows 11 host with the repo's `uv` toolchain, no WSL,
  no compiler. (The fleet carries a `win-tooling` consumer repo; Windows is first-class, not an
  afterthought.)
- **Works-from-a-worktree** — a batch lane running in `.claude/worktrees/<name>` can produce or read
  the artifact, and F2's path-split does not silently give it a different answer.
- **Cost** — dependency count, install surface, glue lines, *and* the governance cost of adoption
  (§2.6), which is the axis usually left uncosted.

### 2.2 Option A — Datasette

**What it is.** Point it at a SQLite file and get a browsable web UI plus a JSON API with zero schema
configuration: `datasette logs/TELEMETRY.db`. Latest is **0.65.3**, `requires-python >=3.9`.

**Zero-server: fails as normally used, passes in one specific mode.** `datasette serve` is a uvicorn
ASGI process — the UI exists only while it runs. But `--get` is a real escape hatch: it "specifies
the path to a page within Datasette and causes Datasette to output the content from that path
**without starting the web server**", e.g. `datasette --get '/-/versions.json'`. So Datasette can be
used as a *batch renderer* that bakes a page to stdout. Note what that costs: the baked page is
Datasette's own table HTML, not a chart, and full static export is still an open upstream request
([simonw/datasette#1662](https://github.com/simonw/datasette/issues/1662)).

**Windows fit: adequate, with a documented rough edge.** The early blockers are fixed (uvloop is
gone; the Unix-only `EX_CANTCREAT` import was removed). Upstream's own position is that Datasette
works on Windows but its *test suite* needs WSL ([#511](https://github.com/simonw/datasette/issues/511)).
For a consumer that is fine. It does mean a Windows-side problem is harder to get upstream traction on.

**Works-from-a-worktree: yes, and this is its best axis.** It is a read-only viewer over a file path;
point it wherever the DB actually is. Pair it with `-i/--immutable` and it opens read-only, which
also sidesteps F3's sidecar problem.

**Cost: the highest of the three, and mostly invisible.** **19 runtime dependencies** — `asgiref`,
`click`, `click-default-group`, `Jinja2`, `hupper`, `httpx`, `pluggy`, `uvicorn`, `aiofiles`,
`janus`, `asgi-csrf`, `PyYAML`, `mergedeep`, `itsdangerous`, `setuptools`, `pip`, `platformdirs`,
`typing_extensions`, `flexcache`, `flexparser`. `uvx datasette` keeps them out of the project
environment entirely, which is the honest way to use it here — as an operator tool, never imported.

**Verdict: keep, but not as the dashboard surface.** Datasette is the right answer to "let me slice
this six ways once a month" and the wrong answer to "show me the trend". It is an *explorer*, and
the three things §3 asks for are *reports*. The memo reached the same split and called it
"Adopt (secondary)". Nothing found here changes that.

**One variant worth recording and declining:** `datasette-lite` runs Datasette in the browser under
Pyodide/WASM, so a static host serves a full Datasette with no server at all. It genuinely satisfies
zero-server. It is declined for this use because it downloads a Python interpreter into the browser
on every open and needs a CORS-serving host for the `.db` — which is the *opposite* of intake #9's
"opens as a local file in VS Code, no network fetch".

### 2.3 Option B — static HTML generation

**What it is.** A generator reads the DB (and the audit corpus), renders one self-contained `.html`
per dashboard into the tree, and the operator opens it. No process, no host.

**Zero-server: passes outright.** This is the only option that does, without qualification.

**Windows fit: passes.** Pure-Python generation plus a browser. No native build step if the charting
library ships wheels.

**Works-from-a-worktree: passes for generation, with one caveat that is really F2's.** A lane can
generate a page; whether the page is *correct* depends on the reader resolving the same root the
writer used. Fix F2 once and both sides inherit it.

**Cost: depends entirely on the library, and the three candidates are far apart.**

| Candidate | Self-contained mechanism | Payload | Extra deps | Note |
|---|---|---|---|---|
| **Plotly** | `write_html(include_plotlyjs=True)` | **~3 MB per file** — the docs state the `cdn` variant is "about 3MB smaller" | `plotly` | Every dashboard, every regeneration, 3 MB of vendored JS |
| **Altair / Vega-Lite** | `chart.save(..., inline=True)` | vega+vega-lite+vega-embed, **~322 KB min+gzip** vs plotly.js **~1.1 MB** | `altair` **+ `vl-convert-python`** (`inline=True` requires it) | `vl-convert-python` is a PyO3/Rust wheel; **Windows x64 wheels are published**, so no compiler |
| **Hand-rolled HTML/SVG/CSS** | there is nothing to inline | **single-digit KB** | **none** | The repo has already done this once — see below |

**The precedent that decides this row.** The Arc-5 P6 pilot
(`docs/audits/2026-07-06-arc5-buy-vs-build-verdicts.md:39`) shipped exactly this and recorded the
result: *"a live, default-private, theme-aware page rendered from repo data in one session, **zero
deps**, CSP-self-contained… **Plain HTML sufficed; no Mermaid was needed for the tabular/status class
of content.**"* Two of the three dashboards in §3 (D2, D3) are tabular/status content by that
classification. Only D1 is a genuine continuous trend, and a sparkline is an SVG `<polyline>`.

So the honest reading of the "static HTML" option is that it splits in two, and the cheap half wins:
**hand-rolled HTML for tabular/status, and a charting library only if a chart class appears that
SVG cannot carry.** If that day comes, Altair is the pick over Plotly — a third of the payload, and
`vl-convert-python` has Windows wheels. Plotly's 3 MB per file, committed or regenerated, is not
proportionate to 43 checks and a dozen lanes.

### 2.4 Option C — plain `sqlite3` CLI views

**What it is.** Ship SQL. `CREATE VIEW`s in the schema, or a `.sql` file the operator runs with
`sqlite3 -box logs/TELEMETRY.db < queries/organ-cost.sql`.

**Zero-server: passes.** **Windows fit: passes**, with one wrinkle — the `sqlite3` CLI binary is not
bundled with Python (the `sqlite3` *module* is), so on Windows it is a separate download unless
invoked through Python. A ten-line `python -m` wrapper removes the wrinkle and keeps the
zero-dependency property. **Works-from-a-worktree: passes.** **Cost: zero.** Standard library.

**Verdict: adopt as the substrate, reject as the surface.** Views are the correct place to put the
definition of "organ cost" — one definition, versioned in git, reused by every consumer including
Datasette and the HTML generator. What views cannot do is answer *"is this getting better?"* at a
glance: a 43-row table of durations is not a trend, and the WARN burn-down is a shape, not a number.
The operator's three questions in §3 are all shape questions.

The real conclusion is that C is not a rival to B — **C is B's data layer.** Treating them as
alternatives is the error the three-way framing invites.

### 2.5 The fourth option, surfaced because it is the standing recommendation

The brief lists three candidates. The memo that Stage 1 implements already picked a **fourth** and
called it primary: an in-terminal `rich` + `plotext` report ("Adopt (primary read surface)"), with
Datasette secondary and Streamlit explicitly declined.

I am surfacing this rather than quietly designing around it, because a Stage-2 design that
contradicts its own contract of record without saying so is how a decision gets re-litigated later.
Two things have changed since the memo:

1. **The operator has since given a direction the memo predates.** Intake #9 (2026-07-08) fixes the
   human-facing surface as **local HTML openable in VS Code**, and the brief restates it as "the
   Anthropic-artifact shape the operator likes". A terminal report is not that surface.
2. **The memo's own staging differs from the brief's.** The memo puts read surfaces in **Stage 3**
   ("month 2"), with Stage 2 being derived signals (`test_run` duration, `dep_scan`, mutation score).
   The brief calls the read path Stage 2. Not a contradiction to resolve here, but the numbering in
   the two documents does not line up, and someone will trip on it.

`rich`/`plotext` is not dead — it remains the right shape for a `--summary` flag that prints while a
gate runs. It is simply not the surface intake #9 asked for. **Recommendation: keep it out of Stage
2 entirely** rather than build two surfaces at once.

### 2.6 The cost axis nobody costed — ADR-112 tier

Every option above carries an adoption tier, and this changes the ranking.

ADR-112's guard sentence is quoted verbatim from intake #28 §A and is load-bearing:

> **Tier S never touches gates, hooks that block, or `scripts/` — anything that would, is Tier L by
> definition.**

A dashboard generator lives in `scripts/`. So:

- **Plotly / Altair / `vl-convert-python`** — new libraries imported from `scripts/` → **Tier L**:
  measured-divergence evaluation, ADOPT or REJECT on numbers, **consuming a gap-week slot**
  (`STANDING_RULINGS` E1).
- **Datasette used as `uvx datasette` and never imported** — not a `scripts/` dependency, arguably a
  Tier S operator tool: install → 30-minute try → KEEP or DELETE → one ledger line, **no births**.
- **Hand-rolled HTML + stdlib `sqlite3`** — **not an adoption at all**. No new dependency, no tier,
  no slot, no ledger line.

That is a real and previously unpriced difference: the Plotly/Altair path spends a gap-week
evaluation slot before a single pixel is drawn. The zero-dep path spends none. Note also the
`pyproject.toml` precedent for the analytics group — a hub-only dependency takes **no**
`ecosystem/dependency-baseline.yaml` row, because a baseline row is for deps consumers need to
operate a methodology mechanism. A read-path dep would inherit that, which lowers the paperwork but
does not remove the Tier L evaluation.

### 2.7 The comparison, all four axes plus tier

| | Zero-server | Windows fit | From a worktree | Dependency cost | ADR-112 tier |
|---|---|---|---|---|---|
| **A. Datasette (`serve`)** | **No** — standing uvicorn process | OK; test suite needs WSL upstream | Yes — read-only viewer over a path | 19 runtime deps (isolated via `uvx`) | Tier S if never imported |
| **A′. Datasette (`--get`)** | Yes — bakes a page, no server | same | Yes | same | same |
| **A″. datasette-lite (WASM)** | Yes — but needs a CORS host + downloads Pyodide | Browser only | n/a | none locally | n/a — **declined**, contradicts intake #9 |
| **B1. Plotly static HTML** | **Yes** | Yes | Yes (after F2) | `plotly`; **~3 MB per file** | **Tier L** — gap-week slot |
| **B2. Altair static HTML** | **Yes** | Yes — `vl-convert` ships win_amd64 wheels | Yes (after F2) | `altair` + `vl-convert-python`; ~322 KB | **Tier L** — gap-week slot |
| **B3. Hand-rolled HTML/SVG** | **Yes** | Yes | Yes (after F2) | **none**; single-digit KB | **none** — not an adoption |
| **C. `sqlite3` views** | Yes | Yes (CLI binary separate; wrap in Python) | Yes | **none** | none |

---

## 3. The three dashboards

Each is stated as: the question, the pain it answers, the source, a mocked layout, what keeps it
honest, and — the part that decides build order — **whether its data exists today**.

Mocks are described layouts. Nothing was built.

### 3.1 D1 — Organ cost: per-check duration trend

**Question.** *Which of the 43 checks is buying its runtime, and which is just spending it?*

**Pain.** `[#528]` measured the full suite at **1001 s**, and a 4-leg batch lane pays roughly that
once per lane plus once per merge — ~50 min wall-clock for one lane. The row's leg 3 is exactly
"emit `test_run` duration via the telemetry leg so the trend is measured, not felt". Today the gate
mesh's cost is felt and never measured, so there is no evidence for retiring or splitting a check.

**Source.** `events WHERE event_type='check_run'` — `name`, `duration_ms`, `ts`, `outcome`.

**Layout.**

```
ORGAN COST                                       window: last 30 days   runs: 41
--------------------------------------------------------------------------------
TOTAL GATE TIME PER RUN                                    p50 / p95 / max
  [ 43-point sparkline, one point per audit run ]          812s / 1104s / 1301s
  annotated: vertical ticks where ALL_CHECKS count changed (40 -> 43)

SLOWEST CHECKS                     p50      p95     share    fires   blocks
  journal_spine_anchor            180ms    340ms     22%       41       3
  undeclared_edges                150ms    290ms     18%       41       0   <- never blocked
  doc_rot                          95ms    140ms     11%       41       0   <- never blocked
  ... 40 more, sorted by share of total

RETIREMENT CANDIDATES  (memo line: "retire checks with fires>0/blocks=0")
  8 checks: 41 fires, 0 blocks, 31% of total gate time
  -> judgement required, not automatic
```

**What keeps it honest.** Three things, all of which a naive version gets wrong:

- **`share` must be of measured time, not of wall-clock.** Until every one of the 43 checks emits a
  duration, the denominator is partial. The panel must show `n covered / 43` and refuse to print a
  percentage while that is below 43 — the `coverage="unknown"` discipline the emit library already
  enforces at `:252-263`, applied at the read end.
- **"Never blocked" is not "useless".** A check with 0 blocks may be a check whose *deterrent* works.
  The panel labels these "retirement **candidates**", and the memo's own caveat ("after judgment")
  belongs on the page, not in a footnote.
- **The `ALL_CHECKS` count changes over time** (40 → 43 in this repo's own history). A total-time
  trend that does not annotate registry growth reads a bigger suite as a regression.

**Data today: NONE.** Blocked on F1 (no timer anywhere in `audit.py`) and on `[#529]` leg 1. This is
the most valuable dashboard and the one furthest from having a single row to draw.

### 3.2 D2 — Lane anatomy: dispatch → merge

**Question.** *Where does a batch lane's wall-clock actually go, and which stage is the queue lever?*

**Pain.** Batch 6 dispatched **width 12** in one wave. Batch 5 had two lanes whose branch names
`validate_branch_naming.LANE_BRANCH_RE` refused, silently forfeiting the ADR-110 exemption and
forcing a hand-anchoring workaround; batch 4 hit the same class and dropped two lanes. The cost of a
lane is currently a story told after the fact in a packet, per batch, by hand.

**Source — and this is the one that must not come from `events`.** Per F2, lane telemetry is written
into the worktree and deleted at teardown. So D2 is built from **git history plus the committed
manifests**, both of which survive:

- dispatch: the manifest, committed at dispatch (`[#505]` leg 1, first met by batch 6)
- merge: `batch_manifest.merged_branch_name(repo, sha)` / `is_lane_merge(repo, sha)` — the existing
  single definition of a lane merge, reused rather than re-derived
- first/last commit per lane branch: `git log` on the merged branch

**Layout.** A horizontal stage bar per lane, one row per lane, aligned on a shared time axis:

```
BATCH 6  (width 12, one wave)             dispatched 2026-08-16   [ 9 merged / 3 open ]
--------------------------------------------------------------------------------
                  dispatch->first commit | work | idle-before-merge | merge
lane a  #409...   ###                    |######|                   |##      1h42m
lane b  #210...   ##                     |####  |                   |#       0h58m
lane x  #532      ####                   |##########################|###     4h10m  <- outlier
lane y  #531      ###                    |#####                     |##      2h04m
...
--------------------------------------------------------------------------------
STAGE MEDIANS      dispatch->first  0h21m | work 1h12m | idle 0h34m | merge 0h08m
QUEUE LEVER        idle-before-merge is 24% of batch wall-clock across 9 merged lanes
REFUSED AT DISPATCH  0 lanes  (all 12 names pre-checked against LANE_BRANCH_RE)
```

**What keeps it honest.**

- **"idle-before-merge" is the whole point of the chart**, and it is the only stage that is pure
  queueing. Splitting it out is what turns a Gantt chart into a lever.
- **Merge order is serial by protocol** (`/lane-integrate` walks the queue serially), so lanes later
  in the queue inherit idle from lanes ahead. The panel must sort by merge order, not by lane letter,
  or the tail lanes look slow when they were merely last.
- **Open lanes must not be silently excluded from medians.** `9 merged / 3 open` on the header, and
  medians labelled as over merged lanes only.
- **A shallow clone cannot compute this at all.** The panel prints `unavailable` rather than a
  truncated number — the same refusal `assert_not_shallow()` (`telemetry_emit.py:219`) makes on the
  write side. This lane's own container is the worked example.

**Data today: PARTIAL and retroactive.** Git history plus 2 committed manifests (batch 5, batch 6).
Buildable, but the series is two batches long, and batch 6's lanes had not merged when this was
written.

### 3.3 D3 — Gate WARN ledger over time: the path to zero, visibly burning down

**Question.** *Is the WARN count going to zero, and which check is the one that is not moving?*

**Pain.** The night-3 lane C ledger enumerated **36 WARNs** and a concrete path to zero for each.
That path currently exists as prose in one dated audit. There is no surface on which the operator can
see it burn down, so "path to zero" is re-derived by hand every time someone asks.

**Source — and this one already exists.** Two, and the second is the find of this lane:

1. `events WHERE outcome='block'` and `event_type='blocker_fired'`, once wired — the live future.
2. **`docs/audits/*-ecosystem-audit.md` — 17 committed files, already machine-parseable.** Each
   carries a one-line roll-up and a per-check `| name | VERDICT | detail |` table:

```
2026-05-15   40 total —   8 pass, 29 fail,  3 warn
2026-06-02   60 total —  60 pass,  0 fail,  0 warn
2026-06-10   80 total —  77 pass,  2 fail,  1 warn
2026-06-14   97 total —  90 pass,  2 fail,  5 warn
2026-07-31  221 total — 159 pass,  3 fail, 21 warn, 38 n/a
```

That is a real 17-point series, extractable today with a regex and no new dependency.

**Layout.**

```
WARN LEDGER                                       source: 17 committed ecosystem-audits
--------------------------------------------------------------------------------
WARNS OVER TIME        [ stacked area, one band per check, 2026-05-15 .. 2026-07-31 ]
                       overlaid line: total registered checks (40 -> 221)
                       shaded gap: 2026-06-14 .. 2026-07-31, no digest committed

NOT MOVING                       first seen   age    path-to-zero recorded?
  undeclared_edges (x20)         2026-06-14   63d    yes - night3 ledger 1.1
  doc_rot (x7)                   2026-06-11   66d    yes - [#532] arms
  reconciled_versions (x1)       2026-07-31   16d    yes
  ...

BURN-DOWN            36 open  |  0 closed this window  |  no target date set
```

**What keeps it honest.** This dashboard is the easiest one to make lie, in four distinct ways:

- **The denominator moves.** Checks went 40 → 221 over the series. A raw WARN count that does not
  overlay registry growth reads "getting worse" when it may mean "measuring more". The overlaid
  total line is not decoration.
- **The series has a 47-day hole** (2026-06-14 → 2026-07-31, no committed digest). Interpolating
  across it would invent a trend. The gap is shaded and labelled, never bridged.
- **The last file's schema differs** — it adds an `n/a` field the earlier 16 lack. A parser that
  ignores this silently mis-attributes 38 checks. Version the parse; report `unknown` for fields a
  given file does not carry, per the constraint the emit library already encodes.
- **The 221 is the fleet roll-up across 5 repos; the 36 is the hub's own ledger.** *These are
  different denominators and must never share an axis.* The night-3 lane already recorded a
  near-miss of exactly this class — two unrelated 36s that happened to match — and warned "do not
  read the match as agreement". The same trap is one careless join away here.

**Data today: YES — 17 points, retroactive, zero new dependencies, zero blocked legs.** This is the
only one of the three that can be built before `[#529]` closes.

---

## 4. Where the dashboards live

### 4.1 The governing sources, quoted

**Intake #9** (`docs/intake/2026-07-08-func-dashboards-local-html.md`), operator direction, 2026-07-08
— the most specific source, and it is nearly a spec:

> **Must:** the Tier-4 human visualization surface is **local HTML** — a file openable inside VS Code
> in-session, **self-contained** (renders with no external host and no CDN dependency for the data).
>
> **Must:** generation writes into the **repo/working tree** (a committed-generated or gitignored
> local artifact), **not** to claude.ai hosting.

Its acceptance criteria add: renders **with no network fetch**, verified offline (AC-1); publishes
nothing (AC-2); **theme-aware in VS Code light and dark** (AC-4).

**Status caveat, stated rather than glossed:** intake #9 is **SEED** — the earliest lifecycle stage,
"awaiting technical triage". It records an operator *direction*, not a ratified decision. It is the
best evidence of intent available and it is not yet binding.

**The brief's phrasing resolves cleanly against it, and the near-conflict is worth defusing.** Intake
#9 explicitly *counters* claude.ai Artifacts as the surface; the brief asks for "the
**Anthropic-artifact shape** the operator likes". Those agree: the brief asks for the *shape* — one
self-contained, theme-aware, polished HTML page — not the hosting. A local `.html` in the tree is
that shape with no publishing boundary. No conflict, but a reader skimming both would think there is
one.

**ADR-80 §(b)** is the rule that answers committed-vs-gitignored — and intake #9's first open question
names it by name ("the ADR-80 writer-policy question"):

> the high-churn mutable pointer … is **gitignored**; the durable record … is **committed by the
> writer**.

**The live `.gitignore` shows what "high-churn mutable" has meant in practice** — six read-only
reporter digests, each gitignored with the same stated reason. `logs/FLEET-ANALYTICS.md`'s comment is
the closest analogue and is decisive: *"Frames change on every commit by construction, so committing
this would churn the tree constantly and trip session-end backpressure."*

**The `logs/` naming ruling** (2026-07-22, `[#395]`, CLAUDE.md §9): UPPERCASE-KEBAB stem, *"the
extension stays honest to the format"*. `.html` is an honest format claim, so it needs no
restyling — the ruling already accommodates a file class it never anticipated.

### 4.2 The gate, executed rather than asserted

I ran the live ADR-101 refusal gate against five candidate paths instead of reasoning about it
(`python3 -c "import validate_hermetization as v; ..."`):

```
docs/audits/2026-08-16-technical-nb4-telemetry-read.md   A=ok    B=ok    C=ok
docs/diagrams/organ-cost.html                            A=BLOCK B=ok    C=BLOCK
docs/DASHBOARD.html                                      A=ok    B=ok    C=BLOCK
logs/TELEMETRY-DASHBOARD.html                            A=ok    B=ok    C=ok
docs/audits/2026-08-16-dashboard-organ-cost.html         A=ok    B=ok    C=ok
```

Four things follow, and two of them are findings rather than confirmations:

1. **`logs/*.html` is admissible today.** No amendment, no ruling, no new home.
2. **`docs/<anything>.html` loose at the `docs/` root is refused by Rule C** — the exact class
   `docs/ORGAN-INDEX.md` belonged to, now sealed.
3. **`docs/diagrams/` is refused by Rule A *and* Rule C.** It is not in `SANCTIONED_GENRES`
   (`archive, audits, decisions, handoffs, intake`) and does not exist on disk — yet
   `templates/ARCHITECTURE-template.md:103` tells every consumer repo that diagrams *"live under
   `docs/diagrams/`"*. **The template names a home the hub's own gate would refuse.** Filed in §4.4.
4. **`docs/audits/*.html` passes all three rules** — because Rule B, by its own literal spec, only
   grammar-checks `docs/audits/***.md**`. An `.html` there is name-checked by nothing. That is a gate
   hole, not a licence, and it should not be walked through casually.

### 4.3 The proposal

**Generated dashboards live at `logs/<NAME>-DASHBOARD.html`, gitignored, with a committed digest
only where a durable record is owed.**

- **Gitignored, per ADR-80 §(b).** A dashboard regenerated from git history and an event log changes
  on **every commit** — precisely `FLEET-ANALYTICS.md`'s stated condition. Committing it churns the
  tree and trips session-end backpressure, which is the failure the six existing reporter entries all
  exist to prevent. This answers intake #9's first open question with the rule intake #9 itself
  points at.
- **`logs/`, because the gate already admits it** (§4.2 line 4) and the naming ruling already covers
  the extension. Nothing new is sanctioned; no ADR-101 amendment is needed. **This is the property
  that makes the proposal cheap**, and it is why `docs/dashboards/` — which would need an amendment —
  is not proposed.
- **The `.gitignore` line must be `logs/*-DASHBOARD.html`, and the same commit must add
  `logs/TELEMETRY.db*`** (glob, per F3 — the `-wal`/`-shm` sidecars).
- **Durable records stay where they are.** ADR-80's committed half is already served by
  `docs/audits/*.md`. A dashboard is a *view*; when a number needs to survive, it goes in an audit,
  as it does today. No second durable channel.
- **Self-contained is a build constraint, not a hope.** Intake #9 AC-1 says "verified by opening it
  offline". If a generator is built, its test asserts the emitted HTML contains **no** `http://` or
  `https://` resource reference — the mechanical form of that criterion. Note this is the criterion
  Plotly's `include_plotlyjs='cdn'` fails and `=True` passes at 3 MB, and that hand-rolled
  HTML/SVG passes at single-digit KB.
- **Theme-aware (AC-4)** via `prefers-color-scheme`, matching the Arc-5 P6 pilot which already
  demonstrated dual-theme with zero deps.

### 4.4 Two drive-by findings, filed not fixed

Both surfaced while establishing §4.2 and neither is in this lane's scope. Recording them so they are
not re-discovered.

- **`templates/ARCHITECTURE-template.md:103` names `docs/diagrams/` as where diagrams live. The hub's
  own ADR-101 gate refuses that path under Rule A and Rule C, and the directory does not exist in the
  hub.** Every consumer repo carries this template. Either the genre is sanctioned by amendment or
  the template is corrected; today the fleet's own template points at a refused home.
- **Rule B grammar-checks `docs/audits/*.md` only, so `docs/audits/*.html` (or `.csv`, `.svg`) enters
  with no name check at all.** Narrow today because only `.md` is written there. It becomes load-bearing
  the moment any generated non-`.md` artifact is proposed for `docs/audits/` — which §4.2 line 4 shows
  is currently the path of least resistance.

---

## 5. Recommendation

**Stack: stdlib `sqlite3` views as the data layer + hand-rolled self-contained HTML/SVG as the
surface, written to `logs/<NAME>-DASHBOARD.html` and gitignored. `uvx datasette` retained as the
zero-install ad-hoc explorer, never imported, never the dashboard. No charting library adopted in
Stage 2 — revisit only when a chart class appears that SVG cannot carry, and if that day comes the
pick is Altair (~322 KB, Windows wheels) over Plotly (~3 MB per file), not the reverse.**

It is the only combination that passes all four axes with no qualification, it is the only one that
is **not an ADR-112 Tier L adoption** — so it spends no gap-week evaluation slot before drawing a
pixel — and it is the one the repo has already proven once, in the Arc-5 P6 pilot's own words: *zero
deps, CSP-self-contained, theme-aware, one session.*

**Build first: D3, the WARN ledger burn-down.** Not because it is the most valuable — D1 is — but
because it is the **only one of the three whose data exists today**. D1 has no data at all until F1
is fixed (43 checks, zero timers in `audit.py`) and `[#529]` leg 1 lands. D2's telemetry source is
destroyed at worktree teardown until F2 is fixed. D3 needs neither: **17 committed
`docs/audits/*-ecosystem-audit.md` files already carry a parseable per-check verdict series**, so D3
can ship against real historical data before `[#529]` closes, and gain live `blocker_fired` rows
later without changing its shape. Building it first also proves the surface — self-contained,
offline, theme-aware, gitignored — on data that cannot be blamed for a rendering bug.

**Two prerequisites that belong to `[#529]`, not to Stage 2, and should be stated on that row before
either D1 or D2 is scheduled:** leg 1 must say *time the checks*, not merely *wire the call sites*
(F1); and the `default_db_path()` worktree split must be fixed via `git rev-parse --git-common-dir`,
the pattern `fleet_analytics.py:1075` already carries (F2). Until both land, D1 and D2 are designs
without a data source, and this report should not be read as saying otherwise.

---

## Sources

Repo (read live this session): `scripts/telemetry_emit.py` · `scripts/audit.py` ·
`scripts/validate_hermetization.py` (executed) · `scripts/fleet_analytics.py` ·
`scripts/batch_manifest.py` · `.gitignore` · `.worktreeinclude` · `pyproject.toml` · `BACKLOG.md`
`[#528]`/`[#529]` · `CLAUDE.md` §4/§5/§9 · `docs/intake/2026-07-08-func-dashboards-local-html.md` ·
`docs/decisions/ADR-80`/`ADR-101`/`ADR-112` · `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md` ·
`docs/audits/2026-07-06-arc5-buy-vs-build-verdicts.md` · `docs/audits/2026-08-15-verification-night3-warn-ledger.md` ·
`docs/audits/2026-08-16-technical-batch-6-manifest.md` · `docs/audits/*-ecosystem-audit.md` (17) ·
`templates/ARCHITECTURE-template.md`

Web:
[Datasette](https://datasette.io/) ·
[datasette on PyPI (0.65.3, deps)](https://pypi.org/pypi/datasette/json) ·
[datasette#1662 — static publish](https://github.com/simonw/datasette/issues/1662) ·
[datasette#511 — Windows tests](https://github.com/simonw/datasette/issues/511) ·
[Datasette Lite](https://github.com/simonw/datasette-lite) ·
[Datasette Lite writeup](https://simonwillison.net/2022/May/4/datasette-lite/) ·
[Datasette CLI reference](https://docs.datasette.io/en/stable/cli-reference.html) ·
[plotly.io.write_html](https://plotly.com/python-api-reference/generated/plotly.io.write_html.html) ·
[Saving Altair Charts](https://altair-viz.github.io/user_guide/saving_charts.html) ·
[altair#2271 — offline JS](https://github.com/altair-viz/altair/issues/2271) ·
[vl-convert-python on PyPI](https://pypi.org/pypi/vl-convert-python/json) ·
[vega-embed](https://github.com/vega/vega-embed) ·
[bundle-size comparison](https://npm-compare.com/chart.js,plotly.js,vega-embed)
