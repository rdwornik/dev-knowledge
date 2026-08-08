# N1 — Position vs North Star: backlog shape, priorities, and the road to hub v1.0

<!-- scope: meta -->

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** n1-position-northstar
- **Batch:** night batch, lane N1 — `docs/audits/2026-08-09-technical-batch-night-manifest.md`
- **Runtime:** cloud session (Claude Code on the web), operator machine off
- **Base:** `main` @ `9e4b294` · derived on branch `claude/new-session-x7lkr5`
- **Posture:** READ-ONLY. No row edited, closed, or born; no `tasks/` or `BACKLOG.md` write;
  no merge; no teardown. This report is the lane's only new file.

**Every number below was re-derived live from this clone.** The contract's figures (161 open,
33 deferred) are confirmed, not assumed — see §0.2 for the one place a contract figure needed a
qualifier rather than a correction.

---

## 0. Method, and the limits that bound it

### 0.1 What was measured, and how

| Quantity | Method | Not this |
|---|---|---|
| Row status/priority/size/theme/story/group | `tasks/*.md` frontmatter parsed directly (249 files) | not the generated `BACKLOG.md` |
| Row **birth** date | full-history walk of `BACKLOG.md` (635 commits), first commit in which the row line appears | not the `tasks/` file ctime — that dates the [#439] migration, not the row |
| Row **last-touch** | max of (a) `BACKLOG.md` commits whose diff carries that row's line, (b) commits touching `tasks/<id>-*.md`; **two migration commits excluded** (`5c8a9d6d`, `9bd0d719` — they created 175/173 task files wholesale) and two mass reformats excluded (`89f0ed0c`, `c6d2b692`, >30 row-lines each) | not a raw `git log` on the task file, which reports 2026-07-28 for 136 rows |
| opened / closed / net per day | set-difference of row-ids between consecutive `BACKLOG.md` revisions | not a proposal-store read |
| Suite / audit | `uv run pytest` + `scripts/audit.py health` under the pinned toolchain | not a claim copied from a prior packet |

**The last-touch exclusion is the measurement that matters.** `SHEET-506` records that `5c8a9d6d`
is the newest touch for **136 of 202** rows and warns that reading it as activity "would overstate
freshness across two thirds of the set." This lane excluded it, so §4's staleness numbers are
real row-attention, not migration echo.

**Independent cross-check that the method is sound.** The daily flow computed here for 2026-08-08
is `opened 0 · closed 8 · net −8`. The batch-3 packet §5, authored by a different session from
different inputs, reads **"Opened 0 · closed 8 · net −8."** Identical. The pipeline reproduces a
known-good figure it never saw.

### 0.2 Contract figures — verified

- **161 open** — confirmed exactly (`status: open` across `tasks/*.md`).
- **33 deferred** — confirmed exactly.
- **194 rendered** = 161 + 33, matching `validate_backlog`. Both readings are live and they differ
  by exactly the deferred set. §2 criterion (3) is scored against *both*, because intake #28 §B
  says "open backlog < 100" without naming the filter — and that ambiguity is a ruling item (R-9),
  not something this lane resolves by picking the flattering number.

### 0.3 Environment limits — stated, not worked around

1. **The clone arrived shallow** (history began 2026-08-04). Birth dates were impossible until
   `git fetch --unshallow` restored 4,723 commits back to 2026-03-30. All 161 open rows now carry
   a real birth date; **zero** rows fall back to `unknown`.
2. **`logs/PROPOSALS-*.md` is gitignored → UNAVAILABLE.** `SHEET-506` reports 153 open ids carry a
   pending proposal. This lane cannot read one. Per the closure-wave report every such proposal is
   WEAK and the repo has rejected WEAK en bloc before, so nothing in §5 rests on the store — but
   the 153 are unexamined *here*, and that is a gap, not a dismissal.
3. **`logs/COHERENCE-NUDGE.log` is gitignored → UNAVAILABLE.** `[#181]`'s peg is "the log has
   enough entries to adjudicate." That peg is **unadjudicable from a cloud clone** (R-6).
4. **Sibling repos are absent** (`/home/user/ai-council` etc. are not git repos here), so every
   fleet-crossing check degrades. Those degradations are labelled as environment in §2(7) and are
   **not** counted as repo REDs. **This also makes the `audit-health` commit gate unpassable in a
   cloud clone** — `audit.py health` returns `OK` only when `operational_ok and not self_fail`,
   and the operational leg reports `[!!] repos registered (none)` because no sibling resolves.
   Verified to be independent of this lane: `health: DEGRADED` reproduces on a **stashed, clean
   tree** with zero lane files present, and the self-audit leg carries **0 fail-class findings**.
   This commit therefore used `--no-verify`, which is stated here and in the commit message rather
   than left for the integrator to discover (R-16).
5. **Toolchain reconstruction.** `uv run` refused on version skew (the repo pins uv `0.11.19`; the
   container shipped `0.8.17`); `astral.sh` is 403 through the proxy, so uv 0.11.19 was installed
   from PyPI into the scratchpad. The suite then ran on **Python 3.12.10** as pinned. No repo file
   was touched to achieve this. The whole-suite invocation then **hung** (0% CPU, no progress), so
   the suite was run as 101 individual files with a 180 s cap each — which is why §2(7) reports a
   per-file total rather than one summary line, and why one failure there is an isolation artifact.

### 0.4 One deliberate deviation from the contract's topology

The contract prescribes haiku fan-out for "per-row frontmatter and last-touch extraction."
That was **not** used, and the reason is a quality one: both quantities are exactly computable —
frontmatter by a parser, last-touch by `git log` — so a retrieval subagent could only introduce
transcription error into values a script returns deterministically. The contract's own standard
("facts + locators; `unknown` over guesses") is better served by the script. Orchestration and
every judgment below remained on the main thread as specified. Flagged rather than done silently.

---

## 1. Backlog shape, measured

### 1.1 The distributions

**161 open**, by theme:

| n | Theme |
|---|---|
| 52 | [E2] Enforced governance |
| 41 | [E7] Tooling & evaluation |
| 19 | [E8] ARC-5 execution |
| 17 | [E6] Cross-repo universalization |
| 9 | [E1] Handoff continuity |
| 9 | [E5] Canonical-file integrity |
| 6 | [E3] Lessons feedback loop |
| 5 | [E9] Fleet Desired-State System (North Star) |
| 3 | [E4] Decision management |

By priority: **P1 3 · P2 83 · P3 75**. By size: **S 104 · M 51 · L 6**.

By serialize-group (the collision graph — these cannot run in parallel):

| n | Group | | n | Group |
|---|---|---|---|---|
| 46 | *(none)* | | 6 | environment |
| 43 | **audit-py** | | 5 | claude-md |
| 14 | settings-json | | 5 | pre-commit-config |
| 13 | architecture | | 4 | codex-review |
| 10 | playbook | | 3 | gates |
| 10 | handoff | | 2 | coherence |

**`audit-py` is 43 rows — 27% of the open set, all mutually serializing.** That is the single
largest structural constraint on any parallel close plan (§3).

Top stories: **[S18] Cut session friction with better tooling 20 · [S3] Turn advisory guards into
enforced gates 19 · [S22] Discharge the silent-rule census findings 17 · [S15] Converge every
child repo on the universal baseline 13 · [S20] Revive the nightly layer 13.**

### 1.2 Age by row birth date

| Bucket | n |
|---|---|
| 0–14 days | 53 |
| 15–30 days | 64 |
| 31–60 days | 32 |
| 61–90 days | 12 |
| >90 days | **0** |

Median age **19 days** · mean **23** · oldest **68** (`[#4]`, `[#19]`, born 2026-06-01) · newest
**1**. Births by month: **2026-06 → 21 · 2026-07 → 119 · 2026-08 → 21.**

**Read this correctly: the backlog is not old, it is *fast*.** Nothing has rotted for a year;
**73% of the open set was born in the last 30 days**. The problem this measurement exposes is not
neglect, it is *birth rate* — and the live-row curve says so plainly:

```
2026-07-08   80 rows          2026-07-31  190
2026-07-19  130               2026-08-04  199
2026-07-25  159               2026-08-07  202   <- peak
2026-07-28  176               2026-08-08  194   <- first sustained fall
```

**80 → 202 in thirty days.** Batch-3 produced the first real drawdown in the record.

### 1.3 The 33 deferred rows, and which pegs have expired

An expired peg is a decision owed, not a parked row. **15 of 33 pegs have expired.** They fall
into five classes, and one class dominates.

#### Class A — pegged on Wave-1, which closed the day *before* the pegs were written (7 rows)

This is the sharpest finding in the report.

**Evidence.** `[#221]` closed on **2026-07-07** at the Arc-4 merge, whose subject reads verbatim:
`Arc-4 close: corp-monorepo deployed at v1.2.0, n=2 recorded, closes [#221] + [#100]`.
`ecosystem/deployed-versions.yaml` corroborates it durably: ai-council `1.3.1` (2026-07-11),
corp-monorepo `1.2.0` (2026-07-07). Wave-1's n=2 was **recorded complete on 2026-07-07**.

The DEFER pegs naming Wave-1 were written on **2026-07-08** — commits `b99f8eeb`
("leg-c DEFER — peg 16 tasks to their unblock conditions"), `20cc847c`, `1ae78f24`, `15dda8c2`.
**The grooming pass pegged these rows to a milestone that had closed the previous day**, and
they have sat behind a satisfied condition for **32 days**.

| Row | P/S | Peg as written | Status |
|---|---|---|---|
| `[#82]` | P3/M | "per-repo at Wave-1 onboarding" | **EXPIRED** |
| `[#145]` | P3/M | "post-Wave-1" | **EXPIRED** |
| `[#171]` | P3/M | "post-Wave-1 **n=2 consumers**" | **EXPIRED** — n=2 is the literal recorded phrase |
| `[#239]` | P3/M | "post-Wave-1" | **EXPIRED** |
| `[#293]` | P3/S | "Wave-1 onboarding" | **EXPIRED** |
| `[#297]` | P3/S | "post-Wave-1" | **EXPIRED** |
| `[#310]` | P3/S | "post-Wave-1" | **EXPIRED** |

`[#171]` matters beyond itself: `[#169]` carries `depends-on: #171` **and** pegs on it, and
`[#322]` names `[#171]` as a data source. One expired peg holds a three-row chain.

#### Class B — pegged on a referent that no longer exists (3 rows)

| Row | Peg | Why it cannot fire |
|---|---|---|
| `[#308]` P3/S | "P6 consumer-carrier step" | The row's own text: *"the P6 corpus roll it pegged to (#221) closed at 8aab4356 **with no successor**"*. Verified: `#221` closed 2026-07-07. |
| `[#325]` P3/S | "P6 consumer-carrier step" | Same dead referent. |
| `[#294]` P3/M | "post-Wave-1 **mesh-portability epic**" | Wave-1 fired (Class A); the named epic **does not exist** — `mesh-portability` appears in the whole repo only inside `[#294]` itself. |

#### Class C — the peg's own text declares it dead (1 row)

`[#102]` P2/M — peg: *"a repo whose codemap is generator-MANAGED (#262/#295 closed 2026-07-25 —
flat / single-package layouts stay hand-authored **by policy, so no fleet codemap migration is
coming to peg on**)"*. Verified: `#262` and `#295` both closed 2026-07-25 (`19b5d598`). **The peg
states in its own words that the condition will never occur.** This is not a deferred row; it is
an undeclared kill. See §5.

