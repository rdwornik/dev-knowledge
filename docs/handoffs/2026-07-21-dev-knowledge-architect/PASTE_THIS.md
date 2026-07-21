=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-21-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-21-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Break the plan→ship deadlock by DELIVERING one thing end-to-end — this session is judged on delivery, not planning.** The operator's mandate (see `SUPPLEMENT.md`, which is filled and authoritative on sequencing) is a single lane: dissolve `assets/` in ai-council to a **deployed, operator-witnessed** end-state — already granted 2026-07-19, so execute it rather than re-seeking permission. Merged is not done; witnessed is done. Treat any new audit, intake, or ADR as a distraction unless it directly enables that one shipped change, and read `SUPPLEMENT.md` **before** `RESIDUAL.md` §4 — §4 was written from repo state alone and carries an inline reconciliation marking where the supplement overrides it. Repo-side context that is *not* in the supplement and still stands: `RESIDUAL.md` §4 items 4 and 5 (a witnessed contradiction between two sibling night-batch lanes, and the code audit's independent rediscovery of `[E8]`'s own thesis). Task-state pointer: `BACKLOG.md` `[E8]`.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-dev-knowledge-architect-0721`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **Anti-bluff in effect (read `PROBES.md` header).** This bundle **withholds every probe answer
> value** by construction — no counts, SHAs, dates, verdicts, or orienting lines. The withholding IS
> the teeth; run the commands. Generation-time drift hints live in the JOURNAL generation-entry, which
> the browser never sees — never in this bundle.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

---

=== protocols/HANDOFF_BOOT.md ===

---
reconciled_with: handoff-process@5.7
---

# HANDOFF_BOOT — thin browser boot (HANDOFF_PROCESS v5)
<!-- scope: meta -->

> **What this is.** The whole boot for a fresh browser (Claude.ai) chat. Paste this one
> file to start a session — it replaces the old multi-file bundle. Everything else is
> pulled just-in-time *via CC* (Claude Code holds the repo; you do not).
> Process: **HANDOFF_PROCESS v5** (canonical) — the live spec is `protocols/HANDOFF_PROCESS.md`,
> which CC holds; ask CC to pull any part you need.

## Core — these three lines are the boot. Read them first.

1. **Who you are.** You are the **critical architect** for this work. Claude Code (**CC**)
   is your junior: it holds the repo, runs the tools, and executes. You direct; it does.
2. **One rule.** Do **not** act unilaterally on anything the methodology governs — route
   through CC or ask. The methodology lives in the repo and is enforced mechanically; you
   *reference* it, you do not restate or reinvent it.
3. **First move.** Read **CC's handoff** (its residual + pointers + **drift-flags**). Do
   nothing else until you have it.

**On load, reply exactly:** `Booted as the Layer-1 browser under HANDOFF_PROCESS v5. Ready for CC's handoff.`
— so a partial or missing paste is visible (if you can't, say what's missing).

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
the generative posture below instead — HANDOFF_PROCESS v5 §13.) Concretely:

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
  backlog**: your role is already set (above); next you grasp the vision; then the backlog drives the
  work. *Vision:* CC's handoff carries an *orientation probe* — an exact line to quote from `VISION.md`
  (`## Vision` — *what `.dev-knowledge` is*) and from `ARCHITECTURE.md` Chapter 1 (*where this work
  sits — Layer 2 of the three-layer model*). You have no files, so reply **"run `<command>`"**; CC reads
  the **live** file and substring-checks the quote — it cannot be bluffed from a summary, and that is the
  point. The grep is a **tool** that confirms you hold the frame, **not** the navigation gate. *Then the
  backlog navigates:* once role and vision are in hand, the architect starts from `BACKLOG.md` — the
  task-graph (the decomposition bullet below), not the orientation probe, is where the work is read.
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

