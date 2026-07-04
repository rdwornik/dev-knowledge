=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-04-dev-knowledge-architect` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **The [#244] essence-spec lifecycle epic is BUILT: P1→P4 all SHIPPED this window (the prior handoff resumed at P2 — this window ran P2→P3→P4 to completion, n=1 proven throughout).** The deploy engine gained a **remove leg** (ADR-96) and pruned a real component from ai-council (verified ABSENT, locally-modified REFUSED); the **methodology roster is now machine-generated** (CLAUDE.md §9 `@import`, Fable R3 closed); the **Informant gained a Tier-3 drift classifier + fleet drift line** (seb inject→DRIFT→rejected-non-waivable proven). Deployed methodology **v1.2.0 to ai-council** (tag `v1.2.0`). Only **P5 (hub self-prune #130) + P6 (fleet roll n=2+ #221)** remain of the epic. **Separately — and this is the real work of the next session — four Fable read-only reviews LANDED** (analysis-only, all merged, nothing acted on): **handoff-adoption** (headline **RF-1: the anti-bluff probe contract is INVERTED — every architect bundle including THIS one prints probe answers as `expected:` hints; the bluff-dogfood never re-ran**), **coherence-spine** (inverted investment + demonstrated self-blindness + the RF-5 FAIL-trap), the **rot-algorithm design** (build-it-small; the home for the operator's continuous-conformance vision), and the **Fable-5 architecture review**. **The next session is an ADJUDICATION session, not a build one:** (1) route the four Fable reviews' findings (RF-1 is meta-urgent — it indicts this very handoff mechanism); (2) sequence the epic tail P5→P6 (P6 gated on #225, and on NOT onboarding a consumer through a soon-to-change corpus); (3) decide build-vs-defer on the rot-algorithm / continuous-conformance vision; (4) clear the LIVE standing debt — ai-council's `CLAUDE.md` is A2-stale and the now-deployed freshness gate WILL block its next commit (a real re-review, never a faked stamp). |
| **Generated at** | Bundle cut on branch `docs/2026-07-04-architect-handoff` **off `main` (`25b104e`)**, working tree **clean**, `main` **in sync with `origin/main`** at generation. **All epic work is on `main`** — no parallel feature branch this window (contrast the prior `feat/essence-spec-p1`). This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **`SUPPLEMENT.md` is generated EMPTY.** The bundle is assembled by CC from committed repo state; the
> operator may fill the supplement from the outgoing architect chat (`supplement filled`) so its ANSWERS
> fold into `PASTE_THIS.md`, or leave it empty for a cold handoff (the defined §13 disposition). **Until
> filled, the incoming §13(d) operator-context beat fires FULL** (a full off-repo ask), not the narrowed
> *"anything changed since?"*.

> **RF-1 corrective in effect (read `PROBES.md` header).** Because the Fable handoff-adoption review
> found that every recent bundle prints its probe answers as `expected:` hints — inverting the §5
> anti-bluff contract — this bundle **deliberately withholds the probe answer values** (no counts, SHAs,
> dates, verdicts, or orienting lines). Whether the drift-reference hints should return is itself an open
> §4 decision (RF-1). The withholding IS the teeth; run the commands.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (the 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

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

# Residual — 2026-07-04 architect handoff — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This window CLOSED the [#244] essence-spec lifecycle epic P1→P4.** The prior
> `2026-07-03-dev-knowledge-architect` handoff resumed the epic at **P2 (PRUNE)**. This window ran
> **P2 → P3 → P4** to completion: the deploy engine gained a **remove leg** (ADR-96) and pruned a
> real component from ai-council (verified ABSENT, locally-modified REFUSED); the **methodology
> roster is now machine-generated** (CLAUDE.md §9 `@import`, Fable R3 closed); the **Informant
> gained a Tier-3 drift classifier + fleet drift line** (n=1 seb inject→DRIFT→rejected-non-waivable
> proven). Deployed methodology **v1.2.0 to ai-council** (tag `v1.2.0`). Only **P5 (hub self-prune,
> #130) + P6 (fleet roll n=2+, #221)** remain of the epic.
>
> **Separately, three Fable analysis-only audits + one Fable-5 architecture review LANDED** (all
> merged, nothing built) — and they are the **real architect work of the next session**: the
> handoff-adoption review, the coherence-spine review, and the rot-algorithm design each surfaced
> meaty methodology findings that need **architect adjudication + routing**, not execution.
>
> **`SUPPLEMENT.md` is generated EMPTY** — the operator fills it from the outgoing architect chat
> (`supplement filled`) or leaves it empty for a cold handoff (§13 disposition). Until filled, the
> incoming §13(d) operator-context beat fires **FULL**.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the
> load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-04-architect-handoff` off `main` `25b104e`, tree clean, in sync with `origin/main`).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and CLEAN; **10 WARN dispositioned, NO `[stale]` line**

