#!/usr/bin/env python
"""check_seal_identity.py — [#475] seal identity as a pre-commit gate on handoff bundles.

[#473] taught `gen_handoff.verify_seal_identity` to refuse SEALING a bundle whose internal
slug does not name its own directory — but that refusal fires inside `generate()`, so it
governs the machine path only. A hand-renamed directory, an edited Slug row, or a copied
bundle all reach `git commit` unchecked, and once committed the artifact is immutable, so
the defect is permanent (live proof: the 2026-08-02 boot absorbed three sealed probe rows
naming the un-suffixed sibling bundle). This hook runs the SAME verifier — reused, not
reimplemented — over every bundle a staged `docs/handoffs/**` path belongs to, at the
moment the artifact becomes durable.

Wiring: a `.pre-commit-config.yaml` local hook with `files: '^docs/handoffs/'` and
`pass_filenames: true`, so pre-commit invokes it only when such files are staged (zero
cost otherwise) and hands it exactly the staged paths.

Exit codes (honest by contract): 0 clean / nothing to check; 1 identity violation;
2 internal error — an error is a BLOCK, never a silent pass.

Honest limit (stated in the [#475] row): this catches the Slug row disagreeing with the
directory. A stale P0c/P3/P8 locator inside an otherwise correctly-labelled bundle is not
detected here.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Bare import first so every launch path (pytest, hook, direct run) resolves ONE module
# object for gen_handoff — the #153 two-copies identity/monkeypatch trap.
_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))
try:
    from gen_handoff import BundleIdentityError, verify_seal_identity
except ImportError:  # pragma: no cover — package-style launch
    from scripts.gen_handoff import BundleIdentityError, verify_seal_identity

_GENRE = ("docs", "handoffs")


def bundle_dir_for(path: Path) -> Path | None:
    """The bundle directory a staged path belongs to, or None when it is not in one.

    `docs/handoffs/<bundle>/<...>` -> `docs/handoffs/<bundle>`; a file sitting directly
    at the genre root (e.g. docs/handoffs/README.md) belongs to no bundle. Works on both
    the repo-relative paths pre-commit passes and absolute paths (tests), by locating the
    `docs/handoffs` segment pair inside the path rather than assuming a prefix.
    """
    parts = path.parts
    for i in range(len(parts) - 1):
        if parts[i : i + 2] == _GENRE:
            if len(parts) >= i + 4:  # at least one component below the bundle dir
                return Path(*parts[: i + 3])
            return None
    return None


def main(argv: list[str] | None = None) -> int:
    paths = sys.argv[1:] if argv is None else argv
    bundles: dict[Path, None] = {}  # ordered dedupe: one bundle verifies once
    for raw in paths:
        bundle = bundle_dir_for(Path(raw))
        if bundle is not None:
            bundles[bundle] = None

    failures: list[str] = []
    for bundle in bundles:
        try:
            verify_seal_identity(bundle)
        except BundleIdentityError as exc:
            failures.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — FR4: an internal error must BLOCK
            print(f"check_seal_identity: INTERNAL ERROR verifying {bundle}: {exc!r} — "
                  f"refusing the commit; an error is never a silent pass",
                  file=sys.stderr)
            return 2

    if failures:
        for failure in failures:
            print(f"check_seal_identity: SEAL-IDENTITY FAIL: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
