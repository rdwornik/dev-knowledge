"""Tests for FM-5 — `audit.py governance-health`, the value half.

WHAT IS ACTUALLY AT RISK here, and it is not "does a report print".

  * **The shared fields must not be recomputed.** The lane's Ex-ante is a BYTE-FOR-BYTE
    equality against FM-4's FUNNEL HEALTH block for the shared fields, and that is
    achievable exactly one way: both render from the same function. So the load-bearing
    assertion is a NEGATIVE one — when FM-4's emitter is absent, the four FM-4-owned fields
    render `unavailable` with a reason, and NOTHING computes them locally. A command that
    quietly produced its own number for `intakes consumed-unarchived` would satisfy every
    happy-path test and fail the only requirement that matters.

  * **Value evidence must be quoted, never synthesised.** "Sourced from close packets,
    never invented" is the contract's own wording, and the failure mode it names is a
    plausible benefit sentence with no packet behind it. The evidence is therefore the
    packet's own LINE, verbatim, with a `file:line` locator, and a row whose packets say
    nothing renders `no value evidence`. The discriminating case
    (`test_a_bare_mention_is_not_value_evidence`) is the one that proves the predicate
    DISCRIMINATES rather than merely matching every `[#id]` in the corpus.

  * **There must be no second store.** A1 is explicit: append-only records into the
    EXISTING telemetry store, derived views, no second store. `logs/TELEMETRY.db`
    (`scripts/telemetry_emit.py`, `[#529]`) is that store, and this command becomes a
    call site on its documented CALL SURFACE rather than a new one.
    `test_emit_writes_no_second_store` is the regression test for the whole clause.

RED-FIRST. Every case in this file was written and run BEFORE `scripts/governance_health.py`
existed; the first run collected 0 tests and errored on the import, which is the honest RED
for a module that is not there yet. The one case that stays RED after this lane is
`test_shared_fields_equal_fm4_block_byte_for_byte` — the Ex-ante itself — because FM-4 (lane
K) had not merged when this lane ran. That RED is the proof the Ex-ante asks for, not a
defect in this file.
"""
from __future__ import annotations

import sqlite3
import textwrap
from pathlib import Path

import pytest

import audit as aud
import governance_health as gh

_REPO_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------------------
# Close-packet discovery — the shapes are WITNESSED on disk, not trusted from the contract
# --------------------------------------------------------------------------------------

@pytest.mark.live_repo
def test_close_packet_discovery_finds_the_live_packets() -> None:
    """The contract lists two candidate shapes and says to verify them. This does."""
    packets = gh.close_packets(_REPO_ROOT)
    assert packets, "no close packets discovered under docs/audits/ — the corpus has them"
    for p in packets:
        assert p.parent == _REPO_ROOT / "docs" / "audits"
        assert any(p.match(pat) for pat in gh.CLOSE_PACKET_PATTERNS), p.name


def test_close_packet_discovery_is_pattern_bound(tmp_path: Path) -> None:
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True)
    (audits / "2026-01-01-verification-batch-1-close-packet.md").write_text("x", encoding="utf-8")
    (audits / "2026-01-02-technical-batch1-end-of-batch-packet.md").write_text("x", encoding="utf-8")
    (audits / "2026-01-03-technical-nb2-a-packet.md").write_text("x", encoding="utf-8")
    (audits / "README.md").write_text("x", encoding="utf-8")

    names = sorted(p.name for p in gh.close_packets(tmp_path))
    assert names == [
        "2026-01-01-verification-batch-1-close-packet.md",
        "2026-01-02-technical-batch1-end-of-batch-packet.md",
    ], "a lane packet is not a close packet — the globs are the boundary"


# --------------------------------------------------------------------------------------
# Value evidence — verbatim, locatored, and DISCRIMINATING
# --------------------------------------------------------------------------------------

def _seed_packet(tmp_path: Path, body: str, name: str = "2026-01-01-x-close-packet.md") -> Path:
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    p = audits / name
    p.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    return p


