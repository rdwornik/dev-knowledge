"""RED-first witnesses for `decision_coverage` ([#692], A9-1..A9-3, ADR-108 §B).

Every test in this file was written and run RED before `scripts/decision_coverage.py`
existed. The frozen contract's clause 1 names the trip-test in one sentence — *"an accepted
decision with no row makes the query FAIL"* — and this file carries it plus the other
direction, because **a test that passes on conforming input is not a trip-test** and a gate
that can only fail is not a gate.

WHAT EACH GROUP WITNESSES:

  1. the POPULATION — three classes (ADR `Accepted`, intake `ACCEPTED`/`RATIFIED`, a
     transport `DECLARE-`/`AMEND-`), read from the documents because a decision nothing
     cites has no node in FPG-1 and is exactly the decision this query must see;
  2. the LIFECYCLE — every decision lands on one of A9-1's five states, and each mapping is
     pinned separately so a silent collapse (everything `considered`) cannot pass;
  3. the REFUSAL at commit tier, BOTH directions, plus the refusal TEXT: A9-1 requires it to
     list the decisions AND state what must be done;
  4. the ERA BOUND — the one design ruling this lane makes. It is pinned from both sides so
     it can neither widen into a tree-wide wedge nor quietly evaporate;
  5. the GRAPH half — `implements` runs from the ROW to the DECISION on FPG-1, never from a
     private scan here (ADR-118 §1: a new edge kind is added to FPG-1, never to a script);
  6. the `implements:` frontmatter key — STRUCTURED and VALIDATED, which is clause 2's word;
  7. A9-2's ledger and A9-3's four numbers.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import decision_coverage as dc  # noqa: E402
import file_purpose_graph as fpg  # noqa: E402
import graph_store as gs  # noqa: E402
import validate_backlog as vb  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------------------- the fixture


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _adr(root: Path, number: int, status: str, date: str, slug: str) -> None:
    _write(root / "docs" / "decisions" / f"ADR-{number}-{slug}.md",
           f"# ADR-{number}: {slug.replace('-', ' ')}\n\n"
           f"**Status:** {status}\n"
           f"**Date:** {date}\n\n"
           f"## Context\nA fixture decision.\n")


def _intake(root: Path, intake_id: int, status: str, date: str, slug: str) -> None:
    _write(root / "docs" / "intake" / f"{date}-{slug}.md",
           f"---\nintake-id: {intake_id}\nstatus: {status}\nconsumed-by:\n---\n\n"
           f"# {slug}\n\nA fixture intake.\n")


def _row(root: Path, task_id: int, status: str, implements: str | None, body: str) -> None:
    lines = ["---", f'id: "[#{task_id}]"', f'title: "fixture row {task_id}"',
             f"status: {status}"]
    if implements is not None:
        lines.append(f'implements: "{implements}"')
    lines += ["generates: BACKLOG.md", "---", "",
              f"- [#{task_id}] [P1][S] **fixture row {task_id}** - {body}"
              + (f" · implements: {implements}" if implements else "")
              + " · Done when: the fixture holds · refs none · kill-candidates: none", ""]
    _write(root / "tasks" / f"{task_id}-fixture.md", "\n".join(lines))


#: Far enough past `ARM_DATE` that the fixture never has to be re-dated when the calendar moves.
IN_ERA = "2026-09-12"
#: Comfortably before it — the grandfathered half.
PRE_ERA = "2026-01-05"


@pytest.fixture
def tiny_decisions(tmp_path: Path) -> Path:
    """A minimal tree carrying one decision of every state A9-1 names.

      * `ADR-900` — Accepted, in-era, implemented by the OPEN row `[#800]`   -> executing
      * `ADR-901` — Accepted, in-era, implemented by NOTHING                 -> accepted (REFUSE)
      * `ADR-902` — Proposed, in-era                                         -> considered
      * `ADR-903` — Superseded                                               -> superseded
      * `ADR-904` — Accepted, in-era, implemented by the CLOSED row `[#801]` -> done
      * `ADR-905` — Accepted, PRE-era, implemented by nothing                -> accepted, not refused
      * intake 900 — ACCEPTED, in-era, implemented by nothing                -> accepted (REFUSE)
      * intake 901 — DRAFT                                                   -> considered
    """
    root = tmp_path / "tiny"
    _adr(root, 900, "Accepted", IN_ERA, "accepted-and-executing")
    _adr(root, 901, "Accepted", IN_ERA, "accepted-and-uncovered")
    _adr(root, 902, "Proposed", IN_ERA, "still-considered")
    _adr(root, 903, "Superseded", IN_ERA, "left-the-lifecycle")
    _adr(root, 904, "Accepted", IN_ERA, "accepted-and-done")
    _adr(root, 905, "Accepted", PRE_ERA, "grandfathered")
    _intake(root, 900, "ACCEPTED", IN_ERA, "tech-accepted-and-uncovered")
    _intake(root, 901, "DRAFT", IN_ERA, "tech-still-considered")
    _row(root, 800, "open", "ADR-900", "the open row that implements ADR-900")
    _row(root, 801, "done", "ADR-904", "the CLOSED row that implemented ADR-904")
    _write(root / "ARCHITECTURE.md", "# Architecture\n\nA fixture tree.\n")
    return root


@pytest.fixture
def tiny_store(tiny_decisions: Path, tmp_path: Path):
    db = tmp_path / "store" / "FPG.db"
    gs.rebuild(tiny_decisions, db)
    return gs.open_store(db)


def _by_key(rows: list) -> dict:
    return {d.key: d for d in rows}


# ------------------------------------------------------------- witness 1: the POPULATION


def test_the_population_is_the_three_classes_A9_1_names(tiny_decisions: Path, tiny_store):
    """An ADR, an intake and a transport decision are all decisions, and nothing else is."""
    found = dc.decisions(tiny_decisions, tiny_store)
    assert {d.kind for d in found} == {dc.KIND_ADR, dc.KIND_INTAKE}
    keys = _by_key(found)
    assert "adr:901" in keys and "intake:900" in keys


def test_a_decision_NOTHING_cites_is_still_in_the_population(tiny_decisions: Path, tiny_store):
    """The whole point: FPG-1 mints `adr:N` only for an ADR something CITES, so a query that
    read the population off the graph would be blind to exactly the uncited, unimplemented
    decision this organ exists to find."""
    assert tiny_store.node("adr:901") is None, "fixture premise: nothing cites ADR-901"
    assert "adr:901" in _by_key(dc.decisions(tiny_decisions, tiny_store))


def test_a_transport_decision_file_joins_the_population(tiny_decisions: Path, tiny_store,
                                                        tmp_path: Path):
    transport = tmp_path / "transport"
    _write(transport / "to-cc" / "AMEND-FIXTURE-001.md",
           "carried-by: OPEN\n\n# AMEND-FIXTURE-001\n\nA fixture ruling.\n")
    found = dc.decisions(tiny_decisions, tiny_store, transport=transport)
    keys = _by_key(found)
    assert "declare:AMEND-FIXTURE-001" in keys
    assert keys["declare:AMEND-FIXTURE-001"].kind == dc.KIND_TRANSPORT


def test_an_absent_transport_DEGRADES_it_never_silently_empties(tiny_decisions: Path,
                                                                tiny_store):
    """DEFECT E-29's rule: an unknown boundary is not a clean one. With no transport the ADR
    and intake legs still answer, and the caller can tell that the third class was not read."""
    found = dc.decisions(tiny_decisions, tiny_store, transport=None)
    assert found, "the other two classes must still be measured"
    assert not any(d.kind == dc.KIND_TRANSPORT for d in found)


# ---------------------------------------------------------------- witness 2: the LIFECYCLE


def test_every_decision_lands_on_one_of_the_five_states(tiny_decisions: Path, tiny_store):
    assert dc.LIFECYCLE == (dc.STATE_CONSIDERED, dc.STATE_ACCEPTED, dc.STATE_EXECUTING,
                            dc.STATE_DONE, dc.STATE_SUPERSEDED)
    for d in dc.decisions(tiny_decisions, tiny_store):
        assert d.state in dc.LIFECYCLE, f"{d.key} carries {d.state!r}"


@pytest.mark.parametrize("key,state", [
    ("adr:900", dc.STATE_EXECUTING),     # an OPEN row implements it
    ("adr:901", dc.STATE_ACCEPTED),      # accepted and unexecuted -- the refusal class
    ("adr:902", dc.STATE_CONSIDERED),    # Proposed
    ("adr:903", dc.STATE_SUPERSEDED),    # left the lifecycle
    ("adr:904", dc.STATE_DONE),          # only CLOSED rows implement it
    ("intake:900", dc.STATE_ACCEPTED),
    ("intake:901", dc.STATE_CONSIDERED),
])
def test_each_lifecycle_mapping_separately(tiny_decisions: Path, tiny_store, key, state):
    """Pinned one by one. A single "every state is in the enum" assertion passes just as well
    when the mapping collapses and every decision answers `considered`."""
    assert _by_key(dc.decisions(tiny_decisions, tiny_store))[key].state == state


def test_a_closed_row_does_not_hold_a_decision_EXECUTING(tiny_decisions: Path, tiny_store):
    """`executing` must mean work is in flight. ADR-904's only claimant is closed, so the
    decision is `done` -- the same rule `_open_task_ids` applies to task coverage."""
    d = _by_key(dc.decisions(tiny_decisions, tiny_store))["adr:904"]
    assert d.state == dc.STATE_DONE
    assert d.rows == ("801",)


# ------------------------------------------------- witness 3: the REFUSAL, both directions


def test_an_accepted_decision_with_no_implementing_row_is_REFUSED(tiny_decisions: Path,
                                                                  tiny_store):
    """The frozen contract's clause-1 trip-test, in one assertion."""
    findings = dc.decision_coverage(tiny_decisions, tiny_store,
                                    staged=["docs/decisions/ADR-901-accepted-and-uncovered.md"])
    assert [f.subject for f in findings] == ["ADR-901"]


