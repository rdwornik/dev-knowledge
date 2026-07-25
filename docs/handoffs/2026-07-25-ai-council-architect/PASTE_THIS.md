=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-25-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. Every probe runs in the **target** root — see the run-in-root table at the top of `PROBES.md`. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-25-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**The checker got built — and it shipped with a hole its own green test suite structurally could not see. Rule that class, then shape the arc.** The last window's biggest gap (no automated doc-vs-reality organ) is now partly closed: a read-only, non-blocking claim-vs-reality checker landed, alongside the allowed-edge-set ruling (recorded as **TARGET**, re-derivation triggered by the refactor ticket) and the largest filing batch in the recent record. But its rule registry is **incomplete and undisclosed** (**P11**), for the second instance of one recurring shape — a validator checked against its own artifact. Rule the standalone repair, rule whether that shape gets a durable home, then rule the checker's gate posture and the zero-findings follow-up whose target moves on its own (**P12**). **Keep the blind-scoring lane unblocked and out of the ordering — it is operator-only and shares no surface with any of this.** Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; the grooming log's 2026-07-25 entries are this window's ruling record — read them before re-deciding anything.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-25-ai-council`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-25-ai-council-architect — the part the repo does not already encode

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

> **The ANSWERS outrank this residual on intent, priority and SEQUENCING — read them before acting on
> §4's ordering.** This residual is repo-derived; the supplement carries what only the outgoing
> architect held. Five load-bearing corrections, so §4 is not silently followed as written:
>
> - **(A) Sequencing is inverted — "Unit 1.5 before Unit 2."** Two filed follow-ups change the
>   **frozen `Finding` harness surface** (one adds a field, one changes the printer). Land them while
>   the blast radius is four legs; at eleven it becomes a retrofit. §4 item 1 (the registry repair) is
>   still correct as the *standalone* first move, but the harness changes come **before** any Unit-2
>   rule building — not after, as §4 item 4 implies.
> - **(B) The dispositioned precision-over-recall High is NOT merely "waiting on the operator"** (as
>   §4 item 8 files it). Its revisit trigger has **already fired early**: the same repo-rooted guard is
>   implicated in three separate failures, making it the **single highest-leverage fix in the checker**.
>   Treat it as a live design item near the top, not queued admin.
> - **(C) A ruling landed this window that §4 does not carry at all** — the operator ruled **CLI is the
>   default transport for debate, API for research mode**. It exists **only in chat**: it belongs in an
>   ADR or at minimum a ticket. It also **reframes the blind-scoring lane** (§4 item 0) from a decision
>   into a **cost control** — measuring what the preference costs in quality, not whether it is
>   preferred — so that lane's done-when needs rewriting. Item 0's *ordering* rule still stands
>   unchanged: operator-only, never sequenced behind anything (it has now slipped **six consecutive
>   windows**).
> - **(D) An open governance question, absent from §4:** a push to `origin/main` this window came from
>   neither CC nor the cloud session. "The operator is the serial merge gate" is **not enforced against
>   a background pusher.**
> - **(E) A hard execution constraint on the next arc:** in this target, **worktrees are blocked
>   outright** — a worktree shares the primary's editable install, so pytest inside one silently tests
>   the primary's source, and the include-file that would fix it does not exist here. Plan the arc as
>   primary-checkout work.
>
> Also carried by the supplement and worth reading directly: a **do-not-relitigate list** (§3) and an
> explicit **architect-seat calibration** — several browser-seat errors this window were all one class
> (asserting conclusions rather than primitives), all caught downstream. Treat browser-seat pointers as
> claims to verify. **On any number, the probes outrank both this residual and the supplement.**

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks **the target actually has** — the four gating `ai-council`
validators (P7) + `validate_backlog` (P9) + the **new** report-only claim-vs-reality checker (P11/P12)
— plus hand intersection where the hub organ has no target equivalent (P2, P4, P14). **Re-derive each
at read-time — the teeth are in `PROBES.md`, not in trusting these lines.** This bundle states **no**
validator verdict, count, drifted `#id`, or sha — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo re-frame:** `ai-council` still carries **no** `audit.py` ship-gate, `validate_doc_claims`,
`validate_git_backlog`, or disposition register. What changed this window: the doc-vs-reality gap the
last two bundles named as *specified-but-not-built* is now **partially built** — `scripts/validate_claims.py`
(`#97` Unit 1) runs read-only and **non-blocking** as a `check.ps1` section. It is a **measurement
surface, not a gate**; a non-zero finding count is the point, not a failure.

**NEW + LOAD-BEARING (the headline): the checker's rule registry is INCOMPLETE, and its own test suite
structurally cannot say so.** `#97` specifies fourteen rules. Some rule ids have **no row in the
registry at all** — not implemented, not stubbed, not disclosed by the checker's KNOWN LIMITATIONS
header — so **no run mentions them and no drift they were commissioned to catch is monitored today**
(**P11** re-derives the exact set difference; the outstanding total is larger than the report implies).
The root cause is the part that generalizes and is the reason this leads the headline: the registry
test is parametrized **over the registry**, so it covers whatever is present and **cannot detect an
omission** — a self-referential completeness test has no denominator. A large new test module went
green while rules were missing. This is the *same shape* as the rule-14 leg-(a) vacuity the last
window fixed (validating a hand-maintained map against itself), recurring one layer up, in the organ
built to catch exactly that class. The repair (register the absent rules + an **external** expected-set
test) is `#97`'s own remaining work and is not done.

