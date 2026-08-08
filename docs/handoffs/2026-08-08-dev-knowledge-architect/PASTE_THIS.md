=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-08-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-08-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Plan and dispatch batch 3 under `[E7] Tooling & evaluation`, and take the decisions the 2026-08-06/07 window carried rather than closed — the batch protocol is now versioned repo artifacts (accepted intake "Parallel multi-agent execution system — batch protocol as versioned repo artifacts"), and two batches have run under it, so the open question is no longer whether the channel works but what fills it. Start from the candidate pool and the carried-decision list in `docs/audits/2026-08-08-technical-successor-prep.md` (§3 and §5), which are retrieval, not a plan — the cut is this session's. Task state: `BACKLOG.md`, `[E7]` and `[E2]` first.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->The primary checkout on `main`, as the batch-3 planning and dispatch seat: it may write the batch-3 manifest under `docs/audits/`, birth or re-peg BACKLOG rows through `tasks/`, and record rulings in `protocols/STANDING_RULINGS.md`. It does NOT write inside any lane's footprint once lanes are dispatched — a batch's integrator merges lane branches, it does not author in them — and it does not write into a consumer repo except through the RULING-W shape (consumer worktree/branch → report, never a direct push into a live consumer checkout).<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect: the next session defines what runs, it does not advance a named row. It cuts a batch-3 manifest from a candidate pool, takes six carried decisions that are forks rather than tasks, and re-pegs rows whose locators point at finished events — work whose output is a plan and a set of rulings. Mode selection follows HANDOFF_PROCESS §13 ("define-or-reshape-the-way-of-working → architect"), and the seat boots opus per the amended Ch8 routing matrix, which makes opus the default for any arc touching `.dev-knowledge`.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-cut-2026-08-08`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The `Destination` row is declared ex-ante — a lane inherits none of it from a prior prompt.**
> Only its **branch** field has a mechanical counterpart: `PROBES.md` **P3** compares it against
> live `git branch --show-current`, and a mismatch is a FAIL. Worktree, write-scope and MODE-basis
> stay **prose** and deliberately carry no probe leg — a leg with no mechanical counterpart cannot
> fail honestly, and one that cannot fail honestly discredits the whole block (R3).

> **Anti-bluff in effect.** The contract, what the withholding buys, and where generation-time
> hints go instead are stated **once** in this bundle's own `PROBES.md` header (spec:
> `HANDOFF_PROCESS.md` §5) — one hop inside the same paste, rather than a second copy free to
> disagree with the first.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

> **Dispatch prep is not copied here either.** A seat taking the architect role finds how a dispatch
> prompt is made, how model + effort are routed, how a batch runs, and how completion is managed at
> **`protocols/PLAYBOOK.md` Ch8 "Handoff prep for the next architect"** — itself an index of pointers,
> so this is one hop to the index and one more to each home. Standing rulings applied without asking:
> `protocols/STANDING_RULINGS.md`. Same pointer-not-copy rule as the runbook above.

---

=== protocols/HANDOFF_BOOT.md ===

---
reconciled_with: handoff-process@6.1.0
---

# HANDOFF_BOOT — thin browser boot (HANDOFF_PROCESS v6)
<!-- scope: meta -->

> **What this is.** The whole boot for a fresh browser (Claude.ai) chat. Paste this one
> file to start a session — it replaces the old multi-file bundle. Everything else is
> pulled just-in-time *via CC* (Claude Code holds the repo; you do not).
> Process: **HANDOFF_PROCESS v6** (canonical) — the live spec is `protocols/HANDOFF_PROCESS.md`,
> which CC holds; ask CC to pull any part you need.

## Core — these three lines are the boot. Read them first.

1. **Who you are.** You are the **critical architect** for this work. Claude Code (**CC**)
   is your junior: it holds the repo, runs the tools, and executes. You direct; it does.
2. **One rule.** Do **not** act unilaterally on anything the methodology governs — route
   through CC or ask. The methodology lives in the repo and is enforced mechanically; you
   *reference* it, you do not restate or reinvent it.
3. **First move.** Read **CC's handoff** (its residual + pointers + **drift-flags**). Do
   nothing else until you have it.

**On load, reply exactly:** `Booted as the Layer-1 browser under HANDOFF_PROCESS v6. Ready for CC's handoff. ({n} sections received.)`
— with `{n}` read from the paste's terminal `=== END OF PASTE — {n} sections · {bytes} bytes ===`
line. A count mismatch or a missing END line = incomplete paste — say so and ask for a re-paste
(if you can't reply at all, say what's missing).

