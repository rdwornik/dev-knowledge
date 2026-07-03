=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-03-dev-knowledge-architect` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **The prior handoff's enforcement-mesh P0 is substantially DONE — Axis-1 enforcement-transfer is PROVEN on ai-council (n=1).** This window built the **Informant Organ** (`enforcement_coverage.py`, `[#235]` Stage-2 — read-only per-consumer × per-organ coverage reporter; first run reproduced the honest 0-enforcing-local fleet-map) → the **mesh carrier** hub-side (`deploy/carrier_mesh.py`, `#236` + the `session_end_backpressure` git-toplevel-first port `#237`) → deployed methodology **v1.1.0 to ai-council** (tag `v1.1.0`, ADR-91 record) → **fired `enforcement_coverage.py --fire` and got `enforcing-local ×2`** (seb `decision:block` on unanchored work + `canonical_freshness` blocked-in-isolation) — **the first empirical proof the deployed methodology BITES in a consumer** (ADR-81 leg-(e) acceptance MET). `#236`/`#237` **closed** (done-items-leave). Separately, **all 4 Fable consult #1 rulings landed** (**ADR-94** status-line-mutable-on-ratification, **ADR-95** ai-council query lane-split, the **#179** undeclared-edge ship-gate WARN leg, **ADR-81 leg-(e)** functional-proof). **The immediate open arc: the P1 essence-spec + release-lint on `feat/essence-spec-p1` — committed but NOT merged (commit-and-stop, `[#244]`), awaiting architect review + integration decision.** The next frontier: **(1)** review + merge the essence-spec P1 branch (+ its 3 surfaced decisions: absorb-in-place spec-path, release-lint preflight wiring, P2/PRUNE gating); **(2)** ~~decide whether the mesh-model Fable consult #2 is needed~~ — **answered by the filled supplement: RESOLVED + MOOT**, settled by measurement + build (mesh carrier = "Model D", enforcing-local ×2), do NOT spin one up; only `#243` stays open; **(3)** Stage-4 doctrine writeup (`#238` "deployed presence ≠ deployed enforcement") + fleet n=2+ (`#221`, now that the carrier is proven). **The demoted three-goal priority stays real, sequenced-after:** Fable whole-system review · ai-council-as-governed-query · close the ADR + ai-council methodology tracks. |
| **Generated at** | Bundle cut on branch `docs/2026-07-03-architect-handoff` **off `main` (`ff3d744`)** — deliberately NOT off `feat/essence-spec-p1`, so merging this handoff never drags the unreviewed P1 arc onto `main`. Working tree **clean**; `main` **in sync with `origin/main`** at generation. This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **`SUPPLEMENT.md` is FILLED — its ANSWERS are folded into `PASTE_THIS.md` and SUPERSEDE the residual on priority/design.** The bundle was assembled by CC from committed repo state, but the operator then filled the supplement from the outgoing architect chat. **Load-bearing answers (read the folded `SUPPLEMENT.md` in full — authoritative):** `[#244]` is the methodology **LIFECYCLE-MANAGEMENT** epic (transfer · sync · **PRUNE**) — **resume at P2 (PRUNE, the first deleting phase; Opus, plan-first, gated on operator D1–D3)**; the essence-spec P1 spec-path (in-place absorb-not-pair) is **APPROVED → merge `feat/essence-spec-p1` to `main`**; release-lint preflight wiring **correctly deferred** out of P1; the **mesh-model Fable consult #2 is RESOLVED + MOOT** (settled by measurement + build — mesh carrier is "Model D", fired enforcing-local ×2; **do NOT spin one up**); a **continuous-conformance** nightly-hygiene routine (Opus decomposes → Sonnet observers per-file rot-check) rides in as new vision under `[#244]`. Because the supplement carries answers, the incoming **§13(d) operator-context beat NARROWS** to *"anything changed since?"* — not a FULL re-ask.

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

# Residual — 2026-07-03 architect handoff — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This window EXECUTED the prior handoff's P0.** The `2026-07-02-dev-knowledge-architect-2`
> bundle re-scoped the priority to *close the enforcement-transfer gap*. This window **did it**:
> Informant Organ → mesh carrier → deployed v1.1.0 to ai-council → **enforcing-local ×2 PROVEN**
> (the first empirical proof the deployed methodology BITES in a consumer). Plus all 4 Fable
> consult #1 rulings landed. The one **un-integrated** arc is the P1 essence-spec on
> `feat/essence-spec-p1` (commit-and-stop, `[#244]`) — **the immediate architect review item** (§4).
>
> **`SUPPLEMENT.md` is now FILLED — it SUPERSEDES this residual on priority/design.** The operator
> supplied this window's strategic *why* from the outgoing architect chat; it is folded into
> `PASTE_THIS.md` (**read it in full — authoritative**), so the incoming §13(d) beat **NARROWS** to
> *"anything changed since?"* Headline answers: **`[#244]` is the methodology LIFECYCLE-MANAGEMENT
> epic** (transfer · sync · **PRUNE**) — **resume at P2 (PRUNE, the first *deleting* phase; Opus,
> plan-first, gated on operator D1–D3)**; the essence-spec P1 spec-path (in-place absorb-not-pair) is
> **APPROVED → merge `feat/essence-spec-p1` to `main`**; release-lint preflight wiring is **correctly
> deferred** out of P1; the **mesh-model Fable consult #2 is RESOLVED + MOOT** (settled by
> measurement + build — the mesh carrier shipped as "**Model D**", fired enforcing-local ×2; **do NOT
> spin one up**). A new vision element rides in: a **continuous-conformance** nightly hygiene routine
> (Opus decomposes → cheap Sonnet observers do per-file binary rot-checks). §4's posed questions
> below are **answered by the supplement** — kept for the reasoning, not to relitigate.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the
> load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-03-architect-handoff` off `main` `ff3d744`).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and CLEAN; **10 WARN dispositioned, NO `[stale]` line**

`python scripts/audit.py ship-gate` → **GREEN** (**10 WARN dispositioned**, **NO `[stale]`**) —
verification organs green against the `main` arc. The 10 dispositioned WARNs are all standing /
benign (none is a regression):

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) — **expected seam, not a regression.** **#210** (open) proposes converting
  this class from per-instance disposition to a standing rule (path-scoped EXEMPT or branch-then-merge
  the JOURNAL wrap) — a §4-adjacent decision.
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241**. **NEW this window** — the `#179` undeclared-edge scan (Fable consult #1 ruling #2) was
  wired as a ship-gate WARN leg and **fires as designed**; the 6 hub candidates were dispositioned
  per-doc (precise, not blanket-declared) with the declare-vs-defer adjudication tracked by **#241**.

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the
  methodology source; its own entry stays null. **ai-council** now records **`1.1.0`** (`source_tag
  v1.1.0`, `deployed_date 2026-07-03`) in `ecosystem/deployed-versions.yaml` — deploy run #1.
