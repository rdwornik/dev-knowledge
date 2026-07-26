=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-26-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. Every probe runs in the **target** root — see the run-in-root table at the top of `PROBES.md`. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-26-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**A great deal landed, and all three mission axes moved zero. Break that pattern, then rule the class of defect that made the green lights untrustworthy.** Everything shipped this window was record and quality-control scaffolding — worth having, but the standing axes (CLI parity, now in its **seventh** un-run window; the boost/protocol Contract-Version arc; non-cognitive debate) are exactly where they were. Two of the three are gated on **decisions, not work** — an operator sit-down and an ADR-11 interactivity ruling that resolves its dependent in **either** direction. Meanwhile the window surfaced one recurring defect **five times**, twice inside the checker built to catch it: **a green published without the predicate that produced it** — a rule reporting pass while reading a fraction of the surfaces it claims (**P11**), and validators whose exit zero is silence rather than a verdict (**P7**). The instance repairs are filed; **whether that class gets a durable home is the open design question**. Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; read the grooming log's 2026-07-26 entries before re-deciding anything. **The supplement is FILLED and it CORRECTS this residual — read its ANSWERS before accepting §4's ordering** (see the corrections block at the top of `RESIDUAL.md`); the §13(d) beat narrows to *"anything changed since?"*.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-26-ai-council`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **The ANSWERS outrank this residual on intent, priority and SEQUENCING — read them before acting on
> §4's ordering.** This residual is repo-derived; the supplement carries what only the outgoing
> architect held. Six load-bearing corrections and additions, so §4 is not silently followed as written:
>
> - **(A) §4's ordering is right but too weak.** The supplement upgrades "hygiene does not preempt
>   items 1–3" into a **testable sequencing rule**: *a window discharges at least one non-delegable
>   item — operator-gated or architect-owed — **before** any CC lane opens.* Testable at close: did it?
>   The diagnosis behind it is sharper than §4's: **all three axis-unblockers are non-delegable**, while
>   **every** backlog defect is CC-executable — so defect-driven ordering fills the window by
>   construction, and once a CC lane is open the architect's attention goes to directing it (which is
>   exactly how `#103` was displaced after being explicitly promised). **Naming this is not a
>   mechanism** — it was named last window and happened again, twice.
> - **(B) A whole item is missing from §4: the unanchored JOURNAL tail is the next session's FIRST
>   act** — a JOURNAL anchor for the window's last three merges. It is **structural, not drift**: an
>   entry cannot name the SHA of the commit containing it, so every session's final commit is
>   unanchorable by construction. Do not file it as a defect.
> - **(C) The mechanism half is capped, deliberately.** `#102`'s ranked queue (with axis items held in
>   its top slots) is the durable version of "axes first" — but **if it threatens to eat the window it
>   drops**. The risk is explicit: it would become the *third consecutive* methodology arc. Open
>   question attached: does the queue **reserve** top slots, or rank purely by priority? A purely
>   priority-ranked queue re-creates the failure, because **every axis item is P3 and the defects are
>   P2**.
> - **(D) Two inherited premises are REFUTED — do not carry them forward.** The previous bundle's
>   "the operator ruled CLI is the default transport" **does not survive the repo** (ADR-12 §5 is
>   unamended; the code requires per-seat opt-in and no seat declares it) — it was **intent, not
>   implemented state**, so `#27` keeps its original meaning as the authorizing gate. And "worktrees are
>   blocked outright" was **wrong as stated**: the real constraint was the system-interpreter editable
>   install, and this target needs no `.worktreeinclude` today. Also corrected: **`#88` has no `#92`
>   binding** in its live ticket text — it is independently schedulable.
> - **(E) §1's "green without its predicate" list gains a third, subtler member.**
>   `canonical_freshness` checks **stamp-vs-commit-date, not content accuracy** — the doc was factually
>   wrong for the whole period and the gate stayed green, *correctly*, because freshness is not
>   accuracy. Reading "freshness gate green" as "the doc is current in substance" is reading a
>   predicate the gate does not compute.
> - **(F) Two hub-side items land on THIS repo, not the target.** The commissioned fleet-methodology
>   intake **exists only as a file and must be placed in the hub's `docs/intake/` or it is lost**; and
>   commission I asks whether two hub handoff-tooling defects were ever filed. **Partially discharged
>   this session:** the probe-tokenizer dotfile blindness **is** filed as hub `[#421]`, and this
>   session found a **second variant** of the same tokenizer defect (a backticked `#id` in a probe's
>   source column is parsed as a markdown anchor) plus **confirmed** the `assemble_paste` partial
>   cold→FILLED reflow — it flipped its own framing sites in this very bundle and left seven
>   hand-authored ones contradicting them, swept by hand. Neither is filed yet.
>
> Also carried by the supplement and worth reading directly: a **do-not-relitigate list** (§3, nine
> items with reasons) and an explicit **architect-seat calibration** — six named browser-seat errors,
> two of which *reproduced the window's own defect class inside the auditing artifacts*. Treat
> browser-seat pointers as claims to verify. **On any number, the probes outrank both this residual and
> the supplement.**

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
> **The FILLED supplement upgrades this into a testable rule — see correction (A) above: discharge a
> non-delegable item BEFORE opening any CC lane. Read it before following the ordering below.**

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

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS are folded into `PASTE_THIS.md`, so the incoming §13(d)
> operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*
> **Read the ANSWERS before the residual's §4 ordering — they correct it on load-bearing points**
> (see the corrections block at the top of `RESIDUAL.md`). The supplement wins on intent, priority and
> sequencing; the residual stays authoritative on *what the defects are*; **the probes below outrank
> both on any number.**
>
> **One caution specific to this supplement.** Its answers state a number of repo-state values (a HEAD
> sha, a test count, a checker summary line, task/theme counts, a next-free id) — beyond the
> interview's why-only scope (§13 "hard scope constraint"). They are committed **verbatim and
> unedited**, as the contract requires, but they are a **generation-time snapshot and are never
> trusted over the repo**: **P3, P6, P9 and P12** still govern those numbers and must be re-derived
> live. If a supplement value and a probe disagree, **the probe is right.**

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
operator-context beat fires (§13d) — NARROWED** (the supplement is FILLED — ask only *"anything changed
since it was written?"*).

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
   substring-matched. **Then run the operator-context beat (§13d) — NARROWED** (the supplement is
   FILLED — ask only *"anything changed since it was written?"*). Then run P2–P16, each against **live
   state now**.
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
   (HANDOFF_PROCESS §13); the supplement is **FILLED**, so its ANSWERS are folded into `PASTE_THIS.md`
   and the §13(d) beat **NARROWS**. Confirm by looking at the bundle directory in the hub — it is
   CC-side bookkeeping, not target state.

---

=== SUPPLEMENT.md ===

# Handoff supplement — ai-council window 2026-07-25 → 2026-07-26

**End state:** main `0e60320`, `## main...origin/main` clean and in sync, tree clean, only `main` locally, primary-only worktree, four `archive/cited-*` tags on origin. All seven gates EXIT 0 (`check.ps1` 891 passed). `SUMMARY: pass 4 | FINDINGS 0 across 0 rules | anchor-missing 0 | skipped(Unit2) 9 | errors 0`. `validate_backlog: OK (7 themes, 15 stories, 78 tasks, 0 warnings)`. Next free id `#127`; reserved `#107` only.

**Known unanchored tail — the next session's FIRST act:** JOURNAL anchor for `4d4bd87`, `6ed4bbd`, `0e60320`. This is structural, not drift (see Q4.8).

---

## Plan vs actual

| Planned | Result |
|---|---|
| FLOOR F1 — #97 registry repair | ✅ gates (i)+(ii) met; ticket stays open |
| FLOOR F2 — ruling batch | ✅ nine rulings + four forks landed as BACKLOG records |
| FLOOR F3 — #112 + gc.auto | ✅ four commits rescued to pushed tags; gc.auto restored |
| PRIMARY P1 — Unit 1.5 harness | 🟡 #106 + #108 closed; #105 open, unscheduled |
| PRIMARY P2 — guard measurement + ruling | ✅ exceeded — measured, rebuilt (#116), ADR-15 authored |
| SECONDARY S1 — unit (b) | ❌ specified, predicate pinned and approved, NOT started |
| SECONDARY S2 — record debt | ✅ renumber arc closed; #99 untouched |
| STRETCH T1′ — #100 | ❌ not started |
| **Lane O — #27, #55** | ❌ **not run** |

**Succeeded:** the checker went from 17 findings to 0 with **no suppression** — every finding was closed by fixing its defect. The canonical record is internally consistent and every ruling of the window is a repo record rather than a transcript.

**Failed, and this is the headline: all three standing axes moved ZERO.** Everything that landed is record hygiene and quality-control scaffolding. This is the second consecutive window in which the way-of-working goal consumed the entire window.

---

## 1. Strategic intent — the way-of-working goal for the next session

**Open the window on the work CC cannot do, and do not open a CC lane until it is discharged.**

The diagnosis, stated precisely because six windows of good intentions have not moved it: **all three axis-unblockers are non-delegable work.**

- `#27` — the operator reads twelve blinded pairs. Not a build.
- `#117` — one ruling: may a council-side stage ask the caller a question mid-run? Not a build.
- `#103` — the architect writes a design. Not a build.

Nothing CC can execute unblocks any axis. Meanwhile every defect in the backlog *is* CC-executable, so defect-driven ordering fills the window with them by construction. And once a CC lane is open, the architect's attention goes to directing it — which is exactly how `#103` was displaced this window after being explicitly promised.

This is the same structural blindness the previous supplement named about `#27` ("defect-driven ordering structurally cannot see an operator-blocked task"). It was named, and it happened again, twice over. **Naming it is not a mechanism.**

So the goal has two halves:

**(a) The sequencing rule, load-bearing:** a window discharges at least one non-delegable item — operator-gated or architect-owed — **before** any CC lane opens. Testable at close: did it?

**(b) The mechanism, if there is room:** `#102`'s ranked queue, with the axis items held in its top slots regardless of defect pressure, plus its leg (ii) session-close regroom advisory. Prose ordering has now failed six times; a queue that `validate_backlog` checks is the only version of "axes first" that survives a session boundary. **Cap it hard** — if `#102` threatens to eat the window, it drops. Half (a) is the load-bearing half, and the risk of (b) is precisely that it becomes this window's third consecutive methodology arc.

**Second, smaller goal: establish what a green signal's predicate actually is before trusting it.** Three separate greens this window did not mean what a reader would assume:

- rule 4's spec claims set-equality across **four** doc surfaces; `_adr_roster_docs` returns `("CLAUDE.md",)` — two surfaces, one direction. `ARCHITECTURE.md` and `docs/decisions/README.md` are never read by it (`#125`).
- `canonical_freshness` checks **stamp-vs-commit-date, not content accuracy**. ARCHITECTURE was factually wrong about ADR-15 for the whole period and the gate stayed green — correctly, because freshness is not accuracy. A reader who takes "freshness gate green" as "the doc is current in substance" is reading a predicate the gate does not compute.
- four **armed pre-commit gates** emit no output and assert nothing; a silently-degraded one passes every commit while checking nothing (`#126`).

**And the load-bearing observation: `FINDINGS 0` did not move before or after the ADR-15 roster repair.** A defective gate sat under a clean report the whole time and still would have. This is the window's own LESSONS class — *a value published without the predicate that produces it* — turning up inside the organ built to catch it.

---

## 2. Tensions weighed, and where they landed

**Mission vs scaffolding.** Landed on **capping the checker**: the seven remaining Unit-2 stubs (5/6/9/10/11/13/14) are HELD by architect ruling, registered and reporting SKIP so the coverage block keeps disclosing them. Reason: the checker already earns its keep on the drift classes that actually bit; the rest are speculative against a now-clean canonical surface. This is the first deliberate *stop building the tool* decision in the arc.
**Trade-off, stated:** rule 13 (ticket-reference resolution) is held, and it is the mechanised fix for the id-collision class that has now bitten **three times**. It is the stub most likely to be un-held first, and the trigger is written into `#97`: build the one rule, earned by the incident.

**Report vs gate (`#104`).** Landed: promotion is **per-rule**, on four criteria, and the checker was **not** promoted despite being promotable. Read report-wide, criterion (iii) produced an absurdity — a newly implemented rule finding a *real* defect would reset every already-clean rule's clock, creating a standing incentive not to add rules. Criterion (iv) was added because a reworded section heading yields `anchor-missing`, which only WARNs — so the audited document can silently un-gate the rule that checks it.
**Where it stands:** all four implemented rules restarted their clocks at the harness fix, so promotion is at least five first-parent commits away. The measured "rule 3 = 11, rule 4 = 11" was never credit — (iii) is conjunctive with (ii), and (ii) was never met by either rule: a dirty uncommitted config flips rule 3, a single untracked draft ADR flips rule 4.

**Fix vs suppress (`#112`).** Landed on rescuing the four commits into pushed annotated tags — thirteen of seventeen findings disappeared **because the defect was fixed**, not because a count was lowered. The gate on the decision was stated in advance as *content value, never finding count*; de-citing to quiet the checker was named as the laundering option and rejected. Each annotation carries its own retention predicate, so the tag explains itself without the ticket.

**Determinism vs recall (the rule-2 guard).** Landed on the resolution model (ADR-15) **after a measurement**, not before. My own first recommendation — key the guard on git's tracked set — was **withdrawn on the evidence**: `logs/` is gitignored, so as a *skip* predicate it would have silenced the single true positive rule 2 produced. The distinction that resolved it: git state as a **skip** predicate silences; as a **resolution** predicate it surfaces. Same data, opposite sign.
And the durable lesson, recorded in ADR-15: the frozen acceptance test **passed while the implementation was still wrong**, because it compared index to commit tree on a clean tree — and a clean tree is what repo policy *requires*. The acceptance compared two things policy guarantees are identical and could never have gone red. Caught by adversarial review, not by the contract.

**Parallel vs serial.** Landed on **serial**, after paying for the wrong answer. Three streams were scaffolded around what was, at every moment, one executable task; coordination cost exceeded the work. The three-condition rule applies to **work in hand, not paper plans**, and it needs a fourth condition: a shared **public signature** forces serial even when files are disjoint (paid for 2026-07-20 — three zero-shared-file lanes went RED on merge).

**Local fix vs upstream fix (`#111`).** Landed on **both**: the local divergence plus hub `#427`, with the hub ticket named as the divergence's explicit **retirement trigger** so it expires by reference rather than becoming a permanent record of a temporary condition. Hub-first alone was rejected (unbounded latency on a one-line local correction); an R2 allowlist entry was rejected because it hides the class rather than adjudicating it.

**CLI default — the premise that failed.** The incoming supplement carried "the operator ruled CLI is the default transport" as a load-bearing correction that reframed `#27` from a decision into a cost control. **It does not survive the repo.** ADR-12 §5 is unamended ("Until then `backend: api` remains the default everywhere"), and the code agrees: `seat_router.py:144` is the only path to `cli` and requires per-seat opt-in, while `config/settings.yaml` declares **no** `backend:` for any seat. The statement is **intent, not implemented state**. `#27` therefore keeps its original meaning as the authorizing gate, and the instrument needs no edit — rubric, margins and the twelve pairs stand as written.

---

## 3. Considered and rejected — do not relitigate

- **Widening the ARCHITECTURE allowed-edge set** to legalise cli.py's real 14-edge surface. The set is TARGET; `#92`'s decomposition shrinks reality toward it. Rewording a boundary to match a defect launders the defect.
- **Removing the rule-2 guard outright**, and **keying it as a skip predicate**. Both rejected on the measurement; ADR-15 records the full anatomy including why no measurement of the old guard could have predicted `_R2_RUNTIME_PATHS`.
- **Resolving `#118` by adding more bases.** Each base widens what silently resolves; the fourth (`docs/decisions/`) was already added under acceptance pressure. The fix is to declare the convention.
- **A checker rule for self-referential validation (v1).** It is a property of the *test suite*, not doc-vs-reality drift, and a rule detecting self-reference is very easy to write self-referentially. Homes are a LESSONS entry plus a collection-time assertion (`#115`).
- **A non-zero baseline / gate-on-new-findings for `#104`.** A baseline file is a hand-maintained artifact anchored to nothing — a never-expiring allowlist, the same defect as `_R2_ALLOWLIST`.
- **A separate ADR for the CLI default.** Ratification is an **ADR-12 §5 amendment** gated on `#27`. DRAFT-CLI-3 has no file vehicle — it lives as a §4 pre-draft in an intake file **with an empty evidence slot that only the parity sitting fills**. A new ADR would create two records of one decision.
- **Shipping `#100` alone.** The Contract-Version 1.1 cut is `#34` + `#76` + `#100`, versioned together — the ticket says so explicitly.
- **Mapping codex onto another vendor's API class (`#43`).** No-fallback sentinel: under ADR-03 blind voting a silent identity swap is worse than a hard failure, because the panel cannot see the substitution.
- **Renaming `docs/archive/` (`#56`)** — banner, not rename. **Dropping the `verify_*`/`validate_*` convention (`#109`)** — write it down. **DeepSeek as an open evaluation (`#6`)** — convert to watch W5. **Changing the emitter for ADR-34 (`#8`)** — exemption instead. **Keeping the `rounds:` pin (`#87`)** — drop it.
- **Re-homing a repo-local codex-review wrapper (`#73`)** — point at the global script; a repo-local copy re-creates the drift the ticket records.
- **Worktrees "blocked outright".** This inherited claim was **wrong as stated** and propagated unverified. The real constraint was the system-interpreter editable install leaking into every cwd (`#123`); the fix is a per-worktree venv plus the root `conftest.py` guard, and ai-council needs no `.worktreeinclude` today (tested).
- **`pytest -n auto`** in this repo (measured 1.42×, not worth it); **markdown-it-py** for the options scanner (`#80`/`#81` spike).

---

## 4. Open questions

1. **The ADR-11 decision-1 interactivity ruling (`#117`).** May a council-side stage ask the caller a question mid-run, or is Lane A fire-and-forget by contract? The structural fact either answer must survive: Lane A has **no ask-back channel** — the CLI blocks synchronously and speaks only exit codes and files — so "yes" costs a two-phase file protocol or MCP elicitation, and "no" costs the clarify loop. `#113`'s both exits are already named, so either ruling resolves it. **This is the single ruling that unblocks the boost axis's deferred half, and nothing has scheduled it for two windows.**
2. **`#27`'s outcome, and its consequence chain.** Unrun. Nested and easy to miss: if parity passes, ratification amends ADR-12 §5 — and `#43` also needs an ADR-12 amendment, so **sequence them together rather than opening ADR-12 twice**.
3. **Does `#102`'s queue reserve top slots for axis items, or rank purely by priority?** This is the mechanism question behind Q1(b). A purely priority-ranked queue re-creates the failure, because every axis item is P3 and the defects are P2.
4. **`#125`'s repair scope.** Does rule 4 grow to read all four surfaces, or is the spec narrowed? The ticket says explicitly *do not narrow the spec to match the code* — but the repair shape is unruled, and rule 3 already reads two docs, so the narrowness is rule 4's, not a harness limit.
5. **`#118`.** Declare the base-relative convention in ARCHITECTURE, or write the paths in full? Both are named; neither chosen. The required collision test — a doc citing a path that resolves only under an unintended base — is unwritten.
6. **`#124`'s direction.** Pin/cap mypy and google-genai, or fix `src/` against the newer APIs? The ticket calls this *a decision, not a default*, and warns against pinning to whatever the machine happens to hold, which would freeze the accident into the declaration.
7. **Do the seven held stubs stay held?** Rule 13 is the likeliest to be un-held (three id collisions and counting).
8. **The one-commit JOURNAL tail — accepted, or does ADR-85 change?** A JOURNAL entry cannot name the SHA of the commit containing it, because that SHA does not exist until the entry is written and writing it changes it. Every session's final commit is therefore unanchorable and inherited. Recorded on `#50`/W4 as construction rather than conduct. It also sharpens W4's real question: **the gate contributes one guaranteed anchor-only commit per session, so entries-per-substantive-change is depressed by the mechanism before any behaviour is measured.** A watch that does not subtract that would measure the gate and call it behaviour. Fleet question — hub `#423`'s neighbourhood.

---

## 5. Decomposition rationale — and what not to redo

**Why this shape.** The window was ordered **floor → harness → rules**, deliberately inverted from the incoming residual's ordering. Two filed follow-ups changed the frozen `Finding` interface, and every leg inherits it: fixing at four legs is cheap, at eleven it is a retrofit. That call held and is the reason `#106`/`#108` landed cleanly.

The record work ran as one batch, last among code work but before session end, because it is the **persistence mechanism** for everything decided in chat — the window's own closure criterion.

The checker was **capped rather than finished**. That is a deliberate stop, not an omission.

**Do NOT redo or re-decide:**

- **The fourteen-rule spec.** It lives inline in `#97` with earned-by traces per rule, and its id set was independently re-derived by sol from that line alone, agreeing at `{1..14}` with rule 12 identified as the non-leg exemption. Two blind derivations agreeing is what makes the denominator evidence rather than an echo.
- **ADR-15's resolution model** — the four declared bases, `_R2_RUNTIME_PATHS`, the `git ls-tree -r HEAD` vs `git ls-files` distinction, and the self-validating declaration rule.
- **`#97`'s held/scheduled split.** It now sums: implemented `{2,3,4,8}` + stubs `{1,5,6,7,9,10,11,13,14}` + structural `{12}` = 14; held `{5,6,7,9,10,11,13}` ∪ scheduled `{1,14}` = the stub set, intersection empty. It was wrong in **both** directions once and the arithmetic is what caught it.
- **The renumber arc** — closed; `#96` free; `#84`/`#85` live tasks; audits and JOURNAL deliberately untouched because they are append-only and correctly record the pre-renumber state.
- **The F2 batch** — nine rulings and four forks, all with reasons in-ticket. Two (`#8`, `#87`) are flagged **executor rulings, reversible while still BACKLOG records** and still await operator confirm-or-overturn.
- **`#112`'s tag rescue** and the `archive/cited-*` namespace.
- **Unit (b)'s predicate**, pinned and approved, verified against the real table: *a module is an entry in ARCHITECTURE's Modules table (lines 31–52), name from column 1, path from column 3; an edge is any import whose target is one of those enumerated modules, regardless of location.* `config` is the forcing case — enumerated but a top-level package outside `src/`, so a `src/`-scoped definition silently drops `cli -> config`, one of the edges rule 14 leg (b) exists to catch. Rule 1 and rule 14 leg (b) build as **one unit** because they share this definition, not merely enumeration machinery.
- **`#104`'s four promotion criteria** and the clock-reset reasoning.

---

## 6. Off-repo context

**The three axes, graded honestly.**

- **CLI (`#27`).** Zero. Seventh window. The instrument has been READY and unused for five days: twelve pairs, rubric inline, key sealed and gitignored, scoring **resumable in parts** — four pairs now and eight later costs nothing. The window's only contribution was proving on both surfaces that API is still the default, which killed a false inherited premise. That is clearing ground, not progress. And the structural point worth carrying: **DRAFT-CLI-3 is literally incomplete until this sitting runs** — it has an empty evidence slot that only the parity run fills. Six windows of slippage is not a ticket sliding; it is a hole in a decision document.
- **Boost / protocol.** Nothing built. `#117` gave the ADR-11 ruling an owner — real, but an owner is not a ruling. The theme's actual blocker for reaching another repo is `#100`: the contract describes its field set in **prose**, so a foreign caller has nothing to validate against. Correction to a claim the incoming supplement carried: **`#88` has no `#92` binding in its live ticket text** — it is independently schedulable. `#101` and `#113` remain genuinely bound (`#101` to the P2 arc, `#113` to `#117`).
- **Non-cognitive debate.** Zero, sixth window. `#55` — the matched-compute baseline, the **adjudicator of the entire debate bet** — untouched and operator-gated. `#103` is **architect-owed** and was not started: it is browser-architect work, not CC work, and it was displaced by this window's record and checker arcs. Owed, not dropped; the deferral reason I gave last window ("it competes with the ruling batch") **expired when the ruling batch landed**, and I did not act on that.

**Commissioned to the hub, and it exists only as a file:** a fleet-methodology intake assembling this window's fleet-level defects into ten commissions — environment/test isolation; session attribution and the multi-writer primary; the external-denominator principle; position-dependent template content; gate reproducibility; the parallel-work protocol; review routing; id-space and decision-record hygiene; handoff tooling defects; operational gotchas. ai-council records that it was raised (`#121`, `#122`, `#123`, `#124`, `#125`, `#73`, `#97`, `#116`, `#118`, ADR-15, LESSONS 2026-07-26 are its evidence refs), but **the document itself must be placed in the hub's `docs/intake/` or it is lost**.

**Never confirmed all window:** whether the two hub-side defects were actually filed — the probe tokenizer's dotfile blindness (*no probe in any bundle can currently bind to a dotfile, and dotfiles are where config gates live*) and `assemble_paste`'s partial cold→FILLED reflow. Carried as commission I: verify filed; file if not.

**Architect-seat errors this window, named so the next seat treats browser-seat pointers as claims:**
1. Propagated the inherited "worktrees blocked" claim without verifying it; one command settled it three turns later.
2. Asserted a "third unexplained mutation" of the primary from a misread of CC's **own reported merge**. The conclusion happened to be right — a genuinely unattributed checkout exists — but the evidence was wrong, and being right by accident is not a method.
3. Over-corrected under pressure rather than verifying: abandoned a position entirely when challenged, when the truth was that the constraint was real and only its stated mechanism was wrong.
4. Designed a merge bracket that **conflated "the hazard occurred" with "the operation never ran"** — it false-alarmed on first real use.
5. Authored a frozen acceptance contract that **could not go red** (index vs commit tree on a clean tree).
6. Six violations of the prompt-as-paste-artifact contract: destination as prose header instead of the block's first line; "plan mode" written into prompt text; an invented lane label (`Stream D`) that existed in no repo file, which made CC ask what its scope was; several prompts emitted at once.

The pattern in 4 and 5 is worth stating plainly: **I produced the window's own defect class inside my own artifacts, twice, while auditing for it.**

**Operator process corrections, now standing:** one CC prompt per turn, emitted and then waited on; the destination worktree/branch is the **first line inside the block**, never prose above it; no invented lane labels — worktree names are **ticket-derived** so CC reads scope from the backlog; plan mode is toggled, never written into prompt text; a new worktree means a new terminal; load-bearing numbers travel by file, not chat paste (three consecutive pastes arrived corrupted in transport).

**On ARCHITECTURE's stamp**, since it was queried: the copy circulated mid-window predates the ADR-15 repair. That repair updated the Governing-ADRs roster, the header's local ADR span to `ADR-01…15`, and re-stamped `last_reviewed` — verified by hand across five surfaces, because rule 4 reads only one of them. Note what this means for the next seat: **`canonical_freshness` green never implied the document was accurate**, only that its stamp was not older than its last commit touch. Those are different predicates and only one of them is checked.
