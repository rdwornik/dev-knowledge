"""b2-transport-lint (LANE-B2-W1-b2-transport-lint): a transport file that breaks the grammar is
caught when it is written, not at the batch close.

The failure this lane closes: FOUNDATION's close was refused by ONE file -- a run SIGNAL written
under a DECISION prefix (`AMEND-5-GREEN-2026-10-03.md`) as a one-line file with no `carried-by:`
head. Nothing checked it when it was written; the trial cut found it 9 h later. `SIGNAL_FIXTURE`
below is that file's original shape, byte for byte.

One test group per Done-contract item (1 kinds, 2 CLI, 3 writers, 4 sweep, 5 R59 enforcement).
Everything drives a synthetic transport in `tmp_path`; nothing here touches the real drive.
"""
from __future__ import annotations

import ast
import importlib
import os
import re
import sys
import time
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

REGISTRY_PATH = _REPO / "ecosystem" / "transport-registry.yaml"

#: The original shape of `AMEND-5-GREEN-2026-10-03.md`: one line, no `carried-by:` head.
SIGNAL_FIXTURE = "AMEND-5 GREEN at 3157d69b\n"

CONFORMING_DECISION = (
    "carried-by: OPEN\n"
    "lands-via: the lanes of the batch\n"
    "date: 2026-10-04\n"
    "\n"
    "# AMEND — a clarification\n"
)


def _mod(name: str):
    return importlib.import_module(name)


@pytest.fixture()
def t():
    return _mod("transport")


@pytest.fixture()
def lint():
    return _mod("transport_lint")


@pytest.fixture()
def registry(t):
    return t.load_registry(REGISTRY_PATH)


@pytest.fixture()
def world(tmp_path: Path) -> dict:
    root = tmp_path / "drive"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-browser").mkdir()
    return {"root": root, "cc": root / "to-cc", "browser": root / "to-browser"}


def _raw_kinds() -> list[dict]:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))["kinds"]


# --- item 1: signals have their own non-decision kind; the decision prefixes are reserved --------

def test_every_registry_row_carries_a_decision_class():
    """The class is DATA on every kind, not a default the loader fills in."""
    missing = [r["kind"] for r in _raw_kinds() if r.get("class") not in ("decision", "non-decision")]
    assert not missing, f"kinds with no decision/non-decision class: {missing}"


def test_the_registrys_decision_kinds_equal_the_carriage_prefixes_exactly(t, registry):
    """`gen_handoff.CARRIAGE_PREFIXES` is the decision predicate (a ruling, not a lane's call);
    the registry's class must equal it so the two cannot drift."""
    gh = _mod("gen_handoff")
    decision_prefixes = {k.prefix for k in registry if k.decision}
    assert decision_prefixes == set(gh.CARRIAGE_PREFIXES)


def test_a_signal_kind_exists_and_is_non_decision(t, registry):
    kind = t.classify("SIGNAL-B2-W1-GREEN-2026-10-04.md", registry)
    assert kind is not None and kind.name == "SIGNAL"
    assert kind.decision is False
    assert kind.prefix == "SIGNAL-"


def test_the_batch_integrator_order_is_a_registered_non_decision_to_cc_kind(t, registry):
    """N1: `INTEGRATOR-<BATCH>-<date>.md` classified as unregistered, so the sweep would have
    flagged the live integrator order of the batch it runs in."""
    for name in ("INTEGRATOR-B2-W1-2026-10-04.md", "INTEGRATOR-FOUNDATION-2026-10-03.md"):
        kind = t.classify(name, registry)
        assert kind is not None, name
        assert kind.folder == "to-cc" and kind.decision is False and kind.versioned is True


def test_claim_markers_are_a_registered_kind(t, registry):
    kind = t.classify("LANE-B2-W1-b2-transport-lint.CLAIMED-e576645a", registry)
    assert kind is not None and kind.name == "CLAIM_MARKER" and kind.decision is False


