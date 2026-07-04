"""Lived-workflow sandbox — the SIX-HOOK ARC driver + GATE-0 (Slice B; [#252]).

Drives a REAL headless ``claude -p`` session through ``branch -> edit -> commit -> wrap``
inside a consumer-shaped clone, so the deployed mesh's hooks fire and the observer can
measure enforcement-in-effect. Three parts, deterministic-first:

- ``consumer_shape`` — clone the hub (``spawn.sandbox_clone``), reconcile to the v1.2.0
  consumer target with the REPO-SCOPED carriers only (precommit PRUNES ruff -> genuine
  prune-conformance + pins hub_hooks; floor + mesh idempotent). Skips global-config
  (~/.codex) and the tier1-plugin marketplace install ([MC-3]: all three are clone-rooted).
- ``evaluate_gate_zero`` — **[MF-1] isolation-ONLY**, decoupled from hook-completeness
  (that is C3, the observer's job). config-provenance (a DEDICATED user-level sentinel,
  separate from the six) + outer-L0-markers-absent + child-exit-0. Because the sentinel is
  USER-level and the six are PROJECT-level, ``--leg-e`` (silencing one of the six) can never
  silence the isolation signal -> GATE-0 still passes on the arc-silent freeze.
- ``run_arc`` — the live driver (skip-gated: needs ``claude`` + a key + LIVED_SANDBOX_LIVE).
  ``leg_e`` disables one gated hook to seed the EXPECTED-BUT-SILENT case (C4).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import observe as _observe
from . import oracle as _oracle
from . import spawn as _spawn

# Reuse the repo-scoped carriers (deploy/ is on sys.path via spawn.py's shim).
_DEPLOY = Path(__file__).resolve().parent.parent
if str(_DEPLOY) not in sys.path:
    sys.path.insert(0, str(_DEPLOY))
from carrier_floor import FloorCarrier  # noqa: E402
from carrier_mesh import MeshCarrier  # noqa: E402
from carrier_precommit import PrecommitCarrier  # noqa: E402

# A DEDICATED user-level SessionStart sentinel — the GATE-0 config-provenance signal. Unique
# token: no assistant narration emits it, only the isolated config's hook (so the blob check
# is safe here, unlike the enforcement channel which is structured-event keyed — [NB-2]).
PROVENANCE_MARKER = "LSANDBOX_ARC_PROVENANCE"
# The outer machine's real ~/.claude SessionStart surfacing markers — the negative control.
# If ANY appears in the child transcript, isolation leaked. Broad (blob) check = strictest.
OUTER_MARKERS = ("[fleet]", "[changelog]", "[closures]")

_MANIFEST_REL = "deploy/manifest-v1.2.0.yaml"

# The arc the inner session performs. No push (refusal); /review-closures is the >=1 command
# act. Kept terse + deterministic so the observer measures the mesh, not the model's prose.
ARC_PROMPT = (
    "You are in a throwaway sandbox clone. Perform EXACTLY this workflow, then stop:\n"
    "1. git checkout -b feat/sandbox-arc\n"
    "2. Create a file SANDBOX_ARC.md containing one line: sandbox lived-workflow arc\n"
    "3. git add -A && git commit -m 'feat(arc): sandbox lived-workflow edit'\n"
    "4. Run the /review-closures command.\n"
    "Do NOT push. Do NOT edit any other file. Reply with only: ARC DONE"
)


def _load_spec(repo_root: Path) -> dict:
    return yaml.safe_load((Path(repo_root) / _MANIFEST_REL).read_text(encoding="utf-8"))


def _carrier_target(spec: dict, carrier_id: str) -> dict:
    for c in spec.get("carriers") or []:
        if isinstance(c, dict) and c.get("id") == carrier_id:
            return c.get("target") or {}
    return {}


def _component(spec: dict, component_id: str) -> dict | None:
    for c in spec.get("components") or []:
        if isinstance(c, dict) and c.get("id") == component_id:
            return c
    return None


def consumer_shape(clone: Path, *, repo_root: Path | None = None) -> list[str]:
    """Reconcile a hub clone to the v1.2.0 consumer target with the repo-scoped carriers.

    PRUNES ruff (the real P2 remove-leg -> ruff verifiably ABSENT = prune-conformance),
    pins hub_hooks + local hooks (precommit), and idempotently ensures floor + mesh. Returns
    the flat list of changes. Clone-rooted only ([MC-3]); no ~/.codex or marketplace step.
    """
    clone = Path(clone)
    root = Path(repo_root) if repo_root else _repo_root()
    spec = _load_spec(root)
    changes: list[str] = []

    pre = PrecommitCarrier(clone)
    ruff = _component(spec, "ruff-gate")
    if ruff is not None:
        pr = pre.prune(ruff)
        changes.extend(pr.removed)
        changes.extend(f"REFUSED: {x}" for x in pr.refused)
    changes.extend(pre.apply(_carrier_target(spec, "precommit")).changes)
    changes.extend(FloorCarrier(clone).apply(_carrier_target(spec, "floor")).changes)
    changes.extend(MeshCarrier(clone).apply(_carrier_target(spec, "enforcement-mesh")).changes)
    return changes


def _precommit_config(clone: Path) -> Path:
    return Path(clone) / ".pre-commit-config.yaml"


def disable_precommit_hook(clone: Path, hook_id: str) -> bool:
    """Remove a pre-commit hook by id from the clone's config (the leg-e silencer for a
    pre-commit-stage gated hook). Returns True if a hook was removed. Preserves everything else."""
    path = _precommit_config(clone)
    if not path.exists():
        return False
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    removed = False
    for entry in config.get("repos", []) or []:
        hooks = entry.get("hooks") if isinstance(entry, dict) else None
        if not isinstance(hooks, list):
            continue
        kept = [h for h in hooks if not (isinstance(h, dict) and h.get("id") == hook_id)]
        if len(kept) != len(hooks):
            entry["hooks"] = kept
            removed = True
    if removed:
        path.write_text(
            yaml.safe_dump(config, sort_keys=False, default_flow_style=False, width=4096),
            encoding="utf-8", newline="\n")
    return removed


@dataclass
class GateZero:
    """GATE-0 verdict — ISOLATION-ONLY ([MF-1]), decoupled from hook-completeness (C3).

    A FAILED gate means the observer is NOT trusted (the seam is unproven under real work):
    STOP and surface. Holds on BOTH the arc-green and arc-silent freezes.
    """

    provenance_present: bool   # the dedicated user-level sentinel fired -> child read OUR config
    outer_markers_absent: bool  # the real ~/.claude L0 markers did NOT leak in
    exit_ok: bool               # the child run exited 0 (no false-green from a crashed child)

    @property
    def passed(self) -> bool:
        return self.provenance_present and self.outer_markers_absent and self.exit_ok

    def summary(self) -> str:
        v = "PROVEN" if self.passed else "FAILED"
        return (f"GATE-0 isolation {v}: provenance={self.provenance_present} "
                f"outer-absent={self.outer_markers_absent} exit-ok={self.exit_ok}")


def evaluate_gate_zero(result, *, provenance_marker: str = PROVENANCE_MARKER,
                       outer_markers: tuple[str, ...] = OUTER_MARKERS) -> GateZero:
    """Derive GATE-0 from a SpawnResult. Isolation signals use unique tokens over the broad
    transcript surface (Slice-A precedent) — distinct from the enforcement channel, which is
    structured-event keyed. Does NOT assert any of the six fired (that is C3)."""
    blob = result.transcript_text()
    return GateZero(
        provenance_present=provenance_marker in blob,
        outer_markers_absent=not any(m in blob for m in outer_markers),
        exit_ok=result.exit_code == 0,
    )


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


@dataclass
class ArcRun:
    """The teardown-safe evidence of one live arc — everything is computed INSIDE the clone's
    lifetime (before ``sandbox_clone`` tears the temp root down), so the caller can freeze the
    transcript and read the verdict without a dangling clone reference."""

    exit_code: int
    gate: GateZero
    observation: _observe.ObservationResult
    transcript_jsonl: str   # raw on-disk transcript content, for the CLI to scrub + freeze
    changes: tuple[str, ...]  # consumer_shape changes (incl. the ruff prune)


def run_arc(*, repo_root: Path | None = None, api_key: str | None = None,
            model: str = _spawn.DEFAULT_MODEL, leg_e_hook_id: str | None = None,
            timeout: int = 600) -> ArcRun:
    """LIVE: clone+shape the hub, seed the user-level provenance sentinel, run the arc, and
    observe it — all before teardown. ``leg_e_hook_id`` disables one gated pre-commit hook
    first (the seeded EXPECTED-BUT-SILENT case, C4). Skip-gated in tests — needs ``claude`` +
    a key. GATE-0 is evaluated here; a caller that sees ``gate.passed is False`` must STOP."""
    root = Path(repo_root) if repo_root else _repo_root()
    key = api_key or _spawn.load_api_key()
    oracle = _oracle.load_for_version("1.2.0", repo_root=root)
    with _spawn.sandbox_clone(root, prefix="lived-sandbox-arc-") as (clone, env):
        changes = consumer_shape(clone, repo_root=root)
        if leg_e_hook_id:
            disable_precommit_hook(clone, leg_e_hook_id)
        # User-level isolated config carrying ONLY the provenance sentinel (the six live at
        # PROJECT level in the clone — the [MF-1] split). config_dir under the clone's temp root.
        cfg = _spawn.write_isolated_config(
            clone.parent / "cfg", session_start_marker=PROVENANCE_MARKER)
        result = _spawn.spawn(clone, ARC_PROMPT, config_dir=cfg, api_key=key,
                              model=model, extra_env=env, timeout=timeout)
        gate = evaluate_gate_zero(result)
        observation = _observe.observe_spawn(result, oracle, clone=clone)
        jsonl = (result.transcript_path.read_text(encoding="utf-8", errors="replace")
                 if result.transcript_path and result.transcript_path.exists() else "")
        return ArcRun(exit_code=result.exit_code, gate=gate, observation=observation,
                      transcript_jsonl=jsonl, changes=tuple(changes))
