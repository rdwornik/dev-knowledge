"""Derived-copy registry contract — pydantic models for `ecosystem/derived-copies.yaml`.

Models ONLY: no file I/O, no network, no execution (Layer-2, ADR-28/36), matching the
convention `ecosystem/schema/provider_registry.py` already establishes for this directory.
The loader, the staged-path resolution and the verification subprocess all live in
`scripts/check_derived_copies.py`, which parses the YAML and hands the mapping here.

WHY PYDANTIC AND NOT A HAND-ROLLED SHAPE CHECK — the contract's library-first clause (C-11),
answered the same way the sibling registry answered it. `pydantic>=2` is already in the
curated baseline (`pyproject.toml`, ADR-109/[#382] W2) and `ecosystem/schema/` is already
the declared contract home, so the MEASURED divergence a hand-rolled checker would need to
justify itself does not exist here. `extra="forbid"` is the load-bearing half: without it a
misspelled `comit_gate:` is silently inert data — a registry row that looks armed, is read
by nothing, and reports green. That is the present-but-unread failure mode the registry
itself exists to catch, and it would be embarrassing to reproduce it in the registry's own
schema.

THE ONE CROSS-FIELD RULE, and why it is here rather than in the checker. A row declares
`commit_gate: gate` together with the hook id in `gate:`, or `commit_gate: self` together
with a `verify:` argv. Every other pairing is a spec error, not a runtime condition:

  * `commit_gate: gate` with no `gate:` names no hook, so nothing can be asserted about it —
    the row would claim protection it cannot point at.
  * `commit_gate: self` with no `verify:` declares that this registry is the only thing
    holding the copy current and then supplies no way to check it. That row is strictly
    worse than an absent one: it reads as covered.

Both are decidable from the data alone, so they refuse at load time on every consumer,
rather than at the moment some commit happens to rebind that particular copy.

WHAT THE SCHEMA DOES NOT DO, stated because it bounds a green load. It validates SHAPE. It
does not open a `target`, does not resolve a `sources` glob against the tree, and does not
check that a named `gate` exists in `.pre-commit-config.yaml` — that last one is a live-tree
assertion and belongs to the checker, which does it on every commit.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator, model_validator

SCHEMA_VERSION = "1.0.0"

#: How a rebound copy is verified. `command` runs `verify` as argv after the interpreter and
#: reads the exit code; `region` runs it to capture stdout and looks for that text inside the
#: target. Two kinds, because this repo's generators come in exactly those two shapes.
Kind = Literal["command", "region"]

#: Where the copy lives. `repo` is a tracked path; `l0` is the operator's `~/.claude/` disk,
#: which is ABSENT on CI, in a container and on a cloud lane — the distinction the
#: `on_target_absent` policy exists to serve.
TargetScope = Literal["repo", "l0"]

#: `gate` delegates the commit-time guarantee to a named pre-commit hook; `self` keeps it
#: here. There is no third value: a copy either has a commit-time guarantee somewhere or it
#: does not, and "somewhere" is a thing the registry can name.
CommitGate = Literal["gate", "self"]

#: What an absent target means. `warn` reports and passes (register ruling Z-G4: a gap that
#: is named is not a pass, but it is also not this commit's fault); `fail` refuses.
AbsencePolicy = Literal["warn", "fail"]


class _Contract(BaseModel):
    """Contract-native type: this repo owns the grammar, so an unknown key is a spec error."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class DerivedCopy(_Contract):
    """One derived copy: what it comes from, where it lands, and what refuses a stale one."""

    what: StrictStr
    sources: tuple[StrictStr, ...]
    target: StrictStr
    target_scope: TargetScope
    render: StrictStr
    kind: Kind
    verify: Optional[tuple[StrictStr, ...]] = None
    commit_gate: CommitGate
    gate: Optional[StrictStr] = None
    on_target_absent: AbsencePolicy = "fail"
    note: Optional[StrictStr] = None

    @field_validator("sources")
    @classmethod
    def _sources_non_empty(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        """A row with no sources can never be rebound, so nothing about it is ever checked."""
        if not v:
            raise ValueError("`sources` is empty, so this copy can never be rebound")
        return v

    @model_validator(mode="after")
    def _gate_and_verify_agree(self) -> "DerivedCopy":
        """The one cross-field rule — see the module docstring for why it lives here."""
        if self.commit_gate == "gate" and not self.gate:
            raise ValueError("`commit_gate: gate` names no hook in `gate:`")
        if self.commit_gate == "self":
            if self.gate:
                raise ValueError("`commit_gate: self` also names a `gate:` hook; pick one")
            if not self.verify:
                raise ValueError("`commit_gate: self` supplies no `verify:` argv")
        return self


class DerivedCopiesRegistry(_Contract):
    """The whole file: a schema version and the `copies:` mapping, keyed by id."""

    schema_version: StrictStr
    copies: dict[StrictStr, DerivedCopy]

    @field_validator("copies")
    @classmethod
    def _copies_non_empty(cls, v: dict[str, DerivedCopy]) -> dict[str, DerivedCopy]:
        """An empty registry passes every check while registering nothing. Refuse it."""
        if not v:
            raise ValueError("`copies` is empty; an empty registry reports green vacuously")
        return v

    @property
    def self_gated(self) -> dict[str, DerivedCopy]:
        """The rows this registry is itself the commit-time guarantee for."""
        return {k: c for k, c in self.copies.items() if c.commit_gate == "self"}

    @property
    def gate_ids(self) -> tuple[str, ...]:
        """Every distinct pre-commit hook id the registry delegates a guarantee to."""
        seen: list[str] = []
        for copy in self.copies.values():
            if copy.gate and copy.gate not in seen:
                seen.append(copy.gate)
        return tuple(seen)
