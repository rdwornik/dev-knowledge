#!/usr/bin/env python
"""system_map.py -- the generated drill-down system map: one JSON, one static HTML page, no LLM.

WHAT THIS ANSWERS. "What is this system, stage by stage, down to the file -- and which parts
of it are dead?" Before this module the answer was a hand-join of six surfaces. Here it is ONE
deterministic JSON built from those surfaces, and ONE static HTML page rendered from that JSON
(inline JS for expand/collapse and a filter; no CDN, no network, no model call). Row `[#781]`
nearest; batch BW lane C6 (`lane-bw-781-system-map`), adopted by R96 D4, grimp by D15.

TWO VIEWS, C4-style:
  * PROCESS -- ADR -> backlog -> task -> distiller -> lane -> checkers -> land -> rollup ->
    handoff. Each stage names the scripts that realise it: a short DECLARED table
    (`PROCESS_STAGES`) plus every script `ecosystem/harness.yaml` wires into a spine stage or a
    moment, attached to the process stage that moment belongs to (`_MOMENT_STAGE`). A declared
    script that is not on disk renders MISSING rather than vanishing.
  * MODULE -- system -> stage -> script -> file leaf. A leaf carries purpose, consumers,
    imports / imported-by, tests, last commit and used yes/no. Files no stage claims sit under
    an "unstaged" group per area, so nothing in the leaf set is dropped.

INPUTS, and none of them is a parallel census:
  * `scripts/file_purpose_graph.py` (FPG-1) -- purpose, consumers, `triggers`, `imports`. A
    leaf FPG cannot explain (`UnknownFile`) is rendered UNEXPLAINED and listed separately:
    *a file nothing explains is a defect, not a mystery* -- dropping it would hide the defect.
  * `grimp.build_graph("scripts")` -- the module import graph (see HONEST LIMIT below).
  * `scripts/generate_organ_index.py::collect_organs` -- the organ roster that renders
    `ecosystem/organ-index.md`, REUSED, not re-derived. An organ with no trigger renders DEAD
    (`organ_state`), in the organ table AND in a separate DEAD list: an omitted dead organ is
    indistinguishable from one never built.
  * `ecosystem/harness.yaml` (spine stages and moments), `ecosystem/provider-registry.yaml`
    (providers and roles), and the `.claude/commands|skills|agents` listings (as leaves).

HONEST LIMIT -- grimp over a non-package. The hub's `scripts/` has no `__init__.py`
(`worktree_import_proof.py` says NOT-APPLICABLE), so grimp builds it as a NAMESPACE package
rooted at the repo, in a separate `python -I` process so the caller's `sys.modules` cannot
redirect it to another checkout. grimp therefore sees the `scripts.`-qualified import form
(`from scripts import x`, the dual-import shim's first leg) and NOT the bare `import x` form
that resolves through `scripts/` on `sys.path`. FPG's own `ast` pass resolves that bare form,
so a leaf's `imports` is the UNION of both, and `meta.grimp` / `meta.fpg_imports` report each
source's edge count separately. No edge is invented to close the gap.

DETERMINISM. Same tree -> byte-identical JSON: every collection is sorted, the JSON is
dumped with sorted keys and ASCII escapes, and nothing reads the clock, the user's home or
the commit history. A leaf's LAST COMMIT is history, not tree (two identical trees reached
by different histories differ in it -- Codex r1 HIGH), so `last_commits()` feeds the HTML
only and stays out of the hashed JSON. The map sha is sha256 of the JSON bytes. The record
file is EXCLUDED from the leaf set, so committing a new record never changes the map it
records.

WHAT IS COMMITTED (Done-contract item 4). The JSON and HTML are regenerate-on-demand outputs
and are GITIGNORED, on the `ecosystem/trends.html` precedent (`.gitignore`): a committed
generated page goes stale and then needs a freshness gate to police a staleness that only
exists because it is committed; and the JSON moves with every content change of
any leaf, so a committed JSON would churn. What IS committed is `ecosystem/system-map-record.json` -- the
map sha, the previous sha, the added/removed node diff and the node list the next diff is
taken against -- the place the handoff generator (lane D2) reads. A rebuild that yields the
same sha leaves the record byte-untouched, so `/map` on an unchanged tree dirties nothing.

Layer-2 posture: read-only over the repo except the two gitignored outputs and the one record.

Usage:
    uv run --locked python scripts/system_map.py build [--repo-root .] [--out-dir DIR] [--record PATH]
"""

