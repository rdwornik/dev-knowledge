"""
audit.py — Ecosystem audit tool per ADR-36.

Reads child repos under Dev/ and writes only to .dev-knowledge paths.
Read-only contract: never touches child repo files (hard constraint, ADR-36).

This module is self-documenting: `python scripts/audit.py --help` and
`python scripts/audit.py <cmd> --help` are the authoritative CLI reference. The
conceptual / authority model — what this tool is, why the cross-repo `run` is
advisory while the self-audit `health` gates commits, and the self-only
enforcement model — lives in ARCHITECTURE.md (§"Validators and enforcement",
§"Authority and governance") and ADR-36. Do not re-narrate that here.

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
import subprocess
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
_FRESHNESS_FILES = ["VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md"]

# Calendar-age backstop (A1): WARN — not FAIL — when last_reviewed exceeds this many
# days even if the file has not changed. A loose nudge toward periodic re-reading; the
# load-bearing signal is A2 (edited-since-review), which is the FAIL.
_FRESHNESS_CADENCE_DAYS = 30

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
    """Check #2: ADR-38 (amendments A5 2026-05-23, A6 2026-06-02) universal governance baseline.

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


def check_mermaid_theme_directive(repo_path: Path) -> list[Finding]:
    """Check #7 (ADR-51 v2): Mermaid blocks use base+themeVariables; classDef fill has color.

    Scanned: ARCHITECTURE.md + templates/ARCHITECTURE-template.md.
    Excluded (immutable dated artifacts per ADR-39): docs/audits/, docs/decisions/ADR-*,
    JOURNAL.md, docs/archive/.
    """
    _SCANNED_PATHS = [
        repo_path / "ARCHITECTURE.md",
        repo_path / "templates" / "ARCHITECTURE-template.md",
    ]

    violations: list[str] = []

    for file_path in _SCANNED_PATHS:
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = file_path.relative_to(repo_path)

        in_fence = False
        fence_start_line = 0
        block_lines: list[tuple[int, str]] = []  # (1-based line number, content)

        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not in_fence:
                if stripped.startswith("```mermaid"):
                    in_fence = True
                    fence_start_line = i
                    block_lines = []
            else:
                if stripped.startswith("```"):
                    # End of fence — evaluate this block
                    non_empty = [(ln, ln_text) for ln, ln_text in block_lines if ln_text.strip()]
                    if non_empty:
                        first_ln, first_content = non_empty[0]
                        fc = first_content.strip()
                        if not (re.search(r"'theme'\s*:\s*'base'", fc)
                                and re.search(r"'themeVariables'\s*:", fc)):
                            violations.append(
                                f"{rel}:{first_ln}: mermaid block missing base+themeVariables "
                                f"directive (first non-empty line: {fc[:80]!r})"
                            )
                    else:
                        violations.append(
                            f"{rel}:{fence_start_line}: empty mermaid block (no content)"
                        )

                    # Check every classDef line in the block
                    for ln, content in block_lines:
                        cs = content.strip()
                        if re.search(r"\bclassDef\b", cs) and re.search(r"\bfill:#", cs):
                            if not re.search(r"\bcolor:#", cs):
                                violations.append(
                                    f"{rel}:{ln}: classDef has fill:# but no color:# — "
                                    f"{cs[:100]!r}"
                                )

                    in_fence = False
                    block_lines = []
                else:
                    block_lines.append((i, line))

    if violations:
        evidence = f"{len(violations)} violation(s): " + "; ".join(violations[:3])
        if len(violations) > 3:
            evidence += f" … (+{len(violations) - 3} more)"
        return [Finding("mermaid_theme_directive", "fail", evidence)]
    return [Finding("mermaid_theme_directive", "pass",
                    "All mermaid blocks use base+themeVariables; all classDef fill: have color:")]


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
    """Check #8 (HANDOFF_PROCESS v4.3 item F): v4 handoff bundle structure validator.

    Scans docs/handoffs/<slug>/ and validates only STAMPED v4 bundles — those whose
    README.md carries the `Generated by HANDOFF_PROCESS v4.x (status: beta|stable)`
    stamp. Pre-stamp bundles (the v4.1 first-run) and v3.x sync bundles predate the
    contract and are out of scope (preserved historical evidence). The four-tag
    section is required only for v4.3+ bundles.

    Per stamped bundle: 8 files present (README + 01–07); README carries a
    `## Drift cross-check` section; 04_RECENT carries `## Load-bearing facts` (and,
    for v4.3+, `## Four-tag discipline (canonical)`); per-file line budgets respected.
    Excludes aborted/, in-progress/, archive/. Read-only (ADR-28/36).
    """
    handoffs = repo_path / "docs" / "handoffs"
    if not handoffs.exists():
        return [Finding("handoff_bundle_structure", "pass",
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
    """Check #9 (HANDOFF_PROCESS v4.3 item F): §3.1 tag-canonicity lint.

    Scans protocols/HANDOFF_PROCESS.md §3.1 ONLY (not the end-of-file amendments).
    §3.1 must EITHER enumerate all four canonical tags (witnessed/recall/inferred/
    unknown — the post-v5 consolidated state) OR carry a cross-reference to
    Amendment A (the four-tag canonical). A three-tag §3.1 with no cross-reference is
    the drift this check exists to catch (closes C3 durably). Read-only.
    """
    spec = repo_path / "protocols" / "HANDOFF_PROCESS.md"
    if not spec.exists():
        return [Finding("handoff_tag_canonicity", "pass",
                        "no protocols/HANDOFF_PROCESS.md — nothing to validate")]

    lines = spec.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines) if re.match(r"^###\s+3\.1\b", ln)), None)
    if start is None:
        return [Finding("handoff_tag_canonicity", "pass",
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


def _parse_last_reviewed(text: str) -> Optional[date]:
    """Extract `last_reviewed` from a file's YAML frontmatter, or None if absent.

    Returns None when the file has no frontmatter, the frontmatter is unclosed or not a
    mapping, the key is missing, or its value is not a parseable ISO date. YAML parses an
    unquoted ISO date to a date (or datetime); quoted/string forms are parsed explicitly.
    """
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    val = fm.get("last_reviewed")
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val.strip())
        except ValueError:
            return None
    return None


def _git_last_commit_date(repo_path: Path, filename: str) -> Optional[date]:
    """Author date (short ISO) of the most recent commit touching `filename`.

    Uses author date (`%as`), not committer date (`%cs`): author date is preserved across
    rebase / cherry-pick / amend, so A2 keys off when the content was actually edited rather
    than when history was last rewritten (avoids spurious staleness FAILs after a rebase).

    Read-only (`git log`). Returns None when git is absent, the path is not a git repo, or
    the file has no commit history — callers then skip the A2 signal and fall back to the A1
    calendar backstop, so a non-git consumer degrades gracefully rather than erroring.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%as", "--", filename],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    out = result.stdout.strip()
    if result.returncode != 0 or not out:
        return None
    try:
        return date.fromisoformat(out)
    except ValueError:
        return None


def check_canonical_freshness(repo_path: Path) -> list[Finding]:
    """Check #10: canonical living-file freshness cadence (operationalizes ADR-39 grooming).

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
    """
    fails: list[str] = []
    warns: list[str] = []
    today = date.today()

    for fname in _FRESHNESS_FILES:
        fpath = repo_path / fname
        if not fpath.exists():
            continue  # presence enforced by checks #1/#3/#5 — don't double-report
        reviewed = _parse_last_reviewed(fpath.read_text(encoding="utf-8"))
        if reviewed is None:
            warns.append(f"{fname}: no parseable last_reviewed frontmatter")
            continue
        git_date = _git_last_commit_date(repo_path, fname)
        if git_date is not None and reviewed < git_date:
            fails.append(
                f"{fname}: last_reviewed {reviewed.isoformat()} predates last edit "
                f"{git_date.isoformat()} - edited but not re-reviewed")
            continue  # A2 dominates; don't also calendar-warn a file already failing
        age = (today - reviewed).days
        if age > _FRESHNESS_CADENCE_DAYS:
            warns.append(
                f"{fname}: last_reviewed {reviewed.isoformat()} is {age}d old "
                f"(> {_FRESHNESS_CADENCE_DAYS}d cadence)")

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
    """Check #11 (no-leftovers invariant — ADR-61/ADR-68, PLAYBOOK G5): no orphaned
    `<repo>-*` sibling directories left behind by a torn-down worktree.

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
    the mechanization PLAYBOOK G5 §924 named.

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
    """Check #12 (ADR-38 A6): each present canonical file carries its [U] heading spine.

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


ALL_CHECKS = [
    check_vision_md,
    check_adr38_baseline,
    check_claude_md,
    check_dot_prefix_discipline,
    check_canonical_md_visibility,
    check_workspace_settings,
    check_mermaid_theme_directive,
    check_handoff_bundle_structure,
    check_handoff_tag_canonicity,
    check_canonical_freshness,
    check_no_sibling_orphans,
    check_canonical_structure,
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
