"""W-G3 migrations onto FPG-1, one organ per section, each with its diff = 0 proof ([#664]).

ADR-118 section 5 rules the migration *"one per lane, each proving its edge set is a subset of
FPG-1 (diff = 0) before the old computation is retired"*; lane `ab-664-spine-witnessed`'s frozen
contract orders it one organ per COMMIT. Either way the proof is the same object, so each
migration here carries two witnesses:

  1. a FIXTURE witness, RED before the loader existed, that the relation now arrives as FPG-1
     edges with its link kind on the edge;
  2. a DIFF witness against the organ's own answer -- on the fixture and on the live tree -- so
     "the graph holds it" is measured rather than asserted. Where the two answers are not
     byte-equal the difference is NAMED, and the test pins that it is exactly that difference.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import batch_manifest as bm  # noqa: E402
import consumer_at_landing as cal  # noqa: E402
import file_purpose_graph as fpg  # noqa: E402
import graph_queries as gq  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


# ============================================ migration 1: batch_manifest.manifest_links


MANIFEST = "2026-09-04-technical-batch-z-manifest.md"
CLOSER = "2026-09-04-technical-batch-z-close-packet.md"
LINKED_SLUG = "2026-09-04-technical-lane-z-1-widget.md"
LINKED_PATH = "2026-09-04-verification-zparity-a1b2c3d4.md"
UNLINKED = "2026-09-04-technical-unlinked-memo.md"


@pytest.fixture
def batch_repo(tmp_path: Path) -> Path:
    """The `tests/test_manifest_link_route.py` shape: a manifest reaching one artifact by path
    and one by lane slug, a closer that names the manifest, and one artifact nothing links."""
    audits = tmp_path / "docs" / "audits"
    _write(audits / MANIFEST,
           "---\nbatch: Z\nstatus: open\n"
           f"closed_by: docs/audits/{CLOSER}\n---\n\n"
           "# BATCH Z\n\n## THE LANES -- 1 committing\n\n"
           "```\nZ1  lane-z-1-widget        local  sonnet  [#901]\n```\n\n"
           f"Parity witness: `docs/audits/{LINKED_PATH}`.\n")
    _write(audits / CLOSER, f"# BATCH Z -- CLOSE PACKET\n\nCloses `docs/audits/{MANIFEST}`.\n")
    for name in (LINKED_SLUG, LINKED_PATH, UNLINKED):
        _write(audits / name, f"# {name}\n\nBody.\n")
    for rel in cal.POOL_DIRS:
        _write(tmp_path / rel / "seed.md", "Pool file citing nothing.\n")
    return tmp_path


def _manifest_link_edges(graph: fpg.PurposeGraph) -> dict[str, set[str]]:
    """target basename -> the set of surface paths that link it, read from FPG-1 ONLY."""
    out: dict[str, set[str]] = {}
    for edge in graph.all_edges():
        if (edge.kind == fpg.EDGE_CONSUMED_BY and edge.source == fpg.INPUT_CONSUMER_AT_LANDING
                and edge.detail.startswith(fpg.MANIFEST_LINK_DETAIL_PREFIX)):
            src, dst = graph.node(edge.src), graph.node(edge.dst)
            out.setdefault(dst.path.rsplit("/", 1)[-1], set()).add(src.path)
    return out


def test_manifest_links_arrive_as_FPG1_consumed_by_edges_attributed_to_their_surface(batch_repo):
    """THE FIXTURE WITNESS. Each link is an edge FROM the surface that wrote it -- the manifest
    for its own roster and paths, the CLOSER for the manifest it closes -- with the link kind
    on the edge. The unlinked artifact carries none."""
    edges = _manifest_link_edges(fpg.build(batch_repo))
    assert edges.get(LINKED_PATH) == {f"docs/audits/{MANIFEST}"}
    assert edges.get(LINKED_SLUG) == {f"docs/audits/{MANIFEST}"}
    assert edges.get(MANIFEST) == {f"docs/audits/{CLOSER}"}, \
        "the manifest is linked by its closer, never by itself"
    assert UNLINKED not in edges
    graph = fpg.build(batch_repo)
    details = {e.detail for e in graph.all_edges()
               if e.detail.startswith(fpg.MANIFEST_LINK_DETAIL_PREFIX)}
    assert details == {f"{fpg.MANIFEST_LINK_DETAIL_PREFIX}explicit",
                       f"{fpg.MANIFEST_LINK_DETAIL_PREFIX}lane-slug"}


def test_the_per_surface_split_is_exactly_the_union_the_organs_already_read(batch_repo):
    """Splitting the parser by surface must not move a single link: the union of the per-
    surface answers IS `manifest_links`, field for field."""
    surfaces = bm.manifest_link_surfaces(batch_repo)
    union = bm.manifest_links(batch_repo)
    assert frozenset().union(*(s.explicit for s in surfaces.values())) == union.explicit
    assert frozenset().union(*(s.lane_slugs for s in surfaces.values())) == union.lane_slugs


def _diff(root: Path) -> tuple[set[str], set[str]]:
    """(organ-only, graph-only) basenames for the manifest-link relation."""
    organ = set(cal.measure(root).manifest_linked)
    graph = set(_manifest_link_edges(fpg.build(root)))
    return organ - graph, graph - organ


def test_manifest_link_diff_is_ZERO_on_the_fixture(batch_repo):
    assert _diff(batch_repo) == (set(), set())


def test_manifest_link_diff_on_the_LIVE_tree_is_zero_but_for_named_self_links():
    """THE DIFF WITNESS on this repo's own corpus.

    One difference is structural and is named rather than rounded away: FPG-1 drops a self
    edge by construction (`PurposeGraph.add_edge`), so an artifact whose ONLY link is its own
    manifest naming itself is linked in the organ's answer and absent from the graph. The test
    pins that every organ-only name is exactly such a self-link, and that the graph invents
    nothing the organ does not hold."""
    organ_only, graph_only = _diff(REPO_ROOT)
    assert graph_only == set(), f"FPG-1 links artifacts the organ does not: {sorted(graph_only)}"
    surfaces = bm.manifest_link_surfaces(REPO_ROOT)
    for name in organ_only:
        linkers = {rel for rel, links in surfaces.items() if bm.links_artifact(links, name)}
        assert linkers == {f"docs/audits/{name}"}, (
            f"{name} is linked by {sorted(linkers)} yet absent from FPG-1 -- not a self-link")


def test_the_register_row_for_manifest_links_is_reconciled():
    row = gq.EDGE_COMPUTATIONS.get("scripts/batch_manifest.py::manifest_link_surfaces")
    assert row is not None and row.status == "reconciled"
    assert "scripts/batch_manifest.py" not in gq.EDGE_COMPUTATIONS
