## Phases

```yaml
phases:
  - id: P1
    name: spec
    row_phase: build
    role: plan
    cli: uv
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 120
    budget_usd: 0
    max_rounds: 2
    inputs: []
    command: [uv, run, --locked, python, tests/fixtures/stub_phase.py, "{payload}", "{nonce}", "{input_hash}"]
  - id: P2
    name: red
    row_phase: build
    role: red
    cli: uv
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 120
    budget_usd: 0
    max_rounds: 2
    inputs: []
    command: [uv, run, --locked, python, tests/fixtures/stub_phase.py, "{payload}", "{nonce}", "{input_hash}"]
    fallback: [claude, -p, --output-format, json, "Write a phase payload to {payload} with nonce {nonce} and input hash {input_hash}"]
  - id: P3
    name: implement
    row_phase: build
    role: implement
    cli: uv
    model: null
    payload_model: PhasePayload
    gate: payload
    timeout_s: 120
    budget_usd: 0
    max_rounds: 2
    inputs: []
    command: [uv, run, --locked, python, tests/fixtures/stub_phase.py, "{payload}", "{nonce}", "{input_hash}"]
```
