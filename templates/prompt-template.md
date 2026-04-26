# Prompt Template for Claude Code
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

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

## Git workflow
<!-- scope: meta -->

1. `git checkout -b <branch-name>` (branch name follows repo convention from AGENTS.md)
2. Commit after each step (or numbered group below)
3. Merge to main when green: `git checkout main && git merge --ff-only <branch>`

## UNDERSTAND
<!-- scope: meta -->

**Problem:** `<2-4 sentences describing what's wrong, why it matters, what's the desired end state>`

**What could break:**
- `<failure mode 1 — concrete, repo-specific>`
- `<failure mode 2>`
- `<add as identified>`

**Most likely failure mode:** `<the one that's most probable given the change shape — with mitigation>`

`<For Scale L: also include "What's already done that this builds on" pointing to ADRs, prior commits, related templates>`

## Step 1: `<imperative — what's done>`
<!-- scope: meta -->

`<concrete action with file paths, commands, or content>`

```powershell
<commands if applicable>
```

`<verification — how to know step succeeded>`

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

Merge: `git checkout main && git merge --ff-only <branch>`

## What NOT to do
<!-- scope: meta -->

- Do NOT `<anti-pattern specific to this task>`
- Do NOT `<scope creep risk>`
- Do NOT `<repo-specific hazard>`
- Do NOT touch `<repos or paths explicitly out of scope>`

---

**Section history:**
- v1.0 (2026-04-24) — initial template per Gap #2. Standard 8-section structure (Model/Mode/Effort → Title → Read first → Git → UNDERSTAND → Steps → Final → What NOT to do).