- `enforcement_coverage` (`[--]`) — the Informant Organ's static leg is **read-only, never
  FAIL/WARN**; per-consumer coverage is measured by `scripts/enforcement_coverage.py` (the fire test
  is the truth-maker, not this leg).

_(No `[stale]` disposition. This is a clean gate — the whole §1 is standing flags, no new regression.)_

---

## §2 — Shipped this window (prior `-2` bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~8). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`. **On `main` (`ff3d744`)** except where noted.

**The enforcement-mesh P0 — BUILT + ARMED + PROVEN (n=1) — the sealed backdrop (do NOT redo):**
- **Informant Organ** (`#235` Stage-2, `99401d7`/`03a3280`; epic filed `c310058`): `enforcement_coverage.py`
  (`CoverageProbe{applicability → locate → fire_test}`; fire_test = clone+inject+assert-block, the
  **sole** truth-maker for `enforcing-local`). First run reproduced the **honest fleet-map** —
  `canonical_freshness` + `session_end_backpressure` **absent ×4** (the real closable gap);
  `doc_claims` + `git_backlog_drift` **hub-scoped ×8** (hub-only-guarded — no consumer wiring can fire
  them); `reconciled_versions` **n/a-no-edges ×4**. Static leg added to `ALL_CHECKS` (non-blocking `n/a`).
