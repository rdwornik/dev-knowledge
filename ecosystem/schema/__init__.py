"""ecosystem/schema/ — the declared contracts for this repo's ecosystem-state files (pydantic).

Models only; loaders live in scripts/ (Layer-2: read-only validators). Directory authorized
per ADR-109 §8 (F2, operator via architect, 2026-07-31).

Three contracts live here:

* `desired_state` — the ADR-109 fleet desired-state contract v1 ([#382] W2).
* `provider_registry` — the `ecosystem/provider-registry.yaml` contract (LANE L1, 2026-08-23),
  loaded by `scripts/provider_registry.py`.
* `lane_report` — the section-3 LANE REPORT ([#1368], batch BW), with its generated JSON Schema
  `lane-report.schema.json`; read by `scripts/lane_digest.py --manifest` and `scripts/dispatch.py`.
  Not re-exported below: its consumers import it by module, lazily.
"""

from ecosystem.schema.desired_state import SCHEMA_VERSION, FleetDesiredState
from ecosystem.schema.provider_registry import ProviderRegistry

__all__ = ["SCHEMA_VERSION", "FleetDesiredState", "ProviderRegistry"]
