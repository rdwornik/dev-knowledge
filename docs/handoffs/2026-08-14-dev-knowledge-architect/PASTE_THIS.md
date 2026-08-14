=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-14-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-14-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Execute wave 2 of W4 from the prepared `W4-WAVE2-INPUT.md` operator-side input file, and stand up the telemetry v1 EMIT lane (Stage 1 of the 2026-08-14 usage-telemetry design memo, `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`, attached as a leg on intake #29 Fold A). Two carried rows from batch-4's TRUE close — `[#514]` and `[#510]` — and the corrected five-branch `claude/*` night-lane resolution (see `RESIDUAL.md` §1 — SUPERSEDED-DELETE, dispositioned in STANDING_RULINGS §L/§M) are this window's inheritance, and the `[#492]` Grok re-check falls due 2026-08-17, inside this window. Live row set: `BACKLOG.md`.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->ratification/GO decisions named in `SUPPLEMENT.md` §7 — the wave-2 width GO, the telemetry v1 lane GO, the [#528] lane-latency GO, and any remaining ADR-112-adjacent promotion ratifications. **Not** a code lane: dispatch to execution lanes follows once GO is given, per the §1/§2 EXPANDED addenda in `SUPPLEMENT.md`<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->`SUPPLEMENT.md` §7 lists pending operator words (ADR-112-adjacent promotion ratification, wave-2 width GO, telemetry v1 lane GO, [#528] GO, the single-flight dispatch guard GO-or-park) that gate every execution lane this window would otherwise start — all *what should be true* questions, which is architect scope, not execution scope. The one state-integrity question this cut surfaced (the night-branch set) is now RESOLVED by the supplement's correction addendum, not a blocker on its own<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-cut-2026-08-14`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

# Residual — 2026-08-14-dev-knowledge-architect — the part the repo does not already encode

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
**STANDING / dispositioned — none of these is new this window** (dispositions live in
`ecosystem/disposition-register.yaml`; re-derive every value via P4/P6/P7/P9):

- The `undeclared_edges` prose-edge family (ADR-88 FC2) — owned by `[#241]`, cardinality-free
  Done-when so the set grows without re-breaking the row.
- `preflight_backlog_ids` — advisory per the `[#483]` R3 ruling.
- `review_artifact_coverage` — advisory per the `[#480]` P3 ruling, deferred pending 0 false
  positives over two consecutive windows.
- `journal_spine_anchor` "anchored by mention, not by record" — the advisory leg built under
  CODEX-524 leg (c) / L5; WARN-not-FAIL by design.
- `no_ff_merges` — three legacy June non-merge spine commits, grandfathered. **Never rewrite them.**
- `doc_rot` backlog-accretion on the large rows (`[#511]` `[#510]` `[#514]` `[#522]` `[#505]`
  `[#322]`) — the condense route is `[#426]`/grooming territory, not an in-window fix.

**NEW THIS WINDOW, RESOLVED BY CORRECTION:** the 2026-08-14 batch-4 TRUE close packet
(`docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §5) named **five** `claude/*`
branches as "the next window's inheritance" — `claude/nc-lessons-mechanisms-jw5dda`,
`claude/nd-governance-promotion-prune-77qc6b`, `claude/night-nb-handoff-prep`,
`claude/night-ne-northstar-value`, `claude/window-truth-audit-yr83j2`. This seat confirmed
(twice, via `git branch -a` after `fetch --prune` and `gh api repos/rdwornik/dev-knowledge/
branches`) that **none of the five exist on `origin`** — only `main` and `automation/
fleet-audit` remain. **`SUPPLEMENT.md`'s correction addendum resolves this**: all five were
verified branch-by-branch and deliberately deleted (verdict SUPERSEDED-DELETE — none was an
ancestor of `main`), with every actionable item individually dispositioned in
`STANDING_RULINGS.md` §L/§M (the 143/143 adjudication, tables M-1..M-11 — both confirmed
present in-repo). The per-branch deletion evidence itself is an **off-repo operator record**,
so it is advisory rather than re-derivable here — but the repo-verifiable half (branch
non-existence + the §L/§M disposition tables) checks out. Nothing was lost; the TRUE-close
packet's "next window's inheritance" phrasing is superseded, not this session's to edit
(`docs/audits/` is immutable).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
| id / artifact | Where |
|---|---|
| Batch-4 **TRUE close packet** — corrects FLAG-1's carried count now `[#513]` discharged; CLOSED `[#270]`/`[#132]`/`[#521]`/`[#513]`, CARRIED `[#514]`/`[#510]` | `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md`; commit `e4e1624b` |
| `doc_rot` dual-instrument claim corrected — no disposition-register suppression exists in code (one instrument, not two) | `STANDING_RULINGS.md` §O-1/O-2; commit `90daea1e` |
| Usage-telemetry design memo landed + attached as a LEG on intake #29 Fold A (v1-EMIT slice) | `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`; commit `c3c7aa90` |
| `[#526]`/`[#527]`/`[#528]` **born** (root-hygiene audit P3/S, anti-direct-to-main hook P2/S, lane-latency gate-mesh cost P1/M) + a leg on `[#523]` | `tasks/526-*.md`/`527-*.md`/`528-*.md`, `BACKLOG.md`; commits `30c1ed91`/`2588d07d`/`50e9f251`/`d63a6dc6` |
| `[#511]` three-loads split ruled **DEFERRED**, stays unsplit P2/M — "JOURNAL-purpose" load has no located scope anywhere in the tree | `STANDING_RULINGS.md` N2-E3-06 |
| ADR-112 bullet added to `ARCHITECTURE.md`'s Governing-ADRs list | commit `d63a6dc6` |
| 4 LESSONS entries appended — duplicate-execution, unlocated register loads, doc_rot dual-instrument, serialize-group derivation | `LESSONS.md`; commit `eac92922` |
| PR #67 merged `worktree-packet-close` → `main`, one commit per step | `65bdd836` |
| W4 wave-1 arithmetic: 69 live ids, 39 converted / 30 skipped, no skip silent | `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §3 |
| Two duplicate-execution artifacts (independent runs of the SAME packet-close contract, colliding on `[#526]`-`[#529]` numbering) flagged, **not merged**: `docs/packet-close`, `docs/packet-close-v2` — both now absent from `origin` post-PR-67 | JOURNAL 2026-08-14 (d) |

Detail is in `JOURNAL.md` 2026-08-14 (d)/(c); this is the map, not the recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**Three items, ordered by what blocks what — this session's own residual, distinct from
`SUPPLEMENT.md` (pointer, not a duplicate; its answers are folded into `PASTE_THIS.md`).**

1. **THE 5-BRANCH NIGHT-LANE SET IS RESOLVED, NOT OPEN.** §1 above records the correction:
   `SUPPLEMENT.md`'s addendum confirms deliberate SUPERSEDED-DELETE with every actionable item
   dispositioned in `STANDING_RULINGS.md` §L/§M. The remaining open question for `[#511]`'s I-D4
   continuity legs (R43/R50/R51) is narrower than "was this lost" — it is whether those
   distillate rows' own text still accurately cites what the (now-deleted) branches carried, a
   normal staleness check, not a recovery investigation.

2. **`SUPPLEMENT.md` §2 NAMES A CONCRETE NEXT-WINDOW MECHANISM CANDIDATE** — a single-flight
   dispatch guard against contract-of-record collision, born from this window's own near-miss
   (three concurrent executions of the packet-close contract; one caught and stopped via
   `TaskStop` before it merged anything; all three colliding on `[#526]`-`[#529]` numbering for
   the same four filings). It is a candidate, not a ruled row — whether it becomes a `[#id]` is
   the next architect's call.

3. **THE E1-5/L-9 TIMING CLAUSE DISCHARGES WITH THIS CUT.** `protocols/STANDING_RULINGS.md` L-9
   ("Clause 5 (handoff cut < 10 min) discharges by timing the very next cut") is satisfied by
   this bundle's own generation — the measured wall-clock is in this session's closing packet to
   the operator, not restated here. Whether the result clears the 10-minute bar, and what that
   implies for `[#511]`'s re-scoped non-mechanized load, is the next architect's read to make,
   not this cut's to adjudicate.
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
> **Branch note.** This bundle was generated on branch `docs/handoff-cut-2026-08-14`. This line names only *which*
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-14-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-14-dev-knowledge-architect/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
This bundle's supplement is **FILLED** — its ANSWERS fold into `PASTE_THIS.md`, so the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-14-dev-knowledge-architect/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-14-dev-knowledge-architect/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-14-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-14-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-14-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

§1 Intent: The 2026-08-12→14 window converted the planning surplus to law and executed: adjudication 143/143, W3 [#513] organ merged, W4 wave 1 (~36 conversions), corpus reconciled for [#492]. The next window is EXECUTION-FIRST: wave 2 W4 from the prepared input file, telemetry v1 EMIT lane (Stage 1 of the landed memo), [#492] Grok re-check 2026-08-17, satellite-serving lane due (≤2 windows from 2026-08-12).
§2 Tensions: parallel width is limited by the serial review gate (browser architect reviews every packet) and shared surfaces (BACKLOG/manifest regenerate) — wave 2 should run 6–10 disjoint tasks/-only lanes; integration is the bottleneck to price, not lane count. CODEX-524: producer activation undesigned (#341 open); R5 fallback ruled — do not re-litigate. three concurrent executions of one contract collided on ids ([#526]-[#529] double-assigned); single-flight dispatch guard (step-0 contract-of-record collision must block duplicate runs) is a next-window mechanism candidate.
§3 Rejected: standing OneDrive declared-need clause (T1 grant mechanism ruled instead); folds A+B (NIE — provenance over cosmetics); hollow existence checks (judgment carve-out class rules); reopening [#439] (new-row route ruled).
§4 Off-repo inputs: dispatch command format is exercised law (literal fenced block, PowerShell single-quote nesting, no \"); operator dispatches every lane himself; transport = file upload, never long pastes.
§5 Do-not-rederive: picker rulings (register sections L/M), FLAG-1 batch-close shape, W4 partition (69 live ids, wave-2 input file), baseline pins from PACKET-CLOSE step 4, telemetry route (leg on existing owner, v1 = EMIT slice, Zabbix/Splunk/OTel ruled do-not-adopt).
§6 Calendar: 2026-08-17 [#492] Grok re-check (corpus ready) · 2026-09-09 [#322] dated review · night-branch (claude/*) adjudication owed · #341 activation design when a window affords it. orphan packet-close branches deleted post-PR-67, [#514]/[#510] carried, night claude/* branches awaiting adjudication.
§7 Pending operator words: ADR-112-adjacent promotions ratification if any remain Proposed · wave-2 width GO · telemetry v1 lane GO.

---CORRECTION + EXPANSION ADDENDUM (outgoing browser seat, 2026-08-14, appended below the original answers per primary-source discipline; the original stands, this supersedes where they differ)---

**§6 CORRECTION (clears the gate's INHER FAIL):** The line "night claude/* branches awaiting adjudication" is STRUCK — it was written before the cleanup executed later the same day. Live truth: all five night branches (nc-lessons-mechanisms-jw5dda, nd-governance-promotion-prune-77qc6b, night-nb-handoff-prep, night-ne-northstar-value, window-truth-audit-yr83j2) were verified branch-by-branch and DELETED with verdict SUPERSEDED-DELETE — none was an ancestor of main, but every actionable item each carried is individually dispositioned in STANDING_RULINGS §L/§M (143/143 adjudication + tables M-1..M-11); the deletion report with per-branch evidence is in this window's operator record. Nothing was lost; the TRUE-close packet's "next window's inheritance" phrasing is superseded by this addendum. Remaining refs by design: main + automation/fleet-audit only.

**§1 EXPANDED — the next window's first hour, prescriptive:** Boot → gate → then dispatch WITHOUT a planning phase, in this order: (1) wave-2 W4 mini-GO straight from `~/Downloads/W4-WAVE2-INPUT.md` and its on-main twin (29 needs-draft ids + 1 re-check [#419]) — the needs-draft class means ONE draft-production lane (census-instrument, produces conversion drafts) runs FIRST, then conversion lanes consume them; (2) telemetry v1 EMIT lane per the landed memo's Stage 1 (events check_run / hook_run / blocker_fired; SQLite WAL + structlog; the leg is already filed on the telemetry owner — row-is-the-spec); (3) [#528] lane-latency P1 (pytest-xdist into the gate runs + codify the tiered-suite law: targeted in-lane, ONE full suite at integration) — this lane pays for every future lane, dispatch it early; (4) [#527] anti-direct-to-main local hook; (5) 2026-08-17: [#492] Grok re-check on the reconciled corpus (12/12 pinned, 0 flips — do not re-reconcile); (6) single-flight dispatch guard design (the §2 collision); (7) satellite-serving lane is DUE this window or next (≤2 windows from 2026-08-12 — [#293] runbooks 0/6 is the natural target). [#514]/[#510] carried legs ride as spare capacity.

**§2 EXPANDED — width and the review gate:** Run wave-2 at 6–10 lanes; the disjointness law is tasks/-file ownership (one file per id — partition freely). The serial browser-review gate is the true ceiling: BATCH the reviews — lanes commit-and-STOP, the operator relays packets in ONE file batch, the browser seat reviews the batch in one pass, the integrator merges the approved queue serially. Do not relay packets one-per-turn; that pattern cost this window hours. Suite economics until [#528] lands: full suite ≈ 15–16 min — budget one full run per merge, not per lane step.

**§4 EXPANDED — exercised operational law (verbatim, do not re-derive):**
- Dispatch template: `claude --bg --model <alias> --effort <low|medium|high> --worktree lane-<letter>-<id>-<slug> --permission-mode bypassPermissions "[dk · #<id> · <label>] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\<CONTRACT>.md — step 0 commits the contract of record; run the /lane-boot sequence from step 3 onward, commit-and-STOP."` Every contract carries this LITERALLY in a fenced ## Dispatch block, all fields filled by the architect/machine — the operator NEVER fills placeholders.
- PowerShell quoting: inner strings in single quotes; `\"` is a witnessed ParserError.
- Integration: `/lane-integrate <worktree-name>` in PRIMARY; regenerate BACKLOG/manifest/audit-index at merge, never hand-merge; JOURNAL day-letters derived at merge (re-letter later entry).
- Background sessions may refuse merge/push-to-main by their own standing policy and open a draft PR instead — that is lawful; the operator merges the PR (witnessed: PR #67 → 65bdd836).
- Teardown after merge: close the holding session on the Agents board FIRST (locks name live pids), then worktree remove + prune + branch -d.
- Transport: files, never long pastes; PASTE_THIS.md is the only sanctioned chat-paste.

**§5 EXPANDED — do-not-rederive additions (with locators):** PR #67 content IS the packet-close truth on main at 65bdd836 — the parallel duplicate runs' branches are deleted and ids [#529]/[#530] are FREE; [#526]=root-hygiene audit, [#527]=anti-direct-to-main mechanism, [#528]=lane-latency (P1) — these meanings are fixed, do not re-read them from the discarded run. [#511] is DEFERRED-unsplit by register ruling (N2-E3-06) — the discarded SPLIT never landed. Four window lessons are in LESSONS.md as PLAYBOOK-promotion candidates (dispatch-block law, PS quoting, repin guard, R5/#341) — promote via adjudication, do not hand-edit PLAYBOOK chapters. [#524]'s four legs are LIVE on main (62f42dad): day-letter check floored at 2026-07-30, past-review-date WARN, mention-not-record WARN (advisory, noisy at 381 mentions by design), hooks-armed assert.

**§6 EXPANDED — measured state at seal (baseline for the next window's deltas):** seal 1ffb030d (handoff cut ~43 min — the L-9/[#511] measurement, OVER the 10-min bar: register-line it and treat [#511] as evidence-fed now) · open-total 196, window net +3 (three ruled P1/P2 births — deliberate, priced) · untestable ≈58 (from 95; wave-2 target: ≤29) · doc_rot pin 38 (new instrument; the ship-gate WARN count is the OPERATIVE gate metric — P7 shows 41 undispositioned WARNs at seal: first grooming target) · suite 2891 pass / 1 owned RED ([#457] leg ii) / 17 environmental pandas-dep fails appear ONLY in isolation worktrees (not on primary — do not chase them) · P6 drift: doc-counts 2895 vs live 2897 (two tests landed after the count regen — one-line refresh, first mechanical fix of the window) · P4: #505 drift flag is the KNOWN false positive, do not close.

**§7 EXPANDED — pending operator words, complete list:** wave-2 width GO (recommend 6–8 + draft-production lane first) · telemetry v1 lane GO · [#528] lane-latency GO (recommend same wave) · single-flight guard: mechanism design GO or backlog-park · promotions still Proposed (if any at boot — check register) ratification · P10 full grooming census is the incoming seat's boot duty per the process's own text.

---END ADDENDUM---

---

=== END OF PASTE — 5 sections · 52991 bytes ===
