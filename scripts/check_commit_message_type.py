#!/usr/bin/env python
"""commit-msg hook ([#834]).

`protocols/PLAYBOOK.md` "### Commit message standard" states Conventional Commits
(`type(scope): summary`) as the required shape and until this row nothing refused a
violation -- the rule was carried by that heading, by CONTRIBUTING.md's live examples,
and by `/save`'s own template, and zero organs. Measured with
`git log --all --no-merges --format='%H %s'` filtered for `Revert "`/`Merge ` (git's own
auto-generated shapes, out of scope) and the stash/worktree synthetic entries `git status`
surfaces as pseudo-commits: 15 real breaches, all from the pre-formalization era (the
`[ADR-30]`/`@ docs(...)` commit streams) -- refs `docs/audits/2026-09-16-technical-lane-ab-834-protocols-heading-gate.md`
for the full table.

Deliberately narrow: this checks the STRUCTURAL shape (a leading `type` token, optional
`(scope)`, optional `!`, then `: `) -- not the closed six-type enum PLAYBOOK's prose
names (`feat fix docs refactor test chore`). Live practice already extends that enum
(`perf`, `build`, `lessons` -- the last sanctioned by `~/.claude/rules/git-discipline.md`
for LESSONS.md appends) without anyone treating it as a violation, so gating the literal
enum would refuse sanctioned commits on day one. Gating the 72-char summary-length
sub-rule was considered and rejected for the same reason (5680/7985 historical commits
exceed it, including commits that comply with this repo's own `[#id]`-citation
conventions) -- see the artifact's "Top pick and the caveat" section.

Read-only: reads only the message file; never writes, never touches the diff.

Wired via `.pre-commit-config.yaml` `stages: [commit-msg]`; install with
`pre-commit install --hook-type commit-msg`.
"""

from __future__ import annotations

import re
import sys

_TYPE_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.-]*(\([^)]*\))?!?: ")
_EXEMPT_PREFIXES = ("Merge ", 'Revert "', "fixup!", "squash!")


def _subject(msg: str) -> str:
    stripped = msg.strip("\n")
    for line in stripped.splitlines():
        if line.strip():
            return line
    return ""


def check(msg: str) -> bool:
    """Return True if the commit message's subject conforms (or is exempt); False = violation."""
    subject = _subject(msg)
    if not subject:
        return True  # empty message is a different gate's problem
    if subject.startswith(_EXEMPT_PREFIXES):
        return True
    return bool(_TYPE_RE.match(subject))


def main():
    if len(sys.argv) < 2:
        return 0
    try:
        msg = open(sys.argv[1], encoding="utf-8").read()
    except OSError:
        return 0
    if not check(msg):
        subject = _subject(msg)
        print(
            f"commit-msg: subject line has no Conventional Commits type prefix: {subject!r}",
            file=sys.stderr,
        )
        print(
            "  Use 'type(scope): summary' (types: feat fix docs refactor test chore, "
            "or an established extension e.g. perf/build/lessons). "
            "PLAYBOOK.md 'Commit message standard'.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
