=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-26-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. Every probe runs in the **target** root — see the run-in-root table at the top of `PROBES.md`. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-26-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**A great deal landed, and all three mission axes moved zero. Break that pattern, then rule the class of defect that made the green lights untrustworthy.** Everything shipped this window was record and quality-control scaffolding — worth having, but the standing axes (CLI parity, now in its **seventh** un-run window; the boost/protocol Contract-Version arc; non-cognitive debate) are exactly where they were. Two of the three are gated on **decisions, not work** — an operator sit-down and an ADR-11 interactivity ruling that resolves its dependent in **either** direction. Meanwhile the window surfaced one recurring defect **five times**, twice inside the checker built to catch it: **a green published without the predicate that produced it** — a rule reporting pass while reading a fraction of the surfaces it claims (**P11**), and validators whose exit zero is silence rather than a verdict (**P7**). The instance repairs are filed; **whether that class gets a durable home is the open design question**. Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; read the grooming log's 2026-07-26 entries before re-deciding anything. **The supplement is EMPTY — run the §13(d) operator-context beat in FULL before accepting the residual's ordering.**<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-26-ai-council`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-26-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **CROSS-REPO (ADR-36/41).** The subject is **`ai-council`**; the bundle is hosted in the
> `.dev-knowledge` hub. Every `#id`, path, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The hub is read-only-adjacent here: it hosts, it does not own these tickets.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.
>
> **Consequence, stated plainly:** this residual is **repo-derived by construction** and therefore
> carries **no operator intent** — not the priority call, not the "why now," not anything decided in
> chat and never written down. Last window's bundle carried a filled supplement whose ANSWERS
> **corrected the residual on five load-bearing points**, including inverted sequencing and a ruling
> that existed only in chat. Assume the same gap exists now and is simply unfilled. **Run the §13(d)
> beat in full before acting on §4's ordering** — §4 is CC's best repo-derived reading, not the
> operator's plan.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

**Cross-repo re-frame.** `ai-council` carries **no** `audit.py` ship-gate, **no**
`validate_doc_claims`, **no** `validate_git_backlog`, and **no** disposition register — so there is no
single GREEN/RED headline verdict to report and no dispositioned-WARN concept at all. The drift
surface here is: the **four gating read-only validators** (P7) + `validate_backlog` (P9) + the
report-only **claim-vs-reality checker** (P11/P12), plus **hand intersection** where no organ exists
(P2, P4, P8, P14). **Re-derive each at read-time — the teeth are in `PROBES.md`, not in trusting these
lines.** This bundle states **no** exit code, count, verdict, drifted `#id`, or sha.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**THE HEADLINE IS NOT A DRIFT-FLAG — IT IS THE OPPOSITE, AND THAT IS THE PROBLEM.**

Read this before the backlog, because the backlog cannot show it. A reader arriving at this repo will
find a large batch of closed tickets, a claim-checker reporting cleanly, gates exiting zero, and a
clean tree — and could reasonably conclude the window went to plan. **It did not.** Everything that
landed is **record and quality-control scaffolding**. **All three standing mission axes moved zero.**
That gap is the single most important fact about this window, and a backlog structurally cannot
express it: a backlog shows what closed, never what should have.

**The drift that matters this window is drift the instruments could not see** — five separate
instances of one class:

- **`#125` (NEW, and the sharpest).** The claim-checker's rule 4 is specified as set-equality across
  **four** doc surfaces; its implementation reads **fewer** (P11 re-derives exactly how many and
  which). A genuinely stale canonical surface sat under a clean report for the entire window. **The
  report did not move before or after the repair** — the surface was fixed by hand, and nothing
  automated ever noticed. A defective gate under a green light is *worse* than no gate, because it
  converts "unchecked" into "checked and fine." **The ticket states explicitly that the SPEC must not
  be narrowed to match the code** — the four-surface claim is the requirement; the code is what is
  wrong.
- **`#126` (NEW, sibling).** Several armed validators emit **no output at all**, so their exit zero is
  **silence, not a verdict** (P7 deliberately asks for the stdout-vs-exit-code split for this reason).
