---
last_reviewed: 2026-09-06
reconciled_with: handoff-process@7.1.0
status: active
owner: Rob
---

# protocols/ — canonical universal-methodology genre (hub)

**Scope marker (BACKLOG #314 / #327).** In the fleet, `protocols/` is a
**methodology-mandated genre** — "what other repos/agents must know to interact with
THIS repo" — with the universal methodology-vs-project boundary applied INSIDE it. This
is the **hub**, so `protocols/` here is the **canonical home of the universal
methodology**: the docs below are the source consumers point at, never copies.

Canonical methodology docs (universal — read via this `protocols/`, never copied into a
consumer):

- `PLAYBOOK.md` — universal protocols; the full methodology reference
  (`ESSENTIALS.md` was DELETED 2026-09-14 by `[#628]`; its doctrine moved here on
  2026-07-05 per `[#258]`, so PLAYBOOK is the sole universal-protocol read)
- `AGENT_FRAMEWORK.md` — agent / subagent operating framework
- `HANDOFF_PROCESS.md` — the handoff protocol (v7; CC-owned residual + probe manifest, one-round-trip boot, plus the §17 BOOT-INVERSION). The live version is the file's own `Version:` header, not this line
- `HANDOFF_BOOT.md` — the thin browser-chat boot entry
- `SESSION_SETUP.md` — session bootstrap / environment wiring
- `ENVIRONMENT.md` — the `~/.claude/` runtime + machine environment contract
- `DEFINITION_OF_DONE.md` — the session-close definition-of-done (ADR-85; teeth at pre-push since the amendment 2026-08-03, not Stop-gated)
- `STANDING_RULINGS.md` — the ratified-in-chat rulings agents apply silently, with no other landed home yet
- `FUNNEL_LIFECYCLE.md` — the governed-object state machine (states, transitions, terminal conditions, archival) unifying ADR-98/111/100/70

**Consumers hub-pointer here.** Child repos do NOT copy these files; their `CLAUDE.md` §1
reads them at this hub `protocols/` path by design. A consumer's own `protocols/` holds
only its **project-local, marked** interface docs (the "marked" half of the #314 split —
see e.g. `ai-council/protocols/README.md`).

> Note: `AI_COUNCIL_PROCESS.md` is a **different genre** living here — ecosystem *process*
> governance for the six-step gated Council process (ADR-67), not a tool-operational or
> universal-methodology doc. Its residence here is historical; the #327 interface-genre
> ruling will settle its placement. No content overlap with the methodology docs above.

> Note: `REPO_ONBOARDING.md` — the repo-onboarding runbook (bring a repo onto the
> universal methodology baseline). An **operational process spec**, not a consumer
> hub-pointer doc; collapsed here from the one-member `docs/runbooks/` genre per the
> ADR-101 amendment 2026-07-22 (d.i reversal).

**Filename casing (ADR-34, written down 2026-07-22):** every file in `protocols/` follows
the ADR-34 file-type table row `Protocols → UPPERCASE_WITH_UNDERSCORES.md` (example:
`HANDOFF_PROCESS.md`). The existing residents all conform — they are the de-facto pattern
ADR-34 codified, not carve-outs — and `REPO_ONBOARDING.md` was renamed from
`repo-onboarding.md` at its 2026-07-22 move-in to conform. (The row itself is a recorded
carve-out from ADR-34's 2026-05-11 universal-hyphen separator amendment, acknowledged in
that ADR's Consequences.)

---

**Seed shell** (BACKLOG #314 partial): this states the genre + the hub-pointer /
local-marked boundary. The full interface-genre definition (the genre wording + one
interface doc per repo) lands with #327.