- **Mesh carrier hub-side** (`#236`/`#237`, `5028d03`/`62c26b2`/`edc1f5f`/`dd53c99`, merged `e5e88cf`):
  `deploy/carrier_mesh.py` (5th carrier) + `session_end_backpressure` **git-toplevel-first** root
  resolution + extracted `scripts/canonical_freshness_gate.py` (single-sourced hub module). A staging
  **defect** (gitignore swallowed 2 of 7 artifacts) was **caught in Phase-1 + fixed** (`5f8be71`:
  `.gitignore` re-include negation + `git check-ignore` committability verify — *presence ≠ committable*).
- **Deployed v1.1.0 to ai-council** (`52e87ac`, tag `v1.1.0`, merged `4592ed4`; ADR-91/92) →
  **fired `enforcement_coverage.py --fire` → `enforcing-local ×2`** (`5f95d06`, anchored `e2161f9`):
  seb `decision:block` on unanchored work + `canonical_freshness` blocked-in-isolation. **ADR-81
  leg-(e) acceptance MET — the first empirical proof a deployed organ BITES.** `#236`/`#237` **closed**
  (done-items-leave, operator-approved).
- **Fable consult #1 — all 4 rulings landed** (`a0f5aac` merge): **ADR-94** status-line-mutable-on-
  ratification (operator-signed, `e682bdd`); **ADR-95** ai-council query lane-split (record-only);
  the **#179** undeclared-edge scan wired as a ship-gate WARN leg (`62a8248`, demonstrated to fire);
  **ADR-81 leg-(e)** functional-proof amendment (`76d71aa`, mirrored to PLAYBOOK Ch12). Filed
  `#241`/`#242`/`#243` from the disposition pass.

**The immediate open arc (NOT on `main` — `feat/essence-spec-p1`, 7 commits, commit-and-stop `[#244]`):**
- **P1 essence-spec v1 + release-lint** (`16c31ee`→`0fc3807`): `deploy/manifest-v1.1.0.yaml` grew
  `anchors:` / `components:` (13, status `active`, INERT to tool.py) / `doc_shapes:`; `deploy/release_lint.py`
  (C1–C7 reconciling all 5 version anchors to `source_tag`); 27 acceptance tests (golden-diff proves
  `assess` is byte-identical old-vs-new + 17 injected-mismatch teeth). **Behavior-preserving by design.**
  Acceptance MET (golden-diff IDENTICAL, release-lint GREEN + fails 17 mismatch classes, 1101 passed,
  ship-gate GREEN). **This is the architect's review + integration item (§4).**

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — on `main`: **7 themes, 22 stories, 100 tasks** (witnessed via
  `validate_backlog`); on `feat/essence-spec-p1`: **23 stories, 101 tasks** (the `#244` epic). The
  spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated), `feat/essence-spec-p1`
  (**the live unmerged P1 arc — do NOT delete**), this handoff branch `docs/2026-07-03-architect-handoff`,
  plus two **merged stragglers safe to `-d`** (`feat/mesh-carrier-hubside`, `deploy/record-ai-council-1.1.0`)
  and `automation/fleet-audit` (a routine baseline branch, unmerged — separate concern, leave).
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the serialize-groups
  + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9): **code-edge = just `#218`**;
  **coherence = `#180/#181/#182/#220/#241`** (`#241` added this window — the declare-vs-defer edge item);
  **audit-py group includes `#234/#240/#242/#243`**. Note `#238`/`#240`'s `depends-on: #236` was
  **removed** when `#236` closed (satisfied) — they are unblocked.

---

## §4 — The next frontier (open architecture decisions)

**The prior P0 is substantially closed.** "Held by mechanism, not memory" is now **TRUE for one
consumer** (ai-council, n=1) — not just the hub. The frontier shifts from *build the mesh* to *review
the immediate arc, generalize the mesh, and resume the demoted goals*. **recall/inferred** — the
architect resumes here; if an outgoing chat holds more, the operator fills `SUPPLEMENT.md`.

### (1) IMMEDIATE — review + integrate the essence-spec P1 branch (`feat/essence-spec-p1`, `[#244]`)

> **→ ANSWERED (supplement §2/§A):** spec-path (in-place absorb-not-pair) **APPROVED**;
> release-lint preflight **DEFERRED** (correctly out of P1); action = **`--no-ff` merge to `main`
> from the primary**. Then resume the epic at **P2 (PRUNE)**. The posed decisions below are settled —
> kept for the rationale.

