---
name: spine
description: Run the harness spine (stage table in ecosystem/harness.yaml) for a change kind and subject, stopping at the first missing stage.
---

# /spine — the build-list stage run

Arguments: `<kind> <subject>`. Run from the repo root:

```
HARNESS_KIND=<kind> HARNESS_SUBJECT=<subject> uv run --locked doit -f scripts/dodo.py spine
```

(PowerShell: `$env:HARNESS_KIND="<kind>"; $env:HARNESS_SUBJECT="<subject>"; uv run --locked doit -f scripts/dodo.py spine`.)

doit halts at the first failing stage; a stage with no command fails on purpose. It prepares a
contract and moves no row through phases. Stage table and semantics: `scripts/dodo.py`.
