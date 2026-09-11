"""Impacted-test selection -- a changed file selects the tests that cover it ([#278]).

WHAT THIS IS FOR. PLAYBOOK Ch5 splits the suite into a targeted in-lane tier A and one
full tier-B suite at integration, and says in the repo's own voice that the general
form of tier A -- "tier A plus anything covering the touched module" -- was ABSENT:

    The general form is *tier A plus anything covering the touched module*, which is
    [#278] (impacted-test selection); until that lands, the named-module rule above is
    its checkable subset.   -- protocols/PLAYBOOK.md

This module is that general form. It never replaces the full suite: AW2-1 keeps "the
integrator keeps one full suite per integration as the net", and the measured in-lane
miss-rate below is only acceptable BECAUSE that net exists.

WHY AN IMPORT GRAPH AND NOT A COVERAGE PLUGIN. Chosen by measurement, not preference,
and both legs' numbers are recorded in
`docs/audits/2026-09-11-technical-w278-selector-leg-measurement.md`. The short form:
`pytest-testmon` scores a perfect miss-rate against a coverage oracle because it
IMPLEMENTS that oracle's definition, while 72.6 % of this repo's (test, script)
path-string edges -- 53 of 73 -- are invisible to in-process coverage, since 82 of 171
test files use `subprocess` and a governance repo is full of tests that assert on a
source file's TEXT. It also needs a ~50-minute cold coverage DB per checkout, and
ADR-110 gives every lane a FRESH worktree. FPG-1's AST pass sees the string edges,
needs no persisted state, and adds no dependency.

THIS IS A CONNECT, NOT A SECOND GRAPH. ADR-118 section 1 rules that the repo has one
graph and organs are views over it, so the module map and the call-site edge reader are
FPG-1's (`_script_module_map`, `_import_targets`) rather than re-implemented here.
`test_the_fpg1_seam_this_module_connects_to_still_exists` fails loudly if either is
renamed, because the alternative is selection degrading in silence.

HONEST LIMITS, measured rather than left to be discovered:

  * Miss-rate 0.048 over 31 scored diffs -- roughly one affected test file in twenty is
    not selected. Tier B is what catches those.
  * Precision (macro) 0.680: the selected set is a superset of the affected set. That is
    the safe direction, and it is bounded by DEFAULT_DEPTH.
  * DEPTH IS LOAD-BEARING. FPG-1's closure is transitive and this repo has hub modules
    most tests import, so unbounded, "tests reaching scripts/fleet_health.py" answers 76
    of 173 test files where the truth is 7. Miss-rate stops improving past depth 3 while
    precision keeps decaying, so depth 3 is where the dial was set -- by the number.
  * Selection is computed from the repo TREE, so it answers for the working state, not
    for an arbitrary historical commit.
"""
from __future__ import annotations

import logging
import pathlib
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field

import click

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import file_purpose_graph as fpg

logger = logging.getLogger(__name__)

#: Bounded transitive import depth. Set by measurement, not taste -- see the module
#: docstring and the leg-measurement audit. Raising it lowers precision and does NOT
#: lower the miss-rate (0.064 at depth 3 and at unbounded, before the convention rule).
DEFAULT_DEPTH = 3

#: The pytest marker that selects the tests asserting against the LIVE repo tree. It is
#: this repo's already-declared docs-only tier (`pyproject.toml` markers, `/ship`), not a
#: new vocabulary invented here.
LIVE_REPO_MARKER = "live_repo"

#: Where test files live.
TEST_ROOTS = ("tests", "plugins/tier1-lifecycle/tests")

#: Where importable first-party source lives.
SOURCE_ROOTS = ("scripts", "deploy", "plugins")

#: A change to one of these can move ANY test, so narrowing would be a guess. The
#: fail-safe direction is the full suite.
ENVIRONMENT_FILES = frozenset({
    "pyproject.toml",
    "uv.lock",
    ".python-version",
    "conftest.py",
    ".pre-commit-config.yaml",
})

