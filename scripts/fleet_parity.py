#!/usr/bin/env python
"""fleet_parity.py -- the #328 fleet-parity checker (WARN-only v1; FR-3/FR-4/FR-5/FR-6).

Deterministic, READ-ONLY conformance walk of the registered fleet against the versioned
parity manifest ``ecosystem/parity-surfaces.yaml`` (FR-1/FR-2) + the dependency baseline
``ecosystem/dependency-baseline.yaml`` (FR-7, #332). Implements the intake #12 nightly
decision tree per repo x per surface, hub INCLUDED as a fleet member (section 9a):

    surface in template[role]?  -> tier logic (MUST / SHOULD / LOCAL / IGNORE / INVERSE
                                   / TOMBSTONE; fidelity = present != carried)
    not in template?            -> declared in that repo's .methodology.yaml -> OK
                                   -> Tier-4 ephemera tracked -> WARN tracked-ephemera
                                   -> else WARN-undeclared (the anti-regress property)

Verdict vocabulary = the register grammar (fleet-parity register section 9 / FR-14):
``AT-PARITY | PASS-declared | WARN-undeclared | MUST-absent | tombstone-violated`` plus
the extension states ``advisory-rewarn | stale-declaration | refused | unavailable |
skipped-pre-deploy | tracked-ephemera``. Severity labels (info|warn|error) are REPORT
labels only -- the intake #12 severity model rendered honestly; the PROCESS posture is
WARN-only v1 (section 9b, ADR-85 hardening pattern): a completed run ALWAYS exits 0,
is wired into no gate, and is deliberately NOT an ``audit.py`` ``ALL_CHECKS`` member
(``cmd_ship_gate`` REDs on any undispositioned WARN, so battery-wiring would create a
de-facto blocking gate; wiring is a later operator ruling). Exit 2 ONLY when the
manifest itself is unreadable / unparseable -- and then NO digest is written, so a
broken contract can never render as a green "0 findings" (the never-silently-green
rule, Codex FR-12).

Extends -- never duplicates -- the existing machinery (FR-12):
  * ``enforcement_coverage`` is the ``.methodology.yaml`` authority: this module reuses
    ``read_allowlist`` / ``validate_allowlist_entry`` / ``AllowlistEntry`` and the deploy
    manifest waivability policy verbatim. One deliberate semantic FORK, ruled not drifted:
    the Informant's Tier-3 treats ``AL_EXPIRED`` as invalid (-> DRIFT); the #328 section 9b
    ruling makes an expired ``review_date`` an ADVISORY re-WARN here (``advisory-rewarn``,
    PASS-declared lineage). ``validate_allowlist_entry`` itself is untouched.
  * Declaration matching follows the disposition-register grammar: EXACT component-id
    equality only (no substring / prefix / bare-id), one declaration suppresses at most
    ONE concern (``waiver_component`` is unique across manifest rows), a declaration
    matching a surface with no live divergence decorates STALE, and unmapped
    declarations are inert (listed informationally, never a WARN -- consumer files are
    not this checker's to police into churn).
  * Fleet discovery = the committed ``ecosystem/deployed-versions.yaml`` registry keys
    cross-checked against the manifest ``fleet:`` map (mismatch = refusal finding);
    consumer roots resolve override -> ``ecosystem/<name>/state.yaml`` ``path:`` (reusing
    ``fleet_health._load_state_yaml``) -> hub-sibling fallback. The HUB target is always
    THIS checkout's root (worktree-safe; never keyed by directory name).

Probes assert EFFECT where semantics exist (FR-6, the S4 class): ``git check-ignore``
for ignore rules (an inline-commented pattern is textually present and semantically
inert -- a text grep false-passes it), installed+armed hook stages via
``git rev-parse --git-path hooks`` (worktree/hooksPath-safe) with any relic
``core.hooksPath`` recorded, and tag existence + ancestry in the hub repo for pinned
hub-block revs. Working-tree reads by design (bounded, no clones -- AC-7); the
Informant's clone-based fire_test remains the enforcement truth-maker; this checker
covers presence/fidelity/shape, a different axis (FR-9's DID-fire telemetry is a later
phase and is NOT built here).

JSONL events (FR-8/FR-13, CHECKER RUNS ONLY -- organ-wrapper emitters are a later
carrier phase): one schema-versioned line per finding + one run summary, appended to
the gitignored rotation-capped ``logs/parity-events.jsonl``. Emission is FAIL-OPEN in
whole: an emission error prints one ASCII note and never affects verdicts or the exit
code. ``event_id`` is a deterministic content hash (replay-idempotent ingestion,
Codex FR-07); ``mode`` separates ``actual`` from ``synthetic`` so test runs can never
read as fleet history. Non-firing is NOT an event (FR-9 expectation-join, later phase).

Layer-2 posture (ADR-28/36): reads sibling trees read-only; writes ONLY the gitignored
``logs/FLEET-PARITY.md`` digest + ``logs/parity-events.jsonl`` under THIS repo. All
printed output and evidence strings are ASCII (cp1252-safe stdout).
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import click
import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Bare import FIRST so every launch path (pytest sys.path insert, script mode, hook
# mode) resolves ONE module object -- the #153 two-copies gotcha.
try:
    import enforcement_coverage as ec
except ImportError:  # pragma: no cover - package-context fallback
    from scripts import enforcement_coverage as ec
try:
    import fleet_health as fh
except ImportError:  # pragma: no cover
    from scripts import fleet_health as fh

__version__ = "1.0.0"

DEFAULT_MANIFEST = _REPO_ROOT / "ecosystem" / "parity-surfaces.yaml"
DEFAULT_BASELINE = _REPO_ROOT / "ecosystem" / "dependency-baseline.yaml"
DEFAULT_REGISTRY = _REPO_ROOT / "ecosystem" / "deployed-versions.yaml"
DEFAULT_ECOSYSTEM_DIR = _REPO_ROOT / "ecosystem"
DIGEST_PATH = _REPO_ROOT / "logs" / "FLEET-PARITY.md"
EVENTS_PATH = _REPO_ROOT / "logs" / "parity-events.jsonl"
EVENTS_MAX_BYTES = 5_000_000  # rotate past this; single .1 backup (os.replace, Windows-safe)

# Verdict vocabulary (register grammar + extension states).
AT_PARITY = "AT-PARITY"
PASS_DECLARED = "PASS-declared"
WARN_UNDECLARED = "WARN-undeclared"
MUST_ABSENT = "MUST-absent"
TOMBSTONE_VIOLATED = "tombstone-violated"
ADVISORY_REWARN = "advisory-rewarn"
STALE_DECLARATION = "stale-declaration"
REFUSED = "refused"
UNAVAILABLE = "unavailable"
SKIPPED_PRE_DEPLOY = "skipped-pre-deploy"
TRACKED_EPHEMERA = "tracked-ephemera"

SEV_INFO = "info"
SEV_WARN = "warn"
SEV_ERROR = "error"  # REPORT label (intake #12 MUST/INVERSE class); never blocks in v1

TIERS = frozenset({"MUST", "SHOULD", "LOCAL", "IGNORE", "INVERSE", "TOMBSTONE"})
ROLES = frozenset({"hub", "consumer", "pre-deploy"})

# FR-14 register-faithful action hints (FIX-NOW / DECLARE-LOCAL / TICKET / AT-PARITY lineage).
_ACTIONS = {
    AT_PARITY: "-",
    PASS_DECLARED: "-",
    SKIPPED_PRE_DEPLOY: "-",
    WARN_UNDECLARED: "FIX or DECLARE-LOCAL",
    MUST_ABSENT: "FIX-NOW",
    TOMBSTONE_VIOLATED: "FIX or DECLARE-knowingly",
    ADVISORY_REWARN: "RE-REVIEW declaration (expired review_date; section 9b advisory)",
    STALE_DECLARATION: "PRUNE stale declaration",
    REFUSED: "FIX manifest/pointer (refused; no action proposed)",
    UNAVAILABLE: "RESOLVE repo path",
    TRACKED_EPHEMERA: "UNTRACK or DECLARE (Tier-4 ephemera is tracked)",
}


def _ascii(s: str) -> str:
    """Evidence sanitizer: ASCII-only (cp1252 stdout gotcha) + markdown-table-safe."""
    return str(s).encode("ascii", "backslashreplace").decode("ascii").replace("|", "/")


@dataclass(frozen=True)
class RepoTarget:
    repo_id: str
    role: str
    root: Path | None
    note: str = ""


@dataclass(frozen=True)
class ParityFinding:
    repo_id: str
    surface_id: str
    verdict: str
    severity: str
    evidence: str
    action: str = ""
    waiver_component: str | None = None


class ManifestUnreadable(Exception):
    """The parity manifest itself is unusable -- exit-2 class; NO digest is written."""


# ---------------------------------------------------------------------------
# Loaders + validation (refusal findings, never guesses).
# ---------------------------------------------------------------------------


def _refusal(surface_id: str, reason: str) -> ParityFinding:
    return ParityFinding("-", surface_id, REFUSED, SEV_WARN, _ascii(reason),
                         _ACTIONS[REFUSED])


# Required probe params per type -- validated at load so a malformed row REFUSES
# instead of crashing the facts collector (codex code-review 2026-07-13).
_PROBE_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "path_tracked": ("path",), "dir_tracked": ("path",), "dir_exists": ("path",),
    "file_exists": ("path",), "file_contains": ("path", "token"),
    "glob_tracked": ("glob",), "command_present": ("file",),
    "precommit_hook": ("hook_id",), "precommit_remote": ("repo_token",),
    "settings_hook": ("event", "token"), "plugin_enabled": ("token",),
    "settings_local_blocks": (), "claude_subtrees": (), "commands_roster": (),
    "check_ignore": ("candidate",), "ruff_config_form": (),
}


def load_manifest(path: Path) -> tuple[dict, list[ParityFinding]]:
    """Parse + validate the parity manifest. Structural unusability raises
    ManifestUnreadable (exit-2 class); a malformed individual ROW yields a refusal
    finding and the row is skipped -- refused, never guessed."""
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, UnicodeDecodeError, ValueError) as exc:
        raise ManifestUnreadable(f"parity manifest unreadable ({path}): {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("fleet"), dict) \
            or not isinstance(data.get("surfaces"), list):
        raise ManifestUnreadable(
            f"parity manifest missing fleet:/surfaces: structure ({path})")
    if "version" not in data:
        raise ManifestUnreadable(f"parity manifest carries no version: line ({path})")

    refusals: list[ParityFinding] = []
    fleet = data["fleet"]
    for repo_id, spec in sorted(fleet.items()):
        role = (spec or {}).get("role") if isinstance(spec, dict) else None
        if role not in ROLES:
            raise ManifestUnreadable(
                f"fleet entry '{repo_id}' has unknown role {role!r} (known: hub/consumer/pre-deploy)")

    valid_keys = set(fleet.keys()) | ROLES
    seen_ids: set[str] = set()
    seen_waivers: set[str] = set()
    seen_tombstone_joins: set[str] = set()
    rows: list[dict] = []
    for i, row in enumerate(data["surfaces"]):
        rid = row.get("id") if isinstance(row, dict) else None
        label = str(rid or f"surfaces[{i}]")
        if not isinstance(row, dict) or not rid:
            refusals.append(_refusal(label, "surface row is not a mapping with an id"))
            continue
        if rid in seen_ids:
            refusals.append(_refusal(label, f"duplicate surface id '{rid}'"))
            continue
        tier = row.get("tier")
        if not isinstance(tier, dict) or not tier:
            refusals.append(_refusal(label, "tier: must be a non-empty role/repo-keyed map"))
            continue
        bad_key = next((k for k in tier if k not in valid_keys), None)
        bad_tok = next((t for t in tier.values() if t not in TIERS), None)
        if bad_key is not None:
            refusals.append(_refusal(
                label, f"tier key '{bad_key}' is neither a fleet repo nor a role"))
            continue
        if bad_tok is not None:
            refusals.append(_refusal(label, f"unknown tier token '{bad_tok}'"))
            continue
        probe = row.get("probe")
        if not isinstance(probe, dict) or not probe.get("type"):
            refusals.append(_refusal(label, "probe: must be a mapping with a type"))
            continue
        required = _PROBE_REQUIRED_FIELDS.get(str(probe["type"]))
        if required is None:
            refusals.append(_refusal(label, f"unknown probe type '{probe['type']}'"))
            continue
        missing = [f for f in required if not probe.get(f)]
        if missing:
            refusals.append(_refusal(
                label, f"probe type '{probe['type']}' missing required field(s): "
                       f"{', '.join(missing)}"))
            continue
        wc = str(row.get("waiver_component") or rid)
        if wc in seen_waivers:
            # The structural half of one-declaration-one-concern: two rows sharing a
            # waiver_component would let one declaration suppress two concerns.
            refusals.append(_refusal(
                label, f"waiver_component '{wc}' already used by another row"))
            continue
        if "TOMBSTONE" in tier.values():
            join = row.get("join")
            if not isinstance(join, dict) or not join.get("manifest_component"):
                refusals.append(_refusal(
                    label, "TOMBSTONE row without join.manifest_component (ambiguous "
                           "tombstone pointer -- refusing, not guessing)"))
                continue
            jc = str(join["manifest_component"])
            if jc in seen_tombstone_joins:
                refusals.append(_refusal(
                    label, f"second TOMBSTONE row joining deploy component '{jc}' "
                           f"(ambiguous join -- refusing, not guessing)"))
                continue
            seen_tombstone_joins.add(jc)
        seen_ids.add(rid)
        seen_waivers.add(wc)
        rows.append(row)
    data["surfaces"] = rows
    return data, refusals


def load_baseline(path: Path) -> tuple[dict, list[ParityFinding]]:
    """Parse the dependency baseline (FR-7). Unreadable baseline = refusal findings +
    an empty dependency leg (the surface walk still runs; absence is surfaced, never
    silently green)."""
    refusals: list[ParityFinding] = []
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, UnicodeDecodeError, ValueError) as exc:
        return {"dependencies": []}, [_refusal(
            "dependency-baseline", f"baseline unreadable ({path}): {exc}")]
    if not isinstance(data, dict) or not isinstance(data.get("dependencies"), list):
        return {"dependencies": []}, [_refusal(
            "dependency-baseline", f"baseline missing dependencies: list ({path})")]
    rows = []
    for i, row in enumerate(data["dependencies"]):
        if not isinstance(row, dict) or not row.get("name") or not row.get("recommended"):
            refusals.append(_refusal(f"dependency-baseline[{i}]",
                                     "dep row needs name + recommended"))
            continue
        rows.append(row)
    data["dependencies"] = rows
    return data, refusals


def _dev_dir(hub_root: Path) -> Path:
    """The directory holding the fleet's sibling repos. Worktree-safe: resolve the
    PRIMARY checkout via git-common-dir (a linked worktree's plain parent would be
    .claude/worktrees/ -- the codex-flagged false-unavailable class)."""
    rc, out = _git(["rev-parse", "--path-format=absolute", "--git-common-dir"],
                   hub_root)
    if rc == 0 and out:
        primary = Path(out).parent  # <primary>/.git -> <primary>
        return primary.parent
    return Path(hub_root).parent


def resolve_fleet(manifest: dict, hub_root: Path, registry_path: Path,
                  ecosystem_dir: Path, overrides: dict[str, Path],
                  ) -> tuple[list[RepoTarget], list[ParityFinding]]:
    """Fleet map -> concrete repo targets. Cross-checks fleet keys == registry keys in
    BOTH directions (a repo visible to one record and not the other is a refusal
    finding, never a silent skip). Hub root is ALWAYS this checkout (worktree-safe)."""
    findings: list[ParityFinding] = []
    fleet: dict = manifest["fleet"]

    registry = ec._read_yaml(Path(registry_path))
    repos = registry.get("repos") if isinstance(registry.get("repos"), dict) else None
    if repos is None:
        findings.append(_refusal(
            "fleet-registry", f"deployed-versions registry unreadable/shapeless "
                              f"({registry_path}); fleet/registry cross-check skipped"))
    else:
        for name in sorted(set(repos) - set(fleet)):
            findings.append(_refusal(
                "fleet-registry", f"registry repo '{name}' missing from the manifest "
                                  f"fleet map (silent-gap refusal)"))
        for name in sorted(set(fleet) - set(repos)):
            findings.append(_refusal(
                "fleet-registry", f"fleet-map repo '{name}' absent from "
                                  f"deployed-versions.yaml (silent-gap refusal)"))

    targets: list[RepoTarget] = []
    for repo_id in sorted(fleet):
        role = fleet[repo_id]["role"]
        if role == "pre-deploy":
            targets.append(RepoTarget(repo_id, role, None, "pre-deploy: not walked"))
            continue
        if role == "hub":
            targets.append(RepoTarget(repo_id, role, hub_root,
                                      "hub = this checkout (worktree-safe)"))
            continue
        if repo_id in overrides:
            root, note = overrides[repo_id], "resolved via --repo-root override"
        else:
            state = fh._load_state_yaml(Path(ecosystem_dir) / repo_id / "state.yaml")
            stored = state.get("path", "")
            if stored and Path(stored).is_dir():
                root, note = Path(stored), "resolved via ecosystem state.yaml path"
            else:
                root = _dev_dir(hub_root) / repo_id
                note = "resolved via dev-dir sibling fallback (worktree-safe)"
        if not (Path(root) / ".git").exists():
            targets.append(RepoTarget(repo_id, role, None,
                                      f"unresolved: {root} is not a git repo"))
        else:
            targets.append(RepoTarget(repo_id, role, Path(root), note))
    return targets, findings


# ---------------------------------------------------------------------------
# Probes (impure I/O -- everything the pure verdict engine may NOT touch).
# ---------------------------------------------------------------------------


def _git(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or "").strip()
    except OSError as exc:  # git missing etc. -- surfaced in evidence, never a crash
        return 999, f"git unavailable: {exc}"


def _local_token(row: dict, repo_id: str, default: str) -> str:
    names = row.get("local_names") or {}
    return str(names.get(repo_id, default))


def collect_facts(target: RepoTarget, manifest: dict, baseline: dict,
                  hub_root: Path, registry_path: Path) -> dict:
    """One deterministic facts snapshot per walked repo (FR-3): every probe runs here;
    ``verdicts()`` is pure over the result. Sorted, ASCII, no wall-clock."""
    root = target.root
    assert root is not None
    rc_ls, ls_out = _git(["ls-files", "-z"], root)
    git_error = "" if rc_ls == 0 else (f"git ls-files failed (rc={rc_ls}): "
                                       f"{ls_out[:120]}")
    tracked = sorted(p for p in ls_out.split("\0") if p) if rc_ls == 0 else []
    tracked_set = set(tracked)
    top_level = sorted({p.split("/", 1)[0] for p in tracked})

    rc_head, head = _git(["rev-parse", "HEAD"], root)
    rc_st, status = _git(["status", "--porcelain"], root)
    rc_hp, hooks_path_cfg = _git(["config", "core.hooksPath"], root)
    rc_gp, git_hooks_dir = _git(["rev-parse", "--git-path", "hooks"], root)
    armed = {}
    if rc_gp == 0:
        hooks_dir = Path(git_hooks_dir)
        if not hooks_dir.is_absolute():
            hooks_dir = root / hooks_dir
        for stage in ("pre-commit", "commit-msg", "pre-push"):
            armed[stage] = (hooks_dir / stage).is_file()

    registry = ec._read_yaml(Path(registry_path))
    source_tag = None
    reg_repos = registry.get("repos") or {}
    if isinstance(reg_repos.get(target.repo_id), dict):
        source_tag = reg_repos[target.repo_id].get("source_tag")

    precommit_cfg = ec._read_yaml(root / ".pre-commit-config.yaml")
    hook_ids = sorted({str(h.get("id")) for h in ec._precommit_hooks(root)
                       if isinstance(h.get("id"), str)})
    remotes = []
    for repo in precommit_cfg.get("repos") or []:
        if isinstance(repo, dict) and isinstance(repo.get("repo"), str):
            ids = [str(h.get("id")) for h in repo.get("hooks") or []
                   if isinstance(h, dict) and h.get("id")]
            remotes.append({"repo": repo["repo"], "rev": str(repo.get("rev", "")),
                            "hook_ids": ids})

    settings = ec._read_json(root / ".claude" / "settings.json")
    plugins = settings.get("enabledPlugins")
    plugin_names = sorted(plugins.keys()) if isinstance(plugins, dict) else \
        sorted(str(p) for p in plugins) if isinstance(plugins, list) else []
    settings_by_event: dict[str, list[str]] = {}
    hooks_cfg = settings.get("hooks")
    events = sorted(hooks_cfg.keys()) if isinstance(hooks_cfg, dict) else []
    for ev in events:  # EVERY configured event, never a hardcoded subset
        cmds = ec._settings_hook_commands(root, ev)
        if cmds:
            settings_by_event[ev] = cmds

    claude_subdirs = sorted({p.split("/")[1] for p in tracked
                             if p.startswith(".claude/") and p.count("/") >= 2})
    commands = sorted(p.rsplit("/", 1)[1] for p in tracked
                      if p.startswith(".claude/commands/") and p.endswith(".md"))

    # Per-surface probe results keyed by surface id.
    surfaces: dict[str, dict] = {}
    for row in manifest["surfaces"]:
        sid = row["id"]
        probe = row["probe"]
        ptype = probe["type"]
        res: dict = {"type": ptype}
        if ptype == "path_tracked":
            res["present"] = probe["path"] in tracked_set
            res["detail"] = probe["path"]
        elif ptype == "dir_tracked":
            prefix = probe["path"].rstrip("/") + "/"
            res["present"] = any(p.startswith(prefix) for p in tracked)
            res["detail"] = probe["path"] + "/"
        elif ptype == "dir_exists":
            res["present"] = (root / probe["path"]).is_dir()
            res["detail"] = probe["path"] + "/ (disk)"
        elif ptype == "file_exists":
            res["present"] = (root / probe["path"]).exists()
            res["detail"] = probe["path"] + " (disk)"
        elif ptype == "file_contains":
            try:
                text = (root / probe["path"]).read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            res["present"] = probe["token"] in text
            res["detail"] = f"{probe['path']} contains '{probe['token']}'"
        elif ptype == "glob_tracked":
            hits = [t for t in top_level if fnmatch.fnmatch(t, probe["glob"])]
            res["present"] = bool(hits)
            res["detail"] = f"{probe['glob']} -> {hits or 'none'}"
        elif ptype == "command_present":
            res["present"] = probe["file"] in commands
            res["detail"] = f".claude/commands/{probe['file']}"
        elif ptype == "precommit_hook":
            token = _local_token(row, target.repo_id, probe["hook_id"])
            res["present"] = token in hook_ids
            res["detail"] = f"pre-commit hook id '{token}'"
        elif ptype == "precommit_remote":
            token = probe["repo_token"]
            hit = next((r for r in remotes if token in r["repo"]), None)
            res["present"] = hit is not None
            res["rev"] = hit["rev"] if hit else None
            res["detail"] = f"pre-commit remote containing '{token}'"
            required_ids = [str(x) for x in probe.get("required_hook_ids") or []]
            if hit and required_ids:
                # intake #12 Tier-1: carried-block fidelity = rev + hook IDS.
                res["missing_hook_ids"] = sorted(set(required_ids) - set(hit["hook_ids"]))
            if probe.get("expected_rev_from") == "deployed-versions":
                res["expected_rev"] = source_tag
                if hit and source_tag:
                    tag_rc, _ = _git(["rev-parse", "-q", "--verify",
                                      f"refs/tags/{hit['rev']}"], hub_root)
                    res["tag_exists_in_hub"] = tag_rc == 0
                    if probe.get("ancestry") and tag_rc == 0:
                        anc_rc, _ = _git(["merge-base", "--is-ancestor",
                                          f"refs/tags/{hit['rev']}", "HEAD"], hub_root)
                        res["tag_is_ancestor"] = anc_rc == 0
        elif ptype == "settings_hook":
            token = _local_token(row, target.repo_id, probe["token"])
            cmds = settings_by_event.get(probe["event"], [])
            res["present"] = any(token in c for c in cmds)
            res["detail"] = f"settings.json {probe['event']} hook containing '{token}'"
        elif ptype == "plugin_enabled":
            res["present"] = any(probe["token"] in p for p in plugin_names)
            res["detail"] = f"enabledPlugins containing '{probe['token']}'"
        elif ptype == "settings_local_blocks":
            res["all_commands"] = sorted(c for cmds in settings_by_event.values()
                                         for c in cmds)
            res["present"] = True
        elif ptype == "claude_subtrees":
            res["subdirs"] = claude_subdirs
            res["present"] = True
        elif ptype == "commands_roster":
            res["commands"] = commands
            res["present"] = True
        elif ptype == "check_ignore":
            rc, _out = _git(["check-ignore", "-q", probe["candidate"]], root)
            res["ignored"] = rc == 0
            res["present"] = res["ignored"]
            res["detail"] = f"git check-ignore {probe['candidate']} (effect probe)"
        elif ptype == "ruff_config_form":
            # Representation-only (intake #12 Tier-3 convergence candidate / W3-14
            # OPEN): the FORM is reported as evidence, never verdicted.
            forms = []
            pyp = root / "pyproject.toml"
            if pyp.exists():
                try:
                    import tomllib
                    if "ruff" in (tomllib.loads(
                            pyp.read_text(encoding="utf-8")).get("tool") or {}):
                        forms.append("pyproject [tool.ruff]")
                except Exception:  # noqa: BLE001 -- malformed toml reads as no-form
                    pass
            if (root / ".ruff.toml").exists():
                forms.append(".ruff.toml")
            if (root / "assets" / "ruff-pre-commit.yaml").exists():
                forms.append("assets/ruff-pre-commit.yaml")
            res["present"] = bool(forms)
            res["detail"] = ("ruff config form(s): "
                             + (", ".join(forms) if forms else "none"))
        else:
            res["error"] = f"unknown probe type '{ptype}'"
        surfaces[sid] = res

    deps: dict[str, dict] = {}
    for dep in baseline.get("dependencies", []):
        deps[dep["name"]] = _probe_dep(root, dep["name"], hub_root)

    return {
        "repo_id": target.repo_id,
        "role": target.role,
        "git_error": git_error,
        "head": head if rc_head == 0 else "unknown",
        "dirty": bool(status) if rc_st == 0 else True,
        "hooks_path_cfg": hooks_path_cfg if rc_hp == 0 and hooks_path_cfg else "",
        "hooks_armed": armed,
        "has_precommit_config": (root / ".pre-commit-config.yaml").exists(),
        "top_level_tracked": top_level,
        "claude_subdirs": claude_subdirs,
        "commands": commands,
        "surfaces": surfaces,
        "deps": deps,
        "source_tag": source_tag,
    }


def _normalize_dep(name: str) -> str:
    return name.lower().replace("-", "_")


_SPECIFIER_SPLIT = re.compile(r"[<>=!~\[\s;]")


def _dep_token(requirement: str) -> str:
    """'pytest-xdist>=3.8' -> 'pytest_xdist' (normalized name token, EXACT-equality
    matched downstream so 'pytest' never matches 'pytest-xdist')."""
    return _normalize_dep(_SPECIFIER_SPLIT.split(requirement.strip(), 1)[0])


def _probe_dep(root: Path, name: str, hub_root: Path) -> dict:
    """Declared (pyproject/requirements parse) + installed (dist-info dir scan; the
    running interpreter for the no-venv hub). Parsing only -- consumer code NEVER runs."""
    declared, declared_src = None, "none"
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 -- malformed toml reads as no-declaration
            data = {}
        groups: list = []
        proj = data.get("project") or {}
        groups.extend((proj.get("optional-dependencies") or {}).values())
        groups.append(proj.get("dependencies") or [])
        groups.extend((data.get("dependency-groups") or {}).values())
        for group in groups:
            for item in group or []:
                if isinstance(item, str) and _dep_token(item) == _normalize_dep(name):
                    declared, declared_src = item.strip(), "pyproject.toml"
                    break
            if declared:
                break
    if declared is None:
        for req in sorted(root.glob("requirements*.txt")):
            try:
                for line in req.read_text(encoding="utf-8", errors="replace").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and \
                            _dep_token(line) == _normalize_dep(name):
                        declared, declared_src = line, req.name
                        break
            except OSError:
                continue
            if declared:
                break

    installed, installed_src = None, "none"
    site = root / ".venv" / "Lib" / "site-packages"
    if site.is_dir():
        versions = []
        for d in sorted(site.glob("*.dist-info")):
            pkg, _, ver = d.name[: -len(".dist-info")].rpartition("-")
            if pkg and _normalize_dep(pkg) == _normalize_dep(name):
                versions.append(ver)
        if versions:
            installed = versions[-1]
            installed_src = ".venv site-packages"
        else:
            installed_src = ".venv site-packages (not found)"
    elif Path(root).resolve() == Path(hub_root).resolve():
        try:
            from importlib.metadata import version
            installed, installed_src = version(name), "running interpreter (hub no-venv policy)"
        except Exception:  # noqa: BLE001
            installed_src = "running interpreter (not found)"
    else:
        installed_src = "uninspectable (no .venv)"
    return {"declared": declared, "declared_src": declared_src,
            "installed": installed, "installed_src": installed_src}


def _version_tuple(v: str) -> tuple[int, ...]:
    parts = []
    for tok in v.split("."):
        digits = "".join(ch for ch in tok if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts) or (0,)


def _satisfies(installed: str | None, recommended: str) -> bool:
    """Tiny dotted-int comparator (no packaging dep): supports '>=X', '==X', bare 'X'
    (as a minimum). Honest floor semantics for a WARN-only reporter."""
    if installed is None:
        return False
    rec = recommended.strip()
    if rec.startswith(">="):
        return _version_tuple(installed) >= _version_tuple(rec[2:].strip())
    if rec.startswith("=="):
        return _version_tuple(installed) == _version_tuple(rec[2:].strip())
    return _version_tuple(installed) >= _version_tuple(rec)


_DECLARED_VERSION_RE = re.compile(r"(>=|==|~=|>)\s*([0-9][0-9.]*)")


def _declared_ok(declared: str | None, recommended: str) -> bool:
    """The DECLARED specifier must itself satisfy the baseline: a declaration pinned
    BELOW the recommendation (e.g. ==3.1 vs >=3.8) false-passes on a lucky env and
    regresses on a clean rebuild (codex delta re-review 2026-07-13). An unpinned
    declaration asserts presence, not version -- accepted, evidence shows the pin
    state either way."""
    if not declared:
        return False
    m = _DECLARED_VERSION_RE.search(declared)
    if not m:
        return True  # unpinned declaration: presence declared, no version floor
    return _satisfies(m.group(2), recommended)


# ---------------------------------------------------------------------------
# Declaration matching (the FR-4 leg -- exact-id, shelf-life honored).
# ---------------------------------------------------------------------------


def _match_declaration(component: str, allowlist: list, *, run_date, policy: dict,
                       ) -> tuple[str, str]:
    """('valid'|'expired'|'invalid'|'none', evidence). EXACT component-id equality only
    -- a substring / prefix / bare-id declaration matches nothing (disposition-register
    precision-over-recall)."""
    outcomes: list[tuple[str, str]] = []
    for entry in allowlist:
        if entry.component.strip() != component:
            continue
        status, ev = ec.validate_allowlist_entry(entry, run_date=run_date,
                                                 waivable_policy=policy)
        if status == ec.AL_VALID:
            return "valid", ev
        outcomes.append((status, ev))
    for status, ev in outcomes:
        if status == ec.AL_EXPIRED:
            return "expired", ev  # section 9b: advisory re-WARN, not drift (ruled fork)
    if outcomes:
        return "invalid", "; ".join(ev for _s, ev in outcomes)
    return "none", f"no declaration for component '{component}'"


# ---------------------------------------------------------------------------
# Verdict engine (PURE: manifest + facts + allowlists + run_date -> findings).
# ---------------------------------------------------------------------------


def _tier_for(row: dict, repo_id: str, role: str) -> str | None:
    tier = row["tier"]
    if repo_id in tier:
        return tier[repo_id]
    return tier.get(role)


def _row_waivable(row: dict, tier_token: str) -> bool:
    if "waivable" in row:
        return bool(row["waivable"])
    return tier_token not in ("MUST", "INVERSE")


@dataclass
class _RepoEval:
    findings: list[ParityFinding] = field(default_factory=list)
    consumed: set[str] = field(default_factory=set)
    # components that showed a LIVE divergence this run (consumed or not): a stale
    # decoration must never fire on a surface that actually diverged (codex 2026-07-13)
    diverged: set[str] = field(default_factory=set)
    must_settings_tokens: list[str] = field(default_factory=list)


def _must_settings_tokens(manifest: dict, repo_id: str, role: str) -> list[str]:
    """The hub-carried settings tokens applicable to this repo, derived from the
    manifest's own settings_hook rows (single source -- never a hardcoded twin)."""
    tokens: list[str] = []
    for row in manifest["surfaces"]:
        if row["probe"].get("type") != "settings_hook":
            continue
        if _tier_for(row, repo_id, role) is None:
            continue
        tokens.append(_local_token(row, repo_id, row["probe"]["token"]))
    return tokens


