# 00_first-message.md — Paste This as First Message

*Paste everything below this line as the first message in the NEW (fresh) chat.*

---

You are receiving a handoff bundle for **.dev-knowledge**.

You are a **fresh chat with zero prior history** of this project. All context
you need is in the uploaded files. The OLD chat that accumulated this session's
knowledge has been wrapped up; its knowledge lives in `06_STATE_OF_PLAY.md`
and `07_ACTION_PLAN.md`.

---

## Reading order

Read files in this order before responding:

1. `01_MANIFEST.md` — metadata, file index, state validation
2. `02_VISION.md` — ecosystem context and mission
3. `04_ESSENTIALS.md` — high-leverage rules and operating posture
4. `07_ACTION_PLAN.md` — goal, directives, boundaries (operational center)
5. `06_STATE_OF_PLAY.md` — current state, decisions locked, verification
6. `05_GOVERNANCE_ESSENCES.md` — ADR rules driving specific actions
7. `03_PLAYBOOK.md` — full methodology reference (skim unless needed)

Skip `01_manifest.json` (machine-readable checksums, not for reading).
Skip `08_TREE.txt` unless you need to verify file existence.

---

## State validation

You cannot run shell commands. Ask the operator to run these and report results:

```
git rev-parse HEAD
git status --porcelain
git branch --show-current
```

Expected HEAD: `5f09fe19e87164aec1472afa3da65bc594dab8ab` (or Stage 3 commit
descendant — one additional commit for the Stage 3 folder generation itself).

**If HEAD differs significantly from expected:** STOP. Report the mismatch
to the operator before proceeding. Do not assume the difference is harmless.

---

## Receiver synthesis (MANDATORY before action)

After reading the full bundle, present your synthesis in this exact format:

> "I will execute **{goal from 07 OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06 Current State}**.
>
> My reasoning: **{paraphrase 07 RATIONALE section in architect's terms}**.
>
> I will execute in order: **{numbered DIRECTIVES from 07}**.
>
> I will NOT do: **{key BOUNDARIES from 07}**.
>
> Verification: HEAD matches `5f09fe1...` (or descendant), working tree {state}.
>
> I will start with **{first DIRECTIVE}**."

**Wait for operator confirmation before proceeding.** Do not begin executing
directives until operator responds.

---

## Operator response handling

Operator will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. Ask if you have any
   clarification questions (Q&A loop), or ask: "Ready to generate Claude Code
   prompt(s)? Single prompt or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. Update your
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
   (max 3 per round)
   Please route these to the OLD chat and return answers."

2. Operator routes to OLD chat, gets answers, returns them.
3. Update synthesis with answers; may have follow-up (round 2).
4. Maximum 3 rounds. After round 3: proceed with best available understanding
   OR ask operator to restart Stage 2.

When no more questions: "Ready to generate Claude Code prompt(s)? Single or split?"

---

## Prompt generation

After Q&A loop closed and operator confirms format (single/split):

- Generate Claude Code prompt(s) per `03_PLAYBOOK.md` conventions:
  - Model/Mode/Effort table at top
  - Title, Repo, Purpose sections
  - Read first list
  - Git workflow
  - UNDERSTAND
  - Steps with COMMIT markers
  - What NOT to do section
- Output as downloadable `.md` file(s)
- Operator downloads, runs in Claude Code in `.dev-knowledge` (NOT in another repo)

---

## Press-back partner posture

This session's goal is refinement, not execution. For each BACKLOG strategic
item in the directives:

- **Press back on vague scope** — if an item is fuzzy, say so explicitly and
  propose a sharper definition before adding it to a session plan
- **Propose concrete first steps** — smallest reversible action
- **Surface dependencies** — flag when item B cannot start without item A
- **Classify debate vs conversational** — scope/architecture = Council debate;
  clarifications = conversational
- **Flag hidden compound items** — one BACKLOG entry that's really three
- **Propose scope boundaries** — explicit IN and OUT for next session attempt

This posture is not optional — the `07_ACTION_PLAN.md` explicitly mandates it.
Reference: Browser-3 catching the DoD "4 vs 5 sections" error is the precedent.

---

## Continuous improvement reminder

`.dev-knowledge`'s meta-goal is continuous improvement (per `02_VISION.md` and
`04_ESSENTIALS.md` Continuous Improvement section). The immediate session scope
is in `07_ACTION_PLAN.md`. Long-term posture: always advancing the framework.

After executing directives, encourage capturing lessons — what was surprising,
what patterns emerged, what should be different next time. These go into
`LESSONS.md` (append-only, oldest-first per ADR-29).

---

*Begin by reading all files in the order above, then present your receiver synthesis.*