def test_the_lint_refuses_a_signal_shaped_file_under_a_decision_prefix(lint):
    findings = lint.lint_text("AMEND-5-GREEN-2026-10-03.md", "to-cc", SIGNAL_FIXTURE)
    assert [f.code for f in findings] == ["signal-under-decision-prefix"]
    assert "SIGNAL-" in findings[0].reason


def test_the_same_one_line_body_is_clean_under_the_signal_kind(lint):
    assert lint.lint_text("SIGNAL-5-GREEN-2026-10-03.md", "to-browser", SIGNAL_FIXTURE) == []


# --- item 2: the CLI checks a file's kind, head and carried-by -----------------------------------

def test_a_conforming_decision_file_passes(lint):
    assert lint.lint_text("AMEND-CLARIFY-2026-10-04.md", "to-cc", CONFORMING_DECISION) == []


@pytest.mark.parametrize("name,folder,text,code", [
    ("ZZUNKNOWN-thing-2026-10-04.md", "to-cc", "x\n", "unknown-kind"),
    ("AMEND-has a space.md", "to-cc", CONFORMING_DECISION, "pattern-mismatch"),
    ("AMEND-CLARIFY-2026-10-04.md", "to-browser", CONFORMING_DECISION, "wrong-folder"),
    ("AMEND-CLARIFY-2026-10-04.md", "to-cc", "date: 2026-10-04\n\n# a ruling\nwith a body\n",
     "no-carried-by"),
    ("AMEND-CLARIFY-2026-10-04.md", "to-cc", "carried-by: soon\n\n# a ruling\n",
     "carried-by-not-a-path"),
])
def test_the_lint_refuses_each_grammar_break_with_its_own_code(lint, name, folder, text, code):
    assert code in [f.code for f in lint.lint_text(name, folder, text)]


def test_carried_by_below_the_sixth_line_is_not_anchored(lint):
    head = "".join(f"filler {i}\n" for i in range(6))
    text = head + "carried-by: OPEN\n"
    assert "no-carried-by" in [f.code for f in lint.lint_text("DECLARE-X-2026-10-04.md", "to-cc", text)]


def test_carried_by_inside_an_html_comment_is_not_anchored(lint):
    text = "<!-- carried-by: OPEN -->\n\n# body\n"
    assert "no-carried-by" in [f.code for f in lint.lint_text("BATCH-X-2026-10-04.md", "to-cc", text)]


def test_carried_by_naming_a_repo_path_passes(lint):
    text = "carried-by: protocols/STANDING_RULINGS.md §AN\n\n# body\n"
    assert lint.lint_text("DECLARE-X-2026-10-04.md", "to-cc", text) == []


def test_the_head_reader_agrees_with_gen_handoff_on_the_same_file(lint, tmp_path):
    """Library-first: the lint reads the head exactly as `gen_handoff.carried_by_value` does."""
    gh = _mod("gen_handoff")
    for body in (CONFORMING_DECISION, SIGNAL_FIXTURE, "x\ny\n" * 5 + "carried-by: OPEN\n",
                 "carried-by:   protocols/X.md  \r\n"):
        p = tmp_path / "AMEND-PARITY.md"
        p.write_bytes(body.encode("utf-8"))
        assert lint.carried_by_value(body) == gh.carried_by_value(p)


def test_cli_check_exits_nonzero_with_the_reason_and_zero_on_a_conforming_file(lint, world, capsys):
    bad = world["cc"] / "AMEND-5-GREEN-2026-10-03.md"
    bad.write_text(SIGNAL_FIXTURE, encoding="utf-8")
    good = world["cc"] / "AMEND-CLARIFY-2026-10-04.md"
    good.write_text(CONFORMING_DECISION, encoding="utf-8")
    assert lint.main(["check", str(bad)]) == 1
    err = capsys.readouterr()
    assert "signal-under-decision-prefix" in (err.out + err.err)
    assert lint.main(["check", str(good)]) == 0


