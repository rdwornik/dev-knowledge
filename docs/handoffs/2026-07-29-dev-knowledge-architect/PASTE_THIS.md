=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-29-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-29-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**W-D intake-#18 ratification session (2026-07-30).** Rule the handoff-process amendment pack A1–A11 to a ratification decision and settle the v5.8-vs-v6 label; the decision surface is `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md`, whose per-amendment live checks and recommendations are already done — this session **rules**, it does not re-derive. Three inputs join the dossier and are not optional: (i) the **[#441] condition-2 vs A5 conflict**, left deliberately open by the 2026-07-29 adoption ruling and carried in the PLAYBOOK Ch8 *Open reconciliation* paragraph + dossier pack-finding 2 — one of the two yields here; (ii) **stale-procedure audit row 13** (`docs/audits/2026-07-29-technical-postflip-stale-procedure-audit.md`), the §14a epic-return "applies the backlog delta" clarifier, routed here as an A10-batch ride-along rather than a hotfix; (iii) the dossier's **§B rider register sequencing recommendation** — rule §B(b)'s *direction* first, then A7 / A4-item-3 as its content. Task-graph pointer: `BACKLOG.md`, the `handoff` serialize-group ([#435] owns the stewardship; [#421]/[#422]/[#344]/[#390] are its neighbours) — read the group, not a re-narration of it.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/window-winddown-2026-07-29`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-29-dev-knowledge-architect — the part the repo does not already encode

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
**Nothing new was introduced by this window's wind-down arc; everything below is inherited or environmental.** Read this as a map of *which* flags to expect and *why they are what they are* — P4/P6/P7/P9 supply every value.

- **Standing / dispositioned.** The WARN set carried into this window is the one the register already
  holds (`ecosystem/disposition-register.yaml`); the wind-down arc dispositioned nothing and added no
  register entry. If a `[stale]` line appears, treat it as a register-vs-live-WARN mismatch to resolve
  by ownership, not as this arc's residue.
