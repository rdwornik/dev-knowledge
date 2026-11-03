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


def test_g_handoff_files_are_unchanged_from_origin_main():
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=_REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if resolved.returncode:
        pytest.skip("origin/main does not resolve in this checkout")

    diff = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD", "--", "docs/handoffs"],
        cwd=_REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    assert not diff.stdout.strip(), (
        f"docs/handoffs differs from origin/main: {diff.stdout.strip()!r}"
    )
