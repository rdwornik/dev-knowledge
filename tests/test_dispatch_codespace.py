"""`scripts/dispatch.py`'s codespace exec/harvest/stop/delete legs (LANE-5B4-10).

RED-FIRST: written and first run against a tree with none of `run_gh`, `codespace_exec`,
`codespace_harvest`, `verify_harvest_manifest`, `codespace_stop` or `codespace_delete` defined
(import/attribute error) -- see the lane's session file for the RED transcript.

Every test drives these functions through the `invoker` seam (ported from `Invoke-CodespaceGh`'s
own `-Invoker`), never a real `gh` binary or a real codespace -- the same doctrine
`test_codespace_admission.py` states for its own `Probe` seam: a transport that can only be
exercised by really provisioning a machine is a transport whose guards are never tested.

The machine/idle defaults the first tests read are the 1:1 condition's substrate (`[#1335]`, lane
b2-codespace-1to1, ADR-126 D2).

R17's own test is `TestCodespaceDelete`: delete is refused when the manifest is missing or a hash
differs, and allowed when it verifies -- and in the refusal case, `gh` is never called at all.
"""
from __future__ import annotations

import copy
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import asdict as _asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import codespace_regime as _regime
import dispatch as d
from fake_agy import FAKE_CODE, FAKE_URL, FakeAgy, FakeClock
cs = d.cs


@pytest.fixture(autouse=True)
def _private_receipt_homes(tmp_path_factory, monkeypatch):
    """Every exec/delete now writes step rows and regime rows: a test that names no seam must never
    reach the operator's `~/.claude/remote-runs` or the tracked `logs/CODESPACE-RECEIPTS.jsonl`."""
    root = tmp_path_factory.mktemp("receipt-homes")
    monkeypatch.setattr(d, "DEFAULT_HARVEST_ROOT", root / "remote-runs")
    # `dispatch` and this file may hold two module objects of the regime (`scripts.codespace_regime` and
    # `codespace_regime`): the default ledger is read from whichever one the code calls, so patch all
    for mod in {id(m): m for m in (_regime, d.regime, sys.modules.get("scripts.codespace_regime"),
                                   sys.modules.get("codespace_regime")) if m is not None}.values():
        monkeypatch.setattr(mod, "_REPO_ROOT", root / "repo")


@pytest.fixture(autouse=True)
def _pre_launch_cleared(monkeypatch):
    """P1-B04 (`e2-subst-gate`): `codespace-exec` now runs `moment:pre-launch` before it touches gh. The
    tests below exercise what comes AFTER that step with stub contracts, so the moment is stubbed
    open here; its refusal, and its ordering before `codespace_exec`, are witnessed in
    `tests/test_dispatch_subst_prelaunch.py`."""
    monkeypatch.setattr(d, "run_prelaunch", lambda *a, **k: d.PreLaunch(True))


# ---------------------------------------------------------------------------------------------
# run_gh / format_gh_line
# ---------------------------------------------------------------------------------------------

def test_retention_defaults_are_valid_go_durations_not_a_day_suffix():
    """Measured against the REAL `gh codespace create` (not the invoker seam, 2026-09-27): its
    `--retention-period` flag parses Go's `time.Duration` grammar (digits + h/m/s), which has NO
    `d` unit -- `retention: str = "1d"` failed every real call with `unknown unit "d"`, a bug no
    invoker-faked unit test could ever catch. `codespace_plan`, `codespace_exec` and the
    `codespace-exec` CLI's own `--retention` default all share this constant so it cannot drift
    back to a day suffix in only one of the three."""
    import inspect

    go_duration = re.compile(r"^\d+[hms]$")
    for default in (
        inspect.signature(d.codespace_plan).parameters["retention"].default,
        inspect.signature(d.codespace_exec).parameters["retention"].default,
    ):
        assert go_duration.match(default), default
    cli_default = next(p.default for p in d.codespace_exec_cmd.params if p.name == "retention")
    assert go_duration.match(cli_default), cli_default


def test_machine_and_idle_defaults_are_the_adr_126_d2_pair_in_all_three_places():
    """ADR-126 D2 / R63 (lane b2-codespace-1to1): a Codespace lane defaults to the 4-core
    `standardLinux32gb` machine and a 240-minute idle timeout. RED on `e67f27ac`, where all three
    sites read `basicLinux32gb` / `30m` (a 2-core box that idles out in half an hour). The three
    sites are `codespace_plan`, `codespace_exec` and the `codespace-exec` CLI's own options;
    asserting each one keeps a fourth copy from drifting back to the old pair in only one place."""
    import inspect

    sites = {
        "codespace_plan": inspect.signature(d.codespace_plan).parameters,
        "codespace_exec": inspect.signature(d.codespace_exec).parameters,
        "codespace-exec CLI": {p.name: p for p in d.codespace_exec_cmd.params},
    }
    for site, params in sites.items():
        assert params["machine"].default == "standardLinux32gb", site
        assert params["idle_timeout"].default == "240m", site


def test_a_default_plan_creates_the_four_core_machine_with_the_long_idle_timeout():
    """The defaults reach the `gh codespace create` argv, not only the signature."""
    steps = d.codespace_plan("o/r", "main", "slug", Path("contract.md"), ["claude", "-p", "x"])
    create = steps[0].argv
    assert create[create.index("--machine") + 1] == "standardLinux32gb"
    assert create[create.index("--idle-timeout") + 1] == "240m"


def test_the_idle_default_is_a_valid_go_duration_within_the_codespaces_ceiling():
    """`gh codespace create --idle-timeout` parses Go's duration grammar and GitHub caps idle at
    four hours -- 240 minutes is the ceiling, so a default above it would be refused at create."""
    import inspect

    default = inspect.signature(d.codespace_plan).parameters["idle_timeout"].default
    match = re.fullmatch(r"(\d+)m", default)
    assert match and int(match.group(1)) <= 240, default


def test_format_gh_line_quotes_only_when_needed():
    assert d.format_gh_line(["codespace", "stop", "-c", "fluffy-1"]) == \
        "gh codespace stop -c fluffy-1"


def test_format_gh_line_quotes_a_space_and_escapes_a_quote():
    line = d.format_gh_line(["codespace", "ssh", "-c", "fluffy-1", "--", 'a "quoted" arg'])
    assert '"a ""quoted"" arg"' in line


def test_run_gh_uses_the_invoker_seam_and_never_shells_out():
    calls = []

    def fake(argv):
        calls.append(list(argv))
        return d.GhResult(ok=True, exit_code=0, stdout="hello")

    res = d.run_gh(["codespace", "list"], invoker=fake)
    assert res.ok and res.stdout == "hello"
    assert calls == [["codespace", "list"]]


def test_run_gh_returns_a_result_when_gh_is_missing_rather_than_raising(monkeypatch):
    """Codex terra P1 (2026-09-27): an unrunnable `gh` used to raise `FileNotFoundError` out of
    every codespace command instead of taking its documented refusal path."""

    def raise_missing(*_args, **_kwargs):
        raise FileNotFoundError("no such file or directory: 'gh'")

    monkeypatch.setattr(d.subprocess, "run", raise_missing)
    result = d.run_gh(["codespace", "list"])
    assert not result.ok
    assert result.exit_code == 127
    assert "gh could not be run" in result.stdout


def test_run_gh_converts_a_timeout_into_a_refusal_rather_than_hanging(monkeypatch):
    """Codex terra P1 (2026-09-27): a stalled `gh` (an auth prompt with no TTY, a hung network
    call) had no bound at all -- every codespace command blocked indefinitely instead of taking
    its documented refusal path."""

    def raise_timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd=["gh"], timeout=d.GH_TIMEOUT_SECONDS)

    monkeypatch.setattr(d.subprocess, "run", raise_timeout)
    result = d.run_gh(["codespace", "ssh", "-c", "fluffy-1"])
    assert not result.ok
    assert result.exit_code == 124
    assert "timed out" in result.stdout


def test_run_gh_keeps_stderr_separate_from_stdout(monkeypatch):
    """Codex terra P1 (2026-09-27): a real `gh codespace create` that also writes progress or
    warnings to stderr must not have them appended to `stdout` -- that value becomes the NAME
    every later `-c` call keys on, and a harvested `cat`'s stderr would otherwise be hashed into
    the manifest as if it were the file's own content."""

    class _FakeCompleted:
        returncode = 0
        stdout = "fluffy-space-1\n"
        stderr = "some progress line\n"

    monkeypatch.setattr(d.subprocess, "run", lambda *a, **k: _FakeCompleted())
    result = d.run_gh(["codespace", "create"])
    assert result.ok
    assert result.stdout == "fluffy-space-1\n"
    assert result.stderr == "some progress line\n"


# ---------------------------------------------------------------------------------------------
# codespace_exec
# ---------------------------------------------------------------------------------------------

_HEALTHY_LOG = "[2026-10-05 08:04:02.884Z] Finished configuring codespace.\n"
_RECOVERY_LOG = ("[2026-10-04 22:07:14.201Z] postCreateCommand failed with exit code 1.\n"
                 "Container creation failed.\nCreating recovery container.\n")


def _ssh_reply(argv, *, log: str = _HEALTHY_LOG):
    """What a `codespace ssh` answers: the creation log when it is asked for, else nothing."""
    if "creation.log" in " ".join(argv):
        return d.GhResult(ok=True, exit_code=0, stdout=log)
    if argv[-1].endswith("handback.json"):      # the lane's LANE REPORT, pulled back by `cat`
        return d.GhResult(ok=True, exit_code=0, stdout=json.dumps(_LANE_REPORT))
    return d.GhResult(ok=True, exit_code=0, stdout="")


class _FakeGh:
    """Records every argv it is called with and answers by matching on the leading verb pair,
    same shape as `_StubRunProbe` in `test_codespace_admission.py`."""

    def __init__(self, *, receipt_written: dict | None = None, fail_at: str | None = None,
                created_name: str = "fluffy-space-1", log: str = _HEALTHY_LOG,
                fail_code: int = 1):
        self.calls: list[list[str]] = []
        self.receipt_written = receipt_written
        self.fail_at = fail_at
        self.created_name = created_name
        self.log = log
        self.fail_code = fail_code

    def __call__(self, argv):
        argv = list(argv)
        self.calls.append(argv)
        verb = " ".join(argv[:2])
        # `codespace ssh` covers several distinct calls (`mkdir -p <workdir>`, the creation-log
        # read, then `bash -l <runner>`) -- tag them apart so a test can fail one without silently
        # failing the others too.
        tag = ("codespace ssh mkdir" if verb == "codespace ssh" and "mkdir" in argv else
               "codespace ssh log" if verb == "codespace ssh" and "creation.log" in " ".join(argv)
               else "codespace ssh probe" if verb == "codespace ssh" and argv[-3:-1] == ["sh", "-c"]
               else "codespace ssh run" if verb == "codespace ssh" and "bash" in argv else verb)
        if self.fail_at in (verb, tag):
            return d.GhResult(ok=False, exit_code=self.fail_code, stdout="boom")
        if verb == "codespace create":
            # measured (`DIGEST-2026-09-15-codespaces-reference.md:182-183`): `gh codespace
            # create` writes the codespace NAME to stdout via `fmt.Fprintln`.
            return d.GhResult(ok=True, exit_code=0, stdout=self.created_name + "\n")
        if verb == "codespace cp":
            # the LAST positional is the local destination for a `remote:...` source cp
            if argv[-2].startswith("remote:") and self.receipt_written is not None:
                Path(argv[-1]).write_text(json.dumps(self.receipt_written), encoding="utf-8")
            return d.GhResult(ok=True, exit_code=0, stdout="")
        if verb == "codespace ssh":
            return _ssh_reply(argv, log=self.log)
        raise AssertionError(f"unexpected gh call: {argv}")


def test_codespace_exec_happy_path_returns_the_receipt(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    receipt = copy.deepcopy(_GOOD_RECEIPT)
    fake = _FakeGh(receipt_written=receipt)

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                              invoker=fake, batch="B1")

    assert result.ok, result.failure
    assert result.name == "fluffy-space-1"
    assert result.receipt == receipt
    # create (its stdout IS the name), read the creation log over ssh (item 3: a recovery
    # container is refused before anything ships), mkdir the workdir, cp contract, cp runner, ssh
    # run, cp receipt back -- no `list` call: the name is never reconstructed (codex terra P1,
    # 2026-09-27)
    verbs = [" ".join(c[:2]) for c in fake.calls]
    # ... then the handback is pulled back by `ssh cat` (the lane's LANE REPORT)
    assert verbs == ["codespace create", "codespace ssh", "codespace ssh", "codespace cp",
                     "codespace cp", "codespace ssh", "codespace cp", "codespace ssh"]


def test_codespace_exec_refuses_on_create_failure_without_further_calls(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(fail_at="codespace create")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")

    assert not result.ok
    assert "create exited" in result.failure
    assert len(fake.calls) == 1


def test_codespace_exec_refuses_when_create_returns_no_name(tmp_path):
    """Codex terra P1 (2026-09-27): the name is READ from `create`'s own stdout, never
    reconstructed by re-listing and matching on display name (not unique across a stale
    codespace from a prior run of this same slug -- a leaked, billing orphan on any mismatch)."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(created_name="")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")
    assert not result.ok
    assert "no name" in result.failure
    assert len(fake.calls) == 1  # nothing else was attempted without a name in hand


def test_codespace_exec_refuses_with_no_receipt_gate(tmp_path):
    """The PS verb's own doctrine: 'no receipt is a WARNING... never reporting success.'"""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(receipt_written=None)  # the cp-back call succeeds but writes nothing

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")
    assert not result.ok
    assert "no receipt" in result.failure


def test_codespace_exec_creates_the_workdir_before_shipping_anything_into_it(tmp_path):
    """Codex terra P1 (2026-09-27): `workdir` is NOT the checkout `gh codespace create` produces
    (`/workspaces/<repo-name>`) -- nothing creates it, so the first `cp` into it failed on every
    fresh codespace until this mkdir ran first."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(fail_at="codespace ssh mkdir")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")

    assert not result.ok
    assert "creating" in result.failure
    verbs = [" ".join(c[:2]) for c in fake.calls]
    assert verbs == ["codespace create", "codespace ssh", "codespace ssh"]  # nothing shipped


def test_codespace_exec_still_pulls_the_receipt_after_a_failed_runner(tmp_path):
    """Codex terra P1 (2026-09-27): the runner writes `receipt.json` in its own `exit $code`
    tail, so a non-zero ssh exit still has a receipt worth reading -- it must not be thrown away."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    receipt = {"exit_code": 1, "is_error": True, "status": "error"}
    fake = _FakeGh(receipt_written=receipt, fail_at="codespace ssh run")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")

    assert not result.ok
    assert "runner exited" in result.failure
    assert result.receipt == receipt  # kept, not discarded


def test_codespace_exec_rejects_a_receipt_that_reports_is_error(tmp_path):
    """Codex terra P1 (2026-09-27): `bash runner_remote` only ever fails on a TRANSPORT problem --
    it can exit 0 while the agent it ran reports `is_error: true`, and that must not read as OK."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    receipt = {"exit_code": 1, "is_error": True, "status": "error_during_execution"}
    fake = _FakeGh(receipt_written=receipt)  # ssh itself reports ok=True

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="B1")

    assert not result.ok
    assert result.receipt == receipt
    assert "receipt reports failure" in result.failure


def test_codespace_exec_rewrites_the_local_contract_path_for_the_remote_runner(tmp_path):
    """Codex terra P1 (2026-09-27): `plan`'s own argv names the LOCAL contract path in its
    prompt; unrewritten, the agent inside the codespace was asked to read a file that only ever
    existed on the dispatching machine, so no planned dispatch could execute its own contract."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    captured: dict[str, str] = {}

    def fake(argv):
        argv = list(argv)
        verb = " ".join(argv[:2])
        if verb == "codespace create":
            return d.GhResult(True, 0, "fluffy-1\n")
        if verb == "codespace cp":
            if argv[-1].startswith("remote:") and argv[-1].endswith(".sh"):
                captured["runner_body"] = Path(argv[-2]).read_text(encoding="utf-8")
            elif argv[-2].startswith("remote:"):
                Path(argv[-1]).write_text(json.dumps(_GOOD_RECEIPT), encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    prompt = f"Read and execute the frozen contract at {contract}"
    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", prompt],
                              invoker=fake, batch="B1")

    assert result.ok, result.failure
    assert str(contract) not in captured["runner_body"], "the local path leaked into the runner"
    assert f"/workspaces/dispatch/{contract.name}" in captured["runner_body"]


def test_codespace_exec_rewrites_a_relative_contract_argument_too(tmp_path, monkeypatch):
    """Codex terra P1 (2026-09-27): the documented flow is `plan --substrate codespace` (which
    resolves the contract to ABSOLUTE before embedding it in the prompt, dispatch.py:1792) then
    `codespace-exec --argv-json <that plan's argv>` with whatever contract argument the caller
    typed -- often relative. `str(contract)` unresolved never matched the absolute path already
    in `head_argv`, so the rewrite silently did nothing and the local path leaked into the runner
    (the exact failure the OTHER rewrite test above exists to catch, but only when both sides
    already agree on absolute -- this is the mismatched-forms case)."""
    monkeypatch.chdir(tmp_path)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    absolute_contract = contract.resolve()
    captured: dict[str, str] = {}

    def fake(argv):
        argv = list(argv)
        verb = " ".join(argv[:2])
        if verb == "codespace create":
            return d.GhResult(True, 0, "fluffy-1\n")
        if verb == "codespace cp":
            if argv[-1].startswith("remote:") and argv[-1].endswith(".sh"):
                captured["runner_body"] = Path(argv[-2]).read_text(encoding="utf-8")
            elif argv[-2].startswith("remote:"):
                Path(argv[-1]).write_text(json.dumps(_GOOD_RECEIPT), encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    # `plan`'s own prompt always embeds the ABSOLUTE path; the CONTRACT arg handed to exec is
    # relative, exactly as a caller typing `LANE-x.md` on the command line would produce.
    prompt = f"Read and execute the frozen contract at {absolute_contract}"
    relative_contract = Path("LANE-x.md")
    result = d.codespace_exec("me/repo", "main", "lane-x", relative_contract,
                              ["claude", "-p", prompt], invoker=fake, batch="B1")

    assert result.ok, result.failure
    assert str(absolute_contract) not in captured["runner_body"], \
        "the absolute local path leaked into the runner"
    assert f"/workspaces/dispatch/{contract.name}" in captured["runner_body"]


def test_codespace_exec_runs_the_agent_in_the_checkout_derived_from_repo(tmp_path):
    """Codex terra P1 (2026-09-27): `checkout_dir` must be derived from `repo` (the last path
    segment -- `gh codespace create -R owner/name` checks out to `/workspaces/<name>`), and the
    runner's `cd` must target it rather than `workdir` (this runner's own scratch directory)."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    captured: dict[str, str] = {}

    def fake(argv):
        argv = list(argv)
        verb = " ".join(argv[:2])
        if verb == "codespace create":
            return d.GhResult(True, 0, "fluffy-1\n")
        if verb == "codespace cp":
            if argv[-1].startswith("remote:") and argv[-1].endswith(".sh"):
                captured["runner_body"] = Path(argv[-2]).read_text(encoding="utf-8")
            elif argv[-2].startswith("remote:"):
                Path(argv[-1]).write_text(json.dumps(_GOOD_RECEIPT), encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    result = d.codespace_exec("me/dev-knowledge", "main", "lane-x", contract, ["claude"],
                              invoker=fake, batch="B1")

    assert result.ok, result.failure
    cd_line = next(ln for ln in captured["runner_body"].splitlines() if ln.startswith("cd "))
    assert "/workspaces/dev-knowledge" in cd_line
    assert "/workspaces/dispatch" not in cd_line


def test_codespace_exec_refuses_an_empty_argv_without_calling_gh(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")

    def fake(argv):  # pragma: no cover -- must not be reached
        raise AssertionError("gh must not be called with an empty argv")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, [], invoker=fake, batch="B1")
    assert not result.ok
    assert "empty" in result.failure


def test_runner_script_embeds_the_argv_as_a_file_never_an_ssh_string():
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo",
                                      ["claude", "-p", "a b"])
    assert body.startswith("#!/usr/bin/env bash")
    assert "'a b'" in body or '"a b"' in body
    assert "receipt.json" in body


def test_runner_script_runs_the_agent_in_the_checkout_not_the_scratch_workdir():
    """Codex terra P1 (2026-09-27): the agent's cwd must be the repo `create` checked out, never
    `workdir` (this runner's own empty scratch directory for the contract/runner/receipt files)
    -- otherwise a contract asking the agent to edit, commit, or push has nothing to act on."""
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/dev-knowledge",
                                      ["claude", "-p", "hi"])
    lines = body.splitlines()
    cd_line = next(ln for ln in lines if ln.startswith("cd "))
    assert "/workspaces/dev-knowledge" in cd_line
    assert "/workspaces/dispatch" not in cd_line
    assert "/workspaces/dispatch/run.log" in body  # run.log/receipt.json stay in the scratch dir


def _extract_receipt_writer_py(body: str) -> str:
    """Pulls the embedded `python3 -c '<code>'` argument back out of a generated runner script's
    bash -- `shlex.quote`'s own POSIX single-quote escaping, unwound by `shlex.split`. The quoted
    code itself contains literal newlines, so it spans several physical lines of `body` and
    cannot be pulled out by `splitlines()`; locate it by the surrounding markers instead."""
    marker = "python3 -c "
    start = body.index(marker) + len(marker)
    end = body.index(' "$code"', start)
    return shlex.split(body[start:end])[0]


def test_runner_script_receipt_scan_skips_a_trailing_non_json_line(tmp_path):
    """Codex terra P1 (2026-09-27): `run.log` also carries stderr (folded in by the runner's own
    `2>&1`), so a trailing diagnostic AFTER the agent's real final JSON result must not stop the
    reverse scan before it reaches that result -- the earlier version's unconditional `break`
    took whatever the LAST line was, JSON or not, and a non-JSON tail read as a silent success."""
    workdir = tmp_path
    body = d._codespace_runner_script(str(workdir), str(tmp_path / "checkout"), ["true"])
    code = _extract_receipt_writer_py(body)

    (workdir / "run.log").write_text(
        '{"is_error": true, "subtype": "error_during_execution", "num_turns": 2, '
        '"session_id": "abc"}\n'
        "a trailing stderr diagnostic, not JSON at all\n",
        encoding="utf-8",
    )
    subprocess.run([sys.executable, "-c", code, "0"], cwd=workdir, check=True)
    receipt = json.loads((workdir / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["is_error"] is True
    assert receipt["status"] == "error_during_execution"


def test_runner_script_receipt_scan_ignores_a_trailing_json_line_that_is_not_an_object(tmp_path):
    """A trailing JSON value that parses but isn't a `dict` (a bare number, a list) is not the
    agent's receipt line either -- same doctrine as the non-JSON case above, one line down."""
    workdir = tmp_path
    body = d._codespace_runner_script(str(workdir), str(tmp_path / "checkout"), ["true"])
    code = _extract_receipt_writer_py(body)

    (workdir / "run.log").write_text(
        '{"is_error": false, "subtype": "success", "num_turns": 1, "session_id": "abc"}\n'
        "[1, 2, 3]\n",
        encoding="utf-8",
    )
    subprocess.run([sys.executable, "-c", code, "0"], cwd=workdir, check=True)
    receipt = json.loads((workdir / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["is_error"] is False
    assert receipt["status"] == "success"


# ---------------------------------------------------------------------------------------------
# codespace_harvest / verify_harvest_manifest
# ---------------------------------------------------------------------------------------------

def _ssh_cat_fake(contents: dict[str, str], *, missing: tuple[str, ...] = ()):
    """A file is present iff it is a KEY in `contents` -- a file merely absent from the dict is
    also absent on 'the remote', not present-with-empty-content. `missing` names a key to force
    absent even though the harness's caller passed content for it (kept for symmetry with the
    fixture's counterpart in test_codespace_admission.py)."""
    def fake(argv):
        argv = list(argv)
        assert argv[:3] == ["codespace", "ssh", "-c"]
        path = argv[-1]
        rel = path.split("/")[-1]
        if rel not in contents or rel in missing:
            return d.GhResult(ok=False, exit_code=1, stdout="")
        return d.GhResult(ok=True, exit_code=0, stdout=contents[rel])
    return fake


def test_harvest_writes_files_and_a_manifest_with_matching_hashes(tmp_path):
    fake = _ssh_cat_fake({"run.log": "hello world\n", "receipt.json": '{"exit_code": 0}\n'})

    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-x", out_root=tmp_path,
                                 invoker=fake)

    assert result.ok, result.failure
    assert set(result.files) == {"run.log", "receipt.json"}
    out_dir = tmp_path / "B1" / "lane-x"
    assert (out_dir / "run.log").read_text(encoding="utf-8") == "hello world\n"
    manifest = json.loads((out_dir / d.HARVEST_MANIFEST_NAME).read_text(encoding="utf-8"))
    assert manifest["files"] == result.files


def test_harvest_skips_a_file_absent_on_the_remote_rather_than_refusing(tmp_path):
    fake = _ssh_cat_fake({"run.log": "only this one\n"}, missing=("receipt.json",))

    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-y", out_root=tmp_path,
                                 invoker=fake)

    assert result.ok
    assert set(result.files) == {"run.log"}


def test_harvest_refuses_a_second_call_without_force(tmp_path):
    fake = _ssh_cat_fake({"run.log": "x\n"})
    first = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-z", out_root=tmp_path,
                                invoker=fake)
    assert first.ok

    second = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-z", out_root=tmp_path,
                                 invoker=fake)
    assert not second.ok
    assert "already exists" in second.failure


def test_harvest_dry_run_writes_nothing(tmp_path):
    calls = []

    def fake(argv):  # pragma: no cover -- must never be reached in a dry run
        calls.append(argv)
        raise AssertionError("dry run must not call gh")

    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-dry", out_root=tmp_path,
                                 dry_run=True, invoker=fake)
    assert result.ok
    assert not calls
    assert not (tmp_path / "B1" / "lane-dry").exists()
    assert result.commands  # the plan is still shown


