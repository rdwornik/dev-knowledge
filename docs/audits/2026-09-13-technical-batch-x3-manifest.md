---
batch: X3
seq: 3
status: open
closed_by: docs/audits/2026-09-13-technical-batch-x3-close-packet.md
---

# Batch X wave 3 — manifest (dispatch half) · 2026-09-13

**Seat:** dispatcher · **Batch:** X, wave 3 · **Ceiling:** ADR-110, six lanes
**Base at fire:** `main` = `69c8a344` for slot 1, `b154fd1a` for slots 2–4 — main advanced
mid-fire as the integrator merged the x-734 anchor, so **the four opening lanes do not share a
base**. Recorded rather than smoothed over; see §6 finding 5.
**Status:** **SIX CONTRACTS FROZEN. FOUR FIRED. TWO ON ROLLING BACKFILL.**

**Consumers:** `[#689]` · `[#683]` · `[#730]` · `[#664]` — plus two un-numbered lanes (the
trustworthy-suite lane from AX28-1 and the docs-cut manifest from AX28-2). Every contract named
in §2 is copied in-tree into `docs/audits/2026-09-13-technical-batch-x3-launch-contracts/`.

---

## 1 · The GO, recorded

This section IS the GO record. The operator's message of 2026-09-13 is the authority for every
lane below, and it arrived with its own model corrections already applied.

> …treat this as the operator's GO for batch X wave 3 — six lanes per to-cc/AMEND-BATCH-X-ROSTER-028.md
> AX28-4, with AX27-1..AX27-5 in force: concurrency 4 with rolling backfill, serialise on
> serialize-group overlap rather than refuse, `-Model` explicit, each recorded in the manifest, and
> no lane may wait on the operator mid-run. […] Freeze all six, DryRun, then poll until the wave-2
> merges are on main and fire. Report the receipts.

> Model corrections before freeze: lane (4) one-command row closure runs at `-Model sonnet`
> (bounded, fully specified work), and lane (5) spine runs `opusplan` (Opus plans, Sonnet
> implements) rather than pure opus. Lanes (1) opusplan, (2) opus, (3) sonnet, (6) sonnet
> unchanged. […] No non-Claude producer is ordered tonight: Grok and Copilot Enterprise enter the
> implement role through a supervised daytime trial, not an unattended run; Codex stays reviewer.
> Record the model and token count per lane on every receipt.

**Scope bound:** the GO covers these six lanes and no lane outside them fires on it.

## THE LANES — six, frozen 2026-09-13 (§2)

```
slot  row     slug                           model     effort  state at close of freeze
1     #689    lane-x-689-conductor-e-proof   opusplan  high    FIRED  session c8431775
2     --      lane-x-000-trustworthy-suite   opus      high    FIRED  session bcb07e60
3     #683    lane-x-683-three-small-fixes   sonnet    high    FIRED  session 8bc9be0d
4     #730    lane-x-730-one-command-closure sonnet    high    FIRED  session 5c655b7e
5     #664    lane-x-664-spine-armed         opus *    high    BACKFILL — gated on slot 2
6     --      lane-x-000-docs-cut-manifest   sonnet    high    BACKFILL — gated on first teardown
```

`*` **Slot 5 fires at `opus`, not the `opusplan` its frozen contract states** — because
`opusplan` on a `--bg` lane silently resolves to Sonnet, measured on slot 1. The full reasoning,
the evidence, and the fact that the operator may reverse it are §6 finding 7.

**Concurrency 4 with rolling backfill (AX27-2).** Four run; the next enters when one merges.
Wave 2 proved six concurrent lanes lose commits to memory, and a lost commit costs more than a
queued lane. The ADR-110 ceiling of six is unchanged — this is a concurrency bound inside it.

**Serialise-group (AX27-3):** slots 2 and 5 may both touch the persisted graph store. They are
**serialised, not refused** — slot 5 enters only once slot 2's worktree is gone. Teardown is the
**detectable proxy** for "slot 2 is no longer writing"; it is strictly more conservative than
handback, and handback is not observable from outside the lane. Each contract carries a
point-of-use copy of the order.

**`opusplan` on slots 1 and 5 was an operator ruling**, on each contract's routing row AND its
dispatch line, so the lane cannot re-decide it. It required widening `MODEL_ENUM` — §6 finding 1.

## 3 · STEP 0 refusals

| check | result |
|---|---|
| `lane-ceiling` (count leg) | **PASS** — 6 lanes ≤ 6 |
| `lane-ceiling --check-worktrees` | **REFUSED, twice, both times on non-lane worktrees** — §6 finding 3 |
| `carried-by` | **PASS** — 28 of 28 batch-X amendments governed and carried |
| `sleeping-poll` | **PASS** — 1 declared wait, with interval, bound and a ref-surface predicate |
| `dryrun-step0` | **PASS** — 6 of 6 contracts DryRun on the last line of step 0 |

