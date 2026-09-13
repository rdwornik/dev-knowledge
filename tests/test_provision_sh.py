"""[#664] guards `.devcontainer/provision.sh` against naming a retired module by path.

`safe_remove`'s static importer scan cannot see a referrer that names a module by file path
(`scripts/<name>.py` in a shell command) rather than by `import` — which is how six call sites
naming the retired `scripts/cloud_provisioning.py` survived that module's own deletion at
`3c9418cc` ([#734]) and false-PASSed as safe. This asserts the class stays closed going forward:
provision.sh must never name a `scripts/*.py` path that is not on disk.
"""
from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PROVISION_SH = _REPO_ROOT / ".devcontainer" / "provision.sh"

# Matches an actual invocation (`python scripts/<name>.py`), not a prose mention of the path —
# this file's own retirement-record comments cite retired paths by name deliberately.
_INVOCATION_RE = re.compile(r"\bpython\s+scripts/([A-Za-z0-9_]+\.py)")


def test_provision_sh_names_no_retired_module_path():
    text = _PROVISION_SH.read_text(encoding="utf-8")
    named = set(_INVOCATION_RE.findall(text))
    missing = sorted(name for name in named if not (_REPO_ROOT / "scripts" / name).exists())
    assert not missing, f"provision.sh invokes retired scripts/ path(s): {missing}"
