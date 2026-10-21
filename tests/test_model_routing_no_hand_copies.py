"""RED witnesses: the alias tables and the reviewer row hold no hand copy of a registry model id.

The registry is the one source; `MODEL_ALIASES` / `_ALIAS_EXPLICIT_ID` are derived from it and
`routing-table.yaml`'s reviewer row carries no `model:` (the `review` role is the source).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parents[1]
for _p in (_ROOT, _ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import dispatch  # noqa: E402
import gen_lane_contract as glc  # noqa: E402
import plan_lint  # noqa: E402

_REG = yaml.safe_load((_ROOT / "ecosystem" / "provider-registry.yaml").read_text(encoding="utf-8"))
_TABLE = _ROOT / "ecosystem" / "routing-table.yaml"


def _role_model(role: str, provider: str = "anthropic") -> str:
    return next(e["model"] for e in _REG["roles"][role]["order"] if e["provider"] == provider)


def _expected() -> dict[str, str]:
    assert "seat-orchestrator" in _REG["roles"] and "seat-integrator" in _REG["roles"], (
        "registry lacks the seat roles the aliases derive from")
    return {"sonnet": _role_model("seat-orchestrator"), "opus": _role_model("seat-integrator"),
            "haiku": _role_model("read")}


def test_dispatch_aliases_follow_the_registry():
    exp = _expected()
    for alias, model in exp.items():
        assert dispatch.MODEL_ALIASES[alias] == model, f"{alias}: the registry role is the one source"
    combo = dispatch.MODEL_ALIASES["opusplan"]
    assert exp["opus"] in combo and exp["sonnet"] in combo


def test_plan_lint_aliases_follow_the_registry():
    exp = _expected()
    got = plan_lint._ALIAS_EXPLICIT_ID
    assert got["sonnet"] == exp["sonnet"] and got["opus"] == exp["opus"]
    assert got["opusplan"] == exp["opus"] and got["haiku"] == exp["haiku"]


@pytest.mark.parametrize("rel", ["scripts/dispatch.py", "scripts/plan_lint.py",
                                 "ecosystem/routing-table.yaml"])
def test_no_retired_literal_remains(rel):
    text = (_ROOT / rel).read_text(encoding="utf-8")
    for pattern in (r"claude-sonnet-5(?![\w.-])", r"gpt-6-astra"):
        hits = [m.start() for m in re.finditer(pattern, text)]
        assert not hits, f"{rel} still holds a hand copy matching {pattern!r} ({len(hits)}x)"


def test_routing_table_reviewer_row_has_no_model_key():
    table = yaml.safe_load(_TABLE.read_text(encoding="utf-8"))

    def find(node):
        if isinstance(node, dict):
            if "reviewer" in node and isinstance(node["reviewer"], dict):
                return node["reviewer"]
            for v in node.values():
                r = find(v)
                if r is not None:
                    return r
        return None

    row = find(table)
    assert row is not None, "no reviewer row"
    assert "model" not in row, "the registry `review` role is the one source of the reviewer model"


def test_reviewer_cli_is_still_codex():
    assert glc.reviewer_cli() == "codex"
