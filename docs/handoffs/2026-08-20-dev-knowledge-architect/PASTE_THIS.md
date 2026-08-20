=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-20-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-20-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Drain the unruled queue the 2026-08-19 cloud harvest deposited, and convert evidence into rulings, rows and ADRs — this window produced findings faster than it produced decisions, and `docs/audits/2026-08-19-technical-c-lanes-consolidated.md` §6 assembles ten open asks that no seat has ruled. **The standing authority is `[E7] Tooling & evaluation`** and the batch shape stays ADR-110 (one plan → N file-disjoint frozen lanes → one serial integrator). Suggested order, and the reasoning is in `RESIDUAL.md` §4 rather than here: rule the **cloud-lane contract vs `audit-index-freshness` conflict** first because the digest records it recurring on *every* cloud lane that adds an audit artifact, then the **C6 `run_id` emit-contract** question while `[#529]` is still library-only and therefore still cheap to amend, then the free-standing C2/C3/C4 asks, then resume **priority order v2** (`[#533]` leg 2 → `[#529]`/`[#530]` wiring → `[#554]` → the `[#533]` seam leg → `[#555]`), and decide whether the seven DRAFT intakes get their own lane rather than riding a wrap again. Task-state is `BACKLOG.md` — the spec, read it there, never re-narrated here; the prior window's ordered plan lives in `docs/handoffs/2026-08-17-dev-knowledge-architect/SUPPLEMENT.md` and is an **INPUT** to this handoff, not the handoff itself.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->Planning and governance surfaces only: `tasks/` plus `gen_task_tree.py --emit-source` for any row change (never `BACKLOG.md` by hand), `docs/decisions/ADR-*.md` for ratifications, `docs/intake/*` status transitions **with both** intake generators, `protocols/*.md` for promotion debt, `JOURNAL.md`, and `docs/audits/` for anything this seat produces. **Implementation does not happen in this tree** — `[#533]` leg 2, the `[#529]`/`[#530]` wiring and `[#554]` are dispatched to file-disjoint lane worktrees from this seat, because the seat's own writes and a lane's writes must not share a tree.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->**architect**, because the deliverable is a decision set — which of the ten assembled asks are ruled, which intakes ratify, and what shape the next batch takes — rather than the advance of one named backlog row, which is what execution mode is profiled for. So the residual is scoped to the planning *why* plus the whole `BACKLOG.md`, and the browser is served the generative/decompositional posture.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-08-20-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-08-20-dev-knowledge-architect — the part the repo does not already encode

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
**Provenance tag for this whole residual, stated once:** the drift-check *runs* and the branch / backlog / intake reads behind it are `witnessed` — CC re-derived them live at generation. Everything in §2 is `recall` from `JOURNAL.md` and the git spine: **this seat did not participate in the sessions that produced this window's work**, so §2 is a map of the record, not a report of lived experience. Treat it accordingly and re-check anything load-bearing via `PROBES.md`.

