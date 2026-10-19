"""Tests for scripts/test_census.py ([#1566]); written RED first, see the git log."""
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
    assert labels(census, {"t": T({})}, files={"m.py"})["t"] == ["UNCLASSIFIED", "UNKNOWN"]


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


def test_mask_accepts_ints_and_ranges(census):
    assert census._mask([1, 3]) == census._mask(["1-1", "3-3"]) == 0b1010
    assert census._mask(["2-4"]) == 0b11100


def test_tests_dir_edges_never_prevent_orphan(census):
    t = {"t": {"edges": {"scripts/dead.py": [1], "tests/test_x.py": [1], "tests/conftest.py": [2]}}}
    rows = census.classify(t, {"scripts/dead.py"}, {"scripts/dead.py", "tests/test_x.py", "tests/conftest.py"}, None)
    assert rows[0]["classes"] == ["ORPHAN", "UNKNOWN"]


def test_dict_call_is_not_a_mock(census):
    code = "def test_a():\n    r = dict(a=1)\n    assert r == {'a': 1}\n"
    assert census.no_outcome(code, "test_a")["no_outcome"] is False


def test_pytest_fail_counts_as_assertion(census):
    code = "import pytest\ndef test_a():\n    if f():\n        pytest.fail('x')\n"
    assert census.no_outcome(code, "test_a")["no_outcome"] is False


def test_edges_from_data_roundtrip(census, tmp_path):
    import coverage
    src = tmp_path / "mod.py"
    src.write_text("a = 1\nb = 2\nc = 3\n")
    data = tmp_path / ".cov"
    cd = coverage.CoverageData(basename=str(data))
    cd.set_context("tests/t.py::test_a|run")
    cd.add_lines({str(src): [1, 2, 3, 7]})
    cd.write()
    assert census.edges_from_data(str(data)) == {"tests/t.py::test_a": {str(src): ["1-3", "7-7"]}}


# ---- UNCLASSIFIED / fixture-aware DUPLICATE (RED) -----------------------

def test_unclassified_no_edges(census):
    rows = census.classify({"t/a": T({})}, set(), set(), None)
    assert "UNCLASSIFIED" in rows[0]["classes"]
    assert isinstance(rows[0]["evidence"]["UNCLASSIFIED"], str)
    assert rows[0]["evidence"]["UNCLASSIFIED"]


def test_unclassified_only_tests_and_conftest_edges(census):
    tests = {"t/a": T({"tests/helper.py": [1], "conftest.py": [2], "tests/conftest.py": [3]})}
    rows = census.classify(tests, set(), {"tests/helper.py", "conftest.py"}, None)
    assert "UNCLASSIFIED" in rows[0]["classes"]
    assert rows[0]["evidence"]["UNCLASSIFIED"]


def test_unclassified_no_edges_is_never_orphan(census):
    assert "ORPHAN" not in labels(census, {"t/a": T({})})["t/a"]


def test_live_edge_is_not_unclassified_and_unchanged(census):
    assert labels(census, {"t/a": T({"m.py": [1]})}, files={"m.py"})["t/a"] == ["UNKNOWN"]


def test_live_edge_to_dead_module_is_orphan_not_unclassified(census):
    got = labels(census, {"t/a": T({"m.py": [1]})}, dead={"m.py"}, files={"m.py"})["t/a"]
    assert "ORPHAN" in got
    assert "UNCLASSIFIED" not in got


def test_unclassified_evidence_only_for_unclassified_rows(census):
    tests = {"t/a": T({}), "t/b": T({"m.py": [1]})}
    rows = {r["id"]: r for r in census.classify(tests, set(), {"m.py"}, None)}
    assert "UNCLASSIFIED" in rows["t/a"]["evidence"]
    assert "UNCLASSIFIED" not in rows["t/b"]["evidence"]


def test_report_lists_unclassified_ids(census):
    rep = census.report([row("u", "UNCLASSIFIED"), row("clean"), row("k", "UNKNOWN")])
    assert rep["UNCLASSIFIED"] == ["u"]


def test_report_unclassified_alone_not_in_keep(census):
    rep = census.report([row("u", "UNCLASSIFIED"), row("clean")])
    assert "u" not in rep["KEEP"]
    assert "clean" in rep["KEEP"]


def test_report_unclassified_with_no_outcome_is_strengthen_and_listed(census):
    rep = census.report([row("u", "UNCLASSIFIED", "NO-OUTCOME")])
    assert "u" in rep["STRENGTHEN"]
    assert rep["UNCLASSIFIED"] == ["u"]


