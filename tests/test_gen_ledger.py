"""The LEDGER is generated from repo state, reads only, and agrees with the row that reads it.

Two properties carry the rest. `test_a_render_writes_nothing_into_the_repo` is the lane
contract's own constraint ("the LEDGER generator reads, never writes, repo state"), and
`test_the_output_path_agrees_with_the_freshness_row_that_reads_it` closes the gap that makes a
generated surface worse than a hand-written one: a generator writing where nothing looks.
"""
from __future__ import annotations

import re
import subprocess

import pytest
from click.testing import CliRunner

import gen_handoff
import gen_ledger

DATE = "2026-09-09"


@pytest.fixture(scope="module")
def state():
    return gen_ledger.collect(gen_ledger._REPO_ROOT, offline=True)


@pytest.fixture(scope="module")
def text(state):
    return gen_ledger.render(state, date=DATE)


# --- reads, never writes -------------------------------------------------------------------------

def test_a_render_writes_nothing_into_the_repo():
    """The contract's constraint, asserted rather than asserted-in-prose."""
    def status() -> str:
        return subprocess.run(["git", "-C", str(gen_ledger._REPO_ROOT), "status", "--porcelain"],
                              capture_output=True, text=True, check=True).stdout

    before = status()
    gen_ledger.render(gen_ledger.collect(gen_ledger._REPO_ROOT, offline=True), date=DATE)
    assert status() == before


def test_dry_run_writes_no_file(tmp_path):
    target = tmp_path / "LEDGER-dev-knowledge.md"
    result = CliRunner().invoke(gen_ledger.cli, ["--dry-run", "--offline",
                                                 "--out", str(target), "--date", DATE])
    assert result.exit_code == 0
    assert not target.exists()
    assert "## STATE" in result.output


def test_the_cli_writes_exactly_one_file(tmp_path):
    target = tmp_path / "nested" / "LEDGER-dev-knowledge.md"
    result = CliRunner().invoke(gen_ledger.cli, ["--offline", "--out", str(target),
                                                 "--date", DATE])
    assert result.exit_code == 0
    assert target.exists()
    assert sorted(p.name for p in target.parent.iterdir()) == [target.name]


# --- it agrees with the organ that reads it --------------------------------------------------------

def test_the_output_path_agrees_with_the_freshness_row_that_reads_it():
    """`gen_handoff._row_ledger_refreshed` looks in ONE place; this generator writes in it."""
    assert gen_ledger.out_relpath(".dev-knowledge") == "to-browser/LEDGER-dev-knowledge.md"


def test_the_refreshed_token_is_the_one_the_freshness_row_parses(text):
    """The row reads an anchored `refreshed <YYYY-MM-DD>` from the first 4000 characters."""
    match = gen_handoff._LEDGER_REFRESHED_RE.search(text[:4000])
    assert match is not None and match.group(1) == DATE


def test_the_next_bound_is_read_from_boot_frontier_not_retyped():
    import boot_frontier
    assert gen_ledger.NEXT_BOUND is boot_frontier.LEDGER_BOUND


# --- the three sections the contract names ---------------------------------------------------------

def test_the_three_sections_are_present_in_order(text):
    positions = [text.index(h) for h in ("## STATE", "## BLOCKED BY", "## NEXT")]
    assert positions == sorted(positions)


def test_state_reports_the_shas_the_worktrees_and_the_open_batch(text, state):
    assert f"- main: {state['main']}" in text
    assert "- origin/main:" in text
    assert "- worktrees:" in text
    assert "- newest JOURNAL entry:" in text
    assert ("OPEN BATCH" in text) == bool(state["open_batches"])


def test_next_says_on_its_own_line_that_it_is_a_proposal(text):
    assert "A PROPOSAL, not a dispatch" in text
    assert "explicit operator GO" in text


def test_blocked_by_states_the_only_blockage_it_can_see(text):
    """The honest limit rides in the artifact, not only in the module docstring."""
    assert "`depends-on` among open rows and nothing else" in text


def test_the_header_says_no_gate_and_no_suite_was_run(text):
    assert "NO gate and NO suite was run" in text


# --- shape: flat, because it is pasted into a browser chat -----------------------------------------

def test_the_journal_head_is_a_dated_entry_and_not_a_silent_UNAVAILABLE(text):
    """JOURNAL entries are depth 3 under a depth-1 title, so a "first `##`" read finds nothing
    and renders UNAVAILABLE while the file is perfectly readable -- a wrong answer that looks
    like a missing file. Caught on the first witnessed run."""
    head = next(ln for ln in text.splitlines() if ln.startswith("- newest JOURNAL entry:"))
    assert gen_ledger._UNKNOWN not in head
    assert re.search(r"\d{4}-\d{2}-\d{2}", head)


def test_the_journal_reader_accepts_the_depth_the_file_actually_uses(tmp_path):
    (tmp_path / "JOURNAL.md").write_text(
        "# Journal\n\n> preamble\n\n### 2026-09-09 (a) - CC: a thing\n\nbody\n", encoding="utf-8")
    assert gen_ledger._journal_head(tmp_path).startswith("2026-09-09 (a)")


def test_the_worktree_line_counts_lanes_rather_than_trees(text):
    """"How many trees exist" and "how many lanes are live" differ by one, always."""
    line = next(ln for ln in text.splitlines() if ln.startswith("- worktrees:"))
    assert "primary + " in line


