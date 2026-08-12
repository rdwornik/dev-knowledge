=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-12-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-12-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Adjudicate the two night DRAFTS — that is this session's first order of business, not background reading.** `night-1` (truth audit + handoff numbers) and `night-2` (lessons, governance, strategy) are merged to `main` and ratify nothing; their findings are proposals until this seat rules on them. Then settle the **one OPEN ruling carried out of the window** — the I-D6 working-set reading, whose two definitions differ by 11 and which gates the consolidation-intake filing. Work sits in **[E2] Enforced governance** (the ADR-101 tree seal and its new Rule C leg) and **[E1] Handoff continuity**; the live row set is `BACKLOG.md`.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->adjudication output — rulings into `protocols/STANDING_RULINGS.md`, ADRs, intake status flips, and BACKLOG rows. **Not** a code lane: the closing arc left the tree green and the two night artifacts are immutable audits, so nothing here is edited to make a finding go away<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the whole inbound payload is undecided — two unadjudicated DRAFTS, an open ruling with two irreconcilable readings, and eight RECORDED-ONLY rulings that never reached the tree. Every one is a *what should be true* question, which is architect scope; sending it to an execution seat would ask a lane to decide what it was dispatched to implement<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/batch-4-packet-and-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-08-12-dev-knowledge-architect — the part the repo does not already encode

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
**STANDING / dispositioned — none of these is new this window** (dispositions live in
`ecosystem/disposition-register.yaml`; re-derive every value via P4/P6/P7/P9):

- The `undeclared_edges` prose-edge family (ADR-88 FC2) — owned by `[#241]`, whose Done-when was
  deliberately re-phrased **cardinality-free** so this set can grow without re-breaking the row.
- `no_ff_merges` — three legacy June non-merge spine commits, grandfathered. **Never rewrite them.**
- `doc_rot` history-accretion on the large rows (`[#511]` `[#510]` `[#514]` `[#522]` `[#505]`
  `[#322]`) — the condense route is `[#426]`/grooming territory, not an in-window fix.
- `reconciled_versions` — one malformed template edge, pre-existing.
- `preflight_backlog_ids` — advisory per the `[#483]` R3 ruling.
- `review_artifact_coverage` — advisory per the `[#480]` P3 ruling.

**MOVED THIS WINDOW, and the direction matters:**

- **`doc_rot` file-budget on `CLAUDE.md` grew, by this arc's own hand.** The §12 v2.58 entry pushed
  it further past its self-declared budget. It is a WARN and it is *earned* — but the next
  condense pass on that file is now overdue rather than optional.
- **`git_backlog_drift` on `[#505]` was a FALSE POSITIVE and has aged out of the detector window.**
  Recorded so it is not re-flagged: the bracketed id in `25ff8ec37` is a *reference*, and that
  commit's own body says "3 rows filed, 0 closed".

**NEW THIS WINDOW — one, and it is a test, not a flag:** the single standing suite RED is the
`[#426]` class (a live-backlog routine-row count). It is a retrofit debt, not a regression.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
| id / artifact | Where |
|---|---|
| `[#514]` leg 3 + `[#510]` partial | W1, merge `0136cec6` — **both rows remain OPEN** |
| `[#270]` **closed** | W2, merge `c7f4fd92`; close `679d8eca` |
| `[#132]` **closed** — organ index ships | W5, merge `e624a172`; close `83a869e6` |
| `[#521]` **born and closed** | W-521, merge `aafe3c8e` |
| `[#522]` born · `[#117]` un-deferred | `3aaf5140` · `64ea92bb` |
| ADR-111 **Accepted**; intakes #28–#32 ratified as ONE act | `3aaf5140` / merge `3b711e87` |
| Absorb ×7 executed, retention mechanism killed | 7 merges under authorization `710dabfa` |
| **Batch 4 CLOSED** — the end-of-batch packet | `docs/audits/2026-08-11-technical-batch-4-packet.md` |
| **Organ index relocated** `docs/ORGAN-INDEX.md` → `ecosystem/organ-index.md` + **Rule C** guard | operator ruling A; register `STANDING_RULINGS` **K-1** |
| `gen_audit_index` tracked-files fix + terra findings consumed | artifact `docs/audits/2026-08-12-codex-closing-arc-organ-index-guard.md` |
| PLAYBOOK Ch8 dispatch-surface correction | the alias claim → the PATH-command reality |
| Night-1 + night-2 audits merged **as DRAFTS** | `docs/audits/2026-08-12-*` — **unadjudicated** |