def test_verify_harvest_manifest_missing_refuses(tmp_path):
    verdict = d.verify_harvest_manifest(tmp_path / "nowhere")
    assert not verdict.ok
    assert "no harvest manifest" in verdict.reason


def test_verify_harvest_manifest_matches_after_a_clean_harvest(tmp_path):
    fake = _ssh_cat_fake({"run.log": "clean\n"})
    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-v", out_root=tmp_path,
                                 invoker=fake)
    verdict = d.verify_harvest_manifest(result.out_dir)
    assert verdict.ok, verdict.reason
    assert verdict.checked == ("run.log",)


def test_verify_harvest_manifest_refuses_on_a_tampered_file(tmp_path):
    fake = _ssh_cat_fake({"run.log": "original\n"})
    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-tamper", out_root=tmp_path,
                                 invoker=fake)
    (result.out_dir / "run.log").write_text("tampered\n", encoding="utf-8")

    verdict = d.verify_harvest_manifest(result.out_dir)
    assert not verdict.ok
    assert "hash mismatch" in verdict.reason


def test_verify_harvest_manifest_refuses_when_a_manifested_file_is_missing(tmp_path):
    fake = _ssh_cat_fake({"run.log": "x\n"})
    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-del", out_root=tmp_path,
                                 invoker=fake)
    (result.out_dir / "run.log").unlink()

    verdict = d.verify_harvest_manifest(result.out_dir)
    assert not verdict.ok
    assert "missing on disk" in verdict.reason


# ---------------------------------------------------------------------------------------------
# codespace_stop
# ---------------------------------------------------------------------------------------------

def test_stop_calls_gh_codespace_stop_and_never_deletes():
    calls = []

    def fake(argv):
        calls.append(list(argv))
        return d.GhResult(ok=True, exit_code=0, stdout="")

    result = d.codespace_stop("fluffy-1", invoker=fake)
    assert result.ok
    assert calls == [["codespace", "stop", "-c", "fluffy-1"]]
    assert all("delete" not in c for c in calls)


# ---------------------------------------------------------------------------------------------
# codespace_delete -- the R17 gate itself
# ---------------------------------------------------------------------------------------------

class TestCodespaceDelete:
    def test_refused_when_the_manifest_is_missing_and_gh_is_never_called(self, tmp_path):
        calls = []

        def fake(argv):  # pragma: no cover -- must not be reached
            calls.append(argv)
            raise AssertionError("gh must not be called when the harvest is unverified")

        result = d.codespace_delete("fluffy-1", out_dir=tmp_path / "no-such-harvest",
                                    invoker=fake)
        assert not result.ok
        assert result.refused
        assert "no harvest manifest" in result.reason
        assert not calls

    def test_refused_when_a_hash_differs_and_gh_is_never_called(self, tmp_path):
        fake_harvest = _ssh_cat_fake({"run.log": "before\n"})
        harvested = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-gate", out_root=tmp_path,
                                        invoker=fake_harvest)
        (harvested.out_dir / "run.log").write_text("after\n", encoding="utf-8")

        calls = []

        def fake_delete(argv):  # pragma: no cover -- must not be reached
            calls.append(argv)
            raise AssertionError("gh must not be called on a hash mismatch")

        result = d.codespace_delete("fluffy-1", out_dir=harvested.out_dir, invoker=fake_delete)
        assert not result.ok
        assert result.refused
        assert "hash mismatch" in result.reason
        assert not calls

    def test_allowed_when_the_manifest_verifies(self, tmp_path):
        fake_harvest = _ssh_cat_fake({"run.log": "clean\n"})
        harvested = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-ok", out_root=tmp_path,
                                        invoker=fake_harvest)

        calls = []

        def fake_delete(argv):
            calls.append(list(argv))
            return d.GhResult(ok=True, exit_code=0, stdout="")

        result = d.codespace_delete("fluffy-1", out_dir=harvested.out_dir, invoker=fake_delete)
        assert result.ok
        assert not result.refused
        assert calls == [["codespace", "delete", "-c", "fluffy-1", "--force"]]

    def test_refused_when_the_manifest_is_for_a_different_codespace(self, tmp_path):
        """Codex terra P1 (2026-09-27): hash checks alone verify the evidence is intact but not
        that it is evidence OF the codespace being deleted -- a manifest harvested from A must
        not authorize deleting B."""
        fake_harvest = _ssh_cat_fake({"run.log": "clean\n"})
        harvested = d.codespace_harvest("fluffy-A", batch="B1", lane="lane-swap", out_root=tmp_path,
                                        invoker=fake_harvest)

        calls = []

        def fake_delete(argv):  # pragma: no cover -- must not be reached
            calls.append(argv)
            raise AssertionError("gh must not be called when the manifest names a different codespace")

        result = d.codespace_delete("fluffy-B", out_dir=harvested.out_dir, invoker=fake_delete)
        assert not result.ok
        assert result.refused
        assert "different codespace" in result.reason
        assert not calls

    def test_private_copy_defaults_outside_the_repo_tree(self):
        repo_root = Path(__file__).resolve().parents[1]
        assert not str(d.DEFAULT_HARVEST_ROOT).startswith(str(repo_root))


# ---------------------------------------------------------------------------------------------
# codespace_plan shows the harvest + manifest check before delete (Done-contract item 3)
# ---------------------------------------------------------------------------------------------

def test_codespace_plan_shows_harvest_and_manifest_check_before_delete(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")

    steps = d.codespace_plan("me/repo", "main", "lane-x", contract, ["claude"], batch="B1")
    notes = [s.note for s in steps]
    verbs = [s.argv[:2] for s in steps]

    delete_i = next(i for i, v in enumerate(verbs) if v == ["gh", "codespace"]
                    and steps[i].argv[2] == "delete")
    manifest_i = next(i for i, n in enumerate(notes) if "manifest check" in n)
    harvest_is = [i for i, n in enumerate(notes) if n.startswith("harvest:")]

    assert harvest_is, "no harvest step in the plan"
    assert max(harvest_is) < manifest_i < delete_i
    assert steps[delete_i].argv == ["gh", "codespace", "delete", "-c", "{cs}", "--force"]


# =============================================================================================
# b2-codespace-green (R63, R65, R83): the lane carries its secrets, a recovery container is
# refused before the run, and a stalled or disconnected lane has a fate
# =============================================================================================

_RUNNER = "/workspaces/dispatch/run-lane-x.sh"
_FIVE_SECRETS = ("CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_TOKEN", "CODEX_API_KEY", "XAI_API_KEY",
                 "RCLONE_CONFIG_GDRIVE_TOKEN")


def _contract(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    return contract


# ---- item 1: a login shell with stdin closed (D1, D8) -----------------------------------------

def test_the_planned_run_step_is_a_login_shell(tmp_path):
    """D1, RED on cd3ab8a6: the plan shipped `gh codespace ssh -c {cs} -- bash <runner>`, a
    NON-login shell that sees none of the five Codespaces secrets (night probe x3: `set=no`; a
    login shell `yes`), so `claude -p` answered 'Not logged in'."""
    steps = d.codespace_plan("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"])
    run = next(s for s in steps if s.argv[-1] == _RUNNER)
    assert run.argv[-4:] == ["--", "bash", "-l", _RUNNER], run.argv


def test_the_executed_run_step_is_a_login_shell(tmp_path):
    fake = _FakeGh(receipt_written=copy.deepcopy(_GOOD_RECEIPT))
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert result.ok, result.failure
    run_calls = [c for c in fake.calls if c[:2] == ["codespace", "ssh"] and "bash" in c]
    assert len(run_calls) == 1
    assert run_calls[0][-4:] == ["--", "bash", "-l", _RUNNER], run_calls[0]


def test_the_runner_closes_stdin_of_the_head():
    """D8, RED on cd3ab8a6: `claude -p` waited 3 s on an open stdin and a codex head would hang."""
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo",
                                      ["claude", "-p", "hi"])
    head = next(ln for ln in body.splitlines() if ln.startswith("claude "))
    assert "< /dev/null" in head


def test_the_runner_records_the_five_secrets_as_booleans_and_never_a_value():
    """R13: presence only. The probe names each variable and prints yes/no; no line can expand a
    secret's value."""
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    for name in _FIVE_SECRETS:
        assert name in body
    assert "set=" in body
    assert "printenv" not in body and "env |" not in body
    for name in _FIVE_SECRETS:
        assert f"${name}" not in body and f"${{{name}}}" not in body, \
            f"a line could expand {name}'s value"


def test_the_runner_records_the_copilot_token_as_a_boolean_and_never_a_value():
    """R88a, RED-first: Copilot signs in through COPILOT_GITHUB_TOKEN, so the runner names it in its
    presence probe (yes/no) like the other secrets, and no line can expand its value."""
    assert "COPILOT_GITHUB_TOKEN" in d.RUNNER_SECRETS
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    assert "COPILOT_GITHUB_TOKEN" in body
    assert "$COPILOT_GITHUB_TOKEN" not in body and "${COPILOT_GITHUB_TOKEN}" not in body


# ---- item 5: heartbeat, stall watchdog, and a hangup that does not kill the lane ----------------

def test_the_runner_survives_a_dropped_ssh_connection():
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    assert "trap '' HUP" in body


def test_the_runner_writes_a_heartbeat_the_observer_reads():
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    assert "/workspaces/dispatch/heartbeat" in body
    assert "sleep 30" in body


def test_the_runner_kills_a_stalled_head_after_the_stated_bound():
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"],
                                      stall_after_s=120)
    assert "-gt 120" in body and "kill" in body
    default = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    assert "-gt 900" in default, "the default is classify_lane's own stale bound"


def test_a_stalled_run_writes_a_failed_fate_with_reason_and_step_into_the_receipt(tmp_path):
    body = d._codespace_runner_script(str(tmp_path), str(tmp_path / "checkout"), ["true"],
                                      stall_after_s=120)
    code = _extract_receipt_writer_py(body)
    (tmp_path / "run.log").write_text("partial output, then silence\n", encoding="utf-8")
    subprocess.run([sys.executable, "-c", code, "124", "stalled"], cwd=tmp_path, check=True)
    receipt = json.loads((tmp_path / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["is_error"] is True and receipt["status"] == "hung"
    assert receipt["fate"]["fate"] == "FAILED" and receipt["fate"]["step"] == "run"
    assert "no progress" in receipt["fate"]["reason"] and "120" in receipt["fate"]["reason"]


def test_a_normal_run_writes_no_fate_into_the_receipt(tmp_path):
    body = d._codespace_runner_script(str(tmp_path), str(tmp_path / "checkout"), ["true"])
    code = _extract_receipt_writer_py(body)
    (tmp_path / "run.log").write_text('{"is_error": false, "subtype": "success"}\n',
                                      encoding="utf-8")
    subprocess.run([sys.executable, "-c", code, "0"], cwd=tmp_path, check=True)
    assert "fate" not in json.loads((tmp_path / "receipt.json").read_text(encoding="utf-8"))


# ---- item 3: the creation log is read over ssh, and a recovery container is refused -------------

def test_a_recovery_container_is_refused_before_anything_ships_or_runs(tmp_path):
    """D3, RED on cd3ab8a6: `dispatch.py` never called the classifier, so a recovery container
    (Alpine, no uv/claude/gh) was handed the lane."""
    fake = _FakeGh(log=_RECOVERY_LOG)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert not result.ok
    assert result.name == "fluffy-space-1", "the box was created, so it is named for teardown"
    assert "recovery" in result.failure
    assert [" ".join(c[:2]) for c in fake.calls] == ["codespace create", "codespace ssh"]
    assert fake.calls[1][-2:] == ["cat", "/workspaces/.codespaces/.persistedshare/creation.log"]


def test_an_unreadable_creation_log_is_refused_after_a_bounded_number_of_reads(tmp_path):
    """An empty log is not evidence of health (the classifier's own rule): refuse, never run."""
    fake = _FakeGh(log="")
    slept: list[float] = []
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, sleep=slept.append, batch="B1")
    assert not result.ok and "indeterminate" in result.failure
    reads = [c for c in fake.calls if "creation.log" in " ".join(c)]
    assert len(reads) == d.CREATION_LOG_ATTEMPTS == 3
    assert len(slept) == d.CREATION_LOG_ATTEMPTS - 1
    assert not any("bash" in c for c in fake.calls)


def test_a_log_that_is_not_finished_on_the_first_read_is_read_again(tmp_path):
    answers = iter(["", "[2026-10-05 08:03:00Z] Running the postCreateCommand...\n", _HEALTHY_LOG])

    def fake(argv):
        argv = list(argv)
        verb = " ".join(argv[:2])
        if verb == "codespace create":
            return d.GhResult(True, 0, "fluffy-1\n")
        if verb == "codespace cp":
            if argv[-2].startswith("remote:"):
                Path(argv[-1]).write_text(json.dumps(_GOOD_RECEIPT), encoding="utf-8")
            return d.GhResult(True, 0, "")
        if "creation.log" in " ".join(argv):
            return d.GhResult(True, 0, next(answers))
        if argv[-1].endswith("handback.json"):
            return d.GhResult(True, 0, json.dumps(_LANE_REPORT))
        return d.GhResult(True, 0, "")

    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, sleep=lambda s: None, batch="B1")
    assert result.ok, result.failure


def test_a_creation_failure_without_a_recovery_line_is_refused_too(tmp_path):
    fake = _FakeGh(log="[x] postCreateCommand failed with exit code 1.\nContainer creation failed.\n")
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, sleep=lambda s: None, batch="B1")
    assert not result.ok and "creation-failed" in result.failure


