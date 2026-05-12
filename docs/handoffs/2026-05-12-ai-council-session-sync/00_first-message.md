# First Message — 2026-05-12-ai-council-session-sync

*Copy-paste this entire file as the first message in the NEW claude.ai chat.*

---

You are receiving a handoff bundle for **ai-council**.

You are a **fresh chat with zero prior history** of this project. All context you need
is in these uploaded files. The OLD browser chat for ai-council is being closed; its
accumulated knowledge is preserved in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

---

## Reading order

Read these files in order before responding:

1. `01_MANIFEST.md` — entry point and HEAD verification
2. `04_ESSENTIALS.md` — how Claude thinks + daily operating rules
3. `02_VISION.md` — ecosystem context and methodology mission
4. `06_STATE_OF_PLAY.md` — what was done this session, rationale, deferred items
5. `07_ACTION_PLAN.md` — goals, directives, boundaries (OPERATIONAL CENTER)
6. `05_GOVERNANCE_ESSENCES.md` — ADR rules driving specific actions
7. `08_TREE.txt` — repo file inventory for structural orientation
8. `03_PLAYBOOK.md` — full methodology reference (use as reference, not required reading)
9. Skip `01_manifest.json` (machine-readable checksums only)

---

## State validation

Before acting on any directive, ask operator to run these in ai-council repo:

```
git rev-parse HEAD
git status --porcelain
```

Expected HEAD: `f094d0821a279f3aa36de554943c1b44576d0924`
Expected working tree: clean (no output)

If HEAD mismatch: **STOP**. Report both SHAs to operator. Do not proceed until drift
is explained.

---

## Receiver synthesis (MANDATORY before any action)

After reading the full bundle, present your synthesis in this format:

> "I will execute **{goal from 07 OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06 — what was shipped, what's pending}**.
>
> Key rationale I'm carrying forward: **{most important decision context from 06 RATIONALE — especially the cost-optimization principle}**.
>
> I will execute in order: **{numbered DIRECTIVES from 07}**.
>
> I will NOT do: **{key BOUNDARIES from 07}**.
>
> Verification: HEAD `f094d0821a279f3aa36de554943c1b44576d0924`, working tree clean.
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, **wait for operator response before doing anything**.

---

## Operator response handling

Operator will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. Ask if you have clarification
   questions (Q&A loop) OR ask "single Claude Code prompt or split?"

2. **`synthesis correction: [text]`** — update understanding, re-present synthesis.
   Repeat until operator confirms.

3. **Other text** — treat as correction or question. Incorporate and re-present.

---

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating prompts:

1. After synthesis confirmed, present:
   "I have {N} clarification questions before generating prompts:
   1. {question}
   2. {question}
   (max 3 per round)
   Please route these to the OLD chat and return answers."

2. Operator takes questions to OLD chat, returns answers
3. Update synthesis with answers; may have follow-up questions (round 2)
4. Maximum 3 rounds. After round 3, proceed with best available understanding OR ask
   operator to restart Stage 2

When no more questions: "Ready to generate Claude Code prompt(s)? Single prompt or split?"

---

## Prompt generation

After Q&A closed and operator confirms format:

- Generate formal Claude Code prompt(s) per `03_PLAYBOOK.md` "Writing prompts for
  Claude Code" section (Model/Mode/Effort table + standard 8-section structure)
- Output as downloadable `.md` artifacts
- Operator downloads, runs in Claude Code in ai-council repo

---

## Continuous improvement reminder

ai-council's meta-goal is continuous development and refinement (per `02_VISION.md`
and `04_ESSENTIALS.md` Continuous Improvement section). The immediate scope is in
`07_ACTION_PLAN.md`. After execution, encourage operator to capture any new lessons
for the next session.
