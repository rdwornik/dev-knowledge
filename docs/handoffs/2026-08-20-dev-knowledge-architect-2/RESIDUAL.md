# Residual — 2026-08-20-dev-knowledge-architect-2 — the part the repo does not already encode

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

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**Nothing here is a value — P4/P6/P7/P9 hold the live answers.** What follows is which *classes* are standing versus new, and why, so the incoming architect can tell a carried WARN from a fresh one without waiting for the block.

- **Standing, and deliberately GROWN this window: the `doc_rot` `backlog-row-length` class.** The eight births released by the 2026-08-20 act-group-2 arc landed with bodies over the ceiling, as drafted rather than trimmed, on the precedent `[#559]`/`[#561]` set — the arc disclosed this in `JOURNAL.md` 2026-08-20 (h) rather than letting a reader discover it. This is **not new drift**: it is the unruled ceiling question carried in §4 below, now larger by construction. Treat any row-length finding P7 reports as belonging to that open decision, not to a fresh defect.
- **Standing and dispositioned elsewhere:** the carried classes live in `ecosystem/disposition-register.yaml`; the register is the only place a suppression is legitimate, and the standing stance — `doc_rot` greens by **fixes**, never by dispositions — is why the row-length class was never dispositioned away. Read the register before dispositioning anything P7 surfaces.
- **The silent-rule ratchet was measured, not assumed, at every `protocols/` edit of the window** (before/after each `STANDING_RULINGS.md` write), and the arc recorded that section Q added no `must|shall|never` debt — see `JOURNAL.md` 2026-08-20 (g)/(h). Section Q is phrased declaratively on purpose, per that file's own Editing note; the one softened line (Q4) is disclosed in the JOURNAL rather than left for a reader to notice. P-class re-derivation still binds — the record here is provenance, not a substitute.
- **New-this-window drift, if any, is P7's answer alone.** Both read-only drift-checks (`validate_doc_claims`, `validate_git_backlog`) were exercised at generation time and this bundle states neither result. The load-bearing instruction is the ordinary one: **any FAIL in the evidence block blocks onboarding**, and a WARN whose class is not named above should be read as new until the register says otherwise.
- **One instrument is known-untrustworthy and it gates another** — `review_artifact_coverage` (carried by `[#560]`) reads only the first branch/HEAD triple per file plus one title literal, so a genuine review can be invisible to it. If the block shows a coverage-class finding, weigh it against that known reader defect before treating it as a missing review.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->Terse map only — `JOURNAL.md` 2026-08-20 (f)/(g)/(h) and `git log` carry the detail; this is where to look, not what happened.

- **The window's ten rulings are now in-repo** — `protocols/STANDING_RULINGS.md` **section Q**, one line per ruling, landed by the transcription arc whose contract of record is `docs/audits/2026-08-20-technical-transcription-seat-contract.md` (ADR-110, committed first). Q1 index-freshness on lane material · Q2 primary-checkout-is-seat-arc-only · Q3 harvest order · Q4 cloud-lane hygiene · Q5 receipt gate · Q6 contract-as-file-without-exception · Q7–Q9 the acceptance instrument · Q10 PAUSE-on-refuted-premise.
- **The anti-orphan sweep (P-2) discharged in the register itself**, not only in the arc's packet: 18 of 20 ratifications carried by a live row; **Q2 and Q10 `disposition: deferred`, trigger dated 2026-09-19** — see §4 item 3, because that date is a decision, not an outcome.
- **Verdicts reached the rows** — `[#491]`, `[#561]`, `[#539]` annotated (`20a51638`); **eight births released** `[#562]`–`[#569]` (`b6e2044b`) against the arc's re-measured ledger.
- **The acceptance window's systemic finding** is the newest `LESSONS.md` entry (role discipline is a property of *routing*, not of a model); **`ERRATUM E1`** is appended — not edited — to `docs/audits/2026-08-20-technical-codespaces-audit.md`, withdrawing the workstation `ruff` figure and the ratio built on it while leaving the accepted LEAN v2 intact.
- **Substrate was ruled** — `docs/audits/2026-08-20-technical-codespaces-audit.md` carries the accepted RULING; `[#567]` is the carrier lane it released.
- **The PLAYBOOK gap is measured** — `docs/audits/2026-08-20-technical-playbook-status.md`, a 14-row G1–G14 table that independently reads five of the section-Q rulings as ABSENT from `protocols/PLAYBOOK.md` today. Register and census are cross-cited so they cannot drift apart.
- **Two model-acceptance records, neither an admission** — Gemini 3.7 Flash (slots 1 and 2) and Grok 4.6, all under `docs/audits/2026-08-20-technical-*-ab-*`; slot 1 landed renamed to clear slot 2's paths, with one locator repointed and the as-issued contract left untouched.
- **The ruled `--parallel` flip** of the `audit-health` pre-commit entry merged (`54633041`).<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->**Read this first: the shape of the carry INVERTED today.** The morning bundle handed over an *unruled queue* — ten assembled asks nobody had decided. That queue is drained: the rulings exist as `STANDING_RULINGS.md` section Q and their verdicts reached the rows. What replaced it is the opposite problem. The window ended with **eight new rows, no dispatch plan, and a closing bar that the same arc moved closer to its limit.** The next session's scarce resource is not judgement; it is *throughput and closure*. Sequence and close — do not re-rule section Q.

