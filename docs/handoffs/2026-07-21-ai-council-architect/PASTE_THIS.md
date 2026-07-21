=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-21-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-21-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Rule the boost layer's OWNER, then BUILD — this is an execution window, not another planning one.** The supplement is explicit and it outranks CC's repo-derived reading: the moratorium was **lifted mid-window**, and **H1 is already resolved** — the Council is a decision engine whose *input stage* is question-boosting, a **sequence, not a fork**. So the one genuinely open design question is the boost layer's **owner**: **(A)** caller-side advisor (`#36`, Council stays a stateless CLI per ADR-11) vs **(C)** council-side entry stage (the caller needs to know nothing, but this **reopens ADR-11**). Rule A-vs-C, amend `VISION.md` + ADR-11 to state the boost→decide chain, **then build** — in the supplement's order: boost layer → the claim-vs-reality checker → `#4`'s ADR-02 amendment → `#81` + the remaining P1 waves + the backlog renumber. **The operator's standing demand: the theory is done; "produced another document" is a failure signal for this window.** Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; read `docs/audits/2026-07-21-night-audit-combined-review.md` first — it is the vision material, and its findings are this session's *input*, not something to re-derive.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `worktree-ai-council-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-21-ai-council-architect — the part the repo does not already encode

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
> against verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which and why).
> Note the ADR numbers in this residual are **hub** ADRs when cited as governance (ADR-36/41/65/66/70),
> and **ai-council** ADRs when cited as product decisions (ADR-01/03/05/11/12/43/95) — the residual
> marks which each time.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks. **Re-derive each at read-time — the teeth are in
`PROBES.md` (P2/P4/P7/P9/P11), not in trusting these lines.** This bundle states **no** verdict,
WARN count, `[stale]` status, drifted `#id`, sha, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS part of the headline).** `ai-council` has **no
counterpart to the hub's drift-flag machinery** — no `audit.py ship-gate`, no
`ecosystem/disposition-register.yaml`, no `validate_doc_claims`, no `validate_git_backlog`. There is
therefore **no dispositioned-WARN set to inherit and no standing-vs-new distinction** in the hub's
sense. The target's drift surface is four independent read-only validators plus judgment over
`BACKLOG.md` ∩ git — which is why `PROBES.md` P2/P4/P6/P7 were re-bound rather than run as generated.
**Treat the absence of a consolidated verdict as the flag**, not as a green light: several of those
gates pass *silently*, so "no output" is not "no drift" (P7 reads exit codes explicitly for this reason).

**THE HEADLINE — the record and the ticket-space are out of sync, and the gap is still open.**

> **⚠ CORRECTED BY THE SUPPLEMENT (which outranks this repo-derived reading).** CC wrote this section
> from the committed record, where a filing moratorium appears to hold across the whole window. The
> supplement records that the operator **LIFTED the moratorium mid-window**, and that the P1 fixes then
> went in **fix-on-main with no ticket churn**. **The consequence below is unchanged and is what
> matters:** the lift removed the *block*, not the *backlog* — nothing was absorbed, so the sync gap is
> still open and is now *inherited work* rather than a *policy state*. Read "moratorium" below as "the
> period during which nothing was filed," not as a live constraint to rule on.

A filing moratorium held for most of this window: four night audits ran, a combined review synthesized
them, and two fix lanes landed real code — and **nothing was filed and nothing was struck** except the
two verified-done items. The consequence is a drift class the hub's machinery has no equivalent for:

- **Fixed-but-never-ticketed.** The six defects repaired this window (the night code audit's own
  `P1-*` finding ids, not `#id`s) were confirmed by that audit as **not already tracked**, so no
  `[#id]` applied and none was created. They are now fixed on `main` and recorded **only** in
  `JOURNAL.md` + git — neither "open" nor "closed" anywhere in `BACKLOG.md`. A backlog-∩-git drift
  check would see nothing, because the tickets never existed.
- **Found-but-never-filed.** The remainder of that audit's new `P1` set is still **unfiled** — it
  lives only in `docs/audits/2026-07-20-night-code-audit-opus.md`. The combined review names this the
  strongest argument for lifting the moratorium, because night 2 re-reports the same set until the
  backlog absorbs it.
- **Therefore:** `BACKLOG.md` is currently an **under-count** of known defects by construction, and it
  is the only surface the ADR-66 gate validates. P9/P10 re-derive the live counts; the *judgment* that
  the number is deliberately incomplete is what does not survive a compaction summary.

**Doc-vs-config drift (P2 is the tooth).** `ARCHITECTURE.md` carries a **Pre-commit roster** in prose;
the repo-root pre-commit config carries the live hook set. `ai-council` has **no automated doc-claim
check**, so if these two have diverged, nothing in the repo reports it. **P2 re-derives whether they
match** — do not assume either direction from this line.

**Point-in-time claims inside `JOURNAL.md` that are already stale-by-design.** The newest JOURNAL entry
closes with a **"Push state (corrected)"** paragraph and a **tag-durability** claim about
`spike/md-parser-evidence` (the rescue of four commits that were reachable from no ref). Both were
written mid-session and both are **re-derivable facts about the remote**, not durable record. **P3 and
P11 re-derive them.** Read the JOURNAL's closing paragraph as *a claim made at a moment*, never as
current state — this is the same recency-peak trap §8 asks the browser to scan for.

