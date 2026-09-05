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

def test_manifest_link_route_is_monotone(seeded: Path, monkeypatch):
    """The route may only ever move an artifact uncovered -> covered.

    This is what keeps the committed baseline commensurable without a `DETECTOR_ID` bump: a
    predicate that can only shrink `uncovered` adds no name to the baseline and hides no
    debt. Asserted by construction -- every artifact covered with the route disabled must
    still be covered with it enabled.
    """
    with_route = fc.measure(seeded)
    covered_with = set(with_route.corpus) - set(with_route.uncovered)

    # THE ROUTE IS GENUINELY DISABLED, not subtracted (terra, pass 3, record-only -- and the
    # criticism was right). The first version derived `covered_without` as
    # `covered_with - manifest_linked`, which makes the containment true by set algebra: it
    # passed with the route deleted, and asserted nothing about it. That is this file's own
    # named failure mode -- a check that passes because it looks in a place where dispositions
    # never were -- committed inside the test written to prevent it.
    monkeypatch.setattr(bm, "links_artifact", lambda *_a, **_k: None)
    without_route = fc.measure(seeded)
    covered_without = set(without_route.corpus) - set(without_route.uncovered)

    assert not without_route.manifest_linked, "the route was not actually disabled"
    assert covered_without <= covered_with, (
        "the route removed coverage from an artifact that had it without the route -- it is "
        "additive by contract, so this can only mean it is not")
    # ... and it must actually DO something here, or the containment above is vacuous again.
    assert covered_with - covered_without, (
        "the seeded tree exercises the route not at all; the monotonicity claim is untested")
    assert set(with_route.manifest_linked) <= set(with_route.corpus)


def test_unreadable_manifest_grants_no_coverage(seeded: Path):
    """An ADDITIVE route must fail toward LESS coverage, never toward more."""
    (seeded / "docs" / "audits" / MANIFEST).write_bytes(b"\xff\xfe not utf-8")
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, LINKED_SLUG) is None


def test_a_document_ABOUT_a_lane_is_not_that_lane_s_artifact(seeded: Path):
    """terra HIGH, pre-merge. The leg was `slug in stem`, which admitted a REVIEW of a lane
    as if it were the lane's own packet -- granting both DISPOSITIONED and CITED and silencing
    both ratchets at once. Silent false coverage is the failure mode `funnel_coverage` exists
    to prefer loud false WARNs over, so this is the sharpest test in the module."""
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "2026-09-05-technical-review-of-lane-z-1-widget.md") is None
    assert bm.links_artifact(links, "2026-09-05-technical-notes-on-lane-z-1-widget.md") is None
    # ... while the lane's own artifacts, which BEGIN with the slug, still resolve.
    assert bm.links_artifact(links, LINKED_SLUG) == "lane-slug"
    assert bm.links_artifact(links, "2026-09-05-technical-lane-z-1-widget-close-packet.md")         == "lane-slug"


def test_the_slug_boundary_is_respected(seeded: Path):
    """`lane-z-1-widget` must not admit `lane-z-1-widgetry`: a prefix is not a lane."""
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "2026-09-05-technical-lane-z-1-widgetry.md") is None


def test_an_undated_stem_has_no_tail_to_anchor_and_is_refused(seeded: Path):
    """Refused rather than fuzzily matched -- the additive route fails toward LESS coverage."""
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "lane-z-1-widget.md") is None


# --- the enum-first class split (terra HIGH, pass 2) ------------------------------------------
# The anchor's first cut used a letters-only `[a-z]+` class segment, which got BOTH ends of the
# real audit-name grammar wrong. These four pin the widening; the first two FAIL under the
# reverted regex, which is what makes them regressions rather than decoration.

def test_a_digit_bearing_class_still_yields_the_lane_tail(seeded: Path):
    """`arc5`, `phase0`, `stage3`, `pilot81`, `cohort1` are all real classes on disk.

    A letters-only class cannot match any of them, so a lane's OWN artifact landing under one
    was refused -- a false NEGATIVE introduced while fixing a false positive.
    """
    assert bm.artifact_tail("2026-09-05-arc5-lane-z-1-widget") == "lane-z-1-widget"
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "2026-09-05-arc5-lane-z-1-widget.md") == "lane-slug"


def test_a_hyphenated_ruled_class_yields_the_lane_tail(seeded: Path):
    """`ecosystem-audit` is one ruled class, not `ecosystem` followed by a tail of `audit-...`.

    Longest-match over the enum is what makes the multi-segment classes split whole.
    """
    assert bm.artifact_tail("2026-09-05-ecosystem-audit-lane-z-1-widget") == "lane-z-1-widget"
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "2026-09-05-ecosystem-audit-lane-z-1-widget.md") == "lane-slug"


