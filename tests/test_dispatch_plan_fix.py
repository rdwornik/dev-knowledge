"""B2-W4 lane `dispatch-plan-fix` (DIGEST-TOOLS-IN-USE-2026-10-11): `dispatch.py plan`.

Two defects, one witness each:
  1. the module docstring said "`--token-cap` is optional" while `plan --help` says "REQUIRED here"
     and `plan` exits 2 without it -- the docs must say what the code enforces;
  2. `plan --slug X` against a contract whose Dispatch block names `-n`/`--worktree` Y silently
     planned lane X -- a disagreement must be REFUSED, never quietly resolved.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dispatch as d  # noqa: E402

CONTRACT = """# LANE lane-real -- a test contract

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

```
claude --bg -n lane-real --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-real "Read and execute the frozen contract"
```
"""


def _plan(path: Path, *extra: str):
    return CliRunner().invoke(d.cli, ["plan", str(path), "--token-cap", "1000", *extra])


@pytest.fixture
def contract(tmp_path):
    path = tmp_path / "LANE-file-name.md"
    path.write_text(CONTRACT, encoding="utf-8")
    return path


# --- 1. --token-cap: docstring == help == code ---------------------------------------------------

def _token_cap_sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [s for s in re.split(r"(?<=[.;])\s+", flat) if "--token-cap" in s]


def test_plan_enforces_the_token_cap_as_required():
    option = next(p for p in d.plan_cmd.params if p.name == "token_cap")
    assert option.required is True
    assert "REQUIRED" in (option.help or "")


def test_the_module_docstring_agrees_that_plan_requires_the_token_cap():
    sentences = _token_cap_sentences(d.__doc__ or "")
    assert sentences, "the module docstring must document --token-cap"
    assert not any(re.search(r"`--token-cap` is optional\.", s) for s in sentences), sentences
    assert any("plan" in s and "REQUIRED" in s for s in sentences), sentences


def test_plan_without_a_token_cap_exits_2(contract):
    result = CliRunner().invoke(d.cli, ["plan", str(contract)])
    assert result.exit_code == 2 and "token-cap" in result.output.lower()


# --- 2. --slug never silently replaces the contract's -n / --worktree -----------------------------

def test_a_slug_that_disagrees_with_the_dispatch_block_is_refused(contract, monkeypatch):
    monkeypatch.setattr(d, "_git_branch_exists", lambda ref: False)
    result = _plan(contract, "--slug", "lane-other")
    assert result.exit_code != 0
    assert "lane-other" in result.output and "lane-real" in result.output
    assert "{" not in result.output, "a refusal prints no plan"


def test_a_slug_that_agrees_with_the_dispatch_block_is_planned(contract, monkeypatch):
    monkeypatch.setattr(d, "_git_branch_exists", lambda ref: False)
    result = _plan(contract, "--slug", "lane-real")
    assert result.exit_code == 0, result.output
    assert '"slug": "lane-real"' in result.output


def test_plan_defaults_the_slug_to_the_dispatch_block_not_the_file_name(contract, monkeypatch):
    monkeypatch.setattr(d, "_git_branch_exists", lambda ref: False)
    result = _plan(contract)
    assert result.exit_code == 0, result.output
    assert '"slug": "lane-real"' in result.output


def test_launch_refuses_a_disagreeing_slug_too(contract):
    with pytest.raises(d.DispatchRefused, match="lane-other"):
        d.request_from_contract(contract, slug="lane-other")
