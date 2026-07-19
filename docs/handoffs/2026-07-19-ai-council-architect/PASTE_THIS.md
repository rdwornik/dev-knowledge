=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-19-ai-council-architect` |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-19-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Target repo** | **`ai-council`** — cross-repo (ADR-36/41). This bundle is *hosted* in the hub and derived **READ-ONLY** from the ai-council checkout. **Run every `PROBES.md` command in ai-council, not the hub.** |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Shape the **fix-and-unblock** window that follows ai-council's just-closed verification-and-debt window. Four threads need an architect's call, not an executor's: the two P2 silent-failure defects (#69/#71 — shared-helper vs local patch), whether the silent-failure trio (#62/#63/#65, plus #35) is one uniform fail-loud output-routing contract rather than four S-sized patches, a decide/drop ruling on the two proposed guards (#67/#68), and how to sequence around **#27**, whose Phase-3 operator scoring is the single highest-leverage unblock in the repo and is gated on a human action. Navigate from ai-council **`BACKLOG.md`** (the seven-theme story-map); `RESIDUAL.md` §4 carries the tension in each thread.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/ai-council-architect-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-19-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13). **Target repo: `ai-council`** — this bundle is hosted in the hub
> (ADR-36/41) and derived **READ-ONLY** from the ai-council checkout. Every probe command runs
> **in ai-council**, not the hub.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the ai-council JOURNAL / BACKLOG / git window, may have moved (the load-bearing
> ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

**The load-bearing drift this window was a FALSE PREMISE, not a stale count — and it had gated a whole class of work.** `witnessed` (from the ai-council JOURNAL 2026-07-19 entries): the standing assumption *"codex credits are exhausted until 2026-07-23"* was **empirically falsified** by a live terra probe ($0 under subscription). A body of review debt had been **date-gated on that unverified premise**; lifting it immediately discharged #33 (pass-3 CLEAN) and #44 (the 8-surface review set). **The architect should treat this as the pattern-level flag, not the incident:** a date-gate resting on an unprobed assumption is indistinguishable from a real block until someone probes it.

**Standing flags to re-derive, not trust (values deliberately absent — that is the anti-bluff contract):**
- **Gate-green is a claim, not a fact here.** `check.ps1` reportedly returns clean after the `types-PyYAML` declaration landed — **re-derive via `PROBES.md` P6**; this bundle states no exit code, test count, or mypy verdict.
- **BACKLOG shape moved hard** (#33 struck, #44 closed, #69–#72 filed, #68 re-prioritized) — counts and `OK`/FAIL come from **P3**, membership/liveness from **P7**. No count appears here.
- **ai-council carries no hub-style drift mesh.** There is no `audit.py ship-gate`, no `validate_git_backlog`, no `validate_doc_claims`, no disposition register in this repo — so the hub's usual §1 flag-set structurally **does not exist** here. The equivalents are `validate_backlog.py` + `check.ps1` + `canonical_freshness_gate.py`. Stated explicitly so the architect does not hunt for a mesh that isn't there, or read its absence as a finding.

**A live honesty flag worth the architect's attention (`witnessed`, from the JOURNAL):** **#44 was closed via its done-when's explicit "(or fixes filed)" clause — NOT because the reviewed surfaces came back clean.** Two P2 defects (#69, #71) are the reason a clean-only bar was not met. If the operator's intent was clean-only closure, reopening #44 is one edit. **This is a decision to surface, not inherit silently.**

**Two stale references recorded, not yet fixed:** `scripts/codex-review.ps1` is cited as the runner in both #33 and #44 but **does not exist** (the reviews ran `codex exec` directly); and the #33 pass-3 CLEAN verdict carries an asterisk (terra's read-only sandbox threw a `tempfile` error mid-pass, though its ~40k-token spend indicates real analysis). Neither is filed as a task yet — **an architect call: file or waive.**

---

## §2 — Shipped this window (the map — pointer, not re-narration)

Terse map only; ai-council `JOURNAL.md` (2026-07-18 → 2026-07-19 entries) and `BACKLOG.md` already encode the detail. Do **not** re-derive this narrative — read it there.

- **Review debt discharged** — #33 (verdict-package terra pass-3, CLEAN) and #44 (the 2026-07-18 arc set, now 8/8 surfaces reviewed: 5 in the night pass, 3 in the 2026-07-19 pass) both **struck**. The date-gate that blocked them was falsified (§1).
- **Night-consolidation verification** — 8/8 legs witnessed at $0 via live execution of shipped code, codified as `scripts/verify_night_consolidation.py`; a blind Codex `sol` derivation agreed on all 8 verdicts. Report: `docs/audits/2026-07-19-night-consolidation-verification.md`.
- **Worktree consolidation** — the `s14-cleanup` and smoke-pair branches closed out into `main`; a **sealed-key leak was caught and untracked pre-merge**; the `docs/smoke/` leftover struck under §5 item 9.
- **Type-stub hygiene** — `types-PyYAML>=6.0` **declared** in `[project.optional-dependencies] dev` (not ad-hoc installed); **#20's scope widened** from "the openai 2.x migration" to type-stub hygiene generally, on the reasoning that two stub-class gate failures in one day means the root cause is undeclared typing dependencies, not any single library.
- **Filed from review** — **#69, #70, #71, #72**. Every terra claim was **verified against source before filing**; two severities were **downgraded with the reasons recorded on the items**. While verifying #69, a **second distinct defect the review missed** was found (the inbox/`--file` panel divergence).

---

## §3 — Carried residuals (still live — NOT re-derivable from the repo alone)

**(a) The `--file` vs `--inbox` divergence is an inverted recurrence of a known anti-pattern.** #69 is not one bug but two: a documented frontmatter key silently discarded on every default run, *and* the two entry points guarding on **different conditions**, so the same brief yields a different panel via `--file` than via `--inbox`. This is the CLAUDE.md §10 inbox-parity anti-pattern **inverted** — interactive is the broken half this time. **Design implication that travels:** the fix is a **shared helper**, not two parallel patches; #64 touches the same `--file` surface and should likely merge with it.

**(b) `#71` is shipped code violating the rule that was being enforced the same day.** `--no-persist` calls `mkdtemp()` with **no cleanup anywhere in the module** — a live violation of §5 item 9 "No leftovers." It is also a **concrete instance of the #68 guard proposal**, which strengthens that proposal's case materially. Whether that converts #68 from proposal to accepted work is an **architect call**.

