# HANDOFF_PROCESS v3.2

<!-- version: 3.2 — 2026-05-09 (night per thrice-amended ADR-42) -->
<!-- scope: meta -->

Version: 3.2
Effective: 2026-05-09 (night)
Supersedes: v3.1 (2026-05-09 afternoon), v3.0 (2026-05-09 morning), v2.0 (ADR-32 §4 deprecated; ADR-32 §1-§3 extended)
Authority: ADR-42 (amended 2026-05-09 night)

> **Authoritative source:** `docs/decisions/ADR-42_handoff_format_v3.md` (amended
> through v3.2). This protocol is the operational counterpart of ADR-42: structural
> decisions live in the ADR; operational mechanics (triggers, state tracking, generation
> workflow, roles, validation checkpoints) live here. If they conflict, ADR-42 wins.

---

## Purpose
<!-- scope: meta -->

Operational protocol for generating handoffs in the `.dev-knowledge` ecosystem.
Implements ADR-42 three-stage flow with full Stage 2 mandate — ALL handoff types
(audit-sync, session-sync, feature-X-sync) execute all three stages. No shortcuts.

A handoff transfers session state across browser chats or Claude Code sessions. All
handoff artifacts live in `.dev-knowledge/docs/handoffs/{date}-{slug}/` — ADR-36
read-only contract preserved (no writes to target repos).

---

## Three actors
<!-- scope: meta -->

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│  OLD browser chat for repo  │         │  NEW browser chat for repo  │
│  (existing, dying context)  │         │  (fresh, opened after S3)   │
│                             │         │                             │
│  Stage 2 SOURCE             │         │  Stage 3 RECEIVER           │
│  Architect's tacit          │         │  Acts on directives         │
│  knowledge dump             │         │  Fills 09_EXECUTION_        │
│  before context dies        │         │    EVIDENCE.md              │
└──────────┬──────────────────┘         └──────────▲──────────────────┘
           │                                        │
           │ stage2-response.md                     │ handoff folder
           │ (Rob copies/saves)                     │ (Rob zips + uploads)
           ▼                                        │
┌──────────────────────────────────────────────────┴──────┐
│             Claude Code in .dev-knowledge                │
│             (orchestrator + generator)                   │
│                                                          │
│  Stage 1: generate stage1-question.md → Rob takes to    │
│           OLD chat to extract architect knowledge        │
│  Stage 3: generate 11-file folder → Rob uploads to      │
│           NEW chat to continue work                      │
└──────────────────────────────────────────────────────────┘
```

The OLD chat is being wrapped up because its context is exhausted.
Stage 2 captures its accumulated tacit knowledge before it dies.
The NEW chat opens fresh with the full 11-file bundle — zero history,
complete methodology context via VISION/PLAYBOOK/ESSENTIALS invariants.

If Stage 2 goes to NEW chat: fresh chat has no context; response
collapses to restating known audit findings. Stage 2 adds no signal —
equivalent to the rejected audit-sync shortcut in different form.

If Stage 2 goes to OLD chat: architect's lived knowledge (priorities,
mental model, in-flight decisions, recent concerns) is captured before
context dies. Non-substitutable.

> If your repo has no OLD chat (no prior browser session), use the
> most recent ai-council architect chat that has project context.
> If truly no prior context exists, this may be a bootstrap, not a
> handoff — 3-stage flow still runs but Stage 2 will be thinner.

---

## Trigger phrases
<!-- scope: meta -->

Rob in Claude Code (.dev-knowledge) says one of:

| Phrase | Effect |
|---|---|
| "Make handoff for {repo}" | Stage 1 (default type: session-sync) |
| "Make handoff for {repo}, type {type}" | Stage 1 with explicit type |
| "Complete handoff for {repo}" | Stage 3 (requires stage2-response.md present) |
| "Stage 3 for {slug}" | Stage 3 by exact slug |
| "Save this response as stage 2 for {slug}" | Write stage2-response.md from current chat |

Explicit types: `audit-sync`, `session-sync`, `feature-X-sync` (where X is descriptive).
Handoffs are explicitly triggered by Rob. Claude Code does not propose handoff generation
unprompted.

---

## State tracking
<!-- scope: meta -->

`docs/handoffs/_in_progress/{slug}/` directory tracks in-progress handoffs.

`{slug}` = `{YYYY-MM-DD}-{repo}-{type}` where date is from Stage 1 trigger.

| Files present in `_in_progress/{slug}/` | Detected stage | Action |
|---|---|---|
| (directory absent or empty) | Stage 0 | Run Stage 1 |
| `stage1-question.md` + placeholder `stage2-response.md` | Stage 1 done, awaiting Stage 2 | Show Rob "paste old chat response into stage2-response.md, replacing the placeholder block" |
| `stage1-question.md` + populated `stage2-response.md` | Stage 2 done, ready for Stage 3 | Run Stage 3 |

**Stage 2 content detection:** Stage 1 pre-creates `stage2-response.md` as a
placeholder template. Stage 3 trigger must verify it has been populated:
- File exists AND content below the `═══ REPLACE EVERYTHING BELOW THIS LINE ═══`
  marker contains all 5 expected headings (`### 1. OBJECTIVE` through
  `### 5. BOUNDARIES`) with substantive content (not placeholder `[old chat answer]` text)
