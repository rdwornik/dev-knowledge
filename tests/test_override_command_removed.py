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


@pytest.mark.live_repo
def test_override_command_stays_removed():
    """FAIL if EITHER half returns — the payload file, or a manifest node shipping it."""
    version = rl._current_manifest_version(_REPO_ROOT)
    assert version is not None, "no deploy/manifest-v*.yaml on disk — the tooth has no subject"
    manifest_path = _REPO_ROOT / "deploy" / f"manifest-v{version}.yaml"
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    components = spec.get("components") or []

    violations: list[str] = []

    if (_REPO_ROOT / _PAYLOAD_REL).exists():
        violations.append(f"payload present: {_PAYLOAD_REL}")

    # By id AND by artifact path: a restore could re-file the same payload under a different
    # component id, and an id-only predicate would report it absent.
    if any(c.get("id") == _COMPONENT_ID for c in components):
        violations.append(f"manifest node present: {manifest_path.name} id={_COMPONENT_ID}")

    shipping = sorted(
        str(c.get("id"))
        for c in components
        for art in (c.get("artifacts") or [])
        if isinstance(art, dict) and art.get("path") == _PAYLOAD_REL
    )
    if shipping:
        violations.append(
            f"manifest still ships {_PAYLOAD_REL} via component(s) {shipping} "
            f"in {manifest_path.name}"
        )

    assert not violations, (
        "/override is back, in whole or in part — "
        + "; ".join(violations)
        + ". It was retired by the ADR-85 amendment 2026-08-03 §A2 and discharges no gate; "
        "a consumer that installs it gets a command which logs a token and changes nothing "
        "([#683]). Node and payload are ONE act — restore both or neither."
    )
