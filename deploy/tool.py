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
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path
from typing import Any

import click
import yaml
from rich.console import Console
from rich.markup import escape
from rich.table import Table

# This module lives in deploy/ beside the carriers + contract, which import each
# other flatly (``from contract import ...``). Guarantee deploy/ is importable
# whether tool.py is run as a script (sys.path[0] already covers it) or imported
# as a module by the test suite.
_DEPLOY_DIR = Path(__file__).resolve().parent
if str(_DEPLOY_DIR) not in sys.path:
    sys.path.insert(0, str(_DEPLOY_DIR))

from carrier_docs import DocsCarrier  # noqa: E402
from carrier_floor import FloorCarrier  # noqa: E402
from carrier_globalconfig import GlobalConfigCarrier  # noqa: E402
from carrier_mesh import MeshCarrier  # noqa: E402
from carrier_plugin import PluginCarrier  # noqa: E402
from carrier_precommit import PrecommitCarrier  # noqa: E402
from contract import Carrier, CarrierState, PruneState  # noqa: E402

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


# Accepts (args, cwd, *, stdin=None, stdin_bytes=None, env=None). Always binary
# I/O + explicit UTF-8 (never text mode) — see the docstring for why.
GitRunner = Callable[..., GitResult]


def _default_git(
    args: Sequence[str],
    cwd: Path,
    *,
    stdin: str | None = None,
    stdin_bytes: bytes | None = None,
    env: dict[str, str] | None = None,
) -> GitResult:
    """Real git invoker — fixed argv, no shell, ALWAYS binary I/O + explicit UTF-8.

    NEVER text mode (the Windows-text-mode-git-I/O class). On Windows
    ``subprocess(text=True)`` decodes stdout with the locale encoding (cp1252) AND
    translates ``\\n`` <-> ``\\r\\n`` — two corruptions on two axes:

    - ENCODING: git's UTF-8 output (e.g. ``—`` = ``E2 80 94``) decoded cp1252 then
      re-encoded UTF-8 becomes mojibake (this corrupted the record's comments);
    - EOL: ``\\n`` -> ``\\r\\n`` on a plumbing ``hash-object`` stdin bakes CRLF into
      the object store (autocrlf can't re-normalize plumbing).

    Binary stdin/stdout + explicit UTF-8 keeps every read AND write byte-faithful
    and LF on both axes. ``stdin`` (str) is encoded UTF-8; ``stdin_bytes`` is sent
    verbatim (e.g. the LF record blob).
    """
    full_env = {**os.environ, **env} if env else None
    data = stdin_bytes if stdin_bytes is not None else (
        stdin.encode("utf-8") if stdin is not None else None
    )
    proc = subprocess.run(  # noqa: S603,S607 — fixed argv, no shell, binary UTF-8 I/O
        ["git", *args],
        cwd=str(cwd),
        input=data,
        capture_output=True,
        env=full_env,
    )
    return GitResult(
        proc.returncode,
        # stdout = DATA: STRICT decode. The registry base_text is read here, round-
        # tripped, and re-encoded into a git object -- errors="replace" would
        # silently swap a malformed byte for U+FFFD and bake it into the record
        # (the silent-corruption class this sweep eliminates). Strict raises
        # UnicodeDecodeError, surfaced loudly via _git_checked -> RecordError.
        (proc.stdout or b"").decode("utf-8"),
        # stderr = ERROR TEXT: lenient. Git error messages can carry locale bytes
        # on Windows; never crash the error path on them.
        (proc.stderr or b"").decode("utf-8", "replace"),
    )


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
    # The consumer's registry record (deployed_methodology_version). None = the
    # registry says null: a GREENFIELD consumer no release was ever deployed to,
    # so the remove leg has nothing methodology-deployed to prune (ADR-96
    # amendment 2026-07-06 -- the prune oracle is the last-DEPLOYED shape).
    deployed_version: str | None = None


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
    entry = repos[repo]
    deployed_raw = (
        entry.get("deployed_methodology_version") if isinstance(entry, dict) else None
    )
    deployed_version = str(deployed_raw) if deployed_raw is not None else None

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
        deployed_version=deployed_version,
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
        MeshCarrier.carrier_id: MeshCarrier(repo_root),
        DocsCarrier.carrier_id: DocsCarrier(repo_root),
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
    "enforcement-mesh": "deploy seb + freshness-gate scripts + /override + Stop hook + logs/",
    "docs": "copy the manifest-declared hub docs (intake area, INSTALL.md) into the consumer",
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


