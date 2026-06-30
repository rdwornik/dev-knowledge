"""deploy/tool.py — the deploy orchestrator's ASSESS half (ADR-92, C2a).

**Strictly read-only.** This is the first half of the deploy orchestrator (the
ADR-92 "assess" step): a ``deploy`` CLI that runs **preflight**, then **detects**
every carrier's state against the target manifest and prints a **structured
deployment-plan** of what each carrier *would* do — **without applying anything,
writing the version record, or staging/committing.**

The apply + record half is **C2b**. Keeping the assess engine read-only makes it
safe to run against the real (possibly drifted) fleet to surface drift: the only
carrier side effect reachable here is ``detect()``, which for the plugin carrier
runs ``claude plugin list --json`` (a read) — never ``install``.

CLI::

    deploy <repo> --target <version>        # assess: preflight + detect + print plan

``<repo>`` is the consumer's directory name (the ``ecosystem/deployed-versions.yaml``
registry key, e.g. ``ai-council``); ``<version>`` is the methodology release (e.g.
``v1.0.0`` / ``1.0.0``), which selects ``deploy/manifest-v<version>.yaml``.

Preflight (each a hard abort with a clear message):

1. the target ``<version>`` manifest + its ``source_tag`` git tag resolve;
2. ``<repo>`` is a registered consumer in ``ecosystem/deployed-versions.yaml``;
3. the consumer ``<repo>`` working tree is clean.

The ``--execute`` path (apply + record write + consumer staging) is **C2b** — it
is scaffolded as an explicit guard here, never implemented.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click
import yaml

# This module lives in deploy/ beside the carriers + contract, which import each
# other flatly (``from contract import ...``). Guarantee deploy/ is importable
# whether tool.py is run as a script (sys.path[0] already covers it) or imported
# as a module by the test suite.
_DEPLOY_DIR = Path(__file__).resolve().parent
if str(_DEPLOY_DIR) not in sys.path:
    sys.path.insert(0, str(_DEPLOY_DIR))

_HUB_ROOT = _DEPLOY_DIR.parent
HUB_DIR_NAME = _HUB_ROOT.name  # ".dev-knowledge" — the hub is its own registry key

DEFAULT_REGISTRY = _HUB_ROOT / "ecosystem" / "deployed-versions.yaml"

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Git transport — pure I/O, injectable so the test suite never shells to git.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GitResult:
    """The outcome of one git invocation (what an injected git-runner returns)."""

    returncode: int
    stdout: str = ""
    stderr: str = ""


GitRunner = Callable[[Sequence[str], Path], GitResult]


def _default_git(args: Sequence[str], cwd: Path) -> GitResult:
    """Real git invoker — fixed argv, no shell, read-only commands only here."""
    proc = subprocess.run(  # noqa: S603,S607 — fixed argv, no shell, read-only
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    return GitResult(proc.returncode, proc.stdout or "", proc.stderr or "")


# ---------------------------------------------------------------------------
# Preflight — abort on any failure, before a single carrier is detected.
# ---------------------------------------------------------------------------


class PreflightError(Exception):
    """A preflight check failed — the deploy must abort before assessing."""


@dataclass(frozen=True)
class PreflightContext:
    """The resolved, preflight-passed inputs the assess loop consumes."""

    repo: str
    version: str          # as supplied (display)
    bare_version: str     # leading-'v' stripped (manifest filename component)
    repo_root: Path       # the consumer tree the carriers bind to
    source_tag: str       # the git tag the manifest declares for this release
    manifest: dict[str, Any]
    manifest_path: Path


def normalize_version(version: str) -> str:
    """Strip a single leading ``v`` so ``v1.0.0`` and ``1.0.0`` both map to ``1.0.0``."""
    return version[1:] if version.startswith("v") else version


def manifest_path_for(bare_version: str, deploy_dir: Path = _DEPLOY_DIR) -> Path:
    """The manifest file for a release: ``deploy/manifest-v<bare_version>.yaml``."""
    return deploy_dir / f"manifest-v{bare_version}.yaml"


def load_manifest(path: Path) -> dict[str, Any]:
    """Read + parse a carrier manifest (raises PreflightError if absent/malformed)."""
    if not path.exists():
        raise PreflightError(f"no manifest for that version (expected {path})")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PreflightError(f"manifest did not parse ({path}): {exc}") from exc
    if not isinstance(data, dict) or not data.get("carriers"):
        raise PreflightError(f"manifest missing a 'carriers:' list ({path})")
    return data


def load_registry(registry_path: Path) -> dict[str, Any]:
    """Read the deployed-versions registry's ``repos:`` map (raises on absent/malformed)."""
    if not registry_path.exists():
        raise PreflightError(f"registry absent: {registry_path}")
    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PreflightError(f"registry did not parse ({registry_path}): {exc}") from exc
    repos = data.get("repos") if isinstance(data, dict) else None
    if not isinstance(repos, dict):
        raise PreflightError(f"registry missing a 'repos:' map ({registry_path})")
    return repos


