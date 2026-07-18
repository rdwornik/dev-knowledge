=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode · P6 window completion)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-17-ai-council-architect-p6-window-completion` |
| **Chat title** | `[ai-council] Architect — P6 window completion — 2026-07-17-ai-council-architect-p6-window-completion · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working posture; the session's WORK is small **product BUILD** — the ADR-11 D2 parity pair) |
| **Target repo** | `ai-council` — this bundle lives in the hub .dev-knowledge (ADR-36/42: the hub is the sole handoff carrier; consumers hold no docs/handoffs/ surface). **Run every probe command IN the ai-council checkout.** (The cross-repo probe resolver reads the first backtick span of this row as the target root — it must be `ai-council`.) |
| **Purpose** | **P6 completion wave.** The prior session **closed clean** (P4 build wave COMPLETE — doctor #25 → CLI seats #16 → verdict package #26 — plus a night E2E audit + a morning close). This session drives, in order: (1) the **ready slack #22 + #23** — the ADR-11 **D2 parity closure** (CONTRACT §7 known-deviations: `--file` frontmatter parse #22 + research `--return-dir` #23), both **UNBLOCKED**; closing both **empties CONTRACT §7 → triggers the DRAFT-INT-2 `1.0` version stamp**; (2) the **night-finding hardening fixes #39–#43** (no-persist/scratch output guard #39 · `options_considered` extractor #40 · CLI-seat token regexes #41 · research double-prefix #42 · first-class `codex` seat name #43); then (3) **#27 CLI-4 parity** as the follow-on centerpiece — **un-gates the ADR-12 §5 default-flip**. **Date-gates to flag:** **#33** (terra pass-3) and any terra-gated review are runnable only **on/after 2026-07-23** (codex credits reset). **G3 / Epic B is RESOLVED by operator ruling** (not scoring) — do not re-score. Navigate via ai-council `BACKLOG.md` [E1]/[S10] + the night audit `docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` §4.2 gap-map; the RESIDUAL carries only what the repo does not already encode. |
| **Generated at** | Hand-authored in the hub from **READ-ONLY live git** of `../ai-council` at the **2026-07-17 session close** (P4 wave complete + night batch + morning close all merged; session closed clean). States **no** sha / count / verdict / armed-state — **re-derive HEAD / tree / branch / counts / hooks live in the ai-council checkout** (`PROBES.md` P1–P3) and read the live ready-slack from BACKLOG (P4). |

> **`SUPPLEMENT.md` is FILLED** by the outgoing session CC (which drove the P4-wave close + night batch + morning close). The incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written (2026-07-17)?"* — it does not fire full.

> **Anti-bluff in effect (read `PROBES.md` header).** This bundle **withholds every probe answer value** by construction — no SHAs, counts, region text, phase-table lines, or armed-state. The withholding IS the teeth; run the commands **in the ai-council checkout**.

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

# Residual — 2026-07-17-ai-council-architect-p6-window-completion — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the ai-council `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is a small **product BUILD** (the D2 parity pair + the night-finding hardening fixes #39–#43). **Target repo: ai-council** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../ai-council`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the ai-council plan-of-record / JOURNAL / git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED** by the outgoing session CC (P4-wave close + night batch + morning close); the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* (not full).

---

## §1 — Prior session CLOSED CLEAN; the P6 completion wave is #22/#23 → #39–#43 → #27 (THE HEADLINE)

**The P4 build wave is done AND the session closed clean.** `recall`: doctor (**#25**), CLI seats claude+codex (**#16**), verdict package (**#26**) all shipped; then the session closed properly — a **pre-authorized unattended night E2E audit** (zero stop conditions fired) + a **supervised morning close** landed four more merges on `main`: night deliverables → a durable **synthesizer swap** (`defaults.synthesizer: gemini → openai`, gated green, terra-waived — codex credits exhausted to 2026-07-23) → doc-currency + BACKLOG hygiene (**#31 struck, #24 closed by operator ruling, #39–#43 filed**) → JOURNAL. **P1 re-derives HEAD live** — it has moved well past the P4 merges; do not trust any sha in prose. The sidecar seam rule held: `seats[]` (#16) defined the `_metrics.json` extension mechanism; the verdict package (#26) consumed `seats[]`/`synthesis` **by reference** via a shared `_seat_payload` serializer.

**The P6 completion wave, in order.** Canonical sources: ai-council `BACKLOG.md` (#22/#23 ready-slack) + `protocols/COUNCIL_INVOCATION_CONTRACT.md` §7 (Known deviations) + the night audit `docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` §4.2 gap-map (the next-wave menu — POINT at it, do not re-narrate it).

1. **Ready slack — #22 + #23 (the ADR-11 D2 parity pair, both UNBLOCKED).** **#22** — `--file` parses YAML frontmatter via the same `parse_file()` path as inbox (precedence flag > frontmatter > config default; no frontmatter leaks into the question text). **Likely quick:** the `--file` gap "falls out of" the `cli.py:main` `@click.group` decomposition that **already landed with #25 (A2)** — structural basis exists; a small wiring + test task. **#23** — research mode honors `--return-dir` (`run_research` gains a return-dir copy; canonical `./output/` always; re-confirmed empirically open by the night batch). **Closing both empties CONTRACT §7 → triggers the DRAFT-INT-2 `1.0` version stamp** (per L-INT Q7: a `1.0` shipped with known deviations "would make the first version a lie") — at which point the verdict package's `contract_version` field (currently `null`, shipped by #26) starts echoing `1.0`. **That is P6 window completion.**
2. **Night-finding hardening — #39–#43** (all filed from the night E2E audit; harden the artifact surface): **#39** no-persist/scratch output mode + bounded `output/health/` retention (witness runs pollute canonical `output/`); **#40** fix the verdict-package `options_considered` extractor (empty on picks, polluted on ideas); **#41** CLI-seat token-count regexes (codex records 0, claude under-reports input); **#42** research-path double-prefix filename; **#43** first-class `codex` seat name in the provider registry (it rode `deepseek` in the night batch).
3. **Follow-on centerpiece — #27 CLI-4 parity** (n=12 stratified, sealed-key blind, rubric-scored). Prereq #16 landed; the night batch's zero-fallback CLI E2E de-risks it. **Un-gates the ADR-12 §5 default-flip.**

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or task-line text.

---

## §2 — The #26 residuals + seam constraints still in force (the design context)

**#26 (verdict package) shipped debate-path-only and filed three residuals — do NOT redo, but know they exist:**
- **#33** [P3][S] — **terra pass-3 re-verification, DATE-GATED on/after 2026-07-23.** #26's terra pass-3 was **explicitly waived** (codex credits exhausted mid-gate); pass-1/pass-2 were clean-on-substance after fixes, the two pass-2 fixes are strictly reductive + unit-tested, and the waiver was offset by a fresh live re-witness on the shipping code. #33 runs `codex-review.ps1 -Topic verdict-package-pass3` when credits reset — belt-and-suspenders, not a blocker.
- **#34** [P3][M] — research-path verdict-package parity (R6): `run_research` emits no `council-verdict-*.json` (debate-path only). A Lane A **research** commission gets no transcript-free deliverable until this lands.
- **#35** [P3][S] — broad R4 fail-loud return-dir for transcript/minority (#26 made only the *verdict* raise `OutputRoutingError` on a required-return-dir miss).

**Seam constraints unchanged (design against, never redesign):** the five cross-lane seam contracts are canonical in ai-council `docs/intake/2026-07-06-technical-architect-intake.md` §3. `output.py` remains the highest-contention module (now carries `save_to_file`/`_build_header`/`_build_body` + the verdict package + `seats[]` sidecar via `_seat_payload`) — serialize any work touching it. **Do-not-touch reference module: `healthcheck.py`.**

---

## §3 — Carried residuals (still live — NOT re-derivable from the repo alone)

**(a) G3 / Epic B is RESOLVED — by operator ruling, not by scoring.** `#24` (EPI-1 archaeology) is **CLOSED by operator ruling**. The G3/Epic-B event is the recorded **synthesizer ruling** — ai-council `docs/audits/2026-07-17-synthesizer-ruling-gemini-to-openai.md` (durable `defaults.synthesizer: gemini → openai`, ratified on the night batch's 4/4 empirical corroboration). The EPI-1 40-item pack + sealed key are **RETAINED UNSCORED as the standing reversible instrument** (`docs/audits/2026-07-17-epi1-archaeology/`) — reopen the scoring only if evidence later argues to reverse. **Epic B is formally un-gated:** #2 Branch A (openai) shipped as the durable config default (ADR-01 amendment text pending), and **#18/#19 planning is deferred to a dedicated planning session** on the un-gated baseline — do NOT re-score, re-rule, or start #18/#19 design in this window-completion chat.

**(b) The two consumer→hub NEEDS-RULING intakes — both hub-tracked, ruling pending (do NOT re-plan them here).** Filed locally in ai-council `docs/intake/`, carried across the boundary to the hub (the sanctioned consumer→hub path):
- `2026-07-17-hub-feedback-codex-producer-lane.md` (EPIC-H) — Codex-as-PRODUCER vs the global read-only `~/.codex/AGENTS.md` policy + the Windows write-sandbox. **Hub-tracked as `.dev-knowledge` BACKLOG #341** (per-invocation producer activation without global-infra edits).
- `2026-07-17-hub-feedback-session-close-gate.md` — (Ask 1) the Stop-gate must **mechanically block handoff-bundle generation** until session-close criteria hold (this very bundle was generated mid-session and had to be updated post-close — the exact failure mode); (Ask 2) a **consumer-session guard against hub/global writes**. **Hub-tracked as `.dev-knowledge` BACKLOG #343** (filed this hub session). Both await an operator ruling — a HUB session's work; the browser should not re-plan them.

**(c) Interim Codex-producer fallback — IN FORCE (operator ruling 2026-07-17).** Until the hub reconciles #341: **bounded build tasks run as CC-implements + terra read-only review (`codex exec review`) pre-merge.** This shipped #25/#16/#26 cleanly (terra caught real defects each arc). **Apply to #22/#23 + #39–#43:** CC produces; terra reviews read-only; never plan Codex to write. **Terra-rate-limit lesson:** codex `exec` can hit its usage cap mid-gate (credits exhausted to **2026-07-23**) — if it does, the pattern is an **explicit recorded waiver + a filed follow-up** (like #26 pass-3 → #33), never a silent skip.

**(d) §6.3 scope-boundary fork — still awaiting an explicit ruling.** The plan-of-record / consolidation-brief §6.3 fork (pure-governance vs thinking-aid scope) is implicitly held at "pure governance" but **NOT formally adjudicated** (night audit §4.2) — the one fork worth an explicit ruling. Carry-open; not this window's job unless the operator raises it.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — close the ADR-11 D2 parity window (#22 + #23) → stamp DRAFT-INT-2 `1.0`, then harden (#39–#43), then #27 parity (§1).** The whole-system view the architect must hold: #22 likely falls out of the already-landed A2 `@click.group` decomposition (small); #23 threads `return_dir` through `run_research`; closing both empties §7, the sole precondition for the `1.0` stamp — at which point the verdict package's `contract_version` field starts echoing `1.0` instead of `null`. #39–#43 harden the artifact surface (output-guard / extractor / token-regexes / naming / seat-identity) — the night E2E audit's concrete findings, sized S each. #27 (CLI-4 parity) is the follow-on centerpiece that un-gates the ADR-12 §5 default-flip. Lane parity is a standing contract obligation (L-INT R6): any behavior added to Lane A states its Lane B disposition (#34 is the one place the verdict package is not yet lane-complete).

**Carry-open (do NOT redo / re-decide in this chat):**
- **#33 (terra pass-3)** — date-gated on/after **2026-07-23**; run it then, do not force it early (codex credits). Any other terra-gated review is likewise blocked until the reset.
- **G3 / Epic B is RESOLVED by ruling (§3a)** — #24 closed, the EPI-1 pack retained as the reversible instrument. Do NOT re-score or re-rule; #18/#19 planning is a **separate** dedicated session on the un-gated baseline.
- **The two hub NEEDS-RULING intakes (§3b)** are hub-tracked (#341 codex-producer, #343 session-close-gate) — a **hub** session's ruling; use the interim fallback (§3c) meanwhile.
- **The §6.3 scope-boundary fork (§3d)** — awaits an explicit ruling; not this window's job unless raised.
- **[S13]/#36–#38 (caller-side commissioning advisor, filed by RIDER 2)** — the front half of the delegation window (authoring → decomposition → verdict→ADR read-back), companion to the council-side surface [S10] delivered. Filing only; build when prioritized. #36 must reconcile with #9 (the ADR-67 quality gate, [E6]-deferred), not duplicate it.
- Any **methodology / hub** question → the hub `.dev-knowledge`.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the ai-council **`BACKLOG.md`** (story-map, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2; the ready-slack #22/#23 read live, `PROBES.md` P4) + the frozen **`docs/intake/2026-07-16-plan-of-record.md`** phase→task map (**P6 = #22/#23**) and the night audit **`docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md`** §4.2 gap-map (the next-wave menu), the live branches (`git branch -v` — P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. **New since the P4 close (morning close of the night batch):** **#31 struck** ([S12] delivered), **#24 CLOSED by operator ruling** (G3/Epic-B = the synthesizer ruling; EPI-1 pack retained as the reversible instrument), **#39–#43 filed** from the night E2E audit; #2 Branch A (openai) shipped as the durable config default (ADR-01 amendment text pending). Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier.**

---

=== PROBES.md ===

# Probe manifest — ai-council P6 window completion: anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE ai-council checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, phase-table text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub; its probes bind to **ai-council** — run them in the ai-council checkout. The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the ai-council checkout) | the summary holds a generation-time state; the #26 close + session-wrap already moved HEAD past the merges this residual names — a baked sha goes stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK` with zero warnings? | ai-council `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map moved this session (wave tasks #16/#25/#26 struck; #33/#34/#35 + new story [S13]/#36–#38 filed) — neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`, and is `core.hooksPath` unset? (SessionStart `pre-commit install` arms all three.) | the ai-council checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` |
| P4 | Quote, **substring-exact**, the two **ready-slack task lines (#22 and #23)** — the ADR-11 D2 parity closure pair (`--file` frontmatter · research `--return-dir`) — and their `[P2][S]` size tag, confirming the ready-slack scope is read from the live BACKLOG story-map, not paraphrased from this bundle. (The night audit §4.2 gap-map is the corroborating next-wave menu.) | ai-council `BACKLOG.md` story-map (#22/#23), corroborated by the night-batch E2E audit §4.2 gap-map | the #22/#23 task text + their gates are byte-fixed in the live BACKLOG; a summary paraphrases the ready-slack pair and cannot reproduce the exact `- [#22] … · post-pause (G2)` line; the bundle states none of it | `grep -nE "#(22|23)\]" BACKLOG.md` → the browser's quote must be a substring of a live matched line |

## Gate procedure (CC)

1. **P4 first** — the forced ready-slack read orients the session: it anchors the window-completion scope (ADR-11 D2 parity → #22/#23) in the live BACKLOG story-map before design begins. **Then run the §13(d) operator-context beat NARROWED** (the supplement is FILLED — ask only *"anything changed since it was written?"*). Then P1–P3, each against **live ai-council state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move — re-derive it live, do not trust the residual's prose.

---

=== SUPPLEMENT.md ===

ANSWERS — outgoing architect (2026-07-18, revised: continuation emphasis)

FRAME FOR THE INCOMING SESSION: the operator's three product themes are the
mission, and NONE of them is finished. (T1) de-biased, higher-value debate;
(T2) CLI-subscription engine replacing API spend; (T3) the delegation-window
protocol for other repos. P4 built foundations under all three; the next
sessions CONTINUE them — completion of the window is a milestone on that road,
not the destination.

1. STRATEGIC INTENT: continue the three themes in dependency order. T3 first —
finish the protocol so other repos can rely on it: empty CONTRACT §7 (#22/#23),
harden the artifact surface (#39–#43), research-path parity (#34), then an
honest Contract-Version: 1.0 (a 1.0 with known deviations would be a lie —
L-INT Q7). T2 next — #27 parity (n=12) to EARN the ADR-12 §5 default flip;
until the flip, the cost thesis is proven ($0 CLI lane witnessed) but not
harvested. T1 is now un-gated and has ZERO code built — #18 (tool-grounded crux
resolution) + #19 (debate-time framing defense) + #9 get a dedicated planning
session; they are the largest unfinished half of the mission, not an afterthought.

2. TENSIONS WEIGHED: (a) evidence vs operator authority on G3 — resolved by
authority, de-risked by the retained sealed EPI-1 pack + the night's 4/4
corroboration of openai synthesis; chosen deliberately to keep operator scoring
time (the scarcest resource) off the critical path of T1. (b) terra outage vs
review discipline — explicit recorded waivers, never silent passes; #33 is the
dated backstop (2026-07-23). (c) unattended autonomy vs safety — pre-authorized
night batch, hard stop conditions, zero fired. (d) completion vs new build —
T3/T2 completion work is deliberately sequenced BEFORE T1 design so the protocol
other repos consume stabilizes first.

3. CONSIDERED + REJECTED (do not relitigate): re-running the LLM-judge over
EPI-1 (moot-by-ruling + duplicates the existing second-opinion note); extending
the night batch into code fixes (no unattended edits); a fresh bundle instead of
updating this one (operator ruling: update in place); treating the wave's
completion as mission completion (rejected — the three themes remain open).

4. OPEN / DEFERRED: T1 design entirely (#18/#19/#9 — un-gated, unplanned; own
session); T2 flip evidence (#27); T3 remainder (#22/#23, #34, 1.0 stamp, and
the caller-side advisor [S13]/#36–#38 — the operator's named front half of the
delegation window). The two hub NEEDS-RULING intakes (codex-producer,
session-close-gate) await rulings. §6.3 scope fork unadjudicated. ADR-01
amendment for the synthesizer swap owed if convention requires. Whether #22
truly falls out of the landed A2 — verify against live cli.py first.

5. DECOMPOSITION RATIONALE: #22/#23 → #39–#43 → 1.0 stamp → #27 (T3 then T2),
with the T1 planning session schedulable in parallel to any of it (it is
design, not code, and touches no contended module). #22/#23 are disjoint
(cli.py --file vs run_research). Do NOT re-derive the verdict-package design or
seam contracts (shipped), re-score/re-rule G3 (resolved; pack retained as the
reversal instrument), or re-plan Codex-as-producer (interim fallback in force).

6. OFF-REPO CONTEXT: operator's standing priorities are the three themes, in
his words: CLI engine, the inter-repo protocol with an advisor front-end, and
minimized cognitive bias in the debate. None is declared done by him. Terra
returns 2026-07-23. Operator scoring time stays scarce; the EPI-1 pack remains
his one-evening reversal instrument if openai synthesis quality ever disappoints.
