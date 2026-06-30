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
from rich.console import Console
from rich.table import Table

# This module lives in deploy/ beside the carriers + contract, which import each
# other flatly (``from contract import ...``). Guarantee deploy/ is importable
# whether tool.py is run as a script (sys.path[0] already covers it) or imported
# as a module by the test suite.
_DEPLOY_DIR = Path(__file__).resolve().parent
if str(_DEPLOY_DIR) not in sys.path:
    sys.path.insert(0, str(_DEPLOY_DIR))

from carrier_floor import FloorCarrier  # noqa: E402
from carrier_globalconfig import GlobalConfigCarrier  # noqa: E402
from carrier_plugin import PluginCarrier  # noqa: E402
from carrier_precommit import PrecommitCarrier  # noqa: E402
from contract import Carrier, CarrierState  # noqa: E402

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
# Carrier factory — id -> a carrier instance bound to the consumer tree. Injectable
# so the test suite can supply carriers against a crafted fixture tree (and a mock
# plugin runner) instead of touching the real fleet / the real ``claude`` binary.
# ---------------------------------------------------------------------------


CarrierFactory = Callable[[Path], "dict[str, Carrier]"]


def make_carriers(
    repo_root: Path,
    *,
    plugin_runner: Any | None = None,
    user_config_base: Path | str | None = None,
) -> dict[str, Carrier]:
    """Build every carrier bound to ``repo_root``, keyed by its ``carrier_id``.

    ``plugin_runner`` / ``user_config_base`` are the live carriers' injection
    points (default ``None`` -> the real ``claude`` CLI / the real ``~/.codex``);
    the live tool passes neither, so assess reads real state.
    """
    return {
        GlobalConfigCarrier.carrier_id: GlobalConfigCarrier(
            repo_root, user_config_base=user_config_base
        ),
        PluginCarrier.carrier_id: PluginCarrier(repo_root, runner=plugin_runner),
        PrecommitCarrier.carrier_id: PrecommitCarrier(repo_root),
        FloorCarrier.carrier_id: FloorCarrier(repo_root),
    }


def default_carrier_factory(repo_root: Path) -> dict[str, Carrier]:
    """The live factory — carriers reading real consumer/user/CLI state (read-only)."""
    return make_carriers(repo_root)


# ---------------------------------------------------------------------------
# Planned-action narration — what ``apply`` WOULD do for a detected state. Pure
# string mapping; assess never calls ``apply``.
# ---------------------------------------------------------------------------


_APPLY_HINT = {
    "global-config": "copy hub codex/AGENTS.md -> ~/.codex/AGENTS.md",
    "tier1-plugin": "claude plugin install/update --scope project",
    "precommit": "merge required pins into .pre-commit-config.yaml",
    "floor": "generate .claude/CLAUDE-FLOOR.md + .sha256 sidecar",
}

_STATE_VERB = {
    CarrierState.ABSENT: "would apply from scratch",
    CarrierState.PRESENT_DRIFTED: "would reconcile drift",
    CarrierState.PRESENT_WRONG_VERSION: "would update to target version",
}


def planned_action(carrier_id: str, state: CarrierState) -> str:
    """What ``apply`` would do, in one line (assess never mutates — narration only)."""
    if state is CarrierState.PRESENT_CORRECT:
        return "already correct -- skip"
    verb = _STATE_VERB.get(state, "would apply")
    hint = _APPLY_HINT.get(carrier_id)
    return f"{verb} ({hint})" if hint else verb


# ---------------------------------------------------------------------------
# The deployment plan — structured, read-only output of the assess step.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CarrierPlanItem:
    """One carrier's row in the plan: detected state + what apply would do."""

    carrier_id: str
    order: int
    implemented: bool
    state: CarrierState | None  # None when not implemented or detect errored
    action: str
    error: str | None = None


@dataclass(frozen=True)
class OutOfScopeItem:
    """An ADR-92 ``l0_scope`` payload this tool does NOT deploy (not a failure)."""

    payload: str
    target: str
    reason: str   # "deferred deployable" | "enforced elsewhere"
    detail: str


@dataclass(frozen=True)
class DeploymentPlan:
    """The full assess result for one consumer @ one release. Read-only."""

    repo: str
    repo_root: Path
    version: str
    source_tag: str
    items: tuple[CarrierPlanItem, ...]
    out_of_scope: tuple[OutOfScopeItem, ...]

    @property
    def needs_apply(self) -> tuple[CarrierPlanItem, ...]:
        return tuple(i for i in self.items if i.state is not None and i.state.needs_apply)

    @property
    def correct(self) -> tuple[CarrierPlanItem, ...]:
        return tuple(i for i in self.items if i.state is CarrierState.PRESENT_CORRECT)

    @property
    def errored(self) -> tuple[CarrierPlanItem, ...]:
        return tuple(i for i in self.items if i.implemented and i.state is None and i.error)

    @property
    def skipped(self) -> tuple[CarrierPlanItem, ...]:
        return tuple(i for i in self.items if not i.implemented)


