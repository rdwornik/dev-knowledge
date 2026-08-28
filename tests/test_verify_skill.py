"""[#127] — the `verify` skill's failure-output contract.

Done-when: a seeded failure produces the file/expected/received/directive block, and
success stays 3-line. The enrichment adds a semantic, machine-distinguishable exit
code so an iterate-until-green loop gets an anti-retry-loop signal.

The pure extractors are tested against SEEDED tool output rather than by running the
real pytest/ruff — running the suite from inside the suite is both slow and circular.
The 3-line success shape is proven by driving main() with every subprocess stubbed.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_VERIFY = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "verify" / "verify.py"


def _load():
    spec = importlib.util.spec_from_file_location("verify_skill", _VERIFY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v = _load()


# --- the four required fields, per check ------------------------------------

_REQUIRED = ("file", "expected", "received", "directive")

_PYTEST_OUT = """\
=================================== FAILURES ===================================
_______________________________ test_widget_count ______________________________
tests/test_widget.py:42: in test_widget_count
    assert count == 3
E   assert 2 == 3
=========================== short test summary info ============================
FAILED tests/test_widget.py::test_widget_count - assert 2 == 3
"""

_RUFF_OUT = """\
scripts/audit.py:118:5: F401 [*] `os` imported but unused
Found 1 error.
"""

_GIT_OUT = " M scripts/audit.py\n?? notes.txt\n"


@pytest.mark.parametrize("fields", [
    v.pytest_failure(_PYTEST_OUT),
    v.ruff_failure(_RUFF_OUT),
    v.git_failure(_GIT_OUT),
])
def test_every_failure_carries_all_four_fields(fields):
    for key in _REQUIRED:
        assert key in fields and fields[key], f"{key} missing or empty"


def test_pytest_block_names_the_failing_test_and_the_assertion():
    f = v.pytest_failure(_PYTEST_OUT)
    assert f["file"] == "tests/test_widget.py::test_widget_count"
    assert f["received"] == "assert 2 == 3"
    assert "re-run" in f["directive"]


def test_ruff_block_names_file_line_col_and_rule():
    f = v.ruff_failure(_RUFF_OUT)
    assert f["file"] == "scripts/audit.py:118:5"
    assert f["received"].startswith("F401")
    assert "ruff check --fix" in f["directive"]


def test_git_block_names_a_path_and_counts_the_rest():
    f = v.git_failure(_GIT_OUT)
    assert f["file"] == "scripts/audit.py (+1 more)"
    assert f["received"] == "2 uncommitted path(s)"


def test_unparseable_output_still_yields_a_block_not_a_crash():
    """A checker that cannot read its own input must degrade, never throw."""
    for fields in (v.pytest_failure("total garbage"), v.ruff_failure("total garbage")):
        for key in _REQUIRED:
            assert fields[key]
        assert "unattributed" in fields["file"]


def test_render_block_has_all_four_labels():
    out = v.render_block("pytest", v.pytest_failure(_PYTEST_OUT))
    for label in ("file", "expected", "received", "directive"):
        assert f"{label:<10}:" in out or f"{label}      :" in out or label in out


# --- semantic exit codes (the anti-retry-loop signal) -----------------------

def test_exit_codes_are_distinct_and_composable():
    assert v.exit_code([]) == 0
    assert v.exit_code(["pytest"]) == v.EXIT_PYTEST == 2
    assert v.exit_code(["ruff"]) == v.EXIT_RUFF == 4
    assert v.exit_code(["git"]) == v.EXIT_GIT == 8
    # composability is the point: a loop seeing 6 knows BOTH are red
    assert v.exit_code(["pytest", "ruff"]) == 6
    assert v.exit_code(["pytest", "ruff", "git"]) == 14


def test_each_single_failure_code_identifies_exactly_one_check():
    seen = {v.exit_code([n]) for n in ("pytest", "ruff", "git")}
    assert len(seen) == 3, "codes must be machine-distinguishable"


# --- shape: success is 3 lines, failure adds the block ----------------------

def _drive(monkeypatch, pytest_rc, ruff_rc, git_out):
    calls = {"pytest": (pytest_rc, _PYTEST_OUT if pytest_rc else ""),
             "ruff": (ruff_rc, _RUFF_OUT if ruff_rc else ""),
             "git": (0, git_out)}

    def fake_run(cmd):
        if "pytest" in cmd:
            return calls["pytest"]
        if "ruff" in cmd:
            return calls["ruff"]
        return calls["git"]

    monkeypatch.setattr(v, "run", fake_run)
    return fake_run


def test_success_output_is_exactly_three_lines(monkeypatch, capsys):
    """[#127] Done-when, second half: success stays the 3-line compact form."""
    _drive(monkeypatch, 0, 0, "")
    code = v.main()
    out = capsys.readouterr().out
    assert code == 0
    assert out.strip().splitlines() == ["pytest : PASS", "ruff   : PASS", "git    : PASS"]


def test_seeded_failure_produces_the_actionable_block(monkeypatch, capsys):
    """[#127] Done-when, first half — seeded, per the row."""
    _drive(monkeypatch, 1, 0, "")
    code = v.main()
    out = capsys.readouterr().out
    assert code == v.EXIT_PYTEST
    assert "--- Actionable ---" in out
    for label in ("file", "expected", "received", "directive"):
        assert label in out
    assert "tests/test_widget.py::test_widget_count" in out
    # the 3-line header survives ahead of the block
    assert out.startswith("pytest : FAIL\nruff   : PASS\ngit    : PASS\n")


def test_two_failures_report_both_blocks_and_a_composed_code(monkeypatch, capsys):
    _drive(monkeypatch, 1, 1, "")
    code = v.main()
    out = capsys.readouterr().out
    assert code == v.EXIT_PYTEST + v.EXIT_RUFF == 6
    assert out.count("directive :") == 2
    assert "exit 6 =" in out


def test_dirty_tree_alone_fails_with_the_git_code(monkeypatch, capsys):
    _drive(monkeypatch, 0, 0, _GIT_OUT)
    code = v.main()
    out = capsys.readouterr().out
    assert code == v.EXIT_GIT
    assert "clean working tree" in out
