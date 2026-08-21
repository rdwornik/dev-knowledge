#!/usr/bin/env python
"""[#554] cloud-lane provisioning guard - history sufficiency, ecosystem seeding, prebuild drift.

WHAT THIS IS FOR. `.devcontainer/provision.sh` closes the four legs `[#554]`'s row names, and
`docs/audits/2026-08-19-technical-554-proof.md` measured all four asserting clean on the
Codespaces free tier. Two things it does NOT close were measured by the same pair of audits, and
this module closes them — each reading its settings from `.devcontainer/provisioning.yaml`
rather than carrying a literal:

  history    B1. Leg 2 unshallows, so a cloud clone has DEPTH. It does not necessarily have
             REFS: the proof lane's codespace carried 5329 commits and no local `main`, and
             every instrument that walks main's first-parent spine then ERRORED
             (`AnchorError(... 'fatal: Not a valid object name main')`) rather than passing
             vacuously. "Not shallow" is necessary and insufficient; this asserts the
             sufficient precondition and repairs it BEFORE a lane can reach a spine walker.

  ecosystem  L5. `audit.py health` reports `repos registered (none)` in a fresh container, which
             is the last thing between this substrate and `[#554]`'s D1a Done-when. Not
             structural: `discover_repos()` counts `ecosystem/*/state.yaml`, that glob is
             GITIGNORED, and so no clone has ever carried one. The workstation copies them from
             the primary checkout (`scripts/worktree_seed.py` `_COPY_MANIFEST`, whose comment
             names this exact symptom); a container has no primary, so it audits the one repo it
             has and saves the genuine result.

  prebuild   A3. Reports whether the live Codespaces prebuild configuration agrees with the
             declaration. There is NO public API for prebuild configurations (probed
             2026-08-21: REST 404, GraphQL introspection empty, no `gh codespace` subcommand),
             so the comparison runs against the one field the API does expose —
             `prebuild_availability` on the machines endpoint.

REUSE, NOT REIMPLEMENTATION. `ecosystem --repair` calls `audit.audit_repo` + `audit.save_state`,
the same pair `audit.py repo` uses, and deliberately NOT `audit.py repo` itself: that command
also appends history, writes a report under `docs/audits/` and commits its outputs, none of
which a provisioning step may do to a container's tree. `save_state` writes exactly one
gitignored file.

EXIT CODES. 0 clean · 1 a real violation (looked, and found drift) · 2 could not look (missing
tool, no remote, unreadable config, internal error). The 1/2 split is the repo's
declared-absence-over-false-resolves rule (STANDING_RULINGS F4): "the guard could not run" and
"the guard ran and failed" are different facts and must not share an exit code.

WIRED INTO NO GATE. This is provisioning machinery called by `provision.sh`; it is not a
pre-commit hook and adding it to one is a separate, surfaced act.
"""
from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

LOG = logging.getLogger("cloud_provisioning")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / ".devcontainer" / "provisioning.yaml"
CONFIG_SCHEMA = "dev-knowledge-cloud-provisioning/1"

EXIT_OK = 0
EXIT_VIOLATION = 1
EXIT_UNAVAILABLE = 2

#: `history.disposition` values. `repair` restores the refs; `exclude` declares the spine
#: walkers out of scope for cloud lanes and reports them rather than acting.
DISPOSITIONS = ("repair", "exclude")

_GIT_TIMEOUT = 600      # an --unshallow of this repo's ~5400 commits, with headroom
_GH_TIMEOUT = 60


class ProvisioningError(Exception):
    """Raised when the guard cannot LOOK - distinct from looking and finding drift."""


# --- configuration ----------------------------------------------------------------------


@dataclass(frozen=True)
class HistoryConfig:
    disposition: str
    required_refs: tuple[str, ...]
    spine_walking_instruments: tuple[str, ...] = ()


@dataclass(frozen=True)
class EcosystemConfig:
    self_register: bool
    self_name: str


@dataclass(frozen=True)
class PrebuildConfig:
    configured: bool
    trigger: str
    regions: tuple[str, ...]
    template_history: int
    repository: str


@dataclass(frozen=True)
class Config:
    history: HistoryConfig
    ecosystem: EcosystemConfig
    prebuild: PrebuildConfig


