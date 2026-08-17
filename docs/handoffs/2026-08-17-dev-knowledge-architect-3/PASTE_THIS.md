=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-17-dev-knowledge-architect-3` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-17-dev-knowledge-architect-3 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Flip the window class from audit-PRODUCING to audit-CONSUMING and net-CLOSING: every ratified piece of knowledge becomes either a wired mechanism or a closed row, with no third state. **The standing authority this serves is `[E7] Tooling & evaluation`** — *"As the operator, I want low-friction tooling and timely tech adoption"* — under which every item below is filed; and the governing ACCEPTED intake is **"Parallel multi-agent execution system — batch protocol as versioned repo artifacts"**, which fixes the batch shape this session dispatches under (one plan → N file-disjoint frozen lanes → one serial integrator). Work **priority order v2** in order — `[#533]` leg 2 first (throughput: `audit-health` is a pre-commit gate, so its cost is paid on every commit by every lane and by the integrator), then wire the two built-but-uncalled libraries `[#529]`/`[#530]`, then `[#554]`, then the `[#533]` seam leg *before* lanes l/y, then `[#555]`; and ratify the DRAFT intakes #35–#39 into ADRs + rows rather than leaving them DRAFT. Task-state is `BACKLOG.md` — the spec, read it there, never re-narrated here; the ordered plan and its amendment live in `docs/handoffs/2026-08-17-dev-knowledge-architect/SUPPLEMENT.md`, which is an **INPUT** to this handoff and not the handoff itself.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->Planning and governance surfaces only: `tasks/` plus `gen_task_tree.py --emit-source` for any row change (never `BACKLOG.md` by hand), `docs/decisions/ADR-*.md` for the intake ratifications, `docs/intake/*` status transitions **with both** intake generators, `protocols/PLAYBOOK.md` for the promotion-debt items, `JOURNAL.md`, and `docs/audits/` for anything it produces. **Implementation does not happen in this tree** — `[#533]` leg 2 and the `[#529]`/`[#530]` wiring are dispatched to file-disjoint lane worktrees from this seat, because the seat's own writes and a lane's writes must not share a tree.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->**architect**, because the deliverable is a way-of-working decision set — the priority order, the intake ratifications, and the shape of the first net-closing batch — rather than the advance of one named backlog item, which is what execution mode is profiled for. So the residual is scoped to the planning *why* plus the whole `BACKLOG.md`, and the browser is served the generative/decompositional posture.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-p0c-repair`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The `Destination` row is declared ex-ante — a lane inherits none of it from a prior prompt.**
> Only its **branch** field has a mechanical counterpart: `PROBES.md` **P3** compares it against
> live `git branch --show-current`, and a mismatch is a FAIL. Worktree, write-scope and MODE-basis
> stay **prose** and deliberately carry no probe leg — a leg with no mechanical counterpart cannot
> fail honestly, and one that cannot fail honestly discredits the whole block (R3).

> **Anti-bluff in effect.** The contract, what the withholding buys, and where generation-time
> hints go instead are stated **once** in this bundle's own `PROBES.md` header (spec:
> `HANDOFF_PROCESS.md` §5) — one hop inside the same paste, rather than a second copy free to
> disagree with the first.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

> **Dispatch prep is not copied here either.** A seat taking the architect role finds how a dispatch
> prompt is made, how model + effort are routed, how a batch runs, and how completion is managed at
> **`protocols/PLAYBOOK.md` Ch8 "Handoff prep for the next architect"** — itself an index of pointers,
> so this is one hop to the index and one more to each home. Standing rulings applied without asking:
> `protocols/STANDING_RULINGS.md`. Same pointer-not-copy rule as the runbook above.

---

=== protocols/HANDOFF_BOOT.md ===

---
reconciled_with: handoff-process@6.2.0
---

# HANDOFF_BOOT — thin browser boot (HANDOFF_PROCESS v6)
<!-- scope: meta -->

> **What this is.** The whole boot for a fresh browser (Claude.ai) chat. Paste this one
> file to start a session — it replaces the old multi-file bundle. Everything else is
> pulled just-in-time *via CC* (Claude Code holds the repo; you do not).
> Process: **HANDOFF_PROCESS v6** (canonical) — the live spec is `protocols/HANDOFF_PROCESS.md`,
> which CC holds; ask CC to pull any part you need.

