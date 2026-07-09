=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-10-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-10-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Execute **plan-v3** (fleet execution & methodology rollout — copied in as `PLAN.md`): **G8 runbook fix → B-S2 corp-monorepo onboarding** (n=2 runbook gate), the **QA-role intake decomposition** (EPIC G) after the operator's functional session, and the **`#300` hermetization ADR** (EPIC I) BEFORE Wave-2; EPIC H (subagent/model-routing doctrine) + `#270` re-admission (nightly layer) queue behind them. The operator's **execution-first bar governs** — visible outcomes over governance; new meta-work must unblock onboarding or be rejected. Start at `PLAN.md`, then `BACKLOG.md` (the spec).<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/night-handoff-0709`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since?"*.

> **`PLAN.md` present (manual instance of `#301`).** This bundle carries the operator's plan-v3 as
> **`PLAN.md`** — the session plan of record. It was copied in **by hand**: the `#301` architect-mode
> PLAN.md generator feature is filed (2026-07-09), not yet built, so the mode→artifact symmetry is
> delivered manually for this bundle. Read `PLAN.md` first (objective + epic sequence), then this boot.

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

# Residual — 2026-07-10-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
All drift-flags this window are **STANDING and dispositioned** in `ecosystem/disposition-register.yaml`; the night run introduced **none new** (the two filings + the audit report + this bundle were authored net-neutral — no new `doc_rot`, no new serialize-group). Standing classes, by reference: `no_ff_merges` — the grandfathered journal-wrap / transcript-archive direct-to-main commits (`#210` is the standing-rule proposal); `doc_rot` backlog-accretion — `#262` + `#278` (dispositioned); `undeclared_edges` — the six handoff-process prose edges (`#241`); `handoff_probes` P1a/P1b/P8 — the grep/sed/ls tool-absent SKIPs (environmental, not drift). Run **P4/P6/P7** for the live verdict / count / `[stale]` — this file names none by design. _[witnessed — `audit.py health` re-run live this generation, OK]_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = the **2026-07-09 night hygiene run** (this generation). The map (detail in `JOURNAL.md`):
- **`#301`** filed — session-plan artifact class (architect bundles gain a bundle-resident `PLAN.md`; the mode→artifact symmetry). → `BACKLOG.md` [S2], arc `5fdd074`.
- **`#302`** filed — branch-protection parity: answers the ai-council lived-QA **F1** (hub has NO commit-time branch-guard, only push-time `block-ff-push` HUB-ONLY; consumers lack even that). → `BACKLOG.md` [S8], arc `5fdd074`.
- **Night hygiene audit** — 6-corpus read-only Sonnet fan-out (intake / decisions / audits / handoffs / BACKLOG-coherence / ai-council). Headline: exactly one cold committed bundle leaks (`2026-07-05-dev-knowledge-architect`, 8 fill-markers); corpus referentially clean but no age-based backstop. → `docs/audits/2026-07-09-night-hygiene-audit.md`, arc `558a131`.
- **Prior same-day context** (5 earlier 2026-07-09 sessions — night-verification · morning-ops · session-close · `#164` finish · GATE-0): see the five `JOURNAL.md` 2026-07-09 entries (`#164` CLOSED, `#255` retired, `#291` backup fix).

State pointer: `BACKLOG.md` (82 tasks after the two night filings). _[witnessed — this run]_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The operator's execution-first bar still governs** — *visible outcomes over governance*; any new meta/governance work must unblock onboarding or be rejected. **The plan-v3-specific operator intent is NOT yet in this bundle** — `SUPPLEMENT.md` ANSWERS is generated EMPTY, so the §13d beat fires FULL; fill it at session start. The un-committed "why," in plan-v3 sequence (full plan in `PLAN.md`):

