"""The `PreToolUse` prompts-guard WIRING -- the hook object in `.claude/settings.json`.

`tests/test_fleet_health.py` covers the guard's verdict function. Nothing covered the
hook object that *invokes* it, and that is where MA-1 lived (`[#684]`): the command was
`python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`, and
`CLAUDE_PROJECT_DIR` is set by Claude Code and by nothing else. A reader that honours the
hook file without defining the variable expands it to empty, the interpreter cannot open
the path, it exits non-zero -- and a `PreToolUse` hook that exits non-zero REFUSES. Total
refusal of every tool call, attributed to the tool it blocked rather than to us
(`docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:83, pointer :105).

Five properties are asserted here. The first three are the two edits `[#684]` names;
the fourth was added by the 2026-09-11 Codex review of this branch:

* **The command resolves the repo root itself.** Measured 2026-09-11 by a throwaway child
  session: hook commands run through a POSIX shell (`bash.exe`) with cwd == the project
  directory, so a `${CLAUDE_PROJECT_DIR:-.}` default is both available and correct. The
  RED-first witness `[#684]`'s Done-when asks for is
  `test_hook_command_resolves_the_script_without_claude_project_dir`: delete the fallback
  and it fails.
* **A command that cannot resolve its script passes rather than refuses.** The audit's
  stated intent, verbatim: *"the prompts-guard resolves its own path and fails open on
  interpreter failure"* (REVIEW.md:102). This extends `prompts_guard()`'s own documented
  fail-open posture to the one failure it could not reach -- not being loaded at all.
* **The guard's own refusal code is the ONLY one that refuses.** `prompts_guard()`
  returns 0 or 2 and nothing else, so every other status is a failure to RUN it -- no
  interpreter, an import error -- and those fail open. Added by the third Codex pass of
  this branch, which found MA-1 surviving in exactly that gap.
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

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest


_REPO_ROOT = Path(__file__).resolve().parent.parent
_SETTINGS = _REPO_ROOT / ".claude" / "settings.json"

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
#: from a magic exit code. It used to be an exit of 7, but the command now maps every status
#: except the guard's own `2` to `0` (see `_REFUSES`), so a distinctive exit code can no
#: longer carry this signal -- and a marker on stdout is better evidence anyway: it says
#: WHICH file ran, not merely that something did.
_REACHED = "PROMPTS-GUARD-STANDIN-REACHED"
#: The guard's own refusal code, and now the ONLY code that refuses. A stand-in returning it
#: proves the command PROPAGATES a refusal rather than swallowing it -- hermetically, on any
#: platform, which the live-tree test cannot do because the User-scope half of the real
#: verdict is registry state this suite must not touch.
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


def _fake_tree(root: Path, code: int = 0) -> Path:
    """A tree shaped like this repo whose `scripts/fleet_health.py` announces that it RAN
    and then exits `code` -- `_REFUSES` for a guard that refuses, `1` for one that crashes."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts" / "fleet_health.py").write_text(
        f"import sys\nprint({_REACHED!r})\nsys.exit({code})\n", encoding="utf-8"
    )
    return root


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


def test_hook_command_fails_open_when_no_root_resolves(tmp_path):
    """REVIEW.md:102's stated intent -- *fails open on interpreter failure*.

    Variable unset AND cwd outside any checkout: the guard cannot run. It must PASS, not
    refuse. Closure number from the finding: *tool calls refused because the guard's own
    command could not start: every call in the session -> 0*.
    """
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(_hook_command(), cwd=elsewhere, project_dir=None)
    assert result.returncode == 0, (
        "an unresolvable guard refused instead of passing -- this is MA-1 itself: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )
    assert _REACHED not in result.stdout, (
        "nothing should have run: the pass must come from the existence legs, not from a "
        f"stand-in that executed anyway -- stdout={result.stdout!r}"
    )


def test_hook_command_fails_open_when_the_interpreter_is_unavailable(tmp_path):
    """RED-first witness for the third Codex pass's HIGH: MA-1 again, by a different
    missing piece.

    The two `[ -f ]` legs guard the SCRIPT's existence and said nothing about the
    INTERPRETER's. A reader whose environment has no usable `python` got a non-zero exit
    from the hook -- 127 -- and therefore TOTAL REFUSAL of every matching tool call: the
    exact failure this row exists to close, and a direct contradiction of the intent the
    audit states in its own words, *"fails open on interpreter failure"* (REVIEW.md:102).

    Reached hermetically by emptying PATH, so `python` cannot be found. The stand-in is the
    REFUSING one on purpose: even a tree whose guard would refuse must pass when the guard
    could not be RUN, or the fail-open posture is not the one that is documented.
    """
    tree = _fake_tree(tmp_path / "tree", code=_REFUSES)
    result = _run(_hook_command(), cwd=tree, project_dir=None, path="")
    assert _REACHED not in result.stdout, (
        "PATH was not actually emptied -- the interpreter ran, so this test is not "
        f"measuring what it claims: stdout={result.stdout!r}"
    )
    assert result.returncode == 0, (
        "no usable interpreter REFUSED every matching tool call instead of passing -- this "
        f"is MA-1 by another name: rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_fails_open_when_the_guard_crashes(tmp_path):
    """The other half of "interpreter failure": the module is found and the interpreter
    starts, then dies on import or syntax. `prompts_guard()` returns 0 or 2 and NOTHING
    else, so a `1` cannot be a verdict -- it can only be a crash, and a crashing guard must
    not brick the session. Only the guard's own `2` refuses."""
    tree = _fake_tree(tmp_path / "tree", code=1)
    result = _run(_hook_command(), cwd=tree, project_dir=None)
    assert _REACHED in result.stdout, "the stand-in did not run, so this proves nothing"
    assert result.returncode == 0, (
        "a crashing guard refused instead of passing: "
        f"rc={result.returncode} stderr={result.stderr!r}"
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
