"""Tests for the `/handoff` PREFLIGHT — the nine pre-cut hygiene rows in gen_handoff.py.

The arc is RED-first (ADR-108 §B): every test here was written and watched to fail before
the implementation existed. The load-bearing pair is
`test_seeded_status_over_budget_refuses_the_cut` (a seeded FAIL must REFUSE) and
`test_clean_transport_lets_the_cut_through` (a clean run must not) — a gate that only ever
passes reports a safety it does not provide, which is the exact defect two of the nine rows
carried as specified (rows 7 and 8; see the module docstring of the preflight block).
"""
from __future__ import annotations

import pytest

import gen_handoff as gh

#: The module object gen_handoff ITSELF holds. `scripts.canonical_docs` and
#: `canonical_docs` are two distinct objects under this repo's three-root pythonpath, and a
#: monkeypatch on the wrong one is inert -- patch what the adapter holds.
_cdocs = gh._cdocs

_TODAY = "2026-09-07"


def _transport(tmp_path, *, ledger_date=_TODAY, ratification_date=_TODAY,
               status_bytes=1_000, questions=(), answers=(), repo_name=".dev-knowledge"):
    """A stub prompts-dir: `to-cc/` + `to-browser/` with a CLEAN window by default."""
    root = tmp_path / "transport"
    to_browser = root / "to-browser"
    to_cc = root / "to-cc"
    to_browser.mkdir(parents=True, exist_ok=True)
    to_cc.mkdir(parents=True, exist_ok=True)
    if ledger_date:
        (to_browser / f"LEDGER-{repo_name.lstrip('.')}.md").write_text(
            f"# LEDGER\n<!-- owner: browser seat - v4 refreshed {ledger_date} 00:05 -->\n",
            encoding="utf-8")
    if ratification_date:
        (to_browser / f"RATIFICATION-{ratification_date}.md").write_text(
            "# RATIFICATION\n", encoding="utf-8")
    if status_bytes:
        # EXACTLY `status_bytes` on disk. The seeded FAIL is a THRESHOLD case -- 5,114
        # sits between the two readings of "5 KB" -- so a helper writing header PLUS n
        # bytes lands at 5,121, pins the uncontested case, and says otherwise in its own
        # docstring. That is the shape of defect this whole lane exists to remove.
        head = b"## now\n"
        (to_browser / "STATUS-integrator.md").write_bytes(
            head + b"x" * (status_bytes - len(head)))
    for name, body in questions:
        (to_browser / name).write_text(body, encoding="utf-8")
    for name in answers:
        (to_cc / name).write_text("# ANSWER\n", encoding="utf-8")
    return root


def _hub_stub(tmp_path):
    """A repo carrying a parseable `last_reviewed` stamp on every COMPUTED stamped doc.

    The set is read from the same two surfaces the implementation reads, never typed out —
    a hard-coded roster here would pass while the real one drifted.
    """
    repo = tmp_path / "repo"
    for rel in gh._stamped_docs():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"---\nlast_reviewed: {_TODAY}\nstatus: active\n---\n\n# doc\n",
                     encoding="utf-8")
    return repo


@pytest.fixture
def _quiet_hub(monkeypatch):
    """Arm the hub gate and stub the two EXPENSIVE readers (4m30s ship-gate; git spine walk).

    Same seam idiom the boundary-hygiene tests already use for `_linked_worktrees` /
    `_stash_entries`: the wiring under test is the refusal, not the cost of the probe.
    """
    monkeypatch.setattr(gh, "_is_hub", lambda _root: True)
    monkeypatch.setattr(gh, "_ship_gate_verdict", lambda _root: ("GREEN", "stubbed GREEN"))
    monkeypatch.setattr(gh, "_journal_spine_gaps", lambda _root: [])
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [])


# --- the row contract: PASS / FAIL / n-a, each with a LOCATOR ----------------------------