def test_value_evidence_is_the_packet_line_verbatim_with_a_locator(tmp_path: Path) -> None:
    _seed_packet(tmp_path, """
        # close packet
        preamble line
        | D | `[#900]` | `deadbeef` | **MET** — 77 -> 60, 20 rows, zero content destroyed |
    """)
    found = gh.value_evidence(tmp_path, [900])
    assert list(found) == [900]
    (ev,) = found[900]
    assert ev.text == "| D | `[#900]` | `deadbeef` | **MET** — 77 -> 60, 20 rows, zero content destroyed |"
    assert ev.locator == "docs/audits/2026-01-01-x-close-packet.md:3"


def test_a_row_with_no_packet_line_renders_no_value_evidence(tmp_path: Path) -> None:
    _seed_packet(tmp_path, """
        # close packet
        `[#900]` **MET** — measured 4 -> 2
    """)
    found = gh.value_evidence(tmp_path, [900, 901])
    assert found[900], "900 has a line"
    assert found[901] == [], "901 has none"
    assert gh.NO_VALUE_EVIDENCE in gh.render_value_section(found)
    assert "[#901] — no value evidence" in gh.render_value_section(found)


def test_a_bare_mention_is_not_value_evidence(tmp_path: Path) -> None:
    """THE DISCRIMINATOR. Every `[#id]` in a packet is a mention; only some are evidence.

    Without this case the predicate could be `id in line` and every test above would still
    pass while the coverage fraction reported 100% forever.
    """
    _seed_packet(tmp_path, """
        # close packet
        Two closure candidates, reported not filed: `[#901]` and `[#902]` are still open on main.
        See the row body for `[#903]`.
    """)
    found = gh.value_evidence(tmp_path, [901, 902, 903])
    assert found[901] == []
    assert found[902] == []
    assert found[903] == []


def test_a_measured_delta_alone_is_value_evidence(tmp_path: Path) -> None:
    _seed_packet(tmp_path, """
        # close packet
        `[#904]` docs/intake count 77 -> 60 across 20 relocations
    """)
    assert len(gh.value_evidence(tmp_path, [904])[904]) == 1


def test_coverage_fraction_counts_both_halves(tmp_path: Path) -> None:
    _seed_packet(tmp_path, """
        # close packet
        `[#900]` **MET**
        `[#901]` is still open
        `[#902]` **PARTIAL**
    """)
    found = gh.value_evidence(tmp_path, [900, 901, 902, 903])
    assert gh.coverage(found) == (2, 4)


# --------------------------------------------------------------------------------------
# THE NEGATIVE THAT MATTERS — nothing FM-4 owns is computed here
# --------------------------------------------------------------------------------------

def test_fm4_owned_fields_render_unavailable_when_the_emitter_is_absent(monkeypatch) -> None:
    monkeypatch.setattr(gh, "resolve_fm4_emitter",
                        lambda: gh.Fm4Source(available=False, dotted=None, reason="not present"))
    report = gh.build_report(_REPO_ROOT)
    for field in gh.FM4_OWNED_FIELDS:
        assert report.shared[field] == gh.UNAVAILABLE, field
    assert "not present" in report.fm4.reason


def test_no_fm4_owned_field_is_derivable_from_this_module() -> None:
    """Structural: this module exposes NO function that could compute an FM-4-owned field.

    Asserted against the module's own namespace rather than by reading the render output,
    because the failure this guards is someone adding `_count_unarchived_intakes()` later
    and wiring it in — at which point the equality Ex-ante is dead and every other test
    still passes.
    """
    banned = ("intake", "adr", "orphan", "unarchived", "unexecuted")
    offenders = [n for n in dir(gh)
                 if callable(getattr(gh, n)) and not n.startswith("__")
                 and any(b in n.lower() for b in banned)]
    assert offenders == [], f"FM-4-owned derivations must not live here: {offenders}"


def test_fm5_owned_fields_are_exported_for_fm4_to_import() -> None:
    """The other direction of one-truth: FM-4's block needs `value evidence attached`, and
    this module owns that derivation. It is exported so FM-4 imports rather than re-derives."""
    assert set(gh.FM5_OWNED_FIELDS) == {"rows closed this window", "value evidence attached"}
    assert callable(gh.value_evidence)
    assert callable(gh.rows_closed_in_window)
    assert set(gh.SHARED_FIELDS) == set(gh.FM4_OWNED_FIELDS) | set(gh.FM5_OWNED_FIELDS)


