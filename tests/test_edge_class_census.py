"""RED-first witnesses for the THIRD commit-tier refusal -- the five-kind edge class ([#664]).

Every test in this file was written and run RED before `graph_queries.edge_class_census`
existed. `orphan_census` and `task_coverage` landed with their trip-tests in lane `v-664`
(`tests/test_graph_spine.py` witnesses 2 and 3); this file is the third refusal the frozen
contract names, and the one `[#664]`'s Done-when leaves unarmed.

WHAT IS REFUSED, AND WHAT DELIBERATELY IS NOT. The class is DECLARE-REVIEWS section A.1's
five kinds -- citation, generation, template, test, script call-site -- as narrowed on main
by `ff103444`. Eighteen private computations of that class are live and OWED their W-G3
migration, one organ per lane (ADR-118 section 5). **Driving that eighteen to zero is not
this refusal's job and must not be**: a gate that refused all eighteen would refuse every
commit in the repo on a defect no single committer can legally repair, which is the
unbounded-refusal shape `decision_coverage.ARM_DATE` already exists to avoid.

So the refusal is a RATCHET, not a bar. The set may shrink and may not grow:

  * a module that NEWLY acquires the shape -- an add, or an edit that gives an existing
    module the shape it did not have at HEAD -- and that the register does not verdict,
    REFUSES;
  * a register row naming a file, or a symbol, that is GONE refuses too, so the register
    cannot rot into paper suppressions the way `stale_dispositions` exists to prevent.

**A test that passes on conforming input is not a trip-test** (the frozen contract's words,
carried from `tests/test_graph_spine.py`). Each leg below therefore carries both directions.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import graph_queries as gq  # noqa: E402
import graph_store as gs  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------------------- the fixture


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


#: A module with the shape: it walks the tree AND pulls structure out of the text it reads.
SHAPED = """\
import re
from pathlib import Path

CITE = re.compile(r"`([^`]+\\.md)`")
ROW = re.compile(r"\\[#(\\d+)\\]")


def edges(root):
    found = []
    for path in Path(root).rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        found += CITE.findall(text) + ROW.findall(text)
    return found
"""

#: The same module WITHOUT the shape -- no extraction, so nothing to migrate.
UNSHAPED = """\
from pathlib import Path


def biggest(root):
    return max((p.stat().st_size for p in Path(root).rglob("*.md")), default=0)
"""


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    """A committed tree carrying one shaped module and one unshaped one.

    Both are COMMITTED, which is what makes the ratchet testable at all: the leg compares
    the staged bytes against the module's state at HEAD, so a fixture with no HEAD would
    make every module read as an arrival.
    """
    root = tmp_path / "tiny"
    _write(root / ".pre-commit-config.yaml", """\
repos:
  - repo: local
    hooks:
      - id: wired-gate
        name: the one wired gate
        entry: uv run --locked python scripts/wired.py
        language: system