def test_an_accepted_decision_an_open_row_implements_is_ADMITTED(tiny_decisions: Path,
                                                                 tiny_store):
    """The other direction. A gate that can only fail is not a gate."""
    assert dc.decision_coverage(
        tiny_decisions, tiny_store,
        staged=["docs/decisions/ADR-900-accepted-and-executing.md"]) == []


def test_a_written_disposition_admits_a_decision_with_no_row(tiny_decisions: Path, tiny_store):
    """A9-1's second limb: *"or a written 'no implementation required' disposition"*."""
    register = {"adr:901": dc.Disposition(reason="states a posture, implements nothing",
                                          owner="the architect")}
    findings = dc.decision_coverage(
        tiny_decisions, tiny_store, dispositions=register,
        staged=["docs/decisions/ADR-901-accepted-and-uncovered.md"])
    assert findings == []


def test_a_decision_that_is_not_ACCEPTED_is_never_refused(tiny_decisions: Path, tiny_store):
    """Proposed and Superseded are not accepted; refusing them would make the ADR corpus
    unwritable, since an ADR is Proposed before it is anything else."""
    assert dc.decision_coverage(
        tiny_decisions, tiny_store,
        staged=["docs/decisions/ADR-902-still-considered.md",
                "docs/decisions/ADR-903-left-the-lifecycle.md"]) == []


def test_the_refusal_NAMES_the_decision_and_states_what_must_be_done(tiny_decisions: Path,
                                                                     tiny_store):
    """A9-1 in its own words: *"the refusal lists the decisions and states what must be
    done -- the operator's rule that a process deviation raises an exception that teaches the
    browser."* An exception that names a defect and not its repair teaches nothing."""
    [finding] = dc.decision_coverage(
        tiny_decisions, tiny_store,
        staged=["docs/decisions/ADR-901-accepted-and-uncovered.md"])
    assert "ADR-901" in finding.subject
    assert "implements:" in finding.evidence
    assert "no implementation required" in finding.evidence


def test_the_commit_tier_leg_reads_the_STAGED_set(tiny_decisions: Path, tiny_store):
    """Scoped to what this commit writes, like `task_coverage`. An empty staged set is a
    clean commit, not a vacuous pass -- the era leg below is what reaches the rest."""
    assert dc.decision_coverage(tiny_decisions, tiny_store, staged=[]) == []


def test_the_cli_exits_non_zero_on_a_refusal(tiny_decisions: Path, tmp_path: Path):
    out = subprocess.run(
        [sys.executable, str(_SCRIPTS / "decision_coverage.py"), "check",
         "--repo-root", str(tiny_decisions), "--db", str(tmp_path / "cli" / "FPG.db"),
         "--staged", "docs/decisions/ADR-901-accepted-and-uncovered.md"],
        capture_output=True, text=True, timeout=300)
    assert out.returncode == 1, out.stdout + out.stderr
    assert "ADR-901" in out.stdout


# ------------------------------------------------------------- witness 4: the ERA BOUND


def test_a_PRE_ARM_decision_is_reported_but_never_refused(tiny_decisions: Path, tiny_store):
    """The lane's one design ruling, pinned so it cannot silently widen into a wedge.

    84 ADRs and 20 intakes carry an accepted status on the live tree today and none carries an
    `implements:` key, because the key did not exist. A refusal over all of them would refuse
    every commit in the repo on a defect the committer cannot repair -- the argument `audit.py`
    already settled when it kept `check_funnel_lifecycle` at SHIP rather than COMMIT tier.
    `consumer_at_landing.ARM_DATE` is the precedent and this is the same shape.
    """
    pre = _by_key(dc.decisions(tiny_decisions, tiny_store))["adr:905"]
    assert pre.state == dc.STATE_ACCEPTED, "it IS accepted-and-unexecuted"
    assert dc.decision_coverage(
        tiny_decisions, tiny_store,
        staged=["docs/decisions/ADR-905-grandfathered.md"]) == [], "and it does not refuse"


def test_the_grandfathered_set_is_COUNTED_not_hidden(tiny_decisions: Path, tiny_store):
    """A bound that is not measured is an exemption. The metric carries the debt the gate
    declines to refuse, which is the only thing that keeps the arm date honest."""
    m = dc.metrics(dc.decisions(tiny_decisions, tiny_store), today=_dt.date(2026, 9, 20))
    assert m.grandfathered == 1


def test_an_in_era_decision_refuses_even_when_it_is_not_staged(tiny_decisions: Path,
                                                               tiny_store):
    """The era leg. Without it the gate is satisfiable by never touching the file again."""
    findings = dc.decision_coverage(tiny_decisions, tiny_store, staged=[])
    assert findings == []
    findings = dc.decision_coverage(tiny_decisions, tiny_store, staged=[], era_leg=True)
    assert sorted(f.subject for f in findings) == ["ADR-901", "intake #900"]


# --------------------------------------------------------------- witness 5: the GRAPH half


def test_implements_runs_from_the_ROW_to_the_DECISION_on_FPG1(tiny_decisions: Path):
    """ADR-118 §1: a new edge kind is added to FPG-1, never computed by an organ. The edge is
    the ROW's -- a row depends on the decision existing, so the row is the consumer."""
    graph = fpg.build(tiny_decisions)
    edges = [e for e in graph.all_edges()
             if e.kind == fpg.EDGE_IMPLEMENTS and e.source == fpg.INPUT_DECISION_IMPLEMENTS]
    assert ("task:800", "adr:900") in {(e.src, e.dst) for e in edges}


def test_the_input_8_edge_carries_the_rows_status(tiny_decisions: Path):
    """`detail` is where the row's status rides, so the organ can tell `executing` from `done`
    with one SELECT instead of a second pass over `tasks/`."""
    graph = fpg.build(tiny_decisions)
    by_pair = {(e.src, e.dst): e.detail for e in graph.all_edges()
               if e.source == fpg.INPUT_DECISION_IMPLEMENTS}
    assert by_pair[("task:800", "adr:900")] == f"{fpg.DECISION_DETAIL_PREFIX}open"
    assert by_pair[("task:801", "adr:904")] == f"{fpg.DECISION_DETAIL_PREFIX}done"


def test_the_organ_reads_the_STORE_and_walks_no_tree_for_the_relation(tiny_decisions: Path,
                                                                      tiny_store, monkeypatch):
    """intake #86's acceptance criterion 5, applied here: the relation comes from the graph.
    If the organ recomputed it privately, emptying the store would not change its answer."""
    empty = _by_key(dc.decisions(tiny_decisions, _EmptyStore()))
    assert empty["adr:900"].state == dc.STATE_ACCEPTED, (
        "with no store edges the decision must read as UNIMPLEMENTED -- a private scan here "
        "would keep answering `executing` and defeat the thing the design proves")


