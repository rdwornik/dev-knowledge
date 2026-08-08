"""deploy/carrier_docs.py — the DOC-CARRIER: hub doc paths reconciled into a consumer.

The file-tree carrier specified by `deploy/release-v1.3.x-contract.md` §"Decision per
item" (#280): *"add a file-tree carrier (`carrier_docs`?) that reconciles a declared set
of source->dest doc paths (detect = bytes-match, apply = copy, verify = re-read),
registered in `deploy/tool.py`"*. It exists because the five pre-v1.4.0 carriers ship no
arbitrary doc tree — global-config copies ONE fixed file to a user dir, and the floor /
mesh / precommit / plugin carriers each own a fixed, semantically-special payload. A
plain "carry these hub docs to the consumer verbatim" vector had no home, so two BACKLOG
rows sat undeployable behind it:

- **[#280]** the intake area — `docs/intake/README.md` + `templates/intake-template.md`.
  ADR-98 ruling 1 (Accepted 2026-07-07): *"Greenfield consumers inherit `docs/intake/` at
  methodology deploy. The deploy manifest does not yet propagate the intake area or
  `templates/intake-template.md` ... so that propagation gap is filed as BACKLOG #280"*.
- **[#315]** `INSTALL.md` at the consumer root, sourced from the hub-canonical
  `plugins/tier1-lifecycle/INSTALL.md`.

Unlike every other carrier this one is **fully manifest-driven**: it hardcodes no payload.
The set of (source -> dest) pairs is read from the manifest carrier's ``target``, so
shipping one more hub doc to consumers is a manifest edit, not a code change.

Target shape (the v1.4.0 manifest's ``docs`` carrier entry)::

    doc_paths:
      - source: docs/intake/README.md          # hub-relative source
        path:   docs/intake/README.md          # consumer-relative destination
      - source: plugins/tier1-lifecycle/INSTALL.md
        path:   INSTALL.md

Both legs are repo-relative and are refused if absolute or escaping the root (``..``) —
a generic copy vector is exactly where a malformed manifest could otherwise write outside
the consumer tree.

Deploy mechanism is a straight verbatim COPY (a carried doc has no rev — it is a
hash-guarded *replica* of the hub source, the ADR-93 floor model), so detection
distinguishes only three of the four contract states: ``ABSENT`` (no declared doc
present), ``PRESENT_CORRECT`` (every declared doc byte-identical to its hub source) and
``PRESENT_DRIFTED`` (any missing-but-not-all, or any content mismatch). There is no
``PRESENT_WRONG_VERSION`` — the contract permits a carrier not to exercise all four.

- ``detect`` compares each consumer doc against its hub source -> CarrierState.
- ``apply`` copies each hub source to the consumer path, creating parent dirs;
  idempotent (byte-identical -> changed=False).
- ``verify`` independently re-reads + re-compares via its OWN code path that never routes
  through detect's classifier (ADR-92 Decision 9 / D9). ``_classify_docs`` (detect's
  judgment) and ``_verify_docs`` (verify's judgment) are distinct functions sharing no
  correctness-judgment helper; reading the hub *source* bytes and parsing the manifest
  target are shared SPEC reads (D9-permitted), not shared judgment.

Text is LF-normalized on both read and write (the ``carrier_mesh`` precedent) so a
Windows hub checkout with ``autocrlf`` cannot flip a byte-clean match to a permanent
false drift.
"""

from __future__ import annotations

import logging
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

log = logging.getLogger(__name__)

CARRIER_ID = "docs"