Detail is in `JOURNAL.md` 2026-08-12 (a)–(c); this is the map, not the recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The payload. Seven decisions, ordered by what blocks what.**

1. **ADJUDICATE THE TWO NIGHT DRAFTS — first, before planning anything.** Both are merged and both
   ratify nothing. Night-1 is a truth audit whose verdicts (44 ruling lines; 28 EXECUTED, **8
   RECORDED-ONLY**, 1 UNOWNED-AFTER-DROP) are *claims about this corpus's own honesty*, and they
   are unrefuted rather than accepted. Night-2's Parts C/D/E are unread by any deciding seat.
   Leaving them merged-but-unruled is the worst of both states: they read as landed and bind
   nothing.

2. **THE I-D6 WORKING-SET READING — open, and it gates a filing.** I-D6 defines the working set as
   SEED/DRAFT/READY; the BRIEF one day later applies DRAFT-only. Measured at the cut, the two
   readings differ by **11** (definition-reading 14 against a ceiling of 6; applied reading 3).
   These are not reconcilable by evidence — they are two different rules, and the choice is the
   operator's. *A ceiling that cannot be evaluated is not a ceiling* is I-D6's own stated reason
   for the reading it chose. Until this is settled, any consolidation intake filed against the
   ceiling is filed against an undefined denominator.

3. **THE CONSOLIDATION INTAKE IS MIS-SCOPED AS DRAFTED, and filing it as-is double-births.**
   Night-1 verified the brief's three GAPs negatively: **GAP-1 is real** (no row or intake proposes
   a commit-time architecture-impact gate; `[#169]` is adjacent and should be named as a
   kill-candidate or explicitly disclaimed). **GAP-2 is partly false** — `[#420]` owns the
   archive-folder leg and carries a live *"do NOT touch `docs/archive/`"* order, so a doc-moves
   proposal collides with it on day one. **GAP-3 is not a gap at all** — it is W-9(a), a work-item
   inside an ACCEPTED intake, with a recorded `AGENTS.md` name-collision hazard. The honest ask is
   *"W-9(a) is stalled and its collision is unresolved"*, which is a different thing to file.

4. **EIGHT RULINGS ARE RECORDED-ONLY, and two of them are quietly load-bearing.** 3b-4 (the
   citation convention) and 3b-5 (inherited-vs-measured) were both adopted and neither landed
   anywhere. The window then produced *exactly* the defects they exist to prevent: a `win-tooling`
   SHA presented as a hub SHA, twice, and an "A5" label with no resolvable referent. This arc
   applied 3b-4 at the sites it edited, which is not the same as landing it — **its ruled home in
   PLAYBOOK still has not received it.** The general question is sharper than either instance: a
   register that accumulates unlanded rulings is a backlog wearing a register's clothes.

5. **THE SEEDED-DEFECT CORPUS IS THE BLOCKING ARTIFACT, and a dated re-check is about to measure
   nothing.** The spec is extracted and the amendment DRAFT is written; **the corpus does not
   exist**. `[#491]` (Gemini) and `[#492]` (Grok) are both gated behind it, and `[#492]`'s dated
   re-check is **2026-08-17**. If the corpus is not built by then, that re-check produces a
   verdict with no instrument behind it — which is worse than a missed date.

6. **THE ARCHITECTURE COMMISSION HAS NO VEHICLE.** I-D item 12 commissioned an ARCHITECTURE
   re-read/fix as a batch-4 lane. That lane was W6; W6 was dropped at manifest amendment A-1 and
   carries **no row id**. The 16-claim fix landed separately, but the commissioned re-read arc and
   the G-7 soft-observations scope now have no lane, no row, and no owner. *(Partial evidence
   against it: this arc's own end-to-end re-read of `ARCHITECTURE.md` found three further defects —
   which is an argument that the commission was correctly scoped, not that it is discharged.)*

7. **THE MANIFEST AMENDMENT MARKER IS OWED.** Batch 4's manifest states at `:398` that `[#514]` and
   `[#510]` closed. Both measure `status: open`. `docs/audits/` is immutable, so the route is an
   appended A-4 marker — not an edit, and not silence. The packet records the truth; the manifest
   still carries the false claim.

**One process observation, offered as input rather than a proposal:** both night lanes ran against
the **primary working checkout** instead of one worktree per lane, and it produced a real near-miss
(a commit re-targeted onto the other lane's branch mid-`add`; repaired non-destructively, nothing
lost). `git add` then `git commit` is **not** atomic against a concurrent branch switch in a shared
tree. The mechanical fix is one worktree per lane or a branch-identity assertion immediately before
commit; whether that becomes a rule is this seat's call.
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
> **Branch note.** This bundle was generated on branch `docs/batch-4-packet-and-handoff`. This line names only *which*
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-12-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-12-dev-knowledge-architect/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-12-dev-knowledge-architect/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-12-dev-knowledge-architect/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-12-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-12-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-12-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