def test_cli_check_reads_the_folder_from_the_files_own_parent(lint, world):
    misplaced = world["browser"] / "AMEND-CLARIFY-2026-10-04.md"
    misplaced.write_text(CONFORMING_DECISION, encoding="utf-8")
    assert lint.main(["check", str(misplaced)]) == 1


# --- item 3: every harness writer calls the lint before writing ----------------------------------

def test_write_refuses_a_signal_shaped_decision_file_before_any_byte_lands(t, world, registry):
    dest = world["cc"] / "AMEND-5-GREEN-2026-10-03.md"
    with pytest.raises(t.TransportWriteRefused, match="signal-under-decision-prefix"):
        t.write("operator", dest, SIGNAL_FIXTURE, registry=registry)
    assert not dest.exists()
    assert not [p for p in world["cc"].iterdir()]


def test_write_accepts_a_conforming_decision_file_and_the_signal_kind(t, world, registry):
    ok = t.write("operator", world["cc"] / "AMEND-CLARIFY-2026-10-04.md", CONFORMING_DECISION,
                 registry=registry)
    assert ok.read_text(encoding="utf-8") == CONFORMING_DECISION
    sig = t.write("operator", world["browser"] / "SIGNAL-5-GREEN-2026-10-03.md", SIGNAL_FIXTURE,
                  registry=registry)
    assert sig.read_text(encoding="utf-8") == SIGNAL_FIXTURE


def test_append_lints_the_resulting_file(t, world, registry):
    dest = world["browser"] / "SESSION-lint-lane.md"
    t.append("lane", dest, "first block\n", registry=registry)
    assert dest.read_text(encoding="utf-8").startswith("first block")


def test_emit_lints_a_transport_destination_and_leaves_other_paths_alone(t, world, tmp_path, registry):
    with pytest.raises(t.TransportWriteRefused):
        t.emit("operator", world["cc"] / "AMEND-5-GREEN-2026-10-03.md", SIGNAL_FIXTURE)
    outside = tmp_path / "elsewhere" / "report.md"
    t.emit("gen_ledger", outside, "plain\n")
    assert outside.read_text(encoding="utf-8") == "plain\n"


#: The registry's `writers:` entries that are SCRIPT modules (a file in scripts/), by how this
#: lane left them. A new script writer added to the registry without a line here fails the test.
ROUTED = {            # call the lint through transport.write / append / emit
    "gen_ledger": "gen_ledger.py",
    "propose_row_closures": "propose_row_closures.py",
    "transport_report": "transport_report.py",
    "handback": "handback.py",
    "quota_watch": "quota_watch.py",
}
NOT_TRANSPORT = {      # confirmed by code: writes a repo handoff bundle, not the transport
    "gen_seat_boot": "gen_seat_boot.py",
}
OWNED_ELSEWHERE = {    # another lane of batch B2-W1 owns the call site
    "gen_lane_contract": "lane W1-4 (item 5, after this lane merges)",
}
ROLES = {"operator", "lane", "integrator"}


def _script_writers() -> set[str]:
    out: set[str] = set()
    for row in _raw_kinds():
        for w in row.get("writers", ()):
            if w not in ROLES and (_SCRIPTS / f"{w}.py").is_file():
                out.add(w)
    return out


def test_every_script_writer_in_the_registry_is_accounted_for():
    known = set(ROUTED) | set(NOT_TRANSPORT) | set(OWNED_ELSEWHERE)
    assert _script_writers() == known, (
        f"unaccounted script writers: {sorted(_script_writers() - known)}; "
        f"stale entries: {sorted(known - _script_writers())}")


