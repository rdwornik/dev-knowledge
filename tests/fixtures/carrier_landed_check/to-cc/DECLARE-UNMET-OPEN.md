carried-by: OPEN
lands-via: docs/decisions/ADR-999-never-lands.md, once ratified

## Fixture

A decision file honestly still open: its named landing home does not resolve on `main`
(per the test's monkeypatched `_resolves_on_main`). `carrier_landed_check.py` must count
it as measured but must not flag it -- the debt is real, but it is not THIS organ's debt to
name (it belongs in the contract's RESIDUAL-CARRIERS block instead).
