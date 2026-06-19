=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-19-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one workday past `2026-06-18-dev-knowledge-architect`, capturing the 2026-06-19 window (scope-matrix **Case 2** — clean tree, commits since the `496016a` `…-architect` bundle, today's slug absent). The window landed the **enforcement seal**: **(1)** the **Phase-1 "seal" integration** — three worktree tracks merged `--no-ff` to `main` (seal-hooks: **#188** hook-completeness audit [OPEN] + the **C1** per-session JOURNAL SHA-anchor fix in `session_end_backpressure.py` + an ADR-85 amendment; seal-dedup: **#187** dedup-on-entry WARN + **#186** floor-sync of the #156 task-graph checks into the plugin floor; grooming: **#140** `doc_rot` grooming-gate, `ALL_CHECKS` 20→**21**), closing **#187 / #186 / #140**; **(2)** **ADR-88** *file-oriented dependency management* **authored** (`7e6f996`, **Proposed**) — the capstone the 2026-06-18 supplement directed, now existing-but-unratified; **(3)** the **consolidation doc-currency seal** — `DEFINITION_OF_DONE` C1-boundary rewrite (push→session), **ESSENTIALS** brought under the freshness gate (check #10), a sealed state report; **(4)** a **PLAYBOOK/ESSENTIALS currency groom** (purged the archived `/boot`,`/evolve`; fixed coherence) and a **session-wrap** (pushed `main`, deleted 9 merged branches + 3 seal worktrees, archived 2 deep-research transcripts). The next architect inherits the still-open strategic spine — **unify + encapsulate the methodology into ONE self-enforcing, deployable whole, with #131 (ai-council onboarding) as the first deployment test** (the 2026-06-18 filled supplement's directive) — now with the **capstone ADR-88 authored but unratified**, plus **#184** (demonstrate ADR-87, rides #131), the **§7 graduated review-command reconcile** (still not landed), **#181** coherence-v2 (data-gated on `logs/coherence-nudge.log`), **#164** (the v5 generator), the standing threads (**#162** vocab, **#161** probe-core, the **#170→#168** / **#171→#169** ADR-85 chains), and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `3a894ee`, working tree clean, `main` **in sync** with `origin/main` (0 ahead / 0 behind at generation). This handoff's own commits put `main` **ahead** of origin until pushed. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **⚠ UPDATE — supplement FILLED (warm).** Generated cold (fresh `/clear`ed CC session,
> reconstructed from JOURNAL + live git), but the operator then `supplement filled` **real
> architect answers**, now folded into `PASTE_THIS.md` (answers-only). Read the folded
> `SUPPLEMENT.md` answers as the **authoritative strategic *why*** of this handoff. **Headline:**
> everything this session did was **one thing — grounding ADR-88 (file-oriented dependency
> management) in reality.** The next session's way-of-working goal is to turn ADR-88 from
> *Proposed-and-partially-detected* into an **enforced lifecycle organ for the whole repo** — three
> organs: **(1)** a referential-currency detector (does every edge — command/ADR/§/file reference —
> still resolve?), **(2)** a structural linter (graph shape: numbering / headers / ToC — the things
> the architect *provably cannot eyeball*, proven this session), **(3)** an "earns-its-keep" check
> (does each node — file, automation, branch, folder — still justify existing?). **This must exist
> BEFORE further methodology deployment (#131)** — you cannot deploy onto a base that silently rots.
> **First move: the mechanism design from a debate running in another chat** (the design authority —
> *not* a re-audit). On the two CC-observed addenda: **A** ratify ADR-88 via a Council-equivalent
> deliberation *first* (the running debate may serve), **before** the build; **B** ship-gate =
> **(B) operator-accept the one-off + (C) tighten the wrap workflow so even a journal-wrap branches**
> — **reject (A)** (dispositioning direct-wraps erodes core-invariant #5). The §13(d) beat
> **narrows** to "changed since the supplement?" (it does **not** fire full). Read any "cold / empty
> ANSWERS / beat fires full" phrasing below as **generation-time history**. The 2026-06-18 filled
> supplement (`docs/handoffs/2026-06-18-dev-knowledge-architect/SUPPLEMENT.md`) remains the
> prior-window context.

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
- **Hand CC a build prompt as intent + mode + a thin governance-pointer — not the skeleton.**
  When a build task falls out of decomposition, emit *intent* + *closure* + *anti-patterns* +
  the *plan/auto mode* (with its basis) + a *thin governance-pointer* (the ADR/LESSONS/sibling-spec
  the task touches — CC won't self-infer it). CC owns the skeleton, code-impact context, generic
  gotchas, and model/effort, and self-loads them reliably for code-impact tasks; the **format
  stays in PLAYBOOK** — you carry the contract, not the form. Equilibrium contract: ADR-87 /
  PLAYBOOK §2 "Architect output vs CC consumption-spec".
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

# Residual — 2026-06-19 architect handoff (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to BACKLOG, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," the
> task-state points at the whole BACKLOG / relevant themes, and the open architecture questions
> travel as residual so the next session resumes the design rather than rediscovering it.
>
> **⚠ UPDATE — supplement FILLED (warm).** Generated cold (reconstructed from JOURNAL + live git in
> a fresh `/clear`ed session, not witnessed-live; the drift-checks below were run **live** at
> generation), but the operator then `supplement filled` real architect answers — see **§2**, now the
> authoritative strategic *why*. The §13(d) beat **narrows**. Read any "COLD / empty ANSWERS / beat
> fires full" phrasing below as **generation-time history**.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py health` / `ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation. **Re-derive each at read-time** — the
teeth are in `PROBES.md`, not in trusting these lines.

### ⚠ HEADLINE — `ship-gate` is RED: two wrap commits landed direct-on-`main` (undispositioned)

`python scripts/audit.py ship-gate` → **RED — 2 new/undispositioned WARN(s)**, both `no_ff_merges`:

- `3a894ee` (2026-06-19) `docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive)`
- `d0f9ead` (2026-06-19) `chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability)`

Both are **non-merge commits on `main`** (FF/direct), violating **core-invariant #5** (every
change — including one-line doc edits — goes branch → merge `--no-ff`; never direct to `main`).
They are the 2026-06-19 **session-wrap** commits: the wrap journal entry + the transcript archive
were committed straight onto `main` instead of via a branch + `--no-ff` merge. The session-wrap
JOURNAL entry records the work but **does not note** that these two went direct.

**Why this is a next-session decision, not fixed here:**
- They are **already pushed** — `main` was in sync with `origin/main` (0 ahead / 0 behind) at
  generation. Un-FF'ing them means a published-history rewrite — **off the table** (P0: no
  destructive history ops without explicit operator approval).
- So the resolution is a **judgment call the architect/operator must make**, not a mechanical fix:
  **(option A)** add a `disposition-register.yaml` entry classing direct-on-`main` *journal/chore
  wrap* commits as accepted (and decide whether to carve that pattern in generally — risky, it
  weakens core-invariant #5), **or (option B)** operator-accept the RED as a one-off slip and let
  it age out of the `no_ff_merges` window, **or (option C)** tighten the wrap workflow so even the
  journal-wrap goes through a branch (the real prevention). **This handoff surfaces it; it does not
  pick.** (Memory: *don't self-declare operator verdicts*; *state honest enforcement limits*.)
- **Process note for THIS handoff:** its own commits go on `docs/handoff-2026-06-19-architect` and
  merge `--no-ff`, so the handoff does **not** add to the `no_ff` drift. After the handoff merge,
  `ship-gate` will **still** be RED (the two pre-existing wrap commits remain) — that is expected;
  `PROBES.md` P7 binds to it.

### Other flags (benign / dispositioned)

- **`#77` closed-but-present** `[~~]` — `validate_git_backlog` flags `#77` (closes in `77e5d7df9`)
  still in `BACKLOG.md`. **Dispositioned** (`warn-77-voided-closure`) — a known voided/misattributed
  closure, carried benign. (Memory: *re-verify STRONG closure content* — `#77`/`#5` are the standing
  false-positive STRONG hits; do **not** close them on a tag match.)
- **5 `doc_rot` history-accretion WARNs** `[~~]` — BACKLOG `#164`/`#77`/`#134`/`#10` + CLAUDE.md
  `§section-history` (21 entries). All **grandfathered** (ref `#140`) when the `doc_rot` gate landed
  this window — the arc introduced the *detector*, not the debt; new accretion still blocks.

### ✅ Cleared since the last bundle — `pytest_collected` re-drift is FIXED

The 2026-06-18 bundle headlined `pytest_collected@ARCHITECTURE.md` doc=587 vs live=614. The
2026-06-19 **consolidation** session bumped `ARCHITECTURE.md` to the integrated live count on a
genuine end-to-end re-read. `validate_doc_claims` now reads **OK — 4 claims match**
(`pytest_collected` doc **667** / actual **667**; `audit_check_count` 21/21; hook count 9/9; hook
roster matches). `PROBES.md` P6 is therefore **expected to MATCH** this time — but the pass
criterion is still "answered from the live source," never "matches a remembered number."

---

## §2 — Supplement status (FILLED — warm) — the authoritative strategic *why*

`SUPPLEMENT.md` was generated cold (empty ANSWERS, committed) and then **FILLED** post-generation
with **real outgoing-architect answers**. `scripts/assemble_paste.py` folds the **ANSWERS region
only** into `PASTE_THIS.md` (answers-only — no QUESTIONS leakage); the incoming **§13(d) beat
narrows** to "anything changed since the supplement was written?". **Read the folded `SUPPLEMENT.md`
ANSWERS in full — they are the design authority for the next session.** The headline, surfaced (not
buried):

- **The through-line — everything this session did was ONE thing: grounding ADR-88 (file-oriented
  dependency management) in reality.** Model: *markdown files are objects; their references
  (commands / ADRs / §-sections / files) are edges; the repo is a graph; a retired target leaves a
  **dangling edge** read as if live — that is the rot.* The repo has a dangling-edge detector for
  **one** node type (the #156/#179 BACKLOG task-graph) and **none for prose**.
- **Strategic intent:** turn ADR-88 from *Proposed-and-partially-detected* into an **enforced
  lifecycle organ for the whole repo** — three organs: **(1) referential-currency detector** (does
  every edge resolve?), **(2) structural linter** (graph shape — numbering / headers / ToC, the
  things the architect *provably cannot eyeball* — proven 2/2 false this session), **(3)
  "earns-its-keep" check** (does each node — file, automation, branch, folder — still justify
  existing?). The two deterministic triggers already shipped this window are FC3 dedup (#187) + FC4
  history-accretion (#140); the **structural + lifecycle halves remain unbuilt**.
- **Sequence (locked):** prove-the-problem (this session's audit + manual groom = the *prototype*) →
  **design the mechanism** (a **debate running in another chat** — the next session's primary design
  input + design authority) → build + enforce → **then** deploy methodology (**#131**). The organ
  must exist **before** #131 — you cannot deploy onto a base that silently rots.
- **The two CC-observed addenda, answered:** **(A)** ratify ADR-88 via a **Council-equivalent
  deliberation first** (the running debate may serve), *before* the build — it is foundational
  doctrine, not the ADR-82/#149 narrow-operator-ratify class; it gates whether #179–#183 + the
  shipped detectors are *doctrine* vs *proposal*. **(B)** ship-gate RED → **(B) operator-accept the
  one-off + (C) tighten the wrap workflow so even a journal-wrap branches; reject (A)** —
  dispositioning direct-wraps away erodes core-invariant #5 (the genuine fork is acknowledged, but
  the architect's call is *tighten, don't disposition*).
- **Do NOT redo** (per the answers): the confirm-live ledger, the committed currency audit, the
  note-vs-usable distinction, the *structural-claims-need-a-live-organ* lesson, or the groom itself —
  and **do not re-audit PLAYBOOK/ESSENTIALS by hand**; build the organ so hand-auditing is never
  needed again.

**Prior-window context (still relevant, not superseded):** the **2026-06-18 filled supplement**
(`docs/handoffs/2026-06-18-dev-knowledge-architect/SUPPLEMENT.md`) — *unify + encapsulate into ONE
self-enforcing deployable whole, #131 as the first deployment test, enforcement > documentation*.
This window's answers **sharpen** that into its first concrete dependency: the lifecycle organ for
ADR-88 must exist before #131.

---

## §3 — Planning *why*: the 2026-06-19 window arc (what the design did and why)

The window executed the **"machinery not memory" closures** the 2026-06-18 supplement named as the
unify-goal's dependency — the enforcement gaps that let the methodology be bypassed:

1. **Phase-1 "seal" — three worktree tracks integrated `--no-ff`, then closed via `/review-closures`.**
   - **seal-hooks (`442c994`)** — **#188** hook-completeness audit [left OPEN per operator] (no
     uncovered zones; the live finding = the P0 `block-onedrive` guard sees only the shell command
     string, not `Edit`/`Write` `file_path` → **#191** filed as the `file_path` PreToolUse guard);
     the **C1** fix in `session_end_backpressure.py` (the JOURNAL SHA-anchor was computed at the
     *push* boundary, so deferred-serial-push let one prior citation vaccinate a multi-session arc —
     narrowed to the **session** boundary, `--first-parent`); **ADR-85 amendment** records the
     per-session-anchor semantics.
   - **seal-dedup (`dd025c3`)** — **#187** deterministic near-duplicate-title WARN on the hub
     `validate_backlog.py` (token-overlap, explicit stated limit, never a hard-fail); **#186**
     floor-sync of the **#156** task-graph checks (`depends-on` reference-existence + no-cycle)
     **verbatim** into the plugin floor, with an ADR-78 carrier-doctrine twin-marker.
   - **grooming (`e48da28`)** — **#140** `doc_rot` grooming-gate: new `scripts/validate_doc_rot.py`
     + `audit.py check_doc_rot` (`ALL_CHECKS` 20→**21**), the **Layer-2 deterministic trigger for
     ADR-88 FC4** (history-accretion bloat). DETECT-only / condense-preserving; 5 pre-existing loci
     grandfathered (teeth verified RED→GREEN).
2. **ADR-88 *file-oriented dependency management* authored (`7e6f996`, Proposed).** The capstone the
   2026-06-18 supplement directed ("name the paradigm as an ADR, not a VISION"). It names markdown-
   as-a-design-pattern and the failure classes the paradigm addresses; `#140` is its FC4 trigger,
   already shipped. **Status: Proposed — unratified** (open question §4).
3. **Consolidation doc-currency seal.** `DEFINITION_OF_DONE` JOURNAL-gate boundary rewritten
   **push→session** (the C1 amendment); **ESSENTIALS** brought under the canonical freshness gate
   (`audit.py` check #10 / `_FRESHNESS_FILES`) with the coherent four→five ripple; a sealed
   sealed/open/sequenced **state report** (`docs/audits/2026-06-19-consolidation-state-report.md` —
   the **text precursor to the visual workflow/dependency dashboard**). The session **refuted its
   own central hypothesis** ("PLAYBOOK prompt-format lags ADR-87" — PLAYBOOK §2 already carried the
   ADR-87 contract verbatim), so the real laggard was `DEFINITION_OF_DONE`.
4. **Currency groom + session-wrap.** PLAYBOOK/ESSENTIALS reconciled against live state (purged the
   archived `/boot`,`/evolve` from usable positions → one consolidated retired-machinery note; fixed
   two off-by-one §-cross-refs; tagged the ADR-87 split in the prompt skeletons). Wrap: pushed
   `main`, deleted 9 merged branches + 3 seal worktrees (no-loss verified), archived 2 deep-research
   transcripts (dependency-detection + doc↔code-traceability — these **feed** the doc-lifecycle /
   dependency Council arc). **← This wrap is where the §1 direct-on-`main` slip happened.**

**The through-line:** every track this window was an *enforcement* move (a gate, an anchor fix, a
detector, a floor-sync) — exactly the "machinery not memory" the unify-goal depends on. The capstone
doctrine (ADR-88) now exists to name *why* they cohere. What is **not** yet done is the unification
itself — composing these into ONE articulable, deployable whole and proving it on **#131**.

---

## §4 — Open architecture questions (travel as residual — resume the design, don't rediscover it)

> **Reframed by the FILLED supplement (§2).** The **top thread is now the ADR-88 lifecycle-organ
> design** — taken from a **debate running in another chat** (the design authority; the next session's
> first move is to incorporate its output, **not** a re-audit). Q1 and Q4 below now carry an architect
> **lean** from the answers (still open = *decide/execute*, not *rediscover*). The 2026-06-18 "#184
> first" sequencing is **subordinated** to "the lifecycle organ exists before #131."

0. **The lifecycle-organ mechanism (NEW top thread).** Design + build the three organs (§2:
   referential-currency detector · structural linter · earns-its-keep check). Primary input = the
   running mechanism debate. Open *inside* it: how does the detector mechanically tell a *note* from a
   *usable* dead-ref (the note-vs-usable distinction is load-bearing — ~18 `CHANGELOG retired` notes
   are keep, not purge)? How does the linter cope with a two-documents-glued file (the PLAYBOOK
   one-doc-or-two question)? Does the organ start prose-only or span all node types (files / automation
   / branches / folders)?
1. **ADR-88 ratification path** *(lean in §2: Council-equivalent first, before the build)*. ADR-88 is
   **Proposed**. The answer leans **ratify via a Council-equivalent deliberation** (the running debate
   may serve) **before** the build, since it is foundational doctrine (not the ADR-82/#149
   narrow-operator-ratify class); it gates whether `#179–#183` + the shipped detectors are *doctrine*
   vs *proposal*. **Decide + execute.**
2. **The unify + encapsulate goal — sequence it.** The strategic spine (§2) is still unbuilt as a
   *whole*. With the enforcement gaps now closed (#140/#187/#186/#191) and the capstone authored,
   what is the **decomposition** of "ONE self-enforcing deployable whole → test on #131"? The
   2026-06-18 supplement's sequencing held **#184 first** (demonstrate ADR-87, riding #131's
   onboarding as the real build). Re-confirm or re-decide.
3. **§7 graduated review-command rule — still not landed.** The 2026-06-18 supplement specified
   interim → `/code-review high`; final pre-merge (3+ files) → `/codex-review`, with Codex auth =
   ChatGPT-authed default (no per-token billing). **Not encoded in PLAYBOOK §7.** A small encoding
   that "rides along" — but still open.
4. **The §1 `ship-gate` RED disposition** *(lean in §2: B + C, reject A)*. The answer leans
   **(B) operator-accept the already-pushed one-off + (C) tighten the wrap workflow so even a
   journal-wrap branches**, and **reject (A)** (dispositioning direct-wraps away erodes core-invariant
   #5 — "the ship-gate going RED is the system correctly flagging the erosion; honor it by tightening,
   not by dispositioning it away"). The genuine fork is acknowledged (A is defensible if a journal-only
   wrap is judged low-risk-enough to exempt). **Operator decision + execute.**
5. **Standing design threads (unchanged from the prior bundle, still open):** **#181** coherence-v2
   (data-gated on `logs/coherence-nudge.log` accumulating signal); **#164** the v5 cross-repo handoff
   generator (+ the deferred `verify_handoff_probes.py` teeth validator); **#162** architect
   actor-vs-mode vocab; **#161** the teeth probe-core; the **#170→#168** / **#171→#169** ADR-85
   chains; the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14 — is the session-end gate
   over-firing?).

---

## §5 — Task-state (pointer, not narration — v5 §6)

- **The BACKLOG is the spec; items are tickets.** Read `BACKLOG.md` directly. Live shape:
  `validate_backlog: OK — 7 themes, 20 stories, 82 tasks, 0 warnings`. Themes: Big picture · Handoff
  continuity · Enforced governance · Lessons feedback loop · Decision management · Canonical-file
  integrity · Cross-repo universalization · Tooling & evaluation.
- **Serialize-groups (#156 durable task-graph — live):** 10 groups. The **handoff** group =
  `#1, #26, #159, #161, #162, #184, #164, #10`; the **coherence** group = `#179, #180, #181, #182`.
  *(These are live schema facts that drift on any BACKLOG edit — `PROBES.md` P9 re-derives them; do
  not trust this line.)* The soft/provenance graph beyond the hard `depends-on` edges stays residual
  prose (ADR-66 amendment: `depends-on` is hard-blocked-by only).
- **Closures pending:** the SessionStart surfaced **16 closure proposals** — `/review-closures` is a
  separate human-gated loop, **not** this handoff's job. Standing false-positive STRONG hits to
  exclude: `#5` / `#77`.
- **Branches:** `main` + `automation/fleet-audit` (KEPT — by-design ADR-84 writer-isolation infra,
  not a straggler). No merged stragglers at generation. This handoff adds
  `docs/handoff-2026-06-19-architect` (merges `--no-ff`, then deletable).
- **Drift-flag (task-state):** the only `validate_git_backlog` flag is the dispositioned `#77` (§1).

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — supplement FILLED.** This bundle was generated cold, but the
> operator then `supplement filled` real answers (see the `RESIDUAL.md` / `HANDOFF_BOOT.md` UPDATE
> banners + the folded `SUPPLEMENT.md`). The teeth probes (P2–P9) are **unchanged** — they bind to
> **live state**, which the fill does not touch. The only changes: the **§13(d) beat in P1's gate
> NARROWS** to "anything changed since the supplement?" (it does **not** fire full), and **P8's
> ANSWERS state is FILLED** (not empty). Read any "cold / empty ANSWERS / beat fires full" phrasing
> below as **generation-time history**; read the folded `SUPPLEMENT.md` answers first.

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer**. The browser has no file access, so for every probe it must reply
> **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC**
> runs each command against **live state at check-time**, re-derives ground truth, and records
> PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN
> `anchor-missing`, re-anchor (never a synthesized pass); git/tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> The answers — the orienting lines, the check count + last name, the HEAD sha, the drifted
> `#id` + closing sha, the serialize-group membership, the counts, the dates — are deliberately
> **absent from this whole bundle**. That is what gives the probes teeth. Do not infer them; run
> the command.
>
> **This bundle is COLD** (fresh CC session; `SUPPLEMENT.md` committed with empty ANSWERS), so the
> §13(d) operator-context beat in P1's gate **fires FULL** — there is nothing to narrow against.
> The *2026-06-18* bundle's **filled** supplement carries the operator's most recent strategic
> *why* (pointer in `RESIDUAL.md` §2/§3); read it as context, then the beat asks the live off-repo
> question.

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
findings not in the repo / changed decisions). **This bundle is COLD** (empty ANSWERS — `RESIDUAL.md`
§2), so the beat **fires FULL** — there is no this-session supplement answer to narrow against. Read
the *2026-06-18* filled supplement first (the most recent strategic *why*), then ask the full
off-repo question.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `3a894ee`, the tree was clean, and `main` was in sync (0/0) — but this handoff's own commits put `main` ahead until pushed, and HEAD/sync move on any commit, push, or fetch; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` (line 284) + live pytest | the live count drifts on any test change; neither integer appears in the residual — **unlike the prior bundle this probe is now expected to MATCH** (the 587-vs-614 re-drift was fixed in the 06-19 consolidation; the residual claims 667/667), but the live count is still the only ground truth and the pass test is "answered from the live source," not "matches a remembered number" | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** isolate this; use the standalone |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, and if RED, **which commits** (full short-sha + date) does the `no_ff_merges` check name as direct-on-`main`? | live git ∩ `main` history ∩ `disposition-register.yaml` | **THIS is the §1 headline** — at generation ship-gate is **RED** with **two** undispositioned `no_ff_merges` WARNs (`3a894ee`, `d0f9ead`, the 2026-06-19 wrap commits); but the live answer is the only ground truth (a disposition could be added, or new commits could appear), and the values are high-entropy / absent from the bundle | `python scripts/audit.py ship-gate` (read the `no_ff_merges` lines + the final RED/GREEN verdict) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + the v5.2 **always-generated** `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-19-dev-knowledge-architect/` (no `README.md`; `SUPPLEMENT.md` present, **ANSWERS FILLED** post-generation — see the UPDATE banner; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`s are in the **handoff** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle (unlike the prior window, **no new group formed** this window — the `coherence` group already exists) | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, **NARROWING**
   this bundle (supplement **FILLED** post-generation — read the folded `SUPPLEMENT.md` answers first,
   then ask only "anything changed since the supplement?") — before design. Then run P2–P9, each
   against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P2/P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P7 is the headline: expected RED** (two undispositioned `no_ff_merges` wrap commits, §1)
   — but the pass criterion is **"answered from the live source,"** never "matches the verdict the
   summary remembered." **P6 is now expected to MATCH** (667/667 — the prior re-drift was fixed). P2 is
   expected to read **21** (last name `doc_rot`; no new check landed since the #140 grooming-gate). P8
   pins the post-collapse four-file shape (+ the v5.2 always-generated `SUPPLEMENT.md`, **ANSWERS
   FILLED** post-generation; no README). P9 pins the now-durable serialize-group graph (#156) — the `handoff`
   and `coherence` groups, no new group this window.

---

=== SUPPLEMENT.md ===

# Handoff supplement — outgoing architect — 2026-06-19



> Old hand to new hand. This is not a task list — it is the *way-of-working* state at the close
> of a long session, so the next architect inherits judgment, not just facts. Written deep, not
> exhaustive. Repo facts (SHAs, line numbers) are in the residual + the committed audit; this is
> the **why**.

---

## The through-line — read this first

Everything this session did was one thing: **grounding ADR-88 (file-oriented dependency management) in reality.** Not a side-cleanup — the central arc.

The session's core engineering was the **Phase-1 seal: three Claude-Code worktrees run in parallel** (this was the most important work):
- **seal-hooks** — fixed the **C1 JOURNAL-gate bug** (the Stop-gate computed its commit arc as the *push* boundary, so under deferred-serial-push a multi-session unpushed arc let one prior SHA-citation "vaccinate" the whole arc → later sessions could ship unjournaled and the gate passed silently). Narrowed to the *session* boundary. Also the #188 hook-completeness audit.
- **seal-dedup** — #187 dedup-on-entry + #186 floor-sync.
- **seal-grooming** — #140 `doc_rot` history-accretion detector.

Those three shipped **ADR-88's deterministic triggers**: FC3 dedup (#187) and FC4 history-accretion (#140). So part of ADR-88 is already mechanically real. The afternoon then authored ADR-88 itself (Proposed) and ran straight into the proof that the *rest* of it is not real: PLAYBOOK + ESSENTIALS were rotting with references to machinery that no longer exists. We audited, groomed the currency, and cleaned the repo — but the structural and lifecycle halves remain unbuilt.

**Where the next session must focus:** make file-oriented dependency management *enforced across the whole repo* before any further methodology deployment (#131). The methodology is not deployed yet. It is closer. It is not there.

---

## What ADR-88 actually is (because you said you don't fully feel it)

Plain model: **markdown files are objects. Their references are edges. The repo is a graph.**

A file references other things — commands (`/boot`), ADRs, sibling sections (`§16`), other files, systems. Each reference is an **edge** from this node to another. In OOP terms: an object holding a pointer to another object. When the target is retired (a method deleted, a command archived, a section removed), the edge becomes a **dangling pointer** — it points at nothing, but it still sits there, read as if live.

The repo has a dangling-edge detector for **one** node type — the BACKLOG task-graph (#156 / #179). It has **none** for prose. So prose docs accrete dangling edges with nothing to catch them. That is the rot you feel. The four failure classes:

- **FC1** — spine-failure (the coherence spine breaks).
- **FC2** — undeclared edges (#179): a real dependency that isn't declared, so nothing tracks it.
- **FC3** — duplication (#187): the same content in two places, drifting apart.
- **FC4** — history-accretion (#140): dead content piles up and is never removed.

"Graphs / whole-repo" = treating every node (file, automation branch, folder) as a graph node that must (a) have all its edges resolve, and (b) prove it still **earns its keep**. That second half is the broadened diagnosis below.

---

## 1. Strategic intent (way-of-working goal)

Turn ADR-88 from *Proposed-and-partially-detected* into an **enforced lifecycle organ** for the whole repo, so the repo becomes self-policing about its own coherence. Concretely, three organs:
1. **Referential-currency detector** — does every edge (command/ADR/section/file reference) still resolve?
2. **Structural linter** — is the graph shape sound? (numbering, header scheme, ToC — the things the architect provably *cannot* eyeball; see Q3.)
3. **"Earns-its-keep" check** — does each node still justify existing? (files, automation, branches, folders — see Off-repo.)

The goal is not to fix today's rot (we did, manually). It is to make manual re-grooming **never necessary again** — so #131 deployment stands on a base that cannot silently rot.

## 2. Tensions weighed, where I landed, why

- **Groom-first vs mechanism-first** → groom-first. The manual currency groom was the *prototype*: doing it by hand is what told us exactly what is mechanical vs judgment, which makes the mechanism design concrete instead of abstract. It also unblocked the handoff (a handoff built on a lying PLAYBOOK carries the rot forward).
- **Where the organ runs** → the same **detect / groom / gate** triad as the rest of the system: detect = nightly conformance digest (ADR-84); groom = human-ratified purge; gate-on-regression = pre-commit + handoff (universal root-7 + a `.dev-knowledge`-local extension for PLAYBOOK/ESSENTIALS). Hard-gating *full* currency would breed `/override` habits, so the gate only blocks *newly-added* dead edges.
- **One problem or three** → three distinct organs. The architect can reliably reason about *references* but **not** *structure* (proven, Q3). So references → detector; structure → linter; lifecycle → earns-its-keep. Don't collapse them.

## 3. Considered + rejected — do NOT relitigate

- **Blanket-purge of every retirement annotation** — REJECTED. Two kinds: dead-refs-in-usable-positions (purge) vs anti-regression context-notes (keep). The ~18 `CHANGELOG retired` notes are load-bearing; a detector that flags all of them is wrong. The **note-vs-usable distinction is settled** and is a load-bearing requirement of the detector.
- **Architect eyeball for structural claims** — REJECTED, *proven wrong this session*. My audit's structural section was 2/2 false: the §18 numbering gap is intentional (documented, "git has it") not rot; the embedded-template H2s sit inside fenced blocks the ToC generator skips, so they don't pollute anything and demoting them would corrupt the templates. A grep over a snapshot cannot see fences, intent-notes, or generator behaviour. **Structural checks must be a live organ. Settled.**
- **Memory-based dead-lists** — REJECTED. Truth derives from live state ∪ the retirement ledger (JOURNAL / archive / ADR), never a hand-kept list. Mechanism-not-memory is ADR-88's own principle.
- **Renumbering the §18 gap; demoting the H2s** — REJECTED (above). Renumbering would have *created* new dangling edges.

## 4. Open questions (unresolved / deferred)

- **The mechanism's exact shape** — you have a debate running in another chat that proposes the solution; that proposal is the next session's primary design input. Open inside it: how does the detector mechanically tell note from usable? How does the linter cope with a two-documents-glued file?
- **The two-docs split** — is PLAYBOOK one document or two (a *reference* doc + a *workflow-recipes* doc)? This is where "I can't see the shape of my infrastructure" lives. Deferred to a deliberate structural decision (Council-class).
- **Lifecycle scope** — see Off-repo: the rot is not only prose edges; automation, branches, folders, ENVIRONMENT.md currency all need the earns-its-keep check. Open: does the organ extend to all node types or start prose-only?
- **ESSENTIALS-as-lens** — reshape ESSENTIALS into a 1:1 projection of PLAYBOOK's chapter list (itself a checkable file-dependency). Deferred, deliberate.
- **Over-annotation condense** — the ~18 / ~10 / ~8 inline retirement notes → canonical-once. Deferred (operator judgment on aggressiveness).
- **Residuals A and B** below.

## 5. Decomposition rationale — what NOT to redo

Locked sequence: **prove the problem** (this session: audit + manual groom = the prototype) → **design the mechanism** (your running debate) → **build + enforce** → **then deploy methodology (#131)**. The groom-as-prototype concretizes the design; the organ must exist before #131 because you cannot deploy onto a base that silently rots.

Do **not** redo: the confirm-live ledger (`/boot`/`/evolve` dead; `/save`/§19 live; all 44 cited ADRs resolve — verified live); the committed audit's findings; the note-vs-usable distinction; the structural-claims-need-a-live-organ lesson (now in LESSONS); the currency groom itself (shipped, merged). **Do not re-audit PLAYBOOK/ESSENTIALS currency by hand** — build the organ so it never needs hand-auditing again.

## 6. Off-repo context

- **Operator state**: deep frustration that `protocols/` rots despite long effort — felt as the methodology not-yet-being-real. The reframe that landed and should hold: it is **one missing organ (lifecycle enforcement)**, not a failed methodology. Everything else worked this session.
- **A debate is running in another chat** proposing the mechanism. Incorporate its output; it is the design authority for the next session.
- **Broadened diagnosis (this-session finding, not yet in an ADR): system-lifecycle-rot, not just doc-rot.** Automation (`automation/fleet-audit`, `automation/conformance-digest`), branches, folders, ENVIRONMENT.md — all accrete with nothing asking "does this still earn its keep / is its output consumed." `fleet-audit` is confirmed live by-design ADR-84 infra (it writes daily; verified, kept) but **its output-consumption is unverified** and it writes local-only (not pushed to origin like its sibling) — a concrete instance of the open lifecycle question.
- **Priority is explicit**: file-oriented dependency management + graphs + whole-repo coherence come **before** further methodology deployment.

---

## A. ADR-88 ratification path — and what it gates

**Lean: ratify via Council (or a Council-equivalent deliberation), not bare operator-ratify — and ratify *before* the mechanism build.** ADR-88 is foundational doctrine — the "files are objects with edges" model the entire lifecycle organ will enforce — not a narrow/procedural decision like the ADR-82/#149 operator-ratify precedent. **But**: your running debate may itself be the deliberation. If it is a genuine multi-agent weighing of the doctrine, its verdict can serve as the ratification basis; otherwise convene. **What it gates**: whether #179–#183 and the shipped detectors are treated as load-bearing *doctrine* vs *proposal*. The mechanism can be *built on* them while Proposed; calling them canonical waits on ratification. Ratify first so the build enforces ratified doctrine, not a draft.

## B. ship-gate RED — disposition

**Lean: (B) for the immediate RED, (C) for the durable rule.** The two wrap commits are already pushed and un-FF — you can't un-ring them, so operator-accept the one-off (B). Going forward, tighten the wrap workflow so even the journal-wrap branches + FFs (C). Reasoning: a wrap commit is still a commit, and "direct-on-`main`" is exactly the discipline-erosion core-invariant #5 exists to prevent — so **#5 should bind a wrap as strictly as anything else.** Reject (A): dispositioning direct-wraps as acceptable is the camel's nose — it converts the invariant into a suggestion. Note the genuine fork: (A) is defensible *if* you judge a journal-only wrap as low-risk-enough to exempt and would rather accept mild gate-noise than mild branch-ceremony. I don't — but it's your call to make, and the way the ship-gate went RED is itself the system correctly flagging the erosion. Honor it by tightening, not by dispositioning it away.

---

*Outgoing-architect supplement, session 2026-06-19. Pairs with the residual and the committed audit `docs/audits/2026-06-19-playbook-essentials-currency-audit.md`. The next session's first move is the mechanism design from the running debate — not a re-audit.*
