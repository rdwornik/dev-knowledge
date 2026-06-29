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
class PrecommitTarget:
    config_path: str
    required_repos: tuple[RequiredRepo, ...]


def parse_target(target: Any) -> PrecommitTarget:
    """Interpret the opaque manifest entry into the carrier's typed model."""
    config_path = target.get("config_path", DEFAULT_CONFIG_NAME)
    repos: list[RequiredRepo] = []
    for r in target.get("required_repos", []) or []:
        hooks = tuple(dict(h) for h in r.get("hooks", []) or [])
        repos.append(RequiredRepo(repo=r["repo"], rev=str(r["rev"]), hooks=hooks))
    return PrecommitTarget(config_path=config_path, required_repos=tuple(repos))


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
