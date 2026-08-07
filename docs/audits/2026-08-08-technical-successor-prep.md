# Successor prep pack — the 36-item ledger re-colored, the wave-2 pre-check, the batch-3 pool, the carried decisions

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** successor-prep
- **Source-session:** unattended night window, Claude Code on the web (cloud container); branch
  `claude/night-cloud-contract-exec-g4bk91`; base `81d572d7` (`main` at clone time)
- **Status:** RETRIEVAL + LIVE RE-DERIVATION ONLY — **zero rows born, zero rows closed, zero
  builds.** Every §C priority class and every proposal in the parent intake stays exactly where
  the operator left it.
- **Model:** one Opus-class seat, no fan-out.
- **Consumer:** the successor architect seat (the 2026-08-08 morning integration).
- **Consumption path:** §1 before planning batch 3 · §2 before dispatching a lane that carries
  `[#393]` · §3 as the candidate pool the successor **cuts from** · §4 for the gap-week queue ·
  §5 as the decision list only the operator can take · §6 for what this container could not see.

---

## 0. How to read this, and the one rule it follows

The parent ledger is `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` (intake #27),
whose §A carries 36 rows with a status vocabulary and an evidence locator each. This document
**re-colors those 36 rows against live repo state** after the 2026-08-06/07 window, and adds
three sheets the successor needs before it can plan.

**The rule: facts with locators, and nothing else.** A status here is either read from live state
(a `tasks/*.md` frontmatter field, a validator's stdout, a resolved SHA) or it is marked
`UNVERIFIED` with the reason. Where the parent intake recommends something, that recommendation is
quoted as the parent's, never restated as this document's finding. Nothing below proposes a
sequence; §3 is a **pool**, not a plan, and the successor cuts it.

**Δ vocabulary.** `=` no change · `→` status moved · `PEG-SPENT` the row did not move but the
event its status pointed at has now happened, so the locator no longer routes anywhere ·
`PREMISE-MOVED` the row did not move but a number or blocker it was scoped against did.

---

## 1. §A ledger, re-colored POST-window (all 36 rows)

Read `Status @ #27` as of the intake's authoring (2026-08-06); `Today` as of this branch's base
`81d572d7`.

### 1.1 The board

| # | Item | Status @ #27 (2026-08-06) | Today (2026-08-08) | Δ | Evidence (live locator) |
|---|---|---|---|---|---|
| 1 | Gemini CLI lane `[#491]` | SCHEDULED(batch-2 grooming) | OPEN, **unpegged** | PEG-SPENT | `tasks/491-*.md` `status: open`; batch 2 ran at width 3 and closed (`8bef876`), and `[#491]` is in none of the six manifest lanes — `docs/audits/2026-08-07-technical-batch-2-manifest.md` |
| 2 | Grok lane `[#492]` | SCHEDULED(peg ≥2026-08-07; seeded-defect list unwritten) | DEFERRED, **peg date reached**, list still unwritten | PEG-SPENT | `tasks/492-*.md` `status: deferred`, clause `DEFER — peg: ≥ 2026-08-07`; grep for a seed-defect list under `docs/` returns only handoff prose, no artifact |
| 3 | Copilot Free as Grok channel | DEFERRED(opens with #2) | = | = | gated on row 2, which did not open |
| 4 | sol/terra/luna routing table | ADOPTED-live; **terra owed on `[#504]`** | ADOPTED-live; **the `[#504]` debt is discharged** | → | `[#504]` closed at `1447d06`; the artifact exists — `docs/audits/2026-08-06-codex-lane-c-504-failclosed.md`. **Caveat, live:** `audit.py health` still WARNs `review_artifact_coverage: 5af0b33c -> 2026-08-06-codex-lane-c-504-failclosed.md` — the artifact carries no parseable `**Tally:**` line |
| 5 | Actions report-only recorder `[#501]` | SCHEDULED(batch 1) | **CLOSED / ADOPTED-live** | → | `tasks/501-*.md` `status: closed`; closed at `93b2fa3` on push-run evidence; recorder fired on three consecutive pushes (`2f2edd2b`, `4ad76bc5`, `945598f9`), run `31169364373` — JOURNAL 2026-08-07 (b) and (d) |
| 6 | Scheduled runs + dead-man `[#493]` | DEFERRED(no date) — B-2 still silent | = OPEN, still no date, **still silent** | = | `tasks/493-*.md` `status: open`; nothing in the window's 72 commits touches `scripts/fleet-baseline.task.xml` or `setup-fleet-scheduler.ps1` |
| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | = | = | no row, no locator movement |
| 8 | mutmut `[#502]` | EVAL-RUN(pass) + SCHEDULED behind `[#501]` | **UNBLOCKED**, three blockers cleared, **still zero mutant numbers** | → | `[#501]` closed (row 5) lifts the host block. Blocker chain in full, JOURNAL 2026-08-07 (c)+(d): (1) `-p no:xdist` unloading the plugin that supplies `-n`; (2) `.dev-knowledge` literal vs a dotless CI checkout; (3) repo markers absent inside mutmut's `mutants/` sandbox. Fixes `e024a8c8`, `8bb06e0`. `tasks/502-*.md` stays `open` — the pilot last reported all 84 mutants `not checked` |
| 9 | CONTRIBUTING currency `[#503]` | SCHEDULED(batch 1, ×6 claims + DoD + override.md) | **CLOSED** | → | `tasks/503-*.md` `status: closed`; closed at `1447d06` "on verified evidence" |
| 10 | vale (P6) | REFUTED | = | = | `5125dd6` + JOURNAL (b) `616f4814` — both SHAs resolve in this clone |
| 11 | commitlint / gitlint (P6) | EVAL-RUN(LEAVE) | = | = | `81cf13b` resolves; §B carries it as do-not-relitigate |
| 12 | lychee (P6) | EVAL-RUN(ADOPT-candidate, `--include-fragments`) | = **unadopted** | = | `grep lychee .pre-commit-config.yaml` → no match. Stays P-B |
| 13 | copier living-template (W-1) | DEFERRED(batch 2 W-wave) | DEFERRED, **no W-wave ever ran** | PEG-SPENT | batch 2's six lanes were `[#490]+[#430]`, `[#429]`, `[#320]`, `[#283]`, `[#416]`, `[#393]` — zero W-items (`docs/audits/2026-08-07-technical-batch-2-manifest.md`) |
| 14 | kernel/lab check tiering (W-2) | DEFERRED(batch 2; pyproject collision) | same as 13 | PEG-SPENT | ditto |
| 15 | pre-commit native distribution (W-3) | DEFERRED(batch 2; reconcile `[#497]` @ `carrier_mesh.py:75` FIRST) | same as 13; **`[#497]` still open**, so the stated precondition is intact | PEG-SPENT | `tasks/497-*.md` `status: open` |
| 16 | reusable kernel.yml (W-4) | DEFERRED(batch 2; `.github/workflows/` single-owner = `[#501]`) | same as 13; **the single-owner is now a real file**, and a second row already targets it | PEG-SPENT | `[#501]` closed → `.github/workflows/report-only-wall.yml` exists; `[#507]` (born `80d4eb6`) declares `footprint: .github/workflows/report-only-wall.yml, ARCHITECTURE.md Ch6, tests/test_report_only_wall.py` — W-4 now collides with a live row, not a pending one |
| 17 | pytest-testmon (W-5) | SCHEDULED(batch-2 ledger per rider R-ii; **targets 410s/run**) | SCHEDULED; **the 410s premise moved** | PREMISE-MOVED | the suite is parallel-by-default since 2026-08-06: `pyproject.toml` `[tool.pytest.ini_options]` records serial `1785.61s` vs `-n auto` `358.77s` / `330.15s` (~5.2×, identical counts across all three runs). Whatever W-5 buys, it is no longer measured against 410s |
| 18 | schema-as-code (W-6) | DEFERRED(floats behind W-5) — reshaped by §A item 35 | = | = | unmoved; still floats behind a row whose own premise moved (row 17) |
| 19 | sphinx-needs study (W-7) | UNPLACED | = | = | P-D, no trigger fired |
| 20 | local-vs-reference matrix (W-8) | UNPLACED(intake prose) | = | = | — |
| 21 | AGENTS.md + thin shim (W-9a) | DEFERRED(batch 2) + HAZARD: collides with `codex/AGENTS.md` | same as 13; **hazard confirmed live** | PEG-SPENT | `ls codex/` → `AGENTS.md` present |
| 22 | VISION→README (W-9b) | UNPLACED (S, gap-week) | = | = | P-B |
| 23 | `.claude/skills` ↔ `.agents/skills` symlink (W-9d) | UNPLACED (S, gap-week) | = | = | P-B |
| 24 | routing-table-as-config (W-10) | DEFERRED(batch 2) | same as 13; **the prose surface it would replace grew twice this window** | PEG-SPENT | Ch8 routing matrix landed as prose at `e03df5c4`; amended again on this branch (Phase 1 of this window). W-10's subject is larger than when it was deferred |
| 25 | standing-rulings register (V-2) | ADOPTED-live (4 lessons + B2 label land in successor Phase 2) | ADOPTED-live and **materially extended** | → | `protocols/STANDING_RULINGS.md` now carries sections A–F: B5 (`automation/` prefix), B6 (anchor discharges by APPEND ONLY), B7 (VISIBLE = DISPATCHED), and a whole new **section F** with F1–F6 (`6ae62c6` for F1–F5; F6 from the PRE-2 gate-hygiene arc) |
| 26 | risk-tiered ceremony + plan-mode-by-exception (V-3) | ADOPTED-live (`prompt-template` v1.6) | ADOPTED-live at **v1.11** | → | `templates/prompt-template.md` section history: v1.7 scope-split, v1.8 anchor-text, v1.9 dispatch row, v1.10 routing matrix, v1.11 (this window's Phase 1) |
| 27 | first V-1 worktree batch | GO-GIVEN, runs as successor Phase 4 | **batch 1 AND batch 2 have both run and closed** | → | batch-1 packet `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`; batch-2 packet `docs/audits/2026-08-07-technical-batch-2-packet.md`, closed at width 3, merge `8bef876` |
| 28 | worktree hygiene prune (V-5) `[#429]` | SCHEDULED(mechanized, successor Phase 3) | **CLOSED** | → | `tasks/429-*.md` `status: closed`; closed at `a96040c`; lane merge `e685a30` |
| 29 | seal velocity metrics (V-6) | PARTIAL(qualitative only; hard numbers = batch-1 packet) | **still PARTIAL** — the packet landed and carries **merge SHAs, not durations** | = | `docs/audits/2026-08-06-technical-batch-1-integration-packet.md` §1 is a per-lane merge-SHA table; a grep for velocity/elapsed/wall-clock in it returns nothing. The one hard number the window produced is a *different* metric: `[#511]`'s ~4.5s mechanized cut cost vs a 30-min wall clock |
| 30 | `[#408]` three-layer sync spec | DESIGN-LANDED (`c55c7e51`); build = OWN ARC, unplaced | = OPEN, build still unplaced | = | `tasks/408-*.md` `status: open`, `serialize-group: audit-py` |
| 31 | Fibonacci estimate binding `[#488]` | UNPLACED (backlog has no ranking function) | = OPEN | = | `tasks/488-*.md` `status: open` |
| 32 | R1–R4 retirement ranking | DORMANT since `[#487]` engine refutation | = ; `[#487]` still open | = | `tasks/487-*.md` `status: open` `[P2][L]` |
| 33 | **pytest-xdist** (`-n auto`) | NEW EVAL candidate | **ADOPTED-live** | → | `pyproject.toml` `[tool.pytest.ini_options]` — parallel by default, adopted on measurement 2026-08-06 (numbers in row 17). Carries a recorded interaction: `[tool.mutmut] pytest_add_cli_args = ["-n", "0"]`, and the comment states why `-n 0` and **not** `-p no:xdist` |
| 34 | **jsonc-parser** as merge engine | NEW EVAL candidate | = | = | no repo trace (`grep` over `tasks/`, `pyproject.toml`, `.pre-commit-config.yaml` → null) |
| 35 | **check-jsonschema** (pre-commit hook) | NEW EVAL candidate | = | = | no repo trace, same grep |
| 36 | **mise** (per-repo toolchain pinning) | NEW EVAL candidate | = , and **the uv-pin class bit again tonight** | PREMISE-MOVED | `pyproject.toml` pins `required-version = "==0.11.19"`; this container ships uv `0.8.17` and `uv self update 0.11.19` returns *"version 0.11.19 was not found for the app uv"*. Every pre-commit hook whose entry is `uv run --locked …` is therefore unrunnable here. That is a **second** independent instance of the class STANDING_RULINGS D1 names ("the exact `uv` pin is load-bearing for the entire organ mesh"), on a surface `mise` targets |

### 1.2 The three things this re-color found that are not per-row

**(i) Six rows share one spent peg.** Rows 13, 14, 15, 16, 21, 24 all read `DEFERRED(batch 2 …)`.
Batch 2 ran and closed with **zero** W-items in it. Those six statuses are now locators pointing at
a finished event. This is a bookkeeping fact, not a proposal — the parent intake's §C already
classes all six as P-A, and where the next peg goes is the operator's.

**(ii) Two rows had their measured premise move under them, in opposite directions.** Row 17
(pytest-testmon) was scoped against a 410s suite that is now ~330–360s. Row 36 (mise) was scoped
against a *hypothetical* recurrence of the uv-pin class, and the recurrence happened tonight, in
this container, on the exact surface it names.

**(iii) The window's closes are concentrated.** Of the 36, four moved to a terminal state
(`[#501]` row 5, `[#503]` row 9, `[#429]` row 28, and row 33 pytest-xdist adopted), and one debt
discharged (row 4). Everything else either held or lost its peg. Live task-status census at
`81d572d7`: **169 open · 33 deferred · 44 closed · 1 superseded · 1 retired = 248** task files;
`validate_backlog` reports `202 tasks` (open + deferred), `gen_task_tree.py --check` exits 0.

---

## 2. Wave-2 pre-check — the `serialize-group: audit-py` pair, re-derived live

**Why this section exists.** Two documents left an instruction, and the second is stricter than
the first:

> "**Serialize-group note, recorded so it is not discovered at merge time.** `[#430]` (lane-1) and
> `[#393]` (lane-6) both declare `serialize-group: audit-py`. They are in **different waves**,
> which serialises them by construction. If wave 2 is ever pulled forward, this pair is the first
> thing to re-check."
> — `docs/audits/2026-08-07-technical-batch-2-manifest.md`

> "Wave 2 was not pulled forward, so the pair never met — but `[#430]` is now partly landed, so
> **that pair must be re-checked before lane-6 runs**, exactly as the manifest instructed."
> — `docs/audits/2026-08-07-technical-batch-2-packet.md` §9

### 2.1 What was re-derived, and how

| Input | Live value at `81d572d7` | How read |
|---|---|---|
| `[#430]` status | `open` | `tasks/430-consumer-template-rejects-root-conftest-py-fleet.md` frontmatter |
| `[#430]` serialize-group | `audit-py` | same file, frontmatter **and** the body's trailing `· serialize-group:` clause |
| `[#393]` status | `open` | `tasks/393-corp-sca-rot-review-confirm-live-or-retire-3-can.md` |
| `[#393]` serialize-group | `audit-py` | same |
| the group's live membership | **50 ids**, `[#430]` and `[#393]` both present | `python scripts/validate_backlog.py` stdout, the `serialize-groups —` summary line |
| the co-run rule | *"two tasks co-run iff no depends-on path links them and they share no group"* | `scripts/validate_backlog.py` module docstring, lines 34–38 |
| `[#430]`(a) landing | landed; the missing locator now exists | `3cf3a5b0` (the fleet-wide permit) + `protocols/STANDING_RULINGS.md` F5 "First instance, executed here — the `[#430]`(a) root-`conftest.py` ruling" |
| `[#430]`(b) landing | **not landed** | the row's own Done-when clause (b) — *"a ship-gate verdict is reproducible from the subject repo's own state"* — is unmet; `fleet_parity` still reads live sibling state |

### 2.2 Verdict, quoted

> **The pair is still serialized. `[#430]` and `[#393]` may not co-run.**

The derivation is mechanical and has one step: both rows are live in the tree, both carry
`serialize-group: audit-py`, and `validate_backlog`'s own stated rule is that two tasks co-run
**iff** they share no group. They share one. **Nothing about `[#430]` being "partly landed"
changes this** — the constraint keys on the declared group label, not on how much of a row has
shipped, and half a row shipping does not remove its label.

### 2.3 Three facts about that verdict the successor should hold

1. **The group is 50 ids wide.** `audit-py` is not a two-row pairwise constraint; it is the
   largest serialize-group in the repo by a wide margin (next: `settings-json` 18, `architecture`
   15, `handoff` 12 — all four read from the same `validate_backlog` summary line). Cross-checked
   against `tasks/` frontmatter, those 50 are **44 open + 6 deferred** (a further 9 `audit-py` rows
   are closed and so absent from the generated `BACKLOG.md`). The 44 open members are **26.0% of
   the 169 open rows**. Stated as a measurement, not a complaint: the pair-check the manifest asked
   for passes trivially, and the interesting question it exposes — whether a 50-member group is a
   mutual-exclusion declaration or a topic tag — is **not** something this document rules on.
2. **The two rows' real footprints do not obviously overlap.** `[#430]`(b) names
   `scripts/fleet_parity.py`; `[#393]` is corp-sca consumer work whose Done-when is *"each of the
   3 is confirmed-live or retired"* and whose only hub artifact is a disposition report. If the
   successor wants to run them concurrently, the lawful path is a **ruling that changes a label**,
   not a lane that ignores one — F2 ("names, paths and identifiers derive from validators and
   enums") points the same way.
3. **Neither row's blocker from batch 2 has cleared.** `[#393]` was carried because "satellite repo
   lacks the enforcement organs the lane would need"
   (`docs/audits/2026-08-07-technical-batch-2-packet.md` §9). This container cannot see
   `corp-sca-time-automation` at all (§6), so whether that is still true is **UNVERIFIED here** and
   has to be re-witnessed from a machine that can reach the sibling.

---

## 3. Batch-3 candidate sheet — RETRIEVAL ONLY

**What this is and is not.** This is the pool of OPEN rows that could plausibly fill
**feature/consumer** lanes, with each row's footprint and collisions derived live. **It is not a
manifest, not a ranking, and not a recommendation.** The successor cuts it. Sequence, width, wave
split and lane assignment are all outside this document.

**The cap it is sized against, quoted:**

> "**Process-lane cap — from batch 2 onward, at most 1/4 of a batch's lanes target methodology or
> hub-process surfaces.** The remainder carry product/consumer work. A batch that cannot fill its
> non-process lanes **reports the shortfall** in its end-of-batch packet and runs narrower;
> backfilling the gap with additional process lanes defeats the cap…"
> — `protocols/PLAYBOOK.md` Ch8, "The batch protocol"

At width 6 that is **5 feature/consumer + 1 process**. The contract asked for ≥5 fillable lanes;
the sheet below carries 9 candidates, so the successor has something to cut *from* rather than a
list it has to accept whole.

### 3.1 The measurement that shapes every row below

**5 of 169 open rows carry a declared `footprint:` field** (`[#502]`, `[#505]`, `[#506]`,
`[#507]`, `[#508]`). Every other footprint in this sheet is **DERIVED by me** from the row's body
`refs`/prose and marked as such. This is the same defect the batch-2 manifest recorded — *"exclusive
footprints declared **because none of the six rows carries a `footprint:` field** (LB-1 repeating at
scale)"* — measured again here and still true: 164 of 169 open rows have no declared footprint.
**A derived footprint is a claim, not a field.** The successor re-verifies before dispatch.

### 3.2 Feature/consumer candidates (the non-process class)

| id | title | P/size | footprint (D = derived, F = declared field) | collisions |
|---|---|---|---|---|
| `[#393]` | corp-sca rot review — confirm-live-or-retire 3 candidates | P3/S | **D:** `corp-sca-time-automation` working tree only (`config/category_mapping.yaml`, `requirements.txt`, `config/excluded.yaml`) + one hub disposition artifact | **`serialize-group: audit-py`** — §2 verdict binds. Carried from batch-2 wave 2 |
| `[#416]` | ai-council `ARCHITECTURE.md` codemap drift at L23/L109 | P3/S | **D:** `ai-council/ARCHITECTURE.md` only | `serialize-group: architecture` (15 ids). Carried from batch-2 wave 2. Row text: *"routes via a dedicated ai-council session per ADR-41; the hub files it, never writes it"* — the RULING-W consumer-worktree shape is what batch 2 used to square that |
| `[#283]` | corp-monorepo `hybrid_classifier.json` 1.08MB duplication | P3/S | **D:** `corp-monorepo` working tree only (`models/`, `src/corp/extractor/data/`) | none declared. Carried from batch-2 wave 2 |
| `[#282]` | fleet `.gitattributes` EOL-normalization parity | P3/S | **D:** one `.gitattributes` per consumer; **3 of 4 remain** (corp-ops, corp-sca, demo-prep — ai-council done 2026-07-08) | none declared. Splits per repo, so it can be one lane or three |
| `[#334]` | fleet-wide ruff hook id migration `ruff` → `ruff-check` | P3/S | **D:** three `.pre-commit-config.yaml` (hub + corp-monorepo + ai-council) + hub `CLAUDE.md` §9 roster line + doc-counts | `serialize-group: pre-commit-config` (5 ids: `#345 #132 #334 #351 #369`). **Row's own text forbids splitting it**: *"ONE coordinated arc across hub + corp-monorepo + ai-council, never per-repo drift"* |
| `[#315]` | `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried | P3/S | **D:** `deploy/manifest-v*.yaml` + `plugins/tier1-lifecycle/INSTALL.md` + one consumer root | pairs with `[#280]` (both need the same doc-carrier); no serialize-group |
| `[#280]` | propagate the intake area to greenfield consumers via the deploy manifest | P3/S | **D:** `deploy/manifest-v*.yaml`, `templates/intake-template.md`, `docs/intake/README.md` | **collides with `[#315]`** on `deploy/manifest-v*.yaml` — same doc-carrier gap; a shared lane or an ordered pair, not two lanes |
| `[#290]` | floor-carrier verify-teeth + self-heal | P3/S | **D:** `deploy/carrier_floor.py` + tests | none declared; **touches `deploy/`, which `[#315]`/`[#280]` also enter** — different files, same directory |
| `[#281]` | re-peg the ai-council ADR-66 story-map convergence | P2/S | **D:** a recorded peg (hub) + possible `ai-council` BACKLOG surface | pairs with `[#331]` (the adoption ruling it is downstream of); `[#294]` is its named blocker |

### 3.3 Two structural facts that bound this pool

**(a) Every consumer row above is ADR-41 queue-only in the hub, and RULING-W is the only shape
that makes it a lane.** `[#283]`, `[#393]`, `[#416]` and `[#282]` each say some version of *"routes
via the consumer session; the hub files it, never writes it."* Batch 2 squared that by declaring the
lane footprint as `<consumer> working tree only (consumer worktree/branch shape, RULING-W)` —
`docs/audits/2026-08-07-technical-batch-2-manifest.md` lanes 4–6. RULING-W is canonical at
`protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md` Ch8: **consumer worktree/branch → report,
never a direct push into a live consumer checkout, re-witness the consumer live first.**

**(b) The reason batch 2 carried all three consumer lanes is unresolved.** Every wave-2 lane was
carried for the same stated cause — *"satellite repo lacks the enforcement organs the lane would
need"* (batch-2 packet §9). **Nothing in the 2026-08-06/07 window deployed enforcement organs to a
satellite.** So the successor plans batch 3 into the same condition batch 2 declined, unless it
either (i) re-witnesses the satellites and finds the premise stale, or (ii) accepts a lane that
runs without the organs and says so in the manifest. **This document does not pick.** It records
that the choice exists and that this container cannot make it (§6).

### 3.4 The process-lane side (for completeness — at width 6, exactly one slot)

Open rows that clearly target methodology/hub-process surfaces and are ready enough to be a lane:
`[#505]` (P1/M, `footprint:` **declared**, `serialize-group: playbook`), `[#506]` (P2/M,
`footprint:` **declared** — whole-set P10 grooming; its own text splits it into a READ-ONLY
evidence-sheet half that *"may run parallel to any batch"* and an adjudication half that
serializes), `[#507]` (P3/S, declared, `architecture`), `[#508]` (P3/S, declared, `gates`),
`[#511]` (P2/M, `handoff`), `[#512]` (P2/S, `gates`). **Six candidates for one slot** — which is
the cap doing exactly what it was written to do.

---

## 4. P-B pool and the `[#491]` / `[#492]` state

### 4.1 The P-B pool, re-counted

Intake #27 §C defines P-B as *"gap-week S-evals (~9 items): cheap, independent, one sitting each
(12, 18, 20, 22, 23, 33–36)"*, and STANDING_RULINGS **E1** carries the standing rule
*"gap-weeks consume P-B evals"*.

| §A # | Item | P-B state today |
|---|---|---|
| 12 | lychee `--include-fragments` | **live** — ADOPT-candidate, not in `.pre-commit-config.yaml` |
| 18 | schema-as-code (W-6) | **live**, and still floats behind W-5 (row 17) whose premise moved |
| 20 | local-vs-reference matrix (W-8) | **live** — the parent intake calls it *"candidate for a one-line register ruling"*, which STANDING_RULINGS now has a section for |
| 22 | VISION→README (W-9b) | **live** |
| 23 | `.claude/skills` ↔ `.agents/skills` symlink (W-9d) | **live** |
| 33 | pytest-xdist | **LEAVES THE POOL — adopted** (§1 row 33) |
| 34 | jsonc-parser | **live** |
| 35 | check-jsonschema | **live** |
| 36 | mise | **live**, with fresh evidence from tonight (§1 row 36) |

**Pool: 9 → 8.** One item graduated by adoption, which is the pool draining the way it was
designed to. Nothing was added. (Phase R of this window proposes candidate *additions* to §A —
**proposal only**, in `docs/audits/2026-08-08-technical-library-research.md`; the operator assigns,
and this document births nothing.)

### 4.2 `[#491]` Gemini lane

- `tasks/491-*.md` — `status: open`, `[P3][S]`, theme `[E7]`, story `[S19]`, no serialize-group.
- Intake #27 pegged it `SCHEDULED(batch-2 grooming)`. **Batch 2 ran and closed without it.** The
  peg is spent (§1 row 1).
- Its Done-when has **two** clauses and neither has moved: *"the R-G one-line ruling is recorded"*
  — grep of `protocols/STANDING_RULINGS.md` for R-G: no match — **and** *"the lane has passed one
  real-work acceptance run with spot-verification evidence."*
- Its acceptance subject is `[#487]`'s ranked sheet or the fleet dependency scan. `[#487]` is
  **open** (`[P2][L]`), so the first option's input does not exist yet.
- The row's own hard constraint, restated because it is easy to lose:
  **retrieval-not-classification is baked into every Gemini contract, by ruling, on a measured
  incident** (a fan-out leg fabricated an ADR count).

### 4.3 `[#492]` Grok lane — the peg, and what the first task is

- `tasks/492-*.md` — `status: deferred`, clause `DEFER — peg: ≥ 2026-08-07, the Grok 4.6 release`.
- **The peg date has arrived** (this document is dated 2026-08-08). Whether *Grok 4.6* has actually
  shipped is an **off-repo fact this section does not assert** — see
  `docs/audits/2026-08-08-technical-library-research.md` §8 for what the network could and could
  not establish tonight.
- **The seeded-defect list is still unwritten.** A repo-wide grep for a seed/seeded-defect artifact
  returns only prose inside sealed handoff bundles — no `docs/` artifact exists. Per the row, that
  list *is* the method: *"seed a defect list drawn from THIS fleet's own history (vacuous test,
  fail-open except, stale locator, fence corruption) into real diffs, then compare catch rate
  against the terra baseline on the SAME diffs."*
- **So the eval's first task is writing that list**, and the four named classes are already the
  list's spine. Raw material for it exists and is locatable — each class has witnessed instances in
  this repo's own record (e.g. the vacuous-pass class named in JOURNAL 2026-08-07 (d); the
  fail-open→fail-closed flip in ADR-85 amendment §A5/§A6; the stale-locator class as `[#503]` and
  `templates/prompt-template.md` v1.8's four rotted line anchors). **Assembling it is the eval's
  work, not this document's** — listing it here would pre-commit the seat that runs it.
- The row also carries a birth-time obligation worth surfacing: **artifact-or-RED, and the severity
  tally written into the artifact body from day one** — the `[#480]` durability property applied at
  birth rather than retrofitted. Live relevance: `audit.py health` currently WARNs that one
  existing artifact carries no parseable tally (§1 row 4), i.e. the retrofit problem is visible in
  the tree right now.

---

## 5. Carried decisions — the list only the operator can take

Each item below is **carried, not adjudicated**. Where a source document proposed an answer, the
proposal is quoted as that document's, and the fact that it is unlanded is stated.

### 5.1 `win-tooling` has no `origin` remote — 14 branches on one disk

- **Source:** `docs/audits/2026-08-07-technical-batch-2-lessons.md` §4 item 1, which calls it
  *"Highest-value item on this list: it is the only one where the failure mode is losing work."*
- **State:** found by lane-3, outside `[#320]`'s Done-when (which names three repos, all
  discharged), so it did not block that close.
- **Fork, as recorded:** *add a remote* **or** *accept-local with a recorded reason*. Both are
  dispatch acts, and were explicitly forbidden to batch 2's integrator and to the consolidation arc.
- **UNVERIFIED here:** this container has no `win-tooling` checkout (§6). The 14-branch figure is
  quoted from the lessons register, not re-counted.

### 5.2 The 3.2 ratification — the ≤1/4 process-lane cap is width-dependent

- **Source:** `docs/audits/2026-08-07-technical-batch-2-lessons.md` §3.2.
- **The finding:** the manifest planned width 6 as 5 feature/consumer + 1 process, compliant. The
  batch **ran at width 3**, and `floor(3/4) = 0` process lanes are permitted at that width — so the
  executed batch exceeds a cap it was planned to satisfy, **retroactively, without anyone doing
  anything.**
- **The proposal, quoted, unlanded:** *"Evaluate the cap against **dispatched width**, and report
  the **close-width delta** in the end-of-batch packet."* Rationale recorded there: the cap exists
  to stop methodology work expanding to fill available width, and that expansion is a
  planning-time behaviour, so planning-time width is the honest denominator.
- **Why it is the operator's:** the cap's text is operator-directive doctrine (2026-08-06) carried
  by intake #27. Its live home is `protocols/PLAYBOOK.md` Ch8 (quoted in §3 above) and
  `docs/decisions/ADR-110-parallel-execution-batch-protocol.md:189`.

### 5.3 The 3.3 ratification — `[#505]` clause 2, per batch or per integration?

- **Source:** `docs/audits/2026-08-07-technical-batch-2-lessons.md` §3.3.
- **The measurement:** counted from session transcripts — AM4-FOLD 1, lane-1 2, lane-2 1, lane-3 1,
  integrator 1 = **6**, plus the packet hand-back = **7**. *Per-batch reading:* 7 ≫ 2, **falsified.**
  *Per-integration reading* (what `/lane-integrate` §0 actually says): the GO plus the packet =
  **exactly 2, met.** The row does not say which it means; the packet declined to pick, on the
  stated ground that *"a single number there would have been a choice dressed as a measurement."*
- **The proposed sentence, quoted verbatim so ratification is a yes/no rather than a drafting
  exercise:**
  > **Clause 2 (proposed).** The 2-touch budget is measured **per seam, per batch**, and the two
  > seams are counted separately. *operator ↔ integration*: the GO at dispatch and the
  > end-of-batch packet at close — target exactly 2. *operator ↔ lanes*: one dispatch per lane,
  > plus any ask-class (a)–(c) escalation — target ≤1 escalation per batch, reported in the packet
  > rather than budgeted away. A batch reports both numbers; neither substitutes for the other.
- **State:** **not landed**; `[#505]` stays `open` (`tasks/505-*.md`).

### 5.4 The ADR-87 residual, and what this window's Phase 1 did and did not do to it

- **Source:** `docs/audits/2026-08-07-technical-batch-2-lessons.md` §4 item 2, which Ch8's own text
  points at.
- **The residual:** the Ch8 routing matrix puts model **and** effort on the architect's dispatch
  line; ADR-87's equilibrium ("The two lifelines" § Lifeline 1, restated at PLAYBOOK §2 "How to
  choose Model") puts model selection on CC's side. `e03df5c4` declared a **population boundary**
  rather than editing either. *"The residual: the ADR-87 table and its §2 restatement still read as
  architect-excluded on the dispatch act itself."*
- **What Phase 1 of this window did:** amended the matrix's Model row (opus is the
  `.dev-knowledge` default; sonnet narrows to small **and** self-contained) plus the
  `prompt-template` point-of-use copy.
- **What it did NOT do, stated so nobody reads it as discharged:** it did not touch ADR-87, the
  equilibrium table, or the §2 restatement. **The residual is exactly as open as it was**, and the
  fork is unchanged: *ratify the boundary as written, or rule an ADR-87 amendment.* Phase 1 made
  the matrix stronger, which arguably raises the stakes on the residual rather than lowering them.

### 5.5 `check-seal-identity` fails on an immutable bundle

- **Source:** `docs/audits/2026-08-07-technical-batch-2-lessons.md` §4 item 3.
- **The defect, re-verified live here rather than quoted:**
  `docs/handoffs/2026-08-01-dev-knowledge-architect-2/HANDOFF_BOOT.md` carries
  `| **Slug** | `2026-08-01-dev-knowledge-architect` |` while its directory carries the `-2`
  suffix, and **both directories exist** — so the internal slug names a *different, real* bundle.
  The lessons register attributes it to `80dd54d6` and calls it untouched by batch 2; **that SHA
  does not resolve in this shallow clone**, so the attribution is carried as a quote, while the
  mismatch itself is a direct observation.
- **Why it is the operator's:** `docs/handoffs/` is immutable (CLAUDE.md §5 rule 3), so this is a
  real defect in an artifact that cannot be edited. It will fail every `pre-commit run --all-files`
  sweep **until someone rules how an immutable bundle with a bad seal gets retired.**
- **Direct bearing on the morning:** the morning cut runs `check-seal-identity` at commit time
  (CLAUDE.md §9). The hook is staged-file-scoped, so a new bundle's own commit is unaffected — but
  an `--all-files` sweep on the same machine is not. See
  `docs/audits/2026-08-08-technical-handoff-cut-staging.md` §3.

### 5.6 `[#502]` — the import convention underneath the mutmut chain

**Stated honestly first: "the `[#502]` import convention" does not resolve to a single in-repo
locator.** No `tasks/*.md` row and no audit artifact carries that phrase. What the repo does carry
is the substrate, re-measured live tonight:

| Fact | Live value | How read |
|---|---|---|
| `sys.path.insert` occurrences | **100** across **92 files** | `grep -rn 'sys.path.insert' scripts/ deploy/ tests/ --include=*.py` |
| …by area | `scripts/` 19 in 15 files · `deploy/` 6 in 6 · `tests/` **75 in 71** | same |
| `conftest.py` anywhere | **none** — neither root nor `tests/` | `ls conftest.py tests/conftest.py` → both absent |
| packages that do exist | `scripts/codemap/`, `scripts/toc/`, `deploy/lived_sandbox/` only | `find scripts deploy -name __init__.py` |
| the declared stance | `package = false`, *"flat-layout governance repo, never built or installed"* | `pyproject.toml` `[tool.uv]` |

**The Δ that makes this a decision and not a curiosity:** the last recorded measurement of this
class (JOURNAL, `sys.path.insert` root-cause paragraph) was *"17 `sys.path.insert` sites … no
`conftest.py` anywhere … 30 test files each duplicate the mutation."* Live today: **100 occurrences
across 92 files.** The class grew ~3× in files and ~6× in occurrences while nothing ruled on it.

**How it connects to `[#502]`:** two of the three mutmut blockers were import/location assumptions,
not test logic — the dotless-checkout literal and the `mutants/`-sandbox partial tree (JOURNAL
2026-08-07 (c) and (d)). A flat layout that every module re-mounts by hand is the surface those
failures live on. **Trade-offs of each standard fix shape, costed against this repo, are in
`docs/audits/2026-08-08-technical-library-research.md` §5 — as analysis, not as a recommendation.**

### 5.7 `[#511]` — the handoff-cut fork

- `tasks/511-*.md`, `[P2][M]`, `open`, `serialize-group: handoff`.
- **Measured 2026-08-07:** mechanized cost of a cut + live probe gate is **~4.5s = 0.25%** of the
  30-minute wall clock (`docs/audits/2026-08-07-technical-handoff-engine-thinning.md`). **It is not
  a performance row.**
- **Where the time actually goes:** 15 FILL-IN markers, a 38,067-byte `PASTE_THIS.md`, and 14
  probes that `/handoff-verify` re-derives live.
- **One number in that row does not match the newest bundle on disk, and the difference is not
  reconciled here.** `[#511]` records 38,067 bytes; the live
  `docs/handoffs/2026-08-06-dev-knowledge-architect/PASTE_THIS.md` is **51,138 bytes** (`wc -c`).
  Reproducing 38,067 would mean running a cut, which this window is forbidden to do, so the gap is
  **reported, not resolved** — the plausible causes (a filled supplement folding into the paste, a
  different bundle, a pre-fill measurement) are not distinguishable without that run. If the fork
  is decided on byte load, re-measure first.
- **The fork, quoted:** *"cut FILL-IN count (vs RF-6), probe count (vs §5), or verify pass (vs
  anti-bluff) — any cut is a version bump + reconciliation."* Each candidate cut trades against a
  named invariant, which is why it is a doctrine decision and not an edit.
- **One precision worth carrying into the ruling:** "15 FILL-IN regions" counts **markers**, not
  regions. Live census of the 2026-08-06 bundle: `HANDOFF_BOOT.md` 8 markers / **4** regions,
  `RESIDUAL.md` 6 markers / **3** regions, `PROBES.md` 1 marker / **0** regions (that one marker is
  a *reference* to the boot region inside P0c's command, not a fill site). **15 markers, 7
  authored regions.** If the ruling is "cut the FILL-IN count", 7 is the number it is cutting.

### 5.8 `[#399]` and `[#512]` — two rows on the same generator, ready as stated

Both are open, both `[P2]`, and both are unusually well-specified — each names its file, its line,
its fix and its regression test, so neither needs a design round.

| | `[#399]` | `[#512]` |
|---|---|---|
| size | S | S |
| group | `handoff` | `gates` |
| defect | `protocols/HANDOFF_PROCESS.md:481` declares `docs/handoffs/README.md` is rendered "from one source" (the v5 `.tmpl`) but **no script reads the `.tmpl`** — `seed_runbook.py:85/:106` generalizes from the already-rendered hub README | `batch_manifest._git()` (`scripts/batch_manifest.py:140`) runs `subprocess.run` with **no `env=` scrub**, so an inherited `GIT_DIR` redirects the read and `gen_handoff.py:403`'s open-batch refusal silently sees no open batches |
| class | phantom-enforcement (`[#359]`) | missing scrub — explicitly **not** a duplicate of `[#396]`, which DRY-consolidates a scrub that already exists in three places |
| decision content | three-way: build it / correct `:481` to name the real source / record accepted-with-reason — **and** decide the `.tmpl`'s fate (live source vs archived) in the same pass | none — the fix shape is stated; only scheduling is open |
| bearing on the morning | the morning cut writes into `docs/handoffs/`; the `.tmpl` claim is about the **index**, not the bundle, so it does not block a cut | **a real, if narrow, hazard for the cut**: the refusal that protects against sealing mid-batch is the one with the unscrubbed read. Mitigation for the morning is environmental, not a code change — see the staging doc §3 |

---

## 6. What this container could not see — SKIPs, each with its structural reason

Stated per the window contract: a SKIP is allowed only where the check is **structurally
impossible here**, and the reason is named.

| Skipped | Structural reason | What it means for this document |
|---|---|---|
| every sibling-repo fact (`ai-council`, `corp-monorepo`, `corp-sca-time-automation`, `win-tooling`, `corp-ops`, `demo-prep`, `life-architect`, `terminal-setup`) | the cloud container clones **one** repo; `/home/user/ai-council` and `/home/user/corp-monorepo` are not git repos — `audit.py health` reports exactly that under `fleet_parity` | §3's consumer footprints are derived from **hub-side row text only**; §5.1's 14-branch figure is quoted, not re-counted; §2.3 item 3 is explicitly UNVERIFIED |
| `pre-commit` hook execution | `pyproject.toml` pins `required-version = "==0.11.19"` (ADR-106) and this container ships uv `0.8.17`; `uv self update 0.11.19` reports the version is not available. Every hook whose entry is `uv run --locked …` is unrunnable | validators were run **directly** against the system interpreter instead, and each verdict is recorded in the commit messages rather than assumed |
| `journal_spine_anchor` | the clone is **shallow** (246 commits); the disposition floor `24882f8cc` is not in this history, so the backstop cannot answer. It reports the unknown state rather than passing | recorded as an inherited container FAIL; every *other* SHA this document cites was checked to resolve (`git cat-file -t`) before being written down |
| `hooks_armed` | follows from the uv row above — the hooks cannot be installed, so the check correctly reports them absent | inherited container FAIL |
| any `~/.claude` (user-layer) fact | out of the container by construction; the window contract forbids touching it | `[#338]`(c) and the win-tooling PowerShell-profile item are carried as **untouched**, and the library research treats the second as analysis only |

---

## 7. Provenance

Produced unattended on `claude/night-cloud-contract-exec-g4bk91` from base `81d572d7` under a
frozen operator contract. **No merge, no push to `main`, no bundle cut, no supplement answer, no
row born or closed, no batch machinery edited.** Sibling documents from the same window:
`docs/audits/2026-08-08-technical-handoff-cut-staging.md` (the morning cut's pre-verified fills and
runbook) and `docs/audits/2026-08-08-technical-library-research.md` (library-first research +
this window's own critical review).
