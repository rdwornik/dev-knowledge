=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-20-dev-knowledge-architect-arc5` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-20-dev-knowledge-architect-arc5 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->_(fill: one-line session purpose — what the next session should achieve; ~3 sentences + a `BACKLOG.md` pointer, no re-narration)_<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-dev-knowledge-architect-arc5`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-20-dev-knowledge-architect-arc5 — the part the repo does not already encode

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
_(fill: which drift-flags are standing/dispositioned vs new-this-window, and why — by reference to `ecosystem/disposition-register.yaml` and the relevant `#id`s. State no verdict/count/[stale]/sha value; P7/P4 re-derive those.)_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
_(fill: terse shipped-this-window map — `#id`s + ADRs, one line each, pointing at `BACKLOG.md` / `JOURNAL.md`. Not a recap; the JOURNAL already encodes the detail.)_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
_(fill: the open design questions / next-frontier decisions the next session should resume — the un-committed "why." This is the residual's core payload; the generator cannot author it.)_
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
> **Branch note.** This bundle was generated on branch `docs/handoff-dev-knowledge-architect-arc5`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-20-dev-knowledge-architect-arc5/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-20-dev-knowledge-architect-arc5/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-20-dev-knowledge-architect-arc5/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

# SUPPLEMENT ANSWERS — authored by the outgoing browser architect (2026-07-19); CC transcribes VERBATIM

STRATEGIC INTENT — operator-dictated, one line: **AUDITS ARE OVER. ARC 5 IS EXECUTION.** The night audit (14 artifacts, sol-validated on all 8 domains, terra-corrected ×7) reduced the whole system to one meta-finding: **"decision recorded ≠ decision enforced ≠ decision legible."** ARC 5 closes that gap by BUILDING — no new audits, no new studies; every wave below lands mechanisms and visible file changes. Growth-side is proven sound (E1 fire-tests); all work is lifecycle-side. The operator's bar, verbatim in spirit: "I keep repeating the same pains for 10-20 chats — stop theorizing, execute."

OPERATOR PAIN → BUILD MAP (his named pains, each with its concrete build; this ordering IS the wave order):

**W1 — VISIBLE BOUNDARY (the "colors" — the operator's most-repeated ask).**
Build #329/#352: versioned `.vscode` background decoration (grey/navy, dark theme) of `owner=hub` / `owner=repo` regions, deployed fleet-wide as carrier material; PLUS a sweep completing RULING-S reader-visible universal-vs-repo section headers in every governed file across all three repos (CLAUDE.md + configs). Done-when: the operator opens any governed file in any repo and SEES which lines are methodology and which are repo-personal. P4a .vscode ruling shelf-life 2026-08-13 — this wave must land before it.

**W2 — STRUCTURE EQUALIZATION LEG 2 (the assets/ folder, mypy, "why do folders differ").**
Named forever-pain: `ai-council/assets/ruff-pre-commit.yaml` sits in an undeclared root `assets/` folder. Ruling R1 below disposes it. Plus: mypy/cache-handling posture per repo (declare or equalize — R1b), `hub-toc-hooks` resolution (S5 §4.2 — recommend path (b): hub manifest re-scope v1.3.2 matching the hub's own retirement, then prune ai-council + retire corp's waiver), #331 ratification + `parity-surfaces.yaml` consumer-tier rows for the BACKLOG story-map schema + gate (both consumers already adopted de facto — S5 gap 1), reconcile the corp-vs-ai `validate_backlog.py` fork (S5 gap 2: ai adopts corp's full plugin form via RULING-W leg, or a time-boxed declared divergence), corp `deployed-versions.yaml` currency (evidence for #276). All consumer writes via RULING-W worktree/branch → report; all changes land as manifest/template carrier material (replication-first).

**W3 — LIFECYCLE MECHANISMS (intake→ADR→backlog→close→DELETE — "the process problem").**
Seed 2 (sol-upgraded): `validate_intake.py` HARD pre-commit gate — closed status enum (+ ratified tech-extension per R4), unique `intake-id` (fixes the live id:14 triple collision), required `consumed-by` on CONSUMED, machine-readable `Intake:` provenance field on ADRs + citation enforcement (ADR-102/103 backfill or recorded non-intake-origin). Seed 3: build #242 (ADR header↔README status reconciliation; ADR-88/89 frozen-Proposed case). Seed 4: `gen_grooming_worksheet.py` + `audit.py` grooming-cadence/net-delta WARN (witnessed accretion 74→116 in 11 days, ~3.8/day — this makes it a standing signal); extend `safe_remove.py` M2/M3 as #347's sanctioned REAL-DELETION mechanism (R3). #269 build (count-tiered audit index per ADR-100).

**W4 — ARCHIVE LEGIBILITY (the operator's archiving ask — see R2, honest tension).**
The operator wants: when something is archived, its genre (intake/decision/audit) must be knowable from the name. Facts: file NAMES already encode genre+date by convention (ADR-NN-slug, date-class-slug audits, date-genre-slug intakes); the ruled convention is stay-in-place (join keys, ADR-101 seal) with status on index surfaces. R2 decides the shape; whichever way it goes, the build is this wave: either the index/status surfaces (seeds 2/3 + #269 + handoff-README micro-era clause) OR a physical `archive/` with a genre-preserving naming rule via ADR amendment. NOT both by default; no silent relitigating.

**W5 — SESSION/WRITE GUARDS (worktree pain, #353/#344/#349).**
sol's strongest contribution (R5): ONE unifying organ — a HEAD-bound operator-authorization token (names worktree + branch + allowed paths) checked by a PreToolUse guard — satisfies #344 Ask-2 (consumer hub-write guard), #353 (boot contract: refuse mid-session external orders without clean-tree-or-named-worktree), and the S7 prompt-attestation at once. Plus S6's boot-snapshot SessionStart hook, the `.claude/.session-lock` HEAD-movement advisory, #349 close-discipline boot echo, and sol's signed integration-return token for self-merge detection. Five recovered-not-prevented incidents justify this wave.

**W6 — CANON INOCULATION + PROMPT EQUILIBRIUM (PLAYBOOK/handoff currency, "ekwilibrium").**
Seed 1 (cheapest, highest leverage — may run FIRST in parallel as a doc lane): transcribe the four un-inoculated rulings (RULING-W · two-tier · worktree side-effect rule · consumer merge-delegation composite) into PLAYBOOK (operational) + ESSENTIALS (one-liner), grep-verified against the ADR amendments; build the staged-diff CO-CHANGE checker (NOT a `coherence-nudge` extension — terra) with explicit ADR-36/41/101→PLAYBOOK/ESSENTIALS edges. Seed 7: the 7-item inbound prompt-spec as a PLAYBOOK §2 amendment + handoff-time self-check probe (R6 decides hard-probe vs soft). Handoff-README micro-era documentation (stage1/stage2 archive class).

**W7 — TESTING + FLEET STATE (last, per dependency).**
Seed 9: dynamic-test evidence gate (code-impact tier in ship.md or versioned `test-harness.yaml`), WARN-first then FAIL after two demonstrated runs, depends-on #270; `protocols/AGENTIC_TESTING.md` as #348 config material. Seed 8 (sol-sharpened): a scheduled `fleet_collect` PULL collector with watermarks ("silence ≠ absence") subsuming the two reporters; SQL/SIEM stays SHELVED until a witnessed join-pain (matches the intake #14 ruling — confirm as standing answer, R7).

NEEDS-RULING (operator's bounded picks — recommendations attached; answerable one word each):
- **R1** `assets/` disposition: (a) DISSOLVE — relocate `ruff-pre-commit.yaml` content to the canonical config location, delete the folder (RULING-W leg + safe-deletion path), or (b) UNIVERSALIZE `assets/` as a fleet deployment convention. **Recommend (a)** — one file, no fleet role, and (b) would mint a new mandatory folder fleet-wide for no carrier need. R1b: mypy posture — declare ai-council's mypy as sanctioned divergence (recommend) vs roll out fleet-wide.
- **R2** archive shape: (a) INDEX-ARCHIVE — status/count-tiered index surfaces, files stay, names already carry genre (recommend — zero join-key breakage, builds already seeded), or (b) PHYSICAL `archive/` folders with genre-preserving rename rule via ADR-98/100/101 amendments. **Recommend (a).**
- **R3** #347 safe-deletion = `safe_remove.py` M2/M3 extension as THE sanctioned mechanism. **Recommend YES.**
- **R4** intake enum: ratify the 6 off-canon statuses as a documented tech-genre extension vs reclassify the docs. **Recommend ratify-with-documentation** (they are functioning plan-of-record artifacts).
- **R5** unifying HEAD-bound authorization token as ONE organ for #344/#353/attestation vs three separate builds. **Recommend ONE organ.**
- **R6** prompt-spec: hard handoff probe vs soft self-check. **Recommend hard probe on the bundle side** (the off-repo prompt itself can't be gated — attestation covers the paste).
- **R7** fleet-state: confirm "collector + reporters now, SQLite shelved" as standing. **Recommend confirm.**
- **R8** (carried, corp-side) #38 channel pick: 1 primary-direct / 2 worktree / 3 epic-dev.

BINDING (travel verbatim; do NOT relitigate): the ARC-4 rulings (RULING-W/S/PY/CF, two-tier "compliance IS authorization" in force now), the terra ×7 corrections as applied, sol's 4 mechanism upgrades as accepted strengthenings, satellite wave FROZEN until Wave-1 lessons extracted, luna's floor-misreport corrected (consumers DO carry the floor, hash-matched — Haiku fan-out is indicative, not authoritative), E1 scope honesty (only two organs fire-proved this run).

CONSIDERED + REJECTED: SQL/SIEM now (premature per intake #14 + S8); `coherence-nudge` extension for co-change (terra: not implementable); blanket new-path blocking (two-tier rule supersedes); physical file moves for archival as default (R2 decides, convention says stay-in-place); more audits (operator: enough).

DO-NOT-REDO: the nine seeds' adjudication (terra-corrected kill-candidates stand); the 8-domain gap derivation (sol-triangulated); the ARC-4 equalization values (py311/120/>=0.15.5/minversion 9.0 — at-parity, verified); the grooming closes #306/#307/#328.

OFF-REPO CONTEXT: the 14 audit artifacts live on branch `audit/2026-07-19-cycle-close` (worktree `night-audit-cycle-close`, base 6077c428) — MERGE IS THE FIRST MECHANICAL ACT of the next session (serial, --no-ff, operator GO) so the seeds become citable from main. The e5-registry bundle sits quarantined on `docs/corp-e5-registry-developer-handoff` (3b6b3f18) pending R8. Corp freshness debt cleared by corp's own session (verified genuine re-read). Operator frustration is itself context: visible results per wave (W1 first is deliberate — colors are the most visible), one wave = one merged arc, educate artifact per wave with file-level before→after.

DECOMPOSITION RATIONALE: waves are ordered by operator pain-priority, not dependency elegance; W6 seed-1 doc lane may run parallel from day one (file-disjoint from W1/W2). Every wave: frozen acceptance contract before delegation, Codex terra pre-merge, RULING-W for any consumer write, replication material over one-off fixes, educate with before→after. The successor's first three moves: (1) merge the audit branch, (2) collect R1–R8 rulings (single bounded-pick message to the operator), (3) open W1.

---



**CC-OBSERVED ADDENDUM (not operator-authored — generation-time state correction).**

The OFF-REPO CONTEXT above names merging `audit/2026-07-19-cycle-close` as "the FIRST MECHANICAL ACT of the next session", and the closing line lists it as successor move (1). **That merge has already landed** — completed 2026-07-19 at `9292d38a` (*Merge audit/2026-07-19-cycle-close — night-audit cycle-close artifacts (9 streams + E1 + luna + consolidated + sol/terra) + JOURNAL anchor*, 16 files / +1620). The `audit/2026-07-19-cycle-close` branch no longer exists and the `night-audit-cycle-close` worktree is torn down (no orphan dirs). Two commits landed on top since: `8aed1e62` (corp-E5 registry-developer bundle) and `e0421a13` (JOURNAL branch-consolidation anchor).

**Consequence for the successor:** the 14 audit artifacts ARE citable from `main` now — the purpose that step served is satisfied. The successor's first three moves therefore begin at **(2) collect the R1–R8 rulings** (single bounded-pick message to the operator), then **(3) open W1**. Everything else in the ANSWERS above stands unchanged.

**W5 evidence (new, witnessed this session).** During this handoff generation a concurrent session transiently checked out `worktree-monorepo-handoff` in the PRIMARY working tree, moving HEAD off this branch mid-command (reflog `HEAD@{0}: checkout: moving from docs/handoff-dev-knowledge-architect-arc5 to worktree-monorepo-handoff`); a running heredoc failed as its target directory was swapped out, and a subsequent regeneration wrote a COLD bundle into the other session's tree (caught and removed before contamination). No guard fired. This is a **sixth** recovered-not-prevented incident for the W5 justification pile, and unlike the prior five it carries a clean reflog trace — direct evidence for the `.claude/.session-lock` HEAD-movement advisory and the `#353` boot contract.
