=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-02-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **The FILLED supplement re-scoped the priority to a new P0: close the enforcement-transfer gap.** A CC-verified live finding (all 4 consumers) shows the deploy subsystem carries the **presence** of the methodology, **not its enforcement** — five hub enforcement organs (`session_end_backpressure` JOURNAL hard-block, `canonical_freshness`, `doc_claims`, `git_backlog_drift`, the coherence spine) are **HUB-ONLY**; **nothing inside any consumer enforces them locally (5/5 ABSENT).** "Held by mechanism, not memory" is **TRUE for the hub, FALSE for every consumer** — a constitution violation replicated 4× (proof: ai-council shipped 3 epics with JOURNAL ~1 month stale, unblocked). **P0 = build the consumer-local enforcement carrier the deploy subsystem never had:** decomposition is **(2) Informant Organ** (read-only enforcement-coverage reporter, low-regret, operator-approves its path) → **(3) mesh carrier** — the **located Fable consult** on the mesh-transfer model **(A)** 5th-carrier-local / **(B)** hub-sweep-on-cadence / **(C)** hybrid, whose tension is **local enforcement vs the Layer-2 autonomy-no invariant** → (4) record the *deployed-presence ≠ deployed-enforcement* lesson. **The prior three-goal priority (Fable whole-system review → ai-council-as-governed-query → close ADR + ai-council methodologies) is DEMOTED to sequenced-after** (real, kept; note #170/#168 were reclassified as arc-tracking, NOT the ADR sticking point — that track is less blocked than believed). Fleet **#221** stays sequenced-after; **do NOT onboard corp-monorepo until the mesh carrier + Informant Organ are proven.** **The only git delta this window:** a housekeeping **stale-disposition prune** (`b255a8c`) → `ship-gate` GREEN, **4 WARN dispositioned (down from 6), NO `[stale]`**; the finding itself is off-repo (browser-side), carried in the folded supplement. |
| **Generated at** | Bundle cut at HEAD `f3c3f51`, **working tree clean**, `main` **in sync with `origin/main`**. This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` **ahead of `origin` until pushed**. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **Generated cold, then FILLED — the fill RE-SCOPED the priority to the enforcement-mesh P0.** This bundle's `SUPPLEMENT.md` was generated empty (housekeeping-only git window) and then **FILLED** by the operator from an outgoing architect chat holding a **CC-verified live finding** — the enforcement-transfer gap (above). Its ANSWERS are folded into `PASTE_THIS.md`, carry this window's **off-repo strategic "why,"** and **supersede the prior three-goal priority.** `HANDOFF_BOOT` + `RESIDUAL` §4 are **re-scoped to lead with the enforcement-mesh P0** (three goals + fleet #221 demoted to sequenced-after, kept not deleted). Because the supplement carries answers, the incoming **§13(d) operator-context beat NARROWS** to *"anything changed since?"* — **not** a FULL re-ask. The prior bundle's supplement (`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md`) holds the now-demoted three-goal context.

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
> **Generated as a cold refresh, then FILLED — and the fill RE-SCOPED the priority.** The window's
> only git delta since the prior bundle (`docs/handoffs/2026-07-02-dev-knowledge-architect/`) is a
> **housekeeping stale-disposition prune** (`b255a8c`, §1/§2). But the operator then **FILLED
> `SUPPLEMENT.md`** from an outgoing architect chat holding a **CC-verified live finding** that
> **supersedes** the prior three-goal priority: **the enforcement-transfer gap is now P0** (§4). The
> filled ANSWERS are folded into `PASTE_THIS`; the incoming **§13(d) beat NARROWS** to *"anything
> changed since?"* **§4 below leads with the enforcement-mesh P0**; the three goals + fleet #221 are
> demoted to **sequenced-after** (kept, not deleted). The full rationale is the folded
> `SUPPLEMENT.md` ANSWERS — read them.
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

## §4 — The next frontier (open architecture decisions — RE-SCOPED by the FILLED supplement to the enforcement-mesh P0)

**The filled supplement's CC-verified finding re-scoped the priority.** The deploy subsystem is
**BUILT + ARMED + PROVEN (n=1) + DOCUMENTED** — but it carries the **presence** of the methodology,
**not its enforcement**. **Authoritative source (READ IT):** the folded
`SUPPLEMENT.md` ANSWERS (this bundle). **recall/inferred from the fill** — the architect resumes here.

**THE P0 (new — supersedes the prior three-goal priority):**
> **Close the enforcement-transfer gap — make "held by mechanism, not memory" TRUE for consumers, not just the hub.**

- **The finding (CC-verified live, all 4 consumers).** Five hub enforcement organs —
  `session_end_backpressure` (JOURNAL hard-block), `canonical_freshness`, `doc_claims`,
  `git_backlog_drift`, the coherence spine — are **HUB-ONLY**: they fire only when the hub runs
  `audit.py` against a consumer from outside. **Nothing inside any consumer enforces them locally
  (5/5 ABSENT across ai-council / corp-monorepo / corp-ops / corp-sca-time-automation).** The one
  organ present fleet-wide is the plugin's `propose_closures` — **non-blocking by design.** So there
  is **zero fail-closed enforcement in any consumer.** Proof it bites, not theory: ai-council shipped
  3 feature epics this window with JOURNAL ~1 month stale and nothing blocked it. **"Held by mechanism,
  not memory" is TRUE for the hub, FALSE for every consumer — a constitution violation replicated 4×.**
- **The gap:** the deploy subsystem's 4 carriers (globalconfig / plugin / precommit / floor) were
  **never designed to transfer** the hub Stop-hook or the `audit.py` organs. There is **no
  consumer-local enforcement carrier.**
- **The decomposition (dependency-ordered; steps 0–1 DONE this window):** (0) stabilize live + (1)
  fleet-map — **done** (the blast-radius map above; ai-council JOURNAL-backfill instruction sent to
  its architect) → **(2) build the Informant Organ** (read-only per-consumer × per-organ coverage
  reporter: enforcing-local / absent) — **low-regret, correct regardless of mesh-model, gives the mesh
  work its acceptance signal; its file path is a new-path decision needing operator approval** →
  **(3) build the mesh carrier** — **the located Fable consult** → (4) record the lesson (LESSONS +
  PLAYBOOK: *deployed presence ≠ deployed enforcement; done only when enforcement-in-effect is
  demonstrated — the configured→armed→proven distinction, generalized to the mesh*).
- **The core fork (→ Fable RULES, CC IMPLEMENTS):** the **mesh-transfer model** — **(A)** mesh as a
  **5th carrier**, organs run locally inside each consumer; **(B) hub-sweep-as-mesh**, the hub runs
  `audit.py` against the fleet on a cadence (must actually run, not "when I remember"); **(C) hybrid** —
  fail-closed organs (JOURNAL) go local via (A), awareness organs (freshness/drift) go hub-sweep via
  (B). **Tension:** local enforcement (autonomy/immediacy) **vs the Layer-2 autonomy-no invariant** — a
  hub pushing running hooks into consumers on a schedule brushes against "hub initiates no autonomous
  cross-repo writes." Contested + high-stakes + no-obvious-answer + a Layer-2-invariant tension → clears
  the routing bar for a Fable consult. **Feed Fable the fleet-map, not an n=1 sample.**
- **OPEN:** mesh-model A/B/C (→ Fable); per-organ local-vs-hub assignment (JOURNAL clearly local;
  `git_backlog_drift` + coherence spine may be inherently hub-scoped); Informant-Organ file path
  (operator approval); does #139 (merged-arc→record) + #170/#168 (arc-tracking spine) fold into this
  work-stream (likely yes — record-integrity family); **the #168-hard vs Fable-WARN conflict** (#168's
  Done-when says promote the JOURNAL leg to fail-closed HARD; Fable consult #1 ruled arc-tracking stays
  WARN with no-item disposition) — **unresolved.**
- **DON'T lose the un-merged Fable consult #1 rulings** (accepted, disposition pass halted by the
  re-scope — fold into the next session or they die in the outgoing chat): leg-(e) functional-proof into
  ADR-81; undeclared-edge scan → ship-gate WARN; immutability re-scope (status-line mutable on
  ratification, decision-content frozen — narrows core-invariant #5, operator sign-off pending);
  ai-council wiring lane-split (architect frames, CC mechanically expands).

**The prior three-goal priority — DEMOTED to sequenced-after (real, kept, not deleted):**
- **(a) FABLE whole-system review + merge rulings** — but note the **mesh-model ruling (step 3 above)
  is now the highest-value remaining use of the perishable Fable window**; the drafted §7 system-audit
  review-ask is real but sequenced behind the mesh consult. Input:
  `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier;
  browser → CC → ai-council; CC owns the mechanical lifecycle, architect owns question-framing) —
  **designed, not built.** Sequenced after the mesh gap.