def test_the_held_back_line_reports_a_count_and_a_bounded_sample(state):
    """~60 ids would be the longest line in the file and would say nothing the count does not."""
    proposal = state["proposal"]
    if proposal is None or not proposal.held_back_disjointness:
        pytest.skip("nothing held back in the live queue")
    line = next(ln for ln in gen_ledger.render(state, date=DATE).splitlines()
                if ln.startswith("- held back"))
    assert f"{len(proposal.held_back_disjointness)} row(s)" in line
    assert line.count("#") <= gen_ledger.HELD_BACK_SHOWN + 1
    if len(proposal.held_back_disjointness) > gen_ledger.HELD_BACK_SHOWN:
        assert "more (full roster:" in line


def test_the_output_carries_no_column_padded_table(text):
    """PLAYBOOK section 8 -- a padded table costs ~3x its content for a border the client draws."""
    assert not re.search(r"^\s*\|", text, re.MULTILINE)
    assert not re.search(r"  +\|", text)


# --- degradation ------------------------------------------------------------------------------------

def test_origin_main_reports_UNREACHABLE_rather_than_falling_back_to_the_cached_ref(monkeypatch):
    """A cached `origin/main` is a fact about the last fetch, and the two look identical."""
    monkeypatch.setattr(gen_ledger, "_git", lambda *_a, **_k: gen_ledger._UNKNOWN)
    out = gen_ledger._origin_main(gen_ledger._REPO_ROOT)
    assert out.startswith("UNREACHABLE")
    assert "cached ref" in out


def test_offline_skips_the_remote_read_entirely(monkeypatch):
    def explode(*_a, **_k):                       # pragma: no cover -- must not be reached
        raise AssertionError("--offline still called git")

    monkeypatch.setattr(gen_ledger, "_git", explode)
    assert gen_ledger._origin_main(gen_ledger._REPO_ROOT, offline=True) == "not read (offline)"


def test_an_unreadable_queue_degrades_to_a_named_reason_rather_than_a_crash(monkeypatch):
    monkeypatch.setattr(gen_ledger._bf, "load_open_rows",
                        lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("cyclic depends-on")))
    rendered = gen_ledger.render(gen_ledger.collect(gen_ledger._REPO_ROOT, offline=True),
                                 date=DATE)
    assert "the queue could not be read: cyclic depends-on" in rendered
    assert "## NEXT" in rendered


# --- a failed probe is never rendered as a fact (terra HIGHs, 2026-09-09) --------------------------

def test_an_unreadable_queue_does_not_render_as_zero_open_rows(monkeypatch):
    """"open rows: 0" invites the reader to conclude there is no pending work."""
    monkeypatch.setattr(gen_ledger._bf, "load_open_rows",
                        lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("cyclic")))
    rendered = gen_ledger.render(gen_ledger.collect(gen_ledger._REPO_ROOT, offline=True),
                                 date=DATE)
    assert "- open rows: 0" not in rendered
    assert f"- open rows: {gen_ledger._UNKNOWN}" in rendered


def test_a_failed_batch_read_does_not_render_as_no_open_batches(monkeypatch):
    """Whether the ADR-110 exemption is live is exactly what the operator opens this to learn."""
    monkeypatch.setattr(gen_ledger, "_open_batches",
                        lambda _root: ([], "manifest reader blew up"))
    rendered = gen_ledger.render(gen_ledger.collect(gen_ledger._REPO_ROOT, offline=True),
                                 date=DATE)
    assert "no integration-arc exemption is live" not in rendered
    assert "manifest reader blew up" in rendered


def test_a_failed_git_status_does_not_render_as_DIRTY():
    assert gen_ledger._tree_state(gen_ledger._UNKNOWN).startswith(gen_ledger._UNKNOWN)
    assert gen_ledger._tree_state("") == "clean"
    assert gen_ledger._tree_state("?? a\n?? b") == "DIRTY - 2 path(s)"


def test_a_failed_worktree_probe_does_not_render_as_primary_only():
    assert gen_ledger._worktree_line([], False).startswith(gen_ledger._UNKNOWN)
    assert gen_ledger._worktree_line(["/repo"], True) == "primary only"
    assert gen_ledger._worktree_line(["/repo", "/repo/.claude/worktrees/x"], True) == (
        "primary + 1 - x")


def test_a_failed_branch_probe_does_not_render_as_zero():
    assert gen_ledger._branch_line(gen_ledger._UNKNOWN).startswith(gen_ledger._UNKNOWN)
    assert gen_ledger._branch_line("main\nfeat/x") == "2 - main, feat/x"


def test_the_batch_reader_returns_its_error_rather_than_swallowing_it(monkeypatch):
    import batch_manifest

    monkeypatch.setattr(batch_manifest, "open_batches",
                        lambda *_a: (_ for _ in ()).throw(RuntimeError("boom")))
    batches, error = gen_ledger._open_batches(gen_ledger._REPO_ROOT)
    assert batches == [] and error == "boom"


def test_no_transport_and_no_out_is_refused_rather_than_written_somewhere(monkeypatch):
    monkeypatch.setattr(gen_ledger._gh, "transport_root", lambda *_a, **_k: None)
    result = CliRunner().invoke(gen_ledger.cli, ["--offline", "--date", DATE])
    assert result.exit_code == 1
    assert "nothing written" in result.output
