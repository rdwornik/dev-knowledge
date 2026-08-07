#!/usr/bin/env python
"""worktree_seed.py — the fleet worktree seed manifest, stated ONCE in the hub ([#429] leg (a)).

WHAT THIS IS
------------
[#429] leg (a): *"a portable seed-manifest stated ONCE in the hub, not hand-copied per
satellite — a satellite without today's `.worktreeinclude` (ai-council, verified) must be able
to provision"*. This module is that manifest, plus the renderer that answers the question for
any repo in the fleet, including one carrying no `.worktreeinclude` of its own.

THE RESHAPE THIS ENCODES, because it is the finding and not just the fix. `.worktreeinclude` is
a list of UNTRACKED FILES to copy into a new worktree, and the row's framing assumes that is
what portability means. Measured against the row's own named satellite it is not: `ai-council`
gitignores `.env` and `.claude/settings.local.json` and has NEITHER on disk, so its correct
`.worktreeinclude` is EMPTY — and an empty manifest would still leave every ai-council worktree
broken, because its provisioning need was never an untracked file. It is an ENVIRONMENT: a
per-checkout venv, leg (b). A seed mechanism that models only the copy half cannot make a
satellite provisionable, so this manifest models both, and `--plan` emits both.

WHAT IS DECLARED, AND WHAT IS DERIVED — the split is the portability property.
  * DECLARED (`_COPY_MANIFEST`, below): which untracked paths a worktree needs. Small, closed,
    hub-owned, and the only part a satellite could not compute for itself.
  * DERIVED (`env_bootstrap`): how that repo builds a per-checkout environment, read from the
    repo's own packaging files at call time. A satellite that adopts uv later needs no edit
    here — the derivation sees `uv.lock` appear and changes its answer. Declaring it per repo
    instead would have recreated the hand-copied-per-satellite problem one layer up.

WHY THE MANIFEST LIVES IN CODE. It follows `scripts/validate_branch_naming.py`, which holds the
branch-prefix enum as a module constant for the same reason: a small closed declaration whose
members are ruled elsewhere, wanting tests more than it wants a parse step. An
`ecosystem/*.yaml` surface is the better long-run home and is recorded as deferred, not
rejected — it acquires registry/parity obligations this arc is not scoped to take.

POSTURE — READ-ONLY OUTSIDE THE HUB, AND WIRED INTO NO GATE. Layer 2 (ADR-28/36) forbids driving
state in a child repo, so `--write` refuses any target but the hub's own `.worktreeinclude`, and
`--plan` PRINTS the provisioning commands rather than running them. The lane (or `/lane-boot`)
executes them locally, which keeps the act where the authority is. Adoption-first, per
`/preflight`: nothing consumes the exit code yet.

HONEST LIMITS
  * `--plan` is checked against what the target repo declares, not against what a session
    actually did. It cannot tell a seeded worktree from an unseeded one — `worktree_import_proof`
    is the organ that measures the outcome, and the plan deliberately ends by naming it.
  * The copy manifest is a list of paths, not a policy. A gitignored file nobody thought of is
    absent from it, and its absence is silent by construction.
  * The universal entries are copied ONLY when they exist in the primary. A repo that has
    neither gets an empty copy list, which is a correct answer and not a broken one.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_DRIFT = 1
EXIT_ERROR = 2

HUB_REPO_NAME = ".dev-knowledge"

#: Untracked paths EVERY fleet repo's worktree wants, gitignored in each by fleet convention.
#: `.env` carries provider keys; `.claude/settings.local.json` carries the seat's local
#: permission grants. Both are per-machine and therefore absent from git by design, which is
#: exactly why a worktree silently loses them.
UNIVERSAL_COPY = (
    ".env",
    ".claude/settings.local.json",
)

#: Per-repo additions, keyed by checkout directory name. The hub's entry is the live content of
#: its own `.worktreeinclude` (ADR-61/#107): gitignored ecosystem state a lane's `audit-health`
#: gate reads, whose absence reports `repos registered (none)` and blocks every commit.
_COPY_MANIFEST: dict[str, tuple[str, ...]] = {
    HUB_REPO_NAME: ("ecosystem/*/state.yaml",),
}

#: How a checkout gets an environment of its own. Values are DERIVED per repo (`env_bootstrap`),
#: never declared per repo.
ENV_UV = "uv"
ENV_VENV_EDITABLE = "venv-editable"
ENV_NONE = "none"


class SeedError(Exception):
    """Raised when the tool cannot look — distinct from looking and finding drift."""


@dataclass(frozen=True)
class Plan:
    """One checkout's provisioning answer."""

    root: Path
    primary: Path
    repo_name: str
    copy: tuple[str, ...]
    present: tuple[str, ...]
    env_kind: str
    env_commands: tuple[str, ...]

    @property
    def is_worktree(self) -> bool:
        return self.root != self.primary


