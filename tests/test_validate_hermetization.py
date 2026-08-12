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


def test_rule_a_blocks_collapsed_runbooks_genre():
    # ADR-101 amendment 2026-07-22: d.i REVERSED -- `runbooks` LEFT SANCTIONED_GENRES
    # (the one-member genre collapsed into protocols/REPO_ONBOARDING.md). Re-creating
    # the genre is a surfaced, gated act, not a silent one.
    assert "runbooks" not in vh.SANCTIONED_GENRES
    r = vh.rule_a_violation("docs/runbooks/repo-onboarding.md")
    assert r is not None and "genre folder" in r


def test_rule_a_allows_file_under_sanctioned_dir():
    assert vh.rule_a_violation("scripts/newmod.py") is None
    assert vh.rule_a_violation("tests/test_newmod.py") is None
    assert vh.rule_a_violation("deploy/manifest-v1.4.0.yaml") is None


def test_rule_a_allows_tasks_dir():
    # tasks/: ADR-101 amendment 2026-07-27 ([#433]) -- the DERIVED per-task tree
    # emitted from BACKLOG.md joined the sanctioned Tier-1 directories (the closed
    # set grew by amendment, never a drive-by add; source of truth stays BACKLOG.md
    # until the flip arc).
    assert "tasks" in vh.SANCTIONED_TIER1_DIRS
    assert vh.rule_a_violation("tasks/433-backlog-restructure.md") is None
    assert vh.rule_a_violation("tasks/manifest.json") is None
    assert vh.rule_a_violation("tasks/README.md") is None


def test_rule_a_allows_github_workflows_dir():
    # .github/: ADR-101 amendment 2026-08-06 ([#501]) -- the server-side REPORT-ONLY
    # recorder joined the sanctioned Tier-1 directories. The directory is NOT virgin
    # ground: it existed and was deleted at `82227f08` under [#255] because a
    # PR-triggered organ never fired under a local-merge workflow. It returns on a
    # `push` trigger, and only for the report-only wall.
    assert ".github" in vh.SANCTIONED_TIER1_DIRS
    assert vh.rule_a_violation(".github/workflows/report-only-wall.yml") is None


def test_rule_a_allows_sanctioned_top_level_file():
    # uv.lock + .python-version: ADR-101 amendment 2026-07-27 ([#432]/ADR-106) --
    # the uv toolchain's lockfile + interpreter pin joined the build/package class.
    for f in ("pyproject.toml", "CLAUDE.md", ".gitignore", ".pre-commit-hooks.yaml",
              "uv.lock", ".python-version"):
        assert vh.rule_a_violation(f) is None, f


def test_rule_a_allows_root_methodology_yaml_section_9a():
    # ADR-101 amendment 2026-07-13 ([#328]): intake #12 section 9a (SETTLED 2026-07-12)
    # rules the hub carries its OWN .methodology.yaml as a fleet member -- the closed
    # Tier-1 file class grew by amendment, never a drive-by add.
    assert vh.rule_a_violation(".methodology.yaml") is None


def test_rule_a_allows_file_in_sanctioned_genre():
    assert vh.rule_a_violation("docs/audits/2026-07-11-technical-foo.md") is None
    assert vh.rule_a_violation("docs/decisions/ADR-102-thing.md") is None


def test_rule_a_allows_file_directly_under_docs_root_but_rule_c_does_not():
    # ADR-101 section 3 Rule A enumerates: new top-level dir / file / genre FOLDER. A file
    # directly under docs/ introduces no new genre folder, so Rule A is silent (literal spec).
    # THAT SILENCE IS HOW docs/ORGAN-INDEX.md WAS BORN. Rule A's reading is kept exactly as
    # it was -- the fix is a new leg, not a re-interpretation of an existing one -- and this
    # test now pins BOTH halves so neither can drift into the other.
    assert vh.rule_a_violation("docs/ORGAN-INDEX.md") is None
    assert vh.rule_c_violation("docs/ORGAN-INDEX.md") is not None
    assert vh.classify("docs/ORGAN-INDEX.md") is not None


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


# --- Rule B: codex-review 2026-07-11 hardening (uppercase .MD / malformed slug) ---

def test_rule_b_blocks_uppercase_md_extension():
    # An uppercase .MD extension must NOT dodge Rule B (apply is extension-case-insensitive).
    r = vh.rule_b_violation("docs/audits/2026-07-11-technical-good.MD")
    assert r is not None and "casing" in r


def test_rule_b_blocks_empty_slug():
    r = vh.rule_b_violation("docs/audits/2026-07-11-technical-.md")
    assert r is not None and "slug" in r


def test_rule_b_blocks_malformed_slug_double_and_trailing_hyphen():
    assert "slug" in vh.rule_b_violation("docs/audits/2026-07-11-technical--foo.md")
    assert "slug" in vh.rule_b_violation("docs/audits/2026-07-11-technical-foo-.md")


def test_rule_b_wellformed_multi_segment_slug_passes():
    assert vh.rule_b_violation("docs/audits/2026-07-11-technical-a-b-c.md") is None


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


