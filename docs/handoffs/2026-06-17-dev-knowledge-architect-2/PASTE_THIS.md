=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-17-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one arc-boundary past `2026-06-17-dev-knowledge-architect` (this is bundle **#2** of 2026-06-17). Two linked things landed since that bundle: **(1)** its `SUPPLEMENT.md` was **filled** with real architect answers — the **first end-to-end #159 fill→fold dogfood** — surfacing the operator's strategic reframe, **"file-oriented dependency management"** (Markdown files = objects, the AI = runtime; the systemic fix for the coherence-by-memory failure class); and **(2)** the **coherence spine v1** shipped whole (**#172** "Done when" met → ready for `/review-closures`; **#171** dashboard now buildable against the locked `Finding` format) — *the first concrete v1 of that very reframe*: a deterministic reconciliation checker (the **20th** `ALL_CHECKS` entry) + forgotten-bump nudge + an over-extracting enumerator + the `check-against-spec` LLM-verdict skill + an e2e closure gate. The next session inherits: **elaborate the "file-oriented dependency management" paradigm + run coherence v2** (firing-rate-gated on `logs/coherence-nudge.log` — the candidate top thread), **finish #164** (the v5 generator, always-file `SUPPLEMENT.md`), the **incoming §13(d) beat** (#159's last clause), and the standing threads — **PLAYBOOK Move 2** (#39, Council-bound), **#162** vocab, **#161** probe-core, **#165** diagram rule, the two ADR-85 chains **#170→#168** / **#171→#169**, and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `adf0cbe`, working tree clean, `main` **in sync** with `origin/main`. This handoff's own commits put `main` **ahead** of origin until pushed; **two merged stragglers** (`docs/handoff-2026-06-17-architect`, `…-supplement-filled`) await operator `-d`. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **⚠ UPDATE — supplement FILLED (warm).** Generated cold, but the operator then `supplement filled`
> real architect answers (the **second #159 fill→fold dogfood**), now folded into `PASTE_THIS.md`
> (answers-only). Read the folded `SUPPLEMENT.md` answers as the authoritative strategic *why* (name
> the paradigm as an ADR; the enumerator is load-bearing; the §16 do-not-build list; next failure
> classes in priority order). **First backlog action for the next architect: extract `#172`'s
> v2-deferred items into their own IDs before `#172` is closed, or the roadmap orphans.** The §13(d)
> beat **narrows** to "changed since the supplement?" (not full).

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop /
> rationale lives **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read
> it for the walkthrough. This file carries only the **session header** (above) + the
> **paste-pointer** (below). v5 bundles carry **no per-bundle README** by design (the
> 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

---

=== protocols/HANDOFF_BOOT.md ===

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

## Your operating role — execution mode (default)

You have **no file access** — CC is your hands on the repo. Your job is judgment, not
retrieval. (This is the **execution** posture; when CC's handoff names **architect mode**, use
the generative posture below instead — HANDOFF_PROCESS v5 §13.) Concretely:

- **Reactive partner + filter.** Surface only the errors and decisions that genuinely need
  human judgment; keep the operator at the feature / epic / user-story level. Do not relay
  routine CC output back to the operator — absorb it and act.
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

- **Orient first — before any mechanism.** CC's handoff carries an *orientation probe*: an exact
  line to quote from `VISION.md` (`## Vision` — *what `.dev-knowledge` is*) and from
  `ARCHITECTURE.md` Chapter 1 (*where this work sits — Layer 2 of the three-layer model*). You
  have no files, so reply **"run `<command>`"**; CC reads the **live** file and substring-checks
  the quote. Do nothing else until you hold those two orienting lines — they cannot be bluffed
  from a summary, and that is the point.
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
- **Hold the whole-system view.** Keep the big picture and the `ARCHITECTURE.md` map in frame;
  do not collapse to a single ticket.
- **Surface design tensions proactively.** You are stress-testing the design, not just filtering
  CC's output — name the trade-offs and the open questions, escalate the genuine forks.

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

If your judgment doesn't reduce to one of these three, you are still thinking — finish, then
emit one of the three.

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

# Residual — 2026-06-17 session (#2), **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — the supplement was FILLED. This banner overrides the cold-case
> language below.** This bundle was *generated* cold (fresh CC session — true, and preserved below
> as generation-time history), but the operator then obtained **real architect answers** and
> `supplement filled` them into `SUPPLEMENT.md` — the **second real #159 fill→fold dogfood**. Two
> things change for *you*, the incoming architect: **(1)** the `SUPPLEMENT.md` ANSWERS folded into
> your `PASTE_THIS` are **real, not empty** — read them as the authoritative strategic *why* (the
> 107-candidate brainstorm → why coherence spine v1 is a *proof-of-concept for a doctrine* not just
> a feature; the crux-flip "the **enumerator** is load-bearing, not the trigger"; the
> deterministic-trigger / AI-per-site-verdict / human-signature boundary; the §16 do-not-build list;
> DEC-01/03/04/07; and the priority order of the next coherence-by-memory failure classes). **(2)**
> the §13(d) operator-context beat **narrows to "anything changed since the supplement was
> written?"** — it does **NOT** "fire full." Every "cold / empty ANSWERS / beat fires full" phrasing
> below is **generation-time history**; the folded answers + this banner are the live truth.
>
> **⚠ Operationally load-bearing (from the answers — surfaced, not buried):** the architect's
> **first backlog action** is to **extract the v2-deferred items out of `#172`'s body into their own
> backlog IDs BEFORE `#172` is closed** — else the roadmap orphans on closure. The operator is
> poised to `/review-closures` `#172`; do the extraction first. Also decided in the answers: **name
> the paradigm as an ADR, not a VISION** (a VISION invites the maximalism just resisted); the §7
> review-command canon resolves to a **graduated rule** (interim/small → `/code-review high`; final
> pre-merge, 3+ files → `/codex-review` for the independent lens — confirm Codex auth-mode first).
> Do **not** reparent `#169`/`#166` yet (deferred until ≥2 real drifts); do **not** hand-close `#172`.

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is **clean on doc-claims**: the actionable carry the *prior* bundle flagged
> (`ARCHITECTURE.md` `pytest_collected` 511→534) was **resolved** (now 587/587), `main` is **in
> sync** with origin, and `audit.py health` is **OK**. Two residual loose ends remain — the
> carried-benign `#77` `[~~]` WARN and **two merged handoff stragglers** awaiting `-d` (operator-gated).
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` + the **durable**
> serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at HEAD
> `adf0cbe`, working tree clean, `main` in sync with `origin/main`. Re-derive HEAD/sync at
> read-time (`PROBES.md` P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session** (`/clear`ed);
> the arc it hands off (the supplement-fill dogfood + the coherence-spine v1 integration) was done
> in **prior** sessions, so there is **no live session reasoning** to transmit. State facts (§1, §5)
> are **witnessed** (verified live at generation via the read-only drift-checks); design framing
> (§2–§4) is **recall/inferred** from JOURNAL (the four 2026-06-17 entries + the last ~6), BACKLOG,
> and the two prior bundles — verify against the live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff one arc-boundary past `…-architect` (this is bundle #2 of 2026-06-17).**
> The state moved since the `2026-06-17-dev-knowledge-architect` bundle was generated: (1) that
> bundle's `SUPPLEMENT.md` was **filled** with real architect answers — the **first end-to-end #159
> fill→fold dogfood** — surfacing the operator's strategic reframe ("**file-oriented dependency
> management**"); and (2) the **coherence-spine v1** shipped whole (#172 done-when met; #171 now
> buildable) — *the first concrete v1 of that very reframe*. Orient first (`PROBES.md` P1), **then ask
> the operator for off-repo context** (§13d — **per the UPDATE banner the supplement was FILLED, so this beat NARROWS to "anything changed since the supplement?"**; see §2), then resume the design.
>
> **This bundle is itself a v5.2 cold case.** Like the prior two architect bundles it is cold (fresh
> CC session, no outgoing browser holding *this generation's* deliberation). v5.2 makes that
> **defined, not a gap**: `SUPPLEMENT.md` is generated + committed with **empty ANSWERS** (the
> assembler folds nothing; the incoming §13(d) beat fires full). The *prior* bundle's filled
> supplement + the JOURNAL "Notable" line carry the operator's most recent strategic *why* — read
> them as the planning context (pointer in §2), then the beat asks what changed since.

---

## 1. Drift-flags — the headline (this time: **clean on doc-claims; two loose ends**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90, plus CC's
state read at generation). **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (17/20 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P5/P6/P7).

### STATE — the prior bundle's actionable carry is **RESOLVED**: `pytest_collected` now matches

The `2026-06-17-dev-knowledge-architect` bundle flagged `pytest_collected@ARCHITECTURE.md` as
doc=511 vs live=534 (the headline "fix owed"). During the coherence-spine arc that drift was
**fixed**: `ARCHITECTURE.md` line 274 was bumped to the live count and re-stamped (commits
`79ff7dd` 511→564, then `3fd2621` 564→587). `validate_doc_claims` now reports **all 4 claims match**
— `pytest_collected (doc 587 / actual 587)`, `audit_check_count (20/20)`, `precommit_hook_count
(9/9)`, roster matches. **No actionable doc-claim drift this handoff.** *(Honest enforcement limit
still stands: `audit.py health`'s integrated `doc_claims` gates only 3 of the 4 claims — only the
standalone `validate_doc_claims.py` (probe P6) surfaces `pytest_collected`; so "health: OK" alone is
not proof the count is clean — P6 re-derives it.)* **Confirm:** `python scripts/validate_doc_claims.py`.

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure
  from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **in sync** with origin; **two merged handoff stragglers** await `-d`

`git status -sb` reports `## main...origin/main` (in sync at generation — the coherence-spine arc was
pushed). But `git branch --merged main` now shows **two merged stragglers**:
`docs/handoff-2026-06-17-architect` and `docs/handoff-2026-06-17-supplement-filled` — both merged,
neither `-d`'d. (The only other branch, `automation/fleet-audit`, **never merges to main by design —
ADR-84**, NOT a loose end.) Deleting merged branches is **operator-gated** (no-branch-deletion-without-
asking) — surfaced, not done. **This handoff's own branch** `docs/handoff-2026-06-17-architect-2`
merges on completion and **puts `main` ahead of origin until pushed**. Re-derive at read-time —
`git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The arc this window: the operator's strategic reframe became the first concrete mechanism.** Two
linked things landed since the `…-architect` bundle [witnessed via JOURNAL + audit state]:

- **#159 fill→fold dogfood (the supplement proven live).** The operator relayed **real** architect
  answers into the prior bundle's `SUPPLEMENT.md` and said `supplement filled`; CC committed them
  **verbatim** (advisory/non-fabricated contract) and `assemble_paste.py` folded the **ANSWERS region
  only** (zero QUESTIONS leakage, verified) into that bundle's `PASTE_THIS.md`. This is the **first
  end-to-end exercise** of the v5.1/v5.2 fill→fold path — #159's *fill* half. **Surfaced, not buried —
  the load-bearing output:** the operator reframed the whole methodology as a **"file-oriented
  dependency management"** paradigm (Markdown files = objects, the AI = runtime), the systemic fix for
  the coherence-by-memory failure class. That reframe is now in external research and is the **candidate
  top thread** for the next architect session. **Pointer (not re-narrated here):**
  `docs/handoffs/2026-06-17-dev-knowledge-architect/SUPPLEMENT.md` (the verbatim answers) + the JOURNAL
  2026-06-17 "supplement FILLED" entry "Notable" line.
- **Coherence spine v1 — the first concrete v1 of that reframe (the window's headline ship, #172).**
  Built in three parallel-then-integration prompts: **(A)** a generic deterministic **reconciliation
  checker** (`scripts/validate_reconciliation.py`) reading each dependent's `reconciled_with:
  <spec-id>@<version>` frontmatter edge against the spec's **live** version — registered as the **20th
  `ALL_CHECKS` entry** (`check_reconciled_versions`; mismatch → `Finding(fail)`, malformed → `Finding(warn)`
  fail-open) — plus a **non-blocking forgotten-version-bump nudge** (`scripts/coherence_nudge.py`,
  instrumented to `logs/coherence-nudge.log`); **(B)** a **reconciliation enumerator**
  (`scripts/coherence_enumerator.py`) + the `check-against-spec` skill that, given a stale-edge flag,
  **over-extracts every candidate reference site** by category (sections / walkthrough_steps / diagrams /
  commands / summaries — "never miss") and an LLM verdicts **each** (`stale|fine|not-relevant`); **(C)**
  the **integration** — wired the enumerator to A's real `enumerate_edges()` contract (replacing B's stub),
  deduped the spec-version parser to one, added the **e2e closure gate** (`tests/test_coherence_integration.py`:
  spec 5.2→5.3 + stale walkthrough + un-updated mermaid → real `Finding(fail)` → both missed sites named
  by category), and **locked the `Finding` output format** for #171's dashboard. **#172's "Done when" is
  fully met** → ready for the operator-gated Tier-1 closure loop (`/review-closures`).

**The design tensions now on the table** [recall/inferred]:

- **(A‴) "File-oriented dependency management" — the paradigm is named + has a v1, but is un-elaborated
  as doctrine.** The coherence spine is its *first* mechanism (specs are the "definition", dependents
  declare a `reconciled_with` edge, a deterministic check + LLM enumerator catch version-lag drift). The
  open architecture work is whether/how to elaborate this into a named governing model (an ADR? a
  VISION/ARCHITECTURE thread?) and which *other* coherence-by-memory failure classes it should next
  cover. This is the candidate top thread (§3 Q-A‴).
- **(B) The deterministic-vs-judgment split is now a shipped invariant — guard it.** The spine's R2
  framing (operator ruling): the **deterministic** guarantee is *version-lag-detected + every candidate
  site enumerated*; the **staleness verdict is the LLM/human advisory gate** (`check-against-spec`),
  never claimed by the test. Coherence v2 must preserve that line (don't let the enumerator's output
  harden into an auto-edit). See §3 Q-A‴(v2).
- **(C) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** The
  structural split → thin `§N`-index + per-section modules is justified on **maintainability** (≈84k
  tokens, ~3.5× the read-cap, frequently edited), **not** parallelism. Council-bound: the §1–§19 spine
  is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-C.

### Where the coherence spine leaves v2 (the firing-rate-gated triggers, surfaced)

v1 deliberately stopped at *surface + advise*; v2 is **data-gated**, not scheduled [witnessed via JOURNAL]:

- **The nudge's escape-hatch / deferred-hash / promote-to-gate decision is gated on real firing data.**
  Every forgotten-version-bump fire appends to `logs/coherence-nudge.log`; **v2 fires when that log
  accumulates signal** (a too-noisy nudge → escape hatch or content-hash; a reliably-correct nudge →
  promote to a gate). Do not pre-decide it — read the log first.
- **#171 dashboard is now buildable** against the locked `Finding` format (the integration's deliverable).
- **A surfaced R3 reconcile (do not lose):** the JOURNAL flagged that **PLAYBOOK §7 (~line 1620) names
  `/codex-review` as the canonical pre-merge gate, but this feature's actual practice used `/code-review
  high`.** A `/review` vs `/codex review`-class doc-vs-practice drift — **surfaced for reconcile**, not
  silently resolved. (Also pre-existing, flagged-not-fixed in the enumerator JOURNAL: `CLAUDE.md` §8 still
  says "No repo-level skills directory exists yet" while `.claude/skills/verify/` + `.claude/skills/check-against-spec/`
  now exist — a doc-claim the coherence spine itself could eventually cover.)

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A‴ — elaborate "file-oriented dependency management" + run coherence v2 (the top candidate thread).**
  v1 shipped the *first* mechanism (#172). Open: (i) **whether to elaborate the paradigm as named
  doctrine** (the operator's reframe — Markdown = objects, AI = runtime — currently lives only in a
  filled SUPPLEMENT + external research, not in VISION/ARCHITECTURE/an ADR); (ii) **coherence v2**, which
  is *firing-rate-gated* on `logs/coherence-nudge.log` (escape-hatch / deferred-hash / promote-nudge-to-
  gate) — read the log before deciding; (iii) **which next coherence edges** to declare beyond the v1
  single edge (`docs/handoffs/README.md` → `handoff-process@5.2`).
- **Q-A″ — finish the v5 generator (#164) + the *incoming*-beat half of #159.** #159's **fill→fold** half
  is now **exercised** (this window); its only-remaining clause is the **incoming §13(d) beat** — run when
  the *next* architect session boots on a `PASTE_THIS` (this bundle's beat fires full — cold). **#164**
  still carries the v4 8-file generator in `.claude/commands/handoff.md` (marked SUPERSEDED); the v5
  emissions are specified but not the wired generator (must emit the v5.2 always-file `SUPPLEMENT.md`).
- **Q-C — PLAYBOOK Move 2 (Council-bound, unchanged).** Structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the
  consumer API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 / #146**
  (the playbook serialize-group).
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — note **this bundle is again a hand-assembled probe set** (the
  persisting capture point; serialize-group `handoff`).
- **Q-F — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check flagging
  any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed (live
  enforcement ahead of its doctrine — ADR-82 still reads "Proposed" in-header vs operator-ratified is a
  live instance). Serializes within the `audit-py` group.
- **Q-G — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — two real edges were
  dropped (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also **anchor the parser
  to clause position** so prose tokens can't self-trip it.
- **Q-H — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the v5 runbook chose mermaid), awaiting ratification — not a unilaterally
  minted ADR. Record where the diagram convention lives once ratified. `serialize-group: architecture`.
- **Q-J — #170 → #168, the traceability spine.** Design + land the traceability-spine ADR (issue-ID↔commit
  anchor) — the airtight, **always-warranted** link that promotes ADR-85's BACKLOG leg from advisory to a
  **hard** gate (#168 depends-on #170). *Note the overlap with Q-A‴:* the coherence spine's `reconciled_with`
  edge model is a sibling pattern (a frontmatter-declared dependency edge); whether the traceability spine
  reuses it is an open design connection.
- **Q-K — #171 → #169, the conformance dashboard.** Build `ecosystem/conformance.md` (ADR-86 / ADR-85 R2)
  — a read-only validator generates **and commits its own output** (ADR-80 committed-generated-zone writer
  policy). **Now unblocked** by the coherence integration's locked `Finding` format — the dashboard can
  consume `Finding`s directly. ARCHITECTURE Ch2 will point to it.
- **Q-L — ADR-85 standing governance obligation (a watch, not a design question).** The gate is **live**.
  A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% →
  tune the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.

**Resolved-since the `…-architect` bundle (do NOT re-open):** the `pytest_collected` actionable carry
(→ bumped 511→587 + re-stamped) · the #159 *fill→fold* half (→ exercised live) · the coherence-spine v1
*design* (→ #172 shipped; only v2's firing-rate-gated decisions remain) · the v5.1 cold-handoff supplement
gap (→ HANDOFF_PROCESS v5.2, prior window).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize**
  (do not co-schedule). The **audit-py** group = `{#153, #7, #36, #95, #140, #139, #166, #172}` (**#172
  added** this window — the coherence-spine story). The **playbook** group = `{#146, #77, #67, #18, #39}`.
  The **architecture** group = `{#165, #35}`. (Plus `claude-md {#112,#157}`, `claude-md-template`,
  `environment`, `pre-commit-config`, `settings-json` — see the validator's full summary line.) Hard
  precedence edges (`depends-on`): **#168 → #170**, **#169 → #171**. Parallel-safety is **derived** (no
  shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A‴ (coherence v2 / paradigm doctrine) is the top candidate thread** — but v2's sub-decisions are
    *firing-rate-gated* on `logs/coherence-nudge.log`; not schedulable until the log has signal.
  - **#171 (Q-K) is now unblocked** — the integration locked the `Finding` format the dashboard consumes;
    it still **depends-on #171's parent** in the `#169→#171` chain only as encoded.
  - **#164 (Q-A″) is the last big handoff-machinery item** — serializes within the `handoff` group; now
    must also emit the v5.2 always-file `SUPPLEMENT.md`.
  - **#170 (Q-J) unblocks #168**; the coherence `reconciled_with` edge is a *sibling* of the traceability
    edge — a possible reuse, surfaced as a design connection, not a schema fact.
  - **Move 2 (Q-C) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "candidate-thread / unblocks / sibling" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes — the coherence work lives under the audit/governance
  themes (#172 in the `audit-py` group; #171/#169 conformance dashboard; #166/#167 cleanups), the handoff
  group (#159/#161/#162/#164), and the playbook group (Move 2 / #39). Do **not** trust any re-narrated ID
  text — open the live BACKLOG (the §3 text is recall; the file is truth). `validate_backlog`: **76 tasks,
  0 warnings, 7 themes, 20 stories, 9 serialize-groups** at generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end); **two merged stragglers** — `docs/handoff-2026-06-17-architect`,
  `docs/handoff-2026-06-17-supplement-filled` (await operator `-d`, §1). This handoff's own branch
  `docs/handoff-2026-06-17-architect-2` merges on completion.
- **Drift-flags:** doc-claims **clean** (the prior `pytest_collected` carry resolved — §1) + the
  carried-benign `git_backlog_drift` #90a `[~~]` (#77). `main` in sync at generation; two merged
  stragglers to `-d`. Re-derive: `python scripts/audit.py health` + `python scripts/validate_doc_claims.py`
  + `git status -sb` + `git branch --merged main`.
- **Audit-gating note (load-bearing):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** v5 bundle. `2026-06-17-dev-knowledge-architect-2` is now lexically-max → it **is** this
  check's target (superseding `…-architect`). Its 10 probes were verified to bind via
  `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-17-dev-knowledge-architect-2`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **21 closure proposals** await — `/review-closures` (human-gated, done-items-leave). **#172 is the
  ready one** (its "Done when" is met — close it here).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **two merged handoff stragglers** — `docs/handoff-2026-06-17-architect`,
  `docs/handoff-2026-06-17-supplement-filled` — `-d` is the operator's call (§1).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — supplement FILLED.** This bundle was generated cold, but the
> operator then `supplement filled` real answers (see `RESIDUAL.md` UPDATE banner). The teeth probes
> (P2–P9) are **unchanged** — they bind to **live state**, which the fill does not touch. The only
> change is the **§13(d) beat in P1's gate: it now NARROWS to "anything changed since the
> supplement?"**, it does **not** fire full (the supplement carried answers). Read any "ANSWERS empty
> / beat fires full" phrasing below as generation-time history.

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and records
> PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN
> `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted
> `#id`, the serialize-group membership, the counts, the dates — are deliberately **absent from
> this whole bundle**. That is what gives the probes teeth. Do not infer them; run the command.

## P1 — Orientation (the architect's **first move**, before any mechanism — v5 §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a
copy of VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line
read**: the line enters the session **only** by CC reading the **live** primary source, and the
quote must match as a **substring** (never a paraphrase). The browser has no files → it replies
**"run `<command>`"**; CC reads live and substring-checks.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` (line 11) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` (line 47) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read
live by CC, substring-matched. **Then, before design, the operator-context beat fires (v5 §13d):**
the browser asks the operator one targeted question for **off-repo** context (intent / priorities /
findings not in the repo / changed decisions). **This bundle's `SUPPLEMENT.md` was FILLED
post-generation (UPDATE banner / `RESIDUAL.md`), so the beat NARROWS to "anything changed since the
supplement was written?"** — its answers already carried the off-repo context (Q6 + the addenda); do
not re-ask it whole. The folded answers are the authoritative strategic *why* — read them first.
*(Generation-time history: the bundle was generated cold with empty ANSWERS, when the beat would have
fired full.)*

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both — and one **landed this window** (the coherence-spine reconciliation gate), so a stale summary undercounts | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `adf0cbe`, the tree was clean, and `main` was in sync — but this handoff's own commits put `main` ahead until pushed, and HEAD/sync move on any commit, push, or fetch; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely (ARCHITECTURE was re-stamped this window for the count + check-count bumps) | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual — and unlike the prior bundle (which carried a doc=511 vs live=534 **mismatch**, now **resolved**), this probe is **expected to MATCH** at generation, but the live count is still the only ground truth | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** catch this; use the standalone |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + the v5.2 **always-generated** `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-17-dev-knowledge-architect-2/` (no `README.md`; `SUPPLEMENT.md` present, **ANSWERS FILLED** post-generation — see the UPDATE banner; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, and which `#id`s are in the **handoff** group (and which group did the coherence-spine story `#172` join)? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit (the `audit-py` group gained `#172` this window); it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, **NARROWED**
   to "anything changed since the supplement?" this bundle (the supplement was FILLED — UPDATE banner;
   read the folded answers first) — before design. Then run P2–P9, each against **live state now**
   (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P2/P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P6 is expected to MATCH at generation** (the prior bundle's 511 vs 534 carry was
   resolved) — but the pass criterion is **"answered from the live source,"** never "matches the value
   the summary remembered." P2 is expected to read **20** (a check landed this window); P8 pins the
   post-collapse four-file shape (+ the v5.2 always-generated `SUPPLEMENT.md`, no README); P9 pins the
   now-durable serialize-group graph (#156) with `#172` newly in the `audit-py` group.

---

=== SUPPLEMENT.md ===

Orientation for the incoming architect. This session took a 107-candidate brainstorm on dependency coherence and shipped one proven thing: coherence spine v1 (#172) — a narrow, complete, end-to-end slice on a single edge (dependent README ← spec HANDOFF_PROCESS, version-coupling). It is a proof-of-concept for a doctrine, not just a feature. Read these answers as a map of what was decided and why, so you extend a proven primitive deliberately rather than rebuild or relitigate it.
1. Strategic intent (way-of-working level).

Two goals, both methodology, neither a task. First: decide whether coherence-by-mechanism instead of coherence-by-memory becomes named doctrine (see A), and establish a cadence for adding mechanisms without sliding into maximalism. Second, harder: make the backlog genuinely load-bearing. This session shipped v1 to main three times before the backlog story even existed — the advisory gate nudged but never stopped us. You are the architect who drives from the backlog and delegates; freewheeling ("wolna amerykanka") is the anti-pattern to kill. Operate that for real, not nominally.
2. Tensions weighed + where we landed.

Maximalism vs narrow slice — 107 candidates, four visions. Landed narrow (one edge, the minimal Spine), deferred the rest. Reason: solo-dev constraint — the methodology must not outgrow the work; prove the mechanism before scaling.
The crux flip — I first believed the trigger (version-vs-hash) was the crux. The Council plus first-principles flipped it: the enumerator is load-bearing. The partial-update miss (walkthrough + diagram left stale) happens after the trigger fires — it is a completeness problem caught only by enumerating every reference site, not a detection problem. Do not re-elevate the trigger.
Version-coupling vs content-hash (DEC-01) — landed version-coupling (fires only on deliberate change, no over-firing on prose) plus a pre-commit nudge as a cheap forgotten-bump floor. Deferred the full content-hash floor until nudge data justifies it.
Deterministic vs AI — deterministic trigger + deterministic site-extraction + AI per-site verdict + human signature. The AI advises inside the gate; it never waives it.
Closure — the e2e mutation test (real injected drift → real checker fails → enumerator names the missed sites) is closure. Not green tests.
Review independence vs usage limits — leaned toward an independent lens at the pre-merge gate (codex caught 2 HIGH this session). See B.

3. Considered + rejected (do not relitigate).

The §16 do-not-build list stands: graph-DB for the methodology (killed empirically — grep was cheaper), a second task tool (two sources of truth), enterprise cross-tool ingestion (a solo dev is the curator), transclusion-everywhere (literate spaghetti), self-healing without human approval (ungrounded LLM drifts further), predictive-drift ML (no data advantage at solo scale), adopting any substrate platform / the Reactive Kernel (VISION-1) as a build target — study and borrow, do not migrate.
Dumping the raw brainstorm inventory into the repo — rejected. The architect distills it into an ADR; the brainstorm doc is off-repo input, not a repo artifact.
"The trigger is the crux" — rejected; the enumerator is load-bearing.
Forcing one regex for the deduped version parser — rejected; pin both behaviours, unify at the consumer layer, layer A's numeric validation, never bend a test.
Hand-closing #172 / freewheeling the backlog — rejected; the operator-gated closure loop owns it.

4. Open questions (unresolved / deferred).

The doctrine question (A) — name it or keep it implicit. Your first decision.
DEC-04 — lead with removal (transclusion/generation) or detection (gate)? We built detection first as the backstop; the split is unresolved.
DEC-03 — file-level vs element-level granularity; the stakes threshold for element-level is undecided.
DEC-07 — folder-level dependency contracts (_index.md); lean was rollup-over-files, folder-as-unit for high-stakes only.
Coherence v2 escape-hatch / deferred-hash / promote-nudge-to-gate — firing-rate-gated on logs/coherence-nudge.log; deliberately deferred until data (B).
§7 review-command canon + Codex auth mode — unresolved; lean given (B).
Which coherence-by-memory failure classes the spine covers next, and in what order (A).
#168 (backlog advisory → hard) — justified, depends on #170; sequencing open.

5. Decomposition rationale + what NOT to redo.

Shape: one organizing story (#172 = the spine), v1 as three sub-arcs (A checker / B enumerator / Integration), v2 as a deferred list. Reason: the spine is a general mechanism that several existing point-checks are instances of — #169 (canonical-doc staleness) reparents under it, #166 (task→ADR) reparents, #171 (dashboard) is its shared output surface, #170 (traceability) is a sibling. A and B were split for parallel build behind a clean Edge contract; Integration wired them. v1 narrow proves the mechanism; v2 scales, each item trigger-gated.

Do not redo or re-decide: the spine core (shipped and proven — build on it), DEC-01 for v1, the enumerator-is-load-bearing call, the deterministic/AI/human boundary, the §16 list. Do not reparent #169/#166 yet — deferred until ≥2 real drifts plus a #169-fit decision (a deliberate evidence-gate, not an oversight). Do not hand-close #172.

Critical hygiene, your first backlog action: the v2-deferred list currently lives inside #172's body. Extract those items into their own backlog IDs before closing #172, or the roadmap orphans on closure. (And reconcile this whole map against the live backlog — I can't see it from the browser.)
6. Off-repo context.

The brainstorm inventory (the 107 candidates, the full design-pattern catalogue, the do-not-build reasoning, the open decisions) is off-repo. The architect carries it by re-upload. Your first build task: distil it into an ADR and extract the active v2 items. It is also the record of what we chose not to build.
Codex pricing (researched here): Codex CLI is included in a paid ChatGPT plan if authed via ChatGPT sign-in (no extra money, draws plan limits); API-key mode bills per token (extra money). /code-review runs on Claude / your Max plan (no extra money). Confirm the auth mode before settling the review rule.
The methodology's own backlog discipline failed three times this session (shipped untracked → recovered via retroactive #172). That is the live case for #168 and the reason the architect wants the backlog genuinely load-bearing. The recurring spec↔practice drift in our own docs (§7, the pytest_collected count) is the same shape — the problem we are solving keeps appearing in our own process. Validating, not embarrassing.
Operating intent throughout: narrow-first, deliberate extension, the architect selects and decides — not dump, not maximise.

A. "File-oriented dependency management" as doctrine + next failure classes.

Name it — as an ADR, not a VISION. It is proven in miniature, and a proven mechanism earns a decision-record; a name gives the next mechanisms a coherent frame so v2 reads as "extending the paradigm" rather than ad-hoc feature-adding. Keep it an ADR (decision + principles + the v1 proof + the distilled roadmap), not a sprawling VISION — a VISION invites exactly the maximalism we just resisted. Bound it in the ADR: the doctrine is coherence-by-mechanism; deterministic trigger + AI judgment + human signature; graph-in-repo-not-model; narrow-first — and the do-not-build list is part of the doctrine, not separate from it.

Next failure classes, priority order (beyond the single reconciled_with edge):

More spec→dependent edges of the same type (other docs describing other specs) — just more declarations, proven mechanism, immediate value; includes scaling — generate the graph from frontmatter (SPINE-08), cross-repo (SPINE-09 / confirm #164 covers this).
Resolve DEC-04 and, for the highest-duplication content, remove the drift surface (transclusion) rather than detect it — the field's strongest claim; a bigger commitment, so gate it on the DEC-04 decision.
The forgotten / mis-classified bump (the false-negative the version edge can't see) — currently the nudge; promote to a content-hash floor if nudge data shows real misses.
Undeclared edges — dependencies that live in prose but aren't declared; AGENT-11 infers candidates for human confirmation.
Intra-file frontmatter↔prose drift (DET-16) and a whole-graph contradiction sweep (DET-11) — periodic, non-blocking.

You set the exact order; this is the shape.

B. Coherence v2 trigger lean + §7 reconcile.

v2 escape-hatch / deferred-hash / promote-nudge-to-gate: no off-repo intent should pre-empt the data — instrumenting the nudge is the decision mechanism. Hold it; do not let the next session build it speculatively. If forced to lean: promote-nudge-to-gate is the natural escalation if the nudge fires accurately and rarely; the escape-hatch and deferred-hash are the answer only if it proves noisy. Decide from logs/coherence-nudge.log.

§7 reconcile: this is not a cost decision — both are included if Codex is ChatGPT-authed. Lean: interim / small reviews → /code-review high (you're already in Claude); final pre-merge gate (3+ files) → /codex-review (independent GPT lens — it earned its place this session). Encode that graduated rule in §7, not a single command. Confirm Codex auth mode first; if it's API-key, codex costs extra → flip toward /code-review or switch the auth. And note the meta-point worth carrying: §7-vs-practice drift is itself a coherence instance — reconciling it is the doctrine in action.