def _calls_in(path: Path, names: set[str], skip_functions: set[str] = frozenset()) -> list[int]:
    """Line numbers of calls to any of `names` (attribute or bare), outside `skip_functions`."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    hits: list[int] = []

    def visit(node: ast.AST, inside: bool) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in skip_functions:
            inside = True
        if isinstance(node, ast.Call) and not inside:
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if nm in names:
                hits.append(node.lineno)
        for child in ast.iter_child_nodes(node):
            visit(child, inside)

    visit(tree, False)
    return hits


@pytest.mark.parametrize("writer", ["gen_ledger", "propose_row_closures", "transport_report"])
def test_an_owned_writer_has_no_direct_write_that_bypasses_the_lint(writer):
    """The writers this lane owns write only through `transport.write`/`emit` -- no
    `write_text`/`write_bytes`/`deliver` call of its own (transport_report's own `deliver`
    definition is the plumbing `transport.write` calls)."""
    path = _SCRIPTS / ROUTED[writer]
    assert _calls_in(path, {"write_text", "write_bytes", "deliver"}, {"deliver"}) == []
    assert _calls_in(path, {"write", "append", "emit"}), f"{writer} never calls the lint-gated writer"


def test_the_not_transport_writer_never_names_the_transport():
    """`gen_seat_boot` renders the text of a boot (which names `CLAUDE_PROMPTS_DIR` in prose) and
    writes it into a repo handoff bundle directory the caller names; it never resolves the
    transport, so it has no transport write to lint."""
    src = (_SCRIPTS / NOT_TRANSPORT["gen_seat_boot"]).read_text(encoding="utf-8")
    assert not re.search(r"\b(resolve_transport|transport_root)\s*\(|^\s*(import|from)\s+(scripts\.)?transport\b",
                         src, re.M)
    assert "def write_bundle(bundle_dir" in src


def test_already_routed_writers_still_go_through_transport_write():
    for w in ("handback", "quota_watch"):
        assert _calls_in(_SCRIPTS / ROUTED[w], {"write", "append"}), w


def test_write_calls_the_lint_before_it_touches_the_filesystem(t):
    src = (_SCRIPTS / "transport.py").read_text(encoding="utf-8")
    body = src[src.index("def write("):src.index("class _DestinationLock")]
    assert body.index("transport_lint") < body.index("deliver(")


def test_the_lane_end_artifact_still_lints_clean_through_transport_report(world, monkeypatch):
    """transport_report's Stop-hook write keeps working: the LANE-END file is a non-decision kind."""
    tr = _mod("transport_report")
    repo = world["root"].parent / "repo"
    (repo / "logs" / "receipts").mkdir(parents=True)
    rc = tr.main(["--lane", "demo-lane", "--repo", str(repo), "--transport-root", str(world["root"]),
                  "--receipts-dir", str(repo / "logs" / "receipts")])
    assert rc == 0
    assert (world["browser"] / "LANE-END-demo-lane.md").is_file()


# --- item 4: a wake sweeps the transport and flags a bad file within one wake ---------------------

def _bad_world(world):
    (world["cc"] / "AMEND-CLARIFY-2026-10-04.md").write_text(CONFORMING_DECISION, encoding="utf-8")
    (world["browser"] / "SIGNAL-OK-2026-10-04.md").write_text("fine\n", encoding="utf-8")
    (world["cc"] / "AMEND-5-GREEN-2026-10-03.md").write_text(SIGNAL_FIXTURE, encoding="utf-8")
    (world["browser"] / "NOT-A-KIND-2026-10-04.md").write_text("x\n", encoding="utf-8")
    return world


def test_one_sweep_pass_flags_a_hand_written_bad_file(lint, world):
    _bad_world(world)
    findings = lint.sweep(world["root"])
    flagged = {f.path for f in findings}
    assert flagged == {"to-cc/AMEND-5-GREEN-2026-10-03.md", "to-browser/NOT-A-KIND-2026-10-04.md"}


def test_the_sweep_cli_exits_nonzero_with_one_line_per_bad_file(lint, world, capsys):
    _bad_world(world)
    assert lint.main(["sweep", "--transport-root", str(world["root"])]) == 1
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) == 2
    assert any("to-cc/AMEND-5-GREEN-2026-10-03.md" in ln and "signal-under-decision-prefix" in ln
               for ln in lines)


