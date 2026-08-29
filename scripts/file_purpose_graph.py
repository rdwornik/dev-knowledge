#!/usr/bin/env python
"""file_purpose_graph.py — FPG-1, the file-purpose graph, first slice (A3).

THE QUESTION THIS ANSWERS. `why <path>` returns three things about a governed surface:
**purpose** (what this file is for), **consumers** (what reads it) and **edges** (what it
reads / is coupled to). And on a file nothing explains it REFUSES — *a file nothing explains
is a defect, not a mystery.* The refusal is half the value and it was built first: the
failing witness for this module is `tests/test_file_purpose_graph.py::
test_why_refuses_a_planted_unknown_file`, which was RED against a stub whose `why` answered
every path before this file existed.

FIVE INPUTS, ONE GRAPH. The repo already knows most of this; it knows it in five places that
have never been joined:

  1. `ecosystem/doc-code-edge.yaml`   -- declaration docs and the `<!-- rule: -->` /
     `# rule:` pairs that bind a written rule to the organ enforcing it.
  2. `docs/audits/README.md`          -- the generated index, which is the only surface that
     enumerates the audit corpus.
  3. the `[#595]` consumer-at-landing citations -- BOTH directions: what an artifact declares
     as its consumer, and which governance surface cites the artifact back.
  4. `tasks/**` `depends-on`          -- the row graph. `tasks/` is the SOURCE OF TRUTH;
     `BACKLOG.md` is a generated one-line view and is never read for edges.
  5. `deploy/manifest-v*.yaml`        -- which carrier and which component ship which file.

ONE DIRECTION CONVENTION, AND IT IS LOAD-BEARING. **Every edge points from the consumer to
the thing it consumes**: `A --kind--> B` reads "A depends on / reads / is coupled to B". So
`consumers(X)` is exactly the in-edge set and `edges(X)` exactly the out-edge set, with no
per-kind special-casing at the query boundary. Two edge kinds look inverted until read that
way and both are deliberate: `generated-from` runs from the GENERATED view to the row it
derives from (`BACKLOG.md --generated-from--> task:42`), and `declared-in` runs from the rule
to the doc that declares it. `EDGE_KINDS` registers every kind with the phrase used when it is
rendered outward and the phrase used when it is rendered inward; a kind absent from that table
is a bug the direction-invariant test refuses.

LIBRARY-FIRST — rustworkx, and it is the NAMED CONSUMER standing ruling R-A reserved: *"if a
consumer is ever named, the library is rustworkx, not networkx"*. Authorization is the
operator's A3 mandate verbatim -- *"a real graph library, not more hand-rolled traversal"* --
and the dependency was declared through the ruled ADR-106 path (`pyproject.toml` -> `uv lock`
-> `uv sync --locked`) in its own commit rather than smuggled in with a feature. R-A left
installability MEASUREMENT-OWED-LOCAL; measured in-lane 2026-08-29 under the pinned uv
0.11.19 / CPython 3.12.10 / win_amd64, rustworkx 0.18.1 installs from a PREBUILT hash-pinned
wheel (`rustworkx-0.18.1-cp310-abi3-win_amd64.whl`), so R-A's sqlite/stdlib fallback was NOT
taken. What the library actually buys, beyond storing adjacency: `transitive_consumers()` is
`rustworkx.ancestors` over the whole joined graph, which is the query the five separate
surfaces cannot answer at all -- an enforcing organ is a consumer of the doc that declares
its rule TWO hops out, and no single input knows that.

THE `_parse_deps` TRAP, AND WHICH SIDE OF IT THIS MODULE IS ON. `validate_backlog._parse_deps`
resolves the depends-on clause with `search()`, so it reads only the FIRST clause on a row;
multi-target edges in this repo are therefore written as ONE comma-separated clause. This
module reuses that helper's REGEXES (`_DEPENDS_CLAUSE_RE`, `_DEPID_RE` -- imported, never
re-derived) but applies `finditer()`, so it reads EVERY clause, and it additionally reads the
frontmatter `depends-on:` key that `tasks/112-*.md` carries. Both differences are deliberate
and both are pinned by tests. Consequence, stated rather than left to be discovered: this
module can see a dependency edge the rest of the repo does not. Measured against the live
tree on 2026-08-29 the two readings AGREE -- no row carries a second body clause today -- so
the divergence is latent, not active.

WHAT "GOVERNED" MEANS HERE, and its honest limit. A path is governed iff at least one of the
five inputs names it. Nothing else confers it -- not existing, not being imported, not being
tested. That is the point: measured against the live tree, most of `scripts/` and all of
`tests/` are UNKNOWN to this graph, and `why` refuses them. That refusal is the finding, not
a gap in the query.

PHASE FENCE (FPG-1). New-files-first: this module is a library plus a CLI. It is wired into
NO gate, no check and no hook. Making `check_funnel_lifecycle` -- or anything else -- consume
the predicate is a later batch and is deliberately not done here.

LAYER-2 POSTURE: read-only. Nothing here writes a file, and no health number is emitted, so
the A1 telemetry clause is not engaged; the store that WOULD receive one is
`logs/TELEMETRY.db` via `scripts/telemetry_emit.py`, named here so a later slice does not
have to rediscover it or invent a second store.

Output is ASCII-only in the printed strings (a Windows cp1252 console crashes on arrow
glyphs), flat key/value and bullets rather than a table, so a pasted transcript carries no
render-layer border glyphs.

Usage:
    python scripts/file_purpose_graph.py why <path> [--repo-root .] [--depth N]
    python scripts/file_purpose_graph.py stats [--repo-root .]
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import rustworkx
import yaml

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

# LIBRARY-FIRST, and every one of these is a regex or scanner that has already been hardened
# somewhere else in this repo. Re-deriving any of them would be a second chance to get a
# boundary wrong -- `_AUDIT_NAME_RE` alone carries five rounds of measured boundary fixes.
from consumer_at_landing import (  # noqa: E402
    _COMMISSION_ID_RE,
    _STEM_RE,
    POOL_DIRS,
    POOL_ROOT_FILES,
    identifiers,
)
from funnel_coverage import _AUDIT_NAME_RE  # noqa: E402
from validate_backlog import _DEPENDS_CLAUSE_RE, _DEPID_RE  # noqa: E402
from validate_doc_code_edge import DOC_RE, markers_in_source  # noqa: E402

# --------------------------------------------------------------------------------------- ids

#: The five inputs, by the name each stamps on the edges it contributes. `INPUTS` is the
#: checkable roster: the live-repo test asserts that every one of them actually contributed at
#: least one edge, so an input that silently stops resolving fails rather than thinning the
#: graph unnoticed.
INPUT_DOC_CODE_EDGE = "doc-code-edge"
INPUT_AUDITS_INDEX = "audits-index"
INPUT_CONSUMER_AT_LANDING = "consumer-at-landing"
INPUT_TASKS_DEPENDS_ON = "tasks-depends-on"
INPUT_DEPLOY_MANIFEST = "deploy-manifest"

INPUTS: tuple[str, ...] = (
    INPUT_DOC_CODE_EDGE,
    INPUT_AUDITS_INDEX,
    INPUT_CONSUMER_AT_LANDING,
    INPUT_TASKS_DEPENDS_ON,
    INPUT_DEPLOY_MANIFEST,
)

EDGE_ENFORCES = "enforces"
EDGE_DECLARED_IN = "declared-in"
EDGE_INDEXES = "indexes"
EDGE_CITES = "cites"
EDGE_CONSUMED_BY = "consumed-by"
EDGE_DEPENDS_ON = "depends-on"
EDGE_SHIPS = "ships"
EDGE_CARRIER_SOURCE = "carrier-source"
EDGE_CARRIED_BY = "carried-by"
EDGE_GOVERNED_BY = "governed-by"
EDGE_GENERATED_FROM = "generated-from"

#: kind -> (phrase when rendered on an OUT edge, phrase when rendered on an IN edge). Every
#: kind the builder emits is registered here; `test_every_edge_is_consumer_to_consumed`
#: refuses an unregistered one, because an unregistered kind renders as a bare token and
#: silently breaks the one direction convention this module's readability rests on.
EDGE_KINDS: dict[str, tuple[str, str]] = {
    EDGE_ENFORCES: ("enforces", "is enforced by"),
    EDGE_DECLARED_IN: ("is declared in", "declares"),
    EDGE_INDEXES: ("indexes", "is indexed by"),
    EDGE_CITES: ("cites", "is cited by"),
    EDGE_CONSUMED_BY: ("consumes", "is consumed by"),
    EDGE_DEPENDS_ON: ("depends on", "is depended on by"),
    EDGE_SHIPS: ("ships", "is shipped by"),
    EDGE_CARRIER_SOURCE: ("carries", "is carried by"),
    EDGE_CARRIED_BY: ("is carried by", "carries"),
    EDGE_GOVERNED_BY: ("is governed by", "governs"),
    EDGE_GENERATED_FROM: ("is generated from", "generates"),
}

NODE_FILE = "file"
NODE_RULE = "rule"
NODE_TASK = "task"
NODE_ADR = "adr"
NODE_INTAKE = "intake"
NODE_CARRIER = "carrier"
NODE_COMPONENT = "component"

#: A governed file that states no purpose of its own. NOT a refusal -- "nothing explains this
#: file" and "this file states no purpose" are different facts and are reported differently.
NO_STATED_PURPOSE = "<no stated purpose>"

# ------------------------------------------------------------------------------ small parsers

_H1_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.M)
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.S)
_TASK_ID_RE = re.compile(r"\[#(\d+)\]")
_ADR_RE = re.compile(r"\bADR-(\d+)(?![0-9])")
_INTAKE_RE = re.compile(r"\bintake\s+#(\d+)", re.I)
_WF_RE = re.compile(r"\b(wf-[0-9a-f]{6,})\b")
#: A generated-index row: `- [2026-08-29](2026-08-29-slug.md) - Title`. Link target only.
_INDEX_ROW_RE = re.compile(r"^\s*[-*]\s*\[[^\]]*\]\((?P<target>[^)]+)\)", re.M)
_MANIFEST_VERSION_RE = re.compile(r"manifest-v(?P<v>[0-9]+(?:\.[0-9]+)*)\.yaml$")
_STANDING_RULINGS_PATH = "protocols/STANDING_RULINGS.md"

DOC_CODE_EDGE_RELPATH = "ecosystem/doc-code-edge.yaml"
AUDITS_INDEX_RELPATH = "docs/audits/README.md"
AUDITS_RELPATH = "docs/audits"
TASKS_RELPATH = "tasks"
DEPLOY_RELPATH = "deploy"


def _read(path: Path) -> str | None:
    """Text, or None. A file this module cannot read contributes no edge and says nothing --
    it never silently becomes an empty one."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _frontmatter(text: str) -> dict:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        loaded = yaml.safe_load(match.group("body"))
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _body_after_frontmatter(text: str) -> str:
    match = _FRONTMATTER_RE.match(text)
    return text[match.end():] if match else text


