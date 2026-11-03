"""Coverage for scripts/boot_frontier.py -- the v7 BOOT-INVERSION frontier/scoring/batch
library (contract lane-b-2-handoff-v7, item 2: "the hard part is a library, not a skill").
"""
from __future__ import annotations

from pathlib import Path

import pytest

import boot_frontier as bootf
import gen_task_tree as gtt

REPO_ROOT = Path(__file__).resolve().parent.parent


def _row(id_, raw_tail="", priority="P2"):
    """A minimal open TaskRow: `- [#N] [P2] title <tail>`."""
    raw = f"- [#{id_}] [{priority}] row {id_}{raw_tail}"
    return gtt.TaskRow(id=id_, raw=raw, theme=None, story=None)


# --- depends_on_ids -----------------------------------------------------------------------

def test_depends_on_ids_absent():
    row = _row(1)
    assert bootf.depends_on_ids(row.raw) == frozenset()


def test_depends_on_ids_single():
    row = _row(1, " · depends-on: #2")
    assert bootf.depends_on_ids(row.raw) == frozenset({2})


def test_depends_on_ids_multiple():
    row = _row(1, " · depends-on: #2, #3")
    assert bootf.depends_on_ids(row.raw) == frozenset({2, 3})


# --- build_dependency_graph / unblocked_frontier ------------------------------------------

