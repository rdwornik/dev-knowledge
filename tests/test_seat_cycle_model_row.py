import pytest

import provider_registry
import seat_cycle as sc


@pytest.mark.parametrize(
    ("role", "registry_role"),
    [
        ("orchestrator", "seat-dispatcher"),
        ("integrator", "seat-integrator"),
    ],
)
def test_successor_model_uses_successor_role_row(role, registry_role):
    assert sc.successor_model(role) == provider_registry.anthropic_role_model(registry_role)
