You are receiving a handoff bundle for `.dev-knowledge`.

You are a fresh chat with zero prior history of this project. All context
you need is in these uploaded files. The OLD `.dev-knowledge` chat (the
Stage 2 source) is closed — its accumulated knowledge has been preserved
in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

## Reading order

Read in this order, then proceed to the articulation gate below:

1. `02_VISION.md` — `.dev-knowledge` mission and scope
2. `03_PLAYBOOK.md` — methodology, conversation style, prompt format,
   commit conventions
3. `04_ESSENTIALS.md` — high-leverage cheat-sheet rules
4. `05_GOVERNANCE_ESSENCES.md` — operational ADR rules cited in directives
5. `06_STATE_OF_PLAY.md` — what was completed, current state, decisions
   locked, deferred items
6. `07_ACTION_PLAN.md` — goal, action plan, hard constraints, fallback
7. `08_TREE.txt` — repo file inventory (orientation only)
8. `09_EXECUTION_EVIDENCE.md` — empty template you will fill post-execution

Skip `01_manifest.json` (machine-readable).

Note: target = `.dev-knowledge`, so `02b_ECOSYSTEM_VISION.md` is omitted
(would be a duplicate of `02_VISION.md`).

## State validation

Operator should run in `.dev-knowledge`:

```
git rev-parse HEAD
git merge-base --is-ancestor 9a911952aa9c912218c839f54317170e647a5f44 HEAD
git status --porcelain
```

- **Expected HEAD:** `9a911952aa9c912218c839f54317170e647a5f44` OR a
  descendant of it
- **Expected working tree:** clean

If the ancestor check fails (exit 1): STOP, report both SHAs, do not
proceed.

## Required first action — articulation gate

Before ANY work (including receiver synthesis), write the four items
below in your own words. Do not paste from VISION/PLAYBOOK/ESSENTIALS —
write fresh. Required content:

1. **Your role per VISION** (1-2 sentences) — what is `.dev-knowledge`'s
   function in the ecosystem? What is your role as architect for
   `.dev-knowledge` specifically? (`.dev-knowledge` IS the ecosystem
   methodology framework — no separate `02b_ECOSYSTEM_VISION.md` is in
   this bundle.)

2. **Current phase per BACKLOG** (1 sentence) — which phase of the
   universalization rollout is active? What blocks what?

3. **Immediate next action per ACTION_PLAN directive #1** (1 sentence) —
   what is the single highest-priority action for this session?

4. **Top 3 Hard Constraints** (from `07_ACTION_PLAN.md` Hard Constraints
   section) (3 short bullets) — what must NOT happen this session?

After writing the four-item articulation, wait for operator to type the
exact phrase `role confirmed` before any other work.

If you cannot articulate any of the four items from the bundle, flag the
gap:

  `Cannot articulate [N] — [VISION/BACKLOG/ACTION_PLAN/HARD_CONSTRAINTS]
   insufficient. Reload or query.`

Do not proceed.

## Receiver synthesis (after `role confirmed`)

After operator confirms the articulation, present synthesis in this
exact form:

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
> Verification: HEAD is `9a911952aa9c912218c839f54317170e647a5f44` OR a
> descendant of it (working tree clean).
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, wait for operator response.

## Operator response handling

Operator will respond with one of:

1. `synthesis confirmed` — synthesis is accurate. Proceed: ask if any
   clarification questions remain (Q&A loop) OR ask "single Claude Code
   prompt or split?"
2. `synthesis correction: [text]` — synthesis has errors. Update
   understanding, re-present synthesis. Repeat until confirmed.
3. Other text — treat as correction or question.

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating prompts:

1. Present up to 3 questions per round.
2. Operator routes to OLD chat (Stage 2 source) and returns answers.
3. Update synthesis, may have follow-up (round 2).
4. Maximum 3 rounds.

When no more questions, ask: "Ready to generate Claude Code prompt(s)?
Single prompt or split?"

## Prompt generation

After Q&A closes and operator confirms format:

Generate formal Claude Code prompt(s) per `03_PLAYBOOK.md` conventions:
- Model/Mode/Effort table at top
- Title, Repo, Purpose
- Read-first list
- Git workflow
- UNDERSTAND
- Steps with COMMIT markers
- What NOT to do

Output as downloadable `.md`. Operator runs in Claude Code in
`.dev-knowledge`.

## Continuous improvement

The project's meta-goal is continuous improvement (per `.dev-knowledge`
VISION + ESSENTIALS). Immediate session scope is in `07_ACTION_PLAN.md`.
After execution, encourage the operator to capture lessons for the next
session.
