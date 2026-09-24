#!/usr/bin/env python
"""file_purpose_graph.py — FPG-1, the file-purpose graph, first slice (A3).

THE QUESTION THIS ANSWERS. `why <path>` returns three things about a governed surface:
**purpose** (what this file is for), **consumers** (what reads it) and **edges** (what it
reads / is coupled to). And on a file nothing explains it REFUSES — *a file nothing explains
is a defect, not a mystery.* The refusal is half the value and it was built first: the
failing witness for this module is `tests/test_file_purpose_graph.py::
test_why_refuses_a_planted_unknown_file`, which was RED against a stub whose `why` answered
every path before this file existed.

SEVEN INPUTS, ONE GRAPH -- five joined in the A3 slice, two added by `[#664]` under ADR-118
section 1 (*"a new edge kind is added to FPG-1, never to a script"*). The repo already knows
most of this; it knows it in places that had never been joined:

  1. `ecosystem/doc-code-edge.yaml`   -- declaration docs and the `<!-- rule: -->` /
     `# rule:` pairs that bind a written rule to the organ enforcing it.
  2. `docs/audits/README.md`          -- the generated index, which is the only surface that
     enumerates the audit corpus.
  3. the `[#595]` consumer-at-landing citations -- BOTH directions: what an artifact declares
     as its consumer, and which governance surface cites the artifact back.
  4. `tasks/**` `depends-on`          -- the row graph. `tasks/` is the SOURCE OF TRUTH;
     `BACKLOG.md` is a generated one-line view and is never read for edges.
  5. `deploy/manifest-v*.yaml`        -- which carrier and which component ship which file.
  6. the WIRING SURFACES (`[#664]`)   -- `.pre-commit-config.yaml`, `.claude/settings.json`,
     the plugin `hooks.json`, the scheduled task and the CI workflows, plus the script call
     graph closed transitively over them by `ast`. Contributes `triggers` and `imports`.
     This is the relation whose ABSENCE was the whole finding: with nothing answering "what
     fires this", *"list all processes"* was a re-read of the repo, and
     `docs/audits/2026-09-08-technical-process-trigger-census.md` had to compute the relation
     privately to answer it once. Its method is carried here, recorded errors and all --
     see `_script_module_map` and `_import_targets`, which name the two the census records.
  7. `tasks/**` OPEN rows (`[#664]`)  -- `implements`, BOTH directions: the row names the
     file, and the file names the row. The code layer is where ownership is claimed, and it
     is exactly the layer the governance pool of input 3 deliberately excludes.

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

WHAT "GOVERNED" MEANS HERE -- AMENDED BY `[#664]`, because the amendment changes an answer
this header used to give. A path is governed iff at least one of the seven inputs names it,
PLUS one deliberate widening: every in-tree PROCESS file (`process_class` -- script / command
/ skill) is a node whether or not anything names it.

The widening is not a softening. Under the five original inputs a process nothing named had
NO VERTEX AT ALL, so the file most in need of a census was the one the census could not see:
`.claude/commands/save.md` and both `.claude/skills/*/SKILL.md` were invisible for exactly
that reason, measured on the first live run of the wiring loader. A query cannot report an
absence it has no node for.

So the refusal MOVED rather than weakened. `why` on an unexplained script now answers
(purpose, zero consumers) where it used to raise `UnknownFile`; the refusal it carried is now
`orphan_census`, which refuses at the COMMIT GATE and therefore blocks something. `tests/` is
still UNKNOWN and `why` still refuses it -- which remains the finding this header always
claimed it was, now stated about the surface where it is still true.

PHASE FENCE, LIFTED 2026-09-09 BY `[#664]`, and the old text is QUOTED rather than deleted
because lifting it is the point of the row. It read: *"this module is a library plus a CLI.
It is wired into NO gate, no check and no hook."* ADR-118 measured that sentence as the
defect -- a graph built to be authoritative and consumed by nothing, while twelve organs
computed edges privately. FPG-1 is now the DELIVERY SPINE: `scripts/graph_store.py` persists
it on every commit and `scripts/graph_queries.py` runs three commit-tier REFUSALS over the
persisted store. This module is still a library plus a CLI; what changed is that something
reads it.

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
import json
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree

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
from batch_manifest import links_artifact, manifest_link_surfaces  # noqa: E402
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
#: INPUT 6 -- the wiring surfaces, and the transitive script call graph closed over them.
#: Added by `[#664]` under ADR-118 §1 (*"a new edge kind is added to FPG-1, never to a
#: script"*), carrying the method of `docs/audits/2026-09-08-technical-process-trigger-census.md`
#: from a one-time audit into the graph.
INPUT_WIRING = "wiring"
#: INPUT 7 -- `implements`, both directions, between an OPEN row and the files it owns.
INPUT_TASK_IMPLEMENTS = "task-implements"
#: INPUT 8 -- `implements`, from a row to the DECISION it discharges (`[#692]`, A9-1).
#: Added to FPG-1 rather than computed in `decision_coverage.py`, which is ADR-118 §1
#: ("a new edge kind is added to FPG-1, never to a script") applied to a relation the corpus
#: did not hold: nothing in this repo could answer "what implements ADR-118".
INPUT_DECISION_IMPLEMENTS = "decision-implements"

#: The `detail` a manifest-link `consumed-by` edge carries, followed by the link kind
#: (`explicit` | `lane-slug`). Input 3's pool pass writes "governance citation"; the prefix is
#: what lets a reader select one route without a second pass over the corpus.
MANIFEST_LINK_DETAIL_PREFIX = "manifest link: "

INPUTS: tuple[str, ...] = (
    INPUT_DOC_CODE_EDGE,
    INPUT_AUDITS_INDEX,
    INPUT_CONSUMER_AT_LANDING,
    INPUT_TASKS_DEPENDS_ON,
    INPUT_DEPLOY_MANIFEST,
    INPUT_WIRING,
    INPUT_TASK_IMPLEMENTS,
    INPUT_DECISION_IMPLEMENTS,
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
EDGE_ARCHIVES = "archives"
#: `[#664]` -- the three kinds the delivery spine needs, all three registered HERE rather
#: than computed by an organ of their own. `triggers` runs from a WIRING SURFACE to the
#: process it fires, `imports` from a module to the module it calls, and `implements` from
#: an OPEN row to the file it owns. All three obey the one direction convention above.
EDGE_TRIGGERS = "triggers"
EDGE_IMPORTS = "imports"
EDGE_IMPLEMENTS = "implements"

#: kind -> (phrase when rendered on an OUT edge, phrase when rendered on an IN edge). Every
#: kind the builder emits is registered here; `test_every_edge_is_consumer_to_consumed`
#: refuses an unregistered one, because an unregistered kind renders as a bare token and
#: silently breaks the one direction convention this module's readability rests on.
EDGE_KINDS: dict[str, tuple[str, str]] = {
    EDGE_ENFORCES: ("enforces", "is enforced by"),
    EDGE_DECLARED_IN: ("is declared in", "declares"),
    EDGE_INDEXES: ("indexes", "is indexed by"),
    # "references", not "cites". Terra pre-merge finding 2 read `cites` through `[#595]`'s
    # phrase "an artifact declares its CONSUMER" and concluded the edge points backwards. It
    # does not -- but the word invited the reading. The fact this edge asserts is that the
    # artifact's own text REFERENCES this governance object, which is a coupling the artifact
    # owns and therefore an out-edge. The other fact -- that the object names the artifact
    # BACK -- is the separate `consumed-by` edge, and the two together are exactly `[#595]`'s
    # declaration leg and consumption leg. `test_cites_and_consumed_by_run_in_OPPOSITE
    # _directions` pins the pair so a reversal cannot pass as a rename.
    EDGE_CITES: ("references", "is referenced by"),
    EDGE_CONSUMED_BY: ("consumes", "is consumed by"),
    EDGE_DEPENDS_ON: ("depends on", "is depended on by"),
    EDGE_SHIPS: ("ships", "is shipped by"),
    EDGE_CARRIER_SOURCE: ("carries", "is carried by"),
    EDGE_CARRIED_BY: ("is carried by", "carries"),
    EDGE_GOVERNED_BY: ("is governed by", "governs"),
    EDGE_GENERATED_FROM: ("is generated from", "generates"),
    EDGE_ARCHIVES: ("archives its body in", "is the archived body of"),
    # `triggers` is the one relation the corpus had NO answer for, and its absence is what
    # made "list all processes" a re-read of the repo rather than a query. It runs from the
    # wiring surface to the process, because the surface is what depends on the process
    # existing -- delete the script and the hook breaks, not the other way round.
    EDGE_TRIGGERS: ("triggers", "is triggered by"),
    EDGE_IMPORTS: ("imports", "is imported by"),
    # `implements` runs from the ROW to the file. A row depends on the files that discharge
    # it; the file is the thing consumed. Reading it inward -- "is implemented by [#664]" --
    # is the coverage question `task_coverage` asks.
    EDGE_IMPLEMENTS: ("implements", "is implemented by"),
}

NODE_FILE = "file"
NODE_RULE = "rule"
NODE_TASK = "task"
NODE_ADR = "adr"
NODE_INTAKE = "intake"
NODE_CARRIER = "carrier"
NODE_COMPONENT = "component"
#: A transport ruling (`to-cc/AMEND-SESSION-PLAN-009.md`). It has NO PATH in this repo --
#: the transport is a machine-level surface (`CLAUDE_PROMPTS_DIR`), not a tracked tree -- so
#: it is keyed on the file STEM, which is how every row, contract and audit already cites one.
NODE_DECLARE = "declare"

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

# ------------------------------------------------------------------ [#664] the wiring input

#: THE SEVEN ROOTS, taken VERBATIM from the process-trigger census's Method section
#: (`docs/audits/2026-09-08-technical-process-trigger-census.md`) rather than re-decided here:
#: *"the seven wiring surfaces that can fire something without a human deciding in the
#: moment"*. Six are in-tree and listed; the seventh, `~/.claude/settings.json`, is the L0
#: layer on the operator's disk and is NOT a node of this repo's corpus. Its absence is
#: stated rather than silently dropped -- an L0 hook is out of a corpus graph's reach by
#: construction, and that is one half of why `orphan_census` cannot reach the census's 32.
#:
#: PROVISIONING WAS ADDED 2026-09-15 ([#554] lane aa-1), and it is an ENUM FIX discharging a
#: finding the register already carried in prose. `graph_queries.ORPHAN_DISPOSITIONS` held a row
#: for `scripts/provision_legs.py` saying, in as many words, that the file IS machine-triggered,
#: that `.devcontainer/provision.sh` is what triggers it, that *"the enum simply does not list
#: it"*, and that *"the underlying WIRING_SURFACES gap is a finding against the enum"*. That gap
#: is not academic: the same blind spot read `scripts/cloud_provisioning.py` as an unreferenced
#: orphan while six shell call sites named it, the deletion landed at `3c9418cc`, and on
#: 2026-09-14 a fresh codespace died into a recovery container ([#746]).
#:
#: IT SATISFIES THE CENSUS'S OWN PREDICATE, which is the whole argument for admitting it: a
#: container creation fires provisioning *"without a human deciding in the moment"*. Nothing
#: about the predicate was widened to let it in.
#:
#: WHAT IT DOES NOT DO, because the deferral rested on a guess about exactly this: it does not
#: make every `scripts/*.py` that any shell script names into a non-orphan. The admitted set is
#: this CLOSED TUPLE, not shell scripts as a class, and
#: `test_widening_the_enum_moves_only_the_provisioning_chain` measures which nodes changed side.
#: `ecosystem/harness.yaml` -- ADDED by LANE-5A-10 (2026-09-24), the SAME kind of admission as
#: provisioning above and for the same reason: it satisfies the census's own predicate
#: verbatim. A stage fires under the spine runner (`dodo.py`) and a moment fires under the
#: launcher, the Stop hook or the integrator command -- none of the six needs a human
#: deciding in the moment. Before this admission the file carried no trigger at all, so every
#: script a stage or moment names came back a false orphan; measured live, nine of the
#: census's orphans were exactly this (`docs/handoffs/.../DIGEST-HANDOFF-READINESS-2026-09-23
#: .md` §3: "orphan-census 5 -> 14 (9 are scripts harness.yaml DOES run)"). Parsed by a
#: DEDICATED reader, `_harness_command_targets`, never the generic leaf-walk the other six
#: surfaces use -- see that function's docstring for why the generic walk is the wrong tool
#: for this one file.
HARNESS_DECLARATION_RELPATH = "ecosystem/harness.yaml"

WIRING_SURFACES: tuple[str, ...] = (
    ".pre-commit-config.yaml",
    ".pre-commit-hooks.yaml",
    ".claude/settings.json",
    "plugins/tier1-lifecycle/hooks/hooks.json",
    "scripts/fleet-baseline.task.xml",
    ".devcontainer/devcontainer.json",
    ".devcontainer/provision.sh",
    HARNESS_DECLARATION_RELPATH,
)
#: The CI leg. The census records this as `push`-triggered, not scheduled; either way it
#: fires without a human deciding in the moment, which is the census's own predicate.
WIRING_WORKFLOW_GLOB = ".github/workflows/*.yml"

#: A repo-relative script path in a config VALUE. Bounded to the trees that hold executables,
#: so a doc path in an `args:` list cannot masquerade as a call site. `.devcontainer/*.sh` is
#: here because `devcontainer.json`'s three lifecycle commands name `provision.sh` in exactly
#: that position (`"onCreateCommand": "bash .devcontainer/provision.sh"`), and without it the
#: provisioning chain would be admitted at its second hop while its first hop stayed invisible —
#: half a chain in a graph is worse than none, because it reads as a complete answer.
_SCRIPT_PATH_RE = re.compile(
    r"(?:(?:scripts|plugins)/[A-Za-z0-9_./-]+\.(?:py|ps1)"
    r"|\.devcontainer/[A-Za-z0-9_.-]+\.sh)")
#: `python -m scripts.codemap.cli` -- the OTHER executable spelling in this repo's hooks.
_DASH_M_RE = re.compile(r"-m\s+(scripts(?:\.[A-Za-z0-9_]+)+)")

#: What counts as a PROCESS for the census. Derived from kind and path, never declared on a
#: node -- intake #40 §1's standing rule, and the reason `script` / `hook` / `command` /
#: `skill` are NOT minted as rival node kinds: a script IS a file, and a second vertex for
#: one file is the defect `PurposeGraph.node_for_path` exists to prevent.
PROCESS_SUFFIXES = (".py", ".ps1")


def process_class(relpath: str) -> str | None:
    """`script` / `command` / `skill` for a process file, else None.

    The census's populations A and C, as a predicate over a path. Population B (L0 hooks
    under `~/.claude/hooks/`) has no in-tree path and therefore no answer here; population D
    (`audit.ALL_CHECKS` members) is a set of FUNCTIONS inside files this already classifies,
    and the census reports it at zero orphans, so it needs no separate class.
    """
    rel = relpath.replace("\\", "/")
    if "__pycache__" in rel:
        return None
    if rel.endswith(PROCESS_SUFFIXES) and (
            rel.startswith("scripts/") or (rel.startswith("plugins/") and "/scripts/" in rel)):
        return "script"
    if rel.endswith(".md") and (
            rel.startswith(".claude/commands/") or
            (rel.startswith("plugins/") and "/commands/" in rel)):
        return "command"
    if rel.endswith("/SKILL.md") and (
            rel.startswith(".claude/skills/") or
            (rel.startswith("plugins/") and "/skills/" in rel)):
        return "skill"
    return None


#: Where a process file can live. Not a tree walk of the whole repo: the census's populations
#: A and C are exactly these four roots, and widening beyond them would report files this
#: repo has never called processes.
PROCESS_ROOTS = ("scripts", "plugins", ".claude/commands", ".claude/skills")


def _process_paths(root: Path) -> set[str]:
    """Every in-tree process file, by `process_class`. The census's population, computed."""
    out: set[str] = set()
    for base in PROCESS_ROOTS:
        directory = root / base
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if process_class(rel):
                out.add(rel)
    return out