**NEW: the checker's finding set self-replicates and is GROWING.** Every JOURNAL entry that discusses
dangling-SHA findings **cites SHAs**, which the rule-8 leg then re-reports — so the count climbs on its
own with each prepend, and the line numbers in each finding shift as the newest-first file grows
(**P12** measures it live). This matters structurally, not cosmetically: a filed task's done-when is a
**zero-findings gate**, and it is blocked by two others precisely because the gate is unpassable while
this loop runs. Treat P12's number as *distance-to-passable*, and note that it moves without anyone
touching the checker.

**NEW: one rule is non-deterministic across checkouts for the identical commit.** A gitignored
directory exists as untracked debris on this primary checkout but is absent from a fresh clone, so the
same rule fires here and is suppressed there. Two honest sessions reported contradictory results and
**both were right**. This undercuts the per-rule clean-window trigger a filed follow-up depends on,
independently of the other two blockers — and that follow-up's blocker list does **not** yet name it.

**STANDING, now RECORDED rather than open (do not re-litigate):** the `ARCHITECTURE.md` Layer-edges
allowed set was ruled this window — marked **TARGET, not current state**, with a dated current-state
note recording `cli.py`'s real edge surface, **set values byte-unchanged** (the ruling deliberately did
not widen the boundary to match the defect: *rewording a boundary to match a defect launders the
defect*). The re-derivation trigger is `#92` landing. So the live question is no longer "what is the
gap" but **"has the trigger fired, and is the dated snapshot still true"** — **P14**. The `cli -> boost`
open case is still unruled and still bound to the `#69`/P2 arc.

**STANDING (fenced, not yet resolved):** the dangling `refs #96` occurrences in the carried hub-id
tasks — hazard contained by the BACKLOG **Id-reservations note**, which was **extended a third time**
this window after another hub/local id collision was caught by the standing grep-before-assign rule
(**P13** re-derives the fence). Reactive reservation per collision is the patch; the checker's
ticket-reference rule is the fix, and it is one of the unbuilt ones.

**STANDING (uncommitted, and therefore invisible to every other organ):** a **local** `gc.auto` setting
is what currently keeps four unreachable commit objects alive — they are past git's default prune
horizon, so age no longer protects them. This is a load-bearing fact that **is not in the repo** and
cannot be carried by any clone, doc, or summary (**P15**). Restoring the setting is part of the filed
task's done-when, so the repo is knowingly carrying silent disabled-maintenance debt until then.

