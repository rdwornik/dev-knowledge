---
intake-id: 91
status: DRAFT
origin: browser seat (Fable), Act 0b of window `2026-09-10-dev-knowledge-architect` — `to-cc/DECLARE-REVIEW-CONSUMPTION-2026-09-10.md`, which consumes the ten findings of `docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md` plus two findings of this window; landing form and this file's creation authorized by `to-cc/AMEND-SESSION-PLAN-003.md` §1
consumed-by:
---

# REVIEW consumption — the ten night-mission findings and two window findings, dispositioned

<!-- class: tech (decision carriage) · status: DRAFT — this is the BROWSER-SEAT declaration's
landing form, not an operator ratification. The table below is carried VERBATIM from
`to-cc/DECLARE-REVIEW-CONSUMPTION-2026-09-10.md`; the CC verification section beneath it is this
file's own addition and changes no cell. Fold-first: a row is filed only where no existing row's
Done-when can absorb the finding. -->

## The disposition table (verbatim from DECLARE-REVIEW-CONSUMPTION-2026-09-10)

**Landing form:** CC creates `docs/intake/2026-09-10-tech-review-consumption.md` (date-slug convention; authorization: AMEND-SESSION-PLAN-003 §1) carrying this table verbatim, files the FILE rows in `tasks/`, regenerates `BACKLOG.md`. New rows count against M4.

| # | REVIEW finding (line) | Disposition | Target / new row |
|---|---|---|---|
| 1 | :32 `[#644]` freeze never put to the operator | FOLD | `[#644]` — its Done-when already demands the DECLARE; operator sitting item 1 |
| 2 | :56 v1.5.0 floor ships `/override`, which discharges no gate | FILE | new row, P1: remove `/override` payload AND its manifest node together (`deploy/manifest-v1.5.0.yaml:995-1004`) — batch W lane L11; Done-when: node absent, payload absent, `release_lint.py` green, one test fails if either returns |
| 3 | :83 MA-1 guard refuses every non-Claude reader | FILE | new row, P1: `.claude/settings.json:21` — `$CLAUDE_PROJECT_DIR` resolved by the hook itself (repo-root fallback), matcher narrowed; Done-when: one non-Claude CLI smoke passes under the guard, a RED-first test fails when the fallback is removed — batch W lane L2 |
| 4 | :109 16-stage order enumerated nowhere | FOLD | `[#667]` (docs rewrite) — the enumeration lands in the recovery-plan intake §4 as part of that rewrite; until then the stage numbers are not cited |
| 5 | :132 `tasks/` frontmatter carries no execution position | FOLD | `[#669]` (conductor: transitions become a state machine over rows) — a state machine needs the position field; CC verifies the Done-when can carry it, else FILE |
| 6 | :158 the operator GO leaves no artifact | FILE | new row, P2: GO is a file (batch manifest line or `RATIFICATION-`), read by `/lane-boot` before dispatch; Done-when: dispatch refuses without it, one test fails when the check is removed — batch X |
| 7 | :182 three decisions unreadable from the tree | FOLD | HARNESS-IS-PROCESS → intake (R-6, L1); DISPATCH-SEAM → intake #90 (A4-4); HARNESS-PROVENANCE → S2 |
| 8 | :208 no telemetry has a consumer | FOLD | `[#627]` (multi-provider telemetry) — CC verifies; else FILE |
| 9 | :234 no gate has ever been proven to refuse | FOLD | `[#664]` clause "the three queries refuse at commit tier with a trip-test each" + ADR-108 §B RED-first; the general case is the per-row RED-first witness, already doctrine |
| 10 | :262 no alias layer for model names | FOLD | `[#582]` per the reviewer's mapping; not admitted this window |
| 11 | this window: P11 checks existence (a `carried-by:` passes while cited nowhere), P8b checks shape (N3 trimmed to 4,992 B), the P11 hand recipe over-globs `to-cc/` beyond the window's files | FILE | new row, P2, `[#664]` family: a carrier resolves only if the named home references the decision; P8b measures the seat's liveness not bytes; P11's population is the window's files by manifest — batch X |
| 12 | this window: BACKLOG view 270 lines vs `tasks/` 217 open rows | FOLD | `[#589]` (BACKLOG view projection with a size assertion) — CC verifies |

