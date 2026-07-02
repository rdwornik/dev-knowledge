=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-02-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **Cold refresh of the same live frontier — the priority is unchanged and is NOT fleet rollout.** The operator's three goals, in order, carry forward from the prior bundle's FILLED supplement: **(a) run the time-boxed FABLE whole-system review + merge its rulings; (b) wire ai-council as a CC-GOVERNED query mechanism (browser → CC → ai-council); (c) CLOSE the two open methodology tracks — ADR methodology + ai-council methodology.** Fleet rollout (**#221**) is real but sequenced **AFTER** the three goals (the Fable review may reshape the methodology, so scaling to n=3 first would propagate a soon-to-change methodology; #234/#231 hardening pair with the ai-council work). **What changed since the prior 2026-07-02 bundle (the ONLY window delta):** a housekeeping **stale-disposition prune** (`b255a8c`) tombstoned the 2 ai-council cross-repo probe dispositions — `handoff_probes` now binds 10 probes clean, so **`ship-gate` is GREEN with `4` WARN dispositioned, down from 6, and NO `[stale]` line.** No new design work landed; the arm-first arc + ARCHITECTURE currency + floor model A remain the sealed backdrop (do NOT redo). The incoming architect's job is unchanged: **run Fable first (perishable window), then wire+seal the two coupled methodology tracks; treat fleet #221 as sequenced-after.** OPEN forks: the Fable review scope under the time-box, the ai-council-integration shape (skill vs hook vs other), and what "closed" means for the ADR methodology (the #170/#168 traceability spine is the sticking point). |
| **Generated at** | Bundle cut at HEAD `f3c3f51`, **working tree clean**, `main` **in sync with `origin/main`**. This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` **ahead of `origin` until pushed**. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **Cold refresh — this bundle's SUPPLEMENT is EMPTY by disposition; the still-live strategic "why" lives in the PRIOR bundle.** This session was a cold `/clear → /handoff` with no outgoing architect chat holding new deliberation, so `SUPPLEMENT.md` is committed **empty** (the defined cold-handoff disposition, §13). The three-goal priority was captured in the **prior** bundle's FILLED supplement — **`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md`** — which remains **authoritative on priority** and un-acted-upon. `RESIDUAL.md` §4 carries that frontier forward (as inferred/recall, pointing at the prior filled supplement); the off-repo "why" is not in THIS paste (the empty supplement is `[skip]`-folded), so the incoming **§13(d) operator-context beat** narrows to *"anything changed since the prior 2026-07-02 supplement's three goals?"* — read the prior filled supplement for the full rationale.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough. This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry **no per-bundle README** (the 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

---

=== protocols/HANDOFF_BOOT.md ===

---
reconciled_with: handoff-process@5.3
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

# Residual — 2026-07-02 architect handoff (`-2`, cold refresh) — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This is a COLD REFRESH of the prior 2026-07-02 bundle.** The session was `/clear → /handoff`
> with no in-session design work; the only window delta since the prior bundle
> (`docs/handoffs/2026-07-02-dev-knowledge-architect/`) is a **housekeeping stale-disposition
> prune** (`b255a8c`). The strategic frontier is **unchanged and un-acted-upon** — the three-goal
> priority is carried forward here (§4) from that prior bundle's **FILLED** supplement, which stays
> **authoritative on priority**. This bundle's own `SUPPLEMENT.md` is committed **empty** (cold
> disposition), so its ANSWERS are not folded into `PASTE_THIS`; the incoming **§13(d) beat**
> narrows to *"anything changed since the prior supplement's three goals?"*
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window + the prior bundle,
> may have moved — the load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and **CLEAN**; the disposition register is now **6 → 4** (the prune cleared 2 stale cross-repo entries)

`python scripts/audit.py ship-gate` → **GREEN** (**4 WARN dispositioned**, **NO `[stale]` line**) —
verification organs green against this arc. The window's **only** change is a register cleanup:

- **2 stale cross-repo probe dispositions PRUNED (`b255a8c`, witnessed).** At the prior bundle's
  generation the ai-council cross-repo probes degraded to WARN and were dispositioned
  (`warn-handoff-probes-p5/p7-crossrepo-ai-council-2026-07-02`). The newer
  `2026-07-02-dev-knowledge-architect` bundle **superseded** the ai-council bundle as *latest*, so
  `handoff_probes` now binds **10 probes clean** ([OK]) and both dispositions matched **no live WARN**
  → tombstoned per the ADR-75 clearing convention. Result: the register drops **6 → 4** dispositioned,
  **NO `[stale]`**. The underlying cross-repo resolve-only gap stays tracked by **#234** (unchanged).

### Standing flags (benign / dispositioned — unchanged, do NOT touch) — the 4 that remain

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned
  (`warn-77-voided-closure`). **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) print `[~~]` under `health`, `[disp]` under `ship-gate`. **Expected
  seam, not a regression.** **#210** (open) proposes converting this class from per-instance
  disposition to a standing rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap) — a
  §4-adjacent decision.

_(The two ai-council cross-repo P5/P7 dispositions that were here at the prior handoff are **gone** —
pruned this window. That is the whole §1 delta.)_

---

## §2 — Shipped this window (prior 2026-07-02 bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~2). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`.

**The window is housekeeping-only — one arc:**
- **Stale-disposition prune** (`b255a8c` + journal anchor `41bc935`, merged `f3c3f51`): tombstoned the
  2 stale ai-council cross-repo probe dispositions (see §1). `ecosystem/disposition-register.yaml`
  (−26/+7). No design decision, no methodology change.

**The sealed backdrop (do NOT redo — carried by the PRIOR bundle, not re-narrated here):**
- The **arm-first chain executed** (#226/#230, **ADR-93** floor model A armed + conformance-proven n=1;
  real ai-council armed), the **ARCHITECTURE currency arc** (#222/#223/#224 — decoupled the volatile
  count-claims into `ecosystem/doc-counts.md`, documented the deploy subsystem, rotated the ADR lists),
  the **external-review system audit**, and the **first-ever cross-repo architect handoff** (ai-council,
  filed #234). Full map: `docs/handoffs/2026-07-02-dev-knowledge-architect/RESIDUAL.md` §2.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** (**94 tasks, 7 themes, 21 stories** — witnessed via
  `validate_backlog`) — the spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated) + this handoff branch
  `docs/2026-07-02-architect-handoff-2`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9,
  unchanged from the prior bundle): **code-edge = just `#218`**, **coherence = `#180/#181/#182/#220`**,
  **audit-py group includes `#234`** (the cross-repo-teeth item). **`#221`'s `depends-on: #226` is
  SATISFIED** (arming closed) — the hard edge that gated fleet is gone; fleet is navigable but
  **sequenced-after** the three goals (§4).