**Standing, by reference — carried deliberately, not oversights:**

- **[#77]** `options_considered` corrupted on `main` — the delegation-surface defect, filed as **one
  contract-scoped ticket** precisely to stop a third round of partial patches. Still unruled on its
  *boundary* question (§4).
- **[#76]** verdict-package `artifacts[]` can name a copy the write never produced;
  `scripts/verify_output_writes.py` reports it as a standing **GAP** — visibility is the interim
  mitigation, **not a fix**.
- **[#75]** `secondary_dir` raises where ADR-43 `target_paths` swallows — the canonical-loss class.
- **[#66]** gated on **[#27]**; **[#27]** itself is operator-blocked, not stalled work (§4 item 8).
- **[#82]'s own premise is verifiably FALSE** (backlog audit A5, against source) — and the vision
  audit's H6 **propagated that false premise** before it was disproved. Correcting **[#82]**'s body
  repairs both. This is the one place in the corpus where **one night report corrected another the
  same night**; the correction is recorded but the ticket body is not yet fixed (moratorium).
- **Record-drift residue, unfixed under the moratorium:** the **[#110]/[#128] → [#84]/[#85]** renumber,
  a **dangling `#96` reference**, and **[#4]**'s fired condition (its "closed as not-needed if Gemini
  retained" escape hatch is void because Gemini was **not** retained, so it is now an unblocked
  required ADR-02 amendment — and ADR-02's own *"No open remainder"* stamp is stale the same way
  ADR-01's was before this window refreshed it).
- **Severity dispute, unadjudicated:** the combined review's **X2** — `BACKLOG.md` files **[#69]** as
  P2 while the code audit argues P1. Unaddressed in the ticket's own text.

**Do not trust any of the above as current state** — P2/P3/P4/P7/P9/P10/P11 re-derive it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (four entries dated **2026-07-21**) already encodes the detail; do not
re-read it as narrative here. **The window's defining property: heavy audit + real code, zero filing.**

- **Night-audit batch reintegrated** — four read-only reports off three worktrees (vision + input-layer
  on one branch; code; backlog-trust), then a **combined review** synthesizing all four. → JOURNAL
  2026-07-21 "night-audit reintegration"; `docs/audits/2026-07-21-night-audit-combined-review.md`.
  Three prompt-vs-reality mismatches were **recorded rather than silently repaired** (branch naming;
  only three worktrees existed, not four; all three worktree locks named **dead PIDs** — checked with
  `Get-Process` *before* touching anything, then `unlock` + plain `remove`, never `-f`).
- **LANE A — provider-layer fixes** (audit ids P1-1 / P1-3 / P1-7), merged. Typed error dispatch by SDK
  class **name** (so one table covers both hierarchies without importing either SDK into `base.py`);
  `_parse()` brought inside `generate()`'s guard; per-event-loop lazy client caching compared by object
  identity. `gemini.py` **untouched — it was already correct and stays the reference implementation.**
- **LANE B — orchestration-resilience fixes** (audit ids P1-2 / P1-8 / P1-9), merged. `return_exceptions`
  + isinstance triage; seat status derived from the **last completed round** (new `lost` status); a
  synthesis failure now **preserves the paid-for transcript + metrics** instead of discarding the run.
  Held **strictly inside contract-1.0** — discharged by grep before coding, pinned by a key-set equality
  test. **Four terra passes, three productive** — every finding reproduced with a failing test first.
- **Closure hygiene** — **[#2]** and **[#3]** struck (the only two done-but-listed of the open set; both
  done-whens **re-verified first-hand against source**, not accepted from the audit). **[S1]** fully
  delivered → collapsed per ADR-65 (hub). ADR-01's Deployment-Status stamp refreshed. → JOURNAL
  2026-07-21 "closure hygiene".
- **Orphan-evidence rescue** — `git tag spike/md-parser-evidence` anchored a **4-commit arc reachable
  from no ref at all** (`git fsck --unreachable`); a `gc --prune=now` would have destroyed it
  irreversibly. It is the evidence base **[#80]/[#81]**'s ruling depends on, and its tagged tip is the
  commit where the spike **retracted its own conclusion**. **P11 re-derives whether that rescue is now
  durable off-machine** — the JOURNAL's claim about it is point-in-time (§1).
- **Nothing filed, nothing struck beyond the two above** — the moratorium held in every one of the four
  sessions, each recording it explicitly. This is the state §4 item 1 asks you to rule on.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
> ## ⚠ READ THE SUPPLEMENT ANSWERS FIRST — THEY OUTRANK THIS SECTION'S FRAMING AND ITS ORDERING
>
> This residual is **repo-derived**; the supplement carries the outgoing architect's own *why*, and on
> **four** points it does not merely re-rank this section — it **overturns** it. Where the two disagree,
> **the supplement wins on intent and priority**; this section stays authoritative on *what the defects
> are*. Everything factual in both is still re-derived live (P2–P12).
>
> 1. **This is NOT a decision session. It is an EXECUTION session.** CC's framing below ("a decision
>    session, not a build session") is **wrong** — it was inferred from a record in which nothing was
>    filed. The operator's standing demand, stated plainly: *the theory is done — audits, intakes, ADRs,
>    plans all exist — and he wants them **executed intelligently**, not added to.* **Treat "produced
>    another document" as a failure signal for this window.**
> 2. **Item (1) below — the moratorium — is ALREADY RULED.** The operator lifted it mid-window. Do not
>    re-open it. What survives is not a decision but *inherited absorb-work* (P12 measures it).
> 3. **Item (3) below — H1 — is ALREADY RESOLVED, and not in the shape this section states.** It is
>    **not** a fork between "decision engine" and "boosting engine"; the operator ruled it a
>    **SEQUENCE**: the Council is a decision engine whose **input stage is question-boosting**. Neither
>    half stands alone — a foreign repo does not know the template or the methodology, so a raw question
>    must be boosted into a well-formed brief *before* the debate can decide well. **`VISION.md` must be
>    amended** to state that chain. The one thing still genuinely open is the boost layer's **OWNER** —
>    **(A)** caller-side advisor (`#36`; Council stays a stateless CLI per ADR-11, but the caller must be
>    able to execute the boost) vs **(C)** council-side entry stage (caller needs to know nothing, but
>    this **reopens ADR-11**). The operator's own framing — *"the foreign repo does not know the
>    methodology"* — pushes toward **C**. **Rule A-vs-C and amend VISION + ADR-11 BEFORE building the
>    boost layer**, or the build anchors the wrong side.
> 4. **Item (4) below is the *input* to that ruling, not work to re-derive.** The 2026-07-21
>    input-layer night audit already designed the boost architectures and named this exact ADR-11
>    tension. Do not re-audit it.
>
> **The supplement's build order supersedes this section's ordering:** (1) rule H1's owner + amend
> `VISION`/ADR-11; (2) **build the boost layer** — the core of the vision and the least-built part of
> the chain; (3) **build the claim-vs-reality checker** (this section's item 9, now with a verdict —
> see the note there); (4) `#4`'s ADR-02 amendment; (5) `#81` ruling + the remaining P1 waves + the
> backlog renumber.
>
> **Also settled by the supplement, do not relitigate:** the **markdown-it-py** spike ran to decision —
> **KEEP-SCANNER** (the library *inverts* `#81`'s failure mode and regresses perf ~11.6× inside
> `md.parse`); recommendation is to hand-port only the fence-skip structure. And the cross-lane lesson
> repeated *again* this window: Lane B relocated a `classify_error` consumer and widened a `seat_router`
> except clause, so Lane A's code ran on inputs neither lane predicted — **only the merged-tree gate
> caught it.** Standing rule reconfirmed: **verify cross-lane contracts on the MERGED tree, never
> per-lane.**

**What follows is CC's repo-derived reading, retained for its defect detail.** Ordered by how much each
constrains the others — **an ordering the supplement supersedes** (see the block above). The window
just past produced four audits, a combined review, and six real fixes.

> **Carried forward from the PREVIOUS architect supplement (2026-07-20) — do NOT relitigate.**
> These were settled by the outgoing architect one window ago and nothing since has disturbed them:
> **(i)** do **not** couple a *compliance* fix to a Contract-Version bump — a compliance fix forces no
> bump (precedent **[#39]**); **[#34]** + **[#76]** remain the 1.1 pair. **(ii)** The lane-split
> standing rule: *before splitting lanes, list each lane's changed **public signatures** and grep the
> others* — file-disjointness is **not** contract-disjointness (this cost a RED `main` once already).
> **(iii)** Do not redo: the A2→A1→C merge order, the two-contract split, the **[#68]** registry-check
> design, the F8 marker-drop, or the 1.0-stamp-holds ruling.

**(1) ~~THE MORATORIUM — lift, hold, or scope it.~~ ✅ ALREADY RULED — LIFTED mid-window by the
operator. Do not re-open.** *Retained only for the mechanism it explains: why the backlog is an
under-count, and why P12's absorb-work exists. The reasoning below about what the moratorium was
protecting is answered — read it as background, not as an open question.*
A filing moratorium has held for the whole window (§2). The combined review is explicit that it blocks
**two of its own top-five actions** — absorbing the new `P1` set into tickets, and closing the verified
record drift — while the other three are **not** blocked. It is also explicit that the moratorium, *not
audit design*, is what binds the **cadence** question (item 7): a finding-audit only becomes
re-runnable-with-value once the backlog has absorbed its previous output, so a held moratorium
guarantees the next code sweep re-reports the same findings. **The open question is not "is filing
good"** — it is *what the moratorium was protecting*, and whether a **scoped lift** (absorb-and-renumber
only, no new feature filing) buys the cadence back without reopening whatever the freeze was for. **CC
cannot see the reason for the moratorium — it is off-repo. Ask the operator first (§13d beat).**

**(2) Rule [#81] — the preferred-failure question. Highest-leverage unmade decision; NOT
moratorium-blocked.**
Both Opus reports independently name it the top outstanding *decision*, and two sessions have now spent
effort downstream of it. The fork: a fenced code block inside an options section is read as list items,
so a fenced diff **fabricates** authoritative options; but making extraction fence-aware **inverts the
failure mode** — if a model ever fences its real options list, fabrication becomes *total option loss*.
**Neither failure is free; the ruling is which one you prefer.** The relevant prior is the **F8
precedent**, where the operator chose *under-match toward the loud failure* — `[]` is honestly empty,
`['Risk one']` is plausibly wrong and consumed silently. That principle, if reaffirmed, decides this.
**It is also upstream of [#77]'s real architectural question** (below), and of **[#80]** (multi-line
option truncation, the same design-fork class). **The evidence base is the rescued spike tag** — whose
tip is the commit where the spike *reversed its own conclusion*, which is precisely the substance the
ruling turns on. Confirm the evidence is durable (**P11**) before ruling on it. **Supplement update:
the spike ran to DECISION — KEEP-SCANNER**, because the library *inverts* the failure mode (the scanner
fabricates options from a fence; the library loses the whole list when the options are fenced) and
regresses perf ~11.6× inside `md.parse`. **Neither option satisfies `[#81]`'s done-when, so the ruling
is still owed** — but the tool choice is settled, and the recommendation is to hand-port only the
fence-skip structure (the one CommonMark rule the spike proved real). **[#80]** rides the same ruling.

**(2b) [#77] — the boundary question underneath the ticket.**
Filed as **one** contract-scoped ticket to force an *ex-ante* contract with tests written before the
fix. But the open **architectural** question is not the regexes: **should option extraction remain
heuristic parsing of synthesizer prose at the output layer at all, or should the synthesizer be asked
to emit structured options directly, so there is nothing to parse?** Every patch so far has assumed the
former without ever deciding it. Rule the boundary, then the contract writes itself.

**(3) ~~Rule H1 — the vision fork.~~ ✅ ALREADY RESOLVED, and the shape below is WRONG.** The operator
ruled H1 a **sequence, not a fork** — decision engine with question-boosting as its input stage (see the
correction block above; the live question is the boost layer's **owner**, A vs C). *Retained for the
evidence it cites — the `ideas`-path thinness and the `[#55]`-adjudicator caveat are still true and
still bear on how the boost layer gets built.* **Do not run the for/against survey below as an open
question.**
`VISION.md` frames a *"multi-model AI debate and research tool for architectural decision-making"*;
the vision audit's H1 finds a **creativity/boosting engine** in the mission framing that the record does
not carry (the `ideas` mode is the least-developed path — one round, no divergence step, and the quality
rubric scores *fidelity*, not *novelty*). **Three of the four night reports touch this fork; none can
resolve it** — the combined review says so explicitly and assigns it to the operator. The vision audit
offers the same fork one level up as **Position 1** (keep the direction, buy the evidence) vs
**Position 2** (reframe from *debate engine* to **adjudication engine** — concentrate on heterogeneous
*verification* rather than heterogeneous *generation*). **Note the honest caveat the report makes about
itself:** its §1 for/against survey is **low-value and will regenerate verbatim** until its own
adjudicator (**[#55]** baseline experiment) actually runs — so H1 is a decision to be *made*, not a
decision to be *researched further* by re-running the same audit.

**(4) The input-layer architecture fork — do not start it before H1.**
The input audit is an **ADR seed, not a decision**: every contested point deliberately holds ≥2 live
options. Three boosting architectures are "held in tension" and the report is explicit that the
**first build choice is the load-bearing one, because each anchors a different owner** — **A** single-shot
reformulator (anchors caller-side), **B** bounded clarify-loop (anchors an interaction channel), **C**
classify-then-decompose (anchors a council-side entry stage). The routing fork (R1/R2/R3) is
**explicitly H1-sensitive** — the mechanism is shared either way, *only the default flips*. Two further
sub-forks stay open: gate posture (hard / advisory / hybrid) and the approval mechanic (two-phase
commit vs inline-with-consent). **ADR-11 reopening:** the report's verdict is that **A and C do not
reopen it** (both fit CLI-as-ABI); **only B done properly does**, because it needs MCP elicitation.
**One genuinely new ground-truth fact worth carrying:** `detect_mode()` **structurally cannot emit
`research`** — that mode is unreachable by auto-detection and must be forced via flag or frontmatter.
This is not in `BACKLOG.md`.

**(4b) The cross-repo governance tension inside item 4 — the architect's own call.**
The input audit names it directly: **hub ADR-95's lane discipline is in direct tension with boosting
itself**, because a boost that improves a weak question is *shaping substance*, which ADR-95 reserves
for the architect. The report offers a candidate line — **the boost may restructure, interrogate, and
flag; it may never assert a fact the caller didn't give.** That candidate is the thing to accept,
amend, or reject. It is a **hub-governance** question surfacing inside an ai-council build decision,
so it is genuinely yours and not delegable downward.

**(5) H7 — the crux artifact is excluded from the verdict package. Flagged as the strongest single new
finding in the night set.**
The tests pin that the crux artifact *"must stay OUT of the verdict package."* Consequence: **a Lane-A
caller cannot tell a grounded verdict from an ungrounded one without parsing the transcript — which is
exactly what the verdict package exists to spare it from.** Two live options: carry it as a **rider on
the [#34] + [#76] Contract-1.1 batch**, or **defend the exclusion explicitly in an ADR**. Either is
defensible; leaving it undecided while [S13]'s caller-side advisor gets built is not, because the
advisor is the consumer that would hit it.

**(6) Contract-Version 1.1 — decide the bundle and cut it. [#34] + [#76].**
Both change the delegation surface, so they version **together**, not piecemeal. **[#34]** =
research-path verdict-package parity (a Lane A *research* commission currently gets no transcript-free
deliverable at all — debate-path-only was an explicit architect ruling, not an oversight).
**[#76]** = two-pass write, so the manifest is serialized only after the writes it describes land.
**Open:** does **H7** (item 5) ride in this same bump? Per the carried-forward ruling above, **[#77]
does not** — it is a compliance fix.

**(7) Audit cadence — the practice is worth keeping; the *clock* is what is wrong.**
The combined review's answer to "which of these should run nightly" is *"none of them, as run"* — three
are **triggered** audits and one is triggered-at-full-scale. Named triggers: the vision axis fires when
H1 is ruled, when the **[#55]** baseline lands, or when an ADR changes direction; the input-layer axis
**should not re-run at all until a ruling lands**; the backlog axis fires at **merge-arc** cadence; the
code axis fires at full-sweep scale, and its *nightly-shaped* equivalent **already exists** as
diff-scoped `/codex-review`. **Decide the trigger set, and note the dependency: this is downstream of
item 1** (a held moratorium makes every re-run report the same findings).

**(8) [#27] Phase-3 blind scoring — CARRIED FORWARD UNMOVED, and the previous architect ranked it
FIRST.**
The 2026-07-20 supplement named it *"THE highest-leverage item, the one objective function of five that
missed"* — non-delegable, one operator sitting, and it gates the ADR-12 §5 flip → **[#41]** → **[#66]**.
**This window did not touch it.** It is surfaced here explicitly because the defect-driven ordering
above **structurally cannot see an operator-blocked scoring task** — the same blind spot the previous
residual had to be corrected for. **Decide where it ranks now; do not let it disappear for a fifth
consecutive window by default.**

**(9) Enforcement asymmetry with the hub — ✅ RULED (b), and PROMOTED to this window's headline BUILD.**
The supplement settles it and escalates it: the claim-vs-reality failure is now **systemic across every
artifact layer**, not just code — a docstring says *"Never raises"* while the code can (`P1-1`); ticket
**[#82]** asserts retrieval-on-every-debate while the code makes it conditional; an ADR-01 stamp claimed
an open residual thirteen lines above where it had been discharged. **The ruling is to BUILD the
mechanism:** one composed, **read-only "repo-health" checker** that compares **claims against reality**
— doc-vs-config, docstring-vs-behaviour, ticket-premise-vs-source — and **fails loud on drift**. That is
step (3) of the supplement's build order, and it is the concrete discharge of the 2026-07-20
enforcement-asymmetry question. *The two readings below are retained only as the rationale; (b) won.*
`ai-council` has four independent read-only validators and **no consolidated gate**; the hub has a
registry, a ship-gate verdict, and a disposition register. Two honest readings: **(a)** correct —
`ai-council` is a *code* repo, the hub is a *governance* repo, so their enforcement shapes should
differ; or **(b)** a gap — several `ai-council` gates pass **silently**, so there is no single place to
read *"is this repo healthy."* **New evidence for (b) this window:** the combined review's cross-cut
**C4** — *prose asserts guarantees the code does not honour* — which it calls **the most transferable
finding in the night set**, and which is the doc-vs-config drift **P2** exists to catch. **Do not close
this by defaulting to hub parity — rule on it.**

**(10) The inbox/CLI parity blind spot — [#69]. Structural fix, or stop calling it a blind spot.**
`LESSONS.md` records this pattern **three separate times**, each with the same rule: *investigate
whether the two paths can share a common processor; if not addressable structurally, add a parity
test.* **[#69]** is the next instance — the two entry points guard the same frontmatter key on
**different conditions**, so the same brief file yields a different panel via `--file` than via
`--inbox`. The recurrence count now argues the structural change was warranted several instances ago.
**Also unadjudicated: its severity** (combined-review **X2** — filed P2, the code audit argues P1).
Patching it in isolation makes it instance four of five.

**(11) Rulings owed + carried triage — pointer only, deliberately not expanded here.** Named in the
JOURNAL's own "rulings still owed" line: **[#6]**, **[#8]**, **[#73]**. **[#4]** is no longer merely
"owed" — the supplement confirms its condition **fired at strike time** (the Gemini escape hatch is
void), making it an **unblocked, required ADR-02 amendment** and **step (4) of the build order**, with
a stale *"No open remainder"* stamp mirroring the ADR-01 one this window fixed. **The supplement also
carries forward, in its own words:** **[#19]** F4-lift (undesigned), codex **H3** (`_client_for_loop`
abandons the old SDK client on rebind — needs an async close lifecycle), a **test-mock-integrity
sweep** (a broken mock made a **live API call** this window, so other suites may hide the same), the
remaining **P1-6/10/11** and **P1-14/15/16** waves plus ~30 P2/P3, and two machine-level gotchas to
route to the **hub** rather than fix here. **Read those from the supplement ANSWERS, not from here** —
re-narrating them into the residual is exactly the §2 disease this bundle is built to avoid.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the backlog, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per hub ADR-66, `[S<n>]` story ids. Every `#id` in this residual is an **ai-council** id.
  `[E1]` (invocation surface & delegation-readiness) carries the delegation-surface work §4 items
  5/6 are about; `[E6]` (council process & epistemic quality) carries the H1/input-layer work.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** — this is a cross-repo handoff and the
  hub is **read-only-adjacent**: it hosts the bundle, it is not the subject.
- **The backlog is a known under-count right now** (§1) — the moratorium means fixed-but-unticketed and
  found-but-unfiled work exists outside it. **P10 grooms the whole open set at boot** (live / dead /
  awaiting-ruling per open `#id`); **that grooming is the operator-ruled boot obligation, not optional**,
  and this window it must *also* reconcile against the unfiled audit set, which no validator can see.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist. **P4** substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection, and
  **P10 is the judgment layer over it.**

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
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an answer hint.
>
> **Branch note.** This bundle was generated on branch `worktree-ai-council-handoff` **in the hub**.
> That names only which hub branch hosted generation — **re-derive the TARGET's HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P12** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | ai-council |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below confirmed present at generation time by running its command in the target). Where the hub
has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS are folded into `PASTE_THIS.md`, so the incoming §13(d)
> operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*
> **Read the ANSWERS before the residual's §4 ordering** — they correct it on two load-bearing points
> (the moratorium was lifted mid-window; H1 is resolved as a sequence, not a fork), and the supplement
> wins on intent and priority. The residual stays authoritative on *what the defects are*.

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
by CC, substring-matched. **P1a is unusually load-bearing this window, and for a sharper reason than
the residual first stated:** the supplement resolves H1 by ruling that the Council is a decision engine
whose *input stage* is question-boosting — and it says `VISION.md` **must be amended** to state that
boost→decide chain, because today it claims the decision half only. So P1a reads *the exact line that
is slated to change*. Read it live before drafting any amendment to it. **Then, before design, the
operator-context beat fires (§13d)** — **NARROWED**, since the supplement is filled.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run-in root noted) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS`, and no `validate_doc_claims` either; this row restores that missing doc-vs-reality tooth by hand.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and does `ARCHITECTURE.md`'s **Pre-commit roster** prose list that **same set** — or has the doc drifted behind the config? | `ARCHITECTURE.md` (Pre-commit roster prose) ∩ the pre-commit config | the roster drifts every time a gate lands, and `ai-council` has **no automated doc-claim check** to catch the doc falling behind — so a mismatch stays invisible until someone reads both. This is the concrete instance of the combined review's cross-cut **C4** (*prose asserts guarantees the code does not honour*), which that review calls the most transferable finding in the night set; neither the count, the tail id, nor the verdict is in this bundle | **TARGET:** `grep -n 'Pre-commit' ARCHITECTURE.md` for the doc side; for the config side run grep -c and grep-tail for the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the two sets by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it. **The newest `JOURNAL.md` entry makes an explicit push-state claim that was already corrected once mid-session** — treat that paragraph as a point-in-time claim, never as current state | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change, and this window added a large block of them; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **read-only** repo validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Note several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly. That silence is itself the evidence residual §4 item 9 asks the architect to rule on | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | **[RE-BOUND — the stock row bound to the hub bundle dir, which is unresolvable from the target root.]** How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; the count, the tail slug, and whether the index has kept pace are all live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | **[RE-BOUND — `ai-council`'s `validate_backlog` prints NO serialize-groups line; its summary is counts-only.]** What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit, this window moved two of them, and none appears in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **This window the grooming must also reconcile against work that was fixed or found but never ticketed** (residual §1) — a gap no validator can see | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[NEW this window — the orphan-evidence rescue.]** Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors a 4-commit arc that was reachable from **no ref at all** — a `gc --prune=now` would have destroyed it irreversibly — and it is the **entire evidence base that residual §4 item 2's `[#81]` ruling depends on**. A branch push does **not** carry tags, so local-only is a live possibility; only the remote can answer it, and the JOURNAL's claim about it is point-in-time and was already corrected once | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports. **If the remote does not carry it, that is the one item in this handoff that still guards against irreversible loss** — surface it to the operator before any design work begins |
| P12 | **[NEW this window — the moratorium's actual size.]** How many distinct `P1-*` finding ids does `docs/audits/2026-07-20-night-code-audit-opus.md` carry, how many of those does `JOURNAL.md` record as **already fixed**, and how many appear as a filed `[#id]` in `BACKLOG.md`? | `docs/audits/2026-07-20-night-code-audit-opus.md` ∩ `JOURNAL.md` ∩ `BACKLOG.md` | **this is the size of the absorb-work the next window inherits** — the gap between what the repo *knows* is broken and what it *tracks*. The supplement records that the moratorium was **lifted mid-window** and that the fixes went in **fix-on-main with no ticket churn**, so the gap was never closed: the lift removed the *block*, not the *backlog*. It exists only by intersecting three sources at answer-time; no validator computes it (audit finding ids are not `#id`s), and a summary cannot produce it because the sets have still never been reconciled | **TARGET:** `grep -o 'P1-[0-9]\+' docs/audits/2026-07-20-night-code-audit-opus.md \| sort -u \| wc -l`, then read the two 2026-07-21 lane entries in `JOURNAL.md` for which ids they record as fixed, then check `BACKLOG.md` for any corresponding filed id. **Report the gap as a number, not a verdict** |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config file is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked dotfile name is looked up without its dot, which resolves nowhere — the
> probe is then FAILed as a missing target even though the file plainly exists.
> **Consequence: no probe in any bundle — hub or cross-repo — can currently bind to a dotfile.** That is
> a hub tooling defect worth filing (dotfiles are exactly where config gates live); it is deliberately
> **not** patched from inside this handoff, because hub infra changes are exception-with-ruling
> (core-invariant #6). The probe's teeth are unaffected — the comparison is still live-only and
> answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `scripts/validate_backlog.py` all exist in
   both). This is the single most likely failure mode of a cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d), NARROWED** (the supplement is
   filled — ask only *"anything changed since it was written?"*). Then run P2–P12, each against
   **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P12 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." **P7 is the headline substitute** (four exit codes, read
   explicitly — several gates pass silently, so "no output" must not be scored as "no drift").
   **P2 is the hand-built doc-vs-reality tooth** this repo otherwise lacks. **P10 grooms the whole
   open BACKLOG at boot** (live / dead / awaiting-ruling per open `#id`) — the operator-ruled boot
   obligation, not optional. **P11 and P12 are this window's additions**, and their order is
   deliberate: **P11 early** (one command, and it can reveal an irreversible-loss exposure), **P12
   before any moratorium ruling** (it supplies the number that decision is about).
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **FILLED**, so its ANSWERS are folded into `PASTE_THIS.md`
   and the §13(d) beat **NARROWS**. Confirm by looking at the bundle directory in the hub — it is
   CC-side bookkeeping, not target state.

---

=== SUPPLEMENT.md ===

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

SUPPLEMENT ANSWERS — outgoing ai-council architect (2026-07-21); CC transcribes VERBATIM

1. STRATEGIC INTENT (way-of-working level).
The failure this repo keeps paying for has moved up a layer. It used to be "decision recorded ≠
enforced" at the code level; this window's four-axis night audit proved it is now systemic across
EVERY artifact layer — a docstring says "Never raises" while the code can (P1-1); a ticket (#82)
asserts "retrieval on every debate" while the code makes it conditional; an ADR-01 stamp claims a
residual open 13 lines above where it was discharged. The next session's way-of-working goal is NOT
another audit and NOT another plan — it is to build the ONE mechanism that closes this class: a
composed, read-only "repo-health" checker that compares CLAIMS against REALITY (doc-vs-config,
docstring-vs-behaviour, ticket-premise-vs-source) and fails loud on drift. This is the §4(4)
enforcement-asymmetry ruling from 2026-07-20, now with overwhelming evidence. The operator has been
explicit for two windows: the theory is done, the plans exist, the audits/intakes/ADRs are written —
what he wants is INTELLIGENT EXECUTION of that theory, not more of it. His priority framing for the
whole project, in his words: managing the methodology and the ecosystem — naming, versions, where each
concern lives (documented vs coded) — not just the LLM debate. Treat "produced another document" as a
failure signal for the next window.

2. TENSIONS WEIGHED.
(a) Moratorium vs execution. The intake/ADR moratorium was holding back the audits' highest-value
output (~10 verified P1s + backlog drift). Landed: operator LIFTED it mid-window on explicit
instruction ("puść prąd"). The fixes went in fix-on-main (no ticket churn); JOURNAL records them.
(b) Parallelism by file-surface. ~10 P1s split into two parallel code lanes (providers/ ∥
debate+output+synthesis+orchestrator+models) + one docs lane. Held: file-disjoint is necessary, not
sufficient — proven AGAIN this window. Lane B relocated the classify_error consumer (debate.py:68→:99)
and widened seat_router's except from ProviderError to Exception, so Lane A's classify_cli_failure now
runs on any exception. Neither lane summary predicted the coupling; only the combined-tree gate (793
tests) caught it. STANDING RULE reconfirmed: verify cross-lane contracts on the MERGED tree, never
per-lane.
(c) Audit cadence vs cost. Four Mythos/Opus night batches produced value ONCE. Landed: none is a
nightly routine — vision/input are TRIGGERED (regenerate until a ruling lands), backlog is merge-arc
cadence, code full-sweep re-reports the same P1s until absorbed (its nightly-shaped form is
/codex-review, which already exists). The real cadence binder is the moratorium, not audit design.
(d) Buy-vs-build enforced. The markdown-it-py spike was run to DECISION before adoption: KEEP-SCANNER,
because the library inverts #81's failure mode (scanner fabricates options from a fence; library loses
the whole list when the options are fenced) and regresses perf 11.6x inside md.parse. Neither satisfies
#81's done-when — the ruling is still owed.

3. CONSIDERED + REJECTED (do not relitigate).
- Adopting markdown-it-py to dissolve #80/#81 — REJECTED: it only inverts #81's failure mode and
  regresses perf; recommend KEEP-SCANNER + hand-port the fence-skip structure (the one CommonMark rule
  the spike proved real).
- Running the P1 fixes as one worktree — REJECTED: file-surface split into disjoint lanes; a combined
  acceptance contract would have stopped being checkable.
- Emitting the verdict package on synthesis failure (P1-9) — REJECTED: it hardcodes exit_semantics:0,
  which would assert a usable verdict that does not exist against the real exit 1. Preserve transcript
  + metrics only; exit stays 1.
- Two-value provider_statuses (P1-8) — REJECTED: flattening back to ok/failed loses exactly the
  mid-debate-loss signal the fix exists to surface. Landed three-value ok/lost/failed, proven
  contract-1.0-safe by grepping every consumer.
- Nightly full-src code audit as a standing routine — REJECTED: it re-reports the same findings until
  the backlog absorbs them; the diff-scoped form already exists as /codex-review.
- Treating H1 as an either/or fork (decision engine VS boosting engine) — REJECTED by the operator:
  it is a sequence, not a fork (see 4).

4. OPEN QUESTIONS / DEFERRED (ranked by leverage).
- H1 — RESOLVED by the operator, and the resolution sharpens the next build. It is NOT a fork between
  "decision engine" and "boosting engine" — it is a SEQUENCE: the Council is a decision engine whose
  INPUT stage is question-boosting. Neither half stands alone — a foreign repo does not know the
  template or the methodology, so a raw question must be boosted into a well-formed brief (by type:
  research vs decision) BEFORE the debate can decide well. VISION.md must be amended to state this
  boost→decide chain explicitly (today it claims "decision engine" only, and the boost layer
  #36/#37/#38 is the least-built part of the chain). The ONE thing still genuinely open is the boost
  layer's OWNER, and it is a real ADR-11 decision, not a preference: (A) caller-side advisor (#36) —
  boost runs as prompts in the foreign agent, Council stays a stateless CLI per ADR-11, but the caller
  must be capable of executing the boost; (C) council-side entry stage — Council boosts the raw
  question itself as a first stage, the caller needs to know nothing, but this REOPENS ADR-11 (Council
  is no longer a pure stateless CLI). The operator's own framing ("the foreign repo does not know the
  methodology") pushes toward C. Next window: rule A vs C, amend VISION + ADR-11 accordingly, THEN
  build the boost layer — do not build the advisor before this owner ruling lands, or it anchors the
  wrong side. The 2026-07-21 input-layer night audit already designed 2-3 boost architectures and
  named this exact ADR-11 tension — it is the input to this ruling, not a re-derivation.
- #4 — a LIVE knock-on this window created: striking #2/#3 fired #4's condition (its "closed if Gemini
  retained" escape hatch is void — Gemini was not retained). #4 is now an unblocked REQUIRED ADR-02
  amendment with a stale "No open remainder" stamp, mirroring the ADR-01 stamp fixed this window. Not
  deferred by choice — it became live at strike time.
- #81 fabrication-vs-total-loss — highest-leverage OUTSTANDING code ruling; two windows have spent
  effort downstream of it. Evidence now tag-preserved (spike/md-parser-evidence, on origin).
- #27 Phase-3 blind scoring, still 0/12 — the operator sitting that gates the ADR-12 §5 CLI-default
  flip → #66. Non-delegable, unchanged.
- #19 F4-lift (design the runtime framing alarm + role — undesigned) — deferred; T1 shipped #18 solo.
- The enforcement mechanism itself (Strategic Intent §1) — the deferred BUILD, not a question.

5. DECOMPOSITION RATIONALE.
Split by FILE SURFACE, not ticket, and verified public-signature disjointness before splitting — then
STILL caught a cross-lane contract coupling on the merged tree (see 2b). What the next session must NOT
redo: the P1-1/2/3/7/8/9 fixes (landed, 793 green, terra-passed); the #2/#3 strike (done, verified);
the markdown-it-py spike (decided — KEEP-SCANNER); the four night audits (run — their findings are the
input, do not re-audit). What it MUST do fresh, in order: (1) rule H1's owner (A vs C) + amend
VISION/ADR-11; (2) build the boost layer per that ruling — the core of the vision, least-built part of
the chain; (3) build the claim-vs-reality checker as the first execution of the enforcement-asymmetry
ruling; (4) #4 ADR-02 amendment; (5) #81 ruling + remaining P1 waves + backlog renumber.

6. OFF-REPO CONTEXT.
The operator's standing demand, stated plainly this window: the theory is DONE — audits, intakes, ADRs,
plans all exist — and he wants them EXECUTED INTELLIGENTLY, not added to. The four night reports + the
combined review (docs/audits/2026-07-21-night-audit-combined-review.md) are the vision material — read
that ONE file first. Recurring machine-level gotchas to route to the hub, not fix here: (1) worktree
locks outlive their process — Get-Process the pid before any -f -f (fired 3x across two windows);
(2) the codex-review severity counter prints "High 0" over real HIGH findings — console-only regex
defect, read the artifact body not the counter (fired 3x). Triage carried forward, unfiled: codex H3
(_client_for_loop abandons the old SDK client on rebind — needs an async close lifecycle, out of the P1
lane); a test-mock-integrity sweep (a broken mock made a LIVE API call this window — other suites may
hide the same). Remaining waves: P1-6/10/11 (research), P1-14/15/16 (test-integrity), ~30 P2/P3;
backlog edits now unblocked: renumber #110→#84/#128→#85, resolve dangling #96, correct #82's overstated
premise. main was +22 ahead of origin at write time — confirm the push landed before trusting this
bundle's SHAs.