**Net:** 4 FILE (2, 3, 6, 11) · 8 FOLD (CC-verified: 5, 8, 12). Batch W after A4-2: L1 · L11 · L2 · L7 · L9.

## CC verification of the three CC-verified FOLDs — 5, 8, 12

Ordered by the DECLARE's own instruction: *"CC VERIFIES every FOLD against the target row's live Done-when before landing; a fold that does not fit is reported, not forced."* Verified against the live `tasks/` bodies at `7dbe7a4f`. **All three fail to fit. None was forced; none of the three findings is filed as a row here** — the disposition of each returns to the operator.

### FOLD 5 → `[#669]` — DOES NOT FIT

`[#669]`'s live Done-when, `tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md:13`, verbatim:

> Done when: each of the four transitions fires from a declared trigger with a trip-test proving it fires and a test proving it does NOT fire on the state before it; the operator's five decisions remain the only manual transitions and are named in the machine rather than implied; `archive_row_body` runs from its trigger rather than by hand; and emitted telemetry has a named consumer that reads it on the merge leg

No clause mentions a `tasks/` frontmatter field, an execution position, or row-level state storage. The row's own body states the opposite architecture: the conductor **CONSUMES** the `writes` / `triggers` edges of the `[#664]` spine "to decide a transition" — state is computed from the graph, not stored on the row. `[#669]` can therefore close in full while `tasks/` frontmatter still records no execution position. The finding survives its target.

### FOLD 8 → `[#627]` — DOES NOT FIT, and the clause it needs is in a different row

`[#627]`'s live Done-when, `tasks/627-agy-route-is-inert-no-row-authorizes-analysis-admission.md:12`, is wholly about agy's admission: the `analysis` role row existing in the authoritative table, admission gated on the SDA-1 analysis pack scored against C-1…C-15, the verdict landing as a `role_admission:` record on a model row that exists, and `ROUTING.md`'s agy line stating the outcome. **Telemetry consumption appears nowhere in it.**

The clause the finding needs already exists — in `[#669]`, quoted above: *"and emitted telemetry has a named consumer that reads it on the merge leg."* So finding 8 is absorbable, but by `[#669]`, not by the `[#627]` the table names. Re-pointing a FOLD to a different row is a disposition change, which is the operator's, so it is reported rather than applied.

### FOLD 12 → `[#589]` — DOES NOT FIT

`[#589]`'s live Done-when, `tasks/589-one-line-per-row-the-backlog-view-projection-wit.md:14`, verbatim:

> Done when: the generated view emits one line per row (`id · theme · status · title · one-line · pointer to tasks/<id>.md`), `gen_task_tree.py --check` carries a size assertion that FAILS on a deliberately inflated view (a test plants one), every field the old view rendered is either in the new line or reachable from its pointer, and `BACKLOG.md` measures under 70,000 bytes on an unchanged `tasks/`

