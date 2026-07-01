"""deploy/carrier_precommit.py — the pinned-pre-commit-hooks carrier (ADR-92 C1).

The reference carrier that proves the ADR-92 contract end-to-end on the cleanest
vector: pinned pre-commit hooks (ADR-71). Pure-file — no shell-out, no user-path —
and it closes the observed deploy gap: a prior deploy to ai-council left the
Tier-1 ruff lint gate (assets/ruff-pre-commit.yaml) unapplied.

A carrier instance is bound to one consumer repo (``repo_root``); the three
contract methods take the manifest ``target``. Target shape (the v1.0.0
manifest's ``precommit`` entry)::

    config_path: .pre-commit-config.yaml
    required_repos:
      - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.15.5
        hooks:
          - id: ruff
            name: ...
            args: []

- ``detect`` classifies the consumer's .pre-commit-config.yaml against
  ``required_repos`` into a CarrierState.
- ``apply`` merges each required repo-pin into the config (creating it if absent),
  preserving everything else and writing only on a real change (idempotent).
- ``verify`` independently re-confirms — via a separate fresh read + check that
  never routes through detect's classifier (ADR-92 Decision 9 / D9). ``_classify``
  (detect's judgment) and ``_verify_satisfied`` (verify's judgment) are distinct
  functions with no shared correctness-judgment helper; a bug in one cannot make
  the other falsely agree.
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

log = logging.getLogger(__name__)

CARRIER_ID = "precommit"
DEFAULT_CONFIG_NAME = ".pre-commit-config.yaml"


# ---------------------------------------------------------------------------
# Target model — interpret the opaque manifest entry into a typed shape.
# (Shared target-PARSING is fine under D9: it reads the spec, not the consumer's
# state. The forbidden sharing is the correctness judgment about the consumer.)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RequiredRepo:
    """One pre-commit repo-pin the target requires (parsed from the manifest)."""

    repo: str
    rev: str
    hooks: tuple[dict[str, Any], ...]  # full hook stanzas, written verbatim on apply

    @property
    def hook_ids(self) -> tuple[str, ...]:
        return tuple(h["id"] for h in self.hooks if isinstance(h, dict) and "id" in h)


@dataclass(frozen=True)
class HubHooksReq:
    """The hub-hooks rev-pin requirement — the version-coupling anchor.

    The consumer's `.dev-knowledge` hook-source entry pinned at ``rev`` = the
    methodology version tag (v1.0.0), so the pre-commit rev EQUALS
    ``deployed_methodology_version`` — a second visible version anchor.

    Identification is PATH-INDEPENDENT (the consumer's ``repo:`` path varies —
    local clone path vs URL): the entry is matched by hook-id intersection with
    ``marker_hook_ids`` (the hub's published ids, read live from
    .pre-commit-hooks.yaml), never by the ``repo:`` string. ``repo``/``hooks`` are
    used ONLY to CREATE an absent entry; an existing entry is bumped in place
    (its ``repo:`` path preserved).
    """

    rev: str
    marker_hook_ids: frozenset[str]
    repo: str  # canonical hub source, used only when creating an absent entry
    hooks: tuple[dict[str, Any], ...]  # hook stanzas written only on creation

    @property
    def hook_ids(self) -> tuple[str, ...]:
        return tuple(h["id"] for h in self.hooks if isinstance(h, dict) and "id" in h)


@dataclass(frozen=True)
class PrecommitTarget:
    config_path: str
    required_repos: tuple[RequiredRepo, ...]
    hub_hooks: HubHooksReq | None = None
    # Required hooks under a `- repo: local` block (no rev to pin — the consumer's
    # OWN hooks). This carrier is the single writer of .pre-commit-config.yaml, so it
    # owns the floor-hash-verify local hook (the floor carrier writes the SCRIPT the
    # hook runs; ADR-93 — arming spans two carriers, single-writer-per-file). Matched
    # by hook id inside the local block; no version axis, so a missing one is DRIFTED.
    required_local_hooks: tuple[dict[str, Any], ...] = ()


def parse_target(target: Any) -> PrecommitTarget:
    """Interpret the opaque manifest entry into the carrier's typed model."""
    config_path = target.get("config_path", DEFAULT_CONFIG_NAME)
    repos: list[RequiredRepo] = []
    for r in target.get("required_repos", []) or []:
        hooks = tuple(dict(h) for h in r.get("hooks", []) or [])
        repos.append(RequiredRepo(repo=r["repo"], rev=str(r["rev"]), hooks=hooks))
    hub_raw = target.get("hub_hooks")
    hub_hooks = None
    if hub_raw:
        hub_hooks = HubHooksReq(
            rev=str(hub_raw["rev"]),
            marker_hook_ids=frozenset(hub_raw.get("marker_hook_ids", []) or []),
            repo=hub_raw["repo"],
            hooks=tuple(dict(h) for h in hub_raw.get("hooks", []) or []),
        )
    local_hooks = tuple(dict(h) for h in target.get("required_local_hooks", []) or [])
    return PrecommitTarget(
        config_path=config_path,
        required_repos=tuple(repos),
        hub_hooks=hub_hooks,
        required_local_hooks=local_hooks,
    )


