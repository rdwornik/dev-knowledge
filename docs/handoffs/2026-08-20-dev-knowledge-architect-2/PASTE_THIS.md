=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-20-dev-knowledge-architect-2` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-20-dev-knowledge-architect-2 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Sequence and close, rather than rule: the 2026-08-19/20 unruled queue is **drained** — its ten rulings are `protocols/STANDING_RULINGS.md` **section Q** and their verdicts reached the rows — and what the window handed forward instead is **eight new rows with no dispatch plan**, against a closing bar (`[#555]`, net-negative) that the same arc moved measurably closer to its limit. The standing authority is **`[E7] Tooling & evaluation`**, which owns `[#539]` and `[#563]` under `[S18]` and the closing campaign `[#555]` under `[S20]`; the batch shape stays ADR-110 (one plan → N file-disjoint frozen lanes → one serial integrator). Suggested order, with the reasoning in `RESIDUAL.md` §4 rather than here: **rule the `doc_rot` row-length ceiling** (three windows deferred, and every birth makes it worse), **decide `[#539]`'s dispatch** (a dated Q2/Q10 deferral is silently riding on it), **rule what the C1 refusal items measure** before `[#562]` re-runs anything, then **choose between the closing batch `[#555]` and the telemetry chain `[#565]` → `[#529]`/`[#530]`**, and settle whether the seven `DRAFT` intakes finally get their own dispatched lane. Task-state is `BACKLOG.md` — the spec; read it there, never re-narrated here.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->Planning and governance surfaces only: `tasks/` plus `gen_task_tree.py --emit-source` for any row change (**never** `BACKLOG.md` by hand), `docs/decisions/ADR-*.md` for ratifications, `docs/intake/*` status transitions **with both** intake generators (only one of them is hook-gated), `protocols/*.md` for codification and promotion debt, `JOURNAL.md`, and `docs/audits/` for anything this seat produces. **Implementation does not happen in this tree** — `[#539]`, `[#554]`, the `[#565]`/`[#529]`/`[#530]` telemetry chain and the `[#563]`/`[#566]` generator legs dispatch to file-disjoint lane worktrees, because this seat's writes and a lane's writes must not share a tree (section Q's **Q2**: the primary checkout is seat-arc-only).<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->**architect**, because the deliverable is a decision set — which ceiling moves, which lane dispatches, what the refusal items measure, and whether closing or implementation runs first — rather than the advance of one named backlog row, which is what execution mode is profiled for. So the residual is scoped to the planning *why* plus the whole `BACKLOG.md`, and the browser is served the generative/decompositional posture.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-08-20-architect-2`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-08-20-dev-knowledge-architect-2 — the part the repo does not already encode

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

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**Nothing here is a value — P4/P6/P7/P9 hold the live answers.** What follows is which *classes* are standing versus new, and why, so the incoming architect can tell a carried WARN from a fresh one without waiting for the block.

- **Standing, and deliberately GROWN this window: the `doc_rot` `backlog-row-length` class.** The eight births released by the 2026-08-20 act-group-2 arc landed with bodies over the ceiling, as drafted rather than trimmed, on the precedent `[#559]`/`[#561]` set — the arc disclosed this in `JOURNAL.md` 2026-08-20 (h) rather than letting a reader discover it. This is **not new drift**: it is the unruled ceiling question carried in §4 below, now larger by construction. Treat any row-length finding P7 reports as belonging to that open decision, not to a fresh defect.
- **Standing and dispositioned elsewhere:** the carried classes live in `ecosystem/disposition-register.yaml`; the register is the only place a suppression is legitimate, and the standing stance — `doc_rot` greens by **fixes**, never by dispositions — is why the row-length class was never dispositioned away. Read the register before dispositioning anything P7 surfaces.
- **The silent-rule ratchet was measured, not assumed, at every `protocols/` edit of the window** (before/after each `STANDING_RULINGS.md` write), and the arc recorded that section Q added no `must|shall|never` debt — see `JOURNAL.md` 2026-08-20 (g)/(h). Section Q is phrased declaratively on purpose, per that file's own Editing note; the one softened line (Q4) is disclosed in the JOURNAL rather than left for a reader to notice. P-class re-derivation still binds — the record here is provenance, not a substitute.
- **New-this-window drift, if any, is P7's answer alone.** Both read-only drift-checks (`validate_doc_claims`, `validate_git_backlog`) were exercised at generation time and this bundle states neither result. The load-bearing instruction is the ordinary one: **any FAIL in the evidence block blocks onboarding**, and a WARN whose class is not named above should be read as new until the register says otherwise.
- **One instrument is known-untrustworthy and it gates another** — `review_artifact_coverage` (carried by `[#560]`) reads only the first branch/HEAD triple per file plus one title literal, so a genuine review can be invisible to it. If the block shows a coverage-class finding, weigh it against that known reader defect before treating it as a missing review.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->Terse map only — `JOURNAL.md` 2026-08-20 (f)/(g)/(h) and `git log` carry the detail; this is where to look, not what happened.

- **The window's ten rulings are now in-repo** — `protocols/STANDING_RULINGS.md` **section Q**, one line per ruling, landed by the transcription arc whose contract of record is `docs/audits/2026-08-20-technical-transcription-seat-contract.md` (ADR-110, committed first). Q1 index-freshness on lane material · Q2 primary-checkout-is-seat-arc-only · Q3 harvest order · Q4 cloud-lane hygiene · Q5 receipt gate · Q6 contract-as-file-without-exception · Q7–Q9 the acceptance instrument · Q10 PAUSE-on-refuted-premise.
- **The anti-orphan sweep (P-2) discharged in the register itself**, not only in the arc's packet: 18 of 20 ratifications carried by a live row; **Q2 and Q10 `disposition: deferred`, trigger dated 2026-09-19** — see §4 item 3, because that date is a decision, not an outcome.
- **Verdicts reached the rows** — `[#491]`, `[#561]`, `[#539]` annotated (`20a51638`); **eight births released** `[#562]`–`[#569]` (`b6e2044b`) against the arc's re-measured ledger.
- **The acceptance window's systemic finding** is the newest `LESSONS.md` entry (role discipline is a property of *routing*, not of a model); **`ERRATUM E1`** is appended — not edited — to `docs/audits/2026-08-20-technical-codespaces-audit.md`, withdrawing the workstation `ruff` figure and the ratio built on it while leaving the accepted LEAN v2 intact.
- **Substrate was ruled** — `docs/audits/2026-08-20-technical-codespaces-audit.md` carries the accepted RULING; `[#567]` is the carrier lane it released.
- **The PLAYBOOK gap is measured** — `docs/audits/2026-08-20-technical-playbook-status.md`, a 14-row G1–G14 table that independently reads five of the section-Q rulings as ABSENT from `protocols/PLAYBOOK.md` today. Register and census are cross-cited so they cannot drift apart.
- **Two model-acceptance records, neither an admission** — Gemini 3.7 Flash (slots 1 and 2) and Grok 4.6, all under `docs/audits/2026-08-20-technical-*-ab-*`; slot 1 landed renamed to clear slot 2's paths, with one locator repointed and the as-issued contract left untouched.
- **The ruled `--parallel` flip** of the `audit-health` pre-commit entry merged (`54633041`).<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->**Read this first: the shape of the carry INVERTED today.** The morning bundle handed over an *unruled queue* — ten assembled asks nobody had decided. That queue is drained: the rulings exist as `STANDING_RULINGS.md` section Q and their verdicts reached the rows. What replaced it is the opposite problem. The window ended with **eight new rows, no dispatch plan, and a closing bar that the same arc moved closer to its limit.** The next session's scarce resource is not judgement; it is *throughput and closure*. Sequence and close — do not re-rule section Q.

**1. The closing bar is now the binding constraint, and it binds before the next filing — not after.** `[#555]` sets the stated goal as **net-negative** (closures strictly greater than births) and the house rule per `d85490d0` is *banked > window births*. Act-group 2 released eight births against the banked ledger it re-measured from `tasks/` rather than carrying from its contract, and recorded the resulting headroom in `JOURNAL.md` 2026-08-20 (h). **Re-derive that ledger before filing anything** — the rule halts a release the moment it stops holding, and the next window opens much closer to that line than the last one did. The decision this forces: does the next window *dispatch implementation* (which files nothing and closes little) or *run the closing batch* `[#555]` first — and note `[#555]`'s own first act is naming ONE denominator predicate, because three counts of this backlog are still in circulation and until one is chosen **no net-negative claim is falsifiable at all**.

**2. The `doc_rot` row-length ceiling is now a decision the repo is actively voting against.** The standing stance is that `doc_rot` greens by fixes and never by dispositions; the practice is that every window's births land over the ceiling on precedent, and this window added eight more. Three exits, none chosen: **move the ceiling** with a recorded basis (and then the disposition backlog for that class retires); **decompose long rows** (and the eight born-long rows are the first candidates, which makes it a closing-campaign leg rather than a separate arc); or **keep the tension and stop calling it drift** (worst option — it teaches that a named class is optional). This has now been carried across three consecutive windows. It is cheap to rule and it gets more expensive to fix every time it is deferred.

**3. `[#539]` is the load-bearing lane, it is undispatched, and a dated deferral is quietly riding on it.** It carries five of the ten section-Q rulings to their declared durable home (PLAYBOOK Ch8 — the census maps them G10/G9/G14/G3/G13 and reads every one as ABSENT today), and its `--check` leg arms two organs currently wired into no gate, with the two branch-grammar incidents in `LESSONS.md` 2026-08-19 as its evidence base. **Q2 and Q10's deferral triggers on that lane landing *or* 2026-09-19, whichever comes first** — so if `[#539]` does not get dispatched, the deferral does not fail loudly, it just ages. Either dispatch it next window or re-date the deferral with a stated reason; letting the date arrive undecided is the failure mode the anti-orphan sweep exists to prevent.

**4. The open question about model admission is the INSTRUMENT, not the candidates.** Two candidates were assessed and neither admitted; Q9 fixes ADMIT as G1 ∧ G2 ∧ G3 on the seeded-defect pack and Q7 makes Φ trajectory-inclusive, so the *bar* is settled. What is not settled is what the C1 pack's two refusal items measure: the newest `LESSONS.md` entry shows the **incumbent scored 0/2 on the same items**, which means those items may be measuring *dispatch quality* rather than model role-discipline. Three readings are available — keep them as admission gates (and accept that a gate the incumbent fails is a strange gate), demote them to routing diagnostics scored separately, or leave the bar untouched and record "none pass yet" as the result it is. `[#562]`'s guarded rerun is filed, but **its shape depends on this call**, so ruling it first is cheaper than re-running the pack twice.

**5. Decided-unfiled is the repeat failure mode, and it survived another window untouched.** **Seven intakes sit `DRAFT`**; the prior window's plan to ratify did not execute, and this window's transcription arc explicitly excluded intake status transitions — correctly, since that was outside its contract, which is exactly the point: **ratification keeps riding a wrap, and wraps keep getting consumed by integration.** The open decision is unchanged from the morning bundle and is now evidenced twice: does ratification get **its own dispatched lane with its own contract**, the way implementation does? Note the operational trap if it does — an intake status change needs **both** intake generators, and the `intake-index-freshness` gate only covers one of them.

**6. The telemetry chain is sequenced but unowned.** `[#565]` rules that `run_id` lands **before** the read-path lane, and the reasoning is sound while `[#529]` is still library-only with zero call sites. Ruling the sequence did not choose the runner or the window. Still open beneath it: `[#529]`'s four legs (call-site wiring · `.gitignore` the WAL store before the first live emit dirties `git status` · the `structlog` dependency decision · the `_REPO_ROOT` resolution that points at the *worktree* under a linked checkout), and `[#530]`'s two latent races (the ABA in `release`, the `rev-parse` conflation). All are cheap now and none is cheap after wiring.

**7. Substrate is settled; the lane it releases is not.** The Codespaces LEAN v2 is accepted and CX53 is ruled **complementary, not competing** (`[#567]` is its carrier under `[#561]`). What makes an off-machine lane actually run is `[#554]`'s four provisioning legs — pinned `uv`, `git fetch --unshallow`, deterministic `pre-commit install` for all three hook types, and an env gate that refuses a half-provisioned start. Q4 and Q5 (cloud-lane hygiene, receipt gate) now have a written home but **no lane has yet run under them**, so the first cloud dispatch after this handoff is also the first test of those rulings. Sequence `[#554]` before, not after, the next cloud batch.

**8. What NOT to reopen.** Section Q is landed and applies at read time — apply it, do not re-litigate it. The substrate ruling, the `[#488]` axis LEAN (now built by `[#566]`), the `Backlog.md` view-layer verdict (now built by `[#563]` — do not re-run the trial, do not propose it as the store) and the ADR-110 batch shape are all decided. The immutable records — the as-issued lane contracts, `ERRATUM E1`'s append — stay as landed.<!-- FILL-IN:frontier END -->

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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-08-20-architect-2`. This line names only *which*
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-20-dev-knowledge-architect-2/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-20-dev-knowledge-architect-2/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-20-dev-knowledge-architect-2/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-20-dev-knowledge-architect-2/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-20-dev-knowledge-architect-2/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-20-dev-knowledge-architect-2/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-20-dev-knowledge-architect-2/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

# HANDOFF SUPPLEMENT — outgoing 2026-08-17 architect window (closed 2026-08-19 night)

## 1 · Strategic intent for the next session (way-of-working level)
Shift the fleet's center of gravity from PRODUCING evidence to CONSUMING it. This window proved
production at scale (15 closures banked in one day, 5 cloud lanes = 4462 artifact lines, global
dispatch helpers); C3 then measured the systemic defect: **of 116 open rows with git activity, zero
carry a closure signature** — the fleet works but does not close. The next session's methodology goal:
make evidence → ruling → closure a routine, mechanized loop — adjudication seats as a standard form
(S-1 is the proven template), rulings transcribed same-day, the operator dashboard as the visibility
organ (leg 2 scoped by the operator's review), and the full dispatch runbook codified in-repo
([#539]/Ch8) so no future seat needs chat archaeology to execute.

## 2 · Tensions weighed, and where I landed
- **Velocity vs safety gates.** Landed: gates stay, enforcement points chosen by cost — #406 ruled
  accept-as-is (ship-gate WARN, NO new pre-commit leg); commit-tax 291→207s with the --parallel flip
  pending the §2.6 bar. Safety lives in ship/push gates, not in a tax on every commit.
- **Library-first vs bespoke governance.** Landed asymmetrically, on measurement: BUY the view layer
  (Backlog.md ADOPT-VIEW-LAYER, three conditions), KEEP governance bespoke — no library exists for the
  intake→ADR→archive gate; that is our model.
- **Broken cloud CLI vs operator's demand for terminal dispatch.** Landed: engineer the API path
  (POST /v1/sessions with receipt gate) rather than accept manual web-UI paste or a local fallback.
  The product bug is documented to the line; the workaround is itself verified machinery.
- **Lane autonomy vs index freshness.** Landed: the integrator is gate-of-record for index freshness
  on lane material; a declared single-hook bypass on lane branches is sanctioned (ruling 9).
- **Enterprise vs personal substrate.** Measured, not argued: corporate seat is EMU with no Codespaces
  entitlement (403 on all 9 repos) → substrate = personal Codespaces (stage 1 proven by lane J) +
  Hetzner CX53 (stage 2, carrier [#561]).

## 3 · Considered and rejected — do not relitigate
- CLI `claude --cloud` transports: ARG (truncates at newlines+quotes), STDIN (creates no session),
  BRIEF-ON-BRANCH (sessions have no remote). All measured dead 2026-08-19. The working paths are the
  API create (Dispatch-CloudV2) and web-UI sessions.
- GPU substrate — operator-rejected 2026-08-17, do-not-relitigate.
- Enterprise Codespaces — EMU dead end, measured (probe report).
- Backlog.md wholesale migration — its id ledger is unsafe as source of truth (archive frees ids,
  deletion is a supported verb; the #440 weakness class).
- WSJF / RICE ranking axes — rejected per C4's LEAN (3–4 recurring estimates across 183 rows for an
  ordering produced by judgment anyway); graph-centrality inert on a 3-edge population.
- Hard byte ceiling on the assembled paste (#449) — accepted-with-reason HOLD, warn-only stands.
- A pre-commit doc_rot leg (#406) — rejected on velocity grounds, explicitly chosen.
- `tkr` — unlocatable (no npm package, no repo); dropped.
- Local execution of the C-lanes — operator refused; the cloud channel was fixed instead.

## 4 · Open questions (unresolved or deliberately deferred)
- [#397] scripts/ grouping: 26 of 100 files fit no group; DEFERRED to a daytime window, dated. The
  refreshed 100-file map is in C4's artifact.
- [#529] structlog clause: wiring is merged but Done-when says "via structlog" and the lane shipped
  stdlib-logging; ruling owed (adequacy vs literal clause).
- [#530] legs (a) unconditional remote-ref delete on release, (b) `_local_holder` mapping — open.
- Intakes #35–#37: still DRAFT; ratifying them requires ruling their ADR fork (no authorization was
  taken this window — correctly).
- --parallel flip: the §2.6 five-run quiet bar was DELIVERED AS A DISPATCH BLOCK but its execution was
  never confirmed by the operator — treat all three night lanes (gemini A/B, doc-rot hygiene, §2.6
  bar) as QUEUED, not running; they are the next window's first batch.
- Gemini 3.7 Flash admission: same status — the A/B lane is queued (C1 pack + ruled ADMIT bar ready);
  the two refusal items C1-N1/C1-N2 are scored by the architect BY HAND (ruled — they encode rulings,
  not greppable facts).
- [#171] leg 2 scope: awaiting the operator's review of ecosystem/conformance.html.
- Two ruled-but-unlanded births: run_id emit row (sequenced BEFORE the read-path build lane) and the
  #488 constraint-contention tiebreak implementation.
- C3's six self-contained AWAITING-RULING rows (#549 #507 #420 #331 #541 #491) and the [#506] per-id
  verdict pass (179/183 evidence coverage) — the next window's adjudication seat.

## 5 · Decomposition rationale — and what must NOT be redone
Shape: seat-arc (frozen multi-act contract on primary) for governance mutations; file-disjoint
worktree lanes for builds; cloud lanes read-only + docs-only artifacts (the N4 rule); ONE integrator
as serial merge gate; harvest order push-before-delete. This shape held under fire — S-1 executed 8
acts with zero SKIPs while five lanes and a product-debug ran concurrently.
Do NOT redo or re-decide: the eight L-5 rulings (transcribed, closed); the nine digest rulings of
2026-08-19 night (listed in the window memory file; transcription is the next seat's FIRST act); the
cloud-channel verdicts (CLI bug + API path); the dispatch mechanics (shipped as win-tooling global
commands); batch-2 and C-harvest merges (all on origin/main at 1b8992ca).

## 6 · Off-repo context
- Dispatch-CloudV2 + Dispatch-Lane + Get/Archive-CloudSession live in WIN-TOOLING (cross-repo home),
  installed via PSModulePath — new terminals only. Endpoint/headers/environment_id verified against
  claude-code CLI 2.1.235 and may drift with CLI updates; the RE-TEST procedure is in the win-tooling
  README. An Anthropic bug-report draft (CLI silent bundle fallback) is written, NOT yet submitted.
- The operator↔architect paste channel is broken in this chat client: inline browser copy-paste
  arrives EMPTY. All session outputs must travel as uploaded .md files. The next architect must state
  this in its first message and never claim to have read an inline paste without verifying content.
- Operator interface rules ratified this window (now standing): revise the operator's output FIRST,
  then exactly ONE next step; every contract file ships with its runnable dispatch block in the same
  message; every board paste gets an answer block for every "Needs input" row, unprompted; deliverable
  value is stated in human release-notes language, not repo jargon.
- Operator state: velocity frustration is the dominant theme; the dashboard + ledger + release notes
  exist to answer it. Gemini 3.7 Flash (launched 2026-08-13) is real and awaits measured admission.
  `--effort` takes full names only (low/medium/high/xhigh/max) — short forms silently ignored.

## 7 · Ratified-in-chat register (NOT yet recorded in the repo)
1. "Integrator is gate-of-record for index freshness on lane material; declared single-hook bypass on
   lane branches is sanctioned" — home: [#539] contract template + PLAYBOOK Ch8.
2. The nine C-digest rulings of 2026-08-19 night (run_id birth-before-read-path; C6 static-HTML stack
   accepted; C1 ADMIT iff G1∧G2∧G3 with hand-scored refusal items; C2 R1=(a) profiles live in the hub
   now; R2–R6 accepted; #488 LEAN accepted; #397 deferred-dated; C3 six rows + #506 to an adjudication
   seat) — home: row bodies / STANDING_RULINGS via the next seat's act 1.
3. "Push-before-delete on every harvest" — JOURNAL entry (i) exists; PLAYBOOK Ch8 needs the rule.
4. "Primary checkout is seat-arc-only; helper tasks run zero git ops in primary" (two HEAD-swap
   incidents witnessed) — home: STANDING_RULINGS.
5. "Cloud lanes branch fresh off origin/main and never touch foreign dirty files" — home: Ch8.
6. "Every cloud dispatch carries a RECEIPT gate (sources non-empty + first assistant text echoed)" —
   home: Ch8 + the [#539] generator.
7. Backlog.md ADOPT-VIEW-LAYER ratification with three conditions (one-way export; disposable
   gitignored export dir; governance stays bespoke) — verdict is in the trial artifact as PROPOSED;
   the ratification itself needs a decision record (mini-ADR or row).
8. Gemini admission bar (item 2 above) doubles as the standing NEW-MODEL acceptance procedure — home:
   PLAYBOOK lanes section (routing-table governance).
"None" does not apply — items 1–8 above WERE the debt and are now DISCHARGED: the window-close
transcription seat (END PACKET, pushed 217c68cb..4acce74f) landed all of it in the repo. This
register stands as the historical map only.

## 10 · TRANSCRIPTION SEAT — the repo now governs what the chat ruled (origin/main 4acce74f)
- STANDING_RULINGS section Q, ten rulings Q1–Q10 (index-freshness gate-of-record; primary =
  seat-only; push-before-delete; cloud-lane hygiene; receipt gate; contract-as-file; trajectory-
  inclusive Φ; medium tier for fan-out; G1∧G2∧G3 admission with hand-scored refusals + version
  P-item; refuted-premise ⇒ PAUSE). Ratchet held at 440.
- EIGHT births, ledger lawful (15 banked > 11 window births): run_id emit · [#488] tiebreak ·
  CX53 daily-driver ([#561]-carried) · provider-config dynamic links · Backlog.md view-layer
  implementation · lifecycle-archival pass+check · grouped hygiene (suite REDs + census
  findings) · Grok guarded-rerun row. Verdict annotations landed in [#491]/[#561]/[#539] and
  the new rows [#562]–[#569].
- Anti-orphan sweep: 18 carried / 2 deferred(dated: Ch8 landing or 2026-09-19) / 0 VIOLATIONS.
- LIFECYCLE CENSUS (the operator's question, measured): ADRs 88 = 86 live + 2 archived;
  intakes 34 live, 0 archived — NO intake archive directory exists; rows today +8 born / 0
  closed (transcription arc births by design; window total remains net-closing 15 vs 11).
  The archival gap is now a carried row, not a complaint.
- Known state handed forward: 45 WARNs on main incl. doc_rot 19 (births over the 1320 ceiling
  per the [#559] scheme) — next window's hygiene inherits; [#539] gap-table pointer was ADDED
  by this seat (its absence was a real finding, not a confirmation).

## 8 · OPERATOR MANDATE for the next window (his closing list, honest status attached)
Priority 1 — THE DISPATCH SYSTEM IN THE REPO. The helpers exist (win-tooling global commands:
Dispatch-Lane local-worktree, Dispatch-CloudV2 cloud-with-origin), but every new chat still cannot run
worktrees without archaeology. [#539]/Ch8 codification (runbook + gen_lane_contract: which work goes
local vs cloud, receipt gates, harvest, all 2026-08-19 rules) is the FIRST execution lane of the next
window — not a theme, a lane.
Priority 2 — performance he can FEEL: land the --parallel flip (bar report pending), run_id birth +
telemetry read page (C6 contract ready) so prompt/hook timing is visible, devcontainer speedups.
Priority 3 — provider universalization, genuinely NOT started this window: codex folder retirement /
AGENTS.md / vendor-neutral CLAUDE.md; and the VISION→README rename, which is a REFERENCE MIGRATION
(grep census of every referencing surface, atomic migration, dead-path validator) — never a bare
rename. #82 profiles (R1 ruled: hub home now) is the first brick.
Priority 4 — visibility he asked for repeatedly: his review of ecosystem/conformance.html scopes
[#171] leg 2; the #488 tiebreak birth makes priority ranking visible; the adjudication seat runs the
full intake/ADR orphan audit (instrument is live, dashboard section 2 shows VIOLATIONS).
Measured-and-closed (do not reopen): Enterprise Codespaces (EMU, no entitlement), cloud CLI verdict,
GPU. Python-library adoption is point-wise real (mutmut, uv, Backlog.md-view) but has no program —
the next window should name one or explicitly decline one.

## 9 · FINAL-HOUR RESULTS (window truly closed at origin/main 53b904c2)
- **Everything landed and pushed**; final integrator END PACKET is the consolidation of record
  (its WHERE-TO-LOOK section lists the dashboard + five key audits by path). Teardown complete:
  1 worktree (primary), 3 local + 3 origin branches, no --no-verify/SKIP anywhere in the arc.
- **--parallel flip LIVE on main** (54633041): commit tax measured ~97 s quiet; on Codespaces the
  same gate is ~19–20 s.
- **A/B verdicts (architect, hand-scored G1): Gemini 3.7 Flash NOT ADMITTED** (G1 fail — classified
  N1 instead of declining; G2 fails under the trajectory-Φ ruling; run is evidence-only per #491's
  Antigravity exclusion) — but 11/12 mechanical parity at Φ=0 and a TEXTBOOK role-decline on N2;
  after the #491 identity ruling it earns a clean rerun (pinned tier medium, 2.9× wall noted).
  **Grok 4.6 NOT ADMITTED** (G1 fail on clean evidence; C1-R4/C1-N2 contaminated — candidate read
  the pack incl. ground truths; rerun requires a no-pack sandbox guard; $2.69 spend, 81% on the two
  contaminated items). **Systemic finding: the INCUMBENT (haiku fan-out) also classified both role
  items (0/2)** — role discipline today lives in the architect's routing, not in any model; the
  gate works, no model passes it yet.
- **Codespaces audit ON MAIN** (docs/audits/2026-08-20-technical-codespaces-audit.md) with the
  RULING block; substrate escalation recorded: the operator now requires EVERY prompt on fast
  substrate → far above the 30–37 h/mo threshold → the CX53 "daily driver" lane (same
  devcontainer, VS Code Remote, claude on the box; Codespaces as parallel burst) is the FIRST
  substrate lane of the next window under [#561]. Defender-tax measurement task in flight —
  CONFIRMED = free local recovery; POLICY-BLOCKED = one more measured CX53 argument.
- **Pending, with owners:** Ch8 codification (architect; census on main) · provider-config
  dynamic-links lane (architect; junction mechanism, dev-knowledge as truth for
  .claude/.gemini/.grok/.codex) · step-0 free ceiling test (operator, 2 min) · ssh BOM one-byte
  fix (operator; ssh currently non-functional machine-wide) · Gemini slot-1 branch: KEEP
  docs/night-ab-gemini-2026-08-20, next window's hygiene renames its files -slot1 and merges
  docs-only · two pre-existing suite REDs reported undispositioned (stale routine-rows pin;
  constant-refusal test) — next seat's triage.

---

=== END OF PASTE — 5 sections · 65396 bytes ===