def test_frontier_row_with_no_dependency_is_unblocked():
    rows = [_row(1)]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_frontier_excludes_row_blocked_by_open_dependency():
    # #2 depends on #1, and #1 is still open -> #2 is blocked, #1 is the frontier.
    rows = [_row(1), _row(2, " · depends-on: #1")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_frontier_includes_row_whose_dependency_already_closed():
    # #2 depends on #99, which is NOT in the open set (tasks/ carries open rows only, so an
    # absent id is already closed) -> #2 is unblocked.
    rows = [_row(2, " · depends-on: #99")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [2]


def test_frontier_chain_only_root_unblocked():
    # 3 -> 2 -> 1 (each depends on the previous); only #1 has no open dependency.
    rows = [_row(1), _row(2, " · depends-on: #1"), _row(3, " · depends-on: #2")]
    frontier = bootf.unblocked_frontier(rows)
    assert [r.id for r in frontier] == [1]


def test_cycle_raises_cycle_error():
    rows = [_row(1, " · depends-on: #2"), _row(2, " · depends-on: #1")]
    with pytest.raises(bootf.CycleError):
        bootf.unblocked_frontier(rows)


# --- scoring seam --------------------------------------------------------------------------

def test_default_score_orders_by_priority_band_first():
    p1 = _row(1, priority="P1")
    p3 = _row(2, priority="P3")
    scored = bootf.score_frontier([p3, p1], all_open_rows=[p3, p1])
    assert [r.id for r in scored] == [1, 2]


def test_default_score_ties_broken_by_contention_then_id():
    # Same priority band; #10 and #11 share a serialize-group (contention 1 each), #12 does
    # not (contention 0) -- higher contention sorts first as the [#566] tiebreak.
    a = _row(10, " · serialize-group: g", priority="P2")
    b = _row(11, " · serialize-group: g", priority="P2")
    c = _row(12, priority="P2")
    scored = bootf.score_frontier([c, a, b], all_open_rows=[c, a, b])
    assert [r.id for r in scored] == [10, 11, 12]


def test_scorer_is_swappable():
    """The scoring seam accepts a caller-supplied ScoreFn -- the declared, swappable
    interface BOOT-R1's survey will eventually pin (contract item 5)."""
    rows = [_row(1), _row(2)]
    reverse_by_id = lambda row, contention: -row.id  # noqa: E731 -- test-local scorer
    scored = bootf.score_frontier(rows, all_open_rows=rows, scorer=reverse_by_id)
    assert [r.id for r in scored] == [2, 1]


# --- batch selection: disjointness / width / ledger -----------------------------------------

def test_select_batch_respects_ledger_bound():
    rows = [_row(i) for i in range(1, 10)]  # 9 candidates
    batch = bootf.select_batch(rows, width=6, ledger_bound=5)
    assert len(batch.selected) == 5
    assert batch.truncated_by_ledger is True


def test_select_batch_respects_width_when_tighter_than_ledger():
    rows = [_row(i) for i in range(1, 10)]
    batch = bootf.select_batch(rows, width=3, ledger_bound=5)
    assert len(batch.selected) == 3


def test_select_batch_disjointness_holds_back_second_of_same_group():
    a = _row(1, " · serialize-group: g")
    b = _row(2, " · serialize-group: g")
    c = _row(3)
    batch = bootf.select_batch([a, b, c], width=6, ledger_bound=5)
    assert [r.id for r in batch.selected] == [1, 3]
    assert [r.id for r in batch.held_back_disjointness] == [2]


def test_select_batch_not_truncated_when_fewer_rows_than_cap():
    rows = [_row(1), _row(2)]
    batch = bootf.select_batch(rows, width=6, ledger_bound=5)
    assert batch.truncated_by_ledger is False
    assert len(batch.selected) == 2


def test_select_batch_never_only_easy():
    """An unblocked P3 must not crowd out an unblocked P1 for a ledger slot -- the primary
    sort key is the operator-set priority band, not size/effort (contract item 6)."""
    p3s = [_row(i, priority="P3") for i in range(1, 6)]
    p1 = _row(6, priority="P1")
    scored = bootf.score_frontier([*p3s, p1], all_open_rows=[*p3s, p1])
    batch = bootf.select_batch(scored, width=6, ledger_bound=1)
    assert [r.id for r in batch.selected] == [6]


def test_batch_proposal_never_executes_anything():
    """BatchProposal carries no dispatch hook -- it is data, and render_proposal states the
    GO requirement explicitly (AUT-R1 Phase 4)."""
    batch = bootf.select_batch([_row(1)])
    assert not hasattr(batch, "dispatch")
    assert "operator GO" in bootf.render_proposal(batch)


def test_render_proposal_empty_batch():
    batch = bootf.select_batch([])
    assert "no batch to propose" in bootf.render_proposal(batch)


# --- live-repo smoke tests (read-only) -------------------------------------------------------

def test_load_open_rows_reads_the_live_tree():
    rows = bootf.load_open_rows(REPO_ROOT)
    assert isinstance(rows, list)
    assert all(isinstance(r, gtt.TaskRow) for r in rows)


def test_propose_batch_on_live_repo_obeys_the_ledger_bound():
    try:
        batch = bootf.propose_batch(REPO_ROOT)
    except bootf.CycleError as exc:
        pytest.fail(f"live tasks/ depends-on graph has a cycle: {exc}")
    assert len(batch.selected) <= bootf.LEDGER_BOUND
    assert len(batch.selected) <= bootf.BATCH_WIDTH_MAX
    groups = [gtt.derive_serialize_group(r.raw) for r in batch.selected]
    groups = [g for g in groups if g is not None]
    assert len(groups) == len(set(groups))  # disjointness holds on the live proposal


# --- C07 row picking and protected-set distillation --------------------------------------

def _qualifying_tail(*, phase="build", touches="`scripts/widget.py`", done="widget works",
                     depends=None):
    tail = f" · phase: {phase}"
    if touches is not None:
        tail += f" · touches: {touches}"
    if done is not None:
        tail += f" · Done when: {done}"
    if depends is not None:
        tail += f" · depends-on: {depends}"
    return tail


def test_pick_distillable_row_skips_unqualified_and_blocked_rows():
    import boot_frontier

    rows = [
        _row(1, priority="P1"),  # Highest-ranked but unphased.
        _row(2, _qualifying_tail(depends="#1"), priority="P1"),  # Blocked by open #1.
        _row(3, _qualifying_tail(phase="review"), priority="P1"),
        _row(4, _qualifying_tail(touches=None), priority="P1"),
        _row(5, _qualifying_tail(done=None), priority="P1"),
        _row(6, _qualifying_tail(), priority="P2"),
    ]
    picked = boot_frontier.pick_distillable_row(rows)
    assert picked is rows[-1]
    assert boot_frontier.pick_distillable_row(rows, protected={6}) is rows[-1]
    assert boot_frontier.pick_distillable_row(rows, protected={1}) is None
    assert boot_frontier.pick_distillable_row(rows, protected=frozenset()) is None


def test_protected_set_is_committed_validated_data(tmp_path):
    import subprocess
    import boot_frontier
    import silent_rule_detector
    from test_distill_contract import build_fixture_repo

    source = REPO_ROOT / "ecosystem" / "protected-set.yaml"
    assert boot_frontier.PROTECTED_SET_SOURCE == "ecosystem/protected-set.yaml"
    assert source.is_file()
    assert boot_frontier.load_protected_set(REPO_ROOT) == frozenset()
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "ecosystem/protected-set.yaml"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert tracked.stdout.strip() == "ecosystem/protected-set.yaml"
    source_text = source.read_text(encoding="utf-8")
    assert source_text.splitlines()[0].startswith("#")
    assert silent_rule_detector.TOKEN_RE.findall(source_text) == []

    repo = build_fixture_repo(tmp_path / "fixture", protected_ids=(12, 34))
    path = repo / boot_frontier.PROTECTED_SET_SOURCE
    assert boot_frontier.load_protected_set(repo) == frozenset({12, 34})
    malformed = [
        ("empty file", ""),
        ("missing key", "other: []\n"),
        ("not a list", "task_ids: 12\n"),
        ("duplicate", "task_ids: [12, 12]\n"),
        ("boolean", "task_ids: [true]\n"),
        ("fraction", "task_ids: [1.5]\n"),
        ("negative", "task_ids: [-3]\n"),
        ("string", "task_ids: ['12']\n"),
    ]
    for label, contents in malformed:
        path.write_text(contents, encoding="utf-8")
        with pytest.raises(boot_frontier.ProtectedSetError) as refused:
            boot_frontier.load_protected_set(repo)
        assert str(path) in str(refused.value), label
    path.unlink()
    with pytest.raises(boot_frontier.ProtectedSetError) as missing:
        boot_frontier.load_protected_set(repo)
    assert str(path) in str(missing.value)


def test_pick_cli_obeys_protection_and_refuses_malformed_sets(tmp_path, capsys):
    import boot_frontier
    from test_distill_contract import build_fixture_repo, fixture_row, write_protected_set

    repo = build_fixture_repo(
        tmp_path / "fixture",
        rows=[
            fixture_row(100, title="First widget", priority="P1", depends_on=None),
            fixture_row(101, title="Second widget", priority="P2", depends_on=None),
        ],
        protected_ids=(100, 101),
    )
    assert [row.id for row in boot_frontier.load_open_rows(repo)] == [100, 101]
    assert boot_frontier._main(["--pick", "--repo", str(repo)]) == 0
    assert capsys.readouterr().out.strip() == "PICK [#100] phase=build First widget"

    write_protected_set(repo, (101,))
    assert boot_frontier._main(["--pick", "--repo", str(repo)]) == 0
    assert capsys.readouterr().out.strip() == "PICK [#101] phase=build Second widget"

    write_protected_set(repo, ())
    assert boot_frontier._main(["--pick", "--repo", str(repo)]) == 3
    assert capsys.readouterr().out.strip() == "PICK none: 2 unblocked, 2 distillable, 0 protected"
    write_protected_set(repo, (999,))
    assert boot_frontier._main(["--pick", "--repo", str(repo)]) == 3
    assert capsys.readouterr().out.strip() == "PICK none: 2 unblocked, 2 distillable, 1 protected"

    protected = repo / boot_frontier.PROTECTED_SET_SOURCE
    protected.write_text("task_ids: [true]\n", encoding="utf-8")
    assert boot_frontier._main(["--pick", "--repo", str(repo)]) == 2
    captured = capsys.readouterr()
    assert str(protected) in captured.err
    assert "PICK" not in captured.out

    for args in (
        ["--pick", "--repo", str(repo), "--protected-file", str(protected)],
        ["--distill", "--repo", str(repo)],
    ):
        with pytest.raises(SystemExit) as error:
            boot_frontier._main(args)
        assert error.value.code == 2
        capsys.readouterr()
    source = (REPO_ROOT / "scripts" / "boot_frontier.py").read_text(encoding="utf-8")
    assert "QUESTION 2" not in source


def test_pick_distill_cli_is_the_acceptance_gate_and_shares_receipt_output(
    tmp_path, capsys, monkeypatch,
):
    import hashlib
    import json
    import gen_lane_contract as glc
    import boot_frontier
    import conductor
    import plan_lint
    import subst_gate
    import dispatch
    import provider_registry
    from click.testing import CliRunner
    from test_distill_contract import build_fixture_repo, fixture_row

    repo = build_fixture_repo(
        tmp_path / "fixture",
        rows=[fixture_row(4242, depends_on=None)],
        protected_ids=(4242,),
    )
    assert [row.id for row in boot_frontier.load_open_rows(repo)] == [4242]
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    code = boot_frontier._main([
        "--pick", "--distill", "--out-dir", str(out_dir), "--repo", str(repo),
    ])
    assert code == 0
    captured = capsys.readouterr()
    stdout_receipt = json.loads(captured.out)
    picked = boot_frontier.load_open_rows(repo)[0]
    slug = glc.row_slug(picked.id, picked.title)
    contract = out_dir / glc.contract_filename(slug)
    assert contract.is_file()
    assert f"CONTRACT {contract} sha256={hashlib.sha256(contract.read_bytes()).hexdigest()}" in (
        captured.err + captured.out
    )
    text = contract.read_text(encoding="utf-8")
    assert glc.parse_contract(text).ok
    assert plan_lint.lint([plan_lint.parse_lane_contract(contract)], repo) == []
    assert subst_gate.contract_problems(
        text, lane=slug, batch="E3.0",
    )[0] == []
    assert conductor.contract_phases(text) is not None
    launched = CliRunner().invoke(dispatch.cli, ["launch", str(contract), "--dry-run"])
    assert launched.exit_code == 0, launched.output
    launch = json.loads(launched.output.strip().splitlines()[-1])
    assert (launch["slug"], launch["model"], launch["effort"], launch["provider"]) == (
        slug, provider_registry.claude_alias_ids()["sonnet"], "high", "anthropic",
    )

    receipt_path = tmp_path / "picked-receipt.json"
    receipt_out_dir = tmp_path / "with-receipt"
    receipt_out_dir.mkdir()
    code = boot_frontier._main([
        "--pick", "--distill", "--out-dir", str(receipt_out_dir),
        "--receipt", str(receipt_path), "--repo", str(repo),
    ])
    assert code == 0
    captured = capsys.readouterr()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["row_state"] == "ready"
    assert receipt == stdout_receipt
    assert "row_state" not in captured.out
    assert sum(line.startswith("CONTRACT ") for line in captured.err.splitlines()) == 1

    empty_repo = build_fixture_repo(
        tmp_path / "empty", rows=[fixture_row(4242, depends_on=None)],
    )
    empty_out = tmp_path / "empty-out"
    empty_out.mkdir()
    assert boot_frontier._main([
        "--pick", "--distill", "--out-dir", str(empty_out), "--repo", str(empty_repo),
    ]) == 3
    empty_result = capsys.readouterr()
    assert "ruled" not in (empty_result.out + empty_result.err).lower()
    assert list(empty_out.iterdir()) == []

    bad_repo = build_fixture_repo(
        tmp_path / "bad",
        rows=[fixture_row(4242, done="**Consumes:** `unproduced-artifact`")],
        protected_ids=(4242,),
    )
    bad_out = tmp_path / "bad-out"
    bad_out.mkdir()
    assert boot_frontier._main([
        "--pick", "--distill", "--out-dir", str(bad_out), "--repo", str(bad_repo),
    ]) == 1
    assert list(bad_out.iterdir()) == []
    capsys.readouterr()

    override_out = tmp_path / "override"
    override_out.mkdir()
    assert boot_frontier._main([
        "--pick", "--distill", "--slug", "custom-widget-contract",
        "--out-dir", str(override_out), "--repo", str(repo),
    ]) == 0
    capsys.readouterr()
    assert (override_out / "LANE-custom-widget-contract.md").is_file()
    with pytest.raises(SystemExit) as error:
        boot_frontier._main(["--distill", "--repo", str(repo)])
    assert error.value.code == 2
    capsys.readouterr()


def test_row_slug_is_stable_kebab_and_valid_for_punctuation():
    import gen_lane_contract as glc

    title = "Widget — polish `blue` v2 with care plus more words"
    slug = glc.row_slug(4242, title)
    assert slug == "row-4242-widget-polish-blue-v2-with"
    assert len(slug) <= 60
    assert not slug.endswith("-")
    assert glc.validate_slug(slug, strict=False) == slug
    assert glc.row_slug(4242, title) == slug
    long_slug = glc.row_slug(4242, title + " " + "extra " * 20)
    assert len(long_slug) <= 60
    assert not long_slug.endswith("-")
    assert long_slug.endswith("widget-polish-blue-v2-with")


def test_default_and_frontier_cli_output_remain_unchanged_on_a_fixture(tmp_path, capsys):
    import boot_frontier
    from test_distill_contract import build_fixture_repo, fixture_row

    repo = build_fixture_repo(
        tmp_path / "fixture",
        rows=[
            fixture_row(10, title="First widget", depends_on=None),
            fixture_row(11, title="Second widget", depends_on=None),
        ],
    )
    rows = boot_frontier.load_open_rows(repo)
    frontier = boot_frontier.unblocked_frontier(rows)
    expected = boot_frontier.render_proposal(
        boot_frontier.select_batch(boot_frontier.score_frontier(frontier, rows))
    )
    assert boot_frontier._main(["--repo", str(repo)]) == 0
    assert capsys.readouterr().out.strip() == expected

    expected_frontier = [
        f"boot_frontier: {len(frontier)} unblocked row(s) in {len(rows)} open",
        *(f"  [#{row.id}] {gtt.derive_title(row.raw)}" for row in frontier),
    ]
    assert boot_frontier._main(["--frontier", "--repo", str(repo)]) == 0
    assert capsys.readouterr().out.splitlines() == expected_frontier


def test_boot_frontier_stays_outside_edge_computation_shape():
    import graph_queries

    source = (REPO_ROOT / "scripts" / "boot_frontier.py").read_text(encoding="utf-8")
    assert graph_queries.is_edge_computation_shape(source) is False


def test_pick_model_resolution_uses_the_checkout_registry_not_fixture_data(tmp_path):
    import gen_lane_contract as glc
    import provider_registry
    import subst_gate
    import dispatch
    from test_distill_contract import build_fixture_repo

    repo = build_fixture_repo(tmp_path / "fixture")
    assert not (repo / "ecosystem" / "provider-registry.yaml").exists()
    expected_model = provider_registry.claude_alias_ids()["sonnet"]
    assert glc.explicit_model_id("sonnet") == expected_model
    assert dispatch.MODEL_ALIASES["sonnet"] == expected_model
    text = glc.render_contract(glc.LaneSpec(
        slug="lane-ab-4242-registry-check",
        purpose="resolve the model from the registry",
        kind="code",
        model="sonnet",
        model_id=expected_model,
    ))
    assert subst_gate.contract_problems(
        text, lane="lane-ab-4242-registry-check", batch="E3.0",
    )[0] == []
    assert dispatch.parse_dispatch_block(text).model == expected_model


def test_boot_frontier_import_and_pick_do_not_load_provider_callers(tmp_path):
    import subprocess
    import sys
    from test_distill_contract import build_fixture_repo

    repo = build_fixture_repo(tmp_path / "fixture")
    scripts = REPO_ROOT / "scripts"
    import_only = (
        "import sys; "
        f"sys.path.insert(0, {str(scripts)!r}); "
        "import boot_frontier; "
        "unexpected = {'gen_lane_contract', 'yaml'} & sys.modules.keys(); "
        "assert not unexpected, f'unexpected eager imports: {sorted(unexpected)}'"
    )
    imported = subprocess.run(
        [sys.executable, "-I", "-c", import_only],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert imported.returncode == 0, imported.stderr

    pick_only = (
        "import sys; "
        f"sys.path.insert(0, {str(scripts)!r}); "
        "import boot_frontier; "
        f"code = boot_frontier._main(['--pick', '--repo', {str(repo)!r}]); "
        "assert 'provider_router' not in sys.modules; "
        "assert 'run_phase' not in sys.modules; "
        "raise SystemExit(code)"
    )
    picked = subprocess.run(
        [sys.executable, "-I", "-c", pick_only],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert picked.returncode == 3, picked.stderr
    assert picked.stdout.startswith("PICK none:")


def test_pick_to_contract_never_spawns_a_process_or_vendor(tmp_path, monkeypatch, capsys):
    import json
    import subprocess
    import vendor_probe
    import boot_frontier
    from test_distill_contract import build_fixture_repo, fixture_row

    repo = build_fixture_repo(
        tmp_path / "fixture", rows=[fixture_row(4242, depends_on=None)], protected_ids=(4242,),
    )
    def forbidden(*_args, **_kwargs):
        raise AssertionError("pick-to-contract attempted a subprocess or vendor probe")

    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(vendor_probe, "probe_today", forbidden)
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    assert boot_frontier._main([
        "--pick", "--distill", "--out-dir", str(out_dir), "--repo", str(repo),
    ]) == 0
    captured = capsys.readouterr()
    assert "CONTRACT " in captured.err + captured.out
    assert json.loads(captured.out)["challenge"] is None
