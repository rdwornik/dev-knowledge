#!/usr/bin/env python
"""worktree_import_proof.py — does THIS checkout's pytest import THIS checkout's source? ([#429])

WHAT THIS IS
------------
[#429]'s done-when, verbatim: *"a satellite can provision a worktree AND prove by a runnable
check that its pytest imports THAT worktree's source"*. This module is that check. It is the
half the row calls unbuilt, and it is deliberately the FIRST thing built, because leg (b) —
the per-worktree venv — is a remedy whose absence is silent without it.

THE FAILURE IT EXISTS TO CATCH, stated once. A shared editable install lives in an interpreter's
site-packages and points at ONE checkout. Inside a git worktree of the same repo, `import pkg`
therefore resolves to the PRIMARY checkout's source. The worktree's `pytest` then exercises code
the lane never touched and reports the result against the lane's branch: **green tests about the
wrong tree, with nothing in the output saying so.** That is the exact silent-failure class this
fleet hunts, and no amount of documentation survives it — a note in a doc does not fail a build.

WHY IT RUNS PYTEST RATHER THAN JUST IMPORTING. The row says *its pytest*, not *its interpreter*,
and the distinction is load-bearing: pytest inserts rootdir/conftest paths of its own, loads
plugins, and honours an ini file that can add `pythonpath` or `testpaths`. An `import` performed
by this script would prove a claim about a DIFFERENT process than the one whose greenness is
being trusted. So the proof spawns the repo's real pytest, under the repo's own ini, and asks
the assertion from inside a collected test — the same process shape that produces the green.

The same reasoning is why the child runs under `PYTHONSAFEPATH` (see `_child_env`): matching the
repo's pytest is not enough if the proof's own *entry point* injects a path the real command
would not. A proof whose verdict depends on how the proof was launched is not a proof.

PORTABILITY IS THE POINT (leg (a)). Nothing here is hub-shaped: the package list is read from
the target repo's own `pyproject.toml`, the interpreter is discovered per-checkout, and the
repo may carry no `.worktreeinclude` at all. `ai-council` — the row's named satellite, verified
to have no manifest — is the proving subject, and it is reached by pointing `--repo` at it.

POSTURE — READ-ONLY, AND WIRED INTO NO GATE. Layer 2 (ADR-28/36): it drives no state in a child
repo, and it does not RUN one either. The generated test resolves each package with `find_spec`
rather than importing it, so no child-repo module body executes — an `import` would have run
arbitrary sibling code with whatever import-time side effects it carries, which is a step beyond
anything else in `scripts/` (those shell out to `git`, never to the child's own code). The
distinction costs nothing here: resolution is the entire question, and `find_spec` walks the same
finders over the same `sys.path` that `import` would. Found by terra, second pass.
It writes exactly one file, into the system temp directory, and removes it; the target
tree is never written to — `-p no:cacheprovider` suppresses `.pytest_cache` and
`PYTHONDONTWRITEBYTECODE` suppresses `__pycache__`, so the no-leftovers round-trip holds even
on the repo being proved. Both were found by the test that asserts it rather than assumed.
Whether it should gate is a separate ruling — the `/preflight` adoption-first precedent.

EXIT CODES — a skip never greens.
  0  PASS            every declared package resolved inside the checkout
  1  FAIL            at least one resolved outside it, or pytest could not run the proof
  2  internal error  the tool could not look (an error BLOCKS; it never reports a silent pass)
  3  NOT-APPLICABLE  the repo declares no importable package AND no pytest ini to root
A distinct code for NOT-APPLICABLE is deliberate. Folding it into 0 would let a repo the tool
cannot actually examine report the same verdict as one it examined and cleared — which is the
failure mode the whole module exists to refuse.

WHAT "READ-ONLY" DOES AND DOES NOT COVER, measured rather than asserted (terra, third pass).
The proof spawns the target checkout's interpreter and its pytest. That is irreducible: the row
asks whether *its pytest* imports the right source, and no static read answers that. What it
does NOT do is run the target's own code, and each route was closed or checked:
  * the selected packages are RESOLVED, never imported (`find_spec`), and only ever by their
    TOP-LEVEL name — `find_spec("pkg.sub")` would import `pkg` to read its `__path__`, so a
    dotted name is reduced at discovery and refused again inside the generated test;
  * installed pytest plugins do not autoload (`PYTEST_DISABLE_PLUGIN_AUTOLOAD`), which is the
    one route by which a repo could get its own code executed by entry point;
  * the target's `conftest.py` is NOT loaded — **verified, not reasoned**: a sentinel appended
    to ai-council's root conftest never fired across four runs. The collected test file lives
    in the system temp directory, and conftest discovery walks the *collected args'* ancestors,
    which never reach the repo. (Independent corroboration: ai-council's root conftest RAISES on
    a wrong-tree import, and the wrong-tree run reported a clean FAIL rather than aborting.)
  * the repo's pytest ini is read as DATA (`-c`), which is configuration, not execution.
So the residual is exactly "the target's interpreter and pytest run", which the done-when
requires, and nothing wider. Stated here rather than left to a reader to discover.

HONEST LIMITS
  * A conforming IMPORT is not a conforming ENVIRONMENT. This proves where the source came
    from, not that the dependency set matches the lock. `uv run --locked` covers that axis.
  * The package list comes from `pyproject.toml`. A repo that ships an importable package
    without declaring it there is invisible to the discovery step — `--packages` is the
    override, and the report always names which packages it actually checked, so a short list
    is readable as a short list rather than as a clean bill of health.
  * A repo with no per-checkout venv is not refused up front. The proof runs against whatever
    interpreter the checkout resolves to and lets the import location decide, because "no venv"
    is a diagnosis, not a verdict: a repo with no importable package is unaffected by it.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2
EXIT_NOT_APPLICABLE = 3

#: Written into the system temp dir, collected by the target repo's pytest, deleted after.
#: It reports rather than asserts: a failed assertion inside pytest yields a traceback, while
#: the caller needs the resolved paths for BOTH outcomes to write a useful report.
_PROOF_TEST = '''\
"""Generated by scripts/worktree_import_proof.py — deleted when the run ends.

