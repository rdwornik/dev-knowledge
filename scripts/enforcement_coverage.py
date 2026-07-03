#!/usr/bin/env python
"""enforcement_coverage.py — the Informant Organ (enforcement-coverage reporter).

Stage 2 of the enforcement-transfer epic. A **read-only** fleet reporter that measures,
per consumer repo x per hub enforcement organ, whether each mechanism is
**enforcing-in-effect locally** — testing whether the gate FIRES, not whether files are
PRESENT. The deploy subsystem (ADR-92/93) carries the *presence* of the methodology to the
consumers; nothing carries its *enforcement*. This organ makes that gap mechanically visible.

Why firing-not-presence: every prior fleet audit reported CONFORMS by checking presence and
missed that nothing enforced. A Stop hook can be registered and structurally "wired" yet emit
`additionalContext` instead of `{"decision":"block"}` — only RUNNING it tells enforcement from
inert. So static detection is a candidate PRE-FILTER, never a verdict; the ``fire_test`` (a
floor_conformance-style clone+inject+assert-block) is the sole truth-maker for ``enforcing-local``.

The five hub enforcement organs are NOT homogeneous (this is the load-bearing refinement — a flat
"all absent" map manufactures a fake gap). They split by portability:

  * Group A — portable, deployable as a consumer-local gate:
      ``canonical_freshness`` (audit.py takes repo_path, no guard) and
      ``reconciled_versions`` (portable but a no-op PASS with zero ``reconciled_with`` edges).
  * Group B — hub-only-GUARDED (``if repo_path != _REPO_ROOT: return pass``): ``doc_claims`` and
      ``git_backlog_drift``. NO consumer wiring can make these fire without changing the organ's
      code. Reported ``hub-scoped`` — and that verdict is DEMONSTRATED, not source-read: the organ
      is invoked off-hub and observed to return the hub-only PASS despite an injected violation
      (see ``_demonstrate_hub_scoped``). If the guard ever stops short-circuiting, the demonstration
      flips and the cell is surfaced, never forced green.
  * Group C — hub-hardcoded standalone (``session_end_backpressure.py``), carried by no manifest
      carrier. Reported ``absent`` on consumers (the genuine, currently-unclosable-without-porting
      gap), with a non-portability note.

Tier-1 verdict vocabulary: ``enforcing-local | absent | hub-scoped | n/a-no-edges`` (+ the
static-only leg label ``present-unverified`` where a candidate exists but no fire_test was run).
Tier-2 (a bounded PRESENCE surface, the 4 deploy manifest carriers): ``present-and-wired |
present-not-wired | absent`` — honestly labelled presence, kept visually separate from the Tier-1
firing matrix (a carrier PRESENT_CORRECT proves bytes present, not that the git hook is installed).

Two runtimes (the floor_conformance Layer-1/Layer-2 split):
  * ``evaluate_static`` — cheap applicability + locate only, NEVER clones. Feeds the read-only
    ``audit.py::check_enforcement_coverage`` leg (runs on every hub commit; must not clone 4 repos).
  * ``evaluate_full`` / the CLI — runs the expensive ``fire_test`` (clone+inject) for any organ whose
    locate returns ``candidate``. On the live fleet no consumer is a candidate for any organ, so the
    fire path is exercised only by the hermetic fixtures in tests/test_enforcement_coverage.py.

Layer-2 invariant (ADR-28/36): this is a read-only validator. It reads consumer trees (and clones
them to a throwaway temp dir for fire_test), writes ONLY the gitignored digest
``logs/ENFORCEMENT-COVERAGE.md``, and mutates no consumer and no enforcement organ.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import click
import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_DEPLOY_DIR = _REPO_ROOT / "deploy"
_DIGEST_PATH = _REPO_ROOT / "logs" / "ENFORCEMENT-COVERAGE.md"

# Tier-1 verdicts (the honest 4-value map + the static-only leg label).
ENFORCING_LOCAL = "enforcing-local"
ABSENT = "absent"
HUB_SCOPED = "hub-scoped"
NA_NO_EDGES = "n/a-no-edges"
NA_NO_JOURNAL = "n/a-no-journal"
PRESENT_UNVERIFIED = "present-unverified"  # static path only: candidate found, fire_test not run

# Tier-2 presence labels (mapped from the deploy carriers' CarrierState).
T2_PRESENT_WIRED = "present-and-wired"
T2_PRESENT_NOT_WIRED = "present-not-wired"
T2_ABSENT = "absent"
T2_ERROR = "error"


# ---------------------------------------------------------------------------
# Result shapes.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Cell:
    """One (consumer x Tier-1 organ) result. ``verdict`` is the honest-map value;
    ``fired`` is True/False only when a fire_test actually ran, else None."""

    organ_id: str
    verdict: str
    evidence: str
    fired: bool | None = None


@dataclass(frozen=True)
class Tier2Cell:
    """One (consumer x deploy carrier) PRESENCE result — carrier detect() mapped to a label."""

    carrier_id: str
    state: str
    evidence: str


@dataclass(frozen=True)
class ConsumerReport:
    """A single consumer's full row: Tier-1 firing cells + Tier-2 presence cells."""

    name: str
    root: str
    tier1: tuple[Cell, ...]
    tier2: tuple[Tier2Cell, ...]


