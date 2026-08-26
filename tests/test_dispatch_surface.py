"""Tests for scripts/dispatch_surface.py + audit.py::check_dispatch_verb_agreement (R5).

THE DEFECT, as `protocols/STANDING_RULINGS.md` §V measured it: the hub carried FOUR rival
literal launch commands for one act, `/lane-boot` emitted the form Ch8 itself labels a fallback
while silently dropping `--model` and `--effort`, and roughly thirty consecutive browser seats
failed to launch a lane — "not uninformed; informed by four sources that disagreed." §V's own
closing line calls the organ that would catch this "owed and unbuilt". This is the tree-side
half of it.

Every test that asserts a violation seeds a RIVAL into a temp copy of the two real files, so the
RED is produced by the condition the gate exists to refuse rather than by a stub.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import audit as aud  # noqa: E402
import dispatch_surface as ds  # noqa: E402

_REPO = Path(__file__).resolve().parents[1]


def _mirror(tmp_path: Path) -> Path:
    """A temp repo carrying the three REAL files this gate reads, so a seeded rival is a
    mutation of live content rather than a fixture that merely resembles it."""
    root = tmp_path / "repo"
    for rel in (ds.PLAYBOOK_PATH, *ds.AGREEMENT_SITES):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_REPO / rel, dst)
    return root


def _seed_rival(root: Path, rel: str, line: str) -> None:
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8") + f"\n```\n{line}\n```\n", encoding="utf-8")


# --- reading the SOLE literal-command site ----------------------------------

def test_ruled_form_is_read_from_ch8_not_hardcoded():
    lines = ds.ruled_form(_REPO)
    assert lines, "Ch8's LOCAL-lane form must be readable"
    assert lines[0].startswith("dispatch ")


def test_ruled_verb_is_the_lead_token():
    assert ds.ruled_verb(_REPO) == "dispatch"


def test_ruled_form_returns_none_rather_than_a_remembered_command(tmp_path):
    """A second copy of the line is the defect §V ruled on, so the degrade path is a POINTER,
    never a fallback string. None is the signal that produces one."""
    assert ds.ruled_form(tmp_path) is None                       # no PLAYBOOK at all
    root = tmp_path / "reworded"
    (root / "protocols").mkdir(parents=True)
    (root / ds.PLAYBOOK_PATH).write_text("# P\n\n## Something else\n", encoding="utf-8")
    assert ds.ruled_form(root) is None                           # heading moved/reworded


# --- the fence split, which the whole rival test rests on -------------------

def test_fenced_lines_ignores_prose_backticks():
    text = "a line mentioning `claude --bg` in prose\n\n```\ndispatch FILE.md\n```\n"
    assert ds.fenced_lines(text) == ["dispatch FILE.md"]


# --- agreement, live -------------------------------------------------------

def test_live_surfaces_agree_with_the_ruled_verb():
    """The tree as it stands: both point-of-use sites name `dispatch` in a fence and carry no
    rival form in one. A regression here is the exact §V recurrence."""
    assert ds.agreement_findings(_REPO) == []


def test_check_is_green_on_the_live_repo():
    findings = aud.check_dispatch_verb_agreement(_REPO)
    assert [f.status for f in findings] == ["pass"]


def test_check_is_registered_in_all_checks():
    assert aud.check_dispatch_verb_agreement in aud.ALL_CHECKS


# --- RED against a seeded rival --------------------------------------------

def test_seeded_raw_claude_bg_form_in_lane_boot_is_refused(tmp_path):
    """§V V4: the raw form "does not appear in a command file or a template". This is the exact
    line `/lane-boot` emitted until 2026-08-25 — the one that dropped --model and --effort."""
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md",
                "claude --worktree lane-x --bg --permission-mode bypassPermissions")
    hits = ds.agreement_findings(root)
    assert any("lane-boot.md" in h and "rival" in h for h in hits), hits


def test_seeded_rival_in_the_template_is_refused(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, "templates/prompt-template.md", "claude --bg --model opus --effort high")
    hits = ds.agreement_findings(root)
    assert any("prompt-template.md" in h and "rival" in h for h in hits), hits


def test_seeded_superseded_alias_is_refused(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "Dispatch-CloudBrief BRIEF.md")
    assert any("Dispatch-CloudBrief" in h for h in ds.agreement_findings(root))


def test_seeded_version_named_alias_is_refused(tmp_path):
    """§V V3: substrate-named verbs are canonical, version-named ones are deprecated aliases."""
    root = _mirror(tmp_path)
    _seed_rival(root, "templates/prompt-template.md", "Dispatch-Lane lane-x FILE.md")
    assert any("Dispatch-Lane" in h for h in ds.agreement_findings(root))


def test_prose_mention_of_the_raw_form_is_NOT_refused(tmp_path):
    """The negative control that matters. Both files RECORD the correction in prose — "this line
    used to emit a raw `claude --worktree … --bg …` form" — and a gate that refused the mention
    would force them to delete the history explaining why they changed."""
    root = _mirror(tmp_path)
    p = root / ".claude/commands/lane-boot.md"
    p.write_text(p.read_text(encoding="utf-8")
                 + "\nUntil 2026-08-25 this emitted a raw `claude --worktree x --bg` form.\n",
                 encoding="utf-8")
    assert ds.agreement_findings(root) == []


def test_dispatch_local_fallback_is_not_a_rival(tmp_path):
    """§V V2 makes `Dispatch-Local` the documented manual fallback, so it stays legal."""
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "Dispatch-Local lane-x FILE.md -Effort high")
    assert ds.agreement_findings(root) == []


def test_site_that_stops_naming_the_ruled_verb_is_refused(tmp_path):
    """The other §V class: a pointer that stopped pointing."""
    root = _mirror(tmp_path)
    p = root / "templates/prompt-template.md"
    p.write_text(p.read_text(encoding="utf-8").replace("dispatch <THIS-CONTRACT-FILENAME>.md",
                                                       "somethingelse <FILE>.md"),
                 encoding="utf-8")
    assert any("no fenced line names the ruled verb" in h for h in ds.agreement_findings(root))


def test_unreadable_ch8_is_reported_not_waved_through(tmp_path):
    """A gate whose anchor moved says so. It never passes because it could not look."""
    hits = ds.agreement_findings(tmp_path)
    assert len(hits) == 1 and "unreadable" in hits[0]


def test_check_is_fail_class_on_a_seeded_rival(tmp_path):
    root = _mirror(tmp_path)
    _seed_rival(root, ".claude/commands/lane-boot.md", "claude --bg --model opus")
    findings = aud.check_dispatch_verb_agreement(root)
    assert [f.status for f in findings] == ["fail"]
    assert "|" not in findings[0].evidence