# ---------------------------------------------------------------------------
# detect path — _load_config + _find_repo + _classify.
# ---------------------------------------------------------------------------


def _load_config(path: Path) -> dict[str, Any]:
    """Read + parse the consumer's pre-commit config (empty dict if absent/blank)."""
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _find_repo(config: dict[str, Any], repo_url: str) -> dict[str, Any] | None:
    """Return the consumer repo entry matching ``repo_url`` (detect's helper)."""
    for entry in config.get("repos", []) or []:
        if isinstance(entry, dict) and entry.get("repo") == repo_url:
            return entry
    return None


def _find_local_entry(config: dict[str, Any]) -> dict[str, Any] | None:
    """Return the first `- repo: local` entry (detect/apply's helper), or None.

    The local block is the consumer's own hooks — the floor-hash-verify hook lands
    here. (verify does NOT use this; it re-scans independently — D9.)
    """
    for entry in config.get("repos", []) or []:
        if isinstance(entry, dict) and entry.get("repo") == "local":
            return entry
    return None


def _find_hub_entry(
    config: dict[str, Any], marker_hook_ids: frozenset[str]
) -> dict[str, Any] | None:
    """Find the consumer's hub-hooks entry PATH-INDEPENDENTLY (detect's helper).

    Matched by hook-id intersection with the hub's published ids, NOT by the
    ``repo:`` string (which is consumer-local). A ``repo: local`` entry is the
    consumer's OWN hooks (no rev to pin) and is skipped, so a consumer that
    mirrors the hub's local-hook pattern is not mistaken for the version-pinned
    hub source.
    """
    for entry in config.get("repos", []) or []:
        if not isinstance(entry, dict) or entry.get("repo") == "local":
            continue
        ids = {h.get("id") for h in entry.get("hooks", []) or [] if isinstance(h, dict)}
        if ids & marker_hook_ids:
            return entry
    return None


def _classify(config: dict[str, Any], target: PrecommitTarget) -> CarrierState:
    """detect's correctness judgment: consumer config -> CarrierState.

    Precedence (the Decision 6 reconcile model):
      - nothing required present                  -> ABSENT
      - a required repo or hook missing           -> PRESENT_DRIFTED
      - all present but some rev mismatched        -> PRESENT_WRONG_VERSION
      - all present, all hooks, all revs match     -> PRESENT_CORRECT
    """
    total = len(target.required_repos)
    present = 0
    missing_required = False  # a required repo entry absent, or a required hook missing
    wrong_version = False
    for req in target.required_repos:
        entry = _find_repo(config, req.repo)
        if entry is None:
            continue
        present += 1
        have_ids = {h.get("id") for h in entry.get("hooks", []) or [] if isinstance(h, dict)}
        if any(hid not in have_ids for hid in req.hook_ids):
            missing_required = True
        elif str(entry.get("rev")) != req.rev:
            wrong_version = True
    # Hub-hooks rev-pin (matched path-independently by hook-ids). Folds into the
    # same accounting: absent -> a missing requirement; present-but-wrong-rev ->
    # wrong_version (the rev-pin's real use).
    if target.hub_hooks is not None:
        total += 1
        hub_entry = _find_hub_entry(config, target.hub_hooks.marker_hook_ids)
        if hub_entry is not None:
            present += 1
            if str(hub_entry.get("rev")) != target.hub_hooks.rev:
                wrong_version = True
    # Required local hooks (no rev axis): present iff the id is in the local block;
    # a missing one is a missing requirement -> DRIFTED (via present < total).
    for lhook in target.required_local_hooks:
        total += 1
        local_entry = _find_local_entry(config)
        have_local = local_entry is not None and lhook.get("id") in {
            h.get("id") for h in local_entry.get("hooks", []) or [] if isinstance(h, dict)
        }
        if have_local:
            present += 1
    if present == 0:
        return CarrierState.ABSENT
    if missing_required or present < total:
        return CarrierState.PRESENT_DRIFTED
    if wrong_version:
        return CarrierState.PRESENT_WRONG_VERSION
    return CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# apply path — _reconcile + _dump_config.
