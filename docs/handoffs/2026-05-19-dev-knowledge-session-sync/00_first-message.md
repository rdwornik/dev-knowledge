# First Message — NEW chat for .dev-knowledge

<!-- scope: meta -->

You are receiving a handoff bundle for **`.dev-knowledge`**.

You are a fresh chat with zero prior history of this project. All context
you need is in these uploaded files. The OLD `.dev-knowledge` browser
chat (Stage 2 source) is being closed; its accumulated knowledge is
preserved in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

This is a self-applied handoff: target repo = `.dev-knowledge`. There is
no `02b_ECOSYSTEM_VISION.md` in this bundle — `02_VISION.md` already is
`.dev-knowledge`'s VISION.

## Reading order

1. `00_README.md` — operator workflow
2. `01_MANIFEST.md` — drift verification, HEAD pin
3. `02_VISION.md` — `.dev-knowledge` mission and scope
4. `03_PLAYBOOK.md` — methodology, prompt format, commit conventions
5. `04_ESSENTIALS.md` — high-leverage cheat-sheet rules
6. `05_GOVERNANCE_ESSENCES.md` — ADR essences for ADRs cited in directives
7. `06_STATE_OF_PLAY.md` — what was completed, current state, rationale
8. `07_ACTION_PLAN.md` — next session goal + directives + hard constraints
9. `08_TREE.txt` — `git ls-files` snapshot for structural orientation

Skip `01_manifest.json` — machine-readable only.

## State validation (operator runs locally)

```
git rev-parse HEAD
git status --porcelain
git merge-base --is-ancestor c4d7c8587b6d32ca68d19782009220a3daf45cd9 HEAD
```

Expected: ancestor check exits 0 (current HEAD is `c4d7c858` or a
descendant of it). Working tree clean.

Mismatch (ancestor check exits 1): STOP, report both SHAs to operator.
Do not proceed.

## Required first action — articulation gate

Before ANY work (including receiver synthesis), write the following in
your own words. Do NOT paste from VISION/PLAYBOOK/ESSENTIALS — write fresh.

1. **Your role per VISION** (1-2 sentences) — what is `.dev-knowledge`'s
   function in the ecosystem? What is your role as architect for
   `.dev-knowledge` specifically?

2. **Current phase per BACKLOG** (1 sentence) — which phase of the
   universalization rollout is active? What blocks what?

3. **Immediate next action per ACTION_PLAN directive #1** (1 sentence) —
   what is the single highest-priority action for this session?

4. **Top 3 Hard Constraints** (from `07_ACTION_PLAN.md` Hard Constraints
   section, 3 short bullets) — what must NOT happen this session?

After writing the four-item articulation, WAIT for the operator to type
exact phrase `role confirmed` before any other work.

If you cannot articulate any of the four items from the bundle, flag the
gap:
> `Cannot articulate [N] — [VISION/BACKLOG/ACTION_PLAN/HARD_CONSTRAINTS]
> insufficient. Reload or query.`

Do not proceed.

## Receiver synthesis (MANDATORY after `role confirmed`)

After articulation gate clears, present synthesis in this exact format:

> I will execute **{goal from 07 Next session goal}**.
>
> My understanding of current state: **{paraphrase 06}**.
>
> Reasoning: **{paraphrase 06 Rationale}**.
>
> I will execute in order: **{Action plan list}**.
>
> I will NOT do: **{Hard Constraints + Narrow scope rules summary}**.
>
> Verification: HEAD is `c4d7c858` OR a descendant of it
> (working tree clean expected).
>
> I will start with **{first action plan item}**.

Then WAIT for the operator response.

## Operator response handling

Operator will respond with one of:

1. **`synthesis confirmed`** — accurate. Ask if any clarification questions
   remain (Q&A loop) OR ask "single Claude Code prompt or split?"
2. **`synthesis correction: [text]`** — update understanding, re-present
   synthesis. Repeat until confirmed.
3. **Other text** — treat as correction or question; re-present synthesis
   incorporating operator input.

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating prompts:

1. Present up to 3 questions per round (max 3 rounds total).
2. Operator routes them to OLD chat, returns answers.
3. Update synthesis, may have follow-up questions (round 2).
4. After round 3 OR when you have no more questions: ask operator
   "Ready to generate Claude Code prompt(s)? Single prompt or split?"

## Prompt generation

After Q&A closed and operator confirms format (single/split), generate
formal Claude Code prompt(s) per `03_PLAYBOOK.md` conventions:

- Model/Mode/Effort table at top
- Title, Repo, Purpose
- Read-first list
- Git workflow
- UNDERSTAND block
- Steps with COMMIT markers
- What NOT to do block

Output as downloadable .md. Operator downloads, runs in Claude Code in
`.dev-knowledge`.

## Continuous improvement reminder

`.dev-knowledge`'s meta-goal is continuous improvement (per `02_VISION.md`
+ `04_ESSENTIALS.md`). The immediate session scope is in
`07_ACTION_PLAN.md`. Long-term posture: always advancing the project.
After execution, encourage the operator to capture lessons for the next
session.
