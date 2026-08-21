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
    ref: str = "main"


@dataclass(frozen=True)
class Config:
    history: HistoryConfig
    ecosystem: EcosystemConfig
    prebuild: PrebuildConfig


def _strict_bool(block: dict, key: str, *, default: bool) -> bool:
    """A YAML value that must BE a boolean, not merely coerce to one.

    `bool("false")` is `True`, so a declaration written `configured: "false"` — quoted by hand,
    or by a generator that stringifies — silently flipped to the opposite meaning. Here that
    authorises ecosystem mutation or inverts a prebuild verdict, which is worse than refusing to
    read the file (terra HIGH round 4, 2026-08-21). A missing key still takes the default; a
    present key of the wrong type is a could-not-look.
    """
    if key not in block:
        return default
    value = block[key]
    if isinstance(value, bool):
        return value
    raise ProvisioningError(
        f"{key!r} is {value!r} ({type(value).__name__}), which is not a YAML boolean - write "
        f"`{key}: true` or `{key}: false`, unquoted")


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
            self_register=_strict_bool(eco, "self_register", default=False),
            self_name=str(eco.get("self_name") or ".dev-knowledge"),
        ),
        prebuild=PrebuildConfig(
            configured=_strict_bool(pre, "configured", default=False),
            trigger=str(pre.get("trigger") or ""),
            regions=tuple(pre.get("regions") or ()),
            template_history=int(pre.get("template_history") or 0),
            repository=str(pre.get("repository") or ""),
            ref=str(pre.get("ref") or "main"),
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
    """True when `refs/heads/<ref>` names a commit in THIS clone.

    Resolution is pinned to the `refs/heads/` NAMESPACE, not to the bare name. A bare
    `git rev-parse main` also resolves a TAG called `main`, a remote-tracking ref, or anything
    else git's disambiguation rules reach — and every instrument in
    `history.spine_walking_instruments` means the local BRANCH. Accepting a look-alike here
    would let a spine walk run over unrelated history and report clean, which is the vacuous-gate
    class this whole module exists to close (terra HIGH, 2026-08-21).
    """
    return _git(root, "rev-parse", "--verify", "--quiet",
                f"refs/heads/{ref}^{{commit}}").returncode == 0


def remote_ref(root: Path, ref: str, remote: str = "origin") -> str | None:
    """The SHA of the CACHED `refs/remotes/<remote>/<ref>`, or None when this clone has none.

    Cached, and therefore only as fresh as the last fetch. `live_remote_sha` is what the
    currency check uses; this remains for callers that genuinely want the local cache.
    """
    r = _git(root, "rev-parse", "--verify", "--quiet",
             f"refs/remotes/{remote}/{ref}^{{commit}}")
    return r.stdout.strip() if r.returncode == 0 else None


def live_remote_sha(root: Path, ref: str, remote: str = "origin") -> str | None:
    """The tip of `refs/heads/<ref>` ON THE REMOTE, asked of the remote. None if it has no such
    branch; raises on a transport failure.

    THE CURRENCY CHECK MUST NOT READ A CACHE (terra HIGH round 4, 2026-08-21). Comparing a local
    branch with `refs/remotes/origin/<ref>` compares two things that went stale together: a clone
    that has not fetched since upstream advanced finds them equal, reports clean, and the spine
    walkers then miss every commit added since. `ls-remote` is read-only and answers about the
    remote as it is now, which is the only reading that can support a currency claim.
    """
    r = _git(root, "ls-remote", "--exit-code", "--heads", remote, f"refs/heads/{ref}")
    if r.returncode == 0:
        first = r.stdout.split(maxsplit=1)
        if not first:
            raise ProvisioningError(
                f"`git ls-remote {remote} refs/heads/{ref}` succeeded with no output")
        return first[0]
    if r.returncode == 2:
        return None
    raise ProvisioningError(
        f"`git ls-remote {remote} refs/heads/{ref}` failed (exit {r.returncode}): "
        f"{r.stderr.strip()} - cannot tell whether the branch exists or the remote is "
        f"unreachable")


#: Local-vs-remote states for a required ref. The four are kept apart because they get three
#: DIFFERENT treatments, and collapsing them is how a repair becomes data loss.
REF_CURRENT = "current"     # equal, or local ahead — nothing missing from the spine walk
REF_BEHIND = "behind"       # local is an ANCESTOR of remote: fast-forwardable, safe to update
REF_DIVERGED = "diverged"   # neither is an ancestor: updating would DISCARD local commits
#: The remote tip is not an object in this clone at all — which happens precisely when the clone
#: has never fetched it. Not current (the walk is provably missing that commit), and not
#: classifiable further without fetching, so it is never treated as fast-forwardable.
REF_TIP_ABSENT = "tip-absent"


def object_exists(root: Path, sha: str) -> bool:
    return _git(root, "cat-file", "-e", f"{sha}^{{commit}}").returncode == 0


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    r = _git(root, "merge-base", "--is-ancestor", ancestor, descendant)
    if r.returncode in (0, 1):
        return r.returncode == 0
    raise ProvisioningError(
        f"git merge-base --is-ancestor could not answer ({ancestor} -> {descendant}): "
        f"{r.stderr.strip()}")


def ref_status(root: Path, ref: str, remote_sha: str) -> str:
    """Classify the local branch against its remote-tracking ref.

    THE DISTINCTION IS LOAD-BEARING (terra CRITICAL, 2026-08-21). An earlier version asked only
    "is the remote an ancestor of local?" and treated every `no` as behind — which lumps a
    DIVERGED branch in with a fast-forwardable one. The repair then force-fetched over it, so a
    VPS clone carrying an unpushed commit on local `main` would have lost the only reference to
    it the moment `origin/main` also advanced. Divergence is now refused, never overwritten.

    Being AHEAD is normal on a workstation (a lane's own commits) and reads as current: nothing
    is missing from the walk.
    """
    local = f"refs/heads/{ref}"
    if not object_exists(root, remote_sha):
        # The remote tip has never been fetched, so no ancestry question can be answered here.
        # What IS known: the local branch cannot contain a commit this clone does not have.
        return REF_TIP_ABSENT
    if _is_ancestor(root, remote_sha, local):
        return REF_CURRENT
    if _is_ancestor(root, local, remote_sha):
        return REF_BEHIND
    return REF_DIVERGED


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


def remote_has_branch(root: Path, ref: str, remote: str = "origin") -> bool:
    """Whether `remote` carries `refs/heads/<ref>`, asked of the REMOTE itself.

    Three-valued underneath: the branch exists, it verifiably does not, or the remote could not
    be reached (which raises). Before this, ANY failed fetch was reported as "origin has no such
    branch" — so an auth failure, a DNS failure or an unreachable host all became a
    positively-observed configuration violation (exit 1) when the honest answer was
    could-not-look (exit 2). Terra HIGH round 3, 2026-08-21.
    """
    return live_remote_sha(root, ref, remote) is not None


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
    #: Refs present and walkable whose currency could NOT be checked (no remote-tracking ref).
    #: Surfaced rather than folded into `ok`: not-compared is not the same fact as compared-clean.
    uncompared: list[str] = field(default_factory=list)

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
            continue
        if length == 0:
            report.violations.append(
                f"ref {ref!r} walks to an EMPTY first-parent spine - the instruments would "
                f"pass on nothing, which is the vacuous-gate failure shape leg 2 exists to close")
            continue
        # Present, walkable — and possibly STALE. A local branch left behind the remote hides
        # every spine entry in between, so the instruments run over a short history and report
        # clean. The comparison is against the LIVE remote (`ls-remote`, read-only), never the
        # cached remote-tracking ref: a clone that has not fetched has a cache that went stale
        # alongside its branch, and comparing the two finds them equal (terra HIGH round 4).
        remote_sha = live_remote_sha(root, ref) if has_remote(root) else None
        if remote_sha is None:
            report.uncompared.append(ref)
            continue
        status = ref_status(root, ref, remote_sha)
        if status in (REF_BEHIND, REF_TIP_ABSENT):
            report.violations.append(
                f"ref {ref!r} is BEHIND origin/{ref} ({remote_sha[:9]}) - the spine walk would "
                f"miss every entry in between and still report clean")
        elif status == REF_DIVERGED:
            report.violations.append(
                f"ref {ref!r} has DIVERGED from origin/{ref} ({remote_sha[:9]}) - it carries "
                f"commits the remote does not. This guard REFUSES to repair it: a forced update "
                f"would discard them. Resolve the divergence by hand.")
    return report


def repair_history(root: Path, cfg: HistoryConfig) -> HistoryReport:
    """Deepen the clone and restore the required refs, then re-assess.

    Gated throughout: `--unshallow` is an error on a complete clone, and fetching a ref that is
    already checked out is an error too, so each action runs only when its precondition holds.
    Idempotent — a second run performs no action and says so.
    """
    # An environment this guard cannot ACT in is a could-not-look, not a violation: the 0/1/2
    # contract says so, and returning 1 here would tell a caller "the clone is wrong" when the
    # honest answer is "there is nothing here to repair it from" (terra HIGH, 2026-08-21).
    if not has_remote(root):
        report = assess_history(root, cfg)
        if report.ok and not report.uncompared:
            return report
        raise ProvisioningError(
            "no `origin` remote - a clone missing history cannot be repaired here")

    # Keep the remote-tracking refs usable for the LANE (a `git log origin/main` in the container
    # should not lie). Explicitly NOT load-bearing for anything this guard decides: the currency
    # check reads `ls-remote`, so a failure here cannot make a stale clone look current. Its
    # return code is therefore ignored on purpose, and it is not recorded in `actions` — it is a
    # convenience refresh, and counting it would make every run look like it changed something.
    for ref in cfg.required_refs:
        _git(root, "fetch", "origin", f"+refs/heads/{ref}:refs/remotes/origin/{ref}", "--quiet")

    report = assess_history(root, cfg)
    if report.ok and not report.uncompared:
        return report

    if report.shallow:
        LOG.info("history: clone is shallow - fetching full history (git fetch --unshallow)")
        r = _git(root, "fetch", "--unshallow", "--quiet")
        if r.returncode != 0:
            raise ProvisioningError(f"`git fetch --unshallow` failed: {r.stderr.strip()}")
        report.actions.append("git fetch --unshallow")

    # Violations only the REPAIR ATTEMPT can learn, kept apart from `report.violations` — those
    # describe the clone BEFORE acting and are re-derived by the final assessment.
    repair_notes: list[str] = []
    checked_out = current_branch(root)

    for ref in cfg.required_refs:
        if ref == checked_out:
            # A checked-out branch always resolves, and git refuses a fetch into the ref HEAD
            # points at. Stated rather than left implicit.
            continue
        remote_sha = live_remote_sha(root, ref)
        present = ref_resolves(root, ref)
        if present and remote_sha is not None:
            status = ref_status(root, ref, remote_sha)
            if status == REF_CURRENT:
                continue
            if status == REF_TIP_ABSENT:
                # The convenience refresh above should have brought the tip in. If it did not,
                # the clone still cannot be classified, and forcing an update on an unclassified
                # ref is exactly the divergence hazard the CRITICAL fix closed — so refuse.
                LOG.error("history: ref %r cannot be classified against origin/%s - the remote "
                          "tip is not present locally even after a refresh; refusing to force it",
                          ref, ref)
                continue
            if status == REF_DIVERGED:
                # REFUSE, do not repair. assess_history below reports it as a violation.
                LOG.error("history: ref %r has DIVERGED from origin/%s - refusing to force-update "
                          "it, because that would discard local commits", ref, ref)
                continue
        elif present:
            continue                      # present, and nothing to compare against — leave it
        if not present and not remote_has_branch(root, ref):
            # ASKED OF THE REMOTE, not inferred from a failed fetch. `ls-remote --exit-code`
            # separates "the branch verifiably does not exist" (a real violation) from a
            # transport failure (which raises inside `remote_has_branch` and exits 2).
            repair_notes.append(
                f"required ref {ref!r} is absent locally and origin has no branch of that name "
                f"- the declaration names a ref no reachable clone carries")
            continue
        LOG.info("history: ref %r is %s - fetching it from origin", ref,
                 "absent" if not present else "behind origin")
        # `+` forces the update, which is what makes this repair a STALE-ref fix and not only a
        # missing-ref fix. Safe here by construction: the ref is not the checked-out branch.
        r = _git(root, "fetch", "origin", f"+refs/heads/{ref}:refs/heads/{ref}", "--quiet")
        if r.returncode == 0:
            report.actions.append(f"git fetch origin +refs/heads/{ref}:refs/heads/{ref}")
            continue
        # Reaching here means `ls-remote` said the branch EXISTS and the fetch still failed, so
        # this is an action the guard could not perform — never a statement about the branch.
        raise ProvisioningError(
            f"`git fetch origin +refs/heads/{ref}:refs/heads/{ref}` failed even though origin "
            f"reports the branch exists: {r.stderr.strip()}")

    final = assess_history(root, cfg)
    final.actions = report.actions
    # Carry forward what only the REPAIR attempt could learn (e.g. "origin has no such branch").
    # A re-assessment sees the ref is missing; it cannot see that fetching it was tried and why
    # it failed, and dropping that would make the report less true after acting than before.
    final.violations.extend(n for n in repair_notes if n not in final.violations)
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


def _gh_machines(repository: str, ref: str, location: str) -> list[dict]:
    """`GET /repos/<repository>/codespaces/machines` via gh, or raise ProvisioningError.

    `ref` and `location` are sent because the endpoint's `prebuild_availability` is answered
    IN THEIR CONTEXT — it reports whether a prebuild is available for that branch in that
    region, not whether a configuration exists. Omitting them (the first version of this
    function did) asks a different question from the one the caller means.
    """
    if shutil.which("gh") is None:
        raise ProvisioningError("`gh` is not on PATH - cannot read the live prebuild state")
    try:
        r = subprocess.run(
            ["gh", "api",
             f"/repos/{repository}/codespaces/machines?ref={ref}&location={location}"],
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


#: What a `prebuild_availability` reading lets the caller conclude. Three states, because the
#: API's own enum has three meanings and collapsing them produces wrong verdicts in two
#: quadrants at once (terra HIGH round 3, 2026-08-21).
PREBUILD_CONFIRMED = "confirmed"    # `ready` / `in_progress` — a configuration demonstrably exists
PREBUILD_NONE = "none"              # every machine says `none` — no prebuild for this ref/region
PREBUILD_UNKNOWN = "unknown"        # `null` or an unrecognised value — could not determine

#: GitHub's documented values. `none` means UNAVAILABLE and is emphatically not "no answer";
#: reading it as truthy (which "any non-null value" does) turns the clearest possible negative
#: into a false positive.
_PREBUILD_CONFIRMING = frozenset({"ready", "in_progress"})
_PREBUILD_NEGATIVE = frozenset({"none"})


def prebuild_state(repository: str, ref: str, location: str) -> str:
    """Classify `prebuild_availability` across the machine types for `ref` in `location`.

    THIS IS AN AVAILABILITY READING, NOT A CONFIGURATION READING, and the distinction decides
    what the caller may conclude. GitHub answers this endpoint for a given branch and region:
    `ready`/`in_progress` prove a prebuild exists there, so a configuration exists; `none` proves
    only that nothing is available for that branch and region, which a configuration whose
    prebuild has not run or has expired also produces; `null` (and anything unrecognised) is not
    an answer at all.

    The trigger, the region set and the template-history depth are not readable by any API: they
    are operator UI state.
    """
    values = [m.get("prebuild_availability")
              for m in _gh_machines(repository, ref, location)]
    if any(v in _PREBUILD_CONFIRMING for v in values):
        return PREBUILD_CONFIRMED
    if values and all(v in _PREBUILD_NEGATIVE for v in values):
        return PREBUILD_NONE
    return PREBUILD_UNKNOWN


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

    if not report.ok:
        return EXIT_VIOLATION
    if report.uncompared:
        # Present and walkable, but its CURRENCY could not be checked — a stale local branch
        # would look exactly like this. Exit 2, not 0: reporting "clean" from a reading that
        # cannot support it is the false-resolve the 1/2 split exists to prevent (terra HIGH
        # round 2, 2026-08-21).
        for ref in report.uncompared:
            LOG.warning("history: %s has no origin/%s to compare against - its currency is "
                        "UNCHECKED, not confirmed", ref, ref)
        return EXIT_UNAVAILABLE
    LOG.info("history: OK - full history, %d required ref(s) resolve and are current with "
             "origin, spine walks succeed", len(cfg.required_refs))
    return EXIT_OK


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
    """Report the prebuild declaration against the ONE thing the API can answer.

    The three-way outcome is deliberate and follows from what the endpoint means:

      declared configured  + CONFIRMED -> EXIT_OK. Corroborated (the trigger/region/history
        settings remain unverifiable, and the log says so).
      declared configured  + NONE      -> EXIT_VIOLATION. Positively observed drift: a prebuild
        is claimed and the branch/region it is claimed for reports `none`.
      declared NOT config. + CONFIRMED -> EXIT_VIOLATION. Also positively observed: a `ready` or
        `in_progress` prebuild PROVES a configuration exists, so denying one is drift.
      declared NOT config. + NONE      -> EXIT_UNAVAILABLE. `none` means nothing is available
        here; it is not evidence that no CONFIGURATION exists (an unrun or expired prebuild
        reads the same). Exiting 0 would report a verification the reading cannot support.
      anything             + UNKNOWN   -> EXIT_UNAVAILABLE. `null` is not an answer.
    """
    cfg = load_config(args.config).prebuild
    if not cfg.repository:
        raise ProvisioningError("prebuild.repository is empty - nothing to query")
    if not cfg.regions:
        raise ProvisioningError("prebuild.regions is empty - the availability query needs one")

    ref = cfg.ref or "main"
    location = cfg.regions[0]
    LOG.info("prebuild: declared - trigger=%s regions=%s template_history=%d configured=%s",
             cfg.trigger, ",".join(cfg.regions), cfg.template_history, cfg.configured)
    LOG.info("prebuild: NOT verifiable by any API - trigger, region set and template history are "
             "operator UI state (probed 2026-08-21: REST 404, GraphQL introspection empty, no "
             "`gh codespace` subcommand). Only availability is readable.")

    state = prebuild_state(cfg.repository, ref, location)
    LOG.info("prebuild: live - prebuild_availability for %s @ %s in %s reads %s",
             cfg.repository, ref, location, state.upper())

    if state == PREBUILD_UNKNOWN:
        LOG.warning("prebuild: INDETERMINATE - the API returned `null` (or a value this tool does "
                    "not recognise), which is not an answer either way.")
        return EXIT_UNAVAILABLE
    # A CONFIRMED reading is positive evidence in both directions and never leaves a question.
    if state == PREBUILD_CONFIRMED:
        if cfg.configured:
            LOG.info("prebuild: OK - a prebuild exists for the declared branch and region")
            return EXIT_OK
        LOG.error("prebuild: DRIFT - the declaration says NO prebuild is configured, but one is "
                  "ready or building for %s @ %s in %s, which proves a configuration exists",
                  cfg.repository, ref, location)
        return EXIT_VIOLATION
    if cfg.configured:
        LOG.error("prebuild: DRIFT - the declaration says a prebuild is configured, but every "
                  "machine type reports `none` for %s @ %s in %s",
                  cfg.repository, ref, location)
        return EXIT_VIOLATION
    LOG.warning("prebuild: INDETERMINATE - the declaration says no prebuild is configured, and a "
                "`none` availability cannot confirm that (an unrun or expired prebuild reads the "
                "same). Configuration state is verifiable only in the GitHub UI.")
    return EXIT_UNAVAILABLE


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
