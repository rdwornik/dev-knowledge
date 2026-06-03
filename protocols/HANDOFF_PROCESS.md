# HANDOFF_PROCESS v4

<!-- version: 4.3.1 — 2026-05-30 (v4.0 radical simplification + v4.1 fix: in-progress/ folder + sage→apprentice single-cluster interview + v4.2 refinements: four-tag sage + drift visibility + bundle maintenance + v4.3: comprehensive fresh-eyes close + enforcement groundwork + v4.3.1: architectural caveat patch + status stable) -->
<!-- scope: meta -->

Version: 4.3
Effective: 2026-05-29
Supersedes: v3.4 (preserved at `protocols/archive/HANDOFF_PROCESS_v3.4.md`) and the
full v3.x chain it carried forward.
Status: live
Authority: this protocol is the single live source of truth for handoff mechanics.
ADRs 42/45/55/56/57/58 describe the v3.x design and remain immutable historical
record; where they conflict with v4, **v4 wins** (the architectural decision
formalizing v4 is deferred to a future AI Council convene — see BACKLOG).

> **Why a rewrite.** v3.4 was retry-ready but over-engineered (13–14 files, a
> placeholder dance, a JSON manifest, Stage 1↔3 desync risk, drift-prone
> hand-maintained surfaces). v4 reframes a handoff as **onboarding a new chat — a
> teaching protocol, not a file transfer** — and collapses the mechanics to two
> phases and eight source-generated bundle files.

---

## 1. Purpose
<!-- scope: meta -->

A handoff onboards a **new chat** to continue work that a prior (sender) chat or
session began. The deliverable is not a data dump — it is a teaching sequence: the
new chat learns who it is, how we work, what the project is, what just happened,
and what to do now; then it proves comprehension before it touches anything.

All handoff artifacts live in `.dev-knowledge/docs/handoffs/<slug>/`. The
ADR-36 read-only contract holds: a handoff never writes to a target repo. Per
ADR-41, a bundle covers only its own repo's state and never directs work on
another repo.

---

## 2. When to invoke
<!-- scope: meta -->

Two triggers, both operator-initiated (Claude Code never proposes a handoff
unprompted):

- **Session end** — a working chat's context is filling up; preserve its state
  for a fresh chat to continue.
- **New-repo onboarding** — bring a fresh chat up to speed on a repo it has never
  seen.

Trigger phrases:

| Phrase | Effect |
|---|---|
| `please create handoff for <repo>` | Phase 1 — generate the interview |
| `complete handoff for <repo>` | Phase 2 — consolidate the bundle |

`<repo>` defaults to `.dev-knowledge` (self-handoff). Naming a different repo is a
cross-repo handoff (§8).

---

## 3. Two-phase flow
<!-- scope: meta -->

Phase 1 (CC) writes the interview → operator copies the questions to the sender
browser chat and pastes the answers back → Phase 2 (CC) reads them, cross-checks
against repo state, and generates the bundle. In detail:

- **Phase 1 — Interview (Claude Code).** On `please create handoff for <repo>`, CC
  writes an in-progress file `docs/handoffs/in-progress/<slug>/_handoff-interview.md`
  containing a single **sage→apprentice** cluster of 5 questions (Past / Present /
  Future / Wisdom / Warnings) and a `=== PASTE ANSWERS BELOW THIS LINE ===` marker
  (full structure in §3.1). CC appends a JOURNAL marker and commits the in-progress
  file on the feature branch.
- **Operator (between phases).** The operator copies the questions into the
  **sender** browser chat (the chat being wrapped up, which holds the lived
  context), gets narrative answers, pastes them below the marker in the in-progress
  file, and saves.
- **Phase 2 — Consolidate (Claude Code).** On `complete handoff for <repo>`, CC
  reads the interview, **cross-checks the browser answers against actual repo
  state** (drift detection — surfaced to the operator if found), generates the
  bundle at `docs/handoffs/<slug>/` (README + 01–07) from source files, removes the
  `in-progress/<slug>/` folder, appends a JOURNAL marker, and commits.

