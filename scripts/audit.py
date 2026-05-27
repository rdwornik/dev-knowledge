"""
audit.py — Ecosystem audit tool per ADR-36.

Reads child repos under Dev/ and writes only to .dev-knowledge paths.
Read-only contract: never touches child repo files.

Commands:
    audit run                          # full ecosystem; writes report
    audit repo <name>                  # single repo
    audit registry update              # regenerate ecosystem/index.yaml
    audit health                       # quick TTY status, no file writes

Usage:
    python scripts/audit.py run
    python scripts/audit.py run --repo-path ../ai-council
    python scripts/audit.py repo ai-council
    python scripts/audit.py health
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import click
import yaml

# Resolve repo root (scripts/ sibling) — after imports
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("audit")

ECOSYSTEM_DIR = Path(_REPO_ROOT) / "ecosystem"
AUDITS_DIR = Path(_REPO_ROOT) / "docs" / "audits"
ECOSYSTEM_INDEX = Path(_REPO_ROOT) / "ecosystem" / "index.yaml"

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
    "requirements.txt",     # pip convention
    "requirements-dev.txt",
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "tach.toml",            # verified 2026-05-27: tach 0.34.0 does not read .tach.toml
    "README.md",            # deprecated from baseline; if present, no dot
}

# Canonical files universally mandatory at repo root (ADR-38 A5 / ADR-51).
_CANONICAL_MANDATORY = ["VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "BACKLOG.md"]

# All canonical names whose casing is checked when present (mandatory + optional
# + .dev-knowledge-only). Presence is required only for _CANONICAL_MANDATORY.
_CANONICAL_ALL = _CANONICAL_MANDATORY + [
    "JOURNAL.md", "ENVIRONMENT.md", "CONTRIBUTING.md",
    "ESSENTIALS.md", "PLAYBOOK.md", "LESSONS.md", "TOKEN-LOG.md", "README.md",
]

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
    check_name: str
    status: str          # "pass" | "fail" | "warn" | "unavailable"
    evidence: str

@dataclass
class RepoState:
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
    """Check #1: VISION.md presence + parseable YAML frontmatter per ADR-33."""
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
    """Check #2: ADR-38 (amendment A5, 2026-05-23) universal governance baseline.

    Checks the governance documents every repo must carry — not code structure.
    The repo-tier system is deprecated, so there is no per-tier branching. Code
    layout (src/, tests/, pyproject.toml) is scoped to code projects per the
    amendment and is NOT part of this universal governance check (governance-only
    repos such as .dev-knowledge have no src/ or pyproject.toml). README.md is
    optional (deprecated from the baseline); CHANGELOG.md was removed by ADR-49.
    CLAUDE.md is covered by check_claude_md.
    """
    required_files = ["VISION.md", "ARCHITECTURE.md", "BACKLOG.md"]

    missing_files = [f for f in required_files if not (repo_path / f).exists()]

    if missing_files:
        status = "fail"
        evidence = f"Missing required: {missing_files}"
    else:
        status = "pass"
        evidence = "All ADR-38 universal governance baseline files present"
    return [Finding("adr38_baseline", status, evidence)]


def check_claude_md(repo_path: Path) -> list[Finding]:
    """Check #3: ADR-31 CLAUDE.md presence and non-empty per authority model baseline."""
    claude = repo_path / "CLAUDE.md"
    if not claude.exists():
        return [Finding("claude_md", "fail", "CLAUDE.md absent at repo root")]
    content = claude.read_text(encoding="utf-8").strip()
    if not content:
        return [Finding("claude_md", "fail", "CLAUDE.md exists but is empty")]
    return [Finding("claude_md", "pass", f"CLAUDE.md present ({len(content)} chars)")]