The one un-merged arc; committed commit-and-stop precisely so the architect owns the integration call.
- **Merge decision:** review the 7-commit branch; integrate from the **primary** checkout via `--no-ff`
  (never a worktree — the seed-state lesson). P1 is behavior-preserving (golden-diff IDENTICAL) — low risk.
- **Surfaced decision — spec-path (absorb-not-pair):** P1 evolved `manifest-v1.1.0.yaml` **IN PLACE**,
  rejecting a paired `manifest-v1.2.0` (a second spec file recreates the drift-twin; a bumped version
  implies an untagged release preflight would refuse). **Architect confirm or override.**
- **Surfaced decision — release-lint wiring:** `deploy/release_lint.py` is **manually invoked**, wired
  into neither `ALL_CHECKS` nor deploy preflight. Preflight wiring is behavior-changing → **deferred for
  architect placement.**
- **`[#244]` lifecycle epic — P2–P6 gated:** P2 (PRUNE / remove-leg + tombstone) is gated on **operator
  D3**; P3 (roster generation), D2 (divergence allowlist), P5 (hub self-prune), P6 (fleet) all downstream.
  Sequence the epic.

### (2) The mesh generalization — is the Fable consult #2 (mesh-model A/B/C) still needed?

> **→ ANSWERED (supplement §B): RESOLVED + MOOT — do NOT spin up a Fable consult #2.** The A/B/C
> question was settled by research + live recon (corp-ops has no git remote → CI-as-universal-guarantee
> is structurally impossible → **local-carrier + central-detection**) + build (the mesh carrier shipped
> as **Model D**, fired enforcing-local ×2). The Informant fleet-map settled *which* organs are portable
> (Group A freshness/reconciled = portable-local; Group C seb = ported-local; Group B
> `doc_claims`/`git_backlog_drift` = hub-scoped by construction). Settled-by-measurement-and-build. The
> reasoning below stands as the record; the open call is now only `#243`.

The prior handoff located a Fable consult on the **mesh-transfer model**: **(A)** 5th carrier, organs
run locally; **(B)** hub-sweep-on-cadence; **(C)** hybrid. **VERIFY-FIRST:** the Informant Organ's
fleet-map **may have already answered it empirically** — the organ-portability split is not a matter of
taste, it's structural: `canonical_freshness` + `session_end_backpressure` are **locally enforceable**
(now shipped local via the model-A mesh carrier, proven on ai-council), while `doc_claims` +
`git_backlog_drift` are **hub-scoped-by-construction** (they cannot fire inside a consumer without
changing the organ). **That reads like model C (hybrid) decided by measurement, not by consult.** So the
architect's first call: **does a Fable consult #2 still add value, or does the fleet-map + the proven
model-A carrier settle the design** — leaving only `#243` (below) as the open governance sub-question?
(See the memory note *"Enforcement organs not homogeneous"* — the 5 organs split by portability.)
- **`#243` — the `#168`-hard vs Fable-WARN conflict** (unresolved): `#168`'s Done-when says promote the
  JOURNAL leg to fail-closed HARD; Fable consult #1 ruled arc-tracking stays WARN with no-item
  disposition. Resolves at/after the mesh-model call.

### (3) Generalize + formalize the enforcement-mesh (dependency-ordered)

- **`#238` — Stage-4 record+formalize:** write the **"deployed presence ≠ deployed enforcement"**
  doctrine into LESSONS + PLAYBOOK (the configured→armed→proven distinction, generalized to the mesh:
  *done only when enforcement-in-effect is demonstrated, not merely deployed*). **Open** — the doctrine
  is proven but not yet recorded.
- **`#221` — fleet rollout n=2+:** Axis-1 is proven n=1; run `deploy/tool.py` on
  corp-monorepo / corp-ops / corp-sca-time-automation, each using **#230** as its acceptance gate and
  requiring **#225** (surgical precommit carrier) closed first. **Carry the pilot rule:** treat each
  consumer's `.gitignore` + config shape as an **UNKNOWN to probe, not a copy of the hub** (the
  `override.md`/`logs/.gitkeep` gitignore defect that halted the ai-council deploy — LESSONS 2026-07-03).
  **Do NOT onboard corp-monorepo through a soon-to-change methodology** — sequence after the Fable
  whole-system review if that will move the corpus.
