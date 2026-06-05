"""Unit tests for scripts/validate_backlog.py (ADR-66 story-map hierarchy validator)."""

import importlib.util
from pathlib import Path

_VB = Path(__file__).resolve().parent.parent / "scripts" / "validate_backlog.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_backlog", _VB)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vb = _load()

VALID = """# .dev-knowledge BACKLOG
## Big picture
A short paragraph.
**Themes (backbone):** Theme A
## Theme A
> As a persona, I want a goal.
### Story one
So that reasons hold.
- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1
### Story two
So that more reasons.
- [#2] [P3][S] do another thing · Done when: criterion met
"""


def _run(text):
    return vb.validate(*vb.parse(text))


def test_valid_passes():
    hard, _ = _run(VALID)
    assert hard == []


def test_missing_big_picture_fails():
    hard, _ = _run(VALID.replace("## Big picture", "## Overview"))
    assert any("Big picture" in h for h in hard)


def test_duplicate_big_picture_fails():
    hard, _ = _run(VALID.replace("## Theme A", "## Big picture", 1))
    assert any("Big picture" in h for h in hard)


def test_story_missing_so_that_fails():
    hard, _ = _run(VALID.replace("So that reasons hold.\n", ""))
    assert any("So that" in h for h in hard)


def test_task_missing_done_when_fails():
    hard, _ = _run(VALID.replace(" · Done when: it is done · refs ADR-1", ""))
    assert any("Done when" in h for h in hard)


def test_task_missing_band_fails():
    hard, _ = _run(VALID.replace("[#1] [P1][M] ", "[#1] "))
    assert any("band" in h for h in hard)


def test_duplicate_id_fails():
    hard, _ = _run(VALID.replace("[#2]", "[#1]"))
    assert any("duplicate id" in h for h in hard)


def test_orphan_task_fails():
    orphan = """# B
## Big picture
x
## Theme A
> As a p, I want g.
- [#9] [P1][M] orphan task · Done when: x
"""
    hard, _ = _run(orphan)
    assert any("not under a user story" in h for h in hard)


def test_structured_done_marker_fails():
    hard, _ = _run(VALID.replace(" · refs ADR-1", " · status:done"))
    assert any("done task" in h for h in hard)


def test_legit_bracket_x_in_prose_passes():
    # a literal [x] inside task prose is NOT a done marker
    hard, _ = _run(VALID.replace("do a thing", "document the [x] checkbox syntax"))
    assert hard == []


def test_empty_story_warns_not_fails():
    text = VALID + "### Empty story\nSo that nothing.\n"
    hard, warn = _run(text)
    assert hard == []
    assert any("no tasks" in w for w in warn)


# --- #83: in-place RESOLVED / struck-through task lines (ADR-65 done-items-leave) ---
# Fixture shape from commit 052e311 (the #79 stub finding F2 exposed): a task struck
# through in place + a bold **RESOLVED** marker, instead of the item LEAVING the file.

def test_struck_through_task_fails():
    hard, _ = _run(VALID.replace(
        "- [#1] [P1][M] do a thing · Done when: it is done · refs ADR-1",
        "- [#1] ~~[P1][M] do a thing · Done when: it is done · refs ADR-1~~ "
        "**RESOLVED 2026-06-03 — no build needed.**",
    ))
    assert any("ADR-65" in h and "resolved" in h.lower() for h in hard)


def test_inplace_resolved_marker_fails():
    hard, _ = _run(VALID.replace(
        " · refs ADR-1",
        " · refs ADR-1 **RESOLVED 2026-06-05 — landed.**",
    ))
    assert any("ADR-65" in h and "resolved" in h.lower() for h in hard)


def test_clean_task_with_done_when_passes_inplace_check():
    # the unmodified VALID has no strike/RESOLVED marker -> no in-place finding
    # ("Done when:" is title-case and must NOT trip the all-caps DONE marker)
    hard, _ = _run(VALID)
    assert not any("in-place" in h for h in hard)


def test_live_backlog_passes_inplace_check():
    text = (Path(vb.__file__).resolve().parent.parent / "BACKLOG.md").read_text(encoding="utf-8")
    hard, _ = _run(text)
    assert not any("in-place" in h for h in hard)
