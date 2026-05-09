# First Message — ai-council Handoff (audit-sync, 2026-05-09)

You are receiving a handoff bundle for **ai-council**. You are a fresh chat with
zero prior history of this project. All context you need is in these uploaded files.

The previous ai-council chat (where work was discussed and decisions were made) is
now closed. Its accumulated knowledge has been captured in `06_STATE_OF_PLAY.md`
and `07_ACTION_PLAN.md` in this bundle.

## Reading order

Before acting on any directives, read in this order:

1. `00_README.md` — what this bundle is and operator workflow (you're reading the
   first message, not this file)
2. `01_MANIFEST.md` — metadata, HEAD verification, file index
3. `02_VISION.md` — ecosystem context (why .dev-knowledge exists, scope, methodology)
4. `03_PLAYBOOK.md` — HOW we work (methodology, prompt format, commit conventions)
5. `04_ESSENTIALS.md` — high-leverage rules (cheat sheet for daily work)
6. `05_GOVERNANCE_ESSENCES.md` — ADR-33 + ADR-35 operational rules relevant to directives
7. `06_STATE_OF_PLAY.md` — current state (audit findings, architect knowledge, verification)
8. `07_ACTION_PLAN.md` — what to do (goal, directives, boundaries, success criteria)
9. `08_TREE.txt` — ai-council file inventory (repo structure orientation)
10. `09_EXECUTION_EVIDENCE.md` — you will fill this after completing directives

**Note on `01_manifest.json`:** machine-readable metadata with SHA-256 checksums
for all files. Skip during sequential reading — reference only if you need
programmatic file integrity verification or exact checksums. `01_MANIFEST.md`
(Markdown counterpart) contains the same metadata in human-readable form.

## State validation (do this first)

Before doing anything else:

```bash
cd C:/Users/1028120/Documents/Dev/ai-council
git rev-parse HEAD
git status --porcelain
```

**Expected HEAD:** `c821157fcfa957bc6612c74667d70c8c9a88ef5c`

If HEAD does not match: STOP. Report the mismatch and current HEAD to Rob.
Do not proceed until Rob confirms whether to continue with drifted state.

**Expected working tree:** `M config/settings.yaml` (one modified file — intentional)

## Receiver synthesis (MANDATORY before acting on any directive)

After reading the full bundle, provide this synthesis before acting:

> "I will execute **{goal from 07_ACTION_PLAN OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06_STATE_OF_PLAY
> — migration status, audit findings, what architect witnessed}**.
>
> Reasoning: **{paraphrase 07_ACTION_PLAN RATIONALE
> — tier M reasoning, lessons discovery criterion}**.
>
> I will execute in order: **{numbered DIRECTIVES list from 07_ACTION_PLAN}**.
>
> I will NOT: **{BOUNDARIES list from 07_ACTION_PLAN}**.
>
> Verification: HEAD matches `c821157fcfa957bc6612c74667d70c8c9a88ef5c`,
> working tree has `M config/settings.yaml`.
>
> I will start with **{first directive from 07_ACTION_PLAN}**."

**After presenting synthesis, wait for Rob's response.**

## Operator response handling

Rob will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. Ask if you have any
   clarification questions (Q&A loop below) OR ask Rob: "Ready to generate
   the Claude Code prompt. Single prompt or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. Update your
   understanding based on the correction, re-present the synthesis. Repeat
   until Rob confirms.

3. **Other text** — treat as correction or question. Re-present synthesis
   incorporating Rob's input.

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating the Claude Code prompt:

After synthesis confirmed, present your questions as:

> "I have {N} clarification questions before generating the prompt:
> 1. {question 1}
> 2. {question 2}
> 3. {question 3}
> (max 3 per round)
> Please route these to the OLD ai-council chat and return answers."

Rob will take your questions to the OLD ai-council chat, get answers, and
return them. You may have follow-up questions (round 2). Maximum 3 rounds.
After round 3, proceed with best available understanding OR ask Rob to
restart Stage 2.

When you have no more questions, ask: "Ready to generate the Claude Code
prompt. Single prompt or split?"

## Prompt generation

After Q&A loop closed and Rob confirms format (single/split):

Generate a formal Claude Code prompt per `03_PLAYBOOK.md` conventions:
- Model/Mode/Effort table at top
- Title, Repo, Purpose
- Read first list
- Git workflow
- UNDERSTAND section
- Numbered steps with COMMIT markers
- What NOT to do section

Output the prompt as a downloadable .md file. Rob will download it and
run it in Claude Code in the ai-council repo.

## Continuous improvement reminder

This project's meta-goal (per `.dev-knowledge` VISION + ESSENTIALS) is
continuous improvement. The immediate session scope is in `07_ACTION_PLAN.md`
(F-01 + F-02). Long-term posture: always advancing ai-council. After
execution, encourage Rob to capture lessons for the next session.
