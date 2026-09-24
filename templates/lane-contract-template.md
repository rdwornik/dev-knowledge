---
reconciled_with: handoff-process@7.1.0
---
<!-- scope: meta -->
<!--
  templates/lane-contract-template.md — the shape of a LANE's frozen contract
  (`protocols/HANDOFF_PROCESS.md` §1): Model table · Read first · Dispatch · Owns · Value ·
  Done-contract · Do not. The architect writes one per lane; the lane executes it; nobody edits
  it after the freeze (a revision is a new file, the old one kept as `-v1-superseded`).

  DISTILLED (LANE-5A-9, 2026-09-24) from the wave-5A contracts (`LANE-5A-*.md`) and the handback
  rules of `WAVE4B-COMMON-2026-09-22`. `scripts/gen_lane_contract.py` emits a contract with
  the mechanical regions baked in.

  THE PARTS CODE READS — keep their spelling, or a reader goes blind without refusing:
  * `| Model | Mode | Effort |` table and the `## Dispatch` fence — `scripts/dispatch.py launch`
    reads both for their FIELDS and does not run the line; the two agree or it refuses.
  * `**Files you own:**`, `**Starts after `<lane>` is merged**`, `**Serial: ...**`,
    `**Produces:**` / `**Consumes:**`, and "the `<moment>` moment of `ecosystem/harness.yaml`" —
    `scripts/plan_lint.py` reads these to find collisions and ordering before the freeze.

  ROUTING IS DATA. The Model cell names the model the registry routes this lane's ROLE to
  (`ecosystem/provider-registry.yaml` — produce, review, orchestrate, ...); do not pick a model
  from memory. Commands come from `uv run --locked python scripts/dispatch.py launch --help`.
  Replace every <angle-bracket> placeholder; delete this comment.
-->
# LANE <slug> — <the value, as one clause>

| Model | Mode | Effort |
|---|---|---|
| <the model provider-registry.yaml routes this role to> | <execute|plan> | <low|medium|high|xhigh> |

**Read first:**
- the common rules: `to-cc/<BATCH-COMMON-...>.md`;
- the plan: `to-cc/<PLAN-...>.md` §<n> — the requirement this lane serves;
- <the one or two files that carry the decision this lane implements — an ADR, a ruling, a digest §>.

## Dispatch

```
claude --bg -n <slug> --model <model> --effort <effort> --permission-mode bypassPermissions --worktree <slug> "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-<id>-<slug>.md"
```

The launcher reads this block; the dispatcher runs
`uv run --locked python scripts/dispatch.py launch --batch <BATCH> LANE-<id>-<slug>.md`, and uses
this line by hand only when the launcher refuses, recording that it did.
<**Starts after `<lane>` is merged.** — only when this lane depends on another>

**Owns:**

**Files you own:** `<path>`, `<path>` and their tests; <the `<moment>` moment of `ecosystem/harness.yaml`, if any>.
<**Produces:** `<artifact>` · **Consumes:** `<artifact>` — only when another lane of the batch reads it>

<Operator authorization, quoted with its date, for any path this lane creates; a path not named here is not created.>

## Value

<Why this lane exists: the measured problem, in two or three sentences, and what is true after it.
This line is how the lane decides every question it meets at night — write it so it can.>

## Done-contract (immutable)

1. <A checkable end-state — the command or test that shows it, not "improved".>
2. <...>
n. **Close-out:** targeted tests for this diff; Codex review record citing its consumer (the row
   or this contract); self-check and purity per the common rules; handback in
   `to-browser/SESSION-<slug>.md` ending `HANDBACK <branch> @ <sha> <code|docs>`.

## Do not

- <An act outside the lane's scope that a reasonable executor might still take.>
- <Files owned by another lane of the batch, by name.>
- Create any path not named above.