class _EmptyStore:
    """A store that holds nothing. Not a mock of the interface -- the two methods the organ
    is allowed to use, answering empty."""

    def in_edges(self, key, kinds=None):
        del key, kinds
        return []

    def node(self, key):
        del key
        return None


# ------------------------------------------- witness 6: the `implements:` frontmatter key


def test_implements_is_derived_from_the_row_body_so_frontmatter_stays_honest(tmp_path: Path):
    """`gen_task_tree`'s leg-2 contract: every frontmatter key is a pure function of the body,
    so a hand-edited one cannot sit in a source-of-truth file meaning nothing."""
    import gen_task_tree as gtt  # noqa: PLC0415
    raw = ("- [#900] [P1][S] **a row** - prose · implements: ADR-118, intake-91 · "
           "Done when: it holds · refs none")
    assert gtt.derive_implements(raw) == "ADR-118, intake-91"
    assert gtt.derive_implements("- [#901] [P1][S] **no key** - prose · Done when: x") is None


@pytest.mark.parametrize("token", ["ADR-118", "intake-91", "DECLARE-GRAPH-2026-09-07",
                                   "AMEND-SESSION-PLAN-009"])
def test_the_grammar_admits_every_form_clause_2_names(token):
    assert vb._IMPLEMENTS_TOKEN_RE.fullmatch(token), token


@pytest.mark.parametrize("token", ["ADR118", "adr-118", "#91", "intake 91", "GRAPH-2026"])
def test_the_grammar_REFUSES_a_malformed_token(token):
    assert not vb._IMPLEMENTS_TOKEN_RE.fullmatch(token), token


def test_a_malformed_implements_token_is_a_HARD_fail():
    tasks = [{"id": "900", "line": 1,
              "rest": "[P1][S] **a row** · implements: adr-118 · Done when: x",
              "raw": "- [#900] [P1][S] **a row** · implements: adr-118 · Done when: x",
              "story": None, "theme": None}]
    hard = vb._check_implements_grammar(tasks)
    assert hard and "adr-118" in hard[0]


def test_an_implements_token_naming_an_ADR_that_does_not_exist_is_a_HARD_fail(
        tiny_decisions: Path):
    tasks = [{"id": "900", "line": 1,
              "rest": "[P1][S] **a row** · implements: ADR-999 · Done when: x",
              "raw": "- [#900] [P1][S] **a row** · implements: ADR-999 · Done when: x",
              "story": None, "theme": None}]
    hard = vb._check_implements_references(tasks, repo_root=tiny_decisions)
    assert hard and "ADR-999" in hard[0]


def test_a_transport_token_is_grammar_checked_only_and_says_so(tiny_decisions: Path):
    """The transport is a MACHINE-level surface, not a repo one, so in-repo reference
    resolution is not available for it. Stated rather than silently skipped."""
    tasks = [{"id": "900", "line": 1,
              "rest": "[P1][S] **a row** · implements: AMEND-NOT-ON-THIS-DISK-001 · Done when: x",
              "raw": "- [#900] · implements: AMEND-NOT-ON-THIS-DISK-001 · Done when: x",
              "story": None, "theme": None}]
    assert vb._check_implements_references(tasks, repo_root=tiny_decisions) == []


# ------------------------------------------------- witness 7: A9-2's ledger, A9-3's numbers


def test_the_ledger_lists_every_OPEN_decision_with_its_state(tiny_decisions: Path, tiny_store):
    """A9-2: *"The bundle generator emits, from `decision_coverage`, every open decision with
    its state."* Open = not yet out of the lifecycle, so `done` and `superseded` leave."""
    text = dc.render_ledger(dc.decisions(tiny_decisions, tiny_store))
    assert "ADR-901" in text and dc.STATE_ACCEPTED in text
    assert "ADR-900" in text and dc.STATE_EXECUTING in text
    assert "ADR-903" not in text, "a superseded decision has left the lifecycle"
    assert "ADR-904" not in text, "a done decision has left the lifecycle"


def test_the_ledger_is_FLAT_no_padded_table(tiny_decisions: Path, tiny_store):
    """CLAUDE.md output-formatting: the bundle is read into a browser window and a padded
    markdown table costs ~3x its content for a border the client draws anyway."""
    text = dc.render_ledger(dc.decisions(tiny_decisions, tiny_store))
    assert "|" not in text
    assert "  " not in text.replace("\n", "")


def test_metrics_report_A9_3s_four_numbers(tiny_decisions: Path, tiny_store):
    """*"decisions accepted, executing, done, and age of the oldest accepted-but-unexecuted
    decision."*"""
    m = dc.metrics(dc.decisions(tiny_decisions, tiny_store), today=_dt.date(2026, 9, 20))
    assert (m.accepted, m.executing, m.done) == (3, 1, 1)
    assert m.oldest_unexecuted_days == (_dt.date(2026, 9, 20)
                                        - _dt.date(2026, 1, 5)).days


def test_the_metric_line_renders_the_four_numbers_and_nothing_else(tiny_decisions: Path,
                                                                   tiny_store):
    line = dc.metrics(dc.decisions(tiny_decisions, tiny_store),
                      today=_dt.date(2026, 9, 20)).render()
    assert line.startswith("[decisions]")
    for part in ("accepted", "executing", "done", "oldest"):
        assert part in line


def test_the_oldest_age_is_None_when_nothing_is_unexecuted(tiny_decisions: Path, tiny_store):
    """An honest absence, never a 0 that reads as "nothing is old"."""
    covered = [d for d in dc.decisions(tiny_decisions, tiny_store)
               if d.state != dc.STATE_ACCEPTED]
    assert dc.metrics(covered, today=_dt.date(2026, 9, 20)).oldest_unexecuted_days is None


# --------------------------------------------------- witness 8: the ONBOARDING refusal


def test_the_onboarding_rung_FAILS_on_an_in_era_undisposed_decision(tiny_decisions: Path,
                                                                    tiny_store):
    """A9-2: *"the incoming seat's plan must dispose each one ... before its plan is accepted
    -- a probe, not prose."* `accepted` IS the undisposed state: executing-in-batch-N and
    scheduled-with-a-row both read as `executing`, and refused-in-writing is a disposition."""
    results = dc.onboarding_findings(dc.decisions(tiny_decisions, tiny_store))
    assert results and all(r.status == "fail" for r in results)
    assert "ADR-901" in results[0].detail


def test_the_onboarding_rung_PASSES_when_every_in_era_decision_is_disposed(
        tiny_decisions: Path, tiny_store):
    register = {"adr:901": dc.Disposition("no implementation required", "the architect"),
                "intake:900": dc.Disposition("no implementation required", "the architect")}
    found = dc.decisions(tiny_decisions, tiny_store, dispositions=register)
    assert dc.onboarding_findings(found) == []


# ------------------------------------------------------------- the live tree, measured
#
# ONE STORE AND ONE TRANSPORT READ FOR THE WHOLE GROUP. `gs.ensure` pays an mtime sweep and, on
# a stale store, a full rebuild (~15 s on this tree); four witnesses each calling it turned a
# fast file into a three-minute one. Session scope is correct rather than merely cheap: these
# witnesses all measure the SAME tree at the same moment, so re-reading it between them would
# not make any of them stricter.


@contextlib.contextmanager
def _live_store():
    """The live store, open for exactly as long as a read takes.

    NEVER held across tests, and the reason is measured rather than stylistic. `gs.ensure`
    rebuilds by swapping a new file into place; on Windows that swap FAILS while any process
    holds the `-wal` open, and it then raises `StoreUnreadable`. A session-scoped handle is
    such a reader for the length of the run, so under xdist it makes a SIBLING worker's
    rebuild fail -- six `tests/test_graph_spine.py` tests went red on this branch and not on a
    worktree of `main`, which is how this was found. A test file that reds other people's tests
    by existing is a defect in the test file.
    """
    store = gs.ensure(REPO_ROOT)
    try:
        yield store
    finally:
        store.close()


@pytest.fixture
def live_store():
    """Function-scoped ON PURPOSE -- see `_live_store`. The one-open-per-test cost is ~1s and
    buys back a suite that does not fight itself."""
    with _live_store() as store:
        yield store


@pytest.fixture(scope="session")
def live_transport():
    """The operator's transport, or None. A suite result must not depend on what happens to be
    sitting in the operator's own prompts directory, so every witness below states which case
    it is in -- `verify_handoff_probes._unnamed_open_carriers` records the same hazard, having
    measured a unit test being judged against the live transport."""
    return dc._transport_root()


