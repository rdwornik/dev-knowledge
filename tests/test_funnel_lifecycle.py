"""Tests for the FM-2 funnel-lifecycle detector and its audit adapter.

RED-FIRST, AND THE TWO REDS MEAN DIFFERENT THINGS. The contract asks for both and they prove
different properties:

  1. Against the LIVE tree -- `test_live_tree_reproduces_the_census_finding` refuses to pass
     unless the detector sees the two CONSUMED-but-unarchived intakes the 2026-08-29 census
     (`docs/audits/2026-08-29-census-nb2-funnel.md` section 3.2) named as decision candidates
     and the wave-2 GO then ruled terminal. That is the proof of TEETH: two instruments, one
     reality. It is written to fail loudly the day the detector stops seeing them for the
     WRONG reason, and `test_live_tree_leg_a1_is_location_sensitive` is its twin -- it proves
     the same objects stop being violations once they are relocated, so the leg is measuring
     LOCATION and not merely reading a status word.
  2. Seeded and hermetic -- every `tmp_path` test below builds a synthetic tree, asserts the
     violation, then removes exactly the defect and asserts it is gone. A green assertion that
     never went red proves the assertion runs, not that it discriminates.

EVERY ADMISSION HAS A REFUSAL TWIN. The failure mode a lifecycle gate falls into is passing
because it looked where the defect never was, so each leg is tested for what it must NOT flag:
an ACCEPTED doc that is deliberately live, an archived doc that is correctly archived, a
pre-cutoff row with a dangling ref, a READY doc under the threshold.
"""
from __future__ import annotations

import datetime as _dt
import subprocess
from pathlib import Path

import pytest

import funnel_lifecycle as fl


REPO_ROOT = Path(__file__).resolve().parents[1]


# --- synthetic-tree helpers -------------------------------------------------------

def _write_lf(path: Path, text: str) -> None:
    """Write with LF endings, always.

    `Path.write_text` applies universal newlines and launders every `\\n` into `\\r\\n` on
    Windows. `gen_task_tree._FM_ID_RE` is `^id: "\\[#(\\d+)\\]"$` under `re.MULTILINE`, where `$`
    matches before `\\n` -- so a CRLF line ends `..."\\r` and the id does NOT parse. The whole
    fixture corpus was silently id-less until leg (c)'s Z-G4 raise made it visible: before
    that, `frontmatter_id() is None` was a `continue`, so every row-shaped test was scoring an
    EMPTY row set and passing. `tasks/` is pure LF by contract, so the fixtures must be too.
    """
    path.write_bytes(text.encode("utf-8"))


def _intake(dirpath: Path, name: str, *, intake_id: str, status: str, **extra: str) -> Path:
    dirpath.mkdir(parents=True, exist_ok=True)
    lines = ["---", f"intake-id: {intake_id}", f"status: {status}"]
    # Values are QUOTED. A live `consumed-by:` opens with `[#446]`, and an unquoted `[` is a
    # YAML flow-sequence opener -- the parse fails, `_parse_frontmatter` returns {}, and the
    # doc trips the Z-G4 leg instead of the one under test. Same class as the backtick opener
    # that broke six live intakes (census D1); caught here by the fixture doing it wrong first.
    lines += [f'{k.replace("_", "-")}: "{v}"' for k, v in extra.items()]
    lines += ["---", "", f"# {name}", ""]
    p = dirpath / name
    _write_lf(p, "\n".join(lines))
    return p


def _row(root: Path, rid: int, *, status: str = "open", body: str | None = None) -> Path:
    tasks = root / "tasks"
    tasks.mkdir(parents=True, exist_ok=True)
    body = body if body is not None else f"- [#{rid}] [P2][M] **Row {rid}** · refs ADR-100"
    text = (f'---\nid: "[#{rid}]"\ntitle: "Row {rid}"\nstatus: {status}\n'
            f"generates: BACKLOG.md\n---\n\n{body}\n")
    p = tasks / f"{rid}-row-{rid}.md"
    _write_lf(p, text)
    return p


def _adr(root: Path, number: int, *, status: str, archived: bool = False) -> Path:
    d = root / "docs" / "decisions" / ("archive" if archived else "")
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"ADR-{number}-synthetic.md"
    _write_lf(p, f"# ADR-{number}: synthetic\n\n- **Status:** {status}\n")
    return p


