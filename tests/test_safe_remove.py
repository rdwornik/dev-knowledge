"""#195 safe-removal gate — demonstrated-catch suite (the consumer that gives the #193
reverse-dep oracle teeth).

CLOSURE is the DEMONSTRATED catch (#207 lesson): the gate must actually FAIL a real
removal-with-a-live-referrer, naming the referrer — NOT merely "the gate is wired". A test that
removes a module with NO referrer and checks it is allowed proves nothing; the load-bearing
tests here EXERCISE the block path.

Three layers, ordered by how strongly they prove teeth:
  A. Deterministic block-logic + plumbing (ALWAYS runs, no Pyright) — the teeth proof: a stub
     oracle reporting a surviving referrer drives evaluate_removal AND the full
     diff->materialize->FAIL path (check_removal) AND the audit adapter to a FAIL.
  B. Real-oracle catch (@requires_pyright): the REAL Pyright oracle, run over a faithful copy of
     the live scripts/, surfaces a REAL cross-module referrer -> unsafe (the GAP-1 payoff). The
     copy's cross-module parity with the live repo was verified empirically (#195 probe).
  C. Inverse + co-removal: legitimate removals do NOT false-fire (no-referrer / co-remove the
     sole referrer / oracle-unavailable -> allow).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest  # noqa: E402

import audit as aud  # noqa: E402
import reverse_dep_oracle as rdo  # noqa: E402
import safe_remove as sr  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[1]

# Same langserver resolution + skip-gate the oracle's own suites use, so this never silently
# passes when Pyright is unprovisioned (a SKIP is not-proven-in-this-env, never fake-green).
_LS_ARGV = rdo.find_langserver(_REPO_ROOT)
_LS_OVERRIDE = _LS_ARGV[1] if (_LS_ARGV and _LS_ARGV[0] == "node") else None


def _langserver_available() -> bool:
    return shutil.which("node") is not None and _LS_ARGV is not None


requires_pyright = pytest.mark.skipif(
    not _langserver_available(),
    reason="safe-removal real-oracle catch needs a Pyright langserver; absent in this env -- "
    "skip-guarded (never fake-green), same contract as test_legibility_graph_conformance",
)


# --- stubs + fixtures ------------------------------------------------------------------

def _stub_oracle(*, status="resolved", deps=(), completeness="complete"):
    """A deterministic oracle replacement (run_oracle's signature) — the #207 teeth-proof feeds
    a KNOWN surviving referrer so the block path is exercised without Pyright."""
    def _o(symbol, file, repo_root, langserver=None, timeout=20):
        return {
            "resolution": {"status": status},
            "reverse_dependents": [dict(d) for d in deps],
            "reverse_dependent_count": len(deps),
            "provenance": {"completeness": completeness},
        }
    return _o


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)


def _init_git_repo(root: Path, files: dict) -> None:
    """A throwaway git repo committed at HEAD, so check_removal's git-diff deletion detection +
    HEAD-restore materialization run for real (no Pyright; the oracle is stubbed)."""
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    _git(root, "init")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "init")


_FOO = "def widget():\n    return 1\n"
_BAR = "from foo import widget\n\n\ndef use():\n    return widget()\n"


# =======================================================================================
# Layer A — deterministic teeth-proof (ALWAYS runs; the block path is EXERCISED)
# =======================================================================================

def test_evaluate_removal_blocks_on_surviving_referrer(tmp_path):
    """THE teeth proof: a removed module whose symbol still has an external referrer -> unsafe,
    and the referrer is NAMED. (A no-referrer 'allowed' test would prove nothing — #207.)"""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "foo.py").write_text(_FOO, encoding="utf-8")
    verdict = sr.evaluate_removal(
        ["scripts/foo.py"], tmp_path,
        oracle=_stub_oracle(deps=[{"file": "scripts/bar.py", "line": 1}]))
    assert verdict.status == "unsafe", verdict
    named = {r["referrer"] for r in verdict.surviving_referrers}
    assert "scripts/bar.py" in named, verdict.surviving_referrers


def test_check_removal_blocks_end_to_end_with_stub_oracle(tmp_path):
    """The BUILD-TIME automatic path, deterministically: a real git deletion of scripts/foo.py
    is detected, the module is restored from HEAD into the materialized query root, and the
    (stubbed) oracle's surviving referrer drives a FAIL — proving diff->materialize->block wiring
    without needing Pyright."""
    _init_git_repo(tmp_path, {"scripts/foo.py": _FOO, "scripts/bar.py": _BAR})
    (tmp_path / "scripts" / "foo.py").unlink()  # stage the removal in the working tree
    verdict = sr.check_removal(
        tmp_path, oracle=_stub_oracle(deps=[{"file": "scripts/bar.py", "line": 1}]))
    assert verdict.status == "unsafe", verdict
    assert verdict.removal_set == ["scripts/foo.py"], verdict.removal_set
    assert any(r["referrer"] == "scripts/bar.py" for r in verdict.surviving_referrers), verdict


def test_audit_adapter_emits_fail_finding_naming_referrer(tmp_path, monkeypatch):
    """Through the registered audit check: an unsafe Verdict -> a FAIL Finding per surviving
    referrer, the referrer named (FAIL-class -> blocks audit-health + ship-gate)."""
    unsafe = sr.Verdict(
        "unsafe", ["scripts/foo.py"],
        surviving_referrers=[{"referrer": "scripts/bar.py", "line": 7,
                              "symbol": "widget", "module": "scripts/foo.py"}],
        completeness="complete", reason="1 surviving referrer")
    monkeypatch.setattr(aud._sr, "check_removal", lambda *a, **k: unsafe)
    findings = aud.check_safe_removal(tmp_path)
    assert [f.status for f in findings] == ["fail"], [(f.status, f.evidence) for f in findings]
    assert findings[0].check_name == "safe_removal"
    assert "scripts/bar.py" in findings[0].evidence and "widget" in findings[0].evidence


# =======================================================================================
# Layer C — inverse + co-removal (legitimate removals do NOT false-fire)
# =======================================================================================

def test_co_removal_passes(tmp_path):
    """Removing a module AND its sole referrer together -> the referrer is in the removal set ->
    NOT surviving -> safe (the documented legitimate case must PASS)."""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "foo.py").write_text(_FOO, encoding="utf-8")
    (tmp_path / "scripts" / "bar.py").write_text(_BAR, encoding="utf-8")
    verdict = sr.evaluate_removal(
        ["scripts/foo.py", "scripts/bar.py"], tmp_path,
        oracle=_stub_oracle(deps=[{"file": "scripts/bar.py", "line": 1}]))
    assert verdict.status == "safe", verdict
    assert verdict.surviving_referrers == []


def test_no_referrer_passes(tmp_path):
    """A truly orphaned module (no referrers) -> safe."""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "orphan.py").write_text(_FOO, encoding="utf-8")
    verdict = sr.evaluate_removal(["scripts/orphan.py"], tmp_path, oracle=_stub_oracle(deps=[]))
    assert verdict.status == "safe", verdict


