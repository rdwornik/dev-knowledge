#!/usr/bin/env python
"""coherence_nudge.py — pre-commit forgotten-version-bump nudge (coherence spine).

The deterministic reconciliation checker (validate_reconciliation.py) only fires once a
dependent's declared version DISAGREES with the spec — it cannot see the false-negative
where a spec's CONTENT changes but its version is NOT bumped (so every dependent still
"matches" the unchanged number while the spec actually moved). This pre-commit hook closes
that gap: on a commit that touches a registered spec, if the spec's content changed vs HEAD
but its version did NOT, print a NON-BLOCKING stdout nudge and append a line to the
firing-rate log.

Design constraints (operator ruling, prompt A):
  - NON-BLOCKING — always exit 0 (a gate WARN on every typo is a false-positive death-spiral;
    a forgotten bump is a nudge, not a gate). NOT wired into the ship-gate Finding pipeline.
  - NO escape hatch in v1 — a non-blocking nudge needs no suppression.
  - INSTRUMENTED — every fire appends one line to logs/coherence-nudge.log. That firing-rate
    data is what decides v2's open questions (escape hatch? deferred-hash? promote to gate?).

Spec set is single-sourced from validate_reconciliation._SPEC_REGISTRY (the same specs the
reconciliation checker authorities), so the two halves never drift apart. Read-only except
the append-only firing-rate log (Layer-2: it instruments itself, drives no other state).
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

try:
    from scripts.validate_reconciliation import _SPEC_REGISTRY, SpecSource
except ImportError:
    from validate_reconciliation import _SPEC_REGISTRY, SpecSource

_LOG_PATH = _REPO_ROOT / "logs" / "coherence-nudge.log"


def _extract_version(text: str, spec: SpecSource) -> Optional[str]:
    """The spec version parsed from arbitrary spec TEXT (HEAD or staged), or None."""
    m = spec.version_re.search(text)
    return m.group(1) if m else None


def _short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def should_nudge(head_text: str, staged_text: str, spec: SpecSource) -> bool:
    """True iff the spec's CONTENT changed vs HEAD but its parsed version did NOT.

    Both versions must parse (an unparseable version is the reconciliation checker's
    concern, not the nudge's) and be equal while the content differs."""
    if head_text == staged_text:
        return False
    hv = _extract_version(head_text, spec)
    sv = _extract_version(staged_text, spec)
    return hv is not None and sv is not None and hv == sv


def _git_head_text(repo_root: Path, rel: str) -> Optional[str]:
    """The committed (HEAD) text of `rel`, or None when the file is new / git unavailable."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "show", f"HEAD:{rel}"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    return proc.stdout if proc.returncode == 0 else None


def _spec_for(rel: str) -> Optional[SpecSource]:
    """The registered SpecSource whose path equals `rel` (posix), or None."""
    norm = rel.replace("\\", "/")
    for spec in _SPEC_REGISTRY.values():
        if spec.path == norm:
            return spec
    return None


def _append_log(rel: str, version: str, head_text: str, staged_text: str,
                now: datetime, log_path: Path = _LOG_PATH) -> None:
    """Append one firing-rate line (append-only instrumentation)."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = (f"{now.isoformat(timespec='seconds')} {rel} version={version} "
            f"head={_short_hash(head_text)} staged={_short_hash(staged_text)}\n")
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(line)


def process(repo_root: Path, rel: str, now: Optional[datetime] = None,
            log_path: Path = _LOG_PATH) -> Optional[str]:
    """If `rel` is a registered spec changed-without-bump, log + return the nudge message.

    Returns the nudge string (also the signal a fire happened) or None. Pure given the
    repo state: reads HEAD + the staged working file, appends the log on a fire."""
    spec = _spec_for(rel)
    if spec is None:
        return None
    head_text = _git_head_text(repo_root, rel)
    if head_text is None:
        return None  # new file (no HEAD) — nothing to compare
    fpath = repo_root / rel
    if not fpath.exists():
        return None
    staged_text = fpath.read_text(encoding="utf-8", errors="replace")
    if not should_nudge(head_text, staged_text, spec):
        return None
    version = _extract_version(staged_text, spec) or "?"
    _append_log(rel, version, head_text, staged_text, now or datetime.now(), log_path)
    return (f"coherence-nudge: {rel} content changed but Version stayed {version}. "
            f"If this edit is substantive, bump the spec Version (and reconcile dependents' "
            f"reconciled_with). Non-blocking — logged to logs/coherence-nudge.log.")


def main(argv: Optional[list[str]] = None) -> int:
    """pre-commit entry: each staged filename arg is checked; print nudges; ALWAYS exit 0."""
    argv = sys.argv[1:] if argv is None else argv
    for rel in argv:
        msg = process(_REPO_ROOT, rel, log_path=_LOG_PATH)
        if msg:
            print(msg)
    return 0  # non-blocking by construction


if __name__ == "__main__":
    sys.exit(main())