def test_rename_to_bad_audit_name_is_blocked(tmp_path):
    # codex-review 2026-07-11: a rename INTRODUCES a new pathname; --no-renames surfaces it
    # as an ADD so the off-grammar destination is policed (not silently skipped as status R).
    repo = _init_repo(tmp_path)
    good = repo / "docs" / "audits" / "2026-07-11-technical-ok.md"
    good.write_text("# ok\n", encoding="utf-8")
    _git(repo, "add", str(good))
    _git(repo, "commit", "-q", "-m", "add a good audit")
    _git(repo, "mv", str(good), str(repo / "docs" / "audits" / "2026-07-11-BAD_RENAME.md"))
    res = _run_hook(repo)
    assert res.returncode == 1
    assert "casing" in res.stderr


def test_main_fail_open_on_git_error(monkeypatch, capsys):
    def _boom():
        raise RuntimeError("simulated git failure")

    monkeypatch.setattr(vh, "staged_added_paths", _boom)
    assert vh.main() == 0                          # fail OPEN
    assert "skipped" in capsys.readouterr().err    # but LOUD


# --- Rule C: the home allowlist (operator ruling A 2026-08-11; register K-1) --

def test_rule_c_blocks_a_file_loose_at_the_docs_root():
    """The seeded out-of-home file REDs -- the exact breach the ruling corrects."""
    r = vh.rule_c_violation("docs/stray-note.md")
    assert r is not None
    assert "new path outside allowlisted homes -- operator approval required" in r
    assert "'docs/'" in r


def test_rule_c_admits_the_relocated_organ_index():
    """The organ-index move PASSES: ecosystem/ is an allowlisted home."""
    assert vh.rule_c_violation("ecosystem/organ-index.md") is None
    assert vh.classify("ecosystem/organ-index.md") is None


def test_rule_c_blocks_a_new_package_dir_under_an_allowlisted_parent():
    # scripts/ is sanctioned and scripts/codemap|hooks|toc are known homes; a NEW package
    # dir is a deliberate act (it adds a codemap node), so it is surfaced rather than added.
    assert vh.rule_c_violation("scripts/newpkg/mod.py") is not None
    assert vh.rule_c_violation("scripts/codemap/mod.py") is None


def test_rule_c_admits_open_homes_the_repo_creates_routinely():
    # Handoff bundles and fixture trees are created constantly; gating them would make the
    # organ a nuisance. `**` admits arbitrary depth below those two roots BY DESIGN.
    assert vh.rule_c_violation("docs/handoffs/2026-08-12-dev-knowledge-architect/README.md") is None
    assert vh.rule_c_violation("docs/handoffs/archive/legacy/old/x.md") is None
    assert vh.rule_c_violation("tests/fixtures/brand-new-tree/src/pkg/mod.py") is None
    assert vh.rule_c_violation("ecosystem/win-tooling/history/2026-01-01.md") is None
    assert vh.rule_c_violation(".claude/skills/a-new-skill/SKILL.md") is None


def test_rule_c_is_silent_where_rule_a_already_speaks():
    # Two rules shouting about one path helps nobody: an unsanctioned TOP-LEVEL dir is
    # Rule A's refusal, and a top-level FILE is Rule A's territory entirely.
    assert vh.rule_c_violation("brandnew/thing.md") is None
    assert vh.rule_a_violation("brandnew/thing.md") is not None
    assert vh.rule_c_violation("STRAY.md") is None


def test_rule_c_admits_every_tracked_path_in_the_live_repo():
    """THE ANTI-DRIFT TEST: the allowlist is DERIVED from the live taxonomy, so every
    path the repo already tracks is admissible. If a pattern is dropped or a convention
    changes, this reds -- rather than the gate quietly refusing legitimate work."""
    repo = Path(__file__).resolve().parent.parent
    out = subprocess.run(["git", "-C", str(repo), "ls-files"],
                         capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0, out.stderr
    paths = [p for p in out.stdout.splitlines() if p.strip()]
    assert len(paths) > 500, "guard against a vacuous pass on an empty ls-files"
    offenders = {p: vh.rule_c_violation(p) for p in paths if vh.rule_c_violation(p)}
    assert not offenders, f"Rule C refuses {len(offenders)} already-tracked path(s): " \
                          f"{sorted(offenders)[:5]}"


def test_rule_c_blocks_end_to_end_through_the_hook(tmp_path):
    """Firing test, not a presence test: the hook exits 1 on a staged out-of-home ADD."""
    repo = _init_repo(tmp_path)
    stray = repo / "docs" / "stray-note.md"
    stray.write_text("# stray\n", encoding="utf-8")
    _git(repo, "add", str(stray))
    res = _run_hook(repo)
    assert res.returncode == 1
    assert "new path outside allowlisted homes" in res.stderr
    assert "operator approval required" in res.stderr


def test_rule_c_lets_the_organ_index_relocation_through_the_hook(tmp_path):
    """The move itself passes the live organ, staged exactly as `git mv` stages it."""
    repo = _init_repo(tmp_path)
    (repo / "ecosystem").mkdir(parents=True, exist_ok=True)
    idx = repo / "ecosystem" / "organ-index.md"
    idx.write_text("# organ index\n", encoding="utf-8")
    _git(repo, "add", str(idx))
    res = _run_hook(repo)
    assert res.returncode == 0, res.stderr
