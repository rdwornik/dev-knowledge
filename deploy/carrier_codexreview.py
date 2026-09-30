"""deploy/carrier_codexreview.py — the Codex-review organ carrier ([#1328]).

Reconciles the Codex-review organ (the reviewer wrapper script + its slash-command
doc) from the hub-tracked source (``deploy/codex-review.ps1`` / ``deploy/codex-review.md``)
to the user-level ``~/.claude/`` tree: ``bin/codex-review.ps1`` and
``commands/codex-review.md``. Same USER-machine-scoped shape as
``carrier_globalconfig.py`` (ADR-54 precedent) — ``repo_root`` is accepted for a
uniform carrier constructor but is UNUSED — extended to carry a PAIR of files
instead of one (the ``carrier_docs.py`` multi-path precedent), each written under
a different subdirectory of the user base.

Before this carrier the organ was L0-only and untracked: ``~/.claude/bin/
codex-review.ps1`` and ``~/.claude/commands/codex-review.md`` existed only on the
operator's machine, in no ref (R42.2, `to-browser/RATIFICATION-2026-09-30.md` v2).
Its source now moves under the hub, tested; ``~/.claude/`` becomes an installed
copy, never edited directly (ruling (j)).

BYTE FIDELITY, NOT LF-NORMALIZATION — the one deliberate divergence from
``carrier_globalconfig``'s committed-blob read. That carrier reads ``git show
HEAD:<rel>`` and LF-normalizes, because its target (``~/.codex/AGENTS.md``) is a
plain LF doc. This carrier's target is the OPPOSITE: two Windows-native,
CRLF-authored files (the live organ, verified `file` CRLF on both), and the whole
point of ``[#1328]`` is that a deploy run REPRODUCES those two files byte-for-byte.
So this carrier reads the WORKING-TREE bytes directly (``Path.read_bytes()``, no
git-show, no newline translation) and ``.gitattributes`` pins both hub sources
CRLF on checkout (``*.ps1 text eol=crlf`` already covers the script;
``deploy/codex-review.md text eol=crlf`` was added for the doc) so a fresh clone —
including CI, on either OS, since ``eol=crlf`` renders the same regardless of the
checkout platform — reproduces the same CRLF bytes this carrier was authored
against. Reading the committed blob here would silently LF-flip the reproduction
this carrier's own contract exists to prove.

Detection is three-state (ABSENT / PRESENT_CORRECT / PRESENT_DRIFTED), same as
``carrier_globalconfig`` — a copied file has no rev.

Test safety: the user-config base is injectable (constructor param
``user_config_base``, then the ``CLAUDE_CONFIG_DIR`` env var — Claude Code's own
real relocation variable, mirroring ``carrier_globalconfig``'s ``CODEX_HOME``
precedent — then the default ``~/.claude``), so tests point it at a temp dir and
the real ``~/.claude/`` is never written by this carrier (ruling (j): the
integrator installs post-merge, from the merged hub source).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

log = logging.getLogger(__name__)

CARRIER_ID = "codex-review-organ"

# The hub root (this module lives in deploy/, so the hub is its parent's parent),
# used to resolve the manifest's repo-relative `source_path` entries.
_HUB_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_USER_BASE = Path.home() / ".claude"

#: The two (source_path, target_rel) pairs this carrier ships, mirroring the
#: manifest's `organ_paths:` target shape 1:1 — used as a fallback when a target
#: omits the list (defensive; the manifest always declares it).
_DEFAULT_PAIRS: tuple[tuple[str, str], ...] = (
    ("deploy/codex-review.ps1", "bin/codex-review.ps1"),
    ("deploy/codex-review.md", "commands/codex-review.md"),
)


def _resolve_user_base(override: Path | str | None) -> Path:
    """Resolve the user-config base: param > CLAUDE_CONFIG_DIR env > ~/.claude.

    The injection point that keeps tests off the real ``~/.claude/``: a test passes
    a temp dir as ``override``. ``CLAUDE_CONFIG_DIR`` mirrors Claude Code's own
    real relocation env (the ``carrier_globalconfig``/``CODEX_HOME`` precedent) so
    real operator usage stays honest too.
    """
    if override is not None:
        return Path(override)
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return Path(env)
    return DEFAULT_USER_BASE


def _pairs(target: Any) -> tuple[tuple[str, str], ...]:
    """The declared (source_path, target_rel) pairs from the manifest carrier target."""
    entries = (target or {}).get("organ_paths")
    if not isinstance(entries, list) or not entries:
        return _DEFAULT_PAIRS
    out: list[tuple[str, str]] = []
    for entry in entries:
        out.append((str(entry["source_path"]), str(entry["target_rel"])))
    return tuple(out)


def _read_source(source_rel: str) -> bytes:
    """The hub canonical source bytes, verbatim (no newline translation — see module docstring)."""
    return (_HUB_ROOT / source_rel).read_bytes()


# ---------------------------------------------------------------------------
# detect path — _classify_organ (detect's correctness judgment).
# ---------------------------------------------------------------------------


def _classify_organ(pairs: tuple[tuple[str, str], ...], user_base: Path) -> CarrierState:
    """detect's judgment across BOTH files: nothing present -> ABSENT, every file
    byte-identical -> PRESENT_CORRECT, anything else (partial presence or content
    mismatch) -> PRESENT_DRIFTED."""
    present = 0
    correct = 0
    for source_rel, target_rel in pairs:
        target_path = user_base / target_rel
        if not target_path.exists():
            continue
        present += 1
        if target_path.read_bytes() == _read_source(source_rel):
            correct += 1
    if present == 0:
        return CarrierState.ABSENT
    if correct == len(pairs):
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN fresh read + its OWN compare;
# shares no correctness-judgment helper with _classify_organ.
# ---------------------------------------------------------------------------


def _verify_organ(pairs: tuple[tuple[str, str], ...], user_base: Path) -> list[str]:
    """verify's independent judgment: re-read fresh, return unmet requirements per file."""
    failures: list[str] = []
    for source_rel, target_rel in pairs:
        target_path = user_base / target_rel
        if not target_path.exists():
            failures.append(f"organ file absent: {target_path}")
            continue
        current = target_path.read_bytes()
        expected = _read_source(source_rel)
        if current != expected:
            failures.append(
                f"{target_path} differs from hub source {source_rel} "
                f"({len(current)}B on disk vs {len(expected)}B source)"
            )
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class CodexReviewCarrier(Carrier):
    """Codex-review organ carrier — USER-machine scoped (not the consumer), two files."""

    carrier_id = CARRIER_ID

    def __init__(
        self, repo_root: Path | str, user_config_base: Path | str | None = None
    ) -> None:
        self.repo_root = Path(repo_root)  # consumer root; UNUSED — user-scoped carrier
        self.user_config_base = _resolve_user_base(user_config_base)

    def detect(self, target: Any) -> CarrierState:
        pairs = _pairs(target)
        state = _classify_organ(pairs, self.user_config_base)
        log.debug("codex-review-organ detect: %s (%d file(s)) -> %s",
                  self.user_config_base, len(pairs), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        pairs = _pairs(target)
        changes: list[str] = []
        for source_rel, target_rel in pairs:
            desired = _read_source(source_rel)
            target_path = self.user_config_base / target_rel
            existed = target_path.exists()
            if existed and target_path.read_bytes() == desired:
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(desired)
            action = "updated" if existed else "created"
            changes.append(f"{action} {target_path} from {source_rel}")
        if not changes:
            return ApplyResult(changed=False, detail=f"all {len(pairs)} organ file(s) already at hub source")
        log.info("codex-review-organ apply: %s -> %d change(s)", self.user_config_base, len(changes))
        return ApplyResult(
            changed=True,
            changes=tuple(changes),
            detail=f"{len(changes)} of {len(pairs)} organ file(s) written from hub source",
        )

    def verify(self, target: Any) -> VerifyResult:
        # Independent read + compare — does NOT call _classify_organ (D9).
        pairs = _pairs(target)
        failures = _verify_organ(pairs, self.user_config_base)
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail=(
                f"all {len(pairs)} organ file(s) match hub source"
                if ok
                else f"{len(failures)} of {len(pairs)} organ file(s) unmet"
            ),
        )
