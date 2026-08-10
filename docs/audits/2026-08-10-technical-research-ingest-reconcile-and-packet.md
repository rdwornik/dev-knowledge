# Research-ingest lane A — orphan-split reconcile ledger and end-of-arc packet

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10
- **Source-session:** batch lane A, worktree `ingest-research-corpus`, branch `worktree-ingest-research-corpus`; base HEAD `12ef9c91`; lane commits `f571ac3c` (corpus) → `1cb4c09d` (distillate) → this file
- **Status:** complete — reconcile verdicts are findings, not decisions; the two draft folds await an operator GO ruling
- **Model:** opus (effort high), unattended background lane

Companion artifact: **`docs/audits/2026-08-10-technical-research-corpus-distillate.md`** — the ONE distillate table (59 proposals × 10 columns), the extracted seeded-defect-corpus spec (§4), the commission-5 halves with candidate homes (§4.7), and the two draft fold texts (§5). This file is the reconcile ledger and the lane packet; it does not restate the table.

## 1. Reconcile ledger — every orphan-split element, landed vs new

**Baseline is two commits, not one.** The lane contract names `6a4a1d78` ("ARC-2 Phase D — the three orphan commissions homed: 1 new intake, 2 amendments, 1 scope note"). Verified live: a **second** commit, `036385a6` ("file #30 and #31 verbatim — the two id-reserved drafts land"), landed intakes `#30` and `#31` after it. That second commit closes a gap `#32` itself recorded as open — its `note:` says 30/31 are "RESERVED, not free… that 30/31 are still unfiled is a NOT-COVERED item in the coverage diff, not a closed question." **It is now a closed question**, and the reconcile is scored against both commits.

### 1.1 The four elements `6a4a1d78` landed — all four confirmed LANDED, none re-applied

| Element | Commission | Landed at | Verified live | Verdict |
|---|---|---|---|---|
| Intake **#32** (new) — compute placement | 6 · `wf-1dc18e42` | `6a4a1d78` | `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md`, `intake-id: 32`, `status: DRAFT` | **LANDED** — not touched by this lane |
| **#29 Fold A** — agent instrumentation & telemetry | 3 · `wf-02c940ef` | `6a4a1d78` | `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md` §"Fold A — agent instrumentation & telemetry (memo `wf-02c940ef`)" | **LANDED** — not touched |
| **#29 Fold B** — dependency/ontology graph | 2 · `wf-f6851745` | `6a4a1d78` | same file, §"Fold B — the dependency/ontology graph (memo `wf-f6851745`)" | **LANDED** — not touched |
| **#25 W-9(a) scope note** — multi-provider portability | 4 · `wf-d68b2f7f` | `6a4a1d78` | `docs/intake/2026-08-05-func-simplification-distribution-wave.md` §"SCOPE NOTE 2026-08-09 … the portability commission folds into W-9(a)" | **LANDED** — not touched |

### 1.2 The two elements the contract expects to be NEW — both confirmed genuinely un-landed

| Element | Commission | Why it is new, not landed | Draft text |
|---|---|---|---|
| **Seeded-defect corpus spec** → `#29` amendment | 3 · `wf-02c940ef` | Fold A landed the *ruling* — "no bake-off runs before the seeded-defect corpus exists" and the model-comparison bar (paired designs, 5–10 repeats, bootstrap CIs). It **named an artifact it never specified**: no size, no defect classes, no generation strategy, no scoring axes, no leakage constraints. The spec is un-landed. | distillate **§5.1**; full spec **§4** |
| **Decision-lifecycle half** → `#30` §A fold | 5 · `wf-fafd931b` | `#30` §A exists and proposes the landing-predicate organ, but carries **no reference to this memo** — the external convergence, the industry name (architecture fitness functions + ADR-to-code traceability), the coverage bar ("every non-retired ADR should map to ≥1 fitness function"), and the library-first candidate order (import-linter / Conftest / pytest) are all absent. | distillate **§5.2** |

### 1.3 Elements the contract's ledger does not name — found by this reconcile