_PRUNE_VERB = {
    PruneState.ALREADY_ABSENT: "already absent -- skip",
    PruneState.PRESENT_CLEAN: "would prune (remove from consumer)",
    PruneState.PRESENT_MODIFIED: "would REFUSE -- locally modified since deploy",
}


def planned_prune(state: PruneState) -> str:
    """What the remove leg would do for a removed component (narration only)."""
    return _PRUNE_VERB.get(state, "would prune")


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
class PrunePlanItem:
    """One removed component's row in the plan: its detected remove-leg state.

    The remove leg (P2) is COMPONENT-driven (not carrier-driven): a status:removed
    component is resolved to its carrier, whose detect_prune reports whether the
    artifact is present-clean (will remove), locally-modified (will refuse), or
    already absent (no-op). ``removed_in`` / ``reason`` carry the tombstone record.
    """

    component_id: str
    carrier_id: str
    removed_in: str
    reason: str
    state: PruneState | None  # None if detect_prune errored / no carrier
    action: str
    error: str | None = None


@dataclass(frozen=True)
class DeploymentPlan:
    """The full assess result for one consumer @ one release. Read-only."""

    repo: str
    repo_root: Path
    version: str
    source_tag: str
    items: tuple[CarrierPlanItem, ...]
    out_of_scope: tuple[OutOfScopeItem, ...]
    prune_items: tuple[PrunePlanItem, ...] = ()
    # True when the consumer's registry record is null (never deployed). The
    # remove leg is component-driven off the LAST-DEPLOYED shape (ADR-96 D2);
    # with no deploy ever recorded, "locally modified since deploy" is a
    # category error -- any URL-matched artifact is consumer property, not
    # methodology residue, so --execute skips the prune sweep entirely
    # (ADR-96 amendment 2026-07-06). prune_items stays POPULATED (read-only
    # detect) so assess remains honest about what exists on disk.
    greenfield: bool = False

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

    @property
    def prune_pending(self) -> tuple[PrunePlanItem, ...]:
        """Removed components whose artifact is PRESENT (clean or modified) — the
        sweep will touch a real artifact. Drives the destroy-confirm gate.
        Empty on a greenfield consumer: the sweep never runs, so nothing is
        pending and no destroy-confirm may fire (ADR-96 amendment)."""
        if self.greenfield:
            return ()
        return tuple(
            i for i in self.prune_items
            if i.state in (PruneState.PRESENT_CLEAN, PruneState.PRESENT_MODIFIED)
        )


