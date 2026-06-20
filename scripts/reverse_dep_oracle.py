#!/usr/bin/env python
"""reverse_dep_oracle.py — #193 code->code reverse-dependency oracle (ADR-89, Track A).

Given a Python symbol, return its reverse-dependents (callers / referencers) by driving a
headless Pyright language server over LSP `textDocument/references`, with a MANDATORY
provenance block on every answer. This implements ADR-89's computed-edge doctrine (code
edges are *computed* from source, never declared via `reconciled_with`) and settles its
open provenance/truncation question (OQ2): the provenance shape below is the resolution.

The LSP client (`uri`, `class LSP`, the initialize handshake) is lifted VERBATIM from the
sanctioned 2026-06-20 benchmark harness (`docs/audits/2026-06-20-pyright-reverse-dep-
oracle-findings.md`, the `bench.py` <details> block) — proven crash/hang-free on this
repo. Symbol resolution adapts that audit's `gen_targets.py` AST walk.

Scope & honest limits (ADR-89's three limits — emitted as caveats on EVERY answer):
  * static-Python-only — sees only statically-resolvable Python. Dynamic dispatch,
    getattr/setattr, string-keyed registries, reflection, monkeypatching, and ALL
    cross-language edges (markdown->script, settings.json / .pre-commit hook-wiring,
    plugin manifests) are INVISIBLE. Never presented as catching them.
  * repo-scoped — definitions resolved within scripts/ of THIS repo; numbers do not
    extrapolate to child repos.
  * references()-only — call-hierarchy (with its ~8 s warm-up) is not used.

What this is NOT (intent-spec anti-patterns): it is the oracle TOOL only. It is not wired
into `audit.py` ALL_CHECKS, not a pre-commit hook, not a gate. The safe-removal gate that
CONSUMES it is #195 (Track D), a separate later item. Because a gate will consume this, the
"never crash" contract is load-bearing: every startup-failure mode (missing langserver,
missing node, a langserver that dies/errors on start) maps to the SAME `oracle-unavailable`
envelope (exit non-zero, install hint) — never a stack-trace a consuming gate could inherit
and fail-open on.

Layer-2 / read-only (ADR-28/36): spawns Pyright (read-only analysis subprocess), reads
source + git metadata, opens documents in the LSP. Writes NO repo files.

Line convention: output `line` fields are 1-based (editor / `file:line` clickable); the
internal `Definition` carries the 0-based LSP `line`/`character` the protocol needs.

Usage:  python scripts/reverse_dep_oracle.py <symbol> [--file scripts/audit.py]
                 [--json | --text] [--langserver PATH] [--timeout 20] [--repo-root .]
Bootstrap (one-time, vendors Pyright):  npm install        (in the repo root)
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

SCHEMA = "reverse-dep-oracle/v1"

REQ_TIMEOUT = 30.0          # per-request LSP timeout (lifted from bench.py)
POLL_INTERVAL = 0.25        # canary readiness poll cadence (250 ms, per the benchmark)
DEFAULT_WARM_TIMEOUT = 20.0  # completeness deadline (benchmark cold-start was 3.6-4.3 s)

# The three ADR-89 limits, stated on EVERY answer (mandatory; hardcoded, never optional).
STATIC_PYTHON_CAVEAT = (
    "static-python-only: dynamic dispatch, getattr/setattr, string-keyed registries, "
    "reflection, monkeypatching, and ALL cross-language edges (markdown->script, "
    "settings.json / .pre-commit-config.yaml hook-wiring, plugin manifests) are INVISIBLE "
    "to this oracle."
)
REPO_SCOPED_CAVEAT = (
    "repo-scoped: definitions resolved within scripts/ of THIS repo only; referencers "
    "reported workspace-wide within this repo; numbers do not extrapolate to child repos."
)
WORKING_TREE_CAVEAT = (
    "working-tree: Pyright analyses files as they exist in the working tree (read via "
    "didOpen), so this answer reflects the working tree, NOT committed state at git_rev. "
    "When dirty=true the two differ."
)
CAVEATS = [STATIC_PYTHON_CAVEAT, REPO_SCOPED_CAVEAT, WORKING_TREE_CAVEAT]

_INSTALL_HINT = "pyright langserver not found — run `npm install` in the repo root"


class OracleUnavailable(Exception):
    """Any startup/runtime failure that must surface as `oracle-unavailable`, not a crash."""


# --- symbol resolution (pure AST; adapted from the benchmark's gen_targets.py) ---------

@dataclass(frozen=True)
class Definition:
    """A def/class site. `line`/`character` are 0-based LSP coordinates (query-native)."""

    file: str       # repo-relative, forward slashes (e.g. "scripts/audit.py")
    name: str
    kind: str       # "FunctionDef" | "AsyncFunctionDef" | "ClassDef"
    line: int       # 0-based (LSP)
    character: int  # 0-based (LSP), pointing at the NAME identifier, not the keyword


def iter_definitions(repo_root: Path) -> list[Definition]:
    """Every FunctionDef/AsyncFunctionDef/ClassDef in scripts/, name-identifier position.

    Position points at the symbol NAME (`phys.find(node.name, col)`), not the def/class
    keyword — pointing at the keyword yields no references from Pyright.
    """
    scripts_dir = repo_root / "scripts"
    out: list[Definition] = []
    if not scripts_dir.is_dir():
        return out
    for path in sorted(scripts_dir.rglob("*.py")):
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src, filename=str(path))
        except (SyntaxError, OSError):
            continue
        lines = src.splitlines()
        rel = str(path.relative_to(repo_root)).replace("\\", "/")
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                line0 = node.lineno - 1
                col = node.col_offset
                phys = lines[line0] if line0 < len(lines) else ""
                idx = phys.find(node.name, col)
                if idx < 0:
                    idx = phys.find(node.name)
                if idx < 0:
                    continue
                out.append(Definition(rel, node.name, type(node).__name__, line0, idx))
    return out


def _file_matches(def_file: str, want: str) -> bool:
    want = want.replace("\\", "/")
    return (
        def_file == want
        or def_file.endswith("/" + want)
        or Path(def_file).name == Path(want).name
    )


def resolve_symbol(name: str, repo_root: Path, file: str | None = None) -> list[Definition]:
    """Definitions named `name` in scripts/, optionally narrowed by `file` (basename or
    path-suffix). 0 -> not found; >1 without `file` -> ambiguous; exactly 1 -> resolved."""
    defs = [d for d in iter_definitions(repo_root) if d.name == name]
    if file:
        defs = [d for d in defs if _file_matches(d.file, file)]
    return defs


# --- git provenance (reuses the session_end_backpressure._git pattern) -----------------

def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
    )


def git_provenance(repo_root: Path) -> dict:
    """{git_rev (HEAD), dirty, dirty_files}. Fail-soft: git absent -> rev None, no dirty."""
    git_rev = None
    try:
        rev = _git(repo_root, "rev-parse", "HEAD")
        if rev.returncode == 0:
            git_rev = rev.stdout.strip()
        st = _git(repo_root, "status", "--porcelain")
        dirty_files = [
            line[3:].strip() for line in st.stdout.splitlines() if line.strip()
        ] if st.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        dirty_files = []
    return {"git_rev": git_rev, "dirty": bool(dirty_files), "dirty_files": sorted(dirty_files)}


# --- LSP client (lifted VERBATIM from bench.py; argv parametrized, spawn fail -> raise) -

def uri(path: Path) -> str:
    """Windows file:// URI (matches the benchmark host; e.g. file:///C%3A/Users/...)."""
    s = str(path).replace("\\", "/")
    drive, rest = s[0], s[1:]
    return "file:///" + quote(drive) + "%3A" + quote(rest[1:], safe="/")


