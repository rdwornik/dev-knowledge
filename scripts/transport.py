#!/usr/bin/env python
"""transport.py -- the transport's write gate: registered kinds, registered writers.

WHY THIS EXISTS (lane-transport-registry, BATCH-WAVE5B-N1 #9). The transport
(`CLAUDE_PROMPTS_DIR`, `to-cc/` + `to-browser/` + its own root -- OPERATOR-INTERFACE.md
S1's "Transport v2.1" grammar) is 119 separate read sites and no list of what may be
WRITTEN. A report once landed in the wrong folder because nothing checked. This module is
the one place that answers "is this filename a known kind, and is THIS caller the kind's
registered writer" -- `ecosystem/transport-registry.yaml` is the data, this is the one
function (`write` / `append`) every future writer composes rather than reinventing.

WHO CALLS IT. `handback.py`'s two writes (the REFUSED order and the SESSION append) were the
first; LANE-B2-W1-b2-transport-lint added the lint (`transport_lint.py`: a decision file's
`carried-by:` head, a signal kept out of the decision prefixes, a lane contract's R59 proof)
INSIDE `write()` / `append()`, and routed `transport_report.py`, `gen_ledger.py` and
`propose_row_closures.py` through `write()` / `emit()`. `gen_seat_boot.py` writes a repo
handoff bundle, not the transport, so it has no call site here. `gen_lane_contract.py` (lane
W1-4's) and the integrator template's own writes (lane W1-5's) follow after this lane merges;
`transport_lint.py sweep` covers them in the meantime.

DERIVED, NOT HAND-COPIED (Done-when 1: "a test derives the kinds from the code and asserts
none is missing"). `derive_kinds_from_code()` below scans every script that actually touches
the transport (calls `resolve_transport()`/`transport_root()`, or mentions `to-browser`/
`to-cc` in its own source) for a filename-template literal -- a run of `WORD-WORD-...-`
immediately followed by a placeholder (`{`, `<`, `*`) or the end of the literal -- and
`tests/test_transport.py` asserts every prefix that scan finds has a registry row.
A concrete, already-resolved filename cited in a docstring (`DIGEST-AUDIT-CROSSCHECK-
2026-09-23.md`, no placeholder after the prefix) does not match; only a live template does.

WHY THE INDEX WENT STALE (lane bu-1539-transport, [#1539]). The refresh trigger lives in
`write()` / `append()`, and the transport's main writers bypass it: the browser seat writes through
Drive and CC seats through their own file tool. On 2026-10-15 52 files were newer than the INDEX and
none had been written through `write()`. So the reader (`query`) and the generated-file writers
refresh, and `index_stale(root)` says when. The INDEX is now two files: `INDEX-ARCHIVE.md` (the full
text, the cache `refresh_index` reads) and `INDEX.md` (`build_view`, a small current view with the
derived request status, capped at `INDEX_BYTE_CAP`).

READ-ONLY BY DEFAULT. `write()`/`append()` are the only functions that write a TRANSPORT file for
a caller; the report command (`report`) and every registry query below are pure reads. The one
other writer is this module's own generated surface (LANE-1439-b2w2-transport-index): the
`index` command writes `to-browser/INDEX.md` (and `write()`/`append()` refresh it after a
classified write), `inventory` and `seat-ids` rewrite their sections of `ecosystem/seat-ids.yaml`,
and `janitor --apply --expect-manifest <hash>` MOVES -- never deletes or overwrites -- the
`-superseded` files of registered, attributable kinds into `<folder>/archive/YYYY-MM/`. The
`janitor` without `--apply` is a dry run that prints the move list and its hash. `query` (lane
bw-1439-transport-index) reads that generated INDEX: the rows for a kind, a date (or its
prefix) and a seat (or a session slug the seat map resolves), so a reader never opens INDEX.md by hand.
It refreshes a stale INDEX first (read-repair; `--no-refresh` or `--index PATH` keeps it a pure read);
`--since` lists the live files' headers instead and `--seat architect` is the architect's inbox.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import logging
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
KIND_CLASSES = ("decision", "non-decision")

#: The writers that are a person or a seat (a registry `writers` entry); every other writer name
#: is a script. The `by:` rule refuses an unsigned NEW file from a role and only advises a script.
ROLE_WRITERS = ("operator", "lane", "integrator")
#: The generated index, the repository token the attribution rule reads, and the generated data
#: file that holds the seat-ID map and the landing inventory (LANE-1439-b2w2-transport-index).
INDEX_NAME = "INDEX.md"
ARCHIVE_INDEX_NAME = "INDEX-ARCHIVE.md"
_ARCHIVE_REL = f"to-browser/{ARCHIVE_INDEX_NAME}"
INDEX_BYTE_CAP = 40_000
CURRENT_DAYS = 7
REQUEST_KINDS = ("QUESTION", "BATCH", "AMEND")
REQUEST_TIMEOUT_DAYS = 3
ANSWERS_ERA = "2026-10-15"
REPO_TOKEN = "dev-knowledge"
_log = logging.getLogger("transport")
DEFAULT_SEAT_IDS = _ROOT / "ecosystem" / "seat-ids.yaml"


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
    folder: str                 # the primary folder: "to-cc" | "to-browser" | "root"
    writers: tuple[str, ...]
    readers: tuple[str, ...] = field(default_factory=tuple)
    repo_scope: str = "hub"     # "hub" (.dev-knowledge only) | "any" (every repo on the transport)
    versioned: bool = False
    notes: str = ""
    decision: bool = False      # class: decision -> the file carries an anchored `carried-by:`
    folders: tuple[str, ...] = ()   # every home, primary first; defaults to (folder,)

    def __post_init__(self) -> None:
        if not self.folders:
            object.__setattr__(self, "folders", (self.folder,))

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
        raw_folder = row["folder"]
        folders = tuple(raw_folder) if isinstance(raw_folder, list) else (raw_folder,)
        if not folders:
            raise TransportRegistryError(f"kind {name!r}: folder list is empty")
        for f in folders:
            if f not in FOLDERS:
                raise TransportRegistryError(
                    f"kind {name!r}: folder {f!r} is not one of {FOLDERS}")
        writers = tuple(row["writers"])
        if not writers:
            raise TransportRegistryError(f"kind {name!r} has no registered writer")
        try:
            regex = re.compile(row["pattern"])
        except re.error as exc:
            raise TransportRegistryError(f"kind {name!r}: bad pattern {row['pattern']!r}: {exc}") from exc
        cls = row.get("class", "non-decision")
        if cls not in KIND_CLASSES:
            raise TransportRegistryError(
                f"kind {name!r}: class {cls!r} is not one of {KIND_CLASSES}")
        out.append(Kind(name=name, prefix=row.get("prefix", ""), regex=regex,
                        folder=folders[0], folders=folders, writers=writers,
                        readers=tuple(row.get("readers", ())),
                        repo_scope=row.get("repo_scope", "hub"),
                        versioned=bool(row.get("versioned", False)),
                        notes=row.get("notes", ""),
                        decision=cls == "decision"))
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
    parent_name = dest.parent.name.lower()   # a Windows path may spell it `TO-BROWSER`
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
    if actual_folder not in kind.folders:
        # Codex terra HIGH (this lane's own review): matching `dest.name` alone let a registered
        # writer recreate the exact "landed in the wrong folder" failure the registry exists to
        # end -- e.g. `handback` writing a correctly-named SESSION file into `to-cc/`.
        raise TransportWriteRefused(
            f"{dest!r} is kind {kind.name!r}, registered to {' or '.join(kind.folders)}/, but the "
            f"destination's own folder is {actual_folder}/; refusing to write it there")
    return kind


def known_root() -> Optional[Path]:
    """The transport root the environment names (`CLAUDE_PROMPTS_DIR`), or None. The `by:` rule and
    the INDEX refresh act only on a destination inside it, so a scratch tree is never touched."""
    raw = _tr.windows_user_env("CLAUDE_PROMPTS_DIR") or os.environ.get("CLAUDE_PROMPTS_DIR")
    return Path(raw) if raw else None


def same_path(a: Path, b: Path) -> bool:
    try:
        return _same(Path(a).resolve(), Path(b).resolve())
    except OSError:
        return False


def _lint(dest: Path, text: str, reg: list[Kind], writer: Optional[str] = None) -> None:
    """`transport_lint` on the file about to be written (LANE-B2-W1-b2-transport-lint): a
    decision file with no anchored `carried-by:`, a signal under a decision prefix, a lane
    contract with no R59 proof -- refused here, before any byte lands, not at the batch close.
    With a `writer` and a destination inside the known transport it also applies the `by:` rule
    (LANE-1439-b2w2-transport-index): a role writer's NEW unsigned `.md` is refused, a script
    writer's is advised on stderr. Imported on use: `transport_lint` imports this module."""
    import transport_lint  # noqa: PLC0415
    folder = _folder_of(dest)
    by = writer is not None and dest.name.endswith(".md") and _inside_known_transport(dest)
    inventory = load_inventory(DEFAULT_SEAT_IDS) if by else None
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    findings = transport_lint.lint_text(
        dest.name, folder, text, reg, require_by=by,
        file_class=lambda: transport_lint.file_class(
            transport_lint.inventory_key(folder, dest.name), sha, inventory),
        refuse_by=(writer in ROLE_WRITERS) if by else None)
    refused = [f for f in findings if f.level == "refuse"]
    if refused:
        note = ""
        if by and inventory is None:
            note = (f"; no readable landing inventory at {DEFAULT_SEAT_IDS}, so every file counts "
                    "as new")
        raise TransportWriteRefused(
            f"{dest.name!r} fails the transport lint: "
            + "; ".join(f"{f.code} ({f.reason})" for f in refused) + note)
    for f in findings:
        if f.code == "no-by-generated-kind":
            print(f"transport: {dest.name}: {f.reason}", file=sys.stderr)
    if by:
        _refuse_unregistered_seat(dest, text, transport_lint)


def unregistered_seats(text: str, registered: set[str], by_text: str) -> list[str]:
    """Tech-Architect ids named in `by_text` that `registered` lacks and that `text`'s own head does
    not register: the registering write states its own pair (one id, one session slug), the shape
    `build_seat_map` reads, so `seat-ids --write` picks it up afterwards."""
    named = sorted(set(_TA_RE.findall(by_text)))
    head = [m.group(1) for ln in text.lstrip("﻿").splitlines()[:HEAD_LINES]
            if (m := _FROM_BY_RE.match(ln))]
    head_seats = {s for v in head for s in _TA_RE.findall(v)}
    head_slugs = {s for v in head for s in _SLUG_RE.findall(v)}
    states_pair = len(head_seats) == 1 and len(head_slugs) == 1
    return [s for s in named if s not in registered and not (states_pair and s in head_seats)]