def parse_dep_ids(row_text: str) -> list[str]:
    """Every depends-on id on a row -- EVERY clause, not just the first.

    `validate_backlog._parse_deps` resolves the same clause with `search()` and so reads only
    the first one. The REGEXES here are that helper's, imported rather than re-derived; the
    quantifier is the deliberate difference, and it is pinned by
    `test_multi_target_depends_on_reads_every_id_in_the_clause`.
    """
    out: list[str] = []
    for match in _DEPENDS_CLAUSE_RE.finditer(row_text):
        for dep in _DEPID_RE.findall(match.group(1)):
            if dep not in out:
                out.append(dep)
    return out


# ------------------------------------------------------------------------------------- model


@dataclass(frozen=True)
class Node:
    """One vertex. `path` is the repo-relative file this node IS, when it is a file at all --
    a rule, an ADR and a manifest component are governed objects with no path of their own."""
    kind: str
    key: str
    label: str
    path: str | None = None


@dataclass(frozen=True)
class Edge:
    """One directed edge, consumer -> consumed. `source` names which of the five inputs
    contributed it, so an answer can always be traced back to the surface that asserted it."""
    src: str
    dst: str
    kind: str
    source: str
    detail: str = ""


@dataclass
class Answer:
    """What `why` returns: the three answers, plus the node it resolved to."""
    path: str
    node: Node
    purpose: str
    consumers: list[tuple[Edge, Node]] = field(default_factory=list)
    edges: list[tuple[Edge, Node]] = field(default_factory=list)


