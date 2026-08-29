> **PROVENANCE — harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-D lane-f adr81-fuzzy-band` | receipt id `cse_01HHzS1D3WXL3zUWf1db43Uw` | dispatched 2026-08-29, harvested 2026-08-29 by `Save-CloudSessionReport` (the `Harvest-Cloud` alias).
> Selection rule: the LONGEST assistant text, not the last — text #3 of 11 across 4 pages.
> Bytes written unchanged: **14,979**. Harvester reported no deviation. NOTE: this lane also committed ADR-116 to branch claude/lane-f-000-adr81-fuzzy-band (d8f2993), unmerged.
> Nothing below this line was edited, reflowed or trimmed.

---

## RECEIPT

**Brief total line count: 98 lines** (between the `--- BEGIN BRIEF ---` / `--- END BRIEF ---` fences).

**Final line, verbatim:**

```
- No edits outside this lane's declared footprint.
```

Not truncated. **Honest defect in my own execution, reported rather than smoothed:** the receipt was ordered *first*, and I emitted tool calls before any text. It is stated here instead. That also settles the receipt-gate echo field, which must be what actually happened rather than what was supposed to:

```
git-source-resolves-non-empty:  https://github.com/rdwornik/dev-knowledge
                                (origin fetch+push; HEAD == origin/main @ 66662c7)
first-assistant-text-echoed:    "No hooks installed in this clone; `HEAD` is `origin/main` at
                                `66662c7`. Branching fresh and authoring the ADR."
```

---

# THE DESIGN — the fuzzy-band acceptance shape

Landed as `docs/decisions/ADR-116-fuzzy-band-acceptance-shape.md` (259 lines, Status **Proposed**), committed as `d8f2993` on `claude/lane-f-000-adr81-fuzzy-band`, pushed. Not merged.

## 0. Ownership check (done-contract item 1)

`grep -rn "fuzzy" tasks/ docs/decisions/` returns exactly two hits: `ADR-81:45` (the deferral itself) and `ADR-85:12` (an unrelated *"no longer a fuzzy semantic question"*). **No other surface owns this band.** The deferral has been open since 2026-06-24.

## 1. The unit of acceptance

**The smallest artifact that has its own addressee.** Not the directory, not the bundle, not the arc. This rule did not exist when I started — exercise finding E1 produced it.

## 2. The partition — the whole idea

Every fuzzy artifact splits into a **rind** (every leg that *does* reduce to an exact check, given the tooling actually reachable at authoring time) and a **core** (what is left, where closure is judgment).

The split is a **per-instance declaration carrying its environment**, never a property of the artifact's class. And:

> "Fuzzy" describes the core. It is **not a property an artifact may claim.** It is what remains after the rind has been made as large as reachable tooling allows. An artifact calling itself fuzzy while leaving a mechanizable leg unmechanized has not entered this band — it has laundered a defect into one.

That clause is the entry gate, and it is what stops the shape becoming an escape hatch from ADR-81.

## 3. The four legs — F1 to F4, authored ex-ante and frozen

Same immutability property as ADR-81's 2026-06-24 amendment, restated for this band:

```
The executor may TIGHTEN  — add a leg, sharpen a criterion, or PROMOTE a core leg
                            into the rind by mechanizing it.
The executor may not SOFTEN — delete a leg, narrow the addressee, or DEMOTE a rind
                            leg into the core.
