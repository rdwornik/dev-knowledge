# ADR-116: The fuzzy-band acceptance shape — non-binary closure for decks, prose and judgment artifacts

- **Status:** Proposed
- **Date:** 2026-08-29
- **Decision tier:** Architecture (Path A — design lane output, awaiting architect ratification)
- **Amends:** none — ADR-81 §"Scope — deterministic only; fuzzy deferred" **named** this arc; this ADR **discharges** that deferral. ADR-81's own text stands unchanged.
- **Related:** ADR-81 (the deferral this discharges, and the deterministic contract this deliberately does not touch); ADR-111 (finding triage — a disposition funnel for *findings*, not an acceptance shape for *artifacts*); ADR-112 (adoption tiers — a routing rule for *candidates*); ADR-85 (session-close scope, distinct); ADR-100 §4 (separate genres, separate lifecycles, *"governed oppositely on purpose"* — see the locator note below)
- **Decommission:** none
- **Source:** lane `lane-f-000-adr81-fuzzy-band`, cloud substrate, 2026-08-29; exercised on two artifacts from this repo's own corpus before being written down.

<!-- Decommission: none -->

## Context

ADR-81's 2026-06-24 amendment binds **deterministic build tasks** to a frozen, executable, test-first
acceptance contract. Its final scope paragraph then names what it cannot bind:

> The **fuzzy band** — decks, prose, judgment artifacts where closure cannot be an exact pass/fail — is
> **explicitly deferred to its own arc** (it needs a different, non-binary acceptance shape).

That deferral has been open since 2026-06-24. At the time of writing,
`grep -rn "fuzzy" tasks/ docs/decisions/` returns exactly two hits: the deferral line itself
(`ADR-81:45`) and an unrelated use in `ADR-85:12` ("no longer a fuzzy semantic question"). **No other
surface owns it.** Meanwhile the repo has kept shipping fuzzy artifacts — handoff bundles, censuses,
audit packets, residuals, close packets — and has closed each one on the author's word.

The gap is not that these artifacts are ungoverned. It is that the governance is **invented per
artifact**, so a strong instance and a weak instance are indistinguishable at the point of closure: both
end with a file and a claim. The corpus already contains the ingredients of a shape — it has just never
been written as one.

**This ADR is deliberately a distillation, not an invention.** Every load-bearing clause below was
lifted from a place this repo already got it right, and each is cited to that place. What is new is the
partition, the verdict vocabulary and the refusal rule.

## Decision

### The unit of acceptance

**The acceptance unit is the smallest artifact that has its own addressee.** Not the directory, not the
bundle, not the arc. (Earned by exercise — see "Where the shape bit", finding E1: judging a five-file
handoff bundle as one unit averaged an excellent mechanical rind over an empty judgment core and hid
the hole entirely.)

### The partition, which is the whole idea

Every fuzzy artifact splits into two parts, and the split is a **per-instance declaration**, never a
property of the artifact's class:

- the **rind** — every leg that *does* reduce to an exact check, given the tooling actually reachable
  when the artifact was authored;
- the **core** — what is left, where closure is a judgment.

"Fuzzy" is a description of the core. It is **not a property an artifact may claim**; it is what
remains after the rind has been made as large as the reachable tooling allows. An artifact that calls
itself fuzzy while leaving a mechanizable leg unmechanized has not entered this band — it has laundered
a defect into one.

### The four legs — F1 to F4

The architect authors these **before** the work and freezes them, exactly as ADR-81's 2026-06-24
amendment requires for the deterministic band. Same immutability property, restated for this band:

> The executor may **tighten** — add a leg, sharpen a criterion, or **promote** a core leg into the rind
> by mechanizing it. The executor may never **soften** — delete a leg, narrow the addressee, or
> **demote** a rind leg into the core. Promotion is always allowed and always improves the contract;
> demotion is a weakening and requires the architect.

