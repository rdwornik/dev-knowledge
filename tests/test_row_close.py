"""Tests for `scripts/row_close.py` -- the integrator's row-close step (batch B2-W1, lane W1-1).

Contract: `LANE-B2-W1-b2-row-close-on-merge.md` Done-contract items 1-5. Every test here was
written first and is RED on `e67f27ac` (the module does not exist there).

Fixtures only (the contract's Do-not): every close runs on a tmp repo with its own `tasks/`
tree, a real git history and a closed merge receipt written through `merge_receipt.Receipt`.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import gen_task_tree as gtt
import merge_receipt as mr
import row_close as rc

SLUG = "b2-row-close-on-merge"
LANE_SESSION = "684b23dd"
INTEGRATOR_SESSION = "1463b888"
TEST_ID = "tests/test_widget.py::test_widget_works"

_TWO_THEMES = (
    "# T\n\n## [E1] One\n\n### [S1] Story\n- [#1] [P1][S] **A** — b\n"
    "\n## [E2] Two\n\n### [S2] Other\n- [#2] [P2][M] **B** — b\n"
)

CONTRACT = (
    "# LANE b2-row-close-on-merge — x\n\n"
    "**Rows:** closes — [#1]; related, not closed by this lane — [#2], `[#976]`.\n\n"
    "## Value\nv\n"
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


class Fixture:
    def __init__(self, root: Path):
        self.repo = root / "repo"
        self.repo.mkdir()
        _git(self.repo, "init", "-q", "-b", "main")
        _git(self.repo, "config", "user.email", "t@example.invalid")
        _git(self.repo, "config", "user.name", "t")
        _git(self.repo, "config", "commit.gpgsign", "false")
        (self.repo / "tests").mkdir()
        (self.repo / "tests" / "test_widget.py").write_text(
            "class TestGroup:\n    def test_nested(self):\n        pass\n\n\n"
            "def test_widget_works():\n    assert True\n\n\n"
            "@pytest.mark.parametrize(\"x\", [1])\ndef test_param(x):\n    assert x\n", encoding="utf-8")
        self.source = self.repo / "BACKLOG.md"
        self.source.write_bytes(_TWO_THEMES.encode("utf-8"))
        self.tasks = self.repo / "tasks"
        gtt.write_tree(gtt.parse_backlog(_TWO_THEMES), self.tasks)
        gtt.main(["--emit-source", "--source", str(self.source), "--out", str(self.tasks)])
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "merge")
        self.merge_sha = _git(self.repo, "rev-parse", "HEAD")
        _git(self.repo, "update-ref", "refs/remotes/origin/main", self.merge_sha)
        self.write_receipt(self.merge_sha)

    def write_receipt(self, merge_sha, *, closed="2026-10-04T10:00:00+00:00", slug=SLUG):
        receipt = mr.Receipt(slug=slug, batch="B2-W1", opened="2026-10-04T09:00:00+00:00",
                             host="h", concurrent_seats=0, merge_sha=merge_sha, closed=closed)
        ledger = self.repo / mr.LEDGER_RELPATH
        ledger.parent.mkdir(parents=True, exist_ok=True)
        with ledger.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(receipt.to_dict(), sort_keys=True) + "\n")

    def gh(self, *, head_sha=None, event="push", status="completed", conclusion="success"):
        wanted = head_sha or self.merge_sha

        def run(run_id: str) -> dict:
            return {"headSha": wanted, "event": event, "status": status,
                    "conclusion": conclusion}
        return run

    def snapshot(self) -> dict[str, bytes]:
        return {str(p.relative_to(self.repo)): p.read_bytes()
                for p in sorted(self.tasks.rglob("*")) if p.is_file()}

    def close(self, **over):
        kwargs = dict(contract_text=CONTRACT, slug=SLUG, ci_run="123456", tests=[TEST_ID],
                      caller_session=INTEGRATOR_SESSION, lane_session=LANE_SESSION,
                      cwd=self.repo, gh=self.gh())
        kwargs.update(over)
        return rc.close_for_merge(self.repo, **kwargs)


@pytest.fixture
def fx(tmp_path):
    return Fixture(tmp_path)


def _row_file(fx: Fixture, task_id: int) -> Path:
    return next(p for p in fx.tasks.iterdir() if p.name.startswith(f"{task_id}-"))


# --- item 1: the contract names its rows --------------------------------------------------

def test_parse_a_contract_with_no_rows_line_yields_no_ids_and_a_refusal():
    parsed = rc.parse_rows_line("# LANE x\n\n## Value\nnothing about rows\n")
    assert parsed.closes == ()
    assert parsed.refusal and "**Rows:**" in parsed.refusal


def test_parse_this_batchs_contract_shape_yields_the_closes_ids_and_ignores_related():
    parsed = rc.parse_rows_line(CONTRACT)
    assert parsed.refusal is None
    assert parsed.closes == (1,)
    assert parsed.related == (2, 976)


def test_parse_closes_none_is_a_present_line_with_no_ids():
    parsed = rc.parse_rows_line(
        "**Rows:** closes — none filed for this requirement (the order is its source); "
        "related, not closed by this lane — `[#519]`, `[#730]`.\n")
    assert parsed.refusal is None
    assert parsed.closes == ()
    assert parsed.related == (519, 730)


def test_parse_reads_several_closed_ids_in_order():
    parsed = rc.parse_rows_line("**Rows:** closes — [#12], `[#7]`; related — [#3]\n")
    assert parsed.closes == (12, 7)


def test_the_lane_contract_template_carries_the_rows_line():
    template = (Path(__file__).resolve().parent.parent / "templates"
                / "lane-contract-template.md").read_text(encoding="utf-8")
    parsed = rc.parse_rows_line(template)
    assert parsed.refusal is None


# --- items 2 + 3: the close, and the view -------------------------------------------------

def test_the_named_row_reads_open_before_and_closed_after_the_merge(fx):
    """The order's own RED test: on a fixture merge the named row still reads OPEN."""
    assert gtt.frontmatter_status(_row_file(fx, 1).read_text(encoding="utf-8")) != "closed"
    assert fx.close() == [1]
    text = _row_file(fx, 1).read_bytes().decode("utf-8")
    assert gtt.frontmatter_status(text) == "closed"
    body = gtt.extract_body(text)
    assert f"evidence {fx.merge_sha}" in body
    assert "CI run 123456" in body
    assert TEST_ID in body


