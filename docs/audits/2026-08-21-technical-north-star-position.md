# North Star position — measured, not narrated

<!-- scope: meta -->

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-21 · **Slug:** north-star-position
- **Base:** `main` @ `78267fdb`, clean tree; derived in worktree `north-star-position-2026-08-21`
- **Posture:** READ-ONLY on the repo. No row edited, born or closed; no intake status touched; no
  ruling made. This file plus the regenerated `docs/audits/README.md` index are the only writes.
- **Trigger:** the operator's question, verbatim — *"where are we on the North Star — L1, L2, L3,
  L4? where are our artifacts, the python? where are we on the intake rollout? I don't even know
  what to ask any more."*

**Every number below was derived live from this tree today** unless a line says otherwise. Where a
figure is quoted from an earlier artifact it is labelled with that artifact's date, because a
2026-07-31 reading is not a 2026-08-21 measurement. Where the repo does not settle a question the
answer is **UNDETERMINED** with the thing that would settle it named.

---

## 1. The North Star, quoted

### 1.1 Four candidate statements exist. They are not rivals — they are different scopes.

| # | Statement | Home | Status today | Scope |
|---|---|---|---|---|
| A | The `[E9]` user story | `BACKLOG.md:455` | live theme, 6 open rows | fleet end-state, one sentence |
| B | Intake **#16** FLEET NORTH STAR | `docs/intake/2026-07-21-func-fleet-north-star.md` | `status: ACCEPTED`, `disposition: active` | fleet end-state, full plan (§1–§6) |
| C | Intake **#28 §B** hub DONE-manifest v1.0 | `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md:29` | `status: ACCEPTED` (flipped at `3aaf5140`) | **hub** finish line, 8 clauses + 2 amendments |
| D | **ADR-109** fleet desired-state contract v1 | `docs/decisions/ADR-109-fleet-desired-state-contract-v1.md` | Accepted | the binding mechanical contract |

### 1.2 The end-state, in its own words (≤5 lines)

> As the operator, I want the fleet's desired state declared once as versioned data and
> mechanically reconciled, so that "done" stops being anyone's word and becomes a report I can
> read in two minutes. — `BACKLOG.md:455`

> The trust consequence (the point of all of it): the operator stops verifying anything by hand.
> "Done" stops being anyone's word and becomes a mechanical report. The current distrust is the
> *correct* response to the mechanism not existing yet. — intake #16 §2, `:80`

### 1.3 Which is authoritative, and why — governance precedence, not preference

**There is no single North Star statement. There are two, at two scopes, and one is nearer.**

