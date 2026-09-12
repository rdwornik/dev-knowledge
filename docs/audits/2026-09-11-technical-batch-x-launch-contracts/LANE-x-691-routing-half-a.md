# LANE lane-x-691-routing-half-a — X1-4 Half A: the routing mechanism, Claude-only - telemetry, registry, router and re-rank built and trip-tested with no non-Claude provider ordered

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-691-routing-half-a LANE-x-691-routing-half-a.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #691 · lane-x-691-routing-half-a]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-691-routing-half-a` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The fence above is written in the grammar the contract gate admits, which has no `-Model` alternative (`gen_lane_contract.py:227`). The model is therefore made explicit when the lane is fired:

```
Dispatch-Lane lane-x-691-routing-half-a LANE-x-691-routing-half-a.md -Effort high -Model opus
```

This lane ORCHESTRATES routing, so under AX21-1 it is **Opus only** — orchestration never routes to a cheaper tier, which is the one line of the role table that is not subject to re-ranking.

## Worktree pairing

slug `lane-x-691-routing-half-a` -> branch `worktree-lane-x-691-routing-half-a` -> contract `LANE-x-691-routing-half-a.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. `provider-registry.yaml` encodes, per ROLE, an ORDERED fallback list; the **reviewer ≠ producer** exclusion (AX22-2 — Codex terra reviews unless Codex produced, then Grok after admission or Sonnet); and a per-repo `providers.allowed` allowlist carried in the deploy manifest. The router **REFUSES** a provider not on the repo's list and **REFUSES** a non-admitted provider in the implement role — a RED-first trip-test for each refusal.
2. Every call records **model, tokens, cost and outcome** (tests green? review HIGH-free?) in the tally, and the router **re-ranks by measured pass rate per cost** — not by a list typed into a file. Admission is **≥ 8 of 10 tasks green on first review** (AX22-1); below it the provider ranks LAST and the log-review routine files the anomaly as a row. The expected steady state is Copilot → Grok → Sonnet, but it is **earned, not declared** — until admission the implement order is **Sonnet first**.
3. **The Half A / Half B boundary (AX23-2), and it is the clause that scopes this lane.**
   Everything above is built, trip-tested and committed with **no non-Claude provider
   ordered**. The registry MAY list `agy`, Grok 4.6, Copilot Enterprise and Codex terra as
   entries whose admission state is recorded **NOT ADMITTED**, and the router's two refusals
   are trip-tested against exactly those entries — that is what makes Half B safe to run
   later. This lane places **no call** to any of them. Admission itself — the bounded trial
   tasks and the ≥ 8-of-10 measurement — is **Half B**, a separate lane ordered after this
   one under AX23-1's stdout-and-verify shape.
4. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md`, as amended by `AMEND-BATCH-X-ROSTER-021.md` and `-022.md` (Fable's five corrections). This lane's FIRST COMMIT writes these clauses into its own rows.


### Row `[#691]` — Done-when, verbatim

> Done when: carried verbatim from `to-cc/AMEND-BATCH-W-004.md` AW4-1 row 2 — "`provider-registry.yaml` gains a role entry with an ORDERED fallback list; only providers that passed intake #75's seeded-defect admission bar, and whose licence permits the use, may appear on it; the review tally records which model actually answered. RED-first test: listing a non-admitted provider fails."


### Row `[#694]` — Done-when, verbatim

> Done when: modules wired or deleted; dispatch refuses without the GO file, trip-tested · **plus AX9-5's metric clause**: raw-search calls vs organ calls per session, and organs never called in 30 days, both emitted by the surviving telemetry


### `AX21-1` — verbatim

> - **AX21-1 · Role→model table (routing X1-4 + prompt distiller `[#617]`):** orchestrate / plan → Opus only · implement → Copilot Enterprise (bounded, small) → **Grok 4.6** (multi-step, long-horizon; `--max-turns`; reasoning `high`, `xhigh` for hard tasks) → Sonnet · review before merge → Codex terra, never the producing provider · read / scan → agy → Copilot Enterprise → Sonnet (locator + verbatim; CC verifies) · verify → Sonnet + the lane's RED-first tests.


### `AX21-2` — verbatim

> - **AX21-2 · Self-optimising order, not a fixed list:** every call records model, tokens, cost and outcome (tests green? review HIGH-free?) in the tally; `provider-registry.yaml` holds per-role ordered lists that the router re-ranks by measured pass rate per cost; the log-review routine (AX8-2) demotes a provider whose pass rate drops and files the anomaly as a row.


### `AX21-3` — verbatim

> - **AX21-3 · Admission by outcome for producers:** Grok 4.6 and Copilot Enterprise enter the implement role on verification — their output ships only through the lane's tests + a Codex review with no unresolved HIGH; the first ten tasks per provider are the measurement. R1-4(b)/A7-5 applies: a CLI that cannot enforce a token ceiling by flag is not ordered; CC verifies grok's flags before the first call.


### `AX21-4` — verbatim

> - **AX21-4 · Grok account:** X1-4's first act reads the usage-limit cause; if it is a spending cap, the operator raises it (his act, one line in the lane's report).