@pytest.fixture()
def tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A minimal governed tree with the git birth-date lookup stubbed to "everything is old".

    The stub is the DEFAULT so a leg-(c) test states its own dates explicitly; the real git
    path has its own test below (`test_row_birth_dates_reads_real_git`) so stubbing here never
    means the git leg is untested.
    """
    (tmp_path / "docs" / "intake").mkdir(parents=True)
    (tmp_path / "docs" / "intake" / "archive").mkdir(parents=True)
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    (tmp_path / "tasks").mkdir(parents=True)
    (tmp_path / "protocols").mkdir(parents=True)
    _adr(tmp_path, 1, status="Accepted")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {
        p.relative_to(root).as_posix(): "2026-01-01"
        for p in (root / "tasks").glob("*.md")})
    return tmp_path


def _legs(m: fl.Measurement, leg: str) -> list[str]:
    return [v.subject for v in m.by_leg(leg)]


# --- leg a1: a terminal intake that never left docs/intake/ -----------------------

@pytest.mark.parametrize("status", sorted(fl.TERMINAL_INTAKE_STATUSES))
def test_a1_flags_every_terminal_status_at_depth_1(tree: Path, status: str):
    _intake(tree / "docs" / "intake", "2026-08-01-tech-x.md", intake_id="7", status=status)
    assert _legs(fl.measure(tree), fl.LEG_A1) == ["docs/intake/2026-08-01-tech-x.md"]


@pytest.mark.parametrize("status", ["SEED", "DRAFT", "READY", "ACCEPTED"])
def test_a1_refuses_to_flag_a_live_status(tree: Path, status: str):
    """The refusal twin. ACCEPTED is the load-bearing one: `docs/intake/README.md` section 5
    keeps it OUT of the terminal set on purpose -- "a standing authority must stay visible
    live" -- so a leg that flagged it would be enforcing the opposite of the ruling."""
    _intake(tree / "docs" / "intake", "2026-08-01-tech-x.md", intake_id="7", status=status)
    assert _legs(fl.measure(tree), fl.LEG_A1) == []


def test_a1_is_right_either_way_when_the_doc_is_relocated(tree: Path):
    """The contract's own ask: the check must be right whether lane J has relocated the doc
    or not. Same file, same terminal status, different HOME -- and only the unarchived one is
    a violation. This is what makes leg a1 a LOCATION check rather than a status reader."""
    live = _intake(tree / "docs" / "intake", "2026-08-01-tech-x.md",
                   intake_id="7", status="CONSUMED")
    assert _legs(fl.measure(tree), fl.LEG_A1) == ["docs/intake/2026-08-01-tech-x.md"]

    archived = tree / "docs" / "intake" / "archive" / live.name
    archived.write_bytes(live.read_bytes())        # byte-identical, as the ruling requires
    live.unlink()
    m = fl.measure(tree)
    assert _legs(m, fl.LEG_A1) == []
    assert m.archived_intakes == 1 and m.live_intakes == 0


# --- leg a2: ACCEPTED, but every row it names is done ------------------------------

def test_a2_flags_accepted_whose_named_rows_are_all_terminal(tree: Path):
    _row(tree, 500, status="closed")
    _row(tree, 501, status="superseded")
    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="ADR-110 (header); [#500] closed; [#501] superseded")
    assert _legs(fl.measure(tree), fl.LEG_A2) == ["docs/intake/2026-08-01-func-y.md"]


def test_a2_refuses_when_one_named_row_is_still_open(tree: Path):
    _row(tree, 500, status="closed")
    _row(tree, 501, status="open")
    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="[#500] closed; [#501] open")
    assert _legs(fl.measure(tree), fl.LEG_A2) == []


def test_a2_refuses_the_vacuous_case_of_an_accepted_doc_naming_no_row(tree: Path):
    """`all(...)` over an EMPTY set is True. Without the ">= 1 named row" bar this leg would
    flag every ACCEPTED standing authority in the folder -- the intake #28 / ADR-112 class,
    which is HELD live on purpose."""
    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="ADR-112 section A")
    assert _legs(fl.measure(tree), fl.LEG_A2) == []


def test_a2_refuses_when_a_named_row_is_not_in_this_tree(tree: Path):
    """A row id this tree does not carry says nothing about terminality; guessing would turn a
    stale citation into a status verdict."""
    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="[#99999] closed")
    assert _legs(fl.measure(tree), fl.LEG_A2) == []


# --- leg b: a terminal ADR that never left docs/decisions/ -------------------------

@pytest.mark.parametrize("status", sorted(fl._vas.TERMINAL_STATUSES))
def test_b_flags_a_terminal_adr_at_depth_1(tree: Path, status: str):
    _adr(tree, 52, status=status)
    assert _legs(fl.measure(tree), fl.LEG_B) == ["docs/decisions/ADR-52-synthetic.md"]


def test_b_refuses_an_accepted_adr_and_an_already_archived_terminal_one(tree: Path):
    _adr(tree, 53, status="Accepted")
    _adr(tree, 52, status="Superseded", archived=True)
    assert _legs(fl.measure(tree), fl.LEG_B) == []


