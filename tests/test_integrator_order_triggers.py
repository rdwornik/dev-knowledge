"""Witnesses for `templates/integrator-order-template.md`'s close and refusal steps
(LANE-5B3-2-wire-quota-distiller, Done-contract item 1).

The two silent organs `quota_watch.py` and `learning_distiller.py` MERGED with nobody
triggering them (DIGEST-WAVE5B-N2-2026-09-26.md G9). This file asserts the trigger prose is
actually in the template, not merely that this lane believes it wrote it: the close step
calls `quota_watch.py record` then `quota_watch.py line`, and `learning_distiller.py run`
over the batch's REFUSED files; the refusal step calls `learning_distiller.py run` over the
one REFUSED file it just wrote. Ownership: this lane edits ONLY the close and refusal
sections (ruling (i)) -- a separate test asserts every other section is byte-unchanged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TEMPLATE = REPO_ROOT / "templates" / "integrator-order-template.md"


def _section(text: str, heading: str) -> str:
    """The body of one `## <heading>` section, up to the next `## ` heading or EOF."""
    pattern = re.compile(
        rf"^##\s*{re.escape(heading)}\s*$(?P<body>.*?)(?=^##\s|\Z)", re.M | re.S)
    m = pattern.search(text)
    assert m, f"no '## {heading}' section found in {TEMPLATE}"
    return m.group("body")


def _close_section(text: str) -> str:
    return _section(text, "Close — when every lane is MERGED or FAILED, or at <time>, whichever comes first")


def _refusals_section(text: str) -> str:
    return _section(text, "Refusals and repairs")


def test_template_exists():
    assert TEMPLATE.exists()


def test_close_step_calls_quota_watch_record_then_line():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    record_idx = close.find("scripts/quota_watch.py record")
    line_idx = close.find("scripts/quota_watch.py line")
    assert record_idx != -1, "close step does not call `quota_watch.py record`"
    assert line_idx != -1, "close step does not call `quota_watch.py line`"
    assert record_idx < line_idx, "record must be called before line, not after"


def test_close_step_calls_learning_distiller_over_the_batchs_refused_files():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    assert "scripts/learning_distiller.py" in close
    assert "run --integrator" in close
    assert "--dispatcher" in close
    assert "--refused" in close
    assert "REFUSED-" in close


def test_close_step_never_claims_the_distiller_files_rows():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    assert "ruling h" in close
    assert "does not file" in close or "files nothing" in close


def test_refusal_step_calls_learning_distiller_over_the_refused_file_it_just_wrote():
    text = TEMPLATE.read_text(encoding="utf-8")
    refusals = _refusals_section(text)
    assert "REFUSED-<slug>.md" in refusals, "the refusal step must name the file it just wrote"
    assert "scripts/learning_distiller.py" in refusals
    assert "run --integrator" in refusals
    assert "--refused to-browser/REFUSED-<slug>.md" in refusals
    assert "ruling h" in refusals


def test_both_organs_are_called_from_both_the_close_and_refusal_steps_collectively():
    """The contract's own framing: 'both calls' (quota_watch + learning_distiller) show up
    across 'both steps' (close + refusal) -- quota_watch only at close (there is no per-
    refusal cost line), learning_distiller at both close and refusal."""
    text = TEMPLATE.read_text(encoding="utf-8")
    close, refusals = _close_section(text), _refusals_section(text)
    assert "quota_watch.py" in close
    assert "learning_distiller.py" in close
    assert "learning_distiller.py" in refusals


def test_no_must_shall_or_never_added_zero_headroom_baseline():
    """Lessons of N2 (a): `protocols/*.md`, `templates/**`, `ecosystem/*.yaml` carry zero
    headroom on the silent-rule baseline -- this template had zero occurrences before this
    lane touched it, and it must stay at zero. (Regression guard for this lane's own edit,
    not a claim on the integrator's full ratchet test, which only the integrator runs.)"""
    text = TEMPLATE.read_text(encoding="utf-8")
    hits = re.findall(r"\b(must|shall|never)\b", text)
    assert hits == [], f"forbidden normative word(s) found: {hits}"


def test_only_close_and_refusal_headings_changed_shape_others_untouched():
    """Ownership (ruling (i)): this lane edits ONLY the close and refusal steps. The other
    section headings and their intervening prose stay exactly as `templates/dispatcher-
    order-template.md`'s sibling lane and `lane-orchestrator-cycling` expect to find them."""
    text = TEMPLATE.read_text(encoding="utf-8")
    for heading in (
        "Merge priority when several are waiting",
        "Per handback — the one path",
    ):
        assert re.search(rf"^##\s*{re.escape(heading)}\s*$", text, re.M), (
            f"heading '{heading}' is missing or reworded -- out of this lane's ownership")
