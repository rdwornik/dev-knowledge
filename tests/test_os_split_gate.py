"""LANE e2-os-split: non-vacuous coverage gates for Windows-only tests."""
from __future__ import annotations

import ast
import importlib
import os
import operator
import re
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import platform_skip_ratchet as ratchet  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SMOKE_PREFIX = "tests/test_os_split_gate.py::test_windows_smoke_"
_PLATFORM_TERMS = re.compile(
    r"\bos\.name\b|\bsys\.platform\b|\bwinreg\b|\bplatform\.system\b",
    re.IGNORECASE,
)
_PWSH_TERMS = re.compile(r"\bPWSH\b|\bpwsh\b|\bpowershell\b", re.IGNORECASE)
_COMPARE = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.In: lambda left, right: left in right,
    ast.NotIn: lambda left, right: left not in right,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}


def _live_windows_only() -> frozenset[str]:
    from conftest import WINDOWS_ONLY_TESTS

    return WINDOWS_ONLY_TESTS


def _covered(nodeid: str, windows_only_set: frozenset[str]) -> bool:
    nodeid = nodeid.replace("\\", "/")
    module = nodeid.split("::", 1)[0]
    return (
        nodeid in windows_only_set
        or module in windows_only_set
        or f"{module}::<module>" in windows_only_set
    )


def uncovered(
    nodeids: list[str], windows_only_set: frozenset[str], smoke_prefix: str
) -> list[str]:
    return sorted(
        nodeid.replace("\\", "/")
        for nodeid in nodeids
        if not nodeid.replace("\\", "/").startswith(smoke_prefix)
        and not _covered(nodeid, windows_only_set)
    )


def _truth_on_ubuntu(node: ast.expr):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Attribute):
        name = ast.unparse(node)
        if name == "os.name":
            return "posix"
        if name == "sys.platform":
            return "linux"
        return None
    if isinstance(node, ast.Name):
        if node.id == "True":
            return True
        if node.id == "False":
            return False
        return None
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        value = _truth_on_ubuntu(node.operand)
        return None if value is None else not value
    if isinstance(node, ast.BoolOp):
        values = [_truth_on_ubuntu(value) for value in node.values]
        if isinstance(node.op, ast.And):
            if False in values:
                return False
            return True if all(value is True for value in values) else None
        if isinstance(node.op, ast.Or):
            if True in values:
                return True
            return False if all(value is False for value in values) else None
        return None
    if isinstance(node, ast.Compare):
        left = _truth_on_ubuntu(node.left)
        if left is None:
            return None
        for operation, comparator in zip(node.ops, node.comparators):
            right = _truth_on_ubuntu(comparator)
            function = _COMPARE.get(type(operation))
            if right is None or function is None:
                return None
            try:
                if not function(left, right):
                    return False
            except (TypeError, ValueError):
                return None
            left = right
        return True
    return None


def _is_platform_shaped(condition: ast.expr, aliases: dict) -> bool:
    """A condition about the platform, not about a tool being installed.

    pwsh/powershell counts only when it is NOT reached through a tool-presence lookup
    (`shutil.which(...)`, directly or via a module-level alias): ubuntu-latest has pwsh.
    """
    text = ast.unparse(condition)
    for name in ast.walk(condition):
        if isinstance(name, ast.Name) and name.id in aliases:
            text += " " + ast.unparse(aliases[name.id])
    if _PLATFORM_TERMS.search(text):
        return True
    return bool(_PWSH_TERMS.search(text)) and "which(" not in text


def _may_skip_on_ubuntu(condition: ast.expr, aliases: dict | None = None) -> bool:
    return _is_platform_shaped(condition, aliases or {}) and (
        _truth_on_ubuntu(condition) is not False
    )


def _is_call(node: ast.AST, module: str, name: str) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == name
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == module
    )


def _is_pytest_call(node: ast.AST, name: str) -> bool:
    """`pytest.<name>(...)` or a bare/imported `<name>(...)`."""
    return _is_call(node, "pytest", name) or (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    )