def test_b_binds_to_the_ruled_constant_not_a_local_copy():
    """The terminal set is `validate_adr_status.TERMINAL_STATUSES`. Re-declaring it here would
    let the two drift, and a check enforcing a stale enum is worse than none."""
    assert frozenset({"Superseded", "Deprecated"}) == fl._vas.TERMINAL_STATUSES


# --- leg c: post-cutoff row provenance --------------------------------------------

def test_c_flags_a_post_cutoff_row_with_no_refs_clause(tree: Path,
                                                       monkeypatch: pytest.MonkeyPatch):
    _row(tree, 700, body="- [#700] [P2][M] **No provenance at all**")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == ["[#700] tasks/700-row-700.md"]


def test_c_flags_a_post_cutoff_row_whose_every_token_dangles(tree: Path,
                                                             monkeypatch: pytest.MonkeyPatch):
    _row(tree, 700, body="- [#700] [P2][M] **Dangling** · refs N4-F1/F6, #99999, ADR-9999")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == ["[#700] tasks/700-row-700.md"]


def test_c_passes_when_one_token_resolves(tree: Path, monkeypatch: pytest.MonkeyPatch):
    """ONE resolving token is the bar, matching the census's backward direction. The seeded
    RED above and this GREEN differ by exactly the `ADR-1` token."""
    _row(tree, 700, body="- [#700] [P2][M] **Mixed** · refs N4-F1, #99999, ADR-1")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == []


def test_c_grandfathers_a_dated_pre_cutoff_row(tree: Path, monkeypatch: pytest.MonkeyPatch):
    _row(tree, 35, body="- [#35] [P2][M] **Old and dangling** · refs coherence-audit")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/35-row-35.md": "2026-07-27"})
    m = fl.measure(tree)
    assert _legs(m, fl.LEG_C) == [] and m.post_cutoff_rows == 0


def test_c_treats_an_undated_row_as_in_scope(tree: Path, monkeypatch: pytest.MonkeyPatch):
    """Absence of evidence buys no exemption. A row git cannot date is evaluated, not waved
    through -- the same direction Z-G4 points, applied to the cutoff rather than the rule."""
    _row(tree, 700, body="- [#700] [P2][M] **Undated and dangling** · refs N4-F1")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {})
    m = fl.measure(tree)
    assert _legs(m, fl.LEG_C) == ["[#700] tasks/700-row-700.md"] and m.post_cutoff_rows == 1


def test_c_does_not_resolve_a_bare_hash_against_the_intake_namespace(tree: Path,
                                                                    monkeypatch: pytest.MonkeyPatch):
    """Both id namespaces start at 1 (census section 4.2: 8 open rows sit on that ambiguity).
    A FAIL-armed leg must not try a token two ways until one works, so `#8` naming an intake
    and no row stays UNRESOLVED -- while the explicit `intake #8` form resolves."""
    _intake(tree / "docs" / "intake", "2026-08-01-tech-z.md", intake_id="8", status="READY")
    _row(tree, 700, body="- [#700] [P2][M] **Ambiguous** · refs #8")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == ["[#700] tasks/700-row-700.md"]

    _row(tree, 700, body="- [#700] [P2][M] **Explicit** · refs intake #8")
    assert _legs(fl.measure(tree), fl.LEG_C) == []


def test_c_cutoff_is_the_consumer_at_landing_constant():
    """One cutoff, one constant. Two legs grandfathering the same corpus by two dates would
    diverge silently the first time either moved."""
    assert fl.ARM_DATE is fl._cal.ARM_DATE


def test_row_birth_dates_reads_real_git(tmp_path: Path):
    """The one test that exercises the real subprocess, so the stub elsewhere never means the
    git path is unproven."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    _row(tmp_path, 700)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "row"], cwd=tmp_path, check=True)
    births = fl._row_birth_dates(tmp_path)
    assert births["tasks/700-row-700.md"] == _dt.date.today().isoformat()


def test_row_birth_dates_raises_outside_a_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Z-G4: a cutoff that cannot be computed is a FAIL, never a leg that quietly grandfathers
    the whole corpus -- which is what an empty dict would have done."""
    monkeypatch.setattr(fl.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
        a[0] if a else [], 128, "", "not a git repository"))
    with pytest.raises(fl.LifecycleUnreadable, match="uncomputable"):
        fl._row_birth_dates(tmp_path)


# --- leg d: READY past a RULED threshold ------------------------------------------

def _rule_threshold(tree: Path, days: int) -> None:
    _write_lf((tree / "protocols" / "FUNNEL.md"), 
        f"# Funnel\n\n- **READY threshold: {days} days**\n")


