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
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

import click
import yaml

# Resolve repo root (scripts/ sibling) — after imports
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)

# Hub identity, decided in ONE place. `_REPO_ROOT` is derived live from __file__ so it always
# names THIS checkout; the `path` in ecosystem/<name>/state.yaml is absolute and committed, so
# it names the checkout that registered the repo. When the two disagree — a worktree, a cloud
# clone, a relocated repo — the hub resolved as not-the-hub and every hub-only check skipped
# silently ([#465] legs 2+3: the 2026-07-21 daily fell 16 WARNs → 2, the missing 14 being
# exactly the three hub-only checks). The comparison lives here and nowhere else so a new
# check cannot gate slightly differently; `resolve_repo_path` keeps the inputs honest.
HUB_REPO_NAME = ".dev-knowledge"


def _is_hub(repo_path) -> bool:
    """True when `repo_path` is the hub tree this audit.py belongs to."""
    try:
        return Path(repo_path).resolve() == Path(_REPO_ROOT).resolve()
    except OSError:  # an unresolvable path is never the hub; never wedge a check
        return False

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

# [#446] A10 item 2 / R4 — the boot byte budget lives ONCE, in the assembler that also warns
# on it; this check reads the constant rather than re-declaring the number. Same shape.
try:
    from scripts import assemble_paste as _assemble_paste
except ImportError:
    import assemble_paste as _assemble_paste

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

# ARC-5 residual-completeness gate — refuses a bundle shipping a hand-authored FILL-IN region
# still carrying its generator placeholder; same module-import + thin-adapter shape; tests
# monkeypatch `_vrc.find_unfilled`.
try:
    from scripts import validate_residual_completeness as _vrc
except ImportError:
    import validate_residual_completeness as _vrc

# [#436] silent-rule ratchet detector — the PINNED definition of the metric (regex + file
# filter + detector id). Same module-import + thin-adapter shape; the check is an adapter
# so the detector contract stays independently testable.
try:
    from scripts import silent_rule_detector as _srd
except ImportError:
    import silent_rule_detector as _srd

# [#433]/C1 derived-tree coherence gate — the `tasks/` emitter, imported so the check can
# invoke its `--check` semantics in-process rather than shelling out. Same shape.
try:
    from scripts import gen_task_tree as _gtt
except ImportError:
    import gen_task_tree as _gtt

# [#383] wave-1 — the docs/intake/ residue-carrier gate (ADR-109 §4's generality proof).
# Same module-import + thin-adapter shape as the `tasks/` gate above.
try:
    from scripts import gen_intake_tree as _gint
except ImportError:
    import gen_intake_tree as _gint

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


# --- [#465] leg 4, FR-1: why an n/a is an n/a -------------------------------
# A dead check and a correctly-skipped one both rendered as the bare token "n/a", so they were
# indistinguishable in every daily -- which is how `handoff_tag_canonicity` emitted a verdict
# for two spec generations after its subject stopped existing, unnoticed.
#
# The reason rides a parsable PREFIX inside the existing `evidence` string. That is deliberate
# and it is what keeps tripwire T1 from firing: `Finding` keeps exactly three fields and the
# five-value status enum, so the LOCKED coherence-spine contract and the daily's column grammar
# are untouched, and `test_finding_format_is_locked` still passes.
#
#   SUBJECT-ABSENT  the governed thing does not exist ANYWHERE -- the check can never fire
#   NOT-APPLICABLE  this repo legitimately lacks the surface; another repo has it
_NA_SUBJECT_ABSENT = "SUBJECT-ABSENT"
_NA_NOT_APPLICABLE = "NOT-APPLICABLE"
_NA_REASONS = (_NA_SUBJECT_ABSENT, _NA_NOT_APPLICABLE)
_NA_REASON_RE = re.compile(rf"^\[n/a-reason:({'|'.join(_NA_REASONS)})\] (.+)$", re.DOTALL)


def _na(check_name: str, reason: str, evidence: str) -> Finding:
    """An n/a Finding carrying a machine-readable reason. Raises on an unknown reason --
    a mis-typed reason must not silently become an unclassifiable n/a."""
    if reason not in _NA_REASONS:
        raise ValueError(f"unknown n/a reason: {reason!r}")
    return Finding(check_name, "n/a", f"[n/a-reason:{reason}] {evidence}".replace("|", "/"))


def _na_reason(finding: Finding) -> str | None:
    """The encoded reason, or None for a non-n/a finding OR an unclassified one.

    None is meaningful, not an error value: the detector treats an unclassified n/a as a loud
    WARN rather than assuming either reason (FR-3 -- never pass silently)."""
    if finding.status != "n/a":
        return None
    m = _NA_REASON_RE.match(finding.evidence)
    return m.group(1) if m else None

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
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(state.to_dict(), fh, default_flow_style=False, allow_unicode=True)


_HISTORY_ROW_RE = re.compile(r"^\|\s*([a-z0-9_]+)\s*\|")


def _previously_reported_checks(repo_name: str, upto: date) -> set[str]:
    """Check names in the single most recent history READING at or before `upto`.

    Two details are load-bearing (terra HIGH, 2026-08-04):

    * SAME-DAY entries count. An earlier version compared strictly against an EARLIER DATE, so
      a second `run` on the same day compared against yesterday and re-emitted a retirement
      notice the first run had already recorded — writing a false "retired since the previous
      reading" into the durable history on every rerun.
    * Only the LAST table in that file is parsed. A history file accumulates appended readings,
      so unioning all of them would resurrect names retired several readings ago and suppress
      the notice for a check that vanished today.

    Derived from the history files themselves — there is deliberately no retired-check registry
    to maintain (FR-4). Empty when there is no prior reading, so a repo's first ever run
    correctly reports nothing retired rather than everything.
    """
    hist = ECOSYSTEM_DIR / repo_name / "history"
    if not hist.is_dir():
        return set()
    prior = sorted(p for p in hist.glob("*.md") if p.stem <= upto.isoformat())
    if not prior:
        return set()
    text = prior[-1].read_text(encoding="utf-8", errors="replace")
    last_reading = text.rsplit("\n## ", 1)[-1]
    names = {m.group(1) for m in (_HISTORY_ROW_RE.match(ln)
                                  for ln in last_reading.splitlines()) if m}
    # An UNAVAILABLE repo's reading is a single `availability` row, and an aborted append can
    # leave a partial table. Neither is a complete reading, and treating one as complete would
    # announce every check the repo normally runs as "retired" in the next daily -- a false
    # entry written into the durable history (terra HIGH r2, 2026-08-04). None means "cannot
    # compare", which the caller renders as an explicit unavailable notice rather than silence.
    if not names or names == {"availability"}:
        return None
    return names


def append_history(state: RepoState, run_date: date) -> None:
    p = _history_path(state.name, run_date)
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    lines = [f"## {run_date.isoformat()} — {ts}\n\n"]

    # [#465] leg 4 / FR-5: a retired check must be visible TO A READER OF THE DAILIES, not only
    # in a commit message. Without this, a check simply stops appearing and the row's absence is
    # indistinguishable from a run that never reached it -- the same invisibility that let
    # `handoff_tag_canonicity` emit a verdict for two spec generations after its subject died.
    # Best-effort by design: this is a NOTICE, and a notice must never be able to fail the write
    # of the daily it annotates. It is never silent, though -- a comparison that cannot run says so.
    try:
        previous = _previously_reported_checks(state.name, run_date)
        if previous is None:
            lines.append("> **Retirement comparison unavailable** — the previous reading was "
                         "absent, unavailable, or partial, so a missing row below cannot be "
                         "read as a retirement.\n\n")
        else:
            gone = sorted(previous - {f.check_name for f in state.findings})
            if gone:
                lines.append(f"> **Checks retired since the previous reading:** "
                             f"{', '.join(gone)}. No longer in ALL_CHECKS; their absence below "
                             "is deliberate.\n\n")
    except Exception as exc:  # noqa: BLE001 -- notice only; never blocks the daily
        lines.append(f"> **Retirement comparison unavailable** ({exc!r}) — a missing row below "
                     "cannot be read as a retirement.\n\n")

    lines.append("| Check | Status | Evidence |\n|---|---|---|\n")
    for f in state.findings:
        lines.append(f"| {f.check_name} | {f.status} | {f.evidence} |\n")
    lines.append("\n")
    with open(p, "a", encoding="utf-8") as fh:
        fh.writelines(lines)


