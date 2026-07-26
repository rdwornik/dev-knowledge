=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-26-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-26-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Rule the two ARC-5 rows that block everything downstream, then decide whether the arc's own closure contract survives contact with reality.** `R8` (the corp-side `#38` channel pick) and `R12` (narrow the target vs gate the growth, at N_silent 176) are the two rows the last sweep could not close — `R8` because it is explicitly the operator's own pick, `R12` because no recommendation is attached to delegate to. Beyond those, this window surfaced a cluster of **structural** questions rather than bugs: the 1200-char backlog ceiling now demonstrably prevents records from existing, a gate and a test can disagree permanently about the same condition, a cross-repo gate reads live sibling trees, and a BINDING ruling was relitigated because it lived on a surface nobody searches. Start from **`BACKLOG.md`** — `[E8]` (the ARC-5 wave map, decision table, and frozen closure contract) and `[E9]` (the Fleet Desired-State North Star) are the two themes in play; `RESIDUAL.md` §4 carries the decision context so you resume the design instead of rediscovering it.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-26-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-26-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Read this section as a map of WHICH flags exist and WHY. Every value — verdict, WARN count,
`[stale]` status, drifted id, sha — is withheld by construction; P4/P6/P7/P9 are the answer.**

**Standing (dispositioned before this window, unchanged by it).** Four classes in
`ecosystem/disposition-register.yaml`, none of them new information for the next session:
`no_ff_merges` (legacy pre-invariant commits on main's first-parent spine — history, never to be
rewritten); `undeclared_edges` (the handoff-process references from `BACKLOG.md` / `VISION.md` /
`AI_COUNCIL_PROCESS.md` / `ESSENTIALS.md` / `PLAYBOOK.md` / `SESSION_SETUP.md` — declared-and-parked,
not drift); `doc_rot` on `BACKLOG#278` / `#332` / `#344` (the **accretion** class); and
`reconciled_versions` on `templates/CONTRIBUTING-md-template.md` (a check-precision bug against a
placeholder, not real drift).

**New this window — three entries, and TWO of them are architecturally interesting, not routine.**

1. **`doc_rot` on `BACKLOG#421` + `#422` — filed under a DISTINCT reason class: *oversized single
   filing, explicitly NOT accretion.*** One session, one day, one filing each; the length is precise
   mechanism description, not accumulated dated history. Trim was refused by operator ruling
   (2026-07-26) and other sessions' task text is not rewritten (the A0-seal precedent). **The register
   entries themselves say the fix is the format, not the wording** — they point at intake #17. Treat
   these two rows as evidence in the restructure argument (§4), not as a cleanup chore.
2. **`fleet_parity` on ai-council's root `conftest.py` — an EXTERNAL, IN-FLIGHT condition with no
   action available inside this repo.** A sibling repo's merge turned this repo's gate red mid-close.
   Both candidate fixes (a per-repo manifest declaration in ai-council vs an amendment to the hub's
   consumer-role root template) are real and **neither was chosen by inference** — filed as `[#430]`,
   which carries both halves. This row should clear itself once `[#430]` rules, at which point it
   decorates stale; that is the intended lifecycle, not rot.

**A predicate defect recorded in the register as a comment rather than a seventh ticket.**
`validate_doc_rot`'s backlog accretion predicate counts date **occurrences**, not **distinct days**,
and counts dates appearing inside **path-like tokens** — so a single-day filing that cites a dated
`docs/handoffs/…` path registers as multiple "dated blocks" and trips the ACCRETION leg although
nothing accreted. Both rows above would still WARN on the gross-chars leg, which is the honest
signal. Deliberately left unticketed (six were filed that session and none closed); it is a candidate
fix for whoever re-reviews at the shelf-life date.

**One condition that is NOT a disposition and NOT a gate — do not conflate them.** A single named
test (`tests/test_audit.py::test_check_fleet_parity_green_on_live_repo`) is red on **proven external
provenance** — it calls the check directly and asserts on the raw finding, so the disposition that
legitimately clears the same WARN at the ship-gate is invisible to it. `main` was pushed red by
explicit operator ruling, on evidence, and the record of that exception is deliberate: JOURNAL
2026-07-26 (d) exists so the exception is never mistaken for an oversight. **The gate-vs-test
divergence is itself the finding** — see §4. Re-run to learn whether the sibling has since declared
it; the bundle asserts nothing about its current state.