# ---------------------------------------------------------------------------
# Config readers (committed-vs-working-tree caveat: the static leg reads the consumer's
# WORKING tree; the CLI's fire_test reads a fresh CLONE = committed state. Verdicts on the
# live fleet are `absent` regardless, so the distinction does not change the answer today;
# evidence is stamped so the reader knows which was read).
# ---------------------------------------------------------------------------


def _read_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _precommit_hooks(root: Path) -> list[dict]:
    """Every hook dict across every repo stanza in the consumer's .pre-commit-config.yaml."""
    cfg = _read_yaml(root / ".pre-commit-config.yaml")
    hooks: list[dict] = []
    for repo in cfg.get("repos") or []:
        if isinstance(repo, dict):
            for h in repo.get("hooks") or []:
                if isinstance(h, dict):
                    hooks.append(h)
    return hooks


def _precommit_hook_strings(root: Path) -> list[str]:
    """Identity strings (id / name / entry) for every pre-commit hook — the locate scan surface."""
    out: list[str] = []
    for h in _precommit_hooks(root):
        for key in ("id", "name", "entry"):
            v = h.get(key)
            if isinstance(v, str) and v:
                out.append(v)
    return out


def _settings_hook_commands(root: Path, event: str | None = None) -> list[str]:
    """Every hook ``command`` string in .claude/settings.json, optionally scoped to one event."""
    data = _read_json(root / ".claude" / "settings.json")
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return []
    events = [event] if event else list(hooks.keys())
    cmds: list[str] = []
    for ev in events:
        for group in hooks.get(ev) or []:
            if not isinstance(group, dict):
                continue
            for h in group.get("hooks") or []:
                if isinstance(h, dict) and isinstance(h.get("command"), str):
                    cmds.append(h["command"])
    return cmds


def _has_journal(root: Path) -> bool:
    return (root / "JOURNAL.md").exists()


_RECONCILED_RE = re.compile(r"^reconciled_with:\s*\S", re.MULTILINE)
_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".ruff_cache",
             ".pytest_cache", ".mypy_cache"}


def _has_reconciled_edge(root: Path) -> bool:
    """True iff any living-doc frontmatter in the consumer declares a ``reconciled_with:`` edge."""
    for md in root.rglob("*.md"):
        if any(part in _SKIP_DIRS or part == "worktrees" for part in md.parts):
            continue
        try:
            head = md.read_text(encoding="utf-8")[:2000]
        except OSError:
            continue
        if _RECONCILED_RE.search(head):
            return True
    return False


# ---------------------------------------------------------------------------
# Clone context for fire_test (reuses floor_conformance's proven Windows/autocrlf gotcha
# handling: -c core.autocrlf=false at clone, per-run PRE_COMMIT_HOME, read-only-bit teardown).
# Lazily imported so the audit-leg static path never pulls deploy/ or click-heavy modules.
# ---------------------------------------------------------------------------


def _ensure_deploy_on_path() -> None:
    if str(_DEPLOY_DIR) not in sys.path:
        sys.path.insert(0, str(_DEPLOY_DIR))


