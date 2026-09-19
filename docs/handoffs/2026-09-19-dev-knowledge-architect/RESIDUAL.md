# Residual — 2026-09-19-dev-knowledge-architect — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-09-17-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**`fleet_parity` is a DECISION, not a defect.** Its `settings-deny-and-point` row was deliberately
set to hub-INVERSE this window: BUILD MODE rule 8 unwired that PreToolUse guard, so the hub is
expected to lack it and a consumer that still ships it is the divergence. The inversion is
therefore the correct reading of the live fleet, and a parity flag from that row is the mechanism
working. What is NOT decided: the parity schema has no row-level expiry the checker reads, so the
inversion cannot expire with BUILD MODE by itself — that gap is owned by its own row, and no field
was invented to paper over it. Every other parity flag is a defect and is owned as such.

**`reconciled_versions` is a defect if it flags.** It reads the registered specs against the docs
declaring a `reconciled_with:` edge; nothing this window did makes a mismatch intentional.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail is in `JOURNAL.md` 2026-09-19 entries (aq)-(au) and the rows themselves.

- `[#926]` — the two refuse-forever gates (`journal_day_letters`, `substrate_declaration`) narrowed
  to recognise the correction their own invariants permit. Temporary by construction: each check
  reads its own expiry constant, and past it the narrowing switches off and the finding names the
  row for re-ruling. **Row stays OPEN** — the expiry needs an operator re-ruling, not a closure.
- `[#921]` — filed: ARCHITECTURE re-read and restamped, R-2 re-landed, AX9-5 consumer declared.
- `[#922]`-`[#927]` — filed: the quick-fix arc's carried debt (silent rules drained, parity
  inverted, four audits given real consumers). No check was changed by that arc.
- `[#928]` — filed: the parity schema cannot express a row-level expiry (see §1).
- `[#916]` — amended: the ratchet drop removed prose, not risk; it is explicitly NOT a fix.

**Carried decisions — `carried-by: OPEN`, named here because the residual is their only carrier
(P11 leg 2).** Each of these states an OPEN carrier and has no repo home yet; the next session
either lands each one or re-declares the carriage:

- `to-cc/AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/AMEND-BATCH-night-2026-09-17.md`
- `to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md`
- `to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md`
- `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md`
- `to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md`
- `to-cc/AMEND-ORGAN-USE-2026-09-17.md`
- `to-cc/BATCH-dispatch-order-2026-09-17.md`
- `to-cc/BATCH-night-2026-09-17.md`
- `to-cc/BATCH-night-wave2-2026-09-19.md`
- `to-cc/BATCH-night-wave2-CORRECTED-2026-09-19.md`
- `to-cc/BATCH-night-wave2-FINAL-2026-09-19.md`
- `to-cc/BATCH-night-wave2-FULL-2026-09-19.md`
- `to-cc/DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md`
- `to-cc/DECLARE-BUILD-MODE-2026-09-18.md`
- `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md`
- `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md`
- `to-cc/DECLARE-SPINE-AND-B3-2026-09-19.md`

**Carried WARN debt.** This window hands off with the ship-gate's open WARNs unresolved rather than
silenced; P7 re-derives them live. The organ-level attribution is generated in §1 above, and the
standing families are the register's. Nothing was dispositioned to make a gate pass — the two
gates that blocked the cut were fixed at their scoping defect, with a test proving the uncorrected
case still fails.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The outgoing architect's own "why" is folded into this paste from `SUPPLEMENT.md` and is not
restated here. What follows is the executor-side residue: the questions this window's *work* left
open, each with the surface that would answer it.

**1. What makes a temporary measure expire by itself — and what happens when the schema cannot
hold an expiry?** This window landed two narrowings whose expiry is a constant the check itself
reads against one date seam, so they switch themselves off with no human in the loop. That shape
worked, and it is the pattern to generalise. But the same window hit a surface where it does not
fit: the parity schema has no row-level expiry field a checker reads, so a deliberately inverted
row cannot expire with the order that justified it. Inventing a field was refused. The open
question is whether expiry belongs in each schema or in one surface every dated exception
registers with. Owning rows: the narrowing row and the parity-schema row.

**2. Does a gate that refuses forever mean debt, or a scoping defect?** Both gates that blocked
this cut turned out to be the second kind: their invariant permitted exactly one correction, and
neither could recognise it. Neither was waived and neither was widened — the sanctioned escape on
one of them was refused on the record, because its own docstring says using it would falsify the
record. The transferable question: at a refusing gate, ask first whether the correction the
invariant permits is expressible to the check, before reaching for a disposition. There is still
no sanctioned FAIL waiver in this repo, which is a deliberate absence, not a gap to fill.

**3. Adversarial review is worth more than one pass, and the cost is bounded.** The narrowings
went through four cross-provider passes; the first three each found a way the narrowing was
WIDER than ordered (key collision, nested scope inheritance, case folding) and one finding was
rejected on the record with reasons. None would have been caught by the tests as first written.
The open design question is whether "review until a clean pass" becomes the lane standard, given
the passes are cheap relative to a landed widening.

**4. The preflight's cut criterion versus the tag's.** This cut proceeded on zero hard-fails with
the open WARNs carried explicitly in this residual, which is the preflight's actual contract — a
window may hand off with debt when the debt is explicit and owned, never when it is silent. Worth
knowing that the earlier reading (treating the tag's green as the cut's bar) is what deadlocked
this window in the first place.

**5. The carried decisions above are the real queue.** They accumulated because a decision file
can declare an OPEN carrier indefinitely and nothing ages it. The next session should treat
landing them as work, not as filing.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
