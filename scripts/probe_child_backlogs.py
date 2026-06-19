#!/usr/bin/env python
"""probe_child_backlogs.py — #120 child-BACKLOG schema-conformance probe.

The READINESS GATE that precedes distribution of the `validate-backlog` pre-commit
hook to child repos. It answers one question per child: *is this child's BACKLOG.md
already conformant to the schema the hook would enforce?* — so turning the hook on in
a child can't immediately wedge that child's commits. It DISTRIBUTES NOTHING and edits
no child; the prerequisite, not the distribution.

Floor-faithful criterion (the load-bearing design choice, operator-ruled): a child is
CONFORMANT iff the FLOOR ARTIFACT's validate() returns zero hard-fails. The floor
artifact is the plugin script `plugins/tier1-lifecycle/scripts/validate_backlog.py` —
the validator that becomes a child's hook when validate-backlog is distributed via the
`tier1-lifecycle` plugin — NOT the hub's `scripts/validate_backlog.py` directly (the floor
is a check-minimal twin of it). As of #186 the floor carries the hub's #156 task-graph
checks (depends-on reference-existence + no-cycle) on top of the ADR-66 structural checks,
so a child with a dangling depends-on edge or a dependency cycle now classifies as
needs-migration. The probe mirrors the floor AS-SHIPPED so it greenlights exactly the
children that would pass the hook they'd actually install (zero drift) — the probe and the
installed hook stay in lockstep by construction (the former #156 floor-gap is closed).

Verdicts (per child):
  conformant       BACKLOG.md present, floor validate() clean (warnings are informational)
  needs-migration  BACKLOG.md present, floor validate() reports >=1 hard-fail
  absent           repo reached but no BACKLOG.md at its root
  unreachable      repo dir not found / BACKLOG.md unreadable
  unparseable      validator raised (defensive; the floor parse/validate is permissive)

Layer-2 / read-only contract (ADR-28/36): reads each child read-only; the only side
effect is stdout (recording is operator-captured — no hub file written). Awareness layer,
NOT a gate: exit 0 in every normal case (findings included); nonzero only when the floor
validator itself can't be loaded (a genuine install error). Fail-soft on discovery: a
missing/malformed registry yields "no children", never a crash.

Discovery reuses the established cascade (audit.py / fleet_health.py): the tracked
`ecosystem/index.yaml` is the primary repo list (robust in a fresh clone where the
gitignored `ecosystem/*/state.yaml` may be absent); per child the path resolves
state.yaml `path:` -> index `path:` -> `<hub_parent>/<name>`. `--repo-path PATH`
(repeatable) overrides the registry. The hub self-entry is excluded (the hub guards its
own BACKLOG via the live pre-commit hook).

Usage:
    python scripts/probe_child_backlogs.py
    python scripts/probe_child_backlogs.py --repo-path ../some-repo
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple, Optional

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_ECOSYSTEM_DIR = _REPO_ROOT / "ecosystem"
_ECOSYSTEM_INDEX = _ECOSYSTEM_DIR / "index.yaml"
# The artifact that becomes a child's hook (see module docstring) — NOT scripts/validate_backlog.py.
_PLUGIN_VB = _REPO_ROOT / "plugins" / "tier1-lifecycle" / "scripts" / "validate_backlog.py"

# The hub's canonical ecosystem name (CLAUDE.md §2 repo identity). The hub guards its own
# BACKLOG via the live pre-commit hook, so it is excluded from the child set — by this name
# AND by run-dir/path identity, so the exclusion holds whether the probe runs from the
# `.dev-knowledge` primary checkout or a `dev-knowledge-NNN` worktree (a different dir name).
HUB_CANONICAL_NAME = ".dev-knowledge"

_VERDICT_ORDER = ("conformant", "needs-migration", "absent", "unreachable", "unparseable")


class Child(NamedTuple):
    name: str
    path: Optional[Path]


class ChildResult(NamedTuple):
    name: str
    path: Optional[Path]
    verdict: str
    detail: str
    n_hard: int
    n_warn: int


# ---------------------------------------------------------------------------
# Floor validator load (explicit-path importlib so it never collides with the
# hub's same-named scripts/validate_backlog.py; import is side-effect-free).
# ---------------------------------------------------------------------------

def load_floor_validator(path: Path = _PLUGIN_VB):
    """Load the plugin floor validate_backlog as a module under a distinct name."""
    spec = importlib.util.spec_from_file_location("floor_validate_backlog", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load floor validator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def _read_index(index_path: Path) -> list:
    """Return [(name, path_or_None)] from ecosystem/index.yaml. Fail-soft: [] on any error."""
    try:
        data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    if not isinstance(data, dict):
        return []
    out = []
    for r in data.get("repos") or []:
        if not isinstance(r, dict):
            continue
        name = r.get("name")
        if not name:
            continue
        p = r.get("path")
        out.append((name, Path(p) if p else None))
    return out


def _read_ecosystem_dirs(ecosystem_dir: Path) -> list:
    """Fallback registry: ecosystem/<name>/ dirs carrying a state.yaml. Mirrors audit.discover_repos."""
    if not ecosystem_dir.exists():
        return []
    return [
        (d.name, None)
        for d in sorted(ecosystem_dir.iterdir())
        if d.is_dir() and (d / "state.yaml").exists()
    ]


def _state_path_field(ecosystem_dir: Path, name: str) -> Optional[Path]:
    """The machine-local `path:` from ecosystem/<name>/state.yaml, or None. Fail-soft."""
    sp = ecosystem_dir / name / "state.yaml"
    try:
        d = yaml.safe_load(sp.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if isinstance(d, dict) and d.get("path"):
        return Path(d["path"])
    return None


def _resolve_child_path(name: str, index_path: Optional[Path], ecosystem_dir: Path,
                        repo_root: Path) -> Path:
    """state.yaml path -> index path -> <hub_parent>/<name>; first that exists, else fallback."""
    fallback = repo_root.parent / name
    for cand in (_state_path_field(ecosystem_dir, name), index_path, fallback):
        if cand and cand.exists():
            return cand
    return fallback


def discover_children(repo_root: Path, index_path: Path, ecosystem_dir: Path,
                      explicit_paths: Optional[list] = None) -> list:
    """Return [Child(name, path)] for every registered child, hub self-entry excluded.

    --repo-path overrides the registry (and is NOT hub-filtered — an explicit ask wins).
    Otherwise read index.yaml (fall back to state.yaml-dir discovery), resolve each path,
    drop the hub self-entry (by canonical name, run-dir name, or path identity), dedup by name.
    """
    if explicit_paths:
        out = []
        for p in explicit_paths:
            rp = Path(p).resolve()
            out.append(Child(rp.name, rp))
        return out

    entries = _read_index(index_path) or _read_ecosystem_dirs(ecosystem_dir)
    hub_names = {HUB_CANONICAL_NAME.lower(), repo_root.name.lower()}
    repo_root_real = repo_root.resolve()
    children, seen = [], set()
    for name, idx_path in entries:
        if name.lower() in hub_names:
            continue
        path = _resolve_child_path(name, idx_path, ecosystem_dir, repo_root)
        if path.resolve() == repo_root_real:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        children.append(Child(name, path))
    return children


# ---------------------------------------------------------------------------
# Conformance classification (against the injected floor validator)
# ---------------------------------------------------------------------------

def _summarize_hard(hard: list) -> str:
    head = "; ".join(hard[:3])
    if len(hard) > 3:
        head += f" (+{len(hard) - 3} more)"
    return head


def classify_backlog(repo_path: Optional[Path], validator) -> tuple:
    """Return (verdict, detail, n_hard, n_warn) for one repo's BACKLOG.md against `validator`."""
    if repo_path is None or not repo_path.exists():
        where = f": {repo_path}" if repo_path is not None else ""
        return "unreachable", f"repo dir not found{where}", 0, 0
    backlog = repo_path / "BACKLOG.md"
    if not backlog.exists():
        return "absent", "no BACKLOG.md at repo root", 0, 0
    try:
        text = backlog.read_text(encoding="utf-8")
    except OSError as e:
        return "unreachable", f"could not read BACKLOG.md: {e}", 0, 0
    try:
        themes, stories, tasks = validator.parse(text)
        hard, warn = validator.validate(themes, stories, tasks)
    except Exception as e:  # defensive — the probe must never crash on one bad child
        return "unparseable", f"floor validator raised: {type(e).__name__}", 0, 0
    if hard:
        return "needs-migration", f"{len(hard)} hard-fail(s): {_summarize_hard(hard)}", len(hard), len(warn)
    n_themes = sum(1 for t in themes if t != validator.BIG_PICTURE)
    detail = f"({n_themes} themes, {len(stories)} stories, {len(tasks)} tasks)"
    return "conformant", detail, 0, len(warn)


