=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-11-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-11-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Plan the post-plan-v3 frontier: 2026-07-10 executed most of plan-v3 §D (ADR-101 hermetization **ratified**, #299 G8 runbook fix **closed**, #303–#309 filed — see RESIDUAL §2), so this session resumes from what remains. The **filled `SUPPLEMENT.md` sets the priority** (operator, this fill): the P1 headline is a **fleet universalization/hermetization boundary audit** across dev-knowledge / ai-council / corp-monorepo — an evidence-based methodology-vs-project boundary per surface → a divergence matrix → PLAYBOOK → mechanisms (carriers/gates), because Wave-1 n=2 proved *enforcement* in effect but never *structural uniformity*. **#270 (operator-load gauge) drops to position 2.** The repo-derived legs behind them: **B-S2 corp onboarding** (unblocked; a dedicated ADR-41 corp chat), the **EPIC G QA-role** decomposition (waits on the operator's functional QA intake session), **EPIC H** model-routing doctrine, the hermetization build follow-ups (#306/#307). The operator's **execution-first bar governs** — visible outcomes over governance. Start from the folded **SUPPLEMENT** (the operator's charter) + `BACKLOG.md` (the spec), with `docs/handoffs/2026-07-10-dev-knowledge-architect/PLAN.md` as the now-largely-executed plan-v3 of record.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-11-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-11-dev-knowledge-architect — the part the repo does not already encode

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
All drift-flags this window are **STANDING and dispositioned** in `ecosystem/disposition-register.yaml`; the handoff-generation arc introduced **none new** (the bundle was authored net-neutral — no new `doc_rot`, no new edge). Standing classes, by reference: `no_ff_merges` — the grandfathered journal-wrap + transcript-archive direct-to-main commits (`#210` is the standing-rule proposal that would retire the per-instance dispositions); `doc_rot` backlog-accretion — `#262` + `#278` (dispositioned; self-induced trims kept net-neutral); `undeclared_edges` — the six tier-1-doc → handoff-process prose edges (`#241`). The `handoff_probes` P1a/P1b/P8 SKIPs are **environmental, not drift** — grep/sed/ls PATH-absence in a bare PowerShell shell; they bind `[OK]` (10 probes) the moment the standard tools resolve (git-bash / the pre-commit shell), so a PowerShell-only ship-gate reads a spurious RED that clears under the real gate. Run **P4/P6/P7** for the live verdict / count / `[stale]` — this file names none by design. _[witnessed — `audit.py ship-gate` + `health` re-run live this generation under git-bash: GREEN / OK, 11 WARN dispositioned, zero new content drift]_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = the **2026-07-10 execution arc** (the plan-v3 §D session; 5 JOURNAL entries + ~40 commits since the 07-10 bundle was cut at `3bc2adb`). The map (detail in the `JOURNAL.md` 2026-07-10 entries + `git log 3bc2adb..HEAD`):
- **ADR-101 hermetization RATIFIED** (Proposed→Accepted, `1d2d962`) — sanctioned top-level set + 11-class audit-name enum + refusal-gate spec; **Amends ADR-34**; `templates/audit-template.md` added. Lands plan-v3's **d.iii** (prospective + grandfather + CLASS enum).
- **#299 CLOSED** (`44da4b8`, fire-test basis) — G8 runbook Layer-6 verify exercises the hook's real interpreter. **This unblocks B-S2** (the n=2 runbook gate's precondition).
- **#303–#309 filed** + #262/#302 augmented (`f436e33`) — the morning-verdict batch: seeder child-class-awareness (#303), runbook fixes (#304/#305), hermetization build tickets (#306/#307), branch-protection parity (#302/#309).
- **#310 filed / #311 closed** — cold-bundle annotation surface (M15, `cec46d7`); fleet_health groom-parser twin fix (`7024ec4`).
- **Lane-N night consolidation integrated** (`bee5b0d`) — 6-corpus census + morning brief + changelog review (`docs/audits/2026-07-11-*`).

State pointer: `BACKLOG.md` — **7 themes / 20 stories / 89 tasks** (§4 sets the current priority — the filled SUPPLEMENT's universalization/hermetization audit leads; #270 at position 2). _[witnessed count — `validate_backlog.py` re-run this generation; the arc itself is recall — reconstructed from the 2026-07-10 JOURNAL entries + `git log`, not lived this session]_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Priority per the FILLED `SUPPLEMENT` (operator, this fill) — read it first; it supersedes the repo-derived ordering below.** The operator's **P1 headline is a fleet universalization/hermetization boundary audit** (dev-knowledge / ai-council / corp-monorepo → an evidence-based methodology-vs-project boundary per surface, a **divergence matrix** with per-item disposition, then PLAYBOOK + mechanisms — *not* prose; "all onboarded = all OK" is a **rejected** claim shape — Wave-1 n=2 proved *enforcement* in effect, never *structural uniformity*). One big read-only comparative fan-out that **builds on** (never repeats) the 2026-07-11 corp root-hygiene audit + naming census + ADR-101 + the QA n=2 scorecard, ending in a matrix + dispositions, **never a verdict**. **#270 is demoted to position 2.** The full charter, tensions weighed, and rejected options are in the folded SUPPLEMENT — not re-narrated here.

The operator's **execution-first bar still governs** — visible outcomes over governance. Most of plan-v3 §D executed on 2026-07-10 (§2); the **repo-derived work inventory** below is the remaining backlog — read it as inventory, **not** the priority order (the SUPPLEMENT sets priority):

- **#270 operator-load gauge — position 2** (`[P1]`, §S20; was the repo-derived headline — the 2026-07-10 JOURNAL M12 named it the *next architect-session headline* — **demoted to position 2 by the operator's filled SUPPLEMENT**). Still the gating FIRST element *within* any Tier-2 nightly-layer revival — it lands **before** #271 (nightly proposal loop, `depends-on #270`). The build-ready design + ex-ante success metric + pre-registered kill criterion are already specced (`docs/audits/2026-07-05-draft-tier2-nightly-layer.md`); this is a **build, not a re-decision**. _[recall — plan-v3 OD4 + 2026-07-10 JOURNAL 'Next']_
- **B-S2 corp-monorepo onboarding — now UNBLOCKED** (#299 G8 fix closed today). The **n=2** runbook gate after the ai-council n=1 pilot; a dedicated corp chat (ADR-41), plan-first. Runs the leg-b seeder as first real consumer; surfaces #262/#295 (corp is the *second* concrete failing codemap layout — **node-granularity, not tach-presence, is the blocker**, per #262's 2026-07-11 correction) + the runbook fixes #303/#304/#305 the corp gap-notes (G10/G12/G13) raised. _[recall — plan-v3 §D · #299 close]_
- **EPIC G QA-role decomposition** — waits on the operator's **functional QA intake session** (still pending; the functional boot is printed/ready). Then technical decomposition → ADR (role · protocol · report-gate) → build → **FLEET CARRIER** (every onboarded repo inherits it). Evidence set: incidents I1–I6 + OD2 proportional test-depth keyed to the T1–T5 scope-tags (#278 test-suite hygiene is the nearest live consumer; #144 feature-DoD E2E adjacent). _[recall — plan-v3 §A/§B]_
- **Hermetization — RULED, now BUILD** (ADR-101 Accepted today). d.iii is landed; the follow-ups are **#306** (`validate_hermetization.py` refusal-gate — HUB-ONLY, prospective-only, added-paths-filter) + **#307** (`gen_intake_index.py`); d.i/d.ii landings + closing **#300** remain. Filed, not built, per the 07-10 mandate (capture-precedes-construction). _[witnessed — BACKLOG #300/#306/#307 open; ADR-101 Accepted]_
- **EPIC H — subagent/model-routing doctrine** (OD3): research spike → PLAYBOOK doctrine (Opus = orchestration/judgment · Sonnet = bounded probes/mechanical · Haiku = cheap fan-out where the quality floor allows) → binds EPIC G's QA runs as the first consumer. The 2026-07-10 night run (Opus orchestrator + 6 Sonnet read-only subagents, all git mutations serial in the main thread) is another clean datapoint. _[recall — plan-v3 OD3]_
- **Operator-owed (not CC work):** P7 3-mode one-liner (formally closes EPIC C — #164 itself already closed) · the QA-functional session · close the 3 live worktree sessions + re-run the verdict-sheet Section C removes (`lane-a -d`; `lane-b`/`lane-n -D`, superseded). _[recall — 2026-07-10 JOURNAL 'Next']_
- **Corp session (ADR-41, separate chat — queue-only here):** CLAUDE.md §4 YAML one-liner · models/eval READMEs · the D4 ARCHITECTURE refresh · #262 corp codemap · #283 dup · #126 loop pilot. _[recall — 2026-07-10 JOURNAL 'Next']_

**Provenance (honest).** This architect self-handoff was cut from a fresh `/clear` CC session, so the repo-derived frontier above is **reconstructed** from the 2026-07-10 JOURNAL 'Next' lines + live `BACKLOG.md`, not witnessed deliberation (hence the `recall` tags). The operator has since **FILLED `SUPPLEMENT.md`** — the strategic "why" (intent · tensions weighed · rejected options · the reprioritization above) now travels in the folded SUPPLEMENT, so the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

**This bundle supersedes `docs/handoffs/2026-07-10-dev-knowledge-architect/`** (complete + immutable — its plan-v3 was executed 2026-07-10; boot THIS one, the 07-10 bundle stays as history). Slug dated **2026-07-11** (next working session) because the 07-10 slug is held by that consumed bundle — the same convention the 07-10 bundle used to avoid its 07-09 collision.
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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-11-architect`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-11-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-11-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-11-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

1. STRATEGIC INTENT — Universalization + hermetization of the methodology across the three
repos (dev-knowledge / ai-council / corp-monorepo) is priority ONE. Dev-knowledge is the
source of truth over what is methodology-specific vs project-specific. Next session's
way-of-working goal: produce the evidence-based BOUNDARY per surface (root files, CLAUDE.md
sections, hooks inventory, folders, protocols/, .code-workspace, caches, tests layout),
document it in the PLAYBOOK, and route it into mechanisms (carriers/gates/routines), not
prose. Framing correction on record: Wave-1 n=2 proved the ENFORCEMENT layer is in effect;
it never proved structural uniformity — that gap is this charter. "All onboarded = all OK"
is hereby rejected as a claim shape.

2. TENSIONS WEIGHED — (a) universal-vs-project boundary: land = every CLAUDE.md carries an
explicit methodology block (~identical fleet-wide, hub-owned) + a free project block.
(b) visible-outcomes bar vs meta-work: this audit is meta but operator-ruled P1; it
qualifies because trustworthy fleet rollout (P6 carriers) is blocked without the boundary.
(c) epic numbering: KEEP numbered IDs fleet-wide (EPIC n / S-n / #n) — referenceability
wins; settled, do not relitigate. (d) ARCHITECTURE ToC: operator leans REMOVE — but
toc-freshness is a deployed hub@v1.2.0 carrier component, so removal = a methodology
component deprecation decision, not a doc edit. (e) Mermaid: operator now leans REMOVE-ALL
(visualization method changing) — NOTE this reverses the 2026-07-11 menu-12 ruling
(M1/M2 KEEP-HAND-AUTHORED) and, with #262 BLOCKED, deletion without a successor leaves corp
mapless. Successor first, deletion second.

3. CONSIDERED + REJECTED (do not relitigate) — (a) deleting .methodology.yaml: REJECTED
WITH EVIDENCE — permanently answered 2026-07-11 (corp brief §3.2-A): hub Informant contract
file at the fixed root path (enforcement_coverage ALLOWLIST_REL + fleet_health); operator
ratified KEEP-ROOT + the CLAUDE.md §4 note. (b) "only hub has pre-commit hooks": CORRECTED
— all three repos have armed hooks (corp: 6 firing, QA-proven scorecard; ai-council: B-S1);
the real divergence is hook-SET inventories (empty commit-msg/pre-push stages = #302 +
parity item). Audit compares inventories, never presence. (c) retroactive renames: rejected
by ADR-101 (prospective-only + grandfather, Accepted). (d) redoing dependency mapping
(code-to-code/file-to-file): works, not a bottleneck, out of scope. (e) re-numbering
debate: settled per (2c).

4. OPEN QUESTIONS (the audit's charter) — (a) where exactly the methodology/project
boundary runs, per surface. (b) protocols/ as a methodology-mandated genre? (ai-council
has it, corp lacks it; operator wants per-package protocol docs in corp — "interface in
markdown", coupled to ARCHITECTURE). (c) ToC deprecation (carrier impact) + Mermaid
successor (vs the #262 codemap north star; corp G11 requirement input stands). (d) the
missing consolidation MECHANISM: a routine/generator that concatenates + diffs all
CLAUDE.md (methodology blocks) fleet-wide and surfaces drift continuously — the "3 months
and still invisible" gap; candidate new organ. (e) .claude/ full review across repos
(worktrees, workflows, skills — gotchas already universalized); commands documentation
coverage in each CLAUDE.md (/codex-review present; /code-review and other session commands
missing). (f) INSTALL.md in ai-council root vs absent in corp — why, and which is
methodology. (g) .code-workspace diffs; cache-folder policy (ai-council has ruff/pytest/
mypy caches, corp doesn't — programming-style drift evidence). (h) CI/CD report currency.
(i) tests/ layout chaos in corp (separate dedicated session — flag only). (j) web-research
leg: are there better current libraries/approaches for architecture + dependency
visualization (file-to-file, file-to-code, code-to-code) than our home-grown set —
sky-is-the-limit budget.

5. DECOMPOSITION RATIONALE — shape: ONE big multi-dimensional comparative audit session
(read-heavy → read-only parallel fan-out per repo is sanctioned; synthesis serial),
deliverable = a DIVERGENCE MATRIX with per-item disposition (methodology-generic vs
project-specific vs defect) + PLAYBOOK update; mechanism-building sessions follow, never
inside the audit. The audit must BUILD ON (not repeat): the 2026-07-11 corp root-hygiene
audit + the naming census (they are INPUTS — corp root is already inventoried to the file),
ADR-101 + audit-template (ratified), the QA n=2 scorecard (gates fire — do not re-prove),
gotchas universalization (done). The audit must NOT end with a verdict ("all OK" is a
banned claim shape) — it ends with the matrix + dispositions for operator ruling.

6. OFF-REPO CONTEXT — Operator trust statement on record: trust in the system is GATED on
visible universalization; treat as P1 posture until the boundary is documented and
mechanism-held. Queue after the audit: #270 (clock-triggered staleness — demoted from
headline to position 2 by operator priority), builds #306/#307, corp D4 refresh (GO
stands), CLAUDE.md trim RANK 1+2+3 (architect GO stands), #302 + commit-msg parity,
57 WEAK closure candidates grooming pass. Standing: codex-review now pinned gpt-5.6-sol
(A/B-proven, caught #311); P7 one-liner STILL OWED (closes EPIC C). Session plan file +
verdict sheet from 2026-07-10/11 are the audit's provenance trail.
