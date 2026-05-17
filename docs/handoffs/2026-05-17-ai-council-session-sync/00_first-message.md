# First Message for New ai-council Chat

---

You are being onboarded to the `ai-council` project via a structured handoff. The files attached to this message contain everything you need to operate effectively in this codebase. Read all attached files before responding.

## Articulation gate — complete all four before continuing

Before generating any prompts or taking any actions, answer these four questions in your response:

1. **What is the single most important thing the next ai-council session must accomplish, and why is it the highest priority?**
2. **What is the recurring failure that Directive 1 is designed to fix — describe it in your own words, including what currently causes it and what the fix addresses?**
3. **What file must be created, what is it for, and what must it NOT be confused with?**
4. **What does the pre-commit hook verification tell you before other work begins, and what should you do if it fails?**

Do not proceed to synthesis or prompt generation until you have answered all four. If you cannot answer any of them from the uploaded files, say so explicitly — that indicates a gap in the bundle.

---

## Your role

You are the receiving session for the `ai-council` project. Your job is to:

1. Read the uploaded files
2. Answer the four articulation-gate questions above
3. Present a synthesis of the current state and what you will do
4. Wait for the operator to confirm or correct your synthesis
5. Ask the operator: "single Claude Code prompt or split into separate prompts?"
6. Generate the prompt(s) after confirmation

---

## Bundle orientation

| File | What it is |
|---|---|
| `01_MANIFEST.md` | Entry point: HEAD pin, file index, verification instructions |
| `02_VISION.md` | ai-council VISION — what the project is and does |
| `02b_ECOSYSTEM_VISION.md` | .dev-knowledge VISION — the ecosystem this project lives in |
| `03_PLAYBOOK.md` | How we work: methodology, conversation style, commit conventions |
| `04_ESSENTIALS.md` | High-leverage rules — read before making any decisions |
| `05_GOVERNANCE_ESSENCES.md` | ADR essences for rules that drive your actions |
| `06_STATE_OF_PLAY.md` | Current state: what was done, what's verified, what's missing |
| `07_ACTION_PLAN.md` | Objective, ordered directives, and boundaries |
| `08_TREE.txt` | Full tracked file tree at HEAD (what's in the repo) |
| `09_EXECUTION_EVIDENCE.md` | Fill this out as you execute directives |

---

## HEAD verification

Before generating any prompts, the prompt you generate for Claude Code must include this verification step:

```
git rev-parse HEAD
```

Expected: `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8`

If the result differs, Claude Code must stop and report the discrepancy. Do not proceed past the HEAD check until the operator confirms.

---

## After synthesis confirmation

After the operator types `synthesis confirmed` (or you address corrections):

- Ask: "Single Claude Code prompt or split into separate prompts?"
- Generate the prompt(s) as a copyable code block or downloadable `.md`
- The prompt(s) must reference `09_EXECUTION_EVIDENCE.md` — Claude Code fills it in as directives are executed

---

## Important constraints from the bundle

- Do NOT change Council `research`-mode runtime behavior — the fix for Directive 1 is a documentation change only
- Do NOT create AGENTS.md by inventing its specification if cross-repo scope decisions are needed — surface to the operator
- Do NOT edit existing LESSONS.md entries — only append (ADR-29)
- Do NOT recreate `CHANGELOG.md` — it was intentionally removed per ADR-49
- Do NOT skip the pre-commit hook verification before other work
