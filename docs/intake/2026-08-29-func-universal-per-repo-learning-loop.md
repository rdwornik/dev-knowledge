---
intake-id: 63
status: DRAFT
origin: operator direction, stated verbatim mid-flight during the 2026-08-29 post-night reconcile-and-file pass; filed by the integrator under ADR-111's only path from a CANDIDATE, and explicitly evidence-gated on the AUT-R3 cloud lane
consumed-by:
---

# Universal per-repo learning loop — the hub deploys the mechanism, never the managed state

<!-- class: func (operator design input) · status: DRAFT — NOT ratified; DRAFT BINDS NOTHING.
Non-citable as doctrine until ratified; the repo wins on any conflict. -->
<!-- origin: operator direction, 2026-08-29 -->

> **DRAFT BINDS NOTHING.** This file records operator direction and the question it raises. It
> authorises no build, no dependency, and no change to any consumer repo. Nothing below is doctrine
> until this intake is ratified — and its ratification is **gated on measurement**, see §3.

## 1. The direction, in the operator's terms

> **"UNIVERSAL PER-REPO LEARNING LOOP — every consumer repo ships with an isolated self-learning
> layer (event loop → local index/memory → boot surface), hub deploys the MECHANISM never the
> managed state."**

Three properties are load-bearing in that sentence and each is a separate decision:

1. **Isolated per repo.** The learning layer's state belongs to the repo that produced it. No
   cross-repo state pool, and no consumer reading another consumer's index.
2. **Event loop → local index/memory → boot surface.** A closed loop: the repo's own events feed an
   index, and the index surfaces at boot where it can change what the next session does. A loop that
   does not reach the boot surface is a log, not a learning layer.
3. **The hub deploys the MECHANISM, never the managed state.** This is the ADR-28 Layer-2 invariant
   restated for a new organ class: the hub ships the carrier, and the state stays the consumer's.
   A hub that shipped the index would be driving state in a child repo.

## 2. Why this is not already covered

Reconciled before filing (2026-08-29): a search of `docs/intake/` for learning loops, per-repo
memory, local indexes and embeddings returned **no existing object**. The adjacent live objects are
related but distinct, and none of them owns this:

- the telemetry → trends → rulings loop is a **hub-local** feedback path, not a per-consumer one
- `LESSONS.md` is append-only prose, read by humans and agents, with **no index and no ranking**
- the funnel gates enforce lifecycle; they do not learn
- the C3 typed multi-layer graph (filed this same day) is the **substrate this would learn over**,
  not the learning layer itself

## 3. THE GATE — this intake does not ratify on argument

Ratification is **evidence-gated on the `AUT-R3` cloud lane** (dispatched 2026-08-29, read-only,
session `cse_01FteQFHM1VuYdQLypkwogGq`), whose deliverable is a survey of repo-as-reinforcement-
environment practice plus a **blind-spot list scored against our live organs** and a library-first
BUY-vs-BUILD sweep. Three of that lane's outputs bear directly here:

