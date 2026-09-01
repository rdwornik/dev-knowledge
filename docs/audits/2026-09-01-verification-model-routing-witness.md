# MODEL ROUTING — witnessed per lane, and the ledger's "31 lanes on opus" is FALSE

- **Class:** verification · **Date:** 2026-09-01 · **Arc:** `[#614]` · **Consumed by:** `[#614]`, `[#615]`
- **Question (operator, at the batch-F GO):** the ledger says 31 lanes ran `opus/high`; R-MODELS
  ruled **sonnet for workers**. Is the model parameter not applied at dispatch, or does the ledger
  read the orchestrator's model?

---

## 1 · The answer: NEITHER. The parameter IS applied; the ledger read the CONTRACT.

**The model parameter is applied at dispatch — witnessed.** **The ledger did not read the
orchestrator's model either.** It read each lane's **declared routing table**, and it says so in
its own words: *"Three of the five columns reconstruct cleanly from committed manifests and
contracts."* Every batch-E contract declares `| opus | execute | high |`, so every row reads
`opus / high` — **a declaration, rendered as if it were a measurement.**

## 2 · The witness — actual models, from the session transcripts

Not from a contract, a manifest or a process list: from `~/.claude/projects/<lane>/*.jsonl`, which
records the model of every assistant turn. Counts are assistant turns at that model.

```
batch-E lane                                    WITNESSED        contract DECLARES
lane-b-2-essentials-and-claude-md   119 turns   claude-opus-5    opus     (DC-3, 1st dispatch)
lane-b-3-claude-md-genre            260 turns   claude-sonnet-5  opus     (DC-3, re-dispatch)
lane-c-3-root-contract               71 turns   claude-opus-5    opus
lane-d-4-ai-council-instantiation   107 turns   claude-sonnet-5  opus
lane-e-5-eval-sda1-harbor            75 turns   claude-sonnet-5  opus
lane-f-6-observability-otel          60 turns   claude-sonnet-5  opus
lane-g-7-typed-multi-layer-graph     73 turns   claude-opus-5    opus
lane-i-9-distiller-filing-amendment  77 turns   claude-opus-5    opus
lane-j-10-equilibrium-checkpoint    120 turns   claude-sonnet-5  opus
lane-k-11-derived-doc-freshness     264 turns   claude-opus-5    opus
lane-l-12-logs-retention-rule        82 turns   claude-sonnet-5  opus
lane-m-13-templates-disposition     100 turns   claude-sonnet-5  opus
lane-n-14-trends-burndown-quota     110 turns   claude-sonnet-5  opus

BATCH E, 13 lanes witnessed:  8 SONNET · 5 OPUS  -- MIXED, not uniform
batch D (a-619, d-000, g-000):  3 of 3 OPUS      -- and batch D PREDATES R-MODELS
```

A second, independent witness for the same fact was captured live earlier the same day: the DC-3
lane's own OS process command line read
`claude.exe … --model sonnet --effort high --worktree lane-b-3-claude-md-genre`, while the
contract it was executing declared `opus`.

**So the ledger's headline — *"Every one of the 31 lanes ran on opus at effort: high"* — is
false**, and its conclusion drawn from it (*"there is no model variance to analyse"*) is false
twice over: there **is** variance, and it is invisible to every committed surface.

## 3 · The real defect underneath it: THREE surfaces default to opus, independently

```
gen_lane_contract.py   DEFAULT_MODEL = "opus"    -> the CONTRACT declares opus unless told
DispatchHelpers.psm1   [string]$Model = 'opus'   -> the RUN uses opus unless told   (line 96)
the ledger             reads the contract        -> reports opus whatever ran
```

**The contract's model and the dispatch's model are two surfaces free to disagree, and nothing
checks them.** That is the same class `gen_lane_contract` already refuses for the command line —
its own words: *"two forms free to disagree is the class this generator removes"* — closed for the
dispatch verb and left open for the model.

**And the operator's concern is REAL, just smaller than the ledger implied: five batch-E lanes did
run opus.** Under R-MODELS (*"Orchestrator and every integration adjudication ran Opus. All seven
dispatched lanes ran Sonnet, set at dispatch through `Dispatch-Local`'s own `-Model` parameter"*),
a dispatched lane is sonnet-class. Five were not, and no surface would ever have shown it —
because the one surface anyone would check declares `opus` for all of them regardless.

**R-MODELS was ruled during the 2026-09-01 night window.** Batch D (all opus) predates it and is
not a violation. Batch E straddles it.

## 4 · IT REACHES BATCH F RIGHT NOW

**Six of the seven frozen batch-F contracts declare `opus`** — L1, L2, L4, L5, L6, L7; only L3
declares `sonnet`. They were generated with the generator's default and frozen before this was
measured. **L1 is staged for dispatch.**

If R-MODELS binds as recorded — dispatched lane = sonnet, orchestrator and adjudication = opus —
then six contracts declare the wrong model and the fix is a **REISSUE**, not an amendment, because
changing a frozen routing table is not additive.

**This is a routing decision and it is the technical architect's** (ADR-108 §A), so it is reported
rather than taken. What this file establishes is only the fact: the parameter works, the ledger
reads a declaration, and the defaults on three surfaces all point at opus.

## 5 · The fix, in the order that makes each step checkable

1. **Correct the ledger's claim** — an amendment on its sidecar, not a rewrite of the landed HTML.
2. **Rule the model per batch-F lane**, then reissue the contracts that change.
3. **Close the disagreement structurally**: either `Dispatch-Local` READS the contract's routing
   table instead of carrying its own default, or a gate asserts the two agree. A default that
   silently wins over a frozen declaration is the defect; the ledger only made it visible.
4. **`[#615]` remains the enabling row** for ever seeing this from the repo rather than from
   `~/.claude/projects/`. Session transcripts are outside the repo, per-machine, and not a
   governance surface — this witness is real but it is not a mechanism.
