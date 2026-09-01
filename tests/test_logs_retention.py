"""Tests for scripts/logs_retention.py (HY-2 -- dated logs/ into dated subfolders by a
RETENTION RULE; `logs/TOKEN-LOG.md` stays flat, strict append-only, no archival exception
(ADR-29/39 -- the 2026-07-17 LESSONS.md carve-out does NOT extend to it)).

RED-first per ADR-108 section B: written before the organ, including the TOKEN-LOG and
PROPOSALS-*/DETECTOR-ERROR-* exclusion fire-tests the frozen contract requires.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "logs_retention.py"


def _load():
    spec = importlib.util.spec_from_file_location("logs_retention", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["logs_retention"] = module
    spec.loader.exec_module(module)
    return module


lr = _load()


# --- is_excluded: the exclusion predicate, fired directly -------------------

def test_is_excluded_fires_for_token_log():
    assert lr.is_excluded("TOKEN-LOG.md") is True


def test_is_excluded_fires_for_proposals_prefix():
    # logs/PROPOSALS-*.md is read flat by a live consumer (scripts/propose_closures.py
    # resolve_window / find_last_proposals_head, scripts/review_closures.py
    # latest_proposals) -- relocating it would corrupt the closure-detector's pending
    # window and the loud-failure-on-absence signal.
    assert lr.is_excluded("PROPOSALS-2026-08-15.md") is True


def test_is_excluded_fires_for_detector_error_prefix():
    assert lr.is_excluded("DETECTOR-ERROR-2026-08-15.md") is True


def test_is_excluded_false_for_an_ordinary_dated_name():
    assert lr.is_excluded("WIDGET-2026-08-15.md") is False


# --- parse_dated_month: the naming predicate --------------------------------

def test_parse_dated_month_matches_trailing_date():
    assert lr.parse_dated_month("WIDGET-2026-08-15.md") == "2026-08"


def test_parse_dated_month_none_for_undated_name():
    assert lr.parse_dated_month("FLEET-HEALTH.md") is None


def test_parse_dated_month_none_for_invalid_calendar_date():
    assert lr.parse_dated_month("WIDGET-2026-13-40.md") is None


def test_parse_dated_month_none_for_token_log():
    assert lr.parse_dated_month("TOKEN-LOG.md") is None


# --- plan_moves: pure planning over a directory listing ---------------------

def test_plan_moves_token_log_excluded(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "TOKEN-LOG.md").write_text("### 2026-08-01 | entry\n", encoding="utf-8")
    (logs_dir / "WIDGET-2026-08-15.md").write_text("widget content\n", encoding="utf-8")
    moves = lr.plan_moves(logs_dir)
    srcs = {m[0].name for m in moves}
    assert "TOKEN-LOG.md" not in srcs
    assert "WIDGET-2026-08-15.md" in srcs


def test_plan_moves_proposals_and_detector_error_excluded(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "PROPOSALS-2026-08-15.md").write_text("p\n", encoding="utf-8")
    (logs_dir / "DETECTOR-ERROR-2026-08-16.md").write_text("d\n", encoding="utf-8")
    assert lr.plan_moves(logs_dir) == []


def test_plan_moves_undated_flat_files_untouched(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "FLEET-HEALTH.md").write_text("digest\n", encoding="utf-8")
    (logs_dir / "TELEMETRY.db").write_bytes(b"\x00\x01")
    assert lr.plan_moves(logs_dir) == []


def test_plan_moves_targets_month_subfolder(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("x\n", encoding="utf-8")
    moves = lr.plan_moves(logs_dir)
    assert len(moves) == 1
    src, dst = moves[0]
    assert src == logs_dir / "WIDGET-2026-08-15.md"
    assert dst == logs_dir / "2026-08" / "WIDGET-2026-08-15.md"


def test_plan_moves_ignores_files_already_in_a_dated_subfolder(tmp_path):
    logs_dir = tmp_path / "logs"
    (logs_dir / "2026-08").mkdir(parents=True)
    (logs_dir / "2026-08" / "WIDGET-2026-08-15.md").write_text("x\n", encoding="utf-8")
    assert lr.plan_moves(logs_dir) == []


def test_plan_moves_absent_dir_is_empty():
    assert lr.plan_moves(Path("this-does-not-exist-anywhere-xyz")) == []


# --- apply_moves: the mutation, content-preserving ---------------------------

def test_apply_moves_relocates_byte_identical(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    src_file = logs_dir / "WIDGET-2026-08-15.md"
    content = "line one\nline two\n"
    src_file.write_text(content, encoding="utf-8", newline="\n")
    moves = lr.plan_moves(logs_dir)
    lr.apply_moves(moves)
    dst = logs_dir / "2026-08" / "WIDGET-2026-08-15.md"
    assert dst.is_file()
    assert not src_file.exists()
    assert dst.read_bytes() == content.encode("utf-8")


def test_apply_moves_refuses_a_destination_collision(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("new\n", encoding="utf-8")
    dest_dir = logs_dir / "2026-08"
    dest_dir.mkdir()
    (dest_dir / "WIDGET-2026-08-15.md").write_text("old\n", encoding="utf-8")
    moves = [(logs_dir / "WIDGET-2026-08-15.md", dest_dir / "WIDGET-2026-08-15.md")]
    with pytest.raises(lr.RetentionError):
        lr.apply_moves(moves)
    # the pre-existing archive copy is untouched, and the source was NOT deleted
    assert (dest_dir / "WIDGET-2026-08-15.md").read_text(encoding="utf-8") == "old\n"
    assert (logs_dir / "WIDGET-2026-08-15.md").exists()


# --- run_retention: end-to-end, TOKEN-LOG never moves -----------------------

def test_run_retention_end_to_end_excludes_token_log_and_moves_dated(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    token_log_content = "### 2026-04-21 | entry one\n### 2026-08-15 | entry two\n"
    (logs_dir / "TOKEN-LOG.md").write_text(token_log_content, encoding="utf-8", newline="\n")
    (logs_dir / "PROPOSALS-2026-08-15.md").write_text("p\n", encoding="utf-8")
    (logs_dir / "WIDGET-2026-08-15.md").write_text("w\n", encoding="utf-8")

    moved = lr.run_retention(logs_dir)

    assert (logs_dir / "TOKEN-LOG.md").read_text(encoding="utf-8") == token_log_content
    assert (logs_dir / "PROPOSALS-2026-08-15.md").exists()
    assert not (logs_dir / "WIDGET-2026-08-15.md").exists()
    assert (logs_dir / "2026-08" / "WIDGET-2026-08-15.md").is_file()
    assert len(moved) == 1


def test_run_retention_dry_run_moves_nothing(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("w\n", encoding="utf-8")
    planned = lr.run_retention(logs_dir, dry_run=True)
    assert len(planned) == 1
    assert (logs_dir / "WIDGET-2026-08-15.md").exists()
    assert not (logs_dir / "2026-08").exists()


def test_run_retention_is_idempotent(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("w\n", encoding="utf-8")
    lr.run_retention(logs_dir)
    second = lr.run_retention(logs_dir)
    assert second == []
    assert (logs_dir / "2026-08" / "WIDGET-2026-08-15.md").is_file()


# --- main(): CLI smoke test --------------------------------------------------

def test_main_dry_run_reports_and_touches_nothing(tmp_path, capsys):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("w\n", encoding="utf-8")
    rc = lr.main(["--logs-dir", str(logs_dir), "--dry-run"])
    assert rc == 0
    assert (logs_dir / "WIDGET-2026-08-15.md").exists()
    out = capsys.readouterr().out
    assert "WIDGET-2026-08-15.md" in out


def test_main_live_run_relocates(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "WIDGET-2026-08-15.md").write_text("w\n", encoding="utf-8")
    rc = lr.main(["--logs-dir", str(logs_dir)])
    assert rc == 0
    assert (logs_dir / "2026-08" / "WIDGET-2026-08-15.md").is_file()


# --- the TARGET GUARD (terra CRIT, post-merge review round 2026-09-01) ----------------------
#
# THE DEFECT, in the reviewer's words: "`logs_dir` is accepted without constraining it to this
# repository's `logs/` directory. A caller can pass an external or synced path and the script
# will relocate its files."
#
# Exact. `main` took `--logs-dir` as a bare `Path`, `run_retention` passed it through, and
# `apply_moves` does `dst.parent.mkdir(parents=True)` + `src.rename(dst)` inside it. A MOVER with
# no constraint on where it moves. Against core-invariant #1 that is a T2 write into the
# exclusion zone from a script this repo ships -- and the hazard that rule names (a cleanup
# script that moved the operator's personal files) is precisely this shape.
#
# TWO INDEPENDENT LEGS, because they fail differently:
#   (1) EXCLUSION  -- an excluded-zone path is refused ABSOLUTELY, no override, wherever it sits.
#   (2) CONTAINMENT -- the directory must be inside the repo or inside the system temp dir,
#       which is what keeps `tmp_path` fixtures legal. Everything else is refused.
# A path can pass (2) and fail (1), so neither leg subsumes the other.

_ZONE = "OneDrive - " + "Blue Yonder"


def test_an_excluded_zone_path_is_refused_absolutely(tmp_path):
    mod = _load()
    bad = tmp_path / _ZONE / "logs"
    bad.mkdir(parents=True)
    with pytest.raises(mod.RetentionTargetError) as exc:
        mod.run_retention(bad, dry_run=True)
    assert "exclusion" in str(exc.value).lower()


def test_a_path_outside_the_repo_and_outside_temp_is_refused():
    mod = _load()
    with pytest.raises(mod.RetentionTargetError):
        mod.run_retention(Path.home() / "Documents" / "logs", dry_run=True)


def test_a_tmp_path_logs_dir_is_still_allowed(tmp_path):
    """Every fixture in this file depends on it, so the guard states that dependency."""
    mod = _load()
    d = tmp_path / "logs"
    d.mkdir()
    assert mod.run_retention(d, dry_run=True) == []


def test_the_repos_own_logs_dir_is_allowed():
    mod = _load()
    assert mod.run_retention(mod._DEFAULT_LOGS_DIR, dry_run=True) is not None


def test_the_guard_refuses_BEFORE_planning_not_after(tmp_path, monkeypatch):
    """Order matters. A guard that runs after `plan_moves` has already WALKED the directory, and
    reading an excluded path is itself outside what core-invariant #1 permits."""
    mod = _load()
    called = []
    monkeypatch.setattr(mod, "plan_moves", lambda d: called.append(d) or [])
    bad = tmp_path / _ZONE / "logs"
    bad.mkdir(parents=True)
    with pytest.raises(mod.RetentionTargetError):
        mod.run_retention(bad, dry_run=True)
    assert called == [], "plan_moves ran before the guard refused"


def test_main_reports_the_refusal_and_exits_nonzero(tmp_path, capsys):
    mod = _load()
    bad = tmp_path / _ZONE / "logs"
    bad.mkdir(parents=True)
    assert mod.main(["--logs-dir", str(bad), "--dry-run"]) == 2
    assert "refus" in capsys.readouterr().err.lower()