def _importorskip(node: ast.AST) -> bool:
    return _is_pytest_call(node, "importorskip") and bool(
        _PLATFORM_TERMS.search(ast.unparse(node))
    )


def _is_skipif(node: ast.AST, aliases: dict) -> bool:
    marker = ratchet._resolve_marker(node, aliases)
    condition = ratchet._skipif_condition(marker) if marker is not None else None
    return condition is not None and _may_skip_on_ubuntu(condition, aliases)


def _pytestmark_skipif(body: list, aliases: dict) -> bool:
    for node in body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "pytestmark"
                   for target in node.targets):
            continue
        values = node.value.elts if isinstance(node.value, (ast.List, ast.Tuple)) else [node.value]
        if any(_is_skipif(value, aliases) for value in values):
            return True
    return False


def _skip_in_platform_branch(root: ast.AST, aliases: dict) -> bool:
    """A skip / importorskip that a platform condition can route to on Ubuntu."""
    for node in ast.walk(root):
        if _importorskip(node):
            return True
        if not isinstance(node, ast.If) or not _is_platform_shaped(node.test, aliases):
            continue
        truth = _truth_on_ubuntu(node.test)
        if truth is True:
            branch = node.body
        elif truth is False:
            branch = node.orelse
        else:
            branch = node.body + node.orelse
        if any(_is_pytest_call(inner, "skip")
               for stmt in branch for inner in ast.walk(stmt)):
            return True
    return False


def _module_level_skip(tree: ast.Module, aliases: dict) -> bool:
    if _pytestmark_skipif(tree.body, aliases):
        return True
    return any(
        _skip_in_platform_branch(node, aliases)
        for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )


def _test_sites(body: list, prefix: tuple, inherited: bool, aliases: dict):
    """(node-id parts, function, class-level skip) for every collected test function."""
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_"):
                yield prefix + (node.name,), node, inherited
        elif isinstance(node, ast.ClassDef):
            class_skip = (
                inherited
                or any(_is_skipif(d, aliases) for d in node.decorator_list)
                or _pytestmark_skipif(node.body, aliases)
            )
            yield from _test_sites(node.body, prefix + (node.name,), class_skip, aliases)


def ubuntu_skipping_tests(source_text: str, module: str) -> list[str]:
    """Test node ids with a platform-conditioned skip that may fire on Ubuntu.

    Sites: module/class `pytestmark` or class decorator, a test decorator, a skip in the
    test body, or a call (one level) to a module-level helper holding such a skip.
    """
    tree = ast.parse(source_text)
    aliases = ratchet._module_assignment_nodes(tree)
    module_skip = _module_level_skip(tree, aliases)
    helpers = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("test_")
        and _skip_in_platform_branch(node, aliases)
    }
    skipped: set[str] = set()
    for parts, function, class_skip in _test_sites(tree.body, (), False, aliases):
        nodeid = "::".join((module, *parts))
        if (
            module_skip
            or class_skip
            or any(_is_skipif(d, aliases) for d in function.decorator_list)
            or _skip_in_platform_branch(function, aliases)
            or any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in helpers
                for node in ast.walk(function)
            )
        ):
            skipped.add(nodeid)
    return sorted(skipped)


def platform_skip_violations(
    source_text: str, module: str, windows_only_set: frozenset[str]
) -> list[str]:
    return [
        nodeid
        for nodeid in ubuntu_skipping_tests(source_text, module)
        if not _covered(nodeid, windows_only_set)
    ]


def _live_test_files() -> list[tuple[str, str]]:
    return [
        (path.relative_to(ROOT).as_posix(), path.read_text(encoding="utf-8"))
        for path in sorted(TESTS.rglob("*.py"))
        if "__pycache__" not in path.parts
    ]


def _live_ubuntu_skips() -> list[str]:
    return sorted(
        nodeid
        for module, text in _live_test_files()
        for nodeid in ubuntu_skipping_tests(text, module)
    )