- If file exists but contains placeholder only: report "Stage 2 not yet provided —
  old chat response awaited. Open `stage2-response.md`, replace the placeholder
  block with architect response." Do NOT proceed to Stage 3.

If state is ambiguous (e.g., both files populated but Rob says "make handoff" again),
FLAG and ask Rob: delete and restart, or proceed to Stage 3?

---

## Stage 1 — Question generation
<!-- scope: hybrid -->

**Trigger:** "Make handoff for {repo}" or "Make handoff for {repo}, type {type}"

**Procedure:**

1. Determine slug: `{YYYY-MM-DD}-{repo}-{type}` (use today's date)
2. Verify target repo path exists and is a git repository
3. Capture target repo state:
   - HEAD SHA (`git rev-parse HEAD`)
   - Branch (`git branch --show-current`)
   - Working tree status (`git status --porcelain`)
4. Read `.dev-knowledge/BACKLOG.md`, identify items relevant to {repo}
5. If `audit-sync` type: read `.dev-knowledge/docs/audits/` for relevant audit
   reports; load findings as Stage 1 context — they inform question generation
   but do NOT substitute for Stage 2
6. Read `templates/HANDOFF_QUESTION_TEMPLATE.md`
7. Create directory `docs/handoffs/_in_progress/{slug}/`
8. Generate `docs/handoffs/_in_progress/{slug}/stage1-question.md` per
   `templates/HANDOFF_QUESTION_TEMPLATE.md` two-section structure:
   - Metadata header: target repo, HEAD SHA, branch, working tree state,
     timestamp, type, slug
   - Section A (Rob's operational instructions only — NOT pasted into old chat):
     which chat to open, which block to copy, where to save response, what
     command to issue next
   - PASTE_BOUNDARY delimiter (thick `═` line — visually unmistakable)
   - Section B (paste-this block for old chat) — MUST follow this order:
     1. Title
     2. Your role (project architect, not ecosystem oracle; witnessed vs
        inferred vs unknown — old chat must read this BEFORE questions)
     3. What's in handoff bundle (VISION/PLAYBOOK/ESSENTIALS/ADR essences/
        audit report/repo snapshot — so old chat doesn't repeat these)
     4. Epistemic honesty instruction (witnessed/inferred/unknown markers)
     5. Format requirements (markdown, exact headings, no fence wrap)
     6. Current state (Stage 1 captured metadata)
     7. Audit context (if audit-sync; informational only — extend/correct)
     8. BACKLOG items relevant to repo
     9. Pipeline questions (5 SBAR/I-PASS questions with inline epistemic
        notes per question)
     10. End-of-paste divider
   - Sections 2-5 (role, bundle, epistemic, format) MUST be at TOP of
     Section B — old chat reads these before drafting response. Placing
     them at end (as in v3.1 first iteration) caused old chat to produce
     plain-text headings, fabricated specifics, and duplicated ecosystem
     info it doesn't actually know.
   - NOTE: receiver synthesis prompt is NOT included in stage1-question.md.
     It belongs in Stage 3 output (00_first-message.md) per HANDOFF_FOLDER_TEMPLATE.
9. Pre-create `docs/handoffs/_in_progress/{slug}/stage2-response.md` as a
   placeholder template with:
   - Header block: repo, type, slug, timestamp
   - HTML comment for Rob with step-by-step instructions
   - `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker
   - Placeholder 5-section skeleton (headings + `[old chat answer]` text)

   This file is committed alongside stage1-question.md. Rob opens it when
   returning from old chat, replaces the placeholder block, saves.
10. Append JOURNAL entry under today's date:
    `- Handoff Stage 1 generated for {slug}: HEAD {SHA} captured; awaiting Stage 2`
11. Run validators (`python scripts/validate_scope_tags.py`, `pre-commit run --all-files`)
12. Single commit on feature branch (includes both stage1-question.md and stage2-response.md)
13. Report to Rob:
    - Stage 1 complete
    - Files created: `_in_progress/{slug}/stage1-question.md` (questions) and
      `_in_progress/{slug}/stage2-response.md` (awaiting architect response)
    - Next: open the EXISTING (OLD) browser chat for {repo}; copy the PASTE_BOUNDARY
      block from stage1-question.md into that chat; receive response; open
      stage2-response.md, replace placeholder block with response; save
    - Then: say "complete handoff for {repo}" to trigger Stage 3

**Output:** `_in_progress/{slug}/stage1-question.md` + `_in_progress/{slug}/stage2-response.md`
(placeholder), JOURNAL entry, single commit

---

## Stage 2 — Architect response (Rob's manual step in OLD chat)
<!-- scope: llm -->

**Source:** OLD browser chat for {repo} — the existing chat being
wrapped up due to context exhaustion. **NOT a new chat.**

**Input:** Content of `_in_progress/{slug}/stage1-question.md`

**Procedure (Rob does this manually):**

1. Open the EXISTING (OLD) browser chat for {repo} — the chat being
   wrapped up. It holds the accumulated context being preserved.
2. Paste the "Context for browser-2 architect" section through end of
   `stage1-question.md` as a message in that chat.
3. OLD chat architect answers all 5 pipeline questions (OBJECTIVE /
   REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) from lived knowledge:
   priorities, mental model, in-flight decisions, recent concerns.
4. Open the pre-created `_in_progress/{slug}/stage2-response.md` (Stage 1
   created this file as a placeholder template). Replace everything below the
   `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with the architect's
   response. Save.
   - Option A: Rob edits the file directly (open in editor, replace placeholder)
   - Option B: In Claude Code — "save this response as stage 2 for {slug}";
     Claude Code overwrites the placeholder block with response content

**Output:** `_in_progress/{slug}/stage2-response.md` populated with architect response

**Critical:** Stage 2 MUST go to OLD chat. A new chat has no context;
its response would collapse to restating audit findings — equivalent to
the rejected shortcut. The architecture depends on tacit knowledge
extraction from the existing session before context dies.

No separate commit at this step — Rob edits the file locally. Stage 3
commit includes the populated stage2-response.md as a modified file.

---

## Stage 2.5 — Q&A iteration loop (optional)
<!-- scope: meta -->

Between Stage 2 (architect response) and Stage 3 (folder generation),
NEW chat may have clarification questions before acting on the bundle.
Optional iteration phase — bypassed if NEW chat has no questions.

**Procedure (Rob's manual step):**

1. NEW chat (Browser-3) presents synthesis after reading bundle
2. If NEW chat asks clarification questions:
   - Format: numbered list, max 3 questions per round
   - Rob takes to OLD chat (Stage 2 source)
   - OLD chat answers
   - Rob returns answers to NEW chat
3. NEW chat updates synthesis, may have follow-up questions (round 2)
4. Maximum 3 rounds total
5. Each round captured in
   `docs/handoffs/_in_progress/{slug}/stage2-amendments.md`

**When to ask vs proceed:**
- Genuine ambiguity in directives → ask
- Missing factual context → ask
- Synthesis paraphrase reveals misunderstanding → ask
- Pure execution detail → proceed, flag in evidence

**Maximum rounds (3) rationale:**
- Rounds 1-2 typically sufficient
- Round 3+ signals fundamental bundle inadequacy → restart Stage 2
- Prevents infinite loop

**Stage 3 readiness:**
After Q&A loop closed (or skipped), NEW chat asks Rob "single prompt or
split?" Then generates Claude Code prompt(s) and proceeds to Stage 3
(Rob runs prompts in Claude Code in target repo).

---

## Stage 3 — Reconciliation + folder generation
<!-- scope: hybrid -->

**Trigger:** "Complete handoff for {repo}" or "Stage 3 for {slug}"

**Procedure:**

1. Verify `_in_progress/{slug}/stage1-question.md` exists — if missing, FLAG and STOP
2. Verify `_in_progress/{slug}/stage2-response.md` exists — if missing, FLAG and STOP
   with message: "Stage 2 not complete. Paste browser-2 response as stage2-response.md first."
3. Re-capture target repo state:
   - Current HEAD SHA
   - Compare to Stage 1 SHA (from `stage1-question.md` header)
   - If drifted: FLAG to Rob with both SHAs, ask whether to proceed or abort and
     re-generate Stage 1 (do NOT silently proceed)
4. Read `templates/HANDOFF_FOLDER_TEMPLATE.md`
5. Read `.dev-knowledge` VISION.md, protocols/PLAYBOOK.md, protocols/ESSENTIALS.md
6. Read `_in_progress/{slug}/stage2-response.md`
7. Identify ADRs cited in DIRECTIVES (07_ACTION_PLAN content)
8. Generate folder `docs/handoffs/{slug}/` with 11 files (all flat, no subdirectories):
   - `00_README.md` — Rob's upload instructions
   - `00_first-message.md` — browser-2 first message + receiver synthesis prompt
   - `01_MANIFEST.md` — entry, file index, drift verification, HEAD SHA
   - `01_manifest.json` — machine-readable metadata + SHA-256 of all files (generated last)
   - `02_VISION.md` — full copy of `.dev-knowledge/VISION.md`
   - `03_PLAYBOOK.md` — full copy of `.dev-knowledge/protocols/PLAYBOOK.md`
   - `04_ESSENTIALS.md` — full copy of `.dev-knowledge/protocols/ESSENTIALS.md`
   - `05_GOVERNANCE_ESSENCES.md` — 2-4 sentence essences for ADRs cited in directives
   - `06_STATE_OF_PLAY.md` — REALITY + RATIONALE answers from Stage 2; audit findings
     if audit-sync; deferred items as BACKLOG references (do not duplicate queue)
   - `07_ACTION_PLAN.md` — OBJECTIVE + DIRECTIVES + BOUNDARIES from Stage 2
   - `08_TREE.txt` — `git ls-files` output in target repo at Stage 3 time
   - `09_EXECUTION_EVIDENCE.md` — empty return-trip template
9. Compute SHA-256 of every file in folder, populate `01_manifest.json`
10. Move `_in_progress/{slug}/` to `docs/handoffs/_archive/{slug}/`:
    - `_archive/{slug}/stage1-question.md`
    - `_archive/{slug}/stage2-response.md`
    This preserves Stage 1+2 inputs for traceability without violating flat structure
    of the final handoff folder.
11. Append JOURNAL entry under today's date:
    `- Handoff Stage 3 complete for {slug}: folder at docs/handoffs/{slug}/`
12. Append CHANGELOG entry under today's date (Changed or Added section)
13. Review BACKLOG.md: if any P1 items were closed by this handoff, update Status
14. Run validators (`python scripts/validate_scope_tags.py`, `pre-commit run --all-files`)
15. Single commit on feature branch
16. Report to Rob:
    - Stage 3 complete
    - Folder: `docs/handoffs/{slug}/`
    - The OLD chat (Stage 2 source) can now be closed — its knowledge
      is preserved in the handoff bundle.
    - Next: open a NEW claude.ai chat for {repo} (fresh start). Zip +
      upload the folder contents to that new chat. Paste
      `00_first-message.md` as the first message.
    - New chat executes directives, fills `09_EXECUTION_EVIDENCE.md`
    - Return that file to `.dev-knowledge` for next session reference

**Output:** `docs/handoffs/{slug}/` (11 files flat) + `docs/handoffs/_archive/{slug}/`
(stage1 + stage2 inputs), JOURNAL + CHANGELOG entries, commit

---

## Folder structure (per ADR-42)
<!-- scope: meta -->

```
docs/handoffs/{date}-{slug}/
├── 00_README.md                 (Rob's upload instructions)
├── 00_first-message.md          (browser-2 first message, copy-paste)
├── 01_MANIFEST.md               (entry point, file index, HEAD pin)
├── 01_manifest.json             (machine-readable, SHA-256 checksums)
├── 02_VISION.md                 (FULL .dev-knowledge VISION copy)
├── 03_PLAYBOOK.md               (FULL .dev-knowledge PLAYBOOK copy)
├── 04_ESSENTIALS.md             (FULL .dev-knowledge ESSENTIALS copy)
├── 05_GOVERNANCE_ESSENCES.md    (ADR essences relevant to actions)
├── 06_STATE_OF_PLAY.md          (current state, audit findings)
├── 07_ACTION_PLAN.md            (goals, directives, boundaries)
├── 08_TREE.txt                  (target repo file inventory)
└── 09_EXECUTION_EVIDENCE.md     (return trip template)
```

Stage 1+2 inputs archived separately at:
```
docs/handoffs/_archive/{slug}/
├── stage1-question.md
└── stage2-response.md
```

Slug format: `{YYYY-MM-DD}-{repo}-{type}`. Final folder immutable post-close.

---

## File responsibilities
<!-- scope: meta -->

| File | Purpose | Content origin |
|---|---|---|
| `00_README.md` | Rob's instructions: how to use this handoff | Generated by Claude Code |
| `00_first-message.md` | Copy-paste for browser-2 first message | Generated by Claude Code |
| `01_MANIFEST.md` | Entry point, file index, HEAD pin, receiver synthesis prompt | Generated by Claude Code |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums | Generated by Claude Code (last) |
| `02_VISION.md` | Ecosystem context | Full copy of `.dev-knowledge/VISION.md` |
| `03_PLAYBOOK.md` | HOW we work — methodology preserved across sessions | Full copy of `.dev-knowledge/protocols/PLAYBOOK.md` |
| `04_ESSENTIALS.md` | High-leverage cheat-sheet rules | Full copy of `.dev-knowledge/protocols/ESSENTIALS.md` |
| `05_GOVERNANCE_ESSENCES.md` | ADR rules driving specific actions in this handoff | Curated by Claude Code from relevant ADRs |
| `06_STATE_OF_PLAY.md` | Current State per ADR-37 | Stage 2 REALITY/RATIONALE answers + audit findings if audit-sync |
| `07_ACTION_PLAN.md` | Future State per ADR-37 | Stage 2 OBJECTIVE/DIRECTIVES/BOUNDARIES answers |
| `08_TREE.txt` | Target repo file inventory at Stage 3 | `git ls-files` in target repo |
| `09_EXECUTION_EVIDENCE.md` | Return trip: browser-2 fills post-work | Empty template, filled by next session |

**Invariant rule:** `02_VISION.md`, `03_PLAYBOOK.md`, `04_ESSENTIALS.md` are FULL
copies — never curated. They are the methodology anchors that prevent browser-2 from
hallucinating norms.

**ADR essence rule:** `05_GOVERNANCE_ESSENCES.md` includes ONLY ADRs cited in
`07_ACTION_PLAN.md` directives. Format per essence: title + 2-3 operational
sentences + reference path to full ADR.

---

## Drift mitigation
<!-- scope: dev -->

Stage 1 captures target repo HEAD SHA in `stage1-question.md` header. Stage 3
re-verifies before generation:

- **Match:** proceed
- **Mismatch:** Claude Code STOPS, flags to Rob with both SHAs, asks whether to
  proceed (Rob may abort and re-generate Stage 1 from current HEAD)

`01_manifest.json` SHA-256 checksums prevent post-generation file tampering.

Browser-2 first action upon opening handoff: verify HEAD SHA via `git rev-parse HEAD`
in target repo. Mismatch → STOP, report drift, do not proceed.

---

## Return trip
<!-- scope: hybrid -->

`09_EXECUTION_EVIDENCE.md` is filled by browser-2 or Claude Code in target repo after
completing handoff work. Provides:
- Commands run (raw stdout)
- Test results (pytest output)
- Git diffs of changes made
- Final HEAD SHA after work
- Failures or partial completions (explicit, not omitted)
- Handoff for next session if applicable

Next `.dev-knowledge` session reads `09_EXECUTION_EVIDENCE.md` to verify what actually
happened — eliminates "Self-Correction Theatre."

---

## Validation checkpoints
<!-- scope: meta -->

| Stage | Validator | Expected result |
|---|---|---|
| Stage 1 | `python scripts/validate_scope_tags.py` | passes, hybrid ≤25% |
| Stage 1 | `pre-commit run --all-files` | passes |
| Stage 1 | `git status` | single new file (`_in_progress/{slug}/stage1-question.md`) + JOURNAL modified |
| Stage 3 | `python scripts/validate_scope_tags.py` | passes |
| Stage 3 | `pre-commit run --all-files` | passes |
| Stage 3 | folder structure | 11 files flat in `docs/handoffs/{slug}/`, no subdirectories |
| Stage 3 | `01_manifest.json` | SHA-256 entries for all 11 files present |

---

## Roles
<!-- scope: meta -->

- **Rob.** Triggers handoff (never browser-2 unprompted), reviews Stage 1 question
  prompt, carries browser-2 response back (Stage 2), accepts handoff folder.
- **Claude Code (.dev-knowledge).** Executes Stage 1 and Stage 3: reads target repo
  state, generates question prompt, generates folder, computes checksums, runs
  validators, commits.
- **Browser-2 (target project chat).** Executes Stage 2: answers 5 pipeline questions
  with project-level intelligence. Also consumes the handoff: opens it, verifies HEAD
  SHA, provides receiver synthesis, executes directives, fills `09_EXECUTION_EVIDENCE.md`.

Browser-2 does NOT generate folders or run git in target repo (unless Rob explicitly
directs it to). Claude Code does NOT redesign architecture or invent session content.

---

## What changed v3.1 → v3.2
<!-- scope: meta -->

| Dimension | v3.1 | v3.2 |
|---|---|---|
| Q&A iteration | Not specified | Stage 2.5 optional phase, max 3 rounds |
| Operator synthesis confirmation | Implicit ("confirm before proceeding") | Exact phrases: "synthesis confirmed" / "synthesis correction: [text]" |
| 00_README content | How to use (5 steps) | Explicit 10-step operator workflow |
| 00_first-message content | Synthesis prompt + wait | Synthesis prompt + operator response handling + Q&A loop + prompt generation protocol + continuous improvement reminder |
| Continuous improvement | Not stated | VISION + ESSENTIALS mandate; default posture across ecosystem |

---

## What changed v3.0 → v3.1
<!-- scope: meta -->

| Dimension | v3.0 (morning) | v3.1 (afternoon) |
|---|---|---|
| Stage 2 mandate | Skipped for audit-sync | Mandatory for ALL handoff types |
| State tracking | None | `_in_progress/{slug}/` directory with stage detection |
| Trigger phrases | Loose ("Make handoff...") | Table with exact phrases and effects |
| Archive | Not specified | Stage 1+2 inputs archived at `docs/handoffs/_archive/{slug}/` |
| Validation checkpoints | Implicit | Explicit per-stage table |
| JOURNAL hook | Not specified | Stage 1 + Stage 3 append entries |
| CHANGELOG hook | Not specified | Stage 3 appends entry |
| BACKLOG integration | Read at Stage 1 | Read at Stage 1; update at Stage 3 if items closed |
| Drift detection | Stage 3 re-verifies | Stage 3 re-verifies AND flags both SHAs on mismatch |

---

## References
<!-- scope: meta -->

- `docs/decisions/ADR-42_handoff_format_v3.md` — authoritative source (amended 2026-05-09 afternoon)
- `docs/decisions/ADR-32_handoff_format.md` — v2.0 (§4 deprecated by ADR-42; §1-§3 extended)
- `docs/decisions/ADR-37_session_boundary_protocol.md` — two-phase Current/Future overlay
- `docs/decisions/ADR-41_cross_session_backlog_architecture.md` — BACKLOG as pending items source
- `docs/decisions/ADR-36_audit_tool_architecture.md` — read-only contract
- `templates/HANDOFF_QUESTION_TEMPLATE.md` — Stage 1 output skeleton
- `templates/HANDOFF_FOLDER_TEMPLATE.md` — Stage 3 folder structure spec
- Council #24 — "wygeneruj handoff" trigger phrase

---

## Section history
<!-- scope: meta -->

- v3.2 (2026-05-09 night) — Stage 2.5 Q&A iteration loop added (optional, max 3
  rounds, NEW chat asks clarification questions back to OLD chat before Stage 3).
  Operator workflow made explicit (10-step list in 00_README). Synthesis confirmation
  phrases mandated ("synthesis confirmed" / "synthesis correction: [text]"). Continuous
  improvement principle embedded in template specs. Authority: ADR-42 third amendment.
- v3.1 (2026-05-09 afternoon) — Stage 2 mandatory for ALL handoff types (audit-sync
  shortcut removed per amended ADR-42). Operational state tracking via
  `_in_progress/{slug}/` directory. Trigger phrase table. Per-stage validation
  checkpoints. JOURNAL hook per Stage 1 + Stage 3. CHANGELOG hook per Stage 3.
  BACKLOG update at Stage 3. Archive pattern: Stage 1+2 inputs at
  `docs/handoffs/_archive/{slug}/`. Drift flag reports both SHAs.
- v3.1 update (2026-05-09 later afternoon) — Stage 2 source semantics corrected
  per ADR-42 second amendment: Stage 2 source = OLD (existing, dying) chat;
  Stage 3 receiver = NEW (fresh) chat. 3-actor diagram added. Stage 2 section
  rewritten; Stage 1 + Stage 3 report steps updated with correct chat direction.
- v3.0 (2026-05-09 morning) — full rewrite per ADR-42. Three-stage flow, flat 11-file
  structure, VISION/PLAYBOOK/ESSENTIALS as mandatory invariants, standardized 5-question
  pipeline, `09_EXECUTION_EVIDENCE.md` return trip. ADR-32 §4 deprecated in favor of
  BACKLOG.md.
- v2.0 (2026-04-28) — full rewrite per ADR-32. 9-section HANDOFF.md, folder convention,
  point-in-time copies, charter + step-verification controls, extract-to-task mechanics.
- v1.x — superseded. Single-file Type A/B framing.
