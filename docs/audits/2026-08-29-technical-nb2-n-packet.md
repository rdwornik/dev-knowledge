# NB2 · WAVE 2 · LANE N — DB-1: the dashboard successor — hand-back packet

**Batch:** night-batch-2, wave 2 · **Lane:** N (DB-1) · **Substrate:** local
**Branch:** `worktree-lane-n-1-db-dashboard-successor` · **Consumer:** the nb2 wave-2 integrator
**Contract:** `C:\Users\1028120\Downloads\NB2-W2-LANE-N-DB1-dashboard.md`, frozen 2026-08-28
(`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §DB-1) + the 2026-08-29 operator
addendum carried in the same file.

---

## 0. Ex-ante line, verbatim, and the measured result against it

> **Ex-ante (operator's acceptance verbatim):** DIRECTION visible in one glance; zero colored-table
> markdown; regenerable from the store with one command.

| # | Ex-ante clause | Measured result | Witness |
|---|---|---|---|
| 1 | DIRECTION visible in one glance | **MET.** Every `ok` panel carries a direction verdict computed over the whole window — a drawn SVG polygon plus the word `improving` / `worsening` / `flat`. Verdicts are the first element in each panel. | `test_every_rendered_panel_declares_a_direction`; the 9-line console summary below |
| 2 | Zero colored-table markdown | **MET.** No markdown table row, no table rule, and no HTML `<table>` either — the HTML half was added after a reviewer showed the original assertion would have passed a `<table>` rebuild of the predecessor. | `test_output_carries_no_table_of_any_kind` + `test_the_no_table_assertion_actually_rejects_a_table` |
| 3 | Regenerable from the store with ONE command, idempotent | **MET.** `uv run --locked python scripts/gen_trend_dashboard.py --write`. Two consecutive real runs are **byte-identical** (`cmp` clean). Idempotence required a fix: the stamp was wall-clock and is now HEAD's own commit date. | `test_main_is_idempotent_across_two_real_runs`; `cmp` of two `--out` runs |

**The one command:**

```
uv run --locked python scripts/gen_trend_dashboard.py --write
```

**Its current output (console summary, 2026-08-29, at `77096131`):**

```
open backlog rows                      IMPROVING  -6 rows
banked ledger (status: closed)         IMPROVING  +110 rows
backlog velocity (net banked - births) IMPROVING  +16 rows/week
paste / boot bytes                     WORSENING  +11232 bytes
funnel orphans (undispositioned)       INSUFFICIENT (2 pts)
doc-rot findings                       INSUFFICIENT (1 pts)
gate time per runner invocation        ABSENT
suite wall-time                        ABSENT
per-model change quality               ABSENT

wrote ecosystem\trends.html (12,358 bytes, ascii-verified)
```

---

## 1. Per-done-item verdicts

### D1 — Enumerate the actual history sources on disk and record their paths — **MET**

The contract makes this a done-item on its own. For each of the seven contracted series plus the
addendum's two, this is the store, its path, and how far back it reaches. **Measured on disk, not
inferred.**

Sample counts below are read off the rendered page (`grep '&middot; N samples'`), not estimated
from the window length — the 12-week window offers 13 weekly sample dates, and each series lands
fewer because its store does not reach that far back.

| Series | Store (path) | Tracked? | Reach | State |
|---|---|---|---|---|
| open rows | `tasks/*.md` frontmatter `status:`, per rev | yes | 2026-07-27 → now (287 commits touch `tasks/`) | ok, **5 samples** |
| banked ledger | same store, `status: closed` | yes | same | ok, **5 samples** |
| backlog velocity | banked delta vs `--diff-filter=A` on `tasks/` | yes | same (N bands = N−1 windows) | ok, **4 samples** |
| paste / boot bytes | `protocols/HANDOFF_BOOT.md` blob size, per rev | yes | 32 revisions of the file | ok, **12 samples** |
| funnel orphans | `ecosystem/audit-funnel-baseline.json` → `uncovered` | yes | **2 value-changing revisions** | insufficient, 2 |
| doc-rot findings | `ecosystem/.dev-knowledge/history/*.md` dated snapshots | yes | **1 usable point** | insufficient, 1 |
| commit-gate wall-time | `logs/TELEMETRY.db` → `events.duration_ms` | **no** (gitignored) | **file does not exist** | absent |
| suite wall-time | — none — | — | — | absent |
| per-model change quality | — none — | — | — | absent |

**Stores found and rejected as bases, with reasons** (they exist, and saying why they are not used
is part of the enumeration):

- **`logs/OPERATOR-LOAD.csv`** — the single richest daily series in the repo: 22 rows,
  2026-08-12 → 2026-08-29, nine columns (`triage, closures, dispositions, review_pending,
  backlog_p1..p3, funnel_total`), written by `scripts/fleet_health.py:122` at SessionStart.
  **Gitignored** (`.gitignore:65`), so it is absent from a clean clone and from this worktree.
  Building the surface on it would make "regenerable from the store" true only on one machine.
- **`ecosystem/*/state.yaml`** — carries the live `doc_rot` and funnel values, but is gitignored
  (`.gitignore:69`), so it has **no history at all**. It is a snapshot, not a series.
- **`logs/TOKEN-LOG.md`** — tracked, append-only, dated, and carries **per-model** token and cost
  share. Deliberately **not** used for the per-model series: usage share is not change *quality*,
  and the addendum explicitly forbids proxying that series.
- **`JOURNAL.md` `**Ledger:**` lines** — 6 lines, free-grammar prose (`unchanged`,
  `banked closures 14 → 15`, `banked closures 6→13, births 3→6, window net +3→−5`). C6's judgment
  that it "is not a series" is confirmed at 6 lines as it was at 2. Parsing it into a chart would
  be the invented history the contract forbids.

**Findings worth the integrator's attention, from the enumeration itself:**

1. **The telemetry store has never been written.** `scripts/telemetry_emit.py` exists and is wired
   (`audit.py:4438`, `block_commit_on_main.py:189`, `block_ff_push.py:234`), but `logs/TELEMETRY.db`
   **does not exist in the primary checkout either** — emission is opt-in via
   `DEV_KNOWLEDGE_TELEMETRY=1`. The C6 memo's `scripts/gen_telemetry_dashboard.py` and
   `ecosystem/telemetry-dashboard.html` were **never built**.
2. **The tracked per-day audit snapshot store went dormant on 2026-07-31** for every repo but
   `win-tooling`. It is the only *tracked* home for doc-rot history, which is why that series has
   one usable point.
3. **`doc_rot` did not exist before 2026-07-31**, so the fifteen earlier snapshots are not clean
   zeros — see §4, finding F1.

### D2 — The addendum's FIRST ACT: locate intake #50 and the L5 cost-research artifact — **MET**

Both resolve. No `MEASUREMENT-OWED`.

- **Intake #50** = `docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md` (97 lines,
  `status: READY`, `intake-id: 50`). *"Cost-and-delivery telemetry — one weekly automated report,
  and why it is the first consumer arc."*
- **The L5 artifact**, named by #50's own Status block:
  `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md` (26,063 B), paired with
  `docs/audits/2026-08-25-technical-research-delivery-telemetry-attribution.md` (R-J, 22,684 B).

**What the store's shape is, per the addendum's question.** #50 does not describe an existing
store — it *proposes* one: a weekly pull-join-render pipeline over `ccusage`, provider billing
APIs, GitHub compute billing and git delivery data, joined in DuckDB/SQLite, with only the
join-and-render script custom. **None of it is built.** The store that *does* exist is the
Stage-1 one #50 does not mention: `logs/TELEMETRY.db`, single table
`events(id, ts, event_type, name, outcome, duration_ms, context_json, run_id)`, append-only by
discipline (no UPDATE or DELETE path in the module), WAL-mode, gitignored as `logs/TELEMETRY.db*`,
relocatable via `DEV_KNOWLEDGE_TELEMETRY_DB`. **That is the store this lane renders against**, and
it currently has zero rows.

**The fence held.** This lane added no collection, no hook, and no emission. Its only telemetry
contact is a read-only `sqlite3` connection opened `mode=ro`.

### D3 — ONE analyst-grade surface rendering TRENDS over window history — **MET**

`scripts/gen_trend_dashboard.py` → `ecosystem/trends.html`. Nine panels, CSS-grid, light/dark
aware, self-contained, no external asset. Each panel carries: direction verdict + drawn glyph,
sparkline, from → to values, sample span, **its predicate as a literal string**, and its basis.

The predicate line is not decoration. C6 measured **four disagreeing "open rows" denominators** in
one repo; a chart that does not name which one it used entrenches whichever it happened to pick.

### D4 — Library-first, by measured fit, alternatives named — **MET**

**Chosen: inline SVG on the stdlib.** Measured against the criteria that actually bind here:

| Criterion | inline SVG (stdlib) | matplotlib | plotly | mermaid `xychart-beta` |
|---|---|---|---|---|
| ADR-106 dependency act | **none** — `uv.lock`/`pyproject.toml` untouched, 34 packages before and after (`git diff --stat` empty) | required | required | none |
| Output diffable as text | **yes** (12,358 B ASCII) | no (binary PNG) | no (bundled JS) | yes |
| Can render an ABSENT panel as a first-class state | **yes** | no | no | **no** |
| Can carry a per-panel predicate label | **yes** | awkward | yes | **no** |
| ASCII-only output achievable | **yes** | n/a (binary) | no | no |

**Nothing was hand-rolled that a library would have done better**, so there is no divergence to
record beyond the choice itself. The contract's own hint — *"if a stdlib/SVG render meets all three
acceptance tests, that IS the library-first answer"* — is what the measurement returns.
**Reused rather than reimplemented:** `telemetry_emit.is_shallow_repository` /
`default_db_path`, and `gitenv.scrubbed_git_env`.

### D5 — Consumer statement for the predecessor — **MET (and the answer is: archival is NOT free)**

The contract asks whether anything reads `ecosystem/conformance.html`, because *"if anything reads
it, your successor must serve that reader or the archival is not safe."* Two live consumers:

1. **A machine consumer.** `scripts/generated_artifact_freshness.py:148` declares it a gated output
   of the `conformance-dashboard` group: `outputs=("ecosystem/conformance.md",
   "ecosystem/conformance.html")`. FM-3 archiving the file **without editing that tuple in lockstep**
   leaves an audit check pointing at a moved artifact. Its evidence line is currently live and
   WARNing: `conformance-dashboard: 5d stale`.
2. **A declared operator consumer.** `docs/intake/2026-08-23-tech-generated-artifact-currency.md:39`:
   *"As the operator I open `ecosystem/conformance.html` to answer 'did the intakes pass their
   gate?'"*

**This successor does NOT serve consumer 2.** It renders direction over time; it does not answer
"did check X pass right now". They are different questions and this lane deliberately did not
widen its scope to cover both. **Reported to FM-C/FM-3 as a blocking input to the archival
decision, not resolved here.** Neither file was touched: `git show --stat` on the lane commit lists
only the three files in §2.

### D6 — Generated-artifact freshness story — **MET, and the answer is "none is owed"**

`ecosystem/trends.html` is **gitignored** (`.gitignore`, with the rationale in-file). No gate is
owed because the artifact is never committed, and a page regenerated on demand cannot be stale.

This is a deliberate inversion of the predecessor, not a convenience: the conformance dashboard's
own disease is that it is committed-generated and therefore *can* be stale — the live audit store
says so right now. Committing this page would inherit that disease and then require a second gate
to police a staleness that only exists because the file is committed.

### D7 — Hazards — **MET**

- **PYTHONUTF8 / silent mojibake:** closed **structurally**, not documented. Direction glyphs are
  DRAWN as SVG polygons, never typed as arrow characters, so the page contains no non-ASCII byte to
  launder. `--write` calls `.encode("ascii")` and then re-reads and compares the bytes it wrote
  rather than trusting exit 0. Pinned by `test_output_is_pure_ascii`.
- **cp1252 console:** the console summary is ASCII-only.
- **`validate_hermetization` Rule C:** output lands in `ecosystem/`, an existing home; the module in
  `scripts/`, the tests in `tests/`. The gate **passed** on the lane commit (see §2).
- **`Path.write_text` LF→CRLF laundering:** avoided — `write_bytes` throughout.

---

## 2. Commit SHAs, in order

| # | SHA | Subject |
|---|---|---|
| 1 | `3669f9c4ef543adff0734f73c965f5cac720b617` | `feat(telemetry): DB-1 — the dashboard successor, one trend surface over the existing stores` |

One commit. 3 files, **+1714 / −0**: `scripts/gen_trend_dashboard.py` (new),
`tests/test_trend_dashboard.py` (new), `.gitignore` (+15).

**No generated surface was regenerated** — `BACKLOG.md`, `docs/audits/README.md`,
`ecosystem/doc-counts.md`, `ecosystem/organ-index.md` and `.claude/generated/*` are untouched, and
no gate forced one. **No `tasks/` write, no row closure, no JOURNAL entry.**

**Gate state at commit** (from the pre-commit run, all `Passed`): `block-commit-on-main`,
`codemap-freshness`, `validate-hermetization`, `provider-registry-agreement`, `audit-health`,
`ruff`, `backlog-id-on-close`, `backlog-filing-backpressure`. No `SKIP=`, no `--no-verify`.

**Ratchet — measured, not assumed, as the contract requires:**

| When | detector | files | count |
|---|---|---|---|
| before first commit | `silent-rule-v5` | 61 | **443** |
| after last commit | `silent-rule-v5` | 61 | **443** |

**Delta 0.** `protocols/` and `templates/` untouched, as the wave-2 default requires. The wave-1
dispatch figure of 443 was re-measured rather than assumed and is unchanged, so lane C did not move
it.

---

## 3. Terra tally

`codex exec` over this lane's own staged diff (not `/codex-review` — a mixed doc/code diff kills
that lane). **Five rounds. Every finding in rounds 1–4 was fixed, not dispositioned.**

| Round | c | h | m | l | Outcome |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 0 | 0 | all 8 fixed |
| 2 | 0 | 6 | 0 | 0 | all 6 fixed |
| 3 | 0 | 3 | 0 | 0 | all 3 fixed |
| 4 | 0 | 2 | 0 | 0 | both fixed |
| 5 | — | — | — | — | **reviewer unreachable** — see below |

**Cumulative: c=0 h=19 m=0 l=0, all 19 fixed.**

**Round 5 did not complete.** Verbatim: `ERROR: You've hit your usage limit. Upgrade to Pro ... or
try again at 4:20 PM.` No tally was emitted. Per the contract that is one recorded line, not a lane
failure — **but the run is not being written off**, because it died *mid-investigation* of a real
hypothesis and had already emitted its measurements. It was testing whether
`git rev-list -1 --before` can select an unmerged lane commit as "the state" for a sample date. Its
own output shows the two predicates agree at every sample date where they differ (closed 52/52,
open 161/161 at 2026-08-08; closed 90/90, open 185/185 at 2026-08-22), and I finished the boot-bytes
leg it did not reach: 16493 == 16493. **So the hypothesis is measured and changes no output today.**
The sampler was moved to `--first-parent` anyway — in a `--no-ff` repo the first-parent spine *is*
main's history, so this makes it correct by construction rather than correct by luck.

**Terra was NOT run to a clean pass.** The trend 8 → 6 → 3 → 2 is converging and every round found
strictly fewer and narrower issues, but a sixth round is owed before anyone calls the module
reviewed-clean.

**The four findings that were materially wrong output, not style** — these are the argument for the
reviewer, and they are named because a packet that reports "8 findings, fixed" hides which ones
mattered:

- **R1/H1 — births matched positionally.** `collect_bands` drops sample dates from before `tasks/`
  existed, so its list is *shorter* than the sample vector; pairing them by index shifted every
  birth count. **The velocity headline flipped from `IMPROVING +12` to `WORSENING −5` when fixed.**
- **R3 — `tasks/archive/` counted as births.** A birth is a row coming into existence; the archive
  holds relocated records of rows already born. Measured: the 2026-08-22..29 window counted **57**
  additions, **21** of them archive files — a 58% overstatement. **The headline flipped back to
  `IMPROVING +16`.**
- **R2/N2 — `check_run` double-counted.** `check_run` is emitted per check from inside `audit.py`,
  which *is* the `audit-health` hook and emits its own enclosing `hook_run`. Summing both charges
  the same milliseconds twice.
- **R1/H7 — the page failed its own acceptance test 3.** A wall-clock stamp made every regeneration
  differ. Now stamped with HEAD's commit date; two real runs are byte-identical.

**Two findings forced the panel to claim less than it originally did**, which is worth flagging
because both were the surface over-claiming in exactly the way it exists to refuse:

- The `commit-gate wall-time` panel is now **`gate time per runner invocation`**.
  `telemetry_emit.current_run_id`'s own docstring states the limit: the id reaches descendants, not
  siblings, and pre-commit spawns each hook as its own child — so *"one `git commit` yields one
  run_id per emitting hook, not one for the commit"*. The original label asserted a number the store
  cannot produce.
- The missing-store message no longer says telemetry was "never enabled". File absence proves no
  store is readable *here*; it does not prove history.

---

## 4. Candidate filings — REPORTED, not filed

No `tasks/` write was made. Five candidates, each with the evidence that produced it.

**F1 — `MODEL ATTRIBUTION` (the addendum's named enabling row).** Every model-authored commit
carries a model + version signature trailer, hook-enforced, consumed by the telemetry store. That
is what would make the per-model change-quality series real. Adjacent prior art already exists:
intake #50's *Should* clause names the `Assisted-by:` / `Model:` commit-trailer convention (R-J) as
"the published cross-ecosystem standard, so adopt rather than invent". **Not built, no hook added**,
per the addendum.

**F2 — The Stage-1 telemetry store has never been written.** `logs/TELEMETRY.db` does not exist in
this worktree *or the primary*. Emission is opt-in and nothing opts in. Consequence: the gate-cost
panel is permanently absent, and `[#529]`'s store is instrumented-but-unfed. A one-line decision
(enable `DEV_KNOWLEDGE_TELEMETRY=1` in the session env) would make a real series appear within days.

**F3 — `run_id` cannot express a whole-commit gate cost.** `current_run_id` step 1 leaves the seam
open — an outer wrapper setting `DEV_KNOWLEDGE_TELEMETRY_RUN_ID` before `pre-commit` starts would
correlate a whole commit. Nothing does. Until then no reader can honestly render "commit-gate
wall-time", and this lane relabelled rather than pretend.

**F4 — The tracked per-day audit snapshot store went dormant 2026-07-31.**
`ecosystem/<repo>/history/*.md` is the only *tracked* history for audit findings; the live values
live in gitignored `state.yaml`, which has no history. Every audit-derived trend is therefore
frozen at 2026-07-31. This is why doc-rot has one point.

**F5 — `ecosystem/conformance.html` cannot be archived without a lockstep edit.**
`generated_artifact_freshness.py:148` names it in an `outputs=` tuple. **Owner: FM-C / FM-3**, and
the operator-facing question it serves (intake #42 line 39) is not served by this successor.

---

## 5. Budget decisions

- **Dependencies: zero.** No ADR-106 act. `uv.lock` + `pyproject.toml` untouched; 34 packages
  before and after. The dependency the contract pre-authorised was not needed and was not taken.
- **Ratchet: 0 spent** of a 0-headroom baseline. No `protocols/` or `templates/` edit.
- **`.gitignore` (+15 lines) is the one edit outside the declared write-scope** ("new render module
  + tests"). It is load-bearing: an ungitignored generated artifact dirties `git status`, trips
  session-end backpressure and `stale_worktrees`, and would drag a freshness gate in behind it.
  Declared here rather than left for the integrator to find.
- **Scope held.** No collection code, no hook, no `tasks/` write, no row closure, no generated-surface
  regeneration, no JOURNAL entry, no self-merge.
- **Terra rounds: five attempted, four completed.** Stopped on a hard reviewer usage limit, not on a
  judgment that the module was clean. A sixth round is owed.

---

## 6. Deviations, with owners

| # | Deviation | Owner | Note |
|---|---|---|---|
| D-1 | Output `ecosystem/trends.html` is **gitignored**, not committed | this lane | The contract asks which gate was added "or why none is owed". None is owed: the artifact never persists. Reverses the predecessor's staleness failure mode rather than inheriting it. |
| D-2 | `.gitignore` edited (+15) — outside "new render module + tests" | this lane | See §5. Minimal, rationale in-file. |
| D-3 | Panel renamed `commit-gate wall-time` → `gate time per runner invocation` | this lane | The contract names the series "commit-gate wall-time". The store cannot support that quantity — `telemetry_emit`'s own docstring says grouping by `run_id` groups runner invocations. Renamed rather than assert a number the store cannot produce. **Flagged for the architect**: if the contracted name is required, F3 is the work that would earn it. |
| D-4 | Two series render `INSUFFICIENT` rather than `ok` | store, not lane | funnel orphans (2 pts) and doc-rot (1 pt). A 3-point floor: two samples always have a slope, so a 2-point "trend" produces a confident arrow from no evidence. Named in the page legend. |
| D-5 | Terra not run to a clean pass | this lane | Round 5 hit a reviewer usage limit. §3. |
| D-6 | Predecessor's operator-facing question is not served | FM-C / FM-3 | §1 D5 / F5. Blocking input to the archival decision. |

---

## 7. Test state

**60 tests, all passing**, in `tests/test_trend_dashboard.py`. Targeted only — the full suite runs
once at integration, per the contract.

```
uv run --locked pytest tests/test_trend_dashboard.py -q     ->  60 passed
uv run --locked ruff check scripts/ tests/                  ->  All checks passed
```

**RED-first, and the witnesses are recorded rather than asserted:**

1. **Initial RED** — the whole file was written and run *before* `scripts/gen_trend_dashboard.py`
   existed: 26 tests, all ERROR on module absence.
2. **Discriminating REDs** — because "it errored before the file existed" proves the tests run, not
   that they discriminate. Two mutations were introduced into the finished module and each was
   killed by *named* tests:
   - `direction()` reading the last step instead of the window → **3 failures**, including
     `test_direction_reads_the_window_not_the_last_step`.
   - un-inverting the SVG y-axis (`y = frac*h`) → **1 failure**,
     `test_sparkline_maps_low_values_to_the_bottom_of_the_box`.
3. **Regression tests carry their finding.** Each terra fix landed with a test naming the defect —
   `test_velocity_matches_births_by_date_not_by_index`,
   `test_archived_records_are_not_counted_as_births`,
   `test_commit_gate_excludes_check_run_because_it_nests_inside_a_hook`,
   `test_parse_doc_rot_count_is_none_when_the_check_did_not_exist_yet`,
   `test_sample_dates_spans_the_full_requested_window`.

**Known REDs that are not this lane's:** none encountered. The two the contract names — the
anchor-gate probe test (RED on main since 2026-08-22) and `test_stale_worktrees` (structurally RED
in a lane worktree) — were not run, because this lane ran targeted tests only.

**One defect was found by the generator's own output rather than by review**, and it is the one most
worth recording: the first real run reported doc-rot as `WORSENING +2` over a fifteen-sample flat
line. `doc_rot` is registered check #24 and appears in **no** snapshot before 2026-07-31; those
snapshots record passing checks too, so its absence means the check did not exist. Fifteen
fabricated zeros were producing a confident headline describing nothing but a check being added —
precisely the invented history this surface exists to refuse, committed by the surface itself.
Reading the output was what caught it.

---

## 8. STOP

Lane N is complete and **STOPPED**. Branch `worktree-lane-n-1-db-dashboard-successor` at
`3669f9c4` enters the frozen queue. No self-merge, no JOURNAL entry (the integrator writes one
anchor for the whole queue — the Stop hook's demand is **declined for that reason**, per ADR-85
amendment 2026-08-03 §A5, which made that hook advisory in full; the hard leg is
`block-unanchored-push`, and a lane does not push).

---

## AMENDMENT 1 — 2026-08-29, the branch tip

*In-file amendment marker (§5 rule 3: an audit is immutable and is corrected by an amendment,
never by an in-place edit). The text above stands as written.*

**§2 and §8 name `3669f9c4` as the branch tip. That was true when they were written and is not
true now** — committing this packet advanced the branch, and a packet cannot name its own SHA in
advance. Corrected for the integrator walking the merge queue:

| # | SHA | Subject |
|---|---|---|
| 1 | `3669f9c4ef543adff0734f73c965f5cac720b617` | `feat(telemetry)` — the render module + tests + `.gitignore` (3 files, +1714) |
| 2 | `70ec1db4` | `docs(audits)` — this packet (1 file, +394) |

**Branch `worktree-lane-n-1-db-dashboard-successor` enters the frozen queue at `70ec1db4`.**
§2's "One commit" describes the *deliverable* commit enumerated in its table, which is unchanged;
the branch carries two. Both passed the full pre-commit gate set with no `SKIP=` and no
`--no-verify`.
