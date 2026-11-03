# LANE round-loop-dispatch-fixture

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5-5 | execute | high |

- **Row:** [#4243]

## Dispatch

**Engine:** conductor

```
claude --bg -n round-loop-dispatch-fixture --model claude-sonnet-5-5 --effort high --permission-mode bypassPermissions --worktree round-loop-dispatch-fixture "Read and execute the frozen contract at LANE-round-loop-dispatch-fixture.md"
```

## Phases

```yaml
phases:
  - id: implement
    name: implement
    row_phase: build
    role: implement
    cli: uv
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 120
    budget_usd: 0
    max_rounds: 1
    inputs: []
    command: [echo, fixture]
```
