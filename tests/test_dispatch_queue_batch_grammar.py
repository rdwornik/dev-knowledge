"""RED-first witnesses for [#1674]: `queue --batch` obeys the same `E<n>.<n>` grammar as `launch`.

A malformed batch (`bogus`, `E2.0junk`, `B1`) -- from `--batch` or `$HARNESS_BATCH` -- is refused (rc 5,
`REFUSED [batch-grammar]`) BEFORE any launch or spawn. `--dry-run` only prints a static order and
spawns nothing, so it is not gated (the order template renders it with a placeholder batch). A well-formed batch
passes through to `launch_lane`; an empty one stays the callers' own case.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))
    monkeypatch.delenv("HARNESS_BATCH", raising=False)


def _contract(tmp_path: Path, slug: str = "lane-a") -> Path:
    filename = f"LANE-{slug}.md"
    text = "\n\n".join([
        f"# LANE {slug} -- a synthetic lane\n",
        "| Model | Mode | Effort |\n|---|---|---|\n| claude-sonnet-5 | execute | high |\n",
        f"## Dispatch\n\n```\nclaude --bg -n {slug} --model claude-sonnet-5 --effort high "
        f'--permission-mode bypassPermissions --worktree {slug} "..."\n```\n',
        f"slug `{slug}` -> branch `worktree-{slug}` -> contract `{filename}`\n",
        "**Files you own:** `scripts/nothing.py`.\n",
    ])
    path = tmp_path / filename
    path.write_text(text, encoding="utf-8")
    return path


class _Recorder:
    def __init__(self, monkeypatch, allow_launch=False):
        self.launches, self.spawns = [], []

        def fake_launch(request, **kw):
            if not allow_launch:
                raise AssertionError("launch_lane must not be called")
            self.launches.append(request)
            return d.LaunchResult(slug=request.slug, provider="anthropic", model_requested=request.model,
                                  model_reported="pending", job_id="abcd1234", worktree="w",
                                  session_name=request.slug)

        def fake_spawn(*a, **k):
            self.spawns.append(a)
            raise AssertionError("spawn_process must not be called")

        monkeypatch.setattr(d, "launch_lane", fake_launch)
        monkeypatch.setattr(d, "spawn_process", fake_spawn)
        monkeypatch.setattr(d, "list_agents", lambda: [])


def _queue(contract, tmp_path, *extra):
    return CliRunner().invoke(d.cli, ["queue", str(contract), "--repo-root", str(tmp_path / "repo"),
                                      "--floor-mb", "0", *extra])


@pytest.mark.parametrize("batch", ["bogus", "E2.0junk", "B1"])
def test_queue_refuses_a_malformed_batch_before_any_launch(tmp_path, monkeypatch, batch):
    rec = _Recorder(monkeypatch)
    contract = _contract(tmp_path)

    out = _queue(contract, tmp_path, "--batch", batch,)

    assert out.exit_code == 5, out.output
    assert "batch-grammar" in out.output
    assert rec.launches == [] and rec.spawns == []


def test_queue_refuses_what_launch_refuses(tmp_path, monkeypatch):
    _Recorder(monkeypatch)
    contract = _contract(tmp_path)

    launched = CliRunner().invoke(d.cli, ["launch", str(contract), "--batch", "bogus", "--dry-run"])
    queued = _queue(contract, tmp_path, "--batch", "bogus")

    assert launched.exit_code == queued.exit_code == 5
    assert "batch-grammar" in launched.output and "batch-grammar" in queued.output


def test_queue_passes_a_well_formed_batch_to_launch_lane(tmp_path, monkeypatch):
    rec = _Recorder(monkeypatch, allow_launch=True)
    contract = _contract(tmp_path)

    out = _queue(contract, tmp_path, "--batch", "E2.0")

    assert out.exit_code == 0, out.output
    assert [r.batch for r in rec.launches] == ["E2.0"]


def test_queue_with_no_batch_anywhere_still_launches(tmp_path, monkeypatch):
    rec = _Recorder(monkeypatch, allow_launch=True)
    contract = _contract(tmp_path)

    out = _queue(contract, tmp_path)

    assert out.exit_code == 0, out.output
    assert len(rec.launches) == 1 and rec.launches[0].batch == ""


def test_a_malformed_harness_batch_env_is_refused_too(tmp_path, monkeypatch):
    rec = _Recorder(monkeypatch)
    monkeypatch.setenv("HARNESS_BATCH", "bogus")
    contract = _contract(tmp_path)

    out = _queue(contract, tmp_path)

    assert out.exit_code == 5, out.output
    assert rec.launches == [] and rec.spawns == []