def test_d_is_inert_and_says_so_when_no_threshold_is_ruled(tree: Path):
    """FM-1 rules the number. Absent, the leg reports a GAP and arms nothing. It does NOT
    FAIL: Z-G4 governs a check that cannot compute the ground truth of a rule that EXISTS,
    and a threshold nobody ruled is not a constant this gate may invent."""
    _intake(tree / "docs" / "intake", "2020-01-01-tech-ancient.md", intake_id="9", status="READY")
    m = fl.measure(tree)
    assert m.threshold_days is None and _legs(m, fl.LEG_D) == []
    statuses = fl.findings(m)
    # The assertion is that NO finding is a fail -- not that the status tuple differs from one
    # arbitrary pair, which was the first version and would have passed on
    # [("fail", ...), ("warn", "NOT ARMED")] (terra pass 1, HIGH-13).
    assert [s for s, _ in statuses] == ["warn"]
    gap = [e for s, e in statuses if "NOT ARMED" in e]
    assert len(gap) == 1 and "1 READY intake(s) went unexamined" in gap[0]


def test_d_arms_the_moment_a_threshold_is_ruled(tree: Path):
    """The same tree, the same doc, one ruled constant -- and the leg starts discriminating.
    This is the seam FM-1 lands into."""
    _intake(tree / "docs" / "intake", "2020-01-01-tech-ancient.md", intake_id="9", status="READY")
    _rule_threshold(tree, 30)
    m = fl.measure(tree, today=_dt.date(2026, 8, 29))
    assert m.threshold_days == 30
    assert m.threshold_locator == "protocols/FUNNEL.md:3"
    assert _legs(m, fl.LEG_D) == ["docs/intake/2020-01-01-tech-ancient.md"]
    assert all(s == "warn" for s, _ in fl.findings(m)), "leg d is WARN-tier by the contract"


def test_d_refuses_a_doc_under_the_threshold_and_one_carrying_a_review_date(tree: Path):
    _rule_threshold(tree, 30)
    _intake(tree / "docs" / "intake", "2026-08-20-tech-recent.md", intake_id="9", status="READY")
    _intake(tree / "docs" / "intake", "2020-01-01-tech-ruled.md", intake_id="10",
            status="READY", review_date="2026-12-01")
    assert _legs(fl.measure(tree, today=_dt.date(2026, 8, 29)), fl.LEG_D) == []


def test_d_reads_the_threshold_only_from_protocols(tree: Path):
    """Scoped on purpose: if any file could arm it, an audit draft or a scratch note would."""
    (tree / "docs").mkdir(exist_ok=True)
    _write_lf((tree / "docs" / "note.md"), "READY threshold: 1 days\n")
    assert fl.ready_threshold(tree) == (None, None)


def test_d_threshold_regex_accepts_the_declared_shapes():
    for text, expected in (("READY threshold: 30 days", 30),
                           ("- **intake READY threshold: 45 days**", 45),
                           ("READY-age threshold = 7 day", 7)):
        assert fl._READY_THRESHOLD_RE.search(text).group("days") == str(expected)


# --- terra pass 1: the thirteen HIGH findings, each with its own regression -------

def test_a2_does_not_read_an_intake_id_as_a_row_id(tree: Path):
    """HIGH-1. `consumed-by: "intake #28"` names INTAKE 28; the loose `\\[?#(\\d+)\\]?` form also
    matched it, so an ACCEPTED doc would have been judged against ROW 28's status. Leg a2 takes
    the bracketed form only -- the shape the contract names."""
    _row(tree, 28, status="closed")
    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="intake #28 section A")
    assert _legs(fl.measure(tree), fl.LEG_A2) == []

    _intake(tree / "docs" / "intake", "2026-08-01-func-y.md", intake_id="8", status="ACCEPTED",
            consumed_by="[#28] closed")
    assert _legs(fl.measure(tree), fl.LEG_A2) == ["docs/intake/2026-08-01-func-y.md"]


def test_replay_preserves_a_birth_date_across_a_rename():
    """HIGH-2. `gen_task_tree` derives the filename slug from the TITLE, so a title edit
    renames the row. `--diff-filter=A` drops renames, leaving the row UNDATED -- which is in
    scope -- so a legitimate pre-cutoff row could be FAILed for having been retitled."""
    events = [("2026-08-28", ["R100", "tasks/1-old.md", "tasks/1-new.md"]),
              ("2026-07-01", ["A", "tasks/1-old.md"])]          # newest-first, as git emits
    assert fl.replay_path_events(events) == {"tasks/1-new.md": "2026-07-01"}


def test_replay_takes_the_newest_add_after_a_delete():
    """HIGH-4. Added pre-cutoff, deleted, re-added post-cutoff is NEW work wearing an old
    date. "Oldest add wins" grandfathered it out of leg (c) entirely."""
    events = [("2026-08-28", ["A", "tasks/1-x.md"]),
              ("2026-08-01", ["D", "tasks/1-x.md"]),
              ("2026-07-01", ["A", "tasks/1-x.md"])]
    assert fl.replay_path_events(events) == {"tasks/1-x.md": "2026-08-28"}