When two genuinely independent streams can run at once, parallelize via worktrees; otherwise
serial is cheaper. **Decision-rule (apply BEFORE splitting — all three must be YES):** the
streams touch **disjoint substantive files**; they are **two distinct goals** (not "finish the
rest of X" — that is one goal, done serially); **each stream is more than a single-file edit.**
Keep it to ~2–3 streams; a safe default pair is **one code item ∥ one doc item** (disjoint by
construction). Below that bar, do the items serially.

The command you hand the operator is **`claude --worktree <name>`** (new terminal) or
**`EnterWorktree`** (mid-session) — **never** a raw sibling `git worktree add` (that skips the
`.worktreeinclude` seed and spawns the `.dev-knowledge-*` orphans). Lifecycle is *provision →
work on its own branch → integrate → teardown* (`worktree remove` + `prune` + `branch -d`,
then verify no leftovers).

**Integrate serially from the primary** — parallel sessions **commit-and-STOP; they never
self-merge.** A worktree→`main` merge is **git-structurally prevented** (a linked worktree
can't check out `main`, already held by the primary — the #200 finding), so integration always
funnels through the single primary checkout, where you `/ship` / `git merge --no-ff` **one
branch at a time**. The operator is the serial gate.

Canon: **PLAYBOOK §8** ("Parallel sessions & worktree discipline" — ask CC to pull it).

## Verification split (who checks what)

- **You verify the *artifact*.** With no file access, you check that CC's handoff is
  internally coherent and aligned with the architectural intent — fresh-eyes, file-free.
  Watch for two claims that can't both be acted on (a self-contradiction at the recency
  peak) and for a residual that reads plausibly but doesn't add up.
- **CC verifies *state fidelity*.** Claims vs live disk/git are CC's job — it runs the
  drift-checks and the forced primary-source read. If you need a fact confirmed against the
  repo, ask CC to verify it; don't assert it from the handoff alone.

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
  (`python scripts/audit.py ship-gate`) plus the freshness / `doc_claims` / BACKLOG legs, and
  the deterministic **ADR-85 Stop-gate** (next section). Don't design around them — design *with*.
- **Automation map.** Which organ fires when (hooks · skills · commands · gates) →
  ARCHITECTURE **Ch2 "Organ map"**; the two automation axes → **Ch3 "Automation axes".**

## Closing a session — definition of done

Plan with closure in mind from the start. The session-end Stop-gate (ADR-85) is
deterministic and **mechanically enforced** — the canon is `protocols/DEFINITION_OF_DONE.md`
(ask CC to pull it). The two load-bearing rules:

- **JOURNAL — hard.** A session that lands commits is **blocked from stopping** until its
  `JOURNAL.md` entry names ≥1 commit-SHA from this session. Not a nudge — a block.
- **BACKLOG — advisory (v1).** Landing commits without a structural-marker change in
  `BACKLOG.md` raises a nudge, not a block (it hardens later — ADR-85 R1).

The four other living docs (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING) are *update-when-
materially-affected*, not per-session-gated. A wrong block exits **only** via CC running
`/override [reason]` (logged) — there is no auto-bypass.

---

=== RESIDUAL.md ===

# Residual — 2026-07-21-dev-knowledge-architect — the part the repo does not already encode

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
**The CC session that generated this was cold; the SUPPLEMENT is not.** The generating session was
`/clear`ed and did no work of its own, so everything in **this file** is repo-derived from the
git/JOURNAL window since `2026-07-20-dev-knowledge-architect`, tagged `witnessed` where re-derived live
at generation and `recall` where read out of the record. **`SUPPLEMENT.md` was subsequently FILLED** by
the outgoing architect chat and its ANSWERS are folded into `PASTE_THIS.md` — so the §13(d) beat
**NARROWS** to *"anything changed since the supplement was written?"*, it does not fire full.

**Read the SUPPLEMENT before this file's §4.** The two were authored in that order and the supplement
**overrides §4 on sequencing** — the reconciliation is marked inline at §4 rather than by silently
rewriting it, so you can see what the repo said and what the operator ruled.

**Standing (dispositioned — expect them; they are not news).** `witnessed` — the same four register
families as the previous bundle, unchanged in composition: the `no_ff_merges` journal-wrap /
transcript-archive entries, the `undeclared_edges` HANDOFF_PROCESS dependents (`#241`), the `doc_rot`
backlog-accretion entries, and the `reconciled_versions` CONTRIBUTING-template entry (`#335`). Read
them at `ecosystem/disposition-register.yaml`; P7 re-derives which are live.

**Carried, NOT new, and still deliberately un-dispositioned — the one flag to actually look at.**
`VISION.md`'s `last_reviewed` cadence flag, owned by **[#368]**. It has now aged a further day by pure
calendar rollover; the file itself is still untouched. The previous bundle's reasoning stands verbatim
and should not be relitigated: re-stamping to reach a green number converts an honest signal into a
false one, and dispositioning it is the same move in a different costume. **The correct discharge is a
genuine end-to-end re-read of `VISION.md`** — and this window's vision audit (below) is a strong reason
to do that re-read *now*, with the audit's H1/H2/H6 critiques in hand, rather than as a stamping chore.

**A register-accuracy correction landed this window and supersedes the night audit's own guidance.**
`recall` (JOURNAL, `3234b4a0` lane) — the 2026-07-21 backlog audit's operator watch-out about which
`#id` closures would orphan a disposition is **wrong in both directions**: three ids it names orphan
nothing, it omits four `doc_rot` entries whose refs are open tickets and *would* orphan on close, and
its multiplicity for `#241` is understated. **The audit is immutable, so the correction lives only in
the JOURNAL entry for that lane** — a `/review-closures` pass that trusts the audit rather than the
JOURNAL will retire the wrong entries. Re-derive the live set from
`ecosystem/disposition-register.yaml`; do not read the numbers out of either document.

**Environmental, not a regression.** `handoff_probes` binds to the newest *committed* bundle, so once
this bundle lands it becomes the gate's target. Two known non-defects if you see them: a linked
worktree trips `deployed_methodology_version` on its directory name, and a cross-repo bundle can trip
sibling-resolution. Neither warrants a disposition entry.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the `2026-07-20-dev-knowledge-architect` bundle. Detail is in `JOURNAL.md` (newest-first,
five entries cover it) and `docs/audits/`; do not re-read it here.

**The one-line summary of the window: no ARC-5 wave opened.** What shipped was three read-only audit
lanes plus a hygiene pass. Hold that against `[E8]`'s own banner — *"AUDITS ARE OVER. ARC 5 IS
EXECUTION"* — and against §4 item 2 below, which is where it bites.

- **Night batch, three read-only lanes merged** (`eee8f532`, `94f910e3`, `1ef71834`) — vision/direction
  critique, code-quality audit, and backlog-trust audit, each an artifact in `docs/audits/` under the
  2026-07-21 `technical` class. **By contract all three filed proposals only** — zero ticket ids, zero
  backlog mutation. They are undischarged inputs, not shipped work.
- **Backlog hygiene arc** (the `worktree-cleanup-backlog` merge; sha withheld — it is adjacent to P3's
  live answer) — five tickets closed through the ADR-70 Tier-1 gate
  (`[#302]` `[#309]` `[#131]` `[#314]` `[#292]`), seven tickets repointed, four `#NNN` placeholders
  resolved to `[#234]`. Net task count fell. **Four audit claims were refuted on live verification**
  and the refutations live in that lane's JOURNAL entry, not in the immutable audit.
- **Registry lane** (the `worktree-cleanup-registry` merge) — the corp-monorepo `deployed-versions.yaml` entry annotated rather
  than bumped, and the night audit's A1 finding refuted: the corpus-version-vs-gate-rev divergence is
  deliberate and already modeled under **ADR-102**.
- **The direct-to-main incident is CLOSED** — the `[#373]`–`[#380]` id-range reservation that landed
  off-spine was relocated onto a proper `--no-ff` merge (`e3e79ada`). Core-invariant #5 holds on the
  spine again. Next-free id is unchanged by this window.
- **ARC-5 itself: no movement.** No wave opened, no decision ruled, `[#352]` clause (f) still
  unwitnessed, `[#371]` still unbuilt. `[E8]` in `BACKLOG.md` is unchanged from the previous bundle.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
> **RECONCILIATION — the SUPPLEMENT was filled AFTER this section and overrides it on sequencing.**
> §4 was authored from repo state alone; the supplement then arrived carrying the operator's intent.
> Where they disagree **the supplement wins**, and the disagreement is marked here rather than edited
> away, so the next session can see both. Per item:
>
> - **Item 1 — OVERRIDDEN on sequencing.** The supplement's mandate is **one delivery lane**
>   (`assets/` dissolution in ai-council, already granted 2026-07-19 — *execute, do not re-seek
>   permission*), **not** a bounded-pick message. It also effectively rules **R12** by rejecting the
>   narrowing option outright (*"goal is ALL rules, prioritised, never lowered"*), and it names a
>   **different owed-ruling set** — five one-sentence rulings on `#339`, `#327`, `#304`+`#305`,
>   `#262`+`#295`, `#215`. Treat *that* list as the live ask, not R1–R8.
> - **Item 2 — PARTIALLY ruled.** *"Consume the three audits, do not commission more"*; they are the
>   last input. **The clause-(d) accretion tension is NOT resolved** — that half of the item stands.
> - **Item 3 — AFFIRMED and given a disposition.** The polyrepo bet is confirmed as the sharpest
>   hole and routed to **its own session**, deliberately not mixed into the delivery work, with a
>   standing brake: *do not build more fleet machinery until it is ruled.*
> - **Items 4 and 5 — UNTOUCHED by the supplement; they stand.** Item 4 is independently corroborated:
>   the supplement's DO-NOT-REDO list carries the same `#320` refutation from the other direction.
> - **Item 6 — the buy-vs-build half is RULED.** The template engine is **rejected** (merge-replay
>   engines fail at this divergence profile; the hub is already regenerate-shaped), keeping only the
>   per-consumer version-pin scalar. So `[#371]`'s vehicle is no longer blocked on an open engine
>   question. The clause-(f) operator witness remains open.

### 1. The ten unruled decisions are STILL unruled — this is the second handoff to say so

`[E8]`'s decision table (R1, R1b, R2–R8, R12) is unchanged and **entirely unruled**. The previous
bundle named "a single bounded-pick message to the operator" as *the successor's first substantive
move*; that did not happen, and the window went to audits instead. **Repeating the same
recommendation a third time is not the move.** Either the bounded-pick message goes out at the top of
the next session, or the reason it keeps not happening is itself the thing to diagnose — because
several waves (W2 needs R1/R1b, W3's deletion path R3, W4's shape R2, W5's organ count R5) are
formally blocked on it and have been for two windows.

**R12 still leads, and item 3 below may have changed what R12 is choosing between.**

### 2. Three audit reports landed UNTRIAGED — and the triage is a decision, not a task

Roughly fourteen hundred lines across vision, code, and backlog critiques sit in `docs/audits/`,
each filed proposals-only by contract. The code audit carries an explicit triage test in its §0
(*location + falsifiable defect ⇒ ticket; opinion without a location ⇒ logged-reject*); the vision
audit attaches a falsification hook to every hole. **So the material is triage-ready and nothing is
blocking it except a decision about how much of it to accept.**

**The recursion is the actual problem, and it is worth stating plainly.** Discharging these reports
mints tickets. `[E8]`'s closure clause (d) requires backlog accretion **net ≤ 0** excluding tickets
minted by ARC-5's own waves — and audit-derived tickets are *not* wave-minted, so every one of them
counts against closure. **A full triage of these three reports could make clause (d) unreachable in a
single move.** The choices are real and none is obviously right: triage fully and re-baseline clause
(d); triage a bounded slice and log the rest as accepted-unfiled; or defer triage entirely until a
wave has actually shipped. **Pick one explicitly** — drifting into partial triage is the option that
looks like progress and satisfies nothing.

### 3. The vision audit asks one question that sits ABOVE ARC-5 and re-prices it

Its §6: *"if the three repos were folded into one tomorrow, how much of this system would still
deserve to exist — and is what remains the part I actually value?"* The claim is that a monorepo
**dissolves by construction** most of what the fleet machinery does — fleet parity, carriers and
deploy manifests, dependency parity, cross-repo pins, the collector, most of the parity register, and
the id-collision / worktree-contamination class — while what survives is the methodology lifecycle,
the census idea, the handoff harness, and the agent-coordination guards.

**Why this is a frontier item and not just a provocative read:** the audit's supporting observation is
that the **polyrepo shape was never actually decided** — no ADR argues it, and the 10–20 repo target
appears in scale requirements without a defence. If that is right, then **ARC-5's W2 (structure
equalization) is investment in exactly the layer the question puts at risk**, and R12 — "what is
ARC-5" — is downstream of a bet nobody has written down. This does not mean fold the repos; it means
the bet should be made explicit and defended (the audit's own estimate is an afternoon's ADR, with
two named falsification hooks) **before** W2 opens, not after.

### 4. Two sibling lanes of the SAME night batch contradict each other — and the batch has no organ that noticed

`witnessed`. The vision audit's **H7** ("the governance system audits naming conventions while three
repos sit unbacked on one disk") rests on three factual claims about consumer-repo backup posture.
**All three were independently refuted the same night by the backlog lane**, which verified them live
against the real repos; `[#320]` in `BACKLOG.md` now carries the corrected premise at `7c592062`. So
H7's evidence base is gone while H7 itself still reads as live in an **immutable** artifact.

Two things follow, and the second is the bigger one:

- **H7's architectural point may still stand on its own** — that the system has a *parity* register
  which ranks divergence but no *risk* register which ranks loss, and that drift detection was built
  before disaster recovery. That claim survives the refutation of its evidence. Salvage it
  deliberately or drop it deliberately; do not let it die by association with three wrong facts.
- **Nothing in the batch cross-checked the lanes against each other.** Each lane verified its own
  claims against live state and both did that job well — the contradiction is *between* them, and
  parallel read-only lanes have no shared adjudication step. This is a real gap in the batch method
  at n=1 witnessed, and it is the same failure shape `HANDOFF_PROCESS` §8 already names for the
  browser's artifact check: *two load-bearing claims that cannot both be acted on, where every
  per-claim check passes because each is checked against state and never against the other.*

### 5. The code audit independently rediscovered ARC-5's own disease model — in the code

Its closing structural observation across the top shortlist items: *"the recurring failure in this
codebase is not bad design and not missing tests; it is designed invariants with no organ asserting
them"* — a cycle detector that cannot see its own graph, a git-env scrub applied at one of nine
sites, a `Carrier` contract whose invariants no test asserts. **That is `[E8]`'s "recorded ≠ enforced
≠ legible" thesis, arrived at from the opposite direction by a lane that was auditing Python.**

The convergence is the finding. It says ARC-5's disease model generalizes beyond governance prose
into the enforcement machinery itself, which strengthens the arc's premise — and it supplies the
audit's own conclusion that the durable fix is usually **"make the existing gate real", not "add a
gate"**. That principle is a candidate for the arc's binding set, and it points at a cheap opening
move: the shortlist's item 1 is a check that is already registered, already wired, and simply
vacuous. Whether repairing existing organs counts as ARC-5 wave work or as separate hygiene is
**unruled**, and it interacts with clause (d) in item 2.

### 6. W1's tail is blocked on a decision that just got bigger

Unchanged from the previous bundle and still open: clause **(f)** — `[#352]`'s operator-witness of the
boundary decoration — and clause **(c)** — W1 has no archived Codex review artifact, and clause (c) is
itself a MUST-shaped rule with no mechanism, which is the arc's own disease on the arc's own board.

What changed: **`[#371]`** (the consumer editor-config write-through, declared at manifest v1.4.0 and
never built) has its vehicle decided by the pending buy-vs-build fleet-template ADR — and that ADR is
now entangled with the vision audit's **H4** (the buy-vs-build bet, as tabled, adopts the wrong tools
for this fleet's shape) **and** with item 3's monorepo question. A one-ticket write-through has become
the visible edge of a three-way decision. **The cheap escape is worth naming:** clause (f) needs the
operator to *see* the decoration in a consumer, and that witness does not require the fleet-template
ADR to be settled first.
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
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts,
> group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass criterion
> is **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-dev-knowledge-architect-0721`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **Windows note:** `audit.py checks` (P2) can crash mid-listing on a bare cp1252 PowerShell console
> (a non-ASCII glyph in a check docstring) — run with `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`); this
> is Python's stdout encoding, shell-independent, so git-bash does **not** avoid it. `ship-gate` (P7)
> can false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (§13c), not this read.

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-21-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-21-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-21-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ `scripts/validate_backlog.py` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one the fleet already shipped or superseded | `python scripts/validate_backlog.py` (schema + serialize-groups) then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d).** Then run P2–P10, each against
   **live state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P10 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state**. P10 grooms the
   whole open BACKLOG at boot (live / dead / awaiting-ruling per open `#id`). First check
   which branch is live (P3), then re-derive every load-bearing fact from the live primary source.

---

=== SUPPLEMENT.md ===

1. STRATEGIC INTENT

The next session must break the plan→execution deadlock. This fleet has spent 3-5 sessions
planning what it cannot ship: assets/ still sits in ai-council, granted-and-planned since
2026-07-19, never executed. That is the way-of-working defect to fix — not another audit, not
another intake, not another ADR. The methodology-management goal (structure, naming, config,
dependencies — not only LLM working-methodology) is sound and the theory is complete. What is
missing is DELIVERY. So the intent is: pick ONE narrow, fully-specified, operator-witnessed
equalization and DRIVE IT TO A DEPLOYED END-STATE the operator sees with his own eyes — assets/
dissolution in ai-council is the obvious first, because it is the smallest granted-but-unexecuted
item and it is the operator's own symbol of the execution failure. Merged is not done; deployed-
and-witnessed is done. If the next session ends with assets/ gone from ai-council and the operator
confirms it, the deadlock is broken and the pattern is proven repeatable. If it ends with another
plan, the way-of-working has failed again and THAT becomes the finding.

The deeper way-of-working question the vision audit forced open: WHY can this fleet plan but not
ship? The likely answer is that the meta-work (audits, intakes, ADRs, census) has been crowding
out the object-work (actually changing consumer repos). The next session should treat "did a
consumer repo visibly change" as its only success metric, and treat any new audit/intake/ADR as
a distraction from that unless it is the direct enabler of the one shipped change.

2. TENSIONS WEIGHED

- PLAN vs SHIP. Weighed hard, landed on SHIP. Every prior session produced excellent artifacts
  and zero consumer-visible change. The bias must invert: no new planning artifact unless it is
  the direct enabler of a shipped change this session.
- BUY vs BUILD (the template engine). Weighed via the vision audit and REVERSED the earlier
  buy-vs-build draft: Copier/cruft are merge-replay engines that fail at heavy declared
  divergence; the field moved to projen's REGENERATE-DON'T-MERGE model, and the hub IS ALREADY
  THAT (generated rosters, floor-hash replica, regen-and-diff gates). Landing: do NOT adopt a
  template engine. Take only Copier's one good idea — a per-consumer template-version scalar as
  the desired-state hash — and keep the existing regenerate machinery. This DELETES a large
  planned workstream rather than building it, which serves intent #1.
- SIEM FRAME vs STATE-DIFF. Landed on state-diff. The fleet is nightly cooperative state-diff,
  not real-time adversarial event-stream. Keep the requirements (they're state-shaped already),
  drop the SIEM frame and its ingestion-machinery pull.
- SCOPE of the first ship: whole-fleet equalization vs one consumer, one surface. Landed on ONE
  (ai-council, assets/). Proving the delivery loop once beats planning the whole matrix again.
- NARROW vs BROAD id-allocation / session-coordination fix. The night proved (n=3) the repo holds
  serialization by discipline not machinery. Weighed building the organ now vs parking it. Landed:
  PARK it as a named ticket, do not let it become the next session's object-work — it is
  infrastructure, and infrastructure is how this fleet has avoided shipping. Fix it AFTER the
  delivery loop is proven once.

3. CONSIDERED + REJECTED (do not relitigate)

- Template engine adoption (Copier/cruft as the fleet engine) — REJECTED by the vision audit on
  evidence: merge-replay fails at this divergence profile; the hub is already regenerate-shaped.
  Keep only the version-pin scalar. Do not re-open "should we adopt Copier".
- Renovate for dependency parity — REJECTED: it needs a hosted platform; on local-disk repos it's
  detect-only. #332's central-constraints-file + per-repo-sync is already the proven pattern.
- SIEM as the architecture frame — REJECTED as the wrong mental model. Do not build event-pipeline
  ingestion.
- Narrowing the ARC-5 rule-fix goal to a bounded slice — REJECTED earlier by the operator (goal is
  ALL rules, prioritised, never lowered). Still stands.
- Auto-deleting from the backlog in a night batch — REJECTED; operator is the strike gate via
  /review-closures. Still stands.
- Another round of audits as the next session's work — REJECTED implicitly by intent #1. AUDITS ARE
  OVER (ARC-5's own banner, twice-violated). The three night audits are the last input; the next
  session consumes them, it does not commission more.
- Hand-close / hand-edit tickets outside the gate to force closures — REJECTED; the cleanup session
  held the line (closure set = 5 not 6 because #215 is gate-unreachable; declined rather than
  hand-forced).

4. OPEN QUESTIONS (unresolved / deliberately deferred)

- FIVE OWED RULINGS (one sentence each, needed before their tickets can close): #339 demotion
  (A2 byte-identical helper leg unbuilt, no owner); #327 demotion (clauses appear met but corp's
  own markers contradict — wording done + markers stale, or genuinely live?); #304+#305 (doc pass
  closes #304; #305 needs a code clause blocked by PreflightError — re-scope?); #262+#295 (policy
  ruling: abandon generator-management for flat layouts?); #215 (permanent gate-invisibility —
  text edit to make it gate-visible, or accept a manual disposition path?).
