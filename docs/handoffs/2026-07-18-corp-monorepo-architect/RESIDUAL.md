# Residual — 2026-07-18-corp-monorepo-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **architect** (§13) — planning / decomposition posture; the session's WORK is **product**. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is EMPTY (cold handoff).** ANSWERS committed empty; the incoming §13(d) operator-context beat fires **FULL**.

---

## §1 — The headline: the plan is encoded; the architect resumes decomposition at the E5-build / SIM-1-gap frontier

**The product plan is fully in-repo and the last window CLOSED cleanly.** `witnessed` (READ-ONLY, at derivation): corp `main` is **clean and in sync with `origin/main`** — no unmerged product branches, one already-merged straggler (`docs/2026-07-18-manifest-doctrine-closeout`, deletable on the operator's OK). The A3 target-architecture ruling (R1–R10, `docs/audits/2026-07-17-a3-target-architecture-ruling.md`) still governs; the integration-protocol ruling is **CLOSED**; the **NOT-list (no microservices, no service mesh, no message bus)** is binding at solo-operator scale.

What a fresh architect chat lacks — and the ONLY thing this residual carries — is the **entry point + the decomposition frontier + the design "why,"** none of which the repo re-narrates:

- **Entry point.** The corp **execution charter** `docs/audits/2026-07-17-execution-charter.md` is still the single consolidated reading map (its §2 reading map points to every canonical doc). Read it first; everything below is a pointer INTO it, not a copy.
- **Role split (does not live in the repo).** This browser chat is the **TECHNICAL ARCHITECT** (Layer-1, no file access) — it decomposes the next frontier into a task-graph, holds the whole-system view (A3 + `ARCHITECTURE.md`), and reviews each arc's plan before execution (one plan-review output-contract form: the exact CC option / paste-ready feedback / `approve`). The incoming Claude Code session is the **executor** (Layer-3, holds the tree). The architect does **not** execute. Methodology questions route to the **hub** `.dev-knowledge` (corp is A0-closed), **not** this chat.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or region text — those are the probes' live answers.

---

## §2 — Pending / shipped this window (pointer, not re-narration)

**SHIPPED since the last handoff (2026-07-16→18; detail lives in the corp `JOURNAL.md`, not recapped here):**
- **Arc-B signed deletions** `#19–#23` — MERGED+PUSHED, close-out package delivered (`corp index rebuild`: B2 facts residue cleared, `facts_count=0`).
- **Arc-C Wave 1 canonical homes** `#25`/`#26`/`#27` — MERGED (LLM-JSON→`schema.utils`; frontmatter→`vault_io`; a new `schema/model_pricing.py` built from the live per-provider dicts). **Deletion-candidate lists** for the now-unused old copies live in those commit bodies → they **feed the NEXT signed deletion manifest** (Arc-C wave 2). The new `docs/templates/deletion-manifest-template.md` (closing-sweep) codifies the manifest doctrine: column-granularity consumer enumeration before a KILL; runtime-claim kills default PROPOSED-GATED.
- **E5 registry foundation design** — Lane B doc MERGED (doc-only, **no task closed**): `docs/intake/2026-07-17-tech-e5-registry-foundation-design.md` (intake-id 16). Key corrected semantics: **`#35` is the `ContentRegistry` routing gate, not the FR-10 registry** — the FR-10 URL/source registry is `#38`/`#40`; build order **`#35→#38→#40→#36`**. Open design decision points D1–D5 + Graph consent live in the design's §8.
- **Night process audit** (unattended, 2026-07-17→18) — `docs/audits/2026-07-18-process-audit.md`. **The spine WORKS end-to-end** (ingest → deep knowledge note → cited RFP draft, ~$0.045 surfaced). It surfaced a **SIM-1 gap list** (the real product-quality frontier, see §4): retrieval is **metadata/title-only** (no body FTS), the **facts pipeline is absent** (`facts_count=0` at all consumer sites), **ingest hard-crashes** on a fresh env without `<mywork>/.corp/content_registry.yaml`, and the **project↔vault link + client propagation** is missing. Two DISCLOSED read-only real-MyWork leaks (F18 `project_resolver` roots, F26 `com` lane) — no writes, SHA-256 baseline held.

**PENDING — no unmerged product branches.** `witnessed`: corp `main` carries no open feature/fix lanes at derivation (the two worktree lanes were integrated + torn down 2026-07-17). The only non-`main` branch is the merged straggler above.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — the architect's job this session is to sequence and decompose the next product arc.** Two candidate frontiers are both ready and the ordering is the live architectural call (§13(d) captures the operator's priority):

1. **The SIM-1 gap-fill "day-arc"** (from the night audit). The 07-18 JOURNAL is explicit: *"the day-arc launches as a FRESH executor session on the senior's formal prompt (authored from the HUB session, not here)"* — i.e. **this architect chat authors that executor prompt.** The ranked queue: (1) ingest content-registry fallback+bootstrap [F1]; (2) note-body FTS **or** wire the facts pipeline [F6/F7]; (3) project↔vault link + client propagation [F16/F9]; then the missing **Content-Manifest producer** (SIM-1's one absent output — the T6 corp↔consumer seam). SIM-2: the `data/kb` RFP producer [F11], CKE tier/schema drift [F21/F22].
2. **The E5 registry BUILD** (`#35→#38→#40→#36`) — the design is ratified and merged; the build arc executes from it. **Graph API consent gates `#36`/`#40` live resolution** (operator queue, below).

**The R10 "why":** after the F0/E1–E2 substrate, the **knowledge loop (E5/E6) takes precedence over the RFP rewrite (E4)** — a conscious, recorded deviation from the intake's "build before gap-fill" order; the BACKLOG sequences themes E1→E2→E3→**E5→E6**→E4→E7 accordingly (theme *ids* keep identity, theme *sequence* carries priority). The SIM-1 gaps sharpen this: the spine runs, but retrieval quality and the facts pipeline are the gating weakness for the RFP output — which is exactly why the knowledge loop is elevated ahead of the RFP rewrite.

**CLOSED — do NOT re-open (charter §3, PROBES P4):** CKE is a subprocess with an explicit contract (R2, one invoker); accessors resolve through config incrementally (R6); the corp↔consumer seam is the T6 Content Manifest; seam contracts are guarded by N2-class seam tests. If an arc's plan reaches for an infrastructure tier (a service, mesh, or bus), the architect rejects it — a violation at 3-RFPs/month scale.

**Operator queue (off-repo — the §13(d) beat captures it live; charter §5 is the verbatim list):** Graph API consent (unblocks scout `#36` + `#40` + X1), the absent vault git remote, 4 credential rotations, final backup-zone names, the ADR-35 amendment decision (backup leg-2 → personal OneDrive, `#18`), the T6-D4 SharePoint confidentiality push, and the E5 design's D1–D5 decision points. These gate specific tasks and only the operator can close them.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (E1–E7 product story-map in R10 priority sequence, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2), the live in-progress branches (`git branch -v` — none open at derivation; P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**
