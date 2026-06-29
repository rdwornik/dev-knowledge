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
