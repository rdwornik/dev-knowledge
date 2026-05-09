# First Message — ai-council audit-sync handoff

Paste this verbatim as your first message in the new browser-2 chat.

---

I am resuming work on the **ai-council** repository. I have uploaded a
`.dev-knowledge` handoff bundle (v3.0 format, ADR-42) for this session.

## Step 1: Verify HEAD SHA (MANDATORY before anything else)

Run in ai-council repo:
```
git rev-parse HEAD
```

Expected: `c821157fcfa957bc6612c74667d70c8c9a88ef5c`

**If the SHA does not match: STOP. Report the actual SHA and do not proceed
until Rob resolves the drift.**

Note: The audit found `config/settings.yaml` modified in the working tree.
This is a known drift point — do NOT include these changes in commits for
F-01 or F-02 work. Work only on new files (VISION.md) and CLAUDE.md.

## Step 2: Reading order

Read the uploaded files in this order:
1. `01_MANIFEST.md` — entry point, metadata, navigation
2. `02_VISION.md` — ecosystem context (why .dev-knowledge exists)
3. `03_PLAYBOOK.md` — HOW we work (methodology)
4. `04_ESSENTIALS.md` — daily cheat sheet rules
5. `05_GOVERNANCE_ESSENCES.md` — ADR-33 and ADR-35 essences (drive your actions)
6. `06_STATE_OF_PLAY.md` — current state: audit findings, what's locked, what's deferred
7. `07_ACTION_PLAN.md` — your goals, directives, and boundaries

Read `08_TREE.txt` if you need structural orientation. Read `09_EXECUTION_EVIDENCE.md`
only at end of session to fill it out.

## Step 3: Receiver synthesis (MANDATORY before acting)

After reading all files above, provide this synthesis before doing anything:

> "I will execute [goal from 07_ACTION_PLAN.md]. My understanding:
> [paraphrase of audit findings + locked decisions]. I will NOT [out-of-scope items].
> I will start with [first directive from 07_ACTION_PLAN.md].
> HEAD SHA matches c821157fcfa957bc6612c74667d70c8c9a88ef5c.
> Working tree has config/settings.yaml modified — I will not touch this file."

**Only proceed after Rob confirms the synthesis is accurate.**
