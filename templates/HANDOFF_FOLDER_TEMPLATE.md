# Handoff Folder Template (Stage 3 output structure)

Used by Claude Code in .dev-knowledge during Stage 3 to generate the
handoff folder. See ADR-42 (amended) and HANDOFF_PROCESS.md v3.3.3 for full flow.

## Stage 3 inputs

Stage 3 reads from `docs/handoffs/in-progress/{slug}/`:
- `stage1-question.md` — required; contains Stage 1 HEAD SHA for drift check
- `stage2-response.md` — required; contains browser-2 architect answers

If either file is missing, Stage 3 STOPS and flags to Rob.

After Stage 3 completes, both files are moved to:
`docs/handoffs/archive/{slug}/` (sibling to final handoff folder, preserving
Stage 1+2 inputs for traceability without violating flat folder structure).

## Folder location

`.dev-knowledge/docs/handoffs/{date}-{slug}/`

Where:
- `{date}` = YYYY-MM-DD (date handoff is generated, not necessarily session date)
- `{slug}` = `{repo}-{type}` (e.g., `ai-council-audit-sync`)

Full example: `docs/handoffs/2026-05-09-ai-council-audit-sync/`

## Files (all flat, single level — no subdirectories)

### Bundle layers (two-layer contract, per ADR-57 / Council Q2)

The bundle has two layers:

- **Governance floor (unconditional — every handoff):** `02_VISION.md`,
  `03_PLAYBOOK.md`, `04_ESSENTIALS.md`. Full copies, never curated. Prevents norm
  hallucination; preserves drift detection. (Plus the structural files: README,
  first-message, manifests, governance essences, state, action plan, tree,
  execution evidence, gate probe, claims.)
- **Operational layer (scoped — selected per `next_session_scope`):** relevant
  `skills`, `gotchas`, and `JOURNAL` slices, included only when the next session's
  declared scope invokes them. Selected by the mapping table below, not ad-hoc
  sender judgment. Named `12_OPERATIONAL_{artifact}.md` (e.g.
  `12_OPERATIONAL_gotchas.md`, `12_OPERATIONAL_journal-slice.md`).

`next_session_scope` is a required bundle field (carried in `01_MANIFEST.md` and
`01_manifest.json`) from this controlled vocabulary:

| Scope | Operational layer includes |
|---|---|
| `code-implementation` | relevant skills (per task domain) + gotchas filtered by scope + recent JOURNAL slice |
| `architecture-decision` | relevant ADRs (cite specific) + Council transcripts (if applicable) + recent JOURNAL slice |
| `audit-work` | audit tool docs + baseline audit (if exists) + JOURNAL audit history |
| `documentation` | style references + recent JOURNAL slice + templates in scope |
| `mixed-uncertain` | full bundle (worst-case) + flag for operator |

`mixed-uncertain` is the fail-safe: when scope is unclear, ship the worst-case
superset and flag for operator review. The vocabulary is intentionally small;
expand only by amending this table and the matching one in `HANDOFF_PROCESS.md`.

### 00_README.md

Purpose: operator instructions for using the handoff bundle.

Content (in order):

#### What this folder is
- Brief identification (date, type, target repo, format version)
- Note that OLD chat (Stage 2 source) can be closed; its knowledge is
  in this bundle
- Reference to _archive location for Stage 1+2 inputs

#### Operator workflow (explicit 10-step list)

1. Open NEW claude.ai chat (fresh, zero context — NOT the OLD chat)
2. Drag-drop all {N} files from this folder, OR zip and upload zip
3. Paste content of `00_first-message.md` as first message
4. NEW chat reads bundle, presents receiver synthesis
5. Confirm synthesis. Type exact phrase:
   - `synthesis confirmed` (proceeds to Q&A or prompt generation)
   - `synthesis correction: [specifics]` (NEW chat updates, re-presents)
6. Q&A loop (if NEW chat asks clarification questions):
   - NEW chat presents up to 3 questions
   - Take questions to OLD chat (Stage 2 source — the chat being
     wrapped up)
   - Get answers from OLD chat
   - Paste answers back to NEW chat
   - Repeat up to 3 rounds total
   - After round 3 OR when NEW chat says "no more questions":
     proceed
