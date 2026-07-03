"""deploy/carrier_mesh.py — the enforcement-mesh carrier (Axis-1 enforcement transfer, #236).

Deploys the two portable/ported fail-closed organs INTO a consumer repo so they fire
enforcing-local (on the consumer's OWN actions), with hub-parity logged-override. Fable-consult
mesh model D (deploy-into-consumer): the fire_test clones the consumer in isolation, so every
script an organ's hook invokes must physically live in the consumer tree — hence the code is
deployed, not called-from-hub.

Artifacts this carrier writes/stages into the consumer (ADR-92 write-yes / commit-no):

1. ``scripts/session_end_backpressure.py`` — the #237-ported organ (git-toplevel-first root),
   byte-copied from the hub. Fires as a ``.claude/settings.json`` Stop hook (below).
2. ``scripts/canonical_freshness_gate.py`` — the single-sourced freshness gate, byte-copied from
   the hub. Wired as a pre-commit hook by the **precommit carrier** (single-writer of
   ``.pre-commit-config.yaml``), NOT here (arming spans two carriers — the ADR-93 precedent).
3. ``.claude/commands/override.md`` — the hub ``/override`` command, verbatim (repo-agnostic:
   relative ``logs/`` paths + ``git rev-parse HEAD`` on cwd). Restores seb's ONLY escape hatch —
   ``git commit --no-verify`` does NOT bypass a Stop hook, so without ``/override`` seb-in-consumer
   would be stricter than the hub. Hub-parity requires it.
4. ``.claude/settings.json`` — a ``Stop`` hook running seb (merged; coexists with the tier1 plugin
   propose-closures Stop hook exactly as the hub does; the Informant's locate excludes propose).
5. ``logs/.gitkeep`` — so ``logs/`` exists for the ``/override`` command's ``Set-Content logs/…``
   (which does not mkdir). ``logs/`` is tracked; only the two ephemeral token files are gitignored.
6. ``.gitignore`` — a DISTINCT sentinel-delimited block ignoring ``logs/.session-override-token`` +
   ``logs/OVERRIDES.md``. The floor carrier owns the ``.claude/*`` block; this carrier owns ONLY its
   own sentinel-delimited region (single-writer-per-REGION — no concurrent-write hazard).

Three contract states (script content-mismatch is drift, not a version anchor — the manifest
rev-pin on the precommit carrier is the version surface, so no PRESENT_WRONG_VERSION): ``ABSENT``
(nothing deployed), ``PRESENT_CORRECT`` (all six artifacts present + correct + the Stop hook wired),
``PRESENT_DRIFTED`` (some present, some missing/wrong).

D9 (ADR-92 Decision 9): ``_classify_mesh`` (detect) and ``_verify_mesh`` (verify) are distinct
functions with no shared correctness-judgment helper; the byte reads / settings parse are shared
SPEC reads (D9-permitted).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

_HUB_ROOT = Path(__file__).resolve().parent.parent

log = logging.getLogger(__name__)

CARRIER_ID = "enforcement-mesh"

# Hub source bytes (read at deploy time from the tagged hub — "deploy vX uses vX", ADR-92).
_HUB_SEB = _HUB_ROOT / "scripts" / "session_end_backpressure.py"
_HUB_FRESHNESS_GATE = _HUB_ROOT / "scripts" / "canonical_freshness_gate.py"
_HUB_OVERRIDE_CMD = _HUB_ROOT / ".claude" / "commands" / "override.md"

# Consumer-root-relative destinations.
SEB_REL = "scripts/session_end_backpressure.py"
FRESHNESS_GATE_REL = "scripts/canonical_freshness_gate.py"
OVERRIDE_CMD_REL = ".claude/commands/override.md"
SETTINGS_REL = ".claude/settings.json"
GITIGNORE_REL = ".gitignore"
GITKEEP_REL = "logs/.gitkeep"

# The Stop hook that fires seb. Mirrors the hub shape: the Informant's locate scans Stop commands
# for this token, and its fire _resolve_script expands $CLAUDE_PROJECT_DIR + takes the .py token,
# so the script resolves INSIDE the clone. Must contain "session_end_backpressure" (locate) and
# not "propose_closures" (locate excludes the plugin's Stop hook).
_STOP_COMMAND = 'python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'
_STOP_SENTINEL = "session_end_backpressure"

# The DISTINCT, sentinel-delimited .gitignore region this carrier owns (never the floor's block).
_GITIGNORE_BEGIN = "# >>> enforcement-mesh: override-token (ADR-85 /override; ephemeral) >>>"
_GITIGNORE_END = "# <<< enforcement-mesh: override-token <<<"
_GITIGNORE_ENTRIES = ("logs/.session-override-token", "logs/OVERRIDES.md")
_GITIGNORE_BLOCK = (_GITIGNORE_BEGIN, *_GITIGNORE_ENTRIES, _GITIGNORE_END)


# ---------------------------------------------------------------------------
# Shared SPEC reads / parsers (D9-permitted — no state judgment here).
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """LF-normalize so a Windows checkout can't flip a byte-clean match to a miss."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _hub_bytes(path: Path) -> str:
    return _normalize(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return _normalize(path.read_text(encoding="utf-8")) if path.exists() else ""


def _load_settings(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    data = json.loads(raw)
    return data if isinstance(data, dict) else {}


def _stop_commands(data: dict[str, Any]) -> list[str]:
    cmds: list[str] = []
    for group in (data.get("hooks", {}) or {}).get("Stop", []) or []:
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []) or []:
            if isinstance(hook, dict) and isinstance(hook.get("command"), str):
                cmds.append(hook["command"])
    return cmds


def _stop_hook_wired(settings_path: Path) -> bool:
    return any(_STOP_SENTINEL in c for c in _stop_commands(_load_settings(settings_path)))


def _gitignore_block_present(path: Path) -> bool:
    lines = [ln.strip() for ln in _read_text(path).splitlines()]
    return all(entry in lines for entry in _GITIGNORE_ENTRIES)


# ---------------------------------------------------------------------------
# detect — _classify_mesh (detect's OWN judgment; D9).
# ---------------------------------------------------------------------------


def _file_correct(dest: Path, src: Path) -> bool:
    return _read_text(dest) == _hub_bytes(src)


def _classify_mesh(root: Path) -> CarrierState:
    seb_ok = _file_correct(root / SEB_REL, _HUB_SEB)
    gate_ok = _file_correct(root / FRESHNESS_GATE_REL, _HUB_FRESHNESS_GATE)
    override_ok = _file_correct(root / OVERRIDE_CMD_REL, _HUB_OVERRIDE_CMD)
    stop_ok = _stop_hook_wired(root / SETTINGS_REL)
    gitkeep_ok = (root / GITKEEP_REL).exists()
    gitignore_ok = _gitignore_block_present(root / GITIGNORE_REL)

    nothing = (
        not (root / SEB_REL).exists()
        and not (root / FRESHNESS_GATE_REL).exists()
        and not (root / OVERRIDE_CMD_REL).exists()
        and not stop_ok
    )
    if nothing:
        return CarrierState.ABSENT
    if seb_ok and gate_ok and override_ok and stop_ok and gitkeep_ok and gitignore_ok:
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_DRIFTED


# ---------------------------------------------------------------------------
# verify — INDEPENDENT of detect (D9). Own re-reads, own checks.
# ---------------------------------------------------------------------------


def _verify_mesh(root: Path) -> list[str]:
    failures: list[str] = []
    for rel, src in ((SEB_REL, _HUB_SEB), (FRESHNESS_GATE_REL, _HUB_FRESHNESS_GATE),
                     (OVERRIDE_CMD_REL, _HUB_OVERRIDE_CMD)):
        dest = root / rel
        if not dest.exists():
            failures.append(f"missing: {rel}")
        elif _read_text(dest) != _hub_bytes(src):
            failures.append(f"content drift vs hub: {rel}")
    if not _stop_hook_wired(root / SETTINGS_REL):
        failures.append(f"settings.json has no seb Stop hook (token {_STOP_SENTINEL!r})")
    if not (root / GITKEEP_REL).exists():
        failures.append(f"missing: {GITKEEP_REL} (logs/ dir for the override token)")
    gi = [ln.strip() for ln in _read_text(root / GITIGNORE_REL).splitlines()]
    if any(entry not in gi for entry in _GITIGNORE_ENTRIES):
        failures.append(".gitignore missing the override-token block")
    return failures


# ---------------------------------------------------------------------------
# apply — idempotent per-artifact ensures. Writes/stages only (commit-no).
# ---------------------------------------------------------------------------


def _write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _ensure_file(dest: Path, src: Path) -> str | None:
    desired = _hub_bytes(src)
    if _read_text(dest) == desired:
        return None
    existed = dest.exists()
    _write_lf(dest, desired)
    return f"{'updated' if existed else 'wrote'} {dest.name}"


def _ensure_gitkeep(path: Path) -> str | None:
    if path.exists():
        return None
    _write_lf(path, "")
    return f"wrote {path}"


def _ensure_stop_hook(path: Path) -> str | None:
    data = _load_settings(path)
    if any(_STOP_SENTINEL in c for c in _stop_commands(data)):
        return None
    existed = path.exists()
    hooks = data.setdefault("hooks", {})
    stop = hooks.setdefault("Stop", [])
    stop.append({
        "matcher": "",
        "hooks": [{"type": "command", "command": _STOP_COMMAND, "timeout": 15}],
    })
    _write_lf(path, json.dumps(data, indent=2) + "\n")
    return f"{'updated' if existed else 'wrote'} {path.name} (seb Stop hook)"


def _ensure_gitignore(path: Path) -> str | None:
    lines = _read_text(path).splitlines()
    stripped = [ln.strip() for ln in lines]
    if all(entry in stripped for entry in _GITIGNORE_ENTRIES):
        return None
    existed = path.exists()
    # Append the whole sentinel-delimited block (only when incomplete; idempotent on entries).
    body = "\n".join(lines).rstrip("\n")
    block = "\n".join(_GITIGNORE_BLOCK)
    new = (body + "\n\n" + block + "\n") if body else (block + "\n")
    _write_lf(path, new)
    return f"{'updated' if existed else 'wrote'} {path.name} (override-token block)"


class MeshCarrier(Carrier):
    """Enforcement-mesh carrier — bound to one consumer repo."""

    carrier_id = CARRIER_ID

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    def detect(self, target: Any) -> CarrierState:
        state = _classify_mesh(self.repo_root)
        log.debug("mesh detect: %s -> %s", self.repo_root, state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        changes: list[str] = []
        for change in (
            _ensure_file(self.repo_root / SEB_REL, _HUB_SEB),
            _ensure_file(self.repo_root / FRESHNESS_GATE_REL, _HUB_FRESHNESS_GATE),
            _ensure_file(self.repo_root / OVERRIDE_CMD_REL, _HUB_OVERRIDE_CMD),
            _ensure_stop_hook(self.repo_root / SETTINGS_REL),
            _ensure_gitkeep(self.repo_root / GITKEEP_REL),
            _ensure_gitignore(self.repo_root / GITIGNORE_REL),
        ):
            if change is not None:
                changes.append(change)
        if not changes:
            return ApplyResult(changed=False, detail="enforcement-mesh already deployed")
        log.info("mesh apply: %s -> %d change(s)", self.repo_root, len(changes))
        return ApplyResult(changed=True, changes=tuple(changes),
                           detail=f"enforcement-mesh deployed ({len(changes)} change(s))")

    def verify(self, target: Any) -> VerifyResult:
        failures = _verify_mesh(self.repo_root)  # independent of detect (D9)
        ok = not failures
        return VerifyResult(ok=ok, failures=tuple(failures),
                            detail="enforcement-mesh deployed + wired" if ok
                            else f"{len(failures)} unmet requirement(s)")
