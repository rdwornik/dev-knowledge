"""Regression test for the nightly-conformance-triage counts contract.

Kills the fixture/production drift class (LESSONS 2026-06-05): the synthetic
fixture is validated against the ACTUAL marker regex extracted live from the
Action yml, not a hand-copied one. If the yml's marker format changes, this
test re-reads it from the yml; if the fixture stops matching the live contract,
the test fails -- so fixture and parser cannot silently diverge again.

Pure-Python (no bash dependency) so it runs in the local pytest gate on
Windows. The real-shell proof (the exact yml bash run under `set -euo pipefail`
for the valid + corrupted-marker paths) is recorded in the JOURNAL / handoff
for the fix/nightly-counts-contract branch.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
YML = REPO / ".github/workflows/nightly-conformance-triage.yml"
FIXTURE = REPO / "tests/fixtures/nightly-triage/2099-01-02-conformance-nightly-digest.md"

MARKER_RE = r"<!-- counts: raw=(\d+) survived=(\d+) killed=(\d+) -->"


def _marker_ere_from_yml() -> str:
    """Extract the exact ERE the Action greps for, so this test cannot drift from it."""
    text = YML.read_text(encoding="utf-8")
    m = re.search(r"grep -oE '(<!-- counts:[^']+)'", text)
    assert m, "could not find the counts-marker grep -oE in the Action yml"
    return m.group(1)


def test_fixture_matches_live_yml_marker_regex():
    """The committed fixture must be parseable by the regex the Action actually uses."""
    ere = _marker_ere_from_yml()
    body = FIXTURE.read_text(encoding="utf-8")
    assert re.search(ere, body), f"fixture has no marker matching the live Action regex: {ere!r}"


def test_fixture_survived_count_parses_and_is_survivor():
    body = FIXTURE.read_text(encoding="utf-8")
    m = re.search(MARKER_RE, body)
    assert m, "fixture missing counts marker"
    raw, survived, killed = (int(g) for g in m.groups())
    assert (raw, survived, killed) == (1, 1, 0)
    assert survived > 0, "survivor fixture must drive the triage-issue path"


def test_fixture_has_no_handmade_counts_table():
    """The real generator never emits a '### Counts' table; the fixture must not either.

    Line-anchored so the fixture's own descriptive prose (which names the
    `### Counts` table it deliberately omits) does not false-positive.
    """
    body = FIXTURE.read_text(encoding="utf-8")
    assert not re.search(r"(?m)^### Counts\b", body), "fixture must not carry a '### Counts' heading"
    assert not re.search(r"(?m)^\s*\|\s*Survived skeptic\s*\|", body), "fixture must not carry a Counts table row"


def test_absent_marker_is_fail_closed_signal():
    """A digest with no marker yields no match -> the Action's fail-closed path fires."""
    no_marker = "# digest\n\nSurvived skeptic: one, but no machine-readable marker.\n"
    assert re.search(MARKER_RE, no_marker) is None


def test_yml_marker_extraction_has_failopen_guard():
    """The marker grep must carry `|| true` so a no-match cannot abort the step
    under `set -euo pipefail` (that bug made the fail-closed path unreachable)."""
    text = YML.read_text(encoding="utf-8")
    line = next((ln for ln in text.splitlines() if "grep -oE '<!-- counts:" in ln), "")
    assert "|| true" in line, "marker grep must end with `|| true` for fail-closed reachability"
