#!/usr/bin/env python
"""graph_store.py -- FPG-1 PERSISTED, so an organ can query it instead of rebuilding it ([#664]).

WHAT THIS IS. The persistence half of the delivery spine. `file_purpose_graph.py` builds the
one repo graph; this writes it to a stdlib SQLite file and hands back a read-only query
surface. Everything downstream -- the three commit-tier refusals -- reads the STORE, never a
live build. That is `[#664]`'s explicit bar (*"print node and edge counts read back from the
persisted artifact, never from an in-memory build"*) and it is also the only reason three
refusals can ride one commit: a full build measures ~13 s on this tree (17.5 s wall for
the rebuild hook), and three of them would put a minute on every commit. A store read
measures milliseconds -- the whole read path is one sqlite open and a handful of SELECTs.

WHY SQLITE AND NOT A LIBRARY. The row says it: *"sqlite -- stdlib, no new dependency"*. It is
also the answer standing ruling R-A already measured for exactly this workload --
`docs/audits/2026-08-21-technical-library-first-research.md`, quoted in intake #40 §4: *"at
11,684 edges, stdlib sqlite3 answers reachability, orphan and degree in 1-4 ms."* The graph is
BUILT with rustworkx (R-A's named-consumer discharge, unchanged); it is QUERIED from sqlite.
Those are different questions and the repo has a measured answer to each.

WHERE THE STORE LIVES, AND WHY IT IS NOT UNDER `logs/`. Under the RESOLVED git dir --
`git rev-parse --absolute-git-dir` -- which is outside the working tree by construction. Three
things follow, and the third is the one that decided it:

  1. It can never dirty `git status`, so it cannot trip session-end backpressure. The
     `logs/TELEMETRY.db*` entry in `.gitignore` exists to buy exactly this, and its comment
     records the WAL sidecars that made a bare name insufficient.
  2. In a worktree the git dir resolves PER WORKTREE, which is the right granularity: a
     worktree is a different tree and therefore a different graph. A shared store would have
     one lane's orphan census answering from another lane's files.
  3. It needs no `.gitignore` line -- and `.gitignore` is not in `[#664]`'s declared
     footprint. A store that requires an edit the lane may not make is the wrong store.

WAL, AND THE THREE PRAGMAS ARE NOT DECORATION. Pre-commit hooks and parallel lanes read this
concurrently; `telemetry_emit.WAL_PRAGMAS` records the reason in the memo's own words --
*"readers do not block writers and a writer does not block readers."* The same three pragmas
are used here rather than re-chosen.

LAYER-2 POSTURE (ADR-28/36, core invariant #4). This module WRITES, and the barred class is
orchestration that drives state in a CHILD repo. One local file under this repo's own git dir
is the established in-repo pattern -- `logs/FLEET-HEALTH.md`, `logs/ENFORCEMENT-COVERAGE.md`,
`logs/TELEMETRY.db` -- and this joins it. Nothing here touches a sibling repo.

STALENESS IS A MEASUREMENT, NOT A PROMISE. `ensure()` rebuilds when the store is older than
the newest source file it was built from, and `is_stale()` says so without rebuilding. The
commit-time hook calls `rebuild()` unconditionally, so the store is rebuilt on every commit as
the row requires; `ensure()` exists so a query run outside that path self-heals rather than
refusing on a store nobody built yet.

Usage:
    python scripts/graph_store.py rebuild [--repo-root .] [--db PATH]
    python scripts/graph_store.py stats   [--repo-root .] [--db PATH]
"""

from __future__ import annotations

import argparse
import contextlib
import logging
import os
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("graph-store")

#: Bumped whenever the table shape changes. A store stamped with a different version is not
#: readable by this code, and `open_store` says so rather than answering from a shape it does
#: not understand -- the `silent_rule_ratchet` discipline, applied to a schema.
SCHEMA_VERSION = 1

#: Where the store sits under the resolved git dir. One directory so the WAL sidecars
#: (`-wal`, `-shm`) stay together and a cleanup is one `rmtree`.
STORE_RELPATH = "fpg-graph/FPG.db"

