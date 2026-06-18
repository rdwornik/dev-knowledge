=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-18-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one workday past `2026-06-17-dev-knowledge-architect-2`. The 2026-06-18 window landed four linked things: **(1)** **ADR-87** — the architect/CC **equilibrium contract** (the prompt division of labor: architect emits intent + closure + anti-patterns + mode + a thin governance-pointer; CC owns code-impact context, gotchas, the skeleton, model/effort) — codified across PLAYBOOK §2, the prompt template, ESSENTIALS, HANDOFF_BOOT; empirical close = **#184** (OPEN), GAP-2 residue = **#185** (filed, not built); **(2)** the **coherence-spine consolidation** — #172's v2 roadmap **extracted** into **#179–#183** (a NEW `coherence` serialize-group; the prior bundle's load-bearing "extract before close" first-action) and **#172 closed**; **(3)** a **backlog groom** — closed #138, condensed the giants (ADR-65), filed #187–#189 (net 83 tasks); **(4)** the **worktree / parallel-arc lifecycle** codified in PLAYBOOK (native auto-seed verified). The next session inherits the candidate top thread — **name "file-oriented dependency management" as an ADR** (the prior supplement's explicit directive; the durable #179–#183 graph now lacks its capstone doctrine) — plus **coherence v2** (#181 data-gated on `logs/coherence-nudge.log`), the **§7 review-command graduated-rule reconcile** (not landed), **ADR-87 demonstration** (#184), **#164** (the v5 generator), the standing threads (#162 vocab, #161 probe-core, the **#170→#168** / **#171→#169** ADR-85 chains, **#186** plugin-floor sync), and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `62763d7`, working tree clean, `main` **in sync** with `origin/main`. This handoff's own commits put `main` **ahead** of origin until pushed; **no merged stragglers** (the prior bundle's two were `-d`'d). Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **⚠ UPDATE — supplement FILLED (warm).** Generated cold, but the operator then `supplement filled`
> real architect answers, now folded into `PASTE_THIS.md` (answers-only). Read the folded
> `SUPPLEMENT.md` answers as the authoritative strategic *why*: **the top priority is to unify +
> encapsulate the methodology into ONE self-enforcing, deployable whole, with #131 (ai-council
> onboarding) as the first deployment test** (enforcement > documentation; the named spine-failure is
> "accepting inherited framing without verifying against state"). **First moves for the next architect:
> author the capstone "file-oriented dependency management" ADR; sequence #184 first (it rides #131's
> onboarding as the real build proving ADR-87); the §7 graduated review-command rule rides along
> (Codex auth = ChatGPT-authed default).** The §13(d) beat **narrows** to "changed since the
> supplement?" (not full).

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