def _config_strings(value) -> list[str]:
    """Every string leaf of a parsed config, and NOTHING a parser dropped.

    THE POINT OF PARSING RATHER THAN GREPPING. `.pre-commit-config.yaml` carries more
    comment prose than configuration, and that prose names scripts by path constantly
    (`block-ff-push below stays the push-time half`, and a dozen others). A text scan would
    read those as call sites and manufacture triggers -- which under-reports orphans, the
    exact direction an orphan census must never be wrong in. A YAML/JSON parser drops
    comments by construction, so the roots are what the file DECLARES rather than what it
    discusses.
    """
    out: list[str] = []
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            stack.extend(item.keys())
            stack.extend(item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend(item)
    return out


#: A line whose first non-blank content opens a `//` comment. `devcontainer.json` is JSONC, not
#: JSON — the spec allows comments and this repo's file is roughly three parts comment to one
#: part configuration — so `json.loads` raises on it and a fail-soft reader silently contributes
#: ZERO edges for the surface that fires every container creation. Full-line comments only: a
#: `//` inside a string value (a `documentationUrl`, and there is one) must survive, and the
#: parse still fail-softs if this is ever not enough.
_JSONC_COMMENT_LINE_RE = re.compile(r"^\s*//")


def _jsonc_strings(text: str) -> list[str]:
    return _config_strings(json.loads("\n".join(
        "" if _JSONC_COMMENT_LINE_RE.match(line) else line for line in text.splitlines())))


def _shell_tokens(text: str) -> list[str]:
    """A shell script's WORDS, with comments dropped — the same discipline the parsers give.

    WHY NOT A GREP, which is what every previous look at this problem reached for. The reason
    `_config_strings` parses instead of scanning applies here with more force, not less:
    `.devcontainer/provision.sh` is roughly half comment prose, and it names retired module
    paths ON PURPOSE as its own retirement record (`scripts/cloud_provisioning.py` appears in
    five comments). A text scan would read those as call sites and manufacture triggers —
    "which under-reports orphans, the exact direction an orphan census must never be wrong in".

    `shlex` is the stdlib's shell lexer and it drops `#` comments and respects quoting by
    construction, so the discipline is BORROWED rather than re-implemented (library-first).

    PER LINE, and the granularity is the point. Lexing the whole file would abort on the first
    unbalanced quote — an `awk '…'` program spanning lines, a heredoc carrying an apostrophe —
    and return an empty list, which is the silent-zero failure this function exists to avoid.
    A line that cannot be lexed costs that line and nothing else.
    """
    out: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        try:
            out.extend(lexer)
        except ValueError:
            continue
    return out


def _surface_strings(path: Path) -> list[str]:
    """Parse one wiring surface into its string leaves, fail-soft on an unparseable file."""
    text = _read(path)
    if text is None:
        return []
    suffix = path.suffix.lower()
    try:
        if suffix in (".yaml", ".yml"):
            return _config_strings(yaml.safe_load(text))
        if suffix == ".sh":
            return _shell_tokens(text)
        if suffix == ".json":
            return _jsonc_strings(text)
        if suffix == ".xml":
            root = ElementTree.fromstring(text)
            out: list[str] = []
            for element in root.iter():
                if element.text:
                    out.append(element.text)
                out.extend(str(v) for v in element.attrib.values())
            return out
    except (yaml.YAMLError, json.JSONDecodeError, ElementTree.ParseError):
        # An unparseable wiring surface makes every process it fires look like an orphan.
        # Reporting nothing is the honest failure here: the caller sees the surface
        # contributed no edges, and `INPUTS` coverage is asserted by a live-repo test.
        return []
    return []


def _script_module_map(root: Path) -> dict[str, str]:
    """Dotted module name -> repo-relative path, PACKAGE-QUALIFIED.

    The census's recorded error 2, not repeated: *"An AST pass keyed modules by bare
    filename. Seven names collide (`cli`, `check`, `generator`, `__init__`, and the three
    plugin derived copies), so `scripts/toc/generator.py` was credited with
    `scripts/codemap/`'s call site."* Every suffix of the dotted name is registered, and a
    suffix that TWO modules would claim is registered by NEITHER -- an ambiguous name buys
    no edge rather than the wrong one.
    """
    paths: list[str] = []
    for base in ("scripts", "plugins"):
        directory = root / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            rel = path.relative_to(root).as_posix()
            if "__pycache__" not in rel:
                paths.append(rel)

    claims: dict[str, set[str]] = {}
    for rel in paths:
        parts = rel[: -len(".py")].split("/")
        for start in range(len(parts)):
            claims.setdefault(".".join(parts[start:]), set()).add(rel)
    return {name: next(iter(owners)) for name, owners in claims.items() if len(owners) == 1}


#: A bare sibling module named as a string, the third executable spelling in this repo:
#: `audit.py` loads its git seam with `Path(__file__).resolve().with_name("gitenv.py")`, and
#: the census counts exactly that -- *"a string literal naming `<mod>.py` in executable
#: position"*. Resolved against the NAMING file's own directory, never repo-wide, so a bare
#: name cannot bind to a same-named module in another package.
_BARE_MODULE_RE = re.compile(r"\A([A-Za-z_][A-Za-z0-9_]*)\.py\Z")


def _resolved_targets(text: str, modules: dict[str, str], root: Path,
                      bases: tuple[str, ...] = (), exact_only: bool = False) -> set[str]:
    """The script paths one config or code string names, by any of the three spellings.

    `bases` are the directories a RELATIVE spelling may resolve against, NEAREST FIRST, with
    the repo root tried LAST. A plugin manifest writes
    `${CLAUDE_PLUGIN_ROOT}/scripts/propose_closures.py`, and the ORDER is what makes that
    resolve correctly: `scripts/propose_closures.py` also exists at the repo root -- it is
    the hub original the plugin copy is derived from -- so a root-first search bound the
    plugin's Stop hook to the WRONG FILE and left all three plugin scripts reading as
    orphans while the hook that fires them looked wired. Measured on the first live run.
    A config names paths relative to itself before it names them relative to the repo.
    """
    found: set[str] = set()
    if exact_only and not _SCRIPT_PATH_RE.fullmatch(text.strip()):
        # EXECUTABLE POSITION, and this clause is the census's recorded error 1 arriving in
        # a NEW DRESS -- caught by this lane's own measurement disagreeing with the census.
        # `graph_queries.ORPHAN_DISPOSITIONS` is a dict whose KEYS are exact process paths.
        # Read as call sites, they made the register that RECORDS "this has no trigger"
        # MANUFACTURE one for every row in it: 25 dispositioned scripts came back triggered,
        # and the census's own 20 silently reported clean. A register that launders its own
        # subject is worse than no register.
        #
        # So a code string counts only when BOTH hold: it sits inside a `Call` (the caller
        # passes `exact_only` there and nowhere else), AND it is EXACTLY a path rather than
        # prose containing one. A dict key is not in a call; a `reason="... scripts/x.py
        # ..."` sentence is in a call but is not exactly a path. Both are excluded, and
        # `Path(__file__).with_name("gitenv.py")` -- a real load, in a call, exactly a name
        # -- still counts. Config surfaces are unaffected: an `entry:` line embeds its path
        # in a command line by construction, so they pass `exact_only=False`.
        return _bare_module_target(text, root, bases)
    for match in _SCRIPT_PATH_RE.findall(text):
        for base in bases + ("",):
            candidate = f"{base}/{match}" if base else match
            if (root / candidate).is_file():
                found.add(candidate)
                break
    for match in _DASH_M_RE.findall(text):
        target = modules.get(match)
        if target:
            found.add(target)
            found.update(_package_inits(match, modules))
    found |= _bare_module_target(text, root, bases)
    return found


def _bare_module_target(text: str, root: Path, bases: tuple[str, ...]) -> set[str]:
    """`"gitenv.py"` -- a sibling module named as a bare filename, resolved against the
    NAMING file's own directory and never repo-wide, so a bare name cannot bind to a
    same-named module in another package."""
    bare = _BARE_MODULE_RE.match(text.strip())
    if not bare:
        return set()
    for base in bases:
        candidate = f"{base}/{bare.group(1)}.py" if base else f"{bare.group(1)}.py"
        if (root / candidate).is_file():
            return {candidate}
    return set()


def _ancestor_bases(relpath: str) -> tuple[str, ...]:
    """The directories `relpath` sits under, NEAREST FIRST, repo root last (as `""`)."""
    parts = relpath.split("/")[:-1]
    return tuple("/".join(parts[:stop]) for stop in range(len(parts), 0, -1))


def _package_inits(dotted: str, modules: dict[str, str]) -> set[str]:
    """Every `__init__.py` an import of `dotted` also executes.

    Without this a package marker is an orphan by an accident of the resolver: nothing
    names `scripts/toc/__init__.py`, yet importing `scripts.toc.generator` runs it. The
    edge is real, so the graph carries it rather than the register apologising for it.
    """
    out: set[str] = set()
    parts = dotted.split(".")
    for stop in range(1, len(parts)):
        target = modules.get(".".join(parts[:stop] + ["__init__"]))
        if target:
            out.add(target)
    return out


def _relative_module(relpath: str, level: int, module: str | None) -> str | None:
    """`from ._common import Finding`, resolved against the importing module's package.

    A RELATIVE import is the single largest class this pass can miss, and missing it is not
    a thinner graph -- it is a WRONG one. `scripts/audit_checks/` reaches its twenty-three
    check modules entirely through `from .check_x import ...`, and `scripts/codemap/cli.py`
    reaches its five the same way, so skipping level>0 imports reported twenty-eight live,
    commit-gate-firing modules as orphans on the first live run of this loader. Measured,
    fixed, and pinned by a test -- an orphan census that over-reports is worse than none,
    because every false orphan is an invitation to retire something load-bearing.
    """
    parts = relpath[: -len(".py")].split("/")[:-1]   # the importing module's package path
    if level > len(parts):
        return None
    base = parts[: len(parts) - (level - 1)] if level > 1 else parts
    return ".".join(base + ([module] if module else []))


def _import_targets(path: Path, root: Path, modules: dict[str, str]) -> set[str]:
    """Call-site edges out of one module -- `ast`, with DOCSTRINGS EXCLUDED.

    The census's recorded error 1, not repeated: *"A regex pass counted any docstring
    mention as a call site. `audit.py`'s docstrings name nearly every module in the repo, so
    133 of 139 scripts came back 'triggered'. A prose mention is the opposite of a
    trigger."* So a string constant counts only when it is NOT the docstring of its module,
    class or function -- which is the same distinction, made structurally.
    """
    text = _read(path)
    if text is None:
        return set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()

    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docstrings.add(id(body[0].value))

    rel = path.relative_to(root).as_posix()
    bases = _ancestor_bases(rel)
    found: set[str] = set()

    def visit(node: ast.AST, in_call: bool) -> None:
        if isinstance(node, ast.Import):
            for alias in node.names:
                target = modules.get(alias.name)
                if target:
                    found.add(target)
                    found.update(_package_inits(alias.name, modules))
        elif isinstance(node, ast.ImportFrom):
            dotted = (_relative_module(rel, node.level, node.module) if node.level
                      else node.module)
            if dotted:
                target = modules.get(dotted)
                if target:
                    found.add(target)
                    found.update(_package_inits(dotted, modules))
                for alias in node.names:
                    sub = modules.get(f"{dotted}.{alias.name}")
                    if sub:
                        found.add(sub)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and in_call and id(node) not in docstrings:
            found.update(_resolved_targets(node.value, modules, root, bases,
                                           exact_only=True))
        for child in ast.iter_child_nodes(node):
            visit(child, in_call or isinstance(node, ast.Call))

    visit(tree, False)
    return found


def _harness_command_targets(text: str, modules: dict[str, str], root: Path,
                             bases: tuple[str, ...]) -> set[str]:
    """The scripts `ecosystem/harness.yaml`'s stages and moment organs actually RUN.

    A DEDICATED reader, not the generic `_surface_strings` leaf-walk every other wiring
    surface uses. This file also carries a `fates:` section whose entire point is to record
    scripts the loop does NOT yet run -- a `path:` key plus prose `reason:` text that names
    still more scripts by path (e.g. "called by lanes at handback; a moment declaration is
    owed by the next wave"). A leaf-walk would read every one of those as a call site and
    manufacture a `triggers` edge for exactly the scripts the census must keep reporting as
    orphans -- the over-triggering `_config_strings`'s own docstring warns against, in a new
    dress. So only `stages[].command` and `moments[].organs[].command` are read; `fates` is
    never touched. `command: null` (a stage not built yet) contributes nothing, the same rule
    `graph_queries.load_declaration` applies reading the same file for the moments query.
    """
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError:
        return set()
    if not isinstance(raw, dict):
        return set()
    commands: list = []
    for stage in raw.get("stages") or []:
        if isinstance(stage, dict) and isinstance(stage.get("command"), list):
            commands.append(stage["command"])
    for moment in raw.get("moments") or []:
        if not isinstance(moment, dict):
            continue
        for organ in moment.get("organs") or []:
            if isinstance(organ, dict) and isinstance(organ.get("command"), list):
                commands.append(organ["command"])
    found: set[str] = set()
    for command in commands:
        for arg in command:
            if isinstance(arg, str):
                found |= _resolved_targets(arg, modules, root, bases)
    return found


def wiring_targets(root: Path) -> dict[str, set[str]]:
    """`{wiring surface: the repo files it names in executable position}`.

    LIFTED OUT OF `_load_wiring` SO IT HAS EXACTLY ONE DEFINITION. `safe_remove` needs the same
    relation to refuse retiring a file a wiring surface calls, and a second implementation there
    would be a private edge computation racing FPG-1 — ADR-118's first anti-pattern, and the
    one `graph_queries.edge_class_census` blocks commits over. A consumer reads this; nobody
    recomputes it.
    """
    modules = _script_module_map(root)
    surfaces = [root / rel for rel in WIRING_SURFACES]
    workflows = sorted(root.glob(WIRING_WORKFLOW_GLOB))
    out: dict[str, set[str]] = {}
    for path in surfaces + workflows:
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        bases = _ancestor_bases(rel)
        targets: set[str] = set()
        if rel == HARNESS_DECLARATION_RELPATH:
            text = _read(path)
            if text is not None:
                targets |= _harness_command_targets(text, modules, root, bases)
        else:
            for value in _surface_strings(path):
                targets |= _resolved_targets(value, modules, root, bases)
        targets.discard(rel)                     # a surface naming itself is not a call site
        if targets:
            out[rel] = targets
    return out


def _load_wiring(graph: PurposeGraph, root: Path) -> None:
    """INPUT 6 -- `triggers` from a wiring surface, `imports` along the script call graph.

    WHY THIS BELONGS ON FPG-1 AND NOT IN AN ORGAN. ADR-118 §1 rules that a new edge kind is
    added to the graph, never to a script, and this is the edge kind whose ABSENCE was the
    whole finding: with no `triggers` relation, *"list all processes"* was answered by
    re-reading the repo, and the process-trigger census had to compute the relation privately
    to answer it once. Moving the computation here is that census's method becoming a
    standing query -- intake #86's *"this replaces the REPETITION of that pass, not the pass
    itself."*
    """
    modules = _script_module_map(root)

    # EVERY PROCESS FILE BECOMES A NODE, whether or not another input names it -- and this is
    # a deliberate widening of what "governed" means, recorded rather than slipped in. Under
    # the five original inputs a process nothing named had NO VERTEX AT ALL, so the file most
    # in need of a census was the one the census could not see: `.claude/commands/save.md` and
    # both `.claude/skills/*/SKILL.md` were invisible on the first live run for exactly that
    # reason. A query cannot report an absence it has no node for.
    #
    # WHAT THIS COSTS, stated plainly: `why` on an unexplained script now ANSWERS (purpose,
    # zero consumers) where it used to REFUSE. The refusal is not lost, it MOVES -- from a
    # per-file `UnknownFile` in a read-only CLI to `orphan_census`, which refuses at the
    # commit gate and therefore actually blocks something. The module header's "most of
    # `scripts/` is UNKNOWN to this graph" is updated there rather than left to rot.
    for rel in sorted(_process_paths(root)):
        graph.node_for_path(rel)

    for rel, targets in sorted(wiring_targets(root).items()):
        source_key = graph.node_for_path(rel)
        for target in sorted(targets):
            graph.add_edge(Edge(source_key, graph.node_for_path(target), EDGE_TRIGGERS,
                                INPUT_WIRING, f"named by {rel}"))

    for rel in sorted(set(modules.values())):
        path = root / rel
        if not path.is_file():
            continue
        source_key = graph.node_for_path(rel)
        for target in sorted(_import_targets(path, root, modules)):
            if target != rel:
                graph.add_edge(Edge(source_key, graph.node_for_path(target), EDGE_IMPORTS,
                                    INPUT_WIRING, "import or call-site string"))


# ------------------------------------------------------- [#664] the task-implements input

#: WHERE AN OWNERSHIP CLAIM CAN BE WRITTEN -- which is nearly the whole tree, and the two
#: absences are the informative ones. `JOURNAL.md` and `BACKLOG.md` are excluded by being
#: root files rather than by a rule: a journal entry names every row a session touched, so
#: reading it as an ownership claim would make every file any session mentioned "covered",
#: and `BACKLOG.md` is a generated VIEW of `tasks/` and is never read for an edge (input 4's
#: rule, applied here too). Measured cost of the widening from the four code roots to these
#: nine: 2668 files walked, leg 2 rising 1.2 s -> 3.6 s. Bought because `docs/` is where most
#: of this repo's change lands, and a coverage gate blind to it would pass by not looking.
#:
#: ADR-118 names the code layer as FPG-1's measured hole (*"the code layer is thin -- 21
#: nodes"*); leg 2 is the input that fills it.
IMPLEMENTS_SCAN_DIRS = ("scripts", "tests", ".claude", "plugins",
                        "docs", "protocols", "templates", "ecosystem", "deploy")
#: Never descend into these. `.claude/worktrees/` holds FULL CHECKOUTS of this repo -- a
#: parallel lane's tree -- so walking it would read another lane's files as if they were
#: this one's, at a cost of one whole corpus per live worktree.
IMPLEMENTS_SKIP_DIRS = frozenset({"__pycache__", "worktrees", ".venv", "node_modules"})
#: A file this size is not a module claiming a row; reading it is cost with no answer in it.
IMPLEMENTS_MAX_BYTES = 512 * 1024
#: `_TASK_ID_RE`'s byte twin, kept beside it so a change to one is visibly owed by the other.
_TASK_ID_BYTES_RE = re.compile(rb"\[#(\d+)\]")
#: A repo-relative path token in a row body. Existence on disk is the filter -- an
#: unresolvable token is `validate_backlog`'s finding, not an invented node (`_load_tasks`'s
#: own rule, applied to paths instead of ids).
_REL_PATH_RE = re.compile(
    r"(?:^|[\s`'\"(\[])((?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6})")


def _open_task_ids(root: Path) -> dict[str, Path]:
    """`{task id: row path}` for OPEN rows only.

    AT OPEN AND NOT ONLY AT CLOSE -- `[#664]`'s own words for what `task_coverage` must
    mean. A closed row confers no coverage, so its paths contribute no edge and a file whose
    only claimant is done reads as uncovered, which is the true answer.
    """
    tasks_dir = root / TASKS_RELPATH
    out: dict[str, Path] = {}
    if not tasks_dir.is_dir():
        return out
    for path in sorted(tasks_dir.glob("*.md")):
        text = _read(path)
        if text is None:
            continue
        frontmatter = _frontmatter(text)
        if str(frontmatter.get("status", "")).strip().lower() != "open":
            continue
        match = _TASK_ID_RE.search(str(frontmatter.get("id", ""))) or re.match(r"^(\d+)-", path.name)
        if match:
            out[match.group(1)] = path
    return out


#: Root files are scanned too -- `.pre-commit-config.yaml` names the row whose hooks it
#: carries, and `CLAUDE.md` / `ARCHITECTURE.md` name the rows that changed them. NOT a
#: `rglob` at the root: that would descend into `.git`, `.venv` and `.claude/worktrees`
#: (a full second checkout per live lane). Top level only, by suffix.
IMPLEMENTS_ROOT_SUFFIXES = (".md", ".yaml", ".yml", ".toml", ".json", ".cfg")
#: Excluded from the ROOT sweep, each for a stated reason rather than by omission.
#: `JOURNAL.md` names every row a session touched, so reading it as an ownership claim would
#: make every file any session mentioned "covered"; `BACKLOG.md` is a generated view of
#: `tasks/` and input 4's rule is that a view is never read for an edge.
IMPLEMENTS_ROOT_EXCLUDE = frozenset({"JOURNAL.md", "BACKLOG.md"})


def _implements_scan_paths(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.glob("*")):
        if (path.is_file() and path.suffix in IMPLEMENTS_ROOT_SUFFIXES
                and path.name not in IMPLEMENTS_ROOT_EXCLUDE):
            try:
                if path.stat().st_size <= IMPLEMENTS_MAX_BYTES:
                    out.append(path)
            except OSError:
                pass
    for base in IMPLEMENTS_SCAN_DIRS:
        directory = root / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            if IMPLEMENTS_SKIP_DIRS & set(path.relative_to(root).parts):
                continue
            try:
                if path.stat().st_size > IMPLEMENTS_MAX_BYTES:
                    continue
            except OSError:
                continue
            out.append(path)
    return out


def _load_task_implements(graph: PurposeGraph, root: Path) -> None:
    """INPUT 7 -- `implements`, BOTH DIRECTIONS, between an OPEN row and the files it owns.

    TWO LEGS, because ownership is asserted from two ends and both assertions are real.

      * **Leg 1 -- the row names the file.** `[#664]` names `scripts/file_purpose_graph.py`,
        so the row claims it.
      * **Leg 2 -- the file names the row.** Every module in this repo already opens with the
        `[#id]` it was built for; that docstring is a claim of ownership, not an incidental
        mention. The edge is therefore computed from a convention that EXISTS rather than
        imposed as a new one a lane would have to be told about.

    Leg 2 is scoped to `IMPLEMENTS_SCAN_DIRS` rather than the whole tree, and the scope is
    the governance pool's exclusions read forwards: `consumer_at_landing` excludes `scripts/`
    and `tests/` because *"a mention in a session log or a machine baseline is a record that
    the file existed, not evidence that anything consumes it"* -- true for CONSUMPTION, and
    the exact opposite for OWNERSHIP, where the code layer is where the claim lives.
    """
    open_tasks = _open_task_ids(root)
    if not open_tasks:
        return

    for task_id, row_path in sorted(open_tasks.items()):
        text = _read(row_path) or ""
        task_key = _task_key(task_id)
        if graph.node(task_key) is None:
            graph.add_node(Node(NODE_TASK, task_key, f"[#{task_id}]",
                                row_path.relative_to(root).as_posix()))
        for candidate in sorted(set(_REL_PATH_RE.findall(text))):
            rel = candidate.removeprefix("./")
            if rel and (root / rel).is_file():
                graph.add_edge(Edge(task_key, graph.node_for_path(rel), EDGE_IMPLEMENTS,
                                    INPUT_TASK_IMPLEMENTS, "named by the row body"))

    # BYTES, NOT TEXT, and it is a measurement rather than a preference: leg 2 sweeps ~2.7k
    # files totalling ~42 MiB, and decoding all of that to look for an ASCII token cost ~1.5 s
    # of the pass for no answer it changed. `[#664]` is `[#664]` in every encoding this
    # corpus uses, and a byte scan additionally cannot raise `UnicodeDecodeError` on a file
    # that is not text -- so the sweep degrades to "no claim found" rather than to a
    # traceback inside a commit hook.
    for path in _implements_scan_paths(root):
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        claimed = {tid.decode() for tid in _TASK_ID_BYTES_RE.findall(blob)} & set(open_tasks)
        if not claimed:
            continue
        rel = path.relative_to(root).as_posix()
        file_key = graph.node_for_path(rel)
        for task_id in sorted(claimed):
            graph.add_edge(Edge(_task_key(task_id), file_key, EDGE_IMPLEMENTS,
                                INPUT_TASK_IMPLEMENTS, "the file names the row"))


# --------------------------------------------------- [#692] the decision-implements input

#: The `implements:` frontmatter value, split into tokens. The key is DERIVED from the row
#: body's `· implements: …` clause (`gen_task_tree.derive_implements`), so reading the
#: frontmatter here reads the body's claim -- there is no second authority.
#: The grammar is `validate_backlog._IMPLEMENTS_TOKEN_RE`'s, and it is DUPLICATED NOWHERE:
#: that module owns validation, this one owns the join, and both read the same three forms
#: clause 2 names -- `ADR-n`, `intake-n`, `DECLARE-…`/`AMEND-…`.
_DECISION_TOKEN_RE = re.compile(
    r"\bADR-(?P<adr>\d+)(?![0-9])"
    r"|\bintake-(?P<intake>\d+)(?![0-9])"
    r"|\b(?P<declare>(?:DECLARE|AMEND)-[A-Za-z0-9][A-Za-z0-9-]*)")

#: What an input-8 edge carries in `detail`: the IMPLEMENTING ROW's own status, verbatim.
#: Held here rather than in the consumer so the writer and the reader cannot drift -- a
#: second literal in `decision_coverage.py` would be free to disagree with this one.
DECISION_DETAIL_PREFIX = "row status: "


def decision_key(token: str) -> str | None:
    """The graph key a `implements:` token names, or None when the token is not one.

    `ADR-118` -> `adr:118`, `intake-91` -> `intake:91`, `AMEND-SESSION-PLAN-009` ->
    `declare:AMEND-SESSION-PLAN-009`. The ADR and intake keys are the ones `_governance_node`
    already mints, deliberately: an ADR cited by an audit and an ADR implemented by a row must
    meet at ONE vertex, which is the identity-before-adjacency rule this module learned the
    hard way at input 4.
    """
    match = _DECISION_TOKEN_RE.fullmatch(token.strip())
    if match is None:
        return None
    if match.group("adr"):
        return f"{NODE_ADR}:{match.group('adr')}"
    if match.group("intake"):
        return f"{NODE_INTAKE}:{match.group('intake')}"
    return f"{NODE_DECLARE}:{match.group('declare')}"


def _decision_node(graph: PurposeGraph, key: str) -> str:
    kind, _, value = key.partition(":")
    if kind == NODE_ADR:
        return graph.add_node(Node(NODE_ADR, key, f"ADR-{value}"))
    if kind == NODE_INTAKE:
        return graph.add_node(Node(NODE_INTAKE, key, f"intake #{value}"))
    return graph.add_node(Node(NODE_DECLARE, key, value))


def _load_decision_implements(graph: PurposeGraph, root: Path) -> None:
    """INPUT 8 -- `implements`, from a ROW to the DECISION it discharges.

    ONE DIRECTION ONLY, and the asymmetry with input 7 is the point. Input 7 reads BOTH ends
    because a module's docstring naming `[#664]` is a real ownership claim that already exists
    in this corpus. No such convention exists on the other side here: an ADR that mentions
    `[#692]` in its Related line is CITING the row, not being implemented by it, and reading
    that as coverage would let any decision discharge itself by naming a row in passing. So the
    claim must be made by the row, in one declared key, and nowhere else.

    EVERY ROW, OPEN OR CLOSED -- again unlike input 7, and again deliberately. Input 7 asks
    "is this file owned by live work", so a closed row confers nothing. This input answers a
    different question: a decision implemented only by CLOSED rows is DONE, and dropping those
    edges would make it indistinguishable from a decision nobody ever scheduled. The row's own
    status rides on the edge (`DECISION_DETAIL_PREFIX`) so the consumer can tell the two apart
    with one SELECT rather than a second pass over `tasks/`.
    """
    tasks_dir = root / TASKS_RELPATH
    if not tasks_dir.is_dir():
        return
    for path in sorted(tasks_dir.glob("*.md")):
        text = _read(path)
        if text is None:
            continue
        frontmatter = _frontmatter(text)
        raw = str(frontmatter.get("implements", "")).strip()
        if not raw:
            continue
        match = _TASK_ID_RE.search(str(frontmatter.get("id", ""))) or re.match(r"^(\d+)-", path.name)
        if not match:
            continue
        task_key = _task_key(match.group(1))
        if graph.node(task_key) is None:
            graph.add_node(Node(NODE_TASK, task_key, f"[#{match.group(1)}]",
                                path.relative_to(root).as_posix()))
        status = str(frontmatter.get("status", "")).strip().lower() or "unknown"
        for token in (part.strip() for part in raw.split(",")):
            key = decision_key(token) if token else None
            if key is None:
                # A malformed token is `validate_backlog`'s HARD FAIL, not an invented node --
                # `_load_tasks`'s own rule for a dangling id, applied to a dangling decision.
                continue
            graph.add_edge(Edge(task_key, _decision_node(graph, key), EDGE_IMPLEMENTS,
                                INPUT_DECISION_IMPLEMENTS, f"{DECISION_DETAIL_PREFIX}{status}"))


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

    def node_for_path(self, relpath: str) -> str:
        """The node key for a path, REUSING an existing one rather than minting a rival.

        Terra pre-merge finding 5. A `tasks/NNN-*.md` path already owns the identity-keyed
        node `task:NNN`; a later loader that reached for `_file_node()` unconditionally would
        add a second vertex for the same file, and `_by_path.setdefault` would then leave
        `why` answering from the first while the new edges hung off the second. One file, two
        vertices, no error -- the same failure the pass ORDER in `build()` exists to prevent,
        reachable by a different route. This is the single funnel both routes now go through.
        """
        return self.key_for_path(relpath) or self.add_node(_file_node(relpath))

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
    # identifier -> the SET of artifacts carrying it, never a single winner. Terra pre-merge
    # finding 6: the corpus is recursive and keyed on BASENAME, so two artifacts at different
    # depths can share one identifier -- a limit `consumer_at_landing` records for itself
    # ("none does today, but that is a property of the keying rather than a proof"). Assigning
    # into a `dict[str, str]` made the last-sorted path win SILENTLY, which would move a real
    # consumption edge onto the wrong file rather than reporting a collision. A set edges to
    # both: an ambiguous citation becomes visible in the answer instead of being resolved by
    # sort order.
    by_identifier: dict[str, set[str]] = {}

    def _claim(token: str, rel: str) -> None:
        by_identifier.setdefault(token, set()).add(rel)

    for path in _audit_paths(root):
        rel = path.relative_to(root).as_posix()
        graph.add_node(_file_node(rel))
        for token in identifiers(path.name):
            _claim(token, rel)
        match = _COMMISSION_ID_RE.search(path.name)
        if match:
            _claim(match.group(1), rel)

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
        hits: set[str] = set()
        for token in named:
            hits |= by_identifier.get(token, set())
        if not hits:
            continue
        src = graph.node_for_path(rel)
        for target in sorted(hits):
            graph.add_edge(Edge(src, _file_key(target), EDGE_CONSUMED_BY,
                                INPUT_CONSUMER_AT_LANDING, "governance citation"))

    # -- the manifest-link route, the half of `consumer_at_landing` this input used to omit.
    # `consumer_at_landing.measure` counts an artifact a batch manifest (or its `closed_by:`
    # packet) links as CONSUMED (operator ruling 2026-09-05), and until `[#664]` lane
    # `ab-664-spine-witnessed` FPG-1 copied only the pool pass -- so the register row calling
    # this input "reconciled" was true of one leg of two. The parser is IMPORTED
    # (`batch_manifest.manifest_link_surfaces`), never re-derived, and each link is an edge FROM
    # the surface that wrote it, with the link kind on the edge.
    audits = _audit_paths(root)
    for surface_rel, links in manifest_link_surfaces(root).items():
        src = graph.node_for_path(surface_rel)
        for path in audits:
            kind = links_artifact(links, path.name)
            if kind is None:
                continue
            graph.add_edge(Edge(src, _file_key(path.relative_to(root).as_posix()),
                                EDGE_CONSUMED_BY, INPUT_CONSUMER_AT_LANDING,
                                f"{MANIFEST_LINK_DETAIL_PREFIX}{kind}"))


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

    # `tasks/archive/NNN.md` -- the row-body archival records. `glob("*.md")` above is the
    # right scope for ROWS (an archive record is not a row: it carries `row:`/`record:`
    # frontmatter, no `title` and no `status`), but the archive file IS explained, by the row
    # whose annotations it holds, and its own frontmatter says which one. Reading it here
    # removes a FALSE-REFUSAL class measured at 14 live files -- and a refusal that fires on a
    # file a row names by path is the worst failure this module can have, because the refusal
    # is the half of the deliverable that has to be trustworthy. Terra pre-merge finding 4
    # reached the same place from the other direction (a non-recursive scan of a `**` input).
    archive_dir = tasks_dir / "archive"
    if archive_dir.is_dir():
        for path in sorted(archive_dir.glob("*.md")):
            text = _read(path)
            if text is None:
                continue
            frontmatter = _frontmatter(text)
            match = _TASK_ID_RE.search(str(frontmatter.get("id", "")))
            if not match or graph.node(_task_key(match.group(1))) is None:
                continue
            rel = path.relative_to(root).as_posix()
            graph.add_node(_file_node(rel))
            graph.add_edge(Edge(_task_key(match.group(1)), _file_key(rel), EDGE_ARCHIVES,
                                INPUT_TASKS_DEPENDS_ON, "row-body archival record"))

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


def _carrier_source_paths(target) -> list[str]:
    """Every hub file a carrier's `target:` block names, across ALL THREE shapes it uses.

    Terra pre-merge finding 3, and it was a real omission rather than a hypothetical: reading
    only `source_path` silently dropped the live `editor-config` carrier (which uses
    `source_paths:`, a bare list) and the whole `docs` carrier (which uses `doc_paths:`, a
    list of `{source, path}` pairs whose `source` is the hub side). A loader that recognises
    one of three declared shapes does not report a thin graph, it reports a wrong one.

    A `~`-rooted target is skipped everywhere: that is a USER-machine path (`~/.codex/...`),
    not a file in this repo's space, and minting a node for it would fabricate a local file.
    """
    if not isinstance(target, dict):
        return []
    out: list[str] = []

    def _push(value) -> None:
        rel = str(value).strip()
        if rel and not rel.startswith("~") and rel not in out:
            out.append(rel)

    if target.get("source_path"):
        _push(target["source_path"])
    for item in target.get("source_paths") or []:
        _push(item)
    for pair in target.get("doc_paths") or []:
        if isinstance(pair, dict) and pair.get("source"):
            _push(pair["source"])
    return out


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
        for rel in _carrier_source_paths(carrier.get("target")):
            dst = graph.node_for_path(rel)
            graph.add_edge(Edge(key, dst, EDGE_CARRIER_SOURCE,
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
            graph.add_edge(Edge(key, graph.node_for_path(rel), EDGE_SHIPS,
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
    # `[#664]`, and the ORDER RULE above still binds: both new passes mint FILE nodes for
    # paths the earlier passes may already own as identity-keyed nodes, so both go through
    # `node_for_path` and both run LAST, after every identity-bearing loader has claimed
    # its keys. Identity before adjacency -- the same lesson, honoured rather than relearnt.
    _load_wiring(graph, root)
    _load_task_implements(graph, root)
    # INPUT 8 (`[#692]`) rides at the end for the ORDER RULE above: it mints decision
    # vertices `_load_consumer_at_landing` may already own by the same keys, so it must run
    # after every identity-bearing loader has claimed them.
    _load_decision_implements(graph, root)
    return graph


def _normalise(repo_root: Path, path: str) -> str:
    """A caller's path spelling -> the repo-relative posix key the graph is indexed on.

    `removeprefix("./")`, NOT `lstrip("./")`. `lstrip` takes a character SET, so it eats every
    leading `.` and `/`: `.vscode/settings.json` became `vscode/settings.json` and `why`
    refused three files the live manifest genuinely governs (`.vscode/settings.json`,
    `.vscode/extensions.json`, `.claude/commands/override.md`). Terra pre-merge finding 1, and
    the exact class this repo already records as "probe tokenizer strips leading dot".
    """
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(repo_root).as_posix()
        except ValueError:
            return candidate.as_posix()
    return candidate.as_posix().removeprefix("./")


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


def list_nodes(graph: PurposeGraph) -> list[tuple[str, str, int, int]]:
    """Every node as (path-or-key, purpose, edge count, consumer count), in ONE pass.

    Shares `_purpose_of` with `why` and counts edges the way `why` lists them (out-edges =
    `edges`, in-edges = `consumers`), so a row here always agrees with `why <path>`. It exists
    because answering "what is every file for" by looping `why` per file costs a build per call.
    """
    rows = []
    for idx in graph.graph.node_indices():
        node = graph.graph[idx]
        purpose = " ".join(_purpose_of(graph.repo_root, node).split())
        # The machine-readable dump names the absence with the token, not `why`'s prose form.
        if not purpose or purpose == NO_STATED_PURPOSE:
            purpose = "NO_STATED_PURPOSE"
        rows.append((node.path or node.key, purpose,
                     graph.graph.out_degree(idx), graph.graph.in_degree(idx)))
    return sorted(rows)


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
    sub.add_parser("list", parents=[common],
                   help="every node: path, purpose, edge count, consumer count (tab-separated)")

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

    if args.command == "list":
        print("path	purpose	edges	consumers")
        for path, purpose, edges, consumers in list_nodes(graph):
            print(f"{path}	{purpose}	{edges}	{consumers}")
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