#: Verbatim from `telemetry_emit.WAL_PRAGMAS` -- the memo's three, not three of our own.
WAL_PRAGMAS = (
    "PRAGMA journal_mode=WAL",
    "PRAGMA synchronous=NORMAL",
    "PRAGMA busy_timeout=5000",
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS nodes (
    key   TEXT PRIMARY KEY,
    kind  TEXT NOT NULL,
    label TEXT NOT NULL,
    path  TEXT,
    process_class TEXT
);
CREATE TABLE IF NOT EXISTS edges (
    src    TEXT NOT NULL,
    dst    TEXT NOT NULL,
    kind   TEXT NOT NULL,
    source TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS roots (key TEXT PRIMARY KEY);
CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges (dst, kind);
CREATE INDEX IF NOT EXISTS idx_edges_src ON edges (src, kind);
CREATE INDEX IF NOT EXISTS idx_nodes_path ON nodes (path);
CREATE INDEX IF NOT EXISTS idx_nodes_process ON nodes (process_class);
"""


@dataclass(frozen=True)
class Counts:
    """What the store holds, read back OUT of it. Clause 1's evidence, in one object."""
    nodes: int
    edges: int
    kinds: int

    def as_dict(self) -> dict[str, int]:
        return {"nodes": self.nodes, "edges": self.edges, "kinds": self.kinds}

    def render(self) -> str:
        # Flat key/value, no column padding -- CLAUDE.md output-formatting: a table here
        # renders as border glyphs in the TUI and triples in a pasted transcript.
        return (f"nodes    : {self.nodes}\n"
                f"edges    : {self.edges}\n"
                f"kinds    : {self.kinds}")


class StoreUnreadable(RuntimeError):
    """The store is absent, or was written by a schema this code does not understand.

    A REFUSAL RATHER THAN A REBUILD, at the read boundary. A reader that silently rebuilt on
    a version mismatch would answer from a graph the caller never asked for and hide the
    mismatch; `ensure()` is where rebuilding is a decision, and it is explicit there.
    """


# ----------------------------------------------------------------------------- where it lives


def _resolved_git_dir(repo_root: Path) -> Path | None:
    """`git rev-parse --absolute-git-dir`, or None outside a repository.

    NOT `repo_root / ".git"`. In a worktree `.git` is a FILE pointing at
    `<main>/.git/worktrees/<name>`, so the naive spelling either fails or -- worse -- lands
    every worktree's store in one shared path, and one lane's census would then answer from
    another lane's tree.
    """
    try:
        out = subprocess.run(["git", "rev-parse", "--absolute-git-dir"],
                             cwd=repo_root, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
        return None
    return Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else None


def store_path(repo_root: Path | str) -> Path:
    """The store's path for this tree. Falls back to `<repo>/.git/` outside a repository,
    which is where a fixture tree lands -- still outside anything a walker reads."""
    root = Path(repo_root).resolve()
    git_dir = _resolved_git_dir(root) or (root / ".git")
    return git_dir / STORE_RELPATH


# ------------------------------------------------------------------------------------- write


def _connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    for pragma in WAL_PRAGMAS:
        connection.execute(pragma)
    return connection


def rebuild(repo_root: Path | str, db_path: Path | str | None = None) -> Counts:
    """Build FPG-1 once and write it to the store. Returns the counts AS WRITTEN.

    The rustworkx import is deferred into this function on purpose: the read path -- three
    commit-tier hooks -- must not pay for a graph library it never uses. `graph_queries.py`
    imports this module and never reaches `rebuild`, so its cold start stays stdlib-only.
    """
    import file_purpose_graph as fpg   # noqa: PLC0415 -- see docstring; read path stays stdlib

    root = Path(repo_root).resolve()
    path = Path(db_path) if db_path else store_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)

    graph = fpg.build(root)
    nodes = [graph.graph[index] for index in graph.graph.node_indices()]
    edges = graph.all_edges()

    # ONE TEMP FILE PER PROCESS. A shared `.rebuilding` name is a race, and it is not a
    # theoretical one: five xdist workers each calling `ensure()` on a cold store collided
    # on Windows with `WinError 32 -- the process cannot access the file because it is being
    # used by another process`. Concurrency is this store's normal condition (parallel lane
    # worktrees, a commit hook, a test session), so the writer is made concurrent-safe
    # rather than the callers made careful.
    tmp = path.with_suffix(f".rebuilding-{os.getpid()}")
    for stale in (tmp, tmp.with_name(tmp.name + "-wal"), tmp.with_name(tmp.name + "-shm")):
        stale.unlink(missing_ok=True)
    connection = _connect(tmp)
    try:
        connection.executescript(_SCHEMA)
        connection.executemany(
            "INSERT OR REPLACE INTO nodes (key, kind, label, path, process_class) "
            "VALUES (?, ?, ?, ?, ?)",
            [(n.key, n.kind, n.label, n.path,
              fpg.process_class(n.path) if n.path else None) for n in nodes])
        connection.executemany(
            "INSERT INTO edges (src, dst, kind, source, detail) VALUES (?, ?, ?, ?, ?)",
            [(e.src, e.dst, e.kind, e.source, e.detail) for e in edges])
        connection.executemany(
            "INSERT OR REPLACE INTO roots (key) VALUES (?)",
            [(key,) for key in sorted(_wiring_root_keys(fpg, root))])
        connection.executemany(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            [("schema_version", str(SCHEMA_VERSION)), ("repo_root", root.as_posix())])
        connection.commit()
    finally:
        connection.close()

    # ATOMIC SWAP rather than a write in place. A hook that dies mid-rebuild would otherwise
    # leave a half-written store that reads as a repo with no edges -- and an orphan census
    # over an empty graph reports EVERY process as an orphan. The failure mode of a truncated
    # store is not a smaller answer, it is a maximally wrong one.
    _swap_into_place(tmp, path)
    return open_store(path).counts()


#: How long a swap keeps retrying before giving up. On Windows `os.replace` FAILS if the
#: destination is open, and a concurrent reader holding the store for a millisecond is
#: normal here rather than exceptional -- so the swap retries instead of the reader being
#: asked not to read. Short, bounded, and it gives up loudly rather than looping.
_SWAP_ATTEMPTS = 20
_SWAP_BACKOFF_S = 0.1
#: How long a rebuild lock is honoured before it is treated as held by a dead builder.
#: Generous against the ~17 s live build, bounded so a crash costs one wait and never a wedge.
_LOCK_TTL_S = 120.0


def _swap_into_place(tmp: Path, path: Path) -> None:
    """Atomic-swap the freshly written store over the live one.

    ATOMIC SWAP RATHER THAN A WRITE IN PLACE. A hook that dies mid-rebuild would otherwise
    leave a half-written store that reads as a repo with no edges -- and an orphan census
    over an empty graph reports EVERY process as an orphan. The failure mode of a truncated
    store is not a smaller answer, it is a maximally wrong one.
    """
    for suffix in ("-wal", "-shm"):
        Path(str(path) + suffix).unlink(missing_ok=True)
    last: OSError | None = None
    for attempt in range(_SWAP_ATTEMPTS):
        try:
            os.replace(tmp, path)
            return
        except OSError as exc:   # a reader holds the destination; it will let go
            last = exc
            time.sleep(_SWAP_BACKOFF_S * (attempt + 1) / 4)
    tmp.unlink(missing_ok=True)
    raise StoreUnreadable(
        f"{path}: could not swap in the rebuilt store after {_SWAP_ATTEMPTS} attempts "
        f"({last}). A reader is holding it open; retry, or close the reader.")


def _wiring_root_keys(fpg, root: Path) -> set[str]:
    """The wiring surfaces this store was built from, as node keys.

    STORED, NOT RE-DERIVED BY THE READER. A query that recomputed the root set would hold a
    second opinion about what a trigger is -- thirteen answers becoming fourteen, which is
    the exact shape ADR-118 exists to end. The store is self-describing instead.
    """
    keys = {fpg._file_key(rel) for rel in fpg.WIRING_SURFACES
            if (root / rel).is_file()}
    keys |= {fpg._file_key(path.relative_to(root).as_posix())
             for path in root.glob(fpg.WIRING_WORKFLOW_GLOB)}
    return keys


# -------------------------------------------------------------------------------------- read


@dataclass(frozen=True)
class StoredNode:
    key: str
    kind: str
    label: str
    path: str | None
    process_class: str | None


class GraphStore:
    """A read-only query surface over the persisted graph. Opens the file; builds nothing."""

    def __init__(self, db_path: Path):
        self.path = db_path
        if not db_path.exists():
            raise StoreUnreadable(
                f"{db_path}: no persisted graph. Build it with "
                f"`uv run --locked python scripts/graph_store.py rebuild`.")
        self._connection = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
        self._connection.row_factory = sqlite3.Row
        try:
            row = self._connection.execute(
                "SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
        except sqlite3.DatabaseError as exc:
            raise StoreUnreadable(f"{db_path}: not a readable graph store ({exc}).") from exc
        if row is None or int(row["value"]) != SCHEMA_VERSION:
            raise StoreUnreadable(
                f"{db_path}: schema version {row['value'] if row else 'absent'} != "
                f"{SCHEMA_VERSION}. Rebuild rather than read a shape this code does not know.")

    def close(self) -> None:
        self._connection.close()

    def counts(self) -> Counts:
        nodes = self._connection.execute("SELECT COUNT(*) AS n FROM nodes").fetchone()["n"]
        edges = self._connection.execute("SELECT COUNT(*) AS n FROM edges").fetchone()["n"]
        kinds = self._connection.execute(
            "SELECT COUNT(DISTINCT kind) AS n FROM edges").fetchone()["n"]
        return Counts(nodes=nodes, edges=edges, kinds=kinds)

    def edges_by_kind(self) -> dict[str, int]:
        return {row["kind"]: row["n"] for row in self._connection.execute(
            "SELECT kind, COUNT(*) AS n FROM edges GROUP BY kind ORDER BY n DESC")}

    def edges_by_source(self) -> dict[str, int]:
        return {row["source"]: row["n"] for row in self._connection.execute(
            "SELECT source, COUNT(*) AS n FROM edges GROUP BY source ORDER BY n DESC")}

    def roots(self) -> set[str]:
        return {row["key"] for row in self._connection.execute("SELECT key FROM roots")}

    def processes(self) -> list[StoredNode]:
        """Every node the graph classes as a process, ordered by path."""
        return [StoredNode(row["key"], row["kind"], row["label"], row["path"],
                           row["process_class"])
                for row in self._connection.execute(
                    "SELECT * FROM nodes WHERE process_class IS NOT NULL ORDER BY path")]

    def key_for_path(self, relpath: str) -> str | None:
        row = self._connection.execute(
            "SELECT key FROM nodes WHERE path = ? ORDER BY key LIMIT 1", (relpath,)).fetchone()
        return row["key"] if row else None

    def in_edges(self, key: str, kinds: tuple[str, ...] | None = None):
        sql = "SELECT src, dst, kind, source, detail FROM edges WHERE dst = ?"
        params: list[str] = [key]
        if kinds:
            sql += f" AND kind IN ({','.join('?' * len(kinds))})"
            params.extend(kinds)
        return [dict(row) for row in self._connection.execute(sql, params)]

    def node(self, key: str) -> StoredNode | None:
        row = self._connection.execute("SELECT * FROM nodes WHERE key = ?", (key,)).fetchone()
        return None if row is None else StoredNode(
            row["key"], row["kind"], row["label"], row["path"], row["process_class"])

    def reachable(self, roots: set[str], kinds: tuple[str, ...]) -> set[str]:
        """Every node reachable from `roots` over `kinds` -- the triggered set.

        A BREADTH-FIRST WALK IN SQL, not a transitive-closure table. R-A's measurement is
        what licenses the simple shape: reachability over ~14k edges answers in single-digit
        milliseconds from stdlib sqlite, so the frontier query per level costs nothing worth
        a schema. Cycles terminate because a node enters `seen` before it is expanded.
        """
        seen: set[str] = set()
        frontier = {key for key in roots if key}
        placeholders = ",".join("?" * len(kinds))
        while frontier:
            batch = list(frontier)
            frontier = set()
            for start in range(0, len(batch), 400):   # SQLITE_MAX_VARIABLE_NUMBER headroom
                chunk = batch[start:start + 400]
                sql = (f"SELECT DISTINCT dst FROM edges WHERE kind IN ({placeholders}) "
                       f"AND src IN ({','.join('?' * len(chunk))})")
                for row in self._connection.execute(sql, list(kinds) + chunk):
                    if row["dst"] not in seen:
                        seen.add(row["dst"])
                        frontier.add(row["dst"])
        return seen

    def trigger_of(self, key: str) -> str:
        """The nearest reason this node runs -- a wiring surface, or the module that imports
        it. Reported so a `process_list` row says WHY, not merely that."""
        rows = self.in_edges(key, ("triggers",))
        if rows:
            node = self.node(rows[0]["src"])
            return node.path or rows[0]["src"] if node else rows[0]["src"]
        rows = self.in_edges(key, ("imports",))
        if rows:
            node = self.node(rows[0]["src"])
            return node.path or rows[0]["src"] if node else rows[0]["src"]
        return ""


def open_store(db_path: Path | str) -> GraphStore:
    return GraphStore(Path(db_path))


# ------------------------------------------------------------------------------- staleness


def _newest_source_mtime(repo_root: Path) -> float:
    """The newest mtime across the trees the graph is built from.

    DELIBERATELY COARSE. This is a self-healing convenience for a query run outside the
    commit hook, not the freshness contract -- the contract is the hook, which rebuilds
    unconditionally. A coarse mtime scan can only ever rebuild too often, never too rarely,
    which is the safe direction for a gate.
    """
    newest = 0.0
    for base in ("scripts", "tasks", "docs", "plugins", ".claude/commands", ".claude/skills",
                 "ecosystem", "deploy", "tests"):
        directory = repo_root / base
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            parts = set(path.relative_to(repo_root).parts)
            if "__pycache__" in parts or "worktrees" in parts:
                continue
            try:
                if path.is_file():
                    newest = max(newest, path.stat().st_mtime)
            except OSError:
                continue
    for name in ("ARCHITECTURE.md", ".pre-commit-config.yaml", ".pre-commit-hooks.yaml"):
        candidate = repo_root / name
        if candidate.is_file():
            newest = max(newest, candidate.stat().st_mtime)
    return newest


def is_stale(repo_root: Path | str, db_path: Path | str | None = None) -> bool:
    root = Path(repo_root).resolve()
    path = Path(db_path) if db_path else store_path(root)
    if not path.exists():
        return True
    return path.stat().st_mtime < _newest_source_mtime(root)


def ensure(repo_root: Path | str, db_path: Path | str | None = None) -> GraphStore:
    """Open the store, rebuilding first if it is absent or stale.

    ONE REBUILDER AT A TIME, and the lock is the cheap kind: an exclusive `open(..., "x")`
    on a sidecar. Whoever wins builds; everyone else WAITS for the result rather than
    building a second copy of the same graph. Without it, a parallel test session paid five
    concurrent ~17 s builds and then raced on the swap -- the measured failure that produced
    this function's current shape. A stale lock (a killed builder) is honoured for
    `_LOCK_TTL_S` and then broken, so a crash costs one wait and never a wedge.
    """
    root = Path(repo_root).resolve()
    path = Path(db_path) if db_path else store_path(root)
    if not is_stale(root, path):
        with contextlib.suppress(StoreUnreadable):
            return open_store(path)

    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".rebuild-lock")
    try:
        with contextlib.suppress(OSError):
            if lock.exists() and time.time() - lock.stat().st_mtime > _LOCK_TTL_S:
                lock.unlink(missing_ok=True)   # a builder died holding it
        with open(lock, "x"):
            pass
    except FileExistsError:
        deadline = time.time() + _LOCK_TTL_S
        while time.time() < deadline and lock.exists():
            time.sleep(_SWAP_BACKOFF_S)
        with contextlib.suppress(StoreUnreadable):
            return open_store(path)

    try:
        rebuild(root, path)
    finally:
        lock.unlink(missing_ok=True)
    return open_store(path)


# ------------------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Persist FPG-1 to a queryable SQLite store, and read it back.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=".", help="repo to read (default: cwd)")
    common.add_argument("--db", default=None, help="store path (default: under the git dir)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("rebuild", parents=[common], help="rebuild the store from source")
    sub.add_parser("stats", parents=[common], help="counts read back FROM the store")

    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve()
    path = Path(args.db) if args.db else store_path(root)

    if args.command == "rebuild":
        counts = rebuild(root, path)
        print(f"store    : {path}")
        print(counts.render())
        for kind, count in open_store(path).edges_by_kind().items():
            print(f"  {kind:<16} {count}")
        return 0

    try:
        store = open_store(path)
    except StoreUnreadable as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"store    : {path}")
    print(store.counts().render())
    for source, count in store.edges_by_source().items():
        print(f"  {source:<22} {count}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