def test_the_plan_names_the_creation_log_check_before_the_run(tmp_path):
    steps = d.codespace_plan("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"])
    notes = [s.note for s in steps]
    log_i = next(i for i, n in enumerate(notes) if "creation log" in n)
    run_i = next(i for i, s in enumerate(steps) if s.argv[-1] == _RUNNER)
    assert log_i < run_i
    assert steps[log_i].argv[-2:] == ["cat", "/workspaces/.codespaces/.persistedshare/creation.log"]


def test_run_gh_takes_a_per_call_timeout_so_an_observer_read_cannot_block_for_900_s(monkeypatch):
    seen: dict = {}

    def capture(*_a, **kw):
        seen.update(kw)
        raise subprocess.TimeoutExpired(cmd=["gh"], timeout=kw["timeout"])

    monkeypatch.setattr(d.subprocess, "run", capture)
    result = d.run_gh(["codespace", "ssh", "-c", "x"], timeout=7)
    assert seen["timeout"] == 7 and result.exit_code == 124


def test_run_gh_closes_stdin_so_a_gh_prompt_cannot_wait_on_a_pipe(monkeypatch):
    seen: dict = {}

    class _Done:
        returncode, stdout, stderr = 0, "", ""

    def capture(*_a, **kw):
        seen.update(kw)
        return _Done()

    monkeypatch.setattr(d.subprocess, "run", capture)
    d.run_gh(["codespace", "list"])
    assert seen.get("stdin") is subprocess.DEVNULL


# ---- item 5: a failed run carries its fate ---------------------------------------------------------

@pytest.mark.parametrize("code,word", [(255, "disconnected"), (124, "timed out")])
def test_a_run_whose_transport_died_fails_with_a_fate_naming_the_step(tmp_path, code, word):
    """D4/D5, RED on cd3ab8a6: the failure was a bare string; the lane had no fate."""
    fake = _FakeGh(receipt_written=None, fail_at="codespace ssh run", fail_code=code)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert not result.ok
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "run"
    assert word in result.fate["reason"]


def test_a_missing_receipt_after_a_clean_run_fails_with_a_receipt_step_fate(tmp_path):
    fake = _FakeGh(receipt_written=None)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert not result.ok
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "receipt"


def test_a_stalled_receipt_is_a_failed_run_with_the_runners_own_fate(tmp_path):
    receipt = {"exit_code": 124, "is_error": True, "status": "hung",
               "fate": {"fate": "FAILED", "step": "run", "reason": "no progress for 901s"}}
    fake = _FakeGh(receipt_written=receipt)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert not result.ok
    assert result.fate == receipt["fate"]


def test_a_successful_exec_has_no_fate_failure(tmp_path):
    fake = _FakeGh(receipt_written=copy.deepcopy(_GOOD_RECEIPT))
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, batch="B1")
    assert result.ok and result.fate == {}


# ---- items 3 and 5: the observer (live -> working, deleted -> absent) -------------------------------

class _ObserveGh:
    def __init__(self, *, listing, probe=None, list_ok=True, probe_ok=True):
        self.listing, self.probe = listing, probe
        self.list_ok, self.probe_ok = list_ok, probe_ok
        self.calls: list[list[str]] = []

    def __call__(self, argv):
        argv = list(argv)
        self.calls.append(argv)
        if argv[:2] == ["codespace", "list"]:
            return d.GhResult(self.list_ok, 0 if self.list_ok else 1, json.dumps(self.listing))
        if argv[:2] == ["codespace", "ssh"]:
            return d.GhResult(self.probe_ok, 0 if self.probe_ok else 255,
                              self.probe if self.probe_ok else "", "" if self.probe_ok else "reset")
        raise AssertionError(f"unexpected gh call: {argv}")


def test_a_live_lane_reads_working_not_unknown():
    """D4, RED on cd3ab8a6: the hub classifier read `unknown` for a live box."""
    fake = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=1000 log=990 hb=995 receipt=0\n")
    seen = d.codespace_observe("cs-1", invoker=fake)
    assert seen["state"] == "working" and seen["fate"] == "RUNNING"
    assert seen["container_state"] == "Available" and seen["progress_age_s"] == 10.0


def test_a_deleted_codespace_reads_absent_and_is_not_probed_over_ssh():
    fake = _ObserveGh(listing=[{"name": "someone-else", "state": "Available"}])
    seen = d.codespace_observe("cs-1", expected_gone=True, invoker=fake)
    assert seen["state"] == "absent" and seen["fate"] == "TORN-DOWN"
    assert not any(c[:2] == ["codespace", "ssh"] for c in fake.calls)


def test_a_vanished_codespace_this_line_did_not_delete_is_failed():
    seen = d.codespace_observe("cs-1", invoker=_ObserveGh(listing=[]))
    assert seen["state"] == "absent" and seen["fate"] == "FAILED"


def test_a_stalled_lane_is_hung_and_failed_at_the_run_step():
    fake = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=5000 log=100 hb=4990 receipt=0\n")
    seen = d.codespace_observe("cs-1", invoker=fake)
    assert seen["state"] == "hung" and seen["fate"] == "FAILED" and seen["step"] == "run"


def test_a_listing_that_cannot_be_read_is_waiting_never_absent():
    seen = d.codespace_observe("cs-1", invoker=_ObserveGh(listing=[], list_ok=False))
    assert seen["state"] == "unknown" and seen["fate"] == "WAITING"


def test_an_unreachable_box_waits_then_is_disconnected_at_the_bound():
    fake = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}], probe_ok=False)
    early = d.codespace_observe("cs-1", invoker=fake, unreachable_for_s=10)
    late = d.codespace_observe("cs-1", invoker=fake, unreachable_for_s=300)
    assert early["state"] == "unknown" and early["fate"] == "WAITING"
    assert late["state"] == "disconnected" and late["fate"] == "FAILED"


def test_a_receipt_on_the_box_reads_finished_and_a_handback():
    fake = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=1000 log=900 hb=900 receipt=1\n")
    seen = d.codespace_observe("cs-1", invoker=fake)
    assert seen["state"] == "finished" and seen["fate"] == "HANDBACK"


def test_the_observe_cli_prints_the_reading_as_json(monkeypatch, tmp_path):
    from click.testing import CliRunner

    monkeypatch.setattr(d, "run_gh", lambda argv, **kw: _ObserveGh(
        listing=[{"name": "cs-1", "state": "Available"}],
        probe="now=1000 log=990 hb=995 receipt=0\n")(argv))
    out = CliRunner().invoke(d.cli, ["codespace-observe", "--name", "cs-1", "--slug", "lane-x",
                                     "--ledger", str(tmp_path / "receipts.jsonl")])
    assert out.exit_code == 0, out.output
    assert json.loads(out.output)["state"] == "working"


def test_the_run_step_outlasts_every_other_gh_call():
    assert d.RUN_TIMEOUT_SECONDS > d.GH_TIMEOUT_SECONDS


def test_a_run_refused_at_creation_still_harvests_its_creation_log_so_the_box_can_be_deleted(tmp_path):
    """b2-codespace-green run 1: a recovery container was refused before the run, so it had no
    run.log and no receipt, the manifest listed nothing, and `codespace_delete` refused -- a
    billing box with no way out. The creation log is the evidence such a run DOES have."""
    fake = _ssh_cat_fake({"creation.log": "Creating recovery container."})
    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-refused", out_root=tmp_path,
                                 invoker=fake)
    assert result.ok and set(result.files) == {"creation.log"}
    assert d.verify_harvest_manifest(result.out_dir, expected_name="fluffy-1").ok
    deleted = d.codespace_delete("fluffy-1", out_dir=result.out_dir,
                                 invoker=lambda argv: d.GhResult(True, 0, ""))
    assert deleted.ok and not deleted.refused


def test_harvest_reads_the_creation_log_from_its_fixed_remote_path(tmp_path):
    seen = []

    def fake(argv):
        seen.append(list(argv)[-1])
        return d.GhResult(ok=False, exit_code=1, stdout="")

    d.codespace_harvest("fluffy-1", batch="B1", lane="lane-path", out_root=tmp_path, invoker=fake)
    assert d.cs.CREATION_LOG_PATH in seen


# ---- item 5, review P1-2 (repair 2): the fate has its OWN clock and the line RECORDS it --------------
#
# RED on 86a8d744 (merged with origin/main a09c4fff): the disconnect bound took its clock from the
# CALLER (`unreachable_for_s`, default 0), so repeated `codespace-observe` readings of an unreachable
# box never crossed it, and no path in the line called `write_fate` -- a disconnected lane was never
# recorded FAILED by the line, only by the hand-run `codespace_regime.py fate` CLI.

_T0 = datetime(2026, 10, 6, 0, 0, 0, tzinfo=timezone.utc)


def _t(seconds: float) -> datetime:
    return _T0 + timedelta(seconds=seconds)


def _fates(ledger) -> list[dict]:
    if not ledger.is_file():
        return []
    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [r for r in rows if r.get("kind") == "codespace-fate"]


def _unreachable() -> "_ObserveGh":
    return _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}], probe_ok=False)


def _observe(fake, ledger, at, **kw):
    return d.codespace_observe("cs-1", invoker=fake, slug="lane-x", ledger_path=ledger,
                               now=_t(at), **kw)


def test_repeated_readings_of_an_unreachable_box_cross_the_bound_on_their_own_clock(tmp_path):
    """No caller-supplied duration anywhere: the first-unreachable stamp is stored in the ledger and
    the duration is derived from it, so three plain readings reach `disconnected` -> FAILED."""
    ledger, fake = tmp_path / "receipts.jsonl", _unreachable()
    first = _observe(fake, ledger, 0)
    middle = _observe(fake, ledger, 120)
    last = _observe(fake, ledger, cs.DISCONNECT_AFTER_S + 10)
    assert (first["state"], first["fate"]) == ("unknown", "WAITING")
    assert (middle["state"], middle["fate"]) == ("unknown", "WAITING")
    assert middle["unreachable_for_s"] == 120
    assert (last["state"], last["fate"], last["step"]) == ("disconnected", "FAILED", "observe")
    assert last["unreachable_for_s"] == cs.DISCONNECT_AFTER_S + 10
    rows = _fates(ledger)
    assert [(r["fate"], r["state"]) for r in rows] == [("WAITING", "unknown"),
                                                     ("FAILED", "disconnected")], rows
    failed = rows[-1]
    assert failed["codespace"] == "cs-1" and failed["slug"] == "lane-x"
    assert failed["step"] == "observe" and "unreachable over ssh" in failed["reason"]
    assert failed["unreachable_since"] == _T0.isoformat(timespec="seconds")


def test_a_reachable_reading_ends_the_unreachable_streak_and_resets_its_clock(tmp_path):
    ledger = tmp_path / "receipts.jsonl"
    _observe(_unreachable(), ledger, 0)
    ok = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                    probe="now=1000 log=990 hb=995 receipt=0\n")
    assert _observe(ok, ledger, 200)["fate"] == "RUNNING"
    again = _observe(_unreachable(), ledger, 400)       # a NEW streak: 0 s, not 400 s
    assert again["unreachable_for_s"] == 0 and again["fate"] == "WAITING"
    assert _observe(_unreachable(), ledger, 400 + cs.DISCONNECT_AFTER_S - 1)["fate"] == "WAITING"
    assert _observe(_unreachable(), ledger, 400 + cs.DISCONNECT_AFTER_S)["fate"] == "FAILED"


def test_every_fate_transition_writes_its_row_through_write_fate_and_a_repeat_writes_none(tmp_path):
    ledger = tmp_path / "receipts.jsonl"
    live = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=1000 log=990 hb=995 receipt=0\n")
    hung = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=5000 log=100 hb=4990 receipt=0\n")
    done = _ObserveGh(listing=[{"name": "cs-1", "state": "Available"}],
                      probe="now=1000 log=900 hb=900 receipt=1\n")
    gone = _ObserveGh(listing=[])
    for at, fake in ((0, live), (30, live), (60, hung), (90, hung), (120, done), (150, gone)):
        _observe(fake, ledger, at, expected_gone=fake is gone)
    assert [(r["fate"], r["state"]) for r in _fates(ledger)] == [
        ("RUNNING", "working"), ("FAILED", "hung"), ("HANDBACK", "finished"),
        ("TORN-DOWN", "absent")]
    hung_row = _fates(ledger)[1]
    assert hung_row["step"] == "run" and "no progress" in hung_row["reason"]


def test_the_recorded_fate_goes_through_write_fate_not_a_second_writer(tmp_path, monkeypatch):
    seen = []
    real = d.regime.write_fate
    monkeypatch.setattr(d.regime, "write_fate", lambda *a, **k: seen.append((a, k)) or real(*a, **k))
    _observe(_unreachable(), tmp_path / "receipts.jsonl", 0)
    assert len(seen) == 1 and seen[0][0][2] == "WAITING"


def test_a_reading_with_no_slug_records_nothing_and_keeps_the_callers_clock(tmp_path):
    ledger = tmp_path / "receipts.jsonl"
    seen = d.codespace_observe("cs-1", invoker=_unreachable(), ledger_path=ledger, now=_t(0),
                               unreachable_for_s=cs.DISCONNECT_AFTER_S)
    assert seen["fate"] == "FAILED" and not ledger.exists()


def test_the_observe_cli_records_the_fate_in_the_ledger(tmp_path, monkeypatch):
    from click.testing import CliRunner

    ledger = tmp_path / "receipts.jsonl"
    monkeypatch.setattr(d, "run_gh", lambda argv, **kw: _ObserveGh(
        listing=[{"name": "cs-1", "state": "Available"}],
        probe="now=1000 log=990 hb=995 receipt=0\n")(argv))
    out = CliRunner().invoke(d.cli, ["codespace-observe", "--name", "cs-1", "--slug", "lane-x",
                                     "--ledger", str(ledger)])
    assert out.exit_code == 0, out.output
    assert json.loads(out.output)["fate"] == "RUNNING"
    assert [(r["slug"], r["fate"]) for r in _fates(ledger)] == [("lane-x", "RUNNING")]


# ---- review of the repair-2 delta (Codex terra, nonce c4837ade7279): two further P1s ------------------

def test_the_observe_cli_refuses_a_reading_with_no_slug_so_the_line_never_runs_unrecorded(tmp_path):
    """Delta P1 (dispatch.py:2319): `codespace-observe --name X` could report FAILED and record
    nothing. The line's entry point now REQUIRES the lane slug; the pure-read primitive stays a
    function seam (tested above) and is not reachable from the CLI."""
    from click.testing import CliRunner

    ledger = tmp_path / "receipts.jsonl"
    out = CliRunner().invoke(d.cli, ["codespace-observe", "--name", "cs-1", "--ledger", str(ledger)])
    assert out.exit_code == 2 and "slug" in out.output.lower()
    assert not ledger.exists()


def test_an_unreadable_listing_between_unreachable_readings_keeps_the_disconnect_stamp(tmp_path):
    """Delta P1 (dispatch.py:2358): an intermittent `gh codespace list` failure cleared the stamp, so
    a box whose ssh stayed dead never reached the bound. The stamp survives an INDETERMINATE reading
    and ends only on an affirmative recovery or a terminal state."""
    ledger = tmp_path / "receipts.jsonl"
    _observe(_unreachable(), ledger, 0)
    blind = _ObserveGh(listing=[], list_ok=False)
    mid = _observe(blind, ledger, 100)
    assert (mid["state"], mid["fate"]) == ("unknown", "WAITING")
    last = _observe(_unreachable(), ledger, cs.DISCONNECT_AFTER_S + 10)
    assert (last["state"], last["fate"]) == ("disconnected", "FAILED")
    assert last["unreachable_since"] == _T0.isoformat(timespec="seconds")
    rows = _fates(ledger)
    assert [(r["fate"], r["state"]) for r in rows] == [("WAITING", "unknown"),
                                                     ("FAILED", "disconnected")], rows


def test_a_terminal_reading_ends_the_streak_and_a_later_box_starts_a_new_clock(tmp_path):
    ledger = tmp_path / "receipts.jsonl"
    _observe(_unreachable(), ledger, 0)
    gone = _observe(_ObserveGh(listing=[]), ledger, 50, expected_gone=True)
    assert gone["fate"] == "TORN-DOWN" and gone["unreachable_since"] is None
    assert "unreachable_since" not in _fates(ledger)[-1]


def test_the_prior_fate_is_looked_up_by_codespace_and_slug(tmp_path):
    """Delta P2 (codespace_regime.py:251): a reused codespace NAME must not inherit another lane's
    stamp or suppress the new lane's first row."""
    ledger = tmp_path / "receipts.jsonl"
    d.regime.write_fate("cs-1", "lane-old", "WAITING", "unknown", "waiting", "observe",
                        ledger_path=ledger, now=_t(0), unreachable_since=_t(0))
    seen = d.codespace_observe("cs-1", invoker=_unreachable(), slug="lane-new", ledger_path=ledger,
                               now=_t(cs.DISCONNECT_AFTER_S + 50))
    assert seen["fate"] == "WAITING" and seen["unreachable_for_s"] == 0
    assert [r["slug"] for r in _fates(ledger)] == ["lane-old", "lane-new"]


def test_an_unreadable_listing_is_never_read_as_a_confirmed_teardown_even_when_one_is_expected(tmp_path):
    """Declined delta P1 (Codex terra, nonce 07d6dfb67a66; rejected by grok-4.7, nonce 97937798389b):
    `container is None` is an UNREADABLE listing, a readable one without the box is "Absent". Only
    the latter is a confirmed absence, so only the latter ends the streak and reads TORN-DOWN."""
    ledger = tmp_path / "receipts.jsonl"
    _observe(_unreachable(), ledger, 0)
    blind = _observe(_ObserveGh(listing=[], list_ok=False), ledger, 50, expected_gone=True)
    assert (blind["state"], blind["fate"]) == ("unknown", "WAITING")
    assert blind["unreachable_since"] == _T0.isoformat(timespec="seconds")
    sure = _observe(_ObserveGh(listing=[]), ledger, 60, expected_gone=True)
    assert (sure["state"], sure["fate"], sure["unreachable_since"]) == ("absent", "TORN-DOWN", None)


# =====================================================================================================
# b2-codespace-subscription-auth (W1-13, R87): the launcher MIRRORS each CLI's own sign-in cache
# =====================================================================================================
#
# RED on 84ee7e90 (origin/main when the lane started): `codespace_exec` has no `mirror`, no
# `MirrorConfig`, no `leak_check` -- it creates the box, ships the contract and runs the lane with
# whatever the Codespaces secrets hold, and nothing reads the laptop's sign-ins, checks them for
# expiry, compares the claude versions or proves that no credential reached an artefact.
#
# Every credential below is a SENTINEL: the tests assert that the sentinel's bytes never reach an
# argv, a result, a runner script or a record -- by comparing, never by printing.

_SENTINEL_CODEX = "SENTINEL-CODEX-REFRESH-0123456789abcdef"
_SENTINEL_GEMINI = "SENTINEL-GEMINI-REFRESH-0123456789abcdef"
_NOW = datetime(2026, 10, 6, 12, 0, tzinfo=timezone.utc)

_MIRROR_REGISTRY = {"providers": {"openai": {"cli": "codex"}, "anthropic": {"cli": "claude"},
                                  "antigravity": {"cli": "agy"}, "deepseek": {"cli": None}},
                    "roles": {}, "models": {}}


def _codex_auth(age_days: float, token: str = _SENTINEL_CODEX) -> str:
    return json.dumps({"auth_mode": "chatgpt", "OPENAI_API_KEY": None,
                       "tokens": {"id_token": "i", "access_token": "a", "refresh_token": token,
                                  "account_id": "acc"},
                       "last_refresh": (_NOW - timedelta(days=age_days)).isoformat()})


