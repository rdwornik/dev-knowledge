#!/usr/bin/env python
"""gen_task_tree.py -- [#433] BACKLOG restructure strangler STEP 1-2.

Deterministic splitter/emitter for BACKLOG.md: parses the file into a lossless
line model, emits a per-task file tree under tasks/ (one frontmattered .md per
task) plus a tasks/manifest.json structure manifest, and reassembles BACKLOG.md
BYTE-IDENTICALLY from that tree.

This is a gen_* family committed-generated-zone writer (ADR-80 pattern, same
posture as gen_audit_index.py): it writes ONLY under the output tree, and only
when invoked with --write. It NEVER deletes anything on disk -- a stray file
under the output tree that looks task-shaped is reported, never touched.

BACKLOG.md remains the single source of truth until a later flip arc retires
it in favor of the tree; this module only builds the derived, disposable side.
Reassembly is byte-identical BY CONSTRUCTION (the line model preserves every
original physical line verbatim) and is ASSERTED at parse time (parse_backlog
refuses to return a model that does not reassemble back to its own input), and
re-verified by the --roundtrip / --check CLI verbs against disk state.
"""

from __future__ import annotations

import argparse
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
_DEFER_MARKER = "· DEFER"
_TITLE_STRIP_RE = re.compile(r"^- \[#\d+\] (?:\[P\d\](?:\[[SML]\])?)?\s*(.*)$")
_TITLE_FALLBACK_DELIMS = (" — ", " (", ": ", " · ")

_ORPHAN_RE = re.compile(r"^\d+-.*\.md$")


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