@contextlib.contextmanager
def _cloned_consumer(consumer: Path):
    """Yield (clone_path, env, fc) — a throwaway clone of the consumer with its OWN .git,
    plain-delete teardown. fire_test operates on committed state, never the live tree."""
    _ensure_deploy_on_path()
    import floor_conformance as fc  # noqa: E402  (lazy: fire_test path only)

    consumer = Path(consumer).resolve()
    if not (consumer / ".git").exists():
        raise RuntimeError(f"consumer is not a git repo: {consumer}")
    temp_root = Path(tempfile.mkdtemp(prefix="enfcov-"))
    env = {"PRE_COMMIT_HOME": str(temp_root / ".pc-home")}
    try:
        clone = temp_root / "clone"
        r = fc._run(
            ["git", "-c", "core.autocrlf=false", "clone", "--quiet", str(consumer), str(clone)],
            temp_root,
        )
        if r.returncode != 0:
            raise RuntimeError(f"clone failed: {r.stderr.strip()}")
        for cfg in (["core.autocrlf", "false"], ["user.email", "enfcov@example.com"],
                    ["user.name", "Enforcement Coverage"], ["commit.gpgsign", "false"]):
            fc._run(["git", "config", *cfg], clone, env)
        yield clone, env, fc
    finally:
        fc._rmtree_guarded(temp_root, temp_root.parent)


def _run_in(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    full = {**os.environ, **(env or {})}
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=full)


# ---------------------------------------------------------------------------
# Organ 1 — session_end_backpressure (Group C: JOURNAL Stop-block).
# ---------------------------------------------------------------------------

_BACKPRESSURE_TOKENS = ("session_end_backpressure", "backpressure", "journal-anchor",
                       "journal_anchor")
_PROPOSE_CLOSURES = "propose_closures"


def _seb_applicability(root: Path) -> tuple[str, str]:
    if not _has_journal(root):
        return (NA_NO_JOURNAL, "no root JOURNAL.md — the organ's semantics do not exist here")
    return ("applicable", "has root JOURNAL.md (Group C: hub-hardcoded standalone, no carrier deploys it)")


def _seb_candidate_command(root: Path) -> str | None:
    """The Stop command that references a session-end/JOURNAL-anchor script, EXCLUDING the
    non-blocking plugin propose_closures. (propose_closures is registered via enabledPlugins,
    not hooks.Stop, so it never appears here — the exclusion is belt-and-braces.)"""
    for cmd in _settings_hook_commands(root, "Stop"):
        low = cmd.lower()
        if _PROPOSE_CLOSURES in low:
            continue
        if any(tok in low for tok in _BACKPRESSURE_TOKENS):
            return cmd
    return None


def _seb_locate(root: Path) -> tuple[bool, str]:
    cmd = _seb_candidate_command(root)
    if cmd:
        return (True, f"candidate: hooks.Stop runs a backpressure script ({cmd!r})")
    return (False, "no blocking hooks.Stop backpressure script "
                   "(enabledPlugins:tier1-lifecycle -> propose_closures is non-blocking, excluded)")


_CLAUDE_PROJECT_DIR_RE = re.compile(r"\$\{?CLAUDE_PROJECT_DIR\}?")
_PY_TOKEN_RE = re.compile(r'["\']?([^"\'\s]+\.py)["\']?')


def _resolve_script(cmd: str, clone: Path) -> Path | None:
    # A replacement FUNCTION (not a string) so a Windows clone path's backslashes are not
    # misread as regex escape/backref sequences in the substitution.
    resolved = _CLAUDE_PROJECT_DIR_RE.sub(lambda _m: str(clone), cmd)
    m = _PY_TOKEN_RE.search(resolved)
    if not m:
        return None
    tok = m.group(1)
    p = Path(tok)
    if not p.is_absolute():
        p = clone / tok
    return p


