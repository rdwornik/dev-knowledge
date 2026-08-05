# Residual — 2026-08-05-dev-knowledge-architect — the part the repo does not already encode

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
**Every WARN class the gate currently raises is STANDING and already carries a register entry** —
`no_ff_merges` (the legacy journal-wrap / transcript-archive entries), `reconciled_versions` (the
CONTRIBUTING template row, ref `#335`), the `undeclared_edges` handoff-process family (ref `#241`),
`fleet_parity` (the ai-council root `conftest.py` row, ref `#430`), `preflight_backlog_ids` (ref
`#310`, advisory per `[#483]`'s ruling R3). None of these is new; read them at
`ecosystem/disposition-register.yaml`.

**One disposition IS new this window and is deliberately time-boxed** — the `doc_rot`
backlog-accretion entry for `[#492]`. The (e) close-out drained the other self-induced accretion by
rewording rather than by dispositioning it; `[#492]` was the single genuine rule-vs-ruling conflict,
because the ruled Grok peg adds a third dated block and the detector keys on dates. It carries a
review date and retires on the flip — check the register, not this line, for its state.

**One is an EXEMPTION, not a disposition, and it expires by design** — the TEMPORARY
`ecosystem/doc-code-edge.yaml` entry covering the new review-artifact-coverage leg. `[#499]`'s
done-when owns its discharge (rider R2), so the exemption cannot outlive its reason. Distinct in kind
from `preflight_backlog_ids`' PERMANENT row.

**The load-bearing gap is what NO flag reports.** The (f) sweep found stale `ARCHITECTURE.md` claims
about the enforcement organs' failure postures and reported them **unfixed and unfiled** by ruling
(the window was closed to filings). They are therefore invisible to every check — they exist only in
JOURNAL prose, and no probe below will re-surface them. `[#497]` owns the same retired posture at
*different* sites and `[#408]` owns the mechanism that would prevent the class; neither owns these
contents. Treat the absence of a flag here as a scope statement, not as cleanliness — §4 carries the
decision.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail lives in `JOURNAL.md` 2026-08-05 (a)–(f); this is the map only.

- **`[#480]` closed** — the review-artifact coverage leg (advisory/WARN tier) plus the canonical
  artifact header grammar, measured before ruling. → JOURNAL (e)
- **`[#498]` closed** — a tracked exec bit on a carried hook script, fixed RED-first, with a
  structural (not enumerated) guard so the next carried script is covered without an edit. → (d)
- **`[#489]` retired** as a duplicate; `[#218]` carries the surviving scope.
- **`[#499]` + `[#500]` filed** — the evidence-gated hard flip of the coverage leg, and the
  session-end advisory that reads a correctly-closed row as nothing-closed. → (e), (d)
- **The night drafts adjudicated** — eight rows flipped open (`[#486]` `[#487]` `[#488]` `[#490]`
  `[#491]` `[#493]` `[#496]` `[#497]`), against the live rows rather than a restated list. → (c)
- **Night-batch verification + FR-1's honest limit discharged** — verified on the machine of record,
  not in the container that produced it. → (a), (b)
- **Intake #24 landed verbatim as DRAFT** — `docs/intake/2026-08-05-tech-currency-wave-1.md`; Part A
  excluded **mechanically** (extraction refuses on the marker; the landed slice re-probed for all
  five Part A signatures). No rows born by the filing. → (f)
- **Pre-seal currency sweep — zero regen-shaped fixes, and that is the finding**; the generated
  surfaces were already fresh. What it found instead is §1's unfiled class. → (f)

ADR surface: no new ADR this window. The binding recent ones are unchanged — see
`.claude/generated/recent-adrs.md` and `docs/decisions/README.md`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**1. Intake #24 — the decision is ADR-vs-rows, and it is an architectural posture question, not a
tooling shopping list.** The intake's claim is narrow and testable: this fleet is ahead on LLM-ops
discipline and behind on exactly one axis — **all hard enforcement is client-side**. If that holds,
"add a server-side wall" moves *where enforcement lives*, which is ADR-shaped (it changes the
enforcement-mesh model `ARCHITECTURE.md` Ch2 describes and the failure posture of every organ that
currently assumes local-only). If it does not, it decomposes into ordinary `[E2]` rows. Deciding that
first prevents the usual failure — filing six tool rows and discovering afterwards that they encode a
posture nobody ruled.

**2. The P1 candidate carries an unverified premise, so the first act may be a verification row.**
The intake states plainly that enforcing required-checks on **private** repos may need a paid plan,
and the repos stay private by standing ruling (employer material). A build row filed ahead of that
check can produce a report-only wall marketed as a gate — the exact fake-green class this repo's
doctrine exists to refuse. Report-only is still valuable (a tamper-proof server-side record, out of
local reach), but it is a *different* deliverable and should be named as one.

**3. Capacity, not appetite, sequences this.** §F pairs the intake's ~5-6 rows against `[#487]`'s
consumption engine as the compensating close. Two things to weigh: `[#487]`'s own measured precedent
is **near-zero precision** on the parked set (the WEAK heuristic keys on churn in large canonical
files), so it is a *judgment* arc, not throughput; and the session-start surfacing now reports a
parked count **above** the figure `[#487]`'s row text records, so the set has grown since filing.
Verify the live number before treating that row as the close engine.

**4. The ownership boundary for reported-but-unfiled defects is undecided, and it recurs.** The (f)
sweep did the right thing under a closed window — report, don't file, don't widen a row's scope by
assertion. But the residue then has no owner and no gate: it lives in JOURNAL prose and dies there.
The open question is whether that is by design (a closed window legitimately drops findings) or
whether the sealing arc needs a durable landing surface — a sweep-residue row, an intake, or a rule
that a seal files what it reports. This is the second consecutive window in which `ARCHITECTURE.md`
drift was found by hand; `[#408]` already cites that fact in its own body.

**5. `silent_rule_ratchet` vs richly-commented config is a structural tension, flagged twice in one
arc.** Explanatory prose in `ecosystem/*.yaml` tripped the detector from a disposition comment and
from an exemption comment; both were drained by rewording with the baseline **held**, never raised.
The detector's scope and the practice of writing *why* into config are pulling against each other.
Intake #24's P6 names `vale` as the evaluation candidate for exactly this case, with a
measured-divergence bar. Options: narrow the detector's scope, accept the rewording tax as the price
of a ratchet that cannot be gamed, or measure the `vale` overlap first.

**6. `[#499]`'s evidence bar is a cadence commitment that nothing mechanically enforces.** The hard
flip opens on *0 false positives reported at two consecutive seals*. If a seal does not report that
count, the row never opens and nothing goes red — a deferral that decays into a disclaimer, which is
the class ADR-81 (d) exists to prevent. Either the seal ritual acquires the reporting obligation, or
the bar needs a different shape.

**7. `[#490]` is declared a precondition to any further `[#383]` wave.** Parity resolves a subset of
the ADR-104-declared members while every "fleet parity GREEN" reads as a claim about the fleet. The
`membership_agreement` check already prints the split honestly, so the question is purely
sequencing: close the manifest to 9/9 first, or let waves proceed on a declared subset with the
partial-coverage caveat carried into the wave record.

**8. Standing operational queues awaiting an operator/architect verdict, not CC action.** Nightly
triage findings are parked in the Issues tab; `changelog_sentinel` reports the Claude Code version
has advanced well past the last reviewed one and `/changelog-review` is **PUSH-trigger-only** by
design, so it waits on the operator. Neither is a defect — both are cadence decisions.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