def test_the_closed_row_leaves_the_manifest_and_the_regenerated_view(fx):
    fx.close()
    manifest = json.loads((fx.tasks / "manifest.json").read_bytes().decode("utf-8"))
    assert all(n.get("task") != 1 for n in manifest["nodes"])
    assert any(n.get("task") == 2 for n in manifest["nodes"]), "the related row stays open"
    assert gtt.main(["--emit-source", "--source", str(fx.source), "--out", str(fx.tasks)]) == 0
    view = fx.source.read_text(encoding="utf-8")
    assert "[#1]" not in view
    assert "[#2]" in view
    assert gtt.frontmatter_status(_row_file(fx, 1).read_text(encoding="utf-8")) == "closed"


def test_a_contract_that_closes_no_row_is_a_clean_no_op(fx):
    before = fx.snapshot()
    contract = "**Rows:** closes — none; related, not closed by this lane — [#2]\n"
    assert fx.close(contract_text=contract) == []
    assert fx.snapshot() == before


# --- item 4: a row with no evidence is never closed ---------------------------------------

def _refuses(fx: Fixture, **over):
    before = fx.snapshot()
    with pytest.raises(rc.RowCloseRefusal):
        fx.close(**over)
    assert fx.snapshot() == before, "a refusal leaves the row files and manifest byte-identical"


def test_refuses_a_contract_with_no_rows_line(fx):
    _refuses(fx, contract_text="# LANE x\nno rows line\n")


def test_refuses_when_the_receipt_is_missing(fx):
    _refuses(fx, slug="some-other-lane")


def test_refuses_when_the_receipt_is_not_closed(tmp_path):
    fx = Fixture(tmp_path)
    (fx.repo / mr.LEDGER_RELPATH).unlink()
    fx.write_receipt(fx.merge_sha, closed=None)
    _refuses(fx)


def test_refuses_when_the_receipt_names_no_merge_sha(tmp_path):
    fx = Fixture(tmp_path)
    (fx.repo / mr.LEDGER_RELPATH).unlink()
    fx.write_receipt(None)
    _refuses(fx)


