#!/usr/bin/env python
"""reuse_gate.py -- PreToolUse reuse gate: a lane may not create a new file under `scripts/` or `.claude/` that its contract does not name and no `why` search covers.

WHY IT EXISTS (`[#735]` nearest; R96 D7, package T5.2; batch BW lane `lane-bw-735-reuse-gate`). The
manifest's lane rule 2 says *before creating any file, run `file_purpose_graph.py why <neighbour>`;
a new file is allowed only where the contract names it*. That rule was prose a lane could skip.
This hook is the mechanism: a Write/Edit/MultiEdit/NotebookEdit call whose target does NOT exist
yet and sits under `scripts/` or `.claude/` is DENIED unless

  (a) the active lane contract's `## Done-contract` section names the path -- or names its
      directory, when that directory is strictly below the guarded root (naming `scripts/` itself
      would name the whole zone); a path the contract itself calls *unnamed* ("an unnamed
      `scripts/x_probe.py`") is not a naming; OR
  (b) a `why` record exists for a NEIGHBOUR: a file in the same directory (or the directory).

THE RECORD (defined here; the existing receipt home is reused). `file_purpose_graph.py why`
appends one JSON line per search to `WHY-SEARCHES.jsonl` in the lane's receipts directory --
`$HARNESS_RECEIPTS_DIR`, else `<root>/logs/receipts/` (gitignored), the home `lane_end_guard.py`
already writes its receipts to. A refused `why` is recorded too: the search is what the rule asks
for, and "nothing explains this file" is an answer. Each line carries `lane`, `path`, `outcome`,
`session` and `at`. The gate counts a record of THIS lane only. It does not filter on `session`:
`CLAUDE_CODE_SESSION_ID` is inherited by child hosts (measured in-lane 2026-10-13: a `copilot -p`
child carried its parent's id while its own hook payload carried its own), so a session-keyed
match would refuse the very search a child just ran. The lane worktree is the session boundary --
one checkout is one committing session (AGENTS.md), and the receipts directory dies with it.

THE ACTIVE CONTRACT. The lane slug is `lane_end_guard.resolve_lane` (`$HARNESS_LANE`, else the
worktree directory name under `.claude/worktrees/`); its contract file is
`gen_lane_contract.contract_filename(slug)`, looked up in the in-tree frozen bundles
`docs/audits/*-launch-contracts/` (newest bundle wins). Both helpers are imported lazily, only once
a call is a real candidate, so an ordinary Write pays only the stdlib prefilter.

NEVER A WEDGE. Outside a lane (no slug), or in a worktree with no contract on disk (an integration
worktree), the rule ALLOWS and LOGS. Any error inside the gate allows and logs (posture fail-open,
`bounded_hook.POSTURES` "reuse-gate"). `DEV_KNOWLEDGE_REUSE_GATE_DISABLE=1` allows every call, and
says so on stderr.

THE WIRE. To DENY it prints Claude Code's documented PreToolUse form on stdout and exits 0:
`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
"permissionDecisionReason": <one line>}}`. Not the `scope_guard.py` wire (`{"decision":"block"}` +
exit 2): measured in-lane 2026-10-13 against Copilot CLI 1.0.96, which honours this file's hooks,
an exit 2 is denied as "hook errored" and the reason never reaches the model, while this JSON form
reaches it verbatim ("Denied by preToolUse hook: <reason>"). Item 3's remedy line is only a remedy
if the agent can read it. To ALLOW it exits 0 silently. Registered in `.claude/settings.json`
through the shared launcher `scripts/hooks/hook_launcher.py` (matcher
`Write|Edit|MultiEdit|NotebookEdit`).

A TEST RUN NEVER WRITES THE LIVE RECORD. A test that runs `why` in a lane worktree
(`test_deny_and_point.py` executes `why scripts/gen_task_tree.py` against the real tree) would
otherwise leave a record that silently opens the gate for `scripts/` -- measured in-lane: it did,
and the R8 usage probe was wrongly allowed. So under pytest (`PYTEST_CURRENT_TEST`, which pytest
exports and subprocesses inherit) `record_why` writes only when `$HARNESS_RECEIPTS_DIR` redirects
the home.

HONEST LIMIT. It reads the tool call's target path only: a file created by a Bash/PowerShell
command (`>`, `New-Item`) is not seen -- the Done-contract binds Write/Edit calls, and parsing
shell redirections is the scope guard's heavier machinery, not this gate's.

FLOOR: hub-only. One-line reason: it reads the hub's in-tree launch-contract bundles and FPG-1,
neither of which a consumer repo carries.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = REPO_ROOT / "scripts"

LOG = logging.getLogger("reuse_gate")

#: The wedge escape: allows every call, checked first.
DISABLE_ENV = "DEV_KNOWLEDGE_REUSE_GATE_DISABLE"
_TRUE = frozenset({"1", "true", "yes", "on"})

#: The zone. A new file below either root is a candidate; everything else is allowed.
GUARDED_ROOTS = ("scripts", ".claude")
#: The tools that create or change a file. `Edit` on a missing file is treated as a create.
WRITE_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})
#: `file_path` (Claude Code), `notebook_path` (NotebookEdit), `path` (Copilot CLI's Write).
PATH_FIELDS = ("file_path", "notebook_path", "path")

#: The record, in the lane's receipts directory.
WHY_RECORD_NAME = "WHY-SEARCHES.jsonl"
_CONTRACT_GLOB = "docs/audits/*-launch-contracts/{name}"

_DONE_HEADING = re.compile(r"^##\s+Done[- ]contract\b.*$", re.IGNORECASE | re.MULTILINE)
_NEXT_HEADING = re.compile(r"^##\s", re.MULTILINE)
_PATH_TOKEN = re.compile(r"[\w.\-/]+")
_UNNAMED = re.compile(r"\b(unnamed|not\s+named|does\s+not\s+name)\b[^\n`]{0,20}`?$", re.IGNORECASE)


# --------------------------------------------------------------------------------- the lane

def _import_scripts_module(name: str):
    if str(_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS))
    return __import__(name)


def lane_of(root: Path, environ: Mapping[str, str]) -> str:
    """This checkout's lane slug, or '' -- `lane_end_guard.resolve_lane`, not a second copy."""
    return _import_scripts_module("lane_end_guard").resolve_lane(environ, root)