def verdicts(manifest: dict, baseline: dict, targets: list[RepoTarget],
             facts_by_repo: dict[str, dict], allowlists: dict[str, list],
             deploy_manifest: dict, run_date: str,
             ) -> tuple[list[ParityFinding], dict[str, set]]:
    """The intake #12 decision tree over the facts snapshots. Pure + deterministic:
    same inputs -> same findings, run_date is a parameter (never wall-clock), one
    finding per concern. Also returns the per-repo CONSUMED declaration components
    (feeds the stale/unmapped awareness rendering)."""
    policy = ec.waivability_policy_from_manifest(deploy_manifest)
    deploy_components: dict[str, dict] = {}
    deploy_dup_ids: set[str] = set()
    for c in deploy_manifest.get("components") or []:
        if isinstance(c, dict) and c.get("id"):
            cid = str(c["id"])
            if cid in deploy_components:
                deploy_dup_ids.add(cid)  # ambiguous join target -> refuse downstream
            deploy_components[cid] = c
    out: list[ParityFinding] = []
    consumed_by_repo: dict[str, set] = {}

    for target in targets:
        if target.role == "pre-deploy":
            out.append(ParityFinding(target.repo_id, "fleet-membership",
                                     SKIPPED_PRE_DEPLOY, SEV_INFO,
                                     "registered, no methodology deployed yet -- "
                                     "rendered, not silently absent", "-"))
            continue
        if target.root is None:
            out.append(ParityFinding(target.repo_id, "fleet-membership", UNAVAILABLE,
                                     SEV_WARN, _ascii(target.note),
                                     _ACTIONS[UNAVAILABLE]))
            continue
        facts = facts_by_repo[target.repo_id]
        if facts.get("git_error"):
            # A repo git cannot enumerate is UNAVAILABLE -- never a storm of false
            # MUST-absent findings (codex 2026-07-13; Codex FR-12 never-silently-green).
            out.append(ParityFinding(
                target.repo_id, "fleet-membership", UNAVAILABLE, SEV_WARN,
                _ascii(f"facts snapshot unavailable: {facts['git_error']} -- surface "
                       f"walk skipped, nothing rendered green"),
                _ACTIONS[UNAVAILABLE]))
            consumed_by_repo[target.repo_id] = set()
            continue
        allowlist = allowlists.get(target.repo_id, [])
        ev = _RepoEval()
        ev.must_settings_tokens = _must_settings_tokens(manifest, target.repo_id,
                                                        target.role)
        for row in manifest["surfaces"]:
            _eval_row(row, target, facts, allowlist, policy, deploy_components,
                      run_date, ev, deploy_dup_ids)
        _eval_sweep(manifest, target, facts, allowlist, policy, run_date, ev)
        _eval_deps(baseline, target, facts, allowlist, policy, run_date, ev)
        _eval_hooks_armed(target, facts, allowlist, policy, run_date, ev)
        _eval_stale(manifest, baseline, target, facts, allowlist, ev)
        consumed_by_repo[target.repo_id] = ev.consumed
        out.extend(ev.findings)
    return out, consumed_by_repo


