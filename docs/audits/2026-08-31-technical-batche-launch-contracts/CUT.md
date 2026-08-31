# BATCH E — THE ARCHITECT'S CUT

> **Ruled 2026-08-31 by the operator, on `PLAN.md`'s four named blockers.** This file is the
> DECISION record; `PLAN.md` beside it is the derivation. Where the two disagree, **this file
> wins and `PLAN.md` is the superseded draft** — PLAN.md is not edited, on the immutability
> discipline that governs audits.
>
> **Effect: all four blockers are cleared. The batch is UNBLOCKED and proceeds to FREEZE.**
>
> Flat by design — no pipe tables — so it copies into browser chat without border glyphs.

---

## CUT-1 · U-1 — TWO DEPLOYMENT ORDERS. RULED: they were never rivals.

**The ruling.** The **MIGRATION WAVE** ships in the operator's order:

```
hub -> monorepo -> ai-council -> win-tooling
```

**What "last" means, stated because the plan read it as a demotion and it is not.**
win-tooling's position at the END of the migration wave **does NOT roll back its status as the
FIRST INSTANTIATED CONSUMER.** The floor stays. win-tooling is:

- **FIRST** to be instantiated — it already carries the engine, and `DC-5` uses its template as
  the precedent for consumer #2 (ai-council). That is why DC-5 exists at all.
- **LAST** to receive the **consolidated-doctrine migration** — because it is the most mature
  consumer, so it is the one that can most afford to wait, and the one where a mid-re-genre
  ship would cost the most.

**So the "conflict" PLAN.md named is dissolved rather than adjudicated.** The two orders address
two different things: **instantiation order** (win-tooling first — already true, unchanged) and
**migration order** (win-tooling last — this ruling). PLAN.md's U-1 was right that two sequences
were on the record and wrong that they contradicted; naming it was still correct, because a
sequence that reads as a contradiction has to be resolved explicitly or it gets resolved
silently by whoever ships first.

**Recorded supersession.** The `sequence` field on the DEPLOYMENT WAVE arc in
`scripts/gen_north_star.py` — where the older HERMETIZATION order lives — now carries the ruled
migration order and this distinction, replacing the "CONFLICT NAMED, NOT RESOLVED" text. The
intake #62 amendment carries the same supersession, since it is the other site that recorded the
open conflict.

---

## CUT-2 · U-4 — DC-2/DC-3 ARE FLEET-WIDE. RULED: not a blocker. That IS the intended order.

**The ruling.** DC-2 and DC-3 **edit the HUB-OWNED regions first** — the hub regions are the
**source of truth**, and consolidating them is the point of the DOCTRINE CONSOLIDATION arc, not a
side effect to be avoided. The **DEPLOYMENT WAVE consumes the consolidated regions afterwards**,
in CUT-1's order.

**The circularity PLAN.md feared does not exist**, and the reason is worth stating so it is not
re-derived next batch: `blocked_by` on the DEPLOYMENT WAVE arc means *shipping a corpus
mid-re-genre ships the churn rather than the doctrine*. Editing the region templates **is** the
re-genre. The block says "do not SHIP while the corpus is churning" — it does not say "do not
CHANGE the corpus". Consolidate first, ship second. That was always the sequence; PLAN.md read
the block one step too strictly.

**Consequence for fleet parity, named rather than discovered:** between DC-23's merge and the
first consumer deploy, the hub's region templates lead the fleet. That window is **expected and
declared**, not a defect, and it closes on the migration wave's first step (hub -> monorepo).

**The Obsidian DELETE proceeds UNCONDITIONALLY.** `CLAUDE.md` `:40` and `:77` are **REPO-owned**
(verified against the `methodology:start/end` markers, not inferred), so the deletion is hub-local
with zero fleet consequence and is gated on nothing.

---

## CUT-3 · U-6 — DC-1/DC-2/DC-3 COLLIDE ON CLAUDE.md. RULED: one lane, and DC-1 gets out of the way.

**The ruling, in three parts:**

**(a) Dependency-chained work stays in ONE lane.** DC-2 and DC-3 become a single lane **`DC-23`**,
run in one worktree, **sequential inside**. They are not parallelised and they are not two
merges. This is the general principle the cut states once: *a dependency chain is a lane, not a
schedule* — splitting chained work across lanes buys no parallelism and costs a merge-order
constraint.

**(b) DC-1 EXCLUDES `CLAUDE.md` ENTIRELY.** DC-1's write-scope loses the file. This is what makes
the disjointness real rather than negotiated: DC-1 and DC-23 now touch **no common file**.

**(c) The VISION-line removals move.** `CLAUDE.md` `:39` (critical paths) and `:68` (living docs)
are removed **by DC-23, as its LAST act, conditioned on DC-1 being merged.** They are
VISION-retirement work, so they cannot land before DC-1 retires VISION — but they are CLAUDE.md
edits, so they must ride the CLAUDE.md lane. Putting them last in DC-23 satisfies both.

**Merge order:** `DC-1 -> DC-23`.

**Disjointness is RE-VERIFIED THROUGH `[#591]` AT FREEZE** — not asserted here. See CUT-5.

---

## CUT-4 · U-10 — DM-4 FAILS THREE BARS. RULED: do NOT freeze as written. Downgrade to Tier-L evaluation.

**The ruling.** DM-4 becomes a **Tier-L EVALUATION lane**, not a Tier-S build:

