"""RED-first acceptance tests for the V5 handoff boot changes."""
from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"


@pytest.fixture()
def t():
    if str(_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS))
    return importlib.import_module("transport")


@pytest.fixture()
def world(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "drive"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-browser").mkdir()
    return {"root": root, "cc": root / "to-cc", "browser": root / "to-browser"}


@pytest.fixture()
def registry(t):
    return t.load_registry(_REPO / "ecosystem" / "transport-registry.yaml")


@pytest.fixture()
def live(t, world, tmp_path: Path, monkeypatch):
    seat_file = tmp_path / "seat-ids.yaml"
    t.write_seat_ids(seat_file, seats=[], inventory={})
    monkeypatch.setattr(t, "known_root", lambda: world["root"])
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", seat_file)


def test_a_role_writers_includes_dispatcher_and_keeps_existing_roles(t):
    assert t.ROLE_WRITERS == ("operator", "lane", "integrator", "dispatcher"), (
        "ROLE_WRITERS must include dispatcher and retain operator, lane, and integrator"
    )


def test_b_dispatcher_is_registered_only_for_question_writes(t, world, registry):
    answer = world["browser"] / "ANSWER-dispatcher-refused.md"
    with pytest.raises(t.TransportWriteRefused, match="registered writer"):
        t.write("dispatcher", answer, "answer\n", registry=registry)
    assert not answer.exists(), "a refused dispatcher write must not create the ANSWER file"

    question = next(kind for kind in registry if kind.name == "QUESTION")
    assert question.writers == ("lane", "dispatcher"), (
        "the QUESTION registry writers must be exactly lane and dispatcher"
    )


def test_c_new_dispatcher_question_without_by_is_refused(t, world, live, registry):
    dest = world["browser"] / "QUESTION-dispatcher-unsigned.md"
    with pytest.raises(t.TransportWriteRefused, match="by:"):
        t.write("dispatcher", dest, "plain text, no by line\n", registry=registry)
    assert not dest.exists(), "an unsigned dispatcher QUESTION must not be written"


def test_d_v5a_ruling_is_between_v5_and_v6_without_silent_rule_words():
    text = (_REPO / "protocols" / "STANDING_RULINGS.md").read_text(encoding="utf-8")
    paragraph_re = re.compile(r"(?ms)^\*\*V5a\b.*?(?=\n\s*\n|\Z)")
    v5a = list(paragraph_re.finditer(text))
    assert len(v5a) == 1, "STANDING_RULINGS.md must contain exactly one V5a paragraph"

    v5 = re.search(r"(?ms)^\*\*V5\s.*?(?=\n\s*\n|\Z)", text)
    v6 = re.search(r"(?ms)^\*\*V6\s.*?(?=\n\s*\n|\Z)", text)
    assert v5 is not None and v6 is not None, "the V5 and V6 ruling paragraphs must remain"
    assert v5.start() < v5a[0].start() < v6.start(), "V5a must sit between V5 and V6"

    paragraph = v5a[0].group()
    for phrase in (
        "NEW Claude Code Agent SDK session",
        "Q-H2",
        "to-browser/RATIFICATION-2026-11-01.md section 1",
        "V5's terminal start remains for a lane in the primary checkout",
    ):
        assert phrase in paragraph, f"V5a paragraph is missing {phrase!r}"
    assert re.search(r"\b(?:must|shall|never)\b", paragraph, re.IGNORECASE) is None, (
        "V5a paragraph must not contain must, shall, or never"
    )


def test_e_handoff_boot_has_the_updated_start_and_land_path():
    text = (_REPO / "protocols" / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    assert not any(line.startswith("- **R45**") for line in lines), (
        "HANDOFF_BOOT.md must remove the R45 bullet"
    )
    assert "VISION.md" not in text, "HANDOFF_BOOT.md must not mention VISION.md"
    assert "six acts" in text, "HANDOFF_BOOT.md must describe the operator's six acts"
    assert "scripts/land_lane.py" in text, "HANDOFF_BOOT.md must name scripts/land_lane.py"
    assert "gen_handoff.py --cut" in text and "--land" in text, (
        "HANDOFF_BOOT.md must describe gen_handoff.py --cut and --land"
    )

    interactive = next((line for line in lines if line.startswith("- **interactive**")), "")
    assert "Agent SDK" in interactive, "the interactive start line must name Agent SDK"
    non_lane = next(
        (paragraph for paragraph in re.split(r"\n\s*\n", text)
         if "Each non-lane seat starts by the operator pasting" in paragraph),
        "",
    )
    assert non_lane, "HANDOFF_BOOT.md must retain the non-lane seat start paragraph"
    assert "Agent SDK" in non_lane, "the non-lane seat start paragraph must name Agent SDK"
    assert "scripts/merge_path.py land" in text, "HANDOFF_BOOT.md must retain the merge-path land command"
    assert "/lane-integrate" in text, "HANDOFF_BOOT.md must retain the /lane-integrate command"


def test_f_dispatcher_integrator_and_common_templates_have_the_updated_contract():
    dispatcher = (_REPO / "templates" / "dispatcher-order-template.md").read_text(encoding="utf-8")
    integrator = (_REPO / "templates" / "integrator-order-template.md").read_text(encoding="utf-8")
    common = (_REPO / "templates" / "batch-common-rules-template.md").read_text(encoding="utf-8")

    assert "NEW Claude Code Agent SDK session" in dispatcher, (
        "dispatcher template must specify a NEW Claude Code Agent SDK session"
    )
    assert "## Questions" in dispatcher, "dispatcher template must add a Questions section"
    assert "resume cron" in dispatcher, "dispatcher template must cover resuming its cron"
    assert any("RETIRED (R130, [#1633])" in line for line in dispatcher.splitlines()), (
        "dispatcher template must retain its RETIRED header"
    )
    assert "carried-by: RETIRED" in dispatcher, "dispatcher template must retain carried-by: RETIRED"
    assert re.search(r"\b(?:must|shall|never)\b", dispatcher, re.IGNORECASE) is None, (
        "dispatcher template must not contain must, shall, or never"
    )
    assert "NEW Claude Code Agent SDK session" in integrator, (
        "integrator template must specify a NEW Claude Code Agent SDK session"
    )
    assert "every 30 min" in integrator, "integrator template must specify the 30-minute cycle"
    assert "QUESTION <slug>: <question>" in common, (
        "common-rules template must specify the QUESTION filename shape"
    )
    assert "the one exception" in common, "common-rules template must name the one exception"


_HANDOFFS = "docs/handoffs"
_BUNDLE_DIR_RE = re.compile(r"\d{4}-\d{2}-\d{2}-.+")


def _handoff_landing_violations(repo: Path, base_ref: str = "origin/main") -> list[str]:
    """Paths under docs/handoffs/ that `base_ref...HEAD` changes illegally.

    Illegal: any modify/delete/rename, or any add inside a bundle directory that EXISTS on
    `base_ref`, or an add outside a dated `<YYYY-MM-DD>-...` bundle directory. Legal: only ADDING
    files under a NEW dated bundle directory (a handoff cut's landing). [] = a legal landing.
    Renames are reported as delete + add (`--no-renames`) so neither half can hide the other.
    """
    diff = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", "-z", f"{base_ref}...HEAD",
         "--", _HANDOFFS],
        cwd=repo, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    entries = [(diff[i], diff[i + 1]) for i in range(0, len(diff) - 1, 2)]
    if not entries:
        return []
    listing = subprocess.run(
        ["git", "ls-tree", "--name-only", "-z", base_ref, f"{_HANDOFFS}/"],
        cwd=repo, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    existing = {name.rsplit("/", 1)[-1] for name in listing if name}
    violations: list[str] = []
    for status, path in entries:
        parts = path.split("/")
        bundle = parts[2] if len(parts) > 3 else None
        legal = (status == "A" and bundle is not None
                 and bundle not in existing and _BUNDLE_DIR_RE.fullmatch(bundle) is not None)
        if not legal:
            violations.append(path)
    return violations


def test_g_handoff_files_are_unchanged_from_origin_main():
    """A LANE must not edit an existing handoff bundle. A handoff cut's landing, which only ADDS a
    new dated bundle directory, is legal ([#1886])."""
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=_REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if resolved.returncode:
        pytest.skip("origin/main does not resolve in this checkout")

    violations = _handoff_landing_violations(_REPO)
    assert not violations, (
        f"docs/handoffs differs from origin/main beyond adding a new dated bundle: {violations!r}"
    )


def _landing_git(repo: Path, *args: str):
    p = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t",
         "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert p.returncode == 0, f"git {' '.join(args)} failed: {p.stderr.strip()}"
    return p


def _landing_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _landing_git(repo, "init", "-b", "main")
    existing = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect"
    existing.mkdir(parents=True)
    (existing / "HANDOFF_BOOT.md").write_text("# existing boot\n", encoding="utf-8")
    (existing / "README.md").write_text("# existing readme\n", encoding="utf-8")
    _landing_git(repo, "add", "--all")
    _landing_git(repo, "commit", "-m", "base handoff")
    _landing_git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    _landing_git(repo, "checkout", "-b", "lane")
    return repo


def _landing_commit(repo: Path) -> None:
    _landing_git(repo, "add", "--all")
    _landing_git(repo, "commit", "-m", "lane change")


def test_handoff_landing_allows_files_in_a_new_dated_bundle(tmp_path):
    repo = _landing_repo(tmp_path)
    new_bundle = repo / "docs" / "handoffs" / "2026-11-05-dev-knowledge-architect"
    new_bundle.mkdir(parents=True)
    (new_bundle / "HANDOFF_BOOT.md").write_text("# new boot\n", encoding="utf-8")
    (new_bundle / "README.md").write_text("# new readme\n", encoding="utf-8")
    (new_bundle / "PROBES.md").write_text("# probes\n", encoding="utf-8")
    _landing_commit(repo)

    assert _handoff_landing_violations(repo) == []


def test_handoff_landing_rejects_modifying_an_existing_bundle_file(tmp_path):
    repo = _landing_repo(tmp_path)
    path = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect" / "README.md"
    path.write_text("# modified readme\n", encoding="utf-8")
    _landing_commit(repo)

    violations = _handoff_landing_violations(repo)
    assert "docs/handoffs/2026-10-01-dev-knowledge-architect/README.md" in violations


def test_handoff_landing_rejects_deleting_an_existing_bundle_file(tmp_path):
    repo = _landing_repo(tmp_path)
    path = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect" / "README.md"
    path.unlink()
    _landing_commit(repo)

    violations = _handoff_landing_violations(repo)
    assert "docs/handoffs/2026-10-01-dev-knowledge-architect/README.md" in violations


def test_handoff_landing_rejects_adding_inside_an_existing_bundle(tmp_path):
    repo = _landing_repo(tmp_path)
    path = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect" / "EXTRA.md"
    path.write_text("# extra\n", encoding="utf-8")
    _landing_commit(repo)

    violations = _handoff_landing_violations(repo)
    assert "docs/handoffs/2026-10-01-dev-knowledge-architect/EXTRA.md" in violations


def test_handoff_landing_ignores_new_bundle_when_existing_bundle_is_modified(tmp_path):
    repo = _landing_repo(tmp_path)
    new_bundle = repo / "docs" / "handoffs" / "2026-11-05-dev-knowledge-architect"
    new_bundle.mkdir(parents=True)
    (new_bundle / "HANDOFF_BOOT.md").write_text("# new boot\n", encoding="utf-8")
    changed = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect" / "README.md"
    changed.write_text("# modified readme\n", encoding="utf-8")
    _landing_commit(repo)

    violations = _handoff_landing_violations(repo)
    assert violations == ["docs/handoffs/2026-10-01-dev-knowledge-architect/README.md"]


def test_handoff_landing_allows_changes_outside_handoffs(tmp_path):
    repo = _landing_repo(tmp_path)
    (repo / "notes.md").write_text("unrelated change\n", encoding="utf-8")
    _landing_commit(repo)

    assert _handoff_landing_violations(repo) == []


def test_handoff_landing_rejects_renaming_inside_an_existing_bundle(tmp_path):
    repo = _landing_repo(tmp_path)
    existing = repo / "docs" / "handoffs" / "2026-10-01-dev-knowledge-architect"
    (existing / "README.md").rename(existing / "NOTES.md")
    _landing_commit(repo)

    violations = _handoff_landing_violations(repo)
    assert set(violations) & {
        "docs/handoffs/2026-10-01-dev-knowledge-architect/README.md",
        "docs/handoffs/2026-10-01-dev-knowledge-architect/NOTES.md",
    }