---

## §4 — The next frontier (open architecture decisions — carried forward from the prior FILLED supplement)

**Unchanged from the prior 2026-07-02 bundle** — nothing this window touched the design. The deploy
subsystem is **BUILT + ARMED + PROVEN (n=1) + DOCUMENTED**; the arm-first chain is **done and sealed**.
The repo's dependency graph reads fleet (#221) as next, but **the operator's FILLED supplement
re-scoped that** — fleet is real but **sequenced AFTER** the three goals below. The operator ruled the
supplement **authoritative on priority**. **Authoritative source (READ IT):**
`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md` ANSWERS. **recall/inferred** — the
architect resumes the design here.

**The priority (operator-ruled — the repo's dependency graph does NOT encode this):**
> **(a) FABLE review (time-boxed, FIRST)** → **(b)+(c) wire ai-council-as-governed-query + close the ADR + ai-council methodology tracks (one coupled work-stream, after Fable)** → **fleet #221 (sequenced-after)**.

1. **(a) Run the Fable whole-system review + merge its rulings — FIRST, because it is time-boxed.** The
   `.dev-knowledge` system audit + the review-ask (Part A: the §7 architecture forks; Part B: process-meta
   — over-engineering-for-solo, verify-proportionality, canonical-doc naming, deterministic-gate-vs-semantic-
   property) are **drafted**. Get them to Fable, extract maximum value from the **perishable preview window**
   (Mythos-tier, possibly export-restricted), then merge Fable's architectural rulings back into the
   methodology. **Do this first** — Fable's rulings (esp. two-track coherence + the deterministic-gate-vs-
   semantic-property class) **may reshape goals (b)/(c)**, so closing the methodologies before merging risks
   an unwind. OPEN: the review **scope** under the time-box (lean focused, not "review everything").
