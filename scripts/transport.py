#!/usr/bin/env python
"""transport.py -- the transport's write gate: registered kinds, registered writers.

WHY THIS EXISTS (lane-transport-registry, BATCH-WAVE5B-N1 #9). The transport
(`CLAUDE_PROMPTS_DIR`, `to-cc/` + `to-browser/` + its own root -- OPERATOR-INTERFACE.md
S1's "Transport v2.1" grammar) is 119 separate read sites and no list of what may be
WRITTEN. A report once landed in the wrong folder because nothing checked. This module is
the one place that answers "is this filename a known kind, and is THIS caller the kind's
registered writer" -- `ecosystem/transport-registry.yaml` is the data, this is the one
function (`write` / `append`) every future writer composes rather than reinventing.

SCOPE, DELIBERATELY NARROW (lane contract: "switch the writer" is `handback.py` only).
This organ does not change `transport_report.py`, `gen_ledger.py`, `gen_seat_boot.py` or
`propose_row_closures.py` -- their own direct writes to the transport are untouched, and
their kinds are registered here as READ-ONLY data (the registry describes what they already
do; it does not intercept them). Only `handback.py`'s two writes (the REFUSED order and the
SESSION append) are switched to call through here.

DERIVED, NOT HAND-COPIED (Done-when 1: "a test derives the kinds from the code and asserts
none is missing"). `derive_kinds_from_code()` below scans every script that actually touches
the transport (calls `resolve_transport()`/`transport_root()`, or mentions `to-browser`/
`to-cc` in its own source) for a filename-template literal -- a run of `WORD-WORD-...-`
immediately followed by a placeholder (`{`, `<`, `*`) or the end of the literal -- and
`tests/test_transport.py` asserts every prefix that scan finds has a registry row.
A concrete, already-resolved filename cited in a docstring (`DIGEST-AUDIT-CROSSCHECK-
2026-09-23.md`, no placeholder after the prefix) does not match; only a live template does.

READ-ONLY BY DEFAULT. `write()`/`append()` are the only functions that touch the drive; the
report command (`report`) and every registry query below are pure reads.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import yaml  # noqa: E402

import transport_report as _tr  # noqa: E402

_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = _ROOT / "ecosystem" / "transport-registry.yaml"
FOLDERS = ("to-cc", "to-browser", "root")


class TransportRegistryError(Exception):
    """The registry file itself is missing or malformed -- never guessed past."""


class TransportWriteRefused(Exception):
    """`write()`/`append()` refused: the filename matches no registered kind, or `writer` is
    not that kind's registered writer. Never partially written."""


@dataclass(frozen=True)
class Kind:
    name: str
    prefix: str                 # the literal prefix a code-derived template also reduces to
    regex: "re.Pattern[str]"
    folder: str                 # "to-cc" | "to-browser" | "root"
    writers: tuple[str, ...]
    readers: tuple[str, ...] = field(default_factory=tuple)
    repo_scope: str = "hub"     # "hub" (.dev-knowledge only) | "any" (every repo on the transport)
    versioned: bool = False
    notes: str = ""

    def matches(self, filename: str) -> bool:
        return bool(self.regex.match(filename))


# --- loading the registry -------------------------------------------------------------------

def load_registry(path: Path = DEFAULT_REGISTRY) -> list[Kind]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise TransportRegistryError(f"could not read {path}: {exc}") from exc
    kinds = (raw or {}).get("kinds")
    if not isinstance(kinds, list) or not kinds:
        raise TransportRegistryError(f"{path} has no non-empty top-level 'kinds' list")
    out: list[Kind] = []
    seen: set[str] = set()
    for row in kinds:
        for req in ("kind", "pattern", "folder", "writers"):
            if req not in row:
                raise TransportRegistryError(f"kind row missing {req!r}: {row!r}")
        name = row["kind"]
        if name in seen:
            raise TransportRegistryError(f"duplicate kind {name!r} in {path}")
        seen.add(name)
        if row["folder"] not in FOLDERS:
            raise TransportRegistryError(
                f"kind {name!r}: folder {row['folder']!r} is not one of {FOLDERS}")
        writers = tuple(row["writers"])
        if not writers:
            raise TransportRegistryError(f"kind {name!r} has no registered writer")
        try:
            regex = re.compile(row["pattern"])
        except re.error as exc:
            raise TransportRegistryError(f"kind {name!r}: bad pattern {row['pattern']!r}: {exc}") from exc
        out.append(Kind(name=name, prefix=row.get("prefix", ""), regex=regex,
                        folder=row["folder"], writers=writers,
                        readers=tuple(row.get("readers", ())),
                        repo_scope=row.get("repo_scope", "hub"),
                        versioned=bool(row.get("versioned", False)),
                        notes=row.get("notes", "")))
    # Longest prefix first: `LANE-END-{lane}.md` must classify as LANE_END, never the shorter
    # `LANE-{stem}.md` (LANE_CONTRACT) a substring-first search would match instead.
    out.sort(key=lambda k: len(k.prefix), reverse=True)
    return out