from __future__ import annotations

import hashlib
import html
import json
import logging
import subprocess
import sys
from collections import Counter
from pathlib import Path

import click
import yaml

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

import file_purpose_graph as fpg  # noqa: E402
import generate_organ_index as goi  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("system-map")

_REPO_ROOT = _SCRIPTS.parent

SCHEMA = "system-map/1"
RECORD_SCHEMA = "system-map-record/1"
JSON_NAME = "system-map.json"
HTML_NAME = "system-map.html"
RECORD_REL = "ecosystem/system-map-record.json"
DEFAULT_OUT_REL = "ecosystem"

LIVE = "LIVE"
DEAD = "DEAD"
MISSING = "MISSING"
UNEXPLAINED = "UNEXPLAINED"

#: Consumers listed per leaf before the list is cut; the COUNT is never cut.
CONSUMER_SAMPLE = 25

#: The leaf set: every tracked file under these trees. `ecosystem/` contributes its direct
#: children only -- its `*/history/` trees are dated records, not system parts.
LEAF_TREES = (
    "scripts/", ".claude/commands/", ".claude/skills/", ".claude/agents/",
    ".claude/workflows/", ".claude/rules/", "plugins/",
)
LEAF_FLAT = ("ecosystem/",)

#: The process view's declared spine (Proposal section 9 C). Each stage names the scripts
#: that realise it; harness wiring adds more (see `_MOMENT_STAGE`).
PROCESS_STAGES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("adr", "ADR", ("scripts/validate_adr_status.py",)),
    ("backlog", "Backlog", ("scripts/gen_task_tree.py", "scripts/validate_backlog.py")),
    ("task", "Task", ("scripts/task_record.py", "scripts/row_close.py")),
    ("distiller", "Distiller", ("scripts/gen_lane_contract.py",)),
    ("lane", "Lane", ("scripts/dispatch.py", "scripts/lane_boot.py")),
    ("checkers", "Checkers", ("scripts/gates.py", "scripts/dodo.py")),
    ("land", "Land", ("scripts/merge_path.py", "scripts/merge_receipt.py")),
    ("rollup", "Rollup", ("scripts/lane_digest.py", "scripts/transport_report.py")),
    ("handoff", "Handoff", ("scripts/gen_handoff.py",)),
)

#: Which process stage a harness moment belongs to. The 12 spine stages prepare a lane
#: contract, so they belong to the distiller.
_MOMENT_STAGE = {
    "spine": "distiller",
    "pre-launch": "lane",
    "lane-start": "lane",
    "merge": "land",
    "teardown": "land",
    "lane-end": "rollup",
    "batch-close": "rollup",
    "seat-release": "handoff",
}

#: An organ is DEAD when nothing fires it: its trigger is absent or manual-only, or the
#: organ index reports it not armed.
_TRIGGERLESS = frozenset({"", "manual", "none", "(unparsed)", "(absent)"})
_DEAD_STATUSES = frozenset({"MANUAL", "ABSENT", "DISARMED", "RETIRED", "(unparsed)",
                            "(absent)"})

_GRIMP_PROGRAM = r"""
import json, sys
root = sys.argv[1]
sys.path.insert(0, root)
import grimp
g = grimp.build_graph("scripts", cache_dir=None)
mods = sorted(g.modules)
edges = sorted([m, i] for m in mods for i in g.find_modules_directly_imported_by(m))
print(json.dumps({"modules": mods, "edges": edges}))
"""


# ------------------------------------------------------------------------------- collection


def _git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                             text=True, encoding="utf-8", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


def _all_files(root: Path) -> list[str]:
    """Tracked files (repo-relative POSIX), or a filesystem walk outside a git work tree."""
    tracked = goi.tracked_files(root)
    if tracked is not None:
        return sorted(tracked)
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and ".git" not in p.relative_to(root).parts)


def _is_leaf(rel: str) -> bool:
    if rel == RECORD_REL or "__pycache__" in rel:
        return False
    if rel.startswith(LEAF_TREES):
        return True
    return any(rel.startswith(p) and "/" not in rel[len(p):] for p in LEAF_FLAT)


def _area(rel: str) -> str:
    for prefix in LEAF_TREES + LEAF_FLAT:
        if rel.startswith(prefix):
            return prefix.rstrip("/")
    return rel.split("/", 1)[0]


