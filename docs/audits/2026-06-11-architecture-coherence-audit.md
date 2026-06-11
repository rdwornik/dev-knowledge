# Architecture & Governing-Doc Coherence Audit — 2026-06-11

<!-- scope: meta -->

> **Read-only, adversarial audit.** Immutable per repo convention (supersede with a new
> dated file; never edit in place). No fixes are applied here — this audit *feeds* the
> next session, which stabilizes the foundation. Findings were verified against live repo
> state during the session that produced this file; line numbers are as of 2026-06-11.

---

## Orientation (read this first)

**What `.dev-knowledge` is.** The ecosystem's methodology brain — Layer 2 of the ADR-28
three-layer model. It absorbs lessons from every `Dev/` repo, universalizes them into
enforced conventions, and audits the ecosystem against them. It is *passive storage +
governance authority*, not an execution engine: it holds protocols, ADRs, handoffs,
templates, and **read-only** validators. The three layers: **Layer 1** = browser chat
(architect — analysis & design), **Layer 2** = this repo (storage & governance), **Layer 3**
= Claude Code working in child repos (execution).

**Why this audit exists.** The way-of-working has evolved — *model C* (ADR-82, the v5
handoff: CC owns and initiates the handoff; the browser is a thin reactive partner) — faster
than the governing docs that describe it. Worse, the docs have begun describing the system
**to themselves** in prose that restates other docs and drifts from them. That restatement-
drift is the repo's *own named failure class* ("resident-copy drift"); this audit turns that
lens on the repo's self-description. It maps what is **stale, contradictory, missing, or
unreadable** before a future session redesigns the handoff and pointerizes the docs.

**Standing caveat (true throughout).** **ADR-82 is `Proposed`; v5 is `beta` / NON-canonical;
v4.4 (`protocols/HANDOFF_PROCESS.md`) remains the canonical handoff authority.** So most
"v4" descriptions below are *correct today* but will go **silently stale at the #149 flip**.
The exceptions — surfaces already stale against *current* reality — are called out explicitly.

