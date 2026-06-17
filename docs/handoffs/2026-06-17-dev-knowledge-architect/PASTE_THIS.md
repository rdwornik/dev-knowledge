=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-17-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one arc-boundary past 2026-06-16. The 2026-06-16 bundle's first-dogfood finding — *a cold/`/clear`ed handoff produced **no** supplement file at all (missing-deliverable look, zero git tracking, operator un-led)* — **landed its fix as HANDOFF_PROCESS v5.2**: the architect strategic supplement is now an **always-generated, committed, self-documenting fillable file** (`SUPPLEMENT.md`), with a **defined cold-handoff disposition** (empty ANSWERS = committed N/A, not a defect) and an **ANSWERS-only, fold-if-non-empty** assembler rule (was: whole-file fold + warn-if-absent). The next session inherits: **the #159 dogfood — fill→fold half now EXERCISED** (this bundle's `SUPPLEMENT.md` was filled with real architect answers post-generation and folded into `PASTE_THIS` — the first real run; only the **incoming** §13(d) beat half remains, run when you boot), **finish #164** (the v5 generator must now emit the always-file form), and the standing threads — **PLAYBOOK Move 2** (#39, Council-bound), **#162** vocab, **#161** probe-core, **#165** diagram rule, the two ADR-85 build chains **#170→#168** / **#171→#169**, and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `ef62dd8`, working tree clean, `main` **in sync** with `origin/main` (a change from the 2026-06-16 `ahead 9` — the v5.2 arc was pushed and the merged stragglers `-d`'d). This handoff's own commits put `main` **ahead** of origin until pushed. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

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