def test_refuses_a_merge_sha_that_does_not_resolve(tmp_path):
    fx = Fixture(tmp_path)
    (fx.repo / mr.LEDGER_RELPATH).unlink()
    fx.write_receipt("deadbeef" * 5)
    _refuses(fx)


def test_refuses_a_merge_sha_not_reachable_from_main(tmp_path):
    fx = Fixture(tmp_path)
    _git(fx.repo, "checkout", "-q", "-b", "side")
    (fx.repo / "side.txt").write_text("x", encoding="utf-8")
    _git(fx.repo, "add", "-A")
    _git(fx.repo, "commit", "-q", "-m", "side")
    side = _git(fx.repo, "rev-parse", "HEAD")
    (fx.repo / mr.LEDGER_RELPATH).unlink()
    fx.write_receipt(side)
    _refuses(fx, gh=fx.gh(head_sha=side))


def test_refuses_a_ci_run_for_a_different_sha(fx):
    _refuses(fx, gh=fx.gh(head_sha="1" * 40))


def test_refuses_a_schedule_run(fx):
    _refuses(fx, gh=fx.gh(event="schedule"))


def test_refuses_an_in_progress_run(fx):
    _refuses(fx, gh=fx.gh(status="in_progress", conclusion=None))


def test_refuses_a_cancelled_run(fx):
    _refuses(fx, gh=fx.gh(conclusion="cancelled"))


def test_refuses_a_timed_out_run(fx):
    _refuses(fx, gh=fx.gh(conclusion="timed_out"))


def test_a_completed_failure_run_is_recorded_not_refused(fx):
    """A red present on both sides is FLAGGED by the merge receipt, never refused (common
    rules section 3); the run is the evidence, its conclusion is recorded."""
    assert fx.close(gh=fx.gh(conclusion="failure")) == [1]
    assert "(failure)" in gtt.extract_body(_row_file(fx, 1).read_text(encoding="utf-8"))


def test_refuses_when_gh_is_unreadable(fx):
    def broken(run_id):
        raise FileNotFoundError("gh")
    _refuses(fx, gh=broken)


def test_refuses_a_non_numeric_ci_run(fx):
    _refuses(fx, ci_run="latest")


def test_refuses_no_ci_run(fx):
    _refuses(fx, ci_run=None)


def test_refuses_no_named_tests(fx):
    _refuses(fx, tests=[])


def test_refuses_a_test_file_absent_at_the_merge_sha(fx):
    _refuses(fx, tests=["tests/test_nope.py::test_x"])


def test_refuses_a_test_function_absent_at_the_merge_sha(fx):
    _refuses(fx, tests=["tests/test_widget.py::test_missing"])


def test_a_class_nested_and_a_parametrised_function_id_resolves(fx):
    assert fx.close(tests=["tests/test_widget.py::TestGroup::test_nested",
                           "tests/test_widget.py::test_param"]) == [1]


def test_refuses_any_parameter_selector_even_on_a_parametrised_test(fx):
    """A case id cannot be proven without collecting; the function id is what is recorded."""
    _refuses(fx, tests=["tests/test_widget.py::test_param[nonexistent]"])
    _refuses(fx, tests=["tests/test_widget.py::test_param[1]"])


def test_refuses_a_row_that_is_not_open_and_writes_none_of_the_batch(fx):
    contract = "**Rows:** closes — [#1], [#9]; related — none\n"
    _refuses(fx, contract_text=contract)


# --- item 5: a lane cannot close its own row ----------------------------------------------

def test_refuses_when_run_from_inside_the_lanes_own_worktree(fx):
    wt = fx.repo / ".claude" / "worktrees" / SLUG
    wt.mkdir(parents=True)
    _refuses(fx, cwd=wt)


def test_refuses_when_the_caller_is_the_implementing_session(fx):
    _refuses(fx, caller_session=LANE_SESSION)


def test_refuses_when_the_caller_is_unknown(fx):
    _refuses(fx, caller_session=None)


def test_a_different_session_in_the_primary_checkout_closes(fx):
    assert fx.close(caller_session=INTEGRATOR_SESSION, cwd=fx.repo) == [1]


# --- the CLI ------------------------------------------------------------------------------

