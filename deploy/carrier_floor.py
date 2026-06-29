"""deploy/carrier_floor.py — the per-repo methodology-floor carrier (ADR-92 C4).

Reconciles the consumer repo's methodology floor (ADR-78): ``.claude/CLAUDE-FLOOR.md``
+ its ``.sha256`` content-integrity sidecar. Unlike the global-config carrier this
one is **consumer-repo scoped** — it writes into the consumer tree (the ADR-78 /
generate_floor.py ``--out-dir`` write precedent, the ADR-92 "write-into-sibling"
relaxation).

Generation is REUSED from the hub's ``scripts/generate_floor.py`` by IMPORTING its
building blocks — ``render_floor`` (the floor body, byte-for-byte the shipped
template), ``floor_sha256`` (LF-normalized, autocrlf-proof hash) and ``validate``
(token-ceiling / F5 / zero-URL gate). They are cleanly importable, so NO subprocess
is needed. Importing the pieces (rather than shelling out to ``generate_floor.py
generate --out-dir``) is also the CORRECT scope: the CLI command additionally
refreshes the HUB's ``templates/child-methodology-floor.sha256`` anchor and prints an
install note — side-effects a consumer-only carrier must NOT cause. This carrier
writes ONLY the consumer tree; it never mutates the hub and never refactors the
generator (ADR-92 build-slice constraint).

Three contract states (the ``.sha256`` is content-integrity, not a version anchor —
so no PRESENT_WRONG_VERSION): ``ABSENT`` (floor missing), ``PRESENT_CORRECT``
(consumer floor + sidecar both hash to the freshly-generated corpus floor),
``PRESENT_DRIFTED`` (floor edited, corpus moved, or sidecar missing/stale).

Target shape (the v1.0.0 manifest's ``floor`` entry)::

    floor_path: .claude/CLAUDE-FLOOR.md           # relative to the consumer repo root
    sidecar_path: .claude/CLAUDE-FLOOR.md.sha256

D9 (ADR-92 Decision 9): ``_classify_floor`` (detect's judgment) and ``_verify_floor``
(verify's judgment) are distinct functions with no shared correctness-judgment helper.
``render_floor``/``floor_sha256``/``_read_sidecar_hash`` are shared SPEC reads + a
parser (D9-permitted, like target-parsing) — the JUDGMENT (compare-to-corpus) is
implemented twice, independently.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

# Reuse the hub generator's importable building blocks. scripts/ lives beside deploy/
# under the hub root; add it to the path so `import generate_floor` resolves.
_HUB_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = _HUB_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import generate_floor as gf  # noqa: E402

log = logging.getLogger(__name__)

CARRIER_ID = "floor"

# Defaults mirror generate_floor.py's own constants (the floor under the consumer's
# .claude/). The manifest target may override the relative paths.
DEFAULT_FLOOR_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/{gf.FLOOR_FILENAME}"
DEFAULT_SIDECAR_REL = f"{gf.CHILD_CLAUDE_DIRNAME}/{gf.SIDECAR_FILENAME}"

_SHA_RE = re.compile(r"[0-9a-f]{64}")


# ---------------------------------------------------------------------------
# Spec generation + sidecar parse. SHARED between detect/verify is D9-fine: this
# renders/hashes the SPEC (the corpus-state floor) and PARSES the sidecar — it does
# not JUDGE the consumer's state (that is _classify_floor / _verify_floor).
# ---------------------------------------------------------------------------


def _corpus_floor() -> tuple[str, str]:
    """Render the floor from the hub template at corpus state -> (body, sha256).

    The template content IS the shipped floor body (deterministic — same template ->
    same hash). Refuses if the hub template somehow violates a binding rule (it never
    should; the shipped template is canonical), so a broken hub floor fails loud
    rather than silently deploying garbage.
    """
    floor = gf.render_floor()
    issues = gf.validate(floor)
    if issues:
        raise RuntimeError(f"hub floor template failed validation: {issues}")
    return floor, gf.floor_sha256(floor)


def _read_sidecar_hash(sidecar_path: Path) -> str:
    """Extract the 64-hex digest recorded in the sidecar ('' if absent/unparsable)."""
    if not sidecar_path.exists():
        return ""
    m = _SHA_RE.search(sidecar_path.read_text(encoding="utf-8"))
    return m.group(0) if m else ""


# ---------------------------------------------------------------------------
# detect path — _classify_floor (detect's correctness judgment).
# ---------------------------------------------------------------------------


def _classify_floor(
    corpus_digest: str, floor_path: Path, sidecar_path: Path
) -> CarrierState:
    """detect's judgment: consumer floor + sidecar vs corpus floor -> CarrierState.

    absent floor -> ABSENT; consumer floor content AND its sidecar both hash to the
    corpus floor -> PRESENT_CORRECT; anything else (floor edited, corpus moved, or
    sidecar missing/stale) -> PRESENT_DRIFTED.
    """
    if not floor_path.exists():
        return CarrierState.ABSENT
    actual = gf.floor_sha256(floor_path.read_text(encoding="utf-8"))
    recorded = _read_sidecar_hash(sidecar_path)
    if actual == corpus_digest and recorded == corpus_digest:
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN re-hash + its OWN checks;
# shares no correctness-judgment helper with _classify_floor.
# ---------------------------------------------------------------------------


def _verify_floor(corpus_digest: str, floor_path: Path, sidecar_path: Path) -> list[str]:
    """verify's independent judgment: re-hash fresh, return unmet requirements.

    Built so a bug in detect's _classify_floor cannot be mirrored here: it checks the
    floor's content hash and the sidecar's recorded hash against the corpus digest
    directly + separately. Empty list => target satisfied.
    """
    failures: list[str] = []
    if not floor_path.exists():
        failures.append(f"floor absent: {floor_path}")
        return failures
    actual = gf.floor_sha256(floor_path.read_text(encoding="utf-8"))
    if actual != corpus_digest:
        failures.append(
            f"floor content hash {actual[:12]} != corpus floor {corpus_digest[:12]}"
        )
    if not sidecar_path.exists():
        failures.append(f"sidecar absent: {sidecar_path}")
    else:
        recorded = _read_sidecar_hash(sidecar_path)
        if recorded != corpus_digest:
            failures.append(
                f"sidecar hash {recorded[:12] or '(none)'} != corpus floor "
                f"{corpus_digest[:12]}"
            )
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class FloorCarrier(Carrier):
    """Per-repo methodology-floor carrier — bound to one consumer repo."""

    carrier_id = CARRIER_ID

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def _floor_path(self, target: Any) -> Path:
        return self.repo_root / (target or {}).get("floor_path", DEFAULT_FLOOR_REL)

    def _sidecar_path(self, target: Any) -> Path:
        return self.repo_root / (target or {}).get("sidecar_path", DEFAULT_SIDECAR_REL)

    def detect(self, target: Any) -> CarrierState:
        _, corpus_digest = _corpus_floor()
        state = _classify_floor(
            corpus_digest, self._floor_path(target), self._sidecar_path(target)
        )
        log.debug("floor detect: %s -> %s", self._floor_path(target), state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        floor, corpus_digest = _corpus_floor()
        fpath = self._floor_path(target)
        spath = self._sidecar_path(target)
        # idempotency: floor content + sidecar both already at corpus state.
        floor_ok = (
            fpath.exists()
            and gf.floor_sha256(fpath.read_text(encoding="utf-8")) == corpus_digest
        )
        sidecar_ok = _read_sidecar_hash(spath) == corpus_digest
        if floor_ok and sidecar_ok:
            return ApplyResult(changed=False, detail="floor already at corpus state")

        floor_existed = fpath.exists()
        sidecar_existed = spath.exists()
        fpath.parent.mkdir(parents=True, exist_ok=True)  # the consumer's .claude/
        # render_floor already returns LF-normalized text w/ a single trailing NL;
        # newline="\n" prevents Windows CRLF translation so on-disk bytes match the
        # hash (byte-identical to what generate_floor.py --out-dir would write,
        # minus the hub-SHA refresh this carrier deliberately omits).
        fpath.write_text(floor, encoding="utf-8", newline="\n")
        spath.write_text(f"{corpus_digest}\n", encoding="utf-8", newline="\n")
        changes = (
            f"{'updated' if floor_existed else 'wrote'} {fpath}",
            f"{'updated' if sidecar_existed else 'wrote'} {spath}",
        )
        log.info("floor apply: %s -> %s", fpath, corpus_digest[:12])
        return ApplyResult(
            changed=True, changes=changes, detail=f"floor generated at {corpus_digest[:12]}"
        )

    def verify(self, target: Any) -> VerifyResult:
        # Independent re-hash — does NOT call _classify_floor (D9).
        _, corpus_digest = _corpus_floor()
        failures = _verify_floor(
            corpus_digest, self._floor_path(target), self._sidecar_path(target)
        )
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail="floor at corpus state" if ok else f"{len(failures)} unmet requirement(s)",
        )
