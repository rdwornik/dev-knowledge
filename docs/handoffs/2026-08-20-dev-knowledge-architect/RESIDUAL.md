# Residual — 2026-08-20-dev-knowledge-architect — the part the repo does not already encode

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
**Provenance tag for this whole residual, stated once:** the drift-check *runs* and the branch / backlog / intake reads behind it are `witnessed` — CC re-derived them live at generation. Everything in §2 is `recall` from `JOURNAL.md` and the git spine: **this seat did not participate in the sessions that produced this window's work**, so §2 is a map of the record, not a report of lived experience. Treat it accordingly and re-check anything load-bearing via `PROBES.md`.

**Standing / already-dispositioned — not news.** The row-length family in `ecosystem/disposition-register.yaml` now covers `[#546]` `[#547]` `[#552]` `[#533]` `[#529]` `[#530]`; alongside it sit the undeclared-intake prompt-template family (intake #25, #30, the v6 proposal), `warn-reconciled-versions-contributing-template`, `warn-review-artifact-lane-c-504-no-tally` and `warn-journal-spine-anchored-by-mention`. **The register growing on the row-length axis is itself the signal** — §4 item 4 carries why that is a decision and not a maintenance chore.

**New this window, and it changes how one flag class must be READ.** `[#560]` establishes that `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file and one title literal, so a real review can be invisible to it and some of its WARNs are false by construction. `[#499]`'s hard flip is gated on that same count. Until `[#560]` lands, **that WARN family is not evidence** — do not disposition against it and do not read a clean count from it as coverage.

**Second reading caveat, from the harvest itself.** C2 recorded that the cloud containers had **no gates armed at all**, so for the five `claude/*` lanes the first hub gate run was the merge, not the lane. Any drift those artifacts carry therefore surfaces in post-merge checks now rather than having been caught in-lane — §4 item 2 is the decision that follows.

No verdict, WARN count, `[stale]` status, drifted `#id` or sha appears above **by design**: `PROBES.md` P4/P6/P7/P9 re-derive every one of them live, and naming a value here would re-invert the anti-bluff contract.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
`recall` — reconstructed from `JOURNAL.md` and `git log --first-parent`, one line per arc, pointing at the entry that holds the detail. The JOURNAL already encodes the *how*; this is only the map. Thirty-five first-parent spine entries landed since the prior bundle was cut.

- **Batch 1 integrates** — 8 lanes merged, 6 rows banked, the row-length pile reaches zero undispositioned · JOURNAL 2026-08-18 (d); its two own drifts repaired in (e), packet closed out in (f)
- **Phase 0 baselines** — the commit-tax measured at **6.9× its recorded figure**, and the mutation pilot measured nothing · 2026-08-18 (c). The commit-tax number is what makes `[#533]` leg 2 a throughput argument rather than a legibility one
- **NB7 morning consolidation** — two of four land; the two oversized rows come under the ceiling · 2026-08-18 (a)/(b)
- **The N1–N5 night** — four of five land; **N4 refused at the docs-only gate** · 2026-08-19 (a) — then landed audits-only by the S-1 adjudication seat, which also gave two unlocated rules a locator, cleared D8's WARN, and recorded **three births, seven closures** · (b)
- **`[#122]` closes** on the operator's KEEP word, and the fleet-audit blocker clears · 2026-08-19 (c)
- **Batch 2** — four lanes land, **lane L2 REFUSED on its own Done-when**; the operator then reversed the refusal as mis-addressed and L2 merged · (d)/(e). The refusal-then-reversal is precedent worth knowing before the next refuse-rule call
- **`[#486]` closes** — the cp1252 crash the caches wave recorded but did not own · (f); dashboard regenerated onto the closed state · (g)
- **The five cloud C-lanes are harvested** — **5 merged / 0 refused / 0 pending**, 4462 lines of artifact, one consolidated digest `[#348]` · (h) — and their five dispatch briefs land so provenance sits in the same tree `[#539]` · (i)
- **Born this window:** `[#559]` (kernel/lab check tiering + installable package — the fleet's oldest ACCEPTED-unfiled debt), `[#560]` (the review-artifact reader's structural blindness), `[#561]` (re-base the compute plan onto the Hetzner CX line)
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Read this first: the window's defining asymmetry.** It closed with a large, well-evidenced, *assembled but unruled* queue — `docs/audits/2026-08-19-technical-c-lanes-consolidated.md` §6 lists ten asks, each carried across with its originating lane's own urgency framing, and the digest is explicit that it **assembles evidence and rules nothing**. The seat that produced the evidence was correct not to rule from inside the harvest. The consequence is that the ruling debt is now this seat's, and it is the largest single carry into the next session.

**1. The cloud-lane contract vs `audit-index-freshness` — rule this one first; it is the only ask that recurs.** A cloud lane whose contract forbids index regeneration cannot add a `docs/audits/` artifact without tripping the hub's `audit-index-freshness` gate. C1 resolved it the only way left to it — `git commit --no-verify`, twice, and it declared this rather than hiding it. The digest names it a **standing structural conflict, not a lane defect**, recurring on every cloud lane that adds an artifact. Three shapes are available and none is chosen: exempt cloud lanes from regeneration and have the integrator regenerate once at the queue's close (which is de facto what 2026-08-19 (h) already did, successfully, and the conflict-by-regeneration resolution there is a working precedent); or drop the no-regeneration clause from the lane contract; or make the gate lane-aware. Ruling it once retires a per-lane bypass that currently looks like discipline failure in the record but is not.

**2. Cloud lanes run with no gates armed — so "green in the lane" is not a claim about a cloud lane.** C2 recorded that the containers had **no hub gates armed at all**; the merge was the first time any gate ran on that material. This is the same question as `[#554]`'s provisioning leg (deterministic `pre-commit install` for all three hook types) arriving from the other direction, and it should be ruled as one question, not two. The decision is whether the model is **integrator-as-gate** (accepted, and then the lane contract should stop implying in-lane verification) or **provisioned-and-armed** (and then `[#554]` owns it and the cloud dispatch path blocks on it). Leaving it unstated is what produces receipts that read greener than they are.

**3. Two time-critical asks expired unruled — and one of the two deadlines was simply wrong.** C6 routed `run_id` in the emit contract as due "TODAY" with its window closing at the L2 merge; **L2 merged on 2026-08-19** (JOURNAL (e)), so that window closed. But `[#529]` is still **LIBRARY ONLY with zero call sites**, so the emit contract is still cheap to amend right up until the wiring lands — the *ask* is live, the *deadline* was mis-derived. C1's three-gate ADMIT/REFUSE bar was scoped to "tonight's slot," which has passed; it needs re-issuing or declaring moot. **The meta-question is the durable one:** a lane may declare a deadline the integrator has no way to meet, and nothing in the protocol catches that. Worth one ruling on whether a lane-declared deadline binds at all.

**4. Carried and deliberately deferred — resume, do not relitigate.** (a) The `doc_rot` **row-length ceiling versus actual practice** — the register now carries six row-length dispositions and the standing stance is that `doc_rot` greens by fixes and never by dispositions, so either the ceiling moves or long rows decompose; every future birth otherwise adds a finding to a class that is supposed to be shrinking. (b) **Which row owns the unshallow and the `uv`-pin assert** — `[#554]` and `[#453]` overlap on two of four legs, and `[#554]`'s second-lander-points-at-the-first clause is a convention this seat may ratify or replace, not a decision already made. (c) **One denominator predicate** — three counts of the same backlog remain in circulation, and `[#555]` makes naming one its first act; until then any *net-negative* claim is unfalsifiable, which matters because net-closing is the stated goal. (d) **Who performs promotion** — the durable homes for the ratified terms are named, the promotion *act* is still unowned.

**5. Decided-unfiled is now the repeat failure mode, and it has a measurement.** Seven intakes sit `DRAFT`; the prior window's plan to ratify #35–#39 did not execute. `[#559]` is the sharpest instance — intake #25's W-2 was ACCEPTED on 2026-08-05 and carried **zero rows for fourteen days**, verified by carrier test rather than asserted. The pattern is that ratification rides a wrap, and wraps get consumed by integration. The open decision is whether ratification gets **its own dispatched lane** with its own contract, the way implementation does.

**6. One instrument is untrustworthy and gates another.** `[#560]`: `review_artifact_coverage` reads only the first branch/HEAD triple per file plus one title literal, so a genuine review can be invisible to it — and `[#499]`'s hard flip is gated on that leg's false-positive count. Fixing the reader is a precondition for the flip, not an independent tidy-up. Sequence them.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