def build_prune_plan(
    manifest: dict[str, Any], carriers: dict[str, Carrier]
) -> tuple[PrunePlanItem, ...]:
    """Detect the remove-leg state of every status:removed component. Read-only.

    Component-driven: filter components: to status:removed, resolve each to its
    carrier, call detect_prune(component). A carrier with no remove leg
    (PruneUnsupported) or a detect_prune that raises is captured as an error row,
    never a crash — mirroring assess's degraded-fleet tolerance.
    """
    items: list[PrunePlanItem] = []
    for comp in manifest.get("components", []) or []:
        if not isinstance(comp, dict) or comp.get("status") != "removed":
            continue
        cid = str(comp.get("id", ""))
        carrier_id = str(comp.get("carrier", ""))
        removed_in = str(comp.get("removed_in", ""))
        reason = str(comp.get("reason", ""))
        carrier = carriers.get(carrier_id)
        if carrier is None:
            items.append(PrunePlanItem(
                cid, carrier_id, removed_in, reason, state=None,
                action="skip -- no carrier bound",
                error="carrier id not registered in the deploy tool",
            ))
            continue
        try:
            state = carrier.detect_prune(comp)
        except Exception as exc:  # noqa: BLE001 — read-only: surface, never crash
            items.append(PrunePlanItem(
                cid, carrier_id, removed_in, reason, state=None,
                action="could not detect", error=str(exc),
            ))
            continue
        items.append(PrunePlanItem(
            cid, carrier_id, removed_in, reason, state=state,
            action=planned_prune(state),
        ))
    return tuple(items)


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
        prune_items=build_prune_plan(ctx.manifest, carriers),
        greenfield=ctx.deployed_version is None,
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

    if plan.prune_items:
        console.print(
            "\n[bold]Remove leg[/] (status:removed components -- the prune sweep):"
        )
        ptable = Table(show_header=True, title_style="bold")
        ptable.add_column("Component")
        ptable.add_column("Carrier")
        ptable.add_column("removed_in", justify="right")
        ptable.add_column("Prune state")
        ptable.add_column("Planned action")
        for p in plan.prune_items:
            if p.state is PruneState.PRESENT_MODIFIED:
                st = "[red]present_modified[/]"
            elif p.state is PruneState.PRESENT_CLEAN:
                st = "[yellow]present_clean[/]"
            elif p.state is PruneState.ALREADY_ABSENT:
                st = "[green]already_absent[/]"
            else:
                st = "[red]ERROR[/]"
            ptable.add_row(p.component_id, p.carrier_id, p.removed_in, st, p.action)
        console.print(ptable)
        for p in plan.prune_items:
            if p.error:
                console.print(f"  [red]![/] {p.component_id}: {p.error}")
        if plan.greenfield:
            console.print(
                "  [yellow]Remove leg SKIPPED on --execute -- greenfield consumer "
                "(deployed_methodology_version: null; nothing methodology-deployed "
                "to prune; ADR-96 REFUSE semantics preserved for previously-deployed "
                "consumers).[/]"
            )
        elif plan.prune_pending:
            console.print(
                f"  [yellow]{len(plan.prune_pending)} present artifact(s) -- "
                "--execute will REQUIRE confirmation before pruning "
                "(--auto-approve to skip in scripted runs).[/]"
            )

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
# EXECUTE (C2b) — the WRITER. apply -> verify per carrier, gate the version-record
# write on EVERY carrier verifying (ADR-92 Decision 9). Two writes on full
# success only: stage the consumer (write-yes / commit-no, Decision 3) + commit
# the record on a hub branch the operator merges (Decision 4). On ANY verify
# failure: ABORT -- no stage, no record (the consumer may be partially applied;
# the reconcile is rerunnable).
# ---------------------------------------------------------------------------


class RecordError(Exception):
    """A record-write or consumer-staging git operation failed."""


# Field lines under a repo entry in the registry (4-space indent, ADR-91 schema).
_RECORD_FIELDS = ("deployed_methodology_version", "deployed_date", "source_tag")
_REPO_HEADER_RE = re.compile(r"^  (\S[^:]*):\s*$")
_FIELD_RE = re.compile(rf"^    ({'|'.join(_RECORD_FIELDS)}):\s*.*$")


def _set_repo_record(
    text: str, repo: str, *, deployed_version: str, deployed_date: str, source_tag: str
) -> str:
    """Set a repo's three record fields in-place, preserving comments + layout.

    A surgical line edit (NOT a yaml round-trip, which would strip the registry's
    explanatory header comments). Finds ``  <repo>:`` then rewrites the three
    4-space-indented field lines in that block; everything else is byte-preserved.
    Raises RecordError if the repo block or any field line is not found.
    """
    values = {
        "deployed_methodology_version": deployed_version,
        "deployed_date": deployed_date,
        "source_tag": source_tag,
    }
    out: list[str] = []
    in_block = False
    found_repo = False
    seen: set[str] = set()
    target_header = f"  {repo}:"
    for line in text.splitlines():
        if not in_block:
            out.append(line)
            if line.rstrip() == target_header:
                in_block = True
                found_repo = True
            continue
        # Inside the target repo block. A new repo header (or a dedented line)
        # ends it.
        m = _FIELD_RE.match(line)
        if m:
            key = m.group(1)
            out.append(f'    {key}: "{values[key]}"')
            seen.add(key)
            continue
        if _REPO_HEADER_RE.match(line) or (line and not line.startswith("    ")):
            in_block = False
        out.append(line)
    if not found_repo:
        raise RecordError(f"{repo!r} not found under 'repos:' in the registry")
    missing = [f for f in _RECORD_FIELDS if f not in seen]
    if missing:
        raise RecordError(f"could not set fields {missing} for {repo!r}")
    return "\n".join(out) + "\n"