**Two surfacers are shouting and neither is a drift-check.** The session-start hooks report a
standing pool of unreviewed **closure proposals** (`/review-closures`) and a set of unreviewed
**nightly triage findings** in the Issues tab; the changelog sentinel reports the tool has moved
several patch versions past the last review (`/changelog-review`). None of these gate anything.
That is precisely why they have accumulated — and §4 treats the pattern, not the queue.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the previous architect bundle merged (`docs/handoffs/2026-07-25-dev-knowledge-architect/`).
Detail lives in `JOURNAL.md` 2026-07-26 entries (a)–(e) and `BACKLOG.md`; this is the map only.

- **ADR-105 accepted** — Routine consumer declaration: a six-field row shape, **gated at ACTIVATION,
  not at filing**. Landed with the `[E9]` brake discharged and `[#419]` given teeth.
- **Hygiene + currency (the last merge)** — `ARCHITECTURE.md` brought current through ADR-105; the
  organ map gained a **Status** column (ARMED / RULED-UNBUILT / RETIRED); Ch6's nightly loop marked
  **broken at the triage edge**; the `[#373]`–`[#380]` reserved-id banner released; three merged
  branches deleted.
- **A stranded branch recovered** — intake **#17**
  (`docs/intake/2026-07-25-tech-consolidation-decision.md`, ACCEPTED, three open questions) plus
  `[#421]` and `[#422]`, which had been misfiled onto another session's branch and never reached
  `main`. See JOURNAL (c).
- **Filed, not closed:** `[#423]`, `[#427]`, `[#428]`, `[#429]`, `[#430]`, `[#431]` — plus the two
  recovered above. **Closures this window: none.** That direction is a standing input to §4.
- **`[E8]` decision table dispositioned against live state** — outcome: one DEAD-OBE, three
  already-ruled, four ruled by operator-delegated adoption, **two still open (`R8`, `R12`)**. A ruling
  there is *recorded, never executed* — each adopted row still needs its build.
- **Two review lanes both bit** — the doc lane and the adversarial lane each returned High findings on
  work that had already passed the other, including a **relitigated BINDING ruling**. See §4.
- **The `[E8]` preamble now carries an explicit reconciliation-debt list** (stale `CONTRIBUTING.md`
  prose describing a deleted Action in the present tense; `[#389]`/W3/W4/W6/W7 R-status text now
  stale) — enumerated rather than silently left.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### A. The two rulings the operator owns — nothing downstream moves without them

**`R8` — the corp-side `#38` channel pick** (1 primary-direct / 2 worktree / 3 epic-dev). Four
exhaustive searches across BACKLOG / JOURNAL / `docs/` found **no ruling**. It was **explicitly
excluded** from the 2026-07-26 delegation order — the operator's own pick. Do not re-search for it and
do not infer it; ask.

**`R12` — the ARC-5 closure contract is not satisfiable as written, and this is the largest open
architecture question in the repo.** Clause (b) requires that *"everything still unenforced has moved
to declared-unenforced with an owner and a review date."* At **N_silent = 176** that means
dispositioning 176 rules — not achievable in one arc. Two options are on the table: **(i) NARROW** the
target to a bounded load-bearing slice (the four census escalations `[#358]`–`[#361]`, the two
still-silent seed-1 rules `[#356]`, the 49 dropped `#242` guards `[#362]`), or **(ii) GATE THE GROWTH**
of silent rules instead of draining the pool. **No recommendation is attached, deliberately** — there
is nothing to rule by delegation, and narrow-vs-gate is a genuine choice with different downstream
shapes.

