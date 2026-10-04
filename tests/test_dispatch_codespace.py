"""`scripts/dispatch.py`'s codespace exec/harvest/stop/delete legs (LANE-5B4-10).

RED-FIRST: written and first run against a tree with none of `run_gh`, `codespace_exec`,
`codespace_harvest`, `verify_harvest_manifest`, `codespace_stop` or `codespace_delete` defined
(import/attribute error) -- see the lane's session file for the RED transcript.

Every test drives these functions through the `invoker` seam (ported from `Invoke-CodespaceGh`'s
own `-Invoker`), never a real `gh` binary or a real codespace -- the same doctrine
`test_codespace_admission.py` states for its own `Probe` seam: a transport that can only be
exercised by really provisioning a machine is a transport whose guards are never tested.

R17's own test is `TestCodespaceDelete`: delete is refused when the manifest is missing or a hash
differs, and allowed when it verifies -- and in the refusal case, `gh` is never called at all.
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


import dispatch as d


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

class _FakeGh:
    """Records every argv it is called with and answers by matching on the leading verb pair,
    same shape as `_StubRunProbe` in `test_codespace_admission.py`."""

    def __init__(self, *, receipt_written: dict | None = None, fail_at: str | None = None,
                created_name: str = "fluffy-space-1"):
        self.calls: list[list[str]] = []
        self.receipt_written = receipt_written
        self.fail_at = fail_at
        self.created_name = created_name

    def __call__(self, argv):
        argv = list(argv)
        self.calls.append(argv)
        verb = " ".join(argv[:2])
        # `codespace ssh` covers two distinct calls (`mkdir -p <workdir>`, then `bash <runner>`)
        # -- tag them apart so a test can fail one without silently failing the other too.
        tag = ("codespace ssh mkdir" if verb == "codespace ssh" and "mkdir" in argv else
              "codespace ssh run" if verb == "codespace ssh" and "bash" in argv else verb)
        if self.fail_at in (verb, tag):
            return d.GhResult(ok=False, exit_code=1, stdout="boom")
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
            return d.GhResult(ok=True, exit_code=0, stdout="")
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
    # create (its stdout IS the name), mkdir the workdir, cp contract, cp runner, ssh run, cp
    # receipt back -- no `list` call: the name is never reconstructed (codex terra P1, 2026-09-27)
    verbs = [" ".join(c[:2]) for c in fake.calls]
    assert verbs == ["codespace create", "codespace ssh", "codespace cp", "codespace cp",
                     "codespace ssh", "codespace cp"]


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
    assert verbs == ["codespace create", "codespace ssh"]  # nothing shipped


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
            return d.GhResult(True, 0, "")
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
            return d.GhResult(True, 0, "")
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
            return d.GhResult(True, 0, "")
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