RESOLVES, NEVER IMPORTS. `find_spec` runs the same finders on the same `sys.path` that `import`
would, and returns the origin it WOULD have loaded — without executing the target package's
module body. That answers the question exactly (which checkout does this name resolve to?)
while keeping a Layer-2 hub tool from running arbitrary child-repo code with import-time side
effects. Do not "simplify" this back to `import_module`.
"""
import importlib.util
import json
import os
import pathlib


def test_imports_resolve_inside_this_checkout(pytestconfig):
    root = pathlib.Path(os.environ["WT_PROOF_ROOT"]).resolve()
    names = [n for n in os.environ["WT_PROOF_PACKAGES"].split(",") if n]
    resolved = {}
    for name in names:
        if "." in name:  # a dotted name would make find_spec import the parent - never resolve one
            resolved[name] = {"error": f"ValueError: refusing a dotted name {name!r}"}
            continue
        try:
            spec = importlib.util.find_spec(name)
        except Exception as exc:  # noqa: BLE001 - an unresolvable package is a reportable result
            resolved[name] = {"error": f"{type(exc).__name__}: {exc}"}
            continue
        if spec is None:
            resolved[name] = {"error": f"ModuleNotFoundError: No module named {name!r}"}
            continue
        origin = spec.origin
        if origin is None or origin == "namespace":
            paths = [str(pathlib.Path(p).resolve())
                     for p in (spec.submodule_search_locations or [])]
            resolved[name] = {"namespace_paths": paths}
            continue
        resolved[name] = {"file": str(pathlib.Path(origin).resolve())}
    payload = {
        "root": str(root),
        "rootdir": str(pathlib.Path(str(pytestconfig.rootpath)).resolve()),
        "executable": str(pathlib.Path(os.sys.executable).resolve()),
        "prefix": str(pathlib.Path(os.sys.prefix).resolve()),
        "packages": resolved,
    }
    pathlib.Path(os.environ["WT_PROOF_OUT"]).write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
'''


#: Interpreters tried, in order, when the checkout has no `.venv` of its own. `py` leads on
#: purpose: the Windows launcher lives in `C:\Windows` and starts the SYSTEM interpreter, so it
#: is the one name no venv activation can shadow. That matters because the system interpreter is
#: where a shared editable install actually lives — the ai-council repo-root conftest names it
#: as the cause in as many words ("a bare `python` / `py` resolves `ai_council` to the primary
#: checkout from any cwd"). Resolving to whatever venv the CALLER happened to have active would
#: make the verdict a property of this seat rather than of the target repo.
_FALLBACK_INTERPRETERS = ("py", "python3", "python")


class ProofError(Exception):
    """Raised when the tool cannot look — distinct from looking and finding a bad import."""


@dataclass
class Proof:
    """One checkout, examined."""

    root: Path
    packages: tuple[str, ...]
    interpreter: list[str]
    venv_inside_checkout: bool
    rootdir: Path | None = None
    resolved: dict[str, dict] = field(default_factory=dict)
    outside: list[str] = field(default_factory=list)
    pytest_returncode: int | None = None
    pytest_output: str = ""

    @property
    def passed(self) -> bool:
        return self.pytest_returncode == 0 and not self.outside and bool(self.resolved)


# --- discovery --------------------------------------------------------------------------

def resolve_root(repo: Path) -> Path:
    """The checkout `repo` sits in. Inside a linked worktree this is the WORKTREE root, which
    is the whole point — `--show-toplevel` reports the working tree, not the common git dir."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProofError(f"cannot run git in {repo}: {exc}") from exc
    if proc.returncode != 0:
        raise ProofError(f"not a git checkout: {repo} ({proc.stderr.strip()})")
    return Path(proc.stdout.strip()).resolve()


