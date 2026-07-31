# [#382] close — L0–L5 ladder evidence pack, answered FROM MAIN with per-level anchors

- **Class:** verification (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** 382-ladder-evidence
- **Subject:** the operator's L0–L5 challenge, answered from `main` at **`f7abe228`** (the [#382]
  closure merge) — every level carries a SHA or `file:line`, or is stated NOT DONE with an
  estimate. Ladder levels are intake #16 §1's layer table (L0 structure-as-state · L1 dependency
  architecture · L2 methodology versioning + deployment · L3 full lifecycle · L4 tech-currency ·
  L5 predictive), with the operator's half-steps L0.5 / L3.5 added.
- **Method:** read-only. Live runs are named where run; absences are cited as absences.

---

## L0 — structure as managed state · PARTIAL, first mechanical read exists

The divergence report is the first surface that answers "what is conformant" mechanically.
**Live run on this repo, `main` `f7abe228`** (`uv run --locked python scripts/desired_state_report.py`):

```
fleet members (deployed-versions anchor): .dev-knowledge, ai-council, corp-monorepo, corp-ops, corp-sca-time-automation
summary — conform: 185 · diverge: 3 · declared: 3 · n/a: 219
```

- The 3 **diverge** cells are real, previously invisible gaps: `ai-council` deployed 1.3.1 vs the
  declared 1.4.0 target (G11 — the gap that had no field anywhere), `corp-ops` and
  `corp-sca-time-automation` ruled `full` with nothing deployed (C3).
- The 3 **declared** cells are sanctioned, rendered as declarations not reds
  (`corp-monorepo` gate-rev-ahead, `scripts/desired_state_report.py:_corpus_cell`).