`python scripts/audit.py ship-gate` → **GREEN** (**10 WARN dispositioned**, **NO `[stale]`**) —
verification organs green against the `main` arc. The 10 dispositioned WARNs are the **same
standing set** as the prior handoff (no new regression this window):

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) — **expected seam, not a regression.** **#210** (open) proposes converting
  this class to a standing rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap).
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241** — the standing declare-vs-defer adjudication. **The Fable coherence-spine review (RF-4)
  argues these 6 are major-granularity edges mis-served by an `@5.3` remedy — a §4 decision.**

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the
  methodology source; its own entry stays null. **ai-council** now records **`1.2.0`** (`source_tag
  v1.2.0`, `deployed_date 2026-07-04`) in `ecosystem/deployed-versions.yaml` — moved 1.1.0→1.2.0 by
  this window's **P2 prune deploy**. corp-monorepo / corp-ops / corp-sca-time-automation still `null`
  (P6 fleet not yet run).
- `enforcement_coverage` (`[--]`) — the Informant's static leg is **read-only, never FAIL/WARN**;
  per-consumer coverage is measured by `scripts/enforcement_coverage.py --fire` (the fire test is the
  truth-maker, not this leg). **New this window:** the Informant now also carries a Tier-3 drift
  classifier + `static_drift_summary` (no-clone/no-fire snapshot).

_(No `[stale]` disposition. This is a clean gate — the whole §1 is standing flags, no new regression.)_

---

## §2 — Shipped this window (prior `-architect` bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~10). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`. **All on `main` (`25b104e`)** — unlike the prior
handoff, nothing is left on an unmerged feature branch.

**The [#244] essence-spec lifecycle epic — P1→P4 SHIPPED (the sealed backdrop; do NOT redo):**
- **P1 essence-spec v1 + release-lint** (merged `b65c760`): the prior handoff's immediate review
  item. Spec-path (**in-place absorb-not-pair**) was **APPROVED** by the outgoing architect and
  merged; `manifest-v1.1.0.yaml` grew `anchors:`/`components:`/`doc_shapes:`, `deploy/release_lint.py`
  reconciles all 5 version anchors to `source_tag` (C1–C7), 27 golden-diff/teeth tests.
  Behavior-preserving (golden-diff IDENTICAL). release-lint stays **manual** (preflight wiring
  correctly deferred).
- **P2 PRUNE — the deploy remove leg** (ADR-96; merged `2c86951`; deploy record `86aec77`): the
  add-only engine gained `detect_prune`/`prune`/`verify_pruned` (`deploy/contract.py`), the
  `carrier_precommit` remove leg (hash-guarded whole-entry removal), manifest `removed_in`/`reason`/
  `prune` schema with `ruff-gate` flipped to `status: removed`, `release_lint` C6 unlocking `removed`,
  and a Terraform-style destroy-confirm in `tool.py`. **Tagged `v1.2.0`; PROVEN n=1 on ai-council** —
  `ruff-pre-commit` **pruned + verified ABSENT**, a **locally-modified target REFUSED**
  (`PRESENT_MODIFIED` → abort, no record), non-pruned surface byte-identical. **First deleting phase —
  autonomous deletion stays forbidden; consumer-invoked + staged + hash-guarded only.**
- **P3 generated methodology roster** (merged `a750456`): Fable **R3** closed (consumer CLAUDE.md
  rosters were hand-prose → rot). The deployed corpus is now machine-generated from
  `deploy/manifest-v*.yaml` `components:[].roster` into `.claude/methodology-roster.md`, `@`-imported
  via CLAUDE.md §9; `gen_methodology_roster.py` + a blocking `roster-freshness` gate. Generated file
  is deliberately OUT of `DEFAULT_FRESHNESS_FILES` (currency = regen). FU **#248** (hub-local-source
  registry), **#249** (`@import`-edge coverage gate).
