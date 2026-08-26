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

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import generated_artifact_freshness as gaf

_MODULE = Path(__file__).resolve().parent.parent / "scripts" / "generated_artifact_freshness.py"


def _fixed_dates(mapping: dict[str, date]):
    """A `git_date_fn` stand-in: pathspec -> date, None for anything unmapped.

    These pin the RELATION; WHICH git date the real function reads is pinned separately, against
    real git, by `test_live_a_cherry_picked_input_cannot_hide_behind_its_author_date`.
    """
    return lambda _repo, pathspec: mapping.get(pathspec)


def _artifact(**overrides) -> gaf.GeneratedArtifact:
    base = dict(name="probe", outputs=("out.md",), inputs=("in.md",), baseline_days=3,
                regen_command="python scripts/gen_dashboard.py --write")
    base.update(overrides)
    return gaf.GeneratedArtifact(**base)


def _tree(tmp_path: Path, artifact: gaf.GeneratedArtifact) -> Path:
    """A directory where the artifact's outputs actually EXIST.

    `measure` checks disk presence before it asks git, because `git log -1 -- <deleted-path>`
    answers with the deletion commit's date and a present-tense reading of that date would call a
    deleted artifact fresh (terra, 2026-08-23). So even the pure date-arithmetic tests have to
    materialize the outputs — the precondition is real, not a fixture detail.
    """
    for rel in artifact.outputs:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("artifact", encoding="utf-8")
    return tmp_path


# --------------------------------------------------------------- the relation, pinned to the day

def test_fresh_when_inputs_are_older_than_the_artifact(tmp_path):
    a = _artifact()
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 18)}))
    assert m.verdict == "fresh"
    assert m.staleness_days == 0, "an artifact newer than its inputs floors at 0, never negative"


def test_fresh_at_exactly_the_baseline(tmp_path):
    """BOUNDARY: baseline 3, staleness 3 -> fresh. Fails if the comparison is `>=`."""
    a = _artifact(baseline_days=3)
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 23)}))
    assert m.staleness_days == 3
    assert m.verdict == "fresh"


def test_stale_at_baseline_plus_one(tmp_path):
    """BOUNDARY: baseline 3, staleness 4 -> stale. This is the leg firing."""
    a = _artifact(baseline_days=3)
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "in.md": date(2026, 8, 24)}))
    assert m.staleness_days == 4
    assert m.verdict == "stale"


def test_stalest_output_face_drives_the_verdict(tmp_path):
    """Two faces, one lagging -> the LAGGING one is used. Fails if `min` becomes `max`."""
    a = _artifact(outputs=("a.md", "b.html"), baseline_days=0)
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "a.md": date(2026, 8, 10), "b.html": date(2026, 8, 23), "in.md": date(2026, 8, 12)}))
    assert m.stalest_output == "a.md"
    assert m.staleness_days == 2 and m.verdict == "stale"


def test_newest_input_drives_the_verdict(tmp_path):
    """Several inputs, one moved -> the MOVED one is used. Fails if `max` becomes `min`."""
    a = _artifact(inputs=("x.md", "y.md"), baseline_days=0)
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 20), "x.md": date(2026, 8, 1), "y.md": date(2026, 8, 22)}))
    assert m.newest_input == "y.md"
    assert m.staleness_days == 2 and m.verdict == "stale"


def test_an_output_present_but_never_committed_warns(tmp_path):
    """terra, 2026-08-23. `--check` does NOT catch this: it reports MISSING only for an ABSENT
    file, so a present-but-untracked artifact passes it. And "committed-generated" is the zone
    class's own claim, so an artifact that was never committed violates this leg's premise —
    reporting it as `unavailable` would let it ship green, because the ship-gate does not block
    on `unavailable`."""
    (tmp_path / "out.md").write_text("present but no history", encoding="utf-8")
    a = _artifact()
    m = gaf.measure(tmp_path, a, git_date_fn=_fixed_dates({"in.md": date(2026, 8, 23)}))
    assert m.verdict == "uncommitted", m.detail
    assert gaf.STATUS_FOR_VERDICT[m.verdict] == "warn"
    fails, warns = gaf.evaluate(tmp_path, (a,),
                                git_date_fn=_fixed_dates({"in.md": date(2026, 8, 23)}))
    assert fails == [] and len(warns) == 1