def _read_pyproject(root: Path) -> dict:
    path = root / "pyproject.toml"
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProofError(f"cannot read {path}: {exc}") from exc


def _package_dir_exists(root: Path, name: str) -> bool:
    """True when `name` is on disk here as a real package — under the root or a `src/` layout.
    Discovery is filtered through this so a declared-but-absent name is not reported as a
    package the proof "checked": an import that could never have resolved locally proves
    nothing about which checkout won.

    PEP 420 IS A PACKAGE TOO (terra P1, fifth pass). A namespace package has no `__init__.py`,
    so an `__init__.py`-only predicate reports the repo as having nothing importable and the CLI
    answers NOT-APPLICABLE — a disclosed skip rather than a false pass, but still a supported
    packaging style going unchecked. A directory is accepted when it ships modules at its top
    level or one level down. The depth bound is deliberate: an unbounded `rglob` over a
    `node_modules`-shaped tree turns a fast predicate into a slow one, and a namespace package
    whose only `.py` files are three levels deep is not a shape worth paying for.
    """
    top = name.split(".")[0]
    for base in (root, root / "src"):
        candidate = base / top
        if (candidate / "__init__.py").is_file() or (base / f"{top}.py").is_file():
            return True
        if candidate.is_dir() and (
            any(candidate.glob("*.py")) or any(candidate.glob("*/__init__.py"))
        ):
            return True
    return False


def top_level(name: str) -> str:
    """`pkg.subpkg` -> `pkg`. Every name this module handles is reduced to its top-level segment.

    This is a Layer-2 requirement, not tidiness (terra P1, fourth pass). `find_spec("pkg.subpkg")`
    has to IMPORT `pkg` to read its `__path__` before it can look inside — so a dotted name would
    execute child-repo code by the back door, through the very call chosen to avoid executing it.
    Nothing is lost by resolving only the top level: the top-level package's origin is what
    determines which checkout the whole subtree comes from, which is the entire question.
    """
    return name.split(".")[0]


