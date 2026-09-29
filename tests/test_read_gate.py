"""A read counts only when its output exists, its log is clean and every quotation is
literally in the source (LANE-5B5-11, AMEND v3 "Add: N5-11 -- the read gate, with
fall-through"). No course text anywhere in this file -- every fixture is synthetic, built by
`tests/fixtures/read_gate/synth.py` at run time.

THE RED-FIRST WITNESS (DONE-ITEM 3) is the three tests in `TestDoneWhenItem3RedFirst`: (a) a
SUCCESS status with a missing output file is rejected and falls through; (b) a paraphrase in
quotation marks is rejected; (c) a faithful read is accepted on the first route. Run against a
stub verifier that accepts every read (see that class's docstring), all three fail -- that
failure, captured on `origin/main` before this module existed, is the RED half; green is this
suite passing against the real `verify_read`/`run_read_gate` on this lane's tip.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "read_gate"))
import synth  # noqa: E402 -- must follow the sys.path insert above

import read_gate as gate


# --- quotation extraction / whitespace normalization (module docstring's own definition) ----


def test_extract_quotations_finds_straight_quotes() -> None:
    assert gate.extract_quotations('He said "hello world" today.') == ["hello world"]


def test_extract_quotations_finds_curly_quotes() -> None:
    assert gate.extract_quotations("She said “good morning”.") == ["good morning"]


def test_extract_quotations_normalizes_internal_whitespace() -> None:
    assert gate.extract_quotations('"line one\n   line two"') == ["line one line two"]


def test_extract_quotations_returns_empty_list_when_none_present() -> None:
    assert gate.extract_quotations("no quotes here at all") == []


# --- the verifier's three checks, each with its own test (DONE-ITEM 1) -----------------------


def test_verify_read_rejects_a_missing_output_file(tmp_path: Path) -> None:
    verdict = gate.verify_read(None, "", "the source text")
    assert not verdict.accepted
    assert verdict.failed_check == "output-file-missing-or-empty"


def test_verify_read_rejects_an_empty_output_file(tmp_path: Path) -> None:
    output = tmp_path / "out.txt"
    output.write_text("", encoding="utf-8")
    verdict = gate.verify_read(output, "", "the source text")
    assert not verdict.accepted
    assert verdict.failed_check == "output-file-missing-or-empty"


def test_verify_read_rejects_a_log_carrying_a_print_timeout(tmp_path: Path) -> None:
    output = tmp_path / "out.txt"
    output.write_text('"the source text"', encoding="utf-8")
    verdict = gate.verify_read(output, "hit a PRINT TIMEOUT after 20m", "the source text")
    assert not verdict.accepted
    assert verdict.failed_check == "print-timeout-in-log"


def test_verify_read_rejects_a_quotation_not_literally_in_the_source(tmp_path: Path) -> None:
    output = tmp_path / "out.txt"
    output.write_text('"a paraphrase of the source"', encoding="utf-8")
    verdict = gate.verify_read(output, "", "the actual source text")
    assert not verdict.accepted
    assert verdict.failed_check is not None
    assert verdict.failed_check.startswith("quotation-not-in-source:")


def test_verify_read_accepts_a_literal_quotation_whitespace_normalized(tmp_path: Path) -> None:
    output = tmp_path / "out.txt"
    output.write_text('"the  actual\nsource   text"', encoding="utf-8")
    verdict = gate.verify_read(output, "", "the actual source text, and more")
    assert verdict.accepted
    assert verdict.failed_check is None


def test_verify_read_rejects_output_with_no_quotations_at_all(tmp_path: Path) -> None:
    """Codex terra CRITICAL (`docs/audits/2026-09-29-codex-lane-read-gate.md`): the three
    AMEND checks alone accept a paraphrase that carries no quotation marks at all, since
    "every quotation is literal" is vacuously true of an empty set. Strengthened, never
    weakened (ADR-108 SS B)."""
    output = tmp_path / "out.txt"
    output.write_text("a summary with no quoted spans", encoding="utf-8")
    verdict = gate.verify_read(output, "", "anything")
    assert not verdict.accepted
    assert verdict.failed_check == "no-quotation-in-output"


def test_verify_read_propagates_a_decode_error_reading_the_output(tmp_path: Path) -> None:
    """The output path exists and is non-empty, but is not valid UTF-8 -- `verify_read`
    itself raises; `run_read_gate` is the layer that must catch this (see the run_read_gate
    tests below), not `verify_read`."""
    output = tmp_path / "not-utf8.txt"
    output.write_bytes(b"\xff\xfe\x00invalid")
    with pytest.raises(UnicodeDecodeError):
        gate.verify_read(output, "", "anything")


# --- extraction per format, each on a synthetic fixture generated here (DONE-ITEM 1) ---------


def test_extract_source_text_reads_a_synthetic_pdf(tmp_path: Path) -> None:
    fixture = synth.write_pdf_fixture(tmp_path / "doc.pdf", "The quick brown fox.")
    assert "The quick brown fox." in gate.extract_source_text(fixture)


def test_extract_source_text_reads_a_synthetic_epub(tmp_path: Path) -> None:
    fixture = synth.write_epub_fixture(tmp_path / "book.epub", "A synthetic epub paragraph.")
    assert "A synthetic epub paragraph." in gate.extract_source_text(fixture)


def test_extract_source_text_reads_plain_text_as_is(tmp_path: Path) -> None:
    fixture = synth.write_text_fixture(tmp_path / "note.txt", "Plain text, verbatim.")
    assert gate.extract_source_text(fixture) == "Plain text, verbatim."


# --- the route runner reads roles.read at run time (DONE-ITEM 2) -----------------------------


def _write_registry(path: Path, providers: list[str]) -> Path:
    order = [{"provider": p} for p in providers]
    path.write_text(
        yaml.safe_dump({"roles": {"read": {"order": order}}}), encoding="utf-8"
    )
    return path


def test_load_read_routes_reads_the_declared_order(tmp_path: Path) -> None:
    registry = _write_registry(tmp_path / "registry.yaml", ["antigravity", "anthropic"])
    routes = gate.load_read_routes(registry)
    assert [r.provider for r in routes] == ["antigravity", "anthropic"]


def test_load_read_routes_changes_order_when_the_fixture_registry_reorders_it(
    tmp_path: Path,
) -> None:
    """A test that reorders a fixture registry and sees the order change (DONE-ITEM 2)."""
    registry_a = _write_registry(tmp_path / "a.yaml", ["antigravity", "copilot-enterprise"])
    registry_b = _write_registry(tmp_path / "b.yaml", ["copilot-enterprise", "antigravity"])
    order_a = [r.provider for r in gate.load_read_routes(registry_a)]
    order_b = [r.provider for r in gate.load_read_routes(registry_b)]
    assert order_a == ["antigravity", "copilot-enterprise"]
    assert order_b == ["copilot-enterprise", "antigravity"]
    assert order_a != order_b


def test_load_read_routes_never_names_gemini_as_a_route() -> None:
    """The batch's own rule: "The `gemini` CLI is not a route." Checked against the real
    registry, not a fixture -- this is the one test in this file that reads a real repo file,
    because it is asserting a fact ABOUT that file, not exercising the mechanism."""
    routes = gate.load_read_routes(gate.REPO_ROOT / gate.REGISTRY_REL)
    assert "gemini" not in [r.provider for r in routes]


def _fixture_registry(tmp_path: Path, providers: list[str]) -> Path:
    return _write_registry(tmp_path / "registry.yaml", providers)


class TestDoneWhenItem3RedFirst:
    """Each test below is run twice: once against `_stub_invoker`-driven real code (GREEN,
    the assertions as written), and once -- for the close-out's RED-first witness -- with
    `verify_read` monkeypatched to a stub that accepts every read unconditionally (RED: each
    assertion below fails, because the stub wrongly accepts what should be rejected). That
    swap is done by hand at close-out, captured as pasted output, and is not part of this
    file's permanent behavior -- this class's job is only to state the three fixtures and the
    correct (green) verdict."""

    def test_a_success_with_no_output_file_is_rejected_and_falls_through(
        self, tmp_path: Path
    ) -> None:
        registry = _fixture_registry(tmp_path, ["antigravity", "anthropic"])
        source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
        workdir = tmp_path / "work"
        workdir.mkdir()
        ledger = tmp_path / "ledger.jsonl"

        def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
            if route.provider == "antigravity":
                # SUCCESS status, but no output file was ever written -- the N5-7 defect.
                return gate.InvokeAttempt(None, log_text="", status="SUCCESS")
            output = _workdir / "anthropic.output.txt"
            output.write_text('"The literal source text."', encoding="utf-8")
            return gate.InvokeAttempt(output, log_text="", status="SUCCESS")

        result = gate.run_read_gate(
            source, registry_path=registry, invoke=invoke, workdir=workdir,
            ledger_path=ledger,
        )
        assert result.accepted
        assert result.served_route == "anthropic"
        assert [a.route for a in result.attempts] == ["antigravity", "anthropic"]
        assert result.attempts[0].verdict == "rejected"
        assert result.attempts[0].failed_check == "output-file-missing-or-empty"

    def test_a_paraphrase_in_quotation_marks_is_rejected(self, tmp_path: Path) -> None:
        registry = _fixture_registry(tmp_path, ["antigravity"])
        source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
        workdir = tmp_path / "work"
        workdir.mkdir()
        ledger = tmp_path / "ledger.jsonl"

        def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
            output = _workdir / f"{route.provider}.output.txt"
            output.write_text('"a paraphrased version of the text"', encoding="utf-8")
            return gate.InvokeAttempt(output, log_text="", status="SUCCESS")

        result = gate.run_read_gate(
            source, registry_path=registry, invoke=invoke, workdir=workdir,
            ledger_path=ledger,
        )
        assert not result.accepted
        assert result.attempts[0].failed_check.startswith("quotation-not-in-source:")

    def test_a_faithful_read_is_accepted_on_the_first_route(self, tmp_path: Path) -> None:
        registry = _fixture_registry(tmp_path, ["antigravity", "anthropic"])
        source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
        workdir = tmp_path / "work"
        workdir.mkdir()
        ledger = tmp_path / "ledger.jsonl"
        calls = []

        def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
            calls.append(route.provider)
            output = _workdir / f"{route.provider}.output.txt"
            output.write_text('"The literal source text."', encoding="utf-8")
            return gate.InvokeAttempt(output, log_text="", status="SUCCESS")

        result = gate.run_read_gate(
            source, registry_path=registry, invoke=invoke, workdir=workdir,
            ledger_path=ledger,
        )
        assert result.accepted
        assert result.served_route == "antigravity"
        assert calls == ["antigravity"]  # never fell through to the second route


def test_run_read_gate_falls_through_on_every_route_and_names_each_failed_check(
    tmp_path: Path,
) -> None:
    registry = _fixture_registry(tmp_path, ["antigravity", "copilot-enterprise"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    ledger = tmp_path / "ledger.jsonl"

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        return gate.InvokeAttempt(None, log_text="", status="FAILED")

    result = gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    assert not result.accepted
    assert result.served_route is None
    assert [a.route for a in result.attempts] == ["antigravity", "copilot-enterprise"]
    assert all(a.failed_check == "output-file-missing-or-empty" for a in result.attempts)
    assert result.failure_summary() == (
        "antigravity: output-file-missing-or-empty; "
        "copilot-enterprise: output-file-missing-or-empty"
    )


def test_run_read_gate_falls_through_when_the_invoker_raises(tmp_path: Path) -> None:
    registry = _fixture_registry(tmp_path, ["antigravity", "anthropic"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    ledger = tmp_path / "ledger.jsonl"

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        if route.provider == "antigravity":
            raise OSError("agy not found")
        output = _workdir / "anthropic.output.txt"
        output.write_text('"The literal source text."', encoding="utf-8")
        return gate.InvokeAttempt(output, log_text="", status="SUCCESS")

    result = gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    assert result.accepted
    assert result.served_route == "anthropic"
    assert result.attempts[0].failed_check == "invoke-error:agy not found"


def test_run_read_gate_ignores_a_stale_or_foreign_path_an_invoker_claims(tmp_path: Path) -> None:
    """Codex terra HIGH (`docs/audits/2026-09-29-codex-lane-read-gate.md`): the runner must
    own each attempt's output path, not trust whatever path an `InvokeAttempt` names. A
    misbehaving invoker that points at a leftover file from an earlier attempt, or at the
    source file itself, must not be read back as this attempt's real output."""
    registry = _fixture_registry(tmp_path, ["antigravity"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    ledger = tmp_path / "ledger.jsonl"
    foreign = workdir / "leftover-from-a-different-run.txt"
    foreign.write_text('"a stale accepted-looking quote"', encoding="utf-8")

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        # Never writes to `_workdir / "antigravity.output.txt"` -- claims the foreign path.
        return gate.InvokeAttempt(foreign, log_text="", status="SUCCESS")

    result = gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    assert not result.accepted
    assert result.attempts[0].failed_check == "output-file-missing-or-empty"


def test_run_read_gate_clears_a_route_leftover_before_invoking_it(tmp_path: Path) -> None:
    """A file left at the canonical path by an earlier run must not be read back as THIS
    attempt's output when the invoker writes nothing this time."""
    registry = _fixture_registry(tmp_path, ["antigravity"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    (workdir / "antigravity.output.txt").write_text(
        '"a leftover quote from a prior run"', encoding="utf-8"
    )
    ledger = tmp_path / "ledger.jsonl"

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        return gate.InvokeAttempt(None, log_text="", status="FAILED")  # writes nothing

    result = gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    assert not result.accepted
    assert result.attempts[0].failed_check == "output-file-missing-or-empty"


def test_run_read_gate_rejects_rather_than_raises_on_an_unreadable_output(tmp_path: Path) -> None:
    """A route whose canonical output path exists but cannot be decoded as UTF-8 text is
    rejected and falls through instead of aborting the whole run."""
    registry = _fixture_registry(tmp_path, ["antigravity", "anthropic"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    ledger = tmp_path / "ledger.jsonl"

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        expected = _workdir / f"{route.provider}.output.txt"
        if route.provider == "antigravity":
            expected.write_bytes(b"\xff\xfe\x00invalid")
            return gate.InvokeAttempt(expected, log_text="", status="SUCCESS")
        expected.write_text('"The literal source text."', encoding="utf-8")
        return gate.InvokeAttempt(expected, log_text="", status="SUCCESS")

    result = gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    assert result.accepted
    assert result.served_route == "anthropic"
    assert result.attempts[0].failed_check.startswith("verify-error:")


# --- the real CLI invoker: injectable runner, no test calls a real reader --------------------


def _fake_runner(returncode: int = 0, stdout: str = "", stderr: str = ""):
    import subprocess as sp

    def runner(argv, **kwargs):
        return sp.CompletedProcess(argv, returncode, stdout=stdout, stderr=stderr)

    return runner


def test_cli_invoker_passes_devnull_stdin_so_it_cannot_hang_on_a_waiting_cli(
    tmp_path: Path,
) -> None:
    """Codex terra HIGH: a CLI that waits on stdin must not stall the route."""
    seen: dict = {}

    def capturing_runner(argv, **kwargs):
        seen["kwargs"] = kwargs
        import subprocess as sp
        return sp.CompletedProcess(argv, 0, stdout="", stderr="")

    invoke = gate._cli_invoker("agy", gate._agy_argv, 5, runner=capturing_runner)
    invoke(gate.RouteSpec("antigravity"), tmp_path / "source.txt", tmp_path)
    assert seen["kwargs"]["stdin"] == gate.subprocess.DEVNULL


def test_cli_invoker_reports_unavailable_when_the_binary_is_missing(tmp_path: Path) -> None:
    def raising_runner(argv, **kwargs):
        raise OSError("agy not found")

    invoke = gate._cli_invoker("agy", gate._agy_argv, 5, runner=raising_runner)
    attempt = invoke(gate.RouteSpec("antigravity"), tmp_path / "source.txt", tmp_path)
    assert attempt.output_path is None
    assert attempt.status == "unavailable"


def test_cli_invoker_reports_unavailable_on_a_timeout(tmp_path: Path) -> None:
    def timing_out_runner(argv, **kwargs):
        raise gate.subprocess.TimeoutExpired(cmd=argv, timeout=5)

    invoke = gate._cli_invoker("agy", gate._agy_argv, 5, runner=timing_out_runner)
    attempt = invoke(gate.RouteSpec("antigravity"), tmp_path / "source.txt", tmp_path)
    assert attempt.output_path is None
    assert attempt.status == "unavailable"


def test_cli_invoker_reports_no_output_file_when_the_cli_writes_nothing(tmp_path: Path) -> None:
    """Non-JSON or empty CLI stdout does not crash this path -- the output file's presence is
    the only thing that matters, and this run writes none."""
    invoke = gate._cli_invoker(
        "agy", gate._agy_argv, 5, runner=_fake_runner(stdout="not json at all")
    )
    attempt = invoke(gate.RouteSpec("antigravity"), tmp_path / "source.txt", tmp_path)
    assert attempt.output_path is None
    assert attempt.status == "exit=0"


def test_real_invoker_refuses_the_anthropic_route_rather_than_fabricating_a_read(
    tmp_path: Path,
) -> None:
    """Codex terra CRITICAL: `real_invoker` must not auto-accept the live-terminal-fallback
    route with manufactured content. A caller that wants it answered supplies its own
    invoker for that one entry."""
    with pytest.raises(gate.ReadGateError, match="not automatable"):
        gate.real_invoker(gate.RouteSpec("anthropic", model="claude-sonnet-5"),
                           tmp_path / "source.txt", tmp_path)


# --- the outcome ledger: one line per read (DONE-ITEM 4) -------------------------------------


def test_run_read_gate_appends_one_ledger_line_per_route_attempted(tmp_path: Path) -> None:
    registry = _fixture_registry(tmp_path, ["antigravity", "anthropic"])
    source = synth.write_text_fixture(tmp_path / "source.txt", "The literal source text.")
    workdir = tmp_path / "work"
    workdir.mkdir()
    ledger = tmp_path / "ledger.jsonl"

    def invoke(route: gate.RouteSpec, _source: Path, _workdir: Path) -> gate.InvokeAttempt:
        if route.provider == "antigravity":
            return gate.InvokeAttempt(None, log_text="", status="FAILED")
        output = _workdir / "anthropic.output.txt"
        output.write_text('"The literal source text."', encoding="utf-8")
        return gate.InvokeAttempt(output, log_text="", status="SUCCESS")

    gate.run_read_gate(
        source, registry_path=registry, invoke=invoke, workdir=workdir, ledger_path=ledger
    )
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    import json

    rows = [json.loads(line) for line in lines]
    assert rows[0]["route"] == "antigravity"
    assert rows[0]["verdict"] == "rejected"
    assert rows[0]["failed_check"] == "output-file-missing-or-empty"
    assert rows[1]["route"] == "anthropic"
    assert rows[1]["verdict"] == "accepted"
    assert rows[1]["failed_check"] is None
    expected_sha = gate.hashlib.sha256(source.read_bytes()).hexdigest()
    assert rows[0]["source_sha256"] == expected_sha == rows[1]["source_sha256"]


def test_ledger_append_is_never_a_rewrite(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text('{"pre-existing": true}\n', encoding="utf-8")
    outcome = gate.RouteOutcome("anthropic", "accepted", None)
    gate._append_ledger(ledger, outcome, "deadbeef")
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert lines[0] == '{"pre-existing": true}'
    assert len(lines) == 2
