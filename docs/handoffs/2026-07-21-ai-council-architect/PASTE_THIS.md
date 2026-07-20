=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-21-ai-council-architect` |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-21-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Target repo** | **`ai-council`** — CROSS-REPO handoff (ADR-36/41). The bundle lives in the `.dev-knowledge` hub; the **subject** is the sibling repo `ai-council`, and every probe binds to **its** files, resolved from **its** root. The hub is read-only w.r.t. the target. |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**CROSS-REPO — the target is `ai-council`, not the hub.** Rule on the design forks the 2026-07-20 window deliberately left open rather than patched: **`[#80]`/`[#81]`** (where `RESIDUAL.md` §4 item 1 shows the operator-ruled doctrine and `[#81]`'s own done-when **contradict each other**, so no implementation can close it as written), the **buy-vs-build** question the markdown-it-py spike deferred on one unanswered empirical premise, and the twice-deferred **Contract-Version 1.1** bundle (`[#34]` + `[#76]`). **Time-critical:** §1's headline flag is that the spike's *evidence* — the empirical basis for the first two rulings — is currently in an **unreachable git object awaiting `gc`**; `PROBES.md` **P11 re-derives whether it still exists and should be run EARLY**. Navigate from `ai-council/BACKLOG.md` (theme backbone `[E1]`–`[E7]`; `[E1]` carries most of the above) — and note **`RESIDUAL.md` §4 is the payload here, not §2**.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/ai-council-architect-handoff-0721`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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
> the hub's governance corpus, and CC made **no** change to `ai-council` while generating this bundle
> (including the recoverable-but-unreachable spike evidence in §1 — surfaced, deliberately not
> recovered). The stock generator probes were hub-bound and have been **re-authored against
> verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which and why).

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the target's **own** read-only checks (`scripts/canonical_freshness_gate.py`,
`validate_docs_registry`, `validate_sealed_keys`, `validate_audit_casing`, `validate_backlog`) plus
judgment over `BACKLOG.md` ∩ git — **not** by the hub's `audit.py`, which `ai-council` does not have.
**Re-derive each at read-time — the teeth are in `PROBES.md` (P4/P6/P7/P9/P11/P12), not in trusting
these lines.** This bundle states **no** verdict, exit code, WARN count, drifted `#id`, or count —
those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS part of the headline).** `ai-council` has **no
counterpart to the hub's drift-flag machinery** — no `audit.py ship-gate`, no
`ecosystem/disposition-register.yaml`, no `validate_doc_claims`, no `validate_git_backlog`. There is
therefore **no dispositioned-WARN set to inherit and no standing-vs-new distinction** in the hub's
sense. The target's drift surface is four independent read-only validators plus judgment over
`BACKLOG.md` ∩ git — which is why `PROBES.md` P2/P4/P6/P7 are re-bound rather than run as generated.
**Treat the absence of a consolidated verdict as the flag**, not as a green light: several of those
gates pass *silently*, so "no output" is not "no drift" (P7 reads exit codes explicitly).