def test_an_unmeasurable_declared_input_is_unverifiable_not_fresh(tmp_path):
    """terra, 2026-08-23 — the gate excusing itself. An earlier version DROPPED inputs it could
    not measure and reported freshness from whatever remained, so if the input that had actually
    moved was the unreadable one, the artifact was called `fresh` on the strength of the others.
    A declared input that cannot be measured is a defect in the declaration; the relation over the
    survivors is not a freshness verdict and must not be presented as one."""
    a = _artifact(inputs=("readable.md", "no-history.md"))
    m = gaf.measure(_tree(tmp_path, a), a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 24), "readable.md": date(2026, 8, 1)}))
    assert m.verdict == "unverifiable", m.detail
    assert m.verdict != "fresh"
    assert "no-history.md" in m.detail
    assert gaf.STATUS_FOR_VERDICT[m.verdict] == "warn"


def test_absent_output_is_subject_absent_not_merely_unavailable(tmp_path):
    """A consumer repo that simply has no dashboard must not be reported the same way as a repo
    whose git could not answer — collapsing the two is the 'skip rendered as pass' class."""
    m = gaf.measure(tmp_path, _artifact(), git_date_fn=_fixed_dates({"in.md": date(2026, 8, 23)}))
    assert m.verdict == "unmeasurable" and m.subject_absent is True
    assert "not present in this repo" in m.detail


def test_a_deleted_output_is_reported_deleted_not_fresh(tmp_path):
    """terra, 2026-08-23 — the hole this verdict exists to close. `git log -1 -- <deleted-path>`
    answers with the DELETION commit's date, which is recent. An implementation that consulted
    disk only after git returned None would measure that recent date against older inputs and
    call a DELETED artifact **fresh** — silently disarming the ship-time signal for the exact
    event it should shout about. Presence is therefore checked first."""
    a = _artifact()  # note: `_tree` NOT called — the output is absent from the tree
    m = gaf.measure(tmp_path, a, git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 24), "in.md": date(2026, 8, 1)}))
    assert m.verdict == "deleted", m.detail
    assert m.verdict != "fresh"
    assert "MISSING from the tree but has git history" in m.detail
    fails, warns = gaf.evaluate(tmp_path, (a,), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 24), "in.md": date(2026, 8, 1)}))
    assert fails == [] and len(warns) == 1, "a deleted artifact must WARN, not pass silently"


def test_no_input_measurable_at_all_is_unverifiable(tmp_path):
    a = _artifact()
    m = gaf.measure(_tree(tmp_path, a), a,
                    git_date_fn=_fixed_dates({"out.md": date(2026, 8, 20)}))
    assert m.verdict == "unverifiable" and m.staleness_days is None


def test_every_warn_verdict_is_derived_from_the_status_table():
    """The table is the single place a verdict's meaning is decided. `WARN_VERDICTS` is derived
    from it so the two cannot drift, and every verdict `measure` can return must be IN it —
    an unmapped verdict would raise in the audit leg rather than pass silently, which is the
    point, but it should never get that far."""
    assert set(gaf.WARN_VERDICTS) == {
        v for v, s in gaf.STATUS_FOR_VERDICT.items() if s == "warn"}
    assert gaf.STATUS_FOR_VERDICT["fresh"] == "pass"
    # `content-stale` joined the set with [#590]: the EXACT verdict, distinct from `stale`
    # because that one is a DATE relation and can only say "an input moved since", while this
    # says "regenerating would change these bytes".
    assert set(gaf.WARN_VERDICTS) == {"stale", "deleted", "uncommitted", "unverifiable",
                                      "content-stale"}
    assert gaf.STATUS_FOR_VERDICT["unmeasurable"] == "unavailable"