""")
    _write(root / "scripts" / "wired.py", "def main():\n    return 1\n")
    _write(root / "scripts" / "old_scanner.py", SHAPED)
    _write(root / "scripts" / "plain.py", UNSHAPED)
    _write(root / "ARCHITECTURE.md", "# Architecture\n\nThe gate is `scripts/wired.py`.\n")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "lane@example.invalid")
    _git(root, "config", "user.name", "lane")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "the tree as it stands")
    return root


@pytest.fixture
def tiny_store(tiny_repo: Path, tmp_path: Path):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    store = gs.open_store(db)
    try:
        yield store
    finally:
        store.close()


PRIVATE = gq.EdgeComputation(kind="citation", status="private",
                             owner="a W-G3 migration lane")


# ------------------------------------------------------- the shape predicate, both directions


def test_the_shape_predicate_recognises_extraction_over_a_tree_walk():
    """THE PREDICATE. Extraction (two regexes, or an `ast` parse) over a scan or a read."""
    assert gq.is_edge_computation_shape(SHAPED)


def test_the_shape_predicate_admits_a_module_that_extracts_nothing():
    """A gate that can only fail is not a gate. Walking a tree is not computing an edge."""
    assert not gq.is_edge_computation_shape(UNSHAPED)


def test_the_shape_predicate_admits_a_module_that_never_touches_a_file():
    """Two regexes over an argument string is not a corpus-structure computation."""
    source = ("import re\nA = re.compile('a')\nB = re.compile('b')\n"
              "def f(s):\n    return A.match(s) or B.match(s)\n")
    assert not gq.is_edge_computation_shape(source)


def test_the_shape_predicate_recognises_an_ast_walker_with_no_regex_at_all():
    """`codemap/ast_walker.py` and `reverse_dep_oracle.py` compile ZERO regexes.

    The predicate lane `v-664` STATED for its section 2.5 table -- *"walks the tree and
    compiles two or more regexes"* -- does not reproduce that table: four of its twenty-one
    rows fail it in one direction or the other. Recorded as a finding in this lane's
    artifact; repaired here by making `ast` a first-class extraction signal.
    """
    source = ("import ast\nfrom pathlib import Path\n\n"
              "def imports(root):\n"
              "    for p in Path(root).rglob('*.py'):\n"
              "        for node in ast.walk(ast.parse(p.read_text())):\n"
              "            yield node\n")
    assert gq.is_edge_computation_shape(source)


def test_the_shape_predicate_survives_a_module_it_cannot_parse():
    """Unparseable is not shaped. A syntax error is `ruff`'s refusal, not this one."""
    assert not gq.is_edge_computation_shape("def (:\n")


# ------------------------------------------------- leg 1: the ratchet REFUSES a new computation


def test_edge_class_census_refuses_a_NEW_private_edge_computation(tiny_repo: Path, tiny_store):
    """THE TRIP. A module that arrives with the shape and no verdict refuses the commit."""
    _write(tiny_repo / "scripts" / "new_scanner.py", SHAPED)
    _git(tiny_repo, "add", "scripts/new_scanner.py")

    findings = gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["scripts/new_scanner.py"], register={})
    assert [f.subject for f in findings] == ["scripts/new_scanner.py"]
    assert "FPG-1" in findings[0].evidence, \
        "a refusal that does not name the repair trains the reader to distrust the pointer"


def test_edge_class_census_admits_a_new_module_the_register_verdicts(tiny_repo: Path,
                                                                     tiny_store):
    """The permissive direction: a verdicted arrival is admitted, whatever its shape."""
    _write(tiny_repo / "scripts" / "new_scanner.py", SHAPED)
    _git(tiny_repo, "add", "scripts/new_scanner.py")

    register = {"scripts/new_scanner.py": PRIVATE}
    assert not gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["scripts/new_scanner.py"], register=register)


def test_edge_class_census_admits_a_new_module_with_no_shape(tiny_repo: Path, tiny_store):
    _write(tiny_repo / "scripts" / "new_plain.py", UNSHAPED)
    _git(tiny_repo, "add", "scripts/new_plain.py")
    assert not gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["scripts/new_plain.py"], register={})


def test_edge_class_census_admits_a_module_that_ALREADY_had_the_shape_at_HEAD(
        tiny_repo: Path, tiny_store):
    """THE RATCHET'S WHOLE POINT, and the direction that makes it landable.

    `old_scanner.py` is one of the eighteen in miniature: shaped, unverdicted, and live.
    Editing it must NOT refuse -- the migration it owes is a W-G3 lane's act, and a gate
    that refused it would refuse every commit in the repo on a defect the committer cannot
    repair. The set may shrink; it may not grow.
    """
    path = tiny_repo / "scripts" / "old_scanner.py"
    path.write_text(SHAPED + "\n\ndef also(root):\n    return edges(root)\n",
                    encoding="utf-8", newline="\n")
    _git(tiny_repo, "add", "scripts/old_scanner.py")
    assert not gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["scripts/old_scanner.py"], register={})