class LSP:
    def __init__(self, argv: list[str]) -> None:
        try:
            self.proc = subprocess.Popen(
                argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, bufsize=0,
            )
        except OSError as exc:  # node missing / argv unspawnable -> oracle-unavailable
            raise OracleUnavailable(f"could not spawn language server ({argv[0]}): {exc}") from exc
        self._id = 0
        self._lock = threading.Lock()
        self._responses: dict[int, dict] = {}
        self._events: dict[int, threading.Event] = {}
        self.crashed = False
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _send(self, obj: dict) -> None:
        data = json.dumps(obj).encode("utf-8")
        try:
            self.proc.stdin.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii") + data)
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            self._fail()

    def _fail(self) -> None:
        """Mark crashed and wake every pending waiter (snappy startup-death detection)."""
        self.crashed = True
        with self._lock:
            for ev in self._events.values():
                ev.set()

    def _read_loop(self) -> None:
        f = self.proc.stdout
        while True:
            headers = b""
            while b"\r\n\r\n" not in headers:
                ch = f.read(1)
                if not ch:
                    self._fail()
                    return
                headers += ch
            length = 0
            for line in headers.decode("ascii", "replace").split("\r\n"):
                if line.lower().startswith("content-length:"):
                    length = int(line.split(":", 1)[1].strip())
            body = b""
            while len(body) < length:
                chunk = f.read(length - len(body))
                if not chunk:
                    self._fail()
                    return
                body += chunk
            try:
                self._dispatch(json.loads(body.decode("utf-8")))
            except Exception:
                continue

    def _dispatch(self, msg: dict) -> None:
        if "id" in msg and "method" in msg:
            self._answer_server(msg)
        elif "id" in msg:
            with self._lock:
                self._responses[msg["id"]] = msg
                ev = self._events.get(msg["id"])
            if ev:
                ev.set()

    def _answer_server(self, msg: dict) -> None:
        # Answer server->client requests so Pyright never blocks (load-bearing).
        if msg.get("method") == "workspace/configuration":
            result = [None] * len(msg.get("params", {}).get("items", []))
        else:
            result = None
        self._send({"jsonrpc": "2.0", "id": msg["id"], "result": result})

    def request(self, method: str, params: dict, timeout: float = REQ_TIMEOUT):
        """Returns (result, hung). hung=True on timeout OR crash (no response present)."""
        with self._lock:
            self._id += 1
            mid = self._id
            ev = threading.Event()
            self._events[mid] = ev
        self._send({"jsonrpc": "2.0", "id": mid, "method": method, "params": params})
        ev.wait(timeout)
        with self._lock:
            resp = self._responses.pop(mid, None)
            self._events.pop(mid, None)
        if resp is None:                       # timeout or crash-woke with no response
            return None, True
        return resp.get("result"), False

    def notify(self, method: str, params: dict) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def shutdown(self) -> None:
        try:
            self.request("shutdown", {}, timeout=5)
            self.notify("exit", {})
        except Exception:
            pass
        try:
            self.proc.terminate()
        except Exception:
            pass