# ---------------------------------------------------------------------------


def _reconcile(
    config: dict[str, Any] | None, target: PrecommitTarget
) -> tuple[dict[str, Any], list[str]]:
    """Return (desired config, list of change descriptions). Empty list => no-op.

    Reconcile, not overwrite: ensure each required repo entry exists at the target
    rev with the required hooks; preserve every other repo/hook/key the consumer
    has. Drives apply's idempotency — a config already at target yields no changes.
    """
    new = copy.deepcopy(config) if config else {}
    repos = new.get("repos")
    if not isinstance(repos, list):
        repos = []
        new["repos"] = repos
    changes: list[str] = []
    for req in target.required_repos:
        entry = _find_repo(new, req.repo)
        if entry is None:
            repos.append(
                {"repo": req.repo, "rev": req.rev, "hooks": [dict(h) for h in req.hooks]}
            )
            changes.append(f"added repo {req.repo}@{req.rev} with hooks {list(req.hook_ids)}")
            continue
        if str(entry.get("rev")) != req.rev:
            changes.append(f"pinned {req.repo} rev {entry.get('rev')!r} -> {req.rev!r}")
            entry["rev"] = req.rev
        entry_hooks = entry.get("hooks")
        if not isinstance(entry_hooks, list):
            entry_hooks = []
            entry["hooks"] = entry_hooks
        have_ids = {h.get("id") for h in entry_hooks if isinstance(h, dict)}
        for hook in req.hooks:
            if hook.get("id") not in have_ids:
                entry_hooks.append(dict(hook))
                changes.append(f"added hook {hook.get('id')} to {req.repo}")
    # Hub-hooks rev-pin: bump the identified entry IN PLACE (preserving its
    # consumer-local repo: path + hooks); create the canonical entry only when
    # absent.
    hub = target.hub_hooks
    if hub is not None:
        hub_entry = _find_hub_entry(new, hub.marker_hook_ids)
        if hub_entry is None:
            repos.append(
                {"repo": hub.repo, "rev": hub.rev, "hooks": [dict(h) for h in hub.hooks]}
            )
            changes.append(
                f"added hub-hooks repo {hub.repo}@{hub.rev} with hooks {list(hub.hook_ids)}"
            )
        elif str(hub_entry.get("rev")) != hub.rev:
            changes.append(
                f"pinned hub-hooks {hub_entry.get('repo')!r} rev "
                f"{hub_entry.get('rev')!r} -> {hub.rev!r}"
            )
            hub_entry["rev"] = hub.rev
    # Required local hooks: append each to the (created-if-absent) local block,
    # preserving any sibling local hooks the consumer already has.
    for lhook in target.required_local_hooks:
        local_entry = _find_local_entry(new)
        if local_entry is None:
            local_entry = {"repo": "local", "hooks": []}
            repos.append(local_entry)
            changes.append("added repo: local block")
        local_hooks = local_entry.get("hooks")
        if not isinstance(local_hooks, list):
            local_hooks = []
            local_entry["hooks"] = local_hooks
        have_ids = {h.get("id") for h in local_hooks if isinstance(h, dict)}
        if lhook.get("id") not in have_ids:
            local_hooks.append(dict(lhook))
            changes.append(f"added local hook {lhook.get('id')}")
    return new, changes


