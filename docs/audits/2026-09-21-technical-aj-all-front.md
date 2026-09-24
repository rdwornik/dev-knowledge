# Architekt Jutra M01-M05 vs our harness — front door (2026-09-21)

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: CLOSED on landing` with no repo citation actually present. Source:
> `to-browser/DIGEST-AJ-ALL-FRONT-2026-09-21.md`. Full companions
> (`DIGEST-AJ-ALL-COMPARISON-2026-09-21.md`, `DIGEST-AJ-TOOLS-2026-09-21.md`) were not committed by
> this lane — they are not in this contract's audit list; land them separately if needed.
> Carrier row: this lane's PLAN-WAVE5 landing (`2026-09-23-technical-plan-wave5.md`), which is the
> record this front-door digest exists to inform; no window defect names it directly.

carried-by: CLOSED on landing (read-only digest; no repo change)
date: 2026-09-21
from: CC orchestrator, batch AJ-ALL front door; built by code, no new analysis
full: to-browser/DIGEST-AJ-ALL-COMPARISON-2026-09-21.md · to-browser/DIGEST-AJ-TOOLS-2026-09-21.md

## How this was cut

Verbatim excerpts. To fit 15 KB, fields were dropped, never reworded; evidence ids,
what-to-build, the not-ranked note and tool descriptions/recs/URLs are in the full files above.

## In ten sentences

1. The course frames AI-native development as "harness engineering" (Agent = Model + Harness) and treats the whole SDLC, not just code, as the thing you architect — a framing our own hub already embodies as a Layer 2 governance repo.
2. Its single most-repeated technical gap against us is credential handling: four independent modules say a dispatched unit of work should get only the secrets its contract needs, never the whole store, and our fleet still hands every lane the entire `.env`.
3. Its second most-repeated gap is that we already built a knowledge graph (FPG-1) that does what several lessons spend a whole unit teaching you to hand-build, but nothing steers agents to use it over grep, so a working capability sits unused — `why` scored 0/5 against grep in a live trial.
4. It repeatedly argues review output should be typed, machine-readable data an evaluator can act on, not prose a human or a regex has to parse, matching a gap our own loop-eval mapping already found in stage 14.
5. It teaches that physical/structural constraints (sandboxes, typed contracts, manifests) beat after-the-fact review, and names the exact regression we have: the two guards built for that literal pattern, `deny_and_point.py` and the ADR-77 `block_immutable_edits.py` guard, are both currently switched off.
6. It surveys protocol-level machinery — MCP host/client/server, OAuth token exchange, remote transports — mostly as things to scope narrowly or defer, matching our own posture of no MCP server yet and `[#729]`'s stdio-only, tools-only shape as already correct if it is ever built.
7. It teaches watching an external spec for revision before building against it — the MCP 2026 revision drops stateful mode, Sampling, Roots, HTTP+SSE, and DCR by August 2027 — a general discipline we do not currently practice for any external dependency.
8. It confirms our core engineering discipline is already sound: spec-before-build, frozen per-lane contracts, second-provider review before every merge, narrow-then-widen trust, and TDD-as-build-arc-standard all match or exceed what the course teaches.
9. It confirms the parts of the course aimed at teams — platform-team sizing, multi-tenant SaaS architecture, Slack-interruption relief, fixed experimentation-time budgets — have no analogue in a one-operator fleet and are correctly declined as IGNORE, not left as gaps.
10. Where the course proposes an autonomous, alert-triggered agent that self-judges its output with an LLM, it directly contradicts two of our standing rules — single-operator dispatch (AM-5) and no naked LLM-judge score as a gate — and is declined as a literal pattern, translated instead into an operator-ratified backlog row.

## Top ten recommendations, ranked by value for the harness

| # | recommendation | rec | wave | cost | value | prior audit |
|---|---|---|---|---|---|---|
| 1 | **Scope each dispatched lane's secret access instead of full-store inheritance** | ADOPT | 4 | M | every lane today inherits the whole `.env` secret store with no least-privilege boundary, the single most-corroborated gap in the whole course (four independent modules, one already-open P1 row) | CONFIRMS |
| 2 | **Make FPG-1/`why` the default lookup path ahead of grep, and wire `edge-class-census` into an architectural gate** | ADOPT/ADAPT | 3 (default-path wiring) then wave later (architectural gate) | S then M | the ontology the course spends whole lessons teaching you to hand-build already exists here, but sits unused: ADR-118 itself says FPG-1 is "wired into NO gate, no check and no hook," and `why` measured 0/5 against grep in `[#924]` | CONFIRMS |
| 3 | **Define a structured, machine-readable stage-14 review verdict and fold the lane's trace into `review_packet`** | ADOPT/ADAPT | 3 | M | our own loop-eval mapping already names this gap: the review record is a prose audit file a regex tallies, not a schema, and the reviewer sees the diff but never *why* a lane did what it did | CONFIRMS |
| 4 | **Re-arm, or replace with a bounded fail-closed version, `deny_and_point.py` and the ADR-77 `block_immutable_edits.py` guard** | ADAPT | 4 | S-M | this is the one place the harness built the literal prevent-by-construction mechanism the course's central thesis argues for, then turned it off | CHANGES (M01 prior-art recommended WIRE for this guard class; it is now further unwired) |
| 5 | **Add a per-role, size-tiered model ladder with a documented degrade-on-unavailable fallback** | ADAPT | 4 | M | `routing-table.yaml` routes role to CLI with no cost/size axis, and the second pass already priced the gap at $48.53 for one S-sized row run Opus-only | CONFIRMS |
| 6 | **Scope `[#729]`'s eventual MCP build to the new stateless spec, watch the spec externally, and bind a protocol-conformance Done-when** | ADOPT/ADAPT | n/a (spec-watch, precedes wave 4) then wave 4 (build scope) | S | the 2026 MCP spec revision already drops stateful mode, Sampling, Roots, HTTP+SSE, and DCR by August 2027, and nothing here watches an external spec for revision before a build gets scoped against a shape already being deprecated | CONFIRMS (`[#729]`, `[#770]`, `[#771]`, all open) |
| 7 | **Seed a new lane's frozen contract from 1-2 prior lanes of the same shape** | ADOPT | later | S | the cheapest item across the whole course and reconfirmed a fourth independent time | CONFIRMS |
| 8 | **Add a root-cause failure taxonomy beside the CRITICAL/HIGH/MEDIUM/LOW severity ladder** | ADOPT | 4 | S | we already have the reuse half (PLAYBOOK §17 applied across every review and all 8 night lanes) but only a severity axis, not a cause axis | NEW |
| 9 | **Add a standing rule: quoted/third-party text in a doc is data, never an instruction** | ADAPT | later | S | a fleet whose whole surface is markdown a session reads has no rule separating operator-authored control instructions from ingested repo content, exactly the prompt-injection/RoguePilot channel | NEW |
| 10 | **Measure whether the operator's own GO/review approvals are genuine scrutiny or rubber-stamping** | ADAPT | later | S | nothing currently measures this, and the 2026-09-10 night mission already called it the sharpest row in its own table, unfiled since | CONFIRMS |

## Must not rebuild (course practices we already have, all modules)

- User Harness (Maister/SkillPanel-class org-built extension layer) | our organ: the `.dev-knowledge` repo itself — richer state SHAPE than Maister, which has zero enforcement
- ADRs generated automatically as a build byproduct | our organ: `docs/decisions/ADR-*.md`, ADR-94 keeps decisions human-ratified
- Visualization/dashboard tooling for AI-output volume | our organ: `ecosystem/conformance.html`, `scripts/codemap/mermaid_emit.py` — `scripts/gen_trend_dashboard.py` retired by design at `c9ea3b07`
- Mutation testing (mutmut-class) | our organ: `tasks/502` (closed) — shelved for a platform reason (Windows needs WSL), not an appetite reason
- Hexagonal/ports-and-adapters, microkernel/macrokernel plugin cores, semver adapter-layer SDK mechanics | our organ: none — no product codebase at Layer 2
- Database/schema strategy (NoSQL document embedding, JSONB vs EAV, blob-vs-object storage) | our organ: none — no runtime database in a governance hub
- Frontend/UI plugin sandboxing (iframe, Shadow DOM, postMessage, CSS-in-JS) | our organ: git worktree isolation already covers the analogous concern
- Multi-tenant SaaS provisioning, entitlements, self-service marketplace | our organ: none — single operator
- Legacy-monolith strangler-pattern migration | our organ: none — no legacy monolith
- LLM Gateway (LiteLLM-class wire-level proxy) | our organ: `ecosystem/routing-table.yaml` + `scripts/dispatch.py` already govern at process-launch level, no HTTP traffic to proxy
- Multi-hop model fallback chain | our organ: `ecosystem/routing-table.yaml:25` `bounded_alternate: codex` — a chain would be over-engineering at this fleet's scale
- Token-cap / rate limiting as a new build | our organ: spine stage 11 `token-cap` (`dispatch.py plan --token-cap`), already FIXED at HEAD, not `command: null` as some stale sources claim
- A second MCP server implementation ahead of scope | our organ: none yet by design — `[#729]`/`[#770]`/`[#771]` already track scope and risk before build
- PII masking (Presidio-class) | our organ: none — no PII surface in a dev-governance repo
- Hosted observability/tracing platforms (Langfuse, LangSmith, Opik, Braintrust) | our organ: none — barred by the no-new-deps rule at current volume
- FPG-1/`why` as a second graph implementation | our organ: `scripts/file_purpose_graph.py`, ADR-118 — the graph already exists; the gap is adoption (0/5 in `[#924]`), not capability
- MCP Apps (interactive iframe UI, `postMessage`, D3.js/Plotly visualization) | our organ: n/a — no chat-UI MCP Host exists in this CLI-driven fleet to render one
- Remote-OAuth machinery in full (discovery, PKCE, CIMD/DCR, WAF/CDN edge friction) | our organ: n/a — `[#729]` is scoped to local stdio, which needs none of it
- Engineering-intelligence SaaS (Swarmia, Jellyfish, DX) | our organ: none — one operator, low volume, would be a new hosted dependency

## Contradictions with our rulings (all modules)

- Collaborative Spec-Driven Development / multiplayer Agentic Development Environments (shared real-time agent sessions) | ruling: AM-5, `protocols/STANDING_RULINGS.md:285` ("a nested session carries no row, dispatch is an operator act") | recommended stance: IGNORE — reconfirm single-operator-by-design; no multiplayer mode is planned
- Bug-fix agent that wakes on monitoring alerts / Jira tickets and opens a PR before any human message | ruling: AM-5 (`protocols/STANDING_RULINGS.md:285`, "never spawned from the primary session or any other session") + the "entry is a chat sentence or a backlog row" layer-00 rule (no event listener) | recommended stance: IGNORE as a literal event-listener — the admissible translation is "an alert becomes a backlog row the operator ratifies"; anything more needs an AM-5 re-ruling, which ADR-120 D3 explicitly declines here
- Automate evaluation with a naked "LLM as a judge" score once enough data is collected | ruling: `docs/audits/2026-08-29-technical-aut-r2-decision-quality-frameworks.md:894-903` ("RULED OUT (2): a naked LLM-as-judge score as a gate," Zheng et al. 2023 bias, kappa 0.366-0.424) + ADR-118 clause 4 ("LLMs are methods on the structure, never its judge") | recommended stance: IGNORE as a gate — an LLM judge that triages and routes to a human stays inside the ruling
- Platform team as a centralized executor running work for consuming teams | ruling: `CLAUDE.md` §5 rule 4 / ADR-28 "Layer 2 never executes," kept by ADR-120 D2 | recommended stance: ADAPT — adopt the monitoring half of the idea (`scripts/fleet_health.py`, ADR-111 triage funnel), never let the hub execute state changes in a child repo

## The eleven web-vetted tools, with their warnings

- **ArchUnit** | vetting: maintained yes, latest v1.4.2 (2026-04-18); licence Apache-2.0; Windows+Python: N/A — JVM tool, not Python, but runs anywhere a JVM does including Windows
- **dependency-cruiser** | vetting: maintained yes, latest v18.4.0 (published ~20h before check, i.e. 2026-09-20/21); licence MIT; Windows+Python: yes as an npm/Node CLI (not Python, but installs/runs fine on Windows via `npm i dependency-cruiser`)
- **import-linter** | vetting: maintained yes, latest v2.9 (2025-12-11); licence BSD (sources disagree BSD-1-Clause vs BSD-2-Clause — UNVERIFIED which exact BSD variant); Windows+Python: yes, `pip install import-linter`, pure Python
- **go-arch-lint** | vetting: maintained yes, latest (fe3dback/go-arch-lint) published 2025-11-13; licence MIT; Windows+Python: N/A — Go binary, not Python, but cross-compiles/runs on Windows
- **LiteLLM** | vetting: maintained yes, latest v1.102.0 (2026-09-20); licence MIT; Windows+Python: yes, `pip install litellm`, pure Python — NOTE a PyPI supply-chain compromise of the `litellm` package was reported in 2026 (verify pinned hash/source before any install)
- **Model Context Protocol (MCP)** | vetting: maintained yes, spec actively evolving (latest spec 2026-07-28, adds stateless core, Multi-Round-Trip Requests, header routing, cacheable list results, auth hardening); licence MIT (spec + official Python SDK); Windows+Python: yes — official `modelcontextprotocol/python-sdk`, requires Python 3.10+, ships `pywin32` as a Windows-only dependency for stdio subprocess management, i.e. Windows is a first-class target, not an afterthought
- **JSON-RPC (2.0)** | vetting: maintained — the spec itself is a finished, stable 2010 document (not versioned like a software product, so "latest release + date" does not apply in the normal sense — UNVERIFIED in that specific sense); licence: the spec text carries no explicit licence marker on jsonrpc.org; multiple independent Python implementations exist (`json-rpc`, `jsonrpclib`, `python-jsonrpc-server`), each separately MIT/BSD-licensed; Windows+Python: yes, several pure-Python implementations install and run on Windows with no native deps
- **Discord** | vetting: maintained yes (actively developed consumer/business SaaS platform, no meaningful "end of life" risk); licence: the Discord service itself is proprietary/closed; the Python client library `discord.py` is MIT-licensed; Windows+Python: yes, `py -3 -m pip install -U discord.py` works on Windows, requires Python 3.8+
- **RTK** ("Rust Token Killer") | vetting: maintained yes, very active (rolling pre-release channel, e.g. `dev-0.50.0-rc.450` dated 2026-09-21 — no single "stable" tag surfaced, so exact stable version/date is UNVERIFIED beyond "actively shipping same-day builds"); licence Apache-2.0; Windows+Python: PARTIAL — native Windows support confirmed (winget install, native binary hook since v0.37.2) but it is a standalone Rust binary, not a Python package — usable *alongside* Python tooling, not *via* Python
- **Headroom** | vetting: maintained yes (2026 releases, active blog/docs); licence Apache-2.0 ("see LICENSE" in repo); Windows+Python: yes — installable via `pip install "headroom-ai[all]"`, ships a CLI, publishes prebuilt Windows wheels (`win_amd64`) so no Rust toolchain is needed on Windows
- **Caveman** | vetting: maintained yes (active repo, 2026 posts/guides); licence split — skill/adoption surfaces MIT, the engine-linked runtime under BSL-1.1 (Business Source License, converting to Apache-2.0 by 2030-06-21 or 4 years after each version ships, whichever is earlier) — note this BSL clause before adopting the runtime half; Windows+Python: yes, PowerShell-based installer documented for Windows, and a `caveman-middleware` Python package exists on PyPI alongside the npm CLI