def resolve_repo_root(repo: str, hub_root: Path = _HUB_ROOT) -> Path:
    """Resolve a registry repo-name to its working-tree path (a sibling under Dev/).

    The hub's own dir name resolves to the hub itself; every other consumer is a
    sibling next to the hub (``<dev>/<repo>``). Keyed identically to the registry
    (by directory name), so the path and the registry key never diverge.
    """
    return (hub_root.parent / repo).resolve()


def git_tag_exists(tag: str, hub_root: Path, git: GitRunner) -> bool:
    """True iff ``tag`` resolves in the hub repo (lightweight or annotated)."""
    res = git(["rev-parse", "-q", "--verify", f"refs/tags/{tag}"], hub_root)
    return res.returncode == 0


def git_tree_clean(repo_root: Path, git: GitRunner) -> bool:
    """True iff the consumer working tree has no staged/unstaged/untracked changes."""
    res = git(["status", "--porcelain"], repo_root)
    if res.returncode != 0:
        raise PreflightError(
            f"could not read git status for {repo_root}: {res.stderr.strip()}"
        )
    return res.stdout.strip() == ""


def preflight(
    repo: str,
    version: str,
    *,
    hub_root: Path = _HUB_ROOT,
    deploy_dir: Path = _DEPLOY_DIR,
    registry_path: Path = DEFAULT_REGISTRY,
    git: GitRunner = _default_git,
) -> PreflightContext:
    """Run every preflight gate; return the resolved context or raise PreflightError.

    Order: resolve the manifest, confirm the repo is a registered consumer, confirm
    its tree exists + is clean, confirm the release tag resolves. The first failure
    aborts with a specific, actionable message.
    """
    bare = normalize_version(version)
    mpath = manifest_path_for(bare, deploy_dir)
    manifest = load_manifest(mpath)

    repos = load_registry(registry_path)
    if repo not in repos:
        raise PreflightError(
            f"{repo!r} is not a registered consumer in {registry_path.name} "
            f"(known: {', '.join(sorted(repos)) or 'none'})"
        )

    repo_root = resolve_repo_root(repo, hub_root)
    if not repo_root.is_dir():
        raise PreflightError(f"consumer working tree not found: {repo_root}")

    source_tag = str(manifest.get("source_tag") or "").strip()
    if not source_tag:
        raise PreflightError(f"manifest declares no 'source_tag' ({mpath})")
    if not git_tag_exists(source_tag, hub_root, git):
        raise PreflightError(
            f"target tag {source_tag!r} does not resolve in the hub -- "
            f"the release is not tagged yet"
        )

    if not git_tree_clean(repo_root, git):
        raise PreflightError(
            f"{repo} working tree is not clean -- commit or stash changes first"
        )

    return PreflightContext(
        repo=repo,
        version=version,
        bare_version=bare,
        repo_root=repo_root,
        source_tag=source_tag,
        manifest=manifest,
        manifest_path=mpath,
    )


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


_EXECUTE_GUARD = (
    "execute (apply + version-record write + consumer staging) is implemented in "
    "C2b -- this build is the read-only ASSESS half only. Omit --execute to print "
    "the deployment plan."
)


@click.command()
@click.argument("repo")
@click.option(
    "--target",
    "version",
    required=True,
    help="Methodology release to assess against (e.g. v1.0.0); selects the manifest.",
)
@click.option(
    "--execute",
    is_flag=True,
    help="[C2b — not implemented] apply + write the version record. Guarded here.",
)
def deploy(repo: str, version: str, execute: bool) -> None:
    """Assess <REPO> against --target: preflight, detect every carrier, print the plan.

    Strictly read-only — never applies, never writes the version record, never
    stages or commits. Run the execute half (C2b) to actually deploy.
    """
    if execute:
        # Scaffolded entry point for C2b — explicitly guarded, never implemented here.
        raise click.ClickException(_EXECUTE_GUARD)

    try:
        ctx = preflight(repo, version)
    except PreflightError as exc:
        raise click.ClickException(f"preflight failed -- {exc}") from exc

    # The assess loop + structured deployment-plan output land in step 4.
    click.echo(
        f"preflight OK: {ctx.repo} @ {ctx.version} "
        f"(manifest {ctx.manifest_path.name}, tag {ctx.source_tag})"
    )


def main() -> None:
    deploy()


if __name__ == "__main__":
    main()
