=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-17-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-17-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Plan the next way-of-working frontier after the 2026-07-16 CC-primary multi-arc close-out landed clean (ship-gate GREEN, `main` + `automation/fleet-audit` only). The open threads cluster around **fleet-governance maturation** — the fleet_parity checker exists but is only informational, and its promotion to a blocking gate is deferred behind an unresolved corp split-state — plus two lifecycle-doctrine decisions (a LESSONS chronological-archival split needing an ADR-29 reconciliation, and a codex-review global-infra consolidation). Orient (P1), take the operator-context beat (§13d, FULL — cold supplement), then **navigate from `BACKLOG.md`** — the load-bearing themes are E2/S8 (enforcement-transfer mesh: #336→#337), E3/S9 (#339), E6/S15–S16 (satellite onboarding fan-out), E7 (#338).<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-17-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-17-dev-knowledge-architect — the part the repo does not already encode

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
**All standing WARNs this window are pre-dispositioned in `ecosystem/disposition-register.yaml` — no NEW/undispositioned flag was introduced by the 2026-07-16 close-out.** Re-derive the live verdict/count/`[stale]` via P7 — do not trust this framing. The standing families, by reference (all carry register entries):

- **`no_ff_merges`** — three grandfathered direct-on-`main` commits (two 2026-06-19 journal/transcript, one 2026-06-26 freshness-wrap), each `warn-no-ff-*`-dispositioned; historical, pre-date the `block-ff-push` prevent organ.
- **`doc_rot` (backlog-accretion)** — the long-lived tickets `#262 / #278 / #328 / #332`, each `warn-doc-rot-backlog-*`-dispositioned; trimming is the standing kill-lever, not a gate failure. **Watch:** any edit that pushes another task past the 1200-char threshold mints a NEW WARN (the [[backlog-edit-doc-rot-threshold]] class) — keep task edits net-neutral.
- **`undeclared_edges`** — six `*-handoff-process` prose edges (`BACKLOG / VISION / ESSENTIALS / PLAYBOOK / SESSION_SETUP / AI_COUNCIL_PROCESS`), all `warn-undeclared-*` under `#241`; deferred structural work, not fresh drift.
- **`reconciled_versions`** — the `CONTRIBUTING-md-template.md` malformed-stamp WARN under `#335`, dispositioned.
- **`fleet_parity` (informational only — never a gate input, `#337`)** — its live `warn-undeclared` surface is corp-monorepo `precommit-hub-block` rev-vs-source_tag (the `#336` split-state), surfaced by `cmd_ship_gate` but NOT an `ALL_CHECKS` member. This is the thing standing between the fleet and a true zero-WARN state — hence the `#337` DEFER-peg on `#336`. Re-derive the live surface count via `python scripts/fleet_parity.py`.

**Disposition hygiene:** if the next session CLOSES a task that owns a doc_rot disposition, remove the register entry in the same arc or P7 prints a `[stale]` line (the [[close-backlog-orphans-disposition]] class).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail lives in `JOURNAL.md` (2026-07-16 entries) and `BACKLOG.md`; this is pointers only.

- **`#328` / `#332` fleet_parity checker + data plane** (ADR-101 in-file amendment) — `scripts/fleet_parity.py` + `ecosystem/{parity-surfaces,dependency-baseline}.yaml` + hub `.methodology.yaml`; both stay **OPEN** (consumer-side deploy carrier unbuilt). Merges `2bc02196` (build) → `3a2086`-era surfacing.
- **`#337` fleet_parity → informational ship-gate surface** — wired into `cmd_ship_gate` as a visible-every-ship, never-a-gate-input line (fail-open widened to `except Exception`); the **promotion-to-blocking** is the filed `#337`, DEFER-pegged on `#336`.
- **`#336` filed** — corp hub-block v1.3.1-vs-v1.2.0 split-state reconciliation (leg-1 deferral, operator-ruled: do not touch the record/pin this arc).
- **Satellite onboarding rulings** — `ecosystem/satellite-onboarding-rulings.yaml` + advisory validator + 4 ready onboarding prompts (`docs/intake/2026-07-16-*`, intake #15); all 4 satellites FULL (life-architect FULL overrides the census floor-only). **Prompts ready but UNFIRED** — operator fires per rollout order.
- **`#333` closed → `#338` filed** — codex-review doc-lane + §16 model re-pin shipped; the 5 residual drift items folded into `#338`.
- **`#339` filed (PROPOSED)** — LESSONS legacy-split ruling recorded in `LESSONS.md`; pending an ADR-29 amendment (chronological archival split ≠ ADR-29's rejected by-topic split).
- **`#254` closed** — fleet-audit data-branch organ (both parts verified; `origin/automation/fleet-audit` pushed, NOT merged — orphan organ stays separate).
- **CLAUDE §1 first-read diet** (v2.41) — PLAYBOOK demoted to on-demand reference; owner=hub region + `templates/claude-regions/first-read.md` in lockstep.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The open way-of-working questions, in rough dependency order. These are **decisions to make**, not tasks to execute — the execution tickets already exist in `BACKLOG.md`.

**1. The shared blocker: sequence the consumer/satellite onboarding wave (E6/S15–S16).** Several DEFER-pegs converge on one un-happened thing — *consumer-side deployment actually running*: `#337` (fleet_parity → blocking) is pegged on a true zero-WARN fleet, `#293` (consumer runbook fan-out) is pegged on Wave-1 onboarding, `#332`'s Done-when includes a deploy carrier. The 4 satellite onboarding prompts (intake #15) are **ready but unfired**, and the operator holds the rollout order (corp-ops → corp-sca → life-architect → demo-prep). **Decision:** does this session's plan fire the wave (unblocking the peg-cluster), or does it advance the hub-side design first? The tension is *breadth-first onboarding* (unblock the mesh) vs *depth-first hub hardening* (get the checker/gate right before it fans out). Note the hard guardrail: CC does not write into consumer trees (ADR-36/41) — the fan-out is per-repo operator-run, not a hub push.

**2. fleet_parity maturation — the split-state modeling call (`#336`, E2/S8).** `#336` is the concrete design decision, and it is the sole thing standing between the fleet and zero-WARN. Two named options: (a) **model enforcement-gate-rev separately from corpus `source_tag`** in `parity-surfaces.yaml` (touches the `#328` checker + the MUST/non-waivable branch — a schema change that recognizes "gate uplifted ahead of a full redeploy" as a legitimate, declarable state), or (b) **schedule a real v1.3.1 corp redeploy** (but full redeploy re-appends the `codemap-freshness` hook corp deliberately removed, #276 unlanded). All three naive fixes (record-stamp / full-redeploy / pin-revert) are ruled wrong — see the `#336` body. **Decision:** (a) vs (b), and whether the answer generalizes into a durable parity-surfaces concept (gate-rev ≠ corpus-rev) rather than a one-off patch.

**3. LESSONS lifecycle — the ADR-29 reconciliation (`#339`, E3/S9).** The ruling (recorded in `LESSONS.md`, 2026-07-16) proposes a **chronological** legacy split (move a contiguous older block byte-unchanged into `LESSONS-legacy-<period>.md`, leave a pointer) — which is **distinct from the by-topic split ADR-29 rejected**, so it stays UNsanctioned until ADR-29 is formally amended/superseded. **Decisions:** (i) the split *threshold* — a hard line/entry count vs the softer navigation-pain trigger; (ii) whether a read-only helper enumerates the split boundary; (iii) draft the ADR-29 amendment that sanctions chronological-but-not-topical archival. This is the append-only-record doctrine (ADR-29/39) meeting a real navigation-scale problem.

**4. codex-review consolidation — the global-infra question (`#338`, E7).** Five folded items; the load-bearing one is **(c): bring `~/.claude/bin/codex-review.ps1` + the `/codex-review` command under version control / a deploy carrier.** This is per-machine, un-versioned global infra → it needs a **core-invariant #6 ruling** (global-infra edits are exception-with-ruling, never unilateral). The meta-question: *how does fleet methodology take ownership of per-machine Claude Code runtime config* — the same class as `#289` (OneDrive-guard should be hub-owned). Also live: (a) config default `sol` vs doctrine `terra` (because the code path passes no `-m`), and (e) the `.ps1` sandbox-halt vs the native `codex exec review --base` path.

**Cross-cutting:** the through-line is the ecosystem crossing from **hub-only enforcement to a fleet/satellite mesh** (ADR-28 Layer-2 governing all of `Dev/`). Questions 1, 2, and 4 are all facets of "how does the hub's methodology reach and stay in-sync with N consumers without the hub reaching into their trees." A standing older thread worth a decision if bandwidth allows: **`#162`/S1** — the "architect" actor-vs-mode vocab collision is still live (the model decision, not just the boot-ack slice).
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
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-17-architect`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-17-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-17-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-17-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

ANSWERS — outgoing browser architect (authored by the browser architect;
CC transcribes verbatim). 2026-07-17.

1. STRATEGIC INTENT — Move fleet structural governance from SEEN to
EXPLAINED → ENFORCED → UNATTENDED → REPLICABLE, working ON the census
document of record (docs/audits/2026-07-16-technical-fleet-structure-
census.md), never around it. Operator doctrine, binding: a PASS verdict
without a recorded WHY is not governance — every root-level divergence
(.claude layout, .github, assets, config, каждая) must carry a machine-
readable reason; the consolidated model must then deploy automatically onto
a new repo (correct-by-default scaffold), run unattended nightly, and only
then be optimized. Each repo stays hermetized in its own way of working —
uniformity is never the goal; explained, declared, enforced divergence is.

2. TENSIONS WEIGHED — (a) uniformity vs product-local hermetization: held
DECLARED-WITH-REASON; census category (b) is nearly empty — the discipline
is current. (b) teeth-now vs teeth-after-zero: promotion (#337) stays
pegged on #336, never a date. (c) #336 split-state: mechanism over stamp —
record-stamp rejected as over-claim; schema remodel is the path.
(d) verdict-labels vs operator's WHY-ask: verdicts alone ruled
insufficient; the ownership+reason axis (#316) is elevated to the cycle's
centerpiece. (e) canonical-doc content: stays repo-authored except floor +
Form-A regions (#312); the boundary formalization is #316's file-set grain.
(f) tool caches: on-disk presence is runtime noise (local test runs);
the governed surface is gitignore effect — AT-PARITY fleet-wide; do not
re-open as structural drift.

3. CONSIDERED + REJECTED — record-stamp / full-redeploy / pin-revert for
#336 (over-claims corpus / re-appends the #276-removed hook / discards
#318-#319 uplift) → ticketed remodel instead. Verbatim hub Rule-A carry to
consumers (would brick dev under src/, data/, council_inbox/) → per-repo
sanctioned set DERIVED from the manifest (P2 shape). Ultracode auto-
orchestration for night batches → self-orchestrated Task fan-out per our
own doctrine (explicit shape, haiku walkers / sonnet probes / opus
orchestrator). A dedicated .vscode policy row before the e1 ruling →
generic root-sweep + declared LOCAL with forcing shelf-life. Any greenfield
mechanism → barred; every arc maps to a filed ticket (#306/#316/#324/#336/
#337). Codex --yolo: operator-ruled IN for overnight legs, review/
derivation ONLY, never edit authority — accepted-risk posture, do not
relitigate.

4. OPEN QUESTIONS (operator) — P4a .vscode e1: durable LOCAL vs fleet
template (architect rec: LOCAL; shelf-life 2026-08-13 forces it). P4b
ai-council .claude/skills/ (#308): adopt minimal vs waive (rec: adopt —
FULL-profile consistency). #336 schema shape (separate enforcement-gate-rev
axis) — the design fork inside P1's first arc. Extend #316's Done-when
with a per-entry reason: field (the operator's "answers for everything,
tracked" — recommended: fold it in). Satellite prompts (intake #15) ready,
UNFIRED — operator fires per rollout order. #338/#339 scheduling; W3-13
operator-present. BACKLOG grooming probe: operator wants every open item
verified live / dead / awaiting-ruling at next boot.

5. DECOMPOSITION RATIONALE — serialize around the manifest (both #336 and
#316 touch parity-surfaces.yaml): (1) #336 schema remodel → clears the sole
WARN; (2) #337 promotion to blocking ALL_CHECKS; (3) #316 ownership+REASON
axis (unblocks #329 viz) — the operator's management-system centerpiece;
(4) #306 consumer tree-seal (sanctioned set derived from the enriched
manifest, so it follows #316); (5) #324 nightly runtime LAST — it consumes
everything above into the walk → verdict sheet → morning prompt. P4
rulings slot anywhere. NOT redo / NOT re-decide: the census's divergence
classifications and coverage audit (sol-derived, terra-reviewed); ARC-A/B
declarations + shelf-lives; satellite tier rulings (all FULL); W3-16
no-op closures (fleet is LF — proven); merge/push execution delegation
(PLAYBOOK Ch8); TARGET-REPO guard; ADR-65 grooming discipline (done tasks
leave — the operator has re-confirmed this expectation).

6. OFF-REPO CONTEXT — Operator's strategic ladder, verbatim intent:
explain → consolidate → document → deploy automatically onto other repos →
manage → optimize; the census is the working document for it. Codex
registry healthy (sol 36-point derivation + terra doc-lane both clean on
the census); native codex exec is the working path, .ps1 wrapper halt is
#338(e). Corp product-architect browser chat: payload printed by corp CC,
NOT yet booted — operator's move. CC effort settings persist across
sessions (operator reminded to reset after high-effort night runs).
Operator hard rule (new, 2026-07-16): zero invented filesystem paths —
every emitted path must come from a quoted governance source or be
delegated to CC to derive from primary sources; hyphen-only naming.
