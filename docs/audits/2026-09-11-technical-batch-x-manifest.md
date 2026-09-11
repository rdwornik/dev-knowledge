# Batch X — manifest (dispatch half) · 2026-09-11

**Seat:** dispatcher · **Batch:** X, wave 1, first set · **Ceiling:** ADR-110, six lanes
**Base at freeze:** `main` = `2177f14a` (X-0 merged); re-based to `78d99d55` at commit time,
after the integrator landed the batch W close packet under this seat.
**Status:** **SIX CONTRACTS FROZEN. NOTHING FIRED.** Held at the two wait conditions in §6.

**Consumers:** intake #93 · `[#692]` · `[#689]` · `[#664]` · `[#727]` · `[#734]` · `[#716]` ·
`[#717]` · `[#718]` · `[#684]` — this manifest is the dispatch-half record for those rows'
lanes, and every contract in
`docs/audits/2026-09-11-technical-batch-x-launch-contracts/` is linked from §2 above.

---

## 1 · The GO, recorded

This section IS the GO record. The operator's paste of 2026-09-11 is reproduced as the
authority for every lane below; `to-browser/RATIFICATION-2026-09-11.md` is its ratification
file, and `AMEND-BATCH-X-ROSTER-014` / `-015` amend its scope.

> **GO (operator) for batch X wave 1, first set, and for the deletion lane — this paste is
> the GO record; write it into the manifest.** Freeze today, not tomorrow (supersedes
> AX12-3's timing). Render from rows on `worktree-lane-x-000-batch-x-roster-lands`
> (tip `86a4cbe0`) per `to-cc/DECLARE-BATCH-X-ROSTER-2026-09-11.md` with AMEND-001…013
> applied; each contract carries its row's Done-when plus every AX clause addressed to it,
> verbatim (AX12-1).

> **Capacity update** per `AMEND-BATCH-X-ROSTER-014.md`: fill to the ceiling of 6 — add lane 5
> (dispatch defects `[#716]` `[#717]` `[#718]`, one lane, RED-first per defect) and lane 6.
> Then run a rolling backfill within the roster (AX14-2). Fire confirmation per AX14-3.

> **Slot 6 correction** per `AMEND-BATCH-X-ROSTER-015.md` AX15-3: slot 6 is **lane W-2′**
> (guard fails closed and loud; continues on the W-2 branch).

> **Timing correction:** no overnight bound — the operator lifted it. Fire as soon as X-0 is
> on `main` and the lane ceiling passes, on the operator's `y`; substrate by Ch8 Q1–Q4 alone.

**Scope bound (AX14-3):** the GO covers every roster lane and **no lane outside the roster
fires on it**.

**Superseded by this GO:** AX12-3's "tomorrow" freeze timing, and AX11-1 / AX14-1's
overnight-only substrate bound. Both are recorded as superseded rather than deleted.

## 2 · The six lanes

Row ids are the authority, not the `X1-N` labels: the operator's numbering (AX14-2 —
"X1-3 merge cost (after X1-2)") differs from `DECLARE-BATCH-X-ROSTER`'s table, where X1-2 was
merge cost and X1-3 conductor E. The rows disambiguate; the labels do not.

```
slot     row(s)              slug                                branch                                    model  effort  mode
X1-1     [#692]              lane-x-692-decision-coverage        worktree-lane-x-692-decision-coverage     opus   high    execute
X1-2     [#689]              lane-x-689-conductor-e              worktree-lane-x-689-conductor-e           opus   high    execute
X1-5     [#664] + [#727]     lane-x-664-delivery-spine           worktree-lane-x-664-delivery-spine        opus   high    plan
X-DEL    [#734]              lane-x-734-retire-stage             worktree-lane-x-734-retire-stage          opus   high    execute
lane-5   [#716][#717][#718]  lane-x-716-dispatch-defects         worktree-lane-x-716-dispatch-defects      opus   high    execute
W-2'     [#684]              lane-w-684-pretooluse-guard-root    (INHERITED — already exists)              opus   high    execute
```

Contracts are frozen at the prompts-dir **root** (where the verb reads — `[#718]`) and carried
in-tree at `docs/audits/2026-09-11-technical-batch-x-launch-contracts/`. All six pass
`gen_lane_contract.py check` (8 sections; X-DEL 9).

### Sequencing — from the rows, not composed

