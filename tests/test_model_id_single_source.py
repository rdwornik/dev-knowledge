r"""[#1536] (5): a registry model id is written in the registry, not in `scripts/`.

The scanner is an AST walk over `scripts/**/*.py`: every string `Constant` that is not a
module/class/function docstring, matched against the registry's `models:` keys (longest first,
boundary `(?<![\w.-])` ... `(?![\w-])`). Today's literals are a frozen, grandfathered baseline:
the counts may only shrink and no new (path, id) pair may appear.
"""
from __future__ import annotations

import ast
import re
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parent.parent

BASELINE: dict[tuple[str, str], int] = {
    ("scripts/decision_coverage.py", "grok-4.6"): 1,
    ("scripts/decision_coverage.py", "grok-4.7"): 1,
    ("scripts/dispatch.py", "claude-haiku-4-5-20251001"): 1,
    ("scripts/dispatch.py", "claude-opus-5-5"): 2,
    ("scripts/dispatch.py", "claude-sonnet-5"): 2,
    ("scripts/dispatch_surface.py", "claude-sonnet-5"): 1,
    ("scripts/gen_seat_boot.py", "gpt-5.6-terra"): 1,
    ("scripts/plan_lint.py", "claude-haiku-4-5-20251001"): 1,
    ("scripts/plan_lint.py", "claude-opus-5-5"): 2,
    ("scripts/plan_lint.py", "claude-sonnet-5"): 1,
    ("scripts/provider_bench.py", "claude-sonnet-5"): 1,
    ("scripts/routing_agreement.py", "claude-sonnet-5"): 1,
}


def registry_ids() -> list[str]:
    data = yaml.safe_load(
        (_ROOT / "ecosystem" / "provider-registry.yaml").read_text(encoding="utf-8")
    )
    return list(data["models"])


def _docstring_nodes(tree: ast.AST) -> set[int]:
    skip: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                skip.add(id(body[0].value))
    return skip


def scan(root: Path, ids: Iterable[str]) -> Counter:
    """Count (relative posix path, id) -> live string-constant occurrences under root/scripts."""
    ordered = sorted(set(ids), key=len, reverse=True)
    if not ordered:
        return Counter()
    pattern = re.compile(
        r"(?<![\w.-])(" + "|".join(re.escape(i) for i in ordered) + r")(?![\w-])"
    )
    found: Counter = Counter()
    for path in sorted((root / "scripts").rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        skip = _docstring_nodes(tree)
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                    and id(node) not in skip):
                for m in pattern.finditer(node.value):
                    found[(rel, m.group(1))] += 1
    return found


# Judge round 1 (A): MODEL-SHAPED tokens that are NOT registered ids. Measured live 2026-10-16;
# grandfathered, may only shrink.
UNREGISTERED_BASELINE: dict[tuple[str, str], int] = {
    ("scripts/gen_seat_boot.py", "gpt-5.6"): 1,
    ("scripts/provider_bench.py", "claude-fable-5.1"): 1,
    ("scripts/provider_bench.py", "gpt-5"): 1,
}

_MODEL_SHAPED = re.compile(
    r"(?<![\w.-])(claude-[a-z]+-[0-9][\w.-]*"
    r"|gpt-[0-9][\w.-]*|grok-[0-9][\w.-]*|gemini-[0-9][\w.-]*)(?![\w-])"
)


def scan_unregistered(root: Path, registered: Iterable[str]) -> Counter:
    """Count (relative posix path, token) for model-shaped string-constant tokens under
    root/scripts whose value is not a registered id (docstrings excluded)."""
    known = set(registered)
    found: Counter = Counter()
    for path in sorted((root / "scripts").rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        skip = _docstring_nodes(tree)
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                    and id(node) not in skip):
                for m in _MODEL_SHAPED.finditer(node.value):
                    token = m.group(1).rstrip(".-")
                    if token not in known:
                        found[(rel, token)] += 1
    return found


def violations(
    root: Path,
    registered: Iterable[str],
    baselines: tuple[dict[tuple[str, str], int], dict[tuple[str, str], int]],
) -> list[str]:
    """Combined policy: registered-id literals and unregistered model-shaped literals, each
    against its own grandfathered baseline."""
    registered = list(registered)
    registered_baseline, unregistered_baseline = baselines
    problems: list[str] = []
    for live, baseline in (
        (scan(root, registered), registered_baseline),
        (scan_unregistered(root, registered), unregistered_baseline),
    ):
        for (path, mid), n in sorted(live.items()):
            allowed = baseline.get((path, mid), 0)
            if n > allowed:
                problems.append(f"model-id literal outside the registry: {path} {mid} "
                                f"(x{n}, baseline {allowed})")
    return problems


def test_r1536_live_unregistered_scan_never_exceeds_its_baseline():
    live = scan_unregistered(_ROOT, registry_ids())
    problems = []
    for (path, mid), n in sorted(live.items()):
        allowed = UNREGISTERED_BASELINE.get((path, mid), 0)
        if n > allowed:
            problems.append(f"model-id literal outside the registry: {path} {mid} "
                            f"(x{n}, baseline {allowed})")
    assert not problems, "\n".join(problems)


def test_r1536_a_planted_unregistered_literal_is_flagged(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "x.py").write_text('MODEL = "claude-unregistered-9"\n',
                                               encoding="utf-8")
    registered = registry_ids()
    assert "claude-unregistered-9" not in registered
    assert scan_unregistered(tmp_path, registered) == Counter(
        {("scripts/x.py", "claude-unregistered-9"): 1}
    )
    found = violations(tmp_path, registered, ({}, {}))
    assert found and "scripts/x.py claude-unregistered-9" in found[0]
    assert found[0].startswith("model-id literal outside the registry: ")


def test_r1536_a_tree_with_no_literals_has_no_violations(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "z.py").write_text(
        '"""claude-unregistered-9 in a docstring."""\n'
        'TOOL = "claude-code"\nNAME = "gpt-terra"\n',
        encoding="utf-8",
    )
    assert violations(tmp_path, registry_ids(), ({}, {})) == []


def test_r1536_live_tree_has_no_violations_beyond_the_baselines():
    assert violations(_ROOT, registry_ids(), (BASELINE, UNREGISTERED_BASELINE)) == []


def test_r1536_live_scan_never_exceeds_the_grandfathered_baseline():
    live = scan(_ROOT, registry_ids())
    problems = []
    for (path, mid), n in sorted(live.items()):
        allowed = BASELINE.get((path, mid), 0)
        if n > allowed:
            problems.append(f"model-id literal outside the registry: {path} {mid} "
                            f"(x{n}, baseline {allowed})")
    assert not problems, "\n".join(problems)


def test_r1536_a_planted_literal_is_flagged(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "x.py").write_text('MODEL = "claude-sonnet-5-5"\n', encoding="utf-8")
    found = scan(tmp_path, ["claude-sonnet-5", "claude-sonnet-5-5"])
    assert found == Counter({("scripts/x.py", "claude-sonnet-5-5"): 1})


def test_r1536_docstring_and_comment_mentions_are_not_flagged(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "y.py").write_text(
        '"""Module doc names claude-sonnet-5-5."""\n'
        "# comment: claude-sonnet-5-5\n"
        "def f():\n"
        '    """claude-sonnet-5-5 in a docstring."""\n'
        "    return 1\n",
        encoding="utf-8",
    )
    assert not scan(tmp_path, ["claude-sonnet-5-5"])
