# Residual — 2026-08-01-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->

Two REDs are STANDING and OWNED, not new: both are the [#457] ids (a disposition-blind parity assertion and a disputed routine-row pin), and the universal step gate is *no NEW failures beyond those two*. Two advisory WARNs are STANDING by construction and must not be 'fixed': the [S24] empty-story WARN is a story COMPLETING (this window's ruled precedent), and the backpressure BACKLOG leg is blind to pure-deletion closures (JOURNAL-recorded, earns a row only if it re-bites). One NEW-to-the-ledger item is reported not fixed: three ADRs carry `Status: Proposed` in-file while cited elsewhere as ratified — flipping one asserts a ratification event, which is the operator's to confirm. Read the live verdicts from the probes; nothing here states a count.

<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->

[#462] closed — the ADR-104 declaration is now diffed against every repo-keyed surface (`membership_agreement`, `ALL_CHECKS` 37→38); `terminal-setup` registered as the 9th fleet repo. ADR-109 AMENDED (2026-08-01): the Related-line matrix-width gloss corrected — **9 governs**. [#461] closed — the six window metrics mechanized, two of them deliberately carrying NO number. [#459] closed — Ch2 names the ADR-109 organ class and the codemap source-root is ruled **B** (schema out of scope, cost stated). [#465] **leg 1 only** — a skip is never recorded as PASS (16 sites); legs 2–4 remain OPEN. [S24] marked COMPLETED under the new story-level retire-not-delete precedent. Detail: `JOURNAL.md` entries (d)/(e); rows in `BACKLOG.md`.

<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->

**[#472] is the live architecture question** — what form a loadable ADR-104 declaration takes. Every candidate carries a named cost: a regex over ADR prose is brittle, restructuring VISION is a doc change, and a new persisted file reopens an ADR-109 rejection made twice (§2, §9). This window deliberately did NOT pre-empt it: the declaration shipped as a module constant provenance-cited to ADR-104:15, with its drift residual NAMED and mapped to [#472]'s own Done-when rather than half-solved. Do not re-derive that trade-off — resume it.

**Do not re-decide** (each ruled this window, reopening needs NEW evidence): 9-governs; [#459] = B; the `membership_agreement` verdict model (an undeclared member FAILs, a declared-but-absent member is PASS-carried-as-data and never WARN, because an undispositioned WARN REDs the ship-gate); the metrics organ's NOT-COMPUTED semantics; story-level retire-not-delete.

**Undesigned, not merely unbuilt:** the L3.5 reconcile cadence — [#460] unblocked it, but who reads the divergence report on what trigger is unanswered. The 51 replicated fleet-audit commits are pushed and unreviewed. [#465] legs 2–4 (same-day digest overwrite, hub-detection flap, tag-canonicity) are actionable now; leg 1 made the flap VISIBLE without fixing its cause, which is the kind of half-fix worth stating plainly before someone reads leg 1 as having addressed leg 3.

<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
