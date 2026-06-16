=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-16-dev-knowledge-architect` |
| **Mode** | **architect** (v5.1 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff at an arc boundary. The 2026-06-15 headline design thread — **(A) the hybrid handoff** ("v5 has no formal slot for browser-authored judgment") — **substantially landed as HANDOFF_PROCESS v5.1** (the architect strategic supplement: the architect's *why* becomes a first-class advisory supplement via a structured 6-question interview). A **new** governance theme also shipped its v1: **ADR-85 session-lifecycle enforcement** (a deterministic, no-LLM Stop-gate — hard JOURNAL leg + advisory BACKLOG leg + HEAD-bound `/override`) plus the **Stop-hook loop fix** (#142). The consolidation pass filed **#170** (traceability-spine ADR → unblocks #168) and **#171** (conformance dashboard → unblocks #169), + **ADR-86**. The next session inherits: **dogfood the v5.1 supplement + §13(d) beat** (#159 — this handoff is the first to reach the supplement step), **finish #164** (the v5 generator, now also wiring the supplement emission), the two NEW build chains (#170→#168, #171→#169), and the standing Council-bound threads (**PLAYBOOK Move 2**, #162 vocab, #161 probe-core, #165 diagram rule). |
| **Generated at** | HEAD `0752efa`, working tree clean, `main` **ahead 9** of `origin/main` (unpushed — a change from the 2026-06-15 in-sync state; the ADR-85/v5.1/Stop-hook arc landed locally, not pushed). This handoff's own commits increment the ahead-count. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

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
  Architect mode only. (v5.1: when CC's paste carries the strategic **supplement**, its Q6 already
  captured this off-repo context at handoff time — narrow the ask to *"anything changed since the
  supplement was written?"* rather than re-asking it whole; `HANDOFF_PROCESS.md` §13(d), "(d)
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

# Residual — 2026-06-16 session, **architect mode** (v5.1 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — and this time the
> headline is **NOT clean** (§1: an actionable ARCHITECTURE count drift + the unpushed `main`).
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the **durable**
> serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at HEAD
> `0752efa`, working tree clean, `main` **ahead 9** of `origin/main` (unpushed). Re-derive HEAD/sync
> at read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This session was `/clear`ed immediately before
> the handoff, so there is **no live session reasoning** to transmit. The planning "why" below is
> **reconstructed from the repo** — JOURNAL (last ~7 entries), BACKLOG, and the 2026-06-15
> `-architect` bundle. State facts (§1, §5) are **witnessed** (verified live at generation); design
> framing (§2–§4) is **recall/inferred** from those sources — verify against the live BACKLOG (§5),
> do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary.** The state moved **decisively** since 2026-06-15:
> the 2026-06-15 bundle's headline design thread — **(A) the hybrid handoff** ("v5 has no formal slot
> for browser-authored judgment") — **substantially landed as HANDOFF_PROCESS v5.1** (the architect
> strategic supplement). A **new** governance theme also shipped its v1: **ADR-85 session-lifecycle
> enforcement** + the Stop-hook loop fix. Orient first (`PROBES.md` P1), **then ask the operator for
> off-repo context** (§13d / #159), then resume the design.
>
> **First v5.1 supplement dogfood — read §2 "The supplement-interview finding".** This is the **first
> architect handoff to emit the v5.1 supplement interview block**. The honest empirical finding is
> already in hand (a cold/`/clear`ed handoff has no *outgoing* browser to interview) — that is exactly
> the #159 dogfood signal, surfaced not buried.

---

## 1. Drift-flags — the headline (this time: **NOT clean**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (16/19 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P6/P7).

### DRIFT — actionable: `ARCHITECTURE.md` **`pytest_collected` is stale** *(the headline — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` **doc=511, actual=530** — the
recent ADR-85 (+ Stop-hook +26 backpressure tests), v5.1 (+3 `assemble_paste` tests) and prior test
additions moved the live collected count past ARCHITECTURE's claim. **Honest enforcement limit:**
`audit.py health`'s integrated `doc_claims` check reports `[OK] 3 self-claims match` and **does NOT
catch this** — it gates only 3 of the 4 claims; **only the standalone `validate_doc_claims.py` (which
probe P6 binds to) surfaces it.** So `health: OK` is *not* sufficient evidence the doc-claims are
clean here.