# --- the manifest, resolved -------------------------------------------------------------

def copy_patterns(repo_name: str) -> tuple[str, ...]:
    """Every untracked pattern a worktree of `repo_name` seeds. Universal first, then that
    repo's additions — the order the rendered `.worktreeinclude` keeps, so a satellite's file
    and the hub's read as the same document with a different tail."""
    return UNIVERSAL_COPY + _COPY_MANIFEST.get(repo_name, ())


def env_bootstrap(root: Path) -> tuple[str, tuple[str, ...]]:
    """(kind, commands) that give `root` an environment of its own — read from `root` itself.

    Three cases, in order. `uv.lock` means the repo pins its toolchain (ADR-106), and `uv run`
    materialises `<root>/.venv` on first invocation, so nothing needs installing by hand. A
    build-system without a lock means the repo installs itself editable, and the editable
    install is the thing that must be per-checkout rather than shared. No package at all means
    no environment is needed to make imports follow the checkout, and saying so is a real
    answer rather than a gap.
    """
    if (root / "uv.lock").is_file():
        return ENV_UV, (
            "uv sync --locked",
            "# every later test invocation: uv run --locked pytest ...",
        )

    data = _read_pyproject(root)
    if data.get("build-system") and _has_importable_package(root, data):
        extra = ".[dev]" if _declares_dev_extra(data) else "."
        return ENV_VENV_EDITABLE, (
            "py -m venv .venv",
            f'.venv\\Scripts\\python.exe -m pip install -e "{extra}"',
            "# every later test invocation: .venv\\Scripts\\python.exe -m pytest ...",
        )

    return ENV_NONE, ()


def _read_pyproject(root: Path) -> dict:
    path = root / "pyproject.toml"
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SeedError(f"cannot read {path}: {exc}") from exc


def _has_importable_package(root: Path, data: dict) -> bool:
    """True when this repo actually ships a package on disk, so `pip install -e .` has a
    subject. A `[build-system]` alone does not prove one — the hub declares one and ships no
    importable package, and telling it to install itself editable would be noise."""
    names: list[str] = []
    includes = (
        data.get("tool", {}).get("setuptools", {})
        .get("packages", {}).get("find", {}).get("include", [])
    )
    names += [p.rstrip("*").rstrip(".") for p in includes if isinstance(p, str)]
    dist = data.get("project", {}).get("name")
    if isinstance(dist, str):
        names.append(dist.replace("-", "_"))
    for name in names:
        top = name.split(".")[0]
        if not top:
            continue
        for base in (root, root / "src"):
            if (base / top / "__init__.py").is_file() or (base / f"{top}.py").is_file():
                return True
    return False


def _declares_dev_extra(data: dict) -> bool:
    return "dev" in (data.get("project", {}).get("optional-dependencies", {}) or {})


# --- git plumbing -----------------------------------------------------------------------

