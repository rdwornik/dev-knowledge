=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-10-dev-knowledge-architect-2` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-10-dev-knowledge-architect-2 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Adjudicate.** The ruling debt is still the only thing that moves the number, and it is untouched: `docs/audits/2026-08-09-technical-decision-sheet.md` §7 carries fifteen UNADJUDICATED items and ADR-111 §4 its OPERATOR-owed departure — both owed to this seat. **The overnight cloud lanes are no longer in flight**; ARC-5 archived them (manifest `737dd479` → merge `19aca464` → packet `fd464967`), so what was integration work is now *reading* work: three reports under `docs/audits/2026-08-10-technical-*`, plus this arc's own `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`. Two decisions are queued and are the operator's, not this seat's to assume: whether to absorb the six unmerged `claude/conformance-*` digests (a BROKEN step, named — it is a recurrence of open `[#419]`), and every lane's `## Needs a ruling` section. The strategic frame is unchanged: measured close capacity **3 per arc** against **170 open**, so "under 100" needs 71 closes ≈ 24 arcs — **births are the lever, not throughput**. Task state: `BACKLOG.md`, but read per-row status from `tasks/*.md` frontmatter, never from the generated file.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->The primary checkout on `main`, as the adjudication seat. It may record rulings in `protocols/STANDING_RULINGS.md`, ratify or amend ADRs (ADR-111 first), write intake status and `decided-by` fields, and birth or re-peg BACKLOG rows through `tasks/`. **The batch manifest the overnight lanes needed is already authored and already closed by its packet** — ARC-5 did that, so this seat inherits no open batch and no unmerged lane branch. Any conformance-digest absorption it chooses to run is a fresh operator-authorized act, not a carried obligation. It does NOT author inside a lane's branch, does not edit any immutable class in place (ADRs beyond a status line, transcripts, handoffs, audits), and does not push into a live consumer checkout.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect: the next session rules, it does not advance a named row. Its output is adjudications — fifteen carried §7 items, ADR-111's §4 departure from the ARC-2 clause on ADR-98 §3 grounds, and the `[#511]` fork about the SHAPE of the handoff load rather than its seconds — plus the birth decisions those rulings unblock. ARC-4 is the evidence for choosing this mode over execution: it ran four kill proposals to completion and closed nothing, because all four rested on premises no one had checked. The bottleneck is adjudication quality, not throughput. Mode follows HANDOFF_PROCESS §13 ("define-or-reshape-the-way-of-working → architect"), and the seat boots opus per the amended Ch8 routing matrix.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/arc5-night-batch-archive`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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
reconciled_with: handoff-process@6.2.0
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

# Residual — 2026-08-10-dev-knowledge-architect-2 — the part the repo does not already encode

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
Every drift-flag standing at this cut is **dispositioned and carried**, not new. By reference to
`ecosystem/disposition-register.yaml`: the `#241` undeclared-edge class (prose edges to the two
`_SPEC_REGISTRY` specs, `handoff-process` and `prompt-template`); the `[#310] -> #292`
`preflight_backlog_ids` pair; the `[#504]` `review_artifact_coverage` tally gap; the legacy
`no_ff_merges` entries; and the `#335` `reconciled_versions` template-placeholder entry.

**One register entry is NEW this window, and it is this arc's own doing.** ARC-3 filed intake #30
**verbatim** under an explicit no-body-edits ruling; that body's §E line names
`templates/prompt-template.md`, which mints a prose edge no rephrasing may clear. It was
dispositioned under `#241` on the merits rather than written around the scanner — the same
principle the `[#492]` doc_rot entry established ("rephrasing the date games the detector"). **The
row is uninteresting; the reason it had to exist is not** — see §4, "the rule that is missing".

**`[#310]`'s entry must NOT be retired.** Its `match` keys on the `[#310] -> #292` signature, and
the row deliberately still names `#292` so that signature survives; dropping it would rot the entry
into a stale decoration under the ADR-75 rule.

Re-derive every value live via `PROBES.md` P4/P7 — this bundle states no verdict, no count, no
`[stale]` status and no drifted id by design.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
**ARC-4 closed ZERO rows and birthed ZERO.** That is this arc's finding, not its shortfall — §4.

- `201191f` — the 20th `#241`-class disposition; the ship-gate RED that ARC-3 introduced is cleared.
- `01410f9` — K-1/K-2/K-3 executed as ruled: `[#102]`'s never-run **verify-first clause discharged**;
  `[#308]` **re-pegged** to the intake #25 W-wave carrier decision (W-2/W-3); `[#325]`'s fold
  condition **tested and failed**. No row closed by any of the three.
- `9a7ffcb` — `[#310]`: the 2026-07-21 refutation attached to the row itself, **replacing** the
  escape clause that was the re-proposal vector.
- Earlier arcs this window (ARC 1–3) and their SHAs: `JOURNAL.md` entries `2026-08-09 (h)/(i)/(j)`.
- Task-state: `BACKLOG.md` is **generated**; the per-row source of truth is `tasks/*.md`
  frontmatter. Read status from frontmatter, never from the rendered file — the close path has been
  observed reverting statuses while the gates stayed green.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### (a) THE ADJUDICATION DEBT — the first thing the incoming seat owes

**`docs/audits/2026-08-09-technical-decision-sheet.md`** is the architect's ruling surface, under
two pages. **Its fifteen §7 items plus ADR-111 §4 are UNADJUDICATED and are owed to the incoming
seat.** Nothing below unblocks until they are ruled; §4 items A–D of that sheet are the ones ARC-3
surfaced rather than inherited.

### (b) ADR-111 (Proposed) and its OPERATOR-owed departure

ADR-111 rules that every audit finding is triaged into exactly one of four outcomes (owned /
discharged / candidate / rejected). **§4 is a deliberate departure and must be ruled as its own
decision, not nodded through with the ADR:** it *declines* the ARC-2 contract's literal clause
*"an intake may not become rows without an ADR"*, because that clause contradicts ratified
**ADR-98 §3** — an ADR is authored only at a genuine fork (0..n per intake) while epics are 1..n
per accepted intake. Live practice matches ADR-98: intakes #16, #26 and #25 were each accepted by
recorded operator ruling in `decided-by`, not by ADR. ADR-111 therefore ratifies the weaker
coherent rule — **birth requires a ratified intake**, ADR only where the fork test is met. The
three options (ratify as written · rule the ADR genuinely mandatory, which is an **ADR-98
amendment** and lands as one · reject and leave the pipeline unruled) are on the sheet.

### (c) `STANDING_RULINGS` §H — and the reporting question H2 closes

§H (H1–H4) records the ARC-3 hygiene close-out landings. **H2 settles the open-count reporting
question that A4 carried as open** ("is the count scored on `status:open` or on the rendered
total?"): the velocity line **names the filter it was measured on**. Concretely, at this cut:
**170 `status: open` + 26 `status: deferred` = 196 rendered.** `deferred` is **non-terminal by
construction** — `_TERMINAL_STATUSES = ("closed", "retired", "superseded")` — so a deferred row
stays in the queue by design and both numbers are honest provided the filter is named. The other
three: H1 (a defective-seal bundle retires by external dated marker), H3 (an ADR archives at zero
inbound references), H4 (the `[#502]` import convention — Shape B, corrected spelling).

### (d) THE STRATEGIC ARITHMETIC THE INCOMING SEAT INHERITS

**Measured close capacity is 3 per arc. Against 170 open, the "under 100" target needs 71 closes —
roughly 24 arcs at that rate.** That is the number that should govern how the next window is spent.
Note this sits *below* the 5.67/batch figure in Part 3 below: 5.67 was measured across batches 1–3
where lanes executed pre-adjudicated work; **3 is what adjudication alone yielded.** Both are real;
they measure different activities, and the gap between them is itself the finding in (f).

### (e) `[#511]` — BOTH FIGURES CARRIED, NEITHER RESOLVED

The fork is which handoff load is cut. Two measurements exist and **they do not reconcile. This
bundle deliberately resolves neither.**

- **RELAYED, UNVERIFIED, NOT REPRODUCED IN-REPO** (Part 3 below, verbatim): the cut is **20m48s
  end-to-end**, of which generation is **4s (≈0.03%)** — probes ≈5m27s, locator re-verification
  ≈5m16s, answers/fold/gates ≈4m20s. The outgoing operator states plainly that these were relayed
  by the predecessor seat as a measurement, could not be verified, appear nowhere in the repo, and
  were carried into the ARC-4 contract without their arithmetic being checked.
- **TWO INTERNAL INCONSISTENCIES, both named, neither resolved:** (1) 4s of 20m48s is **≈0.32%**,
  roughly **ten times** the stated 0.03%; (2) the components sum to **≈15m03s** (5m27s + 5m16s +
  4m20s), leaving **≈5m45s of the claimed total unaccounted**.
- **THE ONLY MEASURED LINE IN-REPO**, cited as such: `docs/audits/2026-08-07-technical-handoff-engine-thinning.md`
  — **~4.5s mechanized** (collect_state 525ms · collect_hints 831ms · generate 1,708ms · cold CLI
  3,321ms · probes 1.2s), **~0.25% of a ~30-minute cut**; ~4.7s / ~0.26% after that arc's two new
  invariants.
- **WHAT SURVIVES THE DISPUTE INTACT, and it is what the fork actually needs:** on *every* figure,
  **generation is a rounding error.** The cut's real cost is **probes + locator re-verification +
  answers**. **Rule on the SHAPE of that load — not on seconds, and do not re-measure it.**

### (f) THIS ARC'S OWN FINDING — the one worth carrying above the rows

**All four kill candidates survived contact with their own evidence, so the measured close capacity
of 3 was never exercised.** K-1's verify-first clause had never been run (`stacklit` is real and
matches the row's shape; **`scip-search` does not exist** under that name — the referent is
Sourcegraph SCIP, code-navigation indexing, not the repo-topology summary the row wants). K-3's
fold target could not honestly absorb it (`[#294]` is a validator carrier in `audit-py`; `[#325]`
is a command-file artifact in `settings-json`; `[#236]`, the one same-class row, is closed).

**The defect is not the four proposals — it is an audit claim propagating unchecked onto a decision
surface.** The decision sheet inherited N1's *"the precondition for that escape is now satisfied"*
for K-4. That claim had **already been refuted in commit `9fc1a8b4` on 2026-07-21**, which
examined the same escape clause and kept `[#310]` open because
`validate_residual_completeness.py:33-35` is diff-triggered/prospective-only and explicitly
grandfathers the 2026-07-05 bundle — which still carries its 8 `(fill:` markers. All three legs
re-verified live before the re-ask. **The kill proposal was the symptom.** This is the
"ruled-but-unverified" family of A2 arriving in the consumption layer rather than the execution
layer, and it is why the refutation now lives on the row instead of only in a commit body — the
identical fix A7 item 5 demands for the ADR-archival zero-refs bar.

### (g) IN FLIGHT TONIGHT — three cloud lanes, and what the morning integrator owes

Three cloud lanes were dispatched **read-only** after this arc: a **satisfied-row census**, a
**decision-sheet claim verification**, and an **origin branch census**. **They push report branches
and merge nothing.** Their three report branches are owed to the incoming seat.

**No batch manifest was opened, so the morning integrator authors one BEFORE integrating.** This is
load-bearing, not bookkeeping: `gen_handoff.assert_batch_boundary` and the ADR-110 exemption both
key on a committed manifest, and **the ADR-110 exemption does not cover cloud lanes at all** —
`LANE_BRANCH_RE` wants `worktree-lane-…` while these are `claude/<slug>`. Anchor the queue before
merging any of them; a correct manifest grants nothing there.

### (h) `[#502]` — the mis-attribution, corrected

**`[#502]` is the mutmut row** (`tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`,
"mutmut 3.7.0 mutation-testing evaluation — CI-hosted"). The consolidation report §6.2(a) attributed
the Shape-B `sys.path` ruling to it as *"`[#502]` P3/M import convention"*; that is wrong, and the
architect's own challenge answer says the import convention is **not** `[#502]`'s Done-when. **The
ruling itself is landed at `STANDING_RULINGS` H4** (Shape B, corrected spelling
`[".", "scripts", "deploy"]`). **No open row owns its execution — that row is a batch-4 birth
candidate**, and the sheet's §4 item A is where the ownership fork is stated.

---

## §4b — Carried VERBATIM from the outgoing seat's authored supplement, Parts 2–4

> Source: `$env:CLAUDE_PROMPTS_DIR` + `HANDOFF-SUPPLEMENT-and-session-archive.md` (resolved live to
> `C:/Users/1028120/Downloads`; present, 18,940 bytes). Part 1 (A1–A7) is folded into
> `SUPPLEMENT.md`. Parts 2–4 follow **unedited** — plan-versus-outcome, the measurements and
> register that must survive the cut, and the exit sequence with its contingency.
>
> **Note on Part 3's figures:** its `[#511]` line and its "close capacity 5.67 / distance 62 /
> ~11 batches" line are preserved **as written by the outgoing seat**. Both have been overtaken —
> see (d) and (e) above for the current numbers and the unresolved arithmetic. They are carried
> unedited because a verbatim register is the point; they are **not** to be read as current.
# PART 2 — PLAN VERSUS OUTCOME

Written by hand this once, because the operator asked for it as a *result* and not as a mechanism.

| Planned | Landed | Remains, and why |
|---|---|---|
| Close batch 3 under `[E7]` | **Done** — 10 lanes, 8 rows closed, `dd0cb148` | — |
| Land the ratified-unlanded items from the previous window | **Partly** — the 3.2 cap wording, the 3.3 two-number clause, the ADR-87 amendment landed | Seven items still owed (A7 above); the consolidated write never ran because ARC 1 executed its original steps only |
| Run the closure-adjudication wave | **Not yet** — proposals generated (151 distinct ids), never adjudicated | It is step 1 of the exit sequence and the irreducible core |
| Night batch for handoff prep | **Done** — five reports, findings index, packet, `663c0f9d` | Its ~95 findings and 38 ruling items are untriaged |
| Consolidate and hygienise | **Partly** — ARC 1 merged the last branch, cleaned refs, adjudicated four doc defects, `df1b05b0` | Intakes #30/#31 unfiled; archival unrun; prompts-dir consumption unrun |
| Answer the execution challenge | **Done**, with earned colours; three of my claims refuted by retrieval and accepted | Five inventories witnessed and merged |
| Cut the handoff | **Not yet** — unblocked once the night batch closed | Last step; cannot move |

**What this session proved [judgement]:** the machinery closes work honestly at width 10 without bypasses. **What it did not prove:** that the fleet can consume its own research. Twenty audits, zero rows.

---

# PART 3 — MEASUREMENTS AND REGISTER THAT MUST SURVIVE THE CUT

**The `[#511]` decisive measurement — carry this, do not re-measure it.** The cut is **20m48s end to end**, of which generation is **4s (≈0.03%)**: probes ≈5m27s, locator re-verification ≈5m16s, answers/fold/gates ≈4m20s. The fork is about which of those loads is cut, not about performance.

**Other figures that cost real time to obtain:** full suite **539s** on a clean tree versus **1785.6s** serial baseline (×3.3), and **8m46s** with zero worktrees versus **31m43s** with thirteen — the tree-walk mechanism explains ≈24%, the remainder is plausibly concurrent lane sessions plus filesystem placement, antivirus scanning and editor indexing · all 41 gate checks total **11.66s** (~0.2% of an integration arc — not a cost centre) · collection **1.1%** · the suite is **wait-bound at ~15% CPU** · **5 of 169** open rows declare `footprint:` · close capacity **5.67 per batch at net −1.67** · distance to "under 100 open" is 62, i.e. ~11 batches at zero births.

**Register items that appear nowhere else and would be lost:**
- **`[#507]` `[#508]` `[#509]` `[#510]`** — filed rows absent from every plan register so far.
- **win-tooling S-list** — the merge-gate mechanism (prose lost the operator's merge word on day one), a stale pre-rename path from the 2026-07-10 rename, the pre-existing `test_available_backends` RED, and secrets sitting in a cloud-synced profile. The private remote itself is discharged (15 branches pushed, gitleaks clean, fresh-clone verified).
- **Retained branches, reported not deleted:** `automation/fleet-audit` (163 ahead, never merged) and the `conformance-*` set, which carries standing explicit protection in `git-discipline.md`.
- **Two ARC-1 rulings issued:** the eight `undeclared_edges → prompt-template` WARNs are dispositioned under the same reference as the nine existing `→ handoff-process` ones — mention is not dependency — with the note that **17 WARNs of one class is itself the smell**; and the `review_artifact_coverage` WARN on `df1b05b0` is discharged by **running** the reviewer lane, not by dispositioning it.
- **Corrections to my own earlier claims, so they are not inherited as facts:** `CLAUDE.md` does **not** contradict itself (198 counted lines against a ≤200 budget that excludes comment-only lines; my 242 was raw lines, the wrong unit) · the floor files are **one revision**, not three (identical hashes once CRLF-normalised) · `[#408]` is doc-coupling-on-closure, **not** a distiller · intake #27 §A is **38 rows, not 36** · a subagent-spawning workflow **already exists and is committed**.
- **A path claim to verify rather than inherit:** an arc reported a contract file absent from the prompts directory while the operator's own listing shows it present. Almost certainly a `$env:CLAUDE_PROMPTS_DIR` resolution failure in a session started before the variable was set — have the next arc report what it resolves to before treating any file as lost.

---

# PART 4 — THE EXIT SEQUENCE, AND WHAT TO SACRIFICE

1. **Flip intake #25 to ACCEPTED — alone, first, ten minutes.**
2. **The adjudication wave to completion** (ARC 2 v2 Phase A). The only step that moves the number.
3. Triage, capped births (**≤6**), priority pass (ARC 2 v2 Phases B–F).
4. The seven owed writes, intakes #30/#31, archival verification (ARC 1b).
5. Ratification batch — structured as **yes/no lines with my recommendation attached**, plus **at most five genuine forks**. Anything not in those two shapes is not ready for the operator.
6. **The handoff cut.**

**Contingency, decided in advance:** under context pressure, **sacrifice step 5, never step 6.** The adversarial review can happen in the next window before the operator's GO — his GO has not been given, so nothing is lost by moving it. A session that ends without a bundle strands everything above it.

**The irreducible core if everything else must go:** the adjudication wave · intake #25 flipped · this supplement (done) · the plan-versus-outcome section (done) · this register transcribed into the residual.

**The last honest warning, to myself and to whoever reads this:** Phases B–F look interesting and Phase A does not. Arriving at the end of a window with a beautiful triage surface and a backlog that did not move is the failure mode with the highest probability. **Run the adjudication to completion before enjoying the rest.**


### (i) DISCHARGED BY THE ARC-5 ARCHIVE ARC, 2026-08-10 — appended, nothing above edited

**(g) above is left BYTE-UNCHANGED and is now historical.** It is retained rather than
rewritten: it was true when the ARC-4 bundle was sealed, and append-not-amend is the same
discipline `STANDING_RULINGS` B6 fixed for JOURNAL anchors. This subsection records what
happened to what (g) owed.

- **The three cloud lanes delivered.** One branch, `claude/night-batch-cloud-lanes-a4mpkp`,
  tip `fe81e896`, carrying all three reports — they ran in ONE cloud session, not three, so
  they are file-disjoint but **not process-isolated**. Merged `--no-ff` at **`19aca464`**.
- **(g)'s instruction was followed exactly.** A batch manifest was authored BEFORE
  integrating, in the present tense with its lateness stated:
  `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md` (`737dd479`). It is closed
  by `docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` (`fd464967`).
- **(g)'s exemption reading is CONFIRMED, and it was worth stating.** `LANE_BRANCH_RE` is
  `^worktree-lane-...` and the branch is `claude/<slug>`, so `is_lane_merge` returns `False`
  and the manifest granted **nothing**. The manifest is an archival declaration, not a gate
  key. Zero `SKIP=`, zero `--no-verify`, zero force-pushes, zero deletions across the arc.
- **The anchor `fe81e896` could not discharge is attached** — this arc's JOURNAL entry,
  landed as the last commit before push.
- **The supplement is no longer incomplete.** `SUPPLEMENT.md` in THIS bundle carries two
  verbatim folds: the ARC-4 supplement (A1-A7) unchanged, and the outgoing seat's
  night-batch delta, which supersedes parts of A1-A5 and A7.

**Two of the delta's §A7 items were executed by this arc rather than carried forward:**

1. **Four ruled dispositions VERIFIED — 4 of 4 LANDED**, all in `6a4a1d78`, an ancestor of
   `main`: dependency-graph → intake #29 Fold B; telemetry → intake #29 Fold A; portability
   → the W-9(a) scope note in intake #25; cloud-compute → its own intake #32.
2. **The conformance digest gap is ESTABLISHED as a BROKEN step, and the step is named** —
   the manual, operator-authorized *"absorb the nightly conformance digest"* merge, last run
   `24882f8c` (2026-08-02). Not deliberate; the protection those branches carry is against
   **deletion**, not merging. It is a **recurrence at identical width** of open row `[#419]`
   (first instance `claude/conformance-2026-07-21`…`-26`, also six).

Both in `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`.

**STILL OPEN, and deliberately not acted on:** the six digests were **NOT merged** —
consuming them is an operator act. `2026-08-06` has no branch and is reported
**undetermined from the repo**. Every lane's `## Needs a ruling` section is unadjudicated and
is the incoming architect's, at the batch-4 planning GO.
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
> **Branch note.** This bundle was generated on branch `docs/arc5-night-batch-archive`. This line names only *which*
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-10-dev-knowledge-architect-2/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-10-dev-knowledge-architect-2/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-10-dev-knowledge-architect-2/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-10-dev-knowledge-architect-2/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-10-dev-knowledge-architect-2/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-10-dev-knowledge-architect-2/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-10-dev-knowledge-architect-2/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

---

=== END OF PASTE — 5 sections · 80618 bytes ===
