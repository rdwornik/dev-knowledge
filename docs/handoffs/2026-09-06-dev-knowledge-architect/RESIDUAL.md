# Residual — 2026-09-06-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)
- `funnel_coverage` (reads docs/audits/ disposition coverage)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
Of the NEW-and-undispositioned organs listed above, `consumer_at_landing` is a **DECISION, not a
defect** — and the distinction is mechanical rather than a matter of judgment about effort. That
check asks whether a *governance POOL* surface cites an artifact. `docs/audits/` is excluded as a
citer by design, with one narrow carve-out opened by operator ruling: a batch manifest, and each
manifest's `closed_by:` target. So an artifact dispositioned in a ledger row can sit dispositioned
and unconsumed at the same time, permanently, without anything being left undone. Clearing it needs
a POOL-SIDE citer — a different act on a different surface — and that act wants a ruling, because
the obvious home would bloat a row already dispositioned for length. Everything else in the list is
a defect or a calendar, not a decision.

Do not read this as a verdict on the gate's state; `PROBES.md` re-derives that live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` encodes the detail and `BACKLOG.md` is the spec.

- **Batch R5P — CLOSED.** Its close packet and two appended errata are in `docs/audits/`; the
  errata are appended rather than edited, because the packet was on `main` and therefore immutable.
- **Batch H0-PREP — CLOSED this window**, by a packet written on the joint judgment of the handoff
  seat and the integrator rather than on an operator instruction. Read its §0 first: it states who
  decided and on what evidence, and the operator may revisit it. Its hard metric is that **no row
  closed**, which is a measurement, not a shortfall.
- **The AJ second-pass research landed** and is the input `021-D` says must be read before any AJ
  candidate is ratified. Read the integrator's pre-merge findings on it alongside it — they are
  recorded in the merge and in the supplement, and they bear on how far its headline can be relied
  on.
- **The v1.5.0 tag was NOT declared**, and this window did not move it. Its checklist is the
  container the operator declares on; no seat flips it.
- **H0 itself was not executed.** H0-PREP is the preparation batch; the corp-monorepo runbook has
  not been run.
- Per-`#id` and per-ADR detail: `BACKLOG.md` + `JOURNAL.md`. This bundle does not restate them.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The five open questions the next seat should resume rather than rediscover.** Each is genuinely
undecided; none is a task waiting for hands.

**1 — Which agenda governs?** The agenda this bundle was commissioned against is one revision behind
the operator. Later inbox items reverse the day's ordering (visible surfaces before gates), define
universalization as sameness of SHAPE with content staying each repo's own, amend the H0 runbook to
begin with a seal report, and propose a floor staging. **They are unconsumed and were deliberately
left out of the retention sweep.** Ruling which agenda governs is prior to working any row on it.

**2 — What is the tag gate?** Three enumerations of the v1.5.0 gate are live and they do not agree:
the checklist container, the agenda's three named conditions, and a later inbox item stating a
ruling reversal that narrows it further. The checklist is the surface with a recorded
owner-instruction behind it; the reversal is the newest. Ruling from the middle one is the failure
this bundle exists to prevent. The operator declares the tag on the checklist — no seat does.

**3 — What is agy's role, given that the re-adjudication RATIFIED THE REFUSE?** The inherited
framing of that outcome as an admission is wrong, and the correction matters more than the label:
what changed is the *claim*, not the verdict. The provider was refused as not admissible under the
harness as issued, explicitly **not** as fabricating. That makes the live question "is the harness
defect fixed?" rather than "was it admitted?" — a deterministic, localised defect is fixable in a
way an untrustworthy analyst is not. Gemini's reader role, with mandatory verification, is settled
separately and should not be collapsed into this.

**4 — Universalization is first a PACKAGING problem, and that is a claim to accept or reject.** The
proposal is that nothing may be a per-repo act: every element becomes a component with a manifest
version, a carrier, a two-way drift check and a per-consumer waiver — which re-frames the
derived-copies registry from hygiene into the inventory of components. Sending everything at once is
refused on evidence from an earlier batch. The staging proposal wants a ruling before anyone builds.

**5 — Who owns the unowned?** Several items are board-assigned with no brief, and several gates on
the release checklist have no owner. **No owner was invented for any of them.** Assigning them is
the next seat's first act, and inventing one silently is the failure mode this line exists to name.

**One thing about this bundle's own production that belongs in the design record.** The cut refused
twice on fail-closed gates with no override: once over a live lane worktree, and once over an open
batch whose lanes had all merged but whose close packet nobody had written. The second means an
unwritten packet blocks *every* handoff in the repository, and the refusal names the batch rather
than the missing act. Both are filed as candidates. Neither is a defect in the gates — they did
exactly what they say — but the standing instruction to work in an isolation worktree and never the
primary is **unsatisfiable for a handoff cut**, because provisioning the worktree blocks the gate
the cut needs. That contradiction wants resolving before the next window hits it at the same hour.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