- **P4 sync surfacing** (merged `25b104e`): the Informant gained a **Tier-3 drift classifier**
  (`classify_tier3` over Tier-1, allowlist-driven `.methodology.yaml` at the consumer root),
  `static_drift_summary` (no-clone/no-fire), and a **fleet_health per-consumer drift roll-up line**.
  **n=1 demonstrated-catch:** a seb divergence **INJECTED** into an ai-council clone → **DRIFT** → a
  valid but **non-waivable** allowlist entry → **STILL DRIFT (rejected-non-waivable)**. Version
  **HELD 1.2.0** (the `waivable:` field is inert to `deploy/tool.py`). FU **#250** (codemap-freshness
  has no `components:` entry → a P6-coverage gap).

**Four Fable read-only reviews LANDED (analysis-only, all merged — nothing built; §4 is where they go):**
- **Fable handoff-adoption review** (`132c5c9`, `docs/audits/2026-07-04-handoff-adoption-review.md`):
  9 red flags on the v5 handoff surface. **Headline RF-1: the anti-bluff probe contract is INVERTED**
  — every recent architect bundle prints its probes' answers as `expected:` hints, which §5 says are
  "rejected"; the bluff-dogfood ran once at promotion (2026-06-11) and never again; hint-count crept
  1→11. **This bears directly on the bundle you are reading** (see §4 + `PROBES.md` header — I
  minimized `expected:` hints here as a first corrective). RF-2 (#164 generator unbuilt → every
  bundle hand-copied), RF-3 (#159 browser-side contract structurally unwitnessable), RF-4 (CLAUDE.md
  §5 "handoffs immutable" contradicts the §13 fill/fold lifecycle).