def test_edge_class_census_refuses_a_module_that_NEWLY_acquires_the_shape(tiny_repo: Path,
                                                                          tiny_store):
    """THE SECOND TRIP, and the hole the add-only reading would leave.

    `plain.py` is committed without the shape. Growing it one is exactly the act the ratchet
    exists to catch, and an add-only predicate would miss every one of them.
    """
    (tiny_repo / "scripts" / "plain.py").write_text(SHAPED, encoding="utf-8", newline="\n")
    _git(tiny_repo, "add", "scripts/plain.py")
    findings = gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["scripts/plain.py"], register={})
    assert [f.subject for f in findings] == ["scripts/plain.py"]


def test_edge_class_census_looks_only_at_scripts(tiny_repo: Path, tiny_store):
    """`plugins/` holds DERIVED COPIES whose source lives in `scripts/` and is verdicted
    there. Scanning both would refuse a copy for its source's shape."""
    _write(tiny_repo / "plugins" / "p" / "scripts" / "copy.py", SHAPED)
    _git(tiny_repo, "add", "-A")
    assert not gq.edge_class_census(tiny_repo, tiny_store,
                                    staged=["plugins/p/scripts/copy.py"], register={})


def test_edge_class_census_is_silent_during_a_merge(tiny_repo: Path, tiny_store, monkeypatch):
    """A MERGE IS TRANSPORT, NOT AUTHORSHIP -- the carve-out `task_coverage` already sets.

    It binds the GIT-DERIVED staged set only, so an explicit `staged=` is still checked;
    otherwise a merge would be a hole rather than a carve-out.
    """
    _write(tiny_repo / "scripts" / "new_scanner.py", SHAPED)
    _git(tiny_repo, "add", "scripts/new_scanner.py")
    monkeypatch.setattr(gq, "_merge_in_progress", lambda root: True)
    assert gq.edge_class_census(tiny_repo, tiny_store, staged=None, register={}) == []
    assert gq.edge_class_census(tiny_repo, tiny_store,
                                staged=["scripts/new_scanner.py"], register={})


# --------------------------------------------- leg 2: the register cannot rot into paper


def test_edge_class_census_refuses_a_register_row_whose_file_is_gone(tiny_repo: Path,
                                                                     tiny_store):
    """THE THIRD TRIP -- ADR-75's decoration rule, applied to this register.

    A row naming a file that is gone is the register answering from a stale roster, which
    is the class `stale_dispositions()` already pins one register over.
    """
    register = {"scripts/ghost.py": PRIVATE}
    findings = gq.edge_class_census(tiny_repo, tiny_store, staged=[], register=register)
    assert [f.subject for f in findings] == ["scripts/ghost.py"]
    assert "gone" in findings[0].evidence


def test_edge_class_census_refuses_a_register_row_whose_SYMBOL_is_gone(tiny_repo: Path,
                                                                       tiny_store):
    """Two of the live rows are FUNCTIONS inside `audit.py`, not whole modules.

    A row pinned at `<path>::<symbol>` whose file survives a rename of that symbol would
    otherwise suppress silently, which is the same rot one level down.
    """
    register = {"scripts/old_scanner.py::vanished": PRIVATE}
    findings = gq.edge_class_census(tiny_repo, tiny_store, staged=[], register=register)
    assert [f.subject for f in findings] == ["scripts/old_scanner.py::vanished"]

    register = {"scripts/old_scanner.py::edges": PRIVATE}
    assert not gq.edge_class_census(tiny_repo, tiny_store, staged=[], register=register)


# ------------------------------------------------------------------------ the CLI trip-test


def test_edge_class_census_cli_exits_non_zero_on_a_refusal(tiny_repo: Path, tmp_path: Path):
    """THE TRIP-TEST the frozen contract names: the REFUSAL, at the exit code the hook reads.

    A query that reports without refusing discharges nothing.
    """
    _write(tiny_repo / "scripts" / "new_scanner.py", SHAPED)
    _git(tiny_repo, "add", "scripts/new_scanner.py")
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    code = gq.main(["edge-class-census", "--repo-root", str(tiny_repo), "--db", str(db),
                    "--staged", "scripts/new_scanner.py", "--empty-register"])
    assert code != 0


