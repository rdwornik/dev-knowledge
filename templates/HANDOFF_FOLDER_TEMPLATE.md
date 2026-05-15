# Handoff Folder Template (Stage 3 output structure)

Used by Claude Code in .dev-knowledge during Stage 3 to generate the
handoff folder. See ADR-42 (amended) and HANDOFF_PROCESS.md v3.3.2 for full flow.

## Stage 3 inputs

Stage 3 reads from `docs/handoffs/_in_progress/{slug}/`:
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
omit 02b row entirely. {N} = 11 (self-applied) or 12 (cross-repo).

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

#### Required first action — articulation gate

00_first-message.md MUST instruct the new chat that, before ANY work
(including receiver synthesis), it writes in its own words. Do not paste
from VISION/PLAYBOOK/ESSENTIALS — write fresh. Required content:

1. **Your role per VISION** (1-2 sentences) — what is `{repo}`'s
   function in the ecosystem? What is your role as architect for `{repo}` specifically?
   (For ecosystem methodology context — the governance framework this repo operates within —
   read `02b_ECOSYSTEM_VISION.md` if present in the bundle.)

2. **Current phase per BACKLOG** (1 sentence) — which phase of the
   universalization rollout is active? What blocks what?

3. **Immediate next action per ACTION_PLAN directive #1** (1 sentence) —
   what is the single highest-priority action for this session?

4. **Top 3 Hard Constraints** (from `07_ACTION_PLAN.md` Hard Constraints section)
   (3 short bullets) — what must NOT happen this session?

After writing the four-item articulation, wait for operator to type
exact phrase `role confirmed` before any other work. If you cannot
articulate any of the four items from the bundle, flag the gap:

  `Cannot articulate [N] — [VISION/BACKLOG/ACTION_PLAN/HARD_CONSTRAINTS]
   insufficient. Reload or query.`

Do not proceed.

This is friction-gated entry. Operator validates internalization before
work begins. The articulation precedes receiver synthesis — synthesis is
the second gate after articulation passes.

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

#### Prompt generation

After Q&A loop closed and operator confirms format (single/split):

- NEW chat generates formal Claude Code prompt(s) per 03_PLAYBOOK
  conventions:
  - Model/Mode/Effort table at top
  - Title, Repo, Purpose
  - Read first list
  - Git workflow
  - UNDERSTAND
  - Steps with COMMIT markers
  - What NOT to do
- Output as downloadable .md
- Operator downloads, runs in Claude Code in target repo

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
2. Verify `_in_progress/{slug}/stage2-response.md` exists and contains
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
15. Compute SHA-256 of all files (11 for self-applied; 12 for cross-repo including 02b), populate `01_manifest.json` (last)
16. Move `_in_progress/{slug}/` to `docs/handoffs/archive/{slug}/`:
    - `archive/{slug}/stage1-question.md`
    - `archive/{slug}/stage2-response.md`
17. Update JOURNAL + CHANGELOG + BACKLOG
18. Run `python scripts/validate_scope_tags.py` and `pre-commit run --all-files`
19. Single commit on dedicated branch

---

## Content invariants (never violate)

- `02_VISION.md`: FULL copy of target repo's VISION.md — NEVER .dev-knowledge's VISION unless target IS .dev-knowledge
- `02b_ECOSYSTEM_VISION.md` (conditional): FULL copy of `.dev-knowledge/VISION.md` when target ≠ `.dev-knowledge`; omit entirely when target = `.dev-knowledge`
- `03_PLAYBOOK.md`, `04_ESSENTIALS.md`: FULL copies, no editing
- `05_GOVERNANCE_ESSENCES.md`: essences ONLY — 2-4 sentences each, never full ADR text
- Target repo's own ADRs: NEVER included — Browser-2 reads them in the repo
- No subdirectories: all 11 (self-applied) or 12 (cross-repo) files at folder root, flat layout
- `01_manifest.json` generated last (after all other files) for accurate checksums