**(c) The two consumer→hub NEEDS-RULING intakes remain hub-tracked, ruling pending.** Filed locally in ai-council `docs/intake/` and carried across the boundary (the sanctioned consumer→hub path): `2026-07-17-hub-feedback-codex-producer-lane.md` (hub `#341`) and `2026-07-17-hub-feedback-session-close-gate.md` (hub `#344`). **Do not re-plan these in an ai-council chat** — they are a hub session's work. `unknown`: whether either has been ruled since filing.

> **Supplement correction (§13: advisory, never trusted over the repo).** The filled `SUPPLEMENT.md`
> §4 cites the session-close-gate ticket as hub **`#343`**. That is **wrong** — `witnessed` against the
> live hub `BACKLOG.md` this generation: **`#344`** is "Session-close gate for handoff generation +
> consumer hub-write guard (NEEDS-RULING)"; **`#343`** is an unrelated `fleet_parity` ship-gate-scoping
> perf item. The supplement is committed **verbatim and unedited** (CC never rewrites the architect's
> answers) — so the wrong id stands in that file by design, and this note is the correction. **Use
> `#344`.**

**(d) The interim Codex-producer fallback — verify before assuming it still binds.** The 2026-07-17 ruling held that bounded build tasks run as **CC-implements + terra read-only review pre-merge** (never Codex-writes), pending the hub's #341 reconciliation. It shipped several arcs cleanly and terra caught real defects each time. **But its stated rationale referenced the credit-exhaustion premise that §1 falsified** — so the *fallback* may still be right while its *stated reason* is now partly stale. Worth an explicit re-confirmation rather than silent inheritance.

