"""Tests for the Informant Organ (scripts/enforcement_coverage.py) — Stage-2 enforcement-transfer.

The load-bearing proof (closure contract): the reporter measures whether enforcement FIRES, not
whether files are present. Since the ADR-85 amendment 2026-08-03 moved the teeth from the Stop
hook to pre-push, that proof runs against ``block_unanchored_push``:
``test_present_but_inert_anchor_hook_reports_absent`` (a pre-push hook that is a locate CANDIDATE
but behaviourally inert -> verdict ``absent``, NOT ``enforcing-local``) paired with
``test_anchor_gate_probe_distinguishes_installed_from_absent`` (the real organ -> ``enforcing-local``,
and — the part a pair of independent tests cannot pin — the two verdicts DIFFER).

Hermetic (Layer-1): every fixture is a throwaway git repo built in ``tmp_path``; fire_test clones it
(own .git, plain-delete teardown) exactly as floor_conformance does. No network, no real consumers.
The session_end + reconciled fire_tests need no pre-commit; the canonical_freshness fire_test does
(skipif-guarded, mirroring tests/test_floor_conformance.py).
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

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


def test_present_but_inert_anchor_hook_reports_absent(tmp_path):
    """A pre-push hook that is a locate CANDIDATE but behaviourally inert (exits 0 on an
    unanchored push) must be reported ``absent`` — the fire_test, not presence, decides.

    This is the load-bearing firing-not-presence proof, ported to the organ's new home. It
    was `test_present_but_inert_stop_hook_reports_absent` against a Stop look-alike; the
    Stop hook stopped being where the ADR-85 teeth live (amendment 2026-08-03 §A5), so the
    same proof now runs against an inert `block_unanchored_push`.
    """
    root = _anchor_organ_consumer(tmp_path / "inert")
    (root / "scripts" / "block_unanchored_push.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8", newline="\n")
    _git(["add", "-A"], root)
    _git(["commit", "-q", "-m", "replace the organ with an inert allow"], root)

    # locate MUST flag it a candidate (so we genuinely exercise the fire path, not locate).
    assert ec._anchor_hook(root) is not None
    cell = _cell(ec.evaluate_full(root), "session_end_backpressure")
    assert cell.verdict == ec.ABSENT
    assert cell.fired is False


def test_stop_hook_no_longer_enforces_after_the_adr85_amendment(tmp_path):
    """ADR-85 amendment 2026-08-03 §A5/FR5 — the Stop hook is ADVISORY IN FULL, so a repo
    wiring ONLY the Stop hook has NO ADR-85 coverage and must read ``absent``.

    Was `test_blocking_stop_hook_reports_enforcing_local`, which asserted ENFORCING_LOCAL on
    the strength of `{"decision":"block"}`. That block is gone by design: a Stop hook's unit
    is a model-turn boundary the host force-ends after N consecutive blocks, so it cannot
    carry teeth. The ADR-85 teeth now live at pre-push in `block_unanchored_push.py`.

    The pin this test carried — "the Stop hook does not enforce ADR-85" — is unchanged and
    still asserted here. What changed is WHY the cell reads absent: it is no longer a
    candidate that failed to fire (a stale probe pointed at the wrong organ), but a repo
    correctly measured as not having the hard leg installed at all. The evidence must say
    so, naming the Stop hook rather than silently ignoring it — a consumer reading this
    cell needs to know a Stop hook is wired and does not count.
    """
    root = _init_consumer(tmp_path / "stop-only", {
        "JOURNAL.md": "# Journal\n\n- prior session\n",
        "scripts/session_end_backpressure.py": _REAL_SEB,
        ".claude/settings.json": _stop_settings(
            'python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'),
    })
    cell = _cell(ec.evaluate_full(root), "session_end_backpressure")
    assert cell.verdict == ec.ABSENT, cell.evidence
    assert cell.fired is not True, cell.evidence
    assert "block_unanchored_push" in cell.evidence
    assert "advisory in full" in cell.evidence


# ---------------------------------------------------------------------------
# The ADR-85 organ moved to pre-push — the probe must follow it, and must DISTINGUISH.
# ---------------------------------------------------------------------------


_ANCHOR_HOOK_ID = "block-unanchored-push"


def _hub_script_closure(entry_stem: str) -> dict[str, str]:
    """Real hub text for ``scripts/<entry_stem>.py`` + every sibling ``scripts/*.py`` it
    transitively imports.

    DERIVED, never a hand-maintained list: the organ already imports two siblings, which
    themselves import a third, and a fixture that enumerates today's set would silently go
    short the moment that graph changes — the fire_test would then fail for an import
    reason and read as "the organ does not enforce", which is the exact mismeasurement
    this test exists to prevent.
    """
    scripts = _REPO_ROOT / "scripts"
    seen: dict[str, str] = {}
    pending = [entry_stem]
    while pending:
        stem = pending.pop()
        if stem in seen:
            continue
        path = scripts / f"{stem}.py"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        seen[stem] = text
        for m in re.finditer(r"^\s*(?:import|from)\s+([A-Za-z_][A-Za-z0-9_]*)", text, re.M):
            if (scripts / f"{m.group(1)}.py").exists():
                pending.append(m.group(1))
    return {f"scripts/{stem}.py": text for stem, text in seen.items()}


def _hub_anchor_hook_config() -> str:
    """A minimal `.pre-commit-config.yaml` carrying the hub's OWN `block-unanchored-push`
    hook declaration, lifted verbatim from the live config.

    Structural on purpose (fire/locate must key on the shipped declaration): if the hub
    renames the id, moves the stage, or changes the entry, this fixture changes with it and
    `locate` has to keep resolving the real thing rather than a hand-written look-alike.
    """
    live = yaml.safe_load((_REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    for repo in live.get("repos", []):
        for hook in repo.get("hooks", []):
            if hook.get("id") == _ANCHOR_HOOK_ID:
                return yaml.safe_dump(
                    {"default_install_hook_types": live.get(
                        "default_install_hook_types", ["pre-commit", "pre-push"]),
                     "repos": [{"repo": "local", "hooks": [hook]}]},
                    sort_keys=False, allow_unicode=True)
    raise AssertionError(
        f"no {_ANCHOR_HOOK_ID!r} hook in the live .pre-commit-config.yaml — the ADR-85 hard "
        "leg is the organ this probe measures; if it was renamed, repoint the probe with it")


def _anchor_organ_consumer(root: Path) -> Path:
    """A consumer with the ADR-85 hard leg genuinely installed (real scripts + real hook)."""
    files = {
        "JOURNAL.md": "# Journal\n\n- prior session, nothing anchored here\n",
        ".pre-commit-config.yaml": _hub_anchor_hook_config(),
    }
    files.update(_hub_script_closure("block_unanchored_push"))
    return _init_consumer(root, files)


def test_anchor_gate_probe_distinguishes_installed_from_absent(tmp_path):
    """THE distinguishing proof for the repointed organ probe (ADR-85 amendment 2026-08-03).

    Demonstrates the vacuity this replaces: before the repoint, `_seb_fire` probed the Stop
    hook for `{"decision":"block"}`. That block was deleted BY DESIGN when the teeth moved to
    pre-push, so the probe answered ABSENT for every repo in the fleet — including one with
    the ADR-85 hard leg fully installed. A probe with a constant answer measures nothing.

    Shape chosen: a SINGLE test asserting BOTH halves rather than two independent tests. A
    pair can both pass while the probe is constant-ABSENT (the absent half carries it) or
    constant-PRESENT; only asserting the two verdicts DIFFER pins the discrimination itself.
    """
    installed = _anchor_organ_consumer(tmp_path / "installed")
    bare = _init_consumer(tmp_path / "bare", {"JOURNAL.md": "# Journal\n\n- work happened\n"})

    present = _cell(ec.evaluate_full(installed), "session_end_backpressure")
    absent = _cell(ec.evaluate_full(bare), "session_end_backpressure")

    assert present.verdict == ec.ENFORCING_LOCAL, present.evidence
    assert present.fired is True, present.evidence
    assert absent.verdict == ec.ABSENT, absent.evidence
    # The discrimination itself — not merely two verdicts that happen to be right today.
    assert present.verdict != absent.verdict


def test_anchor_gate_fire_requires_both_legs_not_a_constant_refusal(tmp_path):
    """The fire_test must prove the organ DISCRIMINATES anchored from unanchored, not merely
    that it exits non-zero. A hook hard-wired to `sys.exit(1)` refuses every push and enforces
    nothing meaningful; it must NOT read as enforcing-local."""
    root = _anchor_organ_consumer(tmp_path / "always-refuses")
    (root / "scripts" / "block_unanchored_push.py").write_text(
        "import sys\nsys.exit(1)\n", encoding="utf-8", newline="\n")
    _git(["add", "-A"], root)
    _git(["commit", "-q", "-m", "replace the organ with a constant refusal"], root)

    cell = _cell(ec.evaluate_full(root), "session_end_backpressure")
    assert cell.verdict == ec.ABSENT, cell.evidence
    assert cell.fired is False, cell.evidence


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
    still returns the hub-only n/a -> the reporter classifies hub-scoped from behavior, not a
    source-read of the `if repo_path != _REPO_ROOT` guard (architect ratification 2026-07-03)."""
    root = tmp_path / "consumer"
    root.mkdir()
    # Inject violations that WOULD trip each organ on the hub.
    (root / "BACKLOG.md").write_text(
        "# Backlog\n\n- [#999] a task closed in history but never removed\n",
        encoding="utf-8")
    (root / "ARCHITECTURE.md").write_text(
        "# Arch\n\n- audit: **3 registered checks** (wrong on purpose)\n", encoding="utf-8")

    # The demonstration: the organ short-circuits to n/a off-hub DESPITE the violation
    # ([#465] leg 1 retagged the token; the DEMONSTRATED-not-source-read standard is unchanged).
    fn = getattr(audit, f"check_{organ}")
    findings = fn(root)
    assert findings and all(f.status == "n/a" and "hub-only" in f.evidence for f in findings)

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
    root = _anchor_organ_consumer(tmp_path / "cand")
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


# ---------------------------------------------------------------------------
# Tier-3 classifier — demonstrated-catch BOTH directions ([#244] P4 contract 4).
# All route through the SAME classify_tier3 (operator condition 1). The SANCTIONED
# direction uses a FABRICATED waivable-component divergence (synthetic substrate — no
# wired-component fire-measurement exists at n=1; that is the P5/P6 milestone). The
# real fire divergences (seb) can only be DRIFT/REJECTED, which is exactly right.
# ---------------------------------------------------------------------------

# Mirrors the real v1.2.0 manifest waivability (the two fire organs non-waivable).
_REAL_POLICY = {
    "session-end-backpressure": False,
    "canonical-freshness": False,
    "hub-toc-hooks": True,
}


def _valid_entry(component, when="2999-01-01"):
    return ec.AllowlistEntry(component=component, reason="documented local reason",
                             expiry=None, review_date=ec._parse_date(when), raw={})


def test_tier3_divergence_no_allowlist_is_drift():
    """A real seb divergence (mapped ABSENT cell) with NO allowlist -> DRIFT (contract 3)."""
    cells = [ec.Cell("session_end_backpressure", ec.ABSENT, "Stop hook did NOT block")]
    divergences = ec._divergences_from_tier1(cells)
    assert divergences  # seb maps to a manifest component
    t3 = ec.classify_tier3(divergences, [], run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert [c.classification for c in t3] == [ec.DRIFT]
    assert t3[0].component_id == "session-end-backpressure"


def test_tier3_non_waivable_allowlisted_still_drift_rejected():
    """seb allowlisted BUT non-waivable -> REJECTED -> DRIFT (contract 2 + the reject half of 4)."""
    cells = [ec.Cell("session_end_backpressure", ec.ABSENT, "Stop hook did NOT block")]
    divergences = ec._divergences_from_tier1(cells)
    t3 = ec.classify_tier3(divergences, [_valid_entry("session-end-backpressure")],
                           run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert t3[0].classification == ec.DRIFT
    assert "rejected-non-waivable" in t3[0].evidence


def test_tier3_waivable_component_allowlisted_is_sanctioned():
    """A waivable component's divergence WITH a valid allowlist entry -> SANCTIONED (positive
    direction). FABRICATED divergence (synthetic substrate) through the real classify_tier3."""
    divergences = [("hub-toc-hooks", "hub-toc-hooks", "fabricated wired divergence (P5/P6 measurable)")]
    t3 = ec.classify_tier3(divergences, [_valid_entry("hub-toc-hooks")],
                           run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert t3[0].classification == ec.SANCTIONED
    assert t3[0].component_id == "hub-toc-hooks"


def test_tier3_same_divergence_reclassifies_by_allowlist():
    """Inject -> catch -> allowlist -> re-classify (contract 4), SAME classify_tier3: the SAME
    hub-toc-hooks divergence is DRIFT with no entry and SANCTIONED once validly allowlisted."""
    div = [("hub-toc-hooks", "hub-toc-hooks", "fabricated")]
    drift = ec.classify_tier3(div, [], run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    sanctioned = ec.classify_tier3(div, [_valid_entry("hub-toc-hooks")],
                                   run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert drift[0].classification == ec.DRIFT
    assert sanctioned[0].classification == ec.SANCTIONED


def test_tier3_expired_allowlist_is_drift():
    """A waivable component with an EXPIRED entry -> DRIFT (time-boxing enforced)."""
    div = [("hub-toc-hooks", "hub-toc-hooks", "fabricated")]
    t3 = ec.classify_tier3(div, [_valid_entry("hub-toc-hooks", when="2020-01-01")],
                           run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert t3[0].classification == ec.DRIFT
    assert "expired" in t3[0].evidence


# --- #250: codemap-freshness is now a manifest component -> Tier-3-classifiable ---


def test_codemap_component_waivable_in_live_manifest():
    """#250 Done-when: hub-codemap-hooks carries a waivability JUDGMENT read from the LIVE
    manifest (waivable: true, the doc-hygiene class) — so it is no longer invisible to the
    Tier-3 policy the way an unlisted deployed hook was."""
    policy = ec.waivability_policy_from_manifest(ec._latest_manifest())
    assert policy["hub-codemap-hooks"] is True


def test_tier3_codemap_divergence_sanctionable_via_live_policy():
    """#250 Done-when, end-to-end: a hub-codemap-hooks divergence classifies through the REAL
    manifest policy — DRIFT with no allowlist, SANCTIONED once validly allowlisted (the
    per-consumer drift is now Tier-3-classifiable, which it was not before the components: entry)."""
    policy = ec.waivability_policy_from_manifest(ec._latest_manifest())
    div = [("hub-codemap-hooks", "hub-codemap-hooks", "fabricated codemap drift (P5/P6 measurable)")]
    drift = ec.classify_tier3(div, [], run_date="2026-07-04", waivable_policy=policy)
    sanctioned = ec.classify_tier3(div, [_valid_entry("hub-codemap-hooks")],
                                   run_date="2026-07-04", waivable_policy=policy)
    assert drift[0].classification == ec.DRIFT
    assert sanctioned[0].classification == ec.SANCTIONED
    assert sanctioned[0].component_id == "hub-codemap-hooks"


def test_tier3_classification_vocabulary():
    """Every Tier3Cell classification is in the honest {DRIFT, SANCTIONED} axis."""
    div = [("hub-toc-hooks", "hub-toc-hooks", "x"),
           ("session-end-backpressure", "session_end_backpressure", "y")]
    t3 = ec.classify_tier3(div, [_valid_entry("hub-toc-hooks")],
                           run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert {c.classification for c in t3} <= {ec.DRIFT, ec.SANCTIONED}
    assert len(t3) == 2


def test_tier3_unmapped_organ_stays_tier1_only():
    """reconciled_versions/doc_claims/git_backlog_drift have no component -> no Tier-3 row."""
    cells = [ec.Cell("doc_claims", ec.HUB_SCOPED, "hub-only"),
             ec.Cell("reconciled_versions", ec.ABSENT, "absent but unmapped")]
    assert ec._divergences_from_tier1(cells) == []


def test_tier3_build_report_fire_attaches_drift(tmp_path):
    """End-to-end wiring: a consumer with an INERT seb (candidate but non-blocking) + no
    allowlist -> build_report(fire=True) attaches a DRIFT Tier3Cell for session-end-backpressure."""
    root = _init_consumer(tmp_path / "t3fire", {
        "JOURNAL.md": "# Journal\n",
        "scripts/session_end_backpressure.py": _INERT_STOP,
        ".claude/settings.json": _stop_settings(
            'python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'),
    })
    report = ec.build_report("t3fire", root, fire=True, tier2=False, run_date="2026-07-04")
    seb_t3 = [c for c in report.tier3 if c.component_id == "session-end-backpressure"]
    assert seb_t3 and seb_t3[0].classification == ec.DRIFT


# ---------------------------------------------------------------------------
# Tier-3 digest section + surface line ([#244] P4 Step 5).
# ---------------------------------------------------------------------------


def test_render_digest_has_tier3_section():
    rep = ec.ConsumerReport("demo", "/x", (), (), (
        ec.Tier3Cell("hub-toc-hooks", "hub-toc-hooks", ec.SANCTIONED, "sanctioned -- ok"),
        ec.Tier3Cell("session-end-backpressure", "session_end_backpressure", ec.DRIFT,
                     "unsanctioned drift (allowlist: no allowlist entry)"),
    ))
    out = ec.render_digest([rep], run_date="2026-07-04")
    assert "## Tier-3" in out
    assert "hub-toc-hooks" in out and "session-end-backpressure" in out
    assert ec.SANCTIONED in out and ec.DRIFT in out


def test_surface_line_counts_drift_and_sanctioned():
    rep = ec.ConsumerReport("demo", "/x", (), (), (
        ec.Tier3Cell("a", "o", ec.DRIFT, "x"),
        ec.Tier3Cell("b", "o", ec.DRIFT, "y"),
        ec.Tier3Cell("c", "o", ec.SANCTIONED, "z"),
    ))
    line = ec.surface_line([rep])
    assert "2 drift" in line
    assert "1 sanctioned" in line


def test_tier3_sanctioned_is_a_distinct_class_from_tier1():
    """SANCTIONED surfaces ONLY as a Tier-3 classification, never as a Tier-1 verdict
    (contract 3 -- sanctioned divergence is its own class). Checks the BOLD verdict form
    so the intro's descriptive 'sanctioned' word is not a false positive."""
    rep = ec.ConsumerReport("demo", "/x",
        (ec.Cell("session_end_backpressure", ec.ABSENT, "did not block"),),
        (),
        (ec.Tier3Cell("hub-toc-hooks", "hub-toc-hooks", ec.SANCTIONED, "sanctioned -- ok"),))
    out = ec.render_digest([rep], run_date="2026-07-04")
    bold_sanctioned = f"**{ec.SANCTIONED}**"
    tier1_block = out.split("## Tier-1")[1].split("## Tier-3")[0]
    assert bold_sanctioned not in tier1_block            # never a Tier-1 verdict
    assert bold_sanctioned in out.split("## Tier-3")[1]  # its own Tier-3 class


# ---------------------------------------------------------------------------
# Static (no-fire) drift summary ([#244] P4 Step 6). No clone, no fire: reads the
# consumer's WORKING-tree allowlist + locate-only evaluate_static. Feeds the
# fleet_health drift roll-up (Step 7). run_date is a param; policy is passed in.
# ---------------------------------------------------------------------------


def test_static_drift_summary_counts_absent_mapped_organs(tmp_path):
    """A consumer with a JOURNAL but no organ wiring: both mapped organs (seb + canonical_freshness)
    are statically ABSENT -> static_absent_mapped_organs == 2; no allowlist -> declared 0."""
    root = tmp_path / "bare"
    root.mkdir()
    (root / "JOURNAL.md").write_text("# Journal\n", encoding="utf-8")
    summary = ec.static_drift_summary(root, run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert summary["declared"] == 0
    assert summary["valid"] == 0
    assert summary["rejected_non_waivable"] == 0
    assert summary["static_absent_mapped_organs"] == 2
    assert "authoritative" in summary["note"]


def test_static_drift_summary_valid_waivable_entry(tmp_path):
    """A declared, valid allowlist entry for a WAIVABLE component counts as valid (not rejected)."""
    root = tmp_path / "waivable"
    root.mkdir()
    (root / "JOURNAL.md").write_text("# Journal\n", encoding="utf-8")
    (root / ec.ALLOWLIST_REL).write_text(
        "sanctioned_divergences:\n"
        "  - component: hub-toc-hooks\n"
        "    reason: CLI repo has no ARCHITECTURE.md TOC to gate\n"
        "    review_date: 2999-01-01\n",
        encoding="utf-8")
    summary = ec.static_drift_summary(root, run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert summary["declared"] == 1
    assert summary["valid"] == 1
    assert summary["rejected_non_waivable"] == 0


def test_static_drift_summary_rejects_non_waivable_entry(tmp_path):
    """A declared allowlist entry for a NON-waivable component is rejected-non-waivable — a
    fire-INDEPENDENT drift signal surfaced even by the static summary (contract 2)."""
    root = tmp_path / "reject"
    root.mkdir()
    (root / "JOURNAL.md").write_text("# Journal\n", encoding="utf-8")
    (root / ec.ALLOWLIST_REL).write_text(
        "sanctioned_divergences:\n"
        "  - component: session-end-backpressure\n"
        "    reason: we think we can skip it\n"
        "    review_date: 2999-01-01\n",
        encoding="utf-8")
    summary = ec.static_drift_summary(root, run_date="2026-07-04", waivable_policy=_REAL_POLICY)
    assert summary["declared"] == 1
    assert summary["valid"] == 0
    assert summary["rejected_non_waivable"] == 1


# ---------------------------------------------------------------------------
# [#481] — the organ id must name the organ the probe actually measures.
#
# `0c8647c2` repointed the ADR-85 probe at `block_unanchored_push` (pre-push) but kept the
# id `session_end_backpressure`, so the published identity named a Stop-hook script while
# the probe read a different organ at a different stage.
#
# The token is OVERLOADED: `scripts/session_end_backpressure.py` is still a live script,
# still deployed by `deploy/carrier_mesh.py`, still wired as an advisory Stop hook. A text
# scan cannot tell the retired ORGAN-ID from the live SCRIPT-NAME, so the census below
# discriminates by ROLE — the live registry for the code half, syntactic organ-id
# positions for the test half.
# ---------------------------------------------------------------------------

_RETIRED_ORGAN_ID = "session_end_backpressure"

# Organ-id SYNTACTIC positions — the mechanical role rule for the test half. Each pattern
# matches the token only where it stands in for a `Cell.organ_id` / `Tier3Cell.organ_id`
# value, never where it names the still-live script.
_ORGAN_ID_POSITIONS = (
    ("_cell(cells, <organ_id>)", re.compile(r'_cell\([^,]*,\s*"' + _RETIRED_ORGAN_ID + r'"\)')),
    ("cells[<organ_id>]", re.compile(r'cells\[\s*"' + _RETIRED_ORGAN_ID + r'"\s*\]')),
    ("ec.Cell(<organ_id>, ...)", re.compile(r'ec\.Cell\(\s*"' + _RETIRED_ORGAN_ID + r'"')),
    ("(<component_id>, <organ_id>, ...)",
     re.compile(r'"session-end-backpressure",\s*"' + _RETIRED_ORGAN_ID + r'"')),
)


def _anchor_probe():
    """The Group-C ADR-85 probe, resolved from the LIVE registry by GROUP.

    Deliberately not resolved by id literal: selecting the probe by the very string under
    test would make the invariant below circular and it would pass for any id at all.
    """
    group_c = [p for p in ec.TIER1_ORGANS if p.group == "C"]
    assert len(group_c) == 1, f"expected exactly one Group-C organ, got {[p.organ_id for p in group_c]}"
    return group_c[0]


def test_anchor_organ_id_names_the_organ_it_measures():
    """[#481] The Tier-1 organ id must name the organ the probe actually reads.

    Load-bearing AFTER the rename too: a future repoint that changes `_ANCHOR_ORGAN_SCRIPT`
    without renaming the id re-fails this test, which is the regression the row exists to stop.
    """
    probe = _anchor_probe()
    assert ec._ANCHOR_ORGAN_SCRIPT in probe.organ_id, (
        f"organ id {probe.organ_id!r} does not name the organ it measures "
        f"({ec._ANCHOR_ORGAN_SCRIPT!r} at {ec._ANCHOR_STAGE}) — the [#481] defect"
    )


def test_organ_id_census_carries_no_retired_id():
    """[#481] AC1/AC4 census — the ORGAN-ID role, read structurally rather than by grep.

    Code half: introspects the LIVE registry (`TIER1_ORGANS`, `_ORGAN_TO_COMPONENT`). Every
    organ-identity surface — the Tier-1 digest rows, the `<!-- organs: -->` marker, the
    Tier-3 component bridge — is generated from these two structures, so introspecting them
    IS the complete code-side census.

    Test half: scans this module for the syntactic organ-id positions above.

    *Honest limit:* prose mentions in comments/docstrings are not mechanically classifiable
    and are out of this census's scope by construction — it measures organ-id POSITIONS, not
    every appearance of the string.
    """
    registry_ids = {p.organ_id for p in ec.TIER1_ORGANS}
    assert _RETIRED_ORGAN_ID not in registry_ids, (
        f"retired organ id still in TIER1_ORGANS: {sorted(registry_ids)}")
    assert _RETIRED_ORGAN_ID not in ec._ORGAN_TO_COMPONENT, (
        f"retired organ id still keys _ORGAN_TO_COMPONENT: {sorted(ec._ORGAN_TO_COMPONENT)}")

    source = Path(__file__).read_text(encoding="utf-8")
    hits = {label: len(rx.findall(source)) for label, rx in _ORGAN_ID_POSITIONS}
    offenders = {label: n for label, n in hits.items() if n}
    assert not offenders, f"retired organ id still in organ-id positions in this module: {offenders}"
