"""handback.py -- the handback organ (LANE-W4B-2-handback-organ, FR2).

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/handback.py` existed.

The plan's own acceptance leg for FR2: "the organ refuses a lane with (a) a foreign commit,
(b) a review record with no consumer, (c) a ratchet breach, (d) a transport write -- one test
each; a clean lane yields all four artifacts, byte-validated against the schema." The four
refusal-cause tests below monkeypatch exactly ONE self-check leg to fail and the other four to
pass, so each test isolates its named cause. `branch_purity_check`, `transport_write_check`,
`ratchet_check` and `ship_gate_check` additionally get their OWN unit tests against real git
repos / injected runners, proving the leg itself is not vacuous (not just that the organ reacts
correctly to a canned CheckResult).
"""
from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-handback-fr2"
BRANCH = "worktree-lane-handback-fr2"

CHECK_NAMES = {
    "branch_purity_check": "branch-purity",
    "ship_gate_check": "ship-gate",
    "ratchet_check": "ratchet",
    "review_consumer_check": "review-consumer",
    "branch_naming_check": "branch-naming",
    "transport_write_check": "transport-write",
}


def _mod(name: str):
    return importlib.import_module(name)


def _git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True, text=True)


@pytest.fixture()
def git_repo(tmp_path: Path) -> Path:
    """A tiny real repo: `main` with one commit, `worktree-lane-x` branched off it with one more."""
    root = tmp_path / "repo"
    root.mkdir()
    _git("init", "-b", "main", cwd=root)
    _git("config", "user.email", "t@example.com", cwd=root)
    _git("config", "user.name", "t", cwd=root)
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    _git("add", "a.txt", cwd=root)
    _git("commit", "-m", "init", cwd=root)
    _git("checkout", "-b", "worktree-lane-x", cwd=root)
    (root / "b.txt").write_text("b\n", encoding="utf-8")
    _git("add", "b.txt", cwd=root)
    _git("commit", "-m", "feat: b", cwd=root)
    return root


@pytest.fixture()
def transport(tmp_path: Path) -> Path:
    root = tmp_path / "drive"
    (root / "to-browser").mkdir(parents=True)
    (root / "to-cc").mkdir()
    return root


def _resolve(transport: Path):
    return lambda: transport / "to-browser"


# --- leg unit tests: branch purity (real git, not vacuous) ---------------------------------------

def test_branch_purity_check_allows_an_ordinary_lane_history(git_repo):
    hb = _mod("handback")
    result = hb.branch_purity_check(git_repo, base="main")
    assert result.ok is True


def test_branch_purity_check_allows_a_merge_of_the_base(git_repo):
    hb = _mod("handback")
    _git("checkout", "main", cwd=git_repo)
    (git_repo / "d.txt").write_text("d\n", encoding="utf-8")
    _git("add", "d.txt", cwd=git_repo)
    _git("commit", "-m", "main moved", cwd=git_repo)
    _git("checkout", "worktree-lane-x", cwd=git_repo)
    _git("merge", "main", "-m", "sync main", cwd=git_repo)
    result = hb.branch_purity_check(git_repo, base="main")
    assert result.ok is True


def test_branch_purity_check_flags_a_merge_of_a_foreign_branch(git_repo):
    hb = _mod("handback")
    _git("checkout", "main", cwd=git_repo)
    _git("checkout", "-b", "foreign", cwd=git_repo)
    (git_repo / "c.txt").write_text("c\n", encoding="utf-8")
    _git("add", "c.txt", cwd=git_repo)
    _git("commit", "-m", "foreign work", cwd=git_repo)
    _git("checkout", "worktree-lane-x", cwd=git_repo)
    _git("merge", "--no-ff", "foreign", "-m", "merge foreign", cwd=git_repo)
    result = hb.branch_purity_check(git_repo, base="main")
    assert result.ok is False and "foreign" not in result.detail  # named by sha, not by branch
    assert "merge something other than main" in result.detail