# --------------------------------------------------------------------------------------
# Render shape — the FUNNEL HEALTH block is numbers-only, matching FM-4's anti-bluff contract
# --------------------------------------------------------------------------------------

def test_health_block_is_numbers_only(monkeypatch) -> None:
    monkeypatch.setattr(gh, "resolve_fm4_emitter",
                        lambda: gh.Fm4Source(available=False, dotted=None, reason="absent"))
    block = gh.render_health_block(gh.build_report(_REPO_ROOT))
    for line in block.splitlines():
        if ":" not in line or line.startswith(gh.HEALTH_HEADER):
            continue
        value = line.split(":", 1)[1].strip()
        assert value == gh.UNAVAILABLE or value.isdigit(), f"non-numeric value in the block: {line!r}"
    assert gh.SHA_RE.search(block) is None, "anti-bluff: no SHAs in the health block"


def test_health_block_field_order_is_the_contract() -> None:
    block = gh.render_health_block(gh.build_report(_REPO_ROOT))
    seen = [ln.split(":", 1)[0].strip() for ln in block.splitlines()
            if ":" in ln and not ln.startswith(gh.HEALTH_HEADER)]
    assert seen == list(gh.SHARED_FIELDS)


# --------------------------------------------------------------------------------------
# The console the output actually lands on — cp1252, and the corpus already breaks it
# --------------------------------------------------------------------------------------

def test_a_quoted_arrow_delta_would_crash_a_cp1252_console_unencoded(tmp_path: Path) -> None:
    """RED-first witness: the value line most likely to exist is the one that crashes.

    `_DELTA_RE` matches `77 → 60`, `docs/audits/2026-08-26-verification-batch-1-close-packet.md`
    already contains U+2192, and `click.echo` raises on a cp1252 console for it. So this asserts
    BOTH halves: the raw line is unencodable (the defect is real, not imagined) and
    `console_safe` makes it writable without deleting anything.
    """
    _seed_packet(tmp_path, """
        # close packet
        `[#905]` docs/intake 77 → 60
    """)
    (ev,) = gh.value_evidence(tmp_path, [905])[905]
    with pytest.raises(UnicodeEncodeError):
        ev.text.encode("cp1252")

    safe = gh.console_safe(ev.text, "cp1252")
    safe.encode("cp1252")  # must not raise
    assert "\\u2192" in safe, "the character is escaped, never silently dropped"
    assert "[#905]" in safe and "77" in safe and "60" in safe


def test_console_safe_is_identity_when_the_console_can_take_it() -> None:
    assert gh.console_safe("77 → 60", "utf-8") == "77 → 60"


# --------------------------------------------------------------------------------------
# A1 — the EXISTING store, one appended record, no second store
# --------------------------------------------------------------------------------------

def test_emit_appends_one_check_run_to_the_existing_store(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(gh, "resolve_fm4_emitter",
                        lambda: gh.Fm4Source(available=False, dotted=None, reason="absent"))
    db = tmp_path / "TELEMETRY.db"
    report = gh.build_report(_REPO_ROOT)
    row_id = gh.emit(report, db_path=db, repo_path=_REPO_ROOT)
    assert isinstance(row_id, int)

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            "SELECT event_type, name, outcome FROM events").fetchall()
    assert rows == [("check_run", gh.TELEMETRY_NAME, "pass")]


def test_emit_writes_no_second_store(tmp_path: Path, monkeypatch) -> None:
    """A1: NO second store. The only file this may create is the one it was handed."""
    monkeypatch.setattr(gh, "resolve_fm4_emitter",
                        lambda: gh.Fm4Source(available=False, dotted=None, reason="absent"))
    db = tmp_path / "TELEMETRY.db"
    gh.emit(gh.build_report(_REPO_ROOT), db_path=db, repo_path=_REPO_ROOT)
    created = {p.name for p in tmp_path.rglob("*") if p.is_file()}
    assert created <= {"TELEMETRY.db", "TELEMETRY.db-wal", "TELEMETRY.db-shm"}, created


