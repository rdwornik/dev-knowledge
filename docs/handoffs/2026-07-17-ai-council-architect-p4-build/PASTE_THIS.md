=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode · P4 build wave)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-17-ai-council-architect-p4-build` |
| **Chat title** | `[ai-council] Architect — P4 build wave — 2026-07-17-ai-council-architect-p4-build · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working posture; the session's WORK is **product BUILD**) |
| **Target repo** | `ai-council` — this bundle lives in the hub .dev-knowledge (ADR-36/42: the hub is the sole handoff carrier; consumers hold no docs/handoffs/ surface). **Run every probe command IN the ai-council checkout.** (The cross-repo probe resolver reads the first backtick span of this row as the target root — it must be `ai-council`.) |
| **Purpose** | Drive the **P4 build wave** in ai-council — **#25 doctor → #16 CLI seats (claude+codex) → #26 verdict package**, per ai-council `docs/intake/2026-07-16-plan-of-record.md`. Enforce the **sidecar seam rule** (first lane defines the extension mechanism, never built concurrently) and the **refactoring-guide pre-work map** (A2→doctor, A1→A3→CLI seats, A4→verdict package). **Feature-work pause is LIFTED** (ai-council `2a00c37`, G2). Navigate the build via ai-council `BACKLOG.md` [E1]/[E3] + the plan-of-record; the RESIDUAL carries only what the repo does not already encode. |
| **Generated at** | Hand-authored in the hub from **READ-ONLY live git** of `../ai-council` (hub is the carrier; no write ever touches the consumer). States **no** sha / count / verdict / armed-state — **re-derive HEAD / tree / branch / counts / hooks live in the ai-council checkout** (`PROBES.md` P1–P3) and quote the phase table live (P4). |

> **`SUPPLEMENT.md` is FILLED.** The outgoing architect chat answered the 6-question strategic interview (+ the two CC-observed addenda A/B); the ANSWERS region is folded into `PASTE_THIS.md`. The incoming §13(d) operator-context beat therefore **NARROWS** to *"anything changed since the supplement was written (design 2026-07-16, filled 2026-07-17)?"* — it does not fire full (Q6 already carries the off-repo context).

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

# Residual — 2026-07-17-ai-council-architect-p4-build — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the ai-council `BACKLOG.md`, §6). Mode: **architect** (§13); the session's WORK is **product BUILD**. **Target repo: ai-council** — this bundle is hosted in the hub (ADR-36/42), derived READ-ONLY from `../ai-council`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the ai-council plan-of-record / JOURNAL / git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** The outgoing architect's answers are folded into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* (not full).

---

## §1 — Pause LIFTED + the build spec (THE HEADLINE)

**Feature-work pause is LIFTED.** `recall`: G2 (consolidation + GOV-1, ai-council `#31`) lifted the pause; the lift merge is ai-council **`2a00c37`** (`witnessed` at derivation as the ai-council `main` HEAD — **P1 re-derives live**, it will have moved once the build wave commits). The build wave (**P4**) and the post-pause quick unlock (DOC-3, shipped `#30`) were gated on G2; they are now runnable.

**The build spec is the plan-of-record — design AGAINST it, do not redesign.** Canonical source: ai-council `docs/intake/2026-07-16-plan-of-record.md` (the operator's frozen phase plan, materialized). This chat's job is to drive **P4 build wave 1** in order:

1. **#25 doctor** (P4) — pre-work **A2**: decompose `cli.py:main` → a `@click.group` with `run` / `doctor` subcommands. `doctor` consumes `healthcheck.py` — **never rewrites it** (do-not-touch reference module). Same-module adjacencies A5/B5/B7 touch `cli.py`; land the A2 decomposition first.
2. **#16 CLI seats (claude + codex)** (P4, existing task) — pre-work **A1 → A3**: template-method provider base, then the one error classifier + timeout/retry contract (the five-token cause vocabulary = `seats[].fallback_events[]`). A4/B3/B7 touch `output.py`/`policy.py`.
3. **#26 verdict package** (P4) — pre-work **A4**: decompose `save_to_file`; `save_verdict_package` lands as a **sibling** (never more lines in `save_to_file`) + **B3** (shared tz-aware timestamp helper for the deterministic `<ts>`). Emits `council-verdict-<ts>-<mode>-<slug>.json` per DRAFT-INT-1 — a transcript-free caller deliverable.

**"A1, A2, and A3 are the load-bearing three"** (refactoring guide, via plan-of-record §5). Part A structural = unblocks the wave; Part B mechanical = do anytime.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P4), not in trusting these lines.** This bundle states **no** sha, count, armed-state, or phase-table text.

