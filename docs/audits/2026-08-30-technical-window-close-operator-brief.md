# WINDOW CLOSE — what changed, in your three categories

> **For the operator.** Every number below is measured on the tree at close, not recalled. The
> "before" column is the state at window open (2026-08-29 morning, `main @ 66662c70`); the "after"
> is `main` at close. Where a number could not be re-derived it says so instead of appearing.
>
> - **Consumed by:** `docs/audits/2026-08-30-technical-autonomy-decision-tree.md`,
>   `ecosystem/north-star.md`, and the window-close JOURNAL entry.

---

## SMALLER — what there is less of

```
                              before        after      delta
CLAUDE.md                 39,147 B      23,931 B    -15,216 B  (-38.9%)
CLAUDE.md lines                 240           230         -10
codex/                    1 file /            0 files       gone
                           3,891 B                    (universalised, NOT deleted)
silent-rule ratchet             443           443           0   (nothing spent)
```

**The CLAUDE.md number is the one that matters, and the reason is the interesting part.** The file
had claimed *"≤200 lines"* and satisfied it — at **165 B/line against a corpus average of ~117**.
The line count was being met by density while the cost you actually pay every session, bytes, was
unbudgeted. It is now budgeted **in bytes, with a gate**. The lines barely moved (240 → 230) and
the bytes fell by nearly two-fifths, which is precisely the gap between the proxy and the thing.

**`codex/` is gone as a folder and NOT gone as content.** Z-G5 ruled it *"not free to delete"* —
it is a live carrier source. It was universalised into the per-CLI instruction architecture, and
the lane went further than asked: `AGENTS.md`'s precedence section now reads *"there is
deliberately no third layer"*, so the `role → doctrine → role` trap is **removed rather than
documented**.

**The ratchet spent nothing.** Every doctrine addition across the window — and there were many —
was authored token-free rather than by requesting headroom against a baseline that has none.

---

## VISIBLE — what can now be seen that could not before

```
                                        before                  after
FUNNEL HEALTH block            6 x "unavailable"        real numbers, all six
SDA-1 adversarial floors          UNCALIBRATED          C=3 H=5 M=5 L=2 (15 items)
terra post-merge round N+I           OWED               C=0 H=3 M=1 L=0
copilot context ceiling            unmeasured           284,300 tokens, canary-verified
copilot billing                "shows zero, why?"       PROVEN routing, UNREAD meter
the arc set / what blocks what      nowhere              ecosystem/north-star.md (generated)
research findings routed             none               55 leaves, 100% routed
unconsumed audit artifacts             28                    10 (all one class)
```

**FUNNEL HEALTH is the headline.** Every handoff bundle had been rendering six `unavailable`s
because the FM-2 ↔ FM-4 field coupling had **zero overlap** — six attributes read, eleven exposed,
intersection empty. It rendered honestly and nobody read it. It now renders numbers.

**Three measurements existed only as adjectives before this window** and are now quantities: the
adversarial floors (which is what "UNCALIBRATED" had meant), the post-merge review tally, and the
provider's context ceiling. A floor you cannot compare against is not a floor.

**The billing answer is a wrong-meter answer, not a routing defect.** Your panel reads zero
*correctly* — it tracks Copilot **Individual** subscriptions and neither account holds one.
Consumption is on the **org** billing page. Proven by witness: a call forced under the personal
token was refused for lack of entitlement, so it could not have billed there.

---

## UNBLOCKED — what can now proceed that could not

```
test_shared_fields_equal_fm4_block   RED (pre-session)  ->  GREEN
FM-2 leg (d)                         NOT ARMED          ->  armed, 1 live finding
ADR-114 (root README)                PARKED             ->  executed; README.md exists
ADR-81 section 45 (fuzzy band)       deferred arc       ->  ADR-116 landed
intake #35 R3 (the eval corpus)      dead fold target   ->  [#625] born
batch-D                              not frozen         ->  7 lanes landed, torn down
backlog rows                         210                ->  218
```

**The sequence is the unblocking, more than any single row.** Four research lanes independently
found the same shape — *this repo is an excellent environment and has no learning signal* — which
gives an order with no branch in it: **metric → measure → only then an optimizer.** That is why
only 2 of 18 true gaps became rows and ten are parked behind named triggers. A gap birthed ahead
of its blocker is a row nobody can work.

**`[#625]` is the head of that sequence** and it exists because a fold instruction was
unexecutable: its target was deferred *and* carried the wrong subject entirely. Nobody was
watching. `[#624]` now watches.

---

## The three things that cost the most, and what they teach

1. **A gate that could not run.** `lane-contract-check` hands every staged contract to a command
   that accepted one path, so the first multi-contract commit died with *"unexpected extra
   arguments"*. It did not refuse a bad contract — **it failed to execute**, silently, past eleven
   prior contracts. *An advisory that never fires and a gate that cannot run look identical from
   outside.*
2. **An explanation built on an unread predicate.** Two lane merges behaved differently; I produced
   a theory instead of reading `batch_manifest.py`. Both halves were wrong, and the manifest I had
   credited with a fix was **inert**. It failed *safe*, which is exactly why the wrong model
   survived long enough to be built on.
3. **A teardown that iterated the wrong enum.** Batch D dispatched across local *and* cloud
   substrates; the teardown iterated local branches only, so a 259-line ADR sat stranded on a
   remote branch while the batch looked complete. *"No leftovers" was satisfied locally and the
   deliverable was still missing.*

All three share one shape: **a mechanism whose failure mode is silence.** The repo's gates are good
at refusing bad input and were, in these three cases, unable to report their own absence.
