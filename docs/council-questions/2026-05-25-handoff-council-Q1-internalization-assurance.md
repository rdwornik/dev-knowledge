---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
---

## Question: What mechanism should a handoff use to confirm a fresh chat has internalized the bundle — rather than only paraphrased it — before it begins substantive work?

### Current State

- A handoff delivers a flat bundle (~12 entries) to a fresh ("NEW") browser chat. The NEW chat's required first action is a four-item articulation gate: write, in its own words, (1) its role per VISION, (2) the current phase, (3) the immediate next action, (4) the top-3 hard constraints. It then produces a receiver synthesis. Both are gated on the operator typing `role confirmed` (`00_first-message.md:33-71`; `HANDOFF_FOLDER_TEMPLATE.md:113-161`).
- On 2026-05-25 a NEW chat passed the gate, but its item 2 asserted a dependency — "scrum-master codification is blocked behind the consolidation decision" — that the bundle's own action plan contradicts: the plan lists an explicit shelve-consolidation → pivot-to-scrum-master path (`07_ACTION_PLAN.md:22-24,37-38`; evidence file `:50-52`).
- One turn after passing the gate, the same chat could not apply bundle standards (VISION, the uploaded files) to a substantive request; operator assessment: "nie zapoznał się ani z Vision, ani z plikami" (evidence `:65-76`).
- A second NEW chat the same evening showed the same shape: upload + gate, then visible comprehension failure on substantive work (evidence `:80-87`).
- Cross-actor finding: the gate's "paraphrase X" task was satisfiable by pattern-match; work that required "use X to decide Y" exposed that internalization had not happened (evidence `:91-99`).

### Questions

1. **What form should the pre-work internalization check take?**
   - A: Keep the current "paraphrase in your own words" articulation gate unchanged.
   - B: Forced-retrieval gate — require answers that can only be produced by reading specific bundle locations (cite file + section), not paraphrased from memory of the upload.
   - C: Applied-task proof — require the chat to apply one bundle rule to a small concrete case before real work (e.g., "given situation X, what does the action plan direct?").
   - D: A different approach (panel names it).

2. **How many engagement passes should the reading process require before work?**
   - A: Single pass plus one gate (current).
   - B: Staged/progressive disclosure — the bundle is revealed in ordered segments, each with its own checkpoint.
   - C: Mandatory clarifying-question round — the chat must ask N questions (routed to the OLD chat) before it may act.

3. **What should happen when the check cannot be satisfied?**
   - A: The chat self-flags "cannot articulate [N]" and stops (current).
   - B: Operator-driven reload/re-upload loop until the check passes.
   - C: Treat failure as bundle inadequacy and regenerate the bundle, not as a reader failure.

### Constraints

- The three-stage relay is validated and stays; it is not under review here (evidence `:137`).
- The receiver is a stateless browser chat with no filesystem access — it can act only on what is uploaded into the session (`ADR-45:80-86`).
- The operator is the only human in the loop; there is no architect-side automated hook to install (`docs/audits/2026-05-20-handoff-process.md:198`).
- Layer-2 invariant: no orchestration/workflow scripts live in `.dev-knowledge` (`ADR-28:15`; evidence `:159`).

### Adjacent concerns — handled in separate debates (not this one)

- Which content the bundle carries (PLAYBOOK/ESSENTIALS vs skills/gotchas/journal) → Q2.
- Whether prompt-generation skill transfers across chats → Q3.
- Sender-side verification and who reviews this gate's output → Q4.
- Whether a document bundle is the right delivery mechanism at all → Q5.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/research/2026-05-25-handoff-failures-evidence.md:40-99,137,159`
- Live gate as delivered: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/00_first-message.md:33-71`
- Gate spec: `templates/HANDOFF_FOLDER_TEMPLATE.md:113-161`
- Contradicted dependency: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/07_ACTION_PLAN.md:22-24,37-38`

### What a usable answer looks like

A decision on the internalization-check mechanism, recorded as an amendment to `HANDOFF_PROCESS.md` / `HANDOFF_FOLDER_TEMPLATE.md` (if it changes the gate) or a new ADR (if it changes the engagement architecture). "Keep status quo, with rationale" is a legitimate outcome.