def test_replay_forgets_a_deleted_path():
    events = [("2026-08-28", ["D", "tasks/1-x.md"]), ("2026-07-01", ["A", "tasks/1-x.md"])]
    assert fl.replay_path_events(events) == {}


def test_parse_name_status_reads_dates_and_rename_pairs():
    out = "\x002026-08-28\nR100\ttasks/1-old.md\ttasks/1-new.md\n\x002026-07-01\nA\ttasks/1-old.md\n"
    assert fl.parse_name_status(out) == [
        ("2026-08-28", ["R100", "tasks/1-old.md", "tasks/1-new.md"]),
        ("2026-07-01", ["A", "tasks/1-old.md"]),
    ]


def test_c_resolves_a_stem_that_lives_in_an_archive(tree: Path,
                                                    monkeypatch: pytest.MonkeyPatch):
    """HIGH-3. An archived object is still valid provenance. The stem walk went one level deep
    into `docs/intake/` and `docs/decisions/` and never entered their `archive/` children, so a
    row citing an archived intake's stem resolved to nothing and leg (c) falsely FAILed."""
    _intake(tree / "docs" / "intake" / "archive", "2026-07-01-tech-gone.md",
            intake_id="3", status="CONSUMED")
    _row(tree, 700, body="- [#700] [P2][M] **Cites the archive** · refs 2026-07-01-tech-gone")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == []


def test_c_refuses_a_path_token_that_escapes_the_repo(tree: Path,
                                                      monkeypatch: pytest.MonkeyPatch):
    """HIGH-11. `../outside.md` reaches a sibling checkout on the operator's disk;
    `Path.exists()` says True and the row passes on provenance THIS repo does not carry."""
    _write_lf((tree.parent / "outside.md"), "x")
    _row(tree, 700, body="- [#700] [P2][M] **Escapes** · refs ../outside.md")
    monkeypatch.setattr(fl, "_row_birth_dates", lambda root: {"tasks/700-row-700.md": "2026-08-28"})
    assert _legs(fl.measure(tree), fl.LEG_C) == ["[#700] tasks/700-row-700.md"]


def test_refs_clause_stops_at_the_end_of_its_own_line():
    """HIGH-12. With `re.S` and a `\\s*$` tail the clause ran past its line and swallowed
    following prose, so a row whose refs all dangled PASSED on a token mentioned three lines
    later -- silent false coverage, the exact failure leg (c) exists to refuse."""
    body = "- [#700] **Row** · refs N4-F1\nSome later prose mentioning ADR-1 and scripts/audit.py\n"
    assert fl.refs_clause(body) == "N4-F1"


def test_zg4_off_enum_and_missing_intake_status_raise(tree: Path):
    """HIGH-6. Both yielded a doc that matched no leg and vanished from a1/a2/d in silence."""
    p = tree / "docs" / "intake" / "2026-08-01-tech-x.md"
    _write_lf(p, "---\nintake-id: 7\norigin: x\n---\n\n# x\n")
    with pytest.raises(fl.LifecycleUnreadable, match="carries no status"):
        fl.measure(tree)
    _write_lf(p, "---\nintake-id: 7\nstatus: WIBBLE\n---\n\n# x\n")
    with pytest.raises(fl.LifecycleUnreadable, match="outside the ruled enum"):
        fl.measure(tree)


def test_zg4_row_without_a_parseable_id_raises(tree: Path):
    """HIGH-7. The row was dropped before its body was read, so it left leg (c)'s DENOMINATOR
    as well as its numerator and the leg passed over it in silence."""
    _write_lf((tree / "tasks" / "700-noid.md"), 
        "---\ntitle: x\nstatus: open\n---\n\n- **no id** · refs ADR-1\n")
    with pytest.raises(fl.LifecycleUnreadable, match="no parseable"):
        fl.measure(tree)


def test_zg4_undecodable_bytes_raise(tree: Path):
    """HIGH-5. `errors="replace"` turns `CONSUM\\xffED` into a string that is simply not in the
    terminal set, and the doc passes -- a verdict manufactured out of damage."""
    (tree / "docs" / "intake" / "2026-08-01-tech-x.md").write_bytes(
        b"---\nintake-id: 7\nstatus: CONSUM\xffED\n---\n\n# x\n")
    with pytest.raises(fl.LifecycleUnreadable, match="undecodable"):
        fl.measure(tree)


def test_zg4_an_adr_with_no_status_field_raises(tree: Path):
    """HIGH-8. `scan_zone` returns `missing` separately, in its own words, "so a caller cannot
    mistake an absent field for a clean one" -- and the first draft discarded it."""
    _write_lf((tree / "docs" / "decisions" / "ADR-99-nostatus.md"), 
        "# ADR-99: no status line here\n")
    with pytest.raises(fl.LifecycleUnreadable, match="cannot read a status"):
        fl.measure(tree)