@pytest.fixture(scope="session")
def live_decisions(live_transport):
    """The POPULATION, computed once and carried -- not the handle that produced it. Session
    scope is still correct for the same reason it always was (every witness measures the same
    tree at the same moment), and it no longer implies a session-long reader."""
    with _live_store() as store:
        return dc.decisions(REPO_ROOT, store, transport=live_transport)


def test_the_live_population_is_readable_and_non_empty(live_decisions):
    """A population this organ cannot read is the one failure it must never render as clean."""
    assert len(live_decisions) > 100, len(live_decisions)
    assert any(d.state == dc.STATE_ACCEPTED for d in live_decisions)


#: LANE-5B3-4-decision-debt's own RESIDUAL-CARRIERS finding: 11 in-era transport decisions
#: measured live at the lane's close with NEITHER a ratification/triage/batch grounding NOR
#: a landed carrier -- named individually (Done-contract item 4's own anticipated shape: "any
#: decision STILL failing P13 must be individually named with its reason") rather than forced
#: to a paper disposition the lane's own Do-not clause forbids ("never write a disposition ...
#: never invent one"). Filed as `ROWS-OWED` in the lane's session file, each with a runnable
#: check. This is a NAMED, CITED residual, not a blanket suppression: any subject outside this
#: set still fails the test below.
#:
#: EMPTIED 2026-10-02 (R53, at the 2026-10-02 handoff cut). All 16 subjects once named here
#: are now covered: the R26 rows `[#1104]`-`[#1122]` (filed 2026-09-28) implement them, and the
#: live population reports each one as `executing` with an OPEN row. The shrink was owed from
#: 2026-09-28. It stayed hidden because this test's earlier `unexpected` leg was already
#: failing on undisposed 2026-09-29 amendments. The empty set means any in-era uncovered
#: decision fails the test below.
_LANE_5B3_4_RESIDUAL_SUBJECTS: frozenset = frozenset()


def test_the_live_tree_carries_no_IN_ERA_uncovered_decision(live_store, live_transport):
    """The bar this lane must leave green: nothing accepted on or after `ARM_DATE` may sit
    without a row or a disposition when the lane ends -- OTHER than the 16 named residuals
    LANE-5B3-4-decision-debt filed as `ROWS-OWED` (measured population: 40 undisposed at the
    lane's start, 24 disposed, 16 residual -- 11 at first disposition, plus QUEUE2/QUEUE3 on
    Codex terra review round 2, plus QUEUE/QUEUE4/QUEUE6 on round 3 once THEIR own
    individually-reasoned WAVE5B-N2 dispositions were found to still overclaim a settled file).
    A subject not in that named set still fails this test; the named 16 do not silently vanish
    -- they are asserted present, so the day one
    lands a real disposition or a row, this set (and the session file's `ROWS-OWED`) must
    shrink to match or this test starts failing for the opposite reason."""
    findings = dc.decision_coverage(REPO_ROOT, live_store, staged=[], era_leg=True,
                                    transport=live_transport)
    subjects = {f.subject for f in findings}
    unexpected = [f for f in findings if f.subject not in _LANE_5B3_4_RESIDUAL_SUBJECTS]
    assert unexpected == [], "; ".join(f"{f.subject}: {f.evidence}" for f in unexpected)
    missing = _LANE_5B3_4_RESIDUAL_SUBJECTS - subjects
    assert not missing, (
        f"named residual(s) no longer found -- disposed? shrink _LANE_5B3_4_RESIDUAL_SUBJECTS "
        f"and the session file's ROWS-OWED to match: {sorted(missing)}")


def test_every_live_disposition_carries_a_reason_and_an_owner():
    """ADR-75's decoration rule, as `graph_queries` applies it: a register allowed to hold a
    bare 'exempt' rots into paper suppressions."""
    for key, disp in dc.DECISION_DISPOSITIONS.items():
        assert disp.reason.strip(), key
        assert disp.owner.strip(), key


def test_no_disposition_names_a_decision_that_is_gone(live_decisions, live_transport):
    if live_transport is None:
        pytest.skip("transport unresolved -- the transport class was not measured, so a "
                    "transport disposition cannot be judged stale (DEFECT E-29)")
    assert dc.stale_dispositions(live_decisions) == []


def test_a_disposition_for_an_UNMEASURED_class_is_not_reported_stale(live_store):
    """The guard the live witness above found. Measured with no transport, every transport
    disposition names a decision that was never read -- 'absent' and 'not measured' are
    different facts, and a register that self-reports as rotten is a register nobody reads."""
    in_repo_only = dc.decisions(REPO_ROOT, live_store, transport=None)
    assert not any(d.kind == dc.KIND_TRANSPORT for d in in_repo_only)
    assert dc.stale_dispositions(in_repo_only) == []


# ---------------------------------------------------------------- step 4: the three consumers
#
# The organ's own answers are witnessed above. THIS group witnesses only the WIRING -- that the
# handoff bundle emits the ledger (A9-2), that onboarding refuses on it (A9-2's probe half), and
# that `fleet_health` reports A9-3's numbers -- because a built organ nothing calls is the exact
# shape of the defect `test_live_repo_builds_and_carries_all_five_inputs` exists to catch one
# level down: a key in the roster, looking armed, contributing nothing.


@pytest.fixture
def wired_population(tiny_decisions: Path, tiny_store):
    return dc.decisions(tiny_decisions, tiny_store, transport=None)


def _bundle(tmp_path: Path, name: str) -> Path:
    """A bundle directory with the one file the rungs use to recognise a v5-lineage bundle."""
    b = tmp_path / "handoffs" / name
    b.mkdir(parents=True)
    (b / "RESIDUAL.md").write_text("# RESIDUAL\n", encoding="utf-8", newline="\n")
    return b


# --- A9-2, the artifact half: the bundle emits the ledger ------------------------------------

def test_the_handoff_writer_emits_the_ledger_into_the_bundle(tmp_path: Path, wired_population,
                                                             monkeypatch):
    """A9-2: *"The bundle generator emits, from `decision_coverage`, every open decision with
    its state."* The generator, not a seat typing a list."""
    import gen_handoff as gh

    monkeypatch.setattr(dc, "live_decisions", lambda *a, **k: wired_population)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    out = gh._write_decision_ledger(bundle, REPO_ROOT)

    assert out == bundle / dc.LEDGER_FILE
    assert out.exists()
    body = out.read_text(encoding="utf-8")
    assert body.startswith(dc.LEDGER_BEGIN)
    assert body.rstrip().endswith(dc.LEDGER_END)
    # the population, not a header: ADR-901 is accepted-and-uncovered in the fixture
    assert "ADR-901" in body
    assert dc.LEDGER_UNAVAILABLE not in body


def test_an_unreadable_population_writes_the_ledger_ANYWAY_saying_so(tmp_path: Path,
                                                                     monkeypatch):
    """DEGRADED, NEVER ABSENT. A missing DECISION_LEDGER.md reads to the incoming seat as
    'no open decisions' -- the one answer this file must never give (DEFECT E-29)."""
    import gen_handoff as gh

    def _boom(*_a, **_k):
        raise gs.StoreUnreadable("fixture: the store cannot be opened")

    monkeypatch.setattr(dc, "live_decisions", _boom)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    out = gh._write_decision_ledger(bundle, REPO_ROOT)

    assert out is not None and out.exists(), "a boundary must not delete the artifact"
    body = out.read_text(encoding="utf-8")
    assert dc.LEDGER_UNAVAILABLE in body
    assert "StoreUnreadable" in body, "the reason is stated, not swallowed"
    assert body.startswith(dc.LEDGER_BEGIN) and body.rstrip().endswith(dc.LEDGER_END)


def test_the_writer_touches_NO_tree_that_is_not_the_hub(tmp_path: Path, monkeypatch):
    """Found by tests/test_gen_handoff.py, not by review. Resolving the population calls
    `graph_store.ensure`, which creates `<repo>/.git/fpg-graph/FPG.db` -- and in a tree with no
    git history that MATERIALISES a `.git` directory, which made six regeneration tests raise
    BundleCollisionError. A surfacing artifact may degrade and may be slow; it may not change
    the tree it is reporting on. `_is_hub` is the predicate already ruled for this scoping."""
    import gen_handoff as gh

    def _never(*_a, **_k):
        raise AssertionError("a non-hub tree must not reach the population at all")

    monkeypatch.setattr(dc, "live_decisions", _never)
    foreign = tmp_path / "some-consumer-repo"
    bundle = foreign / "docs" / "handoffs" / "2026-09-12-consumer-architect"
    bundle.mkdir(parents=True)

    assert gh._write_decision_ledger(bundle, foreign) is None
    assert not (bundle / dc.LEDGER_FILE).exists()
    assert not (foreign / ".git").exists(), "no store, and above all no .git, is created"


