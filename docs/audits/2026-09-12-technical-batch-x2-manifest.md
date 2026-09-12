# Batch X wave 2 — manifest (dispatch half) · 2026-09-12

**Seat:** dispatcher · **Batch:** X, wave 2 · **Ceiling:** ADR-110, six lanes
**Base at freeze:** `main` = `9136f133` (the x-691 merge plus the five AX24-5 closures).
**Status:** **THREE CONTRACTS FROZEN. NOTHING FIRED.** Held at the wait condition in §5.

**Consumers:** `[#727]` · `[#675]` · `[#734]` — this manifest is the dispatch-half record for
those rows' lanes, and every contract named in §2 lives in
`docs/audits/2026-09-12-technical-batch-x2-launch-contracts/`.

---

## 1 · The GO, recorded

This section IS the GO record. The operator's message of 2026-09-12 is reproduced as the
authority for every lane below.

> Confirmed: F1 and F2 are contract preconditions, and each rides its own lane's first commit —
> no separate lane. (F1) `[#727]`'s Done-when is amended to carry the fail-posture: the
> deny-and-point hook refuses its matched class when it cannot evaluate (script missing,
> interpreter missing, crash, unexpected rc), each refusal naming cause and fix, with a RED-first
> trip-test per failure mode; the three allow-on-failure paths are the lane's target and the
> declared `# raw-needed` escape stays; `[#727]` does not close until that clause is green.
> (F2) `[#675]`'s Done-when replaces the stale 12->2 target with the measured baseline — 84 min
> wall = 11.3 targeted tests + 72.7 residual ceremony (itemised views ~90 and ~63, nothing
> measured today) — and the target becomes: per-step minutes recorded into the receipt, full
> suite and index regeneration on GitHub Actions with the integrator reading the result, Codex
> reviews in parallel, the dispatcher refusing to fire two lanes whose contracts touch the same
> file (RED-first), review and triage handed pre-assembled inputs and NOT cut, median merge under
> 30 minutes measured. Freeze the three wave-2 contracts (x2-727-fail-closed at `-Model sonnet`,
> x2-675-merge-cost, x2-del-second-attempt rewritten from the x-734 verdict record on main at
> `f1711e3d` including the release_lint change that lets a `status: removed` tombstone land), run
> dryrun-step0 across all three, and WAIT: fire only once the integrator has pushed the x-691
> merge and torn its worktree down. Also file as rows: lane-ceiling `--check-worktrees` refuses
> on worktree PRESENCE with no merged/unmerged discrimination, and session_end_backpressure
> ordered a commit of another seat's in-flight work — both are the same absent-discriminator
> class as `[#675]`.

**Scope bound:** the GO covers these three lanes and no lane outside them fires on it.

## 2 · The three lanes

Order is AX24-1's, and it is the firing order:

```
slot  row     slug                        model   effort  contract
1     #727    lane-x-727-fail-closed      sonnet  high    LANE-x-727-fail-closed.md
2     #675    lane-x-675-merge-cost       opus    high    LANE-x-675-merge-cost.md
3     #734    lane-x-734-retire-stage-2   opus    high    LANE-x-734-retire-stage-2.md
```

`sonnet` on slot 1 is an operator ruling, not a lane default, and is recorded in that contract's
Dispatch section so the lane does not re-escalate it. The model is ON each dispatch line —
`[#717]`, closed at `9136f133`, is what makes that true by construction rather than by care.

## 3 · STEP 0 refusals

| check | result |
|---|---|
| `lane-ceiling` (count leg) | **PASS** — 3 lanes ≤ 6 |
| `lane-ceiling --check-worktrees` | **REFUSED on placement** — see §6; filed as `[#738]` |
| `carried-by` | 1 refusal, on a pre-existing batch-V declare, nothing this seat authored |
| `sleeping-poll` | **PASS** — 0 declared waits |
| `dryrun-step0` | run across all three contracts — the lines below |

**The LAST line of step 0 — one `-DryRun` per generated contract, and nothing after**
(AMEND-BATCH-V-002 §1). The one contract left out is the one that fails at dispatch; batch V
froze six contracts the live verb refused and found out by running exactly this:

```
dispatch LANE-x-727-fail-closed.md -DryRun
dispatch LANE-x-675-merge-cost.md -DryRun
dispatch LANE-x-734-retire-stage-2.md -DryRun
```

## 4 · Dry-run receipts

`seat_refusals.py dryrun-step0` over all three: **PASS — 3 contract(s) DryRun on the last line of
step 0.** The live-verb dry runs, verbatim:

```
[lane] slug=lane-x-727-fail-closed branch=worktree-lane-x-727-fail-closed model=sonnet effort=high permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-x-727-fail-closed <prompt>

[lane] slug=lane-x-675-merge-cost branch=worktree-lane-x-675-merge-cost model=opus effort=high permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-675-merge-cost <prompt>

[lane] slug=lane-x-734-retire-stage-2 branch=worktree-lane-x-734-retire-stage-2 model=opus effort=high permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-734-retire-stage-2 <prompt>
```

Every contract is covered — AMEND-BATCH-V-002 §1's requirement, and the check batch V discovered
by freezing six contracts the live verb refused. **Nothing was provisioned:** `git worktree list`
and `git branch --list 'worktree-lane-x-{727,675,734}*'` are both empty of these three after the
runs. `sonnet` on slot 1 appears on the resolved line, which is the `[#717]` guarantee holding.

**Two defects surfaced by running this rather than trusting it — neither blocks the freeze:**

1. **`dispatch <FILE> -DryRun` REFUSES every one of these contracts**, on grammar, not on path:
   *"Refusing: the contract's `## Dispatch` block must invoke 'claude', not 'Dispatch-Lane' —
   this script never runs an arbitrary command from a contract file"*
   (`Invoke-Dispatch.ps1:285`). The generator emits a `Dispatch-Lane` fence; the `dispatch` verb
   admits only a `claude` fence. **`[#718]` did NOT close this** — it closed the *location* seam
   (writer and reader resolving from one key, witness
   `test_emit_writes_the_contract_where_the_dispatch_line_it_prints_will_be_read`). The
   *grammar* seam is still open, and the boot's own §2 `dryrun-step0` block tells a seat to run
   the verb that refuses. The receipts above were taken with `Dispatch-Lane … -DryRun`, the
   fallback the boot's §4 names, which is what the contracts actually carry.
2. **Every `-DryRun` exits 1** while printing a correct resolution. Consistent across all three,
   so it is the verb's dry-run convention rather than a per-contract failure — but a non-zero
   exit on a successful dry run is indistinguishable from a real refusal to any caller that
   checks exit codes, which is every gate that might one day wrap it.

## 5 · The wait condition — this batch does NOT fire on this manifest alone

**Fire only once the integrator has (a) PUSHED the x-691 merge and (b) TORN DOWN its worktree.**
Operator instruction, 2026-09-12.

**Both conditions went TRUE during this freeze, and the transition is stamped rather than
smoothed over.** At boot: `main` = `cec75ebc`, x-691 unmerged, its worktree live and locked. At
freeze close: `origin/main` = `9136f133` = local `main` (**(a) satisfied — pushed**), and
`git worktree list` no longer carries `lane-x-691-routing-half-a` (**(b) satisfied — torn down**).
The integrator did both mid-session; none of it is this seat's work.

**This seat still did not fire, and the reason is mechanical rather than cautious.** The dispatch
surface refuses to fire bare by design — with neither `-DryRun` nor `-Run` it asks the operator to
confirm, and *"anything but `y`/`yes` — including empty or non-interactive input — refuses"*
(Ch8, "Row 1 — LOCAL background lane"). A background seat cannot supply an interactive `y`, and
the only way past is `-Run`, which **bypasses the operator's own confirmation gate**. Forcing that
to satisfy a wait condition would defeat the gate the condition exists to reach. So the batch is
armed and held at the operator's `y`.

This is not a soft sequencing preference. It is AX24-1's "no new X2 lane until the finished work
is banked", and the `lane-ceiling` placement refusal in §6 is mechanically unclearable until (b)
happens.

