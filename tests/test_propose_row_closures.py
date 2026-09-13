"""Coverage for scripts/propose_row_closures.py -- [#730] AX16-2/AX27-5 witness scan."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import propose_row_closures as prc  # noqa: E402

_ROW1 = "- [#1] [P1][S] **A** — body · Done when: a is done\n"
_ROW2 = "- [#2] [P1][S] **B** — body · Done when: b is done\n"
_HEADER = "# T\n\n## [E1] One\n\n### [S1] Story\n"


def _git(repo, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _write_manifest(repo: Path, ids: list[int]) -> None:
    manifest = {
        "schema": 2, "role": "source-of-truth", "generates": "BACKLOG.md",
        "generated_sha256": "0" * 64, "generator": "scripts/gen_task_tree.py",
        "nodes": [{"task": i, "file": f"{i}-x.md"} for i in ids],
    }
    (repo / "tasks").mkdir(exist_ok=True)
    (repo / "tasks" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _commit(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    r = _git(repo, "commit", "-q", "--no-verify", "-m", message)
    assert r.returncode == 0, r.stdout + r.stderr
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _closure_fixture(tmp_path: Path) -> Path:
    """main: commit A (rows #1, #2) -> commit B (row #1 removed, simulating a close).
    A `lane` branch forks from commit A -- pre-removal, so #1 still reads OPEN there -- and
    is left checked out as the CURRENT branch, with tasks/manifest.json on disk listing #1,
    #2 AND #3 (an id `main` never touched at all, the no-witness control)."""
    repo = tmp_path
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")

    (repo / "BACKLOG.md").write_text(_HEADER + _ROW1 + _ROW2, encoding="utf-8", newline="\n")
    sha_a = _commit(repo, "commit A -- #1 and #2 open")

    _git(repo, "checkout", "-q", "-b", "lane", sha_a)

    (repo / "BACKLOG.md").write_text(_HEADER + _ROW2, encoding="utf-8", newline="\n")
    _git(repo, "checkout", "-q", "main")
    _commit(repo, "commit B -- closes [#1]")
    _git(repo, "checkout", "-q", "lane")

    _write_manifest(repo, [1, 2, 3])
    return repo


def test_witnessed_closures_finds_the_row_main_already_closed(tmp_path):
    repo = _closure_fixture(tmp_path)
    rows = prc.witnessed_closures(repo, "main")
    assert [r.id for r in rows] == [1]
    assert rows[0].gain == "a is done"
    assert len(rows[0].sha) == 12


def test_witnessed_closures_refuses_a_row_the_compare_ref_never_touched(tmp_path):
    """[#3] is open here and never appears anywhere on `main`'s BACKLOG.md history -- AX10-1's
    load-bearing clause: no witness, no listing."""
    repo = _closure_fixture(tmp_path)
    rows = prc.witnessed_closures(repo, "main")
    assert 3 not in [r.id for r in rows]


def test_witnessed_closures_leaves_a_row_open_on_both_sides_unlisted(tmp_path):
    """[#2] is open on `lane` (here) AND still open on `main` -- nothing to witness."""
    repo = _closure_fixture(tmp_path)
    rows = prc.witnessed_closures(repo, "main")
    assert 2 not in [r.id for r in rows]


def test_witnessed_closures_returns_empty_when_nothing_is_open_here(tmp_path):
    repo = _closure_fixture(tmp_path)
    _write_manifest(repo, [])
    assert prc.witnessed_closures(repo, "main") == []


def test_open_ids_at_ref_reads_head_from_the_working_tree_not_a_commit(tmp_path):
    """HEAD is read off DISK, so an in-progress (uncommitted) close_row plan is reflected
    immediately -- not only after its own commit lands."""
    repo = _closure_fixture(tmp_path)
    git = prc._gd.GitReader(repo)
    assert prc.open_ids_at_ref(repo, git, "HEAD") == {1, 2, 3}
    _write_manifest(repo, [2, 3])  # uncommitted edit -- #1 "closed" in the working tree only
    assert prc.open_ids_at_ref(repo, git, "HEAD") == {2, 3}


def test_render_closure_list_reports_zero_honestly():
    text = prc.render_closure_list([], "main", "2026-09-13")
    assert "0 rows witnessed this run" in text
    assert "2026-09-13" in text


def test_render_closure_list_names_id_done_when_and_sha():
    row = prc._gd.ClosedRow(id=7, title="Widget", gain="it works", theme=None,
                            closed_on="2026-09-01", sha="abc1234def0")
    text = prc.render_closure_list([row], "main", "2026-09-13")
    assert "[#7]" in text and "Widget" in text
    assert "it works" in text
    assert "abc1234def0" in text
    assert "2026-09-01" in text


def test_main_writes_the_default_dated_output_path(tmp_path, monkeypatch):
    """The default output path is the operator TRANSPORT's to-browser/, not a path inside
    this git tree -- landing one inside the tree is exactly the unsanctioned-new-top-level-
    directory shape ADR-101 hermetization refuses."""
    repo = _closure_fixture(tmp_path)
    transport = tmp_path.parent / "fake-transport"
    transport.mkdir(exist_ok=True)
    monkeypatch.setattr(prc._gh, "transport_root", lambda: transport)
    import datetime as _dt
    fixed = _dt.date(2026, 9, 13)

    class _FixedDate(_dt.date):
        @classmethod
        def today(cls):
            return fixed

    monkeypatch.setattr(prc._dt, "date", _FixedDate)
    assert prc.main(["--repo-root", str(repo), "--compare-ref", "main"]) == 0
    out = transport / "to-browser" / "CLOSURE-LIST-2026-09-13.md"
    assert out.exists()
    assert "[#1]" in out.read_text(encoding="utf-8")
    assert not (repo / "to-browser").exists()


def test_main_refuses_when_no_transport_and_no_out(tmp_path, monkeypatch):
    repo = _closure_fixture(tmp_path)
    monkeypatch.setattr(prc._gh, "transport_root", lambda: None)
    assert prc.main(["--repo-root", str(repo), "--compare-ref", "main"]) == 1
    assert not (repo / "to-browser").exists()


def test_main_degrades_honestly_when_no_comparison_ref_resolves(tmp_path):
    """A fresh checkout with no `main` (or an unresolvable --compare-ref) must not crash --
    it writes a list saying so and exits 0, matching this module's read-only, never-repair
    posture (it reports; a caller decides what to do about a missing ref)."""
    repo = tmp_path
    _git(repo, "init", "-q", "-b", "solo")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    (repo / "BACKLOG.md").write_text(_HEADER + _ROW1, encoding="utf-8", newline="\n")
    _commit(repo, "only commit, no main")
    _write_manifest(repo, [1])

    out_path = repo / "out.md"
    assert prc.main(["--repo-root", str(repo), "--out", str(out_path),
                     "--compare-ref", "does-not-exist"]) == 0
    assert "Could not resolve" in out_path.read_text(encoding="utf-8")