def check_dot_prefix_discipline(repo_path: Path) -> list[Finding]:
    """Check #4 (ADR-59 D1): root config files dot-prefixed unless on exception list.

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
    """Check #5 (ADR-59 D2): mandatory canonical files present + correct ALL-CAPS casing.

    Requires only the four universal files (ADR-38 A5 / ADR-51). Optional and
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
    """Check #6 (ADR-59 D3): dot-prefixed .code-workspace carrying required sort settings.

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


ALL_CHECKS = [
    check_vision_md,
    check_adr38_baseline,
    check_claude_md,
    check_dot_prefix_discipline,
    check_canonical_md_visibility,
    check_workspace_settings,
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

_STATUS_EMOJI = {"pass": "✓", "fail": "✗", "warn": "!", "unavailable": "?"}
_STATUS_LABEL = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "unavailable": "N/A"}


def generate_report(states: list[RepoState], run_date: date, repo_root: Path) -> str:
    ts = datetime.now().isoformat(timespec="seconds")
    total_checks = sum(len(s.findings) for s in states)
    passed = sum(1 for s in states for f in s.findings if f.status == "pass")
    failed = sum(1 for s in states for f in s.findings if f.status == "fail")
    warned = sum(1 for s in states for f in s.findings if f.status == "warn")
    unavailable = sum(1 for s in states for f in s.findings if f.status == "unavailable")

    lines = [
        "# Ecosystem Audit Report\n",
        "\n",
        "<!-- scope: meta -->\n",
        "\n",
        f"**Date:** {run_date.isoformat()}  \n",
        f"**Generated:** {ts}  \n",
        f"**Repos audited:** {len(states)}  \n",
        f"**Checks:** {total_checks} total — {passed} pass, {failed} fail, {warned} warn, {unavailable} unavailable\n",
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
    index = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "repos": [s.to_dict() for s in states],
    }
    ECOSYSTEM_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(ECOSYSTEM_INDEX, "w", encoding="utf-8") as fh:
        yaml.dump(index, fh, default_flow_style=False, allow_unicode=True)

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
    """Run full ecosystem audit; write report to docs/audits/."""
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

    failures = sum(1 for s in states for f in s.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s). See report for details.", err=True)
        sys.exit(1)


@cli.command("repo")
@click.argument("name")
@click.option("--repo-path", "repo_path", default=None,
              help="Override filesystem path (bootstrap or ad-hoc).")
def cmd_repo(name: str, repo_path: Optional[str]) -> None:
    """Audit a single repo by name."""
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

    failures = sum(1 for f in state.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s).", err=True)
        sys.exit(1)


@cli.command("registry")
@click.argument("action", type=click.Choice(["update"]))
def cmd_registry(action: str) -> None:
    """Manage ecosystem registry. Action: update (regenerate ecosystem/index.yaml)."""
    names = discover_repos()
    states = [load_state(n) for n in names if load_state(n) is not None]
    regenerate_index(states)
    click.echo(f"ecosystem/index.yaml regenerated ({len(states)} repos).")


@cli.command("health")
def cmd_health() -> None:
    """Quick TTY status: operational deps + .dev-knowledge self-conformance.

    Self-conformance runs the full per-repo check suite (ALL_CHECKS, incl. the
    ADR-59 visual-pattern checks) against .dev-knowledge itself. A self-audit
    `fail` degrades health; a `warn` does not.
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

    # Self-conformance: full check suite against .dev-knowledge.
    self_findings: list[Finding] = []
    for check in ALL_CHECKS:
        self_findings.extend(check(Path(_REPO_ROOT)))
    self_fail = any(f.status == "fail" for f in self_findings)

    click.echo("operational:")
    for label, ok, detail in checks:
        marker = "[OK]" if ok else "[!!]"
        suffix = f"  ({detail})" if detail else ""
        click.echo(f"  {marker} {label}{suffix}")

    passed = sum(1 for f in self_findings if f.status == "pass")
    click.echo(f"self-audit (.dev-knowledge) - {passed}/{len(self_findings)} pass:")
    _marker = {"pass": "[OK]", "warn": "[~~]", "fail": "[!!]", "unavailable": "[??]"}
    for f in self_findings:
        click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")

    if operational_ok and not self_fail:
        click.echo("health: OK")
    else:
        click.echo("health: DEGRADED", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
