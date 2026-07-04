"""Tests for the Informant Organ (scripts/enforcement_coverage.py) — Stage-2 enforcement-transfer.

The load-bearing proof (closure contract): the reporter measures whether enforcement FIRES, not
whether files are present. The two tests that establish it are
``test_present_but_inert_stop_hook_reports_absent`` (a Stop hook that is a locate CANDIDATE but
behaviourally inert -> verdict ``absent``, NOT ``enforcing-local``) paired with
``test_blocking_stop_hook_reports_enforcing_local`` (the real backpressure script -> ``enforcing-local``).

Hermetic (Layer-1): every fixture is a throwaway git repo built in ``tmp_path``; fire_test clones it
(own .git, plain-delete teardown) exactly as floor_conformance does. No network, no real consumers.
The session_end + reconciled fire_tests need no pre-commit; the canonical_freshness fire_test does
(skipif-guarded, mirroring tests/test_floor_conformance.py).
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))
sys.path.insert(0, str(_REPO_ROOT / "deploy"))

import audit  # noqa: E402
import enforcement_coverage as ec  # noqa: E402

_HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not None
_REAL_SEB = (_REPO_ROOT / "scripts" / "session_end_backpressure.py").read_text(encoding="utf-8")

_INERT_STOP = (
    "import json, sys\n"
    'print(json.dumps({"hookSpecificOutput": {"hookEventName": "Stop", '
    '"additionalContext": "inert nudge (never blocks)"}}))\n'
    "sys.exit(0)\n"
)


# ---------------------------------------------------------------------------
# git fixture helpers.
# ---------------------------------------------------------------------------


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def _init_consumer(root: Path, files: dict[str, str]) -> Path:
    """A throwaway consumer git repo with an initial commit of ``files``."""
    root.mkdir(parents=True, exist_ok=True)
    if _git(["init", "-q", "-b", "main"], root).returncode != 0:
        _git(["init", "-q"], root)
    for cfg in (["core.autocrlf", "false"], ["user.email", "t@example.com"],
                ["user.name", "Test"], ["commit.gpgsign", "false"]):
        _git(["config", *cfg], root)
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
    _git(["add", "-A"], root)
    _git(["commit", "-q", "-m", "init"], root)
    return root


def _stop_settings(command: str) -> str:
    return json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": command}]}]}})


def _cell(cells, organ_id):
    return next(c for c in cells if c.organ_id == organ_id)


# ---------------------------------------------------------------------------
# THE load-bearing proof: firing, not presence (session_end_backpressure).
# ---------------------------------------------------------------------------


def test_present_but_inert_stop_hook_reports_absent(tmp_path):
    """A Stop hook that is a locate CANDIDATE (a session_end_backpressure look-alike) but exits 0
    with additionalContext must be reported ``absent`` — the fire_test, not presence, decides."""
    root = _init_consumer(tmp_path / "inert", {
        "JOURNAL.md": "# Journal\n\n- work happened\n",
        ".claude/session_end_backpressure.py": _INERT_STOP,  # look-alike name -> candidate
        ".claude/settings.json": _stop_settings(
            'python "$CLAUDE_PROJECT_DIR/.claude/session_end_backpressure.py"'),
    })
    # locate MUST flag it a candidate (so we are genuinely exercising the fire path, not locate).
    assert ec._seb_candidate_command(root) is not None
    cell = _cell(ec.evaluate_full(root), "session_end_backpressure")
    assert cell.verdict == ec.ABSENT
    assert cell.fired is False


def test_blocking_stop_hook_reports_enforcing_local(tmp_path):
    """The real backpressure script, wired as the Stop hook, blocks unanchored work -> enforcing-local."""
    root = _init_consumer(tmp_path / "enforcing", {
        "JOURNAL.md": "# Journal\n\n- prior session\n",
        "scripts/session_end_backpressure.py": _REAL_SEB,
        ".claude/settings.json": _stop_settings(
            'python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'),
    })
    cell = _cell(ec.evaluate_full(root), "session_end_backpressure")
    assert cell.verdict == ec.ENFORCING_LOCAL, cell.evidence
    assert cell.fired is True


# ---------------------------------------------------------------------------
# locate exclusions (no false positives).
# ---------------------------------------------------------------------------


def test_locate_excludes_propose_closures_plugin(tmp_path):
    """enabledPlugins:tier1-lifecycle + a Stop hook running propose_closures is NON-blocking by
    design and must NOT be a session_end_backpressure candidate."""
    root = _init_consumer(tmp_path / "plugin", {
        "JOURNAL.md": "# Journal\n",
        ".claude/settings.json": json.dumps({
            "enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True},
            "hooks": {"Stop": [{"hooks": [{"type": "command",
                      "command": "python plugin/propose_closures.py"}]}]},
        }),
    })
    assert ec._seb_candidate_command(root) is None
    assert _cell(ec.evaluate_static(root), "session_end_backpressure").verdict == ec.ABSENT


def test_absent_consumer_all_tier1_absent_and_toc_not_false_positive(tmp_path):
    """A consumer wiring ruff + toc-freshness + floor-hash-verify (but no organ gate): every
    Tier-1 organ is absent/n-a/hub-scoped, and toc-freshness does NOT read as canonical_freshness."""
    precommit = (
        "repos:\n"
        "  - repo: local\n"
        "    hooks:\n"
        "      - id: toc-freshness\n"
        "        name: ARCHITECTURE ToC freshness\n"
        "        entry: python toc_check.py\n"
        "      - id: floor-hash-verify\n"
        "        name: Verify CLAUDE-FLOOR matches sidecar\n"
        "        entry: python .claude/check_floor_hash.py\n"
        "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
        "    rev: v0.15.5\n"
        "    hooks:\n"
        "      - id: ruff\n"
    )
    root = _init_consumer(tmp_path / "absent", {
        "JOURNAL.md": "# Journal\n",
        ".pre-commit-config.yaml": precommit,
    })
    assert ec._freshness_candidate(root)[0] is False  # toc-freshness excluded
    cells = {c.organ_id: c.verdict for c in ec.evaluate_static(root)}
    assert cells["session_end_backpressure"] == ec.ABSENT
    assert cells["canonical_freshness"] == ec.ABSENT
    assert cells["reconciled_versions"] == ec.NA_NO_EDGES
    assert cells["doc_claims"] == ec.HUB_SCOPED
    assert cells["git_backlog_drift"] == ec.HUB_SCOPED


# ---------------------------------------------------------------------------
# Group B — hub-scoped verdict DEMONSTRATED (not source-read), despite an injected violation.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("organ", ["doc_claims", "git_backlog_drift"])
def test_group_b_hub_scoped_demonstrated_despite_violation(tmp_path, organ):
    """The Group-B guard is DEMONSTRATED: invoked off-hub with a real violation present, the organ
    still returns the hub-only PASS -> the reporter classifies hub-scoped from behavior, not a
    source-read of the `if repo_path != _REPO_ROOT` guard (architect ratification 2026-07-03)."""
    root = tmp_path / "consumer"
    root.mkdir()
    # Inject violations that WOULD trip each organ on the hub.
    (root / "BACKLOG.md").write_text(
        "# Backlog\n\n- [#999] a task closed in history but never removed\n",
        encoding="utf-8")
    (root / "ARCHITECTURE.md").write_text(
        "# Arch\n\n- audit: **3 registered checks** (wrong on purpose)\n", encoding="utf-8")

    # The demonstration: the organ short-circuits to pass off-hub DESPITE the violation.
    fn = getattr(audit, f"check_{organ}")
    findings = fn(root)
    assert findings and all(f.status == "pass" and "hub-only" in f.evidence for f in findings)

    # The reporter derives hub-scoped from that behavior.
    verdict, evidence = ec._demonstrate_hub_scoped(organ, root)
    assert verdict == ec.HUB_SCOPED
    assert "demonstrated" in evidence
    assert _cell(ec.evaluate_static(root), organ).verdict == ec.HUB_SCOPED


# ---------------------------------------------------------------------------
# reconciled_versions — n/a-no-edges vs applicable-and-fires.
# ---------------------------------------------------------------------------


def test_reconciled_no_edges_is_na(tmp_path):
    root = _init_consumer(tmp_path / "noedge", {"JOURNAL.md": "# Journal\n"})
    assert _cell(ec.evaluate_static(root), "reconciled_versions").verdict == ec.NA_NO_EDGES


def test_reconciled_applicability_flips_and_fires(tmp_path):
    """A consumer with a reconciled_with edge + a wired reconciled_versions gate: applicability flips
    to applicable and the fire_test proves the organ fires FAIL on a version mismatch."""
    spec = (_REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md").read_text(encoding="utf-8")
    dependent = ("---\n"
                 "reconciled_with: handoff-process@1.0\n"
                 "---\n# Dependent doc\n")
    precommit = (
        "repos:\n"
        "  - repo: local\n"
        "    hooks:\n"
        "      - id: reconciled-versions\n"
        "        name: coherence-spine reconciled_versions gate\n"
        "        entry: python reconcile_gate.py\n"
    )
    root = _init_consumer(tmp_path / "reconciled", {
        "JOURNAL.md": "# Journal\n",
        "protocols/HANDOFF_PROCESS.md": spec,
        "docs/dependent.md": dependent,
        ".pre-commit-config.yaml": precommit,
    })
    # applicable (edge present) + candidate (gate wired).
    assert ec._reconciled_applicability(root)[0] == "applicable"
    assert ec._reconciled_candidate(root)[0] is True
    cell = _cell(ec.evaluate_full(root), "reconciled_versions")
    assert cell.verdict == ec.ENFORCING_LOCAL, cell.evidence
    assert cell.fired is True


# ---------------------------------------------------------------------------
# canonical_freshness — fire_test (needs pre-commit, skipif-guarded).
# ---------------------------------------------------------------------------


def test_canonical_freshness_candidate_and_exclusions(tmp_path):
    root = _init_consumer(tmp_path / "freshcand", {
        ".pre-commit-config.yaml":
            "repos:\n  - repo: local\n    hooks:\n"
            "      - id: canonical-freshness\n"
            "        name: canonical_freshness last_reviewed gate\n"
            "        entry: python freshness_gate.py\n",
    })
    assert ec._freshness_candidate(root)[0] is True


@pytest.mark.skipif(not _HAS_PRECOMMIT, reason="pre-commit not installed — commit-time leg unavailable")
def test_canonical_freshness_fires_on_stale_stamp(tmp_path):
    """A wired canonical_freshness gate blocks a commit while a _FRESHNESS_FILES doc is A2-stale."""
    gate = (
        "import sys\n"
        f"sys.path.insert(0, r'{ec._SCRIPTS_DIR}')\n"
        "import audit\n"
        "from pathlib import Path\n"
        'bad = [f for f in audit.check_canonical_freshness(Path(".")) if f.status == "fail"]\n'
        'if bad:\n    print("canonical_freshness FAIL:", bad[0].evidence); sys.exit(1)\n'
        "sys.exit(0)\n"
    )
    precommit = (
        "repos:\n  - repo: local\n    hooks:\n"
        "      - id: canonical-freshness\n"
        "        name: canonical_freshness last_reviewed gate\n"
        "        entry: python freshness_gate.py\n"
        "        language: system\n"
        "        always_run: true\n"
        "        pass_filenames: false\n"
    )
    root = _init_consumer(tmp_path / "freshfire", {
        "CLAUDE.md": "---\nlast_reviewed: 2026-07-03\nversion: 1.0\n---\n# CLAUDE\nbody\n",
        "freshness_gate.py": gate,
        ".pre-commit-config.yaml": precommit,
    })
    cell = _cell(ec.evaluate_full(root), "canonical_freshness")
    assert cell.verdict == ec.ENFORCING_LOCAL, cell.evidence
    assert cell.fired is True


@pytest.mark.skipif(not _HAS_PRECOMMIT, reason="pre-commit not installed — commit-time leg unavailable")
def test_freshness_fire_isolates_from_unresolvable_relative_repo(tmp_path):
    """Mesh-carrier reachability DE-RISK (load-bearing): a consumer whose .pre-commit-config.yaml
    carries an UNRESOLVABLE relative `repo: ../x` ref — exactly ai-council's `repo: ../.dev-knowledge`,
    which is absent from the throwaway clone's parent — must STILL reach enforcing-local. pre-commit
    clones every repo in a config before running any hook, so a full-commit (or even a single-hook
    run against the full config) would fail on the missing sibling — a FALSE verdict. The fire
    isolates the consumer's own freshness hook under a minimal one-hook config. Uses the REAL
    deployed gate (scripts/canonical_freshness_gate.py)."""
    gate_src = (_REPO_ROOT / "scripts" / "canonical_freshness_gate.py").read_text(encoding="utf-8")
    precommit = (
        "repos:\n"
        "  - repo: ../this-sibling-does-not-exist\n"
        "    rev: v1.0.0\n"
        "    hooks: [{id: toc-freshness}]\n"
        "  - repo: local\n    hooks:\n"
        "      - id: canonical_freshness\n"
        "        name: canonical_freshness last_reviewed gate\n"
        "        entry: python scripts/canonical_freshness_gate.py\n"
        "        language: system\n"
        "        always_run: true\n"
        "        pass_filenames: false\n"
    )
    root = _init_consumer(tmp_path / "relref", {
        "CLAUDE.md": "---\nlast_reviewed: 2026-07-03\n---\n# CLAUDE\nbody\n",
        "scripts/canonical_freshness_gate.py": gate_src,
        ".pre-commit-config.yaml": precommit,
    })
    cell = _cell(ec.evaluate_full(root), "canonical_freshness")
    assert cell.verdict == ec.ENFORCING_LOCAL, cell.evidence
    assert cell.fired is True
    assert "isolation" in cell.evidence


@pytest.mark.skipif(not _HAS_PRECOMMIT, reason="pre-commit not installed — commit-time leg unavailable")
def test_freshness_fire_stales_a_quoted_last_reviewed(tmp_path):
    """Regression (ai-council, 2026-07-03): the FIRST _FRESHNESS_FILES doc (VISION.md) can carry a
    QUOTED `last_reviewed: "2026-06-02"` (valid YAML; the deployed gate parses it via yaml). The
    fire's stale-regex must match the quoted form AND target-selection must pick a STALEABLE doc —
    else canonical_freshness false-reports `absent` despite a correctly-deployed gate (the exact
    first live-fire miss). Uses the REAL gate; VISION.md is first in _FRESHNESS_FILES."""
    gate_src = (_REPO_ROOT / "scripts" / "canonical_freshness_gate.py").read_text(encoding="utf-8")
    precommit = (
        "repos:\n  - repo: local\n    hooks:\n"
        "      - id: canonical_freshness\n"
        "        name: canonical_freshness last_reviewed gate\n"
        "        entry: python scripts/canonical_freshness_gate.py\n"
        "        language: system\n        always_run: true\n        pass_filenames: false\n"
    )
    root = _init_consumer(tmp_path / "quoted", {
        "VISION.md": '---\nlast_reviewed: "2026-06-02"\n---\n# VISION\nbody\n',  # QUOTED
        "scripts/canonical_freshness_gate.py": gate_src,
        ".pre-commit-config.yaml": precommit,
    })
    cell = _cell(ec.evaluate_full(root), "canonical_freshness")
    assert cell.verdict == ec.ENFORCING_LOCAL, cell.evidence
    assert cell.fired is True


# ---------------------------------------------------------------------------
# Verdict vocabulary + audit leg posture.
# ---------------------------------------------------------------------------


def test_verdict_vocabulary(tmp_path):
    root = _init_consumer(tmp_path / "vocab", {"JOURNAL.md": "# Journal\n"})
    allowed = {ec.ENFORCING_LOCAL, ec.ABSENT, ec.HUB_SCOPED, ec.NA_NO_EDGES,
               ec.NA_NO_JOURNAL, ec.PRESENT_UNVERIFIED}
    for cell in ec.evaluate_static(root):
        assert cell.verdict in allowed, cell


def test_audit_leg_is_na_on_hub():
    findings = audit.check_enforcement_coverage(Path(audit._REPO_ROOT))
    assert len(findings) == 1
    assert findings[0].status == "n/a"


def test_audit_leg_never_fails_and_never_claims_enforcing_local(tmp_path):
    """The static leg emits only n/a and can NEVER report enforcing-local (it never clones/fires)."""
    root = _init_consumer(tmp_path / "leg", {"JOURNAL.md": "# Journal\n"})
    findings = audit.check_enforcement_coverage(root)
    assert len(findings) == 1
    assert findings[0].status == "n/a"
    # No organ verdict is enforcing-local on the static leg (verdicts render as `organ=verdict`).
    assert "=enforcing-local" not in findings[0].evidence
    # No pipe chars leak into the markdown-table-safe evidence contract.
    assert "|" not in findings[0].evidence


def test_static_path_reports_present_unverified_for_a_candidate(tmp_path):
    """A candidate organ on the STATIC path is present-unverified (not enforcing-local — the leg
    cannot license enforcing-local without a fire_test)."""
    root = _init_consumer(tmp_path / "cand", {
        "JOURNAL.md": "# Journal\n",
        "scripts/session_end_backpressure.py": _REAL_SEB,
        ".claude/settings.json": _stop_settings(
            'python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'),
    })
    cell = _cell(ec.evaluate_static(root), "session_end_backpressure")
    assert cell.verdict == ec.PRESENT_UNVERIFIED
    assert cell.fired is None


def test_tier2_carrier_state_mapping():
    """CarrierState -> Tier-2 presence label (present-and-wired / present-not-wired / absent)."""
    from contract import CarrierState
    assert ec._carrier_state_label(CarrierState.PRESENT_CORRECT) == ec.T2_PRESENT_WIRED
    assert ec._carrier_state_label(CarrierState.PRESENT_DRIFTED) == ec.T2_PRESENT_NOT_WIRED
    assert ec._carrier_state_label(CarrierState.PRESENT_WRONG_VERSION) == ec.T2_PRESENT_NOT_WIRED
    assert ec._carrier_state_label(CarrierState.ABSENT) == ec.T2_ABSENT


# ---------------------------------------------------------------------------
# Allowlist reader + schema validator ([#244] P4 — the "shape" leg; firing != shape).
# PURE: construct entries / read a file, never clone or fire. run_date is a param.
# ---------------------------------------------------------------------------

_WAIVABLE = {"hub-toc-hooks": True, "session-end-backpressure": False}


def _entry(component="hub-toc-hooks", reason="CLI repo has no TOC to gate",
           expiry="2999-01-01", review_date=None):
    return ec.AllowlistEntry(component=component, reason=reason,
                             expiry=ec._parse_date(expiry),
                             review_date=ec._parse_date(review_date), raw={})


def test_allowlist_valid_entry():
    status, _ = ec.validate_allowlist_entry(
        _entry(), run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_VALID


def test_allowlist_reasonless_is_invalid():
    status, _ = ec.validate_allowlist_entry(
        _entry(reason="  "), run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_NO_REASON


def test_allowlist_no_date_is_invalid():
    status, _ = ec.validate_allowlist_entry(
        _entry(expiry=None, review_date=None), run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_NO_DATE


def test_allowlist_expired_vs_run_date():
    status, _ = ec.validate_allowlist_entry(
        _entry(expiry="2026-01-01"), run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_EXPIRED


def test_allowlist_review_date_satisfies_the_time_box():
    """A future review_date (no expiry) is a valid time-box."""
    status, _ = ec.validate_allowlist_entry(
        _entry(expiry=None, review_date="2999-01-01"),
        run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_VALID


def test_allowlist_non_waivable_component_is_rejected():
    """A non-waivable component can NEVER be validly allowlisted (contract 2)."""
    status, _ = ec.validate_allowlist_entry(
        _entry(component="session-end-backpressure"),
        run_date="2026-07-04", waivable_policy=_WAIVABLE)
    assert status == ec.AL_REJECTED


def test_read_allowlist_absent_is_empty(tmp_path):
    assert ec.read_allowlist(tmp_path) == []


def test_read_allowlist_parses_entries(tmp_path):
    (tmp_path / ec.ALLOWLIST_REL).write_text(
        "sanctioned_divergences:\n"
        "  - component: hub-toc-hooks\n"
        "    reason: CLI repo has no ARCHITECTURE.md TOC to gate\n"
        "    review_date: 2999-01-01\n",
        encoding="utf-8")
    entries = ec.read_allowlist(tmp_path)
    assert len(entries) == 1
    assert entries[0].component == "hub-toc-hooks"
    assert entries[0].reason.startswith("CLI repo")
    assert entries[0].review_date == ec._parse_date("2999-01-01")
