=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-23-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-23-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Clear the rulings queue, then shape the next build arc — the 2026-07-21 build mandate was executed, and what gates the next one is a stack of pending operator/architect rulings, not missing theory.** Boost shipped owner-C and is witnessed end-to-end; the P1 absorb is complete; ARCHITECTURE took a repair pass whose last finding is still un-ruled: the codemap's allowed edge set is a **map-derived understatement** against `cli.py`'s real imports (P11 re-derives the live gap), with the `cli -> boost` open case bound to the same future arc as `#69`/`#92`. Rule the allowed-set follow-up, shape the `[S18]`/`#97` checker build (14 rules specified, none built), land `#4`'s fenced ADR-02 amendment, and clear the record debt (the `#110`/`#128` renumber behind the P12 reservation fence, the `#99` triage, the `#73` review-runner convention). Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; the grooming log's 2026-07-23 entries are this window's ruling record — read them before re-deciding anything.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `worktree-ai-council-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS are folded into `PASTE_THIS.md`, so the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*. **The ANSWERS correct the residual on a load-bearing point** — read them before the residual's §4 ordering (ANSWER A splits §4 item 1; ANSWER B fixes the arc order).

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

# Residual — 2026-07-23-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED — its ANSWERS outrank this residual on intent and priority.** The
> §13(d) beat NARROWS. Load-bearing corrections to read before §4: **ANSWER A** splits §4 item 1 —
> the map-vs-source completeness gap belongs to `#97` rule-14 leg (b) and the factual allowed-set
> correction is **immediate and standalone** (the conditional grep it names has since RUN — the
> rule14-legs merge confirmed the edges, so the condition is met); only the `cli -> boost` open case
> rides the `#69`/`#92` arc. **ANSWER B** fixes the arc order (checker first; `#92`→resolver→`#69`→P2
> as ONE arc; `#27` is operator-only and must never be sequenced behind anything). The residual stays
> authoritative on *what the defects are*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks **the target actually has** — the four `ai-council`
validators (P7) + `validate_backlog` (P9) — plus hand intersection where the hub organ has no target
equivalent (P4, P11). **Re-derive each at read-time — the teeth are in `PROBES.md`
(P4/P6/P7/P9/P11), not in trusting these lines.** This bundle states **no** validator verdict,
count, drifted `#id`, or sha — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo re-frame:** `ai-council` carries **no automated drift-check organ** — no `audit.py`
ship-gate, no `validate_doc_claims`, no `validate_git_backlog`, no disposition register. The drift
surface is therefore: the four read-only validators (**P7**, several of which pass *silently* — the
exit code is the signal), `validate_backlog` (**P9**), and hand intersection (**P4**). The organ that
would mechanize doc-vs-reality checking is specified but not built (§4 item 2).

**STANDING + DELIBERATE (the headline):** `ARCHITECTURE.md`'s **Layer-edges allowed set is a
map-derived understatement** against `cli.py`'s real import surface — proven by the window's last
merge (rule-14 leg-b live validation; JOURNAL 2026-07-23 `chore/rule14-legs` entry), **report-only by
instruction**: no doc edit was applied, the follow-up edit awaits the operator's ruling. This is a
*known, held-open* drift, not an oversight — do not "fix" it before the ruling. **P11** re-derives
the live gap; §4 item 1 carries the decision context.

**STANDING (fenced, not yet resolved):** the dangling `refs #96` occurrences in the carried hub-id
tasks (`#110`/`#128`) — hazard contained by the BACKLOG **Id-reservations note** (ids reserved until
the renumber arc lands; **P12** re-derives the fence). And a cosmetic residue flagged in the JOURNAL:
the ARCHITECTURE Modules-table header still claims the `src/ai_council/` root while its config row
correctly points at repo-root `config/`.

**RESOLVED THIS WINDOW — do not re-flag:** the panel-default "3-vs-5 authority conflict" was
**DISSOLVED by archaeology** (code, ADR-02, ARCHITECTURE, GUIDE mutually consistent; the batch
report carries a dated withdrawal AMENDMENT — re-raising it is the false positive checker rule 5 now
guards against); the `#96` id collision was repaired by renumber; the moratorium lift is now recorded
in the grooming log; the E4 exit-3 claim was verified against source.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-21 handoff. One line each; detail lives in `JOURNAL.md` (all entries
2026-07-22/23) + the merge messages. All ids/paths are **ai-council's**.

- `3bf3ca9` — **`council boost` input stage shipped** (Unit 2 P1, TDD-first, owner-**C** per the
  ADR-11 amendment; terra-reviewed; chain witnessed end-to-end incl. one operator-authorized billed
  run). Closed `#37`; `#36` struck superseded-by-boost with remainder `#88`.
