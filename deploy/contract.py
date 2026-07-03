"""deploy/contract.py — the methodology-deployment carrier contract (ADR-92).

The tiny interface every carrier implements: ``detect(target)`` /
``apply(target)`` / ``verify(target)``. A carrier reconciles ONE deployment
vector (pinned pre-commit hooks, the tier1-lifecycle plugin, the global L0
config, the per-repo floor) in a consumer repo toward a per-tag manifest target.

Deliberately tiny (ADR-92 Decision 8 — carriers are "hand-written against a tiny
interface, no plugin-loader, no DSL"): three operations and their result types.
There is **no orchestration here** — detect-then-conditionally-apply, ``--force``,
``--dry-run``, and the version-record write are the deploy *tool*'s job (a later
step, C2), never the contract's.

Three invariants the contract states and each carrier enforces structurally:

- **D9 — verify is independent of detect** (ADR-92 Decision 9). ``verify()`` MUST
  NOT share a code path with ``detect()``; they are independent implementations,
  so a bug in ``detect`` cannot make ``verify`` falsely pass. ``verify``'s
  ``ok`` is what gates the version-record write, so the registry reflects
  *verified reality, not intent*.
- **Layer-2 write boundary — write-yes / commit-no / autonomy-no** (ADR-92
  Decision 3, relaxed). ``apply(target)`` MAY write carrier bytes directly into
  the consumer's working tree (the ``generate_floor.py --out-dir`` precedent),
  but it does NOT commit in the sibling and is never autonomous (operator-invoked
  at a rollout moment only).
- **Structured output** (ADR-92 Decision 9). ``apply`` returns *what it changed*
  so the tool can render the per-carrier ``detected state | action | result |
  verification`` line and the operator reviews a real diff.

The ``target`` argument is the carrier's entry from the per-tag manifest (its
desired state). The contract passes it through opaquely; each carrier interprets
it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class CarrierState(Enum):
    """A carrier's detected state in a consumer repo, relative to its target.

    The four states are the reconcile model (ADR-92 Decision 6): detection must
    distinguish *absent* (nothing applied — apply from scratch), *drifted* (a
    required element is missing — the observed ai-council failure shape), *wrong
    version* (present and complete but pinned to the wrong rev), and *correct*
    (already at target — apply is a no-op). Skip-if-present and blind-overwrite
    were both rejected; only detect-and-reconcile both surfaces drift and
    converges it.
    """

    ABSENT = "absent"
    PRESENT_CORRECT = "present_correct"
    PRESENT_DRIFTED = "present_drifted"
    PRESENT_WRONG_VERSION = "present_wrong_version"

    @property
    def needs_apply(self) -> bool:
        """True for every state except already-correct (the tool reads this, C2)."""
        return self is not CarrierState.PRESENT_CORRECT


@dataclass(frozen=True)
class ApplyResult:
    """What ``apply()`` changed in the consumer tree — structured, for reporting.

    ``changed`` is False when the tree already matched the target (an idempotent
    re-apply writes nothing). ``changes`` enumerates each write/edit so the deploy
    tool can render the per-carrier ``action`` column and the operator reviews a
    real diff. ``apply`` writes/stages only — it never commits (Decision 3,
    commit-no).
    """

    changed: bool
    changes: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True)
class VerifyResult:
    """Independent confirmation that the applied state meets the target (D9).

    Produced by a code path orthogonal to ``detect()`` — a bug in detection
    cannot make verification pass. ``ok`` gates the version-record write
    (Decision 9); ``failures`` names each unmet requirement so a partial apply is
    reported, not silently recorded.
    """

    ok: bool
    failures: tuple[str, ...] = ()
    detail: str = ""


# ---------------------------------------------------------------------------
# The remove leg (P2 / [#244] / ADR-96). The add-only contract above converges
# a consumer TOWARD a target; the remove leg converges a ``status: removed``
# component toward ABSENT. Declarative config-management removal (Terraform
# destroy-on-remove / Ansible ``state: absent``) — NOT an API deprecation window.
# Opt-in per carrier (no-big-bang): only a carrier that owns a prunable component
# overrides the three methods; the base raises ``PruneUnsupported`` so an
# accidental prune of an unsupported carrier fails LOUD, never silently no-ops.
# ---------------------------------------------------------------------------


class PruneUnsupported(NotImplementedError):
    """A carrier was asked to prune a component it has no remove leg for.

    Prune is opt-in per carrier (the "no big-bang sweep" boundary): P2 lands the
    remove leg on exactly one carrier. The base ``Carrier`` methods raise this so
    an unsupported prune surfaces as a hard error, not a silent success.
    """


class PruneState(Enum):
    """A removed component's detected state in a consumer (the remove-leg model).

    Mirrors ``CarrierState`` but for absence-convergence rather than
    presence-convergence:

    - ``ALREADY_ABSENT`` — the artifact is gone; prune is a no-op (idempotent).
    - ``PRESENT_CLEAN`` — present and byte-matches the last-deployed shape → safe
      to remove.
    - ``PRESENT_MODIFIED`` — present but locally edited since deploy (hash/shape
      mismatch) → **REFUSE**; do not clobber the operator's local work. This is
      the copier deletion-propagation hash-guard: a template-deleted file the
      consumer locally modified is surfaced as a conflict, never silently deleted.
    """

    ALREADY_ABSENT = "already_absent"
    PRESENT_CLEAN = "present_clean"
    PRESENT_MODIFIED = "present_modified"

    @property
    def needs_prune(self) -> bool:
        """True only when present-and-clean (the sole state prune acts on)."""
        return self is PruneState.PRESENT_CLEAN


@dataclass(frozen=True)
class PruneResult:
    """What ``prune()`` removed (or refused) in the consumer tree — structured.

    ``pruned`` is False when nothing was removed (already absent, or the
    hash-guard refused). ``removed`` enumerates each deleted artifact/edit for the
    tool's per-component report; ``refused`` names each conflict that blocked
    removal (a locally-modified target). Like ``apply``, ``prune`` writes/stages
    only — it never commits (Decision 3, commit-no).
    """

    pruned: bool
    removed: tuple[str, ...] = ()
    refused: tuple[str, ...] = ()
    detail: str = ""


class Carrier(ABC):
    """One deployment vector's detect/apply/verify against a manifest target.

    A carrier instance is bound to a single consumer repo (the constructor takes
    the repo root); the three methods take ``target`` — the carrier's manifest
    entry (the desired state), interpreted by the carrier. ``carrier_id`` matches
    the manifest entry's ``id``. The contract is single-repo and stateless beyond
    the bound repo root — fleet behavior is a shell loop over invocations (ADR-92
    Decision 5), not the contract's concern.
    """

    #: Stable identifier matching this carrier's manifest entry ``id``.
    carrier_id: str

    @abstractmethod
    def detect(self, target: Any) -> CarrierState:
        """Classify the consumer's current state against ``target``. Read-only."""

    @abstractmethod
    def apply(self, target: Any) -> ApplyResult:
        """Reconcile the consumer toward ``target``. Writes/stages; never commits."""

    @abstractmethod
    def verify(self, target: Any) -> VerifyResult:
        """Independently confirm the target is met. MUST NOT route through ``detect()``."""

    # --- Remove leg (P2 / ADR-96) — opt-in per carrier. The base raises so an
    # unsupported prune fails loud; only the carrier owning a prunable component
    # overrides these three. ``component`` is the manifest ``components:`` entry
    # (its ``prune:`` block, if any, gives the identity + last-deployed oracle).
    # verify_pruned MUST be independent of detect_prune (D9), mirroring verify/detect.

    def detect_prune(self, component: Any) -> PruneState:
        """Classify a removed component's state in the consumer. Read-only."""
        raise PruneUnsupported(
            f"{getattr(self, 'carrier_id', '?')}: no remove leg for component "
            f"{component.get('id') if isinstance(component, dict) else component!r}"
        )

    def prune(self, component: Any) -> PruneResult:
        """Remove the component's artifacts; REFUSE on a locally-modified target.

        Writes/stages only — never commits (Decision 3). Idempotent: an
        already-absent component is a no-op.
        """
        raise PruneUnsupported(
            f"{getattr(self, 'carrier_id', '?')}: no remove leg for component "
            f"{component.get('id') if isinstance(component, dict) else component!r}"
        )

    def verify_pruned(self, component: Any) -> VerifyResult:
        """Independently confirm the component is ABSENT. MUST NOT route through ``detect_prune()``."""
        raise PruneUnsupported(
            f"{getattr(self, 'carrier_id', '?')}: no remove leg for component "
            f"{component.get('id') if isinstance(component, dict) else component!r}"
        )
