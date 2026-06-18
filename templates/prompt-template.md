# Prompt Template for Claude Code
<!-- scope: meta -->
<!-- version: 1.5 — 2026-06-18 -->

> **Copy this template, fill placeholders, save as `.md` artifact, deliver to Claude Code via paste-into-prompt.** Browser chat produces this; Claude Code executes it.
>
> **Per-Scale guidance:**
> - **Scale S** (single file change, <50 lines work): minimal version — Title + Steps + What NOT to do. Skip UNDERSTAND if obvious.
> - **Scale M** (multi-file or non-trivial logic): full template, but UNDERSTAND can be brief.
> - **Scale L** (3+ files, architectural change): full template required, plan-mode usually preferred.

---

| Model  | `<Sonnet | Opus>`             |
| Mode   | `<plan-then-auto | auto-accept>` |
| Effort | `<low | medium | high>`       |

# `<Imperative title — what this prompt accomplishes>`

**Repo:** `<absolute path to repo, e.g. C:\Users\1028120\Documents\Dev\corp-monorepo>`
**Purpose:** `<one sentence — what gets achieved by running this prompt>`

Read `CLAUDE.md`, `<other read-first files relevant to task>`, and check `~/.claude/skills/gotchas/` before starting.

**Governance pointer:** `<the specific ADR / LESSONS entry / sibling-spec this task touches, or "none">` — the architect fills this thin pointer; CC self-loads code-impact context + generic gotchas but won't self-infer governance context (ADR-87).

## Git workflow
<!-- scope: meta -->

1. `git checkout -b <branch-name>` (branch name follows repo convention from CLAUDE.md)
2. Commit after each step (or numbered group below)
3. Merge to main when green: `git checkout main && git merge --no-ff <branch>`

## UNDERSTAND
<!-- scope: meta -->

**Problem:** `<2-4 sentences describing what's wrong, why it matters, what's the desired end state>`

**What could break:**
- `<failure mode 1 — concrete, repo-specific>`
- `<failure mode 2>`
- `<add as identified>`

**Most likely failure mode:** `<the one that's most probable given the change shape — with mitigation>`

`<For Scale L: also include "What's already done that this builds on" pointing to ADRs, prior commits, related templates>`

## READINESS (explore-mode valve — ambiguous input only)
<!-- scope: meta -->

`<Include ONLY when the input is ambiguous — unclear scope, unstated acceptance
criteria, or more than one defensible interpretation. For a well-specified task,
delete this section and proceed to Step 1.>`

When the task is under-specified, do **not** start building. Emit a named
readiness verdict and stop:

- **Verdict:** `<READY | NEEDS-INPUT | BLOCKED>` — one word.
- **What's clear:** `<the parts you can act on with confidence>`
- **What's ambiguous:** `<each open question that changes what gets built — concrete, not "let me know if you have questions">`
- **Go / no-go:** on `NEEDS-INPUT` or `BLOCKED`, **create nothing** and wait for the operator. Only `READY` proceeds to Step 1.

A richer cousin of STOP-after-UNDERSTAND: UNDERSTAND records what you know;
READINESS forces an explicit go/no-go before anything is created. The valve's job
is to make "I wasn't sure, so I guessed" impossible — an unresolved ambiguity is
a stop, not a default.

## Step 1: `<imperative — what's done>`
<!-- scope: meta -->

`<concrete action with file paths, commands, or content>`

```powershell
<commands if applicable>
```

Verify: invoke the `verify` skill — any FAIL blocks this step.

**COMMIT:** `<conventional commit message — feat(scope): / fix(scope): / docs(scope): / chore(scope): / refactor(scope):>`

## Step 2: `<imperative>`
<!-- scope: meta -->

`<repeat structure — content + verification + COMMIT marker>`

`<Add Steps 3-N as needed. Each ends with COMMIT marker unless explicitly grouping into one commit.>`

## Final
<!-- scope: meta -->

```powershell
<verification commands — typically:>
python <validator if applicable>
git log --oneline -<N>
git status
```

`<Specific success criteria for this prompt — what must be true>`

**Obsolescence pass:** propose deletion of content this change supersedes, instead of writing around it — surface candidates with evidence for the operator to ratify (auto-delete stays forbidden; git history preserves). Per the PLAYBOOK §2 pruning-symmetry rule.

Final: `/ship "<summary> [#id if closing]"` — refuses if: on `main`, dirty tree, or validators red.

## What NOT to do
<!-- scope: meta -->

- Do NOT `<anti-pattern specific to this task>`
- Do NOT `<scope creep risk>`
- Do NOT `<repo-specific hazard>`
- Do NOT touch `<repos or paths explicitly out of scope>`

---

**Section history:**
- v1.0 (2026-04-24) — initial template per Gap #2. Standard 8-section structure (Model/Mode/Effort → Title → Read first → Git → UNDERSTAND → Steps → Final → What NOT to do).
- v1.1 (2026-06-06) — Final merge boilerplate replaced with `/ship` delegation (closes #103).
- v1.2 (2026-06-06) — Per-step verification line replaced with `verify` skill invocation (closes #104).
- v1.3 (2026-06-09) — Final gains a standing **obsolescence pass** line (propose deletion of superseded content instead of writing around it; operator ratifies) — point-of-use of the PLAYBOOK §2 pruning-symmetry rule (closes #136).
- v1.4 (2026-06-10) — UNDERSTAND gains an optional **READINESS valve** for ambiguous input (named verdict + go/no-go, create nothing until operator approves) — #111 (c). Folds as a valve, not a new organ.
- v1.5 (2026-06-18) — adds the **Governance pointer** field (the thin per-task ADR/LESSONS/sibling-spec pointer the architect always fills; CC won't self-infer governance context) — point-of-use of the ADR-87 equilibrium contract; dual-maintenance with PLAYBOOK §2 "Architect output vs CC consumption-spec".