def test_every_row_carries_a_status_and_a_locator(tmp_path, monkeypatch, _quiet_hub):
    """The register's shape: nine rows, each PASS/FAIL with a locator. A row with no locator
    reports a verdict the operator cannot act on."""
    repo = _hub_stub(tmp_path)
    rows = gh.preflight_rows(repo, transport=_transport(tmp_path), today=_TODAY)
    assert len(rows) == 9
    assert [r.name for r in rows] == list(gh.PREFLIGHT_ROW_NAMES)
    for r in rows:
        assert r.status in (gh.PREFLIGHT_PASS, gh.PREFLIGHT_FAIL, gh.PREFLIGHT_NA)
        assert r.locator.strip(), f"{r.name} has no locator"
        assert r.detail.strip(), f"{r.name} has no evidence line"


# --- row 4: the byte budget is 5,000 DECIMAL, settled at HANDOFF_PROCESS.md:366-370 -------

def test_status_budget_is_five_thousand_decimal_not_five_one_two_zero():
    """Not re-litigated here — cited. §5 "P8's two legs" pins 5,000 "matching the decimal
    convention", and a file measured at 5,114 bytes sits between the two readings."""
    assert gh.STATUS_BYTE_BUDGET == 5_000


def test_status_row_fails_a_file_between_the_two_readings(tmp_path):
    """5,114 bytes: under 5,120, over 5,000 — the exact file the spec names. The size is
    ASSERTED, not assumed: a fixture that overshoots to 5,121 passes this test while
    measuring the uncontested case, and its docstring goes on claiming it did not."""
    root = _transport(tmp_path, status_bytes=5_114)
    assert (root / "to-browser" / "STATUS-integrator.md").stat().st_size == 5_114 < 5_120
    row = gh._row_status_budget(root)
    assert row.status == gh.PREFLIGHT_FAIL
    assert "STATUS-integrator.md" in row.detail


def test_status_row_passes_a_file_at_the_budget(tmp_path):
    root = _transport(tmp_path, status_bytes=gh.STATUS_BYTE_BUDGET)
    seeded = root / "to-browser" / "STATUS-integrator.md"
    assert seeded.stat().st_size == gh.STATUS_BYTE_BUDGET
    assert gh._row_status_budget(root).status == gh.PREFLIGHT_PASS


# --- row 7: "no QUESTION file without a DISPOSITION" (the corrected wording) --------------

def test_archiving_alone_does_not_discharge_a_question(tmp_path):
    """THE CORRECTION. As registered ("no QUESTION-* unanswered") the row is satisfied by an
    empty directory — lane C-3 archived all 20 outstanding QUESTION files on 2026-09-07 and
    NONE was answered, so the registered row now passes forever and catches nothing."""
    root = _transport(tmp_path)
    arch = root / "to-browser" / "archive" / _TODAY
    arch.mkdir(parents=True)
    (arch / "QUESTION-lane-a.md").write_text("# QUESTION\nstill open\n", encoding="utf-8")
    row = gh._row_question_disposition(root, _TODAY)
    assert row.status == gh.PREFLIGHT_FAIL
    assert "QUESTION-lane-a.md" in row.detail


def test_an_answered_question_is_dispositioned(tmp_path):
    root = _transport(tmp_path,
                      questions=[("QUESTION-lane-a.md", "# QUESTION\n")],
                      answers=["ANSWER-lane-a.md"])
    assert gh._row_question_disposition(root, _TODAY).status == gh.PREFLIGHT_PASS


def test_a_carried_question_needs_a_RESOLVING_locator_not_a_bare_key(tmp_path):
    """The P11 lesson, applied: a predicate that matches the KEY cannot distinguish a carried
    question from one that merely mentions carriage. Anchored AND valued."""
    bare = _transport(tmp_path / "bare",
                      questions=[("QUESTION-lane-a.md", "# Q\ndisposition:\n")])
    assert gh._row_question_disposition(bare, _TODAY).status == gh.PREFLIGHT_FAIL
    prose = _transport(tmp_path / "prose",
                       questions=[("QUESTION-lane-b.md",
                                   "# Q\n\nthe disposition: is written flush-left\n")])
    assert gh._row_question_disposition(prose, _TODAY).status == gh.PREFLIGHT_FAIL
    valued = _transport(tmp_path / "valued",
                        questions=[("QUESTION-lane-c.md",
                                    "# Q\ndisposition: carried -> docs/intake/2026-09-07-x.md\n")])
    assert gh._row_question_disposition(valued, _TODAY).status == gh.PREFLIGHT_PASS


# --- row 7, the 2026-09-08 amendment: ANSWERED or CARRIED-BY-AN-OPEN-ROW -----------------