### `AX22-1` — verbatim

> - **AX22-1 · Admission before position.** Implement order until admission: Sonnet first; Grok 4.6 and Copilot Enterprise receive bounded trial tasks in parallel, each with the lane's RED-first tests and a review by a model that did not produce it. Admission threshold: ≥ 8 of 10 tasks green on first review; below it the provider ranks last and the log-review routine files the anomaly. After admission the router re-ranks by measured pass rate per cost (AX21-2); the expected steady state is Copilot → Grok → Sonnet on quota logic, but it is earned, not declared.


### `AX22-2` — verbatim

> - **AX22-2 · Reviewer ≠ producer, always.** Codex terra reviews unless Codex produced; then the reviewer is Grok (after admission) or Sonnet. The registry encodes the exclusion; the tally records both roles.


### `AX22-4` — WITHDRAWN by AX23-1, quoted so the withdrawal is legible

> - **AX22-4 · Precondition:** no non-Claude producer or reader is ordered before W-2′ (fail-closed guard) is on `main`; the routing lane's Done-when states it.

**This clause no longer binds.** W-2′ merged at `3a8ee7a8` and the precondition was then
measured to be the wrong gate rather than an unmet one — see AX23-1 below.


### `AX23-1` — verbatim

> - **AX23-1 · The guard was the wrong precondition — my planning error, corrected.** A `settings.json` PreToolUse hook governs only clients that read it (Claude Code; `cursor-agent` on the workstation). AX22-4 is withdrawn as a gate on non-Claude admission. Replacement: a non-Claude model is never given repo write access — it runs read-only or produces to stdout, and CC writes the artifact after verification (locators re-checked; produced code passes the lane's RED-first tests and a review by a model that did not produce it). `[#684]`'s undischarged smoke clause is re-scoped to the honour-set (`cursor-agent`) and a row is filed for a client-independent gate (pre-commit / CI), which is the only bar that can govern every provider.


### `AX23-2` — verbatim

> - **AX23-2 · X1-4 is ordered in two halves.** Half A (Claude-only, order now): telemetry wired → registry with roles, exclusions, per-repo allowlist → router → re-rank by measured pass rate per cost. Half B (non-Claude admission: agy, Grok 4.6, Copilot Enterprise on trial tasks) follows Half A under AX23-1's stdout-and-verify shape, not under a hook precondition.


### `AX22-5` — verbatim

> - **AX22-5 · Per-repo provider allowlist in the floor.** The deploy manifest carries `providers.allowed` per consumer; work repositories may exclude paid third-party APIs; the router refuses a provider not on the repo's list (RED-first). Order inside the routing lane: telemetry wired (AX5-1) → registry with roles, exclusions and allowlist → router → re-rank.


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


## The precondition is WITHDRAWN — and the reason matters more than the withdrawal

The frozen full-scope contract gated the non-Claude half on W-2′ reaching `main`. W-2′ **did**
reach `main` (`3a8ee7a8`, *"the prompts guard FAILS CLOSED"*, 312 passed). The gate was then
withdrawn anyway, because it was measured to be **the wrong gate**, not an unmet one:

**A `.claude/settings.json` PreToolUse hook governs only the clients that read that file.** The
honour-set on this workstation is Claude Code and `cursor-agent`. **Codex and Copilot never read
it at all** — so the guard could not have governed the two providers the admission half exists
to admit, and a smoke test from either would have been vacuous. Admission never depended on it.

**The replacement is a posture, not a hook, and it is Half B's frame — not this lane's work:**
a non-Claude model is never given repo write access. It runs read-only or produces to **stdout**;
**CC** writes the artifact after re-verifying every locator; produced code passes the lane's
RED-first tests **and** a review by a model that did not produce it. A client-independent gate
(pre-commit / CI) is filed as its own row, because that is the only bar that can bind every
provider regardless of which config file it honours.

**What this means for THIS lane: nothing is gated, and nothing non-Claude is ordered.** Half A
is Claude-only by scope, not by precondition. If this lane finds itself wanting to place a
non-Claude call to finish a step, that is the signal it has crossed into Half B — it **reports
and stops**, per the refuted-premise rule in the decision budget.

## Order of work INSIDE this lane — fixed by AX22-5, not the lane's choice

```
1  telemetry wired (AX5-1)
2  registry: roles + ordered lists + reviewer-not-producer exclusion + providers.allowed
3  router: refuses an off-list provider, refuses a non-admitted producer
4  re-rank by measured pass rate per cost
```

Built in that order because each step is the previous one's evidence: a router re-ranked on
nothing measured is a fixed list wearing a router's name, which is the exact failure AX21-2
names.

## The two FIRST ACTS move to Half B — do NOT run them here

The full-scope contract opened with two acts: read the grok account's usage-limit cause
(AX21-4), and verify grok's token-ceiling flag (AX21-3 / R1-4(b) / A7-5). **Both are
Grok-specific admission gates, so both belong to Half B** and are recorded here only so Half B
inherits them rather than rediscovering them. Running them in this lane would be the first
non-Claude call in a lane defined by placing none.


## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Step 0 sync (below). **COMMIT** if the sync produces one.
2. Telemetry wired (AX5-1): model, tokens, cost and outcome recorded per call. RED-first. **COMMIT**
3. Registry: roles, ordered fallback lists, the reviewer ≠ producer exclusion, and the per-repo `providers.allowed` allowlist in the deploy manifest. RED-first: listing a non-admitted provider fails. **COMMIT**
4. Router: refuses an off-list provider, refuses a non-admitted producer in the implement role. RED-first per refusal. **COMMIT**
5. Re-rank by measured pass rate per cost, over the telemetry from step 2. Report each provider's recorded admission state — for every non-Claude entry that state is **NOT ADMITTED**, and reporting it is not the same act as measuring it. **COMMIT**
6. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- **No call to any non-Claude provider — no `agy`, no Grok 4.6, no Copilot Enterprise, no
  Codex terra — as producer, reader or reviewer.** This is the single exclusion that defines
  Half A. Listing them in the registry as NOT ADMITTED entries, and trip-testing the router's
  refusals against them, is required work and is not a call.
- No admission measurement. The bounded trial tasks and the ≥ 8-of-10 threshold are Half B's.

## Step 0 — sync before anything else (MANDATORY until `[#716]` lands)

`[#716]` is open: `worktree.baseRef` is unset, so this lane branches from `origin/main` and
may start behind local `main`. Wave 1's six lanes landed on **three different bases** for
exactly this reason. The sync is mandatory and is retired only by the change that makes
`[#716]`'s test green.

```
git fetch origin
git merge main
```