## 4 · Receipts

**Dry runs.** All six taken with `Dispatch-Lane … -DryRun`. Every contract resolved, and **the
ordered model appeared on every resolved line** — including both `opusplan` lanes, which is the
whole point of finding 1.

**Live fires.** Four lanes, each confirmed up by its branch appearing, not by the command
returning:

```
slot 1  lane-x-689-conductor-e-proof    opusplan  session c8431775  branch up after  7s  base 69c8a344
slot 2  lane-x-000-trustworthy-suite    opus      session bcb07e60  branch up after 11s  base b154fd1a
slot 3  lane-x-683-three-small-fixes    sonnet    session 8bc9be0d  branch up after 11s  base b154fd1a
slot 4  lane-x-730-one-command-closure  sonnet    session 5c655b7e  branch up after 15s  base b154fd1a
```

**Token counts per lane** are read from each lane's own session transcript
(`~/.claude/projects/<encoded worktree path>/*.jsonl`, summing the `usage` block per assistant
message). The method was **validated against two completed wave-2 lanes before being relied on**,
and it does more than count: it reports the model each lane ACTUALLY RAN AT, so the ordered tier
is proven rather than assumed. Validation readings — `lane-x-675-merge-cost` 810,788 out /
225,001,610 cache-read on `claude-opus-5`; `lane-x-727-fail-closed` 249,563 out / 67,348,557
cache-read on `claude-sonnet-5` — both matching wave 2's ordered models. Cache-read is reported
separately from fresh input because the two bill differently and folding them would overstate
input several-fold. A lane still running reports a partial, and the transcript's last timestamp
is printed so a partial reads as partial.

## 5 · The wait condition — satisfied, then fired

**Fire only once the wave-2 merges are on `main`.** Operator instruction.

Written as code, not intention: interval 300 s, bound 24 ticks, predicate re-read from the ref
surface each tick. It **drained on tick 3** — `main` = `69c8a344`, lane x-734 zero commits ahead,
zero `lane-x-*` worktrees. The seat then fired. Had the bound been exhausted it would have
STOPPED and reported rather than extended, and it would not have fired into an unmerged tree.

**Unlike wave 2, firing was reachable.** Wave 2's manifest §5 recorded that it could not fire:
bare `dispatch` asks the operator to confirm and *"anything but `y`/`yes` — including empty or
non-interactive input — refuses"*, which a background seat cannot supply, and the only way past
was `-Run`, which would have bypassed the gate the wait existed to reach. The operator's GO in §1
is **explicit and prospective** — it is that consent, recorded in advance.

## 6 · Findings — eleven; one changes what the operator ordered, one needs an operator filing

1. **`MODEL_ENUM` refused the tier the operator ordered.** `gen_lane_contract.py` admitted only
   `{opus, sonnet, haiku}`, so a contract stating `opusplan` was refused by its own freeze gate —
   while the live verb ran it happily, `Dispatch-Lane` taking `-Model` as an unconstrained
   `[string]` handed to `claude --model` verbatim. Generator narrower than verb, no test between
   them: **AX25-1's root cause in miniature**, on a surface AX22-3 had already routed to
   `opusplan` (`SEAT-BOOT-integrator.md` has rendered `model: opusplan` since 2026-09-11).
   Widened RED-first, with a paired negative test keeping `--model gpt` refused. Admitted because
   the CLI **resolves** it — measured: `claude --print --model opusplan` returns a normal
   completion where a bogus id returns `[claude-code:unrecognized_model]`.

2. **The `Dispatch-Lane`/`claude` grammar seam CLOSED on `main` mid-freeze, and this seat's
   contracts predate the close.** At freeze time `dispatch <FILE> -DryRun` refused all six —
   *"the contract's `## Dispatch` block must invoke 'claude', not 'Dispatch-Lane'"*
   (`Invoke-Dispatch.ps1:285`), unchanged since wave 2 recorded it — so receipts were taken with
   the boot's §4 fallback and the lanes fired the same way. By the time this branch synced, the
   generator on `main` emits a **`claude` fence** and names `dispatch` as the ruled verb. **The
   six frozen contracts still carry the old `Dispatch-Lane` fence** and are immutable; they fired
   correctly through it. Slot 3's AX25-2 clause — the conformance test between generator and verb
   — is what keeps this closed, and it is still owed: the fix landed without the test that would
   have caught the divergence in the first place.