def test_the_ledger_is_a_BUNDLE_artifact_not_a_browser_visible_one():
    """The answer-free invariant governs BOOT / RESIDUAL / PROBES and the assembled paste. The
    ledger carries counts, so it may not enter that set -- it rides beside FUNNEL_HEALTH.md,
    which is in the bundle and absent from the assembler, and this pins the same for it.

    HONEST LIMIT: this proves the assembler never reads the file BY NAME, which is how it reads
    every source it has. It is not a proof about a directory walk the assembler does not do."""
    assembler = (REPO_ROOT / "scripts" / "assemble_paste.py").read_text(encoding="utf-8")
    assert "FUNNEL_HEALTH.md" not in assembler, "the precedent this rides on moved"
    assert dc.LEDGER_FILE not in assembler


# --- A9-2, the probe half: onboarding refuses -------------------------------------------------

def test_the_onboarding_era_is_pinned_to_the_organs_own_ARM_DATE():
    """Two spellings of one date. Pinned equal so the rung and the refusals it reports cannot
    come to different conclusions about the same decision."""
    import verify_handoff_probes as vhp

    assert vhp._DECISION_ERA == dc.ARM_DATE.isoformat()


def test_a_PRE_ERA_bundle_is_not_judged(tmp_path: Path, monkeypatch):
    """The bound that keeps 'any FAIL blocks onboarding' from blocking every handoff on the
    decisions that predate the `implements:` key."""
    import verify_handoff_probes as vhp

    def _never(*_a, **_k):
        raise AssertionError("a pre-era bundle must not reach the population at all")

    monkeypatch.setattr(dc, "live_decisions", _never)
    assert vhp._undisposed_decisions(_bundle(tmp_path, "2026-09-10-dev-knowledge-architect"),
                                     REPO_ROOT) == []


def test_the_onboarding_rung_carries_the_organs_verdict_into_the_probe_list(tmp_path: Path,
                                                                            wired_population,
                                                                            monkeypatch):
    """The rung owns WHEN the question is asked; `decision_coverage` owns the answer and its
    wording. A second judgement written here would be free to disagree with the gate."""
    import verify_handoff_probes as vhp

    monkeypatch.setattr(dc, "live_decisions", lambda *a, **k: wired_population)
    monkeypatch.setattr(vhp, "_residual_is_sealed_and_unchanged", lambda *a, **k: False)
    bundle = _bundle(tmp_path, "2026-09-12-dev-knowledge-architect")

    rows = vhp._undisposed_decisions(bundle, REPO_ROOT)

    assert len(rows) == 1, rows
    row = rows[0]
    assert row.probe_id == dc.ONBOARDING_PROBE_ID
    assert row.status == "fail"
    assert row.bundle == bundle.name
    assert "ADR-901" in row.detail and "intake #900" in row.detail
    assert "|" not in row.detail, "ProbeResult detail is pipe-free -- it lands in a table"


def test_a_SEALED_bundle_is_not_judged_and_never_pays_for_the_population(tmp_path: Path,
                                                                         monkeypatch):
    """`check_handoff_probes` is COMMIT tier. Unbounded, this rung would fail every later
    commit in the repo on a bundle nobody may repair -- and pay ~25s for the privilege."""
    import verify_handoff_probes as vhp

    def _never(*_a, **_k):
        raise AssertionError("a sealed bundle must not resolve the population")

    monkeypatch.setattr(dc, "live_decisions", _never)
    monkeypatch.setattr(vhp, "_residual_is_sealed_and_unchanged", lambda *a, **k: True)
    assert vhp._undisposed_decisions(_bundle(tmp_path, "2026-09-12-dev-knowledge-architect"),
                                     REPO_ROOT) == []


def test_an_unreadable_population_DEGRADES_the_rung_it_does_not_vanish(tmp_path: Path,
                                                                       monkeypatch):
    """A rung that disappears when it cannot measure reads as a pass to every consumer of the
    probe list. `skipped` is this validator's own word for 'measured nothing, honestly'."""
    import verify_handoff_probes as vhp

    def _boom(*_a, **_k):
        raise gs.StoreUnreadable("fixture: the store cannot be opened")

    monkeypatch.setattr(dc, "live_decisions", _boom)
    monkeypatch.setattr(vhp, "_residual_is_sealed_and_unchanged", lambda *a, **k: False)

    rows = vhp._undisposed_decisions(_bundle(tmp_path, "2026-09-12-dev-knowledge-architect"),
                                     REPO_ROOT)

    assert len(rows) == 1 and rows[0].status == "skipped", rows
    assert "StoreUnreadable" in rows[0].detail


# --- A9-3: fleet_health reports the four numbers ----------------------------------------------

def test_fleet_health_renders_the_decision_metric(wired_population, monkeypatch):
    """A9-3, wired: *"Decision metric (reported by `fleet_health`)"*."""
    import fleet_health as fh

    monkeypatch.setattr(dc, "store_is_stale", lambda *a, **k: False)
    monkeypatch.setattr(dc, "live_decisions", lambda *a, **k: wired_population)

    line = fh.decision_health_line(REPO_ROOT)

    assert line is not None
    assert line.startswith("[decisions] accepted ")
    for word in ("accepted", "executing", "done", "oldest unexecuted", "grandfathered"):
        assert word in line, word
    assert "|" not in line, "a digest line is flat"


def test_the_narrowed_reading_SAYS_it_is_narrowed(wired_population, monkeypatch):
    """`executing` and `done` are carried almost entirely by the transport class, so an
    unlabelled session-start line would report two clean-looking zeros that are false as
    statements about the repo."""
    import fleet_health as fh

    monkeypatch.setattr(dc, "store_is_stale", lambda *a, **k: False)
    monkeypatch.setattr(dc, "live_decisions", lambda *a, **k: wired_population)
    assert "in-repo classes only" in fh.decision_health_line(REPO_ROOT)

    full = dc.metrics(wired_population).render()
    assert "in-repo classes only" not in full, "the whole population is not labelled narrowed"


def test_a_STALE_store_is_reported_never_rebuilt_at_session_start(monkeypatch):
    """Measured: a cold rebuild is ~16s against ~1.5s warm. The rebuild belongs to the
    `graph-rebuild` pre-commit hook ([#664] clause 1), not to a digest line -- but 'not
    measured' and 'nothing to report' are different facts."""
    import fleet_health as fh

    def _never(*_a, **_k):
        raise AssertionError("a stale store must not be rebuilt by the digest")

    monkeypatch.setattr(dc, "store_is_stale", lambda *a, **k: True)
    monkeypatch.setattr(dc, "live_decisions", _never)

    line = fh.decision_health_line(REPO_ROOT)

    assert line is not None, "silence would read as 'nothing to report'"
    assert "not measured" in line and "stale" in line


def test_the_digest_line_is_dropped_rather_than_faked_when_the_population_is_unreadable(
        monkeypatch):
    """`funnel_health_line`'s posture directly above it: None, never a spurious line."""
    import fleet_health as fh

    def _boom(*_a, **_k):
        raise gs.StoreUnreadable("fixture: the store cannot be opened")

    monkeypatch.setattr(dc, "store_is_stale", lambda *a, **k: False)
    monkeypatch.setattr(dc, "live_decisions", _boom)
    assert fh.decision_health_line(REPO_ROOT) is None


def test_live_decisions_resolves_the_population_ONE_way_for_all_three_consumers(live_store):
    """The point of the shared resolver: a consumer that reads the population its own way is
    free to disagree with the organ that REFUSES on it."""
    direct = dc.decisions(REPO_ROOT, live_store, transport=None)
    shared = dc.live_decisions(REPO_ROOT, transport=None)
    assert [d.key for d in shared] == [d.key for d in direct]
    assert [d.state for d in shared] == [d.state for d in direct]