- **`#124` (NEW, and it BLOCKS `#123` — recorded in both tickets).** A clean-room install of the
  declared dependency ranges does **not** reproduce a green gate; the primary's gate passes only
  because its interpreter happens to hold versions nothing in the repo pins. `#123` repoints the gate
  at a fresh environment, so **`#123` executed first breaks the green gate on the day it lands, and
  the breakage presents as its own regression.** The order is a correctness constraint, not a
  preference.
- **`#121` (evidence upgraded, not resolved).** A config sweep narrowed three candidate explanations
  for an unattributed checkout to **one with demonstrated write access** — which narrows the
  hypothesis but **does not prove the event**. Recorded as narrowing, deliberately not as a finding.

All four are the same shape, named in `LESSONS.md` 2026-07-26: **a green published without the
predicate that produced it.** Twice it occurred *inside the checker built to catch exactly that*.

**STANDING (not new, and none of them are drift — they are un-started work):** the three mission axes
in §4 items 1–3. They carry no flag because nothing is inconsistent; they simply have not moved.

**Mechanically clean, and that is a real result, not a caveat:** the checker reached its clean state
**with no suppression** — no path allowlisted, no rule silenced; every clean result earned by
repairing the thing or adjudicating it in prose. **P12 re-derives what that clean line actually
covers** — the skipped/total split is the real denominator, and the summary line alone does not
disclose it.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Detail lives in `JOURNAL.md` entries **2026-07-26 (1)–(7)** — entry **(7)** is the window-close and the
best single read. This is the map only.

- **`#97` claim-checker** — driven to a clean report **without suppression**; the **rule-2 resolution
  model** and **ADR-15** (commit tree, declared bases, self-validating declarations) landed with it.
  Held set corrected in both directions (it had omitted one rule and wrongly held another; **arithmetic
  caught it, no gate did**) — the set-partition now sums.
- **`RepoContext` harness fix** — determinism moved from one rule to **every** leg, including the stubs.
- **`#112` closed** — four dangling commits made reachable via pushed `archive/cited-*` tags,
  replacing an **uncommitted local config value** with real refs (**P15** verifies the replacement
  actually holds).
- **Renumber arc closed** — the two carried hub-id tasks landed in the local id space; every live
  dangling `refs` hub-qualified; one previously-fenced id **freed**. A **third** hub/local collision
  was caught and a different id is now fenced (**P13** — re-derive; the remembered set is wrong).
- **`#106`, `#108`, `#111` closed**; **`#83` discharged** — via its *"or its findings are filed"*
  clause, **not** because the surface came back clean.
- **F2 ruling batch** — nine rulings and four forks converted from chat into repo records; the
  **Unit-2 stubs HELD by architect ruling** (registered, not deleted, so every run keeps printing them
  as not-checked — that is the whole reason registration was insisted on over deletion).
- **`conftest` wrong-tree guard** — RED-proven in a worktree before being trusted.
- **Eleven tickets filed** (`#114`–`#126`); **ARCHITECTURE** reconciled to ADR-15 and re-stamped.
- **Fleet-methodology intake commissioned to the hub `.dev-knowledge`** — this window's fleet-level
  defects assembled into ten commissions (A–J). **The hub owns those rulings; `ai-council` supplies
  evidence.** Do not re-decide them here.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
> **Ordering is stated so it is not re-derived — and it is the outgoing session's explicit ruling, not
> CC's invention.** **Hygiene does not preempt items 1–3.** Record repair, checker work and teardown
> are the **background lane**. They are how this window filled, and that is the mistake not to repeat.
> **This ordering is repo-derived and the supplement is empty — the §13(d) beat may correct it.**

**1. Owner-gated — neither is CC's to decide, both have been waiting.**
   - **`#27` CLI parity — not run for the SEVENTH window.** The instrument is ready and was verified
     untouched this window. **Nothing blocks it but the decision to sit down with it.** It shares no
     surface with anything else here, so it is never legitimately "behind" other work — if it slips
     again it should be because it was ruled out, not because it was sequenced out.
   - **The `#117` ADR-11 decision-1 interactivity ruling.** `#117` gave the ruling an *owner*, which is
     not the same as making it. ADR-11's amendment still defers interactivity as *"a separable rider
     requiring its own ADR"*, so **`#113` is unresolvable until someone rules** — and **either
     direction resolves it**. This is a cheap unblock being treated as an expensive one.