def _live_platform_skip_violations(windows_only: frozenset[str]) -> list[str]:
    return sorted(
        nodeid
        for module, text in _live_test_files()
        for nodeid in platform_skip_violations(text, module, windows_only)
    )


def _collect(*extra: str) -> list[str]:
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider",
         "-n0", *extra, "tests"],
        cwd=ROOT,
        env={key: value for key, value in os.environ.items()
             if key != "CI_OS_MARKEXPR"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return [
        line.strip().replace("\\", "/")
        for line in completed.stdout.splitlines()
        if line.strip().startswith("tests/") and "::" in line
    ]


@pytest.fixture(scope="module")
def windows_selection() -> list[str]:
    return _collect("-m", "windows_only or windows_smoke")


@pytest.mark.windows_smoke
def test_windows_smoke_import_ci_os_plan():
    importlib.import_module("ci_os_plan")


@pytest.mark.windows_smoke
def test_windows_smoke_import_platform_skip_ratchet():
    importlib.import_module("platform_skip_ratchet")


@pytest.mark.windows_smoke
def test_windows_smoke_import_windows_gate():
    importlib.import_module("windows_gate")


@pytest.mark.windows_smoke
def test_windows_smoke_ci_os_plan_cli_help():
    completed = subprocess.run(
        [sys.executable, str(_SCRIPTS / "ci_os_plan.py"), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_uncovered_finds_selected_tests_without_windows_coverage():
    nodeids = [
        "tests/test_a.py::test_marked",
        "tests/test_b.py::test_module_covered",
        "tests/test_os_split_gate.py::test_windows_smoke_example",
        "tests/test_c.py::test_missing",
    ]
    windows_only = frozenset(
        {"tests/test_a.py::test_marked", "tests/test_b.py::<module>"}
    )

    assert uncovered(nodeids, windows_only, SMOKE_PREFIX) == [
        "tests/test_c.py::test_missing"
    ]


def test_live_windows_marker_selection_is_covered_by_registration(windows_selection):
    registry = _live_windows_only()

    assert windows_selection, "the Windows selection collected nothing"
    assert any(n.startswith(SMOKE_PREFIX) for n in windows_selection)
    assert any(_covered(n, registry) for n in windows_selection)
    assert uncovered(windows_selection, registry, SMOKE_PREFIX) == []


def test_the_windows_selection_equals_registry_expansion_plus_smoke(windows_selection):
    from conftest import _windows_only_covered

    registry = _live_windows_only()
    everything = _collect()
    expected = {
        n for n in everything
        if n.startswith(SMOKE_PREFIX) or _windows_only_covered(n, registry)
    }
    dead = sorted(
        entry for entry in registry
        if not any(_windows_only_covered(n, frozenset({entry})) for n in everything)
    )

    assert dead == [], f"registry entries matching no collected test: {dead}"
    assert set(windows_selection) == expected, (
        f"only selected: {sorted(set(windows_selection) - expected)}; "
        f"only expected: {sorted(expected - set(windows_selection))}"
    )


def test_unmarked_ubuntu_skipif_is_a_platform_skip_violation():
    source = """
import os
import pytest

@pytest.mark.skipif(os.name != "nt", reason="needs Windows")
def test_windows_feature():
    pass
"""

    assert platform_skip_violations(source, "tests/test_sample.py", frozenset()) == [
        "tests/test_sample.py::test_windows_feature"
    ]


def test_registered_ubuntu_skipif_is_not_a_platform_skip_violation():
    source = """
import os
import pytest

@pytest.mark.skipif(os.name != "nt", reason="needs Windows")
def test_windows_feature():
    pass
"""

    assert platform_skip_violations(
        source,
        "tests/test_sample.py",
        frozenset({"tests/test_sample.py::test_windows_feature"}),
    ) == []


def test_posix_only_skipif_is_not_a_platform_skip_violation():
    source = """
import sys
import pytest

@pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only behavior")
def test_posix_feature():
    pass
"""

    assert platform_skip_violations(source, "tests/test_sample.py", frozenset()) == []


def test_unknown_powershell_skip_condition_may_skip_on_ubuntu():
    source = """
import pytest

@pytest.mark.skipif(not PWSH, reason="needs PowerShell")
def test_shell_feature():
    pass
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == [
        "tests/test_sample.py::test_shell_feature"
    ]


def test_live_ubuntu_skips_are_windows_marked_and_registry_is_nonempty():
    windows_only = _live_windows_only()

    assert windows_only
    assert _live_platform_skip_violations(windows_only) == []


def test_removing_a_covering_windows_entry_exposes_a_live_skip_violation():
    windows_only = _live_windows_only()
    live_skips = _live_ubuntu_skips()
    covering_entries = sorted(
        entry
        for entry in windows_only
        if any(
            _covered(nodeid, frozenset({entry}))
            for nodeid in live_skips
        )
    )

    assert covering_entries, "no registered entry covers a live Ubuntu-skipping test"
    reduced = windows_only - {covering_entries[0]}
    assert _live_platform_skip_violations(reduced)


def test_the_helper_mediated_8dot3_skip_is_found_and_its_entry_is_load_bearing():
    witness = "tests/test_scope_guard.py::test_windows_8dot3_short_form_is_refused"
    windows_only = _live_windows_only()

    assert witness in _live_ubuntu_skips()
    assert witness in windows_only
    assert witness in _live_platform_skip_violations(windows_only - {witness})


def test_a_pwsh_tool_presence_skip_is_not_a_platform_skip():
    source = """
import shutil
import pytest

PWSH = shutil.which("pwsh")
needs_pwsh = pytest.mark.skipif(PWSH is None, reason="needs pwsh")

@pytest.mark.skipif(shutil.which("pwsh") is None, reason="needs pwsh")
def test_direct_lookup():
    pass

@needs_pwsh
def test_alias_lookup():
    pass
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == []


def test_a_pwsh_condition_that_also_names_the_platform_is_still_a_platform_skip():
    source = """
import os
import pytest

@pytest.mark.skipif(not PWSH or os.name != "nt", reason="Windows pwsh")
def test_windows_pwsh():
    pass
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == [
        "tests/test_sample.py::test_windows_pwsh"
    ]


def test_a_class_level_skipif_covers_every_test_method():
    source = """
import os
import pytest

@pytest.mark.skipif(os.name != "nt", reason="Windows")
class TestDecorated:
    def test_one(self):
        pass

    def test_two(self):
        pass

class TestMarked:
    pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows")

    def test_three(self):
        pass

class TestPlain:
    def test_four(self):
        pass
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == [
        "tests/test_sample.py::TestDecorated::test_one",
        "tests/test_sample.py::TestDecorated::test_two",
        "tests/test_sample.py::TestMarked::test_three",
    ]


def test_a_helper_holding_a_platform_skip_makes_its_caller_a_skip_site():
    source = """
import os
import pytest

def _needs_windows():
    if os.name != "nt":
        pytest.skip("Windows only")

def _posix_branch():
    if os.name == "nt":
        pytest.skip("not here")

def test_calls_the_helper():
    _needs_windows()

def test_calls_a_harmless_helper():
    _posix_branch()
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == [
        "tests/test_sample.py::test_calls_the_helper"
    ]


def test_bare_and_imported_skip_and_importorskip_are_detected():
    source = """
import os
from pytest import importorskip, skip

def test_bare_skip():
    if os.name != "nt":
        skip("Windows only")

def test_bare_importorskip():
    importorskip("winreg")
"""

    assert ubuntu_skipping_tests(source, "tests/test_sample.py") == [
        "tests/test_sample.py::test_bare_importorskip",
        "tests/test_sample.py::test_bare_skip",
    ]
