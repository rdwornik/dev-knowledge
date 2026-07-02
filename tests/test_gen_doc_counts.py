"""Tests for scripts/gen_doc_counts.py — the #222 doc-counts generator.

gen_doc_counts.py moves ARCHITECTURE.md's three volatile count claims into the
committed-generated ecosystem/doc-counts.md (NOT a freshness file), so a count bump no
longer trips canonical_freshness A2 into forcing a last_reviewed re-stamp. These tests are
PURE (no subprocess, no live-file mutation): they guard the two things that could silently
break the decouple — the template<->regex coupling with validate_doc_claims._CLAIMS, and the
marker splice. Regeneration + reconcile-against-live is covered by the #208 registry guards
in test_validate_doc_claims.py (which now read the repointed ecosystem/doc-counts.md).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_doc_counts as gdc  # noqa: E402
import validate_doc_claims as vdc  # noqa: E402


def test_count_claim_names_match_the_nonset_claims():
    # The generator owns exactly the count claims (kind == "count"); the CLAUDE §9 roster
    # set-claim is NOT moved. If a future count claim is appended to _CLAIMS, this fails
    # until the generator's _COUNT_CLAIM_NAMES + _TEMPLATES are extended in lockstep.
    count_claims = {c.name for c in vdc._CLAIMS if c.kind == "count"}
    assert set(gdc._COUNT_CLAIM_NAMES) == count_claims
    assert set(gdc._TEMPLATES) == count_claims


def test_every_count_claim_points_at_doc_counts_md():
    # The whole #222 decouple rests on these three claims living OUTSIDE a freshness file.
    for c in vdc._CLAIMS:
        if c.kind == "count":
            assert c.doc == "ecosystem/doc-counts.md", \
                f"{c.name} must live in the decoupled doc-counts.md, not {c.doc}"


def test_rendered_line_matches_the_claim_regex():
    # The self-detecting coupling: each template, formatted with a sample integer, must match
    # the corresponding _CLAIMS anchor — else the regenerated file would read as anchor-missing.
    by_name = {c.name: c for c in vdc._CLAIMS}
    for name, template in gdc._TEMPLATES.items():
        line = template.format(1234)
        anchor = by_name[name].anchor
        m = anchor.search(line)
        assert m is not None, f"{name}: template {template!r} does not match its _CLAIMS regex"
        assert m.group(1) == "1234"


def test_splice_replaces_only_between_markers():
    content = (
        "# Doc\n\nintro paragraph\n\n"
        f"{gdc._START_MARKER}\nOLD LINE\n{gdc._END_MARKER}\n\ntrailer\n"
    )
    out = gdc._splice(content, "NEW LINE\n")
    assert "OLD LINE" not in out
    assert "NEW LINE" in out
    assert out.startswith("# Doc\n\nintro paragraph")
    assert out.endswith("trailer\n")
    assert gdc._START_MARKER in out and gdc._END_MARKER in out
    # idempotent shape: splicing the same block again yields the same result
    assert gdc._splice(out, "NEW LINE\n") == out


def test_splice_raises_without_markers():
    import pytest
    with pytest.raises(RuntimeError):
        gdc._splice("# Doc\n\nno markers here\n", "block\n")
