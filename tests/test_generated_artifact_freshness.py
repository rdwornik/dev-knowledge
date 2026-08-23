"""Tests for scripts/generated_artifact_freshness.py — the committed-generated staleness leg
(ADR-86 amended 2026-08-23; `[#171]` leg 1 / f7).

Two halves, deliberately. The PURE half injects `git_date_fn` and pins the relation's boundary
behaviour to the exact day — every one of those assertions is mutation-checked in the sense that
it fails under the obvious wrong implementation (`>=` for `>`, `max` for `min`, no floor at zero).
The LIVE half builds a real throwaway git repo and proves the leg **fires on a genuinely stale
tree and stays quiet on a fresh one**, which is the ADR-81 leg (e) functional proof: a gate that
has never been observed to fire is not done.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

import generated_artifact_freshness as gaf

_MODULE = Path(__file__).resolve().parent.parent / "scripts" / "generated_artifact_freshness.py"


def _fixed_dates(mapping: dict[str, date]):
    """A `git_date_fn` stand-in: pathspec -> date, None for anything unmapped."""
    return lambda _repo, pathspec: mapping.get(pathspec)


def _artifact(**overrides) -> gaf.GeneratedArtifact:
    base = dict(name="probe", outputs=("out.md",), inputs=("in.md",), baseline_days=3,
                regen_command="python scripts/gen_dashboard.py --write")
    base.update(overrides)
    return gaf.GeneratedArtifact(**base)


# --------------------------------------------------------------- the relation, pinned to the day

def test_fresh_when_inputs_are_older_than_the_artifact():
    m = gaf.measure(Path("."), _artifact(), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 18)}))
    assert m.verdict == "fresh"
    assert m.staleness_days == 0, "an artifact newer than its inputs floors at 0, never negative"


def test_fresh_at_exactly_the_baseline():
    """BOUNDARY: baseline 3, staleness 3 -> fresh. Fails if the comparison is `>=`."""
    m = gaf.measure(Path("."), _artifact(baseline_days=3), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 23)}))
    assert m.staleness_days == 3
    assert m.verdict == "fresh"


def test_stale_at_baseline_plus_one():
    """BOUNDARY: baseline 3, staleness 4 -> stale. This is the leg firing."""
    m = gaf.measure(Path("."), _artifact(baseline_days=3), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 24)}))
    assert m.staleness_days == 4
    assert m.verdict == "stale"


def test_stalest_output_face_drives_the_verdict():
    """Two faces, one lagging -> the LAGGING one is used. Fails if `min` becomes `max`."""
    m = gaf.measure(Path("."), _artifact(outputs=("a.md", "b.html"), baseline_days=0),
                    git_date_fn=_fixed_dates({
                        "a.md": date(2026, 8, 10), "b.html": date(2026, 8, 23),
                        "in.md": date(2026, 8, 12)}))
    assert m.stalest_output == "a.md"
    assert m.staleness_days == 2 and m.verdict == "stale"


def test_newest_input_drives_the_verdict():
    """Several inputs, one moved -> the MOVED one is used. Fails if `max` becomes `min`."""
    m = gaf.measure(Path("."), _artifact(inputs=("x.md", "y.md"), baseline_days=0),
                    git_date_fn=_fixed_dates({
                        "out.md": date(2026, 8, 20), "x.md": date(2026, 8, 1),
                        "y.md": date(2026, 8, 22)}))
    assert m.newest_input == "y.md"
    assert m.staleness_days == 2 and m.verdict == "stale"


def test_unmeasurable_when_an_output_has_no_history(tmp_path):
    """An uncommitted artifact is a DIFFERENT defect (gen_dashboard --check reports MISSING);
    this leg refuses to invent a staleness number for it. The file EXISTS here, so the reason is
    `unavailable`-shaped, not subject-absent."""
    (tmp_path / "out.md").write_text("present but no history", encoding="utf-8")
    m = gaf.measure(tmp_path, _artifact(), git_date_fn=_fixed_dates({"in.md": date(2026, 8, 23)}))
    assert m.verdict == "unmeasurable" and m.staleness_days is None
    assert m.subject_absent is False
    assert "no git history for output out.md" in m.detail


def test_absent_output_is_subject_absent_not_merely_unavailable(tmp_path):
    """A consumer repo that simply has no dashboard must not be reported the same way as a repo
    whose git could not answer — collapsing the two is the 'skip rendered as pass' class."""
    m = gaf.measure(tmp_path, _artifact(), git_date_fn=_fixed_dates({"in.md": date(2026, 8, 23)}))
    assert m.verdict == "unmeasurable" and m.subject_absent is True
    assert "not present in this repo" in m.detail


def test_unmeasurable_when_no_input_has_history():
    m = gaf.measure(Path("."), _artifact(), git_date_fn=_fixed_dates({"out.md": date(2026, 8, 20)}))
    assert m.verdict == "unmeasurable" and m.staleness_days is None


def test_a_missing_input_does_not_suppress_the_others():
    """One unmapped input must not turn the whole measurement unmeasurable — otherwise deleting
    an input path would silently disarm the leg."""
    m = gaf.measure(Path("."), _artifact(inputs=("gone.md", "y.md"), baseline_days=0),
                    git_date_fn=_fixed_dates({
                        "out.md": date(2026, 8, 20), "y.md": date(2026, 8, 22)}))
    assert m.verdict == "stale" and m.newest_input == "y.md"


# --------------------------------------------------------------- WARN-only, by construction

def test_evaluate_never_returns_a_fail():
    """ADR-86's 2026-08-23 amendment arms this leg at WARN. RED is a later act with its own
    ruling — so `fails` is empty even on a wildly stale artifact."""
    stale = _artifact(baseline_days=0)
    fails, warns = gaf.evaluate(Path("."), (stale,), git_date_fn=_fixed_dates({
        "out.md": date(2026, 1, 1), "in.md": date(2026, 8, 23)}))
    assert fails == []
    expected = (date(2026, 8, 23) - date(2026, 1, 1)).days
    assert len(warns) == 1 and f"{expected}d stale" in warns[0]
    assert stale.regen_command in warns[0], "a WARN must carry its own discharge"


def test_evaluate_is_quiet_on_a_fresh_artifact():
    fails, warns = gaf.evaluate(Path("."), (_artifact(),), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 23), "in.md": date(2026, 8, 22)}))
    assert fails == [] and warns == []


def test_evaluate_is_quiet_when_unmeasurable():
    """Absence of evidence is not a finding — the audit leg renders this as `unavailable`."""
    fails, warns = gaf.evaluate(Path("."), (_artifact(),), git_date_fn=_fixed_dates({}))
    assert fails == [] and warns == []


# --------------------------------------------------------------- the registered subject

def test_dashboard_baseline_is_the_measured_value():
    """PINNED. 3 days is what the dashboard's staleness actually WAS at `aeec0fd1` on
    2026-08-23 (committed 2026-08-20, newest input 2026-08-23). Raising it silently rebases the
    metric the leg exists to hold, which is why the number is asserted and not merely commented."""
    assert gaf.DASHBOARD.baseline_days == 3


def test_dashboard_outputs_are_both_committed_faces():
    assert gaf.DASHBOARD.outputs == ("ecosystem/conformance.md", "ecosystem/conformance.html")


def test_input_set_agrees_with_the_generator():
    """The literal in the leg vs the generator's own declaration. The leg does not import
    `gen_dashboard` at runtime (it loads three sibling generators at module scope, and a gate
    must not call what it reports on) — so this test is where the two are held together."""
    import gen_dashboard
    assert gaf.DASHBOARD.inputs == gen_dashboard.INPUT_RELPATHS


def test_untracked_inputs_are_declared_rather_than_dropped():
    """The telemetry store is read by the generator but is gitignored, so it can carry no commit
    date. It is named in `untracked_inputs` so the carve-out is visible in the code."""
    import gen_dashboard
    assert gaf.DASHBOARD.untracked_inputs == (gen_dashboard.TELEMETRY_STORE_RELPATH,)
    assert gen_dashboard.TELEMETRY_STORE_RELPATH not in gaf.DASHBOARD.inputs


# --------------------------------------------------------------- live git: does it actually fire?

def _git(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _init_repo(base: Path, name: str = "repo") -> Path:
    repo = base / name
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    return repo


def _commit(repo: Path, rel: str, body: str, when: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    _git(repo, "add", "--", rel)
    # `--no-verify`: a globally-configured `core.hooksPath` would otherwise run the operator's
    # hooks inside these throwaway repos.
    _git(repo, "commit", "-q", "--no-verify", "--date", when, "-m", f"add {rel}")


def test_live_fires_on_a_genuinely_stale_tree(tmp_path):
    """ADR-81 leg (e) functional proof — observed firing, not observed presence."""
    repo = _init_repo(tmp_path)
    _commit(repo, "out.md", "artifact", "2026-08-10T12:00:00")
    _commit(repo, "in.md", "input moved on", "2026-08-20T12:00:00")
    m = gaf.measure(repo, _artifact())
    assert m.verdict == "stale", m.detail
    assert m.staleness_days == 10
    fails, warns = gaf.evaluate(repo, (_artifact(),))
    assert fails == [] and len(warns) == 1


def test_live_quiet_on_a_fresh_tree(tmp_path):
    repo = _init_repo(tmp_path)
    _commit(repo, "in.md", "input", "2026-08-10T12:00:00")
    _commit(repo, "out.md", "artifact regenerated after it", "2026-08-11T12:00:00")
    m = gaf.measure(repo, _artifact())
    assert m.verdict == "fresh", m.detail
    assert m.staleness_days == 0
    fails, warns = gaf.evaluate(repo, (_artifact(),))
    assert fails == [] and warns == []


def test_live_scrubs_an_inherited_git_dir(tmp_path, monkeypatch):
    """[#355]: an inherited GIT_DIR overrides BOTH `cwd=` and `git -C`, so a validator reads the
    PARENT repo while labelling the answer with the target's id. `gitenv` scrubs it; if that
    load ever silently became a no-op, this test reads `decoy`'s history and the date is wrong."""
    repo = _init_repo(tmp_path)
    _commit(repo, "out.md", "artifact", "2026-08-10T12:00:00")
    decoy = _init_repo(tmp_path, "decoy")
    _commit(decoy, "out.md", "decoy", "2020-01-01T12:00:00")
    monkeypatch.setenv("GIT_DIR", str(decoy / ".git"))
    assert gaf.git_last_commit_date(repo, "out.md") == date(2026, 8, 10)


def test_live_cli_exits_zero_even_when_stale(tmp_path):
    """WARN-only has teeth in one direction only: it must never block. A non-zero exit here
    would make the leg a commit gate by accident, which the contract forbids."""
    repo = _init_repo(tmp_path)
    _commit(repo, "ecosystem/conformance.md", "a", "2026-01-01T12:00:00")
    _commit(repo, "ecosystem/conformance.html", "b", "2026-01-01T12:00:00")
    _commit(repo, "BACKLOG.md", "c", "2026-08-23T12:00:00")
    r = subprocess.run([sys.executable, str(_MODULE)], cwd=str(repo),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "STALE" in r.stdout, r.stdout
