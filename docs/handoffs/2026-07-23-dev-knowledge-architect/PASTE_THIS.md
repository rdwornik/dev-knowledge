=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-23-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-07-23-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Planning session: resume and rule the open frontier — the `[#381]` polyrepo ruling (the E9 brake), the ADR-92 amendment call, the `[#403]` derivations choice, and the small `[#402]`/`[#401]` calls; residual §4 carries the priority frame. Decompose what rules into executable lanes. Task-graph: `BACKLOG.md` (the spec — whole-theme view per §13 architect posture).<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-07-23-dev-knowledge-architect — the part the repo does not already encode

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
**Standing (deliberate, not new):** the `VISION.md` `canonical_freshness` backstop WARN — left visible as honest, tracked by `[#368]` (VISION untouched pending its own re-review arc; deliberately NOT dispositioned). `witnessed` at generation; re-derive via P7. **Dispositioned:** `ecosystem/disposition-register.yaml` carries the two historical no-ff spine entries (`warn-no-ff-*-journal-wrap`, `warn-no-ff-*-transcript-archive`) — pre-existing main-spine hits, ruled benign with refs in the register. **New-this-window:** none known at generation (`validate_git_backlog` and `validate_backlog` were clean when this bundle was cut — `witnessed`); the live set at read-time is P4/P7/P9's answer, not this paragraph. **Known-latent:** `gen_handoff.py` leaks architect-mode SUPPLEMENT framing into *execution*-mode renders (`[#404]`, filed this window) — this architect bundle is unaffected (architect is the generator's home path); any execution/developer render before `[#404]` lands needs hand-correction.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-21 architect handoff (detail: `JOURNAL.md` 2026-07-21→23 entries; ids: `BACKLOG.md`).