@pytest.mark.parametrize("gone", ["docs/intake", "docs/decisions", "tasks"])
def test_zg4_a_deleted_corpus_directory_raises(tree: Path, gone: str):
    """HIGH-9. `check_intake_tree_coherence`'s ruling, one level out: "a coherence gate must
    not be satisfiable by deleting what it checks". An absent corpus is a failed computation,
    never an empty set that reports clean."""
    import shutil

    shutil.rmtree(tree / gone)
    with pytest.raises(fl.LifecycleUnreadable, match="is absent at"):
        fl.measure(tree)


def test_d_names_a_ready_doc_whose_age_it_cannot_compute(tree: Path):
    """HIGH-10. Silence about an unmeasurable doc is indistinguishable from "under the
    threshold". Reported at leg (d)'s own WARN tier -- a naming defect belongs to the naming
    organ, not to a hard refusal here."""
    _rule_threshold(tree, 30)
    _write_lf((tree / "docs" / "intake" / "undated-ready.md"), 
        "---\nintake-id: 9\nstatus: READY\n---\n\n# x\n")
    m = fl.measure(tree, today=_dt.date(2026, 8, 29))
    assert _legs(m, fl.LEG_D) == ["docs/intake/undated-ready.md"]
    assert all(s == "warn" for s, _ in fl.findings(m))


# --- Z-G4: cannot compute -> raise, never a verdict --------------------------------

def test_zg4_empty_frontmatter_parse_raises(tree: Path):
    """The D1 defect, made loud. `gen_intake_index._parse_frontmatter` returns {} on malformed
    YAML by design, and six live docs lost id AND status that way while
    `intake-index-freshness` stayed green -- a regen-and-diff gate reproduces a wrong index
    byte-for-byte. A doc whose status cannot be read is not a doc with no status."""
    bad = tree / "docs" / "intake" / "2026-08-27-tech-broken.md"
    _write_lf(bad, "---\nintake-id: 56\nstatus: READY\nconsumers: `docs/audits/x.md`\n---\n\n# x\n")
    with pytest.raises(fl.LifecycleUnreadable, match=r"parsed to \{\}"):
        fl.measure(tree)


def test_zg4_unreadable_file_raises(tree: Path, monkeypatch: pytest.MonkeyPatch):
    """The patched seam is `read_bytes`, and naming it matters. An earlier version patched
    `read_text` -- which `_read` stopped using when it went strict -- so the raise it caught
    was `validate_adr_status.scan_zone`'s, three legs away from the one under test. It passed,
    green, testing something else: the shape terra pass 1 called out at HIGH-13, found once
    more by re-reading the assertion instead of the result."""
    _intake(tree / "docs" / "intake", "2026-08-01-tech-x.md", intake_id="7", status="READY")
    monkeypatch.setattr(fl.Path, "read_bytes",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("boom")))
    with pytest.raises(fl.LifecycleUnreadable, match=r"unreadable: .*2026-08-01-tech-x\.md"):
        fl.measure(tree)


def test_zg4_unrecoverable_row_body_raises(tree: Path):
    _write_lf(tree / "tasks" / "700-broken.md", '---\nid: "[#700]"\nstatus: open\n')
    with pytest.raises(fl.LifecycleUnreadable, match="row body unreadable"):
        fl.measure(tree)


def test_zg4_no_leg_returns_a_skip_or_an_unavailable_status(tree: Path):
    """`unavailable` renders as N/A and projects onto `pass` in `_check_outcome` -- the
    green-by-skip class the 2026-08-25 sweep closed. Every verdict this module emits is one of
    pass/warn/fail."""
    _intake(tree / "docs" / "intake", "2026-08-01-tech-x.md", intake_id="7", status="CONSUMED")
    assert {s for s, _ in fl.findings(fl.measure(tree))} <= {"pass", "warn", "fail"}


# --- verdict shape ----------------------------------------------------------------

def test_one_finding_per_violation_never_a_bundle(tree: Path):
    """The #147 register suppresses an ENTIRE Finding on a substring match, so a bundled
    Finding would let one relocated intake wave through every other violation beside it."""
    _intake(tree / "docs" / "intake", "2026-08-01-a.md", intake_id="7", status="CONSUMED")
    _intake(tree / "docs" / "intake", "2026-08-02-b.md", intake_id="8", status="REJECTED")
    _adr(tree, 52, status="Superseded")
    fails = [e for s, e in fl.findings(fl.measure(tree)) if s == "fail"]
    assert len(fails) == 3


