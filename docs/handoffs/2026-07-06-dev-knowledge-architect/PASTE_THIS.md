=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-06-dev-knowledge-architect` |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Plan the **post-priority-#1 frontier.** With the hub proven **enforcing** on a real consumer (ai-council measured FULL-COVERAGE, priority-#1 CLOSED) and the consumer-onboarding loop now repeatable (`templates/consumer-onboarding-runbook.md`), the central open decision is whether the n=2+ **fleet-roll WAIT is lifted** and how to sequence it (#221 / #244 P6) — alongside closing the enforcement-transfer epic's doctrine half (#238) and the Wave-3 refinement (#267). A **way-of-working / sequencing** session: start from `BACKLOG.md` (Cross-repo universalization + the enforcement-transfer mesh epic), not a single-task execution.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/2026-07-06-architect-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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
reconciled_with: handoff-process@5.5
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

# Residual — 2026-07-06-dev-knowledge-architect — the part the repo does not already encode

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
Authored **recall/inferred** from the JOURNAL window (Wave-2 root + Wave-3); re-derive every value live via `PROBES.md` **P7/P4/P6/P2**. **No new drift class this window.**

**Standing dispositioned set (unchanged in class — see `ecosystem/disposition-register.yaml`):**
- `git_backlog_drift` — the **#77** voided-closure false positive (a misattributed closing sha vs an operator-ruled keep-open). Standing; do not touch.
- `no_ff_merges` — the journal-wrap / transcript-archive direct-to-`main` class; **#210** proposes converting it to a path-scoped standing exemption. This handoff's own JOURNAL wrap may add one more instance of the **same** class — re-derive via P7, do not read it as a new regression.
- `undeclared_edges` — the 6 `…→handoff-process` prose edges (BACKLOG / VISION / AI_COUNCIL_PROCESS / ESSENTIALS / PLAYBOOK / SESSION_SETUP), dispositioned under **#241**.

**One structural change this window (NOT a drift):** Wave-2 **retired audit check #7** (`mermaid_theme`, ADR-51 amendment 2026-07-05), so `ALL_CHECKS` shrank by one and `ecosystem/doc-counts.md` was regenerated once. The live count + last-registered check **name** are **P2**'s answer (withheld here).

**Informational legs (by design — never FAIL/WARN):** `deployed_methodology_version` (ai-council carries a deployed version, the hub's own entry stays null; the linked-worktree-dirname keying artifact is **#265**) and `enforcement_coverage` (read-only — per-consumer truth is the sandbox `--fire` measurement, not this leg).

_No `[stale]` disposition is asserted here — **P7** re-derives the GREEN/RED verdict + the dispositioned-WARN count + any `[stale]` line over live git ∩ `main`; do not trust this prose._
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Two waves landed since the last architect bundle (`2026-07-05-dev-knowledge-architect` — an overnight scaffold cut *before* Wave-2 integration, FILL-INs never authored). **recall/inferred** — re-derive load-bearing values via `PROBES.md`; the JOURNAL top ~6 entries encode the detail. All on `main`; nothing on a feature branch except **this** handoff branch + the routine `automation/fleet-audit` data branch (**#254**).

**Wave-2 — root integration (2026-07-05; ADR-97 tree-orchestration, loop-closes-at-root):** three epic lanes merged serial `--no-ff` — **test-tiering** ([#260]/[#256]/[#257]: /ship pre-flight parallel + diff-shaped `live_repo` selection), **doc-consolidation** ([#258]: ESSENTIALS→charter trim, PLAYBOOK-absorb, CLAUDE.md generability seam), **llm-first-docs** ([#259]: zero-Mermaid ARCHITECTURE, compact-text codemap, **check #7 retired**). **ADR-51 amendment 2026-07-05** ratified (LLM-first canonical docs). 5 tasks closed; follow-ups **#262–#266** filed; doc-counts regenerated once. → `JOURNAL.md` 2026-07-05 root entry.

**Wave-3 — prove the hub on ai-council like a sandbox (2026-07-06; priority-#1 CLOSED):** the `deploy/lived_sandbox/` observer (Slice B) measured ai-council **before 1-of-6 FIRED → after FULL-COVERAGE** (4 FIRED incl. `session-end-backpressure` BLOCKING the child's stop + 2 ARMED-BUT-SKIPPED as correct file-scope behavior), **GATE-0 PROVEN**, **zero consumer-side changes** (every gap instrument-side — measure-first vindicated). Instrument hardening **G1–G7** + two **Codex** passes (0 CRIT). Shipped `templates/consumer-onboarding-runbook.md` (advances **#238** runbook half); filed **#267** (scope-exercising refinement); noted **#238**; +2 **LESSONS** trust-seam proof points; filed the ai-council relative-path fragility pointer for its dedicated chat (ADR-41). → `JOURNAL.md` 2026-07-06 ×3 · `docs/audits/2026-07-06-*`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The re-sequenced program (2026-07-04 supplement — **read it**: `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md`) was **Phase 0 safety → Phase 1 sandbox as the retroactive acceptance instrument → Phase 2 fleet re-gated**, with **P5/P6 held WAIT** while the corpus was moving. Wave-2 stabilized the corpus (three epics integrated) and Wave-3 delivered the Phase-1 payoff (priority-#1 CLOSED — the hub proven enforcing on a real consumer). **The frontier is Phase 2.** The outgoing chat's strategic *why* is **now in `SUPPLEMENT.md` (FILLED)** — its ANSWERS are folded into `PASTE_THIS.md` below; read them for the operator's own framing of Phase 2 (a consolidation wave + the undesigned functional/technical-architect intake process), which supersedes any tag-uncertainty in this CC-derived residual.

### (1) PRIMARY — the fleet-roll sequencing decision (#221 / #244 P6)

The WAIT's two preconditions have moved: the corpus stopped moving (Wave-2) and the sandbox is now the **proven** acceptance instrument (Wave-3, ai-council n=1 FULL-COVERAGE, repeatable via `templates/consumer-onboarding-runbook.md`). **Open decision: is the P5/P6 WAIT lifted, and if so what is the n=2 sequence?**
- **Inputs/gates (verify each live in `BACKLOG.md`):** #221 MUST follow **#225** (comment-preserving surgical precommit carrier — still open) and pairs with **#262** (child codemap migration to compact text); each deploy uses the **#230** conformance self-test as its acceptance gate + the new runbook; **#226** arming already satisfied (2026-07-02); ADR-41 routes each child deploy to its **dedicated chat**, not the hub.
- **The call to make:** pick the first n=2 consumer (corp-monorepo / corp-ops / corp-sca-time-automation) and the residual-close order — or record that the WAIT stays, with the reason.

### (2) Close out the enforcement-transfer epic (#238 doctrine half + Stage-3 adjudication)

Wave-3 proved hub enforcement **fires** on ai-council; two halves remain:
- **[#238] Stage 4 — doctrine half (open; runbook half shipped Wave-3, root-ratified 2026-07-06):** write into **LESSONS + PLAYBOOK** the "deployed *presence* ≠ deployed *enforcement*; done only on enforcement-in-effect (configured→armed→proven, generalized to the mesh)" doctrine + the repeatable deploy-and-re-verify runbook reference.
- **Adjudicate Stage 3 (#236/#237 mesh carrier) — VERIFY-FIRST, don't assume closed:** does the FULL-COVERAGE proof (enforcement fires consumer-local on ai-council, via the already-deployed v1.2.0 corpus) *close* Stage 3, or is the measurement orthogonal to the carrier's port? Check the live BACKLOG state and decide.
- **[#267] P2 — refinement, NOT a closure gate (root ruling: armed-as-enforcing not adopted as doctrine):** extend the ai-council arc with an in-scope edit to witness `hub-toc-hooks` + `floor-hash-verify-hook` **FIRED** (currently ARMED-BUT-SKIPPED — the single-file arc never matched their `files:` scope), and encode the scope-conditional `engages:` entries.
- **FLAG (architect's call — do NOT fold unilaterally):** whether #139 / #168 / #170 (arc-tracking / record-integrity) fold into this epic. My read matches the standing BACKLOG FLAG: **#168/#170 adjacent** (they harden the same `session_end_backpressure` organ #237 ports consumer-local), **#139 tangential** (hub record-integrity). **#243** (the #168-hard vs Fable-WARN conflict) resolves at/after this adjudication.

### (3) The carried methodology reviews' remaining halves

- **RF-1 (handoff anti-bluff) — spec half LANDED:** the structural withhold + the spec amendment both shipped (**v5.4** §5 structural anti-bluff, **v5.5** §14 epic handoffs; `9d5ebe5`). Remaining: the **first bluff-dogfood re-run** since the 2026-06-11 promotion — **this very bundle is the candidate** (it withholds every probe value by construction; try to answer P2–P9 from the compaction summary alone — every probe must fail to be bluffed).
- **RF-4 — CLAUDE.md §5 "handoffs/audits immutable" vs the §13 SUPPLEMENT fill/fold lifecycle:** a standing doctrine contradiction; reconcile to the **ADR-94** status-line-mutable precedent or carve a §13 exception. Coincides with **#157** (intra-CLAUDE.md §4/§5 file-lifecycle restatement) + **#112** (the §5 supersede-vs-never-edit fix).
- **RF-5 / #220 — MODIFY / semantic-drift axis:** VERIFY-FIRST whether any organ gates a meaning-change-without-version-bump (the two doc↔doc walkers' corpus-scope disagreement rides here); establish a demonstrated-catch bar before any design.
- **#159 (RF-3b):** the boot-transcript echo that could close #159 on evidence — **this architect handoff, if the operator runs `supplement filled`, is exactly #159's Done-when** (the incoming §13(d) beat exercised against a *filled* supplement).

### (4) Held / standing debt (do NOT advance without an explicit operator unlock)

- **ai-council relative-path pre-commit fragility (off-repo):** `repo: ../.dev-knowledge` in ai-council's `.pre-commit-config.yaml` breaks ANY out-of-layout checkout (CI, second clone, the sandbox clone — witnessed in measurement-3). Filed as a **pointer** in the BACKLOG ai-council-residuals block for the **ai-council dedicated chat** (ADR-41) — decide pin-by-URL+rev vs documented layout constraint there, NOT in the hub.
- **ai-council CLAUDE.md A2-stale (off-repo, LIVE):** `last_reviewed` < last edit; the now-deployed `canonical_freshness` gate **will block ai-council's next real commit** until a **genuine** re-review + re-stamp (never a faked stamp) — the transferred organ dogfooding itself in a consumer.
- **Deploy-arc residuals:** **#225** (surgical precommit carrier — also gates #221), **#233** (deploy-index test tempdir isolation — the xdist flake), **#247** (Rich markup swallows `[#id]` in the tombstone print), **#245/#246** (add-path `status: removed` awareness / hub-toc-hooks retirement).
- **Corpus growth (ADR-class calls):** **#212** (`docs/handoffs/**` retention/rollup — 400+ immutable bundles, the single largest growth vector), **#213** (PLAYBOOK rule/history condensation).

### Pointers (open the primary source; do not trust a paraphrase)
- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **The strategic frame (READ FIRST):** `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md` (the filled re-sequenced program) — this residual sits inside it.
- **The Wave-3 evidence:** `docs/audits/2026-07-06-ai-council-measurement-3.md`, `templates/consumer-onboarding-runbook.md`, `deploy/lived_sandbox/` (the observer), `JOURNAL.md` top-3.
- **Task-graph:** `BACKLOG.md` — Cross-repo universalization (#221/#244/#262) + the enforcement-transfer mesh epic (#235–#240, #267) + Handoff continuity (#159/#161/#164).
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
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
> **Branch note.** This bundle was generated on branch `docs/2026-07-06-architect-handoff`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **Windows note:** `audit.py checks` (P2) can crash mid-listing on a bare cp1252 PowerShell console
> (a non-ASCII glyph in a check docstring) — run with `PYTHONUTF8=1` or in git-bash. `ship-gate` (P7)
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
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what dev-knowledge is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-06-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-06-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-06-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d).** Then run P2–P9, each against
   **live state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state**. First check
   which branch is live (P3), then re-derive every load-bearing fact from the live primary source.

---

=== SUPPLEMENT.md ===

# SUPPLEMENT ANSWERS (enriched) — outgoing architect wrap · 2026-07-06
# Paste into the outgoing bundle's ANSWERS region (replaces the earlier compressed draft).

## Q1 — Strategic intent (way-of-working level)
The session closed the ecosystem's central claim: enforcement-in-effect is now a MEASURABLE property with a runbook (measure → attribute → complete → re-measure), proven end-to-end on ai-council (1/6 → FULL-COVERAGE, ZERO consumer-side changes — every gap was instrument-side). The next session's way-of-working goal is two-part:
(A) CONSOLIDATION WAVE from the operator's audit list: universalize epic-naming across repos (hub ADR-66 story-map vs ai-council "Epic A/B/C" — one convention or none); child-repo Mermaid migration (#262); References sections in CLAUDE/CONTRIBUTING → generability phase 2; ENVIRONMENT.md retire-or-own (stale ~06-03); audit proliferation → an audit-index/retention rule; transfer Epic-5 test tiering to consumers (ai-council check.ps1 got nothing — tiering is methodology, ship it via the deploy pipeline).
(B) DESIGN THE INTAKE PROCESS the operator sketched: functional architect (gathers requirements, writes intake) → technical architect (owns backlog + ADRs, cuts §14 epic handoffs) → epic browser-chats (one epic each, to completion). Lands in PLAYBOOK as methodology; ai-council wired for genuinely contested forks. This is the operator's explicit ask and UNDESIGNED.
Only after A+B: P6 fleet roll — its WAIT condition (sandbox as acceptance instrument) expired this session; its own gates #225/#249/#250 stand. Phase-2 rot-report equally UNLOCKED (defer-until-after-sandbox expired) — it is the designed answer to the operator's dead-code/redundancy concern; build it rather than hand-sweeping.

## Q2 — Tensions weighed (where landed, why)
- Measure-first vs assume-gaps (Wave 3): measure-first; vindicated — the assumed "mesh completion 1/6→6/6" was a phantom; consumer was healthy, instrument was blind.
- Authorization channel (G3): prompt self-legitimization vs owned-config; CONFIG won — a deployed floor CORRECTLY refuses prompt-asserted authority (witnessed: the child refused the arc as injection citing ai-council's own floor). User-config is the principal's channel; ex-ante standing consent satisfies "ask before destructive" without weakening the floor.
- Armed vs fired (#267): armed-as-enforcing REJECTED as doctrine; file-scoped hooks correctly skipping out-of-scope diffs is correct behavior, not silence. #267 = refinement (in-scope arc edit + scope-conditional engages:), not a closure gate.
- Epic ceremony vs serial: worktree-per-EPIC (not per-story), 2–3-lane cap, root-only merges, file-boundaries adjudicated at spawn — held through two waves incl. self-application (Epic 2 refused BACKLOG-structure edits citing the ADR it was integrating).
- Plan-mode vs execution (operator finding, CONCEDED): plan-first was used at genuine forks (Slice B plan — surfaced two forks; consumer seam) but Waves 2–3 defaulted to EXECUTION and §14a carries no MODE field. Real drift from PLAYBOOK. CORRECTIVE (do early, small): §14a template gains a mandatory Mode row; L-sized epic stories default plan-first; every architect prompt re-declares MODE.
- Autonomy boundary (overnight): execute pre-authorized contracts YES / design decisions NO — held; Block A DEGRADED honestly on a real GATE-0 confound rather than improvising past it; zero safety-envelope violations unattended.

## Q3 — Considered + rejected (do not relitigate)
Hand-copied mesh transfer (deploy pipeline only) · armed-as-enforcing · splitting the 90s E2E test (budget "~2min" met per #256's own framing) · LLM-gating semantic properties · sibling-dir worktrees · AI Council for CLAUDE.md quality (architect review + generability epic was right) · prompt-prose authorization for sandbox children · Task-Scheduler auto-resume harness (FAILED in practice: never fired the resume; clean-tree gate + untested wake path; manual git-boot re-paste is the reliable resume — treat re-automation as a fresh design, not a retry).

## Q4 — Open questions (unresolved / deferred)
- Intake process shape (Q1-B) — undesigned; needs PLAYBOOK section + intake template; how the audit corpus feeds it (operator flags audit proliferation; consider audit-index + retention).
- Epic-naming universalization (fleet-wide convention pick).
- Test-tiering transfer to consumers (hub-only today).
- ENVIRONMENT.md purpose · child Mermaid #262 · References generability · #267 · #254/#255 · #261 (generator slug) · #263–#266 · content-echo doctrine follow-through.
- Vault V1–V5/OM1–4 sign-off: corp-monorepo audit merged (32b4e20) — OPERATOR ratification in a corp-OS session; pointer only, do NOT pull into hub scope.
- Plan-mode corrective (Q2) — first small move.

## Q5 — Decomposition rationale (do not redo)
Dependency-gated waves: instrument before consumers (sandbox = the acceptance instrument), measure before complete (killed a phantom workstream), §14 rails before the 3-lane wave that ran on them, merge order 5→3→4 (ship speedup first; Epic-4's stale loci fixed against post-Epic-3 text). Sealed: C4 closure + fixtures · G3 config-channel trust seam · ADR-51 amendment + check-#7 retirement · ADR-97 · Epic-5 tiering rulings · the operator-approved ESSENTIALS deletion list · priority-#1 closure declaration (8e1dd57).

## Q6 — Off-repo context + the honest ledgers
EVIDENCE SPINE: main a523fca → fb11266 (~25 --no-ff merges, all pushed); suite 1216 → 1323 tests; closed #251/#252/#253a–d/#256–#260; filed #254/#255/#261–#267; ADR-97 new, ADR-51 amended, HANDOFF_PROCESS 5.3→5.4→5.5; ESSENTIALS 448→174 lines; /ship docs-only 9m42s→~34s, code ~2min; ai-council 1/6→FULL-COVERAGE with IDENTICAL consumer HEAD before/after.
INCIDENTS THE INSTRUMENT CAUGHT (methodology wins, on record): ai-council's relic core.hooksPath had EVERY git hook silently bypassed since the repo move (found+repaired mid-mission); the ruff tombstone prune-proof was false-green ("already absent" while ruff ran); the content-echo channel class (repo files quoting signatures leak into tool_result echoes); a deployed floor refusing prompt-asserted authority; the child declining git commit --no-verify at a failing gate under a narrowed allowlist.
ARCHITECT DEFECT LEDGER (the outgoing session's own error rate — trust the mechanism, not the architect): four contract-authoring defects (item-1 RF-1 mislabel; nonexistent docs/adr/ path; S2 bump-vs-boundary contradiction; E4-1 missing tests path) — ALL caught downstream by lane escalation or the fidelity check; plan-mode drift (conceded above); the overnight relaunch harness failure; one mid-session thread-sprawl episode (fixed by hermetization + a STOP rule: nothing new opens until the current wave closes — keep the rule).
OPERATIONAL: API credits funded (negative balance found 07-05; sandbox children bill API credits, NOT the Max subscription — by design of the isolation seam). CC update pending 2.1.177→2.1.200 (native; all claude.exe must exit first; one 14h --dangerously-skip-permissions terminal from the overnight window flagged for conscious close). Overnight-harness scheduled task unregister pending (needs elevation). No LLM-budget ceiling.