# ======================================================================================
# THE RULING REGISTER LEG -- [#721] and R79.3 (batch B2-W1, lane W1-10 `b2-rulings-landing`)
# ======================================================================================
#
# RED-first at origin/main e67f27ac: none of `parse_register`, `uncarried_rulings`,
# `unlanded_rulings`, `rulings_report` or the `rulings` subcommand exists there, so every test in
# this group fails on that tree and passes on the one that adds the leg.
#
# WHAT EACH GROUP WITNESSES:
#   1. LANDED RULING, NO ROW, NO DISPOSITION -> refused BY NAME ([#721]'s own RED), the CLI exits
#      non-zero, and the fully carried fixture exits 0 (the negative case).
#   2. WHAT COUNTS AS CARRIED -- a row that exists, whose status carries, that names the ruling and
#      has a Done-when; or a written "no implementation required" that names a reason AND an owner.
#   3. THE ERA BOUND -- entries below the floor are COUNTED, not refused; the floor is a parameter,
#      so [#721]'s section-AH witness (an un-mechanized older entry) is refused when it is armed.
#   4. UNLANDED FOR MORE THAN ONE BATCH -- the batch clock is the transport's STATE-BATCH files.
#   5. N7's HAZARDS (a)-(d) -- fixtures that must NOT refuse (and (d), one that must).
#   6. THE TRANSPORT BOUNDARY -- unreadable is reported n/a, never a pass.


def _entry(number: int, carried: str | None, title: str = "fixture ruling") -> str:
    out = f"- **R{number} — {title}** (operator, 2026-10-04; full text `RATIFICATION-X.md:1`).\n\n"
    if carried is not None:
        out += f"  **Carried by:** {carried}\n\n"
    return out


def _register(root: Path, *entries: str) -> None:
    _write(root / "protocols" / "STANDING_RULINGS.md",
           "# Standing rulings\n\n## AR. fixture section\n\n" + "".join(entries)
           + "## Editing note\n\nprose\n")


def _ruling_row(root: Path, task_id: int, status: str, cites: str | None,
                done_when: bool = True, owner: "bool | str" = True) -> None:
    body = f"carries {cites}. " if cites else "carries nothing in particular. "
    _write(root / "tasks" / f"{task_id}-fixture.md",
           "\n".join(["---", f'id: "[#{task_id}]"', f'title: "fixture row {task_id}"',
                      f"status: {status}", "generates: BACKLOG.md", "---", "",
                      f"- [#{task_id}] [P2][M] **fixture row {task_id}** - {body}"
                      + ("· Done when: the fixture holds " if done_when else "")
                      + (f"· owner: {'the fixture lane' if owner is True else owner} "
                         if owner else "")
                      + "· refs none", ""]))


NO_IMPL = "no implementation required — procedural, nothing to build (owner: the browser seat)"


def _names(findings) -> list[str]:
    return [f.subject for f in findings]


def test_a_landed_ruling_with_no_row_and_no_disposition_is_REFUSED_by_name(tmp_path: Path):
    """[#721]'s Done-when, verbatim in shape: a register entry with neither an implementing row
    nor a written 'no implementation required' disposition is NAMED by the refusal."""
    root = tmp_path / "r"
    _register(root, _entry(70, None), _entry(71, "[#1500]"))
    _ruling_row(root, 1500, "open", "R71")
    findings = dc.uncarried_rulings(root)
    assert _names(findings) == ["R70"]
    assert "Carried by" in findings[0].evidence and "no implementation required" in findings[0].evidence


def test_the_rulings_cli_exits_non_zero_on_an_uncarried_ruling(tmp_path: Path, capsys):
    root = tmp_path / "r"
    _register(root, _entry(70, None))
    assert dc.main(["rulings", "--repo-root", str(root), "--no-transport"]) == 1
    out = capsys.readouterr().out
    assert "REFUSED" in out and "R70" in out


def test_the_rulings_cli_is_a_real_subprocess_exit(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, None))
    out = subprocess.run(
        [sys.executable, str(_SCRIPTS / "decision_coverage.py"), "rulings",
         "--repo-root", str(root), "--no-transport"],
        capture_output=True, text=True, timeout=120)
    assert out.returncode == 1, out.stdout + out.stderr
    assert "R70" in out.stdout


def test_a_fully_carried_register_exits_zero(tmp_path: Path, capsys):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"), _entry(71, NO_IMPL))
    _ruling_row(root, 1500, "open", "R70")
    assert dc.main(["rulings", "--repo-root", str(root), "--no-transport"]) == 0
    assert "OK" in capsys.readouterr().out


@pytest.mark.parametrize("status,carries", [("open", True), ("closed", True), ("deferred", True),
                                            ("retired", False), ("superseded", False)])
def test_only_a_row_whose_status_carries_counts(tmp_path: Path, status: str, carries: bool):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, status, "R70")
    assert (dc.uncarried_rulings(root) == []) is carries


def test_a_named_row_that_does_not_exist_is_refused(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1599]"))
    (root / "tasks").mkdir()
    got = dc.uncarried_rulings(root)
    assert _names(got) == ["R70"] and "1599" in got[0].evidence


def test_a_row_that_never_names_the_ruling_does_not_carry_it(tmp_path: Path):
    """The back-reference: an entry pointing at an unrelated row (a typo, a copy-paste) must not
    read as carried -- the link is checked from BOTH ends."""
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, "open", "R700")        # R700 is not R70
    assert _names(dc.uncarried_rulings(root)) == ["R70"]


def test_a_row_with_no_done_when_does_not_carry(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, "open", "R70", done_when=False)
    assert _names(dc.uncarried_rulings(root)) == ["R70"]


def test_a_row_with_no_owner_does_not_carry(tmp_path: Path):
    """Codex P1 (b2-rulings-landing review): the contract asks every carrying row for an owner
    (wave or lane); a row with a Done-when and no owner left the ruling nobody's."""
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, "open", "R70", owner=False)
    got = dc.uncarried_rulings(root)
    assert _names(got) == ["R70"] and "owner" in got[0].evidence


@pytest.mark.parametrize("placeholder", ["none", "None.", "tbd", "TBD", "n/a", "nobody", "unknown", "-"])
def test_an_owner_placeholder_is_not_an_owner(tmp_path: Path, placeholder: str):
    """Codex pass 2: any text after `owner:` was accepted. A placeholder names nobody."""
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, "open", "R70", owner=placeholder)
    got = dc.uncarried_rulings(root)
    assert _names(got) == ["R70"] and "owner" in got[0].evidence


@pytest.mark.parametrize("text", [
    "no implementation required",                                # no reason, no owner
    "no implementation required — nothing to build",             # reason, no owner
    "no implementation required — (owner: someone)",             # owner, no reason
])
def test_a_disposition_needs_a_reason_AND_an_owner(tmp_path: Path, text: str):
    root = tmp_path / "r"
    _register(root, _entry(70, text))
    assert _names(dc.uncarried_rulings(root)) == ["R70"]


