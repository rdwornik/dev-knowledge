# Residual — 2026-07-21-dev-knowledge-architect — the part the repo does not already encode

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
**The CC session that generated this was cold; the SUPPLEMENT is not.** The generating session was
`/clear`ed and did no work of its own, so everything in **this file** is repo-derived from the
git/JOURNAL window since `2026-07-20-dev-knowledge-architect`, tagged `witnessed` where re-derived live
at generation and `recall` where read out of the record. **`SUPPLEMENT.md` was subsequently FILLED** by
the outgoing architect chat and its ANSWERS are folded into `PASTE_THIS.md` — so the §13(d) beat
**NARROWS** to *"anything changed since the supplement was written?"*, it does not fire full.

**Read the SUPPLEMENT before this file's §4.** The two were authored in that order and the supplement
**overrides §4 on sequencing** — the reconciliation is marked inline at §4 rather than by silently
rewriting it, so you can see what the repo said and what the operator ruled.

**Standing (dispositioned — expect them; they are not news).** `witnessed` — the same four register
families as the previous bundle, unchanged in composition: the `no_ff_merges` journal-wrap /
transcript-archive entries, the `undeclared_edges` HANDOFF_PROCESS dependents (`#241`), the `doc_rot`
backlog-accretion entries, and the `reconciled_versions` CONTRIBUTING-template entry (`#335`). Read
them at `ecosystem/disposition-register.yaml`; P7 re-derives which are live.

**Carried, NOT new, and still deliberately un-dispositioned — the one flag to actually look at.**
`VISION.md`'s `last_reviewed` cadence flag, owned by **[#368]**. It has now aged a further day by pure
calendar rollover; the file itself is still untouched. The previous bundle's reasoning stands verbatim
and should not be relitigated: re-stamping to reach a green number converts an honest signal into a
false one, and dispositioning it is the same move in a different costume. **The correct discharge is a
genuine end-to-end re-read of `VISION.md`** — and this window's vision audit (below) is a strong reason
to do that re-read *now*, with the audit's H1/H2/H6 critiques in hand, rather than as a stamping chore.

**A register-accuracy correction landed this window and supersedes the night audit's own guidance.**
`recall` (JOURNAL, `3234b4a0` lane) — the 2026-07-21 backlog audit's operator watch-out about which
`#id` closures would orphan a disposition is **wrong in both directions**: three ids it names orphan
nothing, it omits four `doc_rot` entries whose refs are open tickets and *would* orphan on close, and
its multiplicity for `#241` is understated. **The audit is immutable, so the correction lives only in
the JOURNAL entry for that lane** — a `/review-closures` pass that trusts the audit rather than the
JOURNAL will retire the wrong entries. Re-derive the live set from
`ecosystem/disposition-register.yaml`; do not read the numbers out of either document.

**Environmental, not a regression.** `handoff_probes` binds to the newest *committed* bundle, so once
this bundle lands it becomes the gate's target. Two known non-defects if you see them: a linked
worktree trips `deployed_methodology_version` on its directory name, and a cross-repo bundle can trip
sibling-resolution. Neither warrants a disposition entry.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the `2026-07-20-dev-knowledge-architect` bundle. Detail is in `JOURNAL.md` (newest-first,
five entries cover it) and `docs/audits/`; do not re-read it here.

**The one-line summary of the window: no ARC-5 wave opened.** What shipped was three read-only audit
lanes plus a hygiene pass. Hold that against `[E8]`'s own banner — *"AUDITS ARE OVER. ARC 5 IS
EXECUTION"* — and against §4 item 2 below, which is where it bites.

- **Night batch, three read-only lanes merged** (`eee8f532`, `94f910e3`, `1ef71834`) — vision/direction
  critique, code-quality audit, and backlog-trust audit, each an artifact in `docs/audits/` under the
  2026-07-21 `technical` class. **By contract all three filed proposals only** — zero ticket ids, zero
  backlog mutation. They are undischarged inputs, not shipped work.
- **Backlog hygiene arc** (the `worktree-cleanup-backlog` merge; sha withheld — it is adjacent to P3's
  live answer) — five tickets closed through the ADR-70 Tier-1 gate
  (`[#302]` `[#309]` `[#131]` `[#314]` `[#292]`), seven tickets repointed, four `#NNN` placeholders
  resolved to `[#234]`. Net task count fell. **Four audit claims were refuted on live verification**
  and the refutations live in that lane's JOURNAL entry, not in the immutable audit.