def test_branch_purity_check_reports_an_unresolvable_base(tmp_path):
    hb = _mod("handback")
    tmp_path.mkdir(exist_ok=True)
    result = hb.branch_purity_check(tmp_path, base="origin/main")
    assert result.ok is False


# --- leg unit tests: branch-naming -----------------------------------------------------------

def test_branch_naming_check_passes_a_ratified_worktree_branch():
    hb = _mod("handback")
    result = hb.branch_naming_check("worktree-handback-organ")
    assert result.ok is True


def test_branch_naming_check_flags_a_branch_outside_the_enum():
    hb = _mod("handback")
    result = hb.branch_naming_check("some-random-branch")
    assert result.ok is False and "some-random-branch" in result.detail


def test_branch_naming_check_with_repo_passes_when_branch_matches_head(git_repo):
    """Real git, not vacuous: checks out a conforming (non-batch-shaped) worktree branch and
    verifies the cross-check accepts it because it is what `HEAD` actually resolves to."""
    hb = _mod("handback")
    _git("checkout", "-b", "worktree-real-branch", cwd=git_repo)
    result = hb.branch_naming_check("worktree-real-branch", git_repo)
    assert result.ok is True and "matches HEAD" in result.detail


def test_branch_naming_check_with_repo_flags_a_mismatch_against_the_checked_out_branch(git_repo):
    """A conforming name that is NOT what `HEAD` resolves to -- sol/terra's finding that naming
    was checked in isolation from the branch every other leg actually inspects."""
    hb = _mod("handback")
    _git("checkout", "-b", "worktree-real-branch", cwd=git_repo)
    result = hb.branch_naming_check("worktree-some-other-lane", git_repo)
    assert result.ok is False and "does not match the checked-out branch" in result.detail
    assert "worktree-real-branch" in result.detail


# --- leg unit tests: transport-write ---------------------------------------------------------

def test_transport_write_check_flags_a_to_cc_file_naming_the_lane(transport):
    hb = _mod("handback")
    (transport / "to-cc" / f"SOMETHING-{LANE}.md").write_text("x", encoding="utf-8")
    result = hb.transport_write_check(LANE, _resolve(transport))
    assert result.ok is False and LANE in result.detail


def test_transport_write_check_passes_when_to_cc_names_nothing_of_the_lane(transport):
    hb = _mod("handback")
    (transport / "to-cc" / "DECLARE-something-else.md").write_text("x", encoding="utf-8")
    result = hb.transport_write_check(LANE, _resolve(transport))
    assert result.ok is True


def test_transport_write_check_passes_when_transport_is_unmounted():
    hb = _mod("handback")
    tr = _mod("transport_report")

    def unmounted():
        raise tr.TransportRefused("not mounted")

    result = hb.transport_write_check(LANE, unmounted)
    assert result.ok is True


# --- changed-files: real git, fails CLOSED --------------------------------------------------

def test_changed_files_or_raise_reports_the_lanes_own_changed_paths(git_repo):
    hb = _mod("handback")
    assert hb.changed_files_or_raise(git_repo, base="main") == ["b.txt"]


def test_changed_files_or_raise_raises_rather_than_returning_empty_on_git_failure(tmp_path):
    """The sol/terra CRITICAL this closes: `_tr.changed_files()` returns `[]` on git failure
    (correct for a best-effort report), which would let `review_consumer_check` see "no new
    audits" instead of "I could not tell" -- a fail-OPEN gate. This must fail CLOSED instead."""
    hb = _mod("handback")
    tmp_path.mkdir(exist_ok=True)
    with pytest.raises(hb.ChangedFilesUnknown):
        hb.changed_files_or_raise(tmp_path, base="origin/main")