7. NEW chat asks: "single Claude Code prompt or split?"
   Answer based on directive complexity:
   - Single prompt: small directive count, no verification gates
   - Split: 5+ directives OR verification-critical gate (architect
     claim contradicted by repo state, etc.)
8. NEW chat generates Claude Code prompt(s) as downloadable .md
   files. Download them.
9. Open Claude Code in target repo (NOT in .dev-knowledge). Paste
   prompts sequentially. Claude Code executes.
10. Return final 09_EXECUTION_EVIDENCE.md to `.dev-knowledge` for
    review (commit to `.dev-knowledge/docs/handoffs/{slug}/` after
    Stage 3 archive)

#### File index
[Standard table — {N} files, one-line purpose each]

Note on 02_VISION.md: describe as "{repo} VISION.md — target repo's mission and scope".
Note on 02b_ECOSYSTEM_VISION.md (conditional): describe as ".dev-knowledge VISION.md —
ecosystem methodology context (present only for cross-repo handoffs)". If target = .dev-knowledge,
omit 02b row entirely. {N} = 13 (self-applied) or 14 (cross-repo) fixed files
(adds `10_GATE_PROBE.md` + `11_CLAIMS.md` per ADR-55/ADR-58), plus operational-layer
artifacts (variable count per `next_session_scope`, per ADR-57).

#### Notes
- This bundle is the Stage 3 handoff per ADR-42 v3.2
- Stage 1 + Stage 2 inputs archived at
  `.dev-knowledge/docs/handoffs/archive/{slug}/`
- If Q&A loop produces amendments, they are also in archive at
  `archive/{slug}/stage2-amendments.md`

### 00_first-message.md

Purpose: First message for the NEW (fresh) chat receiving this handoff bundle.
Tells NEW chat its role, reading order, synthesis requirements, Q&A protocol,
and prompt generation protocol.

Content (in order):

#### Identification
- "You are receiving a handoff bundle for {repo}."
- "You are a fresh chat with zero prior history of this project."
- "All context you need is in these uploaded files."
- Note OLD chat is closed; its knowledge in 06_STATE_OF_PLAY + 07_ACTION_PLAN

#### Reading order
- Numbered list of files to read in order
- Skip note for 01_manifest.json (machine-readable)
- Note after 02_VISION.md: read `02b_ECOSYSTEM_VISION.md` next if present
  (ecosystem methodology context; skip if not in bundle)