def test_oracle_unavailable_is_unverifiable_not_block(tmp_path):
    """Pyright absent -> oracle-unavailable -> unverifiable (WARN+allow), never a synthesized
    FAIL (#195 can't-verify posture). (Adapter mapping to WARN is its own test below.)"""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "foo.py").write_text(_FOO, encoding="utf-8")
    verdict = sr.evaluate_removal(
        ["scripts/foo.py"], tmp_path, oracle=_stub_oracle(status="oracle-unavailable"))
    assert verdict.status == "unverifiable", verdict
    assert verdict.surviving_referrers == []


def test_check_removal_no_deletion_is_instant_pass(tmp_path):
    """No scripts/*.py deletion in the diff -> instant safe verdict, no oracle call (the fast
    path that bounds the Pyright cost to actual removals)."""
    _init_git_repo(tmp_path, {"scripts/foo.py": _FOO})
    called = {"n": 0}

    def _counting(*a, **k):
        called["n"] += 1
        return _stub_oracle()(*a, **k)

    verdict = sr.check_removal(tmp_path, oracle=_counting)
    assert verdict.status == "safe" and verdict.removal_set == []
    assert called["n"] == 0, "oracle must not be consulted when nothing is removed"


def test_adapter_unverifiable_warns_not_fails(tmp_path, monkeypatch):
    """Explicit: an unverifiable Verdict -> a single WARN Finding (allow), never FAIL."""
    unverifiable = sr.Verdict(
        "unverifiable", ["scripts/foo.py"],
        unverifiable=[{"module": "scripts/foo.py", "symbol": "widget",
                       "reason": "oracle-unavailable"}],
        reason="Pyright absent")
    monkeypatch.setattr(aud._sr, "check_removal", lambda *a, **k: unverifiable)
    findings = aud.check_safe_removal(tmp_path)
    assert [f.status for f in findings] == ["warn"], [(f.status, f.evidence) for f in findings]
    assert "unverifiable" in findings[0].evidence.lower()


# =======================================================================================
# Layer B — real-oracle catch (@requires_pyright): the GAP-1 payoff is real
# =======================================================================================

@requires_pyright
def test_real_oracle_blocks_real_cross_module_removal(tmp_path):
    """The REAL Pyright oracle, over a faithful FULL copy of the live scripts/ (the build-time
    materialization shape — cross-module parity with the live repo verified empirically, #195
    probe), surfaces a REAL cross-module referrer: removing scripts/generate_floor.py would leave
    scripts/audit.py (which imports floor_sha256) dangling -> unsafe, audit.py NAMED. This is the
    demonstrated catch through the real oracle, not a stub."""
    shutil.copytree(_REPO_ROOT / "scripts", tmp_path / "scripts")
    verdict = sr.evaluate_removal(
        ["scripts/generate_floor.py"], tmp_path, langserver=_LS_OVERRIDE)
    assert verdict.status == "unsafe", verdict
    referrers = {r["referrer"] for r in verdict.surviving_referrers}
    assert "scripts/audit.py" in referrers, verdict.surviving_referrers


@requires_pyright
def test_real_oracle_allows_orphan_removal(tmp_path):
    """Inverse with the real oracle: a freshly-added module nothing references -> safe (no
    false-fire). Proves the real-oracle PASS path too, so the block above is a discriminator."""
    shutil.copytree(_REPO_ROOT / "scripts", tmp_path / "scripts")
    (tmp_path / "scripts" / "zz_orphan_probe.py").write_text(
        "def nobody_calls_this():\n    return 42\n", encoding="utf-8")
    verdict = sr.evaluate_removal(
        ["scripts/zz_orphan_probe.py"], tmp_path, langserver=_LS_OVERRIDE)
    assert verdict.status == "safe", verdict