- **`#239` — Tier-2 breadth**, **`#240` — audit-leg regression teeth** (WARN on an `enforcing-local →
  absent` regression once a baseline exists), **`#234` — cross-repo probe FAIL-teeth** (harden the
  `.claude/` cross-repo targets; honest-partial WARN today).
- **ai-council standing debt (off-repo, live consequence):** ai-council's `CLAUDE.md` is genuinely
  A2-stale (`last_reviewed: 2026-06-02` < edited 2026-07-02). The now-live **deployed** freshness gate
  **WILL block ai-council's next real commit** until it is genuinely re-reviewed + re-stamped (the organ
  dogfooding itself). Resolution is a **real re-review, never a faked stamp** — owed in the ai-council chat.

### The prior three-goal priority — still real, sequenced-after (kept, not deleted)

- **(a) Fable whole-system review + merge rulings** — input:
  `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`. Note the perishable Fable
  window is now best spent on the mesh-model call (2) if it is still open; the system-audit review is
  real but lower-urgency.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier; browser →
  CC → ai-council; CC owns the mechanical lifecycle, architect owns question-framing) — **designed, not
  built** (ADR-95 recorded the lane-split).
- **(c) Close the ADR + ai-council methodology tracks** — `#170`/`#168` were verified-at-source as
  **arc-tracking** (issue-ID↔commit anchor), **NOT the ADR sticking point** the earlier handoff feared;
  (b)+(c) remain one work-stream, sequenced after (2)/(3).

### Adjacent open decisions (smaller, mostly unchanged)

- **`#241` — declare-vs-defer `reconciled_with`** for the 6 `…→handoff-process` prose edges (now
  dispositioned, not declared — the standing WARN this window introduced).
- **`#242` — ADR status-flip coherence check** (the ADR-88/89 Pattern-A vs ADR-92/94 Pattern-B header↔README
  divergence — filed, not built).
- **`#220` — the MODIFY / semantic-drift axis.** VERIFY-FIRST: does any organ gate a
  *meaning-change-without-version-bump*, or only add/remove/exist? Demonstrated-catch bar first.
