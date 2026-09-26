carried-by: OPEN
lands-via: the next landing under docs/audits/

## Fixture

The false-positive class measured live on 2026-09-26: a bare directory
(`docs/audits/`) that resolves on `main` in every commit this repo has ever made, so
resolving it proves nothing about whether THIS ruling landed. `carrier_landed_check.py`
must never flag a lands-via whose only candidate is directory-shaped.