def load_config(path: Path = CONFIG_PATH) -> Config:
    """Read `.devcontainer/provisioning.yaml`, or raise ProvisioningError."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProvisioningError(f"provisioning declaration not found at {path}") from exc
    except (OSError, yaml.YAMLError) as exc:
        raise ProvisioningError(f"provisioning declaration at {path} is unreadable: {exc}") from exc

    if not isinstance(raw, dict):
        raise ProvisioningError(f"provisioning declaration at {path} is not a mapping")
    schema = raw.get("schema")
    if schema != CONFIG_SCHEMA:
        raise ProvisioningError(
            f"provisioning declaration schema is {schema!r}, expected {CONFIG_SCHEMA!r}")

    hist = raw.get("history") or {}
    disposition = hist.get("disposition")
    if disposition not in DISPOSITIONS:
        raise ProvisioningError(
            f"history.disposition is {disposition!r}, expected one of {list(DISPOSITIONS)}")
    refs = tuple(hist.get("required_refs") or ())
    if not refs:
        raise ProvisioningError("history.required_refs is empty - nothing to assert")

    eco = raw.get("ecosystem") or {}
    pre = raw.get("prebuild") or {}
    return Config(
        history=HistoryConfig(
            disposition=disposition,
            required_refs=refs,
            spine_walking_instruments=tuple(hist.get("spine_walking_instruments") or ()),
        ),
        ecosystem=EcosystemConfig(
            self_register=bool(eco.get("self_register", False)),
            self_name=str(eco.get("self_name") or ".dev-knowledge"),
        ),
        prebuild=PrebuildConfig(
            configured=bool(pre.get("configured", False)),
            trigger=str(pre.get("trigger") or ""),
            regions=tuple(pre.get("regions") or ()),
            template_history=int(pre.get("template_history") or 0),
            repository=str(pre.get("repository") or ""),
        ),
    )


# --- git ---------------------------------------------------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run one git command in `root`. Raises ProvisioningError when git itself is unusable."""
    try:
        return subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True, timeout=_GIT_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProvisioningError(f"git {' '.join(args)} could not run: {exc}") from exc


def is_shallow(root: Path) -> bool:
    r = _git(root, "rev-parse", "--is-shallow-repository")
    if r.returncode != 0:
        raise ProvisioningError(f"git rev-parse --is-shallow-repository failed: {r.stderr.strip()}")
    return r.stdout.strip() == "true"


