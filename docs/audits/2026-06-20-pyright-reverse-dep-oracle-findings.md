# Pyright reverse-dependency oracle — benchmark findings

> **CC Spike (sanctioned throwaway prototype).** ADR-87 auto-mode intent-spec; the
> gate for the code-edge sibling ADR answering **ADR-88 OQ2** ("is a headless
> language server a viable deterministic reverse-dependency oracle for code→code
> edges, or is a custom code graph warranted?"). Measurement only — **zero
> integration**: nothing here is wired into a hook, gate, pre-commit, or `ALL_CHECKS`,
> and no harness lands in `scripts/`. The harness ran in a throwaway temp dir
> (now removed); its full source is embedded below for reproducibility.

**Date:** 2026-06-20
**Tool:** Pyright `1.1.410` (npm `pyright`, `pyright-langserver --stdio`), out-of-the-box (no `pyrightconfig.json`, no tuning).
**Host:** Windows 11, Node v25.2.1, Python 3.12.10.
**Subject:** this repo's `scripts/` surface — **34 `.py` files, ~7.9k LOC, 286 `def`/`class` symbols**.
**Fallback (`python-lsp-server`):** not exercised — Pyright cleared the bar (see Verdict), so the fallback was unnecessary.

---

## Verdict — **GO: Pyright's workspace index suffices as the oracle**

A custom code-knowledge graph is **not** warranted for this repo's code→code
reverse-dependency needs. Every closure number lands inside an interactive agent
edit-loop budget by one to three orders of magnitude, the server is crash/hang-free
under the agent's actual edit-burst pattern, and — decisively — Pyright resolves
references **semantically, not textually** (evidence below). The one caveat is a
one-time call-graph warm-up; it does not change the verdict. See **Scope &
honest limits** for where this verdict stops.

---

## The four closure numbers (n=3 runs, this repo)

| # | Metric | Result | Budget context |
|---|---|---|---|
| 1 | **Cold-start** (spawn → first *stable* `references()` answer) | **3.6 – 4.3 s** (init response ~0.9 s) | One-time per session. Acceptable. |
| 2 | **p95 query latency** — `references()` | **17–18 ms** (p50 ~4 ms; max ~0.3 s first warm query) | Imperceptible in-loop. |
| 2 | **p95 query latency** — call-hierarchy (`prepareCallHierarchy`+`incomingCalls`) | **25–29 ms** (p50 ~20 ms) | Imperceptible in-loop, **but** see warm-up caveat. |
| 3 | **Worst-case payload** — highest-fan-out symbol | **19,468 bytes (~19 KB)** for `Finding` (`audit.py`, **110 refs**) | Trivial for an agent context. |
| 4 | **Stability under edit-burst** | **0 crashes / 0 hangs** over 60 rapid full-document `didChange`s on the busiest file (`audit.py`), 60/60 queries completed, p95-under-burst ~49–70 ms, process alive after | No instability in the agent's real usage pattern. |

Raw per-run figures:

| Run | cold-start s | refs p50/p95/max ms | call-hier p50/p95/max ms | worst payload B | burst crash/hang/done |
|---|---|---|---|---|---|
| 1 | 3.65 | 3.97 / 18.47 / 310.4 | 19.79 / 29.44 / 7519 | 19,468 | 0 / 0 / 60 |
| 2 | 3.74 | 3.60 / 17.43 / 292.9 | 19.48 / 24.96 / 8733 | 19,468 | 0 / 0 / 60 |
| 3 | 4.25 | 3.80 / 18.48 / 292.9 | 21.09 / 27.49 / 9352 | 19,468 | 0 / 0 / 60 |

### Highest-fan-out symbols (Pyright `references()` ground truth)

| Symbol | File | Kind | Refs | Payload |
|---|---|---|---|---|
| `Finding` | audit.py | class | 110 | 19,468 B |
| `RotFinding` | validate_doc_rot.py | class | 13 | 2,422 B |
| `RepoState` | audit.py | class | 12 | 2,123 B |
| `_git` | session_end_backpressure.py | func | 11 | 2,135 B |
| `ClaimResult` | validate_doc_claims.py | class | 11 | 2,087 B |
| `ProbeResult` | verify_handoff_probes.py | class | 10 | 1,917 B |

The distribution is steep: one dominant hub (`Finding`, 110 refs) then a long tail in
the single digits — typical of a small validator codebase. Worst-case payload is
governed by that single hub and is still only ~19 KB.

## Decisive correctness signal — semantic, not grep

The cold-start canary symbol was `main`, which is **defined in 34 separate files**.
A naive text/grep oracle would report ~68 references (34 defs + 34 `__name__`
call-sites collapsed together). Pyright returned **exactly 2** — this module's `def
main` plus its own `if __name__ == "__main__": main()` call — i.e. it scoped the
reference set to the correct module symbol. This is the property a reverse-dependency
oracle must have and that a grep-based stand-in cannot provide. Likewise `Finding`'s
110 refs are real `Finding(...)` constructions in `audit.py`, not incidental string
matches.

## Scope & honest limits (where this verdict stops)

1. **Repo size.** These numbers are for **this repo** (34 files / ~8k LOC), exactly as
   the spec scoped ("on this repo"). Cold-start, resident memory, and worst-case
   payload **grow with workspace size** and will not extrapolate linearly. Reusing
   Pyright as the oracle in a large child repo (e.g. `corp-monorepo`) requires a fresh
   measurement there — this spike does **not** clear that.
2. **First call-hierarchy warm-up (~8 s, one-time).** The call-hierarchy *max* across
   all three runs is 7.5–9.4 s — a single outlier: the **first** `incomingCalls`
   builds the call graph. It is consistent and one-time (p95 stays ~25–29 ms
   thereafter). `references()` has **no** comparable cliff (first-query max ~0.3 s).
   Implication for the consumer ADR: if reverse-dependency is served via
   `references()`, readiness cost is just cold-start (~4 s); if call-hierarchy is
   used, budget an additional ~8 s one-time warm-up, or prefer `references()`.
3. **Static-analysis blind spots.** `references()`/call-hierarchy see only
   **statically resolvable Python** references. Dynamic dispatch, `getattr`/`setattr`,
   string-keyed registries (e.g. `_SPEC_REGISTRY`-style dispatch), reflection, and
   monkeypatching are **invisible**, as are all **cross-language** edges (markdown →
   script, hook-wiring in `settings.json` / `.pre-commit-config.yaml`, plugin
   manifests). The oracle is sound for **code→code static edges** — precisely OQ2's
   scope — and must not be presented as catching the dynamic or cross-modal edges.
4. **Out-of-the-box config.** Default Pyright settings (basic mode, no project
   config). Per the anti-patterns, config was **not** tuned to flatter the numbers.
5. **Harness realism.** The harness `didOpen`s every target file (mirroring an agent
   with files open) and answers Pyright's `workspace/configuration` requests with
   defaults; `references()` resolves workspace-wide regardless of which files are open.

## Method (reproducibility)

- Targets: AST-enumerate every `FunctionDef`/`AsyncFunctionDef`/`ClassDef` in
  `scripts/` → 286 name-position targets (`gen_targets.py`).
- Client: minimal JSON-RPC-over-stdio LSP client (`bench.py`) drives
  `pyright-langserver --stdio`; a reader thread answers server→client requests
  (`workspace/configuration`, `registerCapability`, `workDoneProgress/create`) so
  Pyright never blocks.
- **Cold-start**: poll a canary `references()` every 250 ms from spawn; record the
  elapsed time at the first of a 2-poll stable, non-empty count streak.
- **p95**: `references()` over all 286 targets; call-hierarchy
  (`prepareCallHierarchy` then `incomingCalls`) over the 222 callable targets;
  per-request wall-clock, percentile by linear interpolation.
- **Worst payload**: UTF-8 byte length of the `references()` result JSON; reported for
  the top-fan-out symbol.
- **Edit-burst**: 60 successive full-document `didChange`s (append a comment line,
  versioned) to the busiest file, each immediately followed by a `references()` query
  with a 10 s hang threshold; count process exits (crash) and threshold breaches
  (hang); restore the file at the end.

### Disposition of the throwaway

Sanctioned-throwaway-prototype discipline (governance pointer): the harness was
**not** added to `scripts/` (Layer-2 validators-only invariant) and does not graduate
into the methodology without a separate decision. It ran in a temp dir
(`%TEMP%\pyright-spike-20260620`, Pyright installed there via npm), now removed — no
leftovers. The two source files are embedded below as the durable reproducible record.

<details>
<summary><code>gen_targets.py</code> — AST target enumerator</summary>

```python
"""Enumerate every function/class definition in scripts/ as an LSP query target.

Emits targets.json: [{file, name, kind, line, character}] with 0-based LSP
position pointing at the *name identifier* (not the def/class keyword).
"""
from __future__ import annotations
import ast
import json
import sys
from pathlib import Path

REPO = Path(r"C:\Users\1028120\Documents\Dev\.dev-knowledge")
SCRIPTS = REPO / "scripts"


def targets_for(path: Path) -> list[dict]:
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError as e:
        print(f"skip {path}: {e}", file=sys.stderr)
        return []
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            line0 = node.lineno - 1
            col = node.col_offset
            phys = src.splitlines()[line0]
            idx = phys.find(node.name, col)
            if idx < 0:
                idx = phys.find(node.name)
            if idx < 0:
                continue
            out.append({"file": str(path), "name": node.name,
                        "kind": type(node).__name__, "line": line0, "character": idx})
    return out


def main():
    targets = []
    for p in sorted(SCRIPTS.rglob("*.py")):
        targets.extend(targets_for(p))
    Path("targets.json").write_text(json.dumps(targets, indent=2), encoding="utf-8")
    print(f"{len(targets)} targets across {len(list(SCRIPTS.rglob('*.py')))} files")


if __name__ == "__main__":
    main()
```
</details>

<details>
<summary><code>bench.py</code> — LSP client + four-metric benchmark</summary>

```python
"""Pyright reverse-dependency oracle benchmark (CC Spike, ADR-88 OQ2 gate).

Four numbers + a verdict on the .dev-knowledge scripts/ surface:
  1 cold-start  2 p95 latency (references + incomingCalls)
  3 worst-case payload  4 edit-burst stability
Measurement only. Honest out-of-the-box config. Throwaway.
"""
from __future__ import annotations
import json, os, subprocess, sys, threading, time
from pathlib import Path
from urllib.parse import quote

REPO = Path(r"C:\Users\1028120\Documents\Dev\.dev-knowledge")
LANGSERVER = Path(__file__).parent / "node_modules" / "pyright" / "langserver.index.js"
REQ_TIMEOUT = 30.0
HANG_THRESHOLD = 10.0


def uri(path: Path) -> str:
    s = str(path).replace("\\", "/")
    drive, rest = s[0], s[1:]
    return "file:///" + quote(drive) + "%3A" + quote(rest[1:], safe="/")


class LSP:
    def __init__(self):
        self.proc = subprocess.Popen(
            ["node", str(LANGSERVER), "--stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
        self._id = 0
        self._lock = threading.Lock()
        self._responses, self._events = {}, {}
        self.crashed = False
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _send(self, obj):
        data = json.dumps(obj).encode("utf-8")
        try:
            self.proc.stdin.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii") + data)
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            self.crashed = True

    def _read_loop(self):
        f = self.proc.stdout
        while True:
            headers = b""
            while b"\r\n\r\n" not in headers:
                ch = f.read(1)
                if not ch:
                    self.crashed = True; return
                headers += ch
            length = 0
            for line in headers.decode("ascii", "replace").split("\r\n"):
                if line.lower().startswith("content-length:"):
                    length = int(line.split(":", 1)[1].strip())
            body = b""
            while len(body) < length:
                chunk = f.read(length - len(body))
                if not chunk:
                    self.crashed = True; return
                body += chunk
            try:
                self._dispatch(json.loads(body.decode("utf-8")))
            except Exception:
                continue

    def _dispatch(self, msg):
        if "id" in msg and "method" in msg:
            self._answer_server(msg)
        elif "id" in msg:
            with self._lock:
                self._responses[msg["id"]] = msg
                ev = self._events.get(msg["id"])
            if ev:
                ev.set()

    def _answer_server(self, msg):
        if msg.get("method") == "workspace/configuration":
            result = [None] * len(msg.get("params", {}).get("items", []))
        else:
            result = None
        self._send({"jsonrpc": "2.0", "id": msg["id"], "result": result})

    def request(self, method, params, timeout=REQ_TIMEOUT):
        with self._lock:
            self._id += 1
            mid = self._id
            ev = threading.Event()
            self._events[mid] = ev
        self._send({"jsonrpc": "2.0", "id": mid, "method": method, "params": params})
        ok = ev.wait(timeout)
        with self._lock:
            resp = self._responses.pop(mid, None)
            self._events.pop(mid, None)
        if not ok:
            return None, True
        return (resp or {}).get("result"), False

    def notify(self, method, params):
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def shutdown(self):
        try:
            self.request("shutdown", {}, timeout=5); self.notify("exit", {})
        except Exception:
            pass
        try:
            self.proc.terminate()
        except Exception:
            pass


def pct(values, p):
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * p
    f = int(k); c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)

def main():
    targets = json.loads(Path("targets.json").read_text(encoding="utf-8"))
    results = {"n_targets": len(targets)}
    t_spawn = time.perf_counter()
    lsp = LSP()
    init_params = {
        "processId": os.getpid(), "rootUri": uri(REPO),
        "capabilities": {
            "textDocument": {"references": {}, "callHierarchy": {},
                             "synchronization": {"didSave": False}},
            "workspace": {"workspaceFolders": True, "configuration": True},
            "window": {"workDoneProgress": True}},
        "workspaceFolders": [{"uri": uri(REPO), "name": "dev-knowledge"}],
        "initializationOptions": {}}
    lsp.request("initialize", init_params)
    t_init = time.perf_counter()
    lsp.notify("initialized", {})

    opened = set()
    for t in targets:                                  # open every target file once
        if t["file"] not in opened:
            text = Path(t["file"]).read_text(encoding="utf-8")
            lsp.notify("textDocument/didOpen", {"textDocument": {
                "uri": uri(Path(t["file"])), "languageId": "python",
                "version": 1, "text": text}})
            opened.add(t["file"])

    # --- 1. cold-start: poll a canary references() until count is stable ---
    canary = next((t for t in targets if t["name"] in
                   ("main", "uri", "_send", "request", "check")), targets[0])
    cold_start, streak, last = None, 0, -1
    poll_start = time.perf_counter()
    while time.perf_counter() - poll_start < 90:
        res, _ = lsp.request("textDocument/references", {
            "textDocument": {"uri": uri(Path(canary["file"]))},
            "position": {"line": canary["line"], "character": canary["character"]},
            "context": {"includeDeclaration": True}})
        if lsp.crashed:
            break
        count = len(res) if isinstance(res, list) else -1
        if count >= 1 and count == last:
            streak += 1
            if streak == 1:
                cand = time.perf_counter()
            if streak >= 2:
                cold_start = cand - t_spawn; break
        else:
            streak = 0
        last = count
        time.sleep(0.25)
    results["cold_start_s"] = round(cold_start or time.perf_counter() - t_spawn, 3)
    results["init_response_s"] = round(t_init - t_spawn, 3)

    # --- 2 & 3. references() + call-hierarchy over every target ---
    ref_lat, ch_lat, fanout, ch_payloads = [], [], [], []
    for t in targets:
        turi = uri(Path(t["file"]))
        pos = {"line": t["line"], "character": t["character"]}
        t0 = time.perf_counter()
        res, hung = lsp.request("textDocument/references", {
            "textDocument": {"uri": turi}, "position": pos,
            "context": {"includeDeclaration": True}})
        dt = (time.perf_counter() - t0) * 1000
        if not hung and res is not None:
            ref_lat.append(dt)
            payload = len(json.dumps(res).encode("utf-8")) if res else 0
            fanout.append({"name": t["name"], "file": Path(t["file"]).name,
                           "kind": t["kind"], "refs": len(res) if res else 0,
                           "bytes": payload})
        if t["kind"] in ("FunctionDef", "AsyncFunctionDef"):
            t0 = time.perf_counter()
            prep, hung = lsp.request("textDocument/prepareCallHierarchy",
                                     {"textDocument": {"uri": turi}, "position": pos})
            if not hung and prep:
                inc, hung2 = lsp.request("callHierarchy/incomingCalls", {"item": prep[0]})
                dt = (time.perf_counter() - t0) * 1000
                if not hung2 and inc is not None:
                    ch_lat.append(dt)
                    ch_payloads.append({"name": t["name"], "incoming": len(inc),
                                        "bytes": len(json.dumps(inc).encode("utf-8")) if inc else 0})
        if lsp.crashed:
            results["aborted"] = "process crashed during query sweep"; break

    results["references"] = {"n": len(ref_lat),
        "p50_ms": round(pct(ref_lat, .5), 2), "p95_ms": round(pct(ref_lat, .95), 2),
        "max_ms": round(max(ref_lat), 2) if ref_lat else None}
    results["call_hierarchy"] = {"n": len(ch_lat),
        "p50_ms": round(pct(ch_lat, .5), 2), "p95_ms": round(pct(ch_lat, .95), 2),
        "max_ms": round(max(ch_lat), 2) if ch_lat else None}
    fanout.sort(key=lambda x: x["refs"], reverse=True)
    results["top_fanout"] = fanout[:12]
    results["worst_payload_bytes"] = max((f["bytes"] for f in fanout), default=0)

    # --- 4. edit-burst stability ---
    from collections import Counter
    busiest = Counter(t["file"] for t in targets).most_common(1)[0][0]
    bt = next(t for t in targets if t["file"] == busiest)
    buri = uri(Path(busiest))
    base_text = Path(busiest).read_text(encoding="utf-8")
    crashes = hangs = 0
    burst_lat, version = [], 2
    for i in range(60):
        lsp.notify("textDocument/didChange", {
            "textDocument": {"uri": buri, "version": version},
            "contentChanges": [{"text": base_text + f"\n# edit-burst probe {i}\n"}]})
        version += 1
        if lsp.crashed:
            crashes += 1; break
        t0 = time.perf_counter()
        res, hung = lsp.request("textDocument/references", {
            "textDocument": {"uri": buri},
            "position": {"line": bt["line"], "character": bt["character"]},
            "context": {"includeDeclaration": True}}, timeout=HANG_THRESHOLD)
        dt = (time.perf_counter() - t0) * 1000
        if lsp.crashed or lsp.proc.poll() is not None:
            crashes += 1; break
        if hung:
            hangs += 1
        else:
            burst_lat.append(dt)
    lsp.notify("textDocument/didChange", {                 # restore
        "textDocument": {"uri": buri, "version": version},
        "contentChanges": [{"text": base_text}]})
    results["edit_burst"] = {"busiest_file": Path(busiest).name, "edits": 60,
        "crashes": crashes, "hangs": hangs, "completed_queries": len(burst_lat),
        "p95_under_burst_ms": round(pct(burst_lat, .95), 2) if burst_lat else None,
        "process_alive_after": lsp.proc.poll() is None}

    lsp.shutdown()
    Path("results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```
</details>

---

**Consumer:** the code-edge sibling ADR answering ADR-88 OQ2/OQ6 (authored after this
lands). **Bottom line for that ADR:** adopt Pyright's workspace index as the
code→code reverse-dependency oracle; do not build a custom code graph for this repo.
Carry forward the three limits — re-measure before reuse in a large child repo, budget
the one-time call-hierarchy warm-up (or prefer `references()`), and treat the oracle
as static-Python-only (dynamic and cross-language edges remain out of its reach).
