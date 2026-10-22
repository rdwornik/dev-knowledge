"""RED tests: the adversarial role pin moves to `gpt-6-sol` in the routing table and registry."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import check_provider_registry as cpr  # noqa: E402
import provider_registry as preg  # noqa: E402
from test_provider_registry import _break, tree  # noqa: F401,E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_ROUTING = _REPO_ROOT / "ecosystem" / "routing-table.yaml"
_RULINGS = "ecosystem/satellite-onboarding-rulings.yaml"


def _roles() -> dict:
    return yaml.safe_load(_ROUTING.read_text(encoding="utf-8"))["roles"]


@pytest.mark.live_repo
def test_adversarial_role_pins_gpt_6_sol():
    assert _roles()["adversarial"]["model"] == "gpt-6-sol"


@pytest.mark.live_repo
def test_gpt_6_sol_is_registered_like_its_sibling():
    models = preg.models()
    assert "gpt-6-sol" in models
    assert models["gpt-6-sol"]["provider"] == "openai"
    assert "roles" in models["gpt-6-sol"]
    assert set(models["gpt-5.6-sol"]) <= set(models["gpt-6-sol"]) | {"attribution_token", "pinned_at"}
    preg.load_registry()
    assert _roles()["adversarial"]["model"] in models


@pytest.mark.live_repo
def test_checker_is_clean_live_and_still_has_teeth(tree):  # noqa: F811
    assert cpr.run(_REPO_ROOT) == []
    _break(tree, _RULINGS, "(gpt-5.6-sol)", "(gpt-0-bogus)")
    assert cpr.run(tree)


@pytest.mark.live_repo
def test_no_role_row_still_pins_gpt_5_6_sol():
    offenders = [name for name, row in _roles().items()
                 if isinstance(row, dict) and row.get("model") == "gpt-5.6-sol"]
    assert offenders == []