- **Runs on:** enterprise / cloud — off the operator's machine. (Written `Runs on:` and not
  `Substrate:` deliberately: this file is a RULING, not a lane contract, and
  `validate_substrate.declared_substrate` reads `**Substrate:**` as a declaration. A ruling that
  parses as a contract would be gated as one — which it was, on the first run of this cut.)
- **Act:** install `sqlite-vec` **plus a NON-REJECTED embedder** in a **scratch environment**.
- **Measure:** hit-rate versus `grep` on **20 real questions**, recorded.
- **ZERO repo dependency change this batch.** No `pyproject.toml` edit, no `uv.lock` edit, no
  `scripts/` producer. ADR-106 makes a dependency change its own gated act and this lane does not
  take it.
- **The Tier-S build rides the NEXT batch, on this measurement.** Evaluate before adopting is
  what ADR-112 Tier L means, and this is that evaluation.

**The rejected embedder is named in the lane brief, with the reason, so it is not re-tried
blindly.** `sentence-transformers` is on the decision tree's REJECTED list (with ChromaDB,
LanceDB, Mem0, Letta/MemGPT, Zep). The autonomy synthesis pairs `sqlite-vec` with **`model2vec`**
instead, and that is the non-rejected embedder the lane starts from. A lane that reaches for
`sentence-transformers` anyway has to say why in writing.

**Why this ruling and not a drop:** the substrate capability IS proved
(`enable_load_extension` works on this host — the Windows blocker does not exist), so the
evaluation is cheap and the question is live. What was never proved is the adoption, and the
brief's "proven under pinned uv" claimed it.

---

## CUT-5 · THE QUOTA PANEL — folded, not born.

**The ruling.** The quota panel folds into **HY-4** (the TRENDS burn-down panel lane) as a
**sub-deliverable**. **No new row, no intake, no ledger spend.** HY-4 already owns a panel-shaped
deliverable and already reads the trend store; a second panel is a second section, not a second
lane.

**Recorded honestly:** `[#615]` (MODEL ATTRIBUTION — the model+version commit trailer) remains the
**enabling row** for per-model attribution, and it is **NOT funded in this batch**. So the quota
panel HY-4 ships attributes **provider and credits** but **cannot attribute a lane to a MODEL**
until `[#615]` lands. That is a stated limit of the panel, and the panel says so in its own text
rather than rendering a column that looks whole and is not. **A partial series that looks
complete is worse than an absent one** — `[#615]`'s own words, applied to its own absence.

---

## CUT-6 · THE FREEZE GATE — six predicates

The freeze runs every contract through the `[#591]` substrate validator. PLAN.md measured **four**
live predicates and recorded that the brief's "predicate six" was really predicate five. The cut
resolves the numbering by naming what predicates five and six ARE:

```
1  substrate-no-live-verb              REFUSE   (live)
2  substrate-cloud-gate-dependent      REFUSE   (live)
3  substrate-offmachine-operator-path  REFUSE   (live)
4  substrate-second-local-writer       WARN     (live)
5  substrate-teardown-enum-coverage    REFUSE   (NEW — 0a)
6  substrate-lane-write-scope-disjoint REFUSE   (NEW — CUT-3(c))
```

**Predicate 5 (0a, TEARDOWN ENUM = LANE ENUM):** a contract naming a substrate whose lane branch
shape the batch teardown does not enumerate is REFUSED at freeze. This is the ADR-116-stranded-on-
`claude/lane-f` defect, made structural: `LANE_BRANCH_RE` matches only `worktree-lane-*`, so cloud
and codespace lanes are invisible to the exemption and to any teardown that iterates it.

**Predicate 6 (CUT-3(c), DISJOINTNESS):** two contracts in one batch whose declared write-scopes
intersect are REFUSED. This is what makes CUT-3 checkable instead of asserted — DC-1 dropping
`CLAUDE.md` has to be provable at freeze, not remembered.

---

## WHAT THE CUT CHANGES IN THE LANE LIST

```
DC-1   write-scope LOSES CLAUDE.md entirely.               (CUT-3b)
DC-23  NEW — DC-2 + DC-3 merged into one sequential lane.  (CUT-3a)
       Its LAST act is the CLAUDE.md :39 / :68 VISION-line removal,
       conditioned on DC-1 merged.                         (CUT-3c)
       Obsidian :40 / :77 deletion is unconditional.       (CUT-2)
DM-4   Tier-S build -> Tier-L EVALUATION, cloud, scratch env,
       zero dependency change, model2vec not sentence-transformers. (CUT-4)
HY-4   GAINS the quota panel as a sub-deliverable, with the
       [#615] attribution limit stated in the panel itself. (CUT-5)
DC-5   unchanged, and win-tooling's template precedent is AFFIRMED. (CUT-1)
```

**Committing lanes after the cut: 15** (was 16 — DC-2 and DC-3 became one).

## WHAT THE CUT DOES NOT CHANGE

- Tier (A) is already dispatched and is untouched by every ruling above.
- No backlog row is born or closed by this cut. `[#615]` stays open and unfunded, by decision.
- Intake #62 stays `DRAFT`. The `.CLAUDE GOVERNANCE MODEL` is filed, not ratified.
- U-2, U-3, U-5, U-9, U-11, U-12, U-13 are not re-opened; they were reported, not blocking.
