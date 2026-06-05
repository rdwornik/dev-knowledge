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


# --- Survivor-issue body extractor (FIX 1: heading-mismatch alignment) --------
# The real generator emits LEVEL-2 headings "## Findings (PROPOSALS ONLY)" /
# "## Next Actions (proposals for operator)" with ### High/Med/Low subsections
# inside Findings. This mirrors the yml awk: capture from the level-2 heading to
# the next level-2 "## " heading or "---" rule.

def _extract_section(body: str, heading_prefix: str) -> str:
    out, cap = [], False
    for line in body.splitlines():
        if not cap:
            if line.startswith("## " + heading_prefix):
                cap = True
                out.append(line)
            continue
        if line.startswith("## ") or re.match(r"^---\s*$", line):
            break
        out.append(line)
    return "\n".join(out)


def test_findings_extractor_captures_real_level2_section():
    body = FIXTURE.read_text(encoding="utf-8")
    findings = _extract_section(body, "Findings")
    assert "SYNTHETIC-F1" in findings, "must capture the survivor finding"
    assert "### Med" in findings, "### subsections must be included (not stop at '### High')"
    assert "Killed Findings" not in findings, "must stop before '## Killed Findings'"
    assert "Next Actions" not in findings


def test_next_actions_extractor_captures_section():
    body = FIXTURE.read_text(encoding="utf-8")
    nextact = _extract_section(body, "Next Actions")
    assert "SYNTHETIC" in nextact, "must capture the next-actions content"
    assert "Safety Tripwire" not in nextact, "must stop at the next '## ' / '---'"


def test_extractor_is_failsoft_when_heading_absent():
    """A digest missing the section -> empty capture -> the yml applies a
    placeholder (never an empty/dead issue body)."""
    body = "## Summary\n\nno findings heading here\n\n## Other\n"
    assert _extract_section(body, "Findings") == ""
    text = YML.read_text(encoding="utf-8")
    assert '[ -n "$FINDINGS" ] ||' in text, "yml must placeholder a missing Findings section"
    assert '[ -n "$NEXTACT" ] ||' in text, "yml must placeholder a missing Next Actions section"


def test_yml_extractor_targets_real_level2_headings():
    """Anti-drift: the yml awk must target the real level-2 headings, and the old
    strict '### Findings by Severity' heading must be retired."""
    text = YML.read_text(encoding="utf-8")
    assert "/^## Findings/" in text
    assert "/^## Next Actions/" in text
    assert "^### Findings by Severity" not in text
