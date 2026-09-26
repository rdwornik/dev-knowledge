carried-by: OPEN
lands-via: docs/decisions/ADR-900-fixture.md, once the lane merges it

## Fixture

A decision file whose stated landing home now exists on `main` (per the test's
monkeypatched `_resolves_on_main`), while its `carried-by:` header was never updated away
from `OPEN`. This is the exact debt `carrier_landed_check.py` exists to flag.