def _eval_hooks_armed(target: RepoTarget, facts: dict, allowlist: list, policy: dict,
                      run_date, ev: _RepoEval) -> None:
    """FR-6 'installed+armed stages': a repo that CARRIES a .pre-commit-config.yaml
    must have the three standard stages armed in its effective hooks dir (worktree/
    hooksPath-safe probe). One concern per repo; complements the hub-only audit.py
    hooks_armed self-check with fleet reach. No config -> no expectation."""
    if not facts.get("has_precommit_config"):
        return
    armed = facts.get("hooks_armed") or {}
    missing = sorted(stage for stage, ok in armed.items() if not ok)
    hp = facts.get("hooks_path_cfg")
    if not missing:
        ev.findings.append(ParityFinding(
            target.repo_id, "hooks-armed", AT_PARITY, SEV_INFO,
            _ascii("all three hook stages armed in the effective hooks dir"
                   + (f" (core.hooksPath={hp})" if hp else "")), "-", "hooks-armed"))
        return
    _sweep_style_finding(
        target, "hooks-armed", "hooks-armed",
        f"pre-commit config present but stage(s) NOT armed: {', '.join(missing)}"
        + (f"; core.hooksPath={hp}" if hp else "")
        + " (installed+armed effect probe -- a carried config with dead hooks is the"
          " relic-hooksPath silence class)", allowlist, policy, run_date, ev)