**1. The closing bar is now the binding constraint, and it binds before the next filing — not after.** `[#555]` sets the stated goal as **net-negative** (closures strictly greater than births) and the house rule per `d85490d0` is *banked > window births*. Act-group 2 released eight births against the banked ledger it re-measured from `tasks/` rather than carrying from its contract, and recorded the resulting headroom in `JOURNAL.md` 2026-08-20 (h). **Re-derive that ledger before filing anything** — the rule halts a release the moment it stops holding, and the next window opens much closer to that line than the last one did. The decision this forces: does the next window *dispatch implementation* (which files nothing and closes little) or *run the closing batch* `[#555]` first — and note `[#555]`'s own first act is naming ONE denominator predicate, because three counts of this backlog are still in circulation and until one is chosen **no net-negative claim is falsifiable at all**.

**2. The `doc_rot` row-length ceiling is now a decision the repo is actively voting against.** The standing stance is that `doc_rot` greens by fixes and never by dispositions; the practice is that every window's births land over the ceiling on precedent, and this window added eight more. Three exits, none chosen: **move the ceiling** with a recorded basis (and then the disposition backlog for that class retires); **decompose long rows** (and the eight born-long rows are the first candidates, which makes it a closing-campaign leg rather than a separate arc); or **keep the tension and stop calling it drift** (worst option — it teaches that a named class is optional). This has now been carried across three consecutive windows. It is cheap to rule and it gets more expensive to fix every time it is deferred.

**3. `[#539]` is the load-bearing lane, it is undispatched, and a dated deferral is quietly riding on it.** It carries five of the ten section-Q rulings to their declared durable home (PLAYBOOK Ch8 — the census maps them G10/G9/G14/G3/G13 and reads every one as ABSENT today), and its `--check` leg arms two organs currently wired into no gate, with the two branch-grammar incidents in `LESSONS.md` 2026-08-19 as its evidence base. **Q2 and Q10's deferral triggers on that lane landing *or* 2026-09-19, whichever comes first** — so if `[#539]` does not get dispatched, the deferral does not fail loudly, it just ages. Either dispatch it next window or re-date the deferral with a stated reason; letting the date arrive undecided is the failure mode the anti-orphan sweep exists to prevent.

**4. The open question about model admission is the INSTRUMENT, not the candidates.** Two candidates were assessed and neither admitted; Q9 fixes ADMIT as G1 ∧ G2 ∧ G3 on the seeded-defect pack and Q7 makes Φ trajectory-inclusive, so the *bar* is settled. What is not settled is what the C1 pack's two refusal items measure: the newest `LESSONS.md` entry shows the **incumbent scored 0/2 on the same items**, which means those items may be measuring *dispatch quality* rather than model role-discipline. Three readings are available — keep them as admission gates (and accept that a gate the incumbent fails is a strange gate), demote them to routing diagnostics scored separately, or leave the bar untouched and record "none pass yet" as the result it is. `[#562]`'s guarded rerun is filed, but **its shape depends on this call**, so ruling it first is cheaper than re-running the pack twice.

**5. Decided-unfiled is the repeat failure mode, and it survived another window untouched.** **Seven intakes sit `DRAFT`**; the prior window's plan to ratify did not execute, and this window's transcription arc explicitly excluded intake status transitions — correctly, since that was outside its contract, which is exactly the point: **ratification keeps riding a wrap, and wraps keep getting consumed by integration.** The open decision is unchanged from the morning bundle and is now evidenced twice: does ratification get **its own dispatched lane with its own contract**, the way implementation does? Note the operational trap if it does — an intake status change needs **both** intake generators, and the `intake-index-freshness` gate only covers one of them.

**6. The telemetry chain is sequenced but unowned.** `[#565]` rules that `run_id` lands **before** the read-path lane, and the reasoning is sound while `[#529]` is still library-only with zero call sites. Ruling the sequence did not choose the runner or the window. Still open beneath it: `[#529]`'s four legs (call-site wiring · `.gitignore` the WAL store before the first live emit dirties `git status` · the `structlog` dependency decision · the `_REPO_ROOT` resolution that points at the *worktree* under a linked checkout), and `[#530]`'s two latent races (the ABA in `release`, the `rev-parse` conflation). All are cheap now and none is cheap after wiring.

**7. Substrate is settled; the lane it releases is not.** The Codespaces LEAN v2 is accepted and CX53 is ruled **complementary, not competing** (`[#567]` is its carrier under `[#561]`). What makes an off-machine lane actually run is `[#554]`'s four provisioning legs — pinned `uv`, `git fetch --unshallow`, deterministic `pre-commit install` for all three hook types, and an env gate that refuses a half-provisioned start. Q4 and Q5 (cloud-lane hygiene, receipt gate) now have a written home but **no lane has yet run under them**, so the first cloud dispatch after this handoff is also the first test of those rulings. Sequence `[#554]` before, not after, the next cloud batch.

**8. What NOT to reopen.** Section Q is landed and applies at read time — apply it, do not re-litigate it. The substrate ruling, the `[#488]` axis LEAN (now built by `[#566]`), the `Backlog.md` view-layer verdict (now built by `[#563]` — do not re-run the trial, do not propose it as the store) and the ADR-110 batch shape are all decided. The immutable records — the as-issued lane contracts, `ERRATUM E1`'s append — stay as landed.<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
