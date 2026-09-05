---
intake-id: 69
status: DRAFT
origin: outgoing Layer-1 browser-seat notes, window 2026-09-02 -> 2026-09-05, section 3 (prioritisation bullet); landed at docs/audits/2026-09-05-technical-browser-seat-notes.md and filed by lane worktree-docs-seat-notes on 2026-09-05
consumed-by:
---

# Boot prioritisation is a sort, not an engine — class weights inside `boot_frontier`'s existing score seam

## Problem / motivation

`/boot-session`'s PROPOSED NEXT BATCH is computed by `scripts/boot_frontier.py`: the
unblocked frontier is the in-degree-0 set of the open `depends-on` graph, scored by
`default_score` — which wraps `gen_task_tree.rank_key`, the already-ruled `[#566]` axis
(P-enum primary, constraint-contention tiebreak, id-as-age floor) — and then cut to a batch
under disjointness, width and ledger bounds.

That axis answers *"which open rows are most important in the abstract"*. It does not
answer *"which rows should this window work on"*, and in one measured window the two
diverged completely: **the frontier proposed 5 rows, none of them on the agenda.** A
proposal nobody acts on is not a cheap miss — it is the boot surface spending the operator's
attention and then being set aside, every window, which teaches the seat to skip it.

The outgoing seat's reading is that the missing input is *ordering by class*, and that every
class it names is **already computable from surfaces this repo has**: `propose_closures`
already knows which rows are witnessed on main; the agenda already exists as the NC list;
holds already carry row ids; the current frontier is already the P1-by-disjointness sort.
Nothing here needs a new scorer, a new model, or a new script — it needs the existing
`ScoreFn` seam supplied with a class weight.

This is filed, not built, for a specific reason: `boot_frontier`'s own docstring says the
scoring rule is **a declared seam whose permanent value BOOT-R1 pins**, and that BOOT-R1's
survey is still RUNNING. `default_score` is documented as the placeholder chosen precisely
because it is *"the one axis the repo has already ruled, not a new one"*. Replacing a
placeholder that was picked to avoid inventing a rule, by inventing a rule, would undo the
discipline that put it there. Whether these weights are the pin, an interim, or input to
BOOT-R1 is the ratification question.

## Scenarios (+1 view)

- **As the operator, I read PROPOSED NEXT BATCH and the first rows are ones whose
  `Done-when` is already witnessed on main.** They cost approximately nothing to close, so
  the closure counter moves in the first minutes of the window rather than at its end.
- **As the operator, I read PROPOSED NEXT BATCH and the rows on the current NC list appear
  in NC order.** The boot surface and the agenda agree, so I do not maintain the agenda
  separately in my head and set the proposal aside.
- **As the browser seat, a substrate is held (`[#634]`-shaped).** The row that would unblock
  it sorts above ordinary P1 work, because everything queued behind the hold is worth more
  than one more P1.
- **As the browser seat, no row falls into any named class.** The proposal is exactly what
  it is today — P1 by serialize-group disjointness — so the change is a **reordering of the
  same set**, never a narrowing of it.
- **As the architect, BOOT-R1 returns with a scoring model.** It reads these weights as one
  documented candidate with a measured defect behind it, and pins whatever it pins. The seam
  is unchanged either way.

## Functional requirements

The proposal, **verbatim** from the source §3:

- **Prioritisation is a sort, not an engine** (library-first: no new scorer). `boot_frontier` today scores P1 flow rows. Proposed order, computed from surfaces that already exist:
  1. rows whose Done-when is already witnessed on main (`propose_closures`) — cost ≈ 0, closure rate ↑ first;
  2. rows on the current NC list for the next tag/H0 (the agenda), by NC order;
  3. rows unblocking a held substrate or provider (holds like [#634]);
  4. P1 by serialize-group disjointness (today's frontier);
  5. everything else.
  Batch G's divergence (frontier proposed 5 rows, none on the agenda) is the measured defect this fixes. Implementation: a weight per class in `boot_frontier`, not a new script.

Read as requirements:

- **Must:** the ordering is a **sort over the existing frontier**, not a filter. A row that
  the current implementation would propose is never dropped by this change — only moved.
- **Must:** each class is computed from a surface that already exists (`propose_closures`,
  the NC/agenda list, hold row ids, the current disjointness sort). A class that needs a new
  source of truth is out of scope for this intake.
- **Must:** it lands as a **class weight consumed through `ScoreFn`** — the seam
  `boot_frontier` already declares — leaving `default_score` available and the module's
  frontier, disjointness, width and ledger logic untouched. **Not a new script.**
- **Should:** class 5 ("everything else") preserves today's `[#566]` ordering exactly, so
  the change is provably a re-rank of the head of the list rather than a new global order.
- **Should:** the class assigned to each proposed row is **visible in the output**, so the
  operator can see why a row sorted where it did and can dispute it.
- **Could:** the weights are declared as data (a named constant, per the repo's preference
  for a declared seam) rather than as branching inside the scorer.

## Acceptance criteria (ex-ante)

1. For a fixed open-row set, the batch proposed by the weighted scorer contains **exactly
   the same rows the unweighted scorer would have made eligible** at unbounded width —
   ordering differs, membership does not. A row disappearing is a failure.
2. Given a row whose `Done-when` is already witnessed on main (per `propose_closures`) and
   an ordinary open P1 with no class, **the witnessed row sorts first**.
3. Given rows on the NC/agenda list, **they appear in NC order** relative to one another.
4. Given a row that unblocks a declared hold, **it sorts above class-4 rows**.
5. With **no** row in classes 1-3, the proposal is **byte-identical** to today's output. This
   is the criterion that proves the change is additive.
6. The measured defect is re-measured: for the window that first runs under it, record **how
   many proposed rows were on the agenda**, against the stated baseline of **0 of 5** in
   batch G. A number, not a verdict.
7. `select_batch`'s disjointness, width and ledger bounds and the `BatchProposal`
   never-dispatches property are **unchanged** — asserted by the existing tests continuing to
   pass unmodified.

## Non-goals

- **A new scorer, a new model, or a new script.** The source says this explicitly
  ("library-first: no new scorer", "a weight per class in `boot_frontier`, not a new
  script") and it is the load-bearing constraint of the filing.
- **Superseding BOOT-R1.** This does not pin the permanent scoring rule; BOOT-R1 does. If
  BOOT-R1 lands first, this becomes input to it rather than a competing answer.
- **Changing what a batch may contain.** Disjointness, `BATCH_WIDTH_MAX` and `LEDGER_BOUND`
  are out of scope, as is the human-GO property.
- **Replacing `[#566]`.** The ruled axis stays as the within-class and residual order.
- **Automating the agenda.** Class 2 assumes an NC/agenda list exists to read; producing or
  maintaining one is a separate question.
- **The §2 bundle-content deltas.** Those are intake #68 — that changes what the bundle
  *carries*, this changes what the repo *proposes*.

## Impact sketch (4+1 lite)

- **Logical:** the scoring seam gains a primary key (class) ahead of the existing `[#566]`
  key, which becomes the within-class order. The frontier and batch-selection models are
  untouched.
- **Process:** the boot proposal starts agreeing with the window's actual agenda, which is
  the point. It also makes the proposal disputable — a visible class is something the
  operator can overrule, where a bare rank is not.
- **Development:** `scripts/boot_frontier.py` (a `ScoreFn` implementation plus a weights
  constant) and `tests/test_boot_frontier.py`. Class 1 needs `propose_closures`' witness
  data reachable from the library; whether that is an import, a passed-in argument, or a
  reason the class cannot be computed here is the main technical unknown.
- **Physical:** none — the module is read-only, drives no state, and stays Layer-2 (ADR-28/36).

## Open questions

- **Where does class 1's witness data come from?** `propose_closures` runs as a plugin `Stop`
  hook. Whether `boot_frontier` may import it, must receive its output, or must not depend on
  it at all is a technical-architect question and the likeliest reason the ordering would need
  re-cutting.
- **What is the agenda, mechanically?** Class 2 says "the current NC list for the next
  tag/H0". That list lives in browser-window packets today, not in a repo surface the library
  can read. If it has no in-repo home, class 2 is not computable as stated.
- **Are the classes exclusive, and what breaks ties across them?** A row can plausibly be both
  witnessed-on-main and on the agenda. The source states an order, not a partition.
- **Weights or strict tiers?** "A weight per class" implies arithmetic that can be outvoted by
  a strong within-class score; a strict tier cannot. These behave differently and the source
  does not say which is meant.
- **Does this collide with BOOT-R1's remit?** If BOOT-R1 is chartered to pin the rule, filing
  a rule here may be the same rival-authority failure the seam was designed to avoid. Worth an
  explicit ruling before build, not after.
- **Is one window's divergence enough evidence?** The measured defect is n=1 (batch G, 5 rows,
  0 on the agenda). It is a striking number and a single observation.

## Status

DRAFT — filed 2026-09-05 by lane `worktree-docs-seat-notes` as a CANDIDATE per ADR-111
(CANDIDATE -> intake -> ratification). Not triaged, not ratified, no backlog row born from
it. Source landed verbatim at `docs/audits/2026-09-05-technical-browser-seat-notes.md` §3;
the source marks the whole section OPINION with a measured basis, and this filing does not
upgrade that.