**F1 — Addressee and next act.** Name the reader, and name the decision or act the artifact must make
possible. Fuzzy closure is *relative to a consumer*: "good prose" is unfalsifiable, "the next seat boots
without asking a question this bundle could have answered" is not. This is the corpus's own
**zero-questions test** (`docs/intake/2026-08-26-tech-handoff-operator-interface.md`,
§"Acceptance criteria (ex-ante)" item 5: *"The operator judges; it is the same acceptance shape as I4's
zero-questions test."*).

**F2 — The rind, enumerated and exhaustive.** List every mechanizable leg and gate it binary. A leg that
was mechanizable and was not mechanized is a **defect**, not a fuzzy leg. Where a rind leg is real but
**unreachable** — the tool exists but could not be run — it is recorded in the corpus's existing
`MEASUREMENT-OWED` form: *the claim is owed, never estimated*
(`docs/audits/2026-08-29-census-nb2-funnel.md` §8). An owed measurement is an honest incomplete rind. A
silently skipped one is a false one.

**F3 — The core, with a graded verdict and a named judging role.** Each core leg carries an ex-ante
criterion and resolves to exactly one of three verdicts:

```
MET                      the criterion is satisfied
MET-WITH-NAMED-LIMIT     satisfied within a boundary the artifact states itself
NOT-MET                  not satisfied
```

No core leg without a criterion; no criterion without a **role** that judges it. The judge is named as
a *role*, never an identity — the judge of a handoff bundle is a seat that does not exist yet at freeze
time (earned by exercise, finding E2).

Where the criterion is stated **negatively** — as a failure mode the artifact must not exhibit — it is
paired with its inverse, or it is explicitly marked one-sided. **A one-sided anti-criterion is bluffable
by inversion** (earned by exercise, finding E3).

**F4 — The self-falsifier.** The artifact ships three things:

1. its declared limits;
2. at least one **measured** place where its own earlier pass was wrong, or where its method does not
   reach;
3. what a reader must do to **overturn** it.

Zero declared limits is `NOT-MET` on F4 by construction. This is the fuzzy analogue of ADR-81's
xfail-strict exemplar: in the deterministic band a frozen decorator makes a premature green *fail*; in
this band the named limit and the measured self-error are what a premature green cannot produce.

### Anti-bluff — carried over unchanged

An ex-ante criterion **states the question, never the answer**. A criterion carrying its expected
verdict is bluffable, for the same reason a probe carrying its answer is
(`HANDOFF_PROCESS.md` §5; enforced there by `scripts/verify_handoff_probes.py`, which FAILs any probe
row printing an `expected:` value). Generation-time hints go to the record the reader never sees, not
into the contract.

### The refusal rule — where the shape is actually non-binary

Closure is declared on the **worst verdict in the core** and the **completeness of the rind**, and it is
declared in public. An artifact closes as exactly one of:

```
ACCEPTED                     rind complete, every core leg MET
ACCEPTED-WITH-NAMED-LIMITS   the limits are named IN the artifact, and the addressee accepts them
RETURNED                     a leg is unnamed, or the addressee declines the residue
```

**A core leg at `NOT-MET` does not automatically block.** It blocks *unless the acceptance record names
it and the addressee accepts it anyway*. What this shape forbids is not imperfection — it is **silence**.
Closure never reduces to a number, a percentage or a score, and two `ACCEPTED-WITH-NAMED-LIMITS`
artifacts are not rankable against each other. That is the point: the output is a three-valued
disposition carrying named residue, not a boolean and not a grade.

## What this does NOT cover — stated so the deterministic band is not quietly re-litigated

- **The deterministic band is untouched.** ADR-81 legs (a)–(e) and its 2026-06-24 frozen executable
  acceptance contract bind exactly as before. Where "done" reduces to an exact executable assertion,
  **ADR-81 binds and this ADR is not available.** F2 is the boundary: it exists to keep as much work as
  possible on ADR-81's side of the line.
- **This is not an opt-out.** An artifact does not enter this band by declaring itself fuzzy. F2's
  exhaustiveness requirement is the entry test.
- **No code artifact is in this band.** Code has an executable acceptance contract by construction.
- **This does not govern findings or candidates.** ADR-111 routes a *finding* into one of four
  outcomes; ADR-112 routes a *candidate* into a tier. This routes an *artifact* to a disposition.
  Three different questions.
- **This is not a session-close gate.** ADR-85 and `protocols/DEFINITION_OF_DONE.md` own that scope.
- **No ranking, no score, no aggregate.** There is deliberately no "fuzzy quality metric".
- **No organ is claimed.** Per ADR-81 leg (d), an **explicit deferral** rather than a silent gap: a
  shape gate could check that an acceptance record *carries* F1–F4 and a disposition — shape only, in
  the manner of `lane-contract-check` — and it is **not built**. It is named here as a candidate, and
  nothing below claims it exists. A gate over the *content* of a core leg is not merely unbuilt but
  refused, per the honest-narrowing law quoted below.

## The exercise — two real artifacts from this corpus

An acceptance shape never run against a real artifact is a proposal, not a shape. Both artifacts below
are in-repo and were read before the shape was written. **Neither was chosen for being flattering, and
the negative results are the point.**

### Artifact 1 — `docs/handoffs/2026-08-28-dev-knowledge-architect/` (handoff bundle, prose + judgment)

Applied per-file, per the unit rule; verdicts below are for the bundle's two governing files.

| Leg | Verdict | Evidence |
|---|---|---|
| F1 | `MET-WITH-NAMED-LIMIT` | addressee and next act are both explicit (incoming architect seat; resume `[E2]`/`[E9]` without re-deriving the window), and the §13(d) beat narrowing to *"anything changed?"* is the zero-questions test in all but name — but it is stated as a **fact about the bundle**, never authored as a criterion before generation. Post-hoc, not frozen. |
| F2 | `MET` | the strongest rind in the corpus: `PROBES.md` P0a/P0b/P0c and P3, plus `verify_handoff_probes`, `check_handoff_probes`, `validate_residual_completeness`, `check_seal_identity`. It goes further than F2 asks and states which legs deliberately carry **no** probe leg (worktree, write-scope, mode-basis) with the reason. |
| F3 | `NOT-MET` | the core legs are *named* — hand-authored Purpose, write-scope prose, mode-basis prose, `RESIDUAL.md` §4 next-frontier decisions — and then left without a criterion, without a judging role, and with no verdict recorded anywhere. P0c is explicit: *"Whether the Purpose genuinely serves that authority is an architect judgment, deliberately outside the mechanical check."* Correct to exclude it from the probe. But nothing else ever picks it up. |
| F4 | `MET-WITH-NAMED-LIMIT` | limits are declared and reasoned (R3; the "honest narrowing (terra H3)" on P0b; the Windows cp1252 caveat). No measured self-error, and no overturn instruction. |

**Disposition: `ACCEPTED-WITH-NAMED-LIMITS`.** Residue: **F3 has no rubric and no recorded verdict.**

This is the finding worth carrying: the handoff machinery mechanized its rind superbly, correctly
identified which legs could not be mechanized, wrote down *why* — and then let the core fall on the
floor. The bundle's own law explains how it happened and does not cover it:

> a leg with no mechanical counterpart cannot fail honestly, and one that cannot fail honestly
> discredits the whole block (R3)

That law is right, and it argues only for keeping the judgment leg **out of the probe block**. It does
not say the leg needs no criterion — but read as a stopping point, that is how it was used.

### Artifact 2 — `docs/audits/2026-08-29-census-nb2-funnel.md` (funnel census, judgment artifact)

| Leg | Verdict | Evidence |
|---|---|---|
| F1 | `MET` | the addressee is named by name and repeatedly (*"each is named because FM-3 inherits them"*), and the next act — the archival worklist — is what the artifact exists to enable. The best F1 in the corpus. |
| F2 | `MET-WITH-NAMED-LIMIT` | counts, the mechanical citation graph, §9's reproduction commands and the zero-write proof are all exact; the two scripts that could run under bare `python3` did, and their outputs are labelled measurements. §8 then declares the rind **incomplete and why** — container `uv` 0.8.17 against `required-version = "==0.11.19"`, so five gate verdicts are `MEASUREMENT-OWED-LOCAL`, *"owed, never estimated"*. |
| F3 | `MET` | criteria were ex-ante and in the brief: class precedence (§1.5), the terminal-state test (§1.4), the governance pool COPIED rather than re-decided (§1.3), and a stated failure mode. Verdicts are recorded in §7 rather than assumed. |
| F4 | `MET` | the reference implementation. It reports a **42 % false-orphan rate in its own first pass** (19 → 11), a **25 % error rate on its highest-consequence list** (intake #42, refuted by opening ADR-115), a third instance of the same class (61 → 24 dangling refs), four named method limits, and the honest inversion — ORPHAN was not the plurality, but PROTECTED at 94.1 % is *the other way to look complete*, so the consumption sub-axis is published underneath it where unconsumed **is** the plurality at 70.6 %. |

**Disposition: `ACCEPTED-WITH-NAMED-LIMITS`.** Residue: **five owed measurements**, each named.

## Where the shape bit — the negative results, which are first-class

The shape did not survive contact unchanged. Four findings; the first three are folded into the
Decision above, and the fourth is not repairable and is therefore named.

- **E1 — the shape had no unit rule, and needed one.** Judging the handoff *bundle* as a single artifact
  averaged `PROBES.md` (near-total rind) against `RESIDUAL.md` §4 (near-total core) and produced a
  comfortable middling verdict that concealed an empty F3. The unit rule — *the smallest artifact with
  its own addressee* — exists because of this, not before it.
- **E2 — "named judge" was wrong as first drafted.** The judge of a handoff bundle is a seat that does
  not exist when the bundle is frozen. F3 therefore names a **role**, never an identity.
- **E3 — a one-sided anti-criterion is bluffable by inversion.** The census's brief gated on a failure
  mode (*"a census routing most objects to ORPHAN without evidence has not censused"*). The census
  cleanly passed it — 1.2 % ORPHAN — and then had to **invent the inverse check itself**, because
  PROTECTED at 94.1 % is an equally vacuous way to look complete and the brief closed only one
  direction. A criterion stated as a prohibition needs its inverse, or an explicit one-sided marker.
- **E4 — F4 is monotone in effort, not in quality, and this is not fixable here.** A thorough artifact
  reports more self-error; a sloppy one reports none; an author who wants a clean F4 can manufacture
  trivial self-corrections. There is no mechanical defense, and inventing one would violate the
  honest-narrowing law this ADR adopts. The partial mitigation is that F4's third clause — *what a
  reader must do to overturn this* — is the hardest of the three to fake self-servingly, because it
  hands the reader a live weapon. **Recorded as a known hole, not solved.**

A fifth observation, not a defect: the rind/core boundary **moved during artifact 2's own life** — two
scripts ran under bare `python3` and promoted their numbers from judgment to measurement, while five
gate verdicts stayed unreachable. This is why the partition is a per-instance declaration carrying its
environment, and not a fact about artifact classes.

## Consequences

- **Easier:** a fuzzy artifact now closes on a stated disposition with named residue rather than on the
  author's word; a weak instance and a strong one become distinguishable at the point of closure;
  ADR-81 §45's oldest open deferral is discharged rather than re-deferred; the corpus's best existing
  practices (`MEASUREMENT-OWED`, anti-bluff, the zero-questions test, the honest inversion) gain one
  home instead of being re-invented per artifact.
- **Harder / cost:** every fuzzy artifact now needs an ex-ante frozen contract, which is work the
  architect must do *before* dispatch, not after; F2's exhaustiveness requirement will convert some
  comfortable "fuzzy" work back into mechanizable work that someone has to mechanize; and F4 asks
  authors to publish their own error rates, which is culturally expensive and, per E4, imperfectly
  verifiable.
- **Deliberately not obtained:** no organ, no gate, no automated verdict. This band's core is
  unmechanizable by definition, and a gate over it would be exactly the leg-that-cannot-fail-honestly
  the shape refuses.

## Alternatives considered

- **Extend ADR-81's frozen executable contract to fuzzy artifacts by loosening "executable".** Rejected:
  this is what the deferral existed to prevent. A criterion that is called executable and is not
  produces the R3 defect at ADR-81's scale.
- **A rubric with a numeric score and a passing threshold.** Rejected: it restores a boolean by the back
  door, invites optimization against the score, and would collapse axes that disagree. The corpus's own
  worked example is artifact 2, whose two axes disagree (PROTECTED 94.1 % against unconsumed 70.6 %) and
  where publishing both is the honest act. **Locator note, recorded because this ADR's own rule requires
  resolving a citation before acting on it:** artifact 2 attributes that non-collapse principle to
  "ADR-100 §4". ADR-100 §4 was opened. Its text rules that **audit and intake are separate genres with
  separate lifecycles, "governed oppositely on purpose"** — it says nothing about retention-versus-
  consumption axes. The census's use is a defensible *extension* of §4's spirit, not its text, and it is
  cited here as an extension so the next reader does not inherit it as a ruling.
- **Peer review as the whole shape — one reader signs off.** Rejected: it is what already happens, it is
  the thing that made strong and weak instances indistinguishable, and it supplies no record. The
  named-limits disposition is the minimum artifact a later reader can audit.
- **Leave the deferral open until an organ can enforce it.** Rejected: the deferral has been open since
  2026-06-24, an organ is not obtainable for this band (see Consequences), and waiting for one is how a
  named deferral becomes a silent gap.
