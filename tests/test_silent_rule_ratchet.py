"""Coverage for the [#436] silent-rule ratchet — scripts/silent_rule_detector.py plus the
`silent_rule_ratchet` ALL_CHECKS member in scripts/audit.py.

The four contract cases the build was gated on (operator-adopted D4 semantics, 2026-07-27)
are pinned here FIRST-CLASS and named accordingly:

    pass-at-baseline        test_pass_at_baseline
    fail-above-baseline     test_fail_above_baseline
    ratchet-down accepted   test_ratchet_down_accepted / test_transition_allows_drain
    baseline-raise rejected test_baseline_raise_rejected / test_transition_rejects_raise

Everything else here defends the detector contract itself: the metric is only meaningful
if the detector that produced the baseline is the detector producing the live count.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud
import silent_rule_detector as srd

REPO_ROOT = Path(__file__).resolve().parent.parent


def _measurement(count: int, detector_id: str = srd.DETECTOR_ID, files: int = 56):
    return srd.Measurement(detector_id=detector_id, count=count, files=files)


def _baseline(value: int, detector_id: str = srd.DETECTOR_ID) -> dict:
    return {"detector_id": detector_id, "baseline": value}


def _git_tree(root: Path, files: dict[str, str]) -> Path:
    """A real git repo -- the corpus is git-defined (v3), so a bare tmp dir has none."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=root, check=True, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "fixture")
    return root


def _status(findings) -> str:
    assert len(findings) == 1, f"expected exactly one Finding, got {findings!r}"
    return findings[0].status


# ---------------------------------------------------------------------------
# The four contract cases
# ---------------------------------------------------------------------------

def test_pass_at_baseline():
    """CASE 1 — live count exactly equal to the committed baseline PASSES.

    Equality is the steady state: the pool has not grown. A gate that fired here would
    RED on its own first run, which is what the arm-time stop existed to prevent.
    """
    findings = aud._ratchet_findings(_measurement(428), _baseline(428))
    assert _status(findings) == "pass"
    assert "428" in findings[0].evidence


def test_fail_above_baseline():
    """CASE 2 — one candidate line above the baseline FAILS, and names both numbers."""
    findings = aud._ratchet_findings(_measurement(429), _baseline(428))
    assert _status(findings) == "fail"
    ev = findings[0].evidence
    assert "429" in ev and "428" in ev, f"evidence must name live and baseline: {ev}"


def test_ratchet_down_accepted():
    """CASE 3 — live BELOW the baseline passes: draining is the point, not a violation.

    The check must not demand exactness, or every drained rule would break the gate.
    """
    findings = aud._ratchet_findings(_measurement(400), _baseline(428))
    assert _status(findings) == "pass"


def test_baseline_raise_rejected():
    """CASE 4 — raising the committed baseline is rejected by the transition validator.

    This is the invariant that makes it a RATCHET rather than a high-water mark: the
    number may fall or hold, never rise. Enforced as a pure function so it is testable
    without a git history, and consumed by the check's git-previous leg.
    """
    reason = srd.validate_transition(old=428, new=500)
    assert reason is not None
    assert "428" in reason and "500" in reason
    assert "reject" in reason.lower()


# ---------------------------------------------------------------------------
# Transition validator — both directions, including the boundary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("old,new", [(428, 428), (428, 427), (428, 0)])
def test_transition_allows_drain(old, new):
    """Holding steady and lowering are both legal transitions."""
    assert srd.validate_transition(old=old, new=new) is None


@pytest.mark.parametrize("old,new", [(428, 429), (0, 1), (100, 1000)])
def test_transition_rejects_raise(old, new):
    """Any increase at all is rejected — there is no tolerance band."""
    assert srd.validate_transition(old=old, new=new) is not None