def test_cli_closes_and_exits_zero_then_refuses_a_second_close_non_zero(fx, tmp_path, monkeypatch):
    contract = tmp_path / "LANE-X.md"
    contract.write_text(CONTRACT, encoding="utf-8")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", INTEGRATOR_SESSION + "-rest")
    monkeypatch.chdir(fx.repo)  # the integrator runs from the primary checkout, not a lane worktree
    root = tmp_path / "prompts"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-cc" / f"LANE-X.CLAIMED-{LANE_SESSION}").write_text("", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(root))
    argv = ["close", "--repo-root", str(fx.repo), "--contract", str(contract), "--slug", SLUG,
            "--ci-run", "123456", "--test", TEST_ID]
    assert rc.main(argv, gh=fx.gh()) == 0
    before = fx.snapshot()
    assert rc.main(argv, gh=fx.gh()) != 0
    assert fx.snapshot() == before


# --- review 1 (Codex terra) fixes ---------------------------------------------------------

def test_parse_refuses_ids_outside_a_closes_clause():
    for line in ("**Rows:** notes [#1]\n", "**Rows:** related — [#1]\n", "**Rows:** [#1]\n"):
        parsed = rc.parse_rows_line(line)
        assert parsed.closes == () and parsed.refusal, line


def test_refuses_a_malformed_rows_line_and_closes_nothing(fx):
    _refuses(fx, contract_text="**Rows:** notes [#1]\n")


def test_refuses_a_function_named_under_the_wrong_class(fx):
    _refuses(fx, tests=["tests/test_widget.py::TestGroup::test_widget_works"])


def test_refuses_a_class_method_named_as_a_module_function(fx):
    _refuses(fx, tests=["tests/test_widget.py::test_nested"])


def test_refuses_a_parameter_selector_on_an_unparametrised_test(fx):
    _refuses(fx, tests=["tests/test_widget.py::test_widget_works[a-b]"])


def _marker_env(tmp_path, monkeypatch, marker_session):
    root = tmp_path / "prompts"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-cc" / f"LANE-X.CLAIMED-{marker_session}").write_text("", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(root))


def _cli(fx, tmp_path, monkeypatch, caller, *extra):
    contract = tmp_path / "LANE-X.md"
    contract.write_text(CONTRACT, encoding="utf-8")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", caller)
    monkeypatch.chdir(fx.repo)
    argv = ["close", "--repo-root", str(fx.repo), "--contract", str(contract), "--slug", SLUG,
            "--ci-run", "123456", "--test", TEST_ID, *extra]
    return rc.main(argv, gh=fx.gh())


def test_the_claim_marker_names_the_lane_when_no_flag_is_given(fx, tmp_path, monkeypatch):
    _marker_env(tmp_path, monkeypatch, LANE_SESSION)
    before = fx.snapshot()
    assert _cli(fx, tmp_path, monkeypatch, LANE_SESSION) != 0
    assert fx.snapshot() == before


def test_there_is_no_lane_session_flag_to_forge(fx, tmp_path, monkeypatch):
    """The implementing session comes from the contract's claim marker alone."""
    _marker_env(tmp_path, monkeypatch, LANE_SESSION)
    with pytest.raises(SystemExit):
        _cli(fx, tmp_path, monkeypatch, INTEGRATOR_SESSION, "--lane-session", "feedface")


def test_no_claim_marker_means_no_close(fx, tmp_path, monkeypatch):
    """With no marker the implementing session is unknown, so the caller cannot prove it is
    not the lane: refused, nothing written."""
    root = tmp_path / "prompts"
    (root / "to-cc").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(root))
    before = fx.snapshot()
    assert _cli(fx, tmp_path, monkeypatch, INTEGRATOR_SESSION) != 0
    assert fx.snapshot() == before


def test_the_rows_line_refuses_a_suffix_that_is_not_a_related_clause():
    for line in ("**Rows:** closes — [#1]; notes [#2]\n", "**Rows:** closes - [#1]; [#2]\n"):
        parsed = rc.parse_rows_line(line)
        assert parsed.closes == () and parsed.refusal, line
    ok = rc.parse_rows_line("**Rows:** closes — [#1];\n")
    assert ok.refusal is None and ok.closes == (1,)


def test_the_integrator_closes_when_the_marker_names_a_different_session(fx, tmp_path,
                                                                         monkeypatch):
    _marker_env(tmp_path, monkeypatch, LANE_SESSION)
    assert _cli(fx, tmp_path, monkeypatch, INTEGRATOR_SESSION + "-x") == 0
