# First Message — ai-council Handoff (audit-sync, 2026-05-09)

You are receiving a handoff bundle for **ai-council**. You are a fresh chat with
zero prior history of this project. All context you need is in these uploaded files.

The previous ai-council chat (where work was discussed and decisions were made) is
now closed. Its accumulated knowledge has been captured in `06_STATE_OF_PLAY.md`
and `07_ACTION_PLAN.md` in this bundle.

## Reading order

Before acting on any directives, read in this order:

1. `00_README.md` — what this bundle is (you're reading the first message, not this file)
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
> I chose this approach because: **{paraphrase 07_ACTION_PLAN RATIONALE
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

**Wait for Rob's confirmation that the synthesis is accurate before proceeding.**
If Rob corrects any element of the synthesis, update understanding and re-confirm.