def test_a_clean_tree_passes_with_its_numbers_in_the_evidence(tree: Path):
    _intake(tree / "docs" / "intake", "2026-08-01-a.md", intake_id="7", status="READY")
    _rule_threshold(tree, 3650)
    _row(tree, 700)
    verdicts = fl.findings(fl.measure(tree, today=_dt.date(2026, 8, 29)))
    assert [s for s, _ in verdicts] == ["pass"]
    assert "1 live + 0 archived intake(s)" in verdicts[0][1]


def test_render_report_is_fenced(tree: Path):
    """CLAUDE.md section 4 render-layer rule: operator-copied output is flat and fenced, so the
    TUI cannot paint box-drawing borders into it."""
    text = fl.render_report(fl.measure(tree))
    assert text.startswith("```\n") and text.endswith("\n```")


# --- the live tree: the census overlap --------------------------------------------

#: The two intake docs `docs/audits/2026-08-29-census-nb2-funnel.md` section 3.2 named as
#: decision candidates and the 2026-08-29 wave-2 GO then ruled terminal (SEED -> CONSUMED and
#: ACCEPTED -> CONSUMED). Named by STEM, because lane J relocates them into
#: `docs/intake/archive/` in this same wave and the directory is exactly what changes.
_CENSUS_RULED_TERMINAL = (
    "2026-07-27-func-operator-design-input-night-shift-handoff-reform.md",
    "2026-08-06-func-parallel-execution-system.md",
)


def test_live_tree_reproduces_the_census_finding():
    """RED #1 -- the proof of teeth, against the real repo rather than a fixture.

    `docs/audits/2026-08-29-census-nb2-funnel.md` section 3.2 listed THREE intake docs as
    "requires a status ruling first": #19, #26, #28. The wave-2 GO ruled #19 and #26 to
    CONSUMED and HELD #28 per ADR-112.

    NO SKIP BRANCH, deliberately. Lane J relocates these two in this same wave, so the naive
    assertion "leg a1 flags both" goes red for an innocent reason after that merge -- and the
    obvious repair, `pytest.skip` when the list is empty, is the green-by-skip class this repo
    spent a sweep removing: it would also pass against a detector that had gone completely
    blind. The invariant that holds BOTH BEFORE AND AFTER the relocation is that each ruled
    doc is EITHER flagged by leg a1 OR sitting in the archive -- never neither, which is the
    only outcome that means the funnel leaked.
    """
    m = fl.measure(REPO_ROOT)
    flagged = {Path(s).name for s in _legs(m, fl.LEG_A1)}
    archived = {d.path.name for d in
                fl.read_intake_dir(REPO_ROOT / fl.INTAKE_ARCHIVE_RELPATH, REPO_ROOT)}
    for stem in _CENSUS_RULED_TERMINAL:
        assert stem in flagged or stem in archived, (
            f"{stem} is terminal by the wave-2 GO's ruling and is neither flagged by leg a1 "
            f"nor archived -- the leg has no teeth")
        assert not (stem in flagged and stem in archived), f"{stem} is in two places at once"
    assert not any("2026-08-08-func-skills-tier" in s for s in flagged), (
        "intake #28 is HELD at ACCEPTED per ADR-112 and must not be flagged")


def test_live_tree_leg_a1_is_location_sensitive():
    """The twin of the test above, and the half that survives lane J's relocation: every doc
    already in `docs/intake/archive/` is terminal AND is not a violation. Together the pair
    pins that leg a1 keys on LOCATION x STATUS, not on either alone."""
    archived = fl.read_intake_dir(REPO_ROOT / fl.INTAKE_ARCHIVE_RELPATH, REPO_ROOT)
    assert archived, "the archive is the control group; an empty one proves nothing"
    assert all(d.status in fl.TERMINAL_INTAKE_STATUSES for d in archived)
    flagged = set(_legs(fl.measure(REPO_ROOT), fl.LEG_A1))
    assert not any(d.relpath in flagged for d in archived)


def test_live_tree_leg_c_measures_zero_so_arming_cannot_red_a_clean_tree():
    """The arming evidence, re-measured rather than quoted. Leg (c) is FAIL-armed only because
    the post-cutoff corpus measures 0 -- the `check_adr_status_grammar` /
    `consumer_at_landing` bar. If this ever REDs, the leg is blocking work for debt somebody
    else created, which is how a gate gets routed around."""
    m = fl.measure(REPO_ROOT)
    assert m.post_cutoff_rows > 0, "a vacuous scope would make the zero meaningless"
    assert _legs(m, fl.LEG_C) == []


def test_live_tree_leg_b_measures_zero_and_the_reason_is_recorded():
    """0 by measurement, not by inertia: `validate_adr_status`'s own docstring records that
    Superseded/Deprecated are carried by ZERO live ADRs, and the two that ARE terminal live in
    `docs/decisions/archive/` -- so this leg is armed against a corpus at zero and the archive
    relocation for ADRs is genuinely clean."""
    m = fl.measure(REPO_ROOT)
    assert _legs(m, fl.LEG_B) == []
    assert m.live_adrs >= 80