# Residual — 2026-06-17 session, **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — the supplement was FILLED. This banner overrides the cold-case
> language below.** This bundle was *generated* cold (fresh CC session, reconstructed — true, and
> preserved below as generation-time history), but the operator then obtained **real architect
> answers** and `supplement filled` them into `SUPPLEMENT.md`. This is the **first real #159
> dogfood**: the fill→fold half is now exercised end-to-end (a browser-authored strategic *why*,
> carried verbatim and folded into your `PASTE_THIS`). Two things change for *you*, the incoming
> architect: **(1)** the `SUPPLEMENT.md` ANSWERS folded into your paste are **real, not empty** —
> read them as the authoritative strategic *why* (they cover intent, tensions, rejected options,
> open questions, decomposition, and off-repo context in depth). **(2)** the §13(d)
> operator-context beat **narrows to "anything changed since the supplement was written?"** — it
> does **NOT** "fire full." Every "cold / empty ANSWERS / beat fires full / #159 still owed
> entirely" phrasing below is **generation-time history**; the folded answers + this banner are the
> live truth. (The only #159 leg still genuinely open is the **incoming** §13(d) beat — exercised
> when *you* boot, not yet.)

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is **mostly clean**: `main` is back **in sync** and the merged stragglers were cleaned
> since 2026-06-16, but **one actionable drift carries** (§1: the `ARCHITECTURE.md` `pytest_collected`
> count, now 511→**534**). Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and
> the **durable** serialize-group graph (#156), not re-narrated IDs. Generated from inside the repo at
> HEAD `ef62dd8`, working tree clean, `main` in sync with `origin/main`. Re-derive HEAD/sync at
> read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session**; the v5.2 arc it
> hands off was done in a **prior** session, so there is **no live session reasoning** to transmit. The
> planning "why" below is **reconstructed from the repo** — JOURNAL (the 2026-06-17 entry + last ~6),
> BACKLOG, and the 2026-06-16 `-architect` bundle. State facts (§1, §5) are **witnessed** (verified live
> at generation); design framing (§2–§4) is **recall/inferred** from those sources — verify against the
> live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary.** The state moved since 2026-06-16: the 2026-06-16
> bundle's **first-dogfood finding** (a cold/`/clear`ed handoff produced **no** supplement file) **landed
> its fix as HANDOFF_PROCESS v5.2** — the architect strategic supplement is now an **always-generated,
> committed, fillable file** with a defined cold-handoff disposition. Orient first (`PROBES.md` P1),
> **then ask the operator for off-repo context** (§13d / #159 — **per the UPDATE banner the supplement
> was filled, so this beat narrows to "anything changed since the supplement?"**), then resume the
> design.
>
> **This bundle is itself the v5.2 cold case — read §2 "Where v5.2 leaves the dogfood".** This is the
> **first architect handoff generated under v5.2**, and like 2026-06-16 it is cold (fresh CC session, no
> outgoing browser). v5.2 makes that case **defined, not a gap**: `SUPPLEMENT.md` is generated and
> committed with empty ANSWERS. But the **real** #159 dogfood — a supplement filled with *actual* answers,
> folded into a `PASTE_THIS` — is **still owed** (surfaced, not buried).

---

## 1. Drift-flags — the headline (this time: **mostly clean, one carry**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (16/19 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P3/P4/P6/P7).

### DRIFT — actionable: `ARCHITECTURE.md` **`pytest_collected` is stale** *(the headline carry — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` **doc=511, actual=534** — the count
moved **further** past the doc since 2026-06-16 (was 511→530; the v5.2 `assemble_paste` ANSWERS-fold
tests added the +4). This is the **same** drift the 2026-06-16 bundle flagged, **still unfixed** —
carried, not introduced here. **Honest enforcement limit:** `audit.py health`'s integrated `doc_claims`
check reports `[OK] 3 self-claims match` and **does NOT catch this** — it gates only 3 of the 4 claims
(`audit_check_count`, `precommit_hook_count`, `precommit_hook_roster`); **only the standalone
`validate_doc_claims.py` (which probe P6 binds to) surfaces `pytest_collected`.** So `health: OK` is
*not* sufficient evidence the doc-claims are clean here.

- **Fix path (next-session work, not this handoff):** bump ARCHITECTURE's `**N collected**` claim
  (line 274) to the live `pytest --collect-only` count, then **genuinely re-read + re-stamp
  `last_reviewed`** (ARCHITECTURE is a canonical living doc — `canonical_freshness` will FAIL the
  *next* commit if the count edit lands without a re-stamp; the JOURNAL 2026-06-16 "operational gotcha"
  documents this exact sequencing trap). Left as a flagged drift, not silently patched mid-handoff.
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

### STATE — `main` is **in sync** with `origin/main`; **no merged stragglers** *(a clean change from 2026-06-16)*

The 2026-06-16 bundle flagged `main` **ahead 9** of origin (unpushed) + **six merged stragglers**. Since
then the v5.2 arc was **pushed** and the stragglers were **`-d`'d** — `git status -sb` reports
`## main...origin/main` (in sync) and `git branch --merged main` shows **only `main`**. The only other
branch is `automation/fleet-audit` (**never merges to main by design — ADR-84**, NOT a loose end).
**This handoff's own commits will put `main` ahead of origin again until pushed** (push is
operator-gated). Re-derive at read-time — `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The 2026-06-16 first-dogfood finding drove this window's work: it landed its fix as v5.2.** Since
2026-06-16 [witnessed via JOURNAL + audit state]:

- **v5.1 ephemeral block → v5.2 always-generated fillable file (the window's headline ship).** v5.1
  made the architect's strategic *why* a first-class advisory supplement, but the supplement became a
  durable artifact **only after** the outgoing browser answered an **ephemeral terminal interview block**
  — so a cold/`/clear`ed handoff produced **no file at all** (missing-deliverable look, zero git tracking,
  operator un-led). That is exactly what the 2026-06-16 bundle's §2 surfaced as a design question. **v5.2
  answers it structurally:** CC now writes `<bundle>/SUPPLEMENT.md` **unconditionally** (a self-documenting
  3-step header + a QUESTIONS section for the outgoing chat + an empty ANSWERS section), **commits it on
  the handoff branch** (empty or filled) for durable tracking, and `scripts/assemble_paste.py` folds the
  **ANSWERS region only, and only when non-empty** (was: whole-file fold + `[warn]`-if-absent). The
  **cold-handoff disposition** is now *defined* (empty ANSWERS = committed N/A, not folded; the incoming
  §13(d) beat fires full). Contract unchanged: advisory, why-only, never teeth, **never fabricated**
  (unanswered = committed empty). Coupled atomic move: `CONTRIBUTING.md` stamp v5.1→**v5.2** (the only
  gate-forced surface — major stays 5, so `CLAUDE.md` / `.claude/commands/handoff.md` unchanged); ADR-82
  amended in-file 2026-06-17. **Dogfooded** by rewriting the 2026-06-16 bundle's own `SUPPLEMENT.md` in
  the new always-file format (empty ANSWERS — the cold case), verifying the cold path folds nothing and
  leaves the immutable `PASTE_THIS.md` unchanged.
- **The carried governance themes are unchanged this window** — ADR-85 lifecycle-gate (the deterministic
  no-LLM Stop-gate: hard JOURNAL leg + advisory BACKLOG leg + HEAD-bound `/override`) shipped its v1 and
  the loop-defect fix (#142) in the *prior* window; this window touched none of it. The two ADR-85 build
  chains (#170→#168 traceability spine, #171→#169 conformance dashboard) and ADR-86 stand as filed.

**The design tensions now on the table** [recall/inferred]:

- **(A″) The hybrid handoff is shipped, hardened (v5.2), but the *value* is STILL un-dogfooded.** v5.1
  answered the *design* question; v5.2 closed the *cold-handoff* gap and hardened the mechanism (always-
  file, ANSWERS-only fold, defined N/A). But **no supplement has ever been filled with real answers and
  folded into a live `PASTE_THIS`.** Until one real run, "judgment transmits via the supplement" is a spec
  assertion, not an empirical fact. **This handoff is again cold** — so it again does not exercise the
  filled path unless the operator routes the QUESTIONS to a chat holding the v5.2 deliberation. The #159
  candidate persists; see "Where v5.2 leaves the dogfood" below.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** Move 1
  barely shrank the file; Move 2 (the structural split → thin `§N`-index + per-section modules) is
  justified on **maintainability** (≈84k tokens, ~3.5× the read-cap, frequently edited), **not**
  parallelism. Council-bound because the `§N`-index design is a genuine fork — the §1–§19 spine is the
  **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q-B.

### Where v5.2 leaves the dogfood (the #159 signal, surfaced — not a defect this time)

The 2026-06-16 §2 raised this as an open *question*; v5.2 **resolved the design and now this bundle
demonstrates the resolved behaviour** [witnessed this session]:

- **2026-06-16's open question is RESOLVED — do not re-open it.** "Does the v5.1 flow need a defined
  behaviour for the cold/`/clear`ed handoff?" → **yes, and v5.2 is it**: always-generate + commit the
  empty `SUPPLEMENT.md`, fold ANSWERS-only-if-non-empty, fire the incoming §13(d) beat full. This bundle's
  own `SUPPLEMENT.md` is the live demonstration (committed, empty ANSWERS).
- **What STILL stands open is the *empirical* leg, not the design.** #159's only-remaining clause is to
  exercise the **filled** path once — operator routes QUESTIONS → a chat holding the strategic *why*
  authors answers → CC commits the filled file → `assemble_paste.py` folds the ANSWERS region into the
  next session's `PASTE_THIS`. v5.2 makes that path *reachable and durable*; it does not *run* it.
- **The standing meta-argument (persists, now sharper):** every v5 bundle — **including this one** — is
  **hand-assembled** by CC following the spec; this is now also the first hand-assembly of the v5.2
  always-file `SUPPLEMENT.md`. That growing hand-maintained surface is the live case for **#164 (the
  generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q-A″ — run the real supplement dogfood + finish the generator (#159 + #164).** v5.2 shipped the
  *mechanism* (always-file + cold disposition + ANSWERS-only fold); the open work is (i) **exercise a
  *filled* supplement end-to-end in a real architect session** (#159's only-remaining clause — this
  session is again the candidate, but cold), and (ii) **#164 wires the emission durably in the always-file
  form** (the generator must write the unconditional `SUPPLEMENT.md` from
  `templates/handoff/v5/SUPPLEMENT.md.tmpl`).
- **Q-B — PLAYBOOK Move 2 (Council-bound, unchanged).** The structural split → thin `§N`-index +
  per-section modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N
  addressability — the consumer API). Maintainability-justified, not urgent. **Unblocks #39;
  decouples #18 / #67 / #77 / #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?); (ii)
  the **cross-repo v4 routing** (ADR-83) — a v4 target repo (lacking `scripts/audit.py`) needs a
  deterministic route to the v4 Phase-1/2 path; (iii) **architect-mode supplement emission in the v5.2
  always-file form** — the generator must write the unconditional `SUPPLEMENT.md` (QUESTIONS + empty
  ANSWERS) and re-run the assembler on `supplement filled`; (iv) a `PASTE_THIS.md` **freshness gate vs its
  sources** (audit F4 — today the assembled snapshot can silently drift).
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
- **Q-J — #170 → #168, the traceability spine.** Design + land the traceability-spine ADR (issue-ID↔commit
  anchor) — the airtight, **always-warranted** link that promotes ADR-85's BACKLOG leg from advisory to a
  **hard** gate (#168 depends-on #170). The spine is the un-gameable AND always-warranted anchor the
  interim structural-marker check lacks.
- **Q-K — #171 → #169, the conformance dashboard.** Build `ecosystem/conformance.md` (ADR-86 / ADR-85 R2)
  — a read-only validator generates **and commits its own output** (ADR-80 committed-generated-zone writer
  policy). It is the deterministic surface #169's ungated-doc staleness signal (ARCHITECTURE/VISION/
  LESSONS/CONTRIBUTING untouched >N sessions while code changed) lands in, and ARCHITECTURE Ch2 will
  point to it.
- **Q-L — ADR-85 standing governance obligation (not a design question — a watch).** The gate is **live**.
  A **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% →
  tune the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.

**Resolved-since 2026-06-16 (do NOT re-open):** the v5.1 cold-handoff supplement gap (→ **HANDOFF_PROCESS
v5.2** — always-generated fillable file + defined cold disposition + ANSWERS-only fold; only the *empirical*
#159 dogfood + #164 wiring remain) · the hybrid-handoff *design* (v5.1) · the Stop-hook loop defect
(#142) · ADR-85 v1 itself (only the R1/R2 hardenings #168/#169 remain as Q-J/Q-K).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **9 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #164, #10}` — these **serialize**
  (do not co-schedule). The **playbook** group = `{#146, #77, #67, #18, #39}`. The **audit-py** group =
  `{#153, #7, #36, #95, #140, #139, #166}`. The **architecture** group = `{#165, #35}`. (Plus `claude-md`,
  `claude-md-template`, `environment`, `pre-commit-config`, `settings-json` — see the validator's full
  summary line.) Hard precedence edges (`depends-on`): **#168 → #170**, **#169 → #171**. Parallel-safety
  is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A″ (#159 dogfood) is exercisable THIS session** — off the build path; but only if a chat holding
    the strategic *why* fills the supplement (this bundle is cold — see §2).
  - **#164 (Q-C) is the last big build item** — gated on the Q-C(i)–(iv) decisions; now also wires the
    v5.2 always-file `SUPPLEMENT.md` emission.
  - **#170 (Q-J) unblocks #168**; **#171 (Q-K) unblocks #169** — two independent ADR-85 build chains,
    parallel to each other and to the handoff group.
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
  recall; the file is truth). `validate_backlog`: **75 tasks, 0 warnings, 7 themes, 19 stories, 9
  serialize-groups** at generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end). **No merged stragglers** (cleaned since 2026-06-16). This handoff's
  own branch `docs/handoff-2026-06-17-architect` merges on completion.
