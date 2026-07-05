"""Orchestration: ast_walker + tach.toml layer extraction + text_emit.

Output form is compact text per ADR-51 amendment 2026-07-05; ``mermaid_emit``
is retained for the human-facing visualization surface but no longer wired in.
"""
from __future__ import annotations

import sys
from pathlib import Path

from .ast_walker import analyze_repo
from .text_emit import emit_text


def _load_tach_layers(repo_path: Path) -> dict[str, str]:
    """Parse tach.toml [modules] for layer assignments.

    Returns {} on missing file or parse failure (degraded mode).
    """
    tach_file = repo_path / "tach.toml"
    if not tach_file.exists():
        return {}

    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

    try:
        data = tomllib.loads(tach_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"warning: could not parse tach.toml: {exc}", file=sys.stderr)
        return {}

    layers: dict[str, str] = {}
    modules = data.get("modules", [])
    if not isinstance(modules, list):
        return {}
    for mod in modules:
        if isinstance(mod, dict):
            name = mod.get("path") or mod.get("name", "")
            layer = mod.get("layer", "")
            if name and layer:
                layers[str(name)] = str(layer)
    return layers


def generate_codemap(repo_path: Path, source_root: str = "src") -> tuple[str, list[str]]:
    """Return (codemap_text, warnings).

    warnings is a list of stderr-bound strings for orphan/cycle/tach issues.
    """
    data = analyze_repo(repo_path, source_root)
    packages: list[str] = data["packages"]
    edges: list[tuple[str, str]] = data["edges"]

    layers = _load_tach_layers(repo_path)

    warnings: list[str] = []

    # Orphan detection
    connected = set()
    for src, dst in edges:
        connected.add(src)
        connected.add(dst)
    orphans = [p for p in packages if p not in connected]
    if orphans:
        warnings.append(f"orphan modules (no edges): {', '.join(sorted(orphans))}")

    # Cycle detection (simple reachability check — emit_mermaid does the real DFS)
    adj: dict[str, list[str]] = {p: [] for p in packages}
    for src, dst in edges:
        adj[src].append(dst)

    def has_cycle() -> bool:
        color = {p: 0 for p in packages}

        def dfs(node: str) -> bool:
            color[node] = 1
            for nb in adj[node]:
                if color[nb] == 1 or (color[nb] == 0 and dfs(nb)):
                    return True
            color[node] = 2
            return False

        return any(dfs(p) for p in packages if color[p] == 0)

    if has_cycle():
        warnings.append("circular imports detected — cycle edges marked in codemap")

    codemap_text = emit_text(
        packages, edges, layers=layers, source_root=source_root
    )
    return codemap_text, warnings
