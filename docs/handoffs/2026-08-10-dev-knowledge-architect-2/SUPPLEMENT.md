# Architect strategic supplement — 2026-08-10-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-10

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

> **THIS BUNDLE IS A SAME-DAY RE-CUT (`--allow-suffix`), and this section carries TWO
> verbatim folds.** The bundle `docs/handoffs/2026-08-10-dev-knowledge-architect/` is
> immutable and is left BYTE-UNCHANGED; it is superseded by this sibling under the
> active-bundle rule (`docs/handoffs/README.md`: a day with more than one handoff produces
> `<slug>`, `<slug>-2`, ... siblings, *that is normal*, and verification resolves to the
> newest by git-add date; `--exact` reports the older one's supersession). Nothing was
> edited to achieve this, and no mechanism was invented.
>
> **FOLD 1 (below, unchanged from the ARC-4 cut):** the outgoing Layer-1 seat's authored
> supplement, Part 1 (A1-A7). Reproduced byte-for-byte from the superseded bundle.
>
> **FOLD 2 (at the end):** the night-batch delta the same seat authored after the three
> cloud lanes delivered, `SUPPLEMENT-UPDATE-night-batch-delta.md`. It SUPERSEDES parts of
> A1-A5 and A7 above; the superseded text is retained rather than rewritten, because the
> update is an overlay authored against it and reads as one.


> **Folded VERBATIM by CC (ARC-4 cut) from the outgoing Layer-1 seat's authored supplement,
> `$env:CLAUDE_PROMPTS_DIR` + `HANDOFF-SUPPLEMENT-and-session-archive.md` (the variable resolved
> live to `C:/Users/1028120/Downloads`; file present, 18,940 bytes), Part 1. Zero rewriting, zero
> summarising, zero reordering. A1-A7 answer supplement questions 1-7 in order. Parts 2-4 of the
> same source (plan-vs-outcome, measurements/register, exit sequence) are carried in `RESIDUAL.md`
> §4.**

# PART 1 — THE SUPPLEMENT (A1–A7)

## A1 — Intent: what this window was for, and what it became

**Planned:** dispatch and close batch 3 under `[E7]`, taking the decisions the previous window carried.

**What it became [judgement]:** the window where the fleet's parallel machinery was proven at width 10 — and where it became clear that the machinery is not the constraint. Ten lanes landed with zero bypasses; eight rows closed; the first sustained fall in the open curve (net −8, open-total 161). Then a five-lane cloud night and six research commissions produced roughly twenty audit artefacts that have so far yielded **zero rows**. That single figure is the inheritance: **the fleet's bottleneck moved from execution to consumption.**

**Secondary intent, achieved:** second-seat verification became a standing batch citizen and earned it — it caught a manifest filename the parser could not see, a lane's own undeclared output path, and two mutually-wrong `doc-counts` figures where picking either side would have committed a number nobody counted.

## A2 — Standing diagnosis and the tensions I did not resolve

**The diagnosis, arrived at independently by two seats [judgement, evidence-backed]: "ruled-but-unverified" is the dominant defect family.** The repo rules excellently and has no organ that notices a ruling landed only halfway. Six instances from lanes that never spoke to each other: `markdown_it` ruled ADOPT and landed at one of three sites (32 and 8 files diverge); `yaml.safe_load` ruled the same day and still unimplemented while its twin migrated; two `LANE_BRANCH_RE` constants disagreeing on 8 of 11 real merged branches; the intake area's two generator-carriers with one hooked; an ADR-archival "zero-refs bar" existing only in a commit body; ADR-100's ruled-but-unbuilt index split. **My own six defects this window are the same family — I knew every rule I broke; nothing checked me.**

**Second diagnosis: the binding constraint is BIRTH RATE, not throughput.** Median row age 19 days, oldest 68, **zero over 90**, 73% born in the last month. Any wave that converts research into rows wholesale makes the number worse however good the rows are.

**Third, and mine alone [judgement]: enforcement is layered by REACH, and the load-bearing parts sit in the shortest-reach layer.** Layer 1 pre-commit needs installation plus a resolvable pinned toolchain — it failed in *every* cloud lane. Layer 2 server-side covers three of seventeen client-side gates. Layer 3 is Claude-Code-specific agent hooks, `block_immutable_edit` among them, with **zero reach elsewhere**. Consequence: in a cloud container or under another provider, immutability of `docs/audits/` is enforced by nothing. This unifies the cloud-ungated problem and the multi-provider portability problem into one root cause.

**Tensions carried, unresolved:** portability versus enforcement (the richest mechanisms are vendor-specific) · **the research set is structurally a threat to the birth-rate finding it made** · cloud speed versus gate integrity · ratchets versus Goodhart (an agent optimising to a length cap splits files) · **measure-first versus the operator's execution tempo** — someone must hold that line or break it deliberately · immutable ADRs versus the felt need to delete (growth is correct and it does not reduce the number he is unhappy about).

## A3 — Rejected, do not relitigate

**From the research window:** *Functional Programming in Scala* as a fleet source of truth · notebook environments for a git/gate agent workflow · server-based graph databases and the archived embedded one · symlinks as the provider-stub mechanism on Windows · parallel memory layers beside the repo (the repo is the memory) · single-GPU model-training tooling · auto-closing stale-bots and backlog bankruptcy as a first resort · big-bang refactor without hotspot measurement · parallelising the probe gate · a standard security-report format for review artefacts (the real gap is producer discipline) · public benchmark scores as the model-selection instrument · routing a consumer subscription through a foreign agent harness.

**From this seat, with the evidence that killed each:** "name it through the generator" as prevention — `PLAYBOOK.md:3476` already held the correct template and the malformed artefact was hand-authored around it anyway (measured negative result) · `contract-lint` as a stamping rule — the contract that motivated it already carried a SHA · a template *section* as a mechanism — prose reminders failed six times in this window · reverting the `prompt-template` spec registration to avoid eight WARNs — that trades a real mechanism for a cosmetic count · importing five research memos into the corpus wholesale · **filing three separate intakes for the three orphan commissions** — that takes pending intakes from four to seven and breaks the ceiling for exactly the reason the plan names.

## A4 — Open questions carried

- **OneDrive rule conflict** — ai-council forbids reads of those paths, corp-ops permits enumerated non-destructive reads, global invariants match corp-ops. **Recommendation to the operator, one word to ratify: the strictest position wins fleet-wide, reads forbidden uniformly, filed as one register line with the two permissive positions superseded.** Grounds: employer data; over-restriction costs a documented workaround, under-restriction costs an exposure you cannot undo. Separately open: secrets living in a cloud-synced profile (win-tooling S-list).
- **Which `LANE_BRANCH_RE` grammar is canonical** — and the sequencing trap: enforce at provisioning first, because tightening the loose regex first makes 9 of 10 historical lane merges non-exempt, i.e. a merge-queue outage.
- **Is the open-count scored on 161 (`status:open`) or 194 (rendered, including 33 deferred)?** Intake #28 never names the filter and batch 3 ruled that naming it is mandatory.
- **`[#430](b)`** — deferred *with direction*: the prior is subject-scoped severity (a sibling's finding never reddens this repo's gate) over pinned snapshots, which collide with ADR-109 §2. To be ruled as ADR input, **not inherited as decided**.
- **`[#511]` fork** — which load is cut, and by how much. See the measurement in Part 3; it is decisive and must travel.
- **`[#491]`/`[#492]`** — the seeded-defect corpus **does not exist**: four defect classes named in prose, no persisted corpus, no seeding harness. It is the admission gate for every future model lane and Grok's calendar peg has already passed. The 2026-07-31 single-diff A/B is precedent for method, not an admission instrument.
- **`[#399]`** — owns the stub file the handoff-engine arc pointed at rather than duplicating; three named forks still open.
- **Cloud runtime** — the toolchain pin ruling (ADR-106 makes it its own gated act) and, separately, **what a cloud lane may change in its own container**: four lanes met the same condition and chose four different answers, so night batches are repeatable only by accident.
- **Measure-first versus tempo** — my recommendation: hold the line where the measurement is cheap and one-off (the footprint predicate, telemetry extraction); break it deliberately where measuring costs more than the mistake would (code-style rule families, the graph build).

## A5 — Settled this window; do not re-derive

- **The finding pipeline.** Audit produces evidence, never decisions → mandatory TRIAGE into exactly one of **(a) OWNED** by an open row, evidence attached, no birth · **(b) DISCHARGED**, with its locator · **(c) CANDIDATE** → intake, an idea that may be rejected · **(d) REJECTED**, with its reason, not relitigated. **REJECTED is a terminal intake status and the existing archive is its home** — no new register. An intake is ratified or rejected **at ADR level**; only an accepted ADR births rows. A finding may not become a row without triage; an intake may not become rows without an ADR.
- **Adjudication runs FIRST in any consolidation.** It is the only step that moves the number without building anything.
- **The pre-anchor technique** (ADR-85 §A7): merge each arc through an integration branch carrying its own JOURNAL entry naming the SHAs the merge introduces. This makes the repo-wide block window zero commits wide. Necessary because **`journal_spine_anchor` scans `main`'s first-parent spine regardless of the committing branch — worktree isolation does not help.**
- **The ADR-110 exemption does not cover cloud lanes at all** (`LANE_BRANCH_RE` wants `worktree-lane-…`; cloud branches are `claude/<slug>`), so a correct committed manifest grants nothing there.
- **Repo commands are the mechanism.** `/lane-boot` provisions, `/lane-integrate` integrates and anchors and tears down. The architect's contract is a thin wrapper; where they disagree, the command wins.
- **`[#502]` direction:** Shape B in the corrected spelling `[".", "scripts", "deploy"]` (measured `23198aae`: zero delta versus baseline, retires 74 of 99 sites, residual 24 non-test + 1 subprocess literal). src-layout excluded without an ADR; root `conftest.py` permitted-not-mandated.
- **Commissions 1–5 decompose one question; cloud (#6) is independent.** Presenting six as one programme would be a story nobody had. Cloud's own verdict: **fix local first.**
- **Cloud precondition, adopted as a rule:** toolchain parity **plus fail-closed attestation — a run that cannot prove its gates executed is untrusted, not green.**
- **Orphan-commission handling, revised and settled:** cloud compute gets **one new intake**; graph and telemetry fold into **#29 as amendments** (same domain); portability folds as a **scope note into the W-wave** (W-9a is its territory). One new intake, two amendments, one note — nothing silently dropped, ceiling intact.

## A6 — Posture for the next seat

**Read the open set before dispatching anything.** Four night lanes independently re-derived `[#453]`, an open row that already recorded their "discovery". That is a consumption failure and it is the cheapest failure to avoid.

**Serial on `main`, always, and anchor as you go.** Parallelism buys nothing if one unanchored merge blocks every commit in the repo.

**Verify before asserting, including your own prior claims.** I carried a lane's stale gate reading into a frozen contract hours later as present fact, and it was false. Restating someone's measurement without a timestamp is a premise error.

**Author from the parser, not from prose intent.** Nine instances in three days: a manifest filename its own glob could not see, a lowercase review heading where `^# Codex Review` is asserted, a `batch:` field carrying a name where `isdigit()` is pinned. Check every name and field against the thing that consumes it before writing.

**Width follows the operator's adjudication capacity, never machine capacity.** By the end of this window the constraint was my review queue, not the lanes.

## A7 — Ratified or ruled, and NOT yet landed

1. **Intake #25 → ACCEPTED.** Ratified by the operator; the file on disk still says DRAFT. **Do this first and alone** — it is a status flip, zero risk, and it unlocks the W-wave and therefore batch 4. Burying it in a seven-item write means it lands last or not at all.
2. The **A7(d) row** — and its *direction*, which must travel with it: a defective-seal bundle retires via an **external dated marker or exclusion, never by editing an immutable bundle**.
3. The **velocity packet law** as landed text (every packet reports opened / closed / net / open-total).
4. **Ch8 seam-name alignment** — older bullets say `operator ↔ batch`; the ratified clause 2 says `operator ↔ integration` and `operator ↔ lane`.
5. The **ADR-archival "zero-refs bar"**, currently applied but existing only in commit `216ce3a8`'s body.
6. **Two LESSONS entries:** the wedged-gate pattern (a RED organ under an always-run hook blocks every commit repo-wide, worktrees included) and the xdist instrument defect (the parallel aggregate undercounts import breakage; per-file isolated collection is the admissible evidence).
7. The **`[#502]` ruling record**, so it stops living in chat.

**Third category — operator-endorsed but UNRATIFIED, do not treat as binding:** the two handoff-engine amendments (the plan travels with the handoff; verification moves to the cut with exceptions-only to the incoming seat plus a read-back obligation).


---

# PART 1b - SUPPLEMENT UPDATE (night-batch delta), folded VERBATIM

> **Folded VERBATIM by CC (ARC-5 archive arc) from the outgoing Layer-1 seat's
> `$env:CLAUDE_PROMPTS_DIR\SUPPLEMENT-UPDATE-night-batch-delta.md` - the variable resolved
> live to `C:\Users\1028120\Downloads`; file present, 6,597 bytes. Zero rewriting, zero
> summarising, zero reordering. Its A7 items 1-3 were acted on by this arc: the `fe81e896`
> anchor is attached, the four ruled dispositions are VERIFIED (4 of 4 landed), and the
> digest gap is established as a BROKEN step with the step named - see
> `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`. The six
> digests were NOT merged; that remains the operator's.**

# SUPPLEMENT UPDATE — night-batch delta, 2026-08-10

**Authored by the outgoing Layer-1 seat.** The bundle at `docs/handoffs/2026-08-10-dev-knowledge-architect/` was cut while three cloud lanes were still in flight; its `RESIDUAL.md §4(g)` records them as owed. They have now delivered (`fe81e896`). This document carries what their results change in the supplement, and **nothing else**. Fold it verbatim by whatever mechanism governance permits — `docs/handoffs/` is immutable and must not be edited.

**Scope note, stated so it is not mistaken:** this is a supplement update, **not a plan**. The incoming architect authors the batch-4 plan; the outgoing seat gives feedback on it. Any plan-shaped document from this window is input to that authoring, never a substitute for it.

---

## Supersedes A1 (intent) — one paragraph added

The bottleneck diagnosis is no longer a judgement; it is measured. **132 of 170 open rows carry prose-only Done-when clauses and cannot be tested mechanically.** That is why close capacity sits at 3: closing is a human reading act, repeated. The window's inheritance is therefore sharper than "twenty audits, zero rows" — the corpus is not merely unconsumed, **it is not machine-checkable**, and no amount of adjudication capacity fixes that.

## Supersedes A2 (diagnosis) — the formulation is now measured

N-B verified 24 claims on the decision surface: **15 verified, 2 refuted, 1 partial, 6 unverifiable — and both errors were inherited claims while every measured claim was correct.** The formulation to carry forward: **we do not err when we measure; we err when we inherit.** The sharpest case was refuted in *three* places before it reached the decision sheet — the closing commit body `9fc1a8b4` (2026-07-21), the row's own `kill-candidates:` line reading *"Do NOT re-propose"*, and the validator's docstring. A second inherited claim: decision-sheet §7 item 12 asserts `ARCHITECTURE.md` was not re-stamped, refuted by `8f09c12d`, whose commit subject says the opposite and predates the sheet by a day.

**Add to the enforcement-reach diagnosis, at machine level:** six nightly conformance digests (2026-08-03 through 08-09) never reached `main` — the digest stream on `main` stops at 2026-08-02, and 08-06 has no branch at all. An organ is running and nobody reads its output. This is the food-chain failure the window kept naming, occurring one layer down.

## Supersedes A3 (rejected) — three additions, each with the evidence that killed it

- **"Origin carries a large and growing branch set"** — my own premise, refuted: `origin` holds **8 heads**, zero deletion candidates, and no branch is an ancestor of `main`. The real defect is that nothing reaps and one branch is an unowned orphan.
- **Kills as a closure strategy** — four candidates adjudicated, **zero closed**, every one failing on its own evidence. Not because capacity was short, but because the proposals rested on unchecked premises.
- **Satisfied-row harvesting as an automatable strategy** — **zero fully-satisfied rows** in ~22 deep-tested of the 53 intersecting recent work, and 132 rows cannot be tested at all. Five are partially satisfied with a named smallest act; the best is `[#390]`, whose resolving ADR-87 amendment landed at `f633e063`, leaving one stale table cell at `templates/prompt-template.md:68` that contradicts `:126` of its own file.

## Supersedes A4 (open questions) — three added, one sharpened

- **The North Star criterion itself is now an open question.** "Under 100 open" needs 71 closes at a demonstrated capacity of 3 — roughly 24 arcs — and it lives in intake #28 §B, which is **still DRAFT and therefore unratified.** Three independent methods have failed to move the number: adjudication gave 3, kills gave 0, satisfied-harvest gave 0. **Recommendation to the operator, not a ruling: re-cut the criterion** toward something measurable and movable — *zero open rows whose Done-when cannot be mechanically tested*, plus *net ≤ 0 sustained across N windows*. The raw count then follows as a consequence rather than being chased.
- **`automation/fleet-audit`** is an orphan with its own root — its "4777 behind" is `main`'s entire history, not staleness — and it is protected by **no written clause**, in a repo whose rule states that silence is not protection. Protect it explicitly or dispose of it; an unowned orphan gets deleted by accident eventually.
- **The six missing conformance digests** — establish whether this is a broken merge step or deliberate, and record which. Until then the organ's output is unread by construction.
- **Sharpened, on `[#511]`:** the cut of 2026-08-10 folded a verbatim supplement and produced a `PASTE_THIS.md` of 68,901 bytes against a 65,000 advisory ceiling, plus 6 flagged promotion-debt lines. Both follow directly from the verbatim mandate and were accepted rather than silenced. That is live evidence for the fork about which load is cut.

## Supersedes A5 (settled) — one proposal, explicitly NOT settled

A convergence worth the incoming seat's attention, offered as **a proposal for their plan and not as a ruling**: the `footprint:` gap (5 of 169 rows), untestable Done-when (132 of 170), and the ruled-but-unverified family appear to be one mechanism — *a row declares what it touches and what would prove it done, in a machine-checkable form*, applied as a **landing predicate on new and touched rows, never as a backfill migration.** Built once it would serve the dependency graph, the close rate, and every future ruling's verifier. **The incoming architect owns whether this is the right spine.**

## Supersedes A7 (owed) — three additions

1. **A JOURNAL anchor for `fe81e896`** — the night branch created that obligation and could not discharge it; it attaches when the report branches merge.
2. **Verify, do not assume, that four ruled dispositions actually executed:** the graph and telemetry commissions folding into intake #29 as amendments, the portability commission folding as a W-wave scope note, and the cloud commission receiving its own intake. The ruling is recorded; the execution is unconfirmed — and an unverified "it landed" is precisely the class N-B measured.
3. **The conformance digest stream** — restore it to `main`, and give it a reader.

---

**One line for whoever folds this:** the bundle is immutable. If governance provides no lawful way to attach an update to an already-cut bundle, that absence is itself a finding worth recording — do not edit the bundle, and do not invent a mechanism to avoid saying so.