# --------------------------------------------------------------- WARN-only, by construction

def test_evaluate_never_returns_a_fail(tmp_path):
    """ADR-86's 2026-08-23 amendment arms this leg at WARN. RED is a later act with its own
    ruling — so `fails` is empty even on a wildly stale artifact."""
    stale = _artifact(baseline_days=0)
    fails, warns = gaf.evaluate(_tree(tmp_path, stale), (stale,), git_date_fn=_fixed_dates({
        "out.md": date(2026, 1, 1), "in.md": date(2026, 8, 23)}))
    assert fails == []
    expected = (date(2026, 8, 23) - date(2026, 1, 1)).days
    assert len(warns) == 1 and f"{expected}d stale" in warns[0]
    assert stale.regen_command in warns[0], "a WARN must carry its own discharge"


def test_evaluate_is_quiet_on_a_fresh_artifact(tmp_path):
    a = _artifact()
    fails, warns = gaf.evaluate(_tree(tmp_path, a), (a,), git_date_fn=_fixed_dates({
        "out.md": date(2026, 8, 23), "in.md": date(2026, 8, 22)}))
    assert fails == [] and warns == []


def test_evaluate_is_quiet_only_when_there_is_nothing_to_govern(tmp_path):
    """The ONE quiet non-fresh case: the artifact does not exist in this repo at all (a consumer
    with no dashboard). Every other way of failing to measure is a WARN — an earlier version was
    quiet on all of them, which is how a gate excuses itself."""
    a = _artifact()   # `_tree` NOT called and no dates: nothing here to govern
    fails, warns = gaf.evaluate(tmp_path, (a,), git_date_fn=_fixed_dates({}))
    assert fails == [] and warns == []
    assert gaf.measure(tmp_path, a, git_date_fn=_fixed_dates({})).subject_absent is True


# --------------------------------------------------------------- the registered subject

def test_dashboard_baseline_is_the_measured_value():
    """PINNED. 4 days is what the dashboard's staleness actually WAS at `aeec0fd1`, measured
    WITH THIS MODULE'S OWN RELATION (committer date, `--first-parent`): outputs committed
    2026-08-20, newest input `docs/audits` committed 2026-08-24. Raising it silently rebases the
    metric the leg exists to hold, which is why the number is asserted and not merely commented.

    It read 3 until 2026-08-24 -- measured by the module's FIRST relation (author date, no
    `--first-parent`) and never re-derived when that relation was replaced. The constant outlived
    its measurement. This assertion is what makes the next such drift fail loudly."""
    assert gaf.DASHBOARD.baseline_days == 4


def test_dashboard_outputs_are_both_committed_faces():
    assert gaf.DASHBOARD.outputs == ("ecosystem/conformance.md", "ecosystem/conformance.html")


def test_input_set_agrees_with_the_generator():
    """The literal in the leg vs the generator's own declaration. The leg does not import
    `gen_dashboard` at runtime (it loads three sibling generators at module scope, and a gate
    must not call what it reports on) — so this test is where the two are held together."""
    import gen_dashboard
    assert gaf.DASHBOARD.inputs == gen_dashboard.INPUT_RELPATHS


def test_input_set_covers_the_code_that_renders_the_artifact():
    """terra, 2026-08-23. Data alone is not the input set: the generator and the parsers it
    borrows decide what is rendered, so a change to them makes the committed artifact stale."""
    import gen_dashboard
    for rel in gen_dashboard.CODE_INPUT_RELPATHS:
        assert rel in gaf.DASHBOARD.inputs, f"{rel} renders the artifact but is not an input"
    assert "scripts/gen_dashboard.py" in gaf.DASHBOARD.inputs


def test_untracked_inputs_are_declared_rather_than_dropped():
    """The telemetry store is read by the generator but is gitignored, so it can carry no commit
    date. It is named in `untracked_inputs` so the carve-out is visible in the code."""
    import gen_dashboard
    assert gaf.DASHBOARD.untracked_inputs == (gen_dashboard.TELEMETRY_STORE_RELPATH,)
    assert gen_dashboard.TELEMETRY_STORE_RELPATH not in gaf.DASHBOARD.inputs


