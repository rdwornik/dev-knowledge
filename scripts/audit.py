"""
audit.py — Ecosystem audit tool per ADR-36.

Reads child repos under Dev/ and writes only to .dev-knowledge paths.
Read-only contract: never touches child repo files (hard constraint, ADR-36).

This module is self-documenting: `python scripts/audit.py --help` and
`python scripts/audit.py <cmd> --help` are the authoritative CLI reference, and
`python scripts/audit.py checks` lists the registered checks straight from the
ALL_CHECKS registry (so the list cannot drift from what actually runs). The
conceptual / authority model — what this tool is, why the cross-repo `run` is
advisory while the self-audit `health` gates commits, and the self-only
enforcement model — lives in ARCHITECTURE.md (§"Validators and enforcement",
§"Authority and governance") and ADR-36. Do not re-narrate that here.

Commands:
    audit run                          # full ecosystem; writes report
    audit repo <name>                  # single repo
    audit registry update              # regenerate ecosystem/index.yaml
    audit health                       # quick TTY status, no file writes
    audit checks                       # list registered checks (from ALL_CHECKS)

Usage:
    python scripts/audit.py run
    python scripts/audit.py run --repo-path ../ai-council
    python scripts/audit.py repo ai-council
    python scripts/audit.py health
"""

from __future__ import annotations

import inspect
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import click
import yaml

# Resolve repo root (scripts/ sibling) — after imports
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)

# Floor policy is single-sourced in generate_floor.py (the generator owns it; audit enforces).
# Dual import: `scripts.generate_floor` for `python -m scripts.audit`; `generate_floor` for
# `python scripts/audit.py` and the test path (scripts/ on sys.path).
try:
    from scripts.generate_floor import F5_BLACKLIST as _FLOOR_F5
    from scripts.generate_floor import floor_sha256 as _floor_sha256
except ImportError:
    from generate_floor import F5_BLACKLIST as _FLOOR_F5
    from generate_floor import floor_sha256 as _floor_sha256

# #90 git↔backlog drift verifier — imported as a module so the check stays a thin
# adapter and tests can monkeypatch `_vgb.reconcile`. Same dual-import shape.
try:
    from scripts import validate_git_backlog as _vgb
except ImportError:
    import validate_git_backlog as _vgb

# #89 prose-vs-state checker — same module-import + thin-adapter shape as _vgb.
try:
    from scripts import validate_doc_claims as _vdc
except ImportError:
    import validate_doc_claims as _vdc

# #153 --no-ff merge guard — same module-import + thin-adapter shape as _vgb/_vdc.
try:
    from scripts import validate_no_ff as _vnf
except ImportError:
    import validate_no_ff as _vnf

# #163 handoff-probe teeth validator — same module-import + thin-adapter shape.
try:
    from scripts import verify_handoff_probes as _vhp
except ImportError:
    import verify_handoff_probes as _vhp

# Coherence-spine reconciliation checker — same module-import + thin-adapter shape.
try:
    from scripts import validate_reconciliation as _vr
except ImportError:
    import validate_reconciliation as _vr

# #140 doc-rot / grooming checker — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_rot as _vdr
except ImportError:
    import validate_doc_rot as _vdr

# #194 doc→code declared-edge resolver — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_code_edge as _vdce
except ImportError:
    import validate_doc_code_edge as _vdce

# Prose structural linter (supplement organ #2) — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_structure as _vds
except ImportError:
    import validate_doc_structure as _vds

# #195 code→code safe-removal gate (consumes the #193 reverse-dep oracle) — same module-import
# + thin-adapter shape as the validators above; tests monkeypatch `_sr.check_removal`.
try:
    from scripts import safe_remove as _sr
except ImportError:
    import safe_remove as _sr

# #179 undeclared-edge scan (Fable consult #1 ruling #2, 2026-07-03) — ship-gate WARN leg; same
# module-import + thin-adapter shape; tests monkeypatch `_sue.scan`.
try:
    from scripts import scan_undeclared_edges as _sue
except ImportError:
    import scan_undeclared_edges as _sue

# Canonical-freshness gate (enforcement-mesh, #236) — single-sourced so the SAME logic serves
# this audit leg AND the consumer-local pre-commit gate the mesh carrier deploys. audit-level
# aliases below keep the existing monkeypatch seam (tests set `_git_last_commit_date`).
try:
    from scripts import canonical_freshness_gate as _cfg
except ImportError:
    import canonical_freshness_gate as _cfg

# Gate-mode flag (#89): cmd_health sets this True around its self-audit loop so the
# expensive claim-3 (pytest --collect-only) is SKIPPED on the per-commit gate and
# evaluated only on the full-audit path (run/repo/CLI/SessionStart). Operator ruling.
_GATE_MODE = False

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("audit")

ECOSYSTEM_DIR = Path(_REPO_ROOT) / "ecosystem"
AUDITS_DIR = Path(_REPO_ROOT) / "docs" / "audits"
ECOSYSTEM_INDEX = Path(_REPO_ROOT) / "ecosystem" / "index.yaml"
# #147 ship-gate: the known-WARN disposition register (read-only). Missing/malformed
# -> [] (every WARN then counts undispositioned — stricter, never wedged).
DISPOSITION_REGISTER = Path(_REPO_ROOT) / "ecosystem" / "disposition-register.yaml"
# ADR-91: the durable per-repo deployed-methodology-version registry (COMMITTED, hand/
# deploy-runbook-written; read-only here). Hub-resolved (a module constant, NOT repo_path) --
# it is ONE hub file read for whichever repo is being audited; check_deployed_methodology_version
# looks up the audited repo by its directory name. Missing/malformed -> WARN (never wedges).
DEPLOYED_VERSIONS_REGISTRY = Path(_REPO_ROOT) / "ecosystem" / "deployed-versions.yaml"

# ---------------------------------------------------------------------------
# Universal visual pattern (ADR-59) — constants
# ---------------------------------------------------------------------------

