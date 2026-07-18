=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-18-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-18-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Run **ARC 4 — fleet equalization**: bring the Wave-1 consumers (corp-monorepo, ai-council) into methodology parity with the hub, harvesting their lessons before propagating. The **first move is the ADR-36/41 amendment** codifying the consumer-write mechanism (RULING-W: worktree/branch → report, mechanism before act) — no equalization edit into a consumer tree precedes it; re-witness each consumer live first. Read `SUPPLEMENT.md` ANSWERS (seven operator rulings, verbatim) and `PLAN.md` (plan-of-record) before starting; task-graph in `BACKLOG.md` (#344, #341/#338, #339, #342, #343, #300 + the 15 night-triage findings).<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-dev-knowledge-architect-2026-07-18`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-18-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED** with this session's operator rulings (transcribed VERBATIM — RULING-W/S/PY/CF + the `#329` and `#341-R2` inputs + the satellite freeze). Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*. **Read the SUPPLEMENT ANSWERS first** — they are the binding off-repo "why" for ARC 4 that the repo structurally cannot carry.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Every standing WARN this window is pre-dispositioned in `ecosystem/disposition-register.yaml`; the 2026-07-18 serial-integration close-out introduced no NEW undispositioned flag** — `#337` merged ship-gate-GREEN and the one new WARN it surfaced (`#344`) was dispositioned in the same arc. Re-derive the live verdict/count/`[stale]` via P7 — do not trust this framing. The standing families, by reference (all carry register entries):

- **`no_ff_merges`** — three grandfathered direct-on-`main` commits (`warn-no-ff-3a894eeb5` / `-d0f9ead67` / `-533109f`), each dispositioned; historical, pre-date the `block-ff-push` prevent organ. This window's four integration merges were all `--no-ff` — no new direct-on-`main` commit.
- **`doc_rot` (backlog-accretion)** — the long-lived tickets `#262 / #278 / #328 / #332`, **plus NEW-this-window `#344`** (`warn-doc-rot-backlog-344`, `review_date: 2026-08-18` shelf-life — the `#332` A0-seal precedent for a load-bearing NEEDS-RULING task condense-deferred). Trimming is the standing kill-lever, not a gate failure. **Watch:** any edit pushing another task past the 1200-char threshold mints a NEW WARN (the [[backlog-edit-doc-rot-threshold]] class) — keep task edits net-neutral.
- **`undeclared_edges`** — six `*-handoff-process` prose edges (`BACKLOG / VISION / ESSENTIALS / PLAYBOOK / SESSION_SETUP / AI_COUNCIL_PROCESS`), all `warn-undeclared-*` under `#241`; deferred structural work, not fresh drift.
- **`reconciled_versions`** — the `CONTRIBUTING-md-template.md` malformed-stamp WARN under `#335`, dispositioned.
- **`fleet_parity` — CHANGED THIS WINDOW: it is now a BLOCKING `ALL_CHECKS` member (`check_fleet_parity`, `#337`), no longer the informational-only surface the last bundle described.** Its verdict→status map: FAIL on refused/must-absent/tombstone-violated, WARN→RED on warn-undeclared/unavailable/tracked-ephemera; stale-declaration + advisory-rewarn stay advisory-but-visible (a date/corpus advance never REDs). The promotion REDs nothing live today (STOP-condition honored at merge). The one live `warn-undeclared` parity surface remains corp-monorepo `precommit-hub-block` rev-vs-`source_tag` — the `#336` split-state, the sole thing between the fleet and a true zero-WARN steady state. Re-derive the live surface via `python scripts/fleet_parity.py`. **Perf note:** the walk (~8.3s in-process) now runs on every hub pre-commit via `audit.py health`; scoping it to ship-gate-only is the filed `#343` (RIDER-2 follow-up).

**Disposition hygiene:** if the next session CLOSES a task that owns a doc_rot disposition (e.g. `#344` on a ruling, or `#328/#332` on the deploy carrier), remove the register entry in the same arc or P7 prints a `[stale]` line (the [[close-backlog-orphans-disposition]] class).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail lives in `JOURNAL.md` (2026-07-18 entries) and `BACKLOG.md`; this is pointers only. This was a **serial-integration close-out** (the day's parallel work landed to a quiet primary), not a build session.

- **`#337` CLOSED — fleet_parity promoted to a blocking `ALL_CHECKS` member** (ADR-101 data plane; ADR-102 gate-rev axis). `check_fleet_parity` + the extracted `fleet_parity.walk()` seam; `ALL_CHECKS` 29→30, doc-counts regen (30 checks / final suite **1595 passed / 3 skipped**), ARCHITECTURE status flip + re-stamp. Merge `--no-ff` **`6673904f`**. One codex-terra P1 (bare `import fleet_parity` broke package-mode `python -m scripts.audit`) fixed pre-merge.
- **corp-monorepo architect handoff integrated** — the hand-authored cross-repo bundle (`docs/handoffs/2026-07-18-corp-monorepo-architect/`), merge `--no-ff` **`7ff9b89e`**.
- **ai-council P6-window handoff integrated + `#343`→`#344` cross-session renumber** — the ai-council session's session-close-gate filing collided with main's `#343` (fleet_parity ship-gate scoping); renumbered to `#344`, BACKLOG auto-merged clean (0 dup ids). Merge `--no-ff` **`1eeea5fb`**.
- **`#344` `doc_rot` dispositioned** — load-bearing NEEDS-RULING task, `review_date: 2026-08-18` shelf-life (`#332` A0-seal precedent). Merge `--no-ff` **`54c502fc`**; session-close JOURNAL anchor `3571bd5c`.
- **Filed this window:** `#343` (fleet_parity ship-gate-only perf scoping, RIDER-2) · `#342` (fleet_parity gate-ahead max-fidelity hardening, deferred #336/ADR-102 items). Branch hygiene: every stale/merged branch deleted; **survivors = `main` + `automation/fleet-audit` only**, primary worktree only, no orphan dirs.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The plan-of-record for the next session is ARC 4 — fleet equalization** (the operator-approved prompt file, operator-held off-repo; encoded in `PLAN.md`). Several standing DEFER-pegs converge on one un-happened thing: the hub's methodology actually reaching and equalizing across the consumer repos. **This window landed the operator rulings that unblock it** — they travel **verbatim in `SUPPLEMENT.md` ANSWERS** (RULING-W/S/PY/CF, the `#329` and `#341-R2` inputs, the satellite freeze); read those first, they are the off-repo "why" the repo cannot carry. The open decisions, in rough dependency order:

**1. ARC 4 fleet equalization — and its enabling mechanism (RULING-W).** The equalization work requires the hub to WRITE into consumer trees (methodology/cleanup), which the current ADR-36/41 read-only contract forbids. **RULING-W resolves this: the hub MAY/SHOULD write into consumers via a separate worktree/branch, then report — and the FIRST step of ANY consumer leg is to codify this as the ADR-36/41 amendment (mechanism before act).** So the next session's opening move is not an equalization edit; it is the amendment. **Guardrail preserved:** re-witness consumers live first (their state may have moved), and every consumer write goes worktree/branch → report, never a direct push into a consumer checkout.

**2. `#344` — session-close gate + consumer hub-write guard (NEEDS-RULING).** Ask 1 (a pre-handoff gate refusing bundle generation until session-close criteria hold — audit artifact + doc-currency + operator close-token) and Ask 2 (a consumer-side PreToolUse guard blocking Writes that resolve under a hub/global path). **RULING-W is the doctrinal complement to Ask 2** — it defines the *sanctioned* consumer→hub write path (worktree/branch + report + mechanism-first), so Ask 2's guard should ALLOW exactly that shape and block the unmediated case. The `block-onedrive` guard is the mechanical precedent (`#289`).

**3. `#341` — Codex producer-lane activation. FORK NOW CLOSED by the R2 ruling.** The prior bundle flagged an open fork (per-run codex flag vs repo-local `AGENTS.md` override); **the operator ruled R2: producer-activation = a sanctioned repo-local `AGENTS.md` override (the per-run flag is REJECTED), decided on witnessed precedence evidence.** Remaining `#341` work is implementation, not decision: witness the `AGENTS.md` precedence once, codify the producer guardrails, reconcile PLAYBOOK §16 + the EPIC-H carve-out. Paired reviewer-path drift is `#338`.

**4. Governed-file structure — RULING-S.** Every governed file gets **reader-visible sections** separating methodology-universal from repo-personal content (CLAUDE.md + configs); **machine markers alone are insufficient** — this is the load-bearing constraint on the existing `owner=hub`/`owner=repo` region work (`#312`). The editor-side complement is the **`#329` input**: background decoration of the marked regions via versioned `.vscode` (grey/navy on a dark theme). These are two halves of one "make the hub/repo boundary legible to a human reader" thread.

**5. Standing build queue (execution tickets exist; these are the way-of-working decisions inside them).** `#339` LESSONS legacy-split BUILD leg (threshold + mechanism; still pending the ADR-29 chronological-archival amendment — the ratification landed in the docs, the executed split is the build leg). `#342` fleet_parity gate-ahead max-fidelity hardening (3 items, deferred from #336/ADR-102). `#343` fleet_parity ship-gate-only perf scoping (RIDER-2; the ~8s walk should not tax every pre-commit). `#300` hermetization residual (d.i runbooks / d.ii mode-boot home / d.iii audit-class grammar — DEFER-pegged BEFORE Wave-2). **RULING-PY:** the ruff baseline targets **py311 now** (the corp floor); the standing "always newest Python" direction becomes a filed **fleet-upgrade ticket** (not yet filed — a next-session filing). **RULING-CF:** ai-council adopts the conformance workflow.

**6. The frozen lane — satellite wave.** The 4 satellite onboarding prompts (intake #15) stay **FROZEN until corp + ai-council lessons are extracted** (operator ruling this window). Do not fire the satellite rollout; the Wave-1 consumers (corp, ai-council) are the lesson source ARC 4 harvests first.

**Cross-cutting through-line:** the ecosystem is crossing from **hub-only enforcement to a fleet mesh** (ADR-28 Layer-2 governing all of `Dev/`). RULING-W is the pivot — it converts the read-only hub into a hub that can *equalize* consumers under a mechanism-first discipline. Questions 1, 2, and 4 are all facets of "how the hub reaches and stays in-sync with N consumers, legibly, without unmediated tree-writes." A standing older thread if bandwidth allows: **`#162`/S1** — the "architect" actor-vs-mode vocab collision (the model decision, not just the boot-ack slice).
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
> **Branch note.** This bundle was generated on branch `docs/handoff-dev-knowledge-architect-2026-07-18`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-18-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-18-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-18-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

ANSWERS — outgoing architect (2026-07-18 serial-integration close-out session)

These are OPERATOR RULINGS made in the outgoing chat and transcribed VERBATIM —
they exist only in chat and must travel. Read them as the binding off-repo "why"
for ARC 4; the schema mapping below is secondary to the verbatim text.

RULINGS (verbatim):

- RULING-W: hub MAY/SHOULD write into consumer repos for methodology/cleanup —
  separate worktree/branch, then report; FIRST step of any consumer leg = codify
  this as the ADR-36/41 amendment (mechanism before act).

- RULING-S: every governed file gets READER-VISIBLE sections separating
  methodology-universal vs repo-personal (CLAUDE.md + configs; machine markers
  alone insufficient).

- RULING-PY: ruff baseline targets py311 now (corp floor); standing direction
  "always newest Python" -> file the fleet-upgrade ticket.

- RULING-CF: ai-council adopts the conformance workflow.

- #329 design input: editor-side background decoration of owner=hub/repo regions
  via versioned .vscode (grey/navy on dark theme).

- #341 R2 ruling: producer-activation = sanctioned repo-local AGENTS.md override
  (per-run flag rejected, witnessed evidence).

- Satellite wave: still FROZEN until corp + ai-council lessons extracted.

--- schema mapping (CC framing of the verbatim rulings above; the rulings are authoritative) ---

1. STRATEGIC INTENT: run ARC 4 — fleet equalization. Bring the Wave-1 consumers
   (corp-monorepo, ai-council) into methodology parity with the hub, harvesting
   their lessons first. RULING-W is the enabling doctrine: the read-only hub
   becomes one that can WRITE into consumers under a mechanism-first discipline
   (worktree/branch → report). The way-of-working goal is the ADR-36/41 amendment
   that sanctions this — it is the FIRST step of any consumer leg, before any
   equalization edit.

2. TENSIONS WEIGHED: breadth-first onboarding vs depth-first hub hardening —
   resolved toward equalizing the two Wave-1 consumers before firing the satellite
   wave (which stays FROZEN until their lessons are extracted). Mechanism-before-act
   (RULING-W) over expedient direct writes: the amendment lands before the edits.
   Machine markers vs human legibility (RULING-S) — resolved that reader-visible
   sections are REQUIRED; the owner=hub/repo comment markers are necessary but not
   sufficient, and #329's editor decoration is the complementary human-facing half.

3. CONSIDERED + REJECTED (do not relitigate): a per-run codex profile/flag for
   producer activation — REJECTED in favor of a sanctioned repo-local AGENTS.md
   override, on witnessed precedence evidence (#341 R2). Firing the satellite
   onboarding wave now — REJECTED (frozen until corp + ai-council lessons land).
   Unmediated hub→consumer or consumer→hub tree writes — REJECTED; the sanctioned
   path is worktree/branch + report (RULING-W). Chasing "always newest Python" as an
   immediate baseline bump — deferred to a filed fleet-upgrade ticket; the ruff
   baseline stays py311 (corp floor) for now (RULING-PY).

4. OPEN / DEFERRED: #344 session-close gate + consumer hub-write guard
   (NEEDS-RULING — Ask 1 pre-handoff gate, Ask 2 consumer-side PreToolUse guard;
   RULING-W defines the sanctioned write path Ask 2 must allow). The fleet-upgrade
   ("always newest Python") ticket is not yet filed. #300 hermetization residual
   (d.i/d.ii/d.iii) pegged BEFORE Wave-2. #339 ADR-29 chronological-split build leg.
   The #162/S1 architect actor-vs-mode vocab collision, standing.

5. DECOMPOSITION RATIONALE: ARC 4 opens with the ADR-36/41 amendment (RULING-W,
   mechanism-first) — NOT an equalization edit — then re-witnesses each consumer
   live before touching it. The reviewer-path (#338) and producer-path (#341) are
   disjoint codex threads; #341's activation decision is already made (R2), so it is
   build, not design. Do NOT re-derive the producer-activation mechanism (repo-local
   AGENTS.md, ruled) or re-open the satellite freeze.

6. OFF-REPO CONTEXT: the ARC 4 prompt file is operator-held (approved, off-repo).
   Re-witness the consumers first — their state may have moved since the last window.
   All seven rulings above are this session's binding operator input and exist only
   in chat; they are the reason the equalization arc can proceed at all.