def extract_out_of_scope(entries: list[dict[str, Any]]) -> list[OutOfScopeItem]:
    """Pull the manifest's ``l0_scope`` deferred / enforced-elsewhere payloads.

    These are declared-but-not-deployed edges (ADR-88 do-not-build-is-doctrine /
    ADR-92 l0_scope honesty) — surfaced as out-of-scope context, never as carriers
    that fail.
    """
    out: list[OutOfScopeItem] = []
    for entry in entries:
        l0 = entry.get("l0_scope")
        if not isinstance(l0, dict):
            continue
        for d in l0.get("deferred_deployables", []) or []:
            out.append(
                OutOfScopeItem(
                    payload=str(d.get("payload", "")),
                    target=str(d.get("target", "")),
                    reason="deferred deployable",
                    detail=str(d.get("status", "")),
                )
            )
        for e in l0.get("enforced_elsewhere", []) or []:
            out.append(
                OutOfScopeItem(
                    payload=str(e.get("payload", "")),
                    target=str(e.get("rule", "")),
                    reason="enforced elsewhere",
                    detail=str(e.get("enforced_by", "")),
                )
            )
    return out


def assess(
    ctx: PreflightContext,
    *,
    carrier_factory: CarrierFactory = default_carrier_factory,
) -> DeploymentPlan:
    """Detect every implemented carrier in manifest order; build the plan. Read-only.

    Calls only ``carrier.detect(target)`` — never ``apply``. A detect that raises
    (e.g. the plugin CLI is absent, a source file is missing) is captured as an
    ``error`` row rather than crashing the run, so assess stays usable against a
    degraded fleet (surfacing drift is the point).
    """
    carriers = carrier_factory(ctx.repo_root)
    entries = sorted(ctx.manifest["carriers"], key=lambda c: c.get("order", 0))
    items: list[CarrierPlanItem] = []
    for entry in entries:
        cid = str(entry.get("id", ""))
        order = int(entry.get("order", 0))
        target = entry.get("target")
        if not entry.get("implemented"):
            items.append(
                CarrierPlanItem(
                    cid, order, implemented=False, state=None,
                    action="skip -- not implemented (do-not-build doctrine)",
                )
            )
            continue
        carrier = carriers.get(cid)
        if carrier is None:
            items.append(
                CarrierPlanItem(
                    cid, order, implemented=True, state=None,
                    action="skip -- no carrier bound",
                    error="carrier id not registered in the deploy tool",
                )
            )
            continue
        try:
            state = carrier.detect(target)
        except Exception as exc:  # noqa: BLE001 — read-only: surface as drift, never crash
            items.append(
                CarrierPlanItem(
                    cid, order, implemented=True, state=None,
                    action="could not detect", error=str(exc),
                )
            )
            continue
        items.append(
            CarrierPlanItem(
                cid, order, implemented=True, state=state,
                action=planned_action(cid, state),
            )
        )
    return DeploymentPlan(
        repo=ctx.repo,
        repo_root=ctx.repo_root,
        version=ctx.version,
        source_tag=ctx.source_tag,
        items=tuple(items),
        out_of_scope=tuple(extract_out_of_scope(entries)),
    )


# ---------------------------------------------------------------------------
# Rendering — Rich, structured. The plan dataclass is the testable surface; this
# only paints it.
# ---------------------------------------------------------------------------


_STATE_STYLE = {
    CarrierState.PRESENT_CORRECT: "green",
    CarrierState.ABSENT: "yellow",
    CarrierState.PRESENT_DRIFTED: "yellow",
    CarrierState.PRESENT_WRONG_VERSION: "yellow",
}


def render_plan(plan: DeploymentPlan, console: Console | None = None) -> None:
    """Print the deployment plan (one row per carrier) + summary. Read-only output."""
    console = console or Console()
    table = Table(
        title=f"Deployment plan -- {plan.repo} @ {plan.version} "
        f"(tag {plan.source_tag}) -- ASSESS / read-only",
        title_style="bold",
    )
    table.add_column("Carrier")
    table.add_column("Order", justify="right")
    table.add_column("Detected state")
    table.add_column("Planned action")
    for item in plan.items:
        if item.state is not None:
            state_text = f"[{_STATE_STYLE.get(item.state, '')}]{item.state.value}[/]"
        elif item.error:
            state_text = "[red]ERROR[/]"
        else:
            state_text = "[dim]n/a[/]"
        table.add_row(item.carrier_id, str(item.order), state_text, item.action)
    console.print(table)

    for item in plan.errored:
        console.print(f"  [red]![/] {item.carrier_id}: could not detect -- {item.error}")

    if plan.out_of_scope:
        console.print(
            "\n[bold]Out of scope[/] (ADR-92 l0_scope -- not deployed by this tool, "
            "not failures):"
        )
        for o in plan.out_of_scope:
            console.print(f"  - {o.payload} [dim]\\[{o.reason}][/] {o.target}")

    n_apply, n_ok = len(plan.needs_apply), len(plan.correct)
    n_err, n_skip = len(plan.errored), len(plan.skipped)
    console.print(
        f"\n[bold]Summary:[/] {n_apply} need apply, {n_ok} already correct, "
        f"{n_err} could not detect, {n_skip} not implemented."
    )
    console.print(
        "[dim]No record will be written in assess mode -- run execute (C2b) to deploy.[/]"
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

    plan = assess(ctx)
    render_plan(plan)


def main() -> None:
    deploy()


if __name__ == "__main__":
    main()