- **`[#692]` precedes `[#689]`.** A9-1 says `decision_coverage` is "batch X lane 0 (before
  conductor E)", and `[#689]` is one of the decisions the query must be able to see. Building
  the query after its first subject would leave it unwitnessed.
- **`[#664]` MERGES LAST in its batch** — its own row says so. Mode `plan`, decision budget 2,
  terra pre-merge.
- **`[#689]` is BLOCKED on GitHub Pro (D2)**, which lives ONLY in
  `to-browser/RATIFICATION-2026-09-10 (1).md` (1,097 B). The same-named 4,332 B file lists
  GitHub Pro under **NOT RATIFIED**. The contract tells the lane to READ it, never infer it.
- **W-2′ inherits its branch** and is therefore not started by `Dispatch-Lane` (§5).

### `[#727]` folded into X1-5 — the dispatcher's call, as the row asks

`[#727]` leaves its placement to "the dispatcher's call on serialize-groups". Derived, not
guessed: `gen_task_tree.derive_serialize_group` returns `None` for `[#664]` **and** `[#727]`
(and for 692, 689, 721), so the disjointness rule in `boot_frontier` binds nothing here — the
operator's "if serialize-groups allow" is satisfied, vacuously but checkably. The two are also
file-disjoint: `[#727]` touches `.claude/settings.json` plus a new hook and test; `[#664]`
touches the graph organs and `.pre-commit-config.yaml`. Folding keeps the set at six and puts
the pointer (`graph_queries.py why|process-list`) in the same lane as the organs it points at.

## 3 · Carriage — AX12-1, mechanically

Each contract carries its row's Done-when verbatim plus every AX clause addressed to it,
quoted with its AX id. **Both were EXTRACTED from source files, never retyped** — a
transcribed "verbatim" quote is a claim; an extracted one is the text. The extractor fails
loud on any row or clause it cannot find, so a silently-dropped clause (the "stays SAID"
failure AX12-1 exists to end) is not expressible.

```
slot     AX clauses carried
X1-1     AX4-1  AX9-4  AX8-4  AX10-3  AX12-1  AX13-1
X1-2     AX4-1  AX9-4  AX3-2  AX12-2
X1-5     AX4-1  AX9-4  AX9-1  AX3-7
X-DEL    AX4-1  AX11-3 AX12-1 AX13-2  AX13-3  AX13-4  AX13-5
lane-5   AX4-1  AX9-4  AX7-3  AX7-5   AX14-1
W-2'     AX4-1  AX9-4  AX15-1 AX15-2  AX15-3
```

AX4-1 (floor declaration mandatory) binds every lane contract; AX9-4 (exists-before-build)
binds every lane that CREATES an organ — X-DEL deletes, so it carries AX4-1 without AX9-4.
Each lane's FIRST COMMIT writes its carried clauses into its own row; a lane does not edit a
row it did not file, and reports the untouched one instead.

## 4 · STEP 0 — the refusals

```
carried-by      PASS  20/20 on the POSITIVE population (batch X decision files only, per
                      AMEND-SESSION-PLAN-005 A5-1). DECLARE-BATCH-V-CLOSE (closed batch) and
                      AMEND-CV-V10-001 (another workstream) are OUT OF POPULATION by the
                      operator's scoping, not waived.
lane-ceiling    HELD  6 lanes planned; W-2' inherits an existing worktree, so 5 are provisioned
                      by this batch. The check REFUSES while any worktree is open and is re-run
                      as the last act before firing (§6).
dryrun-step0    PENDING — the LAST line of step 0, run against all six once the ceiling passes.
sleeping-poll   PASS  0 declared waits.
```

## 5 · Findings — measured while freezing, not inherited

- **F1 · `[#717]`'s fix must widen the CHECKER, not only the generator.**
  `_DISPATCH_LINE_RE` (`scripts/gen_lane_contract.py:227`) is
  `^Dispatch-Lane <slug> <file>( -Effort <v>)?\s*$` — anchored, with **no `-Model`
  alternative**. Adding `-Model opus` to the fence made all six contracts fail with "no
  dispatch command line found". So AX7-3's "explicit `-Model` on every line" is currently
  **unsatisfiable in the fence**, and rendering the model without widening this regex turns
  every contract RED. Recorded in lane-5's contract as part of `[#717]`'s Done-contract.
  **Resolution here:** the fence keeps the gate-admitted grammar; the explicit-model form is
  carried beside it as the line actually run. All six lanes declare `opus` and
  `Start-DispatchLane`'s `-Model` defaults to `opus`, so declared and dispatched models agree
  by construction for this batch — the DryRun receipt is the evidence, not this sentence.
