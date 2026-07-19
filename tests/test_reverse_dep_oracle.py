"""Tests for scripts/reverse_dep_oracle.py (#193 code->code reverse-dep oracle, ADR-89).

Two tiers:
  * unit (always run, no Pyright) — resolution, provenance shape, declaration-exclusion,
    fail-soft for BOTH startup-failure modes (missing langserver AND unspawnable/dies-on-
    start), text rendering.
  * integration (skipif Pyright not vendored) — the headline fixture: querying `Finding`
    (scripts/audit.py, ~110 real refs) resolves with provenance attached.
"""

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_ORACLE = _REPO_ROOT / "scripts" / "reverse_dep_oracle.py"


def _load():
    spec = importlib.util.spec_from_file_location("reverse_dep_oracle", _ORACLE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclass + `from __future__ import annotations` needs it
    spec.loader.exec_module(module)
    return module


oracle = _load()

# Pyright is vendored (npm install) when node is on PATH AND the langserver resolves.
_PYRIGHT_AVAILABLE = (
    shutil.which("node") is not None and oracle.find_langserver(_REPO_ROOT) is not None
)
requires_pyright = pytest.mark.skipif(
    not _PYRIGHT_AVAILABLE, reason="pyright langserver not vendored — run `npm install`"
)


def _mk_repo(tmp_path, files):
    (tmp_path / "scripts").mkdir()
    for name, content in files.items():
        (tmp_path / "scripts" / name).write_text(content, encoding="utf-8")
    return tmp_path


# --- symbol resolution -----------------------------------------------------------------

def test_resolve_unique_symbol(tmp_path):
    repo = _mk_repo(tmp_path, {"a.py": "def bar():\n    pass\n"})
    defs = oracle.resolve_symbol("bar", repo)
    assert len(defs) == 1
    assert defs[0].name == "bar" and defs[0].file == "scripts/a.py"


def test_resolve_not_found(tmp_path):
    repo = _mk_repo(tmp_path, {"a.py": "def bar():\n    pass\n"})
    assert oracle.resolve_symbol("nope", repo) == []


def test_resolve_ambiguous_then_narrow(tmp_path):
    repo = _mk_repo(
        tmp_path, {"a.py": "def foo():\n    pass\n", "b.py": "def foo():\n    pass\n"}
    )
    assert len(oracle.resolve_symbol("foo", repo)) == 2          # ambiguous
    narrowed = oracle.resolve_symbol("foo", repo, file="b.py")    # --file disambiguates
    assert len(narrowed) == 1 and narrowed[0].file == "scripts/b.py"


def test_position_points_at_name_not_keyword():
    """Finding is `class Finding` at audit.py — name identifier is 0-based char 6."""
    defs = oracle.resolve_symbol("Finding", _REPO_ROOT)
    assert len(defs) == 1
    d = defs[0]
    assert d.file == "scripts/audit.py"
    assert d.kind == "ClassDef"
    assert d.character == 6          # len("class ") — points at the F, not the keyword
    assert d.line == 274            # 0-based (audit.py:275 is 1-based)


# --- provenance ------------------------------------------------------------------------

def test_git_provenance_matches_repo_state():
    prov = oracle.git_provenance(_REPO_ROOT)
    head = oracle._git(_REPO_ROOT, "rev-parse", "HEAD").stdout.strip()
    assert prov["git_rev"] == head
    assert isinstance(prov["dirty_files"], list)
    assert prov["dirty"] == bool(prov["dirty_files"])


def test_provenance_block_always_has_three_caveats():
    p = oracle._provenance(_REPO_ROOT, "complete")
    assert p["reflects"] == "working-tree"
    assert p["completeness"] == "complete"
    assert len(p["caveats"]) == 3
    joined = " ".join(p["caveats"])
    assert "static-python-only" in joined
    assert "repo-scoped" in joined
    assert "working-tree" in joined
    assert p["oracle"]["method"] == "textDocument/references"


@pytest.mark.parametrize("status", ["symbol-not-found", "ambiguous", "oracle-unavailable"])
def test_every_envelope_carries_provenance(status):
    env = oracle._envelope("X", None, status, _REPO_ROOT, reason="r")
    assert env["schema"] == "reverse-dep-oracle/v1"
    assert len(env["provenance"]["caveats"]) == 3
    assert "git_rev" in env["provenance"]


# --- declaration exclusion -------------------------------------------------------------

def test_extract_dependents_excludes_declaration():
    audit = (_REPO_ROOT / "scripts" / "audit.py").resolve()
    def_uri = oracle.uri(audit)
    defn = oracle.Definition("scripts/audit.py", "Finding", "ClassDef", 227, 6)
    locations = [
        {"uri": def_uri, "range": {"start": {"line": 227, "character": 6}}},        # decl
        {"uri": def_uri.lower(), "range": {"start": {"line": 227, "character": 6}}},  # decl, lc drive
        {"uri": def_uri, "range": {"start": {"line": 311, "character": 12}}},        # a referencer
    ]
    deps = oracle._extract_dependents(locations, defn, _REPO_ROOT)
    assert deps == [{"file": "scripts/audit.py", "line": 312}]  # decl (228) gone; ref -> 1-based


# --- langserver resolution + fail-soft (BOTH startup-failure modes) --------------------

def test_find_langserver_none_when_absent(tmp_path):
    assert oracle.find_langserver(tmp_path) is None     # no node_modules, nothing on PATH


def test_find_langserver_vendored(tmp_path):
    ls = tmp_path / "node_modules" / "pyright" / "langserver.index.js"
    ls.parent.mkdir(parents=True)
    ls.write_text("// stub", encoding="utf-8")
    argv = oracle.find_langserver(tmp_path)
    assert argv[0] == "node" and argv[-1] == "--stdio" and "langserver.index.js" in argv[1]


def test_lsp_spawn_failure_raises_oracle_unavailable():
    """Mode 1: an unspawnable argv (node missing) -> OracleUnavailable, not a raw OSError."""
    with pytest.raises(oracle.OracleUnavailable):
        oracle.LSP(["definitely-not-a-real-binary-xyz-193", "--stdio"])


def test_run_oracle_fail_soft_when_no_langserver(tmp_path):
    """Mode 2a: langserver absent -> oracle-unavailable envelope (install hint), never crash."""
    repo = _mk_repo(tmp_path, {"a.py": "def bar():\n    pass\n"})
    ans = oracle.run_oracle("bar", None, repo)
    assert ans["resolution"]["status"] == "oracle-unavailable"
    assert "npm install" in ans["resolution"]["reason"]
    assert ans["resolution"]["definition"]["file"] == "scripts/a.py"   # resolved before spawn
    assert len(ans["provenance"]["caveats"]) == 3


def test_run_oracle_fail_soft_on_spawn_death(tmp_path, monkeypatch):
    """Mode 2b: langserver resolves but the process can't start (dies on spawn) -> still the
    SAME oracle-unavailable envelope, never a stack-trace (gate-safety contract)."""
    repo = _mk_repo(tmp_path, {"a.py": "def bar():\n    pass\n"})
    monkeypatch.setattr(
        oracle, "find_langserver", lambda *a, **k: ["not-a-real-binary-xyz-193", "--stdio"]
    )
    ans = oracle.run_oracle("bar", None, repo)
    assert ans["resolution"]["status"] == "oracle-unavailable"
    assert ans["reverse_dependent_count"] == 0


def test_run_oracle_not_found(tmp_path):
    repo = _mk_repo(tmp_path, {"a.py": "def bar():\n    pass\n"})
    ans = oracle.run_oracle("ghost", None, repo)
    assert ans["resolution"]["status"] == "symbol-not-found"


def test_run_oracle_ambiguous(tmp_path):
    repo = _mk_repo(
        tmp_path, {"a.py": "def foo():\n    pass\n", "b.py": "def foo():\n    pass\n"}
    )
    ans = oracle.run_oracle("foo", None, repo)
    assert ans["resolution"]["status"] == "ambiguous"
    assert len(ans["resolution"]["candidates"]) == 2


# --- text rendering (CLAUDE.md §4: flat + fenced) --------------------------------------

def test_format_text_is_fenced_and_lists_caveats():
    defn = oracle.Definition("scripts/audit.py", "Finding", "ClassDef", 227, 6)
    env = oracle._envelope(
        "Finding", None, "resolved", _REPO_ROOT, definition=defn,
        reverse_dependents=[{"file": "scripts/audit.py", "line": 312}],
        completeness="complete",
    )
    text = oracle.format_text(env)
    assert text.startswith("```\n") and text.endswith("\n```")
    assert "reverse-dependents of Finding" in text
    assert "scripts/audit.py:312" in text
    assert "caveats:" in text


def test_format_text_renders_unavailable():
    env = oracle._envelope("X", None, "oracle-unavailable", _REPO_ROOT, reason="boom")
    text = oracle.format_text(env)
    assert text.startswith("```") and "oracle-unavailable: boom" in text


# --- integration: the headline fixture (requires vendored Pyright) ---------------------

@requires_pyright
def test_finding_headline_resolves_with_provenance():
    """#193 closure metric: Finding's real referencers, with provenance attached."""
    ans = oracle.run_oracle("Finding", None, _REPO_ROOT, timeout=40)
    res = ans["resolution"]
    assert res["status"] == "resolved", ans
    assert res["definition"]["file"] == "scripts/audit.py"
    assert res["definition"]["line"] == 275                  # 1-based output
    assert ans["reverse_dependent_count"] >= 50              # floor (measured ~110), drift-robust
    # the declaration site is not its own reverse-dependent
    assert {"file": "scripts/audit.py", "line": 275} not in ans["reverse_dependents"]
    prov = ans["provenance"]
    assert prov["completeness"] == "complete"
    assert prov["git_rev"]
    assert len(prov["caveats"]) == 3


@requires_pyright
def test_main_finding_json_exit_zero(capsys):
    import json as _json
    rc = oracle.main(["Finding", "--json", "--timeout", "40"])
    assert rc == 0
    payload = _json.loads(capsys.readouterr().out)
    assert payload["resolution"]["status"] == "resolved"
    assert payload["reverse_dependent_count"] >= 50