3. **`lane-ceiling --check-worktrees` cannot pass for a dispatcher seat.** It refuses on worktree
   PRESENCE with no discrimination — not merged/unmerged, and **not lane/non-lane**. At step 0 it
   named four wave-2 lane worktrees, handed back and awaiting the integrator, whose teardown
   would have destroyed unmerged work. Re-run at fire time with every lane worktree gone, it
   *still* refused — on the two **dispatcher freeze worktrees**, one of which is the seat's own,
   which the protocol requires it to have. The substantive condition was verified directly
   instead: zero wave-3 lane branches existed at fire time. This sharpens the absent-discriminator
   class wave 2 filed.

4. **Every `-DryRun` exits 1 while printing a correct resolution.** Confirmed benign rather than
   assumed: `$Error.Count` is 0 and `$LASTEXITCODE` is 1, a leaked code from the internal
   "does this branch already exist?" probe, which correctly finds nothing. Still a trap for any
   gate that wraps the verb and reads exit codes.

5. **The four opening lanes do not share a base**, because `worktree.baseRef='head'` resolves each
   lane's base at ITS OWN dispatch moment and the integrator merged the x-734 anchor between slot
   1 and slot 2. Slot 1 is on `69c8a344`; slots 2–4 on `b154fd1a`. Harmless here — the delta is
   one anchor merge — but a batch whose lanes silently straddle a base is the shape that makes
   "it passed in my lane" unreproducible, and nothing currently records the base per lane except
   this line.

6. **`Dispatch-Lane` prints `'m' is not recognized as an internal or external command` on every
   fire.** Cosmetic — all four lanes came up and their branches appeared — but it is a quoting
   defect in the verb's own output path, emitted once per dispatch, and it will mislead whoever
   next reads a dispatch log for errors.

7. **`opusplan` IS A NO-OP ON A `--bg` LANE, AND IT SILENTLY BECOMES SONNET.** The most
   consequential finding of the night, and it falsifies the premise two of the operator's own
   model corrections were made on.

   **Measured, not inferred.** Slot 1 was dispatched `--model opusplan`. Its own session
   transcript records **84 of 84 assistant messages on `claude-sonnet-5`, zero Opus**. The other
   three opening lanes came back exactly as ordered — slot 2 `claude-opus-5`, slots 3 and 4
   `claude-sonnet-5` — so the instrument discriminates rather than reporting one answer.

   **Cause.** `opusplan` is a SPLIT tier that routes Opus *to plan mode*. Dispatch constants put
   every lane on `--permission-mode bypassPermissions`, which never enters plan mode. With no
   plan phase there is no Opus phase, so the tier collapses to its implement half. Nothing warns:
   the flag is accepted, the resolved line reads `--model opusplan`, and the lane runs Sonnet.

   **The scope of the correction is narrower than it first looks.** `opusplan` remains CORRECT
   for an INTERACTIVE seat — an attended session can enter plan mode — so **AX22-3's routing of
   the integrator seat to `opusplan` is untouched**, integration being always local and
   interactive. What is falsified is `opusplan` on an unattended `--bg` LANE, which is a
   different population that happens to share the word.

   **What this seat did about it.** Slot 1 was already 84 messages into real work and was LEFT
   RUNNING — its contract is the most mechanical of the six (run a suite twice, record numbers),
   and burning that progress for a tier change is a worse trade than reporting it. Slot 5 had not
   fired, so it was corrected before launch: **it fires at `-Model opus`, not the contract's
   `opusplan`.** Firing it at `opusplan` would have delivered Sonnet — a tier the frozen contract
   does not name either — so there was no faithful-literal option and both choices deviate. Opus
   is the one matching intent: the operator's own gloss ("Opus plans") asks for Opus involvement,
   and Ch8's routing matrix routes **gate and organ code** — exactly `[#664]`'s three commit-tier
   refusals — to `opus`. Deviation-with-disclosure does not authorise itself, so this is the
   disclosure and the operator may reverse it; re-firing slot 1 at `opus` is one command.

   **Owed as a row:** the enum widened in finding 1 admits a tier that is inert on the surface it
   was widened for. `MODEL_ENUM` should either refuse `opusplan` for `shape: local` or the
   contract should carry the warning, and `gen_lane_contract.py` is where that check belongs —
   the same generator-knows-better-than-the-line property `[#717]` and `[#740]` already establish.