**(e) The §6.3 scope-boundary fork — still awaiting an explicit ruling.** The plan-of-record / consolidation-brief fork (pure-governance vs thinking-aid scope) is implicitly held at "pure governance" but was never formally adjudicated. Carry-open; raise only if the operator does.

---

## §4 — Next-frontier decisions (the design "why" that travels)

**The window that just closed was a *verification and debt* window. The next one is a *fix and unblock* window.** The architect's job is to decide the shape of that, not to re-derive what shipped.

**The four open threads, with the tension in each:**

1. **The two P2 silent-failure defects — #69 and #71 (the ready slack).** Both are *silent* failure class: neither surfaces an error, both produce a plausible-looking success. #69's fix is a shared-helper refactor across two entry points (§3a) and likely merges with #64; #71 is a cleanup-on-exit fix that doubles as evidence for #68 (§3b). **Tension:** patch each locally (fast, but re-splits the `--file`/`--inbox` surface a third time) vs land the shared helper (correct, larger, touches the highest-contention module family).

2. **The silent-failure *trio* — #62, #63, #65 — needs grooming as a class, not as three tickets.** All three are the same shape: a write/route failure that returns success. #62 research `--return-dir` is best-effort; #63 a metrics-sidecar failure **suppresses the verdict package entirely**; #65 `doctor` ignores the #39 output controls. **The architect question is whether these plus #35 are one epic-level fix — a uniform fail-loud output-routing contract — rather than four independent S-sized patches.** That is a way-of-working decision, which is why it belongs in this session and not an execution lane.

3. **The two proposed guards — #67 and #68 — await a decide/drop ruling.** #67 is a pre-commit gate on staged `SEALED-KEY*.json` (motivated by a *real* near-miss this window, not a hypothetical); #68 is a registry check on new `docs/` directories, and #71 just supplied it a live instance. **Tension:** both are hub-methodology-shaped guards living in a consumer repo — the standing question of whether a consumer may grow its own gates or must file the need to the hub.

4. **#27 CLI-4 parity remains the blocking centerpiece.** Phase 1+2 are done (24 blinded transcripts + scoring sheet committed); **Phase 3 is operator scoring — non-delegable and blind.** Until it is scored and unsealed, the **ADR-12 §5 CLI default-flip stays blocked**, which in turn blocks **#41 end-to-end** and **#66**. **This is the single highest-leverage unblock in the repo and it is gated on a human action, not on engineering.** The architect should decide whether to sequence work around that gate or press for the scoring session.

**Carry-open (do NOT redo / re-decide):** the hub NEEDS-RULING intakes (§3c) are hub work; the §6.3 fork (§3e) awaits the operator; the [S13]/#36–#38 caller-side advisor is **filed only** — build when prioritized, and #36 must reconcile with #9 rather than duplicate it.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to ai-council's **`BACKLOG.md`**
(seven-theme story-map, machine-checked by `scripts/validate_backlog.py` — counts re-derived live via
`PROBES.md` **P3**, the #69/#71 ready slack read live via **P4**, the whole open set groomed at boot via
**P7**), plus the **`docs/audits/2026-07-19-night-consolidation-verification.md`** report (this window's
evidence base — point at it, do not re-narrate it), the live branches (`git branch -v`), and any drift
the repo's own gates raise.