**How to read each scope.** Every scope leads with a plain-language **finding** (the "so
what" a human needs); the file:line evidence is the *proof underneath*, not the headline. A
wall of citations would repeat the exact machine-talk-to-itself failure scope D audits — so
this audit is written to pass its own scope-D test.

---

## Scope A — Resident-copy drift (the repo's failure class, turned on itself)

**Finding.** PLAYBOOK's "System Architecture" section is a **stale hand-copy of
ARCHITECTURE.md's layer model**, and it is the single largest drift surface in the repo. It
still shows the *browser* producing handoffs and *no scripts* residing in Layer 2 — both
false now. The canonical doc (`ARCHITECTURE.md`) is largely **correct**; the damage is in the
*copy*. This is the textbook case for the repo's own fix pattern: pointerize the copy so
there is nothing left to drift.

**Evidence — the stale copy (`protocols/PLAYBOOK.md` §"System Architecture", lines 214–257),
a fenced ASCII box diagram:**
- `:217` — "It is the **passive storage layer**… This section describes what is."
- `:223` — Layer-1 box: `Produces: handoffs, ADRs, session summaries, Council briefs`.
- `:225` — edge **out of Layer 1**: `handoff → git commit`.
- `:231` — Layer-2 box: `No scripts reside here. Library, not daemon.`
- `:249` — Rules: `**Layer 2 never executes.** No scripts, no orchestrator, no active daemon…`
- `:250` — `**Write-back via Layer 1 only.** Claude Code (Layer 3) does not directly edit
  `.dev-knowledge/` files.`

**Evidence — the canonical source it drifted from (`ARCHITECTURE.md`), which is current:**
- `:106` — the layer diagram routes the handoff edge **`L3 -->|"handoff → git commit"| L2`**
  — i.e. **Claude Code (Layer 3) produces and commits the handoff**, the opposite of
  PLAYBOOK:223/225. This is already model-C-consistent.
- `:130–131` — Invariant 1, *carefully scoped*: "Layer 2 never executes. **No script here
  orchestrates actions in, or drives state changes in, another repo.**"
- `:132–134` — Invariant 2: "Validators are read-only on siblings… the cross-repo `audit.py
  run`… **writes only into `.dev-knowledge`**." (So the canon already sanctions the
  self-commit that PLAYBOOK:231/249 deny exists.)

**Why it's drift, precisely.** PLAYBOOK drops the qualifiers the canon keeps. "No scripts
reside here" / "Layer 2 never executes" (absolute) is falsified by the live `scripts/`
(audit.py ~17 checks, codemap/toc generators, validate_backlog, normalize_headers, the
424-test suite) and by `audit.py run` committing its own output. The *invariant* (no
cross-repo execution) is intact and correctly stated in ARCHITECTURE.md; only the over-broad
restatement is wrong.

**Severity:** CONTRADICTION (the diagram graphically states the opposite of the current
model on two counts — handoff ownership and Layer-2 execution).

**Counter-finding (no drift — recorded as the model).** `ESSENTIALS.md` correctly
*summarizes* PLAYBOOK with explicit cross-references rather than copying it; no divergence
found. ESSENTIALS is how a derived doc should relate to its source — the contrast that makes
PLAYBOOK's System-Architecture section's failure legible.

---

## Scope B — Handoff / way-of-working descriptions vs model C

**Finding.** Many doc surfaces describe the **v4** handoff (8-file teaching bundle, two-phase
flow, browser-assembles-and-pastes). Under the standing caveat these are *correct today* but
will go stale at the #149 flip — **except** a few already broken against current reality.

**Already stale today (not merely flip-risk):**
- `CLAUDE.md:22` (§1 "First read") — "Most recent `docs/handoffs/*/HANDOFF.md` if continuing
  prior session." **There is no `HANDOFF.md`.** The live 2026-06-11 v5 bundle ships
  `README.md` / `RESIDUAL.md` / `PROBES.md` / `HANDOFF_BOOT.md`; even v4 bundles are
  `README.md` + `01_ROLE…07_ASK_BACK` (`ESSENTIALS.md:225`). A session-*start* instruction
  points at a filename **neither** bundle shape produces.
- `PLAYBOOK.md` System-Architecture diagram (scope A) — already contradicts model C *and*
  current v4 reality (the `/handoff` command runs in CC; the browser only relays the
  interview, it does not "produce → git commit" the handoff).

**Correct-today, stale-at-flip (the v4 description set):**
- `CLAUDE.md:105` — "`/handoff` — … per `HANDOFF_PROCESS.md` v4 two-phase flow (ADR-62)."
- `CONTRIBUTING.md` §"Handoff process" (~`:184`) — the v4 8-file-bundle / two-phase prose.
- `ESSENTIALS.md:225` — "Upload… the most recent handoff bundle folder… (v4 bundles are flat
  — `README.md` + `01_ROLE`…`07_ASK_BACK`)… follow the bundle's `README.md` paste sequence."
- `PLAYBOOK.md` §8 "Handing Off Between Sessions" — subsections "What the v4 bundle carries",
  "Roles" (browser-receives-and-proves), and the documentation-file-types table's v4-bundle row.
- `.claude/commands/handoff.md` — description + mode logic framed as "v4 is canonical/default,
  v5 is beta"; this framing **inverts** at the flip.
- `SESSION_SETUP.md` handoff disclaimers; `ENVIRONMENT.md` handoff-artifact reference
  (surfaced by exploration; confirm exact lines at flip time).
- `ARCHITECTURE.md` Distribution-and-transfer table — the browser-bundle row cites ADR-79 /
  `BUNDLE.md`, which model C's thin boot (`HANDOFF_BOOT.md`) supersedes *at promotion*.

**Note (fair to ARCHITECTURE.md).** Its **core layer diagram is already model-C-consistent**
(scope A, `:106`). The v4 residue in ARCHITECTURE.md is confined to the version stamp (gated),
the distribution-table ADR-79 row, and ADR-62 references — not its structural model.

---

## Scope C — #149 doc-sync checklist (the non-gated prose that will silently rot)

**Finding.** The audit.py coupling gates protect only **5** surfaces. Everything else that
describes the handoff is **ungated prose** — it will not fail any check when v5 flips to
canonical; it will simply become wrong and stay wrong until a human edits it. This is the
deliverable: the manual sweep the flip must run.

**Gated surfaces (audit.py catches a version mismatch here):** anchored on
`protocols/HANDOFF_PROCESS.md`'s `Version:` line —
- `check_handoff_version_stamp` (audit.py `:949`) greps **ARCHITECTURE.md** + **CONTRIBUTING.md**
  for the `stamp vX.Y` occurrences.
- `check_amendment_coherence` (audit.py `:1051`, surfaces `:1021–1029`) checks the normative
  "`handoff per HANDOFF_PROCESS.md vN`" declaration in **CLAUDE.md** + **.claude/commands/handoff.md**.
- → Gated set = **{HANDOFF_PROCESS.md, ARCHITECTURE.md, CONTRIBUTING.md, CLAUDE.md, .claude/commands/handoff.md}**.

**Non-gated checklist — sweep these by hand when #149 flips (none are version-coupled):**
1. `CLAUDE.md:22` — `HANDOFF.md` "first read" pointer (already wrong; see scope B).
2. `PLAYBOOK.md` §8 "Handing Off Between Sessions" — all subsections (bundle, roles, paths).
3. `PLAYBOOK.md` §"System Architecture" — the ASCII diagram + Rules (scope A).
4. `PLAYBOOK.md` — the documentation-file-types table (v4-bundle row).
5. `ESSENTIALS.md:225` — "New browser chat" v4 upload/paste sequence.
6. `SESSION_SETUP.md` — the "Which handoff is this?" v4 disclaimers.
7. `ENVIRONMENT.md` — the handoff-artifact reference.
8. `.claude/commands/handoff.md` — the "v5 is beta / v4 is default" preamble + mode logic.
9. `ARCHITECTURE.md` — Distribution table (ADR-79 / `BUNDLE.md` row); ADR-62/ADR-79
   authority-status cross-references (their immutable text stays; the *references* to them
   as binding must say "superseded by ADR-82").
10. `CLAUDE.md` §11 "Recent ADRs (last 5)" — rotate ADR-82 in at the flip.

**Leave as history (correct as dated record, no fix):** `JOURNAL.md` v4/v5 transition entries;
`BACKLOG.md` closed handoff items; `ADR-62`/`ADR-79` themselves (immutable; superseded at
promotion). **Recommendation for the next session:** either own this as a one-shot checklist
under #149, *or* build a gate that catches handoff-description drift in prose (a stronger,
durable fix — see BACKLOG #151).

---

## Scope D — Human-comprehensibility / the orientation gap

**Finding.** The 2026-06-11 v5 handoff bundle is **machine talking to itself**: every file
opens with internal jargon and IDs and **never says what `.dev-knowledge` is or what the
project is for**. The *mechanism* (teeth-y forced reads, residual-not-bundle) is sound; the
*failure* is jargon without orientation. A handoff a human cannot parse at the big-picture
level is broken however clever its machinery.

**Evidence — the bundle opens cold, every file:**
- `README.md:4` — "The first real v5 handoff for `.dev-knowledge` — **the #149 teeth dogfood**."
- `RESIDUAL.md:4–5` — "The **residual**: what the repo does not already encode. **Drift-flags**
  are the headline… Pointers are paths, not copies."
- `PROBES.md:1` — "Probe manifest — **teeth-y forced primary-source read** (v5 §5)" → `:6`
  "the browser must reply '**run `<command>`**'… instead of **bluffing** it."
- `HANDOFF_BOOT.md` — opens on "heavy multi-file bundle" / "`/review` vs `/codex review`
  class" with no project introduction.

None of these answer *what is this project, what is the big picture, what is the vision* — the
questions a fresh reader needs first.

**Recovery cases (the bar exists in the repo):** `VISION.md:10–23` orients cleanly in three
plain sentences (the model); `CLAUDE.md` §2 "Purpose" line passes. `ARCHITECTURE.md` and
`HANDOFF_PROCESS_v5.md` are *mixed* — they declare what they are but assume layer/organ/
compaction-summary knowledge in their openings.

**Severity:** the deepest finding for the next session. Readable-first must be a *property of
the handoff*, not just of VISION — the architectural handoff mode must carry what-the-project-is
+ vision (BACKLOG #150).

---

## Scope E — Enforcement completeness (heavy enforcement, thin prose)

**Finding.** Enforcement coverage is genuinely strong — ~31 mechanical points (pre-commit
hooks, session hooks, audit checks). But a **handful of load-bearing constraints are
prose-only or re-stated by the browser every session** because no CC-side mechanism enforces
them. The browser re-stating constraints is a *symptom of that gap*, not a permanent design
choice — closing it is what lets handoffs go lean.

**Mechanically enforced (representative, not exhaustive):**
- OneDrive-exclusion write/delete → `block-onedrive` PreToolUse guard (fail-closed).
- Immutable ADRs/transcripts → `block_immutable_edits.py` PreToolUse (fail-closed in-zone, ADR-77).
- Lint / backlog-schema / TOC / codemap / audit-health → pre-commit gates (fail-closed).
- Canonical-file freshness → audit check #10; backlog-id-on-close → commit-msg hook.

**Prose-only / browser-re-stated (the gap):**
- **`branch + merge --no-ff`** — `~/.claude/rules/core-invariants.md` #5 + `git-discipline.md`,
  but **no FF-guard hook**; a fast-forward *could* slip through. Most dangerous of the set.
- **Minimal diffs** — prose in CLAUDE.md / ESSENTIALS only.
- **Append-only discipline** — `LESSONS.md`, `logs/TOKEN-LOG.md`, `JOURNAL.md` ordering are
  conventions; a violation is only detectable after the fact.
- **No CHANGELOG/BACKLOG-archive recreation** — prose-only.

**Recommendation:** move the highest-value of these (starting with `--no-ff`) to a CC-side
mechanical check (BACKLOG #153).

---

## Scope F — Architecture-as-described vs as-built

**Finding.** Reality has moved ahead of *some restatements*, but — importantly — **not ahead
of the canonical `ARCHITECTURE.md` on the big structural claims**. The canon already reflects
model-C handoff ownership and the audit.py self-write. The genuine as-built-ahead items are
narrower than they first appear, plus one concrete stale number.

**What is genuinely behind reality:**
- **Absolute "Layer 2 never executes" restatements** — `PLAYBOOK.md:231/249`, `CLAUDE.md:72`
  ("`scripts/` contains read-only validators only"). As-built: validators run (and `audit.py
  run` commits its own output, ADR-80 §3 writer policy). *Folds into scope A — the canon
  (ARCHITECTURE.md:130–134) is right; the copies are stale.*
- **DRIFT-1 (concrete, actionable now):** `ARCHITECTURE.md:259` stamps **`**420 collected**`**;
  live `pytest --collect-only` = **`424`** this session. The off-gate `doc_claims` check WARNs
  but does not block, so it persisted. → BACKLOG #154.
- **Validator prose vs organ map:** `ARCHITECTURE.md:233+` describes the validators as
  pre-commit/`run`; they *also* run at SessionStart via `fleet_health.py`. The Ch2 organ map
  is current; the prose section is merely incomplete. Low severity.

**What is NOT drift (over-flag corrected):** the layer label "Layer 2 — passive storage &
governance" (`ARCHITECTURE.md:102`) is **not** contradicted by model C. ADR-82:17 states the
three-layer invariants are *unchanged* ("Layer 2 never executes; execution one-way… what
changes is *who initiates*"). Model C moved the handoff *initiator* (L1→L3), which
ARCHITECTURE's diagram already shows (`:106`); the storage layer stays passive. Flagging "L2
passive" as stale would itself be a misread.

---

## Self-check / reconciliation (no two findings may both be true and contradict)

- **A vs F — same root, not opposed.** Both point at the *over-broad restatements* (PLAYBOOK
  §System-Architecture, CLAUDE.md:72), **not** at a stale canon. ARCHITECTURE.md:130–134 is
  precise and current. Resolved: the drift is in the copies; the fix is pointerization (#152).
- **B/C "v4 is wrong" vs the standing caveat "v4 is canonical."** Reconciled by the
  correct-today / stale-at-flip split: v4 prose is *accurate now*; it becomes wrong only when
  v5 is promoted. The two surfaces already stale *today* (CLAUDE.md:22 `HANDOFF.md`; PLAYBOOK
  diagram) are called out separately and do not depend on the flip.
- **F "Layer 2 executes" vs ADR-82:17 "Layer 2 never executes (invariant)."** Reconciled by
  scope: the *invariant* is "no cross-repo orchestration / execution one-way" (intact); the
  *restatements* over-claim "does nothing executable" (false). audit.py writing **into itself**
  is sanctioned by ARCHITECTURE.md:132–134 and violates neither.
- **Exploration over-flagged ARCHITECTURE.md** (handoff edge, L2-passive). Corrected above;
  recorded so the next session does not "fix" a doc that is already right.

---

## Summary — what feeds the next session

**Stale / contradictory:**
- PLAYBOOK §"System Architecture" — stale resident copy (handoff ownership + Layer-2 execution
  both wrong). *Primary drift surface.* → pointerize (#152).
- `CLAUDE.md:22` `HANDOFF.md` pointer — broken against current reality. → #151 sweep.
- The v4 description set (scope B) — correct now, stale at the #149 flip. → #151 checklist.
- `ARCHITECTURE.md:259` `420 collected` → live `424`. → DRIFT-1 (#154).

**Missing:**
- An orientation layer in the handoff (what-the-project-is + vision) — the architectural
  handoff mode (#150). The bundle has teeth but no big picture (scope D).
- CC-side mechanical enforcement for `--no-ff` and the append-only/minimal-diff constraints
  the browser re-states each session (#153).
- A durable gate (or owned checklist) for handoff-description drift in ungated prose (#151).

**Unreadable:**
- The 2026-06-11 v5 bundle, at the big-picture level (scope D). Mechanism sound; orientation
  absent.

**Sound (do not "fix"):** ARCHITECTURE.md's core layer model + invariants; ESSENTIALS's
summarize-not-copy relationship to PLAYBOOK; the enforcement mesh's mechanical coverage; the
v5 teeth mechanism itself.

**Sequencing note for the next session.** The handoff cannot be perfected until the
way-of-working is defined. Stabilize the architecture *enough* (pointerize the drift; define
the two handoff modes); the handoffs improve alongside. Beware the "nothing until the
foundation is perfect" treadmill — a living system's foundation is never *done*.

---

*Audit produced read-only on 2026-06-11. Companion captures: 7 LESSONS entries (2026-06-11)
and BACKLOG #150–#155. No source files were modified by this audit.*
