"""The `PreToolUse` prompts-guard WIRING -- the hook object in `.claude/settings.json`.

`tests/test_fleet_health.py` covers the guard's verdict function. Nothing covered the
hook object that *invokes* it, and that is where MA-1 lived (`[#684]`): the command was
`python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`, and
`CLAUDE_PROJECT_DIR` is set by Claude Code and by nothing else. A reader that honours the
hook file without defining the variable expands it to empty, the interpreter cannot open
the path, it exits non-zero -- and a `PreToolUse` hook that exits non-zero REFUSES. Total
refusal of every tool call, attributed to the tool it blocked rather than to us
(`docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:83, pointer :105).

**THE POSTURE INVERTED 2026-09-11 (batch X lane W-2', AX15-1).** Three of the properties
below used to assert FAIL-OPEN and now assert FAIL-CLOSED. The history is kept rather than
rewritten, because the argument that produced the fail-open form was careful and a later
reader who does not see it will make it again: batch W's W-2 lane reasoned, correctly on
its own terms, that a guard which bricks every tool call because its interpreter is missing
is a worse defect than the stale directory it guards -- and MA-1 itself was exactly that
failure, a non-Claude reader refused by an interpreter error. AX15-1 reverses it on a
different axis: *"a guard that permits when it cannot run is declared enforcement without
enforcement."* What makes the reversal safe rather than a return to the 2026-09-06 wedge is
the MATCHER, which stays narrowed -- the break-glass family is ungated, so a refusing guard
still leaves an in-session way out -- plus a refusal text that names cause AND fix, and a
SessionStart preflight that says so once before any tool call pays for it.

Six properties are asserted here. The first is the edit `[#684]` names; the rest carry the
2026-09-11 Codex review of this branch and AX15-1's inversion:

* **The command resolves the repo root itself.** Measured 2026-09-11 by a throwaway child
  session: hook commands run through a POSIX shell (`bash.exe`) with cwd == the project
  directory, so a `${CLAUDE_PROJECT_DIR:-.}` default is both available and correct. The
  RED-first witness `[#684]`'s Done-when asks for is
  `test_hook_command_resolves_the_script_without_claude_project_dir`: delete the fallback
  and it fails.
* **A command that cannot resolve its script REFUSES, naming cause and fix.** AX15-1's
  first failure mode. The refusal is not bare: it prints which roots it tried and what to
  do about it, because the operator's standing rule is that a deviation raises an exception
  that TEACHES.
* **No usable interpreter REFUSES, naming cause and fix.** AX15-1's second failure mode,
  and the one the fail-open form was written to permit.
* **A crashing guard REFUSES, naming cause and fix.** `prompts_guard()` returns 0 or 2 and
  nothing else, so any other status is a failure to RUN it -- and AX15-1 puts *"any rc
  other than 0"* in the refusing class.
* **A refusal is PROPAGATED, not swallowed.** The risk the fail-open leg creates is
  precise -- a command string that turns the guard's refusal into a pass -- and it is
  pinned hermetically by a stand-in that exits `2`, because the real verdict's User-scope
  half is registry state this suite must not touch.
* **The matcher names tool classes instead of `"*"`.** `"*"` is what converted an
  interpreter error into a session with no escape: `ToolSearch` was refused too, which is
  the only route to the deferred `ExitWorktree` / `SendMessage` tools, so the session could
  not undo the change that broke it (recovery took an external shell). The narrowing is of
  the MATCHER, never of the refusal.
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest


_REPO_ROOT = Path(__file__).resolve().parent.parent
_SETTINGS = _REPO_ROOT / ".claude" / "settings.json"


def _load_fleet_health():
    """The guard module, loaded for ONE constant: the marker its pass emits.

    This file is otherwise deliberately hermetic -- it runs the shipped command string
    through a real shell against stand-in trees, and imports nothing from the thing it
    tests. The marker is the exception because it is the one token that must agree ACROSS
    the two files: `fleet_health.py` prints it, `.claude/settings.json` tests for it, and
    if either side is edited alone the hook silently stops being able to tell a guard that
    passed from a `python` that never ran it. Hard-coding a second copy here would leave
    that break invisible to exactly the suite that exists to catch it.
    """
    spec = importlib.util.spec_from_file_location(
        "fleet_health_for_wiring", _REPO_ROOT / "scripts" / "fleet_health.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


#: Proof the GUARD evaluated -- emitted by `prompts_guard()` on every non-refusing verdict
#: and required by the hook command before it permits. Sourced from the module, never
#: retyped: see `_load_fleet_health`.
_EVALUATED = _load_fleet_health().GUARD_EVALUATED_MARKER

#: The classes a stale `CLAUDE_PROMPTS_DIR` actually makes lie -- anything that reads or
#: writes the filesystem under a directory the seat resolved wrongly.
#:
#: The MCP and secondary routes were added 2026-09-11 by the fresh Codex review of this
#: branch (HIGH-2): an `mcp__*` filesystem tool reaches a wrongly-resolved directory
#: without passing the guard, and so do `ReadMcpResourceTool`, `LSP` and `Monitor`. `LSP`
#: and `ReadMcpResourceTool` are NOT in this client's roster -- a matcher branch naming a
#: tool that does not exist is inert, so over-listing costs nothing and under-listing is a
#: gap. The `mcp__` entry is a representative name, not a roster claim.
_MUST_MATCH = (
    "Read", "Write", "Edit", "MultiEdit", "NotebookEdit",
    "Glob", "Grep", "Bash", "PowerShell",
    "Monitor", "LSP", "ReadMcpResourceTool", "mcp__filesystem__read_file",
)
#: The break-glass, and it is a ROUTE plus a DESTINATION. `ToolSearch` is the only way to
#: reach the deferred session-control tools, so gating it is what made the `"*"` wedge
#: terminal rather than merely loud -- but gating what it reaches defeats the escape just
#: as surely, which is why `ExitWorktree` and `SendMessage` are pinned here too. This is
#: the reason two of the Codex review's HIGH-2 names (`EnterWorktree` / `ExitWorktree`)
#: were refused rather than adopted: they are this family, not the filesystem family.
#: BOTH are pinned, not just `ExitWorktree`: the second Codex pass caught that the roster
#: named only one of the two the comment above rules out, so a later edit could have gated
#: `EnterWorktree` -- re-blocking part of the documented recovery path -- with every test
#: here still green. A decision no test can fail is a comment, not a rule.
_MUST_NOT_MATCH = ("ToolSearch", "EnterWorktree", "ExitWorktree", "SendMessage")

def _resolve_posix_shell():
    """The shell Claude Code actually runs hook commands through, resolved by RUNNING it.

    `shutil.which("bash")` alone is NOT enough on Windows, and the failure is silent in the
    worst way. Measured 2026-09-11 in this repo: from one session `which` returned
    `C:/Program Files/Git/bin/bash.exe` and every test here passed; from another, whose
    PATH put `WindowsApps` first, the same call returned the WSL app-execution-alias stub
    `.../WindowsApps/bash.EXE`, which on a machine with no distro installed exits 1 with
    its message on STDOUT and an EMPTY stderr -- so all eight shell-backed tests failed,
    loudly, with `rc=1 stderr=''` and nothing pointing at the cause. Worse than the noise:
    a WSL bash WITH a distro would run, and would then be asserting the hook's behaviour
    under a shell that cannot even see this repo's Windows paths.

    So candidates are validated by their ability to stat a Windows path, not by existing.
    """
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        shutil.which("bash"),
        shutil.which("sh"),
    ]
    probe = _SETTINGS.as_posix()
    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen or not Path(candidate).exists():
            continue
        seen.add(candidate)
        try:
            probed = subprocess.run(
                [candidate, "-c", f'[ -f "{probe}" ]'],
                capture_output=True, text=True, timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if probed.returncode == 0:
            return candidate
    return None


_SH = _resolve_posix_shell()

#: "The command reached the script at this root", proven POSITIVELY rather than inferred
#: from a magic exit code. It used to be an exit of 7, but under AX15-1 the command maps
#: every status except `0` to `2`, so a distinctive exit code can no longer carry this
#: signal -- and a marker on stdout is better evidence anyway: it says WHICH file ran, not
#: merely that something did. Note this makes the marker load-bearing in BOTH directions
#: now: several tests below assert the refusal came from the existence legs by asserting
#: the marker is ABSENT, which a shared exit code could not distinguish.
_REACHED = "PROMPTS-GUARD-STANDIN-REACHED"
#: The refusal code -- the guard's own, and since AX15-1 also the code the command emits on
#: every inability to evaluate. A stand-in returning it proves the command PROPAGATES a
#: refusal rather than swallowing it -- hermetically, on any platform, which the live-tree
#: test cannot do because the User-scope half of the real verdict is registry state this
#: suite must not touch.
_REFUSES = 2


def _prompts_guard_hooks():
    settings = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    hits = [
        (entry.get("matcher", ""), hook["command"])
        for entry in settings["hooks"]["PreToolUse"]
        for hook in entry["hooks"]
        if "--prompts-guard" in hook.get("command", "")
    ]
    assert len(hits) == 1, f"expected exactly one prompts-guard hook, found {len(hits)}"
    return hits[0]


def _hook_command() -> str:
    return _prompts_guard_hooks()[1]


def _hook_matcher() -> str:
    return _prompts_guard_hooks()[0]


def _matches(matcher: str, tool: str) -> bool:
    """Claude Code's matcher semantics: `"*"` and `""` match every tool; anything else is
    a regex matched against the tool name."""
    if matcher in ("*", ""):
        return True
    return re.fullmatch(matcher, tool) is not None


def _fake_tree(root: Path, code: int = 0, evaluated: bool | None = None) -> Path:
    """A tree shaped like this repo whose `scripts/fleet_health.py` announces that it RAN
    and then exits `code` -- `_REFUSES` for a guard that refuses, `1` for one that crashes.

    `evaluated` controls the second marker, the one the REAL guard emits on a non-refusing
    verdict. It defaults to matching the real module's behaviour (emitted exactly when the
    guard passes), so a stand-in stands in faithfully. Passing `evaluated=False` with
    `code=0` builds the case the Codex review named: something that exits 0 having proven
    nothing -- a shim, a wrapper, or a `python` that never reached this file at all.
    """
    if evaluated is None:
        evaluated = code == 0
    lines = ["import sys", f"print({_REACHED!r})"]
    if evaluated:
        lines.append(f"print({_EVALUATED!r})")
    lines.append(f"sys.exit({code})")
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts" / "fleet_health.py").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return root


def _shim_dir(root: Path, exit_code: int = 0) -> str:
    """A directory holding a `python` that is NOT an interpreter -- it exits without
    running its arguments. Prepended to PATH, it is the shadow-interpreter case."""
    root.mkdir(parents=True, exist_ok=True)
    shim = root / "python"
    shim.write_text(f"#!/bin/sh\nexit {exit_code}\n", encoding="utf-8")
    shim.chmod(0o755)
    return str(root)


def _run(command: str, *, cwd: Path, project_dir, path=None):
    """Run COMMAND the way Claude Code runs a hook command. `path` REPLACES PATH, which is
    how the no-usable-interpreter case is reached hermetically."""
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    if project_dir is not None:
        env["CLAUDE_PROJECT_DIR"] = project_dir
    if path is not None:
        env["PATH"] = path
    assert _SH is not None, (
        "no WORKING POSIX shell found -- Claude Code runs hook commands through one "
        "(measured 2026-09-11: C:/Program Files/Git/bin/bash.exe), so this hook cannot "
        "run here. Note a WSL stub on PATH does not count: it is rejected on purpose, "
        "see _resolve_posix_shell"
    )
    return subprocess.run(
        [_SH, "-c", command],
        cwd=str(cwd), env=env, capture_output=True, text=True, timeout=60,
    )


#: Asserts against the LIVE `.claude/settings.json`, so it belongs in the docs-only ship
#: pre-flight selection (#256/#260 tiering) as well as in the full suite.
#:
#: NO `skipif` on the shell. A machine with no POSIX shell is a machine where this hook
#: command cannot run at all, so skipping there would hide exactly the breakage this file
#: exists to catch -- the `proof_layer` rule, in its own words: *a proof that can be
#: skipped on the machine that breaks the property is not a mechanism*. Absence FAILS,
#: with the reason named.
pytestmark = pytest.mark.live_repo


# --- the repo-root fallback -------------------------------------------------------------

def test_hook_command_resolves_the_script_without_claude_project_dir(tmp_path):
    """RED-first witness for `[#684]`: remove the fallback and this fails.

    Hermetic -- the script it reaches is the exit-7 stand-in, not the real guard, so the
    assertion is about path resolution alone and cannot be satisfied or broken by the
    machine's live `CLAUDE_PROMPTS_DIR` scopes.
    """
    tree = _fake_tree(tmp_path / "tree")
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert _REACHED in result.stdout, (
        "with CLAUDE_PROJECT_DIR unset the hook did not reach "
        f"<root>/scripts/fleet_health.py: rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_still_prefers_claude_project_dir_when_it_is_set(tmp_path):
    """The fallback is a fallback. Where the variable IS set it stays authoritative, so a
    Claude Code session keeps working from any cwd."""
    tree = _fake_tree(tmp_path / "tree")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(_hook_command(), cwd=elsewhere, project_dir=str(tree))
    assert _REACHED in result.stdout, (
        f"CLAUDE_PROJECT_DIR was ignored: rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_falls_back_to_cwd_when_claude_project_dir_is_set_but_wrong(tmp_path):
    """RED-first witness for the Codex review's HIGH-1: a NON-EMPTY but wrong variable.

    `${CLAUDE_PROJECT_DIR:-.}` only defaults when the variable is unset or empty, so a
    variable pointing at the wrong root skipped the fallback entirely and the command
    fell straight through to the fail-open leg -- passing without ever consulting the
    guard that was sitting in cwd all along. The second `[ -f ]` attempt closes that:
    fail-open is now reserved for the case where NO root resolves, which is what the
    posture was always argued as.
    """
    tree = _fake_tree(tmp_path / "tree")
    wrong = tmp_path / "wrong-root"
    wrong.mkdir()
    result = _run(_hook_command(), cwd=tree, project_dir=str(wrong))
    assert _REACHED in result.stdout, (
        "a wrong CLAUDE_PROJECT_DIR fell through to fail-open instead of trying cwd, so "
        "a resolvable guard went unconsulted: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_falls_back_to_cwd_when_claude_project_dir_is_set_empty(tmp_path):
    """Set-but-empty is the shape a harness that *exports* the variable without a value
    produces. `:-` (not `-`) is what makes it take the default, so this pins the colon."""
    tree = _fake_tree(tmp_path / "tree")
    result = _run(_hook_command(), cwd=tree, project_dir="")
    assert _REACHED in result.stdout, (
        f"an empty CLAUDE_PROJECT_DIR did not fall back to cwd: rc={result.returncode} "
        f"stderr={result.stderr!r}"
    )


def test_hook_command_resolves_a_root_whose_path_contains_spaces(tmp_path):
    """This repo's own root has no spaces, but the hook ships to consumers. Every
    expansion in the command is quoted; this asserts that rather than assuming it."""
    tree = _fake_tree(tmp_path / "a root with spaces" / "tree")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(_hook_command(), cwd=elsewhere, project_dir=str(tree))
    assert _REACHED in result.stdout, (
        "a root containing spaces was word-split by the hook command: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )


def _assert_teaches(stderr: str, *, cause_names: tuple[str, ...]):
    """AX15-1's refusal-text clause, asserted rather than trusted: *"the refusal text names
    the cause and the fix (the operator's rule: a deviation raises an exception that
    teaches)"*.

    A bare non-zero exit satisfies "fails closed" and teaches nothing -- and the session
    that receives it sees only that its tool call was refused, with no way to tell a stale
    prompts dir from a guard that could not start. So three things are required of every
    refusal: the verdict word, a labelled CAUSE naming the specific thing that was missing,
    and a labelled FIX that is an action.
    """
    assert "REFUSED" in stderr, f"refusal did not announce itself: {stderr!r}"
    assert "Cause:" in stderr, f"refusal names no cause: {stderr!r}"
    assert "Fix:" in stderr, f"refusal names no fix: {stderr!r}"
    missing = [token for token in cause_names if token not in stderr]
    assert not missing, (
        f"the cause is labelled but not specific -- {missing} absent from: {stderr!r}"
    )


def test_hook_command_refuses_when_no_root_resolves(tmp_path):
    """RED-first trip-test 1 of 2 (AX15-3): **script removed -> refused with message**.

    Variable unset AND cwd outside any checkout: the guard cannot be LOADED. Until
    2026-09-11 this PASSED, by the argument recorded in the module docstring. AX15-1
    reverses it -- *"a guard that permits when it cannot run is declared enforcement
    without enforcement"* -- so the hook must refuse, and must say which roots it tried so
    the reader can fix the one that is wrong.
    """
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(_hook_command(), cwd=elsewhere, project_dir=None)
    assert result.returncode == _REFUSES, (
        "an unresolvable guard PERMITTED the tool call -- declared enforcement without "
        f"enforcement (AX15-1): rc={result.returncode} stderr={result.stderr!r}"
    )
    assert _REACHED not in result.stdout, (
        "nothing should have run: the refusal must come from the existence legs, not from "
        f"a stand-in that executed anyway -- stdout={result.stdout!r}"
    )
    _assert_teaches(result.stderr,
                    cause_names=("CLAUDE_PROJECT_DIR", "scripts/fleet_health.py"))


def test_hook_command_refuses_when_the_interpreter_is_unavailable(tmp_path):
    """RED-first trip-test 2 of 2 (AX15-3): **interpreter broken -> refused with message**.

    The two `[ -f ]` legs guard the SCRIPT's existence and say nothing about the
    INTERPRETER's, so a reader with no usable `python` reaches the `rc != 2` branch. That
    branch used to exit 0. It now refuses, and NAMES the interpreter as the cause -- which
    is the whole difference between this and the MA-1 failure it superficially resembles:
    MA-1 refused SILENTLY, and the reader read it as its own breakage.

    Reached hermetically by emptying PATH. The stand-in is the REFUSING one on purpose, so
    the assertion cannot be satisfied by the stand-in's own exit code.
    """
    tree = _fake_tree(tmp_path / "tree", code=_REFUSES)
    result = _run(_hook_command(), cwd=tree, project_dir=None, path="")
    assert _REACHED not in result.stdout, (
        "PATH was not actually emptied -- the interpreter ran, so this test is not "
        f"measuring what it claims: stdout={result.stdout!r}"
    )
    assert result.returncode == _REFUSES, (
        "no usable interpreter PERMITTED every matching tool call: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )
    _assert_teaches(result.stderr, cause_names=("python", "PATH"))


def test_hook_command_refuses_when_the_guard_crashes(tmp_path):
    """AX15-1's *"any rc other than 0"*, the third inability-to-evaluate mode: the module is
    found and the interpreter starts, then dies on import or syntax.

    `prompts_guard()` returns 0 or 2 and NOTHING else, so a `1` cannot be a verdict -- it
    can only be a crash. The refusal must say so SPECIFICALLY: a crash and a missing
    interpreter reach the same branch, and a message that blamed PATH for an import error
    would send the reader to the wrong place.
    """
    tree = _fake_tree(tmp_path / "tree", code=1)
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert _REACHED in result.stdout, "the stand-in did not run, so this proves nothing"
    assert result.returncode == _REFUSES, (
        "a crashing guard PERMITTED the tool call: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )
    _assert_teaches(result.stderr, cause_names=("crashed", "rc=1"))


def test_hook_command_still_passes_when_the_guard_passes(tmp_path):
    """The non-over-refusal claim, hermetically -- the M7 property in miniature.

    Fail-closed is only defensible if a guard that RAN and said "ok" is still a pass. This
    is the test that fails if the inversion is implemented by refusing on everything that
    is not literally `exit 2`, which would refuse every ordinary session.
    """
    tree = _fake_tree(tmp_path / "tree", code=0)
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert _REACHED in result.stdout, "the stand-in did not run, so this proves nothing"
    assert result.returncode == 0, (
        "a PASSING guard was turned into a refusal -- fail-closed was applied to the "
        f"verdict, not to the inability to evaluate: rc={result.returncode} "
        f"stderr={result.stderr!r}"
    )


def test_hook_command_refuses_an_exit_0_that_carries_no_evaluated_marker(tmp_path):
    """An exit of 0 is not evidence. The MARKER is.

    Added 2026-09-11 by the fresh Codex review of this branch (HIGH-1), and it is the last
    fail-open path that survived the AX15-1 inversion: the command refused on every
    non-zero status but still read `0` as "the guard ran and passed". Nothing established
    that. A `python` that exits 0 without ever opening `fleet_health.py` produces a byte
    identical result, so the hook permitted the call believing it had checked one --
    declared enforcement with no enforcement, the exact thing AX15-1 names.

    The stand-in here RAN (`_REACHED` is on stdout) and still proved nothing, which
    isolates the property to the marker rather than to reachability.
    """
    tree = _fake_tree(tmp_path / "tree", code=0, evaluated=False)
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert _REACHED in result.stdout, "the stand-in did not run, so this proves nothing"
    assert _EVALUATED not in result.stdout, "the stand-in emitted the marker it must not"
    assert result.returncode == _REFUSES, (
        "an exit of 0 with NO proof the guard evaluated was treated as a pass: "
        f"rc={result.returncode} stdout={result.stdout!r}"
    )
    _assert_teaches(result.stderr, cause_names=(_EVALUATED, "rc=0"))


def test_hook_command_refuses_a_shadow_interpreter_that_never_runs_the_guard(tmp_path):
    """The same hole at its REAL entry point: `python` resolved to something else.

    The test above builds the failure from the script side because that is hermetic; this
    one builds it the way it actually arrives -- a `python` earlier on PATH that is not an
    interpreter. A launcher shim, a stale wrapper, a corporate intercept: each exits 0
    having run nothing. The guard tree here is fully intact and would PASS if it were ever
    reached, so a refusal can only come from the hook declining to infer evaluation.
    """
    tree = _fake_tree(tmp_path / "tree", code=0)
    shim = _shim_dir(tmp_path / "shim")
    result = _run(_hook_command(), cwd=tree, project_dir=None, path=shim)
    assert _REACHED not in result.stdout, (
        "the shim was not on PATH -- the real interpreter ran, so this proves nothing: "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert result.returncode == _REFUSES, (
        "a shadow 'python' that never ran the guard PERMITTED the tool call: "
        f"rc={result.returncode} stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    _assert_teaches(result.stderr, cause_names=(_EVALUATED,))


def test_hook_command_tests_for_the_marker_the_guard_module_actually_emits(tmp_path):
    """The two files must agree on the token, and only a test can hold them together.

    `fleet_health.py` prints the marker; `.claude/settings.json` tests for it. Edit either
    alone and the hook stops being able to distinguish a guard that passed from a `python`
    that never ran -- silently, and in the permissive direction on the settings side. The
    constant is read from the module (see `_load_fleet_health`), so this compares the
    shipped command against the live spelling rather than against a second copy.
    """
    assert _EVALUATED in _hook_command(), (
        f"the hook command does not test for {_EVALUATED!r}, the marker the guard emits "
        "-- the two halves of the positive-proof check have drifted apart"
    )


def test_hook_command_propagates_the_guards_refusal(tmp_path):
    """The non-weakening claim, asserted HERMETICALLY -- the Codex review's HIGH-3.

    The risk the fail-open leg creates is precise: a command string that turns the guard's
    REFUSAL into a pass. A stand-in that exits `2` in a `tmp_path` tree pins exactly that,
    on any platform and under any ambient scope, because it removes the registry half of
    the real verdict from the question entirely. Delete the `python "$g"` tail -- or add
    anything that swallows its status -- and this fails.
    """
    tree = _fake_tree(tmp_path / "tree", code=_REFUSES)
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert result.returncode == _REFUSES, (
        "the hook command did not propagate the guard's refusal -- a refusal was converted "
        f"into a pass: rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_still_runs_the_real_guard_from_the_repo_root():
    """Non-weakening against the LIVE tree -- by EQUIVALENCE, not by a two-element set.

    The previous form asserted `rc in (0, 2)`, and the 2026-09-11 Codex review of this
    branch is right that this was environment-dependent (HIGH-3): it passed whether the
    machine's two `CLAUDE_PROMPTS_DIR` scopes agreed or not, so it could not distinguish
    "the guard ran and passed" from "the guard ran and refused" -- nor catch a command
    that converted one into the other. Running the same module directly, through the same
    shell and the same `python`, makes the assertion deterministic under either ambient
    state: whatever the guard says, the hook must say the same thing.
    """
    direct = _run(
        f'python "{_REPO_ROOT.as_posix()}/scripts/fleet_health.py" --prompts-guard',
        cwd=_REPO_ROOT, project_dir=None,
    )
    hooked = _run(_hook_command(), cwd=_REPO_ROOT, project_dir=None)
    assert direct.returncode in (0, 2), (
        "the guard itself returned neither of its own documented codes, so this test "
        f"cannot bind the hook to it: rc={direct.returncode} stderr={direct.stderr!r}"
    )
    assert hooked.returncode == direct.returncode, (
        "the hook command did not return the real guard's verdict: "
        f"hook={hooked.returncode} guard={direct.returncode} stderr={hooked.stderr!r}"
    )
    assert "can't open file" not in hooked.stderr, hooked.stderr


def test_hook_command_names_the_guard_flag_and_the_guard_module():
    """The narrowing and the fallback must not have quietly retargeted the hook."""
    command = _hook_command()
    assert "--prompts-guard" in command
    assert "scripts/fleet_health.py" in command


# --- the matcher ------------------------------------------------------------------------

def test_matcher_is_not_match_all():
    matcher = _hook_matcher()
    assert matcher not in ("*", ""), (
        'matcher "*" refuses every tool class on an error, including ToolSearch -- '
        "which is the only route to the deferred tools that could undo it"
    )


def test_matcher_still_covers_every_class_a_stale_prompts_dir_makes_lie():
    matcher = _hook_matcher()
    missing = [tool for tool in _MUST_MATCH if not _matches(matcher, tool)]
    assert not missing, f"narrowed past the guard's own subject: {missing}"


def test_matcher_leaves_the_break_glass_reachable():
    matcher = _hook_matcher()
    gated = [tool for tool in _MUST_NOT_MATCH if _matches(matcher, tool)]
    assert not gated, (
        f"{gated} is gated -- a refusing guard would again leave no in-session escape"
    )