| Element | Commission | Finding | Verdict |
|---|---|---|---|
| Intake **#31** — code-style doctrine | 1 · `wf-8a83eb70` | **LANDED, outside the contract's baseline.** `036385a6` filed `#31` verbatim; its `origin:` credits "the commissioned research report 'Enforcing a universal code-style doctrine across an LLM-written Python fleet'", and §A–§F map onto the memo (TASTE/MECHANISM split, adoption-order stack, mechanical LIBRARY-FIRST, no-refactor-without-hotspots, caveats, hand-rolled pieces declared). The commission is homed **and consumed**. | **LANDED** — no fold owed. One provenance gap, now closable: `#31` cites the report by **title only, never by `wf-` id**, so before this lane there was no resolvable path from intake to source. The landed file is `docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md`. |
| Intake **#30** — verification organ | — | **LANDED** at `036385a6`; closes `#32`'s recorded NOT-COVERED item. | **LANDED** |
| **Session-continuity half** of commission 5 | 5 · `wf-fafd931b` | **UN-OWNED BY ANY INTAKE.** The memo splits cleanly in two and only the decision-lifecycle half has a named destination. R43 (plan-carrying residual), R50 (drop the boot-time pass table), R51 (verification-at-cut / exceptions-only boot) belong to no intake. | **NEW, and homeless** — four candidate homes offered as options in distillate §4.7; **decision budget fired** (fork class, no standing ruling) → batched question **Q2** below |

**Coverage result: all six commissions are homed.** Five were homed before this lane (four by `6a4a1d78`, one by `036385a6`); the sixth is homed in halves, one of which is homeless. Nothing was silently dropped, and nothing this lane did needed a new intake.

## 2. Double-application check (the risk the contract names)

**Result: zero double-application.** This lane edited **no** intake, **no** ADR, and **no** BACKLOG file. Verified mechanically — the lane's complete diff against base `12ef9c91` touches nine files, all of them under `docs/archive/` and `docs/audits/`:

```
docs/archive/2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md   (new)
docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md               (new)
docs/archive/2026-08-09-research-compute-placement-wf-1dc18e42.md                 (new)
docs/archive/2026-08-09-research-dependency-ontology-graph-wf-f6851745.md         (new)
docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md        (new)
docs/archive/2026-08-09-research-session-continuity-decision-lifecycle-wf-fafd931b.md (new)
docs/archive/README.md                                                            (index entry)
docs/audits/2026-08-10-technical-research-corpus-distillate.md                    (new)
docs/audits/README.md                                                             (generated index)
```

The four landed elements of §1.1 were **read as the reconcile baseline and left byte-identical.** The two expected-new elements exist only as draft report text in the distillate §5, awaiting a GO ruling.

## 3. A premise this lane refuted — recorded, because it is stated in three places

Three sites assert that **no in-repo home exists for an external research memo.** Verbatim, from intake `#32`'s Provenance:

> "**The memo file itself is deliberately NOT landed in this repo** — no governance clause defines a home for external research artefacts, and ADR-101 seals the tree against inventing one."

The same sentence appears in the `#25` W-9(a) scope note's Provenance, and in `6a4a1d78`'s commit body ("NO MEMO FILE IS LANDED, and the governing clause is quoted rather than assumed: no governance clause defines a home for external research artefacts").

**A clause does exist, and it required inventing nothing.** Quoted verbatim, in the order they bind:

- **ADR-60** (Accepted 2026-05-27), `.dev-knowledge` taxonomy table: "`archive/` | ARCHIVED — pending-classification zone"; and §"`archive/` semantics (clarified)": "**Deliberate holding zone for 'don't yet know where this belongs.' Reviewed periodically; each item either deleted (git history retains) or promoted to `decisions/`, `audits/`, `handoffs/`, `diagrams/`, or authored into an ADR.** Every repo's `archive/` carries a `README.md` documenting this. Not a dumping ground — a triage queue."
- **ADR-101 §1 Tier-2**, the tree seal itself: "Sanctioned: `archive/ audits/ decisions/ handoffs/ intake/`." Confirmed in code — `SANCTIONED_GENRES` in `scripts/validate_hermetization.py` contains `archive`. **Landing here creates no folder and trips no seal**; the `validate-hermetization` gate passed on the landing commit.
- **`docs/archive/README.md`** §"Naming convention": "`YYYY-MM-DD-{descriptive-slug}.md` — same as the live `docs/` folders, so a file's date is visible on archive too."
- **Class precedent, four files deep.** The folder already held four external-research memos landed under exactly this convention — `2026-04-23-llm-dev-patterns-2026.md`, `2026-04-24-claude-md-best-practices.md`, `2026-04-24-multi-agent-debate-patterns.md`, `2026-04-27-handoff-patterns-external-research.md` — plus `2026-06-05-agent-automation-external-research-note.md`, whose own index entry cites "the external-research convention".