- **Fix path (next-session work, not this handoff):** bump ARCHITECTURE's `**N collected**` claim to
  the live `pytest --collect-only` count, then **genuinely re-read + re-stamp `last_reviewed`**
  (ARCHITECTURE is a canonical living doc — `canonical_freshness` will FAIL the *next* commit if the
  count edit lands without a re-stamp; the JOURNAL 2026-06-16 "operational gotcha" documents this
  exact sequencing trap). Left as a flagged drift, not silently patched mid-handoff.
- **Confirm:** `python scripts/validate_doc_claims.py` (the `pytest_collected` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure
  from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **ahead 9** of `origin/main` (unpushed) + **six merged stragglers** *(operator-gated)*

A change from 2026-06-15 (which was in sync after that day's push). The ADR-85 lifecycle-gate arc,
the v5.1 verification pass, and the Stop-hook loop fix all landed locally and were **not pushed** —
`git status -sb` reports `## main...origin/main [ahead 9]`. Six merged-but-undeleted feature branches
remain (`docs/handoff-v5.1-architect-supplement`, `docs/handoff-v5.1-boot-beatd-refinement`,
`docs/journal-v5.1-verification`, `feat/adr-85-lifecycle-gate`, `fix/stop-hook-active-is-present`,
`fix/stop-hook-no-autobypass`). Plus `automation/fleet-audit` (**never merges to main by design —
ADR-84**, NOT a loose end). Push + `-d` cleanup are **operator-gated** (no push / no branch deletion
without operator OK). This handoff's own commits will increment the ahead-count further.

- **Confirm:** `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The 2026-06-15 headline thread landed; the work re-centred on enforcement + the un-dogfooded
supplement.** The 2026-06-15 architect bundle named **two** Council-bound threads — **(A) the hybrid
handoff** and **(B) PLAYBOOK Move 2**. Since then [witnessed via JOURNAL + audit state]:

- **(A) the hybrid handoff → SHIPPED as HANDOFF_PROCESS v5.1.** The 2026-06-15 Q-A asked for a
  *formal slot for committed, browser-authored judgment* (v5's residual is by spec CC-authored /
  repo-derived and "structurally cannot carry operator intent"). **v5.1 is that slot:** the architect's
  strategic *why* (intent · tensions · options rejected · open Qs · decomposition rationale · off-repo
  context) is now a **first-class advisory supplement produced by a structured 6-question interview**
  — CC emits a paste-ready block, the operator relays it to the **outgoing** browser, the browser's
  answers become `<bundle>/SUPPLEMENT.md` **verbatim** (no re-typing), folded into the next session's
  `PASTE_THIS` by `assemble_paste.py`. Hard scope-constraint: the interview asks **only**
  non-re-derivable *why* — never repo state / counts / SHAs (those stay forced-read, §3/§5);
  advisory, never teeth; a per-session transient (not a v4-disease maintained surface). ADR-82
  amended 2026-06-16. **Residual clauses: #159 (dogfood — this session) + #164 (the generator must
  wire the emission + the verbatim SUPPLEMENT.md write).**
- **NEW theme — ADR-85 session-lifecycle enforcement v1 shipped.** The executor (not the human) is now
  the session-close trigger via a deterministic, **no-LLM** Stop-gate: a **hard** `decision:block`
  JOURNAL leg (the arc's `JOURNAL.md` additions must name ≥1 `base..HEAD` commit-SHA — un-gameable,
  supersedes the old soft journal-presence check), an **advisory** BACKLOG-marker leg (R1: nudge not
  block in v1), and a pure-read HEAD-bound `/override` token (logged to gitignored `logs/OVERRIDES.md`,
  no auto-bypass). Canon: `protocols/DEFINITION_OF_DONE.md`. **Then the loop-defect fix** (#142): the
  Stop hook **can never loop to the block-cap** — a structural floor (standalone advisory never keeps
  the turn going; it rides only folded inside a hard block) + a freshness same-day exemption + a
  fire-once guard (`stop_hook_active`, witnessed **ACTIVE** at this runtime's wrap, with the floor as
  backstop). The gate is **fail-closed on real non-compliance, fail-open on its own errors**.
- **Consolidation pass under the new DoD** → filed **#170** (traceability-spine ADR — the issue-ID↔commit
  anchor) and **#171** (conformance dashboard at `ecosystem/conformance.md`), plus **ADR-86**
  (dashboard-location decision). These are the new build edges (§3 Q-J / Q-K).

**The two design tensions now on the table** [recall/inferred]:

- **(A′) The hybrid handoff is shipped but UN-DOGFOODED — value is unproven.** v5.1 answered Q-A's
  *design* question, but the supplement interview has **never been exercised end-to-end** (operator
  relays → outgoing browser authors → CC writes `SUPPLEMENT.md` verbatim → folds into the next
  `PASTE_THIS`). Until one real run, the claim "judgment transmits via the supplement" is a spec
  assertion, not an empirical fact. **This session is the first dogfood** — see the finding below.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** Move 1
  barely shrank the file; Move 2 (the structural split → thin `§N`-index + per-section modules) is
  justified on **maintainability** (≈84k tokens, ~3.5× the read-cap, frequently edited), **not**
  parallelism. Council-bound because the `§N`-index design is a genuine fork — the §1–§19 spine is the
  **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-B.

### The supplement-interview finding (first v5.1 dogfood — the #159 signal, surfaced)

This is the **first architect handoff to reach the v5.1 supplement step**, and a cold-handoff design
gap surfaced immediately [witnessed this session]:

- The v5.1 flow targets the **OUTGOING** architect-browser — "*still in context at session end, the
  only actor holding this session's strategic deliberation*." **This handoff was generated after a
  `/clear`** — there is **no outgoing browser in context**, and the residual itself is reconstructed,
  not witnessed-live. So there is no live deliberation for the interview to extract here.
- **Honest disposition (not a fabricated supplement):** CC still emits the paste-ready interview block
  (architect-mode deliverable). The operator routes it to whoever holds the strategic context — a
  still-open prior architect-browser, or the operator answering as the strategic holder — **or skips
  it**, in which case the **incoming** architect's §13(d) operator-context beat (the inbound twin of
  Q6) captures the off-repo context fresh at session start. `assemble_paste.py` will `[warn]`
  `SUPPLEMENT.md` absent — **expected and correct** (no supplement was authored because no outgoing
  browser was in context); CC must **not** synthesize one (that would re-create the v4 disease and
  violate the advisory/non-fabricated contract).
- **The design question for the next architect session (feeds #159/#164):** does the v5.1 flow need a
  defined behaviour for the **cold/`/clear`ed handoff** case — e.g. explicitly fold the supplement into
  the incoming §13(d) beat, or mark it N/A — so "expected in architect mode" doesn't read as a missing
  deliverable when there is structurally no one to interview?

**The standing meta-argument (persists, now sharper):** every v5 bundle — **including this one** — is
**hand-assembled** by CC following the spec, and this is now **also** the first hand-assembly of the
v5.1 supplement-interview emission. That growing hand-maintained surface is the live case for **#164
(the generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A′ — dogfood + finish the hybrid handoff (#159 + #164).** v5.1 shipped the *design*; the open
  work is (i) **exercise the supplement interview + the §13(d) beat in a real architect session**
  (#159's only-remaining clause — **this session is the candidate**), and (ii) resolve the
  cold-handoff behaviour above. Then #164 wires the emission durably.
- **Q-B — PLAYBOOK Move 2 (Council-bound, unchanged).** The structural split → thin `§N`-index +
  per-section modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N
  addressability — the consumer API). Maintainability-justified, not urgent. **Unblocks #39;
  decouples #18 / #67 / #77 / #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item, L).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?); (ii)
  the **cross-repo v4 routing** (ADR-83) — a v4 target repo (lacking `scripts/audit.py`) needs a
  deterministic route to the v4 Phase-1/2 path; (iii) **architect-mode supplement emission** — the
  generator must emit the §13 interview block from `templates/handoff/v5/SUPPLEMENT.md.tmpl` and write
  the browser's answers to `<bundle>/SUPPLEMENT.md` (the v5.1 addition); (iv) a `PASTE_THIS.md`
  **freshness gate vs its sources** (audit F4 — today the assembled snapshot can silently drift).
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — but note **this bundle is again a hand-assembled probe
  set** (the persisting capture point).
- **Q-F — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check
  flagging any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed
  (live enforcement ahead of its doctrine — the #156 gap reconciled by hand on 2026-06-14; ADR-82 still
  reads "Proposed" in-header vs operator-ratified is a live instance).
- **Q-G — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — the 2026-06-14 pass
  dropped two real edges (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also
  **anchor the parser to clause position** so prose tokens can't self-trip it (the 2026-06-14 incident).
- **Q-H — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the v5 runbook chose mermaid), awaiting ratification — not a
  unilaterally minted ADR. Record where the diagram convention lives once ratified.
  `serialize-group: architecture`.
- **Q-J — #170 → #168, the traceability spine (NEW this window).** Design + land the traceability-spine
  ADR (issue-ID↔commit anchor) — the airtight, **always-warranted** link that promotes ADR-85's
  BACKLOG leg from advisory to a **hard** gate (#168 depends-on #170). The spine is the un-gameable
  AND always-warranted anchor the interim structural-marker check lacks.
- **Q-K — #171 → #169, the conformance dashboard (NEW this window).** Build `ecosystem/conformance.md`
  (ADR-86 / ADR-85 R2) — a read-only validator generates **and commits its own output** (ADR-80
  committed-generated-zone writer policy). It is the deterministic surface #169's ungated-doc staleness
  signal (ARCHITECTURE/VISION/LESSONS/CONTRIBUTING untouched >N sessions while code changed) lands in,
  and ARCHITECTURE Ch2 will point to it.
- **Q-L — ADR-85 standing governance obligation (not a design question — a watch).** The gate is **live
  this session**. A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for
  override-rate (**>~10% → tune the rules**). Surfaced so the next session doesn't re-open ADR-85's
  shape mid-freeze.

**Resolved-since 2026-06-15 (do NOT re-open):** the hybrid-handoff *design* (Q-A → HANDOFF_PROCESS
v5.1; only #159 dogfood + #164 wiring remain) · the Stop-hook loop defect (#142 — closed by the
structural-floor fix) · ADR-85 v1 itself (shipped; only the R1/R2 hardenings #168/#169 remain as
Q-J/Q-K).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**.
  The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize** (do not
  co-schedule). The **playbook** group = `{#146, #77, #67, #18, #39}`. The **audit-py** group =
  `{#153, #7, #36, #95, #140, #139, #166}`. Hard precedence edges (`depends-on`): **#168 → #170**,
  **#169 → #171**. Parallel-safety is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A′ (#159 dogfood) is exercisable THIS session** — off the build path; the supplement-interview
    finding above is its first signal.
  - **#164 (Q-C) is the last big build item** — `L`, gated on the Q-C(i)–(iv) decisions; pairs with the
    already-shipped #163 validator + the new v5.1 supplement emission.
  - **#170 (Q-J) unblocks #168**; **#171 (Q-K) unblocks #169** — two independent NEW build chains from
    the ADR-85 consolidation; parallel to each other and to the handoff group.
  - **Move 2 (Q-B) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "decision-not-build / unblocks / parallel" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes **"Handoff continuity"** (the handoff group),
  **"Enforced governance"** (#168/#170, #166, #167), and **"Canonical-file integrity"** (#169/#171) for
  the live tickets. Do **not** trust any re-narrated ID text — open the live BACKLOG (the §3 text is
  recall; the file is truth). `validate_backlog`: **75 tasks, 0 warnings, 9 serialize-groups** at
  generation (7 themes, 19 stories).
- **Live branches at generation** (`git branch -v`): `main` (**ahead 9** of origin, unpushed);
  `automation/fleet-audit` (**never merges to main by design — ADR-84**, NOT a loose end); and **six
  merged stragglers** (the §1 STATE list) — candidates for `-d` cleanup, **operator-gated**, carried
  not deleted here. This handoff's own branch `docs/handoff-2026-06-16-architect` merges on completion.
- **Drift-flags:** the **actionable** `pytest_collected` 511→530 (§1, fix owed) + the carried-benign
  `git_backlog_drift` #90a `[~~]` (#77). `main` **ahead 9** (unpushed). Re-derive: `python
  scripts/audit.py health` + `python scripts/validate_doc_claims.py` + `git status -sb`.
- **Audit-gating note:** `audit.py` check #19 `handoff_probes` validates the **lexically-max** v5
  bundle. `2026-06-16-dev-knowledge-architect` is the only 2026-06-16 bundle → it **is** this check's
  target now (unlike 2026-06-15, where `-session` > `-architect` shadowed the architect bundle). Its
  probes were verified to bind via `python scripts/verify_handoff_probes.py
  docs/handoffs/2026-06-16-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **20 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` is ahead 9 of origin (unpushed)** + six merged stragglers — push + `-d` cleanup are the
  operator's call (the serial-push gate).
- **ARCHITECTURE `pytest_collected` drift** (§1) — bump 511→live count + genuine re-read/re-stamp.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and records
> PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN
> `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted
> `#id`, the serialize-group membership, the dates — are deliberately **absent from this whole
> bundle**. That is what gives the probes teeth. Do not infer them; run the command.

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
findings not in the repo / changed decisions). **v5.1 narrowing:** if the operator relayed a
strategic **supplement** for this session, its Q6 already captured the off-repo context — narrow the
beat to *"anything changed since the supplement was written?"* (§13(d), "(d) refined, not
duplicated"). Exercising this beat **and** the supplement interview in a real architect session is the
only-remaining clause of **#159** — and this is the first handoff to reach the v5.1 supplement step
(see `RESIDUAL.md` §2 "The supplement-interview finding").

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `0752efa`, the tree was clean, and `main` was `ahead 9` of `origin/main` (unpushed) — plus this handoff's own commits since** — but HEAD/sync move on any commit, push, or fetch; **re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual — **and at generation this probe is EXPECTED TO MISMATCH** (the §1 headline drift: doc=511, live moved past it), so the live answer is the only ground truth | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** catch this; use the standalone |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 handoff bundle** carry, does it include a **per-bundle `README.md`**, and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + optional architect `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-16-dev-knowledge-architect/` (no `README.md`; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, and which `#id`s are in the **handoff** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, narrowed to
   "changed since the supplement?" if a supplement was relayed — before design. Then run P2–P9, each
   against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P6 is expected to MISMATCH at generation** (the headline drift) — the pass criterion is
   **"answered from the live source,"** never "matches the value the summary remembered." P8 pins the
   post-collapse four-file shape (+ optional architect `SUPPLEMENT.md`, no README); P9 pins the
   now-durable serialize-group graph (#156).
