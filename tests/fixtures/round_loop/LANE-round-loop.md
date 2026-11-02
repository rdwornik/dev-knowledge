# LANE round-loop

## Lane entry

- **Row:** [#1856]

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