- **G8 runbook fix FIRST (small, serial) — it gates B-S2** (`#299`): the onboarding runbook Layer-6 verify must invoke the SessionStart hook's command line VERBATIM (`python -m pre_commit install`), not a proxy `import pre_commit` that passed on a different interpreter than the hook uses. corp-monorepo shares the latent fragility (`pre_commit` in `.venv`, undeclared in pyproject → a fresh re-clone won't repopulate it). _[recall — plan-v3 §D · `#299`]_
- **B-S2 corp-monorepo onboarding** (dedicated chat, plan-first) — the **n=2** runbook gate after the ai-council n=1 pilot; runs the leg-b seeder as its first real consumer; surfaces D4 + `#262` tool-MANAGED codemap n≥1 (corp-monorepo is tach-bearing, so it can close the generator-managed owe ai-council's flat layout couldn't, `#295`). _[recall — plan-v3 §D]_
- **QA-role intake decomposition (EPIC G)** — after the operator's functional QA session: technical decomposition → ADR (role · protocol · report-gate) → build → **FLEET CARRIER** (every onboarded repo inherits it). Evidence set: incidents **I1–I6** (plan-v3 §A) + OD2 proportional test-depth keyed to the T1–T5 scope-tags. Admission: **`#270` re-enters** — it now unblocks the operator-demanded night capability (OD4). _[recall — plan-v3 §A/§B]_
- **`#300` hermetization ADR (EPIC I) — BEFORE Wave-2**: d.i `docs/runbooks/` location · d.ii mode-boot bundle home (incl. the committed-ephemeral `docs/handoffs/2026-07-07-dev-knowledge-functional/` fate — one migration pass, no drive-by delete) · d.iii audit-class grammar. **Tonight's audit made d.iii decidable**: 41 already-compliant + 31 trivially-compliant vs ~130 subject-before-class + 4 class-less → the honest ruling is **prospective-only + grandfather + a canonical CLASS enum** (not a retroactive rename of ~65% of the corpus, which the index already disambiguates by date). See audit §S3. _[witnessed — this run's finding]_
- **EPIC H — subagent/model-routing doctrine** (OD3): research spike → PLAYBOOK doctrine (Opus = orchestration/judgment · Sonnet = bounded probes/mechanical · Haiku = cheap fan-out where the quality floor allows) → binds EPIC G's QA runs as the first consumer. **This night run is itself an evidence datapoint** — an Opus orchestrator + 6 Sonnet read-only subagents ran cleanly with all git mutations serial in the main thread. _[recall — plan-v3 OD3/§B]_
- **Night-layer `#270` → `#271`** re-admission — the operator-load gauge is the gating FIRST element; night EXECUTES pre-authorized deterministic contracts only and PROPOSES the rest (this run IS the pattern; D8 go/no-go rests on `#270` + intake-8 triage). _[recall — plan-v3 OD4/§C-D8]_
- **Carried CC-observed residuals (reconcile, do NOT drive-by):** (a) the `docs/decisions/README.md` ADR-51 one-liner still speaks tier language, superseded by the 2026-05-23 amendment (audit §S2-2, **verify-then-fix**); (b) the cold `2026-07-05-dev-knowledge-architect` bundle's 8 fill-markers (audit §S4-1 — **backfill or accept-and-annotate**, not a night-fix: immutable + I cannot fabricate that session's retrospective); (c) BACKLOG `#292`'s evidence text is now stale (fixed 07-09 bundle, misses the 07-05 one — audit §S4-2); (d) the hub BACKLOG footer's ai-council-residuals pointer appears already resolved in-repo (audit §S6). _[witnessed — this run's findings]_

**This bundle supersedes `docs/handoffs/2026-07-09-dev-knowledge-architect/`** (complete + immutable, but predates plan-v3 + tonight's findings) — boot THIS one; the 07-09 bundle stays as history. Slug is dated **2026-07-10** (next working session) because the 07-09 slug is held by that complete bundle; the collision + choice are recorded in the night audit + morning briefing.
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
> **Branch note.** This bundle was generated on branch `docs/night-handoff-0709`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.
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
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what .dev-knowledge is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-10-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-10-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-10-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

A1 (strategic intent): EXECUTE plan-v3 §D — theme: "teeth for the edges".
Convert 07-09's incident set (I1–I6) into mechanism: G8 runbook fix first
(gates B-S2), corp-monorepo onboarded as runbook n=2 + seeder first consumer,
#300 hermetization ADR drafted (P1, before Wave-2), EPIC G decomposition the
moment the operator's QA-functional intake lands. Visible-results bar stands.

A2 (tensions weighed): night autonomy vs proposals-only → proposals-only,
validated n=1 (zero unwanted mutations, full queue honored). d.iii retroactive
vs prospective → prospective + grandfather + canonical CLASS enum (S3
quantified: retro = ~65% corpus rename for near-zero gain). PLAN.md generator
vs manual → manual n=1 done (this bundle), generator build = #301. Subagent
parallelism → read-only fan-out only; git mutations serial (index-race,
ratified from lived-QA + night run).

A3 (considered + rejected — do NOT relitigate): retroactive audit renames;
parallel subagent commits on one tree; fabricating SUPPLEMENT/retrospectives
for past sessions (07-05 cold bundle → accept-and-annotate, not backfill);
mandatory-TDD (council-rejected, stands); night merges beyond the 4 committed
classes; docs/plans/ top-level (plans are bundle-resident, #301).

A4 (open questions): #300 d.ii mode-boot bundle home + fate of the 07-07
committed functional bundle + 27 superseded-era bundles (S4-3, one migration
pass); d.iii CLASS enum contents (ruling shape decided, list to draft in the
ADR); age-based backstop design — the night audit's single structural theme
(intake-age → #270/#271, cold-bundle → #292 gate, Pattern-C
amendment-summary drift has NO organ yet, unfiled); EPIC H doctrine (run
changelog V1 worktree-contamination verify as its first input); #254(b)
fleet-audit auto-push vs manual cadence; P7 (operator, one line, closes
EPIC C); QA-functional session output pending.

A5 (decomposition rationale): §D order is dependency-true: G8 fix gates
B-S2 (n=2 must run the corrected layer-6 verify); B-S2 gates v4-template
archival (corp must be off v4) and provides #262 tool-managed n≥1; #300
before Wave-2 (artifact classes multiply per repo onboarded); QA
decomposition ∥ B-S2 is collision-free (hub/browser vs corp-monorepo chat).
Session-start batch (small, serial): ADR-51 README one-liner (verify-then-
fix) · 2 stale intake Status: lines · #181 citation convention ·
docs/handoffs README documents PLAN.md as bundle member · demo-prep backup
verdict if terminal check showed unpushed work. Do NOT redo: the grooming,
#300 scope text (filed verbatim), the d.iii ruling, the night autonomy
contract, C-S3v2 results, lived-QA findings (F1 already filed as #302).

A6 (off-repo context): operator verdicts on record this cycle: QA must be
a PROCESS-level role (playbook + onboarding legs, fleet carrier); test
depth proportional to T1–T5 scope tags; subagent routing doctrine wanted
(EPIC H); night runs wanted — gated by #270, which RE-ENTERS admission;
plans are part of every session (#301, operator-ratified pattern); folder/
naming discipline is a hard trigger for the operator — treat R13 and #300
as P1 posture, not paperwork. WMI machine incident root-caused and fixed
(elevated winmgmt restart; G9 latent, dormant). Operator still owes: P7
one-liner + the QA-functional session (boot is printed and ready). Budget:
sky-is-the-limit stands; Opus+high effort default for judgment work.


---

=== PLAN.md (session plan of record -- appended into PASTE_THIS for the file-less browser; manual #301 instance) ===

<!-- scope: meta -->
> **PLAN.md — operator plan of record (plan-v3), copied into this bundle BY HAND.**
> Manual instance of the `#301` session-plan-artifact pattern (mode->artifact symmetry): the
> architect-mode PLAN.md generator feature is filed (2026-07-09 night run) but NOT yet built, so
> plan-v3 was copied in verbatim below. Source: the operator's
> `2026-07-09-program-plan-fleet-execution-v3.md` (supersedes plan v2). On close, the `#301` pattern
> calls for a RETROSPECTIVE fill here (done / not-done / incidents / carry-forward) — deferred to the
> generator build; for now the plan is read-only.

---

# PROGRAM PLAN v3 — Fleet Execution & Methodology Rollout
**Status:** SESSION RETROSPECTIVE + FORWARD PLAN · **Supersedes:** v2
**Session reviewed:** 2026-07-09-dev-knowledge-architect (executed 07-08/09 wall-clock)
**New drivers:** session incidents I1–I6 · operator directives OD1–OD4 (QA-in-process, proportional test depth, subagent utilization, night schedule)

## CHANGELOG v2 → v3
| Δ | Change |
|---|---|
| RETRO | §A added: full done/not-done/incident accounting for the executed session |
| OD1 | QA role arc formalized: EPIC G (intake → ADR → build → fleet carrier). Evidence register I1–I6 attached |
| OD2 | Proportional test-depth requirement keyed to existing T1–T5 scope-tags — routed into EPIC G intake as structural requirement |
| OD3 | Subagent/model-routing doctrine gap acknowledged (opusplan exists; deliberate Opus→Sonnet→Haiku orchestration is uncodified) → EPIC H (research + PLAYBOOK doctrine + carrier) |
| OD4 | Night schedule: routed to existing intake-id 8 (night-routines suite) — GATED by #270, which therefore RE-ENTERS admission (it now unblocks an operator-demanded capability) |
| NEW | EPIC I: docs-taxonomy hermetization (filed this session) — BEFORE Wave-2 |
| D-reg | D1 demoted to INTERIM (operator questioned twice) — final ruling in hermetization ADR d(i). D8 added (night-layer go/no-go rests on #270 + intake-8 triage) |

---

## §A — SESSION RETROSPECTIVE (vs v2 §4 plan)

### Done (planned)
| Item | Evidence |
|---|---|
| GATE-0 P2–P10 | all PASS; P10 bonus: mode-split already shipped → C rescoped finish-only |
| A-S1 #286 | 5dd2907 · [S1]–[S20] visible · validator grammar + tests · hub-only scope call RATIFIED |
| A-S2 #292 | filed, kill-candidate #117 · backpressure hook FIRST LIVE FIRING: correct |
| A-S3 runbook F5 | 6cf51a6 · markings [hub-runnable]/[consumer-only] + --run-date note |
| B-S1 ai-council pilot | 1bdc2ea · contract 10/10 · fire_test FIRED · gap-notes G1–G9 · fix-arc fba7b13 (SessionStart) — Wave-1 n=1 COMPLETE |
| C (#164) | closed 9e6ceb6 · legs {b-hub,e,g} built, rest evidenced · Done-when amended on record (fan-out → Wave arcs) · C-S3v2 matrix 7/8 · polish filed #298 |
| Consolidation | #294–#297 filed from gap-notes · census docs/handoffs amendment recorded · QA premise-grep (no QA role exists; TDD council-rejected; ADR-81 test-first contract is the nearest construct) |

### Done (unplanned, absorbed)
QA-bundle slug incident remediation (ephemeral pattern) · WMI machine fix (elevated, verified on real path) · git mid-merge incident recovery (in flight) · G8/G9 · temp-repo rule → machine memory.

### NOT done (carried forward)
| Item | Why | Carries to |
|---|---|---|
| F-S1 SEED-6 boundary triage | eaten by incidents | next architect session buffer |
| Step-6 educate/close + handoff | pending recovery + lived-QA returns + P7 | session close |
| P7 operator content verdict (3 modes) | operator's one-liner outstanding | closes EPIC C formally |

### Incident register (I*) — QA-intake EVIDENCE SET
| I | Incident | Lesson class |
|---|---|---|
| I1 | C-S3v1 shallow test (no matrix, no quality rubric) — caught by operator, not mechanism | test-depth unenforced |
| I2 | G8: runbook verify used shim interpreter, hook runtime uses .venv | verify ≠ runtime path |
| I3 | G9: WMI hang — import works, CLI hangs; machine-scoped | env-layer testing gap |
| I4 | dateless slug sailed through every gate (architect-authored) | convention without teeth |
| I5 | F-A: session reported "merged, GREEN" over an uncommitted MERGE_HEAD | premature closure / claim-vs-disk |
| I6 | F-B: maintenance commit in live checkout finalized foreign merge | session isolation unenforced |

---

## §B — PROGRAM STATE (epics)

| Epic | State |
|---|---|
| A visibility | ✅ CLOSED |
| B Wave-1 | B-S1 ✅ · B-S2 corp-monorepo NEXT SESSION (precondition: G8 runbook fix — layer-6 verify must invoke the hook's own command line) |
| C generator | ✅ technically closed · P7 operator verdict pending · #298 polish pegged |
| D e2e test | D-S1 evidence live (pilot + lived-QA exercise in flight) · D-S2 dedicated pass session +2 — MERGES INTO EPIC G protocol once QA role lands (no duplicate test doctrine) |
| E Wave-2 | unchanged; BLOCKED-BY EPIC I (hermetization) by design |
| F architect buffer | carried |
| **G — QA role (NEW)** | intake session = operator's next move (boot printed, evidence I1–I6 + requirements OD2 ready) → technical decomposition → ADR (role, protocol, report-gate) → build → FLEET CARRIER (PLAYBOOK + runbook legs, so every onboarded repo inherits it) |
| **H — subagent/model-routing doctrine (NEW)** | research spike (Task-subagent capabilities/costs/parallelism) → PLAYBOOK doctrine: default routing Opus=orchestration/judgment · Sonnet=bounded probes/mechanical · Haiku=cheap fan-out where quality floor allows → binds EPIC G's protocol (QA runs are the first consumer) |
| **I — docs hermetization (NEW, filed)** | ADR arc: sanctioned top-level set · per-class name grammar `<date>-<class>-<slug>` (audit classes: technical/functional/qa/census/verification) · pre-commit refusal gate · sub-rulings: d(i) runbooks location · d(ii) mode-boot bundle home · d(iii) audit classes. PEG: BEFORE Wave-2 |

## §C — Decisions register (delta)
| ID | Decision | State |
|---|---|---|
| D1 | docs/runbooks location | DEMOTED to interim-keep → final in hermetization ADR d(i) |
| D6 | life-architect privacy gate | STANDING (unchanged, hard) |
| D7 | terminal-setup in Wave-2 | standing recommendation: include |
| **D8** | night-layer go/no-go: after #270 lands + intake-8 triage; unattended = proposal classes only, NEVER autonomous merges | operator rules at that gate |
| P7 | 3-mode content verdict | OPERATOR — one line, closes EPIC C |

## §D — NEXT SESSION PLAN (architect, fresh chat via generated architect bundle)
| Step | What | Notes |
|---|---|---|
| 0 | Boot from /handoff architect bundle (dogfood) + probes | |
| 1 | G8 runbook fix (small, serial) | gates B-S2 |
| 2 | B-S2 corp-monorepo onboarding (dedicated chat, plan-first) | n=2 runbook gate · D4 surface · #262 tool-managed n≥1 target · runs the SEEDER (leg-b fan-out first consumer) |
| 3 | ∥ hub: QA intake decomposition (after operator's functional session) → ADR draft + EPIC G stories | admission: #270 re-enters (unblocks OD4) |
| 4 | ∥ hub: hermetization ADR (EPIC I) if capacity | else session +2, still before Wave-2 |
| 5 | F-S1 SEED-6 boundary (carried) | buffer |

## §E — Session close conditions (this session)
Recovery report GREEN + pushed · lived-QA exercise report reviewed · P7 received · educate artifact delivered · architect close-out handoff generated (dogfood) — then this chat wraps per context self-eval (a).
