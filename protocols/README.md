---
reconciled_with: handoff-process@5.7
---

# protocols/ — canonical universal-methodology genre (hub)

**Scope marker (BACKLOG #314 / #327).** In the fleet, `protocols/` is a
**methodology-mandated genre** — "what other repos/agents must know to interact with
THIS repo" — with the universal methodology-vs-project boundary applied INSIDE it. This
is the **hub**, so `protocols/` here is the **canonical home of the universal
methodology**: the docs below are the source consumers point at, never copies.

Canonical methodology docs (universal — read via this `protocols/`, never copied into a
consumer):

- `ESSENTIALS.md` — Rob's universal working style (summarizes PLAYBOOK, does not copy it)
- `PLAYBOOK.md` — universal protocols; the full methodology reference
- `AGENT_FRAMEWORK.md` — agent / subagent operating framework
- `HANDOFF_PROCESS.md` — the handoff protocol (v5; CC-owned residual + probe manifest)
- `HANDOFF_BOOT.md` — the thin browser-chat boot entry
- `SESSION_SETUP.md` — session bootstrap / environment wiring
- `ENVIRONMENT.md` — the `~/.claude/` runtime + machine environment contract
- `DEFINITION_OF_DONE.md` — the session-close definition-of-done (ADR-85, Stop-gated)

**Consumers hub-pointer here.** Child repos do NOT copy these files; their `CLAUDE.md` §1
reads them at this hub `protocols/` path by design. A consumer's own `protocols/` holds
only its **project-local, marked** interface docs (the "marked" half of the #314 split —
see e.g. `ai-council/protocols/README.md`).

> Note: `AI_COUNCIL_PROCESS.md` is a **different genre** living here — ecosystem *process*
> governance for the six-step gated Council process (ADR-67), not a tool-operational or
> universal-methodology doc. Its residence here is historical; the #327 interface-genre
> ruling will settle its placement. No content overlap with the methodology docs above.

---

**Seed shell** (BACKLOG #314 partial): this states the genre + the hub-pointer /
local-marked boundary. The full interface-genre definition (the genre wording + one
interface doc per repo) lands with #327.