def _home(tmp_path, *, codex_age: float | None = 2.0) -> Path:
    home = tmp_path / "home"
    (home / ".codex").mkdir(parents=True)
    if codex_age is not None:
        (home / ".codex" / "auth.json").write_text(_codex_auth(codex_age), encoding="utf-8")
    return home


def _cfg(tmp_path, *, home=None, env=None, verdicts=None, local_versions=None, registry=None):
    return d.MirrorConfig(home=home or _home(tmp_path), env=dict(env or {}),
                          registry=registry or _MIRROR_REGISTRY, now=_NOW,
                          local_versions=dict(local_versions or {"claude": "2.1.290"}),
                          verdicts=dict(verdicts or {}))


class _MirrorGh(_FakeGh):
    """`_FakeGh` that understands the credential tools script: it records the bytes each `install`
    receives on stdin, answers the mode, the status calls and the claude version, and keeps the
    runner script the launcher shipped."""

    def __init__(self, *, remote_claude="2.1.290", reinstall_fixes=True, status=None,
                 echo_stdin=False, **kw):
        super().__init__(**kw)
        self.stdin: list[tuple[list[str], bytes]] = []
        self.remote_claude = remote_claude
        self.reinstall_fixes = reinstall_fixes
        self.status = status or {}
        self.echo_stdin = echo_stdin
        self.runner_body = ""

    def __call__(self, argv, input_bytes=None):
        argv = list(argv)
        tool = next((a for a in argv if a.endswith("credential-tools.sh")), None)
        if argv[:2] == ["codespace", "ssh"] and tool is not None:
            self.calls.append(argv)
            if input_bytes is not None:
                self.stdin.append((argv, input_bytes))
            return self._tools(argv[argv.index(tool) + 1:], input_bytes)
        if argv[:2] == ["codespace", "cp"] and argv[-1].startswith("remote:") and "/run-" in argv[-1]:
            self.runner_body = Path(argv[-2]).read_text(encoding="utf-8")
        return super().__call__(argv)

    def _tools(self, tail, input_bytes):
        verb = tail[0]
        if verb == "install":
            echoed = input_bytes.decode("utf-8", "replace") if self.echo_stdin and input_bytes else ""
            return d.GhResult(True, 0, echoed + "mode 600\n")
        if verb == "status":
            text, rc = self.status.get(tail[1], ("Logged in", 0))
            return d.GhResult(rc == 0, rc, text)
        if verb in ("agy-signin-start", "agy-signin-code", "agy-probe"):
            return d.GhResult(False, 70, "")     # no URL: the gap is recorded, the launch goes on
        if verb == "agy-signin-stop":
            return d.GhResult(True, 0, "")       # the auth process tree is killed
        if verb == "agy-signin-diag":
            return d.GhResult(True, 0, "out_bytes=0\n")
        if verb == "claude-version":
            return d.GhResult(True, 0, f"{self.remote_claude} (Claude Code)\n")
        if verb == "claude-install":
            if self.reinstall_fixes:
                self.remote_claude = tail[1]
            return d.GhResult(True, 0, "installed\n")
        raise AssertionError(f"unexpected credential tool call: {tail}")


def _run_mirrored(tmp_path, fake, cfg):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake.receipt_written = copy.deepcopy(_GOOD_RECEIPT)
    return d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                            invoker=fake, mirror=cfg, batch="B1")


def _ran(fake) -> bool:
    """Did the lane's runner start (`bash -l <workdir>/run-<slug>.sh`)?"""
    return any(c[:2] == ["codespace", "ssh"] and "-l" in c and c[-1].endswith("/run-lane-x.sh")
               for c in fake.calls)


def _as_dict(result) -> dict:
    from dataclasses import asdict

    return asdict(result)


def test_the_launcher_copies_the_laptops_codex_cache_through_stdin_owner_only_and_never_in_argv(tmp_path):
    cfg = _cfg(tmp_path)
    fake = _MirrorGh()
    result = _run_mirrored(tmp_path, fake, cfg)
    assert result.ok, result.failure
    installs = [(a, b) for a, b in fake.stdin if "install" in a]
    assert len(installs) == 1, "exactly the primary cache file is mirrored"
    argv, body = installs[0]
    assert argv[argv.index("install") + 1] == ".codex/auth.json"
    assert body == (cfg.home / ".codex" / "auth.json").read_bytes(), "the bytes travel on stdin"
    assert not any(_SENTINEL_CODEX in " ".join(c) for c in fake.calls), "never in an argv"
    assert _ran(fake), "the runner started after the mirror"
    codex = next(i for i in result.mirror if i["cli"] == "codex")
    assert codex["action"] == "mirrored" and codex["mode"] == "600" and codex["present"] is True
    assert _SENTINEL_CODEX not in json.dumps(_as_dict(result))


def test_a_key_the_laptop_does_not_use_is_unset_for_the_lane_when_codex_is_mirrored(tmp_path):
    fake = _MirrorGh()
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, env={"CODEX_API_KEY": "k"}))
    assert result.ok, result.failure
    assert "unset CODEX_API_KEY" in fake.runner_body and "OPENAI_API_KEY" in fake.runner_body


def test_an_expired_credential_refuses_before_any_box_exists_with_one_operator_action(tmp_path):
    """Item 3, RED-first: on 84ee7e90 this launches (creates a box, runs the lane); on the tip it
    refuses with the WAITING fate and ONE exact renew line, and `gh` is never called."""
    home = _home(tmp_path, codex_age=None)
    (home / ".codex" / "auth.json").write_text(json.dumps({"auth_mode": "apikey"}), encoding="utf-8")
    fake = _MirrorGh()
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, home=home))
    assert not result.ok and fake.calls == [], "no box was created for a credential known dead"
    assert result.fate["fate"] == "WAITING" and result.fate["step"] == "credentials"
    lines = [x for x in result.failure.split("\n") if x.startswith("OPERATOR-ACTION:")]
    assert len(lines) == 1 and "codex login" in lines[0]


def test_a_codex_cache_past_the_refresh_window_refuses_rather_than_let_two_machines_refresh_it(tmp_path):
    fake = _MirrorGh()
    # 7.9 d, not 7.5: the window is derived from the run bound (~7.83 d, codespace-finish-2026-10-14
    # stage 2), so 7.5 d now MIRRORS; 7.9 d is still inside the band that is refused
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, home=_home(tmp_path, codex_age=7.9)))
    assert not result.ok and fake.calls == []
    assert result.fate["fate"] == "WAITING"
    assert "OPERATOR-ACTION:" in result.failure and "refresh" in result.failure


def test_a_credential_the_codespace_reports_expired_after_the_mirror_refuses_before_the_runner(tmp_path):
    fake = _MirrorGh(status={"codex": ("Your access token could not be refreshed: refresh token was "
                                       "already used", 1)})
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path))
    assert not result.ok and not _ran(fake)
    assert result.fate["fate"] == "WAITING"
    assert result.failure.count("OPERATOR-ACTION:") == 1 and "codex login" in result.failure


def test_the_leak_check_fails_a_runner_that_echoes_a_credential_and_names_only_the_credential(tmp_path):
    """Item 2, RED-first: the fixture echoes the sentinel on stdout; the check compares hashes and
    strings in memory and reports a NAME -- the sentinel appears nowhere in the result."""
    fake = _MirrorGh(echo_stdin=True)
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path))
    assert not result.ok and "leak" in result.failure.lower()
    assert "codex" in result.failure
    blob = json.dumps(_as_dict(result)) + "\n".join(" ".join(c) for c in fake.calls)
    assert _SENTINEL_CODEX not in blob and "refresh_token" not in blob
    assert not _ran(fake), "a leaking mirror never reaches the runner"


def test_leak_check_unit_matches_values_and_the_whole_file_hash_without_returning_either():
    import hashlib

    cred = _codex_auth(1.0).encode()
    assert d.leak_check({"codex": cred}, ["nothing here", "still nothing"]) == []
    assert d.leak_check({"codex": cred}, [f"x {_SENTINEL_CODEX} y"]) == ["codex"]
    assert d.leak_check({"codex": cred}, ["sha " + hashlib.sha256(cred).hexdigest()]) == ["codex"]
    other = json.dumps({"a": _SENTINEL_GEMINI}).encode()
    assert d.leak_check({"codex": cred, "gemini": other}, [_SENTINEL_GEMINI]) == ["gemini"]


def test_a_codespace_claude_older_than_the_laptops_is_re_derived_before_the_runner(tmp_path):
    """Item 4, RED-first: on 84ee7e90 the box launches at whatever the pin said (2.1.289 against a
    laptop at 2.1.290); on the tip the launcher installs the laptop's version and re-reads it."""
    fake = _MirrorGh(remote_claude="2.1.289")
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, local_versions={"claude": "2.1.290"}))
    assert result.ok, result.failure
    installs = [c for c in fake.calls if "claude-install" in c]
    assert installs and installs[0][-1] == "2.1.290", "the version comes from the laptop, not a pin"
    assert fake.remote_claude == "2.1.290"
    claude = next(i for i in result.mirror if i["cli"] == "claude")
    assert claude["local_version"] == "2.1.290" and claude["codespace_version"] == "2.1.290"


def test_a_claude_skew_that_the_install_does_not_fix_refuses_before_the_runner(tmp_path):
    fake = _MirrorGh(remote_claude="2.1.289", reinstall_fixes=False)
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path))
    assert not result.ok and not _ran(fake)
    assert "claude version skew" in result.failure and "2.1.289" in result.failure
    assert "2.1.290" in result.failure


def test_equal_claude_versions_install_nothing(tmp_path):
    fake = _MirrorGh(remote_claude="2.1.290")
    assert _run_mirrored(tmp_path, fake, _cfg(tmp_path)).ok
    assert not any("claude-install" in c for c in fake.calls)


def test_a_refresh_token_that_rotates_makes_the_launch_choose_the_fallback_not_the_mirror(tmp_path):
    """Item 5, RED-first: the second refresher's old token is refused (the recorded verdict is
    `rotates`), so the cache is NOT copied; the item names the fallback and the one step that
    creates it, and the launch goes on (the lane's head does not need codex)."""
    fake = _MirrorGh()
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, verdicts={"codex": "rotates"}))
    assert result.ok, result.failure
    assert not any("install" in a for a, _ in fake.stdin), "nothing was copied"
    codex = next(i for i in result.mirror if i["cli"] == "codex")
    assert codex["action"] == "fallback" and codex["route"] == "secret-fallback"
    assert "OPERATOR-ACTION:" in codex["operator_action"]


def test_decisions_name_every_registry_cli_and_a_provider_without_one(tmp_path):
    items = d.credential_decisions(_cfg(tmp_path))
    by = {i.cli: i for i in items}
    assert {"codex", "claude", "agy"} <= set(by)
    assert by["agy"].action == "gap" and "keyring" in by["agy"].detail  # spec G1: a recorded GAP, not a wait
    assert by["claude"].route == "secret-token" and by["claude"].action == "not-mirrored"
    assert [i.cli for i in items if i.action == "no-cli"] == ["deepseek"]


def test_copilot_is_decided_by_its_token_route_and_is_not_left_waiting(tmp_path):
    """R88a, RED-first: Copilot signs in through the COPILOT_GITHUB_TOKEN secret, so the launch has
    nothing to mirror and nothing to wait on -- it is not an OPERATOR-ACTION line of its own."""
    registry = {"providers": {**_MIRROR_REGISTRY["providers"], "github": {"cli": "copilot"}},
                "roles": {}, "models": {}}
    by = {i.cli: i for i in d.credential_decisions(_cfg(tmp_path, registry=registry))}
    assert by["copilot"].route == "secret-token" and by["copilot"].action == "not-mirrored"
    assert by["copilot"].operator_action == ""


def test_a_cli_the_laptop_has_no_cache_for_is_recorded_absent_not_mirrored(tmp_path):
    cfg = _cfg(tmp_path, home=_home(tmp_path, codex_age=None))
    by = {i.cli: i for i in d.credential_decisions(cfg)}
    assert by["codex"].action == "absent" and by["codex"].files == ()


def test_the_codespace_exec_verb_builds_a_real_mirror_by_default(tmp_path, monkeypatch):
    """The CLI is the launcher: it hands `codespace_exec` a mirror, so no launch skips it."""
    from click.testing import CliRunner

    seen = {}

    def fake_exec(*a, **kw):
        seen.update(kw)
        return d.ExecResult(True, name="n")

    monkeypatch.setattr(d, "codespace_exec", fake_exec)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    res = CliRunner().invoke(d.cli, ["codespace-exec", str(contract), "--repo", "o/r", "--slug", "x",
                                     "--argv-json", '["claude"]', "--batch", "E9.1"])
    assert res.exit_code == 0, res.output
    assert isinstance(seen.get("mirror"), d.MirrorConfig)


# ============================== b2w2-codespace-finish (R87.3, plan M4) -- codex never sees an API key
#
# DERIVED FROM OpenAI's documentation (read 2026-10-09, Codex "Authentication"): `forced_login_method`
# takes `chatgpt | api`, `CODEX_API_KEY` is the non-interactive API route, and a key's precedence over a
# ChatGPT sign-in is NOT documented -- so the lane does not leave it to precedence: neither variable
# is in the environment of any codex invocation. Each test below launches a stub `codex` that records
# BOOLEANS ONLY (whether each variable reached it); a value is never written anywhere.

_NEVER_A, _NEVER_B = "SENTINEL-CODEX-KEY-0001", "SENTINEL-OPENAI-KEY-0002"

_CODEX_STUB = (
    "#!/usr/bin/env bash\n"
    'rec="${CODEX_STUB_RECORD:?}"\n'
    '{ for n in CODEX_API_KEY OPENAI_API_KEY; do\n'
    '    if [ -n "${!n:-}" ]; then echo "$n=yes"; else echo "$n=no"; fi\n'
    '  done; echo "argv=$*"; } >> "$rec"\n'
    'echo "codex-cli 0.0.0"\n'
)


def _bash_exe() -> str:
    """The first `bash` that runs a command (a Windows PATH can lead with the WSL launcher)."""
    import os
    import shutil

    candidates = [shutil.which("bash", path=p) for p in os.environ.get("PATH", "").split(os.pathsep) if p]
    git = shutil.which("git")
    if git:
        root = Path(git).resolve().parent.parent
        candidates += [str(root / "bin" / "bash.exe"), str(root / "usr" / "bin" / "bash.exe")]
    for candidate in candidates:
        if candidate is None or not Path(candidate).is_file():
            continue
        try:
            probe = subprocess.run([candidate, "-c", "echo bash-ok"], capture_output=True, text=True,
                                   timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if probe.returncode == 0 and probe.stdout.strip() == "bash-ok":
            return candidate
    raise AssertionError("no bash on PATH can run a command")


def _codex_stub(tmp_path):
    bin_dir = tmp_path / "stubbin"
    bin_dir.mkdir()
    stub = bin_dir / "codex"
    stub.write_text(_CODEX_STUB, encoding="utf-8", newline="\n")
    stub.chmod(0o755)
    return bin_dir, stub, tmp_path / "codex-record.txt"


def _what_the_stub_saw(record) -> dict:
    seen = {}
    for line in record.read_text(encoding="utf-8").splitlines():
        key, _, value = line.partition("=")
        seen[key] = value
    return seen


def test_codex_api_key_is_no_runner_secret_and_the_never_set_names_are_the_two_keys():
    assert "CODEX_API_KEY" not in d.RUNNER_SECRETS, "it is probed as a boolean, not carried as a lane secret"
    assert d.RUNNER_NEVER_SET == ("CODEX_API_KEY", "OPENAI_API_KEY")


@pytest.mark.parametrize("unset", [(), ("CODEX_API_KEY", "OPENAI_API_KEY")],
                         ids=["no-mirror", "mirror-configured"])
def test_the_runner_hands_a_codex_head_neither_api_key_with_or_without_a_mirror(tmp_path, unset):
    """Launch path 1. Seeded with both keys in the environment, the runner reports the PRESENCE of
    each as a boolean in the run log, removes it, and the head -- a stub `codex` -- sees neither."""
    import os

    bin_dir, stub, record = _codex_stub(tmp_path)
    workdir, checkout = tmp_path / "work", tmp_path / "checkout"
    workdir.mkdir()
    checkout.mkdir()
    runner = workdir / "run-lane.sh"
    runner.write_text(
        d._codespace_runner_script(workdir.as_posix(), checkout.as_posix(),
                                   [stub.as_posix(), "exec", "hello"], unset=unset),
        encoding="utf-8", newline="\n")
    env = {**os.environ, "CODEX_API_KEY": _NEVER_A, "OPENAI_API_KEY": _NEVER_B,
           "CODEX_STUB_RECORD": record.as_posix()}
    console = tmp_path / "console.txt"
    with open(console, "wb") as sink:       # a file, not a pipe: the runner's watchdog outlives it
        subprocess.run([_bash_exe(), runner.as_posix()], env=env, stdout=sink,
                       stderr=subprocess.STDOUT, timeout=180)
    assert _what_the_stub_saw(record) == {"CODEX_API_KEY": "no", "OPENAI_API_KEY": "no",
                                          "argv": "exec hello"}
    log = (workdir / "run.log").read_text(encoding="utf-8", errors="replace")
    for name in ("CODEX_API_KEY", "OPENAI_API_KEY"):
        assert f"[runner] api-key {name} present-before-unset=yes" in log, log
    for text in (log, console.read_text(encoding="utf-8", errors="replace"),
                 record.read_text(encoding="utf-8")):
        assert _NEVER_A not in text and _NEVER_B not in text, "a value reached an artefact"


def test_the_runner_script_unsets_the_two_keys_on_every_launch_and_never_expands_them():
    body = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["claude"])
    assert re.search(r"^unset CODEX_API_KEY OPENAI_API_KEY$", body, re.MULTILINE), body
    assert "present-before-unset" in body
    for name in ("CODEX_API_KEY", "OPENAI_API_KEY"):
        assert f"${name}" not in body and f"${{{name}}}" not in body


def test_the_credential_tools_status_call_runs_codex_without_either_key(tmp_path):
    """Launch path 2: `credential-tools.sh status codex` is the Codespace's own sign-in check; it
    must not be answered by a key. Run for real against a stub `codex`, with both keys seeded."""
    import os

    bin_dir, _stub, record = _codex_stub(tmp_path)
    script = tmp_path / d.CREDENTIAL_TOOLS_NAME
    script.write_text(d._credential_tools_script([]), encoding="utf-8", newline="\n")
    env = {**os.environ, "CODEX_API_KEY": _NEVER_A, "OPENAI_API_KEY": _NEVER_B,
           "CODEX_STUB_RECORD": record.as_posix(),
           "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", "")}
    run = subprocess.run([_bash_exe(), script.as_posix(), "status", "codex"], env=env,
                         capture_output=True, text=True, timeout=120)
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert _what_the_stub_saw(record) == {"CODEX_API_KEY": "no", "OPENAI_API_KEY": "no",
                                          "argv": "login status"}
    assert _NEVER_A not in run.stdout + run.stderr and _NEVER_B not in run.stdout + run.stderr


# =====================================================================================================
# codespace-finish-2026-10-14 (stage 2, RED-first): the credential seeding and the per-step receipts
# =====================================================================================================
#
# RED on 0d97edde: `codespace_exec` has no `batch`, `receipts_root` or `ledger_path`; `MirrorConfig`
# has no `refresh_codex`; there is no `MIRROR_LEAD_S`, `COPY_LIFETIME_S` or `codex_mirror_max_age_days`;
# the runner writes no commit witness, no handback and no EXIT trap; the helper has no agy sign-in
# subcommands; harvest and delete write no step row and the regime ledger's container row is never
# opened or closed by the verbs. The spec is `SPEC.md` section 3 / section 5 of the stage chain.
#
# Everything is offline: the `invoker` seam, `tmp_path` receipt and ledger seams, FAKE credential bytes
# (`_SENTINEL_CODEX`). The runner script itself is executed with a real bash and a real git against a
# local bare "origin" (ADR-127: skipped with its reason where no bash can run a command).