**Why ADR-101 Rule B does not reach the corpus, and why the distillate is the audits-class artifact.** Rule B's `<date>-<class>-<slug>` grammar is scoped to `docs/audits/*.md`. None of the ruled-eleven classes describes an external research memo — which is the second, independent reason the memos belong in `archive/` and the *distillate* belongs in `audits/`.

**What this is and is not.** It is **not** a ruling overturned: grep of `protocols/STANDING_RULINGS.md` and `ecosystem/disposition-register.yaml` finds **no** standing ruling or register entry on external-research artifact homes. It is a **premise, recorded in three places, refuted by quoted governance.** The lane contract's own instruction — "Derive the in-repo home from QUOTED governance… No clause → STOP, report, land nothing" — resolved it: a clause exists, so the corpus landed. **The three stale sentences are reported, not edited** (this lane may not touch intakes; two of the three are inside filed intakes). Repair channel is batched question **Q1**.

## 4. FAIL lines

**None. Zero FAIL lines.** All six inputs resolved on the first attempt under `C:\Users\1028120\Downloads`, and all six landed byte-identical (sha256 verified source-vs-landed, recorded in `f571ac3c`'s commit body). The failure mode the contract names — "the RESEARCH-INGEST predecessor died silently on an unresolved path" — did not occur and needed no operator round-trip.

## 5. End-of-arc packet

### 5.1 Files landed

Six memos, byte-identical, at `docs/archive/`, each named with its source `wf-` id as a trailing token so the landed file resolves to its commissioning artifact without depending on the index surviving. One line quoted from each, as its own identity:

- **`2026-08-09-research-code-style-doctrine-wf-8a83eb70.md`** (commission 1) — *"Mechanize almost everything, write down almost nothing… The 'philosophy' (OO vs functional) is mostly taste; the only enforceable slice is function/module size, complexity ceilings, naming rules, and import boundaries."*
- **`2026-08-09-research-dependency-ontology-graph-wf-f6851745.md`** (2) — *"Build the graph as a committed, regenerated JSONL 'edge log' that every existing validator emits into… not a new database platform, not a running server, not a SaaS."*
- **`2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md`** (3) — *"Most of what you want is already recorded… Your first move is extraction, not plumbing."*
- **`2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`** (4) — *"The portability bet is defensible but narrow… the instruction-file layer ports cleanly, but everything richer (slash commands, hooks, subagents, permissions, skills) must be re-authored per tool."*
- **`2026-08-09-research-session-continuity-decision-lifecycle-wf-fafd931b.md`** (5) — *"Your architecture is ahead of common practice on session handoff and enforcement, but behind on retirement."*
- **`2026-08-09-research-compute-placement-wf-1dc18e42.md`** (6) — *"Fix the laptop first — most of this is a local defect, not a capacity limit… Buying compute now would paper over a bug."*

Plus `docs/archive/README.md`, which gains a dated subsection recording the corpus, per-memo one-liners, and honest promotion semantics (the promotion target is the intake/ADR each proposal feeds, **not** promotion of the memo itself). The pre-existing nine-item list is unchanged, moved under its own heading.

The governing clauses for the home are quoted in full in §3 above and in `f571ac3c`'s commit body.

### 5.2 Table path

**`docs/audits/2026-08-10-technical-research-corpus-distillate.md`** — the ONE distillate table, 59 proposal rows (R01–R59) plus one cross-cutting numbers row (R60), with the contract's ten columns exactly. Consumed-correctly proof: 8 rows in `declined-on-measured-repo-grounds` (12 declines counting §3's self-declines), 7 rows in `false-about-this-repo` (9 distinct claims). 27 rows carry a `LANDED-ALREADY` locator, every one verified to exist on this branch before being cited.

