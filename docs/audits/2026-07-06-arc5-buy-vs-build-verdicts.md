# Arc 5 — Buy-vs-build verdicts (intake doc #2 AC2 + AC4)

**Date:** 2026-07-06 · **Basis:** the six SHOULD pilots below + the MUST sweep (`2026-07-06-arc5-must-verification.md`) · **Authority:** verdicts name what we RETIRE; per doc #2 §5 **no doctrine changes ride this doc** — pilots produce evidence, the architect produces doctrine. Immutable audit record; verdict-writing ran judgment-flagged (Fable window per the epic header).

## AC2 — pilot ledger (one bounded pilot per SHOULD; ex-ante metric vs outcome)

| Pilot | Ex-ante metric (frozen at plan approval) | Outcome | Follow-up |
|---|---|---|---|
| P1 Routines (plan-only, #270-gated) | Design doc passes architect review with all 7 routine-standard points + rent + intact #270 gate; zero night executions | Design doc shipped (`9fe7605`); zero night executions; architect review lands at the read-back | #271 consumes the frozen contract when #270 is IN EFFECT |
| P2 Outcomes | ≥80% criterion agreement + ≥1 real gap vs the architect's #268 UAT walk, heterogeneous grader (ruled D3) | **Availability check FAILED first** — Outcomes is Agent Platform (Managed Agents), not CC CLI; `outcome-grader` absent from the 2.1.202 binary. Absence branch taken: reject-with-why; the ruled pilot design (rubric = done-contract verbatim · ground truth = architect's recorded UAT walk · grader NOT the lane's model, Codex-heterogeneity doctrine) is **pre-registered** here for when the feature reaches our surface | WATCH item (intake follow-up); pilot design frozen above, do not re-derive |
| P3 /batch | Clauses (a) file boundaries (b) commit-and-STOP (c) root-only merge all hold in a contained sandbox | **All three HELD, independently verified** (not lane self-report): per-lane diffs = exactly the granted file; sandbox main untouched at `55cd120` (0 first-parent commits); bare origin still `refs/heads/main` only; branches left mergeable; pre-commit gates ran INSIDE lanes. Bonus witnesses: worktree isolation matches the ADR-97 model; headless `-p "/batch <args>"` works (arg-less hangs); headless lanes invisible in `claude agents`; lane worktrees persist until root merges (leftover burden on root) | Verdict 2; a real-scale (epic-sized) n=2 pilot is the named next gate |
| P4 Ultraplan (draft-only, #213 ruled D4) | Draft covers ≥ the §14a plan-review surfaces; architect judges, lane records | **Could not execute:** `/ultraplan isn't available in this environment` (2.1.202 headless; surface present in binary + docs, needs an environment we didn't have — likely interactive + CC-on-web linkage). Reject-for-now; comparison question stays open | WATCH; one attended interactive attempt by the operator would settle availability cheaply |
| P5 /goal | Terminates by condition-satisfaction (fresh command output, never self-asserted) within ≤5 turns, zero edits to tests/condition | **MET, independently verified:** ruff exit 0; `git diff main -- tests/` empty; tree clean (fix restored the file byte-identical to HEAD). Notable behavior: refused to fabricate an `--allow-empty` "fix" commit — execution-truthfulness held under goal pressure | Evidence recorded against **#126** (backpressure-loop evaluation) — no new item |
| P6 Artifacts | Rendered page has row/count parity with `logs/FLEET-HEALTH.md`; legible both themes; operator usability call stays the operator's | **MET on the mechanical legs:** private Artifact published (fleet-health digest, 2 tables + KPI row, token-based light/dark, self-contained CSP-clean); parity verbatim from source. **Operator usability verdict: OPEN — the operator rules at review** (link in the EPIC RETURN) | Verdict 4; #264 recommendation below |

## AC4 — the four overlap verdicts (each names the RETIRE)

### 1. Routines vs our nightly harness — HYBRID (buy the LLM-night class; keep the deterministic Tier-2 layer)

The premise "replace a fragile Task-Scheduler harness" is half-stale: the LLM-night class is ALREADY bought (#86 nightly conformance Routine, n≥2, envelope-disciplined) — the 07-06 correction stands. What remains local is the **deterministic Tier-2 layer** (`fleet_health.py` under Task Scheduler, ADR-76), and that is doctrine-bound (ADR-76/80: no LLM on the deterministic path), not rot — Routines are the wrong instrument for it.
**RETIRE if the second routine lands (post-#270, n=2):** the *attended* serial-suite timing runs (an operator practice — ~10 min/run witnessed 2026-07-06) and any temptation to build a local timing-trend harness; the cloud digest series replaces both. **Explicitly NOT retired:** Task Scheduler + `fleet_health.py` (different tier, doctrine-bound), the #86 envelope (it is the carrier).
**Honest limit:** cloud timing series ≠ Windows-local latency oracle; the trend is runner-class-relative.

### 2. /batch vs ADR-97 hand-provisioned mechanics — ADOPT-CANDIDATE (governance-compatible on n=1 toy evidence; scale gate before doctrine)

The make-or-break question — can /batch run UNDER our governance — answered YES on first evidence: it respected prompt-stated file boundaries, stopped at commit, imposed no PR flow, left root the `--no-ff` merge, and its lanes ran our pre-commit gates. It operationalizes the ADR-97 *mechanics* (worktree isolation, decomposition) without displacing the ADR-97 *governance* (grants, root-only merge, §14a contracts) — which is exactly the buy we want.
**RETIRE if adopted at scale:** the hand-provisioning choreography — manual `claude --worktree` lane spawning, the per-lane state.yaml seeding ritual (the n=3 gotcha), per-lane branch setup. **NOT retired:** ADR-97 itself, EPIC_BOOT contracts, root merge authority — /batch runs under them.
**Honest limits (all load-bearing):** n=1 at TOY scale (two one-file lanes ≠ epic-scale boundary pressure); the surface is **undocumented officially** (in-binary only — schema/behavior may drift with zero notice; the changelog-review sentinel must watch it); headless lanes don't appear in the `claude agents` cockpit (observability gap vs our orphan-process lesson); lane worktrees persist as root-owned leftovers (No-leftovers §5#9 burden shifts to root); the sandbox ran `--dangerously-skip-permissions` — permission-interaction under our deny-first floor is UNTESTED (deliberately, to observe native flow; the real-scale pilot must run under real permissions).
**Named next gate:** one real epic-scale pilot (n=2) under real permissions before any PLAYBOOK Ch8 change.

### 3. Outcomes vs manual EPIC-RETURN review — KEEP-OURS + WATCH (the feature is not on our surface)

Nothing to buy today: Outcomes is Agent Platform, not Claude Code CLI (docs + binary witness). The manual RETURN review with Codex-heterogeneity stays the mechanism.
**RETIRE (conditional, pre-registered):** IF Outcomes reaches CC and the pre-registered pilot (P2 row above, D3-ruled parameters) meets its ≥80%+≥1-gap metric, the RETIRE is the **manual first-pass RETURN triage** — the architect's final ratification is never in scope for retirement.
**Honest limit:** the WATCH must be active, not passive — the changelog-review feed (R1, live) is the sensor; a "CC gains Outcomes" line routes to intake automatically.

### 4. Artifacts vs #264 (mermaid_emit wiring) — ADOPT-CANDIDATE as the Tier-4 surface; RECOMMEND unparking #264 re-scoped (architect rules)

The pilot settled the surface question #264 was parked on: a live, default-private, theme-aware page rendered from repo data in one session, zero deps, CSP-self-contained — that IS the "human-facing visualization surface" ADR-59/ADR-51-amendment deferred. Plain HTML sufficed; no Mermaid was needed for the tabular/status class of content.
**RECOMMENDATION (not an unparking — the architect rules):** unpark #264 **re-scoped** — the visualization surface = Artifacts pages; `mermaid_emit.py` wiring becomes "emit → embed in an Artifact page" for genuinely graph-shaped content (the ADR-51 diagram-class rule), and for tabular content it is not needed at all.
**RETIRE if adopted:** the undecided "stored-outside-canonical visualization surface" build (#264's original on-demand-vs-stored fork — Artifacts answers it: on-demand, hosted, private-by-default); potentially `mermaid_emit.py` itself if the architect rules the graph class also goes native-HTML — that removal is safe-removal-gated (#24 check) and operator-gated (never a lane call).
**Honest limits:** publishing sends repo-derived content to claude.ai hosting (default-private, org-scoped share) — a data-classification call per surface remains the operator's; parity was hand-verified this run, a repeatable parity check would be needed if this becomes a standing surface.

## A1 economics record (ruled: record here)

Sonnet-5 promo pricing ($2/$10 per Mtok) runs through **Aug 31, 2026** — the real deadline that made A1 timely. Pins refreshed 2026-07-06 (`608eed6`, `399c843`); the verified model string is `claude-sonnet-5` (live-tested, Amendment A). Re-evaluate the XL/Fable tier on any pricing change per the ADR-70 amendment's own condition.

## Cross-cutting observations (for the architect, no action taken)

- The headless `-p "/slash"` path: works WITH arguments (/batch, /goal), hangs bare, and some surfaces refuse the environment entirely (/ultraplan) — unattended automation on native surfaces needs per-surface probing, never assumption.
- The untrusted-workspace warning (sandbox `permissions.allow` ignored) is a quiet portability gotcha for any future sandbox that RELIES on allow-rules: trust must be granted per-workspace or the allowlist silently drops (`hasTrustDialogAccepted`).
- Amendment C witnessed live: Arc 4's deploy session runs against the hub primary (`claude agents` cockpit) — the serialized-integration ruling, not disjointness, is what prevents collision.
