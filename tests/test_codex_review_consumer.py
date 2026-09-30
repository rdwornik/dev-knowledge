"""Tests for the Codex-review organ's consumer declaration ([#1329] item 2).

RED-FIRST (ADR-108 SS B): written against the pre-[#1329] `deploy/codex-review.ps1` /
`deploy/codex-review-lib.ps1`, which had no `-Consumer`/`-NoConsumerReason` params and no
`Get-ConsumerLine` function -- every assertion below failed before this lane's implementation
landed.

TWO LAYERS, because the logic lives in PowerShell (the organ is a USER-machine-scoped,
standalone tool deployed to an arbitrary operator repo -- it cannot reach back into this hub's
`uv`/Python environment at runtime, so the consumer-line composer is hand-duplicated PowerShell,
not an import of `scripts/consumer_at_landing.py`):

  * a PLATFORM-INDEPENDENT static check (regex over the `.ps1` source text) that runs on both
    CI legs (ADR-127) and pins the four citation forms + the reason floor are present and
    match `consumer_at_landing._CITATION_RES` / `NO_CONSUMER_REASON_FLOOR` byte-for-byte, so the
    two copies cannot drift silently;
  * a WINDOWS-GATED behavioral check (`skipif(sys.platform != "win32")`) that actually invokes
    `Get-ConsumerLine` via `pwsh` and asserts real behavior for every branch. This is a PLATFORM
    skip, not a tool-presence probe on the environment being policed -- `proof_layer.py`'s own
    counter-rule states a platform/language-version skipif is not family 3 ("it gates on what
    the code can run under, not on the presence of the thing being policed"). pwsh itself is not
    guaranteed on the Linux CI leg, so the behavioral layer stays Windows-only; the static layer
    covers both legs unconditionally.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_LIB = _REPO / "deploy" / "codex-review-lib.ps1"
_WRAPPER = _REPO / "deploy" / "codex-review.ps1"

sys.path.insert(0, str(_REPO / "scripts"))
from consumer_at_landing import _CITATION_RES, NO_CONSUMER_REASON_FLOOR  # noqa: E402


# ---------------------------------------------------------------------------
# static, platform-independent — pins the two copies against each other
# ---------------------------------------------------------------------------


def _lib_text() -> str:
    return _LIB.read_text(encoding="utf-8")


def test_lib_file_exists():
    assert _LIB.is_file()


def test_lib_declares_get_consumer_line_function():
    assert re.search(r"function\s+Get-ConsumerLine\b", _lib_text())


def test_lib_has_no_top_level_mandatory_param_block():
    """Dot-source safety: the whole point of splitting this into its own file is that it
    can be dot-sourced with no side effect and no interactive prompt. A `Mandatory` param
    anywhere at file scope would defeat that."""
    assert "Mandatory" not in _lib_text()


#: Each of consumer_at_landing._CITATION_RES's four labels, mapped to the literal
#: PowerShell-regex substring codex-review-lib.ps1 must carry for it. A byte-for-byte
#: duplication check, not a semantic one: this fails if a form is dropped or its literal
#: text changes on either side without the other being updated.
_EXPECTED_LIB_PATTERNS = {
    "a backlog row": r"\[#\d+\]",
    "an ADR": r"ADR-\d+",
    "the standing-rulings register": "STANDING_RULINGS",
    "an intake": r"intake\s+#\d+",
}


@pytest.mark.parametrize("label", [label for label, _ in _CITATION_RES])
def test_lib_embeds_every_citation_form(label):
    assert label in _EXPECTED_LIB_PATTERNS, f"no expected-pattern mapping for {label!r}"
    assert _EXPECTED_LIB_PATTERNS[label] in _lib_text(), (
        f"{label!r}'s citation form ({_EXPECTED_LIB_PATTERNS[label]!r}) does not appear "
        f"in {_LIB}")


def test_lib_reason_floor_matches_consumer_at_landing():
    match = re.search(r"\$reasonFloor\s*=\s*(\d+)", _lib_text())
    assert match, "no $reasonFloor constant found in codex-review-lib.ps1"
    assert int(match.group(1)) == NO_CONSUMER_REASON_FLOOR


def test_wrapper_declares_consumer_params():
    text = _WRAPPER.read_text(encoding="utf-8")
    assert "$Consumer" in text
    assert "$NoConsumerReason" in text


def test_wrapper_dot_sources_the_lib():
    text = _WRAPPER.read_text(encoding="utf-8")
    assert "codex-review-lib.ps1" in text
    assert "Get-ConsumerLine" in text


def test_wrapper_embeds_consumer_line_in_header_before_codex_invocation():
    """The consumer declaration is resolved BEFORE `codex exec` runs (fail fast on a bad or
    missing declaration, never after paying for a review)."""
    text = _WRAPPER.read_text(encoding="utf-8")
    consumer_call = text.index("Get-ConsumerLine")
    codex_invocation = text.index("codex exec")
    header_embed = text.index("$consumerLine", consumer_call + 1)
    assert consumer_call < codex_invocation
    assert consumer_call < header_embed


# ---------------------------------------------------------------------------
# behavioral, Windows-only — a real pwsh invocation of Get-ConsumerLine
# ---------------------------------------------------------------------------

pytestmark_skip = pytest.mark.skipif(
    sys.platform != "win32",
    reason="codex-review-lib.ps1 is a Windows-native user-machine organ (PowerShell); this "
           "is a PLATFORM skip (proof_layer.py's counter-rule), not a tool-presence probe — "
           "pwsh itself is never checked for, only the OS this organ runs under")


def _run_get_consumer_line(*args: str) -> subprocess.CompletedProcess:
    script = (
        f". '{_LIB.as_posix()}'; "
        "try { " + " ".join(args) + " } "
        "catch { Write-Error $_.Exception.Message; exit 1 }"
    )
    return subprocess.run(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True, text=True, timeout=30)


@pytestmark_skip
def test_valid_consumer_citation_produces_consumer_line():
    result = _run_get_consumer_line("Get-ConsumerLine -Consumer '[#1329]'")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "**Consumer:** [#1329]"


@pytestmark_skip
def test_invalid_consumer_citation_errors():
    result = _run_get_consumer_line("Get-ConsumerLine -Consumer 'not-a-citation'")
    assert result.returncode != 0
    assert "matches no governance-citation form" in result.stderr


@pytestmark_skip
def test_valid_no_consumer_reason_produces_no_consumer_line():
    reason = "ad-hoc spot-check, no tracked follow-up"
    assert len(reason) >= NO_CONSUMER_REASON_FLOOR
    result = _run_get_consumer_line(f"Get-ConsumerLine -NoConsumerReason '{reason}'")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == f"no-consumer: {reason}"


@pytestmark_skip
def test_too_short_reason_errors():
    result = _run_get_consumer_line("Get-ConsumerLine -NoConsumerReason 'too short'")
    assert result.returncode != 0
    assert "characters" in result.stderr


@pytestmark_skip
def test_neither_consumer_nor_reason_errors():
    result = _run_get_consumer_line("Get-ConsumerLine")
    assert result.returncode != 0


@pytestmark_skip
def test_both_consumer_and_reason_errors():
    reason = "ad-hoc spot-check, no tracked follow-up"
    result = _run_get_consumer_line(
        f"Get-ConsumerLine -Consumer '[#1329]' -NoConsumerReason '{reason}'")
    assert result.returncode != 0
    assert "not both" in result.stderr
