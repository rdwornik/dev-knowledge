=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-20-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-20-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Get ARC-5 unblocked at the decision layer. Ten `[E8]` decisions (R1, R1b, R2–R8, R12) are unruled and several waves cannot open without their pick, so the first substantive move is one bounded-pick message to the operator — led by R12, which decides what the arc's closure target even is. Then settle whether W1 closes, given that its operator render-witness does not exist and its Codex review artifact was never archived. Task-state: the `[E8]` theme in `BACKLOG.md`.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `main`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-20-dev-knowledge-architect — the part the repo does not already encode

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
**Standing (dispositioned — expect them, they are not news).** The register carries four families:
the `no_ff_merges` journal-wrap/transcript-archive entries, the `undeclared` HANDOFF_PROCESS
dependents (BACKLOG · VISION · ai-council · ESSENTIALS · PLAYBOOK · SESSION_SETUP), the `doc_rot`
BACKLOG-task entries (`#262`, `#278`, `#332`, `#344` — the latter two carrying review dates), and the
`reconciled_versions` CONTRIBUTING-template entry. Read them at
`ecosystem/disposition-register.yaml`; P7 re-derives what is live.

**NEW this window, and DELIBERATELY NOT dispositioned — the one flag to actually look at.**
`VISION.md`'s `last_reviewed` aged past the 30-day cadence by pure calendar rollover; the file itself
was not touched. It is **neither stamped nor dispositioned, on purpose.** `last_reviewed` means
*re-read end-to-end and confirmed accurate* — so re-stamping to reach a green number would convert an
honest signal into a false one, and dispositioning it is the same move in a different costume. The
real fix is a genuine re-read, owned by **[#368]**. Treat this flag as **true**, not as noise: it is
the arc's own declare-instead-of-fix pattern showing up on the arc's own board.

**Already resolved — should NOT reappear.** Two WARNs were self-inflicted earlier in the window and
were fixed rather than reported: a `doc_rot` trip on `[#368]`'s own filing, and a `doc_claims` drift
after the boundary-headers test landed (`ecosystem/doc-counts.md` regenerated). If either surfaces
again, that is a regression, not the standing state.

**Structural pressure worth naming.** `[#355]` now sits within a couple of characters of the
`doc_rot` per-task cap, and it is the *second* ticket pinned there. Any further edit to it trips a
new WARN — which is the concrete case **[#364]** argues from, not a maintenance annoyance.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
ARC-5 moved from *planning* to *execution* this window. Terse map — detail is in `JOURNAL.md`
(newest-first) and the `[E8]` theme in `BACKLOG.md`; do not re-read it here.

- **[E8] filed as a living theme** — the ARC-5 plan of record (wave map W1–W7, frozen closure
  contract, unruled decision table) landed in `BACKLOG.md` rather than an ADR, because an ADR is
  immutable and a wave map must evolve. Plus the census declaration test + baseline.
- **W1 (VISIBLE BOUNDARY) merged** — reader-visible ownership headers generated from the `#312`
  marker substrate, plus `.vscode` region decoration declared as fleet carrier material.
  `[#352]` · `[#321]` · CLAUDE.md §12 v2.43–v2.44. **Merged, not closed** — see §4.
- **W6 legibility half merged** — the four ARC-4 rulings inoculated into PLAYBOOK + ESSENTIALS.
  The *enforcement* half is unbuilt and owned by **[#354]**.
- **ARC-5's first enforcing mechanism** — the residual-completeness gate, plus the residual-rule
  declaration that binds its exemption.
- **Census findings discharged into tickets** — `[S22]` (`[#357]`–`[#362]`), including the
  phantom-enforcement class the four-state ledger cannot express (`[#359]`).
- **Session-close hygiene** — `[#368]` (honest-stamp / VISION re-read), `[#369]` (unwired
  `boundary_headers --check`), `[#355]` evidence to n=4.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### 1. Ten decisions are UNRULED and blocking — collect them in ONE bounded-pick message

`[E8]`'s decision table (R1, R1b, R2–R8, R12) is **entirely unruled**. Recommendations are attached
to most, but *a recommendation is not a ruling*, and several waves cannot open without their pick:
W2 needs R1/R1b, W4's very shape is R2, W3's deletion path is R3 and its enum is R4, W5's
one-organ-vs-three is R5. **The successor's first substantive move is a single bounded-pick message
to the operator** — not eight separate asks across eight sessions, and not silently adopting the
recommendations as though they had been ruled.

**R12 is the sharpest and has no recommendation attached.** Closure clause (b) — "everything still
unenforced has moved to declared-unenforced" — is **not achievable in one arc** at the measured
N_silent, which would mean dispositioning every silent rule, and that figure is a *floor* (the ADR
corpus is unswept, `[#357]`). The two live options are **(i) NARROW** the arc target to a bounded
load-bearing slice, or **(ii) GATE THE GROWTH** of silent rules instead of draining the pool. This
decides what ARC-5 *is*, so it should lead the bounded-pick message rather than trail it.

### 2. Does W1 actually close? Two independent gaps — and neither is "merge it harder"

W1 merged, but the closure contract is explicit that **"NOT closure: waves merged, ship-gate green,
tests passing, items marked done."** Two clauses are open:

- **(f) — the operator's own-words confirmation does not exist.** `[#352]`'s Done-when is the
  operator *seeing* the decoration render. That witness has not happened. `[#352]` is deliberately
  left open; **do not close it on the strength of the merge.**
- **(c) — W1 has no archived Codex review artifact.** The per-wave standing requirement is a Codex
  review pre-merge *and* an educate artifact with file-level before→after. W1's reviews were run
  (a CRITICAL, several HIGH, then further findings, all genuinely fixed), but **the artifacts were
  never written to `docs/audits/` and are now unrecoverable** — the findings survive only as
  commit-message prose. So the review *happened* and the evidence *doesn't exist*.

**The design question this raises is bigger than W1:** clause (c) is itself a MUST-shaped rule with
no mechanism — nothing gates a wave merge on the presence of its review artifact. ARC-5's own
closure contract is, by its own census definition, **silently unenforced.** Either it earns a
mechanism, or W1 is waved through and the contract is decorative from wave 1 onward. That choice
should be made explicitly, now, at n=1 — not discovered at W7.

### 3. Wave sequencing is open below the pain-priority ordering

The wave map is ordered by operator pain, not dependency. Two live scheduling facts: **W6 may run
first or in parallel** as a file-disjoint doc lane (its enforcement half, `[#354]`, is unbuilt and
would inoculate rulings before later waves generate more), and **W2 inherits `[#355]`**, a live
false-positive in `fleet_parity` that has already **trained `SKIP=audit-health` bypasses** — a gate
teaching the operator to route around it is a compounding cost, which argues for W2 early regardless
of elegance. Whether W1 must formally *close* before W2 opens is unruled and interacts directly
with item 2 above.

### 4. Two small structural items that will otherwise be rediscovered

- **[#369]** — `boundary_headers.py --check` is the only generated surface with no regen-and-diff
  pre-commit hook; every sibling has one. Not a hole today (the suite catches it at ship-gate), but
  it is an inconsistency in the enforcement mesh, and it moves the gate count when wired.
- **[#364] / the `doc_rot` cap** — two tickets are now pinned against the per-task character cap.
  The cap is doing real work, but at the cap it converts *any* honest edit into a new WARN, which
  pushes toward silence. Worth ruling before a third ticket arrives there.
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
> **Branch note.** This bundle was generated on branch `main`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-20-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-20-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-20-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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
The thesis grew from "recorded ≠ enforced" to "recorded ≠ enforced ≠ EFFECTIVE". Four
green-that-means-nothing instances in one day: phantom enforcement (#359, a rule naming an absent
mechanism); a Codex review that filtered its own subject out of the diff and returned a verdict
(#363); a colour test whose grey predicate also satisfied navy so it passed either way; and a
one-directional doc↔code check reporting agreement it never established. Next session's
way-of-working goal: treat GREEN as a claim to falsify, not a result to trust — prove by violation.
The residual-completeness gate built this session is the template: it shipped only because it was
demonstrated RED on a real unfilled bundle, not because it was registered.

PAIN → BUILD MAP (why the operator cares, one line per wave; the build detail lives in [E8], not here)
- W1 visible boundary — the colours, his single most-repeated ask across ~20 sessions (MERGED, render witness pending).
- W2 structure — "why do the folders differ": assets/→config/, Pyrefly universal, root-vs-config rule.
- W3 lifecycle — intake→ADR→close→DELETE: the process problem, real deletion, accretion brake.
- W4 archive — he must SEE live vs archived; archiving coupled to status, precedes W3.
- W5 guards — the worktree pain; hub goes read-only, handoff the sole writable surface.
- W6 canon+prompt — inoculation legibility (shipped) + the co-change enforcement half ([#354]).
- W7 testing+fleet — evidence gate + the fleet-state collector.

2. TENSIONS WEIGHED
- Measure-the-whole-corpus vs ship-mechanisms → ship, with a measured baseline behind it (320
  MUST-shaped rules, 176 silent = 55%, a FLOOR — docs/decisions/ unswept, #357).
- Ledger as report vs as mechanism → mechanism; a one-off table decays.
- Generate the .vscode config vs eliminate the state → elimination (two regexes keyed on markers
  carry no per-region state, cannot rot). Recorded as a [#352] Done-when amendment. #329 still
  genuinely needs generation from parity-surfaces.yaml.
- Markers vs headers as boundary source of truth → markers win; headers generated from them.

3. CONSIDERED + REJECTED — do not relitigate
- Narrowing the arc to a ~55-rule slice → REJECTED by the operator. Fix ALL rules, prioritised,
  goal never lowered. ARC 5 is the first tranche of a tracked burn-down.
- A fifth ledger state for advisory rules → REJECTED; a MUST-shaped-only denominator drops them out.
- Ratifying the six off-canon intake statuses → REJECTED. One enforced pattern instead:
  SEED→DRAFT→READY→{ACCEPTED|CONSUMED|SUPERSEDED|REJECTED}, the "to what" in required companion
  fields; naming YYYY-MM-DD-<class>-<slug>. Dissolves the id:14 triple.
- mypy as a sanctioned divergence → REJECTED by the operator. Python stack, tooling universal →
  Pyrefly (stable 1.0 May 2026, ships AI-agent workflow docs incl. Stop-event hooks matching this
  fleet; `pyrefly init` migrates from mypy config cheaply).
- Mid-arc re-planning → REJECTED. The plan governs; new scope goes to BACKLOG, execution does not swerve.

4. OPEN QUESTIONS — unresolved / deferred
- [#352] W1 is MERGED, NOT CLOSED — closes only on the operator's render witness, which has not
  happened. Closure clause (f) open.
- W1 clause (c): no archived Codex review artifact — the reviews ran, the evidence was never
  written to docs/audits/. Clause (c) is itself a MUST-rule with no mechanism: the closure contract
  is silently unenforced from wave 1. Rule it now, at n=1.
- Two failure classes the four-state ledger cannot express: phantom enforcement (#359) and orphan
  enforcement (a mechanism no rule declares).
- codex-review scoping (#363): filters mixed diffs to their code subset; can review a fraction while
  reporting a whole-diff verdict. Until fixed, invoke `codex exec` with files named explicitly.
- R8 (corp #38) is OUT — the architect handles hub + methodology only, nothing corp-side.

5. DECOMPOSITION RATIONALE — what NOT to redo
The ARC-5 plan of record is BACKLOG theme [E8] (NOT an ADR — a wave map must evolve). Read [E8];
do not re-file it, re-derive the baseline, or re-adjudicate the nine seeds (terra killed none; W1
and W4 are the seedless waves; seeds 5 and 6 map to W2/W5 by content). Recommended first move: the
STRUCTURE wave (W2) — assets/ dissolution (operator GO recorded; relocate to config/ first, then
delete), the Pyrefly rollout, and the root-vs-config placement rule (root only for tool-mandated
files like pyproject.toml — a named closed exception list; everything else to config/). It is where
the operator's granted rulings sit and what he sees in every repo. The ARCHIVE wave now PRECEDES the
lifecycle wave: archiving is coupled to status (terminal statuses move the file to <folder>/archive/,
so it is a file move needing a reference-integrity check — reversing the inbound "stay-in-place"
convention on the operator's explicit reasoning that he must SEE live vs archived).

6. OFF-REPO CONTEXT
- Operator rulings this session, binding: .vscode is SHARED FLEET CONFIG (hub-owned). Consumers get
  READ-ONLY hub access — read and query, never write; the sole writable surface is docs/handoffs/,
  which another repo may trigger. Simplifies the #344 Ask-2 guard from a HEAD-bound token to a
  path-scoped write deny; aligns with ADR-28 (Layer 2 is passive, not an execution engine).
- ROLE EXPANDED: the architect owns Python engineering standards and cross-repo dependency
  management (real incident: one repo lacked pytest requirements another had), tooling choice, and
  folder/file naming — not only LLM working-methodology.
- The sort-order incident surfaced the .vscode shared-vs-personal boundary: personal view
  preferences (sort order) must NOT live in fleet-canonical config. This is a W2 boundary question.
- NOTHING was deleted this arc and NO backlog task was closed (116→132+). The visible pain the
  operator still sees — the assets/ folder — is W2 work, granted but not executed.

BINDING — do not relitigate
- The baseline is established: 320 MUST-shaped rules, 176 silent (a FLOOR — docs/decisions/ unswept).
- The four-state ledger schema stands.
- The declaration test stands: on-surface AND bound to an open ticket. Neither condition suffices alone.
- .vscode is SHARED FLEET CONFIG, hub-owned.
- The hub is READ-ONLY to consumers; docs/handoffs/ is the sole writable surface.
- Pyrefly is universal across the fleet — NOT a sanctioned mypy divergence.
- Archiving is coupled to status, and the ARCHIVE wave PRECEDES the lifecycle wave.
- The goal is ALL rules, prioritised — not a bounded slice. The goal is never lowered.

DO-NOT-REDO
- [E8] is filed as a BACKLOG theme — do not re-file it or convert it to an ADR.
- The baseline is measured — do not re-derive it.
- The nine seeds are adjudicated — terra killed none; W1 and W4 are the seedless waves; seeds 5 and 6
  map to W2 and W5 by CONTENT, not by label.
- The residual-completeness gate is built AND demonstrated RED on a real bundle — do not rebuild it.