- **(c) Close the two methodology tracks — ADR + ai-council.** **Unblocked this window:** #170/#168
  were verified-at-source as **arc-tracking** (issue-ID↔commit anchor, same family as #139), **NOT
  ADR-lifecycle — the prior handoff mis-filed them as the ADR sticking point.** So ADR-methodology
  closure is less blocked than believed; **(b)+(c) remain one work-stream**, sequenced after the mesh gap.

**Fleet #221 + the hardening items — sequenced AFTER (demoted, not deleted):**
- **#221 — fleet rollout** (gated by intent, not dependency): run `deploy/tool.py` on corp-monorepo /
  corp-ops / corp-sca-time-automation to reach n=2+, each using **#230** as its acceptance gate; done-when
  also requires **#225** (surgical precommit carrier) closed. Scaling to n=3 before merging Fable's rulings
  would propagate a soon-to-change methodology. Carry the pilot rule: **treat each consumer's `.gitignore` +
  config shape as an UNKNOWN to probe, not a copy of the hub** (prior SUPPLEMENT §B; LESSONS 2026-07-01).
  **Rejected — do NOT onboard corp-monorepo now** (supplement §3): it was deliberately sequenced last so
  this gap would surface on the n=1 pilot; onboarding it through the **current** deploy subsystem would
  inherit the same enforcement-mesh gap — **do not onboard until the mesh carrier + Informant Organ are
  proven.**
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
- **The priority "why" (READ FIRST — the P0 re-scope):** THIS bundle's FILLED `SUPPLEMENT.md` ANSWERS —
  the enforcement-mesh finding (5/5 organs ABSENT fleet-wide), the decomposition (Informant Organ → mesh
  carrier → Fable consult on A/B/C), the "deployed presence ≠ deployed enforcement" lesson, the rejected
  paths (§3), and the un-merged Fable consult #1 rulings (§6). **Authoritative on priority; P0.** The PRIOR
  bundle's supplement (`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md`) holds the now-demoted
  three-goal priority — read it for that context, but it is **superseded** on priority.
- **The Fable review input (demoted goal a):** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`
  (the system audit + the review-ask) — sequenced behind the mesh-model Fable consult.
- **The arm-first arc's "why" (sealed backdrop):** **ADR-93** (floor model A, armed + conformance-proven),
  `LESSONS.md`, PLAYBOOK §20, `deploy/` (tool.py + carriers + `carrier_floor.py`), and the prior bundle's
  `RESIDUAL.md`/`HANDOFF_BOOT.md`.
- **This window's captures:** `JOURNAL.md` top entry (`b255a8c`, the prune) + `ecosystem/disposition-register.yaml`;
  the enforcement finding is off-repo (browser-side, CC-verified live) — it lives in the folded `SUPPLEMENT.md`.
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
> **Generated cold, then FILLED — the fill RE-SCOPED the priority.** The git window is housekeeping-only
> (a stale-disposition prune, `b255a8c`), but the operator then **FILLED `SUPPLEMENT.md`** with a
> CC-verified live finding — **the enforcement-transfer gap (5 hub organs HUB-ONLY, 5/5 ABSENT across all
> 4 consumers)** — that **supersedes** the prior three-goal priority. Its ANSWERS are folded into the
> paste; `RESIDUAL.md` §4 + `HANDOFF_BOOT` are re-scoped to lead with the **enforcement-mesh P0** (three
> goals + fleet #221 demoted to sequenced-after). So the §13(d) operator-context beat in P1's gate
> **NARROWS** to *"anything changed since the supplement was written?"* — it does **not** fire FULL.
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
browser asks the operator for **off-repo** context. This bundle's supplement is **FILLED** (its ANSWERS
are in the paste — the enforcement-mesh P0, the Informant-Organ → mesh-carrier decomposition, the
mesh-model A/B/C fork), so the beat **NARROWS** to *"anything changed since the supplement was
written?"* — **not** a FULL re-ask. (The load-bearing off-repo call is already answered:
**enforcement-mesh gap is P0; the prior three goals + fleet are sequenced-after.**)

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — **expected at generation: 26, last name `doc_code_coverage_drift`** (unchanged this window — no new check landed) | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **this bundle was cut at HEAD `f3c3f51`, tree clean, `main` in sync with `origin/main` — but this handoff's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: only the standing `#77` voided-closure false positive (`77e5d7df9`), no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — **expected: stamp on/after the last touch (both 2026-07-02); the 2026-07-02 stamp is HONEST (#223 genuine re-read; #222 decoupled the count-claims that had been forcing it) — this housekeeping window did not touch ARCHITECTURE** | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH (1030/1030)**, but the live count is the only ground truth and the pass test is "answered from the live source," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline:** at generation `ship-gate` is **GREEN** with **`4` WARN dispositioned** (#77 voided-closure + 3 journal-wrap/transcript no-ff) AND carries **NO `[stale]` line**. The register dropped **6 → 4** this window — the prune (`b255a8c`) tombstoned the 2 stale ai-council cross-repo P5/P7 dispositions (probes now bind clean). The live answer is the only ground truth (a new direct-on-`main` commit would re-RED it); the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement state; the live bundle + spec are the only ground truth — **expected: FIVE files (BOOT + RESIDUAL + PROBES + SUPPLEMENT + PASTE_THIS), NO `README.md`; `SUPPLEMENT.md` present with ANSWERS FILLED (generated cold, then filled by the operator → the ANSWERS region carrying the enforcement-mesh finding is folded into `PASTE_THIS`); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-07-02-dev-knowledge-architect-2/` ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: code-edge = ONLY `#218`; coherence = `#180/#181/#182/#220`; the `audit-py` group includes `#234`** (unchanged this window — no BACKLOG edit) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — **NARROWED** to *"anything changed
   since the supplement was written?"* (this bundle's supplement is FILLED, ANSWERS folded into the paste),
   not a FULL re-ask, before design. Then run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **P7 is
   the headline: expected GREEN with `4` dispositioned WARNs AND NO `[stale]` line** (the prune dropped
   6→4) — but the pass criterion is **"answered from the live source,"** never "matches the verdict the
   summary remembered." **P2** is expected to read **26** (last name `doc_code_coverage_drift`). **P5**
   expects an HONEST 2026-07-02 stamp. **P6** is expected to **MATCH** (1030/1030), the claim in
   `doc-counts.md`. **P8** pins the five-file shape with `SUPPLEMENT.md` **FILLED** (generated cold, then
   filled by the operator + folded into `PASTE_THIS`; no README). **P9** pins the now-durable
   serialize-group graph (#156) with **code-edge = just #218** and **`#234` in the `audit-py` group**.

---

=== SUPPLEMENT.md ===

System state — confirmed (what this session established vs what stays open)
The headline finding (CC-verified against live config, all 4 consumers):
The deploy subsystem carries the presence of the methodology, not its enforcement. Five hub enforcement organs — session_end_backpressure (JOURNAL hard-block), canonical_freshness, doc_claims, git_backlog_drift, the coherence spine — are HUB-ONLY across the entire fleet: they only fire when the hub runs audit.py against a consumer from outside. Nothing inside any consumer enforces them locally.
Blast-radius matrix (live, this window):
Consumer5 enforcement organsWhat DID wire in locallyai-council5/5 ABSENTplugin Stop→propose_closures; floor-hash (2-leg); ruff v0.15.5; toc-freshness (1 file)corp-monorepo5/5 ABSENTplugin Stop→propose_closures; ruff v0.15.8; tach-check; toc-freshness (1 file); no floor-hashcorp-ops5/5 ABSENTplugin Stop→propose_closures; surface-conformance.ps1 nudge; no .pre-commit-config.yaml at allcorp-sca-time-automation5/5 ABSENTplugin Stop→propose_closures; floor-hash ONLY
The proof it matters, not theory: ai-council shipped 3 feature epics this window with JOURNAL ~1 month stale and nothing blocked it — because the organ that would block it (ADR-85 session_end_backpressure) does not exist in that repo. The one organ uniformly present fleet-wide is the plugin's propose_closures — which is non-blocking by design (detect-and-propose, never fail-closed). So there is zero fail-closed enforcement in any consumer.
What this means at the principle level: "held by mechanism, not memory" — the system's founding standard — is TRUE for the hub and FALSE for every consumer. In consumers, JOURNAL currency, doc freshness, and coherence are held by operator memory. That is a violation of the constitution, replicated 4×.
Sealed / verified this window (do NOT redo):

The fleet blast-radius map above (CC read-only, live config all 4 repos).
Verify-at-source on #170/#168: they are arc-tracking (issue-ID↔commit anchor), the same family as #139 — NOT ADR-lifecycle. This unblocks ADR-methodology closure (the prior handoff mis-filed them as the ADR sticking point). Grounded in live BACKLOG quotes.
Register cleanup: 2 stale cross-repo dispositions pruned; ship-gate 6→4 dispositioned, GREEN, on main (b255a8c).

Still OPEN (the whole point of the next session):

The enforcement mesh has no consumer-local carrier. The deploy subsystem's 4 carriers (globalconfig/plugin/precommit/floor) were never designed to transfer the hub Stop-hook or the audit.py organs. This is the gap.

Mistakes made this session — carry as lessons (accountability, not hand-wringing)
The load-bearing methodology lesson — this is the one to encode in LESSONS + PLAYBOOK:
Deployed presence ≠ deployed enforcement. Every prior audit (incl. the ai-council adoption audit) reported CONFORMS ✅ / no adoption gaps — because each measured whether the carrier'd files are present + conforming, never whether the enforcement fires. The gap was structurally invisible to the entire verification chain. The operator repeatedly instructed "map the whole methodology into the consumer"; each time, the carriers that exist landed, and each audit confirmed "done" — so more instruction produced more false-green, not detection. The rule this generates: a deploy/onboard is not "done" on presence-conformance; it is done only when enforcement-in-effect is demonstrated (a hook actually fires, a gate actually blocks) — the exact configured→armed→proven distinction the floor arc already established, never generalized to the mesh.
The outgoing architect's own miss (this chat, honest): had the ai-council adoption audit in hand — it literally showed JOURNAL stale by a month — and passed CONFORMS through as "adoption good, green light" instead of interrogating whether present meant enforcing. The operator caught by eye what the review gate should have caught. Root cause of the class, though, predates this chat: the deploy subsystem was designed without a mesh carrier, in prior sessions not auditable from here.
Lesson for the next architect (conduct): this session also failed on delivery — raw reasoning leaked into user-visible output repeatedly, and answers thrashed between walls-of-text and shallow one-liners under pressure. Do not replicate. Keep thinking under the hood; lead insight-first; match depth to the weight of the moment, not to the operator's frustration.
1. Strategic intent (way-of-working goals, not tasks)
The single goal: close the enforcement-transfer gap — make "held by mechanism, not memory" true for consumers, not just the hub. Concretely: design and build the mechanism by which hub enforcement organs reach consumers (or by which the hub reliably enforces against them on a cadence), plus a standing organ that makes this class of gap impossible to miss again by measuring enforcement-in-effect rather than presence.
This supersedes the prior three-goal priority (Fable review → ai-council-as-governed-query → close ADR + ai-council methodologies). Those are real and sequenced-after, but the fleet-wide constitutional gap is now P0. Do not lead with the three goals; lead with the mesh gap.
2. Tensions weighed
Mostly OPEN — the next session must weigh them; do not assume settled:

Mesh-transfer model (the core fork). (A) mesh as a 5th carrier — organs run locally inside each consumer; (B) hub-sweep-as-mesh — the hub runs audit.py against the fleet on a cadence, consumers enforce nothing locally but the sweep must actually run on cadence (not "when I remember"); (C) hybrid — fail-closed organs (JOURNAL) go local via (A), awareness organs (freshness/drift) go hub-sweep via (B). Tension: local enforcement (autonomy, immediacy) vs the Layer-2 autonomy-no invariant — a hub that pushes running hooks into consumers on a schedule brushes against "hub initiates no autonomous cross-repo writes." This is genuinely contested + high-stakes + no-obvious-answer → the located moment for a Fable consult. Fable RULES, CC IMPLEMENTS.
Which organs even belong locally. JOURNAL hard-block clearly should fire in-consumer. But git_backlog_drift and the coherence spine may be inherently hub-scoped (cross-repo reconciliation). The per-organ local-vs-hub call is part of the design, not a given.
Informant Organ scope. Read-only coverage reporter (per-consumer × per-organ: enforcing-local / absent). Low-regret, buildable independently of the mesh-model decision — but its file path is a new-path decision requiring operator approval.

3. Considered + rejected (do NOT relitigate)

"It's an ai-council incident" → rejected by evidence. The fleet-map proves 5/5 ABSENT across all 4 consumers. Fleet-wide, systemic. Any fix must be fleet-wide, not an ai-council patch.
"The system is broken" → rejected as framing. The mesh was never built, not broken. The rest of the hub (coherence spine, ship-gate, floor, ADR lifecycle) is verified-working. This is a missing carrier with clear options, not a failed system.
Onboarding monorepo now → rejected / correctly deferred. monorepo was deliberately sequenced last precisely so this class of gap would surface on the n=1 pilot (ai-council) first. It did. Onboarding monorepo through the current deploy subsystem would inherit the same gap — do NOT onboard it until the mesh carrier + Informant Organ are proven.
Prior-window rejects still stand: floor Model B; in-place-fragment decouple; escalating routine builds to Council.

4. Open questions

Mesh-model A/B/C — to Fable.
Per-organ local-vs-hub assignment.
Informant Organ file path — operator approval (new path).
Does #139 (merged-arc→record) + #170/#168 (arc-tracking spine) fold into the same work-stream? Likely yes — arc-tracking and enforcement-transfer are adjacent record-integrity families.
The #168-hard vs Fable-WARN conflict surfaced in consult #1 (#168's Done-when says promote JOURNAL leg to fail-closed HARD; Fable ruled arc-tracking stays WARN with no-item disposition) — unresolved.

5. Decomposition rationale — why this shape
Four steps, dependency-ordered: (0) stabilize live → (1) fleet-map → (2) Informant Organ → (3) mesh carrier → (4) record the lesson. Steps 0 and 1 are DONE this window (ai-council JOURNAL-backfill instruction sent to that repo's architect; fleet-map complete). The next session starts at step 2/3.
Why Informant Organ (2) before mesh carrier (3): it is low-regret (read-only, no constitutional change) and correct regardless of which mesh-model wins — you need enforcement-coverage visibility no matter what. Building it first also gives the mesh work its acceptance signal (the fix is "done" when the Informant Organ shows enforcement-local green).
Why Fable is warranted for (3) specifically: it clears the routing bar (contested + high-stakes + no-obvious-answer + a Layer-2-invariant tension), unlike consult #1's already-optimized forks. Feed it the fleet-map, not an n=1 sample.
What the next session must NOT redo: the fleet-map (step 1); the #170/#168 classification; the register cleanup. All sealed this window.
6. Off-repo context

Priority is re-scoped by the finding. The prior supplement's three-goal priority (Fable → ai-council-query → close methodologies) is demoted below the enforcement-mesh gap. The mesh gap is P0; the three goals are sequenced-after. (Per point A: nothing else changed the priority this window — but the CC-verified enforcement finding did, and it dominates.)
Consult #1 (Fable) is spent and its rulings are pending-disposition, un-merged — the re-scope to vision/recovery halted the disposition pass. The accepted-but-unmerged rulings are: leg-(e) functional-proof into ADR-81; undeclared-edge scan → ship-gate WARN; immutability re-scope (status-line mutable on ratification, decision-content frozen) — operator sign-off pending, it narrows core-invariant #5; ai-council wiring lane-split (architect frames, CC mechanically expands). These must not be lost — fold them into the next session or they die in the outgoing chat.
ai-council wiring (/council via the plugin carrier) was designed, not built — browser→CC→ai-council, CC owns the mechanical lifecycle, architect owns question-framing. Sequenced after the mesh gap.
Fable is a time-boxed / possibly export-restricted preview. One consult spent. The mesh-model ruling (step 3) is the highest-value remaining use of the window.