def _git_checked(git: GitRunner, args: Sequence[str], cwd: Path, what: str, **kw: Any) -> GitResult:
    """Run a git command; raise RecordError on non-zero or non-UTF-8 output.

    A strict stdout decode (see _default_git) raises UnicodeDecodeError on
    malformed bytes; surface it loudly as a RecordError rather than letting a raw
    decode traceback escape or -- worse -- silently corrupting the round-tripped
    record. No silent partial write.
    """
    try:
        res = git(args, cwd, **kw)
    except UnicodeDecodeError as exc:
        raise RecordError(f"{what} produced non-UTF-8 output: {exc}") from exc
    if res.returncode != 0:
        raise RecordError(f"{what} failed (git {args[0]} exit {res.returncode}): {res.stderr.strip()}")
    return res


def write_record_to_branch(
    hub_root: Path,
    repo: str,
    *,
    deployed_version: str,
    source_tag: str,
    deployed_date: str,
    registry_rel: str = "ecosystem/deployed-versions.yaml",
    base_ref: str = "main",
    branch: str | None = None,
    git: GitRunner = _default_git,
) -> str:
    """Commit the deployed-version record on a NEW hub branch (ADR-92 Decision 4).

    Uses git plumbing (hash-object + a throwaway index via GIT_INDEX_FILE +
    commit-tree + branch) so the operator's checked-out branch, HEAD, working
    tree, and index are NEVER disturbed. The record is based on the committed
    ``base_ref`` (main), not the working tree, and the branch is left for the
    operator to merge -- it is NOT written to main and NOT auto-merged.
    """
    branch = branch or f"deploy/record-{repo}-{deployed_version}"
    base_text = _git_checked(
        git, ["show", f"{base_ref}:{registry_rel}"], hub_root,
        f"read {registry_rel}@{base_ref}",
    ).stdout
    new_text = _set_repo_record(
        base_text, repo, deployed_version=deployed_version,
        deployed_date=deployed_date, source_tag=source_tag,
    )
    # Write the blob as LF BYTES (not text-mode stdin): hash-object is plumbing, so
    # a CRLF blob here (from Windows text-mode translation) would be baked into the
    # object store untouched by autocrlf, flipping the whole registry file to CRLF
    # on merge. LF bytes keep the record blob byte-consistent with the LF registry.
    blob = _git_checked(
        git, ["hash-object", "-w", "--stdin"], hub_root, "write record blob",
        stdin_bytes=new_text.encode("utf-8"),
    ).stdout.strip()
    base_commit = _git_checked(
        git, ["rev-parse", base_ref], hub_root, f"resolve {base_ref}",
    ).stdout.strip()

    idx = Path(tempfile.gettempdir()) / f"deploy-record-index-{os.getpid()}-{blob[:12]}"
    try:
        env = {"GIT_INDEX_FILE": str(idx)}
        _git_checked(git, ["read-tree", base_ref], hub_root, "seed temp index", env=env)
        _git_checked(
            git, ["update-index", "--add", "--cacheinfo", f"100644,{blob},{registry_rel}"],
            hub_root, "stage record in temp index", env=env,
        )
        tree = _git_checked(git, ["write-tree"], hub_root, "write tree", env=env).stdout.strip()
    finally:
        if idx.exists():
            idx.unlink()  # no leftovers — the throwaway index is removed

    msg = (
        f"deploy(record): {repo} -> methodology {deployed_version} "
        f"(tag {source_tag}, {deployed_date}) [ADR-91/92]\n\n"
        f"Deployed-version record for {repo}, written by the deploy tool (C2b) on "
        f"full per-carrier verify success. Operator merges this branch to main."
    )
    commit = _git_checked(
        git, ["commit-tree", tree, "-p", base_commit, "-m", msg], hub_root, "commit record",
    ).stdout.strip()
    _git_checked(
        git, ["branch", branch, commit], hub_root,
        f"create record branch {branch} (already exists?)",
    )
    log.info("deploy record committed on %s (%s)", branch, commit[:12])
    return branch


def stage_consumer(repo_root: Path, *, git: GitRunner = _default_git) -> tuple[str, ...]:
    """Stage the carriers' consumer writes (ADR-92 Decision 3: write-yes / commit-no).

    ``git add -A`` in the consumer -- safe + exact because preflight required a
    clean consumer tree, so the only changes present are the carriers' applies.
    Returns the staged paths for the operator to review (`git diff --cached`) and
    commit. The tool NEVER commits in the consumer.
    """
    _git_checked(git, ["add", "-A"], repo_root, f"stage consumer {repo_root}")
    staged = _git_checked(
        git, ["diff", "--cached", "--name-only"], repo_root, "list staged paths",
    ).stdout
    return tuple(p for p in staged.splitlines() if p.strip())