_cpar = d.cpar

_FIN_BATCH = "B1"
_AGY_URL = FAKE_URL
_A40, _B40 = "a" * 40, "b" * 40

_GOOD_COMMIT = {"base_sha": _A40, "head_sha": _B40, "branch": "worktree-x", "pushed_sha": _B40,
                "committed": True, "pushed": True, "push_exit": 0}
_NO_COMMIT = {"base_sha": _A40, "head_sha": _A40, "branch": "worktree-x", "pushed_sha": None,
              "committed": False, "pushed": False, "push_exit": None}
_NOT_ON_ORIGIN = {"base_sha": _A40, "head_sha": _B40, "branch": "worktree-x", "pushed_sha": _A40,
                  "committed": True, "pushed": False, "push_exit": 1}

_LANE_REPORT = {
    "lane": "lane-x", "batch": "B1", "task": "a sample task", "kind": "doc", "state": "COMPLETED",
    "done": {"met": 1, "total": 1},
    "checks": [{"name": "pre-commit", "how": "deterministic", "result": "PASS", "evidence": "all hooks passed"}],
    "intent_met": None, "unresolved": [], "operator_action": None, "merged_sha": None,
    "producer": {"vendor": "anthropic", "model": "claude-sonnet-5", "session": "sess-1"},
    "cost_usd": None,
    "evidence": {"branch": "worktree-x", "check_run": None, "audit": None},
}

_GOOD_RECEIPT = {"exit_code": 0, "is_error": False, "status": "success", "turns": 3,
                 "transcript": {"session_id": "sess-1", "path": ""},
                 "commit": _GOOD_COMMIT, "handback": {"present": True}}


_FAKE_AGY_VERBS = ("agy-signin-start", "agy-signin-code", "agy-probe", "agy-signin-stop", "agy-signin-diag")


class _FinishGh(_MirrorGh):
    """`_MirrorGh` plus what the finish adds: the agy sign-in helper subcommand (answers a URL line, or
    nothing) and the `ssh cat <workdir>/handback.json` read. `receipt_written` defaults to a lane that
    committed, pushed and handed back."""

    def __init__(self, *, agy_url: str | None = _AGY_URL, handback: str | None = None,
                 agy: FakeAgy | None = None, **kw):
        kw.setdefault("receipt_written", copy.deepcopy(_GOOD_RECEIPT))
        super().__init__(**kw)
        self.agy = agy if agy is not None else FakeAgy(url=agy_url)
        self.handback = json.dumps(_LANE_REPORT) if handback is None else handback

    @property
    def agy_calls(self) -> int:
        return self.agy.started

    def __call__(self, argv, input_bytes=None):
        argv = list(argv)
        if argv[:2] == ["codespace", "ssh"] and argv[-1].endswith("handback.json"):
            self.calls.append(argv)
            if self.handback == "":
                return d.GhResult(False, 1, "")
            return d.GhResult(True, 0, self.handback)
        return super().__call__(argv, input_bytes)

    def _tools(self, tail, input_bytes):
        if tail[0] in _FAKE_AGY_VERBS:
            return self.agy.handle(tail, input_bytes)
        return super()._tools(tail, input_bytes)


def _fin_exec(base: Path, fake, cfg=None, **kw):
    """One `codespace_exec` with the three new seams under `base`. `base` is used ONCE per test
    (`_cfg` builds the laptop HOME under it)."""
    contract = base / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    return d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                            invoker=fake, mirror=cfg if cfg is not None else _cfg(base),
                            batch=_FIN_BATCH, receipts_root=base / "rr",
                            ledger_path=base / "ledger.jsonl", **kw)


def _steps_path(base: Path, batch: str = _FIN_BATCH, lane: str = "lane-x") -> Path:
    return base / "rr" / batch / lane / "steps.jsonl"


def _rows(base: Path, batch: str = _FIN_BATCH, lane: str = "lane-x") -> list[dict]:
    path = _steps_path(base, batch, lane)
    if not path.is_file():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _row(base: Path, step: str, **kw) -> dict:
    found = [r for r in _rows(base, **kw) if r.get("step") == step]
    assert found, f"no {step!r} step row in {_steps_path(base)}"
    return found[-1]


def _ledger_rows(base: Path) -> list[dict]:
    path = base / "ledger.jsonl"
    if not path.is_file():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _sub(tmp_path: Path, name: str) -> Path:
    path = tmp_path / name
    path.mkdir()
    return path


_REGISTRY_ALL_FIVE = {"providers": {**_MIRROR_REGISTRY["providers"], "github": {"cli": "copilot"}},
                      "roles": {}, "models": {}}


# ----- 1-4: create ---------------------------------------------------------------------------------

def test_codespace_exec_writes_a_create_step_receipt_naming_the_codespace(tmp_path):
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    row = _row(tmp_path, "create")
    assert row["schema"] == 1 and row["kind"] == "codespace-step"
    assert row["batch"] == _FIN_BATCH and row["lane"] == "lane-x"
    assert row["codespace"] == "fluffy-space-1" and row["ok"] is True and row["failure"] == ""
    assert row["fate"] == {} and row["recorded"]
    assert set(row["evidence"]) == {"repo", "branch", "machine", "exit_code"}
    assert row["evidence"]["repo"] == "me/repo" and row["evidence"]["exit_code"] == 0
    assert len(result.steps) == len(_rows(tmp_path)), "ExecResult.steps carries the rows written"


def test_codespace_exec_opens_a_regime_ledger_row_on_create(tmp_path):
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    rows = [r for r in _ledger_rows(tmp_path) if r.get("kind") == "codespace"]
    # the creation row stays; the first successful ssh appends ONE more open row stamped `ready`
    assert len(rows) == 2, rows
    assert rows[0]["ready"] is None and rows[1]["ready"]
    row = rows[-1]
    assert row["open"] is True and row["deleted"] is None and row["created"]
    assert row["codespace"] == "fluffy-space-1" and row["slug"] == "lane-x"
    assert row["batch"] == _FIN_BATCH and row["machine"] == "standardLinux32gb"
    assert row["prebuild"] is False and row["tokens"] == {}
    assert [r["codespace"] for r in _regime.open_receipts(tmp_path / "ledger.jsonl")] == ["fluffy-space-1"]


def test_a_failed_create_writes_a_failed_create_step_and_no_ledger_row(tmp_path):
    result = _fin_exec(tmp_path, _FinishGh(fail_at="codespace create"))
    assert not result.ok
    row = _row(tmp_path, "create")
    assert row["ok"] is False and row["codespace"] == "" and row["failure"]
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "create"
    assert _ledger_rows(tmp_path) == [], "a box that never existed has no container row"


def test_the_codespace_exec_cli_requires_batch(tmp_path, monkeypatch):
    """The click usage error when `--batch` is missing; with it, the value reaches `codespace_exec`.
    `codespace_exec` is stubbed so a RED run can never reach a real `gh`."""
    from click.testing import CliRunner

    seen = {}

    def fake_exec(*a, **kw):
        seen.update(kw)
        return d.ExecResult(True, name="n")

    monkeypatch.setattr(d, "codespace_exec", fake_exec)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    base = ["codespace-exec", str(contract), "--repo", "o/r", "--slug", "x", "--argv-json", '["claude"]']
    missing = CliRunner().invoke(d.cli, base)
    assert missing.exit_code == 2 and "--batch" in missing.output, missing.output
    assert not seen, "a usage error launches nothing"
    given = CliRunner().invoke(d.cli, [*base, "--batch", "E9.9"])
    assert given.exit_code == 0, given.output
    assert seen.get("batch") == "E9.9"


# ----- 5-6, 12-14: the credentials step ------------------------------------------------------------

def test_the_credentials_step_names_claude_codex_copilot_gh_and_agy_with_route_and_action(tmp_path):
    cfg = _cfg(tmp_path, registry=_REGISTRY_ALL_FIVE)
    result = _fin_exec(tmp_path, _FinishGh(), cfg)
    assert result.ok, result.failure
    row = _row(tmp_path, "credentials")
    assert row["ok"] is True and row["codespace"] == "fluffy-space-1"
    by = {c["cli"]: c for c in row["evidence"]["clis"]}
    assert {k: by[k]["action"] for k in ("claude", "codex", "copilot", "gh", "agy")} == {
        "claude": "not-mirrored", "codex": "mirrored", "copilot": "not-mirrored",
        "gh": "not-mirrored", "agy": "gap"}
    assert all(by[k]["route"] for k in ("claude", "codex", "copilot", "gh", "agy"))
    assert row["evidence"]["gaps"] == ["agy"]


def test_a_refused_credential_before_create_writes_a_failed_credentials_step_with_no_codespace_name(tmp_path):
    home = _home(tmp_path, codex_age=None)
    (home / ".codex" / "auth.json").write_text(json.dumps({"auth_mode": "apikey"}), encoding="utf-8")
    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, _cfg(tmp_path, home=home))
    assert not result.ok and fake.calls == []
    row = _row(tmp_path, "credentials")
    assert row["ok"] is False and row["codespace"] == "" and "codex login" in row["failure"]
    assert row["fate"]["fate"] == "WAITING" and row["fate"]["step"] == "credentials"


def test_only_the_codex_cache_crosses_stdin_and_the_claude_oauth_file_never_does(tmp_path):
    """GUARD on existing behaviour (the stdin copy is today's): it is RED only through the new kwargs.
    The claude OAuth file's refresh token ROTATES, so a copy would sign the laptop out."""
    cfg = _cfg(tmp_path)
    claude_file = cfg.home / ".claude" / ".credentials.json"
    claude_file.parent.mkdir(parents=True)
    claude_file.write_text(json.dumps({"claudeAiOauth": {"refreshToken": _SENTINEL_GEMINI}}), encoding="utf-8")
    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, cfg)
    assert result.ok, result.failure
    assert [(a[a.index("install") + 1]) for a, _b in fake.stdin if "install" in a] == [".codex/auth.json"]
    assert all(_SENTINEL_GEMINI.encode() not in b for _a, b in fake.stdin)
    assert not any(".credentials.json" in " ".join(c) for c in fake.calls)
    assert _row(tmp_path, "credentials")["evidence"]["clis"], "the step row names what was decided"
    assert ".credentials.json" not in _steps_path(tmp_path).read_text(encoding="utf-8")


def test_agy_is_a_recorded_gap_and_the_launch_continues(tmp_path):
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    agy = next(i for i in result.mirror if i["cli"] == "agy")
    assert agy["action"] == "gap" and agy["gap"] == "agy-interactive-sign-in"
    assert agy["operator_action"], "the renew line is named"
    by = {i.cli: i for i in d.credential_decisions(_cfg(_sub(tmp_path, "dec")))}
    assert by["agy"].action == "gap" and by["agy"].operator_action


def test_the_agy_url_reaches_stderr_and_the_credentials_row_but_never_the_ledger_or_the_commands(tmp_path, capsys):
    """AMENDED (R7): the URL is in stderr AND the credentials step row (the receipt); never in the regime
    ledger and never in `result.commands`."""
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    err = capsys.readouterr().err
    assert _AGY_URL in err and "fluffy-space-1" in err, "the operator sees the URL and the box"
    commands = "\n".join(result.commands)
    assert _AGY_URL not in commands and "fake-not-real" not in commands
    assert _AGY_URL in json.dumps(_row(tmp_path, "credentials")), "the receipt carries the operator-action line"
    ledger = (tmp_path / "ledger.jsonl").read_text(encoding="utf-8")
    assert "fake-not-real" not in ledger and "agy.invalid" not in ledger
    assert next(i for i in result.mirror if i["cli"] == "agy")["auth_url_surfaced"] is True


def test_an_agy_signin_that_prints_no_url_records_false_and_does_not_block(tmp_path, capsys):
    result = _fin_exec(tmp_path, _FinishGh(agy_url=None))
    assert result.ok, result.failure
    agy = next(i for i in result.mirror if i["cli"] == "agy")
    assert agy["auth_url_surfaced"] is False and agy["action"] == "gap"
    assert "https://" not in capsys.readouterr().err


def test_the_helper_has_agy_signin_subcommands_and_takes_the_code_on_stdin_only():
    script = d._credential_tools_script([])
    assert "agy-signin-start" in script and "agy-signin-code" in script
    assert "mkfifo" in script, "stdin of the pty'd agy comes from a FIFO"
    assert "timeout 900" in script, "its life is bounded"
    assert "chmod 700" in script
    start = script.index("agy-signin-code)")
    branch = script[start:script.index(";;", start)]
    assert "read" in branch, "the code is read from stdin"
    assert "$2" not in branch and "${2" not in branch and "$@" not in branch, "never a positional code"


# ----- 7-10: the codex age guard -------------------------------------------------------------------

def test_the_codex_mirror_window_is_derived_from_the_run_bound(tmp_path):
    assert d.MIRROR_LEAD_S == 3600
    assert d.COPY_LIFETIME_S == d.RUN_TIMEOUT_SECONDS + d.MIRROR_LEAD_S
    expected = _cpar.CODEX_REFRESH_DAYS - d.COPY_LIFETIME_S / 86400
    assert d.codex_mirror_max_age_days() == pytest.approx(expected)
    assert getattr(_cpar, "CODEX_MIRROR_MAX_AGE_DAYS", None) != 7.0, "the typed 7.0 is gone"
    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, _cfg(tmp_path, home=_home(tmp_path, codex_age=7.5)))
    assert result.ok, result.failure
    assert next(i for i in result.mirror if i["cli"] == "codex")["action"] == "mirrored"
    assert any("install" in a for a, _b in fake.stdin)


def test_codex_in_the_band_is_refused_with_the_instant_it_reopens_and_no_codex_exec_remedy(tmp_path):
    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, _cfg(tmp_path, home=_home(tmp_path, codex_age=7.9)))
    assert not result.ok and fake.calls == []
    assert result.fate["fate"] == "WAITING" and result.fate["step"] == "credentials"
    reopen = _NOW - timedelta(days=7.9) + timedelta(days=_cpar.CODEX_REFRESH_DAYS)
    assert reopen.strftime("%Y-%m-%d") in result.failure and reopen.strftime("%H:%M") in result.failure
    assert "run any `codex exec`" not in result.failure, "that remedy is false in this band"
    assert result.failure.count("OPERATOR-ACTION:") == 1


def _refresh_cfg(tmp_path, home, refresh):
    return d.MirrorConfig(home=home, env={}, registry=_MIRROR_REGISTRY, now=_NOW,
                          local_versions={"claude": "2.1.290"}, verdicts={}, refresh_codex=refresh)


def test_a_due_codex_cache_is_refreshed_by_one_keyless_laptop_call_then_mirrored(tmp_path, monkeypatch):
    home = _home(tmp_path, codex_age=8.5)
    calls: list[int] = []

    def refresh() -> bool:
        calls.append(1)
        (home / ".codex" / "auth.json").write_text(_codex_auth(0.0), encoding="utf-8")
        return True

    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, _refresh_cfg(tmp_path, home, refresh))
    assert result.ok, result.failure
    assert calls == [1], "exactly one laptop-side call"
    codex = next(i for i in result.mirror if i["cli"] == "codex")
    assert codex["action"] == "mirrored" and "refreshed" in codex["detail"]
    shipped = [b for a, b in fake.stdin if "install" in a]
    assert shipped == [(home / ".codex" / "auth.json").read_bytes()], "the REFRESHED cache is what ships"

    # the DEFAULT refresher: neither API key reaches the laptop-side codex call
    seen = []

    def fake_run(argv, *a, **kw):
        seen.append((list(argv), kw.get("env")))
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setenv("CODEX_API_KEY", "fake-token-not-real")
    monkeypatch.setenv("OPENAI_API_KEY", "fake-token-not-real")
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(shutil, "which", lambda name, *a, **k: name)
    due_home = _home(_sub(tmp_path, "due"), codex_age=8.5)
    cfg = d.MirrorConfig(home=due_home, env={"CODEX_API_KEY": "fake-token-not-real",
                                             "OPENAI_API_KEY": "fake-token-not-real"},
                         registry=_MIRROR_REGISTRY, now=_NOW, local_versions={"claude": "2.1.290"})
    d.credential_decisions(cfg)
    codex_calls = [(a, e) for a, e in seen if "codex" in " ".join(a) and "exec" in a]
    assert len(codex_calls) == 1, seen
    argv, env = codex_calls[0]
    assert "--skip-git-repo-check" in argv and "read-only" in argv
    keyless = (env is not None and not {"CODEX_API_KEY", "OPENAI_API_KEY"} & set(env)) or (
        "-u" in argv and "CODEX_API_KEY" in argv and "OPENAI_API_KEY" in argv)
    assert keyless, "the refresh call is run with neither API key"


def test_a_due_codex_cache_the_laptop_call_did_not_refresh_is_refused(tmp_path):
    home = _home(tmp_path, codex_age=8.5)
    calls: list[int] = []

    def refresh() -> bool:
        calls.append(1)
        return True            # the call "ran" but the cache's last_refresh did not move

    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, _refresh_cfg(tmp_path, home, refresh))
    assert calls == [1]
    assert not result.ok and fake.calls == []
    assert result.fate["fate"] == "WAITING" and "codex login" in result.failure


# ----- 11: the EXIT trap ---------------------------------------------------------------------------

def _bash_or_skip() -> str:
    try:
        return _bash_exe()
    except AssertionError:
        pytest.skip("no bash on PATH can run a command here (ADR-127: skipped with its reason, not passed)")


#: git under some harnesses runs with `safe.bareRepository=explicit`; the local bare "origin" must be usable.
_GIT_BARE_OK = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.bareRepository",
                "GIT_CONFIG_VALUE_0": "all"}


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True, text=True,
                          env={**os.environ, **_GIT_BARE_OK}).stdout.strip()


def _git_lane(base: Path, branch: str = "worktree-x"):
    """A checkout on `branch` with a local bare `origin` that already holds `main`."""
    if shutil.which("git") is None:
        pytest.skip("no git on PATH")
    origin, checkout = base / "origin.git", base / "checkout"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True,
                   env={**os.environ, **_GIT_BARE_OK})
    checkout.mkdir()
    _git(checkout, "init", "-q", "-b", "main")
    for key, value in (("user.name", "t"), ("user.email", "t@example.invalid"), ("commit.gpgsign", "false")):
        _git(checkout, "config", key, value)
    _git(checkout, "remote", "add", "origin", origin.as_posix())
    _git(checkout, "commit", "-q", "--allow-empty", "-m", "base")
    _git(checkout, "push", "-q", "origin", "main")
    if branch != "main":
        _git(checkout, "checkout", "-q", "-b", branch)
    return origin, checkout