def _refuse_unregistered_seat(dest: Path, text: str, transport_lint) -> None:
    """ADR-132 D3 ([#1746]): the successor half of the old `seat_ids_both` row. A `by:` naming a
    Tech-Architect id the generated seat map has not registered is refused at the write. An empty
    map has nothing to check against, so it gates nothing; an unreadable one fails closed."""
    by_text = transport_lint.by_value(text)
    if not by_text or not _TA_RE.search(by_text):
        return
    try:
        seats, _inv = load_seat_ids(DEFAULT_SEAT_IDS)
    except SeatIdsError as exc:
        raise TransportWriteRefused(f"{dest.name!r}: the seat map cannot be read ({exc}); "
                                    "an unread map registers nobody") from exc
    if not seats:
        return
    missing = unregistered_seats(text, {s["seat"] for s in seats}, by_text)
    if missing:
        raise TransportWriteRefused(
            f"{dest.name!r}: `by:` names {', '.join(missing)}, which {DEFAULT_SEAT_IDS.name} has not "
            "registered (ADR-132 D3). State the seat's id and its session slug in the head "
            "(`by: Tech-Architect-NN (<session-slug>)`), then run "
            "`uv run --locked python scripts/transport.py seat-ids --write`")


def _inside_known_transport(dest: Path) -> bool:
    known = known_root()
    return known is not None and is_transport_dest(dest, known)


def write(writer: str, dest: Path, data: str, *, registry: Optional[list[Kind]] = None) -> Path:
    """Write `data` (text) to `dest` WHOLE (atomic tmp+replace, `transport_report.deliver`'s own
    pattern), but only when `dest.name` is a registered kind, `writer` is its registered writer,
    `dest` sits in that kind's registered folder AND `transport_lint` passes the content. The replace
    runs under the destination's lock -- the one `append()` and the janitor's move take -- so no
    registered writer replaces a file between a move's hash check and its rename. Raises
    `TransportWriteRefused` before touching the filesystem otherwise (or when the lock is not released
    within `WRITE_LOCK_TIMEOUT_S`)."""
    reg = registry if registry is not None else load_registry()
    _check(writer, dest, reg)
    _lint(dest, data, reg, writer)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with _DestinationLock(dest, WRITE_LOCK_TIMEOUT_S):      # the lock append() and the janitor's move share
        _tr.deliver(dest, data.encode("utf-8"))
    _after_write(dest, "write", reg)
    return dest


def _same(a: Path, b: Path) -> bool:
    return os.path.normcase(str(a)) == os.path.normcase(str(b))


def is_transport_dest(dest: Path, transport_root: Optional[Path] = None) -> bool:
    """True when `dest` sits in the transport: the root itself (where `LANE-*.md` contracts
    live) or an immediate `to-cc/` / `to-browser/` child of it. The root is `transport_root`,
    else the configured `CLAUDE_PROMPTS_DIR`; paths are resolved and compared case-insensitively
    on Windows, so a scratch directory that merely shares the basename `to-browser` is not the
    transport, and `TO-BROWSER` is. With no root known at all the folder name decides."""
    parent = dest.parent
    raw = transport_root or _tr.windows_user_env("CLAUDE_PROMPTS_DIR") \
        or os.environ.get("CLAUDE_PROMPTS_DIR")
    if not raw:
        return parent.name.lower() in ("to-cc", "to-browser")
    try:
        root, real = Path(raw).resolve(), parent.resolve()
    except OSError:
        return False
    if _same(real, root):
        return True
    return real.name.lower() in ("to-cc", "to-browser") and _same(real.parent, root)


def emit(writer: str, dest: Path, data: str, *, registry: Optional[list[Kind]] = None,
         transport_root: Optional[Path] = None) -> Path:
    """A generator's single write call: a destination inside the transport goes through
    `write()` (registered kind, registered writer, linted content); any other path -- an
    operator's explicit `--out` into a scratch directory -- is a plain atomic write, since it is
    not a transport write."""
    if is_transport_dest(dest, transport_root):
        return write(writer, dest, data, registry=registry)
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
            except (FileExistsError, PermissionError):
                # PermissionError: on Windows O_EXCL against a lock file another thread is
                # deleting (delete-pending) fails with it -- contention, not a denial ([#1350]).
                # A PermissionError that never clears still ends at the deadline below.
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
        existing = dest.read_text(encoding="utf-8", errors="replace") if dest.exists() else ""
        sep = "\n" if existing and not block.startswith("\n") else ""
        tail = "" if block.endswith("\n") else "\n"
        _lint(dest, existing + sep + block + tail, reg, writer)
        with dest.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(sep + block + tail)
        # The INDEX row depends on the first WINDOW_LINES lines (its head keys AND the attribution
        # signals), so the refresh fires when this call created the file or those lines changed.
        fires = not existing or (existing.splitlines()[:WINDOW_LINES]
                                 != (existing + sep + block + tail).splitlines()[:WINDOW_LINES])
    if fires:
        _after_write(dest, "append", reg)
    return dest


# --- the live files, the landing inventory and the seat-ID file ---------------------------------
#
# `ecosystem/seat-ids.yaml` is GENERATED and holds two sections, each rewritten only by its own
# command: `seats:` (`seat-ids --write`: the Tech-Architect-NN <-> session-slug pairs the transport
# heads state, with the file that states each) and `landing_inventory:` (`inventory --write`: every
# live file on the transport at landing, `<folder>/<name>: sha256`). The `by:` rule reads the
# inventory to tell a NEW file from a pre-existing or an edited one; nothing in the lint or the
# gate ever rewrites it.

_SKIP_NAMES = frozenset({"desktop.ini"})


class SeatIdsError(Exception):
    """`ecosystem/seat-ids.yaml` exists but cannot be read; never overwritten blind."""


def rel_key(folder: str, name: str) -> str:
    """The transport-relative key of a file: `<folder>/<name>`, the bare name at the root."""
    return name if folder == "root" else f"{folder}/{name}"


def live_files(root: Path) -> list[tuple[str, Path]]:
    """`(rel, path)` for every live file: a direct child of `to-cc/`, `to-browser/` or the
    root itself (no recursion). Dot-names (the `.tmp` and lock plumbing) and `desktop.ini` are not
    live files. Callers sort for themselves; no caller relies on this order."""
    out: list[tuple[str, Path]] = []
    for folder in FOLDERS:
        home = root if folder == "root" else root / folder
        if not home.is_dir():
            continue
        for entry in sorted(home.iterdir(), key=lambda p: p.name):
            if entry.name.startswith(".") or entry.name in _SKIP_NAMES or not entry.is_file():
                continue
            out.append((rel_key(folder, entry.name), entry))
    return out