def emit_task_file_text(task: TaskRow) -> str:
    """Render one task's frontmattered .md file text.

    Fixed key order (id, title, status, priority?, size?, theme?, story?,
    serialize-group?, depends-on?, source, derived); optional keys are omitted
    when their deriver returns None (or, for theme/story, when the TaskRow field
    itself is None).
    """
    lines = ["---", f'id: "[#{task.id}]"']
    lines.append(f"title: {json.dumps(derive_title(task.raw), ensure_ascii=False)}")
    lines.append(f"status: {derive_status(task.raw)}")
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
    lines.append("source: BACKLOG.md")
    lines.append("derived: true")
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
    """tasks/manifest.json text: schema + source hash + one entry per node, in order."""
    nodes_out: list[dict[str, object]] = []
    for kind, payload in model.nodes:
        if kind == "task":
            nodes_out.append({"task": payload.id, "file": fname_by_id[payload.id]})
        else:
            nodes_out.append({"prose": payload})
    manifest = {
        "schema": 1,
        "source": "BACKLOG.md",
        "source_sha256": hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
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


def _is_generator_emitted(path: Path) -> bool:
    """True iff the file carries BOTH provenance marker lines this generator writes
    (`source: BACKLOG.md` + `derived: true`) inside its frontmatter. The prune path
    (terra P1, 2026-07-27) deletes ONLY files that prove this provenance -- a
    hand-authored task-shaped file is never touched."""
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return "\nsource: BACKLOG.md\n" in text and "\nderived: true\n" in text


def write_tree(model: Model, out_dir: Path, prune: bool = False) -> list[str]:
    """Write every task file + manifest.json under out_dir.

    By default NEVER deletes or truncates anything else already there: a
    pre-existing file that looks task-shaped (matches _ORPHAN_RE) but is not part
    of this emission set is left untouched and reported to stdout as an orphan.

    With prune=True (the explicit `--write --prune` verb; terra P1 fix), a
    task-shaped file OUTSIDE the emission set is deleted IFF it carries this
    generator's own provenance markers (_is_generator_emitted) -- the retired-task
    lifecycle: a task line leaving BACKLOG.md retires its derived file. A
    task-shaped file WITHOUT the markers is still only reported, never deleted.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    tasks = _task_rows(model)
    fname_by_id = _fname_map(tasks)

    written: list[str] = []
    for task in tasks:
        fname = fname_by_id[task.id]
        (out_dir / fname).write_text(emit_task_file_text(task), encoding="utf-8", newline="\n")
        written.append(fname)

    (out_dir / "manifest.json").write_text(render_manifest(model, fname_by_id), encoding="utf-8", newline="\n")
    written.append("manifest.json")

    emitted = set(fname_by_id.values())
    for p in sorted(out_dir.iterdir()):
        if p.is_file() and _ORPHAN_RE.match(p.name) and p.name not in emitted:
            if prune and _is_generator_emitted(p):
                p.unlink()
                print(f"gen_task_tree: pruned retired task file: {p.name}")
            else:
                print(f"gen_task_tree: orphan (not touched): {p.name}")

    return written


def reassemble_from_tree(tree_dir: Path) -> str:
    """Read manifest.json + every task file back into the original BACKLOG.md text.

    This is the proof that tree+manifest carry every byte of the source: a prose
    node contributes its literal string, a task node contributes extract_body of
    its file's bytes (strict utf-8 decode), and the whole thing is '\\n'-joined.
    """
    manifest = json.loads((tree_dir / "manifest.json").read_bytes().decode("utf-8"))
    parts: list[str] = []
    for node in manifest["nodes"]:
        if "task" in node:
            file_text = (tree_dir / node["file"]).read_bytes().decode("utf-8")
            parts.append(extract_body(file_text))
        else:
            parts.append(node["prose"])
    return "\n".join(parts)


def _cmd_write(source_path: Path, out_dir: Path, prune: bool = False) -> int:
    text = source_path.read_bytes().decode("utf-8")
    model = parse_backlog(text)
    write_tree(model, out_dir, prune=prune)
    task_count = sum(1 for kind, _ in model.nodes if kind == "task")
    print(f"gen_task_tree: wrote {task_count} task file(s) + manifest to {out_dir}")
    return 0


def _cmd_check(source_path: Path, out_dir: Path) -> int:
    try:
        text = source_path.read_bytes().decode("utf-8")
    except OSError as exc:
        print(f"gen_task_tree: check FAIL: cannot read source {source_path}: {exc}", file=sys.stderr)
        return 1
    try:
        model = parse_backlog(text)
    except (ValueError, AssertionError) as exc:
        print(f"gen_task_tree: check FAIL: parse error: {exc}", file=sys.stderr)
        return 1

    tasks = _task_rows(model)
    try:
        fname_by_id = _fname_map(tasks)
    except ValueError as exc:
        print(f"gen_task_tree: check FAIL: {exc}", file=sys.stderr)
        return 1

    if not out_dir.exists():
        print(f"gen_task_tree: check FAIL: output dir missing: {out_dir}", file=sys.stderr)
        return 1

    problems: list[str] = []
    for task in tasks:
        fname = fname_by_id[task.id]
        disk_path = out_dir / fname
        if not disk_path.exists():
            problems.append(f"missing task file: {fname}")
            continue
        expected = emit_task_file_text(task)
        actual = disk_path.read_bytes().decode("utf-8")
        if actual != expected:
            problems.append(f"task file content differs from expected: {fname}")

    expected_manifest = render_manifest(model, fname_by_id)
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        problems.append("missing manifest.json")
    else:
        actual_manifest = manifest_path.read_bytes().decode("utf-8")
        if actual_manifest != expected_manifest:
            problems.append("manifest.json differs from expected")

    emitted = set(fname_by_id.values())
    for p in sorted(out_dir.iterdir()):
        if p.is_file() and _ORPHAN_RE.match(p.name) and p.name not in emitted:
            problems.append(f"orphan task-shaped file: {p.name} "
                            f"(a retired derived file is removed by --write --prune)")

    try:
        if reassemble_from_tree(out_dir) != text:
            problems.append("reassemble_from_tree(out_dir) does not match source text")
    except (OSError, ValueError, KeyError) as exc:
        problems.append(f"reassemble_from_tree failed: {exc}")

    if problems:
        for problem in problems:
            print(f"gen_task_tree: check FAIL: {problem}", file=sys.stderr)
        return 1
    print("gen_task_tree: check ok")
    return 0


def _cmd_roundtrip(source_path: Path) -> int:
    text = source_path.read_bytes().decode("utf-8")
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
    parser.add_argument("--write", action="store_true", help="parse source and write the task tree + manifest")
    parser.add_argument("--check", action="store_true", help="verify the on-disk tree matches the source")
    parser.add_argument("--roundtrip", action="store_true", help="verify in-memory lossless reassembly")
    parser.add_argument("--prune", action="store_true",
                        help="with --write: delete a retired task file that carries this "
                             "generator's own provenance markers (never a foreign file)")
    parser.add_argument("--source", type=Path, default=None, help="source BACKLOG.md path (default: repo root)")
    parser.add_argument("--out", type=Path, default=None, help="output tree dir (default: repo root/tasks)")
    args = parser.parse_args(argv)

    source_path = args.source if args.source is not None else _DEFAULT_SOURCE
    out_dir = args.out if args.out is not None else _DEFAULT_OUT

    if args.prune and not args.write:
        print("gen_task_tree: --prune is only valid together with --write", file=sys.stderr)
        return 2
    if args.write:
        return _cmd_write(source_path, out_dir, prune=args.prune)
    if args.check:
        return _cmd_check(source_path, out_dir)
    if args.roundtrip:
        return _cmd_roundtrip(source_path)

    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
