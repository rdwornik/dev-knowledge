"""decision_carriage.py -- the seed of the batch-close dispositions gate (R90).

The pure legs only: the proposal never claims done-ness, a lane landed inside another merge
counts as carried, a fates line never lends one lane's sha to the next, the name match is
bounded, and `render` writes entries for ACCEPTED stems only, as source the register can hold.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import decision_carriage as dc  # noqa: E402


def _ev(stem="AMEND-X-2026-10-04", lanes=None, successor=None, signals=None, record=None):
    ev = {"decision": f"to-cc/{stem}.md", "stem": stem, "exists": True, "lanes": lanes or {},
          "signals": signals or {}, "render_record": record or []}
    if successor is not None:
        ev["successor"] = successor
    return ev


def _lane(merges=(), tips=()):
    return {"merges": list(merges), "tags": {}, "tips_on_ref": list(tips)}


def test_propose_reads_lane_merges_and_never_more():
    assert dc.propose(_ev(lanes={"b2-a": _lane(["1627e74c"])})) == dc.PROPOSE_ALL
    assert dc.propose(_ev(lanes={"b2-a": _lane(["1627e74c"]), "b2-b": _lane()})) == dc.PROPOSE_SOME
    assert dc.propose(_ev(lanes={"b2-a": _lane()})) == dc.PROPOSE_NONE
    assert dc.propose(_ev()) == dc.PROPOSE_NO_LANES


def test_a_lane_landed_inside_another_merge_counts_as_merged():
    ev = _ev(lanes={"foundation-4-merge-gate": _lane(tips=["2dd2067d"])})
    assert dc.propose(ev) == dc.PROPOSE_ALL
    assert "tip 2dd2067d is an ancestor of main" in dc.reason_for(ev, "R.")


def test_a_superseded_file_with_a_live_successor_is_superseded():
    ev = _ev("AMEND-X-2026-10-03-v1-superseded",
             successor={"file": "to-cc/AMEND-X-2026-10-03.md", "exists": True})
    assert dc.propose(ev) == dc.PROPOSE_SUPERSEDED
    assert dc.reason_for(ev, "R.").startswith("SUPERSEDED, never pasted; successor to-cc/")


def test_lane_merges_match_the_branch_name_not_a_substring():
    merges = [("aaaa111", "Merge branch 'worktree-b2-ci-poll' @ x"),
              ("bbbb222", "Merge branch 'worktree-b2-ci-poll-2' @ y")]
    assert dc.lane_merges("b2-ci-poll", merges) == ["aaaa111"]


def test_state_tips_stay_inside_the_lanes_own_clause(tmp_path):
    (tmp_path / "to-browser").mkdir()
    (tmp_path / "to-browser" / "STATE-BATCH-F.md").write_text(
        "fates: WAITING -- foundation-4-merge-gate (from its branch 2dd2067d), "
        "foundation-7-ci-poll, foundation-12-hooks-to-ci (seat ruling 2026-10-04); FAILED\n",
        encoding="utf-8")
    assert dc.state_tips(tmp_path, "foundation-4-merge-gate") == ["2dd2067d"]
    assert dc.state_tips(tmp_path, "foundation-7-ci-poll") == []
    assert dc.state_tips(tmp_path, "foundation-12-hooks-to-ci") == []


def test_name_pattern_is_bounded():
    pat = dc.name_pattern("AMEND-BATCH-FOUNDATION-2026-10-03")
    assert pat.search("## AMEND-BATCH-FOUNDATION applied")
    assert not pat.search("## AMEND-BATCH-FOUNDATION-3 applied")
    assert dc.name_pattern("AMEND-BATCH-FOUNDATION-3-2026-10-03").search(
        "## AMEND-BATCH-FOUNDATION-3 applied")


def test_render_writes_accepted_stems_only_as_register_source():
    evs = [_ev("AMEND-A-2026-10-04", lanes={"b2-a": _lane(["1627e74c"])}),
           _ev("AMEND-B-2026-10-04", lanes={"b2-b": _lane(["42ba43c2"])})]
    out = dc.render(evs, {"AMEND-A-2026-10-04": "extra fact"}, ruling="Ruled.", owner="o")
    assert '"declare:AMEND-A-2026-10-04"' in out and "AMEND-B" not in out
    tree = ast.parse("d = {\n" + out + "\n}")
    (value,) = tree.body[0].value.values
    reason = value.keywords[0].value.value
    assert "merged 1627e74c" in reason and "; extra fact. Ruled." in reason