def classify(filename: str, registry: list[Kind]) -> Optional[Kind]:
    """The first (longest-prefix) registered kind whose pattern matches `filename`, or None."""
    for kind in registry:
        if kind.matches(filename):
            return kind
    return None


# --- the write gate --------------------------------------------------------------------------

def _folder_of(dest: Path) -> str:
    """`dest`'s own folder name, as `scan()`'s convention reads it: `to-cc`/`to-browser` when
    the immediate parent is named that, else `root` (a `LANE-*.md` contract, sitting directly
    under the transport root rather than either subfolder)."""
    parent_name = dest.parent.name
    return parent_name if parent_name in ("to-cc", "to-browser") else "root"


def _check(writer: str, dest: Path, registry: list[Kind]) -> Kind:
    kind = classify(dest.name, registry)
    if kind is None:
        raise TransportWriteRefused(
            f"{dest.name!r} matches no registered kind in {DEFAULT_REGISTRY.name}; "
            f"refusing to write an unregistered kind")
    if writer not in kind.writers:
        raise TransportWriteRefused(
            f"{dest.name!r} is kind {kind.name!r}, whose registered writer(s) are "
            f"{kind.writers!r}; {writer!r} is not among them")
    actual_folder = _folder_of(dest)
    if actual_folder != kind.folder:
        # Codex terra HIGH (this lane's own review): matching `dest.name` alone let a registered
        # writer recreate the exact "landed in the wrong folder" failure the registry exists to
        # end -- e.g. `handback` writing a correctly-named SESSION file into `to-cc/`.
        raise TransportWriteRefused(
            f"{dest!r} is kind {kind.name!r}, registered to {kind.folder}/, but the "
            f"destination's own folder is {actual_folder}/; refusing to write it there")
    return kind


def write(writer: str, dest: Path, data: str, *, registry: Optional[list[Kind]] = None) -> Path:
    """Write `data` (text) to `dest` WHOLE (atomic tmp+replace, `transport_report.deliver`'s own
    pattern), but only when `dest.name` is a registered kind, `writer` is its registered writer,
    AND `dest` sits in that kind's registered folder. Raises `TransportWriteRefused` before
    touching the filesystem otherwise."""
    reg = registry if registry is not None else load_registry()
    _check(writer, dest, reg)
    dest.parent.mkdir(parents=True, exist_ok=True)
    _tr.deliver(dest, data.encode("utf-8"))
    return dest