def _seb_fire(consumer: Path) -> tuple[bool, str]:
    """FIRE test: create a shipped-but-unanchored clean-tree state, run the Stop hook, and
    require it to emit {"decision":"block"} with a JOURNAL reason. additionalContext/empty =
    NOT firing (this is exactly what separates a real backpressure gate from propose_closures)."""
    with _cloned_consumer(consumer) as (clone, env, _fc):
        cmd = _seb_candidate_command(clone)
        if not cmd:
            return (False, "no Stop backpressure command in the committed clone")
        script = _resolve_script(cmd, clone)
        if script is None or not script.exists():
            return (False, f"Stop script did not resolve/exist: {cmd!r}")
        (clone / "_enfcov_probe.txt").write_text("unanchored work\n", encoding="utf-8", newline="\n")
        _run_in(["git", "add", "_enfcov_probe.txt"], clone, env)
        c = _run_in(["git", "commit", "-m", "enfcov: shipped work, no JOURNAL SHA anchor"], clone, env)
        if c.returncode != 0:
            return (False, f"could not create the unanchored probe commit: {(c.stdout + c.stderr).strip()}")
        r = subprocess.run([sys.executable, str(script)], cwd=str(clone), input="{}",
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, **env})
        out = (r.stdout or "").strip()
        try:
            decision = json.loads(out) if out else {}
        except json.JSONDecodeError:
            decision = {}
        if isinstance(decision, dict) and decision.get("decision") == "block":
            reason = str(decision.get("reason", ""))
            journal = "JOURNAL" in reason or "anchor" in reason.lower()
            return (True, "Stop hook emitted decision:block on unanchored work"
                          + (" (JOURNAL reason)" if journal else ""))
        return (False, f"Stop hook did NOT block (out={out[:80]!r}) — inert/additionalContext, not enforcing")


# ---------------------------------------------------------------------------
# Organ 2 — canonical_freshness (Group A: stale last_reviewed gate).
# ---------------------------------------------------------------------------

_FRESHNESS_TOKENS = ("canonical_freshness", "last_reviewed")
# Exclusions the locate MUST NOT count as this organ (TOC != last_reviewed, etc.).
_FRESHNESS_FALSE_POSITIVES = ("toc-freshness", "toc-generate", "toc_freshness")


def _freshness_candidate(root: Path) -> tuple[bool, str]:
    strings = _precommit_hook_strings(root) + _settings_hook_commands(root)
    for s in strings:
        low = s.lower()
        if any(fp in low for fp in _FRESHNESS_FALSE_POSITIVES):
            continue  # toc-freshness is TOC freshness, NOT last_reviewed staleness
        if any(tok in low for tok in _FRESHNESS_TOKENS):
            return (True, f"candidate: a gate references canonical_freshness/last_reviewed ({s!r})")
    return (False, "no canonical_freshness/last_reviewed gate "
                   "(toc-freshness is TOC, not last_reviewed — excluded)")


def _freshness_applicability(root: Path) -> tuple[str, str]:
    return ("applicable", "Group A: portable — audit.py::check_canonical_freshness takes repo_path")


def _freshness_locate(root: Path) -> tuple[bool, str]:
    return _freshness_candidate(root)


_LAST_REVIEWED_RE = re.compile(r"(?m)^last_reviewed:\s*\d{4}-\d{2}-\d{2}\s*$")


def _freshness_files() -> list[str]:
    """The audit organ's own _FRESHNESS_FILES — lazily read so the module stays decoupled."""
    try:
        from scripts import audit as _audit  # noqa: E402
    except ImportError:
        _ensure_scripts_on_path()
        import audit as _audit  # noqa: E402
    return list(getattr(_audit, "_FRESHNESS_FILES", ["CLAUDE.md"]))


