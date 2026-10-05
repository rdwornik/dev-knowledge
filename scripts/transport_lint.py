#!/usr/bin/env python
"""transport_lint.py -- a transport file that breaks the grammar is caught when it is written.

WHY THIS EXISTS (LANE-B2-W1-b2-transport-lint, batch B2-W1, seat ruling 2 of 2026-10-04).
FOUNDATION's close was refused by ONE file: a run SIGNAL written under a DECISION prefix
(`AMEND-5-GREEN-2026-10-03.md`) as a one-line file with no `carried-by:` head. Nothing checked
a transport write, so the trial cut found it 9 h later, at close. A check that only runs at
close is a postmortem, not a gate. This module is the check that runs at WRITE time:

  * `lint_text(name, folder, text)` -- the one function. `transport.write()` / `append()` call
    it before a byte lands, so every harness writer is covered by construction.
  * `check <file>...` -- the same lint by hand, for a file a seat writes to Drive itself
    (which bypasses every hook).
  * `sweep` -- the lint over the live transport since a given time, one line per bad file,
    exit 1 on any. A seat's wake runs it, so a file written by hand is flagged within one wake.
    Report only: it renames, moves and deletes nothing.

WHAT IT CHECKS (each finding has a code and a reason):
  unknown-kind / pattern-mismatch / wrong-folder   -- the filename against `ecosystem/
        transport-registry.yaml`.
  no-carried-by / carried-by-not-a-path            -- a DECISION file (`gen_handoff.
        CARRIAGE_PREFIXES`: DECLARE-, AMEND-, BATCH-) carries a flush-left `carried-by:` in its
        first 6 lines whose value is `OPEN` or names a repo path.
  signal-under-decision-prefix                     -- the specific no-carried-by case where the
        file is one line: a run signal. The fix is its own kind, `SIGNAL-<slug>-<date>.md`.
  lane-contract-no-r59-proof                       -- a `LANE-` contract whose close-out names no
        served model id and no nonce/content-hash proof of read (R59).

It checks SHAPE, never resolution: that the named home exists on `main` is `gen_handoff`'s P11
row, which needs the repository; a file may name a home that lands in the same merge.

LIBRARY-FIRST. The registry is `transport.load_registry` / `classify` (no third reader); the
carriage head, the `OPEN` test and the path tokenizer are `gen_handoff`'s own, imported on the
first decision file rather than copied, and `tests/test_transport_lint.py` holds the registry's
decision class equal to `gen_handoff.CARRIAGE_PREFIXES`, so the two cannot drift. argparse and
stdlib only; no new dependency.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import transport as _t  # noqa: E402

#: The kinds whose file is a lane contract: its close-out names the R59 proof of read.
LANE_CONTRACT_KINDS = ("LANE_CONTRACT", "DATED_SLUG_LANE_CONTRACT")
_SERVED_MODEL_RE = re.compile(r"served[ -]model(?:[ -]id)?", re.I)
_PROOF_RE = re.compile(r"\bnonce\b|content[ -]hash", re.I)

#: Names the sweep never reads: Drive and Windows bookkeeping, and this repo's own
#: `.<name>.tmp` / `.<name>.append.lock` plumbing files.
_SWEEP_SKIP_EXACT = {"desktop.ini"}


@dataclass(frozen=True)
class Finding:
    path: str      # the file name (lint_text) or the transport-relative path (sweep)
    code: str      # a short kebab-case slug
    reason: str

    def render(self) -> str:
        return f"{self.path}: {self.code}: {self.reason}"


# --- the gen_handoff carriage readers (imported once, on the first decision file) -------------

_GH = None


def _gen_handoff():
    global _GH
    if _GH is None:
        import gen_handoff  # noqa: PLC0415 -- heavy; only a decision file needs it
        _GH = gen_handoff
    return _GH


def carried_by_value(text: str) -> Optional[str]:
    """The ANCHORED `carried-by:` value in the first `CARRIAGE_HEAD_LINES` lines of `text`, or
    None -- `gen_handoff.carried_by_value`, on text instead of a path (a test holds them equal)."""
    gh = _gen_handoff()
    head = "".join(text.splitlines(keepends=True)[:gh.CARRIAGE_HEAD_LINES])
    m = gh._CARRIED_BY_RE.search(head)
    return m.group(1).strip() if m else None


def decision_prefixes(registry: list) -> tuple[str, ...]:
    return tuple(k.prefix for k in registry if k.decision)


def is_decision(name: str, registry: list) -> bool:
    """A `.md` file under a decision prefix -- by NAME, as `gen_handoff.decision_files` selects
    it, so a file the registry cannot classify still gets the carriage check."""
    return name.endswith(".md") and name.startswith(decision_prefixes(registry))


def _non_blank_lines(text: str) -> int:
    return sum(1 for ln in text.splitlines() if ln.strip())


# --- the lint ---------------------------------------------------------------------------------

def lint_entry(name: str, folder: str, read_text: Callable[[], str],
               registry: Optional[list] = None) -> list[Finding]:
    """Lint one transport file by NAME and FOLDER; `read_text` is called only when the kind
    needs the body (a decision file, a lane contract) -- a sweep reads nothing else."""
    reg = registry if registry is not None else _t.load_registry()
    findings: list[Finding] = []
    kind = _t.classify(name, reg)
    if kind is None:
        near = [k for k in reg if k.prefix and name.startswith(k.prefix)]
        if near:
            findings.append(Finding(name, "pattern-mismatch",
                f"starts like kind {near[0].name} (`{near[0].prefix}`) but does not match its "
                f"pattern {near[0].regex.pattern}"))
        else:
            findings.append(Finding(name, "unknown-kind",
                "matches no registered kind in ecosystem/transport-registry.yaml"))
    elif kind.folder != folder:
        findings.append(Finding(name, "wrong-folder",
            f"kind {kind.name} belongs in {kind.folder}/, found in {folder}/"))

    if is_decision(name, reg):
        findings.extend(_carriage_findings(name, read_text()))
    elif kind is not None and kind.name in LANE_CONTRACT_KINDS:
        closeout = _closeout_region(read_text())
        if not (_SERVED_MODEL_RE.search(closeout) and _PROOF_RE.search(closeout)):
            findings.append(Finding(name, "lane-contract-no-r59-proof",
                "the close-out names no served model id and no nonce or content-hash proof of "
                "read (R59): a review record without both reads as a failed read"))
    return findings


_CLOSEOUT_RE = re.compile(r"close-?out", re.I)
_HEADING_RE = re.compile(r"^#{1,6}\s", re.M)


def _closeout_region(text: str) -> str:
    """The close-out item of a lane contract: from the first `Close-out` mention to the next
    heading (or the end of the file). The R59 words count only there -- the same words in
    unrelated prose do not satisfy the gate. Empty when the contract has no close-out."""
    m = _CLOSEOUT_RE.search(text)
    if m is None:
        return ""
    rest = text[m.start():]
    h = _HEADING_RE.search(rest, 1)
    return rest[:h.start()] if h else rest


def _carriage_findings(name: str, text: str) -> list[Finding]:
    gh = _gen_handoff()
    value = carried_by_value(text)
    if value is None:
        if _non_blank_lines(text) <= 1:
            return [Finding(name, "signal-under-decision-prefix",
                f"a one-line file with no `carried-by:` under a decision prefix "
                f"({'/'.join(gh.CARRIAGE_PREFIXES)}) is a run signal: write it as "
                "`SIGNAL-<slug>-<date>.md`, which is not a decision kind")]
        return [Finding(name, "no-carried-by",
            f"a decision file carries a flush-left `carried-by:` in its first "
            f"{gh.CARRIAGE_HEAD_LINES} lines (a key in a comment or the body is not anchored)")]
    if gh._OPEN_VALUE_RE.match(value):
        return []
    if not gh._carrier_tokens(value):
        return [Finding(name, "carried-by-not-a-path",
            f"`carried-by: {value[:60]}` is neither `OPEN` nor a repo path")]
    return []


def lint_text(name: str, folder: str, text: str,
              registry: Optional[list] = None) -> list[Finding]:
    return lint_entry(name, folder, lambda: text, registry)


def lint_file(path: Path, folder: Optional[str] = None,
              registry: Optional[list] = None) -> list[Finding]:
    folder = folder or _t._folder_of(path)
    return lint_entry(path.name, folder,
                      lambda: path.read_text(encoding="utf-8", errors="replace"), registry)


# --- the sweep --------------------------------------------------------------------------------

def parse_since(spec: str, now: Optional[float] = None) -> float:
    """`30m` / `2h` / `1d` (relative to `now`) or an ISO-8601 time -> a POSIX timestamp."""
    now = time.time() if now is None else now
    m = re.fullmatch(r"(\d+)([mhd])", spec.strip())
    if m:
        return now - int(m.group(1)) * {"m": 60, "h": 3600, "d": 86400}[m.group(2)]
    return datetime.fromisoformat(spec.strip().replace("Z", "+00:00")).timestamp()


def sweep(transport_root: Path, since: Optional[float] = None,
          registry: Optional[list] = None) -> list[Finding]:
    """The lint over `to-cc/`, `to-browser/` and the root itself (non-recursive, the convention
    `transport.scan` uses), files modified at or after `since`. Report-only."""
    reg = registry if registry is not None else _t.load_registry()
    root = Path(transport_root)
    homes = {"to-cc": root / "to-cc", "to-browser": root / "to-browser", "root": root}
    findings: list[Finding] = []
    for folder, home in homes.items():
        if not home.is_dir():
            continue
        for entry in sorted(home.iterdir()):
            if not entry.is_file() or entry.name.startswith(".") or entry.name in _SWEEP_SKIP_EXACT:
                continue
            if since is not None:
                try:
                    if entry.stat().st_mtime < since:
                        continue
                except OSError:
                    continue
            rel = f"{folder}/{entry.name}" if folder != "root" else entry.name
            for f in lint_entry(entry.name, folder,
                                lambda e=entry: e.read_text(encoding="utf-8", errors="replace"), reg):
                findings.append(Finding(rel, f.code, f.reason))
    return findings


# --- CLI --------------------------------------------------------------------------------------

def _cmd_check(args: argparse.Namespace) -> int:
    reg = _t.load_registry()
    bad = 0
    for raw in args.files:
        path = Path(raw)
        if not path.is_file():
            print(f"{raw}: missing-file: no such file")
            bad += 1
            continue
        found = lint_file(path, args.folder, reg)
        for f in found:
            print(f.render())
        if found:
            bad += 1
        else:
            print(f"{path.name}: ok")
    return 1 if bad else 0


def _cmd_sweep(args: argparse.Namespace) -> int:
    try:
        root = _t._resolve_root(args.transport_root)
    except Exception as exc:  # noqa: BLE001 -- an unset transport is a refusal, said plainly
        print(f"transport_lint: {exc}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"transport_lint: transport root {root} is not mounted or does not exist",
              file=sys.stderr)
        return 2
    since = parse_since(args.since) if args.since else None
    findings = sweep(root, since)
    for f in findings:
        print(f.render())
    print(f"transport_lint: swept {root} since "
          f"{args.since or 'the beginning'}: {len(findings)} non-conforming file(s)",
          file=sys.stderr)
    return 1 if findings else 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="transport_lint.py", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="lint one or more transport files; exit 1 on any finding")
    c.add_argument("files", nargs="+")
    c.add_argument("--folder", choices=_t.FOLDERS, default=None,
                   help="the folder the file is destined for (default: its own parent folder)")
    c.set_defaults(func=_cmd_check)
    s = sub.add_parser("sweep", help="lint the live transport; one line per bad file, exit 1")
    s.add_argument("--transport-root", default=None)
    s.add_argument("--since", default=None,
                   help="only files modified since: 30m, 2h, 1d or an ISO time")
    s.set_defaults(func=_cmd_sweep)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = _parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
