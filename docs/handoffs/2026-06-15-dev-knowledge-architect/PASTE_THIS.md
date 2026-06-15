=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-15-dev-knowledge-architect` |
| **Mode** | **architect** (v5 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff at the close of the **modularization arc** — not a carry-forward refresh. The 2026-06-13 architect theme ("finish the v5 handoff machinery deferred at the #149 flip") **largely landed since**: #163 teeth validator shipped, #156 durable task-graph shipped + ADR-66 ratified, Q9 resolved by ADR-84 (automation-writer isolation), PLAYBOOK Move 1 pointerized, collision graph encoded. The **two queued Council-bound design threads** are now the work: **(A) the hybrid handoff design** (handoff = CC repo-bundle *facts* + architect strategic brief *judgment* — demonstrated by today's `-session` bundle) and **(B) PLAYBOOK Move 2** (the structural split). The last machinery build item, **#164 (the v5 generator)**, is still open — every bundle, including this one, is hand-assembled. |
| **Generated at** | HEAD `ea9f190`, working tree clean, `main` **in sync** with `origin/main` (no ahead/behind — a change from both prior bundles; the 2026-06-15 push reconciled the gap). Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

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
  Architect mode only.
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

---

=== RESIDUAL.md ===

# Residual — 2026-06-15 session, **architect mode** (v5 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph**. Drift-flags are the headline — and this time the
> headline is **clean** (§1). Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md`
> and the now-**durable** serialize-group graph (#156 shipped), not re-narrated IDs. Generated from
> inside the repo at HEAD `ea9f190`, working tree clean, `main` **in sync** with `origin/main`.
> Re-derive HEAD/sync at read-time (P3).
>
> **Provenance — reconstructed, not witnessed-live.** This session was `/clear`ed immediately before
> the handoff, so there is **no live session reasoning** to transmit. The planning "why" below is
> **reconstructed from the repo** — JOURNAL (last ~8 entries), BACKLOG, the 2026-06-13 `-architect`
> bundle, and today's `2026-06-15-dev-knowledge-session` bundle (whose §2 embedded the architect
> brief verbatim — the richest source of the planning judgment). State facts (§1, §5) are
> **witnessed** (verified live at generation); design framing (§2–§4) is **recall/inferred** from
> those sources — verify against the live BACKLOG (§5), do not trust the re-narration.
>
> **Scope — a fresh handoff at an arc boundary, not a refresh.** Unlike 2026-06-13 (an honest
> carry-forward "no design move landed"), the state has moved **decisively** since: the entire
> 2026-06-13 Q-set is largely **resolved** (§3 "Resolved-since"). The modularization arc closed; two
> Council-bound design threads are queued. Orient first (`PROBES.md` P1), **then ask the operator for
> off-repo context** (§13d / #159), then resume the design.

---

## 1. Drift-flags — the headline (this time: clean)

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus CC's
state read at generation. **A flag is a question, not a verdict.** `audit.py health` is **OK** at
generation (18/19 pass; the one `[~~]` below is informational — health exits OK). Re-derive at
read-time (P3/P4/P7).

### CLEAN — `main` is **in sync** with `origin/main`; `no_ff_merges` is **OK** *(the two prior bundles' headlines are both gone)*

The 2026-06-13 `-architect` bundle's headline was a `main↔origin/main` **divergence** (ahead 3 /
behind 1); today's `-session` bundle's headline was an **ahead-8 origin gap**. **Both are resolved.**
`git status -sb` reports a bare **`## main...origin/main`** (no ahead/behind) at generation — the
2026-06-15 push reconciled the gap. And `no_ff_merges` reports **OK** ("no non-merge commits on main
since 2026-06-15"), because **ADR-84 (automation-writer isolation, 2026-06-14)** moved both unattended
writers off `main` (`automation/fleet-audit` local-first + `automation/conformance-digest` on origin)
and removed the `no_ff_merges` exemption — so the **Q9 collision is resolved by design, not carried**.

- **Confirm:** `git status -sb` (in sync) + `python scripts/audit.py health` (the `no_ff_merges` line).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable — carried)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed
  closure from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py`.

### OPERATIONAL ALERT — last night's **nightly may have silently skipped** *(not a drift-flag; an ADR-84-pipeline reliability signal — operator look owed)*

The SessionStart surfacing reported: the expected digest `docs/audits/2026-06-15-conformance-nightly-digest.md`
is **NOT** on the `automation/conformance-digest` branch — *"last night's nightly may have silently
skipped (no retry)."* This is the cloud-Routine conformance pipeline (ADR-84). **Not a way-of-working
design question; an operator check** — was the 2026-06-15 Action run skipped/failed, and does the
no-retry posture want hardening? Surfaced so it is not lost. **Confirm:** the GitHub Actions run for
`nightly-conformance-triage.yml` + `git log --oneline origin/automation/conformance-digest`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The theme shifted — the machinery is (almost) done; the design threads are the work.** The
2026-06-12/06-13 architect theme was *"finish the v5 handoff machinery deferred at the #149 flip."*
Since 2026-06-13 that theme **largely landed** [witnessed via JOURNAL + audit state]:

- **#163 — teeth validator shipped** (`scripts/verify_handoff_probes.py`, merged `dba11d0`
  2026-06-13; now `audit.py` check #19 `handoff_probes`, resolve-only). The manual probe-gate every
  prior bundle leaned on is now **mechanically enforced** on the active bundle.
- **#156 — durable task-graph shipped** (BACKLOG schema carries `serialize-group` / `depends-on`,
  enforced in `validate_backlog.py`) **and ADR-66 ratified 2026-06-14** (operator authority, Path A).
- **Q9 — resolved by ADR-84** (automation-writer isolation): both unattended writers moved off `main`;
  the `--no-ff`-universal × ADR-80-automation-writer collision is closed by design.
- **PLAYBOOK Move 1 pointerized** (#152 + #158): 4 of 5 playbook-cluster tasks left the serialize-group;
  the token-log cadence relocated to `HANDOFF_PROCESS §14`. PLAYBOOK 3288 → 3211 lines.
- **Collision graph encoded** (2026-06-14): 34 tasks annotated across 9 serialize-groups; the
  parallelizable surface **re-measured on real data** (hub-internal N = 9). #167 / #166 filed.

**What that re-measure decided — don't build hub delegate-mode** [recall, from today's `-session`
§2 brief]. The data-grounded NO: *capacity ≠ demand.* The backlog's independent epics are sporadic
periphery; the sustained work (handoff / playbook / audit) lives in **contended-core serialize-groups
that serialize regardless of orchestration** — so a delegate fleet wouldn't speed the work actually
done. Delegate stays for **cross-repo (ADR-41) + research**. The real lever was **contention
reduction** (PLAYBOOK modularization), which is why Move 1 happened and Move 2 is queued. North-star:
the architect **owns the backlog across sessions** and **tracks a delegation ledger** (delegate where
independent, serialize where contended).

**The two design tensions now on the table** [recall/inferred]:

- **(A) The hybrid handoff — v5 has no formal slot for browser-authored judgment.** v5's residual is
  by spec **CC-authored and repo-derived** — it "structurally cannot carry operator intent or off-repo
  findings." Today's `-session` bundle **demonstrated** the hybrid by embedding the architect's
  strategic brief *verbatim* in the residual "why" §, but that placement is **ad-hoc** (the closest
  existing slot, not a designed one). The tension: facts transmit well, **judgment/priorities transmit
  poorly** — yet the architect role *is* judgment/priorities. See §3 Q-A and §4.
- **(B) PLAYBOOK Move 2 — maintainability, not parallelism.** Move 1 barely shrank the file (−2.3%)
  because most "duplicated" content was genuinely PLAYBOOK-canonical and correctly stayed. So Move 2
  (the structural split) is justified on **maintainability** (≈84k tokens, ~3.5× the read-cap,
  frequently edited), **not** parallelism. It is **Council-bound** because the `§N-index` design is a
  genuine fork — the §1–§19 spine is the **consumer API** (ESSENTIALS / CLAUDE.md reference by §N), so
  the split must preserve §N addressability. See §3 Q-B.

**The standing meta-argument:** every v5 bundle — **including this one** — is **hand-assembled** by CC
following the spec. That is exactly the drift-prone hand-maintained surface the methodology outlaws
everywhere else; it is the live case for **#164 (the generator)** and **#161 (the probe-core)**.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Re-profiled for this arc boundary. The 2026-06-13 Q1–Q11 set is **largely resolved** (see
"Resolved-since" below); the live questions are:

- **Q-A — the hybrid handoff design (Council-bound, NEW headline).** Formalize the handoff as **two
  authored components**: CC repo-bundle (*facts*) + architect strategic brief (*through-line +
  priorities + delegation state*). **Open:** v5 has **no formal slot** for a *committed,
  browser-authored* strategic section (today's §4 finding) — design one, and explicitly **reconcile
  with #159** (which chose the *in-session-ask* form and **rejected** a new-bundle-file), with **#161 /
  #162**, and with the residual's **repo-derived / off-repo boundary** so the two channels (CC residual
  + architect brief) are **complementary, not overlapping**. Demonstrated today; needs the Council
  design. (Substrate: today's `-session` `RESIDUAL.md` §2 + §4.)
- **Q-B — PLAYBOOK Move 2 (Council-bound).** The structural split → thin `§N`-index + per-section
  modules + per-module TOC/hook. **Open:** the `§N`-index design (preserve §N addressability — the
  consumer API). Maintainability-justified, not urgent. **Unblocks #39; decouples #18 / #67 / #77 /
  #146** (the playbook serialize-group).
- **Q-C — #164, the v5 generator (the last machinery item, L).** `.claude/commands/handoff.md` still
  carries the v4 8-file two-phase generator (marked SUPERSEDED); the v5 emissions are specified but not
  the wired generator. **Open sub-decisions:** (i) the **per-repo-runbook sync key** —
  write-if-absent-or-version-changed, but *keyed how* (handoff-process version? a content hash?) so a
  genuine runbook edit isn't clobbered and a stale one isn't left; (ii) the **cross-repo v4 routing**
  (ADR-83) — a v4 target repo (one lacking `scripts/audit.py`) needs a deterministic route to the v4
  Phase-1/2 path, since the v5 emissions can't bind a target with no audit checks to probe.
- **Q-D — #162, architect actor-vs-mode vocab.** Disambiguate "architect" the Layer-1 **actor**
  (browser-chat role) from "architect" the §13 **mode** atomically across every surface — rename one
  sense or formally scope both; do not leave the collision live.
- **Q-E — #159, operator-context beat (exercise in a real architect session).** The §13d beat landed
  in the canonical spec; the **only-remaining clause is exercising it in a real architect session** —
  **this session is the candidate** (the beat fires after orientation per the boot, step 6).
- **Q-F — #161, teeth probe-core.** Define a stable shared probe-core (the ~5 forced-read probes) + the
  architect orientation probe, so bundles **stop hand-assembling probe sets** per handoff. Capture-only
  (scoping is a future architect decision) — but note **this is again a hand-assembled probe set** (the
  persisting capture point).
- **Q-G — #166, doctrine_enforcement_coherence check (audit-py).** A read-only `audit.py` check
  flagging any ADR/amendment still `PROPOSED` / `NOT RATIFIED` while its implementing task is closed
  (live enforcement ahead of its doctrine — the #156 gap reconciled by hand on 2026-06-14).
- **Q-H — #167, multi serialize-group schema + parser anchoring.** `_parse_serialize_group` reads only
  the FIRST clause, so a task colliding on two surfaces can't be fully encoded — the 2026-06-14 pass
  dropped two real edges (#105↔#112 on `block_immutable_edits.py`, #5↔#77 on `ESSENTIALS.md`). Also
  **anchor the parser to clause position** so prose tokens can't self-trip it (the 2026-06-14 incident).
- **Q-I — #165, ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (operator-set
  2026-06-12; first applied when the runbook chose mermaid), awaiting ratification — not a unilaterally
  minted ADR. Record where the diagram convention lives once ratified. `serialize-group: architecture`.

**Resolved-since 2026-06-13 (do NOT re-open):** Q2/#163 (teeth validator — shipped `dba11d0`, audit
check #19) · Q3/#156 (durable task-graph — shipped + ADR-66 ratified 2026-06-14) · Q9
(automation-writer vs `--no-ff` — ADR-84 isolation) · Q1's runbook-collapse half (the canonical runbook
landed; the *generator* half persists as Q-C) · Q11 (nightly #26 dispositions — largely cleared; the
residual triage items folded into the operator queue, §6).

---

## 4. The task-graph (now **partly durable** — #156 shipped)

**The biggest change from 2026-06-13:** the task-graph is **no longer purely ephemeral prose.** #156
shipped — **hard edges are now DURABLE** in BACKLOG (`serialize-group` / `depends-on`), enforced
read-only in `validate_backlog.py`. So point at the **live encoding** as the graph; carry only the
**soft / provenance** relations as residual prose (spec §13b: "soft/provenance relations stay residual").

- **Durable (schema fact — re-derive via `python scripts/validate_backlog.py`):** 9 serialize-groups.
  The **handoff** group = {#1, #26, #159, #161, #162, #164, #10} — these **serialize** (do not
  co-schedule). The **playbook** group = {#146, #77, #67, #18, #39}. The **audit-py** group includes
  #166. Parallel-safety is **derived** (no shared group + no `depends-on` path), now a schema-checkable
  property, not a hand-wave.
- **Soft / residual reads (the architect's judgment, NOT schema facts):**
  - **Q-A (hybrid) and Q-B (Move 2) are decision items, not build items** — resolve via Council /
    ratification; parallel to each other.
  - **#164 (Q-C) is the last big build item** — `L`, gated on the Q-C(i)/(ii) decisions; pairs with the
    already-shipped #163 validator (its output is now mechanically checkable).
  - **Move 2 (Q-B) unblocks #39** and **decouples #18 / #67 / #77 / #146** — landing it dissolves the
    playbook serialize-group.
  - **#159 (Q-E) is exercisable THIS session** — off the build path.
  - **#166 / #167 are independent cleanups** — #166 serializes within the audit-py group; #167 is bare.

(The "decision-not-build / Council-bound / unblocks" framing is residual judgment; the serialize-group
edges are the schema fact. #156 made the *hard* edges durable, not these *soft* ones.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` themes **"Handoff continuity"** (the handoff group),
  **"Enforced governance"** (#166), and **"Tooling & evaluation"** for the live tickets. Do **not**
  trust any re-narrated ID text — open the live BACKLOG (the §3 text is recall; the file is truth).
  `validate_backlog`: **72 tasks, 0 warnings**, 9 serialize-groups at generation.
- **Live branches at generation** (`git branch -v`): `main` (in sync with origin); `automation/fleet-audit`
  (**never merges to main by design — ADR-84**, NOT a loose end); this handoff's own
  `docs/handoff-2026-06-15-architect` (merges on completion); and **three merged stragglers** —
  `chore/ratify-adr66-156-amendment`, `feat/encode-collision-graph`, `feat/playbook-pointerize-152-158`
  (already in main; **candidates for `-d` cleanup**, carried from today's `-session` §3, deliberately
  not deleted here — out of this handoff's scope).
- **Drift-flags:** only `git_backlog_drift` #90a `[~~]` (#77, known-benign/dispositioned). `main`
  **in sync** (no divergence, no origin gap). The nightly-skip alert (§1) is operational, not drift.
  Re-derive: `python scripts/audit.py health` + `git status -sb`.
- **Audit-gating quirk (note, not a problem):** `audit.py` check #19 `handoff_probes` validates the
  **lexically-max** bundle. For 2026-06-15, `"session" > "architect"`, so **today's `-session` bundle
  stays the audit-gated one** — this `-architect` bundle is **not** the check's target. Its probes were
  verified to bind separately via `python scripts/verify_handoff_probes.py docs/handoffs/2026-06-15-dev-knowledge-architect`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is operator-gated, not CC's to run
unprompted:

- **15 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.177 > last reviewed 2.1.168` — `/changelog-review`.
- **7 nightly triage findings** await — #31, #29, #27, #25, #23, #21, #19 (Issues tab).
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
- **nightly-skip alert** (§1) — the 2026-06-15 conformance digest is absent from
  `automation/conformance-digest`; check the Action run (no-retry posture).

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
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what `.dev-knowledge` is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits (Layer 2 of the ADR-28 three-layer model)*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read
live by CC, substring-matched. **Then, before design, the operator-context beat fires (v5 §13d):**
the browser asks the operator one targeted question for **off-repo** context (intent / priorities
/ findings not in the repo / changed decisions) — the channel the repo-derived residual cannot
carry. (Exercising this beat in a real architect session is the only-remaining clause of **#159**.)
Net: *readable-first is a verified property of the handoff, with zero content copied*, **then** the
off-repo steering is injected.

## Teeth probes (state fidelity — same contract)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands (#163's `handoff_probes` was the most recent); a summary rounds/omits both | `python scripts/audit.py checks` |
| P3 | What is the current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state; **at this generation HEAD was `ea9f190` and `main` was IN SYNC with `origin/main` (no ahead/behind)** — but HEAD/sync move on any commit, push, or fetch; **re-derive, don't trust this line** | `git rev-parse --short HEAD` (then `git status -sb`) |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the 9-char sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over post-handoff commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp (or `audit.py health` `canonical_freshness`) |
| P6 | What integer does `ARCHITECTURE.md`'s `**N collected**` claim state, and what does `pytest --collect-only` collect **right now**? | `ARCHITECTURE.md` `**N collected**` + live pytest | the live count drifts on any test change; neither integer appears in the residual | `python scripts/validate_doc_claims.py` |
| P7 | Does `audit.py health` flag a **`no_ff_merges`** WARN right now — yes or no — and if so what is the **full short-sha + date** of the direct-on-main commit it names? | live git ∩ `main` history | post-**ADR-84** the writers were isolated, so this is *expected clean* — but the live answer is the only ground truth (a new direct commit could appear); the value is absent from the bundle | `python scripts/audit.py health` (the `no_ff_merges` line) — re-derive; do **not** trust the residual's prose |
| P8 | Does a v5 handoff bundle carry a **per-bundle `README.md`** — and where does the stable operator boilerplate live instead? | `docs/handoffs/<slug>/` listing ∩ `HANDOFF_PROCESS.md` §13 | the 2026-06-12 collapse dropped the per-bundle README; a summary may still "remember" the four-file shape — the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-06-15-dev-knowledge-architect/` (three files, no README) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, and which `#id`s are in the **handoff** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | #156 made the task-graph durable, so the group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — one off-repo ask — before
   design. Then run P2–P9, each against **live state now** (not generation-time).
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor
   missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named
   primary source → CC re-derives the fact → abort if still unmet).
4. Probes P3/P4/P5/P6/P7/P9 are *expected to move* between generation and check-time — that is the
   design. The pass criterion is **"answered from the live source,"** never "matches the value the
   summary remembered." P8 pins the post-collapse three-file shape; P9 pins the now-durable
   serialize-group graph (#156).

---

=== SUPPLEMENT.md ===

To the incoming architect — supplement from the outgoing session.

The bundle is accurate and its facts are verified, but it was reconstructed from the repo after
this session was /cleared — so the why in §2-§4 is recall, not witnessed. Trust §1/§5 (state);
treat §2-§4 as faithful-but-secondhand and verify against live BACKLOG + JOURNAL if anything
load-bearing feels off. Here is the live judgment the reconstruction can't press hard enough:

1. You are the live test of the hybrid handoff — don't formalize it before you've taken it.
Q-A is demonstrated, not designed. The honest next step is not to Council it yet — it's to
notice, as you onboard, whether RESIDUAL §2 actually hands you the backlog priorities and
through-line so you can own them without re-deriving from facts. Your own onboarding is the
data: works -> light codification; leaves you re-deriving -> that gap is the Council input.
Observe first, design second.

2. Don't speculatively build — the hard-won lesson of the arc that just closed. That arc killed
a delegate-mode build on one principle: capacity != demand. Apply it forward to the nine open
questions. In particular: the north-star says "delegation to browsers," but that is demand-gated
— build the delegate mechanism when a real independent / cross-repo workload appears to farm
out, not because the north-star names it. Delegate where independent (cross-repo, research);
serialize where contended (the hub core). Nothing on the board forces a big build right now —
the live moves are validation (the hybrid) and opportunistic cleanup, on Rob's priority.

3. If Rob does want a build, #164 (the generator) is the principled one — because this very
bundle and its probe set were hand-assembled, the drift-prone surface the methodology outlaws
everywhere else (the bundle says so itself). #164 pays down standing risk rather than adding
capability. It's L and gated on the Q-C sub-decisions, but it's the build that makes the next
handoff not hand-built. (The operator-paste slice was just carved off and shipped; the
sync-key + cross-repo-routing remainder stays #164.)

4. The external loop/skills/memory discourse has been scanned — it validates our foundations,
it does not redirect them; don't re-litigate it. The current X-thread orthodoxy ("stop
prompting, write loops"; skills-as-files; Copilot's cited-and-reverified memory; loss-function
development; the ant / Managed-Agents platform) describes patterns we've largely built
independently — and on the three that matter (verification gates, memory-on-disk, governed
skills) we are ahead. Copilot's read-time verification is our PROBES. The autonomous-loop thesis
is the least applicable to our work, for the exact reason the arc killed delegate-mode: it fits
mechanical, schedulable, rubric-checkable work — not judgment-heavy governance — and we already
run loops where they fit (nightly conformance, outcome management). The scan surfaced only two
narrow, demand-gated candidates, both file-not-build: (a) nightly-pipeline reliability — the §1
silent-skip, the most acute candidate because something actually broke; a retry/alert mechanism
beats Managed-Agents complexity; (b) evaluate read-time-verification for LESSONS — verify it
adds anything over canonical-freshness / amendment-coherence / #166 before building, it may be
redundant. One lens to absorb, not build: "every unfenced cheap path is a direction the
optimizer sprints down" — precisely our aggregate-WARN-suppression bug, and it sharpens the
"disposition unit = concern unit" organ-atomization doctrine. Caveat: the product claims (ant
CLI, Managed Agents, Dreaming, Outcomes, headline metrics) are post-cutoff and unverified —
confirm against Anthropic's docs before adopting any product.

Two beats before design (per the boot): orient (P1), then ask Rob one off-repo question and
make it count — what is the priority for this planning session? The bundle hands you the menu;
only Rob holds the rank. And surface the §1 nightly-skip early — it may be an ADR-84 no-retry
gap, not just a missed run.

The facts are in the bundle. This is how to hold them.
