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
import hashlib
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


def test_the_seat_state_json_files_are_registered_so_a_wake_does_not_flag_them(t, registry):
    for name, kind in (("STATE-b2-w1-dispatcher.json", "SEAT_STATE"), ("STATE-b2-w1.json", "SEAT_STATE"),
                       ("STATE-b2-w1.md", "STATE")):
        got = t.classify(name, registry)
        assert got is not None and got.name == kind, name


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
        t.emit("operator", world["cc"] / "AMEND-5-GREEN-2026-10-03.md", SIGNAL_FIXTURE,
               transport_root=world["root"])
    outside = tmp_path / "elsewhere" / "report.md"
    t.emit("gen_ledger", outside, "plain\n", transport_root=world["root"])
    assert outside.read_text(encoding="utf-8") == "plain\n"


def test_a_scratch_directory_sharing_the_basename_is_not_the_transport(t, world, tmp_path):
    """Codex terra HIGH: `--out <scratch>/to-browser/x.md` is not a transport write, and must
    not be refused for being an unregistered kind."""
    scratch = tmp_path / "scratch" / "to-browser" / "my-report.md"
    assert t.is_transport_dest(scratch, world["root"]) is False
    t.emit("gen_ledger", scratch, "plain\n", transport_root=world["root"])
    assert scratch.read_text(encoding="utf-8") == "plain\n"
    assert t.is_transport_dest(world["browser"] / "x.md", world["root"]) is True
    assert t.is_transport_dest(world["root"] / "LANE-x.md", world["root"]) is True


def test_a_differently_cased_folder_name_is_still_the_transport(t, world):
    """Codex terra HIGH: a Windows path may spell the folder `TO-BROWSER`; it must not bypass
    the gate (the real folder is the same one)."""
    assert t.is_transport_dest(world["root"] / "TO-BROWSER" / "x.md", world["root"]) is True
    assert t._folder_of(world["root"] / "TO-CC" / "x.md") == "to-cc"


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
    "seat_state": "no lane of B2-W1 owns it: ROWS-OWED, route its `--path` write through "
                  "transport.emit",
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


def test_r59_words_in_unrelated_prose_do_not_satisfy_the_close_out_gate(lint):
    """Codex terra HIGH: the proof counts in the close-out item, not anywhere in the file."""
    text = ("# LANE x\n\nWe recorded the served model id and a nonce in an earlier lane.\n\n"
            "## Done-contract (immutable)\n\n1. a thing\n"
            "2. **Close-out:** tests and a handback.\n\n## Do not\n\n- record a nonce here\n")
    assert [f.code for f in lint.lint_text("LANE-x.md", "root", text)] == ["lane-contract-no-r59-proof"]


def test_a_lane_contract_with_no_close_out_item_is_refused(lint):
    text = "# LANE x\n\nthe served model id and a nonce\n"
    assert [f.code for f in lint.lint_text("LANE-x.md", "root", text)] == ["lane-contract-no-r59-proof"]


_ITEM_START = re.compile(r"^(\d+|n)\.\s")


def _r59_item_in_done_contract(text: str) -> str:
    """The numbered Done-contract item that carries `R59 proof of read`, or "" if there is none.

    Content-anchored (N5): finds the phrase's line, requires it to lie after the `## Done-contract`
    heading and before the next `## ` heading, and returns that numbered item (its first line up to
    the next numbered item or blank line).
    """
    lines = text.splitlines()
    start = next((n for n, ln in enumerate(lines) if ln.startswith("## Done-contract")), None)
    if start is None:
        return ""
    end = next((n for n in range(start + 1, len(lines)) if lines[n].startswith("## ")), len(lines))
    hit = next((n for n in range(start + 1, end) if "R59 proof of read" in lines[n]), None)
    if hit is None:
        return ""
    first = hit
    while first > start + 1 and not _ITEM_START.match(lines[first]):
        if not lines[first][:1].isspace():  # flush-left prose is not a continuation line
            return ""
        first -= 1
    if not _ITEM_START.match(lines[first]):
        return ""
    last = hit + 1
    while last < end and lines[last][:1].isspace() and lines[last].strip():
        last += 1
    return " ".join(lines[first:last])