def _target_for(manifest: dict[str, Any], carrier_id: str) -> Any:
    """The manifest target entry for a carrier id (what apply/verify receive)."""
    for c in manifest.get("carriers", []) or []:
        if c.get("id") == carrier_id:
            return c.get("target")
    return None


def _component_for(manifest: dict[str, Any], component_id: str) -> dict[str, Any] | None:
    """The manifest component entry for an id (what detect_prune/prune/verify_pruned receive)."""
    for c in manifest.get("components", []) or []:
        if isinstance(c, dict) and c.get("id") == component_id:
            return c
    return None


@dataclass(frozen=True)
class CarrierExecOutcome:
    """One carrier's execute outcome: what was applied + whether it verified."""

    carrier_id: str
    order: int
    detected: CarrierState | None
    applied: bool          # apply() was invoked
    apply_changed: bool    # apply() reported a real change
    verify_ok: bool | None  # None if verify was never reached
    verify_failures: tuple[str, ...] = ()
    error: str | None = None  # detect/apply/verify raised


@dataclass(frozen=True)
class PruneExecOutcome:
    """One removed component's execute outcome: pruned / refused / verified-absent.

    ``pruned`` True iff the artifact was removed AND verify_pruned confirmed absence.
    ``refused`` names a hash-guard conflict (locally modified). ``removed_in`` /
    ``reason`` carry the tombstone record for the render + operator log.
    """

    component_id: str
    carrier_id: str
    removed_in: str
    reason: str
    state: PruneState | None
    pruned: bool
    refused: tuple[str, ...] = ()
    verify_ok: bool | None = None
    verify_failures: tuple[str, ...] = ()
    error: str | None = None


@dataclass(frozen=True)
class ExecuteResult:
    """The full execute result. ``aborted`` => no record, no staging."""

    repo: str
    version: str
    source_tag: str
    outcomes: tuple[CarrierExecOutcome, ...]
    aborted: bool
    failed_carrier: str | None
    record_branch: str | None
    staged_paths: tuple[str, ...]
    out_of_scope: tuple[OutOfScopeItem, ...] = ()
    prune_outcomes: tuple[PruneExecOutcome, ...] = ()
    prune_declined: bool = False  # operator declined the destroy-confirm
    # True when the remove leg was skipped because the consumer is greenfield
    # (registry record null -- ADR-96 amendment); rendered as operator evidence.
    prune_skipped_greenfield: bool = False


PruneConfirm = Callable[["Sequence[PrunePlanItem]"], bool]


def _default_prune_confirm(pending: Sequence[PrunePlanItem]) -> bool:
    """Interactive destroy-confirmation (Terraform-style) for the prune sweep.

    Prints the components that will be pruned and asks for an explicit yes. Used
    only when --execute has a present removed component and --auto-approve is off.
    Tests inject their own confirm fn; the CLI passes this.
    """
    lines = "\n".join(
        f"  - {p.component_id} ({p.carrier_id}, removed_in {p.removed_in}) -- {p.action}"
        for p in pending
    )
    click.echo(
        f"\nThe remove leg will PRUNE {len(pending)} component(s) from the consumer:\n{lines}"
    )
    return click.confirm("Proceed with the prune?", default=False)