def test_the_sweep_exits_zero_on_a_clean_transport(lint, world):
    (world["cc"] / "AMEND-CLARIFY-2026-10-04.md").write_text(CONFORMING_DECISION, encoding="utf-8")
    assert lint.main(["sweep", "--transport-root", str(world["root"])]) == 0


def test_the_sweep_since_a_time_skips_older_files(lint, world):
    _bad_world(world)
    old = time.time() - 3 * 3600
    for p in (world["cc"] / "AMEND-5-GREEN-2026-10-03.md",):
        os.utime(p, (old, old))
    flagged = {f.path for f in lint.sweep(world["root"], since=time.time() - 3600)}
    assert flagged == {"to-browser/NOT-A-KIND-2026-10-04.md"}


def test_since_parses_a_relative_window_and_an_iso_time(lint):
    now = 1_000_000_000.0
    assert lint.parse_since("30m", now=now) == now - 1800
    assert lint.parse_since("2h", now=now) == now - 7200
    assert lint.parse_since("1d", now=now) == now - 86400
    assert lint.parse_since("2026-10-04T00:00:00+00:00") == 1791072000.0


def test_the_sweep_reports_only_and_never_moves_or_deletes(lint, world):
    _bad_world(world)
    before = sorted(p.name for d in (world["cc"], world["browser"]) for p in d.iterdir())
    lint.sweep(world["root"])
    after = sorted(p.name for d in (world["cc"], world["browser"]) for p in d.iterdir())
    assert before == after


def test_the_sweep_ignores_dotfiles_and_the_append_lock(lint, world):
    (world["browser"] / ".SESSION-x.md.append.lock").write_text("", encoding="utf-8")
    (world["browser"] / ".LANE-END-x.md.tmp").write_text("", encoding="utf-8")
    assert lint.sweep(world["root"]) == []


def test_the_dispatcher_order_template_names_the_sweep_in_its_wake():
    text = (_REPO / "templates" / "dispatcher-order-template.md").read_text(encoding="utf-8")
    assert "transport_lint.py sweep" in text


def test_the_batch_common_rules_template_names_the_lint_and_the_signal_kind():
    text = (_REPO / "templates" / "batch-common-rules-template.md").read_text(encoding="utf-8")
    assert "transport_lint.py check" in text
    assert "SIGNAL-" in text
    assert "transport_lint.py sweep" in text


# --- item 5: the R59 proof of read, enforced ------------------------------------------------------

LANE_WITH_PROOF = (
    "# LANE x\n\n## Done-contract (immutable)\n\n"
    "n. **Close-out:** a review record carrying the served model id from the tool's own log and "
    "the nonce or content hash the reviewer returned.\n"
)
LANE_WITHOUT_PROOF = (
    "# LANE x\n\n## Done-contract (immutable)\n\n"
    "n. **Close-out:** targeted tests, a Codex review record, handback.\n"
)


def test_a_lane_contract_naming_the_r59_proof_passes(lint):
    assert lint.lint_text("LANE-B2-W1-x.md", "root", LANE_WITH_PROOF) == []


def test_a_lane_contract_without_the_r59_proof_is_refused(lint):
    codes = [f.code for f in lint.lint_text("LANE-B2-W1-x.md", "root", LANE_WITHOUT_PROOF)]
    assert codes == ["lane-contract-no-r59-proof"]


def test_a_lane_contract_naming_only_the_model_id_is_refused(lint):
    text = "# LANE x\n\nclose-out: record the served model id.\n"
    assert "lane-contract-no-r59-proof" in [f.code for f in lint.lint_text("LANE-x.md", "root", text)]


def test_the_lane_contract_template_still_names_the_proof_at_the_line_the_contract_cites():
    """Item 5's template half is met on main (`6a45b1ff`); quoted, not re-edited here."""
    lines = (_REPO / "templates" / "lane-contract-template.md").read_text(encoding="utf-8").splitlines()
    window = " ".join(lines[84:92])
    assert "R59 proof of read" in window and "nonce or content hash" in window