#: Suffixes that cannot change Python behaviour but CAN break a live-tree assertion.
DOC_SUFFIXES = (".md", ".yaml", ".yml", ".json", ".txt", ".cfg", ".ini", ".toml")


@dataclass(frozen=True)
class Rule:
    """One mapping rule: which changed paths it claims, and what it selects.

    `reason` is not decoration -- a selection a reader cannot audit is a selection
    nobody will trust, so every rule has to be able to say why it fired.
    """

    name: str
    kind: str  # "self" | "covering" | "marker" | "full"
    reason: str
    matches: Callable[[str], bool]


def _is_test(rel: str) -> bool:
    return any(
        rel.startswith(f"{root}/") and rel.rsplit("/", 1)[-1].startswith("test_")
        for root in TEST_ROOTS
    ) and rel.endswith(".py")


def _is_source(rel: str) -> bool:
    return rel.endswith(".py") and any(
        rel.startswith(f"{root}/") for root in SOURCE_ROOTS
    )


def _is_environment(rel: str) -> bool:
    return rel in ENVIRONMENT_FILES or rel.rsplit("/", 1)[-1] == "conftest.py"


def _is_doc(rel: str) -> bool:
    return rel.endswith(DOC_SUFFIXES)


#: THE MAPPING. Order matters: the first rule that claims a path wins, and the
#: environment rule is deliberately ahead of the doc rule so `pyproject.toml` reaches the
#: full suite rather than the markdown tier. Emptying this tuple is what the RED-first
#: witness `test_the_mapping_is_load_bearing_and_its_removal_is_RED` detects.
RULES: tuple[Rule, ...] = (
    Rule("environment", "full",
         "an environment or hook-config file can move any test; narrowing is a guess",
         _is_environment),
    Rule("changed-test", "self",
         "a changed test file is its own impacted test",
         _is_test),
    Rule("source-import-closure", "covering",
         "tests reaching this module through FPG-1 import edges, plus the "
         "test_<x>.py naming convention",
         _is_source),
    Rule("live-tree-doc", "marker",
         "a docs/config change can only break tests that assert against the live tree",
         _is_doc),
)


@dataclass(frozen=True)
class Selection:
    """What to run, and why.

    `full_suite` is not "everything was selected" -- it is the explicit fail-safe, and
    callers must treat it as "this mechanism declined to narrow".
    """

    test_files: tuple[str, ...] = ()
    marker: str | None = None
    full_suite: bool = False
    reasons: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def pytest_args(self) -> list[str]:
        """The argv tail a caller hands to pytest.

        THE MARKER AND A FILE LIST MUST NEVER BE EMITTED TOGETHER. `pytest -m live_repo
        a.py b.py` INTERSECTS them -- it runs only the live_repo-marked tests inside
        those files, silently dropping every covering test that carries no marker. A
        mixed diff therefore resolves the marker to its FILES in `select()` and emits a
        plain union; `-m` survives only for the pure docs-only case, which is the
        repo's already-declared `/ship` docs tier.
        """
        if self.full_suite:
            return []
        if self.marker and not self.test_files:
            return ["-m", self.marker]
        return list(self.test_files)


def all_test_files(repo_root: pathlib.Path) -> tuple[str, ...]:
    """Every test file in the corpus, repo-relative posix."""
    out: list[str] = []
    for root in TEST_ROOTS:
        directory = repo_root / root
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("test_*.py")):
            rel = path.relative_to(repo_root).as_posix()
            if "__pycache__" not in rel:
                out.append(rel)
    return tuple(out)