def declared_packages(root: Path) -> tuple[str, ...]:
    """Importable package names this repo declares, filtered to those that exist on disk.

    Two sources, in order: the setuptools `include` globs (`ai_council*` -> `ai_council`), then
    the distribution name normalised to an import name (`ai-council` -> `ai_council`). The
    second is the fallback because a repo may configure packaging in a way this does not model;
    the disk filter is what keeps either source from inventing a name.
    """
    data = _read_pyproject(root)
    found: list[str] = []

    includes = (
        data.get("tool", {})
        .get("setuptools", {})
        .get("packages", {})
        .get("find", {})
        .get("include", [])
    )
    for pattern in includes:
        if not isinstance(pattern, str):
            continue
        name = top_level(pattern.rstrip("*").rstrip("."))
        if name and _package_dir_exists(root, name) and name not in found:
            found.append(name)

    if not found:
        dist = data.get("project", {}).get("name")
        if isinstance(dist, str):
            name = top_level(dist.replace("-", "_"))
            if _package_dir_exists(root, name):
                found.append(name)

    return tuple(found)


def _venv_python(root: Path) -> Path | None:
    """The checkout's OWN interpreter, if it has one materialised."""
    for relative in ("Scripts/python.exe", "bin/python"):
        candidate = root / ".venv" / relative
        if candidate.is_file():
            return candidate
    return None


def _caller_free_path() -> str:
    """PATH with the CALLER's own virtualenv removed.

    Load-bearing, and learned by getting it wrong: this tool is normally invoked from the hub
    under `uv run`, so `sys.executable` and `PATH[0]` are the HUB's venv. Handing that to an
    unprovisioned satellite checkout produces a FAIL whose stated cause is
    `ModuleNotFoundError` — technically a failure, but not the one the row is about, and a
    reader would take it as "the package is missing" rather than "the package came from the
    wrong checkout". Stripping the caller's prefix makes the child resolve the interpreter a
    real seat in that repo would resolve: the system one, where the shared editable install
    actually lives. That is the interpreter whose silent wrong-tree import is the whole finding.
    """
    prefix = Path(sys.prefix).resolve()
    kept = []
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        try:
            resolved = Path(entry).resolve()
        except (OSError, ValueError):
            kept.append(entry)
            continue
        if resolved == prefix or prefix in resolved.parents:
            continue
        kept.append(entry)
    return os.pathsep.join(kept)


def resolve_interpreter(root: Path) -> tuple[list[str], bool]:
    """Return (argv prefix that runs python for this checkout, is-it-the-checkout's-own).

    A materialised `<root>/.venv` wins outright — it needs no tool on PATH and it is the exact
    thing leg (b) installs. Falling back is deliberate rather than a refusal: an unprovisioned
    checkout is precisely the state the proof should be able to examine and FAIL, and refusing
    to run there would make the failure unwitnessable. The fallback resolves against a
    caller-free PATH so the answer is about the target repo, not about this seat.
    """
    own = _venv_python(root)
    if own is not None:
        return [str(own)], True

    path = _caller_free_path()
    for candidate in _FALLBACK_INTERPRETERS:
        found = shutil.which(candidate, path=path)
        if found:
            return [found], False
    return [sys.executable], False


# --- the proof --------------------------------------------------------------------------

def _pytest_ini_arg(root: Path) -> list[str]:
    """Use the repo's OWN pytest configuration when it has one, so the proof runs under the
    same ini as the green it is vouching for (`testpaths`, `pythonpath`, plugins)."""
    data = _read_pyproject(root)
    if data.get("tool", {}).get("pytest", {}).get("ini_options") is not None:
        return ["-c", str(root / "pyproject.toml")]
    for name in ("pytest.ini", "tox.ini", "setup.cfg"):
        if (root / name).is_file():
            return ["-c", str(root / name)]
    return []