## Core — these three lines are the boot. Read them first.

1. **Who you are.** You are the **critical architect** for this work. Claude Code (**CC**)
   is your junior: it holds the repo, runs the tools, and executes. You direct; it does.
2. **One rule.** Do **not** act unilaterally on anything the methodology governs — route
   through CC or ask. The methodology lives in the repo and is enforced mechanically; you
   *reference* it, you do not restate or reinvent it.
3. **First move.** Read **CC's handoff** (its residual + pointers + **drift-flags**). Do
   nothing else until you have it.

**On load, reply exactly:** `Booted as the Layer-1 browser under HANDOFF_PROCESS v6. Ready for CC's handoff. ({n} sections received.)`
— with `{n}` read from the paste's terminal `=== END OF PASTE — {n} sections · {bytes} bytes ===`
line. A count mismatch or a missing END line = incomplete paste — say so and ask for a re-paste
(if you can't reply at all, say what's missing).

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
the generative posture below instead — HANDOFF_PROCESS v6 §13.) Concretely:

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
  standing topics → backlog**: your role is already set (above); next you grasp the vision; the
  standing authorities (active epic themes + accepted intakes) are reconciled; then the backlog drives
  the work. *Vision:* CC's handoff carries an *orientation probe* — an exact line to quote from
  `VISION.md` (`## Vision` — *what `.dev-knowledge` is*) and from `ARCHITECTURE.md` Chapter 1 (*where
  this work sits — Layer 2 of the three-layer model*). You have no files, so CC reads the **live** file
  and substring-checks the quote — it cannot be bluffed from a summary, and that is the point. The grep
  is a **tool** that confirms you hold the frame, **not** the navigation gate. *Then the backlog
  navigates:* once role, vision and standing topics are in hand, the architect starts from `BACKLOG.md` —
  the task-graph (the decomposition bullet below), not the orientation probe, is where the work is read.
- **One evidence block, not a command ferry (v6).** You do **not** dictate probe commands one at a
  time. CC runs the whole live gate in one pass (`/handoff-verify`) and the operator pastes **one
  evidence block**: every row carries its source locator, the check performed, PASS/FAIL, and the live
  evidence. Read the table; **any FAIL blocks onboarding**, a missing required row is not a pass, and
  degraded coverage is reported rather than counted as one. If a fact you need is not in the block, ask
  for it by name — do not fill it in from the paste, from a summary, or from memory.
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

