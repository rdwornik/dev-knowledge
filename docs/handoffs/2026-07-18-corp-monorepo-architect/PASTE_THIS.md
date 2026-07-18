=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode · corp-monorepo)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-18-corp-monorepo-architect` |
| **Chat title** | `[corp-monorepo] Technical Architect — 2026-07-18-corp-monorepo-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / decomposition posture; the session's WORK is product) |
| **Target repo** | **corp-monorepo** — this bundle lives in the hub `.dev-knowledge` (ADR-36/42: the hub is the sole handoff carrier; consumers hold no `docs/handoffs/` surface). **Run every probe command IN the corp-monorepo checkout.** |
| **Purpose** | Resume **PRODUCT architecture** in corp-monorepo — decompose + sequence the next arc. The last window CLOSED clean (Arc-B `#19–23` · Arc-C Wave-1 `#25/#26/#27` · E5-registry design · the night process audit — RESIDUAL §2). The live architectural call is the ordering of the **SIM-1 gap-fill day-arc** vs the **E5 build** (`#35→#38→#40→#36`), under the A3 R10 knowledge-loop-before-RFP priority (RESIDUAL §4). Navigate product work via the corp `BACKLOG.md` E1–E7 story-map. Methodology questions route to the **hub** (corp is A0-closed), not this chat. |
| **Generated at** | Hand-authored in the hub from **READ-ONLY live git** of `../corp-monorepo` (hub is the carrier; no write ever touches the consumer). States **no** sha / count / verdict — **re-derive HEAD / tree / branch / ahead-behind live in the corp checkout** (`PROBES.md` P1). |

> **`SUPPLEMENT.md` is EMPTY (cold handoff).** No single outgoing chat carried this session's strategic *why* — the last window's work was CC-side across executor + integration + audit sessions. ANSWERS is committed empty: the defined cold-handoff disposition, not a defect; the incoming §13(d) operator-context beat fires **FULL**.

> **Anti-bluff in effect (read `PROBES.md` header).** This bundle **withholds every probe answer value** by construction — no SHAs, counts, region text, or armed-state. The withholding IS the teeth; run the commands **in the corp-monorepo checkout**.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives **once** in the hub canonical runbook **`docs/handoffs/README.md`**. This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry **no per-bundle README** (HANDOFF_PROCESS §13).

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

# Residual — 2026-07-18-corp-monorepo-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **architect** (§13) — planning / decomposition posture; the session's WORK is **product**. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is EMPTY (cold handoff).** ANSWERS committed empty; the incoming §13(d) operator-context beat fires **FULL**.

---

## §1 — The headline: the plan is encoded; the architect resumes decomposition at the E5-build / SIM-1-gap frontier

**The product plan is fully in-repo and the last window CLOSED cleanly.** `witnessed` (READ-ONLY, at derivation): corp `main` is **clean and in sync with `origin/main`** — no unmerged product branches, one already-merged straggler (`docs/2026-07-18-manifest-doctrine-closeout`, deletable on the operator's OK). The A3 target-architecture ruling (R1–R10, `docs/audits/2026-07-17-a3-target-architecture-ruling.md`) still governs; the integration-protocol ruling is **CLOSED**; the **NOT-list (no microservices, no service mesh, no message bus)** is binding at solo-operator scale.

What a fresh architect chat lacks — and the ONLY thing this residual carries — is the **entry point + the decomposition frontier + the design "why,"** none of which the repo re-narrates:

- **Entry point.** The corp **execution charter** `docs/audits/2026-07-17-execution-charter.md` is still the single consolidated reading map (its §2 reading map points to every canonical doc). Read it first; everything below is a pointer INTO it, not a copy.
- **Role split (does not live in the repo).** This browser chat is the **TECHNICAL ARCHITECT** (Layer-1, no file access) — it decomposes the next frontier into a task-graph, holds the whole-system view (A3 + `ARCHITECTURE.md`), and reviews each arc's plan before execution (one plan-review output-contract form: the exact CC option / paste-ready feedback / `approve`). The incoming Claude Code session is the **executor** (Layer-3, holds the tree). The architect does **not** execute. Methodology questions route to the **hub** `.dev-knowledge` (corp is A0-closed), **not** this chat.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or region text — those are the probes' live answers.

---

## §2 — Pending / shipped this window (pointer, not re-narration)

**SHIPPED since the last handoff (2026-07-16→18; detail lives in the corp `JOURNAL.md`, not recapped here):**
- **Arc-B signed deletions** `#19–#23` — MERGED+PUSHED, close-out package delivered (`corp index rebuild`: B2 facts residue cleared, `facts_count=0`).
- **Arc-C Wave 1 canonical homes** `#25`/`#26`/`#27` — MERGED (LLM-JSON→`schema.utils`; frontmatter→`vault_io`; a new `schema/model_pricing.py` built from the live per-provider dicts). **Deletion-candidate lists** for the now-unused old copies live in those commit bodies → they **feed the NEXT signed deletion manifest** (Arc-C wave 2). The new `docs/templates/deletion-manifest-template.md` (closing-sweep) codifies the manifest doctrine: column-granularity consumer enumeration before a KILL; runtime-claim kills default PROPOSED-GATED.
- **E5 registry foundation design** — Lane B doc MERGED (doc-only, **no task closed**): `docs/intake/2026-07-17-tech-e5-registry-foundation-design.md` (intake-id 16). Key corrected semantics: **`#35` is the `ContentRegistry` routing gate, not the FR-10 registry** — the FR-10 URL/source registry is `#38`/`#40`; build order **`#35→#38→#40→#36`**. Open design decision points D1–D5 + Graph consent live in the design's §8.
- **Night process audit** (unattended, 2026-07-17→18) — `docs/audits/2026-07-18-process-audit.md`. **The spine WORKS end-to-end** (ingest → deep knowledge note → cited RFP draft, ~$0.045 surfaced). It surfaced a **SIM-1 gap list** (the real product-quality frontier, see §4): retrieval is **metadata/title-only** (no body FTS), the **facts pipeline is absent** (`facts_count=0` at all consumer sites), **ingest hard-crashes** on a fresh env without `<mywork>/.corp/content_registry.yaml`, and the **project↔vault link + client propagation** is missing. Two DISCLOSED read-only real-MyWork leaks (F18 `project_resolver` roots, F26 `com` lane) — no writes, SHA-256 baseline held.

**PENDING — no unmerged product branches.** `witnessed`: corp `main` carries no open feature/fix lanes at derivation (the two worktree lanes were integrated + torn down 2026-07-17). The only non-`main` branch is the merged straggler above.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — the architect's job this session is to sequence and decompose the next product arc.** Two candidate frontiers are both ready and the ordering is the live architectural call (§13(d) captures the operator's priority):

