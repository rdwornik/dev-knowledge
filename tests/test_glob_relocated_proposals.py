"""[#626] the copies that EXECUTE, not just the hub root, must see a relocated
PROPOSALS file.

`logs_retention.py` (lane-c-3) retired the `PROPOSALS-*.md` exclusion, so these files
are now eligible for relocation into a `logs/YYYY-MM/` bucket like any other dated log
artifact. The hub's `scripts/propose_closures.py` / `scripts/review_closures.py` were
re-pointed at `**/PROPOSALS-*.md` for that -- but three copies that actually EXECUTE
were not: the tier1-lifecycle PLUGIN copies (the LIVE Stop-hook scanner, CLAUDE.md
sections 8/9) and `scripts/fleet_health.py`'s pending-closures gauge. A root-only fix
left the running code broken -- the class this lane's frozen contract exists to close.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_PLUGIN_DIR = _REPO / "plugins" / "tier1-lifecycle" / "scripts"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # so inspect.getsource / linecache resolve cleanly
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def plugin_pc():
    return _load(_PLUGIN_DIR / "propose_closures.py", "pc_glob_test")


@pytest.fixture
def plugin_rc():
    return _load(_PLUGIN_DIR / "review_closures.py", "rc_glob_test")


@pytest.fixture
def fh():
    return _load(_REPO / "scripts" / "fleet_health.py", "fh_glob_test")


# --- plugin propose_closures.py: find_last_proposals_head / resolve_window -----


def test_plugin_find_last_proposals_head_finds_bucketed_file(tmp_path, plugin_pc):
    logs = tmp_path / "logs"
    (logs / "2026-06").mkdir(parents=True)
    (logs / "2026-06" / "PROPOSALS-2026-06-01.md").write_text(
        "---\nhead_commit: " + "1" * 40 + "\n---\n- [ ] **#5** — do x\n",
        encoding="utf-8",
    )
    assert plugin_pc.find_last_proposals_head(logs) == "1" * 40


def test_plugin_resolve_window_holds_baseline_from_bucketed_file(
    tmp_path, plugin_pc, monkeypatch
):
    # same pinned-baseline scenario as the hub's test_resolve_window_holds_baseline_
    # from_bucketed_file, run against the LIVE Stop-hook copy.
    logs = tmp_path / "logs"
    (logs / "2026-06").mkdir(parents=True)
    (logs / "2026-06" / "PROPOSALS-2026-06-01.md").write_text(
        "---\nhead_commit: " + "1" * 40 + "\nsince_commit: " + "0" * 40 + "\n---\n"
        "- [ ] **#5** — do x\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(plugin_pc, "git_valid_rev", lambda repo, rev: True)
    since, rng = plugin_pc.resolve_window(tmp_path, logs, {"5"})
    assert since == "0" * 40              # baseline HELD at since, not advanced
    assert rng == "0" * 40 + "..HEAD"


# --- plugin review_closures.py: latest_proposals --------------------------------


def test_plugin_latest_proposals_finds_bucketed_file(tmp_path, plugin_rc):
    logs = tmp_path / "logs"
    (logs / "2026-06").mkdir(parents=True)
    target = logs / "2026-06" / "PROPOSALS-2026-06-01.md"
    target.write_text("---\nhead_commit: " + "1" * 40 + "\n---\n", encoding="utf-8")
    assert plugin_rc.latest_proposals(logs) == target


def test_plugin_latest_proposals_picks_latest_across_flat_and_bucketed(tmp_path, plugin_rc):
    logs = tmp_path / "logs"
    (logs / "2026-06").mkdir(parents=True)
    (logs / "2026-06" / "PROPOSALS-2026-06-01.md").write_text(
        "---\nhead_commit: " + "1" * 40 + "\n---\n", encoding="utf-8",
    )
    later = logs / "PROPOSALS-2026-07-15.md"
    later.write_text("---\nhead_commit: " + "2" * 40 + "\n---\n", encoding="utf-8")
    assert plugin_rc.latest_proposals(logs) == later


# --- scripts/fleet_health.py: count_pending_closures -----------------------------

_BACKLOG_ONE_OPEN = "- [#11] [P2][M] eleven\n"


def test_fleet_health_count_pending_closures_finds_bucketed_file(tmp_path, fh):
    logs = tmp_path / "logs"
    (logs / "2026-06").mkdir(parents=True)
    (logs / "2026-06" / "PROPOSALS-2026-06-01.md").write_text(
        "- [ ] **#11** - a\n", encoding="utf-8",
    )
    assert fh.count_pending_closures(logs, _BACKLOG_ONE_OPEN) == 1


def test_fleet_health_count_pending_closures_dedupes_flat_and_bucketed(tmp_path, fh):
    # the same id unchecked in a flat file AND a bucketed one is still ONE pending
    # decision -- and the flat file must not be double-counted by the added scan.
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "PROPOSALS-2026-08-01.md").write_text("- [ ] **#11** - a\n", encoding="utf-8")
    (logs / "2026-06").mkdir()
    (logs / "2026-06" / "PROPOSALS-2026-06-01.md").write_text(
        "- [ ] **#11** - a\n", encoding="utf-8",
    )
    assert fh.count_pending_closures(logs, _BACKLOG_ONE_OPEN) == 1
