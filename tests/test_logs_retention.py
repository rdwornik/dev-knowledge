"""Tests for scripts/logs_retention.py (HY-2 -- dated logs/ into dated subfolders by a
RETENTION RULE; `logs/TOKEN-LOG.md` stays flat, strict append-only, no archival exception
(ADR-29/39 -- the 2026-07-17 LESSONS.md carve-out does NOT extend to it)).

RED-first per ADR-108 section B: written before the organ, including the TOKEN-LOG
exclusion fire-test the frozen contract requires. The PROPOSALS-*/DETECTOR-ERROR-*
prefix exemption was RETIRED by lane-c-3 (2026-09-01) once its two live consumers
(propose_closures.py, review_closures.py) were re-pointed at bucketed paths -- see
`test_is_excluded_false_for_proposals_and_detector_error_prefix` below, which replaces
the old fire-tests for those two prefixes.
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


def test_is_excluded_false_for_proposals_and_detector_error_prefix():
    # RETIRED exemption (lane-c-3, 2026-09-01): propose_closures.py / review_closures.py
    # now resolve `**/PROPOSALS-*.md` (bucketed AND flat), so relocating these no longer
    # corrupts the closure-detector's pending window or the loud-failure-on-absence signal.
    assert lr.is_excluded("PROPOSALS-2026-08-15.md") is False
    assert lr.is_excluded("DETECTOR-ERROR-2026-08-15.md") is False


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


def test_plan_moves_proposals_and_detector_error_now_planned(tmp_path):
    # RETIRED exemption (lane-c-3, 2026-09-01) -- these are dated like any other file now.
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "PROPOSALS-2026-08-15.md").write_text("p\n", encoding="utf-8")
    (logs_dir / "DETECTOR-ERROR-2026-08-16.md").write_text("d\n", encoding="utf-8")
    moves = lr.plan_moves(logs_dir)
    srcs = {m[0].name for m in moves}
    assert srcs == {"PROPOSALS-2026-08-15.md", "DETECTOR-ERROR-2026-08-16.md"}


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

    # TOKEN-LOG.md alone stays fixed in place -- the one absolute exclusion.
    assert (logs_dir / "TOKEN-LOG.md").read_text(encoding="utf-8") == token_log_content
    # PROPOSALS-*.md now relocates too (RETIRED exemption, lane-c-3, 2026-09-01).
    assert not (logs_dir / "PROPOSALS-2026-08-15.md").exists()
    assert (logs_dir / "2026-08" / "PROPOSALS-2026-08-15.md").is_file()
    assert not (logs_dir / "WIDGET-2026-08-15.md").exists()
    assert (logs_dir / "2026-08" / "WIDGET-2026-08-15.md").is_file()
    assert len(moved) == 2


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
    """MADE FALSIFIABLE 2026-09-08 ([#643] leg d). The prior body was

        assert mod.run_retention(mod._DEFAULT_LOGS_DIR, dry_run=True) is not None

    and `run_retention` returns a LIST — never None, on any input, for any state of the guard
    or of `logs/`. The assertion therefore held under every possible outcome, including a
    guard that had stopped refusing anything at all. A test that cannot fail is worse than no
    test: it reports a safety it does not provide, and this file's own subject is a module
    that MOVES files under core-invariant #1's exclusion rule.

    Three limbs, each of which a real regression breaks:
      1. the containment leg ADMITS this repo's own `logs/` and returns it RESOLVED — the
         positive half of the guard, and the only claim this test's name makes;
      2. `TOKEN-LOG.md` is never planned, whatever the live directory holds (ADR-29/39: the
         absolute exclusion, with no archival carve-out);
      3. every planned destination is a `logs/YYYY-MM/` bucket keyed off the source's OWN
         date, and `dry_run` leaves the directory byte-for-byte as it found it."""
    mod = _load()
    logs = mod._DEFAULT_LOGS_DIR
    resolved = logs.resolve()

    assert mod._assert_target_allowed(logs) == resolved

    before = sorted(p.name for p in logs.iterdir()) if logs.is_dir() else []
    planned = mod.run_retention(logs, dry_run=True)

    assert all(src.name != mod.TOKEN_LOG_NAME for src, _dst in planned)
    for src, dst in planned:
        assert not mod.is_excluded(src.name)
        assert dst.parent.parent == resolved
        assert dst.parent.name == mod.parse_dated_month(src.name)
        assert dst.name == src.name

    after = sorted(p.name for p in logs.iterdir()) if logs.is_dir() else []
    assert after == before


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


# --- the per-run sequence grammar (operator declaration 2026-09-04, candidate k) ---
#
# THE MEASURED DEFECT these pin, so the scenario is not re-derived from the fix:
# `PROPOSALS-<date>.md` was a DAY-granular name for a per-RUN artifact. Two real runs on
# 2026-09-02 -- head_commit 55fecf34 / window 4754 and 040dec74 / window 4763, eleven minutes
# apart during batch-G integration -- competed for one filename. Flat, the second overwrote the
# first. Once one copy had been archived, `apply_moves` correctly REFUSED to overwrite it and
# aborted the WHOLE plan, so 09-03 and 09-04 queued behind a collision that never cleared.


def test_parse_dated_month_accepts_a_run_sequence():
    """A sequenced per-run file is DATED, not undated.

    Without this arm the sequence fix is worse than the bug: a sequenced file matches nothing,
    is treated as undated, and accumulates FLAT forever -- reinstating the complaint the
    retention organ exists to answer.
    """
    assert lr.parse_dated_month("PROPOSALS-2026-09-02-02.md") == "2026-09"
    assert lr.parse_dated_month("PROPOSALS-2026-09-05-01.md") == "2026-09"
    assert lr.parse_dated_month("DETECTOR-ERROR-2026-09-05-17.md") == "2026-09"


def test_parse_dated_month_still_rejects_an_impossible_date_with_a_sequence():
    """The sequence arm must not smuggle a bad calendar date past the validator."""
    assert lr.parse_dated_month("WIDGET-2026-13-40-02.md") is None


def test_a_sequenced_second_run_relocates_beside_the_first(tmp_path):
    """Two runs on ONE day both reach the same month bucket, neither overwriting the other."""
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "PROPOSALS-2026-09-02-01.md").write_text("run one", encoding="utf-8")
    (logs / "PROPOSALS-2026-09-02-02.md").write_text("run two", encoding="utf-8")

    lr.run_retention(logs)

    bucket = logs / "2026-09"
    assert (bucket / "PROPOSALS-2026-09-02-01.md").read_text(encoding="utf-8") == "run one"
    assert (bucket / "PROPOSALS-2026-09-02-02.md").read_text(encoding="utf-8") == "run two"
    assert not list(logs.glob("PROPOSALS-*.md")), "nothing dated may remain flat"


def test_sequenced_names_sort_in_run_order_within_a_day(tmp_path):
    """Name order must EQUAL time order -- the reason every run is sequenced, not just the 2nd.

    `-` is 0x2D and `.` is 0x2E, so a bare `<date>.md` sorts AFTER `<date>-02.md`. Had run 1
    kept the bare name, the six `sorted(...)[-1]` "latest" sites across propose_closures,
    review_closures and fleet_health would each return run 1 and silently hide run 2.
    """
    names = ["PROPOSALS-2026-09-02-01.md", "PROPOSALS-2026-09-02-02.md",
             "PROPOSALS-2026-09-03-01.md"]
    assert sorted(names) == names
    assert sorted(names)[-1] == "PROPOSALS-2026-09-03-01.md"


# --- the TRIGGER ------------------------------------------------------------------------
#
# `[#664]`'s second ratified TRIGGER row, and `[#655]`'s whole title -- *"run_retention() has
# no production caller"*. Every test above this line calls `run_retention` from a test and
# proves the rule CORRECT; none of them makes anything CALL it, which is the entire content
# of `[#655]`. A rule nothing runs is a rule that will be re-needed next month, which is the
# module's own docstring's argument for existing at all.

_REPO = Path(__file__).resolve().parent.parent


def _session_hook_commands(event: str) -> list[str]:
    """Every hook command registered for `event` in this repo's `.claude/settings.json`."""
    import json
    settings = json.loads((_REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    return [hook.get("command", "")
            for matcher in settings.get("hooks", {}).get(event, [])
            for hook in matcher.get("hooks", [])]


def test_a_session_hook_CALLS_run_retention_and_not_only_the_test_suite():
    """RED-first witness for `[#664]`'s TRIGGER row / `[#655]`'s open question."""
    wired = [c for c in _session_hook_commands("SessionStart")
             if "scripts/logs_retention.py" in c]
    assert wired, (
        "scripts/logs_retention.py is called by no SessionStart hook -- run_retention() still "
        "has no production caller ([#655]), and the tests above call it themselves, which "
        "schedules nothing. [#664] named the SessionStart/Stop path that writes the logs it "
        "would retain")
    assert len(wired) == 1, f"one trigger, not {len(wired)}: {wired}"
    command = wired[0]
    # A retention rule wired in --dry-run mode REPORTS and retains nothing: it would satisfy
    # a grep for the module name while leaving [#655] exactly as open as it is today.
    assert "--dry-run" not in command, (
        f"the wired call must actually relocate, not report: {command!r}")
    # ADR-106: every python hook command in this file runs through the declared environment.
    # [#808]: the hook runs inside `bounded_hook.py run ... -- <command>`, a stdlib wrapper on
    # the system interpreter (the ADR-77 exception's reasoning); the WRAPPED command is the one
    # that must go through the declared environment, and it is held to exactly the old test.
    if "bounded_hook.py" in command:
        command = command.split(" -- ", 1)[1]
    assert command.startswith("uv run --locked "), command


def test_the_retention_trigger_is_on_SESSION_START_not_STOP_and_the_reason_is_pinned():
    """WHY SessionStart, recorded as an assertion because the census offered both.

    The producer of the files this rule retains is `propose_closures.py`, fired by the
    tier1-lifecycle plugin's **Stop** hook. Wiring retention into the same Stop event would
    have a renamer and that producer's own read of `**/PROPOSALS-*.md` interleaving inside
    one event, for no gain: relocation at the NEXT session's start reaches exactly the same
    files, one session later, with nothing racing it. Pinned so the placement is a decision
    a reader can find rather than an accident of where it was easy to add."""
    assert not [c for c in _session_hook_commands("Stop") if "logs_retention" in c], (
        "logs_retention must NOT be on the Stop path: propose_closures writes and re-reads "
        "logs/**/PROPOSALS-*.md inside that same event")


def test_the_retention_trigger_row_and_its_disposition_cannot_both_be_live():
    """A wired module is not an orphan -- the same coupling the archive_row_body row states."""
    sys.path.insert(0, str(_REPO / "scripts"))
    import graph_queries as gq
    assert "scripts/logs_retention.py" not in gq.ORPHAN_DISPOSITIONS, (
        "logs_retention.py now has a trigger and still carries an ORPHAN_DISPOSITIONS entry")