# Residual — 2026-06-18 session, **architect mode** (v5.2 canonical §13)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — the supplement was FILLED. This banner overrides the cold-case
> language below.** This bundle was *generated* cold (fresh CC session — true, preserved below as
> generation-time history), but the operator then obtained **real architect answers** and
> `supplement filled` them into `SUPPLEMENT.md`. Two things change for *you*, the incoming architect:
> **(1)** the `SUPPLEMENT.md` ANSWERS folded into your `PASTE_THIS` are **real, not empty** — read
> them as the authoritative strategic *why*. **(2)** the §13(d) operator-context beat **narrows to
> "anything changed since the supplement was written?"** — it does **NOT** "fire full." Every
> "cold / empty ANSWERS / beat fires full" phrasing below (and in `PROBES.md` / `HANDOFF_BOOT.md`) is
> **generation-time history**; the folded answers + this banner are the live truth.
>
> **⚠ The strategic headline (from the answers — surfaced, not buried):** the operator's **top
> priority reframes the next session above the prior thread.** It is **not** "build the next coherence
> mechanism" — it is **unify + encapsulate the whole methodology into ONE coherent, SELF-ENFORCING
> whole, deployable to a fresh repo, with #131 (ai-council onboarding) as the first deployment test.**
> The methodology already *exists* and is mature; what it is *not* yet is a **self-enforcing** whole —
> this session repeatedly showed the architect **bypassing** the methodology because correctness rode
> on *remembering* to apply it. The named spine-failure: **"accepting inherited framing without
> verifying against state."** So the unify-goal prioritizes **enforcement > documentation** (machinery
> that can't be bypassed: #187 dedup, #140 grooming-gate, #188 deny/hook audit are the "machinery not
> memory" closures it depends on). **Operationally load-bearing for *you*:**
> - **Author the capstone "file-oriented dependency management" ADR now** (answer A) — it *serves* the
>   unify-goal by turning #179–#183 from a feature list into doctrine. Failure-class order suggested
>   (verify against the live #179–#183 scope before locking it).
> - **Sequence #184 first** (answer B): ADR-87 must be *proven*, not just codified — and **#131's
>   onboarding is the natural real-build to demonstrate it on, so #184 rides #131.** The §7 graduated
>   review-command rule rides along; Codex auth = **ChatGPT-authed** default (Max sub) — confirm before
>   any `/codex-review`.
> - **Cross-repo deployment caution:** client-identifying context leaked into a gotcha this session
>   (now generalized; #130 capture-scrub arm) — watch for it in any deployment. And the **empty
>   `ANTHROPIC_API_KEY` → Max-OAuth** override is **load-bearing** (do not break it).
>
> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — this time the
> headline is an **actionable re-drift**: `pytest_collected@ARCHITECTURE.md` says **587** but live
> pytest now collects **614** (this window added ~27 tests and the doc count was not re-bumped). The
> lone other flag is the carried-benign `#77` `[~~]` voided closure. `main` is **in sync** with origin
> and there are **no merged stragglers** this time. Pointers are paths, not copies. Task-state is a
> pointer to `BACKLOG.md` + the **durable** serialize-group graph (#156), not re-narrated IDs.
> Generated from inside the repo at HEAD `62763d7`, working tree clean, `main` in sync with
> `origin/main`. Re-derive HEAD/sync at read-time (`PROBES.md` P3).
>
> **Provenance — reconstructed, not witnessed-live.** This is a **fresh CC session** (`/clear`ed); the
> 2026-06-18 arc it hands off (the equilibrium contract, the coherence-spine consolidation, the backlog
> groom, the worktree-lifecycle gap-fill) was done in **prior** sessions, so there is **no live session
> reasoning** to transmit. State facts (§1, §5) are **witnessed** (verified live at generation via the
> read-only drift-checks); design framing (§2–§4) is **recall/inferred** from JOURNAL (the nine
> 2026-06-18 entries) + BACKLOG + the two prior architect bundles — verify against the live BACKLOG
> (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff one workday past the `2026-06-17-dev-knowledge-architect-2` bundle.** The
> state moved across a heavy 2026-06-18 workday: **ADR-87** (the architect/CC equilibrium contract) was
> ratified + codified; the **coherence-spine consolidation** landed (#172 *closed*, its v2 roadmap
> *extracted* into **#179–#183** — the operator's "extract before close" first-action from the prior
> filled supplement); a **backlog groom** condensed the giants + filed #187–#189; the **worktree /
> parallel-arc lifecycle** was codified in PLAYBOOK; and the floor/schema machinery advanced (#120 +
> #138 closed, #167 multi-serialize-group landed, #186 floor-gap filed). Orient first (`PROBES.md` P1),
> **then ask the operator for off-repo context** (§13d — **per the UPDATE banner the supplement was
> FILLED, so this beat NARROWS to "anything changed since the supplement?"**; see §2), then resume the
> design.
>
> **This bundle was *generated* a v5.2 cold case — then FILLED (see the UPDATE banner at the top).**
> Generation-time history: it was generated cold (fresh CC session, no outgoing browser holding *this*
> window's deliberation), `SUPPLEMENT.md` committed with empty ANSWERS. v5.2 makes that defined, not a
> gap — **and** the operator then `supplement filled` real answers, so the live truth is **warm**: the
> folded ANSWERS carry the operator's strategic *why* (the unify-into-a-self-enforcing-whole goal — see
> the UPDATE banner) and the incoming §13(d) beat **narrows** to "changed since the supplement?". Read
> the folded answers first.

---

## 1. Drift-flags — the headline (this time: **one actionable re-drift + one benign carry**)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90, plus CC's
state read at generation). **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (17/20 pass; 2 `[--]` n/a + 1 `[~~]` informational — health exits OK). Re-derive at
read-time (P2–P9).

### DRIFT — `pytest_collected@ARCHITECTURE.md` **RE-DRIFTED**: doc=587 vs live=614 *(actionable — fix owed)*

`validate_doc_claims` reports `pytest_collected@ARCHITECTURE.md` as **doc=587 / actual=614** — a real
mismatch. The 2026-06-18 window added ~27 tests (the #120 child-BACKLOG probe +22, #167 serialize-group
+3, the equilibrium/floor work) and the `**N collected**` claim in `ARCHITECTURE.md` was **not**
re-bumped. This is the **same drift class** the `2026-06-17-dev-knowledge-architect` bundle headlined
(then doc=511 vs live=534) — it re-drifts on every test-adding window unless the doc is re-stamped.

- **Why it does NOT block the commit (and why this handoff did not "fix" it):** `audit.py health`'s
  *integrated* `doc_claims` gates only **3 of the 4** claims (`audit_check_count`, `precommit_hook_count`,
  `precommit_hook_roster`) — it does **not** gate `pytest_collected`. Only the **standalone**
  `validate_doc_claims.py` (probe **P6**) surfaces it, and that script is **not** a pre-commit hook. So
  "health: OK" is **not** proof the count is clean — P6 re-derives it. The correct fix is a *count bump
  **+** a `last_reviewed` re-stamp*, and the freshness cadence forbids re-stamping `ARCHITECTURE.md`
  without a **genuine end-to-end re-read** (a handoff is not one); a count-bump *without* the re-stamp
  would itself trip the `canonical_freshness` gate (stamp predates last edit). So this is a proper
  **next-session fix** (re-read → bump 587→614 → re-stamp), surfaced here, not silently half-done.
- **Confirm:** `python scripts/validate_doc_claims.py` (the `pytest_collected` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77 legitimately
  stays open. Direction-(a) #90a structurally cannot distinguish a misattributed closure from a real
  one; only arc-content inspection (**#139** / direction-(b)) can. Re-verified again this window in the
  #167-closure session (#5/#77 both **NOT** closed on content grounds — see JOURNAL 2026-06-18).
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### STATE — `main` is **in sync** with origin; **no merged stragglers** this time

`git status -sb` reports `## main...origin/main` (in sync at generation). `git branch --merged main`
shows **only `main`** — the prior bundle's two merged handoff stragglers were `-d`'d. The only other
branch, `automation/fleet-audit`, **never merges to main by design — ADR-84**, NOT a loose end.
**This handoff's own branch** `docs/handoff-2026-06-18-architect` merges on completion and **puts
`main` ahead of origin until pushed** (push is the operator's call — the serial-push gate). Re-derive
at read-time — `git status -sb` + `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The arc this window: the architect/CC division of labor became doctrine, and the coherence-spine
roadmap was made durable.** Four linked things landed across 2026-06-18 [recall/inferred via JOURNAL +
audit state]:

- **ADR-87 — the architect/CC equilibrium contract (the window's headline *way-of-working* ship).**
  STEP 3 of the equilibrium arc codified the prompt division of labor that follows from the STEP-1
  self-load finding (*CC self-loads context reliably **only for code-impact tasks**; read-only / GAP-1,
  execution-gotcha / GAP-2, governance / GAP-3 are unreliable — so an intent-only prompt is
  **conditional**, not universal*). **ADR-87 (Accepted, Path A)** is the canonical home: the **architect
  emits** intent + closure + anti-patterns + plan/auto mode + a thin per-task **governance-pointer**;
  **CC owns** code-impact context, generic gotchas, the skeleton (now reframed as CC's *consumption-spec*),
  model/effort. Carried into four durable surfaces (PLAYBOOK §2, `templates/prompt-template.md`,
  ESSENTIALS, `HANDOFF_BOOT.md`). The empirical close is **#184** (demonstrate on a real build — stays
  OPEN; codification ≠ demonstration); the GAP-2 residue is **#185** (a deterministic gotcha-injection
  PreToolUse guard — filed, *not* built, because prose can't fix an execution-time micro-decision class
  that recurred n=2/n=3 even with the standing "check gotchas" line). **Pointer:**
  `docs/decisions/ADR-87-equilibrium-contract.md` + JOURNAL 2026-06-18 "equilibrium contract STEP 3".
- **Coherence-spine consolidation — the prior bundle's load-bearing first-action, executed.** The prior
  `…-architect-2` filled supplement's *critical first backlog action* was: **extract #172's v2-deferred
  items into their own IDs BEFORE closing #172, or the roadmap orphans.** This window did exactly that —
  the v2 roadmap was extracted into **#179–#183** (a **new `coherence` serialize-group**: #179 AGENT-11
  undeclared-edge scan, #180 transclusion engine [gated on DEC-04], #181 nudge-response [data-gated],
  #182 folder-level contracts [DEC-07], #183 reparent #169/#171/#166 [evidence-gated]), and **only then**
  was **#172 closed** via the operator-gated `/review-closures` loop. The coherence doctrine now has a
  durable task-graph home. **Pointer:** `BACKLOG.md` `coherence` group + JOURNAL 2026-06-18 entries
  "#172 v2-roadmap extract" + "close #172".
- **Backlog groom — operationalizing "make the backlog genuinely load-bearing" (the supplement's #1
  intent).** Applied the approved 2026-06-18 groom: **closed #138** (done-undetected), **condensed** the
  giants (#159/#164 + a lighter set, ADR-65 history→git, ADR-83 LIVE constraint on #164 preserved
  verbatim), **pruned** the grooming log to a git-pointer, **absorbed 8 findings**, **filed** #187
  (dedup-on-entry) / #188 (deny-rule + hook completeness audit) / #189 (`~/.claude` commit-check,
  execute-elsewhere). Net 80→83 tasks, 0 warnings. **Pointer:** `BACKLOG.md` + JOURNAL 2026-06-18
  "apply approved backlog groom".
- **Worktree / parallel-arc lifecycle — a way-of-working gap-fill (W1).** Codified the worktree
  discipline **in place** (PLAYBOOK §"Parallel sessions & worktree discipline", *not* a new doc — the
  lifecycle was ~80% already documented). **Empirically verified the load-bearing premise** the
  `seed-state-yaml` memory had wrong: native `claude --worktree` **auto-seeds** all 5 `ecosystem/*/state.yaml`
  (incl. the dot-prefixed hub) and `audit.py health` returns OK from inside the worktree — the seed-block
  is the **raw `git worktree add`** path, which does not honor `.worktreeinclude`. **Pointer:** PLAYBOOK
  §"Parallel sessions & worktree discipline" + JOURNAL 2026-06-18 "W1".

**The design tensions now on the table** [recall/inferred]:

- **(A) "File-oriented dependency management" — the paradigm is roadmapped but still un-named as
  doctrine.** The prior filled supplement was explicit: **"Name it — as an ADR, not a VISION"** (a VISION
  invites the maximalism just resisted; an ADR earns the proven-in-miniature mechanism a decision-record
  + a coherent frame so v2 reads as "extending the paradigm" not ad-hoc feature-adding). This window
  delivered the *durable v2 task-graph* (#179–#183) but **not** the capstone ADR — so #179–#183 currently
  read as a loose feature list, exactly the failure mode the supplement warned against. **This is the
  candidate top thread** (§3 Q1).
- **(B) The architect/CC division of labor is now a *codified* invariant (ADR-87) — but unproven.** STEP 3
  is the codification; the contract has **never been exercised on a real build** (#184). The open
  way-of-working risk is whether the conditional intent-only prompt actually holds in practice, and
  whether GAP-2 (the execution-time micro-decision) genuinely needs the deterministic guard (#185) or
  whether the prompt contract covers it. See §3 Q4.
- **(C) The backlog-load-bearing intent is being lived, not just stated.** The supplement's #1 intent
  ("the architect drives from the backlog and delegates; freewheeling is the anti-pattern to kill") is
  now visibly operationalized — the groom + the #172/#167/#120 operator-gated closures + the durable
  task-graph (#156/#167 multi-serialize-group). The open question is whether **#168** (promote ADR-85's
  BACKLOG leg from advisory → hard, depends-on #170) should now be sequenced to make it *enforced*, not
  just practiced. See §3 Q7.
- **(D) PLAYBOOK Move 2 — maintainability, not parallelism (unchanged, still Council-bound).** The
  structural split → thin `§N`-index + per-section modules is justified on **maintainability** (the
  PLAYBOOK is ~3.5× the read-cap, frequently edited), **not** parallelism. Council-bound: the §1–§19 spine
  is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so the split must preserve §N
  addressability. See §3 Q5.

### A surfaced doc-vs-practice reconcile (do not lose)

- **§7 review-command canon — the graduated rule the prior supplement specified did NOT land.** The
  prior `…-architect-2` filled supplement (answer B) resolved the `/codex-review` vs `/code-review` drift
  to a **graduated rule**: interim / small → `/code-review high`; final pre-merge (3+ files) →
  `/codex-review` (independent GPT lens — confirm Codex auth mode first). **PLAYBOOK §7 still names a flat
  `/codex-review` for "3+ files / safety-critical"** (lines ~569, ~1651) — the graduated rule was never
  encoded. A `/review` vs `/codex review`-class doc-vs-practice drift — **surfaced for reconcile**, not
  silently resolved. (Also still live, flagged-not-fixed: `CLAUDE.md` §8 says "No repo-level skills
  directory exists yet" while `.claude/skills/verify/` + `.claude/skills/check-against-spec/` now exist —
  a doc-claim the coherence spine itself could eventually cover.)

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The live questions:

- **Q1 — name "file-oriented dependency management" as an ADR (the top candidate thread).** The prior
  supplement's explicit directive. Open: (i) author the **paradigm ADR** (decision + principles
  — coherence-by-mechanism; deterministic trigger + AI per-site verdict + human signature;
  graph-in-repo-not-model; narrow-first; the §16 do-not-build list as *part of* the doctrine — + the v1
  proof + the distilled roadmap); (ii) **which coherence-by-memory failure classes** the spine covers next
  and **in what order** (the supplement's priority sketch: more `reconciled_with` edges → graph-from-
  frontmatter / cross-repo → removal-via-transclusion → content-hash floor → undeclared-edge inference →
  intra-file + whole-graph sweeps). **Pointer for the *why*:**
  `docs/handoffs/2026-06-17-dev-knowledge-architect/SUPPLEMENT.md` (the verbatim answers) +
  `…-architect-2/SUPPLEMENT.md`.
- **Q2 — coherence v2 (the durable #179–#183 graph).** #181 (nudge-response: escape-hatch / deferred-hash
  / promote-nudge-to-gate) is **data-gated** on `logs/coherence-nudge.log` — read the log before deciding
  (the supplement's lean: *promote-to-gate if the nudge fires accurately + rarely; escape-hatch/deferred-hash
  only if noisy*). #180 (transclusion) is **gated on DEC-04** (lead-with-removal vs detection — unresolved).
  #182 (folder contracts) is gated on DEC-07. #183 (reparent #169/#171/#166) is **evidence-gated** (≥2 real
  drifts + a #169-fit decision — a deliberate gate, *not* an oversight; do not reparent yet).
- **Q3 — §7 review-command graduated rule (a doc-vs-practice reconcile, not yet a tracked task).** Encode
  the supplement's graduated rule in PLAYBOOK §7 (interim → `/code-review high`; final pre-merge 3+ files →
  `/codex-review`); confirm Codex auth mode first (ChatGPT-authed = no extra cost; API-key = bills per
  token → flip toward `/code-review` or switch auth). Surfaced in §2; not yet a `#id`.
- **Q4 — ADR-87 demonstration + the GAP-2 guard.** **#184** (demonstrate the equilibrium contract on a
  real build — the empirical close, OPEN) and **#185** (the GAP-2 deterministic gotcha-injection PreToolUse
  guard — filed, not built). Open: whether #185 is genuinely needed once #184 exercises the contract, or
  whether the prompt contract subsumes it.
- **Q5 — PLAYBOOK Move 2 (Council-bound, unchanged).** Structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the consumer
  API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 / #146** (the
  playbook serialize-group).
- **Q6 — handoff-machinery residue.** **#164** (implement the v5 generator — replace the SUPERSEDED v4
  8-file mechanics still in `.claude/commands/handoff.md`; must emit the v5.2 **always-file** `SUPPLEMENT.md`
  + seed each repo's `docs/handoffs/README.md` runbook; **ADR-83 LIVE constraint must survive** — v4
  templates stay live for corp-monorepo until the v5 cross-repo generator lands). **#159** (the *incoming*
  §13(d) beat — its only-remaining clause; the fill→fold half is dogfooded). **#162** (architect actor-vs-mode
  vocab — disambiguate atomically, do not leave the collision live). **#161** (stable probe-core + the
  orientation probe — *capture-only*; **note this bundle is again a hand-assembled probe set**, the
  persisting capture point).
- **Q7 — the ADR-85 enforcement chains + the load-bearing-backlog escalation.** **#170 → #168** the
  traceability spine (issue-ID↔commit anchor — the always-warranted link that promotes ADR-85's BACKLOG
  leg from advisory to a **hard** gate). **#171 → #169** the conformance dashboard (`ecosystem/conformance.md`,
  ADR-86 — now unblocked by the locked `Finding` format). *Connection to Q1:* the coherence `reconciled_with`
  edge model is a **sibling** of the traceability edge — whether #170 reuses it is an open design link.
- **Q8 — ADR-85 standing governance obligation (a watch, not a design question).** The gate is **live**. A
  **4-week scope-freeze runs to ~2026-07-14**; watch `logs/OVERRIDES.md` for override-rate (**>~10% → tune
  the rules**). Surfaced so the next session doesn't re-open ADR-85's shape mid-freeze.
- **Q9 — #186, sync #156 task-graph checks into the distributed plugin floor.** The hub's `validate_backlog.py`
  carries the #156 depends-on reference-existence + no-cycle checks; the **distributed plugin floor**
  (`plugins/tier1-lifecycle/scripts/validate_backlog.py`) carries only the ADR-66 structural checks, so a
  child's installed `validate-backlog` hook would NOT catch a dangling edge / cycle. The #120 probe is
  **floor-faithful** (mirrors the floor as-shipped, deliberately does not compensate), so the gap is tracked
  here — do **before/with** distributing `validate-backlog` to children.

**Resolved this window (do NOT re-open):** #172's v2 roadmap **extracted** (→ #179–#183) + #172 **closed** ·
the equilibrium-contract **codification** (→ ADR-87 STEP 3; only the *demonstration* #184 remains) · #167
multi-serialize-group schema (→ closed) · #120 child-BACKLOG conformance probe (→ closed) · #138 floor
INSTALL_NOTE gitignore-negation (→ closed) · the worktree/parallel-arc lifecycle (→ codified in PLAYBOOK,
native auto-seed verified).

---

## 4. The task-graph (durable hard edges — #156 shipped)

#156 shipped — **hard edges are DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. Point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b).

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** **11 serialize-groups**
  at generation. The **handoff** group = `{#1, #26, #159, #161, #162, #184, #164, #10}` (**#184 added** this
  window — the equilibrium-demo). The **coherence** group = `{#179, #180, #181, #182}` — **NEW this window**
  (the extracted #172 v2 roadmap; #183 is bare). The **audit-py** group = `{#153, #7, #36, #95, #140, #139,
  #166}` (**#172 removed** — closed this window). The **playbook** group = `{#146, #77, #67, #18, #39}`. The
  **architecture** group = `{#165, #35}`. (Plus `claude-md {#112,#157}`, `claude-md-template {#17,#109}`,
  `environment {#71,#119}`, `pre-commit-config {#15,#132}`, `settings-json {#116,#117}`, `validate-backlog
  {#187}` — see the validator's full summary line.) Hard precedence edges (`depends-on`): **#168 → #170**,
  **#169 → #171**. Parallel-safety is **derived** (no shared group + no `depends-on` path).
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q1 (name the paradigm ADR) is the top candidate thread** — but it is *not* a schema edge: #179–#183
    are durably grouped, the **capstone ADR is the soft "frame" they hang off**, carried here as judgment.
  - **#181 (Q2) is the data-gated one** — not schedulable until `logs/coherence-nudge.log` has firing signal.
  - **#184 (Q4) is the ADR-87 empirical close** — serializes within the `handoff` group; closes on the next
    real build that exercises the contract.
  - **#164 (Q6) is the last big handoff-machinery item** — serializes within the `handoff` group; must emit
    the v5.2 always-file `SUPPLEMENT.md`.
  - **#170 (Q7) unblocks #168**; the coherence `reconciled_with` edge is a *sibling* of the traceability
    edge — a possible reuse, surfaced as a design connection, not a schema fact.
  - **Move 2 (Q5) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the playbook
    serialize-group.
  - **#186 (Q9) is independent** — sync the #156 checks into the plugin floor before distributing.

(The "candidate-thread / unblocks / sibling" framing is residual judgment; the serialize-group +
`depends-on` edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes — the coherence work is now its own `coherence` group
  (#179–#183) + #183 bare; the handoff group (#159/#161/#162/#164/#184); the audit-py group (#166/#139 +
  the closed-out #172 gone); the playbook group (Move 2 / #39); the floor/distribution items (#186). Do
  **not** trust any re-narrated ID text — open the live BACKLOG (the §2/§3 text is recall; the file is
  truth). `validate_backlog`: **83 tasks, 0 warnings, 7 themes, 20 stories, 11 serialize-groups** at
  generation.
- **Live branches at generation** (`git branch -v`): `main` (**in sync** with origin at generation; this
  handoff's own commits put it ahead until pushed); `automation/fleet-audit` (**never merges to main by
  design — ADR-84**, NOT a loose end). **No merged stragglers** — the prior bundle's two were `-d`'d. This
  handoff's own branch `docs/handoff-2026-06-18-architect` merges on completion.
- **Drift-flags:** **one actionable** — `pytest_collected@ARCHITECTURE.md` doc=587 vs live=614 (re-drifted,
  fix owed — §1) — plus the **carried-benign** `git_backlog_drift` #90a `[~~]` (#77). `main` in sync; no
  stragglers. Re-derive: `python scripts/audit.py health` + `python scripts/validate_doc_claims.py` +
  `git status -sb` + `git branch --merged main`.
- **Audit-gating note (load-bearing):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** v5 bundle. `2026-06-18-dev-knowledge-architect` is now lexically-max → it **is** this
  check's target (superseding `…-architect-2`). Its 10 probes were verified to bind via
  `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-18-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **`pytest_collected` fix owed** — the headline (§1): re-read `ARCHITECTURE.md` → bump 587→614 →
  re-stamp `last_reviewed`. A next-session doc-coherence fix (not this handoff's, per §1).
- **17 closure proposals** await — `/review-closures` (human-gated, done-items-leave). Re-verify the
  STRONG candidates' evidence SHAs before closing (#5/#77 are the known false-positive/voided pair).
- **changelog drift** — `claude-code 2.1.181 > last reviewed 2.1.177` — `/changelog-review`.
- **nightly may have silently skipped** — the SessionStart reminder flagged the expected
  `docs/audits/2026-06-18-conformance-nightly-digest.md` is **NOT** on the `automation/conformance-digest`
  branch (no retry). Worth a look — not a handoff artifact.
- **10 nightly triage findings** await (#37, #35, #33, #31, #29, #27, #25, #23, #21, #19 — Issues tab).
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **`main` will be ahead of origin after this handoff's commits** — push is the operator's call (the
  serial-push gate). At generation `main` was in sync.
- **ADR-85 override-rate watch** — `logs/OVERRIDES.md`; scope-freeze to ~2026-07-14 (§3 Q8).

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (v5 §5 + §13c)
<!-- scope: meta -->

> **⚠ UPDATE (post-generation) — supplement FILLED.** This bundle was generated cold, but the
> operator then `supplement filled` real answers (see `RESIDUAL.md` UPDATE banner). The teeth probes
> (P2–P9) are **unchanged** — they bind to **live state**, which the fill does not touch. The only
> change is the **§13(d) beat in P1's gate: it now NARROWS to "anything changed since the
> supplement?"**, it does **not** fire full. Read any "cold / empty ANSWERS / beat fires full"
> phrasing below as generation-time history; read the folded `SUPPLEMENT.md` answers first.

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
>
> **This bundle is COLD** (fresh CC session; `SUPPLEMENT.md` committed with empty ANSWERS), so the
> §13(d) operator-context beat in P1's gate **fires FULL** — there is nothing to narrow against. The
> *prior* bundles' **filled** supplements carry the operator's most recent strategic *why* (pointers
> in `RESIDUAL.md` §2/§3); read them as context, then the beat asks the live off-repo question.

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
§2), so the beat **fires FULL** — there is no prior-supplement answer to narrow against this session.
Read the *prior* bundles' filled supplements first (the most recent strategic *why*), then ask the
full off-repo question.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `62763d7`, the tree was clean, and `main` was in sync — but this handoff's own commits put `main` ahead until pushed, and HEAD/sync move on any commit, push, or fetch; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, what does `pytest --collect-only` collect **right now**, and **do they match**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual — and unlike a clean window, this probe is **expected to MISMATCH** at generation (doc=587 vs live=614, the re-drift headline §1), but the live count is still the only ground truth | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) — note: `audit.py health` does **not** catch this; use the standalone |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is a `SUPPLEMENT.md` present (and is its ANSWERS region empty or filled), and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count (the 2026-06-12 collapse dropped the per-bundle README; the four-file `PASTE_THIS` shape + the v5.2 **always-generated** `SUPPLEMENT.md` are live); the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-18-dev-knowledge-architect/` (no `README.md`; `SUPPLEMENT.md` present, **ANSWERS FILLED** post-generation — see the UPDATE banner; boilerplate lives once in `docs/handoffs/README.md`) ∩ `HANDOFF_PROCESS.md` §13 |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`s are in the **handoff** group, and which **new** group did the extracted #172 v2 roadmap form? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit (a new `coherence` group formed + `#172` left `audit-py` this window); it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask, **firing FULL**
   this bundle (it is cold — empty ANSWERS; read the *prior* filled supplements first for context) —
   before design. Then run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P2/P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. **P6 is expected to MISMATCH at generation** (doc=587 vs live=614, the §1 re-drift) — but the
   pass criterion is **"answered from the live source,"** never "matches the value the summary
   remembered." P2 is expected to read **20** (no check landed this window); P8 pins the post-collapse
   four-file shape (+ the v5.2 always-generated `SUPPLEMENT.md`, **empty ANSWERS** — cold; no README); P9
   pins the now-durable serialize-group graph (#156) with the **new `coherence` group** (#179–#182) and
   `#172` gone from `audit-py` (closed).

---

=== SUPPLEMENT.md ===

ANSWERS — 2026-06-18 architect handoff

1. Strategic intent.
Unify and encapsulate the way-of-working methodology into ONE coherent, SELF-ENFORCING whole, deployable to a fresh repo — with #131 (ai-council onboarding) as the first deployment test. The methodology already EXISTS and is mature (the story-map backlog passes validate_backlog 0-warnings; ADR-87 equilibrium contract; handoff §13 architect/execution; worktree lifecycle ~80% codified). What it is NOT yet: a whole that composes into one articulable, enforced process. This session repeatedly showed the architect BYPASSING the methodology because the pieces are scattered and rely on REMEMBERING to apply them. Goal: enforcement > documentation — close the memory-dependence gaps so correctness is held by machinery, not by the architect's memory.

2. Tensions weighed.
(i) Architect-emits-intent vs architect-structures-the-artifact → landed on intent-only (ADR-87), because this session proved the failure of over-reaching into CC's lane (hand-built flat orphan backlog tasks that violated the schema + duplicated #106). (ii) Mode as simple plan/execute vs the full CC permission taxonomy → landed: the architect emits plan/execute; permission posture (bypass/acceptEdits/auto) is the OPERATOR's terminal call, outside the contract — the right abstraction level for each actor. (iii) Backlog: invent methodology vs follow the existing one → the methodology exists (ADR-66); the failure was adherence + a 6-week grooming-cadence lapse, fixed by the groom. (iv) grooming-log archive-file vs git-pointer → git-pointer (archive-file violates §5).

3. Considered + rejected (do NOT relitigate).
- Encoding the mode model as a large PLAYBOOK §2 + HANDOFF deliverable — rejected as over-engineering (the contract + §13 already exist; residual = a clause in #106).
- Routing the mode clarification to AI Council — rejected (it is a small clarification, not an architecture decision).
- Archive-file for the grooming log — rejected (§5).
- Re-archiving the v4 handoff templates — NOT done (they are LIVE for v4 repos per ADR-83; re-archival is gated to #164 close).
- Filing the 8 findings as flat new tasks — rejected; re-mapped (mostly folded into #106/#130/#153/#179/#140; only #187/#188/#189 are genuinely new).
- Standalone condensation-gate — rejected (folded into #140).
- Semantic/LLM dedup in the validator — rejected (validators are deterministic; #187 is a token-overlap heuristic with an explicit stated limit).

4. Open questions / deferred.
(a) The "file-oriented dependency management" capstone ADR is unbuilt — #179-#183 read as a loose feature list, not "extending a paradigm" (see A). (b) #184 (demonstrate ADR-87) vs the §7 review-command reconcile — sequencing + Codex auth-mode cost (see B). (c) Auto Mode go/no-go (#106) now carries the mode-disambiguation clause, but the go/no-go itself + the auto-vs-bypass operator-default recommendation are unresolved. (d) The enforcement gaps (#187 dedup, #140 grooming-gate, #188 deny/hook audit) are filed but unbuilt — these are the "machinery not memory" closures the unify-goal depends on.

5. Decomposition rationale — what NOT to redo / re-decide.
The backlog methodology is SOUND (validate_backlog conformant) — do not "fix" it; the issue was adherence + cadence, both addressed. The mode model is settled (architect: plan/execute; posture: operator terminal call) — do not relitigate the permission taxonomy as an architect concern. ADR-87 needs DEMONSTRATION (#184), not redesign. The worktree lifecycle is codified (d102d63, native .claude/worktrees/) — do not re-propose the sibling-dir path (superseded). The ~/.claude backup is done (private remote). The 8 findings are absorbed — do not re-file them.

6. Off-repo context.
Operator's top priority: unify + encapsulate the methodology into a deployable whole, with #131 as the test. Dominant off-repo finding (not in the repo): the methodology is good but NOT self-enforcing — the architect bypassed it repeatedly this session (flat-orphan filing, mode over-scoping, "closed"-without-delivery, an archive-file instruction violating §5); the pattern is the session's named spine-failure — "accepting inherited framing without verifying against state." The unify-goal must therefore prioritize ENFORCEMENT (machinery that can't be bypassed), not more docs. Two rough methodology areas this session (operator-flagged), both captured: mode (→ #106/#162) and parallel-work management (→ d102d63 + #143/#145). Client-data lesson: client-identifying context leaked into a gotcha via verbatim capture (Würth, now generalized + a #130 capture-scrub arm) — watch for this in any cross-repo deployment. Operator auth: Max subscription; the empty ANTHROPIC_API_KEY override forces Max-OAuth (not API billing) and is load-bearing.

A. Capstone ADR — author now.
Yes — it directly serves the unify+encapsulate goal (it names the paradigm that #179-#183 extend, turning a feature list into doctrine), and the prior supplement already directed ADR-not-VISION. Suggested failure-class order (by this session's evidenced frequency/cost): (1) accepting inherited framing without verifying state (the spine-failure), (2) cross-document staleness via undeclared prose-dependency edges (#179), (3) duplicate/uncoordinated filing (#106→#187), (4) history-accretion bloat (#159/#164→#140). Caveat for the incoming architect: the taxonomy/order is itself a design choice — verify against the actual #179-#183 scope before locking it.

B. Sequence — #184 first.
The unify-goal depends on ADR-87 being PROVEN, not just codified; #184 is that proof, and #131's onboarding is a natural real-build to demonstrate it on — so #184 rides #131. The §7 graduated review-command rule (interim → /code-review high; final pre-merge 3+ files → /codex-review) is a smaller encoding that can ride along. Codex auth: ChatGPT-authed (no extra cost) is the default-sensible choice given the Max subscription + the no-budget-ceiling-but-optimize-later posture; API-key (per-token) only if ChatGPT-auth is insufficient — confirm with the operator, since it affects the cost of every /codex-review.
