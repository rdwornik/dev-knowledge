# LANE batch-e-h-8-local-memory-tier-l-evaluation (DM-4) - TIER-L EVALUATION, not a build: does a local vector index beat grep on 20 real questions? Downgraded from Tier-S by architect ruling CUT-4.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud`

```
Dispatch-CloudV2 LANE-h-8-local-memory-tier-l-evaluation.md -Title 'lane-h-8-local-memory-tier-l-evaluation'
```

**SHAPE IS `cloud` BY ARCHITECT RULING CUT-4**, not by sizing: a Tier-L evaluation installs
packages, and installing them anywhere near the operator's declared environment is precisely
what ADR-106 gates. A disposable off-machine scratch env is the only place this is cheap.

## Worktree pairing

slug `lane-h-8-local-memory-tier-l-evaluation` -> branch `claude/lane-h-8-local-memory-tier-l-evaluation` -> contract `LANE-h-8-local-memory-tier-l-evaluation.md`

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5). Both
fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<total line count of this brief, and its final line verbatim>`

A dispatch missing either half is treated as not having started, and is re-dispatched. The lane
also branches fresh off `origin/main` and leaves files it did not author and this contract does
not name exactly as found (Q4).

## Write-scope (frozen)

**NONE in the repo.** The entire output is one measurement artifact returned by harvest.
**ZERO repo dependency change this batch** - no `pyproject.toml`, no `uv.lock`, no `scripts/`
producer. ADR-106 makes a dependency change its own gated act and this lane does not take it.

**Substrate deviation:** `substrate-teardown-enum-coverage` - this lane runs off-machine on the
cloud transport, whose `claude/<slug>` branch shape `LANE_BRANCH_RE` cannot match; the batch
manifest enumerates this lane by name and the teardown iterates the manifest rather than the
branch regex.

## WHY THIS LANE WAS DOWNGRADED - architect ruling CUT-4, on three measured failures

1. **"sqlite-vec proven under pinned uv by lane-g" is REFUTED.** The autonomy synthesis proves
   only that `enable_load_extension` works on this host, and says outright: *"Nothing was
   installed and nothing was written to run this."* sqlite-vec was never installed, never run,
   never exercised under the pinned `uv`. "Live candidate" is not "proven".
2. **It is ADR-112 TIER L, not Tier S.** The guard sentence: *"Tier S never touches gates, hooks
   that block, or `scripts/` - anything that would, is Tier L by definition."* The synthesis
   already corrected TWO cloud lanes for this exact mislabel, and intake #63 says it verbatim:
   *"ADR-112 Tier-L applies: evaluate before adopting."*
3. **`sentence-transformers` IS ON THE REJECTED LIST** - with ChromaDB, LanceDB, Mem0,
   Letta/MemGPT and Zep. **Do not use it.** The synthesis pairs sqlite-vec with **`model2vec`**,
   and that is where this lane starts. Reaching for the rejected embedder anyway requires
   writing down why, in the report.

## Done-contract (immutable)

1. **A scratch environment**, off the operator's machine, holding sqlite-vec plus a
   NON-REJECTED embedder. Nothing installed into the repo's declared environment.
2. **An index over `docs/` and `tasks/`**, and a **hit-rate measurement against `grep` on 20
   REAL questions** - questions a seat actually asked, not invented ones. List all 20.
3. **The measurement recorded either way.** A result saying grep wins is worth as much as one
   saying it loses, and is the cheaper outcome to act on.
4. **NO ADOPTION.** The Tier-S build rides the NEXT batch, on this measurement.

## Steps

1. Build the scratch env; state exactly what was installed and where.
2. Choose the 20 questions and justify the sample.
3. Measure. Report hit-rate both ways with the raw per-question outcomes.
4. Print the measurement as the final message. It returns by harvest.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