def test_report_unclassified_empty_when_none(census):
    rep = census.report([row("clean"), row("z", "ZERO-KILL")])
    assert rep["UNCLASSIFIED"] == []
    assert rep["STRENGTHEN"] == ["z"]
    assert rep["KEEP"] == ["clean"]


def test_report_reason_and_orphan_note(census):
    rep = census.report([row("clean")])
    assert isinstance(rep["unclassified_reason"], str) and rep["unclassified_reason"]
    assert isinstance(rep["orphan_note"], str)
    assert "ORPHAN cannot fire" in rep["orphan_note"]


def test_report_existing_buckets_unchanged_without_unclassified(census):
    rep = census.report([row("o", "ORPHAN"), row("n", "NO-OUTCOME"), row("d", "DUPLICATE")])
    assert rep["REMOVE"] == ["o"]
    assert rep["STRENGTHEN"] == ["n"]
    assert rep["KEEP"] == ["d"]
    assert rep["DUPLICATE_CANDIDATES"] == ["d"]


def _census_file(tmp_path, rows):
    p = tmp_path / "census.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def test_cli_report_prints_unclassified_count(tmp_path):
    p = _census_file(tmp_path, [row("u1", "UNCLASSIFIED"), row("u2", "UNCLASSIFIED", "UNKNOWN"), row("c")])
    res = run_cli("report", "--census", p)
    assert res.returncode == 0
    assert any(ln.startswith("UNCLASSIFIED: 2") for ln in res.stdout.splitlines())


def test_cli_report_orphan_cannot_fire_near_remove(tmp_path):
    p = _census_file(tmp_path, [row("u1", "UNCLASSIFIED")])
    res = run_cli("report", "--census", p)
    lines = res.stdout.splitlines()
    i = next(n for n, ln in enumerate(lines) if ln.startswith("REMOVE: "))
    assert "ORPHAN cannot fire" in " ".join(lines[i:i + 2])


def test_cli_report_remove_zero_has_sentence(tmp_path):
    p = _census_file(tmp_path, [row("c")])
    res = run_cli("report", "--census", p)
    lines = res.stdout.splitlines()
    i = lines.index("REMOVE: 0")
    assert "ORPHAN cannot fire" in " ".join(lines[i:i + 2])


def _classify_cli(tmp_path, edges, collected_ids):
    e = tmp_path / "E.json"
    e.write_text(json.dumps(edges))
    d = tmp_path / "dead.txt"
    d.write_text("")
    c = tmp_path / "collected.txt"
    c.write_text("".join(i + "\n" for i in collected_ids))
    out = tmp_path / "out.jsonl"
    res = run_cli("classify", "--edges", e, "--dead", d, "--collected", c,
                  "--root", tmp_path, "--out", out)
    assert res.returncode == 0, res.stderr
    return {json.loads(ln)["id"]: json.loads(ln) for ln in out.read_text().splitlines() if ln.strip()}


def test_cli_classify_collected_id_without_edge_is_unclassified(tmp_path):
    rows = _classify_cli(tmp_path, {"tests/t.py::a": {}}, ["tests/t.py::a", "tests/t.py::b"])
    assert "UNCLASSIFIED" in rows["tests/t.py::b"]["classes"]
    assert rows["tests/t.py::b"]["evidence"]["UNCLASSIFIED"]


def test_cli_classify_rows_are_union_of_edges_and_collected(tmp_path):
    edges = {"tests/t.py::a": {}, "tests/t.py::only_edges": {}}
    rows = _classify_cli(tmp_path, edges, ["tests/t.py::a", "tests/t.py::only_collected"])
    assert set(rows) == {"tests/t.py::a", "tests/t.py::only_edges", "tests/t.py::only_collected"}


def test_cli_classify_collected_id_is_not_orphan(tmp_path):
    rows = _classify_cli(tmp_path, {}, ["tests/t.py::b"])
    assert "ORPHAN" not in rows["tests/t.py::b"]["classes"]


# ---- DUPLICATE fixture key ---------------------------------------------

_BODY = "    assert 1 == 1\n"


def _write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


@pytest.fixture
def dup(census, tmp_path):
    def run(edges):
        tests, files = census.build_tests(edges, tmp_path)
        rows = census.classify(tests, set(), {"m.py"} | files, None)
        return {r["id"]: r["classes"] for r in rows}
    return run


A_EDGE = {"m.py": ["1-2"]}
B_EDGE = {"m.py": ["1-3"]}