- **Registry lane** (the `worktree-cleanup-registry` merge) — the corp-monorepo `deployed-versions.yaml` entry annotated rather
  than bumped, and the night audit's A1 finding refuted: the corpus-version-vs-gate-rev divergence is
  deliberate and already modeled under **ADR-102**.
- **The direct-to-main incident is CLOSED** — the `[#373]`–`[#380]` id-range reservation that landed
  off-spine was relocated onto a proper `--no-ff` merge (`e3e79ada`). Core-invariant #5 holds on the
  spine again. Next-free id is unchanged by this window.
- **ARC-5 itself: no movement.** No wave opened, no decision ruled, `[#352]` clause (f) still
  unwitnessed, `[#371]` still unbuilt. `[E8]` in `BACKLOG.md` is unchanged from the previous bundle.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
> **RECONCILIATION — the SUPPLEMENT was filled AFTER this section and overrides it on sequencing.**
> §4 was authored from repo state alone; the supplement then arrived carrying the operator's intent.
> Where they disagree **the supplement wins**, and the disagreement is marked here rather than edited
> away, so the next session can see both. Per item:
>
> - **Item 1 — OVERRIDDEN on sequencing.** The supplement's mandate is **one delivery lane**
>   (`assets/` dissolution in ai-council, already granted 2026-07-19 — *execute, do not re-seek
>   permission*), **not** a bounded-pick message. It also effectively rules **R12** by rejecting the
>   narrowing option outright (*"goal is ALL rules, prioritised, never lowered"*), and it names a
>   **different owed-ruling set** — five one-sentence rulings on `#339`, `#327`, `#304`+`#305`,
>   `#262`+`#295`, `#215`. Treat *that* list as the live ask, not R1–R8.
> - **Item 2 — PARTIALLY ruled.** *"Consume the three audits, do not commission more"*; they are the
>   last input. **The clause-(d) accretion tension is NOT resolved** — that half of the item stands.
> - **Item 3 — AFFIRMED and given a disposition.** The polyrepo bet is confirmed as the sharpest
>   hole and routed to **its own session**, deliberately not mixed into the delivery work, with a
>   standing brake: *do not build more fleet machinery until it is ruled.*
> - **Items 4 and 5 — UNTOUCHED by the supplement; they stand.** Item 4 is independently corroborated:
>   the supplement's DO-NOT-REDO list carries the same `#320` refutation from the other direction.
> - **Item 6 — the buy-vs-build half is RULED.** The template engine is **rejected** (merge-replay
>   engines fail at this divergence profile; the hub is already regenerate-shaped), keeping only the
>   per-consumer version-pin scalar. So `[#371]`'s vehicle is no longer blocked on an open engine
>   question. The clause-(f) operator witness remains open.

### 1. The ten unruled decisions are STILL unruled — this is the second handoff to say so

`[E8]`'s decision table (R1, R1b, R2–R8, R12) is unchanged and **entirely unruled**. The previous
bundle named "a single bounded-pick message to the operator" as *the successor's first substantive
move*; that did not happen, and the window went to audits instead. **Repeating the same
recommendation a third time is not the move.** Either the bounded-pick message goes out at the top of
the next session, or the reason it keeps not happening is itself the thing to diagnose — because
several waves (W2 needs R1/R1b, W3's deletion path R3, W4's shape R2, W5's organ count R5) are
formally blocked on it and have been for two windows.

**R12 still leads, and item 3 below may have changed what R12 is choosing between.**

### 2. Three audit reports landed UNTRIAGED — and the triage is a decision, not a task

Roughly fourteen hundred lines across vision, code, and backlog critiques sit in `docs/audits/`,
each filed proposals-only by contract. The code audit carries an explicit triage test in its §0
(*location + falsifiable defect ⇒ ticket; opinion without a location ⇒ logged-reject*); the vision
audit attaches a falsification hook to every hole. **So the material is triage-ready and nothing is
blocking it except a decision about how much of it to accept.**

**The recursion is the actual problem, and it is worth stating plainly.** Discharging these reports
mints tickets. `[E8]`'s closure clause (d) requires backlog accretion **net ≤ 0** excluding tickets
minted by ARC-5's own waves — and audit-derived tickets are *not* wave-minted, so every one of them
counts against closure. **A full triage of these three reports could make clause (d) unreachable in a
single move.** The choices are real and none is obviously right: triage fully and re-baseline clause
(d); triage a bounded slice and log the rest as accepted-unfiled; or defer triage entirely until a
wave has actually shipped. **Pick one explicitly** — drifting into partial triage is the option that
looks like progress and satisfies nothing.

### 3. The vision audit asks one question that sits ABOVE ARC-5 and re-prices it

Its §6: *"if the three repos were folded into one tomorrow, how much of this system would still
deserve to exist — and is what remains the part I actually value?"* The claim is that a monorepo
**dissolves by construction** most of what the fleet machinery does — fleet parity, carriers and
deploy manifests, dependency parity, cross-repo pins, the collector, most of the parity register, and
the id-collision / worktree-contamination class — while what survives is the methodology lifecycle,
the census idea, the handoff harness, and the agent-coordination guards.

**Why this is a frontier item and not just a provocative read:** the audit's supporting observation is
that the **polyrepo shape was never actually decided** — no ADR argues it, and the 10–20 repo target
appears in scale requirements without a defence. If that is right, then **ARC-5's W2 (structure
equalization) is investment in exactly the layer the question puts at risk**, and R12 — "what is
ARC-5" — is downstream of a bet nobody has written down. This does not mean fold the repos; it means
the bet should be made explicit and defended (the audit's own estimate is an afternoon's ADR, with
two named falsification hooks) **before** W2 opens, not after.