def _freshness_fire(consumer: Path) -> tuple[bool, str]:
    """FIRE test: make a _FRESHNESS_FILES doc A2-stale (last_reviewed predates its last commit),
    then commit an UNRELATED file through the wired gate and require the commit to be BLOCKED
    with HEAD unmoved."""
    with _cloned_consumer(consumer) as (clone, env, _fc):
        ok, ev = _freshness_candidate(clone)
        if not ok:
            return (False, "no canonical_freshness gate wired in the committed clone")
        target = next((f for f in _freshness_files() if (clone / f).exists()), None)
        if target is None:
            return (False, "no _FRESHNESS_FILES doc present to stale")
        doc = clone / target
        text = doc.read_text(encoding="utf-8")
        if _LAST_REVIEWED_RE.search(text):
            text = _LAST_REVIEWED_RE.sub("last_reviewed: 2020-01-01", text, count=1)
        else:
            return (False, f"{target} has no last_reviewed frontmatter to stale")
        doc.write_text(text, encoding="utf-8", newline="\n")
        # Setup commit bypasses the gate (--no-verify) so the file's last-commit-date is NOW while
        # last_reviewed=2020 -> A2 stale. The ASSERTION commit below runs the real gate.
        _run_in(["git", "add", target], clone, env)
        _run_in(["git", "commit", "--no-verify", "-m", "enfcov: stale-stamp setup"], clone, env)
        install = _run_in([sys.executable, "-m", "pre_commit", "install"], clone, env)
        if install.returncode != 0:
            return (False, f"pre-commit install failed: {(install.stdout + install.stderr).strip()}")
        head_before = _run_in(["git", "rev-parse", "HEAD"], clone, env).stdout.strip()
        (clone / "_enfcov_unrelated.txt").write_text("x\n", encoding="utf-8", newline="\n")
        _run_in(["git", "add", "_enfcov_unrelated.txt"], clone, env)
        c = _run_in(["git", "commit", "-m", "enfcov: trigger freshness gate"], clone, env)
        combined = c.stdout + c.stderr
        if c.returncode == 0:
            return (False, "commit was NOT blocked — the freshness gate did not fire")
        head_after = _run_in(["git", "rev-parse", "HEAD"], clone, env).stdout.strip()
        if head_after != head_before:
            return (False, "a commit LANDED despite the gate (HEAD moved)")
        named = "canonical_freshness" in combined or "last_reviewed" in combined
        return (True, "freshness gate blocked a stale-stamp commit (HEAD unmoved)"
                      + ("; reason names the organ" if named else ""))


# ---------------------------------------------------------------------------
# Organ 3 — reconciled_versions (Group A, edge-gated: coherence spine).
# ---------------------------------------------------------------------------

_RECONCILED_TOKENS = ("reconciled_versions", "validate_reconciliation")
_RECONCILED_FALSE_POSITIVES = ("check-against-spec", "check_against_spec")


def _reconciled_applicability(root: Path) -> tuple[str, str]:
    if _has_reconciled_edge(root):
        return ("applicable", "declares >=1 reconciled_with: frontmatter edge")
    return (NA_NO_EDGES, "no reconciled_with edge declared — the organ is a structural no-op here")


def _reconciled_candidate(root: Path) -> tuple[bool, str]:
    strings = _precommit_hook_strings(root) + _settings_hook_commands(root)
    for s in strings:
        low = s.lower()
        if any(fp in low for fp in _RECONCILED_FALSE_POSITIVES):
            continue  # check-against-spec is the semantic re-stamp flow, deliberately NOT a gate
        if any(tok in low for tok in _RECONCILED_TOKENS):
            return (True, f"candidate: a gate references reconciled_versions/validate_reconciliation ({s!r})")
    return (False, "no reconciled_versions gate wired")


def _reconciled_locate(root: Path) -> tuple[bool, str]:
    return _reconciled_candidate(root)


def _reconciled_fire(consumer: Path) -> tuple[bool, str]:
    """FIRE test: in a clone with a reconciled_with edge, force a version mismatch and require the
    organ to produce a FAIL finding (the coherence-spine gate fires fail-closed on stale edges)."""
    with _cloned_consumer(consumer) as (clone, env, _fc):
        # Break every declared edge's version so the live spec no longer matches.
        broke = _force_reconciled_mismatch(clone)
        if not broke:
            return (False, "no reconciled_with edge found to break in the clone")
        try:
            from scripts import audit as _audit  # noqa: E402
        except ImportError:
            _ensure_scripts_on_path()
            import audit as _audit  # noqa: E402
        findings = _audit.check_reconciled_versions(clone)
        if any(f.status == "fail" for f in findings):
            return (True, "reconciled_versions fires FAIL on a version mismatch (fail-closed)")
        return (False, f"organ did not FAIL on the injected mismatch: "
                       f"{[(f.status, f.evidence[:40]) for f in findings]}")


_RECONCILED_EDGE_RE = re.compile(r"(?m)^(reconciled_with:\s*[A-Za-z0-9_.-]+@)(\d+(?:\.\d+)*)\s*$")
# A numeric-dotted bogus version so split_edge parses it (a non-numeric token would read as
# `malformed` -> WARN, not the `mismatch` -> FAIL this fire_test requires).
_MISMATCH_VERSION = "999.999.999"


