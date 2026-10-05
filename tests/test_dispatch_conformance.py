"""The generator<->launcher seam (AX25-2, `[#675]` clause 1), after win-tooling left the loop.

THE SEAM, and what moved. Two owners meet at a lane contract's `## Dispatch` fence: the writer,
`gen_lane_contract.py`, and the reader. The reader was win-tooling's `Invoke-Dispatch.ps1` and a
pre-commit hook, `dispatch-conformance`, probed it through a PowerShell on every commit. The
reader is now the hub's own `dispatch.py` (LANE-B2-W1-b2-dispatch-local-sole, ADR-127 D9), so the
probe needs no shell: this module renders a contract with the live generator and asks the real
reader -- `dispatch.request_from_contract`, and `dispatch.py launch --dry-run` end to end -- what
it resolves. The hook and `scripts/dispatch_conformance.py` are retired (R56 evidence in the lane's
review record); this is the standing witness, and it runs in CI on both OS legs.

THE FOUR PROPERTIES stay ONE assertion, as the clause worded them: four independently green checks
are how four symptoms (`[#716]` base, `[#717]` model, `[#718]` location, `[#740]` fence) co-existed
with a green suite. Each is a property of the one artifact that launches the lane:

  fence     the reader accepts the writer's fence (a `claude` head) and reads its fields
  location  the reader resolves the contract it is handed, and the prompt it builds names that
            resolved file -- no placeholder survives into the launched session's prompt
  model     the declared model reaches the launch argv (a line that drops it re-decides the most
            expensive constant on it)
  base      the lane lands on `worktree-<slug>`: `--worktree <slug>` is in the argv
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d
import gen_lane_contract as glc

_REPO = Path(__file__).resolve().parents[1]
_PLACEHOLDERS = ("<PROMPTS_DIR>", "$env:CLAUDE_PROMPTS_DIR", "%CLAUDE_PROMPTS_DIR%",
                 "${CLAUDE_PROMPTS_DIR}")
CONFORMANT = {"fence": True, "location": True, "model": True, "base": True}


def _render(out_dir: Path, *, slug: str, model: str, effort: str) -> Path:
    """One generator-emitted LOCAL contract, written to `out_dir` and returned.

    `kind="code"` and `needs_base_sync=False` are pinned: the probe measures the DISPATCH FIELDS,
    and the kind declaration and the step-0 region are prose that cannot change them (the latter
    would also make the result depend on the checkout the test ran in)."""
    spec = glc.LaneSpec(slug=slug, purpose="probe the generator<->launcher seam",
                        repo=".dev-knowledge", task_id=None, model=model, kind="code",
                        mode="execute", effort=effort, shape="local", strict_slug=False,
                        needs_base_sync=False)
    path = Path(out_dir) / glc.contract_filename(spec.validated().slug)
    path.write_text(glc.render_contract(spec), encoding="utf-8", newline="\n")
    return path


def properties(path: Path, *, slug: str, model: str) -> dict[str, bool]:
    """The four properties, read off what the REAL reader resolves from the contract."""
    try:
        request = d.request_from_contract(path)
    except d.DispatchRefused:
        return {"fence": False, "location": False, "model": False, "base": False}
    argv = request.argv
    return {
        "fence": request.provider == "anthropic" and request.slug == slug,
        "location": request.contract == path.resolve()
        and str(path.resolve()) in request.prompt
        and not any(p in request.prompt for p in _PLACEHOLDERS),
        "model": argv[argv.index("--model") + 1] == model if "--model" in argv else False,
        "base": argv[argv.index("--worktree") + 1] == slug if "--worktree" in argv else False,
    }


# --- THE CLAUSE -------------------------------------------------------------

@pytest.mark.parametrize("effort", glc.EFFORT_ENUM)
@pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
def test_the_generators_fence_is_one_the_launcher_resolves(tmp_path, model, effort):
    """AX25-2: fence, contract location, model and base -- all four, in ONE assertion. Do not
    split it into four (see the module docstring)."""
    slug = "lane-probe-conformance"
    path = _render(tmp_path, slug=slug, model=model, effort=effort)
    assert properties(path, slug=slug, model=model) == CONFORMANT


def test_a_dry_run_of_the_launcher_over_a_generated_contract_resolves_the_same_lane(tmp_path):
    """End to end through the CLI the operator runs (`dispatch.py launch --dry-run`): exit 0, and
    the JSON it prints is the lane the contract declares. Pre-launch is not run by a dry run."""
    slug = "lane-probe-dryrun"
    path = _render(tmp_path, slug=slug, model="sonnet", effort="high")
    result = CliRunner().invoke(d.cli, ["launch", str(path), "--dry-run"])
    assert result.exit_code == 0, result.output
    got = json.loads(result.output.strip().splitlines()[-1])
    assert (got["slug"], got["model"], got["effort"], got["provider"]) == (
        slug, "sonnet", "high", "anthropic")
    assert got["argv"][:3] == ["claude", "--bg", "-n"]
    assert got["argv"][got["argv"].index("--worktree") + 1] == slug


def test_a_fence_the_launcher_refuses_is_reported_red_on_all_four(tmp_path):
    """The witness can fail: a head the launcher does not admit (the shape the generator emitted
    until 2026-09-12, which refused every contract it produced) reads RED, not green."""
    slug = "lane-probe-refused"
    path = _render(tmp_path, slug=slug, model="sonnet", effort="high")
    text = path.read_text(encoding="utf-8")
    fence = glc.find_command_line(text)
    assert fence is not None and fence.startswith("claude ")
    path.write_text(text.replace(fence, "Dispatch-Lane lane-probe-refused LANE-probe-refused.md"),
                    encoding="utf-8", newline="\n")
    assert properties(path, slug=slug, model="sonnet") == {k: False for k in CONFORMANT}


def test_a_fence_model_that_disagrees_with_the_routing_row_is_refused_not_picked(tmp_path):
    """`[#717]`: the fence and the contract's routing row both name the model, and two sources
    that disagree are a refusal, never a quiet pick of the more expensive one."""
    slug = "lane-probe-model"
    path = _render(tmp_path, slug=slug, model="sonnet", effort="high")
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("--model sonnet", "--model haiku"), encoding="utf-8", newline="\n")
    assert properties(path, slug=slug, model="sonnet") == {k: False for k in CONFORMANT}


def test_opusplan_is_refused_at_render_for_a_background_lane(tmp_path):
    """The model enum's fourth member is a no-op on a `--bg` lane; the writer refuses to emit it,
    so the sweep above does not carry it and no dispatch line for it exists to disagree."""
    with pytest.raises(glc.LaneContractError):
        _render(tmp_path, slug="lane-probe-opusplan", model="opusplan", effort="high")


# --- retired: the PowerShell probe and its hook --------------------------------

def test_the_win_tooling_probe_module_and_its_hook_are_retired():
    """Item 3 of LANE-B2-W1-b2-dispatch-local-sole: no conformance argv names a PowerShell because
    there is no conformance process that spawns one."""
    assert not (_REPO / "scripts" / "dispatch_conformance.py").exists()
    config = (_REPO / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert not re.search(r"^\s*-\s+id:\s+dispatch-conformance\s*$", config, re.MULTILINE)
    assert "scripts/dispatch_conformance.py" not in config
