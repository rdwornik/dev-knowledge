"""The Architekt Jutra delta scan as a mechanism, not a one-off Gemini read
(LANE-5B2-15, `to-browser/DIGEST-AJ-DELTA-2026-09-25.md`).

THE PINNED TEST (`test_scan_against_09_21_state_reproduces_the_digests_seven_candidates`) is the
contract's Done-when item 2: a scan over the state a real 2026-09-21 run would have recorded,
against "today's folders" (a course dir with nothing newer, `SkillPanel/maister`'s two real
2026-09-22 commits and no commits on the other two repos), reproduces exactly C-1..C-7.

The other tests exercise the mechanism generically -- a genuinely new course file, a `gh`
failure, state round-tripping -- so the pinned test is not the only evidence the code works;
it is evidence the code reproduces THIS repo's own prior finding.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

import aj_scan as scan_mod

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "aj_scan"


# --- state round-trip ---------------------------------------------------------------------


def test_state_round_trips_through_save_and_load(tmp_path: Path) -> None:
    state = scan_mod.ScanState(
        last_scan_date="2026-09-25",
        course_high_water="2026-09-25T10:00:00Z",
        repos={"a/b": scan_mod.RepoState(since="2026-09-25T00:00:00Z")},
        carried_candidates=[scan_mod.CarriedCandidate(id="C-1", already_in="x", what="y",
                                                        cost="S")],
        next_candidate_seq=2,
    )
    path = tmp_path / "state.yaml"
    state.save(path)
    reloaded = scan_mod.ScanState.load(path)
    assert reloaded == state


def test_load_refuses_a_missing_state_file(tmp_path: Path) -> None:
    with pytest.raises(scan_mod.ScanError, match="no state file"):
        scan_mod.ScanState.load(tmp_path / "absent.yaml")


def test_load_reads_the_fixture_state_carrying_all_but_one_candidate() -> None:
    state = scan_mod.ScanState.load(FIXTURES / "state-2026-09-21.yaml")
    assert [c.id for c in state.carried_candidates] == ["C-1", "C-2", "C-3", "C-4", "C-5", "C-7"]
    assert state.next_candidate_seq == 6
    assert set(state.repos) == {
        "Architekt-Jutra/architekt-jutra-code",
        "TheSoftwareHouse/copilot-collections",
        "SkillPanel/maister",
    }


# --- course delta: mechanical, no delegate needed -----------------------------------------


def test_scan_course_finds_only_files_newer_than_the_high_water_mark(tmp_path: Path) -> None:
    old = tmp_path / "old.pdf"
    new = tmp_path / "new.pdf"
    old.write_text("old")
    new.write_text("new")
    since = datetime(2026, 9, 21, 12, 57, tzinfo=timezone.utc)
    old_ts = datetime(2026, 9, 21, 12, 10, tzinfo=timezone.utc).timestamp()
    new_ts = datetime(2026, 9, 23, 8, 0, tzinfo=timezone.utc).timestamp()
    os.utime(old, (old_ts, old_ts))
    os.utime(new, (new_ts, new_ts))

    found = scan_mod.scan_course(tmp_path, since)

    assert found == [new]


def test_scan_course_with_no_high_water_mark_returns_every_file(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_text("a")
    (tmp_path / "b.pdf").write_text("b")
    assert len(scan_mod.scan_course(tmp_path, None)) == 2


def test_scan_course_refuses_a_missing_dir(tmp_path: Path) -> None:
    with pytest.raises(scan_mod.ScanError, match="course dir not found"):
        scan_mod.scan_course(tmp_path / "nope", None)


# --- reference-repo commits: gh api ---------------------------------------------------------


def _fake_runner(stdout: str = "[]", returncode: int = 0, stderr: str = ""):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr=stderr)
    return runner


def test_scan_repo_commits_parses_the_maister_fixture() -> None:
    fixture = (FIXTURES / "maister-commits-2026-09-22.json").read_text(encoding="utf-8")
    commits = scan_mod.scan_repo_commits(
        "SkillPanel/maister", "2026-09-21T00:00:00Z", runner=_fake_runner(stdout=fixture)
    )
    assert [c["sha"][:9] for c in commits] == ["d412d49f1", "4151c9c4d"]


def test_scan_repo_commits_empty_list_is_not_an_error() -> None:
    commits = scan_mod.scan_repo_commits(
        "Architekt-Jutra/architekt-jutra-code", "2026-09-21T00:00:00Z",
        runner=_fake_runner(stdout="[]"),
    )
    assert commits == []


def test_scan_repo_commits_raises_on_a_nonzero_gh_exit() -> None:
    with pytest.raises(scan_mod.ScanError, match="exited 1"):
        scan_mod.scan_repo_commits(
            "a/b", "2026-09-21T00:00:00Z",
            runner=_fake_runner(returncode=1, stderr="gh: not authenticated"),
        )


def test_scan_repo_commits_raises_on_unreadable_json() -> None:
    with pytest.raises(scan_mod.ScanError, match="unreadable JSON"):
        scan_mod.scan_repo_commits("a/b", "2026-09-21T00:00:00Z",
                                    runner=_fake_runner(stdout="not json"))


def test_scan_repo_commits_raises_when_gh_cannot_be_run() -> None:
    def raising_runner(command, **kwargs):
        raise OSError("gh not found")

    with pytest.raises(scan_mod.ScanError, match="could not be run"):
        scan_mod.scan_repo_commits("a/b", "2026-09-21T00:00:00Z", runner=raising_runner)


def test_scan_repo_commits_flattens_multiple_pages() -> None:
    """The Codex terra HIGH finding this closes: a bare (unpaginated) `gh api` call returns
    only the first page, permanently dropping the rest on a busy repo."""
    slurped = json.dumps([[{"sha": "a" * 40}, {"sha": "b" * 40}], [{"sha": "c" * 40}]])
    commits = scan_mod.scan_repo_commits("a/b", "2026-09-21T00:00:00Z",
                                          runner=_fake_runner(stdout=slurped))
    assert [c["sha"][0] for c in commits] == ["a", "b", "c"]


def test_scan_repo_commits_passes_paginate_and_slurp_to_gh() -> None:
    seen: dict[str, Any] = {}

    def capturing_runner(command, **kwargs):
        seen["command"] = command
        return subprocess.CompletedProcess(command, 0, stdout="[[]]", stderr="")

    scan_mod.scan_repo_commits("a/b", "2026-09-21T00:00:00Z", runner=capturing_runner)
    assert "--paginate" in seen["command"]
    assert "--slurp" in seen["command"]


# --- repo cursor advancement: never a post-query clock reading -------------------------------


def test_next_repo_since_advances_to_the_latest_commit_date() -> None:
    commits = [
        {"commit": {"author": {"date": "2026-09-22T09:00:00Z"}}},
        {"commit": {"author": {"date": "2026-09-22T14:30:00Z"}}},
    ]
    since = scan_mod._next_repo_since(commits, previously_seen=True, old_since="2026-09-21T00:00:00Z",
                                       now_iso="2026-09-25T00:00:00Z")
    assert since == "2026-09-22T14:30:00Z"


def test_next_repo_since_does_not_advance_a_tracked_repo_with_nothing_found() -> None:
    """The Codex terra HIGH finding this closes: advancing an empty repo to `now_iso` (a clock
    reading taken AFTER the query ran) permanently skips a commit landing in between."""
    since = scan_mod._next_repo_since([], previously_seen=True, old_since="2026-09-21T00:00:00Z",
                                       now_iso="2026-09-25T00:00:00Z")
    assert since == "2026-09-21T00:00:00Z"


def test_next_repo_since_uses_now_iso_for_a_newly_seen_empty_repo() -> None:
    since = scan_mod._next_repo_since([], previously_seen=False, old_since="",
                                       now_iso="2026-09-25T00:00:00Z")
    assert since == "2026-09-25T00:00:00Z"


# --- the delegated large-read leg -----------------------------------------------------------


def test_delegate_describe_records_undisclosed_when_no_model_field() -> None:
    envelope = json.dumps({"response": "a one-sentence description"})
    result = scan_mod.delegate_describe("describe this", runner=_fake_runner(stdout=envelope))
    assert result.response == "a one-sentence description"
    assert result.served_model == scan_mod.UNDISCLOSED_MODEL


def test_delegate_describe_records_a_disclosed_model() -> None:
    envelope = json.dumps({"response": "x", "model": "gemini-3.1-pro-high"})
    result = scan_mod.delegate_describe("describe", runner=_fake_runner(stdout=envelope))
    assert result.served_model == "gemini-3.1-pro-high"


def test_delegate_describe_raises_on_nonzero_exit() -> None:
    with pytest.raises(scan_mod.ScanError, match="exited 1"):
        scan_mod.delegate_describe("x", runner=_fake_runner(returncode=1, stderr="denied"))


# --- candidate rows: carried + new, deterministic ids ---------------------------------------


def _delegate_stub(response: str, model: str = "stub-model"):
    def delegate(prompt: str) -> scan_mod.DelegateResult:
        return scan_mod.DelegateResult(response=response, served_model=model)
    return delegate


def test_build_candidates_with_no_delta_returns_only_the_carried_set() -> None:
    state = scan_mod.ScanState.load(FIXTURES / "state-2026-09-21.yaml")
    rows, new_state = scan_mod.build_candidates(state, course_new=[], repo_commits={})
    assert [r.id for r in rows] == ["C-1", "C-2", "C-3", "C-4", "C-5", "C-7"]
    assert new_state.next_candidate_seq == 6


def test_build_candidates_assigns_the_next_id_to_a_new_course_delta(tmp_path: Path) -> None:
    state = scan_mod.ScanState(last_scan_date="2026-09-21", course_high_water="2026-09-21T12:57:00Z",
                                repos={}, carried_candidates=[], next_candidate_seq=1)
    new_file = tmp_path / "AJ_M06L01_transkrypcja.pdf"
    new_file.write_text("x")
    rows, new_state = scan_mod.build_candidates(
        state, course_new=[new_file], repo_commits={},
        delegate=_delegate_stub("a new module on incident response"),
    )
    assert [r.id for r in rows] == ["C-1"]
    assert rows[0].served_model == "stub-model"
    assert "a new module on incident response" == rows[0].what
    assert new_state.next_candidate_seq == 2
    # the delta is carried forward so the next scan does not re-derive it
    assert new_state.carried_candidates[0].id == "C-1"


def test_build_candidates_assigns_ids_to_each_repo_with_new_commits() -> None:
    state = scan_mod.ScanState(last_scan_date="2026-09-21", course_high_water="2026-09-21T12:57:00Z",
                                repos={}, carried_candidates=[], next_candidate_seq=1)
    rows, _ = scan_mod.build_candidates(
        state, course_new=[],
        repo_commits={"a/b": [{"sha": "1234567890"}], "c/d": [], "e/f": [{"sha": "abcdefabcd"}]},
        delegate=_delegate_stub("unknown until the diff is read", model="stub-model"),
    )
    # `c/d` had no commits and gets no row; the other two do, in a stable order
    assert [r.id for r in rows] == ["C-1", "C-2"]
    assert "a/b" in rows[0].already_in
    assert "e/f" in rows[1].already_in
    assert rows[0].served_model == "stub-model"


# --- the pinned reproduction: 09-21 state + today's folders = C-1..C-7 ----------------------


def test_scan_against_09_21_state_reproduces_the_digests_seven_candidates(tmp_path: Path) -> None:
    """The Done-contract's item 2, made mechanical. `course_dir` has nothing newer than the
    state's high-water mark (matching the digest's own headline: 'the course has nothing new
    since the last scan'). `SkillPanel/maister` answers with its two real 2026-09-22 commits;
    the other two repos answer empty, matching '0 commits since 2026-09-21' for each."""
    state = scan_mod.ScanState.load(FIXTURES / "state-2026-09-21.yaml")

    course_dir = tmp_path / "course"
    course_dir.mkdir()
    old_file = course_dir / "AJ_M05L03.2_transkrypcja.pdf"
    old_file.write_text("unchanged since 09-21")
    old_ts = datetime(2026, 9, 21, 12, 21, tzinfo=timezone.utc).timestamp()
    os.utime(old_file, (old_ts, old_ts))

    maister_fixture = (FIXTURES / "maister-commits-2026-09-22.json").read_text(encoding="utf-8")
    empty_fixture = (FIXTURES / "empty-commits.json").read_text(encoding="utf-8")

    def commit_scanner(repo: str, since_iso: str, **kwargs):
        stdout = maister_fixture if repo == "SkillPanel/maister" else empty_fixture
        return scan_mod.scan_repo_commits(repo, since_iso, runner=_fake_runner(stdout=stdout))

    calls: list[str] = []

    def logging_delegate(prompt: str) -> scan_mod.DelegateResult:
        # No course delta in this fixture, so the only call this scan can make is the
        # repo-commit describe leg -- matching the digest's own "Diff content ... not
        # found" limitation, the stub answers exactly that, with the digest's own
        # attestation that the day's serving model went undisclosed.
        calls.append(prompt)
        return scan_mod.DelegateResult(response="unknown until the diff is read",
                                        served_model=scan_mod.UNDISCLOSED_MODEL)

    result = scan_mod.run_scan(
        course_dir=course_dir,
        repos=list(state.repos),
        state=state,
        scan_date="2026-09-25T00:00:00Z",
        commit_scanner=commit_scanner,
        delegate=logging_delegate,
    )

    ids = [r.id for r in result.rows]
    assert ids == ["C-1", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7"]
    assert len(calls) == 1, "exactly one delegated describe leg -- the maister commit delta"

    by_id = {r.id: r for r in result.rows}
    assert "SkillPanel/maister" in by_id["C-6"].already_in
    assert "d412d49f1" in by_id["C-6"].already_in
    assert "4151c9c4d" in by_id["C-6"].already_in
    assert by_id["C-6"].what == "unknown until the diff is read"
    assert by_id["C-6"].served_model == scan_mod.UNDISCLOSED_MODEL
    assert by_id["C-7"].already_in == "landing gap itself"

    assert result.course_new == []
    assert len(result.repo_commits["SkillPanel/maister"]) == 2
    assert result.repo_commits["Architekt-Jutra/architekt-jutra-code"] == []
    assert result.repo_commits["TheSoftwareHouse/copilot-collections"] == []

    # the new state carries C-6 forward and does not touch the untouched course high-water mark
    assert result.state.course_high_water == state.course_high_water
    assert result.state.next_candidate_seq == 7
    assert [c.id for c in result.state.carried_candidates] == [
        "C-1", "C-2", "C-3", "C-4", "C-5", "C-7", "C-6",
    ]

    # repo cursors: maister advances to its LATEST COMMIT's own date, never to scan_date's
    # "now" (the Codex terra HIGH finding this fix closes); the two empty repos do not
    # advance at all, since nothing was observed to justify moving their mark forward.
    assert result.state.repos["SkillPanel/maister"].since == "2026-09-22T14:30:00Z"
    assert result.state.repos["Architekt-Jutra/architekt-jutra-code"].since == "2026-09-21T00:00:00Z"
    assert result.state.repos["TheSoftwareHouse/copilot-collections"].since == "2026-09-21T00:00:00Z"


# --- CLI: --help documents the command (Done-contract item 3) -------------------------------


def test_cli_help_documents_the_scan_command() -> None:
    from click.testing import CliRunner

    runner = CliRunner()
    top = runner.invoke(scan_mod.cli, ["--help"])
    assert top.exit_code == 0
    assert "scan" in top.output

    sub = runner.invoke(scan_mod.cli, ["scan", "--help"])
    assert sub.exit_code == 0
    assert "--course" in sub.output
    assert "--repos" in sub.output
    assert "--since-state" in sub.output


def test_render_table_lists_every_row() -> None:
    rows = [scan_mod.CandidateRow(id="C-1", already_in="x", what="y", cost="S")]
    table = scan_mod.render_table(rows)
    assert "C-1" in table
    assert "x" in table
