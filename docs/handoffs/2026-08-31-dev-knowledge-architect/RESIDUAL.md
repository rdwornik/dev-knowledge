# Residual — 2026-08-31-dev-knowledge-architect — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-08-28-dev-knowledge-architect/` was added.

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

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**1 · Ten `consumer_at_landing` WARNs cannot clear by citation, and that is structural.** They are the seven frozen batch-D lane contracts, the batch-3 manifest and the codex-fate map. The census pool excludes `docs/audits/` BY DESIGN, so batch machinery citing batch machinery is exactly what that exclusion refuses. Their consumption is real; its evidence is a merge commit, not a citation. Reported, not absorbed.

**2 · The batch-3 manifest is INERT and stays that way.** It carries `status: open` and no `closed_by:`, and `open_batches()` returns `[]` -- a manifest with no `closed_by` *"opens nothing at all"*. `docs/audits/` is immutable so it is not corrected; the ruling applies to the NEXT batch, and the freeze predicate now refuses a dispatch that would repeat it.

**3 · One intake is past its READY threshold.** `docs/intake/2026-07-16-satellite-onboarding-prompts.md`, READY 46 days against the ruled 30, carrying no `review-date:`. This is FM-2 leg (d) working, not a defect -- it is the leg's first live finding and it has been open since the leg armed.

**4 · Pre-existing suite REDs are NOT this window's.** Verified by checking out `66662c70` and re-running the identical node ids; the stale batch-1 fixture (`test_vi_batch1_reproduces_the_wrong_id_citation`) is named in the wave-2 close packet as the architect's.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->**Batch D, seven lanes, all landed or accounted for** -- and one of them landed by REFUSING. Map: `docs/audits/2026-08-29-technical-batchd-launch-contracts/` (the frozen contracts), `docs/audits/2026-08-30-technical-autonomy-decision-tree.md` (55 findings, 100% routed), `ecosystem/north-star.md` (the arc set), `docs/audits/2026-08-30-technical-window-close-operator-brief.md` (the numbers).

Headline deltas: `CLAUDE.md` **39,147 -> 23,931 B**; FUNNEL HEALTH six `unavailable` -> six real numbers; SDA-1 floors UNCALIBRATED -> `C=3 H=5 M=5 L=2`; terra post-merge OWED -> `C=0 H=3 M=1 L=0`; ADR-114 executed; ADR-81 s45 discharged by ADR-116; ratchet **443 -> 443**.<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->**The order is the decision, and it is already made.** Four research lanes independently found one shape -- *this repo is an excellent environment and has no learning signal* -- which yields a sequence with no branch: **metric -> measure -> only then an optimizer**. That is why only 2 of 18 true gaps became rows and ten are parked behind named triggers.

**The open question the next seat inherits** is not *what to build* but *whether `[#625]` discriminates*. Its KEEP condition is falsifiable by design: a deliberately weakened instruction set must FAIL while the intact set passes, and **the config is deleted if it does not discriminate**. A harness that passes everything measures nothing, and the whole downstream arc rests on that one experiment being honest about its own null result.<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.

## §7 — BOOT POINTER: read the arc set before the backlog

`ecosystem/north-star.md` — **the arc set in dependency order, and what blocks what.** GENERATED
from `tasks/` (`scripts/gen_north_star.py --write`), so it cannot drift from the backlog the way a
hand-written roadmap does: arc names, order, done-when and starting contract are DECLARED; every
member row, status and count is DERIVED. Members select by **theme predicate**, so a row filed
tomorrow appears without editing the generator.

**Read it before `BACKLOG.md`.** The backlog is the complete list; this is the order. At close it
reads **162 open of 217 manifest-referenced, 55 deferred** — and it shows deferred per-arc
deliberately, because this window's most expensive defect was a deferred blocker nobody watched.

## §8 — SEAT LESSONS — four, and they share one shape

**All four are mechanisms whose failure mode is SILENCE.** The gates here are good at refusing bad
input and were, in each case, unable to report their own absence. That is the class to watch for.

1. **A gate that could not RUN.** `lane-contract-check` passes every staged contract to a command
   that took one path, so the first multi-contract commit died with *"unexpected extra
   arguments"* — it did not refuse a bad contract, it failed to execute, unnoticed past eleven
   prior contracts. **Fixed + 2 tests.**
2. **An explanation built on an UNREAD PREDICATE.** Two merges behaved differently; I theorised
   instead of reading `batch_manifest.py`. Both halves wrong, and the manifest I had credited with
   a fix was inert. **It failed SAFE — which is exactly why the wrong model survived to be built
   on.** Operator rule: *"appears to" stays a guess until the predicate is quoted.*
3. **A decision premise from a SUMMARY, not the register.** A contract said `codex/` was *"gone
   either way"*, authored from the operator's *"no single-file folders"*. Z-G5 says four lines
   down that it is *"not free to delete"*. The summary carried the rule; the register carried its
   SCOPE. **The lane refused, and was right** — compliance would have broken a live carrier.
4. **A teardown that iterated the WRONG ENUM.** Batch D dispatched across local and cloud
   substrates; teardown iterated local branches only, stranding a 259-line ADR on origin while the
   batch looked complete. *"No leftovers"* was satisfied locally.

**The JOURNAL anchor is a hexadecimal on an `Anchors:` line**, not a sentence — `journal_anchor`
counts a SHA as RECORDED only on a line matching `^\*{0,2}Anchors?\b`. Prose mentions produce 719
`anchored by mention` WARNs, which is `[#623]`.

## §9 — NEXT WINDOW'S FIRST RULED ARC

**Two arcs, and the order between them is already ruled.**

**A · DOCTRINE CONSOLIDATION — continuation.** Batch D landed its first wave (README recreated,
`CLAUDE.md` re-genred 39,147 → 23,931 B, `codex/` universalised). What remains is in
`ecosystem/north-star.md` arc 3 and the batch-D contracts directory. **Not blocked.**

**B · AUTONOMY — from the decision tree**
(`docs/audits/2026-08-30-technical-autonomy-decision-tree.md`). Its head is **`[#625]`**, the
rule-adherence eval corpus, born at this close by operator ruling after both fold targets proved
unusable. **The sequence has no branch in it: metric → measure → only then an optimizer.** Ten
further items are PARKED, each carrying the named trigger that releases it — most of them release
on `[#625]`.

**Do not work arc B ahead of `[#625]`.** Four research lanes independently found that this repo is
an excellent environment with no learning signal; every absent property is downstream of a
measurement that does not yet exist, and a gap worked ahead of its blocker is work optimising
against nothing.

**Carried, unresolved, and the operator's:** whether to arm the next batch manifest's `closed_by:`
(ruled mandatory at dispatch — apply on the next batch, not retroactively; batch-3's manifest is
immutable and stays inert).