def test_dup_baseline_equal_fixtures_subset_is_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py",
           "def test_a():\n" + _BODY + "\ndef test_b():\n" + _BODY)
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" in got["tests/test_x.py::test_a"]
    assert "DUPLICATE" not in got["tests/test_x.py::test_b"]


def test_dup_usefixtures_on_one_test_blocks_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py",
           "import pytest\n\n"
           "def test_a():\n" + _BODY + "\n"
           "@pytest.mark.usefixtures(\"db\")\n"
           "def test_b():\n" + _BODY)
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" not in got["tests/test_x.py::test_a"]
    assert "DUPLICATE" not in got["tests/test_x.py::test_b"]


def test_dup_identical_usefixtures_still_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py",
           "import pytest\n\n"
           "@pytest.mark.usefixtures(\"db\")\n"
           "def test_a():\n" + _BODY + "\n"
           "@pytest.mark.usefixtures(\"db\")\n"
           "def test_b():\n" + _BODY)
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" in got["tests/test_x.py::test_a"]


def test_dup_module_autouse_fixture_applies_to_both_still_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py",
           "import pytest\n\n"
           "@pytest.fixture(autouse=True)\n"
           "def _auto():\n    yield\n\n"
           "def test_a():\n" + _BODY + "\n"
           "def test_b():\n" + _BODY)
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" in got["tests/test_x.py::test_a"]


def test_dup_class_level_usefixtures_on_one_class_blocks_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py",
           "import pytest\n\n"
           "class TestC:\n"
           "    def test_a(self):\n    " + _BODY + "\n"
           "@pytest.mark.usefixtures(\"db\")\n"
           "class TestD:\n"
           "    def test_a(self):\n    " + _BODY)
    got = dup({"tests/test_x.py::TestC::test_a": A_EDGE, "tests/test_x.py::TestD::test_a": B_EDGE})
    assert "DUPLICATE" not in got["tests/test_x.py::TestC::test_a"]
    assert "DUPLICATE" not in got["tests/test_x.py::TestD::test_a"]


def test_dup_conftest_autouse_in_one_directory_blocks_duplicate(tmp_path, dup):
    _write(tmp_path, "tests/a/conftest.py",
           "import pytest\n\n@pytest.fixture(autouse=True)\ndef _auto():\n    yield\n")
    _write(tmp_path, "tests/a/test_x.py", "def test_a():\n" + _BODY)
    _write(tmp_path, "tests/b/test_x.py", "def test_a():\n" + _BODY)
    got = dup({"tests/a/test_x.py::test_a": A_EDGE, "tests/b/test_x.py::test_a": B_EDGE})
    assert "DUPLICATE" not in got["tests/a/test_x.py::test_a"]
    assert "DUPLICATE" not in got["tests/b/test_x.py::test_a"]


def test_dup_fail_closed_when_test_file_missing(tmp_path, dup):
    (tmp_path / "tests").mkdir()
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" not in got["tests/test_x.py::test_a"]
    assert "DUPLICATE" not in got["tests/test_x.py::test_b"]


def test_dup_fail_closed_when_test_file_has_syntax_error(tmp_path, dup):
    _write(tmp_path, "tests/test_x.py", "def test_a(:\n" + _BODY + "def test_b():\n" + _BODY)
    got = dup({"tests/test_x.py::test_a": A_EDGE, "tests/test_x.py::test_b": B_EDGE})
    assert "DUPLICATE" not in got["tests/test_x.py::test_a"]
    assert "DUPLICATE" not in got["tests/test_x.py::test_b"]


def test_build_tests_collected_param_is_accepted(census, tmp_path):
    _write(tmp_path, "tests/test_x.py", "def test_a():\n" + _BODY)
    tests, files = census.build_tests({"tests/test_x.py::test_a": {}}, tmp_path, collected=None)
    assert "tests/test_x.py::test_a" in tests
    assert isinstance(files, set)


def test_relativize_makes_absolute_paths_repo_relative(census, tmp_path):
    edges = {"t": {str(tmp_path / "scripts" / "m.py"): ["1-2"], "elsewhere/x.py": ["3-3"]}}
    assert census.relativize(edges, tmp_path) == {"t": {"scripts/m.py": ["1-2"], "elsewhere/x.py": ["3-3"]}}


def test_edges_without_source_is_a_usage_error(tmp_path):
    r = run_cli("edges", "--out", tmp_path / "E.json")
    assert r.returncode != 0 and "Traceback" not in r.stderr
