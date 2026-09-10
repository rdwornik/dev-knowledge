# LANE lane-w-278-impacted-test-selection — A changed file selects the tests that cover it, and a commit that selects none is refused with the RED-first test named.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-w-278-impacted-test-selection LANE-w-278-impacted-test-selection.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #278 · lane-w-278-impacted-test-selection]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-w-278-impacted-test-selection` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-w-278-impacted-test-selection` -> branch `worktree-lane-w-278-impacted-test-selection` -> contract `LANE-w-278-impacted-test-selection.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Sequencing

**Dispatches in the FIRST WAVE.** AMEND-BATCH-W-003 AW3-1 (later than this batch render, and titled *"pre-dispatch: W-7 before W-6"*) **REVERSES** the *"W-7 dispatches after W-6 merges"* line carried verbatim in the frozen body below: *"Both edit `.pre-commit-config.yaml`, so they are serial; W-6 already waits for W-3's merge and W-7 depends on nothing."* The collision is unchanged -- only which lane takes the slot first. The frozen body is carried UNEDITED so the supersession is visible rather than silent.

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-7 · `[#278]` — a changed file selects the tests that cover it, and a commit that selects none is refused (AW2-1)

- **Row.** **`[#278]`** (P2, M, `[E7]` / `[S18]`), `status: deferred` on `main` at render time.
  **AW2-1 un-defers it, verbatim:** *"W-7 = `[#278]` (impacted-test selection), admitted,
  un-deferred."* The lane's first commit flips `status: deferred → open` and strikes the row's own
  DEFER clause — *"DEFER — the 45-day icebox sweep of 2026-08-27"* — because that clause states its
  own un-defer condition and the condition is now met: *"Un-defers when an arc claims the row or the
  operator re-prioritises it."* An arc claims it here. **No flush-left `kill-candidates:` line is
  owed** — the lane adds no task id, it re-opens one.