- `0611314` — the **boost→decide chain made explicit** in VISION / ARCHITECTURE / ADR-11 (the
  amendment last window's supplement demanded).
- `c35bc3e` — `.vscode/` boundary decoration landed (hub `#352` spec, declared-interim).
- `eb82fd5` — **night batch** (`chore/pre-handoff-cleanup`): dead-patch healthcheck test fix,
  ARCHITECTURE/VISION/CLAUDE/GUIDE doc-currency reconciliation, batch report
  `docs/audits/2026-07-22-pre-handoff-cleanup.md` (15 proposals + checker spec).
- `95b9e4f` — **session-close absorb**: the 8 live-unfiled P1s filed (`#89`–`#95`, `#98`; stories
  `[S17]`/`[S18]`), checker story `#97` filed, xdist declared + honestly re-measured
  (recommendation: do **not** adopt `-n auto` in `check.ps1`), panel-default conflict dissolved.
- `fe42bc2` — **record fixes**: `#96`→`#98` renumber + reservations-rule extension, `#69` P2
  constraint verified + attached, `#4` re-scoped (moratorium lift recorded), `#99` filed
  (batch-§2 pointer), `scripts/council-ask.ps1` deleted.
- `fc71328` — **ARCHITECTURE repair pass** (8 architect edits: layer-edge set completed +
  `cli -> boost` named the one open case, invariants 2/3 marked target-vs-state, boost in Data
  Flow, ADR-13 restored to the roster, stale pending-`#2` clause resolved).
- `6c297dd` — **`#97` rule 14 de-vacuated** (leg b: map completeness vs source), live-validated the
  same hour — the validation that produced §1's headline drift-flag.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
Ordered: rulings that gate build arcs first, then arc-shaping, then record debt.

1. **The ARCHITECTURE allowed-edge-set ruling (the headline's decision).** The completed Layer-edges
   set was audited **map-vs-map**; leg-b's map-vs-source check then showed `cli.py`'s real import
   surface far exceeds it (P11 supplies the live number). The un-ruled fork: **(a)** legalize cli's
   real edge profile as-is (interface→interface/orchestration/core/foundation/output — which
   falsifies "utility-exemption modules: none" and largely dissolves the layer discipline's bite at
   the interface layer), vs **(b)** hold the doc as **target**, and let `#92`'s `cli.run()` refactor
   shrink the real surface toward it before the set is re-derived. The JOURNAL's lean: the ruling
   rides the `#69`/P2 arc, because `#92` is what actually changes cli's import surface. Whatever is
   ruled, the doc must say *which* of current-state vs target it records (the repair pass already
   established that vocabulary for invariants 2/3).
2. **`cli -> boost` open case** — deliberately **not silently legalized** by the repair pass. Two
   candidate resolutions recorded in ARCHITECTURE: reclassify `boost` to orchestration, or admit a
   *scoped* interface→core edge. Bound to the same `#69`/P2 wiring arc; rule it together with item 1.
3. **The `#69` parity fix carries a verified P2 constraint** — the divergent frontmatter-`models:`
   gating expression **is also** the expression that makes `full_panel` the effective 5-model
   default. Any fix must **decouple the models-gate from the panel-default resolution** and land a
   bare-invocation panel-default regression test *first*, else the fix silently flips the default.
   The T8 strict xfail (`tests/test_boost.py`) errors the suite the moment boost wiring lands —
   wiring and parity fix are one arc by construction.
4. **`[S18]`/`#97` checker build** — 14 rules, each traced to a drift that actually occurred, both
   rule-14 legs now non-vacuous. Open design questions: build it as one script or per-rule
   validators; which rules gate vs report; and whether it becomes the target-side organ that closes
   the "no automated doc-claim check" gap (§1). The night-batch spec (`2026-07-22` report §3) is the
   authoritative rule list.
5. **`#4`'s ADR-02 amendment — scope is FENCED.** (a) overlap policy + (b) stale stamp only; the
   panel-default question is **DISSOLVED and out of scope** — the amendment must not reopen it
   (checker rule 5's refinement is the guard: adjudicate *effective flag-resolution behaviour*,
   never raw config keys).
6. **The renumber arc** — `#110`→`#84`, `#128`→`#85`, resolving/dropping their `refs #96` **in the
   same edit** (audit A1's instruction). P12 re-derives the reservation fence; until it lands, three
   ids stay un-assignable.
7. **`#99` triage** — the batch report §2 proposal set is *pointed at* but individually un-triaged
   (deliberate). A triage session decides file/drop per proposal; the un-filed xdist flake finding
   (first witnessed non-xdist-safe test) attaches to that thread.
8. **`#73` review-runner convention** — the review-lane routing posture (which reviewer lane runs
   what; one lane withdrawn on cost) lives only in `~/.claude` + the JOURNAL, not as a repo record —
   the fresh-architect gap the session-close entry names. A ruling here would also absorb it.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council`'s**
`BACKLOG.md` (themes `[E1]`–`[E7]`; the grooming log carries this window's rulings), the live
in-progress branches (`git branch -v`, run in the **target**), and the drifted-closed intersection
**P4 computes by hand** (§1 — the target has no `validate_git_backlog`). Re-narrating item text
splits the truth and drifts — the pointer + the drift-flag is the whole task-state. The whole-open-set
grooming obligation at boot is **P10**.

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
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an answer hint.
>
> **Branch note.** This bundle was generated on branch `worktree-ai-council-handoff` **in the hub**.
> That names only which hub branch hosted generation — **re-derive the TARGET's HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P13** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | ai-council |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below confirmed present at generation time by running its command in the target). Where the hub
has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.
(The gap itself is now a tracked target-repo concern: the claim-vs-reality checker story — see the
residual §4 — is the organ that would close it.)

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS are folded into `PASTE_THIS.md`, so the incoming §13(d)
> operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*
> **Read the ANSWERS before the residual's §4 ordering — they correct it on load-bearing points**
> (ANSWER A splits §4 item 1: the map-vs-source gap belongs to `#97` leg (b), standalone; only the
> `cli -> boost` open case rides the `#69`/`#92` arc. ANSWER B fixes the arc order). The supplement
> wins on intent and priority; the residual stays authoritative on *what the defects are*.

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
by CC, substring-matched. Both files were **amended this window** (the boost→decide chain landed in
VISION per the owner-C ruling; ARCHITECTURE took an eight-edit repair pass) — so the live lines, not
any remembered ones, are the frame. **Then, before design, the operator-context beat fires (§13d) —
NARROWED** (the supplement is FILLED — ask only *"anything changed since it was written?"*).
**P11 is unusually load-bearing this window:** ANSWER A rules that if the commissioned edge grep
came back positive the allowed set is *factually wrong today* and the correction is immediate and
standalone — the grep has since run (post-answers), so P11's live re-derivation is the number that
correction starts from.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run-in root noted) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS`, and no `validate_doc_claims` either; this row restores that missing doc-vs-reality tooth by hand.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and does `ARCHITECTURE.md`'s **hook roster** list that **same set** — or has the doc drifted behind the config? | `ARCHITECTURE.md` (hook-roster prose) ∩ the pre-commit config | the roster drifts every time a gate lands, and `ai-council` has **no automated doc-claim check** to catch the doc falling behind — so a mismatch stays invisible until someone reads both. The roster was reconciled to the live id set mid-window by the night batch; whether it **stayed** reconciled is a live question | **TARGET:** `grep -n 'hook' ARCHITECTURE.md` for the doc side; for the config side run grep -c and grep-tail for the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the two sets by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — and ARCHITECTURE took **two merges of edits** at the very end of this window, so the relation is the freshest fact in the repo | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **read-only** repo validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Note several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; the count, the tail slug, and whether the index has kept pace are all live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings** — and what does `BACKLOG.md`'s grooming log name as the **next free local id** (with which ids **reserved**)? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window moved every one of them (two stories and a double-digit task delta landed); the next-free pointer moved twice; none of it is in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) then `grep -n 'Next free local id' BACKLOG.md \| tail -1` |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **This window's grooming log records several operator rulings mid-flight** (a re-scope, a renumber, a moratorium lift) — the judgment must be made against the post-ruling text, not any remembered pre-ruling one | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[NEW this window — the map-vs-source edge gap, the number the next ruling is about.]** How many **real** `src/ai_council/` inter-module imports does `cli.py` carry **right now** (module-level and function-level; the TYPE_CHECKING-only import excluded), and how many of those edges does `ARCHITECTURE.md`'s **Layer edges** allowed set actually list? Report the **gap as a number**. | `src/ai_council/cli.py` ∩ `ARCHITECTURE.md` "Layer edges" | **this is the evidence base for the pending allowed-set ruling** (residual §4 item 1): the window's last merge proved the codemap understates cli's real import surface, report-only — no doc edit was applied, so the gap is still live. It exists only by intersecting source with doc at answer-time; the checker rule that would mechanize it (rule-14 leg b) is specified but **not built** | **TARGET:** `grep -n 'from ai_council' src/ai_council/cli.py` for the source side; `sed -n '/^Layer edges/,+25p' ARCHITECTURE.md` for the doc side — compare the two sets by hand, note which listed edge is marked the **open case** |
| P12 | **[NEW this window — the reservation fence the renumber arc depends on.]** Which ids does `BACKLOG.md`'s **Id-reservations note** hold reserved **right now**, how many `refs #96` occurrences does the file still carry, and are the two carried hub-id tasks still sitting at their hub ids? | `BACKLOG.md` (Id-reservations note + task lines) | the reservation set and the dangling-ref count are the **preconditions of the pending renumber arc** (residual §4 item 6) — if either has moved, the arc's plan is stale; both are live text facts a summary rounds off, and the reservation rule itself ("grep before assigning any id") was extended mid-window | **TARGET:** `grep -n 'Id reservations' BACKLOG.md` (read the note in full) then `grep -c 'refs #96' BACKLOG.md` then `grep -n '\[#110\]\|\[#128\]' BACKLOG.md` |
| P13 | Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors the evidence base the still-open extractor design forks depend on (the fenced-block and continuation-line rulings — residual §4); a branch push does **not** carry tags, so local-remote divergence is a live possibility only git can answer, and last window's bundle flagged exactly this exposure — whether it was since resolved is answerable only live | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config file is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked dotfile name is looked up without its dot, which resolves nowhere — the
> probe is then FAILed as a missing target even though the file plainly exists.
> **Consequence: no probe in any bundle — hub or cross-repo — can currently bind to a dotfile.** That is
> a hub tooling defect worth filing (dotfiles are exactly where config gates live); it is deliberately
> **not** patched from inside this handoff, because hub infra changes are exception-with-ruling
> (core-invariant #6). The probe's teeth are unaffected — the comparison is still live-only and
> answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `scripts/validate_backlog.py` all exist in
   both). This is the single most likely failure mode of a cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d) — NARROWED** (the supplement is
   FILLED — ask only *"anything changed since it was written?"*). Then run P2–P13, each
   against **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P13 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." **P7 is the headline substitute** (four exit codes, read
   explicitly — several gates pass silently, so "no output" must not be scored as "no drift").
   **P2 is the hand-built doc-vs-reality tooth** this repo otherwise lacks. **P10 grooms the whole
   open BACKLOG at boot** (live / dead / awaiting-ruling per open `#id`) — the operator-ruled boot
   obligation, not optional. **P11 and P12 are this window's additions**, and their order is
   deliberate: **P11 before the allowed-set ruling** (it supplies the number that ruling is about),
   **P12 before any renumber or filing work** (it re-derives the reservation fence). **P13 re-checks
   last window's irreversible-loss flag** — one command, cheap, and the only way to know whether the
   exposure was closed.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **FILLED**, so its ANSWERS are folded into
   `PASTE_THIS.md` and the §13(d) beat **NARROWS**. Confirm by looking at the bundle directory in
   the hub — it is CC-side bookkeeping, not target state.

