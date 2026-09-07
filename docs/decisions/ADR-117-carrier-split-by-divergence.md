# ADR-117: Carrier split by divergence — push for pinnable/waivable, pull for fleet-uniform

- **Status:** Proposed
- **Date:** 2026-09-06
- **Decision tier:** Architecture (Path A — filings-drafted under `DECLARE-F-2026-09-06` F-1, awaiting the browser's `rule`)
- **Amends:** none. This ADR **states** a split the hub already implements; it changes no carrier and retires no mechanism.
- **Related:** ADR-91 (release tagging is the operator's act); ADR-92 Decision 3 (write-yes / commit-no / autonomy-no); ADR-93 §4 (all writes stage only); ADR-102 / `[#336]` (the ratified corp-monorepo pin this ADR exists to be able to express); ADR-28 / ADR-36 (core invariant #4 — Layer 2 never executes); intake #73 (shape spec); `[#616]` (flip-condition instrument — this ADR is its first live instance).
- **Decommission:** none
- **Source:** `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md` §0.1–0.5, ruled at `to-cc/DECLARE-F-2026-09-06.md` ("Read, and accepted as measured"). Drafted by filings-N2, NIGHT-2 lane W2-F1. **The Flip-condition below is instrumented from the operator's MSc thesis `Praca_Dyplomowa_Magisterska` (Robert Dwornik, Warsaw University of Technology; operator disk, uncommitted), principle 5 — sensitivity analysis: a decision that cannot name its own flip has not been sensitivity-tested.** The instrument is catalogued at that audit's row **T-07** (`tex/6-tworzenie-architektury.tex:1206,:1243` — nine closed questions, then the same nine re-answered and the recommendation flips) and tracked by open row `[#616]`, which carries the same provenance sentence (`tasks/616-flip-condition-every-adr-records-what-evidence-w.md:12`).

<!-- Decommission: none -->

> **AMENDMENT 2026-09-07 (lane `worktree-lane-u-000-declare-f2-intakes`, operator-issued
> `to-cc/DECLARE-F-2-2026-09-07.md` §A).** W2-F1's session died after this ADR landed at
> `ec0d7912`, leaving two of its items unseated. Both are discharged here, and nothing in the
> Context, Decision, Flip-condition or Alternatives is touched by either:
> 1. **The provenance line now cites the thesis.** §A: *"the ADR's provenance line cites the thesis
>    (T-01: no ADR cites it yet) — `Praca_Dyplomowa_Magisterska` principle 5 as the source of the
>    Flip-condition."* **T-01's premise was re-verified before filing, not inherited:**
>    `grep -ril "Praca_Dyplomowa\|Magistersk\|dyplomowa" docs/decisions/` returned **no file** on
>    2026-09-07, so this is the first ADR to cite it and the citation is not redundant.
> 2. **The status-line inline comment was moved into the "Status wording" note below.**
>    `gen_claude_rosters.py` scrapes the status line **verbatim** into
>    `.claude/generated/recent-adrs.md`, which is `@`-imported by `CLAUDE.md` — so the comment was
>    reaching a boot-time file whole. The integrator measured it as a quality defect, not a gate
>    break (`test_claude_md_byte_cap.py` 6 passed; `gen_claude_rosters.py --check` exit 0). The
>    rationale is unchanged and is kept below; only its location moved. **General form, worth
>    carrying: the generator scrapes the status line verbatim, so any inline comment there reaches
>    a boot-time file.** The status VALUE is unchanged — still `Proposed`, still not `Accepted`.

> **Status wording — a deviation, recorded not hidden.** *(This paragraph is the home of the note
> that sat as an inline comment on the status line until 2026-09-07 — verbatim, it read:*
> **DECLARE-F F-1 calls this state "DRAFT"; `Proposed` is the enum's spelling of it. NOT ratified.
> See "Status wording" below.** *See amendment item 2 above for why it moved.)*
>
> `DECLARE-F` F-1 and the lane contract both
> say this ADR "stays **DRAFT**". **`DRAFT` is not a member of this repo's ADR status enum**
> (`Explored, not adopted` · `Partially superseded` · `Superseded` · `Deprecated` · `Proposed` ·
> `Accepted` · `PARKED` — `docs/decisions/README.md` §"Status enum", enforced by
> `check_adr_status_grammar` at **TIER_COMMIT**). Measured by lane W2-F1: the literal string `DRAFT`
> is a **blocking** defect — `audit.py health` returns `DEGRADED` and the pre-commit `audit-health`
> hook refuses the commit, so the ADR could not land at all. `Proposed` is the enum member meaning
> *recorded but not ratified*, which is what DECLARE-F means by DRAFT, and it is the status ADR-116
> carries in the same state. **The pin's actual prohibition is untouched: this is NOT `Accepted`, and
> no seat but the browser may make it so.** The lane changed the enum value only; it did not touch
> the ADR machinery (`validate_adr_status.py`, the template) — that is lane W2-F4's footprint.
> Filed as `QUESTION-lane-u-000-adr-carrier-split.md`; **if the browser wants the literal word
> `DRAFT`, the enum must gain the member first, and that is a curated-baseline act, not a lane's.**

> **Not in force.** `DECLARE-F` accepted the model as measured and commissioned this ADR;
> the ADR itself is ratified by the browser at a later sitting. **The adversarial codex pass on §0 that
> `DECLARE-F` owed has been RUN** (lane W2-F1, 2026-09-07 — **HIGH 13 · MED 2 · LOW 0**, recorded
> below). `DECLARE-F` said a HIGH was *expected, not a surprise*; thirteen arrived, two independent
> reads converge on the same four attacks, and **none of them is answered here** — the ruling seat
> reads them and rules. **A2 (the load-bearing capability asymmetry) is the claim to rule first.**

## Context

The fleet's real operating mode is **per-consumer, per-component divergence that is ruled rather
than accidental.** Three deployed consumers carry three different corpus versions, and at least one
of those is a decision: `ecosystem/deployed-versions.yaml` records that corp-monorepo *"Stays 1.2.0
BY DESIGN … #336/ADR-102 (Accepted 2026-07-17) ruled NOT to bump … Do not 'fix' to 1.3.1."*

Read `docs/audits/2026-09-05-technical-fleet-readiness.md` §0 alone and corp-monorepo is "2 releases
behind". Read the durable record and two of those releases are a **ruling**. Both statements are
true; the thing that reconciles them is the **waiver** — which is why fleet-readiness §0 counts
waivers (2 · 1 · 1) as a first-class column rather than a remark.

Two deployment models were compared:

- **Pull (Maister's shape).** A plugin resolved from a marketplace at install time. Measured
  behaviour: the plugin registry is **machine-wide**, so any known marketplace contributes a
  disabled row to every project, and both scope routes (`project`, then `local`) were tried and the
  row survived both. Install state is a property of the *machine*, refined by a per-project enable flag.
- **Push (our carrier).** `deploy/tool.py` plus registered carrier modules write files **into** the
  consumer tree, versioned by `deploy/manifest-v*.yaml`, recorded in `ecosystem/deployed-versions.yaml`,
  with the floor guarded by a hash sidecar.

**The decisive asymmetry is a capability, not a preference.** A pull registry can express
*installed / not installed / enabled here*. It has **nowhere to put a ratified version pin**, because
the version resolves at install time and the registry is machine-scoped — there is no place for
ADR-102's *"do not fix to 1.3.1"* to live. A push carrier has one, and already uses it.

And the hub **already runs both**, since v1.0.0: `deploy/manifest-v1.5.0.yaml` declares carrier #2
`tier1-plugin`, `implemented: true`, reconciling via the external `claude plugin` CLI with
correctness judged from the resulting installed state, never from stdout. Pull is already
carrier-shaped here. What was missing was not a mechanism but a **stated discriminator**, which left
the split looking like an accident of which carrier happened to be written first.

## Decision

> **PUSH for anything a consumer may pin or waive; PULL for anything fleet-uniform by construction —
> and both legs stay COMPONENTS in the deploy manifest, each with a declared version and a drift
> check on both sides.**

**The discriminator, stated as one question:** *does this component have a legitimate per-consumer
divergence?*

- **Yes → push-carried.** Only push has somewhere to record the ruling that authorised the divergence.
- **No → pull-preferred**, because pull is cheaper. Push costs one operator act per consumer per
  release, and the fleet shows what that costs: **five of nine consumers carry no floor at all, and
  three of those have never been measured.**

This is 024's packaging rule with the discriminator named. It is **not a new architecture** — it
promotes an existing split from accident to rule.

## Consequences

1. **A second drift surface, and it is the one genuinely new obligation.** A hybrid has two places
   to be wrong. Plugin-carried state needs the same both-sides drift check `deployed_methodology_version`
   already gets. Carrier #2 half-satisfies this today by judging from installed state rather than
   stdout; **what it lacks is a durable per-consumer record of the plugin version.** → lane W2-F3.
2. **One measured obstacle stands between this model and its first consumer.** `deploy/tool.py`
   resolves the consumer as `hub_root.parent / repo` **with no override**. The win-tooling v1.4.0
   record states the consequence in the file itself: the record was *"written by the lane rather than
   by `deploy/tool.py --execute`"* because the deploy binds to a consumer WORKTREE the tool cannot
   name. → lane W2-F2 adds `--consumer <path>`; default unchanged.
3. **First consumer: corp-monorepo** — the widest measured gap, the operator's own stated priority
   order, and **the case that exercises the waiver leg rather than avoiding it.** A model whose whole
   claim is *"push is required because only push can carry a pin"* should be proven first on the one
   consumer that actually has a ratified pin. Deploying to a clean consumer would demonstrate nothing
   this ADR asserts.
4. **The hub/consumer autonomy question is NOT re-opened by this ADR.** It is closed by citation:
   each consumer runs its own CC sessions independently; the hub deploys and does not drive. That is
   core invariant #4 plus ADR-92 Decision 3 (write-yes / commit-no / autonomy-no) and ADR-93 §4. A
   memo that re-derived it would be manufacturing a fork the repo already closed. The only genuinely
   open sub-question is narrow and is a *limitation*, not a doctrine — consequence 2 above.

## Flip-condition

> **If `claude plugin` gains per-project version pinning AND a way to express a waiver, the push leg
> loses its justification for waivable components, and the model collapses to pull.**

That is the single input change that reverses this recommendation. It is recorded so the decision is
revisited **on evidence rather than on fatigue** — the instrument thesis row T-07 supplies and open
row `[#616]` tracks. This ADR is `[#616]`'s **first live instance**, and lane W2-F4 proposes making
`Flip-condition` a REQUIRED section of the ADR template on that basis.

**Both conditions are required.** Per-project pinning alone does not suffice: a pin without a waiver
expression can record *which version* but not *that the divergence was ruled*, which is the half
ADR-102 actually needs.

## Alternatives considered

- **All-push (retire carrier #2).** Rejected: pays one operator act per consumer per release for
  components with no legitimate divergence, and the fleet's five floorless consumers are the measured
  price of that cost already being too high.
- **All-pull (retire the carrier corpus).** Rejected on a capability, not a preference: the registry
  is machine-scoped with install-time resolution, so ADR-102's pin has nowhere to live. Adopting it
  would silently discard a ratified decision.
- **Keep the split unstated** (status quo ante). Rejected: it was already a hybrid, but as an
  accident of authoring order. An unstated split cannot be checked, cannot be argued against, and
  gives a new component no rule for choosing its leg.

## Adversarial review — codex, one round, 2026-09-06

**TALLY: HIGH 4 · MED 1 · LOW 0.** Reviewer `codex-cli 0.145.0`, briefed adversarially (attack the
design) per C-7, one round, on this draft. `DECLARE-F` predicted this: *"a HIGH from a later
adversarial read is expected, not a surprise."* Four arrived.

**The DECISION is not edited; the dispositions do propose answers.** *(Precision added by lane W2-F1
after a third codex round flagged the original wording — "recorded, not answered" — as overstating
this seat's restraint. It does: A1's disposition supplies a decision procedure and A2's supplies a
narrowed claim. Those are **proposals for the ruling seat, not adopted text** — the Decision,
Flip-condition and Alternatives are byte-unchanged — but calling them mere records was inaccurate,
and the inaccuracy is corrected rather than left to be discovered.)* This ADR is unratified and the
browser rules it; a filings seat that
edited the design to dodge an attack would be ruling it. Each finding gets a disposition line
marking only whether the ADR *can* answer it — that is a reading aid for the ruling seat, not a verdict.

| # | Sev | Finding (codex's words, compressed) | Disposition for the ruling seat |
|---|---|---|---|
| A1 | HIGH | The "legitimate per-consumer divergence" discriminator **begs the question** — "legitimate" has no decision procedure, owner, or criteria. A security-policy plugin could be classified either way by two competent engineers. | **Answerable, and the answer is already in the tree.** A divergence is legitimate iff a ratified ruling records it — ADR-102 is exactly that object. Stating it makes the discriminator decidable: *is there an ADR or ruling authorising this divergence?* The draft states the question but never names the procedure. **A real gap in the text, not in the model.** |
| A2 | HIGH | *"A pull registry has nowhere to put a ratified version pin"* **falsely generalises one measured CLI** into a property of pull registries. A pin can live in a lockfile, per-repo config, a wrapper, or `ecosystem/deployed-versions.yaml` itself. | **The strongest finding, and it lands.** The load-bearing claim overreaches. The defensible narrower claim is about *enforcement*, not storage: the pin can be recorded anywhere, but nothing makes the installing mechanism honour it. Once storage is separated from mechanism, mandatory push loses this justification. **Genuinely weakens the Decision; the browser should rule on the narrowed form.** |
| A3 | HIGH | Requiring **both** native pinning **and** native waiver expression makes the flip-condition **artificially unreachable**, since a waiver is governance metadata that can stay in the ADR or ledger. | **Compounds A2 and shares its root.** The draft argues the conjunction is necessary; codex argues it is self-protective. Both readings are available from the text, which is itself the problem. |
| A4 | HIGH | *"We already do both, we are just naming it"* **smuggles in expanded scope** — the ADR mandates carrier selection for all future components, durable plugin-version records, two-sided drift checks, a new consumer-path capability, and a waiver-bearing first deployment, none of which exist today. | **Lands on the rhetoric, and the evidence is the batch itself.** The ADR commissions four lanes (W2-F2/F3/F4 and the first deployment). Calling that "not a new architecture" understates it. The model may still be right; the framing is not. |
| A5 | MED | The second drift surface is **not the only new obligation** — the hybrid also needs authoritative-source rules, reconciliation ordering, conflict handling, rollback semantics, waiver lifecycle, and migration when a classification changes. | Fair. Consequence 1's *"the one genuinely new obligation"* is too strong. |

**What this seat did NOT do.** It did not soften the Decision, retract the asymmetry claim, or
re-word the flip-condition to survive A3. Those are the browser's to rule. **A2 in particular should
be ruled before this ADR leaves DRAFT** — it is the claim the Decision rests on.

**Honest limit on the review itself:** one round, one reviewer, no fan-out, and the reviewer read
this ADR rather than §0 of the source memo. `DECLARE-F` asked for codex on §0; §0's argument is
restated here in full, so the attack surface overlaps, but it is not literally the same read.

## Adversarial review — codex on §0 of the source memo, one round, 2026-09-07

**This is the pass `DECLARE-F` owed and the section above did not discharge.** The review above read
*this ADR*; `DECLARE-F` asked for codex on **§0 of the source memo**
(`docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md`, lines
40–193). Lane W2-F1 ran it directly against that line range, `codex-cli 0.145.0`, briefed
adversarially per C-7, one round.

**TALLY: HIGH 13 · MED 2 · LOW 0.** `DECLARE-F` predicted *"a HIGH from a later adversarial read is
expected, not a surprise."* Thirteen arrived. **They are recorded, not answered** — this ADR is DRAFT
and the browser rules it; a lane that edited the design to survive an attack would be ruling it.

**The finding that matters most is the convergence.** Two independent adversarial reads — one on the
ADR, one on §0 — land on the *same four* attacks, which is far stronger evidence than either alone:

| §0 finding | Converges with | The shared claim under attack |
|---|---|---|
| Lines 82–98 universalize one measured `claude plugin` CLI into "a pull registry" as a category; lines 96–98 call "no place for a pin" a non sequitur, since a pin can live in a lockfile or hub registry | **A2** | The load-bearing capability asymmetry |
| Lines 111–118: "legitimate per-consumer divergence" has no decision procedure — circular, and cannot constrain placement | **A1** | The discriminator itself |
| Lines 129–133: requiring **both** native pinning and native waiver makes the flip-condition effectively unreachable and protects push from disconfirmation | **A3** | The ADR's own kill switch |
| Lines 115–127: a new allocation policy smuggled in as "not a new architecture" | **A4** | The framing of scope |

**New in this pass, not raised against the ADR** (recorded for the ruling seat):

- **HIGH — lines 98–100 misattribute waiver expressiveness to the *transport*.** The pin and its
  ruling live in hub-owned `ecosystem/deployed-versions.yaml`, not inherently in the pushed consumer
  files; the same record could govern a *pull* reconciler. This is A2's root cause stated more
  sharply: the argument conflates a **control-plane record** with a **delivery mechanism**.
- **HIGH — lines 119–121 assert pull is cheaper without measuring either model.** The five floorless
  consumers include unaudited and pre-deploy repos, so they do not establish push cost as the cause.
- **HIGH — lines 123–127 under-count hybrid risk.** Cross-leg atomicity, version compatibility,
  partial rollout, rollback ordering and split ownership are unexamined (this is A5, raised at MED
  against the ADR, re-raised at HIGH against §0).
- **HIGH — lines 69–78 generalize one documented pin into the fleet's "real operating mode."** Only
  corp-monorepo is evidenced as *intentionally* pinned; lag, defects and absent deployments are not
  ratified divergence.
- **HIGH — lines 159–160's "one measured obstacle" is a completeness claim** one observation cannot
  support; "one *observed* obstacle" is the defensible form.
- **HIGH — lines 181–190 subordinate the memo to ruling 024, which is not in the tree.** A governing
  authority that cannot be read makes the recommendation non-reproducible.
- **MED — lines 102–107** infer "both legs since v1.0.0" from a *v1.5.0* manifest's own assertion.
- **MED — lines 175–179** name corp-monorepo as the pilot without a falsifiable test, so a deploy
  that overwrites or bypasses the pin could still be narrated as success.

**What this lane did NOT do.** It did not soften the Decision, narrow the asymmetry claim, or re-word
the flip-condition to survive the attack. Those are the browser's to rule. Consistent with the review
above, **A2 / the transport-vs-control-plane conflation is the claim to rule first** — it is now
carried by two independent reads.

**Honest limit on this pass:** one round, one reviewer, no fan-out; codex read §0 in the tree but not
the upstream sources §0 itself cites.

### Third round — codex on the landing diff itself, 2026-09-07

Lane W2-F1 also ran the routing-table reviewer on its own landing diff (C-7 / D-1, "review is a lane
act"). **TALLY: HIGH 4 · MED 0 · LOW 0.** Three restate attacks already recorded above and are left
to the browser. **One is new, checkable, and lands on this ADR's central citation:**

- **HIGH — ADR-102 may not ratify what this ADR says it ratifies.** The ADR leans on ADR-102 as a
  *"ratified version pin"*. The reviewer's objection: ADR-102 ruled on an **enforcement-gate carrier
  repoint (2 hooks)**, not a corpus deploy, and it predates v1.4.0 — so "ratified pin" overstates it.
  **The lane verified the quotation and it is exact** (`ecosystem/deployed-versions.yaml:54-58`:
  *"Stays 1.2.0 BY DESIGN … #336/ADR-102 (Accepted 2026-07-17) ruled NOT to bump … Do not 'fix' to
  1.3.1."*). **But the very same comment says the pin is *"an enforcement-gate carrier repoint … not
  a corpus deploy"*, which is the reviewer's point, visible inside the ADR's own evidence.** So the
  quote is faithful and the *inference from it* is what is contested. **This compounds A2:** if the
  one live instance of "a ruling only push can carry" is really a gate repoint, the Decision's
  strongest concrete support is weaker than stated. **Ruling seat: read this together with A2.**
- The other three (the pull-registry capability gap contradicted by the dispositions at lines 145 and
  182–185; *"not a new architecture"* against the five obligations the ADR commissions; and the
  "recorded, not answered" wording) are **A2, A4, and a wording defect the lane corrected in place**
  — see the note under the first review's table.

**Nothing in the Decision, Flip-condition or Alternatives was changed in response to any of the three
rounds.** The only prose the lane edited for accuracy is the sentence describing what the lane itself
did — never the design under review.

## Honest limits

- **The adversarial pass is now DISCHARGED, and it was expensive.** §0 was drafted without one (codex
  absent on the cloud substrate) and without fan-out. Lane W2-F1 ran it on 2026-09-07: **HIGH 13 ·
  MED 2 · LOW 0**, recorded in full in the section above. The precondition of leaving DRAFT is met in
  the sense that the pass was *run and recorded*; **the findings themselves are not discharged**, and
  A2 in particular is unruled.
- **Nothing here is deployed.** ADR-92's commit-no is unchanged: the deploy act stages, the operator
  commits, and the v1.5.0 tag is the operator's (ADR-91).
- **The 6.4× / 16.2× headline from the AJ second pass is not load-bearing anywhere in this ADR.**
  Every claim above rests on an in-tree locator. See the erratum
  `docs/audits/2026-09-06-technical-erratum-aj-second-pass.md`.