### 5.3 Reconcile verdicts

`#32` LANDED · `#29` Fold A LANDED · `#29` Fold B LANDED · `#25` W-9(a) LANDED — none re-applied. Seeded-defect corpus **NEW** (draft §5.1) · decision-lifecycle **NEW** (draft §5.2). Beyond the contract's ledger: `#31` LANDED at `036385a6` (commission 1 homed and consumed) · `#30` LANDED at `036385a6` (closes `#32`'s NOT-COVERED item) · **session-continuity half UN-OWNED**. All six commissions homed; one half homeless.

### 5.4 Suite result

**First run — `uv run --locked pytest -q`, 693.65s (11:33):** `19 failed, 2690 passed, 11 skipped, 1 xfailed`.

Nineteen is not the honest number. Classified, and each class proven rather than asserted:

**(a) 17 × environmental — a lane-venv gap, now fixed.** Every one was `tests/test_fleet_analytics.py … MododuleNotFoundError: No module named 'pandas'`. A fresh lane worktree venv does not carry the `analytics` dependency group. Fixed with `uv sync --locked --group analytics` (installed numpy 2.5.1, pandas 3.0.5, python-dateutil, six, tzdata) and re-run: **all 17 now pass** (`2 failed, 86 passed` across the three re-run targets). Not a code RED, and not this lane's.

**(b) 1 × standing RED — `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`.** This is the `[#348]`/`[#426]` family the contract names. Note precisely what fails: the *check* passes (`f.status == "pass"`); the *test* fails on its pinned evidence string — it asserts `"1 declared routine row"` and the live evidence reads `"2 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426])"`. The test's own docstring says why that matters: "If this number moves, the ADR, the docstring and `[#426]` must move with it." So a second backlog row gained a routine declaration and the three coupled sites did not follow — exactly the drift the test exists to catch.

**(c) 1 × worktree-induced — `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary`.** `aud._REPO_ROOT` resolves to this lane's own linked worktree, so the primary-exclusion property is false by construction when the suite runs from inside a worktree. The assertion names three live linked worktrees (`arch-claims-fix`, a `…t-absorb-prep`, and `ingest-research-corpus`). Structural to running in a lane, not a defect.

**Proof that neither (b) nor (c) is this lane's**, since a lane that RED-ed the suite and reported it as inherited would be the worst failure mode here:

- `git diff --name-only 12ef9c91..HEAD | grep -E "BACKLOG|\.py$|tests/"` → **empty**. This lane touched zero BACKLOG rows, zero Python, zero tests. Its whole diff is nine markdown files under `docs/archive/` and `docs/audits/`.
- The routine-declaration change came in at `a8c62956` ("attach two evidence findings to `[#419]` and `[#310]`"), and `git merge-base --is-ancestor a8c62956 12ef9c91` → **true**: the drift predates this lane's base commit.

**Honest suite verdict: 2 REDs, neither introduced by this lane** — one standing declaration-count drift (b) and one worktree artifact (c). **Reported, not dispositioned**: (b) is a real coupled-sites drift that belongs to `[#426]`, and this lane has no mandate to close, retitle, or re-pin it.

**Other gates.** `ruff check` — **All checks passed**. `python scripts/gen_doc_counts.py --check` — all three counts **match** (`audit_check_count` 41/41 · `precommit_hook_count` 17/17 · `pytest_collected` 2721/2721), which incidentally verifies two figures the memos assert about this repo.

### 5.5 Gates

Zero `SKIP=`, zero `--no-verify` across all lane commits. Every pre-commit run was clean; `validate-hermetization` passed on both content commits (confirming both the `docs/archive/` landing and the audits-class filename), and `audit-index-freshness` passed after `gen_audit_index.py --write`.

### 5.6 Batched questions — the decision budget, fired once, batched

