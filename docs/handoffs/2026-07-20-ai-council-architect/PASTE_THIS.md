=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-20-ai-council-architect` |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-20-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Target repo** | **`ai-council`** — CROSS-REPO handoff (ADR-36/41). The bundle lives in the `.dev-knowledge` hub; the **subject** is the sibling repo `ai-council`, and every probe below binds to **its** files, resolved from **its** root. The hub is read-only w.r.t. the target. |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**CROSS-REPO — the target is `ai-council`, not the hub.** Settle the delegation-surface contract questions that the 2026-07-19/20 reintegration-and-adversarial arc surfaced but deliberately left open: the `options_considered` extraction **contract** ([#77] — decide the boundary, not the regexes), the **Contract-Version 1.1** bundle ([#34] + [#76], versioned together), and the inbox/CLI **parity** pattern now on its fourth recorded instance ([#69]). Also rule on the one genuinely cross-repo question: whether `ai-council`'s thin, silent-passing enforcement surface is correct-by-design or a gap, given that this window's central lesson was that per-lane green does not compose to whole-repo green. Navigate from `ai-council/BACKLOG.md` (theme backbone [E1]–[E7]; [E1] delegation-readiness carries most of the above — P9 re-derives the live counts) — **and note `RESIDUAL.md` §4 is the payload here, not §2.**<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/ai-council-architect-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

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

# Residual — 2026-07-20-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> ## ⚠ CROSS-REPO BUNDLE (ADR-36/41)
>
> **The subject of this handoff is `ai-council`. The bundle lives in the `.dev-knowledge` hub.**
> Every `#id`, file path, ADR number, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The two repos have same-named files with different contents — `BACKLOG.md`,
> `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and even `scripts/validate_backlog.py`
> exist in both. Reading the wrong one is the primary failure mode of a cross-repo bundle; `PROBES.md`
> names a **run-in root** per probe for exactly this reason.
>
> **The hub is read-only w.r.t. the target** — this session plans `ai-council` work; it does not edit
> the hub's governance corpus. The stock generator probes were hub-bound and have been **re-authored
> against verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which four
> and why).

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS the headline).** `ai-council` has **no counterpart to
the hub's drift-flag machinery** — no `audit.py ship-gate`, no `ecosystem/disposition-register.yaml`,
no `validate_doc_claims`, no `validate_git_backlog`. There is therefore **no dispositioned-WARN set to
inherit and no standing-vs-new distinction to make** in the hub's sense. The target's drift surface is
four independent read-only validators plus judgment over `BACKLOG.md` ∩ git — which is exactly why
`PROBES.md` P2/P4/P6/P7 were re-bound rather than run as generated. **Treat the absence of a
consolidated verdict as the flag**, not as a green light: several of those gates pass *silently*, so
"no output" is not "no drift" (P7 reads exit codes explicitly for this reason).

**Standing, by reference — carried deliberately, not oversights:**

- **`options_considered` is corrupted on `main` right now** — the single most consequential standing
  flag, and it sits on the **delegation surface** (the verdict package a consuming repo reads). Filed
  as **[#77]**, recorded explicitly in the 2026-07-20 JOURNAL entry. Deliberately filed as **one
  contract-scoped ticket rather than a patch queue**: this is the *second* window in which the
  function is known-broken and half-fixed (the night audit found it broken both ways; **[#60]** fixed
  one half), and a third round of partial patches is the pattern that filing exists to stop.
- **Manifest-vs-reality gap** — **[#76]**: the verdict package's `artifacts[]` can name a return-dir
  copy that the subsequent write failed to produce. `scripts/verify_output_writes.py` already reports
  this as a standing **GAP**; that visibility is the *interim mitigation, explicitly not a fix*.
- **Asymmetric routing failure** — **[#75]**: `secondary_dir` raises where ADR-43 `target_paths`
  swallows, so a `secondary_dir` failure can abort before canonical artifacts land — the same
  canonical-loss class **[#35]/[#62]** closed for `--return-dir`.
- **[#66] stays OPEN, gated on [#27]** (CLI-backend scoring); no billed witness has been authorized.
  This is cost-gated, awaiting an operator call — not a stalled task.

**New this window:** the six sol-pass filings (**[#75] [#76] [#77] [#78] [#79]**, plus **[#69]** from
the terra pass) were classified **REGRESSION vs PRE-EXISTING by differential run** against `27a45d1`
in a temporary detached worktree — not by reading the diff. All six reproduce byte-identically on both
trees, so **none were introduced by this window's merges**; they are pre-existing defects newly made
visible. The two genuine regressions (F8 marker substring-match, F2 sidecar-before-raise) were
**repaired on `main` immediately** per the operator's repair-regressions-now rule and proven by
individual reversion.

**Do not trust the above as current state** — P4/P7/P9/P10 re-derive all of it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (entries **2026-07-19** reintegration and **2026-07-20** sol
disposition) already encodes the detail; do not re-read it as narrative here.

- **Three-lane serial reintegration** (A2 → A1 → C, operator-gated at every merge). Order was
  load-bearing, not convenience: A1 adds raises in the writer layer while the interactive-debate
  boundary had **no handler at all**, so A2 had to close that window first. → JOURNAL 2026-07-19.
- **The cross-lane seam defect** — the finding that session existed for: A1 green + A2 green + merged
  `main` **RED**. `OutputRoutingError`'s constructor took a `list[RoutingFailure]` with no type guard;
  `str` is iterable, so a message was shredded into one "deliverable" per character. Repaired
  fix-forward with an explicit type guard. **Two per-lane checkers were structurally blind to it** —
  each half sound, the composition broken. → JOURNAL 2026-07-19.
- **End-to-end witness mechanized** — `scripts/verify_output_contract_e2e.py`: **4/4** paths vs a
  **1/4** negative control on original `main` (three paths previously exited 0, silently). Driven by a
  real filesystem failure with providers mocked. The blind spot is now a re-runnable checker, not a
  fixed bug. → JOURNAL 2026-07-19.
- **Sol adversarial disposition** — 2 regressions repaired, 6 filed. → JOURNAL 2026-07-20, audit
  `docs/audits/2026-07-19-codex-a1-failloud-adversarial.md`.
- **Closures / strikes:** **[#67] [#68]** closed via `/review-closures` (ADR-70 Tier-1, WEAK tier, each
  named individually, citing the lane's own merge — *not* the gate's stale pre-merge evidence);
  **[#35] [#62] [#63] [#60] [#65] [#71]** struck; **[#74]** filed and closed in-arc.
- **Synthesizer Branch A (openai) shipped** 2026-07-18 as the durable config default (operator ruling,
  `docs/audits/2026-07-17-synthesizer-ruling-gemini-to-openai.md`). **Remaining scope is the ADR-01
  amendment text only** — see **[#2] [#3]**; the code decision is done.
- **New enforcement surface:** `validate_sealed_keys` **[#67]** and `validate_docs_registry` **[#68]**
  joined the pre-commit set (the latter **fails CLOSED** as `GUARD MALFUNCTION`).
- **Housekeeping closed out:** scratch dirs cleaned, both empty provisioner stub branches deleted,
  all three worktrees removed/pruned/verified absent; `main` pushed. One held-back scratch dir
  (`qfm_mhrt`) awaits an operator ruling.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The design questions this window **surfaced but deliberately did not settle**. Resume these; do not
rediscover them. Ordered by how much they constrain everything downstream.

**(1) `options_considered` — settle it as a CONTRACT, not a third patch. [#77]**
The live decision, not a bug-fix task. The function has now been known-broken across two windows and
half-fixed once; the filing was deliberately scoped to **one** ticket to force an *ex-ante* contract
with **tests written before the fix** (bullet grammar `-`/`*`/`+`/`1.`/`1)`; exact-marker removal that
never eats a payload character — `3D`, `2026` must survive; emphasis unwrapped as real markdown
delimiters, not edge-stripped; a named test per rule). **The open architectural question is the
boundary**, not the regexes: should option extraction remain *heuristic parsing of synthesizer prose
at the output layer at all*, or should the synthesizer be asked to emit structured options directly so
there is nothing to parse? Every patch so far has assumed the former without ever deciding it. **The
F8 precedent is the relevant prior:** the operator rejected scan-narrowing in favour of removing the
defective marker, accepting a real cost (`Approaches Considered` now falls through to the question
fallback) — **under-match toward the loud failure**. `[]` is honestly empty; `['Risk one']` is
plausibly wrong and consumed silently. That principle should govern the contract.

**(2) Contract-Version 1.1 — decide the bundle and cut it. [#34] + [#76]**
Both are flagged 1.1 candidates and both change the delegation surface, so they must be **versioned
together**, not shipped piecemeal. **[#34]** = research-path verdict-package parity (the research lane
emits no `council-verdict-*.json` at all, so a Lane A research commission gets no transcript-free
deliverable — debate-path-only was an explicit architect ruling on 2026-07-17, not an oversight).
**[#76]** = two-pass write, so the manifest is serialized only after the writes it describes have
landed. Open: **is that the whole of 1.1, or does the [#77] contract belong in the same version bump?**
Argument for folding it in: all three are the same delegation-surface-honesty theme, and consumers
should absorb one break, not two.

**(3) The inbox/CLI parity blind spot — structural fix or stop calling it a blind spot. [#69]**
`LESSONS.md` records this pattern **three separate times** (`--full`, `--mode`, target-project
routing), each with the same rule: *"investigate whether the two paths can share a common processor
function; if not addressable structurally, add a parity-check test."* **[#69] is the next instance** —
frontmatter `models:` is dead in the default path *and* the two entry points guard it on **different
conditions**, so the same brief file yields a different panel via `--file` than via `--inbox`. The
recurrence count now argues the structural change was warranted several instances ago and was never
made. **Decide it: shared processor helper, or an enforced parity test as the permanent answer.**
Patching [#69] in isolation makes it instance four of five.

**(4) Enforcement asymmetry with the hub — deliberate thinness, or a gap to close?**
The genuinely cross-repo question, and the one the architect is uniquely positioned to rule on.
`ai-council` has four independent read-only validators and **no consolidated gate**; the hub has
`audit.py` with a registry, a ship-gate verdict, and a disposition register. Two honest readings:
(a) correct — `ai-council` is a *code* repo and the hub is a *governance* repo, so their enforcement
shapes should differ; or (b) a gap — several `ai-council` gates pass **silently**, so there is no
single place to read "is this repo healthy," which is precisely the composition-blindness that let the
seam defect through (two sound checkers, broken composition). **Note the recurring evidence for (b):**
this window's central lesson was that per-lane green does not compose to whole-repo green. Do not
close this by defaulting to hub parity — rule on it.

**(5) Verification-as-code — established doctrine; decide its remaining scope.**
`LESSONS.md` now carries the rule explicitly (*"a report without a re-runnable checker is a claim, not
a witness"*), and this window shipped three checkers plus a negative control. The doctrine is settled.
What is open is **coverage**: which remaining prose claims in `docs/audits/` and `ARCHITECTURE.md`
still assert something no script re-proves. That is a bounded sweep, and it is the natural next
application of the doctrine rather than a new decision.

**(6) Awaiting an operator ruling — not stalled work, but blocking if left.**
**[#66]** gated on **[#27]** (CLI-backend scoring; no billed witness authorized — a cost decision).
The held-back `qfm_mhrt` scratch dir (a 2026-07-18 CLI-seat witness run, unreferenced anywhere in the
repo). The `codex-review.ps1` severity-summary regex fix — **operator-owned, report-only, and
deliberately not edited**; measured across 68 audits in four repos, 8 reports printed `High=0` while
their bodies carried 26 High findings. **No committed audit is wrong** (the counts were never written
to any file); the damage was transient console output that could have been read as "clean" at review
time. Route the hub-owned `/review-closures` staleness class upward to the hub, not fixed here.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the backlog, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per ADR-66. Every `#id` in this residual is an **ai-council** id. `[E1]` (invocation surface
  & delegation-readiness) carries the delegation-surface work §4 is about.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** here — this is a cross-repo handoff
  and the hub is **read-only-adjacent**: it hosts the bundle, it is not the subject. The one item
  routed *toward* it is the `/review-closures` staleness class (§4 item 6), which is filed upward, not
  fixed in `ai-council`.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist there. P4 substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection,
  and **P10 is the judgment layer over it** (groom every open `#id` as live / dead / awaiting-ruling).
  This grooming is the operator-ruled boot obligation, not optional.

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
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts, exit
> codes, or orienting lines are stated. That withholding IS the teeth. The pass criterion is
> **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints live in the JOURNAL generation-entry, which the browser never sees — never here.

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P10** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | `ai-council` |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (anchors
confirmed at generation time by running each command in the target). Where the hub has an organ
`ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what ai-council is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits in the `Dev/` ecosystem*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+3p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run-in root noted) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS`, and no `validate_doc_claims` either; this row restores that missing doc-vs-reality tooth by hand.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and does `ARCHITECTURE.md`'s **Pre-commit roster** prose list that **same set** — or has the doc drifted behind the config? | `ARCHITECTURE.md` (Pre-commit roster prose) ∩ the pre-commit config | the roster drifts every time a gate lands, and `ai-council` has **no automated doc-claim check** to catch the doc falling behind — so this mismatch is invisible until someone reads both; neither the count nor the tail id nor the verdict is in this bundle | **TARGET:** `grep -n 'Pre-commit' ARCHITECTURE.md` for the doc side; for the config side run grep -c and grep-tail for the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the two sets by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **read-only** repo validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Note several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | **[RE-BOUND — the stock row bound to the hub bundle dir, which is unresolvable from the target root.]** How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; the count, the tail slug, and whether the index has kept pace are all live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | **[RE-BOUND — `ai-council`'s `validate_backlog` prints NO serialize-groups line; its summary is counts-only.]** What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit and are absent from this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** `.pre-commit-config.yaml`
> is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked `.pre-commit-config.yaml` is looked up as `pre-commit-config.yaml`, which
> resolves nowhere — the probe is then FAILed as a missing target even though the file plainly exists.
> Verified at generation time: `_resolve_path(root, '.pre-commit-config.yaml')` resolves; the tokenized
> `'pre-commit-config.yaml'` returns `None`. **Consequence: no probe in any bundle — hub or cross-repo —
> can currently bind to a dotfile.** That is a hub tooling defect worth filing (dotfiles are exactly
> where config gates live); it is deliberately **not** patched from inside this handoff, because hub
> infra changes are exception-with-ruling (core-invariant #6). The probe's teeth are unaffected — the
> comparison is still live-only and answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `scripts/validate_backlog.py` all exist in
   both). This is the single most likely failure mode of a cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d).** Then run P2–P10, each against
   **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P10 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." **P7 is the headline substitute** (four exit codes, read
   explicitly — several gates pass silently, so "no output" must not be scored as "no drift").
   **P2 is the hand-built doc-vs-reality tooth** this repo otherwise lacks. **P10 grooms the whole
   open BACKLOG at boot** (live / dead / awaiting-ruling per open `#id`) — the operator-ruled boot
   obligation, not optional. First check which branch is live (P3), then re-derive every
   load-bearing fact from the live primary source.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock P8 was re-bound — it
   pointed at the hub bundle dir, which is unresolvable from the target root). This bundle carries
   `HANDOFF_BOOT` + `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the §13(d) beat fires **FULL**
   unless the operator runs `supplement filled` first. Confirm by looking at the bundle directory in
   the hub — it is CC-side bookkeeping, not target state.