class _DestinationLock:
    """An exclusive, cross-process advisory lock scoped to ONE destination path -- a sibling
    `.<name>.append.lock` file, created with `O_EXCL` (atomic on both POSIX and Windows) and
    removed on release. Bounded retry with backoff, never an indefinite wait (Codex terra HIGH,
    this lane's own review: two concurrent `append()` calls to the SAME `SESSION-<lane>.md`
    could otherwise interleave, or both read the pre-write file size and agree on the same
    separator decision against a file the other has already appended to)."""

    _POLL_S = 0.05

    def __init__(self, dest: Path, timeout_s: float = 10.0):
        self._lock_path = dest.parent / f".{dest.name}.append.lock"
        self._timeout_s = timeout_s
        self._fd: Optional[int] = None

    def __enter__(self) -> "_DestinationLock":
        import time
        deadline = time.monotonic() + self._timeout_s
        while True:
            try:
                self._fd = os.open(str(self._lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise TransportWriteRefused(
                        f"could not acquire the append lock for {self._lock_path.name} within "
                        f"{self._timeout_s}s; another writer appears to be appending to the "
                        f"same destination")
                time.sleep(self._POLL_S)

    def __exit__(self, *exc_info: object) -> None:
        if self._fd is not None:
            os.close(self._fd)
        try:
            self._lock_path.unlink()
        except OSError:
            pass


def append(writer: str, dest: Path, block: str, *, registry: Optional[list[Kind]] = None) -> Path:
    """Append `block` to `dest` (creating it if absent), gated the same way as `write()`.
    Used for a kind multiple callers add to over time (`SESSION-<lane>.md`), where a full
    atomic replace would erase what an earlier writer already left. Serialized per-destination
    (`_DestinationLock`) so the separator decision and the write happen as one protected step."""
    reg = registry if registry is not None else load_registry()
    _check(writer, dest, reg)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with _DestinationLock(dest):
        with dest.open("a", encoding="utf-8", newline="\n") as fh:
            if dest.stat().st_size and not block.startswith("\n"):
                fh.write("\n")
            fh.write(block)
            if not block.endswith("\n"):
                fh.write("\n")
    return dest


# --- the stray-file report (report-only; Done-when 3) -----------------------------------------

@dataclass(frozen=True)
class StrayFinding:
    path: str            # relative to the transport root, e.g. "to-browser/ODD-NAME.md"
    reason: str          # "unregistered kind" | "kind KIND belongs in FOLDER, found in HERE"


def scan(transport_root: Path, registry: Optional[list[Kind]] = None) -> list[StrayFinding]:
    """Non-recursive over `to-cc/` and `to-browser/` (the convention `gen_handoff.decision_files`
    already uses) plus the transport root itself (`LANE-*.md` contracts live there, not in
    either subfolder). Report-only: never renames, moves or deletes anything (Do-not clause)."""
    reg = registry if registry is not None else load_registry()
    findings: list[StrayFinding] = []
    homes = {"to-cc": transport_root / "to-cc", "to-browser": transport_root / "to-browser",
             "root": transport_root}
    for folder_name, folder_path in homes.items():
        if not folder_path.is_dir():
            continue
        for entry in sorted(folder_path.iterdir()):
            if not entry.is_file():
                continue
            if folder_name == "root" and entry.parent != transport_root:
                continue  # never happens (iterdir on transport_root already scopes this)
            kind = classify(entry.name, reg)
            rel = f"{folder_name}/{entry.name}" if folder_name != "root" else entry.name
            if kind is None:
                findings.append(StrayFinding(rel, "unregistered kind"))
            elif kind.folder != folder_name:
                findings.append(StrayFinding(
                    rel, f"kind {kind.name} belongs in {kind.folder}/, found in {folder_name}/"))
    return findings


# --- deriving the kind set from the code itself (Done-when 1) ----------------------------------
#
# Not an AST parse: a transport filename template lives in an f-string, a bare prefix constant,
# a tuple of prefixes, or a PowerShell-quoted help string, so this is a textual scan over the
# specific SYNTACTIC SHAPES that actually build one -- not "every quoted literal in the file",
# which (tried first, see the lane's own session file) drags in every unrelated ALL-CAPS status
# word (`PASS`, `DEGRADED`, ...) these same modules also format into f-strings. A shape a literal
# must match ONE of to be a candidate:
#
#   (join)   `<anything> / <literal>`      -- a Path segment: `browser / f"HANDBACK-REFUSED-{x}.md"`
#   (glob)   `.glob(<literal>)`            -- `to_browser.glob("QUESTION*.md")`
#   (folder) the literal itself contains "to-browser" or "to-cc"  -- `f"to-browser/LEDGER-{x}.md"`
#   (named)  the literal is assigned to, or returned by a function named, something matching
#            PREFIX/NAME/ARTIFACT/TEMPLATE/FILENAME -- `GO_NAME = "GO-{batch}.md"`,
#            `ARTIFACT_PREFIX = "LANE-END-"`, `def contract_filename(...): return f"LANE-{x}.md"`
#
# Each candidate literal is then reduced to a prefix by `_template_prefixes`: a live template's prefix
# sits immediately before a placeholder (`{`, `<`, `*`) or the literal's end; a concrete,
# already-resolved filename (a docstring citing a real past artifact, `DIGEST-AUDIT-CROSSCHECK-
# 2026-09-23.md`) has ordinary text where the placeholder would be and never matches.

_LITERAL = r'(?:"(?:[^"\n])*"|\'(?:[^\'\n])*\')'
_LIT_CONTENT_RE = re.compile(r'"([^"\n]*)"|\'([^\'\n]*)\'')

_JOIN_RE = re.compile(r"/\s*f?(" + _LITERAL + r")")
_GLOB_RE = re.compile(r"\.glob\(\s*f?(" + _LITERAL + r")")
_NAME_RE = re.compile(r"PREFIX|NAME|ARTIFACT|TEMPLATE|FILENAME", re.I)
_ASSIGN_RE = re.compile(r"^[ \t]*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$", re.M)
_DEF_RE = re.compile(r"^[ \t]*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)
_FOLDER_TOKENS = ("to-browser", "to-cc")

#: The (join)/(glob)/(named) shapes are common Python -- shared with plenty of code that has
#: nothing to do with the transport (`dispatch.py`'s local `receipts_dir() / f"LAUNCH-...json"`,
#: `dodo.py`'s local `_receipts() / f"SPINE-...json"`, `lane_end_guard.py`'s own local
#: `OUTPUT_NAME` claim file). Those three shapes are therefore accepted only within
#: `_ANCHOR_WINDOW` lines of an actual transport-resolving token; (folder) needs no such gate,
#: since "to-browser"/"to-cc" inside the literal itself already IS the transport reference.
_ANCHOR_TOKENS = ("resolve_transport", "transport_root", "to-browser", "to-cc",
                  "to_browser", "to_cc")
_ANCHOR_WINDOW = 6


def _line_offsets(text: str) -> list[int]:
    """Start offset of each line, for turning a match index into a line number."""
    offsets = [0]
    for ln in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(ln))
    return offsets


def _line_of(offsets: list[int], idx: int) -> int:
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= idx:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _anchor_lines(text: str, lines: list[str]) -> set[int]:
    return {i for i, ln in enumerate(lines) if any(tok in ln for tok in _ANCHOR_TOKENS)}


def _near_anchor(anchors: set[int], line_no: int, window: int = _ANCHOR_WINDOW) -> bool:
    return any(abs(line_no - a) <= window for a in anchors)

#: A live template, two shapes:
#:   MID  `WORD(-WORD)*` immediately before a placeholder (`{`, `<`, `*`), an optional hyphen
#:        between them (`GO-{batch}` has one, `STATUS*.md`'s glob does not). Preceded by a path
#:        separator, whitespace or the literal's start, so a multi-path help string naming two
#:        kinds in one literal (`gen_seat_boot.py`'s `"$d/to-cc/DECLARE-*.md $d/to-cc/AMEND-*.md"`)
#:        yields every prefix in it, not just the first.
#:   BARE the WHOLE literal is `WORD(-WORD)*-` and nothing else (`ARTIFACT_PREFIX = "LANE-END-"`,
#:        one element of a `("DECLARE-", "AMEND-", "BATCH-")` tuple) -- a prefix CONSTANT, not a
#:        filename with the prefix as a substring.
#: BARE, not a bare end-of-string on MID, is deliberate: a short argument string with no hyphen
#: at all (`_next_free_dated_path(_LOGS_DIR, "PROPOSALS")`) must NOT read as a one-word "kind"
#: just because it happens to sit at a literal's end -- it is not a filename template at all.
_TEMPLATE_MID_RE = re.compile(r"(?:^|[/\s])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)-?(?=[{<*])")
_TEMPLATE_BARE_RE = re.compile(r"^([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)-$")


def _template_prefixes(literal: str) -> set[str]:
    found = {m.group(1) + "-" for m in _TEMPLATE_MID_RE.finditer(literal)}
    bare = _TEMPLATE_BARE_RE.match(literal)
    if bare:
        found.add(bare.group(1) + "-")
    return found

#: `def foo(...):` body scanned for a NAMED-return candidate: this many lines after the `def`,
#: or the next top-level `def`/`class`, whichever comes first -- `contract_filename` is 6 lines.
_DEF_BODY_WINDOW = 15


def _content(literal_with_quotes: str) -> str:
    m = _LIT_CONTENT_RE.match(literal_with_quotes)
    return m.group(1) if m.group(1) is not None else m.group(2)


def _candidate_literals(text: str) -> set[str]:
    """Every quoted literal (its content, quotes stripped) matching one of the four shapes
    above -- see the section docstring. (join)/(glob)/(named) additionally require a transport
    anchor within `_ANCHOR_WINDOW` lines (see `_ANCHOR_TOKENS`'s own docstring); (folder) does
    not, since the literal already names the folder itself."""
    out: set[str] = set()
    lines = text.splitlines()
    offsets = _line_offsets(text)
    anchors = _anchor_lines(text, lines)

    def near(idx: int) -> bool:
        return _near_anchor(anchors, _line_of(offsets, idx))

    for m in _JOIN_RE.finditer(text):
        if near(m.start()):
            out.add(_content(m.group(1)))
    for m in _GLOB_RE.finditer(text):
        if near(m.start()):
            out.add(_content(m.group(1)))
    for m in _LIT_CONTENT_RE.finditer(text):
        content = m.group(1) if m.group(1) is not None else m.group(2)
        if any(tok in content for tok in _FOLDER_TOKENS):
            out.add(content)
    for m in _ASSIGN_RE.finditer(text):
        var_name, rhs = m.group(1), m.group(2)
        if _NAME_RE.search(var_name) and near(m.start()):
            for lm in _LIT_CONTENT_RE.finditer(rhs):
                out.add(lm.group(1) if lm.group(1) is not None else lm.group(2))
    for dm in _DEF_RE.finditer(text):
        # Not proximity-gated like the shapes above: a named-filename function's own body is
        # often the transport-resolving call's ONLY definition site in the file (e.g.
        # `contract_filename` in `gen_lane_contract.py`, dozens of lines from where
        # `transport_root()` is imported), so an anchor window here would exclude the very
        # function that IS the anchor. The function-name restriction alone is the gate.
        if not _NAME_RE.search(dm.group(1)):
            continue
        start_line = _line_of(offsets, dm.start())
        window_text = "\n".join(lines[start_line:start_line + _DEF_BODY_WINDOW])
        for lm in _LIT_CONTENT_RE.finditer(window_text):
            out.add(lm.group(1) if lm.group(1) is not None else lm.group(2))
    return out


def derive_kinds_from_code(scripts_dir: Path = _SCRIPTS) -> set[str]:
    """Every filename-template prefix (`"LEDGER-"`, `"LANE-END-"`, ...) a script in `scripts_dir`
    actually builds, read straight from the source text -- see the section docstring for the
    four syntactic shapes recognised and why a bare "every quoted literal" scan is not this."""
    prefixes: set[str] = set()
    for path in sorted(scripts_dir.glob("*.py")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for literal in _candidate_literals(text):
            prefixes |= _template_prefixes(literal)
    return prefixes


# --- CLI ----------------------------------------------------------------------------------------

def _resolve_root(explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    root = _tr.windows_user_env("CLAUDE_PROMPTS_DIR") or os.environ.get("CLAUDE_PROMPTS_DIR")
    if not root:
        raise _tr.TransportRefused("CLAUDE_PROMPTS_DIR is not set; no transport to report on")
    return Path(root)


def _cmd_report(args: argparse.Namespace) -> int:
    root = _resolve_root(args.transport_root)
    if not root.is_dir():
        print(json.dumps({"transport": str(root), "resolved": False,
                          "reason": "not mounted or does not exist"}, sort_keys=True))
        return 0
    findings = scan(root)
    print(json.dumps({"transport": str(root), "resolved": True,
                      "stray_count": len(findings),
                      "stray": [{"path": f.path, "reason": f.reason} for f in findings]},
                     indent=2, sort_keys=True))
    return 0  # report-only: never a refusal exit


def _cmd_derive(_args: argparse.Namespace) -> int:
    derived = sorted(derive_kinds_from_code())
    registry = load_registry()
    registered = {k.prefix for k in registry}
    missing = sorted(set(derived) - registered)
    print(json.dumps({"derived": derived, "missing_from_registry": missing}, indent=2))
    return 1 if missing else 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="transport.py", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report", help="report-only: stray/misplaced files on the live transport")
    r.add_argument("--transport-root", default=None)
    r.set_defaults(func=_cmd_report)
    d = sub.add_parser("derive", help="derive kind prefixes from the code; diff against the registry")
    d.set_defaults(func=_cmd_derive)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = _parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