- **Known red, external, not actionable here — [#430](b).** `fleet_parity` reads **live sibling-repo
  state**, so a concurrent merge in ai-council or corp-monorepo reddens this repo's gate with no action
  available in this tree. The row names both halves; (b) is the one that bites at ship time. Reproduce
  on bare `main` before spending any time on it.
- **`doc_rot` backlog-accretion loci — pre-existing, unchanged.** The accreted rows are [#344], [#421],
  [#422], [#332], [#278]. This arc measured its two row writes **before** writing them ([#441] edited,
  [#445] added) and both sit under the gross cap, so the locus set is byte-for-byte the one that
  existed at the window's start. Do not read a locus here as new.
- **[#364] is the live meta-flag, and it took a fresh hit this window.** The 2026-07-29 `.vscode` ruling
  could **not** be recorded into the [#371] or [#352] rows — both sit within ~16 and ~34 characters of
  the cap — so the ruling went to its own audit artifact instead. That is the "gate degrading the record
  it protects" failure the row predicted, now witnessed rather than argued. Recorded in
  `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md`, final section.
- **Environmental, recurring, never a finding.** The worktree-dir-name deployed-version WARN and the
  sibling-absent legs on a VM are environment artifacts. Also: run the gates from **Git Bash**, not
  PowerShell — a PATH-absence SKIP reds `handoff_probes` spuriously and invites a false disposition.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
The 2026-07-28→29 window, one line each. Detail is in `JOURNAL.md` entries 2026-07-28 (k)–(n) and
2026-07-29 (a)–(b); this is the map, not the recap.

- **[#439] — ADR-107 strangler step 3 executed.** `tasks/` is the source of truth; `BACKLOG.md` is
  generated. `ARCHITECTURE.md` Ch5 source zone + `tasks/README.md` are the conformed reference set.
- **[#437] — shared closure-token core.** One `strip_quoted_contexts` / `closure_ids` detection core
  consumed by both scanners plus the plugin twin, under a byte-parity test. Closed on two independent
  MET verdicts.
- **[#444] — `tier1-lifecycle` 0.1.11 released.** The [#437] fix reaches the version-keyed cache;
  5-manifest anchor lockstep. Closed.
- **[#441] — codified, then ADOPTED (operator, 2026-07-29).** PLAYBOOK Ch8 carries one launch test:
  fat prompt on primary is the default, worktrees behind the four-condition test. The DRAFT marker and
  its self-contradicting ratification note are gone (terra H3 resolved); the row's `§8/Ch5` citation is
  corrected to Ch8. **The row stays OPEN** — closing it is the closure loop's call, and one condition-2
  reconciliation is still owed (§4).
- **Post-flip stale-procedure batch — audit rows 1–12 applied**, rows 14–19 no-ops by verdict, row 13
  routed to the ratification session. Terra doc-lane review paid the review leg the cloud night lane
  could not run: H1 + M1 fixed, H2 + H3 dispositioned then both resolved in this wind-down arc.
- **Two operator rulings recorded at their convention homes, one artifact-borne.** The sanctioned
  shortened-sequence precedent sits at PLAYBOOK Ch8 *Integration authority*; the [#441] adoption at the
  Ch8 launch-decision block; the `.vscode` W1 ruling at
  `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md` (its surface is immutable, so the
  ruling gets its own dated artifact).
- **[#445] filed** — the `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing on a
  mixed diff. Third instance of the [#431] family; mechanism-scoped.
- **`ARCHITECTURE.md` delta-checked, deliberately untouched** — reasoning in §4.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### The decision this session owes (its whole reason to exist)

**Intake #18 ratification** — dossier `docs/audits/2026-07-29-technical-intake18-ratification-dossier.md`.
The un-committed "why" the dossier cannot carry: the pack was written as *eleven independent amendments*,
but §B(b) (one-round-trip boot) is a **workflow reshape**, not an amendment, and A7 / A4-item-3 are its
content rather than its peers. Rule the direction first or the content rulings land unanchored — that
sequencing is the dossier's own recommendation and it is the tension worth protecting. The v5.8-vs-v6
label follows the §B(b) call honestly; it is not a separate aesthetic decision.

**The [#441] condition-2 vs A5 conflict — deliberately left open, and it is a real fork, not a wording
tidy.** [#441] condition 2 cites "pre-allocated JOURNAL letters" as a contract that pre-resolves lane
contention; intake #18 A5 rules the opposite mechanism — letters are assigned **at integration**, never
by lanes. Both cannot be canon. The design argument the dossier makes (and this session should test
rather than accept): pre-allocation fails on the *second unplanned lane*, whereas assign-at-integration
cannot collide by construction. If A5 wins, [#441]'s condition-2 example list is amended **in the same
ruling** — one statement in the corpus, which is the whole point of the [#441] codification. The live
text of both sides is at PLAYBOOK Ch8 *Open reconciliation* and dossier A5 / pack-finding 2.

### Carried residue — what is open, and why it stayed open

- **Queued cross-repo arc (`.vscode` W1), RULING-W shape, not started.** Three legs, all consumer-side:
  the corp-monorepo manual `.vscode` decoration copy (the ai-council precedent, ADR-93 merge-not-clobber),
  and the `review_date: 2026-08-13 → 2026-08-26` e1 re-date in **both** consumers' `.methodology.yaml`.
  Ruled 2026-07-29, recorded in `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md`,
  executed **nowhere** — the operator scoped it as its own follow-up arc. Re-witness each consumer live
  before editing; the sizing surface's reads are dated 2026-07-28.
- **The 2026-08-26 cluster is now four things, not one.** The drain slice ([#356], [#358]–[#361] —
  prep artifact `2026-07-28-technical-drain-slice-prep.md`), the 26-row D-queue
  (`2026-07-28-technical-d-queue-0826.md`), [#364] build option 4(a) plus the disposition reviews, and —
  newly folded in by the 2026-07-29 ruling — **the `.vscode` mechanism-DATE selection**. That session is
  getting heavy; whether it splits is an architect call worth making *before* it arrives, not at its door.
- **[#433] stays open on §6.2 grounds — two concordant NOT-MET verdicts.** The ADR-107 §6.2
  generalization obligation is undischarged by design (its owner is [#383], open) and §6.3 is ruled but
  not structurally discharged; §7.5 bars closing on the ADR alone. This is the correct state, not a
  stalled one — do not let a closure sweep re-litigate it without the second-surface demonstration.
- **[#440] / [#442] / [#443] open, unbuilt.** [#440] — the `tasks/` id ledger is not tamper-evident (a
  *deleted* retired record silently frees its id; the gate only catches a re-issue while both holders are
  present). [#442] — plugin command-cache staleness: cached command text can outlive a workflow change,
  and this window witnessed exactly that. [#443] — planning artifacts outside the three enforced classes
  carry no rent rule. All three are honest gaps, none blocking.
- **H2-class residue: none outstanding.** H2 was the ADR-65 "closing adds no new per-item write" claim,
  falsified as a *mechanism* statement post-flip. Fixed in this arc by rewording to outcome language
  matching the converged host-branching sentence audit rows 5/9 landed. The **class** — pre-flip
  mechanism claims surviving as prose in un-swept files — is not provably drained; the night audit's
  19-row sweep plus this fix is the coverage, and a further instance would be a new finding, not a
  reopening.
- **Plugin-bump deferral state.** `plugin.json` holds at **0.1.11**. The morning batch's documentation-only
  plugin edits (the `/review-closures` host-shape branching) are therefore **not** in the version-keyed
  cache; an explicit cache-lag notice sits in `plugins/tier1-lifecycle/INSTALL.md`. Deliberate: a
  half-release (bump landed, marketplace + three-repo `plugin update` + restart not run) is worse than a
  documented lag for a docs-only change. The bump folds into the next release act — it is owed, not lost.
- **[#430] is the known red** — see §1. Reproduce on bare `main` before treating it as this arc's.

### One thing deliberately NOT done, so the next session does not redo it

`ARCHITECTURE.md` was delta-checked against this window's shipped set (flip live, shared closure core,
plugin 0.1.11, [#441] codified) and **left untouched**, with `last_reviewed` unbumped. Reasoning: Ch5's
source zone was already conformed at the flip and the night audit lists it in the conformed reference
set; the plugin version is pinned in `deploy/manifest-v*.yaml`, never in ARCHITECTURE; the [#437] shared
core lives under `plugins/` (outside the codemap's `scripts` source-root) and changed implementation, not
organ identity or posture; the [#441] launch test is PLAYBOOK doctrine, which ARCHITECTURE points at
rather than restates. The one borderline line — Ch2's closure-loop arrow ending "`BACKLOG.md` updated" —
is outcome language that still holds post-flip (the regen updates it), and the night audit adjudicated
exactly that class as CORRECT in its rows 15–17. A stamp bump without a genuine end-to-end re-read would
have been the dishonest move; the re-read was not run, so the stamp did not move.
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
> **Branch note.** This bundle was generated on branch `docs/window-winddown-2026-07-29`. This line names only *which*
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
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream) |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-29-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-29-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-29-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

=== ANSWERS === (outgoing browser seat, 2026-07-29)

Q1 STRATEGIC INTENT: Move from the structure era to the consumption era. This window made
tasks/ the live source, the closure loop real (4 full loops), and the fat-prompt default
doctrine (PLAYBOOK Ch8). The next session's way-of-working goal: pay the ratification debt
— intake #18 per-amendment rulings + the v6 cut decision — so the remaining prose-held
coordination properties (boot round-trip, JOURNAL letters, spec currency) move into
mechanism. After that, the 2026-08-26 cluster executes dispositions at scale, and the
[#382]→[#383]→[#385] chain is the system-implementation era (charter on main; the operator
may pull [#382] build forward of the 08-26 sizing as a priority call).

Q2 TENSIONS WEIGHED: (a) speed vs verification — operator-directed early merge (14bcb1c4)
landed as a NAMED precedent: sanctioned only with the mandatory post-hoc verification leg;
unshortened default stands. (b) delegation vs ADR-70 — closure sweep ran on a BATCH-SCOPED
delegation with dual independent Done-when verdicts; a standing delegation was deliberately
NOT created (would need an ADR-70 amendment — raise at #18 only if the operator wants it).
(c) producer≠reviewer economics on S-size — CC-builds/terra-reviews chosen over
Codex-producer (which would force sol). (d) cloud night lane vs absent user-level gates —
UNVERIFIED-UNTIL-LOCAL contract, branch-only, no merges. (e) cap integrity vs record
richness — compress-precedent used 3×, option 4(a) adopted, build at 08-26.

Q3 CONSIDERED + REJECTED (do not relitigate): PLAYBOOK codification of lesson 7 as-written
(self-blocked by prove-then-codify → LESSONS.md + [#443] chosen) · intake #16 → CONSUMED
(archives a live spec → ACCEPTED+deferred, trigger "[#382] build starts") · in-arc plugin
bump (half-release worse than documented lag → [#444] release act) · indented-code-block
stripping (excluded by design, loud residual test) · [#433] closure (twice, two concordant
NOT-MET on ADR-107 §6.2; sol E5 holds) · night work as a ROUTINE (ADR-105 + unratified
#19 §B → one-off cloud batch under branch-only).

Q4 OPEN QUESTIONS: [#441] condition-2 (pre-allocated JOURNAL letters) vs intake #18 A5
(assign-at-integration) — named fork, decide AT #18 · A7 + A4-item-3 sequence AFTER the
§B(b) one-round-trip-boot ruling · audit row 13 (HANDOFF_PROCESS §14a clarifier) rides the
v6 cut · .vscode mechanism DATE + vehicle ADR ([#387]) — 08-26 · #364 4(a) build shape —
08-26 · governs-vs-contains sub-question inside the #370 disposition · standing closure
delegation (ADR-70 amendment): raised, undecided, operator's call.

Q5 DECOMPOSITION RATIONALE / DO-NOT-REDO: the window ran serial-primary + Codex background
with per-arc frozen A–H contracts — keep that shape (it produced 100% plan execution, zero
process violations). Do NOT redo or re-decide: flip mechanics (live-witnessed) · shared
closure-token core design · #20/#16 rulings · .vscode option (b) · the Ch8 four-condition
launch test · the 12 stale-procedure fixes · everything in Q3. Next task-graph: W-D #18
FIRST (dossier docs/audits/2026-07-29-technical-intake18-ratification-dossier.md is the
decision surface; sol derives the v6 spec ONLY if a cut is ruled) → cross-repo RULING-W arc
(corp .vscode copy + both e1 re-dates; corp GO already given) → 2026-08-26 cluster.

Q6 OFF-REPO CONTEXT: operator escalation calibration (2026-07-28): D3/D4-class decisions
are the ARCHITECT's lane — decide + one-line note; escalate only real forks
(irreversibility, operator drivers, no objectively best option). Operator endorses the
fat-prompt default live ("better quality than singles", running the browser seat on Fable)
— recorded as [#441] evidence. Merge 14bcb1c4 authorship CONFIRMED by the operator in chat.
Night lane environment class: Anthropic cloud VM = no ~/.claude, no Codex — every future
night batch inherits UNVERIFIED-UNTIL-LOCAL. Operator wants night batches to continue —
route the standing version through #19 §B at the #18 session, not ad-hoc.