def _force_reconciled_mismatch(root: Path) -> bool:
    changed = False
    for md in root.rglob("*.md"):
        if any(part in _SKIP_DIRS or part == "worktrees" for part in md.parts):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        if _RECONCILED_EDGE_RE.search(text):
            new = _RECONCILED_EDGE_RE.sub(rf"\g<1>{_MISMATCH_VERSION}", text)
            if new != text:
                md.write_text(new, encoding="utf-8", newline="\n")
                changed = True
    return changed


# ---------------------------------------------------------------------------
# Organs 4 & 5 — doc_claims / git_backlog_drift (Group B: hub-only-guarded).
# The hub-scoped verdict is DEMONSTRATED, not source-read: invoke the organ off-hub and confirm
# it returns the hub-only PASS. A future refactor that drops the guard flips this and is surfaced.
# ---------------------------------------------------------------------------


def _ensure_scripts_on_path() -> None:
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))


def _demonstrate_hub_scoped(check_name: str, consumer_root: Path) -> tuple[str, str]:
    """Run the Group-B organ against a NON-hub repo_path and observe the guard. This converts
    'I read the `if repo_path != _REPO_ROOT: return pass` guard' into 'I demonstrated the organ
    returns the hub-only PASS off-hub' — the firing-not-presence standard applied at its own seam."""
    try:
        from scripts import audit as _audit  # noqa: E402
    except ImportError:
        _ensure_scripts_on_path()
        import audit as _audit  # noqa: E402
    fn = getattr(_audit, f"check_{check_name}", None)
    if fn is None:
        return (ABSENT, f"UNEXPECTED: audit.check_{check_name} not found")
    findings = fn(Path(consumer_root))
    if findings and all(f.status == "pass" and "hub-only" in f.evidence for f in findings):
        return (HUB_SCOPED,
                f"demonstrated: check_{check_name} returned the hub-only PASS off-hub "
                f"(guard short-circuits despite any local violation)")
    # The guard did NOT short-circuit as classified — surface it, never force green.
    return (ABSENT,
            f"UNEXPECTED off-hub result for check_{check_name} (guard may have changed): "
            + "; ".join(f"{f.status}:{f.evidence[:40]}" for f in findings))


def _group_b_probe(check_name: str):
    def applicability(root: Path) -> tuple[str, str]:
        return _demonstrate_hub_scoped(check_name, root)
    return applicability


# ---------------------------------------------------------------------------
# Organ registry + evaluation.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrganProbe:
    organ_id: str
    group: str  # "A" | "B" | "C"
    applicability: Callable[[Path], tuple[str, str]]
    locate: Callable[[Path], tuple[bool, str]] | None
    fire: Callable[[Path], tuple[bool, str]] | None


TIER1_ORGANS: tuple[OrganProbe, ...] = (
    OrganProbe("session_end_backpressure", "C", _seb_applicability, _seb_locate, _seb_fire),
    OrganProbe("canonical_freshness", "A", _freshness_applicability, _freshness_locate, _freshness_fire),
    OrganProbe("reconciled_versions", "A", _reconciled_applicability, _reconciled_locate, _reconciled_fire),
    OrganProbe("doc_claims", "B", _group_b_probe("doc_claims"), None, None),
    OrganProbe("git_backlog_drift", "B", _group_b_probe("git_backlog_drift"), None, None),
)


def evaluate_organ(probe: OrganProbe, consumer_root: Path, *, allow_fire: bool) -> Cell:
    """Applicability -> locate (candidate pre-filter) -> fire_test (sole enforcing-local truth-maker)."""
    app_verdict, app_ev = probe.applicability(consumer_root)
    if app_verdict != "applicable":
        return Cell(probe.organ_id, app_verdict, app_ev, fired=None)
    if probe.locate is None:  # applicable but no locate defined -> treat as absent (no wiring path)
        return Cell(probe.organ_id, ABSENT, app_ev + " | no locate signature", fired=None)
    candidate, loc_ev = probe.locate(consumer_root)
    if not candidate:
        return Cell(probe.organ_id, ABSENT, loc_ev, fired=None)
    if not allow_fire or probe.fire is None:
        return Cell(probe.organ_id, PRESENT_UNVERIFIED,
                    loc_ev + " | fire_test not run (static path — enforcing-local unproven)", fired=None)
    fired, fire_ev = probe.fire(consumer_root)
    return Cell(probe.organ_id, ENFORCING_LOCAL if fired else ABSENT,
                loc_ev + " | " + fire_ev, fired=fired)