- `[E9]` North Star ingested (intake #16; `[#381]`–`[#388]`) — **the brake is live: no new fleet machinery before `[#381]` rules**
- `[#386]` delivery loop codified into PLAYBOOK §21 (+ `[#389]`/`[#390]` filed)
- `[#384]` CLOSED — L5a fleet analytics reporter (`fleet_analytics.py`, read-only)
- Night batch: `docs/decisions/transcripts/` DELETED (operator ruling; ADR-77 guard kept armed) + archival audit; `[#400]` filed; integration filings `[#391]`–`[#396]`
- Hygiene lane: logs/ naming convention `[#395]` + ARCHITECTURE currency `[#321]`; filings `[#397]`–`[#399]`
- `docs/runbooks/` collapsed into `protocols/` + ADR-101 d.i reversal amendment
- ADR-43 routed-mirror clause RETIRED by amendment (re-scope); `[#401]` filed (ai-council routing armed at deleted hub zone)
- `[#398]` CLOSED — intake status-enum deployed, id:14 triple dissolved; `[#402]` filed (naming clause)
- ARCHITECTURE currency lane: carrier 4→5 (5 sites), Ch4 channel/carrier vocabulary split, child roster +win-tooling, Governing-ADRs refresh; `[#403]` filed (doc_claims coverage gap); ADR-92 stale-side finding REPORTED, not edited
- `[#404]` filed — gen_handoff execution-mode SUPPLEMENT leak, found cutting (and hand-correcting) the now-superseded same-day execution bundle; this architect bundle supersedes it
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The open rulings/design questions this planning session should resume, in rough priority order (`recall` — re-check each against live `BACKLOG.md` at boot):

1. **`[#381]` polyrepo ruling** — the E9 brake gates ALL new fleet machinery; nothing in `[#382]`/`[#383]`/`[#385]` may start before it rules. THE standing architect decision.
2. **ADR-92 amendment call** — reality is five carrier modules; ADR-92's body still says "four hard-coded carriers". The divergence is annotated legible in `ARCHITECTURE.md` (Governing-ADRs row); the amendment itself is owed.
3. **`[#403]` derivations ruling** — which machine-derivable doc_claims checks to adopt (carrier count / child roster / Governing-ADR completeness); candidates named in the ticket, none chosen.
4. **`[#402]` naming-clause ruling** + **`[#401]` ai-council routing disarm** — both small, both blocked on an operator call.
5. **Conformance remotes + nightly-triage findings** — 2 remote conformance branches left for triage (2026-07-23 consolidation JOURNAL entry).
6. **`[#404]` generator mode-blindness** — execution/developer renders leak architect SUPPLEMENT framing + a dead P8 binding; fix = mode-aware framing tokens, mode-conditional P8 row, per-mode render test. Small, self-contained; a candidate first execution task once rulings land.
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
> **Branch note.** This bundle was generated on branch `docs/handoff-architect`. This line names only *which*
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
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-07-23-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-07-23-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-07-23-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

1. STRATEGIC INTENT — the way-of-working goal for the next session

Convert fleet governance from prose-plus-checks to ONE declarative data contract with
mechanisms DERIVED from it — the Terraform MODEL (declare → plan/diff → apply → state
→ reconcile), never the Terraform tool. The operator's vision, restated at handoff:
manage the process (intake→ADR→backlog→execution→archive), the naming, the files, the
dependencies (doc2doc/doc2file, hooks, skills), the methodology deployment and
versioning, with Python libraries (pydantic schema + networkx graph + pandas
divergence report) — never hand-rolled, never hole-patched. This arc PROVED the
delivery loop and codified it (PLAYBOOK §21); the next session does not re-prove it —
it uses it, starting with the one gate: the [#381] polyrepo shape ruling, in its own
fresh chat, before any machinery is built (standing brake, JOURNAL:76).

Newly dictated at handoff, mostly UNFILED — the next session files these as
intake/backlog rows, does not silently absorb them:
(a) UNIVERSAL PYTHON STYLE: one fleet-wide way of producing code — functional-vs-OOP
    stance ruled once, uniform naming for classes/files/objects/variables, a universal
    Python-delivery methodology that is improvable BECAUSE it is universal. The 07-19
    ruff/pytest parity covers tooling only; the paradigm/naming half is unfiled.
(b) AUTO-COUPLED DOC UPDATES: closing a backlog item must PULL the ARCHITECTURE update
    and JOURNAL entry mechanically — wired, not remembered. Evidence this is needed:
    ARCHITECTURE drift was found TWICE this arc, once the day after a genuine re-read
    ([#403] is the mechanism seed — doc_claims extension to machine-derivable claims).
(c) THREE STANDING NIGHT BATCHES: code review · architecture review · creative
    session — produced at night, consumed by day sessions. The pattern ran twice this
    arc (night audit, night integration batch) and worked, including an armed stop
    that correctly held a bad merge; it needs formalizing as routine.
(d) SUBAGENT/WORKFLOW ROUTING: the operator sees systematic underuse of Sonnet
    fan-out, mini-agents, workflows, and wants ONLINE RESEARCH into Anthropic's own
    published commands/skills (code-review, hooks/skills review, etc.) and their
    adoption across the fleet.
(e) COLORS, SEMANTICS CLARIFIED: opening ANY governed markdown must visually show
    what is the global, hub-managed, repeatable part vs the per-repo personalized
    part. Deployed to ai-council as a DECLARED interim (review 2026-10-22); the real
    blocker is the ownership model itself — see open questions.

2. TENSIONS WEIGHED — where we landed and why

- Buy-vs-build → adopt the MODEL, not the tool (three times: Copier→regenerate,
  Terraform→reconcile loop, Splunk→the data frame). The fleet's substrate (markdown-
  heavy, local-disk, divergence-not-merge-replay) kept failing the tools' assumptions
  while their architecture held.
- System-first vs deliver-now → system-first stands, with ONE declared interim: the
  colors deploy (annotated, review-dated, replaced by the carrier when it lands).
  Declared deviations beat silent ones and beat waiting.
- Archival visibility vs strictness → ACCEPTED is a LIVE status (stays in the working
  folder) with a mandatory `disposition: active|deferred(+trigger)` companion — the
  operator must SEE parked-but-alive vs closed; terminal = CONSUMED|SUPERSEDED|
  REJECTED only.
- Enum reality vs aspiration → enums describe what exists on disk (Withdrawn dropped
  at zero uses ever; Proposed/Deprecated recognized). Aspirational categories with no
  queue get deleted, not kept (same ruling shape as the runbooks genre collapse).
- Immutability vs currency → append-only amendment markers on ADRs, live docs
  repointed, historical records left as accurate history (docs/smoke precedent) —
  never rewrite, never stamp around; freshness-gated files get a GENUINE re-read
  before any stamp.
- Meta vs object work → every session's success metric is a consumer-visible,
  operator-witnessed change; merged ≠ done, witnessed = done.

3. CONSIDERED + REJECTED — do not relitigate

Template engines (Copier/cruft: merge-replay fails our divergence profile; hub is
already regenerate-shaped; kept only the per-consumer version-pin scalar) · Renovate ·
SIEM event-stream framing (fleet is nightly cooperative state-diff) · PyDriller
(measured: ~60x slower than git log --numstat; its cyclomatic value-add returns None
on a ~70%-markdown fleet; stdlib+pandas is MORE faithful to the CodeScene model the
spec cites) · CSV analytics output before L5b consumes it · a third status enum
(reconciled the two that existed) · wholesale ADR-43 retirement (re-scoped instead:
hub landing retired, ai-council repo-local production stands) · Withdrawn ADR status ·
one-member genres (runbooks collapsed; SANCTIONED_GENRES shrunk so recreation is
Rule-A-refused — mechanism, not prose) · closing tickets on unmerged branches ·
worktrees for sequential work (worktree = parallel mutation isolation, nothing else) ·
narrowing the ARC-5 rule-fix goal · the 10-20-repo figure (FABRICATED — live
requirements say 5-8+; price the polyrepo ADR at 5-8+).

4. OPEN QUESTIONS — unresolved or deliberately deferred

OPERATOR-OWNED (nobody else can discharge):
- [#381] the polyrepo shape ruling — THE gate. Inputs: intake #16 §4 + the 2026-07-21
  recon. Must price: unfold cost (~4,200 plural-only lines), the employer-data
  compliance boundary (work vs personal repos in one tree — ONE SENTENCE from the
  operator settles it), pre-sales blast radius. Standing recommendation: PARTIAL fold
  along the compliance boundary — fewer repos, not one repo.
- [#386] closes on his witness of merged PLAYBOOK §21.
- ADR-92 amendment (its body still says "four hard-coded carriers"; reality is five —
  the divergence is now LEGIBLE in ARCHITECTURE's Governing-ADR row, marked
  "amendment owed").
- [#403] derivation choice (carrier set / child roster / Governing-ADR completeness).
- docs/archive/ second review — 9 files, per-file proposals ready in the night-batch
  audit; the queue's own contract says default-to-delete, ~8 weeks overdue.
- ADR-77 guard over the deleted transcripts/ zone: stays armed (current) or retires
  (needs an ADR-77 amendment + lockstep hook/test/organ removal).
- Three unreviewed nightly conformance branches (claude/conformance-2026-07-21/22/23,
  0 High total; summarized in JOURNAL).

DESIGN QUESTIONS:
- The ownership model needs a third cell: commands/skills/hooks rosters are
  hub-mandated STRUCTURE with repo-specific CONTENT — neither owner=hub nor
  owner=repo is true ([#400], same gap as [#370] for ~/.claude). This blocks the
  colors semantics the operator actually wants.
- The status-coupled archival VALIDATOR (W3 seed 2; spec in the 2026-07-23
  enum-reconcile audit §4) — enums are now deployed, the mechanism is unbuilt.
- [#401] ai-council routing still armed at the deleted hub zone + a
  declared-unenforced re-creation gap (candidate organs named, none chosen).
- [#391] fleet_analytics nightly wiring · [#392] rename-alias history ·
  [#393]/[#394] rot review + coverage gap · [#397] scripts/ restructure (impact map
  attached, no moves) · [#399] v5 README.tmpl phantom source · [#402] intake naming
  clause (join-key hazard recorded) · [#389]+[#390] prompt-lint + the ADR-87↔PLAYBOOK
  effort-ownership contradiction · [#387] buy-vs-build intake rewrite · [#396]
  gitenv.py extraction · [#242]/[#362] ADR normalization pair · [#368] VISION
  freshness — deliberately honest, discharges ONLY at the #381 session's genuine
  re-read (carries a named checklist item for VISION:110-113).
- The newly dictated items 1(a)-(d) above — all need filing.

5. DECOMPOSITION RATIONALE — why this shape; what NOT to redo

The chain is #381 ruling → #382 desired-state ADR (pydantic/networkx/pandas; its
first deliverable is a CONFORMING technical intake derived from intake #16) → #383
execution waves (per-surface, worktrees singly, wave-done = the pandas report shows
zero undeclared divergence) → #385 L4 tech-currency. Decisions precede machinery —
that ordering IS the lesson of three months (fleet machinery grew under a shape
nobody argued; ~4,200 lines of it may dissolve on the ruling). The hygiene/enum/
doctrine lanes ran FIRST because desired-state migration needs trustworthy statuses
and truthful canon: both enums are now ruled AND deployed, archives exist and are
visible, ARCHITECTURE is current with its claim-drift corrected twice.

Do NOT: re-prove the delivery loop (canon, PLAYBOOK §21) · re-decide the enums or the
companion-field schema (deployed; migration done, zero OTHER bucket) · restructure
ecosystem/ or deploy/ before their gates (#382 replaces the registry sprawl; deploy/
is on the dissolves-on-fold list) · relitigate anything in Q3 · build the desired-
state system before #381 rules · generate handoffs without the operator's explicit
trigger · treat CC's "(Recommended)" as authority — every plan-mode pick is reasoned
per-question on the merits (two picker shapes; closed-set pickers take a note, not
free text).

6. OFF-REPO CONTEXT

- Operator state: long arc, tired at close, but the deadlock is broken — this arc
  SHIPPED (assets/ dissolved+witnessed; loop codified; L5a analytics live and [#384]
  closed through the gate; runbooks collapsed; transcripts/ deleted with ADR-43
  re-scoped; both enums deployed with [#398] closed; hygiene + ARCHITECTURE currency
  landed; colors deployed as declared interim). Do not cite assets/ as an achievement
  — it was only ever a symbol; the SYSTEM is the demand.
- The operator triggers handoffs. Never the architect, never auto.
- Standing communication contract: five architect fields (INTENT · MODE+basis ·
  EFFORT · GOVERNANCE POINTER · CLOSURE+ANTI-PATTERNS), CC self-loads the rest.
  MODE is the field chats keep forgetting — it is not optional. Wrap verification
  runs SHIP-GATE, never health (health is FAIL-only; the WARN class that blocks
  integration is invisible to it — cost us [#401]).
- Worktree algorithm (repeated operator pain, now fixed doctrine): dependency? →
  sequential. No dependency + disjoint files + both mutate the same repo → parallel
  REQUIRES one worktree per lane (index isolation is the only thing a worktree does).
  Different actors/repos/read-only → parallel with no worktree. Propose the priced
  choice unprompted at the moment the second lane is emitted; the operator picks.
- Blue Yonder boundary: corp-monorepo carries employer/pre-sales material; the
  polyrepo ADR must ask the operator the one-sentence compliance question before any
  fold crosses work/personal.
- The architect's recurring failure class this arc, for the next one to guard
  against: asserting unverified load-bearing facts (a fabricated repo count, a
  nonexistent ruling date, a gitignored "path class", an already-installed
  extension). CC caught each. Verify-or-mark-unverified; the discipline works in
  both directions — two of three suspected formatting defects in the final review
  were render artifacts, correctly flagged as verify-first and correctly left
  untouched.