def _lane_env(base: Path) -> dict:
    stubbin = base / "stubbin"
    stubbin.mkdir(exist_ok=True)
    shim = stubbin / "python3"
    shim.write_text(f'#!/usr/bin/env bash\nexec "{Path(sys.executable).as_posix()}" "$@"\n',
                    encoding="utf-8", newline="\n")
    shim.chmod(0o755)
    home = base / "home"
    home.mkdir(exist_ok=True)
    return {**os.environ, "HOME": home.as_posix(), "PATH": str(stubbin) + os.pathsep + os.environ.get("PATH", ""),
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid", **_GIT_BARE_OK}


def _run_runner(base: Path, body: str, workdir: Path, env: dict) -> None:
    runner = workdir / "run-lane.sh"
    runner.write_text(body, encoding="utf-8", newline="\n")
    with open(base / "console.txt", "wb") as sink:     # a file, not a pipe: the watchdog outlives it
        subprocess.run([_bash_or_skip(), runner.as_posix()], env=env, stdout=sink,
                       stderr=subprocess.STDOUT, timeout=180)


def _head_stub(base: Path, lines: str) -> list[str]:
    stub = base / "head.sh"
    stub.write_text("#!/usr/bin/env bash\n" + lines, encoding="utf-8", newline="\n")
    return [_bash_or_skip(), stub.as_posix()]


@pytest.mark.parametrize("head_exit", [0, 3], ids=["clean-exit", "non-zero-exit"])
def test_the_runner_removes_every_mirrored_cache_on_exit(tmp_path, head_exit):
    """The mirrored `$HOME/.codex/auth.json` cannot outlive the run: an EXIT trap removes it, also on a
    non-zero head exit (this is what makes the age window a real bound)."""
    _bash_or_skip()
    _origin, checkout = _git_lane(tmp_path)
    work = _sub(tmp_path, "work")
    fake = _FinishGh()
    cfg = _cfg(tmp_path)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    head = _head_stub(tmp_path, f"exit {head_exit}\n")
    result = d.codespace_exec("me/repo", "main", "lane-x", contract, head, invoker=fake, mirror=cfg,
                              batch=_FIN_BATCH, receipts_root=tmp_path / "rr",
                              ledger_path=tmp_path / "ledger.jsonl")
    assert result.ok, result.failure
    body = fake.runner_body.replace("/workspaces/dispatch", work.as_posix()) \
                           .replace("/workspaces/repo", checkout.as_posix())
    cache = cfg.home / ".codex" / "auth.json"
    assert cache.is_file()
    _run_runner(tmp_path, body, work, {**_lane_env(tmp_path), "HOME": cfg.home.as_posix()})
    assert (work / "receipt.json").is_file(), "the runner ran to its receipt"
    assert not cache.exists(), "the mirrored codex cache must be removed by the runner's EXIT trap"


# ----- 16-17, 20: the commit witness and the handback, from the REAL runner -----------------------

def _lane_run(base: Path, *, branch: str = "worktree-x", head_lines: str):
    origin, checkout = _git_lane(base, branch)
    work = _sub(base, "work")
    head = _head_stub(base, head_lines)
    body = d._codespace_runner_script(work.as_posix(), checkout.as_posix(), head)
    _run_runner(base, body, work, _lane_env(base))
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    return origin, checkout, work, receipt


def test_the_runner_writes_a_commit_witness_into_the_receipt(tmp_path):
    origin, checkout, _work, receipt = _lane_run(tmp_path, head_lines='git commit -q --allow-empty -m "lane work"\n')
    commit = receipt["commit"]
    assert set(commit) == {"base_sha", "head_sha", "branch", "pushed_sha", "committed", "pushed", "push_exit"}
    head = _git(checkout, "rev-parse", "HEAD")
    assert commit["head_sha"] == head and commit["base_sha"] != head
    assert commit["branch"] == "worktree-x" and commit["committed"] is True
    assert commit["pushed"] is True and commit["pushed_sha"] == head and commit["push_exit"] == 0
    assert _git(checkout, "ls-remote", "origin", "refs/heads/worktree-x").split()[0] == head


def test_a_lane_that_commits_nothing_has_an_unpushed_witness(tmp_path):
    _origin, checkout, _work, receipt = _lane_run(tmp_path, head_lines="true\n")
    commit = receipt["commit"]
    assert commit["committed"] is False and commit["pushed"] is False
    assert commit["head_sha"] == commit["base_sha"] == _git(checkout, "rev-parse", "HEAD")


def test_the_runner_pushes_only_its_own_branch_and_never_main(tmp_path):
    body = d._codespace_runner_script("/w", "/c", ["true"])
    assert "HEAD:refs/heads/" in body, "the refspec is HEAD:refs/heads/<branch>"
    assert "--force" not in body and "--no-verify" not in body
    origin, checkout, _work, receipt = _lane_run(tmp_path, branch="main",
                                                 head_lines='git commit -q --allow-empty -m "oops on main"\n')
    base_main = _git(origin, "rev-parse", "refs/heads/main")
    assert base_main != _git(checkout, "rev-parse", "HEAD"), "the lane did commit on main"
    assert receipt["commit"]["committed"] is True and receipt["commit"]["pushed"] is False
    assert _git(origin, "rev-parse", "refs/heads/main") == base_main, "main on origin never moves"


def test_a_lane_that_commits_in_a_linked_worktree_branch_is_witnessed_and_pushed(tmp_path):
    """Live 2026-10-16 (batch-resume-night PART B): the lane followed the repo rule "parallel work
    needs a worktree", committed its RED and fix on `worktree-lane-<slug>` in a linked worktree, and the
    checkout's own HEAD never moved -- the witness read "the lane committed nothing" for finished work.
    The runner now also looks at the lane's declared branch."""
    origin, checkout = _git_lane(tmp_path, "main")
    work = _sub(tmp_path, "work")
    wt = (tmp_path / "lane-wt").as_posix()
    head = _head_stub(tmp_path, f'git worktree add -q "{wt}" -b worktree-lane-x\n'
                                f'git -C "{wt}" commit -q --allow-empty -m "lane work in a linked worktree"\n')
    body = d._codespace_runner_script(work.as_posix(), checkout.as_posix(), head,
                                      lane_branch="worktree-lane-x")
    _run_runner(tmp_path, body, work, _lane_env(tmp_path))
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    commit = receipt["commit"]
    lane_tip = _git(checkout, "rev-parse", "refs/heads/worktree-lane-x")
    assert commit["committed"] is True and commit["branch"] == "worktree-lane-x"
    assert commit["head_sha"] == lane_tip and commit["pushed"] is True
    assert _git(origin, "rev-parse", "refs/heads/worktree-lane-x") == lane_tip


_STREAM_FIRST = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1,
                 "session_id": "s-0", "structured_output": {"state": "FAILED", "marker": "first"}}


def _stream_head(base: Path, last: dict) -> str:
    data = base / "stream.jsonl"
    data.write_text("\n".join([json.dumps(_STREAM_FIRST), json.dumps({"type": "assistant", "message": "x"}),
                               json.dumps(last)]) + "\n", encoding="utf-8", newline="\n")
    return f'cat "{data.as_posix()}"\n'


def test_the_runner_writes_the_lane_report_as_handback_json(tmp_path):
    last = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 2,
            "session_id": "s-1", "structured_output": _LANE_REPORT}
    _origin, _checkout, work, receipt = _lane_run(tmp_path, head_lines=_stream_head(tmp_path, last))
    assert json.loads((work / "handback.json").read_text(encoding="utf-8")) == _LANE_REPORT, \
        "the LAST result object's structured_output, not the first"
    assert receipt["handback"] == {"present": True}


def test_the_runner_records_no_handback_when_the_last_result_has_no_structured_output(tmp_path):
    last = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 2, "session_id": "s-1"}
    _origin, _checkout, work, receipt = _lane_run(tmp_path, head_lines=_stream_head(tmp_path, last))
    assert receipt["handback"] == {"present": False}
    assert not (work / "handback.json").exists()


# ----- 18-19: the commit step ----------------------------------------------------------------------

def test_a_lane_that_committed_nothing_fails_at_the_commit_step(tmp_path):
    fake = _FinishGh(receipt_written={**copy.deepcopy(_GOOD_RECEIPT), "commit": _NO_COMMIT})
    result = _fin_exec(tmp_path, fake)
    assert not result.ok
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "commit"
    row = _row(tmp_path, "commit")
    assert row["ok"] is False and row["evidence"]["committed"] is False
    assert set(row["evidence"]) == {"branch", "base_sha", "head_sha", "pushed_sha", "committed",
                                    "pushed", "push_exit"}
    assert _row(tmp_path, "run")["ok"] is True


def test_the_codespace_exec_cli_exits_no_commit_when_the_fate_is_the_commit_step(tmp_path, monkeypatch):
    from click.testing import CliRunner

    monkeypatch.setattr(d, "codespace_exec", lambda *a, **kw: d.ExecResult(
        False, name="n", failure="the lane committed nothing",
        fate={"fate": "FAILED", "step": "commit", "reason": "committed nothing"}))
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    res = CliRunner().invoke(d.cli, ["codespace-exec", str(contract), "--repo", "o/r", "--slug", "x",
                                     "--argv-json", '["claude"]', "--batch", "E9.1"])
    assert res.exit_code == d.EXIT_NO_COMMIT == 6, res.output


def test_a_commit_not_on_origin_fails_at_the_commit_step(tmp_path):
    fake = _FinishGh(receipt_written={**copy.deepcopy(_GOOD_RECEIPT), "commit": _NOT_ON_ORIGIN})
    result = _fin_exec(tmp_path, fake)
    assert not result.ok
    assert result.fate["step"] == "commit"
    row = _row(tmp_path, "commit")
    assert row["ok"] is False and row["evidence"]["committed"] is True and row["evidence"]["pushed"] is False


# ----- 21: the handback step -----------------------------------------------------------------------

def test_a_missing_or_invalid_handback_fails_at_the_handback_step(tmp_path):
    from ecosystem.schema.lane_report import LaneReport

    LaneReport.model_validate(_LANE_REPORT)       # the fixture is itself a valid LANE REPORT

    good = _fin_exec(_sub(tmp_path, "good"), _FinishGh())
    assert good.ok, good.failure
    row = _row(tmp_path / "good", "handback")
    assert row["ok"] is True and row["evidence"] == {"present": True, "valid": True, "errors": []}

    missing = _fin_exec(_sub(tmp_path, "missing"), _FinishGh(handback=""))
    assert not missing.ok and missing.fate["step"] == "handback"
    row = _row(tmp_path / "missing", "handback")
    assert row["ok"] is False and row["evidence"]["present"] is False and row["evidence"]["valid"] is False

    invalid = _fin_exec(_sub(tmp_path, "invalid"), _FinishGh(handback=json.dumps({"state": "BOGUS"})))
    assert not invalid.ok and invalid.fate["step"] == "handback"
    row = _row(tmp_path / "invalid", "handback")
    assert row["evidence"]["present"] is True and row["evidence"]["valid"] is False
    assert row["evidence"]["errors"] and all(isinstance(e, str) for e in row["evidence"]["errors"])

    both = _fin_exec(_sub(tmp_path, "both"), _FinishGh(
        handback=json.dumps({"state": "BOGUS"}), receipt_written={**copy.deepcopy(_GOOD_RECEIPT), "commit": _NO_COMMIT}))
    assert both.fate["step"] == "commit", "the first failure in run, commit, handback order is the fate"
    assert {r["step"] for r in _rows(tmp_path / "both")} >= {"run", "commit", "handback"}, \
        "every row is still written whenever its evidence exists"


def test_the_run_step_row_carries_exit_code_status_turns_and_session(tmp_path):
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    row = _row(tmp_path, "run")
    assert row["ok"] is True
    assert row["evidence"] == {"exit_code": 0, "status": "success", "is_error": False, "turns": 3,
                               "session_id": "sess-1"}
    assert [r["step"] for r in _rows(tmp_path)] == ["create", "credentials", "run", "commit", "handback"]
    assert all(r["ok"] is True for r in _rows(tmp_path))


# ----- 22: harvest ---------------------------------------------------------------------------------

def test_harvest_collects_handback_json_and_writes_a_harvest_step(tmp_path):
    assert d.HARVEST_FILES == ("run.log", "receipt.json", "handback.json")
    fake = _ssh_cat_fake({"run.log": "x\n", "receipt.json": '{"exit_code": 0}\n',
                          "handback.json": json.dumps(_LANE_REPORT) + "\n"})
    result = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-h", out_root=tmp_path, invoker=fake)
    assert result.ok, result.failure
    assert "handback.json" in result.files
    rows = [json.loads(ln) for ln in (tmp_path / "B1" / "lane-h" / "steps.jsonl").read_text("utf-8").splitlines()]
    assert [r["step"] for r in rows] == ["harvest"]
    row = rows[0]
    assert row["ok"] is True and row["codespace"] == "fluffy-1" and row["kind"] == "codespace-step"
    assert row["evidence"]["files"] == result.files
    assert row["evidence"]["manifest_path"] == str(result.manifest_path)
    again = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-h", out_root=tmp_path, invoker=fake)
    assert not again.ok
    rows = [json.loads(ln) for ln in (tmp_path / "B1" / "lane-h" / "steps.jsonl").read_text("utf-8").splitlines()]
    assert [r["ok"] for r in rows] == [True, False], "a refusal writes ok: false"
    d.codespace_harvest("fluffy-1", batch="B1", lane="lane-dry", out_root=tmp_path, dry_run=True, invoker=fake)
    assert not (tmp_path / "B1" / "lane-dry" / "steps.jsonl").exists(), "a dry run writes no row"


# ----- 23-24: delete -------------------------------------------------------------------------------

def _open_row(ledger: Path, name: str = "fluffy-1", minutes: float = 30.0):
    now = datetime.now(timezone.utc)
    _regime.write_receipt("lane-x", "B1", name, created=now - timedelta(minutes=minutes), deleted=None,
                          machine="standardLinux32gb", prebuild=False, tokens={}, ledger_path=ledger)


def test_delete_writes_a_delete_step_and_closes_the_regime_row(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    _open_row(ledger)
    assert [r["codespace"] for r in _regime.open_receipts(ledger)] == ["fluffy-1"]
    harvested = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-x", out_root=tmp_path / "rr",
                                    invoker=_ssh_cat_fake({"run.log": "clean\n"}))
    calls = []

    def fake_delete(argv):
        calls.append(list(argv))
        return d.GhResult(ok=True, exit_code=0, stdout="")

    result = d.codespace_delete("fluffy-1", out_dir=harvested.out_dir, invoker=fake_delete,
                                batch="B1", lane="lane-x", receipts_root=tmp_path / "rr", ledger_path=ledger)
    assert result.ok and calls == [["codespace", "delete", "-c", "fluffy-1", "--force"]]
    row = _row(tmp_path, "delete")
    assert row["ok"] is True and row["codespace"] == "fluffy-1"
    assert row["evidence"]["refused"] is False and row["evidence"]["exit_code"] == 0
    assert row["evidence"]["uptime_minutes"] > 0
    assert _regime.open_receipts(ledger) == [], "the container row is closed"
    closed = [r for r in map(json.loads, ledger.read_text("utf-8").splitlines()) if r.get("codespace") == "fluffy-1"][-1]
    assert closed["open"] is False and closed["deleted"] and closed["uptime_minutes"] > 0


def test_a_refused_delete_writes_a_refused_step_and_leaves_the_regime_row_open(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    _open_row(ledger)

    def fake_delete(argv):  # pragma: no cover -- must not be reached
        raise AssertionError("gh must not be called when the harvest is unverified")

    result = d.codespace_delete("fluffy-1", out_dir=tmp_path / "rr" / "B1" / "lane-x", invoker=fake_delete,
                                batch="B1", lane="lane-x", receipts_root=tmp_path / "rr", ledger_path=ledger)
    assert result.refused
    row = _row(tmp_path, "delete")
    assert row["ok"] is False and row["evidence"]["refused"] is True and row["evidence"]["reason"]
    assert [r["codespace"] for r in _regime.open_receipts(ledger)] == ["fluffy-1"], "no regime row written"


def test_a_failed_gh_delete_writes_a_failed_step_and_no_closed_regime_row(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    _open_row(ledger)
    harvested = d.codespace_harvest("fluffy-1", batch="B1", lane="lane-x", out_root=tmp_path / "rr",
                                    invoker=_ssh_cat_fake({"run.log": "clean\n"}))
    result = d.codespace_delete("fluffy-1", out_dir=harvested.out_dir,
                                invoker=lambda argv: d.GhResult(ok=False, exit_code=1, stdout="boom"),
                                batch="B1", lane="lane-x", receipts_root=tmp_path / "rr", ledger_path=ledger)
    assert not result.ok and not result.refused
    row = _row(tmp_path, "delete")
    assert row["ok"] is False and row["evidence"]["exit_code"] == 1
    assert [r["codespace"] for r in _regime.open_receipts(ledger)] == ["fluffy-1"]


# ----- 25: no credential byte in any row -----------------------------------------------------------

def test_no_credential_byte_reaches_any_step_row_or_ledger_row(tmp_path):
    cfg = _cfg(tmp_path)
    codex_bytes = (cfg.home / ".codex" / "auth.json").read_bytes()
    fake = _FinishGh()
    result = _fin_exec(tmp_path, fake, cfg)
    assert result.ok, result.failure
    harvested = d.codespace_harvest(result.name, batch=_FIN_BATCH, lane="lane-x", out_root=tmp_path / "rr",
                                    invoker=_ssh_cat_fake({"run.log": "clean\n", "receipt.json": "{}\n"}))
    assert harvested.ok, harvested.failure
    deleted = d.codespace_delete(result.name, out_dir=harvested.out_dir, invoker=lambda argv: d.GhResult(True, 0, ""),
                                 batch=_FIN_BATCH, lane="lane-x", receipts_root=tmp_path / "rr",
                                 ledger_path=tmp_path / "ledger.jsonl")
    assert deleted.ok
    steps = _steps_path(tmp_path).read_text(encoding="utf-8")
    ledger = (tmp_path / "ledger.jsonl").read_text(encoding="utf-8")
    assert len(_rows(tmp_path)) >= 7 and ledger.strip(), "the flow really wrote its rows (no vacuous pass)"
    assert d.leak_check({"codex": codex_bytes}, [steps, ledger]) == []


# ----- round 2 (judge R1): batch is required; a credential byte in a harvested file is flagged -------

def test_codespace_exec_without_a_batch_is_refused_not_a_silent_bare_launch(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    calls = []

    def fake(argv, *a):  # pragma: no cover -- must not be reached
        calls.append(list(argv))
        raise AssertionError("no gh call may be made without a batch")

    with pytest.raises(TypeError):
        d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)
    with pytest.raises(d.DispatchRefused):
        d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="")
    assert calls == []


def test_the_leak_check_flags_a_credential_byte_in_a_harvested_file(tmp_path):
    """NEGATIVE CONTROL, may already be GREEN on arrival: the leak check must flag a harvested
    `run.log` that holds the (fake) codex cache bytes -- proof the clean-flow test is not vacuous."""
    cfg = _cfg(tmp_path)
    codex_bytes = (cfg.home / ".codex" / "auth.json").read_bytes()
    result = _fin_exec(tmp_path, _FinishGh(), cfg)
    assert result.ok, result.failure
    remote = {"run.log": codex_bytes.decode("utf-8") + "\n", "receipt.json": "{}\n"}
    harvested = d.codespace_harvest(result.name, batch=_FIN_BATCH, lane="lane-x", out_root=tmp_path / "rr",
                                    invoker=_ssh_cat_fake(remote))
    assert harvested.ok, harvested.failure
    texts = {rel: (harvested.out_dir / rel).read_text(encoding="utf-8") for rel in harvested.files}
    flagged = {rel for rel, text in texts.items() if d.leak_check({"codex": codex_bytes}, [text])}
    assert flagged == {"run.log"}, "the finding names the harvested file that carries the bytes"
    assert d.leak_check({"codex": codex_bytes}, list(texts.values())) == ["codex"]


_TRACKED_LEDGER = Path(d.__file__).resolve().parents[1] / "logs" / "CODESPACE-RECEIPTS.jsonl"


def test_the_codespace_suites_never_write_the_tracked_ledger_or_the_home_receipts(tmp_path):
    """A representative exec that names NO receipt seam (the shape of the old callers) must leave the
    tracked regime ledger and `~/.claude/remote-runs/B1` exactly as they were."""
    home_b1 = Path.home() / ".claude" / "remote-runs" / "B1"

    def state():
        ledger = _TRACKED_LEDGER.read_bytes() if _TRACKED_LEDGER.is_file() else None
        home = sorted((str(p), p.stat().st_mtime_ns) for p in home_b1.rglob("*")) if home_b1.exists() else []
        return ledger, home

    before = state()
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=_FakeGh(
        receipt_written=copy.deepcopy(_GOOD_RECEIPT)), batch="B1")
    assert result.ok, result.failure
    assert result.steps, "the exec did write its step rows -- to the private test home"
    assert state() == before