- **B (intake #16) is the authoritative FLEET end-state.** `BACKLOG.md`'s `[E9]` preamble names it
  as `Source.` by filename; `[E9]` exists because #16 exists. A is B's one-line rendering, not an
  independent authority.
- **C (intake #28 §B v1.0) is the authoritative HUB finish line** — a nearer, narrower gate that
  says when `.dev-knowledge` itself is done, at which point *"the default window class flips from
  hub-process to product (satellite backlogs)"*. It does not restate B and does not supersede it.
- **D (ADR-109) outranks both as binding law** for what it covers. ADR-98 makes the intake the
  requirements spine and the ADR the ratified decision; #16 §1–§3 + §5 were consumed *into* ADR-109
  and #16 §4 *into* ADR-104 (in-file SUPERSEDED marker at `:56`). Where #16's prose and ADR-109
  disagree about the contract, ADR-109 governs. #16 stays live because §6's plan spine (steps 4–7)
  is unconsumed — the doc's own NOTE at `:11-16` says exactly that.

**One recorded inconsistency, not repaired here.** `BACKLOG.md:457` describes intake #16 as
`(intake **#16**, DRAFT)`. The file's frontmatter reads `status: ACCEPTED`. The BACKLOG prose is
stale against the doc it cites.

---

## 2. The ladder — and the two other things "L2" can mean

The operator's "L1, L2, L3, L4" is ambiguous **by ratified decision, not by accident**. ADR-113
(Accepted 2026-08-19) decision 3 rules that **three unrelated `L` namespaces are live at once**
and a bare `L<n>` does not say which. Both readings that could be meant are answered below.

### 2.1 Reading A — the MATURITY LADDER (this is almost certainly the one meant)

Definition home: intake #16 §1's layer table (`:48-56`), **ratified as fleet vocabulary by ADR-113**
with the operator's half-steps L0.5 / L3.5. ADR-113 decision 2: *"A level is a maturity claim,
never an authority."* It arms no gate and schedules no work.

The last full per-rung reading was `docs/audits/2026-07-31-verification-382-ladder-evidence.md`
(from `main` @ `f7abe228`). ADR-113 explicitly declines to re-measure it. **The column below is a
fresh measurement taken today**; the 07-31 column is quoted so the delta is visible.

| Rung | One-line definition | 2026-07-31 reading | **Measured today (2026-08-21)** | What must be true to reach the next rung |
|---|---|---|---|---|
| **L0** structure as managed state | conformance is readable mechanically, not inferred | PARTIAL — first mechanical read exists; `conform 185 · diverge 3 · declared 3 · n/a 219` | **PARTIAL, unmoved on the thing that matters.** Live run of `scripts/desired_state_report.py`: `conform 190 · diverge 3 · declared 3 · n/a 224`. **+5 conform, +5 n/a, and diverge is still exactly 3 after 21 days.** | The 3 diverge cells close (ai-council 1.3.1 vs declared 1.4.0; corp-ops and corp-sca ruled `full` with nothing deployed). Owner: `[#383]`. |
| **L0.5** recurrence on `main` | the reading actually runs, and on `main` rather than one machine | NO ON MAIN — one undeclared Windows Task Scheduler entry, output trail dead since 2026-07-16 | **PARTIAL, and this is the one rung that genuinely moved.** `.github/workflows/report-only-wall.yml` now exists and is repo-declared. But its triggers are `push: branches: [main]` + `workflow_dispatch` — **there is no `schedule:` key anywhere in the tree**, and the file's own header says *"REPORT-ONLY FOREVER, not a gate awaiting promotion"*. `[#493]` (open) records the scheduled fleet-baseline task *"silent 10+ days"*. | A time-driven trigger exists in the repo, or the push-triggered wall is declared as the recurrence mechanism and the scheduler question in `[#493]` is ruled. |
| **L1** dependency architecture | dependencies are declared and checkable | SATISFIED for `[#382]`'s Done-when; *typed, not queried* | **SATISFIED, and still typed-not-queried.** `ecosystem/schema/` + `scripts/desired_state_loader.py` are live and load 5 resolved members. **`networkx` — named by intake #16 §2 as the dependency-graph library — has zero occurrences in `pyproject.toml`, `uv.lock`, `ecosystem/` and `scripts/`.** There is no graph and no rot query. | A graph query exists over the typed edges. Blocked by ADR-105 (no networkx until a consumer is named). Owner: `[#383]`. |
| **L2** methodology versioning + deployment | the methodology is versioned and reaches consumers | NOT DONE — manifest declares 1.4.0, highest deployed is 1.3.1 | **NOT DONE. Byte-for-byte unchanged in 3 weeks.** `deploy/manifest-v1.4.0.yaml:58` still declares `methodology_version: "1.4.0"`; `ecosystem/deployed-versions.yaml` still reads ai-council `1.3.1`, corp-monorepo `1.2.0` (by design, ADR-102), corp-ops `null`, corp-sca `null`, hub `null`. **`git log` on `deployed-versions.yaml`: last change `3234b4a0`, 2026-07-21 — 31 days ago.** `git tag` shows no `v1.4.0`. The v1.4.0 carrier is still `implemented: false` (`:327`). | One consumer records `1.4.0` in `deployed-versions.yaml` from a real `deploy/tool.py --execute` run. **No open row names the v1.4.0 consumer write-through** — see §6. |
| **L3** full lifecycle | the loop closes end to end, not once | REAL BUT ONE-OFF | **REAL BUT STILL ONE-OFF.** `desired_state_report.py` appears in no `.claude/settings.json` hook block, no pre-commit hook id, no `ALL_CHECKS` member (43 members enumerated live), and no scheduled task. Its `main()` prints to stdout and writes no artifact — `scripts/window_metrics.py` reports drift-report runs as **`NOT COMPUTED — not-instrumented`** for exactly that reason. Archive + real deletion remain decided-but-unbuilt. | The report writes a durable artifact and something invokes it without a human typing it. |
| **L3.5** the reconcile loop | the report runs on a cadence *and* its output is read by someone | NOT DONE | **NOT DONE, and now with NO OWNING ROW.** `[#460]` (the write-only-telemetry filing) and `[#461]` (metric mechanization) are both **closed**; `scripts/window_metrics.py` shipped from `[#461]` and is itself **unwired — no call site outside `tests/`**. Nearest live rows are `[#391]` (fleet_analytics nightly), `[#419]` (routines nobody consumes), `[#493]` (silent scheduler) — none of which names this report. | A row exists that gives `desired_state_report.py` a cadence and an ADR-105 consumer. **That row does not exist today.** |
| **L4** tech-currency | the stack's currency is tracked rather than discovered | THREE ITEMS, ALL NOT STARTED; 4–7 windows | **PARTIAL — one of three items is now real.** The changelog channel exists and fires: `.claude/commands/changelog-review.md` is ARMED in the organ index, `scripts/changelog_sentinel.py` is wired into `SessionStart`, and it reported live this session (*"claude-code 2.1.238 > last reviewed 2.1.204"*). What is still absent is the **distribution** half — a version bump written into the desired-state contract and pushed through the apply channel. `[#385]` (open, P3) still reads *"L4 is ~5% today, one-offs only"*; `[#495]` (deferred) carries the cadence question. | One version-bump proposal is written into the contract, ruled, and distributed, with the version visible in `deployed-versions.yaml`. **Gated on L2 existing** — `[#385]`'s own `depends-on: 383`. |
| **L5** predictive | the corpus is mined to anticipate rather than to report | UNTOUCHED | **L5a exists as code, is not a lane; L5b untouched.** `scripts/fleet_analytics.py` (1,263 LOC) is the `[#384]` reporter and `[#384]` is **closed**; `logs/FLEET-ANALYTICS.md` exists. But `[#391]` (open) still reads *"nothing invokes `scripts/fleet_analytics.py`"*, `pandas` is declared only in the optional `analytics` group, and **PyDriller — the library intake #16 §3 names — is deliberately absent** (`pyproject.toml:45`, D1 deviation). No predictive model exists. | L5a frames run on a cadence with a consumer (`[#391]`), then L5b gates on "L5a frames show enough signal". |

**Ladder verdict in one line:** the fleet is **at L1**, with L0 partial and stalled, L0.5 partially
mechanized, L2/L3.5 not started and L2 not moved in three weeks, L3 real-but-manual, L4 one-third
real, L5 code-without-a-lane.

### 2.2 Reading B — the ADR-28 THREE-LAYER model (L1 architect / L2 methodology / L3 executor)

Definition home: `docs/decisions/ADR-28-three-layer-architecture.md` (Accepted 2026-04-21,
self-declared **Descriptive**). Layer 1 = browser chat (analysis) → Layer 2 = `.dev-knowledge`
(this repo) → Layer 3 = child repos (execution).

| Layer | Meaning | Position today | Evidence |
|---|---|---|---|
| **L1** browser architect | analysis and rulings happen in browser chat, handed to CC by bundle | **LIVE and mechanized.** 12 stamped v4+ handoff bundles validate; the active bundle is `docs/handoffs/2026-08-20-dev-knowledge-architect-2` and its 14 probes bind to live state. | `audit.py health`: `handoff_bundle_structure: 12 stamped v4 bundle(s) valid`; `handoff_probes: 14 probe(s) bind to live state` |
| **L2** methodology hub | this repo governs; validators here, no orchestration of child state | **LIVE.** 53 organs across 8 classes; 43 registered audit checks; 3 git-hook stages armed. | `ecosystem/organ-index.md:28`; `len(audit.ALL_CHECKS) == 43`; `hooks_armed: OK` |
| **L3** child-repo execution | the methodology reaches and runs in child repos | **PARTIAL.** 6 repos audited, 4 green / 2 with findings. But only **2 of 5** fleet members have any deployed methodology version at all, and the newest release has reached **zero**. | `logs/FLEET-HEALTH.md` (run_date 2026-08-21); `ecosystem/deployed-versions.yaml` |

**The important thing about reading B:** ADR-28's decision text still says *"`.dev-knowledge`
contains no executable orchestration — scripts do not reside here."* That is descriptively false —
this repo carries **86,127 LOC of tracked Python**. `CLAUDE.md` §5 rule 4 and §3 were re-scoped for
exactly this on 2026-08-16 (L10 v2.61/v2.62) and `VISION.md` on 2026-08-18 (`[#558]`); ADR-28 itself
was not, and is immutable. Flagged, not repaired.

### 2.3 Reading C — the DISTRIBUTION layer (ARCHITECTURE Ch2)

The third live namespace ADR-113 names. Here `L0` means *the global `~/.claude` user layer*, as
opposed to `hub` / `plugin` / `pre-commit` (`ARCHITECTURE.md:274`). It is a **placement** fact, not
a maturity claim. When someone writes a bare "L0" near an organ table, this is what it means. ADR-113
records that **nothing checks this convention** — no validator distinguishes a maturity claim from a
placement fact in prose.

---

## 3. Artifact inventory — what the fleet has produced, and where it lives

### 3.1 Headline

| Class | Count | Home |
|---|---|---|
| ADR files | **88** — 86 in `docs/decisions/`, 2 in `docs/decisions/archive/` | `docs/decisions/` |
| Intake docs | **41** — 34 live, 7 archived (**39 distinct ids**) | `docs/intake/` |
| Backlog rows LIVE | **214** — 190 `open` + 24 `deferred` | `BACKLOG.md` (generated) / `tasks/` (source) |
| Backlog rows EVER | **526 distinct ids** across 763 commits touching `BACKLOG.md` | git history |
| `tasks/` files | **299** — open 190 · deferred 24 · closed 81 · retired 3 · superseded 1 | `tasks/` |
| Audits | **640** (+ generated index) | `docs/audits/` |
| Handoff bundles | 695 files across the bundle tree | `docs/handoffs/` |
| Python modules | **263 tracked `.py`**, 86,127 LOC | `scripts/`, `tests/`, `deploy/`, `ecosystem/`, `plugins/` |
| Markdown | **1,951 files, 347,058 lines** | repo-wide |
| Organs | **53 across 8 classes** — 53 ARMED, 3 DECLARED, 2 RETIRED | `ecosystem/organ-index.md` |

### 3.2 ADRs

86 files in `docs/decisions/` covering **84 distinct numbers** (ADR-27 … ADR-113; ADR-44 absent;
ADR-51 and ADR-70 each have a second *amendment* file) plus 2 archived (ADR-40 Deprecated, ADR-52
Superseded). Status mix as the dashboard reads it: **Accepted 81 · Partially superseded 2 ·
Deprecated 1 · Superseded 1 · Explored-not-adopted 1 · off-enum 1 · unparsed 1**.

Three measured header defects, all already on record in `ecosystem/conformance.md` §3 and none
repaired here: **ADR-41** carries `open | in-progress | blocked | done` as its Status (OFF-ENUM);
**ADR-61** has no parsable status line at all; **ADR-43** uses underscores in its filename and is
invisible to the shared parser's grammar.

**ADRs 1–26 do not exist in this repo** — numbering begins at ADR-27 (2026-04-21). No file, index
row or README line accounts for the missing range. **UNDETERMINED**; what would settle it is a
statement in `docs/decisions/README.md` or a ruling, neither of which exists.

### 3.3 Backlog

Live: **214 rows** — P1 **9** · P2 **109** · P3 **96**; size S **125** · M **82** · L **7**;
9 themes, 26 stories. Per-theme (from `ecosystem/conformance.md` §1, HEAD `d436d64f`): E2 62 open,
E7 48, E8 17, E6 15, E5 12, E1 11, E3 6, E4 6, **E9 5**.

**The flow, measured today with `scripts/window_metrics.py`:**

| Window | Rows at open | Rows at close | Filed | Closed | Net |
|---|---:|---:|---:|---:|---:|
| 7 days (`8ec77f3e`..HEAD) | 194 | **214** | 35 | 15 | **+20** |
| 30 days (`09c50cc0`..HEAD) | 138 | **214** | 107 | 31 | **+76** |

Filing outruns closing **2.3 : 1** over the last week and **3.5 : 1** over the last month.

### 3.4 Audits — and the un-consumed ones

640 audit files. Class mix is dominated by `technical` (277) and `codex` (139); then `conformance`
23, `verification` 22, `ecosystem` 18, `corp` 15, `census` 13, `ai` 12.

Inbound-reference census (every tracked `.md`/`.py`/`.yaml`/`.json` file scanned for each audit's
basename; the generated `docs/audits/README.md` index and the file itself excluded):

| Consumption class | Count | Meaning |
|---|---:|---|
| consumed into a row | **96** | referenced from `BACKLOG.md` or a `tasks/*.md` — the only class that provably became work |
| journal-only | 237 | named in `JOURNAL.md`, never in a row |
| audit-to-audit only | **244** | cited only by other audits — the corpus talking to itself |
| other-doc only | 31 | referenced from a protocol / ADR / ecosystem file |
| handoff-only | 24 | referenced only from a handoff bundle |
| **zero inbound** | **8** | referenced by nothing anywhere |

**Never referenced outside `docs/audits/` at all: 252 of 640 (39%)** — by month, 2026-05: 22 ·
2026-06: 32 · 2026-07: 55 · **2026-08: 143**.

**The 8 with no inbound reference anywhere** (all 2026-08-19/20, all lane contracts or cloud briefs
— i.e. dispatch artifacts that outlived their dispatch):

```
2026-08-19-technical-171-dashboard-lane-contract.md
2026-08-19-technical-486-cp1252-lane-contract.md
2026-08-19-technical-cloud-c1-brief.md
2026-08-19-technical-cloud-c2-brief.md
2026-08-19-technical-cloud-c3-brief.md
2026-08-19-technical-cloud-c4-brief.md
2026-08-19-technical-cloud-c6-brief.md
2026-08-20-technical-parallel-flip-lane-contract.md
```

`[#443]` (open) is the row that owns this class — *"Planning artifacts outside the three enforced
classes carry no rent rule"*, citing North Star §5 lesson 7 (*meta serves object*).

### 3.5 Generated ecosystem outputs (the "dashboards")

| Artifact | Generator | State today |
|---|---|---|
| `ecosystem/conformance.md` + `.html` | `gen_dashboard.py` | **STALE** — `--check` reports drift on both; HEAD stamp `d436d64f`, **27 commits behind** `main` |
| `ecosystem/organ-index.md` | `generate_organ_index.py` | fresh (hook-gated) |
| `ecosystem/doc-counts.md` | `gen_doc_counts.py` | fresh |
| `ecosystem/index.yaml` | `audit.py regenerate_index` | observed rollup dated **2026-08-05T10:36:01**, rendered as-is, never regenerated by the report (C8) |
| `logs/FLEET-HEALTH.md` | `fleet_health.py` | fresh — `run_date: 2026-08-21`, 4/6 green |
| `logs/PROPOSALS-YYYY-MM-DD.md` | `propose_closures.py` | **83 daily files**, 2026-06-02 → 2026-08-20, unbroken |
| `logs/TELEMETRY.db` | `telemetry_emit.py` | **ABSENT** — verified on disk today |

---

## 4. The Python program — what the codebase IS today

### 4.1 Size and module map

**263 tracked `.py` files, 86,127 LOC.**

| Area | Files | LOC |
|---|---:|---:|
| `tests/` | 140 | 43,755 |
| `scripts/` (top level) | 67 | 30,411 |
| `deploy/` | 18 | 7,460 |
| `scripts/audit_checks/` | 18 | 1,593 |
| `plugins/` | 5 | 1,185 |
| `ecosystem/` (schema) | 2 | 659 |
| `scripts/codemap/` | 7 | 535 |
| `scripts/toc/` | 4 | 279 |
| `scripts/hooks/` | 1 | 192 |
| `.claude/` | 1 | 58 |

`scripts/` top level splits by name into **11 generators** (`gen_*`/`generate_*`), **13 validators**
(`validate_*`), **3 checkers** (`check_*`), **3 refusal gates** (`block_*`) and 37 other modules.
The ten largest: `audit.py` 4,524 · `fleet_parity.py` 2,049 · `fleet_analytics.py` 1,263 ·
`gen_dashboard.py` 1,239 · `gen_task_tree.py` 1,215 · `enforcement_coverage.py` 1,180 ·
`fleet_health.py` 1,017 · `gen_handoff.py` 878 · `generate_organ_index.py` 845 ·
`verify_handoff_probes.py` 697.

### 4.2 The curated baseline (`pyproject.toml`)

Not a package (`[tool.uv] package = false`); Python `>=3.12`; **uv pinned exactly** at
`==0.11.19` per ADR-106 because uv is pre-1.0 and drifts in point releases.

`dev` group: `pytest>=9.0` · `pytest-xdist>=3.8` · `ruff==0.15.5` (exact-match with the pinned
pre-commit rev) · `pre-commit>=4.5` · `pyyaml>=6.0` · `click>=8.0` · `rich>=13.0` ·
`pydantic>=2.0,<3` · `packaging>=24.0` · `markdown-it-py>=4.0`.
`analytics` group (hub-only, optional): `pandas>=2.0`.

**Two libraries the North Star named are absent.** `networkx` (intake #16 §2, the dependency-graph
row) has **zero occurrences** anywhere in the tree. `PyDriller` (intake #16 §3, the L5a mining row)
is **deliberately** absent with a recorded rationale at `pyproject.toml:45` and
`scripts/fleet_analytics.py:35-39` — `git log --numstat` is used instead. The pandas half of the
§2 mapping did land; the networkx half did not.

### 4.3 Tests

**3,143 tests collected** across 140 files (`pytest --collect-only -q -n 0`, 4.61 s).

Runtime — measured on this workstation and recorded in-repo, most recent first:

| Date | Result | Wall clock | Source |
|---|---|---|---|
| 2026-08-19 | 8 failed, 3008 passed | **273.80 s (4:33)** — **Codespaces container**, `-m "not slow"` | `docs/audits/2026-08-19-technical-554-proof.md:208` |
| 2026-08-18 | 5 failed, 3023 passed | **1651.51 s (27:31)**, `pytest -n auto` | `docs/audits/2026-08-18-technical-batch1-integrator-packet.md:81` |
| 2026-08-17 | 2 failed, 2968 passed | **948.45 s (15:48)** | `docs/audits/2026-08-17-technical-batch-7a-packet.md:125` |

So: **~16–27 minutes on the Windows workstation, ~4.5 minutes in a 4-core Codespaces container.**
The suite was **not run today** — 44 live `python` processes were observed at session start,
and running a second full suite under contention produces a false RED. **UNDETERMINED for today's
pass/fail**; what would settle it is one uncontended `pytest -n auto` run.

The **two standing REDs** are named and owned by `[#569]` (open, P2/M):
`test_routine_consumers_live_backlog_governs_exactly_one_row` (a stale pin — expects 1 declared
routine row while the audit reports 3 **and passes**) and
`test_anchor_gate_probe_distinguishes_installed_from_absent` (does not discriminate).

### 4.4 Which modules carry the governance organs

| Organ | Module | Wired where | Live evidence today |
|---|---|---|---|
| the audit engine | `scripts/audit.py` (4,524 LOC) + `scripts/audit_checks/` (18 modules) | `audit-health` pre-commit hook | **`len(ALL_CHECKS) == 43`**; `audit.py health` today = **OK, exit 0**, 44 OK / **46 WARN** / 0 FAIL |
| backlog schema | `scripts/validate_backlog.py` | `validate-backlog` pre-commit | armed |
| backlog engine | `scripts/gen_task_tree.py` | `task_tree_coherence` in ALL_CHECKS | **`tasks/` is the source of truth; `BACKLOG.md` is GENERATED** (ADR-107 STEP 3, flipped by `[#439]` 2026-07-28) |
| the report surface | `scripts/gen_dashboard.py` (1,239 LOC) | **nothing** | **no call site outside `tests/`** — see §4.5 |
| telemetry | `scripts/telemetry_emit.py` + `scripts/single_flight.py` | nothing yet | store `logs/TELEMETRY.db` **absent**; `[#529]`/`[#530]`/`[#565]` open |
| push/commit refusal | `block_ff_push.py`, `block_unanchored_push.py`, `block_commit_on_main.py` | pre-push / pre-commit | `hooks_armed: OK` — all three stages installed |
| shared anchor predicate | `scripts/journal_anchor.py` | shared by the pre-push gate and the audit backstop | `journal_spine_anchor: OK` |

**`audit.py health` today, in full: 44 OK, 46 WARN, 0 FAIL, exit 0.** WARN classes: `doc_rot` 20 ·
`undeclared_edges` 19 · `no_ff_merges` 3 · `review_artifact_coverage` 2 · `reconciled_versions` 1 ·
`journal_spine_anchor` 1 (mention-not-record, 492 SHAs). For comparison, `ecosystem/conformance.md`
§5 records the **2026-08-18** standing total as **32 across 8 classes**; `doc_rot` alone has gone
**6 → 20** in three days.

### 4.5 Built but unwired — every module with no call site outside `tests/`

Method: for each of the 67 top-level `scripts/*.py`, count word-boundary references from other
`scripts/`, from config surfaces (`.pre-commit-config.yaml`, `.claude/`, `plugins/`, `deploy/`,
`.github/`), and from `tests/`. A module with zero non-test, non-doc references is unwired.

| Module | LOC | What it is | Note |
|---|---:|---|---|
| **`gen_dashboard.py`** | 1,239 | **the conformance dashboard** — the single surface that renders "done" as a report rather than a word | Writes two committed outputs, so it *is* being run by hand (both files stamped 2026-08-20) — but **nothing invokes it**, and both are STALE today. This is the North Star's own trust mechanism, un-automated. |
| **`window_metrics.py`** | 191 | the six operator window metrics, from `[#461]` | Shipped to replace hand-assembled numbers; nothing calls it. Two of its six metrics self-report `NOT COMPUTED`. |
| **`probe_child_backlogs.py`** | 270 | child-repo backlog probe | last referenced by audits from 2026-06/07 |
| **`seed_runbook.py`** | 122 | seeds a consumer's `docs/handoffs/README.md` from the hub source | This is the mechanism §B clause 4 ("satellite onboarding = one command") needs. `[#293]` (open) is its row: *"0/6 consumers done"*. |

Four modules, **1,822 LOC**, built and dormant. Three of the four are load-bearing for a North Star
clause.

---

## 5. Intake pipeline rollout — the funnel, and where it actually stalls

### 5.1 The funnel, counted

Measured today with the dashboard generator's own join (`gen_dashboard.intake_rows`), so these are
the same numbers the gate itself would print, not a re-derivation.

| Stage | Count | Note |
|---|---:|---|
| Intake docs that ever entered | **41** | 34 live + 7 archived |
| Distinct intake ids | **39** | ids 1–39, none missing; **id #14 is used by three files** (two archived CONSUMED drafts + the live ruled pack) |
| `SEED` | 10 | never worked by a functional-architect conversation |
| `DRAFT` | 7 | all filed 2026-08-05 → 2026-08-17 |
| `READY` | 1 | #15 satellite-onboarding-prompts |
| `ACCEPTED` (live standing authority) | **16** | |
| — of which **carried** by ≥1 live row | **11** | |
| — of which **ACCEPTED-with-no-carrier (orphans)** | **5** | **#18, #26, #28, #30, #31** |
| — of which **parked behind a dead trigger** | **3** | #12, #13, #14 all carry `trigger: "#328 build"` |
| Terminal + archived | **7** | CONSUMED 5 · SUPERSEDED 1 · REJECTED 1 |
| **Reached an ADR** | **6 distinct ids** | #1→ADR-98 · #16→ADR-104, ADR-113 · #17→ADR-107 · #22→ADR-108, ADR-109 · #26→ADR-110 · #28→ADR-112 |

**On "expect 0 archived":** 7 docs are archived. That is **correct behaviour**, not a defect — the
`docs/intake/README.md` §5 enum makes CONSUMED / SUPERSEDED / REJECTED terminal and requires
relocation to `archive/`, while **ACCEPTED is deliberately NOT terminal** ("a standing authority
must stay visible live"). The number that should be 0 is *ACCEPTED docs sitting in `archive/`*, and
that number **is 0**. Both readings answered.

**15% conversion.** 6 of 39 intake ids ever produced an ADR.

### 5.2 Where the pipeline stalls — three distinct stalls, in order of severity

**Stall 1 — the dead trigger. Three ACCEPTED plan-of-record intakes are un-startable by
construction.** Intakes #12 (Fleet Ownership Manifest), #13 (Plan-of-record — Fleet Hygiene) and
#14 (SIEM requirements ruled pack) are all `disposition: deferred` behind `trigger: "#328 build"`.
Verified live today: `grep -c "^- \[#328\]" BACKLOG.md` → **0**; `ls tasks/328-*` → **no such
file**. **`[#328]` has no row and no task file.** Three operator-approved requirements packs are
parked on an un-park condition that cannot fire. `[#549]` (open, P2) states this in the row's own
text and has been open since 2026-08-16.

**Stall 2 — ACCEPTED without a carrier. Five ruled intakes have nowhere to be worked.** #18
(HANDOFF_PROCESS v6), #26 (parallel execution), **#28 (the hub finish line itself)**, #30
(verification organ), #31 (code-style doctrine). The dashboard reports these as VIOLATION of its
own anti-orphan rule and has done so continuously; the count has not moved. The sharpest instance:
**the intake that defines "when is the hub done" has no row that tracks getting there.**

**Stall 3 — and this is the real answer to the operator's question — the stall is NOT in the
intake pipeline at all. It is at closure.** The intake funnel is producing: **16 intake docs carry
a filename date of 2026-08-05 or later** (2+2+2+3+1+1+5 across seven filing days), and **9 of the
16 live `ACCEPTED` docs date from that same 17-day window**. What is not moving is the backlog:

| | 7 days | 30 days |
|---|---:|---:|
| filed | 35 | 107 |
| closed | 15 | 31 |
| **net** | **+20** | **+76** |

Every ratified intake births rows; the rows do not leave. `[#555]` (P1/M, *"Closing campaign batch 1
+ kill-candidates instrument"*) is the row that owns reversing this, and the active handoff's
Purpose line names the choice between it and the telemetry chain as the window's open decision.
**183 closure proposals are queued** by `propose_closures.py` (SessionStart digest, today) and the
funnel gauge reads **186 closures pending**. The proposals exist; the executions do not.

---

## 6. Where we are vs where the North Star says we should be

### 6.1 Against intake #28 §B v1.0 — the hub finish line (the nearer gate)

Re-scored today. The previous scoring is `docs/audits/2026-08-09-technical-n1-position-northstar.md`
§2 (**0 of 8 met, 1 partial**), taken when #28 was still DRAFT; it is now ACCEPTED, so the bar is
**binding** rather than proposed.

| # | Clause | North Star target | Measured today | Gap | Owner |
|---|---|---|---|---|---|
| 1 | W-wave landed | intake #25 births closed | #25 ACCEPTED, births filed (`[#294]`,`[#308]`,`[#541]`,`[#559]`,`[#561]`) — **all still open** | whole wave | `[#559]`, `[#561]` |
| 2 | closure harvest routine, net ≤ 0 × 2 windows | net ≤ 0 twice running | **net +20** over 7 days | wrong sign, not just distance | `[#555]` |
| 3 | open backlog < 100 | < 100 | **214** | **114 rows** | `[#555]`, `[#506]` |
| 4 | satellite onboarding = one command from the template | one command | `seed_runbook.py` exists and is **unwired**; the *template* is intake #25's copier item, unbuilt | a template + a wiring | `[#293]`, `[#294]` |
| 5 | handoff cut < 10 min measured | < 10 min | `[#511]` open; re-scoped to non-mechanized load (machinery measured at ~4.5 s of a ~30 min cut) | ~20 min of authoring | `[#511]` |
| 6 | provider-swap on a real lane | producer lane, non-Claude | **UNDETERMINED.** Reviewer-lane swaps are witnessed (terra, grok, codex, Gemini A/B). The 2026-07-31 pack states *"the builder lane is untested — every line of code this arc shipped was written by Claude"*; no later artifact reverses it. Settled by one lane whose code was produced by a non-Claude model and merged. | a producer lane | `[#492]`, `[#491]` |
| 7 | zero standing suite REDs without a dispositioned owner | 0 unowned | **2 REDs, both named and owned by `[#569]`** | arguably MET-by-owner; the register entry is what would make it unambiguous | `[#569]` |
| 8 | weekly so-what packet | the artifact exists | **UNDETERMINED.** Batch packets exist (`docs/audits/2026-08-18-technical-batch1-integrator-packet.md`); no artifact is named "weekly so-what packet" and no `· routine:` block declares one. Settled by a ruling that names an existing packet as this, or by the artifact. | the artifact or the ruling | **NO OWNER** |
| A1 | *(amendment)* zero mechanically-untestable Done-when on open rows | 0 | **UNMEASURED.** Last count is **95 untestable (72 convertible)**, hand-taken 2026-08-12. **No detector exists** — `grep untestable\|machine.verifiable` over `scripts/` and `tests/` returns nothing. Intake **#37** *tech-machine-verifiable-done-when* is `DRAFT`. | the detector, then the conversion | intake #37, **no row** |
| A2 | *(amendment)* clause 5 stays < 10 min | — | as row 5 | — | `[#511]` |

**Score today: 0 of 8 clauses met outright · 1 met-by-owner (7) · 2 UNDETERMINED (6, 8) · 5 open ·
1 amendment unmeasured.** Twelve days after the 2026-08-09 scoring, the one clause that moved
(#3, open backlog) **moved in the wrong direction: 161 → 214.**

### 6.2 Against intake #16 — the fleet end-state (the far gate)

| Dimension | North Star target (#16) | Measured today | Gap | Owner |
|---|---|---|---|---|
| L0 — structure as data | zero undeclared divergence per surface | `diverge: 3`, unchanged for 21 days | 3 cells | `[#383]` |
| L1 — dependency graph | doc2doc/doc2file edges as a **graph**, rot = a graph query (networkx) | edges typed as rows; **no networkx, no graph, no rot query** | the graph | `[#383]` |
| L2 — versioning + deployment | the version reaches consumers via the apply channel | manifest at 1.4.0, **highest deployed 1.3.1 (2026-07-11)**, no `v1.4.0` tag, carrier `implemented: false` | one real deploy | **NO OWNER for the v1.4.0 consumer write-through** — `[#294]` covers a validator carrier, `[#245]` the add-path, neither this |
| L3.5 — the reconcile loop | nightly reconcile producing the plan-report, read by someone | report is stdout-only, invoked by hand, consumed by nothing | cadence + consumer | **NO OWNER** — `[#460]`/`[#461]` closed; `[#391]`/`[#419]`/`[#493]` are adjacent, none names this report |
| L4 — tech-currency | proposal → contract → ruled → **distributed** | research channel live and firing; distribution half absent | the apply channel | `[#385]` (gated on L2), `[#495]` (deferred) |
| L5 — predictive | nightly L5a frames → rot tickets, then L5b | `fleet_analytics.py` is code, not a lane; no PyDriller; no frames on a cadence | a lane | `[#391]`, `[#392]`, `[#393]` |
| **Trust** — "done" is a report | the operator stops verifying by hand | the report generator **has no caller** and both its outputs are **STALE** (27 commits behind) | automation of `gen_dashboard.py` | **NO OWNER** |
| Sequencing | `[#382]`→`[#383]`→`[#385]` gated | **the gates are prose and do not fire** — `_DEPID_RE` requires `#`, the `[E9]` clauses are bare | a parser fix | `[#424]` (open since 2026-07-26) |
| Backlog volume | *(#28 §B)* < 100 | 214, net +76 over 30 days | 114 | `[#555]` |

**Four NO-OWNER findings.** L2 consumer write-through · L3.5 reconcile cadence · the dashboard's
automation · §B clause 8. Each is a step the North Star names and no live row carries.

---

## 7. ORIENT

*Paste this section alone into a fresh chat to orient an architect in 60 seconds. Every claim
carries its evidence pointer. Measured on `main` @ `78267fdb`, 2026-08-21.*

### (a) What is DONE

- **The decision spine works.** 88 ADRs, 43 armed audit checks, 53 organs across 8 classes, three
  git-hook stages armed, `audit.py health` **OK / exit 0** today (44 OK, 46 WARN, 0 FAIL).
  *Evidence:* `audit.py health`; `ecosystem/organ-index.md:28`.
- **L1 of the maturity ladder is satisfied.** The desired-state schema is committed and loads five
  fleet members; the divergence report runs live and prints `conform 190 · diverge 3 · declared 3`.
  *Evidence:* `scripts/desired_state_report.py` run today; ADR-109.
- **The backlog engine flipped.** `tasks/` is the source of truth, `BACKLOG.md` is generated, and
  the coherence gate is armed. *Evidence:* `tasks/README.md:1`; `task_tree_coherence: OK`.
- **The handoff harness is mechanized.** 12 stamped bundles valid; the active bundle's 14 probes
  bind to live state in one round trip. *Evidence:* `handoff_bundle_structure`, `handoff_probes`.
- **The intake pipeline itself is producing.** 41 docs, 39 ids, 16 ACCEPTED standing authorities,
  6 ids promoted to ADRs. *Evidence:* §5.1.

### (b) What is IN FLIGHT

- **The active seat is architect mode**, bundle `docs/handoffs/2026-08-20-dev-knowledge-architect-2`,
  destination `main` in the primary tree. Its own Purpose line says the window handed forward
  *"eight new rows with no dispatch plan"* and names the open choice: **rule the `doc_rot`
  row-length ceiling → decide `[#539]`'s dispatch → rule what the C1 refusal items measure → choose
  between the closing batch `[#555]` and the telemetry chain `[#565]` → `[#529]`/`[#530]`.**
- **Telemetry v1** — `telemetry_emit.py` + `single_flight.py` exist; `logs/TELEMETRY.db` does not.
  `[#565]` (P1) is sequenced before the read path. *Evidence:* file absent on disk; `[#529]`,`[#530]`.
- **Five lane worktrees are provisioned and in use, with no landed work yet** — all five sit at
  `78267fdb`, zero commits ahead; and at least two of them (`lane-rat-intakes`,
  `lane-arch-adr-audits`) were observed running `scripts/audit.py health` concurrently during this
  session. Provisioned and active, but nothing has reached the spine from them.
  *Evidence:* `git worktree list`; live process table, 2026-08-21 11:44–11:47.
- **Seven DRAFT intakes have never been dispatched a lane.** *Evidence:* §5.1; the handoff Purpose
  line names this as an open question.

### (c) The SINGLE next thing that matters most

**Close rows. Nothing else on the board moves until the flow inverts.**

The measurement, in one line: **filed 107 / closed 31 over 30 days — net +76. The open backlog is
214 against a ratified target of < 100.** *Evidence:* `scripts/window_metrics.py 09c50cc0..HEAD`.

Why this and not something else, stated as arithmetic rather than as preference:

1. It is the **only §B clause whose distance grew** since the last scoring (161 → 214 in 12 days).
   Every other clause is static; this one is actively receding.
2. Clause 1 (W-wave) **can only be satisfied by making clause 3 worse** — closing the wave means
   filing its births first. The order is forced: drain, then fill.
3. The work is already prepared and is not being executed: **183 closure proposals are queued**
   and the funnel gauge reads **186 closures pending / 0 triage**. This is an execution gap, not a
   discovery gap. *Evidence:* SessionStart digest, 2026-08-21; `logs/PROPOSALS-2026-08-20.md`.
4. The owning row exists and is **P1**: `[#555]` *Closing campaign batch 1 + kill-candidates
   instrument*.

**The two things to decide alongside it, because both are un-startable and neither has an owner:**

- **`[#328] does not exist.** Three ACCEPTED plan-of-record intakes (#12, #13, #14) are parked
  behind `trigger: "#328 build"`. Verified: no row, no task file. Either re-anchor the trigger or
  record the supersession. *Evidence:* §5.2 stall 1; `[#549]`.
- **The dashboard has no caller.** `gen_dashboard.py` (1,239 LOC) is the surface that makes "done"
  a report instead of a word — the North Star's stated point — and it is invoked by nothing, with
  both its committed outputs **STALE by 27 commits**. Four modules totalling 1,822 LOC are built
  and unwired; three of them are load-bearing for a §B clause. *Evidence:* §4.5.

---

## Honest limits of this report

- **The suite was not run.** 44 live `python` processes were present at session start; a contended
  run yields a false RED. Test *count* (3,143) is measured; today's pass/fail is UNDETERMINED.
- **Two §B clauses are UNDETERMINED, not scored** — provider-swap on a producer lane (6) and the
  weekly so-what packet (8). Each names what would settle it.
- **The §B amendment criterion is unmeasured because no detector exists.** The 95/72 figures are a
  2026-08-12 hand-count carried forward, labelled as such.
- **The audit-consumption census is reference-based, not semantic.** An audit counted as "consumed
  into a row" is one whose filename appears in `BACKLOG.md` or a `tasks/` file. It does not prove
  the finding was acted on, only that the row points at it.
- **Per-theme backlog splits in §3.3 are quoted from `ecosystem/conformance.md` at `d436d64f`**,
  which is 27 commits stale. Every fleet-wide total in this report was re-measured today.
- **Nothing here is a ruling or a recommendation dressed as a finding.** §7(c) states which number
  is receding and which row already owns it; the decision is the architect's.