No Stage vocabulary, no placeholder dance, no separate claims/scope/probe artifacts
— claims and scope become inline narrative in the generated bundle.

### 3.1 The Phase 1 interview (sage→apprentice frame)
<!-- scope: meta -->

> **Note (updated 2026-05-29, v4.3 item C):** The three-tag claim discipline shown
> in the interview template below has been **superseded by Amendment A** (end of
> document) — four-tag canonical (witnessed/recall/inferred/unknown). Amendment
> precedence applies; the body below is preserved for historical decision-tracking,
> but the live discipline is four-tag.

The interview is **not a methodology quiz**. The books (`PLAYBOOK`, `ESSENTIALS`,
`CLAUDE.md`, the ADRs) already hold the theory, which the apprentice (next chat)
reads independently. What only the sender chat (the **sage**) can transmit is the
*lived implementation* of that theory in this project's circumstances this session
— so the interview asks for experience, not curriculum. One cluster of 5 questions
— **Past / Present / Future / Wisdom / Warnings** — written verbatim by Phase 1:

```
# Handoff Interview — {slug}

| Field | Value |
|---|---|
| Repo | {repo} (self-handoff or cross-repo) |
| Slug | {slug} |
| Date | {date} |
| Type | session |
| HEAD captured | {sha} |
| Branch (at capture) | {branch} |
| Working tree (at capture) | {clean/dirty} |
| Process | HANDOFF_PROCESS v4 — Phase 1 (interview) |

## Role frame

Imagine an elder sage handing wisdom to a young apprentice. You — the sage —
are tired, your context is fading, but you hold the lived experience the
apprentice needs to continue this specific project's work. The apprentice
will read the books independently — PLAYBOOK, ESSENTIALS, CLAUDE.md, ADRs
— that's the theory. What only you can transmit is how the theory was
implemented in THIS project's specific circumstances during this session.

Answer narratively. Tag each claim:
- **witnessed** (you saw it happen this session)
- **inferred** (you're reasoning from evidence)
- **unknown** (you don't have direct knowledge — say so)

Skip any question that doesn't apply. Say so explicitly.

## Question block — copy from here

### 1. Past — what shipped

What did this session actually accomplish? Concretely: what merged, what
shipped, what changed in the codebase, what audits or decisions landed.

### 2. Present — where things stand

What's currently in-flight? Anything half-done, on an unmerged branch,
waiting on a merge, paused mid-decision, blocked on something external?

### 3. Future — natural next step

Of the open paths, which is the natural next step? What were you about to
do when this chat wound down? What's the obvious follow-up to what was
just done?

### 4. Wisdom — key decisions

Of the key decisions made this session, what was the reasoning? Anything
considered and rejected, and why? What turned out harder or easier than
expected?

### 5. Warnings — landmines

What should the next session NOT do? Anti-patterns you saw recur, landmines
specific to the current state, things that look wrong but are intentional,
witnessed-only context that won't be obvious from JOURNAL / BACKLOG / git
history.

## Question block — copy to here

=== PASTE ANSWERS BELOW THIS LINE ===
```

---

## 4. Bundle structure
<!-- scope: meta -->

`slug = YYYY-MM-DD-<repo>-<type>` (e.g. `2026-05-29-dev-knowledge-session`). Eight
files, flat, no subdirectories:

```
docs/handoffs/<slug>/
├── README.md          Operator-facing: paste sequence + escalation ladder
├── 01_ROLE.md         ≤100 lines — who the new chat is, who Rob is
├── 02_METHODOLOGY.md  ≤200 lines — pointers to PLAYBOOK + key extracts
├── 03_PROJECT.md      ≤150 lines — vision + sacred files (from VISION.md)
├── 04_RECENT.md       ≤250 lines — narrative synthesized from JOURNAL + interview
├── 05_NOW.md          ≤100 lines — top P1s + in-progress branches (BACKLOG + git)
├── 06_QUESTIONS.md    ≤80 lines  — comprehension check, 5–7 questions
└── 07_ASK_BACK.md     ≤50 lines  — new chat's question slot, max 3 invited
```