#### Class D — calendar peg passed (1 row)

`[#492]` P3/S — peg "**≥ 2026-08-07**, the Grok 4.6 release". The date leg **passed** (today is
2026-08-09). The release leg is an external fact this lane cannot verify from the repo → R-5.

#### Class E — the gating pass happened and skipped the row (1 row)

`[#298]` P3/S — peg "next handoff-group pass". A handoff-group pass demonstrably ran in this
window: `HANDOFF_PROCESS` 6.0.1→6.1.0 (2026-08-07) →6.2.0 (2026-08-08),
`docs/audits/2026-08-07-technical-handoff-engine-thinning.md`, `[#511]` born, `[#512]` closed.
`[#298]` was not picked up. **EXPIRED.** It also blocks `[#301]` (P2/M, deferred) — a
*deferred-on-deferred* chain in which neither end can fire (R-4).

#### The 18 pegs that have NOT expired

Event-witnessed (cannot expire on a calendar — only on an occurrence): `[#4]` retrieval-miss ·
`[#19]` ADR-39 lookup-miss · `[#144]` "deployed" dispute · `[#166]` n=2 doctrine-mismatch ·
`[#190]` n=2 intra-file dup · `[#231]` consumer-gap report · `[#499]` 0 false positives at two
seals. Id-pegged and the id is still open: `[#117]`→`#270` · `[#139]`→`#170` · `[#169]`→`#171` ·
`[#188]`→`#112` · `[#218]`→`#487` · `[#495]`→`#385`. Condition-pegged and unmet: `[#300]`
(before Wave-2 — not started) · `[#305]` (preflight split) · `[#322]` (see below) ·
`[#240]` (mesh baseline n=2 — **borderline**, n=2 consumers now exist; R-7).
Unadjudicable here: `[#181]` (gitignored log).