def evaluate_static(consumer_root: Path) -> list[Cell]:
    """Cheap applicability + locate ONLY (never clones). Feeds the audit.py read-only leg."""
    consumer_root = Path(consumer_root)
    return [evaluate_organ(p, consumer_root, allow_fire=False) for p in TIER1_ORGANS]


def evaluate_full(consumer_root: Path) -> list[Cell]:
    """Full evaluation: runs fire_test for any organ whose locate returns candidate (CLI/tests)."""
    consumer_root = Path(consumer_root)
    return [evaluate_organ(p, consumer_root, allow_fire=True) for p in TIER1_ORGANS]


# ---------------------------------------------------------------------------
# Tier-2 — bounded PRESENCE surface (the 4 deploy manifest carriers). CLI-only; the carriers'
# detect() (esp. the plugin carrier's `claude plugin list` shell-out) is not run in the leg/CI.
# ---------------------------------------------------------------------------


def _carrier_state_label(state) -> str:
    _ensure_deploy_on_path()
    from contract import CarrierState  # noqa: E402
    if state == CarrierState.PRESENT_CORRECT:
        return T2_PRESENT_WIRED
    if state in (CarrierState.PRESENT_DRIFTED, CarrierState.PRESENT_WRONG_VERSION):
        return T2_PRESENT_NOT_WIRED
    return T2_ABSENT


def evaluate_tier2(consumer_root: Path, *, manifest_version: str = "1.0.0") -> list[Tier2Cell]:
    """Report each manifest carrier's detect() state per consumer (PRESENCE, not firing)."""
    _ensure_deploy_on_path()
    import tool as deploy_tool  # noqa: E402

    manifest_path = _DEPLOY_DIR / f"manifest-v{manifest_version}.yaml"
    manifest = _read_yaml(manifest_path)
    carriers = deploy_tool.make_carriers(Path(consumer_root))
    cells: list[Tier2Cell] = []
    for entry in sorted(manifest.get("carriers") or [], key=lambda c: c.get("order", 0)):
        cid = str(entry.get("id", ""))
        carrier = carriers.get(cid)
        if carrier is None or not entry.get("implemented"):
            cells.append(Tier2Cell(cid, T2_ABSENT, "carrier not implemented/bound"))
            continue
        try:
            state = carrier.detect(entry.get("target"))
            cells.append(Tier2Cell(cid, _carrier_state_label(state),
                                   f"carrier detect(): {getattr(state, 'value', state)} (presence, not firing)"))
        except Exception as exc:  # noqa: BLE001 — read-only: surface as error, never crash
            cells.append(Tier2Cell(cid, T2_ERROR, f"detect() raised: {exc!r}"))
    return cells


# ---------------------------------------------------------------------------
# Fleet enumeration + report assembly.
# ---------------------------------------------------------------------------


def consumer_paths() -> list[tuple[str, Path]]:
    """(name, path) for every registered consumer (registry keys minus the hub). Reuses the
    committed deployed-versions registry + the deploy tool's sibling resolver."""
    _ensure_deploy_on_path()
    import tool as deploy_tool  # noqa: E402
    repos = deploy_tool.load_registry(deploy_tool.DEFAULT_REGISTRY)
    hub = deploy_tool.HUB_DIR_NAME
    out: list[tuple[str, Path]] = []
    for name in sorted(repos):
        if name == hub:
            continue
        out.append((name, deploy_tool.resolve_repo_root(name)))
    return out


def build_report(name: str, root: Path, *, fire: bool, tier2: bool) -> ConsumerReport:
    tier1 = evaluate_full(root) if fire else evaluate_static(root)
    t2 = tuple(evaluate_tier2(root)) if tier2 else ()
    return ConsumerReport(name=name, root=str(root), tier1=tuple(tier1), tier2=t2)


