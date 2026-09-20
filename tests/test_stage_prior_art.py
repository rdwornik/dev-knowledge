"""lane-l7-prior-art: spine stage 2 searches our own archive, not just commit messages.

RED-FIRST (ADR-108 §B): authored and witnessed FAILING before `scripts/stage_prior_art.py` existed
and before `ecosystem/harness.yaml` stage 2 pointed at it; the RED output is quoted in the RED
commit body.

The defect (RECON-NIGHT-2026-09-20 §3): stage 2 was `git log --grep=<subject> -- tasks scripts
protocols` -- commit MESSAGES only, and never `docs/audits/` or `docs/archive/`, which is where the
answers this project paid for twice were. So the fixtures here are the three shapes the contract
names -- prior art only in an audit, prior art only in a commit message, prior art nowhere -- and
the stage-2 row is exercised under the real spine, not just parsed.

The audit fixture is a REAL record from 2026-09-20, copied out of the checkout, so the test cannot
pass on a hand-made file that happens to match the parser.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_DODO = _SCRIPTS / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

# A real 2026-09-20 record, and a term that occurs in it and (deliberately) nowhere in the roots
# a git-log search would have looked at.
_RECORD = "2026-09-20-technical-loop-eval-mapping.md"
_RECORD_TERM = "BECOMES-STAGE-13"


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                   check=True, capture_output=True, text=True)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A throwaway git repo with the three roots present and one unrelated commit."""
    _git(tmp_path, "init", "-q")
    for sub in ("docs/audits", "docs/archive", "tasks", "scripts", "protocols"):
        (tmp_path / sub).mkdir(parents=True)
    (tmp_path / "tasks" / "unrelated.md").write_text("nothing to see\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "chore: seed")
    return tmp_path


def _spa():
    import stage_prior_art
    return stage_prior_art


def _emit(root: Path, subject: str, *extra: str):
    return CliRunner().invoke(_spa().cli, ["emit", "--subject", subject, "--root", str(root), *extra])


# --- Done-contract 5a: prior art that exists only in docs/audits/ is found -----------------------

def test_the_real_2026_09_20_record_is_the_fixture_and_still_exists():
    assert (_REPO / "docs" / "audits" / _RECORD).is_file()
    assert _RECORD_TERM in (_REPO / "docs" / "audits" / _RECORD).read_text(encoding="utf-8")


def test_a_subject_whose_prior_art_is_only_in_docs_audits_is_found(repo):
    shutil.copy(_REPO / "docs" / "audits" / _RECORD, repo / "docs" / "audits" / _RECORD)
    result = _emit(repo, _RECORD_TERM)
    assert result.exit_code == 0, result.output
    hits = [ln for ln in result.output.splitlines() if ln.startswith("candidate:")]
    assert hits, result.output
    assert any(f"docs/audits/{_RECORD}:" in ln for ln in hits), hits
    # the locator is enough to open it: path:LINE, and the line really holds the term
    path, line = re.search(rf"(docs/audits/{re.escape(_RECORD)}):(\d+):", "\n".join(hits)).groups()
    text = (repo / path).read_text(encoding="utf-8").splitlines()[int(line) - 1]
    assert _RECORD_TERM.lower() in text.lower()
    assert "NONE FOUND" not in result.output


def test_docs_archive_is_searched_too(repo):
    (repo / "docs" / "archive" / "2026-01-01-old.md").write_text("we settled the flurbo question\n",
                                                                 encoding="utf-8")
    result = _emit(repo, "FLURBO")
    assert result.exit_code == 0, result.output
    assert "docs/archive/2026-01-01-old.md:1:" in result.output


def test_the_search_is_case_insensitive_and_matches_a_file_name(repo):
    (repo / "docs" / "audits" / "2026-09-01-technical-zorblax-review.md").write_text("body\n", encoding="utf-8")
    result = _emit(repo, "ZORBLAX")
    assert "docs/audits/2026-09-01-technical-zorblax-review.md" in result.output


# --- Done-contract 5b: prior art that is only a commit message is still found ---------------------

def test_a_subject_whose_prior_art_is_only_a_commit_message_is_still_found(repo):
    (repo / "tasks" / "row.md").write_text("row\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "feat: introduce the quuxwidget organ")
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=repo, capture_output=True,
                         text=True, check=True).stdout.strip()
    result = _emit(repo, "quuxwidget")
    assert result.exit_code == 0, result.output
    commit_lines = [ln for ln in result.output.splitlines() if ln.startswith("candidate:") and "commit" in ln]
    assert len(commit_lines) == 1, result.output
    assert sha in commit_lines[0], "the locator must let the reader `git show` it"
    assert "tasks/row.md" in commit_lines[0], "a commit candidate carries a path it touched"
    assert "NONE FOUND" not in result.output


def test_commit_history_keeps_todays_roots_only(repo):
    """The git leg is 'as today': a commit that touched only docs/ is outside its pathspec."""
    (repo / "docs" / "note.md").write_text("n\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "docs: the plughtwist note")
    result = _emit(repo, "plughtwist")
    assert "NONE FOUND" in result.output


# --- Done-contract 3: a negative answer is explicit -----------------------------------------------

def test_a_subject_with_no_prior_art_yields_an_explicit_negative_that_names_what_ran(repo):
    term = "zqxv-" + uuid.uuid4().hex
    result = _emit(repo, term)
    assert result.exit_code == 0, "absence is a recorded answer, not a refusal"
    assert "NONE FOUND" in result.output
    assert term in result.output, "the receipt must name the term searched"
    for root in ("docs/audits", "docs/archive", "git-log"):
        assert root in result.output, f"the negative must name the root {root}: {result.output}"
    assert "candidate:" not in result.output


def test_a_root_that_does_not_exist_is_recorded_as_absent_not_as_searched(repo):
    shutil.rmtree(repo / "docs" / "archive")
    result = _emit(repo, "zqxv-" + uuid.uuid4().hex)
    assert result.exit_code == 0
    assert re.search(r"docs/archive\S*\s*\(?absent", result.output), result.output


def test_an_empty_subject_is_refused_because_it_would_match_everything(repo):
    result = _emit(repo, "   ")
    assert result.exit_code != 0


# --- Done-contract 4: bounded and timed -----------------------------------------------------------

def test_the_result_count_is_bounded_and_says_it_truncated(repo):
    for i in range(30):
        (repo / "docs" / "audits" / f"2026-09-{i:02d}-many.md").write_text("the manyhit term\n", encoding="utf-8")
    result = _emit(repo, "manyhit", "--limit", "5")
    assert result.exit_code == 0, result.output
    assert len([ln for ln in result.output.splitlines() if ln.startswith("candidate:")]) == 5
    assert re.search(r"found=30\b", result.output), result.output
    assert "truncated=yes" in result.output
    assert "truncated=no" in _emit(repo, "manyhit", "--limit", "50").output


def test_a_non_ascii_snippet_survives_a_piped_windows_stdout(repo):
    """The receipt's stdout file is a pipe (cp1252 on Windows); a real audit line holds an arrow."""
    (repo / "docs" / "audits" / "2026-09-02-arrow.md").write_text("verdict → zyxwarrow kept\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_SCRIPTS / "stage_prior_art.py"), "emit", "--subject",
                           "zyxwarrow", "--root", str(repo)], capture_output=True, timeout=60)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    assert "→ zyxwarrow".encode("utf-8") in proc.stdout


def test_its_own_runtime_is_recorded(repo):
    result = _emit(repo, "zqxv-" + uuid.uuid4().hex)
    assert re.search(r"runtime_ms=\d+", result.output), result.output


def test_the_real_checkout_search_is_fast_enough_for_a_stage():
    """A stage that costs seconds is skipped by a tired operator; 1,000+ audits must stay inside 5s."""
    started = subprocess.run([sys.executable, str(_SCRIPTS / "stage_prior_art.py"), "emit", "--subject",
                              "zqxv-" + uuid.uuid4().hex, "--root", str(_REPO)],
                             capture_output=True, text=True, timeout=60)
    assert started.returncode == 0, started.stderr
    ms = int(re.search(r"runtime_ms=(\d+)", started.stdout).group(1))
    assert ms < 5000, f"{ms} ms"


def test_the_real_checkout_finds_the_real_record():
    """The archive really is searched -- not only the tmp fixture."""
    out = subprocess.run([sys.executable, str(_SCRIPTS / "stage_prior_art.py"), "emit", "--subject",
                          _RECORD_TERM, "--root", str(_REPO)], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    assert f"docs/audits/{_RECORD}:" in out.stdout


# --- Done-contract 2 + 5d: stage 2 points at it and still runs under the spine --------------------

def _stage2() -> dict:
    stages = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["stages"]
    return next(s for s in stages if s["stage"] == 2)


def test_stage_2_row_keeps_its_stage_field_and_kind_and_points_at_the_script():
    row = _stage2()
    assert (row["stage"], row["name"], row["field"], row["kind"]) == (2, "prior-art", "prior-art", "deterministic")
    assert "scripts/stage_prior_art.py" in row["command"]
    assert row["command"][:4] == ["uv", "run", "--locked", "python"], "mirror stage 6's invocation"
    assert "{subject}" in " ".join(row["command"]), "the subject must reach the script"
    assert (_REPO / "scripts" / "stage_prior_art.py").is_file()


def test_the_other_eleven_stages_are_untouched_by_this_lane():
    """Only stage 2's line may differ from main: pin the neighbours' commands by their script names."""
    stages = {s["stage"]: s for s in yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["stages"]}
    assert stages[1]["command"][:4] == ["git", "--no-pager", "grep", "-n"]
    assert "scripts/stage_library_first.py" in stages[6]["command"]
    assert "scripts/validate_substrate.py" in stages[7]["command"]
    assert sorted(stages) == list(range(1, 13))


def _run_stage_2(tmp: Path, subject: str) -> tuple[subprocess.CompletedProcess, dict, str]:
    env = {**os.environ, "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": subject, "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")}
    env.pop("HARNESS_YAML", None)
    proc = subprocess.run([sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(tmp),
                           "--db-file", str(tmp / ".doit.db"), "-s", "stage:02-prior-art"],
                          capture_output=True, text=True, env=env, cwd=tmp, timeout=300)
    receipts = sorted((tmp / "receipts").glob("*PRIOR-ART*.json"))
    assert receipts, (proc.stdout, proc.stderr, sorted(p.name for p in (tmp / "receipts").glob("*")))
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    output = (tmp / "receipts" / receipt["output_file"]).read_text(encoding="utf-8")
    return proc, receipt, output


def test_stage_2_runs_under_the_real_spine_and_records_a_candidate(tmp_path):
    proc, receipt, output = _run_stage_2(tmp_path, _RECORD_TERM)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert receipt["exit_code"] == 0 and receipt["status"] == "ok"
    assert f"docs/audits/{_RECORD}:" in output


def test_stage_2_under_the_spine_turns_nothing_found_into_a_receipt_not_a_failure(tmp_path):
    term = "zqxv-" + uuid.uuid4().hex
    proc, receipt, output = _run_stage_2(tmp_path, term)
    assert proc.returncode == 0, "nothing found must not fail the stage"
    assert receipt["exit_code"] == 0 and receipt["status"] == "ok"
    assert "NONE FOUND" in output and term in output
