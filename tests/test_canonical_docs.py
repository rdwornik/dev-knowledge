"""Tests for the canonical-doc-name registry — `scripts/canonical_docs.py`.

CLOUD-4 v2's answer to `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md`
§1.5 GO-(b): ONE table the ten machine constants read, instead of ten independent literals.

**These tests still do not assert a RENAME — because none happened.** `cdocs.VISION` is
still the string `"VISION.md"` and the file is still tracked at the root, byte-identical.
What `[#614]` lane-a changed is the doc's **TIER**, not its name: `VISION.md` left
`CANONICAL_MANDATORY` for `CANONICAL_RETIRED`, and `README.md` became MUST at the hub via
`CANONICAL_HUB_MANDATORY`. R2 §1.5 verdicted the *rename* NO-GO as briefed and that verdict
is untouched; the sequenced fleet-wide filename migration (ADR-114 option (C)) is still
future work. What these tests assert, as before, is that the ten sites name the SAME
strings — which is exactly what made a tier decision landable in one file.

Three groups:

* **Repoint** — each of the eight hub-local constants IS the registry's value.
* **Carried-copy fallback** — `canonical_freshness_gate` and `session_end_backpressure` are
  byte-copied into consumers by `deploy/carrier_mesh.py` as standalone single files, so they
  import the registry SOFTLY and keep a literal fallback. The fallback is parsed out of the
  source text and compared to the registry, so hub-side drift between the two reds here
  rather than going silent at a consumer.
* **Cross-language** — `.claude/workflows/conformance-hub.js` (R2 seam S11) is a JavaScript
  string list that cannot import Python at all; it is held in agreement by reading the file.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

import canonical_docs as cdocs  # noqa: E402
import canonical_freshness_gate as cfg  # noqa: E402
import gen_handoff as gh  # noqa: E402
import session_end_backpressure as seb  # noqa: E402
import validate_doc_rot as vdr  # noqa: E402
import validate_doc_structure as vds  # noqa: E402
import validate_hermetization as vh  # noqa: E402
from audit_checks.check_canonical_md_visibility import _CANONICAL_ALL, _CANONICAL_MANDATORY
from audit_checks.check_canonical_structure import _CANONICAL_SPINE

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFORMANCE_HUB = ".claude/workflows/conformance-hub.js"


# --- the value is unchanged ----------------------------------------------------------------

def test_the_registry_still_says_vision_md():
    """A tier moved; the NAME did not. If this line ever changes it is a ruled decision
    (ADR-114 option (C)'s nine-repo filename migration), not a lane.

    Pinned deliberately alongside the retirement: retiring `VISION.md` from the mandatory
    set and RENAMING it are different acts, and this line is what keeps the second from
    riding in on the first.
    """
    assert cdocs.VISION == "VISION.md"


def test_the_mandatory_set_is_the_adr38_a6_seven_minus_the_retired_vision():
    """ADR-38 A6's seven, minus `VISION.md` — retired by ADR-114 (Accepted 2026-08-29,
    AMENDMENT 1), executed here by `[#614]` lane-a.

    The pin is written as an explicit six rather than a derivation so that a name
    re-entering the mandatory set is a visible edit to THIS line. Retirement is a
    subtraction, and the direction is the safety argument: dropping a presence
    requirement cannot RED a member that still carries the file, whereas ADDING one
    (promoting `README.md` here) would RED the six ADR-104 children that have none.
    """
    assert cdocs.CANONICAL_MANDATORY == (
        "ARCHITECTURE.md", "CLAUDE.md", "BACKLOG.md",
        "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md",
    )
    assert cdocs.VISION not in cdocs.CANONICAL_MANDATORY
    assert cdocs.CANONICAL_RETIRED == ("VISION.md",)


def test_readme_is_hub_mandatory_and_deliberately_not_fleet_mandatory():
    """The seam that lets ADR-114 option (C) be SEQUENCED instead of taken in one commit.

    `README.md` is MUST at the hub and unchanged for the fleet. If these two assertions
    ever have to move together, the fleet-wide migration has happened and it is a ruled
    act, not a lane's drive-by.
    """
    assert cdocs.README in cdocs.CANONICAL_HUB_MANDATORY
    assert cdocs.README not in cdocs.CANONICAL_MANDATORY
    assert cdocs.README not in cdocs.ADR38_BASELINE_REQUIRED
    # Nothing fleet-wide may read the hub tuple — that is what makes it hub-scoped.
    assert cdocs.CANONICAL_HUB_MANDATORY == cdocs.CANONICAL_MANDATORY + (cdocs.README,)


def test_retired_and_hub_scoped_names_keep_their_casing_check():
    """A retired name is not a deleted one, and a hub-scoped one is not a fleet one —
    but BOTH stay name-checked. `CANONICAL_ALL` is the casing surface
    (`check_canonical_md_visibility`), and dropping either from it would silently stop
    catching a `Vision.md` / `Readme.md` mis-casing anywhere in the fleet."""
    assert cdocs.VISION in cdocs.CANONICAL_ALL
    assert cdocs.README in cdocs.CANONICAL_ALL
    assert len(cdocs.CANONICAL_ALL) == len(set(cdocs.CANONICAL_ALL)), "no duplicate names"


# --- the eight hard repoints ---------------------------------------------------------------

def test_check_canonical_md_visibility_reads_the_registry():
    assert _CANONICAL_MANDATORY == list(cdocs.CANONICAL_MANDATORY)
    assert _CANONICAL_ALL == list(cdocs.CANONICAL_ALL)
    # The re-export contract is a name, a value AND a type: tests/test_audit.py reads
    # `aud._CANONICAL_MANDATORY` and a tuple would be a silent behaviour change.
    assert isinstance(_CANONICAL_MANDATORY, list)


def test_check_adr38_baseline_reads_the_registry():
    from audit_checks import check_adr38_baseline as mod
    src = Path(mod.__file__).read_text(encoding="utf-8")
    assert "canonical_docs.ADR38_BASELINE_REQUIRED" in src
    assert cdocs.ADR38_BASELINE_REQUIRED == (
        "ARCHITECTURE.md", "BACKLOG.md",
        "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md",
    )
    assert cdocs.CLAUDE not in cdocs.ADR38_BASELINE_REQUIRED, "check_claude_md owns CLAUDE.md"
    # This check runs FLEET-WIDE (its own docstring says so), which is the whole reason the
    # retirement is a subtraction here: `terminal-setup` is a declared ADR-104 member that
    # has never carried a VISION.md, so this line turns a latent divergence GREEN.
    assert cdocs.VISION not in cdocs.ADR38_BASELINE_REQUIRED


def test_check_canonical_structure_keys_come_from_the_registry():
    assert set(_CANONICAL_SPINE) == set(cdocs.CANONICAL_SPINE)
    assert _CANONICAL_SPINE[cdocs.VISION] == [
        "## Vision", "## Scope", "## Values", "## Lifecycle", "## References"]
    # README is deliberately NOT keyed here, and this pins the absence so it stays a
    # decision instead of decaying into an oversight. `release_lint` C7 mirrors this dict
    # into every RELEASED manifest's `doc_shapes` and lints the live constants against
    # v1.1.0 and v1.2.0, so adding the key REDs shipped specs; the sanctioned answer is a
    # manifest version bump, which rides ADR-114 option (C), not this lane.
    assert cdocs.README not in _CANONICAL_SPINE


def test_check_vision_md_uses_the_registry_name():
    from audit_checks.check_vision_md import check_vision_md
    findings = check_vision_md(Path("/nonexistent-repo-root"))
    assert findings[0].evidence == f"{cdocs.VISION} absent at repo root"


def test_validate_doc_rot_reads_the_registry():
    assert vdr._SECTION_HISTORY_DOCS == list(cdocs.SECTION_HISTORY_DOCS)
    assert vdr._FILE_SIZE_BUDGETS == {cdocs.CLAUDE: 200}


def test_validate_doc_structure_reads_the_registry():
    assert vds._STRUCTURE_DOCS == list(cdocs.STRUCTURE_DOCS)


def test_validate_hermetization_seals_exactly_the_registry_living_docs():
    """ADR-101 §1's Tier-1 `.md` set = the ADR-38 canonical set PLUS `AGENTS.md`
    and `README.md`.

    ADR-115 admits `AGENTS.md` as a Tier-1 file WITHOUT making it a canonical living
    doc: it is portable-instruction payload, not a freshness-stamped governance
    surface. **ADR-114 (Accepted 2026-08-29, AMENDMENT 1) admits `README.md`** on its
    `Amends` line — *"the closed Tier-1 file enum in `SANCTIONED_TIER1_FILES` would
    gain `README.md`"* — for the opposite reason: it IS canonical in substance at the
    hub (it supersedes `VISION.md`), but promoting it into `CANONICAL_MANDATORY` would
    enrol it in `ADR38_BASELINE_REQUIRED` and in every consumer's canonical-set check
    while only 2 of the 8 ADR-104 children carry one. That promotion is the sequenced
    fleet migration, `[#621]`.

    Each divergence is written as an explicit **named** exception, with the ADR that
    admitted it, so that a third one cannot slip in unnamed. Executed by `[#614]`.
    """
    md_members = {n for n in vh.SANCTIONED_TIER1_FILES if n.endswith(".md")}
    assert md_members == set(cdocs.CANONICAL_MANDATORY) | {"AGENTS.md", "README.md"}


def test_gen_handoff_name_and_degrade_string_move_together():
    """R2 §1.4 R2: this generator does not crash on a missing section — it stamps a
    placeholder into a bundle that is immutable the moment it is committed. So the filename
    and its degrade contract live in one place, and this pins that they do."""
    assert gh._vision_extract(Path("/nonexistent-repo-root")) == cdocs.VISION_EXTRACT_MISSING
    assert cdocs.VISION in cdocs.VISION_EXTRACT_MISSING
    assert cdocs.VISION_EXTRACT_HEADING == "## Vision"


@pytest.mark.live_repo
def test_gen_handoff_still_extracts_the_live_vision_section():
    extract = gh._vision_extract(_REPO_ROOT)
    assert extract and extract != cdocs.VISION_EXTRACT_MISSING


# --- the two deploy-carried copies ----------------------------------------------------------

def _literal_fallback(module, symbol: str):
    """Parse the `else:` fallback assignment out of a guarded-import module's source.

    Read from the SOURCE, deliberately: at the hub the guarded import succeeds, so the live
    attribute is the registry's value and comparing it to itself proves nothing. The consumer
    runs the other branch, and the other branch is only visible in the text.
    """
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        for stmt in node.orelse:
            if isinstance(stmt, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == symbol for t in stmt.targets):
                return ast.literal_eval(stmt.value)
    raise AssertionError(f"no literal fallback for {symbol} in {module.__file__}")


def test_freshness_gate_live_value_is_the_registry():
    assert cfg.DEFAULT_FRESHNESS_FILES == list(cdocs.FRESHNESS_FILES)


def test_freshness_gate_consumer_fallback_equals_the_registry():
    assert _literal_fallback(cfg, "DEFAULT_FRESHNESS_FILES") == list(cdocs.FRESHNESS_FILES)


def test_backpressure_live_values_are_the_registry():
    assert seb._CANON == tuple(cdocs.BACKPRESSURE_CANON)
    assert seb._JOURNAL == cdocs.JOURNAL
    assert seb._BACKLOG == cdocs.BACKLOG


def test_backpressure_consumer_fallback_equals_the_registry():
    assert _literal_fallback(seb, "_CANON") == tuple(cdocs.BACKPRESSURE_CANON)
    assert _literal_fallback(seb, "_JOURNAL") == cdocs.JOURNAL
    assert _literal_fallback(seb, "_BACKLOG") == cdocs.BACKLOG


def test_the_fallback_parser_would_notice_a_drifted_fallback(tmp_path):
    """Teeth for the parser itself — a helper that silently returns nothing on a shape it does
    not understand would make the two tests above vacuous."""
    mod = tmp_path / "m.py"
    mod.write_text("if x:\n    A = ['live']\nelse:\n    A = ['drifted']\n", encoding="utf-8")

    class _Fake:
        __file__ = str(mod)

    assert _literal_fallback(_Fake, "A") == ["drifted"]
    with pytest.raises(AssertionError):
        _literal_fallback(_Fake, "B")


# --- the cross-language site (R2 seam S11) ---------------------------------------------------

@pytest.mark.live_repo
def test_the_conformance_hub_scan_list_agrees_with_the_registry():
    """Seam S11. A JavaScript string list cannot import Python, so the coupling is a read."""
    text = (_REPO_ROOT / _CONFORMANCE_HUB).read_text(encoding="utf-8")
    m = re.search(r"Scan these files for VERIFIABLE FACTUAL claims[^:]*:\s*(.+?)\.\s+Do NOT scan",
                  text)
    assert m, "the V2 verifier scan-list sentence was not found"
    listed = [tok.strip() for tok in m.group(1).split(",")]
    assert listed == list(cdocs.CONFORMANCE_V2_SCAN)