# SUPPLEMENT — ANSWERS from the outgoing architect (seat 27, browser) · 2026-08-12
Paste everything below into the ANSWERS region of SUPPLEMENT.md, then tell CC `supplement filled`.

**1. Strategic intent.** The next session's way-of-working goal is a single flip: **adjudicate-then-execute**. This window (and the two before it) produced a planning SURPLUS — two night reports, a ratification batch, a brief, three instruments answered — and the surplus is now the risk: every unadjudicated draft is a page someone will re-derive. The next session converts the surplus into law in ONE morning act (the adjudication hour), and then the seat's job for the rest of the week is **execution only**: no new planning artifacts, no new instruments, no new intakes beyond the one re-scoped filing below, until batch-4 truly closes. The operator has said this in his own words; treat it as the window's contract.

**2. Tensions weighed.** (a) Measure-first vs the operator's tempo — held in governance (ruff behind hotspots, providers behind the corpus, refactors behind §D) and broken once by drift in tooling (the dispatch saga: four tempo-fixes before the mechanism class was questioned); the repair was mechanization, not apology (`fb52bf6`, `-Check`). (b) Research consumption vs the birth cap — resolved amendment-over-birth (`[#513]`), ledger held at 2+1. (c) Honest-red vs green optics — chosen every time it mattered: W1/W2 refused to close rows over blank legs; the untestable count is reported as NOT fallen; the §B dashboard shipped at 0🟢. (d) Sequential vs parallel — settled as sequential-by-default with matrix-proven, operator-approved pairs; the matrix is the law, not caution.

**3. Considered + rejected (do not relitigate).** Building a prompt-distiller (backlog verdict PARTIALLY — every axis owned, `[#412]` lead; library-first says measure CC-native agents/skills first) · Fable as the architect seat (Ch8 routing; Fable stays the adversarial reserve) · "merge W4/W6 before W1" (rejected for ids-before-contract + W6 drop) · `protocols/` as the organ-index home (ruling A: `ecosystem/`, generated-artifact pattern; register K-1) · immediate ruff-family adoption (behind churn×complexity hotspots, unrun) · graph-DB/server storage (dead list) · retiring Codex before Grok passes the corpus (admit-then-retire) · backlog bankruptcy (per-row argued removal instead).

**4. Open questions (deliberate, each with its gate).** (i) **I-D6 working-set reading** — operator's word; gates the intake filing. (ii) **The consolidation intake's FINAL scope** — night-1 falsified the draft scoping: GAP-2's archive leg is OWNED by `[#420]` under a live do-not-touch order, GAP-3 is W-9(a) inside an ACCEPTED intake with a recorded AGENTS.md collision hazard; the filing therefore covers **GAP-1 (architecture-freshness mechanism) + the ontology/graph attach + ONLY the genuinely unowned legs of taxonomy/portability, cross-referencing [#420] and W-9(a) as owners instead of re-scoping them**. (iii) The strict live-id `depends-on` predicate (parked; interim strip-law covers operations). (iv) §B clauses 1/5 falsifiability-from-tree (22% of the finish line). (v) The OneDrive read-only rule (operator TAK/NIE pending). (vi) Bake-off timing vs the corpus-reconciliation gate (11/12 verdicts pinned to `extend-select = []`).

**5. Decomposition rationale — what must NOT be redone.** Batch-4's shape stands: W1/W2/W5/W-521 merged, W3 carried because it shared freshness-gated CLAUDE.md with live W1 (unblocked at `0136cec6`), W4 carried because a lane without a row id is the defect W1 exists to prevent (G-2: ids-before-contract), W6 dropped (cap + ARCHITECTURE collision + no id). The next-session order 1–8 is gate-derived, not preference: adjudication unlocks removals, lessons and I-D6 at once; W4 outranks W3 because repairing 72 existing rows beats protecting future ones on the under-100 axis; everything later sits behind a named gate (intake←I-D6; bake-offs←corpus reconciliation; style←hotspots; telemetry←two windows of data). Do NOT re-derive: the disjointness matrix, the census classes (95/72/23/8), the G-register resolutions, or the night reports' evidence — adjudicate them, don't re-measure them.

