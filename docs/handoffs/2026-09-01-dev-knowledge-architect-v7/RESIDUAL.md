# Residual — 2026-09-01-dev-knowledge-architect-v7 — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-08-31-dev-knowledge-architect/` was added.

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
**The one judgment: the five OPEN rows are a DECISION, not a defect.** Batch F merged eight
lanes and closed **zero** rows. That is deliberate. Terra's pre-merge pass refused something in
all but one lane, and in five cases the defect defeats the row's own stated purpose — a
predicate that is never invoked, a waiver that fails open, a freshness gate pointing at a file
whose absence makes it silently skip. Those rows were left OPEN rather than closed on "tests
pass, merged". Read every one of them as *chosen*, and re-open the choice only with the packet
in hand: `docs/audits/2026-09-02-technical-batch-f-close-packet.md` §3.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
```
[#611]  HANDOFF_PROCESS v6.3.0 -> v7.0.0, cut as ONE coupled release act; /boot-session +
        boot_frontier.py + the FUNNEL HEALTH digest + spec sec17. ROW OPEN -- its Done-when
        also requires a measured paste from a real cut, which is THIS bundle.
[#632]  the codespace long-run proof RAN and REPORTED. Two Z-G3 W4 blockers measured CLOSED
        (uv IS present; the clone IS fresh); a third fixed at dispatch. Verdict RED at L5.
[#621][#626][#276][#629][#630][#627]  all merged, all OPEN, each with a named defect and a
        named fix direction -- see the close packet sec3. This is G's most concrete inventory.
[#614]  batch F CLOSED. dashboard home ruled to docs/dashboard/; the article brief disposed.
```
Detail lives in JOURNAL `(ai)` `(aj)` `(ak)` and the close packet — not restated here.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**1. The substrate decision is now evidence-bound, and the evidence is split.** The operator's
ruling was: Codespaces becomes the DEFAULT execution substrate *on green*. The proof lane's own
verdict is **RED at L5**, so it stays non-default — but L1–L4 and L6 are GREEN and two of the
three Z-G3 W4 blockers are now measured false. The open question is no longer *does it work*;
it is **whether an L5 RED made of pre-existing suite failures should gate a substrate decision
at all** — and terra removed the lane's argument that those failures are container-independent.
That is the first thing to rule on.

**2. The auth mechanism in the container is not what the runbook says it is.** `[#632]` L2:
`CLAUDE_CODE_OAUTH_TOKEN` is UNSET, the dispatched agent authenticates over some other live
channel, and a **nested** `claude -p` reproduces the "Not logged in" trap verbatim. Any design
that assumes a script can shell out to `claude` mid-lane is building on that trap.

**3. The lane/copy split is a doctrine gap, not six coincidences.** Five of eight lanes fixed a
root copy and missed the copy that executes. Nothing in the contract template asks "which copy
actually runs?" — that is a cheap, high-yield addition to the freeze gate.

**4. The integrator's own fan-out has no budget.** The 6/12 concurrency ruling governs LANES.
It held. What broke was the SEAT: three concurrent terra reviews produced two hard failures
(codex OOM twice; a fork-exhaustion that killed a push). Nobody has costed the integrator's
parallelism, and G should.

**5. HISTORY DELTA and EQUILIBRIUM MAP** — the operator's batch-G seed, this window. A first
hand-derived cut of both is committed at
`docs/audits/2026-09-01-technical-v7-history-delta-equilibrium-map.md`; the seed itself is the
close packet sec8. They are hand-derived ON PURPOSE — G builds the generator, and this cut exists
so G is specifying against a worked example rather than a description.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