def receipts_dir(root: Path, environ: Mapping[str, str]) -> Path:
    """The receipt home `lane_end_guard.py` already uses: `$HARNESS_RECEIPTS_DIR`, else
    `<root>/logs/receipts`."""
    return Path(environ.get("HARNESS_RECEIPTS_DIR") or root / "logs" / "receipts")


def contract_path(root: Path, lane: str) -> Optional[Path]:
    """The lane's frozen contract in the newest in-tree launch-contracts bundle, or None."""
    name = _import_scripts_module("gen_lane_contract").contract_filename(lane)
    found = sorted(root.glob(_CONTRACT_GLOB.format(name=name)))
    return found[-1] if found else None


def done_contract(text: str) -> str:
    """The `## Done-contract` section; the whole text when a contract carries no such heading."""
    head = _DONE_HEADING.search(text)
    if head is None:
        return text
    rest = text[head.end():]
    nxt = _NEXT_HEADING.search(rest)
    return rest[: nxt.start()] if nxt else rest


def named_paths(section: str) -> set[str]:
    """Every path-shaped token the section names, minus the ones it calls unnamed."""
    section = section.replace("\\", "/")
    names: set[str] = set()
    for match in _PATH_TOKEN.finditer(section):
        token = match.group(0).rstrip(".,/").removeprefix("./")
        if "/" not in token:
            continue
        if _UNNAMED.search(section[max(0, match.start() - 40): match.start()]):
            continue
        names.add(token)
    return names


def _contract_names(rel: str, names: set[str]) -> bool:
    if rel in names:
        return True
    parent = rel.rsplit("/", 1)[0]
    return parent.count("/") >= 1 and parent in names   # strictly below `scripts/` / `.claude/`


# --------------------------------------------------------------------------------- the record

def record_why(root: Path, path: str, outcome: str,
               environ: Mapping[str, str] = os.environ) -> Optional[Path]:
    """Append one `why` search to the lane's record; None (nothing written) outside a lane, or
    under a test run that has not redirected the receipts home.

    Called by `file_purpose_graph.py why`, the record's one producer."""
    if environ.get("PYTEST_CURRENT_TEST") and not environ.get("HARNESS_RECEIPTS_DIR"):
        return None
    lane = lane_of(root, environ)
    if not lane:
        return None
    home = receipts_dir(root, environ)
    home.mkdir(parents=True, exist_ok=True)
    line = {"lane": lane, "path": path.replace("\\", "/").removeprefix("./"), "outcome": outcome,
            "session": environ.get("CLAUDE_CODE_SESSION_ID"),
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    target = home / WHY_RECORD_NAME
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=True) + "\n")
    return target