def test_the_lane_contract_template_still_names_the_proof_at_the_line_the_contract_cites():
    """Item 5's template half is met on main (`6a45b1ff`); quoted, not re-edited here.

    The contract cited `:88`, frozen at `e67f27ac`; a later lane inserted lines above it, so the
    check now finds the item wherever it sits inside `## Done-contract` (N5: no frozen line number).
    """
    item = _r59_item_in_done_contract(
        (_REPO / "templates" / "lane-contract-template.md").read_text(encoding="utf-8"))
    assert "R59 proof of read" in item and "nonce or content hash" in item


def test_the_template_proof_check_refuses_the_sentence_moved_below_do_not():
    """Negative: the same check over a tmp copy with the R59 item moved under `## Do not` must fail."""
    text = (_REPO / "templates" / "lane-contract-template.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    first = next(n for n, ln in enumerate(lines) if "R59 proof of read" in ln)
    while not _ITEM_START.match(lines[first]):
        first -= 1
    last = first + 1
    while lines[last].strip():
        last += 1
    moved = lines[first:last]
    rest = lines[:first] + lines[last:]
    at = next(n for n, ln in enumerate(rest) if ln.startswith("## Do not"))
    mutated = "\n".join(rest[:at + 1] + moved + rest[at + 1:])
    assert "R59 proof of read" in mutated  # the phrase still exists; only its place changed
    item = _r59_item_in_done_contract(mutated)
    assert not ("R59 proof of read" in item and "nonce or content hash" in item)


def test_the_template_proof_check_refuses_unrelated_prose_adjacent_to_a_numbered_item():
    """Codex terra P1 (repair 2): the phrases split across a numbered item and flush-left prose
    after it are not one item, so the check must not accept them."""
    text = ("## Done-contract (immutable)\n\n"
            "n. **Close-out:** handback, and a nonce or content hash.\n"
            "The R59 proof of read is mentioned here in unrelated prose.\n\n"
            "## Do not\n")
    assert _r59_item_in_done_contract(text) == ""
    ok = ("## Done-contract (immutable)\n\n"
          "n. **Close-out:** the R59 proof of read:\n"
          "   a nonce or content hash.\n\n## Do not\n")
    item = _r59_item_in_done_contract(ok)
    assert "R59 proof of read" in item and "nonce or content hash" in item


# =====================================================================================================
# lane b2w2-transport-index ([#1439], batch B2-W3): the `by:` rule, in three classes.
#
# A NEW file of a role-written kind with no `by:` in its head is refused; a file that was already on
# the transport when the landing inventory was generated is only REPORTED (`no-by-predates-landing`
# when its sha256 still equals the inventory's, `EDITED-UNSIGNED` when it changed); a new file of a
# script-only kind is REPORTED (`no-by-generated-kind`). The inventory is written by
# `transport.py inventory --write` alone, never by the lint. Every test drives a synthetic transport
# in `tmp_path`; nothing here touches the real drive.
# =====================================================================================================

TA44 = "Tech-Architect-44 (R91)"
UNSIGNED = "plain text, no by line\n"


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _signed(line_no: int = 3) -> str:
    """A body whose flush-left `by:` sits on line `line_no` (1-based)."""
    lines = [f"filler {i}" for i in range(1, line_no)] + [f"by: {TA44}", "", "# body"]
    return "\n".join(lines) + "\n"


def _land(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _inventory_file(t, world, tmp_path: Path, name: str = "seat-ids.yaml") -> Path:
    """The generated landing inventory of everything currently on the fixture transport."""
    path = tmp_path / name
    t.write_seat_ids(path, seats=[], inventory=t.build_inventory(world["root"]))
    return path


# --- the finding carries a level; the rule is opt-in at the library level ----------------------------

def test_a_finding_has_a_level_that_defaults_to_refuse(lint):
    assert lint.Finding("a.md", "no-by", "why").level == "refuse"
    assert lint.Finding("a.md", "no-by-predates-landing", "why", "report").level == "report"
    assert lint.Finding("a.md", "no-by", "why").render() == "a.md: no-by: why"


def test_lint_text_without_require_by_is_unchanged(lint, registry):
    """`gen_lane_contract` and every other lint_text caller keep today's behaviour."""
    assert lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", UNSIGNED, registry) == []
    assert lint.lint_text("PLAN-x-v1.md", "to-cc", UNSIGNED, registry) == []
    assert lint.lint_text("LEDGER-x.md", "to-browser", UNSIGNED, registry) == []


# --- class (i): a NEW unsigned file -------------------------------------------------------------------

@pytest.mark.parametrize("name,folder", [
    ("PLAN-x-v1.md", "to-cc"),                  # a role-written hub kind
    ("GO-demo-2026-10-10.md", "to-cc"),
    ("DIGEST-x-2026-10-10.md", "to-browser"),   # a role-written `any` kind
    ("SESSION-lane-one.md", "to-browser"),
    ("QUESTION-seat1.md", "to-browser"),
])
def test_lint_by_new_unsigned_file_of_a_role_written_kind_is_refused(lint, registry, name, folder):
    found = lint.lint_text(name, folder, UNSIGNED, registry, require_by=True)
    assert [(f.code, f.level) for f in found] == [("no-by", "refuse")]
    assert "by:" in found[0].reason


@pytest.mark.parametrize("name,folder", [
    ("LEDGER-demo.md", "to-browser"),            # gen_ledger only
    ("LANE-END-demo.md", "to-browser"),          # transport_report only
    ("SEAT-BOOT-demo.md", "to-browser"),
])
def test_lint_by_new_unsigned_file_of_a_script_only_kind_is_reported_not_refused(lint, registry, name, folder):
    found = lint.lint_text(name, folder, UNSIGNED, registry, require_by=True)
    assert [(f.code, f.level) for f in found] == [("no-by-generated-kind", "report")]


@pytest.mark.parametrize("line_no,clean", [(1, True), (3, True), (11, True), (12, True), (13, False)])
def test_lint_by_reads_the_twelve_line_head(lint, registry, line_no, clean):
    found = lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", _signed(line_no), registry, require_by=True)
    assert (found == []) is clean


@pytest.mark.parametrize("text", [
    "by:\n# empty value\n",
    "by:    \n# blank value\n",
    "  by: indented\n# indented key\n",
    "> by: quoted\n# not flush-left\n",
    "<!-- by: comment -->\n# in a comment\n",
])
def test_lint_by_needs_a_flush_left_key_with_a_value(lint, registry, text):
    found = lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", text, registry, require_by=True)
    assert [f.code for f in found] == ["no-by"]


def test_lint_by_does_not_ask_a_non_md_file(lint, registry):
    for name in ("DIGEST-x.json", "DIGEST-x.yaml", "LANE-demo.CLAIMED-ab12cd"):
        folder = "to-cc" if name.startswith("LANE") else "to-browser"
        assert lint.lint_text(name, folder, "{}\n", registry, require_by=True) == [], name


def test_lint_by_composes_with_the_existing_findings(lint, registry):
    """A decision file with no `carried-by:` AND no `by:` reports both; the old finding is untouched."""
    found = lint.lint_text("AMEND-x-2026-10-10.md", "to-cc", "no heads here\nsecond line\n", registry,
                           require_by=True)
    assert sorted(f.code for f in found) == ["no-by", "no-carried-by"]
    ok = lint.lint_text("AMEND-x-2026-10-10.md", "to-cc", CONFORMING_DECISION.replace(
        "carried-by: OPEN\n", f"carried-by: OPEN\nby: {TA44}\n"), registry, require_by=True)
    assert ok == []


# --- the class of a path is decided by the inventory's path and sha256 --------------------------------

def test_file_class_is_new_pre_existing_or_edited(lint):
    inv = {"to-cc/A.md": "a" * 64, "ROOT.md": "b" * 64}
    assert lint.file_class("to-cc/A.md", "a" * 64, inv) == "pre-existing"
    assert lint.file_class("to-cc/A.md", "c" * 64, inv) == "edited"
    assert lint.file_class("to-cc/A.md", None, inv) == "edited"          # unreadable counts as edited
    assert lint.file_class("to-cc/B.md", "a" * 64, inv) == "new"
    assert lint.file_class("ROOT.md", "b" * 64, inv) == "pre-existing"   # the root's files carry no folder
    assert lint.file_class("to-cc/A.md", "a" * 64, None) == "new"        # no inventory: fail closed
    assert lint.file_class("to-cc/A.md", "a" * 64, {}) == "new"


@pytest.mark.parametrize("cls,name,code", [
    ("pre-existing", "DIGEST-x-2026-10-10.md", "no-by-predates-landing"),
    ("pre-existing", "LEDGER-demo.md", "no-by-predates-landing"),
    ("edited", "DIGEST-x-2026-10-10.md", "EDITED-UNSIGNED"),
    ("edited", "LEDGER-demo.md", "EDITED-UNSIGNED"),
])
def test_lint_by_pre_existing_and_edited_unsigned_files_are_reported_never_refused(lint, registry, cls, name, code):
    folder = "to-browser"
    found = lint.lint_text(name, folder, UNSIGNED, registry, require_by=True, file_class=cls)
    assert [(f.code, f.level) for f in found] == [(code, "report")]
    assert lint.lint_text(name, folder, _signed(), registry, require_by=True, file_class=cls) == []


def test_the_class_is_evaluated_only_for_an_unsigned_file(lint, registry):
    """The sha256 of a file is computed only when the file is unsigned AND in the inventory."""
    def boom():
        raise AssertionError("the class of a signed file was computed")

    assert lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", _signed(), registry,
                          require_by=True, file_class=boom) == []
    calls = []
    lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", UNSIGNED, registry, require_by=True,
                   file_class=lambda: calls.append(1) or "pre-existing")
    assert calls == [1]