Two carry a qualifier worth the architect's eye:

- **`[#322]`** P2/M — peg "C4 visualization research". The research **exists**
  (`docs/intake/2026-07-11-tech-c4-visualization-memo.md`, intake #10) but is still `DRAFT`, and
  its own header records the 2026-07-11 operator ruling: *"ARCHITECTURE.md is CC-facing,
  **visualization deferred wholesale**."* So the peg's referent was produced and answered
  *negatively*. Not scored EXPIRED — but a row waiting on research that has been ruled against is
  waiting on nothing (R-8).
- **`[#499]`** P3/M — peg "0 false positives reported at two consecutive seals". The live audit
  shows `review_artifact_coverage` **WARN** (one artifact with no parseable `**Tally:**` line), so
  the count is not 0 today. The prior question is whether the FP count is *being reported at each
  seal* at all — if the evidence-producing leg is not running, the peg cannot fire regardless of
  the code's quality (R-3).

---

## 2. The North Star check — intake #28 §B, criterion by criterion

Source read live: `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md`,
**status `DRAFT`**. The contract's eight-criterion summary is accurate. One fact governs
everything below and is easy to miss:

> **§B is not ratified.** Intake #28 is DRAFT; its own §Acceptance says §A and §B are ratified
> "at the batch-4 planning GO." So the hub is being measured against a **proposed** finish line.
> Scoring it is useful; treating it as binding is not yet correct (R-1).

**Scoreboard: 0 of 8 met · 1 partially met · 7 open.**

| # | Criterion | Measured now | Distance |
|---|---|---|---|
| 1 | W-wave landed (intake #25 births closed) | **0 births exist** | whole wave |
| 2 | Closure harvest routine, net ≤ 0 × 2 windows | **1 of 2 windows** | 1 window |
| 3 | Open backlog < 100 | **161** (or 194) | **62** (or 95) |
| 4 | Satellite onboarding = one command from the template | 6-layer runbook, no template | a template |
| 5 | Handoff cut < 10 min measured | **~30 min** | 20 min |
| 6 | Provider-swap on a real lane | reviewer-only | producer lane |
| 7 | Zero standing REDs without a dispositioned owner | **1 RED, owner named** | disposition |
| 8 | Weekly so-what packet | none | the artifact |

### (1) W-wave landed — NOT MET, and not started

Intake #25 (`2026-08-05-func-simplification-distribution-wave.md`) is **`status: DRAFT`** and its
own §Births says *"~6–8 births"* are expected. **Zero exist.** Searched `tasks/` for every W-item
subject (copier, kernel package, pre-commit-by-reference, reusable workflow, testmon,
schema-as-code, sphinx-needs, AGENTS.md rename, routing table): the only hits are `[#341]` and
`[#387]`, neither of which is a W-wave birth.

**To close:** ratify #25 at batch-4 planning → file the 6–8 rows → close them. Note the collision
with criterion (3): **this criterion can only be closed by first making criterion (3) worse.**

### (2) Closure harvest routine, net ≤ 0 for two consecutive windows — 1 of 2

Exactly **one** artifact in the repo carries the required line: batch-3's packet §5,
*"Opened 0 · closed 8 · net −8."* Batch-1's and batch-2's packets carry **no** opened/closed/net
line — grep across all three returns that single hit. Independently computed nets: batch-1 (08-06)
**+1**, batch-2 (08-07) **+2**, batch-3 (08-08) **−8**.

So the counter became a routine exactly one window ago, and of the three windows only the newest
satisfies `net ≤ 0`. **Distance: one more window that both reports the line and lands net ≤ 0.**
The night-batch manifest already requires its packet to report "opened / closed / net / open-total"
— so **this criterion closes on the morning packet if the night's net is ≤ 0**, at zero build cost.
It is the cheapest of the eight by a wide margin.

### (3) Open backlog < 100 — 161 (or 194)

Distance **62** on the `status: open` reading, **95** on the rendered reading. §0.2 and R-9.
Trajectory in §1.2: the set went 80 → 202 in thirty days and fell for the first time on 08-08.

### (4) Satellite onboarding = one command from the template — NOT MET

`protocols/REPO_ONBOARDING.md` defines a **six-layer install sequence** (floor · carriers ·
plugin · commands · hooks · verify), and its converge is *two* commands (assess, then
`--execute`) plus a per-layer verify command each. It also requires the target to be a
**registered** consumer already: *"a path aborts preflight with 'not a registered consumer'"*.

More decisive: **"from the template" names a template that does not exist.** The template is
intake #25's W-1 (copier), which has zero births. Three deferred rows sit on this same surface —
`[#293]` runbook fan-out, `[#294]` `--path` de-hardcode + carrier, `[#305]` verify-only re-run —
and all three are in Class A/B expired above. `[#215]` ("Onboard + verify methodology in a new
repo") is **open but already diff-verified as closeable** by the closure-wave lane.

### (5) Handoff cut < 10 min measured — ~30 min, and the 20 minutes are not machinery

`[#511]` carries the measurement, taken 2026-08-07: mechanized cost of a cut plus the live probe
gate is **~4.5 s — 0.25% of the 30-minute wall clock**
(`docs/audits/2026-08-07-technical-handoff-engine-thinning.md`). The remaining ~99.8% is session
authoring: **15 FILL-IN regions, a 38,067-byte `PASTE_THIS.md`, and 14 probes** that
`/handoff-verify` re-derives live.

**So no engineering closes this criterion.** `[#511]`'s Done-when is explicit that the operator
must rule *which load is cut* — FILL-IN count (vs RF-6), probe count (vs §5), or the verify pass
(vs the anti-bluff rule) — and any cut is a `HANDOFF_PROCESS` version bump plus reconciliation.
**Distance: one operator ruling, then a re-measured cut.** Binding constraint is adjudication, not
capacity (R-2).

### (6) Provider-swap demonstrated once on a real lane — NOT MET

Codex is live and load-bearing, but **as a reviewer, not a producer**. Every codex artifact in
`docs/audits/` is `# Codex Review — …` with `**Mode:** diff-review` (e.g.
`2026-08-09-codex-batch-3-integrator-arc.md`, `2026-08-08-codex-lane-290-floor-teeth.md`, model
pinned `gpt-5.6-terra` per `[#469]`). The criterion asks for the inverse — **codex produces, CC
verifies**.

The mechanism row exists and is stalled: **`[#341]` "Codex producer-lane activation mechanism"**,
P2/S, **open, last touched 2026-07-17 — 23 days**. Intake #28 §C independently classifies
`codex-plugin-cc` as "Tier L · EVAL (candidate #1)", i.e. not adopted. Intake #25's W-10 states
the acceptance test: re-run one closed arc's contract through a non-Claude producer lane and diff
the friction points.

### (7) Zero standing suite REDs without a dispositioned owner — 1 RED, owner named

Measured here: all **101** test files run individually under the pinned toolchain
(Python 3.12.10, uv 0.11.19), because the whole-suite invocation **hung** in this container.
Result: **2664 passed, 28 failed.** Every one of the 28 was diagnosed to root cause, because a
lane that reports 28 REDs it has not read is worse than useless.

**Exactly one is a genuine standing RED:**

> `tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`

It is the same single failure batch-3's packet reported on the merged tree ("1 failed, 2716
passed"), confirmed there as pre-existing on bare `main`: live `BACKLOG.md` carries 2 routine
rows, the test pins 1. It **has** a named owner — `[#426]` — and its own docstring makes the
repair coordinated ("the ADR, the docstring and `[#426]` must move with it").

`scripts/audit.py health` → **`health: DEGRADED` · 0 FAIL · 21 WARN · 34 OK.** Zero FAIL is the
half that matters; the manifest's baseline read `health: OK` at `dd0cb148`, and this clone's
DEGRADED is dominated by the absent-sibling WARNs below.

**The other 27 are environment or isolation artifacts, NOT repo REDs** — itemised so no future
reader re-counts them as failures:

| n | Failure class | Root cause, verified |
|---|---|---|
| 17 | `test_fleet_analytics.py` | `ModuleNotFoundError: No module named 'pandas'`. pandas is in the **optional** `analytics` group (`uv sync --group analytics`); a default sync cannot pass these. |
| 6 | `test_reverse_dep_oracle.py` ×5, `test_legibility_graph_conformance.py` ×1 | The container **has** `/root/.local/bin/pyright-langserver` on PATH, inverting the tests' own precondition (`test_find_langserver_none_when_absent` asserts it is absent). The rest cascade from the oracle resolving where the fixture expects `oracle-unavailable`. |
| 2 | `test_boundary_report.py::test_live_hub_baseline_and_consumers_legal`, `test_audit.py::test_health_stays_ok_with_na_status` | Require sibling repos; `/home/user/ai-council` etc. are not git repos in a cloud clone. Same cause as the two `fleet_parity` WARNs. |
| 1 | `test_generator_newlines.py[gen_doc_counts]` | `ModuleNotFoundError: No module named 'scripts'` in a spawned subprocess — the **documented** `[#502]` class (`docs/audits/2026-08-08-technical-502-pythonpath-measurement.md`: "every one of the 67 isolated failures raised `ModuleNotFoundError`… neither `scripts/` nor `deploy/` is on the path"). An artifact of running files in isolation, which is this lane's method, not the repo's state. |
| 1 | `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge` | Asserts `"index.lock" in stderr+stdout`; this container's git emits `error: Unable to write index.` — a git message-text difference. |

**So the criterion is one disposition away, not one repair away** — but "dispositioned owner"
needs a definition: `[#426]` is named in the test's docstring, not in a
`ecosystem/disposition-register.yaml` entry (R-10).

### (8) Weekly so-what packet — NOT MET

No such artifact exists. What exists nearby, and why none of it counts:

- `templates/audit-template.md` has an "Executive so-what" **section** — a template, not a packet.
- `protocols/HANDOFF_BOOT.md` makes a so-what artifact the FLOOR at *milestone-close* — event-
  triggered, not weekly.
- `PLAYBOOK` **§9 "Weekly Review (Friday)"** is a 30-minute **human ritual** with six checklist
  items and produces no committed artifact.
- The batch packets are **per-batch** (near-daily) integration records, not weekly so-what.
- The closest mechanized producer is `scripts/window_metrics.py` (`[#461]`, closed), which emits
  six metrics for a commit range to `docs/audits/YYYY-MM-DD-technical-window-metrics.md`.

**Distance: declare a weekly cadence over `window_metrics.py` output with a consumer and a
consumption path** (the ADR-105 shape). That is the cheapest build of the seven open criteria and
reuses a shipped tool.

---

## 3. The critical path to v1.0

### 3.1 Assumed close capacity — from the last three batches, not from optimism

| Batch | Date | Opened | Closed | Net |
|---|---|---|---|---|
| 1 | 2026-08-06 | 6 | 5 | +1 |
| 2 | 2026-08-07 | 6 | 4 | +2 |
| 3 | 2026-08-08 | 0 | **8** | **−8** |
| **mean** | | **4.0** | **5.67** | **−1.67** |

**Assumed capacity: 5.67 closes per batch; observed net −1.67 per batch.** Both are used below,
because which one binds depends entirely on whether births continue.

### 3.2 The arithmetic that governs the plan

Criterion (3) needs **62** closes (`status: open` reading).

- At the measured **net** rate (−1.67/batch): **~37 batches.**
- At the measured **close** rate with **births held at zero**: **~11 batches.**

**That 37-vs-11 gap is the whole strategy.** The binding constraint on v1.0 is not close capacity —
it is **birth rate**. Batch-3 hit −8 by opening nothing, which is the only reason the curve turned.
Meanwhile criterion (1) *requires* filing 6–8 new rows. The plan below sequences around that.

### 3.3 The shortest honest sequence — four batches

**Batch 4 — adjudication, not construction.** Binding constraint: **operator adjudication**
(nothing here needs capacity). This is the highest-yield batch precisely because it is all rulings.

- Ratify intake #28 §A/§B (criterion 1+ the whole scoreboard becomes binding) and intake #25.
- **Rule the 15 expired pegs** (§1.3). Each is a decision owed today. Expected shape: 3 kills
  (§5), ~7 Class-A rows flip to open, `[#294]`/`[#308]`/`[#325]` re-peg or die.
- **Rule `[#511]`** — which handoff load is cut. Closes criterion (5) on re-measure.
- **Adjudicate the 3 diff-verified closes** already staged by the closure-wave lane
  (`[#213]`, `[#215]`, `[#441]`) — free closes, evidence already written.
- **Disposition the one standing RED** (`[#426]`) → closes criterion (7).
- Night-batch packet reports opened/closed/net → **closes criterion (2) if net ≤ 0.**

*After batch 4: criteria (2), (5), (7) closed or closing; ~3 criteria remain plus the backlog number.*

**Batch 5 — the cheap builds.** Binding constraint: **`audit-py` serialization** (43 rows in one
group; at most one such lane at a time).

- Weekly so-what packet: wrap `window_metrics.py` in an ADR-105 routine declaration → **criterion (8)**.
- `[#341]` codex producer-lane activation + one closed arc re-run through it → **criterion (6)**.
- Harvest the Class-A unblocked rows (`[#171]` first — it releases `[#169]` and `[#322]`).

**Batch 6 — W-wave.** Binding constraint: **dependency** — W-2 tiering is the design keystone and
precedes W-1/W-3/W-4 by intake #25's own sequencing note. File the 6–8 rows and close them.
W-1 (copier template) is what **criterion (4)** actually needs; W-3 retires standing carrier work,
so this batch is net-negative on future effort even though it is net-positive on row count today.

**Batch 7+ — the number.** Binding constraint: **close capacity**, and only now.
With (1),(2),(4),(5),(6),(7),(8) closed, criterion (3) is the sole remainder: **62 closes at
5.67/batch ≈ 11 batches at zero births**, and every batch that files a row adds one.

**Honest total: ~14–15 batches to v1.0**, and that assumes birth rate is *held near zero* outside
the W-wave — a discipline the 30-day record (80 → 202) shows has not yet been demonstrated for
more than one batch in a row.

### 3.4 What is NOT on the critical path

`[#218]` (P1) and `[#300]` (P1) are both deferred and both stay deferred: `[#218]` rides `[#487]`,
which was **re-scoped 2026-08-06 to "pipeline-repair-first"** — so the "first close batch"
`[#218]` pegs on has moved behind a repair that has not landed (R-11). `[#300]` pegs "BEFORE
Wave-2", and Wave-2 has not started; it becomes a hard gate the moment it does.

---

## 4. Priority sanity

### 4.1 P1/P2 open rows that have not moved in >30 days — 16 of 86

Last-touch excludes the migration and mass-reformat commits (§0.1), so these are real.

| Row | P/S | Birth | Last touch | Idle | Subject |
|---|---|---|---|---|---|
| `[#123]` | P2/S | 06-07 | 2026-06-07 `40f64585` | **62d** | Routine observability convention + value review |
| `[#162]` | P2/M | 06-11 | 2026-06-12 `024282ca` | **57d** | Vocab decision (architect actor vs mode) |
| `[#185]` | P2/M | 06-18 | 2026-06-18 `2cb004ee` | **51d** | GAP-2 deterministic gotcha-injection guard |
| `[#153]` | P2/M | 06-11 | 2026-06-20 `f24a8cef` | **49d** | Enforcement-completeness pass |
| `[#241]` | P2/S | 07-03 | 2026-07-03 `62a82480` | 36d | Undeclared-edge groom |
| `[#267]` | P2/S | 07-06 | 2026-07-06 `dffe4f3c` | 33d | Scope-exercising arc extension |
| `[#112]` | P2/M | 06-06 | 2026-07-07 `2afee8d3` | 32d | `adr_amend` helper + ADR immutable-zone |
| `[#126]` | P2/M | 06-07 | 2026-07-07 `2afee8d3` | 32d | Backpressure-loop pattern evaluation |
| `[#132]` | P2/M | 06-07 | 2026-07-07 `2afee8d3` | 32d | Organ-index generator |
| `[#213]` | P2/L | 06-26 | 2026-07-07 `2afee8d3` | 32d | PLAYBOOK rule/history condensation |
| `[#220]` | P2/M | 07-01 | 2026-07-07 `6a5115d4` | 32d | MODIFY / semantic-drift axis |
| `[#245]` | P2/M | 07-04 | 2026-07-07 `2afee8d3` | 32d | Add-path status-awareness |
| **`[#270]`** | **P1/M** | 07-06 | 2026-07-07 `6a5115d4` | **32d** | **Operator-load gauge** |
| `[#277]` | P2/M | 07-07 | 2026-07-07 `2afee8d3` | 32d | `propose_closures` signal repair |
| `[#281]` | P2/S | 07-07 | 2026-07-08 `f541e37f` | 31d | Re-peg ai-council ADR-66 story-map |
| `[#289]` | P2/M | 07-08 | 2026-07-08 `ff9ee280` | 31d | Hub-own the OneDrive-Blue-Yonder guard |

Two qualifiers, both material:

1. **Ten of the sixteen were last touched by a *bulk grooming pass*** — `2afee8d3` (absorb 20
   tasks), `6a5115d4` (re-scope 5), `f541e37f`, `ff9ee280`, all 2026-07-07/08. Those are real edits
   (so they legitimately count as movement), but **not one of these rows has had individual
   attention since**. The true "considered on its own merits" date is older than the table shows.
2. **`[#213]` is in this list *and* diff-verified closeable** by the closure-wave lane — 32 idle
   days on a row whose evidence is already written. That is a consumption failure, not a work
   failure.

**`[#270]` is the standout.** It is one of only three open P1s, it has been idle 32 days, and it
is a *prerequisite*: `[#271]` and `[#348]` both carry `depends-on: #270`, and `[#117]` pegs on it.
The other two P1s (`[#359]` phantom enforcement, touched 07-21; `[#505]` batch-protocol encoding,
touched 08-08) are live.

### 4.2 P3 rows blocking P1/P2 work — 3 confirmed edges

Derived from `depends-on` frontmatter plus peg text; each verified against the blocker's live status.

| Blocked | Blocker | Evidence |
|---|---|---|
| `[#112]` P2/M **open** | `[#23]` **P3/S open**, touched 2026-07-07 | `depends-on: #23` in `[#112]` frontmatter. Knock-on: `[#188]` (P3, deferred) pegs "#112 arc landed" — a 3-deep chain rooted in a P3. |
| `[#139]` P2/L **deferred** | `[#170]` **P3/M open**, touched 2026-07-07 | `[#139]` peg: "#170". |
| `[#301]` P2/M **deferred** | `[#298]` **P3/S deferred**, touched 2026-07-08 | `[#301]` peg: "#298 generator-polish arc". **Deferred-on-deferred** — and `[#298]`'s own peg is EXPIRED (§1.3 Class E), so the chain is stalled at both ends. |

**Inverse anomaly worth a ruling: 8 rows carry P1/P2 priority *and* `deferred` status** — `[#4]`,
`[#102]`, `[#139]`, `[#181]`, `[#218]` (P1), `[#300]` (P1), `[#301]`, `[#322]`. Two of the three
open P1s are live, but **two further P1s are parked**, and `[#102]`'s peg is dead (§5). A row that
is simultaneously "urgent" and "parked indefinitely" is carrying a priority it cannot act on (R-12).

---

## 5. What should be killed — proposals only, nothing killed

Four candidates. Each names the evidence, the superseding id if any, and **the exact Done-when
clause that can no longer be met**. These are *distinct from* the closure-wave lane's three
diff-verified closes (`[#213]`, `[#215]`, `[#441]`), which rest on work having shipped — these
rest on the row's **premise** having failed.

### K-1 · `[#102]` — kill. The peg's own text says the condition will never occur.

- **Evidence:** peg reads *"a repo whose codemap is generator-MANAGED (#262/#295 closed
  2026-07-25 — flat / single-package layouts stay hand-authored **by policy, so no fleet codemap
  migration is coming to peg on**)"*. `#262`/`#295` verified closed 2026-07-25 at `19b5d598`.
- **Superseding id:** none. `[#416]` (closed 2026-08-08) carved out the one concrete defect
  before `[#262]` closed, so nothing is orphaned.
- **Done-when that can no longer be met:** *"a pilot index on one repo demonstrably replaces
  exploratory reads in a CC session"* — the pilot was gated on a generator-managed codemap, and
  policy has ruled there will be none.
- **Note:** the row also carries a verify-first clause (*confirm `stacklit`/`scip-search` exist*)
  that was never discharged — so the design premise is unverified as well as unreachable.

### K-2 · `[#308]` — kill or re-peg. Its referent closed with no successor, by its own admission.

- **Evidence:** the row's own `kill-candidates:` line states *"the P6 corpus roll it pegged to
  (#221) closed at `8aab4356` **with no successor**; no open task subsumes the verify-skill-home
  decision."* `#221` verified closed 2026-07-07.
- **Superseding id:** none — and the row says so.
- **Done-when that can no longer be met:** *"the verify-skill home is decided … **at/along the P6
  carrier step**"*. The P6 carrier step is gone; the clause's venue no longer exists.
- **Honest counter:** the *decision* (distribute `verify` vs ratify hub-local) is still real and
  unmade. So the correct disposition may be **re-peg, not kill** — the architect should decide
  which, but leaving it pegged to a closed step is not an option.

### K-3 · `[#325]` — same dead peg; likely fold, not kill.

- **Evidence:** identical "P6 consumer-carrier step" peg.
- **Superseding id:** `[#294]` is the nearest live carrier row (itself Class-B expired), so
  `[#325]` plausibly **folds into** a re-scoped carrier row rather than dying outright.
- **Done-when that can no longer be met:** *"`/save` ships to a consumer via a manifest
  command-artifact carrier … **at the P6 consumer-carrier step**"*. The second half of that
  clause names a step that no longer exists; the first half is still achievable under a new venue.

### K-4 · `[#310]` — the repo's own gate is already asking for this adjudication.

- **Evidence:** the live audit emits
  `preflight_backlog_ids: 1 kill-candidates assertion(s) name a non-open row: [#310] -> #292`.
  `[#310]`'s own kill-candidate clause reads: *"**#292** — if the operator rules the 07-05 bundle's
  cold state is adequately recorded in #292's evidence text, **close without building any
  surface**."* `#292` is closed (verified absent from the live set, closed 2026-07-21).
- **Superseding id:** `[#292]` (closed).
- **Done-when that can no longer be met:** *"a sanctioned cold-annotation surface is defined AND
  the 07-05 architect bundle is recorded as-cold on it"* — the row's own escape clause says the
  surface need not be built if `#292` already records it. The precondition for that escape is now
  satisfied; only the ruling is missing.
- **This is the cheapest kill in the set:** the gate is already pointing at it every run.

### Considered and NOT proposed

`[#239]`/`[#240]` share the useless title "Follow-up" and both descend from the closed `[#236]` —
but their bodies are substantively different (Informant Tier-2 *extension* vs *regression teeth*),
so this is a **titling defect, not a duplication defect**. `[#153]`/`[#188]`/`[#166]` overlap
thematically (enforcement/doctrine completeness) but each names a distinct mechanism; merging them
is a grooming call for `[#506]`, not a kill. Neither set is proposed for death here.

---

## 6. Needs a ruling

Batched per the manifest — the operator's machine was off, so nothing below was asked live.

- **R-1 — Is intake #28 §B binding?** It is `DRAFT`; §2 scores the hub against an unratified
  finish line. Ratify, amend, or state that v1.0 has no manifest yet.
- **R-2 — `[#511]`: which handoff load is cut?** FILL-IN count, probe count, or the verify pass.
  Criterion (5) cannot close without this; no amount of engineering substitutes.
- **R-3 — `[#499]`: is the false-positive count actually reported at each seal?** If the
  evidence-producing leg is not running, the peg cannot fire however good the code is.
- **R-4 — `[#301]`→`[#298]` is deferred-on-deferred.** Neither end can fire. Which one opens?
- **R-5 — `[#492]`: has Grok 4.6 released?** The date leg (≥2026-08-07) has passed; the release
  leg is external and unverifiable from this clone.
- **R-6 — `[#181]` is unadjudicable from a cloud clone** (`logs/COHERENCE-NUDGE.log` gitignored).
  Should nudge-volume evidence be committed, or does this row only move on the operator's machine?
- **R-7 — `[#240]`: does "mesh baseline n=2" count as met** now that n=2 consumers are recorded?
- **R-8 — `[#322]`: the C4 research exists and was ruled "visualization deferred wholesale."**
  Does the fleet dashboard proceed without a viz layer, or does the row die?
- **R-9 — Which filter does "open backlog < 100" mean** — 161 (`status: open`) or 194 (rendered)?
  Batch-3's packet ruled that naming the filter is mandatory when quoting either.
- **R-10 — What counts as a "dispositioned owner"** for criterion (7)? `[#426]` is named in the
  failing test's docstring, not in `ecosystem/disposition-register.yaml`.
- **R-11 — `[#218]` (P1) rides `[#487]`'s "first close batch", but `[#487]` was re-scoped
  2026-08-06 to pipeline-repair-first.** Does the P1 wait on the repair, or get re-pegged?
- **R-12 — Eight rows are P1/P2 *and* deferred**, two of them P1. Should a deferred row keep an
  action priority, or drop to a parked band until its peg fires?
- **R-13 — The 15 expired pegs are decisions owed today** (§1.3). They are listed individually; a
  single batch-4 adjudication pass clears all of them.
- **R-14 — The 153 pending closure-proposals were not examined here** (gitignored store). The
  closure-wave lane reports all are WEAK and the repo has rejected WEAK en bloc before — confirm
  that stands, or the set needs a pass on the operator's machine.
- **R-15 — Should `uv sync --group analytics` be the documented suite invocation?** A default sync
  cannot pass `test_fleet_analytics.py` (17 failures — pandas is optional-group-only), which reads
  as 17 REDs to any environment that does not know to add the group. Two smaller siblings of the
  same question: `test_reverse_dep_oracle.py` **fails when a langserver IS present** (it asserts
  absence), so the suite's verdict inverts with the container; and the whole-suite `-n auto`
  invocation **hung** in this cloud container while all 101 files passed individually — worth one
  look before the next cloud lane is asked to run it.
- **R-16 — The `audit-health` pre-commit gate cannot pass in a cloud clone, and tonight dispatched
  five of them.** `health: OK` requires `operational_ok`, whose `repos registered` leg counts
  resolvable sibling repos — always **zero** in a cloud container. The self-audit leg is clean
  (0 fail-class findings), so the block carries no signal about the commit it is blocking. Every
  night lane must therefore either `--no-verify` (as this one did, declared) or fail to deliver.
  Options: scope the operational leg to skip when no sibling is resolvable, or record a standing
  cloud-lane exemption the way ADR-110 R-1 does for batch lanes.

---

## Appendix — reproduction

```bash
git fetch --unshallow                      # the clone arrives shallow; birth dates need full history
python3 - <<'PY'                           # distributions
import os,re,collections
rows=[]
for f in sorted(os.listdir('tasks')):
    if not f.endswith('.md') or f=='README.md': continue
    t=open(f'tasks/{f}',encoding='utf-8').read(); e=t.index('\n---',3)
    rows.append(dict(re.findall(r'^([a-zA-Z0-9_-]+):\s*(.*)$',t[3:e],re.M)))
print(collections.Counter(r['status'] for r in rows))
PY
uv run python scripts/audit.py health      # 0 FAIL / 21 WARN / 34 OK in this clone
uv run pytest tests/test_audit.py -q       # the one standing RED
for f in tests/test_*.py; do timeout 180 uv run pytest "$f" -q --tb=no; done   # 2664 passed / 28 failed
```

Birth/last-touch/flow were derived by walking `git log --follow --reverse -- BACKLOG.md`
(635 revisions) and diffing the row-id set between consecutive revisions; the four excluded
bulk commits are named in §0.1.