def test_one_row_may_carry_several_rulings(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"), _entry(71, "[#1500]"))
    _ruling_row(root, 1500, "open", "R70 and R71")
    assert dc.uncarried_rulings(root) == []


# --- the era bound ------------------------------------------------------------------------


def test_entries_below_the_floor_are_counted_not_refused(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(54, None), _entry(55, "[#1500]"))
    _ruling_row(root, 1500, "open", "R55")
    assert dc.FIRST_GATED_RULING == 55
    assert dc.uncarried_rulings(root) == []
    counts = dc.register_counts(root)
    assert counts.grandfathered == 1 and counts.carried == 1 and counts.gated == 1


def test_armed_over_the_whole_register_the_refusal_names_the_old_entry(tmp_path: Path):
    """[#721]'s witness is section AH's un-mechanized entries: the floor is a parameter so the
    same predicate refuses them the day someone arms it over the older sections."""
    root = tmp_path / "r"
    _register(root, _entry(54, None))
    assert _names(dc.uncarried_rulings(root, floor=1)) == ["R54"]


def test_the_landed_id_grammar_is_the_bundles_own():
    """`handoff_state._LANDED_RE` is how the bundle's Landed row counts ruling ids. The gate
    reads the register with the SAME shape, or the two could disagree about what is landed."""
    import handoff_state as hs
    assert dc._LANDED_RE.pattern == hs._LANDED_RE.pattern


def test_fenced_text_inside_an_entry_is_never_an_entry(tmp_path: Path):
    root = tmp_path / "r"
    fenced = ("- **R70 — real** (operator, 2026-10-04).\n\n  **Carried by:** [#1500]\n\n"
              "  ```verbatim to-browser/X.md:1-3\n  - **R71 — quoted, not an entry**\n"
              "  **Carried by:** [#9999]\n  ```\n\n")
    _register(root, fenced)
    _ruling_row(root, 1500, "open", "R70")
    assert [e.number for e in dc.parse_register((root / "protocols/STANDING_RULINGS.md")
                                                .read_text(encoding="utf-8"))] == [70]
    assert dc.uncarried_rulings(root) == []


# --- unlanded for more than one batch ------------------------------------------------------


def _transport(tmp_path: Path, ratifications: dict[str, str], batches: dict[str, str]) -> Path:
    root = tmp_path / "t"
    for name, text in ratifications.items():
        _write(root / "to-browser" / name, text)
    for name, text in batches.items():
        _write(root / "to-browser" / name, text)
    (root / "to-cc").mkdir(parents=True, exist_ok=True)
    return root


def _ratification(date: str, *rulings: str, carried: str = "OPEN") -> str:
    return (f"carried-by: {carried}\nlands-via: x\ndate: {date}\nversion: v1\nkind: RATIFICATION\n\n"
            "# RATIFICATION\n\n" + "".join(f"## {r} — a ruling\n\ntext\n\n" for r in rulings))


CLOSED = "CLOSED {day}T08:00Z -- fixture\n"


def test_an_unlanded_ruling_older_than_one_closed_batch_is_REFUSED(tmp_path: Path):
    """The RED the AMEND names: a fixture RATIFICATION holding an unlanded ruling, two closed
    batches after its date -> refused, and the CLI exits non-zero."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
         "STATE-BATCH-TWO.md": CLOSED.format(day="2026-09-09")})
    got = dc.unlanded_rulings(root, transport)
    assert _names(got) == ["R99"]
    assert "RATIFICATION-2026-09-01.md" in got[0].evidence and "2 closed batch" in got[0].evidence


def test_the_unlanded_cli_exits_non_zero_and_the_landed_one_exits_zero(tmp_path: Path,
                                                                       monkeypatch, capsys):
    root = tmp_path / "r"
    _register(root, _entry(99, NO_IMPL))
    batches = {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
               "STATE-BATCH-TWO.md": CLOSED.format(day="2026-09-09")}
    bad = _transport(tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R98")},
                     batches)
    monkeypatch.setattr(dc, "_transport_root", lambda: bad)
    assert dc.main(["rulings", "--repo-root", str(root)]) == 1
    assert "R98" in capsys.readouterr().out
    good = _transport(tmp_path / "good",
                      {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")}, batches)
    monkeypatch.setattr(dc, "_transport_root", lambda: good)
    assert dc.main(["rulings", "--repo-root", str(root)]) == 0
    assert "OK" in capsys.readouterr().out


def test_one_closed_batch_is_the_grace_period_not_a_refusal(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
         "STATE-BATCH-OLD.md": CLOSED.format(day="2026-08-01")})   # closed BEFORE the ruling
    assert dc.unlanded_rulings(root, transport) == []


def test_a_batch_that_is_not_closed_does_not_age_a_ruling(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
         "STATE-BATCH-TWO.md": "RUNNING since 2026-09-06\n",
         "STATE-BATCH-THREE.md": "FINISHED 2026-09-07T01:00Z\n"})
    assert dc.unlanded_rulings(root, transport) == []


# --- N7's hazards --------------------------------------------------------------------------


_TWO_CLOSED = {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
               "STATE-BATCH-TWO.md": CLOSED.format(day="2026-09-09")}


def test_hazard_a_an_id_that_restarts_in_another_file_is_not_a_false_refusal(tmp_path: Path):
    """R-ids are not globally unique (`RATIFICATION-2026-09-25.md` restarts at R1 in the live
    transport): the same id in two files, landed once, must not refuse either of them."""
    root = tmp_path / "r"
    _register(root, _entry(1, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R1"),
                   "RATIFICATION-2026-09-02.md": "carried-by: OPEN\ndate: 2026-09-02\n\n"
                                                 "- **R1** backlog O1.\n"}, _TWO_CLOSED)
    assert dc.unlanded_rulings(root, transport) == []


def test_hazard_b_a_landed_ruling_in_a_file_still_reading_OPEN_is_not_unlanded(tmp_path: Path):
    """Seven older non-superseded files still read `carried-by: OPEN` and their rulings ARE
    landed. Carriage is not the landed test; the register's content is."""
    root = tmp_path / "r"
    _register(root, _entry(99, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99", carried="OPEN")},
        _TWO_CLOSED)
    assert dc.unlanded_rulings(root, transport) == []


def test_hazard_c_files_with_no_ruling_ids_contribute_nothing(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": "date: 2026-09-01\n\none line per item: O-1, B-2\n",
                   "RATIFICATION-DIGEST-2026-09-06.md": "## R999 — a digest, not a ruling file\n"},
        _TWO_CLOSED)
    assert dc.unlanded_rulings(root, transport) == []


@pytest.mark.parametrize("name", ["RATIFICATION-2026-09-01-v3-superseded.md",
                                  "RATIFICATION-2026-09-01-v6-withdrawn.md"])
def test_a_superseded_or_withdrawn_file_is_not_a_non_superseded_file(tmp_path: Path, name: str):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(tmp_path, {name: _ratification("2026-09-01", "R99")}, _TWO_CLOSED)
    assert dc.unlanded_rulings(root, transport) == []


def test_hazard_d_a_carried_by_naming_the_register_does_not_land_a_ruling(tmp_path: Path):
    """P11 proves a HOME exists, not that the ruling is in it. A file whose carried-by names
    `protocols/STANDING_RULINGS.md` resolves under P11 and its ruling is still not landed."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification(
            "2026-09-01", "R99", carried="protocols/STANDING_RULINGS.md")}, _TWO_CLOSED)
    assert _names(dc.unlanded_rulings(root, transport)) == ["R99"]


def test_an_undated_unlanded_ruling_is_REFUSED_not_forgotten(tmp_path: Path):
    """Codex P1: 'never refused on a guess' made an undated ruling exempt FOREVER. Not knowing
    when a ruling was made cannot excuse leaving it unlanded; the refusal says what is missing."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(tmp_path, {"RATIFICATION-undated.md": "## R99 — undated\n"}, _TWO_CLOSED)
    got = dc.unlanded_rulings(root, transport)
    assert _names(got) == ["R99"] and "date" in got[0].evidence


def test_an_undated_ruling_that_is_landed_is_not_refused(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(99, NO_IMPL))
    transport = _transport(tmp_path, {"RATIFICATION-undated.md": "## R99 — undated\n"}, _TWO_CLOSED)
    assert dc.unlanded_rulings(root, transport) == []


def test_a_malformed_header_date_reads_as_undated_and_does_not_crash(tmp_path: Path):
    """Codex P1: `date: 2026-99-01` raised ValueError out of the ship gate."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-99-01", "R99")},
                           _TWO_CLOSED)
    assert _names(dc.unlanded_rulings(root, transport)) == ["R99"]


def test_a_malformed_CLOSED_date_makes_the_batch_clock_unreadable_not_a_crash(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")},
        {"STATE-BATCH-ONE.md": "CLOSED 2026-99-01T00:00Z\n"})
    with pytest.raises(dc.TransportUnreadable):
        dc.closed_batch_dates(transport)
    report = dc.rulings_report(root, transport=transport)
    assert report.unlanded is None and "not measured" in report.render()


def test_an_unreadable_ratification_file_is_not_an_empty_one(tmp_path: Path, monkeypatch):
    """Codex P1: `file_rulings` swallowed OSError into `[]`, so a read failure looked like a file
    with no rulings and the unlanded leg passed."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")}, _TWO_CLOSED)
    real = Path.read_text

    def deny(self, *a, **k):
        if self.name == "RATIFICATION-2026-09-01.md":
            raise PermissionError("access denied")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", deny)
    report = dc.rulings_report(root, transport=transport)
    assert report.unlanded is None and "RATIFICATION-2026-09-01.md" in report.unmeasured_reason


def test_an_invalid_header_date_is_undated_not_the_file_name_date(tmp_path: Path):
    """Codex pass 2: a bad `date:` header fell back to the file-name date, which can sit inside
    the grace period and hide the refusal. Present-but-invalid is undated, and undated refuses."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-99-01", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05")})      # ONE batch: inside the grace
    got = dc.unlanded_rulings(root, transport)
    assert _names(got) == ["R99"] and "no computable date" in got[0].evidence


def test_an_unreadable_STATE_BATCH_file_makes_the_clock_unreadable(tmp_path: Path, monkeypatch):
    """Codex pass 2: `_head` swallowed the OSError, so a denied batch file was an omitted batch
    and the count fell to zero."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05"),
         "STATE-BATCH-TWO.md": CLOSED.format(day="2026-09-09")})
    real = Path.read_text

    def deny(self, *a, **k):
        if self.name == "STATE-BATCH-TWO.md":
            raise PermissionError("access denied")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", deny)
    with pytest.raises(dc.TransportUnreadable):
        dc.closed_batch_dates(transport)
    report = dc.rulings_report(root, transport=transport)
    assert report.unlanded is None and "STATE-BATCH-TWO.md" in report.unmeasured_reason


