# First Message — dev-knowledge Handoff (2026-05-12 session-sync)

<!-- scope: meta -->

You are receiving a handoff bundle for **`.dev-knowledge`**.

You are a **fresh chat with zero prior history** of this project. All context you
need is in the uploaded files. The OLD chat (Stage 2 source) is closed — its
accumulated knowledge is captured in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

---

## Reading order

Read these files in this order before doing anything else:

1. `01_MANIFEST.md` — overview, HEAD pin, file index
2. `02_VISION.md` — ecosystem context and mission
3. `04_ESSENTIALS.md` — daily operating rules (cheat sheet)
4. `03_PLAYBOOK.md` — full methodology reference (skim sections, read deeply what's relevant)
5. `05_GOVERNANCE_ESSENCES.md` — ADR operational rules for this session's actions
6. `06_STATE_OF_PLAY.md` — current state, what was done, decisions made
7. `07_ACTION_PLAN.md` — goals, directives, boundaries for next session
8. `08_TREE.txt` — target repo file inventory for structural orientation
9. Skip `01_manifest.json` — machine-readable only
10. `09_EXECUTION_EVIDENCE.md` — empty template, you will fill this after work

---

## State validation

These checks require Claude Code (not browser chat). Ask operator to run in
`.dev-knowledge` before proceeding:

```
git rev-parse HEAD    # expected: 0125f1b0065bea3de34d1a93e5034fac9201881f
git branch --show-current    # expected: main
git status --porcelain
```

**If HEAD SHA does not match** → STOP, report drift to operator before proceeding.
**Working tree note:** One unstaged deletion (`docs/handoffs/2026-05-12-session-handoff/2026-05-12-session-handoff.md`) is expected — pre-existing state, Directive 2 resolves it.

---

## Receiver synthesis (MANDATORY before any action)

After reading the full bundle, you MUST present a synthesis in this exact format:

> "I will execute **{goal from 07_ACTION_PLAN OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06_STATE_OF_PLAY}**.
>
> Reasoning: **{paraphrase 07_ACTION_PLAN RATIONALE}**.
>
> I will execute in order: **{DIRECTIVES list from 07_ACTION_PLAN}**.
>
> I will NOT do: **{BOUNDARIES list from 07_ACTION_PLAN}**.
>
> Verification: HEAD matches `0125f1b`, working tree has one known deletion.
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, **wait for operator response**.

---

## Operator response handling

1. **`synthesis confirmed`** — synthesis is accurate. Proceed: ask if you have
   clarification questions (Q&A loop), then ask "single Claude Code prompt or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. Update your
   understanding, re-present synthesis. Repeat until confirmed.

3. **Other text** — treat as correction or clarification. Re-present synthesis.

---

## Q&A iteration loop (if needed)

If you have clarification questions before generating prompts:

1. After synthesis confirmed, present:
   "I have {N} clarification question(s) before generating prompts:
   1. {question}
   ...
   (max 3 per round)
   Please route to OLD chat and return answers."

2. Operator takes questions to OLD chat, returns answers
3. Update synthesis, may have follow-up questions (round 2)
4. Maximum 3 rounds. After round 3, proceed with best available understanding.

When no more questions: "Ready to generate Claude Code prompt(s). Single prompt or split?"

---

## Prompt generation

After Q&A closed and operator confirms format (single/split), generate formal Claude
Code prompt(s) per `03_PLAYBOOK.md` conventions:

- Model/Mode/Effort table at top
- Title, Repo, Purpose
- Read first list (CLAUDE.md + gotchas + relevant files)
- Git workflow
- UNDERSTAND section
- Steps with COMMIT markers
- What NOT to do section

Output as downloadable `.md` files. Operator downloads, runs in Claude Code in
`.dev-knowledge`.

---

## Continuous improvement reminder

`.dev-knowledge`'s meta-goal is **continuous improvement** (per `02_VISION.md` and
`04_ESSENTIALS.md`). The immediate session scope is in `07_ACTION_PLAN.md`. Long-term
posture: always advancing the framework. After execution, capture lessons for the next
session in `LESSONS.md`.
