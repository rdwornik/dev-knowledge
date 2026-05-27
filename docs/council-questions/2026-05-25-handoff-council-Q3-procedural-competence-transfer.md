---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
---

## Question: How should the procedure for producing Claude Code prompts — the decision algorithm, model selection, and prompt structure — reach a fresh chat, given that shipping the reference docs has not reliably reproduced it?

### Current State

- Prompt-generation conventions (prompt skeleton, the Model/Mode/Effort table, the Sonnet-vs-Opus selection rule) live inside PLAYBOOK and are pointed to from the first message: "generate prompt(s) per `03_PLAYBOOK` conventions" (`00_first-message.md:86-96`).
- That pointer references a 2,718-line document; the procedure is prose spread through PLAYBOOK, not a self-contained worked algorithm (`00_first-message.md:86-91`; PLAYBOOK length measured on the 2026-05-25 bundle).
- The full PLAYBOOK ships in the bundle, yet the operator reports the receiver "forgets how to create prompts," with an unclear decision algorithm and unclear model selection (evidence `:128`).
- Prompt generation currently happens in the NEW browser chat, which then hands the prompt to Claude Code (the executor) to run (`HANDOFF_FOLDER_TEMPLATE.md:201-214`).
- The first message already carries an inline model-selection reminder (Sonnet for mechanical work, Opus for judgment-heavy work) but as a one-line note, not a decision artifact (`00_first-message.md:93-96`).

### Questions

1. **Where should prompt-generation authority sit?**
   - A: In the NEW browser chat, guided by PLAYBOOK (current).
   - B: In Claude Code (the executor), with the browser chat supplying only intent and constraints.
   - C: Split — the browser chat drafts intent, Claude Code formalizes the prompt structure.

2. **By what mechanism should the procedure transfer?**
   - A: Rely on the receiver reading PLAYBOOK conventions (current).
   - B: A compact, self-contained prompt-generation checklist/algorithm carried in the bundle.
   - C: Worked exemplar prompts (a few concrete examples) instead of, or alongside, prose rules.
   - D: A different mechanism (panel names it).

3. **Should model/effort selection be an explicit decision artifact?**
   - A: Keep the inline reminder in the first message (current).
   - B: A standalone decision table mapping task-type → model + effort.
   - C: Not needed — selection is situational and should stay a judgment call.

### Constraints

- The three-stage flow stays; the browser chat is stateless and cannot read the filesystem (`ADR-45:80-86`).
- Anything added must be self-contained in the bundle — no pointers to documents the receiver will not open.
- Which reference documents are in the bundle is decided in Q2; this debate concerns the transfer mechanism for procedure, not the document set.
- Layer-2 invariant: no orchestration/workflow scripts in `.dev-knowledge` (`ADR-28:15`).

### Adjacent concerns — handled in separate debates (not this one)

- Which reference documents the bundle carries → Q2.
- How the receiver internalizes the bundle before acting → Q1.
- Delivery form and where invariants live → Q5.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/research/2026-05-25-handoff-failures-evidence.md:124,128,149`
- Prompt-gen pointer + model reminder: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/00_first-message.md:86-96`
- Where prompt generation happens: `templates/HANDOFF_FOLDER_TEMPLATE.md:201-214`

### What a usable answer looks like

A decision on where prompt-generation authority lives and how the procedure is transferred, recorded as an amendment to `HANDOFF_FOLDER_TEMPLATE.md` / `00_first-message.md` generation rules, or a new ADR if it relocates authority off the browser chat. "Keep prose-in-PLAYBOOK, with rationale" is a legitimate outcome.
