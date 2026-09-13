#!/usr/bin/env python
"""gen_task_tree.py -- [#433] STEP 1-2 (split) / [#439] STEP 3 (the flip).

THE DERIVATION RUNS TREE -> FILE. `tasks/` is the SOURCE OF TRUTH; `BACKLOG.md`
is GENERATED from it. That direction was flipped by [#439] on 2026-07-28 under
ADR-107 §7.2, once both of its preconditions held (the ADR Accepted, and the
tasks/ coherence gate armed and witnessed firing). Before the flip the arrow
pointed the other way, and most of this module's history assumes that; read
`--write` in particular with the flip in mind (see below).

The source of truth is TWO artifacts, and both are load-bearing:
  * `tasks/<id>-<slug>.md` -- one frontmattered file per task. The BODY is the
    task's own BACKLOG line, verbatim, and is the authoritative text. The
    FRONTMATTER is DERIVED FROM THAT BODY (id/title/status/priority/... are all
    parsed out of the line), so editing frontmatter changes nothing on its own --
    `find_incoherences` REFUSES a file whose frontmatter disagrees with what its
    own body derives, precisely so that inert-looking metadata cannot rot into a
    quiet lie. Edit the body; the frontmatter follows.
  * `tasks/manifest.json` -- the residue carrier: every non-task prose line of
    BACKLOG.md, in order, interleaved with task-node pointers. It carries the
    document's STRUCTURE, so ordering, headings and narrative live here. This is
    what makes one-file->many-files reversible (ADR-107 §5 finding 6).

`BACKLOG.md` is NOT decommissioned by the flip (ADR-107 "Decommission: none").
It stays on disk, and every other gate that reads it -- doc_rot, validate_backlog,
the commit-msg hooks, propose_closures -- keeps working against it. What changed at
the flip is only which side of the pair is the expectation and which is the output.

WHAT [#589] CHANGED, ON TOP OF THAT FLIP, AND WHY IT IS NOT THE SAME KIND OF CHANGE.
The generated `BACKLOG.md` is no longer the byte-identical reassembly; it is a
ONE-LINE-PER-ROW PROJECTION (`render_view` / `project_row`). Measured: 279,814 B ->
66,290 B, -76%, on an unchanged tree -- and it is 100% of the boot cost of a file
every session reads. Nothing is lost, because the bodies were ALREADY in `tasks/`
before this arc; what changed is that the view stopped carrying a second copy.

Three consequences, each handled rather than assumed away:
  * the reassembly is still computed and still asserted (`--check` leg 6,
    `--roundtrip`) -- a lossy view is only safe while the lossless text it projects
    from provably still reassembles;
  * every gate that reads a row BODY (`· routine:`, `· kill-candidates:`,
    `Done when:`, row length) now reads that reassembly through
    `scripts/backlog_source.py::canonical_text`, because pointing such a gate at the
    projection makes it measure an empty set and report a clean PASS;
  * `--write` REFUSES a projection outright and `--force` cannot override it, since
    importing one would overwrite 202 real bodies with their own titles.

CLI verbs, by direction:
  --emit-source   tree -> BACKLOG.md. THE NORMAL POST-FLIP REGEN. Run it after
                  any edit under tasks/.
  --check         verifies BACKLOG.md on disk equals what the tree generates,
                  and that every task file's frontmatter matches its own body.
                  Read-only; armed as an audit.py ship-gate leg ([#433] C1).
  --roundtrip     in-memory lossless proof over the generated text.
  --rank          READ-ONLY report ([#566], building the accepted [#488] axis LEAN):
                  ranks the OPEN queue by the hand-set [P1..P3], breaking ties within
                  a tier on CONSTRAINT CONTENTION over `serialize-group`, and what
                  remains on id as a monotonic age proxy. Derives every input from
                  task bodies already parsed here — no new authored field — and
                  writes nothing, in particular not a reordering of BACKLOG.md.
  --write         BACKLOG.md -> tree. THE IMPORT/RECOVERY DIRECTION, deliberately
                  kept (it is how the tree was bootstrapped and how it would be
                  rebuilt), but post-flip it OVERWRITES SOURCE FROM A DERIVED
                  FILE — so since [#474] a detected warning condition (a populated
                  tasks/ tree) REFUSES before touching disk; --force is the loud,
                  named escape hatch. The clean bootstrap state is unchanged.
  --prune         REFUSED post-flip. Deleting a task file now deletes source, and
                  ADR-107 §6.3 rules retire-not-delete: a retired task leaves the
                  QUEUE by dropping out of manifest.json while its file REMAINS as
                  the allocation record that keeps its id from being re-issued.

Reassembly is byte-identical BY CONSTRUCTION (the line model preserves every
original physical line verbatim), ASSERTED at parse time (parse_backlog refuses
to return a model that does not reassemble back to its own input), and
re-verified by --roundtrip / --check against disk state.

Layer-2 posture is unchanged (ADR-28/36): this writes only BACKLOG.md and the
tasks/ tree, drives no state in any other repo, and never deletes a file it did
not emit.

WHY THE FRONTMATTER PARSER IS HAND-ROLLED, AND NOT WHAT YOU'D EXPECT ([#468]).
The expected answer -- "a YAML library would break byte-exactness" -- is TRUE of
one library and FALSE of another, so it is not the reason. Measured 2026-08-01
over 20 real fixtures from this tree:
  * `python-frontmatter` -- 0/20 byte-identical, with no config escape: PyYAML
    `sort_keys=True` reorders every key, quote style is re-derived rather than
    preserved, and `BaseHandler.format()` strips the trailing newline.
    DISQUALIFIED on fidelity.
  * `ruamel.yaml` -- 20/20 faithful at `width>401`. It would work.
The actual reason is REDUNDANCY, not fidelity: this module TEMPLATES frontmatter
fresh from the body on every emit (`emit_task_file_text`, with a fixed key order)
instead of round-tripping it, so no parser sits on the critical path at all --
the authoritative text is the body line, and frontmatter is output. The only
YAML-ish READS are the narrow `frontmatter_status`/`frontmatter_id` helpers,
which pull one scalar each. Adding a
dependency would buy nothing that is load-bearing here. Recorded because the
choice was previously undocumented anywhere (grep-verified: zero hits for
`python-frontmatter`/`ruamel` in ADR-107/109, the gen_*_tree.py pair,
docs/audits/, LESSONS, PLAYBOOK), which made a load-bearing decision look
accidental. Full measurement:
docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_DEFAULT_SOURCE = _REPO_ROOT / "BACKLOG.md"
_DEFAULT_OUT = _REPO_ROOT / "tasks"

# Line classification (ground truth: BACKLOG.md is pure LF; task lines are always
# a single physical line; fences are column-0 ``` markers).
_TASK_RE = re.compile(r"^- \[#(\d+)\] ")
_THEME_TRIGGER_RE = re.compile(r"^## \[E\d+\]")
_STORY_TRIGGER_RE = re.compile(r"^### \[S\d+\]")

# Derivation regexes (conservative -- each helper returns None when absent).
_PRIORITY_RE = re.compile(r"^- \[#\d+\] \[(P\d)\]")
_SIZE_RE = re.compile(r"^- \[#\d+\] \[P\d\]\[([SML])\]")
_SERIALIZE_GROUP_RE = re.compile(r"· serialize-group: ([A-Za-z0-9-]+)")
_DEPENDS_ON_RE = re.compile(r"· depends-on: ([^·]+?)(?= ·|$)")
#: `[#692]` clause 2 -- the `implements:` key is DERIVED from this body clause, exactly as
#: `depends-on` and `serialize-group` are. That is not a stylistic choice: leg 2 of
#: `source_coherence_problems` re-renders every task file from its own body and refuses a
#: byte difference, so a frontmatter key with no deriver would be hand-editable, inert and
#: silently wrong in the source of truth. One clause, one key, one direction.
_IMPLEMENTS_RE = re.compile(r"· implements: ([^·]+?)(?= ·|$)")
_DEFER_MARKER = "· DEFER"
_TITLE_STRIP_RE = re.compile(r"^- \[#\d+\] (?:\[P\d\](?:\[[SML]\])?)?\s*(.*)$")
_TITLE_FALLBACK_DELIMS = (" — ", " (", ": ", " · ")

_ORPHAN_RE = re.compile(r"^\d+-.*\.md$")

# Post-flip provenance ([#439]). Pre-flip each task file carried `source: BACKLOG.md`
# + `derived: true`; both became FALSE at the flip -- these files are the source now,
# and BACKLOG.md is the derived side. One honest line replaces the pair, and it doubles
# as the engine-managed marker: a task-shaped file carrying it is ours (a retired
# allocation record or a live task), one without it is foreign and is never touched.
_PROVENANCE_KEY = "generates"
_PROVENANCE_LINE = f"{_PROVENANCE_KEY}: BACKLOG.md"

# A RETIRED allocation record must say so. ADR-107 §6.3 requires the retained record to
# carry its opaque id AND its terminal status; an unreferenced file still reading
# `status: open` is a closed task that looks actionable to every consumer of the tree.
# Enforced rather than merely documented (terra P1, 13th pass) -- this repo's own
# "no organ = decoration" rule: a retirement convention with no gate is prose.
_TERMINAL_STATUSES = ("closed", "retired", "superseded")
_FM_STATUS_RE = re.compile(r"^status: (.+)$", re.MULTILINE)
_FM_ID_RE = re.compile(r'^id: "\[#(\d+)\]"$', re.MULTILINE)

# --- [#589] THE VIEW PROJECTION and its two size assertions -----------------------------
#
# `BACKLOG.md` is emitted as ONE LINE PER ROW (see `render_view`). These two ceilings are
# what make that structural rather than a convention someone can quietly undo: both are
# checked by `find_incoherences`, i.e. by the same `--check` the audit-health commit gate
# and the ship gate already run, so a regression to full-body rendering FAILS rather than
# lands. Measured on the live tree at the time of the flip (2026-08-26, 202 rows):
# total 66,290 B, mean 141 B/row, max 222 B/row, against 279,814 B / 1,199 B-per-row before.
#
# TWO legs, because they refuse DIFFERENT things and one alone is not enough:
#   * PER-ROW MAX is the anti-re-inflation leg and it is the one with teeth. It is
#     GROWTH-PROOF -- adding rows never moves it -- so it holds forever without being
#     re-baselined, and a single row rendered back at body length (mean 1,199 B) trips it
#     on its own.
#   * TOTAL BYTES records the [#589] done-when bar as an enforced fact rather than a
#     claim in a closed row. It is NOT growth-proof and is not pretended to be: at 66,290 B
#     today it holds ~230 further rows before it binds. When it does bind, that is the
#     backlog outgrowing its declared budget -- groom, or raise this deliberately, the same
#     way `validate_doc_rot._FILE_SIZE_BUDGETS` treats CLAUDE.md's 200-line budget. Set at
#     100,000 rather than at the done-when's 70,000 so ordinary queue growth cannot wedge a
#     PER-COMMIT gate; the 70,000 figure is asserted where a point-in-time measurement
#     belongs, in `tests/test_gen_task_tree.py`.
_VIEW_ROW_BYTE_CEILING = 400
_VIEW_BYTE_CEILING = 100_000
# The projection's own pointer prefix -- one place, so the renderer and any reader agree.
_VIEW_POINTER_DIR = "tasks/"
# THE PROJECTION'S GRAMMAR, in one place, because two different jobs must agree on it:
# `view_problems` (is the committed view still a view?) and `_looks_like_view` (would
# importing this file destroy the corpus?). They were separate heuristics for one commit and
# that was already one too many -- the terra review of 2026-08-26 found a bypass in the
# second and a gap in the first, and both trace to the same thing: neither asserted the SHAPE
# `project_row` actually emits.
#
# END-ANCHORED, and that anchor carries the weight. A projected row ends with its
# ` · tasks/<file>.md` pointer, so body material appended to a row breaks the match rather
# than merely making it longer. What the anchor cannot catch is body material spliced BEFORE
# the pointer; that is what `_VIEW_ROW_BYTE_CEILING` bounds, and the two together are what
# make re-inflation a FAIL instead of a slow drift (see `view_problems` for the arithmetic).
_VIEW_ROW_RE = re.compile(
    r"^- \[#\d+\] (?:\[P\d\](?:\[[SML]\])?\s)?.*? · tasks/[^/\\]+\.md$")

# THE VIEW'S IDENTITY, emitted by `render_view` itself and by nothing else. This is what the
# destructive-import refusal reads; the grammar above is what the GATE reads. They were the
# same predicate for one round and terra broke it from both sides at once:
#   * a projection whose row exceeded the per-row budget stopped looking like a projection,
#     so `--write --force` would import it and overwrite every body (CRITICAL); and
#   * a legitimate full-body row under the budget that happened to cite its task file last
#     matched the grammar, so `--write` refused a valid bootstrap input with no override
#     (HIGH).
# Those two cannot BOTH be fixed by tuning a shape heuristic -- tightening it widens one hole
# while narrowing the other. Identity is not a heuristic: this line is in a file iff the
# generator put it there.
#
# Emitted from HERE, not from the manifest's prose header, and that is the difference between
# a marker and a decoration: manifest prose is source an operator may edit, so a sentinel
# living there could be retitled away and silently re-enable the destructive import. This one
# is a property of the RENDERER.
#
# HONEST FAILURE DIRECTION, since it has one: strip the line and `--write` stops refusing.
# That is strictly better than the shape predicate's failure, which ran in BOTH directions --
# and the exact leg (byte-equality with `render_view`) still catches the current tree's view
# regardless, so stripping it only reaches a view of some OTHER tree.
_VIEW_MARKER = ("<!-- [#589] GENERATED VIEW — one line per row. NOT an import source: "
                "`gen_task_tree.py --write` refuses this file. -->")
# NO ROW-TEXT SIGNAL SURVIVES IN EITHER PREDICATE, and that is the whole lesson of terra
# round 1. `Done when:` looks like a perfect body marker -- ADR-66 requires it on every real
# row and a projected row has no body -- but a row's TITLE can contain the words, and a title
# rides into the projection verbatim. Used in the import refusal it was a CRITICAL bypass (one
# such row and `--write --force` overwrote every body); used in the gate it was a false FAIL
# that REFUSED `--emit-source` on a legitimate row, i.e. the generator could not emit the very
# view the gate was demanding. Both were caught by the suite, one by a test written for this
# arc and one by a fixture that predates it.
#
# What is left is STRUCTURE, which the renderer owns and a title cannot forge: the
# end-anchored grammar plus the per-row budget.


def frontmatter_status(file_text: str) -> str | None:
    """The `status:` value declared in a task file's frontmatter, or None if absent."""
    m = _FM_STATUS_RE.search(file_text)
    return m.group(1).strip() if m else None