**2. Architect-owed — `#103`.** Browser-architect design work, **not CC's to build**; dated
   not-started. Non-cognitive debate (`#55`) is untouched; this is the **sixth window on paper** for
   that axis.

**3. Build lane — the Contract-Version 1.1 arc: `#34` + `#76` + `#100`, versioned TOGETHER, never
   alone.** Untouched this window. The togetherness is the design constraint — the version is the unit,
   and splitting it is what the grouping exists to prevent.

**4. Behind them, in this order** (the order within this item is load-bearing at one point):
   **`#124` → `#123`** — **serial, and a correctness constraint**: `#123` first breaks the green gate
   on the day it lands and the breakage presents as its own regression. Then **`#105`**, then
   **`#119`/`#120`**, then **unit (b) + `#125` + `#118`**.

### The open design questions — resume these, do not rediscover them

- **What is the durable answer to the "green without its predicate" class?** It has now appeared
  **five times in one window**, twice inside the checker built to find it. `#125` and `#126` repair two
  *instances*. **Whether the class gets a durable home — a rule, a report-format contract, a review
  step — is unruled.** This is the highest-leverage open question in the repo, and it is a design
  question, not a build ticket.
- **What is a validator's reporting contract?** `#126` says exit-zero-with-no-output is silence, not a
  verdict. That is a **fleet-shaped** question (it is in the hub commission set) but `ai-council` is
  where it bites. Is the answer a local convention, or does the repo wait on the hub ruling? **Waiting
  is a legitimate answer — but it should be a decision, not a default.**
- **The held Unit-2 stubs: what actually un-holds one?** The ruling is *"revisit when a drift a held
  rule would have caught actually bites, then build that one rule, earned by the incident."* The
  trigger is deliberately incident-driven — **so nothing schedules them, and nothing is supposed to.**
  Confirm that is still intended rather than quietly re-planning them.
- **Rule 4's spec-vs-code direction is already ruled** — the spec stands, the code is wrong. **Do not
  relitigate this into "narrow the spec to match."** It is recorded in the ticket precisely because it
  is the tempting wrong fix.
- **`#121` — an unattributed checkout with one demonstrated-write-access candidate.** Narrowed, not
  proven. Open question: is further pursuit worth it, or is the honest disposition to record the
  narrowing and stop? **Do not conflate it with the separate rejected-tool-call-that-had-already-
  executed finding** — that one is fully attributable from the reflog and is a *different* failure
  shape. Conflating them sends the next session hunting a phantom concurrent writer; the outgoing
  session flagged this explicitly.

### The meta-finding, stated plainly because it is the thing most likely to repeat