---

=== SUPPLEMENT.md ===

SUPPLEMENT ANSWERS — outgoing ai-council architect (2026-07-22/23); CC transcribes VERBATIM

===============================================================================
0. THE VISION, RESTATED BY THE OPERATOR — READ THIS FIRST
===============================================================================

The operator restated the target this session, and it is sharper than VISION.md
currently carries. In his framing:

  A foreign repo under Dev/ says "I want to learn about this" or "make a
  research" or "make a decision". It sends the raw question through a simple
  interface. The Council takes it through the protocol, BOOSTS it, runs it,
  and returns the answer TOGETHER WITH THE PATH TO WHERE THE ANSWER LIVES.
  Effectively a very basic API — a simple interface for inter-repo
  communication via Claude. Later this may be packaged as skills, hooks, or
  similar; that packaging layer is unnamed and unbuilt.

Three standing themes, in his priority frame, unchanged across five windows:
  T1  minimize cognitive bias / raise debate value
  T2  CLI seats over API (cost)
  T3  the delegation window — the protocol/interface above

HOW FAR ARE WE. Honest split, because the two halves are at very different
maturity:

  THE ENGINE — roughly there.
    boost (input stage)                SHIPPED 2026-07-22, standalone
    debate + blind vote + synthesis    shipped
    verdict package (decision path)    shipped, Contract-Version 1.0
    path-to-the-answer                 --return-dir + R4 fail-loud, shipped

  THE INTERFACE — about a quarter built.
    ONE invocation                     NO. It is two: the caller must run
                                       `council boost`, then `council --file`
                                       itself. This is P2/#69 and it is the
                                       single largest gap between what exists
                                       and what the operator described.
    research-path verdict package      NO (#34). His use case explicitly
                                       includes "make a research" — that path
                                       returns a report and no machine-readable
                                       deliverable. A hole directly inside the
                                       stated vision, not a side item.
    caller-facing invocation docs      NO (#88 boost side, #38 verdict→ADR
                                       read-back side). A foreign repo has no
                                       documented way to learn that boost exists
                                       or what to do with a verdict.
    schema for either contract end     NO, and not filed. See OPEN QUESTIONS.
    skills / hooks packaging           NO, not filed, not designed.

  The next session should treat "one invocation, both modes, documented" as the
  T3 finish line — not "boost exists".

===============================================================================
1. STRATEGIC INTENT (way-of-working level)
===============================================================================

The failure this repo keeps paying for has moved again. Two windows ago it was
"decision recorded ≠ enforced" in code. Last window's audit proved it systemic
across every artifact layer. THIS window proved the layer underneath both:

  A DECISION THAT LIVES ONLY IN PROSE IS INVISIBLE TO EVERY GATE, BECAUSE THE
  GATES VALIDATE THE REPO AND THE DECISION IS NOT IN IT.

Three independent instances, one session, each found by review and none by any
gate:
  - the #84/#85 id reservation existed only in handoff prose → two new tickets
    took the reserved ids;
  - the dangling hub `refs #96` existed only in a carried-forward drift list →
    assigning #96 locally made those refs silently resolve to an unrelated
    ticket, which is worse than dangling because dangling is visible;
  - the 2026-07-21 moratorium LIFT was never recorded → CC conservatively
    respected a constraint that had not existed for two days.

All three are now repo records with mechanisms behind them (the reservations
note, the grep-before-assign rule, the grooming-log entry).

THE NEXT SESSION'S WAY-OF-WORKING GOAL: build [S18]/#97, the claim-vs-reality
checker, and treat its fourteen rules as the definition of done — not as a
wish list. The spec is complete and every rule carries an earned-by trace to a
real drift found this window. This is the mechanism that ends the class. It is
the highest-leverage item in the repo that is not operator-blocked.

The operator's standing demand is unchanged and was reaffirmed twice this
window: the theory is done. Execute it. "Produced another document" remains a
failure signal.

===============================================================================
2. TENSIONS WEIGHED
===============================================================================

(a) BOOST OWNER — caller-side advisor (A) vs council-side entry stage (C).
LANDED: C. Reasoning that decided it, in the operator's own frame: methodology
must live in ONE place. Owner-A distributes template knowledge across N foreign
callers, so every template change becomes N repo updates — the exact "where does
each concern live" disease he named as the top project framing. The foreign repo
"only accepts the question"; it must know nothing.

(b) DOES C REOPEN ADR-11? The incoming supplement said yes; the input-layer
audit said only the clarify-loop does. A LIVE READ SETTLED IT AND THE AUDIT WAS
RIGHT: the object ADR-11 rejected is STATEFULNESS (a Python library API, an
MCP/server surface). `council boost` is file-in/file-out, stateless, one
invocation, exit-code-carrying — a CLI-surface EXTENSION, therefore a
CLARIFICATION of decision 5, not a reversal. What WOULD reopen it is
interactivity, and that fails on two independent grounds: it is named in
"Considered and rejected", and it collides with decision 1's explicit
no-interactive-concepts cut. Deferred as a separable rider.

(c) HOW MUCH SHOULD THE BOOST BOOST? This is the tension worth carrying, because
the name oversells the behaviour. CC's build decided — correctly, and beyond
what the contract specified — that reformulation is DETERMINISTIC SCAFFOLDING
ONLY: the brief body is caller text plus fixed template constants; the LLM
contributes only the classification label and the hybrid split points, and those
split points must be a contiguous span of the caller's own text or the legs fall
back to full text and the run exits 3. The confabulation guard (T5) is therefore
satisfied BY CONSTRUCTION, not by test. Consequence, witnessed in the live demo:
a weak question gets structure and a `[BOOST-GAP]` flag, NOT enumerated options
— the panel had to enumerate the options itself. That honours the ADR-95
boundary and it means boost-emitted briefs are not fully GUIDE-conformant in the
`### Questions` sense. Whether that is the end state or a first step is an open
question below.

(d) STRETCH: BUILD THE CHECKER, OR SPEC IT? The session plan had the checker as
STRETCH after the boost layer. It was NOT built. Instead the night batch became
a manual run of it, and produced a fourteen-rule specification where every rule
is traced to a drift it actually found. JUDGEMENT: this is the better outcome
and was worth the substitution. A checker built from imagination would have had
different rules; this one is evidence-backed, including rule 12 (every finding
must carry a re-runnable evidence command), which exists because the scanners
produced four false positives in one night.

(e) PARALLELISM. The operator asked for worktrees. Recon killed it on a
mechanism, not a preference: ai-council has no `.worktreeinclude`, and — this is
the part that matters — the seed mechanism CANNOT fix the real blocker anyway.
The blocker is editable-install aliasing: the shared `.venv` finder hardcodes the
primary's absolute `src/`, so pytest inside a worktree imports the PRIMARY's code.
In an all-TDD session that is silent falsification of test results, not an
inconvenience. The two working fixes are outside the seed entirely:
`PYTHONPATH=<worktree>/src` per session, or a per-worktree venv. TRAP, recorded
because it is destructive: running `pip install -e .` from a worktree into the
shared venv REWRITES the finder to point at the worktree and silently breaks the
primary checkout.

(f) xdist. The batch reported 3.9× and recommended adopting `-n auto`. CHALLENGED
AND OVERTURNED: the baseline was measured while four codex scans ran, and the
xdist number under the same contention — the comparison was never made under
equal conditions. Clean re-measurement: serial 61.25s vs 43.13s = 1.42×. Then a
first witnessed non-xdist-safe test surfaced (`test_no_persist_removes_scratch_
on_abort` snapshots the SHARED system temp). LANDED: declare the dep (that is
dep-parity, checker rule 10, right regardless), do NOT adopt `-n auto` in
check.ps1. 18 seconds does not buy a flaky-failure surface.

===============================================================================
3. CONSIDERED + REJECTED — do not relitigate
===============================================================================

- Owner-A caller-side advisor. Rejected: distributes methodology across N repos.
- Interactive clarify-loop / MCP elicitation as the boost's gap handler.
  Rejected for P1: reopens ADR-11 and collides with its decision 1. Gaps are
  advisory annotations. Retained as a separable rider needing its own ADR.
- Routing R2 (hybrid as a third debate lane). Rejected on the input audit's own
  reasoning: the input layer must not drive the third-lane question (ADR-04/05/06
  conflict surface). Keep the class representable; R1 composition + R3 as
  validation of the classifier's guess.
- Wiring boost into `--file`/`--inbox` inside P1. Rejected deliberately: it would
  inherit the #69 parity blind spot onto a brand-new surface and make it instance
  five of the same pattern. P2 closes parity and wiring as one atomic unit.
- Adding a schema library (jsonschema/pydantic) for the brief. Rejected for P1:
  the repo has zero schema infrastructure, the artifact is markdown+frontmatter
  not JSON, and the established idiom is fail-loud bespoke checks. NOTE this is a
  P1 scoping call, NOT a ruling on the schema question — see OPEN QUESTIONS.
- Adopting `pytest-xdist -n auto` in check.ps1. Rejected on the clean numbers.
- `.worktreeinclude` as the parallelism fix. Rejected: structurally cannot
  address editable-install aliasing.
- sol for the boost design derivation. WITHDRAWN BY THE OPERATOR on token cost.
  Per the incoming ruling this was a SUBSTITUTION, not a skip — recorded, not
  silently dropped.
- Rewording invariant 2 to match the code. Rejected: it is retained as the TARGET
  with a status marker pointing at #92. Rewording an invariant to match a defect
  launders the defect.
- Silently adding `interface -> core` to the allowed layer-edge set to legalise
  `cli -> boost`. Rejected: that would be the architect rationalising his own
  output. Named as an OPEN CASE instead.

===============================================================================
4. OPEN QUESTIONS / DEFERRED (ranked by leverage)
===============================================================================

1. #27 PHASE-3 BLIND SCORING — 0/12, SIX CONSECUTIVE WINDOWS. Operator-only, one
   sitting, non-delegable. It gates the ADR-12 §5 CLI-default flip → #66, which
   means IT IS THE CHOKE POINT FOR TWO OF THE THREE THEMES: T2 cannot land
   without it, and T1's measurement story is downstream of the same evidence.
   Defect-driven ordering structurally cannot see an operator-blocked scoring
   task, so it falls out of every ranking by default. It has now done so five
   times. If it is not entering the next window, say so EXPLICITLY rather than
   letting it drop a seventh time.

2. HOW MUCH SHOULD THE BOOST BOOST? (from tension (c)). Today boost scaffolds,
   classifies, decomposes and flags — it does not restructure a rambling question
   into enumerated sub-questions with options. The ADR-95 boundary forbids
   INVENTING facts; it does not obviously forbid RESTRUCTURING what the caller
   supplied. There is a real design space between "scaffold only" and
   "confabulate", and P1 sits at the extreme safe end. Whether that is the end
   state is unruled. Bears directly on whether #38's read-back and the GUIDE's
   `### Questions` template are satisfiable by machine.

3. THE SCHEMA QUESTION — now load-bearing, and unfiled. ARCHITECTURE calls the
   verdict package "machine-authoritative" twice; there is no schema anywhere
   (hand-rolled json.dumps, an in-code "no parallel schema" note at
   output.py:1295, zero jsonschema/pydantic in the repo). Contract-Version exists
   as a NUMBER with nothing mechanically enforcing what it means. Both ends of
   the foreign-repo contract are now unschematised: the verdict package (output)
   and the boosted brief (input). For an interface other repos consume, that is
   the same disease as the rest of this window — the contract is prose, not a
   mechanism. Sits near #34/#76 (the 1.1 pair). NOT FILED — file it or rule it
   out deliberately.

4. #81 FABRICATION VS TOTAL LOSS — still owed, and it now has a precedent from
   INSIDE this repo. The fork assumes option extraction stays heuristic parsing
   of synthesizer prose. The boost answered the same class of problem
   structurally today: do not let the model produce free text you must then
   parse; constrain it to spans you can verify. That argues the real question is
   #77's boundary question — should the synthesizer emit structured options
   directly — rather than either arm of the #81 fork. KEEP-SCANNER is settled;
   the ruling is not.

5. `cli -> boost` LAYER EDGE — named as an OPEN CASE in ARCHITECTURE, unruled.
   Two candidates: (a) boost is misclassified and is really orchestration (its
   shape matches runner: provider selection + step coordination), which dissolves
   it with no code change; (b) `interface -> core` is legitimate for single-stage
   commands and should be added with that scope stated. See ANSWER A for the
   vehicle.

6. THE ALLOWED-EDGE-SET ASTERISK — my own work, flagged honestly. I derived
   ARCHITECTURE's "complete allowed set" FROM the codemap, which is
   hand-maintained, whose checker always reports a diff, and which is wired to no
   gate. So it is complete relative to the map, not to the source. Two edges I
   suspect exist in code and are absent from the map: `cli -> inbox`
   (interface→interface) and `cli -> config` (interface→foundation — which if
   real also falsifies the document's "Utility-exemption modules: none" line).
   A grep was commissioned; if either is real the set needs a correction edit.

7. #4 ADR-02 AMENDMENT — re-scoped and much smaller than feared, because the
   panel-default "conflict" dissolved. Remaining: the overlap-policy amendment
   and the stale stamp. Unblocked, cheap.

8. Carried unchanged: #19 F4-lift (undesigned) · #34 research-path verdict parity
   (now understood as a VISION hole, not a nice-to-have) · #99 triage of the batch
   proposal set · the #110→#84 / #128→#85 renumber (which also carries resolving
   the hub `refs #96` as the same edit) · the review-lane routing posture
   (luna/terra/sol) is not a repo record, adjacent to #73, and is hub-level not
   repo-level.

===============================================================================
5. DECOMPOSITION RATIONALE — and what NOT to redo
===============================================================================

WHY THIS SHAPE. The session ran rule → amend → contract → build → witness →
absorb → repair, serially, because worktree parallelism was mechanically blocked
(tension (e)) and because the boost pipeline is one schema-coupled chain
(classify → decompose → reformulate → emit) that cannot be split by file surface
without fabricating the exact cross-lane coupling defect that went RED on main
two windows ago.

DO NOT REDO:
- The owner ruling (C) or the ADR-11 clarification. Settled, amended, merged.
- The boost P1 build. Merged 3bf3ca9, 818 green, terra-passed, live-witnessed
  end-to-end including a decomposition case at $0.0507 actual.
- The panel-default archaeology. DISSOLVED — no defect exists; code, ADR-02,
  ARCHITECTURE and GUIDE are mutually consistent; `default_panel = 3` is the LITE
  set and `eff_full = (use_full_panel or not lite)` makes 5 the effective default.
  A withdrawal amendment is appended to the batch report. If a future scanner
  re-reports this, it is reading a config key without tracing its caller —
  checker rule 5 exists for exactly this.
- The 16-P1 accounting: 6 deliberately fixed (in-code `P1-n:` comments), 2
  pre-filed (#69, #75), 8 now filed (#89–#95, #98). Earlier "9 unfiled" figures
  were weaker evidence; this one was verified per-item against source.
- The xdist measurement. Clean, uncontended, decided.
- The night batch's four autonomous fixes and the ARCHITECTURE repair pass.

WHAT MUST BE DONE FRESH — see ANSWER B for ordering.

THE ARC SHAPE THAT MATTERS MOST, because it is not obvious from the tickets:
#92, the shared resolver, #69 and P2 ARE ONE ARC, not four tickets.
  - Invariant 2 is false: cli.run() is ~196 statements / complexity ~50.
  - Because the edge absorbed the middle, the same precedence decision is
    implemented TWICE (cli.py:689 and :812) — that IS #69.
  - The 2026-07-19 ruling already prescribed the cure: "both entry points conform
    via ONE shared helper". #69 is still live, so the helper was never built.
  - The pattern is PROVEN IN THE SAME FILE: cli.py already has "one
    output-destination resolver shared by run + doctor". #69 needs the identical
    shape applied to INPUT precedence. This is a copy of a working pattern, not a
    design question — it makes the arc materially cheaper than it looks.
  - LESSONS records this parity pattern three times. #69 is instance four. Doing
    P2 without the extraction makes it instance five AND enlarges #92.
  - HARD CONSTRAINT, already recorded on #69: the gate expression is the SAME
    expression that makes 5-model the effective default. Pin bare-invocation
    5-model with a regression test BEFORE touching it, or a parity fix silently
    flips the panel to 3.

===============================================================================
6. OFF-REPO CONTEXT
===============================================================================

SESSION PLAN vs OUTCOME. The plan set: FLOOR = owner ruled + VISION/ADR-11/
ARCHITECTURE Ch1 amended in effect + frozen acceptance contract authored and
delegated. PRIMARY = boost built and wired, one raw question flowing end-to-end
including a decomposition case. STRETCH = the checker built and proven on a
seeded drift.

  FLOOR    HIT.
  PRIMARY  HIT, with a live billed witness.
  STRETCH  NOT BUILT — converted to an evidence-backed 14-rule spec, filed as
           [S18]/#97. Judged a better outcome; see tension (d).
  E4 (#4)  MISSED as an opportunistic rider. It was re-scoped but the amendment
           itself is not written. Honest miss against the plan.

  Unplanned and delivered: the night batch, the absorption of three windows of
  backlog debt, two id collisions caught and mechanised, and the ARCHITECTURE
  repair pass.

THEME STATUS — where the three actually stand:

  T1 BIAS. Formally stalled: #27 at 0/12, #18 merged but unclosed (no live
  witness), #19 undesigned, #55 design-only, #9 hard-deferred. BUT a real T1 win
  landed under a T3 label and should be credited: the GUIDE's own doctrine says
  question framing is the ONLY bias-control point with no safety net, and the
  boost is now STRUCTURALLY incapable of injecting model bias into the question —
  deterministic scaffolding plus the span gate mean the model cannot write
  content into the brief. That is a bias control enforced by construction rather
  than promised in a document. It is the first T1 property in the repo that
  cannot silently regress.

  T2 COST. Proven, not harvested. CLI seats witnessed at $0 marginal, ~10.7×
  cheaper end-to-end in the smoke pair. Entirely gated on #27 → ADR-12 §5 → #66.
  Zero movement this window and none is possible without the sitting.

  T3 DELEGATION. The window's real subject and its real progress. See section 0
  for the honest engine-vs-interface split.

OPERATOR-LEVEL NOTES:
- He asked twice for parallel execution and accepted the mechanical explanation
  both times. The parallelism that DID run was read-only fan-out during his merges
  — that is the shape that works here without worktrees.
- He is explicit that management of the methodology and the ecosystem — naming,
  versions, where each concern lives, documented vs coded — is the top framing,
  above the LLM debate itself.
- Recurring machine-level gotchas, route to the hub not here: worktree locks
  outlive their process (Get-Process the pid before any -f); the codex-review
  severity counter prints zero over real HIGH findings (console-only regex
  defect — read the artifact BODY).

ARCHITECT-SEAT FAILURE MODE, recorded because it will recur in the seat, not the
person. I asserted from prior reports rather than from verification five times
this session: a task-count baseline (47 vs the real 48), an unfiled-P1 count (9 vs
the real 8 of 16), the panel-default consequence chain (escalated as fact while
simultaneously commissioning the check that disproved it), a forward reference to
"#97 rule 14" when #97 had twelve rules — caught by the very rule I had just
proposed — and an allowed edge set derived from a map that may itself be
incomplete. Every one was caught by review; none by a gate. THE LESSON FOR THE
SEAT: the browser architect's irreducible half is the off-repo input, and that is
precisely where nothing downstream catches an error. Verify before asserting a
consequence, not in parallel with asserting it.

===============================================================================
ANSWER A — the allowed-set ruling's vehicle
===============================================================================

CC's question conflates two separate things. Split them.

(i) THE `cli -> boost` OPEN CASE (is boost core or orchestration?) — YES, this
rides the #69/P2 arc. That arc is what decides whether boost gains an
orchestration entry point when it is wired in, so ruling it earlier would be
ruling without the information the arc produces. Hold it open in ARCHITECTURE as
written.

(ii) THE MAP-vs-SOURCE COMPLETENESS GAP — NO, this rides nothing. It belongs to
#97 as rule 14's second leg and is independent of both #69 and #92. Do not hold
it behind an arc.

And the sharper point, which is why they must not travel together: RULE 14 AS
WRITTEN IS VACUOUS. It validates codemap against the allowed set — the map
against itself. It does not validate SOURCE against MAP, so an illegal import the
hand-maintained codemap simply omits passes the gate. That is the exact case it
exists to catch: `cli -> boost` was only caught because the night batch happened
to add it to the map by hand. Rule 14 needs two legs:
  (a) every codemap edge is inside the allowed set or a named open case;
  (b) every real import between modules in src/ appears in the codemap.
Leg (b) is what makes it a mechanism instead of an instruction.

FURTHER: if the commissioned grep shows `cli -> inbox` or `cli -> config` are
real, then ARCHITECTURE's allowed set is FACTUALLY WRONG TODAY, not merely
incomplete — and a wrong set is worse than a missing one, because leg (a) would
then validate against a false standard. That correction is immediate and
standalone, gated only on the grep result. It is not a held-open design question.

===============================================================================
ANSWER B — next-arc priority
===============================================================================

ORDER, with the reason each position is earned:

1. [S18]/#97 CHECKER v1 — FIRST. It is the only item that changes the failure
   rate of everything after it; every subsequent arc will produce drift and the
   checker is what catches it. It is also the least entangled: read-only, no
   contention on cli.py or output.py, so it cannot collide with anything else.
   Its spec is complete and evidence-backed. And leg (b) of rule 14 answers the
   `cli -> inbox` / `cli -> config` question MECHANICALLY as a byproduct, which
   is strictly better than answering it by hand.
   Build rule 14 with BOTH legs. Rules 13 and 14 were absorbed 2026-07-23.

2. #92 → SHARED PRECEDENCE RESOLVER → #69 → P2 — as ONE arc, in that order.
   Rationale in section 5. Doing P2 first enlarges #92 and makes #69 instance
   five. Non-negotiable sub-constraint: pin bare-invocation 5-model with a
   regression test BEFORE touching the gate expression.
   This arc also produces the information that rules the `cli -> boost` open case
   (ANSWER A(i)) — close it in the same arc rather than as a separate pass.

3. RECORD-DEBT — rides in the gaps, does not need its own window. The
   #110→#84/#128→#85 renumber is mechanical and now unblocked (ids reserved,
   grep-before-assign rule live); it folds in resolving the hub `refs #96` as the
   same edit. #4's ADR-02 amendment is small now that the panel-default question
   dissolved.

4. #99 TRIAGE — a decision session, not a build session. Its content is mostly
   deletions and keep-or-remove calls that only the operator can rule. Batch it;
   do not dribble it.

OPERATOR-RESERVED vs DELEGABLE:

  OPERATOR-ONLY, NON-DELEGABLE
    #27 blind scoring. One sitting. DO NOT SEQUENCE IT BEHIND ANY OF THE ABOVE —
    it is unblocked by all of them and can run in parallel with any arc. It is
    the choke point for two of three themes and has been deferred five times.

  OPERATOR RULES, CC EXECUTES
    #99 triage (deletions, keep-or-remove) · #4's overlap policy · the schema
    question in OPEN QUESTIONS 3 · the "how much should the boost boost" question
    in OPEN QUESTIONS 2.

  FULLY DELEGABLE
    #97 build · the #92/#69/P2 arc · the renumber · the ARCHITECTURE allowed-set
    correction if the grep comes back positive.