def _git(args: list[str], cwd: Path) -> str:
    try:
        proc = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SeedError(f"cannot run git in {cwd}: {exc}") from exc
    if proc.returncode != 0:
        raise SeedError(f"git {' '.join(args)} failed in {cwd}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def resolve_checkout(repo: Path) -> tuple[Path, Path]:
    """(this checkout's root, the PRIMARY checkout's root).

    In a linked worktree these differ, and the second is where the untracked files to copy
    actually live: `--git-common-dir` points at the primary's `.git`, whose parent is the
    primary tree. Deriving it rather than asking for it is what lets `--plan` be given nothing
    but the worktree path.
    """
    root = Path(_git(["rev-parse", "--show-toplevel"], repo)).resolve()
    common = Path(_git(["rev-parse", "--path-format=absolute", "--git-common-dir"], repo)).resolve()
    return root, common.parent.resolve()


# --- rendering --------------------------------------------------------------------------

def render_worktreeinclude(repo_name: str) -> str:
    """The `.worktreeinclude` content for `repo_name`, from the manifest above."""
    lines = [
        "# Generated from scripts/worktree_seed.py in the .dev-knowledge hub ([#429] leg (a)).",
        "# Edit the manifest there, not this file. Regenerate: python scripts/worktree_seed.py --write",
        "#",
        "# Untracked paths a native `claude --worktree` lane copies from the primary checkout.",
        "# A per-checkout ENVIRONMENT is the other half of provisioning and is NOT expressible",
        "# here -- see `--plan`, and verify the outcome with scripts/worktree_import_proof.py.",
    ]
    lines += list(copy_patterns(repo_name))
    return "\n".join(lines) + "\n"


def build_plan(repo: Path) -> Plan:
    root, primary = resolve_checkout(repo)
    repo_name = primary.name
    patterns = copy_patterns(repo_name)
    present = tuple(p for p in patterns if _matches_in(primary, p))
    kind, commands = env_bootstrap(root)
    return Plan(root=root, primary=primary, repo_name=repo_name, copy=patterns,
                present=present, env_kind=kind, env_commands=commands)


def _matches_in(base: Path, pattern: str) -> bool:
    """Does `pattern` match anything in the primary? A pattern that matches nothing is reported
    as declared-but-absent rather than dropped, so a reader can tell "this repo does not use
    it" from "this repo lost it"."""
    try:
        return any(base.glob(pattern))
    except (OSError, ValueError):
        return False


def _copy_block(plan: Plan) -> list[str]:
    """The PowerShell that seeds `plan.root` from `plan.primary`.

    The patterns are expanded by `Get-ChildItem -Path`, NOT by `-Recurse -Filter`. That is a
    correctness requirement rather than a style preference: the hub's own worktrees live at
    `.claude/worktrees/` INSIDE the primary tree, so a recursive basename search run during a
    parallel batch would walk into every other lane's checkout and copy whichever
    `settings.local.json` it happened to find first. A path glob matches the declared location
    and nothing else.
    """
    patterns = ", ".join(f"'{p.replace('/', chr(92))}'" for p in plan.present)
    return [
        f"$primary = '{plan.primary}'",
        f"$lane    = '{plan.root}'",
        f"foreach ($p in @({patterns})) {{",
        "    Get-ChildItem -Path (Join-Path $primary $p) -File -Force | ForEach-Object {",
        "        $t = Join-Path $lane $_.FullName.Substring($primary.Length + 1)",
        "        New-Item -ItemType Directory -Force -Path (Split-Path $t) | Out-Null",
        "        Copy-Item $_.FullName $t -Force",
        "    }",
        "}",
    ]


def render_plan(plan: Plan) -> str:
    lines = [
        f"repo       : {plan.repo_name}",
        f"checkout   : {plan.root}",
        f"primary    : {plan.primary}",
        f"kind       : {'linked worktree' if plan.is_worktree else 'PRIMARY checkout'}",
        "",
        "1. Untracked files to seed from the primary",
    ]
    if not plan.copy:
        lines.append("   (none declared for this repo)")
    for pattern in plan.copy:
        state = "present in the primary" if pattern in plan.present else "not present - skip"
        lines.append(f"   {pattern}  [{state}]")
    if plan.is_worktree and plan.present:
        lines.append("")
        lines.append("   PowerShell:")
        lines.extend("     " + line for line in _copy_block(plan))
    elif plan.is_worktree:
        lines.append("")
        lines.append("   Nothing to copy - this repo's worktree needs no untracked seed.")

    lines.append("")
    lines.append(f"2. Per-checkout environment  [{plan.env_kind}]")
    if plan.env_kind == ENV_NONE:
        lines.append("   This repo ships no importable package, so no per-checkout install is")
        lines.append("   needed for imports to follow the checkout.")
    else:
        lines.append("   PowerShell, run from the worktree root:")
        for command in plan.env_commands:
            lines.append(f"     {command}")

    lines.append("")
    lines.append("3. Verify the outcome - the step that makes 1 and 2 checkable")
    lines.append(f"     python <hub>/scripts/worktree_import_proof.py --repo {plan.root}")
    lines.append("   PASS means this checkout's pytest imports this checkout's source.")
    return "\n".join(lines)


# --- CLI --------------------------------------------------------------------------------

def _own_checkout() -> Path:
    """The checkout THIS script is part of — `scripts/worktree_seed.py` -> its repo root."""
    return Path(__file__).resolve().parent.parent


def _hub_root(repo: Path) -> Path:
    """The checkout `--write` is allowed to modify, or a refusal.

    IDENTITY, NOT NAME (terra P1, third pass). The first version compared
    `primary.name != HUB_REPO_NAME`, which authorises any checkout that merely happens to sit in
    a directory called `.dev-knowledge` — a clone at another path, a restored backup, a
    same-named repo belonging to something else entirely. A refusal keyed to a string a stranger
    can satisfy by renaming a folder is not a refusal. The binding question is narrower and has
    an exact answer: `--write` may only rewrite the `.worktreeinclude` of the checkout **this
    file is running out of**. The name check is kept behind it as a second, independent
    condition rather than replaced by it.
    """
    root, primary = resolve_checkout(repo)
    own = _own_checkout()
    if root != own:
        raise SeedError(
            f"refusing to write outside this checkout: {root} is not {own}. "
            "--write only ever rewrites the .worktreeinclude of the checkout this script runs "
            "from; Layer 2 drives no state in a child repo -- use --render or --plan there."
        )
    if primary.name != HUB_REPO_NAME:
        raise SeedError(
            f"refusing to write outside the hub: {primary} is not {HUB_REPO_NAME}. "
            "Layer 2 drives no state in a child repo -- use --render or --plan there."
        )
    return root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The fleet worktree seed manifest, stated once in the hub ([#429]).",
    )
    parser.add_argument("--repo", default=".", help="path inside the checkout (default: cwd)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plan", metavar="PATH", nargs="?", const=".",
                       help="print how to provision this checkout (copies + environment)")
    group.add_argument("--render", metavar="REPO_NAME",
                       help="print the .worktreeinclude a named repo should carry")
    group.add_argument("--check", action="store_true",
                       help="regen-and-diff the hub's own .worktreeinclude")
    group.add_argument("--write", action="store_true",
                       help="write the hub's own .worktreeinclude (hub only)")
    args = parser.parse_args(argv)

    try:
        if args.render:
            sys.stdout.write(render_worktreeinclude(args.render))
            return EXIT_OK

        if args.plan is not None:
            print(render_plan(build_plan(Path(args.plan))))
            return EXIT_OK

        root = _hub_root(Path(args.repo))
        target = root / ".worktreeinclude"
        expected = render_worktreeinclude(HUB_REPO_NAME)
        actual = target.read_text(encoding="utf-8") if target.is_file() else ""

        if args.check:
            if actual == expected:
                print(f"OK  {target} matches the manifest")
                return EXIT_OK
            print(f"DRIFT  {target} does not match the manifest in scripts/worktree_seed.py")
            print("       regenerate: python scripts/worktree_seed.py --write")
            return EXIT_DRIFT

        target.write_text(expected, encoding="utf-8", newline="\n")
        print(f"wrote {target}")
        return EXIT_OK

    except SeedError as exc:
        print(f"worktree_seed: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