- **Fable coherence-spine review** (`5d87838`, `docs/audits/2026-07-04-coherence-spine-review.md`):
  **inverted investment** (heaviest machinery on the least-drifting axis; ESSENTIALS↔PLAYBOOK drift
  has zero mechanized edge) + **demonstrated self-blindness** (3 canon surfaces call the
  undeclared-edge scan "not in gate" a day after it was wired) + RF-5 latent FAIL-trap (the two
  doc↔doc walkers disagree on corpus scope) + the shared **presence-not-currency** blind spot (#220).
- **Fable rot-algorithm design** (`493fccb`, `docs/audits/2026-07-04-rot-algorithm-design.md`):
  designs `scripts/rot_report.py` — a nightly zero-LLM reverse-reference multimap + 3 existence
  predicates (dangling-path / dangling-wiring / tombstone blast-radius) + `--impact` pre-deletion
  query. **Verdict: build it, but small — assembly over existing primitives.** Implements #169's
  intent; feeds #244 P4/P5; the natural home for the operator's continuous-conformance vision.
- **Fable-5 architecture review** (`d319df9`, merged `22a5a22`,
  `docs/audits/2026-07-04-comprehensive-...` per the prior handoff's demoted-goal input): the
  whole-system review — the prior three-goal priority's (a) item.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — on `main`: **7 themes, 23 stories, 107 tasks** (witnessed via
  `validate_backlog`). The `[#244]` epic now records **P1/P2/P3/P4 SHIPPED**, P5/P6 remaining. The
  spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (all epic work integrated), this handoff
  branch `docs/2026-07-04-architect-handoff`, and `automation/fleet-audit` (a routine baseline branch,
  unmerged — separate concern, **leave**). **No unmerged feature branch this time** (contrast the
  prior handoff's `feat/essence-spec-p1`). No merged stragglers left to `-d`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9):
  **code-edge = just `#218`**; **coherence = `#180/#181/#182/#220/#241`**; **audit-py group =
  `#242/#153/#7/#36/#95/#139/#166/#190/#210/#234/#243/#240`**. The **new follow-ups** from this
  window (#245/#246 P2, #248/#249 P3, #250 P4) are filed but their graph edges are light — open the
  file for placement.

---

## §4 — The next frontier (open architecture decisions)

**The build epic is essentially done; the next session is an ADJUDICATION session, not a build one.**
[#244] P1–P4 shipped and proved (n=1); what remains is (1) **routing the four Fable reviews' findings**
(the meaty methodology work), (2) sequencing the epic's tail P5/P6, (3) the continuous-conformance
build decision, and (4) a live standing debt. **recall/inferred** — the architect resumes here; the
outgoing chat's strategic *why* fills `SUPPLEMENT.md`.

### (1) IMMEDIATE — adjudicate + route the four Fable reviews (the real architect work)

Four analysis-only reviews landed this window; **none acted on any finding** (by mandate). The
architect's first job is to triage and route them. Highest-stakes, in order:

- **RF-1 (handoff-adoption) — re-ratify or retire the anti-bluff probe contract. META-URGENT: it
  indicts THIS handoff mechanism.** §5 says a probe that ships its answer is "rejected"; every recent
  architect bundle (including this one, minimally) prints `expected:` hints. Either the hints are a
  legitimate *drift-reference* (the spec's current framing) or they inﬂate the contract (Fable's
  claim). **Decide + record**, and if the contract stands, **re-run the bluff-dogfood** (it has not
  run since promotion). This is the one finding that changes how the *next* handoff is generated.
- **RF-3b (handoff-adoption) — the boot-transcript echo that could close #159 on evidence.** The
  browser-side contract (#159) is unwitnessable because the exercise happens in a chat the repo can't
  see; RF-3b proposes an on-load echo the repo *can* capture. Cheap, closes a 12-supplement-old
  unclosable ticket.
- **Coherence-spine "demonstrated self-blindness" + RF-5 FAIL-trap.** 3 canon surfaces mis-describe a
  live gate; the two doc↔doc walkers disagree on corpus scope (handoff bundles' embedded
  `reconciled_with` escape the gate only by an assembly-format accident). Correctness bug in the
  coherence mesh — worth a fix pass.
- **RF-4 (both reviews) — CLAUDE.md §5 "handoffs immutable" vs the §13 fill/fold lifecycle.** A
  standing doctrine contradiction the fill/fold practice already violates. Reconcile the rule to the
  ADR-94 status-line-mutable precedent (or carve a §13 exception).

### (2) Sequence the epic tail — P5 (hub self-prune) → P6 (fleet roll n=2+)

- **`#130` / P5 — hub self-prune:** the hub prunes its **own** tombstoned components (dogfood the
  remove leg on the hub, not just a consumer). Next epic phase; Opus, plan-first.
- **`#221` / P6 — fleet roll n=2+:** Axis-1 proven n=1 (ai-council @ v1.2.0); run `deploy/tool.py` on
  corp-monorepo / corp-ops / corp-sca-time-automation. **Carry the pilot rule** (LESSONS 2026-07-03):
  treat each consumer's `.gitignore` + config shape as an **UNKNOWN to probe, not a copy of the hub**
  (the gitignore defect that halted the ai-council deploy). **Gated on `#225`** (surgical precommit
  carrier) closing first; FU **#250** (codemap-freshness component) + the rider-2 coupling warning
  become live here. **Do NOT onboard a new consumer through a soon-to-change corpus** — if RF-1/RF-4
  or the rot-algorithm build will move the methodology, sequence P6 after.

### (3) The continuous-conformance build decision (the rot-algorithm)

The Fable rot-algorithm design (`493fccb`) is **landed as a design doc, not filed as a build.** It
maps directly to the operator's **continuous-conformance vision** (prior supplement §6: Opus
decomposes → cheap Sonnet observers do per-file binary rot-checks). **Decision:** file it as a
BACKLOG build item with an ex-ante ADR-81 contract + a ratifying ADR (the design's own "Next"), or
defer. Implements #169's intent; the layer *above* P4/P5 where manual release-lint gets wired.
Same-day the design flagged **two stale P1-era comments** (manifest-v1.2.0 header L40-43, release_lint
docstring) + P4 flagged a **stale `enforcement_coverage.py` docstring** (seb "reported absent" is now
false for a v1.2.0 consumer) — small doc-currency fixes the rot-report would itself surface.

### (4) Standing debt (off-repo, LIVE consequence) — ai-council CLAUDE.md re-stamp

ai-council's `CLAUDE.md` is genuinely A2-stale (`last_reviewed` < last edit). The now-live **deployed**
`canonical_freshness` gate **WILL block ai-council's next real commit** until it is genuinely
re-reviewed + re-stamped — **the transferred organ dogfooding itself in a consumer.** Resolution is a
**real re-review, never a faked stamp** — owed in the ai-council chat.

### The prior three-goal priority — still real, sequenced-after (kept, not deleted)

- **(a) Fable whole-system review** — the Fable-5 architecture review (`d319df9`) landed this window;
  routing its findings is part of (1)'s adjudication load.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier) —
  **designed, not built** (ADR-95 recorded the lane-split).
- **(c) Close the ADR + ai-council methodology tracks** — `#170`/`#168` verified-at-source as
  arc-tracking (NOT the ADR sticking point earlier feared); (b)+(c) remain one work-stream.
- **`#243` — the `#168`-hard vs Fable-WARN conflict** (unresolved): `#168` wants the JOURNAL leg
  fail-closed HARD; Fable consult #1 ruled arc-tracking stays WARN. Resolves alongside (1)/(2).

### Adjacent open decisions (smaller, mostly unchanged)

- **`#241` — declare-vs-defer `reconciled_with`** for the 6 `…→handoff-process` edges (now
  dispositioned; RF-4 above reframes the remedy granularity).
- **`#242` — ADR status-flip coherence check** (Pattern-A vs Pattern-B header↔README divergence).
- **`#220` — the MODIFY / semantic-drift axis** (presence ≠ currency — named by both reviews as the
  shared blind spot). VERIFY-FIRST: does any organ gate a meaning-change-without-version-bump?
- **`#210` — journal-wrap no-ff standing rule**; **`#233`/`#232` — ship-gate right-sizing / tempdir
  isolation** (hygiene).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The [#244] epic close (READ FIRST — the P0 that finished):** `JOURNAL.md` top ~8 entries
  (P2 PRUNE → P3 ROSTER → P4 SYNC-SURFACING); `deploy/contract.py`, `deploy/carrier_precommit.py`,
  `deploy/manifest-v1.2.0.yaml`, `deploy/release_lint.py`, `scripts/gen_methodology_roster.py`,
  `scripts/enforcement_coverage.py`, `scripts/fleet_health.py`; `ecosystem/deployed-versions.yaml`
  (ai-council `1.2.0`); **ADR-96** (remove leg); ADR-91/92/93.
- **The four Fable reviews (THE ADJUDICATION INPUT — §4 item 1):**
  `docs/audits/2026-07-04-handoff-adoption-review.md` (RF-1 anti-bluff),
  `docs/audits/2026-07-04-coherence-spine-review.md` (inverted investment / RF-5 FAIL-trap),
  `docs/audits/2026-07-04-rot-algorithm-design.md` (the continuous-conformance build), and the
  Fable-5 architecture review landed `d319df9`.
- **The continuous-conformance vision (off-repo, prior supplement §6):**
  `docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md` (the operator's own contribution —
  Opus-decomposes → Sonnet-observers nightly rot-check). Do NOT lose it.
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
> **RF-1 corrective (NEW — read this).** The Fable handoff-adoption review (`132c5c9`) found that every
> recent architect bundle prints its probes' answers as `expected: <value>` hints — which §5 says makes
> a probe **bluffable and rejected**. This bundle **deliberately withholds the answer values** below:
> no counts, no SHAs, no dates, no verdicts, no orienting lines are stated. That withholding IS the
> teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a
> remembered number." Where a branch-context note appears, it is there only so CC knows *which* live
> value to compare (e.g. which branch is checked out), not the value itself. **Whether even the old
> drift-reference hints should return is itself an open §4 decision (RF-1) — do not restore them
> without adjudication.**
>
> **Branch note (load-bearing for P3/P6/P9).** This bundle was generated on
> `docs/2026-07-04-architect-handoff` **off `main` (`25b104e`)**, tree clean, in sync with
> `origin/main`. **Unlike the prior handoff, ALL epic work is on `main`** — there is no parallel
> feature branch whose values differ. This handoff's own commit + the later `/ship` `--no-ff` merge
> move HEAD and push `main` ahead until pushed. **Re-derive; do not trust this line.**
>
> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS
> region is empty → the assembler folds nothing → the incoming §13(d) operator-context beat fires
> **FULL** (P1 gate below). **P8's live answer includes the supplement's fill-state — check it.**
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
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (v5.3 §13d):** the
browser asks the operator for **off-repo** context. This bundle's supplement is **generated EMPTY**, so
the beat fires **FULL** (*"what off-repo context — intent, priorities, findings not in the repo,
changed decisions?"*) — **not** a narrowed "anything changed since?" — unless the operator fills the
supplement first (`supplement filled`), in which case its ANSWERS fold into `PASTE_THIS.md` and the
beat narrows.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, RF-1**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-04-dev-knowledge-architect/` ∩ `HANDOFF_PROCESS.md` §13 (∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md` — is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — it fires **FULL** while the
   supplement is empty (a full off-repo ask), or **NARROWS** to *"anything changed since?"* once the
   operator fills the supplement. Then run P2–P9, each against **live state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **Answer
   values are deliberately absent (RF-1)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state** (empty at
   generation; may be filled by read-time). First check which branch is live (P3) — this window unlike
   the last has no parallel feature branch, so `main` is the single source of truth.
