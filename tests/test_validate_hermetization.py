"""Tests for scripts/validate_hermetization.py (#306 ADR-101 refusal gate).

Firing tests, not presence: the pure classifiers (Rule A top-level seal + Rule B audit
grammar/R4 casing) are exercised directly, and the prospective-only/grandfather behavior
is proven end-to-end against a REAL temp git repo (an added off-grammar file BLOCKS while
a modified grandfathered one PASSES).
"""

import importlib.util
import subprocess
import sys
from pathlib import Path


_P = Path(__file__).resolve().parent.parent / "scripts" / "validate_hermetization.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_hermetization", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_hermetization"] = module
    spec.loader.exec_module(module)
    return module


vh = _load()


# --- Rule A: top-level seal --------------------------------------------------

def test_rule_a_blocks_new_top_level_dir():
    assert vh.rule_a_violation("newpkg/mod.py") is not None
    assert "top-level directory" in vh.rule_a_violation("newpkg/mod.py")


def test_rule_a_blocks_new_top_level_file():
    r = vh.rule_a_violation("notes.txt")
    assert r is not None and "top-level file" in r


def test_rule_a_blocks_new_docs_genre_folder():
    r = vh.rule_a_violation("docs/proposals/2026-07-11-idea.md")
    assert r is not None and "genre folder" in r


def test_rule_a_allows_file_under_sanctioned_dir():
    assert vh.rule_a_violation("scripts/newmod.py") is None
    assert vh.rule_a_violation("tests/test_newmod.py") is None
    assert vh.rule_a_violation("deploy/manifest-v1.4.0.yaml") is None


def test_rule_a_allows_sanctioned_top_level_file():
    for f in ("pyproject.toml", "CLAUDE.md", ".gitignore", ".pre-commit-hooks.yaml"):
        assert vh.rule_a_violation(f) is None, f


def test_rule_a_allows_file_in_sanctioned_genre():
    assert vh.rule_a_violation("docs/audits/2026-07-11-technical-foo.md") is None
    assert vh.rule_a_violation("docs/decisions/ADR-102-thing.md") is None


def test_rule_a_allows_file_directly_under_docs_root():
    # ADR-101 section 3 Rule A enumerates: new top-level dir / file / genre FOLDER. A file
    # directly under docs/ introduces no new genre folder, so Rule A is silent (literal spec).
    assert vh.rule_a_violation("docs/ORGAN-INDEX.md") is None


# --- Rule B: audit grammar + R4 casing ---------------------------------------

def test_rule_b_blocks_uppercase_underscore_corp_class():
    # The motivating fixture: the corp-monorepo UPPERCASE _AUDIT_/_BRIEF_ divergence (R4).
    r = vh.rule_b_violation("docs/audits/2026-07-11-TECHNICAL_AUDIT_BRIEF.md")
    assert r is not None and "casing" in r


def test_rule_b_blocks_underscore_lowercase():
    r = vh.rule_b_violation("docs/audits/2026-07-11-technical_foo.md")
    assert r is not None and "casing" in r


def test_rule_b_blocks_off_enum_class():
    r = vh.rule_b_violation("docs/audits/2026-07-11-bogusclass-foo.md")
    assert r is not None and "class" in r


def test_rule_b_blocks_missing_date():
    r = vh.rule_b_violation("docs/audits/technical-foo.md")
    assert r is not None and "grammar" in r


def test_rule_b_allows_valid_technical():
    assert vh.rule_b_violation("docs/audits/2026-07-11-technical-foo.md") is None


def test_rule_b_allows_degenerate_recurring_no_slug():
    assert vh.rule_b_violation("docs/audits/2026-06-14-ecosystem-audit.md") is None


def test_rule_b_allows_longest_match_multiword_class():
    # conformance-nightly-digest must whole-token match, NOT split on the first hyphen.
    assert vh.rule_b_violation(
        "docs/audits/2026-07-11-conformance-nightly-digest-delta.md") is None
    assert vh.rule_b_violation("docs/audits/2026-07-11-changelog-review-2.1.204.md") is None


def test_rule_b_allows_dot_slug_carveout():
    # `.` allowed inside the slug for repo/version tokens (S3-1 carve-out).
    assert vh.rule_b_violation("docs/audits/2026-07-11-technical-v3.4-abort.md") is None
    assert vh.rule_b_violation(
        "docs/audits/2026-07-11-census-.dev-knowledge-sweep.md") is None


