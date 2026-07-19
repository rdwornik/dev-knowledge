=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-19-corp-monorepo-architect` |
| **Chat title** | `[corp-monorepo] Technical Architect — 2026-07-19-corp-monorepo-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Decompose the next **product** arc for corp-monorepo now that E5 `#38` shipped merged primitives and every lane is integrated and torn down. The frontier is the E5 continuation (`#40 → #36 → #55`), the `[S10]` SIM-1 acceptance gaps, and the sized option menu in the module connection map — pick and sequence, then author the executor lane contract (including the one-channel pick). Navigate from the corp `BACKLOG.md` (E1–E7 in R10 priority sequence); orientation comes from `PROBES.md` P1, not from this header.<!-- FILL-IN:purpose END --> |
| **Target repo** | **corp-monorepo** — this bundle is hosted in the hub `.dev-knowledge` (ADR-36/41) and derived READ-ONLY from `../corp-monorepo`. **Every probe runs in the corp checkout**, not the hub. |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state, on hub branch `docs/2026-07-19-corp-monorepo-architect-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P2, in the corp checkout). |

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

# Residual — 2026-07-19-corp-monorepo-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to the corp `BACKLOG.md`, §6). Mode: **architect** (§13) — planning / decomposition posture; the session's WORK is **product**. **Target repo: corp-monorepo** — this bundle is hosted in the hub (ADR-36/41), derived READ-ONLY from `../corp-monorepo`.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live at derivation; `recall`/`inferred` = reconstructed from the corp JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS (the outgoing architect's strategic *why*) fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*. **Read the supplement's TRUST POSTURE line and its five off-file findings — they carry corrections this residual could not derive from the repo.**

---

## §1 — The headline: the E5 build crossed from design into merged code; the frontier is the `#40 → #36 → #55` continuation

**The largest single-window delivery since the A3 ruling landed, and it closed clean.** `witnessed` (READ-ONLY, at derivation): corp `main` is **clean**, **`main` is the only branch** — no open product lanes, no straggler, and **no worktrees registered** (`git worktree list` returns the primary alone). Every lane opened this window was integrated and torn down.

What a fresh architect chat lacks — and the ONLY thing this residual carries — is the **entry point + the decomposition frontier + the design "why,"** none of which the repo re-narrates:

- **Entry point.** Two documents, in this order. (1) The corp **execution charter** `docs/audits/2026-07-17-execution-charter.md` — still the single consolidated reading map (its §2 points at every canonical doc). (2) **New this window and load-bearing:** `docs/audits/2026-07-19-night-consolidation-decision-plan.md` — the N1 night-batch record **plus a large in-file amendment** (the module connection map). Its **§3-EXT start-here plan** is an ordered 8-step lane queue and its **§6 improvement options** table (O1–O9, each sized, NOT-list-bounded) is the decomposition menu. Read it second; everything in §4 below is a pointer INTO it, not a copy.
- **Role split (does not live in the repo).** This browser chat is the **TECHNICAL ARCHITECT** (Layer-1, no file access) — it decomposes the frontier into a task-graph, holds the whole-system view (A3 + `ARCHITECTURE.md`), and reviews each arc's plan before execution (one plan-review output-contract form: the exact CC option / paste-ready feedback / `approve`). The incoming Claude Code session is the **executor** (Layer-3, holds the tree). The architect does **not** execute. Methodology questions route to the **hub** `.dev-knowledge` (corp is A0-closed), **not** this chat.

Drift-flags are re-derived by the consumer's own live checks — **re-derive at read-time; the teeth are in `PROBES.md` (P1–P6), not in trusting these lines.** This bundle states **no** sha, count, armed-state, verdict, or region text — those are the probes' live answers.

**One standing caveat worth carrying (`witnessed`, from the module-map §7.2):** corp's `ARCHITECTURE.md` **codemap is substantially stale** — phantom import edges, one edge drawn as an import that is actually a subprocess, every runtime data-flow seam missing, and the new `#38` `ops/` modules unreflected. The audit proposes a rewrite scope (§7.3) but **deliberately did not execute it** — it belongs to the A3 R9 rewrite arc, **currently unscheduled**. Treat `ARCHITECTURE.md`'s codemap as an untrusted source until that arc runs; the module-map §5.2 is the witnessed replacement.

---

## §2 — Shipped this window (pointer, not re-narration)

Detail lives in the corp `JOURNAL.md` (newest-first) — not recapped here. The map, by lane:

- **E5 `#38` FR-10 source registry — BUILT and MERGED.** The epic's first build story: `source_registry.py` + `source_value.py` + `source_observation_repo.py` + a `source_observations` table, all pure-Python and **zero Graph calls**. 11 commits on `epic/e5-registry`; **+~80 tests** (`test_ops` roughly doubled). Cleared a **5-pass terra pre-merge review** — 6 P1s, every one a genuine fail-closed/design-invariant gap (silently-empty registry on a misspelled root key; unnormalized stored paths; `operator_prior=exclude` outvoted by arithmetic; silently-dropped unknown `dims` keys; a persistence-layer drop of the gate flag). **`#38` stays OPEN** — its "scout consumes the score" done-when completes at `#40`.
- **S13 documentation archival — SIGNED then EXECUTED** (two sessions, per the ADR-38 contract). `docs/audits/` shrank hard (relocations + signed deletions); `#66`/`#67`/`#68` all closed, story removed per ADR-65.
- **BACKLOG distribution — Parts 1 & 2.** Part 1 decomposed the census into **14 new tasks / 4 new stories** (`#55`–`#68`, `[S10]`–`[S13]`) under existing themes — operator picked "no new themes, no Big Picture edit." Part 2 ratified intake-16 §8.1 (the D1/D3/D4/D5 picks + the *"manual first, automate later; deploy first, iterate"* philosophy) → status **READY-FOR-TECHNICAL**.
- **Ratifications:** SIM acceptance-spec RATIFIED then relocated to `docs/intake/2026-07-18-func-sim-acceptance-tests.md` (taxonomy correction); **ADR-37 Accepted** (frontmatter-canonical + the facts_count projection leg); **ADR-38 Accepted** (deletion/relocation doctrine).
- **Night batch + module map.** N2 fixed `test_cke_paths_resolve` worktree-compat (the basename assertion → a stable pyproject-identity check); N3 filed `#69` (ADR archival). The N1 decision-plan was then completed into the **module connection map** — 8 modules, each verdict witnessed by command or `file:line`, adjudicated against an independent blind `sol` derivation, plus a freshness verdict and a 4/4 cold-reader comprehension probe.
- **One methodology lesson worth knowing (it shaped this window's process):** the **execution-channel discipline** entry in corp `LESSONS.md` (2026-07-19) — a prior session compounded BOTH build channels for the same epic (an in-terminal worktree lane AND a hub developer bundle) without the operator's one-channel pick. That pick is a **contract-authoring-time decision** and belongs to *this* chat when it spawns a lane.

**PENDING — nothing.** `witnessed`: no unmerged product branches, no open worktrees at derivation.

---

## §4 — Next-frontier (the design "why" that travels)

**The architect's job this session is to decompose the next arc within the operator's standing ruling** — *knowledge modules first, decks the NEXT phase*, with **SIM-2** (not SIM-1) as the phase acceptance bar and per-module witnessed sandbox runs (`#34` shape, `docs/intake/2026-07-18-func-sim-acceptance-tests.md` C1–C4/C6) as the acceptance evidence. Three ready frontiers, in the module map's own order:

1. **Finish the E5 epic — `#40 → #36 → #55`.** `#38` shipped the *primitives*; nothing is wired to the system yet. `#40` seeds the three operator golden sources, resolves them to Graph IDs, and scores them; `#36` runs the scout pilot (**day-1 = deterministic `rank_by_value_score`; the bandit is cycle-3+**); `#55` emits the draft Content-Manifest. Only then does the epic finalize. **The `epic/e5-registry` branch and its worktree are gone** — a `#40` lane starts fresh from current `main`, which supersedes the module map's §3-EXT step 1 ("sync the lane forward"). **Graph consent is GRANTED and auth D2 = delegated SSO user token + refresh** (operator charter for this lane) — but see the open question below.
2. **The SIM-1 acceptance gaps — `[S10]` `#56`–`#60`.** The spine runs end-to-end, but the module map's **§5.3 unwired-seams** list names what it costs: body-FTS absent (**the biggest live gap inside the otherwise-wired spine** — body-phrased queries return nothing, which degrades exactly the RFP grounding R10 elevated the knowledge loop to protect), no project↔vault link, index-hygiene duplicates, split path/config resolution.
3. **The `[S11]` RFP intake** — **but its input may not exist.** The module map records that the terrain-recon return branch is **absent from this repo** and must be located elsewhere or treated as not-yet-produced. Do not schedule `[S11]` on the assumption that recon landed.

**The decomposition menu is already written and sized:** module map **§6** options **O1–O9** (body-FTS · ingest cold-start · project↔vault link · `com` revival · `#38` registry wiring · the vault-writer invariant hole · synthesize→vault · Content-Manifest→deck · the ADR-27 doc drift). They are **options, not decisions** — the architect picks and sequences; each is NOT-list-bounded.

> **One menu row is already dead — do not spend a lane on it.** `witnessed` (CC re-derived live at derivation): **O2 / F1 (ingest cold-start) is FIXED**, not open. The module map's §5.3.9 and its O2 row still describe it as a live crash, but `#35` landed the bootstrap + fallback floor (`bootstrap_content_registry` and the empty-fallback path are present in `src/corp/ops/registry.py` on `main`). The audit is stale on this row; the code is the truth. **Generalize the habit, not just the correction:** re-witness any F-number, count, or audit finding at the moment it drives work — this arc alone overturned two census counts, a bundle premise, and this F-row. Two are worth flagging as cheap-and-load-bearing: **O4 `com` revival is ~4 env vars and one filename, zero code**, and **O6 closes a real safety hole** — `copy_to_vault` writes into the protected zone bypassing `write_note`, so the ADR-27 enforcement test **false-greens** and unvalidated notes can enter undetected. One option is explicitly **PARKED per ADR-37(iii)**: the key_facts retrieval surface — do **not** build it until a witnessed post-F6 real-RFP grounding failure.

**The R10 "why" (unchanged, still governing):** after the F0/E1–E2 substrate, the **knowledge loop (E5/E6) takes precedence over the RFP rewrite (E4)** — a conscious, recorded deviation from the intake's "build before gap-fill" order; the BACKLOG sequences themes E1→E2→E3→**E5→E6**→E4→E7 accordingly (theme *ids* keep identity, theme *sequence* carries priority).

**CLOSED — do NOT re-open (charter §3, PROBES P5):** CKE is a subprocess with an explicit contract (R2, one invoker); accessors resolve through config incrementally (R6); the corp↔consumer seam is the T6 Content Manifest; seam contracts are guarded by N2-class seam tests. If an arc's plan reaches for an infrastructure tier (a service, mesh, or bus), the architect rejects it — a violation at 3-RFPs/month scale.

**Operator queue (off-repo — the §13(d) beat captures it live; charter §5 is the verbatim list).** Carried forward and still open: the absent vault git remote, 4 credential rotations, final backup-zone names, the ADR-35 amendment decision (backup leg-2 → personal OneDrive, `#18`), the T6-D4 SharePoint confidentiality push. **New this window** (module map §4-EXT): final **zone names (DR-6/7)** gate `#35`'s renames · run `#69` (the ADR-archival forwarding-marker arc) now or hold · **the ADR-27 §Decision-2 doc drift + the `copy_to_vault` invariant hole — enforce-fix now or schedule to the A3 R9 arc?** · and one the module map left genuinely unresolved: **is Graph auth D2 fully closed by the charter grant, or still jointly dependent on X1's ADR (DR-11 family)?** That last one gates `#40`'s live-resolve leg, so settle it before scoping the lane.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the corp **`BACKLOG.md`** (E1–E7 product story-map in R10 priority sequence, machine-checked by `validate_backlog` — counts re-derived live, `PROBES.md` P3), the live in-progress branches (`git branch -v` — none open at derivation; P2 re-derives HEAD/branch/ahead-behind), and any drift-flag the consumer's checks raise. Re-narrating item text splits the truth — the pointer + the live probe is the whole task-state. **A closed id never returns:** the next-free task id is `max` bracketed `[#NNN]` across **all git history** + 1, not the live-file max (P3's second command). **The anti-bluff PROBES manifest (`PROBES.md`, P1–P6) is the load-bearing carrier: every claim above that could drift has a probe.**

---

=== PROBES.md ===

# Probe manifest — corp-monorepo architect (2026-07-19): orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE corp-monorepo checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, region text, verdicts, or orienting lines are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub `.dev-knowledge`; its probes bind to **corp-monorepo** — run them in the corp checkout (`../corp-monorepo` from the hub, or the corp working directory). The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values. Hub-only surfaces (`ALL_CHECKS`, `ecosystem/doc-counts.md`, the disposition register, `validate_doc_claims`) are **deliberately absent** — corp does not carry them, and a probe pointing at a non-existent target is an `anchor-missing` FAIL by construction.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line enters the session **only** by CC reading the **live** primary source, and the quote must match as a **substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of corp `VISION.md` `## Vision` — *what corp-monorepo is*. | corp `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of corp `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits*. | corp `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d).** The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin` is it? | live git (the corp-monorepo checkout) | the summary holds a generation-time state; corp closed a large window this cycle (S13 archival execution, the E5 `#38` merge, the night batch, the module-map lane) and the next arc moves HEAD again — any baked sha is already stale | `git rev-parse --short HEAD` then `git status -sb` |
| P3 | How many **themes / stories / tasks** does `validate_backlog` count in corp's `BACKLOG.md` right now, does it report `OK`, and what is the **next-free task id**? | corp `BACKLOG.md` product story-map (E1–E7, R10 sequence) ∩ `scripts/validate_backlog.py` | the counts drifted twice this window (the +14 distribution decomposition, then the S13 closes) and drift again on any edit; neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py BACKLOG.md`, then `git log --all --oneline \| grep -oE '\[#[0-9]+\]'` for the next-free id (max across ALL history +1, never the live-file max) |
| P4 | Are corp's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`? | the corp checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` (must be unset/empty) |
| P5 | Quote, **substring-exact**, the first content line inside the `owner=hub` region `conventions-commit-branch` of corp's `CLAUDE.md` — confirming the hub methodology is materialized **verbatim**, not paraphrased. | corp `CLAUDE.md` region `<!-- methodology:start id=conventions-commit-branch owner=hub -->` | the owner=hub region text is byte-fixed from the hub template (`templates/claude-regions/`); a summary paraphrases it and cannot reproduce the substring | `grep -n -A4 "methodology:start id=conventions-commit-branch" CLAUDE.md` → the quote must be a substring of the live region |
| P6 | How many `.md` files does corp's `docs/audits/` hold **right now**, and how many live in `docs/archive/`? | corp `docs/audits/` ∩ `docs/archive/` (live filesystem) | the S13 archival manifest executed this window (relocations + signed deletions), so both counts moved and will move again on the next manifest; neither number appears in this bundle | `ls docs/audits/*.md \| wc -l` then `ls docs/archive/ \| wc -l` |

## Gate procedure (CC)

1. **P1 first** — the forced orientation read (P1a + P1b) establishes the vision frame before product planning resumes; the architect may not begin design until it holds both lines. **Then run the §13(d) operator-context beat NARROWED** — the supplement is FILLED and its ANSWERS are in the paste, so the ask is *"anything changed since the supplement was written?"*, not the full off-repo interview. Then P2–P6, each against **live corp state now**.
2. **P5 early among the teeth** — the forced CLAUDE-region read confirms the hub methodology layer is materialized verbatim (corp is A0-closed; methodology questions route to the hub, not this chat).
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P6 are *designed to move* between generation and check-time — that is the point. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P2's HEAD/branch is designed to move (the next product arc) — re-derive it live, do not trust the residual's prose.

---

=== SUPPLEMENT.md ===

========== SUPPLEMENT ANSWERS — corp-monorepo, outgoing architect, 2026-07-19/20 ==========
State at handoff: main 1dfee3e · single branch · zero worktrees · 2730 tests green · no
unmerged work anywhere. Companion artifact: SOURCE-MAP-corp-monorepo-successor.md (the
"which file answers which question" index — read it with this).

--- 1. STRATEGIC INTENT (way-of-working level) ---

The repo crossed from consolidating knowledge to building with it. Consolidation is DONE and
measured: 52 of 53 consumable July artifacts have witnessed downstream consumption; the one
outstanding (intake-16) is ratified and in build. So the next session's goal is NOT "consume
more" and NOT "audit more". It is to make the loop hold MECHANICALLY instead of by architect
vigilance. Three way-of-working goals, in priority order:

(a) COMPLETE ONE FULL EPIC CYCLE, DELIBERATELY. The developer/epic pipeline has never run
    end-to-end: G-A (intake→ADR→epic with stories+done-when) → G-B (architect-authored
    ex-ante done-contract, FILE-BOUNDARY, escalation, MODE) → build → G-C (RETURN → review →
    serial merge → closure on the HARD metric → teardown). #38 was a STORY return inside a
    lane, not a closed epic. E5 (#40 → #36 → #55) is the right vehicle: finish it as a real
    epic cycle with a return artifact and a teardown, so the pipeline is proven once before
    KE and RFP ride on it.

(b) GUARDS MUST BE PROVABLY GUARDING. This session found a PASSING safety test in front of a
    VIOLATED invariant (details in Q4/Q6). The methodology's load-bearing claim is
    "instructions are requests, MECHANISMS are guarantees" — a mechanism that cannot see what
    it claims to guard is worse than prose, because it manufactures confidence. The
    generalizable rule the next session should establish: every safety/invariant test
    declares WHAT it scans, and is itself verified against a known-violating negative
    fixture. Start with the one concrete instance (vault-writer), then decide whether the
    rule belongs hub-side.

(c) RE-WITNESS AT POINT OF USE. A document produced two days ago contradicted a merged,
    witnessed fix (F1/O2 — see Q4). The rule that caught it was applied ad hoc by the
    architect. Make it routine: any ruling that cites an F-number, an audit finding, or a
    count re-witnesses it live at the moment it drives work. Evidence has a shelf life; the
    census counts alone were corrected twice this arc (17→19 digests, 3→8 audits).

Standing product goal underneath all three (unchanged, operator-ruled): four focus modules to
DEPLOYED-AND-WITNESSED — metadata/Obsidian · URL/source registry · knowledge extractor · RFP
agent. Acceptance = a green WITNESSED sandbox end-to-end run per module. C1 is closed; C2, C3,
C4, C6 remain. Decks are the NEXT phase (C5 and the SIM-2 run deferred with it).

--- 2. TENSIONS WEIGHED ---

(a) Consolidate vs build. The operator was (rightly) tired of circling; building on unconsumed
    knowledge would have repeated work already paid for. LANDED: one evidence census, then
    build. WHY: the census proved the felt problem was execution, not consumption — and it
    cost hours, not days. Do not re-open; do not re-audit July.

(b) Archive hygiene vs reference integrity. The operator wants consumed artifacts out of the
    working folders; moving them strands citations inside immutable ADRs. LANDED: #68 policy —
    relocation requires FULLY CONSUMED **and** SUPERSEDED; citations move in the same commit;
    JOURNAL is never edited; a move that would strand a live citation is BLOCKED; LIVE specs
    archive at closure only (intake-16 at E5 closure, the SIM spec at deck-phase closure).
    2026-07-06-technical-architect-intake was DEFERRED, not moved, for exactly this reason.
    WHY: a tidy folder is worth less than a resolvable citation graph.

(c) Facts revival vs staying dead. Evidence overturned a premise mid-arc: key_facts is densely
    populated (392/488 notes), which made revival CHEAP — and cheap is seductive when a signed
    deletion (Arc-B B2) stands behind the current state. LANDED (ADR-37): the pipeline stays
    dead; add exactly ONE projection (facts_count from frontmatter) so the 29 consumer sites
    stop reporting a lie; a key_facts RETRIEVAL surface is parked behind a quantified trigger
    (witnessed post-F6 grounding failure in real RFP use). WHY: cheap ≠ needed; the chosen
    retrieval surface is body-FTS, and reversing a signed deletion on enthusiasm would gut the
    deletion doctrine.

(d) Canonical layer: frontmatter vs DB. LANDED: frontmatter canonical, index.db a derived,
    disposable projection, NO dual-write ever. WHY: witnessed reality — the DB is
    drop/recreate on rebuild and never projected the richest frontmatter fields.

(e) Two build channels. Worktree lane in-terminal vs epic outsourcing via a dev-knowledge
    developer bundle are BOTH legitimate; compounding them cost a session of confusion and
    contaminated a live hub session. LANDED: the channel is an OPERATOR pick, asked BEFORE any
    provisioning; corp currently runs primary + `claude --worktree`. The generated E5 bundle
    is quarantined hub-side — do not recreate it in corp.

(f) Path safety vs friction. After the docs/templates violation I hard-gated all new paths;
    that then STOPPED a fully convention-compliant ADR path and wasted a round-trip. LANDED
    (operator ruling, codified hub-side as ADR-101): compliance IS authorization — a path
    matching a codified, citable convention proceeds WITH its citation as the audit trail;
    unsanctioned paths and ALL new folders stay hard-gated. Also settled in the same family:
    docs/audits/ is markdown-only at the root — no subdirectories, no working corpora.

(g) Serial orders vs orchestrated fan-out. Serial single-thread CC orders are simpler but
    degrade badly on read-heavy multi-module work. LANDED: audit/review-scale work runs as
    Opus orchestrator + Sonnet bounded probes + Haiku read-only fan-out + an independent Codex
    derivation, in its own worktree, with ALL git mutations serial in the main thread. PROVEN
    this arc: a blind sol derivation from src/ alone added three real edges the CC probes
    missed, while the CC probes caught one thing sol was structurally blind to.

(h) Deterministic scoring vs learning. LANDED: equal weights day-1 with `weights_version` as
    the tuning seam; neighbour-prior is single-pass from intrinsic scores (the bounded form);
    bandit only at cycle 3+ behind the quantified trigger (≥3 cycles, ≥30 labelled, top-3
    precision <70% twice). Literal PageRank is permanently NOT-listed. Safety/consent gates
    numerically override any score — `exclude` means non-rankable and cannot be outvoted by
    arithmetic.

(i) BACKLOG shape. New themes (E8/E9/E10) vs stories under existing themes. LANDED: Option B —
    stories under E3/E4/E5/E7. WHY: theme SEQUENCE carries R10 priority, so appending new
    themes after E7 would have buried the operator's own focus modules at the bottom of the
    priority order. Execution order is lane-scheduled by the architect, never derived from
    theme position.

(j) Comprehensibility vs completeness. The cold-reader probe (4/4 ANSWERED) proves what is
    written is understandable from the repo alone — it does NOT prove the map is complete.
    Completeness rests on two blind derivations agreeing. Keep both instruments; do not let a
    green probe create false confidence.

--- 3. CONSIDERED + REJECTED (do not relitigate) ---

· Literal PageRank — permanently NOT-listed (A3). Neighbour-prior single-pass is the sanctioned
  bounded form.
· Reviving facts / facts_fts tables, loader, or FTS — rejected in ADR-37 even after evidence
  made it cheap.
· Dual-write between frontmatter and the DB — rejected (ADR-37).
· A speculative key_facts retrieval index before body-FTS proves insufficient — parked behind
  the quantified trigger, not built.
· Building a data/kb canonical-JSON producer for the RFP agent — REJECTED on evidence: the
  Word/Excel lane is already vault-wired via rfp/vault_adapter.py (subprocess `corp retrieve`);
  the canonical JSON is a VESTIGIAL FALLBACK to retire, not an orphan needing a producer. This
  overturns the process audit's F11 framing — build body-FTS instead.
· New BACKLOG themes E8/E9/E10 — rejected (see 2(i)).
· Relocating 2026-07-06-technical-architect-intake — DEFERRED (#69): would strand four
  immutable-ADR citations. Only a forwarding-marker arc makes it movable.
· Recreating the E5 developer bundle inside corp — rejected; it is quarantined hub-side and the
  active channel is primary + worktree.
· Blanket pre-commit blocking of every new path — rejected in favour of the two-tier rule.
· Rewriting ARCHITECTURE.md now — rejected: that is the A3 R9 "as-is docs rewritten once" arc.
  Only the item-by-item drift list and a proposed rewrite scope were produced.
· Deck / PowerPoint work this phase — operator ruling: next phase.
· Any service, mesh, or message-bus shape — A3 NOT-list at 3-RFPs/month scale. If a plan
  reaches for an infrastructure tier, reject it on sight.
· Editing signed manifests, ADRs, audits, or JOURNAL in place — supersede or use the sanctioned
  amendment marker; never in-place.
· Fixing test_cke_paths_resolve inside the E5 lane — rejected as out-of-boundary; it was fixed
  on main by the night batch instead.

--- 4. OPEN QUESTIONS ---

DESIGN (need a ruling):
· Does the classify→finalize inbox path have to trigger extraction? Today it does NOT, so files
  routed that way land with no knowledge note — silently. Product decision, operator-owned.
· Vault-writer invariant fix SHAPE: route copy_to_vault through write_note, extend the AST
  scanner to follow helper calls, or both (my ruling: both). The generalization — should every
  safety test carry a negative fixture and declare its scan scope? — is probably a hub-level
  methodology question, not a corp one.
· INDEX_EXTRA_ROOTS federation vs ADR-22 merge: federation is BUILT and TESTED (config.py:100,
  schema/pipeline_config.py:77); ADR-22 was ratified-but-never-built and is superseded by
  ADR-33; the ACTIVATION ratification is not witnessed anywhere. Needs a decision inside the
  RFP intake.
· ADR-27 canonical-output prose (02_sources/ vs the actual 01_Knowledge/ routing) — amendment
  marker now; the full doc rewrite belongs to R9.
· How does the E5 epic CLOSE, given the bundle is quarantined — a close-out audit doc (my
  ruling) or a regenerated return artifact? Process question for the hub.
· Who schedules the A3 R9 as-is-docs rewrite arc? Its trigger and authorship have been
  unscheduled since the ruling was written.

DELIBERATELY DEFERRED (do not treat as forgotten):
· ARCHITECTURE.md rewrite → R9. · #69 ADR archival (forwarding-marker arc on ADR-33/34/35/36) →
  operator: run now or hold. · key_facts retrieval → quantified trigger. · Paper-only ADR-34/35/36
  enforcement → stories #63–#65 (enforce OR record an explicit deferral naming the gap). ·
  Deck lane C5 + the SIM-2 run → deck phase. · #35 follow-ups: the ≥80% dry-run match check and
  the DR-6/7 zone renames (renames blocked on the operator's final zone names).

STATUS UNKNOWNS (not design — someone must simply look):
· The RFP terrain-recon lane was launched and its return was NEVER reported; no *terrain*/*rfp*
  branch exists in corp. Locate it or treat the recon as not-yet-produced before relying on it
  for the RFP intake.
· The night CR batch (N1-A..D) status since it was rescheduled.

OPERATOR-ONLY (only Rob can close):
· Which RFP-KB product families count as "gold" (evidence: the KB is real submitted BY answers,
  mixed quality, Planning-heavy 894/1329 — so it is neither a curated gold set nor a dump). ·
  Final zone names (DR-6/7). · 90_Archive: JOURNAL says 9 stale projects were moved, the zone is
  empty — where did they go? · SharePoint/Salesforce: is automation wanted, or is the manual
  interface deliberate? · Whether the sanctioned-pattern path guard gets built (may already be
  absorbed hub-side).

--- 5. DECOMPOSITION RATIONALE ---

SHAPE. Themes E1–E7 carry R10 priority in their SEQUENCE (knowledge loop E5/E6 before the RFP
rewrite E4), so new work enters as STORIES under existing themes and never as appended themes.
One build unit = one story cluster = one lane; lanes are file-disjoint by construction — E5 owns
src/corp/ops registry surfaces, KE owns extraction/index surfaces, RFP owns retrieve/rfp
surfaces, doc lanes own docs/. That disjointness is what makes two lanes safe in parallel, with
the operator as the single serial merge gate.

REGISTRY ORDER IS FIXED AND D8-CORRECTED — do not re-conflate: #35 is the ContentRegistry
ROUTING gate (DONE, closed C1); the FR-10 SOURCE registry is #38 (DONE — primitives only) →
#40 (seed the three golden sources, resolve, score) → #36 (scout pilot, day-1 deterministic
rank) → #55 (draft Content-Manifest, the deck-facing tail, DRAFT schema, small, NOT a deck-lane
beachhead).

REPAIR PRIORITY PRINCIPLE (use it to schedule lanes, it was derived from the connection map):
failures cluster as (a) BYPASSES of the main path, (b) DERIVED DATA nobody writes, (c)
CAPABILITY not yet wired. Close bypasses first — they cause silent wrongness that nobody
notices for months; missing capability is visible the moment you need it.

MUST NOT BE REDONE OR RE-DECIDED:
· The July knowledge census (52/53) — do not re-audit July.
· The module connection map — consolidate FROM it; but re-witness any individual cell before
  acting on it (see the F1/O2 trap in Q6).
· The process audit, the architecture ground-truth recon, the A3 R1–R10 ruling, the deletion
  doctrine and its amendments, the S13 manifest rulings — all settled records.
· intake-16 and its D1/D3/D4/D5 picks — ratified.
· ADR-37 and ADR-38 — accepted; changing either requires a SUPERSEDING ADR with new evidence,
  not a re-argument.
· The Option B backlog structure.
· The #38 build rulings: a single `weights_version` field (no separate score_version),
  round-half-UP (not banker's), `exclude` → gated with score forced to zero.

--- 6. OFF-REPO CONTEXT ---

OPERATOR WORKING CONTRACT (hold this or lose him — every item below was learned the hard way):
· Plain human terms first, acronyms explained; insight-first with the "so what"; scannable;
  zero corporate filler; shortest complete answer.
· Bounded A/B picks for decisions, never questionnaires. He is a peer, not a menu.
· Progress reports must be product-owner concrete — use case by use case, evidence, and an
  explicit what's-missing list. Abstract shorthand gets rejected.
· NEVER create, move, or delete a path without his word. Two violations this window (a template
  file in a new docs/ folder; an acceptance spec dropped at docs/ root on an inherited path).
  Every path an order emits is either convention-cited or delegated as
  "derive-quote-propose-STOP". He signs every deletion (ADR-38 manifest).
· ANY side-effect-producing task while the primary is busy goes to a WORKTREE, always — the
  cost is not merge conflict, it is the primary losing trust in its own state. Propose the
  worktree unprompted; state its NAME in chat, paired 1:1 with the prompt filename.
· The build CHANNEL (primary vs worktree vs epic-outsourcing) is HIS pick, asked BEFORE
  provisioning. Never compound two mechanisms.
· He is the serial merge gate; lanes commit-and-STOP and never self-merge.
· Paste blocks must be SELF-CONTAINED. The night batch ran degraded because a full spec never
  reached the executing session; the #38 plan review stalled for the same reason. Assume the
  receiving session has NO chat context.
· Multi-agent utilization is mandatory for audit/review-scale work; under-use is a routing
  failure, and he will say so.
· Prose→mechanism: a recurring instruction written as prompt text is a routing failure. Guards,
  checks and verification belong in scripts/hooks/skills.
· Night missions are PRE-AUTHORIZED — never insert an approval gate between the paste and the
  start; safety lives in the stop conditions. Record the matrix in the log instead.
· Codex: terra reviews EVERY code merge (it earned it — six P1 findings on #38 across five
  passes); sol for independent/adversarial derivations and cold reads; luna for cheap read-only
  fan-out; smoke before relying (quota has been volatile). Every plan names its Codex lane or
  gives a one-line reason for its absence.
· No LLM budget ceiling. Sky-is-the-limit first, optimise later if he asks.
· He signs off on the SUPPLEMENT: the architect authors these answers in chat; CC only
  transcribes them verbatim.

OPERATOR PHILOSOPHY (recorded, and it decides design defaults): manual first, automate later.
Deploy the system first, improve it iteratively. Deterministic before learned. A safety gate is
never outvoted by a computed score.

FINDINGS THAT ARE NOT (YET) IN ANY FILE — these travel only here:
1. STALE EVIDENCE TRAP. The night decision-plan doc's §5.3.9 and option O2 still describe the
   ingest cold-start crash (F1) as OPEN. It is FIXED — #35, merge 6c36f61, witnessed by the
   SIM-1 diagnostic (fresh env self-seeds the registry, 95% match, real assets untouched). Do
   not spend a lane on it; re-witness before believing any F-number.
2. P1 REPAIR, RULED BUT NOT BUILT. copy_to_vault — live in the extract_project workflow — writes
   into the protected 02_sources/ zone via shutil.copy2, bypassing write_note (no frontmatter,
   no quality gate, no conflict protection), while tests/safety/test_vault_writer_invariant.py
   PASSES because its AST scanner reads only actions/*.py textually and cannot see the mutation
   inside the called helper in vault_io.py. Fix the mechanism now; only the ADR-27 prose
   correction defers to R9.
3. NEW SILENT GAP. The secondary inbox path classify→finalize never calls extraction; files
   routed that way land with no knowledge note and no error.
4. A RULING TO DROP. The "E4=WARN routed to primary" entry could not be witnessed anywhere in
   src/, config/, or intake-16 — it was a chat-level test disposition, and the night batch
   actually FIXED that test (repo-toplevel identity instead of checkout basename). Moot.
5. THE CHEAPEST HIGH-VALUE ITEM ON THE BOARD. `com` (deal loop) is config-stalled, not
   abandoned: four unset env vars plus one template-filename correction, ZERO code, confirmed by
   two independent witnesses; corp/config.py already defaults the same env names to the real
   MyWork paths. Reviving it also activates the dormant com→index edge.

CROSS-REPO: corp is A0-closed — methodology comes FROM the hub, corp never invents it. The
two-tier new-path rule is codified hub-side (ADR-101, "compliance IS authorization"), in force.
The E5 developer bundle is QUARANTINED on a hub branch, not destroyed. Methodology questions
route to the hub, not to this chat's successor.

TRUST POSTURE — the single most important line in this supplement: inherit NO verdict from any
prior chat, audit, or summary without a live probe. This arc overturned census counts twice,
a bundle premise (Graph consent), an audit's F-list entry, and two senior verdicts. The repo is
the truth; documents are its shadow, and shadows go stale.
========== END SUPPLEMENT ANSWERS ==========