def ref_resolves(root: Path, ref: str) -> bool:
    """True when `ref` names a commit in THIS clone. `--verify` refuses an ambiguous name."""
    return _git(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode == 0


def spine_length(root: Path, ref: str) -> int | None:
    """First-parent spine entries reachable from `ref`, or None when the walk itself fails.

    This is the exact shape every instrument in `history.spine_walking_instruments` performs,
    so a walk that works here is the precondition they need — not a proxy for it.
    """
    r = _git(root, "log", "--first-parent", "--format=%H", ref)
    if r.returncode != 0:
        return None
    return len([line for line in r.stdout.splitlines() if line.strip()])


def has_remote(root: Path, name: str = "origin") -> bool:
    r = _git(root, "remote")
    return r.returncode == 0 and name in r.stdout.split()


def current_branch(root: Path) -> str | None:
    """The checked-out branch name, or None on a detached HEAD.

    Raises on a git failure rather than returning None: an unknown branch state must not be
    mistaken for a detached HEAD. (`scripts/block_commit_on_main.py` documents the opposite
    choice for its own hook; the divergence is deliberate — this one never gates a commit.)
    """
    r = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if r.returncode == 0:
        return r.stdout.strip()
    if r.stderr.strip():
        raise ProvisioningError(f"git symbolic-ref failed: {r.stderr.strip()}")
    return None


# --- history: assess and repair ----------------------------------------------------------


@dataclass
class HistoryReport:
    shallow: bool
    refs: dict[str, int | None] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


def assess_history(root: Path, cfg: HistoryConfig) -> HistoryReport:
    """Look at the clone and report whether a spine walker could run here. Never writes."""
    report = HistoryReport(shallow=is_shallow(root))
    if report.shallow:
        report.violations.append(
            "clone is SHALLOW - every history-dependent detector reads vacuously")

    for ref in cfg.required_refs:
        if not ref_resolves(root, ref):
            report.refs[ref] = None
            report.violations.append(
                f"ref {ref!r} does not resolve in this clone - a spine walker errors out "
                f"(the measured shape: \"fatal: Not a valid object name {ref}\")")
            continue
        length = spine_length(root, ref)
        report.refs[ref] = length
        if length is None:
            report.violations.append(
                f"ref {ref!r} resolves but `git log --first-parent {ref}` failed - the walk "
                f"the instruments perform does not work here")
        elif length == 0:
            report.violations.append(
                f"ref {ref!r} walks to an EMPTY first-parent spine - the instruments would "
                f"pass on nothing, which is the vacuous-gate failure shape leg 2 exists to close")
    return report


def repair_history(root: Path, cfg: HistoryConfig) -> HistoryReport:
    """Deepen the clone and restore the required refs, then re-assess.

    Gated throughout: `--unshallow` is an error on a complete clone, and fetching a ref that is
    already checked out is an error too, so each action runs only when its precondition holds.
    Idempotent — a second run performs no action and says so.
    """
    report = assess_history(root, cfg)
    if report.ok:
        return report

    if not has_remote(root):
        report.violations.append(
            "no `origin` remote - a clone missing history cannot be repaired here")
        return report

    if report.shallow:
        LOG.info("history: clone is shallow - fetching full history (git fetch --unshallow)")
        r = _git(root, "fetch", "--unshallow", "--quiet")
        if r.returncode != 0:
            report.violations.append(f"`git fetch --unshallow` failed: {r.stderr.strip()}")
            return report
        report.actions.append("git fetch --unshallow")

    checked_out = current_branch(root)
    for ref in cfg.required_refs:
        if ref_resolves(root, ref):
            continue
        if ref == checked_out:
            # Unreachable in practice (a checked-out branch resolves), and stated rather than
            # left implicit: fetching into the ref HEAD points at is refused by git.
            continue
        LOG.info("history: ref %r is absent - fetching it from origin", ref)
        r = _git(root, "fetch", "origin", f"+refs/heads/{ref}:refs/heads/{ref}", "--quiet")
        if r.returncode != 0:
            LOG.warning("history: could not fetch %r from origin: %s", ref, r.stderr.strip())
            continue
        report.actions.append(f"git fetch origin +refs/heads/{ref}:refs/heads/{ref}")

    final = assess_history(root, cfg)
    final.actions = report.actions
    return final


# --- ecosystem: the registration a fresh clone cannot inherit ------------------------------


def registered_repos(root: Path) -> list[str]:
    """Directories under `ecosystem/` carrying a state.yaml - `audit.discover_repos`'s predicate.

    Re-expressed against an arbitrary root rather than imported, because `audit.discover_repos`
    closes over the module-level `ECOSYSTEM_DIR` of the checkout it was imported from and this
    function must be able to answer for a container's tree in a test.
    """
    eco = root / "ecosystem"
    if not eco.exists():
        return []
    return sorted(d.name for d in eco.iterdir() if d.is_dir() and (d / "state.yaml").exists())


def seed_self_registration(root: Path, name: str) -> str:
    """Audit THIS repo and save the result as its state.yaml. Returns the path written.

    Writes exactly one gitignored file. Deliberately not `audit.py repo`, which additionally
    appends history, writes a dated report under `docs/audits/` and COMMITS its outputs — three
    things a provisioning step must never do to a container's tree.
    """
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import audit  # noqa: PLC0415  (import is deliberately lazy: heavy, and only this path needs it)
    except ImportError as exc:
        raise ProvisioningError(f"could not import scripts/audit.py: {exc}") from exc

    state = audit.audit_repo(name, root, date.today())
    audit.save_state(state)
    return str(root / "ecosystem" / name / "state.yaml")


# --- prebuild: declaration vs the one field the API exposes --------------------------------


def _gh_machines(repository: str) -> list[dict]:
    """`GET /repos/<repository>/codespaces/machines` via gh, or raise ProvisioningError."""
    if shutil.which("gh") is None:
        raise ProvisioningError("`gh` is not on PATH - cannot read the live prebuild state")
    try:
        r = subprocess.run(
            ["gh", "api", f"/repos/{repository}/codespaces/machines"],
            capture_output=True, text=True, timeout=_GH_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProvisioningError(f"`gh api` could not run: {exc}") from exc
    if r.returncode != 0:
        raise ProvisioningError(f"`gh api` failed: {r.stderr.strip() or r.stdout.strip()}")
    try:
        payload = json.loads(r.stdout)
    except json.JSONDecodeError as exc:
        raise ProvisioningError(f"`gh api` returned non-JSON: {exc}") from exc
    machines = payload.get("machines")
    if not isinstance(machines, list):
        raise ProvisioningError("`gh api` payload carries no `machines` list")
    return machines


def prebuild_live_configured(repository: str) -> bool:
    """True when ANY machine type reports a non-null `prebuild_availability`.

    This is the whole of what the public API exposes about prebuilds. The trigger, the region
    set and the template-history depth are NOT readable — they are operator UI state — so this
    answers "is a prebuild configured at all" and nothing finer. Stated here rather than left
    to be discovered by a reader who expects the checker to verify all three settings.
    """
    return any(m.get("prebuild_availability") is not None for m in _gh_machines(repository))


# --- commands ------------------------------------------------------------------------------


def cmd_history(args: argparse.Namespace) -> int:
    cfg = load_config(args.config).history
    root = args.root

    if cfg.disposition == "exclude":
        LOG.warning(
            "history: disposition is 'exclude' - the %d spine-walking instrument(s) below are "
            "declared OUT OF SCOPE for cloud lanes and this guard repairs nothing:",
            len(cfg.spine_walking_instruments))
        for instrument in cfg.spine_walking_instruments:
            LOG.warning("history:   excluded - %s", instrument)
        return EXIT_OK

    report = repair_history(root, cfg) if args.repair else assess_history(root, cfg)

    for action in report.actions:
        LOG.info("history: performed %s", action)
    if not report.actions and args.repair:
        LOG.info("history: no-op - the clone already satisfies every precondition")
    for ref, length in report.refs.items():
        if length is not None:
            LOG.info("history: %s walks %d first-parent spine entries", ref, length)
    for violation in report.violations:
        LOG.error("history: %s", violation)

    if report.ok:
        LOG.info("history: OK - full history, %d required ref(s) resolve, spine walks succeed",
                 len(cfg.required_refs))
        return EXIT_OK
    return EXIT_VIOLATION


def cmd_ecosystem(args: argparse.Namespace) -> int:
    cfg = load_config(args.config).ecosystem
    root = args.root

    repos = registered_repos(root)
    if repos:
        LOG.info("ecosystem: OK - %d repo(s) registered: %s", len(repos), ", ".join(repos))
        return EXIT_OK

    if not args.repair:
        LOG.error("ecosystem: no repo registered - `audit.py health` reports "
                  "`repos registered (none)` and exits non-zero here")
        return EXIT_VIOLATION

    if not cfg.self_register:
        LOG.error("ecosystem: no repo registered and ecosystem.self_register is false - "
                  "nothing this guard is permitted to do")
        return EXIT_VIOLATION

    LOG.info("ecosystem: nothing registered - auditing this repo as %r and saving its state",
             cfg.self_name)
    written = seed_self_registration(root, cfg.self_name)
    LOG.info("ecosystem: wrote %s (gitignored)", written)

    repos = registered_repos(root)
    if not repos:
        LOG.error("ecosystem: still nothing registered after seeding - the write did not land")
        return EXIT_VIOLATION
    LOG.info("ecosystem: OK - %d repo(s) registered: %s", len(repos), ", ".join(repos))
    return EXIT_OK


def cmd_prebuild(args: argparse.Namespace) -> int:
    cfg = load_config(args.config).prebuild
    if not cfg.repository:
        raise ProvisioningError("prebuild.repository is empty - nothing to query")

    LOG.info("prebuild: declared - trigger=%s regions=%s template_history=%d configured=%s",
             cfg.trigger, ",".join(cfg.regions), cfg.template_history, cfg.configured)
    live = prebuild_live_configured(cfg.repository)
    LOG.info("prebuild: live - a prebuild is %sconfigured for %s "
             "(read from `prebuild_availability`; the trigger, regions and template history "
             "are operator UI state with no public API and are NOT verifiable here)",
             "" if live else "NOT ", cfg.repository)

    if live == cfg.configured:
        LOG.info("prebuild: OK - the declaration agrees with the live state")
        return EXIT_OK
    LOG.error("prebuild: DRIFT - declaration says configured=%s, the API reports %s",
              cfg.configured, live)
    return EXIT_VIOLATION


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cloud_provisioning.py",
        description="[#554] cloud-lane provisioning guard - history sufficiency, ecosystem "
                    "registration, prebuild drift. Exit 0 clean / 1 violation / 2 could not look.")
    parser.add_argument("--root", type=Path, default=REPO_ROOT,
                        help="Repository root to act on (default: this checkout).")
    parser.add_argument("--config", type=Path, default=CONFIG_PATH,
                        help="Provisioning declaration (default: .devcontainer/provisioning.yaml).")
    parser.add_argument("--quiet", action="store_true", help="Log warnings and errors only.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_hist = sub.add_parser("history", help="B1 - assert (and optionally repair) the refs a "
                                            "spine-walking instrument needs.")
    p_hist.add_argument("--repair", action="store_true",
                        help="Deepen the clone and fetch missing refs, then re-assert.")
    p_hist.set_defaults(func=cmd_history)

    p_eco = sub.add_parser("ecosystem", help="L5 - assert (and optionally seed) the ecosystem "
                                             "registration `audit.py health` reads.")
    p_eco.add_argument("--repair", action="store_true",
                       help="Audit this repo and save its state.yaml when nothing is registered.")
    p_eco.set_defaults(func=cmd_ecosystem)

    p_pre = sub.add_parser("prebuild", help="A3 - report declaration-vs-live prebuild drift.")
    p_pre.set_defaults(func=cmd_prebuild)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="[cloud-provisioning] %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    try:
        return args.func(args)
    except ProvisioningError as exc:
        LOG.error("could not look: %s", exc)
        return EXIT_UNAVAILABLE
    except Exception as exc:                                  # noqa: BLE001 — an error BLOCKS
        LOG.exception("internal error: %s", exc)
        return EXIT_UNAVAILABLE


if __name__ == "__main__":
    raise SystemExit(main())
