"""The `PreToolUse` prompts-guard WIRING -- the hook object in `.claude/settings.json`.

`tests/test_fleet_health.py` covers the guard's verdict function. Nothing covered the
hook object that *invokes* it, and that is where MA-1 lived (`[#684]`): the command was
`python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`, and
`CLAUDE_PROJECT_DIR` is set by Claude Code and by nothing else. A reader that honours the
hook file without defining the variable expands it to empty, the interpreter cannot open
the path, it exits non-zero -- and a `PreToolUse` hook that exits non-zero REFUSES. Total
refusal of every tool call, attributed to the tool it blocked rather than to us
(`docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:83, pointer :105).

Four properties are asserted here. The first three are the two edits `[#684]` names;
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
_MUST_NOT_MATCH = ("ToolSearch", "ExitWorktree", "SendMessage")

_SH = shutil.which("bash") or shutil.which("sh")

#: Outside every code the real guard returns (0 pass / 2 refuse), so a test asserting it is
#: asserting "the command reached the script at this root" and nothing else.
_REACHED = 7
#: The guard's own refusal code. A stand-in returning it proves the command string
#: PROPAGATES a refusal rather than swallowing it -- hermetically, on any platform, which
#: the live-tree test cannot do because the User-scope half of the verdict is registry state.
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


def _fake_tree(root: Path, code: int = _REACHED) -> Path:
    """A tree shaped like this repo whose `scripts/fleet_health.py` only reports that it
    RAN -- or, at `code=_REFUSES`, one that stands in for a guard that REFUSES."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts" / "fleet_health.py").write_text(
        f"import sys\nsys.exit({code})\n", encoding="utf-8"
    )
    return root


def _run(command: str, *, cwd: Path, project_dir):
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    if project_dir is not None:
        env["CLAUDE_PROJECT_DIR"] = project_dir
    assert _SH is not None, (
        "no POSIX shell on PATH -- Claude Code runs hook commands through one (measured "
        "2026-09-11: C:/Program Files/Git/bin/bash.exe), so this hook cannot run here"
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
    assert result.returncode == _REACHED, (
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
    assert result.returncode == _REACHED, (
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
    assert result.returncode == _REACHED, (
        "a wrong CLAUDE_PROJECT_DIR fell through to fail-open instead of trying cwd, so "
        "a resolvable guard went unconsulted: "
        f"rc={result.returncode} stderr={result.stderr!r}"
    )


def test_hook_command_falls_back_to_cwd_when_claude_project_dir_is_set_empty(tmp_path):
    """Set-but-empty is the shape a harness that *exports* the variable without a value
    produces. `:-` (not `-`) is what makes it take the default, so this pins the colon."""
    tree = _fake_tree(tmp_path / "tree")
    result = _run(_hook_command(), cwd=tree, project_dir="")
    assert result.returncode == _REACHED, (
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
    assert result.returncode == _REACHED, (
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
