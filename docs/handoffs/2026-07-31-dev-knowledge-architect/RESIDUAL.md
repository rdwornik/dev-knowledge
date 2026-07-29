# Residual — 2026-07-31-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**All standing, all dispositioned — one row added this window, none left undispositioned.** Read
`ecosystem/disposition-register.yaml` for the live set; re-derive the verdict via P7.

- **Standing families, unchanged:** the `no_ff_merges` legacy-spine rows (June commits — never
  rewrite them), `reconciled_versions` (ref `#335`), the `doc_rot` history-accretion rows
  (`#344`, `#421`, `#422`, `#332`, `#278`), and the `undeclared_edges` `#241` family.
- **NEW this window — one row:** the `#241` family gained a fourth member for the intake-21
  orientation snapshot ingested this arc. Dispositioned rather than declared because a dated
  orientation snapshot is definitionally not coupled to a spec version; a `reconciled_with` there
  would assert a coupling the doc is designed not to have. **Its shelf-life asks a real question**
  rather than waiting for an event: unlike the proposal rows, which self-clear when intake 18
  ratifies or retires, this edge has no such trigger — 08-26 decides whether an archived snapshot
  should carry a live disposition at all.
- **Cross-repo, not ours:** the `fleet_parity` consumer root-sweep row (ref `#430`) is
  pre-existing and reproduces with the consumer on bare `main`; it is not this window's work.
- **Cleared this window:** one self-induced `doc_rot` row was fixed at source rather than
  dispositioned (a row authored over the cap, compressed back under it). Self-induced bloat is not
  a disposition candidate — see the LESSONS entry filed 2026-07-30 on pre-write measurement.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail is in `JOURNAL.md` 2026-07-30 (a) / (b) / (c) — this is the map only.

- **`[#435]` CLOSED** — intake #18 (handoff-process v6) stewarded to ratification; all 11
  amendments A1–A11 ruled, intake left PROPOSED → ACCEPTED. Record:
  `docs/audits/2026-07-30-technical-intake18-ratification-record.md` (+ its dated amendment
  marker). Retired per ADR-107 §6.3 — file retained, terminal status.
- **`[#446]` FILED** — the §B(b) one-round-trip boot build, carrier of the v6 bump. Not started.
- **`[#447]` FILED** — self-referential gate family, two instances witnessed.
- **RULING-W `.vscode` W1 EXECUTED** across all three repos (the 2026-07-29 ruling, previously
  executed nowhere): corp gained the boundary decoration, all three `.vscode` declarations
  re-dated off the 2026-08-13 lapse. Record:
  `docs/audits/2026-07-30-technical-vscode-w1-execution-record.md`.
- **v6 spec DRAFT produced** (sol, adversarial derivation) —
  `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md`. **NOT canon**; the spec version is
  unchanged and the bump rides `[#446]`.
- **intake #21 INGESTED** — the browser-seat orientation snapshot, with a delta table heading it.
- **3 LESSONS entries** + the RM-1 order-convention sweep completed in PLAYBOOK Ch6.
- **Global core-invariants #5 executed** — branch grammar widened to the ratified lane-prefix
  enum (off-repo file; its evidence is the amendment marker + JOURNAL).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The frontier is `[#446]` — the §B(b) one-round-trip boot build — consuming the sol draft as its
named input, then `[#382]`.** The pull-forward of `[#382]` was offered and **declined**; the order
stands. The draft is at `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md` and is explicitly
**not canon** — it was produced adversarially over a closed five-file input set and verified on
three legs (coverage / boundary / anti-bluff fidelity), which is exactly why it is safe to build
from and unsafe to cite as doctrine.

**Its 7 OPEN questions are the build's FIRST rulings, in this order.** The producer flagged them
rather than resolving them by fiat, so each is a genuine decision the build cannot start without:

1. what command name exposes the one-round-trip boot;
2. P0a/P0b/P0c's exact source locators, commands, and honest-narrowed assertions;
3. what two values P3 compares, and what PASS is;
4. the `HANDOFF_BOOT.md` numeric byte budget — A10 cannot close on a placeholder;
5. RM-8's exact targets and diagnostic;
6. the types, defaults, CLI mapping and interaction of `main()`'s `repo_root` / `cross_repo`;
7. what tokenizer behavior and acceptance test constitute the `[#421]` absorption.

The design constraint that governs all seven: **the reshape moves who ferries the evidence, never
what is proven.** The §5 anti-bluff contract survives verbatim in the draft; any answer that
weakens a probe to make the single evidence block tidier has mistaken the goal.

**The 2026-08-26 cluster — deferred by decision, not dropped.** It is now four things (the drain
slice · the 26-row D-queue · `[#364]` 4(a) plus the disposition reviews · the `.vscode`
mechanism-DATE selection), and it is heavy. **Whether it splits is the FIRST ARCHITECT CALL WHEN
08-26 PLANNING OPENS** — made before that session arrives, not at its door. **The
§3.2-vs-`[#364]`-4(a) reconciliation is THAT PLANNING'S ENTRY GATE:** intake #17 §3.2 declares the
`doc_rot` cap raised 1200 → 1597 as adopted doctrine while the `[#364]` matrix recommends 4(a) and
"leave both cap legs unchanged" — two rulings in direct conflict, neither executed, and neither
document cites the other, so the conflict is invisible from either side's own checklist. Build
neither until it is reconciled.

**Riders.** U6(a) — the intake #19 §B standing night-batch section + ADR-105 activation record —
stays **DEFERRED**, trigger: the next night-batch request. U6(b) — standing closure delegation, an
ADR-70 amendment — was **NOT ADOPTED**; closures remain per-batch operator words, and its trigger
is **spent and reset**, so a future `/review-closures` must not re-raise it as pending.

**Closure-deferred — seven rows presented and ruled STAYS-OPEN this window**, each on its own
Done-when, not on inattention: `[#441]` (the ADR-61 "one launch test, not two" leg is unrecorded),
`[#446]` and `[#447]` (nothing built yet), `[#421]` (absorbed as a leg of `[#446]`, explicitly *not*
killed — closing it standalone would contradict `[#446]`'s scope), `[#422]` (detector unbuilt),
`[#445]` (its target is global infra, gated by core-invariant #6), and `[#433]` (not
re-adjudicated by standing ruling; ADR-107 §6.3 still self-declares Obligation 3 undischarged).

**One open judgment worth the architect's eye:** the closure detector is in a degenerate state —
its window has ratcheted back over nearly the whole history because pending proposals accumulate
unchecked, so almost every open row matches something and the STRONG tier is empty. That is the
open `[#277]`. Until it is repaired, every closure is effectively a manual adjudication, which is
survivable but means the "ready-set" half of the arc-exit test cannot mechanize.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