# --------------------------------------------------------------- live git: does it actually fire?

def _git(repo: Path, *args, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env={**os.environ, **env} if env else None)


def _init_repo(base: Path, name: str = "repo") -> Path:
    repo = base / name
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    return repo


def _commit(repo: Path, rel: str, body: str, when: str,
            committer_when: str | None = None) -> None:
    """Commit `rel` with BOTH git dates pinned (committer defaults to the author date).

    Both are set on purpose. `git commit --date=` sets only the AUTHOR date and leaves the
    committer date at wall-clock now, and `measure` reads both — taking the later on the input
    side, so an author-date-only fixture would silently measure "today" and test nothing it meant
    to. Passing `committer_when` separately is how the cherry-pick test manufactures the exact
    divergence that behaviour exists for.
    """
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    _git(repo, "add", "--", rel)
    # `--no-verify`: a globally-configured `core.hooksPath` would otherwise run the operator's
    # hooks inside these throwaway repos.
    _git(repo, "commit", "-q", "--no-verify", "-m", f"add {rel}",
         env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": committer_when or when})


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


def _dashboard_repo(tmp_path: Path, *, outputs_at: str, inputs_at: str) -> Path:
    """A repo carrying the FULL declared `DASHBOARD` shape — every output and every declared
    input committed. All of them, because a declared input with no history is now `unverifiable`
    by design: an under-declared fixture would test the wrong thing.

    A directory input is seeded with a file inside it, which is what `git log -- <dir>` answers
    for. Inputs are committed first so `outputs_at` can be later or earlier as the test needs.
    """
    repo = _init_repo(tmp_path)
    for rel in gaf.DASHBOARD.inputs:
        seed = rel if rel.endswith((".md", ".py")) else f"{rel}/seed.md"
        _commit(repo, seed, "input", inputs_at)
    for rel in gaf.DASHBOARD.outputs:
        _commit(repo, rel, "artifact", outputs_at)
    return repo


def test_live_a_generator_source_change_alone_makes_the_artifact_stale(tmp_path):
    """terra, 2026-08-23 — the defect that would have made this leg decorative. NOTHING in the
    DATA moves here: only `scripts/gen_task_tree.py`, a parser the generator borrows. The rendered
    output would differ, so the committed artifact IS stale, and a data-only input set would have
    called it fresh forever."""
    repo = _dashboard_repo(tmp_path, inputs_at="2026-07-01T12:00:00",
                           outputs_at="2026-08-01T12:00:00")
    m = gaf.measure(repo, gaf.DASHBOARD)
    assert m.verdict == "fresh", f"precondition: nothing has moved yet — {m.detail}"

    _commit(repo, "scripts/gen_task_tree.py", "parser rewritten", "2026-08-20T12:00:00")

    m = gaf.measure(repo, gaf.DASHBOARD)
    assert m.verdict == "stale", m.detail
    assert m.newest_input == "scripts/gen_task_tree.py", m.detail
    assert m.staleness_days == 19


def test_live_quiet_on_a_fresh_tree(tmp_path):
    repo = _init_repo(tmp_path)
    _commit(repo, "in.md", "input", "2026-08-10T12:00:00")
    _commit(repo, "out.md", "artifact regenerated after it", "2026-08-11T12:00:00")
    m = gaf.measure(repo, _artifact())
    assert m.verdict == "fresh", m.detail
    assert m.staleness_days == 0
    fails, warns = gaf.evaluate(repo, (_artifact(),))
    assert fails == [] and warns == []


def test_live_a_cherry_picked_input_cannot_hide_behind_its_author_date(tmp_path):
    """terra, 2026-08-23. A cherry-picked or rebased commit keeps its ORIGINAL author date, so a
    relation built on author dates reads the wrong order: an input that landed in this history
    AFTER the artifact carries an older author date, and the artifact is called `fresh` while the
    checked-out input is genuinely newer. The leg reads COMMITTER date, which records when the
    commit landed HERE — the only ordering this relation is actually about."""
    repo = _init_repo(tmp_path)
    _commit(repo, "out.md", "artifact", "2026-08-10T12:00:00")
    # THE DIVERGENCE, manufactured: author date backdated well before the artifact (as a
    # cherry-pick preserves it), committer date after it (as the replay sets it).
    _commit(repo, "in.md", "cherry-picked from an old branch", "2026-07-01T12:00:00",
            committer_when="2026-08-22T12:00:00")

    assert gaf.git_last_commit_date(repo, "in.md") == date(2026, 8, 22), (
        "the leg must read the COMMITTER date (2026-08-22), not the author date (2026-07-01)")

    m = gaf.measure(repo, _artifact())
    assert m.verdict == "stale", (
        f"an input that landed after the artifact was reported {m.verdict}: {m.detail}")


def test_live_a_rebased_output_is_not_spuriously_stale(tmp_path):
    """The other direction, and why the min/max hybrid was retired (terra, 2026-08-23). A rebased
    or amended ARTIFACT keeps its old author date while landing after its inputs. Reading the
    author date on the output side would call it `stale` when it is the newest thing in the tree
    — a spurious WARN, which trains the operator to ignore the leg."""
    repo = _init_repo(tmp_path)
    _commit(repo, "in.md", "input", "2026-08-20T12:00:00")
    # Artifact regenerated and committed AFTER the input, but carrying an old author date.
    _commit(repo, "out.md", "artifact", "2026-07-01T12:00:00",
            committer_when="2026-08-21T12:00:00")

    m = gaf.measure(repo, _artifact())
    assert m.verdict == "fresh", (
        f"a rebased artifact newer than its inputs was reported {m.verdict}: {m.detail}")
    assert m.staleness_days == 0


def test_live_an_old_side_branch_input_merged_no_ff_counts_as_landing_today(tmp_path):
    """terra, 2026-08-23 — and this repo's mandated workflow is the failure case. Core-invariant
    #5 makes every change arrive by `--no-ff` merge. A plain `git log -1 -- <path>` follows the
    path INTO the side branch and reports the old feature commit, so a lane with three-week-old
    commits that merges today measures as three weeks old and the artifact is called `fresh`
    forever. `--first-parent` asks the right question: when did this land on THIS branch."""
    repo = _init_repo(tmp_path)
    _commit(repo, "in.md", "seed", "2026-07-01T12:00:00")
    _commit(repo, "out.md", "artifact regenerated", "2026-08-20T12:00:00")

    _git(repo, "checkout", "-q", "-b", "feat/old-lane")
    _commit(repo, "in.md", "worked on weeks ago", "2026-08-01T12:00:00")
    _git(repo, "checkout", "-q", "main")
    merge = _git(repo, "merge", "--no-ff", "--no-verify", "-m", "Merge branch 'feat/old-lane'",
                 "feat/old-lane",
                 env={"GIT_AUTHOR_DATE": "2026-08-24T12:00:00",
                      "GIT_COMMITTER_DATE": "2026-08-24T12:00:00"})
    assert merge.returncode == 0, merge.stdout + merge.stderr

    assert gaf.git_last_commit_date(repo, "in.md") == date(2026, 8, 24), (
        "the input landed at the MERGE (2026-08-24), not at its side-branch commit (2026-08-01)")
    m = gaf.measure(repo, _artifact())
    assert m.verdict == "stale", (
        f"an input merged in after the artifact was reported {m.verdict}: {m.detail}")
    assert m.staleness_days == 4


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
    repo = _dashboard_repo(tmp_path, inputs_at="2026-01-01T12:00:00",
                           outputs_at="2026-01-01T12:00:00")
    _commit(repo, "BACKLOG.md", "moved on", "2026-08-23T12:00:00")
    r = subprocess.run([sys.executable, str(_MODULE)], cwd=str(repo),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "STALE" in r.stdout, r.stdout