def test_run_self_check_turns_an_unresolvable_changed_files_into_a_failing_review_consumer_leg(
        monkeypatch, tmp_path, transport):
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    monkeypatch.setattr(hb, "changed_files_or_raise",
                        lambda *a, **k: (_ for _ in ()).throw(hb.ChangedFilesUnknown("boom")))
    repo = tmp_path / "repo"
    repo.mkdir()
    purity, checks = hb.run_self_check(repo, LANE, BRANCH, hb.DEFAULT_BASE, _resolve(transport))
    review_consumer = next(c for c in checks if c.name == "review-consumer")
    assert review_consumer.ok is False and "boom" in review_consumer.detail


# --- leg unit tests: ratchet, ship-gate, review-consumer (injected) ------------------------------

def test_ratchet_check_reports_the_failure_tail(tmp_path):
    hb = _mod("handback")
    result = hb.ratchet_check(tmp_path, runner=lambda *a, **k: (1, "AssertionError: boom"))
    assert result.ok is False and "boom" in result.detail


def test_ratchet_check_passes_on_a_clean_exit(tmp_path):
    hb = _mod("handback")
    result = hb.ratchet_check(tmp_path, runner=lambda *a, **k: (0, ""))
    assert result.ok is True


def test_ship_gate_check_passes_when_head_is_clean(tmp_path):
    hb = _mod("handback")
    result = hb.ship_gate_check(tmp_path, head_fails=lambda repo: frozenset())
    assert result.ok is True


def test_ship_gate_check_passes_when_the_fail_is_already_on_the_baseline(tmp_path):
    hb = _mod("handback")
    result = hb.ship_gate_check(tmp_path, head_fails=lambda repo: frozenset({"check_x"}),
                                base_fails=lambda: frozenset({"check_x"}))
    assert result.ok is True


def test_ship_gate_check_flags_only_what_the_branch_introduced(tmp_path):
    hb = _mod("handback")
    result = hb.ship_gate_check(tmp_path, head_fails=lambda repo: frozenset({"check_x", "check_y"}),
                                base_fails=lambda: frozenset({"check_x"}))
    assert result.ok is False and "check_y" in result.detail and "check_x" not in result.detail


def test_review_consumer_check_is_a_no_op_with_no_new_audit(tmp_path):
    hb = _mod("handback")
    result = hb.review_consumer_check(tmp_path, ["scripts/a.py"])
    assert result.ok is True


def test_review_consumer_check_flags_an_undeclared_own_audit(monkeypatch, tmp_path):
    hb = _mod("handback")
    cal = _mod("consumer_at_landing")

    class _Artifact:
        def __init__(self, name: str) -> None:
            self.name = name

    monkeypatch.setattr(cal, "measure", lambda repo: object())
    monkeypatch.setattr(cal, "undeclared", lambda m: [_Artifact("2026-09-22-codex-lane-x.md")])
    result = hb.review_consumer_check(tmp_path, ["docs/audits/2026-09-22-codex-lane-x.md"])
    assert result.ok is False and "2026-09-22-codex-lane-x.md" in result.detail


def test_review_consumer_check_passes_when_declared(monkeypatch, tmp_path):
    hb = _mod("handback")
    cal = _mod("consumer_at_landing")
    monkeypatch.setattr(cal, "measure", lambda repo: object())
    monkeypatch.setattr(cal, "undeclared", lambda m: [])
    result = hb.review_consumer_check(tmp_path, ["docs/audits/2026-09-22-codex-lane-x.md"])
    assert result.ok is True


# --- FR2 acceptance: one refusal test per named cause, plus the clean case -----------------------

def _stub_all_checks_ok(monkeypatch, hb) -> None:
    for name in CHECK_NAMES:
        monkeypatch.setattr(hb, name, lambda *a, _n=name, **k: hb.CheckResult(CHECK_NAMES[_n], True, "ok"))
    monkeypatch.setattr(hb, "changed_files_or_raise", lambda *a, **k: [])
    monkeypatch.setattr(hb._tr, "changed_files", lambda repo: [])
    monkeypatch.setattr(hb, "_git_head", lambda repo: "1a2b3c4d")


@pytest.mark.parametrize("failing_name", ["branch_purity_check", "review_consumer_check",
                                          "ratchet_check", "transport_write_check"])
