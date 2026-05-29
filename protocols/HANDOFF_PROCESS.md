# HANDOFF_PROCESS v4

<!-- version: 4.0 — 2026-05-29 (radical simplification: onboarding-as-teaching, two-phase, 8-file bundle, files generated from source) -->
<!-- scope: meta -->

Version: 4.0
Effective: 2026-05-29
Supersedes: v3.4 (preserved at `protocols/archive/HANDOFF_PROCESS_v3.4.md`) and the
full v3.x chain it carried forward.
Status: live
Authority: this protocol is the single live source of truth for handoff mechanics.
ADRs 42/45/55/56/57/58 describe the v3.x design and remain immutable historical
record; where they conflict with v4, **v4 wins** (the architectural decision
formalizing v4 is deferred to a future AI Council convene — see BACKLOG).

> **Why a rewrite.** v3.4 was technically retry-ready but architecturally
> over-engineered: 13–14 bundle files, a multi-stage placeholder dance, a JSON
> manifest sidecar, Stage 1↔3 desync risk, and hand-maintained surfaces prone to
> drift (2026-05-29 process audit + ecosystem audit findings). v4 reframes a
> handoff as **onboarding a new chat — a teaching protocol, not a file transfer**
> — and collapses the mechanics to two phases and eight bundle files generated
> from source at handoff time.

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

```
Phase 1 (CC)          Operator (browser)            Phase 2 (CC)
────────────          ──────────────────            ────────────
write interview  →    copy questions to        →    read answers,
scratch file          sender chat, paste            cross-check vs repo,
(~10 questions)       narrative answers back        generate 8-file bundle,
                      below the marker, save        delete interview, commit
```

- **Phase 1 — Interview (Claude Code).** On `please create handoff for <repo>`, CC
  writes a scratch file `docs/handoffs/_scratch/_handoff-interview.md` containing
  ~10 questions in two clusters (5 project + 5 methodology) and a
  `=== PASTE ANSWERS BELOW THIS LINE ===` marker. CC appends a JOURNAL marker and
  commits the scratch file on the feature branch.
- **Operator (between phases).** The operator copies the questions into the
  **sender** browser chat (the chat being wrapped up, which holds the lived
  context), gets narrative answers, pastes them below the marker in the scratch
  file, and saves.
- **Phase 2 — Consolidate (Claude Code).** On `complete handoff for <repo>`, CC
  reads the interview, **cross-checks the browser answers against actual repo
  state** (drift detection — surfaced to the operator if found), generates the
  bundle at `docs/handoffs/<slug>/` (README + 01–07) from source files, deletes
  the scratch interview, appends a JOURNAL marker, and commits.

There is no Stage vocabulary, no placeholder-file dance, no separate claims/scope/
probe artifacts. Claims and scope become inline narrative in the generated bundle.

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

**Total ≤930 lines** — roughly half the v3.4 footprint. README is operator-facing
and not pasted into the new chat; 01–07 are the teaching sequence.

---

## 5. File generation principle (critical)
<!-- scope: meta -->

Bundle files are **generated FROM source at handoff time**, not hand-maintained.
This directly addresses the ecosystem-audit doc-truth-drift finding: a hand-kept
parallel copy of methodology/project facts drifts from the real files. Generating
from source each time means the bundle is as current as the repo.

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
2. Open `docs/handoffs/_scratch/_handoff-interview.md`; copy the question block
   into the **sender** browser chat (the one being wrapped up).
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

The escalation ladder replaces v3.4's structured ratification (UNVERIFIED/VERIFIED
modes). It is operator-driven, tiered, and has an explicit abort.

---

## 7. State machine
<!-- scope: meta -->

Three live states, detected by **content** (marker presence + non-empty answers),
not by file existence alone (closes the v3.4 state-ambiguity finding):

| State | Detected by | Action |
|---|---|---|
| Fresh | no `_handoff-interview.md` in `_scratch/` | run Phase 1 |
| Awaiting answers | interview present, nothing below the PASTE marker | instruct operator (idempotent — do not regenerate) |
| Ready to consolidate | interview present **with** non-empty answers below the marker | run Phase 2 |
| Complete | bundle folder exists at `docs/handoffs/<slug>/` | instruct operator on use |

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

A source file may be missing (e.g. a target repo has no `VISION.md`) or a named
section may have moved so a `{{PULL}}` marker cannot resolve.

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
| Three-stage / placeholder dance | two phases + one scratch interview file |

ADRs 42/45/55/56/57/58 remain immutable; each carries an appended 2026-05-29
amendment noting this supersession. The formal ADR for v4 is **deferred to AI
Council** per standing operator preference (architecture decisions go through
Council, not unilateral edits) — tracked in BACKLOG.

---

## Section history
<!-- scope: meta -->

- v4.0 (2026-05-29) — full rewrite. Reframes handoff as onboarding-as-teaching.
  Two phases (interview / consolidate) replace the three-stage flow; eight bundle
  files (README + 01–07) generated from source replace 13–14 hand-maintained
  files; operator escalation ladder replaces structured ratification; content-based
  three-state machine replaces six-state file-existence detection. Removes JSON
  manifest, gate-probe artifact, separate claims file, placeholder dance, and Stage
  vocabulary. Grounded in the 2026-05-29 process audit (13 findings) + ecosystem
  audit (22 findings, doc-truth drift dominant) + operator/architect design
  discussion. v3.4 archived. ADR for v4 deferred to Council.
- v3.x (2026-05-09 → 2026-05-26) — three-stage flow; see
  `protocols/archive/HANDOFF_PROCESS_v3.4.md` for the full v3.x section history.
