"""[#683] regression tooth — the retired `/override` command stays removed, BOTH halves.

`/override` was RETIRED by the ADR-85 amendment 2026-08-03 §A2: its local-token path
discharges no gate, `scripts/session_end_backpressure.py` no longer reads the token, and the
command's own description says so in as many words. It nevertheless survived as a component
node in the current deploy manifest with a payload behind it, so every fully-deployed
consumer installed a working-looking escape hatch that escapes nothing
(`docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:56 finding, :79 pointer).

**Node and payload are ONE act, and that coupling is what this module holds.** Removing the
node alone orphans the payload in the carried corpus; removing the payload alone leaves a
node pointing at nothing. One test, asserting on the union of both violations, so a later
edit cannot restore one side quietly while the other stays gone.

HONEST LIMIT — read this before treating the tooth as a second line of defence. It is the
FIRST and only one. `deploy/release_lint.py` does **not** catch a split: it reconciles the
five version anchors (C1-C5) and validates component SCHEMA (C6-C8), and it never resolves a
component's ``artifacts[].path`` against the tree — grep it for ``artifacts`` and the only
hits are prose. A manifest node whose payload has been deleted lints green today.

SCOPE is the CURRENT manifest only — the highest-versioned ``deploy/manifest-v*.yaml`` on
disk, resolved by reusing ``release_lint._current_manifest_version`` rather than re-deriving
it. That mirrors the C7 currency doctrine (R-G-G3b, [#621]): a superseded manifest is frozen
release history and is not retro-edited, so v1.0.0-v1.4.0 keep their `/override` node as the
record of what those releases actually shipped.

THE ID PREDICATE IS SCOPED TO `status: active` (lane-x-683-three-small-fixes, per the
`lane-x-734-retire-stage-2` evidence's escalation, `docs/audits/
2026-09-12-technical-lane-x-734-retire-stage-2-evidence.md` "The ONE escalation"). A bare-id
match at ANY status forbade the deploy manifest's own documented lifecycle — a removed
component's "manifest entry is retained as a tombstone" — from ever recording `/override`'s
retirement, even though a tombstone with no `artifacts:` ships no payload and restores
nothing. The other two legs (payload-file existence, artifacts[].path) already carry the
"node and payload are ONE act" intent for a REAL restore; scoping the id leg to `active`
narrows it to that same restore, not to the tombstone record.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import release_lint as rl

_REPO_ROOT = Path(__file__).resolve().parents[1]

#: The retired command's two halves, each named once so a partial restore cannot pass.
_PAYLOAD_REL = ".claude/commands/override.md"
_COMPONENT_ID = "override-command"


def _violations(components: list[dict], manifest_name: str, *, payload_exists: bool) -> list[str]:
    """The pure predicate, factored out so a synthetic manifest can drive it without a live
    repo. Three legs, each independent: payload file, active id, shipped artifact path."""
    violations: list[str] = []

    if payload_exists:
        violations.append(f"payload present: {_PAYLOAD_REL}")

    # By id AND by artifact path: a restore could re-file the same payload under a different
    # component id, and an id-only predicate would report it absent.
    #
    # Scoped to `status: active` — a `status: removed` tombstone entry (the deploy manifest's
    # own documented lifecycle) carries the retired id forever by design and ships no
    # artifacts; the artifacts[].path leg below still catches a tombstone that keeps shipping
    # the payload, so narrowing this leg to `active` loses no real coverage.
    if any(c.get("id") == _COMPONENT_ID and c.get("status") == "active" for c in components):
        violations.append(f"manifest node present: {manifest_name} id={_COMPONENT_ID}")

    shipping = sorted(
        str(c.get("id"))
        for c in components
        for art in (c.get("artifacts") or [])
        if isinstance(art, dict) and art.get("path") == _PAYLOAD_REL
    )
    if shipping:
        violations.append(
            f"manifest still ships {_PAYLOAD_REL} via component(s) {shipping} "
            f"in {manifest_name}"
        )

    return violations


@pytest.mark.live_repo
def test_override_command_stays_removed():
    """FAIL if EITHER half returns — the payload file, or an ACTIVE manifest node shipping it."""
    version = rl._current_manifest_version(_REPO_ROOT)
    assert version is not None, "no deploy/manifest-v*.yaml on disk — the tooth has no subject"
    manifest_path = _REPO_ROOT / "deploy" / f"manifest-v{version}.yaml"
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    components = spec.get("components") or []

    violations = _violations(
        components, manifest_path.name,
        payload_exists=(_REPO_ROOT / _PAYLOAD_REL).exists())

    assert not violations, (
        "/override is back, in whole or in part — "
        + "; ".join(violations)
        + ". It was retired by the ADR-85 amendment 2026-08-03 §A2 and discharges no gate; "
        "a consumer that installs it gets a command which logs a token and changes nothing "
        "([#683]). Node and payload are ONE act — restore both or neither."
    )


def test_a_removed_tombstone_with_no_artifacts_does_not_violate():
    """RED-first witness: a `status: removed` tombstone entry, id `override-command`, no
    `artifacts:` — the deploy manifest's own documented lifecycle for a retired component.
    Refused before the id leg was scoped to `active`; lands after."""
    components = [{"id": _COMPONENT_ID, "status": "removed"}]
    assert _violations(components, "manifest-vX.yaml", payload_exists=False) == []


def test_an_active_override_component_still_violates():
    """The id leg still fires on a genuine restore — an ACTIVE component reusing the retired
    id — so scoping to `active` narrows the predicate without hollowing it out."""
    components = [{"id": _COMPONENT_ID, "status": "active"}]
    violations = _violations(components, "manifest-vX.yaml", payload_exists=False)
    assert any(_COMPONENT_ID in v for v in violations)


def test_a_removed_tombstone_that_still_ships_the_payload_path_still_violates():
    """The artifacts[].path leg is id-and-status-blind by design — a tombstone that keeps
    shipping the payload is caught regardless of what scoped the id leg."""
    components = [{"id": _COMPONENT_ID, "status": "removed",
                   "artifacts": [{"path": _PAYLOAD_REL}]}]
    violations = _violations(components, "manifest-vX.yaml", payload_exists=False)
    assert any(_PAYLOAD_REL in v for v in violations)