def test_refuse_by_override_lets_the_gate_decide_from_the_writer(lint, registry):
    as_script = lint.lint_text("DIGEST-x-2026-10-10.md", "to-browser", UNSIGNED, registry,
                               require_by=True, refuse_by=False)
    assert [(f.code, f.level) for f in as_script] == [("no-by-generated-kind", "report")]
    as_role = lint.lint_text("LEDGER-demo.md", "to-browser", UNSIGNED, registry,
                             require_by=True, refuse_by=True)
    assert [(f.code, f.level) for f in as_role] == [("no-by", "refuse")]


# --- `check`: the three classes end to end ------------------------------------------------------------

def _by_world(t, world, tmp_path):
    """Four files landed, then the inventory generated, then one edited and three added:

    pre-existing unsigned DIGEST, edited unsigned DIGEST, edited unsigned LEDGER, signed-then-edited PLAN,
    then a NEW unsigned DIGEST, a NEW unsigned LEDGER and a NEW signed DIGEST."""
    _land(world["browser"] / "DIGEST-old-2026-10-01.md", UNSIGNED)
    _land(world["browser"] / "DIGEST-edited-2026-10-02.md", UNSIGNED)
    _land(world["browser"] / "LEDGER-edited.md", UNSIGNED)
    _land(world["cc"] / "PLAN-signed-v1.md", _signed())
    inv_path = _inventory_file(t, world, tmp_path)
    _land(world["browser"] / "DIGEST-edited-2026-10-02.md", UNSIGNED + "an edit\n")
    _land(world["browser"] / "LEDGER-edited.md", UNSIGNED + "an edit\n")
    _land(world["cc"] / "PLAN-signed-v1.md", _signed() + "an edit\n")
    _land(world["browser"] / "DIGEST-new-2026-10-10.md", UNSIGNED)
    _land(world["browser"] / "LEDGER-new.md", UNSIGNED)
    _land(world["browser"] / "DIGEST-new-signed-2026-10-10.md", _signed())
    return inv_path