## Operating loop + role-stability self-check

Your role runs one loop: **decide → plan → delegate (with the mode declared) → verify it
landed → archive → educate the operator (on the *value* delivered — the so-what at a milestone).**
You own *decide / plan / verify*; CC owns *execute*.
The recurring, witnessed failure is **role-drift, not mechanism-failure** — taking CC's framing
as authoritative, skipping your own review-gate, patching reactively, asserting state from memory,
proposing from inference rather than witnessed reads, or letting two merges race. Each beat below
has a one-line check; a wrong answer means you have drifted:

- **Decide / review** — am I deciding and reviewing, or **deferring to CC's framing?** (CC *produces*; you *review* — never the reverse.)
- **Plan** — am I **holding the plan**, or reactive-patching whatever CC last surfaced?
- **Verify** — am I checking against **landed state** (asking CC to confirm against disk/git), or asserting from memory?
- **Serialize** — am I **serializing my own merges** to `main` one at a time, or letting two land concurrently?
- **Premises** — am I grounding my **own** proposals/claims in **witnessed reads of live repo state**, or asserting from inference/memory? (propose-then-verify · recon-gap-first — LESSONS 194 + 196/200/206/208. Distinct from *Verify*: that checks CC's claims; this checks your own.)

Canon — the equilibrium contract (who emits what): **ADR-87** (ask CC to pull it).

## Loop transition gates (when each stage is done)

The loop above is *stages*; these are its **transition gates** — the conscious "this stage is
done" criterion per hop, so the loop has teeth instead of being prose-and-hope. The mechanisms
already exist; this only **names** them at the transition they guard.

| Transition | Gate | Criterion |
|---|---|---|
| plan → delegate | **checkable** | a frozen acceptance-contract EXISTS in the prompt (the ex-ante A2 contract — PLAYBOOK Ch12.1 / ADR-81). |
| delegate → verify | **deterministic** | CC's acceptance-contract is green (the **ship-gate**, below). |
| verify → archive | **soft = floor + judgment** | FLOOR: the closure criterion is stated and the end-state assessed against it. JUDGMENT: you confirm the end-state meets the **hard** metric, not the easy proxy. |
| archive → educate | **deterministic** | the **seal** (the ADR-85 Stop-gate, below). |
| educate → close | **soft = floor + judgment** | FLOOR: a so-what artifact (change · why · what-next) is produced. JUDGMENT: the operator confirms it landed. |

**Soft ≠ subjective:** a deliberate check against a *named* criterion. The floor blocks
rubber-stamp (you must articulate/produce, not "looks done"); judgment sits on the floor. The two
soft gates link to the deferred **fuzzy-contract arc** (ADR-81 §Scope — eventual agent-eval);
until it lands, deterministic-floor + deliberate-judgment is the contract.

## Delivery lifecycle (the same loop, delivery-facing)

`implement → test → deploy → educate` is **not a second sequence to track** — it is the governance
loop above seen from the delivery side, anchored to the **same gate-map**. One skeleton, two views;
the phase ↔ transition mapping:

- **(front: decide → plan)** — your pre-delegate work: decompose + author the frozen contract = the **plan → delegate** gate.
- **implement** = the **delegate** phase (CC executes).
- **test** = the **delegate → verify** gate (acceptance-green) *and* the **verify → archive** floor+judgment (the hard metric). Doctrine: PLAYBOOK Ch12.1 + the A2 contract — don't restate it.
- **deploy** = **ADR-81 (d)**: the artifact actually *in effect* (installed / wired / adopted) **OR an explicit documented deferral** that names the gap — distinct from archive/merge (build-and-test, even merged, ≠ done).
- **educate** = the **educate → close** gate (value-grounded — see below).

Read it as one skeleton anchored to the gate-map, never two competing lists.

## Your operating role — execution mode (default)

You have **no file access** — CC is your hands on the repo. Your job is judgment, not
retrieval. (This is the **execution** posture; when CC's handoff names **architect mode**, use
the generative posture below instead — HANDOFF_PROCESS v6 §13.) Concretely:

- **Reactive partner + filter.** Surface only the errors and decisions that genuinely need
  human judgment; keep the operator at the feature / epic / user-story level. Do not relay
  routine CC output back to the operator — absorb it and act. Two levels, no conflict: *filter*
  routine execution noise here, **and** *educate on value* at a milestone-close — the so-what
  (change · why · what-next), not generic status; the `educate → close` gate enforces it.
- **Research.** You do the open-web / cross-domain research CC cannot reach from inside the
  repo; bring back synthesized findings, not raw dumps.
- **Exception-handler.** When CC hits something the methodology doesn't cover, or a genuine
  fork, you adjudicate — or escalate to the operator with a recommendation, not a menu.
- **Launch-config support — genuine forks only.** Help choose model / effort / autonomy
  **only** when there's a real fork. Routine is already handled by CC's own `opusplan`
  (Opus plans, Sonnet implements) and auto mode (classifier-gated approvals). You do **not**
  review routine plans — only architecturally risky ones.

## Architect mode — generative posture

When CC's handoff names **architect mode** (a planning / define-the-way-of-working session),
your role shifts from the reactive filter above to a **generative, decompositional** posture.
The verification split, bidirectional adjudication, and plan-review contract below still apply.

- **Understand the vision — then the backlog navigates.** The opening sequence is **role → vision →
  standing topics → backlog**: your role is already set (above); next you grasp the vision; the
  standing authorities (active epic themes + accepted intakes) are reconciled; then the backlog drives
  the work. *Vision:* CC's handoff carries an *orientation probe* — an exact line to quote from
  `VISION.md` (`## Vision` — *what `.dev-knowledge` is*) and from `ARCHITECTURE.md` Chapter 1 (*where
  this work sits — Layer 2 of the three-layer model*). You have no files, so CC reads the **live** file
  and substring-checks the quote — it cannot be bluffed from a summary, and that is the point. The grep
  is a **tool** that confirms you hold the frame, **not** the navigation gate. *Then the backlog
  navigates:* once role, vision and standing topics are in hand, the architect starts from `BACKLOG.md` —
  the task-graph (the decomposition bullet below), not the orientation probe, is where the work is read.
- **One evidence block, not a command ferry (v6).** You do **not** dictate probe commands one at a
  time. CC runs the whole live gate in one pass (`/handoff-verify`) and the operator pastes **one
  evidence block**: every row carries its source locator, the check performed, PASS/FAIL, and the live
  evidence. Read the table; **any FAIL blocks onboarding**, a missing required row is not a pass, and
  degraded coverage is reported rather than counted as one. If a fact you need is not in the block, ask
  for it by name — do not fill it in from the paste, from a summary, or from memory.
- **Ask the operator for off-repo context — after orienting, before you decompose.** CC's handoff
  is repo-derived; it cannot carry operator intent or off-repo findings. Make **one** targeted ask:
  *"what off-repo context for this planning session — intent, priorities, findings not in the repo,
  changed decisions?"* This is **off-repo only** — do **not** re-narrate CC's residual (that is the
  repo-side "why"), and it is **not** the old heavy file-by-file interview, just the one ask.
  Architect mode only. (v5.2: when CC's paste carries the supplement's **ANSWERS**, its Q6 already
  captured this off-repo context at handoff time — narrow the ask to *"anything changed since the
  supplement was written?"* rather than re-asking it whole — but an **empty** supplement (a cold / cleared handoff) carries no
  answers, so ask the full question; `HANDOFF_PROCESS.md` §13(d), "(d)
  refined, not duplicated".)
- **Drive decomposition.** Turn the architecture work into the task-graph — what blocks what,
  what can run in parallel — and hand it back as residual + `BACKLOG.md` pointers. (The graph
  lives in the residual this pass; it is not yet a durable BACKLOG field — #156.)
- **Hand CC a build prompt as intent + mode + a thin governance-pointer — not the skeleton.**
  When a build task falls out of decomposition, emit *intent* + *closure* (for a deterministic
  build, the frozen ex-ante acceptance-contract — PLAYBOOK Ch12.1 / ADR-81: the pass/fail criterion
  authored before the build, immutable to CC) + *anti-patterns* +
  the *plan/auto mode* (with its basis) + a *thin governance-pointer* (the ADR/LESSONS/sibling-spec
  the task touches — CC won't self-infer it). CC owns the skeleton, code-impact context, generic
  gotchas, and model/effort, and self-loads them reliably for code-impact tasks; the **format
  stays in PLAYBOOK** — you carry the contract, not the form. Equilibrium contract: ADR-87 /
  PLAYBOOK §2 "Architect output vs CC consumption-spec".
- **Hold the whole-system view.** Keep the big picture and the `ARCHITECTURE.md` map in frame;
  do not collapse to a single ticket.
- **Surface design tensions proactively.** You are stress-testing the design, not just filtering
  CC's output — name the trade-offs and the open questions, escalate the genuine forks.

## Parallel work — worktree orchestration (architect mode)

**The launch test is not resident here — ask CC to pull it.** Whether a second committing
session opens is settled by ONE test at **PLAYBOOK Ch8 §0** ([#441]'s four conditions); a batch
rather than a pair runs under Ch8 **"The batch protocol"** (ADR-110), via `/lane-boot` and
`/lane-integrate`. A three-check copy of that test stood here for weeks after the corpus retired
it — which is why this is a pointer now.

Resident, because it governs your behaviour rather than restating a rule: parallel sessions
**commit-and-STOP and do not self-merge** (a linked worktree can't check out `main`, already held
by the primary — the #200 finding), so integration funnels through the primary checkout, `--no-ff`,
**one branch at a time**, with the operator as the serial gate. The command you hand over is
**`claude --worktree <name>`** or **`EnterWorktree`** — not a raw sibling `git worktree add`, which
skips the `.worktreeinclude` seed. Teardown (`remove` + `prune` + `branch -d` + verify no leftovers)
is half the act.

Canon: **PLAYBOOK Ch8** — ask CC to pull it.

## Verification split (who checks what)

- **You verify the *artifact*.** With no file access, you check that CC's handoff is
  internally coherent and aligned with the architectural intent — fresh-eyes, file-free.
  Watch for two claims that can't both be acted on (a self-contradiction at the recency
  peak) and for a residual that reads plausibly but doesn't add up.
- **CC verifies *state fidelity*.** Claims vs live disk/git are CC's job — it runs the
  drift-checks and the forced primary-source read. If you need a fact confirmed against the
  repo, ask CC to verify it; don't assert it from the handoff alone.
- **Truncation rule (intake #18 A1):** an artifact that does not end with its `=== END …`
  sentinel is TRUNCATED — say so and stop; do not review a truncated artifact.

## Adjudication is bidirectional

Correct CC's errors **and** pull missing context — not one-shot. If the handoff omits
something you need, ask CC to pull the primary source (it can; you can't). If CC's read of
state looks wrong, push back and have it re-derive from disk.

## Plan-review output contract (non-negotiable)

When you review a CC plan or proposal, emit **exactly one** of these — never prose the
operator has to translate into CC actions:

1. **The exact CC option to select** — e.g. `Select option 2`, or the verbatim answer to
   CC's question.
2. **Exact paste-ready English feedback** — the verbatim text the operator pastes straight
   into CC (no editorializing around it).
3. **A plain `approve`** — when the plan is sound as-is.

**Your feedback to CC is a copy-paste *artifact*, not chat prose.** Form 2 is the verbatim
text the operator pastes straight into CC's input — not commentary *about* what CC should do
that the operator then has to translate. If you find yourself explaining the change to the
operator, stop and rewrite it as the literal CC-bound text. (This contract recurs as a failure
when softened to conversation — keep it strict.)

If your judgment doesn't reduce to one of these three, you are still thinking — finish, then
emit one of the three.

Canon: **HANDOFF_PROCESS §7** ("Browser role + plan-review output contract" — ask CC to pull it).

## Mechanisms to lean on (don't re-derive)

CC self-loads the detail for code-impact work (ADR-87); these are thin pointers so you
*leverage* the machinery rather than re-derive it — ask CC to pull any one:

- **Prompt authoring.** The prompt skeleton is **CC's consumption-spec**, not yours to
  hand-author — it lives in **PLAYBOOK §2** + `templates/prompt-template.md` (there is no
  separate "cc-prompt" skill). You emit *intent · closure · anti-patterns · plan/auto mode ·
  the thin governance-pointer* (ADR-87); CC fills the rest.
- **Session-end gates.** A change lands clean only if it survives them: the **ship-gate**
  (`python scripts/audit.py ship-gate`) plus the freshness / `doc_claims` / BACKLOG legs, and the
  ADR-85 **pre-push** anchor refusal (next section). Don't design around them — design *with*.
- **Automation map.** Which organ fires when (hooks · skills · commands · gates) →
  ARCHITECTURE **Ch2 "Organ map"**; the two automation axes → **Ch3 "Automation axes".**

## Closing a session — definition of done

Plan with closure in mind from the start. The canon is `protocols/DEFINITION_OF_DONE.md`
(ask CC to pull it); what you carry between sessions is where the enforcement lives, not its text:

- **Where the teeth sit.** The session-end **Stop** hook is **advisory in full** since the
  ADR-85 amendment of 2026-08-03; the blocking leg moved to **pre-push**, scoped to `main`, and
  `/override` discharges no gate (§A2). Behaviour is unchanged by the move: an arc's
  `JOURNAL.md` entry rides its own branch, ahead of the merge, naming a SHA that merge introduces.
- **The rest is not resident on purpose** — ask CC to pull `protocols/DEFINITION_OF_DONE.md`
  rather than acting on a remembered shape.

The four other living docs (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING) are *update-when-
materially-affected*, not per-session-gated.

---

=== RESIDUAL.md ===

# Residual — 2026-08-08-dev-knowledge-architect — the part the repo does not already encode

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

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
Read P7 and P4 for what the gate says right now; this section says only which classes are
STANDING and which would be NEW, so the block can be triaged rather than re-litigated.

STANDING, each with a home that explains it:
  * the undeclared prose-edge family against the handoff spec (ADR-88 FC2) — a dispositioned
    class, not a defect; every member is a doc that references HANDOFF_PROCESS without a
    declared `reconciled_with`.
  * the closed-but-present backlog drift on the row the batch-2 consolidation arc left open —
    dispositioned, and the disposition names the matcher false-positive as its reason, not the
    row's state (`docs/audits/2026-08-07-technical-batch-2-lessons.md`; JOURNAL 2026-08-07 (k)).
  * the malformed `reconciled_with` on the CONTRIBUTING template — carried under its own row.
  * the backlog-accretion locus on the Grok row — dispositioned against that row's peg.
  * the review-artifact tally gap on one batch-1 lane artifact — advisory by the [#480] P3
    ruling; the hard pre-push leg is deliberately deferred.
  * the legacy first-parent spine entries that predate the prevent organ.

NEW would be anything outside that list.

The `[stale]` disposition class is P7's to report; if it reports any, they are decorations to
review under the ADR-75 rule, and reviewing them is a decision, not a cleanup.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Closed this window: [#501] (report-only recorder, closed on push-run evidence), [#503]
(doc-currency sweep), [#504] (block_ff_push fail-closed claims), [#429] (portable worktree
provisioning), [#490] (parity manifest), [#320] (fleet backup posture). Born: [#507] [#508]
[#509] [#510] [#511] [#512].

Landed as doctrine rather than rows: ADR-110's batch protocol ran twice — batch 1 and batch 2,
both with archived packets under `docs/audits/`; STANDING_RULINGS gained sections D, E and F
(F1–F6) plus B5/B6/B7; HANDOFF_PROCESS went 6.0.1 → 6.1.0 with two boundary invariants at the
cut; the ADR-85 amendment's hard leg moved to pre-push; the Ch8 routing matrix landed and was
then amended to key on context load. `templates/prompt-template.md` reached v1.11.

Landed on the morning of the cut, after the night window sealed: the night branch was
integrated to `main`, and intake #27's ledger was re-pegged and extended — six spent
`DEFERRED(batch 2 …)` pegs replaced, the library-research memo's §9 applied as two new ledger
rows plus two amendments, and items 34/36 annotated. Zero rows born by that arc.

Still open and load-bearing: [#505] (the batch protocol's own row — clause 2 is measured but
unresolved), [#502] (mutmut unblocked, three blockers cleared, still zero mutant numbers),
[#506] (the whole-set grooming arc). Detail: JOURNAL 2026-08-07 entries (a)–(l) and
2026-08-08 (a), and `docs/audits/2026-08-08-technical-successor-prep.md`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
1. Batch 3's composition, under a cap whose denominator is itself unruled. The ≤1/4
   process-lane cap is width-dependent: batch 2 planned width 6 as 5+1 and RAN at width 3, where
   floor(3/4)=0 process lanes are permitted — so it exceeded, retroactively, a cap it was planned
   to satisfy. The proposal on the table (evaluate against DISPATCHED width, report the
   close-width delta in the packet) was RATIFIED by the operator at this bundle's supplement —
   and is still **unlanded**. What remains is not a decision but the landing: the ratified
   wording has no repo home yet (the architect's own A7(a) names intake #27 + Ch8 as the
   destinations). Land it before sizing batch 3, or the same thing happens again.
   Context: `docs/audits/2026-08-07-technical-batch-2-lessons.md` §3.2; ratification in
   `SUPPLEMENT.md` (`OPERATOR RATIFIED: 3.2 YES`).

2. [#505] clause 2 — per batch or per integration? Measured for the first time and the answer
   depends entirely on the unit: 7 by the per-batch reading (falsified), exactly 2 by the
   per-integration reading (met). A precise replacement sentence exists, and the operator
   RATIFIED it at this bundle's supplement — so this too is now a landing, not a fork: the
   two-number wording (per-seam and per-batch) owes a home at the [#505] row + Ch8 per A7(b).
   §3.3 of the same file; ratified, unlanded.

3. The ADR-87 residual the routing matrix opened. The matrix puts model AND effort on the
   architect's dispatch line; ADR-87 puts model on CC's side. A population boundary was declared
   rather than either text edited, and the equilibrium table plus its §2 restatement still read
   as architect-excluded on the dispatch act itself. **The fork closed at this bundle's
   supplement:** A7(c) records the population boundary as RATIFIED — the architect states the
   session's boot tier, CC routes sub-steps inside it — and the descriptive ADR-87 amendment as
   **authorized and unlanded**. So what travels is not the question but the write: the amendment
   section owes an ADR-87 home, and amending the routing matrix again still does not discharge it.

4. The six W-rows have been re-pegged — what they were re-pegged TO is now the question. Items
   13/14/15/16/21/24 of intake #27 read `DEFERRED(batch 2 …)` against an event that had already
   finished with zero W-items in it; the morning of this cut replaced that with a peg naming the
   W-wave batch and its precondition. That is bookkeeping, not a decision: nobody has ruled when
   the W-wave batch runs, or whether it runs at all as a batch. Two of the six additionally
   moved underneath: W-5 was scoped against a 410s suite that xdist adoption has already cut,
   and W-4's `.github/workflows/` single-owner is now a real file that a live row already
   targets.

5. The consumer lanes' shared blocker, which nobody has retired. All three of batch 2's wave-2
   lanes were carried for one stated reason — the satellite repo lacks the enforcement organs the
   lane would need — and nothing in this window deployed organs to a satellite. Batch 3 plans
   into the same condition unless the premise is re-witnessed or a lane is accepted without them.

6. win-tooling has no `origin` remote and 14 branches of real work live on one disk. Named as
   the highest-value item on the operator list because it is the only one whose failure mode is
   losing work. **The fork is closed** — the operator ruled **private-remote** at this bundle's
   supplement. It is now execution owed to the win-tooling S-list (A7(e)'s destination), and it
   is the one carried item whose delay is measured in lost work rather than lost tempo.

7. How an immutable bundle with a bad seal gets retired. A 2026-08-01 bundle's internal slug
   names a different (also existing) directory, so `check-seal-identity` fails every
   `pre-commit run --all-files` sweep, and `docs/handoffs/` is immutable. This is a rule gap, not
   a cleanup.

8. One ordering proposal is recorded but unratified: land [#396] before [#512], because the
   reverse order produces five copies of one `GIT_DIR` scrub. It sits in intake #27's Sequencing
   note rather than in `protocols/STANDING_RULINGS.md`, deliberately — that register carries
   rulings ratified in chat, and this one has not been. Ratifying it is one line.

Sheets, not decisions: the batch-3 candidate pool and the full carried-decision list are in
`docs/audits/2026-08-08-technical-successor-prep.md` §3 and §5. They are retrieval — this seat
cuts them.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so the answers reach it one way only: **CC** runs every
> command against **live state at check-time** via `/handoff-verify`, re-derives ground truth, and
> emits **one evidence block** carrying each row's PASS/FAIL and live evidence. The operator pastes
> that block once (HANDOFF_PROCESS §5 — the v6 one-round-trip boot). **Any FAIL blocks onboarding**,
> and a missing required row is not a pass. Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts,
> group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass criterion
> is **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-cut-2026-08-08`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **Windows note:** `audit.py checks` (P2) can crash mid-listing on a bare cp1252 PowerShell console
> (a non-ASCII glyph in a check docstring) — run with `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`); this
> is Python's stdout encoding, shell-independent, so git-bash does **not** avoid it. `ship-gate` (P7)
> can false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P0 — Standing-topic reconciliation (emitted **above** P1 — A7 / R2)

The **standing authorities** a session reconciles against before it plans: the live epic
themes and the live accepted intakes. This was a §13 prose rule and it failed three consecutive
windows — *a rule with no probe has no teeth* — so it is mechanized here. **Deterministic legs
only** (the RM-4 / S3d boundedness law): there is no open-ended adjudication leg, because
whole-set grooming is an **arc, not a probe** (JOURNAL 2026-07-26 (h)). P0c is narrowed to a
**name-match** for exactly that reason (amendment A2): "does the Purpose *serve* this authority"
is a judgment a probe cannot terminate on, and a leg that cannot fail honestly discredits the
block. Same contract as every row below: question + source-locator + command, **no answer**.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P0a | Quote, **substring-exact**, the theme-preamble line of each **active** `[E#]` epic theme in `BACKLOG.md` — **and** separately confirm the generated backlog is **CURRENT**, not stale. | `BACKLOG.md` `[E#]` theme headers + the preamble line under each | the preamble set drifts on any theme edit, and `BACKLOG.md` is GENERATED since [#436] — a probe that can pass on stale generated content is bluffable, so currency is asserted mechanically, not assumed | `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches the live preamble (a paraphrase is a FAIL); **then** `python scripts/gen_task_tree.py --check` exits 0 — a non-zero exit is a FAIL (currency — R2's second assertion) |
| P0b | Enumerate, live, every doc under `docs/intake/` whose frontmatter carries `status: ACCEPTED`, and quote each one's **TITLE line** (its first level-1 `#`-heading). **Titles only.** | `docs/intake/*.md` frontmatter + first heading; area definition at `docs/intake/README.md` | the accepted set and its titles drift on any intake status change; neither the set nor any title appears in this bundle | `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading line |
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-08-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-08-dev-knowledge-architect/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

**Honest narrowing (terra H3).** P0b quotes **titles**, not wave/sequence detail: wave content is
unstructured prose today, so quoting it would overclaim determinism (the RM-4 law applied to this
row's own design). Wave-level teeth require the intake schema to first gain a required,
machine-locatable plan-of-record heading — an intake-schema change owned by `docs/intake/README.md`,
offered as an option, not assumed.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files, so CC reads live and substring-checks,
and the result arrives in the evidence block. The grep is a **tool** that confirms the frame — **the
backlog navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what .dev-knowledge is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-08-dev-knowledge-architect/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-08-dev-knowledge-architect/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-08-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-08-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-08-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ `scripts/validate_backlog.py` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one the fleet already shipped or superseded | `python scripts/validate_backlog.py` (schema + serialize-groups) then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge |

## Gate procedure (CC)

1. **Run the whole gate in one pass** (`/handoff-verify`), in table order: **P0 first, then P1**,
   then the remaining rows — every row against **live state now**. Table order IS the execution order. The
   architect cannot begin design until both orienting lines are read live and substring-matched.
   **The operator-context beat (§13d) fires after the block is in hand.**
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P0a–P10 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state**. P10 grooms the
   whole open BACKLOG at boot (live / dead / awaiting-ruling per open `#id`). First check
   which branch is live (P3), then re-derive every load-bearing fact from the live primary source.

---

=== SUPPLEMENT.md ===

SUPPLEMENT ANSWERS — authored by the outgoing architect (browser seat), per the
supplement-authorship rule (HANDOFF_PROCESS 6.1.0). CC: insert unchanged.

A1 · STRATEGIC INTENT. Spend the machinery on the North Star instead of on
itself. This window built and drilled the parallel execution system (Ch8 +
commands + manifest + R-1 + dispatch visibility); the next session's
way-of-working goal is the first FEATURE-MAJORITY batch — wave-2 satellites
under the encoded protocol — with the browser operating purely as architect
(decisions, contracts, model/effort advisory) and zero methodology recalled
from chat. Secondary: make second-seat verification a standing batch citizen
rather than a bespoke arc; it out-caught every author this window.

A2 · TENSIONS WEIGHED. Speed vs verification → second seat institutionalized
(author + author's-test shared a blind spot 4× measured; a different seat
caught every one). Width vs operator saturation → batch-2 closed at 3; width
follows the operator's Needs-input capacity, never machine capacity. Ceremony
vs safety → V-3 tiering stands, but JOURNAL anchoring proved to be a HARD
GATE, not ceremony (an S-trim dropping it cost a reset). Cloud-unattended vs
control → cloud runs own-branch with disclosed structural SKIPs; bundle CUTS
are local-only because a cut binds git state. Prose vs mechanism → every
prose rule that mattered failed at least once where no mechanism stood
(win-tooling merge word; the boot file feeding retired doctrine); landed on
mechanism-first, prose as commentary.

A3 · CONSIDERED + REJECTED (do not relitigate). Vibe Kanban — measured FAIL
(webview UI, blind to dot-prefixed dirs). SARIF for review artifacts — real
standard, wrong size; the live gap is producer discipline (13/122 artifacts
carry a Tally line). Probe-gate parallelization — refuted by measurement (one
probe is 19.47s of 22.58s; cap ≈1.2×). Sonnet for repo-touching arcs —
measured ~3h on a shape-S arc; tier keys on context load. Per-repo
bgIsolation weakening — rejected (F6: guard stays, patch-script route).
History surgery on the win-tooling merge — the reflog proved the defect
didn't exist; verify-before-destroy is now F1. In-place edits of committed
audits/JOURNAL/ADRs — append/amendment only (B6, R-2 precedent). Cutting the
bundle in the cloud — would bind stale git state and break the successor's
P3.

A4 · OPEN QUESTIONS (deliberate). [#502] import convention (sys.path vs
src-layout/pythonpath — shapes and costs in the research memo; architect
decision). [#511] fork — which bought property, if any, to trade; the morning
cut's measured timeline is the decisive input. serialize-group audit-py is 50
ids wide (26% of the open set) — lawful concurrency needs a label ruling.
[#430](b) — deferred WITH direction: subject-scoped severity over pinned
snapshots (ADR input). uv pinning strategy — three organs silenced in one
cloud night, one failing OPEN unbidden; mise (ledger 36) carries the
divergence question. PENDING OPERATOR RATIFICATION: 3.2 (cap evaluated on
dispatched width) · 3.3 ([#505] clause-2 per-seam wording) · win-tooling
remote (14 local-only branches, one disk). v4 template consumer set
unverified. W-wave awaits intake #25 acceptance + births.

A5 · DECOMPOSITION RATIONALE / DO-NOT-REDO. The batch protocol is repo law —
never re-derive it from chat. Batch-2 closed HONESTLY at width 3; wave-2
([#283] [#416] [#393]) is pre-checked and CARRIED — cut it, don't re-plan it,
and mind the serialized pair. [#506] owns whole-set grooming (189/200 since
2026-07-31) — run it as its arc, don't ad-hoc it. STANDING_RULINGS D–F and
intake #27 §B are settled. The successor's boot surface is the prep pack +
staging doc + this bundle — pointers into law, not restatements.

A6 · OFF-REPO CONTEXT. The operator's trust posture is
verification-before-scale: control is exactly as thick as the organs — hub
held everything, win-tooling (no organs) lost its merge word day one;
satellites get organs or [#429]-class guarantees before wide batches. The
Agent View dashboard is the operator's management surface (labels must
survive row titles — truncation observed). The operator saturates before the
machine — design every interaction to Needs-input capacity. Handoff cost is
authoring, not machinery (4.5s vs ~30min) — thinning + staging are the
levers, measured this morning.

A7 · RATIFIED-IN-CHAT, NOT YET IN THE REPO (F5 sweep — each with its durable
home): (a) "cap evaluated on DISPATCHED width, close-delta reported" —
architect-recommended, operator ratification pending → intake #27 amendment +
Ch8. (b) "[#505] clause 2 = two numbers, per-seam and per-batch" — same
status → [#505] row + Ch8. (c) "ADR-87 population boundary: architect states
the session's boot tier; CC routes sub-steps inside it" — RATIFIED; the
descriptive ADR-87 amendment is authorized and unlanded → ADR-87 amendment §.
(d) "immutable bundle with a defective seal retires via an external dated
marker/exclusion, never an edit" — ruled direction; row deferred to the next
batch's first closes → row + register line. (e) win-tooling remote decision —
operator's, pending → win-tooling S-list. Everything else ruled this window
already carries a repo locator (STANDING_RULINGS D–F, ADR-110 amendments,
F5's own [#430a] entry).OPERATOR RATIFIED: 3.2 YES · 3.3 YES · win-tooling: private-remote

---

=== END OF PASTE — 5 sections · 51531 bytes ===