def _pass_or_declare(row: dict, target: RepoTarget, tier_token: str, divergence_ev: str,
                     allowlist: list, policy: dict, run_date, ev: _RepoEval,
                     warn_verdict: str = WARN_UNDECLARED,
                     warn_sev: str = SEV_WARN) -> None:
    """Shared divergence path: declaration flips to PASS-declared (valid) /
    advisory-rewarn (expired); non-waivable rows and missing declarations WARN."""
    sid = row["id"]
    component = str(row.get("waiver_component") or sid)
    ev.diverged.add(component)
    if not _row_waivable(row, tier_token):
        ev.findings.append(ParityFinding(
            target.repo_id, sid, warn_verdict, warn_sev,
            _ascii(divergence_ev + " -- non-waivable surface (declarations do not apply)"),
            _ACTIONS[warn_verdict], component))
        return
    status, decl_ev = _match_declaration(component, allowlist, run_date=run_date,
                                         policy=policy)
    if status == "valid":
        ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, PASS_DECLARED, SEV_INFO,
            _ascii(divergence_ev + " -- declared: " + decl_ev),
            _ACTIONS[PASS_DECLARED], component))
    elif status == "expired":
        ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, ADVISORY_REWARN, SEV_WARN,
            _ascii(divergence_ev + " -- declaration EXPIRED: " + decl_ev),
            _ACTIONS[ADVISORY_REWARN], component))
    else:
        detail = decl_ev if status == "invalid" else "undeclared"
        if status == "invalid":
            ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, warn_verdict, warn_sev,
            _ascii(divergence_ev + " -- " + detail), _ACTIONS[warn_verdict], component))