> **Pointer correction (`witnessed` this generation — do not inherit the old one).** The phase→task
> plan-of-record has been **ARCHIVED** to `docs/intake/archive/2026-07-16-plan-of-record.md`, and the
> seam-contract intake likewise to `docs/intake/archive/2026-07-06-technical-architect-intake.md`.
> Prior ai-council bundles cite both at live `docs/intake/` paths; those citations are now **stale**.
> The archived plan-of-record is **history, not the navigation surface** — **`BACKLOG.md` navigates**
> (§13c). Read the archive only for provenance on a decision, never to derive current scope. Re-narrating item text splits the truth — the pointer + the live probe is the whole
task-state. **The anti-bluff `PROBES.md` manifest (P1–P7) is the load-bearing carrier.**

---

=== PROBES.md ===

# Probe manifest — ai-council architect: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts, task-line
> text, or orienting lines are stated. That withholding IS the teeth. The pass criterion is **"answered
> from the live source at check-time,"** never "matches a remembered number."
>
> **CROSS-REPO — run these in the ai-council checkout (load-bearing).** This bundle is *hosted* in the
> hub (`.dev-knowledge`, ADR-36/41 read-only-on-target) but its **subject is `ai-council`**. Every command
> below runs in the **ai-council** working copy. The probes are re-bound to ai-council's own surfaces
> (`scripts/validate_backlog.py`, `scripts/check.ps1`, its `BACKLOG.md` / `VISION.md` / `ARCHITECTURE.md`);
> the hub's `audit.py ship-gate` / `ALL_CHECKS` / `doc-counts` / disposition-register probes are
> **deliberately absent** — ai-council carries no such surfaces, so a hub-bound probe would FAIL
> `anchor-missing` by construction rather than testing anything.
>
> **Branch note.** This bundle was cut on hub branch `docs/ai-council-architect-handoff`. That names only
> where the *artifact* lives — **re-derive ai-council's HEAD / tree / branch / ahead-behind live (P2); do
> not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of ai-council `VISION.md` `## Vision` — *what ai-council is*. | ai-council `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of ai-council `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *what the system does*. | ai-council `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | What is ai-council's current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how far **ahead of / behind** `origin` is it? | live git (the **ai-council** checkout) | the summary holds a generation-time state; this window closed with merges still landing, so a baked sha is stale on arrival | `git rev-parse --short HEAD` then `git status -sb` |
| P3 | How many **themes / stories / tasks** does `validate_backlog` count in ai-council's `BACKLOG.md` right now, and does it report `OK` with zero warnings? | ai-council `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map moved hard this window (#33 struck, #44 closed, #69–#72 filed, #68 re-prioritized) — neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py` |
| P4 | Quote, **substring-exact**, the two **P2 silent-failure task lines — #69 and #71** — including their bracketed priority/size tags, confirming the ready slack is read from the live story-map and not paraphrased from this bundle. | ai-council `BACKLOG.md` story-map (#69, #71) | both lines were authored *after* the compaction window and are byte-fixed in the live file; a summary paraphrases the pair and cannot reproduce the exact `- [#69] …` / `- [#71] …` text; this bundle states none of it | `grep -nE '^- \[#(69\|71)\]' BACKLOG.md` → the browser's quote must be a substring of a live matched line |
| P5 | Are ai-council's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`, and is `core.hooksPath` unset? | the ai-council checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` |
| P6 | Does the repo gate pass **right now** — what does `check.ps1` **exit**, how many tests pass, and does `mypy src/` report clean? | ai-council `scripts/check.ps1` (pytest + mypy + ruff) | the pass-count and the mypy verdict are live build facts that drift on any merge; the `types-PyYAML` declaration landed *this* window, so the green claim is exactly what must be re-derived rather than trusted — the residual states neither value | `pwsh -File scripts/check.ps1` (or `py -m pytest -q` then `py -m mypy src/`) → read the exit code + the counts |
| P7 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in ai-council's `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` passes unreconciled. | ai-council `BACKLOG.md` ∩ `scripts/validate_backlog.py` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded | `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then P4**, which anchors this window's ready slack (#69/#71) in the live
   story-map. **Then the operator-context beat (§13d), NARROWED** — the supplement is FILLED and its
   ANSWERS are in the paste, so ask only *"anything changed since the supplement was written?"*.
   Then P2, P3, P5, P6, P7 — each against **live ai-council state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P7 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P6 is the headline gate (exit code + test count + mypy verdict);
   P7 grooms the whole open BACKLOG at boot. First re-derive which branch is live (P2), then re-derive
   every load-bearing fact from the live primary source.

---

=== SUPPLEMENT.md ===

ANSWERS — outgoing architect (2026-07-19, ai-council)

FRAME FOR THE INCOMING SESSION: the operator's three themes are the mission and the operator's
standing expectation is EXECUTION — implement, archive what is implemented, implement what is
meant to be implemented. A session that produces another intake, audit or ADR instead of shipped
behaviour will be judged a failure regardless of its quality. An intake/ADR MORATORIUM is in force
by operator declaration until implementation debt clears; the only permitted ADR is one that
RECORDS a decision already in effect (as ADR-13 did for the 1.0 stamp), never new design.

1. STRATEGIC INTENT (way-of-working level)
Shift the ratio from producing governance artifacts to discharging them, and make that shift
mechanical rather than remembered. Three way-of-working goals, in order:
(a) Every artifact carries its own deployment status and its own EXIT CONDITION. This session
    started the pattern — 56 Deployment-Status stamps, a docs/audits "Live corpora" registry whose
    operative line is "an unregistered folder is indistinguishable from a leftover", and exit
    conditions per live corpus. The next session finishes it by making it enforced: #67 (reject a
    staged SEALED-KEY*.json) and #68 (registry check for new docs/ directories) are specified and
    unbuilt, and the cli4-parity registry row is retired by hand until #68 ships.
(b) Verification-before-claim as a MECHANISM. scripts/verify_night_consolidation.py now re-runs
    eight shipped-behaviour legs and prints PASS/FAIL; extend that pattern per arc so "merged" can
    never again be reported as "deployed". Merged is not deployed; this was the single most
    load-bearing distinction of the session.
(c) Plan-then-build in ONE session for T1. The recurring failure across this repo is that design
    accumulates and code does not. The T1 planning session must end with frozen build contracts AND
    the first arc built, not with another design document.
Default execution shape for any audit/review-scale work: orchestrator + fan-out (Opus orchestrates
and owns all git mutations serially in the main thread; Sonnet takes bounded legs in parallel;
Haiku takes cheap read-only sweeps; Codex sol derives independently, terra reviews). Serial
single-thread orders for read-heavy multi-module work are a routing failure.

2. TENSIONS WEIGHED
(a) Ship-with-waivers vs hold-for-review. Landed: ship, with a recorded waiver per arc plus one
    batch re-review item. Reason: holding seven S-size arcs for five days was pure latency.
    CORRECTION THAT MATTERS MORE THAN THE RULING: the premise was false. Terra was live the whole
    time — a one-line probe settled it that night ("TERRA-OK"). The waiver stack rested on an
    assumption nobody tested. Lesson for the next architect: verify tool availability empirically
    before letting it gate sequencing.
(b) 1.0 stamp on §7-empty vs waiting for #34. Landed: stamp on §7-empty (operator D2(a)). Reason:
    CONTRACT §5 already declares the verdict package debate-path-only with #34 referenced — a
    documented scope is not a lie, an undocumented gap would be; #34 bumps 1.1, which is what a
    versioned ABI is for. Honest caveat: terra later found #62/#63/#69 beneath that surface. The
    stamp remains defensible (it speaks to declared scope, not defect-freeness) but 1.0 shipped
    with three silent-failure hazards filed under it.
(c) Corpus blessing vs "just run it" for #27. Landed: operator blessed the 12 briefs before freeze.
    Reason: the freeze is irreversible (no swaps once a pair has run) and 24 billed debates are the
    price of a wrong corpus.
(d) Paid live E2E verification vs $0 offline proof. Landed: $0 offline — MockProvider and canned
    CLI output driving the REAL shipped code, with everything un-exercisable recorded as an
    explicit GAP rather than a fake PASS. Cost of the choice: the token-count leg is verified at
    adapter level, not production seat routing (gated on the §5 flip).
(e) Archive-now vs keep-in-place for live corpora. Landed: keep in place, register them. Reasons:
    the archive zone's own README admits only completed artifacts with no open remainder, so filing
    a live instrument there mislabels it as finished; and relocating would have forced a .gitignore
    rewrite that recreates the exact condition under which a SEALED-KEY.json was nearly staged.
    The hygiene problem was never "a folder exists" but "you cannot tell why it is there".
(f) Parallelism vs primary-state integrity. Landed: worktree for ANY task with side effects
    regardless of size; commit-and-STOP; the operator is the serial merge gate. Reason: the cost is
    not merge conflict, it is the primary losing trust in its own state.

3. CONSIDERED + REJECTED — do not relitigate
- Blanket ban on directories under docs/ — rejected: it would reject archive/ itself and both
  legitimately registered live corpora. #68 is a registry check instead.
- Moving EPI-1 into docs/audits/archive/ — rejected on three independent grounds (the 2026-07-18
  retention ruling; the archive's "no open remainder" contract; the .gitignore seal-exposure
  hazard). It stays, with a condensation markdown as its front door.
- Moving or summarizing cli4-parity before unseal — rejected: it is the live blind trial and the
  operator needs those artifacts in front of him to score.
- Editing the three docs/smoke references — rejected: accurate historical prose in append-only
  records; editing violates ADR-29 / CLAUDE.md §5.3.
- Blanket-striking #44 — rejected: it would have recorded three unreviewed merges as reviewed.
  Narrowed, then discharged by an actual live review.
- n=8 pilot for #27 — rejected: below the rubric's own n=12 floor; a trial that cannot ratify burns
  its whole spend.
- Claude-only parity with the codex arm deferred to #43 — rejected in favour of a TRIAL-SCOPED
  gemini synthesizer, which frees the openai API seat and gives codex a clean transport-only pair.
  The durable openai default is untouched.
- Reusing night-batch pins (claude-haiku, unpinned codex default) — rejected: not
  transport-only-correct. Operator ruled newest-models, identical both arms: claude-opus-4-8 and
  gpt-5.6-terra (the medium tier, not the flagship).
- Building #43 before #27 — rejected: scope expansion mid-window.
- An env-only variant of #39 in the worktree — rejected: splitting flag/env across two arcs is a
  follow-up for no gain.
- A third mypy ignore for the PyYAML stub — rejected: two stub-class gate failures in one day meant
  the gate was drifting to expected-red. types-PyYAML declared in dev extras; #20 widened from the
  openai 2.x migration to type-stub hygiene generally.
- Generating a handoff bundle before scoring — rejected: it would be stale the moment the flip
  decision lands (the exact failure mode already filed to the hub as #343).

4. OPEN QUESTIONS / DELIBERATELY DEFERRED
- THE decision: #27 blind scoring → unseal → ratify or retire DRAFT-CLI-3 and amend ADR-12 §5.
  Threshold: CLI fails at most one more pair than API per rubric item (margin 1/12), ZERO margin on
  items 2 (no hallucinated consensus) and 4 (faithfulness); regression on 2/4 across two attempts
  retires the flip.
- #43 — the codex CLI seat has no API twin, so the ADR-12 same-seat fallback assumption breaks.
  What are the fallback semantics when the CLI lane is unavailable and no codex API provider
  exists? A genuine design decision, sized M, blocking a first-class codex seat name.
- #69's second half — --file and --inbox resolve the panel through different guards (interactive
  `not eff_full` vs inbox `not use_full_panel`), so the same brief yields different panels. This is
  the CLAUDE.md §10 inbox-parity anti-pattern and needs a ruling on which lane is canonical before
  anyone patches it.
- §6.3 scope-boundary fork (pure governance vs thinking aid) — still unadjudicated, carried.
- Hub-owned and awaiting hub rulings: #341 (Codex-as-producer vs the global read-only AGENTS.md and
  the Windows write sandbox) and #343 (Stop-gate must block handoff-bundle generation until
  session-close criteria hold; consumer-session guard against hub writes). Interim fallback in
  force meanwhile: CC produces, terra reviews read-only, Codex never plans as producer.