def _backlog(tmp_path, *open_ids):
    """A repo stub whose BACKLOG.md carries exactly `open_ids` as OPEN rows."""
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    rows = "".join(f"- [#{i}] [P2][S] row {i} - tasks/{i}-x.md\n" for i in open_ids)
    (repo / "BACKLOG.md").write_text("# BACKLOG\n\n" + rows, encoding="utf-8")
    return repo


def test_a_question_CARRIED_by_an_OPEN_row_is_dispositioned(tmp_path):
    """The ruling's carry leg: debt may travel, so long as an OPEN row owns it."""
    root = _transport(tmp_path, questions=[
        ("QUESTION-lane-a.md", "# Q\ndisposition: CARRIED by [#9042] -- first sitting\n")])
    row = gh._row_question_disposition(root, _TODAY, _backlog(tmp_path, "9042"))
    assert row.status == gh.PREFLIGHT_PASS
    # The pass is only honest if the seat is handed the residual obligation AND the count.
    assert "1 carried question(s) is named in the residual" in row.detail
    assert "DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08" in row.detail


def test_a_CLOSED_row_does_not_carry_an_open_question(tmp_path):
    """The refusal the carry leg turns on. `[#9042]` is locator-SHAPED, so without the id leg
    running FIRST this value would pass as an ANSWERED citation and void the ruling."""
    root = _transport(tmp_path, questions=[
        ("QUESTION-lane-a.md", "# Q\ndisposition: CARRIED by [#9042]\n")])
    row = gh._row_question_disposition(root, _TODAY, _backlog(tmp_path, "999"))
    assert row.status == gh.PREFLIGHT_FAIL
    assert "closed row does not carry" in row.detail


def test_an_unjudgeable_owner_is_not_an_owner(tmp_path):
    """No BACKLOG to read: the owner cannot be judged, which is not the same as absent.
    Unknown is not clean -- the direction every other row here already takes."""
    root = _transport(tmp_path, questions=[
        ("QUESTION-lane-a.md", "# Q\ndisposition: CARRIED by [#9042]\n")])
    row = gh._row_question_disposition(root, _TODAY, tmp_path / "no-such-repo")
    assert row.status == gh.PREFLIGHT_FAIL
    assert "could not be read" in row.detail


def test_the_row_reports_WHICH_leg_discharged_each_question(tmp_path):
    """Evidence-block discipline (HANDOFF_PROCESS s5): report what resolved and from where.
    A row that reports only PASS/FAIL cannot be audited later."""
    root = _transport(tmp_path, questions=[
        ("QUESTION-lane-a.md", "# Q\ndisposition: CARRIED by [#9042]\n")])
    ok, why = gh._question_disposition_verdict(
        root / "to-browser" / "QUESTION-lane-a.md", root, {"9042"})
    assert ok and why == "CARRIED by OPEN [#9042]"


# --- row 8: a budget that DOES NOT EXIST renders n/a-with-reason, never a silent pass -----

def test_memory_row_is_not_applicable_while_no_budget_is_declared(tmp_path):
    """THE SECOND CORRECTION. The register's row 8 ("MEMORY.md within cap") names a cap that
    is declared nowhere in scripts/, protocols/ or tests/. Inventing a number would be making
    a decision this lane does not own, so the row reads a DECLARED constant and renders
    NOT-APPLICABLE-with-reason when none is declared. It must not pass silently."""
    mem = tmp_path / "MEMORY.md"
    mem.write_bytes(b"x" * 23_851)
    row = gh._row_memory_within_cap(memory_path=mem)
    assert row.status == gh.PREFLIGHT_NA
    assert "[n/a-reason:NO-DECLARED-BUDGET]" in row.detail
    assert gh.MEMORY_BUDGET_DECLARATION_SITE in row.locator


def test_memory_row_arms_itself_the_moment_a_budget_is_declared(tmp_path, monkeypatch):
    """No code change is owed when the operator sets it — the row reads the constant."""
    monkeypatch.setattr(gh._cdocs, "MEMORY_BYTE_BUDGET", 20_000, raising=False)
    mem = tmp_path / "MEMORY.md"
    mem.write_bytes(b"x" * 23_851)
    assert gh._row_memory_within_cap(memory_path=mem).status == gh.PREFLIGHT_FAIL
    mem.write_bytes(b"x" * 19_999)
    assert gh._row_memory_within_cap(memory_path=mem).status == gh.PREFLIGHT_PASS


