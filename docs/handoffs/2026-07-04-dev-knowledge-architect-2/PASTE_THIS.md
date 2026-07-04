=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-04-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **Second architect handoff of 2026-07-04 — the delta since the `-architect` bundle (`c185c09`), which is: the operator's re-sequenced program moved into execution.** The prior (filled) supplement re-ordered everything around **deployment · sandbox · tests** and ruled **P5/P6 WAIT**: Phase 0 (safety + self-honesty) → Phase 1 (build the lived-workflow **sandbox** as the retroactive acceptance instrument for [#244] P1–P4) → Phase 2 (fleet re-gated). This window executed into that: **(1) ARCHITECTURE 2026-07-04 currency re-read** (coherence-spine self-blindness cleared — `undeclared_edges` now verified live in `ALL_CHECKS`, `roster-freshness` gate added, honest re-stamp); **(2) RF-2 hub self-arm + `hooks_armed` check** (the sandbox's own precondition; delete-a-hook→`health DEGRADED` demonstrated); **(3) the handoff-generator lane** — `gen_handoff.py` + the anti-bluff RF-1 answer-hint rung made **STRUCTURAL, not hand-discipline** ([#164]/[#161]/[#163], NOT closed); **(4) lived-workflow sandbox Slice A** ([#252]) — isolated `claude -p` **spawn + isolation PROVEN + Codex-hardened** (2 CRIT + 2 HIGH fixed), then **STOP at the Slice A gate for architect review**. **The next session's PRIMARY job is that review:** adjudicate the spawn+isolation foundation → on approval, build **Slice B** (OUTER deterministic observer + `engages:`-spec oracle + six-hook arc + seeded-EXPECTED-BUT-SILENT closure). Secondary, all still open: (a) **integrate the handoff-generator's deferred spec arc** (HANDOFF_PROCESS §5/§13 → option b + `5.3→5.4` bump + 5 `reconciled_with` re-stamps — decoupled to the architect because it collides with sandbox-owned `ARCHITECTURE.md`); (b) **route the four carried Fable reviews** (RF-1 now *structurally* half-fixed — the spec re-ratify + first bluff-dogfood-rerun still owed); (c) hold **P5/P6** per the operator rule; (d) clear the LIVE debts — **ai-council `CLAUDE.md` A2-stale** (the deployed freshness gate will block its next commit) and a **flagged `ANTHROPIC_API_KEY` leak** into this session's local transcript (rotation recommended). |
| **Generated at** | Bundle cut on branch `docs/2026-07-04-architect-handoff-2` **off `main` (`a523fca`)**, working tree **clean**, `main` **in sync with `origin/main`** at generation. **All window work is on `main`** — no parallel feature branch open (the sandbox `feat/lived-sandbox-slice-a` and `feat/handoff-generator` lanes already merged `--no-ff`; only `automation/fleet-audit`, a routine baseline branch, remains unmerged — separate concern, leave). This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **`SUPPLEMENT.md` is generated EMPTY.** The bundle is assembled by CC from committed repo state; the
> operator may fill the supplement from the outgoing architect chat (`supplement filled`) so its ANSWERS
> fold into `PASTE_THIS.md`, or leave it empty for a cold handoff (the defined §13 disposition). **Until
> filled, the incoming §13(d) operator-context beat fires FULL** (a full off-repo ask), not the narrowed
> *"anything changed since?"*.

> **RF-1 corrective in effect — now the RATIFIED, STRUCTURAL contract (read `PROBES.md` header).** The
> Fable handoff-adoption review found every recent bundle printed its probe answers as `expected:` hints,
> inverting the §5 anti-bluff contract; the operator **re-ratified** withholding ("treat every `expected:`
> as SUSPECT") and this window made the fix **structural** — `verify_handoff_probes._classify` now FAILs a
> probe that ships an answer hint, so the erosion cannot silently return. This bundle **deliberately
> withholds the probe answer values** (no counts, SHAs, dates, verdicts, or orienting lines). The
> withholding IS the teeth; run the commands.

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

# Residual — 2026-07-04 architect handoff (#2) — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This is the SECOND architect handoff of 2026-07-04.** The first (`c185c09`,
> `docs/handoffs/2026-07-04-dev-knowledge-architect/`) closed [#244] P1→P4 and had its supplement
> **filled** (`0684174`) — the operator's answers **re-sequenced the whole program** around
> **deployment · sandbox · tests**, ruled **P5/P6 WAIT**, and set the phase order **Phase 0 (safety +
> self-honesty) → Phase 1 (build the sandbox as the retroactive acceptance instrument for P1–P4) →
> Phase 2 (fleet re-gated)**, with the rot-algorithm **deferred-until-after-sandbox**. **This window
> executed into that program.** Read the prior bundle's filled `SUPPLEMENT.md` — it is the strategic
> frame this residual sits inside, and it is NOT re-narrated here.
>
> **The delta this window = four lanes, all merged to `main`:** (1) ARCHITECTURE currency re-read,
> (2) RF-2 hub self-arm, (3) the handoff-generator (anti-bluff made structural), (4) **lived-workflow
> sandbox Slice A — STOP at the review gate.** **The next session's PRIMARY job is the Slice A review**
> (§4.1).
>
> **`SUPPLEMENT.md` is generated EMPTY** — the operator fills it from the outgoing architect chat
> (`supplement filled`) or leaves it empty for a cold handoff (§13 disposition). Until filled, the
> incoming §13(d) operator-context beat fires **FULL**.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate outputs);
> `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved — the load-bearing
> ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**, on branch
`docs/2026-07-04-architect-handoff-2` off `main` `a523fca`, tree clean, in sync with `origin/main`).
**Re-derive each at read-time via `PROBES.md`** — the teeth are there, not in trusting these lines. Per
the ratified RF-1 corrective, the bluffable values (the GREEN/RED verdict, the dispositioned count) are
**withheld here and obtained live via P7**; only the *named, structural* standing flags are listed.

### ✅ HEADLINE — the gate carries **only the standing dispositioned set; no new regression this window**

`python scripts/audit.py ship-gate` (**run it — P7**) returns the verification organs against the `main`
arc. The dispositioned WARNs are the **same standing set** as the prior handoff — this window added no new
drift class:

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but #77
  stays in BACKLOG by design — operator ruled keep-open). Dispositioned (`warn-77-voided-closure`).
  **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits — **expected seam, not a
  regression.** **#210** (open) proposes converting this class to a standing rule.
- `undeclared_edges`: **6** `…→handoff-process` prose edges (`BACKLOG.md`, `VISION.md`,
  `AI_COUNCIL_PROCESS.md`, `ESSENTIALS.md`, `PLAYBOOK.md`, `SESSION_SETUP.md`) dispositioned under
  **#241**. **The carried Fable coherence-spine review (RF-4) argues these 6 are major-granularity edges
  mis-served by an `@5.3` remedy — a §4 decision, unchanged.**

### One `ALL_CHECKS` change this window (structural, not a drift)

- `ALL_CHECKS` **grew by one** — RF-2 added **`hooks_armed`** (the hub self-arm check). The count and the
  last-registered check **name** are the live answer to **P2** (withheld here). The `doc_code_coverage_drift`
  guard reports **all** members covered (annotated or exempt) — no coverage escape.

### Two non-blocking informational legs (by design — not WARNs)

- `deployed_methodology_version` for **.dev-knowledge** = `unset` (`[--]`) — the hub **is** the methodology
  source; its own entry stays null. **ai-council** records **`1.2.0`** (unchanged this window — no new deploy;
  P6 fleet still held). corp-monorepo / corp-ops / corp-sca-time-automation still `null`.
- `enforcement_coverage` (`[--]`) — read-only, never FAIL/WARN; per-consumer truth is the `--fire` test.

_(No `[stale]` disposition — witnessed. Verify via P7; do not trust this line.)_

---

## §2 — Shipped this window (prior `-architect` bundle `c185c09` → now) — the map, not the narration

Pointer-first (`git log --first-parent c1454e4..HEAD`, `JOURNAL.md` top 2 entries). **All on `main`
(`a523fca`)** — every lane merged `--no-ff`; nothing left on a feature branch. **recall/inferred** from the
window; re-derive load-bearing values via `PROBES.md`.

**Four lanes landed (the sealed backdrop — do NOT redo):**

- **(1) ARCHITECTURE 2026-07-04 currency re-read** (merged `fbf88ae`; `docs/architecture-currency-2026-07-04`):
  cleared the **coherence-spine review's "demonstrated self-blindness"** — `undeclared_edges` is now
  confirmed live in `ALL_CHECKS` (not just asserted by the review), the omitted **`roster-freshness`** gate
  was added to the ARCHITECTURE inventory, and `last_reviewed` was **honestly re-stamped** after a genuine
  end-to-end read. This resolved the dirty-tree precondition the sandbox lane needed. (Operator change #1.)
- **(2) RF-2 hub self-arm + `hooks_armed`** (merged `2e7b072`; Fable arch review §4 — *the sandbox's own
  precondition*): `scripts/arm_hooks.py` (idempotent / fail-soft SessionStart self-arm) + a new
  `audit.py::check_hooks_armed` that resolves the hooks dir via `git rev-parse --git-path hooks`.
  **`ALL_CHECKS` 28→29.** **Demonstrated live:** delete `pre-push` → `audit.py health` goes **DEGRADED**.
  The redundant `core.hooksPath` (= default) was unset per operator so `pre-commit install` works normally.
- **(3) The handoff-generator lane** (merged `9d5ebe5`; `feat/handoff-generator`; [#164] RF-2 / [#161] /
  [#163] — **NOT closed**): built `scripts/gen_handoff.py` (assembles a valid v5 bundle from **committed**
  state) + `templates/handoff/v5/{PROBES,HANDOFF_BOOT,RESIDUAL}.md.tmpl` + a size-warn on
  `assemble_paste.py`. **The load-bearing win: the anti-bluff RF-1 fix is now STRUCTURAL, not
  hand-discipline** — the `/expected[ :]/`→FAIL rung rides `verify_handoff_probes._classify` (row-scoped;
  live 07-04 bundle passes 10/10, historical 06-25 fails 6 in isolation, ship-gate `handoff_probes` stays
  GREEN because the deployed check reads only the latest bundle). Answer-hint VALUES now go to a
  **JOURNAL-draft on stdout**, never a browser-visible file — so the `expected:` erosion (0→peak-5 across
  06-20..07-03) **cannot silently return**. **Zero `scripts/audit.py` edits** (stayed file-disjoint from
  the sandbox lane).
- **(4) Lived-workflow sandbox Slice A** (merged `a523fca`; `feat/lived-sandbox-slice-a`; **[#252]**;
  scaffold `ac3461c` + Codex fixes `ad719b9`): `deploy/lived_sandbox/` — an isolated `claude -p` **spawn** +
  clone/teardown + the **isolation proof**. **Correctness property PROVEN empirically + via the module:**
  SessionStart hooks DO fire under `claude -p` headless on Windows; `CLAUDE_CONFIG_DIR` governs user-level
  hooks (sentinel present-configA / absent-configB, both exit 0). **Codex review** (gpt-5.5 high,
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md`) found **2 CRITICAL + 2 HIGH — all fixed + tested
  + isolation re-PROVEN** (false-green exit-gating; teardown blast-radius anchored to system-temp;
  `extra_env` can't override protected keys; subprocess→`SandboxError`). Module suite 16 passed / 1 skipped;
  full suite 1210 passed / 1 skipped / **1 failed = the pre-existing [#251] only**. **STOP at the Slice A
  gate** — the whole point of the lane (§4.1).

**Also logged (not built):** **[#251]** — a pre-existing deploy-CLI success-render red (`record_branch`
dropped; stale-test-vs-regression TBD), captured `f62d4f4` so the sandbox suite's "1 failed" is a known
quantity, not a new break.

**Carried, unchanged this window (the prior bundle's real work — still the next session's load):** the
**four Fable read-only reviews** (handoff-adoption / coherence-spine / rot-algorithm design / Fable-5
architecture review) are all merged and **none acted on**. RF-1 (anti-bluff) has now advanced *structurally*
(lane 3) but its **spec re-ratification + first bluff-dogfood-rerun are still owed** (§4.2). See the prior
`RESIDUAL.md` §2/§4 for their full statement — not re-narrated here.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** — **7 themes, 23 stories, 109 tasks** (witnessed via `validate_backlog`;
  +2 vs the prior bundle = the new **[#251]** deploy-CLI red + **[#252]** sandbox epic). The `[#244]` epic
  records **P1/P2/P3/P4 SHIPPED**, **P5/P6 remaining (WAIT per operator)**. The spec; items are tickets.
  Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (all window work integrated), this handoff
  branch `docs/2026-07-04-architect-handoff-2`, and `automation/fleet-audit` (a routine baseline branch,
  unmerged — separate concern, **leave**). **No unmerged feature branch this window** — the sandbox +
  handoff-generator lanes already merged. No merged stragglers to `-d` beyond what `/ship` will handle.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the serialize-groups
  (verify via `PROBES.md` P9). This window's new groups: **`sandbox` = [#252]**, **`deploy` = [#251]**;
  the audit-py / coherence / code-edge groups are unchanged from the prior bundle. Open the file for
  placement of the new follow-ups.

---

## §4 — The next frontier (open architecture decisions)

**The next session is a REVIEW-then-BUILD session gated on one thing: the Slice A foundation.** The
[#244] build epic is sealed (P1–P4, P5/P6 held); the operator's re-sequenced program (prior supplement) put
the **sandbox** as Phase 1 — the retroactive acceptance instrument for everything already shipped — and this
window delivered its **Slice A** to a STOP gate. Everything else is carried and sequenced *after* that gate.
**recall/inferred** — the outgoing chat's strategic *why* fills `SUPPLEMENT.md`.

### (1) PRIMARY — review the lived-workflow sandbox Slice A, then build Slice B ([#252])

This is the session's reason to exist. Slice A is the **spawn + isolation foundation** for the episodic
lived-workflow harness (the operator's continuous-conformance instrument). It is **built, Codex-hardened,
and STOPPED for architect review** — autonomous progression past the gate was deliberately withheld.

- **The review:** adjudicate `deploy/lived_sandbox/` (spawn / clone / teardown / isolation proof) +
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` (the 2 CRIT + 2 HIGH, all fixed). Is the isolation
  contract sound — `CLAUDE_CONFIG_DIR`-governed hooks, system-temp-anchored teardown blast-radius, protected
  env keys, exit-gating not false-green? Is the abstraction the right seam for Slice B to build on?
- **On approval — build Slice B** (the sandbox's actual acceptance value, from the prior "Next"): the
  **OUTER deterministic observer** + the **`engages:`-spec oracle** (essence-spec as the pass/fail source)
  + the **six-hook arc** + **seeded-EXPECTED-BUT-SILENT closure** (inject a should-fire-but-doesn't organ,
  prove the harness catches the silence). Opus, plan-first. This is what makes the sandbox a *retroactive
  acceptance instrument for P1–P4*, not just a spawn wrapper.
- **Live security flag from the Slice A session (act before/independently):** an `ANTHROPIC_API_KEY` was
  printed into this session's **local transcript** via a `${KEY:-}` bash bug (local only — not committed,
  not external). **Rotation recommended** (the harness reads the key fresh each spawn, so a rotate is
  cheap). Gotcha logged (`~/.claude/skills/gotchas/gotchas.md`, `${VAR:-}` secret-leak entry).

### (2) Integrate the handoff-generator's DEFERRED spec arc (this window created the debt)

Lane 3 shipped the generator + the structural anti-bluff fix but **deliberately deferred the spec
reconciliation to the architect at serial integration** (operator ruling Q1), because it collides with
**sandbox-owned `ARCHITECTURE.md`** and touches freshness-gated CLAUDE/ARCHITECTURE. Owed:

- **HANDOFF_PROCESS §5/§13 additive reconciliation to RF-1 "option b"** (the structural withhold) + the
  **`5.3 → 5.4` version bump** + **5 `reconciled_with` re-stamps** (the coupled surfaces the version bump
  forces atomic). Fold into an ARCHITECTURE-currency pass so the freshness gate rides the content commit.
- **Adjudicate [#164]'s formal BACKLOG disposition:** RF-2 slice + RF-1 "option b" are **done**; cross-repo
  probe sets + v4-prose removal remain open (both ADR-83-gated). [#161]/[#163] similarly partial.
- **Reconcile the shared `ecosystem/doc-counts.md` `pytest_collected`** once, after all test-adding branches
  are integrated (this window's suite grew; regenerate, don't hand-edit).

### (3) Route the four carried Fable reviews (RF-1 now half-done — finish it)

All four landed in the *prior* window and remain the meaty methodology work. Priority order (RF-1 changed):

- **RF-1 (handoff-adoption) — the STRUCTURAL fix landed (lane 3); the DOCTRINE half is still owed.** The
  operator re-ratified withholding and `verify_handoff_probes` now enforces it, but §5/§13 has not been
  amended to say so (that is item (2) above) **and the first bluff-dogfood has still not re-run since
  2026-06-11 promotion.** Close both to actually retire RF-1.
- **RF-3b — the boot-transcript echo that could close #159 on evidence** (cheap; a 12-supplement-old
  unclosable ticket).
- **Coherence-spine RF-5 FAIL-trap + the residual self-blindness** — the ARCHITECTURE re-read (lane 1)
  cleared the *demonstrated* self-blindness, but **RF-5 (the two doc↔doc walkers disagree on corpus scope)
  is a live correctness bug**, unfixed.
- **RF-4 — CLAUDE.md §5 "handoffs immutable" vs the §13 fill/fold lifecycle.** Standing doctrine
  contradiction; reconcile to the ADR-94 status-line-mutable precedent or carve a §13 exception.

### (4) Held + carried (do NOT advance without an explicit operator unlock)

- **P5 (`#130` hub self-prune) → P6 (`#221` fleet roll n=2+): still WAIT** (operator rule from the filled
  supplement — do not onboard n=2+ through a moving corpus while RF-1/RF-4 and the sandbox are in flight).
  P6 stays gated on **#225** (surgical precommit carrier) + FU **#250** (codemap-freshness component).
- **The rot-algorithm / continuous-conformance build: defer-until-after-sandbox** (operator rule — the
  sandbox and the rot-report share the observer machinery; build the sandbox first, then the rot-report on
  top). The Fable design (`docs/audits/2026-07-04-rot-algorithm-design.md`) stays a landed design, not a
  filed build, until the sandbox proves the shared primitives.
- **Standing debt — ai-council `CLAUDE.md` A2-stale (off-repo, LIVE):** `last_reviewed` < last edit; the
  now-**deployed** `canonical_freshness` gate **WILL block ai-council's next real commit** until a **genuine
  re-review + re-stamp** (never a faked stamp) — the transferred organ dogfooding itself in a consumer.
- **Smaller adjacent (unchanged):** `#220` MODIFY/semantic-drift axis (presence ≠ currency — verify-first
  whether any organ gates a meaning-change-without-version-bump), `#242` ADR status-flip coherence, `#210`
  journal-wrap no-ff standing rule, `#243` the #168-hard vs Fable-WARN JOURNAL-leg conflict.

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **The strategic frame (READ FIRST — it is the program this residual sits inside):** the prior bundle's
  **filled** `docs/handoffs/2026-07-04-dev-knowledge-architect/SUPPLEMENT.md` (the re-sequenced
  deployment · sandbox · tests program, P5/P6 WAIT, phase order) + its `RESIDUAL.md` §4 (the four Fable
  reviews in full — not re-narrated here).
- **The Slice A review input (§4.1 — the PRIMARY):** `deploy/lived_sandbox/` (the package),
  `tests/test_lived_sandbox.py` + `tests/fixtures/lived-workflow/`,
  `docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` (the 2 CRIT + 2 HIGH review),
  `JOURNAL.md` top entry (the program-session Did/Result/Next).
- **The handoff-generator (§4.2):** `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py` (the
  `_classify` anti-bluff rung), `templates/handoff/v5/*.tmpl`, and `protocols/HANDOFF_PROCESS.md` §5/§13
  (the spec to reconcile + version-bump).
- **RF-2 hub-arm (§2 lane 2):** `scripts/arm_hooks.py`, `audit.py::check_hooks_armed`, `.claude/settings.json`.
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`, `CLAUDE.md`
  — referenced by pointer, enforced mechanically (§3), never re-narrated.
- **The four Fable reviews (carried adjudication input — §4.3):** `docs/audits/2026-07-04-*.md`.
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
> **RF-1 corrective (NOW STRUCTURAL — read this).** The Fable handoff-adoption review found every recent
> architect bundle printed its probes' answers as `expected: <value>` hints — which §5 says makes a probe
> **bluffable and rejected**. The operator **re-ratified** withholding and this repo now **enforces it
> structurally**: `verify_handoff_probes._classify` FAILs any probe that ships an answer hint (row-scoped),
> so the erosion cannot silently return. This bundle **deliberately withholds the answer values** below —
> no counts, SHAs, dates, verdicts, or orienting lines are stated. That withholding IS the teeth. The pass
> criterion is **"answered from the live source at check-time,"** never "matches a remembered number."
> Where a branch-context note appears, it is there only so CC knows *which* live value to compare, not the
> value itself.
>
> **Branch note (load-bearing for P3/P7/P8).** This bundle was generated on
> `docs/2026-07-04-architect-handoff-2` **off `main` (`a523fca`)**, tree clean, in sync with
> `origin/main`. **ALL window work is on `main`** — there is no parallel feature branch whose values
> differ (the sandbox + handoff-generator lanes already merged `--no-ff`). This handoff's own commit + the
> later `/ship` `--no-ff` merge move HEAD and push `main` ahead until pushed. **Re-derive; do not trust
> this line.**
>
> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS
> region is empty → the assembler folds nothing → the incoming §13(d) operator-context beat fires **FULL**
> (P1 gate below). **P8's live answer includes the supplement's fill-state — check it.**
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
the beat fires **FULL** (*"what off-repo context — intent, priorities, findings not in the repo, changed
decisions?"*) — **not** a narrowed "anything changed since?" — unless the operator fills the supplement
first (`supplement filled`), in which case its ANSWERS fold into `PASTE_THIS.md` and the beat narrows.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, RF-1**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? (It **grew by one this window** — RF-2 added a hub-arm check; the number + name are the live answer.) | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? (It was re-stamped this window by the currency re-read — verify the stamp is not now behind a *later* edit.) | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? Note the claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-04-dev-knowledge-architect-2/` ∩ `HANDOFF_PROCESS.md` §13 (∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-04-dev-knowledge-architect-2/SUPPLEMENT.md` — is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **`sandbox`** group (new this window — the [#252] epic), and which `#id`s are in the **`code-edge`** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

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
   values are deliberately absent (RF-1, now structurally enforced)**: the pass criterion is **"answered
   from the live source,"** never "matches a remembered number." P7 is the headline (GREEN/RED +
   dispositioned-WARN count + any `[stale]` line). P8 pins the bundle shape **and the live supplement
   fill-state** (empty at generation; may be filled by read-time). First check which branch is live (P3) —
   this window, like the last, has no parallel feature branch, so `main` is the single source of truth.

---

=== SUPPLEMENT.md ===

# ARCHITECT SUPPLEMENT — dev-knowledge architect, session wrap 2026-07-04

Outgoing-architect answers for the incoming session. Pairs with CC's repo-derived bundle (BOOT + RESIDUAL + PROBES). This is the off-repo half — rulings, dispositions, forward plan — none derivable from committed state. **Re-verify every state claim against live HEAD before acting** (a point-in-time supplement is not current truth). Supersedes any earlier wrap draft (this one reflects Slice A *shipped*).

## State snapshot (both lanes, final)

- **main = a523fca, pushed** (local == origin). Tree clean. Worktree fully cleaned (no linked worktrees, no stale `feat/*` or `worktree-*` branches, no `.dev-knowledge-*` orphans).
- **Sandbox Slice A SHIPPED** (merged `--no-ff`, Codex-hardened): `deploy/lived_sandbox/` (spawn + isolation + cli). Spawn viability PROVEN empirically; isolation PROVEN (configA-sentinel/configB seam). doc-counts current at 1216.
- **Handoff-generator lane INTEGRATED** (`9d5ebe5`): `gen_handoff.py` + anti-bluff rung + templates + size-warn. Anti-bluff is now structural (option b) — the erosion cannot silently return.
- **RF-2 hub self-arm** (`2e7b072`) + **ARCHITECTURE currency + coherence RF-1 surfaces** (`fbf88ae`) + **OneDrive P0 guard** all landed and verified.
- **Open for operator:** rotate the leaked `ANTHROPIC_API_KEY` (operator-only — CC blocked by the P0 guard from writing `.secrets/.env`, which is OneDrive-redirected). No build impact.

## Q1 — Strategic intent (way-of-working level)

**Prove the COMPOSED system end-to-end on a real consumer — close "presence ≠ enforcement" at the workflow level, on ai-council.** Slice A proved the sandbox *foundation* (spawn + isolation). What's missing is the *measuring instrument*: Slice B's OUTER observer + the essence-spec `engages:` oracle + the six-hook arc + the seeded EXPECTED-BUT-SILENT closure — and then the **first ai-council consumer-run**, which is the operator's stated priority #1 ("the hub tested on ai-council like a sandbox") and is **still undelivered**. Phase 0 (turn the standard inward — the hub meets its own standard) is ~60% done; Phase 1's foundation is proven but its instrument is not built. Q1 = build the observer, then run the first consumer-sandbox on an ai-council clone.

## Q2 — Tensions weighed, where I landed

- **Split the sandbox at the spawn-isolation boundary** (Change #2): landed on split because `claude -p` spawn is the no-precedent part — prove + Codex-review the foundation before building the observer on it. **Validated** — the split caught a false-green isolation bug (Codex CRIT: `IsolationResult.passed` was true even when both runs failed).
- **Ship-Slice-A-then-wrap vs plow into Slice B** (this session): landed on wrap — Slice B is a fresh large build deserving clean context, and CONTEXT SELF-EVAL triggered (≥3 unresolved follow-ups).
- **Fleet-currency signal:** landed on **D5 (coverage) is the dominant signal, not D1 (stamp)** — measured the matrix, don't patch dates.
- **ai-council CLAUDE.md stale:** landed on **timing, not bug** — the gate was born in the same commit it "should have caught"; the next commit hard-blocks; the standing sweep is the proactive catch. Don't patch the date.

## Q3 — Considered + rejected (do NOT relitigate)

- **Anti-bluff option (a)** (ratify drift-reference hints in the bundle) — REJECTED for option (b) (strip values by construction; hints → JOURNAL). Built.
- **Fable consult on the core plan** — REJECTED: the four reviews ARE the consult (convergent, no contested fork). Codex is the heterogeneity mechanism at implement-time, not a fresh consult.
- **The separate 8-finding Phase-0 recon** — RETIRED in favor of plan-first-self-verifying builds (each build verifies its finding in the plan phase — fewer round-trips).
- **LLM-gating on semantic properties in the sandbox** — REJECTED (false-positive death-spiral). Model-mediated engagement is observed-and-reported, never gated.
- **Worktree or container for the sandbox** — REJECTED (shared `.git`/stash class; Windows-native fidelity is the point). Throwaway `mkdtemp` clone + isolated `CLAUDE_CONFIG_DIR`.
- **The §5 edit inside the handoff worktree** (Q1 ruling) — REJECTED (ARCHITECTURE.md collision + freshness-gated). Decoupled to serial integration.
- **Rot-algorithm build-now** — NOT rejected; deferred to Phase 2 (feeds P5). Don't build it before the sandbox.

## Q4 — Open questions (unresolved / deferred)

- **§5/§13 spec-arc sequencing** — see B (ruled: after Slice B).
- **#164 formal disposition** — amend-then-close vs keep-open (cross-repo probes + v4-prose removal remain ADR-83-gated). Architect's call at integration.
- **#251 deploy-CLI red** (`test_cli_execute_success_reports_branch`) — stale-test vs real UX regression (the success render dropped the `record_branch` string). Decide, don't carry indefinitely.
- **Semantic content-drift tier** (fleet matrix dim-2) — deferred behind an n=2-adoption + findings-acted-on gate.
- **Load-gauge** — I ruled it lands BEFORE more mechanisms (the one entropy source with no counter-tactic); confirm still un-built and prioritize in the Phase-0 batch.

## Q5 — Decomposition rationale (the task-graph shape)

Three dependency-gated phases: **Phase 0** (self-application — cheap, unblocks everything) → **Phase 1** (sandbox — gated on RF-2, else it measures a facade) → **Phase 2** (currency + fleet — gated on corpus-settling). WHY: safety before momentum (P6 multiplies unfixed risk across 4 repos); the sandbox is the acceptance instrument so it precedes the fleet; the composed-workflow proof needs the foundation (spawn+isolation, Slice A) before the observer (Slice B). **Do NOT redo/re-decide:** the P1–P4 mechanism (shipped n=1); the sandbox-oracle decision (essence-spec `engages:`); the "what NOT to add" refusals; the 4 sandbox-plan corrections; Slice A's isolation contract (Codex-hardened); the anti-bluff option-b decision; the fleet D5>D1 reframe; the ai-council timing verdict.

## Q6 — Off-repo context

- **Operator priority #1 is STILL undelivered:** prove the hub on ai-council like a sandbox — needs Slice B observer + the first consumer-run. Everything else is subordinate to reaching that.
- **Worktree-isolation lesson (methodology-relevant):** a worktree isolates the CHECKOUT, but an absolute path to the primary bypasses it (the handoff session mis-rooted edits into the primary via subagent-reported absolute paths; recovered, no work lost). Future parallel-worktree delegates MUST operate strictly within their worktree dir (relative paths). CC saved memory `worktree-edits-land-in-primary-via-absolute-paths`.
- **Key rotation pending** (operator-only; the P0 guard blocked CC from `.secrets/.env` — the guard working on its author, the best possible proof it fires).
- No LLM-budget ceiling.

## A — Slice A acceptance bar (ACCEPTED)

I **accept** Slice A; the isolation contract IS the seam I want, and the boundary does NOT move — Slice B builds the observer ON this contract:
- `CLAUDE_CONFIG_DIR` governs user-level hooks (proven configA/configB); project-level hooks in the clone's cwd still fire independently.
- Teardown blast-radius anchored to the system-temp dir (Codex fix), `_rmtree_guarded`.
- Protected env: `CLAUDE_CONFIG_DIR`/`ANTHROPIC_API_KEY` pinned LAST, `CLAUDE_PROJECT_DIR` popped (so `extra_env` can't override; Codex fix).
- Exit-gating: `passed` requires `exitA==0 AND exitB==0` (the false-green fix).

**One re-verify at Slice B start (not a Slice A defect):** confirm the isolation still holds when the inner session does REAL work — the six-hook branch→edit→commit→wrap arc — not just the sentinel probe. I.e., the arc's own hooks fire in the isolated child as expected. That is the first Slice B check, before the observer is trusted.

## B — Sequencing the §5 spec-arc vs the sandbox → AFTER Slice B

**Ruling: do the §5/§13 spec-arc AFTER Slice B, not before.** Reasoning:
- **No technical collision either way.** The ARCHITECTURE.md "collision" only bites if the two run CONCURRENTLY (parallel worktrees). Sequential in one lane, there is no conflict — so the choice is about value/momentum, not safety.
- **§5 is orthogonal to Slice B.** Slice B touches `deploy/lived_sandbox` + manifest + observer; it does NOT touch HANDOFF_PROCESS or the reconciled_with docs. An un-settled §5 does not interfere with Slice B at all.
- **§5 is additive bookkeeping** — it NAMES an already-true invariant (the rung already enforces it; §5 already says "never the answer... rejected") + a version bump. Interrupting the priority-#1 deliverable (Slice B + ai-council run) for bookkeeping is backwards.
- **The corpus doesn't need §5 settled for the bundle** — anti-bluff is already structural (option b built), so a generated bundle is already clean regardless of §5.
- **Efficiency note:** Slice B will touch ARCHITECTURE.md anyway (register the sandbox check). The §5 ARCHITECTURE.md re-stamp CAN fold into that same currency pass (one re-read covering both the sandbox-check-count and the 5.4 bump) to avoid a double re-read — architect's call at integration.

## Audit disposition (the four Fable audits + the Codex review)

| Audit                                     | Key findings                                                                                                                                            | Disposition                                                                                                                                                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fable architecture review**             | RF-1 OneDrive P0, RF-2 hub self-arm, RF-3 honest-limits, §6 sandbox, RF-6 consult-lane, RF-7 routing, RF-8 dead v4 checks, RF-9 worktree-context        | RF-1 ✅ built · RF-2 ✅ built · §6 sandbox foundation ✅ (Slice A) · RF-3/6/7/8/9 → Phase 0 batch / Slice B                                                                          |
| **Handoff-adoption review**               | RF-1 anti-bluff, RF-2 generator, RF-3b boot-echo, RF-4 immutability, RF-5 cp1252, RF-6 re-narration, RF-7/8/9                                           | RF-1 ✅ built (option b) · RF-2 ✅ built (generator) · RF-4 → §5 spec-arc (deferred, see B) · RF-3b/5/6/7/8/9 → not built                                                           |
| **Coherence-spine review**                | RF-1 stale surfaces, RF-2 ESSENTIALS↔PLAYBOOK inversion, RF-3/#220 currency≠presence, RF-4 granularity, RF-5 FAIL-trap, RF-6 spec-absent→WARN, RF-7/8/9 | RF-1 ✅ (L318/L392 cleared via currency; PLAYBOOK:253/256 + RF-8 docstrings pending) · RF-3 → fleet-sweep (scoped, not built) · RF-5/RF-6 → Phase 0 batch · RF-2/4/7/9 → not built |
| **Rot-algorithm design**                  | `rot_report.py` — reverse-reference multimap + 3 existence predicates (dangling-path / dangling-wiring / tombstone blast-radius) + `--impact`           | **DESIGNED, NOT BUILT** · Phase 2 · feeds P5 · Track-B sibling of the fleet-currency sweep                                                                                        |
| **Codex review — Slice A** (gpt-5.5 high) | 2 CRIT (isolation false-green; teardown blast-radius) + 2 HIGH (env-key override order; spawn-failure handling)                                         | ✅ all fixed + tested; isolation re-PROVEN. (A code-review artifact for our Slice A build — lives in `docs/audits/` per the review-artifact convention.)                           |

## Forward plan (phases + real status)

**Phase 0 — self-application (~60% done):** ✅ OneDrive P0 · ✅ RF-2 self-arm · ✅ anti-bluff · ✅ coherence RF-1 (L318/L392). **⬜ Remaining batch (disjoint from sandbox):** coherence RF-5 FAIL-trap (one function move + tests), RF-6 spec-absent→FAIL, cp1252 + ASCII-output regression test, honest-limits in DEFINITION_OF_DONE, **load-gauge** (before more mechanisms), PLAYBOOK:253/256 RF-1 surfaces, validate_reconciliation RF-8 docstrings, #251 disposition.

**Phase 1 — sandbox (foundation proven, instrument not built):** ✅ Slice A (spawn + isolation, Codex-hardened). **⬜ Slice B [#252]:** OUTER deterministic observer (transcript + git-state + hook-stdout, never inner narration — LESSONS 2026-06-04) + essence-spec `engages:` oracle (extend `deploy/manifest-v1.2.0.yaml` components with `{trigger, observable, expect}` + `release_lint` lint) + six-hook branch→edit→commit→wrap arc + ≥1 command acts + **seeded EXPECTED-BUT-SILENT closure** (disable a should-fire hook, prove the observer FLAGS it — the harness leg-e). Refusals: no nightly, no LLM-gating, no container, inner never self-certifies, never push to a live remote. **⬜ First ai-council consumer-run** (`cli --consumer <ai-council-clone>`) — this delivers priority #1. **⬜ RF-3b boot-echo** (closes #159).

**Phase 2 — currency + fleet (scoped, not built):** ⬜ rot-report (feeds P5) · ⬜ standing fleet-currency sweep (matrix measured: D5 coverage dominant, 12 uncovered cells, corp-ops zero-mesh) — Track-B family with rot-report · ⬜ P5 hub self-prune (#130, Opus/plan-first) · ⬜ P6 fleet roll n=2+ (gated: Phase 0/1 + D4 + v1.3.0 cut + standing sweep + **per-consumer mesh transfer not just presence** + mesh-commit bumps target stamp + #225/#249/#250; corp-ops needs the whole mesh, corp-monorepo/sca need the freshness gate) · ⬜ semantic content-drift tail (deferred behind adoption gate).

**Integration follow-ons:** §5/§13 spec-arc (after Slice B, per B) · #164 disposition · corp-sca version-provenance backfill.

## First next-session actions

1. Boot + orient (VISION/ARCHITECTURE quotes via CC). Confirm open verification threads (below).
2. Build **Slice B** [#252] — the observer + oracle + arc + seeded-silent closure. First check: re-verify isolation holds under the real arc (not just the sentinel).
3. Run the **first ai-council consumer-sandbox** — delivers priority #1.
4. In parallel (disjoint, worktree — enforce the relative-path lesson): the **Phase-0 batch** (RF-5/RF-6/cp1252/honest-limits/load-gauge/PLAYBOOK/RF-8/#251).
5. §5 spec-arc + #164 disposition after Slice B.

## Open verification threads (confirm at read-time — do not assume)

- Key rotated? (operator, pending)
- #251: stale-test or real regression?
- Any drift on main since a523fca?