def live_repo_test_files(repo_root: pathlib.Path) -> tuple[str, ...]:
    """Test files carrying the `live_repo` marker, found statically.

    Static rather than by `pytest -m live_repo --collect-only`, which costs a full
    collection (29 s measured) every time a gate wants an answer. The scan matches both
    spellings this repo uses -- a module-level `pytestmark` and a per-test decorator.

    HONEST LIMIT: this selects the whole FILE when any test in it is marked, so it is a
    superset of `-m live_repo`. That is the safe direction, and it is only used for a
    MIXED diff; a pure docs-only diff still emits `-m live_repo` exactly.
    """
    out: list[str] = []
    for rel in all_test_files(repo_root):
        try:
            text = (repo_root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if LIVE_REPO_MARKER in text:
            out.append(rel)
    return tuple(out)


def _module_map(repo_root: pathlib.Path) -> dict[str, str]:
    """FPG-1's dotted-name map, widened to the roots FPG-1 does not walk.

    FPG-1's PROCESS_ROOTS are scripts/, plugins/, .claude/commands and .claude/skills --
    `tests/` is deliberately not a process root, so the live graph carries no test node.
    Selection needs tests as import SOURCES, so the map is widened here rather than by
    changing what FPG-1 considers a process, which would move the orphan census.
    """
    base = dict(fpg._script_module_map(repo_root))
    claims: dict[str, set[str]] = {}
    for sub in (*TEST_ROOTS, "deploy"):
        directory = repo_root / sub
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            rel = path.relative_to(repo_root).as_posix()
            if "__pycache__" in rel:
                continue
            parts = rel[: -len(".py")].split("/")
            for start in range(len(parts)):
                claims.setdefault(".".join(parts[start:]), set()).add(rel)
    for name, owners in claims.items():
        # FPG-1's rule, kept: a name two modules would claim buys NO edge rather than
        # the wrong one (the census's recorded error 2).
        if len(owners) == 1 and name not in base:
            base[name] = next(iter(owners))
    return base


def _direct_edges(repo_root: pathlib.Path, modules: dict[str, str]) -> dict[str, set[str]]:
    """relpath -> files it imports or names in call position, via FPG-1's reader."""
    edges: dict[str, set[str]] = {}
    for sub in (*SOURCE_ROOTS, *TEST_ROOTS):
        directory = repo_root / sub
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            rel = path.relative_to(repo_root).as_posix()
            if "__pycache__" in rel:
                continue
            try:
                edges[rel] = set(fpg._import_targets(path, repo_root, modules))
            except (OSError, SyntaxError):
                logger.warning("impacted-tests: unreadable source %s", rel)
                edges[rel] = set()
    return edges


def _closure(edges: dict[str, set[str]], start: str, depth: int) -> set[str]:
    seen: set[str] = set()
    frontier = {start}
    for _ in range(depth):
        nxt: set[str] = set()
        for cur in frontier:
            for tgt in edges.get(cur, ()):
                if tgt not in seen and tgt != start:
                    seen.add(tgt)
                    nxt.add(tgt)
        if not nxt:
            break
        frontier = nxt
    return seen


def _convention_pairs(repo_root: pathlib.Path) -> dict[str, list[str]]:
    """source relpath -> tests naming it by the `test_<x>.py` convention.

    This rule is not a stylistic nicety. It recovers ONE measured class the AST pass
    cannot see: a test that loads its subject with
    `importlib.util.spec_from_file_location` and a composed path, where the filename is
    a string constant in a BinOp rather than in call position. Measured effect:
    miss-rate 0.064 -> 0.048, with precision unchanged-to-better.
    """
    stems: dict[str, list[str]] = {}
    for root in SOURCE_ROOTS:
        directory = repo_root / root
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.py"):
            rel = path.relative_to(repo_root).as_posix()
            if "__pycache__" not in rel:
                stems.setdefault(path.stem, []).append(rel)
    pairs: dict[str, list[str]] = {}
    for root in TEST_ROOTS:
        directory = repo_root / root
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("test_*.py")):
            trel = path.relative_to(repo_root).as_posix()
            for src in stems.get(path.stem[len("test_"):], []):
                pairs.setdefault(src, []).append(trel)
    return pairs


def covering_tests(repo_root: pathlib.Path, depth: int = DEFAULT_DEPTH) -> dict[str, list[str]]:
    """source relpath -> the test files that cover it. The mapping's core table."""
    modules = _module_map(repo_root)
    edges = _direct_edges(repo_root, modules)
    covers: dict[str, set[str]] = {}
    for test in all_test_files(repo_root):
        for reached in _closure(edges, test, depth):
            covers.setdefault(reached, set()).add(test)
    for src, tests in _convention_pairs(repo_root).items():
        covers.setdefault(src, set()).update(tests)
    return {k: sorted(v) for k, v in covers.items()}


