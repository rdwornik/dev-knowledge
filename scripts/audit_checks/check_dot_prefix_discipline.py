"""`check_dot_prefix_discipline` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with the two constants it exclusively owns. No logic,
naming, formatting or docstring change; `audit.py` re-exports all three names.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# Config-file suffixes subject to dot-prefix discipline (root-level only).
_CONFIG_SUFFIXES = {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg", ".conf"}

# Industry-standard names that MUST NOT be dot-prefixed (ADR-59 exception list).
# This is a mirror of the ADR-59 exception list — update BOTH together when a
# new tool is adopted (see PLAYBOOK "Universal visual pattern" maintenance rule).
_DOT_PREFIX_EXCEPTIONS = {
    "pyproject.toml",       # Python PEP 518
    "package.json",         # npm
    "package-lock.json",    # npm lockfile
    "Cargo.toml",           # Rust
    "setup.py",             # Python legacy
    "setup.cfg",            # Python legacy
    "pytest.ini",           # pytest will not read .pytest.ini (ADR-59 amend 2026-06-02)
    "requirements.txt",     # pip convention
    "requirements-dev.txt",
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "tach.toml",            # verified 2026-05-27: tach 0.34.0 does not read .tach.toml
    "README.md",            # deprecated from baseline; if present, no dot
}


def check_dot_prefix_discipline(repo_path: Path) -> list[Finding]:
    """Root config files dot-prefixed unless on exception list (ADR-59 D1).

    Root-level only — subfolder configs are ignored. A config-suffix file that is
    neither dot-prefixed nor on the ADR-59 exception list is a violation.
    """
    violations = []
    for p in sorted(repo_path.iterdir()):
        if not p.is_file():
            continue
        if p.suffix not in _CONFIG_SUFFIXES:
            continue
        if p.name.startswith("."):
            continue
        if p.name in _DOT_PREFIX_EXCEPTIONS:
            continue
        violations.append(p.name)
    if violations:
        return [Finding("dot_prefix_discipline", "fail",
                        f"Root config files not dot-prefixed (not on ADR-59 exception list): {violations}")]
    return [Finding("dot_prefix_discipline", "pass",
                    "All root config files dot-prefixed or on ADR-59 exception list")]
