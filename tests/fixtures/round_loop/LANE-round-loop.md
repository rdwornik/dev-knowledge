# LANE round-loop — round-loop fixture contract (tests only; never launched)

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

- **Row:** [#1856]

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

**Kind:** `code` — changes executable code — `scripts/`, `tests/`, hooks, schema, generators.

The kind is DECLARED, not inferred, and it is what the routing default keys on
(`[#885]` clause 2). A code lane plans on Opus and implements on Sonnet **as two sessions
with a file between them**, never as one session changing tier mid-flight, because the
prompt cache is keyed PER MODEL.

```
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree round-loop "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-round-loop.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-round-loop.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`. The launcher reads this `## Dispatch` block for its
fields and builds the session's own argv; it never runs the block. This file is a test
fixture for the round loop and is never dispatched.

## Roles

| Phase | Model | Where |
|---|---|---|
| implement | claude-sonnet-5-5 | codespace |
| lane head | claude-sonnet-5-5 | local |
| RED tests | **Copilot CLI** `gpt-6-luna` | codespace |
| review | gpt-5.6-terra + **Copilot CLI** (default model) | local + codespace |
| isolated verify | claude-sonnet-5-5 | local |

## Worktree pairing

slug `round-loop` -> branch `worktree-round-loop` -> contract `LANE-round-loop.md`

One lane = one contract file = one branch (ADR-110, fifth per-lane requirement). The
`worktree-` prefix is applied exactly ONCE — the flag takes the bare lane name.

## Done-contract (immutable)

1. `<what [#1856] delivers — checkable, not aspirational>`
2. `<the second done-when, or delete this line>`
3. Docs and code in English; hyphen-only names; logging rather than print;
   `pytest` green.
4. **Close-out:** the review record carries the served model id from the tool's
   own log and the nonce or content hash the reviewer returned (R59).

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

## Steps

1. `<imperative — what is done>` **COMMIT**
2. `<imperative>` **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once at the merge.
- No edits outside this lane's declared footprint.

## Phases
```yaml
phases:
  - id: P1
    name: plan
    row_phase: build
    role: plan
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P1"]
  - id: P2
    name: red
    row_phase: build
    role: red
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P2"]
  - id: P3
    name: implement
    row_phase: build
    role: implement
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P3"]
  - id: P4
    name: constraints
    row_phase: build
    role: constraints
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P4"]
  - id: P5
    name: review
    row_phase: build
    role: review
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P5"]
  - id: P7
    name: judge
    row_phase: build
    role: judge
    cli: python
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 30
    budget_usd: 0
    max_rounds: 2
    inputs: ["{contract}"]
    command: ["__PYTHON__", "__TOY_PHASE__", "P7"]
```
