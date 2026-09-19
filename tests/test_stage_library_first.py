"""Stage 6 (library-first) REFUSES a sentence, and accepts only a command and its output.

RED-FIRST. DECLARE-SPINE-AND-B3 §6: `library-first` "accepts ONLY a SEARCH COMMAND AND ITS
OUTPUT. A sentence is an empty field." Prose failed on the architect three times in one session,
so the field is enforced by the runner rather than by instruction. Every refusal test here is a
removal test: it fails the moment the refusal it names stops raising. The passing-path tests
exist so a checker cannot pass its own trip-test by refusing everything.

The deptry leg is exercised against a throwaway project in `tmp_path`, because the hub's own
report is a MEASUREMENT (recorded in the handback), not a fixture.
"""
from __future__ import annotations

import textwrap

import pytest
from click.testing import CliRunner

import stage_library_first as slf

_GOOD = textwrap.dedent("""\
    # contract

    - **library-first:**

    ```
    $ rg -n "toposort" scripts/
    scripts/graph_store.py:12:import rustworkx
    ```
    - **rejected-alternatives:** hand-written toposort
    """)


def _contract(field_body: str) -> str:
    return f"# contract\n\n- **library-first:** {field_body}\n\n- **anti-claims:** none\n"


def test_a_sentence_in_the_field_is_refused():
    text = _contract("We checked the ecosystem and no library covers this, so we build it.")
    with pytest.raises(slf.StageRefusal, match="stage 6"):
        slf.check_contract(text, site="c.md")


def test_an_empty_field_is_refused():
    with pytest.raises(slf.StageRefusal, match="empty"):
        slf.check_contract(_contract(""), site="c.md")


def test_a_contract_with_no_field_at_all_is_refused():
    with pytest.raises(slf.StageRefusal, match="no `library-first`"):
        slf.check_contract("# contract\n\n- **prior-art:** something\n", site="c.md")


def test_a_command_with_no_output_is_refused():
    body = "\n\n```\n$ rg -n toposort scripts/\n```\n"
    with pytest.raises(slf.StageRefusal, match="output"):
        slf.check_contract(_contract(body), site="c.md")


def test_a_prompt_line_whose_head_is_not_a_command_is_refused():
    """A sentence dressed as a command: `$ we looked and found nothing`."""
    body = "\n\n```\n$ we looked and found nothing\nnothing\n```\n"
    with pytest.raises(slf.StageRefusal, match="command"):
        slf.check_contract(_contract(body), site="c.md")


def test_a_command_and_its_output_passes():
    assert slf.check_contract(_GOOD, site="c.md") == 1


def test_a_backticked_inline_command_without_output_is_still_a_sentence():
    with pytest.raises(slf.StageRefusal):
        slf.check_contract(_contract("`rg -n toposort scripts/` found nothing"), site="c.md")


def test_the_refusal_names_a_way_forward():
    with pytest.raises(slf.StageRefusal) as exc:
        slf.check_contract(_contract("no library"), site="c.md")
    assert exc.value.remedy
    assert "REFUSED" in str(exc.value)


def test_cli_exits_1_on_a_sentence_and_0_on_a_command_and_output(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text(_contract("no library covers this"), encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text(_GOOD, encoding="utf-8")
    runner = CliRunner()
    assert runner.invoke(slf.cli, ["check", str(bad)]).exit_code == 1
    assert runner.invoke(slf.cli, ["check", str(good)]).exit_code == 0


# --- the deptry leg -----------------------------------------------------------------------------

def _project(tmp_path, *, imports: str, declared: str):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "t"\nversion = "0"\nrequires-python = ">=3.12"\n'
        f"dependencies = [{declared}]\n",
        encoding="utf-8",
    )
    (tmp_path / "mod.py").write_text(imports, encoding="utf-8")
    return tmp_path


def test_deptry_refuses_an_import_that_no_dependency_declares(tmp_path):
    root = _project(tmp_path, imports="import notdeclaredpkg\n", declared="")
    with pytest.raises(slf.StageRefusal, match="DEP001"):
        slf.run_deptry(root)


def test_deptry_passes_a_project_whose_imports_are_declared(tmp_path):
    root = _project(tmp_path, imports="import json\n", declared="")
    assert slf.run_deptry(root) == 0


def test_deptry_reads_the_target_roots_config_not_the_callers(tmp_path):
    """Codex terra P1: the subprocess kept the caller's cwd, so this hub's `[tool.deptry]`
    waiver for `structlog` silently applied to a foreign root. Run from the hub, a target project
    that imports structlog undeclared must still be refused."""
    root = _project(tmp_path, imports="import structlog\n", declared="")
    with pytest.raises(slf.StageRefusal, match="DEP001"):
        slf.run_deptry(root)
