# Residual — 2026-07-17-corp-monorepo-executor-product-execution — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **execution** (§13); the browser is the SENIOR architect who reviews plans, the incoming chat is the executor. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is EMPTY (cold handoff).** ANSWERS committed empty; the incoming §13(d) operator-context beat fires **FULL**.

---

## §1 — The headline: the plan is encoded; the executor needs the entry point + the supervision loop

**The product plan is fully in-repo.** The A3 target-architecture ruling (R1–R10), the SIGNED Arc-B deletion manifest, the ADR pack (33–36), the intake +§9, the T6 brief, the FR-13 reconciliation, and the product-axis `BACKLOG.md` all landed 2026-07-16/17. What a fresh executor chat lacks — and the ONLY thing this residual carries — is the **entry point + the role split + the supervision loop**, none of which the repo encodes:

- **First-read pointer.** The single entry point is the corp **execution charter** `docs/audits/2026-07-17-execution-charter.md`. Read it first; it consolidates by pointing to every canonical doc (its §2 reading map). Everything below is a pointer INTO it, not a copy of it.
- **Role split (does not live in the repo).** This browser chat is the **SENIOR architect** (Layer-1, no file access); the incoming Claude Code session is the **executor** (Layer-3, holds the tree). The executor runs `BACKLOG.md` top-down; the senior architect **reviews each arc's plan before execution** and emits exactly one plan-review output-contract form (the exact CC option / paste-ready feedback / `approve`). The browser does **not** execute.
- **Supervision loop (does not live in the repo).** Per arc: executor drafts the plan → operator relays it to the senior architect → architect reviews and returns one output-contract form → executor executes only on `approve`/selection → gates-green `--no-ff` merge → push without asking (standing rule). Deletions ONLY per a signed manifest row.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or quote text — those are the probes' live answers.

---

## §2 — Pending / shipped this window (pointer, not re-narration)

**PENDING — the executor's first three moves (charter §4; do NOT re-plan here, submit each to the senior architect first):**
- **Arc-B execution** — the five signed batches (BACKLOG `#19–#23`). The execution prompt is in the operator's Downloads (`2026-07-17_PROMPT_arc-b-execution.md`), named in charter §4: one revertable commit per batch; Batch 2 repoints `search_facts`→notes_fts then `corp index rebuild`; Batch 3 witnesses the dead-lane boundary before cutting; Batch 4 fires only on the recorded zero-use word.
- **Arc-C wave 1** — the canonical-home unifications not gated on the config capstone: LLM-JSON→`schema.utils` (#27), frontmatter→`vault_io` (#26), the models+pricing registry BUILT from the live per-provider dicts (#25).
- **E3 / E5** in disjoint worktrees where parallelizable.

**Three hard `depends-on` edges only:** `#29` after `#19–#23`; `#36` after `#35`; `#53` after `#29` (the R9 docs-once gate). All other ordering is R10 theme sequence, not a hard edge.

**SHIPPED (recent, by reference — detail lives in the corp `JOURNAL.md` 2026-07-16/17, not recapped here):** the architecture ground-truth audit + Codex edge-diff; the Arc-B manifest PROPOSED→SIGNED; ADR-33..36 ratified; the intake §9 addenda + FR-13 reconciliation + T6 brief; the A3 ruling codified in-repo; the product-axis BACKLOG rebuild; and — this session — the execution charter + this handoff bundle. This is a **map** — the corp `JOURNAL.md` is the record.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — resume PRODUCT execution.** Open the charter, then Arc-B. The R10 "why": after the F0/E1–E2 substrate, the **knowledge loop (E5/E6) takes precedence over the RFP rewrite (E4)** — a conscious, recorded deviation from the intake's "build before gap-fill" order; the BACKLOG sequences themes accordingly (theme *ids* keep identity, theme *sequence* carries priority).

**The integration-protocol ruling is CLOSED — do NOT re-open it (charter §3, PROBES P4):** CKE is a subprocess with an explicit contract (R2, one invoker); accessors resolve through config incrementally (R6); the corp↔consumer seam is the T6 Content Manifest; seam contracts are guarded by N2-class seam tests. **NOT-list: no microservices, no service mesh, no message bus** — an infrastructure tier is a violation at solo-operator scale (3 RFPs/month). If an arc's plan reaches for one, the senior architect rejects it.

**Operator queue (off-repo — the §13d beat captures it live; charter §5 is the verbatim list):** Graph API consent (unblocks scout #36 + X1), the absent vault git remote, 4 credential rotations, final backup-zone names, the ADR-35 amendment decision (backup leg-2→personal OneDrive, #18), and the T6-D4 SharePoint confidentiality push. These gate specific tasks and only the operator can close them — the executor does not.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (7 themes E1–E7 / 9 stories / 51 tasks, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2), the live in-progress branches (`git branch -v`; P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**