def _check(lint, world, inv_path, name, capsys, *extra):
    folder = "to-cc" if name.startswith(("PLAN", "GO")) else "to-browser"
    path = world["root"] / folder / name
    rc = lint.main(["check", "--inventory", str(inv_path), *extra, str(path)])
    return rc, capsys.readouterr().out


def test_check_classifies_a_path_by_the_inventory_and_exits_1_only_for_a_new_unsigned_role_file(
        t, lint, world, tmp_path, capsys):
    inv = _by_world(t, world, tmp_path)
    rc, out = _check(lint, world, inv, "DIGEST-new-2026-10-10.md", capsys)
    assert rc == 1 and "no-by" in out and "predates" not in out
    rc, out = _check(lint, world, inv, "DIGEST-old-2026-10-01.md", capsys)
    assert rc == 0 and "no-by-predates-landing" in out
    rc, out = _check(lint, world, inv, "DIGEST-edited-2026-10-02.md", capsys)
    assert rc == 0 and "EDITED-UNSIGNED" in out
    rc, out = _check(lint, world, inv, "LEDGER-edited.md", capsys)
    assert rc == 0 and "EDITED-UNSIGNED" in out                     # a script-only kind, edited
    rc, out = _check(lint, world, inv, "LEDGER-new.md", capsys)
    assert rc == 0 and "no-by-generated-kind" in out
    rc, out = _check(lint, world, inv, "PLAN-signed-v1.md", capsys)
    assert rc == 0 and "ok" in out                                   # signed, edited: clean
    rc, out = _check(lint, world, inv, "DIGEST-new-signed-2026-10-10.md", capsys)
    assert rc == 0 and "ok" in out