def _neighbour_searched(root: Path, environ: Mapping[str, str], lane: str, rel: str) -> bool:
    parent = rel.rsplit("/", 1)[0]
    try:
        lines = (receipts_dir(root, environ) / WHY_RECORD_NAME).read_text(encoding="utf-8")
    except OSError:
        return False
    for raw in lines.splitlines():
        try:
            rec = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(rec, dict) or rec.get("lane") != lane:
            continue
        searched = str(rec.get("path", "")).rstrip("/")
        if searched == parent or (searched.rsplit("/", 1)[0] == parent and searched != rel):
            return True
    return False


# --------------------------------------------------------------------------------- the decision

def _target(payload: dict, root: Path) -> Optional[tuple[Path, str]]:
    """(absolute target, repo-relative posix path) of a write under the guarded roots, else None."""
    tool_input = payload.get("tool_input")
    if payload.get("tool_name") not in WRITE_TOOLS or not isinstance(tool_input, dict):
        return None
    raw = next((tool_input[f] for f in PATH_FIELDS if isinstance(tool_input.get(f), str)), None)
    if not raw:
        return None
    cwd = payload.get("cwd")
    base = Path(cwd) if isinstance(cwd, str) and cwd else root
    target = Path(os.path.abspath(base / raw))
    try:
        rel = Path(os.path.relpath(target, root)).as_posix()
    except ValueError:                                    # another drive
        return None
    if rel.startswith("../") or rel == ".." or "/" not in rel:
        return None
    if rel.split("/", 1)[0].lower() not in GUARDED_ROOTS:
        return None
    return target, rel


def _neighbour(root: Path, rel: str) -> str:
    """An existing file beside `rel` to run `/why` on -- else its nearest existing directory."""
    parent = rel.rsplit("/", 1)[0]
    directory = root / parent
    siblings = sorted(p.name for p in directory.iterdir() if p.is_file()) if directory.is_dir() else []
    if siblings:
        return f"{parent}/{siblings[0]}"
    while parent.count("/") and not (root / parent).is_dir():
        parent = parent.rsplit("/", 1)[0]
    return parent


def _denied(rel: str, contract_rel: str, neighbour: str) -> str:
    folder = rel.rsplit("/", 1)[0]
    return (f"DENIED (reuse gate, R96 D7): new file {rel} is not named by {contract_rel}'s "
            f"Done-contract and no why search covers its neighbours -- run `/why {neighbour}` "
            f"(uv run --locked python scripts/file_purpose_graph.py why {neighbour}; any file in "
            f"{folder}/ counts) first, or name the file in the contract.")


def decide(payload: object, root: Path = REPO_ROOT,
           environ: Mapping[str, str] = os.environ) -> tuple[str, str]:
    """('block'|'allow', reason). Every error path allows and logs -- never a wedge."""
    if str(environ.get(DISABLE_ENV, "")).strip().lower() in _TRUE:
        LOG.info("reuse-gate: %s is set -- this call was NOT evaluated", DISABLE_ENV)
        return "allow", "gate disabled by the operator-settable switch"
    if not isinstance(payload, dict):
        return "allow", "unrecognised payload"
    try:
        found = _target(payload, root)
        if found is None:
            return "allow", "not a write under scripts/ or .claude/"
        target, rel = found
        if target.exists():
            return "allow", "an edit to an existing file"
        lane = lane_of(root, environ)
        if not lane:
            LOG.info("reuse-gate: allow %s -- no active lane in %s (allow-and-log)", rel, root)
            return "allow", "no active lane"
        contract = contract_path(root, lane)
        if contract is None:
            LOG.info("reuse-gate: allow %s -- no active lane contract for %s (allow-and-log)",
                     rel, lane)
            return "allow", "no active lane contract"
        if _contract_names(rel, named_paths(done_contract(contract.read_text(encoding="utf-8")))):
            return "allow", "the lane contract names this file"
        if _neighbour_searched(root, environ, lane, rel):
            return "allow", "a why search covers a neighbour"
        contract_rel = contract.relative_to(root).as_posix()
        return "block", _denied(rel, contract_rel, _neighbour(root, rel))
    except Exception as exc:  # noqa: BLE001 -- fail OPEN: a broken gate must not wedge a session
        LOG.warning("reuse-gate: could not evaluate (%r) -- allowing", exc)
        return "allow", "the gate could not evaluate"


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:  # noqa: BLE001 -- unparseable payload: nothing to judge
        payload = None
    decision, reason = decide(payload, REPO_ROOT, os.environ)
    if decision == "block":
        sys.stdout.write(json.dumps(deny_output(reason), ensure_ascii=True) + "\n")
    return 0


def deny_output(reason: str) -> dict:
    """The PreToolUse deny both Claude Code and Copilot CLI read (see THE WIRE)."""
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": reason}}


if __name__ == "__main__":
    sys.exit(main())
