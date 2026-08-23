# ADR-86: Conformance-dashboard location — `ecosystem/conformance.md` as an ADR-80 committed-generated zone

**Status:** Accepted
**Date:** 2026-06-16
**Decision tier:** Architecture (Path A — architect/operator decision, captured in the 2026-06-16 consolidation pass; originates from ADR-85 R2)

## Context
ADR-85 R2 deferred ungated-doc staleness detection (and the broader claims-vs-state conformance surface) to "the daily digest / **conformance dashboard**" — but never said *where* that dashboard lives, *in what zone class*, or *how it is maintained*. BACKLOG #169 (the ADR-85 R2 staleness signal) and any future conformance surface therefore had **no build target**: they "ride with the conformance-dashboard work" against a dashboard that was named but never located. This left the decision recorded nowhere (the 2026-06-16 consolidation survey found it absent from every ADR, the JOURNAL, and BACKLOG). The dashboard must satisfy the repo's standing invariants: deterministic, **read-only-generated** (Layer-2 never executes — `scripts/` validators only), and **committed** so it is diffable and auditable across runs rather than regenerated-on-demand.

## Decision
1. **Location.** The conformance dashboard lives at **`ecosystem/conformance.md`** — alongside the existing `ecosystem/` registry/state artifacts (the natural home for cross-repo conformance state).
2. **Zone class: ADR-80 committed-generated.** A read-only validator **generates it and commits its own output** under the ADR-80 writer policy (pathspec-bounded — never `git add -A`; fail-soft; the automation commits only its own file). This preserves the Layer-2 "validators only / never executes cross-repo" invariant (ADR-28/ADR-36): the dashboard is *produced by* a validator, it does not *drive* anything.
3. **Navigation (Ch2 pointer).** `ARCHITECTURE.md` Ch2 (organ map) gains a pointer to the dashboard — resolving the **G7** coverage-matrix gap (the organ map should point to the conformance surface). The pointer **lands with the build, not before**: a pointer to a not-yet-generated file would itself be drift, so it is part of the build item (#171), gated by the build's own freshness discipline.
4. **It is the surface ADR-85 R2 / #169's ungated-doc staleness signal lands in** — deterministic, not per-session-gated, not human memory.

**Deferred to the build (#171), not decided here:** the exact write channel (committed on `main` as a navigable surface vs. an `automation/*` branch per the ADR-84 writer-isolation pattern), the generator's check set, and the freshness/staleness hook. This ADR settles **location + zone class + navigation intent**; the mechanism is #171.

## Consequences
**Positive:** #169 and the conformance surface now have a concrete build target; the dashboard is deterministic, diffable, and Layer-2-safe; it reuses the existing ADR-80 writer pattern (no new mechanism invented). The location decision that G7 was blocked on is now recorded in the decision archive rather than living only as ADR-85's deferred R2 prose.
**Negative / accepted:** the dashboard is a **decision only** here — it is not built (the build is #171), so ADR-85 R2 staleness detection has no live home until #171 ships; the on-`main`-vs-`automation/*` channel question stays open until then.

## Alternatives rejected
- **Dedicated `automation/*` branch only (the ADR-84 nightly-digest model).** Rejected as the *primary* framing: the conformance dashboard is a durable, navigable surface that ARCHITECTURE Ch2 points to, not unattended write-output that must be isolated from `main`. (The channel may still borrow ADR-84 plumbing at build time — that is #171's call, not a reason to define the dashboard as branch-only.)
- **Generated-on-demand / not committed.** Rejected: not diffable or auditable across runs; the value is a committed artifact whose history shows conformance drift over time.
- **Folding it into the nightly digest.** Rejected: the digest is a point-in-time `docs/audits/*` record (append-one-per-night); the dashboard is a single living-but-generated surface — different lifecycle.

## Links
- ADR-85 (R2 — the originating deferral; this ADR locates the dashboard R2 named)
- ADR-80 (committed-generated zone / writer policy reused here)
- ADR-84 (automation-writer branch isolation — candidate plumbing for #171's channel choice)
- BACKLOG #169 (the staleness signal that lands here) · #171 (the build item)
- `ARCHITECTURE.md` Ch2 Organ map (the pointer target — pointer added by #171)

---

## Amendment — 2026-08-23 (R1: a human or integrator commit satisfies "committed"; §2's *self*-committing writer clause is withdrawn)

**Form.** Appended marker, per `CLAUDE.md` §5 rule 3 ("supersede with a new file or an in-file
amendment marker; never edit in place") and `protocols/STANDING_RULINGS.md` **J-3**. §2's original
text above is unmodified and remains the record of what was decided on 2026-06-16.

**What was wrong.** §2 classifies the dashboard as an ADR-80 committed-generated zone in which
"a read-only validator **generates it and commits its own output**". Measured live at `aeec0fd1`
on 2026-08-23: **no such code path has ever existed.** `gen_dashboard.py::write_outputs` writes two
files and returns `0`; its only `subprocess` site is `GitReader`, which reads. Every commit that has
ever updated `ecosystem/conformance.{md,html}` was made by a human. The clause was not drifted-from
— it was **never implemented**, and both artifact faces repeated it to every reader, which is how a
review pass came to judge `[#171]`'s "committed" leg met by reading the header rather than the
mechanism.

**The ruling — option (b).** **A human or integrator commit satisfies "committed."** The dashboard
is generated by `python scripts/gen_dashboard.py --write` and committed by the person or integrator
who ran it, pathspec-bounded to the two output paths, inside the ordinary branch → `--no-ff` merge
discipline. This also settles the channel question §2's *Deferred to the build* paragraph left
open: **committed on `main` as a navigable surface**, not an `automation/*` branch — the ADR-84
isolation pattern is for unattended writers, and there is no unattended writer here.

**Why (b) and not (a) — the evidence, not a preference.** Every `git add` / `git commit` subprocess
site under `scripts/` was enumerated on 2026-08-23: `enforcement_coverage.py` (throwaway probe
clones), `nopack_sandbox.py` (a fixture tree), and three read-only sites
(`review_closures.py:187`, `single_flight.py:419`, `cloud_provisioning.py:322`). **No generator in
this repo commits its own output. ADR-80 §3's writer policy has zero implementations here.** The
shape all eight generators do follow is *write → print → a human commits → a `--check`
regen-and-diff hook refuses a stale copy* — the shape `BACKLOG.md` has run on since the ADR-107
§7.2 source-of-truth flip. Option (a) would have added the repo's **first** self-committing writer,
with its own failure surface (locked index, mid-merge, diverged `main`), to solve a problem
convention had already solved.

**What §2 keeps, and what it loses.** Unchanged: the location `ecosystem/conformance.md`, the
ADR-80 **committed-generated** *zone class* and its name, the Layer-2 posture (ADR-28/36), the
pathspec-bounded discipline, and the diffable-and-auditable rationale that rejected
generate-on-demand. Withdrawn: only the clause that the **validator itself** performs the commit.
The zone class was always about the artifact's *state* — committed rather than regenerated on
demand — and that property is fully preserved by (b).

**ADR-80 §3 is not repealed.** Its writer policy (Option b + the three riders) stays live doctrine
for any unattended job that dirties the tree. It is simply **not the mechanism for this artifact**,
and this ADR no longer claims it is.

**The gap (b) does not close, and what was done about it.** (b) answers *is the header true?* It
does not answer *is the output current?* — an honest header on a stale trust surface is still a
stale trust surface. So this amendment ships with a **staleness leg on the ship-gate**: WARN, armed
at the measured 2026-08-23 baseline of **3 days** between the artifact's commit date and the newest
commit date across its declared input set, forbidding it from getting worse. WARN, not FAIL: RED is
a later act with its own ruling. The leg is implemented in
`scripts/generated_artifact_freshness.py`; its `ALL_CHECKS` registration ships as a fenced diff in
`docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md` §5 because `audit.py` is a
shared-collision file this batch, so **the leg is written and tested but not yet armed** — an
explicit ADR-81 (d) deferral, named here rather than left for a later audit to rediscover.

**Still open, unchanged by this amendment.** `gen_dashboard.py --check` is armed nowhere — the lone
ungated committed-generated surface in this repo (R3 **F5**). That is a *gating* gap, not a *writer*
gap; the Phase-0 packet is explicit that the two are separate defects, and F5 is not disposed of
here.

**Source:** architect ruling **R1**, `LANE-L4-dashboard-commit-path.md` (REISSUE, 2026-08-23),
executed by lane L4. Evidence: `docs/audits/2026-08-23-technical-phase0-preconditions.md` §Premise B
(CONFIRMED) and §Premise A (which REFUTED the claim that this fork had already been ruled);
`docs/audits/2026-08-23-technical-lane-docs-governance.md` §1 item 6 (R3 **F3**).