**Total ≤930 lines** (≈half the v3.4 footprint). README is operator-facing and not
pasted into the new chat; 01–07 are the teaching sequence pasted in order.

---

## 5. File generation principle (critical)
<!-- scope: meta -->

Bundle files are **generated FROM source at handoff time**, not hand-maintained: a
hand-kept parallel copy drifts from the real files (the ecosystem-audit
doc-truth-drift finding). Generating each time keeps the bundle as current as the repo.

> **Claim sharpened — see Amendment v4.3 §A.** "Generated FROM source" is *deterministic* for the sacred-file lifecycle tables and conventions lists, but *LLM-synthesized* (partly aspirational) for the arc narrative, wisdom, and warnings. The honest framing — and why synthesis imperfection is expected and feeds the next iteration — is in §A "Architectural claim sharpening" below.

| File | Generated from |
|---|---|
| `01_ROLE.md` | Template + operator-specific role context (slowly evolving) |
| `02_METHODOLOGY.md` | Key sections (by name) of `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md`; model-selection + prompt-format + hooks + AI-Council + conventions extracts |
| `03_PROJECT.md` | `VISION.md` (vision + scope) + `CLAUDE.md` (purpose/critical paths) + sacred-files list from ADRs/conventions; ADR-41 cross-repo ownership note |
| `04_RECENT.md` | CC narrative synthesis of `JOURNAL.md` last N entries (default N=20 OR last 7 days, whichever is smaller) + browser interview answers folded inline. **Narrative prose, not a journal copy.** |
| `05_NOW.md` | `BACKLOG.md` top P1s + `git branch -v` (in-progress branches) + recent commit tip |
| `06_QUESTIONS.md` | Template (4–5 static comprehension questions) + 1–2 dynamic slots tailored to recent work (from interview/JOURNAL) |
| `07_ASK_BACK.md` | Static template inviting up to 3 questions before work starts |

The templates in `templates/handoff/` carry generation markers:

- `{{PULL: <source>#<section>}}` — copy/condense a named section from a source file
- `{{SYNTHESIZE: <source>}}` — CC writes narrative prose from the source
- `{{CONTEXT: <variable>}}` — substitute a captured value (slug, repo, branch, …)

CC resolves every marker at Phase 2. An unresolved marker in a generated file is a
generation failure — fix it or note the degradation (§9), never ship the literal
marker.

---

## 6. Operator workflow
<!-- scope: meta -->

1. In Claude Code (`.dev-knowledge`): `please create handoff for <repo>`.
2. Open `docs/handoffs/in-progress/<slug>/_handoff-interview.md`; copy the question
   block into the **sender** browser chat (the one being wrapped up).
3. Paste the chat's narrative answers below the
   `=== PASTE ANSWERS BELOW THIS LINE ===` marker; save.
4. In Claude Code: `complete handoff for <repo>`. CC generates the bundle and
   surfaces any drift it found between the browser answers and repo state.
5. Use the bundle per its `README.md` escalation ladder:

```
Step A: Paste 01–05 as ONE message into the new chat. Wait for acknowledgment.
Step B: Paste 06 (questions). Read the chat's answers.

IF comprehension FAILS:
  Tier 1 — re-paste the specific files the chat got wrong + "read again carefully".
  IF still fails:
  Tier 2 — ask CC to verify the specific facts against repo state; paste CC's
           findings to the new chat.
  IF still fails:
  Tier 3 — ABORT onboarding. Reactivate the sender chat, or do a manual context dump.

IF comprehension PASSES:
  Step C: Paste 07 (ask_back). Answer the chat's questions from memory or sender chat.
  Step D: The chat begins work.
```

---

## 7. State machine
<!-- scope: meta -->

Three live states, detected by **content** (marker presence + non-empty answers),
not by file existence alone (closes the v3.4 state-ambiguity finding):

| State | Detected by | Action |
|---|---|---|
| Fresh | no `_handoff-interview.md` in `in-progress/<slug>/` | run Phase 1 |
| Awaiting answers | interview present, nothing below the PASTE marker | instruct operator (idempotent — do not regenerate) |
| Ready to consolidate | interview present **with** non-empty answers below the marker | run Phase 2 |
| Complete | bundle folder exists at `docs/handoffs/<slug>/` (no `in-progress/<slug>/`) | instruct operator on use |

