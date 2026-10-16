"""Vendor smoke probe, cached per day, and the VENDOR-FAIL line (AMEND-1 PART V).

A vendor whose probe did not pass TODAY is not routed to, and a vendor that fails a phase is
recorded as `VENDOR-FAIL <vendor> <phase> <error>` -- never replaced silently (the 2026-10-15 BU
lane 1536 implement fell back from Copilot to Sonnet with no record). The served-id probe is
`codespace_parity._probe_one` (reused, not rewritten); Copilot additionally has to READ a staged
file, which is the path the matrix showed `-p` mode denies outside the cwd.
"""
from __future__ import annotations

import json
import os
import secrets
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

#: registry provider -> the CLI that serves it
VENDOR_CLI = {"openai": "codex", "xai": "grok", "copilot-enterprise": "copilot", "anthropic": "claude"}
CACHE_ENV = "VENDOR_PROBE_DIR"


@dataclass(frozen=True)
class ProbeResult:
    vendor: str
    ok: bool
    served: Optional[str]
    error: str


def vendor_fail_line(vendor: str, phase: str, error: str) -> str:
    return f"VENDOR-FAIL {vendor} {phase} {error}"


def served_matches(requested: Optional[str], served: Optional[str]) -> bool:
    """The model the CLI says it served is exactly the one asked for."""
    return bool(requested) and bool(served) and requested == served


def registry_model(vendor: str, role: str = "review") -> Optional[str]:
    import provider_router
    for entry in provider_router.declared_order(role):
        if entry.get("provider") == vendor:
            return entry.get("model")
    return None


def _cache_dir(cache_dir: Optional[Path]) -> Path:
    root = cache_dir or os.environ.get(CACHE_ENV) or Path(tempfile.gettempdir()) / "dev-knowledge-vendor-probe"
    path = Path(root)
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_probe(vendor: str) -> ProbeResult:
    """One real call: the CLI serves the registry's id, and Copilot reads a file staged in its cwd."""
    import codespace_parity as cp
    import run_phase
    cli = VENDOR_CLI.get(vendor)
    model = registry_model(vendor)
    if cli is None or not model:
        return ProbeResult(vendor, False, None, "no CLI or no registry model for this vendor")
    nonce = "CHK-" + secrets.token_hex(4).upper()
    with tempfile.TemporaryDirectory(prefix="vendor-probe-") as tmp:
        record = cp._probe_one(cli, cp.default_run, Path(tmp), cp.ExpectedModel(model, "roles.review"),
                               nonce, Path.home(), 240)
        served = record.get("served_id")
        if record.get("state") != "served":
            return ProbeResult(vendor, False, served, f"{record.get('state')}: {record.get('detail', '')}"[:200])
        if not served_matches(model, served):
            return ProbeResult(vendor, False, served, f"asked {model}, served {served}")
        if cli == "copilot":
            src = Path(tmp) / "outside" / "probe.txt"
            src.parent.mkdir()
            src.write_text(nonce + "\n", encoding="utf-8", newline="\n")
            work = Path(tmp) / "work"
            run_phase.stage_input(src, work)
            res = cp.default_run(["copilot", "-p", "Read probe.txt in the current directory and reply with "
                                  "exactly its contents.", "--model", model, "--allow-all-tools",
                                  "--no-ask-user", "--no-color"], cwd=work, timeout=240)
            if nonce not in (res.stdout or ""):
                return ProbeResult(vendor, False, served, "staged read failed: " + (res.stdout or res.stderr or "")[:120])
    return ProbeResult(vendor, True, served, "")


def probe_today(vendor: str, *, cache_dir: Optional[Path] = None, today: Optional[str] = None,
                probe: Optional[Callable[[str], ProbeResult]] = None,
                model: Optional[str] = None) -> ProbeResult:
    """`vendor`'s probe result for `today`: from the cache when one was recorded today FOR THIS
    VENDOR AND REGISTRY MODEL, else probed and recorded. A cached FAILURE is kept for the day too (a
    vendor is not hammered). A cache entry that names another vendor or model, or cannot be read, is
    a miss; a cache that cannot be written leaves the result uncached -- never an exception, so the
    caller records a VENDOR-FAIL instead of aborting (Codex terra, round 1)."""
    today = today or date.today().isoformat()
    model = model if model is not None else registry_model(vendor)
    try:
        path: Optional[Path] = _cache_dir(cache_dir) / f"{vendor}.json"
    except OSError:
        path = None
    if path is not None:
        try:
            cached = json.loads(path.read_text(encoding="utf-8"))
            hit = ProbeResult(**cached["result"])
            if cached.get("day") == today and cached.get("model") == model and hit.vendor == vendor:
                return hit
        except (OSError, ValueError, KeyError, TypeError):
            pass
    result = (probe or default_probe)(vendor)
    if path is not None:
        tmp = path.with_suffix(f".{secrets.token_hex(3)}.tmp")
        try:
            tmp.write_text(json.dumps({"day": today, "model": model, "result": asdict(result)}),
                           encoding="utf-8", newline="\n")
            os.replace(tmp, path)
        except OSError:
            tmp.unlink(missing_ok=True)
    return result