**The launch test is not resident here — ask CC to pull it.** Whether a second committing
session opens is settled by ONE test at **PLAYBOOK Ch8 §0** ([#441]'s four conditions); a batch
rather than a pair runs under Ch8 **"The batch protocol"** (ADR-110), via `/lane-boot` and
`/lane-integrate`. A three-check copy of that test stood here for weeks after the corpus retired
it — which is why this is a pointer now.

Resident, because it governs your behaviour rather than restating a rule: parallel sessions
**commit-and-STOP and do not self-merge** (a linked worktree can't check out `main`, already held
by the primary — the #200 finding), so integration funnels through the primary checkout, `--no-ff`,
**one branch at a time**, with the operator as the serial gate. The command you hand over is
**`claude --worktree <name>`** or **`EnterWorktree`** — not a raw sibling `git worktree add`, which
skips the `.worktreeinclude` seed. Teardown (`remove` + `prune` + `branch -d` + verify no leftovers)
is half the act.

Canon: **PLAYBOOK Ch8** — ask CC to pull it.

## Verification split (who checks what)

- **You verify the *artifact*.** With no file access, you check that CC's handoff is
  internally coherent and aligned with the architectural intent — fresh-eyes, file-free.
  Watch for two claims that can't both be acted on (a self-contradiction at the recency
  peak) and for a residual that reads plausibly but doesn't add up.
- **CC verifies *state fidelity*.** Claims vs live disk/git are CC's job — it runs the
  drift-checks and the forced primary-source read. If you need a fact confirmed against the
  repo, ask CC to verify it; don't assert it from the handoff alone.
- **Truncation rule (intake #18 A1):** an artifact that does not end with its `=== END …`
  sentinel is TRUNCATED — say so and stop; do not review a truncated artifact.

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
  (`python scripts/audit.py ship-gate`) plus the freshness / `doc_claims` / BACKLOG legs, and the
  ADR-85 **pre-push** anchor refusal (next section). Don't design around them — design *with*.
- **Automation map.** Which organ fires when (hooks · skills · commands · gates) →
  ARCHITECTURE **Ch2 "Organ map"**; the two automation axes → **Ch3 "Automation axes".**

## Closing a session — definition of done

Plan with closure in mind from the start. The canon is `protocols/DEFINITION_OF_DONE.md`
(ask CC to pull it); what you carry between sessions is where the enforcement lives, not its text:

- **Where the teeth sit.** The session-end **Stop** hook is **advisory in full** since the
  ADR-85 amendment of 2026-08-03; the blocking leg moved to **pre-push**, scoped to `main`, and
  `/override` discharges no gate (§A2). Behaviour is unchanged by the move: an arc's
  `JOURNAL.md` entry rides its own branch, ahead of the merge, naming a SHA that merge introduces.
- **The rest is not resident on purpose** — ask CC to pull `protocols/DEFINITION_OF_DONE.md`
  rather than acting on a remembered shape.

The four other living docs (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING) are *update-when-
materially-affected*, not per-session-gated.

---

=== RESIDUAL.md ===

# Residual — 2026-08-17-dev-knowledge-architect-3 — the part the repo does not already encode

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
**Standing and register-dispositioned** (`ecosystem/disposition-register.yaml`), so a flag in these classes is expected rather than news: the ADR-88 FC2 `undeclared_edges` prose-edge class against the `handoff-process` and `prompt-template` specs, and the legacy `no_ff_merges` entries for the pre-floor journal/transcript wrap commits. Do not re-disposition these — they carry their reasons in the register.

**Standing and advisory BY RULING, not by register.** A different thing, and the distinction is load-bearing because these will never appear in the register no matter how long they persist: `review_artifact_coverage` (both legs) is advisory per the `[#480]` P3 ruling, its hard pre-push leg deliberately deferred pending two consecutive clean windows; and `journal_spine_anchor`'s *anchored-by-mention-not-by-record* leg is advisory per N2-L5 (`[#524]` leg c) and never changes that check's pass/fail verdict.

**New this window, and self-inflicted — recorded here rather than left to be discovered.** The two births `[#554]` and `[#555]` each exceed `doc_rot`'s declared `backlog-row-length` ceiling, so this window ADDED members to that class. They add nothing to the `backlog-accretion` ARM class, because a newly born row has a single history date, so the owned suite RED's condition — accretion findings present, not merely length findings — was not worsened by them. **But that RED's locus set has grown past what the prior supplement recorded:** it named a single accreting row, and the live corpus now carries several, `[#553]` among them. Re-derive the set; do not inherit the single-locus framing.

**The two OWNED suite REDs are unchanged in kind and still owned** — the `routine_consumers` live-corpus pin (which asserts an exact routine-row population that the batch was explicitly told to grow) and the `doc_rot` accretion pin above. Neither is a defect detector firing on a defect; both are pins tracking a corpus that keeps moving, which is exactly why they are owned rather than dispositioned.

**Everything quantitative is deliberately absent from this file** — no verdict, no counts, no `[stale]` status, no shas, no drifted ids. `PROBES.md` P4/P6/P7/P9 re-derive them at check-time; a value written here would be bluffable from a summary and would invert the anti-bluff contract this bundle exists to hold.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
- **Lane r merged** (`worktree-lane-r-412-research-intake`, new-files-only) — five EXTERNAL EVIDENCE browser-research artifacts into `docs/archive/`, intakes **#35–#39** into `docs/intake/` at `status: DRAFT`, and the lane's contract of record into `docs/audits/`. References `[#412]`; **does not close it** — that row's Done-when also wants a routing doctrine in `protocols/PLAYBOOK.md`.
- **Two births** — `[#554]` devcontainer + provisioning script (NB4-G stage 1) and `[#555]` closing campaign batch 1 + the kill-candidates instrument. Each discharges one *NO ROW — file it first* entry in the amended plan.
- **The 08-17 supplement amended** to priority order v2 and marked **INPUT, not the handoff** — additive only, per the handoff-immutability rule, so the ranking first ruled stays legible beside the one ruled after.
- **The last lane worktree and branch torn down**, so no `worktree-lane-*` branch exists. That teardown is what discharges the `[#510]` honest exception: the ADR-110 anchoring exemption keys on lane-branch SHAPE, so it is self-grantable only while such a branch exists, and it evaporates at closure.
- Detail lives in `JOURNAL.md` **2026-08-17 (e)** and this arc's commits; the rows live in `BACKLOG.md`. This is a map, not a recap — the JOURNAL already encodes the reasoning.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Carried and deliberately deferred — resume these, do not relitigate them:** the consumer-side home for `[#293]` (candidates await one ruling); the final seam re-point shape for the monkeypatch-pinned checks (smallest-diff versus a shared seams module, nb5-A on the table); the class-3 N-1 landing-predicate re-point, which is governance and separate from the seam leg; the telemetry read-path stack (D3-first is ruled — datasette versus static HTML is decided only **after** `[#529]` wiring emits real data); the routing-table amendment, gated on NB4-A seeded-defect acceptance plus the `[#492]` Grok browser check — **that peg was due 2026-08-17 and repo evidence said not-released as of 08-10, so assume it may be unmet**; and the audit-corpus `status:`-frontmatter proposal versus ADR-100's files-never-move stance, filed and unratified.

**Opened by this arc — each is a decision this seat owns, not a task:**

1. **The `doc_rot` row-length ceiling versus actual practice.** The declared ceiling sits far below what recent rows actually run, and the two births are now among the longest rows in the corpus. The standing stance is that `doc_rot` is greened by FIXES and never by dispositions — so either the ceiling is wrong and moves, or long rows get decomposed. Left undecided, every future birth adds a finding to a class that is meant to be shrinking. This was created knowingly: the row content was authorized, and trimming it to the ceiling would have cost the load-bearing reasoning, so the tension is escalated rather than silently absorbed in either direction.

2. **Which row owns the unshallow and the `uv`-pin assert.** `[#554]` and `[#453]` overlap on two of four legs — found by checking the *nothing owns this* premise instead of accepting it. `[#554]`'s clause says whichever lands second discharges by pointing at the first; that is a convention this seat can ratify or replace, not a decision already made.

3. **One denominator predicate.** Three counts of the same backlog are in circulation — the open set from `tasks/` frontmatter, the rendered `BACKLOG.md` bullet count, and the `SessionStart` load gauge, which agrees with neither. `[#555]` makes naming one predicate its first act; until that lands, any *net-negative* claim is unfalsifiable.

4. **Who performs promotion.** `assemble_paste.py` flagged ruling-bearing lines in the folded ANSWERS as promotion debt, and answer 7 names durable homes for six ratified terms (PLAYBOOK §8 / §8b / batch-protocol / batch-close, and intake #39). The homes are named; the promotion **act** is unowned — the same decided-unfiled failure mode the amended plan flags twice.
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
> answer**. The browser has no file access, so the answers reach it one way only: **CC** runs every
> command against **live state at check-time** via `/handoff-verify`, re-derives ground truth, and
> emits **one evidence block** carrying each row's PASS/FAIL and live evidence. The operator pastes
> that block once (HANDOFF_PROCESS §5 — the v6 one-round-trip boot). **Any FAIL blocks onboarding**,
> and a missing required row is not a pass. Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts,
> group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass criterion
> is **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-p0c-repair`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
>
> **Windows note:** `audit.py checks` (P2) can crash mid-listing on a bare cp1252 PowerShell console
> (a non-ASCII glyph in a check docstring) — run with `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`); this
> is Python's stdout encoding, shell-independent, so git-bash does **not** avoid it. `ship-gate` (P7)
> can false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P0 — Standing-topic reconciliation (emitted **above** P1 — A7 / R2)

The **standing authorities** a session reconciles against before it plans: the live epic
themes and the live accepted intakes. This was a §13 prose rule and it failed three consecutive
windows — *a rule with no probe has no teeth* — so it is mechanized here. **Deterministic legs
only** (the RM-4 / S3d boundedness law): there is no open-ended adjudication leg, because
whole-set grooming is an **arc, not a probe** (JOURNAL 2026-07-26 (h)). P0c is narrowed to a
**name-match** for exactly that reason (amendment A2): "does the Purpose *serve* this authority"
is a judgment a probe cannot terminate on, and a leg that cannot fail honestly discredits the
block. Same contract as every row below: question + source-locator + command, **no answer**.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P0a | Quote, **substring-exact**, the theme-preamble line of each **active** `[E#]` epic theme in `BACKLOG.md` — **and** separately confirm the generated backlog is **CURRENT**, not stale. | `BACKLOG.md` `[E#]` theme headers + the preamble line under each | the preamble set drifts on any theme edit, and `BACKLOG.md` is GENERATED since [#436] — a probe that can pass on stale generated content is bluffable, so currency is asserted mechanically, not assumed | `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches the live preamble (a paraphrase is a FAIL); **then** `python scripts/gen_task_tree.py --check` exits 0 — a non-zero exit is a FAIL (currency — R2's second assertion) |
| P0b | Enumerate, live, every doc under `docs/intake/` whose frontmatter carries `status: ACCEPTED`, and quote each one's **TITLE line** (its first level-1 `#`-heading). **Titles only.** | `docs/intake/*.md` frontmatter + first heading; area definition at `docs/intake/README.md` | the accepted set and its titles drift on any intake status change; neither the set nor any title appears in this bundle | `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading line |
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-17-dev-knowledge-architect-3/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-17-dev-knowledge-architect-3/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

**Honest narrowing (terra H3).** P0b quotes **titles**, not wave/sequence detail: wave content is
unstructured prose today, so quoting it would overclaim determinism (the RM-4 law applied to this
row's own design). Wave-level teeth require the intake schema to first gain a required,
machine-locatable plan-of-record heading — an intake-schema change owned by `docs/intake/README.md`,
offered as an option, not assumed.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files, so CC reads live and substring-checks,
and the result arrives in the evidence block. The grep is a **tool** that confirms the frame — **the
backlog navigates** (§13c), not this read.

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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-17-dev-knowledge-architect-3/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-17-dev-knowledge-architect-3/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-17-dev-knowledge-architect-3/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-17-dev-knowledge-architect-3/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-17-dev-knowledge-architect-3/SUPPLEMENT.md` (is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ `scripts/validate_backlog.py` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one the fleet already shipped or superseded | `python scripts/validate_backlog.py` (schema + serialize-groups) then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge |

## Gate procedure (CC)

1. **Run the whole gate in one pass** (`/handoff-verify`), in table order: **P0 first, then P1**,
   then the remaining rows — every row against **live state now**. Table order IS the execution order. The
   architect cannot begin design until both orienting lines are read live and substring-matched.
   **The operator-context beat (§13d) fires after the block is in hand.**
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P0a–P10 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state**. P10 grooms the
   whole open BACKLOG at boot (live / dead / awaiting-ruling per open `#id`). First check
   which branch is live (P3), then re-derive every load-bearing fact from the live primary source.

---

=== SUPPLEMENT.md ===

ARCHITECT ANSWERS — handoff Q1-7, seat 2026-08-14-dev-knowledge-architect, 2026-08-17

1. STRATEGIC INTENT: Shift the window class from audit-PRODUCING to audit-CONSUMING and net-CLOSING. The next session's way-of-working goal: every ratified piece of knowledge becomes either a wired mechanism or a closed row — no third state. Concretely: throughput first (#533 leg 2), wire the two BUILT-UNWIRED libraries, ratify intakes #35-#39 into ADRs+rows, run the first net-negative backlog batch (closing campaign batch 1 with the kill-candidates instrument).

2. TENSIONS WEIGHED: (a) max parallel width vs serial integration queue -> settled at width 11-12 with admission control MAX 6 active locally (measured: 99.6% CPU, hook starvation at 12); the queue is the binding constraint, not lane count. (b) Workaround vs structural fix at the l<->y collision -> chose mid-batch decomposition (#533); cost accepted: 27 checks held on three measured blocker classes; gain: the collision class is dead, not patched. (c) Behavior-freeze vs performance in lane m -> kept byte-identical golden proof, deferred parallelism to leg 2 (never mix refactor and behavior change). (d) Operator visibility vs process purity -> the §D direct-supplement was a process violation (owned); handoff runs by the book now. (e) Telemetry rank: lane c said #1, architect ruled #2 with #533-leg-2 first — measured commit-tax beats measurement infrastructure by one slot, no lower.

3. CONSIDERED + REJECTED (do not relitigate): section-scoped shared ownership for l<->y (superseded by #533 decomposition); hand-anchoring the ADR-110 exemption (batch-5 emergency shape only — uniform rename + the #531 creation-time gate is the standard); a 16-wide local batch (W5 cap + queue arithmetic + measured saturation); GPU substrate (I/O-bound workload, wf-fe444def verdict: open-weight still -8.6 SWE-bench pts and 5-20x latency); Oracle free tier (gutted, enforcement 2026-08-18); greening doc_rot by dispositions (fixes only); monorepo migration (stay polyrepo, hub-as-platform per wf-460fee76); file-sync tools for remote lanes (git is the sync layer).

4. OPEN QUESTIONS (deliberately deferred): consumer-side home for [#293] (nb5-B candidates await one ruling); final seam re-point shape for the 25 monkeypatch-pinned checks (smallest-diff vs shared seams module — nb5-A on the table); class-3 N-1 landing-predicate re-point (governance, separate from the seam leg); telemetry read-path stack (D3-first ruled; datasette vs static HTML decided after #529 wiring emits real data); routing-table amendment gated on NB4-A seeded-defect acceptance + the #492 Grok browser check (DUE TODAY 2026-08-17, assume peg possibly unmet — repo evidence says not-released as of 08-10); audit-corpus status: frontmatter row vs ADR-100 files-never-move tension (row filed, unratified).

5. DECOMPOSITION RATIONALE (do not redo): batch shape = ONE plan -> N file-disjoint frozen lanes -> ONE serial integrator with the operator as the only merge gate; RESERVED ID BLOCKS for concurrent births are now proven (17 births, zero collisions) and are the standard; every lane contract carries a PINNED-BY-TESTS section (five-witness finding: OWNED-FILES bounds writes, not test-pin dependencies); #533's module home is recorded (STANDING_RULINGS K-2) — never re-derive; ADR-110 exemption evaporates at closure (batch-6 discovery, recorded); in-lane tests run -n 0, parallelism belongs to the one integration suite.

6. OFF-REPO CONTEXT: five browser-research artifacts landed with EXTERNAL EVIDENCE headers, intakes #35-#39 DRAFT await ratification — they carry the model-portability (AGENTS.md-as-canonical + pointers), autonomy-ladder, done_when schema, fleet-conformance (fleet_check.py sketch), and substrate plans; substrate direction confirmed by the operator: Codespaces free tier stage 1 -> Hetzner CX53 SHARED (post-2026-repricing; NOT CCX), VS Code Remote Tunnel + tmux as the control plane, teleport is one-way web->local and the VS Code extension cannot attach to live remote bg sessions; the operator's standing demand: visible ROI — dispositions, archival routine, and net closure are the acceptance test of the next window, not new audits.

7. RATIFIED-IN-CHAT REGISTER (verbatim term · definition · durable home): "audit-to-row conversion authority" · every audit carries exactly one disposition ACTIONED/FILED/REJECTED/SUPERSEDED, an undisposed audit is a defect · PLAYBOOK batch-close section + already embodied in the 2026-08-17 disposition ledger; "admission control" · local batch width bounded by measured schedulable concurrency, default 6 on this machine class · PLAYBOOK §8 (candidate landed in LESSONS at batch-6 wrap — promote); "reserved id blocks" · concurrent-birth safety via per-lane disjoint id ranges printed at dispatch · PLAYBOOK batch protocol; "PINNED-BY-TESTS section" · mandatory lane-contract section listing live-tree properties the lane legitimately changes · PLAYBOOK §8b; "priority order v2" · #533-leg2 -> telemetry+single_flight wiring -> devcontainer -> seam-leg+l/y -> campaign batch 1 · supplement amendment (this handoff); "teleport one-way / no VS-Code-attach to remote bg" · substrate constraint from wf-fe444def · intake #39 ratification target, not PLAYBOOK yet.

---

=== END OF PASTE — 5 sections · 50947 bytes ===