- **F2 · The verb set has NO resume mode.** AX15-3 rules W-2′ "continues on the W-2 branch",
  but `Dispatch-Lane`/`Start-DispatchLane` **refuse when the branch exists** — correct
  behaviour (a re-run must be a no-op), so it cannot be argued around. W-2′ therefore uses the
  gate's `interactive` form and is started as a `--bg` session with cwd set to the existing
  worktree. Worth a row: "a lane cannot be resumed by any dispatch verb."
- **F3 · X-DEL is not ten file deletions.** Each of the eight modules is coupled to up to
  three further surfaces — its dedicated test, its `Disposition` entry in
  `scripts/graph_queries.py`, and its entry in the `tests/test_graph_spine.py` list — and two
  are internal PAIRS (`boundary_headers`→`boundary_report`,
  `desired_state_report`→`desired_state_loader`). Deleting a module alone REDs the suite. The
  table is in X-DEL's contract.
- **F4 · `safe_remove.py` produced NO OUTPUT** over the eight modules in the dispatcher's
  pre-run (>120 s, then nothing). Silence is **not** clearance. The contract tells the lane to
  re-run it and treat empty output as inconclusive. Conversely a name-grep is not evidence
  either: the dispatcher's sweep returned hundreds of "referrers" per target, almost entirely
  prose. Neither instrument cleared anything.
- **F5 · The eight modules ARE already dispositioned orphans** in `graph_queries.py`
  (`owner="V+1 retirement-or-wiring list"`, reasons "documented, never wired" / "a test is not
  a trigger"). The census verdict is corroborated by the graph organ — which is what makes the
  delete list credible, and is the strongest evidence in this batch.
- **F6 · A concurrent seat moved `main` three times mid-freeze** (`14772c6e` → `b595545b` →
  `2177f14a`) and tore down two worktrees. Every premise here was re-derived after the last
  move; the freeze base is stated at the top so a later reader can tell what it was built on.
- **F7 · The dispatcher overwrote batch W's `LANE-w-684-pretooluse-guard-root.md` in the
  transport** with `--force` while generating, and **restored it byte-exactly (8,579 B)** from
  the in-tree frozen copy on `main`. W-2′ was then given its own filename, which is correct
  independently: a correction re-enters as a NEW contract, never as an edit of a frozen one.

## 6 · Wait conditions — the batch does not fire while either is open

1. **X-0 on `main`** — **MET.** `b595545b`, anchored by `2177f14a`.
2. **`lane-ceiling` PASSES** — **OPEN.** It refuses while any worktree is provisioned. One
   remains: `lane-w-684-pretooluse-guard-root` (11 commits ahead, unmerged). W-2′ inherits it
   by design, so the integrator's merge-and-teardown of the OTHER lanes is what clears this.
3. **The operator's `y`** — per AX14-3, and the fire method is `-Run` (§7).

## 7 · Fire method — AX14-3, resolved against the installed verb

`dispatch.ps1` exposes **`-Run`**: "Execute immediately, skipping the interactive confirm."
So the verb DOES offer a non-interactive confirmation and the dispatcher uses it, recording
the GO reference per fire:

```
dispatch <CONTRACT>.md -Run          # cites to-browser/RATIFICATION-2026-09-11.md
```

W-2′ is the exception (§5 F2): a `--bg` session with cwd set to the existing worktree, given
its contract's `Read … and execute it exactly.` line.

## 8 · Rolling backfill — AX14-2

On every merge + teardown, the next roster item whose dependencies are on `main` fires, never
exceeding six. Queue, in order, each recorded here when it fires:

```
X1-3  merge cost [#675]        after X1-2
X1-6  task keys  [#687]        after X1-5
X2 head, in order: docs-cut manifest step (cut ONLY on the operator's GO) · prompt-distiller
trace home · logs lane (+ log-review routine) · test-baseline debt
```

**Backfill log:** (empty — nothing has fired.)

---

**Last updated:** 2026-09-11 · **Seat:** dispatcher · **Nothing fired.**
