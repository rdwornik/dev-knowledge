---
intake-id: 64
status: REJECTED
origin: batch-E tier-(A) lane a7 (agy admission + quota visibility), harvested 2026-08-31; filed as a SEED by the night orchestrator 2026-09-01 per the night protocol's "proposals land in docs/intake as status SEED" and ADR-111's only path from a CANDIDATE
consumed-by:
reason: the provider registry stays thin identity-only (gate-ruled); a quota locator belongs in the capability profile, not in the registry
---

# A machine-readable quota locator, and whether the provider registry is allowed to hold one

<!-- class: tech (registry-schema question) · status: SEED — a pre-intake candidate, not yet
worked by a functional conversation. SEED BINDS NOTHING. -->
<!-- origin: A7 census, 2026-08-31 -->

> **SEED BINDS NOTHING.** This records a candidate the A7 lane was contractually forbidden to
> file itself — *"a BIRTH proposal, not a repair — and per ADR-111 / Z-G1 it is a CANDIDATE,
> which this lane may draft and may not file"*. It authorises no schema edit and no registry
> write. Everything below is A7's finding restated for triage, plus the counter-precedent that
> makes it a real question rather than a repair.

## Problem / motivation

**The "quota-source field" does not exist and never did.** A7 re-ran the search at HEAD and
confirms AUT-R4a's earlier finding: `quota`, `quota_source` and `quota-source` appear in exactly
four places repo-wide, all of them **audit prose about the field's own non-existence** — zero
code, zero YAML, zero schema. So every prior reference to "the quota-source field" is a reference
to nothing, and the correction stands at HEAD.

What the absence costs, concretely: HY-4's quota panel (folded into the trends dashboard by
ruling CUT-5 and merged 2026-09-01) can derive PROVIDER IDENTITY live but must render CREDITS as
a **named absence**, because no store in this repo can answer "how much of this plan is left".
The panel says so in its own text rather than showing a column that looks whole. That is the
right behaviour for a surface with no source — and it is also the shape of the gap.

**If this stays unaddressed:** the operator keeps reading quota out of vendor UIs by hand, every
future panel repeats the named-absence workaround, and each audit that mentions "the quota-source
field" re-creates the impression that a surface exists.

## Scenarios (+1 view)

- *As the operator*, I open the trends dashboard mid-window and want to know which provider is
  closest to its ceiling before dispatching four more lanes. Today the panel names the limit
  instead of answering; I open two vendor consoles by hand.
- *As a lane*, I am routed to a provider by `ecosystem/routing-table.yaml` and have no way to
  know that provider's plan is nearly spent. The routing decision and the budget it consumes are
  recorded on different surfaces, one of which is a browser tab.
- *As an auditor*, I read `provider-registry.yaml` and find quota facts already present — the
  copilot-enterprise billing note and the google/antigravity notes — **as prose comments**,
  because the schema refused them as data.

## Open questions — the ones that decide this

1. **Is the provider registry allowed to hold a quota locator at all?** A7 argues it should be:
   quota is metered per ACCOUNT/PLAN rather than per model id, so it belongs on the PROVIDER row;
   `substrate-registry.yaml` disclaims provider facts, and Z-G3 scopes `routing-table.yaml` to
   which role runs on which CLI. **THE COUNTER-PRECEDENT IS TWO DAYS OLD AND IT IS THE STRONGEST
   ARGUMENT AGAINST:** on 2026-08-29 (`86bed82`) a rich copilot-enterprise entry was REFUSED by
   this same schema and its content went to a comment plus L0 `~/.claude/ROUTING.md`, with the
   commit recording *"the registry is a provider/CLI identity surface"*. A `quota_source` field
   cuts against that ruling-in-practice, and A7 says outright that the operator or architect
   should settle it before anything lands.
2. **Would the field be a LOCATOR or a VALUE?** A locator (where to look) is stable and cheap; a
   value is stale the moment it is written and has no producer here.
3. **What does the schema cost?** `ecosystem/schema/provider_registry.py` sets `extra="forbid"`,
   deliberately — *"forbidding extras converts a typo into a blocked commit and makes 'add a
   field deliberately' a real act with a real diff"*. So this is a schema version bump
   (A7 drafts `SCHEMA_VERSION 1.0.0 -> 1.1.0`, additive and optional, invalidating no existing
   row) plus a validator decision about what may be asserted.
4. **Does an OPTIONAL field actually change anything?** `role_admission` is the precedent for
   optional-and-defaulted, and a field that is absent everywhere is a field nobody reads.

## What this SEED deliberately does NOT do

It does not propose a schema diff for adoption, does not touch `ecosystem/provider-registry.yaml`,
and does not re-open the agy admission question — A7's separate finding there is that **nothing
in `tasks/` authorises an admission act today**, and the rerun that would settle it is itself
blocked on an untriaged intake. Full evidence, including A7's draft YAML shape and its
registry-choice reasoning: `docs/audits/2026-08-31-technical-agy-admission-and-quota-visibility.md`.

---

## RULED 2026-09-01 — NO, as framed. The need survives; the home does not.

> **Operator ruling 5.** *"NO — the provider registry stays thin identity-only (gate-ruled); quota
> locators live in the capability profile (`ROUTING.md` / its L0-derived copy). Amend #64."*

**The counter-precedent this SEED carried is the one that decided it**, which is the reason it was
carried rather than left for the reader to find. `86bed82` (2026-08-29) refused a rich
copilot-enterprise entry on exactly this ground, and the registry's own comment block states the
rule in its own words: *"this registry is a thin provider/CLI identity surface and its schema
forbids the extra fields. The measured capability profile … and the BILLING VERDICT live in
`~/.claude/ROUTING.md`, which is L0 and outside this repo."* **The schema's `extra="forbid"` was
not an obstacle to route around — it was the rule already saying no.**

**What is NOT rejected: the underlying gap.** A7's finding stands in full — `quota`,
`quota_source` and `quota-source` appear in four places repo-wide, **all of them prose about the
field's own non-existence**. HY-4's quota panel still renders credits as a NAMED ABSENCE, and that
remains the correct behaviour for a surface with no source. What the ruling settles is **where a
locator would live if one is ever written: the capability profile, not the registry.**

**Terminal by the enum** (`REJECTED (reason, kept)`) — rejections are knowledge, so this doc stays
rather than being deleted, and relocates byte-identical to `docs/intake/archive/` per the
2026-07-22 archive-inside-each-folder ruling.