Promotion is always allowed and always improves the contract.
Demotion is a weakening and requires the architect.
```

- **F1 — Addressee and next act.** Name the reader; name the decision the artifact must make possible. Fuzzy closure is relative to a consumer: *"good prose"* is unfalsifiable, *"the next seat boots without asking a question this bundle could have answered"* is not. This is the corpus's own **zero-questions test** (`docs/intake/2026-08-26-tech-handoff-operator-interface.md`, §"Acceptance criteria (ex-ante)" item 5).

- **F2 — The rind, enumerated and exhaustive.** Gate every mechanizable leg binary. A leg that *was* mechanizable and was not mechanized is a **defect**, not a fuzzy leg. A rind leg that is real but **unreachable** is recorded in the corpus's existing `MEASUREMENT-OWED` form — *owed, never estimated*. An owed measurement is an honest incomplete rind; a silently skipped one is a false one.

- **F3 — The core, with a graded verdict and a named judging role.** Three values, per leg:

```
MET                     the criterion is satisfied
MET-WITH-NAMED-LIMIT    satisfied within a boundary the artifact states itself
NOT-MET                 not satisfied
```

  No core leg without an ex-ante criterion; no criterion without a **role** that judges it (a role, never an identity — E2). A criterion stated **negatively**, as a failure mode, must be paired with its inverse or explicitly marked one-sided (E3).

- **F4 — The self-falsifier.** The artifact ships (1) its declared limits, (2) at least one **measured** place where its own earlier pass was wrong or its method does not reach, (3) what a reader must do to **overturn** it. Zero declared limits is `NOT-MET` by construction. This is the fuzzy analogue of ADR-81's xfail-strict exemplar: there, a frozen decorator makes a premature green *fail*; here, the measured self-error is what a premature green cannot produce.

**Anti-bluff, carried over unchanged:** a criterion states the question, never the answer — the same reason `verify_handoff_probes.py` FAILs a probe row printing an `expected:` value.

## 4. The refusal rule — where this is actually non-binary

Closure is declared on the **worst verdict in the core** and the **completeness of the rind**, in public:

```
ACCEPTED                    rind complete, every core leg MET
ACCEPTED-WITH-NAMED-LIMITS  the limits are named IN the artifact, addressee accepts them
RETURNED                    a leg is unnamed, or the addressee declines the residue
```

**A `NOT-MET` core leg does not automatically block.** It blocks *unless the record names it and the addressee accepts it anyway*. What this shape forbids is **silence, not imperfection**. Closure never reduces to a number; two `ACCEPTED-WITH-NAMED-LIMITS` artifacts are deliberately not rankable.

## 5. What it does NOT cover (done-contract item 3)

- **The deterministic band is untouched.** ADR-81 legs (a)–(e) and its frozen executable contract bind exactly as before. Where "done" reduces to an exact executable assertion, **ADR-81 binds and this ADR is not available.** F2 is the boundary, and it exists to keep as much work as possible on ADR-81's side of it.
- Not an opt-out; no code artifact is in this band.
- Not ADR-111 (routes a *finding*) and not ADR-112 (routes a *candidate*) — this routes an *artifact*.
- Not a session-close gate (ADR-85 / `DEFINITION_OF_DONE.md` own that).
- No ranking, no score, no aggregate.
- **No organ is claimed.** Per ADR-81 leg (d), an explicit deferral rather than a silent gap: a *shape* gate (does the record carry F1–F4 and a disposition, in the manner of `lane-contract-check`) is named as a candidate and is **not built**. A gate over the *content* of a core leg is not merely unbuilt but **refused** — it would be exactly the leg-that-cannot-fail-honestly the shape adopts R3 to avoid.

## 6. The exercise — two real in-corpus artifacts (done-contract item 2)

Both were read before the shape was written. Neither was chosen for being flattering.

**Artifact 1 — `docs/handoffs/2026-08-28-dev-knowledge-architect/`** (handoff bundle; prose + judgment)

```
F1  MET-WITH-NAMED-LIMIT   addressee + next act explicit; the §13(d) narrowing to "anything
                           changed?" IS the zero-questions test — but stated as a fact about
                           the bundle, never frozen as a criterion before generation.
F2  MET                    strongest rind in the corpus: PROBES P0a/P0b/P0c + P3, plus
                           verify_handoff_probes, check_handoff_probes,
                           validate_residual_completeness, check_seal_identity. Goes further
                           than F2 asks and states which legs deliberately carry NO probe.
F3  NOT-MET                core legs are NAMED — Purpose, write-scope prose, mode-basis prose,
                           RESIDUAL §4 — then left with no criterion, no judging role, and no
                           verdict recorded anywhere.
F4  MET-WITH-NAMED-LIMIT   limits declared and reasoned (R3; terra H3; the cp1252 caveat).
                           No measured self-error, no overturn instruction.