def _eval_row(row: dict, target: RepoTarget, facts: dict, allowlist: list,
              policy: dict, deploy_components: dict, run_date, ev: _RepoEval,
              deploy_dup_ids: set | None = None) -> None:
    sid = row["id"]
    tier_token = _tier_for(row, target.repo_id, target.role)
    if tier_token is None:
        return
    component = str(row.get("waiver_component") or sid)
    res = facts["surfaces"].get(sid, {})
    if res.get("error"):
        ev.diverged.add(component)  # unevaluable, never stale-decorated
        ev.findings.append(ParityFinding(target.repo_id, sid, REFUSED, SEV_WARN,
                                         _ascii(res["error"]), _ACTIONS[REFUSED],
                                         component))
        return
    present = bool(res.get("present"))
    detail = res.get("detail", sid)

    if row["probe"]["type"] == "settings_local_blocks":
        _eval_settings_blocks(row, target, facts, allowlist, policy, run_date, ev)
        return
    if row["probe"]["type"] == "claude_subtrees":
        _eval_claude_subtrees(row, target, facts, allowlist, policy, run_date, ev)
        return
    if row["probe"]["type"] == "commands_roster":
        _eval_commands_roster(row, target, facts, allowlist, policy, run_date, ev)
        return

    if tier_token == "MUST":
        if not present:
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, MUST_ABSENT, SEV_ERROR,
                _ascii(f"MUST surface absent: {detail}"), _ACTIONS[MUST_ABSENT],
                component))
            return
        fidelity_bad = _fidelity_problem(res)
        if fidelity_bad:
            # unfaithful carriage of a MUST surface is the error class (present !=
            # carried) -- the remediation is FIX, never DECLARE (codex 2026-07-13)
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, WARN_UNDECLARED, SEV_ERROR,
                _ascii(f"present but not carried faithfully: {fidelity_bad}"),
                _ACTIONS[MUST_ABSENT], component))
            return
        expected_div = (row.get("declared_divergence") or {}).get(target.repo_id)
        if expected_div:
            status, decl_ev = _match_declaration(component, allowlist,
                                                 run_date=run_date, policy=policy)
            if status == "valid":
                ev.consumed.add(component)
                ev.findings.append(ParityFinding(
                    target.repo_id, sid, PASS_DECLARED, SEV_INFO,
                    _ascii(f"at parity with a manifest-expected declared behavioral "
                           f"divergence ({expected_div}) -- " + decl_ev),
                    _ACTIONS[PASS_DECLARED], component))
            elif status == "expired":
                ev.consumed.add(component)
                ev.findings.append(ParityFinding(
                    target.repo_id, sid, ADVISORY_REWARN, SEV_WARN,
                    _ascii(f"declared behavioral divergence EXPIRED -- {decl_ev}"),
                    _ACTIONS[ADVISORY_REWARN], component))
            else:
                ev.diverged.add(component)
                ev.findings.append(ParityFinding(
                    target.repo_id, sid, WARN_UNDECLARED, SEV_WARN,
                    _ascii(f"manifest expects a declared behavioral divergence here "
                           f"({expected_div}) but the declaration is {status}"),
                    _ACTIONS[WARN_UNDECLARED], component))
            return
        ev.findings.append(ParityFinding(
            target.repo_id, sid, AT_PARITY, SEV_INFO,
            _ascii(f"present + faithful: {detail}" + _fidelity_note(res)), "-",
            component))
        return

    if tier_token == "SHOULD":
        if present:
            ev.findings.append(ParityFinding(target.repo_id, sid, AT_PARITY, SEV_INFO,
                                             _ascii(f"present: {detail}"), "-", component))
        else:
            _pass_or_declare(row, target, tier_token,
                             f"SHOULD surface absent: {detail}", allowlist, policy,
                             run_date, ev)
        return

    if tier_token == "LOCAL":
        if not present:
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO,
                _ascii(f"LOCAL surface not carried (fine): {detail}"), "-", component))
            return
        if row.get("declared_by") == "intake-12":
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO,
                _ascii(f"LOCAL surface present; declared by the SETTLED template "
                       f"(intake #12 Tier-3): {detail}"), "-", component))
            return
        _pass_or_declare(row, target, tier_token,
                         f"LOCAL surface present: {detail}", allowlist, policy,
                         run_date, ev)
        return

    if tier_token == "INVERSE":
        if present:
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, MUST_ABSENT, SEV_ERROR,
                _ascii(f"surface present where the role forbids it: {detail}"),
                _ACTIONS[MUST_ABSENT], component))
        else:
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO,
                _ascii(f"correctly absent (inverse rule): {detail}"), "-", component))
        return

    if tier_token == "IGNORE":
        if res.get("ignored"):
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO,
                _ascii(f"ignored by the resolver: {detail}"), "-", component))
        else:
            _pass_or_declare(row, target, tier_token,
                             f"NOT ignored by the resolver (effect probe -- a "
                             f"textually-present pattern may be semantically inert): "
                             f"{detail}", allowlist, policy, run_date, ev)
        return

    if tier_token == "TOMBSTONE":
        comp_id = row["join"]["manifest_component"]
        if deploy_dup_ids and comp_id in deploy_dup_ids:
            # refused = unevaluable: mark diverged so _eval_stale can never ALSO
            # decorate this component's declaration stale in the same run (a
            # "no action proposed" run must not propose pruning a declaration --
            # codex delta re-review 2026-07-13)
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, REFUSED, SEV_WARN,
                _ascii(f"ambiguous tombstone join: the deploy manifest carries more "
                       f"than one component with id '{comp_id}' -- refusing to "
                       f"evaluate (no action proposed)"), _ACTIONS[REFUSED],
                component))
            return
        comp = deploy_components.get(comp_id)
        if comp is None:
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, REFUSED, SEV_WARN,
                _ascii(f"tombstone pointer mis-addressed: deploy manifest has no "
                       f"component '{comp_id}' -- refusing to evaluate (no action "
                       f"proposed)"), _ACTIONS[REFUSED], component))
            return
        if comp.get("status") != "removed":
            ev.diverged.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, REFUSED, SEV_WARN,
                _ascii(f"tombstone join mismatch: parity row says TOMBSTONE but deploy "
                       f"component '{comp_id}' has status "
                       f"'{comp.get('status')}' -- refusing (no action proposed)"),
                _ACTIONS[REFUSED], component))
            return
        removed_in = comp.get("removed_in", "?")
        if not present:
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO,
                _ascii(f"tombstone honored: absent-by-design (removed_in "
                       f"{removed_in}): {detail}"), "-", component))
            return
        _pass_or_declare(
            row, target, tier_token,
            f"tombstoned component present again (status: removed since "
            f"{removed_in}): {detail}", allowlist, policy, run_date, ev,
            warn_verdict=TOMBSTONE_VIOLATED)
        if row.get("pending_migration"):
            pm = row["pending_migration"]
            ev.findings.append(ParityFinding(
                target.repo_id, sid + ":pending-migration", AT_PARITY, SEV_INFO,
                _ascii(f"pending coordinated migration on record: -> {pm.get('to')} "
                       f"({pm.get('ticket')}) -- representation only, no verdict "
                       f"effect"), "-", None))
        return


def _fidelity_problem(res: dict) -> str | None:
    if "expected_rev" in res:
        expected, actual = res.get("expected_rev"), res.get("rev")
        if expected is not None:
            if actual != expected:
                return (f"rev {actual!r} != recorded deploy source_tag {expected!r} "
                        f"(present != carried)")
            if res.get("tag_exists_in_hub") is False:
                return f"pinned rev {actual!r} is not a tag in the hub repo"
            if res.get("tag_is_ancestor") is False:
                return (f"pinned tag {actual!r} exists but is not an ancestor of hub "
                        f"HEAD (tag-ancestry effect probe)")
    if res.get("missing_hook_ids"):
        return (f"hub block missing required hook id(s): "
                f"{', '.join(res['missing_hook_ids'])} "
                f"(carried-block fidelity = rev + hook ids, intake #12)")
    return None