Every clause is about **projection shape and byte size**. The 270-vs-217 divergence is neither. Measured at `7dbe7a4f`: the 53-row gap is exactly the rows whose `tasks/` frontmatter carries **`status: deferred`** — the `BACKLOG.md` view renders them as rows, while `boot_frontier.load_open_rows` (the `tasks/` counter, and `gen_ledger.py`'s source) excludes them. Sampled: `[#4]`, `[#19]`, `[#23]`, `[#43]`, `[#82]` — all `status: deferred`, all present in the view.

So the divergence is a **population/semantics** difference between two counters, not a projection defect, and `[#589]` can satisfy all four of its clauses with the gap unchanged. It is also not obviously a defect at all: "open" and "open + deferred" are two different questions, and no surface currently claims the two counters should agree. That judgment — defect or by-design — is not CC's to make.

## What this file does NOT claim

No operator ratification. The FILE rows below were filed with the Done-when text the DECLARE specifies, verbatim; their theme, story, size and priority are CC's assignment against the live enum and carry no ruling. The three failed FOLDs are **not** converted to rows here — the DECLARE's `else FILE` fallback is a disposition choice, and with all three failing for different reasons (one architectural, one mis-targeted, one arguably not a defect) the operator rules them rather than CC defaulting.

## Note for the next filer — two `[#675]`-class traps this filing hit

**Filing a row and landing an intake each trip a surface that is not the obvious one:** a task id is
NOT free just because `tasks/<id>-*.md` is absent — `tasks/manifest.json` must be checked too, or
`gen_task_tree.py --emit-source` REFUSES the regen reading the new file as a *retired allocation
record* that is not marked terminal (ADR-107 §6.3); and an intake add trips **three** surfaces, not
two — `gen_intake_index.py --write`, `gen_intake_tree.py --write`, and the `intake_tree_coherence`
audit leg that blocks the commit until the second one has run. Recorded per
`to-cc/AMEND-SESSION-PLAN-005.md` A5-5; both are the `[#675]` class (a manifest read that returns a
plausible wrong answer instead of failing).

## Rows filed from this table

- `[#683]` — finding 2, the `/override` node and payload in the v1.5.0 floor
- `[#684]` — finding 3, MA-1: the `PreToolUse` guard's unresolved `$CLAUDE_PROJECT_DIR`
- `[#685]` — finding 6, the operator GO leaves no artifact
- `[#686]` — finding 11, three gate predicates that measure the wrong property
- `[#687]` — finding 5, re-dispositioned FILE by `to-cc/AMEND-SESSION-PLAN-005.md` A5-2 after the fold into `[#669]` was verified and refused

---

## Resolution of the three verified FOLDs — `to-cc/AMEND-SESSION-PLAN-005.md`

CC verified FOLDs 5, 8 and 12 against the target rows' live Done-when (section above) and reported
all three as not fitting, without forcing any. A5-2/A5-3/A5-4 rule each one. **These rulings
supersede the `Target / new row` cell of rows 5, 8 and 12 in the table above; the table itself is
carried verbatim and is not edited.**

| Row | Table said | Ruled by A5-005 | Carrier |
|---|---|---|---|
| 5 | FOLD → `[#669]`, else FILE | **FILE** (A5-2) | new row `[#687]`, P2, `depends-on: #669`, batch X |
| 8 | FOLD → `[#627]`, CC verifies | **FOLD → `[#669]`** (A5-3) | `[#669]`'s existing clause; no new row |
| 12 | FOLD → `[#589]`, CC verifies | **REFUSED as a row** (A5-4) | none; the refusal is this record |

**Row 5 → FILE, as `[#687]`.** A5-2: *"`[#669]` computes state from spine edges rather than storing
it and can close with the finding unaddressed."* The new row's Done-when is A5-2's text verbatim —
*"a task's execution position is readable from the row or derivable from the spine, ruled one way,
with the reader named"* — which leaves the choice between the two mechanisms open and makes the
NAMED READER the deliverable. `depends-on: #669`, because the spine-derived option cannot be
evaluated before the conductor exists.

**Row 8 → FOLD into `[#669]`, not `[#627]`.** A5-3 re-points the fold to the row whose Done-when
already carries the clause: *"emitted telemetry has a named consumer that reads it on the merge
leg."* `[#627]` is untouched — its Done-when is wholly about agy's admission and never mentioned
telemetry, which is what CC's verification found. **No row is filed for finding 8**; it closes when
`[#669]` closes.

**Row 12 → REFUSED as a row.** A5-4, verbatim: *"The 53-line gap is `status: deferred` rows the view
renders and the counter excludes — a population difference by design. M4's counter stands
(`boot_frontier.load_open_rows`, deferred excluded); the intake records the refusal."* So the
divergence is **not** a defect, `[#589]` is not asked to absorb it, and no row is filed. M4's
counter is `boot_frontier.load_open_rows` with deferred excluded. This paragraph is the refusal
record the ruling calls for — the finding is dispositioned, not dropped.