def resolve_repo_path(repo_name: str, stored_path: Optional[str]) -> Path:
    """The tree to audit for `repo_name` — the seam where the hub finds itself.

    The hub always audits the tree audit.py lives in, never the absolute path committed to
    its state.yaml: that value is machine- and checkout-specific, so from any other tree the
    hub failed to recognise itself and every hub-only check skipped as `n/a` ([#465]).
    Consumers keep resolving through their stored path — for them it is the only thing that
    says where the repo is.
    """
    if repo_name == HUB_REPO_NAME:
        return Path(_REPO_ROOT)
    if stored_path:
        return Path(stored_path)
    return Path(_REPO_ROOT).parent / repo_name


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
        return [_na("handoff_bundle_structure", "NOT-APPLICABLE",
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
        return [Finding("no_sibling_orphans", "unavailable",
                        "git unavailable or not a repo - sibling-orphan check skipped")]
    prefix = repo_path.name + "-"
    try:
        siblings = sorted(
            p for p in repo_path.parent.iterdir()
            if p.is_dir() and p.name.startswith(prefix))
    except OSError:
        return [Finding("no_sibling_orphans", "unavailable",
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


# [#505] batch hygiene. The horizon is the MECHANIZED WEEKLY PRUNE the intake keeps ("hygiene
# organ — WARN on stale worktrees (mechanized weekly prune stays)", intake #26 Track 1 item 4),
# so 7 is that cadence rather than a taste call. Changing it changes what "stale" means; it is
# named here once so the check and its tests cannot drift to two numbers.
_STALE_WORKTREE_HORIZON_DAYS = 7


def _git_commit_epoch(repo_path: Path, rev: Optional[str]) -> Optional[int]:
    """Committer epoch of `rev`, or None when it cannot be read.

    None is a real answer, not an error code: the caller reports an unreadable date as
    INDETERMINATE rather than defaulting it either way. Defaulting to "now" would hide a stale
    worktree; defaulting to 0 would manufacture one out of a git hiccup.

    Read-only (`git show -s`). Same graceful-degradation contract as its neighbours.
    """
    if not rev:
        return None
    proc = _git(repo_path, "show", "-s", "--format=%ct", rev)
    if proc is None or proc.returncode != 0:
        return None
    try:
        return int(proc.stdout.strip().splitlines()[0])
    except (ValueError, IndexError):
        return None


def _git_linked_worktrees(repo_path: Path) -> Optional[list[dict]]:
    """Every LINKED worktree of `repo_path` — the main one is excluded — carrying the two facts
    staleness needs: whether the directory still exists, and when its checked-out tip was
    committed.

    Distinct from `_git_registered_worktrees` above, which answers a different question (is
    THIS path registered?) and returns a flat path set with no per-worktree detail. Kept as a
    separate reader rather than widening that one, because `check_no_sibling_orphans` depends on
    its exact set semantics.

    `git worktree list --porcelain` reports the MAIN worktree first, always — that ordering is
    the porcelain contract, and it is how the primary is dropped without resolving and comparing
    paths. Prunable/locked annotations are deliberately NOT parsed: they arrived in later git
    versions, so on-disk presence is tested directly and the reader stays version-independent.

    Read-only. Returns None when git is absent or the path is not a git repo, so a non-git
    consumer degrades gracefully (the check is then n/a) — the `_git_registered_worktrees`
    contract.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    records: list[dict] = []
    current: dict = {}
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            if current:
                records.append(current)
            current = {"path": line[len("worktree "):].strip(), "branch": None, "head": None}
        elif not current:
            continue
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):].strip().removeprefix("refs/heads/")
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD "):].strip()
    if current:
        records.append(current)
    out: list[dict] = []
    for rec in records[1:]:      # [0] is the main worktree
        try:
            on_disk = Path(rec["path"]).is_dir()
        except OSError:
            on_disk = False
        out.append({
            "path": rec["path"],
            "branch": rec["branch"],
            "on_disk": on_disk,
            "last_commit_epoch": _git_commit_epoch(repo_path, rec["head"]),
        })
    return out


def check_stale_worktrees(repo_path: Path, now: Optional[float] = None) -> list[Finding]:
    """[#505] batch hygiene — WARN on a linked worktree no live batch owns (ADR-110 §1 item 4).

    THE GAP THIS COVERS, and why `check_no_sibling_orphans` above does not: that check looks for
    `<repo>-*` sibling dirs git has already DEREGISTERED. The state here is the opposite one — a
    worktree git still registers, sitting in `.claude/worktrees/`, left behind because a batch
    ended without its integrator walking the refuse-to-finish close-out. Unclosed parallel work
    is the operator's stated #1 pain (intake #26); this is the after-the-fact backstop for it.

    STALE means either of two things, and both are measured rather than inferred:
      - the last commit on the worktree's tip predates the weekly prune horizon
        (`_STALE_WORKTREE_HORIZON_DAYS`), strictly — reaching the horizon is still live; or
      - git registers the worktree but its directory is gone from disk, AT ANY AGE. That is a
        half-finished teardown (`git worktree remove` silently no-ops on a locked directory),
        and holding it for a week would hide the exact failure the teardown round-trip exists
        to catch.

    A worktree whose commit date cannot be read is reported as INDETERMINATE — surfaced, never
    silently counted as fresh, and never counted as stale either. A detector that cannot see
    does not report clean, and equally does not invent a finding it did not measure.

    POSTURE — WARN only, by ruling. ADR-110 §3 arms no gate, and the [#505] contract scopes this
    organ to WARN-tier. It informs; it does not become a new way for the commit gate to go red
    on a live batch. `tests/test_stale_worktrees.py` pins that at the source level.

    MID-BATCH IS A PASS, deliberately: during a running batch every lane worktree is registered
    and recently committed. An organ that fired then would alarm through the whole run it exists
    to close, and would be muted by the second batch.

    PORTABLE: a consumer inherits it unchanged — nothing here is hub-keyed. Read-only
    (`git worktree list`, `git show -s`); degrades to n/a without git.

    Honest limits. It cannot tell a genuinely abandoned lane from a long-running one that is
    simply slow — age is the only signal available without a batch manifest to read. It says
    nothing about UNMERGED lane branches whose worktree was already removed, which is the other
    half of unclosed parallel work and is the integrator checklist's item 1, not this organ's.
    And it fires after the fact: the close-out refusal lives in `/lane-integrate`, not here.
    """
    entries = _git_linked_worktrees(repo_path)
    if entries is None:
        return [_na("stale_worktrees", _NA_NOT_APPLICABLE,
                    "git unavailable or not a repo - stale-worktree check skipped")]
    if not entries:
        return [Finding("stale_worktrees", "pass",
                        "no linked worktrees registered (primary only) - nothing to close out")]
    if now is None:
        now = datetime.now(timezone.utc).timestamp()
    horizon_secs = _STALE_WORKTREE_HORIZON_DAYS * 86400
    problems: list[str] = []
    live = 0
    for entry in entries:
        label = entry.get("branch") or Path(str(entry.get("path"))).name
        if not entry.get("on_disk"):
            problems.append(f"{label} [registered but gone from disk - run `git worktree prune`]")
            continue
        epoch = entry.get("last_commit_epoch")
        if epoch is None:
            problems.append(f"{label} [age unknown - last-commit date unreadable]")
            continue
        age_days = (now - epoch) / 86400
        if (now - epoch) > horizon_secs:
            problems.append(f"{label} [last commit {age_days:.0f}d ago]")
        else:
            live += 1
    if problems:
        return [Finding("stale_worktrees", "warn",
                        f"{len(problems)} of {len(entries)} linked worktree(s) look unclosed "
                        f"(horizon {_STALE_WORKTREE_HORIZON_DAYS}d): {'; '.join(problems)} - "
                        f"close them out per the /lane-integrate checklist, or say why they "
                        f"stay".replace("|", "/"))]
    return [Finding("stale_worktrees", "pass",
                    f"{live} linked worktree(s) registered, each committed within the "
                    f"{_STALE_WORKTREE_HORIZON_DAYS}d horizon and present on disk - live batch "
                    f"lanes, not leftovers")]


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
        return [_na("handoff_version_stamp", "NOT-APPLICABLE",
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
        return [_na("floor_integrity", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("hooks_armed", "NOT-APPLICABLE",
                        "hub-only — git-hook arming check skipped (not the hub repo)")]
    try:
        if not (Path(repo_path) / ".pre-commit-config.yaml").exists():
            return [_na("hooks_armed", "NOT-APPLICABLE",
                            "no .pre-commit-config.yaml — no managed git hooks to arm")]
        gp = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=repo_path, capture_output=True, text=True, timeout=10,
        )
        if gp.returncode != 0:
            return [_na("hooks_armed", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("git_backlog_drift", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("doc_claims", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("doc_rot", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("undeclared_edges", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("doc_structure", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("no_ff_merges", "NOT-APPLICABLE",
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


# Repo-location env vars git inherits from a hook/pre-commit parent; GIT_DIR overrides both
# `cwd=` and `-C`. Mirrors _GIT_LOCATION_ENV in scripts/fleet_parity.py ([#355]) and is
# deliberately DUPLICATED rather than imported: audit.py imports fleet_parity LAZILY (inside
# check_fleet_parity, for dual script/package mode), and bundle selection must not acquire a
# dependency on that import path. Scrubbed by NAME, never a `startswith("GIT_")` strip -- a
# blanket strip would also drop GIT_CONFIG_GLOBAL / GIT_AUTHOR_* / GIT_SSH_COMMAND.
#
# Applied ONLY inside _select_active_bundle's runner. Deliberately NOT applied to the
# fleet-automation commit path further down, which sets GIT_INDEX_FILE ON PURPOSE via its own
# explicit env= dict -- routing that through this scrub would silently break it.
# DERIVED from `git rev-parse --local-env-vars` (git's own canonical repo-local list, and its
# documented advice for hooks touching a foreign repo), unioned with repo-SCOPING vars git
# does not class as local-env. Deriving removes the rot mode: the first hand-written version
# of this list omitted 8 of git's 15, caught in review. _FALLBACK applies only if git is absent.
_GIT_LOCATION_ENV_EXTRA = ("GIT_CEILING_DIRECTORIES", "GIT_NAMESPACE")
_GIT_LOCATION_ENV_FALLBACK = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
    "GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS", "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
)
_GIT_LOCATION_ENV_CACHE: Optional[frozenset] = None


def _git_location_env() -> frozenset:
    """git's own repo-local env vars (+ _EXTRA). Queried once, cached; pinned fallback if
    git is unavailable. The query itself is repo-agnostic, so it needs no scrubbing."""
    global _GIT_LOCATION_ENV_CACHE
    if _GIT_LOCATION_ENV_CACHE is None:
        names: set[str] = set(_GIT_LOCATION_ENV_FALLBACK)
        try:
            p = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            if p.returncode == 0:
                names |= {ln.strip() for ln in p.stdout.split() if ln.strip()}
        except OSError:
            pass
        _GIT_LOCATION_ENV_CACHE = frozenset(names | set(_GIT_LOCATION_ENV_EXTRA))
    return _GIT_LOCATION_ENV_CACHE


def _select_active_bundle(
    repo_path: Path, candidates: list[Path]
) -> tuple[Optional[Path], str, str]:
    """Pick the ACTIVE handoff bundle from `candidates` by GIT ADD DATE, not slug order.

    Returns ``(bundle, kind, detail)`` where kind is one of:
      "sole"      -- exactly one candidate; no git needed
      "fresh"     -- exactly one candidate with no add-commit (untracked OR staged): the
                     bundle being generated right now, so it outranks every tracked one
      "add-date"  -- newest first-add commit among the tracked candidates
      "no-git"    -- not a git repo / unborn HEAD -> lexical-max fallback (legacy heuristic;
                     a bundle is still returned, so the check stays useful)
      "ambiguous" -- >=2 candidates are fresh; `bundle` is None. NEVER silently pick one:
                     a silent pick between two uncommitted bundles is the same "green about
                     the wrong file" class this selector exists to kill.
      "degraded"  -- git present but a probe errored; `bundle` is None -> caller WARNs.

    WHY not lexical (the defect this replaces): "2026-07-20-dev-knowledge-architect-arc5"
    sorts AFTER "2026-07-20-dev-knowledge-architect" because "-arc5" > "", yet arc5 was
    git-added 2026-07-19 and the plain slug 2026-07-20 -- so the gate validated a stale
    bundle and reported green about the wrong file while the active bundle went unchecked.
    mtime is not usable as a tiebreak: a git worktree checkout re-stamps every file.

    Read-only; fail-soft. EVERY git call here runs through the scrubbed env -- an inherited
    GIT_DIR would resolve the guard below to the WRONG toplevel and silently degrade
    selection to the lexical fallback, reintroducing the exact bug ([#355] recursion).
    """
    lexical = max(candidates, key=lambda d: d.name)
    if len(candidates) == 1:
        return candidates[0], "sole", candidates[0].name

    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}

    def _run(args: list[str]) -> Optional[str]:
        try:
            p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env)
        except OSError:
            return None
        return p.stdout if p.returncode == 0 else None

    # Guard: an empty `--diff-filter=A` means "never added" ONLY inside a real repo whose
    # root IS repo_path. Without this, a temp dir nested under some ancestor repo reports
    # every bundle as fresh -> a bogus ambiguous FAIL.
    #
    # The three failure shapes below are deliberately NOT collapsed into one lexical
    # fallback. Collapsing them is how the stale-bundle false green returns: a git
    # misconfiguration would silently restore exactly the behaviour this selector replaces.
    # Only a confirmed NON-git tree earns the legacy heuristic; everything else degrades
    # loudly.
    top = _run(["rev-parse", "--show-toplevel"])
    if not top or not top.strip():
        # Not a git repo (or git absent). The legacy lexical heuristic is the honest
        # degradation here -- a non-git consumer still gets its bundle validated.
        return lexical, "no-git", lexical.name
    try:
        same = (os.path.normcase(str(Path(top.strip()).resolve()))
                == os.path.normcase(str(Path(repo_path).resolve())))
    except OSError:
        same = False
    if not same:
        # repo_path is nested inside a DIFFERENT repo, so add-dates would be read from the
        # wrong history. Never fall back silently -- surface it.
        return None, "degraded", (f"git toplevel {top.strip()} is not {repo_path} "
                                  "(nested repo?) — cannot trust add-dates")
    if _run(["rev-parse", "--verify", "HEAD"]) is None:
        # Unborn HEAD in a real repo: nothing is committed, so EVERY candidate is
        # genuinely fresh. Fall into the ambiguity rule rather than picking lexically --
        # otherwise a fresh repo with two bundles silently gets the wrong one.
        return None, "ambiguous", ", ".join(sorted(d.name for d in candidates))

    fresh: list[Path] = []
    dated: list[tuple[int, str, Path]] = []
    for d in candidates:
        # No `-1`: git applies -1 BEFORE --reverse, which would yield the NEWEST commit.
        # %at (author unix seconds) not %aI: an integer cannot misorder across timezone
        # offsets, and author-date survives a rebase that rewrites committer dates.
        out = _run(["log", "--diff-filter=A", "--reverse", "--format=%at",
                    "--", f"docs/handoffs/{d.name}"])
        if out is None:
            return None, "degraded", f"git log failed for {d.name}"
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        if not lines:
            fresh.append(d)          # untracked, or staged-but-never-committed
            continue
        try:
            dated.append((int(lines[0]), d.name, d))
        except ValueError:
            return None, "degraded", f"unparseable add-date for {d.name}"

    if len(fresh) > 1:
        return None, "ambiguous", ", ".join(sorted(d.name for d in fresh))
    if len(fresh) == 1:
        return fresh[0], "fresh", fresh[0].name
    if not dated:
        return lexical, "no-git", lexical.name
    dated.sort(key=lambda t: (t[0], t[1]))   # add-date, then slug as a stable tiebreak
    return dated[-1][2], "add-date", dated[-1][1]


# rule: handoff-probes-bind
def check_handoff_probes(repo_path: Path) -> list[Finding]:
    """#163 handoff-probe teeth: every probe in the LATEST v5 PROBES.md bundle binds
    to live state (structural, RESOLVE-ONLY — Critical Rule #4 "Layer 2 never executes",
    zero false positives). Mechanizes the manual v5 probe-gate (HANDOFF_PROCESS §5/§10).

    Bundle-presence-based: validates the ACTIVE docs/handoffs/<slug>/PROBES.md (excluding
    aborted/in-progress/archive); a repo with no such bundle is a no-op pass, so this
    no-ops on the fleet's child repos. Only the ACTIVE handoff is checked — older bundles
    are immutable historical artifacts whose source anchors legitimately drift, so
    re-validating them against current state would mis-flag.

    "Active" is decided by _select_active_bundle: an uncommitted bundle (the one being
    generated now), else the newest by GIT ADD DATE — never slug order, which picked a
    stale "<date>-<slug>-arc5" over the newer "<date>-<slug>" ([#372]). Two uncommitted
    bundles is ambiguous → FAIL, never a silent pick.

    FAIL-class (gating, unlike the WARN-only doc_claims): a malformed row or a missing
    source/command-target FAILs -> Finding "fail" -> the audit-health + ship-gate block
    (a toothless probe cannot ship). A moved anchor / absent tool -> WARN (anchor-missing
    / skipped: degrade loudly, never a synthesized pass). The "Why" column is checked for
    PRESENCE only — rationale quality stays the manual gate. Fail-soft on any error.
    Read-only. Logic lives in scripts/verify_handoff_probes.py.
    """
    handoffs = Path(repo_path) / "docs" / "handoffs"
    if not handoffs.exists():
        return [_na("handoff_probes", "NOT-APPLICABLE",
                        "no docs/handoffs/ — no probe bundle to validate")]
    candidates = sorted(
        (d for d in handoffs.iterdir()
         if d.is_dir() and d.name not in _BUNDLE_EXCLUDE_DIRS
         and (d / "PROBES.md").exists()),
        key=lambda d: d.name,
    )
    if not candidates:
        return [Finding("handoff_probes", "pass",
                        "no v5 PROBES.md bundle to validate")]
    latest, kind, detail = _select_active_bundle(Path(repo_path), candidates)
    if kind == "ambiguous":
        return [Finding("handoff_probes", "fail",
                        f"ambiguous active handoff bundle: {detail} are all uncommitted "
                        "— commit or remove all but one. Refusing to guess which bundle "
                        "the gate validates (a silent pick is a green about the wrong "
                        "file)".replace("|", "/"))]
    if latest is None:
        return [Finding("handoff_probes", "warn",
                        f"bundle selection degraded (read-only, non-blocking): {detail}"
                        .replace("|", "/"))]
    # Cross-repo bundle (ADR-36/41): a handoff whose declared target repo differs from this
    # one. Its probes bind to the TARGET repo's files, so resolve against the target root,
    # not the hub — resolving foreign paths against the hub gives both false FAILs (a target
    # file absent here) AND false PASSes (a basename collision like JOURNAL.md fake-resolves).
    # Fleet onboarding (#221) makes cross-repo the common case, so this keeps the teeth rather
    # than skipping them. A `.claude/` or ambiguous foreign target degrades to WARN (#234).
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
    # Status follows the BRANCH, not the call site ([#465] leg 1): edges that were checked and
    # matched are a real `pass`; zero declared edges is a skip and must not borrow that pass.
    if n:
        return [Finding("reconciled_versions", "pass",
                        f"{n} reconciled_with edge(s) match live spec version(s)")]
    return [_na("reconciled_versions", "NOT-APPLICABLE", "no reconciled_with edges declared")]


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
    if not _is_hub(repo_path):
        return [_na("doc_code_edge", "NOT-APPLICABLE",
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
        return warns or [_na("doc_code_edge", "NOT-APPLICABLE",
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


def check_residual_completeness(repo_path: Path) -> list[Finding]:
    """ARC-5 residual-completeness gate: a handoff bundle may not ship a hand-authored
    FILL-IN region still carrying the generator's `_(fill: ...)_` placeholder.

    Closes a witnessed failure: the ARC-5 inbound bundle merged with §1 ("THE HEADLINE"),
    §2 and §4 ("the residual's core payload") as literal unfilled templates, and no organ
    objected. The generator scaffolds those regions and cannot author them, so landing-time
    is the only catchable moment.

    FAIL-class (gating, like check_handoff_probes): one FAIL Finding per unfilled region, so
    the #147 ship-gate dispositions each independently.

    Diff-triggered / prospective-only (the check_safe_removal shape + the ADR-101
    grandfathering rule): only bundle files added or modified vs HEAD are scanned; a clean
    tree is an instant PASS. Already-committed bundles are historical artifacts, the same
    reasoning check_handoff_probes uses for validating only the active bundle. Stated
    plainly: this does not retroactively fail the ARC-5 bundle that motivated it, but it
    would have failed the commit that landed it.

    ANTI-BLUFF NON-COLLISION: asserts only that the placeholder was replaced — never that a
    value is present, and never on PROBES.md. A demand for concrete content would push an
    author to write the ship-gate verdict / WARN count / drifted #id that probe P7 and the
    verify_handoff_probes answer-hint rung require to be ABSENT. Full rationale and the two
    pinning tests: scripts/validate_residual_completeness.py.

    Fail-soft on any error (never wedge audit-health). Read-only (Layer 2, ADR-28/36).
    """
    try:
        unfilled = _vrc.find_unfilled(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("residual_completeness", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not unfilled:
        return [Finding("residual_completeness", "pass",
                        "no unfilled FILL-IN region in changed handoff bundle files")]
    return [
        Finding("residual_completeness", "fail",
                f"{u.path}: FILL-IN region '{u.region}' still carries the generator "
                f"placeholder (a hand-authored residual shipped as a template)".replace("|", "/"))
        for u in unfilled
    ]


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
    if not _is_hub(repo_path):
        return [_na("doc_code_coverage_drift", "NOT-APPLICABLE",
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
    if not _is_hub(repo_path):
        return [_na("fleet_parity", "NOT-APPLICABLE",
                        "hub-only -- fleet-parity walk skipped (not the hub repo)")]
    try:
        try:
            from scripts import fleet_parity as fp   # package-mode: `python -m scripts.audit`
        except ImportError:
            import fleet_parity as fp                # script-mode: `python scripts/audit.py`
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
        return [_na(name, "NOT-APPLICABLE",
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
    if _is_hub(repo_path):
        return [_na(name, "NOT-APPLICABLE",
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
    return [_na(name, "NOT-APPLICABLE",
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
        return [_na(name, "NOT-APPLICABLE", "no root CLAUDE.md (presence gated by check_claude_md)")]
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


# ADR-105 routine marker. Clause-scoped extraction in the established
# _SERIALIZE_CLAUSE_RE idiom (validate_backlog.py:81) — delimiter-anchored, so a prose
# mention of the keyword in a task body cannot register as a phantom declaration.
_ROUTINE_MARKER_RE = re.compile("·\\s*routine\\s*:")
_ROUTINE_FIELD_RE = re.compile("·\\s*(consumer|consumption_path)\\s*=([^·]*)")
_ROUTINE_TASK_RE = re.compile(r"^- \[#(\d+)\]")
_ROUTINE_REQUIRED = ("consumer", "consumption_path")
# A LOOKALIKE delimiter before `routine:` (bullet/interpunct variants that are NOT the
# canonical U+00B7). Without this a mistyped marker parses as "no declaration" and fails
# OPEN -- the exact silent-inertness class [#424]/[#425] were filed for, so this check
# refuses to reproduce it. A bare prose "routine:" with no bullet is NOT a lookalike.
_ROUTINE_LOOKALIKE_RE = re.compile("[•∙‧⋅]\\s*routine\\s*:")
# Declaration CONTEXT — a lookalike is only a mistyped marker if the row also carries a
# `field=` clause. Without this, prose comparing bullet-listed terms false-FAILs.
_ROUTINE_ANYFIELD_RE = re.compile(r"\b(consumer|consumption_path|trigger|scope)\s*=")
_ROUTINE_FENCE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})")
_ROUTINE_TICK_RUN_RE = re.compile(r"`+")
_ROUTINE_INVISIBLE = str.maketrans({c: None for c in "​‌‍﻿⁠"})
# Values that carry word characters but name nothing.
_ROUTINE_SENTINELS = frozenset({"tbd", "todo", "tba", "n/a", "na", "none", "xxx", "?"})


def _routine_code_spans(line: str) -> list[tuple[int, int]]:
    """Inline-code spans as [start, end) — a backtick run opens, an EQUAL-length run closes.

    Length-matched per CommonMark, so a double-backtick span ``· routine:`` is ONE span
    rather than two single-tick spans that would leave the marker exposed. Deleting spans
    outright was the earlier bug: it erased legitimate backticked VALUES
    (`consumer=`ops-bot``), so spans are located and consulted, never removed.
    """
    runs = [(m.start(), m.end()) for m in _ROUTINE_TICK_RUN_RE.finditer(line)]
    spans: list[tuple[int, int]] = []
    i = 0
    while i < len(runs):
        start, start_end = runs[i]
        width = start_end - start
        for j in range(i + 1, len(runs)):
            close, close_end = runs[j]
            if close_end - close == width:
                spans.append((start, close_end))
                i = j
                break
        i += 1
    return spans


def _routine_in_code(idx: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= idx < b for a, b in spans)


def _routine_value_is_named(raw: str) -> bool:
    """True only for a value that actually NAMES something.

    Rejects blank, invisible-only, punctuation-only, sentinel (`TBD`/`TODO`/`N/A`), and
    unfilled `<template placeholders>`. A placeholder is angle-wrapped AND contains a
    space (ADR-105's template reads `consumer=<who reads it>`); an angle-wrapped autolink
    (`<https://…>`, `<mailto:…>`) has no space and is a legitimate consumption path, so
    it passes. Backticks around a value are formatting, not content.
    """
    v = raw.translate(_ROUTINE_INVISIBLE).strip().strip("`").strip()
    if not v:
        return False
    if v.startswith("<") and v.endswith(">") and " " in v:
        return False
    if v.lower() in _ROUTINE_SENTINELS:
        return False
    return any(ch.isalnum() for ch in v)


def check_routine_consumers(repo_path: Path) -> list[Finding]:
    """[#419]/ADR-105 — a declared routine must name a `consumer` and a `consumption_path`.

    COVERAGE BOUNDARY — read before reading a green result: this checks ONLY BACKLOG
    rows carrying an ADR-105 `· routine:` marker, which at acceptance is exactly ONE row
    ([#348]). The ~30 live routines — session hooks, commit-time gates, scheduled jobs —
    are not BACKLOG rows, carry no marker, and are NOT checked; a pass here says nothing
    whatever about them (retrofit: [#426]). Green does NOT mean the fleet's routines have
    consumers.

    ADR-105 gates at ACTIVATION, not at filing: a row that merely *proposes* a routine
    carries no marker and is correctly not checked. ADR-105 declares six fields; this
    gates the two that make output reach a decision — the other four
    (trigger/scope/verified_by/review_date) are declared, not gated. A marker whose
    `consumer` or `consumption_path` is missing, blank, placeholder, or duplicated is a
    FAIL: an unconsumed routine is the defect [#419] names, and a routine that cannot
    name a consumer is retired rather than activated (that decision is the operator's,
    never this check's).

    Parsing is deliberately hostile to near-misses: fields are read ONLY from the suffix
    after the marker (so prose earlier in the row cannot satisfy the gate), duplicates
    are rejected rather than last-wins, fenced blocks and inline-code spans are stripped
    (so a row *quoting* the marker stays a proposal), and a lookalike delimiter is
    surfaced rather than failing open. Read-only.
    """
    name = "routine_consumers"
    backlog = Path(repo_path) / "BACKLOG.md"
    if not backlog.exists():
        return [_na(name, "NOT-APPLICABLE", "no BACKLOG.md in this repo")]
    try:
        text = backlog.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [Finding(name, "unavailable", f"cannot read BACKLOG.md: {exc}")]
    bad: list[str] = []
    declared = 0
    fence: tuple[str, int] | None = None      # (char, run-length) of the OPEN fence
    for lineno, line in enumerate(text.splitlines(), 1):
        fm = _ROUTINE_FENCE_RE.match(line)
        if fm:
            run = fm.group("fence")
            if fence is None:
                fence = (run[0], len(run))    # indented >3 never opens (regex bounds it)
                continue
            if run[0] == fence[0] and len(run) >= fence[1]:
                fence = None                  # only a same-char, >=-length run closes
            continue
        if fence is not None:
            continue                          # an example is not a declaration
        task = _ROUTINE_TASK_RE.match(line)
        if not task:
            continue
        loc = f"[#{task.group(1)}] line {lineno}"
        spans = _routine_code_spans(line)
        markers = [m for m in _ROUTINE_MARKER_RE.finditer(line)
                   if not _routine_in_code(m.start(), spans)]
        if not markers:
            look = _ROUTINE_LOOKALIKE_RE.search(line)
            if look and not _routine_in_code(look.start(), spans) \
                    and _ROUTINE_ANYFIELD_RE.search(line):
                bad.append(f"{loc}: lookalike delimiter before 'routine:' — a mistyped "
                           f"marker must not fail open".replace("|", "/"))
            continue
        declared += 1
        if len(markers) > 1:
            # A second marker would lend its fields to an incomplete first declaration.
            bad.append(f"{loc}: {len(markers)} 'routine:' markers on one row — "
                       f"ambiguous declaration".replace("|", "/"))
            continue
        suffix = line[markers[0].end():]  # fields belong to the DECLARATION, not the row
        found: dict[str, list[str]] = {}
        for key, value in _ROUTINE_FIELD_RE.findall(suffix):
            found.setdefault(key, []).append(value)
        problems: list[str] = []
        for required in _ROUTINE_REQUIRED:
            values = found.get(required, [])
            if len(values) > 1:
                problems.append(f"{required} declared {len(values)}x")
            elif not values or not _routine_value_is_named(values[0]):
                problems.append(required)
        if problems:
            bad.append(f"{loc}: {', '.join(problems)}".replace("|", "/"))
    if bad:
        return [Finding(name, "fail",
                        "declared routine(s) with no named consumer/consumption_path: "
                        + "; ".join(bad))]
    return [Finding(name, "pass",
                    f"{declared} declared routine row(s) name a consumer and a "
                    f"consumption_path (live hooks/schedules out of scope — [#426])")]


def _index_worktree_divergence(repo_path: Path, *paths: str) -> tuple[str, list[str]]:
    """Do the index and the working tree agree on `paths`? -> ("ok"|"diverged"|"unknown", …)

    Any check that reads the WORKING TREE is only trustworthy while the index agrees with
    it: otherwise a change can be staged and the working copy restored, so the check
    validates the old bytes while the commit records the new ones. Both organs here read
    the working tree, so both consult this first.

    "unknown" (a git probe that could not complete) is NOT "ok" -- treating it as ok was
    itself the fail-open terra found on the sixth pass. Callers block on both non-ok
    states.

    The predicate is simply "does the index differ from the working tree for any monitored
    path", which is what `git diff -- <paths>` answers directly. An earlier version
    INTERSECTED the staged and unstaged path lists (terra HIGH, 7th pass) and so returned
    "ok" when DIFFERENT monitored paths diverged -- staged `BACKLOG.md` alongside a
    regenerated-but-unstaged `tasks/` passed, letting the gate bless a coherent working
    tree while the commit recorded only half of it. Untracked files under the monitored
    paths count too: a newly generated task file is invisible to `git diff`, so omitting
    it would leave the same hole for the add case.
    """
    unstaged = _git(Path(repo_path), "diff", "--name-only", "--", *paths)
    untracked = _git(Path(repo_path), "ls-files", "--others", "--exclude-standard",
                     "--", *paths)
    if unstaged is None or untracked is None \
            or unstaged.returncode != 0 or untracked.returncode != 0:
        return "unknown", []
    divergent = sorted(set(unstaged.stdout.split()) | set(untracked.stdout.split()))
    return ("diverged", divergent) if divergent else ("ok", [])


def _load_silent_rule_baseline(repo_path: Path) -> Optional[dict]:
    """Read ecosystem/silent-rule-baseline.yaml. Returns None when absent/malformed.

    Fail-soft to None rather than raising: an unreadable baseline must surface as an
    INERT gate (a visible WARN), never wedge the whole audit and never pass silently.
    """
    try:
        data = yaml.safe_load(
            (Path(repo_path) / _srd.BASELINE_RELPATH).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


_BASELINE_REFS = ("origin/main", "main")


def _git(repo_path: Path, *args: str) -> Optional[subprocess.CompletedProcess]:
    """Run a git command, or None if git itself could not be invoked."""
    try:
        return subprocess.run(["git", *args], cwd=str(repo_path), capture_output=True,
                              text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError):
        return None


def _target_baseline_state(repo_path: Path) -> tuple[str, Optional[int], Optional[str]]:
    """The baseline on the INTEGRATION TARGET as a PROVEN state, not an inference.

    Returns one of:
      ("valid", n)      a target ref carries a well-formed baseline -- compare against it
      ("absent", None)  a target ref RESOLVES and provably does NOT contain the file --
                        genuine bootstrap, nothing to compare and nothing to launder
      ("invalid", None) a target ref contains the file but it is unreadable/malformed --
                        INDETERMINATE, must block
      ("unresolved", None)  no target ref resolves at all -- UNVERIFIABLE, must block

    Why proven rather than inferred (terra HIGH, 3rd pass 2026-07-27): the previous shape
    asked two separate questions -- "did any ref resolve?" and "did reading a baseline
    succeed?" -- and treated `ref resolved + read failed` as bootstrap. That is fail-open:
    a target baseline that exists but is malformed, or a `git show` that timed out, would
    be read as "no baseline yet" and a raised branch value would pass uncompared. Absence
    is now established positively with `git cat-file -e`, so only real absence bootstraps.

    Reading the target and NOT `HEAD` is itself the earlier fix: once a raise is committed
    HEAD *is* the new value, so a HEAD comparison compares the baseline against itself.
    """
    states = [_ref_baseline_state(repo_path, ref) for ref in _BASELINE_REFS]
    resolved = [(s, v, d) for s, v, d in states if s != "unresolved"]
    if not resolved:
        return "unresolved", None, None
    if any(s == "invalid" for s, _, _ in resolved):
        # ANY resolved-but-unreadable target makes the comparison indeterminate. Falling
        # through to another ref would be the fail-open this shape exists to close.
        return "invalid", None, None
    valid = [(v, d) for s, v, d in resolved if s == "valid" and v is not None]
    if not valid:
        return "absent", None, None        # every resolving ref provably lacks the file
    # Reconcile DETECTORS BEFORE any numeric comparison (terra HIGH, 9th pass). Running
    # min() first could return the ref whose detector happens to match while a second ref
    # sat on a different, non-commensurable scale -- and then merely changing the old
    # detector's numbers would flip the verdict from migration-WARN to PASS.
    detectors = {d for _v, d in valid}
    if len(detectors) > 1:
        return "mixed", None, None
    # STRICTEST of the resolved targets (terra HIGH, 4th pass): returning the first valid
    # ref let a raise hide behind the other one -- with origin/main at 500 and an ahead
    # local main at 400, a branch value of 450 passed against 500 while raising the real
    # local target from 400. min() cannot be gamed by ref ordering or divergence.
    value, detector = min(valid, key=lambda pair: pair[0])
    return "valid", value, detector


def _ref_baseline_state(repo_path: Path, ref: str) -> tuple[str, Optional[int], Optional[str]]:
    """One ref's baseline state: unresolved / absent / valid / invalid.

    Absence is proven with `git ls-tree`, not `git cat-file -e` (terra HIGH, 4th pass).
    `cat-file -e` returns non-zero for an inaccessible or corrupt object and for a failed
    promisor fetch exactly as it does for a missing path, so "non-zero means absent" would
    read an unreadable target as first-introduction and let a raise through uncompared.
    `ls-tree` exits 0 for a resolvable ref and prints NOTHING when the path is genuinely
    absent, which separates "not there" from "could not look".
    """
    rev = _git(repo_path, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if rev is None or rev.returncode != 0 or not rev.stdout.strip():
        return "unresolved", None, None
    # Pin the resolved OID and use it for BOTH probes (terra HIGH, 5th pass). Re-reading
    # the mutable ref NAME lets a concurrent fetch move it between the absence check and
    # the content read, so the two could observe different commits -- and a target baseline
    # could be classified absent against one commit while existing in another.
    oid = rev.stdout.strip()
    listing = _git(repo_path, "ls-tree", "--full-tree", "-z", oid,
                   "--", _srd.BASELINE_RELPATH)
    if listing is None or listing.returncode != 0:
        return "invalid", None, None       # the lookup itself failed: indeterminate
    if not listing.stdout.strip():
        return "absent", None, None        # PROVEN absent at this commit
    show = _git(repo_path, "show", f"{oid}:{_srd.BASELINE_RELPATH}")
    if show is None or show.returncode != 0:
        return "invalid", None, None       # it exists but could not be read
    try:
        data = yaml.safe_load(show.stdout)
    except yaml.YAMLError:
        return "invalid", None, None
    if not isinstance(data, dict):
        return "invalid", None, None
    value = data.get("baseline")
    if not isinstance(value, int) or isinstance(value, bool):
        return "invalid", None, None
    detector = data.get("detector_id")
    if not isinstance(detector, str) or not detector:
        # Without the target's detector id the two numbers cannot be shown commensurable,
        # and the module's whole premise is that counts from different detectors are not
        # comparable (terra HIGH, 8th pass). Indeterminate, so block.
        return "invalid", None, None
    return "valid", value, detector


def _ratchet_findings(live: "_srd.Measurement", baseline: Optional[dict],
                      previous: Optional[int] = None,
                      ref_state: str = "absent",
                      previous_detector: Optional[str] = None) -> list[Finding]:
    """Testable core of check_silent_rule_ratchet ([#436]).

    Kept pure (no filesystem, no git) so the four contract cases -- pass-at-baseline,
    fail-above-baseline, ratchet-down accepted, baseline-raise rejected -- are pinned
    without standing up a repo. Emits exactly ONE Finding so a #147 disposition, if one
    is ever written, cannot suppress an unrelated concern bundled alongside.
    """
    name = "silent_rule_ratchet"
    if baseline is None:
        return [Finding(name, "warn",
                        f"no readable {_srd.BASELINE_RELPATH} — ratchet INERT "
                        f"(live count {live.count}); gate is not measuring anything")]
    stamped = baseline.get("detector_id")
    if stamped != live.detector_id:
        return [Finding(name, "fail",
                        (f"detector mismatch: baseline stamped {stamped!r} but live count "
                         f"produced by {live.detector_id!r} — the two are not commensurable; "
                         f"re-measure and re-stamp rather than comparing them")
                        .replace("|", "/"))]
    value = baseline.get("baseline")
    if not isinstance(value, int) or isinstance(value, bool):
        return [Finding(name, "fail",
                        f"malformed baseline value {value!r} — expected an integer")]
    if ref_state == "mixed":
        # The two integration refs carry baselines from DIFFERENT detectors. There is no
        # single scale to compare against, and picking either would be arbitrary — a
        # broken target state needing human resolution, not a routine migration.
        return [Finding(name, "fail",
                        (f"integration refs ({', '.join(_BASELINE_REFS)}) carry baselines "
                         f"from DIFFERENT detectors — no common scale to compare against; "
                         f"reconcile them before the ratchet can verify anything "
                         f"(live {live.count}, committed {value})").replace("|", "/"))]
    if ref_state == "invalid":
        # The target HAS a baseline but it could not be read. Indeterminate, so a raise
        # cannot be ruled out — block rather than bootstrap past it.
        return [Finding(name, "fail",
                        (f"raise-guard INDETERMINATE: the baseline on the integration ref "
                         f"exists but is unreadable or malformed, so a raise cannot be "
                         f"ruled out (live {live.count}, committed {value})")
                        .replace("|", "/"))]
    if ref_state == "unresolved":
        # No integration ref at all (no remote, shallow/detached clone, not a git tree).
        # WARN blocks ship-gate unless explicitly dispositioned; a pass with a note would
        # not, which was the fail-open terra found on re-review.
        return [Finding(name, "warn",
                        (f"raise-guard UNVERIFIABLE: no integration ref (origin/main, "
                         f"main) resolves, so a baseline raise cannot be ruled out "
                         f"(live {live.count}, committed {value})").replace("|", "/"))]
    if previous is None:
        # PROVEN absent on a resolving ref — the file is genuinely new, so there is no
        # prior value to launder. Surfaced in the evidence, never silent.
        guard = " [raise-guard bootstrap: baseline provably absent on the integration ref]"
    elif previous_detector is not None and previous_detector != live.detector_id:
        # A detector revision makes the two numbers non-commensurable, so the ratchet
        # CANNOT verify this transition -- comparing them numerically would let a bump
        # silently rebase the metric (terra HIGH, 8th pass). WARN blocks ship-gate unless
        # dispositioned, which is the explicit migration path: an operator reviews the
        # re-measurement once, deliberately, rather than a version bump waving it through.
        return [Finding(name, "warn",
                        (f"detector MIGRATION {previous_detector} -> {live.detector_id}: "
                         f"the target baseline {previous} and this arc's {value} were "
                         f"measured by different detectors and are not commensurable; the "
                         f"ratchet cannot verify this transition — review the "
                         f"re-measurement explicitly").replace("|", "/"))]
    else:
        rejection = _srd.validate_transition(old=previous, new=value)
        if rejection is not None:
            return [Finding(name, "fail", rejection.replace("|", "/"))]
        guard = ""
    if live.count > value:
        return [Finding(name, "fail",
                        (f"silent-rule pool GREW: live {live.count} > baseline {value} "
                         f"(+{live.count - value}) under detector {live.detector_id} across "
                         f"{live.files} file(s) — drain the additions or record an operator "
                         f"ruling; the baseline does not rise on a commit")
                        .replace("|", "/"))]
    headroom = value - live.count
    drained = (f"; {headroom} below baseline — ratchet-down available" if headroom else "")
    return [Finding(name, "pass",
                    (f"live {live.count} <= baseline {value} under detector "
                     f"{live.detector_id} ({live.files} file(s) in scope){drained}{guard}")
                    .replace("|", "/"))]


def check_silent_rule_ratchet(repo_path: Path) -> list[Finding]:
    """[#436] silent-rule ratchet — gate the GROWTH of the silently-unenforced rule pool.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction (ship-gate runs
    the full registry and reads Finding.status directly). FAIL-class: the pool growing
    blocks the arc.

    WHAT A GREEN HERE DOES AND DOES NOT MEAN -- read before trusting it. The metric is a
    normative-keyword OCCURRENCE COUNT produced by a pinned detector
    (scripts/silent_rule_detector.py), NOT the census's `N_silent`. It cannot distinguish a
    rule from a mention of one in an example, and it counts keywords rather than rules. Green
    means "the governed corpus did not accrete normative prose since the baseline" -- it
    does NOT mean the 176-rule backlog was drained, and it says nothing about whether any
    individual rule has a mechanism. The drain is separate work ([#356], [#358]-[#361],
    review 2026-08-26).

    Why a proxy at all: the census figure is not reproducible by code (its regex and file
    filter were never recorded), so no check can recompute it. The 2026-07-27 arm-time
    re-measurement stopped the build on exactly that. D4 (architect-proposed,
    operator-adopted) resolves it by pinning a detector and letting it define the metric.

    RATCHET-DOWN ONLY, enforced two ways: `validate_transition` FAILs a raise of the
    committed baseline against its previous committed value, and this check never writes.
    Hub-only (the detector's scope roots are hub surfaces); read-only.
    """
    if not _is_hub(repo_path):
        return [_na("silent_rule_ratchet", "NOT-APPLICABLE",
                        "hub-only — the detector's scope roots are hub governance surfaces")]
    try:
        live = _srd.measure(Path(repo_path))
    except (OSError, UnicodeDecodeError, _srd.DetectorError) as exc:
        # FAIL, not "unavailable" (terra HIGH, 2026-07-27): ship-gate blocks only on `fail`
        # and undispositioned `warn`, so an "unavailable" detector would ship GREEN having
        # measured nothing at all. A decode failure silently zeroed files in the arm-time
        # probe's first run -- an unmeasured corpus must block, not wave the arc through.
        return [Finding("silent_rule_ratchet", "fail",
                        f"detector could not measure the corpus: {exc!r}".replace("|", "/"))]
    # The baseline is read from the WORKING TREE while the detector measures the INDEX, so
    # staging a raised baseline and restoring the working copy would validate the old value
    # while committing the raised one -- defeating ratchet-down-only (terra HIGH, 6th pass).
    # Refuse to answer unless the two agree.
    agreement, divergent = _index_worktree_divergence(Path(repo_path),
                                                      _srd.BASELINE_RELPATH)
    if agreement != "ok":
        detail = (", ".join(divergent) if divergent
                  else "git could not compare index and working tree")
        return [Finding("silent_rule_ratchet", "fail",
                        (f"baseline read is untrustworthy: {detail} — stage or restore "
                         f"{_srd.BASELINE_RELPATH} consistently, then re-run")
                        .replace("|", "/"))]
    ref_state, previous, previous_detector = _target_baseline_state(Path(repo_path))
    return _ratchet_findings(live, _load_silent_rule_baseline(Path(repo_path)),
                             previous, ref_state, previous_detector)


def _task_tree_findings(problems: list[str], present: bool = True) -> list[Finding]:
    """Testable core of check_task_tree_coherence ([#433] C1). Pure: takes the problem list
    `gen_task_tree.find_incoherences` produced and maps it to a Finding.

    Direction flipped by [#439] (ADR-107 step 3): `tasks/` is the SOURCE OF TRUTH and
    `BACKLOG.md` is the generated side, so the remedy named in a failure is
    `--emit-source` (tree -> file), not `--write` (file -> tree, now the import path).
    """
    name = "task_tree_coherence"
    if not present:
        return [_na(name, "NOT-APPLICABLE", "no tasks/ source tree in this repo")]
    if problems:
        shown = "; ".join(problems[:6])
        more = f" (+{len(problems) - 6} more)" if len(problems) > 6 else ""
        return [Finding(name, "fail",
                        (f"BACKLOG.md is STALE vs the tasks/ source of truth — regenerate "
                         f"with `gen_task_tree.py --emit-source`: {shown}{more}").replace("|", "/"))]
    return [Finding(name, "pass",
                    "BACKLOG.md coherent with the tasks/ source of truth "
                    "(structure + frontmatter honesty + full reassembly)")]


def check_task_tree_coherence(repo_path: Path) -> list[Finding]:
    """[#433] C1 — the `tasks/` coherence gate. [#439] — flipped to the post-flip direction.

    Closes a gap ARCHITECTURE Ch5 named against its own "no organ = decoration" rule:
    `gen_task_tree.py --check` existed as a MODE that nothing invoked. No pre-commit hook
    and no audit check called it, so coherence rested entirely on one pytest case — and a
    BACKLOG edit that skipped the suite left the tree stale at commit time. That was not
    hypothetical: at `b4dd3e48` the committed tree had already drifted (two task files
    stale, [#435]/[#436] missing, manifest and reassembly both mismatched).

    ARMING THIS GATE WAS A PRECONDITION OF THE FLIP, not a follow-up to it (ADR-107 §7.2
    condition (ii)): a stale DERIVED tree is merely wrong, whereas a stale SOURCE-OF-TRUTH
    tree is a corrupted record. Since [#439] the pair is inverted — `tasks/` is the source
    and `BACKLOG.md` is generated — so this leg now asks "does the committed BACKLOG.md
    equal what the tree generates, and does every task file's frontmatter still agree with
    its own body?" Both artifacts are still required, and the index/worktree guard still
    covers both paths, because either one going stale is the same corruption.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction. FAIL-class.

    SCOPE (inherited from `find_incoherences`, restated so a green is not over-read): this
    compares the two artifacts against EACH OTHER. It does NOT detect a consistent rewrite
    of both together — the expectation is derived from the tree being checked. Source
    integrity is a separate leg (clean `git status` plus the manifest's `generated_sha256`
    pinning which output bytes the tree claims to produce). Hub-only; read-only — it never
    regenerates anything, because a gate that silently fixes what it measures cannot fail.
    """
    if not _is_hub(repo_path):
        return [_na("task_tree_coherence", "NOT-APPLICABLE",
                        "hub-only — tasks/ is a hub-owned tree")]
    root = Path(repo_path)
    source, out_dir = root / "BACKLOG.md", root / "tasks"
    # On the hub BOTH artifacts are required, so a missing one is a FAIL, not "n/a"
    # (terra HIGH, 2026-07-27): returning n/a here made the newly-armed leg non-blocking
    # precisely when one of its artifacts had been deleted -- deleting tasks/ would have
    # disarmed the gate that exists to notice tasks/ drifting. `n/a` is reserved for the
    # off-hub guard above, which is the only case where absence is legitimate. Post-flip
    # ([#439]) an absent tasks/ is strictly worse than it was: it is the SOURCE that has
    # gone missing, not a regenerable derivative.
    missing = [n for n, p in (("BACKLOG.md", source), ("tasks/", out_dir)) if not p.exists()]
    if missing:
        return [Finding("task_tree_coherence", "fail",
                        f"required hub artifact(s) absent: {', '.join(missing)} — the "
                        f"coherence gate cannot be satisfied by deleting what it checks")]
    # The coherence read is a WORKING-TREE read, so it is only trustworthy while the index
    # agrees with the working tree for these paths (terra HIGH, 5th pass): otherwise a
    # staged BACKLOG change can be hidden by restoring the working copy before committing,
    # and the gate would bless a coherent old tree while the commit records an incoherent
    # source/tree pair. Refuse to answer rather than answer about the wrong bytes.
    # A probe that could NOT complete is not agreement (terra HIGH, 6th pass): skipping the
    # guard on a git timeout or error reopened the exact hiding path it exists to close.
    agreement, divergent = _index_worktree_divergence(Path(repo_path), "BACKLOG.md", "tasks")
    if agreement != "ok":
        detail = ("index and working tree disagree on " + ", ".join(divergent)
                  if divergent else "git could not compare index and working tree")
        return [Finding("task_tree_coherence", "fail",
                        (f"{detail} — the coherence read cannot be trusted; stage or "
                         f"restore consistently, then re-run").replace("|", "/"))]
    try:
        problems = _gtt.find_incoherences(source, out_dir)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        # FAIL, not warn (terra HIGH re-review, 2026-07-27). A blanket `except Exception ->
        # warn` let malformed artifacts slip past a gate documented as FAIL-class: the
        # commit-time audit-health gate blocks only on `fail`. These are the artifact-read
        # and parse errors the tree can legitimately raise, and an unreadable derived tree
        # is exactly the state this gate exists to refuse. Anything OUTSIDE this set is a
        # programming defect and is deliberately left to propagate rather than be
        # laundered into a passing status.
        return [Finding("task_tree_coherence", "fail",
                        f"derived-tree check could not complete: {exc!r}".replace("|", "/"))]
    return _task_tree_findings(problems)


def check_intake_tree_coherence(repo_path: Path) -> list[Finding]:
    """[#383] wave 1 — the `docs/intake/` residue-carrier gate: ADR-109 §4's generality proof.

    ADR-109 §4 (transcribing ADR-107 §6.2) withholds the fleet desired-state contract's claim
    to GENERALITY until the engine pattern is *shown* on a second governed surface —
    "per-item frontmattered `.md` files with byte-exact identity, a residue manifest, and a
    green regen-and-diff round-trip — demonstrated by a committed round-trip proof, not by
    argument". This leg is the "green regen-and-diff round-trip" half, armed so the proof is
    a standing gate rather than a one-off run: the same "no organ = decoration" rule that
    motivated `check_task_tree_coherence` for surface 1.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction. FAIL-class.

    HUB-ONLY, and the guard is the REPO IDENTITY, not the presence of `docs/intake/`
    (verification finding, [#383] wave 1). Both corp-monorepo and ai-council DO carry a
    `docs/intake/` while carrying no residue carrier — the carrier is hub machinery that has
    not been distributed — so keying "adopted" off the folder would have reported a FAIL on
    two consumer repos and manufactured a fleet gap that does not exist (the
    enforcement-organs-are-not-homogeneous class). Off-hub is `n/a`.

    On the hub BOTH artifacts are required, so a missing one is a FAIL, not `n/a` — the same
    terra ruling the `tasks/` gate carries: a coherence gate must not be satisfiable by
    deleting what it checks. `n/a` is reserved for the off-hub guard.

    The four legs are NOT re-declared here — `gen_intake_tree.evaluate` is the single
    definition, shared with the `--check` CLI, so the gate and the command can never disagree
    about what coherent means. Read-only: it never regenerates anything, because a gate that
    silently fixes what it measures cannot fail.
    """
    if not _is_hub(repo_path):
        return [_na("intake_tree_coherence", "NOT-APPLICABLE",
                        "hub-only — the docs/intake/ residue carrier is hub-owned")]
    intake_dir = Path(repo_path) / "docs" / "intake"
    # The coherence read is a WORKING-TREE read, so it is only trustworthy while the index
    # agrees with the working tree for these paths (codex-review HIGH, 2026-07-31 — the
    # `tasks/` gate carries this guard and this one did not): otherwise a staged deletion or
    # edit under docs/intake/ can be hidden by restoring the working copy before committing,
    # and the gate would bless a coherent working tree while the commit records an
    # incoherent — or absent — carrier.
    agreement, divergent = _index_worktree_divergence(Path(repo_path), "docs/intake")
    if agreement != "ok":
        detail = ("index and working tree disagree on " + ", ".join(divergent)
                  if divergent else "git could not compare index and working tree")
        return [Finding("intake_tree_coherence", "fail",
                        (f"{detail} — the coherence read cannot be trusted; stage or "
                         f"restore consistently, then re-run").replace("|", "/"))]
    try:
        verdict, reasons = _gint.evaluate(intake_dir)
    except Exception as exc:  # noqa: BLE001 — a gate that cannot complete must not pass
        return [Finding("intake_tree_coherence", "fail",
                        f"intake residue-carrier check could not complete: {exc!r}"
                        .replace("|", "/"))]
    if verdict == _gint.OK:
        return [Finding("intake_tree_coherence", "pass",
                        f"intake residue carrier coherent ({reasons[0]})".replace("|", "/"))]
    return [Finding("intake_tree_coherence", "fail",
                    (f"{'; '.join(reasons)} — run {_gint.REMEDY}").replace("|", "/"))]


# rule: handoff-boot-budget
def check_boot_byte_budget(repo_path: Path) -> list[Finding]:
    """A10 item 2 / R4 ([#446]): `protocols/HANDOFF_BOOT.md` stays within its stated numeric
    byte budget — 18,000 bytes, ruled 2026-07-31 (architect technical lane).

    WHY A GATE AND NOT JUST A WARN (operator ruling 2026-07-31). Enforcement is split by
    site: `assemble_paste.py` WARNs and still assembles, so an over-long boot stays
    GENERATABLE; this check FAILs, so it stops being SHIPPABLE. The guarantee belongs in the
    organ that blocks the merge — a warning nobody has to clear is how the 36.5 KB -> 59 KB
    paste creep happened in the first place (the precedent that motivated a budget at all).

    The budget VALUE is single-sourced from `assemble_paste.HANDOFF_BOOT_BYTE_BUDGET`, never
    re-declared here: two organs enforcing the same rule against two different numbers is the
    drift this pairing exists to prevent. Scope is the boot file ALONE — the per-bundle
    session header is explicitly NOT governed by it (R4), and the assembled `PASTE_THIS.md`
    keeps its own separate `_SIZE_WARN_BYTES` budget.

    Portable: every repo with a `protocols/HANDOFF_BOOT.md` is measured. Absent file -> n/a
    (a consumer that has not adopted the browser boot is not in breach). Read-only.
    """
    boot = Path(repo_path) / "protocols" / "HANDOFF_BOOT.md"
    if not boot.exists():
        return [_na("boot_byte_budget", "NOT-APPLICABLE",
                        "no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot")]
    try:
        size = len(boot.read_bytes())
    except OSError as exc:
        return [Finding("boot_byte_budget", "warn",
                        f"could not read protocols/HANDOFF_BOOT.md: {exc!r}".replace("|", "/"))]
    budget = _assemble_paste.HANDOFF_BOOT_BYTE_BUDGET
    if size > budget:
        return [Finding("boot_byte_budget", "fail",
                        f"protocols/HANDOFF_BOOT.md is {size} bytes, over its {budget}-byte "
                        f"budget by {size - budget} — trim the browser role file "
                        f"(A10 item 2 / R4)")]
    return [Finding("boot_byte_budget", "pass",
                    f"protocols/HANDOFF_BOOT.md is {size} bytes, within its {budget}-byte budget")]


# --- [#460] replication of the ADR-80 durable record ------------------------
# ADR-80 promises a DURABLE record; `_commit_routine_outputs` writes it to a LOCAL branch.
# Between 2026-07-16 and 2026-08-01 the push that made it durable was absent and 51 commits
# accumulated on one disk unnoticed, because the push's only owner ([#254]) had closed on an
# existence-shaped Done-when ("origin/... exists and tracks") that a single manual push
# satisfied. The push leg (`_push_routine_branch`) fixes the mechanism; this alarm is the
# BACKSTOP, because a push can only shout at the moment it fails while divergence PERSISTS.
#
# Graduated rather than binary: the routine is daily, so one or two commits of lag is a
# transient push failure (network, credentials) and REDding the ship-gate for it would train
# the operator to disposition the organ -- the exact way the 46-day FAIL on the fleet branch
# came to be ignored. Past the threshold it is an outage, and ADR-80's promise is false.
REPLICATION_LAG_FAIL_AFTER = 3


def classify_replication_lag(ahead: int) -> tuple[str, str]:
    """PURE: (status, evidence) for `ahead` unreplicated commits. ASCII-only evidence ([#470])."""
    if ahead <= 0:
        return ("pass", f"{_AUTOMATION_BRANCH} is replicated to origin (0 commits ahead)")
    if ahead <= REPLICATION_LAG_FAIL_AFTER:
        return ("warn", f"{_AUTOMATION_BRANCH} is {ahead} commit(s) ahead of origin -- a "
                        f"recent push likely failed; ADR-80's durable record is behind")
    return ("fail", f"{_AUTOMATION_BRANCH} is {ahead} commit(s) ahead of origin, over the "
                    f"{REPLICATION_LAG_FAIL_AFTER}-commit threshold -- ADR-80 promises a "
                    f"durable record that currently exists on ONE disk ([#460])")


def check_fleet_audit_replication(repo_path: Path) -> list[Finding]:
    """[#460] — is the ADR-80 durable record actually replicated to origin?

    HUB-ONLY by repo identity, not by branch presence: `automation/fleet-audit` is hub
    machinery that was never distributed, so keying off anything else would manufacture a
    fleet gap on consumers that correctly have no such branch (the
    enforcement-organs-are-not-homogeneous class, [#383] wave 1).

    Reads the REMOTE-TRACKING ref, never the network: the check must be runnable offline and
    inside the ship-gate without turning a verification organ into a network dependency. The
    consequence is stated rather than hidden -- it measures lag against the last-known origin,
    so a very stale fetch understates it. It cannot OVERstate it, which is the safe direction
    for an alarm.

    An absent branch or absent tracking ref is `n/a`, not a failure: there is nothing to
    replicate, and a repo that has never run the routine is not in breach of ADR-80.
    """
    if not _is_hub(repo_path):
        return [_na("fleet_audit_replication", "NOT-APPLICABLE",
                        "hub-only -- automation/fleet-audit is hub-owned machinery")]

    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}

    def _run(args: list[str]) -> Optional[str]:
        try:
            p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env)
        except OSError:
            return None
        return p.stdout.strip() if p.returncode == 0 else None

    local = _run(["rev-parse", "--verify", "--quiet", f"refs/heads/{_AUTOMATION_BRANCH}"])
    if not local:
        return [_na("fleet_audit_replication", "NOT-APPLICABLE",
                        f"no local {_AUTOMATION_BRANCH} branch -- nothing to replicate")]
    remote_ref = f"refs/remotes/origin/{_AUTOMATION_BRANCH}"
    if not _run(["rev-parse", "--verify", "--quiet", remote_ref]):
        # NOT n/a (codex HIGH, 2026-08-01). A local durable branch with no remote-tracking ref
        # means this clone has no evidence the record was EVER replicated -- the strongest form
        # of the defect, not an absence of one. Returning `n/a` here would disable the backstop
        # in exactly the never-replicated case it exists for, and the first draft's own evidence
        # string said "has never been replicated" while reporting `n/a`.
        return [Finding("fleet_audit_replication", "fail",
                        f"local {_AUTOMATION_BRANCH} exists but there is no {remote_ref} -- no "
                        f"evidence it has EVER been replicated; ADR-80's durable record may "
                        f"exist on ONE disk ([#460]). If this clone simply has not fetched, "
                        f"run git fetch origin and re-check")]

    count = _run(["rev-list", "--count", f"{remote_ref}..refs/heads/{_AUTOMATION_BRANCH}"])
    if count is None or not count.isdigit():
        return [Finding("fleet_audit_replication", "unavailable",
                        "git rev-list failed -- replication lag not measurable here")]

    status, evidence = classify_replication_lag(int(count))
    return [Finding("fleet_audit_replication", status, evidence.replace("|", "/"))]


# --- [#462] fleet-membership agreement --------------------------------------
# The [#382] census censused `ecosystem/registry.md` ITSELF, so a member absent FROM that
# registry was invisible BY CONSTRUCTION -- `terminal-setup` sat declared in ADR-104 and in
# VISION while present in zero machine surfaces, caught only because three consecutive
# nightly digests re-noticed it by hand. This organ inverts the direction: the DECLARATION is
# the fixed point and the surfaces are diffed against it, so absence is reported rather than
# waited for.
#
# The declaration is a CONSTANT, deliberately. Parsing ADR-104's prose into repo ids is a new
# loadable declaration source -- [#472]'s scope, and its option (c) collides with ADR-109 §2
# ("No new physical contract file is created in v1.") and §9's named rejection. A constant
# needs no new file, no `SourceSurface` value and no loader change.
#
# Its honest cost, named not claimed away: the constant COULD drift from ADR-104:15 silently.
# [#472] CLOSED that (ADR-104 amendment 2026-08-03): the ADR now carries the same nine ids inside
# a machine-locatable `declaration:start/end id=adr104-fleet-members` anchor, and the
# declaration-agreement leg below reads it and REDs `audit-health` on any disagreement. The
# amendment is the SOURCE; this constant is the MIRROR the leg checks -- it stays the census
# input (ADR-109 section 2/9 forbid a new persisted declaration file), so nothing here becomes a
# loader. Edit one without the other and the gate names which side is stale.
ADR104_FLEET_DECLARATION = (
    ".dev-knowledge", "ai-council", "corp-monorepo", "corp-ops",
    "corp-sca-time-automation", "demo-prep", "life-architect", "terminal-setup",
    "win-tooling",
)

# ADR-109 §2: membership resolves TOWARD deployed-versions.yaml -- the durable record.
_MEMBERSHIP_ANCHOR = "deployed-versions"

# [#472] -- the ADR-104 declaration anchor. An HTML-comment PAIR, chosen on evidence: this repo's
# scripts/ parses five HTML-comment grammars for content location and ZERO fence info-strings
# (every fence handler treats a fence as a region to SKIP). `methodology:*` was rejected as
# boundary_report's hub/repo-OWNERSHIP axis, and the UPPERCASE `X:START/END` form as the shape
# three GENERATORS use -- putting that in an immutable ADR would falsely signal a machine may
# rewrite the block. The fence inside the block is render decoration; the comments are the
# contract.
ADR104_PATH = "docs/decisions/ADR-104-fleet-repository-shape.md"
_DECL_ANCHOR_ID = "adr104-fleet-members"
# FULL-LINE markers with a HARD id boundary (terra HIGH, 2026-08-04). `\b` after the id was
# wrong twice over: `-` is a non-word character, so `id=adr104-fleet-members-v2` satisfied a
# word boundary and matched this anchor -- a differently-versioned block would have been read
# as if it were this one. The id must now be followed by whitespace or the comment close, and
# the marker must occupy its own line, so a marker mentioned mid-sentence is not a match either.
_DECL_START_RE = re.compile(
    rf"^[ \t]*<!--[ \t]*declaration:start[ \t]+id={_DECL_ANCHOR_ID}(?=[ \t]|-->)[^>]*-->[ \t]*$",
    re.MULTILINE)
_DECL_END_RE = re.compile(
    rf"^[ \t]*<!--[ \t]*declaration:end[ \t]+id={_DECL_ANCHOR_ID}(?=[ \t]|-->)[ \t]*-->[ \t]*$",
    re.MULTILINE)


class DeclarationError(RuntimeError):
    """The ADR-104 declaration anchor is absent, duplicated, or unterminated."""


def read_adr104_declaration(path) -> list[str]:
    """The repo ids inside ADR-104's `declaration:start/end` anchor, in file order.

    Returns a LIST, not a set: the count is part of the contract, so a duplicated line is a
    detectable defect rather than one silently collapsed away.

    Raises DeclarationError when the anchor is missing, appears more than once, or has no end
    marker. Never degrades to an empty result -- the check's standing rule is that a gate which
    can be satisfied by deleting what it checks is not a gate.
    """
    text = Path(path).read_text(encoding="utf-8")
    # A marker shown as an EXAMPLE inside a code fence is not the declaration (terra HIGH,
    # 2026-08-04): without this, an incidental fenced example could supply the only matched
    # pair and be read as the source while the real anchor was absent. Fence detection is the
    # corpus-proven `toc.generator` helper rather than a second hand-rolled toggle -- the
    # 2026-08-03 arc established that such toggles are wrong in at least four ways.
    # Dual-import, the pattern block_ff_push already uses for validate_no_ff. Script mode
    # (`python scripts/audit.py`) puts scripts/ on sys.path; package mode
    # (`python -m scripts.audit`) puts the repo ROOT there. The bare import happens to resolve
    # in package mode today only because another imported script inserts scripts/ as a SIDE
    # EFFECT -- incidental, not a contract, and terra flagged the fragility (2026-08-04).
    try:  # noqa: PLC0415 -- local: keeps audit's import cheap on the audit-health path
        from toc.generator import _code_line_indices
    except ImportError:
        from scripts.toc.generator import _code_line_indices
    fenced = _code_line_indices(text)

    def _outside_fence(m) -> bool:
        return text.count("\n", 0, m.start()) not in fenced

    starts = [m for m in _DECL_START_RE.finditer(text) if _outside_fence(m)]
    ends = [m for m in _DECL_END_RE.finditer(text) if _outside_fence(m)]
    if not starts:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' not found in {ADR104_PATH} -- "
            f"the declaration source cannot be satisfied by deleting what it checks ([#472])")
    if len(starts) > 1:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' appears {len(starts)} times in "
            f"{ADR104_PATH}; exactly one is required ([#472])")
    if not ends:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has a start marker with no matching "
            f"end marker ([#472])")
    if len(ends) > 1:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has {len(ends)} end markers in "
            f"{ADR104_PATH}; exactly one is required ([#472])")
    if ends[0].start() < starts[0].end():
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has its end marker before its start "
            f"marker in {ADR104_PATH} ([#472])")
    inner = text[starts[0].end():ends[0].start()]
    # The fence is decoration (without it markdown joins the ids into one paragraph), so fence
    # lines are dropped and every other non-blank line is an id.
    return [ln.strip() for ln in inner.splitlines()
            if ln.strip() and not ln.strip().startswith("```")]

# Surface id -> repo-relative path. Ids reuse the loader's C1 facts vocabulary
# (`desired_state_loader.SRC_*`) so the two organs name the same surfaces the same way.
_MEMBERSHIP_SURFACES = (
    ("registry-md", "ecosystem/registry.md"),
    ("index-yaml", "ecosystem/index.yaml"),
    ("deployed-versions", "ecosystem/deployed-versions.yaml"),
    ("parity-surfaces", "ecosystem/parity-surfaces.yaml"),
    ("onboarding-rulings", "ecosystem/satellite-onboarding-rulings.yaml"),
)


def _read_registry_members(path: Path) -> set[str]:
    """The hand-maintained markdown table -> registered repo ids.

    Twin of `desired_state_loader.parse_registry_md` (same row regex). Duplicated ON PURPOSE
    rather than imported: that module pulls pydantic, and this check runs on the `audit-health`
    pre-commit path where [#343] already flags per-commit cost. The duplication is held honest
    by a test asserting both readers agree on the live file, not by a comment.
    """
    return set(re.findall(r"(?m)^\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|[^|]*\|\s*$",
                          path.read_text(encoding="utf-8")))


def _read_surface_members(surface_id: str, path: Path) -> set[str]:
    """Repo ids carried by one repo-keyed surface. Raises on absent/malformed -- the caller
    turns that into a FAIL, because a gate satisfiable by deleting its input is not a gate."""
    if surface_id == "registry-md":
        return _read_registry_members(path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if surface_id == "index-yaml":
        return {str(r["name"]) for r in (doc.get("repos") or ()) if r.get("name")}
    key = {"deployed-versions": "repos", "parity-surfaces": "fleet",
           "onboarding-rulings": "rulings"}[surface_id]
    return {str(k) for k in (doc.get(key) or {})}


def classify_membership(declaration: tuple[str, ...],
                        surfaces: dict[str, set[str]]) -> list[tuple[str, str]]:
    """PURE: [(status, evidence)] for a fleet declaration diffed against repo-keyed surfaces.

    Two directions, deliberately asymmetric:

    * A repo a surface carries but the declaration does not -> FAIL, naming repo AND surface.
      Either ADR-104 is stale or the surface is wrong; both need a human, and which surface
      is the first question that human asks.
    * A declared repo missing from the anchor -> reported as DATA at pass. Ruled 2026-08-01,
      on ADR-109 §2 ("the disagreement itself is carried as model data, never a load error")
      and §8 ("Stale derived inputs are surfaced, not fixed"). Not warn: an undispositioned
      WARN REDs the ship-gate, which trains the operator to disposition the organ -- exactly
      how a 46-day FAIL came to be ignored ([#460]).

    ASCII-only, pipe-free evidence ([#470] + the Finding contract).
    """
    declared = set(declaration)
    findings: list[tuple[str, str]] = []
    for surface_id, members in surfaces.items():
        for repo in sorted(members - declared):
            findings.append(("fail",
                             f"{surface_id} carries repo '{repo}', absent from the ADR-104 "
                             f"fleet declaration -- an undeclared member: either the "
                             f"declaration is stale or the surface is wrong ([#462])"))

    resolved = surfaces.get(_MEMBERSHIP_ANCHOR, set())
    where = [f"{repo} [{', '.join(s for s, m in surfaces.items() if repo in m) or 'NO SURFACE'}]"
             for repo in declaration if repo not in resolved]
    coverage = ", ".join(f"{s} {len(m & declared)}/{len(declared)}"
                         for s, m in surfaces.items())
    findings.append(("pass",
                     f"{len(declared)} declared (ADR-104); {len(resolved & declared)} resolved "
                     f"members ({_MEMBERSHIP_ANCHOR}); coverage {coverage}; "
                     f"declared-but-not-deployed: {'; '.join(where) if where else 'none'}"))
    return findings


def _declaration_agreement(repo_path: Path) -> list[Finding]:
    """[#472] — ADR-104's anchored declaration vs `ADR104_FLEET_DECLARATION`.

    Three assertions and nothing more:
      1. the anchor pair exists exactly once (absent / duplicated / unterminated -> FAIL);
      2. the ids agree with the constant as a SET **and** in COUNT, so a duplicated line is
         caught rather than collapsed away;
      3. nothing else -- the block is NEVER fed to `classify_membership`. The amendment is the
         authority the constant is checked against, never the census's membership input, so
         ADR-109 section 2 (`resolve_fleet_members` not widened) stays intact.

    Drift is reported naming BOTH directions separately, because "which side is stale" is the
    first question a human asks.
    """
    try:
        declared = read_adr104_declaration(Path(repo_path) / ADR104_PATH)
    except DeclarationError as exc:
        return [Finding("membership_agreement", "fail", str(exc).replace("|", "/"))]
    except OSError as exc:
        return [Finding("membership_agreement", "fail",
                        f"ADR-104 could not be read at {ADR104_PATH}: {exc!r}".replace("|", "/"))]

    constant = list(ADR104_FLEET_DECLARATION)
    if sorted(declared) == sorted(constant):
        return [Finding("membership_agreement", "pass",
                        f"declaration source: ADR-104 anchor '{_DECL_ANCHOR_ID}', "
                        f"{len(declared)} ids, agrees with audit.ADR104_FLEET_DECLARATION")]

    only_adr = sorted(Counter(declared) - Counter(constant))
    only_const = sorted(Counter(constant) - Counter(declared))
    parts = []
    if only_adr:
        parts.append(f"in the ADR amendment only: {', '.join(only_adr)}")
    if only_const:
        parts.append(f"in the constant only: {', '.join(only_const)}")
    if not parts:  # same members, different counts -- a duplicated line
        parts.append(f"same ids but different counts (ADR {len(declared)} vs constant "
                     f"{len(constant)}); a duplicated line in the ADR amendment only")
    return [Finding("membership_agreement", "fail",
                    "ADR-104 declaration and audit.ADR104_FLEET_DECLARATION disagree: "
                    + "; ".join(parts)
                    + "; the constant and its declaring ADR have drifted -- fix whichever is "
                      "stale, in one commit with the other ([#472])")]


def check_membership_agreement(repo_path: Path, _surface_paths=None) -> list[Finding]:
    """[#462] — the ADR-104 fleet declaration diffed against every repo-keyed machine surface.

    Closes the blind spot that made [#462] invisible for months: a census keyed on one
    registry cannot see a member missing from that registry, so this one is keyed on the
    DECLARATION and reports per-repo per-surface presence.

    HUB-ONLY by repo identity, never by artifact presence: `ecosystem/`'s registries are hub
    machinery that was never distributed, so guarding on "does this repo have registries"
    would report FAIL across the fleet and manufacture a gap that does not exist (the
    enforcement-organs-are-not-homogeneous class, [#383] wave 1).

    Read-only. It never regenerates a surface -- a gate that silently fixes what it measures
    cannot fail. `resolve_fleet_members` is NOT consulted and NOT widened: that resolution is
    a named ADR-109 §2 ruling and belongs to [#472].
    """
    if not _is_hub(repo_path):
        return [_na("membership_agreement", "NOT-APPLICABLE",
                        "hub-only -- the ecosystem/ membership surfaces are hub-owned")]

    # [#472] declaration-agreement leg. Attached HERE -- after the hub guard, before the surfaces
    # loop -- on purpose: the constant is verified before it is handed to classify_membership, and
    # a declaration/constant disagreement is still reported when a later surface read fails.
    # Evaluated HERE (before the surfaces loop) per the ruled attach point, so the constant is
    # verified before classify_membership receives it and the verdict survives an early return.
    # Emitted LAST: output position is cosmetic, and prepending would silently re-index every
    # caller that reads findings[0] as the census verdict.
    decl: list[Finding] = list(_declaration_agreement(Path(repo_path)))

    surfaces: dict[str, set[str]] = {}
    for surface_id, rel in (_surface_paths or _MEMBERSHIP_SURFACES):
        path = Path(repo_path) / rel
        try:
            surfaces[surface_id] = _read_surface_members(surface_id, path)
        except FileNotFoundError:
            return [Finding("membership_agreement", "fail",
                            f"membership surface {rel} is absent -- the census cannot be "
                            f"satisfied by deleting what it checks ([#462])")] + decl
        except Exception as exc:  # noqa: BLE001 -- a gate that cannot complete must not pass
            return [Finding("membership_agreement", "fail",
                            f"membership surface {rel} could not be read: {exc!r}"
                            .replace("|", "/"))] + decl
    # Same rule as `discover_repos()` (a dir carrying state.yaml) but keyed on repo_path.
    # NOT `discover_repos()` itself: it reads the module-global ECOSYSTEM_DIR, so reusing it
    # would make this one surface read a DIFFERENT repo than the other five whenever the two
    # disagree -- caught by test_health_ok_with_registered_repo, which monkeypatches exactly
    # that global. A check that takes repo_path must honour it for every surface it reads.
    #
    # Guarded like the other five (terra HIGH, 2026-08-01): an unguarded `iterdir()` raises
    # on a permission or I/O error and takes down the whole `audit.py health` run -- strictly
    # worse than this check failing, because it denies every OTHER check its verdict too.
    eco = Path(repo_path) / "ecosystem"
    try:
        surfaces["state-dirs"] = ({d.name for d in eco.iterdir()
                                   if d.is_dir() and (d / "state.yaml").exists()}
                                  if eco.is_dir() else set())
    except OSError as exc:
        return [Finding("membership_agreement", "fail",
                        f"membership surface ecosystem/<repo>/ could not be read: {exc!r}"
                        .replace("|", "/"))] + decl

    return [Finding("membership_agreement", status, evidence.replace("|", "/"))
            for status, evidence in classify_membership(ADR104_FLEET_DECLARATION, surfaces)] + decl


# rule: seal-journal-spine-anchor
def check_journal_spine_anchor(repo_path: Path) -> list[Finding]:
    """ADR-85 amendment 2026-08-03 §A8 / FR4 — the audit BACKSTOP for the pre-push hard leg.

    Walks `git log --first-parent main` and asserts every spine entry AT OR ABOVE the ADR's
    dated disposition floor is anchored by a JOURNAL entry. **A gap is a FAIL, not a WARN**,
    and that is load-bearing rather than stylistic: a WARN is dispositionable, and a
    dispositionable backstop cannot be the thing that makes `git push --no-verify` non-silent.
    The escape stays legitimate; it just stops being invisible.

    The anchoring predicate is imported from `journal_anchor` -- the SAME module the pre-push
    organ uses -- so the gate and its backstop cannot drift about what "anchored" means.
    Predicate (§A7): a spine entry is anchored when JOURNAL names >=1 SHA the entry
    INTRODUCED, never the entry's own SHA (a merge cannot name its own hash).

    The floor is READ FROM THE RATIFIED ADR, never hardcoded and never re-derived here
    (FR4). A floor living in a Python literal can be widened in a commit that reads like a
    refactor; widening it in the ADR is a visible governance act. An unreadable/unparseable
    floor is a FAIL, not a pass -- an unknown exemption boundary is not a clean one.

    HUB-ONLY by repo identity: ADR-85's floor lives in this repo's ADR and consumers carry
    neither it nor this JOURNAL shape, so scanning them would manufacture a fleet gap (the
    enforcement-organs-are-not-homogeneous class). Read-only (Layer-2).
    """
    if not _is_hub(repo_path):
        return [_na("journal_spine_anchor", "NOT-APPLICABLE",
                        "hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned")]
    try:
        import journal_anchor as _ja
        floor = _ja.floor_sha(repo_path)
        journal = _ja.journal_text(repo_path)
        gaps = _ja.unanchored_on_spine(repo_path, "main", floor, journal)
    except Exception as exc:  # noqa: BLE001 -- FR6: an error is never a silent pass
        return [Finding("journal_spine_anchor", "fail",
                        f"backstop could not complete ({exc!r}) -- an unknown anchoring "
                        "state is not a clean one (ADR-85 §A6)".replace("|", "/"))]
    if gaps:
        named = "; ".join(_ja.describe(repo_path, s) for s in gaps[:5])
        more = f" (+{len(gaps) - 5} more)" if len(gaps) > 5 else ""
        return [Finding("journal_spine_anchor", "fail",
                        f"{len(gaps)} first-parent spine entry(ies) above the disposition "
                        f"floor {floor[:9]} carry no JOURNAL anchor: {named}{more}"
                        .replace("|", "/"))]
    return [Finding("journal_spine_anchor", "pass",
                    f"every first-parent spine entry above the ADR-85 disposition floor "
                    f"{floor[:9]} is JOURNAL-anchored")]


def check_preflight_backlog_ids(repo_path: Path) -> list[Finding]:
    """[#483] R3 — ADVISORY leg: a BACKLOG `kill-candidates:` VALUE naming a non-open row.

    WARN-TIER BY RULING, never FAIL. R3 defers hard-gating pending measured evidence — zero
    false positives over two consecutive windows, reported at each seal — because the leg's
    predecessor flagged 11/11 correct historical citations on its first production run. A gate
    wired on that behaviour REDs every handoff bundle by construction. Promotion is a separate
    decision that arrives with data; this leg exists to produce that data.

    SCOPE is the assertion-role surface R2 defines in-repo, and it is deliberately narrow. A
    `kill-candidates:` value claims the named row is OPEN — you cannot kill a dead row. Every
    other `[#id]` in a BACKLOG row (`refs`, the reason prose after the em-dash) cites related
    work INCLUDING closed rows by design, and `docs/audits/`, `docs/handoffs/`, JOURNAL and
    LESSONS are citation-role wholesale. Measured on the live corpus, widening this to intake /
    protocols / ADRs would fire ~255 day-one flags, all narration.

    The role predicates are IMPORTED from `preflight_contract`, never restated, so the tool and
    this leg cannot drift into disagreeing about what an assertion is.

    DEPENDENCY THIS LEG RESTS ON, named so removing it cannot silently blind the leg: it reads
    the GENERATED `BACKLOG.md`, which is sound ONLY because currency is asserted mechanically
    elsewhere — `gen_task_tree.py --check` (and the handoff bundle's P0a probe). If that
    currency check is ever dropped, this leg starts measuring a stale view of the backlog and
    will keep reporting clean while doing it.

    HONEST LIMIT (R3's named gap): this verifies id-LIVENESS of assertions, not correctness of
    PLACEMENT. A citation on the wrong line still passes. Hard enforcement must not claim
    otherwise.
    """
    name = "preflight_backlog_ids"
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only — BACKLOG.md kill-candidates assertions are a hub surface")]
    try:
        try:
            from scripts import preflight_contract as _pf
        except ImportError:
            import preflight_contract as _pf

        backlog = Path(repo_path) / "BACKLOG.md"
        if not backlog.exists():
            return [Finding(name, "warn", "no BACKLOG.md — nothing to scan")]
        text = backlog.read_text(encoding="utf-8", errors="replace")
        open_ids = set(re.findall(r"(?m)^- \[#(\d+)\]", text))
        stale: list[str] = []
        for line in text.splitlines():
            if not _pf._BACKLOG_ROW.match(line):
                continue
            # EVERY delimited kill-candidates value, via the shared span helper — a row may
            # carry more than one field, and stopping at the first hid a real stale assertion
            # behind an earlier benign one (terra HIGH 2026-08-04).
            spans = _pf.kill_candidate_value_spans(line)
            if not spans:
                continue
            row = re.match(r"- \[#(\d+)\]", line).group(1)
            for start, end in spans:
                for cited in re.findall(r"#(\d+)", line[start:end]):
                    if cited not in open_ids:
                        stale.append(f"[#{row}] -> #{cited}")
        if stale:
            named = ", ".join(stale[:5])
            more = f" (+{len(stale) - 5} more)" if len(stale) > 5 else ""
            return [Finding(name, "warn",
                            f"{len(stale)} kill-candidates assertion(s) name a non-open row: "
                            f"{named}{more} — advisory per the [#483] ruling R3"
                            .replace("|", "/"))]
        return [Finding(name, "pass",
                        "every kill-candidates assertion names an open row")]
    except Exception as exc:  # noqa: BLE001 — advisory leg: never wedge a gate on its own input
        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]


# NO `# rule:` MARKER, deliberately, until [#499]: the rule this leg embodies is not yet
# written in a living doc, so a marker here would point at nothing and register as a
# code_orphan. The leg carries a TEMPORARY exemption in ecosystem/doc-code-edge.yaml that
# expires with [#499], where the PLAYBOOK rule lands and the marker is reinstated.
# [#480] P3 ruling (2026-08-05). Shape (b): ONE canonical machine-parseable header. Measured
# before the grammar was ruled -- across all 108 codex artifacts `Branch` appears 99x, `HEAD`
# 97x, and a tally line ZERO times -- so this codifies what already exists and adds one line.
_REVIEW_RULING_DATE = "2026-08-05"
_REVIEW_CODE_SUFFIXES = (".py", ".ps1")
# NO bare directory-prefix rule (terra HIGH, 2026-08-05, measured): OR-ing `scripts/`,
# `deploy/`, `tests/`, `plugins/` against the suffix rule made 43 tracked non-code files
# code-impact -- `plugins/tier1-lifecycle/commands/ship.md`, `INSTALL.md`,
# `deploy/release-v1.3.x-contract.md`. A docs-only merge touching one would have WARNed, and
# false WARNs corrupt the very zero-false-positive evidence bar [#499] is gated on.
#
# The reviewer's proposed fix -- require suffix AND prefix -- is WRONG HERE and was not taken:
# 3 tracked code files live outside those directories (`ecosystem/schema/desired_state.py`,
# `ecosystem/schema/__init__.py`, `.claude/skills/verify/verify.py`), so it would trade false
# positives for false NEGATIVES on real code. Suffix-anywhere + exact paths has neither.
# Consequence accepted and named: a non-.py/.ps1 behavioral file (a deploy manifest, a carried
# plugin asset) is NOT code-impact today. Widening is a ruling, never a sweep.
# EXACT-PATH members (operator amendment 2026-08-05), deliberately not a `.yaml` sweep: the
# tight rule would miss the two files where THIS window's enforcement defects actually live
# ([#498] and the [#497] fold are both stale/inert carried pre-commit declarations), while a
# sweep would drag in `ecosystem/*.yaml` data files and manufacture WARNs on data-only merges.
# Further path additions arrive BY RULING, never by widening this tuple in passing.
_REVIEW_CODE_EXACT = (".pre-commit-hooks.yaml", ".pre-commit-config.yaml")
_REVIEW_TALLY_RE = re.compile(r"(?m)^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b")
# The canonical TITLE is what makes a doc a review artifact -- a Branch/HEAD field alone does
# NOT (terra HIGH, 2026-08-05, measured): 13 tracked non-review audit docs carry a `**Branch:**`
# field, so field-presence alone would let a memo satisfy coverage and make the pass evidence
# overstate that a review happened. Measured discrimination: 0 of those 13 carry this title,
# and the review wrapper emits it on every run.
_REVIEW_TITLE_RE = re.compile(r"(?m)^# Codex Review\b")
# UTC epoch, not a timezone-bearing calendar date (terra HIGH, 2026-08-05). `%cs` renders in
# each commit's OWN timezone, so a merge near midnight could fall either side of the ruling
# date depending on where it was authored. `%ct` is a UTC instant; the cutoff is UTC midnight
# of the ruling date. Deterministic rather than ambient -- an evidence bar cannot rest on a
# boundary that moves with the committer's clock.
_REVIEW_CUTOFF_EPOCH = int(datetime(2026, 8, 5, tzinfo=timezone.utc).timestamp())
_REVIEW_BRANCH_RE = re.compile(r"(?m)^\*\*Branch:\*\*[ \t]*`?([^`\s]+?)`?[ \t]*$")
_REVIEW_HEAD_RE = re.compile(r"(?m)^\*\*HEAD:\*\*[ \t]*`?([0-9a-f]{7,40})`?")
_REVIEW_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")


def _review_is_code_impact(paths: list[str]) -> bool:
    """True when >=1 changed path is a code surface under the ruled predicate."""
    return any(p in _REVIEW_CODE_EXACT or p.endswith(_REVIEW_CODE_SUFFIXES) for p in paths)


def check_review_artifact_coverage(repo_path: Path) -> list[Finding]:
    """[#480] P3 -- ADVISORY leg: a code-impact merge carrying no linked review artifact.

    THE GAP: the 2026-08-02 W2 report recorded "terra review: zero findings on both arcs"
    while NO artifact existed anywhere. The claim was never refuted -- it was UNFALSIFIABLE,
    and nothing in the repo could tell a real review from a remembered one.

    WARN-TIER BY RULING, never a hard verdict. The P3 ruling is LAYERED: this advisory leg
    now, the hard pre-push leg DEFERRED behind an evidence bar of zero false positives over
    two consecutive windows, reported at each seal. This leg exists to produce that data.
    The property is asserted structurally by the test suite (no status literal for the hard
    verdict appears in this function), because an observational check only proves such a
    path was not REACHED -- which is exactly what a latent one looks like.

    FORWARD-ONLY from the ruling date. Of the 16 window artifacts only 3 carried a machine
    readable tally and 9 matched no recognised shape; those are immutable records, so a leg
    that reached backwards would demand retro-editing precisely what the ruling forbids
    touching. The date filter is the mechanism that makes "never retro-edited" true.

    LINKAGE IS TWO-LEGGED, either satisfying: by BRANCH (the artifact names the branch in the
    merge subject) or by an in-range HEAD (the artifact names a commit the merge introduced).
    The HEAD leg covers a review whose branch was renamed; the BRANCH leg covers a review that
    ran BEFORE a rebase, whose recorded SHA the rebase then rewrote out of the range. An
    artifact naming neither is not evidence for this merge -- otherwise one stale file in
    docs/audits/ would silence the whole leg.

    NAMED LIMITS OF THE LINKAGE, all three surfaced by review rather than discovered later:
      * The BRANCH leg reads a `Merge branch '<x>'` subject, which is the only shape
        core-invariant #5 permits on this spine (`block_ff_push` refuses the rest). A SQUASH
        merge carries no such subject AND its pre-squash SHA is not in `introduced()`, so it
        would WARN despite a real review. That is a false positive this leg does not prevent;
        it is bounded to a merge shape the repo's own gate already refuses.
      * BRANCH linkage is name-based, so REUSING a branch name for a later, unreviewed merge
        lets the earlier artifact cover it. Accepted deliberately: the alternative (full-SHA
        only) breaks the pre-rebase case the leg exists to tolerate.
      * HEAD linkage prefix-matches an abbreviation (>=7 hex). A collision would have to land
        inside the merge's OWN introduced set to mislink, which bounds it sharply, but it is
        not impossible.
    Each of these makes the leg MISS or over-credit; none makes it fail closed on real work.
    They are the reason the hard flip ([#499]) is gated on measured false positives rather
    than on this docstring's confidence.

    Reuses `journal_anchor`'s spine walk and `introduced()` rather than restating them, so
    this leg and the ADR-85 organs cannot drift about what a spine entry is or what a merge
    brought in -- the same anti-drift discipline block_ff_push and the backstop already share.

    HUB-ONLY by repo identity: the codex-review convention is a hub practice (108 artifacts
    here, none in a consumer), so scanning consumers would manufacture a fleet gap -- the
    enforcement-organs-are-not-homogeneous class. Read-only (Layer-2).

    HONEST LIMIT: this verifies an artifact EXISTS, is LINKED, and carries a PARSEABLE tally.
    It cannot verify the review happened, was competent, or that the tally is truthful -- a
    fabricated header passes. It converts an unfalsifiable claim into a checkable one; it does
    not make it a true one. The predicate also does not see a code change arriving through a
    path outside the tuples above; widening is a ruling, not a sweep.
    """
    name = "review_artifact_coverage"
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only -- the codex-review artifact convention is a hub practice")]
    try:
        try:
            from scripts import journal_anchor as _ja
        except ImportError:
            import journal_anchor as _ja

        root = Path(repo_path)
        artifacts = []
        audits = root / "docs" / "audits"
        if audits.is_dir():
            for p in sorted(audits.glob("*.md")):
                txt = p.read_text(encoding="utf-8", errors="replace")
                branch_m = _REVIEW_BRANCH_RE.search(txt)
                head_m = _REVIEW_HEAD_RE.search(txt)
                if not _REVIEW_TITLE_RE.search(txt) or not (branch_m or head_m):
                    continue          # not a review artifact -- an index, a memo, a report
                artifacts.append({
                    "branch": branch_m.group(1) if branch_m else None,
                    "head": head_m.group(1) if head_m else None,
                    "tally": bool(_REVIEW_TALLY_RE.search(txt)),
                    "file": p.name,
                })

        unlinked: list[str] = []
        untallied: list[str] = []
        scanned = 0
        # BATCHED date lookup -- one git call for the whole spine, not one PER ENTRY. The
        # per-entry form cost 236s on this repo's 1317-entry spine, and this leg runs inside
        # `audit-health`, a PRE-COMMIT gate: it would have added ~4 minutes to every commit in
        # the repo. Measured, not estimated. `spine_entries` still supplies the authoritative
        # entry list (shared --first-parent definition); this map only annotates it with dates.
        spine_dates: dict[str, int] = {}
        for ln in _ja._git(root, "log", "--first-parent", "--format=%H %ct", "main").splitlines():
            sha_part, _, date_part = ln.strip().partition(" ")
            if sha_part and date_part.strip().isdigit():
                spine_dates[sha_part] = int(date_part.strip())
        for sha in _ja.spine_entries(root, "main"):
            # Absent from the map is NOT treated as in-scope: a date we could not read is an
            # unknown, and an unknown must not silently become a WARN against a merge that may
            # predate the ruling. The pairing is one walk, so a miss means git disagreed with
            # itself -- surfaced by the outer handler if it matters, never guessed at here.
            if spine_dates.get(sha, 0) < _REVIEW_CUTOFF_EPOCH:
                continue
            parents = _ja._git(root, "rev-list", "--parents", "-n", "1", sha).split()
            if len(parents) < 2:
                continue              # root commit: no first parent to diff against
            changed = [ln.strip() for ln
                       in _ja._git(root, "diff", "--name-only", parents[1], sha).splitlines()
                       if ln.strip()]
            if not _review_is_code_impact(changed):
                continue
            scanned += 1
            subject = _ja._git(root, "log", "-1", "--format=%s", sha).strip()
            subject_m = _REVIEW_MERGE_SUBJECT_RE.match(subject)
            branch = subject_m.group(1) if subject_m else None
            brought = set(_ja.introduced(root, sha))
            linked = None
            for art in artifacts:
                if branch and art["branch"] == branch:
                    linked = art
                    break
                if art["head"] and any(c.startswith(art["head"]) for c in brought):
                    linked = art
                    break
            if linked is None:
                unlinked.append(f"{sha[:8]} {branch or subject[:40]}")
            elif not linked["tally"]:
                untallied.append(f"{sha[:8]} -> {linked['file']}")

        deferred = ("advisory per the [#480] P3 ruling; the hard pre-push leg is deferred "
                    "pending 0 false positives over two consecutive windows")
        out: list[Finding] = []
        if unlinked:
            named = ", ".join(unlinked[:5])
            more = f" (+{len(unlinked) - 5} more)" if len(unlinked) > 5 else ""
            out.append(Finding(name, "warn",
                               f"{len(unlinked)} code-impact merge(s) since "
                               f"{_REVIEW_RULING_DATE} carry no linked review artifact: "
                               f"{named}{more} -- {deferred}".replace("|", "/")))
        if untallied:
            named = ", ".join(untallied[:5])
            more = f" (+{len(untallied) - 5} more)" if len(untallied) > 5 else ""
            out.append(Finding(name, "warn",
                               f"{len(untallied)} linked artifact(s) carry no parseable "
                               f"**Tally:** line: {named}{more} -- persistence is not "
                               f"machine-auditability; {deferred}".replace("|", "/")))
        if not out:
            out.append(Finding(name, "pass",
                               f"{scanned} code-impact merge(s) since {_REVIEW_RULING_DATE} "
                               f"each carry a linked review artifact with a parseable tally"))
        return out
    except Exception as exc:  # noqa: BLE001 -- advisory leg: never wedge a gate on its own input
        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]


ALL_CHECKS = [
    check_vision_md,
    check_adr38_baseline,
    check_claude_md,
    check_dot_prefix_discipline,
    check_canonical_md_visibility,
    check_workspace_settings,
    # check_mermaid_theme_directive retired 2026-07-05 (ADR-51 amendment — LLM-first)
    check_handoff_bundle_structure,
    check_canonical_freshness,
    check_no_sibling_orphans,
    check_stale_worktrees,   # [#505] batch hygiene — WARN-tier by ruling (ADR-110 §1 item 4)
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
    check_residual_completeness,
    check_deployed_methodology_version,
    check_enforcement_coverage,
    check_undeclared_edges,
    check_doc_code_coverage_drift,
    check_import_edges,
    check_fleet_parity,   # [#337] blocking #328 fleet-parity gate (was informational)
    check_routine_consumers,   # [#419]/ADR-105 activation gate; scope = marked rows only
    check_silent_rule_ratchet,   # [#436] D4 ratchet — gates GROWTH of the silent-rule pool
    check_task_tree_coherence,   # [#433] C1 — arms gen_task_tree --check as a gate
    check_intake_tree_coherence,   # [#383] wave 1 — arms gen_intake_tree --check (ADR-109 §4)
    check_boot_byte_budget,   # [#446] A10 item 2 / R4 — the gate half of the split enforcement
    check_fleet_audit_replication,   # [#460] — ADR-80's durable record must exist off this disk
    check_membership_agreement,   # [#462] — ADR-104's declaration vs every repo-keyed surface
    check_journal_spine_anchor,   # ADR-85 amendment 2026-08-03 §A8/FR4 — backstop for the
                                  # pre-push hard leg; makes `--no-verify` non-silent
    check_preflight_backlog_ids,   # [#483] R3 — ADVISORY (WARN-tier by ruling); hard-gating is
                                   # deferred pending 0 false positives over two windows
    check_review_artifact_coverage,   # [#480] P3 — ADVISORY (WARN-tier by ruling);
                                     # the hard pre-push leg is deferred behind a
                                     # two-window zero-false-positive evidence bar
]


def detect_unconditionally_inert_checks(
    repo_paths: dict[str, Path],
    checks: "Sequence[Callable[[Path], list[Finding]]] | None" = None,
) -> list[Finding]:
    """[#465] leg 4 / FR-2 — WARN for any check that can only ever return SUBJECT-ABSENT.

    THE CLASS, NOT THE INSTANCE. `handoff_tag_canonicity` emitted a verdict every day for two
    spec generations after its subject stopped existing, and nothing noticed: 285 n/a vs 5
    pass across every `ecosystem/*/history/*.md` on `origin/automation/fleet-audit`, and those
    five passes were the leg-1 skip-as-pass defect. Deleting that one check would have repaired
    the instance and left the next one to die exactly as invisibly. This asks the question
    instead.

    SELF-ENUMERATING over `ALL_CHECKS`, never a hand-maintained roster (the leg-2/3 precedent,
    and FR-4: a "known-inert" list would reproduce the registry sprawl ADR-109 dissolves).
    `checks` is a test seam only; `None` late-binds the live registry so a member added
    tomorrow is covered with no edit here.

    INERT means, across every supplied repo: every result is `n/a`, AND at least one of them is
    SUBJECT-ABSENT. A check that is merely NOT-APPLICABLE everywhere is NOT inert — that is the
    FR-7 consumer-safety line, and getting it wrong is exactly the D1 defect the wave-1 producer
    lane shipped (it would have manufactured a fleet gap on corp-monorepo and ai-council).

    POSTURE (FR-3): WARN, never FAIL — it informs, it does not become a new way for the gate to
    go red on doc drift. An unclassified n/a, a check returning nothing, or a check that raises
    is itself a loud WARN: a detector that cannot see must not report clean.

    Read-only (FR-4 / ADR-28, ADR-36): it invokes read-only checks and writes nothing.

    Honest limits — it does NOT catch: a check that wrongly returns `pass`, a check whose
    assertions are vacuous, subject-absence recorded outside the `_na` prefix, or a check that
    is inert only on the repos it was not run against.
    """
    out: list[Finding] = []
    by_check: dict[str, dict[str, list[Finding]]] = {}
    for check in (ALL_CHECKS if checks is None else checks):
        name = getattr(check, "__name__", str(check)).removeprefix("check_")
        for repo_name, repo_path in repo_paths.items():
            try:
                returned = list(check(Path(repo_path)))
            except Exception as exc:  # noqa: BLE001 -- FR-3: surface, never swallow
                out.append(Finding("writer_integrity", "warn",
                                   f"{name}: could not be evaluated for {repo_name}: {exc!r}"
                                   .replace("|", "/")))
                continue
            # Register the check even when it returned NOTHING: the coverage rule below turns
            # the missing repo into a WARN. Skipping it entirely would make a check that
            # reports nothing disappear from the detector's view — silence about a gap, which
            # is the failure mode this leg exists to remove.
            slot = by_check.setdefault(name, {})
            if returned:
                slot[repo_name] = returned
    return out + classify_inert_checks(by_check, sorted(repo_paths))


def classify_inert_checks(by_check: "dict[str, dict[str, list[Finding]]]",
                          repo_names: "Sequence[str]") -> list[Finding]:
    """THE RULE, defined once, over findings that have ALREADY been computed.

    Extracted so the production path costs nothing (terra HIGH r1, 2026-08-04). `cmd_run` has
    just executed every check against every repo; re-running them inside the detector would
    double a whole fleet audit. Both callers share this function, so the daily and the test seam
    cannot drift about what "inert" means -- the single-definition discipline `journal_anchor`
    uses for the ADR-85 predicate.

    COVERAGE IS PART OF THE RULE (terra HIGH r2, 2026-08-04). `by_check` is keyed check -> repo,
    not check -> flat findings, because "inert" is a claim about the WHOLE fleet: concluding it
    from a subset would let one unavailable or half-audited repo retire a check that is alive
    elsewhere. A check missing a result from a repo that WAS evaluated is reported as incomplete
    coverage and explicitly NOT judged -- silence about a gap is the failure mode this whole leg
    exists to remove.

    `repo_names` must be the repos actually evaluated; callers exclude unavailable ones.
    """
    out: list[Finding] = []
    expected = set(repo_names)
    where = ", ".join(sorted(expected))
    for name in sorted(by_check):
        per_repo = by_check[name]
        missing = expected - set(per_repo)
        if missing:
            out.append(Finding("writer_integrity", "warn",
                               f"{name}: no result from {', '.join(sorted(missing))}; coverage is "
                               "incomplete so inertness was NOT judged -- a check that reports "
                               "nothing cannot be read as clean ([#465] leg 4)"))
            continue
        results = [f for fs in per_repo.values() for f in fs]
        if any(f.status != "n/a" for f in results):
            continue  # it can say something other than n/a somewhere -- not inert
        reasons = [_na_reason(f) for f in results]
        if any(r is None for r in reasons):
            out.append(Finding("writer_integrity", "warn",
                               f"{name}: emitted an n/a with no machine-readable reason -- it "
                               "cannot be told apart from a dead check ([#465] leg 4, FR-1)"))
            continue
        if _NA_SUBJECT_ABSENT not in reasons:
            continue  # NOT-APPLICABLE everywhere is a correct skip, not an inert check
        out.append(Finding("writer_integrity", "warn",
                           f"{name}: UNCONDITIONALLY INERT -- every result across [{where}] is "
                           f"n/a and its subject is absent, so the check can never fire. Fix its "
                           f"subject or retire it ([#465] leg 4)"))
    return out


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
    out.write_text(content, encoding="utf-8", newline="\n")
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
    with open(ECOSYSTEM_INDEX, "w", encoding="utf-8", newline="\n") as fh:
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


_PUSH_TIMEOUT_S = 120


def _push_routine_branch(repo_path: Optional[Path] = None) -> tuple[bool, str]:
    """[#460] — replicate `automation/fleet-audit` to origin. Returns (ok, detail).

    PLACEMENT: called by `_commit_routine_outputs` immediately after `update-ref`, so the
    push belongs to the ACT THAT CREATES THE COMMIT rather than to a separate scheduler leg.
    That is the whole lesson of [#460]: the previous push was a separate, manual organ, so it
    could die without the writer noticing, and it did -- for 16 days. One act, one failure
    surface. (The repo's own ratified line: "push is part of the act it verifies".)

    LOUD ON FAILURE, at ERROR: the surrounding writer is deliberately fail-soft, logging
    WARNs for its ordinary skips, so a replication failure logged at WARN would be
    indistinguishable from "nothing to record today" -- silent success theater, which is the
    defect class itself.

    NEVER RAISES: loud must not mean fatal. Breaking the nightly routine to report a failed
    push would trade a replication gap for a total outage. Persistence is carried by
    `check_fleet_audit_replication`, which sees the lag on every subsequent run.

    Non-interactive and bounded: GIT_TERMINAL_PROMPT=0 plus a timeout, because this runs
    unattended under Task Scheduler where a credential prompt would hang the routine forever.
    """
    repo = Path(repo_path) if repo_path is not None else _REPO_ROOT
    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), "push", "origin",
             f"refs/heads/{_AUTOMATION_BRANCH}:refs/heads/{_AUTOMATION_BRANCH}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env, timeout=_PUSH_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        detail = f"push timed out after {_PUSH_TIMEOUT_S}s"
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)
    except OSError as exc:
        detail = f"could not run git push: {exc!r}"
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)

    if p.returncode != 0:
        detail = (p.stderr or p.stdout or "no output").strip().replace("\n", " ")[:400]
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)
    return (True, "pushed")


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
        # [#460]: the commit exists on ONE disk until this runs. Replication is part of the
        # act, not a follow-on chore — the follow-on chore is precisely what died in July.
        _push_routine_branch(repo)
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
    # [#465] leg 4 / FR-2: the inert-check detector must actually RUN in production -- a
    # detector nothing calls is a mechanism that reports nothing, which is the exact class this
    # leg was opened to remove (terra HIGH r1, 2026-08-04).
    #
    # It is fleet-scoped by construction (a check that is n/a here and firing there is alive),
    # so the hub's verdict cannot be written until every repo has been audited. ONLY the hub's
    # persistence is deferred: consumers still save-and-append as they complete, exactly as
    # before, so a later repo raising cannot lose earlier repos' durable progress (terra HIGH
    # r2 -- deferring everything silently changed that failure semantics). The hub is persisted
    # in a `finally`, so it survives that failure too, with whatever coverage was achieved.
    states = []
    hub_state = None
    try:
        for name in names:
            existing = load_state(name)
            rp = resolve_repo_path(name, existing.path if existing else None)
            state = audit_repo(name, rp, run_date)
            states.append(state)
            if state.name == HUB_REPO_NAME:
                hub_state = state          # held back for the fleet-scoped detector
            else:
                save_state(state)
                append_history(state, run_date)
    finally:
        if hub_state is not None:
            # An unavailable repo contributes no check results; judging inertness against it
            # would let one missing tree retire a check that is alive everywhere else.
            evaluated = [s for s in states
                         if not any(f.check_name == "availability" and f.status == "unavailable"
                                    for f in s.findings)]
            by_check: dict[str, dict[str, list[Finding]]] = {}
            for s in evaluated:
                for f in s.findings:
                    by_check.setdefault(f.check_name, {}).setdefault(s.name, []).append(f)
            # WARNs attach to the HUB only: this is hub-owned machinery, and writing one onto a
            # consumer would manufacture exactly the fleet gap FR-7 forbids.
            hub_state.findings.extend(
                classify_inert_checks(by_check, [s.name for s in evaluated]))
            save_state(hub_state)
            append_history(hub_state, run_date)

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
        rp = Path(repo_path).resolve()  # explicit override wins over the resolver
    else:
        rp = resolve_repo_path(name, existing.path if existing else None)
        if not existing:
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
