# BATCH F — TERRA PRE-MERGE TALLIES (amendment 2), running record

- **Class:** verification · **Date:** 2026-09-01 · **Arc:** `[#614]` · **Consumed by:** the batch-F close packet
- **Author:** CC (Opus 5, integrator seat) · **Status:** RUNNING — appended per merge, landed once

> Amendment 2 of the batch-F manifest ratified a terra pre-merge review on **every** lane,
> including lanes that changed no code: *"A CLEAN pass IS a review."* This file is that record.
> **Refutations are recorded as prominently as acceptances** — the amendment's own words.
>
> Command shape: `codex exec -m gpt-5.6-terra --sandbox read-only`, scope stated INSIDE the focus
> prompt (`--base` and a prompt are mutually exclusive).

## Queue worktrees (not batch-F lanes, but merged in this window)

### dashboard-home-ruling-filing → merged `3a4066eb`

```
VERDICT: CLEAN PASS (a) real defects: 0   (b) recorded tensions: 0
Scope reviewed: docs/intake/ filings + generated README.md + manifest.json
Evidence: "README.md and manifest.json agree with all 57 intake frontmatters;
          the #66 DRAFT->READY transition is correctly reflected."
```

Integrator note: the merge carried two conflicts, both resolved by **union, not side-pick** —
`tasks/615` kept HEAD's two added audit refs AND the branch's PANEL HOME RE-POINTED ruling;
`docs/intake/manifest.json` is generated and was resolved by **regeneration**, not by hand.

### boot-r1-survey → merged `3fe5db59`

```
VERDICT: NOT CLEAN -- (a) real defects: 2 (both HIGH)   (b) recorded tensions: 1
```

**(a) HIGH — the "BUILD NOTHING" verdict overclaims its evidence.** §3.1 / §8. The
single-project study supports *"criteria importance can be stage-dependent"*; it does not
support *"directly contradicts"* WSJF/RICE, nor that the incumbent beats every surveyed
alternative. The closed verdict is stronger than what is cited.

**(a) HIGH — §7.3 and §9.1 contradict each other, and the pin is the casualty.** The measured
result establishes that a **naive top-K slice collides**. It does NOT establish that contention
*"inverts"*, is generally harmful, or should be absent from batch selection — under first-seen
disjoint selection `rank_key` still orders groups by contention. The identical width-7 output is
a **local** result, not a general property. So §9's instruction to *import* `rank_key`
contradicts §7.3's conclusion to *exclude* contention.

**(b) TENSION — "decisive" vs `n=1`.** §7.2 calls the one-batch 0-of-7 result *decisive* while
§11 correctly records it as `n=1` awaiting retrospective replication. The limit IS recorded; the
stronger wording should not be the thing that carries the §9 pin.

**INTEGRATOR DISPOSITION.** The artifact LANDS — its survey, its fetch ledger and its negative
results are the value, and they are unaffected. What does **not** carry forward unqualified is
its §9 pin, because **L2's scoring seam was to consume exactly that pin.** The seam is therefore
recorded as **CONSUMED-WITH-QUALIFICATION**: reuse `gen_task_tree.rank_key` as an import (that
much is agreed by both sides), but the §7.3 "contention inverts" claim is **not** ratified and
must not be built on until replicated at n>1. Carried into the close packet and the residual.