def _child_env(root: Path, packages: tuple[str, ...], out: Path) -> dict[str, str]:
    """The child's environment, with the inherited venv pointers REMOVED.

    `VIRTUAL_ENV` / `PYTHONHOME` / `PYTHONPATH` leak the parent seat's environment into the
    child and are exactly the leak under investigation — a proof that inherited them could
    report the parent's answer while appearing to ask the child. `PYTHONNOUSERSITE` blocks the
    per-user site-packages, another cross-checkout path the interpreter would otherwise honour.
    """
    env = dict(os.environ)
    for leaked in ("VIRTUAL_ENV", "PYTHONHOME", "PYTHONPATH", "PYTHONSTARTUP"):
        env.pop(leaked, None)
    env["PATH"] = _caller_free_path()
    env["PYTHONNOUSERSITE"] = "1"
    # THE FALSE-PASS THIS CLOSES (terra P1, 2026-08-07). `python -m pytest` prepends the CWD to
    # `sys.path`; the command a lane actually runs — `uv run --locked pytest`, i.e. the console
    # script — does not. Without this, a FLAT-LAYOUT package resolves out of the worktree purely
    # because the proof's own entry point put it there, and the proof reports PASS about a
    # package the real command would have taken from the shared install in the primary checkout.
    # It was not hypothetical: in the recorded ai-council FAIL, `config` (flat layout) reported
    # PASS in the very checkout whose `ai_council` (src layout) was demonstrably coming from the
    # primary. `PYTHONSAFEPATH` makes `-m` behave like the console script, so the proof and the
    # command it vouches for resolve imports the same way — which is the whole of its value.
    env["PYTHONSAFEPATH"] = "1"
    # Third-party pytest plugins installed in the TARGET's environment autoload by entry point,
    # and a repo may install one of its own. Those are the one route by which collecting a
    # temp-dir test file could still execute child-authored code, so the autoload is off: the
    # generated proof needs no plugin. What this does NOT claim to prevent is running the
    # target's interpreter and pytest at all — the row's done-when requires exactly that, and it
    # is disclosed in the module docstring rather than papered over.
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    # Importing the target's packages compiles them, and the bytecode lands in the TARGET tree
    # as `__pycache__/`. Every fleet repo gitignores it, so it would never have shown up as
    # dirt — which is exactly why it is worth suppressing rather than tolerating: a read-only
    # organ whose only writes are invisible ones is still an organ that writes.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["WT_PROOF_ROOT"] = str(root)
    env["WT_PROOF_PACKAGES"] = ",".join(packages)
    env["WT_PROOF_OUT"] = str(out)
    return env


