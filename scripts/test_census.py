"""The test census ([#1566], R120.3): classify every test ORPHAN / DUPLICATE / ZERO-KILL / NO-OUTCOME.

No model decides a class. Edges come from coverage.py (`coverage json --show-contexts`,
recorded with `pytest --cov-context=test`), assertions from stdlib `ast`, kill data from mutmut.

Classes (R120.3 / row [#1566] Done-when 2):
  UNCLASSIFIED a test with no live coverage edge: ORPHAN and DUPLICATE cannot be decided for it.
  ORPHAN      every edge points to a DEAD or missing module (a test with no edge is NOT orphan).
  DUPLICATE   CANDIDATE only: covered (module, line) set is a strict subset of another test's,
              equal normalised assert expressions, equal fixtures, neither parametrized.
  ZERO-KILL   every mutated function the test covers has 0 kills; any covered function the kill
              data does not reach makes it UNKNOWN, never ZERO-KILL.
  NO-OUTCOME  no assertion-bearing call, or every one targets a Mock.
  UNKNOWN     the kill-based class could not be decided (no / partial mutmut data).

Subcommands: edges, classify, report. `report` deletes nothing and says so.

Usage:
  uv run --locked python scripts/test_census.py edges --data .coverage --out test-edges-<sha>.json
      (--cov cov.json instead reads a `coverage json --show-contexts` report: small suites only)
  uv run --locked python scripts/test_census.py classify --edges E.json --dead dead.txt \
      --collected collected.txt --mutmut mutants/mutmut-stats.json --out census.jsonl
      (--collected: `pytest --collect-only -q` ids; a collected test with no edge becomes UNCLASSIFIED)
  uv run --locked python scripts/test_census.py report --census census.jsonl
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_PHASE = re.compile(r"\|(run|setup|teardown)$")
_PARAM_SUFFIX = re.compile(r"\[.*\]$")
_MUTANT_SUFFIX = re.compile(r"__mutmut_\d+$")
#: mock-API assertions (`m.assert_called_once()`); unittest's are `assertEqual` etc.
_MOCK_ASSERT = re.compile(r"^assert_(called|not_called|any_call|has_calls|awaited|not_awaited|"
                          r"called_once|called_with|called_once_with|awaited_once|awaited_with)")
_MOCK_FACTORIES = {"Mock", "MagicMock", "AsyncMock", "NonCallableMock", "PropertyMock",
                   "create_autospec", "patch"}
_RAISES = {"raises", "warns", "deprecated_call"}
#: mutmut exit codes that are NOT a kill: survived, not checked, no tests, skipped, suspicious, timeout.
_NOT_KILL = {0, None, 5, 24, 33, 34, 35, 36, 152}
_HELPER_DEPTH = 3


# ---------------------------------------------------------------- edges

def edges_from_coverage(cov: dict) -> dict[str, dict[str, list[int]]]:
    """`coverage json --show-contexts` -> {test id: {module: sorted lines}}."""
    out: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for path, info in cov.get("files", {}).items():
        for line, ctxs in (info.get("contexts") or {}).items():
            for ctx in ctxs:
                if not ctx:
                    continue
                out[_PHASE.sub("", ctx)][path].add(int(line))
    return {t: {m: sorted(ls) for m, ls in mods.items()} for t, mods in out.items()}


# ---------------------------------------------------------------- NO-OUTCOME (ast)

def _root_name(node: ast.AST) -> str | None:
    while isinstance(node, (ast.Attribute, ast.Subscript, ast.Call)):
        node = node.value if not isinstance(node, ast.Call) else node.func
    return node.id if isinstance(node, ast.Name) else None


def _callee(node: ast.Call) -> str | None:
    f = node.func
    return f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None


def _is_mock_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and _callee(node) in _MOCK_FACTORIES


def _names_in(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _mock_names(fn: ast.AST) -> set[str]:
    names: set[str] = set()
    args = fn.args  # type: ignore[attr-defined]
    positional = [a.arg for a in [*args.posonlyargs, *args.args] if a.arg != "self"]
    n_patch = sum(1 for d in fn.decorator_list  # type: ignore[attr-defined]
                  if "patch" in ast.dump(d.func if isinstance(d, ast.Call) else d)
                  and "new=" not in ast.dump(d) and len(getattr(d, "args", ())) < 2)
    names |= set(positional[:n_patch])
    for n in ast.walk(fn):
        if isinstance(n, ast.Assign) and _is_mock_call(n.value):
            names |= {t.id for t in n.targets if isinstance(t, ast.Name)}
        elif isinstance(n, ast.With):
            for it in n.items:
                if _is_mock_call(it.context_expr) and isinstance(it.optional_vars, ast.Name):
                    names.add(it.optional_vars.id)
    return names


def _find_function(tree: ast.Module, func: str, cls: str | None):
    if cls is None:
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func:
                return n
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef) and (cls is None or n.name == cls):
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.name == func:
                    return m
    return None


def _real_assertion(fn: ast.AST, helpers: dict[str, ast.AST], depth: int) -> str | None:
    """Return a description of the first assertion-bearing node that is not Mock-targeting."""
    mocks = _mock_names(fn)
    for n in ast.walk(fn):
        if isinstance(n, ast.Assert):
            roots = _names_in(n.test)
            if roots and roots <= mocks:
                continue
            return "assert statement"
        if not isinstance(n, ast.Call):
            continue
        name = _callee(n)
        if name is None:
            continue
        if name in _RAISES or name == "fail":
            return f"pytest.{name}"
        if name.startswith("assert") and not _MOCK_ASSERT.match(name):
            roots = set().union(*(_names_in(a) for a in n.args), set()) if n.args else set()
            if roots and roots <= mocks:
                continue
            return f"unittest {name}"
        if _MOCK_ASSERT.match(name):
            continue
        if name in helpers and depth > 0 and helpers[name] is not fn:
            if _real_assertion(helpers[name], helpers, depth - 1):
                return f"helper {name}() asserts"
    return None


def no_outcome(source: str, func_name: str, class_name: str | None = None) -> dict[str, Any]:
    """NO-OUTCOME verdict for one test function; stdlib `ast` only."""
    tree = ast.parse(source)
    fn = _find_function(tree, func_name, class_name)
    if fn is None:
        return {"no_outcome": False, "reason": f"{func_name} not found in source (no verdict)"}
    helpers = {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name != func_name}
    found = _real_assertion(fn, helpers, _HELPER_DEPTH)
    if found:
        return {"no_outcome": False, "reason": f"has {found}"}
    anything = any(isinstance(n, ast.Assert) or (isinstance(n, ast.Call) and (_callee(n) or "").startswith("assert"))
                   for n in ast.walk(fn))
    return {"no_outcome": True,
            "reason": "every assertion targets a Mock" if anything else "no assertion-bearing call"}


def _is_fixture_decorator(d: ast.AST) -> bool:
    return isinstance(d, ast.Call) and _callee(d) == "fixture" and any(
        k.arg == "autouse" and isinstance(k.value, ast.Constant) and k.value.value is True
        for k in d.keywords)


def _usefixtures(nodes) -> list[str]:
    """String arguments of every `*.usefixtures("a", "b")` call in the given decorator/expr nodes."""
    out: list[str] = []
    for node in nodes:
        for n in ast.walk(node):
            if isinstance(n, ast.Call) and _callee(n) == "usefixtures":
                out += [f"usefixtures:{a.value}" for a in n.args
                        if isinstance(a, ast.Constant) and isinstance(a.value, str)]
    return out


def _autouse(body, where: str) -> list[str]:
    return [f"autouse:{where}:{n.name}" for n in body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and any(_is_fixture_decorator(d) for d in n.decorator_list)]


def _module_marks(tree: ast.Module) -> list[ast.AST]:
    """Right-hand sides of module-level `pytestmark = ...`."""
    return [n.value for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in n.targets)]


def scope_fixtures(tree: ast.Module, fpath: str, cls: str | None, fn: ast.AST,
                   root: Path) -> tuple[list[str], bool]:
    """Fixtures a test is subject to beyond its arguments: (names, readable).

    `usefixtures` on the test / its class / module `pytestmark`, autouse fixtures defined in the
    module, the class, and every `conftest.py` from the root down to the test's directory.
    readable is False when a scope cannot be read (unparsable conftest, class with an unreadable
    base): the duplicate bucket then fails closed.
    """
    names = _usefixtures(fn.decorator_list)  # type: ignore[attr-defined]
    names += _usefixtures(_module_marks(tree))
    names += _autouse(tree.body, fpath)
    readable = True
    if cls is not None:
        node = next((n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls), None)
        if node is None:
            readable = False
        else:
            names += _usefixtures(node.decorator_list) + _autouse(node.body, f"{fpath}::{cls}")
            for b in node.bases:
                if ast.unparse(b) not in {"object", "TestCase", "unittest.TestCase"}:
                    readable = False
    parts = Path(fpath).parent.parts
    for i in range(len(parts) + 1):
        d = "/".join(parts[:i])
        conf = root / d / "conftest.py" if d else root / "conftest.py"
        if not conf.is_file():
            continue
        try:
            ctree = ast.parse(conf.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            readable = False
            continue
        names += _autouse(ctree.body, f"conftest:{d}") + _usefixtures(_module_marks(ctree))
    return names, readable


def _fn_facts(fn: ast.AST) -> tuple[list[str], tuple[str, ...], bool]:
    """(normalised asserts, fixture arg names, parametrized) for a test function node."""
    asserts: list[str] = []
    for n in ast.walk(fn):
        if isinstance(n, ast.Assert):
            asserts.append(ast.dump(n.test))
        elif isinstance(n, ast.Call) and (_callee(n) or "").startswith("assert"):
            asserts.append(ast.dump(n))
        elif isinstance(n, ast.Call) and _callee(n) in _RAISES:
            asserts.append(ast.dump(n))
    args = fn.args  # type: ignore[attr-defined]
    fixtures = tuple(sorted(a.arg for a in [*args.posonlyargs, *args.args, *args.kwonlyargs] if a.arg != "self"))
    param = any("parametrize" in ast.dump(d) for d in fn.decorator_list)  # type: ignore[attr-defined]
    return sorted(asserts), fixtures, param


# ---------------------------------------------------------------- classify

def _mask(lines) -> int:
    """Line numbers (ints) or 'a-b' range strings -> one int bitmask."""
    m = 0
    for ln in lines:
        if isinstance(ln, str):
            a, _, b = ln.partition("-")
            a, b = int(a), int(b or a)
            m |= (1 << (b + 1)) - (1 << a)
        else:
            m |= 1 << ln
    return m


def _live_edges(edges: dict) -> dict:
    """Edge modules that can decide a class: the test files and conftest are always live."""
    return {m: v for m, v in edges.items() if not (m.startswith("tests/") or m.endswith("conftest.py"))}


def _duplicates(tests: dict[str, dict]) -> dict[str, str]:
    """test id -> evidence, for strict-subset candidates within equal (asserts, fixtures) groups."""
    groups: dict[tuple, list[str]] = defaultdict(list)
    masks: dict[str, dict[str, int]] = {}
    for tid, t in tests.items():
        if t.get("parametrized") or not t.get("asserts") or t.get("fixtures_unreadable"):
            continue
        mk = {m: _mask(ls) for m, ls in _live_edges(t.get("edges", {})).items()}
        mk = {m: v for m, v in mk.items() if v}
        if not mk:
            continue
        masks[tid] = mk
        groups[(tuple(t["asserts"]), tuple(t.get("fixtures", ())))].append(tid)

    def strict_subset(a: dict[str, int], b: dict[str, int]) -> bool:
        if any(m not in b or v & ~b[m] for m, v in a.items()):
            return False
        return a != b

    out: dict[str, str] = {}
    for ids in groups.values():
        if len(ids) < 2:
            continue
        for tid in sorted(ids):
            supers = [o for o in sorted(ids) if o != tid and strict_subset(masks[tid], masks[o])]
            if supers:
                more = f" (+{len(supers) - 1} more)" if len(supers) > 1 else ""
                out[tid] = f"strict subset of {supers[0]}{more}; equal asserts, candidate only"
    return out


def _kill_class(tid: str, mutmut: dict | None, covered_by: dict | None = None) -> tuple[str | None, str]:
    if not mutmut:
        return "UNKNOWN", "no mutmut data"
    tbf = mutmut.get("tests_by_function") or {}
    kills = mutmut.get("kills_by_function") or {}
    covered = sorted(covered_by.get(tid, ())) if covered_by is not None else sorted(f for f, ts in tbf.items() if tid in ts)
    if not covered:
        return "UNKNOWN", "covers no mutated function in the mutmut slice"
    unreached = [f for f in covered if f not in kills]
    if unreached:
        return "UNKNOWN", f"kill data does not reach {len(unreached)} of {len(covered)} covered functions"
    killed = [f for f in covered if kills[f] > 0]
    if killed:
        return None, ""
    return "ZERO-KILL", f"all {len(covered)} covered mutated functions have 0 kills"


def classify(tests: dict, dead: set[str], repo_files: set[str], mutmut_stats: dict | None) -> list[dict]:
    dups = _duplicates(tests)
    covered_by: dict[str, set[str]] | None = None
    if mutmut_stats:
        covered_by = defaultdict(set)
        for f, ts in (mutmut_stats.get("tests_by_function") or {}).items():
            for x in ts:
                covered_by[x].add(f)
    rows = []
    for tid in sorted(tests):
        t = tests[tid]
        classes: dict[str, str] = {}
        mods = list(_live_edges(t.get("edges", {})))
        if not mods:
            classes["UNCLASSIFIED"] = ("no live coverage edge (no coverage context recorded, or only "
                                       "tests/conftest edges): ORPHAN and DUPLICATE cannot be decided")
        if mods and all(m in dead or m not in repo_files for m in mods):
            gone = sorted(m for m in mods if m not in repo_files)
            classes["ORPHAN"] = f"all {len(mods)} edge modules dead or missing" + (f" (missing: {', '.join(gone[:3])})" if gone else "")
        if tid in dups:
            classes["DUPLICATE"] = dups[tid]
        label, why = _kill_class(tid, mutmut_stats, covered_by)
        if label:
            classes[label] = why
        if t.get("no_outcome"):
            classes["NO-OUTCOME"] = t.get("no_outcome_reason", "no assertion-bearing call")
        rows.append({"id": tid, "classes": sorted(classes), "evidence": classes})
    return rows


def report(rows: list[dict]) -> dict[str, Any]:
    """KEEP / STRENGTHEN / REMOVE. Deletes nothing."""
    rep: dict[str, Any] = {"KEEP": [], "STRENGTHEN": [], "REMOVE": [], "UNCLASSIFIED": [],
                           "DUPLICATE_CANDIDATES": []}
    for r in rows:
        c = set(r["classes"])
        bucket = ("REMOVE" if "ORPHAN" in c else "STRENGTHEN" if c & {"NO-OUTCOME", "ZERO-KILL"}
                  else "UNCLASSIFIED" if "UNCLASSIFIED" in c else "KEEP")
        rep[bucket].append(r["id"])
        if "UNCLASSIFIED" in c and bucket != "UNCLASSIFIED":
            rep["UNCLASSIFIED"].append(r["id"])  # also listed: UNCLASSIFIED counts every row with that class
        if "DUPLICATE" in c:
            rep["DUPLICATE_CANDIDATES"].append(r["id"])
    rep["unclassified_reason"] = ("no live coverage edge: the test recorded no coverage context on a "
                                  "non-test module, so ORPHAN and DUPLICATE could not be decided for it")
    rep["orphan_note"] = ("ORPHAN cannot fire for a test with no coverage edge (a test of a deleted module "
                          "has none), so REMOVE is a lower bound, not a finding of absence")
    rep["deleted"] = 0
    rep["note"] = "report only: deletes nothing; every bucket is a proposal for the operator's GO"
    return rep


# ---------------------------------------------------------------- CLI

def _split_id(tid: str) -> tuple[str, str | None, str]:
    parts = _PARAM_SUFFIX.sub("", tid).split("::")
    return parts[0], (parts[-2] if len(parts) > 2 else None), parts[-1]


def load_mutmut(path: Path) -> dict:
    """Normalise raw `mutmut-stats.json` (+ sibling `.meta` kill files) or a pre-normalised dict."""
    d = json.loads(path.read_text(encoding="utf-8"))
    if "tests_by_function" in d:
        return d
    tbf = {_MUTANT_SUFFIX.sub("", k): v for k, v in d.get("tests_by_mangled_function_name", {}).items()}
    per_func: dict[str, list[int | None]] = defaultdict(list)
    for meta in path.parent.rglob("*.meta"):
        try:
            codes = json.loads(meta.read_text(encoding="utf-8")).get("exit_code_by_key", {})
        except (OSError, ValueError):
            continue
        for key, code in codes.items():
            per_func[_MUTANT_SUFFIX.sub("", key)].append(code)
    kills: dict[str, int] = {}
    for func, codes in per_func.items():
        n = sum(1 for c in codes if c not in _NOT_KILL)
        if n or all(c is not None for c in codes):  # 0 kills is only certain when every mutant ran
            kills[func] = n
    return {"tests_by_function": tbf, "kills_by_function": kills}


def build_tests(edges: dict, root: Path, collected=None) -> tuple[dict, set[str]]:
    """One entry per test in `edges` UNION `collected`: a collected test with no edge is still a row."""
    repo_files = {m for mods in edges.values() for m in mods if (root / m).exists()}
    asts: dict[str, ast.Module | None] = {}
    sources: dict[str, str] = {}
    tests: dict[str, dict] = {}
    for tid in sorted(set(edges) | set(collected or ())):
        mods = edges.get(tid, {})
        t: dict[str, Any] = {"edges": mods, "asserts": [], "fixtures": (), "parametrized": "[" in tid,
                             "fixtures_unreadable": True}
        fpath, cls, func = _split_id(tid)
        if fpath not in asts:
            p = root / fpath
            try:
                sources[fpath] = p.read_text(encoding="utf-8")
                asts[fpath] = ast.parse(sources[fpath])
            except (OSError, SyntaxError, UnicodeDecodeError):
                asts[fpath] = None
        tree = asts[fpath]
        fn = _find_function(tree, func, cls) if tree else None
        if fn is not None:
            t["asserts"], t["fixtures"], param = _fn_facts(fn)
            t["parametrized"] = t["parametrized"] or param
            extra, readable = scope_fixtures(tree, fpath, cls, fn, root)
            t["fixtures"] = tuple(sorted({*t["fixtures"], *extra}))
            t["fixtures_unreadable"] = not readable
            res = no_outcome(sources[fpath], func, cls)
            t["no_outcome"], t["no_outcome_reason"] = res["no_outcome"], res["reason"]
        tests[tid] = t
    return tests, repo_files


def edges_from_data(data_file: str) -> dict[str, dict[str, list[str]]]:
    """Read the `.coverage` database directly (the JSON report is multi-GB on this suite).

    Lines are stored as 'a-b' range strings, which `classify` expands to bitmasks.
    """
    from coverage import CoverageData

    cd = CoverageData(basename=data_file)
    cd.read()
    acc: dict[str, dict[str, int]] = defaultdict(dict)
    for path in cd.measured_files():
        for ln, ctxs in cd.contexts_by_lineno(path).items():
            for ctx in ctxs:
                if ctx:
                    d = acc[_PHASE.sub("", ctx)]
                    d[path] = d.get(path, 0) | (1 << ln)
    out: dict[str, dict[str, list[str]]] = {}
    for tid, mods in acc.items():
        out[tid] = {}
        for m, mask in mods.items():
            bits = bin(mask)[:1:-1]  # bit n of mask == character n
            out[tid][m] = [f"{r.start()}-{r.end() - 1}" for r in re.finditer("1+", bits)]
    return out


def relativize(edges: dict, root: Path) -> dict:
    """Absolute module paths under `root` -> posix repo-relative (coverage stores absolute paths unless
    `relative_files` is set), so `tests/` filtering and `--dead` matching see repo paths."""
    base = root.resolve()
    out: dict = {}
    for tid, mods in edges.items():
        out[tid] = {}
        for m, lines in mods.items():
            try:
                m = Path(m).resolve().relative_to(base).as_posix() if Path(m).is_absolute() else m
            except ValueError:
                pass
            out[tid][m] = lines
    return out


def _cmd_edges(a) -> int:
    if not a.data and not a.cov:
        raise SystemExit("edges: give --cov FILE or --data .coverage")
    if a.data:
        edges = edges_from_data(a.data)
    else:
        edges = edges_from_coverage(json.loads(Path(a.cov).read_text(encoding="utf-8")))
    edges = relativize(edges, Path(a.root))
    Path(a.out).write_text(json.dumps(edges, sort_keys=True), encoding="utf-8")
    return 0


def _cmd_classify(a) -> int:
    edges = json.loads(Path(a.edges).read_text(encoding="utf-8"))
    dead = {ln.strip() for ln in Path(a.dead).read_text(encoding="utf-8").splitlines() if ln.strip()}
    mm = load_mutmut(Path(a.mutmut)) if a.mutmut and a.mutmut != "none" else None
    collected = ([ln.strip() for ln in Path(a.collected).read_text(encoding="utf-8").splitlines() if ln.strip()]
                 if a.collected else None)
    tests, repo_files = build_tests(edges, Path(a.root), collected)
    rows = classify(tests, dead, repo_files, mm)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.writelines(json.dumps(r, sort_keys=True) + "\n" for r in rows)
    return 0


def _cmd_report(a) -> int:
    rows = [json.loads(ln) for ln in Path(a.census).read_text(encoding="utf-8").splitlines() if ln.strip()]
    rep = report(rows)
    cls: dict[str, int] = defaultdict(int)
    for r in rows:
        for c in r["classes"]:
            cls[c] += 1
    print(f"{len(rows)} tests; classes: " + ", ".join(f"{k}={v}" for k, v in sorted(cls.items())))
    print(f"UNCLASSIFIED: {len(rep['UNCLASSIFIED'])} -- {rep['unclassified_reason']}")
    for b in ("REMOVE", "STRENGTHEN", "KEEP", "UNCLASSIFIED"):
        print(f"{b}: {len(rep[b])}")
        if b == "REMOVE":
            print(f"  {rep['orphan_note']}")
        for tid in rep[b][: a.top]:
            ev = next(r["evidence"] for r in rows if r["id"] == tid)
            print(f"  {tid}  {'; '.join(f'{k}: {v}' for k, v in ev.items())}")
    print(f"DUPLICATE candidates: {len(rep['DUPLICATE_CANDIDATES'])}")
    print(rep["note"])
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("edges")
    e.add_argument("--cov", default=None, help="coverage json --show-contexts output (small suites)")
    e.add_argument("--data", default=None, help="a .coverage database (large suites)")
    e.add_argument("--out", required=True)
    e.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    c = sub.add_parser("classify")
    c.add_argument("--edges", required=True)
    c.add_argument("--dead", required=True)
    c.add_argument("--mutmut", default=None)
    c.add_argument("--collected", default=None,
                   help="pytest --collect-only -q node ids, one per line: every one gets a row")
    c.add_argument("--out", required=True)
    c.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    r = sub.add_parser("report")
    r.add_argument("--census", required=True)
    r.add_argument("--top", type=int, default=20)
    a = ap.parse_args(argv)
    return {"edges": _cmd_edges, "classify": _cmd_classify, "report": _cmd_report}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