def execute(
    ctx: PreflightContext,
    *,
    carrier_factory: CarrierFactory = default_carrier_factory,
    force: bool = False,
    git: GitRunner = _default_git,
    hub_root: Path = _HUB_ROOT,
    today: str | None = None,
    auto_approve: bool = False,
    prune_confirm: PruneConfirm = _default_prune_confirm,
) -> ExecuteResult:
    """Apply + verify every carrier, then prune removed components; gate the record.

    Per carrier (manifest order): if it needs apply (drifted/absent) OR ``force``
    -> apply() then verify(); if already correct -> verify() only (confirm).
    Then the REMOVE LEG (P2): converge-then-prune — after the add-loop succeeds,
    prune every status:removed component. A destroy-confirm is REQUIRED before
    pruning when a removed artifact is present, unless ``auto_approve``. On a
    GREENFIELD consumer (registry record null) the sweep is skipped entirely —
    nothing methodology-deployed exists to prune (ADR-96 amendment 2026-07-06).
    Fail-fast: the first carrier that fails verify, OR a prune that REFUSES (a
    locally-modified target), OR a failed verify_pruned, OR a declined confirm,
    ABORTS the run -- no consumer staging, no record write. So there is never a
    state where the record says success while a removed component is still present
    (D9 / criterion 5). The reconcile is rerunnable.
    """
    carriers = carrier_factory(ctx.repo_root)
    plan = assess(ctx, carrier_factory=lambda _root: carriers)

    outcomes: list[CarrierExecOutcome] = []
    failed: str | None = None
    for item in plan.items:
        if not item.implemented:
            continue  # not part of execute (declared, not built)
        carrier = carriers.get(item.carrier_id)
        if carrier is None or item.state is None:
            # no carrier bound, or detect errored -> cannot safely apply: abort.
            outcomes.append(
                CarrierExecOutcome(
                    item.carrier_id, item.order, item.state, applied=False,
                    apply_changed=False, verify_ok=False,
                    error=item.error or "no carrier bound / detect failed",
                )
            )
            failed = item.carrier_id
            break

        target = _target_for(ctx.manifest, item.carrier_id)
        do_apply = force or item.state.needs_apply
        applied = apply_changed = False
        try:
            if do_apply:
                ar = carrier.apply(target)
                applied = True
                apply_changed = ar.changed
            vr = carrier.verify(target)
        except Exception as exc:  # noqa: BLE001 — a carrier failure aborts; never record
            outcomes.append(
                CarrierExecOutcome(
                    item.carrier_id, item.order, item.state, applied=applied,
                    apply_changed=apply_changed, verify_ok=False, error=str(exc),
                )
            )
            failed = item.carrier_id
            break

        outcomes.append(
            CarrierExecOutcome(
                item.carrier_id, item.order, item.state, applied=applied,
                apply_changed=apply_changed, verify_ok=vr.ok,
                verify_failures=tuple(vr.failures),
            )
        )
        if not vr.ok:
            failed = item.carrier_id
            break

    aborted = failed is not None

    # --- REMOVE LEG (P2 / ADR-96) — converge-then-prune. Runs only if the add-loop
    # fully succeeded. Destroy-confirm gates a present prune (unless auto_approve);
    # a decline, a REFUSE (locally-modified target), or a failed verify_pruned aborts
    # BEFORE any stage/record, so the record never reports success with a removed
    # component still present (criterion 3/5 / D9). ---
    prune_outcomes: list[PruneExecOutcome] = []
    prune_declined = False
    # Greenfield consumers (registry record null) skip the sweep entirely: the
    # prune oracle is the last-DEPLOYED shape, and nothing was ever deployed
    # here -- a URL-matched artifact is consumer property, never methodology
    # residue (ADR-96 amendment 2026-07-06).
    if not aborted and not plan.greenfield:
        pending = plan.prune_pending
        if pending and not auto_approve and not prune_confirm(pending):
            prune_declined = True
            aborted = True
        if not aborted:
            for p in plan.prune_items:
                carrier = carriers.get(p.carrier_id)
                comp = _component_for(ctx.manifest, p.component_id)
                if carrier is None or comp is None:
                    prune_outcomes.append(PruneExecOutcome(
                        p.component_id, p.carrier_id, p.removed_in, p.reason,
                        state=p.state, pruned=False, verify_ok=False,
                        error=p.error or "no carrier bound / component not found",
                    ))
                    failed = p.component_id
                    aborted = True
                    break
                try:
                    state = carrier.detect_prune(comp)  # fresh — apply ran since assess
                    if state is PruneState.ALREADY_ABSENT:
                        prune_outcomes.append(PruneExecOutcome(
                            p.component_id, p.carrier_id, p.removed_in, p.reason,
                            state=state, pruned=False, verify_ok=True,
                        ))
                        continue
                    pr = carrier.prune(comp)
                    if not pr.pruned:  # REFUSED (locally modified) — no delete
                        prune_outcomes.append(PruneExecOutcome(
                            p.component_id, p.carrier_id, p.removed_in, p.reason,
                            state=state, pruned=False, refused=pr.refused,
                            verify_ok=False, error=pr.detail,
                        ))
                        failed = p.component_id
                        aborted = True
                        break
                    vr = carrier.verify_pruned(comp)
                except Exception as exc:  # noqa: BLE001 — a prune failure aborts; never record
                    prune_outcomes.append(PruneExecOutcome(
                        p.component_id, p.carrier_id, p.removed_in, p.reason,
                        state=p.state, pruned=False, verify_ok=False, error=str(exc),
                    ))
                    failed = p.component_id
                    aborted = True
                    break
                prune_outcomes.append(PruneExecOutcome(
                    p.component_id, p.carrier_id, p.removed_in, p.reason,
                    state=state, pruned=vr.ok, verify_ok=vr.ok,
                    verify_failures=tuple(vr.failures),
                ))
                if not vr.ok:  # pruned but verify_pruned did not confirm absence
                    failed = p.component_id
                    aborted = True
                    break

    record_branch: str | None = None
    staged: tuple[str, ...] = ()
    if not aborted:
        # FULL SUCCESS only — two writes, two contexts (ADR-92 Decisions 3 + 4):
        # (1) stage the consumer's carrier changes (write-yes / commit-no);
        # (2) commit the version record on a hub branch the operator merges.
        staged = stage_consumer(ctx.repo_root, git=git)
        record_branch = write_record_to_branch(
            hub_root,
            ctx.repo,
            deployed_version=str(ctx.manifest.get("methodology_version", ctx.bare_version)),
            source_tag=ctx.source_tag,
            deployed_date=today or _date.today().isoformat(),
            git=git,
        )

    return ExecuteResult(
        repo=ctx.repo,
        version=ctx.version,
        source_tag=ctx.source_tag,
        outcomes=tuple(outcomes),
        aborted=aborted,
        failed_carrier=failed,
        record_branch=record_branch,
        staged_paths=staged,
        out_of_scope=plan.out_of_scope,
        prune_outcomes=tuple(prune_outcomes),
        prune_declined=prune_declined,
        prune_skipped_greenfield=plan.greenfield and bool(plan.prune_items),
    )