- #33 carries an asterisk: pass-3 returned CLEAN but terra crashed mid-pass on a tempfile error
  after real analysis; re-runnable if certainty is wanted.
- T1 in its entirety — #18 (tool-grounded crux resolution), #19 (debate-time framing defense), #9
  (must reconcile with #36, not duplicate it), with #55 (G5 baseline/self-consistency experiment)
  as input. Zero code, zero design.
- The live-corpora registry is maintained by hand until #68 ships; #27's done-when now carries the
  retirement obligation so the surface cannot rot in the meantime.

5. DECOMPOSITION RATIONALE
The dependency order is not arbitrary. T3 (the inter-repo protocol) went first because other repos
consume it and a moving contract cannot be depended on — it is now at 1.0 with CONTRACT §7 empty,
verified by eight legs, with the remainder being #34 (→1.1), the caller-side advisor
[S13]/#36–#38, and the robustness trio #62/#63/#69 sitting UNDER the 1.0 surface. T2 (the CLI
engine) comes next because it is evidence-gated, not design-gated: everything is built and proven
at $0, and the only missing piece is a quality proof that costs exactly one operator sitting —
the highest value per operator-minute in the backlog. T1 (de-bias) is last in sequence but largest
in remaining scope, and because it is design touching no contended module it can run in parallel
with anything.
The next session must NOT redo or re-decide: G3 / the synthesizer ruling (resolved; EPI-1 retained
unscored as the reversal instrument, condensation markdown is its front door — do not re-score);
the verdict-package design or the five seam contracts (shipped); the 1.0 stamp trigger (D2(a));
the archival and registry rulings; Codex-as-producer (hub-owned); the frozen #27 corpus or the
trial pins. Do not touch docs/audits/2026-07-18-cli4-parity/ or either sealed key before unseal.
Do not write new intakes or ADRs.