2. **(b) Wire ai-council as a CC-GOVERNED query mechanism.** Elevate ai-council from a standalone tool to a
   governed part of the methodology: an architect's multi-model-debate request routes **browser → CC (skill/
   hook) → ai-council**, with **CC managing the query lifecycle** — question authoring, save-to-correct-path
   discipline, and ADR management of the output. Closes the loop where ai-council *produces* ADRs but their
   governance is not yet mechanized. OPEN: the **integration shape** (skill vs hook vs other CC-side trigger)
   — settled in intent (CC governs the lifecycle regardless of trigger form), undecided in mechanism.
3. **(c) Close the two open methodology tracks — ADR methodology + ai-council methodology.** These are the
   operator's named "not yet done" loops; **(b) and (c) are one work-stream** (ai-council produces ADRs, the
   ADR methodology governs them). Seal both by mechanism, not memory. OPEN: what "closed" **means** for the
   ADR methodology — the **#170/#168 traceability spine** is the half-built sticking point.

**Fleet #221 + the hardening items — sequenced AFTER (demoted, not deleted):**
- **#221 — fleet rollout** (gated by intent, not dependency): run `deploy/tool.py` on corp-monorepo /
  corp-ops / corp-sca-time-automation to reach n=2+, each using **#230** as its acceptance gate; done-when
  also requires **#225** (surgical precommit carrier) closed. Scaling to n=3 before merging Fable's rulings
  would propagate a soon-to-change methodology. Carry the pilot rule: **treat each consumer's `.gitignore` +
  config shape as an UNKNOWN to probe, not a copy of the hub** (prior SUPPLEMENT §B; LESSONS 2026-07-01).
- **#225 — precommit carrier surgical edit** (comment-preserving; precedes fleet for clean diffs at scale).
- **#231 — consumer→hub feedback loop** (schema + transport + home open; pairs with (b)).
- **#234 — cross-repo probe FAIL-teeth** (harden `.claude/` cross-repo targets; honest-partial WARN today —
  the gap the pruned dispositions rode on).

**Adjacent open decisions (smaller, unchanged):**
- **#220 — the MODIFY / semantic-drift axis.** VERIFY-FIRST: does the ADR-89 Pyright oracle or any existing
  organ gate a *meaning-change-without-version-bump*, or only add/remove/exist? Demonstrated-catch bar first.
- **#210 — journal-wrap no-ff standing rule.** Path-scoped EXEMPT (JOURNAL/transcripts-only) vs branch-then-
  merge the wrap — must NOT weaken core-invariant #5.
