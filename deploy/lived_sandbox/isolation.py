"""Lived-workflow sandbox — the ISOLATION PROOF (Slice A; Fable review §6, THE correctness property).

The child MUST run under an isolated CLAUDE_CONFIG_DIR, or the observer measures the workstation
(a facade), not the deployment. This proves it: a uniquely-named SessionStart SENTINEL hook lives
in configA but NOT configB. A child under configB shows the sentinel ABSENT (isolation holds); the
positive control under configA shows it PRESENT (the sentinel is real — and SessionStart hooks DO
fire under `claude -p`). If either leg fails, the caller STOPs and surfaces rather than measure a
facade. The proof is over a MINIMAL empty work dir (no project hooks) so the only variable is the
user-level config the child reads.
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import spawn as _spawn

_PROMPT = "Reply with exactly the single token: OK"


@dataclass
class IsolationResult:
    marker: str
    present_in_configA: bool   # positive control — MUST be True
    absent_in_configB: bool    # isolation — MUST be True
    exitA: int
    exitB: int
    transcriptA: Path | None
    transcriptB: Path | None
    tempdir: Path

    @property
    def passed(self) -> bool:
        # Both legs must hold AND both child runs must have SUCCEEDED (exit 0). A failed child
        # whose SessionStart hook fired before the failure could otherwise fake a green — a
        # false-green isolation proof is exactly the facade this must never measure (Codex
        # CRITICAL 2026-07-04; Fable §6 "if isolation can't be proven cleanly, STOP").
        return (self.exitA == 0 and self.exitB == 0
                and self.present_in_configA and self.absent_in_configB)

    def summary(self) -> str:
        verdict = "PROVEN" if self.passed else "FAILED"
        clean = "" if (self.exitA == 0 and self.exitB == 0) else " [child run FAILED — not a clean proof]"
        return (f"isolation {verdict}{clean}: sentinel '{self.marker}' "
                f"present-in-configA={self.present_in_configA} (positive control, exit {self.exitA}) / "
                f"absent-in-configB={self.absent_in_configB} (isolation, exit {self.exitB})")


def prove_isolation(marker: str = "LSANDBOX_SENTINEL", *, api_key: str | None = None,
                    model: str = _spawn.DEFAULT_MODEL, keep: bool = False,
                    tempdir: Path | None = None) -> IsolationResult:
    """Run the two-config isolation proof. Returns an IsolationResult; does NOT raise on a FAILED
    proof (the caller decides to STOP + surface). Raises SandboxError only on a spawn precondition
    (e.g. no auth). `keep=True` leaves the temp dir (with transcripts) so the caller can freeze the
    fixture before tearing it down via `spawn.teardown(result.tempdir)`.
    """
    key = api_key or _spawn.load_api_key()
    root = Path(tempdir) if tempdir else Path(tempfile.mkdtemp(prefix="lived-sandbox-iso-"))
    root.mkdir(parents=True, exist_ok=True)
    try:
        cfgA = _spawn.write_isolated_config(root / "cfgA", session_start_marker=marker)
        cfgB = _spawn.write_isolated_config(root / "cfgB")  # no sentinel
        rA = _spawn.spawn(root / "workA", _PROMPT, config_dir=cfgA, api_key=key, model=model)
        rB = _spawn.spawn(root / "workB", _PROMPT, config_dir=cfgB, api_key=key, model=model)
        result = IsolationResult(
            marker=marker,
            present_in_configA=rA.contains(marker),
            absent_in_configB=not rB.contains(marker),
            exitA=rA.exit_code, exitB=rB.exit_code,
            transcriptA=rA.transcript_path, transcriptB=rB.transcript_path,
            tempdir=root,
        )
    except BaseException:
        _spawn.teardown(root)
        raise
    if not keep:
        _spawn.teardown(root)
    return result