def render_execute(result: ExecuteResult, console: Console | None = None) -> None:
    """Print the per-carrier execute outcomes + the gate verdict."""
    console = console or Console()
    table = Table(
        title=f"Deploy EXECUTE -- {result.repo} @ {result.version} "
        f"(tag {result.source_tag})",
        title_style="bold",
    )
    table.add_column("Carrier")
    table.add_column("Order", justify="right")
    table.add_column("Detected")
    table.add_column("Action")
    table.add_column("Verify")
    for o in result.outcomes:
        detected = o.detected.value if o.detected else "[red]ERROR[/]"
        if o.applied:
            action = "applied" if o.apply_changed else "applied (no change)"
        else:
            action = "verify-only"
        if o.error:
            verify = "[red]ERROR[/]"
        elif o.verify_ok is True:
            verify = "[green]ok[/]"
        elif o.verify_ok is False:
            verify = "[red]FAIL[/]"
        else:
            verify = "-"
        table.add_row(o.carrier_id, str(o.order), detected, action, verify)
    console.print(table)

    # Remove-leg outcomes (P2) + tombstone records.
    if result.prune_outcomes:
        ptable = Table(title="Remove leg -- prune sweep", title_style="bold")
        ptable.add_column("Component")
        ptable.add_column("Carrier")
        ptable.add_column("Prune")
        ptable.add_column("Verify absent")
        for po in result.prune_outcomes:
            if po.refused:
                pverb = "[red]REFUSED[/]"
            elif po.state is PruneState.ALREADY_ABSENT:
                pverb = "already absent"
            elif po.pruned:
                pverb = "[green]pruned[/]"
            else:
                pverb = "[red]not pruned[/]"
            if po.verify_ok is True:
                pver = "[green]ABSENT[/]"
            elif po.verify_ok is False:
                pver = "[red]FAIL[/]"
            else:
                pver = "-"
            ptable.add_row(po.component_id, po.carrier_id, pverb, pver)
        console.print(ptable)
        # Tombstone records — the operator logs these (JOURNAL / audit trail).
        pruned_ok = [po for po in result.prune_outcomes if po.pruned and po.verify_ok]
        if pruned_ok:
            console.print("\n[bold]Tombstone record(s)[/] (append to the audit trail):")
            for po in pruned_ok:
                # #247: escape the interpolated data — a reason carrying a bracketed backlog
                # id (e.g. "[#244]") is read by Rich as a markup tag and DROPPED from the
                # printed record, which is the copy-source for the JOURNAL tombstone; a
                # vanished [#id] there trips backlog-id-on-close / git_backlog_drift at fleet
                # scale. escape() keeps the brackets literal.
                console.print(
                    f"  [dim]tombstone[/] {escape(po.component_id)} | "
                    f"removed_in {escape(po.removed_in)} | "
                    f"carrier {escape(po.carrier_id)} | reason: {escape(po.reason)}"
                )

    if result.prune_skipped_greenfield:
        console.print(
            "\n[yellow]Remove leg SKIPPED[/] -- greenfield consumer "
            "(deployed_methodology_version: null; nothing methodology-deployed "
            "to prune; ADR-96 amendment)."
        )

    if result.aborted:
        if result.prune_declined:
            console.print(
                "\n[yellow bold]ABORTED[/] -- prune declined at the confirm prompt. "
                "NO record written; consumer NOT staged. Re-run with --auto-approve "
                "to skip the prompt in scripted runs."
            )
            return
        reason = f"{result.failed_carrier} did not verify"
        refused = [po for po in result.prune_outcomes if po.refused]
        if refused:
            reason = f"{result.failed_carrier} prune REFUSED (locally-modified target)"
        console.print(
            f"\n[red bold]ABORTED[/] -- {reason}. "
            "NO record written; consumer NOT staged. The reconcile is rerunnable."
        )
        for o in result.outcomes:
            if o.error:
                console.print(f"  [red]![/] {o.carrier_id}: {o.error}")
            elif o.verify_ok is False:
                console.print(f"  [red]![/] {o.carrier_id}: {', '.join(o.verify_failures)}")
        for po in result.prune_outcomes:
            if po.refused:
                console.print(f"  [red]![/] {po.component_id}: {', '.join(po.refused)}")
            elif po.verify_ok is False and po.error:
                console.print(f"  [red]![/] {po.component_id}: {po.error}")
            elif po.verify_ok is False:
                console.print(f"  [red]![/] {po.component_id}: {', '.join(po.verify_failures)}")
        return

    console.print("\n[green bold]SUCCESS[/] -- every carrier verified.")
    if result.record_branch is None:
        console.print(
            "[dim]Record write + consumer staging land in step 4 of this build.[/]"
        )
        return
    console.print(
        f"Hub record committed on branch [bold]{result.record_branch}[/] -- the "
        "operator merges it to main (NOT auto-merged)."
    )
    if result.staged_paths:
        console.print(
            f"Consumer staged ({len(result.staged_paths)} path(s)) -- review "
            "`git -C <consumer> diff --cached`, then commit in the consumer:"
        )
        for p in result.staged_paths:
            console.print(f"  [green]+[/] {p}")
    else:
        console.print("Consumer already at target -- nothing to stage.")


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


