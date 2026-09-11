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
X-DEL    [#734]              lane-x-734-retire-stage             worktree-lane-x-734-retire-stage          sonnet high    execute
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

## 4 · The seat refusals

<!-- Deliberately NOT headed "step 0": `seat_refusals.isolate_step0` takes the FIRST heading
     matching /step\s*0/ and reads only to the next heading, so a second such heading is
     unreachable. The step-0 section is §9, and it ends on its DryRun. -->


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

## 5a · F9 · W-2's worktree was torn down mid-freeze; its branch is UNPUSHED

Measured after the freeze, and it changes W-2′'s step 0. The integrator closed batch W and
removed `.claude/worktrees/lane-w-684-pretooluse-guard-root`. The BRANCH
`worktree-lane-w-684-pretooluse-guard-root` survives, **11 commits ahead of `main`**, and
`git ls-remote --heads origin` returns **nothing for it** — those eleven commits of W-2 review
work exist in exactly ONE place, this clone, with no worktree attached and no remote copy.

AX15-3 is unaffected (it named the branch, and the branch is intact), but W-2′ no longer
"continues in an existing worktree": it **re-attaches** one with
`git worktree add <path> worktree-lane-w-684-pretooluse-guard-root`. The contract was
corrected accordingly in both copies. **A new branch would strand the eleven commits** —
which is why the contract says so in as many words.

**Recommended to the integrator, not done by this seat:** push that branch, so eleven commits
of review work stop being single-copy.

## 5b · The fire GO and its three conditions (AMEND-BATCH-X-ROSTER-017)

The operator's `y` of 2026-09-11 approves all six **with conditions**, each discharged here:

- **AX17-1 · Backup before re-attach — DONE.**
  `git push origin worktree-lane-w-684-pretooluse-guard-root` → `[new branch]`, verified by
  `git ls-remote`: `90c727bd... refs/heads/worktree-lane-w-684-pretooluse-guard-root`. Both
  pre-push gates (`block-ff-push`, `block-unanchored-push`) Passed. A lane-branch backup,
  **never a merge to `main`**. F9's single-copy risk is discharged.
- **AX17-2 · X-DEL footprint bounded, and the lane runs at `sonnet` — DONE.** The contract
  gained a "GO footprint" section naming the four in-scope surfaces per target and nothing
  beyond, plus the rule that a silent `safe_remove`/oracle result is INCONCLUSIVE → KEEP with
  that reason. Routing row changed `opus` → `sonnet`.
  **This lane is the live instance of `[#717]`:** its fence carries no `-Model` and
  `Start-DispatchLane` defaults to `opus`, so dispatched by its own carried line it would run
  at opus and nothing would warn. `-Model sonnet` is therefore passed explicitly at the
  dispatch act, and the receipt in §12 is the proof.
- **AX17-3 · Manifest first — INTEGRATOR'S ACT, flagged not done.** This branch
  (`worktree-dispatch-x1-freeze`) must merge before any X1 lane hands back, so batch X lands
  anchored. The dispatcher cannot merge (integration is LOCAL and INTERACTIVE, and this seat
  is a background job).
- **AX17-4 · The F8 finding becomes a row** via the first backfill slot — not this seat's act,
  recorded so it is not lost: one fence, one verb, RED-first that a generated contract
  launches through the ruled verb.

## 6 · Wait conditions — the batch does not fire while either is open

1. **X-0 on `main`** — **MET.** `b595545b`, anchored by `2177f14a`. Batch W has since closed
   too; `main` is `78d99d55`.
2. **`lane-ceiling` PASSES** — **MET.**
   `lane-ceiling: PASS -- 6 lane(s) <= 6, checked before any worktree exists`, run against all
   six slugs with `--check-worktrees`. Zero worktrees are provisioned: the integrator tore
   down every lane worktree, and this seat tore down its own dispatcher worktree and verified
   the removal (the provision→cleanup round-trip left the tree identical, critical rule 9).
3. **The operator's `y`** — **OPEN. This is the only thing left.** Asked per fire (§7).

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

## 9 · Step 0 ends here — the DryRun of every generated contract

The LAST line of step 0 (AMEND-BATCH-V-002 §1), covering **every** generated contract —
the one left out is the one that fails at dispatch. Batch V froze six contracts the live
verb refused and found out by running this.

```
dispatch LANE-x-692-decision-coverage.md -DryRun
dispatch LANE-x-689-conductor-e.md -DryRun
dispatch LANE-x-664-delivery-spine.md -DryRun
dispatch LANE-x-734-retire-stage.md -DryRun
dispatch LANE-x-716-dispatch-defects.md -DryRun
dispatch LANE-w-684-pretooluse-guard-root-prime.md -DryRun
```

## 10 · DryRun receipts

**`dispatch <FILE> -DryRun` REFUSED all six** — see F8. The DryRun was then run through the
verb the fence actually names, `Dispatch-Lane … -DryRun`, which resolved every line:

```
lane-x-692-decision-coverage
  claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-692-decision-coverage <prompt>
lane-x-689-conductor-e
  claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-689-conductor-e <prompt>
lane-x-664-delivery-spine
  claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-664-delivery-spine <prompt>
lane-x-734-retire-stage
  claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-734-retire-stage <prompt>
lane-x-716-dispatch-defects
  claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-716-dispatch-defects <prompt>
W-2' (interactive shape — inherits its worktree, so no Dispatch-Lane line exists to DryRun)
  cwd .claude/worktrees/lane-w-684-pretooluse-guard-root
  claude --bg --model opus --effort high --permission-mode bypassPermissions
```

**AX7-3 is satisfied at the dispatch act:** every resolved line carries `--model opus`
explicitly. Contract-declared model and dispatched model AGREE for all six — verified by
receipt, not asserted.

## 11 · F8 · The two contract gates are MUTUALLY EXCLUSIVE

Measured while DryRunning this batch, and the sharpest finding of the freeze:

- `gen_lane_contract.py check` **requires** the `## Dispatch` fence to be
  `Dispatch-Lane <slug> <file> [-Effort <v>]` (`_DISPATCH_LINE_RE`, line 227), and refuses a
  contract without it: *"no dispatch command line found"*.
- `dispatch` → `Invoke-Dispatch.ps1:285` **refuses** that exact fence: *"the contract's
  `## Dispatch` block must invoke `claude`, not `Dispatch-Lane` — this script never runs an
  arbitrary command from a contract file."*

**No contract can satisfy both.** A generator-emitted contract passes the repo's gate and is
categorically unlaunchable by the ruled verb; a contract the ruled verb accepts fails the gate.
This is not a preference between verbs — it is the same "two independently-correct literals"
class `[#718]` generalises, one seam further out, and `Invoke-Dispatch`'s refusal is *correct*
security behaviour (it will not execute arbitrary commands from a file), so the fix belongs on
the generator/gate side.

Batch W recorded half of this (its F2: `dispatch` refuses a non-`claude` fence). The other
half — that the gate MANDATES the fence `dispatch` refuses — is new here, and it means the
defect cannot be worked around by rewriting a contract: it is structural.

**Consequence for this batch:** the fire path is `Dispatch-Lane … -Model opus`, not
`dispatch … -Run`. `Dispatch-Lane` offers no confirmation prompt at all (it fires
immediately), so AX14-3's "non-interactive confirmation" branch has nothing to use and the
dispatcher **asks the operator `y` per fire** — which is what the operator asked for
independently. Recorded as a candidate row: *"the contract gate and the dispatch verb demand
incompatible fences."*

## 11a · X1-4 FROZEN (not fired) — the routing lane, carrying AX21 + AX22

Frozen ahead of its backfill slot so that when it fires it already carries the role→model
ruling. **Not dispatched**: it is a backfill item, and AX22-4 gates half its work.

```
slot   rows            slug                            branch                                model  effort  mode
X1-4   [#691] [#694]   lane-x-691-routing-telemetry    worktree-lane-x-691-routing-telemetry opus   high    execute
```

`opus` because AX21-1 makes **orchestrate/plan Opus-only**, and a lane that builds the router
is orchestrating routing. That is the one row of the role table not subject to re-ranking.

**Carried verbatim** (extracted, not retyped): rows `[#691]` and `[#694]`; clauses
`AX21-1` `AX21-2` `AX21-3` `AX21-4` `AX22-1` `AX22-2` `AX22-4` `AX22-5` `AX4-1` `AX9-4`.
Contract passes the gate at 11 sections. **DryRun receipt** (not fired):

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-691-routing-telemetry
```

The contract states, where the lane cannot miss them:

- **Two FIRST ACTS** — read the grok account's usage-limit cause (AX21-4; if it is a spending
  cap that is the operator's act, one line in the report), and **verify grok's token-ceiling
  flag** (AX21-3 applying R1-4(b)/A7-5: *a CLI that cannot enforce a token ceiling by flag is
  not ordered*), on this version rather than from docs.
- **Fixed order of work** (AX22-5): telemetry → registry → router → re-rank. Each step is the
  next one's evidence; a router re-ranked on nothing measured is a fixed list wearing a
  router's name.
- **Admission before position** (AX22-1): implement order is **Sonnet first** until admission;
  Grok 4.6 and Copilot Enterprise take bounded trial tasks in parallel; **≥ 8 of 10 green on
  first review** admits, below it the provider ranks last and the anomaly is filed. Copilot →
  Grok → Sonnet is the *expected* steady state, **earned, not declared**.
- **Reviewer ≠ producer, encoded in the registry** (AX22-2), with the tally recording both roles.
- **`providers.allowed` per repo in the deploy manifest**, and the router REFUSES an off-list
  provider — RED-first (AX22-5).
- **PRECONDITION (AX22-4):** no non-Claude producer or reader is ordered before W-2′ is on
  `main`. At freeze W-2′ was RUNNING, not merged. The Claude-side build is ungated; ordering a
  non-Claude provider is gated, and the lane **reports and stops** rather than deciding the
  precondition is close enough. The contract gives it the check to run.

## 11b · Seat models recorded in the renders (AX22-3)

`gen_seat_boot.py` carried **no model concept at all** — the ruling had nowhere to live. Added
`SEAT_MODELS` and a `model:` field in the render header, **RED-first**: three tests written and
failing (`AttributeError: no attribute 'SEAT_MODELS'`) before the code existed; suite now
**28 passed**.

```
dispatcher sonnet     integrator opusplan     filings/handoff/lane opus
```

`model:` sits between `date:` and `ch8-sha256:` because `_HEADER_RE` stops at the pipe after
`date` — the field is additive and no existing reader changes. The remaining three seats are
stated rather than defaulted, so adding a seat to the enum without deciding its tier fails a
test instead of rendering an unresolved one.

**The five refreshed renders were copied to the transport `to-browser/` (AX11-2)** and carry
the ruled models.

**P12 now reports DRIFT against the 2026-09-10 bundle, BY CONSTRUCTION, and that is correct.**
A fresh render carries `model:`; that frozen bundle predates the ruling and does not.
**Handoff bundles are immutable (critical rule 3), so it was NOT regenerated** — the drift is
the immutability rule and the new field meeting, not a defect. P12 is wired into no gate
(absent from `.pre-commit-config.yaml`), so nothing is blocked. The next bundle cut renders
with the field and P12 passes against it. Stated here so the next seat reads a known
consequence rather than discovering an alarming one.

## 12 · FIRE RECEIPTS — all six up

Fired on the operator's `y` of 2026-09-11 with AMEND-017's three conditions, in the ruled
order. Every lane confirmed up by its branch appearing, not by the receipt alone.

```
order  slot     receipt    model   branch up   worktree
1      X1-1     a61224fd   opus    8s          lane-x-692-decision-coverage
2      X1-2     e5cdeb9d   opus    8s          lane-x-689-conductor-e
3      X-DEL    c0645d40   sonnet  8s          lane-x-734-retire-stage
4      lane-5   a7e74d55   opus    12s         lane-x-716-dispatch-defects
5      W-2'     fed4c445   opus    n/a         lane-w-684-pretooluse-guard-root (RE-ATTACHED at 90c727bd, 11 commits)
6      X1-5     98b61963   opus    11s         lane-x-664-delivery-spine       (fired LAST, per its row)
```

**X-DEL's receipt reads `model=sonnet`** — the condition held. This lane is the live `[#717]`
instance: its fence carries no `-Model` and `Start-DispatchLane` defaults to `opus`, so
dispatched by its own carried line it would have run at opus and nothing would have warned.
The explicit flag is what made the declared model true.

**W-2′ took the re-attach path** (§5a): `git worktree add <path>
worktree-lane-w-684-pretooluse-guard-root` onto the EXISTING branch, `state.yaml` seeded
(gitignored, so `git worktree add` does not carry it), then a `--bg` session with its cwd
there. No verb can do this — F2.

### Lane bases are SPLIT, which is `[[#716]]` in the open

```
0be08b3c : X1-1, X1-2          (fired after the integrator's anchor merge)
78d99d55 : X-DEL, lane-5, X1-5 (fired before it)
90c727bd : W-2'                (its own branch, 11 ahead)
```

Three different bases across one batch, because `worktree.baseRef` is unset and lanes branch
from `origin/main` as it stood at their own fire moment — while `main` moved twice during the
fire. **Every contract carries the mandatory step-0 sync**, which is precisely what absorbs
this; `[#716]` is the row that ends it, and it is lane-5's work.

### F10 · The hand-composed W-2′ launch was TRUNCATED — dispatcher error, verified by transcript

**What happened.** W-2′ is the one lane no verb could start (F2), so its launch line was
composed by hand and carried the **literal expanded path** `H:\My Drive\CLAUDE PROMPT DIR\…`.
It split at the space in `My Drive`. The lane received exactly:

```
Read H:\My
```

ten characters. The quoting used — inner double quotes inside a single-quoted PowerShell
string — did not survive the hand-off to `claude`. The operator caught it and relayed the
full instruction; W-2′ recovered and is working.

**The other five were VERIFIED, not assumed.** Read off each lane's own transcript
(`~/.claude/projects/**/<session>.jsonl`, first user message):

```
X1-1   a61224fd  len=101  Read and execute the frozen contract at …\LANE-x-692-decision-coverage.md
X1-2   e5cdeb9d  len=95   … \LANE-x-689-conductor-e.md
X-DEL  c0645d40  len=96   … \LANE-x-734-retire-stage.md
lane5  a7e74d55  len=100  … \LANE-x-716-dispatch-defects.md
X1-5   98b61963  len=98   … \LANE-x-664-delivery-spine.md
W-2'   fed4c445  len=10   Read H:\My                      <-- the only truncation
```

**The truncation is isolated to the hand-composed launch.** `Dispatch-Lane` quotes its own
prompt correctly; every lane it started received the whole instruction naming its own
contract. The defect is the dispatcher's, not the verb's.

**Standing rule from here (operator, AMEND-018):** every prompt names
`$env:CLAUDE_PROMPTS_DIR`, never the literal path. **Note for whoever implements it:**
`Dispatch-Lane` composes `Read and execute the frozen contract at <EXPANDED PATH>` itself, so
the rule is not satisfied by dispatcher discipline alone — the helper's prompt composition has
to change too. That sits squarely in the lane already running as lane-5 (`[#717]`/`[#718]`,
the writer/reader-one-key work), which is the right place for it.

### Not done by this seat, and owed

- **The integrator merges `worktree-dispatch-x1-freeze`** — AX17-3. (Done at `e688669c`,
  anchored at `0be08b3c`; this final receipts commit is a second, smaller merge.)
- **AX17-4's row** — one fence, one verb — files through the first backfill slot.
- **The dispatcher worktree** is torn down and its removal verified once this commits.

---

**Last updated:** 2026-09-11 · **Seat:** dispatcher · **ALL SIX FIRED.**