# =====================================================================================================
# [#1537] codespace-finish -- RED-first witnesses (phase 2). None of it exists on the base: every test
# below fails on `dccc2c03` for the named missing seam, constant or behaviour. The spec ids (R2a ...
# R7i) are in each docstring. Every credential here is a fake sentinel; nothing calls a real gh/claude/agy.
# =====================================================================================================

_CLAUDE_HEAD = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", "claude-sonnet-5",
                "--effort", "low", "--permission-mode", "bypassPermissions", "--json-schema",
                '{"type":"object","title":"LaneReport"}', "do the lane"]


def _seam_exec(base: Path, fake, *, head=None, branch: str = "worktree-lane-x", **kw):
    """One direct `codespace_exec` with a claude head that carries a `--json-schema` token; `kw` carries
    the new seams (`schema_smoke`, `pins`, `agy_wait_s`, `clock`, `sleep`)."""
    contract = base / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    return d.codespace_exec("me/repo", branch, "lane-x", contract, list(head or _CLAUDE_HEAD),
                            invoker=fake, mirror=_cfg(base), batch=_FIN_BATCH,
                            receipts_root=base / "rr", ledger_path=base / "ledger.jsonl", **kw)


def _ok_smoke(seen: list | None = None):
    def smoke(argv):
        if seen is not None:
            seen.append(list(argv))
        return d.SmokeResult(ok=True, exit_code=0, detail="")
    return smoke


# ----- (2) the live schema smoke ---------------------------------------------------------------------

def test_a_failing_schema_smoke_refuses_before_any_gh_call(tmp_path):
    """R2a: a smoke that fails refuses with a schema-smoke fate and a failed step row, and no gh call is made."""
    seen: list[list[str]] = []

    def smoke(argv):
        seen.append(list(argv))
        return d.SmokeResult(ok=False, exit_code=1, detail="API Error: allOf is not permitted at the top level")

    fake = _FinishGh()
    result = _seam_exec(tmp_path, fake, schema_smoke=smoke)
    assert len(seen) == 1, "the smoke ran once"
    assert not result.ok and fake.calls == [], "no gh call: no box exists"
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "schema-smoke"
    assert "schema smoke" in result.failure and "allOf is not permitted" in result.failure
    row = _row(tmp_path, "schema-smoke")
    assert row["ok"] is False and row["codespace"] == ""
    assert [r["step"] for r in _rows(tmp_path)] == ["schema-smoke"], "nothing else was attempted"


def test_a_passing_schema_smoke_runs_once_with_the_exact_token_then_creates(tmp_path):
    """R2b: the smoke gets the very --json-schema token of the head, runs before `create`, and records an ok row."""
    seen: list[list[str]] = []
    calls_at_smoke: list[int] = []
    fake = _FinishGh()

    def smoke(argv):
        calls_at_smoke.append(len(fake.calls))
        return _ok_smoke(seen)(argv)

    result = _seam_exec(tmp_path, fake, schema_smoke=smoke)
    assert result.ok, result.failure
    assert len(seen) == 1 and calls_at_smoke == [0], "once, and before the first gh call"
    token = _CLAUDE_HEAD[_CLAUDE_HEAD.index("--json-schema") + 1]
    assert seen[0][seen[0].index("--json-schema") + 1] == token, "the exact token the lane will get"
    assert seen[0] == d.schema_smoke_argv(_CLAUDE_HEAD)
    assert fake.calls[0][:2] == ["codespace", "create"]
    row = _row(tmp_path, "schema-smoke")
    assert row["ok"] is True and row["evidence"]["exit_code"] == 0
    steps = [r["step"] for r in _rows(tmp_path)]
    assert steps.index("schema-smoke") < steps.index("create")


def test_schema_smoke_argv_is_none_for_a_non_claude_or_schemaless_head():
    """R2c: only a claude head that carries --json-schema is smoked; the argv is the fixed low-effort shape."""
    assert d.schema_smoke_argv(["codex", "exec", "--json", "--json-schema", "{}", "p"]) is None
    assert d.schema_smoke_argv(["claude", "-p", "--model", "opus", "prompt"]) is None
    assert d.schema_smoke_argv(["copilot", "-p", "prompt"]) is None
    argv = d.schema_smoke_argv(_CLAUDE_HEAD)
    assert argv[:9] == ["claude", "-p", "--output-format", "json", "--model", "claude-sonnet-5",
                        "--effort", "low", "--json-schema"]
    assert argv[9] == _CLAUDE_HEAD[_CLAUDE_HEAD.index("--json-schema") + 1] and len(argv) == 11
    assert "FAILED" in argv[10] and "schema smoke" in argv[10], "a fixed prompt asking for a minimal FAILED report"
    assert argv == d.schema_smoke_argv(_CLAUDE_HEAD), "deterministic"
    real = d.build_plan("anthropic", "opus", "lane-x", "high", "p", streamed=True).argv
    assert d.schema_smoke_argv(real)[5] == "opus", "a real planned head is smoked with its own model"


def test_the_cli_verb_wires_the_real_smoke_and_pin_gate(tmp_path, monkeypatch):
    """R2d: `codespace-exec` hands codespace_exec the real schema smoke and a pin gate."""
    from click.testing import CliRunner

    seen: dict = {}

    def fake_exec(*a, **kw):
        seen.update(kw)
        return d.ExecResult(True, name="n")

    monkeypatch.setattr(d, "codespace_exec", fake_exec)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    res = CliRunner().invoke(d.cli, ["codespace-exec", str(contract), "--repo", "o/r", "--slug", "x",
                                     "--argv-json", '["claude"]', "--batch", "E9.1"])
    assert res.exit_code == 0, res.output
    assert seen.get("schema_smoke") is d.run_schema_smoke
    assert seen.get("pins") is not None and callable(seen["pins"])


# ----- (4) the pin is written immediately before creation ----------------------------------------------

_STALE_FINDING = "the laptop prints claude 2.1.295 but the record says '2.1.290' (run `pin write`)"


def test_stale_pins_on_the_branch_refuse_before_create(tmp_path):
    """R4a: a pin check that finds drift refuses WAITING at the pins step with one OPERATOR-ACTION and no gh call."""
    asked: list[str] = []

    def pins(branch):
        asked.append(branch)
        return 1, [_STALE_FINDING]

    fake = _FinishGh()
    result = _seam_exec(tmp_path, fake, pins=pins, branch="worktree-lane-x")
    assert asked == ["worktree-lane-x"], "the pin check is handed the BRANCH name"
    assert not result.ok and fake.calls == []
    assert result.fate["fate"] == "WAITING" and result.fate["step"] == "pins"
    assert _STALE_FINDING in result.failure
    action = ("OPERATOR-ACTION: run `uv run --locked python scripts/codespace_parity.py pin write`, "
              "commit it to worktree-lane-x and push, then launch again")
    assert result.failure.splitlines().count(action) == 1 and result.failure.count("OPERATOR-ACTION:") == 1
    row = _row(tmp_path, "pins")
    assert row["ok"] is False and row["codespace"] == ""


def test_clean_pins_let_create_run_and_record_a_pins_row(tmp_path):
    """R4b: a clean pin check lets the launch go on and leaves an ok `pins` row before the `create` row."""
    fake = _FinishGh()
    result = _seam_exec(tmp_path, fake, pins=lambda branch: (0, []))
    assert result.ok, result.failure
    assert _row(tmp_path, "pins")["ok"] is True
    steps = [r["step"] for r in _rows(tmp_path)]
    assert steps.index("pins") < steps.index("create")
    assert fake.calls[0][:2] == ["codespace", "create"]


def test_the_pin_check_runs_after_the_smoke_and_not_at_all_when_the_smoke_fails(tmp_path):
    """R2b/R4a: the order is smoke, then pins, then create -- a failed smoke never reaches the pin check."""
    asked: list[str] = []
    bad = d.SmokeResult(ok=False, exit_code=1, detail="rejected")
    result = _seam_exec(_sub(tmp_path, "bad"), _FinishGh(), schema_smoke=lambda argv: bad,
                        pins=lambda branch: asked.append(branch) or (0, []))
    assert not result.ok and asked == []
    order: list[str] = []
    fake = _FinishGh()
    good = _seam_exec(_sub(tmp_path, "good"), fake,
                      schema_smoke=lambda argv: order.append("smoke") or d.SmokeResult(True, 0, ""),
                      pins=lambda branch: order.append("pins") or (0, []))
    assert good.ok, good.failure
    assert order == ["smoke", "pins"]


_PINS_TEXT = ('schema: 1\ntools:\n  claude:\n    version: "2.1.290"\n    method: native\n'
              '  gh:\n    version: "2.93.0"\n    method: prebuilt\n')


def _recorded_pins(base: Path, name: str, laptop: dict) -> Path:
    path = base / name
    path.write_text(_PINS_TEXT, encoding="utf-8", newline="\n")
    d.cpar.pin_write(path, laptop)
    return path


class _GitRun:
    """The `run` seam of `branch_pin_check`: records every argv, answers `git show` with a fixed file."""

    def __init__(self, shown: str):
        self.shown = shown
        self.calls: list[str] = []

    def __call__(self, argv, **_kw):
        joined = " ".join(argv)
        self.calls.append(joined)
        return d.cpar.CmdResult(0, self.shown if " show " in f" {joined} " else "", "")


def test_branch_pin_check_reads_the_branchs_file_not_the_worktrees(tmp_path, monkeypatch):
    """R4c: it fetches the branch and reads provisioning.yaml at FETCH_HEAD -- never the checked-out copy."""
    old = {"claude": "2.1.290", "gh": "2.93.0"}
    new = {"claude": "2.1.295", "gh": "2.93.0"}
    branch_text = _recorded_pins(tmp_path, "branch.yaml", old).read_text(encoding="utf-8")
    worktree_file = _recorded_pins(tmp_path, "worktree.yaml", new)
    monkeypatch.setattr(d.cpar, "PROVISIONING_PATH", worktree_file, raising=False)

    run = _GitRun(branch_text)
    code, lines = d.branch_pin_check("worktree-lane-x", run=run, laptop=new)
    assert code == 1 and any("claude" in ln for ln in lines), "the branch's record is behind the laptop"
    joined = "\n".join(run.calls)
    assert "fetch origin worktree-lane-x" in joined
    assert "show FETCH_HEAD:.devcontainer/provisioning.yaml" in joined
    fetch = next(i for i, c in enumerate(run.calls) if "fetch origin worktree-lane-x" in c)
    show = next(i for i, c in enumerate(run.calls) if "show FETCH_HEAD:" in c)
    assert fetch < show, "fetched before it is read"
    assert d.branch_pin_check("worktree-lane-x", run=_GitRun(branch_text), laptop=old) == (0, [])


# ----- (6) hardening ------------------------------------------------------------------------------------

def test_an_empty_batch_is_a_clean_dispatch_refusal(tmp_path):
    """R6a: an empty batch is a click refusal naming the batch, not a bare ValueError, and no gh call is made."""
    import click

    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh()
    with pytest.raises(d.DispatchRefused) as info:
        d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake, batch="")
    assert isinstance(info.value, click.ClickException) and "batch" in info.value.message
    assert fake.calls == []


def test_the_codex_auth_json_fallback_is_removed_by_the_exit_trap(tmp_path):
    """R6b: the runner's one EXIT trap also removes the CODEX_AUTH_JSON fallback file (text-level, then real bash)."""
    body = d._codespace_runner_script("/w", "/c", ["true"])
    traps = [ln for ln in body.splitlines() if re.match(r"\s*trap\b.*\bEXIT\b", ln)]
    assert len(traps) == 1, "one EXIT trap, present even when nothing was mirrored"
    assert ".codex/auth.json" in traps[0] and "fallback" in traps[0], "removed only when the fallback wrote it"
    # the behaviour, on a real bash: the fallback writes the file, the run ends, the file is gone
    _bash_or_skip()
    _origin, checkout = _git_lane(tmp_path)
    work = _sub(tmp_path, "work")
    marker = tmp_path / "fallback-seen.txt"
    head = _head_stub(tmp_path, f'if [ -f "$HOME/.codex/auth.json" ]; then echo present > "{marker.as_posix()}"; fi\n')
    env = {**_lane_env(tmp_path), "CODEX_AUTH_JSON": "FAKE-CODEX-AUTH-JSON-NOT-A-CREDENTIAL"}
    _run_runner(tmp_path, d._codespace_runner_script(work.as_posix(), checkout.as_posix(), head), work, env)
    assert marker.is_file(), "the fallback really wrote $HOME/.codex/auth.json during the run"
    assert not (Path(env["HOME"]) / ".codex" / "auth.json").exists(), "and the EXIT trap removed it"


def test_branch_context_git_env_allows_bare_repos_even_when_the_host_forbids_them(tmp_path, monkeypatch):
    """R6c: `branch_context.git_env()` appends safe.bareRepository=all after any inherited GIT_CONFIG entry."""
    import branch_context

    if shutil.which("git") is None:
        pytest.skip("no git on PATH")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "safe.bareRepository")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "explicit")
    hardened = branch_context.git_env()
    assert hardened["GIT_CONFIG_COUNT"] == "2"
    assert hardened["GIT_CONFIG_KEY_0"] == "safe.bareRepository" and hardened["GIT_CONFIG_VALUE_0"] == "explicit"
    assert hardened["GIT_CONFIG_KEY_1"] == "safe.bareRepository" and hardened["GIT_CONFIG_VALUE_1"] == "all"
    bare = tmp_path / "bare.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, env={**os.environ, **_GIT_BARE_OK})
    probe = ["git", "-C", str(bare), "rev-parse", "--is-bare-repository"]
    control = subprocess.run(probe, capture_output=True, text=True, env=dict(os.environ))
    if control.returncode == 0:
        pytest.skip("this git does not enforce safe.bareRepository=explicit: the control did not bite")
    done = subprocess.run(probe, capture_output=True, text=True, env={**os.environ, **hardened})
    assert done.returncode == 0 and done.stdout.strip() == "true", done.stderr
    # the module's own git helpers carry it too
    assert branch_context._git(bare, "rev-parse", "--is-bare-repository") == "true"
    assert branch_context._git_out(bare, "rev-parse", "--is-bare-repository") == "true"
    monkeypatch.delenv("GIT_CONFIG_COUNT")
    assert branch_context.git_env()["GIT_CONFIG_COUNT"] == "1"


# ----- (7) agy sign-in by an operator link --------------------------------------------------------------

def _channel(base: Path) -> Path:
    """The laptop file the operator puts the browser's code in: next to the lane's steps.jsonl."""
    return _steps_path(base).parent / "agy-code.txt"


def _operator_writes(clock: FakeClock, channel: Path, at_s: float, text: str) -> None:
    def write():
        channel.parent.mkdir(parents=True, exist_ok=True)
        channel.write_text(text, encoding="utf-8")
    clock.at(at_s, write)


def _agy_exec(base: Path, agy: FakeAgy, *, wait: float = 600, clock: FakeClock | None = None):
    """A launch with the agy wait on the fake clock; returns (gh fake, result, clock)."""
    clock = clock or FakeClock()
    fake = _FinishGh(agy=agy)
    result = _fin_exec(base, fake, agy_wait_s=wait, clock=clock.now, sleep=clock.sleep)
    return fake, result, clock


def _agy_record(result) -> dict:
    return next(i for i in result.mirror if i["cli"] == "agy")


def _gap_line(signin: str) -> str:
    return f"GAP: agy sign-in {signin}: the auth process tree was killed; reads go through copilot"


def test_the_operator_action_line_names_the_url_and_the_channel_in_stderr_and_the_receipt(tmp_path, capsys):
    """R7a: one OPERATOR-ACTION line (URL, then the channel file) goes to stderr and into the credentials row."""
    result = _fin_exec(tmp_path, _FinishGh())
    assert result.ok, result.failure
    prefix = f"OPERATOR-ACTION: agy sign-in: open {_AGY_URL}, then put the browser's code in "
    lines = [ln for ln in capsys.readouterr().err.splitlines() if ln.startswith("OPERATOR-ACTION: agy sign-in:")]
    assert len(lines) == 1 and lines[0].startswith(prefix), lines
    assert Path(lines[0][len(prefix):]).parts[-3:] == (_FIN_BATCH, "lane-x", "agy-code.txt")
    row = _row(tmp_path, "credentials")
    recorded = next(c for c in row["evidence"]["clis"] if c["cli"] == "agy")
    assert recorded["operator_action_line"] == lines[0], "the receipt holds the same line"
    assert _agy_record(result)["operator_action_line"] == lines[0]


def test_the_code_written_to_the_channel_is_relayed_on_stdin_only_and_the_channel_is_removed(tmp_path):
    """R7b: a stale channel file is cleared, an empty one is waited out, the code goes on stdin, the file is deleted."""
    channel = _channel(tmp_path)
    channel.parent.mkdir(parents=True)
    channel.write_text("STALE-CODE-FROM-A-PRIOR-RUN\n", encoding="utf-8")
    clock = FakeClock()
    _operator_writes(clock, channel, 10, "")                 # a half-created file is not a code
    _operator_writes(clock, channel, 20, FAKE_CODE + "\n")
    agy = FakeAgy()
    fake, result, _clock = _agy_exec(tmp_path, agy, clock=clock)
    assert result.ok, result.failure
    assert [b.decode().strip() for b in agy.code_stdin] == [FAKE_CODE], "only the operator's code, once"
    relay = [(a, b) for a, b in fake.stdin if "agy-signin-code" in a]
    assert len(relay) == 1 and relay[0][1].decode().strip() == FAKE_CODE
    assert relay[0][0][-1] == "agy-signin-code", "no positional carries the code"
    assert FAKE_CODE not in " ".join(" ".join(c) for c in fake.calls)
    assert not channel.exists(), "the code file is deleted once read"


def test_a_signed_in_agy_answers_the_nonce_probe_and_the_record_says_signed_in(tmp_path):
    """R7c: after the relay a fresh nonce is probed; the nonce echoed back means signed-in; a wrong code is probe-failed."""
    clock = FakeClock()
    _operator_writes(clock, _channel(tmp_path), 30, FAKE_CODE + "\n")
    agy = FakeAgy()
    fake, result, _clock = _agy_exec(tmp_path, agy, clock=clock)
    assert result.ok, result.failure
    record = _agy_record(result)
    assert record["signin"] == "signed-in" and record["probe_ok"] is True
    assert re.fullmatch(r"[0-9a-f]{16}", record["probe_nonce"]), "secrets.token_hex(8)"
    assert agy.probes == [record["probe_nonce"]]
    assert agy.verbs[:3] == ["agy-signin-start", "agy-signin-code", "agy-probe"]
    probe_calls = [c for c in fake.calls if "agy-probe" in c]
    assert probe_calls[0][-2:] == ["agy-probe", record["probe_nonce"]]
    # the twin: a code agy does not accept gives no nonce back -> probe-failed, the tree is killed, reads go to copilot
    twin = _sub(tmp_path, "twin")
    wrong_clock = FakeClock()
    _operator_writes(wrong_clock, _channel(twin), 30, "NOT-THE-CODE-0000\n")
    wrong = FakeAgy()
    _fake2, wrong_result, _c2 = _agy_exec(twin, wrong, clock=wrong_clock)
    assert wrong_result.ok, wrong_result.failure
    bad = _agy_record(wrong_result)
    assert bad["signin"] == "probe-failed" and bad["probe_ok"] is False
    assert wrong.stopped == 1 and bad["auth_tree_killed"] is True and bad["read_route"] == "copilot"
    assert bad["action"] == "gap"