### 4. Two sibling lanes of the SAME night batch contradict each other — and the batch has no organ that noticed

`witnessed`. The vision audit's **H7** ("the governance system audits naming conventions while three
repos sit unbacked on one disk") rests on three factual claims about consumer-repo backup posture.
**All three were independently refuted the same night by the backlog lane**, which verified them live
against the real repos; `[#320]` in `BACKLOG.md` now carries the corrected premise at `7c592062`. So
H7's evidence base is gone while H7 itself still reads as live in an **immutable** artifact.

Two things follow, and the second is the bigger one:

- **H7's architectural point may still stand on its own** — that the system has a *parity* register
  which ranks divergence but no *risk* register which ranks loss, and that drift detection was built
  before disaster recovery. That claim survives the refutation of its evidence. Salvage it
  deliberately or drop it deliberately; do not let it die by association with three wrong facts.
- **Nothing in the batch cross-checked the lanes against each other.** Each lane verified its own
  claims against live state and both did that job well — the contradiction is *between* them, and
  parallel read-only lanes have no shared adjudication step. This is a real gap in the batch method
  at n=1 witnessed, and it is the same failure shape `HANDOFF_PROCESS` §8 already names for the
  browser's artifact check: *two load-bearing claims that cannot both be acted on, where every
  per-claim check passes because each is checked against state and never against the other.*

### 5. The code audit independently rediscovered ARC-5's own disease model — in the code

Its closing structural observation across the top shortlist items: *"the recurring failure in this
codebase is not bad design and not missing tests; it is designed invariants with no organ asserting
them"* — a cycle detector that cannot see its own graph, a git-env scrub applied at one of nine
sites, a `Carrier` contract whose invariants no test asserts. **That is `[E8]`'s "recorded ≠ enforced
≠ legible" thesis, arrived at from the opposite direction by a lane that was auditing Python.**

The convergence is the finding. It says ARC-5's disease model generalizes beyond governance prose
into the enforcement machinery itself, which strengthens the arc's premise — and it supplies the
audit's own conclusion that the durable fix is usually **"make the existing gate real", not "add a
gate"**. That principle is a candidate for the arc's binding set, and it points at a cheap opening
move: the shortlist's item 1 is a check that is already registered, already wired, and simply
vacuous. Whether repairing existing organs counts as ARC-5 wave work or as separate hygiene is
**unruled**, and it interacts with clause (d) in item 2.

### 6. W1's tail is blocked on a decision that just got bigger

Unchanged from the previous bundle and still open: clause **(f)** — `[#352]`'s operator-witness of the
boundary decoration — and clause **(c)** — W1 has no archived Codex review artifact, and clause (c) is
itself a MUST-shaped rule with no mechanism, which is the arc's own disease on the arc's own board.

What changed: **`[#371]`** (the consumer editor-config write-through, declared at manifest v1.4.0 and
never built) has its vehicle decided by the pending buy-vs-build fleet-template ADR — and that ADR is
now entangled with the vision audit's **H4** (the buy-vs-build bet, as tabled, adopts the wrong tools
for this fleet's shape) **and** with item 3's monorepo question. A one-ticket write-through has become
the visible edge of a three-way decision. **The cheap escape is worth naming:** clause (f) needs the
operator to *see* the decoration in a consumer, and that witness does not require the fleet-template
ADR to be settled first.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