def test_rule_b_allows_codex_and_fresh_eyes():
    assert vh.rule_b_violation("docs/audits/2026-07-11-codex-boundary.md") is None
    assert vh.rule_b_violation("docs/audits/2026-06-01-fresh-eyes-review.md") is None


def test_rule_b_shape_only_never_date_accuracy():
    # `2026-13-99` is an impossible date but a VALID shape -> passes (S3-4: shape only).
    assert vh.rule_b_violation("docs/audits/2026-13-99-technical-x.md") is None


def test_rule_b_silent_on_non_audit_paths():
    assert vh.rule_b_violation("docs/audits/README.md") is None      # the generated index
    assert vh.rule_b_violation("docs/decisions/ADR-102-x.md") is None  # different genre
    assert vh.rule_b_violation("scripts/x.py") is None


# --- classify / check aggregation --------------------------------------------

def test_classify_rule_a_precedes_rule_b():
    # An off-grammar name under an UNSANCTIONED genre is caught by Rule A first.
    r = vh.classify("docs/proposals/2026-07-11-TECHNICAL_X.md")
    assert r is not None and "genre folder" in r


def test_check_aggregates_and_labels():
    reasons = vh.check([
        "scripts/ok.py",                                        # clean
        "newdir/bad.py",                                        # rule A
        "docs/audits/2026-07-11-BADCLASS.md",                   # rule B casing
    ])
    assert len(reasons) == 2
    assert any(r.startswith("newdir/bad.py:") for r in reasons)
    assert any(r.startswith("docs/audits/2026-07-11-BADCLASS.md:") for r in reasons)


def test_check_empty_is_clean():
    assert vh.check([]) == []
    assert vh.check(["scripts/a.py", "docs/audits/2026-07-11-technical-a.md"]) == []


# --- prospective-only / grandfather: REAL temp git repo ----------------------

def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(["git", "-C", str(repo), *args],
                         capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0, f"git {args} failed: {out.stderr}"
    return out.stdout


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "docs" / "audits").mkdir(parents=True)
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "seed.txt")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


def _run_hook(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(_P)], cwd=str(repo),
                          capture_output=True, text=True, encoding="utf-8")


def test_prospective_grandfathers_modified_existing(tmp_path):
    # A mis-named audit file that ALREADY EXISTS (committed) is grandfathered: modifying
    # and staging it is status M, not A, so the gate is silent.
    repo = _init_repo(tmp_path)
    bad = repo / "docs" / "audits" / "BADNAME_UPPER.md"
    bad.write_text("# grandfathered\n", encoding="utf-8")
    _git(repo, "add", "-f", str(bad))            # force past any consumer .gitignore
    _git(repo, "commit", "-q", "-m", "grandfather the bad name")
    bad.write_text("# grandfathered, edited\n", encoding="utf-8")
    _git(repo, "add", "-f", str(bad))            # staged as MODIFIED
    res = _run_hook(repo)
    assert res.returncode == 0, res.stderr


def test_blocks_newly_added_off_grammar_audit(tmp_path):
    repo = _init_repo(tmp_path)
    new = repo / "docs" / "audits" / "2026-07-11-TECHNICAL_AUDIT.md"
    new.write_text("# new bad\n", encoding="utf-8")
    _git(repo, "add", str(new))
    res = _run_hook(repo)
    assert res.returncode == 1
    assert "casing" in res.stderr


def test_blocks_newly_added_top_level_dir(tmp_path):
    repo = _init_repo(tmp_path)
    (repo / "sandbox").mkdir()
    f = repo / "sandbox" / "x.py"
    f.write_text("x = 1\n", encoding="utf-8")
    _git(repo, "add", str(f))
    res = _run_hook(repo)
    assert res.returncode == 1
    assert "top-level directory" in res.stderr


def test_allows_newly_added_conformant(tmp_path):
    repo = _init_repo(tmp_path)
    good1 = repo / "docs" / "audits" / "2026-07-11-technical-clean.md"
    good1.write_text("# ok\n", encoding="utf-8")
    good2 = repo / "scripts"
    good2.mkdir()
    (good2 / "newmod.py").write_text("y = 2\n", encoding="utf-8")
    _git(repo, "add", str(good1), str(good2 / "newmod.py"))
    res = _run_hook(repo)
    assert res.returncode == 0, res.stderr


def test_main_fail_open_on_git_error(monkeypatch, capsys):
    def _boom():
        raise RuntimeError("simulated git failure")

    monkeypatch.setattr(vh, "staged_added_paths", _boom)
    assert vh.main() == 0                          # fail OPEN
    assert "skipped" in capsys.readouterr().err    # but LOUD
