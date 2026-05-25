# First Message — corp-monorepo (session-sync)

## Identification

You are receiving a structured handoff bundle for **corp-monorepo**, a multi-package Python CLI monorepo for knowledge extraction, vault management, and presales operations. This session-sync handoff transfers accumulated context from a prior browser chat so you can continue the work without context loss.

## Reading order

Read the uploaded files in this order before responding:

1. `02_VISION.md` — corp-monorepo mission and scope
2. `02b_ECOSYSTEM_VISION.md` — .dev-knowledge ecosystem context
3. `04_ESSENTIALS.md` — high-leverage working rules
4. `06_STATE_OF_PLAY.md` — current state, completed work, deferred items
5. `07_ACTION_PLAN.md` — next session goal, action plan, constraints
6. `08_TREE.txt` — repo file inventory
7. `05_GOVERNANCE_ESSENCES.md` — ADR rules relevant to this session's directives
8. `03_PLAYBOOK.md` — full methodology (reference as needed)
9. `01_MANIFEST.md` — metadata and drift verification

## State validation

Before proceeding, verify:

- The HEAD SHA in `01_MANIFEST.md` is `32a47f85b07d697be20066c1ec69df3cf92cb1f6`.
  When Claude Code opens in corp-monorepo, run `git rev-parse HEAD` and confirm it matches.
- `06_STATE_OF_PLAY.md` Stage 3 verification summary shows no VERIFICATION FAILED entries.
- `07_ACTION_PLAN.md` Hard Constraints are loaded and understood.

## Required first action — articulation gate

**Before writing any synthesis, before answering any questions, before generating any prompts:** write the following 4-item articulation. Write it now, as your first output.

1. **My role per `02_VISION.md`:** What is corp-monorepo, and what am I assisting with in this session?
2. **Current phase per BACKLOG:** What P1 items are open, and what pre-P1 audit must happen first?
3. **Immediate next action per directive #1 in `07_ACTION_PLAN.md`:** What exact verification steps does directive #1 require, and what files must be checked?
4. **Top 3 Hard Constraints per `07_ACTION_PLAN.md`:** List them verbatim.

After writing the 4 items, **stop and wait**. Do not proceed until the operator replies **"role confirmed"**.

If the operator corrects anything in the articulation, update your understanding and confirm the correction before proceeding.

## Receiver synthesis (MANDATORY)

After receiving "role confirmed", write a receiver synthesis using this exact template. Fill each bracket from the uploaded files — do not paraphrase from general knowledge.

---

**corp-monorepo** is [one sentence from `02_VISION.md` describing the repo's purpose].

Current state: [1-2 sentences from `06_STATE_OF_PLAY.md` — what was completed in the last session, what key finding the Stage 3 verification surfaced].

This session's focus: [1-2 sentences from `07_ACTION_PLAN.md` "Next session goal" — the goal and why directive #1 must come first].

My immediate next action: [directive #1 from `07_ACTION_PLAN.md` "Action plan", written as an imperative sentence].

---

After the synthesis, ask: "Does this synthesis look correct? Any corrections before we proceed to planning?"

## Operator response handling

- If operator says **"correct"** or similar: proceed to Q&A loop.
- If operator corrects something: update your synthesis, restate the corrected version, confirm before proceeding.
- If operator asks a question not in the bundle: say so explicitly; do not infer from general knowledge.

## Q&A iteration loop

Offer to answer questions about the action plan, constraints, or state before generating formal Claude Code prompt(s).

When operator is ready to proceed:

- Ask whether they want a **single prompt** (all directives in one Claude Code session) or **split prompts** (one per directive scope).
- Generate formal Claude Code prompt(s) per `03_PLAYBOOK.md` prompt format conventions:
  - Model/Mode/Effort table at top
  - Title, Repo, Purpose
  - Read-first list (must include: `CLAUDE.md`, `ARCHITECTURE.md`, `JOURNAL.md` last 5 entries, `BACKLOG.md`, and any ADR files directly cited in the directive)
  - Git workflow
  - UNDERSTAND section
  - Numbered steps with COMMIT markers
  - What NOT to do section (drawn from `07_ACTION_PLAN.md` Hard Constraints and Narrow scope rules)
- Output prompt(s) as downloadable `.md` file(s).
- Operator downloads and runs in Claude Code in `corp-monorepo`.

## Continuous improvement reminder

After execution, encourage the operator to fill in `09_EXECUTION_EVIDENCE.md` with the actual commands run, test results, git diffs, and final HEAD SHA. This becomes the input for the next session handoff.