def test_an_unmeasured_report_never_renders_as_a_bare_OK(tmp_path: Path):
    """Codex pass 2: the unreadable states rendered `OK`. A leg that was not measured is not a
    pass; the headline says so."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    text = dc.rulings_report(root, transport=None).render()
    head = text.splitlines()[0]
    assert "NOT MEASURED" in head and not head.rstrip().endswith(": OK")


def test_the_rulings_cli_exits_2_when_the_transport_is_unreadable(tmp_path: Path, monkeypatch,
                                                                  capsys):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    (tmp_path / "bare").mkdir()
    monkeypatch.setattr(dc, "_transport_root", lambda: tmp_path / "bare")
    assert dc.main(["rulings", "--repo-root", str(root)]) == 2
    assert "NOT MEASURED" in capsys.readouterr().out


def test_the_rulings_cli_stays_0_when_the_operator_chose_no_transport(tmp_path: Path, capsys):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    assert dc.main(["rulings", "--repo-root", str(root), "--no-transport"]) == 0
    assert "NOT MEASURED" in capsys.readouterr().out


def test_a_date_with_trailing_garbage_is_invalid_not_a_valid_prefix(tmp_path: Path):
    """Codex pass 3: `date: 2026-09-01garbage` matched on its valid-looking prefix."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    transport = _transport(
        tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01garbage", "R99")},
        {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05")})      # ONE batch: inside the grace
    got = dc.unlanded_rulings(root, transport)
    assert _names(got) == ["R99"] and "no computable date" in got[0].evidence


def test_a_CLOSED_date_with_trailing_garbage_makes_the_clock_unreadable(tmp_path: Path):
    transport = _transport(tmp_path, {}, {"STATE-BATCH-ONE.md": "CLOSED 2026-09-05garbage\n"})
    with pytest.raises(dc.TransportUnreadable):
        dc.closed_batch_dates(transport)


@pytest.mark.parametrize("stamp", ["2026-09-05Tgarbage", "2026-09-05T", "2026-09-05T25:99Z",
                                   "2026-09-05T08:00Zjunk"])
def test_a_CLOSED_stamp_with_a_bad_time_part_makes_the_clock_unreadable(tmp_path: Path, stamp: str):
    """Codex pass 4: `T\\S*` accepted any suffix after the T."""
    transport = _transport(tmp_path, {}, {"STATE-BATCH-ONE.md": f"CLOSED {stamp}\n"})
    with pytest.raises(dc.TransportUnreadable):
        dc.closed_batch_dates(transport)


@pytest.mark.parametrize("stamp", ["2026-09-05T08:00Z", "2026-09-05T08:00:30Z", "2026-10-04T14:29+02:00",
                                   "2026-09-05"])
def test_a_wellformed_CLOSED_stamp_is_a_closed_day(tmp_path: Path, stamp: str):
    transport = _transport(tmp_path, {}, {"STATE-BATCH-ONE.md": f"CLOSED {stamp} -- x\n"})
    assert len(dc.closed_batch_dates(transport)) == 1


def test_a_CLOSED_timestamp_is_still_a_closed_day(tmp_path: Path):
    transport = _transport(tmp_path, {}, {"STATE-BATCH-ONE.md": "CLOSED 2026-09-05T08:00Z -- x\n"})
    assert [d.isoformat() for d in dc.closed_batch_dates(transport)] == ["2026-09-05"]


def test_a_folder_that_cannot_be_enumerated_is_unreadable_not_empty(tmp_path: Path, monkeypatch):
    """Codex pass 3: `Path.glob` can hide an enumeration error, which reads as zero batches."""
    transport = _transport(tmp_path, {}, {"STATE-BATCH-ONE.md": CLOSED.format(day="2026-09-05")})

    def deny(_path):
        raise PermissionError("access denied")

    monkeypatch.setattr(dc.os, "listdir", deny)
    with pytest.raises(dc.TransportUnreadable):
        dc.closed_batch_dates(transport)
    with pytest.raises(dc.TransportUnreadable):
        dc.ratification_files(transport)


def test_a_report_that_was_not_measured_has_not_passed(tmp_path: Path):
    """Codex pass 3: `refused` is False for an unmeasured report, so a consumer reading it alone
    would pass. `passed` is the property that is True only when BOTH legs were measured clean."""
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    assert dc.rulings_report(root, transport=None).passed is False
    transport = _transport(tmp_path, {"RATIFICATION-2026-09-01.md": _ratification("2026-09-01", "R70")},
                           _TWO_CLOSED)
    assert dc.rulings_report(root, transport=transport).passed is True


@pytest.mark.parametrize("clause", ["non-owner: the fixture lane", "co-owner: the fixture lane",
                                    "owner_x: the fixture lane", "not owner: the fixture lane",
                                    "not  owner: the fixture lane", "non owner: the fixture lane",
                                    "has no owner: the fixture lane"])
def test_only_an_owner_clause_names_an_owner(tmp_path: Path, clause: str):
    root = tmp_path / "r"
    _register(root, _entry(70, "[#1500]"))
    _ruling_row(root, 1500, "open", "R70", owner=False)
    path = next((root / "tasks").glob("1500-*.md"))
    path.write_text(path.read_text(encoding="utf-8") + f"- extra · {clause}\n", encoding="utf-8")
    assert _names(dc.uncarried_rulings(root)) == ["R70"]


# --- the transport boundary ----------------------------------------------------------------


def test_an_unreadable_transport_is_reported_unmeasured_never_a_pass(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    report = dc.rulings_report(root, transport=None)
    assert report.uncarried == []
    assert report.unlanded is None, "None is 'not measured' -- an empty list would read as clean"
    assert "not measured" in report.render()


def test_a_transport_with_no_to_browser_folder_is_unreadable_not_empty(tmp_path: Path):
    root = tmp_path / "r"
    _register(root, _entry(70, NO_IMPL))
    (tmp_path / "bare").mkdir()
    assert dc.rulings_report(root, transport=tmp_path / "bare").unlanded is None


# --- the live tree --------------------------------------------------------------------------


def test_the_live_register_carries_every_gated_ruling():
    """Item 2's RED: every landed R55-R79 entry has a row or a disposition. On e67f27ac the
    register stops at R54, so this is the test the rows and the section have to turn green."""
    text = (REPO_ROOT / "protocols" / "STANDING_RULINGS.md").read_text(encoding="utf-8")
    landed = {e.number for e in dc.parse_register(text)}
    assert set(range(55, 80)) <= landed, sorted(set(range(55, 80)) - landed)
    assert dc.uncarried_rulings(REPO_ROOT) == [], _names(dc.uncarried_rulings(REPO_ROOT))


def test_the_live_rows_this_lane_filed_sit_in_its_id_block():
    """Every row an R55-R79 entry names is an existing row; the rows this lane filed live in
    1360-1399 (task-id allocation N6) -- a row outside the block was a pre-existing one."""
    text = (REPO_ROOT / "protocols" / "STANDING_RULINGS.md").read_text(encoding="utf-8")
    named = {int(r) for e in dc.parse_register(text) if e.number >= 55 for r in e.rows}
    assert named, "no gated entry names a row"
    pre_existing = {1334}                      # R57 is carried by the row FOUNDATION filed
    assert all(1360 <= n <= 1399 for n in named - pre_existing), sorted(named)
    assert any(1360 <= n <= 1399 for n in named)


def test_the_live_unlanded_leg_where_the_transport_is_reachable():
    transport = dc._transport_root()
    if transport is None or not (Path(transport) / "to-browser").is_dir():
        import warnings
        warnings.warn("UNVERIFIED: no transport -- the unlanded-for-a-batch leg was not run",
                      UserWarning, stacklevel=1)
        return
    got = dc.unlanded_rulings(REPO_ROOT, transport)
    assert got == [], "; ".join(f"{f.subject}: {f.evidence}" for f in got)
