"""AST-based package and import-edge extraction for codemap generation."""
from __future__ import annotations

import ast
import sys
from pathlib import Path


def analyze_repo(repo_path: Path, source_root: str = "src") -> dict:
    """Return packages and intra-source import edges for a repo.

    Returns {"packages": [str, ...], "edges": [(str, str), ...]} — sorted.
    Skips relative, star, and dynamic imports conservatively.
    """
    src_dir = repo_path / source_root
    if not src_dir.is_dir():
        print(
            f"warning: source root '{src_dir}' not found — returning empty graph",
            file=sys.stderr,
        )
        return {"packages": [], "edges": []}

    packages = sorted(
        p.name
        for p in src_dir.iterdir()
        if p.is_dir() and (p / "__init__.py").exists()
    )
    package_set = set(packages)

    edge_set: set[tuple[str, str]] = set()

    for pkg_name in packages:
        pkg_dir = src_dir / pkg_name
        for py_file in pkg_dir.rglob("*.py"):
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(py_file))
            except (SyntaxError, OSError):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0]
                        if top in package_set and top != pkg_name:
                            edge_set.add((pkg_name, top))

                elif isinstance(node, ast.ImportFrom):
                    if node.level and node.level > 0:
                        continue
                    if node.module is None:
                        continue
                    # skip star imports
                    if any(a.name == "*" for a in node.names):
                        continue
                    top = node.module.split(".")[0]
                    if top in package_set and top != pkg_name:
                        edge_set.add((pkg_name, top))

    edges = sorted(edge_set)
    return {"packages": packages, "edges": edges}