def run_proof(root: Path, packages: tuple[str, ...]) -> Proof:
    """Spawn the checkout's pytest on a generated test and read back what it resolved."""
    interpreter, own_venv = resolve_interpreter(root)
    proof = Proof(root=root, packages=packages, interpreter=interpreter,
                  venv_inside_checkout=own_venv)

    with tempfile.TemporaryDirectory(prefix="wt-import-proof-") as tmp:
        tmpdir = Path(tmp)
        test_file = tmpdir / "test_wt_import_proof.py"
        test_file.write_text(_PROOF_TEST, encoding="utf-8", newline="\n")
        out_file = tmpdir / "result.json"

        argv = [
            *interpreter, "-m", "pytest",
            str(test_file),
            "-q",
            "-p", "no:cacheprovider",          # no .pytest_cache left in the target tree
            "-o", "addopts=",                  # drop the repo's own addopts (e.g. `-n auto`)
            "--rootdir", str(root),
            *_pytest_ini_arg(root),
        ]
        try:
            completed = subprocess.run(
                argv, cwd=str(root), capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=600,
                env=_child_env(root, packages, out_file),
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise ProofError(f"cannot run pytest for {root}: {exc}") from exc

        proof.pytest_returncode = completed.returncode
        proof.pytest_output = (completed.stdout + completed.stderr).strip()

        if out_file.is_file():
            try:
                payload = json.loads(out_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ProofError(f"unreadable proof result: {exc}") from exc
            proof.resolved = payload.get("packages", {})
            rootdir = payload.get("rootdir")
            proof.rootdir = Path(rootdir) if rootdir else None

    proof.outside = sorted(
        name for name, info in proof.resolved.items() if not _inside(root, info)
    )
    return proof


def _inside(root: Path, info: dict) -> bool:
    """True when everything this package resolved to lives under `root`. An import ERROR is
    NOT inside: a package that would not load cannot be evidence that the right one did."""
    if "error" in info:
        return False
    if "file" in info:
        return root in Path(info["file"]).parents
    paths = info.get("namespace_paths") or []
    return bool(paths) and all(root in Path(p).parents for p in paths)


# --- reporting --------------------------------------------------------------------------

def render(proof: Proof, applicable: bool) -> str:
    lines = [f"checkout   : {proof.root}"]
    lines.append(f"interpreter: {' '.join(proof.interpreter)}")
    lines.append(
        "venv       : "
        + ("inside the checkout (.venv)" if proof.venv_inside_checkout
           else "NOT inside the checkout - no <root>/.venv; the ambient interpreter was used")
    )
    if proof.rootdir is not None:
        agrees = "matches the checkout" if proof.rootdir == proof.root else "DIFFERS from the checkout"
        lines.append(f"pytest root: {proof.rootdir} ({agrees})")
    if not applicable:
        lines.append("")
        lines.append("NOT-APPLICABLE - this repo declares no importable package in pyproject.toml,")
        lines.append("so there is no import whose checkout could be wrong. Nothing was proved.")
        return "\n".join(lines)

    lines.append("")
    for name in proof.packages:
        info = proof.resolved.get(name)
        if info is None:
            lines.append(f"  ?    {name}: pytest reported nothing for this package")
        elif "error" in info:
            lines.append(f"  FAIL {name}: {info['error']}")
        elif "file" in info:
            mark = "PASS" if _inside(proof.root, info) else "FAIL"
            lines.append(f"  {mark} {name} -> {info['file']}")
        else:
            mark = "PASS" if _inside(proof.root, info) else "FAIL"
            lines.append(f"  {mark} {name} -> namespace {info.get('namespace_paths')}")

    lines.append("")
    if proof.passed:
        lines.append("PASS - this checkout's pytest imports this checkout's source.")
    else:
        lines.append("FAIL - this checkout's pytest does NOT import this checkout's source.")
        lines.append("")
        lines.append("Remedy - give the checkout its own environment, then re-run this proof:")
        lines.append(f"  python scripts/worktree_seed.py --plan {proof.root}")
        if proof.pytest_returncode not in (0, None):
            lines.append("")
            lines.append(f"pytest exited {proof.pytest_returncode}:")
            lines.append(proof.pytest_output[-2000:])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prove that a checkout's pytest imports THAT checkout's source ([#429]).",
    )
    parser.add_argument("--repo", default=".",
                        help="path inside the checkout to prove (default: cwd)")
    parser.add_argument("--packages", default="",
                        help="comma-separated import names, overriding pyproject discovery")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        root = resolve_root(Path(args.repo))
        if args.packages:
            packages = tuple(dict.fromkeys(
                top_level(n.strip()) for n in args.packages.split(",") if n.strip()
            ))
        else:
            packages = declared_packages(root)

        if not packages:
            proof = Proof(root=root, packages=(), interpreter=resolve_interpreter(root)[0],
                          venv_inside_checkout=resolve_interpreter(root)[1])
            report = render(proof, applicable=False)
            print(json.dumps({"verdict": "not-applicable", "root": str(root)}, indent=2)
                  if args.json else report)
            return EXIT_NOT_APPLICABLE

        proof = run_proof(root, packages)
    except ProofError as exc:
        print(f"worktree_import_proof: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if args.json:
        print(json.dumps({
            "verdict": "pass" if proof.passed else "fail",
            "root": str(proof.root),
            "rootdir": str(proof.rootdir) if proof.rootdir else None,
            "interpreter": proof.interpreter,
            "venv_inside_checkout": proof.venv_inside_checkout,
            "packages": proof.resolved,
            "outside": proof.outside,
            "pytest_returncode": proof.pytest_returncode,
        }, indent=2))
    else:
        print(render(proof, applicable=True))
    return EXIT_PASS if proof.passed else EXIT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