def frontmatter_id(file_text: str) -> int | None:
    """The `id:` declared in a task file's frontmatter, or None if absent/malformed."""
    m = _FM_ID_RE.search(file_text)
    return int(m.group(1)) if m else None


@dataclass(frozen=True)
class TaskRow:
    """One task line, plus the theme/story it was nested under at parse time."""

    id: int
    raw: str  # exact original line text, no trailing newline
    theme: str | None  # full text after '## ', e.g. '[E7] Tooling & evaluation'
    story: str | None  # full text after '### '


@dataclass(frozen=True)
class Model:
    """The lossless line model: every physical line of BACKLOG.md, in order."""

    nodes: list[tuple[str, TaskRow | str]]  # ('prose', line) | ('task', TaskRow)
    source_text: str


def parse_backlog(text: str) -> Model:
    """Parse BACKLOG.md text into a Model.

    Refuses CRLF input (the repo's byte contract is pure LF) and duplicate task
    ids, both loudly. Before returning, asserts that reassemble_from_model(model)
    reproduces `text` exactly -- the lossless invariant this whole module exists
    to uphold.
    """
    if "\r" in text:
        raise ValueError("parse_backlog: CRLF detected in input; this repo's byte contract is pure LF")

    nodes: list[tuple[str, TaskRow | str]] = []
    in_fence = False
    current_theme: str | None = None
    current_story: str | None = None
    seen_ids: set[int] = set()

    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            nodes.append(("prose", line))
            continue
        if not in_fence and _THEME_TRIGGER_RE.match(line):
            current_theme = line[3:]
            current_story = None
            nodes.append(("prose", line))
            continue
        if not in_fence and _STORY_TRIGGER_RE.match(line):
            current_story = line[4:]
            nodes.append(("prose", line))
            continue
        task_match = _TASK_RE.match(line) if not in_fence else None
        if task_match:
            task_id = int(task_match.group(1))
            if task_id in seen_ids:
                raise ValueError(f"parse_backlog: duplicate task id [#{task_id}]")
            seen_ids.add(task_id)
            nodes.append(("task", TaskRow(id=task_id, raw=line, theme=current_theme, story=current_story)))
            continue
        nodes.append(("prose", line))

    model = Model(nodes=nodes, source_text=text)
    if reassemble_from_model(model) != text:
        raise AssertionError("parse_backlog: lossless reassembly invariant violated")
    return model


def reassemble_from_model(model: Model) -> str:
    """Inverse of parse_backlog: rejoin every node's original line with '\\n'."""
    parts: list[str] = [payload.raw if kind == "task" else payload for kind, payload in model.nodes]
    return "\n".join(parts)


def derive_priority(raw: str) -> str | None:
    m = _PRIORITY_RE.match(raw)
    return m.group(1) if m else None


def derive_size(raw: str) -> str | None:
    m = _SIZE_RE.match(raw)
    return m.group(1) if m else None


def derive_status(raw: str) -> str:
    return "deferred" if _DEFER_MARKER in raw else "open"


def derive_serialize_group(raw: str) -> str | None:
    m = _SERIALIZE_GROUP_RE.search(raw)
    return m.group(1) if m else None


def derive_depends_on(raw: str) -> str | None:
    m = _DEPENDS_ON_RE.search(raw)
    return m.group(1).strip() if m else None


def derive_implements(raw: str) -> str | None:
    """The decisions this row discharges -- `[#692]`, A9-1's `implements` edge.

    Returns the clause VALUE as written; the token grammar is validated by
    `validate_backlog._check_implements_grammar` and joined to the graph by
    `file_purpose_graph.decision_key`. Three owners, one clause, and none of them re-derives
    another's half.
    """
    m = _IMPLEMENTS_RE.search(raw)
    return m.group(1).strip() if m else None


def derive_title(raw: str) -> str:
    """Best-effort human title for a task line. Always non-empty (fallback 'task')."""
    m = _TITLE_STRIP_RE.match(raw)
    rest = m.group(1) if m else raw
    if rest.startswith("**"):
        end = rest.find("**", 2)
        if end != -1:
            title = rest[2:end].strip()
            return title if title else "task"
    cut = len(rest)
    for delim in _TITLE_FALLBACK_DELIMS:
        idx = rest.find(delim)
        if idx != -1 and idx < cut:
            cut = idx
    title = rest[:cut].replace("*", "").strip()
    return title if title else "task"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())
    slug = slug.strip("-")
    slug = re.sub(r"-+", "-", slug)
    slug = slug[:48].rstrip("-")
    return slug if slug else "task"


def task_filename(task: TaskRow) -> str:
    """Deterministic filename for one task.

    Pure and collision-blind by design -- a caller enumerating a whole emission
    set (write_tree, the --check in-memory builder) is responsible for detecting
    a collision across the set and refusing loudly; ids are unique so one should
    never actually occur.
    """
    return f"{task.id}-{slugify(derive_title(task.raw))}.md"


def emit_task_file_text(task: TaskRow, status_override: str | None = None) -> str:
    """Render one task's frontmattered .md file text.

    Fixed key order (id, title, status, priority?, size?, theme?, story?,
    serialize-group?, depends-on?, implements?, generates); optional keys are omitted when
    their deriver returns None (or, for theme/story, when the TaskRow field
    itself is None).

    This is also the ORACLE for frontmatter honesty post-flip ([#439]): every
    key above except theme/story is a pure function of `task.raw`, so re-rendering
    a file from its own body must reproduce the file byte-for-byte. `--check`
    asserts exactly that, which is what stops a hand-edited `status:` from sitting
    in a source-of-truth file meaning nothing. theme/story come from the task's
    position in the manifest, not from its line, so they are supplied by the
    caller rather than re-derived.

    `status_override` is the ONE deliberate exception, and it exists for exactly one
    caller: `close_row_plan` ([#730]). `derive_status` can only ever return "open" or
    "deferred" -- it has no body grammar for "closed" -- so a terminal status can never be
    reached by re-deriving from the body. Every other caller passes None and gets the pure
    derivation; `plan_frontmatter_refresh` is one of them, which is what keeps a terminal
    status from ever being computed by a regen (see [#730] item 3 -- the row this exists to
    close is absent from the manifest by the time any regen looks at it, so the regen never
    reaches this file at all).
    """
    lines = ["---", f'id: "[#{task.id}]"']
    lines.append(f"title: {json.dumps(derive_title(task.raw), ensure_ascii=False)}")
    lines.append(f"status: {status_override if status_override is not None else derive_status(task.raw)}")
    priority = derive_priority(task.raw)
    if priority is not None:
        lines.append(f"priority: {priority}")
    size = derive_size(task.raw)
    if size is not None:
        lines.append(f"size: {size}")
    if task.theme is not None:
        lines.append(f"theme: {json.dumps(task.theme, ensure_ascii=False)}")
    if task.story is not None:
        lines.append(f"story: {json.dumps(task.story, ensure_ascii=False)}")
    serialize_group = derive_serialize_group(task.raw)
    if serialize_group is not None:
        lines.append(f"serialize-group: {serialize_group}")
    depends_on = derive_depends_on(task.raw)
    if depends_on is not None:
        lines.append(f"depends-on: {json.dumps(depends_on, ensure_ascii=False)}")
    implements = derive_implements(task.raw)
    if implements is not None:
        lines.append(f"implements: {json.dumps(implements, ensure_ascii=False)}")
    lines.append(_PROVENANCE_LINE)
    lines.append("---")
    lines.append("")
    lines.append(task.raw)
    return "\n".join(lines) + "\n"


