---
intake-id: 51
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I3
consumers: R3 (provider roles — queued, NOT admitted by this intake); the fleet provider registry
---

# Provider capacity — Chinese cloud models via Anthropic-compatible endpoints

## Problem / motivation

The fleet's capacity is bounded by one subscription, and every previous attempt to widen it
assumed a **new agent** with a new interaction model — a new CLI to install, a new contract shape,
a new set of lane mechanics. The landed research
(`docs/audits/2026-08-26-technical-research-chinese-coding-models.md`, L4) removes that assumption:
**DeepSeek, Z.ai/GLM, Moonshot/Kimi, MiniMax and Qwen each publish an Anthropic Messages-API-
compatible endpoint**, so **Claude Code drives them directly** — same lanes, same contracts, same
dispatch verbs, **no new agent and no new interaction model**. What is needed is one scoped wrapper
per provider, not a new fleet surface.

The same research names the hazard that makes this urgent to *rule* before it is *adopted*:
pointing Claude Code at another endpoint is done through `ANTHROPIC_BASE_URL` /
`ANTHROPIC_AUTH_TOKEN`, and **a global value silently routes every Claude Code session — hub lanes
included — off the subscription.** That is the identical defect class as the 2026-08-26 credential
leak, measured in `docs/audits/2026-08-26-technical-provider-surface-repair-summary.md` §1, where
a profile-level export overrode the subscription in **every new terminal** and a one-shell
`Remove-Item` looked like a fix but was only a diagnostic.

**This intake therefore embeds ruling 7 as a hard precondition, not as advice.**

## Scenarios (+1 view)

- **As the operator running a volume lane**, I dispatch a contract to a prompt-metered provider
  and the lane behaves exactly like a local Claude Code lane, because it is one.
- **As the operator on a hard problem**, I route that one lane to the strongest available coding
  model without touching any other session.
- **As any session on this machine at any time**, my Claude Code run bills to the subscription,
  because **no billing-relevant variable is ever set globally** — a scoped wrapper sets it for one
  child process and nothing else.

## Functional requirements

- **Must — the hard register rule (ruling 7, ratified):** `ANTHROPIC_BASE_URL` and
  `ANTHROPIC_AUTH_TOKEN` are **never set globally**. A provider is reachable only through a
  **scoped wrapper** that sets them for a single child invocation. **One check covers this and the
  credential-leak class together** — that check is born as a row by this session's act 7.
- **Must:** operator selection is **DeepSeek (already held) + GLM + Kimi** — GLM for volume on a
  prompt-metered plan, Kimi for hard problems as the strongest independent coding benchmark of the
  set. **Qwen optional fourth. MiniMax skipped.** DSH is **REJECTED-BY-FIT** by operator ruling —
  a localhost web UI is the wrong model for a CLI lane — and that is a rejection, not a failure to
  install.
- **Must — registry consequences, presence only:** `deepcode` recorded as a **third strict
  `AGENTS.md` provider** for intake #48; **Cursor recorded blocked-with-cause rather than absent**
  (the only documented Windows route force-copies its binary onto the bare name `agent`, which is
  poisoned on this host per ruling 6); and **a measured-on date is required for fast-moving
  third-party CLIs** — `deepcode` moved two minor versions in one day.
- **Should:** one wrapper shape shared by all providers, so adding a fourth is configuration.
- **Could:** a per-provider health probe that reports `info` when it cannot judge, never a silent
  pass.

## Acceptance criteria (ex-ante)

1. A fresh terminal, profile loaded, has **neither** billing-relevant variable set — asserted by a
   check that **launches a child shell** rather than reading its own environment, because reading
   the current process is the exact mistake that produced a false all-clear before.
2. That check **never prints a value**, and a test asserts a planted secret reaches neither stdout
   nor stderr.
3. A lane dispatched through a provider wrapper completes with the same contract and verb as a
   local lane, and `claude` in **every other** shell still reports the subscription.
4. Each registry row carries a **measured-on date**, and a row older than its declared staleness
   window is reported as stale rather than trusted.
5. The check reports `info` when it cannot judge — never green-by-skip.

## Non-goals

- **Provider ADMISSION and role assignment. R3 owns roles and stays queued** — this intake
  establishes capacity, presence and the safety precondition only. Nothing here admits a provider.
- Benchmarking or model selection beyond recording the operator's stated selection.
- Any change to how lanes or contracts are written — the whole point is that none is needed.

## Impact sketch (4+1 lite)

- **Logical:** providers become a configuration axis behind one existing interaction model.
- **Process:** R3 gains a measured presence table instead of an argument.
- **Development:** one scoped wrapper per provider plus one shared guard check.
- **Physical:** capacity ceases to be bounded by a single subscription — **only after** the guard
  exists, never before.

## Open questions

1. Does headless Claude Code behave identically against each compatible endpoint, or do tool-use
   and streaming diverge in ways a lane would hit? (Measure per provider; do not assume.)
2. `deepcode`'s supply chain — single unattributed maintainer, MIT, four months old, daily
   updates — should R3 rule before it is given a key and shell permissions?
3. `gemini` has changed failure class from free-tier quota to **client deprecation**
   (`UNSUPPORTED_CLIENT`), so a tier upgrade alone may not revive it. Retire the CLI, or wait?

## Status

READY — filed 2026-08-26 by the endgame governance session, with **ruling 7 embedded**. Evidence:
`docs/audits/2026-08-26-technical-research-chinese-coding-models.md` (L4),
`docs/audits/2026-08-25-technical-probe-providers-report.md`,
`docs/audits/2026-08-25-technical-probe-dsh-report.md`, and
`docs/audits/2026-08-26-technical-provider-surface-repair-summary.md` (redacted derived summary).