# ---------------------------------------------------------------------------
# Digest + surfacing.
# ---------------------------------------------------------------------------


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".enfcov-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def render_digest(reports: list[ConsumerReport], *, run_date: str) -> str:
    lines = [
        "# Enforcement Coverage — Informant Organ",
        "",
        f"run_date: {run_date}",
        "",
        "Read-only reporter (ADR-28/36). Measures whether each hub enforcement organ FIRES",
        "locally, not whether files are present. Tier-1 = firing; Tier-2 = presence (separate).",
        "",
        "## Tier-1 — enforcement firing "
        "{enforcing-local | absent | hub-scoped | n/a-no-edges | present-unverified}",
        "",
    ]
    organs = [p.organ_id for p in TIER1_ORGANS]
    for rep in reports:
        lines.append(f"### {rep.name}")
        for cell in rep.tier1:
            lines.append(f"- {cell.organ_id}: **{cell.verdict}** — {cell.evidence}")
        lines.append("")
    if any(rep.tier2 for rep in reports):
        lines.append("## Tier-2 — deploy-carrier PRESENCE "
                     "{present-and-wired | present-not-wired | absent} (NOT firing)")
        lines.append("")
        for rep in reports:
            if not rep.tier2:
                continue
            lines.append(f"### {rep.name}")
            for t2 in rep.tier2:
                lines.append(f"- {t2.carrier_id}: **{t2.state}** — {t2.evidence}")
            lines.append("")
    lines.append("<!-- organs: " + ", ".join(organs) + " -->")
    lines.append("")
    return "\n".join(lines)


def surface_line(reports: list[ConsumerReport]) -> str:
    """A one-line SessionStart-style summary (propose-only; no hook wired this stage)."""
    enforcing = absent = hubscoped = 0
    for rep in reports:
        for cell in rep.tier1:
            if cell.verdict == ENFORCING_LOCAL:
                enforcing += 1
            elif cell.verdict == ABSENT:
                absent += 1
            elif cell.verdict == HUB_SCOPED:
                hubscoped += 1
    return (f"[enforcement-coverage] {len(reports)} consumer(s): "
            f"{enforcing} enforcing-local, {absent} absent, {hubscoped} hub-scoped "
            f"-- see logs/ENFORCEMENT-COVERAGE.md")


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


@click.command()
@click.option("--consumer", "consumer", default=None,
              help="Report a single registered consumer (by registry name) instead of the fleet.")
@click.option("--fire/--no-fire", "fire", default=True,
              help="Run fire_test (clone+inject) for candidate organs. --no-fire = static only.")
@click.option("--tier2/--no-tier2", "tier2", default=True,
              help="Include the Tier-2 deploy-carrier PRESENCE surface (runs carrier detect()).")
@click.option("--run-date", "run_date", required=True,
              help="Run date stamp for the digest (YYYY-MM-DD) — passed in (no wall-clock read).")
@click.option("--write/--no-write", "write", default=True,
              help="Write the gitignored digest logs/ENFORCEMENT-COVERAGE.md.")
def main(consumer: str | None, fire: bool, tier2: bool, run_date: str, write: bool) -> None:
    """Measure per-consumer x per-organ enforcement coverage across the fleet (read-only)."""
    if consumer:
        _ensure_deploy_on_path()
        import tool as deploy_tool  # noqa: E402
        targets = [(consumer, deploy_tool.resolve_repo_root(consumer))]
    else:
        targets = consumer_paths()

    reports: list[ConsumerReport] = []
    for name, root in targets:
        if not Path(root).is_dir():
            reports.append(ConsumerReport(name, str(root),
                           (Cell("*", "unavailable", "consumer tree not found on disk"),), ()))
            continue
        reports.append(build_report(name, root, fire=fire, tier2=tier2))

    digest = render_digest(reports, run_date=run_date)
    if write:
        _atomic_write(_DIGEST_PATH, digest)
        click.echo(f"wrote {_DIGEST_PATH.relative_to(_REPO_ROOT)}")
    click.echo(surface_line(reports))
    for rep in reports:
        click.echo(f"\n{rep.name} ({rep.root}):")
        for cell in rep.tier1:
            click.echo(f"  T1 {cell.organ_id:28} {cell.verdict}")
        for t2 in rep.tier2:
            click.echo(f"  T2 {t2.carrier_id:28} {t2.state}")


if __name__ == "__main__":
    main()