def test_the_organ_refuses_with_a_receipt_for_each_named_cause(monkeypatch, tmp_path, transport,
                                                               failing_name):
    hb = _mod("handback")
    hs = _mod("handback_schema")
    _stub_all_checks_ok(monkeypatch, hb)
    monkeypatch.setattr(hb, failing_name,
                        lambda *a, **k: hb.CheckResult(CHECK_NAMES[failing_name],
                                                       False, f"synthetic failure ({failing_name})"))
    repo = tmp_path / "repo"
    repo.mkdir()

    code, receipt = hb.run(LANE, BRANCH, "docs-only", repo, resolve_transport=_resolve(transport))

    assert code == hb.EXIT_REFUSED
    assert receipt["status"] == "REFUSED"
    assert CHECK_NAMES[failing_name] in receipt["reasons"][0]

    refused_path = transport / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md"
    assert refused_path.is_file()
    order = hs.RefusedOrder.parse(refused_path.read_text(encoding="utf-8"))
    assert order is not None
    ok, _ = order.validate()
    assert ok is True
    assert [c.name for c in order.checks if not c.ok] == [CHECK_NAMES[failing_name]]

    # nothing mergeable reached the transport
    assert not (transport / "to-browser" / f"LANE-END-{LANE}.md").exists()
    session_path = transport / "to-browser" / f"SESSION-{LANE}.md"
    assert not session_path.exists() or "HANDBACK " not in session_path.read_text(encoding="utf-8")