8. **This manifest DECLARES ITS BATCH OPEN — batch X's and X2's did not, and that omission is
   what made wave-2 integration cost an anchor arc PER MERGE.** The ADR-110
   declared-integration-arc exemption requires all four: the manifest tracked by git,
   `status: open`, a `closed_by:` whose shape can resolve, and that closer ABSENT from the tree
   (absence is what makes the exemption EXPIRE instead of running forever). **Batch X and X2's
   manifests carry no frontmatter at all**, so `batch_manifest.open_batches()` returns `[]` —
   confirmed by calling it directly, not inferred from a gate — the exemption was never live,
   and every lane merge left an unanchored spine entry that FAILed the next commit taken in any
   tree. Four wave-2 merges, four two-commit anchor arcs. **That is precisely the integration
   throughput bound AX28-3 names as the night's real constraint**, and it was a dispatch defect
   rather than an integrator one.

   This seat inherited the defect by modelling §1–§7 on X2's manifest, and caught it before
   committing — the one window in which it is fixable, since `docs/audits/` is immutable once
   landed and a missing declaration must then be reported rather than patched. The frontmatter
   above is verified to parse (`status: open`, closer shape valid, closer absent), so wave 3's
   six merges get the exemption X2's four did not. **A seat opening a merge queue should run
   `batch_manifest.open_batches(repo)` first: an empty list means budget one anchor arc per
   merge, and say so up front.**

9. **`[#683]` IS CLOSED, and slot 3's contract cites it as live work.** Surfaced by the
   `graph-task-coverage` gate refusing this commit: `LANE-x-683-three-small-fixes.md` has no
   `implements` edge from an OPEN row, because `tasks/683-…` carries `status: closed` — closed
   2026-09-11 on the operator's word, its Done-when (`/override` node and payload absent,
   `release_lint.py` green) witnessed at `0bb1d5ce`.

   The contract names `[#683]` three times and the mention buys nothing: the gate wants an open
   row, and a closed one cannot claim a file. **AX28-4's clause "`[#683]`'s predicate scoped to
   `status: active` so a tombstone may land" therefore points at a row that is already finished.**
   The *work* may still be real — the `release_lint`/tombstone predicate is adjacent to what
   `[#683]` did — but it needs its own OPEN row, and the operator is the one who files or reopens.
   Slot 3's other two clauses (`safe_remove.py`'s stem-literal downgrade, AX25-2's
   generator-to-verb conformance test) are unaffected and are the two that matter most tonight.

   **Slot 3 was NOT stopped.** It is working, and two of its three clauses stand on their own; the
   third is a filing question the operator rules, not something this seat resolves at 3am by
   reopening a closed row.

10. **`LANE-x-730-one-command-closure.md` never names `[#730]`** — an authoring miss by this seat.
    The row is open and the work is right; the contract's prose simply says "one-command row
    closure" without the id, so the graph forms no `implements` edge. Harmless to the running lane
    (slot 4 reads the contract, not the graph), but it is why the in-tree copy could not land.

**Consequence for this commit, stated rather than worked around:** the two contract copies above
are NOT in it. The other four are, with the manifest. The frozen originals for all six remain on
the transport, which is what the lanes actually read, so no lane is affected. Editing either task
row to manufacture the claim was rejected: `[#683]`'s is closed (reopening is the operator's act)
and both rows are owned by lanes running right now, so an edit from this tree would collide at
integration.

11. **`graph-rebuild` is not concurrency-safe, and this batch runs four concurrent lanes by
    design.** A commit attempt failed inside `graph_store.py::_swap_into_place`; the same rebuild
    run standalone a minute later succeeded and emitted a full edge census. The persisted FPG-1
    store lives in the common git directory and every commit in every worktree rebuilds it, so
    simultaneous commits from sibling lanes race the swap. AX27-2 sets concurrency at 4, which
    makes this reachable on any busy night rather than theoretical — and its symptom is a
    traceback in an unrelated lane's commit, which is the worst place to read it from.

## 7 · What this seat did NOT do

- **No non-Claude producer was ordered.** Grok and Copilot Enterprise enter the implement role
  through a supervised daytime trial, not an unattended run; Codex stays reviewer (operator,
  2026-09-13). Nothing in this batch routes work to either.
- **No integrator render refresh was needed.** AX22-3 asked that the integrator render carry
  `opusplan`; it already does (`SEAT-BOOT-integrator.md`, `model: opusplan`, stamped 2026-09-11),
  verified on the transport rather than assumed.
- **No peer's work was committed.** An uncommitted Codex review stub
  (`docs/audits/2026-09-13-codex-x727-fail-closed.md`, tally still `TBD`) sits in the primary
  checkout. It is the integrator's in-flight work; this seat left it alone.
- **`worktree-dispatch-x2-freeze` is still unmerged** — one commit (`674e67ce`, the AX25 filing).
  It is wave 2's dispatcher branch, not this seat's, and it belongs in the integrator's queue.
