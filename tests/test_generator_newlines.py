"""Tests for the generator newline defect witnessed 2026-08-01 during the intake #23 filing.

The defect: a generator that writes through `Path.write_text()` / `open(..., "w")` WITHOUT a
`newline=` argument inherits the platform's text-mode translation. On Windows that rewrites
every LF to CRLF. `gen_intake_tree.py` then splits its source on "\\n" and matches the
INTAKE-INDEX markers with exact equality, so the trailing "\\r" makes `in_block` never fire and
the residue carrier regenerates with ZERO item nodes -- a silently empty carrier, caught live
only by the item-set integrity leg added after the 2026-07-31 codex-review HIGH.

Why these tests are platform-independent: the bug reproduces only where `os.linesep` is CRLF,
so a plain assertion would vacuously pass on Linux CI and never guard anything. The behavioural
test therefore SIMULATES the translating platform by patching `Path.write_text` to do what
Windows text mode does, then asserts the generator's on-disk bytes are still LF. A generator
that passes `newline="\\n"` survives the simulation; one that omits it does not.

The source-level test is the fleet guard: it holds the invariant across every current and
future write site in `scripts/` -- RECURSIVELY, subpackages included. The first version swept
non-recursively and let `scripts/toc/cli.py` through while reporting green (codex HIGH,
2026-08-01); `test_the_sweep_reaches_nested_script_packages` now pins the recursion itself.
"""

import ast
import importlib.util
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = _REPO_ROOT / "scripts"

_ORIG_WRITE_TEXT = Path.write_text


def _load(name: str):
    """Load a scripts/ module by path -- scripts/ is not an importable package."""
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _translating_write_text(self, data, encoding=None, errors=None, newline=None):
    """Emulate Windows text mode: with newline unset, every "\\n" becomes "\\r\\n".

    Mirrors io.TextIOWrapper's documented behaviour (newline=None -> os.linesep). An explicit
    newline="\\n" disables translation, which is exactly the property under test.
    """
    if newline is None:
        data = data.replace("\n", "\r\n")
    return _ORIG_WRITE_TEXT(self, data, encoding=encoding, errors=errors, newline="")


def test_simulation_itself_reproduces_the_defect(tmp_path):
    """Guard the guard: the simulation must actually translate, or every test below is vacuous."""
    target = tmp_path / "probe.md"
    _translating_write_text(target, "a\nb\n")
    assert target.read_bytes() == b"a\r\nb\r\n", "simulation does not translate -- tests are vacuous"

    _translating_write_text(target, "a\nb\n", newline="\n")
    assert target.read_bytes() == b"a\nb\n", "explicit newline= must defeat the simulation"


def _scanned_files() -> list[Path]:
    """Every .py under scripts/, RECURSIVELY. Subpackages are in scope -- see the regression."""
    return sorted(_SCRIPTS.rglob("*.py"))


def test_the_sweep_reaches_nested_script_packages():
    """Regression for the codex HIGH (2026-08-01): the sweep was non-recursive.

    The first version of this guard used glob("*.py"), which skipped scripts/toc/cli.py --
    a generator that writes the PLAYBOOK ToC and had the very defect being swept for. The
    guard reported GREEN while a live generator could still emit CRLF. A guard that misses a
    subpackage is worse than no guard, because it is believed.
    """
    scanned = _scanned_files()
    nested = [p for p in scanned if p.parent != _SCRIPTS]
    assert nested, "no nested scripts/ package found -- this assertion would be vacuous"
    assert _SCRIPTS / "toc" / "cli.py" in scanned, (
        "scripts/toc/cli.py is not scanned -- the sweep has regressed to non-recursive glob()"
    )


def _write_sites() -> list[tuple[Path, int, str]]:
    """Every text-mode write in scripts/ that does NOT pin `newline=`, found by AST."""
    out: list[tuple[Path, int, str]] = []
    for path in _scanned_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            passed = {kw.arg for kw in node.keywords}
            if isinstance(node.func, ast.Attribute) and node.func.attr == "write_text":
                if "newline" not in passed:
                    out.append((path, node.lineno, "write_text()"))
            elif isinstance(node.func, ast.Name) and node.func.id == "open":
                mode = ""
                if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                    mode = node.args[1].value or ""
                for kw in node.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        mode = kw.value.value or ""
                if "w" in mode and "b" not in mode and "newline" not in passed:
                    out.append((path, node.lineno, "open()"))
    return out


def test_every_text_write_in_scripts_pins_newline():
    """The fleet guard: no write site may inherit platform newline translation.

    Uniform rule with no exemption list, deliberately -- an exemption list is the thing that
    rots. Binary writes and reads are out of scope by construction (mode check above).
    """
    offenders = _write_sites()
    rendered = "\n".join(
        f"  {p.relative_to(_REPO_ROOT).as_posix()}:{line}: {what} missing newline="
        for p, line, what in offenders
    )
    assert not offenders, (
        f"{len(offenders)} text write(s) in scripts/ inherit platform newline translation "
        f'-- pass newline="\\n" (see generate_floor._write_text_lf for the precedent):\n'
        f"{rendered}"
    )


def _capture_write(monkeypatch) -> dict:
    """Intercept Path.write_text on a simulated translating platform WITHOUT touching disk.

    Redirecting the generator's `_TARGET` to tmp_path is not viable: several generators render
    a repo-relative path for their own output line, which raises on an out-of-tree target. So
    the write itself is captured instead -- the repo file is never opened for writing.
    """
    seen: dict[str, bytes] = {}

    def capture(self, data, encoding=None, errors=None, newline=None):
        if newline is None:  # platform translation, exactly what Windows text mode does
            data = data.replace("\n", "\r\n")
        seen["bytes"] = data.encode(encoding or "utf-8")
        return len(data)

    monkeypatch.setattr(Path, "write_text", capture)
    return seen


@pytest.mark.parametrize(
    "module_name", ["gen_audit_index", "gen_intake_index", "gen_doc_counts"]
)
def test_generator_writes_lf_on_a_translating_platform(module_name, monkeypatch):
    """Behavioural leg: regenerate on a simulated CRLF-writing platform, assert the bytes are LF."""
    module = _load(module_name)
    seen = _capture_write(monkeypatch)

    write = module._cmd_write
    # gen_doc_counts takes a run_expensive flag; keep the cheap path.
    kwargs = {"run_expensive": False} if "run_expensive" in write.__code__.co_varnames else {}
    write(**kwargs)

    assert seen.get("bytes"), f"{module_name} wrote nothing"
    assert b"\r\n" not in seen["bytes"], (
        f"{module_name} emitted CRLF on a translating platform -- its write must pin "
        f'newline="\\n". This is the defect that regenerates the intake carrier with zero '
        f"item nodes."
    )


def test_intake_carrier_survives_a_regenerated_index(monkeypatch):
    """The end-to-end failure the defect actually caused: index regen must not blind the split.

    gen_intake_tree matches its markers with exact equality after splitting on "\\n", so a CRLF
    README yields zero item nodes. This asserts the two generators stay composable.
    """
    index = _load("gen_intake_index")
    tree = _load("gen_intake_tree")

    seen = _capture_write(monkeypatch)
    index._cmd_write()
    monkeypatch.undo()

    model = tree.parse_readme(seen["bytes"].decode("utf-8"))
    item_nodes = [n for n in model.nodes if n.kind == "item"]
    assert item_nodes, (
        "regenerating the index produced a README the split engine reads as ZERO item nodes "
        "-- the exact silent-empty-carrier failure witnessed on 2026-08-01"
    )
