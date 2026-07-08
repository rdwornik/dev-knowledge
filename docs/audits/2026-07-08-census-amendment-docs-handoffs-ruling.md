# Census amendment — `docs/handoffs` child-repo target ruling (2026-07-08)

<!-- scope: meta -->

> **Amends** `docs/audits/2026-07-08-fleet-consistency-census.md` — Part 1 taxonomy
> item **f.6 / §B needs-ruling item 6** ("ai-council docs/ taxonomy partial — no
> `docs/handoffs/` or `docs/intake/`; intended divergence vs drift?").
>
> The census runs in **frozen-contract mode** ("forks are recorded, never resolved
> unilaterally") and is an **immutable audit** (CLAUDE.md §5). This ruling therefore
> lands as a **superseding amendment file**, not an in-place edit of the census.

## Provenance

The census flagged ai-council's absent `docs/handoffs/` as a NEEDS-RULING fork. The
ai-council Wave-1 onboarding pilot independently re-surfaced it as **gap-note G3**
(`../ai-council/docs/intake/2026-07-08-runbook-gap-notes.md`): the runbook's per-repo
`docs/` target named `docs/intake` **+ `docs/handoffs`**, which conflicts with the
handoff-centralization ADRs. The pilot **created `docs/intake/` only** (operator GO)
and **did not** create `docs/handoffs/`, routing the conflict back to the hub as a
NEEDS-RULING.

## Ruling (architect-ratified 2026-07-08)

**ADR-60 / ADR-42 WIN.** Child repos do **NOT** create a local `docs/handoffs/`.
Handoffs are centralized in `.dev-knowledge` — this is **intended divergence, not
drift**. The census f.6 / §B-6 target is **amended to `docs/intake`-only** for child
repos; `docs/handoffs/` is **removed** from any child-repo `docs/` target. The ADRs
are **not** amended (the census target was the drifted surface, not the doctrine).

## Basis (verbatim)

- **ADR-60** (docs/ Folder Taxonomy — Semantic Roles):
  - "`handoffs/` | OUTPUTS — ALL handoff bundles (centralized canonical home; child
    repos do NOT carry `handoffs/`)"
  - "Child code repos do **not** carry `handoffs/`, `research/`, or
    `council-questions/`. Handoffs centralize in `.dev-knowledge`."
- **ADR-42** (Handoff Format v3.0): "All handoffs in
  `.dev-knowledge/docs/handoffs/{date}-{slug}/`".
- **ARCHITECTURE.md** (Ch4 Distribution): child code repos do not carry a handoffs
  folder; the hub is the canonical home.

## Effect

- ai-council's absence of `docs/handoffs/` is **CONFORMANT** (intended divergence);
  no ai-council action is owed on this axis.
- The child-repo `docs/` universal target is **`docs/{decisions,audits,archive}` +
  `docs/intake/`** (the latter propagated at deploy per **[#280]**); **not**
  `docs/handoffs/`.
- Any runbook / onboarding surface that names `docs/handoffs` as a child-repo target
  is stale and must read `docs/intake`-only. (Runbook copy-fix, if any, rides the
  Wave-1 onboarding arc.)
- The census's OTHER §B forks are unaffected by this amendment.

---

**Compiled by:** CC (Opus 4.8), QA-intake consolidation session, 2026-07-08.
Read-only re: the census (byte-untouched); this file is the superseding record.