If state is genuinely ambiguous (e.g. a bundle already exists and the operator
says "create handoff" again), FLAG and ask — never silently overwrite.

---

## 8. Cross-repo handoff
<!-- scope: meta -->

Same skill, same flow; only the repo context differs. When `<repo>` is not
`.dev-knowledge`:

- The slug carries the target repo name (`YYYY-MM-DD-<repo>-<type>`).
- Phase 2 reads the **target repo's** state (git, BACKLOG if present) read-only —
  never writes to it (ADR-36).
- `03_PROJECT.md` is built from the target repo's own `VISION.md`/`CLAUDE.md` when
  present; `.dev-knowledge` methodology floor (02) stays universal.
- The bundle still lives in `.dev-knowledge/docs/handoffs/<slug>/`.
- A bundle never directs work on a third repo (ADR-41). Cross-repo threads close
  via routing artifacts, not the handoff.

---

## 9. Failure handling (graceful degradation)
<!-- scope: meta -->

A source file may be missing, or a `{{PULL}}` target section may have moved:

- **Missing source file:** generate the file from available fallbacks, omit the
  unavailable section, and **note the degradation explicitly in `README.md`** ("03
  built without VISION.md — target repo lacks one"). Never fabricate the content.
- **Unresolvable marker (section renamed/removed):** stop on that file, report the
  marker and the source it targeted to the operator, and ask — do not ship the
  literal marker and do not guess the section.
- **Interview present but answers empty:** stay in "awaiting answers"; instruct the
  operator. Do not generate a bundle from an empty interview.
- **Browser answer contradicts repo state:** surface the drift to the operator at
  Phase 2 (both the claim and the repo fact); let the operator decide. The
  generated `04_RECENT.md` reflects verified repo state, with the architect's
  framing where it adds judgment.

Silent truncation or fabrication is the failure mode to avoid: degrade loudly.

---

## 10. Supersession chain
<!-- scope: meta -->

v4 supersedes v3.4 (and the full v3.x chain). v3.4 is preserved verbatim at
`protocols/archive/HANDOFF_PROCESS_v3.4.md`.

The v3.4 Q1–Q5 concepts map into v4 as follows:

| v3.4 concept (ADR) | v4 form |
|---|---|
| Structured claims `11_CLAIMS.md` (ADR-58) | inline verifiable narrative in `04_RECENT.md`, cross-checked by CC at Phase 2 |
| `next_session_scope` (ADR-57) | embedded in `05_NOW.md` narrative |
| Gate probe `10_GATE_PROBE.md` (ADR-55) | receiver-side comprehension check in `06_QUESTIONS.md` |
| Prompt Generation Card (ADR-56) | folded into `02_METHODOLOGY.md` (pulled from PLAYBOOK) |
| JSON manifest sidecar (ADR-42 Q5) | removed — bundle structure declared in `README.md`, markdown only |
| Structured ratification (ADR-58) | operator escalation ladder (Tier 1/2/3, §6) |
| Three-stage / placeholder dance | two phases + one in-progress interview file |

ADRs 42/45/55/56/57/58 remain immutable; each carries an appended 2026-05-29
supersession amendment. The formal ADR for v4 is **deferred to AI Council** per
standing operator preference (architecture goes through Council) — tracked in BACKLOG.

---

## Section history
<!-- scope: meta -->

- v4.0 (2026-05-29) — full rewrite. Reframes handoff as onboarding-as-teaching:
  two phases replace the three-stage flow, eight source-generated bundle files
  replace 13–14 hand-maintained ones, an operator escalation ladder replaces
  structured ratification, and a content-based three-state machine replaces
  six-state file detection (mapping table in §10). Grounded in the 2026-05-29
  process audit (13 findings) + ecosystem audit (22 findings) + operator/architect
  design discussion. v3.4 archived; ADR for v4 deferred to Council.
- v4.1 (2026-05-29) — fix after first Phase 1 invocation surfaced two
  implementation defects: (1) the interview file moves from a unilaterally-
  introduced `_scratch/` folder to the existing `docs/handoffs/in-progress/<slug>/`
  convention (no new folders without operator approval); (2) the Phase 1 interview
  collapses from two clusters (project + methodology) to a single **sage→apprentice**
  cluster of 5 questions (Past/Present/Future/Wisdom/Warnings) — the methodology
  cluster duplicated PLAYBOOK/ESSENTIALS, which the apprentice reads independently;
  the sage transmits only the project's lived implementation (§3.1). Bundle
  structure, generation principle, and templates unchanged.
- v3.x (2026-05-09 → 2026-05-26) — three-stage flow; see
  `protocols/archive/HANDOFF_PROCESS_v3.4.md` for the full v3.x section history.

---

## Amendment 2026-05-29 — v4.2 refinements

After v4.1's first end-to-end run, seven template/spec refinements (no architectural changes; design sound).

### A. Sage tagging discipline (sharper definitions)

The Phase 1 interview preamble now uses **four tags** instead of three:

- **witnessed** = I just verified this OR saw it happen recently AND have no reason to think it changed since
- **recall** = I remember this from earlier in the session — **state may have changed**; prefer verifying via CC inline if claim is load-bearing
- **inferred** = reasoning from evidence (not direct knowledge)
- **unknown** = I don't know — say so explicitly

v4.1's single "witnessed" tag was ambiguous between "just verified" and "remember being true at some point." This bit in v4.1's first run (aborted-folder claim was effectively `recall` but tagged `witnessed` → drift caught by Phase 2 verification). The four-tag system separates them. The Phase 1 interview file's role-frame preamble carries the new tag definitions verbatim.

### B. Verification table standard section in 04_RECENT

The Load-bearing facts cross-check table is now a **required section** of every generated `04_RECENT.md`, present whether drift was detected or not. If no drift: explicit single row `| (all sender claims) | matches repo state | ✅ no drift detected | (verified at Phase 2) |`. If drift: the existing table format extended with a **Verification command** column so the apprentice can re-verify independently.

### C. README drift visibility — section moved up

In every generated `README.md`, the drift section ("Drift cross-check") moves to **immediately after** the paste sequence + escalation ladder, **before** the bundle contents table. Apprentice sees drift on first read, not buried near the end.

### D. Bundle version + status stamp

Every generated `README.md` header now includes a status line: `Generated by HANDOFF_PROCESS v<X.Y> (status: <beta|stable>)`. Status convention: `beta` for the first three end-to-end runs of any version; `stable` thereafter. Provides apprentice with process-maturity context.

### E. Bundle maintenance during session (operator-facing)

`02_METHODOLOGY` template gains a short section: if the apprentice discovers drift between bundle and repo state DURING their work, the flow is: flag to operator → JOURNAL the discovery → amend the bundle's `04_RECENT` Load-bearing facts table via append (don't rewrite). The bundle is living until the next handoff.

