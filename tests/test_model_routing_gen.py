"""RED witnesses: `render_contract` emits the Roles table (`| Phase | Model | Where |`) from the
registry, so a registry edit moves the emitted contract and no literal model id is held here.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parents[1]
for _p in (_ROOT, _ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import gen_lane_contract as glc  # noqa: E402
import provider_registry as pr  # noqa: E402
import subst_gate as sg  # noqa: E402

_LIVE = _ROOT / "ecosystem" / "provider-registry.yaml"


def _spec(**over) -> glc.LaneSpec:
    return glc.LaneSpec(slug="lane-a-539-roles-table", purpose="a roles table", kind="code", task_id="539",
                        **over)


def _rows(text: str) -> list[list[str]]:
    lines = text.splitlines()
    head = next((i for i, ln in enumerate(lines)
                 if [c.strip().lower() for c in ln.strip().strip("|").split("|")] == ["phase", "model", "where"]),
                None)
    assert head is not None, "no `| Phase | Model | Where |` Roles table emitted"
    out = []
    for ln in lines[head + 2:]:
        if not ln.strip().startswith("|"):
            break
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


def _row(rows, needle: str) -> str:
    hits = [" | ".join(r) for r in rows if needle in r[0].lower()]
    assert hits, f"no Roles row for {needle!r}: {rows}"
    return "\n".join(hits)


def _reg_model(role: str, provider: str | None = None, index: int = 0) -> str:
    order = pr.role_order(role)
    entries = [e for e in order if provider is None or e["provider"] == provider]
    return entries[index]["model"]


def test_the_roles_table_is_derived_from_the_registry():
    rows = _rows(glc.render_contract(_spec()))
    implement = _row(rows, "implement")
    assert "Copilot" in implement and next(iter(pr.copilot_gateway_served())) in implement
    assert _reg_model("seat-orchestrator") in _row(rows, "lane head")
    assert "Copilot" in _row(rows, "red")
    review = _row(rows, "review")
    assert _reg_model("review", index=0) in review and "Copilot" in review
    assert _reg_model("verify") in _row(rows, "verify")


def test_the_emitted_contract_passes_the_pre_launch_gate():
    text = glc.render_contract(_spec(model="sonnet"))   # the seat-orchestrator tier alias
    _rows(text)
    problems, _ = sg.contract_problems(text, lane="lane-a-539-roles-table", batch="E2.0")
    assert problems == []


@pytest.fixture()
def swapped_registry(tmp_path, monkeypatch):
    data = yaml.safe_load(_LIVE.read_text(encoding="utf-8"))
    assert "seat-orchestrator" in data["roles"], "registry has no `seat-orchestrator` role yet"
    original = data["roles"]["seat-orchestrator"]["order"][0]["model"]
    other = next(m for m, f in data["models"].items()
                 if f.get("provider") == "anthropic" and m != original and "opus" in m)
    data["roles"]["seat-orchestrator"]["order"][0]["model"] = other
    path = tmp_path / "provider-registry.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    for name in ("provider_registry", "scripts.provider_registry"):
        try:
            mod = importlib.import_module(name)
        except ImportError:
            continue
        monkeypatch.setattr(mod, "DEFAULT_REGISTRY_PATH", path)
    return original, other


def test_the_lane_head_row_follows_the_registry_not_a_literal(swapped_registry):
    original, other = swapped_registry
    head = _row(_rows(glc.render_contract(_spec())), "lane head")
    assert other in head and original not in head, (
        "the lane head row must be read from the registry `seat-orchestrator` role")
