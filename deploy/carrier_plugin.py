"""deploy/carrier_plugin.py — the tier1-lifecycle CC-plugin carrier (ADR-92 C5).

The fourth and final carrier — and the only one that reconciles via an **external
CLI** (``claude plugin …``). It installs/enables the ``tier1-lifecycle`` plugin
from the hub marketplace at **project scope** in a consumer repo, toward the
plugin version the hub source declares.

Why this carrier is special: its correctness cannot be judged from the install
command's self-report. ``claude plugin install`` no-ops ("already installed") on a
repo that's already installed, and exit 0 says only that the command ran — not
that the consumer is at the target version + enabled. So the carrier judges from
the **resulting installed state** (``claude plugin list --json`` + the consumer's
``.claude/settings.json``), never from stdout/exit alone (ADR-92 Decision 9; the
whole point of deterministic verification gating the version-record write).

Target shape (the v1.0.0 manifest's ``tier1-plugin`` entry)::

    plugin: tier1-lifecycle@dev-knowledge-methodology   # the install arg + the list `id`
    marketplace: dev-knowledge-methodology              # the marketplace name
    scope: project                                      # writes the consumer .claude/settings.json

The **target version** is read live from the hub's plugin manifest
(``plugins/tier1-lifecycle/.claude-plugin/plugin.json`` ``version``) — a SPEC read,
like global-config reading the hub source bytes (D9-permitted). So the manifest
entry stays minimal (no embedded version that could drift from the source).

State model (the Decision-6 reconcile model, all four states exercised):

- ``ABSENT``                — the plugin is not installed for this consumer.
- ``PRESENT_DRIFTED``       — installed for this consumer but **not enabled**.
- ``PRESENT_WRONG_VERSION`` — installed + enabled, but at a non-target version.
- ``PRESENT_CORRECT``       — installed + enabled at the target version (apply no-ops).

CLI mechanics encoded (ADR-92 finding (a), confirmed live 2026-06-29):

- ``marketplace add <source> --scope project`` must precede ``install`` on a fresh
  cache (else "Plugin not found in marketplace"); it is idempotent (already-added
  is tolerated).
- ``plugin install <plugin> --scope project`` **no-ops** on an already-installed
  repo — it does NOT upgrade; the upgrade path is ``plugin update --scope project``.
- live activation needs a session restart — irrelevant here: the carrier needs the
  consumer *applied + verified* (the settings record + the installed version),
  not the plugin live in the current session.

Test safety / determinism: the CLI invoker is **injectable** (constructor
``runner``), so unit tests drive a mock and **never invoke the real ``claude``**;
the one real install is the isolated throwaway smoke-test (ADR-92 finding (a)'s
"confirmed at CLI-surface only" caveat). ``apply`` runs every command with
``cwd = repo_root`` so ``--scope project`` writes the *consumer's* settings.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contract import ApplyResult, Carrier, CarrierState, VerifyResult

log = logging.getLogger(__name__)

CARRIER_ID = "tier1-plugin"

# The hub root (this module lives in deploy/, so the hub is its parent's parent).
# Used both as the marketplace SOURCE for `marketplace add` and to read the plugin
# manifest's declared version (the spec).
_HUB_ROOT = Path(__file__).resolve().parent.parent
_PLUGIN_MANIFEST = (
    _HUB_ROOT / "plugins" / "tier1-lifecycle" / ".claude-plugin" / "plugin.json"
)

DEFAULT_PLUGIN = "tier1-lifecycle@dev-knowledge-methodology"
DEFAULT_MARKETPLACE = "dev-knowledge-methodology"
DEFAULT_SCOPE = "project"


# ---------------------------------------------------------------------------
# CLI transport — pure I/O (NOT a correctness judgment). Sharing this between
# detect/verify is D9-fine: it fetches state, it does not judge state-vs-target
# (the forbidden sharing is the judgment, in _classify_plugin vs _verify_plugin).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CmdResult:
    """The outcome of one CLI invocation (what an injected runner returns)."""

    returncode: int
    stdout: str = ""
    stderr: str = ""


class PluginCliError(RuntimeError):
    """A `claude plugin …` command failed in a way the carrier won't paper over.

    Raised on a non-zero install/update (a real failure must surface, never be
    silently recorded) or unparseable `plugin list --json`. The deploy tool (C2)
    catches it; ``verify`` catches it and reports ``ok=False`` rather than crash.
    """


def _default_runner(args: Sequence[str], cwd: Path) -> CmdResult:
    """Real CLI invoker — resolves ``claude`` via PATH; binary I/O + explicit UTF-8.

    NOT text mode (the Windows-text-mode I/O class, same as the git invoker in
    tool.py): on Windows ``text=True`` decodes the CLI's stdout with the locale
    encoding (cp1252), which would mojibake any non-ASCII in ``plugin list --json``
    (a project path / plugin name) before it is JSON-parsed. Binary capture +
    explicit UTF-8 keeps the JSON byte-faithful.
    """
    exe = shutil.which(args[0]) or args[0]
    proc = subprocess.run(  # noqa: S603 — fixed argv, no shell, binary UTF-8 I/O
        [exe, *args[1:]],
        cwd=str(cwd),
        capture_output=True,
    )
    return CmdResult(
        proc.returncode,
        (proc.stdout or b"").decode("utf-8", "replace"),
        (proc.stderr or b"").decode("utf-8", "replace"),
    )


Runner = Callable[[Sequence[str], Path], CmdResult]


# ---------------------------------------------------------------------------
# Target model + the spec read (the hub plugin manifest version).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PluginTarget:
    plugin: str       # the install arg AND the `id` in `plugin list --json`
    marketplace: str  # the marketplace name (for context / messages)
    scope: str        # "project" -> writes the consumer's .claude/settings.json


def parse_target(target: Any) -> PluginTarget:
    """Interpret the opaque manifest entry into the carrier's typed model."""
    t = target or {}
    return PluginTarget(
        plugin=t.get("plugin", DEFAULT_PLUGIN),
        marketplace=t.get("marketplace", DEFAULT_MARKETPLACE),
        scope=t.get("scope", DEFAULT_SCOPE),
    )