- axis **(b)** — what small local models are *actually* good at (retrieval, ranking, "where is
  what") versus not (decision-making, generation quality). If the evidence says the useful band is
  narrow, this intake narrows with it rather than being argued wider.
- axis **(d)** — the ABSENT column. If a property this intake assumes is already PRESENT, the scope
  shrinks; the blind-spot list is the scoping instrument.
- the **library-first sweep** — `sqlite-vec` is the natural first probe because this repo already
  runs sqlite by ruling R-A. ADR-112 Tier-L applies: evaluate before adopting, and the Windows-wheel
  + pinned-`uv` installability constraint (the `rustworkx` precedent) is first-class, not a footnote.

**A negative result from AUT-R3 is a valid outcome for this intake** and would properly close it
REJECTED with the reason recorded, which is the standing precedent for declined work here.

## 4. Open questions this intake does NOT answer

- What the index actually indexes, and whether "importance" is learned or declared.
- Whether the boot surface is a new organ or an extension of an existing generated surface — a new
  boot-time read has a byte cost paid every session, and the paste/boot-bytes panel is currently the
  only WORSENING trends panel (+11,232 B), so any addition argues against a measured headwind.
- Whether a per-repo model is a model at all, or an index plus ranking with no learned parameters.
  The operator's phrase is "small local models"; the evidence may say "index".
- The carrier shape: which deploy manifest component ships it, and what a consumer that declines it
  looks like.

## 5. Provenance and related objects

- North Star: the operator's MSc thesis, per the ruled THESIS-COMPARE input
  (`docs/audits/2026-08-29-technical-thesis-compare-out.md`)
- Substrate it would learn over: the C3 typed multi-layer graph
- Sibling governance question: intake #62 (L0 as a governed layer) — that one asks *who governs the
  global layer*; this one asks *what each repo learns for itself*. They meet at the boot surface.
- Layer invariant: ADR-28 (Layer 2 never executes), which property 3 above restates rather than
  amends.

## AMENDMENT — 2026-08-30: AUT-R3 has landed, and it answers §3's gate

> Appended, not edited. Filed by the integrator's AUTONOMY filing pass.

§3 above gated this intake's ratification on the AUT-R3 lane. That lane landed
(`docs/audits/2026-08-29-technical-aut-r3-repo-as-reinforcement-environment.md`) and was read
jointly with four siblings in `docs/audits/2026-08-29-technical-autonomy-synthesis.md`. Three of
its results bear directly here.

**1 · The diagnosis this intake assumed is CONFIRMED, and independently, four times.** AUT-R3 §2
states it: *"THIS REPO IS AN EXCELLENT ENVIRONMENT AND HAS NO LEARNING SIGNAL"* — PRESENT
concentrated in enforcement and honesty, ABSENT concentrated in feedback. AUT-R1, AUT-R2 and
AUT-R4-A reach the identical conclusion from domains that never touch. **Four lanes, four subjects,
one diagnosis** — a structural finding rather than four coincidences.

**2 · The ORDER is settled, and it constrains this intake rather than licensing it.** The joint
read gives a sequence with no branch: **metric first → measure the surface → only then ask whether
an optimizer beats hand-editing.** A per-repo learning layer sits *downstream* of a reward function
that does not yet exist. So this intake does NOT ratify ahead of intake #35's R3; it is sequenced
behind it, and building the loop first would be the same WRONG-ORDER error the synthesis names for
DSPy — *"an optimizer with no metric optimizes nothing."*

**3 · This intake's Tier-L call was RIGHT, and both cloud lanes got it wrong.** §3 says
*"ADR-112 Tier-L applies: evaluate before adopting"* for `sqlite-vec`. AUT-R3 Shelf 2 scored it
**"BUY, Tier-S"** and AUT-R4-B RANK 2 scored it **Tier S**. ADR-112's own guard sentence refuses
both: *"Tier S never touches gates, hooks that block, or `scripts/` — anything that would, is Tier
L by definition"*, and adopting it means editing `pyproject.toml` + `uv.lock` and writing a
`scripts/` embedding producer. **Neither cloud lane checked its tier label against ADR-112's text.**
Recorded because it is the same class as the two lessons filed 2026-08-29: a label carried forward
from the artifact that proposed it, rather than re-derived from the rule.

**One blocker DISCHARGED, and it needed this machine.** All three machinery lanes flagged
`sqlite-vec`'s Windows `enable_load_extension` availability as unanswerable from a cloud seat. The
synthesis lane ran it here: **it works** (Python 3.12.10, sqlite 3.49.1, under the pinned `uv`).
Shelf 2 stays open on merit rather than on an unknown, and **nothing was installed**.

**Consumed by:** `docs/audits/2026-08-29-technical-autonomy-synthesis.md` §1.2, §1.4, §1.5 and
§(d), plus the five AUT research artifacts it reads.

### Sources consumed by this intake, cited by name

The AUTONOMY research corpus this intake's §3 gate named, and which the 2026-08-30 amendment
above reads. Listed by filename because a citation the census can see is what makes an artifact
CONSUMED rather than an orphan — the alternative is 300-odd audits appearing only in a machine
baseline, which is the failure `[#595]` exists to end.

- `docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md` — axis 5 supplies the
  *"nothing measures organ usage"* half of the shared diagnosis.
- `docs/audits/2026-08-29-technical-aut-r2-decision-quality-frameworks.md` — Part 0E's measured
  options-decay (86% → 56%) and *"nothing surfaces it"*.
- `docs/audits/2026-08-29-technical-aut-r3-repo-as-reinforcement-environment.md` — the lane this
  intake's §3 gate names; §2 states the diagnosis this intake assumed.
- `docs/audits/2026-08-29-technical-aut-r4a-harness-evals-observability.md` — the SkillsBench
  negative-tail result and the harness-portability map.
- `docs/audits/2026-08-29-technical-aut-r4b-orchestration-memory-loop.md` — the RANK-1 derivation
  and the trust paragraph that adjudicates the shelf overlap.
- `docs/audits/2026-08-29-technical-aut-r4a-dispatch-brief.md`,
  `docs/audits/2026-08-29-technical-aut-r4b-dispatch-brief.md`,
  `docs/audits/2026-08-29-technical-aut-r4-dispatch-record.md` — the contracts those artifacts were
  produced under; an artifact without its contract is unauditable provenance.
- `docs/audits/2026-08-29-technical-autonomy-synthesis.md` — the joint read over all five.
- `docs/audits/2026-08-30-technical-autonomy-decision-tree.md` — where every finding above is
  routed to a row, an amendment, a rejection or a park.
- `docs/audits/2026-08-29-census-essentials-consumers.md` — batch-D lane e's census, read for the
  boot-surface half of this intake's open questions.
- `docs/audits/2026-08-29-technical-lane-f-fuzzy-band-design.md` and ADR-116 — the fuzzy-band
  acceptance shape, which is the non-binary scoring this loop would need.
- `docs/audits/2026-08-29-technical-sda1-adversarial-incumbent-baseline.md` — the adversarial
  incumbent baseline any learned component is scored against.
- `docs/audits/2026-08-29-technical-autonomy-arc-filing-packet.md` and `docs/audits/2026-08-29-technical-autonomy-arc-rejected-and-parked.md` — the arc's own filing record and its declined set; the rejections bound what a learning layer is allowed to re-propose.
- `docs/audits/2026-08-29-technical-nb2-wave-candidate-sweep.md` — the ADR-111 triage whose CANDIDATE column is the input pool any learned ranking would score.
- `docs/audits/2026-08-29-codex-e2-terra-post-merge-round6-lanes-n-i.md` — the post-merge round
  whose three honest-degrade Highs are the failure mode a learning loop would inherit.