# --- row 5: the stamped set is COMPUTED, never a roster typed into this module ------------

def test_stamped_set_is_computed_from_the_two_owning_surfaces():
    """`canonical_docs.FRESHNESS_FILES` + `audit._HUB_ONLY_FRESHNESS_FILES`. A literal list
    here would be a roster restated in code — stale at the next commit (CLAUDE.md §4)."""
    computed = set(gh._stamped_docs())
    assert set(_cdocs.FRESHNESS_FILES) <= computed
    import audit as _aud
    assert set(_aud._HUB_ONLY_FRESHNESS_FILES) <= computed


def test_living_docs_row_fails_an_unstamped_member(tmp_path):
    repo = _hub_stub(tmp_path)
    target = gh._stamped_docs()[0]
    (repo / target).write_text("# no frontmatter here\n", encoding="utf-8")
    row = gh._row_living_docs_stamped(repo)
    assert row.status == gh.PREFLIGHT_FAIL
    assert target in row.detail


# --- rows 1, 2, 3, 6, 9 ------------------------------------------------------------------

def test_ship_gate_verdict_is_read_from_BOTH_streams(tmp_path, monkeypatch):
    """`cmd_ship_gate` writes findings to stdout and its VERDICT to stderr. A stdout-only read
    reports "no verdict line" for a gate that ran perfectly — measured 2026-09-08."""
    import subprocess as _sp

    class _P:
        stdout = "  [disp] consumer_at_landing: ... expected, not blocking\n"
        stderr = "ship-gate: RED -- not shipped-ready (1 hard-fail organ(s))\n"

    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "audit.py").write_text("x\n", encoding="utf-8")
    monkeypatch.setattr(_sp, "run", lambda *_a, **_k: _P())
    verdict, evidence = gh._ship_gate_verdict(tmp_path)
    assert verdict == "RED" and "1 hard-fail" in evidence


def test_ship_gate_row_fails_on_RED_carrying_a_hard_fail_organ(tmp_path, monkeypatch):
    """A hard-fail is never carryable -- no residual line disposes of one (ruling 2026-09-08)."""
    monkeypatch.setattr(gh, "_ship_gate_verdict",
                        lambda _root: ("RED", "1 hard-fail organ(s); 7 undispositioned WARN(s)"))
    assert gh._row_ship_gate(tmp_path).status == gh.PREFLIGHT_FAIL


def test_ship_gate_row_PASSES_on_RED_whose_only_reason_is_undispositioned_WARNs(tmp_path, monkeypatch):
    """The 2026-09-08 amendment: a handoff is not a release.

    GREEN is the TAG gate's criterion; demanding it at a CUT deadlocks any window with an open
    finding -- which is what the first live run of this preflight did. The row passes on
    `hard-fail = 0` and states the carried obligation, so the debt is inherited, not erased.
    """
    monkeypatch.setattr(gh, "_ship_gate_verdict",
                        lambda _root: ("RED", "ship-gate: RED -- not shipped-ready "
                                              "(4 new/undispositioned WARN(s))"))
    row = gh._row_ship_gate(tmp_path)
    assert row.status == gh.PREFLIGHT_PASS
    # The pass is only honest if the evidence line hands the seat the obligation AND the count.
    assert "4 undispositioned WARN(s) is named in the residual" in row.detail
    assert "DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08" in row.detail


def test_ship_gate_row_fails_on_a_RED_tail_it_cannot_read(tmp_path, monkeypatch):
    """Neither reason-count present: the hard-fail count is unestablished, so the row refuses.

    Without this leg the amendment would read every unparseable RED as `hard-fail = 0` and turn
    a widened row into a blind one.
    """
    monkeypatch.setattr(gh, "_ship_gate_verdict", lambda _root: ("RED", "RED -- reasons elided"))
    row = gh._row_ship_gate(tmp_path)
    assert row.status == gh.PREFLIGHT_FAIL and "cannot read" in row.detail


