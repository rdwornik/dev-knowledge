"""Lived-workflow sandbox — the ENGAGES ORACLE (Slice B; [#252]).

The essence-spec (``deploy/manifest-vX.Y.Z.yaml``) is the SINGLE pass/fail source (C2):
each active component carries an ``engages: {trigger, observable, expect}`` triple. This
module reads them into typed ``Expectation``s so the observer NEVER hand-codes an
expectation — it reads the oracle and checks the named channel for the named signature.

Partitioning (the observer's gate vs report split, per the [#252] operator ruling):

- **GATED** — ``observable == hook-stdout`` AND an arc-stage ``trigger``: the deployed-mesh
  firing hooks the lived arc gates. Split into ``gated_active`` (the six methodology hooks
  that MUST fire) and ``gated_absent`` (a tombstone whose signature must NOT appear —
  prune-conformance).
- **OBSERVED-not-gated** — everything else (``git-state`` / ``transcript-event`` channels,
  or a non-arc ``operator-invoke`` / ``deploy-time`` trigger): present in the oracle,
  watched + reported, never pass/fail.

Reads only the spec — never inner narration.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

# The arc lifecycle stages (branch->edit->commit->wrap). A hook-stdout expectation on one
# of these is a firing hook the lived arc gates; the two non-arc triggers (operator-invoke,
# deploy-time) are present in the oracle but classified OUT-OF-ARC (never gated).
ARC_STAGES = frozenset(
    {"session-start", "edit", "pre-commit", "commit-msg", "pre-push", "stop"}
)


class OracleError(ValueError):
    """The manifest's engages: data is missing or malformed (release_lint C8 is the gate;
    this is a defensive parse error for the observer's own loader)."""


@dataclass(frozen=True)
class Expectation:
    """One component's lived-workflow engagement expectation, parsed from ``engages:``."""

    component_id: str
    kind: str
    status: str          # active | removed
    trigger: str
    observable: str      # hook-stdout | git-state | transcript-event
    signature: str       # the token the observer searches the channel for
    absent: bool         # tombstone: the signature must NOT appear (prune-conformance)

    @property
    def is_arc_stage(self) -> bool:
        return self.trigger in ARC_STAGES

    @property
    def is_firing_hook(self) -> bool:
        """A hook whose enforcement evidence is its stdout (the gated channel)."""
        return self.observable == "hook-stdout"

    @property
    def is_gated(self) -> bool:
        """A firing hook on an arc stage — the deployed mesh the arc exercises. True for
        the six active methodology hooks AND the ruff tombstone (gated as expect-absent)."""
        return self.is_firing_hook and self.is_arc_stage


def _parse_expect(cid: str, expect: object) -> tuple[str, bool]:
    """(signature, absent). String -> (expect, False); {absent: true, signature} -> (sig, True)."""
    if isinstance(expect, str):
        if not expect.strip():
            raise OracleError(f"{cid}: engages.expect is an empty string")
        return expect, False
    if isinstance(expect, dict):
        sig = expect.get("signature")
        if not isinstance(sig, str) or not sig.strip():
            raise OracleError(f"{cid}: engages.expect.signature must be a non-empty string")
        return sig, expect.get("absent") is True
    raise OracleError(f"{cid}: engages.expect must be a string or {{absent, signature}}")


def _parse_expectation(comp: dict) -> Expectation | None:
    """One component dict -> Expectation, or None when it carries no engages:."""
    eng = comp.get("engages")
    if eng is None:
        return None
    if not isinstance(eng, dict):
        raise OracleError(f"{comp.get('id')!r}: engages must be a mapping")
    cid = str(comp.get("id", "?"))
    signature, absent = _parse_expect(cid, eng.get("expect"))
    return Expectation(
        component_id=cid,
        kind=str(comp.get("kind", "")),
        status=str(comp.get("status", "")),
        trigger=str(eng.get("trigger", "")),
        observable=str(eng.get("observable", "")),
        signature=signature,
        absent=absent,
    )


@dataclass(frozen=True)
class Oracle:
    """The full set of engagement expectations for one methodology release."""

    version: str
    expectations: tuple[Expectation, ...]

    @property
    def gated(self) -> tuple[Expectation, ...]:
        return tuple(e for e in self.expectations if e.is_gated)

    @property
    def gated_active(self) -> tuple[Expectation, ...]:
        """The deployed firing hooks that MUST fire (the six)."""
        return tuple(e for e in self.gated if e.status == "active" and not e.absent)

    @property
    def gated_absent(self) -> tuple[Expectation, ...]:
        """Tombstones gated as must-NOT-fire (prune-conformance; the ruff-gate)."""
        return tuple(e for e in self.gated if e.absent)

    @property
    def observed_not_gated(self) -> tuple[Expectation, ...]:
        return tuple(e for e in self.expectations if not e.is_gated)

    def by_id(self, component_id: str) -> Expectation | None:
        return next((e for e in self.expectations if e.component_id == component_id), None)