# Config-file suffixes subject to dot-prefix discipline (root-level only).
_CONFIG_SUFFIXES = {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg", ".conf"}

# Industry-standard names that MUST NOT be dot-prefixed (ADR-59 exception list).
# This is a mirror of the ADR-59 exception list — update BOTH together when a
# new tool is adopted (see PLAYBOOK "Universal visual pattern" maintenance rule).
_DOT_PREFIX_EXCEPTIONS = {
    "pyproject.toml",       # Python PEP 518
    "package.json",         # npm
    "package-lock.json",    # npm lockfile
    "Cargo.toml",           # Rust
    "setup.py",             # Python legacy
    "setup.cfg",            # Python legacy
    "pytest.ini",           # pytest will not read .pytest.ini (ADR-59 amend 2026-06-02)
    "requirements.txt",     # pip convention
    "requirements-dev.txt",
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "tach.toml",            # verified 2026-05-27: tach 0.34.0 does not read .tach.toml
    "README.md",            # deprecated from baseline; if present, no dot
}

# Canonical files universally mandatory at repo root (ADR-38 A5 / ADR-51).
# ADR-38 A6 (2026-06-02): the seven-file canonical set is mandatory for every repo.
# CONTRIBUTING/JOURNAL/LESSONS were promoted from optional (A5) to mandatory here so
# cross-repo navigation is identical (the same seven anchors in every repo).
_CANONICAL_MANDATORY = [
    "VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "BACKLOG.md",
    "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md",
]

# All canonical names whose casing is checked when present (mandatory + optional
# + .dev-knowledge-only). Presence is required only for _CANONICAL_MANDATORY.
_CANONICAL_ALL = _CANONICAL_MANDATORY + [
    "ENVIRONMENT.md", "ESSENTIALS.md", "PLAYBOOK.md", "TOKEN-LOG.md", "README.md",
]

# Canonical living docs subject to the freshness cadence (check #10; operationalizes
# the ADR-39 "grooming" lifecycle element). PORTABLE: a child repo inherits this list
# unchanged — "CLAUDE.md" resolves to that repo's own project CLAUDE.md. Append-only
# files (JOURNAL/LESSONS) and the per-session BACKLOG are deliberately EXCLUDED: their
# freshness is intrinsic to how they are written, so an edit-since-review signal would
# fire every session by design.
# Single-sourced in scripts/canonical_freshness_gate.py (deployed consumer-local by the mesh
# carrier). Aliased here so audit.py + its importers (enforcement_coverage, tests) keep the name.
# The PORTABLE base (DEFAULT_FRESHNESS_FILES) is what a consumer inherits verbatim via the deployed
# canonical_freshness gate; the HUB-ONLY extras are hub governance docs under protocols/ that do NOT
# exist in a consumer (so they'd be skipped there anyway) and are gated only here, where audit.py
# runs (audit.py is hub-only). Added per the 2026-07-08 fleet-census A-2 ruling — PLAYBOOK is the
# largest ungated canonical doc but is DEFERRED (no last_reviewed frontmatter yet + a genuine
# end-to-end re-read is its own arc; see BACKLOG). SESSION_SETUP + AI_COUNCIL_PROCESS were genuinely
# re-read and stamped in that arc, so they join now.
_HUB_ONLY_FRESHNESS_FILES = ["protocols/SESSION_SETUP.md", "protocols/AI_COUNCIL_PROCESS.md"]
_FRESHNESS_FILES = _cfg.DEFAULT_FRESHNESS_FILES + _HUB_ONLY_FRESHNESS_FILES
_FRESHNESS_CADENCE_DAYS = _cfg.FRESHNESS_CADENCE_DAYS

# Required VS Code workspace settings (ADR-59 Decision 3). "upper" (not "default")
# is what clusters ALL-CAPS canonical .md files ahead of lowercase configs.
_WORKSPACE_REQUIRED_SETTINGS = {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper",
}


def _strip_jsonc(text: str) -> str:
    """Strip // and /* */ comments and trailing commas from JSON-with-comments.

    VS Code .code-workspace files are JSONC; json.loads cannot parse them. Comment
    stripping respects string literals so a `//` inside a string value survives.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))

# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    """One audit/check result — the LOCKED coherence-spine output contract.

    Stable shape: exactly three string fields — `check_name`, `status`, `evidence`.
    `status` is one of the five-value enum: "pass" | "fail" | "warn" | "unavailable" | "n/a".
    `evidence` is markdown-table-safe (no literal `|` — emitters replace it with `/`).

    This is the surface the #171 conformance dashboard consumes (ADR-86): the coherence
    checker emits `check_name == "reconciled_versions"` here (check_reconciled_versions),
    a `fail` per drifting edge. The shape is LOCKED — do not add/rename fields without
    updating that consumer. Pinned by tests/test_coherence_integration.py
    (test_finding_format_is_locked). No dashboard is built yet (#171, v2); this only
    fixes the format it will read.
    """
    check_name: str
    status: str          # "pass" | "fail" | "warn" | "unavailable" | "n/a"
    evidence: str

@dataclass
class RepoState:
    """A repo's last audit result — the schema of ecosystem/<name>/state.yaml.

    Fields (round-tripped by to_dict/from_dict): `name` (matches the
    ecosystem/<name>/ folder), `path` (absolute path stored at registration),
    `last_audit` (ISO date of the last run, or None if never audited), and
    `findings` — a list of Finding(check_name, status, evidence) where status is
    one of pass | fail | warn | unavailable | n/a. state.yaml is the per-repo source of
    truth; ecosystem/index.yaml is a derived rollup of these (see regenerate_index).
    """
    name: str
    path: str
    last_audit: Optional[str]
    findings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "last_audit": self.last_audit,
            "findings": [
                {"check_name": f.check_name, "status": f.status, "evidence": f.evidence}
                for f in self.findings
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepoState":
        findings = [
            Finding(f["check_name"], f["status"], f["evidence"])
            for f in d.get("findings", [])
        ]
        return cls(
            name=d["name"],
            path=d["path"],
            last_audit=d.get("last_audit"),
            findings=findings,
        )


def _state_path(repo_name: str) -> Path:
    return ECOSYSTEM_DIR / repo_name / "state.yaml"


def _history_path(repo_name: str, run_date: date) -> Path:
    return ECOSYSTEM_DIR / repo_name / "history" / f"{run_date.isoformat()}.md"


def load_state(repo_name: str) -> Optional[RepoState]:
    p = _state_path(repo_name)
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    return RepoState.from_dict(d)


def save_state(state: RepoState) -> None:
    p = _state_path(state.name)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        yaml.dump(state.to_dict(), fh, default_flow_style=False, allow_unicode=True)


def append_history(state: RepoState, run_date: date) -> None:
    p = _history_path(state.name, run_date)
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    lines = [f"## {run_date.isoformat()} — {ts}\n\n"]
    lines.append("| Check | Status | Evidence |\n|---|---|---|\n")
    for f in state.findings:
        lines.append(f"| {f.check_name} | {f.status} | {f.evidence} |\n")
    lines.append("\n")
    with open(p, "a", encoding="utf-8") as fh:
        fh.writelines(lines)


def discover_repos() -> list[str]:
    """Return repo names registered in ecosystem/ (by state.yaml presence)."""
    if not ECOSYSTEM_DIR.exists():
        return []
    return [
        d.name
        for d in sorted(ECOSYSTEM_DIR.iterdir())
        if d.is_dir() and (d / "state.yaml").exists()
    ]

# ---------------------------------------------------------------------------
# Audit checks
# ---------------------------------------------------------------------------

def check_vision_md(repo_path: Path) -> list[Finding]:
    """VISION.md presence + parseable YAML frontmatter per ADR-33."""
    vision = repo_path / "VISION.md"
    if not vision.exists():
        return [Finding("vision_md", "fail", "VISION.md absent at repo root")]
    text = vision.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [Finding("vision_md", "fail", "VISION.md has no YAML frontmatter (must start with '---')")]
    # Extract frontmatter between first two ---
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [Finding("vision_md", "fail", "VISION.md frontmatter not closed (missing closing '---')")]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [Finding("vision_md", "fail", f"VISION.md frontmatter YAML parse error: {e}")]
    if not isinstance(fm, dict):
        return [Finding("vision_md", "fail", "VISION.md frontmatter is not a YAML mapping")]
    required_keys = {"version", "last_reviewed", "owner", "status"}
    missing = required_keys - fm.keys()
    if missing:
        return [Finding("vision_md", "warn", f"VISION.md frontmatter missing keys: {sorted(missing)}")]
    return [Finding("vision_md", "pass", f"VISION.md present; frontmatter keys: {sorted(fm.keys())}")]


def check_adr38_baseline(repo_path: Path) -> list[Finding]:
    """ADR-38 (amendments A5 2026-05-23, A6 2026-06-02) universal governance baseline.

    Checks the governance documents every repo must carry — not code structure.
    The repo-tier system is deprecated, so there is no per-tier branching. Code
    layout (src/, tests/, pyproject.toml) is scoped to code projects per the
    amendment and is NOT part of this universal governance check (governance-only
    repos such as .dev-knowledge have no src/ or pyproject.toml). README.md is
    optional (deprecated from the baseline); CHANGELOG.md was removed by ADR-49.
    CLAUDE.md is covered by check_claude_md, so it is not duplicated here.

    A6 (2026-06-02) promoted CONTRIBUTING.md, JOURNAL.md and LESSONS.md from optional
    to the mandatory seven-file canonical set — superseding the A5 "JOURNAL/LESSONS
    remain repo-specific" line.
    """
    required_files = ["VISION.md", "ARCHITECTURE.md", "BACKLOG.md",
                      "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md"]

    missing_files = [f for f in required_files if not (repo_path / f).exists()]

    if missing_files:
        status = "fail"
        evidence = f"Missing required: {missing_files}"
    else:
        status = "pass"
        evidence = "All ADR-38 universal governance baseline files present"
    return [Finding("adr38_baseline", status, evidence)]


def check_claude_md(repo_path: Path) -> list[Finding]:
    """ADR-31 CLAUDE.md presence and non-empty per authority model baseline."""
    claude = repo_path / "CLAUDE.md"
    if not claude.exists():
        return [Finding("claude_md", "fail", "CLAUDE.md absent at repo root")]
    content = claude.read_text(encoding="utf-8").strip()
    if not content:
        return [Finding("claude_md", "fail", "CLAUDE.md exists but is empty")]
    return [Finding("claude_md", "pass", f"CLAUDE.md present ({len(content)} chars)")]


def check_dot_prefix_discipline(repo_path: Path) -> list[Finding]:
    """Root config files dot-prefixed unless on exception list (ADR-59 D1).

    Root-level only — subfolder configs are ignored. A config-suffix file that is
    neither dot-prefixed nor on the ADR-59 exception list is a violation.
    """
    violations = []
    for p in sorted(repo_path.iterdir()):
        if not p.is_file():
            continue
        if p.suffix not in _CONFIG_SUFFIXES:
            continue
        if p.name.startswith("."):
            continue
        if p.name in _DOT_PREFIX_EXCEPTIONS:
            continue
        violations.append(p.name)
    if violations:
        return [Finding("dot_prefix_discipline", "fail",
                        f"Root config files not dot-prefixed (not on ADR-59 exception list): {violations}")]
    return [Finding("dot_prefix_discipline", "pass",
                    "All root config files dot-prefixed or on ADR-59 exception list")]


def check_canonical_md_visibility(repo_path: Path) -> list[Finding]:
    """Mandatory canonical files present + correct ALL-CAPS casing (ADR-59 D2).

    Requires the seven universal files (ADR-38 A6 / A5 / ADR-51). Optional and
    .dev-knowledge-only canonical files are NOT required, but if present (under any
    casing) they must use the canonical ALL-CAPS spelling — a mis-cased canonical
    file breaks the visual clustering the pattern exists to produce.
    """
    missing = [f for f in _CANONICAL_MANDATORY if not (repo_path / f).exists()]

    canonical_lower = {name.lower(): name for name in _CANONICAL_ALL}
    miscased = []
    for p in repo_path.iterdir():
        if not p.is_file():
            continue
        canonical = canonical_lower.get(p.name.lower())
        if canonical and p.name != canonical:
            miscased.append(f"{p.name} (expected {canonical})")

    if missing:
        return [Finding("canonical_md_visibility", "fail",
                        f"Missing mandatory canonical files: {missing}")]
    if miscased:
        return [Finding("canonical_md_visibility", "fail",
                        f"Mis-cased canonical files: {sorted(miscased)}")]
    return [Finding("canonical_md_visibility", "pass",
                    f"Mandatory canonical files present + correctly cased: {_CANONICAL_MANDATORY}")]


def check_workspace_settings(repo_path: Path) -> list[Finding]:
    """Dot-prefixed .code-workspace carrying required sort settings (ADR-59 D3).

    FAIL if absent or unparseable; WARN if present but not dot-prefixed or a
    required setting is missing/wrong; PASS if dot-prefixed with correct settings.
    """
    workspaces = sorted(p for p in repo_path.iterdir()
                        if p.is_file() and p.name.endswith(".code-workspace"))
    if not workspaces:
        return [Finding("workspace_settings", "fail",
                        "No .code-workspace file at repo root")]

    ws = workspaces[0]
    try:
        data = json.loads(_strip_jsonc(ws.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValueError) as e:
        return [Finding("workspace_settings", "fail",
                        f"{ws.name} is not parseable JSON(C): {e}")]

    issues = []
    if not ws.name.startswith("."):
        issues.append(f"workspace file '{ws.name}' is not dot-prefixed")

    settings = data.get("settings", {})
    if not isinstance(settings, dict):
        settings = {}
    for key, expected in _WORKSPACE_REQUIRED_SETTINGS.items():
        actual = settings.get(key, "<absent>")
        if actual != expected:
            issues.append(f"{key}={actual!r} (expected {expected!r})")

    if issues:
        return [Finding("workspace_settings", "warn", f"{ws.name}: " + "; ".join(issues))]
    return [Finding("workspace_settings", "pass",
                    f"{ws.name} present, dot-prefixed, required sort settings correct")]


# check_mermaid_theme_directive (check #7, ADR-51 v2) RETIRED by ADR-51 amendment
# 2026-07-05: canonical docs are LLM-first — Mermaid left them, so the theme standard
# is re-scoped to the visualization surface, unenforced by audit. No replacement
# check asserts Mermaid ABSENCE: child repos carry legacy-form codemaps until their
# per-repo migration (root-scheduled), and a presence-ban would red every child.


# ---------------------------------------------------------------------------
# Handoff-bundle enforcement (HANDOFF_PROCESS v4.3 item F) — constants
# ---------------------------------------------------------------------------

# Per-file line budgets for a v4 handoff bundle (HANDOFF_PROCESS §4).
_BUNDLE_BUDGETS = {
    "01_ROLE.md": 100,
    "02_METHODOLOGY.md": 200,
    "03_PROJECT.md": 150,
    "04_RECENT.md": 250,
    "05_NOW.md": 100,
    "06_QUESTIONS.md": 80,
    "07_ASK_BACK.md": 50,
}
# The 8 required files: README + 01–07.
_BUNDLE_REQUIRED_FILES = ["README.md", *_BUNDLE_BUDGETS.keys()]

# A v4 bundle declares its contract via this README stamp (added v4.2 item D).
# The optional `(?:\.\d+)?` matches a patch segment (v4.3.1) without capturing it —
# major.minor still drive the v4.3+ gate. Without it, three-segment stamps (v4.3.1,
# first used 2026-05-31) silently fail to match and the bundle is skipped, not validated.
_BUNDLE_STAMP_RE = re.compile(
    r"Generated by HANDOFF_PROCESS v(\d+)\.(\d+)(?:\.\d+)? \(status: (?:beta|stable)\)"
)

# Sibling dirs under docs/handoffs/ that are not bundles to validate.
_BUNDLE_EXCLUDE_DIRS = {"aborted", "in-progress", "archive"}


def check_handoff_bundle_structure(repo_path: Path) -> list[Finding]:
    """Historical v4 handoff-bundle structure validator (HANDOFF_PROCESS v4.3 item F).

    Post-#149 flip, v5 is canonical and emits a different artifact (lean residual +
    probe manifest + thin boot — no 8-file bundle), so this check now governs only the
    HISTORICAL v4 bundles. v5-bundle validation is owned by the read-only teeth validator
    (`scripts/verify_handoff_probes.py`, #163 — now live and gating via `check_handoff_probes`
    in ALL_CHECKS); the manual probe-gate (HANDOFF_PROCESS.md §5) remains the rationale-quality
    backstop.

    Scans docs/handoffs/<slug>/ and validates only STAMPED v4 bundles — those whose
    README.md carries the `Generated by HANDOFF_PROCESS v4.x (status: beta|stable)`
    stamp. v5 bundles carry no v4 stamp, so they are skipped here by design. Pre-stamp
    bundles (the v4.1 first-run) and v3.x sync bundles predate the contract and are out
    of scope (preserved historical evidence). The four-tag section is required only for
    v4.3+ bundles.

    Per stamped bundle: 8 files present (README + 01–07); README carries a
    `## Drift cross-check` section; 04_RECENT carries `## Load-bearing facts` (and,
    for v4.3+, `## Four-tag discipline (canonical)`); per-file line budgets respected.
    Excludes aborted/, in-progress/, archive/. Read-only (ADR-28/36).
    """
    handoffs = repo_path / "docs" / "handoffs"
    if not handoffs.exists():
        return [Finding("handoff_bundle_structure", "n/a",
                        "no docs/handoffs/ — nothing to validate")]

    violations: list[str] = []
    validated = 0
    for d in sorted(handoffs.iterdir()):
        if not d.is_dir() or d.name in _BUNDLE_EXCLUDE_DIRS:
            continue
        readme = d / "README.md"
        if not readme.exists():
            continue  # v3.x sync bundles use 00_README.md — not a v4 bundle
        readme_text = readme.read_text(encoding="utf-8")
        stamp = _BUNDLE_STAMP_RE.search(readme_text)
        if not stamp:
            continue  # pre-stamp / non-v4 bundle — out of scope
        validated += 1
        is_v43_plus = (int(stamp.group(1)), int(stamp.group(2))) >= (4, 3)

        for fname in _BUNDLE_REQUIRED_FILES:
            if not (d / fname).exists():
                violations.append(f"{d.name}: missing {fname}")

        if "## Drift cross-check" not in readme_text:
            violations.append(f"{d.name}/README.md: missing '## Drift cross-check' section")

        recent = d / "04_RECENT.md"
        if recent.exists():
            recent_text = recent.read_text(encoding="utf-8")
            if "## Load-bearing facts" not in recent_text:
                violations.append(f"{d.name}/04_RECENT.md: missing '## Load-bearing facts' section")
            if is_v43_plus and "## Four-tag discipline (canonical)" not in recent_text:
                violations.append(
                    f"{d.name}/04_RECENT.md: missing '## Four-tag discipline (canonical)' "
                    "section (v4.3+ requirement)")

        for fname, budget in _BUNDLE_BUDGETS.items():
            fpath = d / fname
            if not fpath.exists():
                continue
            nlines = len(fpath.read_text(encoding="utf-8").splitlines())
            if nlines > budget:
                violations.append(f"{d.name}/{fname}: {nlines} lines > budget {budget}")

    if violations:
        evidence = (f"{len(violations)} violation(s) across {validated} stamped bundle(s): "
                    + "; ".join(violations[:5]))
        if len(violations) > 5:
            evidence += f" … (+{len(violations) - 5} more)"
        return [Finding("handoff_bundle_structure", "fail", evidence)]
    return [Finding("handoff_bundle_structure", "pass",
                    f"{validated} stamped v4 bundle(s) valid (structure + sections + budgets)")]


def check_handoff_tag_canonicity(repo_path: Path) -> list[Finding]:
    """§3.1 tag-canonicity lint (HANDOFF_PROCESS v4.3 item F) — historical v4 surface.

    Post-#149 flip the canonical file is v5, which carries no §3.1 four-tag section, so
    this check degrades to a clean pass ("§3.1 not found — nothing to lint"). It remains
    only to guard the historical v4 tag-canonicity invariant if a §3.1 ever reappears.

    Scans protocols/HANDOFF_PROCESS.md §3.1 ONLY (not the end-of-file amendments).
    §3.1 must EITHER enumerate all four canonical tags (witnessed/recall/inferred/
    unknown — the post-v5 consolidated state) OR carry a cross-reference to
    Amendment A (the four-tag canonical). A three-tag §3.1 with no cross-reference is
    the drift this check exists to catch (closes C3 durably). Read-only.
    """
    spec = repo_path / "protocols" / "HANDOFF_PROCESS.md"
    if not spec.exists():
        return [Finding("handoff_tag_canonicity", "n/a",
                        "no protocols/HANDOFF_PROCESS.md — nothing to validate")]

    lines = spec.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines) if re.match(r"^###\s+3\.1\b", ln)), None)
    if start is None:
        return [Finding("handoff_tag_canonicity", "n/a",
                        "§3.1 section not found (consolidated?) — nothing to lint")]
    # §3.1 body runs to the next standalone '---' rule (section terminator).
    end = next((j for j in range(start + 1, len(lines)) if re.match(r"^---\s*$", lines[j])),
               len(lines))
    section = "\n".join(lines[start:end])

    four_tags = all(re.search(rf"\b{tag}\b", section, re.IGNORECASE)
                    for tag in ("witnessed", "recall", "inferred", "unknown"))
    crossref = re.search(r"(superseded by Amendment|see Amendment A|Amendment A)",
                         section, re.IGNORECASE) is not None

    if four_tags or crossref:
        how = "four canonical tags enumerated" if four_tags else "cross-reference to Amendment A present"
        return [Finding("handoff_tag_canonicity", "pass", f"§3.1 canonical: {how}")]
    return [Finding("handoff_tag_canonicity", "fail",
                    "§3.1 has three-tag content without a cross-reference to Amendment A "
                    "(four-tag canonical) — add a supersession pointer")]


# Single-sourced in canonical_freshness_gate.py; audit-level aliases keep the monkeypatch seam
# (tests set `aud._git_last_commit_date` / `aud._parse_last_reviewed`; check_canonical_freshness
# passes these names into `_cfg.evaluate`, so a monkeypatch at the audit level still applies).
_parse_last_reviewed = _cfg.parse_last_reviewed
_git_last_commit_date = _cfg.git_last_commit_date


# rule: canonical-freshness
def check_canonical_freshness(repo_path: Path) -> list[Finding]:
    """Canonical living-file freshness cadence (operationalizes ADR-39 grooming).

    For each canonical living doc (_FRESHNESS_FILES) that carries `last_reviewed`:
      - A2 (primary, FAIL): `last_reviewed` predates the file's last git-commit date — the
        file was edited but never re-reviewed, so its review stamp is stale.
      - A1 (backstop, WARN): `last_reviewed` is older than _FRESHNESS_CADENCE_DAYS — a
        loose calendar nudge even when nothing changed.
    Missing `last_reviewed` → WARN (child-repo-safe: lets a repo adopt the convention
    without a hard failure). An absent file is skipped (presence is enforced by #1/#3/#5).

    `last_reviewed` means "re-read end-to-end and confirmed accurate (or the drift filed)"
    on that date — NOT merely "touched". This check enforces edit-hygiene + a calendar
    backstop; it does NOT verify content against external decisions (e.g. a doc whose
    prose has drifted from a new ADR while its file was never edited trips neither signal).

    A2 is deliberately COMMIT-based, not working-tree-based: an uncommitted edit that has
    not yet bumped `last_reviewed` is not flagged until it lands in a commit (working-tree
    state would FAIL during normal mid-edit work, before the reviewer has bumped the stamp).
    So the signal is post-commit / eventually-consistent — it catches the stale stamp at the
    next audit after the edit is committed, which is the intended enforcement point.

    Read-only; degrades gracefully without git (A2 skipped). PORTABLE via _FRESHNESS_FILES.
    Logic single-sourced in scripts/canonical_freshness_gate.py (the same module the mesh carrier
    deploys consumer-local); this leg only wraps its (fails, warns) in the Finding envelope. The
    audit-level `_parse_last_reviewed` / `_git_last_commit_date` are passed in so tests that
    monkeypatch them at the audit level still take effect.
    """
    fails, warns = _cfg.evaluate(
        repo_path, _FRESHNESS_FILES,
        parse_fn=_parse_last_reviewed, git_date_fn=_git_last_commit_date)

    if fails:
        evidence = f"{len(fails)} stale (edited since review): " + "; ".join(fails)
        if warns:
            evidence += f" | also {len(warns)} warn: " + "; ".join(warns)
        return [Finding("canonical_freshness", "fail", evidence)]
    if warns:
        return [Finding("canonical_freshness", "warn", "; ".join(warns))]
    return [Finding("canonical_freshness", "pass",
                    f"{len(_FRESHNESS_FILES)} canonical living files fresh "
                    f"(last_reviewed not before last edit; within {_FRESHNESS_CADENCE_DAYS}d)")]


def _git_registered_worktrees(repo_path: Path) -> Optional[set[str]]:
    """Normcased absolute paths of every git worktree registered for `repo_path`.

    Read-only (`git worktree list --porcelain`). Returns None when git is absent or the
    path is not a git repo, so a non-git consumer degrades gracefully (the orphan check is
    then skipped) — same pattern as `_git_last_commit_date`. Paths are normalized through
    `Path.resolve()` + `os.path.normcase` so the on-disk comparison is robust to git's
    forward-slash output and Windows' case-insensitive filesystem.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    registered: set[str] = set()
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            raw = line[len("worktree "):].strip()
            try:
                registered.add(os.path.normcase(str(Path(raw).resolve())))
            except OSError:
                registered.add(os.path.normcase(raw))
    return registered


def _git_repo_root_name(repo_path: Path) -> Optional[str]:
    """Directory name of the MAIN worktree (repo root) for `repo_path`.

    A linked worktree's own basename is a throwaway (`.dev-knowledge-<topic>`); the durable
    repo identity is the main worktree's directory name. `git rev-parse --git-common-dir`
    returns the SHARED `.git` gitdir — `<main-root>/.git` — from any worktree of the repo, so
    its parent's name is the repo-root identity regardless of which worktree we audit from.

    Read-only (`git rev-parse`). Returns None when git is absent or the path is not a git repo
    (same graceful-degradation contract as `_git_registered_worktrees`), so a non-git consumer
    falls back to the working-dir basename at the call site.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    common = result.stdout.strip()
    if not common:
        return None
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = Path(repo_path) / common_path
    try:
        common_path = common_path.resolve()
    except OSError:
        pass
    # `--git-common-dir` is the main worktree's `.git` gitdir; its parent is the repo root.
    return common_path.parent.name


def _looks_like_worktree_remnant(path: Path) -> bool:
    """True when `path` shows evidence of being a torn-down worktree leftover rather
    than an independent repo or an unrelated populated folder.

    Either signal suffices:
      - the directory is EMPTY — the canonical orphan (`.dev-knowledge-cadence` was empty
        after git deregistered it but the shell survived); or
      - it carries a `.git` *gitlink file* (not a `.git/` directory) — the marker a git
        worktree leaves behind, so a half-removed/deregistered worktree that still holds
        content is still caught.

    A legitimate same-prefix sibling is therefore NOT flagged: an independent git repo has
    a `.git/` *directory* (not a gitlink file) plus content, and an unrelated populated
    folder has neither signal. This narrows the detector to actual worktree evidence
    (Codex H1, 2026-06-02) without weakening the registration gate.
    """
    try:
        entries = list(path.iterdir())
    except OSError:
        return False
    if not entries:
        return True
    return (path / ".git").is_file()


def check_no_sibling_orphans(repo_path: Path) -> list[Finding]:
    """No orphaned `<repo>-*` sibling directories left behind by a torn-down worktree
    (no-leftovers invariant — ADR-61/ADR-68, PLAYBOOK G5).

    A parallel-session or night-agent worktree is created as a `<repo>-<topic>` sibling
    next to the repo and removed at goal/run end. When `git worktree remove` silently
    no-ops (the directory is process-locked) and the teardown is not re-checked, git
    deregisters the worktree but the empty directory survives on disk as an orphan — the
    `.dev-knowledge-cadence` / `.dev-knowledge-night-adr` failure (cleaned 2026-06-02).

    A sibling is flagged only when BOTH hold:
      - it is NOT a registered git worktree (registration is the primary gate — a `<repo>-*`
        sibling that IS registered is legitimate in-use parallel work, never flagged); AND
      - it shows worktree-remnant evidence (empty, or a `.git` gitlink file) per
        `_looks_like_worktree_remnant` — so a legitimate same-prefix sibling repo or
        populated folder is not mistaken for an orphan (Codex H1).

    A presence-checking audit structurally cannot catch a directory that exists but should
    not (2026-05-17 decommissioning-gap LESSON), so this is an explicit negative assertion —
    the mechanization PLAYBOOK "No leftovers ... invariant" names (referenced by section name,
    not line number, so it does not drift).

    Read-only (`git worktree list`). Degrades gracefully without git (skipped). PORTABLE:
    a child repo inherits it unchanged — `repo_path.name` resolves to that repo's prefix.
    """
    registered = _git_registered_worktrees(repo_path)
    if registered is None:
        return [Finding("no_sibling_orphans", "pass",
                        "git unavailable or not a repo - sibling-orphan check skipped")]
    prefix = repo_path.name + "-"
    try:
        siblings = sorted(
            p for p in repo_path.parent.iterdir()
            if p.is_dir() and p.name.startswith(prefix))
    except OSError:
        return [Finding("no_sibling_orphans", "pass",
                        "parent directory unreadable - sibling-orphan check skipped")]
    orphans = [
        p.name for p in siblings
        if os.path.normcase(str(p.resolve())) not in registered
        and _looks_like_worktree_remnant(p)]
    if orphans:
        return [Finding("no_sibling_orphans", "fail",
                        f"Unregistered '{prefix}*' sibling dir(s) next to repo - worktree "
                        f"orphan(s) left behind (remove, or re-register if live): {orphans}")]
    return [Finding("no_sibling_orphans", "pass",
                    f"No orphaned '{prefix}*' siblings (each is a registered worktree or a "
                    f"real repo/folder, not a worktree remnant; or none exist)")]


# ADR-38 A6 (2026-06-02): the universal [U] heading spine each canonical file must
# carry. Presence-only (not strict order) — child-repo-safe; the [R]/[C] sections
# (repo-specific / conditional) vary per repo and are deliberately NOT asserted.
# A heading matches if any line .startswith() the substring, so a repo's own H1 suffix
# (e.g. "# Journal - ai-council") still matches. The substrings are taken from
# .dev-knowledge's own canonical files, so the self-only health gate passes by
# construction. BACKLOG.md hierarchy beyond "## Big picture" is covered by
# validate_backlog.py, not duplicated here.
_CANONICAL_SPINE = {
    "VISION.md": ["## Vision", "## Scope", "## Values", "## Lifecycle", "## References"],
    "ARCHITECTURE.md": ["## Purpose", "## Codemap", "## Layer Boundaries & Invariants",
                        "## Key conventions", "## Authority and governance",
                        "## Validators and enforcement"],
    "CLAUDE.md": ["## 1. First read", "## 5. Critical rules", "## 6. Session start protocol"],
    "BACKLOG.md": ["## Big picture"],
    "CONTRIBUTING.md": ["## Branch naming", "## Commit style", "## Handoff process"],
    "JOURNAL.md": ["# Journal"],
    "LESSONS.md": ["# Lessons Learned"],
}


def _heading_present(lines: list[str], heading: str) -> bool:
    """True if some line IS `heading` or continues it past a word boundary.

    Boundary-aware so a repo-specific suffix matches but a near-miss does not:
    `## Purpose [CORE]` and `# Journal - ai-council` satisfy `## Purpose` / `# Journal`,
    while `## Visionary` and `# Journalized` do NOT satisfy `## Vision` / `# Journal`
    (the char after the heading must be absent or a non-word boundary, not a letter or
    digit). Closes Codex review HIGH 2026-06-02 (startswith false-pass).
    """
    n = len(heading)
    for line in lines:
        if not line.startswith(heading):
            continue
        rest = line[n:]
        if rest == "" or not (rest[0].isalnum() or rest[0] == "_"):
            return True
    return False


def check_canonical_structure(repo_path: Path) -> list[Finding]:
    """Each present canonical file carries its [U] heading spine (ADR-38 A6).

    Asserts the universal navigation backbone only — presence of required headings,
    not their order, and not the [R]/[C] sections that legitimately vary per repo. A
    canonical file that is ABSENT is not flagged here (presence is owned by
    check_adr38_baseline / check_canonical_md_visibility); this check validates the
    shape of files that exist. Read-only and child-repo-safe: a not-yet-unified repo
    FAILs, surfacing the structural gap without blocking .dev-knowledge (health is
    self-only).
    """
    missing: list[str] = []
    for fname, required in _CANONICAL_SPINE.items():
        fpath = repo_path / fname
        if not fpath.exists():
            continue
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        for heading in required:
            if not _heading_present(lines, heading):
                missing.append(f"{fname}: {heading!r}")
    if missing:
        return [Finding("canonical_structure", "fail",
                        f"Canonical file(s) missing required spine heading(s): {missing}")]
    return [Finding("canonical_structure", "pass",
                    "All present canonical files carry their required [U] spine headings")]


_STAMP_RE = re.compile(r"stamp\s+v?(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE)
_STAMP_FILES = ["ARCHITECTURE.md", "CONTRIBUTING.md"]


def check_handoff_version_stamp(repo_path: Path) -> list[Finding]:
    """HANDOFF_PROCESS.md version header matches 'stamp v?X.Y' occurrences in living docs.

    Parses the canonical version from the `Version:` line in
    protocols/HANDOFF_PROCESS.md, then greps ARCHITECTURE.md and CONTRIBUTING.md
    for `stamp v?X.Y` patterns. FAILs if any stamp's version does not match the
    canonical version — the S1 recurrence class surfaced in nightly arc #81.
    Read-only; child-repo-safe (HANDOFF_PROCESS.md absent → pass-with-skip).
    """
    spec = repo_path / "protocols" / "HANDOFF_PROCESS.md"
    if not spec.exists():
        return [Finding("handoff_version_stamp", "pass",
                        "no protocols/HANDOFF_PROCESS.md — nothing to validate")]

    spec_text = spec.read_text(encoding="utf-8")
    version_match = re.search(r"^Version:\s+v?(\d+\.\d+(?:\.\d+)?)", spec_text, re.MULTILINE)
    if not version_match:
        return [Finding("handoff_version_stamp", "warn",
                        "protocols/HANDOFF_PROCESS.md: no parseable 'Version:' line")]
    canonical = version_match.group(1)

    mismatches: list[str] = []
    found_any = False
    for fname in _STAMP_FILES:
        fpath = repo_path / fname
        if not fpath.exists():
            continue
        for lineno, line in enumerate(fpath.read_text(encoding="utf-8").splitlines(), start=1):
            m = _STAMP_RE.search(line)
            if m:
                found_any = True
                stamp_ver = m.group(1)
                if stamp_ver != canonical:
                    mismatches.append(
                        f"{fname}:{lineno}: stamp {stamp_ver!r} != canonical {canonical!r}"
                    )

    if mismatches:
        return [Finding("handoff_version_stamp", "fail",
                        f"{len(mismatches)} stamp mismatch(es): " + "; ".join(mismatches))]
    if not found_any:
        return [Finding("handoff_version_stamp", "warn",
                        f"No 'stamp vX.Y' patterns found in {_STAMP_FILES} — "
                        "convention may have drifted")]
    return [Finding("handoff_version_stamp", "pass",
                    f"All stamp occurrences in {_STAMP_FILES} match "
                    f"canonical HANDOFF_PROCESS v{canonical}")]


@dataclass
class CoupledSet:
    """A family of hand-maintained surfaces that must share one authority version (#11).

    A *straggler* — a surface left at a stale version after a multi-surface amendment — is
    the v3.4-abort failure class (LESSONS.md 2026-05-29: the skill announced v3.3.3 while the
    spec was v3.4). `anchor` is the source of truth; every `surface` must agree with it at
    `granularity`. Each regex carries exactly one capture group yielding a dotted version.
    Membership criterion is SEMANTIC intent-to-mirror, not mere co-occurrence of a version.
    """
    name: str
    anchor: tuple[str, str]                  # (path, regex with one capture group)
    surfaces: list[tuple[str, str]]          # [(path, regex with one capture group), ...]
    granularity: str = "full"                # "full" (X.Y[.Z], trailing-zero-normalized) | "major"


# The live coupled-surface manifest — the cross-case "checklist as data" (#11). Add a set
# when a new family of surfaces must track one authority version. Honest limit: this guards
# only surfaces that still HAND-MAINTAIN a version; surfaces de-hardcoded to interpolate the
# spec ({{VERSION}}) carry no static token and are out of scope by design.
_COUPLED_VERSION_SETS: list[CoupledSet] = [
    CoupledSet(
        name="handoff-major-version",
        anchor=("protocols/HANDOFF_PROCESS.md", r"(?m)^Version:\s+v?(\d+(?:\.\d+)*)"),
        surfaces=[
            # The major the command declares it implements — mirrors the spec's major
            # (the full version/status is de-hardcoded to {{VERSION}}, out of scope).
            # Keyed on the NORMATIVE "handoff per HANDOFF_PROCESS.md vN" declaration so a
            # non-authority mention (e.g. a historical "HANDOFF_PROCESS.md v4.2 Amendment"
            # note) does NOT false-match (Codex HIGH-2 / the semantic-coupling criterion).
            ("CLAUDE.md", r"handoff per `?HANDOFF_PROCESS\.md`?\s+v(\d+)\b"),
            (".claude/commands/handoff.md", r"handoff per `?HANDOFF_PROCESS\.md`?\s+v(\d+)\b"),
        ],
        granularity="major",
    ),
]


def _norm_version(raw: str, granularity: str) -> tuple[int, ...]:
    """Parse a dotted version to an int tuple at `granularity`.

    "major" -> (X,); "full" -> (X, Y, ...) with trailing zeros stripped so 3.4 == 3.4.0.
    """
    parts = [int(p) for p in raw.split(".") if p.isdigit()]
    if not parts:
        return ()
    if granularity == "major":
        return (parts[0],)
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


# rule: coherence-amendment
def check_amendment_coherence(
    repo_path: Path, _sets: Optional[list[CoupledSet]] = None) -> list[Finding]:
    """#11 multi-surface amendment gate: coupled surfaces must share one authority version.

    Converts LESSON-#9's advisory "cross-case trace before a multi-surface amendment" guard
    into an enforced gate (the v3.4 self-handoff abort: the skill announced v3.3.3 while the
    spec was v3.4 — a version STRAGGLER that mis-signalled authority). For each set in the
    manifest (_COUPLED_VERSION_SETS): read the anchor's authority version; every coupled
    surface must agree at the set's granularity. A disagreement is a straggler -> FAIL.

    Child-repo-safe: a set whose anchor file is absent is skipped; an absent surface file is
    skipped; the hub anchors are absent on child repos -> all sets skip -> PASS. An anchor
    present-but-unparseable is reported as drift (WARN), never a FAIL.

    Honest enforcement limit (state-honest-enforcement-limits): guards only surfaces that
    still HAND-MAINTAIN a version. De-hardcoded surfaces (handoff skill/templates interpolate
    {{VERSION}}) carry no static token and are out of scope by design — de-hardcoding, not
    this gate, prevents their straggler class. The narrow `check_handoff_version_stamp` owns
    the full `stamp vX.Y` mirrors in _STAMP_FILES; this is the generalized manifest for other
    coupled families. Read-only.
    """
    sets = _COUPLED_VERSION_SETS if _sets is None else _sets
    stragglers: list[str] = []
    drift: list[str] = []
    checked = 0
    for cset in sets:
        anchor_path, anchor_re = cset.anchor
        ap = repo_path / anchor_path
        if not ap.exists():
            continue  # child-repo-safe skip
        am = re.search(anchor_re, ap.read_text(encoding="utf-8", errors="replace"))
        if not am:
            drift.append(f"{cset.name}: anchor {anchor_path} has no parseable version")
            continue
        canonical = _norm_version(am.group(1), cset.granularity)
        if not canonical:
            drift.append(f"{cset.name}: anchor {anchor_path} version unparseable {am.group(1)!r}")
            continue
        for spath, sre in cset.surfaces:
            fp = repo_path / spath
            if not fp.exists():
                continue
            rx = re.compile(sre)
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
            surface_hits = 0
            for lineno, line in enumerate(lines, 1):
                m = rx.search(line)
                if not m:
                    continue
                surface_hits += 1
                checked += 1
                if _norm_version(m.group(1), cset.granularity) != canonical:
                    stragglers.append(
                        f"{spath}:{lineno}: {m.group(1)!r} != anchor "
                        f"{am.group(1)!r} (set {cset.name})")
            if surface_hits == 0:
                # Present surface, no normative mention -> the coupling marker vanished
                # (reworded/removed). Surface it as drift, never silently PASS (Codex
                # HIGH-1). WARN not FAIL: a removed mention may be legitimate. Anchor-
                # absent (child) repos never reach here, so this cannot false-WARN a child.
                drift.append(
                    f"{cset.name}: surface {spath} present but no normative version "
                    f"mention matched (coupling marker missing/reworded?)")

    if stragglers:
        ev = f"{len(stragglers)} version straggler(s): " + "; ".join(stragglers)
        if drift:
            ev += " | drift: " + "; ".join(drift)
        return [Finding("amendment_coherence", "fail", ev)]
    if drift:
        return [Finding("amendment_coherence", "warn", "; ".join(drift))]
    return [Finding("amendment_coherence", "pass",
                    f"{checked} coupled-surface version mention(s) coherent across "
                    f"{len(sets)} set(s)")]


_FLOOR_MD_REF_RE = re.compile(r"[A-Za-z0-9_-]+\.md")


# rule: governance-child-floor
def check_floor_integrity(repo_path: Path) -> list[Finding]:
    """Child methodology-floor conformance (ADR-78 O2; methodology_surface zone, ADR-75).

    Skipped (PASS) when the repo carries no .claude/CLAUDE-FLOOR.md — the floor rollout is gradual,
    and the hub itself (where `health` runs this) is the floor SOURCE, not a carrier, so it
    has none. Where a floor IS present, three conformance signals (all FAIL on violation):

      - Hash integrity: sha256 of the floor (LF-normalized, autocrlf-proof) must match the
        committed CLAUDE-FLOOR.md.sha256 sidecar. A mismatch means the floor was edited
        without regenerating (run the hub generator) or tampered with (restore it).
      - F5 self-containment: no hub-internal artifact tokens leak into the floor (the
        shared generate_floor.F5_BLACKLIST — ADR-72 self-containment / ADR-78 §3 grep).
      - Pointer existence (T3 fold-in): every same-repo `*.md` the floor names must exist
        in the repo (a zero-URL floor has no external links to check).

    Hash + F5 mirror the generator's emit-time gate so a drifted floor is caught fleet-side;
    the sidecar-match here is the hub-runnable signal the tamper test exercises (`audit repo
    <child>`). Read-only; child-repo-safe.
    """
    floor = repo_path / ".claude" / "CLAUDE-FLOOR.md"
    if not floor.exists():
        return [Finding("floor_integrity", "n/a",
                        "no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip)")]

    text = floor.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    # 1. Hash integrity vs sidecar.
    sidecar = repo_path / ".claude" / "CLAUDE-FLOOR.md.sha256"
    actual = _floor_sha256(text)
    if not sidecar.exists():
        issues.append("CLAUDE-FLOOR.md.sha256 sidecar missing (regenerate via hub generator)")
    else:
        m = re.search(r"[0-9a-f]{64}", sidecar.read_text(encoding="utf-8", errors="replace"))
        expected = m.group(0) if m else ""
        if not expected:
            issues.append("CLAUDE-FLOOR.md.sha256 has no parseable sha256")
        elif actual != expected:
            issues.append(
                f"hash drift: floor sha256 {actual[:12]}… != sidecar {expected[:12]}… — floor "
                "edited without regenerating (run hub generator) OR tampered (restore the floor)")

    # 2. F5 self-containment.
    leaks = [label for label, pat in _FLOOR_F5 if pat.search(text)]
    if leaks:
        issues.append(f"F5 self-containment violation — hub-internal token(s) in floor: {leaks}")

    # 3. Pointer existence (same-repo .md targets the floor names).
    refs = {r for r in _FLOOR_MD_REF_RE.findall(text) if r != "CLAUDE-FLOOR.md"}
    broken = sorted(r for r in refs if not (repo_path / r).exists())
    if broken:
        issues.append(f"floor names same-repo file(s) that do not exist: {broken}")

    if issues:
        return [Finding("floor_integrity", "fail", "; ".join(issues))]
    return [Finding("floor_integrity", "pass",
                    f"CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve "
                    f"(sha256 {actual[:12]}…)")]


def check_hooks_armed(repo_path: Path) -> list[Finding]:
    """RF-2 (Fable architecture review 2026-07-04 §4): make the hub apply
    configured->armed->proven to ITSELF. Asserts the three pre-commit-managed git hooks are
    actually installed in this checkout — `.git/hooks/{pre-commit,commit-msg,pre-push}` exist
    AND carry the pre-commit signature — so a configured-but-unarmed window (a fresh clone, or
    a manually deleted hook) fails LOUD instead of silently letting a gate never fire (the
    `.pre-commit-config.yaml` header's own warning; the direct-to-main 533109f that RF-2 cites).

    Hub-only: arming is per-checkout machine state and the hub is the authority (RF-2) — consumer
    arming is measured by the Informant (scripts/enforcement_coverage.py). n/a when the repo
    carries no .pre-commit-config.yaml (nothing to arm) or is not a standard git checkout (no
    resolvable hooks dir). FAIL — not WARN — on a missing/foreign hook: the RF-2 acceptance is
    that deleting `.git/hooks/pre-push` turns `audit.py health` non-green. Fail-soft: any internal
    error -> WARN (never wedge the commit gate). Read-only.

    The self-arm that KEEPS this green is the SessionStart `python -m pre_commit install -t ...`
    hook in .claude/settings.json (added by the same RF-2 arc). Presence/arming infra, not a
    doc->code behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("hooks_armed", "pass",
                        "hub-only — git-hook arming check skipped (not the hub repo)")]
    try:
        if not (Path(repo_path) / ".pre-commit-config.yaml").exists():
            return [Finding("hooks_armed", "n/a",
                            "no .pre-commit-config.yaml — no managed git hooks to arm")]
        gp = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=repo_path, capture_output=True, text=True, timeout=10,
        )
        if gp.returncode != 0:
            return [Finding("hooks_armed", "n/a",
                            "not a standard git checkout (no resolvable hooks dir)")]
        hooks_dir = (Path(repo_path) / gp.stdout.strip()).resolve()
        issues: list[str] = []
        for name in ("pre-commit", "commit-msg", "pre-push"):
            hook = hooks_dir / name
            if not hook.exists():
                issues.append(f"{name} absent (run `pre-commit install -t {name}`)")
                continue
            body = hook.read_text(encoding="utf-8", errors="replace")
            if "File generated by pre-commit" not in body:
                issues.append(f"{name} present but not pre-commit-managed (foreign hook)")
            elif f"--hook-type={name}" not in body:
                issues.append(f"{name} wired for the wrong hook-type")
        if issues:
            return [Finding("hooks_armed", "fail",
                            ("git hooks not armed (RF-2) — SessionStart self-arm should install "
                             "them: " + "; ".join(issues)).replace("|", "/"))]
        return [Finding("hooks_armed", "pass",
                        "pre-commit / commit-msg / pre-push installed and pre-commit-managed")]
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("hooks_armed", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]


# rule: governance-backlog-leave
def check_git_backlog_drift(repo_path: Path) -> list[Finding]:
    """#90 git<->backlog reconciliation (direction (a) STRONG, ADR-65).

    Hub-only: ALL_CHECKS runs per-repo across the fleet, but the `closes [#id]`
    convention + ADR-65 "done items leave" are .dev-knowledge-specific, so on any
    other repo this is a no-op pass. On the hub: a `closes [#id]` commit (full
    history) whose `[#id]` is still present in BACKLOG.md is drift — the closing
    commit fired but the done item never left the file.

    Awareness layer, not a gate: emits WARN on drift (never FAIL → `health` exits 1
    only on FAIL, so this never blocks the audit-health commit gate). Fail-soft on
    any error — a git/parse hiccup must never wedge `audit.py health`. Read-only.
    Detection + formatting live in scripts/validate_git_backlog.py (reused).
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("git_backlog_drift", "pass",
                        "hub-only — git<->backlog drift check skipped (not the hub repo)")]
    try:
        drift = _vgb.reconcile(Path(repo_path), Path(repo_path) / "BACKLOG.md")
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("git_backlog_drift", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not drift:
        return [Finding("git_backlog_drift", "pass",
                        "no closed-but-present backlog drift (direction (a) STRONG, full history)")]
    # ONE Finding per drifted id (atomic). A single aggregate WARN would let the #147
    # ship-gate disposition the WHOLE finding on one matched id and wave a DIFFERENT,
    # undispositioned drift through (Codex CRITICAL 2026-06-10): dispositions match a
    # whole Finding, so the disposition unit must equal the concern unit. Per-id findings
    # gate each drift independently. format_findings({id: ...}) reused (no parallel logic).
    return [
        Finding("git_backlog_drift", "warn",
                ("closed-but-present (ADR-65 done-items-leave): "
                 + _vgb.format_findings({cid: drift[cid]})).replace("|", "/"))
        for cid in sorted(drift, key=int)
    ]


# rule: coherence-doc-claims
def check_doc_claims(repo_path: Path) -> list[Finding]:
    """#89 prose-vs-state: a living doc's count/list CLAIMS vs repo ground truth.

    Hub-only: the claim anchors (ARCHITECTURE "N registered checks", "pre-commit gates
    (N)", CLAUDE §9 roster) are .dev-knowledge-specific, so on any other repo this is a
    no-op pass. Catches edited-but-not-reconciled prose that check #10 (last_reviewed
    staleness) and #13 (HANDOFF version stamps) cannot see; cross-file fidelity / rot
    is #140's, not this check's.

    Awareness layer, not a gate: emits WARN on a mismatch or an anchor-not-found
    (never FAIL → never blocks the audit-health commit gate). The expensive claim-3
    (pytest --collect-only) runs only off the gate (run_expensive=not _GATE_MODE).
    Fail-soft on any error. Read-only. Logic lives in scripts/validate_doc_claims.py.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("doc_claims", "pass",
                        "hub-only — prose-vs-state check skipped (not the hub repo)")]
    try:
        results = _vdc.reconcile(Path(repo_path), len(ALL_CHECKS),
                                 run_expensive=not _GATE_MODE)
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_claims", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    mismatches = [r for r in results if r.status == "mismatch"]
    missing = [r for r in results if r.status == "anchor-missing"]
    if mismatches:
        evidence = (f"{len(mismatches)} prose claim(s) drifted from repo state: "
                    + _vdc.format_findings(results)).replace("|", "/")
        return [Finding("doc_claims", "warn", evidence)]
    if missing:
        evidence = ("anchor(s) not found (doc reworded? re-anchor or accept): "
                    + ", ".join(f"{m.name}@{m.doc}" for m in missing)).replace("|", "/")
        return [Finding("doc_claims", "warn", evidence)]
    matched = sum(1 for r in results if r.status == "match")
    return [Finding("doc_claims", "pass",
                    f"{matched} doc self-claim(s) match repo state")]


# rule: coherence-doc-rot
def check_doc_rot(repo_path: Path) -> list[Finding]:
    """#140 doc-rot / grooming checker — the Layer-2 deterministic-trigger for **ADR-88 FC4**
    (history-accretion bloat). Surfaces inline-history accretion so it can't rot silently, and
    (riding this gate) blocks NEW accretion going forward. Load-bearing doctrine: condense
    inline history to git (ADR-65), retire inline changelogs (ADR-49), groom on cadence
    (ADR-41). DETECT-ONLY / condense-preserving — never edits, never removes a rule.

    Hub-only: BACKLOG.md + the hub living docs are .dev-knowledge-specific, so on any other repo
    this is a no-op pass. Four sub-detectors (BACKLOG inline-history accretion, Section-history
    accretion, file-bloat vs a declared budget, grooming-cadence lapse) — scripts/validate_doc_rot.py.

    Awareness layer, not a gate: emits one WARN PER rot locus (never FAIL -> never blocks the
    audit-health commit gate; one Finding per locus so the #147 ship-gate dispositions each
    independently — same contract as git_backlog_drift / no_ff_merges). Scope boundary: #140's
    cross-file fidelity drift -> coherence-spine (#179/#180/#182, #89 owns one doc's OWN
    self-claims); intra-file duplication -> #190 — both deferred, not built here. Fail-soft on
    any error. Read-only. Logic lives in scripts/validate_doc_rot.py.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("doc_rot", "pass",
                        "hub-only — doc-rot / grooming checker skipped (not the hub repo)")]
    try:
        results = _vdr.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_rot", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        return [Finding("doc_rot", "pass",
                        "no history-accretion bloat past thresholds "
                        "(backlog / section-history / file-budget / grooming-cadence)")]
    return [
        Finding("doc_rot", "warn",
                f"history-accretion bloat: {_vdr.format_findings([r])}".replace("|", "/"))
        for r in results
    ]


def check_undeclared_edges(repo_path: Path) -> list[Finding]:
    """#179 undeclared-edge scan wired as a ship-gate WARN leg (Fable consult #1 ruling #2,
    2026-07-03). Surfaces docs that reference a registered spec in PROSE but carry no
    `reconciled_with: <spec>@<ver>` declaration (ADR-88 failure class FC2) — the DISCOVERY half
    of the coherence spine that validate_reconciliation's staleness gate (which only sees
    already-declared edges) is blind to.

    Hub-only: the spec registry + the tracked-mutable corpus are .dev-knowledge-specific, so on
    any other repo this is a no-op pass (mirrors check_doc_rot / check_git_backlog_drift).

    Awareness layer: emits one WARN PER candidate (never FAIL -> never blocks the audit-health
    commit gate; one Finding per candidate so the #147 ship-gate dispositions each independently
    — same contract as doc_rot / git_backlog_drift). A discovery reporter, NOT a doc->code
    behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml (same posture as
    check_enforcement_coverage). Fail-soft: any error -> WARN. Read-only; logic in
    scripts/scan_undeclared_edges.py.

    Tier filter (architect-noted): only Tier<=2 candidates (scan_undeclared_edges._CANDIDATE_TIER_MAX)
    are WARNed. Tier-3 rows are the scan's own explicitly-designated WEAK signals — bare-name prose
    mentions, human-promotable, NOT confirmed content-dependencies — and format_report splits them
    off the same way. Filtering to Tier<=2 mirrors the tool's own candidate definition; it does NOT
    hide a genuine undeclared edge (a Tier-3 bare mention is not yet a confirmed edge). The standalone
    reporter (scripts/scan_undeclared_edges.py) still surfaces the Tier-3 signals for human promotion.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("undeclared_edges", "pass",
                        "hub-only — undeclared-edge scan skipped (not the hub repo)")]
    try:
        cands = _sue.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("undeclared_edges", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    candidates = [c for c in cands if c.best_tier <= _sue._CANDIDATE_TIER_MAX]
    if not candidates:
        return [Finding("undeclared_edges", "pass",
                        "no undeclared prose edges (tier<=2) — every registered-spec prose "
                        "reference is declared (reconciled_with) or a tier-3 weak signal")]
    return [
        Finding("undeclared_edges", "warn",
                (f"undeclared prose edge (ADR-88 FC2): {c.dependent_path} -> {c.spec_id} "
                 f"(tier {c.best_tier}) — declare `reconciled_with` or disposition")
                .replace("|", "/"))
        for c in candidates
    ]


# rule: coherence-doc-structure
def check_doc_structure(repo_path: Path) -> list[Finding]:
    """Prose **structural** linter (supplement organ #2) — the Layer-2 deterministic-trigger
    for **ADR-88's prose-shape coherence**: section-numbering integrity, header-scheme
    consistency, ToC accuracy. Surfaces the structural rot the architect provably cannot
    eyeball (proven 2/2 false this session: the PLAYBOOK §18 gap + embedded-template H2s).
    DETECT-ONLY — never edits / renumbers / auto-fixes.

    Hub-only: the living docs scanned are .dev-knowledge-specific, so on any other repo this
    is a no-op pass. Five sub-detectors (numbering integrity, header-scheme consistency, ToC
    accuracy, dangling-allow self-policing, Ch/§ two-part heading-scheme integrity) —
    scripts/validate_doc_structure.py. Documented-intentional cases pass via co-located
    `structure-allow` markers + the fence-aware parser.

    Awareness layer, not a gate: emits one WARN PER structural locus (never FAIL -> never
    blocks the audit-health commit gate; one Finding per locus so the #147 ship-gate
    dispositions each independently — same contract as doc_rot / git_backlog_drift). Distinct
    failure class from #140 (history-accretion bloat) — follows its pattern, no overlap.
    Fail-soft on any error. Read-only. Logic lives in scripts/validate_doc_structure.py.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("doc_structure", "pass",
                        "hub-only — prose structural linter skipped (not the hub repo)")]
    try:
        results = _vds.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_structure", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        return [Finding("doc_structure", "pass",
                        "no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme)")]
    return [
        Finding("doc_structure", "warn",
                f"structural rot: {_vds.format_findings([r])}".replace("|", "/"))
        for r in results
    ]


# rule: governance-no-ff
def check_no_ff_merges(repo_path: Path) -> list[Finding]:
    """#153 `--no-ff` merge guard (core-invariants rule 5).

    Hub-only: the rule + the sanctioned-automation allowlist are tuned to
    .dev-knowledge's main, so on any other repo this is a no-op pass (a fleet-wide
    expansion is deferred under #153). Surfaces a non-merge commit on main's
    first-parent spine since the enforcement baseline — a direct-to-main commit or a
    fast-forwarded feature commit the `--no-ff` rule forbids — that does NOT carry an
    ADR-80 automation marker (`chore(routine/…)` scope or a `Routine:` trailer).

    Awareness layer, not a gate: emits one WARN per violation (never FAIL → never
    blocks the audit-health commit gate; one Finding per violation so the #147
    ship-gate dispositions them independently — same contract as git_backlog_drift).
    DETECT-AND-SURFACE, not prevent: git fires no commit-hook on a fast-forward, so
    this cannot block the merge itself; it removes the silence (true prevention = a
    pre-push hook, deferred under #153). Fail-soft on any error. Read-only. Detection
    lives in scripts/validate_no_ff.py.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("no_ff_merges", "pass",
                        "hub-only — --no-ff guard skipped (not the hub repo)")]
    try:
        violations = _vnf.find_violations(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("no_ff_merges", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not violations:
        return [Finding("no_ff_merges", "pass",
                        f"no non-merge commits on main since {_vnf.BASELINE_DATE} "
                        "(--no-ff rule, core-invariants #5; one rule, no exemptions — ADR-84)")]
    return [
        Finding("no_ff_merges", "warn",
                ("non-merge commit on main (FF/direct — expected a --no-ff merge): "
                 + _vnf.format_one(v)).replace("|", "/"))
        for v in violations
    ]


def _bundle_target_repo(bundle_dir: Path) -> str | None:
    """The declared cross-repo target from a bundle's HANDOFF_BOOT.md `Target repo` row
    (e.g. `ai-council`), or None when the bundle carries no such row (a self-handoff).

    Cross-repo handoffs (ADR-36/41) name their target in the session-header table row
    "| **Target repo** | **<repo>** ... |" (repo in a backtick span); the target is the
    first backtick span of that row. Read-only; fail-soft (any read/parse issue -> None ->
    treated as a self-handoff)."""
    boot = bundle_dir / "HANDOFF_BOOT.md"
    if not boot.exists():
        return None
    try:
        for line in boot.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("|") and "target repo" in s.lower():
                m = re.search(r"`([^`]+)`", s)
                if m:
                    return m.group(1).strip()
    except OSError:
        return None
    return None


# rule: handoff-probes-bind
def check_handoff_probes(repo_path: Path) -> list[Finding]:
    """#163 handoff-probe teeth: every probe in the LATEST v5 PROBES.md bundle binds
    to live state (structural, RESOLVE-ONLY — Critical Rule #4 "Layer 2 never executes",
    zero false positives). Mechanizes the manual v5 probe-gate (HANDOFF_PROCESS §5/§10).

    Bundle-presence-based: validates the lexically-max docs/handoffs/<slug>/PROBES.md
    (excluding aborted/in-progress/archive); a repo with no such bundle is a no-op pass,
    so this no-ops on the fleet's child repos. Only the ACTIVE (latest) handoff is
    checked — older bundles are immutable historical artifacts whose source anchors
    legitimately drift, so re-validating them against current state would mis-flag.

    FAIL-class (gating, unlike the WARN-only doc_claims): a malformed row or a missing
    source/command-target FAILs -> Finding "fail" -> the audit-health + ship-gate block
    (a toothless probe cannot ship). A moved anchor / absent tool -> WARN (anchor-missing
    / skipped: degrade loudly, never a synthesized pass). The "Why" column is checked for
    PRESENCE only — rationale quality stays the manual gate. Fail-soft on any error.
    Read-only. Logic lives in scripts/verify_handoff_probes.py.
    """
    handoffs = Path(repo_path) / "docs" / "handoffs"
    if not handoffs.exists():
        return [Finding("handoff_probes", "pass",
                        "no docs/handoffs/ — no probe bundle to validate")]
    bundles = sorted(
        (d for d in handoffs.iterdir()
         if d.is_dir() and d.name not in _BUNDLE_EXCLUDE_DIRS
         and (d / "PROBES.md").exists()),
        key=lambda d: d.name,
    )
    if not bundles:
        return [Finding("handoff_probes", "pass",
                        "no v5 PROBES.md bundle to validate")]
    latest = bundles[-1]
    # Cross-repo bundle (ADR-36/41): a handoff whose declared target repo differs from this
    # one. Its probes bind to the TARGET repo's files, so resolve against the target root,
    # not the hub — resolving foreign paths against the hub gives both false FAILs (a target
    # file absent here) AND false PASSes (a basename collision like JOURNAL.md fake-resolves).
    # Fleet onboarding (#221) makes cross-repo the common case, so this keeps the teeth rather
    # than skipping them. A `.claude/` or ambiguous foreign target degrades to WARN (#NNN).
    target = _bundle_target_repo(latest)
    cross_repo = bool(target) and target != Path(repo_path).name
    verify_root = None
    if cross_repo:
        cand = Path(repo_path).parent / target
        if not cand.is_dir():
            return [Finding("handoff_probes", "warn",
                            f"cross-repo bundle {latest.name}: target repo '{target}' not "
                            "present as a sibling — cannot resolve foreign probe targets "
                            "(read-only, non-gating)")]
        verify_root = cand
    try:
        results = _vhp.verify(latest, repo_root=verify_root, cross_repo=cross_repo)
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("handoff_probes", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        # PROBES.md exists (it is why this bundle was selected) but parses to zero probe
        # rows -> a toothless manifest. Not a silent pass: a v5 bundle must ship probes.
        return [Finding("handoff_probes", "fail",
                        f"{latest.name}/PROBES.md present but no parseable probe rows "
                        "(toothless manifest)")]
    # One Finding per non-passing probe so the #147 ship-gate dispositions each
    # independently (same contract as git_backlog_drift / no_ff_merges): an aggregate
    # WARN would let one disposition mask an unrelated degraded probe.
    findings: list[Finding] = []
    for r in results:
        if r.status == "fail":
            findings.append(Finding("handoff_probes", "fail",
                f"{r.probe_id} toothless in {latest.name}: {r.detail}".replace("|", "/")))
        elif r.status in ("anchor-missing", "skipped"):
            findings.append(Finding("handoff_probes", "warn",
                f"{r.probe_id} {r.status} in {latest.name}: {r.detail}".replace("|", "/")))
    if findings:
        return findings
    return [Finding("handoff_probes", "pass",
                    f"{len(results)} probe(s) bind to live state ({latest.name})")]


# rule: coherence-spec-reconciled
def check_reconciled_versions(repo_path: Path) -> list[Finding]:
    """Coherence-spine reconciliation gate: a dependent's declared `reconciled_with`
    version must match the spec's CURRENT (live) version.

    A dependent doc declares `reconciled_with: <spec-id>@<version>` in its frontmatter;
    the checker resolves the spec via the registry (validate_reconciliation._SPEC_REGISTRY),
    reads its version LIVE, and compares. In v1 exactly one edge is declared
    (docs/handoffs/README.md -> handoff-process). Generic: a child repo with no
    `reconciled_with` edge is a no-op PASS, so this no-ops on the fleet.

    FAIL-class (gating) on a version mismatch — fail-closed: a dependent still claiming an
    old spec version is the drift this exists to block. One Finding per mismatch so the
    #147 ship-gate dispositions each independently (same contract as git_backlog_drift /
    handoff_probes). A checker that cannot read its OWN inputs (malformed frontmatter,
    unknown spec-id, spec absent/unparseable) -> WARN: fail-OPEN on its own error, never a
    synthesized FAIL. Fail-soft on any unexpected error. Read-only. Logic lives in
    scripts/validate_reconciliation.py.

    The mismatch remediation points at the re-stamp flow (run check-against-spec, then bump
    reconciled_with) — but this gate gates the VERSION MISMATCH only. Running or passing
    check-against-spec is DELIBERATELY never a gate condition here: the semantic skill is
    triggered by the re-stamp flow, not the ship-gate (check-against-spec v1 scope). #205.
    """
    try:
        results = _vr.reconcile(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("reconciled_versions", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    findings: list[Finding] = []
    for r in results:
        if r.status == "mismatch":
            findings.append(Finding("reconciled_versions", "fail",
                (f"{r.dependent_path} declares {r.spec_id}@{r.declared} but spec is "
                 f"{r.current} - re-stamp flow: run check-against-spec "
                 f"(py scripts/validate_reconciliation.py emits the invocation), then "
                 f"bump reconciled_with").replace("|", "/")))
        elif r.status in ("malformed", "unknown-spec"):
            findings.append(Finding("reconciled_versions", "warn",
                (f"{r.dependent_path}: {r.status} ({r.current})").replace("|", "/")))
    if findings:
        return findings
    n = len(results)
    return [Finding("reconciled_versions", "pass",
                    f"{n} reconciled_with edge(s) match live spec version(s)"
                    if n else "no reconciled_with edges declared")]


def _load_declaration_docs(repo_path: Path) -> tuple[str, ...]:
    """Read the doc→code edge declaration-doc include-list (`ecosystem/doc-code-edge.yaml`,
    `declaration_docs:`) — the registry-scoped scan scope for `check_doc_code_edge`. Resolved
    from `repo_path` at call time (NOT a module constant) so the hub guard + tmp-hub tests see
    the right file. Returns repo-relative doc paths (forward slashes), in declared order.

    Fail-soft → () : a missing/malformed file renders the advisory check inert and passes —
    correct while the edge is ADVISORY. NOTE (hard-gate promotion, ADR-89 OQ1 / OQ3): when this
    edge is promoted to a gate, switch to WARN-on-missing/malformed-config so a lost config
    cannot silently disable a live gate. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ()
    if not isinstance(data, dict):
        return ()
    docs = data.get("declaration_docs")
    if not isinstance(docs, list):  # a non-list scalar must degrade, not raise
        return ()
    return tuple(d for d in docs if isinstance(d, str))


def _load_coverage_scope(repo_path: Path) -> tuple[str, ...]:
    """Read the doc->code coverage-scope rule-ID list (`ecosystem/doc-code-edge.yaml`,
    `coverage_scope:`) -- the in-scope enforced rule-IDs the #194 rollout must drive to 100%
    resolved (tests/test_doc_code_edge.py asserts each resolves, xfail-strict until complete).

    Sibling key to `declaration_docs`; same fail-soft -> () contract (a missing/malformed file
    or non-list value yields an empty scope -- the coverage test's non-empty precondition guards
    against a vacuous pass). Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ()
    if not isinstance(data, dict):
        return ()
    scope = data.get("coverage_scope")
    if not isinstance(scope, list):  # a non-list scalar must degrade, not raise
        return ()
    return tuple(s for s in scope if isinstance(s, str))


def _load_multi_site(repo_path: Path) -> dict[str, int]:
    """Read the doc->code multi-site expected-count map (`ecosystem/doc-code-edge.yaml`,
    `multi_site:`) -- per ADR-90 (resolver-allows-N), a rule legitimately enforced in N code
    organs declares its expected `# rule:` site count here, so the resolver resolves it at
    EXACTLY that count instead of classing it `ambiguous` (the strict 1:1 duplicate-guard).

    Sibling key to `coverage_scope`/`declaration_docs`; same fail-soft -> {} contract (a
    missing/malformed file or non-mapping value degrades every rule to the strict 1:1 guard --
    conservative: it can only NARROW what resolves, never silently widen it). Only `str -> int`
    entries with count >= 2 are kept (a bool is rejected -- `bool` is an `int` subclass).
    Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, dict):
        return {}
    raw = data.get("multi_site")
    if not isinstance(raw, dict):  # a non-mapping scalar must degrade, not raise
        return {}
    return {k: v for k, v in raw.items()
            if isinstance(k, str) and isinstance(v, int) and not isinstance(v, bool) and v >= 2}


def _load_coverage_exempt(repo_path: Path) -> set[str]:
    """Read the doc->code coverage drift-guard exempt-list (`ecosystem/doc-code-edge.yaml`,
    `exempt:`) -- the ALL_CHECKS members that are NOT declared doc->code behavioral rules: the
    structural/presence baseline checks + the two self-referential meta-checks (`doc_code_edge`,
    `doc_code_coverage_drift`). Entries are CHECK NAMES (a Finding `check_name` =
    `fn.__name__` minus the `check_` prefix).

    Sibling key to `coverage_scope`/`multi_site`; same fail-soft -> set() contract (a
    missing/malformed file or non-list value yields an empty set -- and `check_doc_code_coverage_drift`
    treats an empty scope-or-exempt as INERT, so an absent config cannot vacuously pass every
    member). Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return set()
    if not isinstance(data, dict):
        return set()
    raw = data.get("exempt")
    if not isinstance(raw, list):  # a non-list scalar must degrade, not raise
        return set()
    return {s for s in raw if isinstance(s, str)}


def check_doc_code_edge(repo_path: Path) -> list[Finding]:
    """#194 doc→code declared-edge integrity (advisory-first, ADR-89 OQ1).

    Discovers every `<!-- rule: ID -->` annotation in the DECLARATION DOCS registered in
    `ecosystem/doc-code-edge.yaml` (`declaration_docs:`) and resolves each to its `# rule: ID`
    code annotation under scripts/ — rule-ID identity + path/AST content resolution, move-safe
    per the e22e883 spike. A `broken_edge` (a side resolves to nothing) or `ambiguous` (a
    duplicated ID) surfaces as a WARN advisory naming the rule-ID + reason; the #194 L1 scan
    (validate_doc_code_edge.scan_structural_integrity) ALSO surfaces a `code_orphan` — a
    `# rule:` annotation declared in no declaration doc (code->nonexistent-rule), the direction
    doc-side resolution structurally cannot see. NEVER FAILs this arc — advisory-first; promotion
    to a gate is data-gated (ADR-89 OQ3).

    Hub-only: the rule-ID edge is a .dev-knowledge governance concept, so on any other repo this
    is a no-op pass. The scan is REGISTRY-SCOPED to the authoritative declaration docs (ADR-89
    OQ1 naming convention) — illustrative `<!-- rule: <domain>-<slug> -->` tokens elsewhere
    (immutable design records, teaching sections, the test fixtures) are out of scope, and
    teaching tokens additionally use the angle-bracket placeholder form (outside the ID charset).
    An empty/absent registry → advisory inactive (fail-soft). Read-only. Discovery + resolution
    live in scripts/validate_doc_code_edge.py.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("doc_code_edge", "pass",
                        "hub-only — doc->code edge check skipped (not the hub repo)")]
    code_root = Path(repo_path) / "scripts"
    try:
        include = _load_declaration_docs(repo_path)
        multi = _load_multi_site(repo_path)  # ADR-90: declared multi-site expected counts
        ids = _vdce.iter_doc_rule_ids(Path(repo_path), include)
        # L1 structural integrity (#194): also surface code-side ORPHANS — a `# rule:` whose ID
        # is declared in NO declaration doc (code->nonexistent-rule), the direction the doc-side
        # resolution below structurally cannot see (it iterates doc-declared IDs only).
        # scan_structural_integrity runs the full L1 scan on the live corpus; its doc-side
        # dangling/duplicate findings are already reported below as broken_edge/ambiguous, so here
        # we take ONLY its code_orphan findings (a disjoint id set — no double-report). Advisory:
        # WARN-only, never a gate (hard-gate promotion is data-gated, ADR-89 OQ3).
        orphans = [f for f in _vdce.scan_structural_integrity(
                       Path(repo_path), code_root, include, multi)
                   if f.kind == "code_orphan"]
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_code_edge", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    # ONE Finding per defect (atomic) — a #147 ship-gate disposition then matches the concern
    # unit, never waving a different undispositioned edge through (the per-id git_backlog_drift
    # rule). resolve_edge / scan_structural_integrity re-scan by content → move-safe (e22e883).
    warns: list[Finding] = [
        Finding("doc_code_edge", "warn",
                (f"{f.rule_id}: code_orphan (code sites={len(f.code_sites)}, "
                 f"no declaration)").replace("|", "/"))
        for f in orphans]
    if not ids:
        # No doc-declared edges — but a code orphan is still a real structural defect to surface.
        return warns or [Finding("doc_code_edge", "pass",
                         "no doc rule-IDs in the declaration-doc registry — advisory inactive "
                         "(ecosystem/doc-code-edge.yaml)")]
    resolved = 0
    for rid in sorted(ids):
        result = _vdce.resolve_edge(rid, Path(repo_path), code_root,
                                    include=include, multi_site=multi)
        if result.status == "resolved":
            resolved += 1
        else:
            warns.append(Finding(
                "doc_code_edge", "warn",
                (f"{rid}: {result.status} (doc sites={len(result.doc_sites)}, "
                 f"code sites={len(result.code_sites)})").replace("|", "/")))
    if warns:
        return warns
    return [Finding("doc_code_edge", "pass",
                    # ASCII arrow: this evidence is printed by cmd_health's click.echo, which
                    # crashes on a Windows cp1252 console for chars outside cp1252 (e.g. U+2192).
                    f"{resolved} doc->code edge(s) resolved; none broken/ambiguous/orphaned")]


def check_safe_removal(repo_path: Path) -> list[Finding]:
    """#195 code->code safe-removal gate: removing a scripts/ module while a live EXTERNAL
    referrer still uses one of its top-level symbols FAILs, naming the referrer. The consumer
    that gives the #193 reverse-dep oracle teeth (GAP-1) and the automated form of the manual
    "scan references before cutting" (LESSONS 2026-06-03) — guards the 2026-03-14 bulk-restore
    failure class (removing still-needed files).

    Diff-triggered: a clean tree (no scripts/*.py deletion vs HEAD) is an instant PASS — no
    Pyright cost. On an actual removal, safe_remove.check_removal materializes a query root
    (working scripts/ + removed module(s) restored from HEAD) and queries the oracle there.

    FAIL-class (gating, like check_handoff_probes): one FAIL Finding per SURVIVING referrer so
    the #147 ship-gate dispositions each independently. The oracle's inability to verify (Pyright
    absent -> oracle-unavailable, or an `ambiguous` symbol) is a single WARN — fail-OPEN + ALLOW
    (operator ruling #195), never a synthesized FAIL. Check's own error -> WARN (fail-soft, never
    wedge audit-health). RESOLVE-ONLY / read-only (Layer 2): the oracle spawns Pyright for
    analysis and writes only a temp dir; this writes no repo files. Logic lives in
    scripts/safe_remove.py.

    HONEST LIMIT (inherited from the oracle): static-Python-only. Dynamic/getattr/string-keyed/
    cross-language referrers are INVISIBLE -> a non-blocking false PASS is possible here, never a
    false FAIL. The reliable catch is the pre-removal CLI (queries the live repo); the automatic
    build-time path's cross-module fidelity depends on Pyright resolving the materialized copy.
    """
    try:
        verdict = _sr.check_removal(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("safe_removal", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if verdict.status == "safe" and not verdict.removal_set:
        return [Finding("safe_removal", "pass", "no scripts/*.py module removal in the diff")]
    findings: list[Finding] = []
    # One FAIL per surviving referrer (atomic disposition unit) — the load-bearing block.
    for r in verdict.surviving_referrers:
        findings.append(Finding(
            "safe_removal", "fail",
            (f"{r['referrer']}:{r['line']} still references {r['symbol']} from removed "
             f"{r['module']} — co-remove the referrer or keep the module").replace("|", "/")))
    # All unverifiable symbols collapse to ONE WARN (honest static-only limit; allow).
    if verdict.unverifiable:
        reasons = ", ".join(sorted({u["reason"] for u in verdict.unverifiable}))
        findings.append(Finding(
            "safe_removal", "warn",
            (f"{len(verdict.unverifiable)} symbol(s) unverifiable ({reasons}) for removal of "
             f"{', '.join(verdict.removal_set)} — WARN+allow, static-only limit").replace("|", "/")))
    if findings:
        return findings
    return [Finding("safe_removal", "pass",
                    (f"removal of {', '.join(verdict.removal_set)} has no surviving referrers")
                    .replace("|", "/"))]


def _markers_for_check(fn) -> set[str]:
    """The rule-ID(s) an ALL_CHECKS member declares: real `# rule:` COMMENT tokens in its own
    source body PLUS the contiguous `#`-comment block immediately above its `def`.

    `inspect.getsourcelines` starts at the `def` line and OMITS the leading annotation, so the
    above-def convention (the marker sits on the line directly above `def`, matching the cohort-1
    annotations) needs the walk-back. Reads real COMMENT tokens only, via
    `validate_doc_code_edge.markers_in_source` -- a marker quoted in a docstring/string is never
    collected. Fail-soft -> set() when the source is unavailable.
    """
    try:
        body_lines, start = inspect.getsourcelines(fn)
    except (OSError, TypeError):
        return set()
    pre: list[str] = []
    try:
        module = sys.modules.get(fn.__module__)
        all_lines = inspect.getsource(module).splitlines(keepends=True)
        i = start - 2  # 0-based index of the line directly above the def
        while i >= 0 and all_lines[i].lstrip().startswith("#"):
            pre.insert(0, all_lines[i])
            i -= 1
    except (OSError, TypeError):
        pre = []
    return _vdce.markers_in_source("".join(pre) + "".join(body_lines))


def _coverage_drift_findings(checks, coverage_scope: set[str],
                             exempt: set[str]) -> list[tuple[str, set[str]]]:
    """The testable core of the #203 drift-guard: return `(check_name, markers)` for every check
    that is NEITHER mapped (>=1 marker, all in `coverage_scope`) NOR exempt. Empty list = full
    coverage. `check_name` = `fn.__name__` minus the `check_` prefix (the Finding identity)."""
    drift: list[tuple[str, set[str]]] = []
    for fn in checks:
        name = fn.__name__.removeprefix("check_")
        markers = _markers_for_check(fn)
        mapped = bool(markers) and markers <= coverage_scope
        if not mapped and name not in exempt:
            drift.append((name, markers))
    return drift


def check_doc_code_coverage_drift(repo_path: Path) -> list[Finding]:
    """#203 doc->code coverage drift-guard. Every ALL_CHECKS member must be EITHER annotated with
    a `coverage_scope` rule-ID marker OR listed in `exempt:` (ecosystem/doc-code-edge.yaml) --
    else FAIL, NAMING the escapee. So a NEW enforced rule landing as an ALL_CHECKS check cannot
    silently escape the curated doc->code `coverage_scope` (the stated drift cost of the FALLBACK
    curated mechanism). FAIL-class (gating, like check_safe_removal); hub-only; read-only.

    SCOPE (honest limit): this guards ONLY the auto-enumerable ALL_CHECKS surface. Enforcement
    organs OUTSIDE ALL_CHECKS -- the seal Stop-hook, the commit-msg / pre-push hooks, the
    standalone pre-commit validators -- are NOT auto-guarded; that heterogeneous remainder stays
    curated (no single auto-enumerable registry across all mechanisms; doc-code-edge.yaml header).
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("doc_code_coverage_drift", "pass",
                        "hub-only -- coverage drift-guard skipped (not the hub repo)")]
    try:
        scope = set(_load_coverage_scope(repo_path))
        exempt = _load_coverage_exempt(repo_path)
        if not scope or not exempt:
            # An empty scope OR exempt would let members pass vacuously -- treat as inert config.
            return [Finding("doc_code_coverage_drift", "warn",
                            "coverage_scope or exempt empty/absent -- drift-guard inert "
                            "(ecosystem/doc-code-edge.yaml)")]
        drift = _coverage_drift_findings(ALL_CHECKS, scope, exempt)
    except Exception as exc:  # never wedge the gate on an internal error
        return [Finding("doc_code_coverage_drift", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if drift:
        return [Finding("doc_code_coverage_drift", "fail",
                        ("ALL_CHECKS member(s) neither coverage_scope-annotated nor exempt: "
                         + "; ".join(f"{n} (markers={sorted(m) or 'none'})" for n, m in drift))
                        .replace("|", "/"))]
    return [Finding("doc_code_coverage_drift", "pass",
                    f"all {len(ALL_CHECKS)} ALL_CHECKS members covered "
                    "(coverage_scope-annotated or exempt); none escape coverage_scope")]


def _fleet_parity_findings(parity_findings, register: dict,
                           fail_verdicts: set, warn_verdicts: set) -> list["Finding"]:
    """Testable core of check_fleet_parity ([#337]): map fleet_parity ParityFinding verdicts
    to gating Findings. ONE Finding PER blocking row (disposition contract, Codex CRITICAL
    2026-06-10) -- a register entry keys on check_name='fleet_parity' + a substring of THIS
    row's evidence, so it suppresses one row, never the whole organ. If no row blocks, ONE
    summary `pass` Finding carrying the full register tally, so stale/advisory counts stay
    VISIBLE without blocking."""
    out: list[Finding] = []
    for f in parity_findings:
        status = ("fail" if f.verdict in fail_verdicts
                  else "warn" if f.verdict in warn_verdicts else None)
        if status:
            ev = f"{f.repo_id} {f.surface_id} {f.verdict}: {f.evidence}"
            out.append(Finding("fleet_parity", status, ev.replace("|", "/")[:300]))
    if not out:
        tally = ", ".join(f"{k} {v}" for k, v in sorted(register.items()) if v)
        out.append(Finding("fleet_parity", "pass",
                           f"fleet at parity -- {tally or 'no findings'} (blocking verdicts: 0)"
                           .replace("|", "/")))
    return out


def check_fleet_parity(repo_path: Path) -> list[Finding]:
    """[#337] fleet-parity gate -- the #328 cross-repo parity walk as a BLOCKING ALL_CHECKS
    member (promoted once [#336] cleared the last standing WARN; the fleet is at a zero-WARN
    steady state). Runs `fleet_parity.walk()` IN-PROCESS (the CLI exit code cannot carry the
    signal -- it is always 0/2) and maps blocking verdicts to Findings. HUB-ONLY: the walk is
    fleet-wide, run from the hub. Manifest-driven (ecosystem/parity-surfaces.yaml), so `exempt:`
    in doc-code-edge.yaml -- like enforcement_coverage / deployed_methodology_version, not a
    doc->code rule. Read-only (Layer-2, ADR-28/36).

    Verdict->status map (operator ruling 2026-07-18): FAIL on refused / must-absent /
    tombstone-violated; WARN (undispositioned -> RED) on warn-undeclared / unavailable /
    tracked-ephemera; stale-declaration + advisory-rewarn stay advisory-but-VISIBLE (surfaced in
    the summary, never RED from a date/corpus advance -- which is why the wall-clock run-date is
    safe). PERF ([#337] rider, 2026-07-18): the walk is ~8s and ALL_CHECKS also runs on the
    per-commit audit-health gate; ship-gate-only scoping is a filed follow-up, not this arc.
    """
    if Path(repo_path).resolve() != Path(_REPO_ROOT).resolve():
        return [Finding("fleet_parity", "pass",
                        "hub-only -- fleet-parity walk skipped (not the hub repo)")]
    try:
        import fleet_parity as fp
        from datetime import date as _date
        r = fp.walk(_date.today().isoformat())
        register = fp.summarize(r.findings)
        fail_v = {fp.REFUSED, fp.MUST_ABSENT, fp.TOMBSTONE_VIOLATED}
        warn_v = {fp.WARN_UNDECLARED, fp.UNAVAILABLE, fp.TRACKED_EPHEMERA}
    except Exception as exc:  # never wedge the gate on an internal error (mirrors coverage-drift)
        return [Finding("fleet_parity", "warn",
                        f"fleet-parity walk degraded (read-only): {exc!r}".replace("|", "/"))]
    return _fleet_parity_findings(r.findings, register, fail_v, warn_v)


def check_deployed_methodology_version(repo_path: Path) -> list[Finding]:
    """ADR-91 deployed-version reporter: read the hub-committed deployed-versions registry
    and report THIS repo's deployed methodology-corpus version.

    The registry (ecosystem/deployed-versions.yaml) is the durable record-home ADR-91 chose
    over the derived ecosystem/index.yaml (which audit.py::regenerate_index overwrites wholesale
    each run). One hub file, read for whichever repo is being audited: the audited repo is keyed
    by its repo-ROOT directory name (the main worktree's basename, resolved via
    `git rev-parse --git-common-dir`), so an audit run from a linked worktree keys the record by
    the parent repo — not the throwaway `<repo>-<topic>` worktree basename (#265) — and each
    repo's state.yaml carries its OWN deployed-version finding that fleet_health surfaces per repo.

    Status: `n/a` while the field is null (no methodology release deployed yet -- the expected
    pre-deploy state; the deploy-runbook writer is a separate, later piece); `pass` with the
    version once set. A repo missing from the registry, or an unreadable/malformed registry,
    -> WARN (fail-OPEN on its own input error, never a synthesized FAIL). Read-only; a status
    reporter, NOT a doc->code behavioral rule (so `exempt` in ecosystem/doc-code-edge.yaml).
    """
    name = "deployed_methodology_version"
    try:
        data = yaml.safe_load(DEPLOYED_VERSIONS_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [Finding(name, "warn",
                        f"deployed-versions.yaml unreadable (read-only, non-blocking): {exc!r}"
                        .replace("|", "/"))]
    repos = data.get("repos") if isinstance(data, dict) else None
    if not isinstance(repos, dict):
        return [Finding(name, "warn",
                        "deployed-versions.yaml missing/malformed 'repos:' map (ADR-91)")]
    # Key by the repo-root basename so a linked worktree audits as its parent repo (#265);
    # fall back to the working-dir basename when git is unavailable (non-git consumer).
    repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name
    if repo_key not in repos:
        return [Finding(name, "warn",
                        f"{repo_key} not listed in deployed-versions.yaml (ADR-91)")]
    entry = repos[repo_key]
    version = entry.get("deployed_methodology_version") if isinstance(entry, dict) else entry
    if version is None:
        return [Finding(name, "n/a",
                        f"{repo_key}: unset -- no methodology release deployed yet "
                        "(deploy-runbook will populate; ADR-91)")]
    return [Finding(name, "pass",
                    f"{repo_key}: deployed methodology corpus v{version}")]


def check_enforcement_coverage(repo_path: Path) -> list[Finding]:
    """Informant Organ leg (Stage-2 enforcement-transfer): a READ-ONLY, non-blocking reporter of
    whether the 5 hub enforcement organs fire locally in the audited consumer.

    STATIC path only here (never clones — this runs on every hub commit via audit-health):
    applicability + locate per organ. `enforcing-local` is provable ONLY by the standalone
    reporter's fire_test (scripts/enforcement_coverage.py), so this leg never claims it — its
    strongest per-organ label is `present-unverified`. Posture (operator-ratified 2026-07-03):
    emits `n/a` — never FAIL/WARN — so it cannot RED the hub's own health/ship gate for this
    known-tracked gap; the gap lives in the digest logs/ENFORCEMENT-COVERAGE.md + the standalone
    reporter. On the hub itself this is `n/a` (the hub is the SOURCE of the organs, not a consumer
    coverage row). A status reporter, NOT a doc->code behavioral rule -> `exempt` in
    ecosystem/doc-code-edge.yaml (ADR-91-sibling posture to check_deployed_methodology_version).
    Fail-soft: any error -> WARN (fail-OPEN on its own input), never wedges a gate.

    Stage-3 (on the record, NOT built here): once a consumer establishes an enforcing-local
    baseline, a regression enforcing-local -> absent should WARN. Deferred backlog item.
    """
    name = "enforcement_coverage"
    if Path(repo_path).resolve() == Path(_REPO_ROOT).resolve():
        return [Finding(name, "n/a",
                        "hub - source of the 5 enforcement organs; per-consumer coverage is "
                        "measured by scripts/enforcement_coverage.py (read-only reporter)")]
    try:
        from scripts import enforcement_coverage as _enfcov
    except ImportError:
        import enforcement_coverage as _enfcov
    try:
        cells = _enfcov.evaluate_static(Path(repo_path))
    except Exception as exc:  # never wedge the audit gate on the reporter's own error
        return [Finding(name, "warn",
                        f"reporter degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    summary = "; ".join(f"{c.organ_id}={c.verdict}" for c in cells)
    return [Finding(name, "n/a",
                    (f"{Path(repo_path).name}: {summary} "
                     "(static; enforcing-local proven only by scripts/enforcement_coverage.py)")
                    .replace("|", "/"))]


# ---------------------------------------------------------------------------
# @import edge integrity (#249) — a Claude-Code `@import` whose target is missing
# silently drops session-boot content. The coherence spine tracks reconciled_with
# PROSE edges (validate_reconciliation) but NOT the `@path` file-include graph, so a
# broken/renamed @import target dangles with no gate (the @.claude/CLAUDE-FLOOR.md and
# the [#244] @-imports have been unchecked this way). This check resolves the transitive
# @import graph from the root CLAUDE.md (BFS, cycle-safe, matches Claude-Code boot
# semantics) and FAILs on any target that resolves to nothing. STRUCTURAL presence check,
# not a doc->code behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml.
# ---------------------------------------------------------------------------

# `@` preceded by start-of-line or whitespace (the (?<!\S) guard excludes emails like
# x@gmail.com and plugin@marketplace tokens); target chars = a path.
_IMPORT_RE = re.compile(r"(?<!\S)@([A-Za-z0-9_~./\\-]+)")
_IMPORT_MAX_DEPTH = 5  # Claude Code resolves @imports recursively up to 5 hops


def _blank_preserving_lines(match: "re.Match[str]") -> str:
    """Replace a multi-line match with the same number of newlines (keeps line nos)."""
    return "\n" * match.group(0).count("\n")


def _strip_code_regions(text: str) -> str:
    """Blank fenced code blocks, HTML comments, and inline code spans so a `@path`
    quoted as an example — or the roster's backtick-neutralized import tokens
    (gen_methodology_roster._neutralize_import) — is not read as a live @import.
    Multi-line regions are blanked line-count-preserving; inline spans are single-line."""
    text = re.sub(r"(?ms)^```.*?^```", _blank_preserving_lines, text)
    text = re.sub(r"(?s)<!--.*?-->", _blank_preserving_lines, text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def _looks_like_import_path(target: str) -> bool:
    """A Claude-Code @import target is a FILE PATH — it has a path separator or a
    (alphabetic) file extension. This excludes version tokens like `@5.4` / `@5.5`
    (a `.4` suffix is not an extension) that pepper the section-history prose."""
    if "/" in target or "\\" in target:
        return True
    return bool(re.search(r"\.[A-Za-z]{2,}$", target))


def _import_targets(text: str) -> list[tuple[int, str]]:
    """Return (1-indexed line-no, target) for each live @import in `text`."""
    out: list[tuple[int, str]] = []
    for i, line in enumerate(_strip_code_regions(text).splitlines(), start=1):
        for m in _IMPORT_RE.finditer(line):
            target = m.group(1)
            if _looks_like_import_path(target):
                out.append((i, target))
    return out


def check_import_edges(repo_path: Path) -> list[Finding]:
    """#249 — every Claude-Code `@import` target reachable from the root CLAUDE.md exists.

    BFS the transitive @import graph (cycle-safe, depth <= 5). A target that resolves
    against neither the importing file's directory nor the repo root is a broken edge
    (FAIL — a broken @import silently drops session-boot content; audit-health makes the
    rename-a-generated-fragment failure mode commit-blocking on the hub). Machine-scoped
    (`~`-home) and absolute targets are skipped (counted, never failed). Read-only.
    """
    name = "import_edges"
    repo_root = Path(repo_path)
    root = repo_root / "CLAUDE.md"
    if not root.exists():
        return [Finding(name, "n/a", "no root CLAUDE.md (presence gated by check_claude_md)")]
    visited: set[Path] = set()
    queue: list[tuple[Path, int]] = [(root, 0)]
    broken: list[str] = []
    edge_count = 0
    file_count = 0
    while queue:
        current, depth = queue.pop(0)
        rc = current.resolve()
        if rc in visited or depth > _IMPORT_MAX_DEPTH:
            continue
        visited.add(rc)
        try:
            text = current.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_count += 1
        for lineno, target in _import_targets(text):
            if target.startswith("~") or Path(target).is_absolute():
                continue  # machine-scoped / absolute — count nothing, never fail
            edge_count += 1
            cand_dir = current.parent / target
            cand_root = repo_root / target
            resolved = cand_dir if cand_dir.exists() else (
                cand_root if cand_root.exists() else None)
            rel = (str(current.relative_to(repo_root))
                   if current.is_relative_to(repo_root) else current.name)
            if resolved is None:
                broken.append(f"{rel}:{lineno} -> @{target}".replace("|", "/"))
            elif resolved.suffix == ".md":
                queue.append((resolved, depth + 1))
    if broken:
        return [Finding(name, "fail",
                        "broken CLAUDE.md @import target(s): " + "; ".join(broken))]
    return [Finding(name, "pass",
                    f"{edge_count} @import edge(s) resolve across {file_count} file(s)")]


ALL_CHECKS = [
    check_vision_md,
    check_adr38_baseline,
    check_claude_md,
    check_dot_prefix_discipline,
    check_canonical_md_visibility,
    check_workspace_settings,
    # check_mermaid_theme_directive retired 2026-07-05 (ADR-51 amendment — LLM-first)
    check_handoff_bundle_structure,
    check_handoff_tag_canonicity,
    check_canonical_freshness,
    check_no_sibling_orphans,
    check_canonical_structure,
    check_handoff_version_stamp,
    check_amendment_coherence,
    check_floor_integrity,
    check_hooks_armed,
    check_git_backlog_drift,
    check_doc_claims,
    check_no_ff_merges,
    check_handoff_probes,
    check_reconciled_versions,
    check_doc_rot,
    check_doc_structure,
    check_doc_code_edge,
    check_safe_removal,
    check_deployed_methodology_version,
    check_enforcement_coverage,
    check_undeclared_edges,
    check_doc_code_coverage_drift,
    check_import_edges,
    check_fleet_parity,   # [#337] blocking #328 fleet-parity gate (was informational)
]


def audit_repo(repo_name: str, repo_path: Path, run_date: date) -> RepoState:
    """Run all checks on a single repo and return updated state."""
    if not repo_path.exists():
        state = RepoState(
            name=repo_name,
            path=str(repo_path),
            last_audit=run_date.isoformat(),
            findings=[Finding("availability", "unavailable", f"Path not found: {repo_path}")],
        )
        return state

    findings: list[Finding] = []
    for check in ALL_CHECKS:
        findings.extend(check(repo_path))
    state = RepoState(
        name=repo_name,
        path=str(repo_path),
        last_audit=run_date.isoformat(),
        findings=findings,
    )
    return state

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

# "unavailable" = path-absent / couldn't run; "n/a" = ran but not applicable here (a hub
# no-op: no docs/handoffs/, no section 3.1, no floor). Both surface as "N/A" in the report
# table -- distinguished by the evidence text and the separate per-status tallies below.
_STATUS_EMOJI = {"pass": "✓", "fail": "✗", "warn": "!", "unavailable": "?", "n/a": "-"}
_STATUS_LABEL = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "unavailable": "N/A", "n/a": "N/A"}


def generate_report(states: list[RepoState], run_date: date, repo_root: Path) -> str:
    ts = datetime.now().isoformat(timespec="seconds")
    total_checks = sum(len(s.findings) for s in states)
    passed = sum(1 for s in states for f in s.findings if f.status == "pass")
    failed = sum(1 for s in states for f in s.findings if f.status == "fail")
    warned = sum(1 for s in states for f in s.findings if f.status == "warn")
    unavailable = sum(1 for s in states for f in s.findings if f.status == "unavailable")
    n_a = sum(1 for s in states for f in s.findings if f.status == "n/a")

    lines = [
        "# Ecosystem Audit Report\n",
        "\n",
        "<!-- scope: meta -->\n",
        "\n",
        f"**Date:** {run_date.isoformat()}  \n",
        f"**Generated:** {ts}  \n",
        f"**Repos audited:** {len(states)}  \n",
        f"**Checks:** {total_checks} total — {passed} pass, {failed} fail, {warned} warn, {unavailable} unavailable, {n_a} n/a\n",
        "\n",
        "---\n",
        "\n",
    ]

    for state in states:
        repo_fail = any(f.status == "fail" for f in state.findings)
        repo_unavail = any(f.status == "unavailable" for f in state.findings)
        summary_status = "UNAVAILABLE" if repo_unavail else ("FAIL" if repo_fail else "PASS")
        lines.append(f"## {state.name} — {summary_status}\n\n")
        lines.append(f"**Path:** `{state.path}`  \n")
        lines.append(f"**Last audit:** {state.last_audit}\n\n")
        lines.append("| Check | Status | Evidence |\n")
        lines.append("|---|---|---|\n")
        for f in state.findings:
            label = _STATUS_LABEL.get(f.status, f.status.upper())
            lines.append(f"| `{f.check_name}` | {label} | {f.evidence} |\n")
        history_rel = Path("ecosystem") / state.name / "history"
        lines.append(f"\nHistory: [`{history_rel}/`]({history_rel}/)\n\n")
        lines.append("---\n\n")

    lines.append("## Summary\n\n")
    lines.append(f"- {len(states)} repo(s) audited\n")
    lines.append(f"- {passed}/{total_checks} checks passed\n")
    if failed:
        lines.append(f"- **{failed} failure(s)** — route findings to repo owners\n")
    if warned:
        lines.append(f"- {warned} warning(s)\n")
    if unavailable:
        lines.append(f"- {unavailable} unavailable (path not found)\n")
    if n_a:
        lines.append(f"- {n_a} n/a (check not applicable to that repo)\n")
    lines.append("\n*Report generated by `scripts/audit.py`. Do not edit manually.*\n")

    return "".join(lines)


def write_report(content: str, run_date: date, single_repo: Optional[str] = None) -> Path:
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    if single_repo:
        filename = f"{run_date.isoformat()}-{single_repo}-audit.md"
    else:
        filename = f"{run_date.isoformat()}-ecosystem-audit.md"
    out = AUDITS_DIR / filename
    out.write_text(content, encoding="utf-8")
    return out

# ---------------------------------------------------------------------------
# ecosystem-index regeneration
# ---------------------------------------------------------------------------

def regenerate_index(states: list[RepoState]) -> None:
    """Write the derived ecosystem/index.yaml rollup from the given repo states.

    Shape: `{generated: <ISO timestamp>, repos: [<RepoState.to_dict()>, ...]}` — an
    aggregate snapshot of every registered repo's last audit, for a one-file read of
    ecosystem health. Derived and regenerated wholesale by `registry update`; do not
    edit by hand (manual edits are lost on the next run). The per-repo state.yaml
    files are the source of truth — the index is always rebuildable from them.
    """
    index = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "repos": [s.to_dict() for s in states],
    }
    ECOSYSTEM_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(ECOSYSTEM_INDEX, "w", encoding="utf-8") as fh:
        yaml.dump(index, fh, default_flow_style=False, allow_unicode=True)

# ---------------------------------------------------------------------------
# ADR-84 (Q9) writer commit — isolate durable outputs to automation/fleet-audit
# ---------------------------------------------------------------------------

_AUTOMATION_BRANCH = "automation/fleet-audit"


def _parse_porcelain(raw: str) -> list:
    """Parse `git status --porcelain` lines into [(xy, path), ...]. Pure.

    `xy` is the two-char status field; `path` is repo-relative. Durable output
    paths never rename, so the simple `XY<space>PATH` split suffices.
    """
    out = []
    for line in raw.splitlines():
        if len(line) < 4:
            continue
        out.append((line[:2], line[3:].strip().strip('"')))
    return out


def _restore_durable_scope(pathspecs: list) -> None:
    """Return the working tree to HEAD within the durable output paths.

    Crash-safe cleanup (called from a `finally`): RE-DERIVES the dirty state in
    the durable scope itself (so it runs correctly however the caller exited —
    a failed pre-commit snapshot, a mid-plumbing crash, or success), then removes
    NEW untracked outputs and restores MODIFIED tracked files from HEAD. Only
    paths git reports dirty IN SCOPE are touched — never arbitrary files.
    Best-effort: a git-status or per-path failure is logged, never raised.
    """
    st = subprocess.run(
        ["git", "-C", _REPO_ROOT, "status", "--porcelain", "--untracked-files=all", "--", *pathspecs],
        capture_output=True, text=True,
    )
    if st.returncode != 0:
        logger.warning("ADR-84 restore: git status failed — durable scope NOT cleaned (%s)",
                       st.stderr.strip())
        return
    changed = _parse_porcelain(st.stdout)
    untracked = [p for (xy, p) in changed if xy == "??"]
    tracked = [p for (xy, p) in changed if xy != "??"]
    for p in untracked:
        fp = Path(_REPO_ROOT) / p
        try:
            if fp.is_file():
                fp.unlink()
        except OSError as exc:
            logger.warning("ADR-84 restore: could not remove %s — %s", p, exc)
    if tracked:
        subprocess.run(
            ["git", "-C", _REPO_ROOT, "checkout", "HEAD", "--", *tracked],
            capture_output=True, text=True,
        )


def _commit_routine_outputs(run_date: date) -> None:
    """Capture this run's durable audit outputs onto the `automation/fleet-audit`
    branch via git plumbing — never to `main` (ADR-84 / Q9 writer isolation).

    `cmd_run` writes the durable outputs (docs/audits/, ecosystem/<name>/history/)
    into the main working tree; this records their current state onto the orphan,
    output-only `automation/fleet-audit` branch using a SEPARATE index
    (`GIT_INDEX_FILE`) + `commit-tree` plumbing, so main's HEAD / index / working
    tree are never touched and no pre-commit hook fires. The working tree is then
    restored so the just-written outputs do not dirty `main` (the baseline has no
    readers — the live copy lives on the branch). The branch is created
    (parent-less root) on first run. `state.yaml` is gitignored, never staged,
    and stays.

    Fail-soft + crash-safe: any git error logs a WARN and returns; the
    working-tree restore always runs in a `finally`. Enumerates concrete history/
    paths (no glob — git on Windows does not expand `*` in a subprocess pathspec).
    Assumes the durable scope is clean going in (the automation invariant).
    """
    repo = _REPO_ROOT
    history_specs = (
        [
            (d / "history").relative_to(repo).as_posix()
            for d in sorted(ECOSYSTEM_DIR.iterdir())
            if d.is_dir()
        ]
        if ECOSYSTEM_DIR.exists()
        else []
    )
    pathspecs = history_specs + [AUDITS_DIR.relative_to(repo).as_posix()]

    tmp_index = None
    try:
        # Snapshot durable-scope changes for the branch commit. The early-returns
        # below are INSIDE the try, so the finally always runs the restore — which
        # re-derives the scope itself, cleaning main even if this status call (after
        # cmd_run wrote outputs) fails.
        status = subprocess.run(
            ["git", "-C", repo, "status", "--porcelain", "--untracked-files=all", "--", *pathspecs],
            capture_output=True, text=True,
        )
        if status.returncode != 0:
            logger.warning("ADR-84 commit: git status failed — %s", status.stderr.strip())
            return
        changed = _parse_porcelain(status.stdout)
        if not changed:
            return  # nothing new this run
        # Stage ONLY this run's changed files (not whole dirs): git 2.0+ `git add <dir>`
        # stages deletions, so re-adding dirs against a branch-seeded index would prune
        # prior outputs (which the restore removes from the working tree). Adding the
        # exact changed paths makes the branch ACCUMULATE.
        changed_paths = [p for (_xy, p) in changed]

        fd, tmp_index = tempfile.mkstemp(prefix="q9-fleet-idx-")
        os.close(fd)
        # mkstemp leaves a 0-byte file, which git rejects as a malformed index.
        # Remove it so git writes a fresh, valid index (read-tree on branch-exists,
        # or git add on the orphan first run) at this reserved unique path.
        os.remove(tmp_index)
        env = dict(os.environ, GIT_INDEX_FILE=tmp_index)

        branch_exists = subprocess.run(
            ["git", "-C", repo, "rev-parse", "--verify", "--quiet",
             f"{_AUTOMATION_BRANCH}^{{commit}}"],
            capture_output=True, text=True,
        ).returncode == 0

        # Seed the temp index from the branch tip so the commit accumulates prior
        # outputs (an EMPTY index on first run → an orphan, output-only root).
        if branch_exists:
            rt = subprocess.run(
                ["git", "-C", repo, "read-tree", _AUTOMATION_BRANCH],
                env=env, capture_output=True, text=True,
            )
            if rt.returncode != 0:
                logger.warning("ADR-84 commit: read-tree failed — %s", rt.stderr.strip())
                return

        add = subprocess.run(
            ["git", "-C", repo, "add", "--", *changed_paths],
            env=env, capture_output=True, text=True,
        )
        if add.returncode != 0:
            logger.warning("ADR-84 commit: git add failed — %s", add.stderr.strip())
            return

        wt = subprocess.run(
            ["git", "-C", repo, "write-tree"],
            env=env, capture_output=True, text=True,
        )
        if wt.returncode != 0:
            logger.warning("ADR-84 commit: write-tree failed — %s", wt.stderr.strip())
            return
        tree = wt.stdout.strip()

        parent_args = []
        if branch_exists:
            cur_tree = subprocess.run(
                ["git", "-C", repo, "rev-parse", f"{_AUTOMATION_BRANCH}^{{tree}}"],
                capture_output=True, text=True,
            ).stdout.strip()
            if tree == cur_tree:
                return  # identical tree — nothing new to record
            parent_args = ["-p", _AUTOMATION_BRANCH]

        msg = (
            f"chore(routine/fleet-audit): record {run_date} baseline\n"
            "\n"
            "Routine: fleet-audit"
        )
        ct = subprocess.run(
            ["git", "-C", repo, "commit-tree", tree, *parent_args, "-m", msg],
            capture_output=True, text=True,
        )
        if ct.returncode != 0:
            logger.warning("ADR-84 commit: commit-tree failed — %s", ct.stderr.strip())
            return
        commit = ct.stdout.strip()

        ur = subprocess.run(
            ["git", "-C", repo, "update-ref", f"refs/heads/{_AUTOMATION_BRANCH}", commit],
            capture_output=True, text=True,
        )
        if ur.returncode != 0:
            logger.warning("ADR-84 commit: update-ref failed — %s", ur.stderr.strip())
            return
    except Exception as exc:
        logger.warning("ADR-84 commit: unexpected error — %s", exc)
    finally:
        _restore_durable_scope(pathspecs)
        if tmp_index and os.path.exists(tmp_index):
            try:
                os.remove(tmp_index)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
def cli() -> None:
    """Ecosystem audit tool — reads child repos, writes only to .dev-knowledge."""


@cli.command("run")
@click.option("--repo-path", "repo_path", default=None,
              help="Bootstrap: path to a repo not yet registered. Creates state.yaml on first use.")
def cmd_run(repo_path: Optional[str]) -> None:
    """Run the full ecosystem audit; write a report to docs/audits/.

    Runs ALL_CHECKS against every registered repo, saves each repo's state.yaml,
    appends to ecosystem/<name>/history/YYYY-MM-DD.md, and writes a dated report.
    Exits 1 if any check fails. Cross-repo findings are advisory — remediation is
    manual in the child repo (no downstream commit gating; ARCHITECTURE.md / ADR-36).

    --repo-path bootstraps a not-yet-registered repo: it creates that repo's
    state.yaml and permanently registers it, then runs. It does NOT refresh the
    derived ecosystem/index.yaml — follow with `registry update` for that.

    Examples:
        python scripts/audit.py run
        python scripts/audit.py run --repo-path ../corp-monorepo
    """
    run_date = date.today()

    if repo_path:
        rp = Path(repo_path).resolve()
        repo_name = rp.name
        click.echo(f"Bootstrapping: registering {repo_name} at {rp}")
        # Create/update state.yaml for the new repo, then fall through to full run
        bootstrap_state = RepoState(name=repo_name, path=str(rp),
                                    last_audit=None, findings=[])
        save_state(bootstrap_state)

    names = discover_repos()
    if not names:
        click.echo("No repos registered in ecosystem/. Use --repo-path to register one.", err=True)
        sys.exit(0)
    states = []
    for name in names:
        existing = load_state(name)
        rp = Path(existing.path) if existing else Path(_REPO_ROOT).parent / name
        state = audit_repo(name, rp, run_date)
        save_state(state)
        append_history(state, run_date)
        states.append(state)

    report = generate_report(states, run_date, Path(_REPO_ROOT))
    out = write_report(report, run_date)
    click.echo(f"Report: {out}")
    _commit_routine_outputs(run_date)

    failures = sum(1 for s in states for f in s.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s). See report for details.", err=True)
        sys.exit(1)


@cli.command("repo")
@click.argument("name")
@click.option("--repo-path", "repo_path", default=None,
              help="Override filesystem path (bootstrap or ad-hoc).")
def cmd_repo(name: str, repo_path: Optional[str]) -> None:
    """Audit a single repo by name.

    Same state.yaml / history / report writes as `run`, scoped to one repo; the
    report lands at docs/audits/YYYY-MM-DD-<name>-audit.md. Exits 1 on any failure.
    Pass --repo-path to override the stored path (bootstrap or ad-hoc location).

    Examples:
        python scripts/audit.py repo ai-council
        python scripts/audit.py repo corp-monorepo --repo-path ../corp-monorepo
    """
    run_date = date.today()
    existing = load_state(name)

    if repo_path:
        rp = Path(repo_path).resolve()
    elif existing:
        rp = Path(existing.path)
    else:
        rp = Path(_REPO_ROOT).parent / name
        click.echo(f"No state.yaml for {name}; assuming path {rp}")

    state = audit_repo(name, rp, run_date)
    save_state(state)
    append_history(state, run_date)

    report = generate_report([state], run_date, Path(_REPO_ROOT))
    out = write_report(report, run_date, single_repo=name)
    click.echo(f"Report: {out}")
    _commit_routine_outputs(run_date)

    failures = sum(1 for f in state.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s).", err=True)
        sys.exit(1)


@cli.command("registry")
@click.argument("action", type=click.Choice(["update"]))
def cmd_registry(action: str) -> None:
    """Manage the ecosystem registry. Action: `update`.

    `update` regenerates the derived ecosystem/index.yaml from the current
    ecosystem/<name>/state.yaml files — a pure read-state -> write-index operation:
    it runs no checks, writes no history, and generates no report. Run it after
    registering a repo (e.g. after `run --repo-path`) to keep the rollup current.
    index.yaml is derived; do not edit it by hand (it is overwritten each run).

    Example:
        python scripts/audit.py registry update
    """
    names = discover_repos()
    states = [load_state(n) for n in names if load_state(n) is not None]
    regenerate_index(states)
    click.echo(f"ecosystem/index.yaml regenerated ({len(states)} repos).")


@cli.command("health")
def cmd_health() -> None:
    """Quick TTY status: operational deps + .dev-knowledge self-conformance. No file writes.

    Two parts: (1) operational preflight — click/pyyaml importable, ecosystem/ exists,
    >=1 repo registered; (2) self-audit — the full ALL_CHECKS suite against
    .dev-knowledge itself. A self-audit `fail` (or a failed preflight) prints
    "health: DEGRADED" and exits 1; a `warn` prints but exits 0.

    This is the `audit-health` pre-commit gate ([#69]): a FAIL blocks the commit,
    a WARN only informs. Enforcement is self-only — `health` never reaches child repos.

    Example:
        python scripts/audit.py health
    """
    checks: list[tuple[str, bool, str]] = []

    # (a) click importable
    try:
        import click as _c  # noqa: F401
        checks.append(("click importable", True, ""))
    except ImportError as e:
        checks.append(("click importable", False, str(e)))

    # (b) pyyaml importable
    try:
        import yaml as _y  # noqa: F401
        checks.append(("pyyaml importable", True, ""))
    except ImportError as e:
        checks.append(("pyyaml importable", False, str(e)))

    # (c) ecosystem/ directory exists
    eco_exists = ECOSYSTEM_DIR.exists()
    checks.append(("ecosystem/ exists", eco_exists, "" if eco_exists else str(ECOSYSTEM_DIR)))

    # (d) at least one repo registered
    repos = discover_repos()
    checks.append(("repos registered", len(repos) > 0, f"{repos}" if repos else "none"))

    operational_ok = all(ok for _, ok, _ in checks)

    # Self-conformance: full check suite against .dev-knowledge. Gate mode (#89): the
    # commit gate runs here, so flag it so check_doc_claims skips the expensive claim-3
    # (pytest --collect-only) — that locus is evaluated only on the full-audit path.
    global _GATE_MODE
    self_findings: list[Finding] = []
    _GATE_MODE = True
    try:
        for check in ALL_CHECKS:
            self_findings.extend(check(Path(_REPO_ROOT)))
    finally:
        _GATE_MODE = False
    self_fail = any(f.status == "fail" for f in self_findings)

    click.echo("operational:")
    for label, ok, detail in checks:
        marker = "[OK]" if ok else "[!!]"
        suffix = f"  ({detail})" if detail else ""
        click.echo(f"  {marker} {label}{suffix}")

    passed = sum(1 for f in self_findings if f.status == "pass")
    click.echo(f"self-audit (.dev-knowledge) - {passed}/{len(self_findings)} pass:")
    _marker = {"pass": "[OK]", "warn": "[~~]", "fail": "[!!]", "unavailable": "[??]", "n/a": "[--]"}
    for f in self_findings:
        click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")

    if operational_ok and not self_fail:
        click.echo("health: OK")
    else:
        click.echo("health: DEGRADED", err=True)
        sys.exit(1)


def _load_dispositions() -> list[dict]:
    """Read the #147 known-WARN disposition register. Fail-soft: a missing or malformed
    register degrades to [] — every WARN then counts as undispositioned (stricter), and
    the gate never wedges. Read-only."""
    try:
        data = yaml.safe_load(Path(DISPOSITION_REGISTER).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    if not isinstance(data, dict):
        return []
    items = data.get("dispositions")
    if not isinstance(items, list):  # HIGH (Codex): a non-list scalar must degrade, not raise
        return []
    return [d for d in items if isinstance(d, dict)]


def _match_disposition(finding: "Finding", dispositions: list[dict]) -> Optional[dict]:
    """Return the register entry that dispositions this WARN finding, or None.

    A match requires `organ == finding.check_name` AND the entry's `match` substring to
    appear in `finding.evidence` — keying on the specific benign signature (e.g. the
    commit sha), NOT a bare id, so a DIFFERENT future drift on the same id re-surfaces.
    """
    for d in dispositions:
        token = d.get("match")
        if d.get("organ") == finding.check_name and token and str(token) in finding.evidence:
            return d
    return None


# [#337] the INFORMATIONAL fleet-parity subprocess surface (`_fleet_parity_surface` /
# `_FLEET_PARITY_SCRIPT`) was RETIRED when fleet_parity became a blocking ALL_CHECKS member
# (`check_fleet_parity` above) -- the gate now reads the in-process walk, not an echoed subprocess.


@cli.command("ship-gate")
def cmd_ship_gate() -> None:
    """Pre-ship verification-organ gate (#147): make "Definition of shipped" point (6)
    enforceable at /ship time. No file writes (read-only, Layer-2).

    Runs the full ALL_CHECKS self-audit against .dev-knowledge and emits ONE ship verdict
    by reading Finding.status DIRECTLY — never exit codes: the awareness organs
    (git_backlog_drift #90a, doc_claims #89, canonical_freshness A1) exit 0 even on drift,
    so a gate keyed on exit codes would be vacuous (F1). Verdict / exit:
      - any Finding.status == "fail"                         -> RED, exit 1
      - any "warn" NOT dispositioned by the register         -> RED, exit 1
      - a "warn" matched by a register entry (organ == check_name AND the entry's `match`
        substring in the evidence) is DISPOSITIONED           -> does not block
      - else                                                 -> GREEN, exit 0
    A register entry that matched NO live WARN is surfaced as `[stale]` (ADR-75 decoration
    rule — awareness, does NOT block); the register may not silently rot.

    Disposition contract: a register entry suppresses a WHOLE Finding (its `match` is a
    substring of the evidence). So an aggregate awareness organ MUST emit one Finding per
    concern, or one matched token would suppress unrelated drift bundled in the same
    finding (Codex CRITICAL 2026-06-10). `git_backlog_drift` emits one Finding per drifted
    id for exactly this reason; any future dispositioned organ must do likewise.

    Seam vs the pre-commit `audit-health` gate (they reuse ALL_CHECKS but do NOT
    double-run vacuously — different moment, different posture):
      - `audit-health` gates each COMMIT: FAIL-only (WARNs pass), gate-mode SKIPS the
        expensive claim-3 (pytest --collect-only) to stay fast.
      - `ship-gate` gates the feature ARC at /ship: FAIL **and** new/undispositioned WARN
        block, and it runs claim-3 (full verification — _GATE_MODE stays False).

    Hub-only organs no-op on child repos; the /ship wiring is hub-guarded. Register:
    ecosystem/disposition-register.yaml (fail-soft if absent — stricter, never wedged).

    Example:
        python scripts/audit.py ship-gate
    """
    global _GATE_MODE
    findings: list[Finding] = []
    _GATE_MODE = False  # ship-time = full verification (run the expensive claim-3)
    try:
        for check in ALL_CHECKS:
            findings.extend(check(Path(_REPO_ROOT)))
    finally:
        _GATE_MODE = False

    dispositions = _load_dispositions()
    fails = [f for f in findings if f.status == "fail"]
    undispositioned: list[Finding] = []
    dispositioned: list[tuple[Finding, dict]] = []
    matched_ids: set[str] = set()
    for f in findings:
        if f.status != "warn":
            continue
        entry = _match_disposition(f, dispositions)
        if entry is None:
            undispositioned.append(f)
        else:
            dispositioned.append((f, entry))
            matched_ids.add(str(entry.get("id")))
    stale = [d for d in dispositions if str(d.get("id")) not in matched_ids]

    _marker = {"pass": "[OK]", "warn": "[~~]", "fail": "[!!]", "unavailable": "[??]", "n/a": "[--]"}
    click.echo("ship-gate (#147) — verification organs vs THIS arc:")
    for f in findings:
        click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")
    for f, e in dispositioned:
        click.echo(f"  [disp] {f.check_name}: WARN dispositioned by {e.get('id')} "
                   f"(ref {e.get('ref')}) — expected, not blocking")
    for d in stale:
        click.echo(f"  [stale] disposition {d.get('id')} matched no live WARN — "
                   f"review/remove (ADR-75 decoration rule)")

    # [#337] fleet_parity is now a blocking ALL_CHECKS member (check_fleet_parity); its
    # Findings render inline in the loop above and gate via the normal fails/undispositioned
    # path below -- no separate informational echo.
    if fails or undispositioned:
        reasons = []
        if fails:
            reasons.append(f"{len(fails)} hard-fail organ(s)")
        if undispositioned:
            reasons.append(f"{len(undispositioned)} new/undispositioned WARN(s)")
        click.echo(f"ship-gate: RED — not shipped-ready ({'; '.join(reasons)})", err=True)
        sys.exit(1)
    click.echo("ship-gate: GREEN — verification organs green against this arc "
               f"({len(dispositioned)} WARN dispositioned)")


@cli.command("checks")
def cmd_checks() -> None:
    """List the registered audit checks (sourced from ALL_CHECKS — the same list
    that `health` and `run` execute).

    Authoritative, drift-proof inventory: the count and numbering come from
    ALL_CHECKS at runtime, so this listing cannot diverge from what actually runs.
    Each line shows the check's name (== its Finding.check_name) and the first line
    of its docstring.

    Example:
        python scripts/audit.py checks
    """
    click.echo(f"{len(ALL_CHECKS)} registered checks (ALL_CHECKS — run by `health` and `run`):")
    for i, check in enumerate(ALL_CHECKS, start=1):
        name = check.__name__.removeprefix("check_")  # == Finding.check_name
        first = (check.__doc__ or "").strip().splitlines()
        summary = first[0].strip() if first else ""
        click.echo(f"  {i:>2}. {name} — {summary}")


if __name__ == "__main__":
    cli()