# --- langserver resolution -------------------------------------------------------------

def find_langserver(repo_root: Path, override: str | None = None) -> list[str] | None:
    """Resolve the langserver invocation argv, or None (-> fail-soft oracle-unavailable).

    Order: (1) --langserver (a langserver.index.js path); (2) the vendored
    node_modules/pyright/langserver.index.js; (3) a `pyright-langserver` on PATH.
    """
    if override:
        return ["node", str(Path(override)), "--stdio"]
    vendored = repo_root / "node_modules" / "pyright" / "langserver.index.js"
    if vendored.exists():
        return ["node", str(vendored), "--stdio"]
    on_path = shutil.which("pyright-langserver")
    if on_path:
        return [on_path, "--stdio"]
    return None


# --- the oracle proper -----------------------------------------------------------------

def _uri_to_relpath(loc_uri: str, repo_root: Path) -> str:
    path = unquote(urlparse(loc_uri).path)
    if len(path) >= 3 and path[0] == "/" and path[2] == ":":
        path = path[1:]            # "/C:/x" -> "C:/x"
    try:
        return os.path.relpath(path, str(repo_root)).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


def _extract_dependents(locations, definition: Definition, repo_root: Path) -> list[dict]:
    """Map LSP Location[] -> [{file, line(1-based)}], excluding the declaration site.

    A symbol is not its own reverse-dependent: drop the Location whose (uri, start) equals
    the definition's own name position (drive-case-insensitive uri compare)."""
    def_uri = uri((repo_root / definition.file).resolve()).lower()
    seen: set[tuple[str, int]] = set()
    deps: list[dict] = []
    for loc in locations or []:
        loc_uri = loc.get("uri", "")
        start = loc.get("range", {}).get("start", {})
        line0 = start.get("line")
        char0 = start.get("character")
        if (
            loc_uri.lower() == def_uri
            and line0 == definition.line
            and char0 == definition.character
        ):
            continue  # the declaration itself
        rel = _uri_to_relpath(loc_uri, repo_root)
        key = (rel, line0 if line0 is not None else -1)
        if key in seen:
            continue
        seen.add(key)
        deps.append({"file": rel, "line": (line0 + 1) if line0 is not None else None})
    deps.sort(key=lambda d: (d["file"], d["line"] if d["line"] is not None else -1))
    return deps