- **#233 — deploy-record-index test tempdir isolation** (per-run isolated tempdir; hygiene debt).
- **#232 — ship-gate right-sizing (UNFILED candidate).** Right-size, not skip; referenced by #233 but never
  filed as its own id — the architect files it or folds it.

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The priority "why" (READ FIRST — this bundle's supplement is empty by cold disposition):** the PRIOR
  bundle's FILLED supplement — `docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md` ANSWERS —
  the three-goal priority, the Fable-first rationale (§5), the "what NOT to redo" list (§3), and the
  fleet-after ruling (§A). **Authoritative on priority; un-acted-upon; still live.**
- **The Fable review input (goal a):** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`
  (the system audit + the review-ask, Part A §7 architecture forks + Part B process-meta).
- **The arm-first arc's "why" (sealed backdrop):** **ADR-93** (floor model A, armed + conformance-proven),
  `LESSONS.md`, PLAYBOOK §20, `deploy/` (tool.py + carriers + `carrier_floor.py`), and the prior bundle's
  `RESIDUAL.md`/`HANDOFF_BOOT.md`.
- **This window's one capture:** `JOURNAL.md` top entry (`b255a8c`, the prune) + `ecosystem/disposition-register.yaml`.
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5.3 §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted `#id` +
> closing sha, the serialize-group membership, the counts, the dates — are deliberately **absent from
> this whole bundle**. That is what gives the probes teeth. Do not infer them; run the command. The
> "expected at generation" hints below are a **drift reference** so CC can detect movement between
> generation and check-time — the pass criterion is **"answered from the live source,"** never
> "matches the remembered number."
>
> **Cold refresh — SUPPLEMENT is EMPTY this bundle.** This window is housekeeping-only (a stale-
> disposition prune, `b255a8c`); no design work landed and there was no outgoing architect chat, so
> `SUPPLEMENT.md` is committed **empty** (cold disposition) and is `[skip]`-folded from the paste. The
> three-goal priority (Fable review → ai-council-as-governed-query → close the ADR + ai-council
> methodology tracks) is **carried in `RESIDUAL.md` §4** from the **prior** bundle's FILLED supplement
> (`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md` — authoritative on priority,
> un-acted-upon). So the §13(d) operator-context beat in P1's gate **NARROWS** to *"anything changed
> since the prior supplement's three goals?"* — it does **not** fire FULL (the load-bearing off-repo
> call is already recorded), but the ANSWERS live in the prior bundle, not in this paste.
>
> **Windows note:** `audit.py checks` (P2) crashes mid-listing on a bare cp1252 PowerShell console
> (a `→` in a check docstring) — run with `PYTHONUTF8=1` or in git-bash. `ship-gate` (P7) can
> false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P1 — Orientation (the architect's **first move**, before any mechanism — v5.3 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (v5.3 §13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` (near line 11) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` (near line 48) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (v5.3 §13d):** the
browser asks the operator for **off-repo** context. This bundle's supplement is **empty** (cold), so
its ANSWERS are not in the paste — but the three-goal priority is recorded in `RESIDUAL.md` §4 (from
the prior filled supplement), so the beat **NARROWS** to *"anything changed since the prior 2026-07-02
supplement's three goals?"* — **not** a FULL blank re-ask. (The load-bearing off-repo call is already
answered: **Fable-first, methodologies-next, fleet-after**; the full rationale is in the prior bundle's
`SUPPLEMENT.md`.)

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — **expected at generation: 26, last name `doc_code_coverage_drift`** (unchanged this window — no new check landed) | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **this bundle was cut at HEAD `f3c3f51`, tree clean, `main` in sync with `origin/main` — but this handoff's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: only the standing `#77` voided-closure false positive (`77e5d7df9`), no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — **expected: stamp on/after the last touch (both 2026-07-02); the 2026-07-02 stamp is HONEST (#223 genuine re-read; #222 decoupled the count-claims that had been forcing it) — this housekeeping window did not touch ARCHITECTURE** | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH (1030/1030)**, but the live count is the only ground truth and the pass test is "answered from the live source," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline:** at generation `ship-gate` is **GREEN** with **`4` WARN dispositioned** (#77 voided-closure + 3 journal-wrap/transcript no-ff) AND carries **NO `[stale]` line**. The register dropped **6 → 4** this window — the prune (`b255a8c`) tombstoned the 2 stale ai-council cross-repo P5/P7 dispositions (probes now bind clean). The live answer is the only ground truth (a new direct-on-`main` commit would re-RED it); the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the prior bundle's *filled* supplement; the live bundle + spec are the only ground truth — **expected: FIVE files (BOOT + RESIDUAL + PROBES + SUPPLEMENT + PASTE_THIS), NO `README.md`; `SUPPLEMENT.md` present with ANSWERS EMPTY (this is a COLD refresh — the empty supplement is `[skip]`-folded; the three-goal priority lives in the PRIOR bundle's filled supplement, carried into RESIDUAL §4); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-07-02-dev-knowledge-architect-2/` ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: code-edge = ONLY `#218`; coherence = `#180/#181/#182/#220`; the `audit-py` group includes `#234`** (unchanged this window — no BACKLOG edit) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — **NARROWED** to *"anything changed
   since the prior 2026-07-02 supplement's three goals?"* (this bundle's supplement is empty; the prior
   filled supplement carries the priority), not a FULL re-ask, before design. Then run P2–P9, each against
   **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **P7 is
   the headline: expected GREEN with `4` dispositioned WARNs AND NO `[stale]` line** (the prune dropped
   6→4) — but the pass criterion is **"answered from the live source,"** never "matches the verdict the
   summary remembered." **P2** is expected to read **26** (last name `doc_code_coverage_drift`). **P5**
   expects an HONEST 2026-07-02 stamp. **P6** is expected to **MATCH** (1030/1030), the claim in
   `doc-counts.md`. **P8** pins the five-file shape with `SUPPLEMENT.md` **EMPTY** (cold refresh — do NOT
   confuse with the prior bundle's *filled* supplement; no README). **P9** pins the now-durable
   serialize-group graph (#156) with **code-edge = just #218** and **`#234` in the `audit-py` group**.