def test_edge_class_census_cli_exits_zero_on_a_clean_tree(tiny_repo: Path, tmp_path: Path):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_repo, db)
    code = gq.main(["edge-class-census", "--repo-root", str(tiny_repo), "--db", str(db),
                    "--staged", "scripts/plain.py", "--empty-register"])
    assert code == 0


# ------------------------------------------------------------------- the live tree, measured


def test_every_register_row_carries_a_kind_from_the_FIVE_KIND_class():
    """The class is closed: citation, generation, template, test, script call-site.

    A sixth kind is a widening of DECLARE-REVIEWS section A.1 and is a ruling, not a row.
    The one exception is a `not-an-edge` row, whose whole content is that no kind applies.
    """
    assert gq.EDGE_COMPUTATIONS, "an empty register measures nothing"
    for key, row in gq.EDGE_COMPUTATIONS.items():
        expected = (gq.NO_KIND,) if row.status == "not-an-edge" else gq.FIVE_KINDS
        assert row.kind in expected, f"{key} carries a kind outside the closed class"


def test_every_register_row_carries_a_status_and_an_owner():
    for key, row in gq.EDGE_COMPUTATIONS.items():
        assert row.status in gq.REGISTER_STATUSES, key
        assert row.owner.strip(), f"{key} names no owner -- an unowned row is a wish"


def test_a_NEGATIVE_verdict_is_expressible_and_admits_the_module():
    """THE REGISTER MUST BE ABLE TO SAY NO, and this is the direction that proves it.

    The shape predicate favours recall, so it will keep finding modules that read source
    text for something other than corpus structure. Without `not-an-edge` the only way to
    admit one would be a false `private` row -- inflating N, handing a W-G3 lane a migration
    that does not exist, and making the number this query reports a lie.

    A `not-an-edge` row must NOT count toward N, which is the half a status alone would not
    guarantee.
    """
    register = {"scripts/x.py": gq._not_an_edge("reads its own source, not the corpus")}
    metrics = gq.edge_class_metrics(REPO_ROOT, register)
    assert metrics == {"private": 0, "reconciled": 0, "migrated": 0, "not_an_edge": 1}


def test_the_census_verdicts_ITSELF_out_of_the_class():
    """Found by the gate refusing the very commit that armed it.

    `graph_queries.py` grew an `ast` walk in that change and matched its own predicate. Its
    subject is a MODULE'S SHAPE, never a relation between two corpus files, so there is no
    edge here to read from FPG-1 -- which is what `not-an-edge` says and `private` would not.
    """
    row = gq.EDGE_COMPUTATIONS["scripts/graph_queries.py"]
    assert row.status == "not-an-edge"
    assert row.kind == gq.NO_KIND


def test_every_register_row_names_a_live_file_and_a_live_symbol():
    """The live half of leg 2. A stale row here is a paper suppression on the real tree."""
    assert not gq.stale_edge_computations(REPO_ROOT)


def test_every_register_row_actually_HAS_the_shape_it_is_registered_for():
    """The register and the predicate must agree, or the ratchet is measuring a different
    population from the one it records. Twenty files, twenty-one rows."""
    unshaped = [key for key in gq.EDGE_COMPUTATIONS
                if not gq.is_edge_computation_shape(
                    (REPO_ROOT / key.split("::")[0]).read_text(encoding="utf-8"))]
    assert unshaped == []


def test_the_live_register_measures_EIGHTEEN_private_computations():
    """N, PINNED so a migration moves it deliberately rather than silently.

    Eighteen private, three reconciled as FPG-1 inputs -- lane `v-664`'s section 2.5
    measurement, re-measured here on the merged tree. A W-G3 migration lane flips a row to
    `reconciled` and edits this number in the same commit, which is what makes `migrated`
    a count rather than a claim.
    """
    metrics = gq.edge_class_metrics(REPO_ROOT)
    assert metrics["private"] == 18
    assert metrics["reconciled"] == 3


def test_the_live_tree_does_not_refuse_its_own_edge_class_census():
    """Armed means landable. If this is RED the hook refuses every commit in the repo."""
    store = gs.ensure(REPO_ROOT)
    try:
        assert gq.edge_class_census(REPO_ROOT, store, staged=[]) == []
    finally:
        store.close()