- **Why this row and not a new one.** The mechanism is ABSENT and the repo says so in its own voice:
  `protocols/PLAYBOOK.md:1100` — *"The general form is *tier A plus anything covering the touched
  module*, which is [#278] (impacted-test selection); until that lands, the named-module rule above is
  its checkable subset."* That is the authority AW2-1 cites, and it names `[#278]` as the row that
  lands it. A second row would split one mechanism across two.
- **Intent (AW2-1, verbatim).** *"(a) a changed file selects the tests that cover it, mechanically;
  lanes run that set in parallel plus tier A; the integrator keeps one full suite per integration as
  the net. (b) A commit that changes a `scripts/*.py` file and selects zero tests is REFUSED, and the
  refusal message names the RED-first test to write — the operator's rule that a process deviation
  raises an exception which teaches the agent."*
- **The implementation is chosen by a NUMBER, and AW2-1 says so verbatim.** *"Implementation is chosen
  by a number, not a preference: FPG-1 `imports` edges (existing organ — a CONNECT) versus an
  established pytest plugin (library-first), decided by measured miss-rate on this batch's own diffs,
  recorded in the lane's receipt."* **Both candidates resolve at render time.** The FPG-1 leg is
  `scripts/file_purpose_graph.py` — `EDGE_IMPORTS = "imports"` (:189), built by INPUT 6 over the `ast`
  call graph (:588). The library leg is a library-first survey, which CLAUDE.md ranks above
  hand-rolling *"on a MEASURED divergence on this repo, recorded so it is not relitigated"*. **The
  lane records the miss-rate for BOTH legs, not only the winner's** — a number that names one
  measurement is a preference wearing a number's clothes.
- **Done-when (verbatim from `[#278]`).** *"both acceptance criteria from
  `docs/intake/archive/2026-07-07-test-suite-hygiene.md` hold with the criterion text quoted in the
  closing commit, and the theatricality review ships as a `docs/audits/` artifact and impacted-test
  selection is live in the verify cadence with a test"*
- **Done-when (NEW — AW2-1, verbatim).** *"a RED-first test fails when the mapping is removed; the
  selector returns a non-empty set for every W-lane diff; the refusal in (b) is proven by a trip-test"*
- **CC render note, not a ruling — the row's Done-when asks for MORE than AW2-1's intent, which is why
  both are quoted above.** AW2-1 binds *"`[#278]`'s own Done-when verbatim, plus NEW"*, and that row's
  Done-when carries two clauses the intent never mentions: **the theatricality review as a
  `docs/audits/` artifact**, and **the two ex-ante acceptance criteria of the archived intake**
  (resolved, `docs/intake/archive/2026-07-07-test-suite-hygiene.md` §*Acceptance criteria (ex-ante)*:
  *"Ship-gate wall-time delta and collected-count delta after cleanup are both measured against a
  **recorded baseline** (recorded before cleanup starts, not reconstructed after)"* and *"The "why did
  it get faster" question is answered with evidence — not a guess — before any cleanup work lands"*).
  The row's own census note narrows the first — *"the theatricality pre-scan was CLEAN fleet-wide, so
  #278 narrows to impacted-test selection + ship wall-time + one parametrize candidate"* — but a
  narrowing written in a row body does not delete a clause of that row's Done-when. **What this lane
  owes:** record the baseline **before it changes anything** (that clause becomes unsatisfiable the
  moment work starts, which is why it is first), and then either ship the theatricality artifact or
  escalate the narrowing as an ask-class (b) rule-vs-ruling conflict. It does not quietly drop a
  clause it was handed verbatim.
- **Closure.** impacted-test selection **absent → live in the verify cadence, with a test** · selector
  implementation **chosen by measured miss-rate, both legs' numbers in the receipt** · a `scripts/*.py`
  commit selecting zero tests **merges → REFUSED, the refusal naming the RED-first test to write** ·
  trip-test for that refusal **absent → present** · RED-first test for the mapping **absent → present,
  and RED when the mapping is removed** · selector over each W-lane diff **non-empty, witnessed
  per lane** · ship-gate wall-time + collected-count **baseline recorded BEFORE any change, deltas
  measured against it** · the archived intake's two criteria **quoted verbatim in the closing commit** ·
  theatricality review **shipped as a `docs/audits/` artifact, or the narrowing escalated**.
- **Anti-patterns.** **Do not delete a test to make a number move** — the archived intake's non-goals
  bind: *"No test deletion without operator review"* and *"No coverage reduction disguised as
  cleanup"*, and core-invariant #3 covers tests like anything else. **Do not reconstruct the
  baseline** — the criterion says *recorded before cleanup starts, not reconstructed after*, and a
  reconstruction is the exact failure it names. **Do not let selection replace the full suite** —
  AW2-1 keeps *"the integrator keeps one full suite per integration as the net"*, which is Ch5's
  tier-B rule (`protocols/PLAYBOOK.md:1070`) and this batch's own refuse-to-finish item 2. **Do not
  hand-roll before measuring the library leg.** **Do not arm the (b) refusal tree-wide on its first
  day** — a gate that refuses every `scripts/*.py` commit wedges the batch it is running inside; prove
  it with the trip-test and name the scope it refuses on.
- **The trap this lane is most likely to hit.** FPG-1's `imports` closure is **transitive over `ast`**
  and the builder **retokenizes per rule** (`scripts/file_purpose_graph.py` :27, :516), so a naive
  "which tests reach this module" query returns a set that grows with depth. **A selector that returns
  the whole corpus satisfies "non-empty for every W-lane diff" and selects nothing.** The non-empty
  leg is a **floor, not the acceptance** — the miss-rate is — and a corpus-wide selector has a
  miss-rate of zero and a value of zero. Measure precision alongside miss-rate, or the number decides
  nothing.
- **MODE: plan.** Basis: a new gate, a new selector organ, and a choice between two implementations
  settled by a measurement the lane has to design first. Not auto.
- **SUBSTRATE: LOCAL — cut at Q2.** Q1 fires *not-cloud* (the result is a gate, and the suite is the
  measurement). **Q2 then fires and stops the cut: the Done-when requires the selector to return a
  non-empty set for every W-lane diff, and W-1, W-2 and W-5's branches are unpushed operator-disk
  state** — Q2 names *"unpushed branches"* in its own text. A container reads `origin`; it cannot read
  a local lane's handed-back branch. **AW-4 therefore does NOT apply here** — there is no codespace
  receipt to re-derive, and the verdict is taken where the work runs.
- **Sequencing — after W-6 merges, and on a real collision rather than caution.** AW2-1 hands the
  check to this render: *"serialize-group collision with W-6 is the dispatcher's check."* **It
  collides.** W-7's leg (b) is a commit-time refusal, so it registers a hook in
  `.pre-commit-config.yaml`; W-6's `phase` writer **may** register one too — A7-1 leaves the hook point
  as W-6's own fork (*"staged in pre-commit, or a follow-up commit on merge"*). G2 serializes on
  **witnessed** footprints, and a fork the dispatcher cannot bind is not a witnessed disjointness.
  **So: W-7 dispatches after W-6 merges.** If W-6 takes the follow-up-commit-on-merge path its
  footprint clears `.pre-commit-config.yaml`, and the integrator may then run them concurrently —
  that is his call on a witnessed footprint, not this contract's on a predicted one.
- **Pointer.** AW2-1 · `[#278]` · `protocols/PLAYBOOK.md:1100` (the mechanism is ABSENT, in the repo's
  own voice) · Ch5 *"Tiered suite — targeted in-lane, one full suite at integration"*
  (`protocols/PLAYBOOK.md:1070`) · `docs/intake/archive/2026-07-07-test-suite-hygiene.md`
  §*Acceptance criteria (ex-ante)* + §*Non-goals* · `scripts/file_purpose_graph.py` (FPG-1,
  `EDGE_IMPORTS` :189, INPUT 6 :588) · `[#528]` (the lane-latency row this one serves; its N1 ADR-110
  amendment is batch X) · ADR-108 §B (RED-first) · CLAUDE.md library-first.
- **Budget: 2.** Which leg wins (the number rules, but **designing** the miss-rate measurement is a
  fork); where the refusal is wired and what scope it refuses on. A third fork = commit-and-STOP with
  a QUESTION file.

---

**Not in batch W.** From DECLARE-SITTING §2, verbatim: L6 (ruled, A4-2) · L3/L4/L5 · the `#680`
mechanism · the Q8 predicate. From DECLARE §1: the R1-3 synthetic-flawed-item mechanism if it is not
already a row · the R1-4 PLAYBOOK Ch8 routing note · the R1-7 LESSONS line. From A6-1 and **A7-2,
which supersedes AW-5 expressly**: **the M03 leg-1a re-run**, which AW-5 had reserved as W-6 and
which goes to batch X on the ground that *it moves no metric* — W-6 is `[#687]` widened per A7-1
instead. From A6-2/A6-3/A6-4: the telemetry delete-or-connect row, the C-4
re-verification row, and the model-agnosticism residue. R1-5 folds into `[#676]`'s invocation-shape
data; R1-6 is an operator account fact and goes to the packet, and `grok` is not ordered until he
answers. A6-5's intake #78 is an operator packet item, not a lane. **From AW2-4 — a teardown, not a lane:**
*"`.claude/worktrees/review-consumption` and branch `docs/review-consumption-2026-09-10` (local and
origin) are removed by the integrator once the session holding it (PID 12628) is closed."* It is the
integrator's act at the queue, and it is an open item on his refuse-to-finish list until it is done.
**`[#278]` has LEFT this list** — AW2-1 admits it as W-7 above.

