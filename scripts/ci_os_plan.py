#!/usr/bin/env python
"""ci_os_plan -- which OS legs a merge needs (ADR-127 AMENDMENT 2, Linux-first CI, 2026-10-16).

THE RULING (operator, 2026-10-16, by `to-cc/BATCH-LINUX-FIRST-CI-2026-10-16.md`, reinstating R111
which R116 withdrew on cost alone): a merge to main is judged on the Linux leg only. The Windows
leg runs (a) nightly on main, full suite -- the workflow's `schedule` / `workflow_dispatch`
events -- and (b) on a merge whose diff touches a Windows-sensitive path. This module is the ONE
place that decides (b). Two readers call it and nothing else, so they cannot disagree:
  * `.github/workflows/conductor.yml`'s `plan` job (CLI below) -> the `pytest` matrix `os` list;
  * `merge_path.land` -> `actions_verdict.required_contexts_for` -> whether `pytest (windows-latest)`
    is a context the verdict must see `success`.
When the diff cannot be read, Windows is required: an unreadable diff is never a licence to skip.

THE SENSITIVE LIST IS DERIVED FROM THE REPO, NOT INVENTED. Three sources, each quoted:
  1. THE ORDER'S OWN CATEGORIES -- "hooks, encoding or newline writers, path handling,
     PowerShell, `.gitattributes`" -- as paths: `.gitattributes` (whose header says "PowerShell
     scripts check out CRLF (Windows-native)"), every `*.ps1`/`*.psm1`/`*.psd1`, the hook
     scripts `scripts/hooks/`, the hook wiring `.claude/settings.json` and
     `.pre-commit-config.yaml`, and the workflow directory that defines the matrix itself.
  2. THE KNOWN-REDS REGISTRY'S WINDOWS-ONLY MEMBERS (`logs/KNOWN-REDS-REGISTRY.json`,
     `members_by_os`): a test red on `windows-latest` and absent from `ubuntu-latest`. Its test
     file and every `scripts/…`/`tests/…` file its `reason` names are sensitive. Today that is
     `tests/test_transport.py` and `scripts/transport.py` ("foundation-8 cause SHOWN, in
     scripts/transport.py … on Windows os.open(O_CREAT|O_EXCL) … raises PermissionError").
  3. EVERY PYTHON FILE THAT BRANCHES ON THE PLATFORM -- `PLATFORM_BRANCH_PATTERN`, searched with
     `git grep` over `scripts/`, `deploy/`, `plugins/` at both ends of the diff (ADR-127 Context:
     "every `os.name` site in `scripts/` had a POSIX arm (not all proven working)"). That is the
     path-handling / encoding / newline / lock surface, found by what the code says, not by a
     list someone has to remember to extend.

HONEST LIMIT. A Windows-only break in a file none of the three sources names is found by the
nightly leg, not by the merge. That is the ruling's price: a Windows red found at night becomes
a row the next morning and does not block the day.

THE TEST SELECTION PER LEG (e2-os-split). Which tests a leg runs is decided here too, as a pytest
marker expression (`selection`): Ubuntu runs `not windows_only` (every test that cannot skip on
Ubuntu by platform); Windows on `schedule` / `workflow_dispatch` runs the full suite (`""`, the
nightly is unchanged); Windows on any other event (a Windows-sensitive landing) runs
`windows_only or windows_smoke` only. The markers are data in tests/conftest.py
(`WINDOWS_ONLY_TESTS`, the `windows_smoke` tests), not logic here.

CLI (the workflow): `python3 scripts/ci_os_plan.py --event E --head SHA [--before SHA]` writes
`os=["ubuntu-latest"]` or `os=["ubuntu-latest","windows-latest"]`, `reason=…`, `base=…`,
`m_ubuntu=…` and `m_windows=…` (possibly empty) to `$GITHUB_OUTPUT`. Stdlib only: the plan job
runs before any `uv sync`.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

LINUX = "ubuntu-latest"
WINDOWS = "windows-latest"
#: Events on which the full matrix runs: the nightly `schedule` and a hand-dispatched run (the
#: remedy when a landing is refused for a missing Windows leg).
FULL_MATRIX_EVENTS = ("schedule", "workflow_dispatch")

MARK_WINDOWS_ONLY = "windows_only"
MARK_WINDOWS_SMOKE = "windows_smoke"

REGISTRY_RELPATH = "logs/KNOWN-REDS-REGISTRY.json"

#: Source 1. fnmatch patterns against a repo-relative posix path; `*` crosses `/`.
STATIC_PATTERNS = (
    ".gitattributes",
    "*.ps1", "*.psm1", "*.psd1",
    "scripts/hooks/*",
    ".claude/settings.json",
    ".pre-commit-config.yaml",
    ".github/workflows/*",
)

#: Source 3. ERE for `git grep -E`; no `\b` so it behaves the same on every git build.
PLATFORM_BRANCH_PATTERN = (r"os\.name|sys\.platform|platform\.system|msvcrt|win32|PermissionError"
                           r"|powershell|pwsh")
PLATFORM_SCAN_PATHSPECS = ("scripts/*.py", "deploy/*.py", "plugins/*.py")

_NAMED_FILE_RE = re.compile(r"\b(?:scripts|tests|deploy)/[\w./-]+?\.py\b")

GitFn = Callable[[list], "tuple[int, str]"]


def run_git(root: Path) -> GitFn:
    """The production git runner: `(returncode, stdout)`, never raising."""
    def run(args: list) -> "tuple[int, str]":
        try:
            done = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=120)
        except (OSError, subprocess.SubprocessError) as exc:
            return 1, str(exc)
        return done.returncode, done.stdout
    return run


def registry_windows_only_files(registry_text: str) -> frozenset:
    """Source 2: the test files, and the files their `reason` names, of every member red on
    windows-latest and not on ubuntu-latest. Raises ValueError on text that is not a registry
    carrying `members_by_os` as an object: a registry that cannot be read is a failed scan (the
    caller fails closed), never an empty sensitive set."""
    try:
        by_os = json.loads(registry_text)["members_by_os"]
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError(f"{REGISTRY_RELPATH} is not a readable registry: {exc}") from exc
    if not isinstance(by_os, dict):
        raise ValueError(f"{REGISTRY_RELPATH}: members_by_os is not an object")
    windows = by_os.get(WINDOWS) or {}
    linux = by_os.get(LINUX) or {}
    files: set = set()
    for node_id, entry in windows.items():
        if node_id in linux:
            continue
        files.add(node_id.split("::", 1)[0])
        files.update(_NAMED_FILE_RE.findall(str((entry or {}).get("reason", ""))))
    return frozenset(files)


def platform_branching_files(git: GitFn, ref: str) -> frozenset:
    """Source 3 at `ref`. `git grep` exits 1 on no match, which is an empty set, not an error."""
    code, out = git(["grep", "-l", "-E", PLATFORM_BRANCH_PATTERN, ref, "--", *PLATFORM_SCAN_PATHSPECS])
    if code not in (0, 1):
        raise RuntimeError(f"git grep failed ({code}): {out.strip()[:160]}")
    prefix = f"{ref}:"
    return frozenset(line[len(prefix):] if line.startswith(prefix) else line
                     for line in out.splitlines() if line.strip())


def sensitive_files(git: GitFn, *refs: str) -> frozenset:
    """Sources 2 and 3 read at every `ref` (both ends of a diff, so a deleted file still counts)."""
    found: set = set()
    for ref in refs:
        found |= platform_branching_files(git, ref)
        code, text = git(["show", f"{ref}:{REGISTRY_RELPATH}"])
        if code != 0:
            raise RuntimeError(f"{REGISTRY_RELPATH} could not be read at {ref} ({code})")
        found |= registry_windows_only_files(text)
    return frozenset(found)


def why_sensitive(changed: list, derived: frozenset) -> list:
    """`"<path> (<source>)"` for every changed path that is Windows-sensitive; [] when none is."""
    reasons = []
    for path in changed:
        posix = path.replace("\\", "/")
        pattern = next((p for p in STATIC_PATTERNS if fnmatch.fnmatchcase(posix, p)), None)
        if pattern:
            reasons.append(f"{posix} (static: {pattern})")
        elif posix in derived:
            reasons.append(f"{posix} (derived: registry windows-only member or platform-branching code)")
    return reasons


def changed_paths(git: GitFn, base: str, head: str) -> Optional[list]:
    """Paths changed `base..head`, or None when git could not say (the caller fails closed)."""
    code, out = git(["diff", "--name-only", base, head])
    if code != 0:
        return None
    return [line.strip() for line in out.splitlines() if line.strip()]


def windows_reasons(git: GitFn, base: str, head: str) -> list:
    """The reasons Windows is required for `base..head`. Empty means Linux alone judges it. An
    unreadable diff or scan is itself a reason."""
    try:
        changed = changed_paths(git, base, head)
        if changed is None:
            return ["the diff could not be read (fail closed)"]
        return why_sensitive(changed, sensitive_files(git, base, head))
    except (RuntimeError, OSError, ValueError) as exc:
        return [f"the sensitive-path scan failed: {exc} (fail closed)"]


def windows_required(git: GitFn, base: str, head: str) -> bool:
    return bool(windows_reasons(git, base, head))


def resolve_base(event: str, git: GitFn, head: str, before: Optional[str],
                 main_ref: str) -> Optional[str]:
    """The sha a run's diff (and the `windows-gate`'s known-reds compare) is taken against, or
    None: `github.event.before` for a push to main, else merge-base(origin/main, head)."""
    if event == "push" and main_ref == "refs/heads/main":
        return before if before and set(before) != {"0"} else None
    code, out = git(["merge-base", "origin/main", head])
    return out.strip() if code == 0 and out.strip() else None


def plan(event: str, git: GitFn, head: str, before: Optional[str], main_ref: str) -> "tuple[list, str]":
    """`(os_list, reason)` for one workflow run."""
    if event in FULL_MATRIX_EVENTS:
        return [LINUX, WINDOWS], f"{event}: the full matrix runs (nightly / manual)"
    base = resolve_base(event, git, head, before, main_ref)
    if not base:
        return [LINUX, WINDOWS], "no diff base could be resolved (fail closed)"
    reasons = windows_reasons(git, base, head)
    if reasons:
        shown = "; ".join(reasons[:5]) + (f"; +{len(reasons) - 5} more" if len(reasons) > 5 else "")
        return [LINUX, WINDOWS], f"Windows-sensitive diff: {shown}"
    return [LINUX], "no Windows-sensitive path in the diff: Linux alone judges this merge"


def selection(event: str, os_name: str) -> str:
    """The pytest `-m` expression for one OS leg of one event ("" = the full suite)."""
    if os_name == LINUX:
        return f"not {MARK_WINDOWS_ONLY}"
    if event in FULL_MATRIX_EVENTS:
        return ""
    return f"{MARK_WINDOWS_ONLY} or {MARK_WINDOWS_SMOKE}"


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--event", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--before", default=None, help="github.event.before (a push to main)")
    ap.add_argument("--ref", default="", help="github.ref")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    git = run_git(Path(args.root))
    os_list, reason = plan(args.event, git, args.head, args.before, args.ref)
    base = (args.head if args.event == "schedule"      # the nightly head IS main: no git call needed
            else resolve_base(args.event, git, args.head, args.before, args.ref) or "")
    lines = [f"os={json.dumps(os_list)}", f"reason={reason}", f"base={base}",
             f"m_ubuntu={selection(args.event, LINUX)}",
             f"m_windows={selection(args.event, WINDOWS)}"]
    for line in lines:
        print(line)
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    sys.exit(main())