def test_check_exits_1_when_a_refused_file_sits_among_reported_ones(t, lint, world, tmp_path, capsys):
    inv = _by_world(t, world, tmp_path)
    files = [world["browser"] / n for n in ("DIGEST-old-2026-10-01.md", "LEDGER-new.md", "DIGEST-new-2026-10-10.md")]
    assert lint.main(["check", "--inventory", str(inv), *map(str, files)]) == 1
    out = capsys.readouterr().out
    assert "no-by-predates-landing" in out and "no-by-generated-kind" in out and "DIGEST-new-2026-10-10.md: no-by" in out
    assert lint.main(["check", "--inventory", str(inv), *map(str, files[:2])]) == 0


def test_a_missing_or_unreadable_inventory_fails_closed(t, lint, world, tmp_path, capsys):
    """No readable inventory means every file counts as new, so the pre-existing unsigned role file is refused."""
    _land(world["browser"] / "DIGEST-old-2026-10-01.md", UNSIGNED)
    old = world["browser"] / "DIGEST-old-2026-10-01.md"
    assert lint.main(["check", "--inventory", str(tmp_path / "missing.yaml"), str(old)]) == 1
    captured = capsys.readouterr()
    assert "no-by" in captured.out and "inventory" in captured.err
    bad = tmp_path / "bad.yaml"
    bad.write_text("landing_inventory: [\n", encoding="utf-8")
    assert lint.main(["check", "--inventory", str(bad), str(old)]) == 1
    nomap = tmp_path / "nomap.yaml"
    nomap.write_text("seats: []\n", encoding="utf-8")
    assert lint.main(["check", "--inventory", str(nomap), str(old)]) == 1


def test_the_by_rule_is_off_outside_the_known_transport_unless_an_inventory_is_named(
        t, lint, world, tmp_path, capsys, monkeypatch):
    """Today's `check` and `sweep` behaviour for a scratch tree is unchanged."""
    monkeypatch.setattr(t, "known_root", lambda: tmp_path / "elsewhere")
    f = _land(world["browser"] / "DIGEST-plain-2026-10-10.md", UNSIGNED)
    assert lint.main(["check", str(f)]) == 0
    assert "ok" in capsys.readouterr().out
    assert lint.main(["sweep", "--transport-root", str(world["root"])]) == 0
    capsys.readouterr()


def test_the_by_rule_is_on_inside_the_known_transport_with_the_default_inventory(
        t, lint, world, tmp_path, capsys, monkeypatch):
    old = _land(world["browser"] / "DIGEST-old-2026-10-01.md", UNSIGNED)
    inv = _inventory_file(t, world, tmp_path)
    new = _land(world["browser"] / "DIGEST-new-2026-10-10.md", UNSIGNED)
    monkeypatch.setattr(t, "known_root", lambda: world["root"])
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", inv)
    assert lint.main(["check", str(old)]) == 0
    assert "no-by-predates-landing" in capsys.readouterr().out
    assert lint.main(["check", str(new)]) == 1
    capsys.readouterr()
    assert lint.main(["sweep", "--transport-root", str(world["root"])]) == 1
    assert "DIGEST-new-2026-10-10.md" in capsys.readouterr().out