# ---------------------------------------------------------------------------
# Report (flat ASCII — no U+2192 arrow; child-derived detail stays cp1252-safe)
# ---------------------------------------------------------------------------

def format_report(results: list, hub_name: str = HUB_CANONICAL_NAME) -> str:
    n = len(results)
    lines = [f"probe_child_backlogs: {n} child repo(s) registered (hub {hub_name} excluded)", ""]
    for r in results:
        lines.append(f"  {r.verdict.upper():<16} {r.name:<26} {r.detail}")
    lines.append("")
    counts = Counter(r.verdict for r in results)
    parts = [f"{counts.get(v, 0)} {v}" for v in _VERDICT_ORDER if v != "unparseable" or counts.get(v)]
    lines.append(f"probe_child_backlogs: {', '.join(parts)} (of {n} children)")
    return "\n".join(lines)


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Probe each child repo's BACKLOG.md for ADR-66 floor conformance (read-only).")
    parser.add_argument("--repo-path", action="append", default=[], metavar="PATH",
                        help="probe an explicit repo (repeatable); bypasses the ecosystem registry")
    args = parser.parse_args(argv)

    try:
        validator = load_floor_validator()
    except Exception as e:  # a genuine install error is the one nonzero exit
        print(f"probe_child_backlogs: could not load the floor validator {_PLUGIN_VB}: {e}",
              file=sys.stderr)
        return 1

    children = discover_children(_REPO_ROOT, _ECOSYSTEM_INDEX, _ECOSYSTEM_DIR, args.repo_path)
    if not children:
        print("probe_child_backlogs: 0 child repo(s) registered — nothing to probe "
              "(no ecosystem registry and no --repo-path)")
        return 0

    results = [ChildResult(c.name, c.path, *classify_backlog(c.path, validator)) for c in children]
    print(format_report(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