class UnknownFile(RuntimeError):
    """`why` refused: no input explains this path.

    `exists` distinguishes the two flavours, which are genuinely different facts. `True` --
    the file is on disk and NOTHING in the five inputs explains it: that is the governance
    defect this module exists to surface. `False` -- there is no such path at all: a typo or
    a stale locator, a different problem with a different fix.
    """

    def __init__(self, path: str, exists: bool):
        self.path = path
        self.exists = exists
        if exists:
            super().__init__(
                f"{path}: nothing explains this file. It is on disk and no governed input "
                f"(doc-code-edge registry, audits index, consumer-at-landing citation, "
                f"tasks/ depends-on, deploy manifest) names it. A file nothing explains is a "
                f"defect, not a mystery."
            )
        else:
            super().__init__(f"{path}: no such path in this repo (nothing to explain).")


class PurposeGraph:
    """The five inputs joined into one queryable rustworkx DiGraph."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.graph: rustworkx.PyDiGraph = rustworkx.PyDiGraph()
        self._index: dict[str, int] = {}      # node key -> rustworkx index
        self._by_path: dict[str, str] = {}    # repo-relative path -> node key
        self._edges: list[Edge] = []

    # -- construction ------------------------------------------------------------------
    def add_node(self, node: Node) -> str:
        existing = self._index.get(node.key)
        if existing is None:
            self._index[node.key] = self.graph.add_node(node)
        elif node.path and not self.graph[existing].path:
            # A node first seen without a path (a task cited before its file was walked)
            # gains it when the file itself is read. Identity is the key, never the path.
            self.graph[existing] = node
        if node.path:
            self._by_path.setdefault(node.path, node.key)
        return node.key

    def add_edge(self, edge: Edge) -> None:
        src, dst = self._index.get(edge.src), self._index.get(edge.dst)
        if src is None or dst is None or src == dst:
            return  # a dangling or self edge is dropped, never invented
        self.graph.add_edge(src, dst, edge)
        self._edges.append(edge)

    # -- query -------------------------------------------------------------------------
    def node(self, key: str) -> Node | None:
        idx = self._index.get(key)
        return None if idx is None else self.graph[idx]

    def key_for_path(self, relpath: str) -> str | None:
        return self._by_path.get(relpath)

    def all_edges(self) -> list[Edge]:
        return list(self._edges)

    def consumers(self, key: str) -> list[tuple[Edge, Node]]:
        """In-edges: what reads this."""
        idx = self._index[key]
        return sorted(
            ((payload, self.graph[src]) for src, _dst, payload in self.graph.in_edges(idx)),
            key=lambda pair: (pair[0].kind, pair[1].key),
        )

    def edges_out(self, key: str) -> list[tuple[Edge, Node]]:
        """Out-edges: what this reads / is coupled to."""
        idx = self._index[key]
        return sorted(
            ((payload, self.graph[dst]) for _src, dst, payload in self.graph.out_edges(idx)),
            key=lambda pair: (pair[0].kind, pair[1].key),
        )

    def transitive_consumers(self, key: str) -> set[str]:
        """Every node that reaches this one, at any depth -- `rustworkx.ancestors`.

        This is the query no single input can answer, and the reason a real graph library
        earns its place: an organ enforcing a rule is a consumer of the doc declaring that
        rule two hops out, via a node neither surface shares.
        """
        idx = self._index.get(key)
        if idx is None:
            return set()
        return {self.graph[i].key for i in rustworkx.ancestors(self.graph, idx)}


# ------------------------------------------------------------------------------- node helpers


def _file_key(relpath: str) -> str:
    return f"{NODE_FILE}:{relpath}"


def _file_node(relpath: str) -> Node:
    return Node(NODE_FILE, _file_key(relpath), relpath, relpath)


def _task_key(task_id: str) -> str:
    return f"{NODE_TASK}:{task_id}"


# --------------------------------------------------------------------------------- purpose


def _purpose_of(repo_root: Path, node: Node) -> str:
    """What the file says it is for, read from the file itself -- never invented.

    A `tasks/` row states it in its frontmatter `title`; a Python module in the first
    paragraph of its module docstring; a markdown document in its H1. A file that states none
    says so — which is a different fact from a file nothing EXPLAINS, and is reported
    differently (this returns `NO_STATED_PURPOSE`; that raises `UnknownFile`).
    """
    if node.path is None:
        return node.label
    path = repo_root / node.path
    text = _read(path)
    if text is None:
        return NO_STATED_PURPOSE

    if node.kind == NODE_TASK:
        title = _frontmatter(text).get("title")
        return str(title).strip() if title else NO_STATED_PURPOSE

    if node.path.endswith(".py"):
        # `ast.get_docstring`, not a quote scan. The scan this replaced went RED on
        # `scripts/block_ff_push.py` for a reason worth keeping: it required the docstring to
        # be the first thing in the file, and every script here opens with a shebang. The AST
        # knows what a module docstring IS; a string search only knows what one looks like.
        #
        # The first PARAGRAPH, not the first line: these docstrings wrap at ~95 columns, so a
        # first line is a fragment ("...refuse a push that would put a non-merge") rather than
        # a purpose. The leading `name.py -- ` self-identifying prefix is stripped, or every
        # answer would open by repeating the path the caller just typed.
        try:
            doc = ast.get_docstring(ast.parse(text))
        except (SyntaxError, ValueError):
            return NO_STATED_PURPOSE
        if not doc:
            return NO_STATED_PURPOSE
        paragraph = " ".join(
            line.strip()
            for line in doc.strip().split("\n\n")[0].splitlines()
            if line.strip()
        )
        prefix = Path(node.path).name
        for sep in (" -- ", " — ", " - "):
            if paragraph.startswith(prefix + sep):
                return paragraph[len(prefix) + len(sep):].strip()
        return paragraph or NO_STATED_PURPOSE

    heading = _H1_RE.search(text)
    if heading:
        return heading.group("title").strip()
    frontmatter_title = _frontmatter(text).get("title")
    if frontmatter_title:
        return str(frontmatter_title).strip()
    return NO_STATED_PURPOSE


# ----------------------------------------------------------------------------- input loaders


def _load_doc_code_edge(graph: PurposeGraph, root: Path) -> None:
    """INPUT 1 -- `ecosystem/doc-code-edge.yaml`.

    Contributes `enforces` (a code organ -> the rule it enforces) and `declared-in` (a rule ->
    the doc that authoritatively declares it).

    ONE PASS over `scripts/`, not `build_edge_index`. That helper re-walks and re-tokenizes
    every `.py` once PER RULE ID: measured on the live tree 2026-08-29, 14.53s for 16 rules
    against 0.75s for the single pass below -- a 19x cost for an identical id set, on a query
    a human runs interactively. The hardened scanners are still reused rather than re-derived
    (`markers_in_source`, which tokenizes so a `# rule:` inside a string literal is never a
    hit, and `DOC_RE` for the doc side).
    """
    text = _read(root / DOC_CODE_EDGE_RELPATH)
    if text is None:
        return
    try:
        config = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return
    declaration_docs = [str(d) for d in (config.get("declaration_docs") or [])]

    for rel in declaration_docs:
        doc_text = _read(root / rel)
        if doc_text is None:
            continue
        graph.add_node(_file_node(rel))
        for rule_id in sorted({m.group(1) for m in DOC_RE.finditer(doc_text)}):
            key = graph.add_node(Node(NODE_RULE, f"{NODE_RULE}:{rule_id}", rule_id))
            graph.add_edge(Edge(key, _file_key(rel), EDGE_DECLARED_IN,
                                INPUT_DOC_CODE_EDGE, "declaration doc"))

    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        return
    for py in sorted(scripts_dir.rglob("*.py")):
        src = _read(py)
        if src is None:
            continue
        try:
            marker_ids = markers_in_source(src)
        except Exception:  # noqa: BLE001 -- an untokenizable file is skipped, never fatal
            continue
        if not marker_ids:
            continue
        rel = py.relative_to(root).as_posix()
        graph.add_node(_file_node(rel))
        for rule_id in sorted(marker_ids):
            key = graph.add_node(Node(NODE_RULE, f"{NODE_RULE}:{rule_id}", rule_id))
            graph.add_edge(Edge(_file_key(rel), key, EDGE_ENFORCES,
                                INPUT_DOC_CODE_EDGE, "# rule: marker"))


def _load_audits_index(graph: PurposeGraph, root: Path) -> None:
    """INPUT 2 -- the generated `docs/audits/README.md`.

    Contributes `indexes` (the index -> each artifact it enumerates). The index is GENERATED
    FROM the corpus, so under this module's direction convention it is a consumer of every
    artifact it lists.
    """
    text = _read(root / AUDITS_INDEX_RELPATH)
    if text is None:
        return
    graph.add_node(_file_node(AUDITS_INDEX_RELPATH))
    for match in _INDEX_ROW_RE.finditer(text):
        target = match.group("target").strip()
        if not target.endswith(".md") or target.startswith(("http://", "https://")):
            continue
        rel = f"{AUDITS_RELPATH}/{target.lstrip('./')}"
        graph.add_node(_file_node(rel))
        graph.add_edge(Edge(_file_key(AUDITS_INDEX_RELPATH), _file_key(rel),
                            EDGE_INDEXES, INPUT_AUDITS_INDEX, "generated index row"))


def _governance_node(graph: PurposeGraph, token_kind: str, value: str) -> str:
    """The node a governance citation names. A `[#id]` resolves to the TASK node, not to a
    second file node, so an audit citing `[#42]` and the row at `tasks/42-*.md` meet."""
    if token_kind == NODE_TASK:
        return graph.add_node(Node(NODE_TASK, _task_key(value), f"[#{value}]"))
    if token_kind == NODE_ADR:
        return graph.add_node(Node(NODE_ADR, f"{NODE_ADR}:{value}", f"ADR-{value}"))
    if token_kind == NODE_INTAKE:
        return graph.add_node(Node(NODE_INTAKE, f"{NODE_INTAKE}:{value}", f"intake #{value}"))
    return graph.add_node(_file_node(_STANDING_RULINGS_PATH))


def _audit_paths(root: Path) -> list[Path]:
    """The corpus, RECURSIVE and minus the generated index -- the `consumer_at_landing` v2
    corpus definition, adopted rather than re-decided (its v1 flat glob let a nested launch
    contract sit outside both legs)."""
    audits = root / AUDITS_RELPATH
    if not audits.is_dir():
        return []
    return sorted(p for p in audits.rglob("*.md") if p.is_file() and p.name != "README.md")


def _load_consumer_at_landing(graph: PurposeGraph, root: Path) -> None:
    """INPUT 3 -- the `[#595]` consumer-at-landing citations, BOTH directions.

    `cites` -- an artifact -> the governance object it declares as its consumer (the four
    forms `[#595]` names: a row, an ADR, the rulings register, an intake).
    `consumed-by` -- a governance-pool file -> the artifact it names back.

    IDENTIFIER-KEYED, NEVER FILENAME-KEYED, which is `[#595]`'s explicit requirement and the
    hub diagnostic's own lesson: the corpus cites by identifier, and a filename-keyed reader
    would have called 14 live documents orphans. `identifiers()` and the three hardened
    token regexes are imported from that module, not re-derived.
    """
    by_identifier: dict[str, str] = {}
    for path in _audit_paths(root):
        rel = path.relative_to(root).as_posix()
        graph.add_node(_file_node(rel))
        for token in identifiers(path.name):
            by_identifier[token] = rel
        match = _COMMISSION_ID_RE.search(path.name)
        if match:
            by_identifier[match.group(1)] = rel

        text = _read(path)
        if text is None:
            continue
        for pattern, kind in ((_TASK_ID_RE, NODE_TASK), (_ADR_RE, NODE_ADR),
                              (_INTAKE_RE, NODE_INTAKE)):
            for value in sorted({m.group(1) for m in pattern.finditer(text)}):
                dst = _governance_node(graph, kind, value)
                graph.add_edge(Edge(_file_key(rel), dst, EDGE_CITES,
                                    INPUT_CONSUMER_AT_LANDING, "consumer declaration"))
        if "STANDING_RULINGS" in text:
            dst = _governance_node(graph, NODE_FILE, "")
            graph.add_edge(Edge(_file_key(rel), dst, EDGE_CITES,
                                INPUT_CONSUMER_AT_LANDING, "consumer declaration"))

    # -- the consumption half: one linear pass over the governance pool.
    for path in _pool_paths(root):
        rel = path.relative_to(root).as_posix()
        text = _read(path)
        if text is None:
            continue
        named: set[str] = set()
        named.update(m.group(1) for m in _AUDIT_NAME_RE.finditer(text))
        named.update(m.group(1) for m in _STEM_RE.finditer(text))
        named.update(m.group(1) for m in _WF_RE.finditer(text))
        hits = {by_identifier[token] for token in named if token in by_identifier}
        if not hits:
            continue
        src = graph.key_for_path(rel) or graph.add_node(_file_node(rel))
        for target in sorted(hits):
            graph.add_edge(Edge(src, _file_key(target), EDGE_CONSUMED_BY,
                                INPUT_CONSUMER_AT_LANDING, "governance citation"))


def _pool_paths(root: Path) -> list[Path]:
    """The governance pool, verbatim from `consumer_at_landing` (`POOL_DIRS` +
    `POOL_ROOT_FILES`, imported). Copying that decision rather than re-making it is the point:
    the exclusions -- JOURNAL, handoffs, ecosystem, scripts, tests -- ARE the diagnostic's
    finding, not an oversight to be quietly widened here."""
    out: list[Path] = []
    for rel in POOL_DIRS:
        directory = root / rel
        if directory.is_dir():
            out.extend(sorted(p for p in directory.rglob("*.md") if p.is_file()))
    for rel in POOL_ROOT_FILES:
        path = root / rel
        if path.is_file():
            out.append(path)
    return out


def _load_tasks(graph: PurposeGraph, root: Path) -> None:
    """INPUT 4 -- `tasks/**` `depends-on`. The SOURCE OF TRUTH; `BACKLOG.md` is a generated
    one-line view and is never read for an edge.

    Contributes `depends-on` (row -> row) and `generated-from` (a generated view -> the row
    whose frontmatter declares it generates that view -- inverted, because the view is what
    consumes the row).
    """
    tasks_dir = root / TASKS_RELPATH
    if not tasks_dir.is_dir():
        return
    pending: list[tuple[str, list[str], str | None]] = []
    for path in sorted(tasks_dir.glob("*.md")):
        text = _read(path)
        if text is None:
            continue
        frontmatter = _frontmatter(text)
        raw_id = str(frontmatter.get("id", ""))
        match = _TASK_ID_RE.search(raw_id) or re.match(r"^(\d+)-", path.name)
        if not match:
            continue
        task_id = match.group(1)
        rel = path.relative_to(root).as_posix()
        graph.add_node(Node(NODE_TASK, _task_key(task_id), f"[#{task_id}]", rel))

        deps = parse_dep_ids(_body_after_frontmatter(text))
        # The frontmatter key too: `tasks/112-*.md` carries its dep BOTH places, and reading
        # only the row would drop the edge on a row that carries it only in frontmatter.
        for dep in _DEPID_RE.findall(str(frontmatter.get("depends-on", ""))):
            if dep not in deps:
                deps.append(dep)
        generates = frontmatter.get("generates")
        pending.append((task_id, deps, str(generates).strip() if generates else None))

    for task_id, deps, generates in pending:
        for dep in deps:
            dep_key = _task_key(dep)
            if graph.node(dep_key) is None:
                continue  # a dangling id is validate_backlog's finding, not an invented node
            graph.add_edge(Edge(_task_key(task_id), dep_key, EDGE_DEPENDS_ON,
                                INPUT_TASKS_DEPENDS_ON, "depends-on clause"))
        if generates:
            graph.add_node(_file_node(generates))
            graph.add_edge(Edge(_file_key(generates), _task_key(task_id), EDGE_GENERATED_FROM,
                                INPUT_TASKS_DEPENDS_ON, "frontmatter generates:"))


def _latest_manifest(root: Path) -> Path | None:
    """The highest-versioned `deploy/manifest-v*.yaml`.

    ONE manifest, not a union across releases: the manifest is versioned WITH the methodology,
    so unioning v1.0.0..v1.4.0 would report a component that was pruned two releases ago as a
    live consumer. Sorted on the parsed numeric tuple rather than lexically, or v1.10.0 would
    sort below v1.4.0.
    """
    deploy = root / DEPLOY_RELPATH
    if not deploy.is_dir():
        return None
    candidates: list[tuple[tuple[int, ...], Path]] = []
    for path in deploy.glob("manifest-v*.yaml"):
        match = _MANIFEST_VERSION_RE.search(path.name)
        if match:
            candidates.append((tuple(int(p) for p in match.group("v").split(".")), path))
    return max(candidates)[1] if candidates else None


def _adr_ids(value) -> list[str]:
    items = value if isinstance(value, list) else [value]
    out: list[str] = []
    for item in items:
        out.extend(m.group(1) for m in _ADR_RE.finditer(str(item)))
    return out


def _load_deploy_manifest(graph: PurposeGraph, root: Path) -> None:
    """INPUT 5 -- `deploy/manifest-v*.yaml`.

    Contributes `carrier-source` (a carrier -> the hub file it carries), `ships` (a component
    -> each hub source file it ships), `carried-by` (component -> carrier) and `governed-by`
    (either -> the ADR that decided it).
    """
    manifest_path = _latest_manifest(root)
    if manifest_path is None:
        return
    text = _read(manifest_path)
    if text is None:
        return
    try:
        manifest = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return
    rel_manifest = manifest_path.relative_to(root).as_posix()
    graph.add_node(_file_node(rel_manifest))

    def _link_adrs(src_key: str, raw) -> None:
        for adr in _adr_ids(raw):
            dst = graph.add_node(Node(NODE_ADR, f"{NODE_ADR}:{adr}", f"ADR-{adr}"))
            graph.add_edge(Edge(src_key, dst, EDGE_GOVERNED_BY,
                                INPUT_DEPLOY_MANIFEST, rel_manifest))

    for carrier in manifest.get("carriers") or []:
        if not isinstance(carrier, dict) or not carrier.get("id"):
            continue
        carrier_id = str(carrier["id"])
        key = graph.add_node(Node(NODE_CARRIER, f"{NODE_CARRIER}:{carrier_id}", carrier_id))
        target = carrier.get("target")
        if isinstance(target, dict) and target.get("source_path"):
            rel = str(target["source_path"]).strip()
            graph.add_node(_file_node(rel))
            graph.add_edge(Edge(key, _file_key(rel), EDGE_CARRIER_SOURCE,
                                INPUT_DEPLOY_MANIFEST, f"carrier {carrier_id}"))
        _link_adrs(key, carrier.get("adr"))

    for component in manifest.get("components") or []:
        if not isinstance(component, dict) or not component.get("id"):
            continue
        component_id = str(component["id"])
        key = graph.add_node(
            Node(NODE_COMPONENT, f"{NODE_COMPONENT}:{component_id}", component_id))
        carrier_id = component.get("carrier")
        if carrier_id:
            dst = graph.add_node(
                Node(NODE_CARRIER, f"{NODE_CARRIER}:{carrier_id}", str(carrier_id)))
            graph.add_edge(Edge(key, dst, EDGE_CARRIED_BY,
                                INPUT_DEPLOY_MANIFEST, f"component {component_id}"))
        for artifact in component.get("artifacts") or []:
            if not isinstance(artifact, dict):
                continue
            # `source` is the HUB path (what the component reads); `path` is the CONSUMER
            # target. Only the hub side is a node here -- a consumer's tree is not this
            # repo's file space, and inventing a node for it would fabricate a local file.
            rel = str(artifact.get("source") or "").strip()
            if not rel or rel.startswith("~"):
                continue
            graph.add_node(_file_node(rel))
            graph.add_edge(Edge(key, _file_key(rel), EDGE_SHIPS,
                                INPUT_DEPLOY_MANIFEST, f"component {component_id}"))
        _link_adrs(key, component.get("adr"))


# --------------------------------------------------------------------------------- the build


def build(repo_root: Path | str) -> PurposeGraph:
    """Join all five inputs into one graph. Read-only; nothing is written or cached."""
    root = Path(repo_root).resolve()
    graph = PurposeGraph(root)
    # ORDER IS LOAD-BEARING, and it cost a RED to learn. `tasks/` runs BEFORE the
    # consumer-at-landing pass because a `tasks/NNN-*.md` path must already resolve to its
    # `task:NNN` node when the pool pass reaches it. With the passes the other way round the
    # pool pass minted a second, path-keyed `file:tasks/NNN-*.md` node, and the row's own
    # `depends-on` edges then hung off a DIFFERENT vertex than its citations -- one file,
    # two half-answers, no error. Identity before adjacency.
    _load_doc_code_edge(graph, root)
    _load_audits_index(graph, root)
    _load_tasks(graph, root)
    _load_consumer_at_landing(graph, root)
    _load_deploy_manifest(graph, root)
    return graph


def _normalise(repo_root: Path, path: str) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(repo_root).as_posix()
        except ValueError:
            return candidate.as_posix()
    return candidate.as_posix().lstrip("./")


def why(graph: PurposeGraph, path: str) -> Answer:
    """Purpose, consumers and edges for one governed path -- or a refusal.

    Raises `UnknownFile` when no input explains the path. That is the deliverable's other
    half: a file nothing explains is a defect, not a mystery, and reporting an empty answer
    for it would launder the defect into a shrug.
    """
    rel = _normalise(graph.repo_root, path)
    key = graph.key_for_path(rel)
    if key is None:
        raise UnknownFile(rel, exists=(graph.repo_root / rel).exists())
    node = graph.node(key)
    return Answer(
        path=rel,
        node=node,
        purpose=_purpose_of(graph.repo_root, node),
        consumers=graph.consumers(key),
        edges=graph.edges_out(key),
    )


# ----------------------------------------------------------------------------------- render


def _render_row(edge: Edge, node: Node, outward: bool) -> str:
    phrase = EDGE_KINDS.get(edge.kind, (edge.kind, edge.kind))[0 if outward else 1]
    return f"  - {phrase:<20} {node.key:<52} [{edge.source}]"


#: Rows printed per section before the answer is truncated. `docs/audits/README.md` has 787
#: out-edges on the live tree, so an untruncated answer is a scroll, not an answer. The COUNT
#: in the section header is never truncated -- it is the evidence -- and `--limit 0` prints
#: everything for a machine reader.
DEFAULT_ROW_LIMIT = 20


def _render_section(header: str, pairs, outward: bool, limit: int) -> list[str]:
    lines = [header]
    if not pairs:
        return lines + ["  (none)"]
    shown = pairs if limit <= 0 else pairs[:limit]
    lines.extend(_render_row(edge, node, outward) for edge, node in shown)
    if len(shown) < len(pairs):
        lines.append(f"  ... {len(pairs) - len(shown)} more not shown "
                     f"(--limit 0 for all; the count above is the evidence)")
    return lines


def render(answer: Answer, limit: int = DEFAULT_ROW_LIMIT) -> str:
    """Flat key/value + bullets, no column padding a table would need -- so a pasted
    transcript carries no render-layer border glyphs (CLAUDE.md output-formatting)."""
    lines = [
        f"path     : {answer.path}",
        f"node     : {answer.node.key}",
        f"purpose  : {answer.purpose}",
        "",
    ]
    lines += _render_section(
        f"consumers ({len(answer.consumers)}) -- what reads this",
        answer.consumers, outward=False, limit=limit)
    lines.append("")
    lines += _render_section(
        f"edges ({len(answer.edges)}) -- what this reads / is coupled to",
        answer.edges, outward=True, limit=limit)
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Query the file-purpose graph (FPG-1). Read-only; wired into no gate.")
    # `--repo-root` is declared on the top-level parser AND on every subparser, via a shared
    # parent. argparse does not let a top-level optional appear after the subcommand, so
    # `why <path> --repo-root X` -- the order a person actually types -- would otherwise exit
    # 2 on a usage error rather than answering.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=None,
                        help="repo to read (default: this script's repo)")
    parser.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True)
    ask = sub.add_parser("why", parents=[common],
                         help="purpose + consumers + edges for one governed path")
    ask.add_argument("path")
    ask.add_argument("--depth", type=int, default=1,
                     help="with --depth 2+, also list transitive consumers")
    ask.add_argument("--limit", type=int, default=DEFAULT_ROW_LIMIT,
                     help=f"rows per section (default {DEFAULT_ROW_LIMIT}; 0 = all)")
    sub.add_parser("stats", parents=[common], help="node/edge counts per input")

    args = parser.parse_args(argv)
    # A governance corpus carries em-dashes and typographic quotes, and this command ECHOES
    # file-authored text (an H1, a docstring). On a cp1252/cp437 console an unencodable
    # character raises UnicodeEncodeError mid-print, which would turn a read-only query into a
    # traceback. Degrade the character, never the answer.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass
    root = Path(args.repo_root).resolve() if args.repo_root else _SCRIPTS.parent
    graph = build(root)

    if args.command == "stats":
        print(f"nodes    : {graph.graph.num_nodes()}")
        print(f"edges    : {graph.graph.num_edges()}")
        for source in INPUTS:
            count = sum(1 for edge in graph.all_edges() if edge.source == source)
            print(f"  {source:<22} {count}")
        return 0

    try:
        answer = why(graph, args.path)
    except UnknownFile as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(render(answer, limit=args.limit))
    if args.depth > 1:
        reachable = sorted(graph.transitive_consumers(answer.node.key))
        print(f"\ntransitive consumers ({len(reachable)}) -- any depth")
        for key in reachable:
            print(f"  - {key}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main())