def test_emitted_context_carries_every_shared_field(tmp_path: Path, monkeypatch) -> None:
    """Trends only exist if the record carries the numbers, not just an outcome."""
    import json
    monkeypatch.setattr(gh, "resolve_fm4_emitter",
                        lambda: gh.Fm4Source(available=False, dotted=None, reason="absent"))
    db = tmp_path / "TELEMETRY.db"
    gh.emit(gh.build_report(_REPO_ROOT), db_path=db, repo_path=_REPO_ROOT)
    with sqlite3.connect(db) as conn:
        (ctx,) = conn.execute("SELECT context_json FROM events").fetchone()
    ctx = json.loads(ctx)
    for field in gh.SHARED_FIELDS:
        assert field in ctx["shared"], field
    assert ctx["fm4_source"] == "unavailable"
    assert ctx["git_derived"] is True


# --------------------------------------------------------------------------------------
# Runner reuse — the EXISTING click group, no second parser
# --------------------------------------------------------------------------------------

def test_subcommand_is_registered_on_the_existing_runner() -> None:
    assert "governance-health" in aud.cli.commands
    assert {"health", "checks", "run", "repo"} <= set(aud.cli.commands), \
        "the existing subcommands must still be there — this is reuse, not a rewrite"


@pytest.mark.slow
def test_package_mode_import_still_works() -> None:
    """RED-first, and it went red for real: `from scripts import audit` is a supported entry
    point (`tests/test_audit.py::test_check_fleet_parity_package_mode_import` pins it), and the
    first cut of this module imported `gen_task_tree` by bare name. Under package mode that
    raised ImportError, `audit.py`'s dual shim mis-read it as "governance_health is absent",
    and the sibling test failed with `ModuleNotFoundError: No module named 'governance_health'`.

    This asserts the property directly rather than leaving it to a fleet_parity test to notice.
    """
    import subprocess
    import sys
    code = ("from scripts import audit; "
            "from scripts import governance_health as g; "
            "print('OK' if 'governance-health' in audit.cli.commands and g.SHARED_FIELDS else 'BAD')")
    proc = subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True, cwd=str(_REPO_ROOT))
    assert proc.returncode == 0, proc.stderr[-800:]
    assert proc.stdout.strip().endswith("OK"), proc.stdout + proc.stderr


def test_no_second_argument_parser_was_added() -> None:
    src = (_REPO_ROOT / "scripts" / "governance_health.py").read_text(encoding="utf-8")
    for banned in ("import argparse", "ArgumentParser", "click.group", "@click.command"):
        assert banned not in src, f"{banned!r} — the runner is audit.py's existing click group"


# --------------------------------------------------------------------------------------
# THE EX-ANTE — RED until FM-4 (lane K) merges. That RED is the proof, not a defect.
# --------------------------------------------------------------------------------------

def test_shared_fields_equal_fm4_block_byte_for_byte() -> None:
    """*"the command runs on merged main and its numbers equal FM-4's block byte-for-byte
    for the shared fields."*

    This is the lane's Ex-ante, expressed as the only thing that can measure it. It resolves
    FM-4's emitter, renders both blocks, and compares the shared fields value-for-value.
    While lane K is unmerged the resolver returns unavailable and this FAILS with the
    resolution report — an honest RED naming exactly what is missing.
    """
    src = gh.resolve_fm4_emitter()
    if not src.available:
        pytest.fail(
            "FM-4's FUNNEL HEALTH emitter is not resolvable, so the byte-for-byte equality "
            f"cannot be measured. Resolution report: {src.reason}\n"
            "This RED is the lane's Ex-ante standing unmet until lane K (FM-4) merges; it is "
            "not a defect in FM-5. When K lands, this test measures the Ex-ante with no edit."
        )
    mine = gh.parse_shared_fields(gh.render_health_block(gh.build_report(_REPO_ROOT)))
    theirs = gh.parse_shared_fields(src.render(_REPO_ROOT))
    shared = set(mine) & set(theirs)
    assert shared, "the two blocks share no field names — the coupling is broken, not merely absent"
    for field in sorted(shared):
        assert mine[field] == theirs[field], f"{field}: FM-5 {mine[field]!r} != FM-4 {theirs[field]!r}"