# --- the audit adapter ------------------------------------------------------------

def test_adapter_is_registered_and_declares_a_ship_tier():
    """SHIP-tier is a DECLARED exception to the assignment rule at the head of ALL_CHECKS, not
    an oversight: this check is FAIL-capable, and leg a1 FAILs on live main by design. A
    COMMIT tier would wedge every commit in every lane on a defect the committing session
    cannot legally repair (clearing it means RELOCATING a governed document)."""
    import audit as aud
    from audit_checks.registry import CHECK_ORDER

    assert aud.check_funnel_lifecycle in aud.ALL_CHECKS
    assert aud.tier_of(aud.check_funnel_lifecycle) == aud.TIER_SHIP
    assert "check_funnel_lifecycle" in CHECK_ORDER
    assert tuple(c.__name__ for c in aud.ALL_CHECKS) == CHECK_ORDER


def test_adapter_does_not_run_at_the_commit_gate_but_does_at_ship():
    """The whole point of the tier. `cmd_health` -- the `audit-health` pre-commit hook --
    invokes `run_checks(tier=TIER_COMMIT)`, and the ladder is nested, so ship runs both."""
    import audit as aud

    assert not aud.runs_at_tier(aud.check_funnel_lifecycle, aud.TIER_COMMIT)
    assert aud.runs_at_tier(aud.check_funnel_lifecycle, aud.TIER_SHIP)


def test_adapter_is_na_off_hub(tmp_path: Path):
    """Hub-only by REPO IDENTITY, never by the presence of docs/intake/. corp-monorepo and
    ai-council both carry one while carrying none of the doctrine ([#383]'s measured lesson),
    so keying off the folder would manufacture a fleet gap that does not exist."""
    import audit as aud

    (tmp_path / "docs" / "intake").mkdir(parents=True)
    out = aud.check_funnel_lifecycle(tmp_path)
    assert [f.status for f in out] == ["n/a"]
    assert "NOT-APPLICABLE" in out[0].evidence


def test_the_adapter_and_this_test_file_hold_two_module_objects():
    """A dual-import fact, pinned rather than discovered. `audit.py` binds
    `scripts.funnel_lifecycle`; a bare `import funnel_lifecycle` binds a SECOND module object
    with a SECOND `LifecycleUnreadable` class -- `check_funnel_coverage` and its own test file
    sit in exactly this position. Nothing at runtime compares them, so it is harmless; the
    trap is a test that raises the test-module's exception at the adapter and concludes the
    `except` clause is unreachable. Caught that way here, so the next reader is told instead."""
    import audit as aud

    assert aud._fl is not fl and aud._fl.__name__ == "scripts.funnel_lifecycle"
    assert aud._fl.LifecycleUnreadable is not fl.LifecycleUnreadable
    assert aud._fc.__name__ == "scripts.funnel_coverage", "the sibling has the same shape"


def test_adapter_renders_a_zg4_error_as_fail_never_unavailable(monkeypatch: pytest.MonkeyPatch):
    """`unavailable` renders "N/A" and `_check_outcome` projects it onto `pass`, so an
    unavailable verdict SHIPS GREEN having measured nothing. A failed computation of an
    AVAILABLE ground truth blocks (Z-G4)."""
    import audit as aud

    monkeypatch.setattr(aud._fl, "measure", lambda *a, **k: (_ for _ in ()).throw(
        aud._fl.LifecycleUnreadable("frontmatter parsed to {}")))
    out = aud.check_funnel_lifecycle(REPO_ROOT)
    assert [f.status for f in out] == ["fail"]
    assert "Z-G4" in out[0].evidence


def test_adapter_blocks_on_an_unexpected_internal_error(monkeypatch: pytest.MonkeyPatch):
    """An internal error BLOCKS, never a silent pass -- the sibling gates' exit-2 contract."""
    import audit as aud

    monkeypatch.setattr(aud._fl, "measure", lambda *a, **k: (_ for _ in ()).throw(
        RuntimeError("boom")))
    out = aud.check_funnel_lifecycle(REPO_ROOT)
    assert [f.status for f in out] == ["fail"]
    assert "no verdict from this run is trustworthy" in out[0].evidence


def test_adapter_emits_one_finding_per_violation_on_the_live_tree():
    """Bundling would let the `#147` register suppress every violation with one substring."""
    import audit as aud

    out = aud.check_funnel_lifecycle(REPO_ROOT)
    assert out and all(f.check_name == fl.CHECK_NAME for f in out)
    assert {f.status for f in out} <= {"pass", "warn", "fail"}