def _fidelity_note(res: dict) -> str:
    if "expected_rev" in res:
        if res.get("expected_rev") is None:
            return " (no recorded deploy tag; presence-only)"
        note = f" (rev {res.get('rev')} == recorded source_tag"
        if res.get("tag_is_ancestor"):
            note += ", tag is ancestor of hub HEAD"
        return note + ")"
    return ""


def _eval_settings_blocks(row: dict, target: RepoTarget, facts: dict, allowlist: list,
                          policy: dict, run_date, ev: _RepoEval) -> None:
    """W3-07 hook-block ownership: every settings.json hook command must match a
    hub-carried MUST token or the manifest-owned local set; anything else WARNs."""
    sid = row["id"]
    owned = (row["probe"].get("owned") or {}).get(target.repo_id, [])
    must_tokens = ev.must_settings_tokens
    all_cmds = facts["surfaces"].get(sid, {}).get("all_commands", [])
    unmatched = [c for c in all_cmds
                 if not any(t in c for t in must_tokens)
                 and not any(str(o) in c for o in owned)]
    if not unmatched:
        ev.findings.append(ParityFinding(
            target.repo_id, sid, AT_PARITY, SEV_INFO,
            _ascii(f"every settings hook command is hub-carried or manifest-owned "
                   f"({len(all_cmds)} command(s))"), "-",
            str(row.get("waiver_component") or sid)))
        return
    seen_components: dict[str, int] = {}
    for cmd in unmatched:
        short = cmd if len(cmd) <= 90 else cmd[:87] + "..."
        base = "settings-hook:" + _short_token(cmd)
        # basename collisions get a deterministic ordinal so one declaration can
        # never suppress two distinct commands (codex 2026-07-13)
        n = seen_components.get(base, 0)
        seen_components[base] = n + 1
        component = base if n == 0 else f"{base}#{n + 1}"
        _sweep_style_finding(target, sid, component,
                             f"settings.json hook command not hub-carried and not "
                             f"manifest-owned: '{short}'", allowlist, policy,
                             run_date, ev)


def _short_token(cmd: str) -> str:
    base = cmd.replace("\\", "/").split("/")[-1].split()[0] if cmd.strip() else "empty"
    return base


def _eval_claude_subtrees(row: dict, target: RepoTarget, facts: dict, allowlist: list,
                          policy: dict, run_date, ev: _RepoEval) -> None:
    sid = row["id"]
    shared = [str(s) for s in row["probe"].get("shared") or []]
    owned = [str(o) for o in (row["probe"].get("owned") or {}).get(target.repo_id, [])]
    unexpected = [d for d in facts["claude_subdirs"] if d not in shared + owned]
    if not unexpected:
        ev.findings.append(ParityFinding(
            target.repo_id, sid, AT_PARITY, SEV_INFO,
            _ascii(f".claude subtrees all shared-or-owned: "
                   f"{facts['claude_subdirs'] or ['(none)']}"), "-",
            str(row.get("waiver_component") or sid)))
        return
    for d in unexpected:
        _sweep_style_finding(target, sid, f".claude/{d}",
                             f".claude/{d}/ is tracked but neither shared floor nor a "
                             f"declared owned subtree (W3-07 ownership map)",
                             allowlist, policy, run_date, ev)


def _eval_commands_roster(row: dict, target: RepoTarget, facts: dict, allowlist: list,
                          policy: dict, run_date, ev: _RepoEval) -> None:
    sid = row["id"]
    expected = set(str(x) for x in row["probe"].get("expected_all") or [])
    expected |= set(str(x) for x in
                    (row["probe"].get("expected_repo") or {}).get(target.repo_id, []))
    extras = [c for c in facts["commands"] if c not in expected]
    if not extras:
        ev.findings.append(ParityFinding(
            target.repo_id, sid, AT_PARITY, SEV_INFO,
            _ascii(f"command roster closed: {facts['commands'] or ['(none)']}"), "-",
            str(row.get("waiver_component") or sid)))
        return
    for c in extras:
        _sweep_style_finding(target, sid, f"command:{c}",
                             f".claude/commands/{c} exists but no manifest row or "
                             f"roster expectation covers it", allowlist, policy,
                             run_date, ev)


def _sweep_style_finding(target: RepoTarget, sid: str, component: str, divergence: str,
                         allowlist: list, policy: dict, run_date, ev: _RepoEval,
                         verdict_when_undeclared: str = WARN_UNDECLARED,
                         severity: str = SEV_WARN) -> None:
    """Divergences discovered by enumeration (sweep / roster / subtree): declaration
    component = the concrete entry name, exact-equality matched."""
    ev.diverged.add(component)
    status, decl_ev = _match_declaration(component, allowlist, run_date=run_date,
                                         policy=policy)
    if status == "valid":
        ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, PASS_DECLARED, SEV_INFO,
            _ascii(divergence + " -- declared: " + decl_ev), "-", component))
    elif status == "expired":
        ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, ADVISORY_REWARN, SEV_WARN,
            _ascii(divergence + " -- declaration EXPIRED: " + decl_ev),
            _ACTIONS[ADVISORY_REWARN], component))
    else:
        if status == "invalid":
            ev.consumed.add(component)
        ev.findings.append(ParityFinding(
            target.repo_id, sid, verdict_when_undeclared, severity,
            _ascii(divergence + (" -- " + decl_ev if status == "invalid" else "")),
            _ACTIONS[verdict_when_undeclared], component))


def _covered_top_segments(manifest: dict, repo_id: str, role: str) -> set[str]:
    covered: set[str] = set()
    globs: list[str] = []
    for row in manifest["surfaces"]:
        if _tier_for(row, repo_id, role) is None:
            continue
        probe = row["probe"]
        p = probe.get("path")
        if p:
            covered.add(str(p).replace("\\", "/").strip("/").split("/")[0])
        if probe.get("type") == "glob_tracked":
            globs.append(probe["glob"])
        if probe.get("type") in ("command_present", "claude_subtrees", "commands_roster",
                                 "settings_hook", "plugin_enabled",
                                 "settings_local_blocks"):
            covered.add(".claude")
        if probe.get("type") == "precommit_hook" or probe.get("type") == "precommit_remote":
            covered.add(".pre-commit-config.yaml")
    covered.add(".methodology.yaml")  # the declaration file itself is always sanctioned
    return covered | {"__globs__:" + g for g in globs}


_TIER4_TOP_NAMES = frozenset({
    ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
    ".hypothesis", "node_modules",
})


def _eval_sweep(manifest: dict, target: RepoTarget, facts: dict, allowlist: list,
                policy: dict, run_date, ev: _RepoEval) -> None:
    """The decision tree's NO branch (anti-regress property): every TRACKED top-level
    entry not covered by an applicable manifest row is declared, Tier-4-tracked
    (tracked-ephemera), or WARN-undeclared. Untracked/ignored entries are invisible by
    construction (sanctioned worktree lanes, venvs, scratch never false-positive).
    GRAIN LIMIT (honest, deliberate): the sweep walks TOP-LEVEL entries only -- the
    intake #12 tree's own grain ('per root entry E'). Depth inside a covered top-level
    dir (e.g. a rogue docs/ genre) is Rule-A hermetization's job at the hub and a
    hardening candidate fleet-wide; this v1 does not claim it."""
    covered = _covered_top_segments(manifest, target.repo_id, target.role)
    globs = [c.split(":", 1)[1] for c in covered if c.startswith("__globs__:")]
    for entry in facts["top_level_tracked"]:
        if entry in covered:
            continue
        if any(fnmatch.fnmatch(entry, g) for g in globs):
            continue
        if entry in _TIER4_TOP_NAMES or entry.endswith(".egg-info"):
            _sweep_style_finding(target, "root-sweep", entry,
                                 f"Tier-4 ephemera '{entry}' is TRACKED (should be "
                                 f"gitignored, never committed)", allowlist, policy,
                                 run_date, ev,
                                 verdict_when_undeclared=TRACKED_EPHEMERA)
            continue
        _sweep_style_finding(target, "root-sweep", entry,
                             f"top-level entry '{entry}' is not in the template for "
                             f"role '{target.role}'", allowlist, policy, run_date, ev)