**RESOLVED THIS WINDOW — do not re-flag:** the cloud-run contradiction over a checker finding (resolved
as the checkout-nondeterminism above, not a disagreement); the "missing token log" finding (reconciled
as **stale addressing, not a missing file** — the log is the hub's, as the install doc already states);
a reported protocol-file drift (reconciled as a **checker false positive** — an allowlist keys on a
path prefix *inside* the backticks while the attribution is in prose; folded into an existing follow-up
as a leg, not filed as drift).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-23 handoff. One line each; detail lives in `JOURNAL.md` (entries
2026-07-24/25) + the merge messages. All ids/paths are **ai-council's**. Six first-parent merges.

- `766241a` — **`#27` blind-scoring instrument prepped** (`READING-INDEX.md` + blank `SCORING-RECORD.md`
  inside the existing frozen cli4-parity workspace; rubric inline, 12 pairs in scoring order, sealed key
  verified untracked and never opened). Lane is **READY and waiting on the operator** — not on any build.
- `766241a` (same branch, Lane 1) — **STEP-0 acceptance-freeze reads**: established that the night-batch
  report carries *twelve* rules on disk while the fourteen-rule spec lives only in `BACKLOG.md` `#97`;
  confirmed both late-added rules carry real non-vacuous earned-by traces, with the honest caveat that
  they were earned in their own authoring session and two are partly self-referential.
- `b1f3319` — **FLOOR1 R1 ruling applied** (ARCHITECTURE only): allowed edge set relabelled **TARGET,
  not current state**, `cli.py`'s real surface re-derived **live via AST** (not trusted from the prior
  bundle's probe numbers — the derivation reproduced them exactly), dated current-state note added,
  codemap-completeness gap recorded with a pointer to the map-vs-source rule leg. **Set values
  byte-unchanged**; `cli -> boost` still the one open case.
- `b94e8d1` — **`#97` Unit 1 shipped**: `scripts/validate_claims.py`, a read-only claim-vs-reality
  checker wired as a **non-blocking** `check.ps1` section per the standalone-not-a-gate ruling. Four
  rules implemented RED-first; the remaining registered ones are Unit-2 stubs; the evidence-command rule
  is **structural** (an argv tuple whose shlex round-trip is executed by the harness — verified, not
  promised) rather than a leg. terra returned **5 High / 0 Critical**; four fixed, one dispositioned as
  a deliberate precision-over-recall tradeoff. A KNOWN LIMITATIONS header was added pre-merge so the
  checker does not overclaim about itself.
- `6002aba` — **filing batch**: one 18-item operator window → **12 new ids + 5 rider edits**, every
  claim grep-verified against the live tree before proposing (which changed three of the filings). Task
  count and story count both moved; one id **skipped and newly reserved** on a third hub/local
  collision. `gc.auto` set to `0` repo-locally **before** the branch was cut (mechanism, not prose).
- `1fa0054` — **`#97` reconciled to reality**: the task line now records Unit 1's landing instead of
  reading as unbuilt work, **records the two absent rules**, and amends a done-when whose first clauses
  were already true for the implemented subset. Two gates added to its scope: register all fourteen with
  the one sanctioned structural exemption, and an **external expected-set** registry test.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
Ordered: the standalone correction first, then the design question it raises, then the arc it gates,
then record debt. **One item is deliberately out of the ordering** — see item 0.

**0. `#27` blind scoring is OPERATOR-ONLY and must never be sequenced behind anything.** The instrument
is built and the lane is READY (`766241a`); what remains is the operator reading twelve pairs, then the
unseal and the parity tally. A downstream ticket is gated behind it. It shares no surface with anything
below, so it runs in parallel with every item here — do not let a build arc absorb it. (This ordering
rule was an explicit correction from the last window's supplement; it is repeated because it was
violated once.)

1. **The `#97` registry repair — immediate and standalone.** Register the absent rules, and add the
   **external expected-set** test (an explicit id set asserted against `RULES`, not derived from it).
   This is not blocked on Unit 2 scope, on the checker's gate question, or on anything else; it is a
   correction to something already shipped, and until it lands the checker silently under-reports its
   own coverage. **P11** gives the exact set to repair.
2. **The design question the defect raises — does the "external denominator" rule get a durable home?**
   Twice now the same failure has shipped: a validator checked against its own artifact (the map-vs-map
   leg) and a test parametrized over its own registry. The specific fixes are cheap; the recurring shape
   is the real finding. **Open:** is this a checker rule of its own (self-referential-validation
   detection), a `LESSONS.md` entry, a review-checklist item, or nothing durable? The architect should
   rule — this is exactly the way-of-working question architect mode exists for, and it is currently
   held nowhere but in one JOURNAL paragraph.
3. **Is the zero-findings gate the right shape for the checker follow-up at all?** Its done-when is "0
   findings," and it is already blocked by two other items. Two facts landed this window that the gate's
   design did not anticipate: the finding set **self-replicates** with each JOURNAL prepend (so the
   target moves away from you as you write about it), and one rule is **non-deterministic across
   checkouts for the identical commit**. **Open fork:** (a) keep the zero-findings gate and first fix
   the loop + the nondeterminism, (b) re-shape the gate to a per-rule clean window — which the
   nondeterminism *also* undercuts — or (c) accept a non-zero baseline and gate on *new* findings only.
   Whichever is ruled, the blocker list currently does **not** name the checkout-nondeterminism; that
   omission should be closed in the same edit.
   - **Sub-question worth ruling explicitly:** should JOURNAL entries stop citing bare SHAs for
     dangling-SHA discussions? The last two entries deliberately declined to re-cite them for exactly
     this reason — that is a convention being followed with no written rule behind it.
4. **Checker Unit 2 scope + posture.** The remaining rules (including the AST import-graph leg) build
   against a frozen interface — that part is settled. **Open:** which rules gate versus report; whether
   the checker graduates from a non-blocking `check.ps1` section into a real gate, and if so which
   subset; and whether it becomes the target-side organ that closes the "no automated doc-claim check"
   gap (§1) or stays advisory permanently. Note the standalone-not-a-pre-commit-gate ruling settled the
   *home*, not the *posture*.
5. **The `#92` arc still carries three coupled things — unchanged, and still unruled.** (a) `#92`'s
   `cli.run()` refactor is the named **re-derivation trigger** for the allowed-set snapshot (**P14**
   tells you whether it has fired and whether the dated note still holds); (b) the `cli -> boost` open
   case — reclassify `boost` to orchestration, or admit a *scoped* interface→core edge — rule it with
   the re-derivation, not before; (c) the parity fix carries a **verified constraint**: the divergent
   models-gating expression **is also** what makes the wide panel the effective default, so any fix must
   decouple the two and land a bare-invocation panel-default regression test **first**, or it silently
   flips the default. A strict xfail errors the suite the moment the wiring lands — wiring and parity
   fix are one arc by construction.
6. **The fenced ADR-02 amendment** — scope is (a) overlap policy + (b) stale stamp only. The
   panel-default question inside it is **DISSOLVED and out of scope**; the amendment must not reopen it.
   The checker's config-parity rule carries the guard: adjudicate *effective flag-resolution behaviour*,
   never raw config keys.
7. **Record debt, in dependency order.** The **renumber arc** (both carried hub-id tasks, resolving or
   dropping every `refs #96` occurrence **in the same edit** — the audit's explicit instruction; **P13**
   re-derives the fence, and note the fence grew again this window). Then **restoring `gc.auto`** once
   the dangling objects are dealt with (**P15** — until then the repo carries silent
   disabled-maintenance debt, and the protection is uncommitted). Then the still-**un-triaged** batch
   proposal set, which a BACKLOG-only reader still cannot see item-by-item.
8. **Three done-when texts are still awaiting an operator ruling**, and one of them — the
   **review-runner convention** — is the fresh-architect gap named two windows running: the review-lane
   routing posture (which reviewer lane runs what; one lane withdrawn on cost) lives only in `~/.claude`
   and the JOURNAL, and is **not a repo record**. A ruling here would also absorb it. Separately, the
   dispositioned High from the terra review and the checker's self-negating allowlist residual are both
   waiting on the operator, not on design.
9. **A newly-filed pair encodes a real fork, deliberately as two tickets:** the boost sharpening-
   annotation block and the interactive clarify-loop. The second names **both** exits — built per the
   proposed design, **or** closed as deliberately-not-doing if the ADR-11 decision-1 ruling forecloses
   interactivity — so a ruling either way resolves it rather than leaving a zombie. That ruling is
   architect work and has not been made.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council`'s**
`BACKLOG.md` (themes `[E1]`–`[E7]`; the grooming log carries this window's rulings), the live
in-progress branches (`git branch -v`, run in the **target**), and the drifted-closed intersection
**P4 computes by hand** (§1 — the target has no `validate_git_backlog`). Re-narrating item text splits
the truth and drifts — the pointer + the drift-flag is the whole task-state. The whole-open-set
grooming obligation at boot is **P10**, and its denominator grew materially this window — the filing
batch is the single largest task-count move in the recent record, and several new items are blocked on
each other rather than on work.

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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-25-ai-council` **in the
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

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below confirmed present at generation time by running its command in the target). Where the hub
has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**What changed since the last cross-repo bundle:** the "no automated doc-vs-reality organ" gap is now
**partially closed** — `scripts/validate_claims.py` landed this window as a read-only, **non-blocking**
report-only checker (a fifth validator surface, deliberately **not** a gate). Two probes are new
because of it: **P11** (registry completeness — the window's headline defect) and **P12** (its live
finding set). P2, which existed to hand-build the missing doc-vs-reality tooth, is **kept** — the
checker does not yet cover the hook-roster claim.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead. `scripts/check.ps1`
is likewise **not** a probe — it is the full pytest+mypy+ruff trio, far past read-only-cheap; P6 and
P12 call the two pieces a probe actually needs.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS are folded into `PASTE_THIS.md`, so the incoming §13(d)
> operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*
> **Read the ANSWERS before the residual's §4 ordering — they correct it on load-bearing points**
> (see the corrections block at the top of `RESIDUAL.md`). The supplement wins on intent, priority and
> sequencing; the residual stays authoritative on *what the defects are*; **the probes below outrank
> both on any number.**
>
> **One caution specific to this supplement.** Its answers state some repo-state values (a task count,
> a HEAD sha, an outstanding-rule total) — beyond the interview's why-only scope (§13 "hard scope
> constraint"). They are committed **verbatim and unedited**, as the contract requires, but they are a
> **generation-time snapshot and are never trusted over the repo**: **P9** and **P11** still govern
> those numbers and must be re-derived live. If a supplement value and a probe disagree, the probe is
> right.

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
by CC, substring-matched. `ARCHITECTURE.md` was amended **again** this window (the R1 allowed-set
correction), so the live lines, not any remembered ones, are the frame. **Then, before design, the
operator-context beat fires (§13d) — NARROWED** (the supplement is FILLED — ask only *"anything
changed since it was written?"*).
**P11 and P12 are unusually load-bearing this window:** the supplement's own §5 re-sequences the next
arc around the registry gap and the harness-surface changes, so P11's live set-difference and P12's
live finding count are the two numbers that plan is built on — re-derive both before accepting the
sequencing.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; the new checker does not cover this claim either.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and do **both** doc rosters — `ARCHITECTURE.md`'s prose roster **and** `CLAUDE.md` §9's — list that **same set**, including the total each states? | the pre-commit config ∩ `ARCHITECTURE.md` (hook-roster prose) ∩ `CLAUDE.md` §9 | the roster drifts every time a gate lands, and **two** doc surfaces must both stay reconciled — the checker's rule 3 covers *mention*, not set-equality or the stated total, so a divergence stays invisible until someone reads all three | **TARGET:** `grep -n 'hook' ARCHITECTURE.md` and `grep -n 'id:' CLAUDE.md` for the doc side; for the config side run grep -c and grep -n on the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the three by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it, and several entries this window landed commit-and-STOP branches whose merge/push status is exactly the live question | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch -v` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle. This window filed a double-digit id batch, so the intersection has genuinely moved | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — and ARCHITECTURE took another merge of edits this window (the R1 correction), so the relation is among the freshest facts in the repo | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change, and this window added a large new test module; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **gating** read-only validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Note several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; the count, the tail slug, and whether the index has kept pace are all live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings** — and what does `BACKLOG.md`'s grooming log name as the **next free local id**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window moved every one of them (a double-digit task delta plus a reconciliation landed); the next-free pointer moved too; none of it is in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) then `grep -n 'Next free local id' BACKLOG.md \| tail -1` |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **The open set grew substantially this window** (a filing batch plus rider edits), so the grooming denominator itself has moved — and several of the new items are explicitly blocked on each other | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[NEW — the window's headline defect, and the number the next build arc starts from.]** How many legs does the checker's `RULES` registry actually contain right now; of the fourteen rules `BACKLOG.md` `#97` specifies, **which rule ids have no row in the registry at all** (neither an implemented leg nor a Unit-2 stub); and does the checker's own **KNOWN LIMITATIONS** output disclose those absences? | `scripts/validate_claims.py` (`RULES`) ∩ the #97 task line in `BACKLOG.md` ∩ the checker's report header | the registry is a live code fact; the spec count is a live doc fact; the **set difference between them is the defect** — and it is invisible to the checker's own test suite, because the registry test is parametrized **over the registry** and so has no external denominator. A summary that read "4 built + 7 stubs" never sums it against fourteen — which is precisely how the gap survived a green suite | **TARGET:** `grep -n 'rule_\|_unit2_stub(' scripts/validate_claims.py` (read the `RULES` list in full) then `grep -n 'KNOWN LIMITATIONS' scripts/validate_claims.py` and read the block it heads, then `grep -n '\[#97\]' BACKLOG.md` — compute the set difference by hand |
| P12 | **[NEW — the checker's live finding set; the input to the `#104` zero-findings gate.]** Run the report-only checker: **how many findings** does it emit **right now**, **across which rule ids**, and how many legs report `skipped(Unit2)`? Then: how many of those findings are the **self-replicating** class (a rule-8 dangling-SHA finding whose citation is itself a JOURNAL entry about dangling SHAs)? | `scripts/validate_claims.py` run over the live tree | the count moves on **every JOURNAL prepend** — the self-replication `#105` predicts is a live, growing quantity, and the line numbers in each finding shift as the newest-first file grows. **`#104`'s done-when is a zero-findings gate**, so this number is the gate's live distance-to-passable; none of it is in this bundle | **TARGET:** `python scripts/validate_claims.py` — read the final `SUMMARY:` line (pass / FINDINGS across N rules / anchor-missing / skipped / errors), then read the per-finding lines above it. **Report-only and non-blocking by design — a non-zero finding count is NOT a failure**, it is the measurement |
| P13 | **[The reservation fence the renumber arc depends on — extended again this window.]** Which ids does `BACKLOG.md`'s **Id-reservations note** hold reserved **right now**, how many `refs #96` occurrences does the file still carry, and are the two carried hub-id tasks still sitting at their hub ids? | `BACKLOG.md` (Id-reservations note + task lines) | the reservation set and the dangling-ref count are the **preconditions of the pending renumber arc** — if either has moved, the arc's plan is stale. A **third** hub/local collision was caught and fenced this window, so the reserved set is not the one a summary remembers; both are live text facts | **TARGET:** `grep -n 'Id reservations' BACKLOG.md` (read the note in full) then `grep -c 'refs #96' BACKLOG.md` then `grep -n '\[#110\]\|\[#128\]' BACKLOG.md` |
| P14 | **[The allowed-set gap — now RECORDED as a dated note, so the live question changed.]** `ARCHITECTURE.md`'s Layer-edges allowed set is now labelled **TARGET, not current state**, with a dated current-state note recording `cli.py`'s real edge surface. Re-derive that surface **live**: how many real `src/ai_council/` inter-module imports does `cli.py` carry now (module-level and function-level; TYPE_CHECKING-only excluded), and does the **recorded note still match**? Has the re-derivation trigger — `#92`'s `cli.run()` refactor — **landed yet**? | `src/ai_council/cli.py` ∩ `ARCHITECTURE.md` "Layer edges" + its dated current-state note ∩ the #92 task line in `BACKLOG.md` | the doc now carries a **dated snapshot** of a live quantity — the exact shape that goes stale silently. The R1 ruling deliberately did **not** widen the set; it recorded the gap and named `#92` as the re-derivation trigger, so "has the trigger fired, and does the snapshot still hold" is answerable only by intersecting source, doc, and backlog at answer-time | **TARGET:** `grep -n 'from ai_council' src/ai_council/cli.py` for the source side; `sed -n '/^Layer edges/,+40p' ARCHITECTURE.md` for the doc side (read the dated current-state note **and** the TARGET label); then `grep -n '\[#92\]' BACKLOG.md` for the trigger's status — compare all three by hand, noting which listed edge is still the **open case** |
| P15 | **[NEW — an uncommitted local mechanism holding unreachable objects alive.]** What is this checkout's **local** `gc.auto` setting, and do **all four** of the dangling commit objects `#112` enumerates still resolve as commit objects right now? | `.git/config` (local, **uncommitted by nature**) ∩ live git object store | this is the one load-bearing fact in the repo that **is not in the repo** — a local config value no clone, summary, or file read can carry, protecting objects that are past git's default prune horizon. If it has reverted, the objects can vanish at any `gc --auto`; `#112`'s done-when includes **restoring** it, so its current value is also a debt marker | **TARGET:** `git config --get gc.auto` then `grep -n '\[#112\]' BACKLOG.md` to read the four shas it enumerates, then `git cat-file -t <sha>` for each one |
| P16 | Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors the evidence base the still-open extractor design forks depend on; a branch push does **not** carry tags, so local-remote divergence is a live possibility only git can answer, and the last two bundles both flagged this exposure — whether it was since resolved is answerable only live | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports |

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
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `CLAUDE.md`, `scripts/validate_backlog.py`
   all exist in both). This is the single most likely failure mode of a cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d) — NARROWED** (the supplement is
   FILLED — ask only *"anything changed since it was written?"*). Then run P2–P16, each against
   **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P16 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number."
   **Order matters for three of them:** **P11 before any `#97` build work** (it supplies the registry
   gap the next arc repairs, and the reason the green suite did not catch it); **P12 before touching
   `#104`** (its finding count is that gate's live distance-to-passable, and it grows on its own);
   **P14 before any allowed-set or codemap edit** (the doc now carries a dated snapshot that may
   already be stale, and `#92` is its named re-derivation trigger).
   **P7 remains the headline substitute** (four exit codes, read explicitly — several gates pass
   silently, so "no output" must not be scored as "no drift"). **P12 is report-only: a non-zero
   finding count is the measurement, not a failure.** **P10 grooms the whole open BACKLOG at boot** —
   the operator-ruled boot obligation, not optional, and the open set grew this window.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **FILLED**, so its ANSWERS are folded into `PASTE_THIS.md`
   and the §13(d) beat **NARROWS**. Confirm by looking at the bundle directory in the hub — it is
   CC-side bookkeeping, not target state.

---

=== SUPPLEMENT.md ===

# Handoff answers — `ai-council` window 2026-07-23 → 2026-07-25

End state: `main 1fa0054`, pushed, in sync, tree clean, only `main`, primary worktree only,
`gc.auto 0`, `validate_backlog` OK 7 themes / 15 stories / **71 tasks**, `check.ps1` green with
the claim-checker running non-blocking. Hub `main d589844c`, in sync.

---

## Plan vs actual

| Planned | Result |
|---|---|
| FLOOR 1 — allowed-edge-set correction | ✅ `b1f3319` |
| FLOOR 2 — `#27` scoring materials | ✅ instrument ready, key sealed |
| PRIMARY 1 — checker v1, 14 rules | 🟡 **Unit 1 only** — rules 2/3/4/8 built, 12 structural, **nine outstanding** |
| PRIMARY 2 — `#27` blind-scoring sitting | ❌ **not run** (sixth consecutive window) |
| SECONDARY — filing batch | ✅ `6002aba`, 12 ids + 5 riders, 59→71 |
| SECONDARY — panel-default pin | ❌ |
| STRETCH — renumber, `#19` design | ❌ (`#103` filed, not executed) |

**Succeeded:** the window's closure criterion for *rulings* is fully met — no operator decision
from this window survives only in prose. The checker exists, runs automatically, and is honest
about its own gaps in its own output.

**Failed:** the only item that required the operator's hands did not happen, and it is the one
gating an entire theme.

---

## 1. Strategic intent — the way-of-working goal for next session

**Install external reference points wherever a mechanism currently verifies itself.**

This window's recurring discovery, five separate instances:

- rule 14 leg (a) validates the codemap against itself — an illegal import the map omits passes
- the Codex severity counter printed `0` over eight HIGH findings
- `grep -c '<<<<<<<' JOURNAL.md` counts its own logged quotation, so the counter inflates with
  every session that records the guard
- the Tier-1 gate cited proposal commits instead of build commits
- `@parametrize("leg", RULES)` iterates the registry, so 41 tests passed green while **two rules
  were missing from it entirely**

One principle unifies them: **self-referential verification is not verification.** A test that
enumerates a registry can only confirm what is present. A rule that compares a map to itself is
vacuous. A guard keyed on local directory state gives different answers in different checkouts.

The next session's methodology goal is not "build more rules." It is: every checking mechanism
must be anchored to something outside itself — a literal expected set, a spec, a second
derivation. `#97`'s new done-when clause (ii) is the first instance; the pattern is general.

**Second, smaller goal:** the architect seat should assert primitives, not conclusions. Five
architect errors this window, all the same class (see §6), all caught downstream. The pair works;
the failure concentrates in one half of it.

---

## 2. Tensions weighed, and where they landed

**Precision vs recall in rule 2 (terra H3).** Landed on **precision**, accepted for v1, on the
grounds that a report-only tool's only capital is credibility: a false negative costs one finding,
a false positive costs trust in all of them. **This position is now under revision, earlier than
planned.** The repo-rooted guard turned out to be implicated in three separate failures —
checkout non-determinism, suppression of LESSONS.md's one live defect, and unknown recall. The
revisit trigger I set ("at gating promotion") has fired early.

**Report vs gate.** Landed on **report-only, non-blocking**, but with the script exiting non-zero
from day one and only the `check.ps1` call site swallowing it. Promotion is a one-line call-site
change, never a rewrite.

**Suppress vs classify (rule 8's tracking citations).** Landed on **classify, never suppress.**
Filing `#112` and `#105` doubled rule 8's finding count, because both tickets name the dangling
SHAs they track and the checker cannot tell a tracking citation from a careless one. The cheap fix
— obfuscating the SHAs so rule 8 stops matching — was rejected: hiding a real dangling reference
to lower a count inverts the tool's purpose. `#105`'s distinct-defect accounting is the real fix.

**Rider vs own id (`#101` / `#113`).** Landed on **two tickets.** A deferred clause inside a
ticket that will eventually close either blocks that closure or vanishes with it, carries no
open-id status, and cannot enter a ranked queue.

**Ordering: filing batch vs more code.** Landed on **batch first.** Every operator decision from
this window existed only in chat; the batch is the persistence mechanism, and it is cheap.

**Verification cost vs speed.** I demanded verbatim artifacts four times rather than accepting a
summary. Twice it changed the outcome; once my suspicion was wrong but the check was still correct
to make; once I deliberately skipped it and took the artifact in the post-merge report instead.
That calibration is itself a result: demand the artifact when it gates a freeze or a merge, take
it after the fact when it is cheap to amend.

**CLI default vs measured parity.** The operator stated this window that **CLI is the default
transport for debate, API for research mode**, with deliberate opt-in to API otherwise. That is a
coherent architectural split — research has different needs (retrieval, longer context). My
position: the ruling stands, but it does not remove the reason `#27` exists. Twelve blinded pairs
measure *what the preference costs in quality*, not *whether it is preferred*. The sitting becomes
a cost control, not a decision. **Not yet confirmed by the operator, and `#27`'s done-when should
be rewritten accordingly.**

---

## 3. Considered and rejected — do not relitigate

- **Widening the ARCHITECTURE allowed-edge set** to legalise `cli.py`'s real 14-edge profile.
  Rejected on the repo's own precedent: rewording an invariant to match a defect launders the
  defect. The set is held as **TARGET**; `#92`'s refactor shrinks the real surface toward it, and
  re-derivation is triggered by `#92` landing — not by opinion.
- **`markdown-it-py`** for the options scanner. Rejected by the `#80`/`#81` spike: it inverts the
  failure mode (the scanner fabricates options from a fence; the library loses the whole list) plus
  a large in-parse performance regression. Settled.
- **Stop-hook as the checker's wiring surface** — fires every session end including doc-untouched
  ones, constant noise. **Pre-commit** — pass/fail by construction and sits with formatters, which
  breaks the read-only requirement. Landed on a non-blocking `check.ps1` findings section.
- **Allowlisting `.claude/skills/`** to silence the self-negating finding. Rejected: an allowlist
  would hide the whole negation class. Named in KNOWN LIMITATIONS instead.
- **Worktrees for any pytest-bearing work.** A worktree shares the primary's editable install, so
  pytest inside one silently tests the primary's source. Separately, `.worktreeinclude` does not
  exist in this repo, so worktrees are blocked outright until it does.
- **`pytest -n auto` in `ai-council`'s `check.ps1`** — rejected on clean numbers (1.42×, not
  3.9×). The hub *does* use it; the asymmetry is deliberate, not drift.
- **Assigning `#107`** — reserved instead. Third hub/local id-space collision.
- **`sol` for a second derivation of the rule spec** — the spec is already an evidence-backed
  derivation from a real manual run. Cost without added evidence.
- **The parallel cloud session's branch** — discarded. It converged on identical output (free
  corroboration of the id assignment), but its pre-commit gates were *skipped, not passed*, and it
  filed two claims it could not verify from its checkout.

---

## 4. Open questions

1. **Is the H3 precision-over-recall ruling still right?** Evidence now says the guard is the
   single highest-leverage fix in the checker. Revisit is due now, not at gating promotion.
2. **Is context-adjudication harness-level or per-rule?** `#108` landed rule-2-local, correctly —
   rule 2's case is a false positive (suppression loses nothing) while rule 8's is a true finding
   with near-zero actionability (suppression would hide real fragility). But both need the same
   underlying predicate: *is this token inside a statement about the defect?* A shared helper is a
   third option neither ticket currently holds.
3. **Should `LESSONS.md` enter rule 2's surface?** Adding it buys nothing until the guard is fixed
   — its one live defect (`tasks/lessons.md`, twice, `tasks/` is not a directory) would be
   suppressed anyway. Separately, the exclusion comment at `validate_claims.py:156-157` claims a
   symmetry the code does not implement.
4. **What pushed `origin/main` at 13:58?** Not CC, and not the cloud (it had no remote, and the
   reflog verb says push-from-here). Governance-relevant: "operator is the serial merge gate" is
   not enforced against a background pusher.
5. **`#27`'s done-when** under the CLI-default ruling — decide the flip, or price a flip already
   decided?
6. **`#8` / `#73` / `#87`** — three done-whens, recommendations issued mid-session, never
   confirmed.
7. **ADR-11 decision-1 interactivity ruling** — blocks `#113`, and nothing schedules it.
8. **How much should the boost boost?** Unruled. Bears on whether `#101`'s emitted annotations are
   machine-satisfiable and on the GUIDE's `### Questions` template.

---

## 5. Decomposition rationale — and what not to redo

**Why this shape:**

- The allowed-set correction had to land **before** any rule-14 work, because leg (a) validates the
  codemap against that set. A factually wrong set means validating against a false standard.
- Unit 1 = harness + finding contract + four legs, deliberately small, because `#105` and `#106`
  both change the **frozen** `Finding` interface. Every leg inherits it. Fixing at four legs is
  cheap; fixing at eleven is a retrofit.
- The filing batch ran last among code work but before session end, because it is the persistence
  mechanism for everything decided in chat.
- `#27` was never sequenced behind anything, by design. Defect-driven ordering structurally cannot
  see an operator-blocked task, which is exactly why it fell out of six consecutive windows.

**Consequence for next session — invert the obvious order: Unit 1.5 before Unit 2.**
`#105` adds a subject field to `Finding`; `#106` changes `printed()`. Both are harness surface.
Land them while the blast radius is four legs.

**Unit 2 is NINE rules, not seven.** Rules 1 and 7 are absent from the registry entirely — not
stubs. Rule 1 (module-table completeness) shares `src/` enumeration machinery with rule 14 leg (b);
build them together. Rule 7 (stamp honesty) extends `canonical_freshness` and is precisely the rule
that would audit this window's three `last_reviewed` re-stamps.

**Do NOT redo or re-decide:**

- The fourteen-rule spec. It now lives **inline in `#97`** with earned-by traces per rule, which
  resolves the earlier split between the immutable audit §3 (twelve rules) and the ticket (13/14).
  Read it there; do not re-derive it.
- The allowed-edge-set correction (`b1f3319`) and its TARGET framing.
- The wiring surface, the `#101`/`#113` split, the `#107` reservation, the `markdown-it-py`
  rejection.
- The `Finding`/`RuleResult` divergence from hub `#89`'s scalar `ClaimResult`. It is deliberate —
  a scalar cannot carry rule 12's per-finding evidence command. It needs **recording** in the hub
  packet, not re-deciding.

---

## 6. Off-repo context

**The three standing themes, honestly graded:**

- **Boost / protocol to other repos — strongest motion.** `#101` (sharpening-annotation block:
  candidate narrowings, missing-constraint questions, criterion pushback — questions and flags
  only, never an invented fact, no ADR-11 reopen), `#113` (interactive variant, both exits named so
  it cannot become a zombie), `#100` (verdict-package JSON Schema — the contract is at 1.0 and
  describes its field set in prose, so a foreign caller has nothing to validate against), `#88`
  named by name to the P2 arc.
- **CLI as default — stated, unwritten.** The operator's ruling exists only in chat. It belongs in
  an ADR or at minimum a ticket. It also reframes `#27`.
- **Non-cognitive debate — weakest, and this must be said plainly.** `#103` was filed as a *design
  commission* (research → design → filed tasks, explicitly not a build) and was not executed.
  `#55` — the matched-compute baseline, the adjudicator of the entire debate bet — remains
  operator-gated and untouched. `#27` unscored. The theme moved on paper only, for the fifth
  window. Everything else this session had a mechanism behind it; this one still has an intention.

**Other context not in the repo:**

- The `#27` instrument (`READING-INDEX.md` + `SCORING-RECORD.md`, rubric inline, items 2 and 4
  zero-margin, key sealed and gitignored) has been ready and unused for a full day. Scoring is
  resumable in parts — the key stays sealed until 12/12, so four pairs now and eight later costs
  nothing.
- **Five architect errors this window, all one class**, all caught downstream by CC: `HEAD` instead
  of `main` in a merge-tree preflight; a stale test count authorized as `N=41`; a "13 commits
  disappeared" conclusion drawn from derived arithmetic; a backup asserted from a truncated report
  that did not exist; and approving a rule split covering 12 of 14 without summing it. Treat
  browser-seat pointers as claims to verify, not facts.
- A concurrent Ultraplan cloud session executed the same filing batch independently and produced
  identical ids, placements, riders and counts. Discarded for the reasons in §3, but the
  convergence is real corroboration.
- Unfiled: three gotchas (`git merge -F -` rejects the stdin dash unlike `git commit`; a called
  script's exit leaks into `check.ps1`'s own exit without an explicit `exit 0`; the ADR-85 JOURNAL
  gate fires per session-stop rather than per substantive change). Home is
  `~/.claude/skills/gotchas/gotchas.md`, needs its own window.
- Uncarried hub packet: the `grep -c '^<<<<<<<'` guard fix, and the `Finding`/`ClaimResult`
  divergence record.
- Token spend 2026-07-18 → 07-25: 8 active days, ~$1.4k, 9.88M tokens, Opus 4.8 at 92%.