def test_a_clean_lane_yields_all_four_schema_valid_artifacts(monkeypatch, tmp_path, transport):
    hb = _mod("handback")
    hs = _mod("handback_schema")
    _stub_all_checks_ok(monkeypatch, hb)
    repo = tmp_path / "repo"
    repo.mkdir()

    code, receipt = hb.run(LANE, BRANCH, "docs-only", repo, resolve_transport=_resolve(transport))

    assert code == hb.EXIT_OK
    assert receipt["status"] == "ok"
    assert not (transport / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md").exists()

    # 1. the LANE-END report, byte-validated against the schema
    report_path = transport / "to-browser" / f"LANE-END-{LANE}.md"
    assert report_path.is_file()
    report_facts = hs.LaneEndReport.parse(report_path.read_text(encoding="utf-8"))
    ok, _ = report_facts.validate()
    assert ok is True

    # 2. the session file, at the canonical worktree-slug name
    session_path = transport / "to-browser" / f"SESSION-{LANE}.md"
    assert session_path.is_file()
    text = session_path.read_text(encoding="utf-8")
    handback_lines = [ln for ln in text.splitlines() if ln.startswith("HANDBACK ")]
    state_lines = [ln for ln in text.splitlines() if ln.startswith("STATE ")]
    assert len(handback_lines) == 1
    assert len(state_lines) == 1

    # 3. the HANDBACK line
    handback = hs.HandbackLine.parse(handback_lines[0])
    assert handback is not None
    h_ok, _ = handback.validate()
    assert h_ok is True

    # 4. the STATE line
    state = hs.StateLine.parse(state_lines[0])
    assert state is not None
    s_ok, _ = state.validate()
    assert s_ok is True
    assert state.verdict == hs.STATE_WAITING


def test_a_second_handback_appends_rather_than_overwriting_prior_narrative(monkeypatch, tmp_path,
                                                                          transport):
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    (transport / "to-browser" / f"SESSION-{LANE}.md").write_text(
        "# SESSION\n\nsome narrative the lane wrote by hand\n", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()

    code, _ = hb.run(LANE, BRANCH, "docs-only", repo, resolve_transport=_resolve(transport))

    assert code == hb.EXIT_OK
    text = (transport / "to-browser" / f"SESSION-{LANE}.md").read_text(encoding="utf-8")
    assert "some narrative the lane wrote by hand" in text
    assert text.count("HANDBACK ") == 1


def test_the_refused_receipt_never_exits_the_stop_hooks_blocking_code(monkeypatch, tmp_path,
                                                                     transport):
    """Exit 2 is a Stop hook's block-and-continue; this organ is not on that path, but the
    convention (3=refused, 4=internal) is shared with every other organ on the hub."""
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    monkeypatch.setattr(hb, "branch_purity_check",
                        lambda *a, **k: hb.CheckResult("branch-purity", False, "synthetic"))
    repo = tmp_path / "repo"
    repo.mkdir()
    code, _ = hb.run(LANE, BRANCH, "docs-only", repo, resolve_transport=_resolve(transport))
    assert code not in (0, 2)


# --- adversarial-pass hardening (sol/terra, [#958]) ---------------------------------------------

def test_a_lane_slug_with_a_path_separator_is_refused_before_any_path_is_built(monkeypatch,
                                                                              tmp_path, transport):
    """sol HIGH: `session_path()`/the REFUSED path interpolated `lane` with no containment
    check. A `lane` that cannot even be validated must not reach EITHER path -- the REFUSED
    file's own path is built from the same unsafe string."""
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    repo = tmp_path / "repo"
    repo.mkdir()
    written_before = list((transport / "to-browser").iterdir())

    code, receipt = hb.run("../escape", BRANCH, "docs-only", repo,
                          resolve_transport=_resolve(transport))

    assert code == hb.EXIT_INTERNAL
    assert receipt["status"] == "FAILED"
    assert "lane slug" in receipt["reason"]
    assert list((transport / "to-browser").iterdir()) == written_before


def test_head_moving_between_checks_and_publish_refuses_rather_than_publishing(monkeypatch,
                                                                              tmp_path, transport):
    """sol/terra CRITICAL (TOCTOU): checks and the emitted artifacts must attest one immutable
    snapshot. Simulates a HEAD that moves during the self-check window by returning a different
    SHA on the second `_git_head` call (the pre-publish re-verify)."""
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    shas = iter(["1a2b3c4d", "9f9f9f9f"])
    monkeypatch.setattr(hb, "_git_head", lambda repo: next(shas))
    repo = tmp_path / "repo"
    repo.mkdir()

    code, receipt = hb.run(LANE, BRANCH, "docs-only", repo, resolve_transport=_resolve(transport))

    assert code == hb.EXIT_REFUSED
    assert not (transport / "to-browser" / f"LANE-END-{LANE}.md").exists()
    session_path = transport / "to-browser" / f"SESSION-{LANE}.md"
    assert not session_path.exists() or "HANDBACK " not in session_path.read_text(encoding="utf-8")
    refused_path = transport / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md"
    assert "HEAD moved" in refused_path.read_text(encoding="utf-8")


def test_a_malformed_handback_line_writes_no_lane_end_report(monkeypatch, tmp_path, transport):
    """sol/terra HIGH: the LANE-END report must not land before the mergeable lines validate --
    a `code` branch with no reviewer refuses the HANDBACK line, and that must leave nothing
    "clean-looking" behind in the transport."""
    hb = _mod("handback")
    _stub_all_checks_ok(monkeypatch, hb)
    repo = tmp_path / "repo"
    repo.mkdir()

    code, receipt = hb.run(LANE, BRANCH, "code", repo, resolve_transport=_resolve(transport))

    assert code == hb.EXIT_INTERNAL
    assert "HANDBACK line refused" in receipt["reason"]
    assert not (transport / "to-browser" / f"LANE-END-{LANE}.md").exists()


def test_the_cli_does_not_expose_a_base_override():
    """terra CRITICAL: a caller-controlled `--base` could neutralize purity and the ship-gate
    delta outright (`--base HEAD` empties both). A real invocation only ever gets
    `DEFAULT_BASE`; `base` stays a `run()`/check-function parameter for tests."""
    hb = _mod("handback")
    with pytest.raises(SystemExit):
        hb._parser().parse_args(["run", "--lane", LANE, "--branch", BRANCH,
                                 "--class", "docs-only", "--base", "HEAD"])