def _read_target_version(manifest_path: Path = _PLUGIN_MANIFEST) -> str:
    """The spec version — the hub plugin manifest's ``version`` (D9-permitted read).

    Like global-config reading the hub source bytes: this reads the SPEC (what the
    consumer should match), not the consumer's own state. Shared by detect/verify.
    """
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return str(data["version"])


# ---------------------------------------------------------------------------
# Shared pure helpers — path-normalised projectPath filter (a data SELECT, not a
# judgment; D9-permitted, like target-parsing).
# ---------------------------------------------------------------------------


def _norm(p: str | Path) -> str:
    """Case/separator-normalised absolute path (no filesystem touch — test-safe)."""
    return os.path.normcase(os.path.normpath(os.path.abspath(str(p))))


def _entries_for_repo(
    entries: list[dict[str, Any]], plugin_id: str, repo_root: Path
) -> list[dict[str, Any]]:
    """Select the `plugin list --json` rows for THIS plugin in THIS consumer repo."""
    want = _norm(repo_root)
    out: list[dict[str, Any]] = []
    for e in entries:
        if not isinstance(e, dict) or e.get("id") != plugin_id:
            continue
        pp = e.get("projectPath")
        if pp and _norm(pp) == want:
            out.append(e)
    return out


def _plugin_list_entries(runner: Runner, cwd: Path) -> list[dict[str, Any]]:
    """Fetch + parse `claude plugin list --json` (pure transport; raises on failure)."""
    res = runner(["claude", "plugin", "list", "--json"], cwd)
    if res.returncode != 0:
        raise PluginCliError(f"`plugin list --json` exited {res.returncode}: {res.stderr.strip()}")
    try:
        data = json.loads(res.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise PluginCliError(f"`plugin list --json` output did not parse: {exc}") from exc
    return data if isinstance(data, list) else []


# ---------------------------------------------------------------------------
# detect path — _classify_plugin (detect's correctness judgment).
# ---------------------------------------------------------------------------


def _classify_plugin(matches: list[dict[str, Any]], target_version: str) -> CarrierState:
    """detect's judgment: this consumer's install rows -> CarrierState.

    none                              -> ABSENT
    present but none enabled          -> PRESENT_DRIFTED (installed, not enabled)
    enabled at a non-target version   -> PRESENT_WRONG_VERSION
    enabled at the target version     -> PRESENT_CORRECT
    """
    if not matches:
        return CarrierState.ABSENT
    enabled = [e for e in matches if e.get("enabled") is True]
    if not enabled:
        return CarrierState.PRESENT_DRIFTED
    if target_version in {str(e.get("version")) for e in enabled}:
        return CarrierState.PRESENT_CORRECT
    return CarrierState.PRESENT_WRONG_VERSION


# ---------------------------------------------------------------------------
# verify path — INDEPENDENT of detect (D9). Its OWN judgment (_verify_plugin),
# and it leans on a DIFFERENT primary source detect never reads — the consumer's
# .claude/settings.json `enabledPlugins` — cross-checked with a fresh plugin-list
# version read. Shares no correctness-judgment helper with _classify_plugin.
# ---------------------------------------------------------------------------


def _verify_plugin(
    settings: dict[str, Any],
    entries: list[dict[str, Any]],
    plugin_id: str,
    repo_root: Path,
    target_version: str,
) -> list[str]:
    """verify's independent judgment: return unmet requirements (empty => satisfied).

    Two independent confirmations, so a bug in detect's _classify_plugin cannot be
    mirrored here:
      1. the consumer's .claude/settings.json marks the plugin enabled (a source
         detect does not consult at all);
      2. `plugin list --json` shows it installed + enabled at the target version
         for this consumer (its OWN filter + compare, asserted directly).
    """
    failures: list[str] = []

    enabled_map = settings.get("enabledPlugins", {}) if isinstance(settings, dict) else {}
    if enabled_map.get(plugin_id) is not True:
        failures.append(f"{plugin_id} not enabled in consumer .claude/settings.json")

    matches = _entries_for_repo(entries, plugin_id, repo_root)
    live_enabled = [e for e in matches if e.get("enabled") is True]
    if not live_enabled:
        failures.append(f"{plugin_id} not installed+enabled for {repo_root} (plugin list)")
    elif target_version not in {str(e.get("version")) for e in live_enabled}:
        have = sorted({str(e.get("version")) for e in live_enabled})
        failures.append(f"{plugin_id} version {have} != target {target_version}")
    return failures


# ---------------------------------------------------------------------------
# The carrier.
# ---------------------------------------------------------------------------


class PluginCarrier(Carrier):
    """tier1-lifecycle plugin carrier — installs/enables at project scope.

    Bound to one consumer repo (``repo_root``): every CLI command runs with
    ``cwd = repo_root`` so ``--scope project`` writes that consumer's
    ``.claude/settings.json``. The CLI invoker (``runner``) is injectable so the
    unit suite never calls the real ``claude`` binary.
    """

    carrier_id = CARRIER_ID

    def __init__(
        self,
        repo_root: Path | str,
        runner: Runner | None = None,
        marketplace_source: Path | str | None = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self._runner: Runner = runner or _default_runner
        # The SOURCE passed to `marketplace add` — the hub dir (default) or an
        # override (a throwaway smoke-test points it at the real hub explicitly).
        self.marketplace_source = Path(marketplace_source) if marketplace_source else _HUB_ROOT

    # -- spec + state reads -------------------------------------------------

    def _target_version(self) -> str:
        return _read_target_version()

    def _settings_path(self) -> Path:
        return self.repo_root / ".claude" / "settings.json"

    def _read_settings(self) -> dict[str, Any]:
        """Fresh read of the consumer's .claude/settings.json (verify's source)."""
        path = self._settings_path()
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    # -- contract -----------------------------------------------------------

    def detect(self, target: Any) -> CarrierState:
        t = parse_target(target)
        entries = _plugin_list_entries(self._runner, self.repo_root)
        matches = _entries_for_repo(entries, t.plugin, self.repo_root)
        state = _classify_plugin(matches, self._target_version())
        log.debug("tier1-plugin detect: %s @ %s -> %s", t.plugin, self.repo_root, state)
        return state

    def apply(self, target: Any) -> ApplyResult:
        t = parse_target(target)
        state = self.detect(target)
        if state is CarrierState.PRESENT_CORRECT:
            return ApplyResult(changed=False, detail="already installed+enabled at target version")

        changes: list[str] = []
        # 1. Ensure the marketplace is known (required before install on a fresh
        #    cache; idempotent — an already-added marketplace is tolerated).
        self._marketplace_add(t, changes)
        # 2. Install (absent / drifted) or update (wrong version). A non-zero here
        #    is a real failure — surface it, do not record a partial apply.
        if state is CarrierState.PRESENT_WRONG_VERSION:
            self._run_checked(["claude", "plugin", "update", t.plugin, "--scope", t.scope])
            changes.append(f"plugin update {t.plugin} --scope {t.scope}")
        else:  # ABSENT or PRESENT_DRIFTED
            self._run_checked(["claude", "plugin", "install", t.plugin, "--scope", t.scope])
            changes.append(f"plugin install {t.plugin} --scope {t.scope}")
        log.info("tier1-plugin apply: %s -> %s", state, changes)
        return ApplyResult(changed=True, changes=tuple(changes), detail=f"{state.value} -> reconciled")

    def verify(self, target: Any) -> VerifyResult:
        t = parse_target(target)
        # Independent judgment — does NOT call _classify_plugin (D9). Primary source
        # is the consumer's settings.json (which detect never reads), cross-checked
        # with a fresh plugin-list version read.
        try:
            entries = _plugin_list_entries(self._runner, self.repo_root)
        except PluginCliError as exc:
            return VerifyResult(ok=False, failures=(str(exc),), detail="plugin list failed")
        settings = self._read_settings()
        failures = _verify_plugin(
            settings, entries, t.plugin, self.repo_root, self._target_version()
        )
        ok = not failures
        return VerifyResult(
            ok=ok,
            failures=tuple(failures),
            detail="installed+enabled at target" if ok else f"{len(failures)} unmet",
        )

    # -- CLI helpers --------------------------------------------------------

    def _marketplace_add(self, t: PluginTarget, changes: list[str]) -> None:
        """`marketplace add <source> --scope project`, tolerating already-added."""
        res = self._runner(
            ["claude", "plugin", "marketplace", "add", str(self.marketplace_source),
             "--scope", t.scope],
            self.repo_root,
        )
        if res.returncode == 0:
            changes.append(f"marketplace add {t.marketplace} --scope {t.scope}")
            return
        blob = f"{res.stdout}\n{res.stderr}".lower()
        if "already" in blob or "exists" in blob:
            return  # idempotent: marketplace already known, nothing to record
        raise PluginCliError(
            f"`marketplace add` exited {res.returncode}: {res.stderr.strip()}"
        )

    def _run_checked(self, args: Sequence[str]) -> CmdResult:
        """Run a CLI command; raise PluginCliError on non-zero (no silent partial)."""
        res = self._runner(args, self.repo_root)
        if res.returncode != 0:
            raise PluginCliError(
                f"`{' '.join(args)}` exited {res.returncode}: {res.stderr.strip()}"
            )
        return res
