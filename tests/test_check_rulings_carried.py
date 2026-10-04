"""The `rulings_carried` audit finding, its two homes, and item 2's carriage line (R79.3, [#721]).

Batch B2-W1, lane W1-10 `b2-rulings-landing`. RED-first at origin/main e67f27ac: that tree has no
`check_rulings_carried`, `HANDOFF_ORGAN_NAMES` stops at eleven, and both RATIFICATION files on the
transport read `carried-by: OPEN`, so every test here fails there.

WHAT EACH GROUP WITNESSES:
  1. the ADAPTER -- a refusing register yields `fail` findings, a carried one `pass`, and a
     register-less repo `n/a` (never a pass);
  2. the TRANSPORT BOUNDARY -- leg (a) with no readable transport is `n/a` with a registered
     reason and is NEVER a `pass` (CI has no transport);
  3. THE TWO HOMES -- the check is a handoff organ (so the real cut and `--trial-cut` run it),
     it can FAIL, it is declared SHIP tier, and `ecosystem/harness.yaml`'s `batch-close` moment
     still runs the trial cut that carries the handoff organs;
  4. ITEM 2's CARRIAGE LINE -- `gen_handoff`'s carriage predicate (`carried_by_value` +
     `_resolves_on_main`, the per-file path of `carriage_verdicts`) returns `resolves` for both
     RATIFICATION files. `p11_carriage` itself does not list RATIFICATION files
     (`CARRIAGE_PREFIXES`), which is a ROWS-OWED line and not a widening by this lane.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import audit as aud  # noqa: E402
import decision_coverage as dc  # noqa: E402
import gen_handoff as gh  # noqa: E402
from audit_checks import check_rulings_carried as adapter  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

NO_IMPL = "no implementation required — procedural, nothing to build (owner: the browser seat)"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _repo(tmp_path: Path, *entries: str, row: bool = True) -> Path:
    root = tmp_path / "repo"
    _write(root / "protocols" / "STANDING_RULINGS.md",
           "# Register\n\n## AR. fixture\n\n" + "".join(entries) + "## Editing note\n\nx\n")
    if row:
        _write(root / "tasks" / "1500-fixture.md",
               "---\nid: \"[#1500]\"\nstatus: open\n---\n\n- [#1500] fixture carrying R70 · Done when: x\n")
    return root


def _entry(number: int, carried: str | None) -> str:
    out = f"- **R{number} — a fixture** (operator, 2026-10-04).\n\n"
    return out + (f"  **Carried by:** {carried}\n\n" if carried else "")


@pytest.fixture
def no_transport(monkeypatch):
    monkeypatch.setattr(adapter._dc, "_transport_root", lambda: None)


# --- 1. the adapter -------------------------------------------------------------------------


def test_an_uncarried_ruling_is_a_FAIL_finding_named_by_ruling(tmp_path: Path, no_transport):
    root = _repo(tmp_path, _entry(70, None))
    findings = adapter.check_rulings_carried(root)
    fails = [f for f in findings if f.status == "fail"]
    assert [f.check_name for f in fails] == ["rulings_carried"]
    assert fails[0].evidence.startswith("R70:") and "|" not in fails[0].evidence


def test_a_carried_register_passes_the_carried_leg(tmp_path: Path, no_transport):
    root = _repo(tmp_path, _entry(70, "[#1500]"), _entry(71, NO_IMPL))
    findings = adapter.check_rulings_carried(root)
    assert not [f for f in findings if f.status == "fail"]
    assert any(f.status == "pass" and "2 of 2 gated ruling(s)" in f.evidence for f in findings)


def test_a_repo_with_no_register_is_not_applicable(tmp_path: Path):
    findings = adapter.check_rulings_carried(tmp_path)
    assert [f.status for f in findings] == ["n/a"]
    assert aud._na_reason(findings[0]) == aud._NA_SUBJECT_ABSENT


# --- 2. the transport boundary --------------------------------------------------------------


def test_with_no_transport_the_unlanded_leg_is_NA_and_never_a_pass(tmp_path: Path, no_transport):
    root = _repo(tmp_path, _entry(70, "[#1500]"))
    findings = adapter.check_rulings_carried(root)
    na = [f for f in findings if f.status == "n/a"]
    assert len(na) == 1
    assert aud._na_reason(na[0]) == aud._NA_SUBJECT_ABSENT
    assert "not a pass" in na[0].evidence
    assert not any(f.status == "pass" and "RATIFICATION" in f.evidence for f in findings)


def test_an_unlanded_ruling_past_one_batch_is_a_FAIL_finding(tmp_path: Path, monkeypatch):
    root = _repo(tmp_path, _entry(70, "[#1500]"))
    transport = tmp_path / "t"
    _write(transport / "to-browser" / "RATIFICATION-2026-09-01.md",
           "carried-by: OPEN\ndate: 2026-09-01\n\n## R99 — unlanded\n")
    _write(transport / "to-browser" / "STATE-BATCH-A.md", "CLOSED 2026-09-05T00:00Z\n")
    _write(transport / "to-browser" / "STATE-BATCH-B.md", "CLOSED 2026-09-08T00:00Z\n")
    monkeypatch.setattr(adapter._dc, "_transport_root", lambda: transport)
    fails = [f for f in adapter.check_rulings_carried(root) if f.status == "fail"]
    assert len(fails) == 1 and fails[0].evidence.startswith("R99:")


# --- 3. the two homes -----------------------------------------------------------------------


def test_the_check_is_a_handoff_organ_so_the_real_cut_and_the_trial_cut_run_it():
    assert "check_rulings_carried" in aud.HANDOFF_ORGAN_NAMES
    organs = {fn.__name__ for fn in aud.handoff_organs()}
    assert "check_rulings_carried" in organs
    # `_row_ship_gate` runs EXACTLY this set (tests/test_handoff_cut_acceptance.py pins it), so a
    # check named here runs at the real cut and at `gen_handoff.py --trial-cut` with no edit to
    # `gen_handoff.py`.


def test_the_check_is_declared_ship_tier_and_can_fail():
    names = [c.__name__ for c in aud.ALL_CHECKS]
    check = aud.ALL_CHECKS[names.index("check_rulings_carried")]
    assert aud.tier_of(check) == aud.TIER_SHIP
    import inspect
    assert '"fail"' in inspect.getsource(adapter.check_rulings_carried)


def test_batch_close_still_runs_the_trial_cut_that_carries_the_handoff_organs():
    """N5: the `batch-close` moment of `ecosystem/harness.yaml` runs `gen_handoff.py --trial-cut`.
    That file is W1-2's this batch; this test only reads it, so the claim 'one registered check
    reaches both homes' cannot go stale unnoticed."""
    import yaml
    data = yaml.safe_load((REPO_ROOT / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    moments = {m["name"]: m for m in data["moments"]} if "moments" in data else {}
    assert "batch-close" in moments, "the batch-close moment is gone"
    organs = {o["id"]: o for o in moments["batch-close"]["organs"]}
    command = " ".join(str(part) for part in organs["trial_cut"]["command"])
    assert "gen_handoff.py" in command and "--trial-cut" in command


def test_the_live_finding_on_this_tree_does_not_fail():
    findings = aud.check_rulings_carried(REPO_ROOT)
    fails = [f for f in findings if f.status == "fail"]
    assert fails == [], "; ".join(f.evidence for f in fails)
    assert any(f.status == "pass" for f in findings)


# --- 4. item 2: the two RATIFICATION files resolve under the carriage predicate ----------------

_TRANSPORT_FILES = ("RATIFICATION-2026-10-03.md", "RATIFICATION-2026-10-04.md")


def _verdict(path: Path) -> tuple[str, str]:
    """`gen_handoff`'s per-file carriage predicate, called by import: the value, then the verdict
    `carriage_verdicts` would reach for it (OPEN first, then a token that resolves on `main`)."""
    value = gh.carried_by_value(path)
    if value is None:
        return gh.CARRIAGE_NO_KEY, ""
    if gh._OPEN_VALUE_RE.match(value):
        return gh.CARRIAGE_OPEN, value
    home = next((t for t in gh._carrier_tokens(value) if gh._resolves_on_main(REPO_ROOT, t)), None)
    return (gh.CARRIAGE_RESOLVES, home) if home else (gh.CARRIAGE_UNRESOLVED, value)


def test_the_carriage_predicate_resolves_a_line_naming_the_register(tmp_path: Path):
    """The shape the two files carry: it names the register section that landed the rulings and
    the rows, and the register resolves on `main`."""
    path = tmp_path / "RATIFICATION-X.md"
    _write(path, "carried-by: protocols/STANDING_RULINGS.md section AR (landed by b2-rulings-"
                 "landing, 2026-10-04); rows tasks/1360-d1-is-the-first-real-backlog-task-through"
                 "-the-spin.md\nlands-via: x\n\n# R\n")
    verdict, home = _verdict(path)
    assert verdict == gh.CARRIAGE_RESOLVES and home == "protocols/STANDING_RULINGS.md"


def test_the_carriage_predicate_still_reads_OPEN_as_open(tmp_path: Path):
    path = tmp_path / "RATIFICATION-X.md"
    _write(path, "carried-by: OPEN\nlands-via: x\n")
    assert _verdict(path)[0] == gh.CARRIAGE_OPEN


def test_both_live_ratification_files_resolve_on_main():
    transport = dc._transport_root()
    folder = Path(transport) / "to-browser" if transport else None
    if folder is None or not all((folder / n).is_file() for n in _TRANSPORT_FILES):
        warnings.warn("UNVERIFIED: the transport's RATIFICATION files are not reachable here -- "
                      "item 2's carried-by lines were not read", UserWarning, stacklevel=1)
        return
    bad = {}
    for name in _TRANSPORT_FILES:
        verdict, detail = _verdict(folder / name)
        if verdict != gh.CARRIAGE_RESOLVES:
            bad[name] = (verdict, detail)
    assert not bad, f"carriage predicate does not return `resolves`: {bad}"
