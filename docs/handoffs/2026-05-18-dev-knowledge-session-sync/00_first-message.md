# First Message — .dev-knowledge Handoff (session-sync 2026-05-18)

You are receiving a handoff bundle for **`.dev-knowledge`**.

You are a fresh chat with zero prior history of this project. All context you
need is contained in the uploaded files. The OLD browser chat that accumulated
this knowledge has been wrapped up — its judgment is captured in
`06_STATE_OF_PLAY.md` and `07_ACTION_PLAN.md`. You do not need to reach it.

---

## Reading order

Read the uploaded files in this order before doing anything else:

1. `01_MANIFEST.md` — metadata, file index, drift verification
2. `02_VISION.md` — `.dev-knowledge` mission and scope
3. `03_PLAYBOOK.md` — full methodology reference (how we work)
4. `04_ESSENTIALS.md` — high-leverage daily cheat sheet
5. `05_GOVERNANCE_ESSENCES.md` — ADR operational rules for this session
6. `06_STATE_OF_PLAY.md` — current project state
7. `07_ACTION_PLAN.md` — next session goal and action plan
8. `08_TREE.txt` — file inventory snapshot
9. `09_EXECUTION_EVIDENCE.md` — return-trip evidence form (initially empty)

Skip `01_manifest.json` — it is machine-readable only.

---

## State validation

The operator should run the following commands in the `.dev-knowledge` repo
before beginning work, to verify no drift has occurred since this bundle was
generated:

```powershell
git rev-parse HEAD
git status
```

**Expected HEAD SHA (Stage 1):** `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10`

The current HEAD must be **equal to or a descendant of** the expected SHA. Run:

```powershell
git merge-base --is-ancestor aeaf1582d68c8e2ae4ff304bf08972f6e01eec10 HEAD
echo $LASTEXITCODE  # 0 = OK; non-zero = drift
```

**If exit code is non-zero:** STOP. Report both the expected SHA and the
current HEAD SHA to the operator before proceeding. Do not silently continue.

**Expected working tree state:** clean.

---

## Required first action — articulation gate

Before ANY other work (including receiver synthesis), write the following four
items **in your own words**. Do NOT copy-paste from the bundle files — write
fresh, proving you have read and internalized the content.

1. **Your role per VISION** (1–2 sentences): What is `.dev-knowledge`'s
   function in the ecosystem? What is your role as architect for `.dev-knowledge`
   specifically?

2. **Current phase per BACKLOG** (1 sentence): Which stream or phase of work
   is active right now? What does the BACKLOG tell you about sequencing?

3. **Immediate next action per ACTION_PLAN directive #1** (1 sentence): What
   is the single highest-priority action for this session?

4. **Top 3 Hard Constraints** (3 short bullets, from `07_ACTION_PLAN.md`
   Hard Constraints section): What must NOT happen this session?

After writing the four-item articulation, **wait** for the operator to type
the exact phrase **`role confirmed`** before any other work.

If you cannot articulate any of the four items from the bundle content, flag
the gap:

> `Cannot articulate [N] — [VISION / BACKLOG / ACTION_PLAN / HARD_CONSTRAINTS]
>  insufficient. Reload or query.`

Do not proceed until the operator types `role confirmed`.

---

## Receiver synthesis

After the operator types `role confirmed`, present a receiver synthesis in
this exact format:

> "I will execute **{goal from 07 OBJECTIVE}**.
>
> My understanding of current state: **{paraphrase 06}**.
>
> Reasoning: **{paraphrase 07 RATIONALE section}**.
>
> I will execute in order: **{DIRECTIVES list from 07}**.
>
> I will NOT do: **{BOUNDARIES list from 07}**.
>
> Verification: HEAD is `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10` OR a
> descendant of it (working tree clean).
>
> I will start with **{first DIRECTIVE}**."

After presenting synthesis, **wait** for operator response.

---

## Operator response handling

The operator will respond with one of:

1. **`synthesis confirmed`** — synthesis is accurate. Proceed: ask if any
   clarification questions remain (Q&A loop) OR ask "single Claude Code prompt
   or split?"

2. **`synthesis correction: [text]`** — synthesis has errors. Update your
   understanding, re-present synthesis. Repeat until the operator confirms.

3. **Other text** — treat as a correction or question. Incorporate it and
   re-present synthesis.

---

## Q&A iteration loop (if needed)

If you have clarification questions BEFORE generating prompts:

1. After synthesis confirmed, present:
   > "I have {N} clarification questions before generating prompts:
   > 1. {question 1}
   > 2. {question 2}
   > 3. {question 3} (max 3 per round)
   >
   > Please route these to OLD chat and return answers."

2. Operator routes questions to OLD chat, returns answers.
3. Update synthesis; you may ask follow-up questions (round 2).
4. Maximum 3 rounds. After round 3, proceed with best available understanding
   OR ask operator to restart Stage 2.

When you have no more questions, ask: "Ready to generate Claude Code prompt(s)?
Single prompt or split?"

---

## Prompt generation

After the Q&A loop closes and the operator confirms format:

- Generate formal Claude Code prompt(s) per `03_PLAYBOOK.md` conventions:
  - Model / Mode / Effort table at top
  - Title, Repo, Purpose
  - Read-first list
  - Git workflow
  - UNDERSTAND block
  - Numbered steps with COMMIT markers
  - What NOT to do section
- Output as downloadable `.md` file(s).
- Operator downloads and pastes into Claude Code in `.dev-knowledge`.

---

## Continuous improvement

This project's meta-goal is continuous improvement (per `.dev-knowledge`
VISION + ESSENTIALS). The immediate session scope is in `07_ACTION_PLAN.md`.
After execution, capture lessons: any unexpected pattern or decision that
should survive into the next session belongs in LESSONS.md (append-only).