**Process-lane cap.** Ch8 caps methodology/hub-process lanes at 1/4 of dispatched width. **Batch W is
6/6 process lanes** — a hub-governance batch by construction, every lane targeting hub process, the
deploy corpus or the task spine. The cap is **breached, deliberately and on the record**, and the
packet reports the shortfall rather than the batch pretending otherwise. This is the reporting the cap
asks for when a batch cannot fill its non-process lanes; it is not a waiver. **Width 6 is at the Ch8
ceiling** (4–6, bounded by the integrator's serial capacity), and AW2-2 states where W-7 fits inside
it, verbatim: *"Batch W is at the ADR-110 ceiling: committing lanes W-1, W-2, W-3, W-4, W-6, W-7
(six); W-5 is a primary-session act, not a lane."* **The first render's closing sentence — that batch
W "cannot take a seventh lane without the ADR-110 amendment that N1 assigns to `[#528]` in batch X" —
is SUPERSEDED by AW2-2, and stated as superseded rather than swapped out.** It counted W-5, and W-5
stopped being a lane at AW-3; the ceiling counts **committing lanes**, because what it bounds is the
integrator's serial merge capacity and a primary-session act consumes none of it. **There is no
seventh committing lane: W-7 is the sixth**, and the `[#528]` amendment is still batch X's.

**Row-id ledger, for the manifest.** W-1 files its own (id at filing) · W-2 `[#684]` · W-3 `[#638]` ·
W-4 `[#683]` · W-5 files its own (id at filing) · W-6 `[#687]` · **W-7 `[#278]`, un-deferred by AW2-1
(`status: deferred → open` in the lane's first commit)**. **Every lane has a row at OPEN**, which is
AW-2 satisfied — the first render had two lanes with none. W-7 is the one row that was OPEN-able
rather than open: a deferred row is not an open row, and flipping it is part of the lane's work.

**Nothing here dispatches.** The batch manifest
(`docs/audits/2026-09-10-technical-batch-w-manifest.md`, this file's `carried-by:`) is committed at
DISPATCH, before any lane boots, carrying `status: open` and `closed_by:` — that is what grants the
declared-integration-arc exemption and retires `SKIP=audit-health` on intermediate merges (ADR-110
amendment 2026-08-07). It does not exist yet.

=== END OF CONTRACTS — 7 contracts, 6 committing lanes · W-1 LOCAL · W-2 LOCAL · W-3 CODESPACE · W-4 CODESPACE · W-5 LOCAL (primary session, NOT a lane) · W-6 CODESPACE · W-7 LOCAL ===

## Done-contract (immutable)

**The Done-when and Closure legs are carried VERBATIM in "Frozen intent" below and are this lane's acceptance.** They are not restated here, because a restatement is a paraphrase and the legs are quoted text.

1. Every **Done-when** leg quoted in the frozen body below holds, witnessed.
2. Every **Closure** transition in the frozen body below is carried to its right-hand side.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green via `uv run --locked`.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. **FIRST, before changing anything** -- record the ship-gate wall-time and collected-count baseline. The archived intake's criterion says *recorded before cleanup starts, not reconstructed after*, and the clause becomes unsatisfiable the moment work starts. **COMMIT**
2. Flip `[#278]` `status: deferred -> open` and strike the row's own DEFER clause (its un-defer condition is met: an arc claims it). **No `kill-candidates:` line is owed** -- the lane adds no task id, it re-opens one. **COMMIT**
3. Design the miss-rate measurement, then measure **BOTH** legs on this batch's own diffs -- FPG-1 `imports` edges (`scripts/file_purpose_graph.py`, `EDGE_IMPORTS` :189, INPUT 6 :588) versus an established pytest plugin (library-first). **Measure PRECISION alongside miss-rate**: a corpus-wide selector has a miss-rate of zero and a value of zero. Record both legs' numbers in the receipt. **COMMIT**
4. RED first: the mapping's test fails when the mapping is removed. Build the selector on the leg the NUMBER chose. Witness a non-empty set for every W-lane diff -- a floor, not the acceptance. **COMMIT**
5. Wire leg (b): a commit changing a `scripts/*.py` file and selecting zero tests is REFUSED, the refusal message naming the RED-first test to write. Prove it with a trip-test and **name the scope it refuses on** -- do not arm it tree-wide on its first day or it wedges the batch it runs inside. **COMMIT**
6. Final: quote the archived intake's two ex-ante criteria verbatim in the closing commit; ship the theatricality review as a `docs/audits/` artifact **or escalate the narrowing as an ask-class (b)** -- do not quietly drop a clause handed over verbatim. Selection never replaces the full suite. One end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