def load_oracle(manifest_path: Path | str) -> Oracle:
    """Parse a manifest's engages: expectations into an Oracle. Read-only."""
    path = Path(manifest_path)
    if not path.exists():
        raise OracleError(f"manifest not found: {path}")
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise OracleError(f"manifest is not a mapping: {path}")
    version = str(spec.get("methodology_version", "")).strip()
    components = spec.get("components")
    if not isinstance(components, list):
        raise OracleError(f"manifest has no components: list: {path}")
    exps: list[Expectation] = []
    for comp in components:
        if not isinstance(comp, dict):
            continue
        exp = _parse_expectation(comp)
        if exp is not None:
            exps.append(exp)
    if not exps:
        raise OracleError(f"manifest carries no engages: expectations (pre-Slice-B?): {path}")
    return Oracle(version=version, expectations=tuple(exps))


# ---------------------------------------------------------------------------
# Signature-breadth discipline ([#253c]): a gated hook-stdout signature must be the
# LONGEST STABLE SUBSTRING of the hook's own stdout — never a fragment broad enough to
# match a filename echoed in git output or a generic word in prose (the `closure` case,
# which matched review_closures.py AND the arc prompt's "/review-closures").
# ---------------------------------------------------------------------------

_SIG_MIN_LEN = 8
_SIG_SEPARATORS = set("-_ :.")


def _tracked_basenames(repo_root: Path) -> tuple[str, ...]:
    r = subprocess.run(  # noqa: S603 — fixed argv, no shell
        ["git", "ls-files"], cwd=str(repo_root), capture_output=True, text=True)
    if r.returncode != 0:
        return ()
    return tuple({line.rsplit("/", 1)[-1] for line in r.stdout.splitlines() if line.strip()})


def _is_partial_word_match(sig: str, name: str) -> bool:
    """True when `sig` occurs inside `name` NOT aligned on word boundaries — i.e. the char
    before or after the match is alphanumeric. `closure` in `review_closures.py` is partial
    (followed by `s`); `canonical_freshness` in `canonical_freshness_gate.py` is aligned."""
    start = name.find(sig)
    while start != -1:
        before = name[start - 1] if start > 0 else ""
        after = name[start + len(sig)] if start + len(sig) < len(name) else ""
        if not (before.isalnum() or after.isalnum()):
            return False  # this occurrence is boundary-aligned -> not partial
        start = name.find(sig, start + 1)
    return name.find(sig) != -1


def signature_breadth_problems(oracle: Oracle, *, repo_root: Path | None = None,
                               arc_prompt: str | None = None) -> list[str]:
    """Lint every GATED hook-stdout signature for over-breadth ([#253c]). Returns a flat
    problem list (empty == disciplined). Checks: minimum length; contains a separator
    (a bare alphabetic word is generic prose); no partial-word match inside a tracked
    filename (git-output echo risk); not a substring of the arc prompt (which echoes
    into the transcript as a user message)."""
    problems: list[str] = []
    names = _tracked_basenames(repo_root) if repo_root else ()
    for exp in oracle.gated:
        sig, cid = exp.signature, exp.component_id
        if len(sig) < _SIG_MIN_LEN:
            problems.append(f"{cid}: signature {sig!r} shorter than {_SIG_MIN_LEN} chars")
        if not any(c in _SIG_SEPARATORS for c in sig):
            problems.append(f"{cid}: signature {sig!r} is a bare word (no separator) — generic")
        for name in names:
            if _is_partial_word_match(sig, name):
                problems.append(
                    f"{cid}: signature {sig!r} partial-word-matches tracked file {name!r}")
        if arc_prompt and sig in arc_prompt:
            problems.append(f"{cid}: signature {sig!r} appears in the arc prompt itself")
    return problems


def _repo_root() -> Path:
    # deploy/lived_sandbox/oracle.py -> repo root is three parents up.
    return Path(__file__).resolve().parent.parent.parent


def load_for_version(version: str, *, repo_root: Path | None = None) -> Oracle:
    """Resolve ``deploy/manifest-v<version>.yaml`` under the hub and load its oracle."""
    bare = version[1:] if version.startswith("v") else version
    root = repo_root or _repo_root()
    return load_oracle(root / "deploy" / f"manifest-v{bare}.yaml")