- **`#210` — journal-wrap no-ff standing rule** (path-scoped EXEMPT vs branch-then-merge the wrap; must
  NOT weaken core-invariant #5). **`#233`/`#232` — ship-gate right-sizing / tempdir isolation** (hygiene).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The enforcement-mesh proof (READ FIRST — the P0 that closed):** `JOURNAL.md` top ~6 entries (Informant
  Organ → mesh carrier → deploy defect+fix → **enforcing-local ×2** → close #236/#237); `deploy/carrier_mesh.py`,
  `scripts/enforcement_coverage.py`, `scripts/canonical_freshness_gate.py`; `ecosystem/deployed-versions.yaml`
  (ai-council `1.1.0`); ADR-91/92/93; the memory note *"Enforcement organs not homogeneous"* (the organ split).
- **The immediate review item:** `feat/essence-spec-p1` — `deploy/manifest-v1.1.0.yaml`,
  `deploy/release_lint.py`, `tests/test_essence_spec.py` + `tests/test_release_lint.py`, and the
  `feat/essence-spec-p1` JOURNAL top entry (the P1 arc + the 3 surfaced decisions).
- **Fable consult #1 landings:** ADR-94, ADR-95, ADR-81 (leg-(e) amendment), `scripts/audit.py`
  (`check_undeclared_edges`), `docs/decisions/README.md`.
- **The demoted-goals input:** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`.
- **Prior context (superseded on priority, kept for the "why"):** the `-2` bundle's `SUPPLEMENT.md`
  (the enforcement-mesh finding) + `docs/handoffs/2026-07-02-dev-knowledge-architect/` (the three-goal
  context, now demoted).
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
> **Branch note (load-bearing for P3/P6/P9).** This bundle was generated on `docs/2026-07-03-architect-handoff`
> **off `main` (`ff3d744`)**, deliberately NOT off the unmerged `feat/essence-spec-p1`. So the
> generation-time values below are **`main`-side**. If the operator checks out `feat/essence-spec-p1`
> (the P1 arc under review), several probes shift by known deltas: **P6 pytest → 1101** (not 1074),
> **P9/BACKLOG → 23 stories / 101 tasks** (the `#244` epic). The pass criterion is still "answered
> from the live source" — note *which* branch is live before comparing to the hint.
>
> **`SUPPLEMENT.md` is FILLED.** The operator supplied this window's strategic *why* from the outgoing
> architect chat; its ANSWERS are folded into `PASTE_THIS.md` and supersede the residual on
> priority/design (P2/PRUNE resume · essence-spec merge APPROVED · mesh-model consult MOOT ·
> continuous-conformance vision). So the §13(d) operator-context beat in P1's gate **NARROWS** to
> *"anything changed since?"* — not a FULL re-ask. **P8's expected value is FILLED** (see P8).
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
are folded into `PASTE_THIS.md`), so the beat **NARROWS** to *"anything changed since the supplement was
written?"* — **not** a FULL re-ask. The load-bearing off-repo calls are **already answered** in the
folded supplement: essence-spec P1 merge **APPROVED**, resume at **P2 (PRUNE)**; the **mesh-model Fable
consult #2 is MOOT** (do not spin one up).

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — **expected at generation: 28, last name `doc_code_coverage_drift`** (the count moved 26→28 this window: `+enforcement_coverage` `+undeclared_edges`) | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; **this bundle was cut on `docs/2026-07-03-architect-handoff` off `main` `ff3d744`, tree clean, `main` in sync with `origin/main` — but this handoff's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed; and `feat/essence-spec-p1` is a DIFFERENT tip. Re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` (and `git branch --show-current` — which branch is live?) |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle — **expected: only the standing `#77` voided-closure false positive (`77e5d7df9`), no more** | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — **expected: stamp on/after the last touch (both 2026-07-02); HONEST — this window did not touch ARCHITECTURE on `main`** | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **expected to MATCH: `1074/1074` on `main`, or `1101/1101` on `feat/essence-spec-p1`** (the P1 suite adds 27 tests + regen'd doc-counts). The pass test is "answered from the live source on the live branch," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline:** at generation `ship-gate` is **GREEN** with **`10` WARN dispositioned** (#77 voided-closure + 3 journal-wrap/transcript no-ff + **6 `…→handoff-process` undeclared edges under #241**, NEW this window) AND carries **NO `[stale]` line**. The live answer is the only ground truth (a new direct-on-`main` commit would re-RED it); the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement state; the live bundle + spec are the only ground truth — **expected: FIVE files (BOOT + RESIDUAL + PROBES + SUPPLEMENT + PASTE_THIS), NO `README.md`; `SUPPLEMENT.md` present with ANSWERS **FILLED** (the operator filled it from the outgoing chat → the ANSWERS region IS folded into `PASTE_THIS.md`); boilerplate lives once in `docs/handoffs/README.md`** | `ls docs/handoffs/2026-07-03-dev-knowledge-architect/` ∩ `HANDOFF_PROCESS.md` §13 (∩ `grep -A2 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md` — is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle — **expected: code-edge = ONLY `#218`; coherence = `#180/#181/#182/#220/#241`** (`#241` added this window); the `audit-py` group includes `#234/#240/#242/#243`. On `main`: 22 stories / 100 tasks; on `feat/essence-spec-p1`: 23 / 101 (the `#244` epic) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — it **NARROWS** (this bundle's
   supplement is FILLED, ANSWERS folded into the paste) to *"anything changed since the supplement was
   written?"* — not a FULL re-ask (the essence-spec merge + mesh-model calls are already answered). Then
   run P2–P9, each against **live state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P9 are *expected to move* between generation and check-time — that is the design. **First
   check which branch is live (P3)** — `main` vs `feat/essence-spec-p1` shifts P6 (1074↔1101) and P9
   (22/100 ↔ 23/101). **P7 is the headline: expected GREEN with `10` dispositioned WARNs AND NO
   `[stale]` line** — but the pass criterion is **"answered from the live source,"** never "matches the
   verdict the summary remembered." **P2** is expected to read **28** (last name `doc_code_coverage_drift`).
   **P5** expects an HONEST 2026-07-02 stamp. **P8** pins the five-file shape with `SUPPLEMENT.md`
   **FILLED** (ANSWERS folded into `PASTE_THIS`; no README). **P9** pins the now-durable serialize-group graph
   (#156) with **code-edge = just #218** and **#241 newly in coherence**.

---

=== SUPPLEMENT.md ===

SUPPLEMENT — outgoing architect answers (essence-transfer epic [#244], resume at P2)

=== 1. Strategic intent (way-of-working goal) ===
Build the methodology's LIFECYCLE-MANAGEMENT system: make the methodology a governed, versioned,
PRUNABLE artifact across repos — not an add-only pile. Concretely: close the "only-adds-never-
removes" gap so the live consumer-facing surface (CLAUDE.md rosters, gotchas, active
organs/commands/skills) stays current BY MECHANISM, not by a human catching rot by eye. Epic
[#244]. Resume at P2 (PRUNE — the first deleting phase).

=== 2. Tensions weighed — where we landed + why ===
- Spec representation (separate file vs in-place manifest evolution): landed IN-PLACE (evolve
  manifest-v1.1.0.yaml). Absorb-not-pair (F1): a separate methodology-spec.yaml recreates the
  drift-twin the analysis rejected; a v1.2.0 file is untagged -> preflight refuses -> live
  golden-diff undemonstrable. In-place keeps behavior byte-identical + provable.
- PRUNE vs Layer-2 autonomy-no invariant (how does the hub remove things from a consumer without
  an autonomous cross-repo write): landed on consumer-invoked deploy ONLY, staged-not-committed,
  hash-guarded (locally-modified = conflict-REFUSE, surfaced not deleted). Nothing autonomous
  deletes.
- Append-only vs prune: landed on the PATHOLOGY SPLIT — the audit trail (LESSONS/JOURNAL/ADRs)
  stays append-only/immutable; the live surface (CLAUDE.md/gotchas/active organs) gets pruned; a
  tombstone is itself an append to the audit trail.
- Conformance shape (one organ vs two): landed on ONE — extend the Informant
  (enforcement_coverage.py), three tiers (fire / presence / essence-conformance); firing and shape
  never conflated.
- Version granularity: landed on ONE methodology semver; component-level status:/removed_in: gives
  granularity without ~5x version-anchor drift.
- CLAUDE.md roster home: LEANING separate @-included generated file (keeps CLAUDE.md 100% human
  prose so the freshness gate keeps its teeth undiluted) — but this is operator decision D1 (open).

=== 3. Considered + rejected (do NOT relitigate) ===
- Separate methodology-spec.yaml — rejected (drift-twin, F1; absorb into the manifest).
- v1.2.0 file for P1 — rejected (untagged -> preflight refuse -> golden-diff undemonstrable).
- copier-LITERAL (adopt as a dependency) — rejected (templating doesn't fit organs with firing
  acceptance; the carriers are proven). Adopt the copier MODEL (deletion-propagation), not the tool.
- Renovate/Dependabot/Backstage/OPA as mechanisms — rejected (no cross-repo PR infra on local
  sibling repos; conformance is better-fitted in the Informant). Their SHAPE confirms the pattern
  (pinned versions + surfaced drift + gated update); we additionally have a demonstrated-firing
  standard they lack.
- Two conformance organs — rejected (duplicates the Informant's fleet plumbing + clone harness).
- Big-bang "solve everything in one pass" — rejected (PRUNE = deletion; autonomous deletion is
  forbidden; phased with a demonstrable per-phase acceptance is the discipline).
- Per-component semver — rejected (5x anchor-drift surface for no decision the operator would make
  differently).
- CI-as-guarantee for enforcement — rejected earlier (corp-ops has NO git remote -> a universal CI
  gate is structurally impossible fleet-wide; local-carrier + central-detection is the model).

=== 4. Open questions (deferred / unresolved) ===
- D1 — roster home: separate @-included generated file (rec) vs a marked block inside CLAUDE.md
  (ADR-53 doctrine call). Needed for P3.
- D2 — divergence-allowlist home: consumer-side .claude/methodology.yaml (rec) vs hub-side registry.
- D3 — grace state: a "deprecated" warning tier between active/removed, or straight active->tombstone
  (rec: no grace state at n=4).
- Global vs local conformance coverage: MUST cover BOTH ~/.claude (global gotchas/skills) AND
  per-repo (local) surfaces. Fable inventoried global; local per-repo coverage to be designed at
  P4 / Informant-Tier-3.
- release-lint wiring into preflight — behavior-changing, deferred to a later phase (manual-only today).
- #236 depends-on removal from #238/#240 — verify it actually unblocked them (flagged, unconfirmed).

=== 5. Decomposition rationale (why this shape; what NOT to redo) ===
Dependency order P1 -> P2 -> {P3, P4} -> P5 -> P6, each phase with a DEMONSTRABLE acceptance
(a mechanism that FIRES / a prune that REMOVES + verifies-absent), ai-council n=1 throughout before
any fleet step. P1 first because it's behavior-preserving (golden-diff) — the safe foundation that
establishes the self-model with zero risk. P2 (prune) is the crux + first DELETING phase -> Opus,
plan-first, gated on D1-D3. Fleet (P6) only after prune proven on n=1.
MUST NOT redo/re-decide: the corpus inventory (Fable did it — re-derive from the live repo, never
re-analyze from a summary); the essence-spec schema (built in P1); the in-place spec-path decision;
the mesh carrier (built + proven, Model D); the mesh-model A/B/C question (MOOT — see B).

=== 6. Off-repo context (not in the repo) ===
- CONTINUOUS-CONFORMANCE vision (operator's own contribution — do NOT lose): an ongoing nightly
  hygiene routine that reads the corpus FILE-BY-FILE for rot ("does this reference something
  obsolete / is this no longer needed"). Shape (validated; maps to Anthropic orchestrator+subagents):
  architect/Opus DECOMPOSES -> cheap Sonnet observer-agents do the per-file BINARY rot-check
  (zero/one: rotted y/n) -> surface. This is the continuous-conformance layer ABOVE P4/P5, and where
  release-lint (manual today) gets wired. Cost-appropriate + scalable. Home = [#244].
- Model routing: Fable's architecture job is DONE — do NOT re-invoke it for build phases; reserved
  for a genuinely-new contested fork only. P2 = Opus, plan-first. Mechanical phases + the
  observer-agents = Sonnet.
- Standing debts: P1 merge feat/essence-spec-p1 -> main (primary, --no-ff); ai-council CLAUDE.md
  GENUINE re-stamp (the deployed freshness gate is blocking ai-council's next commit on a live A2 —
  this is the first live-drift firing of the transferred organ; do a real re-read, NEVER a date-bump).

=== A. Essence-spec P1 merge intent + verdict on the two surfaced decisions ===
feat/essence-spec-p1 was committed-and-stopped for BOTH: architect review of the two surfaced
decisions AND to serialize integration (operator merges from primary). Verdicts:
- Spec-path (in-place absorb-not-pair): APPROVED. Fable chose a third option over the two offered,
  and it is the correct one (endorsed at review). methodology_version stays 1.1.0 for P1 (same
  version, richer representation, behavior identical); the next bump = P2 -> v1.2.0 tagged then
  (behavior-changing prune).
- release-lint preflight placement: DEFERRED — correctly OUT of P1. Preflight-wiring is
  behavior-changing; keep release-lint manual until a later phase that owns that behavior change.
Action: --no-ff merge to main from primary.

=== B. Mesh-model consult status ===
RESOLVED + MOOT — do NOT spin up a Fable consult #2 on the mesh-transfer model. The A/B/C question
was settled by RESEARCH (git-hooks: local-advisory vs central-enforcement) + LIVE RECON (corp-ops
has no git remote -> CI-as-universal-guarantee structurally impossible -> local-carrier +
central-detection is the model) + BUILD (the mesh carrier shipped as Model D and FIRED
enforcing-local x2 on ai-council). The Informant fleet-map settled WHICH organs are portable
(Group A canonical_freshness/reconciled = portable-local; Group C seb = ported-local; Group B
doc_claims/git_backlog_drift = hub-scoped by construction), feeding the carrier scope. So:
settled-by-measurement-and-build, not awaiting a consult. The Fable window was instead spent on the
essence-transfer architecture (the larger question), which subsumed the propagation question.