1. **The SIM-1 gap-fill "day-arc"** (from the night audit). The 07-18 JOURNAL is explicit: *"the day-arc launches as a FRESH executor session on the senior's formal prompt (authored from the HUB session, not here)"* — i.e. **this architect chat authors that executor prompt.** The ranked queue: (1) ingest content-registry fallback+bootstrap [F1]; (2) note-body FTS **or** wire the facts pipeline [F6/F7]; (3) project↔vault link + client propagation [F16/F9]; then the missing **Content-Manifest producer** (SIM-1's one absent output — the T6 corp↔consumer seam). SIM-2: the `data/kb` RFP producer [F11], CKE tier/schema drift [F21/F22].
2. **The E5 registry BUILD** (`#35→#38→#40→#36`) — the design is ratified and merged; the build arc executes from it. **Graph API consent gates `#36`/`#40` live resolution** (operator queue, below).

**The R10 "why":** after the F0/E1–E2 substrate, the **knowledge loop (E5/E6) takes precedence over the RFP rewrite (E4)** — a conscious, recorded deviation from the intake's "build before gap-fill" order; the BACKLOG sequences themes E1→E2→E3→**E5→E6**→E4→E7 accordingly (theme *ids* keep identity, theme *sequence* carries priority). The SIM-1 gaps sharpen this: the spine runs, but retrieval quality and the facts pipeline are the gating weakness for the RFP output — which is exactly why the knowledge loop is elevated ahead of the RFP rewrite.

**CLOSED — do NOT re-open (charter §3, PROBES P4):** CKE is a subprocess with an explicit contract (R2, one invoker); accessors resolve through config incrementally (R6); the corp↔consumer seam is the T6 Content Manifest; seam contracts are guarded by N2-class seam tests. If an arc's plan reaches for an infrastructure tier (a service, mesh, or bus), the architect rejects it — a violation at 3-RFPs/month scale.

**Operator queue (off-repo — the §13(d) beat captures it live; charter §5 is the verbatim list):** Graph API consent (unblocks scout `#36` + `#40` + X1), the absent vault git remote, 4 credential rotations, final backup-zone names, the ADR-35 amendment decision (backup leg-2 → personal OneDrive, `#18`), the T6-D4 SharePoint confidentiality push, and the E5 design's D1–D5 decision points. These gate specific tasks and only the operator can close them.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (E1–E7 product story-map in R10 priority sequence, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2), the live in-progress branches (`git branch -v` — none open at derivation; P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**

---

=== PROBES.md ===

# Probe manifest — corp-monorepo architect (2026-07-18): anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE corp-monorepo checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, region text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub `.dev-knowledge`; its probes bind to **corp-monorepo** — run them in the corp checkout (`../corp-monorepo` from the hub, or the corp working directory). The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the corp-monorepo checkout) | the summary holds a generation-time state; corp closed a product window (Arc-B/Arc-C-W1/E5-design merges + a closing sweep) and the next arc will move HEAD, so any baked sha is already stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK`? | corp `BACKLOG.md` product story-map (E1–E7, R10 sequence) ∩ `scripts/validate_backlog.py` | the story-map counts drift on any BACKLOG edit (the closing sweep folded audit note-refs onto #17/#28/#34/#45); neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py BACKLOG.md` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`? (SessionStart `pre-commit install` arms all three.) | the corp checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` |
| P4 | Quote, **substring-exact**, the first content line inside the `owner=hub` region `conventions-commit-branch` of this repo's `CLAUDE.md` — confirming the hub methodology is materialized **verbatim**, not paraphrased. | corp `CLAUDE.md` region `<!-- methodology:start id=conventions-commit-branch owner=hub -->` | the owner=hub region text is byte-fixed from the hub template (`templates/claude-regions/`); a summary paraphrases it and cannot reproduce the substring | `grep -n -A4 "methodology:start id=conventions-commit-branch" CLAUDE.md` → the quote must be a substring of the live region |

## Gate procedure (CC)

1. **P4 first** — the forced CLAUDE-region read orients the session (confirms the hub methodology layer is materialized verbatim; corp is A0-closed) before product planning resumes. **Then run the §13(d) operator-context beat FULL** (the supplement is empty — nothing to narrow against). Then P1–P3, each against **live corp state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move (the next product arc) — re-derive it live, do not trust the residual's prose.