def extract_body(file_text: str) -> str:
    """Inverse of emit_task_file_text's tail: recover the exact raw task line."""
    if not file_text.startswith("---\n"):
        raise ValueError("extract_body: file does not start with a '---' frontmatter fence")
    marker = "\n---\n\n"
    idx = file_text.find(marker, 1)
    if idx == -1:
        raise ValueError("extract_body: no closing '---' fence followed by a blank line was found")
    body = file_text[idx + len(marker) :]
    if not body.endswith("\n"):
        raise ValueError("extract_body: body does not end with a trailing newline")
    return body[:-1]


def render_manifest(model: Model, fname_by_id: dict[int, str]) -> str:
    """tasks/manifest.json text: schema + output hash + one entry per node, in order.

    Schema 2 ([#439]) states the post-flip direction. Schema 1 read
    `source: BACKLOG.md` / `source_sha256`, which described the tree as derived FROM
    that file; after the flip the arrow points the other way, so the keys name what
    this manifest GENERATES. The hash VALUE is unchanged in kind -- it is still the
    sha256 of the reassembled BACKLOG.md text -- but its meaning flips from "the
    bytes we were built from" to "the bytes we are expected to produce", which is
    what makes it checkable against the file on disk.
    """
    nodes_out: list[dict[str, object]] = []
    for kind, payload in model.nodes:
        if kind == "task":
            nodes_out.append({"task": payload.id, "file": fname_by_id[payload.id]})
        else:
            nodes_out.append({"prose": payload})
    manifest = {
        "schema": 2,
        "role": "source-of-truth",
        "generates": "BACKLOG.md",
        "generated_sha256": hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
        "generator": "scripts/gen_task_tree.py",
        "nodes": nodes_out,
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def _task_rows(model: Model) -> list[TaskRow]:
    return [payload for kind, payload in model.nodes if kind == "task"]


def _fname_map(tasks: list[TaskRow]) -> dict[int, str]:
    """id -> filename, refusing (loudly) a filename collision across the set."""
    fname_by_id: dict[int, str] = {}
    seen: set[str] = set()
    for task in tasks:
        fname = task_filename(task)
        if fname in seen:
            raise ValueError(f"gen_task_tree: filename collision: {fname}")
        seen.add(fname)
        fname_by_id[task.id] = fname
    return fname_by_id


def _is_engine_managed(path: Path) -> bool:
    """True iff the file carries this engine's provenance line in its frontmatter.

    Post-flip ([#439]) this no longer gates a DELETION path -- nothing deletes task
    files any more (ADR-107 §6.3, retire-not-delete). It gates CLASSIFICATION: a
    task-shaped file under tasks/ that is not referenced by the manifest is either
    a RETIRED allocation record (ours, legitimate, keeps its id from being re-issued)
    or a foreign file that wandered in. The marker is what tells those apart, so a
    retirement stays silent while a stray still gets reported.
    """
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return f"\n{_PROVENANCE_LINE}\n" in text


def write_tree(model: Model, out_dir: Path) -> list[str]:
    """Write every task file + manifest.json under out_dir -- the IMPORT direction.

    Post-flip ([#439]) this rebuilds the SOURCE OF TRUTH from the generated file, so
    it is the bootstrap/recovery path, not the routine one; `_cmd_write` warns before
    calling it. It remains here deliberately: it is how the tree was first built, how
    it would be rebuilt from a BACKLOG.md restored out of git, and how the flip itself
    re-stamped 175 files onto the new provenance.

    It NEVER deletes anything. A task-shaped file outside the emission set is reported
    and left alone -- and post-flip that set includes legitimately RETIRED allocation
    records, so the report distinguishes them (ours, expected) from strays (foreign).
    The prune path is gone: it deleted retired task files, which after the flip means
    deleting source and re-opening a spent id for re-issue, exactly what ADR-107 §6.3
    forbids.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    tasks = _task_rows(model)
    fname_by_id = _fname_map(tasks)

    # ONE transaction, like --emit-source (terra P1, 8th pass). Post-flip this rewrites the
    # SOURCE OF TRUTH, so an I/O failure partway through would leave the authoritative tree
    # half-rewritten or a manifest truncated -- the recovery command making things worse
    # than the state it was run to repair.
    staged: list[tuple[Path, str]] = [
        (out_dir / fname_by_id[task.id], emit_task_file_text(task)) for task in tasks]
    staged.append((out_dir / "manifest.json", render_manifest(model, fname_by_id)))

    done: list[tuple[Path, bytes | None]] = []
    try:
        for path, text in staged:
            done.append((path, path.read_bytes() if path.exists() else None))
            path.write_text(text, encoding="utf-8", newline="\n")
    except BaseException:
        # BaseException for the same reason as _cmd_emit_source: a Ctrl+C mid-import must
        # not leave the authoritative tree half-rewritten (terra P1, 9th pass).
        for path, original in reversed(done):
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)
            except OSError:
                print(f"gen_task_tree: ROLLBACK FAILED for {path.name} — inspect the tree",
                      file=sys.stderr)
        raise

    written: list[str] = [path.name for path, _ in staged]

    emitted = set(fname_by_id.values())
    live_ids = set(fname_by_id)
    for p in sorted(out_dir.iterdir()):
        if not (p.is_file() and _ORPHAN_RE.match(p.name) and p.name not in emitted):
            continue
        if not _is_engine_managed(p):
            print(f"gen_task_tree: not in the active queue, left untouched (FOREIGN file): {p.name}")
        elif _id_from_filename(p.name) in live_ids:
            # A title edit changes the derived SLUG, so the import path writes a new
            # filename and the old one lingers holding the SAME id. That is a rename
            # remnant, not a retirement, and it REDs the duplicate-id ledger leg until it
            # is removed. Said plainly rather than deleted here: nothing in this module
            # deletes a task file post-flip (ADR-107 §6.3).
            print(f"gen_task_tree: RENAME REMNANT — {p.name} shares id "
                  f"[#{_id_from_filename(p.name)}] with a file just emitted under a new "
                  f"slug. Remove it; a duplicate id REDs the coherence gate.")
        else:
            print(f"gen_task_tree: not in the active queue, left untouched "
                  f"(retired allocation record): {p.name}")

    return written


def reassemble_from_tree(tree_dir: Path) -> str:
    """Read manifest.json + every task file back into the original BACKLOG.md text.

    This is the proof that tree+manifest carry every byte of the source: a prose
    node contributes its literal string, a task node contributes extract_body of
    its file's bytes (strict utf-8 decode), and the whole thing is '\\n'-joined.
    """
    manifest = json.loads((tree_dir / "manifest.json").read_bytes().decode("utf-8"))
    _require_well_formed_nodes(manifest)
    parts: list[str] = []
    for node in manifest["nodes"]:
        if "task" in node:
            unsafe = manifest_filename_problem(node.get("file"))
            if unsafe:
                raise ValueError(unsafe)
            file_text = (tree_dir / node["file"]).read_bytes().decode("utf-8")
            parts.append(extract_body(file_text))
        else:
            parts.append(node["prose"])
    return "\n".join(parts)


def project_row(task_id: int, body: str, filename: str) -> str:
    """One row's projected line: `- [#id] [P][size] title[ · DEFER] · tasks/<file>`.

    Every field the full body rendered is either ON this line or reachable from its
    pointer, which is the [#589] done-when in one sentence:

      * `[#id]`            -- verbatim, and FIRST, because `^- \\[#(\\d+)\\]` is the shape a
                              dozen gates, two commit-msg hooks and `window_metrics` match.
                              The projection is not free to move it.
      * `[P][size]`        -- kept inline rather than pushed to the pointer: `fleet_health`,
                              `preflight_contract._BACKLOG_ROW`, `check_backlog_filing`'s
                              L-epic leg and `gen_dashboard`'s size mix all read the band off
                              the LINE, and a `[P2][M]` costs 8 bytes.
      * title              -- `derive_title` of the body, i.e. exactly the title the derived
                              frontmatter already carries and `--check` already refuses to
                              let drift from the body.
      * `· DEFER`          -- emitted only for a deferred row. Deliberately the SAME marker
                              the body uses, not a new `status:` field, so `derive_status`
                              reads the projection unchanged and `gen_dashboard`'s
                              open/deferred split keeps working with no code edit. `open` is
                              the absence of the marker, so 176 of 202 rows pay nothing.
      * theme / story      -- POSITIONAL. The projection keeps the manifest's `## [E..]` /
                              `### [S..]` scaffolding verbatim, so a row's theme is its
                              enclosing heading -- which is where `parse_backlog`,
                              `gen_dashboard.theme_stats` and `validate_backlog` have always
                              read it from. Repeating it inline would cost ~5.7 KB to say
                              twice what the file already says once.
      * everything else    -- Done-when, refs, kill-candidates, routine fields, the reason
                              prose: reachable at `tasks/<file>`, which is the SOURCE, not a
                              copy. The pointer is a real openable path, not a glob, because
                              a locator you have to resolve by hand is the failure CLAUDE.md
                              M1 names.

    Pure and total: a body with no band, or no derivable title, still yields a line (the
    band is simply omitted, the title falls back to `task`). A renderer that could refuse a
    row would be a renderer that can silently shorten the queue.
    """
    priority = derive_priority(body)
    size = derive_size(body)
    if priority and size:
        band = f"[{priority}][{size}] "
    elif priority:
        band = f"[{priority}] "
    else:
        band = ""
    defer = f" {_DEFER_MARKER}" if derive_status(body) == "deferred" else ""
    return f"- [#{task_id}] {band}{derive_title(body)}{defer} · {_VIEW_POINTER_DIR}{filename}"


def render_view(tree_dir: Path) -> str:
    """THE GENERATED `BACKLOG.md` ([#589]): manifest prose verbatim + one line per row.

    Same walk as `reassemble_from_tree`, same node order, same prose -- the ONLY difference
    is that a task node contributes `project_row(...)` instead of its whole body. Written as
    a sibling rather than a flag on the reassembler on purpose: the two have opposite
    contracts and collapsing them would put the lossless proof and the lossy projection
    behind one boolean, where a caller could get the wrong one by omission.

    `reassemble_from_tree` did NOT become dead code at the flip and must not be deleted --
    it is still the lossless invariant `--roundtrip` proves, and it is now the FULL-BODY
    canonical text every body-reading gate reads through `scripts/backlog_source.py`.
    """
    manifest = json.loads((tree_dir / "manifest.json").read_bytes().decode("utf-8"))
    _require_well_formed_nodes(manifest)
    parts: list[str] = []
    for node in manifest["nodes"]:
        if "task" in node:
            unsafe = manifest_filename_problem(node.get("file"))
            if unsafe:
                raise ValueError(unsafe)
            file_text = (tree_dir / node["file"]).read_bytes().decode("utf-8")
            parts.append(project_row(node["task"], extract_body(file_text), node["file"]))
        else:
            parts.append(node["prose"])
    # The identity marker goes on line 2, under the document title, where a human opening the
    # file reads it before anything else. INSERTED, not appended: the manifest's last prose
    # node is the empty string that gives the file its trailing newline, and appending after
    # it would strip that.
    parts.insert(1 if parts else 0, _VIEW_MARKER)
    return "\n".join(parts)


def task_row_lines(text: str) -> list[str]:
    """Every task-shaped line OUTSIDE a fenced block, in order.

    FENCE AWARENESS IS NOT OPTIONAL and this helper exists because omitting it was a live
    defect for one commit. `parse_backlog` has always skipped fenced blocks -- a task-shaped
    line inside a ``` block is an EXAMPLE, and `BACKLOG.md` contains such examples -- so a
    naive `_TASK_RE` scan over the raw text reported the repo's own documentation as a
    malformed row. Caught by `test_fenced_task_shaped_prose_is_still_legitimate`, which
    predates this arc. Shared so the gate and the parser cannot disagree about what a row is.
    """
    rows: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and _TASK_RE.match(line):
            rows.append(line)
    return rows


def is_projected_row(line: str) -> bool:
    """True when `line` has the SHAPE `project_row` emits — GRAMMAR ONLY.

    The per-row byte budget is deliberately NOT part of this. Conflating "is this the shape
    the renderer emits" with "is it within budget" meant a projection carrying one over-long
    row stopped being recognised as a projection at all — and terra found that as a CRITICAL,
    because the destructive `--write --force` import was gated on the same predicate. Size is
    a `view_problems` concern, identity is `_VIEW_MARKER`'s, and this is the shape.
    """
    return bool(_VIEW_ROW_RE.match(line))


def view_problems(text: str, where: str) -> list[str]:
    """[#589] — every way a rendered view has stopped being a view. Empty list = healthy.

    `where` names which artifact is being measured so a FAIL says whether the GENERATOR
    regressed or the COMMITTED FILE was inflated -- the two have different remedies and a
    shared message would send the reader to the wrong one.

    THREE legs, and the SHAPE leg is why the byte ceilings are not the whole contract (terra
    HIGH, 2026-08-26). Ceilings alone bound how MUCH can come back; they say nothing about
    WHAT, so a renderer could append body material to every row and stay under them. With the
    end-anchored grammar, appended material breaks the match outright, and only material
    spliced BEFORE the pointer is left for the ceilings to bound.

    NO `Done when:` LEG, deliberately -- see the constants block. It reads as the obvious body
    marker and it is a false FAIL on a legitimate title, which here means REFUSING the regen
    of a view the gate itself demands.

    THE RESIDUAL, stated rather than implied: a view can still pass at
    `_VIEW_BYTE_CEILING` total, which over today's 202 rows and 37,972 B of scaffolding is a
    ~307 B/row mean -- 2.2x the live 141 B, and still a quarter of the 1,198 B/row a
    full-body render costs. Re-inflation to BODY length cannot pass; a 2x drift can, and the
    total ceiling is what eventually catches it.
    """
    problems: list[str] = []
    total = len(text.encode("utf-8"))
    if total > _VIEW_BYTE_CEILING:
        problems.append(
            f"{where} is {total:,} bytes, over the {_VIEW_BYTE_CEILING:,}-byte view ceiling "
            f"([#589]) — the view must stay one line per row; groom the queue, or raise "
            f"_VIEW_BYTE_CEILING deliberately")
    rows = task_row_lines(text)
    over = [(line, len(line.encode("utf-8"))) for line in rows
            if len(line.encode("utf-8")) > _VIEW_ROW_BYTE_CEILING]
    if over:
        worst = max(over, key=lambda pair: pair[1])
        problems.append(
            f"{where} carries {len(over)} row(s) over the {_VIEW_ROW_BYTE_CEILING}-byte "
            f"per-row ceiling ([#589]), worst {worst[1]} bytes: "
            f"{worst[0][:80]}… — a row body belongs in tasks/, not in the view")
    misshapen = [line for line in rows if not _VIEW_ROW_RE.match(line)]
    if misshapen:
        problems.append(
            f"{where} carries {len(misshapen)} row(s) that are not the [#589] projection "
            f"shape `- [#id] [P][size] title[ · DEFER] · tasks/<file>.md`, first: "
            f"{misshapen[0][:80]}… — a row that does not END at its pointer is carrying body")
    return problems


def _looks_like_view(source_path: Path, out_dir: Path | None = None) -> bool:
    """True when `source_path` is a [#589] PROJECTION rather than a full-body backlog.

    THE ANSWER GATES A DATA-DESTROYING IMPORT, so it asks only questions that have exact
    answers. NO SHAPE HEURISTIC, and that is terra round 2's lesson in one line:

      1. EXACT -- is this byte-for-byte what the tree currently projects? When `out_dir`
         carries a manifest, that is a comparison, not a guess.
      2. IDENTITY -- failing that (a stale view, a view of a DIFFERENT tree, no tree handed
         over), does it carry `_VIEW_MARKER`, which only `render_view` emits?

    WHY NOT SHAPE. Two rounds of review broke the shape predicate from both sides at once,
    and the second pair proved the class rather than the instance:
      * round 1 (CRITICAL) -- it required that no row carry `Done when:`, and a row whose
        bold TITLE contains those words defeated the conjunction, so `--write --force`
        would import the view and overwrite all 202 bodies;
      * round 2 (CRITICAL) -- the replacement folded the per-row byte budget into the
        predicate, so a projection with one over-long row stopped looking like a projection
        and the same import opened again;
      * round 2 (HIGH) -- and the mirror: a legitimate full-body row under the budget that
        happened to cite its task file last MATCHED, so `--write` refused a valid bootstrap
        input with no override.
    Tightening a shape heuristic closes one of those and widens the other. Identity closes
    both, because a marker is in a file iff the generator put it there.

    Conservative on the OTHER side -- an unreadable file is NOT called a view (returns
    False), because a false positive would block the legitimate bootstrap path this command
    exists for.
    """
    try:
        text = source_path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return False
    if out_dir is not None and (out_dir / "manifest.json").is_file():
        try:
            if text == render_view(out_dir):
                return True
        except (OSError, ValueError, KeyError, UnicodeDecodeError):
            pass          # an unreadable tree cannot answer leg 1; leg 2 still can
    return _VIEW_MARKER in text


def write_warnings(out_dir: Path) -> list[str]:
    """[#474] — the conditions under which --write would DESTROY source-of-truth state.

    Post-flip, the import direction rebuilds `tasks/` from the GENERATED BACKLOG.md, so
    running it against a populated tree overwrites source. Each returned string is one
    detected condition; an empty list is the clean bootstrap/recovery state (absent or
    empty target tree — nothing to destroy), where --write keeps its legacy behavior.
    """
    warnings: list[str] = []
    if (out_dir / "manifest.json").exists():
        warnings.append(
            f"{out_dir / 'manifest.json'} exists -- the target is a POPULATED source-of-"
            f"truth tree, and the import would rewrite it from the generated file")
    task_files = ([p.name for p in sorted(out_dir.iterdir())
                   if p.is_file() and _ORPHAN_RE.match(p.name)]
                  if out_dir.exists() else [])
    if task_files:
        warnings.append(
            f"{len(task_files)} task file(s) present under {out_dir} -- an import "
            f"re-derives filenames from titles, which can re-slug live ids and orphan "
            f"the originals (the [#473] incident: 17 files re-slugged by one mistaken run)")
    return warnings


def _cmd_write(source_path: Path, out_dir: Path, force: bool = False) -> int:
    """IMPORT: BACKLOG.md -> tree. [#474]: a warned state ABORTS unless --force.

    Post-flip this direction overwrites the SOURCE OF TRUTH from a generated file. The
    pre-[#474] behavior -- warn on stderr, then rewrite anyway -- was warn-then-destroy:
    the warning was vigilance, the rewrite was the defect. Now any detected warning
    condition refuses BEFORE touching disk (non-zero exit, zero bytes changed); --force
    is the explicit, loud escape hatch and names every condition it overrides. A clean
    state (no conditions -- the bootstrap/recovery case) behaves exactly as before.
    """
    # [#589] — the ONE refusal --force cannot override, and the asymmetry is the point.
    # Every OTHER --write refusal guards a state a determined operator might legitimately
    # want to overwrite (that is what --force is for). Importing the PROJECTION is not in
    # that class: it would rewrite all 202 bodies as their own one-line titles, and the
    # bodies are the source of truth, so there is no state in which it is the right act.
    # A --force that could reach it would make the guard advisory, which is what the
    # pre-[#474] warn-then-destroy shape already proved is not a guard.
    if _looks_like_view(source_path, out_dir):
        print(f"gen_task_tree: --write REFUSED (nothing written) — {source_path.name} is the "
              f"[#589] one-line VIEW, not a full-body backlog.\n"
              f"  No row in it carries 'Done when:', which ADR-66 requires of every real row, "
              f"so importing it would replace every task body with its own title.\n"
              f"  The bodies are already the source of truth under {out_dir}; there is nothing "
              f"to import. This refusal is NOT overridable with --force.", file=sys.stderr)
        return 2
    warned = write_warnings(out_dir)
    if warned and not force:
        print(f"gen_task_tree: --write REFUSED (nothing written) -- "
              f"{len(warned)} warning condition(s):", file=sys.stderr)
        for warning in warned:
            print(f"  - {warning}", file=sys.stderr)
        print("  The routine post-flip regen is --emit-source (tree -> BACKLOG.md).\n"
              "  To run the import anyway, re-run with --write --force.", file=sys.stderr)
        return 2
    if warned:
        print(f"gen_task_tree: --force OVERRIDE -- proceeding despite "
              f"{len(warned)} warning condition(s):", file=sys.stderr)
        for warning in warned:
            print(f"  - {warning}", file=sys.stderr)
    print(f"gen_task_tree: WARNING -- --write rebuilds the SOURCE OF TRUTH ({out_dir}) "
          f"from {source_path.name}, which is a GENERATED file since the [#439] flip. "
          f"Any edit made under tasks/ but not yet emitted will be overwritten. The "
          f"routine post-flip regen is --emit-source (tree -> BACKLOG.md).", file=sys.stderr)
    text = source_path.read_bytes().decode("utf-8")
    model = parse_backlog(text)
    write_tree(model, out_dir)
    task_count = sum(1 for kind, _ in model.nodes if kind == "task")
    print(f"gen_task_tree: imported {task_count} task file(s) + manifest into {out_dir}")
    return 0


def _cmd_emit_source(source_path: Path, out_dir: Path) -> int:
    """THE NORMAL POST-FLIP REGEN: tree -> BACKLOG.md.

    A COMPLETE regen of the derived material, in three steps, because a half-regen left
    the documented workflow unable to reach green (terra P1, 2026-07-28):
      1. re-render every task file's DERIVED frontmatter from its own body + manifest
         placement (bodies are never touched — they are the source);
      2. write BACKLOG.md from the tree;
      3. re-pin the manifest's `generated_sha256` to those output bytes.

    Each step writes only when bytes actually change, so a no-op regen leaves mtimes
    alone and cannot manufacture a working-tree diff for the coherence gate's
    index/worktree guard to trip over.
    """
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"gen_task_tree: emit-source FAIL: no manifest at {manifest_path} "
              f"-- the source of truth is missing, refusing to write {source_path.name}",
              file=sys.stderr)
        return 1
    # PLAN EVERYTHING FIRST, THEN WRITE (terra P1, 4th pass). Both the frontmatter renders
    # and the full reassembly are computed before a single source byte is touched, so a
    # malformed or missing task file aborts with the tree exactly as it was rather than
    # half-rewritten. Reassembly reads BODIES, which the refresh never alters, so computing
    # it from the pre-write state is equivalent to computing it after.
    # REFUSE on identity corruption before writing anything (terra P1, 7th pass). A regen
    # cannot fix a broken id record -- it would faithfully emit the corruption into
    # BACKLOG.md, re-pin the hash to it, and exit 0, leaving only a LATER --check to notice
    # what this command had already written. Stale derived frontmatter is deliberately NOT
    # in this set: repairing it is what the regen is for.
    broken = identity_problems(out_dir)
    if broken:
        print("gen_task_tree: emit-source REFUSED (nothing written) — the source tree's "
              "identity record is incoherent, and a regen would emit the corruption:",
              file=sys.stderr)
        for problem in broken[:6]:
            print(f"  - {problem}", file=sys.stderr)
        if len(broken) > 6:
            print(f"  (+{len(broken) - 6} more)", file=sys.stderr)
        return 1
    try:
        plan = plan_frontmatter_refresh(out_dir)
        # [#589]: the OUTPUT is the projection, not the reassembly. `reassemble_from_tree`
        # is still computed on the --check path (it is the lossless invariant), but what
        # lands on disk -- and what `generated_sha256` pins -- is what `render_view` emits.
        generated = render_view(out_dir)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        print(f"gen_task_tree: emit-source FAIL (nothing written): {exc}", file=sys.stderr)
        return 1
    # REFUSE rather than write an over-budget view (same posture as the identity refusal
    # above): writing it and letting a LATER --check report what this command had already
    # committed is the failure mode the plan-before-write discipline exists to prevent.
    oversize = view_problems(generated, "the generated view")
    if oversize:
        print("gen_task_tree: emit-source REFUSED (nothing written) — the projection is "
              "over its declared size budget ([#589]):", file=sys.stderr)
        for problem in oversize:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    # Roll back on a mid-loop I/O failure (terra P1, 6th pass). Planning first only
    # covers DATA errors; a full disk or a permissions change partway through would still
    # leave the source tree half-rewritten while BACKLOG.md and the hash never updated —
    # which is the very state the plan-before-write guarantee claims to prevent. Restore
    # the prior bytes so a failed regen is a no-op rather than a torn write.
    # ONE transaction over ALL THREE artifacts (terra P1, 6th + 7th pass). The 6th-pass
    # rollback covered only the task-frontmatter writes, leaving BACKLOG.md and
    # manifest.json — the latter now part of the SOURCE — unguarded and in-place: a failure
    # there could leave the outputs inconsistent or the manifest truncated. Every write
    # this command performs is now staged into one list and rolled back together.
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    digest = hashlib.sha256(generated.encode("utf-8")).hexdigest()
    # terra P1 (9th pass): an existing output containing invalid UTF-8 made this decode
    # raise BEFORE any write, so the one command that could REPAIR the derived artifact
    # was the one command that could not run. Undecodable output is simply stale.
    current: str | None
    try:
        current = source_path.read_bytes().decode("utf-8") if source_path.exists() else None
    except UnicodeDecodeError:
        current = None

    writes: list[tuple[Path, str]] = list(plan)
    if current != generated:
        writes.append((source_path, generated))
    if manifest.get("generated_sha256") != digest:
        manifest["generated_sha256"] = digest
        writes.append((manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"))

    done: list[tuple[Path, bytes | None]] = []
    try:
        for path, text in writes:
            done.append((path, path.read_bytes() if path.exists() else None))
            path.write_text(text, encoding="utf-8", newline="\n")
    except BaseException as exc:
        # BaseException, not OSError (terra P1, 9th pass): a Ctrl+C landing mid-write
        # raises KeyboardInterrupt, which an `except OSError` rollback does not catch --
        # leaving the SOURCE OF TRUTH partially written by the very handler meant to
        # prevent that. Roll back for any interruption, then re-raise anything that is not
        # a plain I/O error so Ctrl+C still reads as Ctrl+C.
        for path, original in reversed(done):
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)
            except OSError:
                print(f"gen_task_tree: ROLLBACK FAILED for {path.name} — inspect the tree "
                      f"before regenerating", file=sys.stderr)
        print(f"gen_task_tree: emit-source FAIL (rolled back, nothing changed): {exc!r}",
              file=sys.stderr)
        if not isinstance(exc, OSError):
            raise
        return 1

    refreshed = [path.name for path, _ in plan]
    if refreshed:
        print(f"gen_task_tree: refreshed derived frontmatter in {len(refreshed)} task file(s)")
    if current != generated:
        print(f"gen_task_tree: regenerated {source_path.name} from {out_dir} "
              f"({_task_count(out_dir)} task(s))")
    elif not refreshed:
        print(f"gen_task_tree: {source_path.name} already current ({_task_count(out_dir)} task(s))")
    if any(path == manifest_path for path, _ in writes):
        print("gen_task_tree: re-pinned manifest generated_sha256")
    return 0


def _task_count(out_dir: Path) -> int:
    """How many task nodes the manifest carries (0 if it cannot be read)."""
    try:
        manifest = json.loads((out_dir / "manifest.json").read_bytes().decode("utf-8"))
    except (OSError, ValueError, KeyError):
        return 0
    return sum(1 for node in manifest.get("nodes", []) if "task" in node)


def find_incoherences(source_path: Path, out_dir: Path) -> list[str]:
    """The testable core of `--check`: every way BACKLOG.md disagrees with its source tree.

    POST-FLIP DIRECTION ([#439]). The tree is the expectation and `BACKLOG.md` is the
    thing being checked -- the inverse of the pre-flip contract, where the tree was
    checked against the file. Returns a list of human-readable problems; EMPTY means
    the committed `BACKLOG.md` is exactly what `tasks/` generates.

    `scripts/audit.py::check_task_tree_coherence` ([#433] C1) wires this as a ship-gate
    leg, which is what makes it an armed gate rather than a mode nothing invokes.

    Three independent legs, because they fail in different ways:
      1. STRUCTURE -- the manifest reads, and every task node it references resolves to
         a file on disk that parses.
      2. FRONTMATTER HONESTY -- each task file re-renders byte-identically from its own
         body. This leg is NEW at the flip and it is the one that earns its keep: the
         frontmatter is derived from the body, so in a source-of-truth file it would
         otherwise be editable, inert, and silently wrong. Catching it here is what lets
         the schema keep derived fields at all.
      3. OUTPUT -- the full reassembly equals the bytes of `BACKLOG.md` on disk.

    A task-shaped file the manifest does NOT reference is not a problem when it carries
    our provenance marker: that is a RETIRED allocation record, which ADR-107 §6.3
    requires the tree to keep so its id is never re-issued. An unreferenced file WITHOUT
    the marker is foreign and is reported.

    LEDGER LIMIT, stated so a green is not over-read: id re-issue is caught while both
    holders are PRESENT (active-vs-active, the concurrent-branch collision; and
    active-vs-retired). Deletion of a retired record is NOT caught -- this walks files
    that exist, and nothing declares which files ought to exist, so removing a retired
    file silently frees its id again. Making the ledger tamper-evident needs an explicit
    tombstone record and is [#440]; ADR-107 §6.3 already records the directory as "not
    complete today" as a ledger.

    SCOPE, stated honestly: this compares two artifacts against each other. It does NOT
    detect a consistent rewrite of both together, because the expectation is derived from
    the tree being checked. That is why source integrity remains a separate leg -- a clean
    `git status`, plus the manifest's `generated_sha256` pinning which output bytes this
    tree claims to produce.
    """
    identity, stale_frontmatter, manifest = _scan_source(out_dir)
    problems = list(identity) + list(stale_frontmatter)
    if manifest is None:
        return problems

    # --- leg 3: output ----------------------------------------------------------
    # [#589]: the expectation is the PROJECTION. The lossless reassembly is still computed
    # (leg 5) because it is the invariant that makes the projection safe to be lossy.
    try:
        generated = render_view(out_dir)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        problems.append(f"render_view failed: {exc}")
        return problems
    try:
        on_disk = source_path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError too (terra P1, 10th pass): pass 9 taught --emit-source to
        # REPAIR a non-UTF-8 output but left --check crashing on the same state, so the
        # verification path traceback'd on exactly the condition the regen path handles.
        # A corrupt output is a coherence FAILURE to report, not an exception to raise.
        problems.append(f"cannot read generated file {source_path}: {exc}")
        return problems
    if on_disk != generated:
        problems.append(f"{source_path.name} does not match what tasks/ generates "
                        f"(regenerate with `gen_task_tree.py --emit-source`)")

    # --- leg 4: the integrity pin actually pins something ------------------------
    # terra P1 (2026-07-28): schema 2 advertises `generated_sha256` as the pin on which
    # output bytes this tree claims to produce, but nothing validated it, and
    # --emit-source did not maintain it. An unchecked, unmaintained hash is decoration --
    # it would drift on the first edit and still report green, which is the exact
    # "no organ = decoration" failure this repo gates against.
    declared = manifest.get("generated_sha256")
    actual_hash = hashlib.sha256(generated.encode("utf-8")).hexdigest()
    if declared is None:
        problems.append("manifest.json carries no generated_sha256 (schema 2 requires it)")
    elif declared != actual_hash:
        problems.append("manifest.json generated_sha256 does not match what the tree "
                        "generates (regenerate with `gen_task_tree.py --emit-source`)")

    # --- leg 5: the view stays a view ([#589]) -----------------------------------
    # Measured on BOTH faces on purpose. The GENERATED bytes catch a regression in the
    # renderer (someone re-points --emit-source at the reassembler); the ON-DISK bytes
    # catch an inflated committed file directly, so the failure names the view even in the
    # runs where leg 3 has already reported a mismatch for its own reason.
    problems += view_problems(generated, "the generated view")
    problems += view_problems(on_disk, f"{source_path.name} on disk")

    # --- leg 6: the LOSSLESS invariant still holds -------------------------------
    # The projection is safe to be lossy ONLY because the tree still round-trips to the
    # full-body text every body-reading gate now reads (scripts/backlog_source.py). Before
    # [#589] leg 3 proved that for free, by comparing the reassembly against disk. It no
    # longer does, and dropping the proof silently is precisely how a lossy view stops
    # being recoverable, so the reassembly is asserted here in its own right.
    try:
        canonical = reassemble_from_tree(out_dir)
        parse_backlog(canonical)   # raises on CRLF / duplicate id / non-lossless model
    except (OSError, ValueError, KeyError, UnicodeDecodeError, AssertionError) as exc:
        problems.append(f"the tasks/ tree no longer reassembles to lossless full-body "
                        f"text — the view's bodies are unrecoverable: {exc}")

    return problems


def _scan_source(out_dir: Path) -> tuple[list[str], list[str], dict | None]:
    """Read the source tree once and split its problems into two classes.

    Returns `(identity_problems, stale_frontmatter_problems, manifest)`. The split matters
    because `--emit-source` must REFUSE on the first class and REPAIR the second: stale
    derived frontmatter is what a regen is for, whereas a broken id record is something a
    regen would faithfully write out as corruption (terra P1, 7th pass). `manifest` is None
    when the scan could not get far enough to have one.
    """
    if not out_dir.exists():
        return ([f"source tree missing: {out_dir}"], [], None)
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        return ([f"missing manifest.json in {out_dir} - the source of truth has no "
                 f"structure record"], [], None)
    try:
        manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        return ([f"manifest.json unreadable: {exc}"], [], None)
    # terra P1 (8th pass): a valid-JSON root that is a list/scalar/null made `.get` raise
    # AttributeError, crashing both the regen and the ship-gate instead of reporting.
    if not isinstance(manifest, dict):
        return ([f"manifest.json root is not an object: {type(manifest).__name__}"], [], None)
    if not isinstance(manifest.get("nodes"), list):
        return (["manifest.json has no 'nodes' list"], [], None)
    malformed = [p for p in (manifest_node_problem(n) for n in manifest["nodes"]) if p]
    malformed += manifest_sequence_problems(manifest["nodes"])
    if malformed:
        return (malformed[:6], [], None)

    identity: list[str] = []
    stale: list[str] = []

    # --- structure: every referenced file resolves, exactly once -----------------
    referenced: dict[str, int] = {}
    for node in manifest["nodes"]:
        if "task" not in node:
            continue
        fname = node["file"]
        # terra P1 (7th pass): collapsing repeats into one dict entry hid them. Reassembly
        # emits the body at EVERY occurrence, so a file referenced twice duplicates the
        # task line in BACKLOG.md while the ledger leg counts it once -- and the whole
        # thing hashes and passes.
        if fname in referenced:
            identity.append(f"manifest references the same task file twice: {fname} "
                            f"(reassembly would emit its body at every occurrence)")
            continue
        if node["task"] in referenced.values():
            identity.append(f"manifest references id [#{node['task']}] more than once "
                            f"(at {fname})")
            continue
        referenced[fname] = node["task"]
        if not (out_dir / fname).exists():
            identity.append(f"manifest references a missing task file: {fname}")

    # --- identity + frontmatter honesty -----------------------------------------
    lineage = lineage_from_manifest(manifest)
    for fname in sorted(referenced):
        path = out_dir / fname
        if not path.exists():
            continue  # already reported above
        try:
            actual = path.read_bytes().decode("utf-8")
            body = extract_body(actual)
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            identity.append(f"task file unreadable or malformed: {fname} ({exc})")
            continue
        # The id must agree in ALL THREE places it is written. Rebuilding the expected
        # frontmatter from the FILENAME alone made a body-id edit invisible: change a body
        # from [#439] to [#500] and the expected frontmatter is still [#439], matches the
        # (unchanged) actual, and the emitted BACKLOG.md carries [#500] -- so the file, the
        # manifest and the document disagree about which id this task is, and every leg
        # passes. That is a corrupted allocation ledger, which is the one thing tasks/
        # exists to be trustworthy about (ADR-107 6.3).
        file_id = _id_from_filename(fname)
        body_match = _TASK_RE.match(body)
        body_id = int(body_match.group(1)) if body_match else None
        node_id = referenced[fname]
        if body_id is None:
            identity.append(f"task file body is not a task line: {fname}")
            continue
        # terra P1 (8th pass): _TASK_RE validates only the FIRST line, while both the
        # frontmatter render and reassembly preserve the whole body -- so extra physical
        # lines rode into BACKLOG.md as prose that never passed through manifest.json,
        # which is the authoritative carrier for every non-task line (ADR-107 §2).
        if "\n" in body:
            identity.append(
                f"task file body spans multiple lines: {fname} — a task is ONE physical "
                f"line; non-task prose belongs in manifest.json, not in a task body")
            continue
        if not (file_id == body_id == node_id):
            identity.append(
                f"task id disagrees across filename/body/manifest: {fname} "
                f"(filename [#{file_id}], body [#{body_id}], manifest [#{node_id}]) - "
                f"identity is byte-exact and must agree in all three")
            continue
        # closed-iff-absent-from-the-manifest (ADR-107 §6.3, [#730] AX16-2): the invariant's
        # OTHER direction from the retired-record leg below (which requires the reverse --
        # absent implies terminal). An identity REFUSAL, not a "stale" repair candidate,
        # because `emit_task_file_text` can only re-derive "open"/"deferred" (see its
        # `status_override` docstring) -- so treating this as ordinary staleness would have
        # `plan_frontmatter_refresh` silently flip a hand-set `status: closed` back to
        # "open" on the next regen ([#730] item 3), exactly the silent revert this refusal
        # exists to prevent. `close_row` never leaves this state: it removes the manifest
        # node in the same atomic write that sets the terminal status.
        status = frontmatter_status(actual)
        if status in _TERMINAL_STATUSES:
            identity.append(
                f"task file carries a terminal status while still referenced by the "
                f"manifest: {fname} (status: {status!r}) — closed-iff-absent-from-the-"
                f"manifest (ADR-107 §6.3, [#730] AX16-2): remove its manifest node "
                f"(gen_task_tree.py --close-row) or revert the status")
            continue
        theme, story = lineage.get(fname, (None, None))
        expected = emit_task_file_text(TaskRow(id=file_id, raw=body, theme=theme, story=story))
        if actual != expected:
            stale.append(
                f"task file frontmatter disagrees with its own body or its manifest "
                f"placement: {fname} (frontmatter is DERIVED - edit the body, then "
                f"--emit-source)")

    # --- the id ledger: retired records vs strays vs re-issued ids ---------------
    # terra P1: retire-not-delete only buys an allocation ledger if a spent id cannot come
    # back. Skipping unreferenced engine-managed files silently allowed exactly that -- a
    # retired `439-old.md` alongside a new active `439-new.md` re-issued a spent id and the
    # gate passed, defeating the guarantee 6.3 keeps those files for.
    seen_ids: dict[int, str] = {}
    for fname in sorted(referenced):
        active_id = _id_from_filename(fname)
        if active_id in seen_ids:
            # ADR-107 6.3's OWN named requirement -- "a `tasks/`-level duplicate-id check
            # makes a collision a gate failure at merge time rather than a silent one". It
            # is the concurrent-branch collision the ADR records as a residual it does NOT
            # prevent: two branches allocate the same next-free id, write differently-
            # slugged filenames, and git merges them cleanly.
            identity.append(
                f"id [#{active_id}] is held by two ACTIVE task files: "
                f"{seen_ids[active_id]} and {fname} - an id is allocated once "
                f"(ADR-107 6.3; the concurrent-branch collision this gate exists to catch)")
        else:
            seen_ids[active_id] = fname
    for p in sorted(out_dir.iterdir()):
        if not (p.is_file() and _ORPHAN_RE.match(p.name) and p.name not in referenced):
            continue
        if not _is_engine_managed(p):
            identity.append(f"foreign task-shaped file (not engine-managed, not in the "
                            f"manifest): {p.name}")
            continue
        record_text = p.read_bytes().decode("utf-8", errors="replace")
        # terra P1 (14th pass): a retired record was trusted on its FILENAME alone while
        # active files had all three ids cross-checked. A retired `77-old.md` whose body
        # and frontmatter say [#78] registered 77 as spent while actually holding 78 -- so
        # an active [#78] was not caught as re-issued, and the ledger silently drifted. A
        # record whose whole job is to keep an id spent must be right about WHICH id.
        record_file_id = _id_from_filename(p.name)
        record_fm_id = frontmatter_id(record_text)
        try:
            record_body = _TASK_RE.match(extract_body(record_text))
        except ValueError:
            record_body = None      # malformed record; the status leg reports it
        record_body_id = int(record_body.group(1)) if record_body else None
        # PRESENT and equal, not merely "not contradicting" (terra P1, 15th pass): filtering
        # None out meant a record with a MISSING frontmatter or body id had nothing left to
        # compare, so `mismatched` came back empty and the corrupted record passed. Absence
        # is not agreement -- the same lesson the index/worktree guard already learned.
        if record_fm_id != record_file_id or record_body_id != record_file_id:
            identity.append(
                f"retired allocation record does not state its id consistently: {p.name} "
                f"(filename [#{record_file_id}], frontmatter "
                f"{'[#%d]' % record_fm_id if record_fm_id is not None else 'MISSING'}, "
                f"body {'[#%d]' % record_body_id if record_body_id is not None else 'MISSING'})"
                f" — a record that keeps an id spent must be right about which id")
        status = frontmatter_status(record_text)
        if status not in _TERMINAL_STATUSES:
            identity.append(
                f"retired allocation record is not marked terminal: {p.name} "
                f"(status: {status!r}; expected one of {', '.join(_TERMINAL_STATUSES)}) — "
                f"ADR-107 §6.3 requires the retained record to carry its terminal status, "
                f"or a closed task keeps looking actionable")
        retired_id = _id_from_filename(p.name)
        if retired_id in seen_ids:
            identity.append(
                f"id [#{retired_id}] is re-issued: retired allocation record {p.name} "
                f"and {seen_ids[retired_id]} share it - a spent id must never be reused "
                f"(ADR-107 6.3)")
        else:
            seen_ids[retired_id] = p.name

    return (identity, stale, manifest)


def _id_from_filename(fname: str) -> int:
    """`439-some-slug.md` -> 439. Guarded by `manifest_filename_problem` at every entry."""
    return int(fname.split("-", 1)[0])


_SAFE_TASK_FILENAME_RE = re.compile(r"^\d+-[^/\\]*\.md$")


def manifest_node_problem(node: object) -> str | None:
    """Reject a manifest node that is not one of the two shapes this module writes.

    terra P1 (2026-07-28, 6th pass): the manifest is HAND-EDITED source now, so "valid
    JSON" is not "valid manifest". A `{"prose": 7}` raised AttributeError inside the
    heading walk and a non-object node raised TypeError -- neither is in the exception set
    `_cmd_emit_source` or `audit.py::check_task_tree_coherence` catch, so a malformed
    source artifact CRASHED the regen and the ship-gate instead of being reported as a
    controlled failure. audit.py deliberately lets unexpected exceptions propagate as
    programming defects; bad hand-edited input is not one, so it must be caught here.

    Returns a problem description, or None when the node is well-formed.
    """
    if not isinstance(node, dict):
        return f"manifest node is not an object: {node!r}"
    has_task, has_prose = "task" in node, "prose" in node
    if has_task == has_prose:
        return (f"manifest node must carry exactly one of 'task'/'prose': "
                f"{sorted(node)!r}")
    if has_prose:
        if not isinstance(node["prose"], str):
            return f"manifest prose node value is not a string: {node['prose']!r}"
        return None
    if not isinstance(node["task"], int) or isinstance(node["task"], bool):
        return f"manifest task node id is not an integer: {node['task']!r}"
    return manifest_filename_problem(node.get("file"))


def manifest_sequence_problems(nodes: list) -> list[str]:
    """Sequence-aware manifest validation — what a per-node check structurally cannot see.

    terra P1 (2026-07-28, 12th pass): a task-shaped line smuggled into a `prose` node
    reassembles into `BACKLOG.md` as a real task row while having NO managed task file, so
    it bypasses the ledger entirely — `--check`, the output hash and duplicate-id
    enforcement all stay green over a row the tree does not know exists. Fence state makes
    this sequence-dependent: inside a fenced block `- [#N]` IS legitimately prose (that is
    exactly what `parse_backlog` does), so only an UNFENCED task-shaped prose line is a
    violation.

    Also rejects an embedded newline in a prose value: one node must be one physical line,
    or the line model silently stops being one-node-per-line.
    """
    problems: list[str] = []
    in_fence = False
    for i, node in enumerate(nodes):
        if not isinstance(node, dict) or "prose" not in node:
            continue
        line = node["prose"]
        if not isinstance(line, str):
            continue  # shape is manifest_node_problem's job
        if "\n" in line:
            problems.append(f"manifest prose node {i} spans multiple physical lines — one "
                            f"node is one line")
            continue
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and _TASK_RE.match(line):
            problems.append(
                f"manifest prose node {i} is a TASK row: {line[:60]!r} — a task must have a "
                f"managed task file, or it bypasses the id ledger entirely")
    return problems


def _require_well_formed_nodes(manifest: dict) -> None:
    """Raise ValueError on the first malformed node — the guard for the traversal paths
    (`lineage_from_manifest`, `reassemble_from_tree`) whose callers catch ValueError."""
    if not isinstance(manifest, dict):
        raise ValueError(f"manifest.json root is not an object: {type(manifest).__name__}")
    nodes = manifest.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("manifest.json has no 'nodes' list")
    for node in nodes:
        problem = manifest_node_problem(node)
        if problem:
            raise ValueError(problem)
    sequence = manifest_sequence_problems(nodes)
    if sequence:
        raise ValueError(sequence[0])


def manifest_filename_problem(fname: object) -> str | None:
    """Reject a manifest `file` value that is not a plain task-file basename.

    terra P1 (2026-07-28): `file` values come out of `manifest.json`, which the flip made
    a HAND-EDITED source artifact. `refresh_task_frontmatter` writes through those values,
    so a malformed or traversing path (`439-../../x.md`, an absolute path, a subdirectory)
    would read and REWRITE a file outside `tasks/` during the ordinary `--emit-source`
    workflow. The directory scan's `_ORPHAN_RE` never guarded this, because it walks real
    dirents rather than manifest strings.

    Returns a problem description, or None when the name is safe. Basename-only by
    construction: no separator can survive the character class, so no traversal can.
    """
    if not isinstance(fname, str) or not fname:
        return f"manifest task node has a non-string/empty 'file': {fname!r}"
    if not _SAFE_TASK_FILENAME_RE.match(fname):
        return (f"unsafe manifest 'file' value (must be a bare `<id>-<slug>.md` basename, "
                f"no path separators): {fname!r}")
    return None


def lineage_from_manifest(manifest: dict) -> dict[str, tuple[str | None, str | None]]:
    """filename -> (theme, story), derived from each task node's PLACEMENT in the manifest.

    theme/story are the two frontmatter fields not derivable from a task's own line: they
    come from which headings the task sits under. The authority for that is the manifest's
    node ORDER, so lineage is computed here rather than read back out of the task file.

    Reading it back would make the honesty check tautological for these two fields (terra
    P1, 2026-07-28): moving a task node under a different theme in `manifest.json` would
    leave the file's stale `theme:` matching itself and pass, while reassembly — which uses
    manifest placement, not frontmatter — happily emits the task under the new heading. So
    output comparison would pass too, and the stale lineage would survive both legs.

    Mirrors `parse_backlog`'s heading/fence rules exactly, so the two cannot disagree.
    """
    _require_well_formed_nodes(manifest)
    lineage: dict[str, tuple[str | None, str | None]] = {}
    theme: str | None = None
    story: str | None = None
    in_fence = False
    for node in manifest.get("nodes", []):
        if "prose" in node:
            line = node["prose"]
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if _THEME_TRIGGER_RE.match(line):
                theme, story = line[3:], None
            elif _STORY_TRIGGER_RE.match(line):
                story = line[4:]
        elif node.get("file"):
            lineage[node["file"]] = (theme, story)
    return lineage


def identity_problems(out_dir: Path) -> list[str]:
    """Every way the tree's IDENTITY record is incoherent — the subset a regen cannot fix.

    Separated from `find_incoherences` (terra P1, 2026-07-28, 7th pass) because
    `--emit-source` must refuse on these BEFORE writing, while it must NOT refuse on the
    frontmatter-staleness problems, which are exactly what it exists to repair. Previously
    the regen validated nothing: a body edited to a malformed marker, or to an id that
    disagreed with its filename and manifest node, produced an incoherent `BACKLOG.md`,
    an updated hash, and exit 0 — with only a LATER `--check` noticing the corruption it
    had already written.

    Covers: manifest readability and node shapes, duplicate file/id references, missing or
    malformed task files, filename/body/manifest id agreement, and id re-issue across
    active and retired records. Read-only.
    """
    problems, _, _ = _scan_source(out_dir)
    return problems


def plan_frontmatter_refresh(out_dir: Path) -> list[tuple[Path, str]]:
    """PURE: compute every task file that needs its derived frontmatter re-rendered.

    Writes nothing. Raises on the first unsafe manifest path or malformed task file, so a
    caller learns the whole plan is invalid BEFORE touching disk.

    Split out from the write step (terra P1, 2026-07-28, 4th pass) because rendering
    file-by-file-and-writing left the SOURCE OF TRUTH partially mutated when a later file
    turned out to be missing or malformed: the earlier files had already been rewritten,
    the command then failed, and the tree was in neither the old state nor the new one.
    Acceptable for a derived tree; not for the source.
    """
    manifest = json.loads((out_dir / "manifest.json").read_bytes().decode("utf-8"))
    lineage = lineage_from_manifest(manifest)
    plan: list[tuple[Path, str]] = []
    for fname, (theme, story) in lineage.items():
        # Never read or write through an unvalidated manifest-supplied path (terra P1):
        # this is the one place the normal workflow REWRITES a file named by hand-edited JSON.
        unsafe = manifest_filename_problem(fname)
        if unsafe:
            raise ValueError(unsafe)
        path = out_dir / fname
        if not path.exists():
            continue
        actual = path.read_bytes().decode("utf-8")
        rendered = emit_task_file_text(
            TaskRow(id=_id_from_filename(fname), raw=extract_body(actual),
                    theme=theme, story=story))
        if rendered != actual:
            plan.append((path, rendered))
    return plan


def refresh_task_frontmatter(out_dir: Path) -> list[str]:
    """Plan-then-write wrapper over `plan_frontmatter_refresh`. Returns changed filenames.

    Kept as the single-call form for callers that do not need to interleave the plan with
    another validation step; `_cmd_emit_source` uses the two-phase form directly so that
    reassembly is proven to succeed before any source file is rewritten.
    """
    plan = plan_frontmatter_refresh(out_dir)
    for path, rendered in plan:
        path.write_text(rendered, encoding="utf-8", newline="\n")
    return [path.name for path, _ in plan]


# --- [#730] one-command row closure -----------------------------------------------
#
# `close_row` is the THREE coupled edits ADR-107 §6.3 already required a human to make by
# hand -- the body-marker append, the frontmatter `status: closed` (which `derive_status`
# cannot produce; see `emit_task_file_text`'s `status_override`), and removal of the row's
# node from `tasks/manifest.json` -- performed as ONE atomic write. `--prune`'s own refusal
# message already names the second and third steps as the sanctioned manual recipe; this is
# that recipe, mechanized, with the plan-then-write-with-rollback discipline
# `_cmd_emit_source` already established: a failure part-way must leave the tree exactly as
# it was, never half-closed.
_EVIDENCE_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
_CLOSE_MARKER_TEMPLATE = " · **CLOSED {date}** — evidence {evidence}"


def close_row_plan(
    out_dir: Path, task_id: int, evidence: str, closed_on: str
) -> list[tuple[Path, str]]:
    """PURE: compute the two writes `close_row` needs, as ONE plan. Writes nothing; raises
    ValueError on the first refusal, so a caller learns whether the close is even possible
    before touching disk (mirrors `plan_frontmatter_refresh`'s plan-then-write split).

    Refuses: a malformed `evidence` (not a 7-40 char lowercase-hex git sha); `task_id` not an
    OPEN row in the manifest (never filed, already closed, or retired); an unsafe or missing
    manifest `file` path; a task file that already carries a terminal status (double-close).
    """
    if not _EVIDENCE_SHA_RE.match(evidence):
        raise ValueError(
            f"close_row: --evidence {evidence!r} is not a git SHA (7-40 lowercase hex chars)")
    manifest_path = out_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    _require_well_formed_nodes(manifest)
    nodes = manifest["nodes"]
    node = next((n for n in nodes if n.get("task") == task_id), None)
    if node is None:
        raise ValueError(
            f"close_row: [#{task_id}] is not an open row in tasks/manifest.json "
            f"(already closed, retired, or never filed)")
    fname = node["file"]
    unsafe = manifest_filename_problem(fname)
    if unsafe:
        raise ValueError(unsafe)
    path = out_dir / fname
    if not path.exists():
        raise ValueError(f"close_row: manifest references a missing task file: {fname}")
    actual = path.read_bytes().decode("utf-8")
    body = extract_body(actual)
    status = frontmatter_status(actual)
    if status in _TERMINAL_STATUSES:
        raise ValueError(
            f"close_row: {fname} already carries a terminal status ({status!r}) -- "
            f"cannot close a row twice")

    lineage = lineage_from_manifest(manifest)
    theme, story = lineage.get(fname, (None, None))
    new_body = body + _CLOSE_MARKER_TEMPLATE.format(date=closed_on, evidence=evidence)
    rendered = emit_task_file_text(
        TaskRow(id=task_id, raw=new_body, theme=theme, story=story),
        status_override="closed")

    new_manifest = dict(manifest)
    new_manifest["nodes"] = [n for n in nodes if n is not node]
    manifest_text = json.dumps(new_manifest, ensure_ascii=False, indent=2) + "\n"
    return [(path, rendered), (manifest_path, manifest_text)]


def _cmd_close_row(out_dir: Path, task_id: int, evidence: str) -> int:
    """`--close-row ID --evidence SHA`. Plans first, then writes both files, rolling back to
    their prior bytes on ANY failure mid-write (same BaseException-safe pattern as
    `_cmd_emit_source`'s rollback, for the same reason: a torn write must not leave the row
    half-closed). Never touches `BACKLOG.md` -- that stays a separate `--emit-source`, exactly
    as the `--prune` refusal already documents for a hand-done retirement.
    """
    closed_on = datetime.date.today().isoformat()
    try:
        writes = close_row_plan(out_dir, task_id, evidence, closed_on)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        print(f"gen_task_tree: close-row FAIL (nothing written): {exc}", file=sys.stderr)
        return 1

    done: list[tuple[Path, bytes | None]] = []
    try:
        for path, text in writes:
            done.append((path, path.read_bytes() if path.exists() else None))
            path.write_text(text, encoding="utf-8", newline="\n")
    except BaseException as exc:
        for path, original in reversed(done):
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)
            except OSError:
                print(f"gen_task_tree: ROLLBACK FAILED for {path.name} — inspect the tree "
                      f"before retrying", file=sys.stderr)
        print(f"gen_task_tree: close-row FAIL (rolled back, nothing changed): {exc!r}",
              file=sys.stderr)
        if not isinstance(exc, OSError):
            raise
        return 1

    print(f"gen_task_tree: closed [#{task_id}] -- body marker + status: closed + manifest "
          f"node removed (evidence {evidence}). Run --emit-source to drop the row from "
          f"BACKLOG.md.")
    return 0


# --- [#566] the ranking axis ------------------------------------------------------
# The [#488] axis LEAN, accepted by the architect 2026-08-20 and measured in
# docs/audits/2026-08-19-technical-c4-ruling-prework.md §2.5: rank by CONSTRAINT
# CONTENTION over `serialize-group`, layered as a TIEBREAK UNDER the hand-set
# [P1..P3] rather than replacing it, with `P-enum + age` (the monotonic,
# ledger-backed id as a free age proxy) as the zero-cost floor beneath both.
#
# The whole axis is DERIVED. It authors no field: priority, serialize-group and id
# are all already parsed out of a task's own body line, so ranking adds nothing to
# maintain and cannot rot independently of the queue it ranks. That is the property
# the LEAN was chosen for -- WSJF would have needed 732 new estimates across 183
# open rows, and the row's own graph-centrality candidate is inert on a 3-edge
# population.
#
# Nothing here writes. Ranking is a REPORT over the source tree, deliberately not a
# reordering of BACKLOG.md: document order is carried by tasks/manifest.json and is
# the operator's narrative structure (themes, stories, prose), which the byte-exact
# reassembly contract depends on. A rank materialised into frontmatter would also be
# a field whose value changes when a DIFFERENT row is filed or closed, churning every
# task file in a group on every edit.
_PRIORITY_RANK = {"P1": 0, "P2": 1, "P3": 2}
_UNPRIORITIZED_RANK = len(_PRIORITY_RANK)  # a row with no [P#] sorts after every P3


@dataclass(frozen=True)
class RankedTask:
    """One row's place in the ranking, plus the three inputs that put it there."""

    rank: int
    id: int
    priority: str | None
    serialize_group: str | None
    contention: int
    title: str


def open_task_rows(rows: list[TaskRow]) -> list[TaskRow]:
    """The ranked population: rows whose own line does not carry the DEFER marker.

    A deferred row is out of the queue by the operator's own decision, so ranking it
    would put a row nobody may pick up in front of one they may.
    """
    return [task for task in rows if derive_status(task.raw) == "open"]


def contention_scores(rows: list[TaskRow]) -> dict[int, int]:
    """id -> how many OTHER rows in the same `serialize-group`; 0 when ungrouped.

    `serialize-group` exists precisely because a shared file serializes lanes, so the
    count is a standing measure of how much parallel work the group is holding.

    HONEST LIMIT, stated where the number is produced: this ranks THROUGHPUT, not
    value. `(group size - 1)` is what the group CONTENDS over, which equals what a
    completion frees only for the row that dissolves or shrinks the group; a row that
    merely shares the file scores the same. It is a strong secondary key and a poor
    sole one, which is why [P1..P3] stays primary.
    """
    sizes: dict[str, int] = {}
    groups: dict[int, str | None] = {}
    for task in rows:
        group = derive_serialize_group(task.raw)
        groups[task.id] = group
        if group is not None:
            sizes[group] = sizes.get(group, 0) + 1
    return {task_id: (sizes[group] - 1 if group is not None else 0)
            for task_id, group in groups.items()}


def rank_key(task: TaskRow, contention: int) -> tuple[int, int, int]:
    """The total order, primary key first: P-enum, then contention DESC, then id ASC.

    Total by construction -- ids are unique -- so the ordering is deterministic and a
    regen cannot shuffle equal rows.
    """
    return (_PRIORITY_RANK.get(derive_priority(task.raw), _UNPRIORITIZED_RANK),
            -contention, task.id)


def rank_tasks(rows: list[TaskRow]) -> list[RankedTask]:
    """Rank the open rows of `rows`. Pure; deferred rows are filtered out here.

    Contention is counted over the SAME filtered population, so a group whose members
    are mostly deferred is scored on what actually contends today.
    """
    live = open_task_rows(rows)
    scores = contention_scores(live)
    ordered = sorted(live, key=lambda task: rank_key(task, scores[task.id]))
    return [RankedTask(rank=position, id=task.id, priority=derive_priority(task.raw),
                       serialize_group=derive_serialize_group(task.raw),
                       contention=scores[task.id], title=derive_title(task.raw))
            for position, task in enumerate(ordered, start=1)]


def render_ranking(ranked: list[RankedTask], top: int | None = None) -> str:
    """Flat, un-padded report text (no column padding, per the output-formatting rule)."""
    shown = ranked if top is None else ranked[:top]
    lines = [
        f"gen_task_tree: {len(ranked)} open task(s) ranked — key: [P1..P3] primary · "
        f"constraint-contention over serialize-group as the tiebreak within a tier · "
        f"id (age proxy) as the floor",
        "gen_task_tree: contention measures THROUGHPUT, not value — it orders a tie "
        "block, it never overrides a hand-set P.",
    ]
    for row in shown:
        lines.append(
            f"{row.rank}. [#{row.id}] {row.priority or 'P?'} · contention "
            f"{row.contention} · group {row.serialize_group or 'none'} · {row.title}")
    if top is not None and len(ranked) > len(shown):
        lines.append(f"… {len(ranked) - len(shown)} more not shown "
                     f"(omit --rank-top to list every open row)")
    return "\n".join(lines)


def _cmd_rank(out_dir: Path, top: int | None = None) -> int:
    """READ-ONLY: rank the open queue from the SOURCE tree, print, write nothing.

    Reads `tasks/`, not `BACKLOG.md`: post-flip the tree is the source of truth, and
    ranking the derived file would rank a copy that `--check` might already be calling
    stale. Any structural problem is reported as a controlled failure -- a rank is a
    report, so it must not traceback on a tree `--check` would red.
    """
    try:
        rows = _task_rows(parse_backlog(reassemble_from_tree(out_dir)))
    except (OSError, ValueError, KeyError, AssertionError, UnicodeDecodeError) as exc:
        print(f"gen_task_tree: rank FAIL (nothing written): {exc}", file=sys.stderr)
        return 1
    ranked = rank_tasks(rows)
    deferred = len(rows) - len(ranked)
    print(render_ranking(ranked, top=top))
    if deferred:
        print(f"gen_task_tree: {deferred} deferred row(s) excluded (· DEFER)")
    return 0


def _cmd_check(source_path: Path, out_dir: Path) -> int:
    """Thin CLI printer over `find_incoherences` — behaviour and exit codes unchanged."""
    problems = find_incoherences(source_path, out_dir)
    if problems:
        for problem in problems:
            print(f"gen_task_tree: check FAIL: {problem}", file=sys.stderr)
        return 1
    print("gen_task_tree: check ok")
    return 0


def _cmd_roundtrip(out_dir: Path) -> int:
    """Lossless proof over the CANONICAL full-body text ([#589] re-pointed this).

    It used to read `BACKLOG.md`, which was the same bytes. Post-[#589] that file is the
    one-line projection, and round-tripping it would still print `roundtrip ok` while
    proving something worthless -- the projection reassembles trivially because
    `parse_backlog` preserves whatever lines it is given. The claim worth making is that
    the SOURCE TREE reassembles losslessly, so that is what this reads.
    """
    try:
        text = reassemble_from_tree(out_dir)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        print(f"gen_task_tree: roundtrip FAIL: {exc}", file=sys.stderr)
        return 1
    try:
        model = parse_backlog(text)
    except (ValueError, AssertionError) as exc:
        print(f"gen_task_tree: roundtrip FAIL: {exc}", file=sys.stderr)
        return 1
    if reassemble_from_model(model) != text:
        print("gen_task_tree: roundtrip FAIL: reassembled text does not match source", file=sys.stderr)
        return 1
    print("gen_task_tree: roundtrip ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gen_task_tree",
        description="Split/emit BACKLOG.md into a per-task file tree under tasks/ (ADR-80 gen_* pattern)",
    )
    parser.add_argument("--emit-source", action="store_true", dest="emit_source",
                        help="THE NORMAL REGEN: rebuild BACKLOG.md from the tasks/ tree")
    parser.add_argument("--check", action="store_true",
                        help="verify BACKLOG.md matches what tasks/ generates, and that every "
                             "task file's frontmatter matches its own body")
    parser.add_argument("--roundtrip", action="store_true", help="verify in-memory lossless reassembly")
    parser.add_argument("--rank", action="store_true",
                        help="READ-ONLY report ([#566]/[#488] LEAN): rank the OPEN queue by "
                             "[P1..P3], breaking ties on constraint-contention over "
                             "serialize-group, then on id as an age proxy. Writes nothing")
    parser.add_argument("--rank-top", type=int, default=None, dest="rank_top", metavar="N",
                        help="with --rank only: show the top N rows instead of every open row")
    parser.add_argument("--write", action="store_true",
                        help="IMPORT/RECOVERY: rebuild the tasks/ tree from BACKLOG.md. Post-flip "
                             "this overwrites the source of truth from a generated file; against "
                             "a populated tasks/ tree it REFUSES unless --force ([#474])")
    parser.add_argument("--prune", action="store_true",
                        help="REFUSED since the [#439] flip — see ADR-107 §6.3 (retire, never delete)")
    parser.add_argument("--close-row", type=int, default=None, dest="close_row", metavar="ID",
                        help="[#730] one-command closure: close row [#ID] atomically -- body "
                             "marker + status: closed + manifest node removal. Requires "
                             "--evidence; run --emit-source afterward to drop the row from "
                             "BACKLOG.md")
    parser.add_argument("--evidence", type=str, default=None, metavar="SHA",
                        help="with --close-row only: the commit SHA proving the row's Done-when")
    parser.add_argument("--force", action="store_true",
                        help="with --write only ([#474]): override a warned refusal (populated "
                             "tasks/ tree); loud, names every condition it overrides")
    parser.add_argument("--source", type=Path, default=None,
                        help="BACKLOG.md path — the GENERATED file (default: repo root)")
    parser.add_argument("--out", type=Path, default=None,
                        help="tasks/ tree dir — the SOURCE OF TRUTH (default: repo root/tasks)")
    args = parser.parse_args(argv)

    if args.force and not args.write:
        parser.error("--force is only meaningful with --write ([#474])")
    if args.rank_top is not None and not args.rank:
        parser.error("--rank-top is only meaningful with --rank ([#566])")
    if args.rank_top is not None and args.rank_top < 1:
        parser.error("--rank-top must be >= 1 (omit it to list every open row)")
    if args.close_row is not None and args.evidence is None:
        parser.error("--close-row requires --evidence <sha> ([#730])")
    if args.evidence is not None and args.close_row is None:
        parser.error("--evidence is only meaningful with --close-row ([#730])")

    source_path = args.source if args.source is not None else _DEFAULT_SOURCE
    out_dir = args.out if args.out is not None else _DEFAULT_OUT

    if args.prune:
        print("gen_task_tree: --prune is REFUSED since the [#439] source-of-truth flip.\n"
              "  Task files are the SOURCE now, so pruning one deletes source and frees its id\n"
              "  for re-issue. ADR-107 §6.3 rules retire-not-delete: retire a task by removing\n"
              "  its node from tasks/manifest.json (it leaves BACKLOG.md on the next\n"
              "  --emit-source) and LEAVE the file in place as the allocation record.",
              file=sys.stderr)
        return 2
    if args.emit_source:
        return _cmd_emit_source(source_path, out_dir)
    if args.check:
        return _cmd_check(source_path, out_dir)
    if args.roundtrip:
        return _cmd_roundtrip(out_dir)
    if args.rank:
        return _cmd_rank(out_dir, top=args.rank_top)
    if args.write:
        return _cmd_write(source_path, out_dir, force=args.force)
    if args.close_row is not None:
        return _cmd_close_row(out_dir, args.close_row, args.evidence)

    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
