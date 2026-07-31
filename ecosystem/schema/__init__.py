"""ecosystem/schema/ — the ADR-109 fleet desired-state contract (pydantic, v1).

Models only; the loader lives in scripts/ (Layer-2: read-only validators). New
directory authorized per ADR-109 §8 (F2, operator via architect, 2026-07-31).
"""

from ecosystem.schema.desired_state import SCHEMA_VERSION, FleetDesiredState

__all__ = ["SCHEMA_VERSION", "FleetDesiredState"]