def _warm_and_query(lsp: LSP, definition: Definition, repo_root: Path, deadline_s: float):
    """Canary-stable readiness gate = completeness signal. Poll references() every 250 ms;
    `complete` when count >= 1 is equal for two consecutive polls; else `partial` at the
    deadline (never hang). The stable poll's result IS the answer (the canary is the symbol).
    """
    turi = uri((repo_root / definition.file).resolve())
    params = {
        "textDocument": {"uri": turi},
        "position": {"line": definition.line, "character": definition.character},
        "context": {"includeDeclaration": True},
    }
    start = time.perf_counter()
    last_count = -1
    last_result: list = []
    while time.perf_counter() - start < deadline_s:
        res, hung = lsp.request("textDocument/references", params)
        if lsp.crashed:
            raise OracleUnavailable("language server crashed during query")
        if hung:
            continue  # still indexing; keep polling until the deadline
        count = len(res) if isinstance(res, list) else -1
        if count >= 1:
            last_result = res
            if count == last_count:
                return res, True              # two consecutive equal counts -> complete
        last_count = count
        time.sleep(POLL_INTERVAL)
    return last_result, False                 # deadline hit -> partial (last known result)


def _provenance(repo_root: Path, completeness: str) -> dict:
    g = git_provenance(repo_root)
    return {
        "git_rev": g["git_rev"],
        "dirty": g["dirty"],
        "dirty_files": g["dirty_files"],
        "reflects": "working-tree",
        "completeness": completeness,
        "caveats": list(CAVEATS),
        "oracle": {"engine": "pyright-langserver", "method": "textDocument/references"},
    }


def _def_dict(d: Definition) -> dict:
    return {"file": d.file, "kind": d.kind, "line": d.line + 1, "character": d.character}


def _envelope(symbol, file, status, repo_root, *, definition=None, candidates=None,
              reverse_dependents=None, completeness="not-computed", reason=None) -> dict:
    """The single answer envelope — provenance is present on EVERY status."""
    resolution: dict = {"status": status}
    if definition is not None:
        resolution["definition"] = _def_dict(definition)
    if candidates is not None:
        resolution["candidates"] = [_def_dict(d) for d in candidates]
    if reason is not None:
        resolution["reason"] = reason
    deps = reverse_dependents or []
    return {
        "schema": SCHEMA,
        "query": {"symbol": symbol, "file": file},
        "resolution": resolution,
        "reverse_dependents": deps,
        "reverse_dependent_count": len(deps),
        "provenance": _provenance(repo_root, completeness),
    }


def run_oracle(symbol: str, file: str | None, repo_root: Path,
               langserver: str | None = None, timeout: float = DEFAULT_WARM_TIMEOUT) -> dict:
    """Resolve `symbol`, query Pyright references(), assemble the provenance-bearing answer.

    Every startup/runtime failure maps to an `oracle-unavailable` envelope — never raises to
    the caller (gate-safety contract; a consuming gate must not inherit a crash)."""
    repo_root = repo_root.resolve()
    defs = resolve_symbol(symbol, repo_root, file)
    if not defs:
        return _envelope(symbol, file, "symbol-not-found", repo_root,
                         reason=f"no def/class named {symbol!r} in scripts/")
    if len(defs) > 1:
        return _envelope(symbol, file, "ambiguous", repo_root, candidates=defs,
                         reason=f"{len(defs)} definitions; re-run with --file to disambiguate")
    definition = defs[0]

    argv = find_langserver(repo_root, langserver)
    if argv is None:
        return _envelope(symbol, file, "oracle-unavailable", repo_root, definition=definition,
                         reason=_INSTALL_HINT)

    lsp: LSP | None = None
    try:
        lsp = LSP(argv)
        init_params = {
            "processId": os.getpid(),
            "rootUri": uri(repo_root),
            "capabilities": {
                "textDocument": {"references": {}, "callHierarchy": {},
                                 "synchronization": {"didSave": False}},
                "workspace": {"workspaceFolders": True, "configuration": True},
                "window": {"workDoneProgress": True}},
            "workspaceFolders": [{"uri": uri(repo_root), "name": repo_root.name}],
            "initializationOptions": {},
        }
        _res, hung = lsp.request("initialize", init_params)
        if hung or lsp.crashed:
            raise OracleUnavailable("language server failed to initialize (timeout or crash)")
        lsp.notify("initialized", {})

        fpath = (repo_root / definition.file).resolve()
        lsp.notify("textDocument/didOpen", {"textDocument": {
            "uri": uri(fpath), "languageId": "python", "version": 1,
            "text": fpath.read_text(encoding="utf-8")}})

        locations, complete = _warm_and_query(lsp, definition, repo_root, timeout)
        deps = _extract_dependents(locations, definition, repo_root)
        return _envelope(symbol, file, "resolved", repo_root, definition=definition,
                         reverse_dependents=deps,
                         completeness="complete" if complete else "partial")
    except OracleUnavailable as exc:
        return _envelope(symbol, file, "oracle-unavailable", repo_root, definition=definition,
                         reason=str(exc))
    except Exception as exc:  # belt-and-suspenders: NO startup/query error may crash a gate
        return _envelope(symbol, file, "oracle-unavailable", repo_root, definition=definition,
                         reason=f"unexpected oracle error: {exc!r}")
    finally:
        if lsp is not None:
            lsp.shutdown()