---

## §2 — The sidecar seam rule + contention map (the design constraint that governs ordering)

**Sidecar seam rule (frozen, verbatim):** *first lane defines the extension mechanism, never built concurrently.* Concretely: `seats[]` (from L-CLI, i.e. #16) and `synthesis` (from L-EPI) both extend the `_metrics.json` sidecar — **whichever lands first defines how the sidecar is extended; the second conforms.** Serialize; never build both extensions in parallel sessions. **The verdict package (#26) is NOT a sidecar extension** — it is a separate caller-facing artifact (the sidecar is telemetry; the package is the deliverable); it consumes `seats[]`/`synthesis` facts **by reference** and designs neither.

**The five cross-lane seam contracts are canonical in the intake §3** (ai-council `docs/intake/2026-07-06-technical-architect-intake.md`) — **design against, never redesign**: (1) metrics sidecar namespacing, (2) doctor ownership (L-DOC owns; L-INT consumes as optional pre-flight; L-CLI contributes exactly the identity re-probe), (3) Epic B gate (L-EPI owns), (4) parity evidence (L-CLI owns; only CLI-4 results ratify the ADR-12 §5 flip), (5) enforcement (L-GOV owns; hub-carrier work is a hub arc).

**Contention map (plan-of-record §5):** `output.py` is the **highest-contention** module of the wave (A4 + B3 + `seats[]` sidecar + verdict package) — **serialize** work touching it. `cli.py` is second (A2/A5/B5/B7 + doctor). Do-anytime, no deps: B2, B3, B4, B5, B6, A5. **Do-not-touch reference module:** `healthcheck.py`.

---

## §3 — Carried residuals (the three the operator flagged — NOT re-derivable from the repo alone)

**(a) G3 is OPEN — the operator's blind-scoring mission, un-gates Epic B.** `#24` (EPI-1 archaeology) is **prepped but unscored**. An overnight-prepared **40-item blind-scoring pack** sits at ai-council `docs/audits/2026-07-17-epi1-archaeology/` (`OPERATOR-SCORING-README.md` = self-sufficient runbook; `items/ITEM-01..40.md`; `scoring-sheet.md`). The operator scores 40 historical syntheses blind (5 yes/no criteria from `SYNTHESIS_QUALITY_RUBRIC.md`), un-blinds with the sealed key, and tallies per-author pass-rates (gemini vs openai). **The flow:** operator blind scoring → a **Beat-1 mini-session** → the **#24 single-recommendation report** (Branch A swap / Branch B keep-gemini) + the operator's **ruling**. **That ruling IS the G3 event = Epic B** — it un-gates **#18 / #19 / #9** (plus D12/D13 and the v2 crux-resolver ranking, ADR-13). **This build chat does NOT do G3** — it is the operator's decision authority (ruling r3 / OQ-3); the LLM-judge second opinion is a *secondary* signal, segregated, never the verdict. G3 is **pause-independent** and can run before/during/after the P4 wave.

**(b) Hub-feedback file to carry hub-side — the Codex producer-lane conflict (NEEDS-RULING).** ai-council `docs/intake/2026-07-17-hub-feedback-codex-producer-lane.md` is a consumer→hub NEEDS-RULING note (EPIC-H). **The conflict:** a day-session plan tasked **Codex as PRODUCER** (#30 DOC-3), but two machine-level facts block it: (1) `~/.codex/AGENTS.md` is a *global read-only reviewer* policy — `codex exec` refuses to write even with `-s danger-full-access`; (2) the Windows write-sandbox can't apply patches (`workspace-write` refused). So Codex-as-producer is **unrealizable on this machine without editing hub-owned global infra — which a consumer must not do (core-invariant #6).** **The ruling the hub owes:** reconcile the Codex-producer doctrine with the global read-only `AGENTS.md` policy — either (a) formally adopt "Codex is review-only; CC/other agents produce" (retire Codex-as-producer from build plans), or (b) define a sanctioned producer-lane exception a consumer can invoke without editing global infra (and if (b), fix the Windows sandbox). **This is a HUB session's work**, not this ai-council build chat's — but the browser should know the ruling is pending so it does not re-plan Codex-as-producer for the P4 wave.

**(c) Interim Codex-producer fallback rule — IN FORCE NOW (operator ruling 2026-07-17).** Until the hub reconciles (b): **bounded build tasks run as CC-implements-Codex's-design + terra read-only review** (`codex exec review`) pre-merge. Codex/terra stays in its configured reviewer role. This shipped #30 cleanly (terra review: no Critical/High) and is recorded as a machine-level gotcha (`~/.claude/skills/gotchas/gotchas.md`). **Apply this to the whole P4 wave:** CC produces the code; Codex/terra reviews read-only; never plan Codex to write.

---

## §4 — Next-frontier (the design "why" that travels)

**Primary — drive P4 build wave 1 in order (#25 → #16 → #26), against the plan-of-record, honoring the sidecar seam rule + the pre-work map (§1/§2).** The whole-system view the architect must hold: the seam contracts are fixed (design against, never redesign); `output.py` is serialized (highest contention); the sidecar's first-lander defines the extension; the verdict package consumes by reference. The specific starting lane + launch config (model / effort / autonomy) rides the filled supplement (Q6 + addendum A: #25→#16→#26 is the recommended default, not dogma; #23 qualifies as an early disjoint parallel lane, #22 must wait for A2) — the narrowed §13(d) beat only re-checks whether anything changed since.

**Carry-open (do NOT redo / re-decide in this build chat):**
- **G3 (#24)** is the **operator's** blind-scoring mission (§3a) — its ruling is the Epic B event that un-gates #18/#19/#9. This chat builds P4; it does not score or rule.
- **The Codex producer-lane ruling (§3b)** is a **hub** session's — do not re-plan Codex-as-producer here; use the interim fallback (§3c).
- **P5 is evidence-gated:** CLI-4 parity (n=12, `#27`, depends-on #16) → default-flip; #18/#19/#9 only after G3. **P5 does not start in this wave** — #16 must land first to produce the parity evidence.
- **P6 is a completion backstop, not a start gate:** the `--file` gap "falls out of" A2's `cli.py:main` decomposition, so #22/#23 (CONTRACT §7 known-deviations) MAY close early during P4 — but the P6 row only verifies the window is complete (CONTRACT §7 emptied). Any **methodology / hub** question → the hub `.dev-knowledge`.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the ai-council **`BACKLOG.md`** (story-map, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P2) + the frozen **`docs/intake/2026-07-16-plan-of-record.md`** phase→task map (P4 = #25/#16/#26; P4 quote re-derived live, `PROBES.md` P4), the live in-progress branches (`git branch -v` — P1 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **The anti-bluff PROBES manifest (`PROBES.md`, P1–P4) is the load-bearing carrier: every claim above that could drift has a probe.**

---

=== PROBES.md ===

# Probe manifest — ai-council P4 build wave: anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE ai-council checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, phase-table text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub; its probes bind to **ai-council** — run them in the ai-council checkout. The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the ai-council checkout) | the summary holds a generation-time state; the P4 build wave will commit and move HEAD off the derivation-time pause-lift merge — a baked sha goes stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK` with zero warnings? | ai-council `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map counts drift on any BACKLOG edit (a build wave closes/edits tasks); neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`, and is `core.hooksPath` unset? (SessionStart `pre-commit install` arms all three.) | the ai-council checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` |
| P4 | Quote, **substring-exact**, the **P4 row(s)** of the phase → task map in the plan-of-record — the build-wave order (doctor / CLI seats / verdict package → their task ids) — confirming the build order is read from the frozen primary source, not paraphrased from this bundle. | ai-council `docs/intake/2026-07-16-plan-of-record.md` §4 "Phase → task map" table | the frozen phase-table rows are byte-fixed in the plan-of-record; a summary paraphrases the ordering and cannot reproduce the exact `P4 \| … \| **#nn**` row text; the bundle states none of it | `grep -n "P4" docs/intake/2026-07-16-plan-of-record.md` → the browser's quote must be a substring of a live `\| P4 \|` row |

## Gate procedure (CC)

1. **P4 first** — the forced phase-table read orients the session: it anchors the build-wave order (doctor → CLI seats → verdict package, mapped to #25/#16/#26) in the frozen primary source before design begins. **Then run the §13(d) operator-context beat NARROWED** (the supplement is FILLED — it already carries the off-repo context, so ask only *"anything changed since it was written?"*). Then P1–P3, each against **live ai-council state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move (the build wave commits) — re-derive it live, do not trust the residual's prose.

---

=== SUPPLEMENT.md ===

ANSWERS — outgoing architect (2026-07-17)

1. STRATEGIC INTENT: Shift the way-of-working from generative planning to build-governance.
   CC produces plan-mode proposals per task; the browser-architect reviews each against the
   frozen plan-of-record (docs/intake/2026-07-16-plan-of-record.md) + seam rules; closure is
   the empirical done-contract (real runs witnessed), never tests-pass. The arc's product
   north star: the delegation window — an external repo invokes the council via CLI/contract
   (ADR-11) and gets a transcript-free verdict package back.

2. TENSIONS WEIGHED: (i) build speed vs record discipline -> record first: G2 consolidation
   preceded any build. (ii) evidence purity vs operator time -> EPI-1 prep decoupled from
   operator scoring; G2 reordered ahead of G3 so a human-time dependency never blocks a
   mechanical unblock. (iii) Codex-producer doctrine vs hub-owned global read-only policy ->
   interim fallback (CC-implements-Codex's-design + terra read-only review); reconciliation
   is the hub's. (iv) workspace taxonomy -> output/ is RESERVED for run artifacts (it is
   also the EPI-1 evidence corpus); homes derive from quoted governance, never inference.
   (v) parallel throughput vs unattended risk -> night work ran serial legs with hard stop
   conditions; the stop fired and was correct.

3. CONSIDERED + REJECTED (do not relitigate): overnight P4 build (seam sequencing requires
   architect plan-review); filing a task for P0 (ADR-65 — done-at-merge tasks don't enter);
   stretching E6 to carry governance (charter dilution -> new E7); retaining both #1/#24
   evidence methods (split truth -> #1 absorbed, ruling recorded); editing ~/.codex/AGENTS.md
   from a consumer session (global infra is hub-owned); resurrecting functional-requirements-
   master (superseded by the intake by design).

4. OPEN QUESTIONS / DEFERRED: G3 — operator blind scoring of the 40-item pack, then the
   Beat-1 mini-session (#24 report + ruling = the Epic-B event). The METHOD is settled and
   sealed — only execution is pending; do not redesign it. Seal disposition at finalization
   already ruled: key + judge second-opinion get committed once un-blinding is recorded.
   Hub-side (separate hub session, not this chat): Codex dual-role mechanism (feedback file
   docs/intake/2026-07-17-hub-feedback-codex-producer-lane.md), EPIC-H doc reconciliation.
   DRAFT-GOV-2 deliberately unratified. #20/#21 remain known pre-existing.

5. DECOMPOSITION RATIONALE: gates-before-phases, because the two real blockers were
   decision-shaped (rulings, evidence ruling), not work-shaped. The phase->task map in the
   plan-of-record is 1:1 — navigate by it, do not re-derive. The task-graph shape is
   CONTENTION-driven as much as dependency-driven: cli.py (A2 decompose + doctor + #22) and
   output.py (A4 + B3 + seats[] + verdict package) are the two serialization points. Do NOT
   redo: the RULED register (15 + fork + scope header), ADR-14, the E7 addition, the
   pre-work mapping, the sidecar seam rule.

6. OFF-REPO CONTEXT: Operator's priority = the delegation window (other repos commissioning
   council debates by CLI command) with CLI-subscription token savings as the economic
   driver (ADR-12; parity #27 is the flip evidence). Operator scoring time is the scarce
   resource — keep it off the critical path. Standing sanctions in force: Codex YOLO
   (danger-full-access on this Windows box, operator owns the risk, sandbox-scoped only);
   zero-invented-paths (every path from quoted governance or delegated derivation);
   night/major session reports persist as audits-class artifacts.

A. BUILD-WAVE ORDERING: #25 -> #16 -> #26 is the recommended default (A2 unblocks the
   cli.py surface; doctor's liveness feeds the seats; the first-landing lane defines the
   sidecar extension mechanism), but it is NOT dogma — the operator may open a parallel
   lane where files are disjoint. Specifically, given the operator's window priority:
   #23 (research --return-dir; research/runner.py) qualifies as an early parallel lane;
   #22 (--file frontmatter; cli.py) must WAIT for A2 to land — same-file contention.
   #26 stays last of the wave (output.py contention + consumes seats[] by reference).

B. CODEX PRODUCER-LANE: Confirmed — the interim fallback (CC implements Codex's design +
   terra read-only review) governs the ENTIRE P4 wave. Hub reconciliation (EPIC-H) is a
   separate hub session. The YOLO sanction covers the sandbox only; the global role policy
   stays hub-owned and untouched.