- **Drift-flags:** the **actionable** `pytest_collected` 511→534 (§1, fix owed — carried from 2026-06-16)
  + the carried-benign `git_backlog_drift` #90a `[~~]` (#77). `main` in sync at generation. Re-derive:
  `python scripts/audit.py health` + `python scripts/validate_doc_claims.py` + `git status -sb`.
- **Audit-gating note:** `audit.py` check #19 `handoff_probes` validates the **lexically-max** v5
  bundle. `2026-06-17-dev-knowledge-architect` is now lexically-max → it **is** this check's target
  (superseding 2026-06-16). Its probes were verified to bind via `python scripts/verify_handoff_probes.py
  docs/handoffs/2026-06-17-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **20 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.179 > last reviewed 2.1.177` — `/changelog-review`.
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ARCHITECTURE `pytest_collected` drift** (§1) — bump 511→live count + genuine re-read/re-stamp.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — supplement FILLED.** This bundle was generated cold, but the
> operator then `supplement filled` real answers (see `RESIDUAL.md` UPDATE banner). The teeth probes
> (P2–P9) are unchanged — they bind to **live state**, which the fill does not touch. The only change
> is the **§13(d) beat in P1's gate: it now NARROWS to "anything changed since the supplement?"**, it
> does **not** fire full (the supplement carried answers). Read any "ANSWERS empty / beat fires full"
> phrasing below as generation-time history.

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
findings not in the repo / changed decisions). **The supplement was FILLED post-generation (UPDATE
banner), so the beat NARROWS to "anything changed since the supplement was written?"** — its Q6 already
captured the off-repo context (§13(d), "(d) refined, not duplicated"); do not re-ask it whole. The
*filled* supplement half of **#159** is now exercised; the **incoming** beat half (this one) is the
remaining clause — running it closes the dogfood loop.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `ef62dd8`, the tree was clean, and `main` was in sync with `origin/main` — but this handoff's own commits put `main` ahead until pushed, and HEAD/sync move on any commit, push, or fetch; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual — **and at generation this probe is EXPECTED TO MISMATCH** (the §1 headline carry: doc=511, live=534 and moving), so the live answer is the only ground truth | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** catch this; use the standalone |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present, and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + the v5.2 **always-generated** architect `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-17-dev-knowledge-architect/` (no `README.md`; `SUPPLEMENT.md` present with empty ANSWERS; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, and which `#id`s are in the **handoff** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, **narrowed to
   "changed since the supplement?"** (the supplement was filled — UPDATE banner) — before design. Then
   run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P6 is expected to MISMATCH at generation** (the carried headline drift, doc=511 vs live
   534) — the pass criterion is **"answered from the live source,"** never "matches the value the
   summary remembered." P8 pins the post-collapse four-file shape (+ the v5.2 always-generated
   architect `SUPPLEMENT.md`, no README); P9 pins the now-durable serialize-group graph (#156).

---

=== SUPPLEMENT.md ===

1. **Strategic intent — the way-of-working goal.**
This arc crossed from *building* enforcement to *discovering its two structural gaps*: imprecision and dependency-incoherence. Three mechanisms shipped — a deterministic session-lifecycle Stop-gate, the architect strategic supplement (v5.1 → v5.2), and a fix for the Stop-gate's own auto-bypass loop — and the moment they were in place, the deepest gap surfaced: **nothing catches "a process changed, so its dependent files must update."** A process was edited, a dependent runbook went partially stale, and nothing flagged it — coherence rode on the operator's memory.

So the next session's goal, at the methodology level, is: **make the methodology's own internal dependencies machine-legible and self-enforcing.** Treat this repo as a new kind of program — files are the objects, the AI agent is the runtime — and give it the equivalent of a compiler/linker for its *prose* dependencies. That is the "file-oriented dependency management" thread (now in external research). It is not a side quest; it is the systemic fix for the failure class this whole session kept hitting: coherence-by-memory.

The principle under all of it: **the methodology must practice its own doctrine.** This session caught the enforcement gate violating the anti-bypass rule it exists to enforce, and caught the architect (me) declaring "all verified" with no mechanism to verify. Close that reflexivity gap — enforcement that enforces itself, coherence that depends on no one remembering.

2. **Tensions weighed — and where I landed.**
- **Strict enforcement vs false-positive friction** (the central tension). A gate too eager fires on *correct* states, then loops or trains the operator to bypass it — which is worse than no gate, because it discredits enforcement. Landed: **hard-gate only what is un-gameable AND always-warranted; everything else stays advisory until a precise anchor exists.** The hard JOURNAL leg qualifies (a session must name a real commit — un-gameable). The BACKLOG leg stays advisory because "did this session finish a task?" is not yet mechanically knowable. Resisting early hardening is the right call; hardening an imprecise check is exactly how you manufacture the loop.
- **Carry vs re-derive across the handoff.** The supplement carries the *why* (it originates in the browser; the repo structurally cannot hold it). Repo *state* is never carried — it is forced-read via probes against live state. The dividing line is **re-derivability**: if a fact can drift and can be re-derived from its source, re-derive it, never transmit it. This is what stops the handoff from rotting (the old "v4 disease" was a maintained summary surface that silently drifted).
- **Always-generate the supplement file vs generate-on-answer.** v5.1 only wrote the file *after* answers came back, so a cold/cleared handoff produced nothing. Landed: **always generate the fillable file**, commit it regardless, fold it forward only if it has answers. The artifact's existence is decoupled from whether anyone was present to fill it.
- **Deterministic mechanism vs AI judgment** (the newest tension, deliberately left open for the research). A dependency check must be deterministic so it can't be argued away — but the coherence judgment ("does this doc still *accurately describe* the process?") is semantic, which an AI can assess and a linter cannot. The landing-in-progress: **deterministic trigger/gate, AI semantic assessment inside it.** Do not collapse to either pole.

3. **Considered + rejected — do not relitigate.**
- **Hardening the BACKLOG advisory leg now** — rejected. It is imprecise until the traceability spine (#170) exists; hard-gating it manufactures the false-positive loop we spent a day fixing. It stays advisory; #168 is the promotion and correctly depends-on #170.
- **Fire-once via `stop_hook_active` on the *hard* leg** — rejected outright. Making the hard gate allow-on-retry *is* the persistence-beats-policy antipattern the gate exists to forbid. Fire-once is for *advisory* legs only; the hard leg blocks until genuine compliance.
- **Structural-floor-only for the Stop-hook fix (drop standalone nudges entirely)** — considered, rejected for fire-once + floor-as-backstop, to keep the nudge when `stop_hook_active` is present (it is, at this runtime — verified live).
- **A git-touch heuristic for dependency coherence** ("the process changed but file X didn't → flag") — pre-emptively rejected. It false-positives whenever X *legitimately* needs no change — the exact BACKLOG-advisory failure, generalized. The research is steered toward *precise* detection (version-coupling / content-hash / declared contract), never touch-heuristics.
- **Restating the supplement mechanism in the playbook or instruction files** — rejected by the no-restate invariant. Those surfaces *defer* to the spec; adding the mechanism there would *be* the drift the invariant prevents (this was proven historically by a hand-copied command-name that drifted).
- **Fabricating a marker or a date to silence an advisory** — never. An advisory firing on a correct no-action state is a defect in the *check*, not a prompt to manufacture a marker.
- **Reopening the Stop-gate's shape or the hybrid-handoff design** — off the table. Both landed (the gate is under a scope-freeze through ~2026-07-14; the hybrid became v5.1/v5.2). Forward work is the hardenings, the generator, and the dependency mechanism — not re-deciding settled designs.

4. **Open questions — unresolved or deliberately deferred.**
- **File-dependency coherence (the top open thread).** No mechanism catches "process changed → dependents must update." Now in external online research, framed as *file-oriented dependency management*: classic dependency management (build DAGs, referential integrity, schema migration/semver, docs-as-code single-sourcing, observer/DI patterns) in a prose substrate with an AI executor. My own lean — **deliberately kept out of the research brief so it isn't anchored** — is version-stamp coupling: generalize the existing version-stamp check so every *declared* dependent of a process must carry a matching process-version stamp, forced to re-stamp (after a genuine re-read) on a bump. Weigh that against what the field actually has; there may be a named pattern I don't know. **This is the systemic fix for the failure that interrupted this very handoff — treat it as load-bearing.**
- **The answers-only fold (test it with THIS supplement).** The assembler folds the *answers* (not the questions) into the next session's paste, assuming answers are self-labeling. This is the first real test. I wrote these to be self-contained for exactly that reason — judge whether, read without the questions, they hold. If under-labeled, switch to folding question+answer pairs.
- **The traceability spine (#170 → #168)** — the keystone for precision. Sub-question surfaced this arc: it must recognize **closure-by-deletion** (a task closed by *removing* its line is invisible to an added-marker check). Key it on the issue-ID in the commit, so a closure is legible whether the task line was updated *or* deleted.
- **The generator (#164)** — the last machinery item; everything is hand-assembled until it lands. Open sub-decisions: the runbook sync key, cross-repo v4 routing, the always-file supplement emission, and a freshness gate on the assembled paste against its sources. **New, from the README failure: it must seed/update each repo's runbook idempotently — per-repo runbook drift is now a demonstrated live risk.**
- **PLAYBOOK Move 2** — Council-bound, deferred on maintainability (not parallelism). Any structural split must preserve the §N addressability that the consumer surfaces depend on.
- **Smaller deferred:** the architect actor-vs-mode vocabulary collision (#162 — resolve it, don't leave it live), a shared probe-core (#161), the ASCII-vs-diagram selection rule (#165, awaiting ratification), a doctrine-enforcement-coherence check (#166), the multi serialize-group parser (#167).

5. **Decomposition rationale — what NOT to redo.**
The graph is **two independent build chains, a keystone, and an emerging top thread.** #170 → #168 (spine → hard BACKLOG leg) and #171 → #169 (conformance dashboard → ungated-doc staleness) run parallel to each other and to the handoff group. The **handoff group serializes** — the handoff-touching tasks (generator, probe-core, vocab) share surfaces, so they must not co-schedule. #164 is the last big item; Move 2 dissolves the playbook serialize-group when it lands.

Do **not** re-decide: the hard precedence edges (#168 depends-on #170, #169 depends-on #171) are durable in the task graph — trust them, and do not try to harden the BACKLOG leg before the spine exists. The hard-vs-advisory split, the supplement model, and the Stop-gate's shape are all settled.

One integration to weigh, not redo: the file-dependency-coherence mechanism (coming from the research) likely **connects to or subsumes #169** — both mechanically detect doc incoherence. Before building #169 standalone, check whether the dependency mechanism is its parent. Re-derive the *soft* parallel/unblock judgment against the live backlog; trust the *hard* edges.

6. **Off-repo context — intent, priorities, findings not in the repo.**
- **The operator's mode this arc: fix it properly, in-session — don't defer.** When I recommended deferring the Stop-hook fix to a later session, he overruled it: a defect that misfires at *every* session-end cannot ride to "later." Default to fixing-in-session over deferring.
- **The process must lead the operator by the hand.** The v5.2 supplement-file redesign came directly from his frustration that the handoff was not a clear, structured, *pulled-by-the-hand* flow. Optimize the operator's *path*, not only the mechanism's correctness.
- **The biggest shift is a paradigm reframe.** The README failure (a process dependency nothing caught) led him to reframe the whole methodology as **a new programming paradigm — "file-oriented dependency management"**: Markdown files as objects, an AI agent as runtime, and a need for OOP-grade dependency mechanisms (inheritance/composition/observer analogs) adapted to prose. This is not a local fix; it reframes what the repo *is*. Hold this lens: the methodology is software, the files are its objects, and their dependencies must be managed like a real dependency graph.
- **Verify-first was validated in real time, three times this arc.** A verbatim cap-override message overruled a confident code-read; the live runtime overruled a doc-summary read; the README overruled my own "all verified." The lesson, now empirically hardened: **when a confident read — yours, the executor's, or a documentation summary — contradicts witnessed behavior, the behavior wins; dig until they reconcile.** Treat every report (including the executor's, including your own) as a claim to verify, not a fact.
- **A trust note for you, the incoming architect.** The operator's trust in "all verified" claims was rightly shaken this arc by my overconfidence. Earn it back not with reassurance but by verifying surfaces yourself — and because you are file-less, that means routing verification through the executor's *live* reads and the probes, never through a summary. Do not declare "done" on the easy metric (tests pass / the executor says so); declare it on the hard one (the end state actually meets the goal, checked).
- **Working mode.** The operator relays between this browser (the Layer-1 architect) and the coding agent (the Layer-3 executor); large paradigm questions go to a separate research session. The supplement you are reading is the first real transmission of architect *why* rather than a repo-reconstruction — its quality is the proof-of-concept for the entire v5.1/v5.2 supplement mechanism. Make it worth reading, then make it routine.
