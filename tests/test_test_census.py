"""RED tests for scripts/test_census.py (module does not exist yet)."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures" / "census"


@pytest.fixture(scope="module")
def census():
    spec = importlib.util.spec_from_file_location("test_census", REPO / "scripts" / "test_census.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def src(name):
    return (FIX / name).read_text()


# ---- no_outcome shapes -------------------------------------------------

@pytest.mark.parametrize(
    "fixture,func,cls,expected",
    [
        ("shape_assert_free.py.txt", "test_runs", None, True),
        ("shape_mock_only.py.txt", "test_mock_only", None, True),
        ("shape_unittest_assert.py.txt", "test_value", "TestX", False),
        ("shape_helper_assert.py.txt", "test_helper", None, False),
        ("shape_pytest_raises.py.txt", "test_raises", None, False),
        ("shape_returncode.py.txt", "test_cli", None, False),
        ("shape_real_assert.py.txt", "test_real", None, False),
    ],
)
def test_no_outcome_shapes(census, fixture, func, cls, expected):
    res = census.no_outcome(src(fixture), func, cls)
    assert set(res) == {"no_outcome", "reason"}
    assert res["no_outcome"] is expected
    assert isinstance(res["reason"], str) and res["reason"]


def test_no_outcome_unittest_returncode(census):
    code = (
        "import unittest, subprocess\n"
        "class TestR(unittest.TestCase):\n"
        "    def test_rc(self):\n"
        "        r = subprocess.run(['true'])\n"
        "        self.assertEqual(r.returncode, 0)\n"
    )
    assert census.no_outcome(code, "test_rc", "TestR")["no_outcome"] is False


def test_no_outcome_pytest_warns(census):
    code = "import pytest\ndef test_w():\n    with pytest.warns(UserWarning):\n        f()\n"
    assert census.no_outcome(code, "test_w")["no_outcome"] is False


def test_no_outcome_mock_only_assert_on_mock_attr(census):
    code = (
        "from unittest.mock import MagicMock\n"
        "def test_m():\n    m = MagicMock()\n    m.run()\n    m.run.assert_called_with()\n"
    )
    assert census.no_outcome(code, "test_m")["no_outcome"] is True


def test_no_outcome_mock_plus_real_assert_is_outcome(census):
    code = (
        "from unittest.mock import MagicMock\n"
        "def test_m():\n    m = MagicMock()\n    m()\n    m.assert_called_once()\n    assert f() == 1\n"
    )
    assert census.no_outcome(code, "test_m")["no_outcome"] is False


def test_no_outcome_helper_without_assert_is_no_outcome(census):
    code = "def _h(x):\n    return x\n\ndef test_a():\n    _h(1)\n"
    assert census.no_outcome(code, "test_a")["no_outcome"] is True


# ---- classify ----------------------------------------------------------

def T(edges, asserts=("a",), parametrized=False, source="def t(): pass"):
    return {"edges": edges, "source": source, "asserts": list(asserts), "parametrized": parametrized}


def labels(census, tests, dead=frozenset(), files=frozenset(), mutmut=None):
    rows = census.classify(tests, set(dead), set(files), mutmut)
    return {r["id"]: r["classes"] for r in rows}


def test_classify_shape_and_sorted(census):
    tests = {"t/b": T({"m.py": [1]}), "t/a": T({"m.py": [1]})}
    rows = census.classify(tests, set(), {"m.py"}, None)
    assert [r["id"] for r in rows] == ["t/a", "t/b"]
    for r in rows:
        assert set(r) == {"id", "classes", "evidence"}
        assert r["classes"] == sorted(r["classes"])
        assert set(r["evidence"]) == set(r["classes"])


def test_orphan_all_dead(census):
    got = labels(census, {"t": T({"d1.py": [1], "d2.py": [2]})}, dead={"d1.py", "d2.py"}, files={"d1.py", "d2.py"})
    assert got["t"] == ["ORPHAN", "UNKNOWN"]


def test_orphan_missing_module(census):
    got = labels(census, {"t": T({"gone.py": [1]})}, files={"m.py"})
    assert got["t"] == ["ORPHAN", "UNKNOWN"]


def test_orphan_mixed_dead_and_missing(census):
    got = labels(census, {"t": T({"d.py": [1], "gone.py": [1]})}, dead={"d.py"}, files={"d.py"})
    assert got["t"] == ["ORPHAN", "UNKNOWN"]


def test_not_orphan_mixed_edges(census):
    got = labels(census, {"t": T({"d.py": [1], "live.py": [1]})}, dead={"d.py"}, files={"d.py", "live.py"})
    assert got["t"] == ["UNKNOWN"]


def test_not_orphan_no_edges(census):
    assert labels(census, {"t": T({})}, files={"m.py"})["t"] == ["UNKNOWN"]


def test_duplicate_strict_subset_same_asserts(census):
    tests = {
        "small": T({"m.py": [1, 2]}, ["x==1"]),
        "big": T({"m.py": [1, 2, 3]}, ["x==1"]),
    }
    rows = {r["id"]: r for r in census.classify(tests, set(), {"m.py"}, None)}
    assert rows["small"]["classes"] == ["DUPLICATE", "UNKNOWN"]
    assert "big" in rows["small"]["evidence"]["DUPLICATE"]
    assert rows["big"]["classes"] == ["UNKNOWN"]


def test_duplicate_subset_across_modules(census):
    tests = {
        "small": T({"m.py": [1]}, ["x"]),
        "big": T({"m.py": [1], "n.py": [5]}, ["x"]),
    }
    assert labels(census, tests, files={"m.py", "n.py"})["small"] == ["DUPLICATE", "UNKNOWN"]


def test_not_duplicate_different_asserts(census):
    tests = {"small": T({"m.py": [1]}, ["x==1"]), "big": T({"m.py": [1, 2]}, ["x==2"])}
    assert labels(census, tests, files={"m.py"}) == {"small": ["UNKNOWN"], "big": ["UNKNOWN"]}


def test_not_duplicate_equal_sets(census):
    tests = {"a": T({"m.py": [1, 2]}), "b": T({"m.py": [1, 2]})}
    assert labels(census, tests, files={"m.py"}) == {"a": ["UNKNOWN"], "b": ["UNKNOWN"]}


def test_not_duplicate_parametrized(census):
    for small_p, big_p in [(True, False), (False, True), (True, True)]:
        tests = {"small": T({"m.py": [1]}, parametrized=small_p), "big": T({"m.py": [1, 2]}, parametrized=big_p)}
        assert labels(census, tests, files={"m.py"}) == {"small": ["UNKNOWN"], "big": ["UNKNOWN"]}


MUT = "scripts.mod.f"


def mutmut(tests_by, kills):
    return {"tests_by_function": tests_by, "kills_by_function": kills}


def test_zero_kill(census):
    m = mutmut({"scripts.mod.f": ["t"], "scripts.mod.g": ["t"]}, {"scripts.mod.f": 0, "scripts.mod.g": 0})
    assert labels(census, {"t": T({"m.py": [1]})}, files={"m.py"}, mutmut=m)["t"] == ["ZERO-KILL"]


def test_not_zero_kill_when_any_function_killed(census):
    m = mutmut({"scripts.mod.f": ["t"], "scripts.mod.g": ["t"]}, {"scripts.mod.f": 0, "scripts.mod.g": 3})
    assert labels(census, {"t": T({"m.py": [1]})}, files={"m.py"}, mutmut=m)["t"] == []


def test_unknown_when_mutmut_none(census):
    assert labels(census, {"t": T({"m.py": [1]})}, files={"m.py"}, mutmut=None)["t"] == ["UNKNOWN"]


def test_unknown_when_test_covers_no_mutated_function(census):
    m = mutmut({"scripts.mod.f": ["other"]}, {"scripts.mod.f": 0})
    assert labels(census, {"t": T({"m.py": [1]})}, files={"m.py"}, mutmut=m)["t"] == ["UNKNOWN"]


def test_zero_kill_ignores_functions_test_does_not_cover(census):
    m = mutmut({"scripts.mod.f": ["t"], "scripts.mod.g": ["other"]}, {"scripts.mod.f": 0, "scripts.mod.g": 9})
    assert labels(census, {"t": T({"m.py": [1]})}, files={"m.py"}, mutmut=m)["t"] == ["ZERO-KILL"]


def test_no_outcome_class_is_accepted_via_report(census):
    rows = [{"id": "t", "classes": ["NO-OUTCOME"], "evidence": {"NO-OUTCOME": "x"}}]
    assert census.report(rows)["STRENGTHEN"] == ["t"]


# ---- report ------------------------------------------------------------

def row(i, *classes):
    return {"id": i, "classes": sorted(classes), "evidence": {c: "e" for c in classes}}


def test_report_buckets(census):
    rows = [
        row("orphan", "ORPHAN"),
        row("orphan_noout", "ORPHAN", "NO-OUTCOME"),
        row("noout", "NO-OUTCOME"),
        row("zk", "ZERO-KILL"),
        row("dup", "DUPLICATE", "UNKNOWN"),
        row("unk", "UNKNOWN"),
        row("clean"),
    ]
    rep = census.report(rows)
    assert rep["REMOVE"] == ["orphan", "orphan_noout"]
    assert sorted(rep["STRENGTHEN"]) == ["noout", "zk"]
    assert sorted(rep["KEEP"]) == ["clean", "dup", "unk"]
    assert rep["DUPLICATE_CANDIDATES"] == ["dup"]
    assert rep["deleted"] == 0
    assert "deletes nothing" in rep["note"]


# ---- edges_from_coverage -----------------------------------------------

def test_edges_from_coverage(census):
    cov = {
        "files": {
            "scripts/a.py": {"contexts": {
                "1": ["", "tests/test_x.py::test_a|run", "tests/test_x.py::test_b|run"],
                "3": ["tests/test_x.py::test_a|setup", "tests/test_x.py::test_a|run"],
            }},
            "scripts/b.py": {"contexts": {
                "9": ["tests/test_x.py::test_a|teardown"],
                "2": [""],
            }},
        }
    }
    assert census.edges_from_coverage(cov) == {
        "tests/test_x.py::test_a": {"scripts/a.py": [1, 3], "scripts/b.py": [9]},
        "tests/test_x.py::test_b": {"scripts/a.py": [1]},
    }


def test_edges_from_coverage_sorts_lines_numerically(census):
    cov = {"files": {"m.py": {"contexts": {"10": ["t|run"], "2": ["t|run"]}}}}
    assert census.edges_from_coverage(cov) == {"t": {"m.py": [2, 10]}}


# ---- CLI ---------------------------------------------------------------

def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "test_census.py"), *map(str, args)],
        capture_output=True, text=True, cwd=REPO,
    )


def test_cli_end_to_end(tmp_path):
    edges = tmp_path / "E.json"
    edges.write_text(json.dumps({
        "tests/t.py::dead": {"scripts/dead.py": [1]},
        "tests/t.py::live": {"pyproject.toml": [1]},
        "tests/t.py::none": {},
    }))
    dead = tmp_path / "D.txt"
    dead.write_text("scripts/dead.py\n")
    mm = tmp_path / "M.json"
    mm.write_text(json.dumps({"tests_by_function": {}, "kills_by_function": {}}))
    out = tmp_path / "O.jsonl"

    r = run_cli("classify", "--edges", edges, "--dead", dead, "--mutmut", mm, "--out", out)
    assert r.returncode == 0, r.stderr
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [x["id"] for x in rows] == ["tests/t.py::dead", "tests/t.py::live", "tests/t.py::none"]
    by = {x["id"]: x["classes"] for x in rows}
    assert "ORPHAN" in by["tests/t.py::dead"]
    assert "ORPHAN" not in by["tests/t.py::live"]
    assert "ORPHAN" not in by["tests/t.py::none"]

    before = {p: p.read_bytes() for p in tmp_path.iterdir()}
    r = run_cli("report", "--census", out)
    assert r.returncode == 0, r.stderr
    assert "deletes nothing" in r.stdout
    assert "tests/t.py::dead" in r.stdout
    assert {p: p.read_bytes() for p in tmp_path.iterdir()} == before


@pytest.mark.parametrize("mm_args", [[], ["--mutmut", "none"]])
def test_cli_mutmut_optional(tmp_path, mm_args):
    edges = tmp_path / "E.json"
    edges.write_text(json.dumps({"tests/t.py::live": {"pyproject.toml": [1]}}))
    dead = tmp_path / "D.txt"
    dead.write_text("")
    out = tmp_path / "O.jsonl"
    r = run_cli("classify", "--edges", edges, "--dead", dead, *mm_args, "--out", out)
    assert r.returncode == 0, r.stderr
    row_ = json.loads(out.read_text().splitlines()[0])
    assert row_["classes"] == ["UNKNOWN"]
