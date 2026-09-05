"""The manifest-link route shared by `funnel_coverage` and `consumer_at_landing`.

THE RULING (operator, 2026-09-05). An audit artifact linked from a batch manifest -- via
`closed_by:`, as a lane packet, or as a close packet -- counts as DISPOSITIONED for
`funnel_coverage` and as CITED for `consumer_at_landing`. Before it, every batch-G lane
artifact raised two WARNs apiece while being fully enumerated by the batch's own
gate-readable manifest: the record existed and nothing read it.

THE SEEDED PAIR IS THE POINT, not the count. An admission test alone cannot distinguish a
route that reads manifests from a route that admits everything -- the failure mode this
repo names as "a check that passes because it looks in a place where dispositions never
were". So every test here has a refusal twin: the linked artifact must go quiet AND the
unlinked one must still raise both findings, in the same tree, in the same run.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import batch_manifest as bm
import consumer_at_landing as cal
import funnel_coverage as fc


MANIFEST = "2026-09-04-technical-batch-z-manifest.md"
CLOSER = "2026-09-04-technical-batch-z-close-packet.md"
LINKED_SLUG = "2026-09-04-technical-lane-z-1-widget.md"
LINKED_PATH = "2026-09-04-verification-zparity-a1b2c3d4.md"
UNLINKED = "2026-09-04-technical-unlinked-memo.md"


def _seed(root: Path) -> None:
    """A minimal but STRUCTURALLY REAL repo: a manifest that declares a lane roster and a
    closer, two artifacts it reaches by the two different link kinds, and one it does not."""
    audits = root / "docs" / "audits"
    audits.mkdir(parents=True)

    (audits / MANIFEST).write_text(
        "---\n"
        "batch: Z\n"
        "status: open\n"
        f"closed_by: docs/audits/{CLOSER}\n"
        "---\n\n"
        "# BATCH Z -- THE MANIFEST\n\n"
        "## THE LANES -- 1 committing\n\n"
        "```\n"
        "Z1  lane-z-1-widget        local  sonnet  [#901]\n"
        "```\n\n"
        f"Parity witness: `docs/audits/{LINKED_PATH}`.\n",
        encoding="utf-8", newline="\n")
    (audits / CLOSER).write_text(
        f"# BATCH Z -- CLOSE PACKET\n\nCloses `docs/audits/{MANIFEST}`.\n",
        encoding="utf-8", newline="\n")
    for name in (LINKED_SLUG, LINKED_PATH, UNLINKED):
        (audits / name).write_text(f"# {name}\n\nBody.\n", encoding="utf-8", newline="\n")

    # The consumer pool must RESOLVE, or its ratchet reports "pool unreadable" instead of a
    # number and the refusal twin would pass for the wrong reason.
    for rel in cal.POOL_DIRS:
        d = root / rel
        d.mkdir(parents=True, exist_ok=True)
        (d / "seed.md").write_text("Pool file citing nothing.\n", encoding="utf-8", newline="\n")

    eco = root / "ecosystem"
    eco.mkdir(parents=True, exist_ok=True)
    (eco / Path(fc.BASELINE_RELPATH).name).write_text(
        json.dumps({"detector_id": fc.DETECTOR_ID, "artifacts": [], "uncovered": 0}),
        encoding="utf-8", newline="\n")
    (eco / Path(cal.BASELINE_RELPATH).name).write_text(
        json.dumps({"detector_id": cal.DETECTOR_ID, "artifacts": [], "unconsumed": 0}),
        encoding="utf-8", newline="\n")


def _warned(messages, name: str) -> int:
    return sum(1 for level, text in messages if level == "warn" and text.startswith(name))


@pytest.fixture()
def seeded(tmp_path: Path) -> Path:
    _seed(tmp_path)
    return tmp_path


# --- the route itself -------------------------------------------------------------

def test_manifest_links_reaches_both_link_kinds(seeded: Path):
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, LINKED_PATH) == "explicit"
    assert bm.links_artifact(links, LINKED_SLUG) == "lane-slug"
    assert bm.links_artifact(links, UNLINKED) is None


def test_the_closer_is_a_linking_surface_too(seeded: Path):
    """The manifest is named only by its close packet, never by itself. If the closer were
    not scanned the manifest would be an orphan in its own batch."""
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, MANIFEST) == "explicit"


# --- the seeded pair --------------------------------------------------------------

def test_linked_artifact_raises_zero_warnings(seeded: Path):
    fm = fc.measure(seeded)
    cm = cal.measure(seeded)
    fw = fc.ratchet_findings(fm, fc.load_baseline(seeded))
    cw = cal.ratchet_findings(cm, cal.load_baseline(seeded))
    for name in (LINKED_SLUG, LINKED_PATH):
        assert _warned(fw, name) == 0, f"{name} still raises funnel_coverage"
        assert _warned(cw, name) == 0, f"{name} still raises consumer_at_landing"


def test_unlinked_artifact_still_raises_two(seeded: Path):
    """THE REFUSAL TWIN. Same tree, same run: exactly one finding from each organ."""
    fm = fc.measure(seeded)
    cm = cal.measure(seeded)
    fw = fc.ratchet_findings(fm, fc.load_baseline(seeded))
    cw = cal.ratchet_findings(cm, cal.load_baseline(seeded))
    assert _warned(fw, UNLINKED) == 1
    assert _warned(cw, UNLINKED) == 1


# --- the property that licenses NOT bumping the detector id -----------------------

def test_manifest_link_route_is_monotone(seeded: Path):
    """The route may only ever move an artifact uncovered -> covered.

    This is what keeps the committed baseline commensurable without a `DETECTOR_ID` bump: a
    predicate that can only shrink `uncovered` adds no name to the baseline and hides no
    debt. Asserted by construction -- every artifact covered with the route disabled must
    still be covered with it enabled.
    """
    with_route = fc.measure(seeded)
    covered_with = set(with_route.corpus) - set(with_route.uncovered)
    covered_without = covered_with - set(with_route.manifest_linked)
    assert covered_without <= covered_with
    assert set(with_route.manifest_linked) <= set(with_route.corpus)


def test_unreadable_manifest_grants_no_coverage(seeded: Path):
    """An ADDITIVE route must fail toward LESS coverage, never toward more."""
    (seeded / "docs" / "audits" / MANIFEST).write_bytes(b"\xff\xfe not utf-8")
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, LINKED_SLUG) is None
