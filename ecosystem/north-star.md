# NORTH STAR - the arc set, in dependency order

> **GENERATED - do not hand-edit.** Regenerate:
> `uv run --locked python scripts/gen_north_star.py --write`
>
> The arc names, their order, their done-when and their starting contract are DECLARED in
> `scripts/gen_north_star.py` - architect judgments, not derivable. Every member row,
> status and count below is DERIVED from `tasks/` at generation time, so this file cannot
> drift from the backlog the way a hand-written roadmap does.

Open rows: **163** of 218 manifest-referenced (**55 deferred**).

**Deferred is shown deliberately.** On 2026-08-30 an intake's fold target was found to
have gone deferred underneath the instruction that cited it, unnoticed, because nothing
watches a blocker's status (`[#624]`). A deferred row is not a closed row and a plan
resting on one is a plan resting on nothing.

**Read the ORDER as binding.** Each arc names what blocks it, and the blocks are not
preferences: an arc worked ahead of its blocker is work optimising against no signal.

## 1. THE METRIC - a reward function, before anything that would consume one

- **Blocked by:** Nothing. This is the head of the sequence.
- **Done when:** A rule-adherence harness scores the instruction corpus, and a deliberately weakened instruction set FAILS while the intact set passes. Until that discriminates, every downstream arc is optimising against no signal.
- **First frozen-contract candidate:** intake #35 PROPOSED ROW R3 (promptfoo) - decided in principle, NOT born; blocked on one ruling about its fold target, since both [#491] and [#492] are deferred today
- **Themes (the selector):** `[E7] Tooling & evaluation`
- **Open rows in scope:** 47 (P1 9 / P2 27 / P3 11)
- **Deferred in scope:** 9

## 2. AUTONOMY ORGANS - what fired, how often, and did it help

- **Blocked by:** THE METRIC. Every absent property here is downstream of a measurement that does not yet exist - four AUT lanes reached that conclusion independently, from subjects that never touch.
- **Done when:** One surface answers what has actually fired, how often, and whether it helped - for organs, for landed rules, and for the LESSONS to rules to gates conversion.
- **First frozen-contract candidate:** docs/audits/2026-08-30-technical-autonomy-decision-tree.md - ten parked items, each carrying the trigger that releases it
- **Themes (the selector):** `[E3] Lessons feedback loop`, `[E4] Decision management`
- **Open rows in scope:** 10 (P2 5 / P3 5)
- **Deferred in scope:** 5

## 3. DOCTRINE CONSOLIDATION - one audience, one owner, budgeted in bytes

- **Blocked by:** Nothing - batch D landed its first wave: README recreated, CLAUDE.md re-genred, codex/ universalised.
- **Done when:** Every boot-time surface is budgeted in BYTES with a gate, and every canonical doc has exactly one owner and one audience.
- **First frozen-contract candidate:** docs/audits/2026-08-29-technical-batchd-launch-contracts/ - the seven frozen contracts; lanes b, c and h landed
- **Themes (the selector):** `[E5] Canonical-file integrity`, `[E1] Handoff continuity`
- **Open rows in scope:** 32 (P1 2 / P2 19 / P3 11)
- **Deferred in scope:** 5

## 4. DEPLOYMENT WAVE - the fleet carries what the hub rules

- **Blocked by:** DOCTRINE CONSOLIDATION - shipping a corpus mid-re-genre ships the churn rather than the doctrine.
- **Done when:** Every ADR-104 member carries the ruled corpus at a declared version, and fleet_parity reports zero undeclared divergence across them.
- **Ships in this order:** hub -> monorepo -> ai-council -> win-tooling (operator-ruled 2026-08-31, batch E CUT-1: this is the MIGRATION order, for the consolidated-doctrine corpus). win-tooling being LAST here does NOT roll back its status as the FIRST INSTANTIATED consumer - the floor stays, and DC-5 instantiates ai-council from win-tooling's template. SUPERSEDES the HERMETIZATION order recorded on this field 2026-08-31 (batch E -> engine ratification -> win-tooling full cycle -> monorepo -> ai-council), which stated the INSTANTIATION sequence, not the migration one. Full ruling: docs/audits/2026-08-31-technical-batche-launch-contracts/CUT.md CUT-1.
- **First frozen-contract candidate:** intake #38 (the root-contract) - amended 2026-08-30; R18 stays parked on tested conditions rather than on silence
- **Themes (the selector):** `[E6] Cross-repo universalization`, `[E9] Fleet Desired-State System (North Star)`
- **Open rows in scope:** 13 (P2 6 / P3 7)
- **Deferred in scope:** 11

## 5. LEARNING LOOP - the repo as its own training signal

- **Blocked by:** THE METRIC, then AUTONOMY ORGANS. A loop with no reward optimises nothing - WRONG ORDER, not wrong tool.
- **Done when:** A per-repo layer turns the repo's own events into a boot-surface signal that changes what the next session does, with the hub shipping the MECHANISM and never the managed state.
- **First frozen-contract candidate:** intake #63 (universal per-repo learning loop) - DRAFT, evidence-gated on AUT-R3
- **Themes (the selector):** `[E2] Enforced governance`
- **Open rows in scope:** 48 (P1 3 / P2 35 / P3 10)
- **Deferred in scope:** 25

## What this view deliberately does NOT do

It does not rank rows inside an arc, and it does not promise that every open row belongs
to an arc. A row outside every theme selector above is not lost - it is simply not part of
the North Star sequence, and `BACKLOG.md` remains the complete list. Claiming otherwise
would make this file a second backlog, which is the duplication this repo spends most of
its enforcement budget preventing.
