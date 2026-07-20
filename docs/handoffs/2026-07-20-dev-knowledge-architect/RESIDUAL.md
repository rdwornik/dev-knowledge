# Residual — 2026-07-20-dev-knowledge-architect — the part the repo does not already encode

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
**Standing (dispositioned — expect them, they are not news).** The register carries four families:
the `no_ff_merges` journal-wrap/transcript-archive entries, the `undeclared` HANDOFF_PROCESS
dependents (BACKLOG · VISION · ai-council · ESSENTIALS · PLAYBOOK · SESSION_SETUP), the `doc_rot`
BACKLOG-task entries (`#262`, `#278`, `#332`, `#344` — the latter two carrying review dates), and the
`reconciled_versions` CONTRIBUTING-template entry. Read them at
`ecosystem/disposition-register.yaml`; P7 re-derives what is live.

**NEW this window, and DELIBERATELY NOT dispositioned — the one flag to actually look at.**
`VISION.md`'s `last_reviewed` aged past the 30-day cadence by pure calendar rollover; the file itself
was not touched. It is **neither stamped nor dispositioned, on purpose.** `last_reviewed` means
*re-read end-to-end and confirmed accurate* — so re-stamping to reach a green number would convert an
honest signal into a false one, and dispositioning it is the same move in a different costume. The
real fix is a genuine re-read, owned by **[#368]**. Treat this flag as **true**, not as noise: it is
the arc's own declare-instead-of-fix pattern showing up on the arc's own board.

**Already resolved — should NOT reappear.** Two WARNs were self-inflicted earlier in the window and
were fixed rather than reported: a `doc_rot` trip on `[#368]`'s own filing, and a `doc_claims` drift
after the boundary-headers test landed (`ecosystem/doc-counts.md` regenerated). If either surfaces
again, that is a regression, not the standing state.

**Structural pressure worth naming.** `[#355]` now sits within a couple of characters of the
`doc_rot` per-task cap, and it is the *second* ticket pinned there. Any further edit to it trips a
new WARN — which is the concrete case **[#364]** argues from, not a maintenance annoyance.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
ARC-5 moved from *planning* to *execution* this window. Terse map — detail is in `JOURNAL.md`
(newest-first) and the `[E8]` theme in `BACKLOG.md`; do not re-read it here.

- **[E8] filed as a living theme** — the ARC-5 plan of record (wave map W1–W7, frozen closure
  contract, unruled decision table) landed in `BACKLOG.md` rather than an ADR, because an ADR is
  immutable and a wave map must evolve. Plus the census declaration test + baseline.
- **W1 (VISIBLE BOUNDARY) merged** — reader-visible ownership headers generated from the `#312`
  marker substrate, plus `.vscode` region decoration declared as fleet carrier material.
  `[#352]` · `[#321]` · CLAUDE.md §12 v2.43–v2.44. **Merged, not closed** — see §4.
- **W6 legibility half merged** — the four ARC-4 rulings inoculated into PLAYBOOK + ESSENTIALS.
  The *enforcement* half is unbuilt and owned by **[#354]**.
- **ARC-5's first enforcing mechanism** — the residual-completeness gate, plus the residual-rule
  declaration that binds its exemption.
- **Census findings discharged into tickets** — `[S22]` (`[#357]`–`[#362]`), including the
  phantom-enforcement class the four-state ledger cannot express (`[#359]`).
- **Session-close hygiene** — `[#368]` (honest-stamp / VISION re-read), `[#369]` (unwired
  `boundary_headers --check`), `[#355]` evidence to n=4.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### 1. Ten decisions are UNRULED and blocking — collect them in ONE bounded-pick message

`[E8]`'s decision table (R1, R1b, R2–R8, R12) is **entirely unruled**. Recommendations are attached
to most, but *a recommendation is not a ruling*, and several waves cannot open without their pick:
W2 needs R1/R1b, W4's very shape is R2, W3's deletion path is R3 and its enum is R4, W5's
one-organ-vs-three is R5. **The successor's first substantive move is a single bounded-pick message
to the operator** — not eight separate asks across eight sessions, and not silently adopting the
recommendations as though they had been ruled.

**R12 is the sharpest and has no recommendation attached.** Closure clause (b) — "everything still
unenforced has moved to declared-unenforced" — is **not achievable in one arc** at the measured
N_silent, which would mean dispositioning every silent rule, and that figure is a *floor* (the ADR
corpus is unswept, `[#357]`). The two live options are **(i) NARROW** the arc target to a bounded
load-bearing slice, or **(ii) GATE THE GROWTH** of silent rules instead of draining the pool. This
decides what ARC-5 *is*, so it should lead the bounded-pick message rather than trail it.

### 2. Does W1 actually close? Two independent gaps — and neither is "merge it harder"

W1 merged, but the closure contract is explicit that **"NOT closure: waves merged, ship-gate green,
tests passing, items marked done."** Two clauses are open:

- **(f) — the operator's own-words confirmation does not exist.** `[#352]`'s Done-when is the
  operator *seeing* the decoration render. That witness has not happened. `[#352]` is deliberately
  left open; **do not close it on the strength of the merge.**
- **(c) — W1 has no archived Codex review artifact.** The per-wave standing requirement is a Codex
  review pre-merge *and* an educate artifact with file-level before→after. W1's reviews were run
  (a CRITICAL, several HIGH, then further findings, all genuinely fixed), but **the artifacts were
  never written to `docs/audits/` and are now unrecoverable** — the findings survive only as
  commit-message prose. So the review *happened* and the evidence *doesn't exist*.

**The design question this raises is bigger than W1:** clause (c) is itself a MUST-shaped rule with
no mechanism — nothing gates a wave merge on the presence of its review artifact. ARC-5's own
closure contract is, by its own census definition, **silently unenforced.** Either it earns a
mechanism, or W1 is waved through and the contract is decorative from wave 1 onward. That choice
should be made explicitly, now, at n=1 — not discovered at W7.

### 3. Wave sequencing is open below the pain-priority ordering

The wave map is ordered by operator pain, not dependency. Two live scheduling facts: **W6 may run
first or in parallel** as a file-disjoint doc lane (its enforcement half, `[#354]`, is unbuilt and
would inoculate rulings before later waves generate more), and **W2 inherits `[#355]`**, a live
false-positive in `fleet_parity` that has already **trained `SKIP=audit-health` bypasses** — a gate
teaching the operator to route around it is a compounding cost, which argues for W2 early regardless
of elegance. Whether W1 must formally *close* before W2 opens is unruled and interacts directly
with item 2 above.

### 4. Two small structural items that will otherwise be rediscovered

- **[#369]** — `boundary_headers.py --check` is the only generated surface with no regen-and-diff
  pre-commit hook; every sibling has one. Not a hole today (the suite catches it at ship-gate), but
  it is an inconsistency in the enforcement mesh, and it moves the gate count when wired.
- **[#364] / the `doc_rot` cap** — two tickets are now pinned against the per-task character cap.
  The cap is doing real work, but at the cap it converts *any* honest edit into a new WARN, which
  pushes toward silence. Worth ruling before a third ticket arrives there.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
