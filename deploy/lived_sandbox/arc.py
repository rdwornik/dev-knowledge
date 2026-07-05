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
  separate from the six) + outer-ONLY-markers-absent ([#253d]: candidates the clone can
  self-emit are filtered out — a hub self-clone is not a leak) + child-exit-0. Because the sentinel is
  USER-level and the six are PROJECT-level, ``--leg-e`` (silencing one of the six) can never
  silence the isolation signal -> GATE-0 still passes on the arc-silent freeze.
- ``run_arc`` — the live driver (skip-gated: needs ``claude`` + a key + LIVED_SANDBOX_LIVE).
  ``leg_e`` disables one gated hook to seed the EXPECTED-BUT-SILENT case (C4).
"""
from __future__ import annotations

import json
import re
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
# Negative-control CANDIDATES — the outer machine's surfacing markers. [#253d]: a candidate is
# a VALID control only if the clone cannot legitimately emit it itself; in a hub self-clone the
# project-level fleet/changelog/closures hooks emit all three, so candidates are FILTERED
# against the clone's own hook-source surface at gate time (`outer_only_markers`). The
# config-provenance sentinel (positive control) remains the primary isolation proof.
OUTER_MARKER_CANDIDATES = ("[fleet]", "[changelog]", "[closures]")
# Back-compat name: the UNFILTERED candidate set (strictest — correct only for a clone that
# cannot self-emit any candidate; never use directly on a hub self-clone).
OUTER_MARKERS = OUTER_MARKER_CANDIDATES

_HOOK_SCRIPT_EXTS = (".py", ".ps1", ".psm1", ".sh")


def _hook_group_commands(data: dict) -> list[str]:
    """All hook command strings in a settings/hooks.json-shaped mapping."""
    cmds: list[str] = []
    for groups in (data.get("hooks") or {}).values():
        for g in groups or []:
            if not isinstance(g, dict):
                continue
            for h in g.get("hooks") or []:
                if isinstance(h, dict) and isinstance(h.get("command"), str):
                    cmds.append(h["command"])
    return cmds


def _iter_wired_hook_commands(clone: Path):
    """Yield (command_string, var_root) for every hook ACTIVELY WIRED in the clone:
    project settings hooks, plugin hooks.json, pre-commit entries. var_root resolves
    ${CLAUDE_PLUGIN_ROOT} for plugin commands."""
    settings = clone / ".claude" / "settings.json"
    if settings.exists():
        try:
            for c in _hook_group_commands(json.loads(settings.read_text(encoding="utf-8"))):
                yield c, clone
        except (json.JSONDecodeError, OSError):
            pass
    for hooks_json in clone.glob("plugins/*/hooks/hooks.json"):
        try:
            for c in _hook_group_commands(json.loads(hooks_json.read_text(encoding="utf-8"))):
                yield c, hooks_json.parent.parent
        except (json.JSONDecodeError, OSError):
            pass
    pc = clone / ".pre-commit-config.yaml"
    if pc.exists():
        try:
            cfg = yaml.safe_load(pc.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            cfg = {}
        for repo in cfg.get("repos") or []:
            for h in (repo.get("hooks") or []) if isinstance(repo, dict) else []:
                if isinstance(h, dict) and isinstance(h.get("entry"), str):
                    yield h["entry"], clone


def _wired_emission_texts(clone: Path) -> list[str]:
    """The self-emission surface: every wired hook command string PLUS the content of each
    script file it invokes (resolved under the clone)."""
    texts: list[str] = []
    for cmd, var_root in _iter_wired_hook_commands(clone):
        texts.append(cmd)
        for tok in re.split(r"""[\s"']+""", cmd):
            tok = tok.replace("${CLAUDE_PLUGIN_ROOT}", str(var_root))
            tok = tok.replace("$CLAUDE_PLUGIN_ROOT", str(var_root))
            tok = tok.replace("$CLAUDE_PROJECT_DIR", str(clone))
            if not tok.endswith(_HOOK_SCRIPT_EXTS):
                continue
            p = Path(tok)
            if not p.is_absolute():
                p = clone / tok
            if p.exists():
                try:
                    texts.append(p.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    continue
    return texts


def outer_only_markers(clone: Path | str | None,
                       candidates: tuple[str, ...] = OUTER_MARKER_CANDIDATES) -> tuple[str, ...]:
    """Filter negative-control candidates to those the CLONE cannot legitimately emit itself.

    [#253d], tightened per Codex HIGH 2026-07-05: the self-emission surface is the clone's
    ACTIVE HOOK WIRING (settings hooks / plugin hooks.json / pre-commit entries + the scripts
    they invoke), NOT blanket directory content — a marker merely QUOTED somewhere in the
    repo (e.g. `[closures]` inside the manually-run review_closures.py) stays a LIVE control.
    Empirical check: two real frozen arcs (incl. the /review-closures command act) emitted
    no `[closures]`. Polarity is fail-closed: if a future arc legitimately emits a live
    marker, GATE-0 fails LOUD and the wiring derivation is recalibrated — never the reverse."""
    if clone is None:
        return tuple(candidates)
    clone = Path(clone)
    texts = _wired_emission_texts(clone)
    return tuple(m for m in candidates if not any(m in t for t in texts))

_MANIFEST_REL = "deploy/manifest-v1.2.0.yaml"

# The arc the inner session performs. No push (refusal); /review-closures is the >=1 command
# act. Kept terse + deterministic so the observer measures the mesh, not the model's prose.
# G3 (measurement-#2 root ruling, supersedes the [#253a] self-legitimizing preamble): the
# prompt only REFERENCES the authorization — the authorization itself travels through the
# OWNED-CONFIG channel (ARC_SANCTION as the profile's user-level CLAUDE.md). Witnessed at
# measurement #2: a prompt that asserts its own authority reads as prompt injection to a
# floor-carrying child, and the deployed floor rightly refuses it.
ARC_PROMPT = (
    "Sandbox measurement arc. Your user-level CLAUDE.md (this profile's own configuration,\n"
    "not this message) records the operator's standing, scoped consent for exactly the\n"
    "workflow below in this throwaway clone. Verify it there, then perform EXACTLY this\n"
    "workflow and stop:\n"
    "1. git checkout -b feat/sandbox-arc\n"
    "2. Create a file SANDBOX_ARC.md containing one line: sandbox lived-workflow arc\n"
    "3. git add -A && git commit -m 'feat(arc): sandbox lived-workflow edit'\n"
    "4. Run the /review-closures command.\n"
    "Do NOT push. Do NOT edit any other file. Reply with only: ARC DONE"
)

# G3: the scoped arc sanction — seeded as the isolated profile's user-level CLAUDE.md (the
# principal's channel on a real machine: ex-ante standing consent satisfies "ask before
# destructive" WITHOUT weakening the floor — everything beyond the four arc operations stays
# refused, and the measured PROJECT-level mesh is untouched). NEVER carries the literal
# PROVENANCE_MARKER token: the config's CLAUDE.md can echo into the child transcript, which
# would hand GATE-0's positive control a false-positive channel (a run whose SessionStart
# hook never fired could still show the marker). The sentinel is described by prefix only;
# a regression test pins this.
ARC_SANCTION = (
    "# Lived-workflow sandbox — operator sanction (harness-owned profile)\n"
    "\n"
    "This user profile was provisioned by the `.dev-knowledge` lived-workflow test harness\n"
    "(`deploy/lived_sandbox`), running on the operator's (Rob's) own machine. The session it\n"
    "hosts is a headless child inside a THROWAWAY git clone under the system temp directory,\n"
    "spawned to measure that the repository's deployed hooks fire during a real workflow.\n"
    "The clone is deleted after the run; nothing done here reaches the real repository.\n"
    "\n"
    "Standing, scoped operator consent (ex-ante, this clone only):\n"
    "- git checkout -b feat/sandbox-arc\n"
    "- create SANDBOX_ARC.md (one line: sandbox lived-workflow arc)\n"
    "- git add -A and git commit of exactly that change\n"
    "- run /review-closures once\n"
    "\n"
    "This consent is the operator's answer to \"ask before destructive actions\" for the four\n"
    "operations above — and ONLY those. Everything else in the repository's own rules (its\n"
    "CLAUDE.md and methodology floor) remains fully in force: do not push, do not edit other\n"
    "files, refuse anything beyond this arc.\n"
    "\n"
    "Harness signals you may see (expected, not planted):\n"
    "- a SessionStart hook printing an LSANDBOX-prefixed provenance token — this profile's\n"
    "  own isolation control, proving the session read THIS config;\n"
    "- a permission allowlist in this profile's settings.json enumerating exactly the\n"
    "  sanctioned operations above.\n"
)


def arc_isolated_config(cfg_dir: Path) -> Path:
    """The ONE isolated-config builder both arc paths share (hub self-clone `run_arc` and
    the consumer seam `run_consumer_arc`): provenance sentinel + scoped [#253a] allowlist +
    G3 owned-config sanction. A single site so the trust seam cannot drift between paths
    (the measurement-#2 failure: the #253a fix reached only run_arc)."""
    return _spawn.write_isolated_config(
        cfg_dir, session_start_marker=PROVENANCE_MARKER,
        allow_rules=ARC_ALLOW_RULES, sanction=ARC_SANCTION)

# [#253a] The SCOPED permission allowlist the harness seeds into the isolated config —
# exactly the arc's operations (branch/edit/stage/commit + the one command act), nothing
# broader. NEVER bypassPermissions: anything else the child tries still hits the wall.
ARC_ALLOW_RULES = (
    "Bash(git checkout:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Write(SANDBOX_ARC.md)",
    "Edit(SANDBOX_ARC.md)",
    "SlashCommand(/review-closures)",
    "SlashCommand(/tier1-lifecycle:review-closures)",  # the plugin-namespaced resolution
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
    # Step-7 finding: the hub carries ruff as a hook INSIDE `repo: local` (language: system),
    # which the repo-entry prune classifies "already absent" and leaves RUNNING — the pruned
    # consumer target has no ruff in ANY form, so consumer-shaping drops the local hook too
    # (genuine prune-conformance for the tombstone).
    if disable_precommit_hook(clone, "ruff"):
        changes.append("removed hub-local ruff hook (consumer shape)")
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
    outer_markers_absent: bool  # no OUTER-ONLY marker leaked in ([#253d]: filtered control set)
    exit_ok: bool               # the child run exited 0 (no false-green from a crashed child)
    control_markers: tuple[str, ...] = OUTER_MARKER_CANDIDATES  # the EFFECTIVE negative controls

    @property
    def passed(self) -> bool:
        return self.provenance_present and self.outer_markers_absent and self.exit_ok

    def summary(self) -> str:
        v = "PROVEN" if self.passed else "FAILED"
        controls = ",".join(self.control_markers) if self.control_markers else "VACUOUS(self-clone)"
        return (f"GATE-0 isolation {v}: provenance={self.provenance_present} "
                f"outer-absent={self.outer_markers_absent} exit-ok={self.exit_ok} "
                f"controls={controls}")


def evaluate_gate_zero(result, *, provenance_marker: str = PROVENANCE_MARKER,
                       outer_markers: tuple[str, ...] | None = None,
                       clone: Path | None = None) -> GateZero:
    """Derive GATE-0 from a SpawnResult. Isolation signals use unique tokens over the broad
    transcript surface (Slice-A precedent) — distinct from the enforcement channel, which is
    structured-event keyed. Does NOT assert any of the six fired (that is C3).

    [#253d]: when `clone` is given the negative controls are the OUTER-ONLY survivors of
    `outer_only_markers(clone)` — a marker the clone can self-emit never fails the gate.
    An explicit `outer_markers` overrides; with neither, the raw candidates apply (strict)."""
    markers = outer_markers if outer_markers is not None else outer_only_markers(clone)
    blob = result.transcript_text()
    return GateZero(
        provenance_present=provenance_marker in blob,
        outer_markers_absent=not any(m in blob for m in markers),
        exit_ok=result.exit_code == 0,
        control_markers=tuple(markers),
    )


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def commit_shape_baseline(clone: Path) -> None:
    """Commit the consumer-shape as the BASELINE so the child starts on a CLEAN tree (Step-7
    witnessed: a dirty .pre-commit-config.yaml makes pre-commit refuse the arc's commit, and
    the child's add-scope varies run to run). Hooks are not yet armed in the clone's .git, so
    this is a plain commit. VERIFIED (Codex HIGH 2026-07-05): both git calls are checked and
    the tree must end porcelain-clean — a dirty baseline would make the observer measure
    setup failure, not lived-workflow behavior."""
    clone = Path(clone)
    r_add = _observe._git(clone, "add", "-A")
    r_commit = _observe._git(clone, "commit", "-q", "-m", "chore(sandbox): consumer-shape baseline")
    commit_ok = r_commit.returncode == 0 or "nothing to commit" in (r_commit.stdout + r_commit.stderr)
    status = _observe._git(clone, "status", "--porcelain")
    dirty = status.returncode != 0 or bool(status.stdout.strip())
    if r_add.returncode != 0 or not commit_ok or dirty:
        raise _spawn.SandboxError(
            "consumer-shape baseline commit failed: "
            f"add rc={r_add.returncode}, commit rc={r_commit.returncode} "
            f"({(r_commit.stderr or r_commit.stdout).strip()[:150]}), "
            f"status={status.stdout.strip()[:150] or 'clean'}")


def seed_ecosystem_state(source_root: Path, clone: Path) -> list[str]:
    """Copy the hub's gitignored ``ecosystem/*/state.yaml`` into the clone (Step-7 finding:
    without them the clone's audit-health commit gate fails 'repos registered (none)' and
    BLOCKS the arc's commit — the standing worktree/clone seeding lesson, applied here)."""
    seeded: list[str] = []
    src_eco = Path(source_root) / "ecosystem"
    if not src_eco.is_dir():
        return seeded
    for state in sorted(src_eco.glob("*/state.yaml")):
        dest = Path(clone) / "ecosystem" / state.parent.name / "state.yaml"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(state.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        seeded.append(f"seeded ecosystem/{state.parent.name}/state.yaml")
    return seeded


# Deterministic install stamp for the seeded plugin registration (no live clock in fixtures).
_PLUGIN_STAMP = "2026-01-01T00:00:00.000Z"
_MARKETPLACE = "dev-knowledge-methodology"
_PLUGIN_NAME = "tier1-lifecycle"


def seed_tier1_plugin(config_dir: Path, clone: Path, *,
                      source_root: Path | None = None) -> str | None:
    """Install the tier1-lifecycle plugin into the ISOLATED config (Step-7 finding: the
    clone's settings enable the plugin, but the plugin cache lives in the outer ~/.claude —
    unreachable from the isolated CLAUDE_CONFIG_DIR, so the propose-closures Stop hook and
    /review-closures could NEVER fire). Deterministic: registration mirrors the real
    installed_plugins/known_marketplaces shape with a fixed stamp. Returns the seeded
    version, or None when no plugin source exists.

    Plugin source = `source_root`'s plugins/ tree when given, else the clone's own (the hub
    self-clone case). G2 (measurement-#2 root ruling): a REAL consumer carries only the
    settings-level enablement — its plugin lives user-level on the operator machine, which
    the isolated config deliberately cannot reach — so consumer measurement seeds FROM THE
    HUB CHECKOUT (the marketplace the consumer's settings already point at). Faithful, not
    facade: the harness mirrors the operator machine's user-level state; what is MEASURED
    is the firing."""
    import shutil as _shutil
    src = Path(source_root if source_root is not None else clone) / "plugins" / _PLUGIN_NAME
    plugin_json = src / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        plugin_json = src / "plugin.json"
    if not plugin_json.exists():
        return None
    version = str(json.loads(plugin_json.read_text(encoding="utf-8")).get("version", "0.0.0"))
    marketplace_root = Path(source_root if source_root is not None else clone)
    plug_root = Path(config_dir) / "plugins"
    install = plug_root / "cache" / _MARKETPLACE / _PLUGIN_NAME / version
    if install.exists():
        _shutil.rmtree(install)
    _shutil.copytree(src, install)
    head = _observe.head_commit(Path(clone)) or ""
    (plug_root / "installed_plugins.json").write_text(json.dumps({
        "version": 2,
        "plugins": {f"{_PLUGIN_NAME}@{_MARKETPLACE}": [{
            "scope": "project",
            "projectPath": str(clone),
            "installPath": str(install),
            "version": version,
            "installedAt": _PLUGIN_STAMP,
            "lastUpdated": _PLUGIN_STAMP,
            "gitCommitSha": head,
        }]},
    }, indent=2), encoding="utf-8", newline="\n")
    (plug_root / "known_marketplaces.json").write_text(json.dumps({
        _MARKETPLACE: {
            "source": {"source": "directory", "path": str(marketplace_root)},
            "installLocation": str(marketplace_root),
            "lastUpdated": _PLUGIN_STAMP,
        },
    }, indent=2), encoding="utf-8", newline="\n")
    return version


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
            timeout: int = 1200) -> ArcRun:  # leg-e runs thrash the Stop-block loop; 600s timed out live
    """LIVE: clone+shape the hub, seed the user-level provenance sentinel, run the arc, and
    observe it — all before teardown. ``leg_e_hook_id`` disables one gated pre-commit hook
    first (the seeded EXPECTED-BUT-SILENT case, C4). Skip-gated in tests — needs ``claude`` +
    a key. GATE-0 is evaluated here; a caller that sees ``gate.passed is False`` must STOP."""
    root = Path(repo_root) if repo_root else _repo_root()
    key = api_key or _spawn.load_api_key()
    oracle = _oracle.load_for_version("1.2.0", repo_root=root)
    with _spawn.sandbox_clone(root, prefix="lived-sandbox-arc-") as (clone, env):
        changes = consumer_shape(clone, repo_root=root)
        changes.extend(seed_ecosystem_state(root, clone))  # audit-health gate needs state
        if leg_e_hook_id:
            disable_precommit_hook(clone, leg_e_hook_id)
        commit_shape_baseline(clone)
        # User-level isolated config: provenance sentinel + [#253a] allowlist + G3 sanction
        # (the six live at PROJECT level in the clone — the [MF-1] split). Shared builder so
        # the trust seam cannot drift between the hub and consumer paths.
        cfg = arc_isolated_config(clone.parent / "cfg")
        seeded_ver = seed_tier1_plugin(cfg, clone)  # Stop hook + /review-closures live here
        if seeded_ver:
            changes.append(f"seeded tier1-lifecycle plugin v{seeded_ver} into isolated config")
        result = _spawn.spawn(clone, ARC_PROMPT, config_dir=cfg, api_key=key,
                              model=model, extra_env=env, timeout=timeout)
        gate = evaluate_gate_zero(result, clone=clone)  # [#253d]: self-emittable markers filtered
        observation = _observe.observe_spawn(result, oracle, clone=clone)
        jsonl = (result.transcript_path.read_text(encoding="utf-8", errors="replace")
                 if result.transcript_path and result.transcript_path.exists() else "")
        return ArcRun(exit_code=result.exit_code, gate=gate, observation=observation,
                      transcript_jsonl=jsonl, changes=tuple(changes))