> **A third framing the record does not yet contain, offered as an option and not as a
> recommendation:** amend the closure contract itself. It is currently marked *frozen — reproduced
> verbatim*, so amending it is a real decision with its own cost (it is the artifact that stops "waves
> merged, ship-gate green" from counting as closure). Narrowing the target and amending the contract
> are **not** the same move, and the record currently conflates them.

### B. Structural questions this window surfaced — each is a design call, not a bug fix

**B1 — The 1200-char `doc_rot` ceiling stopped being a constraint and became a censor.** The evidence
crossed a threshold this window: three findings **could not be recorded in their own tickets at all**
and were relocated to `LESSONS.md`, and **all three references are one-directional** — the lessons cite
the tickets; the tickets cannot cite back. A ticket that cannot hold the evidence for its own defect is
not a formatting inconvenience. Two register entries now say in their own text that **the fix is the
format, not the wording**. The decision is *what a backlog task record is* — not *what the limit
should be*; intake #17 (`docs/intake/2026-07-25-tech-consolidation-decision.md`, ACCEPTED) is the
vehicle. Its three open questions — **R-G** (which Gemini CLI is the scanning lane), **R-N** (confirm
8 days as the overdue-ruling threshold), **R-S** (confirm the seeded-defect list for the acceptance
test) — are unanswered and cheap to close.

**B2 — A gate and a test can disagree about the same condition, and the divergence is structural.**
The disposition register is a **ship-gate** concept; a test that calls a check directly and asserts on
raw findings cannot see it. So a legitimately-dispositioned WARN stays green at the gate and red in
pytest, forever, by construction. Three shapes are available and none has been chosen: make
direct-check tests disposition-aware; rule that such tests must assert only on *undispositioned*
findings; or accept and document the divergence as a declared property. Until one is picked, every
future disposition can mint a permanently-red test.

**B3 — Should a gate's verdict be allowed to depend on state outside its subject?** `fleet_parity`
reads **live sibling-repo working trees**, so another repo's merge can turn this repo's gate red with
**no action available here** — which is exactly what happened. `[#430]` carries the two local fixes
(declare it in the sibling's manifest vs amend the hub's consumer-role root template) and neither was
chosen by inference. The larger question sits above both: a cross-repo gate that reads *live* trees is
non-deterministic by design; reading **declared/committed** state instead would make it reproducible.
That is an architecture ruling, not a ticket.

**B4 — The ruling corpus has no single searchable home, and that already cost us.** A probe searched
`JOURNAL` / `LESSONS` / `docs/decisions/` and concluded *"no prior ruling exists"* — then the
adversarial lane found the ruling in a **handoff supplement**, marked *"BINDING — do not relitigate."*
A settled decision was relitigated because the surface it lived on was not in the search set. Either
binding rulings get a canonical home (and handoff bundles stop being load-bearing for them), or the
"where do I look" contract has to enumerate `docs/handoffs/` explicitly. **This is a live defect in how
decisions are found, not a process nicety.**

**B5 — An attached recommendation is a poor predictor of the operator's call.** Of the `[E8]` rows that
turned out to already have a ruling, **the attached recommendation lost 3 times out of 3** (R1b
rejected, R2 chose (b) over (a), R4 rejected outright). The methodological consequence is direct:
verify each row against live state, never ratify a table wholesale — and treat a recommendation as a
hypothesis, not a default. Worth codifying rather than leaving as a one-session observation.

**B6 — Detection is healthy; consumption is not.** Filings this window: eight. Closures: **zero**. A
standing pool of closure proposals sits unreviewed, the nightly triage findings sit unconsumed (Ch6 is
now explicitly marked **broken at the triage edge**), and the changelog sentinel has been nagging
across several tool versions. Every one of these surfacers is **non-gating** — which is why they
accumulate. Closure-contract clause (d) requires accretion **net ≤ 0**; the current direction is the
opposite. The question is not "run the queues" but **whether a surfacer with no consumer should exist
at all**, and what makes consumption obligatory without turning every nag into a blocker.

**B7 — A repo cannot fix the defects that live in its own tooling.** `[#431]` (the codex-review wrapper
silently drops the doc lane on mixed diffs) sits behind a **core-invariant #6 global-infra ruling** —
so the repo that suffers the defect is not permitted to repair it unilaterally. That guard is correct
and it is also a bottleneck. Worth deciding whether a narrow standing grant exists for
defect-repair-in-place, or whether every such fix waits on a per-instance ruling.

### C. Small open calls — cheap, and each is genuinely the operator's

- **`ecosystem/registry.md` is missing a `terminal-setup` row** (human-registered 8, should be 9). It
  needs a purpose line and a verified status — not derivable. **Note the correction the last session
  had to make:** `index.yaml` is **derived and regenerated wholesale** (`audit.py` says do not hand-edit
  it), so the originally-asserted "`index.yaml` registration gap" was the wrong target; the
  hand-maintained `registry.md` is the real one.
- **Reconciliation debt, enumerated in the `[E8]` preamble rather than silently left:**
  `CONTRIBUTING.md` still describes a deleted Action in the **present tense**; the R-status text on
  `[#389]` / W3 / W4 / W6 / W7 is now stale.

### D. Dated pressure — the only genuinely time-boxed things here

- **W1's `.vscode` ruling shelf-life: 2026-08-13.** W1 is SEEDLESS — justified by operator priority and
  this deadline, *not* by audit evidence. It is the most visible wave, deliberately.
- **Disposition `review_date`s cluster at 2026-08-26** (the `#421`/`#422`/`fleet_parity` rows). Those
  are shelf-lives, not deadlines — they exist so suppressions cannot rot into paper.
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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-26-architect`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-26-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-26-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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