## 6 · Two findings filed as rows, per the GO

- **`[#738]`** — `lane-ceiling --check-worktrees` refuses on worktree PRESENCE with no
  merged/unmerged discrimination; the offered remedy (teardown) would have destroyed seven
  commits of unmerged work.
- **`[#739]`** — `session_end_backpressure` ordered this seat to commit or stash six files that
  were the integrator's in-flight AX24-5 closures.

- **`[#740]`** — the generator emits a `Dispatch-Lane` fence and the ruled verb admits only a
  `claude` fence, so `dispatch -DryRun` refuses every conforming generated contract. Filed on the
  operator's instruction after §4's dry runs surfaced it. **`[#718]` was satisfied on the PATH
  key; the fence mismatch was never in its scope** — two independent seams on one writer/reader
  boundary, distinguishable only by which line refuses (`Invoke-Dispatch.ps1:385` path,
  `:285` fence). **Re-scoped the same day by AX25-1 to a SYMPTOM record** — it proposes no fix and
  closes when `[#675]`'s clause-1 conformance test is green.
- **`[#741]`** — AX25-3: lane launching is methodology, so the hub owns it as a floor component,
  OS-independent, machine-local values staying in `win-tooling`. **Scope is set by the fact-read,
  not by this seat's inference** — the row deliberately enumerates no verbs or dependencies, and
  says why. Executed **after** `[#675]`.

### 6a · AX25 changed this batch's shape mid-freeze, and slot 2 absorbed it

`to-cc/AMEND-BATCH-X-ROSTER-025.md` names the root cause the four dispatch symptoms share:
**the lane-launch path has two owners and no conformance test between them.** Consequences for
this manifest, all already applied:

- **`LANE-x-675-merge-cost.md` gained AX25-2 as clause 1** — the generator↔verb conformance test,
  RED-first, in the hub, asserting **fence + contract location + model + base in ONE assertion**,
  with a refusal leg: a commit that changes either side and leaves it red is refused. **No
  separate lane** (AX25-2's own words). The measured-baseline clause and the six targets shifted
  to clauses 2 and 3; nothing was dropped.
- **The batch is still three lanes.** AX25-2 rides slot 2 and AX25-3 is a filed row executed after
  it, so the `lane-ceiling` count leg in §3 is unchanged at 3 ≤ 6.
- **AX25-4 bounds the fix:** the PowerShell dispatch retires once one batch runs on conductor E,
  so slot 2's verb work is limited to the conformance test plus whatever E's runner needs. The
  contract carries that as a refusal, and `[#740]`'s ask to extend `dispatch_verb_agreement` was
  **removed** as gold-plating rather than carried.

All three are the **same absent-discriminator class as `[#675]`** (operator's characterisation): a
check returns a uniform answer because the field that would separate the cases is absent from
what it reads. `[#675]` is in this same batch, which is where the class gets its mechanism. In
`[#740]`'s case the certifying detector is `dispatch_verb_agreement`, which passes by checking
that the surfaces **name** the ruled verb and never that the verb **accepts** the emitted fence.

## 7 · One finding that changes slot 3, recorded here because it outlives the lane

**The `/override` tombstone was never actually blocked.** The first x-734 run KEPT it citing
`release_lint.py`'s docstring — *"only `status: active` is legal this release … tombstones unlock
in P2, gated on operator decision D3"*. That docstring is **stale**: `ALLOWED_STATUSES =
{"active", "removed"}` at `release_lint.py:101`, unlocked by `1fbdf6f3`, **which is an ancestor of
`f1711e3d`** — so tombstones were already legal when the lane decided they were not. The manifest
already carries `ruff-gate` as the n=1 `status: removed` precedent.

So the "release_lint change that lets a tombstone land" is a **retraction of three stale prose
claims**, not a mechanism unlock. The lane's contract names all three.

This is itself the absent-discriminator class one layer out: a lane consulted prose, the code had
outgrown it, and a correct disposition was reversed on the strength of documentation. It is
recorded in the manifest rather than only in the contract because the lesson outlives slot 3.