#### State validation
- Commands operator should run (browser chat can't run shell)
- Expected HEAD SHA (ancestor-validated: current HEAD must be a descendant of the pinned SHA), working tree state
- Mismatch instruction: STOP, report both SHAs

#### Required first action — applied-task gate (per ADR-55, Council Q1)

The paraphrase gate is replaced by an applied-task proof gate: the NEW chat must
APPLY bundle content to decide an action, not paraphrase it. (The 2026-05-25
evidence showed chats passing a paraphrase gate then failing to operationalize the
same content one turn later.) 00_first-message.md MUST instruct the new chat:

**Step 1 — Grounding (citation-anchored).** Write in your own words, with a
file + section citation for each:

1. **Your role per VISION** — `{repo}`'s function in the ecosystem and your role as
   its architect this session. Citation: `02_VISION.md#{section}` (and
   `02b_ECOSYSTEM_VISION.md` for ecosystem context if present).
2. **Top-3 hard constraints** — what must NOT happen this session. Citation:
   `07_ACTION_PLAN.md` Hard Constraints section.

Anchor on file + heading/section — not line numbers (avoids citation brittleness).

**Step 2 — Applied-task proof.** Read `10_GATE_PROBE.md` — the **mini-scenario and
required-response-structure ONLY**. Do NOT read the operator-only block (the answer
key). Answer:

1. **Directed action** — what should be done.
2. **Controlling bundle location** — the file + section that determines the action.
3. **Preconditions / sequencing** — any pre-work or order constraints.

**Confirmation.** The operator checks your answer against the operator-only expected
answer and types `role confirmed + probe passed` (this replaces bare
`role confirmed`). Do not proceed until you receive it.

**Failure protocol.**
- First fail → operator points to the contradicted bundle location; re-read and
  retry the probe once.
- Second fail → the session terminates; the bundle is treated as inadequate and
  regenerated upstream.

If you cannot ground item 1 or 2 from the bundle, flag the gap
(`Cannot ground [role/constraints] — [file] insufficient. Reload or query.`) and
do not proceed.

This is friction-gated entry: the operator validates *application*, not paraphrase,
before work begins. The applied-task gate precedes receiver synthesis — synthesis is
the second gate after this one passes.

#### Receiver synthesis (MANDATORY before action)
After reading the full bundle, NEW chat MUST provide synthesis. Format:

> "I will execute **{goal from 07 OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06}**.
>
> Reasoning: **{paraphrase 07 RATIONALE}**.
>
> I will execute in order: **{DIRECTIVES list}**.
>
> I will NOT do: **{BOUNDARIES list}**.
>
> Verification: HEAD is {head} OR a descendant of it (working tree {state}).
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, NEW chat MUST wait for operator response.

#### Operator response handling

Operator will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. NEW chat proceeds:
   ask if any clarification questions remain (Q&A loop) OR ask "single
   Claude Code prompt or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. NEW chat
   updates understanding based on correction, re-presents synthesis.
   Repeat until operator confirms.

3. **Other text** — treat as correction or question. Re-present synthesis
   incorporating operator's input.

#### Q&A iteration loop (if needed)

If NEW chat has clarification questions BEFORE generating prompts:

1. After synthesis confirmed, NEW chat presents:
   "I have {N} clarification questions before generating prompts:
   1. {question 1}
   2. {question 2}
   3. {question 3}
   (max 3 per round)
   Please route these to OLD chat and return answers."

2. Operator takes questions to OLD chat, gets answers, returns
3. NEW chat updates synthesis with answers, may have follow-up
   questions (round 2)
4. Maximum 3 rounds. After round 3, NEW chat must proceed with best
   available understanding OR ask operator to restart Stage 2

When NEW chat has no more questions, it asks operator: "Ready to
generate Claude Code prompt(s)? Single prompt or split?"

#### Prompt Generation Card (per ADR-56, Council Q3)

Inline operational extract — the browser chat cannot read the filesystem, so the
procedure lives here at the point of use. PLAYBOOK retains rationale + edge cases;
this card is the procedure. (Replaces the prior "generate per 03_PLAYBOOK
conventions" pointer, which did not reliably reproduce the procedure.) After the
Q&A loop closes and the operator confirms format (single/split), the NEW chat
generates Claude Code prompt(s) using this card:

**Decision algorithm:** classify task → choose model + mode + effort → fill the
mandatory skeleton → validate (matches archetype, skeleton complete, no
hallucinated paths).

**Task archetype → model + mode + effort** (mirrors PLAYBOOK; keep in sync):

| Task archetype | Model | Mode | Effort |
|---|---|---|---|
| Mechanical single-file edit / config / rename | Sonnet | auto-accept | low |
| Write tests for a module (clear spec) | Sonnet | auto-accept | medium |
| Multi-file refactor within known patterns | Sonnet/Opus | plan-then-auto | medium |
| New pipeline step / feature (cross-file) | Opus | plan-then-auto | high |
| Cross-package / schema migration | Opus | plan | high |
| Audit / review / synthesis (judgment-heavy) | Opus | plan-then-auto | high |
| Hardest debugging / end-to-end verification | Opus | plan | xhigh |
| Architecture decision | (not a prompt — convene AI Council) | — | — |
| Code review (security/quality) | (Codex per ADR-54, after Opus implementation) | — | — |
| **Uncertain / mixed** | **Opus** | **plan** | **high + operator review** |

**Mandatory prompt skeleton** — every generated Claude Code prompt MUST contain:

1. Model/Mode/Effort table (top).
2. Title (single sentence).
3. Repo + Purpose.
4. Read first — CLAUDE.md, relevant gotchas, relevant skills (per `next_session_scope`).
5. **Git workflow** — feature branch + multiple revertable commits + test between
   steps + **no auto-push** (operator approves merge).
6. UNDERSTAND — scope + failure modes + what NOT to do.
7. Steps — with COMMIT markers between them.
8. **Hooks needed** — yes/no + which (see Hook selection below).
9. **JOURNAL update target** — per ADR-49 (append: date / did / result / adaptation
   / pattern / next).
10. **Workflow updates needed** — if the task changes PLAYBOOK/templates/process,
    list them.
11. Final — tests + verification + session report.
12. What NOT to do — explicit guards + scope-leak prevention.

(Skeleton items 5, 8, 9, 10 are operator extensions, equal in weight to the
Council-derived card; do not drop them.)

**Hook selection guidance:**

| Task triggers | Consider hook |
|---|---|
| Code changes | pre-commit (lint + test) |
| State-changing tool calls | PreToolUse (gate before destructive ops) |
| Bundle integrity work | `/save` (manifest hash verification per ADR-42 Q5 amendment) |
| Long sessions | SessionStart + Stop |
| Default (no trigger) | none — do not add hooks speculatively |

**Fallback:** task type unclear, multiple archetypes apply, or domain unfamiliar →
**Opus + high effort + mark for operator review.**

**Worked exemplars:**
- *Mechanical (Sonnet / auto-accept / low):* "Add type hints to `utils/parsing.py`;
  run mypy strict; one commit." → mechanical single-file; no hooks; minimal JOURNAL.
- *Multi-file refactor (Opus / plan-then-auto / medium):* "Extract `ConfigLoader`
  from `cli.py` into `config/loader.py`; update 4 call sites; add tests." →
  pre-commit hook for test validation; JOURNAL update; workflow unchanged.
- *Audit (Opus / plan-then-auto / high):* "Audit corp-monorepo against current
  .dev-knowledge baseline; produce findings + execution plan." → no hooks; JOURNAL
  update; workflow may need update if findings drive an ADR amendment.

Output each prompt as a downloadable `.md`; the operator runs it in Claude Code in
the target repo.

**Card maintenance:** any change to prompt conventions updates BOTH this card and
the PLAYBOOK rationale (ADR-56). Size budget: keep the card ≤200 lines; if it
overflows, restructure into card + appendix rather than relocating authority.

#### Continuous improvement reminder
- Project's meta-goal is continuous improvement (per .dev-knowledge
  VISION + ESSENTIALS)
- Immediate session scope is in 07_ACTION_PLAN
- Long-term posture: always advancing the project
- After execution, NEW chat encourages operator to capture lessons
  for next session

Note: receiver synthesis prompt belongs in 00_first-message.md (Stage 3
output, new chat), NOT in stage1-question.md (Stage 1 output, old chat).
Old chat answers questions; it does not synthesize before responding.

### 01_MANIFEST.md

Purpose: Entry point, navigation, drift verification, receiver synthesis.

Content:
- Handoff metadata (date, type, target, generated by, format version)
- Target repo state at Stage 3: HEAD SHA, branch, working tree state
- File index with one-line purpose each (same 02_VISION / 02b conditional rules as 00_README.md)
- HEAD verification instructions for Browser-2
- Receiver synthesis prompt (echoed from 00_first-message.md)
- Reference to 07_ACTION_PLAN.md as operational center

### 01_manifest.json

Purpose: Machine-readable metadata + SHA-256 checksums for drift detection.

Schema:
```json
{
  "handoff_id": "{date}-{slug}",
  "type": "{audit-sync|session-sync|feature-X-sync}",
  "format_version": "v3.0",
  "generated_at": "{ISO 8601 timestamp}",
  "target_repo": {
    "name": "{repo}",
    "path": "{absolute path}",
    "head_sha": "{40-char SHA}",
    "branch": "{branch name}",
    "working_tree": "{clean|modified}"
  },
  "stage_2_provided": true,
  "files": [
    {"path": "00_README.md", "sha256": "..."},
    {"path": "00_first-message.md", "sha256": "..."},
    {"path": "01_MANIFEST.md", "sha256": "..."},
    {"path": "02_VISION.md", "sha256": "..."},
    {"path": "02b_ECOSYSTEM_VISION.md", "sha256": "...", "conditional": "omit when target_repo == .dev-knowledge"},
    {"path": "03_PLAYBOOK.md", "sha256": "..."},
    {"path": "04_ESSENTIALS.md", "sha256": "..."},
    {"path": "05_GOVERNANCE_ESSENCES.md", "sha256": "..."},
    {"path": "06_STATE_OF_PLAY.md", "sha256": "..."},
    {"path": "07_ACTION_PLAN.md", "sha256": "..."},
    {"path": "08_TREE.txt", "sha256": "..."},
    {"path": "09_EXECUTION_EVIDENCE.md", "sha256": "..."}
  ]
}
```

Note: `01_manifest.json` is generated LAST after all other files are written,
so its SHA-256 entries are accurate. It cannot include a checksum of itself.

### 02_VISION.md

Purpose: Target repo's mission and scope — why `{repo}` exists.
Content: FULL copy of `{repo}/VISION.md` (the handoff target's mission). Never curated.
Origin: `cp {TARGET_REPO_PATH}/VISION.md → 02_VISION.md`

### 02b_ECOSYSTEM_VISION.md

Purpose: Ecosystem methodology context — why `.dev-knowledge` exists, how it governs all repos.
Generated only when target repo ≠ `.dev-knowledge`. When target = `.dev-knowledge`, omit
entirely (02_VISION.md already is .dev-knowledge's VISION; 02b would be a duplicate).
Content: FULL copy of `.dev-knowledge/VISION.md`. Never curated.
Origin: `cp .dev-knowledge/VISION.md → 02b_ECOSYSTEM_VISION.md`

### 03_PLAYBOOK.md

Purpose: HOW we work — methodology preserved across sessions.
Content: FULL copy of `.dev-knowledge/protocols/PLAYBOOK.md`. Never curated.
Origin: `cp .dev-knowledge/protocols/PLAYBOOK.md → 03_PLAYBOOK.md`

### 04_ESSENTIALS.md

Purpose: High-leverage cheat-sheet rules.
Content: FULL copy of `.dev-knowledge/protocols/ESSENTIALS.md`. Never curated.
Origin: `cp .dev-knowledge/protocols/ESSENTIALS.md → 04_ESSENTIALS.md`

### 05_GOVERNANCE_ESSENCES.md

Purpose: Operational ADR rules relevant to current handoff actions.

Content: 2-4 sentence ADR essences for ADRs whose rules drive specific
actions listed in `07_ACTION_PLAN.md`. NOT full ADR copies.

Selection rule: only include ADRs explicitly cited in `07_ACTION_PLAN.md`
directives. If a directive says "per ADR-33", include ADR-33 essence.

Format per essence:
```
## ADR-NN — {Title}

{Operational rule: 2-3 sentences describing what must be done/avoided.}

Full ADR: `.dev-knowledge/docs/decisions/ADR-NN_{topic}.md`
```

### 06_STATE_OF_PLAY.md

Purpose: Current State per ADR-37.

Content:
- What was done in current/recent work (commits, decisions made)
- Decisions locked (with rationale — cite ADR if formalized)
- Audit findings (if audit-sync: P1/P2/P3 findings from audit report)
- Browser-2 REALITY + RATIONALE answers (Stage 2 input, if applicable)
- Deferred items: cite BACKLOG entry IDs and names, do NOT duplicate
  the queue content

### 06_STATE_OF_PLAY.md — section conventions

Section names use plain English, not SBAR codes. Canonical headings:
- `## What was completed this session` (was: REALITY)
- `## Current state` (HEAD, branch, working tree, tests, cycle status)
- `## Decisions locked this session` (was: RATIONALE recap, prose form)
- `## Deferred items` (BACKLOG references, not duplications)
- `## Rationale (architect judgment)` (was: RATIONALE — keep but narrative form)
- `## Stage 3 verification summary` (keep — already plain)

Absolute-date conversion rule: when copying REALITY content from `stage2-response.md`
into `06_STATE_OF_PLAY.md`, convert all relative time references to absolute dates.
Replace "yesterday", "this morning", "last week", "N days ago", etc. with the
actual calendar date (YYYY-MM-DD). Anchor: use Stage 1 HEAD date as reference.
This prevents time-anchored claims from becoming uninterpretable in future sessions.

Code gloss rule: first reference to any status code (P-NN priority, F-NN finding,
ADR-NN) within a section MUST include in-line gloss. Example:
  `P1 [governance-blocking] — F-01 [first finding from 2026-05-12 audit] —
   VISION.md absent per ADR-33 [vision-universalization].`
Subsequent references in same section may use bare code.

Sentence-form rule: verb-led sentences for state descriptions.
NOT: `amendment cycle closed`, `compliance verification`, `Stage 3 note — DoD fix target clarification`
DO:  `We stopped amending ADR-42 after the third clarification.`
     `Stage 3 flagged that the fix target is the generated file, not the template.`

### 07_ACTION_PLAN.md

Purpose: Future State per ADR-37.

Content:
- Goals (from Stage 2 OBJECTIVE answer, or audit priority order)
- Directives (numbered actions with verification steps, from Stage 2
  DIRECTIVES answer, or audit recommended order)
- Boundaries (do-not's, out-of-scope, fallbacks, from Stage 2 BOUNDARIES
  answer, or audit tier-dependency deferrals)
- Success criteria (how to verify the session succeeded)

### 07_ACTION_PLAN.md — section conventions

Section names use plain English, not SBAR codes:
- `## Next session goal` (was: OBJECTIVE) — 1-3 paragraphs of plain prose
- `## Action plan` (was: DIRECTIVES) — numbered list, each item:
  action verb + target + verification step
- `## Hard Constraints` (max 5 items, bold) — critical for next step,
  must-not-violate. Definition: violating this blocks the next session's
  primary work.
- `## Narrow scope rules` (rest of DO-NOTs, sub-bulleted or collapsed) —
  scope refinement that helps but isn't blocking.
- `## Fallback contingencies` (keep — already plain)
- `## Success criteria` (keep — already plain)

Same code gloss rule as 06 applies (first reference per section includes gloss).
Same verb-led sentence rule applies.

### 08_TREE.txt

Purpose: Target repo file inventory snapshot for structural orientation.

Content: Output of `git ls-files` in target repo at Stage 3 generation time.
Browser-2 can verify repo structure without additional uploads.

### 09_EXECUTION_EVIDENCE.md

Purpose: Return trip — Browser-2 or Claude Code in target repo fills
this out post-execution. Provides hard evidence for next session.

Initial content (empty template):
```
# Execution Evidence — {handoff_id}

## Commands run

(paste raw stdout here)

## Test results

(paste pytest output here)

## Git diffs

(paste `git diff HEAD~N..HEAD` or equivalent)

## Final HEAD SHA

(paste `git rev-parse HEAD` output after work is complete)

## Failures / partial completions

(describe anything that did not complete as planned)

## Handoff for next session (if applicable)

(brief state summary if more work remains)
```

### 10_GATE_PROBE.md

Purpose: verify the NEW chat internalized the bundle by APPLYING bundle content
to decide an action — not by paraphrasing it. Required bundle artifact per ADR-55
(Council Q1). Authored by the sender (OLD chat) during Stage 2; reviewed by the
sender; checked by the operator at Stage 3.

Numbering note: this file is `10_`, not `08_`. Council Q1 action item named
`08_GATE_PROBE.md`, but `08_TREE.txt`/`09_EXECUTION_EVIDENCE.md` already hold
08/09 (operator decision 2026-05-26 — no renumber).

Structure:

```
# Gate Probe — {handoff_date}

> Purpose: verify the NEW chat internalized the bundle by APPLYING it to decide
> an action, not by paraphrasing. Read the mini-scenario only; do NOT read the
> operator-only block below it.

## Mini-scenario

{1-2 paragraphs: a concrete situation where the NEW chat must use specific bundle
content to decide what to do. Drawn from the highest-risk live decision in this
handoff.}

## Required response structure

The NEW chat's answer must include:
1. Directed action — what should be done
2. Controlling bundle location — file + section that determines the action
3. Preconditions / sequencing dependencies — any pre-work or order constraints

<!-- OPERATOR-ONLY BELOW — DO NOT SHOW TO THE NEW CHAT BEFORE ITS PROBE RESPONSE -->

## Expected answer (operator-only)

{sender-authored expected answer derived from bundle content}

## Acceptable variations

{what counts as semantically correct vs failure}

## Failure rubric

- Pass: correct action + correct bundle-location citation + acknowledges preconditions
- Soft fail: correct action but missing location citation or preconditions → first retry permitted
- Hard fail: wrong action, contradicts bundle, or fabricates non-bundle content → terminate session + regenerate bundle upstream
```

Generation note: the operator-only block (everything below the OPERATOR-ONLY
comment) is the answer key. The NEW chat is instructed in `00_first-message.md` to
read only the mini-scenario + required-response-structure, never the answer key.

### 11_CLAIMS.md

Purpose: sender-side structured grounding of load-bearing claims, to stop
hallucination propagation across the handoff. Required bundle artifact per ADR-58
(Council Q4). Produced by the sender (OLD chat) as the FINAL Stage 2 output;
citations validated by Claude Code (executor) at Stage 3; ratified by the operator
before role confirmation. If the bundle changes materially after this file is
written, regenerate it.

Numbering note: this file is `11_`. Council Q4 named it `CLAIMS.md`; numbered
`11_` here (sequential after `10_GATE_PROBE.md`, operator decision 2026-05-26).

Structure:

```
# Claims — {handoff_date}

> Purpose: structured grounding of load-bearing claims. Each claim cites a source
> OR is marked an explicit assumption. Trigger rule: a confident claim about an
> unread/unverified source requires verification + citation.

## Load-bearing claims

| # | Claim | Source citation | Verifier |
|---|-------|-----------------|----------|
| 1 | {claim} | `file:section` / `ADR-NN` / `session: YYYY-MM-DD` | self / CC / operator |

## Explicit assumptions

| # | Assumption | Risk if wrong | Mitigation |
|---|-----------|---------------|------------|
| 1 | {assumption} | {consequence} | {guard} |

## Expected articulation (sender contract)

{short mapping of what the receiver should understand — supports operator review
without relying on the OLD chat being live}

## Verification status

- [ ] Sender self-verified all citations (locatable in cited source)
- [ ] CC validated citation existence + line-range locatability (Stage 3 executor check)
- [ ] Operator ratified before role confirmation

## Load-bearing claim definition

Decision-affecting (citation required): file paths, commit SHAs, ADR refs,
action plans/sequencing, architecture descriptions, current-state assertions.
Non-examples (no citation): reasoning steps, recommendations, opinions marked as such.
```

Degraded mode: if executor validation is unavailable, the handoff is marked
`UNVERIFIED`; the operator must explicitly acknowledge; no silent bypass.

---

## Stage 3 parsing logic (tolerant heading detection)

When parsing `stage2-response.md` to extract the 5 sections, use tolerant
heading detection. Match ANY of these patterns for section headings:

- `### N. NAME` (markdown level-3)
- `### **N. NAME**` (level-3 + bold)
- `**N. NAME**` (bold only)
- `## N. NAME` or `# N. NAME` (other markdown levels)
- `N. NAME` (plain numbered, no markdown)

Where N is 1-5 and NAME is OBJECTIVE, REALITY, RATIONALE, DIRECTIVES, or
BOUNDARIES (case-sensitive). Section content = everything from heading to
next heading (or end of file). Normalize all headings to `### N. NAME` in
output files.

If parsing fails (sections missing, out of order, content empty): FLAG to
Rob and ask for manual correction. Do not silently skip sections.

## Stage 3 verification layer

After parsing `stage2-response.md`, classify each factual claim:

**Verify (checkable from repo without execution):**
- Witnessed claims about file existence → `ls` or `git ls-files`
- Witnessed claims about config keys → read config files
- Witnessed claims about CLI entry points → read pyproject.toml
- Witnessed claims about commit existence → `git log --grep`

**Preserve without verification:**
- Conversation history claims ("we decided X in this chat")
- Architect inferences (already flagged with "(architect inference)")
- External service behavior ("OpenAI o4-mini intermittently fails")

**Architect unknowns:** attempt verification; if successful, replace unknown
with verified fact and note "Stage 3 verified"; if not, preserve as unknown.

**Verification report** in 06_STATE_OF_PLAY:
```
## Stage 3 verification summary
Architect provided {N} witnessed claims:
- {V} verified against repo state
- {U} unverifiable from repo (decision rationale, conversation history)
- {F} architect-flagged inferences (preserved with flag)
- {K} architect-flagged unknowns: {resolution of each}
```

**Flag mismatches:** if a witnessed claim can be checked but doesn't match
repo state, flag as "VERIFICATION FAILED — {claim} vs {actual}". Do not
silently accept incorrect witnessed claims.

## Generation steps (for Claude Code Stage 3)

1. Create folder `.dev-knowledge/docs/handoffs/{date}-{slug}/`
2. Verify `in-progress/{slug}/stage2-response.md` exists and contains
   substantive content (not placeholder "[old chat answer]") — if not, STOP
3. Parse `stage2-response.md` using tolerant heading detection (above)
4. Apply verification layer to architect's witnessed claims
5. Capture target repo HEAD SHA, branch, working tree state via git;
   compare to Stage 1 SHA from stage1-question.md — drift → FLAG to Rob
6. Generate `00_README.md` with upload instructions
7. Generate `00_first-message.md` with receiver synthesis prompt + HEAD SHA
8. Generate `01_MANIFEST.md` with metadata and file index
9. Copy VISION/PLAYBOOK/ESSENTIALS files:
   - `{TARGET_REPO_PATH}/VISION.md` → `02_VISION.md` (target repo's mission)
   - If target ≠ `.dev-knowledge`: `.dev-knowledge/VISION.md` → `02b_ECOSYSTEM_VISION.md`
   - `.dev-knowledge/protocols/PLAYBOOK.md` → `03_PLAYBOOK.md`
   - `.dev-knowledge/protocols/ESSENTIALS.md` → `04_ESSENTIALS.md`
10. Generate `05_GOVERNANCE_ESSENCES.md` (curated to ADRs cited in 07)
11. Generate `06_STATE_OF_PLAY.md` from Stage 2 REALITY + RATIONALE +
    audit findings + verification summary
12. Generate `07_ACTION_PLAN.md` from Stage 2 OBJECTIVE + DIRECTIVES +
    BOUNDARIES
13. Generate `08_TREE.txt` from `git ls-files` in target repo
14. Generate `09_EXECUTION_EVIDENCE.md` (empty template)
15. Include sender-authored `10_GATE_PROBE.md` and `11_CLAIMS.md` (Stage 2 outputs).
    Verify both are present; if missing, FLAG and STOP (per ADR-55 / ADR-58).
16. Validate `11_CLAIMS.md` citations (file existence + line-range locatability +
    decision-reference format). Flag mismatches as "VERIFICATION FAILED — {claim} vs
    {actual}". If executor validation is unavailable, mark the bundle `UNVERIFIED`
    and require explicit operator acknowledgment — no silent bypass (ADR-58).
17. Assemble operational-layer artifacts per `next_session_scope` (mapping table in
    "Bundle layers" above) as `12_OPERATIONAL_*` files. Governance floor is always
    full + unconditional; operational layer is scoped (ADR-57).
18. Compute SHA-256 of every file + canonical hash/version IDs for the invariant
    floor (VISION/PLAYBOOK/ESSENTIALS); populate `01_manifest.json` last, including
    `next_session_scope` (see `### 01_manifest.json` schema, per ADR-42 Q5 amendment)
19. Move `in-progress/{slug}/` to `docs/handoffs/archive/{slug}/`:
    - `archive/{slug}/stage1-question.md`
    - `archive/{slug}/stage2-response.md`
20. Update JOURNAL + BACKLOG
21. Run `python scripts/validate_scope_tags.py` and `pre-commit run --all-files`
22. Single commit on dedicated branch

---

## Content invariants (never violate)

- `02_VISION.md`: FULL copy of target repo's VISION.md — NEVER .dev-knowledge's VISION unless target IS .dev-knowledge
- `02b_ECOSYSTEM_VISION.md` (conditional): FULL copy of `.dev-knowledge/VISION.md` when target ≠ `.dev-knowledge`; omit entirely when target = `.dev-knowledge`
- `03_PLAYBOOK.md`, `04_ESSENTIALS.md`: FULL copies, no editing
- `05_GOVERNANCE_ESSENCES.md`: essences ONLY — 2-4 sentences each, never full ADR text
- Target repo's own ADRs: NEVER included — Browser-2 reads them in the repo
- No subdirectories: all fixed files — 13 (self-applied) or 14 (cross-repo) — plus
  any operational-layer artifacts at folder root, flat layout
- `10_GATE_PROBE.md` + `11_CLAIMS.md`: sender-authored at Stage 2 (not CC-generated);
  CC includes them in the bundle and validates `11_CLAIMS.md` citations at Stage 3
- Operational-layer artifacts: included only when `next_session_scope` invokes them
  (per the mapping table above); governance floor is always full + unconditional
- `01_manifest.json` generated last (after all other files) for accurate checksums