# --- rendering -------------------------------------------------------------------------

def format_text(answer: dict) -> str:
    """Human mode — flat key:value/bullets inside ONE triple-backtick fence (CLAUDE.md §4),
    so the TUI renders it raw and a copy carries no box-drawing borders."""
    res = answer["resolution"]
    status = res["status"]
    prov = answer["provenance"]
    sym = answer["query"]["symbol"]
    out: list[str] = []
    if status == "resolved":
        d = res["definition"]
        out.append(f"reverse-dependents of {sym} ({d['file']}:{d['line']}, {d['kind']}): "
                   f"{answer['reverse_dependent_count']} found")
        dirty = f"yes ({len(prov['dirty_files'])} file(s))" if prov["dirty"] else "no"
        out.append(f"completeness: {prov['completeness']} | "
                   f"git_rev: {(prov['git_rev'] or '?')[:7]} | dirty: {dirty}")
        out.append("")
        out.append("referencers:")
        out.extend(f"- {dep['file']}:{dep['line']}" for dep in answer["reverse_dependents"])
        if not answer["reverse_dependents"]:
            out.append("- (none)")
    elif status == "ambiguous":
        out.append(f"ambiguous: {sym} has {len(res['candidates'])} definitions "
                   f"- re-run with --file")
        out.extend(f"- {c['file']}:{c['line']} ({c['kind']})" for c in res["candidates"])
    elif status == "symbol-not-found":
        out.append(f"symbol-not-found: {res.get('reason', sym)}")
    elif status == "oracle-unavailable":
        out.append(f"oracle-unavailable: {res.get('reason', '')}")
    out.append("")
    out.append("caveats:")
    out.extend(f"- {c}" for c in prov["caveats"])
    return "```\n" + "\n".join(out) + "\n```"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reverse_dep_oracle",
        description="Code->code reverse-dependency oracle (Pyright references; ADR-89 #193).",
    )
    parser.add_argument("symbol", help="Python symbol (def/class name) to query")
    parser.add_argument("--file", default=None,
                        help="disambiguate a symbol defined in multiple files")
    parser.add_argument("--json", action="store_true", help="emit the JSON answer envelope")
    parser.add_argument("--text", action="store_true", help="emit human text (default)")
    parser.add_argument("--langserver", default=None,
                        help="path to pyright langserver.index.js (override resolution)")
    parser.add_argument("--timeout", type=float, default=DEFAULT_WARM_TIMEOUT,
                        help="readiness/completeness deadline in seconds (default 20)")
    parser.add_argument("--repo-root", default=str(_REPO_ROOT))
    args = parser.parse_args(argv)

    answer = run_oracle(args.symbol, args.file, Path(args.repo_root),
                        args.langserver, args.timeout)
    if args.json:
        print(json.dumps(answer, indent=2))
    else:
        print(format_text(answer))
    return 0 if answer["resolution"]["status"] == "resolved" else 1


if __name__ == "__main__":
    sys.exit(main())