def test_ship_gate_row_fails_when_the_verdict_cannot_be_read(tmp_path, monkeypatch):
    """Unknown is not clean — the refusal direction this module already took for RM-8."""
    monkeypatch.setattr(gh, "_ship_gate_verdict", lambda _root: (None, "timed out after 900s"))
    row = gh._row_ship_gate(tmp_path)
    assert row.status == gh.PREFLIGHT_FAIL and "timed out" in row.detail


def test_ledger_row_fails_when_the_ledger_predates_the_window(tmp_path):
    root = _transport(tmp_path, ledger_date="2026-09-01")
    assert gh._row_ledger_refreshed(root, ".dev-knowledge", _TODAY).status == gh.PREFLIGHT_FAIL


def test_ratification_row_fails_when_the_windows_file_is_absent(tmp_path):
    root = _transport(tmp_path, ratification_date=None)
    row = gh._row_ratification_present(root, _TODAY)
    assert row.status == gh.PREFLIGHT_FAIL and f"RATIFICATION-{_TODAY}.md" in row.locator


def test_journal_row_fails_on_an_unanchored_spine_entry(tmp_path, monkeypatch):
    monkeypatch.setattr(gh, "_journal_spine_gaps", lambda _root: ["77322d48"])
    row = gh._row_journal_anchored(tmp_path)
    assert row.status == gh.PREFLIGHT_FAIL and "77322d48" in row.detail


def test_session_slug_matches_a_REAL_session_store_directory_name():
    """Pinned against a directory shape that ACTUALLY exists in this machine's session
    store, because an internally-consistent slug proves nothing: both sides of the comparison
    compute it, so a wrong rule agrees with itself while the row measures a path nobody writes
    to. That defect shipped here once -- an enumerated character class lost its literal
    backslash in transit, and the MEMORY row read `not present` against a file that was there.
    """
    assert (gh._session_slug(r"C:\Users\u\Documents\Dev\ai-council\.claude\worktrees\cli-provider")
            == "C--Users-u-Documents-Dev-ai-council--claude-worktrees-cli-provider")


def test_worktree_row_fails_only_the_CONJUNCTION_no_seat_and_already_merged(tmp_path,
                                                                             monkeypatch):
    """A tree whose work has LANDED and whose seat is gone is a leftover by construction."""
    monkeypatch.setattr(gh, "_linked_worktrees",
                        lambda _root: [str(tmp_path / "wt" / "lane-abandoned")])
    monkeypatch.setattr(gh, "_git", lambda *_a, **_k: "worktree-lane-abandoned")
    monkeypatch.setattr(gh, "_git_status", lambda *_a, **_k: (True, ""))   # merged into main
    sessions = tmp_path / "projects"
    sessions.mkdir()
    row = gh._row_worktree_owners(tmp_path, sessions_root=sessions)
    assert row.status == gh.PREFLIGHT_FAIL and "lane-abandoned" in row.detail


def test_worktree_row_does_not_call_an_UNMERGED_tree_abandoned(tmp_path, monkeypatch):
    """The seat-evidence leg alone false-FAILs a live lane: a background or subagent session
    files its transcript under its LAUNCHING cwd, so an actively-worked tree can have no project
    directory of its own. Measured 2026-09-08 against two trees that were both being worked."""
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [str(tmp_path / "wt" / "lane-live")])
    monkeypatch.setattr(gh, "_git", lambda *_a, **_k: "worktree-lane-live")
    monkeypatch.setattr(gh, "_git_status", lambda *_a, **_k: (False, ""))  # NOT merged
    sessions = tmp_path / "projects"
    sessions.mkdir()
    assert gh._row_worktree_owners(tmp_path, sessions_root=sessions).status == gh.PREFLIGHT_PASS


def test_worktree_row_passes_a_tree_with_a_live_owner(tmp_path, monkeypatch):
    wt = tmp_path / "wt" / "lane-live"
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [str(wt)])
    sessions = tmp_path / "projects"
    owner = sessions / gh._session_slug(wt)
    owner.mkdir(parents=True)
    (owner / "s.jsonl").write_text("{}\n", encoding="utf-8")
    assert gh._row_worktree_owners(tmp_path, sessions_root=sessions).status == gh.PREFLIGHT_PASS


# --- WIRING: a FAIL refuses the cut, a clean run does not --------------------------------

