> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-cc/AMEND2-PLAN-WAVE5-2026-09-24.md` (a Drive transport path, not retained in this
> repo — verifiable against the bytes landed below by their hash,
> `sha256:346046125f43c2d906c33f0b2012e5d9bb403c84b0c03a8a7890ceb8b349fc19`, 3,731 B, computed
> by this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-amend2-plan-wave5.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: the next landing commits it beside PLAN-WAVE5 and its first AMEND under docs/audits/
date: 2026-09-24
amends: to-cc/PLAN-WAVE5-2026-09-23.md and to-cc/AMEND-PLAN-WAVE5-2026-09-24.md — restores the Architekt Jutra tool trials and the distillers the master plan had dropped; fixes the wave order
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)
basis: the AJ digests of 2026-09-21 (`to-browser/DIGEST-AJ-ALL-FRONT-2026-09-21.md` and its master), the architect's tool-trial rulings of the same day, the operator's reminder 2026-09-24

# AMEND 2 — tool trials, distillers, and the wave order (monorepo last)

## Wave order, corrected

| Wave | Content |
|---|---|
| 5b | the harness core: ADR-121 step 2, launcher to router, hooks, path layer and transport adapter, organ instrument, built-ins replacing organs (O-10), subtraction under O-7/O-8 |
| 5c | off-box: the VM pilot, container tools, Actions runners, Copilot as a session |
| **5d — tools from the course** | the trials below, each measured by the tool-trial organ |
| **5e — distillers** | the three distillers below |
| finish line | one real monorepo feature through the loop |

## 5d — the tool trials (the list of 2026-09-21, none run yet)

**First the instrument:** the tool-trial organ — the existing sandbox rule plus a measurement taken
from receipts (tokens, wall time, cost, defects found), so every trial yields numbers.

| Trial | Measure it against | Order |
|---|---|---|
| Caveman — the skill only (MIT); its BSL engine stays deferred | tokens per turn, quality of contracts unchanged | 1 |
| RTK — command-output compression for the agent | context per session (`/context`), lane outcome unchanged | 2 |
| import-linter and Python boundary tools | boundary violations found; domain rules enforced by code | 3 |
| mutmut, widened beyond one file | mutation score per module; runtime | 4 |
| LiteLLM with the stage-13 adapter, after the supply-chain check | one provider entry for the router; served = ordered | 5 |
| JetBrains repository-intelligence layer, head to head with our graph | the same questions asked of both; answers compared | 6 |
| Copilot cloud agent as an off-box producer | lanes produced, local memory 0 | 7 (5c ties in) |
| Headroom — separately and last, because it sits on the link | context and cost, with a kill switch | 8 |
| the remaining 151 catalogue positions | sifted by code against the criteria recorded in the AJ digest; only survivors get a trial | 9 |

Rules: one trial per lane, read-mostly, night batch; nothing adopted without its numbers; every
adoption replaces something (O-7), it never only adds.

## 5e — the distillers

1. **The contract distiller** — `gen_lane_contract.py` exists. Rule: the architect writes intent,
   closure, anti-patterns and mode; the generator writes the contract in the plan lint's grammar.
   Hand-written contracts are the exception and follow that grammar.
2. **The learning distiller** — incident → cause → proposed mechanism → gated lane → regression
   test, on the event log (ADR-121). A cause seen twice triggers it by code.
3. **The prompt-to-skill distiller** — an organ that detects recurring order and prompt content on
   the transport and proposes a skill or command in its place, so prose migrates into skills the
   model invokes itself. Built-ins are checked first (O-10) before a skill is written.

## Not lost, only moved

- SQLite: the projection of ADR-121 step 3 (5b/5c); git-as-truth first.
- Git adoption from the ADR experiments: trailers hook, orphan state ref, CAS ref updates, bisect run
  — all in ADR-121 step 2 (5b); `bisect run` is already in use by lane-one-registry-ci.
