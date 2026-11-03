"""RED-first contract tests for the moved commit-gate known-reds verdict."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"
_REGISTRY = _REPO / "logs" / "KNOWN-REDS-REGISTRY.json"

REGISTERED_LINES = [
    "[!!] repos registered  (none)",
    "[!!] hooks_armed: git hooks not armed (RF-2) — SessionStart self-arm should install them",
    "[!!] dispatch_drift: PowerShell command 'dispatch' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Dispatch-Cloud' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'claude' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Dispatch-Codespace' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Harvest-Codespace' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Dispatch-Local' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Dispatch-Lane' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Dispatch-CloudV2' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Get-CloudSession' is unavailable",
    "[!!] dispatch_drift: PowerShell command 'Archive-CloudSession' is unavailable",
]
AUDIT_BLOCK = (
    "operational:\n"
    f"  {REGISTERED_LINES[0]}\n"
    "self-audit (.dev-knowledge) - 60/243 pass:\n"
    + "".join(f"  {line}\n" for line in REGISTERED_LINES[1:])
    + "health: DEGRADED\n"
)
NEW_CHECK_LINE = "[!!] new_check: boom"
NEW_DISPATCH_LINE = "[!!] dispatch_drift: command 'Get-Foo' is unavailable"
UNREGISTERED_BLOCK = "graph audit:\n  [!!] graph_orphan: new orphan\n"


def _failed_hook(hook_id: str, output: str, exit_code: int = 1) -> str:
    return (
        f"Hook {hook_id}........................................................Failed\n"
        f"- hook id: {hook_id}\n"
        f"- exit code: {exit_code}\n\n"
        f"{output}"
    )


def _gate_output(*failed_hooks: str, trailer: str = "wall_seconds=72 exit=1") -> str:
    return "".join(failed_hooks) + trailer + "\n"


def _registry(known_reds):
    return known_reds.Registry(
        schema=known_reds.SCHEMA,
        baseline_id="2026-11-03-test-baseline",
        measured_at_sha="test-sha",
        measured_via="test",
        workers=1,
        members={},
        hooks={
            "audit-health": {
                "attribution": known_reds.ENVIRONMENT_MISMATCH,
                "checks": [
                    "dispatch_drift",
                    "hooks_armed",
                    "journal_spine_anchor",
                    "repos registered",
                ],
                "lines": REGISTERED_LINES,
            }
        },
    )


def _commit_gate_step():
    workflow = yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))
    job = workflow["jobs"]["commit-gate"]
    steps = job["steps"]
    gate = next(step for step in steps
                if step.get("name") == "Run the moved commit-gate hooks over this range's staged set")
    verdict = next(step for step in steps
                   if step.get("name", "").startswith("known-reds verdict on audit-health"))
    return gate, verdict


def test_compare_commit_gate_calls_compare_hook_per_failure_and_keeps_baseline(monkeypatch):
    import known_reds

    registry = known_reds.load_registry(Path(known_reds.REGISTRY_PATH))
    original = known_reds.compare_hook
    calls = []

    def recording_compare_hook(hook_id, exit_code, passed_registry, hook_output=None):
        result = original(hook_id, exit_code, passed_registry, hook_output=hook_output)
        calls.append((hook_id, exit_code, hook_output, result))
        return result

    monkeypatch.setattr(known_reds, "compare_hook", recording_compare_hook)
    graph_block = "graph audit:\n  [!!] graph_orphan: new orphan\n"
    output = _gate_output(
        _failed_hook("audit-health", AUDIT_BLOCK),
        _failed_hook("graph-orphan-census", graph_block),
    )

    result = known_reds.compare_commit_gate(output, 1, registry)

    assert [(hook_id, exit_code, hook_output) for hook_id, exit_code, hook_output, _ in calls] == [
        ("audit-health", 1, AUDIT_BLOCK),
        ("graph-orphan-census", 1, graph_block),
    ]
    assert result["baseline_id"] == registry.baseline_id
    assert all(call_result["baseline_id"] == result["baseline_id"]
               for _, _, _, call_result in calls)
    assert result["baseline_id"] == known_reds.load_registry(
        Path(known_reds.REGISTRY_PATH)
    ).baseline_id


def test_conductor_commit_gate_uses_shared_compare_without_copied_registry_rules():
    gate, verdict = _commit_gate_step()
    gate_run = gate["run"]
    verdict_run = verdict["run"]

    assert "scripts/known_reds.py" in gate_run
    assert "scripts/known_reds.py" in verdict_run
    assert "--registry" not in gate_run
    assert "--registry" not in verdict_run
    assert "compare-commit-gate" in gate_run
    assert "--gate-output commit-gate.out" in gate_run
    assert "--gate-exit-code" in gate_run
    assert all(value not in gate_run for value in (
        "audit-health",
        "dispatch_drift",
        "hooks_armed",
        "journal_spine_anchor",
        "2026-10-04-fdf4f4952211",
    ))


def test_audit_health_passes_when_all_twelve_registered_lines_match():
    import known_reds

    result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", AUDIT_BLOCK)),
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "pass"
    assert result["hooks"][0]["verdict"] == "pass"
    assert [line for line in result["hooks"][0]["lines"] if line["tag"] == "known"] == [
        {"text": line, "tag": "known"} for line in REGISTERED_LINES
    ]


def test_audit_health_fails_on_a_new_unregistered_check_line():
    import known_reds

    output = AUDIT_BLOCK + f"  {NEW_CHECK_LINE}\n"
    result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", output)),
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "fail"
    assert any("new_check" in item or NEW_CHECK_LINE in item for item in result["regressions"])


def test_an_unregistered_failed_hook_is_a_regression():
    import known_reds

    result = known_reds.compare_commit_gate(
        _gate_output(
            _failed_hook("audit-health", AUDIT_BLOCK),
            _failed_hook("graph-orphan-census", UNREGISTERED_BLOCK),
        ),
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "fail"
    assert any("graph-orphan-census" in item for item in result["regressions"])


def test_nonzero_gate_exit_without_a_parseable_failed_hook_fails_closed():
    import known_reds

    result = known_reds.compare_commit_gate(
        "Normalize dated-log entry headers........................................Passed\n"
        "wall_seconds=72 exit=1\n",
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "fail"
    assert result["regressions"]


def test_zero_gate_exit_passes_even_without_hook_entries():
    import known_reds

    registry = known_reds.Registry(
        schema=known_reds.SCHEMA,
        baseline_id="2026-11-03-empty",
        measured_at_sha="test-sha",
        measured_via="test",
        workers=1,
        members={},
        hooks={},
    )

    result = known_reds.compare_commit_gate("", 0, registry)

    assert result["verdict"] == "pass"
    assert result["regressions"] == []


def test_registered_check_allowlist_fails_closed_without_parseable_failure_names():
    import known_reds

    result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", "health: DEGRADED\n")),
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "fail"


def test_registered_dispatch_name_does_not_cover_a_new_unregistered_line():
    import known_reds

    output = AUDIT_BLOCK + f"  {NEW_DISPATCH_LINE}\n"
    result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", output)),
        1,
        _registry(known_reds),
    )

    assert result["verdict"] == "fail"
    assert any(NEW_DISPATCH_LINE in item for item in result["regressions"])
    lines = result["hooks"][0]["lines"]
    assert all(line["tag"] == "known" for line in lines[:12])
    assert lines[12] == {"text": NEW_DISPATCH_LINE, "tag": "REGRESSION"}


def test_render_compare_commit_gate_classifies_registered_new_and_changed_lines():
    import known_reds

    registry = _registry(known_reds)
    known_result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", AUDIT_BLOCK)), 1, registry
    )
    known_report = known_reds.render_compare_commit_gate(known_result)
    classified = [line for line in known_report.splitlines() if "[!!]" in line]

    assert "audit-health" in known_report
    assert len(classified) == 12
    assert sum("known" in line for line in classified) == 12
    assert "REGRESSION" not in known_report
    assert not any(line.lstrip().startswith("|") for line in known_report.splitlines())

    new_result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", AUDIT_BLOCK + f"  {NEW_CHECK_LINE}\n")),
        1,
        registry,
    )
    new_report = known_reds.render_compare_commit_gate(new_result)
    assert "REGRESSION" in new_report

    changed_result = known_reds.compare_commit_gate(
        _gate_output(_failed_hook("audit-health", AUDIT_BLOCK + f"  {NEW_DISPATCH_LINE}\n")),
        1,
        registry,
    )
    changed_report = known_reds.render_compare_commit_gate(changed_result)
    changed_lines = [line for line in changed_report.splitlines() if "[!!]" in line]
    assert any(NEW_DISPATCH_LINE in line and "REGRESSION" in line for line in changed_lines)
    assert sum("known" in line for line in changed_lines) == 12


def test_commit_gate_shell_step_classifies_and_appends_both_verdicts(tmp_path):
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash is not on PATH; commit-gate shell integration cannot run")

    gate, _ = _commit_gate_step()
    script = gate["run"]
    for expression, value in (
        ("${{ github.event_name }}", "push"),
        ("${{ github.ref }}", "refs/heads/worktree-x"),
        ("${{ github.sha }}", "abc"),
        ("${{ github.event.before }}", ""),
        ("${{ github.event.pull_request.base.sha }}", ""),
    ):
        script = script.replace(expression, value)

    git_path = shutil.which("git")
    if not git_path:
        pytest.skip("git is not on PATH; commit-gate shell integration cannot run")

    for case, gate_output, expected_exit, expected_tag in (
        ("pass", _gate_output(_failed_hook("audit-health", AUDIT_BLOCK)), 0, "known"),
        (
            "fail",
            _gate_output(_failed_hook(
                "audit-health", AUDIT_BLOCK + f"  {NEW_DISPATCH_LINE}\n"
            )),
            1,
            "REGRESSION",
        ),
    ):
        workdir = tmp_path / case
        workdir.mkdir()
        subprocess.run([git_path, "init", "--quiet", str(workdir)], check=True)
        bin_dir = workdir / "bin"
        bin_dir.mkdir()
        fixture_path = workdir / "fixture.out"
        fixture_path.write_text(gate_output, encoding="utf-8")
        wrapper_env = {
            "FIXTURE": str(fixture_path),
            "FIXTURE_EXIT": "1",
            "PYTHON_EXE": sys.executable,
            "REPO_ROOT": str(_REPO),
        }
        git_wrapper = bin_dir / "git"
        git_wrapper.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = "merge-base" ] && [ "$2" = "--is-ancestor" ]; then exit 0; fi\n'
            'if [ "$1" = "merge-base" ]; then echo fake-base-sha; exit 0; fi\n'
            'if [ "$1" = "fetch" ] || [ "$1" = "reset" ]; then exit 0; fi\n'
            'if [ "$1" = "rev-parse" ]; then echo fake-base-sha; exit 0; fi\n'
            "exit 0\n",
            encoding="utf-8",
        )
        uv_wrapper = bin_dir / "uv"
        uv_wrapper.write_text(
            "#!/bin/sh\n"
            'case " $* " in *" pre-commit "*) cat "$FIXTURE"; exit "$FIXTURE_EXIT";; esac\n'
            'while [ "$#" -gt 0 ]; do\n'
            '  if [ "$1" = "scripts/known_reds.py" ]; then\n'
            "    shift\n"
            '    cd "$REPO_ROOT" || exit 98\n'
            '    exec "$PYTHON_EXE" "$REPO_ROOT/scripts/known_reds.py" "$@"\n'
            "  fi\n"
            "  shift\n"
            "done\n"
            "exit 97\n",
            encoding="utf-8",
        )
        git_wrapper.chmod(0o755)
        uv_wrapper.chmod(0o755)
        summary_path = workdir / "summary.md"
        env = os.environ.copy()
        env.update(wrapper_env)
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        env["GITHUB_STEP_SUMMARY"] = str(summary_path)
        completed = subprocess.run(
            [bash, "-c", script],
            cwd=workdir,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        assert completed.returncode == expected_exit, completed.stdout + completed.stderr
        assert expected_tag in completed.stdout
        summary = summary_path.read_text(encoding="utf-8")
        assert expected_tag in summary
        if case == "pass":
            assert sum(
                "[!!]" in line and "known" in line
                for line in completed.stdout.splitlines()
            ) == 12
            assert sum("[!!]" in line and "known" in line for line in summary.splitlines()) == 12
        if case == "fail":
            assert any(
                NEW_DISPATCH_LINE in line and "REGRESSION" in line
                for line in completed.stdout.splitlines()
            )


def test_compare_commit_gate_and_cli_leave_registry_bytes_unchanged(tmp_path, capsys):
    import known_reds

    real_path = Path(known_reds.REGISTRY_PATH)
    real_before = real_path.read_bytes()
    copied_path = tmp_path / "registry.json"
    copied_path.write_bytes(real_before)
    copied_before = copied_path.read_bytes()
    gate_path = tmp_path / "commit-gate.out"
    gate_path.write_text("wall_seconds=1 exit=0\n", encoding="utf-8")

    result = known_reds.compare_commit_gate(
        gate_path.read_text(encoding="utf-8"),
        0,
        known_reds.load_registry(copied_path),
    )
    assert result["verdict"] == "pass"
    assert copied_path.read_bytes() == copied_before

    rc = known_reds.main([
        "compare-commit-gate",
        "--gate-output",
        str(gate_path),
        "--gate-exit-code",
        "0",
        "--registry",
        str(copied_path),
    ])
    assert rc == 0
    assert capsys.readouterr().out
    assert copied_path.read_bytes() == copied_before
    assert real_path.read_bytes() == real_before


def test_registry_is_origin_main_plus_exactly_the_lines_field():
    import known_reds

    try:
        origin_text = subprocess.run(
            ["git", "show", "origin/main:logs/KNOWN-REDS-REGISTRY.json"],
            cwd=_REPO,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"git or origin/main registry is unavailable: {exc}")

    working = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    origin = json.loads(origin_text)
    hooks = working["hooks"]["audit-health"]
    lines = hooks.get("lines", [])
    hooks_without_lines = dict(hooks)
    hooks_without_lines.pop("lines", None)
    working["hooks"]["audit-health"] = hooks_without_lines
    assert working == origin
    assert len(lines) == 12
    assert all(line.startswith("[!!]") for line in lines)

    registry = known_reds.load_registry(_REGISTRY)
    date = registry.baseline_id.rsplit("-", 1)[0]
    assert registry.baseline_id == known_reds.compute_baseline_id(
        registry.members,
        date=date,
        members_by_os=registry.members_by_os,
    )
