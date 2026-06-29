"""deploy/carrier_globalconfig.py — the global Codex-reviewer-config carrier (ADR-92 C3).

Reconciles the GLOBAL Codex reviewer config (ADR-54): the hub's canonical
``codex/AGENTS.md`` deployed to the user-level ``~/.codex/AGENTS.md``. Unlike every
other carrier this one is **user-machine scoped, not consumer-repo scoped** — its
target is a path under the operator's home, so the carrier's ``repo_root`` binding
(the consumer repo) is unused here; only the injectable user-config base matters.

Per ADR-54 the deploy mechanism is a straight COPY (the global config has no rev —
it is a verbatim file, not a versioned pin), so detection distinguishes only three
of the four contract states: ``ABSENT`` (missing), ``PRESENT_CORRECT`` (byte-identical
to the hub source) and ``PRESENT_DRIFTED`` (differs). There is no
``PRESENT_WRONG_VERSION`` — not every carrier exercises all four states (the contract
allows this; the rev-bearing example is the pre-commit hub-hooks pin).

Target shape (the v1.0.0 manifest's ``global-config`` entry)::

    source_path: codex/AGENTS.md     # hub canonical source, relative to the hub root
    target_filename: AGENTS.md       # written to <user-config-base>/AGENTS.md (~/.codex/)

- ``detect`` compares ``~/.codex/AGENTS.md`` against the hub source -> CarrierState.
- ``apply`` copies the hub source to ``~/.codex/AGENTS.md`` (creating ``~/.codex/`` if
  absent — a user dir, not a repo folder); idempotent (byte-identical -> changed=False).
- ``verify`` independently re-reads + re-compares via its OWN code path that never
  routes through detect's classifier (ADR-92 Decision 9 / D9). ``_classify_global``
  (detect's judgment) and ``_verify_global`` (verify's judgment) are distinct
  functions sharing no correctness-judgment helper; reading the hub *source* bytes is
  a shared SPEC read (D9-permitted, like target-parsing), not a shared judgment.

Test safety: the user-config base is injectable (constructor param ``user_config_base``,
then the ``CODEX_HOME`` env var, then the default ``~/.codex``) so tests point it at a
temp dir and **the real ``~/.codex/`` is never touched**.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

log = logging.getLogger(__name__)

CARRIER_ID = "global-config"

# The hub root (this module lives in deploy/, so the hub is its parent's parent),
# used to resolve the manifest's repo-relative `source_path`.
_HUB_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_SOURCE_REL = "codex/AGENTS.md"  # hub canonical source (ADR-54)
DEFAULT_TARGET_NAME = "AGENTS.md"       # written under the user-config base (~/.codex/)
DEFAULT_USER_BASE = Path.home() / ".codex"


# ---------------------------------------------------------------------------
# Spec read — the hub source bytes. SHARED between detect/verify is D9-fine: this
# reads the SPEC (what the consumer should match), not the consumer's own state.
# A verbatim byte copy keeps "deploy by copying" (ADR-54) faithful and sidesteps
# any newline-translation ambiguity.
# ---------------------------------------------------------------------------


def _read_source(source_path: Path) -> bytes:
    """Read the hub canonical source bytes (the spec)."""
    return source_path.read_bytes()


def _resolve_user_base(override: Path | str | None) -> Path:
    """Resolve the user-config base: param > CODEX_HOME env > ~/.codex.

    The injection point that keeps tests off the real ~/.codex/: a test passes a
    temp dir as ``override``. ``CODEX_HOME`` mirrors Codex's own home-relocation
    env so real operator usage stays honest too.
    """
    if override is not None:
        return Path(override)
    env = os.environ.get("CODEX_HOME")
    if env:
        return Path(env)
    return DEFAULT_USER_BASE


# ---------------------------------------------------------------------------
# detect path — _classify_global (detect's correctness judgment).
# ---------------------------------------------------------------------------


def _classify_global(source: bytes, target_path: Path) -> CarrierState:
    """detect's judgment: user-config file vs hub source -> CarrierState.

    Three states only (a copied file has no rev): absent -> ABSENT, byte-identical
    -> PRESENT_CORRECT, differs -> PRESENT_DRIFTED.
    """
    if not target_path.exists():
        return CarrierState.ABSENT
    if target_path.read_bytes() == source:
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN fresh read + its OWN compare;
# shares no correctness-judgment helper with _classify_global.
# ---------------------------------------------------------------------------


def _verify_global(source: bytes, target_path: Path) -> list[str]:
    """verify's independent judgment: re-read fresh, return unmet requirements.

    Built so a bug in detect's _classify_global cannot be mirrored here: it does its
    OWN existence check + byte compare and asserts identity directly. Empty list =>
    target satisfied.
    """
    failures: list[str] = []
    if not target_path.exists():
        failures.append(f"global config absent: {target_path}")
        return failures
    current = target_path.read_bytes()
    if current != source:
        failures.append(
            f"{target_path} differs from hub source "
            f"({len(current)}B on disk vs {len(source)}B source)"
        )
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class GlobalConfigCarrier(Carrier):
    """Global Codex reviewer config carrier — USER-machine scoped (not the consumer).

    ``repo_root`` is accepted for a uniform carrier constructor but is UNUSED: the
    target is ``<user_config_base>/AGENTS.md``, not a path in the consumer repo.
    """

    carrier_id = CARRIER_ID

    def __init__(
        self, repo_root: Path | str, user_config_base: Path | str | None = None
    ) -> None:
        self.repo_root = Path(repo_root)  # consumer root; UNUSED — this carrier is user-scoped
        self.user_config_base = _resolve_user_base(user_config_base)

    def _source_path(self, target: Any) -> Path:
        rel = (target or {}).get("source_path", DEFAULT_SOURCE_REL)
        return _HUB_ROOT / rel

    def _target_path(self, target: Any) -> Path:
        name = (target or {}).get("target_filename", DEFAULT_TARGET_NAME)
        return self.user_config_base / name

    def detect(self, target: Any) -> CarrierState:
        source = _read_source(self._source_path(target))
        state = _classify_global(source, self._target_path(target))
        log.debug("global-config detect: %s -> %s", self._target_path(target), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        source = _read_source(self._source_path(target))
        tpath = self._target_path(target)
        existed = tpath.exists()
        if existed and tpath.read_bytes() == source:
            return ApplyResult(changed=False, detail="already at hub source")
        tpath.parent.mkdir(parents=True, exist_ok=True)  # ~/.codex/ — a user dir
        tpath.write_bytes(source)
        action = "updated" if existed else "created"
        log.info("global-config apply: %s %s from hub source", action, tpath)
        return ApplyResult(
            changed=True,
            changes=(f"{action} {tpath} from {self._source_path(target)}",),
            detail=f"{action} from hub source",
        )

    def verify(self, target: Any) -> VerifyResult:
        # Independent read + compare — does NOT call _classify_global (D9).
        source = _read_source(self._source_path(target))
        failures = _verify_global(source, self._target_path(target))
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail="matches hub source" if ok else f"{len(failures)} mismatch",
        )
