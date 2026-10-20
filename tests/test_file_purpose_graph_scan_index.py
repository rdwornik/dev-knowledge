"""Tests for `_implements_scan_paths` in scripts/file_purpose_graph.py.

Pins the returned file list, and that the walk never visits `.claude/worktrees/` (a full
checkout per live lane) rather than visiting it and filtering the results afterwards.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_P = _REPO / "scripts" / "file_purpose_graph.py"
_MODNAME = "scripts.file_purpose_graph"


def _load():
    spec = importlib.util.spec_from_file_location(_MODNAME, _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules[_MODNAME] = module
    spec.loader.exec_module(module)
    return module


fpg = _load()


def _write(path: Path, text: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _build(root: Path) -> None:
    for name in ("a.md", "b.yaml", "JOURNAL.md", "x.txt"):
        _write(root / name)
    _write(root / "scripts" / "m.py")
    _write(root / "scripts" / "sub" / "n.py")
    _write(root / "scripts" / "__pycache__" / "z.pyc")
    _write(root / "scripts" / "big.py", "a" * (fpg.IMPLEMENTS_MAX_BYTES + 1))
    _write(root / "docs" / "d.md")
    _write(root / ".claude" / "c.md")
    for lane in ("lane1", "lane2", "lane3"):
        base = root / ".claude" / "worktrees" / lane
        for i in range(10):
            _write(base / f"f{i}.md")
            _write(base / "scripts" / f"s{i}.py")
            _write(base / "docs" / "deep" / f"d{i}.md")


def test_paths_equal_expected_list(tmp_path):
    _build(tmp_path)

    result = fpg._implements_scan_paths(tmp_path)

    assert [p.relative_to(tmp_path).as_posix() for p in result] == [
        "a.md",
        "b.yaml",
        "scripts/m.py",
        "scripts/sub/n.py",
        ".claude/c.md",
        "docs/d.md",
    ]


class _CountingScandir:
    def __init__(self, inner, hits, prefix):
        self._inner = inner
        self._hits = hits
        self._prefix = prefix

    def __enter__(self):
        self._inner.__enter__()
        return self

    def __exit__(self, *exc):
        return self._inner.__exit__(*exc)

    def __iter__(self):
        return self

    def __next__(self):
        entry = next(self._inner)
        if entry.path.replace("\\", "/").startswith(self._prefix):
            self._hits.append(entry.path)
        return entry

    def close(self):
        self._inner.close()


def test_no_entries_visited_under_worktrees(tmp_path, monkeypatch):
    _build(tmp_path)
    prefix = (tmp_path / ".claude" / "worktrees").as_posix()
    hits: list[str] = []

    real_scandir = os.scandir
    real_rglob = pathlib.Path.rglob

    def scandir(*args, **kwargs):
        return _CountingScandir(real_scandir(*args, **kwargs), hits, prefix)

    def rglob(self, *args, **kwargs):
        for path in real_rglob(self, *args, **kwargs):
            if path.as_posix().startswith(prefix):
                hits.append(str(path))
            yield path

    monkeypatch.setattr(os, "scandir", scandir)
    monkeypatch.setattr(pathlib.Path, "rglob", rglob)

    fpg._implements_scan_paths(tmp_path)

    assert len(hits) == 0