def _eval_deps(baseline: dict, target: RepoTarget, facts: dict, allowlist: list,
               policy: dict, run_date, ev: _RepoEval) -> None:
    """FR-7 / #332: recommended vs declared+installed; drift/absence/uninspectable =
    WARN, never a block; a valid declaration clears the WARN without erasing the
    observed evidence (it stays in the finding text)."""
    for dep in baseline.get("dependencies", []):
        applies = dep.get("applies_to") or ["hub", "consumer"]
        if target.role not in applies and target.repo_id not in applies:
            continue
        name = dep["name"]
        rec = str(dep["recommended"])
        d = facts["deps"].get(name, {})
        declared, installed = d.get("declared"), d.get("installed")
        evidence = (f"expected {name} {rec}; declared: "
                    f"{declared or 'absent'} ({d.get('declared_src')}); installed: "
                    f"{installed or 'absent'} ({d.get('installed_src')})")
        sid = f"dep-{name}"
        component = str(dep.get("waiver_component") or sid)
        # AT-PARITY needs BOTH halves of the #332 contract: the declared set AND the
        # active environment (installed-only was the codex-flagged false-green -- an
        # undeclared dep vanishes on the next clean env rebuild), and the declared
        # specifier must itself satisfy the baseline (a ==3.1 pin with 3.8 luckily
        # installed regresses on rebuild -- codex delta re-review).
        if _satisfies(installed, rec) and _declared_ok(declared, rec):
            ev.findings.append(ParityFinding(
                target.repo_id, sid, AT_PARITY, SEV_INFO, _ascii(evidence), "-",
                component))
            continue
        if _satisfies(installed, rec) and not declared:
            evidence += " -- installed but UNDECLARED (pin it or declare the divergence)"
        elif _satisfies(installed, rec) and declared:
            evidence += (" -- installed OK but the DECLARED pin does not satisfy the "
                         "baseline (regresses on a clean rebuild)")
        ev.diverged.add(component)
        status, decl_ev = _match_declaration(component, allowlist, run_date=run_date,
                                             policy=policy)
        if status == "valid":
            ev.consumed.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, PASS_DECLARED, SEV_INFO,
                _ascii(evidence + " -- declared: " + decl_ev), "-", component))
        elif status == "expired":
            ev.consumed.add(component)
            ev.findings.append(ParityFinding(
                target.repo_id, sid, ADVISORY_REWARN, SEV_WARN,
                _ascii(evidence + " -- declaration EXPIRED: " + decl_ev),
                _ACTIONS[ADVISORY_REWARN], component))
        else:
            ev.findings.append(ParityFinding(
                target.repo_id, sid, WARN_UNDECLARED, SEV_WARN, _ascii(evidence),
                "ALIGN version or DECLARE-LOCAL (drift = WARN, never a block)",
                component))


def _eval_stale(manifest: dict, baseline: dict, target: RepoTarget, facts: dict,
                allowlist: list, ev: _RepoEval) -> None:
    """ADR-75-class decoration: a declaration that maps to a manifest surface (or a
    dependency-baseline row) which showed NO divergence this run is STALE (waivers
    must not rot into paper suppressions). A surface that DID diverge is never
    stale-decorated, whatever consumed the declaration (codex 2026-07-13).
    Declarations mapping to nothing are inert (digest unmapped section, never a WARN)."""
    waiver_to_row = {str(r.get("waiver_component") or r["id"]): r
                     for r in manifest["surfaces"]}
    dep_components = {}
    for dep in baseline.get("dependencies", []):
        comp = str(dep.get("waiver_component") or f"dep-{dep['name']}")
        dep_components[comp] = dep
    for entry in allowlist:
        component = entry.component.strip()
        if not component or component in ev.consumed or component in ev.diverged:
            continue
        dep = dep_components.get(component)
        if dep is not None:
            applies = dep.get("applies_to") or ["hub", "consumer"]
            if target.role in applies or target.repo_id in applies:
                ev.findings.append(ParityFinding(
                    target.repo_id, f"dep-{dep['name']}", STALE_DECLARATION, SEV_WARN,
                    _ascii(f"declaration '{component}' matches no live dependency "
                           f"drift (state: at parity) -- stale decoration"),
                    _ACTIONS[STALE_DECLARATION], component))
            continue
        row = waiver_to_row.get(component)
        if row is None:
            continue  # unmapped -> inert (digest info section)
        if _tier_for(row, target.repo_id, target.role) is None:
            continue  # not applicable to this repo -> inert here
        ev.findings.append(ParityFinding(
            target.repo_id, row["id"], STALE_DECLARATION, SEV_WARN,
            _ascii(f"declaration '{component}' matches no live divergence on this "
                   f"surface (state: at parity) -- stale decoration"),
            _ACTIONS[STALE_DECLARATION], component))


def unmapped_declarations(manifest: dict, targets: list[RepoTarget],
                          allowlists: dict[str, list],
                          consumed_by_repo: dict[str, set]) -> dict[str, list[str]]:
    """Per-repo declarations that suppressed nothing this run and produced no stale
    finding: either the component maps to NO manifest surface (inert by the
    Informant's own contract -- unknown components match nothing) or it maps to a
    surface not applicable to that repo (inert HERE). Listed for awareness, never a
    WARN -- consumer files are not this checker's to churn."""
    waiver_to_row = {str(r.get("waiver_component") or r["id"]): r
                     for r in manifest["surfaces"]}
    out: dict[str, list[str]] = {}
    for target in targets:
        consumed = consumed_by_repo.get(target.repo_id, set())
        names = []
        for entry in allowlists.get(target.repo_id, []):
            c = entry.component.strip()
            if not c or c in consumed:
                continue
            row = waiver_to_row.get(c)
            if row is None:
                names.append(f"{c} (no v1 surface)")
            elif _tier_for(row, target.repo_id, target.role) is None:
                names.append(f"{c} (surface not applicable to this repo; inert here)")
            # applicable-and-unconsumed -> the stale finding already covers it
        if names:
            out[target.repo_id] = sorted(set(names))
    return out