# --- `sweep` ---------------------------------------------------------------------------------------------

def test_sweep_reports_by_findings_with_levels(t, lint, registry, world, tmp_path):
    inv_path = _by_world(t, world, tmp_path)
    inv = t.load_inventory(inv_path)
    found = lint.sweep(world["root"], registry=registry, require_by=True, inventory=inv)
    by_path = {f.path: f for f in found}
    assert (by_path["to-browser/DIGEST-new-2026-10-10.md"].code,
            by_path["to-browser/DIGEST-new-2026-10-10.md"].level) == ("no-by", "refuse")
    assert (by_path["to-browser/LEDGER-new.md"].code, by_path["to-browser/LEDGER-new.md"].level) == (
        "no-by-generated-kind", "report")
    assert by_path["to-browser/DIGEST-old-2026-10-01.md"].code == "no-by-predates-landing"
    assert by_path["to-browser/DIGEST-edited-2026-10-02.md"].code == "EDITED-UNSIGNED"
    assert by_path["to-browser/LEDGER-edited.md"].code == "EDITED-UNSIGNED"
    assert "to-cc/PLAN-signed-v1.md" not in by_path and "to-browser/DIGEST-new-signed-2026-10-10.md" not in by_path
    assert {f.path for f in found if f.level == "refuse"} == {"to-browser/DIGEST-new-2026-10-10.md"}
    assert lint.sweep(world["root"], registry=registry) == []             # the default is the old sweep


def test_sweep_cli_counts_predating_files_and_prints_them_with_the_flag(t, lint, world, tmp_path, capsys):
    inv = _by_world(t, world, tmp_path)
    (world["browser"] / "DIGEST-new-2026-10-10.md").unlink()              # leave no refused file
    args = ["sweep", "--transport-root", str(world["root"]), "--inventory", str(inv)]
    assert lint.main(args) == 0
    captured = capsys.readouterr()
    assert "no-by-predates-landing" not in captured.out                  # counted, not listed
    assert "EDITED-UNSIGNED" in captured.out and "no-by-generated-kind" in captured.out
    assert re.search(r"1 .*predat", captured.err)
    assert lint.main([*args, "--report-predating"]) == 0
    assert "DIGEST-old-2026-10-01.md: no-by-predates-landing" in capsys.readouterr().out


# --- the inventory is generated, deterministic, and never rewritten by the lint ----------------------------

def test_the_inventory_is_never_rewritten_by_check_sweep_or_the_gate(t, lint, world, tmp_path, monkeypatch, capsys):
    inv = _by_world(t, world, tmp_path)
    before = inv.read_bytes()
    lint.main(["check", "--inventory", str(inv), str(world["browser"] / "DIGEST-new-2026-10-10.md")])
    lint.main(["sweep", "--transport-root", str(world["root"]), "--inventory", str(inv)])
    monkeypatch.setattr(t, "known_root", lambda: world["root"])
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", inv)
    t.write("operator", world["browser"] / "DIGEST-gated-2026-10-10.md", _signed())
    with pytest.raises(t.TransportWriteRefused):
        t.write("operator", world["browser"] / "DIGEST-refused-2026-10-10.md", UNSIGNED)
    capsys.readouterr()
    assert inv.read_bytes() == before


def test_the_inventory_command_output_equals_a_fresh_generation_and_is_byte_stable(t, world, tmp_path):
    _by_world(t, world, tmp_path)
    seat_file = tmp_path / "gen.yaml"
    t.write_seat_ids(seat_file, seats=[], inventory={})
    args = ["--transport-root", str(world["root"]), "--seat-ids", str(seat_file)]
    assert t.main(["inventory", "--write", *args]) == 0
    first = seat_file.read_bytes()
    assert t.main(["inventory", "--write", *args]) == 0
    assert seat_file.read_bytes() == first
    fresh = tmp_path / "fresh.yaml"
    t.write_seat_ids(fresh, seats=[], inventory=t.build_inventory(world["root"]))
    assert fresh.read_bytes() == first
    assert t.load_inventory(seat_file)["to-browser/DIGEST-new-2026-10-10.md"] == _sha(UNSIGNED)
