# First Message — ai-council Handoff (session-sync, 2026-05-14)

<!-- scope: meta -->

---

You are receiving a handoff bundle for **ai-council**.

You are a **fresh chat with zero prior history of this project.** All context
you need is in the uploaded files. The OLD browser chat for ai-council has been
closed; its knowledge is preserved in `06_STATE_OF_PLAY.md` (current state) and
`07_ACTION_PLAN.md` (next session directives).

---

## Reading order

Read in this order:

1. `01_MANIFEST.md` — entry point, metadata, HEAD pin
2. `02_VISION.md` — ecosystem context (why .dev-knowledge exists)
3. `03_PLAYBOOK.md` — how we work (methodology, prompt format, commit conventions)
4. `04_ESSENTIALS.md` — high-leverage rules cheat sheet
5. `05_GOVERNANCE_ESSENCES.md` — ADR rules driving specific actions
6. `06_STATE_OF_PLAY.md` — what was done; current state; architect judgment
7. `07_ACTION_PLAN.md` — next session goal, directives, boundaries
8. `08_TREE.txt` — repo file inventory for structural orientation

Skip `01_manifest.json` (machine-readable, not for reading) and `09_EXECUTION_EVIDENCE.md` (you fill that after work).

---

## State validation

You cannot run shell commands. Ask the operator to run these in the **ai-council** repo before any work begins:

```
git rev-parse HEAD
git status --porcelain
```

**Expected:** HEAD = `0f069554b894802504aa4e5ce140b1d481ae9ec8`, working tree clean.

If HEAD does not match: **STOP** and report drift to operator. Do not proceed until operator confirms the discrepancy is expected.

---

## Required first action — articulation gate

**Before any other work** (including receiver synthesis), write in your own
words — do NOT copy-paste from the uploaded files. Write fresh:

1. **Your role per VISION** (1-2 sentences) — what is `.dev-knowledge`'s
   function in the ecosystem? What is your role as architect for **ai-council** specifically?

2. **Current phase per BACKLOG** (1 sentence) — which phase of the
   universalization rollout is active for ai-council? What blocks what?

3. **Immediate next action per ACTION_PLAN directive #1** (1 sentence) —
   what is the single highest-priority action for this session?

4. **Top 3 Hard Constraints per BOUNDARIES** (3 short bullets) — what
   must NOT happen this session?

After writing the four-item articulation, **wait for operator to type exact
phrase `role confirmed`** before any other work.

If you cannot articulate any of the four items from the bundle, flag the gap:

> `Cannot articulate [N] — [VISION/BACKLOG/ACTION_PLAN/BOUNDARIES] insufficient. Reload or query.`

Do not proceed until operator responds.

---

## Receiver synthesis (after `role confirmed`)

After operator confirms your articulation, present synthesis in this format:

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
> Verification: HEAD matches `0f069554b894802504aa4e5ce140b1d481ae9ec8`, working tree clean.
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, **wait for operator response.**

---

## Operator response handling

Operator will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. Proceed: ask if any
   clarification questions remain (Q&A loop) OR ask "single Claude Code
   prompt or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. Update
   understanding, re-present synthesis. Repeat until operator confirms.

3. **Other text** — treat as correction or question. Re-present synthesis
   incorporating operator's input.

---

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating prompts:

1. After synthesis confirmed, present:
   "I have {N} clarification questions before generating prompts:
   1. {question 1}
   2. {question 2}
   3. {question 3} (max 3 per round)
   Please route these to OLD chat and return answers."

2. Operator takes questions to OLD chat, gets answers, returns them.
3. Update synthesis with answers. May have follow-up questions (round 2).
4. Maximum 3 rounds. After round 3, proceed with best available understanding
   OR ask operator to restart Stage 2.

When you have no more questions, ask operator: "Ready to generate Claude Code
prompt(s)? Single prompt or split?"

---

## Prompt generation

After Q&A loop closed and operator confirms format (single/split):

Generate formal Claude Code prompt(s) per `03_PLAYBOOK` conventions:
- Model/Mode/Effort table at top
- Title, Repo, Purpose
- Read first list
- Git workflow
- UNDERSTAND section
- Steps with COMMIT markers
- What NOT to do section

Output as downloadable `.md`. Operator downloads and runs in Claude Code in
the ai-council repo.

---

## Continuous improvement reminder

The project's meta-goal is continuous improvement per `.dev-knowledge` VISION
and ESSENTIALS. The immediate session scope is in `07_ACTION_PLAN.md`. Long-term
posture: always advancing the project. After execution, encourage operator to
capture lessons learned for the next session.