**⚠ NEW — and the loudest flag in this bundle: the markdown-it-py spike's EVIDENCE is unreachable.**
The spike branch `chore/spike-md-parser` was deleted with `-D` after teardown. Its JOURNAL prose was
preserved by two cherry-picks — but **those cherry-picks carried `JOURNAL.md` only.** The spike's
actual artifacts (`spike/FINDINGS.md`, `spike/evidence.py` — including the `#81c INVERSION` cases —
plus four implementation files) exist **on no branch**. They survive solely inside a commit object
that is reachable from **no ref**, i.e. dangling and eligible for `git gc`. The teardown JOURNAL entry
**predicted this exact risk in writing** ("cherry-pick … to main if it should survive worktree
teardown") and the mitigation was applied only to the prose half. Recovery handle while it lasts:
**`26192dd`** (`git show 26192dd:spike/FINDINGS.md`). **P11 re-derives live whether it is still
there** — if `gc` has run, this is already unrecoverable.

Why this is the headline and not housekeeping: **§4 items (1) and (2) ask the architect to rule on
`[#80]`/`[#81]` and on buy-vs-build — and the entire empirical basis for both rulings is in that
dangling object.** The perf measurement and the inversion proof are currently prose claims whose
witness is unreachable, in a repo whose own freshly-minted doctrine is *"a report without a
re-runnable checker is a claim, not a witness."* **Recovering or deliberately discarding this is a
decision, and it is time-boxed by `gc`, not by the architect's convenience.** (Read-only bundle: CC
did **not** recover it — that is the target's call, ADR-36/41.)

**CLEARED this window (the prior bundle's single biggest standing flag):** `options_considered`
corrupted on `main` is **fixed and struck** — `[#77]` closed as one contract-scoped ticket, not a
third round of partial patches. The prior handoff's §4 item (1) is **answered**; do not re-open it as
though it were still live.

**Standing, by reference — carried deliberately, not oversights:**

- **Delegation-surface defects still open:** `[#75]` (`secondary_dir` raises where `target_paths`
  swallows), `[#76]` (verdict package names a return copy that never landed), `[#78]`
  (`target_paths` accepts destructive iterable shapes), `[#79]` (failed metrics sidecar can still
  enter the manifest). All four were classified **PRE-EXISTING by differential run**, not by diff
  reading — none were introduced by a merge.
- **`[#66]` stays OPEN, gated on `[#27]`** (CLI-backend scoring); no billed witness authorized. A
  cost decision awaiting the operator — not a stalled task.

**NEW this window, by reference:**

- **A pre-push gate was deliberately bypassed.** `block-ff-push` refused the `#18` push; the operator
  authorized `--no-verify`. **Live re-derivation corrects the JOURNAL's framing on scale:** the entry
  reads as a 3-commit anomaly, but the non-merge population on `main`'s first-parent spine is **very
  much larger and long-standing** (P12 re-derives the live number — it is deliberately not stated
  here). The dominant shape is the *post-merge journal-anchor commit*, which lands direct on `main`
  because a `--no-ff` merge leaves you standing on `main`. So this is a **systemic tension between an
  established anchoring practice and core-invariant #5**, not a one-off — and the gate will keep
  refusing. The decision to not rewrite history was right; the *recurring* condition is unruled.
- **`[#83]` is date-gated:** the `#18` crux-check terra **pass-2 repairs carry no adversarial
  re-review** (pass 3 blocked by a codex usage limit until 2026-07-25). Merged code, unreviewed
  repairs, on a documented deferral.
- **`[#18]` merged but NOT closed** — no live end-to-end witness (every crux path is mock-tested).
  Correct per the doctrine; it means merged ≠ witnessed here, deliberately.
- **A large WEAK closure-proposal backlog is unreviewed** and re-proposes at each session end; only
  `[#77]` was reviewed by operator instruction. P10 grooms the whole open set at boot.

**Do not trust the above as current state** — P4/P7/P9/P10/P11/P12 re-derive all of it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (the **2026-07-20** block, nine entries) already encodes the detail; do
not re-read it as narrative here. **Window boundary:** this covers work landed *after* the
`2026-07-20` bundle was cut — that bundle predates all of it.

- **`[#77]` `options_considered` settled AS ONE CONTRACT and struck.** Six consecutive adversarial
  (terra) passes, each returning real defects; rebuilt on a lane branch, merged, then closed via
  `/review-closures` scoped to `#77` alone. → JOURNAL 2026-07-20 (the six-passes entry + the strike
  entry).
- **The pass-4 finding is the window's real lesson:** the rebuild **introduced a HANG** on an
  ordinary Windows path string, and it **survived three prior review passes**. Answered with fuzz
  guards (termination + non-fabrication, deterministically seeded) rather than another point fix.
- **`[#80]` / `[#81]` filed as DESIGN FORKS — deliberately not fixed.** Both pre-existing; both need
  a ruling, not a patch. Filing-instead-of-widening was explicit: *"quietly widening scope is
  precisely how the previous two fix windows on this function failed."*
- **markdown-it-py buy-vs-build spike — THROWAWAY, recommendation KEEP-SCANNER.** Time-boxed,
  committed-and-stopped, never merged, branch `-D`'d; `src/` never touched. Grounds: a large perf
  regression **and** the `#81` inversion (below). → §1 for the evidence-reachability flag.
- **A published spike verdict was RETRACTED on `main`.** The spike first concluded `#81` was
  *dissolved* by the library; re-testing the half it had not tested showed the opposite. The
  retraction was committed rather than the original entry edited (append-only respected).
- **`[#18]` bounded crux-check Phase A built and merged** — new `crux_check` service + headless
  research executor, wired through orchestrator/synthesis/metrics, with mutation-tested verdict-package
  guards and mechanically-verified boundedness (untouched modules proven byte-identical).
  **Merged, NOT closed.** → JOURNAL 2026-07-20 (the crux entries).
- **Two tickets filed *before* they could become silent debt:** `[#82]` (an accepted Phase-A hole,
  filed **before any implementation**) and `[#83]` (the blocked adversarial re-review, date-gated).
- **`main` pushed** through a deliberate, operator-authorized pre-push bypass (§1).
- **Housekeeping:** two worktree teardowns, both hitting the **same stale-lock / dead-PID** pattern —
  now a repeat, and both resolved by verifying the PID before escalating (no forced removal).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The design questions this window **surfaced but deliberately did not settle**. Resume these; do not
rediscover them. Ordered by how much each constrains the others.

> **Two corrections to the PRIOR bundle, re-derived live — apply before ranking anything.**
> 1. Its §4 item (1) (`options_considered` as a contract) is **DONE**, not open — `[#77]` is closed.
> 2. Its §4 item (3) asserted `LESSONS.md` records the inbox/CLI parity pattern *"three separate
>    times."* **Live re-read: it carries TWO write-ups** — and *each independently claims to be the
>    "3rd instance,"* while naming **different** third incidents. See item (4): this makes the case
>    for the structural fix **stronger** than the prior bundle argued, not weaker.
>
> The supplement (if filled) outranks this section on *intent and priority*; this section stays
> authoritative on *what the defects are*. Everything factual in both is re-derived live (P2–P12).

**(1) `[#80]`/`[#81]` — rule on the preferred failure. The doctrine and the done-when CONTRADICT
each other, and nobody has said so yet.**
This is the item the spike was run to inform, and it is now **evidence-backed and blocking**. The
spike proved **neither implementation satisfies both halves of `[#81]`'s own done-when**: the
line-level scanner *fabricates* options out of a fenced diff, while the library *totally loses* a
fenced options list (returns empty). Here is the contradiction the record does not yet name:

- The `[#77]`/F8 doctrine, operator-ruled and now in `LESSONS.md`, is **under-match toward the loud
  failure** — *"`[]` is honestly empty; `['Risk one']` is plausibly wrong and consumed silently."*
  That doctrine **prefers total loss over fabrication.**
- `[#81]`'s done-when requires *"a fenced options list is shown **not to be silently emptied**"* —
  which **forbids exactly what the doctrine prefers.**

So the ticket cannot be closed as written, by any implementation, while the doctrine stands. **The
ruling is therefore not "which parser" — it is "amend `[#81]`'s done-when to match the doctrine, or
carve out an exception to the doctrine for this case."** Resolve that first; the implementation
question collapses once it is answered. (`[#80]` — continuation-line vs nested-annotation — is a
smaller, genuinely independent rule choice and can ride along.)

**(2) Buy-vs-build is NOT closed — it is deferred on one cheap, unanswered empirical question.**
`output.py` now carries roughly a hundred-plus lines of hand-rolled CommonMark inline parsing, and
that hand-rolling **is the acknowledged root cause of adversarial passes 2–6, including the hang.**
The spike's KEEP-SCANNER recommendation rests on a perf regression measured at a large input size —
and the spike itself posed the gating question and **left it unanswered: is an option payload of that
size realistic at all?** These are synthesizer-emitted option bullets; if the realistic ceiling is far
below the measured point, **the perf objection evaporates and the recommendation flips to ADOPT.**
That is a one-afternoon question with a large architectural consequence, and it should be answered
before any more hand-rolled parser maintenance is authorized.
**Also still unexamined — the prior bundle's actual boundary question, which the spike did NOT
address:** *should the synthesizer be asked to emit structured options directly, so there is nothing
to parse?* The spike compared **two parsers**; it never tested **not parsing**. That third option
remains the only one that removes the defect class rather than relocating it, and it has never been
costed. Do not let "we ran a spike" read as "the boundary question was settled."

**(3) Contract-Version 1.1 — `[#34]` + `[#76]`, now untouched for TWO consecutive windows.**
Carried forward unchanged and slipping. Both change the delegation surface, so they version
**together**. `[#34]` = research-path verdict-package parity; `[#76]` = two-pass write so the
manifest is serialized only after the writes it describes have landed. **Settled and not to be
relitigated** (prior supplement ruling): a *compliance* fix forces no version bump, so do **not**
fold `[#77]`-class work into the 1.1 bundle.

**(4) `[#69]` inbox/CLI parity — the recurrence argument is stronger than previously stated.**
The two `LESSONS.md` write-ups name overlapping-but-different incident lists (they agree on two, and
diverge on the third), so the underlying duplication bug has **more distinct occurrences than either
entry alone claims**, and `[#69]` is the next one after those. **Neither entry records a structural
fix ever landing** — both end with the same unexecuted rule: *share a common processor, or add a
parity-check test.* `[#69]` is itself two defects: frontmatter `models:` is dead in the default path,
**and** the two entry points guard it on **different conditions**, so the same brief yields a
different panel via `--file` than via `--inbox`. **Decide the permanent answer — shared processor or
enforced parity test.** Patching `[#69]` alone guarantees a next instance.

**(5) Two stacked cost decisions on the crux-check, both unpriced.**
(a) `crux_check.providers` is currently a single-provider list and the step is **unconditional** —
widening it toward the general research provider set would put a very long deep-research call between
**every pair of rounds**. The JOURNAL flags this correctly as deserving **an ADR note, not a tuning
knob**: it is a per-run cost multiplier disguised as config. (b) `[#18]` cannot close without a
**billed live end-to-end witness**. Both need an operator call, and (a) should be recorded as a
decision before it is silently widened by someone tuning config.

**(6) Enforcement asymmetry with the hub — carried, with NEW evidence in BOTH directions.**
Still the genuinely cross-repo question the architect is uniquely positioned to rule on: `ai-council`
has independent read-only validators and **no consolidated gate**; the hub has a registry, a ship-gate
verdict, and a disposition register.
*New evidence for "gap":* a pre-push gate was bypassed; the spine condition behind it is systemic and
unruled (§1); and **six evidence files left the repo with no organ noticing** — no gate, anywhere,
observed the spike-evidence loss.
*New evidence for "correct-by-design":* the four validators pass cleanly and silently, and this repo
took `[#77]` through six adversarial passes to a defensible contract **without** a consolidated gate —
the adversarial-review loop, not a gate, is what actually caught the defects here.
**Rule on it; do not close it by defaulting to hub parity.**

**(7) Verification-as-code — the doctrine's first stress test, and it bent on the flank nobody
guarded.**
The doctrine held where it was pointed: `[#18]` merged with mock-only coverage and **stays open** for
want of a live witness — exactly right. But the spike is the counterexample: a **throwaway** branch
produced the empirical basis for two pending rulings, and that basis is now unreachable (§1) while its
conclusions circulate as prose. **The doctrine covers deliverables and does not cover spikes** — yet a
spike is precisely where evidence is most load-bearing and least durable. Decide whether
"verification-as-code" extends to throwaway work, and if so what the minimum durable residue of a
spike is (the measurement script, at least, promoted to `scripts/` before teardown). This is the
generalizable lesson of the window and it is currently unfiled.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per ADR-66. Every `#id` in this residual is an **ai-council** id. `[E1]` (invocation surface
  & delegation-readiness) carries the delegation-surface work §4 items (1)–(4) are about.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** — this is a cross-repo handoff and the
  hub is read-only-adjacent: it hosts the bundle, it is not the subject. Note that at least one
  merge subject on the target's spine carries a **hub-range `#id`**, so an `#id` seen in git is not
  automatically an ai-council ticket — P4/P10 must resolve each against `ai-council/BACKLOG.md`.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist there. P4 substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection,
  and **P10 is the judgment layer over it** (groom every open `#id` as live / dead / awaiting-ruling).
  This grooming is the operator-ruled boot obligation, not optional. **Caution for P4:** a bracketed
  `[#id]` in a merge subject does **not** imply closure here — this window deliberately merged
  `[#18]` *without* closing it, so a naive bracket-scan will report false closures.

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
> codes, group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass
> criterion is **"answered from the live source at check-time,"** never "matches a remembered number."
> Generation hints live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on hub branch `docs/ai-council-architect-handoff-0721`.
> That names only *which* branch hosts the bundle — **re-derive the TARGET's HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P12** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | `ai-council` |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py` / `ALL_CHECKS`, **no** `validate_git_backlog.py`, **no**
`validate_doc_claims.py`, **no** `ecosystem/doc-counts.md`, and **no**
`ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7/P9 rows would have FAILed
`anchor-missing` on every one. Each was re-bound to a **verified-live** `ai-council` surface (anchors
confirmed at generation time by running each command in the target). Where the hub has an organ
`ai-council` genuinely lacks, the probe says so rather than inventing an equivalent. **P11 and P12 are
new in this bundle** — they bind the two live findings that are §1's headline.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its header-normalisation hooks are
**formatters that rewrite files**, which would violate the read-only contract on a cross-repo target.
P7 calls the read-only validators directly instead. **P11 is diagnostic only — do not `git
cherry-pick`, `git branch`, or otherwise mutate the target to "rescue" the object; surfacing it is the
handoff's job, recovering it is the target session's call.**

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

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; this row restores the missing doc-vs-reality tooth by hand.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and does `ARCHITECTURE.md`'s **pre-commit roster** prose list that **same set** — or has the doc drifted behind the config? | `ARCHITECTURE.md` (pre-commit roster prose) ∩ the repo-root pre-commit config | the roster drifts every time a gate lands, and `ai-council` has **no automated doc-claim check** to catch the doc falling behind — so the mismatch is invisible until someone reads both; neither the count, the tail id, nor the verdict is in this bundle | `grep -n -i 'pre-commit' ARCHITECTURE.md` for the doc side; for the config side run a `grep -c` and a grep-tail over the `^  - id:` lines of the repo-root pre-commit config (path deliberately **un-backticked** — see the dotfile note below), then compare the two sets by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` appear in a merge subject on `main`'s first-parent spine, and for each: is that merge an actual **closure**, or a merge that deliberately did **not** close the ticket? | live git ∩ `BACKLOG.md` | the set is computed at answer-time by intersecting two live sources, and the closure/non-closure judgment cannot be read off either one alone | `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect by hand. **A bracketed id in a merge subject does NOT imply closure**: this window merged one ticket *without* closing it, and at least one hub-range id appears on the spine. Judge each, don't count them |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change — and this window added a large block of them; the integer appears nowhere in this bundle | `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **read-only** repo validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | **[RE-BOUND — the stock row bound to the hub bundle dir, unresolvable from the target root.]** How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; count, tail slug, and whether the index kept pace are all live-only and absent from this bundle | `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | **[RE-BOUND — `ai-council`'s `validate_backlog` prints NO serialize-groups line; its summary is counts-only.]** What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window filed several tickets; none are in this bundle | `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded | `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` (this subsumes P4's mechanical half — P10 is the judgment layer over it). **Expect a sizeable open set**; grooming it is the boot obligation, not optional |
| P11 | **[NEW — binds the §1 headline.]** The deleted spike branch's evidence artifacts (`spike/FINDINGS.md`, `spike/evidence.py`, and the implementation files beside them) are **not on any branch**. Locator: commit **`26192dd`**. **Does that object still exist, is it reachable from any ref, and what does its tree still contain?** If it exists — is recovering it, or deliberately discarding it, the ruling? | live git object store (dangling/unreachable objects) | **the answer changes irreversibly the moment `git gc` runs** — this is the one probe in the bundle whose window can close on its own. No summary can know whether collection has already happened; only the live object store can | `git cat-file -t 26192dd` (does it still exist?) then `git branch -a --contains 26192dd` (reachable from anything?) then `git ls-tree -r --name-only 26192dd \| grep spike` (what survives). **Diagnostic only — do not mutate the target to rescue it** |
| P12 | **[NEW — binds the §1 pre-push finding.]** How many **non-merge commits** sit on `main`'s **first-parent spine** right now (the population core-invariant #5 forbids and `block-ff-push` refuses), and what **kind** of commit dominates that population? | live git | the JOURNAL narrates this as a small, recent anomaly; the live population is the only way to see whether it is an anomaly or a standing practice — and the number is deliberately absent from this bundle | `git rev-list --first-parent --no-merges main \| wc -l` then inspect the recent ones' subjects (`git rev-list --first-parent --no-merges main \| head -20`, then `git log -1 --format='%h %cs %s'` per sha) to classify the dominant kind |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config filename is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked dotfile is looked up without its dot, resolves nowhere, and the probe is
> FAILed as a missing target even though the file plainly exists. **Consequence: no probe in any bundle
> — hub or cross-repo — can currently bind to a dotfile.** That is a hub tooling defect worth filing
> (dotfiles are exactly where config gates live); it is deliberately **not** patched from inside this
> handoff, because hub infra changes are exception-with-ruling (core-invariant #6). The probe's teeth
> are unaffected — the comparison is still live-only and answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and
   `scripts/validate_backlog.py` all exist in both). This is the single most likely failure mode of a
   cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d).** Then run P2–P12, each against
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
   open BACKLOG at boot.** First check which branch is live (P3), then re-derive every load-bearing
   fact from the live primary source.
6. **Run P11 EARLY — it is the only probe with an expiring window.** Every other probe's answer is
   recoverable at any later time; P11's ceases to exist when `git gc` collects the object. If P11
   reports the object gone, that is **not** a probe failure — it is a finding, and §1's item is then
   closed as *unrecoverable*, which is itself the answer the architect must rule against.
7. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row was re-bound — it
   pointed at the hub bundle dir, unresolvable from the target root). This bundle carries
   `HANDOFF_BOOT` + `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the §13(d) beat fires **FULL**
   unless the operator runs `supplement filled` first. Confirm by looking at the bundle directory in
   the hub — it is CC-side bookkeeping, not target state.
