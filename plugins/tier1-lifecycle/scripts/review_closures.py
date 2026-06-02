#!/usr/bin/env python
"""review_closures.py — ADR-70 Tier-1 reviewer-side gate (the review half of Unit 2).

READ-ONLY on governed state. This module reads `logs/PROPOSALS-*.md` (Unit-2
output), BACKLOG.md, and git, and emits a re-verified **closure plan**. It does
NOT write BACKLOG.md and does NOT commit — those mutations are performed by the
human-gated `/review-closures` command (the agent), keeping `scripts/` read-only
on governed state per CLAUDE §5 #4 / §10. The tested safety logic lives here; the
agent only mechanically applies the exact lines this gate verifies.

Two CLI modes:
  surface   — SessionStart: print a one-line summary if the latest proposals file
              has candidates; silent (and exit 0) otherwise. No mutation.
  plan      — given the operator-approved ids, re-verify each and print a JSON plan
              {"close": [...], "skip": [...]}. Read-only.

Safety contract (the first contract-driven backlog mutation):
  - Closes ONLY ids passed in (the agent passes ONLY what the operator explicitly
    approved — STRONG together via `y`, WEAK one typed `#N` at a time).
  - Re-verify at plan time (proposals may be stale): an approved id must be
    CURRENTLY open in BACKLOG; a STRONG id must ALSO still have a live evidence
    commit. Fail re-verify -> skip + report, never close.
  - Emits the exact verbatim task line so the agent's removal Edit is exact-match
    (the Edit tool fails on any mismatch — a third safety net after human approval
    and re-verify; the `backlog-id-on-close` commit-msg hook is a fourth).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def _host_root() -> Path:
    """Host repo root (where BACKLOG.md / logs/ / .git live).

    PLUGIN PORTABILITY: this script lives under ${CLAUDE_PLUGIN_ROOT}, NOT in the
    host repo, so the data root must come from $CLAUDE_PROJECT_DIR (set by Claude
    Code for every hook/command), not from __file__. Falls back to cwd for manual
    or test invocation. `_SCRIPTS_DIR` stays __file__-relative — it locates the
    plugin-bundled validate_backlog.py, which is a different root.
    """
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env).resolve() if env else Path.cwd().resolve()


_SCRIPTS_DIR = Path(__file__).resolve().parent  # plugin's own dir (bundled validate_backlog)
_REPO_ROOT = _host_root()
_BACKLOG = _REPO_ROOT / "BACKLOG.md"
_LOGS_DIR = _REPO_ROOT / "logs"

_HEAD_RE = re.compile(r"head_commit:\s*([0-9a-fA-F]{7,40})")
_ITEM_RE = re.compile(r"^- \[ \] \*\*#(\d+)\*\*")
_STRONG_EV_RE = re.compile(r"^\s*- evidence:\s*`([0-9a-fA-F]{7,40})`")
_WEAK_EV_RE = re.compile(r"^\s*- evidence:\s*`([^`]+)`\s+changed in\s+`([0-9a-fA-F]{7,40})`")


# ---------------------------------------------------------------------------
# Pure parsing + planning (no git, no I/O — unit-tested directly)
# ---------------------------------------------------------------------------

def parse_proposals(text: str) -> dict:
    """Parse a PROPOSALS-*.md into {head_commit, strong{id:[sha]}, weak{id:[(path,sha)]}}.

    Mirror of propose_closures.render(); a round-trip test guards the contract.
    """
    head = _HEAD_RE.search(text)
    result = {
        "head_commit": head.group(1) if head else None,
        "strong": {},
        "weak": {},
    }
    section = None  # "strong" | "weak" | None
    cur_id = None
    for raw in text.splitlines():
        if raw.startswith("## STRONG"):
            section, cur_id = "strong", None
            continue
        if raw.startswith("## WEAK"):
            section, cur_id = "weak", None
            continue
        if raw.startswith("## "):  # any other section ends candidate parsing
            section, cur_id = None, None
            continue
        if section is None:
            continue
        item = _ITEM_RE.match(raw)
        if item:
            cur_id = item.group(1)
            result[section].setdefault(cur_id, [])
            continue
        if cur_id is None:
            continue
        if section == "strong":
            m = _STRONG_EV_RE.match(raw)
            if m:
                result["strong"][cur_id].append(m.group(1))
        else:
            m = _WEAK_EV_RE.match(raw)
            if m:
                result["weak"][cur_id].append((m.group(1), m.group(2)))
    return result


def candidate_count(proposals: dict) -> int:
    return len(proposals.get("strong", {})) + len(proposals.get("weak", {}))


def surface_line(proposals: dict) -> str | None:
    """One-line SessionStart summary, or None when there is nothing to review."""
    n_s = len(proposals.get("strong", {}))
    n_w = len(proposals.get("weak", {}))
    if n_s + n_w == 0:
        return None
    parts = []
    if n_s:
        parts.append(f"{n_s} strong")
    if n_w:
        parts.append(f"{n_w} weak")
    # Plain ASCII only — this prints from a SessionStart hook into a console that
    # may be cp1252; a non-ASCII dash would mojibake (the §4 render-layer caveat).
    return (f"[closures] {' + '.join(parts)} closure(s) proposed "
            f"({n_s + n_w} item(s)) -- run /review-closures to review.")


def plan_closures(backlog_text: str, approved_ids, proposals: dict,
                  open_lines: dict, evidence_exists) -> dict:
    """Re-verify approved ids against current state. Pure.

    open_lines: {id: exact_raw_backlog_line} for currently-open tasks.
    evidence_exists: callable(sha)->bool (injected; real impl hits git).
    Returns {"close": [{id,tier,evidence,line}], "skip": [{id,reason}]}.
    """
    strong = proposals.get("strong", {})
    weak = proposals.get("weak", {})
    close, skip = [], []
    seen = set()
    for aid in approved_ids:
        if aid in seen:
            continue
        seen.add(aid)
        if aid not in open_lines:
            skip.append({"id": aid, "reason": "not currently open (already closed or never existed)"})
            continue
        if aid in strong:
            shas = strong[aid]
            alive = [s for s in shas if evidence_exists(s)]
            if not alive:
                skip.append({"id": aid, "reason": f"STRONG evidence commit(s) {shas} no longer found"})
                continue
            close.append({"id": aid, "tier": "strong", "evidence": alive, "line": open_lines[aid]})
        elif aid in weak:
            close.append({"id": aid, "tier": "weak",
                          "evidence": [sha for _path, sha in weak[aid]], "line": open_lines[aid]})
        else:
            skip.append({"id": aid, "reason": "not a proposed candidate (refusing to close un-proposed id)"})
    return {"close": close, "skip": skip}


def remove_task(backlog_text: str, task_id: str) -> tuple:
    """Remove exactly the one `- [#id] ...` line. Returns (new_text, removed_bool).

    Never renumbers, never touches other lines; removes the whole line incl. its
    newline. Refuses (removed=False, text unchanged) if the line is absent or not
    unique — ambiguity must never silently delete the wrong thing.
    """
    pat = re.compile(rf"^- \[#{re.escape(task_id)}\] ", re.M)
    lines = backlog_text.splitlines(keepends=True)
    idx = [i for i, ln in enumerate(lines) if pat.match(ln)]
    if len(idx) != 1:
        return backlog_text, False
    del lines[idx[0]]
    return "".join(lines), True


# ---------------------------------------------------------------------------
# Thin impure adapters
# ---------------------------------------------------------------------------

def _load_validate_backlog():
    spec = importlib.util.spec_from_file_location(
        "validate_backlog", _SCRIPTS_DIR / "validate_backlog.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def open_task_lines(backlog_text: str) -> dict:
    """{id: exact_raw_line} for every open task (reuses validate_backlog.parse)."""
    vb = _load_validate_backlog()
    tasks = vb.parse(backlog_text)[2]
    return {t["id"]: t["raw"] for t in tasks}


def git_commit_exists(repo: Path, sha: str) -> bool:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except OSError:
        return False
    return r.returncode == 0


def latest_proposals(logs_dir: Path):
    files = sorted(logs_dir.glob("PROPOSALS-*.md"))
    return files[-1] if files else None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_proposals_text(path_arg):
    path = Path(path_arg) if path_arg else latest_proposals(_LOGS_DIR)
    if not path or not path.exists():
        return None, None
    return path, path.read_text(encoding="utf-8", errors="replace")


def _debug_surface_log(path_found, text_found, line_produced) -> None:
    # TEMPORARY instrumentation — remove after root-cause confirmed (issue: SessionStart not surfacing)
    import datetime
    try:
        log_path = _LOGS_DIR / "debug-surface.log"
        _LOGS_DIR.mkdir(exist_ok=True)
        entry = (
            f"[{datetime.datetime.now().isoformat(timespec='seconds')}] "
            f"CLAUDE_PROJECT_DIR={os.environ.get('CLAUDE_PROJECT_DIR', 'NOT_SET')!r} "
            f"cwd={Path.cwd()!r} "
            f"_REPO_ROOT={_REPO_ROOT!r} "
            f"proposals_path={path_found!r} "
            f"text_found={text_found is not None} "
            f"line_produced={line_produced!r}\n"
        )
        log_path.write_text(entry, encoding="utf-8") if not log_path.exists() else \
            log_path.open("a", encoding="utf-8").write(entry)
    except Exception:  # noqa: BLE001
        pass  # never block on debug logging


def cmd_surface(args) -> int:
    _path, text = _load_proposals_text(args.proposals)
    line = surface_line(parse_proposals(text)) if text is not None else None
    _debug_surface_log(_path, text, line)
    if text is None:
        return 0  # no proposals file yet — silent, non-blocking
    if line:
        print(line)
    return 0


def cmd_plan(args) -> int:
    path, text = _load_proposals_text(args.proposals)
    if text is None:
        print(json.dumps({"error": "no proposals file found", "close": [], "skip": []}))
        return 0
    proposals = parse_proposals(text)
    backlog_text = Path(args.backlog).read_text(encoding="utf-8", errors="replace")
    approved = [i.strip().lstrip("#") for i in args.ids.split(",") if i.strip()]
    result = plan_closures(
        backlog_text, approved, proposals,
        open_task_lines(backlog_text),
        lambda sha: git_commit_exists(_REPO_ROOT, sha),
    )
    result["proposals_file"] = str(path)
    result["head_commit"] = proposals.get("head_commit")
    print(json.dumps(result, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="review_closures")
    sub = parser.add_subparsers(dest="command", required=True)

    s = sub.add_parser("surface", help="SessionStart one-line summary (read-only)")
    s.add_argument("--proposals", default=None)
    s.set_defaults(func=cmd_surface)

    p = sub.add_parser("plan", help="Re-verify approved ids; emit a JSON close plan (read-only)")
    p.add_argument("--ids", required=True, help="comma-separated operator-approved ids")
    p.add_argument("--proposals", default=None)
    p.add_argument("--backlog", default=str(_BACKLOG))
    p.set_defaults(func=cmd_plan)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