def test_the_widening_does_not_readmit_a_document_ABOUT_a_lane(seeded: Path):
    """The pass-1 HIGH, re-asked under BOTH new class shapes.

    Widening the class split is only safe if the anchor still holds after it -- a fix that
    recovers false negatives by reopening the false positive has traded one silent wrong
    answer for another.
    """
    links = bm.manifest_links(seeded)
    assert bm.links_artifact(links, "2026-09-05-arc5-review-of-lane-z-1-widget.md") is None
    assert bm.links_artifact(
        links, "2026-09-05-ecosystem-audit-notes-on-lane-z-1-widget.md") is None


def test_the_class_enum_is_the_hermetization_module_s_own_object(seeded: Path):
    """IDENTITY, not equality -- the `LANE_BRANCH_RE` precedent in `batch_manifest`.

    A second enum object means a second grammar, and this one governs an exemption: widen it
    and a document ABOUT a lane splits at a longer class and is admitted as that lane's
    artifact. `validate_hermetization` owns the ADR-101 name grammar; this module borrows it.
    """
    import validate_hermetization as vh
    assert bm.AUDIT_CLASS_ENUM is vh.AUDIT_CLASS_ENUM


def test_artifact_tail_refuses_a_stem_that_is_all_class_and_no_tail():
    """`<date>-<class>` with nothing after it has no tail to anchor against."""
    assert bm.artifact_tail("2026-09-05-technical") is None
    assert bm.artifact_tail("2026-09-05-technical-") is None
    assert bm.artifact_tail("not-a-dated-stem-at-all") is None


#: The WIDENING shadow, made concrete. A shadowed enum carrying `technical-review-of` makes
#: `2026-09-05-technical-review-of-lane-g-276-deploy-waiver` split at that longer class, so its
#: tail becomes `lane-g-276-deploy-waiver` -- and the document ABOUT lane g-276 is admitted as
#: that lane's own artifact. That is the pass-1 HIGH, reopened from outside the file.
_HERMETIZATION_SHADOW_PROBE = '''
import sys, types
sys.path.insert(0, {scripts!r})
shadow = types.ModuleType("validate_hermetization")
shadow.__file__ = "/nowhere/validate_hermetization.py"
shadow.AUDIT_CLASS_ENUM = frozenset({{"technical-review-of"}})
sys.modules["validate_hermetization"] = shadow
try:
    import batch_manifest as bm
except ImportError:
    print("REFUSED")
    raise SystemExit(0)
import validate_hermetization as vh
print("IDENTITY_HOLDS" if bm.AUDIT_CLASS_ENUM is vh.AUDIT_CLASS_ENUM else "IDENTITY_BROKEN")
links = bm.ManifestLinks(frozenset(), frozenset({{"lane-g-276"}}), ())
name = "2026-09-05-technical-review-of-lane-g-276-deploy-waiver.md"
print("FALSE_COVERAGE" if bm.links_artifact(links, name) else "STILL_REFUSED")
'''


def test_a_preloaded_shadow_of_the_hermetization_module_is_REFUSED_at_import():
    """The hole `test_the_class_enum_is_the_hermetization_module_s_own_object` CANNOT see.

    TERRA HIGH, PASS 3, AND THE CRITICISM IS EXACT. That identity assertion compares
    `bm.AUDIT_CLASS_ENUM` with `vh.AUDIT_CLASS_ENUM`, and both names resolve through the SAME
    `sys.modules` entry -- so a preloaded shadow makes the two agree perfectly while a
    FABRICATED grammar governs the exemption. The assertion passes with the provenance guard
    deleted, which means it tests the wrong thing on its own: it pins that there is one enum,
    not that the enum is the RIGHT one.

    This is the same shape as `test_a_preloaded_shadow_of_the_enum_module_is_REFUSED_at_import`
    in `tests/test_batch_manifest.py`, and it is here for the same reason that one exists: the
    2026-08-11 terra HIGH established that a name-import CAN suffer the `gitenv` failure mode,
    against the argument that it could not.

    The probe does not merely assert refusal -- it carries the attack, so a future reader can
    see what the guard buys. With the guard removed the probe prints IDENTITY_HOLDS then
    FALSE_COVERAGE: a document ABOUT lane g-276 admitted as that lane's own artifact, silencing
    both ratchets. Run in a SUBPROCESS because a shadow installed in this interpreter would
    poison every later test in the worker.
    """
    import subprocess
    import sys as _sys

    scripts = str(Path(__file__).resolve().parent.parent / "scripts")
    probe = _HERMETIZATION_SHADOW_PROBE.format(scripts=scripts)
    proc = subprocess.run([_sys.executable, "-c", probe], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=60)
    out = proc.stdout.strip()
    assert out == "REFUSED", (
        "a preloaded shadow of validate_hermetization was NOT refused at import; "
        f"probe said {out!r} (stderr: {proc.stderr.strip()[:400]!r})")