Four items. Two are fork classes with no standing ruling (**Q2**, **Q4** — the budget's stated trigger); two are reporting items this lane is forbidden to fix itself.

> **Q1 — What is the repair channel for a stale or mis-cited sentence inside a filed intake?**
> Three sites say no home exists for a research memo (§3), which is now false. Separately, intake `#32` attributes "1785.6s → ~539s" to `STANDING_RULINGS` E1, which carries 1785.61s vs 358.77s / 330.15s (commit `d11dda35`); the 539s figure is real but sourced from `docs/audits/2026-08-08-technical-batch-3-packet.md:46`, already flagged as an observed divergence by the 2026-08-09 challenge-retrieval audit. Intakes are living-with-amendments rather than strictly immutable, but no clause says who may correct a **provenance line** or a **mis-citation** versus append an amendment. Options: (a) an amendment block on each affected intake; (b) a correction recorded only here, leaving the intake text as the point-in-time record; (c) an in-place provenance fix, ruled as metadata rather than content (the ADR-94 status-line precedent, applied to intakes).

> **Q2 — Where does the session-continuity half of commission 5 live?** *(fork class, no standing ruling)*
> R43 / R50 / R51 belong to no intake. Four options, priced in distillate §4.7: (a) intake `#18` (handoff-process v6 proposal — they are all HANDOFF_PROCESS changes); (b) intake `#19` (night-shift handoff reform, if read as operator-design input); (c) attach to **`[#511]`**, whose live fork *is* R50/R51 — tightest coupling, smallest surface; (d) a new intake `#33` — cleanest ownership, but takes the pending set up by one, the same ceiling `#32` respected by filing at 32 rather than 30. **Lane recommendation, offered not taken: (c).**

> **Q3 — Does Phase 3 ratify ADR-111, given a distillate row depends on it?**
> R46 (audit-finding → backlog forcing function) is **DISCHARGED** by ADR-111 — but ADR-111 is `Status: Proposed`, not Accepted. So R46's discharge is "ruled, not ratified", and this distillate is itself an instance of the pipeline ADR-111 specifies (its `LANDED-ALREADY (locator)` column is ADR-111's DISCHARGED outcome, and its two proof columns are REJECTED). If Phase 3 ratifies ADR-111, R46 closes; if not, R46 stays open and this table's own method is un-ratified.

> **Q4 — Where does the seeded-defect corpus live, given it must be unreadable from the tree the agent works in?** *(fork class, no standing ruling)*
> The corpus's leakage constraint (distillate §4.4) requires a private/`.gitignore`d path the agent's tools cannot read, with git history sanitized — in direct tension with this repo's committed-artifact discipline, where an artifact that is not committed is not evidence. It also inherits `[#502]`'s host constraint: mutation generation needs `fork()`, Windows needs WSL, WSL is out by operator constraint, so it is CI-only and behind `[#501]`. This is a placement decision for ratification, not a build detail, and no clause covers a deliberately-unreadable artifact.

## 6. Commit-to-step mapping, and where this lane deviated from the contract

The contract asks for one commit per step. This lane landed **three** commits for five steps, for one stated reason: **audits are immutable** (`CLAUDE.md` §5 item 3 — "supersede with a new file or an in-file amendment marker; never edit in place"), so a step that adds a section to an already-committed audit cannot be its own commit without either editing an immutable artifact in place or attaching an amendment marker to content authored minutes earlier in the same arc, which would misrepresent the history.

| Step | Landed at | Note |
|---|---|---|
| 1 — derive home from quoted governance, land six memos | `f571ac3c` | governance quoted in the commit body and §3 |
| 2 — the ONE distillate table | `1cb4c09d` | ten columns exactly; both proof columns non-empty |
| 4 — seeded-defect spec + commission-5 halves | `1cb4c09d` | **committed with step 2**: both are named sections of the same artifact (distillate §4, §4.7). Splitting them would have meant editing a committed audit in place. |
| 3 — orphan-split reconcile ledger | this commit | §1–§2 of this file |
| 5 — full pytest + end-of-arc packet | this commit | §5 of this file; measured suite result in §5.4 |

Nothing in the contract's scope was skipped or narrowed. Everything the contract forbade was avoided: zero births, zero ADR edits, zero intake status or body changes, zero invented folders, zero merges, zero push, zero `SKIP=`, zero `--no-verify`, and no JOURNAL entry (a lane never journals — the integrator anchors at merge; the `Stop` hook is declined with that recorded reason).
