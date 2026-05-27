---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
---

## Question: Should verification discipline be enforced symmetrically across handoff actors, and who is responsible for substantively reviewing a receiver's articulation before work proceeds?

### Current State

- The methodology gates the receiver (the four-item articulation plus synthesis, confirmed by the operator) but checks the sender's Stage 2 output only for factual claims against the repo and for section thinness — it does not check confident assertions that were never verified (`HANDOFF_FOLDER_TEMPLATE.md:455-485`; `HANDOFF_PROCESS.md:340-348`).
- During the 2026-05-25 sender session, seven verification-miss instances were logged while generating prompts, including a hallucinated bundle file-map that referenced files which do not exist in the repo (evidence `:24-32`).
- Pattern characterization in the evidence: confidence itself was the signal to verify, not to skip; the misses occurred in the chat that held the most context about the system being changed (evidence `:34-36`).
- When the sender chat reviewed the receiver's articulation, it confirmed "role confirmed" without flagging the false item 2 — gates were treated as acknowledgement checkpoints rather than substantive review (evidence `:54,148`).
- The action plan already encodes a discipline rule ("'I'm confident' is the signal to verify harder") but as prose, not as a gate (`07_ACTION_PLAN.md:130-133`).

### Questions

1. **Should the sender (OLD chat / prompt generator) have a pre-send verification gate analogous to the receiver gate?**
   - A: No — keep sender-side verification as prose discipline (current).
   - B: Yes — a symmetric self-verification gate requiring a cited source for each load-bearing claim before output is sent.
   - C: Defer sender verification to the executor (Claude Code pre-flight), not the browser chat.

2. **Who substantively reviews the receiver's articulation?**
   - A: The operator, via the `role confirmed` phrase (current).
   - B: The OLD/sender chat reviews the articulation against the bundle and flags drift before confirmation.
   - C: A mechanical check compares the articulation against the bundle's own claims (executor-side).

3. **What triggers a verification pass?**
   - A: Reader judgment / self-flag (current).
   - B: A fixed rule — a confident claim about an unread source mandates a verification pass.
   - C: A different trigger.

### Constraints

- The three-stage flow and operator-in-the-loop stay (evidence `:137`).
- Browser chats cannot run shell or read the filesystem; any mechanical check can only live on the executor side (`ADR-45:80-86`).
- Layer-2 invariant: no orchestration/workflow scripts in `.dev-knowledge` (`ADR-28:15`).
- The receiver gate's own design is decided in Q1; this debate concerns sender-side symmetry and who owns review of the gate's output.

### Adjacent concerns — handled in separate debates (not this one)

- The design of the receiver gate itself → Q1.
- Whether prompt-generation procedure transfers across chats → Q3.
- Bundle content and delivery form → Q2, Q5.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/council-questions/2026-05-25-handoff-failures-evidence.md:20-36,54,148`
- Stage 3 factual-verification layer (sender claims): `templates/HANDOFF_FOLDER_TEMPLATE.md:455-485`
- Stage 3 thinness pre-flight only: `protocols/HANDOFF_PROCESS.md:340-348`
- Existing prose discipline rule: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/07_ACTION_PLAN.md:130-133`

### What a usable answer looks like

A decision on (a) whether the sender gets a verification gate and where it runs, and (b) who reviews the receiver's articulation — recorded as an amendment to `HANDOFF_PROCESS.md` (Stage 2 / Stage 3 procedure) or a new ADR if it introduces a sender-side gate. "Keep asymmetric, prose-only, with rationale" is a legitimate outcome.