**The tooling got better at telling the truth about itself, and the mission did not advance.** Those
are not in tension — the first was necessary. But a window of pure scaffolding is still a window, and
this is the **seventh** for `#27`. The failure mode to guard against is not laziness; it is that
hygiene work is legible, satisfying, and always available, while the mission axes are gated on
decisions that are easy to defer. **If this window's pattern repeats, the ordering above was
decorative.**
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council/BACKLOG.md`**
(themes `[E1]`–`[E7]`, stories `[S…]`), the live in-progress branches (`git branch -v` in the target),
and the drift set re-derived by **P4** / groomed by **P10**. Re-narrating item text splits the truth
and drifts — the pointer + the drift-flag is the whole task-state.

**Read the `BACKLOG.md` grooming log's 2026-07-26 entries before re-deciding anything** — this
window's rulings landed there, including the held-stubs ruling, the `#124`→`#123` blocking direction,
and the next-session queue recorded as a **note** rather than a section.

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
> exit codes, set-memberships, or orienting lines are stated. That withholding IS the teeth. The pass
> criterion is **"answered from the live source at check-time,"** never "matches a remembered number."
> Generation hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never
> here. The validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an answer hint.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-26-ai-council` **in the
> hub**. That names only which hub branch hosted generation — **re-derive the TARGET's HEAD / tree /
> branch / ahead-behind live (P3); do not trust this line.**

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P16** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | ai-council |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set is hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below was confirmed present at generation time by running its command in the target). Where the
hub has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**What changed since the last cross-repo bundle — three probes were retired or re-pointed because the
thing they measured was RESOLVED this window.** Do not carry the previous bundle's framing:

- **The registry-completeness gap is closed.** Last bundle's P11 asked which of the fourteen specified
  rules had no row in the checker's registry. All fourteen are now registered (implemented, held-stub,
  or structural). **P11 is re-bound** to the defect that replaced it: rule 4's *implementation* reads
  fewer doc surfaces than its spec claims.
- **The `gc.auto` probe is retired.** Last bundle's P15 bound to an **uncommitted local config value**
  holding unreachable objects alive. That mechanism was **replaced by real refs** this window. **P15 is
  re-bound** to those refs — whose whole point is that they are now verifiable from a clone.
- **The id-reservation fence moved.** Two reservations were **discharged** and a different id is now
  fenced. **P13 re-derives the live set** rather than the remembered one.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead. `scripts/check.ps1`
is likewise **not** a probe — it is the full pytest+mypy+ruff trio, far past read-only-cheap; P6 and
P12 call the two pieces a probe actually needs.

> **`SUPPLEMENT.md` is generated EMPTY.** Unless the operator fills it before this bundle is pasted,
> the assembler folds nothing and the incoming §13(d) operator-context beat fires **FULL** — a full
> off-repo ask, not the narrowed *"anything changed since?"*. The residual is therefore the **only**
> carried "why" this window, and it is repo-derived by construction: it cannot carry operator intent.
> **The probes outrank it on every number.**

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
by CC, substring-matched. `ARCHITECTURE.md` was amended **again** this window (a governance-roster
reconciliation), so the live lines, not any remembered ones, are the frame. **Then, before design, the
operator-context beat fires (§13d) — FULL** (the supplement is generated empty; there is nothing to
narrow against).

**P7, P11 and P12 are unusually load-bearing this window.** The residual's headline is that a *green
report was published without the predicate that produced it* — several separate instances, including
inside the checker built to catch exactly that class. P7 measures whether silent exit codes are being
read as verdicts; P11 measures whether one rule's implementation still covers fewer surfaces than its
spec; P12 measures what the clean summary line actually covers. **Run all three before accepting any
claim in the residual that the quality surface is sound.**

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; the claim-checker does not cover this claim either.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and do **both** doc rosters — `ARCHITECTURE.md`'s prose roster **and** `CLAUDE.md` §9's — list that **same set**, including the total each states? | the pre-commit config ∩ `ARCHITECTURE.md` (hook-roster prose) ∩ `CLAUDE.md` §9 | the roster drifts every time a gate lands, and **two** doc surfaces must both stay reconciled — the checker's rule 3 covers *mention*, not set-equality or the stated total, so a divergence stays invisible until someone reads all three | **TARGET:** `grep -n 'hook' ARCHITECTURE.md` and `grep -n 'id:' CLAUDE.md` for the doc side; for the config side run grep -c and grep -n on the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the three by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it, and this window closed with a rapid series of merge-and-push arcs whose live position is exactly the question | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch -v` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle. This window both **closed** and **filed** double-digit id batches, so the intersection has genuinely moved in both directions | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — and ARCHITECTURE took another merge of edits this window (the governing-ADR roster reconciliation), so the relation is among the freshest facts in the repo | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change, and this window landed new harness tests; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict. THIS window filed a ticket asserting these gates report silence rather than a verdict — so read the codes, and read what each one actually printed.]** Run the four **gating** read-only validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero, and how many produced **no stdout at all**? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. The residual's central claim is that a silent exit 0 was being read as a positive verdict when it is only an absence of output — so the **stdout-vs-exit-code split is itself part of the answer**, not incidental | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each) **and note separately whether it printed anything**. Re-derive; do **not** trust the residual's prose |
| P8 | How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and do **both** `docs/decisions/README.md` **and** `ARCHITECTURE.md`'s governing-ADR roster list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` ∩ `ARCHITECTURE.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce. **The three-surface form is deliberate:** a newly-landed ADR reached some of these surfaces but not all of them this window, and the checker did not see it (that is P11's defect). The count, the tail slug, and whether **each** index has kept pace are live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` then `grep -n 'ADR-01\|Governing' ARCHITECTURE.md` — compare all three by hand |
| P9 | What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings** — and what does `BACKLOG.md`'s grooming log name as the **next free local id**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window moved every one of them (a double-digit filing batch plus closures plus a renumber landed); the next-free pointer moved too; none of it is in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) then `grep -n 'Next free local id' BACKLOG.md \| tail -1` |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **The open set moved substantially in both directions this window** (a filing batch plus a closure batch), so the grooming denominator itself has moved — and several new items are explicitly blocked on each other | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[RE-BOUND — last window's registry-completeness gap is CLOSED; this is the defect that replaced it, and it is the window's headline.]** Rule 4 is specified as **set-equality across four doc surfaces**. How many surfaces does the implementation's `_adr_roster_docs` actually return, **which** ones, and is the comparison **one-directional or both**? Then: does the checker's own report or its KNOWN-LIMITATIONS output **disclose** that narrowing anywhere? | `scripts/validate_claims.py` (`_adr_roster_docs` and its caller) ∩ the rule-4 spec line for ticket #97 in `BACKLOG.md` ∩ the checker's report header | the spec count is a live doc fact, the returned tuple is a live code fact, and **the gap between them is the defect** — one that a clean summary line actively conceals, because the rule reports *pass* while reading a fraction of what it claims. This is the "green without its predicate" class turned on the checker itself; a summary that read "rule 4 passes" never asked *passes against what* | **TARGET:** `grep -n '_adr_roster_docs' scripts/validate_claims.py` then read that function and its call site in full, then `grep -n 'KNOWN LIMITATIONS' scripts/validate_claims.py` and read the block it heads, then `grep -n '\[#97\]\|\[#125\]' BACKLOG.md` — compute the surface-set difference by hand |
| P12 | **[The checker's live coverage picture — and the reason its clean summary line must not be read alone.]** Run the report-only checker: what does the final `SUMMARY:` line report for **findings**, **rules covered**, **anchor-missing**, **skipped**, and **errors** — and what does the coverage block report as **implemented vs stubbed vs total**? How many rules are **held stubs** (registered but deliberately unbuilt), and does a reader of the summary line **alone** learn that? | `scripts/validate_claims.py` run over the live tree | the finding count moves on **every JOURNAL prepend**, and the skipped/total split is the whole question: a low finding count across a small covered set is not the same claim as a low count across the full set, and only the coverage block distinguishes them. **Held stubs are registered precisely so the report keeps saying "not checked"** — verifying that it still does is the point. None of these integers are in this bundle | **TARGET:** `python scripts/validate_claims.py` — read the final `SUMMARY:` line, the coverage block, **and** the per-rule SKIP lines above it. **Report-only and non-blocking by design — a non-zero finding count is NOT a failure**, it is the measurement |
| P13 | **[RE-BOUND — the reservation fence MOVED this window: reservations were discharged and a different id is now fenced. Re-derive the live set; the remembered one is wrong.]** Which ids does `BACKLOG.md`'s **Id-reservations note** hold reserved **right now**, which previously-reserved ids has it **discharged** (and are they now in use or free), and how many bare dangling references does the file still carry into the hub id space? | `BACKLOG.md` (Id-reservations note + task lines) | the reservation set is the **precondition of any new filing** — assigning a fenced id silently captures someone else's dangling reference, which has already happened repeatedly here. Both the reserved set and the discharged set changed this window, so a remembered set is actively dangerous; both are live text facts | **TARGET:** `grep -n 'Id reservations' BACKLOG.md` (read the note in full) then `grep -c 'refs #96' BACKLOG.md` then `grep -n '\[#84\]\|\[#85\]\|#107' BACKLOG.md` |
| P14 | **[The allowed-set gap — RECORDED as a dated note, so the live question is whether the snapshot still holds.]** `ARCHITECTURE.md`'s Layer-edges allowed set is labelled **TARGET, not current state**, with a dated current-state note recording `cli.py`'s real edge surface. Re-derive that surface **live**: how many real `src/ai_council/` inter-module imports does `cli.py` carry now (module-level and function-level; TYPE_CHECKING-only excluded), how many fall **inside** the allowed set, and does the **recorded note still match**? Has the re-derivation trigger — the `cli.run()` refactor ticket — **landed yet**? | `src/ai_council/cli.py` ∩ `ARCHITECTURE.md` "Layer edges" + its dated current-state note ∩ the refactor task line in `BACKLOG.md` | the doc carries a **dated snapshot of a live quantity** — the exact shape that goes stale silently. Note that a raw import grep and the note's counting rule do **not** agree by construction (the rule excludes TYPE_CHECKING-only edges), so the comparison requires reading the rule, not just counting lines. Answerable only by intersecting source, doc, and backlog at answer-time | **TARGET:** `grep -n 'from ai_council' src/ai_council/cli.py` for the source side; `sed -n '/^Layer edges/,+40p' ARCHITECTURE.md` for the doc side (read the dated current-state note **and** the TARGET label **and** its counting rule); then `grep -n '\[#92\]' BACKLOG.md` for the trigger's status — compare all three by hand |
| P15 | **[RE-BOUND — the uncommitted-local-config mechanism was REPLACED by real refs this window; verify the replacement actually holds.]** Do the `archive/cited-*` tags exist **locally**, do they exist **on the remote**, do the two sides agree, and does each still resolve to a reachable **commit** object? Is the local `gc.auto` override now **absent** (if it is still set, its value is part of the answer)? | live git refs ∩ `.git/config` (local) ∩ the object store | this replaced the one load-bearing fact that was **not in the repo** — a local config value protecting objects past git's prune horizon. The whole point of the fix is that the protection is now **verifiable from a clone**, so verifying it is not ceremony: if the tags are local-only, or the override silently persists as the real protection, the fix is not the fix it is recorded as | **TARGET:** `git tag -l 'archive/*'` then `git ls-remote --tags origin` then `git cat-file -t` on each tag's target, then `git config --get gc.auto` (**report whether it is set at all** — an unset value exits non-zero, which is a possible correct shape, not an error) |
| P16 | Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors the evidence base the still-open extractor design forks depend on; a branch push does **not** carry tags, so local-remote divergence is a live possibility only git can answer, and several bundles have now flagged this exposure — whether it stayed resolved is answerable only live | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config file is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from the final
> path segment, so a backticked repo-root dotfile is looked up without its dot and resolves nowhere —
> the probe is then FAILed as a missing target even though the file plainly exists. (Dot-*directories*
> are unaffected; it is specifically the last segment.) **Consequence: no probe in any bundle — hub or
> cross-repo — can currently bind to a repo-root dotfile.** That is a hub tooling defect, filed
> upstream as hub `[#421]`; it is deliberately **not** patched from inside this handoff, because hub
> infra changes are exception-with-ruling (core-invariant #6). The probe's teeth are unaffected — the
> comparison is still live-only and answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `CLAUDE.md`, `JOURNAL.md`,
   `scripts/validate_backlog.py` all exist in both). This is the single most likely failure mode of a
   cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d) — FULL** (the supplement is
   generated empty; there is nothing to narrow against). Then run P2–P16, each against **live state
   now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P16 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number."
   **Order matters for four of them:** **P7 before accepting any "the gates are green" claim** (it is
   the headline substitute, and reading its stdout-vs-exit-code split is the window's whole lesson);
   **P11 before any checker work** (it supplies the live shape of the rule-4 narrowing the next arc
   repairs); **P12 before reading any finding count as coverage** (the skipped/total split is the real
   denominator); **P14 before any allowed-set or codemap edit** (the doc carries a dated snapshot that
   may already be stale, and its counting rule must be read, not assumed).
   **P10 grooms the whole open BACKLOG at boot** — the operator-ruled boot obligation, not optional,
   and the open set moved in both directions this window.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the assembler folds nothing and the
   §13(d) beat fires **FULL**. Confirm by looking at the bundle directory in the hub — it is CC-side
   bookkeeping, not target state.