### F. 05_NOW forced-ranking warning

When `05_NOW.md` presents multi-candidate first-moves, the template ends with: *"Propose your choice with rationale to Rob — don't ask him to forced-rank. Operator energy is finite; your job is reasoned pre-selection."*

### G. PLAYBOOK methodology rule promotion (separate edit to PLAYBOOK)

The "handoff is back-and-forth" rule generalizes beyond handoff to all LLM-LLM context transfer (chat-to-chat, browser-to-CC, CC-to-Codex). Codified in PLAYBOOK methodology section, not just here.

### Status of v4 → v4.2

v4 architecture (two-phase, 8-file bundle, files-from-source, sage frame, escalation ladder) **unchanged**. v4.2 is template/spec polish only. No template added or removed. No new file types in bundle. No new phases.

---

## Amendment 2026-05-29 — v4.3 stable-readiness

v4.2's first end-to-end run + fresh-eyes outsider review (independent Opus 4.8, no project context) caught defects insider review missed: 4 critical, 6 medium, 4 minor + the meta-architectural question about v4's "generated from source" claim. This amendment closes all + sharpens v4's architectural claim + lays enforcement groundwork.

### A. Architectural claim sharpening

v4's earlier framing "8 files generated from source" was partly true (sacred-files lifecycle tables, conventions lists — extracted deterministically from CLAUDE/PLAYBOOK/ESSENTIALS) and partly aspirational (the arc narrative, wisdom, warnings — synthesized by LLM at Phase 2 time from architect's interview answers). The honest, sharpened claim:

> v4 collapses **persistently-maintained hand-authored surfaces** (the v3.4 disease) by making bundles **ephemeral, generated per-handoff, verified per-generation against repo state.** Synthesis imperfection during Phase 2 is expected and accepted; imperfections drive template/skill improvements via the use→review→refine→re-validate cycle, not bundle re-maintenance.

What v4 IS: between-session surface collapse + per-generation verification. What v4 IS NOT: zero-imperfection at synthesis time. Imperfections feed the next iteration.

### B. Four-tag canonical definitions inline (closes C1+C2)

Phase 2 bundle generation now ALWAYS inlines the four-tag definitions in `04_RECENT.md` as a standalone section after the narrative arc, before the load-bearing facts table. Apprentice applies discipline from bundle alone, no PLAYBOOK reading required.

### C. §3.1 cross-reference pointer (closes C3, partial)

The spec body §3.1 (three-tag section) gets a one-line cross-reference pointer to Amendment A (four-tag canonical). Update-in-place is acceptable per `protocols/*.md` "living" classification. Amendment-only practice preserved for decision content; metadata annotations are not decision content.

### D. Verdict column label (closes M1)

Load-bearing facts table column "Verdict" renamed "Phase-2 verdict" — disambiguates from sender-tag values.

### E. Beta→stable promotion criterion (closes process gap)