6. OFF-REPO CONTEXT
- The operator's words this session: "Execution, execution, execution." He is explicitly
  frustrated by the ratio of governance artifacts to shipped behaviour. The moratorium is his.
- Terra is LIVE. The "codex credits exhausted until 2026-07-23" premise governed an entire day of
  waivers and was false. From now: terra review per code-impact arc, no waivers. Codex under-use
  is treated as a routing failure, and the lanes are fixed: sol for adversarial/independent
  derivation, terra as the default code review, luna for cheap read-only fan-out.
- Operator scoring time is the scarcest resource in the system. Design every evidence exercise to
  fit one sitting.
- Nothing counts as working until it has been run and compared. The operator demanded and got a
  by-eye CLI-vs-API smoke pair on a fresh question: both arms reached the same verdict with the
  same strongest argument and overlapping blind spots, at $0.000000 seat cost versus $0.281677,
  roughly 30 seconds slower. That standard applies to every claim.
- Operating discipline the operator enforces personally: any order that could create a repo path
  must NAME the path (new folders are hard-gated; convention-compliant new files proceed with a
  citation); anything with side effects runs in a worktree regardless of size, and the architect
  proposes the worktree unprompted.
- Finally, a candid note for the incoming architect: this session's outgoing architect made three
  same-class misses — orders that would have edited immutable records — plus several assertions
  from unverified premises (a witness mechanism that did not exist, a merge conflict that was not
  real, a review lane assumed dead). The executing lane caught every one and was right every time.
  Treat CC's pushback as the system working, and verify your own premises against live state before
  you assert them; that is where this role's worst failures live.