# ---------------------------------------------------------------------------
# Digest (gitignored, atomic, ASCII).
# ---------------------------------------------------------------------------


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".fleet-parity-",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh_:
            fh_.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def summarize(findings: list[ParityFinding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.verdict] = counts.get(f.verdict, 0) + 1
    return counts


def surface_line(findings: list[ParityFinding], targets: list[RepoTarget]) -> str:
    c = summarize(findings)
    walked = sum(1 for t in targets if t.root is not None and t.role != "pre-deploy")
    return (f"[fleet-parity] {walked} repo(s) walked: "
            f"{c.get(AT_PARITY, 0)} at-parity, {c.get(PASS_DECLARED, 0)} pass-declared, "
            f"{c.get(WARN_UNDECLARED, 0)} warn-undeclared, "
            f"{c.get(MUST_ABSENT, 0)} must-absent, "
            f"{c.get(TOMBSTONE_VIOLATED, 0)} tombstone-violated, "
            f"{c.get(ADVISORY_REWARN, 0)} advisory-rewarn, "
            f"{c.get(STALE_DECLARATION, 0)} stale, {c.get(REFUSED, 0)} refused "
            f"-- see logs/FLEET-PARITY.md")


def render_digest(findings: list[ParityFinding], targets: list[RepoTarget],
                  facts_by_repo: dict[str, dict], run_date: str, versions: dict,
                  unmapped: dict[str, list[str]]) -> str:
    lines = [
        "# Fleet parity -- #328 conformance walk (WARN-only v1)",
        "",
        f"run_date: {run_date}",
        f"source_version: checker {versions['checker']} / manifest "
        f"{versions['manifest']} / baseline {versions['baseline']}",
        "",
        "Read-only walk (ADR-28/36) of the registered fleet against "
        "ecosystem/parity-surfaces.yaml + ecosystem/dependency-baseline.yaml.",
        "Verdict grammar: AT-PARITY / PASS-declared / WARN-undeclared / MUST-absent /",
        "tombstone-violated (+ advisory-rewarn, stale-declaration, refused, unavailable,",
        "skipped-pre-deploy, tracked-ephemera). Severity labels are REPORT labels;",
        "process posture is WARN-only: this run gates nothing (section 9b).",
        "",
        "## Targets",
        "",
    ]
    for t in targets:
        facts = facts_by_repo.get(t.repo_id, {})
        head = facts.get("head", "-")
        dirty = "dirty" if facts.get("dirty") else "clean"
        rootnote = str(t.root) if t.root else t.note
        hp = facts.get("hooks_path_cfg")
        hp_note = f"; core.hooksPath={hp}" if hp else ""
        lines.append(f"- {t.repo_id} [{t.role}] head={head[:9] if head != '-' else '-'} "
                     f"{dirty if facts else ''} -- {_ascii(rootnote)}{_ascii(hp_note)}")
    lines += ["", "## Findings (non-at-parity first)", ""]
    order = {MUST_ABSENT: 0, TOMBSTONE_VIOLATED: 1, WARN_UNDECLARED: 2,
             TRACKED_EPHEMERA: 3, ADVISORY_REWARN: 4, STALE_DECLARATION: 5, REFUSED: 6,
             UNAVAILABLE: 7, SKIPPED_PRE_DEPLOY: 8, PASS_DECLARED: 9, AT_PARITY: 10}
    for f in sorted(findings, key=lambda f: (order.get(f.verdict, 99), f.repo_id,
                                             f.surface_id, f.evidence)):
        if f.verdict == AT_PARITY:
            continue
        lines.append(f"- {f.repo_id} :: {f.surface_id} :: **{f.verdict}** "
                     f"[{f.severity}] {f.evidence}"
                     + (f" | action: {f.action}" if f.action and f.action != "-" else ""))
    at_parity = [f for f in findings if f.verdict == AT_PARITY]
    lines += ["", f"## At parity ({len(at_parity)} row(s) -- counted, not listed)", ""]
    counts = summarize(findings)
    lines += ["## Counts", ""]
    for verdict in sorted(counts):
        lines.append(f"- {verdict}: {counts[verdict]}")
    if unmapped:
        lines += ["", "## Unmapped declarations (inert; awareness only)", ""]
        for repo_id in sorted(unmapped):
            lines.append(f"- {repo_id}: {', '.join(unmapped[repo_id])} -- declared "
                         f"components matching no v1 manifest surface (their files "
                         f"call them 'inert-but-recorded'); candidates for later "
                         f"manifest rows, never WARNs")
    lines += ["", surface_line(findings, targets), ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSONL events (FR-8/FR-13; checker runs ONLY; wholly fail-open).
# ---------------------------------------------------------------------------


def _event_id(ts_utc: str, repo_id: str, organ_id: str, event_type: str,
              component: str = "") -> str:
    # component disambiguates multi-finding surfaces (root-sweep, settings blocks):
    # same (ts, repo, organ) must NOT collapse under idempotent ingestion
    # (codex 2026-07-13 / Codex FR-07).
    raw = "|".join((ts_utc, repo_id, organ_id, event_type, component))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def emit_events(findings: list[ParityFinding], targets: list[RepoTarget],
                facts_by_repo: dict[str, dict], *, path: Path, mode: str,
                versions: dict, run_date: str,
                max_bytes: int = EVENTS_MAX_BYTES) -> str | None:
    """Append one schema-versioned JSONL line per finding + one run summary.
    FAIL-OPEN in whole: any error returns a one-line ASCII note and changes nothing
    else -- an emitter that could break the checker would reintroduce the failure
    class this layer exists to catch (FR-8)."""
    try:
        ts_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
        head_by_repo = {t.repo_id: facts_by_repo.get(t.repo_id, {}).get("head", "unknown")
                        for t in targets}
        dirty_by_repo = {t.repo_id: ("dirty" if facts_by_repo.get(t.repo_id, {}).get("dirty")
                                     else "clean") if t.repo_id in facts_by_repo
                         else "unknown" for t in targets}
        lines = []
        for f in findings:
            lines.append(json.dumps({
                "schema_version": 1,
                "event_id": _event_id(ts_utc, f.repo_id, f.surface_id,
                                      "parity-verdict", f.waiver_component or ""),
                "ts_utc": ts_utc,
                "repo_id": f.repo_id,
                "repo_head": head_by_repo.get(f.repo_id, "unknown"),
                "dirty_state": dirty_by_repo.get(f.repo_id, "unknown"),
                "organ_id": f.surface_id,
                "component": f.waiver_component or "",
                "event_type": "parity-verdict",
                "severity": f.severity,
                "verdict": f.verdict,
                "mode": mode,
                "source_version": versions,
                "evidence_ref": f"logs/FLEET-PARITY.md#{f.repo_id}/{f.surface_id}",
            }))
        counts = summarize(findings)
        lines.append(json.dumps({
            "schema_version": 1,
            "event_id": _event_id(ts_utc, "fleet", "fleet_parity", "checker-run"),
            "ts_utc": ts_utc,
            "repo_id": "fleet",
            "repo_head": head_by_repo.get(".dev-knowledge", "unknown"),
            "dirty_state": dirty_by_repo.get(".dev-knowledge", "unknown"),
            "organ_id": "fleet_parity",
            "event_type": "checker-run",
            "severity": "info",
            "verdict": "completed",
            "mode": mode,
            "run_date": run_date,
            "counts": counts,
            "source_version": versions,
            "evidence_ref": "logs/FLEET-PARITY.md",
        }))
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.stat().st_size > max_bytes:
            os.replace(path, Path(str(path) + ".1"))  # single backup; Windows-safe
        with open(path, "a", encoding="utf-8", newline="\n") as fh_:
            for line in lines:
                fh_.write(line + "\n")
        return None
    except Exception as exc:  # noqa: BLE001 -- fail-open BY CONTRACT (FR-8)
        return f"events emission skipped (fail-open): {_ascii(repr(exc))}"


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def _parse_overrides(pairs: tuple[str, ...]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for pair in pairs:
        name, _, p = pair.partition("=")
        if name and p:
            out[name] = Path(p)
    return out


@click.command()
@click.option("--run-date", required=True,
              help="Verdict run date YYYY-MM-DD -- a parameter, never wall-clock.")
@click.option("--manifest", "manifest_path", default=str(DEFAULT_MANIFEST),
              show_default=False, help="Parity manifest path (tests may override).")
@click.option("--baseline", "baseline_path", default=str(DEFAULT_BASELINE),
              help="Dependency baseline path.")
@click.option("--registry", "registry_path", default=str(DEFAULT_REGISTRY),
              help="deployed-versions registry path.")
@click.option("--ecosystem-dir", "ecosystem_dir", default=str(DEFAULT_ECOSYSTEM_DIR),
              help="ecosystem/ dir holding <repo>/state.yaml pointers.")
@click.option("--repo", "only_repos", multiple=True,
              help="Walk only these repo ids (subset run; digest header notes it).")
@click.option("--repo-root", "repo_roots", multiple=True, metavar="NAME=PATH",
              help="Explicit consumer root override(s); wins over state.yaml.")
@click.option("--hub-root", "hub_root_opt", default=None,
              help="Override the hub root (tests; default = this checkout).")
@click.option("--write/--no-write", "write", default=True,
              help="Write the gitignored logs/FLEET-PARITY.md digest.")
@click.option("--events/--no-events", "events", default=True,
              help="Append JSONL events (fail-open; never affects verdicts).")
@click.option("--events-path", "events_path", default=str(EVENTS_PATH),
              help="JSONL events path (gitignored).")
@click.option("--max-events-bytes", "max_events_bytes", default=EVENTS_MAX_BYTES,
              type=int, help="Rotation threshold for the events file.")
@click.option("--mode", "mode", type=click.Choice(["actual", "synthetic"]),
              default="actual",
              help="Event mode: synthetic runs never count as fleet history.")
@click.option("--deploy-manifest", "deploy_manifest_path", default=None,
              help="Deploy manifest override (tests; default = highest deploy/manifest-v*).")
def main(run_date: str, manifest_path: str, baseline_path: str, registry_path: str,
         ecosystem_dir: str, only_repos: tuple, repo_roots: tuple, hub_root_opt,
         write: bool, events: bool, events_path: str, max_events_bytes: int,
         mode: str, deploy_manifest_path) -> None:
    """Deterministic read-only fleet-parity walk (#328). WARN-only: a completed run
    exits 0 whatever it finds; exit 2 only when the parity manifest is unusable (and
    then no digest is written -- never silently green)."""
    hub_root = Path(hub_root_opt) if hub_root_opt else _REPO_ROOT
    # exact YYYY-MM-DD shape THEN calendar validity: fromisoformat alone also accepts
    # compact/week forms like 20260713 (codex delta re-review 2026-07-13); a malformed
    # run_date silently disabling shelf-life is the refused class either way
    try:
        from datetime import date as _date
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", run_date):
            raise ValueError("shape")
        _date.fromisoformat(run_date)
    except ValueError:
        click.echo(f"fleet-parity: REFUSED -- --run-date {run_date!r} is not a valid "
                   f"YYYY-MM-DD date", err=True)
        sys.exit(2)
    try:
        manifest, refusals = load_manifest(Path(manifest_path))
    except ManifestUnreadable as exc:
        click.echo(f"fleet-parity: REFUSED -- {_ascii(str(exc))}", err=True)
        sys.exit(2)
    baseline, base_refusals = load_baseline(Path(baseline_path))
    refusals += base_refusals

    targets, fleet_findings = resolve_fleet(manifest, hub_root, Path(registry_path),
                                            Path(ecosystem_dir),
                                            _parse_overrides(repo_roots))
    if only_repos:
        targets = [t for t in targets if t.repo_id in set(only_repos)]

    facts_by_repo: dict[str, dict] = {}
    allowlists: dict[str, list] = {}
    for t in targets:
        if t.root is not None and t.role != "pre-deploy":
            facts_by_repo[t.repo_id] = collect_facts(t, manifest, baseline, hub_root,
                                                     Path(registry_path))
            allowlists[t.repo_id] = ec.read_allowlist(t.root)

    deploy_manifest = (ec._read_yaml(Path(deploy_manifest_path))
                       if deploy_manifest_path else ec._latest_manifest())
    verdict_findings, consumed_by_repo = verdicts(
        manifest, baseline, targets, facts_by_repo, allowlists, deploy_manifest,
        run_date)
    findings = refusals + fleet_findings + verdict_findings
    unmapped = unmapped_declarations(manifest, targets, allowlists, consumed_by_repo)
    versions = {"checker": __version__, "manifest": str(manifest.get("version")),
                "baseline": str(baseline.get("version", "-"))}

    digest = render_digest(findings, targets, facts_by_repo, run_date, versions,
                           unmapped)
    if only_repos:
        digest = digest.replace("## Targets",
                                f"SUBSET RUN: {', '.join(sorted(only_repos))}\n\n## Targets", 1)
    if write:
        try:
            _atomic_write(DIGEST_PATH, digest)
            click.echo(f"wrote {DIGEST_PATH.relative_to(_REPO_ROOT)}")
        except OSError as exc:
            # digest is ONE of three output channels (stdout + events remain); a
            # write failure is loud but never converts a completed run into a crash
            # exit (codex 2026-07-13; exit 2 stays manifest-unreadable-only)
            click.echo(f"digest write skipped (fail-open): {_ascii(repr(exc))}")
    if events:
        note = emit_events(findings, targets, facts_by_repo, path=Path(events_path),
                           mode=mode, versions=versions, run_date=run_date,
                           max_bytes=max_events_bytes)
        if note:
            click.echo(note)

    click.echo(surface_line(findings, targets))
    for f in sorted(findings, key=lambda f: (f.repo_id, f.surface_id)):
        if f.verdict not in (AT_PARITY,):
            click.echo(f"  {f.repo_id:26} {f.surface_id:32} {f.verdict:18} {f.evidence[:100]}")
    sys.exit(0)


if __name__ == "__main__":
    main()
