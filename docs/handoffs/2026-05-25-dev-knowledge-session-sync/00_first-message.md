# First message — paste this into the NEW chat

You are receiving a handoff bundle for **`.dev-knowledge`**. You are a fresh chat
with zero prior history of this project. All the context you need is in these
uploaded files. The OLD chat that produced this handoff is closed; its
accumulated knowledge is preserved in `06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`.

## Reading order

1. `01_MANIFEST.md` — what this bundle is, repo state, file index
2. `02_VISION.md` — `.dev-knowledge`'s mission and scope (this repo IS the
   ecosystem-methodology layer, so there is no separate `02b_ECOSYSTEM_VISION.md`)
3. `03_PLAYBOOK.md` — how we work (methodology, prompt format, conventions)
4. `04_ESSENTIALS.md` — high-leverage cheat-sheet rules
5. `05_GOVERNANCE_ESSENCES.md` — essences of the ADRs cited in the action plan
6. `06_STATE_OF_PLAY.md` — current state, decisions locked, open threads
7. `07_ACTION_PLAN.md` — goal, action plan, hard constraints, fallbacks
8. `08_TREE.txt` — repo file inventory
9. `09_EXECUTION_EVIDENCE.md` — you fill this out after the work
   (skip `01_manifest.json` — machine-readable checksums)

## State validation (operator runs these — a browser chat cannot)

```
git -C C:\Users\1028120\Documents\Dev\.dev-knowledge merge-base --is-ancestor 2b29329490acfa3484e1a9807845f31d3922ae9a HEAD
git -C C:\Users\1028120\Documents\Dev\.dev-knowledge status --porcelain
```

Expected: the pinned Stage 3 HEAD `2b29329490acfa3484e1a9807845f31d3922ae9a` is
the current HEAD **or an ancestor of it** (the ancestor check exits 0). If it
exits 1, **STOP** and report both SHAs — do not proceed.

## Required first action — articulation gate (before ANY work, including synthesis)

Write the following in your own words. Do NOT paste from VISION/PLAYBOOK/ESSENTIALS
— write fresh:

1. **Your role per VISION** (1-2 sentences) — what is `.dev-knowledge`'s function
   in the ecosystem, and what is your role as its architect this session?
2. **Current phase per BACKLOG/state** (1 sentence) — what is the active phase and
   what blocks what?
3. **Immediate next action per action plan directive #1** (1 sentence).
4. **Top 3 Hard Constraints** (3 short bullets from `07_ACTION_PLAN.md`).

If you cannot articulate any of the four from the bundle, flag the gap:
`Cannot articulate [N] — [VISION/BACKLOG/ACTION_PLAN/HARD_CONSTRAINTS] insufficient.
Reload or query.` and do not proceed.

After writing the four-item articulation, **wait for the operator to type
`role confirmed`** before any other work.

## Receiver synthesis (MANDATORY, after `role confirmed`)

> I will execute **obtaining an operator decision on handoff-bundle consolidation,
> paired with formalizing AI Council decision-return into the workflow** (pivoting
> to scrum-master-pattern codification if consolidation is shelved).
>
> My understanding of current state: **{paraphrase `06_STATE_OF_PLAY.md`}**.
>
> Reasoning: **{paraphrase the Decisions-locked / open-thread rationale in 06}**.
>
> I will execute in order: **{the `07_ACTION_PLAN.md` action list}**.
>
> I will NOT: **{the Hard Constraints + Narrow-scope rules from 07}**.
>
> Verification: HEAD is `2b29329490acfa3484e1a9807845f31d3922ae9a` or a descendant
> of it (working tree clean).
>
> I will start with **action 1 — the consolidation decision.**

After presenting synthesis, **wait** for the operator.

## Operator response handling

- **`synthesis confirmed`** → proceed: ask if any clarification questions remain
  (Q&A loop), else ask "single Claude Code prompt or split?"
- **`synthesis correction: [text]`** → update understanding, re-present synthesis.
- **Other text** → treat as correction/question; re-present synthesis.

## Q&A iteration loop (if you have questions before generating prompts)

Present up to 3 questions per round; the operator routes them to the OLD chat and
returns answers; max 3 rounds. When you have no more, ask: "single Claude Code
prompt or split?"

## Prompt generation

After the format is chosen, generate formal Claude Code prompt(s) per `03_PLAYBOOK`
conventions: Model/Mode/Effort table at top, Title/Repo/Purpose, Read-first list,
Git workflow, UNDERSTAND, Steps with COMMIT markers, What-NOT-to-do. Output as
downloadable `.md`. The operator runs them in Claude Code **in `.dev-knowledge`**.

Note on model selection (a Hard-Constraint-adjacent rule): name the model in each
prompt's Model/Mode/Effort table — Sonnet for mechanical/well-specified work, Opus
for audit/synthesis/architecture/judgment-heavy work. Do not default to Sonnet for
substantive prompts.

## Continuous improvement

This project's meta-goal is continuous improvement. The immediate scope is in
`07_ACTION_PLAN.md`; the long-term posture is always advancing the project. After
execution, capture lessons and fill `09_EXECUTION_EVIDENCE.md` for the next session.