**Standing / already-dispositioned — not news.** The row-length family in `ecosystem/disposition-register.yaml` now covers `[#546]` `[#547]` `[#552]` `[#533]` `[#529]` `[#530]`; alongside it sit the undeclared-intake prompt-template family (intake #25, #30, the v6 proposal), `warn-reconciled-versions-contributing-template`, `warn-review-artifact-lane-c-504-no-tally` and `warn-journal-spine-anchored-by-mention`. **The register growing on the row-length axis is itself the signal** — §4 item 4 carries why that is a decision and not a maintenance chore.

**New this window, and it changes how one flag class must be READ.** `[#560]` establishes that `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file and one title literal, so a real review can be invisible to it and some of its WARNs are false by construction. `[#499]`'s hard flip is gated on that same count. Until `[#560]` lands, **that WARN family is not evidence** — do not disposition against it and do not read a clean count from it as coverage.

**Second reading caveat, from the harvest itself.** C2 recorded that the cloud containers had **no gates armed at all**, so for the five `claude/*` lanes the first hub gate run was the merge, not the lane. Any drift those artifacts carry therefore surfaces in post-merge checks now rather than having been caught in-lane — §4 item 2 is the decision that follows.

No verdict, WARN count, `[stale]` status, drifted `#id` or sha appears above **by design**: `PROBES.md` P4/P6/P7/P9 re-derive every one of them live, and naming a value here would re-invert the anti-bluff contract.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
`recall` — reconstructed from `JOURNAL.md` and `git log --first-parent`, one line per arc, pointing at the entry that holds the detail. The JOURNAL already encodes the *how*; this is only the map. Thirty-five first-parent spine entries landed since the prior bundle was cut.

- **Batch 1 integrates** — 8 lanes merged, 6 rows banked, the row-length pile reaches zero undispositioned · JOURNAL 2026-08-18 (d); its two own drifts repaired in (e), packet closed out in (f)
- **Phase 0 baselines** — the commit-tax measured at **6.9× its recorded figure**, and the mutation pilot measured nothing · 2026-08-18 (c). The commit-tax number is what makes `[#533]` leg 2 a throughput argument rather than a legibility one
- **NB7 morning consolidation** — two of four land; the two oversized rows come under the ceiling · 2026-08-18 (a)/(b)
- **The N1–N5 night** — four of five land; **N4 refused at the docs-only gate** · 2026-08-19 (a) — then landed audits-only by the S-1 adjudication seat, which also gave two unlocated rules a locator, cleared D8's WARN, and recorded **three births, seven closures** · (b)
- **`[#122]` closes** on the operator's KEEP word, and the fleet-audit blocker clears · 2026-08-19 (c)
- **Batch 2** — four lanes land, **lane L2 REFUSED on its own Done-when**; the operator then reversed the refusal as mis-addressed and L2 merged · (d)/(e). The refusal-then-reversal is precedent worth knowing before the next refuse-rule call
- **`[#486]` closes** — the cp1252 crash the caches wave recorded but did not own · (f); dashboard regenerated onto the closed state · (g)
- **The five cloud C-lanes are harvested** — **5 merged / 0 refused / 0 pending**, 4462 lines of artifact, one consolidated digest `[#348]` · (h) — and their five dispatch briefs land so provenance sits in the same tree `[#539]` · (i)
- **Born this window:** `[#559]` (kernel/lab check tiering + installable package — the fleet's oldest ACCEPTED-unfiled debt), `[#560]` (the review-artifact reader's structural blindness), `[#561]` (re-base the compute plan onto the Hetzner CX line)
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Read this first: the window's defining asymmetry.** It closed with a large, well-evidenced, *assembled but unruled* queue — `docs/audits/2026-08-19-technical-c-lanes-consolidated.md` §6 lists ten asks, each carried across with its originating lane's own urgency framing, and the digest is explicit that it **assembles evidence and rules nothing**. The seat that produced the evidence was correct not to rule from inside the harvest. The consequence is that the ruling debt is now this seat's, and it is the largest single carry into the next session.

**1. The cloud-lane contract vs `audit-index-freshness` — rule this one first; it is the only ask that recurs.** A cloud lane whose contract forbids index regeneration cannot add a `docs/audits/` artifact without tripping the hub's `audit-index-freshness` gate. C1 resolved it the only way left to it — `git commit --no-verify`, twice, and it declared this rather than hiding it. The digest names it a **standing structural conflict, not a lane defect**, recurring on every cloud lane that adds an artifact. Three shapes are available and none is chosen: exempt cloud lanes from regeneration and have the integrator regenerate once at the queue's close (which is de facto what 2026-08-19 (h) already did, successfully, and the conflict-by-regeneration resolution there is a working precedent); or drop the no-regeneration clause from the lane contract; or make the gate lane-aware. Ruling it once retires a per-lane bypass that currently looks like discipline failure in the record but is not.

**2. Cloud lanes run with no gates armed — so "green in the lane" is not a claim about a cloud lane.** C2 recorded that the containers had **no hub gates armed at all**; the merge was the first time any gate ran on that material. This is the same question as `[#554]`'s provisioning leg (deterministic `pre-commit install` for all three hook types) arriving from the other direction, and it should be ruled as one question, not two. The decision is whether the model is **integrator-as-gate** (accepted, and then the lane contract should stop implying in-lane verification) or **provisioned-and-armed** (and then `[#554]` owns it and the cloud dispatch path blocks on it). Leaving it unstated is what produces receipts that read greener than they are.

**3. Two time-critical asks expired unruled — and one of the two deadlines was simply wrong.** C6 routed `run_id` in the emit contract as due "TODAY" with its window closing at the L2 merge; **L2 merged on 2026-08-19** (JOURNAL (e)), so that window closed. But `[#529]` is still **LIBRARY ONLY with zero call sites**, so the emit contract is still cheap to amend right up until the wiring lands — the *ask* is live, the *deadline* was mis-derived. C1's three-gate ADMIT/REFUSE bar was scoped to "tonight's slot," which has passed; it needs re-issuing or declaring moot. **The meta-question is the durable one:** a lane may declare a deadline the integrator has no way to meet, and nothing in the protocol catches that. Worth one ruling on whether a lane-declared deadline binds at all.

**4. Carried and deliberately deferred — resume, do not relitigate.** (a) The `doc_rot` **row-length ceiling versus actual practice** — the register now carries six row-length dispositions and the standing stance is that `doc_rot` greens by fixes and never by dispositions, so either the ceiling moves or long rows decompose; every future birth otherwise adds a finding to a class that is supposed to be shrinking. (b) **Which row owns the unshallow and the `uv`-pin assert** — `[#554]` and `[#453]` overlap on two of four legs, and `[#554]`'s second-lander-points-at-the-first clause is a convention this seat may ratify or replace, not a decision already made. (c) **One denominator predicate** — three counts of the same backlog remain in circulation, and `[#555]` makes naming one its first act; until then any *net-negative* claim is unfalsifiable, which matters because net-closing is the stated goal. (d) **Who performs promotion** — the durable homes for the ratified terms are named, the promotion *act* is still unowned.

**5. Decided-unfiled is now the repeat failure mode, and it has a measurement.** Seven intakes sit `DRAFT`; the prior window's plan to ratify #35–#39 did not execute. `[#559]` is the sharpest instance — intake #25's W-2 was ACCEPTED on 2026-08-05 and carried **zero rows for fourteen days**, verified by carrier test rather than asserted. The pattern is that ratification rides a wrap, and wraps get consumed by integration. The open decision is whether ratification gets **its own dispatched lane** with its own contract, the way implementation does.

**6. One instrument is untrustworthy and gates another.** `[#560]`: `review_artifact_coverage` reads only the first branch/HEAD triple per file plus one title literal, so a genuine review can be invisible to it — and `[#499]`'s hard flip is gated on that leg's false-positive count. Fixing the reader is a precondition for the flip, not an independent tidy-up. Sequence them.
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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-08-20-architect`. This line names only *which*
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-20-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-20-dev-knowledge-architect/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-20-dev-knowledge-architect/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-20-dev-knowledge-architect/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-20-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-20-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-20-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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
- --parallel flip: awaiting the night §2.6 five-run quiet bar report.
- Gemini 3.7 Flash admission: awaiting the night A/B results; the two refusal items C1-N1/C1-N2 are
  scored by the architect BY HAND (ruled — they encode rulings, not greppable facts).
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
"None" does not apply — items 1–8 are the debt; the next seat's first act should transcribe them.

---

=== END OF PASTE — 5 sections · 57151 bytes ===
