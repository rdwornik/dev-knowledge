---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
---

## Question: What determines which context a handoff bundle carries, and should that set be the same for every handoff or selected for the work the next session will do?

### Current State

- Every bundle carries full, non-curated copies of three invariants — VISION, PLAYBOOK, ESSENTIALS — regardless of handoff type (`HANDOFF_PROCESS.md:470-472`; `HANDOFF_FOLDER_TEMPLATE.md:294-304`; `ADR-42:233-242`).
- Measured on the 2026-05-25 `.dev-knowledge` bundle: `03_PLAYBOOK.md` is 2,718 lines (~145 KB) — about 94% of the bundle's markdown bytes; `04_ESSENTIALS.md` is 366 lines; `02_VISION.md` is 155 lines (`wc -l` on `docs/handoffs/2026-05-25-dev-knowledge-session-sync/`).
- The operator reports that without PLAYBOOK and ESSENTIALS, prompts are generated badly (evidence `:124`).
- The operator separately questions why a receiver should read PLAYBOOK and ESSENTIALS "when the most important thing is using skills, journals, and gotchas when they are needed" (evidence `:126`).
- Skills, gotchas, and JOURNAL are not part of the bundle inventory — the 11/12-file list contains none of them (`HANDOFF_FOLDER_TEMPLATE.md:28-79`).
- Content selection is currently unconditional: the same invariant set ships whether the next session is mechanical hygiene or judgment-heavy architecture work (`docs/audits/2026-05-20-handoff-process.md:139`).

### Questions

1. **Should bundle content be fixed or conditional?**
   - A: Fixed full-invariant set on every handoff (current).
   - B: Conditional on handoff type or the next session's directives (e.g., prompt-generation-heavy vs mechanical work get different sets).
   - C: Layered — a small always-loaded core plus on-demand references the chat requests when a task needs them.

2. **What content types belong in the bundle?**
   - A: Keep VISION/PLAYBOOK/ESSENTIALS as the methodology anchors; do not add skills/gotchas/JOURNAL.
   - B: Add skills/gotchas/JOURNAL alongside the existing invariants.
   - C: Make skills/gotchas/JOURNAL the primary methodology source and demote PLAYBOOK/ESSENTIALS to reference.
   - D: A different composition (panel names it).

3. **What principle decides inclusion?**
   - A: "Include everything that prevents the receiver from hallucinating norms" (the current SECI-externalization rationale).
   - B: "Include only what the next session's directives actually invoke."
   - C: A different principle.

### Constraints

- The receiver cannot dereference filesystem pointers — anything it needs must be inlined or operator-uploaded (`ADR-45:80-86`).
- The Self-Containment Rule is load-bearing and was explicitly not rolled back (evidence `:138`).
- Full invariants have empirically caught architect fabrications via drift detection (real case: 2026-05-09 ai-council handoff) (`ADR-45:21-31`).
- Delivery form — full copies vs pointer vs condensed, and file count — is decided in Q5, not here. This debate is about which content types are relevant.

### Adjacent concerns — handled in separate debates (not this one)

- Delivery form, file count, full-copy-vs-pointer → Q5.
- How the receiver internalizes whatever is delivered → Q1.
- The mechanism by which prompt-generation procedure transfers → Q3.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/research/2026-05-25-handoff-failures-evidence.md:124,126,138,146`
- Invariant rule: `protocols/HANDOFF_PROCESS.md:470-472`; `templates/HANDOFF_FOLDER_TEMPLATE.md:294-304`
- Measured sizes: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/` (`wc -l`)
- Unconditional-selection observation: `docs/audits/2026-05-20-handoff-process.md:139`

### What a usable answer looks like

A decision on the content-selection principle and content types, recorded as an amendment to `HANDOFF_PROCESS.md` / `HANDOFF_FOLDER_TEMPLATE.md`, or a new ADR if it changes the invariant contract. The operator's stated tension (PLAYBOOK/ESSENTIALS necessary for prompt quality, yet questioned against skills/gotchas/JOURNAL) is the thing the debate must resolve, not assume.