def test_no_baseline_raising_function_exists():
    """RATCHET-DOWN ONLY is a structural property, not a convention.

    The module must expose no callable that writes or raises a baseline. If someone adds
    one, this test names it — the escape hatch has to be a reviewed commit, never a code
    path that quietly re-arms the gate at a higher number.
    """
    forbidden = [n for n in dir(srd)
                 if any(tok in n.lower() for tok in ("write", "raise_", "set_baseline",
                                                     "update_baseline", "bump"))]
    assert forbidden == [], f"module exposes baseline-mutating callables: {forbidden}"


# ---------------------------------------------------------------------------
# Detector-contract defences
# ---------------------------------------------------------------------------

def test_detector_id_mismatch_fails_rather_than_comparing():
    """Two detectors' counts are not commensurable — comparing them is the failure mode
    the whole module exists to prevent, so a stamp mismatch FAILS loudly."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428, detector_id="silent-rule-v0"))
    assert _status(findings) == "fail"
    assert "silent-rule-v0" in findings[0].evidence


def test_absent_baseline_warns_and_does_not_pass_vacuously():
    """No baseline = inert gate. That must be visible, never a silent green."""
    findings = aud._ratchet_findings(_measurement(428), None)
    assert _status(findings) == "warn"


def test_malformed_baseline_value_fails():
    """A non-integer baseline is a corrupt gate, not a zero."""
    findings = aud._ratchet_findings(_measurement(428), {"detector_id": srd.DETECTOR_ID,
                                                         "baseline": "many"})
    assert _status(findings) == "fail"


def test_detector_catches_the_three_adjudicated_silent_rules():
    """The empirical basis for the token choice, pinned so a future 'tidy-up' cannot
    silently narrow it back to uppercase-only.

    These three lines are the rules the 2026-07-27 arm-time probe adjudicated as genuinely
    new-and-silent. An uppercase-anchored detector matched 0 of 3 — it would have been
    blind to the exact growth that stopped the build.
    """
    probes = [
        "**Never branch, commit, or merge under a live session.**",
        "`marketplace add` **must** precede `install`",
        "`.gitignore` floor negations **must use the contents form**",
    ]
    for line in probes:
        assert srd.TOKEN_RE.search(line), f"detector blind to a known silent rule: {line}"


def test_parity_surfaces_excluded_from_scope():
    """parity-surfaces.yaml rows are `tier:` ENUM VALUES read by fleet_parity — enforced
    by construction. In scope they were 120 of 148 candidate lines (81%), so the ratchet
    would have fired on ADDING ENFORCEMENT. Pinned because that is a subtle regression."""
    scoped = {rel for rel, _sha in srd.iter_scoped_files(REPO_ROOT)}
    assert "ecosystem/parity-surfaces.yaml" not in scoped


def test_baseline_file_excluded_from_its_own_scope():
    """The baseline lives in ecosystem/*.yaml; counting its own provenance prose would
    make the metric self-referential (and self-inflating on every re-stamp)."""
    scoped = {rel for rel, _sha in srd.iter_scoped_files(REPO_ROOT)}
    assert srd.BASELINE_RELPATH not in scoped


def test_archive_paths_excluded_from_scope():
    """Retiring doctrine into archive/ is a genuine drain, so archived files are out."""
    scoped = [rel for rel, _sha in srd.iter_scoped_files(REPO_ROOT)]
    assert not [r for r in scoped if "/archive/" in r or r.startswith("archive/")]


def test_measure_is_deterministic_and_sorted():
    """Two runs agree, and enumeration order is stable — a metric that wobbles between
    runs cannot gate anything."""
    first, second = srd.measure(REPO_ROOT), srd.measure(REPO_ROOT)
    assert first == second
    rels = [rel for rel, _sha in srd.iter_scoped_files(REPO_ROOT)]
    # Sorted on the NFC-normalized, casefolded relpath — see iter_scoped_files: ordering
    # has to agree across case- and normalization-insensitive filesystems.
    assert rels == sorted(rels, key=lambda r: (srd._fold(r), r))


def test_committed_baseline_matches_live_measurement():
    """The committed baseline must actually hold on the live repo — i.e. the gate is
    GREEN as shipped. This is the test that would have caught arming at 176."""
    doc = aud._load_silent_rule_baseline(REPO_ROOT)
    assert doc is not None, f"missing {srd.BASELINE_RELPATH}"
    assert doc["detector_id"] == srd.DETECTOR_ID
    live = srd.measure(REPO_ROOT)
    assert live.count <= doc["baseline"], (
        f"live {live.count} exceeds committed baseline {doc['baseline']}")


def test_check_registered_and_green_on_live_repo():
    """The check is in ALL_CHECKS (so it is a ship-gate leg by construction) and passes
    against the live hub."""
    assert aud.check_silent_rule_ratchet in aud.ALL_CHECKS
    findings = aud.check_silent_rule_ratchet(REPO_ROOT)
    assert _status(findings) == "pass"


# ---------------------------------------------------------------------------
# Regression cover for the five terra HIGH findings (2026-07-27). Each names the
# defect it pins so a later refactor cannot quietly reintroduce it.
# ---------------------------------------------------------------------------

def test_detector_failure_blocks_rather_than_shipping_green(monkeypatch):
    """terra HIGH — a measurement failure used to emit `unavailable`, which ship-gate does
    NOT block on (it blocks `fail` and undispositioned `warn` only). An unmeasured corpus
    would have shipped green. It must FAIL.

    Patches `aud._srd`, not the test's own `srd`: audit.py resolves the detector via
    `from scripts import silent_rule_detector`, which is a DIFFERENT module object from a
    bare `import silent_rule_detector` when both the repo root and scripts/ are on the
    path. Patching the wrong one silently no-ops and the test passes vacuously.
    """
    def boom(_root):
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "simulated cp1252 corpus")

    monkeypatch.setattr(aud._srd, "measure", boom)
    findings = aud.check_silent_rule_ratchet(REPO_ROOT)
    assert _status(findings) == "fail", findings
    assert "could not measure" in findings[0].evidence


def test_raise_guard_reads_integration_target_not_head():
    """terra HIGH — the guard read HEAD, so once a raise was committed it compared the new
    baseline against itself and passed. It must read the integration target."""
    import inspect

    src = inspect.getsource(aud._target_baseline_state)
    assert "_BASELINE_REFS" in src
    assert "HEAD:" not in src, "raise-guard must not compare the baseline against HEAD"
    assert aud._BASELINE_REFS[0] == "origin/main"


def test_bootstrap_raise_guard_is_surfaced_not_silent():
    """terra HIGH — when there is no previous value the guard cannot run. Where absence is
    PROVEN ("absent") that is legitimate, but it must still be visible in the evidence, or
    'did not run' reads exactly like 'passed'."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428),
                                     previous=None, ref_state="absent")
    assert _status(findings) == "pass"
    assert "bootstrap" in findings[0].evidence


def test_unverifiable_raise_guard_blocks():
    """terra HIGH (2nd pass) — the first fix still PASSED (with a note) when no integration
    ref resolved, and ship-gate ignores notes on a passing finding, so a detached or
    ref-less checkout could raise the baseline and ship green. Must WARN."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428),
                                     previous=None, ref_state="unresolved")
    assert _status(findings) == "warn"
    assert "UNVERIFIABLE" in findings[0].evidence


def test_indeterminate_target_baseline_blocks():
    """terra HIGH (3rd pass) — 'ref resolved + read failed' was being treated as bootstrap.
    A target baseline that EXISTS but is malformed or unreadable must block: a raise cannot
    be ruled out, and bootstrapping past it is fail-open."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428),
                                     previous=None, ref_state="invalid")
    assert _status(findings) == "fail"
    assert "INDETERMINATE" in findings[0].evidence


def test_target_state_is_proven_not_inferred(tmp_path):
    """A non-git directory resolves no integration ref => 'unresolved', never 'absent'."""
    state, value, detector = aud._target_baseline_state(tmp_path)
    assert (state, value, detector) == ("unresolved", None, None)


def test_target_state_on_live_repo_is_a_known_state():
    """On the live repo the state must be one of the four modelled values, with `valid`
    carrying an int — no silent fifth state."""
    state, value, detector = aud._target_baseline_state(REPO_ROOT)
    assert state in {"valid", "absent", "invalid", "unresolved"}
    assert (value is None) == (state != "valid")
    assert (detector is None) == (state != "valid")


def test_malformed_target_baseline_is_invalid_not_absent(tmp_path):
    """The precise fail-open terra named: the file EXISTS on the target ref but does not
    parse. That must be `invalid` (blocking), never `absent` (bootstrap)."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True,
                       capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    target = tmp_path / srd.BASELINE_RELPATH
    target.parent.mkdir(parents=True)
    target.write_text("baseline: [this is not an int\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "malformed baseline on main")
    state, value, detector = aud._target_baseline_state(tmp_path)
    assert (state, value, detector) == ("invalid", None, None)


def test_valid_target_baseline_is_read(tmp_path):
    """The positive path: a well-formed baseline on the target ref is returned for
    comparison, so a raise on the branch is actually caught."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True,
                       capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    target = tmp_path / srd.BASELINE_RELPATH
    target.parent.mkdir(parents=True)
    target.write_text(f"detector_id: {srd.DETECTOR_ID}\nbaseline: 100\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "baseline on main")
    assert aud._target_baseline_state(tmp_path) == ("valid", 100, srd.DETECTOR_ID)
    # ...and a branch raising it above that value is refused.
    findings = aud._ratchet_findings(_measurement(50), _baseline(150),
                                     previous=100, ref_state="valid")
    assert _status(findings) == "fail"


def test_raise_guard_fails_when_previous_is_lower():
    """The guard's positive case: a branch raising the committed baseline is blocked."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(500), previous=428)
    assert _status(findings) == "fail"
    assert "reject" in findings[0].evidence.lower()


def test_metric_is_reflow_stable():
    """terra HIGH — a per-line count moves under pure reflow: joining two rule lines lowers
    it without removing a rule. Occurrence counting must be invariant under rewrapping."""
    joined = "A rule that must hold. Another that shall hold. A third that never yields."
    split = "A rule that must hold.\nAnother that shall hold.\nA third that never yields."
    assert len(srd.TOKEN_RE.findall(joined)) == len(srd.TOKEN_RE.findall(split)) == 3
    per_line_joined = sum(1 for ln in joined.splitlines() if srd.TOKEN_RE.search(ln))
    assert per_line_joined == 1, "per-line counting is the gameable unit v2 replaced"


def test_path_exclusions_are_case_insensitive(tmp_path):
    """terra HIGH — a differently-cased `templates/Archive/...` must still be excluded, or
    the same tree measures differently per platform."""
    _git_tree(tmp_path, {"templates/Archive/old.md": "must", "protocols/live.md": "must"})
    rels = [rel for rel, _sha in srd.iter_scoped_files(tmp_path)]
    assert "templates/Archive/old.md" not in rels, rels
    assert "protocols/live.md" in rels


def test_detector_id_bumped_for_each_contract_change():
    """The contract says ANY clause change bumps the id, so two incompatible metrics can
    never share a name. v1 counted lines; v2 counted occurrences; v3 took its corpus from
    git's tracked inventory instead of a filesystem walk; v4 reads CONTENT from the object
    store too."""
    assert srd.DETECTOR_ID == "silent-rule-v4"


def test_enumeration_is_case_insensitive_on_extensions(tmp_path):
    """terra HIGH RE-REVIEW — a `.MD` file counted on Windows and vanished on Linux: the
    same tree, two numbers. Suffix matching is casefolded."""
    _git_tree(tmp_path, {"protocols/UPPER.MD": "must", "protocols/lower.md": "must"})
    rels = [rel for rel, _sha in srd.iter_scoped_files(tmp_path)]
    assert rels == ["protocols/lower.md", "protocols/UPPER.MD"], rels
    assert srd.measure(tmp_path).count == 2


def test_casefold_colliding_tracked_paths_are_refused(tmp_path):
    """terra HIGH (3rd pass) — a walk produced DIFFERENT FILE SETS across platforms for
    case-colliding names, so a rule could vanish from the measurement by being on the wrong
    OS. Rather than silently pick one, an ambiguous corpus is REFUSED."""
    import subprocess

    _git_tree(tmp_path, {"protocols/alpha.md": "must"})
    # Add a colliding path directly to the index: on a case-insensitive filesystem the two
    # cannot both exist on disk, which is exactly the ambiguity being refused.
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=tmp_path,
                          input="must", capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                    f"100644,{blob},protocols/Alpha.md"], cwd=tmp_path, check=True,
                   capture_output=True, text=True)
    with pytest.raises(srd.DetectorError) as exc:
        srd.iter_scoped_files(tmp_path)
    assert "colliding" in str(exc.value)


def test_untracked_file_cannot_inflate_the_metric(tmp_path):
    """The corpus is what git TRACKS, so a scratch draft dropped into protocols/ does not
    move the ratchet — correct, since the ratchet governs the committed corpus."""
    _git_tree(tmp_path, {"protocols/live.md": "must"})
    before = srd.measure(tmp_path).count
    (tmp_path / "protocols" / "scratch.md").write_text("must must must", encoding="utf-8")
    assert srd.measure(tmp_path).count == before


def test_non_git_tree_raises_rather_than_measuring_a_subset(tmp_path):
    """A corpus that cannot be enumerated must RAISE. Degrading to a partial count is worse
    than no count, because a partial count reads as a low one."""
    with pytest.raises(srd.DetectorError):
        srd.iter_scoped_files(tmp_path)


def test_content_is_read_from_git_not_the_working_tree():
    """terra HIGH (4th pass) — `ls-files` gave canonical PATHS but content was re-opened
    from disk, handing the bytes back to the host (smudge filters, aliases, NFC/NFD). The
    measurement must come from the object store the index points at."""
    import inspect

    src = inspect.getsource(srd.measure)
    assert "_read_blobs" in src
    assert "read_text" not in src, "content must not be re-opened from the working tree"


def test_working_tree_edit_does_not_move_the_metric(tmp_path):
    """The behavioural consequence: an UNCOMMITTED edit to a tracked file leaves the count
    alone, because the metric reads the committed blob."""
    _git_tree(tmp_path, {"protocols/live.md": "must"})
    before = srd.measure(tmp_path).count
    (tmp_path / "protocols" / "live.md").write_text("must must must must", encoding="utf-8")
    assert srd.measure(tmp_path).count == before


def test_strictest_target_baseline_wins(tmp_path, monkeypatch):
    """terra HIGH (4th pass) — returning the FIRST valid ref let a raise hide behind the
    other: origin/main at 500 and an ahead local main at 400 let a branch value of 450 pass
    against 500 while raising the real local target from 400. min() closes that."""
    calls = {"origin/main": ("valid", 500, srd.DETECTOR_ID),
             "main": ("valid", 400, srd.DETECTOR_ID)}
    monkeypatch.setattr(aud, "_ref_baseline_state", lambda _p, ref: calls[ref])
    assert aud._target_baseline_state(tmp_path) == ("valid", 400, srd.DETECTOR_ID)


def test_any_invalid_ref_blocks_even_if_another_is_valid(tmp_path, monkeypatch):
    """An unreadable target must not be skipped in favour of a readable one — that is the
    same fail-through, one ref along."""
    calls = {"origin/main": ("invalid", None, None),
             "main": ("valid", 400, srd.DETECTOR_ID)}
    monkeypatch.setattr(aud, "_ref_baseline_state", lambda _p, ref: calls[ref])
    assert aud._target_baseline_state(tmp_path) == ("invalid", None, None)


def test_ref_probe_failure_is_invalid_not_absent(tmp_path, monkeypatch):
    """terra HIGH (4th pass) — `git cat-file -e` returns non-zero for an INACCESSIBLE or
    corrupt object exactly as for a missing path, so "non-zero means absent" read an
    unreadable target as first-introduction. Absence is proven with ls-tree; a failed
    lookup is `invalid`."""
    import subprocess

    real = aud._git

    def fake(repo, *args):
        if args[0] == "rev-parse":
            return subprocess.CompletedProcess(args, 0, "deadbeef\n", "")
        if args[0] == "ls-tree":
            return subprocess.CompletedProcess(args, 128, "", "fatal: bad object")
        return real(repo, *args)

    monkeypatch.setattr(aud, "_git", fake)
    assert aud._ref_baseline_state(tmp_path, "origin/main") == ("invalid", None, None)


def test_staged_baseline_raise_cannot_hide_behind_the_working_copy(tmp_path, monkeypatch):
    """terra HIGH (6th pass) — the baseline was read from the WORKING TREE while the
    detector measures the INDEX, so staging a raised baseline and restoring the working
    copy validated the old value while committing the raised one. The check must refuse."""
    import subprocess

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_tree(tmp_path, {srd.BASELINE_RELPATH:
                         f"detector_id: {srd.DETECTOR_ID}\nbaseline: 10\n"})

    target = tmp_path / srd.BASELINE_RELPATH
    original = target.read_bytes()
    target.write_bytes(original.replace(b"baseline: 10", b"baseline: 9999"))
    subprocess.run(["git", "add", srd.BASELINE_RELPATH], cwd=tmp_path, check=True,
                   capture_output=True, text=True)
    target.write_bytes(original)                    # restore the working copy
    findings = aud.check_silent_rule_ratchet(tmp_path)
    assert _status(findings) == "fail", findings
    assert "untrustworthy" in findings[0].evidence


def test_ratchet_blocks_when_divergence_probe_fails(tmp_path, monkeypatch):
    """An unknown answer from the git probe is not agreement — same fail-open class."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(aud, "_git", lambda *a, **k: None)
    monkeypatch.setattr(aud._srd, "measure", lambda _r: _measurement(1))
    findings = aud.check_silent_rule_ratchet(tmp_path)
    assert _status(findings) == "fail", findings
    assert "could not compare" in findings[0].evidence


def test_detector_migration_cannot_silently_rebase_the_metric():
    """terra HIGH (8th pass) — the raise-guard compared NUMBERS across refs without
    checking they came from the same detector, so bumping the detector version would let a
    re-measurement silently rebase the metric past the ratchet-down invariant. A migration
    must be reviewed explicitly, not waved through by a version bump."""
    findings = aud._ratchet_findings(_measurement(9999), _baseline(9999), previous=100,
                                     ref_state="valid", previous_detector="silent-rule-v1")
    assert _status(findings) == "warn"
    ev = findings[0].evidence
    assert "MIGRATION" in ev and "silent-rule-v1" in ev and srd.DETECTOR_ID in ev


def test_same_detector_still_compares_numerically():
    """The migration guard must not disable the ordinary raise check."""
    findings = aud._ratchet_findings(_measurement(50), _baseline(150), previous=100,
                                     ref_state="valid", previous_detector=srd.DETECTOR_ID)
    assert _status(findings) == "fail"
    assert "reject" in findings[0].evidence.lower()


def test_target_without_detector_id_is_invalid(tmp_path):
    """A target baseline carrying no detector id cannot be shown commensurable with the
    live count, so it is indeterminate rather than comparable."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    target = tmp_path / srd.BASELINE_RELPATH
    target.parent.mkdir(parents=True)
    target.write_text("baseline: 100\n", encoding="utf-8")   # no detector_id
    git("add", "-A")
    git("commit", "-qm", "baseline without a detector id")
    assert aud._target_baseline_state(tmp_path) == ("invalid", None, None)
