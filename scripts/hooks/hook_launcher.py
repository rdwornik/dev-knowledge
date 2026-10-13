"""The ONE launcher every `.claude/settings.json` hook that must survive a foreign shell runs through.

WHY IT EXISTS ([#1001] nearest, batch BW lane `lane-bw-1001-hook-launcher`). Claude Code runs a
hook `command` through a POSIX shell with `CLAUDE_PROJECT_DIR` set; Copilot CLI honours the same
file but runs it through PowerShell on Windows and sets no `CLAUDE_PROJECT_DIR` (package T6). The
three hooks that had to work under both -- the PreToolUse scope guard and B1's two Stop gates --
each carried its own inline `python -c` program to find the repo root. This file replaces those
three programs: the settings command only has to FIND this file, and this file runs the hook.

THE DECLARED COMMAND (one shape for every entry; `tests/test_hook_launcher.py` pins it):

    uv run --locked python ${CLAUDE_PROJECT_DIR:+"$CLAUDE_PROJECT_DIR/scripts/hooks/hook_launcher.py"}
        $(git rev-parse --no-revs --no-flags -- ./$(git rev-parse --path-format=relative
        --show-toplevel)scripts/hooks/hook_launcher.py) -m os <target>

It is a polyglot: every construct in it means the same thing, or deliberately nothing, under
bash, pwsh and Windows PowerShell -- measured, not assumed (the test runs it through all three):

  * `${CLAUDE_PROJECT_DIR:+"..."}` -- bash: this file under the Claude Code project root, one
    quoted word, when the variable is set; nothing when it is not. PowerShell reads `${...}` as a
    braced variable NAME that is never defined, so the whole token is empty there.
  * `$(git rev-parse --no-revs --no-flags -- ./$(...)scripts/hooks/hook_launcher.py)` -- every
    shell: the inner call prints the worktree root RELATIVE to the cwd (`./`, `../`, ... -- no
    spaces, so the unquoted result never word-splits); the outer call echoes the joined path back
    only INSIDE a git tree, whether or not the file exists there, and prints nothing outside one.
    The leading `./` keeps PowerShell from splitting a bareword that would otherwise begin with
    `$(`.
  * `-m os <target>` -- when BOTH locators are empty (no project variable, cwd outside every git
    tree) python sees `python -m os <target>`: it runs the inert `os` module and exits 0 -- the
    hook ALLOWS, because nothing identifies a project to guard. When a locator is present, python
    runs this file and the words after it are this file's own argv.

So the outcomes are: a locator found and this file present -> the hook runs; a git tree that
does not carry this file -> python cannot open it and exits 2 (fail CLOSED, R96); no project at
all -> exit 0. Under bash with `CLAUDE_PROJECT_DIR` set the project copy wins (it is first on the
line), so a session whose cwd wandered into another checkout still runs ITS project's hooks.

HONEST COST. Bash evaluates the git locator even when `CLAUDE_PROJECT_DIR` already decided the
answer: no construct is evaluated by PowerShell yet skipped by bash, because PowerShell reads
every `${...}` as an empty variable, so the PowerShell-visible locator cannot sit inside a bash
`${VAR:-...}` default. Measured on the operator's box (Git Bash, 8 warm runs, scope guard, an
allowed Read): median 1.70s for the inline `python -c` launcher this replaces, 2.30s for this
shape -- the two git subshells. A host that runs hooks under bash without the variable needs
them anyway; the price is paid by the host that does not.

ARGV CONTRACT. The LAST argument is the hook script, repo-relative (`scripts/lane_end_guard.py`).
Everything before it is locator residue -- the git locator's path when bash also had the project
variable, and the `-m os` pair -- and is ignored. Keeping the target a literal repo path is what
lets `bounded_hook.POSTURES` (substring match) and the file-purpose graph see which hook an entry
runs.

The hook runs exactly as `python <target>` would run it: `__main__`, `sys.argv[0]` = the target,
its own directory first on `sys.path`, stdin/stdout/stderr and the exit code untouched. A target
that is not a file under this file's root is refused with exit 2 and the reason on stderr --
never a clean allow (R96).
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def resolve_target(argv: list[str], root: Path = ROOT) -> Path | None:
    """The hook script the LAST argv word names, under `root`; None when it is not a file there."""
    if not argv:
        return None
    target = (root / argv[-1]).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return None
    return target


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    target = resolve_target(args)
    if target is None:
        named = args[-1] if args else "<none>"
        print(f"hook_launcher: no hook script {named!r} under {ROOT} -- refusing (fail closed)",
              file=sys.stderr)
        return 2
    sys.argv = [str(target)]
    sys.path.insert(0, str(target.parent))
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