# The hub root (this module lives in deploy/, so the hub is its parent's parent),
# used to resolve each pair's repo-relative `source`.
_HUB_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Shared SPEC reads / parsers (D9-permitted — no state judgment here).
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """LF-normalize so a Windows checkout can't flip a byte-clean match to a miss."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _safe_rel(value: Any, field: str) -> str:
    """A repo-relative path that cannot escape its root — else raise.

    A generic copy carrier is the one vector where a malformed manifest could write
    outside the consumer tree, so an absolute path or any ``..`` segment is refused
    loudly. ``assess``/``execute`` render a raised error as a row rather than crashing.
    """
    rel = str(value or "").strip()
    if not rel:
        raise ValueError(f"docs carrier: doc_paths entry missing {field!r}")
    # Absoluteness is PLATFORM-FLAVORED: on Windows `Path("/tmp/x").is_absolute()` is
    # False (root but no drive) and on POSIX `Path("C:/x").is_absolute()` is False, so a
    # single-flavor check leaks the other platform's absolute paths through. Ask BOTH.
    # `..` is tested on the Windows flavor because it splits on `/` AND `\`, so a
    # backslash traversal cannot hide inside one posix-parsed component.
    win, posix = PureWindowsPath(rel), PurePosixPath(rel)
    if win.is_absolute() or posix.is_absolute() or win.anchor or posix.anchor:
        raise ValueError(f"docs carrier: {field} {rel!r} must be repo-relative, not absolute")
    if ".." in win.parts:
        raise ValueError(f"docs carrier: {field} {rel!r} may not contain '..'")
    return PurePosixPath(*win.parts).as_posix()


def _pairs(target: Any) -> tuple[tuple[str, str], ...]:
    """The declared (source_rel, dest_rel) pairs from the manifest carrier target.

    A SPEC read: it parses what the consumer SHOULD carry, never what it does carry.
    """
    entries = (target or {}).get("doc_paths")
    if not isinstance(entries, list) or not entries:
        raise ValueError("docs carrier: target declares no doc_paths: list")
    pairs: list[tuple[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"docs carrier: doc_paths entry is not a mapping: {entry!r}")
        pairs.append((_safe_rel(entry.get("source"), "source"), _safe_rel(entry.get("path"), "path")))
    return tuple(pairs)


def _hub_text(source_rel: str) -> str:
    """The hub canonical source text for one declared doc, LF-normalized."""
    src = _HUB_ROOT / source_rel
    if not src.exists():
        raise ValueError(f"docs carrier: hub source missing: {source_rel}")
    return _normalize(src.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# detect path — _classify_docs (detect's correctness judgment).
# ---------------------------------------------------------------------------


def _classify_docs(root: Path, pairs: tuple[tuple[str, str], ...]) -> CarrierState:
    """detect's judgment: the consumer's declared docs vs their hub sources.

    Three states only (a copied doc has no rev): nothing present -> ABSENT, every doc
    byte-identical -> PRESENT_CORRECT, anything else (partial presence or content
    mismatch) -> PRESENT_DRIFTED.
    """
    present = 0
    correct = 0
    for source_rel, dest_rel in pairs:
        dest = root / dest_rel
        if not dest.exists():
            continue
        present += 1
        if _normalize(dest.read_text(encoding="utf-8")) == _hub_text(source_rel):
            correct += 1
    if present == 0:
        return CarrierState.ABSENT
    if correct == len(pairs):
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN fresh read + its OWN compare;
# shares no correctness-judgment helper with _classify_docs.
# ---------------------------------------------------------------------------


def _verify_docs(root: Path, pairs: tuple[tuple[str, str], ...]) -> list[str]:
    """verify's independent judgment: re-read fresh, return unmet requirements.

    Built so a bug in detect's _classify_docs cannot be mirrored here: it asserts each
    doc's existence and byte identity directly, per path, and never counts states.
    Empty list => target satisfied.
    """
    failures: list[str] = []
    for source_rel, dest_rel in pairs:
        dest = root / dest_rel
        if not dest.exists():
            failures.append(f"carried doc absent: {dest_rel}")
            continue
        current = _normalize(dest.read_text(encoding="utf-8"))
        expected = _hub_text(source_rel)
        if current != expected:
            failures.append(
                f"{dest_rel} differs from hub source {source_rel} "
                f"({len(current)}B on disk vs {len(expected)}B source)"
            )
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class DocsCarrier(Carrier):
    """Doc-carrier — verbatim hub-doc replicas in the consumer repo (#280 / #315)."""

    carrier_id = CARRIER_ID

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def detect(self, target: Any) -> CarrierState:
        pairs = _pairs(target)
        state = _classify_docs(self.repo_root, pairs)
        log.debug("docs detect: %s (%d doc(s)) -> %s", self.repo_root, len(pairs), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        pairs = _pairs(target)
        changes: list[str] = []
        for source_rel, dest_rel in pairs:
            desired = _hub_text(source_rel)
            dest = self.repo_root / dest_rel
            existed = dest.exists()
            if existed and _normalize(dest.read_text(encoding="utf-8")) == desired:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(desired, encoding="utf-8", newline="\n")
            changes.append(f"{'updated' if existed else 'created'} {dest_rel} from {source_rel}")
        if not changes:
            return ApplyResult(changed=False, detail=f"all {len(pairs)} carried doc(s) already at hub source")
        log.info("docs apply: %s -> %d change(s)", self.repo_root, len(changes))
        return ApplyResult(
            changed=True,
            changes=tuple(changes),
            detail=f"{len(changes)} of {len(pairs)} carried doc(s) written from hub source",
        )

    def verify(self, target: Any) -> VerifyResult:
        # Independent read + compare — does NOT call _classify_docs (D9).
        pairs = _pairs(target)
        failures = _verify_docs(self.repo_root, pairs)
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail=(
                f"all {len(pairs)} carried doc(s) match hub source"
                if ok
                else f"{len(failures)} of {len(pairs)} carried doc(s) unmet"
            ),
        )
