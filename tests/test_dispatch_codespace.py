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

import json
import re
import shlex
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import dispatch as d
cs = d.cs


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
    receipt = {"exit_code": 0, "is_error": False, "status": "success"}
    fake = _FakeGh(receipt_written=receipt)

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                              invoker=fake)

    assert result.ok, result.failure
    assert result.name == "fluffy-space-1"
    assert result.receipt == receipt
    # create (its stdout IS the name), read the creation log over ssh (item 3: a recovery
    # container is refused before anything ships), mkdir the workdir, cp contract, cp runner, ssh
    # run, cp receipt back -- no `list` call: the name is never reconstructed (codex terra P1,
    # 2026-09-27)
    verbs = [" ".join(c[:2]) for c in fake.calls]
    assert verbs == ["codespace create", "codespace ssh", "codespace ssh", "codespace cp",
                     "codespace cp", "codespace ssh", "codespace cp"]


def test_codespace_exec_refuses_on_create_failure_without_further_calls(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(fail_at="codespace create")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)

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

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)
    assert not result.ok
    assert "no name" in result.failure
    assert len(fake.calls) == 1  # nothing else was attempted without a name in hand


def test_codespace_exec_refuses_with_no_receipt_gate(tmp_path):
    """The PS verb's own doctrine: 'no receipt is a WARNING... never reporting success.'"""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(receipt_written=None)  # the cp-back call succeeds but writes nothing

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)
    assert not result.ok
    assert "no receipt" in result.failure


def test_codespace_exec_creates_the_workdir_before_shipping_anything_into_it(tmp_path):
    """Codex terra P1 (2026-09-27): `workdir` is NOT the checkout `gh codespace create` produces
    (`/workspaces/<repo-name>`) -- nothing creates it, so the first `cp` into it failed on every
    fresh codespace until this mkdir ran first."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    fake = _FakeGh(fail_at="codespace ssh mkdir")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)

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

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)

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

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude"], invoker=fake)

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
                Path(argv[-1]).write_text('{"exit_code": 0}', encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    prompt = f"Read and execute the frozen contract at {contract}"
    result = d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", prompt],
                              invoker=fake)

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
                Path(argv[-1]).write_text('{"exit_code": 0}', encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    # `plan`'s own prompt always embeds the ABSOLUTE path; the CONTRACT arg handed to exec is
    # relative, exactly as a caller typing `LANE-x.md` on the command line would produce.
    prompt = f"Read and execute the frozen contract at {absolute_contract}"
    relative_contract = Path("LANE-x.md")
    result = d.codespace_exec("me/repo", "main", "lane-x", relative_contract,
                              ["claude", "-p", prompt], invoker=fake)

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
                Path(argv[-1]).write_text('{"exit_code": 0}', encoding="utf-8")
            return d.GhResult(True, 0, "")
        if verb == "codespace ssh":
            return _ssh_reply(argv)
        raise AssertionError(f"unexpected gh call: {argv}")

    result = d.codespace_exec("me/dev-knowledge", "main", "lane-x", contract, ["claude"],
                              invoker=fake)

    assert result.ok, result.failure
    cd_line = next(ln for ln in captured["runner_body"].splitlines() if ln.startswith("cd "))
    assert "/workspaces/dev-knowledge" in cd_line
    assert "/workspaces/dispatch" not in cd_line


def test_codespace_exec_refuses_an_empty_argv_without_calling_gh(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")

    def fake(argv):  # pragma: no cover -- must not be reached
        raise AssertionError("gh must not be called with an empty argv")

    result = d.codespace_exec("me/repo", "main", "lane-x", contract, [], invoker=fake)
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
    fake = _FakeGh(receipt_written={"exit_code": 0, "is_error": False, "status": "success"})
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake)
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
                              invoker=fake)
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
                              invoker=fake, sleep=slept.append)
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
                Path(argv[-1]).write_text('{"exit_code": 0}', encoding="utf-8")
            return d.GhResult(True, 0, "")
        if "creation.log" in " ".join(argv):
            return d.GhResult(True, 0, next(answers))
        return d.GhResult(True, 0, "")

    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, sleep=lambda s: None)
    assert result.ok, result.failure


def test_a_creation_failure_without_a_recovery_line_is_refused_too(tmp_path):
    fake = _FakeGh(log="[x] postCreateCommand failed with exit code 1.\nContainer creation failed.\n")
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake, sleep=lambda s: None)
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
                              invoker=fake)
    assert not result.ok
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "run"
    assert word in result.fate["reason"]


def test_a_missing_receipt_after_a_clean_run_fails_with_a_receipt_step_fate(tmp_path):
    fake = _FakeGh(receipt_written=None)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake)
    assert not result.ok
    assert result.fate["fate"] == "FAILED" and result.fate["step"] == "receipt"


def test_a_stalled_receipt_is_a_failed_run_with_the_runners_own_fate(tmp_path):
    receipt = {"exit_code": 124, "is_error": True, "status": "hung",
               "fate": {"fate": "FAILED", "step": "run", "reason": "no progress for 901s"}}
    fake = _FakeGh(receipt_written=receipt)
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake)
    assert not result.ok
    assert result.fate == receipt["fate"]


def test_a_successful_exec_has_no_fate_failure(tmp_path):
    fake = _FakeGh(receipt_written={"exit_code": 0, "is_error": False, "status": "success"})
    result = d.codespace_exec("me/repo", "main", "lane-x", _contract(tmp_path), ["claude"],
                              invoker=fake)
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
    fake.receipt_written = {"exit_code": 0, "is_error": False, "status": "success"}
    return d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                            invoker=fake, mirror=cfg)


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
    result = _run_mirrored(tmp_path, fake, _cfg(tmp_path, home=_home(tmp_path, codex_age=7.5)))
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
    assert by["agy"].action == "waiting" and "keyring" in by["agy"].detail
    assert by["claude"].route == "secret-token" and by["claude"].action == "not-mirrored"
    assert [i.cli for i in items if i.action == "no-cli"] == ["deepseek"]


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
                                     "--argv-json", '["claude"]'])
    assert res.exit_code == 0, res.output
    assert isinstance(seen.get("mirror"), d.MirrorConfig)