def _dump_config(path: Path, config: dict[str, Any]) -> None:
    """Write the config back as YAML (LF newlines, insertion order preserved)."""
    text = yaml.safe_dump(config, sort_keys=False, default_flow_style=False, width=4096)
    path.write_text(text, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its own fresh read + its own index +
# its own judgment (_verify_satisfied); shares no correctness-judgment helper
# with _classify/_find_repo.
# ---------------------------------------------------------------------------


def _verify_satisfied(raw_text: str, target: PrecommitTarget) -> list[str]:
    """verify's independent judgment: re-parse fresh, return unmet requirements.

    Built so a bug in detect's _classify path cannot be mirrored here: this builds
    its OWN repo->entry index (not via _find_repo) and asserts each required pin
    directly. Empty list => target satisfied.
    """
    failures: list[str] = []
    try:
        data = yaml.safe_load(raw_text) or {}
    except yaml.YAMLError as exc:
        return [f"config did not parse: {exc}"]
    repos = data.get("repos", []) if isinstance(data, dict) else []
    index = {e.get("repo"): e for e in repos if isinstance(e, dict)}
    for req in target.required_repos:
        entry = index.get(req.repo)
        if entry is None:
            failures.append(f"missing repo {req.repo}")
            continue
        if str(entry.get("rev")) != req.rev:
            failures.append(f"{req.repo} rev {entry.get('rev')!r} != target {req.rev!r}")
        present_ids = [
            h.get("id") for h in (entry.get("hooks") or []) if isinstance(h, dict)
        ]
        for hid in req.hook_ids:
            if hid not in present_ids:
                failures.append(f"{req.repo} missing hook {hid}")
    # Hub-hooks rev-pin — INDEPENDENT path-independent scan (own loop, NOT
    # _find_hub_entry), so a bug in detect's identifier cannot be mirrored here.
    hub = target.hub_hooks
    if hub is not None:
        hub_entry = None
        for e in repos:
            if not isinstance(e, dict) or e.get("repo") == "local":
                continue
            eids = {h.get("id") for h in (e.get("hooks") or []) if isinstance(h, dict)}
            if eids & hub.marker_hook_ids:
                hub_entry = e
                break
        if hub_entry is None:
            failures.append("missing hub-hooks entry (no pinned repo with hub hook-ids)")
        elif str(hub_entry.get("rev")) != hub.rev:
            failures.append(
                f"hub-hooks rev {hub_entry.get('rev')!r} != target {hub.rev!r}"
            )
    # Required local hooks — INDEPENDENT inline scan (own loop, NOT _find_local_entry),
    # so a bug in detect's local finder cannot be mirrored here (D9).
    for lhook in target.required_local_hooks:
        hid = lhook.get("id")
        found = any(
            isinstance(e, dict)
            and e.get("repo") == "local"
            and hid in {h.get("id") for h in (e.get("hooks") or []) if isinstance(h, dict)}
            for e in repos
        )
        if not found:
            failures.append(f"missing local hook {hid}")
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class PrecommitCarrier(Carrier):
    """Pinned pre-commit hooks carrier — bound to one consumer repo."""

    carrier_id = CARRIER_ID

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def _config_path(self, target: PrecommitTarget) -> Path:
        return self.repo_root / target.config_path

    def detect(self, target: Any) -> CarrierState:
        t = parse_target(target)
        config = _load_config(self._config_path(t))
        state = _classify(config, t)
        log.debug("precommit detect: %s -> %s", self._config_path(t), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        t = parse_target(target)
        path = self._config_path(t)
        config = _load_config(path) if path.exists() else None
        desired, changes = _reconcile(config, t)
        if not changes:
            return ApplyResult(changed=False, detail="already at target")
        _dump_config(path, desired)
        log.info("precommit apply: %s -> %d change(s)", path, len(changes))
        return ApplyResult(
            changed=True, changes=tuple(changes), detail=f"{len(changes)} change(s) written"
        )

    def verify(self, target: Any) -> VerifyResult:
        t = parse_target(target)
        path = self._config_path(t)
        # Independent read — does NOT call _load_config/_classify (D9).
        if not path.exists():
            return VerifyResult(
                ok=False, failures=(f"config absent: {path}",), detail="no config to verify"
            )
        failures = _verify_satisfied(path.read_text(encoding="utf-8"), t)
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail="target satisfied" if ok else f"{len(failures)} unmet requirement(s)",
        )