def last_commits(root: Path, leaves: list[str] | None = None) -> dict[str, str]:
    """{path: 12-char sha of the newest commit touching it}, from ONE `git log` pass.

    HISTORY, not tree: rendered on the HTML page only, never part of the hashed JSON."""
    root = Path(root).resolve()
    if leaves is None:
        leaves = [p for p in _all_files(root) if _is_leaf(p)]
    if not leaves:
        return {}
    text = _git(root, "log", "--format=%x01%H", "--name-only", "--no-renames", "--",
                *sorted({_area(p) for p in leaves}))
    if text is None:
        return {}
    wanted, out, current = set(leaves), {}, None
    for line in text.splitlines():
        if line.startswith("\x01"):
            current = line[1:][:12]
        elif line and current and line in wanted and line not in out:
            out[line] = current
    return out


def _module_path(root: Path, module: str) -> str | None:
    parts = module.split(".")
    for candidate in ("/".join(parts) + ".py", "/".join(parts) + "/__init__.py"):
        if (root / candidate).is_file():
            return candidate
    return None


def grimp_imports(root: Path) -> tuple[dict, list[tuple[str, str]]]:
    """(meta, [(importer path, imported path)]) from grimp, run in an isolated interpreter."""
    meta = {"package": "scripts", "mode": "namespace package rooted at the repo",
            "modules": 0, "edges": 0, "error": None}
    if not (root / "scripts").is_dir():
        meta["error"] = "no scripts/ directory"
        return meta, []
    try:
        out = subprocess.run([sys.executable, "-I", "-c", _GRIMP_PROGRAM, str(root)],
                             capture_output=True, text=True, encoding="utf-8",
                             cwd=str(root), timeout=300)
    except (OSError, subprocess.SubprocessError) as exc:
        meta["error"] = type(exc).__name__
        return meta, []
    if out.returncode != 0:
        lines = (out.stderr or "").strip().splitlines()
        meta["error"] = lines[-1] if lines else f"exit {out.returncode}"
        return meta, []
    payload = json.loads(out.stdout)
    edges = []
    for src, dst in payload["edges"]:
        a, b = _module_path(root, src), _module_path(root, dst)
        if a and b and a != b:
            edges.append((a, b))
    meta["modules"] = len(payload["modules"])
    meta["edges"] = len(edges)
    return meta, sorted(set(edges))


def _organ_script(root: Path, organ: goi.Organ, hook_entries: dict[str, str]) -> str | None:
    """The in-repo script an organ runs, when one can be named from its own row."""
    candidates = [organ.name, hook_entries.get(organ.name, ""), organ.source]
    for text in candidates:
        name = goi._script_name(text or "")
        if not name:
            continue
        for base in ("scripts/", "scripts/hooks/", ""):
            if (root / (base + name)).is_file():
                return base + name
    return None