def test_the_wait_prints_a_heartbeat_every_60s_of_clock_time(tmp_path, capsys):
    """R7d: while it waits the launcher prints one heartbeat per 60 s of clock time and counts them in the record."""
    clock = FakeClock()
    _operator_writes(clock, _channel(tmp_path), 130, FAKE_CODE + "\n")
    _fake, result, _clock = _agy_exec(tmp_path, FakeAgy(), clock=clock)
    assert result.ok, result.failure
    err = capsys.readouterr().err
    beats = re.findall(r"\[codespace fluffy-space-1\] agy sign-in: waiting for the code in \S.*? "
                       r"\((\d+)(?:\.0)?s of 600(?:\.0)?s\)", err)
    assert len(beats) == 2, err
    assert 60 <= int(beats[0]) <= 64 and 120 <= int(beats[1]) <= 124
    assert _agy_record(result)["heartbeats"] == 2
    assert all(s <= 2 for s in clock.sleeps), "it polls every AGY_POLL_S, never one long sleep"


def test_no_code_within_600s_is_a_gap_the_tree_is_killed_and_reads_go_through_copilot(tmp_path, capsys):
    """R7e: no code in the window -> GAP, the auth tree is stopped, reads route via copilot, the launch goes on."""
    agy = FakeAgy()
    _fake, result, clock = _agy_exec(tmp_path, agy)
    assert result.ok, result.failure
    assert clock.start + 600 <= clock.t <= clock.start + 600 + d.AGY_POLL_S, "waited the window, not a poll more"
    record = _agy_record(result)
    assert record["signin"] == "timeout" and record["read_route"] == "copilot"
    assert record["auth_tree_killed"] is True and agy.stopped == 1
    assert record["action"] == "gap" and record["gap"] == "agy-interactive-sign-in"
    assert 9 <= record["heartbeats"] <= 10
    assert agy.code_stdin == [] and agy.probes == []
    assert _gap_line("timeout") in capsys.readouterr().err.splitlines()


def test_the_code_never_reaches_an_argv_a_row_the_result_or_stderr(tmp_path, capsys):
    """R7f: the code is on agy's stdin and nowhere else -- and a box that echoes it back is a credential leak."""
    clock = FakeClock()
    _operator_writes(clock, _channel(tmp_path), 20, FAKE_CODE + "\n")
    agy = FakeAgy()
    fake, result, _clock = _agy_exec(tmp_path, agy, clock=clock)
    assert result.ok, result.failure
    assert [b.decode().strip() for b in agy.code_stdin] == [FAKE_CODE], "no vacuous pass: it was relayed"
    seen = capsys.readouterr()
    everything = "\n".join([*(" ".join(c) for c in fake.calls), *result.commands, json.dumps(_asdict(result)),
                            _steps_path(tmp_path).read_text(encoding="utf-8"),
                            (tmp_path / "ledger.jsonl").read_text(encoding="utf-8"), seen.out, seen.err])
    assert FAKE_CODE not in everything
    # the leak check covers it: a box that answers with the code it was handed is refused
    leaky = _sub(tmp_path, "leaky")
    leak_clock = FakeClock()
    _operator_writes(leak_clock, _channel(leaky), 20, FAKE_CODE + "\n")
    _fake2, refused, _c2 = _agy_exec(leaky, FakeAgy(echo_code=True), clock=leak_clock)
    assert not refused.ok and "credential leak" in refused.failure and "agy" in refused.failure
    assert FAKE_CODE not in refused.failure + _steps_path(leaky).read_text(encoding="utf-8")


def test_no_url_runs_the_diag_and_records_it_then_stops_the_tree(tmp_path, capsys):
    """R7g: an agy that prints no URL: its sanitized diag is recorded, the tree is stopped, no wait is spent."""
    agy = FakeAgy(url=None)
    _fake, result, clock = _agy_exec(tmp_path, agy)
    assert result.ok, result.failure
    record = _agy_record(result)
    assert record["signin"] == "no-url" and record["auth_url_surfaced"] is False
    assert record["signin_diag"] == list(agy.diag_lines) and all(isinstance(x, str) for x in record["signin_diag"])
    assert agy.diag_calls == 1 and agy.stopped == 1
    assert agy.verbs.index("agy-signin-diag") < agy.verbs.index("agy-signin-stop"), "read the evidence, then kill"
    assert record["read_route"] == "copilot" and record["auth_tree_killed"] is True
    assert clock.sleeps == [] and clock.t == clock.start, "there is nothing to wait for"
    err = capsys.readouterr().err
    assert _gap_line("no-url") in err.splitlines() and "OPERATOR-ACTION: agy sign-in:" not in err
    assert _agy_record(result)["signin_diag"] == next(
        c for c in _row(tmp_path, "credentials")["evidence"]["clis"] if c["cli"] == "agy")["signin_diag"]


def _helper_branch(script: str, verb: str) -> str:
    """The text of one top-level `case` arm of the credential helper (up to the next arm)."""
    start = script.index(f"  {verb})")
    nxt = re.search(r"\n  [a-z][a-z-]*\)", script[start + 1:])
    return script[start:start + 1 + nxt.start()] if nxt else script[start:]


def test_the_helper_starts_agy_without_browser_in_a_sized_pty_and_can_stop_and_diag_it():
    """R7h: text-level -- start unsets BROWSER, sizes the pty and keeps two pids; stop, diag and probe exist."""
    script = d._credential_tools_script([])
    start = _helper_branch(script, "agy-signin-start")
    assert "env -u BROWSER" in start
    pty = start[re.search(r"script -\w+", start).start():]
    assert "stty cols 500 rows 50" in pty and pty.index("stty cols 500 rows 50") < pty.index("agy"), "sized before agy"
    assert "$box/pid" in start and "$box/holder" in start, "the setsid leader and the FIFO holder are kept"
    assert re.search(r"\\x1b|\\033|\\e\[|\\x1B", start), "the URL is read from ANSI-stripped output"
    assert re.search(r"\b90\b", start), "it waits up to 90 s for the URL"
    stop = _helper_branch(script, "agy-signin-stop")
    assert "TERM" in stop and "KILL" in stop and "holder" in stop and "rm -rf" in stop
    assert re.search(r'kill[^\n]*\s-"?\$', stop), "the whole process GROUP (-<pid>) is signalled"
    diag = _helper_branch(script, "agy-signin-diag")
    for name in ("SSH_CONNECTION", "SSH_TTY", "BROWSER", "DISPLAY", "DBUS_SESSION_BUS_ADDRESS"):
        assert name in diag
    assert "out_bytes=" in diag and "<url>" in diag and re.search(r"tail\s+(-n\s*)?-?30", diag)
    probe = _helper_branch(script, "agy-probe")
    assert "{8,64}" in probe and "64" in probe and "timeout 300 agy -p" in probe and "/dev/null" in probe


def test_the_helper_selects_google_oauth_once_when_agy_shows_the_login_menu():
    """RG1: text-level -- start sees `Select login method` and writes ONE carriage return to the FIFO, flag-guarded."""
    start = _helper_branch(d._credential_tools_script([]), "agy-signin-start")
    assert "Select login method" in start, "the helper must recognise agy's login menu"
    writes = list(re.finditer(r"[^\n]*\b(?:printf|echo)\b[^\n]*>\s*\"\$box/in\"", start))  # `sleep 900 >` is the holder
    assert len(writes) == 1, "exactly one write into the FIFO: nothing else is ever typed"
    line = writes[0].group(0)
    assert re.search(r"\\r|\\015|\\x0d", line), f"the write is a carriage return: {line!r}"
    assert not re.search(r"\b2\b|\\n", line), "never option 2, never a newline-terminated line"
    assert start.index("Select login method") < writes[0].end(), "the write is conditioned on the menu check"
    flags = set(re.findall(r"\b([A-Za-z_]\w*)=\"?(?:1|yes|y|true)\"?(?=\s|;|$)", start))
    before = start[:writes[0].end()]
    tested = {f for f in flags if re.search(rf"\$\{{?{f}\b", before)}
    assert tested, f"a once-only flag variable is tested before the write (flags seen: {sorted(flags)})"
    after = start[start.index("Select login method"):]
    assert any(re.search(rf"\b{f}=\"?(?:1|yes|y|true)\"?", after) for f in tested), \
        "the flag is set once the menu is answered, so it cannot fire twice"


def test_agy_signin_start_against_a_fake_agy_with_a_login_menu_prints_the_url(tmp_path):
    """RG2: the real helper on Linux, a fake agy that waits at the menu, prints the URL after one Enter; stop kills it."""
    missing = [tool for tool in ("bash", "script", "setsid", "mkfifo") if shutil.which(tool) is None]
    if missing:
        pytest.skip(f"needs {', '.join(missing)} on PATH (ADR-127: skipped with its reason, not passed)")
    helper = tmp_path / "credential-tools.sh"
    helper.write_text(d._credential_tools_script([]), encoding="utf-8", newline="\n")
    pidfile = tmp_path / "fake-agy.pid"
    fake = Path(__file__).resolve().parent / "fake_agy.py"
    bindir = tmp_path / "bin"
    bindir.mkdir()
    wrapper = bindir / "agy"
    wrapper.write_text(f"#!/usr/bin/env bash\nexec {shlex.quote(sys.executable)} {shlex.quote(fake.as_posix())} "
                       f"menu {shlex.quote(pidfile.as_posix())}\n", encoding="utf-8", newline="\n")
    wrapper.chmod(0o755)
    env = {**os.environ, "HOME": str(tmp_path), "PATH": f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}"}
    env.pop("BROWSER", None)
    pid = 0
    started = subprocess.run(["bash", helper.as_posix(), "agy-signin-start"], env=env, capture_output=True,
                             text=True, timeout=120, stdin=subprocess.DEVNULL)
    try:
        assert started.returncode == 0, (started.returncode, started.stdout, started.stderr)
        assert started.stdout.strip() == "https://agy.invalid/oauth?state=fake-not-real", started.stdout
        pid = int(pidfile.read_text(encoding="utf-8").strip())
        os.kill(pid, 0)                                   # alive until stop
    finally:
        stopped = subprocess.run(["bash", helper.as_posix(), "agy-signin-stop"], env=env, capture_output=True,
                                 text=True, timeout=60, stdin=subprocess.DEVNULL)
    assert stopped.returncode == 0, stopped.stderr
    gone = False
    for _ in range(50):
        try:
            os.kill(pid, 0)
            stat = Path(f"/proc/{pid}/stat")
            if stat.exists() and stat.read_text(encoding="utf-8").rsplit(")", 1)[-1].split()[0] == "Z":
                gone = True                               # killed, only awaiting a reaper
                break
        except ProcessLookupError:
            gone = True
            break
        time.sleep(0.1)
    assert gone, "the fake agy outlived agy-signin-stop"


def test_every_background_process_of_agy_signin_start_is_detached_from_the_callers_pipes():
    """RG3: text-level -- each `... &` line of start redirects stdin, stdout AND stderr, so a caller that captures
    output (subprocess, `gh codespace ssh`) sees EOF at once; RG2 hung 120 s on Linux CI on the FIFO holder."""
    start = _helper_branch(d._credential_tools_script([]), "agy-signin-start")
    background = [ln.strip() for ln in start.splitlines() if re.search(r"(?<!&)&\s*$", ln)]
    assert len(background) >= 2, f"the FIFO holder and the script/agy leader are both backgrounded: {background}"
    for line in background:
        out = re.search(r"(?:^|\s)1?>>?\s*[^\s&]|&>", line)
        assert out, f"stdout is inherited from the caller: {line!r}"
        err = re.search(r"2>>?\s*[^\s&]|&>", line) or (re.search(r"2>&1", line) and out.start() < line.index("2>&1"))
        assert err, f"stderr is inherited from the caller: {line!r}"
        assert re.search(r"(?:^|\s)0?<\s*[^\s<(]", line), f"stdin is inherited from the caller: {line!r}"


@pytest.mark.parametrize("nonce", ["short", "has space in it!", "x" * 65, "abcdefgh;touch-x"])
def test_the_probe_helper_refuses_a_nonce_that_is_not_8_to_64_alphanumerics(tmp_path, nonce):
    """R7h: the real helper, run on bash, exits 64 for a bad nonce (and not as an unknown subcommand)."""
    bash = _bash_or_skip()
    helper = tmp_path / "credential-tools.sh"
    helper.write_text(d._credential_tools_script([]), encoding="utf-8", newline="\n")
    done = subprocess.run([bash, helper.as_posix(), "agy-probe", nonce], capture_output=True, text=True,
                          timeout=60, stdin=subprocess.DEVNULL)
    assert done.returncode == 64 and "unknown subcommand" not in done.stderr, done.stderr


def test_the_cli_verb_waits_600s_by_default_and_refuses_more(tmp_path, monkeypatch):
    """R7i: `codespace-exec` passes AGY_SIGNIN_WAIT_S (600) by default, honours --agy-signin-wait-s, refuses > 600."""
    from click.testing import CliRunner

    assert (d.AGY_SIGNIN_WAIT_S, d.AGY_HEARTBEAT_S, d.AGY_POLL_S, d.AGY_READ_FALLBACK) == (600, 60, 2, "copilot")
    seen: list[dict] = []

    def fake_exec(*a, **kw):
        seen.append(dict(kw))
        return d.ExecResult(True, name="n")

    monkeypatch.setattr(d, "codespace_exec", fake_exec)
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    base = ["codespace-exec", str(contract), "--repo", "o/r", "--slug", "x", "--argv-json", '["claude"]',
            "--batch", "E9.1"]
    default = CliRunner().invoke(d.cli, base)
    assert default.exit_code == 0, default.output
    assert seen[-1]["agy_wait_s"] == 600
    shorter = CliRunner().invoke(d.cli, [*base, "--agy-signin-wait-s", "120"])
    assert shorter.exit_code == 0, shorter.output
    assert seen[-1]["agy_wait_s"] == 120
    count = len(seen)
    too_long = CliRunner().invoke(d.cli, [*base, "--agy-signin-wait-s", "601"])
    assert too_long.exit_code != 0 and "600" in too_long.output, too_long.output
    assert len(seen) == count, "a refused wait launches nothing"


# ----- judge round 2: F1-F5 RED witnesses ----------------------------------------------------------------

def _unlink_fails_for(monkeypatch, victim: Path) -> None:
    """Make `Path.unlink` raise OSError for `victim` only; every other path unlinks as usual."""
    real = Path.unlink

    def unlink(self, missing_ok=False):
        if self == victim:
            raise PermissionError(13, "the channel is held open by another process")
        return real(self, missing_ok=missing_ok)
    monkeypatch.setattr(Path, "unlink", unlink)


def test_an_unremovable_stale_channel_refuses_the_signin_without_starting_agy(tmp_path, monkeypatch):
    """F1a: a stale channel that cannot be removed is never read as the code -- channel-unusable, no agy start."""
    channel = _channel(tmp_path)
    channel.parent.mkdir(parents=True)
    channel.write_text("STALE-CODE-FROM-A-PRIOR-RUN\n", encoding="utf-8")
    _unlink_fails_for(monkeypatch, channel)
    agy = FakeAgy()
    fake, result, _clock = _agy_exec(tmp_path, agy)
    assert result.ok, result.failure
    assert agy.started == 0 and "agy-signin-start" not in agy.verbs, "agy is never started on a poisoned channel"
    record = _agy_record(result)
    assert record["signin"] == "channel-unusable"
    assert agy.stopped == 1 and record["auth_tree_killed"] is True
    assert record["action"] == "gap" and record["read_route"] == "copilot"
    sent = b"".join(data or b"" for _argv, data in fake.stdin)
    assert b"STALE-CODE" not in sent and agy.code_stdin == [], "the stale content reached no gh call's stdin"


def test_the_channel_is_removed_on_every_exit_of_the_agy_leg(tmp_path, monkeypatch):
    """F1b: a file the wait never consumed is removed at exit; a failed removal of a read code is recorded."""
    # (i) timeout: an empty (half-created) file lands after the last poll of the window and is never a code
    clock = FakeClock()
    channel = _channel(tmp_path)
    _operator_writes(clock, channel, 599, "")
    _fake, result, _c = _agy_exec(tmp_path, FakeAgy(), clock=clock)
    assert result.ok, result.failure
    assert _agy_record(result)["signin"] == "timeout"
    assert not channel.exists(), "the leg removes the channel on its way out, whatever the exit"
    # (ii) a code that was read but could not be deleted: the record says so
    stuck = _sub(tmp_path, "stuck")
    stuck_channel = _channel(stuck)
    stuck_clock = FakeClock()
    _operator_writes(stuck_clock, stuck_channel, 20, FAKE_CODE + "\n")
    with monkeypatch.context() as scope:
        _unlink_fails_for(scope, stuck_channel)
        _fake2, stuck_result, _c2 = _agy_exec(stuck, FakeAgy(), clock=stuck_clock)
    assert _agy_record(stuck_result).get("channel_removed") is False


def test_a_code_written_just_before_the_deadline_is_read_by_a_final_poll(tmp_path):
    """F2: a code that lands in the last poll interval is read at the deadline, and the wait is not extended."""
    clock = FakeClock()
    _operator_writes(clock, _channel(tmp_path), 599, FAKE_CODE + "\n")
    agy = FakeAgy()
    _fake, result, _c = _agy_exec(tmp_path, agy, wait=600, clock=clock)
    assert result.ok, result.failure
    assert _agy_record(result)["signin"] == "signed-in"
    assert [b.decode().strip() for b in agy.code_stdin] == [FAKE_CODE]
    assert clock.t <= clock.start + 600 + d.AGY_POLL_S, "the final read never extends the wait"


@pytest.mark.parametrize("flag, other", [("--json-schema", '{"type":"object","title":"Other"}'),
                                         ("--model", "claude-opus-5")])
def test_duplicate_json_schema_or_model_in_the_head_is_refused_before_any_call(tmp_path, flag, other):
    """F3: two --json-schema (or two --model) tokens are a DispatchRefused before the smoke and any gh call."""
    head = [*_CLAUDE_HEAD[:-1], flag, other, _CLAUDE_HEAD[-1]]
    assert head.count(flag) == 2
    seen: list[list[str]] = []
    fake = _FinishGh()
    with pytest.raises(d.DispatchRefused):
        _seam_exec(tmp_path, fake, head=head, schema_smoke=_ok_smoke(seen))
    assert seen == [] and fake.calls == [], "neither the smoke nor gh was reached"


def test_branch_pin_check_turns_a_pin_error_into_could_not_look(monkeypatch):
    """F4: an unreadable pin record is `(2, [reason])` -- could not look -- never an exception."""
    def broken(_path=None):
        raise d.cpar.PinError("provisioning.yaml declares no tools: block")

    monkeypatch.setattr(d.cpar, "typed_pins", broken)
    code, lines = d.branch_pin_check("worktree-lane-x", run=_GitRun(_PINS_TEXT))
    assert code == 2
    assert any("declares no tools" in ln for ln in lines), lines


def test_a_signed_in_agy_has_its_signin_tree_stopped_after_the_probe(tmp_path):
    """F5: after a good nonce probe the sign-in TUI is stopped (keyring holds the login); no copilot reroute."""
    clock = FakeClock()
    _operator_writes(clock, _channel(tmp_path), 30, FAKE_CODE + "\n")
    agy = FakeAgy()
    _fake, result, _c = _agy_exec(tmp_path, agy, clock=clock)
    assert result.ok, result.failure
    record = _agy_record(result)
    assert record["signin"] == "signed-in" and record["probe_ok"] is True
    assert "agy-signin-stop" in agy.verbs, "the sign-in TUI is stopped once signed in"
    assert agy.verbs.index("agy-signin-stop") > agy.verbs.index("agy-probe"), "stopped AFTER the probe"
    assert agy.stopped == 1 and record["auth_tree_killed"] is True
    assert record.get("read_route") != "copilot", "a signed-in agy is not rerouted"
