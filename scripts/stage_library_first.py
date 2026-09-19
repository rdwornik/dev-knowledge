#!/usr/bin/env python
"""stage_library_first.py -- spine stage 6 (library-first): refuse a sentence, run deptry.

DECLARE-SPINE-AND-B3 §5 row 6: "library-first -- DOES NOT EXIST". §6 field rules: the
`library-first` field of a contract "accepts ONLY a SEARCH COMMAND AND ITS OUTPUT. A sentence is
an empty field." Prose failed on the architect three times in one session, so this stage is the
enforcement rather than another instruction. Two legs, one command (`run`):

  1. `check` -- the contract's `library-first` field must hold a fenced block whose `$ <command>`
     line is followed by output. A sentence, an empty field, a command with no output, and a
     `$ <sentence>` all raise `StageRefusal`.
  2. `deptry` -- the import graph is compared to the declared dependencies, so a library that
     was added without being declared (or declared and never used) is a finding. The library is
     deptry ([tool.deptry] in pyproject.toml holds the measured waivers); this module only runs
     it and turns a non-zero exit into a refusal.

LIBRARY-FIRST for this module, as a command and its output (2026-09-19):
  $ uv run --locked --with deptry deptry .      ->  "Found 336 dependency issues."
  (247 DEP001 first-party siblings + 88 DEP004 dev-group + 1 DEP003; waivers in pyproject.)
  REJECTED: a hand-written import scanner; ruff import rules (style, not declared-vs-imported);
  `seat_refusals.SeatRefusal` (its ids are the closed seat-rule enum, so a stage refusal would
  either widen it or lie about which rule fired).

ANTI-CLAIMS. The `check` leg proves the field HAS THE SHAPE of evidence, not that the output is
real: a fabricated `$ rg` block passes. Only a second pass re-running the command (a different
provider, per §6) can prove that. The deptry leg sees imports and declarations, not whether a
better library exists.

Layer-2 / read-only: reads the contract and the tree, writes nothing (deptry's JSON report goes
to a temp dir and is deleted).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import click

STAGE = 6

#: Head tokens accepted as "a command". Deliberately a closed list of search / inspection /
#: package tools: an open rule ("anything on PATH") would admit `$ find nothing`-shaped prose.
COMMAND_HEADS = frozenset({
    "rg", "grep", "egrep", "git", "gh", "uv", "uvx", "py", "python", "python3", "pip", "deptry",
    "ruff", "pytest", "pre-commit", "npm", "npx", "ls", "dir", "find", "cat", "head", "tail",
    "wc", "where", "which", "curl", "get-childitem", "select-string", "get-content",
})

_FIELD_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?library-first:?(?:\*\*)?:?(?P<rest>.*)$",
                       re.IGNORECASE)
_NEXT_FIELD_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*[\w-]+:?\*\*|^#{1,6}\s")
_FENCE_RE = re.compile(r"^\s*```")
_PROMPT_RE = re.compile(r"^\s*(?:\$|PS>)\s+(?P<cmd>\S.*)$")
_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=\S*$")
_PRUNE = frozenset({".git", ".venv", "venv", "node_modules", "__pycache__", ".claude", ".pytest_cache",
                    ".ruff_cache"})


class StageRefusal(RuntimeError):
    """Stage 6 refused. Raised, never logged; `remedy` names the way forward."""

    def __init__(self, detail: str, *, remedy: str) -> None:
        self.detail = detail
        self.remedy = remedy
        super().__init__(f"REFUSED [stage {STAGE}]: {detail} -- {remedy}")


_REMEDY = ("paste the search you ran as a fenced block: a `$ <command>` line, then its output "
           "(a search with no hits: write `exit=1, no matches`)")


def _field_body(text: str) -> "str | None":
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = _FIELD_RE.match(line)
        if not m:
            continue
        body = [m.group("rest")]
        for nxt in lines[i + 1:]:
            if _NEXT_FIELD_RE.match(nxt):
                break
            body.append(nxt)
        return "\n".join(body)
    return None


def _head(cmd: str) -> str:
    for tok in cmd.split():
        if _ASSIGN_RE.match(tok):
            continue
        return Path(tok.replace("\\", "/")).name.lower().removesuffix(".exe")
    return ""


def _blocks(body: str) -> "list[list[str]]":
    blocks: "list[list[str]]" = []
    cur: "list[str] | None" = None
    for line in body.splitlines():
        if _FENCE_RE.match(line):
            if cur is None:
                cur = []
            else:
                blocks.append(cur)
                cur = None
        elif cur is not None:
            cur.append(line)
    return blocks


def check_contract(text: str, *, site: str) -> int:
    """Return the number of validated command-and-output groups; raise `StageRefusal` if none
    or if any group is malformed."""
    body = _field_body(text)
    if body is None:
        raise StageRefusal(f"{site}: no `library-first` field", remedy=_REMEDY)
    if not body.strip():
        raise StageRefusal(f"{site}: `library-first` field is empty", remedy=_REMEDY)
    groups: "list[tuple[str, list[str]]]" = []
    for block in _blocks(body):
        for line in block:
            m = _PROMPT_RE.match(line)
            if m:
                groups.append((m.group("cmd"), []))
            elif groups and line.strip():
                groups[-1][1].append(line)
    if not groups:
        raise StageRefusal(f"{site}: `library-first` holds a sentence, not a fenced command", remedy=_REMEDY)
    for cmd, output in groups:
        if _head(cmd) not in COMMAND_HEADS:
            raise StageRefusal(f"{site}: `$ {cmd}` -- its head `{_head(cmd)}` is not a command", remedy=_REMEDY)
        if not output:
            raise StageRefusal(f"{site}: `$ {cmd}` has no output", remedy=_REMEDY)
    return len(groups)


def first_party_modules(root: Path) -> "list[str]":
    """Module names that resolve through a sys.path root inside the tree (a `.py` stem or a
    directory on the way to a `.py`), derived from disk so the list cannot drift."""
    names: "set[str]" = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _PRUNE]
        py = [f for f in filenames if f.endswith(".py")]
        if py:
            names.update(Path(dirpath).relative_to(root).parts)  # every ancestor is importable
            names.update(Path(f).stem for f in py)
    return sorted(names)


def run_deptry(root: Path) -> int:
    """Run deptry over `root`; return 0, or raise `StageRefusal` naming the rule codes."""
    root = Path(root)
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "deptry.json"
        root = root.resolve()
        cmd = [sys.executable, "-m", "deptry", ".", "--json-output", str(report)]
        for name in first_party_modules(root):
            cmd += ["--known-first-party", name]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                              cwd=root)  # deptry reads config from cwd, not from its path argument
        if proc.returncode == 0:
            return 0
        if not report.exists():
            raise StageRefusal(f"deptry failed to run (exit {proc.returncode}): {proc.stderr.strip()[:300]}",
                               remedy="fix the deptry invocation; `uv sync --locked` installs it")
        issues = json.loads(report.read_text(encoding="utf-8"))
    codes = Counter(i["error"]["code"] for i in issues)
    first = "; ".join(f"{i['error']['code']} {i['location']['file']}:{i['location']['line']} {i['module']}"
                      for i in issues[:5])
    raise StageRefusal(
        f"deptry found {len(issues)} issue(s) {dict(sorted(codes.items()))}: {first}",
        remedy="declare the dependency in pyproject.toml (with its WHY) or remove the import; a "
               "measured false positive is waived in [tool.deptry] with its reason")


@click.group(help="Spine stage 6 (library-first). Exit 1 = REFUSED.")
def cli() -> None:
    pass


def _refuse(exc: StageRefusal) -> None:
    click.echo(str(exc), err=True)
    sys.exit(1)


@cli.command("check")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True, dir_okay=False))
def cmd_check(files: "tuple[str, ...]") -> None:
    """Refuse a contract whose `library-first` field is not a command and its output."""
    try:
        for f in files:
            n = check_contract(Path(f).read_text(encoding="utf-8"), site=Path(f).name)
            click.echo(f"OK [stage {STAGE}] {Path(f).name}: {n} command(s) with output")
    except StageRefusal as exc:
        _refuse(exc)


@cli.command("deptry")
@click.option("--root", default=".", type=click.Path(file_okay=False))
def cmd_deptry(root: str) -> None:
    """Refuse when the import graph disagrees with the declared dependencies."""
    try:
        run_deptry(Path(root))
        click.echo(f"OK [stage {STAGE}] deptry clean over {Path(root).resolve()}")
    except StageRefusal as exc:
        _refuse(exc)


@cli.command("run")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--root", default=".", type=click.Path(file_okay=False))
@click.pass_context
def cmd_run(ctx: click.Context, files: "tuple[str, ...]", root: str) -> None:
    """The stage-6 command: `check` every contract, then `deptry`."""
    ctx.invoke(cmd_check, files=files)
    ctx.invoke(cmd_deptry, root=root)


if __name__ == "__main__":  # pragma: no cover -- CLI entry
    cli()