def _cut(repo, tmp_path, slug):
    return gh.generate(repo, mode="functional", slug=slug, repo=".dev-knowledge", date=_TODAY,
                       bundle_root=repo / "docs" / "handoffs", assemble=False)


def test_seeded_status_over_budget_refuses_the_cut(tmp_path, monkeypatch, _quiet_hub):
    """THE CLOSURE CRITERION, first half. One seeded FAIL — a 5,114-byte STATUS file — and the
    generator refuses, naming the row and its locator. Nothing is written."""
    repo = _hub_stub(tmp_path)
    monkeypatch.setattr(gh, "transport_root",
                        lambda **_kw: _transport(tmp_path, status_bytes=5_114))
    with pytest.raises(gh.PreflightError) as exc:
        _cut(repo, tmp_path, "0000-00-00-seeded")
    msg = str(exc.value)
    assert "status_byte_budget" in msg and "STATUS-integrator.md" in msg
    assert not (repo / "docs" / "handoffs" / "0000-00-00-seeded").exists()


def test_clean_transport_lets_the_cut_through(tmp_path, monkeypatch, _quiet_hub):
    """THE CLOSURE CRITERION, second half — the negative control. Same repo, same wiring, a
    clean window: the cut proceeds. Without this the refusal above proves only that the
    generator can be made to fail."""
    repo = _hub_stub(tmp_path)
    monkeypatch.setattr(gh, "transport_root", lambda **_kw: _transport(tmp_path))
    res = _cut(repo, tmp_path, "0000-00-00-clean")
    assert (res.bundle_dir / "FUNCTIONAL_BOOT.md").exists()


def test_refusal_names_EVERY_failing_row_not_just_the_first(tmp_path, monkeypatch, _quiet_hub):
    """Same reason `assert_boundary_hygiene` names every leftover: reporting one invites a
    fix-and-retry loop that reveals the next."""
    repo = _hub_stub(tmp_path)
    monkeypatch.setattr(gh, "transport_root",
                        lambda **_kw: _transport(tmp_path, status_bytes=5_114,
                                                 ledger_date="2026-09-01",
                                                 ratification_date=None))
    with pytest.raises(gh.PreflightError) as exc:
        _cut(repo, tmp_path, "0000-00-00-many")
    msg = str(exc.value)
    assert "status_byte_budget" in msg and "ledger_refreshed" in msg
    assert "ratification_present" in msg


def test_preflight_is_hub_scoped_so_a_cross_repo_cut_is_not_judged_by_this_window(tmp_path):
    """Hub-only by repo identity — the same scoping `audit.check_journal_spine_anchor` already
    declares for ADR-85's floor. A consumer carries neither this transport window nor these
    stamped docs, so scanning it would manufacture a fleet gap."""
    repo = _hub_stub(tmp_path)
    rows = gh.preflight_rows(repo, transport=None, today=_TODAY)
    assert {r.status for r in rows} == {gh.PREFLIGHT_NA}
    assert all("NOT-APPLICABLE" in r.detail for r in rows)


def test_unresolvable_transport_is_a_REFUSAL_not_a_pass(tmp_path, monkeypatch, _quiet_hub):
    """An unknown boundary is not a clean one (RM-8). A seat whose CLAUDE_PROMPTS_DIR is stale
    reads an EMPTY `to-cc/` as "nothing filed" — DEFECT E-29 — and a preflight that passed on
    an unresolved transport would report exactly that false safety."""
    repo = _hub_stub(tmp_path)
    monkeypatch.setattr(gh, "transport_root", lambda **_kw: None)
    with pytest.raises(gh.PreflightError) as exc:
        _cut(repo, tmp_path, "0000-00-00-notransport")
    assert "transport" in str(exc.value)


def test_transport_root_prefers_the_env_var_over_the_downloads_fallback(tmp_path):
    """OPERATOR-INTERFACE §1: THE VARIABLE IS THE SOURCE; `~/Downloads` is the fallback."""
    d = tmp_path / "drive"
    (d / "to-browser").mkdir(parents=True)
    assert gh.transport_root(env={"CLAUDE_PROMPTS_DIR": str(d)}) == d
    assert gh.transport_root(env={}, downloads=tmp_path / "nope") is None