def build_inventory(root: Path) -> dict[str, str]:
    """`{rel: sha256}` for every live file except the generated INDEX (whose bytes change with
    every write and which always carries a `by:`)."""
    inv: dict[str, str] = {}
    for rel, path in live_files(root):
        if rel == f"to-browser/{INDEX_NAME}":
            continue
        try:
            inv[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            continue
    return dict(sorted(inv.items()))


_YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def _load_seat_ids_raw(path: Path) -> dict:
    raw = yaml.load(Path(path).read_text(encoding="utf-8"), Loader=_YAML_LOADER)  # noqa: S506 -- safe loader
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise SeatIdsError(f"{path} is not a mapping")
    return raw


def load_seat_ids(path: Path = DEFAULT_SEAT_IDS) -> tuple[list[dict], dict[str, str]]:
    """`(seats, landing_inventory)` from the generated file; a missing file is two empty sections,
    an unreadable one is `SeatIdsError`."""
    if not Path(path).exists():
        return [], {}
    try:
        raw = _load_seat_ids_raw(path)
    except (OSError, yaml.YAMLError, UnicodeDecodeError) as exc:
        raise SeatIdsError(f"could not read {path}: {exc}") from exc
    seats = raw.get("seats") or []
    inv = raw.get("landing_inventory") or {}
    if not isinstance(seats, list) or not isinstance(inv, dict):
        raise SeatIdsError(f"{path}: `seats` is not a list or `landing_inventory` not a mapping")
    return ([dict(s) for s in seats], {str(k): str(v) for k, v in inv.items()})


def load_inventory(path: Path = DEFAULT_SEAT_IDS) -> Optional[dict[str, str]]:
    """The landing inventory, or None when the file is missing, unreadable or has no
    `landing_inventory` mapping -- the `by:` rule then fails closed (every file counts as new)."""
    try:
        raw = _load_seat_ids_raw(Path(path))
    except (OSError, yaml.YAMLError, UnicodeDecodeError, SeatIdsError):
        return None
    inv = raw.get("landing_inventory")
    if not isinstance(inv, dict):
        return None
    return {str(k): str(v) for k, v in inv.items()}


_SEAT_IDS_HEADER = """\
# ecosystem/seat-ids.yaml -- GENERATED; regenerate it, do not edit it by hand.
#
# seats:             the Tech-Architect-NN <-> session-slug pairs the transport heads state, each
#                    with the file that states it (`transport.py seat-ids --write`).
# landing_inventory: every live transport file at landing, `<folder>/<name>: sha256`
#                    (`transport.py inventory --write`). The `by:` rule reads it to tell a new file
#                    from a pre-existing one; the lint and the write gate only read it.
# [#1439] LANE-1439-b2w2-transport-index (batch B2-W3).
"""


def _seat_sort_key(seat: dict) -> tuple:
    m = re.search(r"\d+", str(seat.get("seat", "")))
    return (int(m.group()) if m else 0, str(seat.get("seat", "")), str(seat.get("session", "")))


def _dump(section: dict) -> str:
    return yaml.safe_dump(section, sort_keys=True, allow_unicode=True, default_flow_style=False,
                          width=1_000_000)


def render_seat_ids(seats: list[dict], inventory: dict[str, str]) -> str:
    """The whole generated file as text; the same input is the same bytes."""
    ordered = sorted((dict(s) for s in seats), key=_seat_sort_key)
    return (_SEAT_IDS_HEADER + "\n" + _dump({"seats": ordered}) + "\n"
            + _dump({"landing_inventory": dict(sorted(inventory.items()))}))


def write_seat_ids(path: Path, *, seats: Optional[list[dict]] = None,
                   inventory: Optional[dict[str, str]] = None) -> Path:
    """Write the generated file. A section passed as None keeps the file's existing one (empty
    when there is no file), so each command rewrites only its own section."""
    path = Path(path)
    cur_seats, cur_inv = load_seat_ids(path)
    text = render_seat_ids(cur_seats if seats is None else seats,
                           cur_inv if inventory is None else inventory)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(text.encode("utf-8"))
    os.replace(tmp, path)
    return path


# --- the generated INDEX, the attribution rule and the seat-ID map ------------------------------
#
# LANE-1439-b2w2-transport-index (batch B2-W3). `to-browser/INDEX.md` lists the CURRENT files of this
# repository's kinds, grouped by kind then writer, newest first, every entry with kind, subject, date
# and `by:`. It is GENERATED: `index --write` builds it whole; once it exists `write()` / `append()`
# refresh it (see `refresh_index`), and a test holds the incremental result equal to a full rebuild.
#
# ATTRIBUTION (the amend's S-10 C3 + S-17 + S-40). A file is attributed to this repository when, after
# the foreign veto, its first 30 lines carry (a) the repository token, (b) a Tech-Architect id or a
# session slug of the seat map, or (c) a cited transport file name that classifies as a hub-scope kind.
# The veto `W` is derived from the transport (the `<name>` of every `LEDGER-<name>` that is not this
# repository) plus the file-name segment `cv`; a vetoed file is `UNATTRIBUTED`: listed in its own
# section, never moved. Stated limit (S-17): no head signal can tell a foreign file that names this
# repository from one of ours, so the janitor's exposure is bounded by the seat reviewing its dry run.

class EmptySeatMap(Exception):
    """The seat-ID map is empty: attribution signal (b) has nothing to read, so the run refuses."""


class JanitorRefused(Exception):
    """`janitor --apply` refused: the reviewed manifest hash is missing, malformed or no longer the
    plan's. Nothing is moved."""


HEAD_LINES = 12          # the lines the head keys (`by:`, `date:`, `summary:`, `supersedes:`) are read from
WINDOW_LINES = 30        # the attribution window; a row depends on ALL of it, never just the head
INDEX_LOCK_TIMEOUT_S = 10.0
JANITOR_LOCK_TIMEOUT_S = 10.0   # how long a move waits for a writer that holds the source's append lock
WRITE_LOCK_TIMEOUT_S = 10.0     # how long a whole-file write waits for the destination's lock
STALE_MARGIN_S = 5.0            # a cached INDEX row is trusted only for a file older than the INDEX by this much
INDEX_SUMMARY = "Generated index of the current transport files, by kind and writer, newest first."
INDEX_BY = "transport.py index (generated)"
UNKNOWN = "UNKNOWN"
UNDATED = "undated"
NO_SUBJECT = "(no subject)"
_INDEX_REL = f"to-browser/{INDEX_NAME}"

_TA_RE = re.compile(r"Tech-Architect-\d+")
_SLUG_RE = re.compile(r"(?<![A-Za-z0-9-])\d{4}-\d{2}-\d{2}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_HEAD_KEY_RE = re.compile(r"^(by|date|supersedes|summary|answers|timeout):[ \t]*(.*?)[ \t]*$")
_FROM_BY_RE = re.compile(r"^(?:from|by):[ \t]*(.*)$")
_CITED_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.md")
_SUPERSEDED_RE = re.compile(r"(?<![A-Za-z0-9])superseded(?![A-Za-z0-9])", re.I)
_LEDGER_RE = re.compile(r"^LEDGER-(.+)\.md$", re.I)
_LEDGER_TAIL_RE = re.compile(r"-(?:\d{4}-\d{2}-\d{2}|superseded|v\d+)$")
_REPO_RE = re.compile(rf"\b{re.escape(REPO_TOKEN)}\b", re.I)
_EXT_RE = re.compile(r"\.[A-Za-z0-9]{1,6}$")


def _utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp_epoch(stamp: Optional[str]) -> Optional[float]:
    """Seconds since the epoch of a `regenerated:` stamp, or None when it does not parse."""
    from datetime import datetime, timezone
    try:
        return datetime.strptime(stamp or "", "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        return None


def seatmap_digest(seats: list[dict]) -> str:
    text = "\n".join(sorted(f"{s['seat']}={s['session']}" for s in seats))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def name_has_cv_segment(name: str) -> bool:
    """S-40: the file-name segment `cv`, matched only as a whole hyphen-delimited segment of the
    name without its final extension -- never inside a longer word (`recv`, `cvs`, `devcv`) and
    never in a head."""
    return "cv" in _EXT_RE.sub("", name).lower().split("-")


def veto_tokens(files: list[tuple[str, Path]]) -> list[str]:
    """`W`'s derived part: the `<name>` of every `LEDGER-<name>[-vN][-superseded][-date].md` on the
    transport that is not this repository, normalised (lower-case, `_` as `-`)."""
    out: set[str] = set()
    for _rel, path in files:
        m = _LEDGER_RE.match(path.name)
        if not m:
            continue
        tok = m.group(1).lower().replace("_", "-")
        while True:
            new = _LEDGER_TAIL_RE.sub("", tok)
            if new == tok:
                break
            tok = new
        if tok and tok != REPO_TOKEN:
            out.add(tok)
    return sorted(out)


def _read_window_checked(path: Path) -> tuple[list[str], bool]:
    """`(lines, readable)`: the first `WINDOW_LINES` lines of a `.md` file (others carry no head),
    LF-normalised. `readable` is False when the open or the read failed -- the lines are then empty, and
    a row built from them says so instead of passing for a file with no head."""
    if path.suffix.lower() != ".md":
        return [], True
    try:
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            return [ln.rstrip("\r\n") for ln in itertools.islice(fh, WINDOW_LINES)], True
    except OSError:
        return [], False


def _read_window(path: Path) -> list[str]:
    return _read_window_checked(path)[0]


def _head_keys(lines: list[str]) -> tuple[dict[str, str], Optional[str]]:
    keys: dict[str, str] = {}
    heading: Optional[str] = None
    for ln in lines[:HEAD_LINES]:
        m = _HEAD_KEY_RE.match(ln)
        if m:
            if m.group(2) and m.group(1) not in keys:
                keys[m.group(1)] = m.group(2)
        elif heading is None and ln.startswith("# "):
            heading = ln[2:].strip()
    return keys, heading


def _clean(text: str, limit: Optional[int] = None) -> str:
    text = re.sub(r"\s+", " ", text.replace("|", "/")).strip()
    return text[:limit].rstrip() if limit else text


@dataclass(frozen=True)
class _Row:
    path: str
    kind: str
    subject: str
    date: str
    by: str                       # the `by:` value as written, or UNKNOWN
    attributed: bool
    supersedes: Optional[str] = None
    readable: bool = True         # False: the head could not be read (the row is a placeholder)
    answers: Optional[str] = None
    timeout: Optional[str] = None


class _Attr:
    """The attribution rule, evaluated per file for every kind (a hub-scope kind earns nothing by its
    scope). Built once per run from the live files (the veto), the seat map and the registry."""

    def __init__(self, files: list[tuple[str, Path]], seats: list[dict], reg: list[Kind]):
        self.reg = reg
        self.veto = veto_tokens(files)
        self.veto_re = (re.compile(r"(?<![a-z0-9])(?:" + "|".join(
            re.escape(t) for t in sorted(self.veto, key=len, reverse=True)) + r")(?![a-z0-9])")
            if self.veto else None)
        self.slug_to_seat = {s["session"]: s["seat"] for s in seats}
        self.slug_re = (re.compile(r"(?<![A-Za-z0-9-])(?:" + "|".join(
            re.escape(s) for s in sorted(self.slug_to_seat, key=len, reverse=True)) + r")(?![A-Za-z0-9-])")
            if self.slug_to_seat else None)

    def attributed(self, name: str, lines: list[str]) -> bool:
        if name_has_cv_segment(name):
            return False
        text = "\n".join(lines)
        if self.veto_re is not None and (
                self.veto_re.search(name.lower().replace("_", "-"))
                or self.veto_re.search(text.lower().replace("_", "-"))):
            return False
        if _REPO_RE.search(text) or _TA_RE.search(text):
            return True
        if self.slug_re is not None and self.slug_re.search(text):
            return True
        for cited in _CITED_RE.findall(text):
            kind = classify(cited, self.reg) if cited != name else None
            if kind is not None and kind.repo_scope == "hub":
                return True
        return False


def _scan_row(rel: str, path: Path, kind: Kind, attr: _Attr) -> _Row:
    lines, readable = _read_window_checked(path)
    keys, heading = _head_keys(lines)
    if keys.get("summary"):
        subject = _clean(keys["summary"], 100)
    elif heading:
        subject = _clean(heading, 100) or NO_SUBJECT
    else:
        subject = NO_SUBJECT
    m = _DATE_RE.search(keys.get("date", ""))
    named = _DATE_RE.findall(path.name)
    date = m.group() if m else (named[-1] if named else UNDATED)
    by = _clean(keys["by"], 120) if keys.get("by") else UNKNOWN
    sup = _clean(keys["supersedes"], 200) if keys.get("supersedes") else None
    answers = _clean(keys["answers"], 200) if keys.get("answers") else None
    timeout = _clean(keys["timeout"], 200) if keys.get("timeout") else None
    return _Row(rel, kind.name, subject, date, by or UNKNOWN, attr.attributed(path.name, lines), sup,
                readable, answers, timeout)


def writer_key(by: str, slug_to_seat: dict[str, str]) -> str:
    """The group a `by:` value files under: a `Tech-Architect-NN` token wins, else a session slug of
    the seat map resolves to its seat, else the text before the first parenthesis / dash / comma."""
    if not by or by == UNKNOWN:
        return UNKNOWN
    m = _TA_RE.search(by)
    if m:
        return m.group()
    for slug in sorted(slug_to_seat):
        if re.search(rf"(?<![A-Za-z0-9-]){re.escape(slug)}(?![A-Za-z0-9-])", by):
            return slug_to_seat[slug]
    head = re.split(r" \(| — | · |,|;", by, maxsplit=1)[0].strip()
    return head[:48] or UNKNOWN


def _supersede_targets(rows: list[_Row]) -> set[str]:
    out: set[str] = set()
    for r in rows:
        if r.attributed and r.supersedes:
            for tok in re.split(r"[,;\s]+", r.supersedes):
                tok = tok.strip("`'\"()[]<>")
                if tok:
                    out.add(tok.rsplit("/", 1)[-1])
    return out


def _by_date_desc(rows: list[_Row]) -> list[_Row]:
    """Newest first; a tie by path ascending; undated last (no mtime anywhere)."""
    rows = sorted(rows, key=lambda r: r.path)
    return sorted(rows, key=lambda r: (r.date != UNDATED, r.date), reverse=True)


def _row_line(r: _Row) -> str:
    line = f"- {r.path} | {r.kind} | {r.subject} | {r.date} | by: {r.by}"
    if r.answers:
        line += f" | answers: {r.answers}"
    if r.timeout:
        line += f" | timeout: {r.timeout}"
    return line


def _inputs_line(veto: list[str], digest: str) -> str:
    return f"veto={','.join(veto) or '-'} seatmap={digest}"


def _assemble(rows: list[_Row], *, n_unclassified: int, veto: list[str], digest: str,
              slug_to_seat: dict[str, str], stamp: str, trigger: str) -> str:
    n_unreadable = sum(1 for r in rows if not r.readable)
    me = _Row(_INDEX_REL, "INDEX", INDEX_SUMMARY, stamp[:10], INDEX_BY, True)
    rows = [r for r in rows if r.path != _INDEX_REL] + [me]
    listed = [r for r in rows if r.attributed]
    unattr = [r for r in rows if not r.attributed]
    targets = _supersede_targets(listed)

    def is_superseded(r: _Row) -> bool:
        base = r.path.rsplit("/", 1)[-1]
        return bool(_SUPERSEDED_RE.search(base)) or base in targets

    superseded = [r for r in listed if is_superseded(r)]
    current = [r for r in listed if not is_superseded(r)]
    by_kind_unattr: dict[str, int] = {}
    for r in unattr:
        by_kind_unattr[r.kind] = by_kind_unattr.get(r.kind, 0) + 1
    out = [
        f"by: {INDEX_BY}", f"date: {stamp[:10]}", f"summary: {INDEX_SUMMARY}",
        f"regenerated: {stamp}", f"trigger: {trigger}", f"inputs: {_inputs_line(veto, digest)}",
        "", "# INDEX — current files on the transport", "",
        "Generated by `transport.py index --write`. Regenerate it; do not edit it by hand.", "",
        f"repository: {REPO_TOKEN}", f"live: {len(rows) + n_unclassified}", f"classified: {len(rows)}",
        f"listed: {len(listed)}", f"current: {len(current)}", f"superseded: {len(superseded)}",
        f"UNATTRIBUTED: {len(unattr)}", f"unclassified: {n_unclassified}",
        *([f"unreadable: {n_unreadable}"] if n_unreadable else []),
        "UNATTRIBUTED by kind: " + (", ".join(f"{k}={n}" for k, n in sorted(by_kind_unattr.items())) or "-"),
        "",
    ]

    def by_kind(group: list[_Row]) -> dict[str, list[_Row]]:
        kinds: dict[str, list[_Row]] = {}
        for r in group:
            kinds.setdefault(r.kind, []).append(r)
        return dict(sorted(kinds.items()))

    def flat_section(title: str, group: list[_Row]) -> None:
        out.extend([f"## {title}", ""])
        if not group:
            out.extend(["(none)", ""])
        for kind, krows in by_kind(group).items():
            out.extend([f"### {kind} ({len(krows)})", ""])
            out.extend(_row_line(r) for r in _by_date_desc(krows))
            out.append("")

    out.extend(["## Current", ""])
    for kind, krows in by_kind(current).items():
        out.extend([f"### {kind} ({len(krows)})", ""])
        groups: dict[str, list[_Row]] = {}
        for r in krows:
            groups.setdefault(writer_key(r.by, slug_to_seat), []).append(r)
        real = sorted(w for w in groups if w != UNKNOWN)
        real.sort(key=lambda w: max((r.date for r in groups[w] if r.date != UNDATED), default=""),
                  reverse=True)
        for w in real + ([UNKNOWN] if UNKNOWN in groups else []):
            out.extend([f"#### {w} ({len(groups[w])})", ""])
            out.extend(_row_line(r) for r in _by_date_desc(groups[w]))
            out.append("")
    flat_section("Superseded", superseded)
    flat_section("UNATTRIBUTED", unattr)
    out.extend(["## Supersedes edges", ""])
    edges = sorted((r.path, r.supersedes) for r in listed if r.supersedes)
    out.extend([f"- {p} supersedes {raw}" for p, raw in edges] or ["(none)"])
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def parse_index(text: str) -> dict:
    """`{header, entries, edges}` of a generated INDEX: `header` maps each flush-left `key: value`
    line before the first section; `entries` are `{path, kind, subject, date, by, status}`
    (`status`: current / superseded / unattributed); `edges` are `(path, raw supersedes value)`."""
    header: dict[str, str] = {}
    entries: list[dict] = []
    edges: list[tuple[str, str]] = []
    section: Optional[str] = None
    names = {"Current": "current", "Superseded": "superseded", "UNATTRIBUTED": "unattributed",
             "Supersedes edges": "edges"}
    for ln in text.splitlines():
        if ln.startswith("## "):
            section = names.get(ln[3:].strip())
            continue
        if section is None:
            m = re.match(r"^([A-Za-z][A-Za-z ]*): (.*)$", ln)
            if m:
                header.setdefault(m.group(1), m.group(2))
            continue
        if section == "edges":
            m = re.match(r"^- (\S+) supersedes (.+)$", ln)
            if m:
                edges.append((m.group(1), m.group(2)))
            continue
        if ln.startswith("- ") and " | " in ln:
            parts = ln[2:].split(" | ")
            if len(parts) >= 5 and parts[4].startswith("by: "):
                entry = {"path": parts[0], "kind": parts[1], "subject": parts[2],
                         "date": parts[3], "by": parts[4][4:], "status": section}
                extras = [re.match(r"^(answers|timeout): (.*)$", p) for p in parts[5:]]
                if all(extras):
                    for m in extras:
                        entry[m.group(1)] = m.group(2)
                    entries.append(entry)
    return {"header": header, "entries": entries, "edges": edges}


QUERY_STATUSES = ("current", "superseded", "unattributed", "all")


def _norm_kind(kind: str) -> str:
    return kind.strip().upper().replace("-", "_")


def query_index(text: str, *, kind: Optional[str] = None, date: Optional[str] = None,
                seat: Optional[str] = None, status: str = "current",
                slug_to_seat: Optional[dict[str, str]] = None) -> list[dict]:
    """The INDEX rows that match every filter given, in the INDEX's own order. `kind` matches the
    kind name without case (a hyphen reads as an underscore); `date` matches the row's date or its
    prefix (`2026-10` is the month); `seat` matches the row's writer group (`writer_key`) -- a
    `Tech-Architect-NN`, `UNKNOWN`, or a session slug the seat map resolves to its seat; `status` is
    one of `QUERY_STATUSES`. Each returned row carries its `seat` (the writer group). A pure read of
    the generated text: no live file is opened."""
    if status not in QUERY_STATUSES:
        raise ValueError(f"status {status!r} is not one of {', '.join(QUERY_STATUSES)}")
    slug_to_seat = dict(slug_to_seat or {})
    want_seat = None
    if seat is not None:
        want_seat = slug_to_seat.get(seat.strip(), seat.strip()).lower()
    want_kind = _norm_kind(kind) if kind is not None else None
    out: list[dict] = []
    for e in parse_index(text)["entries"]:
        if status != "all" and e["status"] != status:
            continue
        if want_kind is not None and _norm_kind(e["kind"]) != want_kind:
            continue
        if date is not None and not e["date"].startswith(date.strip()):
            continue
        group = writer_key(e["by"], slug_to_seat)
        if want_seat is not None and group.lower() != want_seat:
            continue
        out.append({**e, "seat": group})
    return out


def build_index(root: Path, *, seats: list[dict], generated_at: Optional[str] = None,
                trigger: str = "index", registry: Optional[list[Kind]] = None) -> str:
    """The whole INDEX text, rebuilt from the live files. Raises `EmptySeatMap` with no seats."""
    if not seats:
        raise EmptySeatMap("the seat-ID map is empty: attribution signal (b) has nothing to read")
    reg = registry if registry is not None else load_registry()
    stamp = generated_at or _utc_now()      # taken before any file is read: no later edit can predate it
    files = _scan_files(root)
    attr = _Attr(files, seats, reg)
    rows: list[_Row] = []
    n_unclassified = 0
    for rel, path in files:
        kind = classify(path.name, reg)
        if kind is None:
            n_unclassified += 1
        else:
            rows.append(_scan_row(rel, path, kind, attr))
    return _assemble(rows, n_unclassified=n_unclassified, veto=attr.veto, digest=seatmap_digest(seats),
                     slug_to_seat=attr.slug_to_seat, stamp=stamp, trigger=trigger)


_INDEX_RELS = (_INDEX_REL, _ARCHIVE_REL)


def _scan_files(root: Path) -> list[tuple[str, Path]]:
    return [(rel, p) for rel, p in live_files(Path(root)) if rel not in _INDEX_RELS]


def _rows_from_index(parsed: dict) -> dict[str, _Row]:
    edge = dict(parsed["edges"])
    return {e["path"]: _Row(e["path"], e["kind"], e["subject"], e["date"], e["by"],
                            e["status"] != "unattributed", edge.get(e["path"]),
                            answers=e.get("answers"), timeout=e.get("timeout"))
            for e in parsed["entries"] if e["path"] not in _INDEX_RELS}


# --- the request status and the current view ----------------------------------------------------------

def _parse_when(value) -> Optional[object]:
    """A UTC datetime from a datetime or an ISO stamp (`YYYY-MM-DD` reads as 00:00Z), else None."""
    from datetime import datetime, timezone
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value or "").strip()
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _answer_names(raw: Optional[str]) -> set[str]:
    out: set[str] = set()
    for tok in re.split(r"[,;\s]+", raw or ""):
        tok = tok.strip("`'\"()[]<>")
        if tok:
            out.add(tok.replace("\\", "/").rsplit("/", 1)[-1])
    return out


def request_status(parsed: dict, now) -> dict[str, tuple[str, str]]:
    """`{path: (status, detail)}` for each in-era current request (`REQUEST_KINDS`, dated on or after
    `ANSWERS_ERA`). ANSWERED when any row's `answers:` names the request's basename; else OVERDUE when
    `now` is past its `timeout:` (default: its date + `REQUEST_TIMEOUT_DAYS`, at 00:00Z); else OPEN.
    `now` is a datetime or an ISO stamp. The request file is never read."""
    from datetime import timedelta
    now_dt = _parse_when(now)
    if now_dt is None:
        raise ValueError(f"cannot read {now!r} as a time")
    answered: set[str] = set()
    for e in parsed["entries"]:
        answered |= _answer_names(e.get("answers"))
    out: dict[str, tuple[str, str]] = {}
    for e in parsed["entries"]:
        if (e["kind"] not in REQUEST_KINDS or e["status"] != "current" or e["date"] == UNDATED
                or e["date"] < ANSWERS_ERA):
            continue
        base = e["path"].rsplit("/", 1)[-1]
        if base in answered:
            by_path = sorted(x["path"] for x in parsed["entries"] if base in _answer_names(x.get("answers")))
            out[e["path"]] = ("ANSWERED", f"answered by {by_path[0]}")
            continue
        due = _parse_when(e.get("timeout"))
        if due is None:
            start = _parse_when(e["date"])
            if start is None:
                continue
            due = start + timedelta(days=REQUEST_TIMEOUT_DAYS)
        shown = due.strftime("%Y-%m-%d") if (due.hour, due.minute, due.second) == (0, 0, 0) \
            else due.strftime("%Y-%m-%dT%H:%M:%SZ")
        if now_dt > due:
            out[e["path"]] = ("OVERDUE", f"timeout {shown}")
        else:
            out[e["path"]] = ("OPEN", f"due {shown}")
    return out


VIEW_SUMMARY = ("Generated inbox view: open requests and the current files of the last "
                f"{CURRENT_DAYS} days, by seat and session; history is in {ARCHIVE_INDEX_NAME}.")
_REQUEST_ORDER = {"OVERDUE": 0, "OPEN": 1, "ANSWERED": 2}


def build_view(archive_text: str, *, slug_to_seat: Optional[dict] = None) -> str:
    """`INDEX.md`: a pure function of the archive text. Its `now` is the archive's `regenerated:`
    stamp. Requests first (OVERDUE, OPEN, ANSWERED), then the current dated rows of the last
    `CURRENT_DAYS` days by seat and session. Over `INDEX_BYTE_CAP` the window shrinks a day at a
    time, then the oldest rows are cut for a pointer line, so the size always holds."""
    from datetime import timedelta
    parsed = parse_index(archive_text)
    header = parsed["header"]
    now = _parse_when(header.get("regenerated")) or _parse_when(_utc_now())
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    today = now.strftime("%Y-%m-%d")
    seat_session = {}
    for slug, seat in sorted((slug_to_seat or {}).items(), reverse=True):
        seat_session[seat] = slug
    live = [e for e in parsed["entries"] if e["path"] not in _INDEX_RELS]
    status = request_status({**parsed, "entries": live}, now)
    reqs = sorted((e for e in live if e["path"] in status),
                  key=lambda e: (_REQUEST_ORDER[status[e["path"]][0]], e["date"], e["path"]))
    cur_all = [e for e in live if e["status"] == "current" and e["date"] != UNDATED]
    n_overdue = sum(1 for e in reqs if status[e["path"]][0] == "OVERDUE")

    def render(days: int, n_cur: Optional[int], n_req: Optional[int]) -> str:
        lo = (now - timedelta(days=days)).strftime("%Y-%m-%d")
        rows = [e for e in cur_all if lo <= e["date"] <= today]
        rows.sort(key=lambda e: e["path"])
        rows.sort(key=lambda e: e["date"], reverse=True)
        cut = 0 if n_cur is None else len(rows) - n_cur
        if cut > 0:
            rows = rows[:n_cur]
        rq = reqs if n_req is None else reqs[:n_req]
        out = [f"by: {INDEX_BY}", f"date: {today}", f"summary: {VIEW_SUMMARY}", f"regenerated: {stamp}",
               f"archive: {_ARCHIVE_REL}", f"window: {lo}..{today}", f"current: {len(rows)}",
               f"requests: {len(reqs)}", f"overdue: {n_overdue}",
               "", "# INDEX — the transport inbox", "", "## Requests", ""]
        for e in rq:
            st, detail = status[e["path"]]
            out.append(f"- {e['path']} | {st} | {e['date']} | {_clean(e['subject'], 80)} | {detail}")
        if not rq:
            out.append("(none)")
        if n_req is not None and len(reqs) > n_req:
            out.append(f"- … {len(reqs) - n_req} more rows in {ARCHIVE_INDEX_NAME}")
        out.extend(["", "## Current", ""])
        groups: dict[tuple[str, str], list[dict]] = {}
        for e in rows:
            key = writer_key(e["by"], slug_to_seat or {})
            groups.setdefault((key, seat_session.get(key, "")), []).append(e)
        ordered = sorted(groups, key=lambda k: (k[0] == UNKNOWN, k[0]))
        ordered.sort(key=lambda k: groups[k][0]["date"], reverse=True)
        for k in ordered:
            head = k[0] + (f" · {k[1]}" if k[1] else "")
            out.extend([f"### {head} ({len(groups[k])})", ""])
            out.extend(f"- {e['path']} | {e['kind']} | {e['date']} | {_clean(e['subject'], 80)}"
                       for e in groups[k])
            out.append("")
        if not rows:
            out.extend(["(none)", ""])
        if cut > 0:
            out.extend([f"- … {cut} more rows in {ARCHIVE_INDEX_NAME}", ""])
        while out and out[-1] == "":
            out.pop()
        return "\n".join(out) + "\n"

    def fits(text: str) -> bool:
        return len(text.encode("utf-8")) <= INDEX_BYTE_CAP

    for days in range(CURRENT_DAYS, 0, -1):
        text = render(days, None, None)
        if fits(text):
            return text
    n_rows = len([e for e in cur_all if (now - timedelta(days=1)).strftime("%Y-%m-%d") <= e["date"] <= today])
    lo_n, hi_n = 0, n_rows
    best: Optional[str] = None
    while lo_n <= hi_n:
        mid = (lo_n + hi_n) // 2
        text = render(1, mid, None)
        if fits(text):
            best, lo_n = text, mid + 1
        else:
            hi_n = mid - 1
    if best is not None:
        return best
    lo_n, hi_n = 0, len(reqs)
    while lo_n <= hi_n:
        mid = (lo_n + hi_n) // 2
        text = render(1, 0, mid)
        if fits(text):
            best, lo_n = text, mid + 1
        else:
            hi_n = mid - 1
    return best if best is not None else render(1, 0, 0)


def _is_same_file(a: Path, b: Path) -> bool:
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def _older_than(path: Path, cutoff: Optional[float]) -> bool:
    """True when `path` was last modified before `cutoff` (epoch seconds). The mtime only decides whether a
    cached INDEX row can be trusted; it is never read as a date (the INDEX dates come from the file's
    own head or name). No cutoff, or an unreadable file, is not older: the row is scanned afresh."""
    if cutoff is None:
        return False
    try:
        return path.stat().st_mtime < cutoff
    except OSError:
        return False


def refresh_index(dest: Path, *, trigger: str, root: Path, seats: list[dict],
                  registry: Optional[list[Kind]] = None, stamp: Optional[str] = None) -> bool:
    """Bring an EXISTING INDEX up to date after `dest` was written. Reads no head but `dest`'s (and a
    new file's), so it is cheap enough for every writer; but it is no shortcut around the rule: the
    header records `inputs:` (the veto set and the seat-map digest) and ANY difference rebuilds in
    full, so a new `LEDGER-<other>` re-evaluates every row. A cached row is reused only for a file not
    modified since the INDEX was made (its `regenerated:` stamp, less `STALE_MARGIN_S`): an edit an
    earlier, failed refresh never saw is scanned afresh here. The result equals a full rebuild at the
    same stamp and trigger (a test holds it). The cache is `INDEX-ARCHIVE.md`, else a legacy full-format
    `INDEX.md`; both files are written. False when neither exists."""
    to_browser = Path(root) / "to-browser"
    archive_path = to_browser / ARCHIVE_INDEX_NAME
    cache_path = archive_path if archive_path.is_file() else to_browser / INDEX_NAME
    if not cache_path.is_file():
        return False
    if not seats:
        raise EmptySeatMap("the seat-ID map is empty: attribution signal (b) has nothing to read")
    reg = registry if registry is not None else load_registry()
    stamp = stamp or _utc_now()
    with _DestinationLock(archive_path, INDEX_LOCK_TIMEOUT_S):
        parsed = parse_index(cache_path.read_text(encoding="utf-8"))
        files = _scan_files(root)
        attr = _Attr(files, seats, reg)
        digest = seatmap_digest(seats)
        if parsed["header"].get("inputs") != _inputs_line(attr.veto, digest):
            new = build_index(root, seats=seats, generated_at=stamp, trigger=trigger, registry=reg)
        else:
            old = _rows_from_index(parsed)
            since = _stamp_epoch(parsed["header"].get("regenerated"))
            cutoff = None if since is None else since - STALE_MARGIN_S
            if parsed["header"].get("unreadable", "0") not in ("", "0"):
                cutoff = None      # a head could not be read when the INDEX was made: no cached row is trusted
            rows: list[_Row] = []
            n_unclassified = 0
            for rel, path in files:
                kind = classify(path.name, reg)
                if kind is None:
                    n_unclassified += 1
                    continue
                prev = old.get(rel)
                if (prev is not None and prev.kind == kind.name and not _is_same_file(path, dest)
                        and _older_than(path, cutoff)):
                    rows.append(prev)
                else:
                    rows.append(_scan_row(rel, path, kind, attr))
            new = _assemble(rows, n_unclassified=n_unclassified, veto=attr.veto, digest=digest,
                            slug_to_seat=attr.slug_to_seat, stamp=stamp, trigger=trigger)
        _write_both(root, new, slug_to_seat=attr.slug_to_seat, registry=reg, locked=True)
    return True


def _write_both(root: Path, archive_text: str, *, slug_to_seat: Optional[dict] = None,
                registry: Optional[list[Kind]] = None, locked: bool = False) -> None:
    """Write `INDEX-ARCHIVE.md` (the full text) and `INDEX.md` (its view) as ONE act under the archive's
    lock -- the lock `refresh_index` holds -- so a concurrent refresh never interleaves between the two
    and leaves a view of another archive (Codex terra HIGH, this lane's review). The caller that already
    holds that lock passes `locked`."""
    to_browser = Path(root) / "to-browser"
    view = build_view(archive_text, slug_to_seat=slug_to_seat)
    pair = ((to_browser / ARCHIVE_INDEX_NAME, archive_text), (to_browser / INDEX_NAME, view))
    if locked:
        for path, text in pair:
            _tr.deliver(path, text.encode("utf-8"))
        return
    reg = registry if registry is not None else load_registry()
    for path, _text in pair:
        _check("transport", path, reg)               # registered kind, registered writer, its own folder
    to_browser.mkdir(parents=True, exist_ok=True)
    with _DestinationLock(pair[0][0], INDEX_LOCK_TIMEOUT_S):
        for path, text in pair:
            _tr.deliver(path, text.encode("utf-8"))


def index_stale(root: Path) -> bool:
    """True when `INDEX-ARCHIVE.md` is missing, when the classified live files differ from its rows, or
    when any live file is as new as the archive (its `regenerated:` stamp, less `STALE_MARGIN_S`).
    A pure read."""
    root = Path(root)
    archive_path = root / "to-browser" / ARCHIVE_INDEX_NAME
    try:
        parsed = parse_index(archive_path.read_text(encoding="utf-8"))
    except OSError:
        return True
    reg = load_registry()
    live = {rel: p for rel, p in _scan_files(root) if classify(p.name, reg) is not None}
    if set(live) != {e["path"] for e in parsed["entries"] if e["path"] not in _INDEX_RELS}:
        return True
    since = _stamp_epoch(parsed["header"].get("regenerated"))
    if since is None:
        return True
    cutoff = since - STALE_MARGIN_S
    for p in live.values():
        try:
            if p.stat().st_mtime >= cutoff:
                return True
        except OSError:
            return True
    return False


def _after_write(dest: Path, verb: str, reg: list[Kind]) -> None:
    """The INDEX trigger (Done 5): after a write or append of a classified file inside the known
    transport, refresh the INDEX when one exists. Fails open -- a held lock, a permission error or any
    other fault is a stderr line and the caller's write stands. Never fires for the INDEX itself."""
    try:
        known = known_root()
        if known is None or not is_transport_dest(dest, known):
            return
        folder = _folder_of(dest)
        if folder == "to-browser" and dest.name in (INDEX_NAME, ARCHIVE_INDEX_NAME):
            return
        if classify(dest.name, reg) is None:
            return
        if not any((Path(known) / "to-browser" / n).is_file() for n in (ARCHIVE_INDEX_NAME, INDEX_NAME)):
            return
        seats, _inv = load_seat_ids(DEFAULT_SEAT_IDS)
        refresh_index(dest, trigger=f"{verb}:{rel_key(folder, dest.name)}", root=Path(known),
                      seats=seats, registry=reg)
    except Exception as exc:  # noqa: BLE001 -- fail open: the index is derived, the write is the fact
        print(f"transport: INDEX refresh skipped ({type(exc).__name__}: {exc})", file=sys.stderr)


# --- the seat-ID map ----------------------------------------------------------------------------

def build_seat_map(root: Path) -> dict:
    """The Tech-Architect-NN <-> session-slug pairs the transport heads STATE: a `.md` file whose first
    12 lines (`from:` and `by:` values together) hold exactly one seat id and exactly one session slug
    states that pair. A seat with two sessions, or a session with two seats, is a conflict: reported,
    excluded. Provenance is the first stating file in (folder, name) order. Never guessed."""
    stated: dict[tuple[str, str], list[tuple[int, str, str]]] = {}
    for rel, path in live_files(Path(root)):
        if not path.name.endswith(".md"):
            continue
        values = [m.group(1) for ln in _read_window(path)[:HEAD_LINES] if (m := _FROM_BY_RE.match(ln))]
        seats = {s for v in values for s in _TA_RE.findall(v)}
        slugs = {s for v in values for s in _SLUG_RE.findall(v)}
        if len(seats) == 1 and len(slugs) == 1:
            folder = rel.split("/", 1)[0] if "/" in rel else "root"
            stated.setdefault((seats.pop(), slugs.pop()), []).append((FOLDERS.index(folder), path.name, rel))
    by_seat: dict[str, set[str]] = {}
    by_session: dict[str, set[str]] = {}
    for seat, session in stated:
        by_seat.setdefault(seat, set()).add(session)
        by_session.setdefault(session, set()).add(seat)
    conflicts: list[dict] = [{"seat": s, "sessions": sorted(v)} for s, v in sorted(by_seat.items())
                             if len(v) > 1]
    conflicts += [{"seat": "-", "session": s, "seats": sorted(v)} for s, v in sorted(by_session.items())
                  if len(v) > 1]
    seats_out = []
    for (seat, session), files in stated.items():
        if len(by_seat[seat]) > 1 or len(by_session[session]) > 1:
            continue
        seats_out.append({"seat": seat, "session": session,
                          "provenance": min(files)[2], "stated_in": len(files)})
    seats_out.sort(key=_seat_sort_key)
    return {"seats": seats_out, "conflicts": conflicts}


# --- the janitor ----------------------------------------------------------------------------------
#
# Moves (never deletes) the `-superseded` files of registered, attributable kinds into
# `<folder>/archive/YYYY-MM/` (`archive/undated/` when the file carries no date of its own). The month
# is the file's own date -- the head `date:`, else the last YYYY-MM-DD in its name -- and NEVER its
# mtime (Drive rewrites that). The dry run prints the full move list and a `manifest-sha256`; `--apply`
# needs that hash, replans, and refuses when the plan no longer hashes to it, so the run moves exactly
# the list that was read. A move is a no-replace rename (`_rename_no_replace`) after an explicit
# "destination absent" check -- never a copy-then-delete, `os.replace`, `unlink` or `rmtree`. The readers (`gen_handoff._question_files`,
# `_question_disposition_verdict`) glob `archive/*/`, one level down, where these moves land.

def _archive_month(lines: list[str], name: str) -> tuple[str, str]:
    keys, _heading = _head_keys(lines)
    m = re.search(r"(\d{4}-\d{2})-\d{2}", keys.get("date", ""))
    if m:
        return m.group(1), "head"
    named = _DATE_RE.findall(name)
    if named:
        return named[-1][:7], "name"
    return UNDATED, "undated"


def _home_of(root: Path, folder: str) -> Path:
    return Path(root) if folder == "root" else Path(root) / folder


def _census(root: Path) -> dict[str, int]:
    archive = 0
    for folder in FOLDERS:
        a = _home_of(root, folder) / "archive"
        if a.is_dir():
            archive += sum(1 for p in a.rglob("*") if p.is_file())
    return {"live": len(live_files(root)), "archive": archive}


def _tree_shas(root: Path) -> list[str]:
    paths = [p for _rel, p in live_files(root)]
    for folder in FOLDERS:
        a = _home_of(root, folder) / "archive"
        if a.is_dir():
            paths.extend(p for p in a.rglob("*") if p.is_file())
    return sorted(hashlib.sha256(p.read_bytes()).hexdigest() for p in paths)


def _manifest_hash(moves: list[dict]) -> str:
    lines = sorted(f"{m['source']}|{m['destination']}|{m['sha256']}" for m in moves)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def janitor_plan(root: Path, *, seats: list[dict], registry: Optional[list[Kind]] = None) -> dict:
    """What the janitor would move, and why it leaves the rest. Reads, moves nothing. Candidates are
    live `-superseded` files that are classified, in their kind's own folder and attributed (the
    same rule the INDEX uses, so a vetoed file is `UNATTRIBUTED`, not a candidate); a destination
    that already exists is a `COLLISION`, reported and skipped with both files intact."""
    if not seats:
        raise EmptySeatMap("the seat-ID map is empty: attribution signal (b) has nothing to read")
    root = Path(root)
    reg = registry if registry is not None else load_registry()
    files = [(rel, p) for rel, p in live_files(root) if rel != _INDEX_REL]
    attr = _Attr(files, seats, reg)
    moves: list[dict] = []
    skipped: list[dict] = []
    for rel, path in sorted(files):
        if not _SUPERSEDED_RE.search(path.name):
            continue
        kind = classify(path.name, reg)
        folder = rel.split("/", 1)[0] if "/" in rel else "root"
        if kind is None:
            skipped.append({"path": rel, "reason": "unregistered"})
        elif kind.name in ("CLAIM_MARKER", "INDEX"):
            continue                                   # not the janitor's: counted as untouched
        elif folder not in kind.folders:
            skipped.append({"path": rel, "reason": "misfoldered"})
        else:
            lines = _read_window(path)
            if not attr.attributed(path.name, lines):
                skipped.append({"path": rel, "reason": "UNATTRIBUTED"})
                continue
            month, source = _archive_month(lines, path.name)
            dest_rel = (f"archive/{month}/{path.name}" if folder == "root"
                        else f"{folder}/archive/{month}/{path.name}")
            if (root / dest_rel).exists():
                skipped.append({"path": rel, "reason": "COLLISION"})
                continue
            data = path.read_bytes()
            moves.append({"source": rel, "destination": dest_rel, "kind": kind.name,
                          "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                          "month": month, "month_source": source})
    census = _census(root)
    return {"moves": moves, "skipped": skipped,
            "untouched": census["live"] - len(moves) - len(skipped),
            "manifest_sha256": _manifest_hash(moves), "census": census}


_NT = os.name == "nt"


def _posix_noreplace():
    """A `rename(src, dst)` that fails with `FileExistsError` instead of replacing `dst`, for a platform
    whose `os.rename` replaces: `renameat2(RENAME_NOREPLACE)` on Linux, `renamex_np(RENAME_EXCL)` on
    macOS. None when the C library has neither -- the janitor then refuses to apply."""
    import ctypes
    try:
        libc = ctypes.CDLL(None, use_errno=True)
    except (OSError, TypeError):
        return None

    def fail(dst: str) -> None:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), dst)

    if sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
        def renameat2(src: str, dst: str) -> None:
            if libc.renameat2(-100, os.fsencode(src), -100, os.fsencode(dst), 1) != 0:   # AT_FDCWD, NOREPLACE
                fail(dst)
        return renameat2
    if sys.platform == "darwin" and hasattr(libc, "renamex_np"):
        def renamex_np(src: str, dst: str) -> None:
            if libc.renamex_np(os.fsencode(src), os.fsencode(dst), 4) != 0:              # RENAME_EXCL
                fail(dst)
        return renamex_np
    return None


def _rename_no_replace(src: Path, dst: Path) -> None:
    """Move `src` to `dst`, atomically, and fail with `FileExistsError` when `dst` exists. Windows: the
    `os.rename` that raises for an existing name. Elsewhere: a no-replace primitive, else
    `NotImplementedError` -- an `os.rename` that replaces is not a move this module makes."""
    if _NT:
        os.rename(src, dst)
        return
    primitive = _posix_noreplace()
    if primitive is None:
        raise NotImplementedError("this platform has no atomic no-replace rename")
    primitive(os.fspath(src), os.fspath(dst))


def _move_one(src: Path, dst: Path, m: dict) -> None:
    """One reviewed move. It runs under the source's append lock -- the lock `append()` holds while it
    adds to a file -- so no append lands between the hash check and the rename; then it re-checks the
    bytes, checks that the destination is absent and renames with a primitive that never replaces
    (`_rename_no_replace`): a destination that appears after the check is a refusal and not an
    overwrite, on Windows and on Linux/macOS alike; a platform with no such primitive refuses to apply.
    Whole-file `write()` takes the same lock, so no registered writer replaces the source between the
    hash check and the rename. A writer that bypasses this module is not coordinated with. Raises
    `JanitorRefused`, with the source untouched, for every fault before the rename."""
    try:
        with _DestinationLock(src, JANITOR_LOCK_TIMEOUT_S):
            if hashlib.sha256(src.read_bytes()).hexdigest() != m["sha256"]:
                raise JanitorRefused(f"{m['source']} changed after the plan was made; nothing further moved")
            if os.path.lexists(dst):
                raise JanitorRefused(f"{m['destination']} appeared after the plan was made; nothing further moved")
            if not _NT and _posix_noreplace() is None:           # refuse before any directory is made
                raise JanitorRefused(f"{m['source']}: this platform has no atomic no-replace rename; run the "
                                     "apply on the host the transport lives on; nothing moved")
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                _rename_no_replace(src, dst)
            except FileExistsError as exc:
                raise JanitorRefused(f"{m['destination']} appeared after the plan was made (the rename "
                                     "found it); nothing further moved") from exc
            except NotImplementedError as exc:
                raise JanitorRefused(f"{m['source']}: {exc}; run the apply on the host the transport lives "
                                     "on; nothing moved") from exc
            except OSError as exc:
                raise JanitorRefused(f"{m['source']}: the rename failed ({type(exc).__name__}: {exc}); "
                                     "nothing further moved") from exc
    except TransportWriteRefused as exc:       # the lock could not be taken: a writer holds the source
        raise JanitorRefused(f"{m['source']}: could not take its writer lock ({exc}); nothing further "
                             "moved") from exc
    if src.exists() or hashlib.sha256(dst.read_bytes()).hexdigest() != m["sha256"]:
        raise JanitorRefused(f"{m['source']}: the move did not verify (source still present or "
                             "destination bytes differ)")


def janitor_apply(root: Path, expect_manifest: str, *, seats: list[dict],
                  registry: Optional[list[Kind]] = None, trigger_stamp: Optional[str] = None) -> dict:
    """Move exactly the plan the reviewed `expect_manifest` (at least 12 hex) names. Raises
    `JanitorRefused` -- moving nothing -- when the hash is malformed or the fresh plan differs."""
    root = Path(root)
    reg = registry if registry is not None else load_registry()
    expect = (expect_manifest or "").lower()
    if not re.fullmatch(r"[0-9a-f]{12,64}", expect):
        raise JanitorRefused("--expect-manifest needs at least 12 hex characters of the dry run's "
                             "manifest-sha256")
    plan = janitor_plan(root, seats=seats, registry=reg)
    if not plan["manifest_sha256"].startswith(expect):
        raise JanitorRefused(f"the move list changed since it was read: the plan now hashes to "
                             f"{plan['manifest_sha256'][:12]}, not {expect[:12]}; run the dry run again")
    before, shas_before = _census(root), _tree_shas(root)
    moved = 0
    for m in plan["moves"]:
        _move_one(root / m["source"], root / m["destination"], m)
        moved += 1
    after = _census(root)
    if (after["live"] != before["live"] - moved or after["archive"] != before["archive"] + moved
            or _tree_shas(root) != shas_before):
        raise JanitorRefused(f"census after the moves does not conserve the files: before {before}, "
                             f"after {after}, moved {moved}")
    report = {"moved": moved, "skipped": plan["skipped"], "untouched": plan["untouched"],
              "manifest_sha256": plan["manifest_sha256"], "census_before": before,
              "census_after": after, "index": "absent"}
    to_browser = root / "to-browser"
    if any((to_browser / n).is_file() for n in (ARCHIVE_INDEX_NAME, INDEX_NAME)):
        try:
            text = build_index(root, seats=seats, generated_at=trigger_stamp, trigger="janitor",
                               registry=reg)
            _write_both(root, text, slug_to_seat={s["session"]: s["seat"] for s in seats}, registry=reg)
            report["index"] = "regenerated"
        except Exception as exc:  # noqa: BLE001 -- the moves stand; `index --write` repairs the INDEX
            report["index"] = f"NOT regenerated ({type(exc).__name__}: {exc})"
    return report


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
            elif folder_name not in kind.folders:
                findings.append(StrayFinding(
                    rel, f"kind {kind.name} belongs in {' or '.join(kind.folders)}/, found in {folder_name}/"))
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


def _cmd_strays(args: argparse.Namespace) -> int:
    """Done-when 1 (lane-transport-strays, [#1016+]): an EXIT-CODE-GATED check, distinct from
    `report`'s always-0 report-only exit -- "a check keeps the count at zero" (the lane's Value
    line) needs a nonzero signal to gate on, which `report` deliberately never gives.

    The exit code fires on ANY finding (unclassified OR a registered kind sitting in the wrong
    folder) -- both are real, actionable strays. The two counts are broken out separately in the
    JSON because they carry different next steps: `unclassified_count` is the contract's own
    literal wording ("reports 0 unclassified") and should always be drivable to zero by adding a
    registry row; `misfoldered_count` can include a same-name, different-CONTENT collision this
    script must never force-resolve (Do-not: never delete, never move an ambiguous file) -- see
    the lane's session file for the live transport's residual OPERATOR-ACTION cases."""
    root = _resolve_root(args.transport_root)
    if not root.is_dir():
        print(json.dumps({"transport": str(root), "resolved": False,
                          "reason": "not mounted or does not exist"}, sort_keys=True))
        return 1
    findings = scan(root)
    unclassified = [f for f in findings if f.reason == "unregistered kind"]
    misfoldered = [f for f in findings if f not in unclassified]
    print(json.dumps({"transport": str(root), "resolved": True,
                      "stray_count": len(findings),
                      "unclassified_count": len(unclassified),
                      "misfoldered_count": len(misfoldered),
                      "stray": [{"path": f.path, "reason": f.reason} for f in findings]},
                     indent=2, sort_keys=True))
    return 1 if findings else 0


def _seat_ids_path(args: argparse.Namespace) -> Path:
    return Path(args.seat_ids) if getattr(args, "seat_ids", None) else DEFAULT_SEAT_IDS


def _cmd_inventory(args: argparse.Namespace) -> int:
    """Generate the landing inventory; `--write` rewrites only the `landing_inventory:` section of
    the seat-IDs file. The lint and the write gate never call this: the inventory is written once,
    at landing, by this command."""
    root = _resolve_root(args.transport_root)
    if not root.is_dir():
        print(f"transport.py: transport root {root} is not mounted or does not exist", file=sys.stderr)
        return 2
    inv = build_inventory(root)
    path = _seat_ids_path(args)
    if args.write:
        write_seat_ids(path, inventory=inv)
    print(f"inventory: {len(inv)} live file(s) under {root}; "
          f"{'written to' if args.write else 'not written (use --write):'} {path}")
    return 0


def _root_and_seats(args: argparse.Namespace) -> Optional[tuple[Path, list[dict]]]:
    """The transport root and the seat map for a command, or None after saying why on stderr."""
    root = _resolve_root(args.transport_root)
    if not root.is_dir():
        print(f"transport.py: transport root {root} is not mounted or does not exist", file=sys.stderr)
        return None
    try:
        seats, _inv = load_seat_ids(_seat_ids_path(args))
    except SeatIdsError as exc:
        print(f"transport.py: {exc}", file=sys.stderr)
        return None
    if not seats:
        print(f"transport.py: the seat-ID map at {_seat_ids_path(args)} is empty "
              "(run `seat-ids --write`); refusing", file=sys.stderr)
        return None
    return root, seats


def _cmd_index(args: argparse.Namespace) -> int:
    got = _root_and_seats(args)
    if got is None:
        return 2
    root, seats = got
    index_path = root / "to-browser" / INDEX_NAME
    archive_path = root / "to-browser" / ARCHIVE_INDEX_NAME
    slug_to_seat = {s["session"]: s["seat"] for s in seats}
    if args.check:
        if not archive_path.is_file():
            print(f"index: STALE ({archive_path} does not exist; run `index --write`)")
            return 1
        current = archive_path.read_text(encoding="utf-8")
        header = parse_index(current)["header"]
        expected = build_index(root, seats=seats, generated_at=header.get("regenerated"),
                               trigger=header.get("trigger") or "index")
        view_ok = (index_path.is_file()
                   and index_path.read_text(encoding="utf-8") == build_view(current, slug_to_seat=slug_to_seat))
        if expected == current and view_ok:
            print("index: fresh")
            return 0
        print(f"index: STALE ({'archive' if expected != current else 'view'} differs; run `index --write`)")
        return 1
    text = build_index(root, seats=seats, generated_at=args.generated_at, trigger="index")
    if args.write:
        _write_both(root, text, slug_to_seat=slug_to_seat)
        header = parse_index(text)["header"]
        print(f"index: wrote {index_path} and {archive_path} ({header['listed']} listed, "
              f"{header['UNATTRIBUTED']} UNATTRIBUTED, {header['unclassified']} unclassified)")
    else:
        print(build_view(text, slug_to_seat=slug_to_seat), end="")
    return 0


_SINCE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?Z?)?$")


def _since_epoch(value: str) -> float:
    """Epoch seconds of a `--since` value (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM[:SS][Z]`, read as UTC)."""
    text = value.strip()
    dt = _parse_when(text) if _SINCE_RE.match(text) else None
    if dt is None:
        raise ValueError(f"--since {value!r} is not YYYY-MM-DD or YYYY-MM-DDTHH:MM[:SS][Z]")
    return dt.timestamp()


def _is_architect_inbox(path: str, by: str, slug_to_seat: dict[str, str]) -> bool:
    return path.startswith("to-browser/") and not _TA_RE.fullmatch(writer_key(by, slug_to_seat))


def _want_architect(seat: Optional[str]) -> bool:
    return seat is not None and seat.strip().lower() == "architect"


def _since_rows(root: Path, since: float, args: argparse.Namespace,
                slug_to_seat: dict[str, str]) -> list[dict]:
    """Header-only rows of the live classified files whose mtime is >= `since`, oldest first."""
    reg = load_registry()
    want_kind = _norm_kind(args.kind) if args.kind is not None else None
    want_seat = None
    if args.seat is not None and not _want_architect(args.seat):
        want_seat = slug_to_seat.get(args.seat.strip(), args.seat.strip()).lower()
    found: list[tuple[float, str, dict]] = []
    for rel, path in _scan_files(root):
        kind = classify(path.name, reg)
        if kind is None:
            continue
        try:
            mtime = path.stat().st_mtime
            if mtime < since:
                continue
            sha = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        except OSError:
            continue
        keys, heading = _head_keys(_read_window(path))
        if keys.get("summary"):
            summary = _clean(keys["summary"], 100)
        elif heading:
            summary = _clean(heading, 100) or NO_SUBJECT
        else:
            summary = NO_SUBJECT
        m = _DATE_RE.search(keys.get("date", ""))
        named = _DATE_RE.findall(path.name)
        date = m.group() if m else (named[-1] if named else UNDATED)
        by = _clean(keys["by"], 120) if keys.get("by") else UNKNOWN
        if want_kind is not None and _norm_kind(kind.name) != want_kind:
            continue
        if args.date is not None and not date.startswith(args.date.strip()):
            continue
        if _want_architect(args.seat):
            if not _is_architect_inbox(rel, by, slug_to_seat):
                continue
        elif want_seat is not None and writer_key(by, slug_to_seat).lower() != want_seat:
            continue
        found.append((mtime, rel, {"path": rel, "kind": kind.name, "date": date, "by": by or UNKNOWN,
                                   "summary": summary, "sha": sha}))
    found.sort(key=lambda f: (f[0], f[1]))
    return [f[2] for f in found]


def _query_read_repair(root: Path, args: argparse.Namespace) -> None:
    """Refresh a stale default INDEX before it is read. Fails open: one stderr line, the read goes on."""
    try:
        if not index_stale(root):
            return
        seats, _inv = load_seat_ids(_seat_ids_path(args))
        if not seats:
            return
        # Refresh only: with no INDEX at all the read stays a refusal (exit 2, the CLI contract);
        # creating one is `index --write`'s act.
        refresh_index(root / "to-browser" / ARCHIVE_INDEX_NAME, trigger="query", root=root, seats=seats)
    except Exception as exc:  # noqa: BLE001 -- fail open: the INDEX is derived, the read still works
        print(f"query: INDEX refresh skipped ({type(exc).__name__}: {exc})", file=sys.stderr)


def _cmd_query(args: argparse.Namespace) -> int:
    """Rows of the generated INDEX for a kind / date / seat: 0 with matches, 1 with none, 2 when the
    INDEX or the seat map cannot be read. Matches go to stdout (the INDEX row verbatim, or JSON);
    diagnostics go through `logging` to stderr. Without `--index` / `--no-refresh` a stale INDEX is
    refreshed first. `--since` reads the live files instead (headers only, oldest first).
    `--seat architect` is the architect's inbox: `to-browser/` files no `Tech-Architect-NN` wrote."""
    since = None
    if args.since is not None:
        try:
            since = _since_epoch(args.since)
        except ValueError as exc:
            _log.error("query: %s", exc)
            return 2
    if since is not None:
        try:
            root = _resolve_root(args.transport_root)
        except _tr.TransportRefused as exc:
            _log.error("query: %s (pass --transport-root)", exc)
            return 2
        if not root.is_dir():
            _log.error("query: transport root %s is not mounted or does not exist", root)
            return 2
        try:
            seats, _inv = load_seat_ids(_seat_ids_path(args))
        except SeatIdsError as exc:
            _log.error("query: %s", exc)
            return 2
        rows = _since_rows(root, since, args, {s["session"]: s["seat"] for s in seats})
        if args.json:
            sys.stdout.write(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
        else:
            for r in rows:
                sys.stdout.write(f"{r['path']} | kind: {r['kind']} | date: {r['date']} | by: {r['by']} "
                                 f"| summary: {r['summary']} | sha: {r['sha']}\n")
        if not rows:
            _log.warning("query: no live file matches --since %s", args.since)
        return 0 if rows else 1
    try:
        if args.index:
            index_path = Path(args.index)
        else:
            root = _resolve_root(args.transport_root)
            if not args.no_refresh:
                _query_read_repair(root, args)
            archive = root / "to-browser" / ARCHIVE_INDEX_NAME
            index_path = archive if archive.is_file() else root / "to-browser" / INDEX_NAME
    except _tr.TransportRefused as exc:
        _log.error("query: %s (pass --index or --transport-root)", exc)
        return 2
    try:
        text = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        _log.error("query: cannot read the INDEX at %s (%s); run `index --write`", index_path, exc)
        return 2
    try:
        seats, _inv = load_seat_ids(_seat_ids_path(args))
    except SeatIdsError as exc:
        _log.error("query: %s", exc)
        return 2
    slug_to_seat = {s["session"]: s["seat"] for s in seats}
    try:
        if _want_architect(args.seat):
            rows = [r for r in query_index(text, kind=args.kind, date=args.date, status=args.status,
                                           slug_to_seat=slug_to_seat)
                    if _is_architect_inbox(r["path"], r["by"], slug_to_seat)]
        else:
            rows = query_index(text, kind=args.kind, date=args.date, seat=args.seat, status=args.status,
                               slug_to_seat=slug_to_seat)
    except ValueError as exc:
        _log.error("query: %s", exc)
        return 2
    if args.json:
        sys.stdout.write(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    else:
        for r in rows:
            sys.stdout.write(f"- {r['path']} | {r['kind']} | {r['subject']} | {r['date']} | by: {r['by']}\n")
    if not rows:
        _log.warning("query: no INDEX row matches (status=%s)", args.status)
    return 0 if rows else 1


def _cmd_seat_ids(args: argparse.Namespace) -> int:
    root = _resolve_root(args.transport_root)
    if not root.is_dir():
        print(f"transport.py: transport root {root} is not mounted or does not exist", file=sys.stderr)
        return 2
    got = build_seat_map(root)
    for c in got["conflicts"]:
        print(f"seat-ids: conflict (excluded): {c}", file=sys.stderr)
    path = _seat_ids_path(args)
    if args.write:
        if not got["seats"]:
            print("seat-ids: the transport states no complete pair; refusing to write an empty map",
                  file=sys.stderr)
            return 2
        write_seat_ids(path, seats=got["seats"])
        print(f"seat-ids: wrote {len(got['seats'])} pair(s) to {path}")
        return 0
    if args.check:
        try:
            stored, _inv = load_seat_ids(path)
        except SeatIdsError as exc:
            print(f"seat-ids: {exc}")
            return 1
        # The PAIRS decide freshness; provenance and the stating-file count move as the transport grows.
        pairs = {(s["seat"], s["session"]) for s in got["seats"]}
        ok = bool(pairs) and pairs == {(s["seat"], s["session"]) for s in stored}
        print("seat-ids: fresh" if ok else "seat-ids: STALE or empty (run `seat-ids --write`)")
        return 0 if ok else 1
    print(_dump({"seats": got["seats"]}), end="")
    return 0


def _manifest_out_problem(target: Path, root: Path) -> Optional[str]:
    """Why `--manifest-out` may not write `target`, or None. A dry run is read-only toward the
    transport: it never replaces a file that exists (a live or archived transport file included) and
    never creates one anywhere under the transport root, the named one or the environment's."""
    if os.path.lexists(target):
        return f"names {target}, which exists; a plan file is never written over another file"
    homes = [Path(root)]
    known = known_root()
    if known is not None:
        homes.append(known)
    try:
        resolved = os.path.normcase(str(Path(target).resolve()))
        for home in homes:
            base = os.path.normcase(str(Path(home).resolve()))
            if resolved == base or resolved.startswith(base.rstrip("\\/") + os.sep):
                return f"names {target}, inside the transport {home}; the plan file goes elsewhere"
    except OSError as exc:
        return f"could not be resolved ({type(exc).__name__}: {exc})"
    return None


def _cmd_janitor(args: argparse.Namespace) -> int:
    got = _root_and_seats(args)
    if got is None:
        return 2
    root, seats = got
    if args.manifest_out:
        problem = _manifest_out_problem(Path(args.manifest_out), root)
        if problem:
            print(f"janitor: refused: --manifest-out {problem}", file=sys.stderr)
            return 2
    if args.apply:
        if not args.expect_manifest:
            print("janitor: --apply needs --expect-manifest <the dry run's manifest-sha256, at least "
                  "12 hex>; run the dry run first", file=sys.stderr)
            return 2
        try:
            report = janitor_apply(root, args.expect_manifest, seats=seats)
        except JanitorRefused as exc:
            print(f"janitor: refused: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    plan = janitor_plan(root, seats=seats)
    reasons: dict[str, int] = {}
    for s in plan["skipped"]:
        reasons[s["reason"]] = reasons.get(s["reason"], 0) + 1
    print(f"janitor: DRY RUN under {root} (nothing was moved)")
    print(f"manifest-sha256: {plan['manifest_sha256']}")
    print(f"live: {plan['census']['live']}  archive: {plan['census']['archive']}  "
          f"moves: {len(plan['moves'])}  skipped: {len(plan['skipped'])}  untouched: {plan['untouched']}")
    print("skipped by reason: " + (", ".join(f"{k}={n}" for k, n in sorted(reasons.items())) or "-"))
    kinds: dict[str, int] = {}
    for m in plan["moves"]:
        kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
    print("moves by kind: " + (", ".join(f"{k}={n}" for k, n in sorted(kinds.items())) or "-"))
    for m in plan["moves"]:
        print(f"{m['source']} | {m['destination']} | {m['sha256']}")
    for s in plan["skipped"]:
        print(f"skipped: {s['path']} ({s['reason']})")
    if args.manifest_out:
        try:
            with open(args.manifest_out, "x", encoding="utf-8", newline="\n") as fh:   # "x": never replace
                fh.write(json.dumps(plan, indent=2, sort_keys=True) + "\n")
        except OSError as exc:
            print(f"janitor: refused: --manifest-out could not be created ({type(exc).__name__}: {exc})",
                  file=sys.stderr)
            return 2
    return 0


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
    s = sub.add_parser("strays", help="exit-code-gated: nonzero if any stray finding exists")
    s.add_argument("--transport-root", default=None)
    s.set_defaults(func=_cmd_strays)
    d = sub.add_parser("derive", help="derive kind prefixes from the code; diff against the registry")
    d.set_defaults(func=_cmd_derive)
    i = sub.add_parser("inventory", help="generate the landing inventory (the by: rule's pre-existing set)")
    i.add_argument("--transport-root", default=None)
    i.add_argument("--seat-ids", default=None, help="the generated seat-IDs file (default: ecosystem/seat-ids.yaml)")
    i.add_argument("--write", action="store_true", help="rewrite the landing_inventory section")
    i.set_defaults(func=_cmd_inventory)
    x = sub.add_parser("index", help="build the generated to-browser/INDEX.md (prints it; --write writes it)")
    x.add_argument("--transport-root", default=None)
    x.add_argument("--seat-ids", default=None, help="the generated seat-IDs file (default: ecosystem/seat-ids.yaml)")
    xm = x.add_mutually_exclusive_group()
    xm.add_argument("--write", action="store_true", help="write to-browser/INDEX.md")
    xm.add_argument("--check", action="store_true", help="exit 1 when INDEX.md is missing or stale")
    x.add_argument("--generated-at", default=None, help="the regenerated: stamp (default: now, UTC)")
    x.set_defaults(func=_cmd_index)
    si = sub.add_parser("seat-ids", help="the Tech-Architect <-> session pairs the transport states")
    si.add_argument("--transport-root", default=None)
    si.add_argument("--seat-ids", default=None, help="the generated seat-IDs file (default: ecosystem/seat-ids.yaml)")
    sm = si.add_mutually_exclusive_group()
    sm.add_argument("--write", action="store_true", help="rewrite the seats section")
    sm.add_argument("--check", action="store_true", help="exit 1 when the file's seats are stale or empty")
    si.set_defaults(func=_cmd_seat_ids)
    q = sub.add_parser("query", help="rows of the generated INDEX for a kind, a date and a seat; refreshes a "
                                     "stale INDEX first (--no-refresh keeps it a pure read); --since lists the "
                                     "live files' headers; exit 1 when nothing matches")
    q.add_argument("--transport-root", default=None)
    q.add_argument("--seat-ids", default=None, help="the generated seat-IDs file (default: ecosystem/seat-ids.yaml)")
    q.add_argument("--index", default=None, help="the INDEX file to read, purely (default: the transport's "
                                                 "to-browser/INDEX-ARCHIVE.md, else INDEX.md)")
    q.add_argument("--since", default=None, help="headers only of live files modified at or after "
                                                 "YYYY-MM-DD or YYYY-MM-DDTHH:MM[:SS][Z] (UTC), oldest first")
    q.add_argument("--no-refresh", action="store_true", help="do not refresh a stale INDEX before reading it")
    q.add_argument("--kind", default=None, help="a registered kind, e.g. LANE_END (case and -/_ ignored)")
    q.add_argument("--date", default=None, help="YYYY-MM-DD, or a prefix such as YYYY-MM")
    q.add_argument("--seat", default=None, help="Tech-Architect-NN, a session slug of the seat map, UNKNOWN, or "
                                                "`architect` (the architect's inbox: to-browser/ files no "
                                                "architect wrote)")
    q.add_argument("--status", default="current", choices=QUERY_STATUSES, help="which INDEX section (default: current)")
    q.add_argument("--json", action="store_true", help="print the matches as a JSON list")
    q.set_defaults(func=_cmd_query)
    j = sub.add_parser("janitor", help="move -superseded files of attributable kinds into archive/ "
                                       "(dry run by default; --apply needs the reviewed manifest hash)")
    j.add_argument("--transport-root", default=None)
    j.add_argument("--seat-ids", default=None, help="the generated seat-IDs file (default: ecosystem/seat-ids.yaml)")
    j.add_argument("--apply", action="store_true", help="move the files (needs --expect-manifest)")
    j.add_argument("--expect-manifest", default=None, help="manifest-sha256 of the reviewed dry run (>= 12 hex)")
    j.add_argument("--manifest-out", default=None, help="write the full plan as JSON to this file")
    j.set_defaults(func=_cmd_janitor)
    return p


def _utf8_stdio() -> None:
    """File names and heads are UTF-8; a redirected Windows console is cp1252 and a `print` of one
    stray character (a star in a subject) would raise. Reconfigure the streams, never fail on it."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main(argv: Optional[list[str]] = None) -> int:
    _utf8_stdio()
    args = _parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