A HANDOFF_PROCESS version promotes from `beta` to `stable` after one fresh-eyes review with **fewer than 2 critical findings.** Fresh-eyes = independent LLM chat, zero project context, given the bundle + meta-reviewer prompt. <2 critical = converged → promote. ≥2 critical = next refinement cycle. **No Council convene required for promotion** (operator's call, captured here for record). This **supersedes** the earlier "three end-to-end runs" promotion heuristic (v4.2 item D): convergence is measured by fresh-eyes defect count, not run count.

### F. Enforcement layer (closes MO2 partial)

`scripts/audit.py` gains check #8 (handoff bundle structure validator) and check #9 (tag-canonicity lint). Health gate goes 7/7 → 9/9. Check #8 validates only **stamped v4 bundles** (those whose `README.md` carries the `Generated by HANDOFF_PROCESS v4.x` stamp); pre-stamp bundles (v4.1 first-run) and v3.x sync bundles predate the contract and are out of scope. The four-tag-section requirement applies only to v4.3+ bundles. Catches structural drift at lint time, prevents §3.1-vs-Amendment-A recurrence at next major version.

### G. Agent-framework v0.1 stub

`protocols/AGENT_FRAMEWORK.md` v0.1 stub authored to anchor operator's strongest structural signal ("musimy zbudować agent framework, który pewne rzeczy, żebym nie musiał po prostu powtarzać"). Stub captures problem + design constraints + future-work pointer. Not implementing the framework in v4.3; this is a placeholder so the signal isn't lost between sessions.

### Status

v4.3 ships at status `beta`. Promotion to `stable` after v4.3 fresh-eyes review confirms <2 critical findings.

## Amendment 2026-05-30 — v4.3.1 architectural caveat patch + stable promotion

The v4.3 fresh-eyes outsider review (independent Opus 4.8, second pass) returned **PROMOTE WITH CAVEATS** — object-level convergence achieved, but two architectural items must be addressed before v4 is "fully converged":

### A. Triangulation scope — honest claim

v4 codified triangulation (insider + outsider review) as the beta→stable promotion criterion. **The fresh-eyes reviewer correctly observed: this guards process VERSIONING, not each routine handoff artifact.** Every routine handoff still rides on Phase-2 self-verification — the exact insider-only coverage (empirically ~25%) the arc disproved.

**Honest scoping:**
- **Process versioning:** triangulation IS the gate. Independent fresh-eyes review with judgment-augmented promotion criterion (see B below).
- **Routine handoffs:** Phase-2 self-verification + operator visual check. Adversarial review per-artifact is a future enhancement (BACKLOG P1).

This scoping does NOT diminish v4's claim — it states what v4 IS (between-session surface collapse with verified ephemeral generation) and IS NOT (per-artifact adversarial verification, which would require an agent framework not yet built).

### B. Promotion criterion — judgment-augmented, not pure count

v4.3's criterion was `<2 critical findings on one fresh-eyes review → promote stable`. The fresh-eyes reviewer correctly observed: **this is itself an easy-metric** — convergence judgment reduced to a count flippable by reviewer reclassification. Bundle warns against this exact failure mode in its decision-carry-forward.

**Revised criterion (judgment-augmented):**

A HANDOFF_PROCESS version promotes from `beta` to `stable` after one fresh-eyes review where:

1. **Mechanical condition:** Stage 1 returns **fewer than 2 critical findings** (severity 4-5/5)
   AND
2. **Judgment condition:** the reviewer's Stage 3 verdict is **PROMOTE** or **PROMOTE WITH CAVEATS** (caveats logged to BACKLOG; ratification follows operator decision)
3. **Override:** if reviewer's judgment recommends DO NOT PROMOTE despite <2 critical mechanical count, **reviewer judgment wins** (v4.4 cycle).

This honors hard-metric > easy-metric: count is a proxy for convergence judgment, not a replacement. Reviewer's judgment overrides count when they differ.

### C. Operational clarification — who runs the fresh-eyes review

The `05_NOW.md` template's immediate objective for a v-X.Y stable-readiness bundle previously read "give this bundle to an independent LLM chat" without specifying WHO runs the chat. **Clarification:** Rob (operator) opens a separate Claude.ai chat with the meta-reviewer prompt + bundle files. The apprentice chat (the recipient of the handoff bundle) **awaits results** — does not spawn the review chat itself.

### D. audit.py check #9 scope — syntactic, not semantic

The v4.3 amendment said check #9 "enforces" tag canonicity. **Clarification:** check #9 is **syntactic** — verifies §3.1 has either (a) four canonical tags enumerated OR (b) "see Amendment A" pointer. It does NOT detect mis-labeled tags (a `witnessed` claim that should have been `recall` passes the lint).

Semantic tag-discipline accuracy requires reader/sage discipline + Phase-2 verification table cross-checking. Check #9 closes the canonicity gap, not the accuracy gap. ML-2 (un-enforced guard pattern) is NOT closed for tag accuracy by check #9 — only for canonicity enumeration. Future BACKLOG: semantic tag-lint (check #10+?) requires LLM-in-the-loop, not regex.

### E. Status: beta → stable

With A-D landed:
- 4/4 v4.2 critical findings closed (per v4.3)
- N1 (triangulation scope) addressed honestly via A
- MO1 (criterion-as-easy-metric) addressed via B
- N4 (operational ambiguity) addressed via C
- N2 (check #9 enforcement framing) addressed via D
- Reviewer's PROMOTE WITH CAVEATS recommendation operationalized

**HANDOFF_PROCESS v4.3 promotes to status `stable` as of this amendment (2026-05-30).**

Remaining items deferred to BACKLOG (not promotion-blocking):
- **P1:** Adversarial fresh-eyes pass in routine handoff generation (operator's agent-framework signal extension)
- **P3:** Periodic fresh-eyes audit cadence (every N handoffs or quarterly)
- **P3:** Semantic tag-lint (check #10 — LLM-in-the-loop, catches mis-labeled tags)
- **P3:** AI Council CLI invocation example in 02_METHODOLOGY
- **P3:** ML-2 namespace expansion (define what ML stands for in repo prose)
- **P3:** Operating mode "test after every change" — reword for layer-agnostic clarity (current wording maps imperfectly to browser architect work)

v5 / next major HANDOFF_PROCESS bump (Council scope, future) consolidates v4 body + amendments A (v4.2) + A (v4.3) + A (v4.3.1) into fresh budget-compliant spec body.