- THE POLYREPO BET, never decided (vision audit's sharpest hole): zero ADRs weigh monorepo vs
  polyrepo; the 10-20-repo target is asserted, never argued. The only coherent n=1 justification
  is that the workforce is AGENT SESSIONS. This is an afternoon's ADR that re-prices every other
  bet — deferred to its OWN awake session, NOT mixed into the delivery work. Do not build more
  fleet machinery until this is ruled, or you risk building an elegant solution to a problem a
  monorepo would dissolve.
- LITERAL hub-push into consumers (vs the ADR-28 read-only + hub-reports-PRs model) — an open
  ADR-28-amendment question, deferred.
- The session-coordination organ (live-session detection + fleet-scoped id-allocation) — the
  night's proven infrastructure gap; parked as a ticket, deferred until the delivery loop ships
  once.

5. DECOMPOSITION RATIONALE (what NOT to redo)

The task-graph shape is deliberately INVERTED from prior sessions: object-work first, meta-work
only as its enabler. The next session is ONE delivery lane (assets/ dissolution in ai-council to a
witnessed end-state), not a matrix of planning artifacts.

Do NOT redo / re-decide:
- The three night audits are DONE and merged — consume them, do not commission more.
- The cleanup is DONE — backlog is 5 tickets lighter and TRUE; the registry is annotated; four
  audit refutations are recorded (do not resurrect: #361 line-drift is false, #320 was wrong on
  three counts, #244 #130 is a delete-not-swap, #314 companion edit is premature). The audit's
  watch-out #1 orphan list is WRONG both ways (flags #210/#146/#277 which orphan nothing; misses
  #262/#278/#332/#344 which do; #241 is ×6) — use the registry lane's JOURNAL correction, NOT the
  audit, on the next /review-closures.
- The buy-vs-build and SIEM decisions are made (reject the engine, drop the frame) — do not
  re-derive them.
- assets/ dissolution is already GRANTED (operator GO 2026-07-19: relocate to config/ first,
  verify, then delete) — do not re-seek permission, EXECUTE it.
- The equalization scope enumeration exists (living-docs, folder layout, naming, .vscode, .claude
  surface, Python parity) — do not re-enumerate; pull ONE row and ship it.

6. OFF-REPO CONTEXT

- OPERATOR'S CORE FRUSTRATION, stated explicitly: this is the 3rd-5th session where everything is
  planned, theorised, prepared — and NOTHING ships. assets/ still sits in ai-council as the symbol
  of it. He expects the theory, the audits, the intakes, the ADRs to FINALLY be implemented
  intelligently. The next session is judged on delivery, not planning.
- The methodology-management scope is broad by operator ruling: not only LLM working-methodology
  but naming, file/folder structure, Python engineering standards, dependency parity — the
  architect owns all of it.
- The vision audit (Fable, cold-boot) is the operator's requested fresh-eyes critique of the whole
  direction — he takes it seriously and wants its theses acted on in their own session, not buried.
- Push is standing-permission; the operator is the merge/strike gate; he judges when a session ends.
- The two intake drafts (buy-vs-build, nightly-audit-standard) exist as downloadable files, NOT yet
  ingested into docs/intake/. Given the reject-the-engine ruling, the buy-vs-build intake needs
  REWRITING before ingest (it argued FOR a pivot the vision audit reversed) — flag, do not ingest
  as-is.