- **Honest limit:** "conform" = no divergence DECLARED. It is NOT a probe result — probe
  execution stays `scripts/fleet_parity.py`'s, and the observational join awaits the G9
  crosswalk (`desired_state_report.py` module docstring; report's own HONEST LIMITS block).

**What L0 still is not:** intake #16 §1 rated L0 ~25% because folder/file/name state is not
managed. The schema types it; nothing yet *converges* it. Convergence is [#383].

## L0.5 — is the night lane RECURRING on main? · NO ON MAIN; machine-local only

**The mechanism is not in the repository.** Verified absences on `main` `f7abe228`:

- No `.github/workflows/` directory exists (`ls .github/workflows` → absent).
- No committed scheduler definition anywhere: no `*.cron`, no crontab file, no task-definition
  XML tracked in the tree.
- `.claude/settings.json` declares **SessionStart / Stop / PreToolUse hooks only** — event-driven
  per session, never time-driven: `fleet_health.py`, `surface_triage.ps1`,
  `billing_leak_sentinel.ps1`, `changelog_sentinel.py`, `arm_hooks.py`.

**What is recurring is machine-local and undeclared:** a Windows Task Scheduler entry
`fleet-baseline` (State `Ready`, `MSFT_TaskDailyTrigger`, `DaysInterval 1`, StartBoundary
`2026-06-06T09:00`) running
`C:\...\Python312\python.exe "C:\...\.dev-knowledge\scripts\fleet_health.py"`.

Two facts about it, both material:

1. **It runs the SYSTEM interpreter, not `uv run --locked`** — an ADR-106 divergence: the
   scheduled path is outside the locked gate environment the whole fleet moved to.
2. **Its output trail stops 2026-07-16.** Last `ecosystem/*/history/*.md` on
   `origin/automation/fleet-audit` = `2026-07-16.md`. `main` carries `2026-07-31.md` dailies —
   but those were written by the **boot hook** and committed by hand this window (`0ed63e4f`),
   not by the scheduler. `Get-ScheduledTaskInfo` returns "cannot find the file specified", so no
   run history is retrievable.

**Answer:** the night lane is **not recurring as a repo-declared mechanism**; a daily task exists
on one machine, is undeclared in the tree, bypasses the locked environment, and has no verifiable
output since 2026-07-16.

**Consumer question — write-only telemetry, no consumer.** The dailies the lane writes are
consumed by nothing. Writer: `scripts/audit.py:361` (`ECOSYSTEM_DIR / repo_name / "history" /
f"{run_date.isoformat()}.md"`), invoked from `cmd_run` (`audit.py:3219`, `:3368`). A full grep of
`scripts/`, `deploy/`, `plugins/` finds **no code that reads a daily's content**; the only three
near-hits are:
- `scripts/scan_undeclared_edges.py:99` — an **exclusion** (`if rel.startswith("ecosystem/") and
  "/history/" in rel`), i.e. code that deliberately ignores them;
- `scripts/audit.py:3230` — writer-side path enumeration for working-tree restore;
- `scripts/validate_doc_rot.py:239` — an unrelated scan of `_SECTION_HISTORY_DOCS` (doc §12
  section-history, not ecosystem dailies).

In the operator's words: **write-only telemetry, no consumer.** ADR-80 §31(b) sanctioned
committing them as "the durable record" without naming a consumer — precisely the shape ADR-105
later ruled must be declared at ACTIVATION. Filed as **[#460]** (keep / aggregate / stop).

## L1 — dependency architecture · [#382] Done-when SATISFIED, with a real run

**The Done-when, quoted from the row as it stood at close** (`tasks/382-*.md:13`, now
`status: closed`):

> `· Done when: an ADR is accepted AND schema v1 is committed ·`

| Clause | Evidence | SHA |
|---|---|---|
| "an ADR is accepted" | ADR-109 status line flipped Proposed → Accepted (ADR-94 in-place), operator GO | `b7197715`, merged `7ef40567` |
| "schema v1 is committed" | `ecosystem/schema/desired_state.py` + `__init__.py`, 49 tests | `2ee3376d`, merged `d163680a` |
| supporting — loader | `scripts/desired_state_loader.py`, 17 tests incl. live-repo leg | merged `ee176854` |
| supporting — report | `scripts/desired_state_report.py`, 16 tests | merged `0708590f` |
| closure | retire-not-delete, detector-clean | `0acc3328`, merged `f7abe228` |

**One REAL loader run, naming the repo.** `load_fleet_model()` against
`C:\Users\1028120\Documents\Dev\.dev-knowledge` at `f7abe228` produced a validated `FleetModel`:
8-repo union → **5 resolved members** (`.dev-knowledge`, `ai-council`, `corp-monorepo`,
`corp-ops`, `corp-sca-time-automation`, resolved toward `deployed-versions.yaml`);
`corp-monorepo` loaded at `1.2.0` with its `v1.3.1` gate as a typed `gate-rev-ahead`
declaration; the `index.yaml` staleness stamp surfaced rather than repaired. The live-repo test
asserts the run leaves `git status` and all seven source files byte-identical
(`tests/test_desired_state_loader.py::test_live_repo_loads_clean_and_writes_nothing`).

**Honest scope:** L1 is *typed*, not *queried*. Edges are rows; there is no graph and no rot
query. That is [#383], by ADR-105 (no networkx until a consumer is named).

## L2 — methodology versioning + deployment · NOT DONE

**State:** `deploy/manifest-v1.4.0.yaml` declares `methodology_version: "1.4.0"` while the highest
value any repo records in `deployed-versions.yaml` is `1.3.1` (ai-council). The v1.4.0 carrier
that motivated the cut is `implemented: false` — "the hub half is built, the consumer
write-through is the next ticket" (`deploy/manifest-v1.4.0.yaml:18-19`). The divergence report now
makes this gap *visible* (the ai-council `corpus-version: diverge` cell) — visibility is the whole
L2 delta this arc produced.

**Estimate to done: 3–5 windows.** One to build the consumer write-through for the declared
carrier; one to run a gated per-repo deploy for ai-council; one to reconcile
`deployed-versions.yaml` + parity rows; 1–2 contingency for the corp-monorepo asymmetry
(sanctioned at 1.2.0 with a gate at v1.3.1 — any deploy must not "fix" it, per ADR-102).

## L3 — full lifecycle · the report is REAL BUT ONE-OFF

**Real:** the report renders live fleet state (the L0 run above), from committed code, with tests.

**One-off:** it runs only when a human types the invocation —
`uv sync --locked --group analytics` then
`uv run --locked python scripts/desired_state_report.py`
(`scripts/desired_state_report.py` module docstring; `main()` at the bottom of the module).

**No scheduler exists for it, and the absence is verifiable:** it appears in no
`.claude/settings.json` hook block, in no pre-commit hook id, in no `ALL_CHECKS` member, and in no
scheduled task (the only task is `fleet-baseline` → `fleet_health.py`, §L0.5). Nothing consumes
its output automatically; there is no drift-report artifact committed anywhere.

**Wider L3 state:** intake → ADR → build is now demonstrated end-to-end by this very arc
(intake #22 §E → ADR-109 → four waves → closure). Archive and **real deletion** remain decided
but unbuilt (ADR-107 §7.3 step 4 deferred; the genre-lifecycle engine unbuilt).

## L3.5 — the reconcile loop (report runs on a cadence, output read by someone) · NOT DONE

Nothing schedules the report; nothing reads it; no artifact is produced on a cadence.

**Estimate to done: 2–3 windows.** One to give the report a durable output artifact + a declared
consumer under ADR-105 (it currently prints to stdout only); one to wire a cadence — and the
cadence question is *blocked behind* [#460], because putting a second write-only producer on a
timer before the first one's consumer question is answered would repeat the exact defect [#460]
names; 1 contingency.

## L4 — tech-currency · THREE ITEMS, ALL NOT STARTED

| Item | Live status (verified `f7abe228`) | Estimate |
|---|---|---|
| **Library/venv lane** (ADR-106 rollout) | Hub done: `pyproject.toml:25` pins `uv==0.11.19`, `uv.lock` + `.python-version` committed. Fleet NOT done: `ecosystem/parity-surfaces.yaml:234` `root-uv-lock` is `tier: {hub: MUST, consumer: LOCAL}` — consumer stays LOCAL "until each repo's own uv arc flips its row to MUST" (ADR-106 pt 7, per-repo GATED rollout). **The scheduled night task itself bypasses uv** (§L0.5). | **2–3 windows** (one per consumer arc + the scheduler fix) |
| **Gemini activation** (R-G) | **Not started.** Proposed only, in intake #22 §C:48-49 — "activate with the #383/L4 era… per ADR-105 (named consumer + consumption_path required)". Zero implementation: no hits for "gemini" in `scripts/`, `.claude/`, `ecosystem/*.yaml`; **zero rows in BACKLOG.md**. | **1–2 windows**, but ADR-105-blocked until #383 supplies the read-heavy consumer |
| **repomix distiller** (§D) | **Not started.** Named in intake #22 §D:55 as a "booster/pre-phase"; §I explicitly excluded it from the [#446] build ("§D's repomix is NOT injected into the boot build", :107). Zero implementation, **zero rows in BACKLOG.md** — intake #22 §D's own instruction to "verify none has a row (grep), then file as research-consumption rows" is **still undischarged**. | **1–2 windows** (file the rows + one evaluation arc) |

**THE CUTOFF TOTAL: 4–7 windows** to clear all three L4 items — and that is the *floor*, because
Gemini's window cannot start until [#383] names its consumer, so the L4 lane is serialized behind
the L1→graph work, not parallel to it.

## L5 — predictive · UNTOUCHED

Intake #16 §1 rates L5 at 0% and designs L5a (PyDriller mining → hotspot / change-coupling
frames) before L5b (risk scoring). Live state: `scripts/fleet_analytics.py` exists and is the
[#384] L5a reporter, but its own header records the D1 deviation — **PyDriller is deliberately
absent** (`pyproject.toml:42-43`: "PyDriller is deliberately absent — see the D1 deviation note").
No frames are produced on a cadence, no consumer reads them, no predictive model exists. This arc
touched L5 in exactly one way: it did not preclude it (ADR-109 §7 kept the observed-state frames
loadable).

---

## §C specifics — grok's two catches, and what each would have cost shipped

Both were found by the grok shadow lane on the W2 schema diff and **missed by terra**, which
reviewed the same diff against the spec. Full artifact:
`docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md`.

1. **`RefKind` was missing the live `audit` provenance kind.** The schema's provenance-reference
   enum enumerated `git-tag / git-commit / backlog / adr / census / file / ruling / document /
   operator-ruling` — but `ecosystem/parity-surfaces.yaml` carries `{kind: audit, ...}` in a live
   ownership provenance block. **Cost if shipped:** the W3 loader would have raised a pydantic
   `ValidationError` on the real parity file the first time it ran against the live fleet — i.e.
   the loader wave would have opened with a fabricated-looking failure in a component that had
   just passed 49 green tests, and the natural first hypothesis (a loader bug) would have been
   wrong. *(grok's stated count "81/81 surfaces" was disk-refuted — the token occurs once — but
   the defect was real either way; the correction is recorded in the artifact.)*
2. **Four `Surface` fields were scalars where the disk holds dicts.** `join`
   (`{manifest_component: ruff-gate}`), `pending_migration` (`{to: ruff-check, ticket: "#334"}`),
   `local_names` (`{repo → name}`) and `declared_divergence` (`{repo → text}`) were typed
   `StrictStr`. **Cost if shipped:** every real parity row carrying one of these would have been
   **refused at load**, and the only way to make it pass would have been to stringify the dicts —
   an out-of-band encoding that directly violates ADR-109 finding 4 (preserve-raw). The schema
   would have forced the loader to lie about the source shape.

The pattern worth carrying: **terra reviewed the diff against the spec; grok read the diff against
the disk.** Both Criticals came from the second posture. Cost leg remains inconclusive — neither
CLI exposes token pricing; wall-clock was comparable (~5 min each).

## §H specifics — the three builder-debt items, verbatim

From `docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md` §H, reproduced verbatim:

> 1. The builder-role probe itself (§H's own proposal) — unrun; natural slot: a later [E9] wave.
> 2. The grok lane ran ad-hoc (hand-built prompt, no wrapper) — a `grok-review` wrapper
>    symmetric to `codex-review.ps1` would make the shadow repeatable + comparable.
> 3. The review wrapper + skills layer (`codex-review.ps1`, Skill plumbing) is
>    harness-specific; portable in shape, unported in fact.

**Portability verdict on record:** derivation and review lanes witnessed multi-provider (sol
derived, terra + grok each landed accepted Criticals, CC built, operator gated); the **builder**
lane is untested — every line of code this arc shipped was written by Claude.

---

## Metrics — the six operator metrics, baseline vs current

| # | Metric | Baseline | Current (this window) | Anchor |
|---|---|---|---|---|
| 1 | Boot round-trips | **10** (v5 multi-paste boot) | **1** — this window's own boot ran the v6 one-round-trip form: one CC-side command emits ONE evidence block, operator pastes once | `protocols/HANDOFF_PROCESS.md` v6.0.1; CLAUDE.md §12 v2.48 |
| 2 | Net backlog delta | 181 rows at window open | **184 rows — net +3** (filed [#457], [#458], [#459], [#460] = +4; closed [#382] = −1) | `validate_backlog: OK (… 184 tasks)` at `f7abe228`+ |
| 3 | First-arc execution | [E9] had 0 build arcs; [#382] open since the North Star (2026-07-21) | **1 arc executed end-to-end**: 4 waves, 4 merges, ADR accepted, row closed, in ONE window | `7ef40567` → `d163680a` → `ee176854` → `0708590f` → `f7abe228` |
| 4 | Windows to cutoff | not previously counted | **4–7** (L4 total, §L4) — plus L2 3–5 and L3.5 2–3 if the ladder is counted whole | §L2, §L3.5, §L4 |
| 5 | Drift-report runs | **0** (no such report existed) | **1 real run** on live fleet state, human-invoked; **0 scheduled** | §L0, §L3 |
| 6 | Paste / boot bytes vs budget | — | boot **16,842 / 18,000 bytes** (94%, `audit.py health` `boot_byte_budget`); paste warn budget **65,000 bytes** (`scripts/assemble_paste.py:32`), no PASTE_THIS generated this window | live `audit.py health` at `f7abe228` |

**Correction to the brief, stated rather than absorbed:** the brief said net backlog delta **+6
this window**; the verified count is **+3** (4 filed, 1 closed, 181 → 184). If the intended count
was "new rows filed", that number is **+4**. Neither reading yields 6.

**Mechanization of these six is not built** — every figure above was assembled by hand from live
state for this pack. Filed as **[#461]**.