def _hook_entries(root: Path) -> dict[str, str]:
    try:
        data = yaml.safe_load((root / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    out = {}
    repos = data.get("repos") if isinstance(data, dict) else None
    for repo in repos if isinstance(repos, list) else []:
        hooks = repo.get("hooks") if isinstance(repo, dict) else None
        for hook in hooks if isinstance(hooks, list) else []:
            if isinstance(hook, dict) and hook.get("id"):
                out[str(hook["id"])] = str(hook.get("entry", ""))
    return out


def organ_state(organ: goi.Organ) -> tuple[str, str | None]:
    """(LIVE|DEAD, reason). DEAD when nothing fires the organ."""
    trigger = organ.trigger.strip()
    if trigger.lower() in _TRIGGERLESS:
        return DEAD, f"no trigger ({trigger or 'empty'})"
    head = organ.status.split()[0] if organ.status.strip() else "(absent)"
    if head in _DEAD_STATUSES:
        return DEAD, f"status {organ.status}"
    return LIVE, None


def _organs(root: Path) -> list[dict]:
    entries = _hook_entries(root)
    rows, seen = [], Counter()
    for organ in goi.collect_organs(root):
        base = f"organ:{organ.cls}:{organ.name}"
        seen[base] += 1
        state, reason = organ_state(organ)
        rows.append({
            "id": base if seen[base] == 1 else f"{base}#{seen[base]}",
            "name": organ.name, "class": organ.cls, "trigger": organ.trigger,
            "source": organ.source, "distribution": organ.distribution,
            "status": organ.status, "state": state, "dead_reason": reason,
            "script": _organ_script(root, organ, entries),
        })
    return rows


def _yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def _command_scripts(root: Path, command) -> list[str]:
    tokens = command if isinstance(command, list) else []
    out = set()
    for token in tokens:
        for name in goi._SCRIPT_TOKEN_RE.findall(str(token)):
            for base in ("scripts/", ""):
                if (root / (base + name)).is_file() and (base + name).startswith("scripts/"):
                    out.add(base + name)
        if str(token).startswith("scripts/") and (root / str(token)).is_file():
            out.add(str(token))
    return sorted(out)


def _harness(root: Path) -> dict:
    data = _yaml(root / "ecosystem" / "harness.yaml")
    stages = []
    for row in data.get("stages") or []:
        if isinstance(row, dict):
            stages.append({"stage": row.get("stage"), "name": str(row.get("name", "")),
                           "scripts": _command_scripts(root, row.get("command"))})
    moments = []
    for row in data.get("moments") or []:
        if not isinstance(row, dict):
            continue
        organs = []
        for organ in row.get("organs") or []:
            if isinstance(organ, dict):
                organs.append({"id": str(organ.get("id", "")),
                               "scripts": _command_scripts(root, organ.get("command"))})
        moments.append({"name": str(row.get("name", "")), "organs": organs})
    return {"stages": stages, "moments": moments}


def _providers(root: Path) -> dict:
    data = _yaml(root / "ecosystem" / "provider-registry.yaml")
    providers = data.get("providers") if isinstance(data.get("providers"), dict) else {}
    roles = data.get("roles") if isinstance(data.get("roles"), dict) else {}
    return {
        "providers": [{"id": str(k), "display_name": str((v or {}).get("display_name", k))
                       if isinstance(v, dict) else str(k)} for k, v in sorted(providers.items())],
        "roles": sorted(str(k) for k in roles),
    }


# ---------------------------------------------------------------------------------- assembly


def _process(root: Path, harness: dict) -> list[dict]:
    extra: dict[str, set[str]] = {sid: set() for sid, _l, _s in PROCESS_STAGES}
    for stage in harness["stages"]:
        extra[_MOMENT_STAGE["spine"]].update(stage["scripts"])
    for moment in harness["moments"]:
        target = _MOMENT_STAGE.get(moment["name"], "checkers")
        for organ in moment["organs"]:
            extra[target].update(organ["scripts"])
    out = []
    for sid, label, declared in PROCESS_STAGES:
        scripts = sorted(set(declared) | extra[sid])
        missing = sorted(p for p in scripts if not (root / p).is_file())
        out.append({"id": f"stage:{sid}", "label": label, "scripts": scripts,
                    "missing": missing, "state": MISSING if missing else LIVE})
    return out


def build_map(repo_root: Path | str) -> dict:
    """Join every input into ONE map dict. Deterministic for a given checkout."""
    root = Path(repo_root).resolve()
    files = _all_files(root)
    leaves = [p for p in files if _is_leaf(p)]
    tests = [p for p in files if p.startswith("tests/") and p.endswith(".py")]

    logger.info("building the file-purpose graph over %s", root)
    graph = fpg.build(root)
    logger.info("building the grimp import graph")
    grimp_meta, grimp_edges = grimp_imports(root)
    organs = _organs(root)
    harness = _harness(root)
    process = _process(root, harness)
    providers = _providers(root)

    imports: dict[str, set[str]] = {p: set() for p in leaves}
    imported_by: dict[str, set[str]] = {p: set() for p in leaves}
    for src, dst in grimp_edges:
        if src in imports:
            imports[src].add(dst)
        if dst in imported_by:
            imported_by[dst].add(src)
    fpg_import_edges = 0
    organ_by_script: dict[str, list[str]] = {}
    for organ in organs:
        if organ["script"]:
            organ_by_script.setdefault(organ["script"], []).append(organ["id"])
    live_organ_scripts = {o["script"] for o in organs if o["script"] and o["state"] == LIVE}
    live_organ_sources = {o["source"] for o in organs if o["state"] == LIVE}

    leaf_rows: dict[str, dict] = {}
    unexplained = []
    for rel in leaves:
        try:
            answer = fpg.why(graph, rel)
        except fpg.UnknownFile:
            answer = None
        row = {"path": rel, "area": _area(rel), "explained": answer is not None,
               "tests": [], "organs":
               sorted(organ_by_script.get(rel, []))}
        if rel.endswith(".py"):
            stem = Path(rel).stem
            row["tests"] = [t for t in tests if Path(t).name in (f"test_{stem}.py",)
                            or Path(t).name.startswith(f"test_{stem}_")]
        if answer is None:
            unexplained.append(rel)
            row.update({"purpose": UNEXPLAINED, "consumers": 0, "consumer_kinds": {},
                        "consumers_sample": [], "triggered_by": []})
        else:
            purpose = " ".join(answer.purpose.split())
            if not purpose or purpose == fpg.NO_STATED_PURPOSE:
                purpose = "NO_STATED_PURPOSE"
            kinds = Counter(edge.kind for edge, _node in answer.consumers)
            row.update({
                "purpose": purpose,
                "consumers": len(answer.consumers),
                "consumer_kinds": dict(sorted(kinds.items())),
                "consumers_sample": [f"{edge.kind} {node.key}" for edge, node
                                     in answer.consumers[:CONSUMER_SAMPLE]],
                "triggered_by": sorted({node.path or node.key for edge, node
                                        in answer.consumers
                                        if edge.kind == fpg.EDGE_TRIGGERS}),
            })
            for edge, node in answer.edges:
                if edge.kind == fpg.EDGE_IMPORTS and node.path:
                    fpg_import_edges += 1
                    imports[rel].add(node.path)
                    if node.path in imported_by:
                        imported_by[node.path].add(rel)
            for edge, node in answer.consumers:
                if edge.kind == fpg.EDGE_IMPORTS and node.path:
                    imported_by[rel].add(node.path)
        leaf_rows[rel] = row

    for rel, row in leaf_rows.items():
        row["imports"] = sorted(imports[rel])
        row["imported_by"] = sorted(imported_by[rel])
        # A data or doc leaf is read, not imported: any non-`implements` consumer counts.
        # A `.py` leaf is used only when something runs or imports it -- a row claiming it
        # (`implements`) or a doc citing it does not execute it.
        readers = any(kind != fpg.EDGE_IMPLEMENTS for kind in row["consumer_kinds"])
        used = bool(row["triggered_by"] or row["imported_by"]
                    or rel in live_organ_scripts or rel in live_organ_sources
                    or (not rel.endswith(".py") and readers))
        # A data file nothing is recorded as reading is UNKNOWN, not unused: code reads it by
        # a path string, which no graph input traces. Only a process file can be called unused.
        if not used and fpg.process_class(rel) is None and not rel.endswith(".py"):
            used = None
        row["used"] = used

    staged = {p for stage in process for p in stage["scripts"]}
    modules = [{"id": stage["id"], "label": stage["label"],
                "files": [p for p in stage["scripts"] if p in leaf_rows]}
               for stage in process]
    unstaged: dict[str, list[str]] = {}
    for rel in leaves:
        if rel not in staged:
            unstaged.setdefault(_area(rel), []).append(rel)
    modules.append({"id": "stage:unstaged", "label": "Unstaged (no process stage)",
                    "groups": [{"area": area, "files": unstaged[area]}
                               for area in sorted(unstaged)]})

    dead = sorted(o["id"] for o in organs if o["state"] == DEAD)
    nodes = sorted(
        [s["id"] for s in process] + ["stage:unstaged"]
        + [f"file:{p}" for p in leaves] + [o["id"] for o in organs]
        + [f"provider:{p['id']}" for p in providers["providers"]]
        + [f"moment:{m['name']}" for m in harness["moments"]]
    )
    return {
        "schema": SCHEMA,
        "generator": "scripts/system_map.py",
        "meta": {
            "grimp": grimp_meta,
            "fpg_imports": fpg_import_edges,
            "leaf_count": len(leaves),
            "organ_count": len(organs),
            "dead_count": len(dead),
            "unexplained_count": len(unexplained),
            "dead_rule": "an organ is DEAD when its trigger is empty or manual-only, or its "
                         "status is one of " + ", ".join(sorted(_DEAD_STATUSES)),
            "used_rule": "a leaf is used when something triggers or imports it, or it is "
                         "the script or source of a LIVE organ, or (a non-.py leaf only) "
                         "any non-implements consumer reads it; a non-process, non-.py "
                         "leaf with no recorded reader is null (unknown), because code "
                         "reads data files by path string, which no graph input traces",
        },
        "process": process,
        "modules": modules,
        "files": leaf_rows,
        "organs": organs,
        "dead_organs": dead,
        "unexplained": unexplained,
        "harness": harness,
        "providers": providers,
        "nodes": nodes,
    }


def render_json(data: dict) -> bytes:
    """Canonical bytes: sorted keys, ASCII escapes, LF, trailing newline."""
    return (json.dumps(data, sort_keys=True, indent=1, ensure_ascii=True) + "\n").encode("ascii")


def map_sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


# ------------------------------------------------------------------------------------- html

_CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1b;--muted:#6b6b66;--line:#deddd8;--card:#ffffff;
--dead:#b3261e;--deadbg:#fbeaea;--warn:#8a5a00;--warnbg:#fff4dc;--ok:#1e6b3a}
@media (prefers-color-scheme: dark){:root{--bg:#161615;--fg:#ecebe6;--muted:#a3a29b;
--line:#34332f;--card:#1f1f1d;--dead:#ff8a80;--deadbg:#3a1d1b;--warn:#f0c46a;
--warnbg:#3a2f14;--ok:#7fd49a}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0;
padding:16px;max-width:1100px}
h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:24px 0 8px}
code,.mono{font-family:ui-monospace,Consolas,monospace;font-size:12.5px}
.muted{color:var(--muted)}
details{border:1px solid var(--line);background:var(--card);border-radius:6px;
margin:4px 0;padding:4px 8px}
summary{cursor:pointer}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}
td,th{border-bottom:1px solid var(--line);padding:3px 6px;text-align:left;vertical-align:top}
.dead{color:var(--dead);background:var(--deadbg)}
.unexplained{border-color:var(--warn)}
.badge{font-size:11px;padding:0 5px;border-radius:4px;margin-left:6px;font-weight:600}
.badge.dead{color:var(--dead);background:var(--deadbg)}
.badge.warn{color:var(--warn);background:var(--warnbg)}
.badge.ok{color:var(--ok)}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
input{flex:1;min-width:160px;padding:4px 6px}
"""

_JS = """
(function(){
  function all(open){document.querySelectorAll('details').forEach(function(d){d.open=open;});}
  document.getElementById('expand').onclick=function(){all(true);};
  document.getElementById('collapse').onclick=function(){all(false);};
  document.getElementById('filter').oninput=function(e){
    var q=e.target.value.toLowerCase();
    document.querySelectorAll('[data-leaf]').forEach(function(el){
      el.style.display=(!q||el.getAttribute('data-leaf').toLowerCase().indexOf(q)>=0)?'':'none';
    });
  };
})();
"""


def _e(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _leaf_html(row: dict, history: dict[str, str]) -> str:
    badges = []
    if not row["explained"]:
        badges.append(f'<span class="badge warn">{UNEXPLAINED}</span>')
    if row["used"] is None:
        badges.append('<span class="badge warn">used: unknown</span>')
    else:
        badges.append('<span class="badge ok">used</span>' if row["used"]
                      else '<span class="badge dead">unused</span>')
    cls = ' class="unexplained"' if not row["explained"] else ""

    def items(values):
        return ", ".join(f"<code>{_e(v)}</code>" for v in values) or '<span class="muted">none</span>'

    sample = "".join(f"<li><code>{_e(c)}</code></li>" for c in row["consumers_sample"])
    more = row["consumers"] - len(row["consumers_sample"])
    if more > 0:
        sample += f'<li class="muted">... {more} more</li>'
    return (
        f'<details{cls} data-leaf="{_e(row["path"])}"><summary><code>{_e(row["path"])}</code>'
        f'{"".join(badges)}</summary>'
        f'<div>purpose: {_e(row["purpose"])}</div>'
        f'<div>consumers: {row["consumers"]} {_e(json.dumps(row["consumer_kinds"], sort_keys=True))}</div>'
        f'<ul>{sample}</ul>'
        f'<div>triggered by: {items(row["triggered_by"])}</div>'
        f'<div>imports: {items(row["imports"])}</div>'
        f'<div>imported by: {items(row["imported_by"])}</div>'
        f'<div>tests: {items(row["tests"])}</div>'
        f'<div>organs: {items(row["organs"])}</div>'
        f'<div>last commit: <code>{_e(history.get(row["path"]) or "none")}</code></div>'
        f"</details>"
    )


def render_html(data: dict, sha: str, history: dict[str, str] | None = None) -> str:
    """ONE static page from the map dict (plus the optional `last_commits` history, which is
    shown per leaf but is not part of the hashed JSON). No network, no model."""
    history = history or {}
    files = data["files"]
    meta = data["meta"]
    out = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>System map</title>",
        f"<style>{_CSS}</style></head><body>",
        "<h1>System map</h1>",
        f'<div class="muted">generated by <code>scripts/system_map.py</code> -- '
        f"map sha <code>{_e(sha)}</code></div>",
        f'<div class="muted">{meta["leaf_count"]} files, {meta["organ_count"]} organs, '
        f'{meta["dead_count"]} DEAD, {meta["unexplained_count"]} {UNEXPLAINED}; grimp '
        f'{meta["grimp"]["modules"]} modules / {meta["grimp"]["edges"]} edges'
        f'{" (error: " + _e(meta["grimp"]["error"]) + ")" if meta["grimp"]["error"] else ""}'
        f', file-purpose-graph imports {meta["fpg_imports"]}</div>',
        '<div class="toolbar"><button id="expand">Expand all</button>'
        '<button id="collapse">Collapse all</button>'
        '<input id="filter" placeholder="Filter files by path"></div>',
        "<h2>Process view</h2>",
        '<div class="muted">ADR &rarr; backlog &rarr; task &rarr; distiller &rarr; lane '
        "&rarr; checkers &rarr; land &rarr; rollup &rarr; handoff</div>",
    ]
    for stage in data["process"]:
        badge = (f'<span class="badge dead">{MISSING}: {len(stage["missing"])}</span>'
                 if stage["missing"] else "")
        dead_li = ' class="dead"'
        lis = "".join(
            f'<li{dead_li if p in stage["missing"] else ""}><code>{_e(p)}</code></li>'
            for p in stage["scripts"])
        out.append(f'<details><summary>{_e(stage["label"])} '
                   f'<span class="muted">({len(stage["scripts"])} scripts)</span>{badge}'
                   f"</summary><ul>{lis}</ul></details>")

    out.append("<h2>Module view</h2>")
    out.append('<div class="muted">system &rarr; stage &rarr; script &rarr; file</div>')
    for module in data["modules"]:
        if "groups" in module:
            inner = "".join(
                f'<details><summary><code>{_e(g["area"])}</code> '
                f'<span class="muted">({len(g["files"])})</span></summary>'
                + "".join(_leaf_html(files[p], history) for p in g["files"]) + "</details>"
                for g in module["groups"])
            count = sum(len(g["files"]) for g in module["groups"])
        else:
            inner = "".join(_leaf_html(files[p], history) for p in module["files"])
            count = len(module["files"])
        out.append(f'<details><summary>{_e(module["label"])} '
                   f'<span class="muted">({count})</span></summary>{inner}</details>')

    out.append(f'<h2>DEAD organs ({len(data["dead_organs"])})</h2>')
    by_id = {o["id"]: o for o in data["organs"]}
    out.append("<ul>" + "".join(
        f'<li class="dead" data-organ="{_e(i)}"><code>{_e(by_id[i]["name"])}</code> '
        f'({_e(by_id[i]["class"])}) -- {_e(by_id[i]["dead_reason"])}</li>'
        for i in data["dead_organs"]) + "</ul>")

    out.append(f'<h2>Organs ({len(data["organs"])})</h2>')
    out.append("<table><thead><tr><th>State</th><th>Organ</th><th>Class</th><th>Trigger</th>"
               "<th>Status</th><th>Script</th><th>Source</th></tr></thead><tbody>")
    for o in data["organs"]:
        cls = "dead" if o["state"] == DEAD else "live"
        out.append(
            f'<tr class="{cls}" data-organ="{_e(o["id"])}"><td>{_e(o["state"])}</td>'
            f'<td><code>{_e(o["name"])}</code></td><td>{_e(o["class"])}</td>'
            f'<td>{_e(o["trigger"])}</td><td>{_e(o["status"])}</td>'
            f'<td><code>{_e(o["script"] or "")}</code></td><td><code>{_e(o["source"])}</code></td></tr>')
    out.append("</tbody></table>")

    out.append(f'<h2>{UNEXPLAINED} files ({len(data["unexplained"])})</h2>')
    out.append('<div class="muted">On disk, in the map, and named by no input of the '
               "file-purpose graph -- a defect, not a mystery.</div>")
    out.append("<ul>" + "".join(
        f'<li class="unexplained"><code>{_e(p)}</code> <span class="badge warn">'
        f"{UNEXPLAINED}</span></li>" for p in data["unexplained"]) + "</ul>")

    out.append("<h2>Harness moments</h2><ul>")
    for m in data["harness"]["moments"]:
        organs = ", ".join(f"<code>{_e(o['id'])}</code>" for o in m["organs"])
        out.append(f"<li><b>{_e(m['name'])}</b>: {organs}</li>")
    out.append("</ul>")

    prov = data["providers"]
    out.append("<h2>Providers</h2><ul>" + "".join(
        f"<li><code>{_e(p['id'])}</code> {_e(p['display_name'])}</li>"
        for p in prov["providers"]) + "</ul>")
    out.append("<div>roles: " + ", ".join(f"<code>{_e(r)}</code>" for r in prov["roles"])
               + "</div>")
    out.append(f"<script>{_JS}</script></body></html>")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------------- record


def _read_record(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def write_outputs(repo_root: Path | str, out_dir: Path | str, record_path: Path | str) -> dict:
    """Build, write JSON + HTML, and update the record when the sha moved. Returns the record
    plus `changed` (whether the record was rewritten) and the two output paths."""
    root = Path(repo_root).resolve()
    out = Path(out_dir)
    record_file = Path(record_path)
    data = build_map(root)
    blob = render_json(data)
    sha = map_sha(blob)
    out.mkdir(parents=True, exist_ok=True)
    json_path, html_path = out / JSON_NAME, out / HTML_NAME
    json_path.write_bytes(blob)
    html_path.write_bytes(render_html(data, sha, last_commits(root)).encode("utf-8"))

    old = _read_record(record_file)
    paths = {"json_path": json_path.as_posix(), "html_path": html_path.as_posix()}
    if old.get("map_sha") == sha:
        return {**old, **paths, "changed": False}
    old_nodes = set(old.get("nodes") or [])
    new_nodes = set(data["nodes"])
    baseline = not old
    added = [] if baseline else sorted(new_nodes - old_nodes)
    removed = [] if baseline else sorted(old_nodes - new_nodes)
    head = _git(root, "rev-parse", "HEAD")
    record = {
        "schema": RECORD_SCHEMA,
        "generator": "scripts/system_map.py build",
        "map_sha": sha,
        "previous_sha": old.get("map_sha"),
        "built_at": head.strip() if head else None,
        "node_count": len(new_nodes),
        "diff": {"baseline": baseline, "added_count": len(added),
                 "removed_count": len(removed), "added": added, "removed": removed},
        "nodes": sorted(new_nodes),
    }
    record_file.parent.mkdir(parents=True, exist_ok=True)
    record_file.write_bytes(render_json(record))
    return {**record, **paths, "changed": True}


# -------------------------------------------------------------------------------------- cli


@click.group()
def cli() -> None:
    """The generated drill-down system map."""


@cli.command("build")
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path),
              default=_REPO_ROOT, show_default=True)
@click.option("--out-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help=f"Where the JSON and HTML go (default <repo-root>/{DEFAULT_OUT_REL}).")
@click.option("--record", "record_path", type=click.Path(dir_okay=False, path_type=Path),
              default=None, help=f"The committed sha record (default <repo-root>/{RECORD_REL}).")
def build_cmd(repo_root: Path, out_dir: Path | None, record_path: Path | None) -> None:
    """Regenerate the map JSON and HTML; print the paths, the map sha and the node diff."""
    root = repo_root.resolve()
    result = write_outputs(root, out_dir or root / DEFAULT_OUT_REL,
                           record_path or root / RECORD_REL)
    diff = result.get("diff") or {}
    click.echo(f"json: {result['json_path']}")
    click.echo(f"html: {result['html_path']}")
    click.echo(f"map_sha: {result['map_sha']}")
    click.echo(f"previous_sha: {result.get('previous_sha') or 'none'}")
    if diff.get("baseline"):
        click.echo(f"diff: baseline ({result.get('node_count')} nodes)")
    else:
        click.echo(f"diff: +{diff.get('added_count', 0)} -{diff.get('removed_count', 0)} nodes")
    click.echo(f"record: {(record_path or root / RECORD_REL).as_posix()} "
               f"({'updated' if result['changed'] else 'unchanged'})")


if __name__ == "__main__":
    cli()