DISPOSITION: ACCEPTED-WITH-NAMED-LIMITS  ·  residue: F3 has no rubric and no verdict
```

The finding worth carrying: the handoff machinery mechanized its rind superbly, correctly identified which legs *could not* be mechanized, wrote down why — and then let the core fall on the floor. Its own law explains how and does not cover it: *"a leg with no mechanical counterpart cannot fail honestly, and one that cannot fail honestly discredits the whole block"* (R3). That law is right, and it argues only for keeping the judgment leg **out of the probe block**. It never says the leg needs no criterion. Read as a stopping point, that is how it was used.

**Artifact 2 — `docs/audits/2026-08-29-census-nb2-funnel.md`** (funnel census; judgment artifact)

```
F1  MET                    addressee named repeatedly ("each is named because FM-3 inherits
                           them"); next act = the archival worklist. Best F1 in the corpus.
F2  MET-WITH-NAMED-LIMIT   counts, citation graph, §9 reproduction commands, zero-write proof
                           all exact; two scripts ran under bare python3. §8 then declares the
                           rind INCOMPLETE and why — container uv 0.8.17 vs ==0.11.19, so five
                           gate verdicts are MEASUREMENT-OWED-LOCAL, "owed, never estimated".
F3  MET                    criteria were ex-ante and in the brief: class precedence §1.5,
                           terminal-state test §1.4, governance pool COPIED not re-decided
                           §1.3, plus a stated failure mode. Verdicts recorded in §7.
F4  MET                    the reference implementation: 42% false-orphan rate in its own
                           first pass (19->11), 25% error on its highest-consequence list
                           (intake #42, refuted by opening ADR-115), 61->24 on the backward
                           pass, four named method limits, and the honest inversion —
                           PROTECTED at 94.1% is the OTHER way to look complete, so the
                           consumption sub-axis is published underneath it, where unconsumed
                           IS the plurality at 70.6%.

DISPOSITION: ACCEPTED-WITH-NAMED-LIMITS  ·  residue: five owed measurements, each named
```

## 7. Where the shape BIT — negative results, first-class

It did not survive contact unchanged. Three findings are folded into the design above; the fourth is not repairable and is named instead.

- **E1 — the shape had no unit rule and needed one.** Judging the handoff *bundle* as one artifact averaged `PROBES.md` (near-total rind) against `RESIDUAL.md` §4 (near-total core) into a comfortable middling verdict that **concealed an empty F3 entirely**. The unit rule exists because of this, not before it.
- **E2 — "named judge" was wrong as drafted.** The judge of a handoff bundle is a seat that does not exist when the bundle is frozen. F3 names a **role**.
- **E3 — a one-sided anti-criterion is bluffable by inversion.** The census's brief gated on *"a census routing most objects to ORPHAN without evidence has not censused"*. The census passed cleanly at 1.2 % ORPHAN — and then had to **invent the inverse check itself**, because PROTECTED at 94.1 % is an equally vacuous way to look complete and the brief closed only one direction.
- **E4 — F4 is monotone in effort, not in quality, and this is not fixable here.** A thorough artifact reports more self-error, a sloppy one reports none, and trivial self-corrections can be manufactured. There is no mechanical defense, and inventing one would violate the honest-narrowing law the shape adopts. Partial mitigation: F4's third clause — *what a reader must do to overturn this* — is the hardest to fake self-servingly, because it hands the reader a live weapon. **Recorded as a known hole, not solved.**

A fifth observation, not a defect: the rind/core boundary **moved during artifact 2's own life** — two scripts ran under bare `python3` and promoted their numbers from judgment to measurement while five gate verdicts stayed unreachable. That is why the partition is a per-instance declaration and not a class fact.

---

# END PACKET

**Footprint:** one file added, `docs/decisions/ADR-116-fuzzy-band-acceptance-shape.md`. Nothing else touched; `git status` clean. `docs/intake/**` was in write-scope and **not used** — the ADR is born from ADR-81 §45's named deferral, not from an intake, so per the template's rule the `Intake:` field is omitted rather than a row being birthed to justify it (filing-backpressure instinct; no `kill-candidates:` line was owed because no backlog id was added).

**Gates: NONE RUN, and none are asserted.** Per contract item 4 this lane is read-only of the gate surface. Declaring what I *did* invoke: only `git`, `grep`, `sed`, `wc`, `ls` and `which`/`--version` probes. `python3` (3.11.15) is present but **I ran no Python at all**. The container's `uv` is **0.8.17** against `pyproject.toml` `required-version = "==0.11.19"`, so no `uv run --locked` gate could have started — independently confirming artifact 2's §8 finding on a clone one day newer. No pre-commit hooks are installed in this clone (`.git/hooks/` holds only samples), so **no hook was bypassed and none fired**; no `--no-verify` was used.

**Two locators corrected rather than inherited** (the "resolve a locator before you act on it" rule biting my own draft):
1. The zero-questions citation is `§"Acceptance criteria (ex-ante)" item 5`, not `§5`.
2. Artifact 2 attributes its non-collapse principle to "ADR-100 §4". I opened it: §4 is **"Genre demarcation — audit vs intake"**, ruling that the two are separate genres *"governed oppositely on purpose"*. It says nothing about retention-versus-consumption axes. The census's use is a defensible **extension**, not the text, and the ADR now cites it as an extension so the next reader does not inherit it as a ruling.

**Reported, not escalated** (V-2 budget — none of the three escalation classes was hit): the contract's write-scope line says this lane *"consumes lane-e's census."* No lane-e census for this batch exists in the tree — `docs/audits/2026-08-29-census-nb2-*.md` belong to night-batch-2 wave 1 (FM-C, codex-surface, readme-vision), and `NB2-LANE-E-605-consumer-root.md` is a different batch's lane E on an unrelated subject. **Not a refuted premise requiring a PAUSE:** none of the four done-contract items depends on that census, and the sentence governs *merge ordering*, which is the integrator's act. Flagged so the integrator does not wait on an input that may not exist.

**Not done, by contract:** no merge, no push to `main`, no JOURNAL entry, no index regeneration, no other branch touched. `docs/decisions/README.md` carries editorial one-liners for ADRs and `.claude/generated/recent-adrs.md` is generated — **both are stale with respect to ADR-116 and are the integrator's regeneration act (Q1)**, not mine.