@click.command()
@click.argument("repo")
@click.option(
    "--target",
    "version",
    required=True,
    help="Methodology release to deploy/assess against (e.g. v1.0.0); selects the manifest.",
)
@click.option(
    "--execute",
    "do_execute",
    is_flag=True,
    help="Apply carriers, verify, and (on full success) stage the consumer + write the record.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Re-apply carriers even when detect says they are already correct.",
)
@click.option(
    "--auto-approve",
    "auto_approve",
    is_flag=True,
    help="Skip the interactive prune confirmation (Terraform-style) for scripted runs. "
    "Without it, --execute prompts before pruning any present status:removed component.",
)
def deploy(repo: str, version: str, do_execute: bool, force: bool, auto_approve: bool) -> None:
    """Deploy <REPO> against --target. Without --execute: read-only assess + plan.

    With --execute: apply each needing-apply carrier then verify; then prune every
    status:removed component (destroy-confirm required unless --auto-approve); gate
    the version-record write on EVERY carrier verifying AND every prune verifying
    absent. On full success stage the consumer (commit-no) and commit the record on
    a hub branch the operator merges. On any verify failure, prune refusal, or
    declined confirm: abort with no record + no staging.
    """
    try:
        ctx = preflight(repo, version)
    except PreflightError as exc:
        raise click.ClickException(f"preflight failed -- {exc}") from exc

    if not do_execute:
        render_plan(assess(ctx))
        return

    try:
        result = execute(ctx, force=force, auto_approve=auto_approve)
    except RecordError as exc:
        raise click.ClickException(f"deploy execute -- write failed: {exc}") from exc
    render_execute(result)
    if result.aborted:
        click.get_current_context().exit(1)


def main() -> None:
    deploy()


if __name__ == "__main__":
    main()