def select(
    repo_root: pathlib.Path | str,
    changed: Iterable[str],
    depth: int = DEFAULT_DEPTH,
    rules: Sequence[Rule] | None = None,
) -> Selection:
    """Select the tests impacted by `changed`.

    `rules=()` is not a trick parameter -- it is how the RED-first witness proves the
    mapping is load-bearing. With no rules, nothing is claimed and the selector reports
    the fail-safe rather than an answer it cannot justify.
    """
    root = pathlib.Path(repo_root).resolve()
    active = RULES if rules is None else tuple(rules)
    paths = [str(c).replace("\\", "/") for c in changed]

    selected: set[str] = set()
    reasons: dict[str, tuple[str, ...]] = {}
    marker: str | None = None
    full = False
    unclaimed: list[str] = []
    need_covering: list[str] = []

    for rel in paths:
        for rule in active:
            if not rule.matches(rel):
                continue
            reasons[rel] = (rule.name, rule.reason)
            if rule.kind == "full":
                full = True
            elif rule.kind == "self":
                selected.add(rel)
            elif rule.kind == "marker":
                marker = LIVE_REPO_MARKER
            elif rule.kind == "covering":
                need_covering.append(rel)
            break
        else:
            unclaimed.append(rel)

    if unclaimed:
        # An unmapped path is the one case where guessing is worse than paying the
        # suite: the mechanism does not know what it cannot see.
        full = True
        for rel in unclaimed:
            reasons[rel] = ("unmapped", "no rule claims this path; failing safe")

    if need_covering:
        table = covering_tests(root, depth=depth)
        for rel in need_covering:
            selected.update(table.get(rel, ()))

    if full:
        return Selection(full_suite=True, reasons=reasons)

    if marker and selected:
        # MIXED diff. Resolving the marker to files here is what keeps `pytest_args`
        # from emitting `-m` alongside a file list, which pytest would read as an
        # intersection and quietly under-select. See `Selection.pytest_args`.
        selected.update(live_repo_test_files(root))

    return Selection(
        test_files=tuple(sorted(selected)), marker=marker, reasons=reasons
    )


def changed_from_git(repo_root: pathlib.Path, ref: str | None = None) -> list[str]:
    """Changed paths from git -- staged plus unstaged, or against `ref` when given."""
    import subprocess

    args = ["git", "diff", "--name-only"]
    if ref:
        args.append(ref)
    else:
        args.append("HEAD")
    out = subprocess.run(
        args, cwd=repo_root, capture_output=True, text=True, check=False
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


@click.command()
@click.option("--repo-root", default=".", help="Repository root to select against.")
@click.option("--changed", multiple=True, help="Changed path (repeatable).")
@click.option("--ref", default=None, help="Select against a git ref instead.")
@click.option("--depth", default=DEFAULT_DEPTH, show_default=True,
              help="Bounded transitive import depth.")
@click.option("--explain", is_flag=True, help="Print why each path selected what it did.")
def main(repo_root: str, changed: tuple[str, ...], ref: str | None,
         depth: int, explain: bool) -> None:
    """Print the pytest arguments for the tests impacted by a change."""
    root = pathlib.Path(repo_root).resolve()
    paths = list(changed) or changed_from_git(root, ref)
    if not paths:
        click.echo("# no changed paths; nothing to select")
        return
    sel = select(root, paths, depth=depth)
    if explain:
        for rel, (name, why) in sorted(sel.reasons.items()):
            click.echo(f"# {rel}: [{name}] {why}", err=True)
        click.echo(f"# selected {len(sel.test_files)} test file(s)", err=True)
    if sel.full_suite:
        click.echo("# FULL SUITE -- the selector declined to narrow")
        return
    click.echo(" ".join(sel.pytest_args()))


if __name__ == "__main__":
    main()