**6. Off-repo context.** The operator's declared week-goal: **execution only** — calibrate expectations: the adjudication hour is the one non-execution act and it is the unlock, not a detour. Transport: the browser paste channel degraded mid-window; the standing practice is FILE UPLOAD for anything longer than a line. Tooling: `dispatch <contract>.md` works in every shell (PATH command, `-Check`-guarded); VS Code is healthy (root cause pre-dated us, removed); the machine owes nothing. The three instrument answers (execution challenge, consumption challenge, interrogation) are committed or riding the closing addendum — they are the window's self-account and the fastest way for the incoming seat to calibrate against reality. Calendar: `[#492]` Grok re-check **2026-08-17 (this week)** · intake #10 disposition rides the adjudication · `[#322]`/`[#360]` dated reviews 2026-09-09.

**7. Ratified-in-chat, not yet in repo.** (a) The **OneDrive read rule** — proposed "read-only under declared diagnostic need, disclosed in-report; writes absolutely denied"; PENDING the operator's word → home: STANDING_RULINGS line when ruled. (b) The operator's **execution-only-week intent** → home: this supplement (now recorded). (c) The **paste-completeness / file-upload transport practice** — browser-seat working rule, no repo home needed (not doctrine, a channel fact). Otherwise: none — every other in-chat ruling of this window was landed with a locator (I-D3, I-D8, AM-5, K-1, strip-law, anchor-law, re-ruling on pairs) or is listed in (4) as deliberately open.

---

## THE PLAN (short-term → session → week → horizon)

**SESSION 1 of the new window (the adjudication hour, then dispatch).**
1. Boot per bundle (Opus; Fable held adversarial). Read: night-1 report · night-2 report · BRIEF · this supplement. No re-derivation.
2. **Operator adjudication batch (one picker set, ≤30 min):** I-D6 reading (rec: DRAFT+READY) · lessons table TAK/NIE per line (19 items, ratchet-clean drafts ready) · removal sheet KEEP/RETIRE/FOLD per row + intake #10 · intake→ADR promotions (per night-2's fork-test arguments) · the re-scoped consolidation-intake filing decision (per §4.ii above) · OneDrive rule.
3. **Execute the adjudication's mechanical tail the same arc:** removals per TAK, lessons→LESSONS/PLAYBOOK, promotion drafts opened, register lines.
4. **Dispatch W3** (`lane-c-513-landing-predicate`, skeleton ready in night-2 E5) — the organ that ends the ruled-but-unlanded class.
5. **Mini-GO: birth the W4 row** (conversion campaign, mechanical Done-when over the census P1/P2 drafts) → dispatch W4 wave 1.
Mechanical success condition (D6 of the interrogation): after step 3, the register holds a disposition for 100% of both night drafts' items — grep-countable, zero lines without a verse.

**THE WEEK (execution only).** W3 merge → W4 waves (the single biggest under-100 lever: 72 rows) → removal executions land → `[#492]` re-check on 2026-08-17 via the corpus (reconciliation first — the pin gate) → batch-4 CLOSES with its packet (checklist items 1+3 finally checkable) → if capacity remains: ARCHITECTURE Ch2/Ch6 organ rows + the `[#514]`/`[#510]` remaining legs. No new intakes, no new instruments, no new planning artifacts this week.

**THE HORIZON (windows 3–8).** Under-100 in ~2–4 execution windows (conditional: W4 fires, net ≤ 0 holds); zero-untestable in ~3–5 — the constraint that moves the finish line most. The consolidation intake (as re-scoped) lands the architecture-freshness mechanism and the ontology recon. Provider table settled by MEASUREMENT: Gemini `[#491]` and Grok `[#492]` on the corpus, Codex sunsets only after a pass, Copilot as the third probe. Code-style stack enters after the hotspot baseline; telemetry reads after two windows of data. **Satellite re-entry:** the feature/satellite quota bucket exists and the fleet gauge (`[#270]`) now watches the satellites — schedule the first satellite-serving lane within two windows so the hub's outputs start paying rent outside the hub (this is the one soft blind spot the plans kept deferring). Monorepo: parked by the operator's own consolidate-first sentence until §B v1.0.

**Blind-spot check, honestly:** (1) the consolidation-intake mis-scope — CAUGHT by night-1, corrected above; (2) satellite consumption — named above with a two-window deadline; (3) the calendar items are in §6; beyond these, no unplanned known work remains: every theme from the operator's strategy dump, the six research commissions, and three instruments maps to a row, an intake, a register line, or a dated gate. The planning is DONE. The week is for the plan.

---

=== END OF PASTE — 5 sections · 54650 bytes ===
